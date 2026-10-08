:mod:`!shlex` --- Phân tích từ vựng đơn giản
============================================

.. module:: shlex
   :synopsis: Phân tích từ vựng đơn giản cho các ngôn ngữ giống shell Unix.

.. moduleauthor:: Eric S. Raymond <esr@snark.thyrsus.com>
.. moduleauthor:: Gustavo Niemeyer <niemeyer@conectiva.com>
.. sectionauthor:: Eric S. Raymond <esr@snark.thyrsus.com>
.. sectionauthor:: Gustavo Niemeyer <niemeyer@conectiva.com>

**Mã nguồn:** :source:`Lib/shlex.py`

--------------

Lớp :class:`~shlex.shlex` giúp dễ dàng viết các bộ phân tích từ vựng cho những cú pháp đơn giản tương tự shell Unix. Điều này thường hữu ích khi viết các ngôn ngữ nhỏ (ví dụ: trong các tệp điều khiển chạy cho ứng dụng Python) hoặc khi phân tích các chuỗi được đặt trong dấu trích dẫn.

Module :mod:`!shlex` định nghĩa các hàm sau:


.. function:: split(s, comments=False, posix=True)

   Tách chuỗi *s* bằng cú pháp tương tự shell. Nếu *comments* là :const:`False` (mặc định), việc phân tích chú thích trong chuỗi đã cho sẽ bị tắt (bằng cách đặt thuộc tính :attr:`~shlex.commenters` của
   :class:`~shlex.shlex` instance thành chuỗi rỗng). Hàm này hoạt động ở chế độ POSIX theo mặc định, nhưng sử dụng chế độ không phải POSIX nếu đối số *posix* là false.

   .. versionchanged:: 3.12
      Việc truyền ``None`` cho đối số *s* hiện sẽ gây ra một ngoại lệ, thay vì đọc :data:`sys.stdin`.

.. function:: join(split_command)

   Nối các token trong danh sách *split_command* và trả về một chuỗi. Hàm này là phép nghịch đảo của :func:`split`.

      >>> from shlex import join
      >>> print(join(['echo', '-n', 'Multiple words']))
      echo -n 'Multiple words'

   Giá trị trả về được escape cho shell để bảo vệ khỏi các lỗ hổng chèn lệnh (xem :func:`quote`).

   .. versionadded:: 3.8


.. function:: quote(s)

   Trả về phiên bản được escape cho shell của chuỗi *s*. Giá trị trả về là một chuỗi có thể được sử dụng an toàn làm một token trong dòng lệnh shell, trong các trường hợp bạn không thể sử dụng một danh sách.

   .. _shlex-quote-warning:

   .. warning::

      Mô-đun ``shlex`` **chỉ được thiết kế cho Unix shells**.

      Hàm :func:`quote` không được đảm bảo là chính xác trên các shell không tuân thủ POSIX hoặc các shell của những hệ điều hành khác như Windows. Việc thực thi các lệnh được module này đặt trong dấu quote trên những shell đó có thể làm phát sinh nguy cơ lỗ hổng chèn lệnh.

      Hãy cân nhắc sử dụng các hàm truyền đối số lệnh bằng danh sách, chẳng hạn như
      :func:`subprocess.run` với ``shell=False``.

   Cách viết này sẽ không an toàn:

      >>> filename = 'somefile; rm -rf ~'
      >>> command = 'ls -l {}'.format(filename)
      >>> print(command)  # được shell thực thi: boom!
      ls -l somefile; rm -rf ~

   :func:`quote` cho phép bạn khắc phục lỗ hổng bảo mật này:

      >>> from shlex import quote
      >>> command = 'ls -l {}'.format(quote(filename))
      >>> print(command)
      ls -l 'somefile; rm -rf ~'
      >>> remote_command = 'ssh home {}'.format(quote(command))
      >>> print(remote_command)
      ssh home 'ls -l '"'"'somefile; rm -rf ~'"'"''

   Cách trích dẫn này tương thích với các shell UNIX và với :func:`split`:

      >>> from shlex import split
      >>> remote_command = split(remote_command)
      >>> remote_command
      ['ssh', 'home', "ls -l 'somefile; rm -rf ~'"]
      >>> command = split(remote_command[-1])
      >>> command
      ['ls', '-l', 'somefile; rm -rf ~']

   .. versionadded:: 3.3

Mô-đun :mod:`!shlex` định nghĩa lớp sau:


.. class:: shlex(instream=None, infile=None, posix=False, punctuation_chars=False)

   Một đối tượng :class:`~shlex.shlex` hoặc một đối tượng của lớp con là một đối tượng bộ phân tích từ vựng. Đối số khởi tạo, nếu có, chỉ định nơi đọc các ký tự. Đối số này phải là một đối tượng giống tệp/luồng có
   các phương thức :meth:`~io.TextIOBase.read` và :meth:`~io.TextIOBase.readline`, hoặc một chuỗi. Nếu không cung cấp đối số, dữ liệu đầu vào sẽ được lấy từ ``sys.stdin``. Đối số tùy chọn thứ hai là một chuỗi tên tệp, dùng để thiết lập giá trị ban đầu của thuộc tính :attr:`~shlex.infile`. Nếu đối số *instream* bị bỏ qua hoặc bằng ``sys.stdin``, đối số thứ hai này mặc định là "stdin". Đối số *posix* xác định chế độ hoạt động: khi *posix* không phải là true (mặc định), thực thể :class:`~shlex.shlex` sẽ hoạt động ở chế độ tương thích. Khi hoạt động ở chế độ POSIX,
   :class:`~shlex.shlex` sẽ cố gắng tuân thủ các quy tắc phân tích cú pháp của shell POSIX sát nhất có thể. Đối số *punctuation_chars* cung cấp một cách để hành vi này gần với cách các shell thực tế phân tích cú pháp hơn nữa. Đối số này có thể nhận một số giá trị: giá trị mặc định, ``False``, giữ nguyên hành vi có trong Python 3.5 trở về trước. Nếu được đặt thành ``True``, việc phân tích cú pháp các ký tự ``();<>|&`` sẽ thay đổi: mọi chuỗi liên tiếp gồm các ký tự này (được xem là các ký tự dấu câu) sẽ được trả về dưới dạng một token duy nhất. Nếu được đặt thành một chuỗi ký tự không rỗng, các ký tự đó sẽ được dùng làm các ký tự dấu câu. Mọi ký tự trong thuộc tính :attr:`wordchars` xuất hiện trong *punctuation_chars* sẽ bị loại bỏ khỏi :attr:`wordchars`. Xem
   :ref:`improved-shell-compatibility` để biết thêm thông tin. Chỉ có thể đặt *punctuation_chars* khi tạo thực thể :class:`~shlex.shlex` và không thể sửa đổi sau đó.

   .. versionchanged:: 3.6
      Tham số *punctuation_chars* đã được thêm vào.

.. seealso::

   Mô-đun :mod:`configparser`
      Bộ phân tích cú pháp cho các tệp cấu hình tương tự như các tệp :file:`.ini` của Windows.


.. _shlex-objects:

Đối tượng shlex
---------------

Một instance :class:`~shlex.shlex` có các phương thức sau:


.. method:: shlex.get_token()

   Trả về một token. Nếu các token đã được xếp chồng bằng :meth:`push_token`, lấy một token khỏi ngăn xếp. Nếu không, đọc một token từ luồng đầu vào. Nếu thao tác đọc gặp ngay cuối tệp, :attr:`eof` được trả về (chuỗi rỗng (``''``) ở chế độ không POSIX và ``None`` ở chế độ POSIX).


.. method:: shlex.push_token(str)

   Đẩy đối số vào ngăn xếp token.


.. method:: shlex.read_token()

   Đọc một raw token. Bỏ qua ngăn xếp pushback và không diễn giải các yêu cầu source. (Đây thường không phải là một điểm truy cập hữu ích và chỉ được ghi lại ở đây để đầy đủ.)


.. method:: shlex.sourcehook(filename)

   Khi :class:`~shlex.shlex` phát hiện một yêu cầu source (xem :attr:`source` bên dưới), phương thức này được truyền token tiếp theo làm đối số và phải trả về một tuple gồm tên tệp và một đối tượng giống tệp đã mở.

   Thông thường, phương thức này trước tiên loại bỏ mọi dấu ngoặc kép khỏi đối số. Nếu kết quả là một pathname tuyệt đối, hoặc trước đó chưa có yêu cầu source nào, hoặc source trước đó là một stream (chẳng hạn như ``sys.stdin``), thì giữ nguyên kết quả. Nếu không, khi kết quả là một pathname tương đối, phần thư mục trong tên của tệp ngay trước nó trên ngăn xếp đưa source vào sẽ được thêm vào trước (cách hoạt động này tương tự cách bộ tiền xử lý C xử lý ``#include "file.h"``).

   Kết quả của các thao tác trên được xem là tên tệp và được trả về dưới dạng thành phần đầu tiên của tuple, còn :func:`open` được gọi trên nó để tạo thành phần thứ hai. (Lưu ý: thứ tự này ngược với thứ tự các đối số khi khởi tạo instance!)

   Hook này được cung cấp để bạn có thể dùng nó triển khai các đường dẫn tìm kiếm thư mục, việc bổ sung phần mở rộng tệp và các thủ thuật namespace khác. Không có hook 'close' tương ứng, nhưng một instance shlex sẽ gọi
   phương thức :meth:`~io.IOBase.close` của input stream nguồn khi nó trả về EOF.

   Để kiểm soát rõ ràng hơn việc xếp chồng nguồn, hãy sử dụng các phương thức :meth:`push_source` và
   :meth:`pop_source`.


.. method:: shlex.push_source(newstream, newfile=None)

   Đẩy một input source stream vào input stack. Nếu chỉ định đối số filename, giá trị này sẽ có sẵn để sử dụng sau trong các thông báo lỗi. Đây cũng là phương thức được :meth:`sourcehook` sử dụng nội bộ.


.. method:: shlex.pop_source()

   Lấy input source được đẩy vào sau cùng ra khỏi input stack. Đây cũng là phương thức được sử dụng nội bộ khi lexer gặp EOF trên một input stream đã được xếp chồng.


.. method:: shlex.error_leader(infile=None, lineno=None)

   Phương thức này tạo phần đầu của thông báo lỗi theo định dạng nhãn lỗi của trình biên dịch Unix C; định dạng là ``'"%s", line %d: '``, trong đó ``%s`` được thay thế bằng tên của tệp nguồn hiện tại và ``%d`` bằng số dòng input hiện tại (có thể sử dụng các đối số tùy chọn để ghi đè các giá trị này).

   Tính tiện lợi này được cung cấp nhằm khuyến khích người dùng :mod:`!shlex` tạo thông báo lỗi theo định dạng chuẩn, có thể phân tích cú pháp, được Emacs và các công cụ Unix khác hiểu.

Các thể hiện của những lớp con :class:`~shlex.shlex` có một số biến thể hiện công khai, dùng để điều khiển việc phân tích từ vựng hoặc phục vụ gỡ lỗi:


.. attribute:: shlex.commenters

   Chuỗi các ký tự được nhận diện là ký tự bắt đầu chú thích. Tất cả ký tự từ ký tự bắt đầu chú thích đến cuối dòng đều bị bỏ qua. Theo mặc định, chỉ bao gồm ``'#'``.


.. attribute:: shlex.wordchars

   Chuỗi các ký tự sẽ được tích lũy thành các token nhiều ký tự. Theo mặc định, bao gồm tất cả các ký tự chữ và số ASCII cùng dấu gạch dưới. Ở chế độ POSIX, các ký tự có dấu trong bộ Latin-1 cũng được bao gồm. Nếu
   :attr:`punctuation_chars` không rỗng, các ký tự ``~-./*?=``, có thể xuất hiện trong đặc tả tên tệp và tham số dòng lệnh, cũng sẽ được bao gồm trong thuộc tính này, và mọi ký tự xuất hiện trong ``punctuation_chars`` sẽ bị xóa khỏi ``wordchars`` nếu chúng có mặt ở đó. Nếu :attr:`whitespace_split` được đặt thành ``True``, điều này sẽ không có tác dụng.


.. attribute:: shlex.whitespace

   Các ký tự được xem là khoảng trắng và bị bỏ qua. Khoảng trắng phân tách các token. Theo mặc định, bao gồm dấu cách, tab, ký tự xuống dòng và ký tự về đầu dòng.


.. attribute:: shlex.escape

   Các ký tự được xem là ký tự escape. Thuộc tính này chỉ được sử dụng ở chế độ POSIX và theo mặc định chỉ bao gồm ``'\'``.


.. attribute:: shlex.quotes

   Các ký tự được coi là dấu nháy chuỗi. Token sẽ được tích lũy cho đến khi gặp lại cùng dấu nháy đó (do đó, các loại dấu nháy khác nhau sẽ bảo vệ lẫn nhau như trong shell). Mặc định, bao gồm dấu nháy đơn và dấu nháy kép ASCII.


.. attribute:: shlex.escapedquotes

   Các ký tự trong :attr:`quotes` sẽ diễn giải các ký tự escape được định nghĩa trong
   :attr:`escape`. Tùy chọn này chỉ được sử dụng ở chế độ POSIX và theo mặc định chỉ bao gồm ``'"'``.


.. attribute:: shlex.whitespace_split

   Nếu ``True``, các token sẽ chỉ được tách tại khoảng trắng. Điều này hữu ích, chẳng hạn, khi phân tích các dòng lệnh có :class:`~shlex.shlex`, để lấy các token theo cách tương tự như các đối số shell. Khi được sử dụng kết hợp với
   :attr:`punctuation_chars`, các token sẽ được tách tại khoảng trắng ngoài các ký tự đó.

   .. versionchanged:: 3.8
      Thuộc tính :attr:`punctuation_chars` được tạo để tương thích với thuộc tính
      :attr:`whitespace_split`.


.. attribute:: shlex.infile

   Tên của tệp đầu vào hiện tại, được thiết lập ban đầu khi khởi tạo lớp hoặc được xếp chồng bởi các yêu cầu nguồn sau đó. Có thể hữu ích khi kiểm tra tên này trong lúc xây dựng thông báo lỗi.


.. attribute:: shlex.instream

   Luồng đầu vào mà từ đó thực thể :class:`~shlex.shlex` này đang đọc các ký tự.


.. attribute:: shlex.source

   Theo mặc định, thuộc tính này là ``None``. Nếu bạn gán cho nó một chuỗi, chuỗi đó sẽ được nhận diện là yêu cầu đưa vào ở cấp từ vựng, tương tự từ khóa ``source`` trong nhiều shell. Nghĩa là, token ngay sau đó sẽ được mở dưới dạng tên tệp và dữ liệu đầu vào sẽ được đọc từ luồng đó cho đến EOF; tại thời điểm đó, phương thức :meth:`~io.IOBase.close` của luồng sẽ được gọi và nguồn đầu vào sẽ trở lại luồng đầu vào ban đầu. Các yêu cầu nguồn có thể được xếp chồng ở bất kỳ số cấp nào.


.. attribute:: shlex.debug

   Nếu thuộc tính này là số và lớn hơn hoặc bằng ``1``, một thực thể :class:`~shlex.shlex` sẽ in thông tin tiến trình chi tiết về hoạt động của nó. Nếu cần sử dụng tính năng này, bạn có thể đọc mã nguồn của module để tìm hiểu chi tiết.


.. attribute:: shlex.lineno

   Số dòng nguồn (số dòng mới đã gặp cho đến thời điểm hiện tại cộng một).


.. attribute:: shlex.token

   Bộ đệm token. Có thể hữu ích khi kiểm tra bộ đệm này trong lúc bắt ngoại lệ.


.. attribute:: shlex.eof

   Token được dùng để xác định cuối tệp. Ở chế độ không phải POSIX, token này sẽ được đặt thành chuỗi rỗng (``''``), còn ở chế độ POSIX sẽ được đặt thành ``None``.


.. attribute:: shlex.punctuation_chars

   Một thuộc tính chỉ đọc. Các ký tự được xem là dấu câu. Các chuỗi ký tự dấu câu sẽ được trả về dưới dạng một token duy nhất. Tuy nhiên, lưu ý rằng sẽ không thực hiện kiểm tra tính hợp lệ về mặt ngữ nghĩa: chẳng hạn, '>>>' có thể được trả về dưới dạng một token, dù shell có thể không nhận dạng nó như vậy.

   .. versionadded:: 3.6


.. _shlex-parsing-rules:

Quy tắc phân tích cú pháp
-------------------------

Khi hoạt động ở chế độ không phải POSIX, :class:`~shlex.shlex` sẽ cố gắng tuân theo các quy tắc sau.

* Các ký tự trích dẫn không được nhận dạng bên trong từ (``Do"Not"Separate`` được phân tích thành một từ duy nhất là ``Do"Not"Separate``);

* Các ký tự escape không được nhận dạng;

* Việc đặt các ký tự bên trong dấu trích dẫn sẽ giữ nguyên giá trị literal của tất cả các ký tự nằm trong dấu trích dẫn;

* Dấu trích dẫn đóng sẽ phân tách các từ (``"Do"Separate`` được phân tích thành ``"Do"`` và ``Separate``);

* Nếu :attr:`~shlex.whitespace_split` là ``False``, mọi ký tự không được khai báo là ký tự từ, khoảng trắng hoặc dấu ngoặc kép sẽ được trả về dưới dạng một token đơn ký tự. Nếu là ``True``, :class:`~shlex.shlex` sẽ chỉ tách các từ tại khoảng trắng;

* EOF được báo hiệu bằng một chuỗi rỗng (``''``);

* Không thể phân tích cú pháp các chuỗi rỗng, ngay cả khi chúng được đặt trong dấu ngoặc kép.

Khi hoạt động ở chế độ POSIX, :class:`~shlex.shlex` sẽ cố gắng tuân theo các quy tắc phân tích cú pháp sau đây.

* Các dấu ngoặc kép sẽ bị loại bỏ và không phân tách các từ (``"Do"Not"Separate"`` được phân tích thành từ duy nhất ``DoNotSeparate``);

* Các ký tự escape không được đặt trong dấu ngoặc kép (ví dụ: ``'\'``) bảo toàn giá trị literal của ký tự tiếp theo sau đó;

* Việc đặt các ký tự bao quanh trong dấu ngoặc kép mà không phải là một phần của
  :attr:`~shlex.escapedquotes` (ví dụ: ``"'"``) bảo toàn giá trị nguyên gốc của tất cả các ký tự nằm trong dấu nháy;

* Các ký tự bao quanh trong dấu nháy là một phần của
  :attr:`~shlex.escapedquotes` (ví dụ: ``'"'``) bảo toàn giá trị nguyên gốc của tất cả các ký tự nằm trong dấu nháy, ngoại trừ các ký tự được đề cập trong :attr:`~shlex.escape`. Các ký tự escape chỉ giữ ý nghĩa đặc biệt khi đứng trước dấu nháy đang được sử dụng hoặc chính ký tự escape. Trong các trường hợp khác, ký tự escape sẽ được coi là ký tự thông thường.

* EOF được báo hiệu bằng giá trị :const:`None`;

* Cho phép sử dụng các chuỗi rỗng được đặt trong dấu nháy (``''``).

.. _improved-shell-compatibility:

Cải thiện khả năng tương thích với Shell
----------------------------------------

.. versionadded:: 3.6

Lớp :class:`shlex` cung cấp khả năng tương thích với cách phân tích cú pháp của các Unix shell phổ biến như ``bash``, ``dash`` và ``sh``. Để tận dụng khả năng tương thích này, hãy chỉ định đối số ``punctuation_chars`` trong constructor. Giá trị mặc định là ``False``, giúp duy trì hành vi trước phiên bản 3.6. Tuy nhiên, nếu đặt thành ``True``, cách phân tích các ký tự ``();<>|&`` sẽ thay đổi: mọi chuỗi liên tiếp gồm các ký tự này sẽ được trả về dưới dạng một token duy nhất. Mặc dù chưa phải là một parser đầy đủ cho shell (điều này nằm ngoài phạm vi của standard library vì có rất nhiều shell khác nhau), tính năng này vẫn cho phép bạn xử lý command line dễ dàng hơn so với trước đây. Để minh họa, bạn có thể xem sự khác biệt trong đoạn mã sau:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> import shlex
   >>> text = "a && b; c && d || e; f >'abc'; (def \"ghi\")"
   >>> s = shlex.shlex(text, posix=True)
   >>> s.whitespace_split = True
   >>> list(s)
   ['a', '&&', 'b;', 'c', '&&', 'd', '||', 'e;', 'f', '>abc;', '(def', 'ghi)']
   >>> s = shlex.shlex(text, posix=True, punctuation_chars=True)
   >>> s.whitespace_split = True
   >>> list(s)
   ['a', '&&', 'b', ';', 'c', '&&', 'd', '||', 'e', ';', 'f', '>', 'abc', ';',
   '(', 'def', 'ghi', ')']

Tất nhiên, sẽ có những token được trả về không hợp lệ đối với shell, và bạn sẽ cần tự triển khai việc kiểm tra lỗi trên các token được trả về.

Thay vì truyền ``True`` làm giá trị cho tham số punctuation_chars, bạn có thể truyền một chuỗi gồm các ký tự cụ thể, được dùng để xác định những ký tự nào tạo thành dấu câu. Ví dụ::

   >>> import shlex
   >>> s = shlex.shlex("a && b || c", punctuation_chars="|")
   >>> list(s)
   ['a', '&', '&', 'b', '||', 'c']

.. note:: Khi ``punctuation_chars`` được chỉ định, thuộc tính :attr:`~shlex.wordchars` sẽ được bổ sung các ký tự ``~-./*?=``. Đó là vì các ký tự này có thể xuất hiện trong tên tệp (bao gồm cả wildcard) và đối số dòng lệnh (ví dụ: ``--color=auto``). Do đó::

      >>> import shlex
      >>> s = shlex.shlex('~/a && b-c --color=auto || d *.py?',
      ...                 punctuation_chars=True)
      >>> list(s)
      ['~/a', '&&', 'b-c', '--color=auto', '||', 'd', '*.py?']

   Tuy nhiên, để khớp với shell sát nhất có thể, bạn nên luôn sử dụng ``posix`` và :attr:`~shlex.whitespace_split` khi sử dụng
   :attr:`~shlex.punctuation_chars`, điều này sẽ vô hiệu hóa
   hoàn toàn :attr:`~shlex.wordchars`.

Để đạt hiệu quả tốt nhất, ``punctuation_chars`` nên được đặt cùng với ``posix=True``. (Lưu ý rằng ``posix=False`` là mặc định cho
:class:`~shlex.shlex`.)
