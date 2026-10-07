.. _regex-howto:

********************************
Hướng dẫn về biểu thức chính quy
********************************

:Author: A.M. Kuchling <amk@amk.ca>

.. TODO:
   Document lookbehind assertions
   Better way of displaying a RE, a string, and what it matches
   Mention optional argument to match.groups()
   Unicode (at least a reference)


.. topic:: Tóm tắt

   Tài liệu này là hướng dẫn nhập môn về cách sử dụng biểu thức chính quy trong Python với mô-đun :mod:`re`. Tài liệu cung cấp phần giới thiệu dễ tiếp cận hơn so với phần tương ứng trong Library Reference.


Giới thiệu
==========

Biểu thức chính quy (được gọi là RE, regex hoặc mẫu regex) về cơ bản là một ngôn ngữ lập trình nhỏ, chuyên biệt cao, được nhúng bên trong Python và cung cấp thông qua mô-đun :mod:`re`. Bằng cách sử dụng ngôn ngữ nhỏ này, bạn chỉ định các quy tắc cho tập hợp những chuỗi có thể khớp; tập hợp này có thể chứa các câu tiếng Anh, địa chỉ e-mail, lệnh TeX hoặc bất cứ thứ gì bạn muốn. Sau đó, bạn có thể đặt những câu hỏi như "Chuỗi này có khớp với mẫu không?" hoặc "Mẫu này có khớp ở vị trí nào trong chuỗi không?". Bạn cũng có thể sử dụng RE để sửa đổi một chuỗi hoặc tách chuỗi đó theo nhiều cách khác nhau.

Các mẫu biểu thức chính quy được biên dịch thành một loạt bytecode, sau đó được thực thi bởi một matching engine được viết bằng C. Đối với việc sử dụng nâng cao, có thể cần chú ý cẩn thận đến cách engine thực thi một RE cụ thể và viết RE theo một cách nhất định để tạo ra bytecode chạy nhanh hơn. Tài liệu này không đề cập đến việc tối ưu hóa vì việc đó đòi hỏi bạn phải hiểu rõ về các thành phần bên trong của matching engine.

Ngôn ngữ biểu thức chính quy tương đối nhỏ và hạn chế, vì vậy không phải mọi tác vụ xử lý chuỗi có thể thực hiện đều có thể được thực hiện bằng biểu thức chính quy. Ngoài ra, có những tác vụ *có thể* được thực hiện bằng biểu thức chính quy, nhưng các biểu thức cuối cùng lại trở nên rất phức tạp. Trong những trường hợp này, bạn có thể sẽ phù hợp hơn khi viết mã Python để thực hiện việc xử lý; mặc dù mã Python sẽ chậm hơn một biểu thức chính quy phức tạp, nhưng có lẽ cũng dễ hiểu hơn.


Mẫu đơn giản
============

Chúng ta sẽ bắt đầu bằng cách tìm hiểu về những biểu thức chính quy đơn giản nhất có thể. Vì biểu thức chính quy được dùng để thao tác trên chuỗi, chúng ta sẽ bắt đầu với tác vụ phổ biến nhất: khớp ký tự.

Để xem giải thích chi tiết về nền tảng khoa học máy tính của biểu thức chính quy (finite automata tất định và không tất định), bạn có thể tham khảo hầu như bất kỳ giáo trình nào về viết compiler.


Khớp ký tự
----------

Hầu hết các chữ cái và ký tự sẽ chỉ khớp với chính chúng. Ví dụ, biểu thức chính quy ``test`` sẽ khớp chính xác với chuỗi ``test``. (Bạn có thể bật chế độ không phân biệt chữ hoa chữ thường để cho phép RE này khớp với cả ``Test`` hoặc ``TEST``; chúng ta sẽ tìm hiểu thêm về điều này sau.)

Có những ngoại lệ cho quy tắc này; một số ký tự là ký tự đặc biệt
:dfn:`siêu ký tự`, và không khớp với chính chúng. Thay vào đó, chúng báo hiệu rằng cần khớp một điều gì đó khác thường, hoặc tác động đến các phần khác của RE bằng cách lặp lại chúng hoặc thay đổi ý nghĩa của chúng. Phần lớn tài liệu này dành để thảo luận về các siêu ký tự khác nhau và chức năng của chúng.

Dưới đây là danh sách đầy đủ các siêu ký tự; ý nghĩa của chúng sẽ được thảo luận trong phần còn lại của HOWTO này.

.. code-block:: none

   . ^ $ * + ? { } [ ] \ | ( )

Các siêu ký tự đầu tiên chúng ta sẽ tìm hiểu là ``[`` và ``]``. Chúng được dùng để chỉ định một character class, tức là một tập hợp các ký tự mà bạn muốn khớp. Các ký tự có thể được liệt kê riêng lẻ, hoặc một dải ký tự có thể được chỉ định bằng cách đưa ra hai ký tự và phân tách chúng bằng ``'-'``. Ví dụ, ``[abc]`` sẽ khớp với bất kỳ ký tự nào trong số ``a``, ``b`` hoặc ``c``; cách này tương đương với ``[a-c]``, sử dụng một dải để biểu diễn cùng một tập hợp ký tự. Nếu bạn chỉ muốn khớp các chữ cái viết thường, RE của bạn sẽ là ``[a-z]``.

Các siêu ký tự (ngoại trừ ``\``) không có hiệu lực bên trong các class. Ví dụ, ``[akm$]`` sẽ khớp với bất kỳ ký tự nào trong số ``'a'``, ``'k'``, ``'m'`` hoặc ``'$'``; ``'$'`` thường là một siêu ký tự, nhưng bên trong character class, nó mất đi tính chất đặc biệt.

Bạn có thể khớp các ký tự không được liệt kê trong class bằng cách :dfn:`bù` cho tập hợp đó. Điều này được biểu thị bằng cách đặt ``'^'`` làm ký tự đầu tiên của class. Ví dụ, ``[^5]`` sẽ khớp với mọi ký tự ngoại trừ ``'5'``. Nếu dấu mũ xuất hiện ở vị trí khác trong character class, nó không có ý nghĩa đặc biệt. Ví dụ: ``[5^]`` sẽ khớp với một ``'5'`` hoặc một ``'^'``.

Có lẽ siêu ký tự quan trọng nhất là dấu gạch chéo ngược, ``\``. Cũng như trong các string literal của Python, dấu gạch chéo ngược có thể được theo sau bởi nhiều ký tự khác nhau để biểu thị các chuỗi đặc biệt khác nhau. Nó cũng được dùng để escape tất cả các siêu ký tự, để bạn vẫn có thể khớp chúng trong các pattern; ví dụ, nếu cần khớp một ``[`` hoặc ``\``, bạn có thể đặt dấu gạch chéo ngược trước chúng để loại bỏ ý nghĩa đặc biệt: ``\[`` hoặc ``\\``.

Một số chuỗi đặc biệt bắt đầu bằng ``'\'`` biểu diễn các tập hợp ký tự được định nghĩa sẵn và thường hữu ích, chẳng hạn như tập hợp các chữ số, tập hợp các chữ cái hoặc tập hợp mọi ký tự không phải khoảng trắng.

Hãy lấy một ví dụ: ``\w`` khớp với mọi ký tự chữ và số. Nếu mẫu regex được biểu diễn dưới dạng byte, điều này tương đương với lớp ``[a-zA-Z0-9_]``. Nếu mẫu regex là một chuỗi, ``\w`` sẽ khớp với tất cả các ký tự được đánh dấu là chữ cái trong cơ sở dữ liệu Unicode do mô-đun :mod:`unicodedata` cung cấp. Bạn có thể sử dụng định nghĩa hạn chế hơn của ``\w`` trong mẫu chuỗi bằng cách cung cấp
cờ :const:`re.ASCII` khi biên dịch biểu thức chính quy.

Danh sách các chuỗi đặc biệt sau đây chưa đầy đủ. Để xem danh sách đầy đủ các chuỗi và định nghĩa lớp mở rộng cho các mẫu chuỗi Unicode, hãy xem phần cuối của :ref:`Cú pháp biểu thức chính quy <re-syntax>` trong tài liệu tham khảo Standard Library. Nhìn chung, các phiên bản Unicode khớp với mọi ký tự thuộc danh mục tương ứng trong cơ sở dữ liệu Unicode.

``\d``
   Khớp với mọi chữ số thập phân; điều này tương đương với lớp ``[0-9]``.

``\D``
   Khớp với mọi ký tự không phải chữ số; điều này tương đương với lớp ``[^0-9]``.

``\s``
   Khớp với mọi ký tự khoảng trắng; điều này tương đương với lớp ``[ \t\n\r\f\v]``.

``\S``
   Khớp với mọi ký tự không phải khoảng trắng; điều này tương đương với lớp ``[^ \t\n\r\f\v]``.

``\w``
   Khớp với mọi ký tự chữ và số; tương đương với lớp ``[a-zA-Z0-9_]``.

``\W``
   Khớp với mọi ký tự không phải chữ hoặc số; tương đương với lớp ``[^a-zA-Z0-9_]``.

Các chuỗi này có thể được đưa vào bên trong một lớp ký tự. Ví dụ: ``[\s,.]`` là một lớp ký tự sẽ khớp với mọi ký tự khoảng trắng, hoặc ``','`` hoặc ``'.'``.

Siêu ký tự cuối cùng trong phần này là ``.``. Nó khớp với mọi thứ ngoại trừ ký tự xuống dòng, và có một chế độ thay thế (:const:`re.DOTALL`) trong đó nó sẽ khớp cả ký tự xuống dòng. ``.`` thường được dùng khi bạn muốn khớp với "bất kỳ ký tự nào".


Lặp lại các thành phần
----------------------

Khả năng khớp với các tập ký tự khác nhau là điều đầu tiên mà regular expression có thể làm nhưng các phương thức có sẵn trên chuỗi thì chưa thể làm được. Tuy nhiên, nếu đó là khả năng bổ sung duy nhất của regex thì chúng sẽ không mang lại nhiều tiến bộ. Một khả năng khác là bạn có thể chỉ định rằng các phần của RE phải được lặp lại một số lần nhất định.

Siêu ký tự đầu tiên dùng để lặp lại các thành phần mà chúng ta sẽ tìm hiểu là ``*``. ``*`` không khớp với ký tự literal ``'*'``; thay vào đó, nó chỉ định rằng ký tự trước đó có thể được khớp từ không đến nhiều lần, thay vì đúng một lần.

Ví dụ: ``ca*t`` sẽ khớp với ``'ct'`` (0 ``'a'`` ký tự), ``'cat'`` (1 ``'a'``), ``'caaat'`` (3 ``'a'`` ký tự), v.v.

Các phép lặp như ``*`` có tính :dfn:`tham lam`; khi lặp một RE, công cụ khớp sẽ cố gắng lặp nó nhiều lần nhất có thể. Nếu các phần sau của mẫu không khớp, công cụ khớp sẽ quay lui rồi thử lại với số lần lặp ít hơn.

Một ví dụ từng bước sẽ giúp điều này dễ hiểu hơn. Hãy xét biểu thức ``a[bcd]*b``. Biểu thức này khớp với chữ cái ``'a'``, không hoặc nhiều chữ cái thuộc lớp ``[bcd]``, và cuối cùng kết thúc bằng một ``'b'``. Bây giờ hãy thử khớp RE này với chuỗi ``'abcbd'``.

+------+------------+--------------------------------------------------------------------------------------------+
| Bước | Đã khớp    | Giải thích                                                                                 |
+======+============+============================================================================================+
| 1    | ``a``      | ``a`` trong RE khớp.                                                                       |
+------+------------+--------------------------------------------------------------------------------------------+
| 2    | ``abcbd``  | Engine khớp với ``[bcd]*``, đi xa nhất có thể, tức là đến cuối chuỗi.                      |
+------+------------+--------------------------------------------------------------------------------------------+
| 3    | *Thất bại* | Engine cố khớp với ``b``, nhưng vị trí hiện tại đã ở cuối chuỗi nên khớp thất bại.         |
+------+------------+--------------------------------------------------------------------------------------------+
| 4    | ``abcb``   | Lùi lại để  ``[bcd]*`` khớp ít hơn một ký tự.                                              |
+------+------------+--------------------------------------------------------------------------------------------+
| 5    | *Thất bại* | Thử lại ``b``, nhưng vị trí hiện tại đang ở ký tự cuối cùng, đó là một ``'d'``.            |
+------+------------+--------------------------------------------------------------------------------------------+
| 6    | ``abc``    | Lùi lại lần nữa để ``[bcd]*`` chỉ khớp với ``bc``.                                         |
+------+------------+--------------------------------------------------------------------------------------------+
| 7    | ``abcb``   | Thử ``b`` lại. Lần này, ký tự tại vị trí hiện tại là ``'b'``, nên phép so khớp thành công. |
+------+------------+--------------------------------------------------------------------------------------------+

Đã đi đến cuối RE và nó đã khớp với ``'abcb'``. Điều này minh họa cách công cụ so khớp cố gắng đi xa nhất có thể ngay từ đầu; nếu không tìm thấy kết quả khớp, nó sẽ dần quay lui và thử lại phần còn lại của RE hết lần này đến lần khác. Nó sẽ quay lui cho đến khi đã thử số lần khớp bằng không với ``[bcd]*``; nếu sau đó vẫn thất bại, công cụ sẽ kết luận rằng chuỗi hoàn toàn không khớp với RE.

Một metacharacter lặp khác là ``+``, khớp một hoặc nhiều lần. Hãy chú ý kỹ sự khác biệt giữa ``*`` và ``+``; ``*`` khớp *zero* lần trở lên, vì vậy phần được lặp có thể hoàn toàn không xuất hiện, trong khi ``+`` yêu cầu ít nhất *one* lần xuất hiện. Lấy một ví dụ tương tự, ``ca+t`` sẽ khớp ``'cat'`` (1 ``'a'``), ``'caaat'`` (3 ``'a'``\ s), nhưng sẽ không khớp ``'ct'``.

Còn hai toán tử lặp hoặc quantifier nữa. Ký tự dấu chấm hỏi, ``?``, khớp một lần hoặc không lần nào; bạn có thể xem nó như việc đánh dấu một phần là tùy chọn. Ví dụ, ``home-?brew`` khớp ``'homebrew'`` hoặc ``'home-brew'``.

Quantifier phức tạp nhất là ``{m,n}``, trong đó *m* và *n* là các số nguyên thập phân. Quantifier này có nghĩa là phải có ít nhất *m* lần lặp và nhiều nhất *n* lần. Ví dụ, ``a/{1,3}b`` sẽ khớp ``'a/b'``, ``'a//b'`` và ``'a///b'``. Nó sẽ không khớp ``'ab'``, vì chuỗi này không có dấu gạch chéo nào, hoặc ``'a////b'``, vì chuỗi này có bốn dấu gạch chéo.

Bạn có thể bỏ qua *m* hoặc *n*; trong trường hợp đó, một giá trị hợp lý sẽ được giả định cho giá trị bị thiếu. Bỏ qua *m* được hiểu là giới hạn dưới bằng 0, còn bỏ qua *n* sẽ cho giới hạn trên bằng vô cực.

Trường hợp đơn giản nhất ``{m}`` khớp chính xác mục đứng trước nó *m* lần. Ví dụ, ``a/{2}b`` sẽ chỉ khớp ``'a//b'``.

Những độc giả có khuynh hướng giản lược có thể nhận thấy rằng ba lượng từ còn lại đều có thể được biểu diễn bằng ký hiệu này. ``{0,}`` giống với ``*``, ``{1,}`` tương đương với ``+``, còn ``{0,1}`` giống với ``?``. Khi có thể, tốt hơn nên dùng ``*``, ``+`` hoặc ``?``, đơn giản vì chúng ngắn hơn và dễ đọc hơn.


Sử dụng biểu thức chính quy
===========================

Bây giờ chúng ta đã xem qua một số biểu thức chính quy đơn giản, vậy thực sự sử dụng chúng trong Python như thế nào? Mô-đun :mod:`re` cung cấp một interface cho regular expression engine, cho phép bạn biên dịch các RE thành các đối tượng rồi thực hiện việc so khớp với chúng.


Biên dịch biểu thức chính quy
-----------------------------

Các biểu thức chính quy được biên dịch thành các đối tượng pattern, có những phương thức để thực hiện nhiều thao tác khác nhau, chẳng hạn như tìm kiếm các kết quả khớp với pattern hoặc thực hiện thay thế chuỗi.::

   >>> import re
   >>> p = re.compile('ab*')
   >>> p
   re.compile('ab*')

:func:`re.compile` cũng chấp nhận một đối số *flags* tùy chọn, dùng để bật nhiều tính năng đặc biệt và biến thể cú pháp khác nhau. Chúng ta sẽ xem xét các thiết lập hiện có sau, nhưng hiện tại chỉ cần một ví dụ là đủ::

   >>> p = re.compile('ab*', re.IGNORECASE)

RE được truyền vào :func:`re.compile` dưới dạng chuỗi. Các RE được xử lý dưới dạng chuỗi vì biểu thức chính quy không thuộc ngôn ngữ Python cốt lõi và không có cú pháp đặc biệt nào được tạo ra để biểu diễn chúng. (Có những ứng dụng hoàn toàn không cần RE, vì vậy không cần làm phình to đặc tả ngôn ngữ bằng cách đưa chúng vào.) Thay vào đó, mô-đun :mod:`re` đơn giản là một mô-đun mở rộng C được tích hợp trong Python, giống như các mô-đun :mod:`socket` hoặc :mod:`zlib`.

Việc đặt RE trong chuỗi giúp ngôn ngữ Python đơn giản hơn, nhưng có một nhược điểm và đó là chủ đề của phần tiếp theo.


.. _the-backslash-plague:

Vấn đề với dấu gạch chéo ngược
------------------------------

Như đã nêu trước đó, biểu thức chính quy sử dụng ký tự gạch chéo ngược (``'\'``) để biểu thị các dạng đặc biệt hoặc cho phép sử dụng các ký tự đặc biệt mà không kích hoạt ý nghĩa đặc biệt của chúng. Điều này xung đột với cách Python sử dụng cùng ký tự đó cho cùng mục đích trong các string literal.

Giả sử bạn muốn viết một RE khớp với chuỗi ``\section``, vốn có thể xuất hiện trong một tệp LaTeX. Để xác định cần viết gì trong mã chương trình, hãy bắt đầu bằng chuỗi mong muốn được khớp. Tiếp theo, bạn phải escape mọi dấu gạch chéo ngược và các metacharacter khác bằng cách đặt một dấu gạch chéo ngược trước chúng, tạo thành chuỗi ``\\section``. Chuỗi kết quả cần được truyền cho :func:`re.compile` phải là ``\\section``. Tuy nhiên, để biểu diễn chuỗi này dưới dạng một string literal trong Python, cả hai dấu gạch chéo ngược đều phải được escape *một lần nữa*.

+-------------------+------------------------------------------------------------+
| Các ký tự         | Giai đoạn                                                  |
+===================+============================================================+
| ``\section``      | Chuỗi văn bản cần khớp                                     |
+-------------------+------------------------------------------------------------+
| ``\\section``     | Dấu gạch chéo ngược được escape cho :func:`re.compile`     |
+-------------------+------------------------------------------------------------+
| ``"\\\\section"`` | Các dấu gạch chéo ngược được escape cho một string literal |
+-------------------+------------------------------------------------------------+

Tóm lại, để khớp với một dấu gạch chéo ngược literal, ta phải viết ``'\\\\'`` làm chuỗi RE, vì regular expression phải là ``\\``, và mỗi dấu gạch chéo ngược phải được biểu diễn bằng ``\\`` bên trong một regular string literal của Python. Trong các RE có nhiều dấu gạch chéo ngược, điều này dẫn đến rất nhiều dấu gạch chéo ngược lặp lại và khiến các chuỗi kết quả khó hiểu.

Giải pháp là sử dụng ký hiệu raw string của Python cho regular expression; các dấu gạch chéo ngược không được xử lý theo cách đặc biệt nào trong một string literal có tiền tố ``'r'``, vì vậy ``r"\n"`` là một chuỗi gồm hai ký tự chứa ``'\'`` và ``'n'``, trong khi ``"\n"`` là một chuỗi gồm một ký tự chứa ký tự xuống dòng. Regular expression thường được viết trong mã Python bằng ký hiệu raw string này.

Ngoài ra, các escape sequence đặc biệt hợp lệ trong regular expression nhưng không hợp lệ dưới dạng string literal của Python giờ đây sẽ tạo ra một
:exc:`SyntaxWarning` và cuối cùng sẽ trở thành :exc:`SyntaxError`, nghĩa là các chuỗi này sẽ không hợp lệ nếu không sử dụng ký hiệu raw string hoặc không escape các dấu gạch chéo ngược.


+-------------------+------------------+
| Regular String    | Chuỗi thô        |
+===================+==================+
| ``"ab*"``         | ``r"ab*"``       |
+-------------------+------------------+
| ``"\\\\section"`` | ``r"\\section"`` |
+-------------------+------------------+
| ``"\\w+\\s+\\1"`` | ``r"\w+\s+\1"``  |
+-------------------+------------------+


Thực hiện khớp
--------------

Sau khi có một đối tượng biểu diễn một biểu thức chính quy đã được biên dịch, bạn sẽ làm gì với nó? Các đối tượng Pattern có một số phương thức và thuộc tính. Ở đây chỉ đề cập đến những thành phần quan trọng nhất; hãy tham khảo tài liệu :mod:`re` để xem danh sách đầy đủ.

+------------------------+-------------------------------------------------------------------------------------+
| Phương thức/Thuộc tính | Mục đích                                                                            |
+========================+=====================================================================================+
| ``match()``            | Xác định liệu RE có khớp ở đầu chuỗi hay không.                                     |
+------------------------+-------------------------------------------------------------------------------------+
| ``search()``           | Quét qua một chuỗi, tìm mọi vị trí mà RE này khớp.                                  |
+------------------------+-------------------------------------------------------------------------------------+
| ``findall()``          | Tìm tất cả các chuỗi con mà RE khớp và trả về chúng dưới dạng một danh sách.        |
+------------------------+-------------------------------------------------------------------------------------+
| ``finditer()``         | Tìm tất cả các chuỗi con mà RE khớp và trả về chúng dưới dạng một :term:`iterator`. |
+------------------------+-------------------------------------------------------------------------------------+

:meth:`~re.Pattern.match` và :meth:`~re.Pattern.search` trả về ``None`` nếu không tìm thấy kết quả khớp nào. Nếu thành công, một thực thể :ref:`đối tượng match <match-objects>` sẽ được trả về, chứa thông tin về kết quả khớp: vị trí bắt đầu và kết thúc, chuỗi con được khớp và nhiều thông tin khác.

Bạn có thể tìm hiểu điều này bằng cách thử nghiệm tương tác với module :mod:`re`.

HOWTO này sử dụng trình thông dịch Python tiêu chuẩn cho các ví dụ. Trước tiên, hãy chạy trình thông dịch Python, import module :mod:`re` và compile một RE::

   >>> import re
   >>> p = re.compile('[a-z]+')
   >>> p
   re.compile('[a-z]+')

Bây giờ, bạn có thể thử khớp nhiều chuỗi khác nhau với RE ``[a-z]+``. Một chuỗi rỗng hoàn toàn không nên khớp, vì ``+`` có nghĩa là 'một hoặc nhiều lần lặp lại'.
Trong trường hợp này, :meth:`~re.Pattern.match` sẽ trả về ``None``, khiến trình thông dịch không in ra kết quả nào. Bạn có thể in rõ ràng kết quả của
:meth:`!match` để làm rõ điều này.::

   >>> p.match("")
   >>> print(p.match(""))
   None

Bây giờ, hãy thử với một chuỗi mà nó sẽ khớp, chẳng hạn như ``tempo``. Trong trường hợp này, :meth:`~re.Pattern.match` sẽ trả về một đối tượng :ref:`match object <match-objects>`, vì vậy bạn nên lưu kết quả vào một biến để sử dụng sau.::

   >>> m = p.match('tempo')
   >>> m
   <re.Match object; span=(0, 5), match='tempo'>

Bây giờ, bạn có thể truy vấn :ref:`match object <match-objects>` để lấy thông tin về chuỗi khớp. Các đối tượng Match cũng có một số phương thức và thuộc tính; những thành phần quan trọng nhất là:

+------------------------+-----------------------------------------------------------------------+
| Phương thức/Thuộc tính | Mục đích                                                              |
+========================+=======================================================================+
| ``group()``            | Trả về chuỗi được RE khớp                                             |
+------------------------+-----------------------------------------------------------------------+
| ``start()``            | Trả về vị trí bắt đầu của kết quả khớp                                |
+------------------------+-----------------------------------------------------------------------+
| ``end()``              | Trả về vị trí kết thúc của kết quả khớp                               |
+------------------------+-----------------------------------------------------------------------+
| ``span()``             | Trả về một tuple chứa các vị trí (bắt đầu, kết thúc) của kết quả khớp |
+------------------------+-----------------------------------------------------------------------+

Thử các phương thức này sẽ nhanh chóng giúp làm rõ ý nghĩa của chúng::

   >>> m.group()
   'tempo'
   >>> m.start(), m.end()
   (0, 5)
   >>> m.span()
   (0, 5)

:meth:`~re.Match.group` trả về chuỗi con được RE khớp. :meth:`~re.Match.start` và :meth:`~re.Match.end` trả về chỉ mục bắt đầu và kết thúc của kết quả khớp. :meth:`~re.Match.span` trả về cả chỉ mục bắt đầu và kết thúc trong một tuple duy nhất. Vì phương thức :meth:`~re.Pattern.match` chỉ kiểm tra xem RE có khớp ở đầu chuỗi hay không, :meth:`!start` sẽ luôn bằng không. Tuy nhiên, phương thức :meth:`~re.Pattern.search` của các pattern sẽ quét xuyên suốt chuỗi, vì vậy trong trường hợp đó, kết quả khớp có thể không bắt đầu từ không.::

   >>> print(p.match('::: message'))
   None
   >>> m = p.search('::: message'); print(m)
   <re.Match object; span=(4, 11), match='message'>
   >>> m.group()
   'message'
   >>> m.span()
   (4, 11)

Trong các chương trình thực tế, cách thường dùng nhất là lưu
:ref:`match object <match-objects>` vào một biến, rồi kiểm tra xem nó có ``None``. Điều này thường có dạng::

   p = re.compile( ... )
   m = p.match( 'string goes here' )
   if m:
       print('Match found: ', m.group())
   else:
       print('No match')

Hai phương thức của pattern trả về tất cả kết quả khớp của một pattern.
:meth:`~re.Pattern.findall` trả về một danh sách các chuỗi khớp::

   >>> p = re.compile(r'\d+')
   >>> p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')
   ['12', '11', '10']

Tiền tố ``r``, biến literal thành raw string literal, là cần thiết trong ví dụ này vì các escape sequence trong literal chuỗi "cooked" thông thường mà Python không nhận diện, trái với regular expressions, giờ đây sẽ dẫn đến một
:exc:`SyntaxWarning` và cuối cùng sẽ trở thành một :exc:`SyntaxError`.  Xem
:ref:`the-backslash-plague`.

:meth:`~re.Pattern.findall` phải tạo toàn bộ danh sách trước khi có thể trả về danh sách đó làm kết quả. Phương thức :meth:`~re.Pattern.finditer` trả về một sequence gồm các
:ref:`đối tượng match <match-objects>` dưới dạng một :term:`iterator`::

   >>> iterator = p.finditer('12 drummers drumming, 11 ... 10 ...')
   >>> iterator  #doctest: +ELLIPSIS
   <callable_iterator object at 0x...>
   >>> for match in iterator:
   ...     print(match.span())
   ...
   (0, 2)
   (22, 24)
   (29, 31)


Các hàm cấp module
------------------

Bạn không cần tạo một đối tượng pattern rồi gọi các phương thức của nó;
:mod:`re` module cũng cung cấp các hàm cấp cao nhất có tên :func:`~re.match`,
:func:`~re.search`, :func:`~re.findall`, :func:`~re.sub`, v.v. Các hàm này nhận cùng các đối số như phương thức pattern tương ứng, với chuỗi RE được thêm vào làm đối số đầu tiên, và vẫn trả về ``None`` hoặc một
:ref:`đối tượng match <match-objects>`.::

   >>> print(re.match(r'From\s+', 'Fromage amk'))
   None
   >>> re.match(r'From\s+', 'From amk Thu May 14 19:12:10 1998')  #doctest: +ELLIPSIS
   <re.Match object; span=(0, 5), match='From '>

Về bản chất, các hàm này chỉ tạo một đối tượng pattern thay bạn rồi gọi phương thức thích hợp trên đó. Chúng cũng lưu đối tượng đã biên dịch vào bộ nhớ đệm, vì vậy các lần gọi sau sử dụng cùng RE sẽ không cần phân tích cú pháp pattern nhiều lần.

Bạn nên sử dụng các hàm cấp module này hay tự lấy pattern rồi gọi các phương thức của nó? Nếu bạn truy cập một regex bên trong vòng lặp, việc biên dịch trước sẽ giúp tiết kiệm một vài lần gọi hàm. Ngoài vòng lặp, nhờ bộ nhớ đệm nội bộ nên không có nhiều khác biệt.


Các cờ biên dịch
----------------

.. currentmodule:: re

Các cờ biên dịch cho phép bạn sửa đổi một số khía cạnh trong cách hoạt động của biểu thức chính quy. Các cờ có trong module :mod:`re` dưới hai tên: tên đầy đủ như
:const:`IGNORECASE` và dạng viết tắt một chữ cái như :const:`I`. (Nếu bạn quen với các modifier của pattern trong Perl, dạng một chữ cái sử dụng cùng những chữ cái đó; chẳng hạn, dạng viết tắt của :const:`re.VERBOSE` là :const:`re.X`.) Có thể chỉ định nhiều cờ bằng cách thực hiện phép OR theo bit giữa chúng; chẳng hạn, ``re.I | re.M`` thiết lập cả cờ :const:`I` và :const:`M`.

Sau đây là bảng các cờ hiện có, tiếp theo là phần giải thích chi tiết hơn về từng cờ.

+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| Cờ                                            | Ý nghĩa                                                                                                        |
+===============================================+================================================================================================================+
| :const:`ASCII`, :const:`A`                    | Khiến một số escape như ``\w``, ``\b``, ``\s`` và ``\d`` chỉ khớp với các ký tự ASCII có thuộc tính tương ứng. |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :const:`DOTALL`, :const:`S`                   | Làm cho ``.`` khớp với mọi ký tự, bao gồm cả ký tự xuống dòng.                                                 |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :const:`IGNORECASE`, :const:`I`               | Thực hiện khớp không phân biệt chữ hoa chữ thường.                                                             |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :const:`LOCALE`, :const:`L`                   | Thực hiện khớp có xét đến locale.                                                                              |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :const:`MULTILINE`, :const:`M`                | Khớp nhiều dòng, ảnh hưởng đến ``^`` và ``$``.                                                                 |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+
| :const:`VERBOSE`, :const:`X` (cho 'extended') | Bật RE ở chế độ verbose, giúp tổ chức chúng rõ ràng và dễ hiểu hơn.                                            |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------+


.. data:: I
          IGNORECASE
   :noindex:

   Thực hiện đối sánh không phân biệt hoa thường; character class và chuỗi literal sẽ đối sánh các chữ cái mà không xét hoa thường. Ví dụ, ``[A-Z]`` cũng sẽ đối sánh các chữ cái viết thường. Đối sánh Unicode đầy đủ cũng hoạt động, trừ khi sử dụng cờ :const:`ASCII` để tắt việc đối sánh các ký tự không phải ASCII. Khi sử dụng các mẫu Unicode ``[a-z]`` hoặc ``[A-Z]`` kết hợp với cờ :const:`IGNORECASE`, chúng sẽ đối sánh 52 chữ cái ASCII và 4 chữ cái không phải ASCII bổ sung: 'İ' (U+0130, chữ I hoa Latin có dấu chấm bên trên), 'ı' (U+0131, chữ i thường Latin không có dấu chấm), 'ſ' (U+017F, chữ s thường Latin dạng dài) và 'K' (U+212A, ký hiệu Kelvin). ``Spam`` sẽ đối sánh ``'Spam'``, ``'spam'``, ``'spAM'`` hoặc ``'ſpam'`` (ký tự sau cùng chỉ được đối sánh ở chế độ Unicode). Việc chuyển thành chữ thường này không xét đến locale hiện tại; nó sẽ xét đến locale nếu bạn cũng đặt cờ :const:`LOCALE`.


.. data:: L
          LOCALE
   :noindex:

   Làm cho ``\w``, ``\W``, ``\b``, ``\B`` và việc đối sánh không phân biệt hoa thường phụ thuộc vào locale hiện tại thay vì cơ sở dữ liệu Unicode.

   Locale là một tính năng của thư viện C, được thiết kế để hỗ trợ viết các chương trình có tính đến sự khác biệt giữa các ngôn ngữ. Ví dụ, nếu bạn đang xử lý văn bản tiếng Pháp đã mã hóa, bạn sẽ muốn có thể viết ``\w+`` để đối sánh các từ, nhưng ``\w`` chỉ đối sánh character class ``[A-Za-z]`` trong các mẫu bytes; nó sẽ không đối sánh các byte tương ứng với ``é`` hoặc ``ç``. Nếu hệ thống của bạn được cấu hình đúng và một locale tiếng Pháp được chọn, một số hàm C sẽ cho chương trình biết rằng byte tương ứng với ``é`` cũng nên được xem là một chữ cái. Việc đặt cờ :const:`LOCALE` khi biên dịch một regular expression sẽ khiến object đã biên dịch kết quả sử dụng các hàm C này cho ``\w``; cách này chậm hơn, nhưng cũng cho phép ``\w+`` đối sánh các từ tiếng Pháp như bạn mong đợi. Không nên sử dụng cờ này trong Python 3 vì cơ chế locale rất không đáng tin cậy, chỉ xử lý được một "văn hóa" tại một thời điểm và chỉ hoạt động với các locale 8-bit. Đối sánh Unicode đã được bật theo mặc định trong Python 3 đối với các mẫu Unicode (str), và có thể xử lý các locale/ngôn ngữ khác nhau.


.. data:: M
          MULTILINE
   :noindex:

   (``^`` và ``$`` vẫn chưa được giải thích; chúng sẽ được giới thiệu trong phần
   :ref:`more-metacharacters`.)

   Thông thường, ``^`` chỉ đối sánh ở đầu chuỗi, còn ``$`` chỉ đối sánh ở cuối chuỗi và ngay trước ký tự xuống dòng (nếu có) ở cuối chuỗi. Khi chỉ định cờ này, ``^`` đối sánh ở đầu chuỗi và ở đầu mỗi dòng trong chuỗi, ngay sau mỗi ký tự xuống dòng. Tương tự, metacharacter ``$`` đối sánh ở cuối chuỗi hoặc ở cuối mỗi dòng (ngay trước mỗi ký tự xuống dòng).


.. data:: S
          DOTALL
   :noindex:

   Khiến ký tự đặc biệt ``'.'`` khớp với mọi ký tự, kể cả ký tự xuống dòng; nếu không có flag này, ``'.'`` sẽ khớp với mọi thứ *ngoại trừ* ký tự xuống dòng.


.. data:: A
          ASCII
   :noindex:

   Khiến ``\w``, ``\W``, ``\b``, ``\B``, ``\s`` và ``\S`` chỉ thực hiện matching theo ASCII thay vì matching Unicode đầy đủ. Điều này chỉ có ý nghĩa đối với các pattern Unicode và bị bỏ qua đối với các pattern byte.


.. data:: X
          VERBOSE
   :noindex:

   Flag này cho phép bạn viết các regular expression dễ đọc hơn bằng cách linh hoạt hơn trong việc định dạng chúng. Khi flag này được chỉ định, khoảng trắng trong chuỗi RE sẽ bị bỏ qua, ngoại trừ khi khoảng trắng nằm trong một character class hoặc đứng trước một dấu gạch chéo ngược chưa được escape; nhờ đó, bạn có thể sắp xếp và thụt lề RE rõ ràng hơn. Flag này cũng cho phép bạn đặt các chú thích trong RE để engine bỏ qua; chú thích được đánh dấu bằng ``'#'`` không nằm trong một character class và không đứng trước một dấu gạch chéo ngược chưa được escape.

   Ví dụ: đây là một RE sử dụng :const:`re.VERBOSE`; bạn có thấy nó dễ đọc hơn nhiều không?::

      charref = re.compile(r"""
       &[#]                # Bắt đầu tham chiếu thực thể số
       (
           0[0-7]+         # Dạng bát phân
         | [0-9]+          # Dạng thập phân
         | x[0-9a-fA-F]+   # Dạng thập lục phân
       )
       ;                   # Dấu chấm phẩy ở cuối
      """, re.VERBOSE)

   Không có thiết lập verbose, RE sẽ trông như thế này::

      charref = re.compile("&#(0[0-7]+"
                           "|[0-9]+"
                           "|x[0-9a-fA-F]+);")

   Trong ví dụ trên, tính năng tự động nối các literal chuỗi của Python đã được dùng để chia RE thành các phần nhỏ hơn, nhưng nó vẫn khó hiểu hơn phiên bản sử dụng :const:`re.VERBOSE`.


Sức mạnh lớn hơn của pattern
============================

Cho đến nay, chúng ta mới chỉ đề cập đến một phần các tính năng của regular expression. Trong phần này, chúng ta sẽ tìm hiểu một số metacharacter mới và cách sử dụng các nhóm để lấy ra những phần văn bản đã được khớp.


.. _more-metacharacters:

Các metacharacter khác
----------------------

Vẫn còn một số metacharacter mà chúng ta chưa đề cập. Phần lớn trong số đó sẽ được trình bày trong phần này.

Một số metacharacter còn lại sẽ được thảo luận là :dfn:`các khẳng định có độ rộng bằng không (zero-width assertions)`. Chúng không khiến engine tiến qua chuỗi; thay vào đó, chúng không tiêu thụ bất kỳ ký tự nào và chỉ đơn giản là khớp hoặc không khớp. Ví dụ, ``\b`` là một khẳng định cho biết vị trí hiện tại nằm ở ranh giới từ; bản thân vị trí đó hoàn toàn không thay đổi bởi ``\b``. Điều này có nghĩa là không bao giờ nên lặp lại các khẳng định có độ rộng bằng không, bởi vì nếu chúng khớp một lần tại một vị trí nhất định thì rõ ràng chúng có thể khớp vô số lần.

``|``
   Phép luân phiên, hay toán tử "hoặc". Nếu *A* và *B* là các regular expression, ``A|B`` sẽ khớp với mọi chuỗi khớp với *A* hoặc *B*. ``|`` có độ ưu tiên rất thấp, để hoạt động hợp lý khi bạn luân phiên giữa các chuỗi gồm nhiều ký tự. ``Crow|Servo`` sẽ khớp với ``'Crow'`` hoặc ``'Servo'``, chứ không phải ``'Cro'``, một ``'w'`` hoặc một ``'S'``, và ``'ervo'``.

   Để khớp với một ``'|'`` nguyên văn, hãy sử dụng ``\|`` hoặc đặt nó bên trong một character class, như trong ``[|]``.

``^``
   Khớp ở đầu các dòng. Trừ khi cờ :const:`MULTILINE` được thiết lập, cờ này chỉ khớp ở đầu chuỗi. Trong chế độ :const:`MULTILINE`, cờ này cũng khớp ngay sau mỗi ký tự xuống dòng trong chuỗi.

   Ví dụ: nếu bạn muốn chỉ khớp từ ``From`` ở đầu một dòng, RE cần dùng là ``^From``.::

      >>> print(re.search('^From', 'From Here to Eternity'))  #doctest: +ELLIPSIS
      <re.Match object; span=(0, 4), match='From'>
      >>> print(re.search('^From', 'Reciting From Memory'))
      None

   Để khớp một ``'^'`` theo nghĩa đen, hãy dùng ``\^``.

``$``
   Khớp ở cuối một dòng, được định nghĩa là cuối chuỗi hoặc bất kỳ vị trí nào theo sau bởi một ký tự xuống dòng.::

      >>> print(re.search('}$', '{block}'))  #doctest: +ELLIPSIS
      <re.Match object; span=(6, 7), match='}'>
      >>> print(re.search('}$', '{block} '))
      None
      >>> print(re.search('}$', '{block}\n'))  #doctest: +ELLIPSIS
      <re.Match object; span=(6, 7), match='}'>

   Để khớp với một ``'$'`` theo nghĩa đen, hãy dùng ``\$`` hoặc đặt nó bên trong một character class, như trong ``[$]``.

``\A``
   Chỉ khớp ở đầu chuỗi. Khi không ở chế độ :const:`MULTILINE`, ``\A`` và ``^`` về cơ bản là giống nhau. Trong chế độ :const:`MULTILINE`, chúng khác nhau: ``\A`` vẫn chỉ khớp ở đầu chuỗi, nhưng ``^`` có thể khớp tại bất kỳ vị trí nào trong chuỗi, miễn là vị trí đó theo sau một ký tự xuống dòng.

``\z``
   Chỉ khớp ở cuối chuỗi.

``\Z``
   Giống ``\z``. Để tương thích với các phiên bản Python cũ.

``\b``
   Ranh giới từ. Đây là một khẳng định có độ rộng bằng không, chỉ khớp ở đầu hoặc cuối một từ. Một từ được định nghĩa là một chuỗi các ký tự chữ và số, vì vậy cuối từ được xác định bởi khoảng trắng hoặc một ký tự không phải chữ và số.

   Ví dụ sau chỉ khớp với ``class`` khi nó là một từ hoàn chỉnh; nó sẽ không khớp khi nằm bên trong một từ khác.::

      >>> p = re.compile(r'\bclass\b')
      >>> print(p.search('no class at all'))
      <re.Match object; span=(3, 8), match='class'>
      >>> print(p.search('the declassified algorithm'))
      None
      >>> print(p.search('one subclass is'))
      None

   Có hai điểm tinh tế bạn cần nhớ khi sử dụng chuỗi đặc biệt này. Thứ nhất, đây là xung đột nghiêm trọng nhất giữa string literal của Python và các chuỗi trong biểu thức chính quy. Trong string literal của Python, ``\b`` là ký tự backspace, có giá trị ASCII là 8. Nếu không sử dụng raw string, Python sẽ chuyển ``\b`` thành ký tự backspace, và RE của bạn sẽ không khớp như mong đợi. Ví dụ sau trông giống RE trước đó, nhưng bỏ qua ``'r'`` ở trước chuỗi RE.::

      >>> p = re.compile('\bclass\b')
      >>> print(p.search('no class at all'))
      None
      >>> print(p.search('\b' + 'class' + '\b'))
      <re.Match object; span=(0, 7), match='\x08class\x08'>

   Thứ hai, bên trong một character class, nơi assertion này không có tác dụng, ``\b`` đại diện cho ký tự backspace để tương thích với các string literal của Python.

``\B``
   Đây là một assertion zero-width khác, đối lập với ``\b``, chỉ khớp khi vị trí hiện tại không nằm tại ranh giới từ.


Grouping
--------

Thông thường, bạn cần thu được nhiều thông tin hơn là chỉ biết RE có khớp hay không. Regular expression thường được dùng để phân tích chuỗi bằng cách viết một RE được chia thành nhiều subgroup, mỗi subgroup khớp với một thành phần cần quan tâm. Ví dụ, một dòng header RFC-822 được chia thành tên header và một giá trị, ngăn cách bởi ``':'``, như sau:

.. code-block:: none

   From: author@example.com
   User-Agent: Thunderbird 1.5.0.9 (X11/20061227)
   MIME-Version: 1.0
   To: editor@example.com

Bạn có thể xử lý trường hợp này bằng cách viết một regular expression khớp với toàn bộ dòng header, trong đó có một group khớp với tên header và một group khác khớp với giá trị của header.

Các group được đánh dấu bằng các metacharacter ``'('``, ``')'``. ``'('`` và ``')'`` có ý nghĩa gần như trong các biểu thức toán học; chúng nhóm các biểu thức nằm bên trong lại với nhau, và bạn có thể lặp lại nội dung của một group bằng một quantifier như ``*``, ``+``, ``?`` hoặc ``{m,n}``. Ví dụ, ``(ab)*`` sẽ khớp với không hoặc nhiều lần lặp của ``ab``.::

   >>> p = re.compile('(ab)*')
   >>> print(p.match('ababababab').span())
   (0, 10)

Các group được biểu thị bằng ``'('``, ``')'`` cũng ghi lại chỉ mục bắt đầu và kết thúc của văn bản mà chúng khớp; bạn có thể lấy thông tin này bằng cách truyền một đối số cho :meth:`~re.Match.group`, :meth:`~re.Match.start`, :meth:`~re.Match.end`, và
:meth:`~re.Match.span`. Các nhóm được đánh số bắt đầu từ 0. Nhóm 0 luôn tồn tại; đó là toàn bộ RE, vì vậy
Các phương thức của đối tượng :ref:`match object <match-objects>` đều có nhóm 0 làm đối số mặc định. Sau này, chúng ta sẽ thấy cách biểu diễn các nhóm không bắt span văn bản mà chúng khớp.::

   >>> p = re.compile('(a)b')
   >>> m = p.match('ab')
   >>> m.group()
   'ab'
   >>> m.group(0)
   'ab'

Các nhóm con được đánh số từ trái sang phải, bắt đầu từ 1. Các nhóm có thể được lồng nhau; để xác định số, chỉ cần đếm các ký tự dấu ngoặc đơn mở từ trái sang phải.::

   >>> p = re.compile('(a(b)c)d')
   >>> m = p.match('abcd')
   >>> m.group(0)
   'abcd'
   >>> m.group(1)
   'abc'
   >>> m.group(2)
   'b'

:meth:`~re.Match.group` có thể được truyền vào nhiều số nhóm cùng lúc; khi đó, nó sẽ trả về một tuple chứa các giá trị tương ứng với những nhóm đó.::

   >>> m.group(2,1,2)
   ('b', 'abc', 'b')

Phương thức :meth:`~re.Match.groups` trả về một tuple chứa các chuỗi của tất cả nhóm con, từ 1 đến số nhóm con hiện có.::

   >>> m.groups()
   ('abc', 'b')

Backreference trong một pattern cho phép bạn chỉ định rằng nội dung của một nhóm bắt trước đó cũng phải được tìm thấy tại vị trí hiện tại trong chuỗi. Ví dụ, ``\1`` sẽ thành công nếu nội dung chính xác của nhóm 1 được tìm thấy tại vị trí hiện tại và không thành công trong trường hợp ngược lại. Hãy nhớ rằng string literal của Python cũng sử dụng dấu gạch chéo ngược theo sau là các chữ số để cho phép đưa các ký tự tùy ý vào chuỗi, vì vậy hãy chắc chắn sử dụng raw string khi đưa backreference vào RE.

Ví dụ, RE sau đây phát hiện các từ bị lặp đôi trong một chuỗi.::

   >>> p = re.compile(r'\b(\w+)\s+\1\b')
   >>> p.search('Paris in the the spring').group()
   'the the'

Các backreference như thế này thường không hữu ích khi chỉ tìm kiếm trong một chuỗi --- có rất ít định dạng văn bản lặp lại dữ liệu theo cách này --- nhưng bạn sẽ sớm nhận ra rằng chúng *rất* hữu ích khi thực hiện thay thế chuỗi.


Nhóm không capturing và nhóm được đặt tên
-----------------------------------------

Các RE phức tạp có thể sử dụng nhiều nhóm, vừa để capture các chuỗi con đáng quan tâm, vừa để nhóm và cấu trúc chính RE. Trong các RE phức tạp, việc theo dõi số nhóm trở nên khó khăn. Có hai tính năng giúp giải quyết vấn đề này. Cả hai đều sử dụng cú pháp chung cho phần mở rộng của regular expression, vì vậy trước tiên chúng ta sẽ xem xét cú pháp đó.

Perl 5 nổi tiếng với những bổ sung mạnh mẽ cho regular expression tiêu chuẩn. Đối với các tính năng mới này, các nhà phát triển Perl không thể chọn các metacharacter chỉ gồm một phím mới hoặc các chuỗi đặc biệt mới bắt đầu bằng ``\`` mà không khiến regular expression của Perl trở nên khác biệt một cách khó hiểu so với các RE tiêu chuẩn. Chẳng hạn, nếu họ chọn ``&`` làm metacharacter mới, các biểu thức cũ sẽ giả định rằng ``&`` là một ký tự thông thường và sẽ không escape nó bằng cách viết ``\&`` hoặc ``[&]``.

Giải pháp được các nhà phát triển Perl lựa chọn là sử dụng ``(?...)`` làm cú pháp mở rộng. ``?`` ngay sau dấu ngoặc đơn là một lỗi cú pháp vì ``?`` sẽ không có gì để lặp lại, do đó không gây ra vấn đề tương thích nào. Các ký tự ngay sau ``?`` cho biết phần mở rộng nào đang được sử dụng, vì vậy ``(?=foo)`` là một dạng (xác nhận lookahead dương), còn ``(?:foo)`` là một dạng khác (một nhóm không capturing chứa biểu thức con ``foo``).

Python hỗ trợ một số phần mở rộng của Perl và bổ sung cú pháp mở rộng riêng vào cú pháp mở rộng của Perl. Nếu ký tự đầu tiên sau dấu hỏi là ``P``, bạn biết đó là một phần mở rộng dành riêng cho Python.

Bây giờ, sau khi đã xem xét cú pháp mở rộng tổng quát, chúng ta có thể quay lại với các tính năng giúp đơn giản hóa việc làm việc với các nhóm trong những RE phức tạp.

Đôi khi bạn sẽ muốn sử dụng một nhóm để biểu thị một phần của regular expression, nhưng không quan tâm đến việc lấy nội dung của nhóm đó. Bạn có thể thể hiện rõ điều này bằng cách sử dụng một nhóm không bắt (non-capturing group): ``(?:...)``, trong đó bạn có thể thay ``...`` bằng bất kỳ regular expression nào khác.::

   >>> m = re.match("([abc])+", "abc")
   >>> m.groups()
   ('c',)
   >>> m = re.match("(?:[abc])+", "abc")
   >>> m.groups()
   ()

Ngoại trừ việc bạn không thể lấy nội dung mà nhóm đã khớp, nhóm không bắt hoạt động hoàn toàn giống như nhóm bắt; bạn có thể đặt bất kỳ nội dung nào bên trong nó, lặp lại nó bằng một repetition metacharacter như ``*``, và lồng nó trong các nhóm khác (bắt hoặc không bắt). ``(?:...)`` đặc biệt hữu ích khi sửa đổi một pattern hiện có, vì bạn có thể thêm các nhóm mới mà không thay đổi cách đánh số của tất cả các nhóm khác. Cần lưu ý rằng không có sự khác biệt về hiệu năng tìm kiếm giữa nhóm bắt và nhóm không bắt; không dạng nào nhanh hơn dạng kia.

Một tính năng đáng chú ý hơn là named group: thay vì tham chiếu đến các nhóm bằng số, bạn có thể tham chiếu đến chúng bằng một tên.

Cú pháp cho named group là một trong những phần mở rộng dành riêng cho Python: ``(?P<name>...)``. *name* hiển nhiên là tên của nhóm. Named group hoạt động hoàn toàn giống nhóm bắt, đồng thời liên kết một tên với một nhóm. Các phương thức của :ref:`match object <match-objects>` xử lý các nhóm bắt đều chấp nhận either số nguyên tham chiếu đến nhóm theo số hoặc chuỗi chứa tên của nhóm mong muốn. Named group vẫn được gán số, vì vậy bạn có thể lấy thông tin về một nhóm theo hai cách::

   >>> p = re.compile(r'(?P<word>\b\w+\b)')
   >>> m = p.search( '(((( Lots of punctuation )))' )
   >>> m.group('word')
   'Lots'
   >>> m.group(1)
   'Lots'

Ngoài ra, bạn có thể lấy các named group dưới dạng một dictionary bằng
:meth:`~re.Match.groupdict`::

   >>> m = re.match(r'(?P<first>\w+) (?P<last>\w+)', 'Jane Doe')
   >>> m.groupdict()
   {'first': 'Jane', 'last': 'Doe'}

Named group rất tiện dụng vì cho phép bạn sử dụng những tên dễ nhớ, thay vì phải nhớ các con số. Sau đây là một RE từ module :mod:`imaplib`::

   InternalDate = re.compile(r'INTERNALDATE "'
           r'(?P<day>[ 123][0-9])-(?P<mon>[A-Z][a-z][a-z])-'
           r'(?P<year>[0-9][0-9][0-9][0-9])'
           r' (?P<hour>[0-9][0-9]):(?P<min>[0-9][0-9]):(?P<sec>[0-9][0-9])'
           r' (?P<zonen>[-+])(?P<zoneh>[0-9][0-9])(?P<zonem>[0-9][0-9])'
           r'"')

Rõ ràng việc lấy ``m.group('zonem')`` dễ hơn nhiều, thay vì phải nhớ lấy group 9.

Cú pháp cho backreference trong một biểu thức như ``(...)\1`` tham chiếu đến số của group. Đương nhiên cũng có một biến thể sử dụng tên group thay cho số. Đây là một phần mở rộng khác của Python: ``(?P=name)`` cho biết nội dung của group có tên *name* sẽ lại được khớp tại vị trí hiện tại. Regular expression để tìm các từ lặp đôi, ``\b(\w+)\s+\1\b`` cũng có thể được viết là ``\b(?P<word>\w+)\s+(?P=word)\b``::

   >>> p = re.compile(r'\b(?P<word>\w+)\s+(?P=word)\b')
   >>> p.search('Paris in the the spring').group()
   'the the'


Khẳng định lookahead
--------------------

Một khẳng định zero-width khác là khẳng định lookahead. Khẳng định lookahead có cả dạng positive và negative, và có dạng như sau:

``(?=...)``
   Khẳng định positive lookahead. Khẳng định này thành công nếu regular expression nằm bên trong, được biểu diễn ở đây bằng ``...``, khớp thành công tại vị trí hiện tại, và thất bại nếu không. Tuy nhiên, sau khi thử biểu thức bên trong, matching engine hoàn toàn không tiến lên; phần còn lại của pattern được thử ngay tại nơi khẳng định bắt đầu.

``(?!...)``
   Khẳng định negative lookahead. Đây là điều ngược lại với khẳng định positive; nó thành công nếu biểu thức bên trong *doesn't* khớp tại vị trí hiện tại trong chuỗi.

Để làm rõ hơn, hãy xem một trường hợp lookahead hữu ích. Hãy xét một pattern đơn giản để khớp một filename và tách nó thành base name và extension, được phân cách bằng ``.``. Ví dụ, trong ``news.rc``, ``news`` là base name và ``rc`` là extension của filename.

Pattern để khớp chuỗi này khá đơn giản:

``.*[.].*$``

Lưu ý rằng ``.`` cần được xử lý đặc biệt vì nó là một metacharacter, nên nó được đặt trong một character class để chỉ khớp với ký tự cụ thể đó. Cũng lưu ý ``$`` ở cuối; phần này được thêm vào để đảm bảo rằng toàn bộ phần còn lại của chuỗi phải được đưa vào extension. Regular expression này khớp với ``foo.bar``, ``autoexec.bat``, ``sendmail.cf`` và ``printers.conf``.

Bây giờ, hãy xem xét việc làm bài toán phức tạp hơn một chút; nếu bạn muốn khớp các tên tệp có extension không phải là ``bat`` thì sao? Một số cách thử không đúng:

``.*[.][^b].*$``

Cách thử đầu tiên ở trên cố gắng loại trừ ``bat`` bằng cách yêu cầu ký tự đầu tiên của extension không phải là ``b``. Cách này sai vì pattern cũng không khớp với ``foo.bar``.

``.*[.]([^b]..|.[^a].|..[^t])$``

Biểu thức trở nên rắc rối hơn khi bạn cố sửa giải pháp đầu tiên bằng cách yêu cầu một trong các trường hợp sau phải khớp: ký tự đầu tiên của extension không phải là ``b``; ký tự thứ hai không phải là ``a``; hoặc ký tự thứ ba không phải là ``t``. Cách này chấp nhận ``foo.bar`` và từ chối ``autoexec.bat``, nhưng yêu cầu extension gồm ba chữ cái và sẽ không chấp nhận tên tệp có extension gồm hai chữ cái như ``sendmail.cf``. Chúng ta sẽ lại làm pattern phức tạp hơn để cố sửa lỗi này.

``.*[.]([^b].?.?|.[^a]?.?|..?[^t]?)$``

Trong lần thử thứ ba, chữ cái thứ hai và thứ ba đều được đặt thành tùy chọn để cho phép khớp các extension ngắn hơn ba ký tự, chẳng hạn như ``sendmail.cf``.

Bây giờ pattern đã trở nên thực sự phức tạp, khiến nó khó đọc và khó hiểu. Tệ hơn nữa, nếu bài toán thay đổi và bạn muốn loại trừ cả ``bat`` lẫn ``exe`` dưới dạng extension, pattern sẽ còn phức tạp và khó hiểu hơn nữa.

Một negative lookahead giúp giải quyết tất cả sự rắc rối này:

``.*[.](?!bat$)[^.]*$``

Negative lookahead có nghĩa là: nếu biểu thức ``bat`` không khớp tại vị trí này, hãy thử phần còn lại của pattern; nếu ``bat$`` khớp, toàn bộ pattern sẽ thất bại. ``$`` ở cuối là bắt buộc để đảm bảo rằng những chuỗi như ``sample.batch``, trong đó phần mở rộng chỉ bắt đầu bằng ``bat``, sẽ được cho phép. ``[^.]*`` đảm bảo rằng pattern vẫn hoạt động khi tên tệp có nhiều dấu chấm.

Việc loại trừ một phần mở rộng tệp khác giờ đây rất đơn giản; chỉ cần thêm nó như một lựa chọn bên trong assertion. Pattern sau loại trừ các tên tệp kết thúc bằng ``bat`` hoặc ``exe``:

``.*[.](?!bat$|exe$)[^.]*$``


Sửa đổi chuỗi
=============

Cho đến thời điểm này, chúng ta chỉ thực hiện tìm kiếm trên một chuỗi tĩnh. Regular expression cũng thường được dùng để sửa đổi chuỗi theo nhiều cách khác nhau, bằng các phương thức pattern sau:

+------------------------+--------------------------------------------------------------------------------+
| Phương thức/Thuộc tính | Mục đích                                                                       |
+========================+================================================================================+
| ``split()``            | Tách chuỗi thành một danh sách, tách chuỗi tại mọi vị trí mà RE khớp           |
+------------------------+--------------------------------------------------------------------------------+
| ``sub()``              | Tìm tất cả các chuỗi con khớp với RE và thay thế chúng bằng một chuỗi khác     |
+------------------------+--------------------------------------------------------------------------------+
| ``subn()``             | Thực hiện tương tự như :meth:`!sub`, nhưng trả về chuỗi mới và số lần thay thế |
+------------------------+--------------------------------------------------------------------------------+


Tách chuỗi
----------

Phương thức :meth:`~re.Pattern.split` của một pattern sẽ tách một chuỗi tại mọi vị trí RE khớp, rồi trả về danh sách các phần. Phương thức này tương tự như
phương thức :meth:`~str.split` của chuỗi nhưng cung cấp nhiều khả năng tổng quát hơn về các dấu phân cách mà bạn có thể dùng để tách; chuỗi :meth:`!split` chỉ hỗ trợ tách theo khoảng trắng hoặc một chuỗi cố định. Đúng như bạn mong đợi, cũng có hàm cấp mô-đun
:func:`re.split`.


.. method:: .split(string [, maxsplit=0])
   :noindex:

   Tách *string* theo các kết quả khớp của biểu thức chính quy. Nếu sử dụng các dấu ngoặc đơn bắt giữ trong RE, nội dung của chúng cũng sẽ được trả về như một phần của danh sách kết quả. Nếu *maxsplit* khác 0, thực hiện nhiều nhất *maxsplit* lần tách.

Bạn có thể giới hạn số lần tách được thực hiện bằng cách truyền một giá trị cho *maxsplit*. Khi *maxsplit* khác không, nhiều nhất *maxsplit* lần tách sẽ được thực hiện, và phần còn lại của chuỗi được trả về dưới dạng phần tử cuối cùng của danh sách. Trong
ví dụ sau, dấu phân cách là bất kỳ chuỗi nào gồm các ký tự không phải chữ và số.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

   >>> p = re.compile(r'\W+')
   >>> p.split('This is a test, short and sweet, of split().')
   ['This', 'is', 'a', 'test', 'short', 'and', 'sweet', 'of', 'split', '']
   >>> p.split('This is a test, short and sweet, of split().', 3)
   ['This', 'is', 'a', 'test, short and sweet, of split().']

Đôi khi bạn không chỉ quan tâm đến nội dung văn bản giữa các dấu phân cách mà còn cần biết dấu phân cách đó là gì. Nếu sử dụng các dấu ngoặc đơn bắt giữ trong RE, thì các giá trị của chúng cũng được trả về như một phần của danh sách. Hãy so sánh các lệnh gọi sau::

   >>> p = re.compile(r'\W+')
   >>> p2 = re.compile(r'(\W+)')
   >>> p.split('This... is a test.')
   ['This', 'is', 'a', 'test', '']
   >>> p2.split('This... is a test.')
   ['This', '... ', 'is', ' ', 'a', ' ', 'test', '.', '']

Hàm cấp mô-đun :func:`re.split` thêm RE cần sử dụng làm đối số đầu tiên, nhưng về các mặt khác thì giống hệt.::

   >>> re.split(r'[\W]+', 'Words, words, words.')
   ['Words', 'words', 'words', '']
   >>> re.split(r'([\W]+)', 'Words, words, words.')
   ['Words', ', ', 'words', ', ', 'words', '.', '']
   >>> re.split(r'[\W]+', 'Words, words, words.', 1)
   ['Words', 'words, words.']


Tìm kiếm và thay thế
--------------------

Một tác vụ phổ biến khác là tìm tất cả kết quả khớp với một pattern rồi thay thế chúng bằng một chuỗi khác. Phương thức :meth:`~re.Pattern.sub` nhận một giá trị thay thế, có thể là một chuỗi hoặc một hàm, cùng với chuỗi cần xử lý.

.. method:: .sub(replacement, string[, count=0])
   :noindex:

   Trả về chuỗi thu được bằng cách thay thế các lần xuất hiện không chồng lấp, nằm ở vị trí ngoài cùng bên trái của RE trong *string* bằng giá trị thay thế *replacement*. Nếu không tìm thấy pattern, *string* được trả về mà không thay đổi.

   Đối số tùy chọn *count* là số lần xuất hiện tối đa của mẫu sẽ được thay thế; *count* phải là một số nguyên không âm. Giá trị mặc định 0 có nghĩa là thay thế tất cả các lần xuất hiện.

Sau đây là một ví dụ đơn giản về cách sử dụng phương thức :meth:`~re.Pattern.sub`. Phương thức này thay thế tên màu bằng từ ``colour``::

   >>> p = re.compile('(blue|white|red)')
   >>> p.sub('colour', 'blue socks and red shoes')
   'colour socks and colour shoes'
   >>> p.sub('colour', 'blue socks and red shoes', count=1)
   'colour socks and red shoes'

Phương thức :meth:`~re.Pattern.subn` thực hiện công việc tương tự, nhưng trả về một tuple 2 phần tử chứa giá trị chuỗi mới và số lần thay thế đã được thực hiện::

   >>> p = re.compile('(blue|white|red)')
   >>> p.subn('colour', 'blue socks and red shoes')
   ('colour socks and colour shoes', 2)
   >>> p.subn('colour', 'no colours at all')
   ('no colours at all', 0)

Các kết quả khớp rỗng chỉ được thay thế khi chúng không liền kề với một kết quả khớp rỗng trước đó.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

   >>> p = re.compile('x*')
   >>> p.sub('-', 'abxd')
   '-a-b--d-'

Nếu *replacement* là một chuỗi, mọi escape bằng dấu gạch chéo ngược trong chuỗi sẽ được xử lý. Nghĩa là, ``\n`` được chuyển thành một ký tự xuống dòng, ``\r`` được chuyển thành ký tự xuống dòng đầu, v.v. Các escape không xác định như ``\&`` được giữ nguyên. Các tham chiếu ngược, chẳng hạn như ``\6``, được thay thế bằng chuỗi con khớp với nhóm tương ứng trong RE. Điều này cho phép bạn đưa các phần của văn bản gốc vào chuỗi thay thế kết quả.

Ví dụ này khớp với từ ``section`` theo sau bởi một chuỗi được đặt trong ``{``, ``}``, rồi thay đổi ``section`` thành ``subsection``::

   >>> p = re.compile('section{ ( [^}]* ) }', re.VERBOSE)
   >>> p.sub(r'subsection{\1}','section{First} section{second}')
   'subsection{First} subsection{second}'

Ngoài ra còn có cú pháp để tham chiếu đến các nhóm có tên được định nghĩa bằng cú pháp ``(?P<name>...)``. ``\g<name>`` sẽ sử dụng chuỗi con khớp với nhóm có tên ``name``, còn ``\g<number>`` sử dụng số nhóm tương ứng. Do đó, ``\g<2>`` tương đương với ``\2``, nhưng không gây mơ hồ trong một chuỗi thay thế như ``\g<2>0``. (``\20`` sẽ được diễn giải là tham chiếu đến nhóm 20, chứ không phải tham chiếu đến nhóm 2 theo sau bởi ký tự chữ ``'0'``.) Các phép thay thế sau đây đều tương đương, nhưng sử dụng cả ba biến thể của chuỗi thay thế.::

   >>> p = re.compile('section{ (?P<name> [^}]* ) }', re.VERBOSE)
   >>> p.sub(r'subsection{\1}','section{First}')
   'subsection{First}'
   >>> p.sub(r'subsection{\g<1>}','section{First}')
   'subsection{First}'
   >>> p.sub(r'subsection{\g<name>}','section{First}')
   'subsection{First}'

*replacement* cũng có thể là một hàm, cho phép bạn kiểm soát nhiều hơn. Nếu *replacement* là một hàm, hàm đó được gọi cho mỗi lần xuất hiện không chồng lấp của *pattern*. Trong mỗi lần gọi, hàm được truyền một
:ref:`match object <match-objects>` làm đối số cho kết quả khớp và có thể sử dụng thông tin này để tính toán chuỗi thay thế mong muốn rồi trả về chuỗi đó.

Trong ví dụ sau, hàm thay thế chuyển đổi các số thập phân thành hệ thập lục phân::

   >>> def hexrepl(match):
   ...     "Return the hex string for a decimal number"
   ...     value = int(match.group())
   ...     return hex(value)
   ...
   >>> p = re.compile(r'\d+')
   >>> p.sub(hexrepl, 'Call 65490 for printing, 49152 for user code.')
   'Call 0xffd2 for printing, 0xc000 for user code.'

Khi sử dụng hàm :func:`re.sub` ở cấp mô-đun, pattern được truyền làm đối số đầu tiên. Pattern có thể được cung cấp dưới dạng object hoặc string; nếu cần chỉ định các cờ của regular expression, bạn phải dùng pattern object làm tham số đầu tiên hoặc dùng các modifier nhúng trong pattern string, ví dụ ``sub("(?i)b+", "x", "bbbb BBBB")`` trả về ``'x x'``.


Các vấn đề thường gặp
=====================

Regular expression là một công cụ mạnh mẽ cho một số ứng dụng, nhưng trong một số trường hợp, hành vi của chúng không trực quan và đôi khi chúng không hoạt động theo cách bạn mong đợi. Phần này sẽ chỉ ra một số cạm bẫy thường gặp nhất.


Sử dụng các phương thức của string
----------------------------------

Đôi khi sử dụng module :mod:`re` là một sai lầm. Nếu bạn đang khớp một chuỗi cố định hoặc một lớp ký tự đơn, và không sử dụng bất kỳ tính năng :mod:`re` nào của :mod:`re` chẳng hạn như cờ :const:`~re.IGNORECASE`, thì có thể không cần đến toàn bộ sức mạnh của biểu thức chính quy. Chuỗi có một số phương thức để thực hiện các thao tác với chuỗi cố định và chúng thường nhanh hơn nhiều, vì phần triển khai chỉ là một vòng lặp C nhỏ được tối ưu hóa cho mục đích này, thay vì một regular expression engine lớn và tổng quát hơn.

Một ví dụ có thể là thay thế một chuỗi cố định bằng một chuỗi khác; chẳng hạn, bạn có thể thay ``word`` bằng ``deed``. :func:`re.sub` có vẻ là hàm cần dùng cho việc này, nhưng hãy cân nhắc phương thức :meth:`~str.replace`. Lưu ý rằng
:meth:`!replace` cũng sẽ thay thế ``word`` bên trong các từ, biến ``swordfish`` thành ``sdeedfish``, nhưng RE ngây thơ ``word`` cũng sẽ làm như vậy. (Để tránh thực hiện phép thay thế trên các phần của từ, mẫu sẽ phải là ``\bword\b``, nhằm yêu cầu ``word`` có word boundary ở cả hai bên. Điều này vượt quá khả năng của :meth:`!replace`.)

Một tác vụ phổ biến khác là xóa mọi lần xuất hiện của một ký tự đơn khỏi chuỗi hoặc thay thế ký tự đó bằng một ký tự đơn khác. Bạn có thể thực hiện việc này bằng cách nào đó như ``re.sub('\n', ' ', S)``, nhưng :meth:`~str.translate` có thể thực hiện cả hai tác vụ và sẽ nhanh hơn bất kỳ thao tác regular expression nào.

Tóm lại, trước khi chuyển sang module :mod:`re`, hãy cân nhắc xem vấn đề của bạn có thể được giải quyết bằng một phương thức chuỗi đơn giản và nhanh hơn hay không.


match() so với search()
-----------------------

Hàm :func:`~re.match` chỉ kiểm tra xem RE có khớp ở đầu chuỗi hay không, trong khi :func:`~re.search` sẽ quét về phía trước trong chuỗi để tìm kết quả khớp. Điều quan trọng là phải ghi nhớ sự khác biệt này. Hãy nhớ rằng :func:`!match` chỉ báo cáo một kết quả khớp thành công bắt đầu tại vị trí 0; nếu kết quả khớp không bắt đầu tại vị trí 0, :func:`!match` sẽ *không* báo cáo kết quả đó.::

   >>> print(re.match('super', 'superstition').span())
   (0, 5)
   >>> print(re.match('super', 'insuperable'))
   None

Mặt khác, :func:`~re.search` sẽ quét về phía trước trong chuỗi và báo cáo kết quả khớp đầu tiên mà nó tìm thấy.::

   >>> print(re.search('super', 'superstition').span())
   (0, 5)
   >>> print(re.search('super', 'insuperable').span())
   (2, 7)

Đôi khi bạn sẽ muốn tiếp tục sử dụng :func:`re.match` và chỉ cần thêm ``.*`` vào đầu RE của mình. Hãy cưỡng lại sự cám dỗ này và sử dụng :func:`re.search` thay vào đó. Trình biên dịch biểu thức chính quy thực hiện một số phân tích RE để tăng tốc quá trình tìm kết quả khớp. Một trong những phân tích đó xác định ký tự đầu tiên của kết quả khớp phải là gì; ví dụ: một mẫu bắt đầu bằng ``Crow`` phải bắt đầu bằng một ``'C'``. Phân tích này cho phép engine nhanh chóng quét qua chuỗi để tìm ký tự bắt đầu, chỉ thử khớp toàn bộ khi tìm thấy một ``'C'``.

Việc thêm ``.*`` sẽ vô hiệu hóa tối ưu hóa này, buộc phải quét đến cuối chuỗi rồi quay lui để tìm kết quả khớp cho phần còn lại của RE. Hãy sử dụng
:func:`re.search` thay vào đó.


Tham lam và không tham lam
--------------------------

Khi lặp lại một biểu thức chính quy, như trong ``a*``, thao tác thu được sẽ tiêu thụ nhiều nhất có thể của mẫu. Điều này thường gây rắc rối khi bạn cố khớp một cặp dấu phân cách cân bằng, chẳng hạn như dấu ngoặc nhọn bao quanh một thẻ HTML. Mẫu ngây thơ để khớp một thẻ HTML đơn không hoạt động vì tính chất tham lam của ``.*``.::

   >>> s = '<html><head><title>Title</title>'
   >>> len(s)
   32
   >>> print(re.match('<.*>', s).span())
   (0, 32)
   >>> print(re.match('<.*>', s).group())
   <html><head><title>Title</title>

RE khớp với ``'<'`` trong ``'<html>'``, còn ``.*`` tiêu thụ phần còn lại của chuỗi. Tuy nhiên, RE vẫn còn phần tiếp theo cần khớp, và ``>`` không thể khớp ở cuối chuỗi, nên engine biểu thức chính quy phải quay lui từng ký tự một cho đến khi tìm thấy kết quả khớp cho ``>``. Kết quả khớp cuối cùng kéo dài từ ``'<'`` trong ``'<html>'`` đến ``'>'`` trong ``'</title>'``, không phải điều bạn mong muốn.

Trong trường hợp này, giải pháp là sử dụng các quantifier non-greedy ``*?``, ``+?``, ``??`` hoặc ``{m,n}?``, vốn khớp với ít *little* văn bản nhất có thể. Trong ví dụ trên, ``'>'`` được thử ngay sau khi ``'<'`` đầu tiên khớp, và khi việc đó thất bại, engine tiến lên từng ký tự một, thử lại ``'>'`` ở mỗi bước. Kết quả thu được vừa đúng như mong muốn::

   >>> print(re.match('<.*?>', s).group())
   <html>

(Lưu ý rằng việc phân tích HTML hoặc XML bằng regular expression rất khó chịu. Các pattern nhanh và sơ sài sẽ xử lý được những trường hợp phổ biến, nhưng HTML và XML có những trường hợp đặc biệt sẽ làm hỏng regular expression hiển nhiên; đến khi bạn viết được một regular expression xử lý tất cả các trường hợp có thể xảy ra, các pattern sẽ trở nên *very* phức tạp. Hãy sử dụng một module parser HTML hoặc XML cho những tác vụ như vậy.)


Sử dụng re.VERBOSE
------------------

Đến lúc này, có lẽ bạn đã nhận thấy regular expression là một ký hiệu rất cô đọng, nhưng không thực sự dễ đọc. Các RE có độ phức tạp vừa phải có thể trở thành những chuỗi dài gồm dấu gạch chéo ngược, dấu ngoặc đơn và metacharacter, khiến chúng khó đọc và khó hiểu.

Với những RE như vậy, việc chỉ định cờ :const:`re.VERBOSE` khi biên dịch regular expression có thể hữu ích, vì nó cho phép bạn định dạng regular expression rõ ràng hơn.

Cờ ``re.VERBOSE`` có một số tác dụng. Khoảng trắng trong regular expression *isn't* nằm bên trong một character class sẽ bị bỏ qua. Điều này có nghĩa là một biểu thức như ``dog | cat`` tương đương với ``dog|cat`` khó đọc hơn, nhưng ``[a b]`` vẫn sẽ khớp với các ký tự ``'a'``, ``'b'`` hoặc một khoảng trắng. Ngoài ra, bạn cũng có thể đặt chú thích bên trong RE; chú thích kéo dài từ ký tự ``#`` đến dòng mới tiếp theo. Khi được sử dụng với chuỗi ba dấu ngoặc kép, tính năng này cho phép định dạng RE gọn gàng hơn::

   pat = re.compile(r"""
    \s*                 # Bỏ qua khoảng trắng ở đầu
    (?P<header>[^:]+)   # Tên header
    \s* :               # Khoảng trắng và dấu hai chấm
    (?P<value>.*?)      # Giá trị của header -- *? từng được dùng để
                        # làm mất khoảng trắng ở cuối theo sau
    \s*$                # Khoảng trắng ở cuối đến hết dòng
   """, re.VERBOSE)

Cách này dễ đọc hơn nhiều so với::

   pat = re.compile(r"\s*(?P<header>[^:]+)\s*:(?P<value>.*?)\s*$")


Phản hồi
========

Biểu thức chính quy là một chủ đề phức tạp. Tài liệu này có giúp bạn hiểu chúng không? Có phần nào chưa rõ hoặc vấn đề nào bạn gặp phải mà chưa được đề cập ở đây không? Nếu có, vui lòng gửi đề xuất cải thiện đến :ref:`issue tracker <using-the-tracker>`.

Cuốn sách đầy đủ nhất về biểu thức chính quy gần như chắc chắn là Mastering Regular Expressions của Jeffrey Friedl, do O'Reilly xuất bản. Đáng tiếc là sách chỉ tập trung vào các biến thể biểu thức chính quy của Perl và Java, hoàn toàn không có nội dung về Python, nên sẽ không hữu ích làm tài liệu tham khảo khi lập trình bằng Python. (Ấn bản đầu tiên có đề cập đến module :mod:`!regex` đã bị loại bỏ của Python, nhưng điều đó cũng không giúp ích nhiều cho bạn.) Hãy cân nhắc việc mượn sách từ thư viện.
