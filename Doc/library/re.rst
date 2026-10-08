:mod:`!re` --- Các thao tác với biểu thức chính quy
===================================================

.. module:: re
   :synopsis: Các thao tác với biểu thức chính quy.

.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>
.. sectionauthor:: Andrew M. Kuchling <amk@amk.ca>

**Mã nguồn:** :source:`Lib/re/`

--------------

Module này cung cấp các thao tác so khớp biểu thức chính quy tương tự như các thao tác trong Perl.

Cả pattern và chuỗi được tìm kiếm đều có thể là chuỗi Unicode (:class:`str`) cũng như chuỗi 8-bit (:class:`bytes`). Tuy nhiên, không thể trộn chuỗi Unicode và chuỗi 8-bit: tức là bạn không thể so khớp một chuỗi Unicode với một pattern bytes hoặc ngược lại; tương tự, khi yêu cầu thay thế, chuỗi thay thế phải có cùng kiểu với cả pattern và chuỗi tìm kiếm.

Biểu thức chính quy sử dụng ký tự dấu gạch chéo ngược (``'\'``) để chỉ các dạng đặc biệt hoặc cho phép sử dụng các ký tự đặc biệt mà không kích hoạt ý nghĩa đặc biệt của chúng. Điều này xung đột với cách Python sử dụng cùng ký tự đó cho cùng mục đích trong các string literal; chẳng hạn, để so khớp một dấu gạch chéo ngược literal, bạn có thể phải viết ``'\\\\'`` làm chuỗi pattern, vì biểu thức chính quy phải là ``\\``, và mỗi dấu gạch chéo ngược phải được biểu diễn dưới dạng ``\\`` bên trong một string literal Python thông thường. Ngoài ra, xin lưu ý rằng mọi chuỗi escape không hợp lệ khi Python sử dụng dấu gạch chéo ngược trong string literal hiện sẽ tạo ra một :exc:`SyntaxWarning`, và trong tương lai điều này sẽ trở thành một :exc:`SyntaxError`. Hành vi này sẽ xảy ra ngay cả khi đó là một chuỗi escape hợp lệ đối với biểu thức chính quy.

Giải pháp là sử dụng ký hiệu chuỗi raw của Python cho các pattern biểu thức chính quy; dấu gạch chéo ngược không được xử lý theo bất kỳ cách đặc biệt nào trong một string literal có tiền tố ``'r'``. Vì vậy, ``r"\n"`` là một chuỗi gồm hai ký tự chứa ``'\'`` và ``'n'``, trong khi ``"\n"`` là một chuỗi một ký tự chứa ký tự xuống dòng. Thông thường, các pattern sẽ được biểu diễn trong mã Python bằng ký hiệu chuỗi raw này.

Điều quan trọng cần lưu ý là hầu hết các thao tác biểu thức chính quy đều có sẵn dưới dạng các hàm cấp mô-đun và các phương thức trên
:ref:`biểu thức chính quy đã biên dịch <re-objects>`. Các hàm này là những lối tắt không yêu cầu bạn phải biên dịch một đối tượng regex trước, nhưng thiếu một số tham số tinh chỉnh.

.. seealso::

   Mô-đun :pypi:`regex` của bên thứ ba, có API tương thích với mô-đun :mod:`!re` trong thư viện chuẩn, nhưng cung cấp thêm chức năng và khả năng hỗ trợ Unicode toàn diện hơn.


.. _re-syntax:

Cú pháp biểu thức chính quy
---------------------------

Một biểu thức chính quy (hoặc RE) chỉ định một tập hợp các chuỗi khớp với nó; các hàm trong mô-đun này cho phép bạn kiểm tra xem một chuỗi cụ thể có khớp với một biểu thức chính quy cho trước hay không (hoặc một biểu thức chính quy cho trước có khớp với một chuỗi cụ thể hay không; về bản chất thì hai cách diễn đạt này giống nhau).

Các biểu thức chính quy có thể được nối với nhau để tạo thành các biểu thức chính quy mới; nếu *A* và *B* đều là các biểu thức chính quy, thì *AB* cũng là một biểu thức chính quy. Nói chung, nếu một chuỗi *p* khớp với *A* và một chuỗi khác *q* khớp với *B*, thì chuỗi *pq* sẽ khớp với AB. Điều này đúng trừ khi *A* hoặc *B* chứa các phép toán có độ ưu tiên thấp; có các điều kiện biên giữa *A* và *B*; hoặc có các tham chiếu nhóm được đánh số. Vì vậy, có thể dễ dàng xây dựng các biểu thức phức tạp từ những biểu thức nguyên thủy đơn giản hơn như các biểu thức được mô tả ở đây. Để biết chi tiết về lý thuyết và cách triển khai biểu thức chính quy, hãy tham khảo cuốn sách của Friedl [Frie09]_, hoặc gần như bất kỳ giáo trình nào về xây dựng trình biên dịch.

Sau đây là phần giải thích ngắn gọn về định dạng của các biểu thức chính quy. Để biết thêm thông tin và có phần trình bày dễ tiếp cận hơn, hãy tham khảo :ref:`regex-howto`.

Biểu thức chính quy có thể chứa cả ký tự đặc biệt và ký tự thông thường. Hầu hết các ký tự thông thường, như ``'A'``, ``'a'`` hoặc ``'0'``, đều là những biểu thức chính quy đơn giản nhất; chúng chỉ khớp với chính chúng. Bạn có thể nối các ký tự thông thường, vì vậy ``last`` khớp với chuỗi ``'last'``. (Trong phần còn lại của mục này, chúng ta sẽ viết các RE dưới dạng ``this special style``, thường không có dấu ngoặc kép, còn các chuỗi cần khớp dưới dạng ``'in single quotes'``.)

Một số ký tự, như ``'|'`` hoặc ``'('``, là ký tự đặc biệt. Ký tự đặc biệt biểu thị các lớp ký tự thông thường hoặc ảnh hưởng đến cách diễn giải các biểu thức chính quy xung quanh chúng.

Các toán tử lặp hoặc bộ định lượng (``*``, ``+``, ``?``, ``{m,n}``, v.v.) không thể được lồng trực tiếp. Điều này tránh sự mơ hồ với hậu tố bổ nghĩa không tham lam ``?`` và với các bộ bổ nghĩa khác trong những triển khai khác. Để áp dụng phép lặp thứ hai cho một phép lặp bên trong, có thể dùng dấu ngoặc đơn. Ví dụ, biểu thức ``(?:a{6})*`` khớp với mọi bội số của sáu ký tự ``'a'``.


Các ký tự đặc biệt gồm:

.. index:: single: . (dot); in regular expressions

``.``
   (Dấu chấm.)  Ở chế độ mặc định, ký tự này khớp với mọi ký tự ngoại trừ ký tự xuống dòng. Nếu cờ :const:`DOTALL` được chỉ định, ký tự này khớp với mọi ký tự, bao gồm cả ký tự xuống dòng. ``(?s:.)`` khớp với mọi ký tự bất kể cờ nào.

.. index:: single: ^ (caret); in regular expressions

``^``
   (Dấu mũ.)  Khớp với đầu chuỗi, và ở chế độ :const:`MULTILINE` cũng khớp ngay sau mỗi ký tự xuống dòng.

.. index:: single: $ (dollar); in regular expressions

``$``
   Khớp với cuối chuỗi hoặc ngay trước ký tự xuống dòng ở cuối chuỗi, và ở chế độ :const:`MULTILINE` cũng khớp trước một ký tự xuống dòng. ``foo`` khớp cả 'foo' và 'foobar', trong khi biểu thức chính quy ``foo$`` chỉ khớp 'foo'. Thú vị hơn, việc tìm ``foo.$`` trong ``'foo1\nfoo2\n'`` thường khớp với 'foo2', nhưng khớp với 'foo1' ở chế độ :const:`MULTILINE`; việc tìm một ``$`` đơn trong ``'foo\n'`` sẽ tìm thấy hai khớp (rỗng): một ngay trước ký tự xuống dòng và một ở cuối chuỗi.

.. index:: single: * (asterisk); in regular expressions

``*``
   Khiến RE kết quả khớp với 0 hoặc nhiều lần lặp của RE đứng trước, nhiều nhất có thể. ``ab*`` sẽ khớp với 'a', 'ab' hoặc 'a' theo sau bởi bất kỳ số lượng 'b' nào.

.. index:: single: + (plus); in regular expressions

``+``
   Khiến RE kết quả khớp với 1 hoặc nhiều lần lặp của RE đứng trước. ``ab+`` sẽ khớp với 'a' theo sau bởi một số lượng 'b' khác 0; nó sẽ không chỉ khớp với 'a'.

.. index:: single: ? (question mark); in regular expressions

``?``
   Khiến RE kết quả khớp với 0 hoặc 1 lần lặp của RE đứng trước. ``ab?`` sẽ khớp với 'a' hoặc 'ab'.

.. index::
   single: *?; in regular expressions
   single: +?; in regular expressions
   single: ??; in regular expressions

``*?``, ``+?``, ``??``
   Các quantifier ``'*'``, ``'+'`` và ``'?'`` đều là :dfn:`greedy`; chúng khớp với nhiều văn bản nhất có thể. Đôi khi hành vi này không được mong muốn; nếu RE ``<.*>`` được áp dụng cho ``'<a> b <c>'``, nó sẽ khớp với toàn bộ chuỗi chứ không chỉ ``'<a>'``. Thêm ``?`` sau quantifier khiến nó thực hiện việc khớp theo cách :dfn:`non-greedy` hoặc :dfn:`minimal`; sẽ khớp với số ký tự *few* nhất có thể. Sử dụng RE ``<.*?>`` sẽ chỉ khớp với ``'<a>'``.

.. index::
   single: *+; in regular expressions
   single: ++; in regular expressions
   single: ?+; in regular expressions

``*+``, ``++``, ``?+``
  Giống các quantifier ``'*'``, ``'+'`` và ``'?'``, những quantifier có ``'+'`` được thêm vào cũng khớp nhiều lần nhất có thể. Tuy nhiên, không giống các quantifier greedy thực sự, chúng không cho phép backtracking khi biểu thức theo sau không khớp. Chúng được gọi là các quantifier :dfn:`possessive`. Ví dụ, ``a*a`` sẽ khớp với ``'aaaa'`` vì ``a*`` sẽ khớp cả 4 ``'a'``\ s, nhưng khi gặp ``'a'`` cuối cùng, biểu thức sẽ được backtrack để cuối cùng ``a*`` khớp tổng cộng 3 ``'a'``\ s, còn ``'a'`` thứ tư được ``'a'`` cuối cùng khớp. Tuy nhiên, khi dùng ``a*+a`` để khớp với ``'aaaa'``, ``a*+`` sẽ khớp cả 4 ``'a'``, nhưng khi ``'a'`` cuối cùng không tìm thấy thêm ký tự nào để khớp, biểu thức không thể backtrack và do đó sẽ không khớp. ``x*+``, ``x++`` và ``x?+`` tương đương lần lượt với ``(?>x*)``, ``(?>x+)`` và ``(?>x?)``.

  .. versionadded:: 3.11

.. index::
   single: {} (curly brackets); in regular expressions

``{m}``
   Chỉ định rằng phải khớp chính xác *m* bản sao của RE trước đó; nếu khớp ít hơn thì toàn bộ RE sẽ không khớp. Ví dụ, ``a{6}`` sẽ khớp chính xác sáu ký tự ``'a'``, nhưng không khớp năm ký tự.

``{m,n}``
   Khiến RE kết quả khớp từ *m* đến *n* lần lặp của RE đứng trước, cố gắng khớp nhiều lần lặp nhất có thể. Ví dụ, ``a{3,5}`` sẽ khớp từ 3 đến 5 ký tự ``'a'``. Bỏ *m* sẽ chỉ định giới hạn dưới là 0, còn bỏ *n* sẽ chỉ định giới hạn trên là vô hạn. Ví dụ, ``a{4,}b`` sẽ khớp với ``'aaaab'`` hoặc một nghìn ký tự ``'a'`` theo sau bởi một ``'b'``, nhưng không khớp với ``'aaab'``. Không được bỏ dấu phẩy, nếu không modifier sẽ bị nhầm với dạng được mô tả trước đó.

``{m,n}?``
   Khiến RE kết quả khớp từ *m* đến *n* lần lặp của RE đứng trước, cố gắng khớp với số lần lặp *ít* nhất có thể. Đây là phiên bản không tham lam (non-greedy) của quantifier trước đó. Ví dụ, trên chuỗi gồm 6 ký tự ``'aaaaaa'``, ``a{3,5}`` sẽ khớp 5 ký tự ``'a'``, còn ``a{3,5}?`` chỉ khớp 3 ký tự.

``{m,n}+``
   Khiến RE kết quả khớp từ *m* đến *n* lần lặp của RE đứng trước, cố gắng khớp nhiều lần lặp nhất có thể *mà không* tạo ra bất kỳ điểm quay lui nào. Đây là phiên bản chiếm hữu (possessive) của quantifier ở trên. Ví dụ, trên chuỗi gồm 6 ký tự ``'aaaaaa'``, ``a{3,5}+aa`` sẽ cố gắng khớp 5 ký tự ``'a'``, sau đó, vì cần thêm 2 ``'a'``\ s, sẽ cần nhiều ký tự hơn số ký tự hiện có và do đó thất bại, trong khi ``a{3,5}aa`` sẽ khớp với ``a{3,5}`` bắt giữ 5, sau đó quay lui để khớp 4 ``'a'``\ s, rồi 2 ``'a'``\ s cuối cùng được khớp bởi ``aa`` cuối cùng trong mẫu. ``x{m,n}+`` tương đương với ``(?>x{m,n})``.

   .. versionadded:: 3.11

.. index:: single: \ (backslash); in regular expressions

``\``
   Hoặc dùng để thoát các ký tự đặc biệt (cho phép bạn khớp những ký tự như ``'*'``, ``'?'``, v.v.), hoặc báo hiệu một chuỗi đặc biệt; các chuỗi đặc biệt được thảo luận bên dưới.

   Nếu bạn không dùng chuỗi raw để biểu diễn mẫu, hãy nhớ rằng Python cũng sử dụng dấu gạch chéo ngược làm chuỗi escape trong các string literal; nếu chuỗi escape không được trình phân tích cú pháp của Python nhận diện, dấu gạch chéo ngược và ký tự tiếp theo sẽ được đưa vào chuỗi kết quả. Tuy nhiên, nếu Python nhận diện chuỗi kết quả, dấu gạch chéo ngược phải được lặp lại hai lần. Điều này phức tạp và khó hiểu, vì vậy bạn nên dùng chuỗi raw cho tất cả biểu thức, trừ những biểu thức đơn giản nhất.

.. index::
   single: [] (square brackets); in regular expressions

``[]``
   Dùng để chỉ một tập hợp các ký tự. Trong một tập hợp:

   * Các ký tự có thể được liệt kê riêng lẻ; ví dụ, ``[amk]`` sẽ khớp ``'a'``, ``'m'`` hoặc ``'k'``.

   .. index:: single: - (minus); in regular expressions

   * Có thể chỉ định các khoảng ký tự bằng cách đưa ra hai ký tự và phân tách chúng bằng ``'-'``; ví dụ, ``[a-z]`` sẽ khớp bất kỳ chữ cái ASCII viết thường nào, ``[0-5][0-9]`` sẽ khớp tất cả các số có hai chữ số từ ``00`` đến ``59``, còn ``[0-9A-Fa-f]`` sẽ khớp bất kỳ chữ số thập lục phân nào. Nếu ``-`` được escape (ví dụ: ``[a\-z]``) hoặc được đặt làm ký tự đầu tiên hay cuối cùng (ví dụ: ``[-a]`` hoặc ``[a-]``), nó sẽ khớp một ``'-'`` theo nghĩa đen.

   * Các ký tự đặc biệt, ngoại trừ dấu gạch chéo ngược, sẽ mất ý nghĩa đặc biệt bên trong các tập. Ví dụ: ``[(+*)]`` sẽ khớp với bất kỳ ký tự nguyên văn nào trong số ``'('``, ``'+'``, ``'*'`` hoặc ``')'``.

   .. index:: single: \ (backslash); in regular expressions

   * Dấu gạch chéo ngược либо dùng để escape các ký tự có ý nghĩa đặc biệt trong một tập, chẳng hạn như chính ``'-'``, ``']'``, ``'^'`` và ``'\\'``, либо báo hiệu một chuỗi đặc biệt biểu diễn một ký tự đơn, chẳng hạn như ``\xa0`` hoặc ``\n``, hoặc một lớp ký tự, chẳng hạn như ``\w`` hoặc ``\S`` (được định nghĩa bên dưới). Lưu ý rằng ``\b`` biểu diễn một ký tự "backspace" đơn, không phải ranh giới từ như khi ở bên ngoài một tập, và các escape số như ``\1`` luôn là escape bát phân, không phải tham chiếu nhóm. Các chuỗi đặc biệt không khớp với một ký tự đơn, chẳng hạn như ``\A`` và ``\z``, không được phép sử dụng.

   .. index:: single: ^ (caret); in regular expressions

   * Có thể khớp các ký tự không nằm trong một khoảng bằng cách :dfn:`lấy phần bù` của tập. Nếu ký tự đầu tiên của tập là ``'^'``, tất cả các ký tự *không* nằm trong tập sẽ được khớp. Ví dụ: ``[^5]`` sẽ khớp với mọi ký tự ngoại trừ ``'5'``, còn ``[^^]`` sẽ khớp với mọi ký tự ngoại trừ ``'^'``. ``^`` không có ý nghĩa đặc biệt nếu không phải là ký tự đầu tiên trong tập.

   * Để khớp một ``']'`` nguyên văn bên trong một tập, đặt trước nó một dấu gạch chéo ngược hoặc đặt nó ở đầu tập. Ví dụ, cả ``[()[\]{}]`` và ``[]()[{}]`` đều sẽ khớp với dấu ngoặc vuông phải, cũng như dấu ngoặc vuông trái, dấu ngoặc nhọn và dấu ngoặc tròn.

   .. .. index:: single: --; in regular expressions
   .. .. index:: single: &&; in regular expressions
   .. .. index:: single: ~~; in regular expressions
   .. .. index:: single: ||; in regular expressions

   * Hỗ trợ các tập lồng nhau và các phép toán trên tập như trong `Unicode Technical Standard #18 <Unicode Technical Standard #18_>`_ có thể được bổ sung trong tương lai. Điều này sẽ làm thay đổi cú pháp, vì vậy để tạo điều kiện cho thay đổi đó, hiện tại một :exc:`FutureWarning` sẽ được phát sinh trong các trường hợp mơ hồ. Điều đó bao gồm các tập bắt đầu bằng một ``'['`` nguyên văn hoặc chứa các chuỗi ký tự nguyên văn ``'--'``, ``'&&'``, ``'~~'`` và ``'||'``. Để tránh cảnh báo, hãy escape chúng bằng dấu gạch chéo ngược.

   .. _Unicode Technical Standard #18: https://unicode.org/reports/tr18/

   .. versionchanged:: 3.7
      :exc:`FutureWarning` is raised if a character set contains constructs
      điều đó sẽ thay đổi về mặt ngữ nghĩa trong tương lai.

.. index:: single: | (vertical bar); in regular expressions

``|``
   ``A|B``, trong đó *A* và *B* có thể là các RE bất kỳ, tạo ra một biểu thức chính quy khớp với either *A* hoặc *B*. Có thể phân tách một số lượng RE bất kỳ bằng ``'|'`` theo cách này. Cách này cũng có thể được sử dụng bên trong các nhóm (xem bên dưới). Khi chuỗi đích được quét, các RE được phân tách bằng ``'|'`` sẽ được thử từ trái sang phải. Khi một mẫu khớp hoàn toàn, nhánh đó được chấp nhận. Điều này có nghĩa là một khi *A* khớp, *B* sẽ không được kiểm tra thêm, ngay cả khi nó tạo ra kết quả khớp tổng thể dài hơn. Nói cách khác, toán tử ``'|'`` không bao giờ là greedy. Để khớp một ``'|'`` nguyên văn, hãy sử dụng ``\|`` hoặc đặt nó bên trong một lớp ký tự, như trong ``[|]``.

.. index::
   single: () (parentheses); in regular expressions

``(...)``
   Khớp với bất kỳ biểu thức chính quy nào nằm bên trong dấu ngoặc đơn, đồng thời biểu thị điểm bắt đầu và kết thúc của một nhóm; nội dung của một nhóm có thể được lấy ra sau khi thực hiện khớp, và có thể được khớp lại ở vị trí sau đó trong chuỗi bằng chuỗi đặc biệt ``\number``, được mô tả bên dưới. Để khớp các ký tự nguyên văn ``'('`` hoặc ``')'``, hãy sử dụng ``\(`` hoặc ``\)``, hoặc đặt chúng bên trong một character class: ``[(]``, ``[)]``.

.. index:: single: (?; in regular expressions

``(?...)``
   Đây là ký hiệu mở rộng (một ``'?'`` theo sau ``'('`` vốn không có ý nghĩa). Ký tự đầu tiên sau ``'?'`` xác định ý nghĩa và cú pháp tiếp theo của cấu trúc này. Các phần mở rộng thường không tạo một nhóm mới; ``(?P<name>...)`` là ngoại lệ duy nhất của quy tắc này. Sau đây là các phần mở rộng hiện được hỗ trợ.

``(?aiLmsux)``
   (Một hoặc nhiều chữ cái thuộc tập ``'a'``, ``'i'``, ``'L'``, ``'m'``, ``'s'``, ``'u'``, ``'x'``.) Nhóm này khớp với chuỗi rỗng; các chữ cái thiết lập những cờ tương ứng cho toàn bộ biểu thức chính quy:

   * :const:`re.A` (khớp chỉ ASCII)
   * :const:`re.I` (bỏ qua chữ hoa chữ thường)
   * :const:`re.L` (phụ thuộc vào locale)
   * :const:`re.M` (nhiều dòng)
   * :const:`re.S` (dấu chấm khớp với mọi ký tự)
   * :const:`re.U` (khớp Unicode)
   * :const:`re.X` (verbose)

   (Các cờ được mô tả trong :ref:`contents-of-module-re`.) Điều này hữu ích nếu bạn muốn đưa các cờ vào một phần của biểu thức chính quy, thay vì truyền một đối số *flag* cho
   :func:`re.compile` hàm. Các cờ nên được sử dụng ở đầu chuỗi biểu thức.

   .. versionchanged:: 3.11
      Cấu trúc này chỉ có thể được sử dụng ở đầu biểu thức.

.. index:: single: (?:; in regular expressions

``(?:...)``
   Một phiên bản không bắt giữ của dấu ngoặc đơn trong biểu thức chính quy. Khớp với bất kỳ biểu thức chính quy nào nằm bên trong dấu ngoặc đơn, nhưng chuỗi con được khớp bởi nhóm *không thể* được truy xuất sau khi thực hiện khớp hoặc được tham chiếu ở phần sau của mẫu.

``(?aiLmsux-imsx:...)``
   (Không hoặc nhiều chữ cái thuộc tập ``'a'``, ``'i'``, ``'L'``, ``'m'``, ``'s'``, ``'u'``, ``'x'``, tùy chọn theo sau bởi ``'-'`` rồi đến một hoặc nhiều chữ cái thuộc tập ``'i'``, ``'m'``, ``'s'``, ``'x'``.) Các chữ cái sẽ thiết lập hoặc xóa các cờ tương ứng cho phần biểu thức:

   * :const:`re.A` (khớp chỉ ASCII)
   * :const:`re.I` (bỏ qua chữ hoa chữ thường)
   * :const:`re.L` (phụ thuộc vào locale)
   * :const:`re.M` (nhiều dòng)
   * :const:`re.S` (dấu chấm khớp với mọi ký tự)
   * :const:`re.U` (khớp Unicode)
   * :const:`re.X` (verbose)

   (Các cờ được mô tả trong :ref:`contents-of-module-re`.)

   Các chữ cái ``'a'``, ``'L'`` và ``'u'`` loại trừ lẫn nhau khi được dùng làm cờ inline, vì vậy chúng không thể được kết hợp hoặc đi sau ``'-'``. Thay vào đó, khi một trong số chúng xuất hiện trong một nhóm inline, nó sẽ ghi đè chế độ khớp trong nhóm bao quanh. Trong các mẫu Unicode, ``(?a:...)`` chuyển sang chế độ khớp chỉ ASCII, còn ``(?u:...)`` chuyển sang chế độ khớp Unicode (mặc định). Trong các mẫu bytes, ``(?L:...)`` chuyển sang chế độ khớp phụ thuộc locale, còn ``(?a:...)`` chuyển sang chế độ khớp chỉ ASCII (mặc định). Việc ghi đè này chỉ có hiệu lực trong nhóm inline giới hạn đó, và chế độ khớp ban đầu được khôi phục bên ngoài nhóm.

   .. versionadded:: 3.6

   .. versionchanged:: 3.7
      Các chữ cái ``'a'``, ``'L'`` và ``'u'`` cũng có thể được sử dụng trong một nhóm.

``(?>...)``
   Cố gắng khớp ``...`` như thể đó là một biểu thức chính quy riêng biệt; nếu thành công, nó tiếp tục khớp phần còn lại của mẫu theo sau nó. Nếu mẫu tiếp theo không khớp, ngăn xếp chỉ có thể được quay lui đến một điểm *trước* ``(?>...)``, vì sau khi thoát, biểu thức được gọi là :dfn:`nhóm atomic` đã loại bỏ mọi điểm trên ngăn xếp bên trong nó. Do đó, ``(?>.*).`` sẽ không bao giờ khớp được gì, vì trước tiên ``.*`` sẽ khớp mọi ký tự có thể, sau đó, do không còn gì để khớp, ``.`` cuối cùng sẽ không khớp. Vì không có điểm nào được lưu trên ngăn xếp trong Nhóm Atomic và cũng không có điểm nào trước nó, toàn bộ biểu thức sẽ không khớp.

   .. versionadded:: 3.11

.. index:: single: (?P<; in regular expressions

``(?P<name>...)``
   Tương tự như dấu ngoặc đơn thông thường, nhưng chuỗi con được nhóm khớp có thể được truy cập thông qua tên nhóm ký hiệu *name*. Tên nhóm phải là các định danh Python hợp lệ, và trong các mẫu :class:`bytes`, chúng chỉ có thể chứa các byte trong phạm vi ASCII. Mỗi tên nhóm chỉ được định nghĩa một lần trong một biểu thức chính quy. Một nhóm ký hiệu cũng là một nhóm được đánh số, giống như khi nhóm đó không được đặt tên.

   Các nhóm có tên có thể được tham chiếu trong ba ngữ cảnh. Nếu mẫu là ``(?P<quote>['"]).*?(?P=quote)`` (tức là khớp với một chuỗi được đặt trong dấu nháy đơn hoặc dấu nháy kép):

   +----------------------------------------------------------------+----------------------------------+
   | Ngữ cảnh tham chiếu đến nhóm "quote"                           | Các cách tham chiếu đến nhóm này |
   +================================================================+==================================+
   | trong chính pattern đó                                         | * ``(?P=quote)`` (như minh họa)  |
   |                                                                | * ``\1``                         |
   +----------------------------------------------------------------+----------------------------------+
   | khi xử lý đối tượng match *m*                                  | * ``m.group('quote')``           |
   |                                                                | * ``m.end('quote')`` (v.v.)      |
   +----------------------------------------------------------------+----------------------------------+
   | trong một chuỗi được truyền vào đối số *repl* của ``re.sub()`` | * ``\g<quote>``                  |
   |                                                                | * ``\g<1>``                      |
   |                                                                | * ``\1``                         |
   +----------------------------------------------------------------+----------------------------------+

   .. versionchanged:: 3.12
      Trong các mẫu :class:`bytes`, nhóm *name* chỉ có thể chứa các byte trong phạm vi ASCII (``b'\x00'``-``b'\x7f'``).

.. index:: single: (?P=; in regular expressions

``(?P=name)``
   Một tham chiếu ngược đến một nhóm có tên; nó khớp với bất kỳ văn bản nào đã được khớp bởi nhóm trước đó có tên *name*.

.. index:: single: (?#; in regular expressions

``(?#...)``
   Một chú thích; nội dung bên trong dấu ngoặc đơn đơn giản là bị bỏ qua.

.. index:: single: (?=; in regular expressions

``(?=...)``
   Khớp nếu ``...`` khớp ở vị trí tiếp theo, nhưng không tiêu thụ bất kỳ phần nào của chuỗi. Đây được gọi là :dfn:`lookahead assertion`. Ví dụ, ``Isaac (?=Asimov)`` sẽ khớp với ``'Isaac '`` chỉ khi theo sau nó là ``'Asimov'``.

.. index:: single: (?!; in regular expressions

``(?!...)``
   Khớp nếu ``...`` không khớp ở vị trí tiếp theo. Đây là một :dfn:`negative lookahead assertion`. Ví dụ, ``Isaac (?!Asimov)`` sẽ khớp với ``'Isaac '`` chỉ khi nó *không* được theo sau bởi ``'Asimov'``.

.. index:: single: (?<=; in regular expressions

``(?<=...)``
   Khớp nếu vị trí hiện tại trong chuỗi đứng sau một kết quả khớp với ``...`` kết thúc tại vị trí hiện tại. Đây được gọi là :dfn:`positive lookbehind assertion`. ``(?<=abc)def`` sẽ tìm thấy kết quả khớp trong ``'abcdef'``, vì lookbehind sẽ lùi lại 3 ký tự và kiểm tra xem mẫu bên trong có khớp hay không. Mẫu bên trong chỉ được khớp với các chuỗi có một độ dài cố định nào đó, nghĩa là ``abc`` hoặc ``a|b`` được phép, nhưng ``a*`` và ``a{3,4}`` thì không. Lưu ý rằng các mẫu bắt đầu bằng positive lookbehind assertion sẽ không khớp ở đầu chuỗi được tìm kiếm; nhiều khả năng bạn sẽ muốn sử dụng
   hàm :func:`search` thay vì hàm :func:`match`:

      >>> import re
      >>> m = re.search('(?<=abc)def', 'abcdef')
      >>> m.group(0)
      'def'

   Ví dụ này tìm một từ đứng sau dấu gạch nối:

      >>> m = re.search(r'(?<=-)\w+', 'spam-egg')
      >>> m.group(0)
      'egg'

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ tham chiếu nhóm có độ dài cố định.

.. index:: single: (?<!; in regular expressions

``(?<!...)``
   Khớp nếu vị trí hiện tại trong chuỗi không đứng trước một kết quả khớp với ``...``. Đây được gọi là :dfn:`khẳng định lookbehind phủ định`. Tương tự như các khẳng định lookbehind dương, mẫu được chứa chỉ được khớp với các chuỗi có độ dài cố định nào đó. Các mẫu bắt đầu bằng khẳng định lookbehind phủ định có thể khớp ở đầu chuỗi đang được tìm kiếm.

.. _re-conditional-expression:
.. index:: single: (?(; in regular expressions

``(?(id/name)yes-pattern|no-pattern)``
   Sẽ thử khớp với ``yes-pattern`` nếu nhóm có *id* hoặc *name* đã cho tồn tại, và với ``no-pattern`` nếu nhóm đó không tồn tại. ``no-pattern`` là tùy chọn và có thể được bỏ qua. Ví dụ, ``(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)`` là một mẫu khớp email kém, khớp với cả ``'<user@host.com>'`` và ``'user@host.com'``, nhưng không khớp toàn bộ ``'<user@host.com'`` cũng như ``'user@host.com>'`` (:func:`re.search` chỉ tìm thấy ``'user@host.com'`` trong chuỗi đầu tiên).

   .. versionchanged:: 3.12
      Nhóm *id* chỉ có thể chứa các chữ số ASCII. Trong các mẫu :class:`bytes`, nhóm *name* chỉ có thể chứa các byte trong dải ASCII (``b'\x00'``-``b'\x7f'``).


.. _re-special-sequences:

Các chuỗi đặc biệt bao gồm ``'\'`` và một ký tự trong danh sách bên dưới. Nếu ký tự thông thường không phải là chữ số ASCII hoặc chữ cái ASCII, thì RE kết quả sẽ khớp với ký tự thứ hai. Ví dụ, ``\$`` khớp với ký tự ``'$'``.

.. index:: single: \ (backslash); in regular expressions

``\number``
   Khớp với nội dung của nhóm có cùng số. Các nhóm được đánh số bắt đầu từ 1. Ví dụ, ``(.+) \1`` khớp với ``'the the'`` hoặc ``'55 55'``, nhưng không khớp với ``'thethe'`` (lưu ý khoảng trắng sau nhóm). Chuỗi đặc biệt này chỉ có thể được dùng để khớp một trong 99 nhóm đầu tiên. Nếu chữ số đầu tiên của *number* là 0, hoặc *number* dài 3 chữ số bát phân, thì nó sẽ không được diễn giải là một kết quả khớp nhóm mà là ký tự có giá trị bát phân *number*. Bên trong ``'['`` và ``']'`` của một character class, tất cả escape số đều được xử lý như các ký tự.

.. index:: single: \A; in regular expressions

``\A``
   Chỉ khớp ở đầu chuỗi.

.. index:: single: \b; in regular expressions

``\b``
   Khớp với chuỗi rỗng, nhưng chỉ ở đầu hoặc cuối một từ. Một từ được định nghĩa là một chuỗi các ký tự từ. Lưu ý rằng về mặt hình thức, ``\b`` được định nghĩa là ranh giới giữa một ký tự ``\w`` và một ký tự ``\W`` (hoặc ngược lại), hoặc giữa ``\w`` và đầu hoặc cuối chuỗi. Điều này có nghĩa là ``r'\bat\b'`` khớp với ``'at'``, ``'at.'``, ``'(at)'`` và ``'as at ay'``, nhưng không khớp với ``'attempt'`` hoặc ``'atlas'``.

   Các ký tự từ mặc định trong các pattern Unicode (str) là các ký tự chữ và số Unicode cùng với dấu gạch dưới, nhưng có thể thay đổi bằng cách sử dụng cờ :py:const:`~re.ASCII`. Ranh giới từ được xác định theo locale hiện tại nếu sử dụng cờ :py:const:`~re.LOCALE`.

   .. note::

      Bên trong một phạm vi ký tự, ``\b`` biểu diễn ký tự backspace, để tương thích với string literal của Python.

.. index:: single: \B; in regular expressions

``\B``
   Khớp với chuỗi rỗng, nhưng chỉ khi nó *not* ở đầu hoặc cuối một từ. Điều này có nghĩa là ``r'at\B'`` khớp với ``'athens'``, ``'atom'``, ``'attorney'``, nhưng không khớp với ``'at'``, ``'at.'`` hoặc ``'at!'``. ``\B`` ngược lại với ``\b``, vì vậy các ký tự từ trong các pattern Unicode (str) là các ký tự chữ và số Unicode hoặc dấu gạch dưới, mặc dù có thể thay đổi điều này bằng cách sử dụng cờ :py:const:`~re.ASCII`. Ranh giới từ được xác định theo locale hiện tại nếu sử dụng cờ :py:const:`~re.LOCALE`.

   .. versionchanged:: 3.14
      ``\B`` hiện khớp với chuỗi đầu vào rỗng.

.. index:: single: \d; in regular expressions

``\d``
   Đối với các pattern Unicode (str):
      Khớp với mọi chữ số thập phân Unicode (tức là mọi ký tự thuộc danh mục ký tự Unicode `[Nd]`__). Danh mục này bao gồm ``[0-9]`` và nhiều ký tự chữ số khác.

      Khớp với ``[0-9]`` nếu sử dụng cờ :py:const:`~re.ASCII`.

      __ https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#G134153

   Đối với các mẫu 8-bit (bytes):
      Khớp với mọi chữ số thập phân trong bộ ký tự ASCII; tương đương với ``[0-9]``.

.. index:: single: \D; in regular expressions

``\D``
   Khớp với mọi ký tự không phải là chữ số thập phân. Đây là ngược lại với ``\d``.

   Khớp với ``[^0-9]`` nếu sử dụng cờ :py:const:`~re.ASCII`.

.. index:: single: \s; in regular expressions

``\s``
   Đối với các pattern Unicode (str):
      Khớp với các ký tự khoảng trắng Unicode (như được định nghĩa bởi :py:meth:`str.isspace`). Bao gồm ``[ \t\n\r\f\v]`` và nhiều ký tự khác, chẳng hạn như các khoảng trắng không ngắt dòng được yêu cầu bởi các quy tắc kiểu chữ trong nhiều ngôn ngữ.

      Khớp với ``[ \t\n\r\f\v]`` nếu sử dụng cờ :py:const:`~re.ASCII`.

   Đối với các mẫu 8-bit (bytes):
      Khớp với các ký tự được xem là khoảng trắng trong bộ ký tự ASCII; tương đương với ``[ \t\n\r\f\v]``.

.. index:: single: \S; in regular expressions

``\S``
   Khớp với mọi ký tự không phải là ký tự khoảng trắng. Đây là giá trị ngược lại của ``\s``.

   Khớp với ``[^ \t\n\r\f\v]`` nếu sử dụng cờ :py:const:`~re.ASCII`.

.. index:: single: \w; in regular expressions

``\w``
   Đối với các pattern Unicode (str):
      Khớp với các ký tự từ Unicode; bao gồm tất cả các ký tự chữ và số Unicode (như được định nghĩa bởi :py:meth:`str.isalnum`), cũng như dấu gạch dưới (``_``).

      Khớp với ``[a-zA-Z0-9_]`` nếu sử dụng cờ :py:const:`~re.ASCII`.

   Đối với các mẫu 8-bit (bytes):
      Khớp với các ký tự được xem là chữ và số trong bộ ký tự ASCII; tương đương với ``[a-zA-Z0-9_]``. Nếu sử dụng cờ :py:const:`~re.LOCALE`, khớp với các ký tự được xem là chữ và số trong locale hiện tại và dấu gạch dưới.

.. index:: single: \W; in regular expressions

``\W``
   Khớp với mọi ký tự không phải là ký tự từ. Đây là phần đối lập của ``\w``. Theo mặc định, khớp với các ký tự không phải dấu gạch dưới (``_``) mà :py:meth:`str.isalnum` trả về ``False``.

   Khớp với ``[^a-zA-Z0-9_]`` nếu sử dụng cờ :py:const:`~re.ASCII`.

   Nếu sử dụng cờ :py:const:`~re.LOCALE`, khớp với các ký tự không phải là chữ và số trong locale hiện tại cũng không phải dấu gạch dưới.

.. index:: single: \z; in regular expressions
           single: \Z; in regular expressions

``\z``
   Chỉ khớp ở cuối chuỗi.

   .. versionadded:: 3.14

``\Z``
   Giống với ``\z``. Để tương thích với các phiên bản Python cũ.

.. index::
   single: \a; in regular expressions
   single: \b; in regular expressions
   single: \f; in regular expressions
   single: \n; in regular expressions
   single: \N; in regular expressions
   single: \r; in regular expressions
   single: \t; in regular expressions
   single: \u; in regular expressions
   single: \U; in regular expressions
   single: \v; in regular expressions
   single: \x; in regular expressions
   single: \\; in regular expressions

Hầu hết các :ref:`chuỗi thoát <escape-sequences>` được hỗ trợ bởi các string literal của Python cũng được bộ phân tích cú pháp biểu thức chính quy chấp nhận::

   \a      \b      \f      \n
   \N      \r      \t      \u
   \U      \v      \x      \\

(Lưu ý rằng ``\b`` được dùng để biểu diễn ranh giới từ và chỉ có nghĩa là "backspace" bên trong các character class.)

Các chuỗi thoát ``'\u'``, ``'\U'`` và ``'\N'`` chỉ được nhận dạng trong các pattern Unicode (str). Trong các pattern bytes, chúng gây ra lỗi. Các chuỗi thoát không xác định của các chữ cái ASCII được dành cho mục đích sử dụng trong tương lai và được xem là lỗi.

Các chuỗi thoát bát phân được hỗ trợ ở dạng giới hạn. Nếu chữ số đầu tiên là 0 hoặc có ba chữ số bát phân thì chuỗi này được coi là chuỗi thoát bát phân. Nếu không, nó là tham chiếu nhóm. Tương tự như string literal, chuỗi thoát bát phân luôn có độ dài tối đa là ba chữ số.

.. versionchanged:: 3.3
   Các chuỗi thoát ``'\u'`` và ``'\U'`` đã được thêm vào.

.. versionchanged:: 3.6
   Các escape không xác định bao gồm ``'\'`` và một chữ cái ASCII giờ đây sẽ gây ra lỗi.

.. versionchanged:: 3.8
   Chuỗi escape :samp:`'\\N\\{{name}\\}'` đã được thêm vào. Tương tự như trong các string literal, nó mở rộng thành ký tự Unicode có tên (ví dụ: ``'\N{EM DASH}'``).


.. _contents-of-module-re:

Nội dung module
---------------

Module này định nghĩa một số hàm, hằng số và một ngoại lệ. Một số hàm là các phiên bản đơn giản hóa của những phương thức đầy đủ tính năng dành cho regular expression đã biên dịch. Hầu hết các ứng dụng không tầm thường luôn sử dụng dạng đã biên dịch.


.. _`Flags`:

Flags
^^^^^

.. versionchanged:: 3.6
   Các hằng số flag giờ đây là các instance của :class:`RegexFlag`, vốn là một lớp con của
   :class:`enum.IntFlag`.


.. class:: RegexFlag

   Một lớp :class:`enum.IntFlag` chứa các tùy chọn regex được liệt kê bên dưới.

   .. versionadded:: 3.11 - được thêm vào ``__all__``

.. data:: A
          ASCII

   Khiến ``\w``, ``\W``, ``\b``, ``\B``, ``\d``, ``\D``, ``\s`` và ``\S`` thực hiện việc so khớp chỉ ASCII thay vì so khớp Unicode đầy đủ. Điều này chỉ có ý nghĩa đối với các pattern Unicode (str) và bị bỏ qua đối với các pattern bytes.

   Tương ứng với inline flag ``(?a)``.

   .. note::

      Flag :py:const:`~re.U` vẫn tồn tại để tương thích ngược, nhưng là dư thừa trong Python 3 vì việc so khớp mặc định là Unicode đối với các pattern ``str``, và không cho phép so khớp Unicode đối với các pattern bytes.
      :py:const:`~re.UNICODE` và inline flag ``(?u)`` cũng tương tự là dư thừa.


.. data:: DEBUG

   Hiển thị thông tin gỡ lỗi về biểu thức đã biên dịch.

   Không có cờ inline tương ứng.


.. data:: I
          IGNORECASE

   Thực hiện đối sánh không phân biệt chữ hoa chữ thường; các biểu thức như ``[A-Z]`` cũng sẽ đối sánh với các chữ cái viết thường. Đối sánh Unicode đầy đủ (chẳng hạn ``Ü`` đối sánh với ``ü``) cũng hoạt động, trừ khi sử dụng cờ :py:const:`~re.ASCII` để tắt việc đối sánh các ký tự không phải ASCII. Locale hiện tại không làm thay đổi tác dụng của cờ này, trừ khi cờ :py:const:`~re.LOCALE` cũng được sử dụng.

   Tương ứng với cờ inline ``(?i)``.

   Lưu ý rằng khi sử dụng các mẫu Unicode ``[a-z]`` hoặc ``[A-Z]`` kết hợp với cờ :const:`IGNORECASE`, chúng sẽ đối sánh với 52 chữ cái ASCII và 4 chữ cái không phải ASCII bổ sung: 'İ' (U+0130, chữ I hoa Latin có dấu chấm bên trên), 'ı' (U+0131, chữ i thường Latin không có dấu chấm), 'ſ' (U+017F, chữ s dài Latin) và 'K' (U+212A, ký hiệu Kelvin). Nếu sử dụng cờ :py:const:`~re.ASCII`, chỉ các chữ cái từ 'a' đến 'z' và từ 'A' đến 'Z' được đối sánh.

.. data:: L
          LOCALE

   Làm cho ``\w``, ``\W``, ``\b``, ``\B`` và việc đối sánh không phân biệt chữ hoa chữ thường phụ thuộc vào locale hiện tại. Chỉ có thể sử dụng cờ này với các mẫu bytes.

   Tương ứng với cờ inline ``(?L)``.

   .. warning::

      Không khuyến khích sử dụng cờ này; thay vào đó, hãy cân nhắc việc so khớp Unicode. Cơ chế locale rất không đáng tin cậy vì chỉ xử lý một "culture" tại một thời điểm và chỉ hoạt động với các locale 8-bit. So khớp Unicode được bật theo mặc định cho các mẫu Unicode (str) và có thể xử lý nhiều locale và ngôn ngữ khác nhau.

   .. versionchanged:: 3.6
      :py:const:`~re.LOCALE` can be used only with bytes patterns
      và không tương thích với :py:const:`~re.ASCII`.

   .. versionchanged:: 3.7
      Các đối tượng biểu thức chính quy đã biên dịch có cờ :py:const:`~re.LOCALE` không còn phụ thuộc vào locale tại thời điểm biên dịch. Chỉ locale tại thời điểm so khớp mới ảnh hưởng đến kết quả so khớp.


.. data:: M
          MULTILINE

   Khi được chỉ định, ký tự mẫu ``'^'`` khớp ở đầu chuỗi và ở đầu mỗi dòng (ngay sau mỗi ký tự xuống dòng); còn ký tự mẫu ``'$'`` khớp ở cuối chuỗi và ở cuối mỗi dòng (ngay trước mỗi ký tự xuống dòng). Theo mặc định, ``'^'`` chỉ khớp ở đầu chuỗi, còn ``'$'`` chỉ khớp ở cuối chuỗi và ngay trước ký tự xuống dòng (nếu có) ở cuối chuỗi.

   Tương ứng với cờ inline ``(?m)``.

.. data:: NOFLAG

   Cho biết không có cờ nào được áp dụng, giá trị là ``0``. Cờ này có thể được dùng làm giá trị mặc định cho một đối số từ khóa của hàm hoặc làm giá trị cơ sở sẽ được OR có điều kiện với các cờ khác. Ví dụ sử dụng làm giá trị mặc định::

      def myfunc(text, flag=re.NOFLAG):
          return re.match(text, flag)

   .. versionadded:: 3.11

.. data:: S
          DOTALL

   Khiến ký tự đặc biệt ``'.'`` khớp với mọi ký tự, bao gồm cả ký tự xuống dòng; nếu không có cờ này, ``'.'`` sẽ khớp với mọi thứ *ngoại trừ* ký tự xuống dòng.

   Tương ứng với cờ inline ``(?s)``.


.. data:: U
          UNICODE

   Trong Python 3, các ký tự Unicode được khớp theo mặc định đối với các mẫu ``str``. Vì vậy, cờ này là dư thừa với **không có tác dụng** và chỉ được giữ lại để tương thích ngược.

   Xem :py:const:`~re.ASCII` để giới hạn việc khớp chỉ ở các ký tự ASCII.

.. data:: X
          VERBOSE

   .. index:: single: # (hash); in regular expressions

   Cờ này cho phép bạn viết các biểu thức chính quy trông đẹp mắt và dễ đọc hơn bằng cách cho phép bạn phân tách trực quan các phần logic của mẫu và thêm chú thích. Khoảng trắng trong mẫu sẽ bị bỏ qua, ngoại trừ khi nằm trong một character class, khi đứng trước một dấu gạch chéo ngược chưa được escape, hoặc khi nằm trong các token như ``*?``, ``(?:`` hay ``(?P<...>``. Ví dụ: ``(? :`` và ``* ?`` không được phép. Khi một dòng chứa ``#`` không nằm trong một character class và không đứng trước một dấu gạch chéo ngược chưa được escape, tất cả ký tự từ ``#`` ngoài cùng bên trái như vậy cho đến cuối dòng sẽ bị bỏ qua.

   Điều này có nghĩa là hai đối tượng biểu thức chính quy sau đây, dùng để khớp một số thập phân, về mặt chức năng là tương đương::

      a = re.compile(r"""\d +  # the integral part
                         \.    # dấu thập phân
                         \d *  # một vài chữ số phần thập phân""", re.X)
      b = re.compile(r"\d+\.\d*")

   Tương ứng với cờ inline ``(?x)``.


Các hàm
^^^^^^^

.. function:: compile(pattern, flags=0)

   Biên dịch một mẫu biểu thức chính quy thành :ref:`đối tượng biểu thức chính quy <re-objects>`, có thể được dùng để so khớp bằng cách sử dụng nó
   :func:`~Pattern.match`, :func:`~Pattern.search` và các phương thức khác được mô tả bên dưới.

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).

   Chuỗi lệnh::

      prog = re.compile(pattern)
      result = prog.match(string)

   tương đương với::

      result = re.match(pattern, string)

   nhưng việc sử dụng :func:`re.compile` và lưu đối tượng biểu thức chính quy thu được để tái sử dụng sẽ hiệu quả hơn khi biểu thức được sử dụng nhiều lần trong cùng một chương trình.

   .. note::

      Các phiên bản đã biên dịch của những mẫu gần đây nhất được truyền cho
      :func:`re.compile` và các hàm matching ở cấp module được lưu vào bộ nhớ đệm, vì vậy các chương trình chỉ sử dụng một vài regular expression tại một thời điểm không cần lo lắng về việc biên dịch regular expression.


.. function:: search(pattern, string, flags=0)

   Quét qua *string* để tìm vị trí đầu tiên mà regular expression *pattern* tạo ra một kết quả khớp, rồi trả về một :class:`~re.Match` tương ứng. Trả về ``None`` nếu không có vị trí nào trong chuỗi khớp với pattern; lưu ý rằng điều này khác với việc tìm thấy một kết quả khớp có độ dài bằng 0 tại một vị trí nào đó trong chuỗi.

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).


.. function:: match(pattern, string, flags=0)

   Nếu không hoặc có một hay nhiều ký tự ở đầu *string* khớp với regular expression *pattern*, hãy trả về một :class:`~re.Match` tương ứng. Trả về ``None`` nếu chuỗi không khớp với pattern; lưu ý rằng điều này khác với một kết quả khớp có độ dài bằng 0.

   Lưu ý rằng ngay cả trong chế độ :const:`MULTILINE`, :func:`re.match` chỉ khớp ở đầu chuỗi, không phải ở đầu mỗi dòng.

   Nếu bạn muốn tìm một kết quả khớp ở bất kỳ vị trí nào trong *string*, hãy sử dụng :func:`search` thay vào đó (xem thêm :ref:`search-vs-match`).

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).


.. function:: fullmatch(pattern, string, flags=0)

   Nếu toàn bộ *string* khớp với biểu thức chính quy *pattern*, hãy trả về một :class:`~re.Match` tương ứng. Trả về ``None`` nếu chuỗi không khớp với mẫu; lưu ý rằng điều này khác với kết quả khớp có độ dài bằng không.

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).

   .. versionadded:: 3.4


.. function:: split(pattern, string, maxsplit=0, flags=0)

   Tách *string* tại các vị trí xuất hiện của *pattern*. Nếu sử dụng các dấu ngoặc bắt giữ trong *pattern*, thì văn bản của tất cả các nhóm trong mẫu cũng được trả về như một phần của danh sách kết quả. Nếu *maxsplit* khác không, sẽ xảy ra nhiều nhất *maxsplit* lần tách, và phần còn lại của chuỗi được trả về dưới dạng phần tử cuối cùng của danh sách.::

      >>> re.split(r'\W+', 'Words, words, words.')
      ['Words', 'words', 'words', '']
      >>> re.split(r'(\W+)', 'Words, words, words.')
      ['Words', ', ', 'words', ', ', 'words', '.', '']
      >>> re.split(r'\W+', 'Words, words, words.', maxsplit=1)
      ['Words', 'words, words.']
      >>> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
      ['0', '3', '9']

   Nếu dấu phân cách có các nhóm bắt giữ và khớp ở đầu chuỗi, kết quả sẽ bắt đầu bằng một chuỗi rỗng. Điều tương tự cũng đúng với cuối chuỗi.::

      >>> re.split(r'(\W+)', '...words, words...')
      ['', '...', 'words', ', ', 'words', '...', '']

   Nhờ đó, các thành phần dấu phân cách luôn được tìm thấy tại cùng các chỉ mục tương đối trong danh sách kết quả.

   Không thể có các kết quả khớp rỗng liền kề, nhưng một kết quả khớp rỗng có thể xuất hiện ngay sau một kết quả khớp không rỗng.

   .. code:: pycon

      >>> re.split(r'\b', 'Words, words, words.')
      ['', 'Words', ', ', 'words', ', ', 'words', '.']
      >>> re.split(r'\W*', '...words...')
      ['', '', 'w', 'o', 'r', 'd', 's', '', '']
      >>> re.split(r'(\W*)', '...words...')
      ['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).

   .. versionchanged:: 3.1
      Đã thêm đối số flags tùy chọn.

   .. versionchanged:: 3.7
      Đã thêm hỗ trợ tách theo một pattern có thể khớp với chuỗi rỗng.

   .. deprecated:: 3.13
      Việc truyền *maxsplit* và *flags* dưới dạng đối số vị trí không còn được khuyến nghị. Trong các phiên bản Python tương lai, chúng sẽ là
      :ref:`các tham số chỉ dùng từ khóa <keyword-only_parameter>`.


.. function:: findall(pattern, string, flags=0)

   Trả về tất cả các kết quả khớp không chồng lấp của *pattern* trong *string*, dưới dạng danh sách các chuỗi hoặc tuple. *string* được quét từ trái sang phải và các kết quả khớp được trả về theo thứ tự tìm thấy. Các kết quả khớp rỗng cũng được đưa vào kết quả.

   Kết quả phụ thuộc vào số lượng nhóm capturing trong pattern. Nếu không có nhóm nào, trả về danh sách các chuỗi khớp với toàn bộ pattern. Nếu có đúng một nhóm, trả về danh sách các chuỗi khớp với nhóm đó. Nếu có nhiều nhóm, trả về danh sách các tuple gồm các chuỗi khớp với các nhóm. Các nhóm non-capturing không ảnh hưởng đến dạng của kết quả.

      >>> re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
      ['foot', 'fell', 'fastest']
      >>> re.findall(r'(\w+)=(\d+)', 'set width=20 and height=10')
      [('width', '20'), ('height', '10')]

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).

   .. versionchanged:: 3.7
      Các kết quả khớp không rỗng giờ đây có thể bắt đầu ngay sau một kết quả khớp rỗng trước đó.


.. function:: finditer(pattern, string, flags=0)

   Trả về một :term:`iterator` tạo ra các đối tượng :class:`~re.Match` cho tất cả các kết quả khớp không chồng lấp của mẫu RE *pattern* trong *string*. *string* được quét từ trái sang phải và các kết quả khớp được trả về theo thứ tự tìm thấy. Các kết quả khớp rỗng được đưa vào kết quả.

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).

   .. versionchanged:: 3.7
      Các kết quả khớp không rỗng giờ đây có thể bắt đầu ngay sau một kết quả khớp rỗng trước đó.


.. function:: sub(pattern, repl, string, count=0, flags=0)

   Trả về chuỗi thu được bằng cách thay thế các lần xuất hiện không chồng lấp ở ngoài cùng bên trái của *pattern* trong *string* bằng chuỗi thay thế *repl*. Nếu không tìm thấy mẫu, *string* được trả về nguyên trạng. *repl* có thể là một chuỗi hoặc một hàm; nếu là chuỗi, mọi escape bằng dấu gạch chéo ngược trong đó sẽ được xử lý. Cụ thể, ``\n`` được chuyển thành một ký tự xuống dòng, ``\r`` được chuyển thành ký tự xuống dòng kiểu carriage return, v.v. Các escape không xác định của các chữ cái ASCII được dành cho mục đích sử dụng trong tương lai và được xử lý như lỗi. Các escape không xác định khác, chẳng hạn như ``\&``, được giữ nguyên. Các backreference, chẳng hạn như ``\6``, được thay thế bằng chuỗi con khớp với group 6 trong mẫu. Ví dụ::

      >>> re.sub(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(\s*\):',
      ...        r'static PyObject*\npy_\1(void)\n{',
      ...        'def myfunc():')
      'static PyObject*\npy_myfunc(void)\n{'

   Nếu *repl* là một hàm, hàm này được gọi cho mỗi lần xuất hiện không chồng lấp của *pattern*. Hàm nhận một đối số :class:`~re.Match` duy nhất và trả về chuỗi thay thế. Ví dụ::

      >>> def dashrepl(matchobj):
      ...     if matchobj.group(0) == '-': return ' '
      ...     else: return '-'
      ...
      >>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
      'pro--gram files'
      >>> re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)
      'Baked Beans & Spam'

   Mẫu có thể là một chuỗi hoặc một :class:`~re.Pattern`.

   Đối số tùy chọn *count* là số lần xuất hiện tối đa của mẫu sẽ được thay thế; *count* phải là một số nguyên không âm. Nếu bị bỏ qua hoặc bằng không, tất cả các lần xuất hiện sẽ được thay thế.

   Không thể có các kết quả khớp rỗng liền kề, nhưng một kết quả khớp rỗng có thể xuất hiện ngay sau một kết quả khớp không rỗng. Do đó, ``sub('x*', '-', 'abxd')`` trả về ``'-a-b--d-'`` thay vì ``'-a-b-d-'``.

   .. index:: single: \g; in regular expressions

   Trong các đối số *repl* dạng chuỗi, ngoài các escape ký tự và backreference được mô tả ở trên, ``\g<name>`` sẽ sử dụng chuỗi con được khớp bởi nhóm có tên ``name``, được định nghĩa bằng cú pháp ``(?P<name>...)``. ``\g<number>`` sử dụng số nhóm tương ứng; vì vậy ``\g<2>`` tương đương với ``\2``, nhưng không gây nhầm lẫn trong một chuỗi thay thế như ``\g<2>0``. ``\20`` sẽ được hiểu là tham chiếu đến nhóm 20, không phải tham chiếu đến nhóm 2 theo sau bởi ký tự chữ ``'0'``. Backreference ``\g<0>`` thay thế bằng toàn bộ chuỗi con được RE khớp.

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).

   .. versionchanged:: 3.1
      Đã thêm đối số flags tùy chọn.

   .. versionchanged:: 3.5
      Các nhóm không khớp được thay thế bằng chuỗi rỗng.

   .. versionchanged:: 3.6
      Các escape không xác định trong *pattern* bao gồm ``'\'`` và một chữ cái ASCII hiện sẽ gây ra lỗi.

   .. versionchanged:: 3.7
      Các escape không xác định trong *repl* gồm ``'\'`` và một chữ cái ASCII hiện được xem là lỗi. Một kết quả khớp rỗng có thể xuất hiện ngay sau một kết quả khớp không rỗng.

   .. versionchanged:: 3.12
      Nhóm *id* chỉ có thể chứa các chữ số ASCII. Trong chuỗi thay thế :class:`bytes`, nhóm *name* chỉ có thể chứa các byte trong phạm vi ASCII (``b'\x00'``-``b'\x7f'``).

   .. deprecated:: 3.13
      Việc truyền *count* và *flags* dưới dạng đối số vị trí đã bị loại bỏ dần. Trong các phiên bản Python tương lai, chúng sẽ
      :ref:`các tham số chỉ dùng từ khóa <keyword-only_parameter>`.


.. function:: subn(pattern, repl, string, count=0, flags=0)

   Thực hiện cùng thao tác như :func:`sub`, nhưng trả về một tuple ``(new_string, number_of_subs_made)``.

   Hành vi của biểu thức có thể được thay đổi bằng cách chỉ định giá trị *flags*. Các giá trị có thể là bất kỳ biến nào trong số `flags`_, được kết hợp bằng phép OR theo bit (toán tử ``|``).


.. function:: escape(pattern)

   Escape các ký tự đặc biệt trong *pattern*. Điều này hữu ích nếu bạn muốn khớp một chuỗi ký tự literal tùy ý có thể chứa các siêu ký tự của regular expression. Ví dụ::

      >>> print(re.escape('https://www.python.org'))
      https://www\.python\.org

      >>> legal_chars = string.ascii_lowercase + string.digits + "!#$%&'*+-.^_`|~:"
      >>> print('[%s]+' % re.escape(legal_chars))
      [abcdefghijklmnopqrstuvwxyz0123456789!\#\$%\&'\*\+\-\.\^_`\|\~:]+

      >>> operators = ['+', '-', '*', '/', '**']
      >>> print('|'.join(map(re.escape, sorted(operators, reverse=True))))
      /|\-|\+|\*\*|\*

   Không được sử dụng hàm này cho chuỗi thay thế trong :func:`sub` và :func:`subn`; chỉ escape dấu gạch chéo ngược. Ví dụ::

      >>> digits_re = r'\d+'
      >>> sample = '/usr/sbin/sendmail - 0 errors, 12 warnings'
      >>> print(re.sub(digits_re, digits_re.replace('\\', r'\\'), sample))
      /usr/sbin/sendmail - \d+ errors, \d+ warnings

   .. versionchanged:: 3.3
      Ký tự ``'_'`` không còn được escape nữa.

   .. versionchanged:: 3.7
      Chỉ những ký tự có thể mang ý nghĩa đặc biệt trong biểu thức chính quy mới được escape. Do đó, ``'!'``, ``'"'``, ``'%'``, ``"'"``, ``','``, ``'/'``, ``':'``, ``';'``, ``'<'``, ``'='``, ``'>'``, ``'@'`` và ``"`"`` không còn được escape nữa.


.. function:: purge()

   Xóa bộ nhớ đệm biểu thức chính quy.


Ngoại lệ
^^^^^^^^

.. exception:: PatternError(msg, pattern=None, pos=None)

   Ngoại lệ được phát sinh khi một chuỗi được truyền vào một trong các hàm ở đây không phải là biểu thức chính quy hợp lệ (ví dụ: chuỗi có thể chứa các dấu ngoặc không khớp) hoặc khi xảy ra lỗi khác trong quá trình biên dịch hay đối sánh. Chuỗi không khớp với mẫu không bao giờ là lỗi. Đối tượng ``PatternError`` có thêm các thuộc tính sau:

   .. attribute:: msg

      Thông báo lỗi chưa được định dạng.

   .. attribute:: pattern

      Mẫu biểu thức chính quy.

   .. attribute:: pos

      Chỉ mục trong *pattern* tại đó quá trình biên dịch không thành công (có thể là ``None``).

   .. attribute:: lineno

      Dòng tương ứng với *pos* (có thể là ``None``).

   .. attribute:: colno

      Cột tương ứng với *pos* (có thể là ``None``).

   .. versionchanged:: 3.5
      Đã thêm các thuộc tính bổ sung.

   .. versionchanged:: 3.13
      ``PatternError`` ban đầu có tên là ``error``; tên sau được giữ lại làm bí danh để đảm bảo khả năng tương thích ngược.

.. _re-objects:

Đối tượng Regular Expression
----------------------------

.. class:: Pattern

   Đối tượng regular expression đã biên dịch được trả về bởi :func:`re.compile`.

   Các pattern là :ref:`generic <generics>` theo kiểu chuỗi mà chúng xử lý (:class:`str` hoặc :class:`bytes`).

   .. versionchanged:: 3.9
      :py:class:`re.Pattern` supports ``[]`` to indicate a Unicode (str) or bytes pattern.
      Xem :ref:`types-genericalias`.

.. method:: Pattern.search(string[, pos[, endpos]])

   Quét qua *string* để tìm vị trí đầu tiên mà regular expression này tạo ra một kết quả khớp, rồi trả về :class:`~re.Match` tương ứng. Trả về ``None`` nếu không có vị trí nào trong chuỗi khớp với pattern; lưu ý rằng điều này khác với việc tìm thấy một kết quả khớp có độ dài bằng không tại một điểm nào đó trong chuỗi.

   Tham số thứ hai tùy chọn *pos* cung cấp một chỉ mục trong chuỗi, tại đó bắt đầu tìm kiếm; giá trị mặc định là ``0``. Điều này không hoàn toàn tương đương với việc cắt chuỗi; ký tự pattern ``'^'`` khớp ở đầu thực của chuỗi và tại các vị trí ngay sau ký tự xuống dòng, nhưng không nhất thiết khớp tại chỉ mục nơi bắt đầu tìm kiếm.

   Tham số tùy chọn *endpos* giới hạn phạm vi tìm kiếm trong chuỗi; chuỗi sẽ được coi như có độ dài *endpos* ký tự, vì vậy chỉ các ký tự từ *pos* đến ``endpos - 1`` mới được tìm kiếm để tìm kết quả khớp. Nếu *endpos* nhỏ hơn *pos*, sẽ không tìm thấy kết quả khớp; nếu không, khi *rx* là một đối tượng regular expression đã biên dịch, ``rx.search(string, 0, 50)`` tương đương với ``rx.search(string[:50], 0)``.::

      >>> pattern = re.compile("d")
      >>> pattern.search("dog")     # Khớp tại chỉ mục 0
      <re.Match object; span=(0, 1), match='d'>
      >>> pattern.search("dog", 1)  # Không khớp; tìm kiếm không bao gồm "d"


.. method:: Pattern.match(string[, pos[, endpos]])

   Nếu không hoặc nhiều ký tự ở *đầu* của *chuỗi* khớp với biểu thức chính quy này, trả về một :class:`~re.Match` tương ứng. Trả về ``None`` nếu chuỗi không khớp với mẫu; lưu ý rằng điều này khác với một kết quả khớp có độ dài bằng không.

   Các tham số tùy chọn *pos* và *endpos* có ý nghĩa giống như đối với
   :meth:`~Pattern.search` method.::

      >>> pattern = re.compile("o")
      >>> pattern.match("dog")      # Không khớp vì "o" không nằm ở đầu "dog".
      >>> pattern.match("dog", 1)   # Khớp vì "o" là ký tự thứ 2 của "dog".
      <re.Match object; span=(1, 2), match='o'>

   Nếu bạn muốn tìm một kết quả khớp ở bất kỳ vị trí nào trong *string*, hãy sử dụng
   :meth:`~Pattern.search` thay vào đó (xem thêm :ref:`search-vs-match`).


.. method:: Pattern.fullmatch(string[, pos[, endpos]])

   Nếu toàn bộ *string* khớp với biểu thức chính quy này, hãy trả về một
   :class:`~re.Match` tương ứng. Trả về ``None`` nếu chuỗi không khớp với mẫu; lưu ý rằng điều này khác với một kết quả khớp có độ dài bằng không.

   Các tham số tùy chọn *pos* và *endpos* có ý nghĩa giống như đối với
   :meth:`~Pattern.search` method.::

      >>> pattern = re.compile("o[gh]")
      >>> pattern.fullmatch("dog")      # Không khớp vì "o" không nằm ở đầu "dog".
      >>> pattern.fullmatch("ogre")     # Không khớp vì toàn bộ chuỗi không khớp.
      >>> pattern.fullmatch("doggie", 1, 3)   # Khớp trong các giới hạn đã cho.
      <re.Match object; span=(1, 3), match='og'>

   .. versionadded:: 3.4


.. method:: Pattern.split(string, maxsplit=0)

   Giống hệt hàm :func:`split`, sử dụng mẫu đã biên dịch.


.. method:: Pattern.findall(string[, pos[, endpos]])

   Tương tự hàm :func:`findall`, sử dụng mẫu đã biên dịch, nhưng cũng chấp nhận các tham số tùy chọn *pos* và *endpos*, giới hạn vùng tìm kiếm tương tự như đối với :meth:`search`.


.. method:: Pattern.finditer(string[, pos[, endpos]])

   Tương tự hàm :func:`finditer`, sử dụng mẫu đã biên dịch, nhưng cũng chấp nhận các tham số tùy chọn *pos* và *endpos*, giới hạn vùng tìm kiếm tương tự như đối với :meth:`search`.


.. method:: Pattern.sub(repl, string, count=0)

   Giống hệt hàm :func:`sub`, sử dụng mẫu đã biên dịch.


.. method:: Pattern.subn(repl, string, count=0)

   Giống hệt hàm :func:`subn`, sử dụng mẫu đã biên dịch.


.. attribute:: Pattern.flags

   Các cờ so khớp regex. Đây là sự kết hợp của các cờ được truyền vào
   :func:`.compile`, mọi cờ inline ``(?...)`` trong pattern và các cờ ngầm định như :py:const:`~re.UNICODE` nếu pattern là một chuỗi Unicode.


.. attribute:: Pattern.groups

   Số lượng nhóm capturing trong pattern.


.. attribute:: Pattern.groupindex

   Một dictionary ánh xạ mọi tên nhóm mang tính biểu tượng được định nghĩa bởi ``(?P<id>)`` đến số nhóm. Dictionary này rỗng nếu không sử dụng nhóm mang tính biểu tượng nào trong pattern.


.. attribute:: Pattern.pattern

   Chuỗi pattern từ đó đối tượng pattern được biên dịch.


.. versionchanged:: 3.7
   Đã bổ sung hỗ trợ cho :func:`copy.copy` và :func:`copy.deepcopy`. Các đối tượng regular expression đã biên dịch được xem là atomic.


.. _match-objects:

Đối tượng Match
---------------

Các đối tượng Match luôn có giá trị boolean là ``True``. Vì :meth:`~Pattern.match` và :meth:`~Pattern.search` trả về ``None`` khi không có kết quả khớp, bạn có thể kiểm tra xem có kết quả khớp hay không bằng một câu lệnh ``if`` đơn giản::

   match = re.search(pattern, string)
   if match:
       process(match)

.. class:: Match

   Đối tượng Match được trả về bởi các ``match``\ es và ``search``\ es thành công.

   Các kết quả khớp mang tính :ref:`generic <generics>` đối với kiểu chuỗi được khớp (:class:`str` hoặc :class:`bytes`).

   .. versionchanged:: 3.9
      :py:class:`re.Match` supports ``[]`` to indicate a Unicode (str) or bytes match.
      Xem :ref:`types-genericalias`.

.. method:: Match.expand(template)

   Trả về chuỗi thu được bằng cách thực hiện phép thay thế dấu gạch chéo ngược trên chuỗi mẫu *template*, như được thực hiện bởi phương thức :meth:`~Pattern.sub`. Các escape như ``\n`` được chuyển đổi thành những ký tự tương ứng, còn các backreference dạng số (``\1``, ``\2``) và backreference được đặt tên (``\g<1>``, ``\g<name>``) được thay thế bằng nội dung của nhóm tương ứng. Backreference ``\g<0>`` sẽ được thay thế bằng toàn bộ kết quả khớp.

   .. versionchanged:: 3.5
      Các nhóm không khớp được thay thế bằng một chuỗi rỗng.

.. method:: Match.group([group1, ...])

   Trả về một hoặc nhiều nhóm con của kết quả khớp. Nếu chỉ có một đối số, kết quả là một chuỗi đơn; nếu có nhiều đối số, kết quả là một tuple với một phần tử cho mỗi đối số. Khi không có đối số, *group1* mặc định là zero (toàn bộ kết quả khớp được trả về). Nếu đối số *groupN* là zero, giá trị trả về tương ứng là toàn bộ chuỗi khớp; nếu là một số nguyên dương, đó là chuỗi khớp với nhóm được đặt trong ngoặc tương ứng. Nếu số nhóm là số âm hoặc lớn hơn số nhóm được định nghĩa trong pattern, một
   Ngoại lệ :exc:`IndexError` được phát sinh. Nếu một group nằm trong phần của pattern không khớp, kết quả tương ứng là ``None``. Nếu một group nằm trong phần của pattern khớp nhiều lần, kết quả khớp cuối cùng sẽ được trả về.::

      >>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
      >>> m.group(0)       # Toàn bộ kết quả khớp
      'Isaac Newton'
      >>> m.group(1)       # Nhóm con được đặt trong cặp ngoặc đầu tiên.
      'Isaac'
      >>> m.group(2)       # Nhóm con được đặt trong cặp ngoặc thứ hai.
      'Newton'
      >>> m.group(1, 2)    # Nhiều đối số sẽ tạo thành một tuple.
      ('Isaac', 'Newton')

   Nếu regular expression sử dụng cú pháp ``(?P<name>...)``, các đối số *groupN* cũng có thể là các chuỗi xác định group bằng tên của group đó. Nếu một đối số chuỗi không được dùng làm tên group trong pattern, ngoại lệ :exc:`IndexError` sẽ được phát sinh.

   Một ví dụ khá phức tạp::

      >>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
      >>> m.group('first_name')
      'Malcolm'
      >>> m.group('last_name')
      'Reynolds'

   Các nhóm được đặt tên cũng có thể được tham chiếu bằng chỉ mục của chúng::

      >>> m.group(1)
      'Malcolm'
      >>> m.group(2)
      'Reynolds'

   Nếu một nhóm khớp nhiều lần, chỉ có kết quả khớp cuối cùng có thể được truy cập::

      >>> m = re.match(r"(..)+", "a1b2c3")  # Khớp 3 lần.
      >>> m.group(1)                        # Chỉ trả về kết quả khớp cuối cùng.
      'c3'


.. method:: Match.__getitem__(g)

   Điều này giống hệt ``m.group(g)``. Điều này giúp truy cập một nhóm riêng lẻ từ một kết quả khớp dễ dàng hơn::

      >>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
      >>> m[0]       # Toàn bộ kết quả khớp
      'Isaac Newton'
      >>> m[1]       # Nhóm con được đặt trong cặp ngoặc đầu tiên.
      'Isaac'
      >>> m[2]       # Nhóm con được đặt trong cặp ngoặc thứ hai.
      'Newton'

   Các nhóm được đặt tên cũng được hỗ trợ::

      >>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Isaac Newton")
      >>> m['first_name']
      'Isaac'
      >>> m['last_name']
      'Newton'

   .. versionadded:: 3.6


.. method:: Match.groups(default=None)

   Trả về một tuple chứa tất cả các nhóm con của kết quả khớp, từ 1 đến số lượng nhóm có trong pattern. Đối số *default* được dùng cho các nhóm không tham gia vào kết quả khớp; giá trị mặc định là ``None``.

   Ví dụ::

      >>> m = re.match(r"(\d+)\.(\d+)", "24.1632")
      >>> m.groups()
      ('24', '1632')

   Nếu chúng ta đặt phần thập phân và mọi thứ sau đó là tùy chọn, có thể không phải tất cả các nhóm đều tham gia vào kết quả khớp. Các nhóm này sẽ mặc định là ``None`` trừ khi cung cấp đối số *default*::

      >>> m = re.match(r"(\d+)\.?(\d+)?", "24")
      >>> m.groups()      # Nhóm thứ hai mặc định là None.
      ('24', None)
      >>> m.groups('0')   # Bây giờ, nhóm thứ hai mặc định là '0'.
      ('24', '0')


.. method:: Match.groupdict(default=None)

   Trả về một dictionary chứa tất cả các nhóm con *có tên* của kết quả khớp, với khóa là tên nhóm con. Đối số *mặc định* được dùng cho các nhóm không tham gia vào kết quả khớp; đối số này mặc định là ``None``. Ví dụ::

      >>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
      >>> m.groupdict()
      {'first_name': 'Malcolm', 'last_name': 'Reynolds'}


.. method:: Match.start([group])
            Match.end([group])

   Trả về các chỉ số của vị trí bắt đầu và kết thúc của chuỗi con được khớp bởi *nhóm*; *nhóm* mặc định là số không (nghĩa là toàn bộ chuỗi con được khớp). Trả về ``-1`` nếu *nhóm* tồn tại nhưng không đóng góp vào kết quả khớp. Với đối tượng kết quả khớp *m* và một nhóm *g* đã đóng góp vào kết quả khớp, chuỗi con được khớp bởi nhóm *g* (tương đương với ``m.group(g)``) là::

      m.string[m.start(g):m.end(g)]

   Lưu ý rằng ``m.start(group)`` sẽ bằng ``m.end(group)`` nếu *nhóm* khớp một chuỗi rỗng. Ví dụ, sau ``m = re.search('b(c?)', 'cba')`` , ``m.start(0)`` là 1, ``m.end(0)`` là 2, ``m.start(1)`` và ``m.end(1)`` đều là 2, và ``m.start(2)`` phát sinh một ngoại lệ :exc:`IndexError`.

   Một ví dụ sẽ loại bỏ *remove_this* khỏi các địa chỉ email::

      >>> email = "tony@tiremove_thisger.net"
      >>> m = re.search("remove_this", email)
      >>> email[:m.start()] + email[m.end():]
      'tony@tiger.net'


.. method:: Match.span([group])

   Với một match *m*, trả về tuple 2 phần tử ``(m.start(group), m.end(group))``. Lưu ý rằng nếu group *group* không đóng góp vào kết quả khớp thì giá trị này là ``(-1, -1)``. group *group* mặc định là zero, tức toàn bộ kết quả khớp.


.. attribute:: Match.pos

   Giá trị của *pos* được truyền vào :meth:`~Pattern.search` hoặc
   Phương thức :meth:`~Pattern.match` của một :ref:`đối tượng regex <re-objects>`. Đây là chỉ mục trong chuỗi tại đó công cụ RE bắt đầu tìm kiếm kết quả khớp.


.. attribute:: Match.endpos

   Giá trị của *endpos* được truyền cho :meth:`~Pattern.search` hoặc
   phương thức :meth:`~Pattern.match` của một :ref:`đối tượng regex <re-objects>`. Đây là chỉ mục trong chuỗi mà sau đó công cụ RE sẽ không tiếp tục.


.. attribute:: Match.lastindex

   Chỉ mục số nguyên của nhóm bắt giữ khớp cuối cùng, hoặc ``None`` nếu hoàn toàn không có nhóm nào khớp. Ví dụ, các biểu thức ``(a)b``, ``((a)(b))`` và ``((ab))`` sẽ có giá trị ``lastindex == 1`` nếu được áp dụng cho chuỗi ``'ab'``, trong khi biểu thức ``(a)(b)`` sẽ có giá trị ``lastindex == 2`` nếu được áp dụng cho cùng chuỗi đó.


.. attribute:: Match.lastgroup

   Tên của nhóm bắt giữ khớp cuối cùng, hoặc ``None`` nếu nhóm đó không có tên hoặc hoàn toàn không có nhóm nào khớp.


.. attribute:: Match.re

   :ref:`Đối tượng biểu thức chính quy <re-objects>` mà phương thức :meth:`~Pattern.match` hoặc
   phương thức :meth:`~Pattern.search` đã tạo ra thực thể khớp này.


.. attribute:: Match.string

   Chuỗi được truyền vào :meth:`~Pattern.match` hoặc :meth:`~Pattern.search`.


.. versionchanged:: 3.7
   Đã bổ sung hỗ trợ cho :func:`copy.copy` và :func:`copy.deepcopy`. Các đối tượng match được xem là nguyên tử.


.. _re-examples:

Ví dụ về Regular Expression
---------------------------


Kiểm tra một đôi
^^^^^^^^^^^^^^^^

Trong ví dụ này, chúng ta sẽ sử dụng hàm trợ giúp sau để hiển thị các đối tượng match dễ đọc hơn một chút::

   def displaymatch(match):
       if match is None:
           return None
       return '<Match: %r, groups=%r>' % (match.group(), match.groups())

Giả sử bạn đang viết một chương trình poker, trong đó bài trên tay của người chơi được biểu diễn bằng một chuỗi gồm 5 ký tự, mỗi ký tự đại diện cho một lá bài: "a" là ace, "k" là king, "q" là queen, "j" là jack, "t" là 10, còn "2" đến "9" đại diện cho lá bài có giá trị tương ứng.

Để kiểm tra xem một chuỗi đã cho có phải là một bộ bài hợp lệ hay không, bạn có thể làm như sau::

   >>> valid = re.compile(r"^[a2-9tjqk]{5}$")
   >>> displaymatch(valid.match("akt5q"))  # Hợp lệ.
   "<Match: 'akt5q', groups=()>"
   >>> displaymatch(valid.match("akt5e"))  # Không hợp lệ.
   >>> displaymatch(valid.match("akt"))    # Không hợp lệ.
   >>> displaymatch(valid.match("727ak"))  # Hợp lệ.
   "<Match: '727ak', groups=()>"

Bộ bài cuối cùng đó, ``"727ak"``, có một đôi, tức là hai lá bài có cùng giá trị. Để khớp mẫu này bằng biểu thức chính quy, ta có thể sử dụng backreference như sau::

   >>> pair = re.compile(r".*(.).*\1")
   >>> displaymatch(pair.match("717ak"))     # Đôi 7.
   "<Match: '717', groups=('7',)>"
   >>> displaymatch(pair.match("718ak"))     # Không có đôi.
   >>> displaymatch(pair.match("354aa"))     # Đôi Át.
   "<Match: '354aa', groups=('a',)>"

Để tìm ra đôi bài gồm những lá nào, có thể sử dụng
:meth:`~Match.group` của đối tượng match theo cách sau::

   >>> pair = re.compile(r".*(.).*\1")
   >>> pair.match("717ak").group(1)
   '7'

   # Error because re.match() returns None, which doesn't have a group() method:
   >>> pair.match("718ak").group(1)
   Traceback (most recent call last):
     File "<pyshell#23>", line 1, in <module>
       re.match(r".*(.).*\1", "718ak").group(1)
   AttributeError: 'NoneType' object has no attribute 'group'

   >>> pair.match("354aa").group(1)
   'a'


Mô phỏng scanf()
^^^^^^^^^^^^^^^^

.. index:: single: scanf (C function)

Python hiện chưa có tương đương với :c:func:`!scanf`. Biểu thức chính quy thường mạnh hơn, dù cũng dài dòng hơn,
các chuỗi định dạng :c:func:`!scanf`. Bảng dưới đây cung cấp một số ánh xạ tương đương tương đối giữa các token định dạng :c:func:`!scanf` và biểu thức chính quy.

+--------------------------------+---------------------------------------------+
| Token :c:func:`!scanf`         | Biểu thức chính quy                         |
+================================+=============================================+
| ``%c``                         | ``.``                                       |
+--------------------------------+---------------------------------------------+
| ``%5c``                        | ``.{5}``                                    |
+--------------------------------+---------------------------------------------+
| ``%d``                         | ``[-+]?\d+``                                |
+--------------------------------+---------------------------------------------+
| ``%e``, ``%E``, ``%f``, ``%g`` | ``[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?`` |
+--------------------------------+---------------------------------------------+
| ``%i``                         | ``[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)``     |
+--------------------------------+---------------------------------------------+
| ``%o``                         | ``[-+]?[0-7]+``                             |
+--------------------------------+---------------------------------------------+
| ``%s``                         | ``\S+``                                     |
+--------------------------------+---------------------------------------------+
| ``%u``                         | ``\d+``                                     |
+--------------------------------+---------------------------------------------+
| ``%x``, ``%X``                 | ``[-+]?(0[xX])?[\dA-Fa-f]+``                |
+--------------------------------+---------------------------------------------+

Để trích xuất tên tệp và các số từ một chuỗi như::

   /usr/sbin/sendmail - 0 errors, 4 warnings

bạn sẽ sử dụng định dạng :c:func:`!scanf` như sau::

   %s - %d errors, %d warnings

Biểu thức chính quy tương đương sẽ là::

   (\S+) - (\d+) errors, (\d+) warnings


.. _search-vs-match:

search() so với match()
^^^^^^^^^^^^^^^^^^^^^^^

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

Python cung cấp các thao tác nguyên thủy khác nhau dựa trên biểu thức chính quy:

+ :func:`re.match` chỉ kiểm tra kết quả khớp ở đầu chuỗi
+ :func:`re.search` kiểm tra xem có khớp ở bất kỳ vị trí nào trong chuỗi (đây là cách Perl hoạt động theo mặc định)
+ :func:`re.fullmatch` kiểm tra xem toàn bộ chuỗi có khớp hay không


Ví dụ::

   >>> re.match("c", "abcdef")    # Không khớp
   >>> re.search("c", "abcdef")   # Khớp
   <re.Match object; span=(2, 3), match='c'>
   >>> re.fullmatch("p.*n", "python") # Khớp
   <re.Match object; span=(0, 6), match='python'>
   >>> re.fullmatch("r.*n", "python") # Không khớp

Các biểu thức chính quy bắt đầu bằng ``'^'`` có thể được sử dụng với :func:`search` để giới hạn kết quả khớp ở đầu chuỗi::

   >>> re.match("c", "abcdef")    # Không khớp
   >>> re.search("^c", "abcdef")  # Không khớp
   >>> re.search("^a", "abcdef")  # Khớp
   <re.Match object; span=(0, 1), match='a'>

Tuy nhiên, lưu ý rằng ở chế độ :const:`MULTILINE`, :func:`match` chỉ khớp ở đầu chuỗi, trong khi việc sử dụng :func:`search` với một biểu thức chính quy bắt đầu bằng ``'^'`` sẽ khớp ở đầu mỗi dòng.::

   >>> re.match("X", "A\nB\nX", re.MULTILINE)  # Không khớp
   >>> re.search("^X", "A\nB\nX", re.MULTILINE)  # Khớp
   <re.Match object; span=(4, 5), match='X'>


Tạo danh bạ điện thoại
^^^^^^^^^^^^^^^^^^^^^^

:func:`split` tách một chuỗi thành một danh sách, được phân cách theo mẫu đã truyền vào. Phương thức này vô cùng hữu ích để chuyển đổi dữ liệu dạng văn bản thành các cấu trúc dữ liệu mà Python có thể dễ dàng đọc và sửa đổi, như được minh họa trong ví dụ sau đây để tạo một danh bạ điện thoại.

Trước tiên, đây là dữ liệu đầu vào. Thông thường, dữ liệu có thể đến từ một tệp; ở đây, chúng ta sử dụng cú pháp chuỗi ba dấu nháy

.. doctest::

   >>> text = """Ross McFluff: 834.345.1254 155 Elm Street
   ...
   ... Ronald Heathmore: 892.345.3428 436 Finley Avenue
   ... Frank Burger: 925.541.7625 662 South Dogwood Way
   ...
   ...
   ... Heather Albrecht: 548.326.4584 919 Park Place"""

Các mục được phân tách bằng một hoặc nhiều ký tự xuống dòng. Bây giờ, chúng ta chuyển chuỗi thành một danh sách, trong đó mỗi dòng không rỗng có một mục riêng:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> entries = re.split("\n+", text)
   >>> entries
   ['Ross McFluff: 834.345.1254 155 Elm Street',
   'Ronald Heathmore: 892.345.3428 436 Finley Avenue',
   'Frank Burger: 925.541.7625 662 South Dogwood Way',
   'Heather Albrecht: 548.326.4584 919 Park Place']

Cuối cùng, hãy tách mỗi mục thành một danh sách gồm tên, họ, số điện thoại và địa chỉ. Chúng ta sử dụng tham số ``maxsplit`` của :func:`split` vì địa chỉ có chứa khoảng trắng, tức là mẫu tách của chúng ta:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> [re.split(":? ", entry, maxsplit=3) for entry in entries]
   [['Ross', 'McFluff', '834.345.1254', '155 Elm Street'],
   ['Ronald', 'Heathmore', '892.345.3428', '436 Finley Avenue'],
   ['Frank', 'Burger', '925.541.7625', '662 South Dogwood Way'],
   ['Heather', 'Albrecht', '548.326.4584', '919 Park Place']]

Mẫu ``:?`` khớp với dấu hai chấm sau họ, để dấu này không xuất hiện trong danh sách kết quả. Với ``maxsplit`` là ``4``, chúng ta có thể tách số nhà khỏi tên đường:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> [re.split(":? ", entry, maxsplit=4) for entry in entries]
   [['Ross', 'McFluff', '834.345.1254', '155', 'Elm Street'],
   ['Ronald', 'Heathmore', '892.345.3428', '436', 'Finley Avenue'],
   ['Frank', 'Burger', '925.541.7625', '662', 'South Dogwood Way'],
   ['Heather', 'Albrecht', '548.326.4584', '919', 'Park Place']]


Xử lý văn bản
^^^^^^^^^^^^^

:func:`sub` thay thế mọi lần xuất hiện của một mẫu bằng một chuỗi hoặc kết quả của một hàm. Ví dụ này minh họa cách sử dụng :func:`sub` với một hàm để “xáo trộn” văn bản, tức là ngẫu nhiên hóa thứ tự của tất cả các ký tự trong mỗi từ của một câu, ngoại trừ ký tự đầu tiên và cuối cùng::

   >>> def repl(m):
   ...     inner_word = list(m.group(2))
   ...     random.shuffle(inner_word)
   ...     return m.group(1) + "".join(inner_word) + m.group(3)
   ...
   >>> text = "Professor Abdolmalek, please report your absences promptly."
   >>> re.sub(r"(\w)(\w+)(\w)", repl, text)
   'Poefsrosr Aealmlobdk, pslaee reorpt your abnseces plmrptoy.'
   >>> re.sub(r"(\w)(\w+)(\w)", repl, text)
   'Pofsroser Aodlambelk, plasee reoprt yuor asnebces potlmrpy.'


Tìm tất cả trạng từ
^^^^^^^^^^^^^^^^^^^

:func:`findall` khớp với *tất cả* lần xuất hiện của một mẫu, chứ không chỉ lần đầu tiên như :func:`search`. Ví dụ: nếu một tác giả muốn tìm tất cả trạng từ trong một đoạn văn bản, họ có thể sử dụng :func:`findall` theo cách sau::

   >>> text = "He was carefully disguised but captured quickly by police."
   >>> re.findall(r"\w+ly\b", text)
   ['carefully', 'quickly']


Tìm tất cả trạng từ và vị trí của chúng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu muốn biết nhiều thông tin hơn về tất cả các kết quả khớp của một mẫu ngoài phần văn bản được khớp, :func:`finditer` rất hữu ích vì nó cung cấp các đối tượng :class:`~re.Match` thay vì các chuỗi. Tiếp tục với ví dụ trước, nếu một tác giả muốn tìm tất cả trạng từ *và vị trí của chúng* trong một đoạn văn bản, họ sẽ sử dụng
:func:`finditer` theo cách sau::

   >>> text = "He was carefully disguised but captured quickly by police."
   >>> for m in re.finditer(r"\w+ly\b", text):
   ...     print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
   07-16: carefully
   40-47: quickly


Ký hiệu chuỗi thô
^^^^^^^^^^^^^^^^^

Ký hiệu chuỗi thô (``r"text"``) giúp các biểu thức chính quy dễ quản lý hơn. Nếu không có nó, mọi dấu gạch chéo ngược (``'\'``) trong biểu thức chính quy đều phải được thêm một dấu gạch chéo ngược khác ở trước để thoát. Ví dụ, hai dòng mã sau đây có chức năng giống hệt nhau::

   >>> re.match(r"\W(.)\1\W", " ff ")
   <re.Match object; span=(0, 4), match=' ff '>
   >>> re.match("\\W(.)\\1\\W", " ff ")
   <re.Match object; span=(0, 4), match=' ff '>

Khi muốn khớp một dấu gạch chéo ngược theo nghĩa đen, dấu đó phải được thoát trong biểu thức chính quy. Với ký hiệu chuỗi thô, điều này có nghĩa là ``r"\\"``. Nếu không dùng ký hiệu chuỗi thô, phải sử dụng ``"\\\\"``, khiến các dòng mã sau đây có chức năng giống hệt nhau::

   >>> re.match(r"\\", r"\\")
   <re.Match object; span=(0, 1), match='\\'>
   >>> re.match("\\\\", r"\\")
   <re.Match object; span=(0, 1), match='\\'>


Viết Tokenizer
^^^^^^^^^^^^^^

`Tokenizer hoặc scanner <https://en.wikipedia.org/wiki/Lexical_analysis>`_ phân tích một chuỗi để phân loại các nhóm ký tự. Đây là bước đầu tiên hữu ích khi viết một compiler hoặc interpreter.

Các danh mục văn bản được chỉ định bằng các biểu thức chính quy. Kỹ thuật này là kết hợp chúng thành một biểu thức chính quy tổng thể duy nhất và lặp qua các kết quả khớp liên tiếp::

    from typing import NamedTuple
    import re

    class Token(NamedTuple):
        type: str
        value: int | float | str
        line: int
        column: int

    def tokenize(code):
        keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),  # Số nguyên hoặc số thập phân
            ('ASSIGN',   r':='),           # Toán tử gán
            ('END',      r';'),            # Dấu kết thúc câu lệnh
            ('ID',       r'[A-Za-z]+'),    # Định danh
            ('OP',       r'[+\-*/]'),      # Toán tử số học
            ('NEWLINE',  r'\n'),           # Ký tự kết thúc dòng
            ('SKIP',     r'[ \t]+'),       # Bỏ qua khoảng trắng và tab
            ('MISMATCH', r'.'),            # Mọi ký tự khác
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value in keywords:
                kind = value
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            yield Token(kind, value, line_num, column)

    statements = '''
        IF quantity THEN
            total := total + price * quantity;
            tax := price * 0.05;
        ENDIF;
    '''

    for token in tokenize(statements):
        print(token)

Tokenizer tạo ra kết quả sau::

    Token(type='IF', value='IF', line=2, column=4)
    Token(type='ID', value='quantity', line=2, column=7)
    Token(type='THEN', value='THEN', line=2, column=16)
    Token(type='ID', value='total', line=3, column=8)
    Token(type='ASSIGN', value=':=', line=3, column=14)
    Token(type='ID', value='total', line=3, column=17)
    Token(type='OP', value='+', line=3, column=23)
    Token(type='ID', value='price', line=3, column=25)
    Token(type='OP', value='*', line=3, column=31)
    Token(type='ID', value='quantity', line=3, column=33)
    Token(type='END', value=';', line=3, column=41)
    Token(type='ID', value='tax', line=4, column=8)
    Token(type='ASSIGN', value=':=', line=4, column=12)
    Token(type='ID', value='price', line=4, column=15)
    Token(type='OP', value='*', line=4, column=21)
    Token(type='NUMBER', value=0.05, line=4, column=23)
    Token(type='END', value=';', line=4, column=27)
    Token(type='ENDIF', value='ENDIF', line=5, column=4)
    Token(type='END', value=';', line=5, column=9)


.. [Frie09] Friedl, Jeffrey. Mastering Regular Expressions. Ấn bản thứ 3, O'Reilly Media, 2009. Ấn bản thứ ba của cuốn sách không còn đề cập đến Python, nhưng ấn bản đầu tiên trình bày rất chi tiết về cách viết các mẫu regular expression tốt.

.. _`tokenizer or scanner`: https://en.wikipedia.org/wiki/Lexical_analysis
