:mod:`!optparse` --- Bộ phân tích cú pháp cho các tùy chọn dòng lệnh
====================================================================

.. module:: optparse
   :synopsis: Thư viện phân tích cú pháp tùy chọn dòng lệnh.

.. moduleauthor:: Greg Ward <gward@python.net>
.. sectionauthor:: Greg Ward <gward@python.net>

**Mã nguồn:** :source:`Lib/optparse.py`

--------------

.. _choosing-an-argument-parser:

Chọn thư viện phân tích cú pháp đối số
--------------------------------------

Thư viện chuẩn bao gồm ba thư viện phân tích cú pháp đối số:

* :mod:`getopt`: một mô-đun gần như phản chiếu API thủ tục của C ``getopt``.
* :mod:`!optparse`: một lựa chọn thay thế mang tính khai báo cho ``getopt``, cung cấp chức năng tương đương mà không yêu cầu mỗi ứng dụng phải tự triển khai logic phân tích cú pháp tùy chọn mang tính thủ tục.
* :mod:`argparse`: một lựa chọn thay thế có tính định hướng rõ ràng hơn cho ``optparse``, cung cấp nhiều chức năng hơn theo mặc định, đổi lại ứng dụng sẽ kém linh hoạt hơn trong việc kiểm soát chính xác cách các đối số được xử lý.

Nếu không có các ràng buộc thiết kế cụ thể hơn đối với việc phân tích đối số, :mod:`argparse` là lựa chọn được khuyến nghị để triển khai các ứng dụng dòng lệnh, vì nó cung cấp mức chức năng cơ sở cao nhất với ít mã ở cấp ứng dụng nhất.

:mod:`getopt` gần như chỉ được duy trì vì lý do tương thích ngược. Tuy nhiên, nó cũng phục vụ một trường hợp sử dụng chuyên biệt như một công cụ để tạo nguyên mẫu và kiểm thử việc xử lý đối số dòng lệnh trong các ứng dụng C dựa trên ``getopt``.

Nên cân nhắc :mod:`!optparse` như một lựa chọn thay thế cho :mod:`argparse` trong các trường hợp sau:

* ứng dụng đã sử dụng :mod:`!optparse` và không muốn mạo hiểm với những thay đổi hành vi tinh vi có thể phát sinh khi chuyển sang :mod:`argparse`
* ứng dụng yêu cầu kiểm soát nhiều hơn đối với cách các tùy chọn và tham số vị trí được đan xen trên dòng lệnh (bao gồm khả năng tắt hoàn toàn tính năng đan xen)
* ứng dụng yêu cầu kiểm soát nhiều hơn đối với việc phân tích tăng dần các thành phần dòng lệnh (mặc dù ``argparse`` có hỗ trợ việc này, cách thức chính xác mà nó hoạt động trên thực tế không phù hợp với một số trường hợp sử dụng)
* ứng dụng cần kiểm soát nhiều hơn việc xử lý các tùy chọn chấp nhận giá trị tham số có thể bắt đầu bằng ``-`` (chẳng hạn như các tùy chọn được ủy quyền để truyền cho các tiến trình con được gọi)
* ứng dụng cần một số hành vi xử lý tham số dòng lệnh khác mà ``argparse`` không hỗ trợ, nhưng có thể được triển khai dựa trên giao diện cấp thấp hơn do ``optparse`` cung cấp

Những cân nhắc này cũng có nghĩa là :mod:`!optparse` có khả năng cung cấp nền tảng tốt hơn cho các tác giả thư viện xây dựng các thư viện xử lý đối số dòng lệnh của bên thứ ba.

Hãy xem xét cụ thể hai cấu hình phân tích đối số dòng lệnh sau đây: cấu hình đầu tiên sử dụng ``optparse``, còn cấu hình thứ hai sử dụng ``argparse``:

.. testcode::

   import optparse

   if __name__ == '__main__':
       parser = optparse.OptionParser()
       parser.add_option('-o', '--output')
       parser.add_option('-v', dest='verbose', action='store_true')
       opts, args = parser.parse_args()
       process(args, output=opts.output, verbose=opts.verbose)

.. testcode::

   import argparse

   if __name__ == '__main__':
       parser = argparse.ArgumentParser()
       parser.add_argument('-o', '--output')
       parser.add_argument('-v', dest='verbose', action='store_true')
       parser.add_argument('rest', nargs='*')
       args = parser.parse_args()
       process(args.rest, output=args.output, verbose=args.verbose)

Điểm khác biệt rõ ràng nhất là trong phiên bản ``optparse``, các đối số không phải tùy chọn được ứng dụng xử lý riêng sau khi hoàn tất việc xử lý tùy chọn. Trong phiên bản ``argparse``, các đối số vị trí được khai báo và xử lý theo cùng cách với các tùy chọn được đặt tên.

Tuy nhiên, phiên bản ``argparse`` cũng sẽ xử lý một số tổ hợp tham số khác với cách mà phiên bản ``optparse`` xử lý. Ví dụ (ngoài những khác biệt khác):

* cung cấp ``-o -v`` sẽ cho ``output="-v"`` và ``verbose=False`` khi sử dụng ``optparse``, nhưng gây ra lỗi sử dụng với ``argparse`` (báo rằng chưa cung cấp giá trị nào cho ``-o/--output``, vì ``-v`` được diễn giải là cờ độ chi tiết)
* tương tự, cung cấp ``-o --`` cho kết quả ``output="--"`` và ``args=()`` khi sử dụng ``optparse``, nhưng gây ra lỗi sử dụng với ``argparse`` (đồng thời phàn nàn rằng chưa cung cấp giá trị cho ``-o/--output``, vì ``--`` được hiểu là kết thúc quá trình xử lý tùy chọn và coi tất cả giá trị còn lại là đối số vị trí)
* cung cấp ``-o=foo`` cho kết quả ``output="=foo"`` khi sử dụng ``optparse``, nhưng cho kết quả ``output="foo"`` với ``argparse`` (vì ``=`` được xử lý đặc biệt như một dấu phân cách thay thế cho các giá trị tham số của tùy chọn)

Việc những hành vi khác nhau này trong phiên bản ``argparse`` được xem là mong muốn hay là một vấn đề sẽ phụ thuộc vào trường hợp sử dụng cụ thể của ứng dụng dòng lệnh.

.. seealso::

    :pypi:`click` là một thư viện xử lý đối số của bên thứ ba (ban đầu dựa trên ``optparse``), cho phép phát triển các ứng dụng dòng lệnh dưới dạng một tập hợp các hàm triển khai lệnh có gắn decorator.

    Các thư viện bên thứ ba khác, chẳng hạn như :pypi:`typer` hoặc :pypi:`msgspec-click`, cho phép chỉ định giao diện dòng lệnh theo những cách tích hợp hiệu quả hơn với việc kiểm tra tĩnh các chú thích kiểu của Python.


Giới thiệu
----------

:mod:`!optparse` là một thư viện thuận tiện, linh hoạt và mạnh mẽ hơn để phân tích các tùy chọn dòng lệnh so với mô-đun tối giản :mod:`getopt`.
:mod:`!optparse` sử dụng phong cách khai báo rõ ràng hơn để phân tích dòng lệnh: bạn tạo một thực thể :class:`OptionParser`, điền các tùy chọn vào đó rồi phân tích dòng lệnh.
:mod:`!optparse` cho phép người dùng chỉ định các tùy chọn theo cú pháp GNU/POSIX thông dụng, đồng thời tự động tạo thông báo usage và help cho bạn.

Sau đây là ví dụ sử dụng :mod:`!optparse` trong một script đơn giản::

   from optparse import OptionParser
   ...
   parser = OptionParser()
   parser.add_option("-f", "--file", dest="filename",
                     help="write report to FILE", metavar="FILE")
   parser.add_option("-q", "--quiet",
                     action="store_false", dest="verbose", default=True,
                     help="don't print status messages to stdout")

   (options, args) = parser.parse_args()

Với vài dòng mã này, giờ đây người dùng script của bạn có thể thực hiện "cách thông thường" trên dòng lệnh, chẳng hạn như::

   <yourscript> --file=outfile -q

Khi phân tích dòng lệnh, :mod:`!optparse` thiết lập các thuộc tính của đối tượng ``options`` được :meth:`~OptionParser.parse_args` trả về dựa trên các giá trị dòng lệnh do người dùng cung cấp. Khi :meth:`~OptionParser.parse_args` trả về sau khi phân tích dòng lệnh này, ``options.filename`` sẽ là ``"outfile"`` và ``options.verbose`` sẽ là ``False``. :mod:`!optparse` hỗ trợ cả tùy chọn dài và tùy chọn ngắn, cho phép gộp các tùy chọn ngắn với nhau, đồng thời cho phép liên kết tùy chọn với đối số của chúng theo nhiều cách khác nhau. Do đó, các dòng lệnh sau đây đều tương đương với ví dụ trên::

   <yourscript> -f outfile --quiet
   <yourscript> --quiet --file outfile
   <yourscript> -q -foutfile
   <yourscript> -qfoutfile

Ngoài ra, người dùng có thể chạy một trong các lệnh sau::

   <yourscript> -h
   <yourscript> --help

và :mod:`!optparse` sẽ in ra bản tóm tắt ngắn gọn về các tùy chọn của script:

.. code-block:: text

   Usage: <yourscript> [options]

   Options:
     -h, --help            show this help message and exit
     -f FILE, --file=FILE  write report to FILE
     -q, --quiet           don't print status messages to stdout

trong đó giá trị của *yourscript* được xác định tại runtime (thông thường từ ``sys.argv[0]``).


.. _optparse-background:

Bối cảnh
--------

:mod:`!optparse` được thiết kế rõ ràng nhằm khuyến khích việc tạo ra các chương trình có giao diện command-line đơn giản, tuân theo các quy ước do họ hàm :c:func:`!getopt` thiết lập, vốn có sẵn cho các lập trình viên C. Vì mục đích đó, nó chỉ hỗ trợ cú pháp và ngữ nghĩa command-line phổ biến nhất thường được sử dụng trong Unix. Nếu bạn chưa quen với các quy ước này, việc đọc phần này sẽ giúp bạn làm quen với chúng.


.. _optparse-terminology:

Thuật ngữ
^^^^^^^^^

đối số
   một chuỗi được nhập trên command-line và được shell truyền cho ``execl()`` hoặc ``execv()``. Trong Python, các đối số là những phần tử của ``sys.argv[1:]`` (``sys.argv[0]`` là tên của chương trình đang được thực thi). Các Unix shell cũng sử dụng thuật ngữ "word".

   Đôi khi bạn có thể muốn thay thế một danh sách đối số khác cho ``sys.argv[1:]``, vì vậy hãy hiểu "đối số" là "một phần tử của ``sys.argv[1:]``, hoặc của một danh sách khác được cung cấp để thay thế cho ``sys.argv[1:]``".

tùy chọn
   một đối số được dùng để cung cấp thêm thông tin nhằm định hướng hoặc tùy chỉnh việc thực thi một chương trình. Có nhiều cú pháp khác nhau cho tùy chọn; cú pháp Unix truyền thống là một dấu gạch nối ("-") theo sau bởi một chữ cái đơn, ví dụ ``-x`` hoặc ``-F``. Ngoài ra, cú pháp Unix truyền thống cho phép gộp nhiều tùy chọn vào một đối số duy nhất, ví dụ ``-x -F`` tương đương với ``-xF``. Dự án GNU đã giới thiệu ``--`` theo sau bởi một chuỗi các từ được phân tách bằng dấu gạch nối, ví dụ ``--file`` hoặc ``--dry-run``. Đây là hai cú pháp tùy chọn duy nhất được :mod:`!optparse` cung cấp.

   Một số cú pháp tùy chọn khác từng xuất hiện gồm:

   * một dấu gạch nối theo sau bởi một vài chữ cái, ví dụ ``-pf`` (điều này *không* giống với nhiều tùy chọn được gộp vào một đối số duy nhất)

   * một dấu gạch nối theo sau bởi một từ hoàn chỉnh, ví dụ ``-file`` (về mặt kỹ thuật, điều này tương đương với cú pháp trước đó, nhưng chúng thường không xuất hiện trong cùng một chương trình)

   * một dấu cộng theo sau bởi một chữ cái đơn, một vài chữ cái hoặc một từ, ví dụ ``+f``, ``+rgb``

   * một dấu gạch chéo theo sau bởi một chữ cái, một vài chữ cái hoặc một từ, ví dụ ``/f``, ``/file``

   :mod:`!optparse` không hỗ trợ các cú pháp tùy chọn này và sẽ không bao giờ hỗ trợ. Đây là chủ ý: ba cú pháp đầu tiên không phải là tiêu chuẩn trong bất kỳ môi trường nào, còn cú pháp cuối chỉ có ý nghĩa nếu bạn chỉ nhắm đến Windows hoặc một số nền tảng cũ (ví dụ: VMS, MS-DOS).

đối số của tùy chọn
   một đối số đứng sau một tùy chọn, liên kết chặt chẽ với tùy chọn đó và được lấy khỏi danh sách đối số khi tùy chọn đó được xử lý. Với
   :mod:`!optparse`, đối số của tùy chọn có thể nằm trong một đối số riêng biệt với tùy chọn đó:

   .. code-block:: text

      -f foo
      --file foo

   hoặc được đưa vào cùng một đối số:

   .. code-block:: text

      -ffoo
      --file=foo

   Thông thường, một tùy chọn nhất định либо nhận một đối số, либо không. Nhiều người muốn có tính năng "đối số tùy chọn tùy ý", nghĩa là một số tùy chọn sẽ nhận một đối số nếu thấy đối số đó và không nhận nếu không thấy. Điều này gây tranh cãi phần nào vì khiến việc phân tích cú pháp trở nên mơ hồ: nếu ``-a`` nhận một đối số tùy ý và ``-b`` là một tùy chọn hoàn toàn khác, chúng ta diễn giải ``-ab`` như thế nào? Do sự mơ hồ này, :mod:`!optparse` không hỗ trợ tính năng này.

đối số vị trí
   thứ gì đó còn lại trong danh sách đối số sau khi các tùy chọn đã được phân tích cú pháp, tức là sau khi các tùy chọn và đối số của chúng đã được phân tích cú pháp và loại bỏ khỏi danh sách đối số.

tùy chọn bắt buộc
   một tùy chọn phải được cung cấp trên dòng lệnh; lưu ý rằng cụm từ "tùy chọn bắt buộc" tự mâu thuẫn trong tiếng Anh. :mod:`!optparse` không ngăn bạn triển khai các tùy chọn bắt buộc, nhưng cũng không hỗ trợ nhiều cho việc đó.

Ví dụ, hãy xét dòng lệnh giả định sau::

   prog -v --report report.txt foo bar

``-v`` và ``--report`` đều là các tùy chọn. Giả sử ``--report`` nhận một đối số, ``report.txt`` là một đối số của tùy chọn. ``foo`` và ``bar`` là các đối số vị trí.


.. _optparse-what-options-for:

Các tùy chọn dùng để làm gì?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các tùy chọn được dùng để cung cấp thêm thông tin nhằm tinh chỉnh hoặc tùy chỉnh việc thực thi một chương trình. Nếu điều này chưa rõ, các tùy chọn thường là *tùy chọn*. Một chương trình phải có thể chạy bình thường mà không cần bất kỳ tùy chọn nào. (Hãy chọn ngẫu nhiên một chương trình trong các bộ công cụ Unix hoặc GNU. Nó có thể chạy mà không cần tùy chọn nào mà vẫn hợp lý không? Các ngoại lệ chính là ``find``, ``tar`` và ``dd``\ ---tất cả đều là những trường hợp kỳ quặc đột biến đã bị chỉ trích chính đáng vì cú pháp không theo chuẩn và giao diện khó hiểu.)

Nhiều người muốn chương trình của mình có "tùy chọn bắt buộc". Hãy thử suy nghĩ: nếu đã bắt buộc thì *không phải là tùy chọn*! Nếu có một mẩu thông tin mà chương trình của bạn nhất thiết cần để chạy thành công, đó chính là lúc dùng các đối số vị trí.

Để lấy một ví dụ về thiết kế giao diện dòng lệnh tốt, hãy xem xét tiện ích ``cp`` đơn giản dùng để sao chép tệp. Việc cố sao chép tệp mà không cung cấp đích đến và ít nhất một nguồn sẽ chẳng có nhiều ý nghĩa. Vì vậy, ``cp`` sẽ báo lỗi nếu bạn chạy nó mà không có đối số nào. Tuy nhiên, nó có cú pháp linh hoạt, hữu ích và hoàn toàn không yêu cầu tùy chọn nào::

   cp SOURCE DEST
   cp SOURCE ... DEST-DIR

Chỉ với vậy, bạn đã có thể làm được khá nhiều việc. Hầu hết các triển khai của ``cp`` đều cung cấp nhiều tùy chọn để điều chỉnh chính xác cách sao chép tệp: bạn có thể giữ nguyên mode và thời gian sửa đổi, tránh đi theo symlink, yêu cầu xác nhận trước khi ghi đè các tệp hiện có, v.v. Nhưng không điều nào trong số đó làm phân tâm khỏi nhiệm vụ cốt lõi của ``cp``, đó là sao chép một tệp sang một tệp khác hoặc sao chép nhiều tệp vào một thư mục khác.


.. _optparse-what-positional-arguments-for:

Các đối số vị trí dùng để làm gì?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các đối số vị trí dùng cho những mẩu thông tin mà chương trình của bạn nhất thiết phải có để chạy.

Một giao diện người dùng tốt nên có càng ít yêu cầu tuyệt đối càng tốt. Nếu chương trình của bạn cần 17 mẩu thông tin riêng biệt để chạy thành công, thì *cách* bạn lấy thông tin đó từ người dùng thực ra không quan trọng---hầu hết mọi người sẽ bỏ cuộc và rời đi trước khi chạy chương trình thành công. Điều này áp dụng cho dù giao diện người dùng là dòng lệnh, tệp cấu hình hay GUI: nếu bạn đặt ra quá nhiều yêu cầu như vậy với người dùng, hầu hết họ sẽ đơn giản là bỏ cuộc.

Tóm lại, hãy cố giảm thiểu lượng thông tin mà người dùng bắt buộc phải cung cấp---sử dụng các giá trị mặc định hợp lý bất cứ khi nào có thể. Tất nhiên, bạn cũng muốn chương trình của mình đủ linh hoạt. Đó là mục đích của các tùy chọn. Một lần nữa, không quan trọng chúng là các mục trong tệp cấu hình, các widget trong hộp thoại "Preferences" của GUI hay các tùy chọn dòng lệnh---càng triển khai nhiều tùy chọn, chương trình của bạn càng linh hoạt và phần triển khai càng trở nên phức tạp. Dĩ nhiên, tính linh hoạt quá mức cũng có nhược điểm; quá nhiều tùy chọn có thể khiến người dùng choáng ngợp và làm mã của bạn khó bảo trì hơn nhiều.


.. _optparse-tutorial:

Hướng dẫn
---------

Mặc dù :mod:`!optparse` khá linh hoạt và mạnh mẽ, nhưng trong hầu hết các trường hợp, nó cũng rất dễ sử dụng. Phần này trình bày các mẫu mã thường gặp trong mọi chương trình dựa trên :mod:`!optparse`\ .

Trước tiên, bạn cần import class OptionParser; sau đó, ở phần đầu của chương trình chính, hãy tạo một instance OptionParser::

   from optparse import OptionParser
   ...
   parser = OptionParser()

Sau đó, bạn có thể bắt đầu định nghĩa các option. Cú pháp cơ bản là::

   parser.add_option(opt_str, ...,
                     attr=value, ...)

Mỗi option có một hoặc nhiều option string, chẳng hạn như ``-f`` hoặc ``--file``, cùng một số thuộc tính option cho :mod:`!optparse` biết cần mong đợi điều gì và phải làm gì khi gặp option đó trên command line.

Thông thường, mỗi option sẽ có một option string ngắn và một option string dài, ví dụ như::

   parser.add_option("-f", "--file", ...)

Bạn có thể tự do định nghĩa bao nhiêu option string ngắn và option string dài tùy thích (kể cả không có), miễn là tổng thể có ít nhất một option string.

Các chuỗi tùy chọn được truyền cho :meth:`OptionParser.add_option` thực chất là nhãn cho tùy chọn được định nghĩa bởi lời gọi đó. Để ngắn gọn, chúng ta sẽ thường nói đến việc *gặp một tùy chọn* trên dòng lệnh; trên thực tế, :mod:`!optparse` gặp *các chuỗi tùy chọn* rồi tra cứu các tùy chọn từ đó.

Sau khi đã định nghĩa tất cả tùy chọn, hãy yêu cầu :mod:`!optparse` phân tích cú pháp dòng lệnh của chương trình::

   (options, args) = parser.parse_args()

(Nếu muốn, bạn có thể truyền một danh sách đối số tùy chỉnh cho :meth:`~OptionParser.parse_args`, nhưng trường hợp này hiếm khi cần thiết: theo mặc định, nó sử dụng ``sys.argv[1:]``.)

:meth:`~OptionParser.parse_args` trả về hai giá trị:

* ``options``, một đối tượng chứa các giá trị cho tất cả tùy chọn của bạn---ví dụ: nếu ``--file`` nhận một đối số chuỗi duy nhất, thì ``options.file`` sẽ là tên tệp do người dùng cung cấp, hoặc ``None`` nếu người dùng không cung cấp tùy chọn đó

* ``args``, danh sách các đối số vị trí còn lại sau khi phân tích cú pháp các tùy chọn

Phần hướng dẫn này chỉ đề cập đến bốn thuộc tính tùy chọn quan trọng nhất:
:attr:`~Option.action`, :attr:`~Option.type`, :attr:`~Option.dest` (đích đến) và :attr:`~Option.help`. Trong số này, :attr:`~Option.action` là nền tảng nhất.


.. _optparse-understanding-option-actions:

Tìm hiểu về các option action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các action cho :mod:`!optparse` biết phải làm gì khi gặp một option trên dòng lệnh. Có một tập hợp action cố định được hard-code trong :mod:`!optparse`; việc thêm action mới là một chủ đề nâng cao được trình bày trong phần
:ref:`optparse-extending-optparse`. Hầu hết action đều yêu cầu :mod:`!optparse` lưu một giá trị vào một biến nào đó—ví dụ: lấy một chuỗi từ dòng lệnh và lưu chuỗi đó vào một attribute của ``options``.

Nếu bạn không chỉ định option action, :mod:`!optparse` sẽ mặc định sử dụng ``store``.


.. _optparse-store-action:

Action store
^^^^^^^^^^^^

Option action phổ biến nhất là ``store``, yêu cầu :mod:`!optparse` lấy đối số tiếp theo (hoặc phần còn lại của đối số hiện tại), đảm bảo đối số đó có đúng kiểu, rồi lưu vào đích đến bạn chọn.

Ví dụ::

   parser.add_option("-f", "--file",
                     action="store", type="string", dest="filename")

Bây giờ hãy tạo một dòng lệnh giả và yêu cầu :mod:`!optparse` phân tích cú pháp của nó::

   args = ["-f", "foo.txt"]
   (options, args) = parser.parse_args(args)

Khi :mod:`!optparse` gặp chuỗi tùy chọn ``-f``, nó lấy đối số tiếp theo, ``foo.txt``, rồi lưu đối số đó vào ``options.filename``. Vì vậy, sau lệnh gọi :meth:`~OptionParser.parse_args` này, ``options.filename`` là ``"foo.txt"``.

Một số kiểu tùy chọn khác được :mod:`!optparse` hỗ trợ là ``int`` và ``float``. Đây là một tùy chọn yêu cầu đối số là số nguyên::

   parser.add_option("-n", type="int", dest="num")

Lưu ý rằng tùy chọn này không có chuỗi tùy chọn dài, điều đó hoàn toàn hợp lệ. Ngoài ra, không có action tường minh nào, vì mặc định là ``store``.

Hãy phân tích một dòng lệnh giả khác. Lần này, chúng ta sẽ đặt đối số của tùy chọn ngay sát tùy chọn: vì ``-n42`` (một đối số) tương đương với ``-n 42`` (hai đối số), đoạn mã::

   (options, args) = parser.parse_args(["-n42"])
   print(options.num)

sẽ in ``42``.

Nếu bạn không chỉ định type, :mod:`!optparse` sẽ giả định ``string``. Kết hợp với việc action mặc định là ``store``, điều đó có nghĩa là ví dụ đầu tiên của chúng ta có thể ngắn hơn nhiều::

   parser.add_option("-f", "--file", dest="filename")

Nếu bạn không cung cấp destination, :mod:`!optparse` sẽ xác định giá trị mặc định hợp lý từ các chuỗi option: nếu chuỗi option dài đầu tiên là ``--foo-bar``, thì destination mặc định là ``foo_bar``. Nếu không có chuỗi option dài nào, :mod:`!optparse` sẽ xem xét chuỗi option ngắn đầu tiên: destination mặc định cho ``-f`` là ``f``.

:mod:`!optparse` cũng bao gồm type ``complex`` tích hợp sẵn. Việc thêm các type được trình bày trong phần :ref:`optparse-extending-optparse`.


.. _optparse-handling-boolean-options:

Xử lý các tùy chọn boolean (flag)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các tùy chọn flag---đặt một biến thành true hoặc false khi gặp một tùy chọn cụ thể---khá phổ biến. :mod:`!optparse` hỗ trợ chúng bằng hai action riêng biệt, ``store_true`` và ``store_false``. Ví dụ, bạn có thể có một flag ``verbose`` được bật bằng ``-v`` và tắt bằng ``-q``::

   parser.add_option("-v", action="store_true", dest="verbose")
   parser.add_option("-q", action="store_false", dest="verbose")

Ở đây, chúng ta có hai tùy chọn khác nhau với cùng một destination, hoàn toàn không có vấn đề gì. (Điều đó chỉ có nghĩa là bạn phải cẩn thận hơn một chút khi đặt các giá trị mặc định---xem bên dưới.)

Khi :mod:`!optparse` gặp ``-v`` trên dòng lệnh, nó đặt ``options.verbose`` thành ``True``; khi gặp ``-q``, ``options.verbose`` được đặt thành ``False``.


.. _optparse-other-actions:

Các hành động khác
^^^^^^^^^^^^^^^^^^

Một số hành động khác được :mod:`!optparse` hỗ trợ gồm:

``"store_const"``
   lưu trữ một giá trị hằng, được đặt trước qua :attr:`Option.const`

``"append"``
   thêm đối số của tùy chọn này vào một danh sách

``"count"``
   tăng bộ đếm lên một

``"callback"``
   gọi một hàm được chỉ định

Các nội dung này được trình bày trong phần :ref:`optparse-reference-guide` và phần :ref:`optparse-option-callbacks`.


.. _optparse-default-values:

Giá trị mặc định
^^^^^^^^^^^^^^^^

Tất cả các ví dụ trên đều liên quan đến việc đặt một biến ("đích") khi phát hiện một số tùy chọn dòng lệnh nhất định. Điều gì xảy ra nếu các tùy chọn đó không bao giờ xuất hiện? Vì chúng ta không cung cấp giá trị mặc định nào, tất cả đều được đặt thành ``None``. Điều này thường không sao, nhưng đôi khi bạn muốn kiểm soát nhiều hơn. :mod:`!optparse` cho phép bạn cung cấp một giá trị mặc định cho mỗi đích, giá trị này được gán trước khi dòng lệnh được phân tích cú pháp.

Trước tiên, hãy xem xét ví dụ verbose/quiet. Nếu muốn :mod:`!optparse` đặt ``verbose`` thành ``True`` trừ khi ``-q`` xuất hiện, chúng ta có thể làm như sau::

   parser.add_option("-v", action="store_true", dest="verbose", default=True)
   parser.add_option("-q", action="store_false", dest="verbose")

Vì các giá trị mặc định áp dụng cho *đích* chứ không áp dụng cho một tùy chọn cụ thể nào, và hai tùy chọn này tình cờ có cùng đích, nên điều này hoàn toàn tương đương với::

   parser.add_option("-v", action="store_true", dest="verbose")
   parser.add_option("-q", action="store_false", dest="verbose", default=True)

Hãy xem xét ví dụ này::

   parser.add_option("-v", action="store_true", dest="verbose", default=False)
   parser.add_option("-q", action="store_false", dest="verbose", default=True)

Một lần nữa, giá trị mặc định cho ``verbose`` sẽ là ``True``: giá trị mặc định cuối cùng được cung cấp cho một đích cụ thể sẽ được sử dụng.

Một cách rõ ràng hơn để chỉ định các giá trị mặc định là phương thức :meth:`set_defaults` của OptionParser, phương thức này bạn có thể gọi bất kỳ lúc nào trước khi gọi
:meth:`~OptionParser.parse_args`::

   parser.set_defaults(verbose=True)
   parser.add_option(...)
   (options, args) = parser.parse_args()

Như trước đây, giá trị cuối cùng được chỉ định cho một đích tùy chọn nhất định là giá trị được áp dụng. Để rõ ràng, hãy cố gắng chỉ sử dụng một trong hai phương pháp đặt giá trị mặc định, không sử dụng cả hai.


.. _optparse-generating-help:

Tạo phần trợ giúp
^^^^^^^^^^^^^^^^^

Khả năng tự động tạo văn bản trợ giúp và usage của :mod:`!optparse` rất hữu ích khi tạo các giao diện dòng lệnh thân thiện với người dùng. Tất cả những gì bạn cần làm là cung cấp giá trị :attr:`~Option.help` cho mỗi tùy chọn và tùy chọn thêm một thông báo usage ngắn cho toàn bộ chương trình. Dưới đây là một OptionParser được điền các tùy chọn thân thiện với người dùng (có tài liệu mô tả)::

   usage = "usage: %prog [options] arg1 arg2"
   parser = OptionParser(usage=usage)
   parser.add_option("-v", "--verbose",
                     action="store_true", dest="verbose", default=True,
                     help="make lots of noise [default]")
   parser.add_option("-q", "--quiet",
                     action="store_false", dest="verbose",
                     help="be vewwy quiet (I'm hunting wabbits)")
   parser.add_option("-f", "--filename",
                     metavar="FILE", help="write output to FILE")
   parser.add_option("-m", "--mode",
                     default="intermediate",
                     help="interaction mode: novice, intermediate, "
                          "or expert [default: %default]")

Nếu :mod:`!optparse` gặp ``-h`` hoặc ``--help`` trên dòng lệnh, hoặc nếu bạn chỉ cần gọi :meth:`parser.print_help`, nó sẽ in nội dung sau ra đầu ra tiêu chuẩn:

.. code-block:: text

   Usage: <yourscript> [options] arg1 arg2

   Options:
     -h, --help            show this help message and exit
     -v, --verbose         make lots of noise [default]
     -q, --quiet           be vewwy quiet (I'm hunting wabbits)
     -f FILE, --filename=FILE
                           write output to FILE
     -m MODE, --mode=MODE  interaction mode: novice, intermediate, or
                           expert [default: intermediate]

(Nếu đầu ra trợ giúp được kích hoạt bởi một tùy chọn trợ giúp, :mod:`!optparse` sẽ thoát sau khi in văn bản trợ giúp.)

Có nhiều yếu tố ở đây giúp :mod:`!optparse` tạo ra thông báo trợ giúp tốt nhất có thể:

* script tự định nghĩa thông báo usage của mình::

     usage = "usage: %prog [options] arg1 arg2"

  :mod:`!optparse` expands ``%prog`` in the usage string to the name of the
  current program, i.e. ``os.path.basename(sys.argv[0])``.  The expanded string
  is then printed before the detailed option help.

  If you don't supply a usage string, :mod:`!optparse` uses a bland but sensible
  default: ``"Usage: %prog [options]"``, which is fine if your script doesn't
  take any positional arguments.

* mỗi option đều định nghĩa một chuỗi trợ giúp và không cần lo về việc ngắt dòng---\ :mod:`!optparse` sẽ xử lý việc ngắt dòng và giúp phần đầu ra trợ giúp trông đẹp mắt.

* các option nhận một giá trị sẽ thể hiện điều này trong thông báo trợ giúp được tự động tạo, ví dụ như với option "mode"::

     -m MODE, --mode=MODE

  Ở đây, "MODE" được gọi là meta-variable: nó đại diện cho đối số mà người dùng được kỳ vọng sẽ cung cấp cho ``-m``/``--mode``. Theo mặc định,
  :mod:`!optparse` chuyển tên biến đích thành chữ hoa và sử dụng tên đó làm meta-variable. Đôi khi, đó không phải điều bạn muốn---ví dụ, option ``--filename`` đặt ``metavar="FILE"`` một cách rõ ràng, tạo ra phần mô tả option được tự động tạo sau đây::

     -f FILE, --filename=FILE

  Tuy nhiên, điều này quan trọng không chỉ vì giúp tiết kiệm không gian: phần văn bản trợ giúp được viết thủ công sử dụng meta-variable ``FILE`` để gợi ý cho người dùng rằng có mối liên hệ giữa cú pháp bán hình thức ``-f FILE`` và mô tả ngữ nghĩa không hình thức "ghi đầu ra vào FILE". Đây là một cách đơn giản nhưng hiệu quả để làm cho văn bản trợ giúp của bạn rõ ràng và hữu ích hơn nhiều đối với người dùng cuối.

* các option có giá trị mặc định có thể bao gồm ``%default`` trong chuỗi trợ giúp---\ :mod:`!optparse` sẽ thay thế nó bằng :func:`str` của giá trị mặc định của option. Nếu một option không có giá trị mặc định (hoặc giá trị mặc định là ``None``), ``%default`` sẽ được mở rộng thành ``none``.

Nhóm các Option
+++++++++++++++

Khi xử lý nhiều tùy chọn, việc nhóm các tùy chọn này lại sẽ giúp phần trợ giúp hiển thị rõ ràng hơn. Một :class:`OptionParser` có thể chứa nhiều nhóm tùy chọn, mỗi nhóm có thể chứa nhiều tùy chọn.

Có thể tạo một nhóm tùy chọn bằng class :class:`OptionGroup`:

.. class:: OptionGroup(parser, title, description=None)

   trong đó

   * parser là instance :class:`OptionParser` mà nhóm sẽ được chèn vào
   * title là tiêu đề của nhóm
   * description, là tùy chọn, là phần mô tả dài về nhóm

:class:`OptionGroup` kế thừa từ :class:`OptionContainer` (giống như
:class:`OptionParser`) và vì vậy phương thức :meth:`add_option` có thể được sử dụng để thêm một tùy chọn vào nhóm.

Sau khi khai báo tất cả các tùy chọn, sử dụng phương thức :class:`OptionParser`
:meth:`add_option_group` nhóm được thêm vào parser đã được định nghĩa trước đó.

Tiếp tục với parser được định nghĩa trong phần trước, việc thêm một
:class:`OptionGroup` vào parser rất dễ dàng::

    group = OptionGroup(parser, "Dangerous Options",
                        "Caution: use these options at your own risk.  "
                        "It is believed that some of them bite.")
    group.add_option("-g", action="store_true", help="Group option.")
    parser.add_option_group(group)

Kết quả sẽ là đầu ra trợ giúp sau đây:

.. code-block:: text

   Usage: <yourscript> [options] arg1 arg2

   Options:
     -h, --help            show this help message and exit
     -v, --verbose         make lots of noise [default]
     -q, --quiet           be vewwy quiet (I'm hunting wabbits)
     -f FILE, --filename=FILE
                           write output to FILE
     -m MODE, --mode=MODE  interaction mode: novice, intermediate, or
                           expert [default: intermediate]

     Dangerous Options:
       Caution: use these options at your own risk.  It is believed that some
       of them bite.

       -g                  Group option.

Một ví dụ hoàn chỉnh hơn có thể bao gồm việc sử dụng nhiều hơn một nhóm: vẫn mở rộng ví dụ trước::

    group = OptionGroup(parser, "Dangerous Options",
                        "Caution: use these options at your own risk.  "
                        "It is believed that some of them bite.")
    group.add_option("-g", action="store_true", help="Group option.")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Debug Options")
    group.add_option("-d", "--debug", action="store_true",
                     help="Print debug information")
    group.add_option("-s", "--sql", action="store_true",
                     help="Print all SQL statements executed")
    group.add_option("-e", action="store_true", help="Print every action done")
    parser.add_option_group(group)

dẫn đến kết quả đầu ra sau đây:

.. code-block:: text

   Usage: <yourscript> [options] arg1 arg2

   Options:
     -h, --help            show this help message and exit
     -v, --verbose         make lots of noise [default]
     -q, --quiet           be vewwy quiet (I'm hunting wabbits)
     -f FILE, --filename=FILE
                           write output to FILE
     -m MODE, --mode=MODE  interaction mode: novice, intermediate, or expert
                           [default: intermediate]

     Dangerous Options:
       Caution: use these options at your own risk.  It is believed that some
       of them bite.

       -g                  Group option.

     Debug Options:
       -d, --debug         Print debug information
       -s, --sql           Print all SQL statements executed
       -e                  Print every action done

Một phương thức thú vị khác, đặc biệt khi làm việc theo cách lập trình với các nhóm option, là:

.. method:: OptionParser.get_option_group(opt_str)

   Trả về :class:`OptionGroup` mà chuỗi option ngắn hoặc dài *opt_str* (ví dụ: ``'-o'`` hoặc ``'--option'``) thuộc về. Nếu không có :class:`OptionGroup` tương ứng, hãy trả về ``None``.

.. _optparse-printing-version-string:

In chuỗi phiên bản
^^^^^^^^^^^^^^^^^^

Tương tự như chuỗi hướng dẫn sử dụng ngắn gọn, :mod:`!optparse` cũng có thể in chuỗi phiên bản cho chương trình của bạn. Bạn phải cung cấp chuỗi này dưới dạng đối số ``version`` cho OptionParser::

   parser = OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")

``%prog`` được mở rộng giống như trong ``usage``. Ngoài ra, ``version`` có thể chứa bất kỳ nội dung nào bạn muốn. Khi bạn cung cấp nó, :mod:`!optparse` sẽ tự động thêm một option ``--version`` vào parser của bạn. Nếu gặp option này trên dòng lệnh, nó sẽ mở rộng chuỗi ``version`` của bạn (bằng cách thay thế ``%prog``), in chuỗi đó ra stdout rồi thoát.

Ví dụ: nếu script của bạn có tên là ``/usr/bin/foo``:

.. code-block:: shell-session

   $ /usr/bin/foo --version
   foo 1.0

Có thể sử dụng hai phương thức sau để in và lấy chuỗi ``version``:

.. method:: OptionParser.print_version(file=None)

   In thông báo phiên bản của chương trình hiện tại (``self.version``) vào *file* (mặc định là stdout).  Tương tự như :meth:`print_usage`, mọi lần xuất hiện của ``%prog`` trong ``self.version`` sẽ được thay thế bằng tên của chương trình hiện tại.  Không thực hiện gì nếu ``self.version`` rỗng hoặc không được định nghĩa.

.. method:: OptionParser.get_version()

   Giống như :meth:`print_version` nhưng trả về chuỗi phiên bản thay vì in chuỗi đó.


.. _optparse-how-optparse-handles-errors:

Cách :mod:`!optparse` xử lý lỗi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có hai nhóm lỗi chính mà :mod:`!optparse` cần xử lý: lỗi của lập trình viên và lỗi của người dùng.  Lỗi của lập trình viên thường là các lời gọi không hợp lệ đến :func:`OptionParser.add_option`, chẳng hạn như chuỗi tùy chọn không hợp lệ, thuộc tính tùy chọn không xác định, thiếu thuộc tính tùy chọn, v.v.  Những lỗi này được xử lý theo cách thông thường: tăng một ngoại lệ (hoặc :exc:`optparse.OptionError` hoặc
:exc:`TypeError`) và để chương trình bị lỗi.

Việc xử lý lỗi của người dùng quan trọng hơn nhiều, vì chúng chắc chắn sẽ xảy ra bất kể mã của bạn ổn định đến đâu.  :mod:`!optparse` có thể tự động phát hiện một số lỗi của người dùng, chẳng hạn như đối số tùy chọn không hợp lệ (truyền ``-n 4x`` trong khi ``-n`` nhận một đối số số nguyên), thiếu đối số (``-n`` ở cuối dòng lệnh, trong khi ``-n`` nhận đối số thuộc bất kỳ kiểu nào).  Ngoài ra, bạn có thể gọi :func:`OptionParser.error` để báo hiệu một điều kiện lỗi do ứng dụng xác định::

   (options, args) = parser.parse_args()
   ...
   if options.a and options.b:
       parser.error("options -a and -b are mutually exclusive")

Trong cả hai trường hợp, :mod:`!optparse` xử lý lỗi theo cùng một cách: in thông báo cách sử dụng của chương trình và thông báo lỗi ra stderr rồi thoát với trạng thái lỗi 2.

Hãy xem xét ví dụ đầu tiên ở trên, trong đó người dùng truyền ``4x`` cho một tùy chọn yêu cầu số nguyên:

.. code-block:: shell-session

   $ /usr/bin/foo -n 4x
   Usage: foo [options]

   foo: error: option -n: invalid integer value: '4x'

Hoặc trường hợp người dùng hoàn toàn không truyền giá trị nào:

.. code-block:: shell-session

   $ /usr/bin/foo -n
   Usage: foo [options]

   foo: error: -n option requires an argument

Các thông báo lỗi do :mod:`!optparse`\  tạo ra luôn đề cập đến tùy chọn liên quan đến lỗi; hãy đảm bảo bạn cũng làm như vậy khi gọi
:func:`OptionParser.error` từ mã ứng dụng của mình.

Nếu hành vi xử lý lỗi mặc định của :mod:`!optparse` không phù hợp với nhu cầu của bạn, bạn sẽ cần tạo lớp con của OptionParser và ghi đè các phương thức :meth:`~OptionParser.exit` và/hoặc :meth:`~OptionParser.error` của nó.


.. _optparse-putting-it-all-together:

Tổng hợp tất cả
^^^^^^^^^^^^^^^

Dưới đây là dạng thường thấy của các script dựa trên :mod:`!optparse`\ ::

   from optparse import OptionParser
   ...
   def main():
       usage = "usage: %prog [options] arg"
       parser = OptionParser(usage)
       parser.add_option("-f", "--file", dest="filename",
                         help="read data from FILENAME")
       parser.add_option("-v", "--verbose",
                         action="store_true", dest="verbose")
       parser.add_option("-q", "--quiet",
                         action="store_false", dest="verbose")
       ...
       (options, args) = parser.parse_args()
       if len(args) != 1:
           parser.error("incorrect number of arguments")
       if options.verbose:
           print("reading %s..." % options.filename)
       ...

   if __name__ == "__main__":
       main()


.. _optparse-reference-guide:

Hướng dẫn tham khảo
-------------------


.. _optparse-creating-parser:

Tạo parser
^^^^^^^^^^

Bước đầu tiên khi sử dụng :mod:`!optparse` là tạo một instance OptionParser.

.. class:: OptionParser(...)

   Hàm khởi tạo OptionParser không có đối số bắt buộc, nhưng có một số đối số keyword tùy chọn. Bạn luôn nên truyền chúng dưới dạng đối số keyword, tức là không dựa vào thứ tự khai báo các đối số.

   ``usage`` (mặc định: ``"%prog [options]"``)
      Bản tóm tắt cách sử dụng sẽ được in khi chương trình của bạn được chạy không đúng cách hoặc với tùy chọn trợ giúp. Khi :mod:`!optparse` in chuỗi cách sử dụng, nó thay thế ``%prog`` bằng ``os.path.basename(sys.argv[0])`` (hoặc bằng ``prog`` nếu bạn đã truyền đối số keyword đó). Để tắt thông báo cách sử dụng, hãy truyền giá trị đặc biệt :const:`optparse.SUPPRESS_USAGE`.

   ``option_list`` (mặc định: ``[]``)
      Danh sách các đối tượng Option dùng để điền vào parser. Các tùy chọn trong ``option_list`` được thêm sau mọi tùy chọn trong ``standard_option_list`` (một thuộc tính lớp có thể được đặt bởi các lớp con của OptionParser), nhưng trước mọi tùy chọn phiên bản hoặc trợ giúp. Đã lỗi thời; thay vào đó, hãy sử dụng :meth:`add_option` sau khi tạo parser.

   ``option_class`` (mặc định: optparse.Option)
      Lớp được sử dụng khi thêm tùy chọn vào parser trong :meth:`add_option`.

   ``version`` (mặc định: ``None``)
      Chuỗi phiên bản sẽ được in khi người dùng cung cấp một tùy chọn phiên bản. Nếu cung cấp giá trị true cho ``version``, :mod:`!optparse` sẽ tự động thêm một tùy chọn phiên bản với chuỗi tùy chọn duy nhất là ``--version``. Chuỗi con ``%prog`` được mở rộng giống như đối với ``usage``.

   ``conflict_handler`` (mặc định: ``"error"``)
      Chỉ định cần làm gì khi các tùy chọn có chuỗi tùy chọn xung đột được thêm vào parser; xem phần
      :ref:`optparse-conflicts-between-options`.

   ``description`` (mặc định: ``None``)
      Một đoạn văn bản cung cấp thông tin tổng quan ngắn gọn về chương trình của bạn.
      :mod:`!optparse` định dạng lại đoạn văn này để phù hợp với chiều rộng terminal hiện tại và in đoạn văn đó khi người dùng yêu cầu trợ giúp (sau ``usage``, nhưng trước danh sách tùy chọn).

   ``formatter`` (mặc định: một :class:`IndentedHelpFormatter` mới)
      Một thực thể của optparse.HelpFormatter sẽ được dùng để in văn bản trợ giúp.  :mod:`!optparse` cung cấp hai lớp cụ thể cho mục đích này: IndentedHelpFormatter và TitledHelpFormatter.

   ``add_help_option`` (mặc định: ``True``)
      Nếu là true, :mod:`!optparse` sẽ thêm một tùy chọn trợ giúp (với các chuỗi tùy chọn ``-h`` và ``--help``) vào parser.

   ``prog``
      Chuỗi được sử dụng khi mở rộng ``%prog`` trong ``usage`` và ``version`` thay cho ``os.path.basename(sys.argv[0])``.

   ``epilog`` (mặc định: ``None``)
      Một đoạn văn bản trợ giúp sẽ được in sau phần trợ giúp về tùy chọn.

.. _optparse-populating-parser:

Thêm tùy chọn vào parser
^^^^^^^^^^^^^^^^^^^^^^^^

Có một số cách để thêm các tùy chọn vào parser. Cách được ưu tiên là sử dụng :meth:`OptionParser.add_option`, như được trình bày trong phần
:ref:`optparse-tutorial`. :meth:`add_option` có thể được gọi theo một trong hai cách:

* truyền cho nó một instance Option (như được trả về bởi :func:`make_option`)

* truyền cho nó bất kỳ tổ hợp đối số vị trí và đối số từ khóa nào được :func:`make_option` chấp nhận (tức là được hàm khởi tạo Option chấp nhận), và nó sẽ tạo instance Option cho bạn

Cách thay thế khác là truyền một danh sách các instance Option đã được tạo sẵn cho hàm khởi tạo OptionParser, như sau::

   option_list = [
       make_option("-f", "--filename",
                   action="store", type="string", dest="filename"),
       make_option("-q", "--quiet",
                   action="store_false", dest="verbose"),
       ]
   parser = OptionParser(option_list=option_list)

(:func:`make_option` là một hàm factory dùng để tạo các instance Option; hiện tại nó là bí danh của hàm khởi tạo Option. Một phiên bản tương lai của
:mod:`!optparse` có thể tách Option thành nhiều lớp, và :func:`make_option` sẽ chọn đúng lớp để khởi tạo. Không khởi tạo Option trực tiếp.)


.. _optparse-defining-options:

Định nghĩa các tùy chọn
^^^^^^^^^^^^^^^^^^^^^^^

Mỗi instance Option đại diện cho một tập hợp các chuỗi tùy chọn dòng lệnh đồng nghĩa, chẳng hạn như ``-f`` và ``--file``. Bạn có thể chỉ định bao nhiêu chuỗi tùy chọn ngắn hoặc dài tùy ý, nhưng tổng thể phải chỉ định ít nhất một chuỗi tùy chọn.

Cách chuẩn để tạo một instance :class:`Option` là sử dụng
phương thức :meth:`add_option` của :class:`OptionParser`.

.. method:: OptionParser.add_option(option)
            OptionParser.add_option(*opt_str, attr=value, ...)

   Để định nghĩa một option chỉ có chuỗi tùy chọn ngắn::

      parser.add_option("-f", attr=value, ...)

   Và để định nghĩa một option chỉ có chuỗi tùy chọn dài::

      parser.add_option("--foo", attr=value, ...)

   Các đối số từ khóa định nghĩa các thuộc tính của đối tượng Option mới. Thuộc tính option quan trọng nhất là :attr:`~Option.action`, và thuộc tính này phần lớn xác định những thuộc tính nào khác có liên quan hoặc bắt buộc. Nếu bạn truyền các thuộc tính option không liên quan, hoặc không truyền các thuộc tính bắt buộc, :mod:`!optparse` sẽ đưa ra một ngoại lệ :exc:`OptionError` giải thích lỗi của bạn.

   Thuộc tính *action* của một option xác định :mod:`!optparse` thực hiện gì khi gặp option này trên dòng lệnh. Các action option tiêu chuẩn được tích hợp sẵn vào
   :mod:`!optparse` là:

   ``"store"``
      lưu đối số của tùy chọn này (mặc định)

   ``"store_const"``
      lưu một giá trị hằng số, được đặt trước qua :attr:`Option.const`

   ``"store_true"``
      lưu ``True``

   ``"store_false"``
      lưu ``False``

   ``"append"``
      thêm đối số của tùy chọn này vào một danh sách

   ``"append_const"``
      thêm một giá trị hằng số vào danh sách, được đặt trước qua :attr:`Option.const`

   ``"count"``
      tăng một bộ đếm lên một

   ``"callback"``
      gọi một hàm được chỉ định

   ``"help"``
      in thông báo hướng dẫn sử dụng bao gồm tất cả các tùy chọn và tài liệu về chúng

   (Nếu bạn không cung cấp một hành động, mặc định là ``"store"``. Với hành động này, bạn cũng có thể cung cấp các thuộc tính tùy chọn :attr:`~Option.type` và :attr:`~Option.dest`; xem :ref:`optparse-standard-option-actions`.)

Như bạn có thể thấy, hầu hết các hành động đều liên quan đến việc lưu trữ hoặc cập nhật một giá trị ở đâu đó.
:mod:`!optparse` luôn tạo một đối tượng đặc biệt cho mục đích này, theo quy ước được gọi là ``options``, là một thể hiện của :class:`optparse.Values`.

.. class:: Values

   Một đối tượng chứa tên và giá trị của các đối số đã được phân tích cú pháp dưới dạng các thuộc tính. Thông thường được tạo bằng cách gọi khi gọi :meth:`OptionParser.parse_args`, và có thể được ghi đè bằng một lớp con tùy chỉnh được truyền vào đối số *values* của
   :meth:`OptionParser.parse_args` (như được mô tả trong :ref:`optparse-parsing-arguments`).

Các đối số của tùy chọn (và nhiều giá trị khác) được lưu trữ dưới dạng các thuộc tính của đối tượng này, theo thuộc tính tùy chọn :attr:`~Option.dest` (đích đến).

Ví dụ, khi bạn gọi::

   parser.parse_args()

một trong những việc đầu tiên :mod:`!optparse` thực hiện là tạo đối tượng ``options``::

   options = Values()

Nếu một trong các tùy chọn trong parser này được định nghĩa bằng::

   parser.add_option("-f", "--file", action="store", type="string", dest="filename")

và dòng lệnh đang được phân tích cú pháp bao gồm bất kỳ dòng nào sau đây::

   -ffoo
   -f foo
   --file=foo
   --file foo

thì :mod:`!optparse`, khi gặp tùy chọn này, sẽ thực hiện thao tác tương đương với::

   options.filename = "foo"

Các thuộc tính tùy chọn :attr:`~Option.type` và :attr:`~Option.dest` gần như quan trọng không kém :attr:`~Option.action`, nhưng :attr:`~Option.action` là thuộc tính duy nhất có ý nghĩa đối với các tùy chọn *all*.


.. _optparse-option-attributes:

Các thuộc tính tùy chọn
^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Option

   Một đối số dòng lệnh duy nhất, với nhiều thuộc tính khác nhau được truyền dưới dạng keyword cho constructor. Thông thường được tạo bằng :meth:`OptionParser.add_option` thay vì tạo trực tiếp, và có thể được ghi đè bằng một class tùy chỉnh thông qua đối số *option_class* của :class:`OptionParser`.

Có thể truyền các thuộc tính tùy chọn sau dưới dạng keyword arguments cho
:meth:`OptionParser.add_option`. Nếu bạn truyền một thuộc tính tùy chọn không liên quan đến một tùy chọn cụ thể hoặc không truyền một thuộc tính tùy chọn bắt buộc,
:mod:`!optparse` sẽ raise :exc:`OptionError`.

.. attribute:: Option.action

   (mặc định: ``"store"``)

   Xác định hành vi của :mod:`!optparse` khi tùy chọn này xuất hiện trên dòng lệnh; các tùy chọn có sẵn được ghi lại :ref:`tại đây <optparse-standard-option-actions>`.

.. attribute:: Option.type

   (mặc định: ``"string"``)

   Kiểu đối số mà tùy chọn này yêu cầu (ví dụ: ``"string"`` hoặc ``"int"``); các kiểu tùy chọn có sẵn được ghi lại :ref:`tại đây <optparse-standard-option-types>`.

.. attribute:: Option.dest

   (mặc định: được suy ra từ các chuỗi tùy chọn)

   Nếu hành động của tùy chọn ngụ ý việc ghi hoặc sửa đổi một giá trị ở đâu đó, tùy chọn này cho :mod:`!optparse` biết nơi ghi giá trị đó: :attr:`~Option.dest` chỉ định một thuộc tính của đối tượng ``options`` mà :mod:`!optparse` tạo ra trong quá trình phân tích dòng lệnh.

.. attribute:: Option.default

   Giá trị dùng cho đích của tùy chọn này nếu tùy chọn không xuất hiện trên dòng lệnh. Xem thêm :meth:`OptionParser.set_defaults`.

.. attribute:: Option.nargs

   (mặc định: 1)

   Cần sử dụng bao nhiêu đối số có kiểu :attr:`~Option.type` khi gặp tùy chọn này. Nếu > 1, :mod:`!optparse` sẽ lưu một tuple các giá trị vào
   :attr:`~Option.dest`.

.. attribute:: Option.const

   Đối với các action lưu trữ một giá trị hằng, giá trị hằng cần lưu trữ.

.. attribute:: Option.choices

   Đối với các tùy chọn có kiểu ``"choice"``, danh sách các chuỗi mà người dùng có thể chọn.

.. attribute:: Option.callback

   Đối với các tùy chọn có action ``"callback"``, callable cần gọi khi gặp tùy chọn này. Xem phần :ref:`optparse-option-callbacks` để biết chi tiết về các đối số được truyền cho callable.

.. attribute:: Option.callback_args
               Option.callback_kwargs

   Các đối số vị trí và đối số từ khóa bổ sung cần truyền cho ``callback`` sau bốn đối số callback tiêu chuẩn.

.. attribute:: Option.help

   Văn bản trợ giúp cần in cho tùy chọn này khi liệt kê tất cả các tùy chọn có sẵn sau khi người dùng cung cấp tùy chọn :attr:`~Option.help` (chẳng hạn như ``--help``). Nếu không cung cấp văn bản trợ giúp, tùy chọn sẽ được liệt kê mà không có văn bản trợ giúp. Để ẩn tùy chọn này, hãy sử dụng giá trị đặc biệt :const:`optparse.SUPPRESS_HELP`.

.. attribute:: Option.metavar

   (mặc định: được suy ra từ các chuỗi tùy chọn)

   Giá trị thay thế cho (các) đối số option được sử dụng khi in văn bản trợ giúp. Xem phần :ref:`optparse-tutorial` để biết ví dụ.


.. _optparse-standard-option-actions:

Các action option tiêu chuẩn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các action option khác nhau có những yêu cầu và hiệu ứng hơi khác nhau. Hầu hết action đều có một số thuộc tính option liên quan mà bạn có thể chỉ định để định hướng hành vi của :mod:`!optparse`; một số ít có các thuộc tính bắt buộc, và bạn phải chỉ định chúng cho mọi option sử dụng action đó.

* ``"store"`` [liên quan: :attr:`~Option.type`, :attr:`~Option.dest`,
  :attr:`~Option.nargs`, :attr:`~Option.choices`]

  Option phải được theo sau bởi một đối số, đối số này được chuyển đổi thành một giá trị theo :attr:`~Option.type` và được lưu trong :attr:`~Option.dest`. Nếu
  :attr:`~Option.nargs` > 1, nhiều đối số sẽ được lấy từ dòng lệnh; tất cả sẽ được chuyển đổi theo :attr:`~Option.type` và được lưu vào :attr:`~Option.dest` dưới dạng một tuple. Xem
  phần :ref:`optparse-standard-option-types`.

  Nếu :attr:`~Option.choices` được cung cấp (một list hoặc tuple các chuỗi), kiểu sẽ mặc định là ``"choice"``.

  Nếu :attr:`~Option.type` không được cung cấp, giá trị mặc định là ``"string"``.

  Nếu :attr:`~Option.dest` không được cung cấp, :mod:`!optparse` sẽ suy ra đích từ chuỗi tùy chọn dài đầu tiên (ví dụ: ``--foo-bar`` ngụ ý ``foo_bar``). Nếu không có chuỗi tùy chọn dài nào, :mod:`!optparse` sẽ suy ra đích từ chuỗi tùy chọn ngắn đầu tiên (ví dụ: ``-f`` ngụ ý ``f``).

  Ví dụ::

     parser.add_option("-f")
     parser.add_option("-p", type="float", nargs=3, dest="point")

  Khi phân tích dòng lệnh::

     -f foo.txt -p 1 -3.5 4 -fbar.txt

  :mod:`!optparse` sẽ thiết lập::

     options.f = "foo.txt"
     options.point = (1.0, -3.5, 4.0)
     options.f = "bar.txt"

* ``"store_const"`` [bắt buộc: :attr:`~Option.const`; liên quan:
  :attr:`~Option.dest`]

  Giá trị :attr:`~Option.const` được lưu trong :attr:`~Option.dest`.

  Ví dụ::

     parser.add_option("-q", "--quiet",
                       action="store_const", const=0, dest="verbose")
     parser.add_option("-v", "--verbose",
                       action="store_const", const=1, dest="verbose")
     parser.add_option("--noisy",
                       action="store_const", const=2, dest="verbose")

  Nếu thấy ``--noisy``, :mod:`!optparse` sẽ đặt::

     options.verbose = 2

* ``"store_true"`` [liên quan: :attr:`~Option.dest`]

  Trường hợp đặc biệt của ``"store_const"`` lưu ``True`` vào
  :attr:`~Option.dest`.

* ``"store_false"`` [liên quan: :attr:`~Option.dest`]

  Giống ``"store_true"``, nhưng lưu trữ ``False``.

  Ví dụ::

     parser.add_option("--clobber", action="store_true", dest="clobber")
     parser.add_option("--no-clobber", action="store_false", dest="clobber")

* ``"append"`` [liên quan: :attr:`~Option.type`, :attr:`~Option.dest`,
  :attr:`~Option.nargs`, :attr:`~Option.choices`]

  Tùy chọn phải được theo sau bởi một đối số, đối số này được thêm vào danh sách trong
  :attr:`~Option.dest`.  Nếu không cung cấp giá trị mặc định cho :attr:`~Option.dest`, một danh sách rỗng sẽ tự động được tạo khi :mod:`!optparse` lần đầu gặp tùy chọn này trên dòng lệnh.  Nếu :attr:`~Option.nargs` > 1, nhiều đối số sẽ được xử lý và một tuple có độ dài :attr:`~Option.nargs` sẽ được thêm vào :attr:`~Option.dest`.

  Giá trị mặc định của :attr:`~Option.type` và :attr:`~Option.dest` giống với giá trị mặc định của action ``"store"``.

  Ví dụ::

     parser.add_option("-t", "--tracks", action="append", type="int")

  Nếu ``-t3`` xuất hiện trên dòng lệnh, :mod:`!optparse` thực hiện tương đương với::

     options.tracks = []
     options.tracks.append(int("3"))

  Nếu sau đó một chút ``--tracks=4`` xuất hiện, nó sẽ thực hiện::

     options.tracks.append(int("4"))

  Action ``append`` gọi phương thức ``append`` trên giá trị hiện tại của option. Điều này có nghĩa là mọi giá trị mặc định được chỉ định đều phải có phương thức ``append``. Điều đó cũng có nghĩa là nếu giá trị mặc định không rỗng, các phần tử mặc định sẽ xuất hiện trong giá trị đã phân tích của option, với mọi giá trị từ dòng lệnh được nối thêm sau các giá trị mặc định đó::

     >>> parser.add_option("--files", action="append", default=['~/.mypkg/defaults'])
     >>> opts, args = parser.parse_args(['--files', 'overrides.mypkg'])
     >>> opts.files
     ['~/.mypkg/defaults', 'overrides.mypkg']

* ``"append_const"`` [bắt buộc: :attr:`~Option.const`; liên quan:
  :attr:`~Option.dest`]

  Tương tự ``"store_const"``, nhưng giá trị :attr:`~Option.const` được nối thêm vào
  :attr:`~Option.dest`; như với ``"append"``, :attr:`~Option.dest` mặc định là ``None``, và một danh sách rỗng sẽ được tự động tạo vào lần đầu tiên option được gặp.

* ``"count"`` [liên quan: :attr:`~Option.dest`]

  Tăng số nguyên được lưu trong :attr:`~Option.dest`. Nếu không cung cấp giá trị mặc định, :attr:`~Option.dest` được đặt thành 0 trước khi được tăng lần đầu.

  Ví dụ::

     parser.add_option("-v", action="count", dest="verbosity")

  Lần đầu tiên ``-v`` xuất hiện trên dòng lệnh, :mod:`!optparse` thực hiện tương đương với::

     options.verbosity = 0
     options.verbosity += 1

  Mỗi lần xuất hiện tiếp theo của ``-v`` sẽ dẫn đến::

     options.verbosity += 1

* ``"callback"`` [bắt buộc: :attr:`~Option.callback`; liên quan:
  :attr:`~Option.type`, :attr:`~Option.nargs`, :attr:`~Option.callback_args`,
  :attr:`~Option.callback_kwargs`]

  Gọi hàm được chỉ định bởi :attr:`~Option.callback`, hàm này được gọi như sau::

     func(option, opt_str, value, parser, *args, **kwargs)

  Xem phần :ref:`optparse-option-callbacks` để biết thêm chi tiết.

* ``"help"``

  In một thông báo trợ giúp hoàn chỉnh cho tất cả các tùy chọn trong option parser hiện tại. Thông báo trợ giúp được tạo từ chuỗi ``usage`` được truyền vào hàm khởi tạo của OptionParser và chuỗi :attr:`~Option.help` được truyền vào mọi tùy chọn.

  Nếu không cung cấp chuỗi :attr:`~Option.help` cho một tùy chọn, tùy chọn đó vẫn sẽ được liệt kê trong thông báo trợ giúp. Để loại bỏ hoàn toàn một tùy chọn, hãy sử dụng giá trị đặc biệt
  :const:`optparse.SUPPRESS_HELP`.

  :mod:`!optparse` tự động thêm tùy chọn :attr:`~Option.help` vào tất cả OptionParser, vì vậy thông thường bạn không cần tạo một tùy chọn như vậy.

  Ví dụ::

     from optparse import OptionParser, SUPPRESS_HELP

     # thông thường, một tùy chọn trợ giúp được tự động thêm vào, nhưng có thể
     # tắt tùy chọn này bằng cách sử dụng đối số add_help_option
     parser = OptionParser(add_help_option=False)

     parser.add_option("-h", "--help", action="help")
     parser.add_option("-v", action="store_true", dest="verbose",
                       help="Be moderately verbose")
     parser.add_option("--file", dest="filename",
                       help="Input file to read data from")
     parser.add_option("--secret", help=SUPPRESS_HELP)

  Nếu :mod:`!optparse` phát hiện ``-h`` hoặc ``--help`` trên dòng lệnh, nó sẽ in một thông báo trợ giúp tương tự như sau ra stdout (giả sử ``sys.argv[0]`` là ``"foo.py"``):

  .. code-block:: text

     Usage: foo.py [options]

     Options:
       -h, --help        Show this help message and exit
       -v                Be moderately verbose
       --file=FILENAME   Input file to read data from

  Sau khi in thông báo trợ giúp, :mod:`!optparse` kết thúc tiến trình của bạn với ``sys.exit(0)``.

* ``"version"``

  In số phiên bản được cung cấp cho OptionParser ra stdout rồi thoát. Số phiên bản thực sự được định dạng và in bởi phương thức ``print_version()`` của OptionParser.  Thường chỉ liên quan nếu đối số ``version`` được cung cấp cho hàm khởi tạo OptionParser.  Cũng như
  các tùy chọn :attr:`~Option.help`, bạn sẽ hiếm khi tạo các tùy chọn ``version``, vì :mod:`!optparse` tự động thêm chúng khi cần.


.. _optparse-standard-option-types:

Các kiểu tùy chọn tiêu chuẩn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`!optparse` có năm kiểu tùy chọn tích hợp sẵn: ``"string"``, ``"int"``, ``"choice"``, ``"float"`` và ``"complex"``.  Nếu cần thêm các kiểu tùy chọn mới, hãy xem phần :ref:`optparse-extending-optparse`.

Các đối số của tùy chọn chuỗi không được kiểm tra hoặc chuyển đổi theo bất kỳ cách nào: văn bản trên dòng lệnh được lưu nguyên trạng vào đích (hoặc được truyền cho callback).

Các đối số số nguyên (kiểu ``"int"``) được phân tích như sau:

* nếu số bắt đầu bằng ``0x``, nó được phân tích thành số thập lục phân

* nếu số bắt đầu bằng ``0``, nó được phân tích thành số bát phân

* nếu số bắt đầu bằng ``0b``, nó được phân tích thành số nhị phân

* nếu không, số được phân tích thành số thập phân


Việc chuyển đổi được thực hiện bằng cách gọi :func:`int` với cơ số tương ứng (2, 8, 10 hoặc 16). Nếu thao tác này thất bại thì :mod:`!optparse` cũng sẽ thất bại, mặc dù với thông báo lỗi hữu ích hơn.

Các đối số tùy chọn ``"float"`` và ``"complex"`` được chuyển đổi trực tiếp bằng
:func:`float` và :func:`complex`, với cách xử lý lỗi tương tự.

``"choice"`` tùy chọn là một kiểu con của ``"string"`` tùy chọn.  The
Thuộc tính option :attr:`~Option.choices` (một dãy chuỗi) xác định tập hợp các đối số tùy chọn được phép.  :func:`optparse.check_choice` so sánh các đối số tùy chọn do người dùng cung cấp với danh sách chuẩn này và phát sinh
:exc:`OptionValueError` nếu một chuỗi không hợp lệ được cung cấp.


.. _optparse-parsing-arguments:

Phân tích cú pháp đối số
^^^^^^^^^^^^^^^^^^^^^^^^

Mục đích chính của việc tạo và điền dữ liệu cho một OptionParser là gọi
phương thức :meth:`~OptionParser.parse_args` của nó.

.. method:: OptionParser.parse_args(args=None, values=None)

   Phân tích các tùy chọn dòng lệnh được tìm thấy trong *args*.

   Các tham số đầu vào là

   ``args``
      danh sách các đối số cần xử lý (mặc định: ``sys.argv[1:]``)

   ``values``
      một đối tượng :class:`Values` để lưu trữ các đối số tùy chọn (mặc định: một instance mới của :class:`Values`) -- nếu bạn cung cấp một đối tượng hiện có, các giá trị mặc định của tùy chọn sẽ không được khởi tạo trên đối tượng đó

   và giá trị trả về là một cặp ``(options, args)`` trong đó

   ``options``
      chính đối tượng đã được truyền vào dưới dạng *values*, hoặc instance ``optparse.Values`` được tạo bởi :mod:`!optparse`

   ``args``
      các đối số vị trí còn lại sau khi tất cả tùy chọn đã được xử lý

Cách sử dụng phổ biến nhất là không cung cấp đối số từ khóa nào. Nếu bạn cung cấp ``values``, đối tượng đó sẽ được sửa đổi bằng các lần gọi :func:`setattr` lặp lại (gần như một lần cho mỗi đối số tùy chọn được lưu vào một đích tùy chọn) và được trả về bởi
:meth:`~OptionParser.parse_args`.

Nếu :meth:`~OptionParser.parse_args` gặp bất kỳ lỗi nào trong danh sách đối số, nó sẽ gọi phương thức :meth:`error` của OptionParser cùng với thông báo lỗi phù hợp cho người dùng cuối. Cuối cùng, thao tác này sẽ kết thúc tiến trình của bạn với trạng thái thoát là 2 (trạng thái thoát Unix truyền thống cho các lỗi dòng lệnh).


.. _optparse-querying-manipulating-option-parser:

Truy vấn và thao tác với option parser của bạn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bạn có thể tùy chỉnh đôi chút hành vi mặc định của option parser, đồng thời kiểm tra option parser để xem nó chứa những gì. OptionParser cung cấp một số phương thức giúp bạn thực hiện việc này:

.. method:: OptionParser.disable_interspersed_args()

   Đặt chế độ phân tích cú pháp dừng ở tùy chọn không phải option đầu tiên. Ví dụ, nếu ``-a`` và ``-b`` đều là các tùy chọn đơn giản không nhận đối số, :mod:`!optparse` thường chấp nhận cú pháp này::

      prog -a arg1 -b arg2

   và xử lý nó tương đương với::

      prog -a -b arg1 arg2

   Để tắt tính năng này, hãy gọi :meth:`disable_interspersed_args`. Thao tác này khôi phục cú pháp Unix truyền thống, trong đó việc phân tích cú pháp tùy chọn sẽ dừng ở đối số đầu tiên không phải option.

   Hãy sử dụng cách này nếu bạn có một command processor chạy một command khác có các tùy chọn riêng và muốn đảm bảo những tùy chọn này không bị nhầm lẫn. Ví dụ: mỗi command có thể có một tập tùy chọn khác nhau.

.. method:: OptionParser.enable_interspersed_args()

   Đặt chế độ phân tích cú pháp để không dừng ở đối số đầu tiên không phải option, cho phép xen kẽ các switch với các đối số lệnh. Đây là hành vi mặc định.

.. method:: OptionParser.get_option(opt_str)

   Trả về thực thể Option có option string *opt_str*, hoặc ``None`` nếu không có option nào có option string đó.

.. method:: OptionParser.has_option(opt_str)

   Trả về ``True`` nếu OptionParser có option với option string *opt_str* (ví dụ: ``-q`` hoặc ``--verbose``).

.. method:: OptionParser.remove_option(opt_str)

   Nếu :class:`OptionParser` có option tương ứng với *opt_str*, option đó sẽ bị xóa. Nếu option đó cung cấp bất kỳ option string nào khác, tất cả các option string đó sẽ trở nên không hợp lệ. Nếu *opt_str* không xuất hiện trong bất kỳ option nào thuộc :class:`OptionParser`, sẽ phát sinh :exc:`ValueError`.


.. _optparse-conflicts-between-options:

Xung đột giữa các option
^^^^^^^^^^^^^^^^^^^^^^^^

Nếu không cẩn thận, bạn rất dễ định nghĩa các option có option string xung đột với nhau::

   parser.add_option("-n", "--dry-run", ...)
   ...
   parser.add_option("-n", "--noisy", ...)

(Điều này đặc biệt đúng nếu bạn đã định nghĩa lớp con OptionParser của riêng mình cùng một số option tiêu chuẩn.)

Mỗi khi bạn thêm một option, :mod:`!optparse` sẽ kiểm tra xung đột với các option hiện có. Nếu phát hiện xung đột, nó sẽ gọi cơ chế xử lý xung đột hiện tại. Bạn có thể thiết lập cơ chế xử lý xung đột trong constructor::

   parser = OptionParser(..., conflict_handler=handler)

hoặc bằng một lệnh gọi riêng::

   parser.set_conflict_handler(handler)

Các trình xử lý xung đột hiện có là:

   ``"error"`` (mặc định)
      giả định xung đột giữa các option là lỗi lập trình và raise
      :exc:`OptionConflictError`

   ``"resolve"``
      giải quyết xung đột giữa các option một cách thông minh (xem bên dưới)


Ví dụ, hãy định nghĩa một :class:`OptionParser` có khả năng giải quyết xung đột một cách thông minh và thêm các option xung đột vào đó::

   parser = OptionParser(conflict_handler="resolve")
   parser.add_option("-n", "--dry-run", ..., help="do no harm")
   parser.add_option("-n", "--noisy", ..., help="be noisy")

Tại thời điểm này, :mod:`!optparse` phát hiện rằng một tùy chọn đã được thêm trước đó đang sử dụng chuỗi tùy chọn ``-n``. Vì ``conflict_handler`` là ``"resolve"``, nó xử lý tình huống này bằng cách xóa ``-n`` khỏi danh sách chuỗi tùy chọn của tùy chọn trước đó. Giờ đây, ``--dry-run`` là cách duy nhất để người dùng kích hoạt tùy chọn đó. Nếu người dùng yêu cầu trợ giúp, thông báo trợ giúp sẽ phản ánh điều đó::

   Options:
     --dry-run     do no harm
     ...
     -n, --noisy   be noisy

Có thể loại bỏ dần các chuỗi tùy chọn của một tùy chọn đã được thêm trước đó cho đến khi không còn chuỗi nào, khiến người dùng không có cách nào gọi tùy chọn đó từ command-line. Trong trường hợp này, :mod:`!optparse` xóa hoàn toàn tùy chọn đó, vì vậy nó không xuất hiện trong help text hay bất kỳ nơi nào khác. Tiếp tục với OptionParser hiện có của chúng ta::

   parser.add_option("--dry-run", ..., help="new dry-run option")

Tại thời điểm này, tùy chọn ``-n``/``--dry-run`` ban đầu không còn có thể truy cập được, vì vậy :mod:`!optparse` xóa nó, để lại help text này::

   Options:
     ...
     -n, --noisy   be noisy
     --dry-run     new dry-run option


.. _optparse-cleanup:

Dọn dẹp
^^^^^^^

Các instance của OptionParser có một số tham chiếu vòng. Điều này không gây vấn đề cho bộ thu gom rác của Python, nhưng bạn có thể muốn ngắt các tham chiếu vòng một cách rõ ràng bằng cách gọi :meth:`~OptionParser.destroy` trên OptionParser sau khi sử dụng xong. Điều này đặc biệt hữu ích trong các ứng dụng chạy lâu dài, nơi các đồ thị đối tượng lớn có thể được truy cập từ OptionParser.


.. _optparse-other-methods:

Các phương thức khác
^^^^^^^^^^^^^^^^^^^^

OptionParser hỗ trợ một số phương thức public khác:

.. method:: OptionParser.set_usage(usage)

   Đặt chuỗi usage theo các quy tắc được mô tả ở trên cho đối số từ khóa constructor ``usage``. Truyền ``None`` sẽ đặt chuỗi usage mặc định; sử dụng :const:`optparse.SUPPRESS_USAGE` để bỏ qua thông báo usage.

.. method:: OptionParser.print_usage(file=None)

   In thông báo usage của chương trình hiện tại (``self.usage``) vào *file* (mặc định là stdout). Mọi lần xuất hiện của chuỗi ``%prog`` trong ``self.usage`` sẽ được thay thế bằng tên của chương trình hiện tại. Không làm gì nếu ``self.usage`` rỗng hoặc chưa được định nghĩa.

.. method:: OptionParser.get_usage()

   Tương tự :meth:`print_usage`, nhưng trả về chuỗi usage thay vì in chuỗi đó.

.. method:: OptionParser.set_defaults(dest=value, ...)

   Đặt các giá trị mặc định cho nhiều đích của option cùng lúc. Sử dụng
   :meth:`set_defaults` là cách ưu tiên để đặt giá trị mặc định cho các option, vì nhiều option có thể dùng chung một đích. Ví dụ: nếu một số option "mode" cùng đặt một đích, bất kỳ option nào trong số đó cũng có thể đặt giá trị mặc định, và giá trị được đặt sau cùng sẽ thắng::

      parser.add_option("--advanced", action="store_const",
                        dest="mode", const="advanced",
                        default="novice")    # bị ghi đè bên dưới
      parser.add_option("--novice", action="store_const",
                        dest="mode", const="novice",
                        default="advanced")  # ghi đè thiết lập bên trên

   Để tránh nhầm lẫn này, hãy sử dụng :meth:`set_defaults`::

      parser.set_defaults(mode="advanced")
      parser.add_option("--advanced", action="store_const",
                        dest="mode", const="advanced")
      parser.add_option("--novice", action="store_const",
                        dest="mode", const="novice")


.. _optparse-option-callbacks:

Callback tùy chọn
-----------------

Khi các action và type tích hợp sẵn của :mod:`!optparse` chưa hoàn toàn đáp ứng nhu cầu của bạn, bạn có hai lựa chọn: mở rộng :mod:`!optparse` hoặc định nghĩa một tùy chọn callback. Việc mở rộng :mod:`!optparse` mang tính tổng quát hơn, nhưng là quá mức cần thiết đối với nhiều trường hợp đơn giản. Khá thường xuyên, một callback đơn giản là tất cả những gì bạn cần.

Có hai bước để định nghĩa một tùy chọn callback:

* định nghĩa chính tùy chọn bằng action ``"callback"``

* viết callback; đây là một hàm (hoặc phương thức) nhận ít nhất bốn đối số, như mô tả bên dưới


.. _optparse-defining-callback-option:

Định nghĩa một tùy chọn callback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Như mọi khi, cách dễ nhất để định nghĩa một tùy chọn callback là sử dụng
phương thức :meth:`OptionParser.add_option`. Ngoài :attr:`~Option.action`, thuộc tính tùy chọn duy nhất bạn phải chỉ định là ``callback``, hàm cần gọi::

   parser.add_option("-c", action="callback", callback=my_callback)

``callback`` là một hàm (hoặc đối tượng có thể gọi khác), vì vậy bạn phải định nghĩa ``my_callback()`` trước khi tạo tùy chọn callback này. Trong trường hợp đơn giản này, :mod:`!optparse` thậm chí không biết ``-c`` có nhận đối số nào hay không, điều này thường có nghĩa là tùy chọn không nhận đối số nào---chỉ cần ``-c`` xuất hiện trên command line là đủ. Tuy nhiên, trong một số trường hợp, bạn có thể muốn callback của mình nhận một số lượng đối số command line tùy ý. Đây là lúc việc viết callback trở nên phức tạp; nội dung này được đề cập ở phần sau của mục này.

:mod:`!optparse` luôn truyền bốn đối số cụ thể cho callback của bạn và chỉ truyền thêm đối số nếu bạn chỉ định chúng thông qua
:attr:`~Option.callback_args` và :attr:`~Option.callback_kwargs`. Vì vậy, chữ ký hàm callback tối thiểu là::

   def my_callback(option, opt, value, parser):

Bốn đối số của một callback được mô tả bên dưới.

Có một số thuộc tính tùy chọn khác mà bạn có thể cung cấp khi định nghĩa một tùy chọn callback:

:attr:`~Option.type`
   có ý nghĩa thông thường: giống như các action ``"store"`` hoặc ``"append"``, nó yêu cầu :mod:`!optparse` nhận một đối số và chuyển đổi đối số đó thành
   :attr:`~Option.type`. Tuy nhiên, thay vì lưu giá trị đã chuyển đổi ở đâu đó, :mod:`!optparse` truyền giá trị đó cho callback function của bạn.

:attr:`~Option.nargs`
   cũng có ý nghĩa thông thường: nếu được cung cấp và > 1, :mod:`!optparse` sẽ nhận :attr:`~Option.nargs` đối số, mỗi đối số phải có thể được chuyển đổi thành
   :attr:`~Option.type`. Sau đó, nó truyền một tuple gồm các giá trị đã chuyển đổi cho callback của bạn.

:attr:`~Option.callback_args`
   một tuple gồm các đối số vị trí bổ sung để truyền cho callback

:attr:`~Option.callback_kwargs`
   một dictionary gồm các đối số từ khóa bổ sung để truyền cho callback


.. _optparse-how-callbacks-called:

Cách gọi callback
^^^^^^^^^^^^^^^^^

Tất cả callback đều được gọi như sau::

   func(option, opt_str, value, parser, *args, **kwargs)

trong đó

``option``
   là instance Option đang gọi callback

``opt_str``
   là chuỗi tùy chọn xuất hiện trên command line và kích hoạt callback. (Nếu sử dụng một long option viết tắt, ``opt_str`` sẽ là chuỗi tùy chọn đầy đủ, chuẩn tắc---ví dụ: nếu người dùng nhập ``--foo`` trên command line làm dạng viết tắt của ``--foobar``, thì ``opt_str`` sẽ là ``"--foobar"``.)

``value``
   là đối số của tùy chọn này xuất hiện trên command line. :mod:`!optparse` sẽ chỉ mong đợi một đối số nếu :attr:`~Option.type` được thiết lập; kiểu của ``value`` sẽ là kiểu được ngụ ý bởi kiểu của tùy chọn. Nếu :attr:`~Option.type` của tùy chọn này là ``None`` (không mong đợi đối số), thì ``value`` sẽ là ``None``. Nếu :attr:`~Option.nargs` > 1, ``value`` sẽ là một tuple gồm các giá trị có kiểu thích hợp.

``parser``
   là instance OptionParser điều khiển toàn bộ quá trình, chủ yếu hữu ích vì bạn có thể truy cập một số dữ liệu thú vị khác thông qua các thuộc tính instance của nó:

   ``parser.largs``
      danh sách hiện tại gồm các đối số còn lại, tức là những đối số đã được dùng nhưng không phải là tùy chọn cũng không phải là đối số của tùy chọn. Bạn có thể tự do sửa đổi ``parser.largs``, chẳng hạn bằng cách thêm các đối số khác vào đó. (Danh sách này sẽ trở thành ``args``, giá trị trả về thứ hai của :meth:`~OptionParser.parse_args`.)

   ``parser.rargs``
      danh sách hiện tại gồm các đối số còn lại, tức là sau khi ``opt_str`` và ``value`` (nếu áp dụng) đã được loại bỏ, và chỉ còn các đối số đứng sau chúng. Bạn có thể tự do sửa đổi ``parser.rargs``, chẳng hạn bằng cách sử dụng thêm các đối số.

   ``parser.values``
      đối tượng mà theo mặc định các giá trị tùy chọn được lưu vào (một instance của optparse.OptionValues). Điều này cho phép callback sử dụng cùng cơ chế như phần còn lại của :mod:`!optparse` để lưu các giá trị tùy chọn; bạn không cần phải dùng biến toàn cục hoặc closure. Bạn cũng có thể truy cập hoặc sửa đổi giá trị của bất kỳ tùy chọn nào đã xuất hiện trên command line.

``args``
   là một tuple gồm các đối số vị trí tùy ý được cung cấp thông qua tùy chọn
   :attr:`~Option.callback_args`.

``kwargs``
   là một dictionary gồm các đối số từ khóa tùy ý được cung cấp thông qua
   :attr:`~Option.callback_kwargs`.


.. _optparse-raising-errors-in-callback:

Phát sinh lỗi trong callback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hàm callback nên phát sinh :exc:`OptionValueError` nếu có bất kỳ vấn đề nào với tùy chọn hoặc (các) đối số của tùy chọn đó. :mod:`!optparse` bắt lỗi này và kết thúc chương trình, đồng thời in thông báo lỗi bạn cung cấp ra stderr. Thông báo của bạn nên rõ ràng, ngắn gọn, chính xác và nêu tùy chọn gây lỗi. Nếu không, người dùng sẽ khó xác định họ đã làm sai điều gì.


.. _optparse-callback-example-1:

Ví dụ callback 1: callback đơn giản
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sau đây là một ví dụ về tùy chọn callback không nhận đối số nào và chỉ ghi lại rằng tùy chọn đó đã được nhìn thấy::

   def record_foo_seen(option, opt_str, value, parser):
       parser.values.saw_foo = True

   parser.add_option("--foo", action="callback", callback=record_foo_seen)

Tất nhiên, bạn có thể thực hiện việc đó bằng action ``"store_true"``.


.. _optparse-callback-example-2:

Ví dụ callback 2: kiểm tra thứ tự tùy chọn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sau đây là một ví dụ thú vị hơn một chút: ghi lại việc ``-a`` được nhìn thấy, nhưng báo lỗi nếu nó xuất hiện sau ``-b`` trên dòng lệnh.::

   def check_order(option, opt_str, value, parser):
       if parser.values.b:
           raise OptionValueError("can't use -a after -b")
       parser.values.a = 1
   ...
   parser.add_option("-a", action="callback", callback=check_order)
   parser.add_option("-b", action="store_true", dest="b")


.. _optparse-callback-example-3:

Ví dụ callback 3: kiểm tra thứ tự tùy chọn (tổng quát hóa)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu muốn sử dụng lại callback này cho một số tùy chọn tương tự (đặt một cờ, nhưng báo lỗi nếu ``-b`` đã được nhìn thấy), bạn cần chỉnh sửa một chút: thông báo lỗi và cờ mà callback đặt phải được tổng quát hóa.::

   def check_order(option, opt_str, value, parser):
       if parser.values.b:
           raise OptionValueError("can't use %s after -b" % opt_str)
       setattr(parser.values, option.dest, 1)
   ...
   parser.add_option("-a", action="callback", callback=check_order, dest='a')
   parser.add_option("-b", action="store_true", dest="b")
   parser.add_option("-c", action="callback", callback=check_order, dest='c')


.. _optparse-callback-example-4:

Ví dụ callback 4: kiểm tra điều kiện tùy ý
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tất nhiên, bạn có thể đặt bất kỳ điều kiện nào vào đó---bạn không bị giới hạn trong việc kiểm tra giá trị của các option đã được định nghĩa. Ví dụ, nếu bạn có các option không nên được gọi khi trăng tròn, tất cả những gì bạn cần làm là như sau::

   def check_moon(option, opt_str, value, parser):
       if is_moon_full():
           raise OptionValueError("%s option invalid when moon is full"
                                  % opt_str)
       setattr(parser.values, option.dest, 1)
   ...
   parser.add_option("--foo",
                     action="callback", callback=check_moon, dest="foo")

(Phần định nghĩa ``is_moon_full()`` được để cho người đọc tự thực hiện.)


.. _optparse-callback-example-5:

Ví dụ callback 5: các đối số cố định
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mọi thứ trở nên thú vị hơn một chút khi bạn định nghĩa các option callback nhận số lượng đối số cố định. Việc chỉ định rằng một option callback nhận các đối số tương tự như định nghĩa option ``"store"`` hoặc ``"append"``: nếu bạn định nghĩa
:attr:`~Option.type`, thì option này nhận một đối số phải có thể chuyển đổi thành kiểu đó; nếu bạn định nghĩa thêm :attr:`~Option.nargs`, thì option này nhận :attr:`~Option.nargs` đối số.

Dưới đây là một ví dụ chỉ mô phỏng action ``"store"`` tiêu chuẩn::

   def store_value(option, opt_str, value, parser):
       setattr(parser.values, option.dest, value)
   ...
   parser.add_option("--foo",
                     action="callback", callback=store_value,
                     type="int", nargs=3, dest="foo")

Lưu ý rằng :mod:`!optparse` đảm nhiệm việc nhận 3 đối số và chuyển chúng thành số nguyên; tất cả những gì bạn cần làm là lưu trữ chúng. (Hoặc tùy bạn; rõ ràng là bạn không cần callback cho ví dụ này.)


.. _optparse-callback-example-6:

Ví dụ callback 6: đối số biến đổi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mọi chuyện trở nên phức tạp khi bạn muốn một tùy chọn nhận số lượng đối số biến đổi. Trong trường hợp này, bạn phải viết một callback, vì :mod:`!optparse` không cung cấp sẵn khả năng này. Và bạn phải xử lý một số chi tiết phức tạp trong việc phân tích cú pháp dòng lệnh Unix thông thường mà :mod:`!optparse` thường đảm nhiệm thay bạn. Cụ thể, callback nên triển khai các quy tắc thông thường cho các đối số ``--`` và ``-`` đứng riêng như sau:

* ``--`` hoặc ``-`` đều có thể là đối số của tùy chọn

* ``--`` đứng riêng (nếu không phải là đối số của một tùy chọn nào đó): dừng xử lý dòng lệnh và loại bỏ ``--``

* ``-`` đứng riêng (nếu không phải là đối số của một tùy chọn nào đó): dừng xử lý dòng lệnh nhưng giữ lại ``-`` (nối nó vào ``parser.largs``)

Nếu bạn muốn một tùy chọn nhận số lượng đối số biến đổi, có một số vấn đề tinh tế và phức tạp cần lưu ý. Cách triển khai chính xác mà bạn chọn sẽ dựa trên những đánh đổi mà bạn sẵn sàng chấp nhận cho ứng dụng của mình (đó là lý do :mod:`!optparse` không hỗ trợ trực tiếp kiểu này).

Tuy vậy, dưới đây là một thử nghiệm về callback cho một tùy chọn có số lượng đối số thay đổi::

    def vararg_callback(option, opt_str, value, parser):
        assert value is None
        value = []

        def floatable(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        for arg in parser.rargs:
            # dừng với các tùy chọn như --foo
            if arg[:2] == "--" and len(arg) > 2:
                break
            # dừng với -a, nhưng không dừng với -3 hoặc -3.0
            if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
                break
            value.append(arg)

        del parser.rargs[:len(value)]
        setattr(parser.values, option.dest, value)

    ...
    parser.add_option("-c", "--callback", dest="vararg_attr",
                      action="callback", callback=vararg_callback)


.. _optparse-extending-optparse:

Mở rộng :mod:`!optparse`
------------------------

Vì hai yếu tố chính chi phối cách :mod:`!optparse` diễn giải các tùy chọn dòng lệnh là action và type của từng tùy chọn, hướng mở rộng nhiều khả năng nhất là thêm các action mới và type mới.


.. _optparse-adding-new-types:

Thêm type mới
^^^^^^^^^^^^^

Để thêm type mới, bạn cần định nghĩa một lớp con của :mod:`!optparse`
:class:`Option` lớp. Lớp này có một vài thuộc tính xác định
các kiểu của :mod:`!optparse`: :attr:`~Option.TYPES` và :attr:`~Option.TYPE_CHECKER`.

.. attribute:: Option.TYPES

   Một tuple gồm các tên kiểu; trong lớp con của bạn, chỉ cần định nghĩa một tuple mới
   :attr:`TYPES` được xây dựng dựa trên tuple chuẩn.

.. attribute:: Option.TYPE_CHECKER

   Một dictionary ánh xạ tên kiểu tới các hàm kiểm tra kiểu. Một hàm kiểm tra kiểu có signature sau::

      def check_mytype(option, opt, value)

   trong đó ``option`` là một instance của :class:`Option`, ``opt`` là một option string (ví dụ: ``-f``), và ``value`` là chuỗi từ command line cần được kiểm tra và chuyển đổi thành kiểu mong muốn. ``check_mytype()`` phải trả về một object thuộc kiểu giả định ``mytype``. Giá trị do một hàm kiểm tra kiểu trả về cuối cùng sẽ nằm trong instance OptionValues được :meth:`OptionParser.parse_args` trả về, hoặc được truyền tới callback dưới dạng tham số ``value``.

   Hàm kiểm tra kiểu của bạn phải raise :exc:`OptionValueError` nếu gặp bất kỳ vấn đề nào. :exc:`OptionValueError` nhận một đối số chuỗi duy nhất, được truyền nguyên trạng tới method :meth:`error` của :class:`OptionParser`, method này lần lượt thêm tên chương trình và chuỗi ``"error:"`` vào đầu, rồi in mọi thứ ra stderr trước khi kết thúc process.

Đây là một ví dụ ngớ ngẩn minh họa cách thêm một kiểu tùy chọn ``"complex"`` để phân tích các số phức theo kiểu Python trên dòng lệnh. (Điều này thậm chí còn ngớ ngẩn hơn trước, vì :mod:`!optparse` 1.3 đã tích hợp sẵn hỗ trợ cho số phức, nhưng thôi không bàn.)

Trước tiên, các import cần thiết::

   from copy import copy
   from optparse import Option, OptionValueError

Trước hết, bạn cần định nghĩa bộ kiểm tra kiểu, vì nó được tham chiếu sau đó (trong
thuộc tính lớp :attr:`~Option.TYPE_CHECKER` của lớp con Option của bạn)::

   def check_complex(option, opt, value):
       try:
           return complex(value)
       except ValueError:
           raise OptionValueError(
               "option %s: invalid complex value: %r" % (opt, value))

Cuối cùng, lớp con Option::

   class MyOption (Option):
       TYPES = Option.TYPES + ("complex",)
       TYPE_CHECKER = copy(Option.TYPE_CHECKER)
       TYPE_CHECKER["complex"] = check_complex

(Nếu chúng ta không tạo một :func:`copy` của :attr:`Option.TYPE_CHECKER`, cuối cùng chúng ta sẽ sửa đổi thuộc tính :attr:`~Option.TYPE_CHECKER` của lớp Option của :mod:`!optparse`. Vì đây là Python, không có gì ngăn bạn làm vậy ngoài phép lịch sự và lẽ thường.)

Vậy là xong! Giờ bạn có thể viết một script sử dụng kiểu tùy chọn mới giống như bất kỳ script nào khác dựa trên :mod:`!optparse`\ , ngoại trừ việc bạn phải chỉ dẫn OptionParser sử dụng MyOption thay vì Option::

   parser = OptionParser(option_class=MyOption)
   parser.add_option("-c", type="complex")

Ngoài ra, bạn có thể tự xây dựng danh sách tùy chọn và truyền danh sách đó cho OptionParser; nếu bạn không sử dụng :meth:`add_option` theo cách trên, bạn không cần cho OptionParser biết nên sử dụng lớp tùy chọn nào::

   option_list = [MyOption("-c", action="store", type="complex", dest="c")]
   parser = OptionParser(option_list=option_list)


.. _optparse-adding-new-actions:

Thêm action mới
^^^^^^^^^^^^^^^

Việc thêm action mới phức tạp hơn một chút, vì bạn phải hiểu rằng
:mod:`!optparse` phân loại action thành một vài nhóm:

action "store"
   các action khiến :mod:`!optparse` lưu một giá trị vào thuộc tính của thực thể OptionValues hiện tại; các tùy chọn này yêu cầu cung cấp thuộc tính :attr:`~Option.dest` cho hàm khởi tạo Option.

action "typed"
   các action nhận một giá trị từ command line và yêu cầu giá trị đó thuộc một kiểu nhất định; hay chính xác hơn là một chuỗi có thể được chuyển đổi sang một kiểu nhất định. Các tùy chọn này yêu cầu một thuộc tính :attr:`~Option.type` trong hàm khởi tạo Option.

Đây là các tập hợp chồng lấp nhau: một số action "store" mặc định là ``"store"``, ``"store_const"``, ``"append"`` và ``"count"``, trong khi các action "typed" mặc định là ``"store"``, ``"append"`` và ``"callback"``.

Khi thêm một action, bạn cần phân loại action đó bằng cách liệt kê nó trong ít nhất một trong các thuộc tính lớp sau của Option (tất cả đều là danh sách các chuỗi):

.. attribute:: Option.ACTIONS

   Tất cả action phải được liệt kê trong ACTIONS.

.. attribute:: Option.STORE_ACTIONS

   Các action "store" cũng được liệt kê tại đây.

.. attribute:: Option.TYPED_ACTIONS

   Các action "typed" cũng được liệt kê tại đây.

.. attribute:: Option.ALWAYS_TYPED_ACTIONS

   Các action luôn nhận một kiểu (tức là các tùy chọn của chúng luôn nhận một giá trị) cũng được liệt kê tại đây. Tác dụng duy nhất của việc này là :mod:`!optparse` gán kiểu mặc định, ``"string"``, cho các tùy chọn không có kiểu được chỉ định rõ ràng mà action của chúng được liệt kê trong :attr:`ALWAYS_TYPED_ACTIONS`.

Để thực sự triển khai action mới, bạn phải ghi đè
:meth:`take_action` method của Option và thêm một case nhận diện action của bạn.

Ví dụ, hãy thêm một action ``"extend"``. Action này tương tự như action ``"append"`` tiêu chuẩn, nhưng thay vì nhận một giá trị duy nhất từ command-line rồi nối giá trị đó vào một list hiện có, ``"extend"`` sẽ nhận nhiều giá trị trong một chuỗi được phân tách bằng dấu phẩy và mở rộng list hiện có bằng các giá trị đó. Nghĩa là, nếu ``--names`` là một option ``"extend"`` thuộc kiểu ``"string"``, command line::

   --names=foo,bar --names blah --names ding,dong

sẽ tạo ra một list::

   ["foo", "bar", "blah", "ding", "dong"]

Một lần nữa, chúng ta định nghĩa một subclass của Option::

   class MyOption(Option):

       ACTIONS = Option.ACTIONS + ("extend",)
       STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
       TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
       ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

       def take_action(self, action, dest, opt, value, values, parser):
           if action == "extend":
               lvalue = value.split(",")
               values.ensure_value(dest, []).extend(lvalue)
           else:
               Option.take_action(
                   self, action, dest, opt, value, values, parser)

Các tính năng đáng chú ý:

* ``"extend"`` vừa yêu cầu một giá trị trên command-line vừa lưu giá trị đó ở đâu đó, vì vậy nó nằm trong cả :attr:`~Option.STORE_ACTIONS` và
  :attr:`~Option.TYPED_ACTIONS`.

* để đảm bảo rằng :mod:`!optparse` gán kiểu mặc định là ``"string"`` cho các action ``"extend"``, chúng ta đưa action ``"extend"`` vào
  :attr:`~Option.ALWAYS_TYPED_ACTIONS` nữa.

* :meth:`MyOption.take_action` chỉ triển khai action mới này, rồi chuyển quyền điều khiển lại cho :meth:`Option.take_action` để xử lý các action :mod:`!optparse` tiêu chuẩn.

* ``values`` là một instance của lớp optparse_parser.Values, lớp này cung cấp method :meth:`ensure_value` rất hữu ích. Về cơ bản, :meth:`ensure_value` là :func:`getattr` có thêm cơ chế an toàn; nó được gọi như sau::

     values.ensure_value(attr, value)

  Nếu thuộc tính ``attr`` của ``values`` không tồn tại hoặc là ``None``, thì ensure_value() trước tiên đặt nó thành ``value``, rồi trả về ``value``. Điều này rất hữu ích cho các action như ``"extend"``, ``"append"`` và ``"count"``, tất cả đều tích lũy dữ liệu vào một biến và yêu cầu biến đó có một kiểu nhất định (list đối với hai action đầu, integer đối với action cuối). Sử dụng
  :meth:`ensure_value` có nghĩa là các script sử dụng action của bạn không phải lo việc đặt giá trị mặc định cho các option destination tương ứng; chúng chỉ cần để giá trị mặc định là ``None`` và :meth:`ensure_value` sẽ đảm nhiệm việc lấy đúng giá trị khi cần.

Ngoại lệ
--------

.. exception:: OptionError

   Được phát sinh nếu một instance :class:`Option` được tạo với các đối số không hợp lệ hoặc không nhất quán.

.. exception:: OptionConflictError

   Được phát sinh nếu các tùy chọn xung đột được thêm vào :class:`OptionParser`.

.. exception:: OptionValueError

   Được phát sinh nếu gặp giá trị tùy chọn không hợp lệ trên dòng lệnh.

.. exception:: BadOptionError

   Được phát sinh nếu một tùy chọn không hợp lệ được truyền trên dòng lệnh.

.. exception:: AmbiguousOptionError

   Được phát sinh nếu một tùy chọn mơ hồ được truyền trên dòng lệnh.
