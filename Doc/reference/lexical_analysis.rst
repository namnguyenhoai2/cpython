
.. _lexical:

*****************
Phân tích từ vựng
*****************

.. index:: lexical analysis, parser, token

Một chương trình Python được đọc bởi *trình phân tích cú pháp*. Đầu vào của trình phân tích cú pháp là một luồng
:term:`token <token>`, được tạo bởi *trình phân tích từ vựng* (còn được gọi là *tokenizer*). Chương này mô tả cách trình phân tích từ vựng tạo ra các token này.

Trình phân tích từ vựng xác định :ref:`bảng mã <encodings>` của văn bản chương trình (UTF-8 theo mặc định) và giải mã văn bản thành
:ref:`ký tự nguồn <lexical-source-character>`. Nếu không thể giải mã văn bản, một :exc:`SyntaxError` sẽ được phát sinh.

Tiếp theo, trình phân tích từ vựng sử dụng các ký tự nguồn để tạo ra một luồng token. Loại của token được tạo thường phụ thuộc vào ký tự nguồn tiếp theo sẽ được xử lý. Tương tự, các hành vi đặc biệt khác của trình phân tích phụ thuộc vào ký tự nguồn đầu tiên chưa được xử lý. Bảng sau đây tóm tắt nhanh các ký tự nguồn này, kèm theo liên kết đến những phần chứa thêm thông tin.

.. list-table::
   :header-rows: 1

   * - Ký tự
     - Token tiếp theo (hoặc tài liệu liên quan khác)

   * - * khoảng trắng
       * tab
       * formfeed
     - * :ref:`Khoảng trắng <whitespace>`

   * - * CR, LF
     - * :ref:`Dòng mới <line-structure>`
       * :ref:`Thụt lề <indentation>`

   * - * dấu gạch chéo ngược (``\``)
     - * :ref:`Nối dòng tường minh <explicit-joining>`
       * (Cũng có ý nghĩa trong :ref:`chuỗi escape <escape-sequences>`)

   * - * dấu thăng (``#``)
     - * :ref:`Chú thích <comments>`

   * - * dấu nháy (``'``, ``"``)
     - * :ref:`Literal chuỗi <strings>`

   * - * chữ cái ASCII (``a``-``z``, ``A``-``Z``)
       * ký tự non-ASCII
     - * :ref:`Tên <identifiers>`
       * literal chuỗi hoặc bytes có tiền tố :ref:` <strings>`

   * - * dấu gạch dưới (``_``)
     - * :ref:`Tên <identifiers>`
       * (Cũng có thể là một phần của :ref:`literal số <numbers>`)

   * - * số (``0``-``9``)
     - * :ref:`Literal số <numbers>`

   * - * dấu chấm (``.``)
     - * :ref:`Literal số <numbers>`
       * :ref:`Toán tử <operators>`

   * - * dấu chấm hỏi (``?``)
       * đô la (``$``)
       ***************
         .. (the following uses zero-width space characters to render
         .. a literal backquote)

         dấu nháy ngược (``​`​``)
       * ký tự điều khiển
     - * Lỗi (bên ngoài các literal chuỗi và chú thích)

   * - * ký tự in được khác
     - * :ref:`Toán tử hoặc dấu phân cách <operators>`

   * - * cuối tệp
     - * :ref:`Dấu kết thúc <endmarker-token>`


.. _line-structure:

Cấu trúc dòng
=============

.. index:: line structure

Một chương trình Python được chia thành một số *dòng logic*.


.. _logical-lines:

Các dòng logic
--------------

.. index:: logical line, physical line, line joining, NEWLINE token

Kết thúc của một dòng logic được biểu diễn bằng token :data:`~token.NEWLINE`. Các câu lệnh không thể vượt qua ranh giới dòng logic, ngoại trừ khi :data:`!NEWLINE` được cú pháp cho phép (ví dụ: giữa các câu lệnh trong câu lệnh phức hợp). Một dòng logic được tạo thành từ một hoặc nhiều *dòng vật lý* bằng cách tuân theo các quy tắc :ref:`nối dòng <explicit-joining>` :ref:`tường minh <implicit-joining>` hoặc *ngầm định*.


.. _physical-lines:

Các dòng vật lý
---------------

Một dòng vật lý là một chuỗi ký tự được kết thúc bằng một trong các chuỗi kết thúc dòng sau đây:

* dạng Unix sử dụng ASCII LF (linefeed),
* dạng Windows sử dụng chuỗi ASCII CR LF (return theo sau là linefeed),
* dạng '`Classic Mac OS`__' sử dụng ký tự ASCII CR (return).

  __ https://en.wikipedia.org/wiki/Classic_Mac_OS

Bất kể nền tảng nào, mỗi chuỗi này đều được thay thế bằng một ký tự ASCII LF (linefeed) duy nhất. (Việc này cũng được thực hiện bên trong :ref:`string literals <strings>`.) Mỗi dòng có thể sử dụng bất kỳ chuỗi nào; chúng không cần phải nhất quán trong một tệp.

Phần cuối của đầu vào cũng đóng vai trò là dấu kết thúc ngầm định cho dòng vật lý cuối cùng.

Về mặt hình thức:

.. grammar-snippet::
   :group: python-grammar

   newline: <ASCII LF> | <ASCII CR> <ASCII LF> | <ASCII CR>


.. _comments:

Chú thích
---------

.. index:: comment, hash character
   single: # (hash); comment

Một chú thích bắt đầu bằng ký tự dấu thăng (``#``) không nằm trong literal chuỗi và kết thúc ở cuối dòng vật lý. Một chú thích biểu thị kết thúc của dòng logic, trừ khi các quy tắc nối dòng ngầm được áp dụng. Chú thích bị cú pháp bỏ qua.


.. _encodings:

Khai báo encoding
-----------------

.. index:: source character set, encoding declarations (source file)
   single: # (hash); source encoding declaration

Nếu một chú thích ở dòng đầu tiên hoặc dòng thứ hai của tập lệnh Python khớp với biểu thức chính quy ``coding[=:]\s*([-\w.]+)``, chú thích này được xử lý như một khai báo encoding; nhóm đầu tiên của biểu thức này chỉ rõ encoding của tệp mã nguồn. Khai báo encoding phải nằm trên một dòng riêng. Nếu nằm ở dòng thứ hai, dòng đầu tiên cũng phải là một dòng chỉ chứa chú thích. Các dạng được khuyến nghị của biểu thức encoding là::

   # -*- coding: <encoding-name> -*-

biểu thức này cũng được GNU Emacs nhận dạng, và::

   # vim:fileencoding=<encoding-name>

được Bram Moolenaar's VIM nhận dạng.

Nếu không tìm thấy khai báo encoding, encoding mặc định là UTF-8. Nếu encoding ngầm định hoặc tường minh của một tệp là UTF-8, dấu thứ tự byte UTF-8 ban đầu (``b'\xef\xbb\xbf'``) sẽ bị bỏ qua thay vì gây ra lỗi cú pháp.

Nếu một encoding được khai báo, tên encoding đó phải được Python nhận dạng (xem :ref:`standard-encodings`). Encoding này được sử dụng cho mọi quá trình phân tích từ vựng, bao gồm các string literal, comment và identifier.

.. _lexical-source-character:

Mọi quá trình phân tích từ vựng, bao gồm các string literal, comment và identifier, đều hoạt động trên văn bản Unicode được giải mã bằng encoding nguồn. Bất kỳ code point Unicode nào, ngoại trừ ký tự điều khiển NUL, đều có thể xuất hiện trong mã nguồn Python.

.. grammar-snippet::
   :group: python-grammar

   source_character:  <any Unicode code point, except NUL>


.. _explicit-joining:

Nối dòng tường minh
-------------------

.. index:: physical line, line joining, line continuation, backslash character

Có thể nối hai hoặc nhiều dòng vật lý thành các dòng logic bằng ký tự backslash (``\``), như sau: khi một dòng vật lý kết thúc bằng backslash không thuộc một string literal hoặc comment, dòng đó được nối với dòng tiếp theo để tạo thành một dòng logic duy nhất, đồng thời xóa backslash và ký tự kết thúc dòng theo sau. Ví dụ::

   if 1900 < year < 2100 and 1 <= month <= 12 \
      and 1 <= day <= 31 and 0 <= hour < 24 \
      and 0 <= minute < 60 and 0 <= second < 60:   # Trông giống một ngày hợp lệ
           return 1

Một dòng kết thúc bằng backslash không thể chứa comment. Backslash không tiếp tục một comment. Backslash không tiếp tục một token, ngoại trừ string literal (tức là các token khác string literal không thể được tách qua nhiều dòng vật lý bằng backslash). Backslash là bất hợp lệ ở mọi vị trí khác trên một dòng bên ngoài string literal.


.. _implicit-joining:

Nối dòng ngầm định
------------------

Các biểu thức trong dấu ngoặc tròn, ngoặc vuông hoặc ngoặc nhọn có thể được tách thành nhiều dòng vật lý mà không cần sử dụng dấu gạch chéo ngược. Ví dụ::

   month_names = ['Januari', 'Februari', 'Maart',      # Đây là
                  'April',   'Mei',      'Juni',       # tên tiếng Hà Lan
                  'Juli',    'Augustus', 'September',  # của các tháng
                  'Oktober', 'November', 'December']   # trong năm

Các dòng được tiếp tục ngầm định có thể chứa chú thích. Thụt lề của các dòng tiếp tục không quan trọng. Có thể có các dòng tiếp tục trống. Không có mã thông báo NEWLINE giữa các dòng tiếp tục ngầm định. Các dòng được tiếp tục ngầm định cũng có thể xuất hiện trong chuỗi được đặt trong ba dấu ngoặc kép (xem bên dưới); trong trường hợp đó, chúng không thể chứa chú thích.


.. _blank-lines:

Dòng trống
----------

.. index:: single: blank line

Một dòng logic chỉ chứa khoảng trắng, tab, ký tự xuống trang và có thể có chú thích sẽ bị bỏ qua (tức là không tạo ra token :data:`~token.NEWLINE`). Trong khi nhập tương tác các câu lệnh, việc xử lý một dòng trống có thể khác nhau tùy thuộc vào cách triển khai vòng lặp đọc-đánh giá-in kết quả. Trong trình thông dịch tương tác tiêu chuẩn, một dòng logic hoàn toàn trống (nghĩa là không chứa dù chỉ khoảng trắng hoặc chú thích) sẽ kết thúc một câu lệnh nhiều dòng.


.. _indentation:

Thụt lề
-------

.. index:: indentation, leading whitespace, space, tab, grouping, statement grouping

Khoảng trắng ở đầu (dấu cách và tab) tại phần đầu của một dòng logic được dùng để tính mức thụt lề của dòng, từ đó xác định cách nhóm các câu lệnh.

Các tab được thay thế (từ trái sang phải) bằng từ một đến tám dấu cách sao cho tổng số ký tự tính đến và bao gồm cả phần thay thế là một bội số của tám (quy tắc này nhằm giống với quy tắc được Unix sử dụng). Sau đó, tổng số dấu cách đứng trước ký tự không trống đầu tiên sẽ xác định mức thụt lề của dòng. Không thể chia phần thụt lề trên nhiều dòng vật lý bằng cách sử dụng dấu gạch chéo ngược; khoảng trắng trước dấu gạch chéo ngược đầu tiên sẽ xác định mức thụt lề.

Thụt lề sẽ bị từ chối là không nhất quán nếu một tệp nguồn trộn tab và dấu cách theo cách khiến ý nghĩa phụ thuộc vào giá trị của một tab tính theo dấu cách; một
:exc:`TabError` được phát sinh trong trường hợp đó.

**Lưu ý về tính tương thích đa nền tảng:** do đặc điểm của các trình soạn thảo văn bản trên những nền tảng không phải UNIX, không nên sử dụng kết hợp dấu cách và tab để thụt lề trong cùng một tệp mã nguồn. Cũng cần lưu ý rằng các nền tảng khác nhau có thể giới hạn rõ ràng mức thụt lề tối đa.

Một ký tự formfeed có thể xuất hiện ở đầu dòng; ký tự này sẽ bị bỏ qua trong các phép tính thụt lề ở trên. Các ký tự formfeed xuất hiện ở vị trí khác trong khoảng trắng đầu dòng có tác động không xác định (chẳng hạn, chúng có thể đặt lại số lượng dấu cách về 0).

.. index:: INDENT token, DEDENT token

Các mức thụt lề của những dòng liên tiếp được dùng để tạo ra
:data:`~token.INDENT` và :data:`~token.DEDENT` token, bằng cách sử dụng một stack, như sau.

Trước khi đọc dòng đầu tiên của tệp, một số 0 duy nhất được đẩy vào stack; số này sẽ không bao giờ bị lấy ra. Các số được đẩy vào stack luôn tăng nghiêm ngặt từ dưới lên trên. Khi bắt đầu mỗi dòng logic, mức thụt lề của dòng được so sánh với đỉnh stack. Nếu bằng nhau thì không có gì xảy ra. Nếu lớn hơn, mức đó được đẩy vào stack và một token :data:`!INDENT` được tạo ra. Nếu nhỏ hơn, nó *phải* là một trong các số xuất hiện trên stack; tất cả các số trên stack lớn hơn nó sẽ được lấy ra, và với mỗi số được lấy ra, một token :data:`!DEDENT` được tạo ra. Khi kết thúc tệp, một token :data:`!DEDENT` được tạo ra cho mỗi số còn lại trên stack lớn hơn 0.

Dưới đây là một đoạn mã Python được thụt lề đúng (mặc dù khá khó hiểu)::

   def perm(l):
           # Tính danh sách tất cả các hoán vị của l
       if len(l) <= 1:
                     return [l]
       r = []
       for i in range(len(l)):
                s = l[:i] + l[i+1:]
                p = perm(s)
                for x in p:
                 r.append(l[i:i+1] + x)
       return r

Ví dụ sau đây cho thấy nhiều lỗi thụt lề khác nhau::

    def perm(l):                       # lỗi: dòng đầu tiên bị thụt lề
   for i in range(len(l)):             # lỗi: không được thụt lề
       s = l[:i] + l[i+1:]
           p = perm(l[:i] + l[i+1:])   # lỗi: thụt lề không mong đợi
           for x in p:
                   r.append(l[i:i+1] + x)
               return r                # lỗi: giảm thụt lề không nhất quán

(Thực ra, ba lỗi đầu tiên được parser phát hiện; chỉ lỗi cuối cùng được lexical analyzer tìm thấy --- mức thụt lề của ``return r`` không khớp với một mức đã được lấy ra khỏi ngăn xếp.)


.. _whitespace:

Khoảng trắng giữa các token
---------------------------

Ngoại trừ ở đầu một dòng logic hoặc trong chuỗi ký tự, các ký tự khoảng trắng space, tab và formfeed có thể được sử dụng thay thế cho nhau để phân tách các token:

.. grammar-snippet::
   :group: python-grammar

   whitespace:  ' ' | tab | formfeed


Khoảng trắng chỉ cần thiết giữa hai token nếu việc nối chúng lại có thể bị diễn giải thành một token khác. Ví dụ, ``ab`` là một token, nhưng ``a b`` là hai token. Tuy nhiên, ``+a`` và ``+ a`` đều tạo ra hai token, ``+`` và ``a``, vì ``+a`` không phải là một token hợp lệ.


.. _endmarker-token:

Dấu kết thúc
------------

Ở cuối dữ liệu đầu vào không tương tác, bộ phân tích từ vựng tạo ra một
:data:`~token.ENDMARKER` token.


.. _other-tokens:

Các token khác
==============

Ngoài :data:`~token.NEWLINE`, :data:`~token.INDENT` và :data:`~token.DEDENT`, còn có các nhóm token sau: *định danh* và *từ khóa* (:data:`~token.NAME`), *literal* (chẳng hạn như
:data:`~token.NUMBER` và :data:`~token.STRING`), cùng các ký hiệu khác (*toán tử* và *dấu phân cách*, :data:`~token.OP`). Các ký tự khoảng trắng (ngoại trừ các ký tự kết thúc dòng logic đã được thảo luận trước đó) không phải là token nhưng được dùng để phân cách các token. Khi có sự mơ hồ, một token bao gồm chuỗi dài nhất có thể tạo thành một token hợp lệ khi được đọc từ trái sang phải.


.. _identifiers:

Tên (identifier và keyword)
===========================

.. index:: identifier, name

Các token :data:`~token.NAME` đại diện cho *identifier*, *keyword*, và *soft keyword*.

Tên được tạo thành từ các ký tự sau:

* các chữ cái viết hoa và viết thường (``A-Z`` và ``a-z``),
* dấu gạch dưới (``_``),
* các chữ số (``0`` đến ``9``), không thể xuất hiện ở ký tự đầu tiên, và
* các ký tự non-ASCII. Tên hợp lệ chỉ có thể chứa các ký tự dạng chữ và dạng chữ số; xem :ref:`lexical-names-nonascii` để biết chi tiết.

Tên phải chứa ít nhất một ký tự, nhưng không có giới hạn độ dài tối đa. Phân biệt chữ hoa và chữ thường.

Về mặt hình thức, tên được mô tả bằng các định nghĩa từ vựng sau:

.. grammar-snippet::
   :group: python-grammar

   NAME:          `name_start` `name_continue`*
   name_start:    "a"..."z" | "A"..."Z" | "_" | <non-ASCII character>
   name_continue: name_start | "0"..."9"
   identifier:    <`NAME`, except keywords>

Lưu ý rằng không phải mọi tên khớp với ngữ pháp này đều hợp lệ; xem
:ref:`lexical-names-nonascii` để biết chi tiết.


.. _keywords:

Từ khóa
-------

.. index::
   single: keyword
   single: reserved word

Các tên sau đây được dùng làm từ dành riêng, hay *từ khóa* của ngôn ngữ, và không thể được dùng làm identifier thông thường. Chúng phải được viết chính xác như dưới đây:

.. sourcecode:: text

   False      await      else       import     pass
   None       break      except     in         raise
   True       class      finally    is         return
   and        continue   for        lambda     try
   as         def        from       nonlocal   while
   assert     del        global     not        with
   async      elif       if         or         yield


.. _soft-keywords:

Từ khóa mềm
-----------

.. index:: soft keyword, keyword

.. versionadded:: 3.10

Một số tên chỉ được dành riêng trong các ngữ cảnh cụ thể. Những tên này được gọi là *từ khóa mềm*:

- ``match``, ``case`` và ``_`` khi được sử dụng trong câu lệnh :keyword:`match`.
- ``type`` khi được sử dụng trong câu lệnh :keyword:`type`.

Về mặt cú pháp, chúng hoạt động như các từ khóa trong những ngữ cảnh cụ thể, nhưng sự phân biệt này được thực hiện ở cấp parser, không phải khi token hóa.

Là các từ khóa mềm, chúng có thể được sử dụng trong grammar mà vẫn duy trì khả năng tương thích với mã hiện có sử dụng những tên này làm tên identifier.

.. versionchanged:: 3.12
   ``type`` hiện là một từ khóa mềm.

.. index::
   single: _, identifiers
   single: __, identifiers
.. _id-classes:

Các lớp định danh dành riêng
----------------------------

Một số lớp định danh (ngoài từ khóa) có ý nghĩa đặc biệt. Các lớp này được xác định bởi các mẫu ký tự gạch dưới ở đầu và cuối:

``_*``
   Không được ``from module import *`` nhập.

``_``
   Trong một mẫu ``case`` thuộc một câu lệnh :keyword:`match`, ``_`` là một
   :ref:`từ khóa mềm <soft-keywords>` biểu thị một
   :ref:`ký tự đại diện <wildcard-patterns>`.

   Ngoài ra, trình thông dịch tương tác cung cấp kết quả của lần đánh giá cuối cùng trong biến ``_``. (Biến này được lưu trữ trong mô-đun :mod:`builtins`, cùng với các hàm dựng sẵn như ``print``.)

   Ở nơi khác, ``_`` là một định danh thông thường. Nó thường được dùng để đặt tên cho các mục "đặc biệt", nhưng bản thân Python không coi nó là đặc biệt.

   .. note::

      Tên ``_`` thường được sử dụng cùng với internationalization; hãy tham khảo tài liệu về mô-đun :mod:`gettext` để biết thêm thông tin về quy ước này.

      Nó cũng thường được dùng cho các biến không được sử dụng.

``__*__``
   Các tên do hệ thống định nghĩa, thường được gọi không chính thức là tên "dunder". Những tên này được trình thông dịch và phần triển khai của nó (bao gồm cả standard library) định nghĩa. Các tên hệ thống hiện tại được thảo luận trong phần :ref:`specialnames` và ở những nơi khác. Có khả năng sẽ có thêm các tên được định nghĩa trong những phiên bản Python tương lai. *Mọi* việc sử dụng các tên ``__*__``, trong bất kỳ ngữ cảnh nào, không tuân theo cách sử dụng được ghi rõ trong tài liệu, đều có thể bị phá vỡ mà không được cảnh báo.

``__*``
   Tên riêng của lớp. Các tên thuộc danh mục này, khi được sử dụng trong ngữ cảnh của một định nghĩa lớp, sẽ được viết lại ở dạng đã được biến đổi để giúp tránh xung đột tên giữa các thuộc tính "riêng" của lớp cơ sở và lớp dẫn xuất. Xem phần
   :ref:`atom-identifiers`.


.. _lexical-names-nonascii:

Các ký tự không thuộc ASCII trong tên
-------------------------------------

Các tên chứa ký tự không thuộc ASCII cần được chuẩn hóa và xác thực bổ sung ngoài các quy tắc và ngữ pháp đã giải thích
:ref:`ở trên <identifiers>`. Ví dụ: ``ř_1``, ``蛇`` hoặc ``साँप`` là những tên hợp lệ, nhưng ``r〰2``, ``€`` hoặc ``🐍`` thì không.

Phần này giải thích các quy tắc chính xác.

Khi phân tích cú pháp, tất cả tên đều được chuyển sang `dạng chuẩn hóa <normalization form_>`_ NFKC. Điều này có nghĩa là, chẳng hạn, một số biến thể kiểu chữ của các ký tự sẽ được chuyển thành dạng "cơ bản" của chúng. Ví dụ, ``ﬁⁿₐˡᵢᶻₐᵗᵢᵒₙ`` được chuẩn hóa thành ``finalization``, vì vậy Python coi chúng là cùng một tên::

   >>> ﬁⁿₐˡᵢᶻₐᵗᵢᵒₙ = 3
   >>> finalization
   3

.. note::

   Việc chuẩn hóa chỉ được thực hiện ở cấp độ từ vựng. Các hàm run-time nhận tên dưới dạng *chuỗi* thường không chuẩn hóa các đối số của chúng. Ví dụ: biến được định nghĩa ở trên có thể được truy cập khi run-time trong
   :func:`globals` từ điển với tên ``globals()["finalization"]`` nhưng không phải ``globals()["ﬁⁿₐˡᵢᶻₐᵗᵢᵒₙ"]``.

Tương tự như việc tên chỉ chứa ASCII phải chỉ gồm chữ cái, chữ số và dấu gạch dưới, đồng thời không được bắt đầu bằng chữ số, một tên hợp lệ phải bắt đầu bằng một ký tự thuộc tập "giống chữ cái" ``xid_start``, còn các ký tự còn lại phải thuộc tập "giống chữ cái và chữ số" ``xid_continue``.

Các tập này dựa trên các tập *XID_Start* và *XID_Continue* được định nghĩa trong phụ lục `UAX-31`_ của tiêu chuẩn Unicode. ``xid_start`` của Python còn bao gồm cả dấu gạch dưới (``_``). Lưu ý rằng Python không nhất thiết tuân thủ `UAX-31`_.

Danh sách không mang tính quy phạm về các ký tự trong các tập hợp *XID_Start* và *XID_Continue* được Unicode định nghĩa có trong tệp `DerivedCoreProperties.txt`_ thuộc Unicode Character Database. Để tham khảo, các quy tắc xây dựng cho các tập hợp ``xid_*`` được nêu dưới đây.

Tập hợp ``id_start`` được định nghĩa là hợp của:

* Danh mục Unicode ``<Lu>`` - chữ cái viết hoa (bao gồm ``A`` đến ``Z``)​​
* Danh mục Unicode ``<Ll>`` - chữ cái viết thường (bao gồm ``a`` đến ``z``)​​
* Danh mục Unicode ``<Lt>`` - chữ cái viết hoa đầu từ
* Danh mục Unicode ``<Lm>`` - chữ cái bổ nghĩa
* Danh mục Unicode ``<Lo>`` - các chữ cái khác
* Danh mục Unicode ``<Nl>`` - số dạng chữ cái
* {``"_"``} - dấu gạch dưới
* ``<Other_ID_Start>`` - một tập hợp ký tự cụ thể trong `PropList.txt`_ để hỗ trợ khả năng tương thích ngược

Sau đó, tập hợp ``xid_start`` đóng tập hợp này dưới phép chuẩn hóa NFKC bằng cách loại bỏ tất cả các ký tự có dạng chuẩn hóa không phải là ``id_start id_continue*``.

Tập hợp ``id_continue`` được định nghĩa là hợp của:

* ``id_start`` (xem ở trên)
* Danh mục Unicode ``<Nd>`` - số thập phân (bao gồm ``0`` đến ``9``)
* Danh mục Unicode ``<Pc>`` - dấu câu nối
* Danh mục Unicode ``<Mn>`` - dấu không chiếm khoảng cách
* Danh mục Unicode ``<Mc>`` - dấu kết hợp có khoảng cách
* ``<Other_ID_Continue>`` - một tập hợp ký tự rõ ràng khác trong `PropList.txt`_ để hỗ trợ khả năng tương thích ngược

Một lần nữa, ``xid_continue`` khép kín tập hợp này theo chuẩn hóa NFKC.

Các danh mục Unicode sử dụng phiên bản của Cơ sở dữ liệu ký tự Unicode được tích hợp trong mô-đun :mod:`unicodedata`.

.. _UAX-31: https://www.unicode.org/reports/tr31/
.. _PropList.txt: https://www.unicode.org/Public/16.0.0/ucd/PropList.txt
.. _DerivedCoreProperties.txt: https://www.unicode.org/Public/16.0.0/ucd/DerivedCoreProperties.txt
.. _normalization form: https://www.unicode.org/reports/tr15/#Norm_Forms

.. seealso::

   * :pep:`3131` -- Hỗ trợ các định danh không phải ASCII
   * :pep:`672` -- Các lưu ý về bảo mật liên quan đến Unicode cho Python


.. _literals:

Literals
========

.. index:: literal, constant

Literals là các ký hiệu biểu thị giá trị hằng của một số kiểu tích hợp sẵn.

Xét về phương diện phân tích từ vựng, Python có literal :ref:`string, bytes <strings>` và :ref:`numeric <numbers>`.

Các "literal" khác được biểu thị về mặt từ vựng bằng :ref:`từ khóa <keywords>` (``None``, ``True``, ``False``) và
:ref:`token dấu ba chấm <lexical-ellipsis>` (``...``).


.. index:: string literal, bytes literal, ASCII
   single: ' (single quote); string literal
   single: " (double quote); string literal
.. _strings:

Literal String và Bytes
=======================

Chuỗi ký tự dạng literal là phần văn bản được đặt trong dấu nháy đơn (``'``) hoặc dấu nháy kép (``"``). Ví dụ:

.. code-block:: python

   "spam"
   'eggs'

Dấu nháy được dùng để bắt đầu literal cũng kết thúc literal đó, vì vậy một chuỗi ký tự dạng literal chỉ có thể chứa loại dấu nháy còn lại (trừ khi sử dụng escape sequence, xem bên dưới). Ví dụ:

.. code-block:: python

   'Say "Hello", please.'
   "Don't do that!"

Ngoài giới hạn này, việc chọn ký tự dấu nháy (``'`` hoặc ``"``) không ảnh hưởng đến cách literal được phân tích cú pháp.

Bên trong chuỗi ký tự dạng literal, ký tự dấu gạch chéo ngược (``\``) mở đầu cho một
:dfn:`escape sequence`, có ý nghĩa đặc biệt tùy thuộc vào ký tự đứng sau dấu gạch chéo ngược. Ví dụ, ``\"`` biểu thị ký tự dấu nháy kép và *not* kết thúc chuỗi:

.. code-block:: pycon

   >>> print("Say \"Hello\" to everyone!")
   Say "Hello" to everyone!

Xem :ref:`escape sequences <escape-sequences>` bên dưới để biết danh sách đầy đủ các sequence này cùng thông tin chi tiết hơn.


.. index:: triple-quoted string
   single: """; string literal
   single: '''; string literal

Chuỗi được đặt trong ba dấu nháy
--------------------------------

Chuỗi cũng có thể được đặt trong các nhóm gồm ba dấu nháy đơn hoặc dấu nháy kép tương ứng. Những chuỗi này thường được gọi là :dfn:`chuỗi ba dấu nháy`::

   """This is a triple-quoted string."""

Trong các literal ba dấu nháy, dấu nháy chưa được escape được phép sử dụng (và được giữ nguyên), ngoại trừ trường hợp ba dấu nháy chưa được escape liên tiếp sẽ kết thúc literal, nếu chúng cùng loại (``'`` hoặc ``"``) với loại được dùng ở phần bắt đầu::

   """This string has "quotes" inside."""

Các ký tự xuống dòng chưa được escape cũng được phép sử dụng và được giữ nguyên::

   '''This triple-quoted string
   continues on the next line.'''


.. index::
   single: u'; string literal
   single: u"; string literal

Tiền tố chuỗi
-------------

Các literal chuỗi có thể có :dfn:`tiền tố` tùy chọn, tiền tố này ảnh hưởng đến cách nội dung của literal được phân tích, ví dụ:

.. code-block:: python

   b"data"
   f'{result=}'

Các tiền tố được phép là:

* ``b``: :ref:`Bytes literal <bytes-literal>`
* ``r``: :ref:`Chuỗi thô <raw-strings>`
* ``f``: :ref:`Literal chuỗi có định dạng <f-strings>` ("f-string")
* ``t``: :ref:`Literal chuỗi mẫu <t-strings>` ("t-string")
* ``u``: Không có tác dụng (được cho phép để duy trì khả năng tương thích ngược)

Xem các phần được liên kết để biết chi tiết về từng loại.

Các tiền tố không phân biệt chữ hoa chữ thường (ví dụ: '``B``' hoạt động giống như '``b``'). Tiền tố '``r``' có thể được kết hợp với '``f``', '``t``' hoặc '``b``', vì vậy '``fr``', '``rf``', '``tr``', '``rt``', '``br``' và '``rb``' cũng là các tiền tố hợp lệ.

.. versionadded:: 3.3
   Tiền tố ``'rb'`` của literal bytes thô đã được thêm vào như một từ đồng nghĩa của ``'br'``.

   Hỗ trợ cho literal unicode kiểu cũ (``u'value'``) đã được đưa trở lại để đơn giản hóa việc duy trì các codebase đồng thời tương thích với Python 2.x và 3.x. Xem :pep:`414` để biết thêm thông tin.


Ngữ pháp hình thức
------------------

Các literal chuỗi, ngoại trừ :ref:`"f-strings" <f-strings>` và
:ref:`"t-strings" <t-strings>`, được mô tả bằng các định nghĩa từ vựng sau.

Các định nghĩa này sử dụng :ref:`lookahead phủ định <lexical-lookaheads>` (``!``) để chỉ ra rằng dấu ngoặc kép kết thúc sẽ kết thúc literal.

.. grammar-snippet::
   :group: python-grammar

   STRING:          [`stringprefix`] (`stringcontent`)
   stringprefix:    <("r" | "u" | "b" | "br" | "rb"), case-insensitive>
   stringcontent:
      | "'''" ( !"'''" `longstringitem`)* "'''"
      | '"""' ( !'"""' `longstringitem`)* '"""'
      | "'" ( !"'" `stringitem`)* "'"
      | '"' ( !'"' `stringitem`)* '"'
   stringitem:      `stringchar` | `stringescapeseq`
   stringchar:      <any `source_character`, except backslash and newline>
   longstringitem:  `stringitem` | newline
   stringescapeseq: "\" <any `source_character`>

Lưu ý rằng, cũng như trong mọi định nghĩa từ vựng, khoảng trắng có ý nghĩa. Cụ thể, tiền tố (nếu có) phải ngay lập tức theo sau dấu ngoặc kép mở đầu.

.. index:: physical line, escape sequence, Standard C, C
   single: \ (backslash); escape sequence
   single: \\; escape sequence
   single: \a; escape sequence
   single: \b; escape sequence
   single: \f; escape sequence
   single: \n; escape sequence
   single: \r; escape sequence
   single: \t; escape sequence
   single: \v; escape sequence
   single: \x; escape sequence
   single: \N; escape sequence
   single: \u; escape sequence
   single: \U; escape sequence

.. _escape-sequences:

Chuỗi escape
------------

Nếu không có tiền tố '``r``' hoặc '``R``', các escape sequence trong literal chuỗi và bytes được diễn giải theo những quy tắc tương tự các quy tắc được Standard C sử dụng. Các escape sequence được nhận dạng là:

.. list-table::
   :widths: auto
   :header-rows: 1

   * * Escape sequence
     * Ý nghĩa
   * * ``\``\ <newline>
     * :ref:`string-escape-ignore`
   * * ``\\``
     * :ref:`Dấu gạch chéo ngược <string-escape-escaped-char>`
   * * ``\'``
     * :ref:`Dấu nháy đơn <string-escape-escaped-char>`
   * * ``\"``
     * :ref:`Dấu nháy kép <string-escape-escaped-char>`
   * * ``\a``
     * Chuông ASCII (BEL)
   * * ``\b``
     * Xóa lùi ASCII (BS)
   * * ``\f``
     * Đổi trang ASCII (FF)
   * * ``\n``
     * Xuống dòng ASCII (LF)
   * * ``\r``
     * Về đầu dòng ASCII (CR)
   * * ``\t``
     * Tab ngang ASCII (TAB)
   * * ``\v``
     * Tab dọc ASCII (VT)
   * * :samp:`\\\\{ooo}`
     * :ref:`string-escape-oct`
   * * :samp:`\\x{hh}`
     * :ref:`string-escape-hex`
   * * :samp:`\\N\\{{name}\\}`
     * :ref:`string-escape-named`
   * * :samp:`\\u{xxxx}`
     * :ref:`Ký tự Unicode thập lục phân <string-escape-long-hex>`
   * * :samp:`\\U{xxxxxxxx}`
     * :ref:`Ký tự Unicode thập lục phân <string-escape-long-hex>`

.. _string-escape-ignore:

Bỏ qua cuối dòng
^^^^^^^^^^^^^^^^

Có thể thêm dấu gạch chéo ngược ở cuối dòng để bỏ qua ký tự xuống dòng::

   >>> 'This string will not include \
   ... backslashes or newline characters.'
   'This string will not include backslashes or newline characters.'

Có thể đạt được kết quả tương tự bằng cách sử dụng :ref:`chuỗi được đặt trong ba dấu nháy <strings>`, hoặc dấu ngoặc đơn và :ref:`phép nối literal chuỗi <string-concatenation>`.

.. _string-escape-escaped-char:

Các ký tự được escape
^^^^^^^^^^^^^^^^^^^^^

Để đưa dấu gạch chéo ngược vào một string literal Python không phải :ref:`raw <raw-strings>`, cần viết nó hai lần. Chuỗi escape ``\\`` biểu thị một ký tự gạch chéo ngược duy nhất::

   >>> print('C:\\Program Files')
   C:\Program Files

Tương tự, các chuỗi ``\'`` và ``\"`` lần lượt biểu thị ký tự dấu nháy đơn và dấu nháy kép::

   >>> print('\' and \"')
   ' and "

.. _string-escape-oct:

Ký tự bát phân
^^^^^^^^^^^^^^

Chuỗi :samp:`\\\\{ooo}` biểu thị một *ký tự* có giá trị bát phân (cơ số 8) là *ooo*::

   >>> '\120'
   'P'

Chấp nhận tối đa ba chữ số bát phân (từ 0 đến 7).

Trong một bytes literal, *ký tự* biểu thị một *byte* có giá trị đã cho. Trong một string literal, nó biểu thị một ký tự Unicode có giá trị đã cho.

.. versionchanged:: 3.11
   Các escape bát phân có giá trị lớn hơn ``0o377`` (255) sẽ tạo ra một
   :exc:`DeprecationWarning`.

.. versionchanged:: 3.12
   Các escape bát phân có giá trị lớn hơn ``0o377`` (255) sẽ tạo ra một
   :exc:`SyntaxWarning`. Trong một phiên bản Python trong tương lai, chúng sẽ phát sinh :exc:`SyntaxError`.

.. _string-escape-hex:

Ký tự thập lục phân
^^^^^^^^^^^^^^^^^^^

Chuỗi :samp:`\\x{hh}` biểu thị một *ký tự* có giá trị hex (cơ số 16) là *hh*::

   >>> '\x50'
   'P'

Khác với Standard C, bắt buộc phải có chính xác hai chữ số hex.

Trong một bytes literal, *character* có nghĩa là một *byte* với giá trị đã cho. Trong một string literal, nó có nghĩa là một ký tự Unicode với giá trị đã cho.

.. _string-escape-named:

Ký tự Unicode có tên
^^^^^^^^^^^^^^^^^^^^

Chuỗi :samp:`\\N\\{{name}\\}` biểu thị một ký tự Unicode với *tên* đã cho::

   >>> '\N{LATIN CAPITAL LETTER P}'
   'P'
   >>> '\N{SNAKE}'
   '🐍'

Chuỗi này không thể xuất hiện trong :ref:`bytes literals <bytes-literal>`.

.. versionchanged:: 3.3
   Đã bổ sung hỗ trợ cho `name aliases <https://www.unicode.org/Public/16.0.0/ucd/NameAliases.txt>`__.

.. _string-escape-long-hex:

Ký tự Unicode dạng thập lục phân
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các chuỗi này :samp:`\\u{xxxx}` và :samp:`\\U{xxxxxxxx}` biểu thị ký tự Unicode có giá trị hex (cơ số 16) đã cho. Cần chính xác bốn chữ số cho ``\u``; cần chính xác tám chữ số cho ``\U``. Chuỗi sau có thể mã hóa bất kỳ ký tự Unicode nào.

.. code-block:: pycon

   >>> '\u1234'
   'ሴ'
   >>> '\U0001f40d'
   '🐍'

Các chuỗi này không thể xuất hiện trong :ref:`bytes literals <bytes-literal>`.


.. index:: unrecognized escape sequence

Chuỗi escape không được nhận diện
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Không giống Standard C, tất cả các chuỗi escape không được nhận diện đều được giữ nguyên trong chuỗi, nghĩa là *dấu gạch chéo ngược được giữ lại trong kết quả*::

   >>> print('\q')
   \q
   >>> list('\q')
   ['\\', 'q']

Lưu ý rằng đối với các literal bytes, các escape sequence chỉ được nhận diện trong các string literal (``\N...``, ``\u...``, ``\U...``) thuộc nhóm escape sequence không được nhận diện.

.. versionchanged:: 3.6
   Các escape sequence không được nhận diện sẽ tạo ra một :exc:`DeprecationWarning`.

.. versionchanged:: 3.12
   Các escape sequence không được nhận diện sẽ tạo ra một :exc:`SyntaxWarning`. Trong một phiên bản Python tương lai, chúng sẽ gây ra một :exc:`SyntaxError`.


.. index::
   single: b'; bytes literal
   single: b"; bytes literal


.. _bytes-literal:

Literal bytes
-------------

:dfn:`Literal bytes` luôn được thêm tiền tố '``b``' hoặc '``B``'; chúng tạo ra một instance của kiểu :class:`bytes` thay vì kiểu :class:`str`. Chúng chỉ có thể chứa các ký tự ASCII; các byte có giá trị số từ 128 trở lên phải được biểu diễn bằng escape sequence (thường là
:ref:`string-escape-hex` hoặc :ref:`string-escape-oct`):

.. code-block:: pycon

   >>> b'\x89PNG\r\n\x1a\n'
   b'\x89PNG\r\n\x1a\n'
   >>> list(b'\x89PNG\r\n\x1a\n')
   [137, 80, 78, 71, 13, 10, 26, 10]

Tương tự, byte có giá trị 0 phải được biểu diễn bằng escape sequence (thường là ``\0`` hoặc ``\x00``).


.. index::
   single: r'; raw string literal
   single: r"; raw string literal

.. _raw-strings:

Các literal chuỗi raw
---------------------

Cả literal chuỗi và literal bytes đều có thể được thêm tiền tố là chữ cái '``r``' hoặc '``R``'; các cấu trúc như vậy lần lượt được gọi là :dfn:`literal chuỗi raw` và :dfn:`literal bytes raw`, đồng thời coi dấu gạch chéo ngược là ký tự literal. Vì vậy, trong các literal chuỗi raw, :ref:`chuỗi escape <escape-sequences>` không được xử lý đặc biệt:

.. code-block:: pycon

   >>> r'\d{4}-\d{2}-\d{2}'
   '\\d{4}-\\d{2}-\\d{2}'

Ngay cả trong một literal raw, dấu ngoặc kép vẫn có thể được escape bằng dấu gạch chéo ngược, nhưng dấu gạch chéo ngược vẫn được giữ lại trong kết quả; ví dụ, ``r"\""`` là một literal chuỗi hợp lệ gồm hai ký tự: dấu gạch chéo ngược và dấu ngoặc kép; ``r"\"`` không phải là một literal chuỗi hợp lệ (ngay cả chuỗi raw cũng không thể kết thúc bằng một số lẻ dấu gạch chéo ngược). Cụ thể, *một literal raw không thể kết thúc bằng một dấu gạch chéo ngược đơn* (vì dấu gạch chéo ngược sẽ escape ký tự ngoặc kép theo sau). Cũng lưu ý rằng một dấu gạch chéo ngược đơn theo sau là một dòng mới được diễn giải là hai ký tự đó trong literal, *không phải* là phần tiếp dòng.


.. index::
   single: formatted string literal
   single: interpolated string literal
   single: string; formatted literal
   single: string; interpolated literal
   single: f-string
   single: fstring
   single: f'; formatted string literal
   single: f"; formatted string literal
   single: {} (curly brackets); in formatted string literal
   single: ! (exclamation); in formatted string literal
   single: : (colon); in formatted string literal
   single: = (equals); for help in debugging using string literals

.. _f-strings:
.. _formatted-string-literals:

f-strings
---------

.. versionadded:: 3.6
.. versionchanged:: 3.7
   :keyword:`await` và :keyword:`async for` có thể được sử dụng trong các biểu thức bên trong f-strings.
.. versionchanged:: 3.8
   Đã thêm bộ chỉ định debug (``=``)
.. versionchanged:: 3.12
   Nhiều hạn chế đối với các biểu thức bên trong f-strings đã được gỡ bỏ. Đáng chú ý, hiện đã cho phép chuỗi lồng nhau, comment và dấu gạch chéo ngược.

Một :dfn:`formatted string literal` hoặc :dfn:`f-string` là một string literal có tiền tố là '``f``' hoặc '``F``'. Không giống các string literal khác, f-string không có giá trị hằng. Chúng có thể chứa các *replacement field* được phân cách bằng dấu ngoặc nhọn ``{}``. Replacement field chứa các biểu thức được đánh giá tại thời điểm chạy. Ví dụ::

   >>> who = 'nobody'
   >>> nationality = 'Spanish'
   >>> f'{who.title()} expects the {nationality} Inquisition!'
   'Nobody expects the Spanish Inquisition!'

Mọi dấu ngoặc nhọn được nhân đôi (``{{`` hoặc ``}}``) bên ngoài replacement field sẽ được thay thế bằng dấu ngoặc nhọn đơn tương ứng::

   >>> print(f'{{...}}')
   {...}

Các ký tự khác bên ngoài replacement field được xử lý như trong string literal thông thường. Điều này có nghĩa là các escape sequence được giải mã (trừ khi literal cũng được đánh dấu là raw string), và có thể sử dụng dòng mới trong f-string được đặt trong ba dấu nháy::

   >>> name = 'Galahad'
   >>> favorite_color = 'blue'
   >>> print(f'{name}:\t{favorite_color}')
   Galahad:       blue
   >>> print(rf"C:\Users\{name}")
   C:\Users\Galahad
   >>> print(f'''Three shall be the number of the counting
   ... and the number of the counting shall be three.''')
   Three shall be the number of the counting
   and the number of the counting shall be three.

Các biểu thức trong formatted string literal được xử lý như các biểu thức Python thông thường. Mỗi biểu thức được đánh giá trong ngữ cảnh nơi formatted string literal xuất hiện, theo thứ tự từ trái sang phải. Không cho phép biểu thức rỗng, và cả :keyword:`lambda` lẫn assignment expression ``:=`` đều phải được đặt trong dấu ngoặc đơn tường minh::

   >>> f'{(half := 1/2)}, {half * 42}'
   '0.5, 21.0'

Có thể sử dụng kiểu dấu nháy của f-string bên ngoài bên trong replacement field::

   >>> a = dict(x=2)
   >>> f"abc {a["x"]} def"
   'abc 2 def'

Dấu gạch chéo ngược cũng được phép sử dụng trong replacement field và được đánh giá giống như trong mọi ngữ cảnh khác::

   >>> a = ["a", "b", "c"]
   >>> print(f"List a contains:\n{"\n".join(a)}")
   List a contains:
   a
   b
   c

Có thể lồng các f-string::

   >>> name = 'world'
   >>> f'Repeated:{f' hello {name}' * 3}'
   'Repeated: hello world hello world hello world'

Các chương trình Python có tính di động không nên sử dụng quá 5 cấp độ lồng nhau.

.. impl-detail::

   CPython không giới hạn mức độ lồng nhau của f-strings.

Các biểu thức thay thế có thể chứa dòng mới trong cả f-strings dùng dấu nháy đơn và f-strings dùng ba dấu nháy, đồng thời có thể chứa chú thích. Mọi nội dung xuất hiện sau ``#`` bên trong một trường thay thế đều là chú thích (kể cả dấu ngoặc nhọn đóng và dấu nháy). Điều này có nghĩa là các trường thay thế có chú thích phải được đóng ở một dòng khác:

.. code-block:: text

   >>> a = 2
   >>> f"abc{a  # This comment  }"  continues until the end of the line
   ...       + 3}"
   'abc5'

Sau biểu thức, các trường thay thế có thể tùy chọn chứa:

* một *bộ chỉ định debug* -- một dấu bằng (``=``), có thể có khoảng trắng ở một hoặc cả hai bên;
* một *bộ chỉ định chuyển đổi* -- ``!s``, ``!r`` hoặc ``!a``; và/hoặc
* một *bộ chỉ định định dạng* được thêm tiền tố là dấu hai chấm (``:``).

Xem phần :ref:`Thư viện chuẩn về f-string <stdtypes-fstrings>` để biết chi tiết về cách các trường này được đánh giá.

Như phần đó giải thích, *format specifier* được truyền làm đối số thứ hai cho hàm :func:`format` để định dạng giá trị của trường thay thế. Ví dụ, chúng có thể được dùng để chỉ định độ rộng của trường và các ký tự đệm bằng :ref:`Ngôn ngữ Đặc tả Định dạng Tối giản <formatspec>`::

   >>> number = 14.3
   >>> f'{number:20.7f}'
   '          14.3000000'

Các format specifier ở cấp cao nhất có thể bao gồm các trường thay thế lồng nhau::

   >>> field_size = 20
   >>> precision = 7
   >>> f'{number:{field_size}.{precision}f}'
   '          14.3000000'

Các trường lồng nhau này có thể bao gồm các trường chuyển đổi riêng và
:ref:`format specifier <formatspec>`::

   >>> number = 3
   >>> f'{number:{field_size}}'
   '                   3'
   >>> f'{number:{field_size:05}}'
   '00000000000000000003'

Tuy nhiên, các trường lồng nhau này không được bao gồm các trường thay thế lồng sâu hơn.

Các string literal được định dạng không thể được dùng làm :term:`docstring <docstring>`, ngay cả khi chúng không bao gồm biểu thức::

   >>> def foo():
   ...     f"Not a docstring"
   ...
   >>> print(foo.__doc__)
   None

.. seealso::

   * :pep:`498` -- Nội suy chuỗi ký tự nguyên văn
   * :pep:`701` -- Hình thức hóa cú pháp của f-string
   * :meth:`str.format`, sử dụng một cơ chế format string liên quan.


.. _t-strings:
.. _template-string-literals:

t-strings
---------

.. versionadded:: 3.14

Một :dfn:`literal chuỗi template` hoặc :dfn:`t-string` là một literal chuỗi được thêm tiền tố '``t``' hoặc '``T``'. Các chuỗi này tuân theo cùng quy tắc cú pháp như
:ref:`literal chuỗi được định dạng <f-strings>`. Để biết sự khác biệt trong quy tắc đánh giá, xem
:ref:`mục Standard Library về t-string <stdtypes-tstrings>`


Văn phạm hình thức của f-string
-------------------------------

F-string được xử lý một phần bởi :term:`lexical analyzer`, thành phần này tạo ra các token :py:data:`~token.FSTRING_START`, :py:data:`~token.FSTRING_MIDDLE` và :py:data:`~token.FSTRING_END`, và một phần bởi parser, thành phần xử lý các biểu thức trong trường thay thế. Cách phân chia công việc chính xác là một chi tiết triển khai của CPython.

Tương ứng, văn phạm f-string là sự kết hợp của
:ref:`các định nghĩa từ vựng và cú pháp <notation-lexical-vs-syntactic>`.

Khoảng trắng có ý nghĩa trong các trường hợp sau:

* Không được có khoảng trắng trong :py:data:`~token.FSTRING_START` (giữa tiền tố và dấu ngoặc kép).
* Khoảng trắng trong :py:data:`~token.FSTRING_MIDDLE` là một phần của nội dung chuỗi literal.
* Trong ``fstring_replacement_field``, nếu có ``f_debug_specifier``, toàn bộ khoảng trắng sau dấu ngoặc nhọn mở cho đến ``f_debug_specifier``, cũng như khoảng trắng ngay sau ``f_debug_specifier``, được giữ lại như một phần của biểu thức.

  .. impl-detail::

     Biểu thức không được xử lý trong giai đoạn tokenization; nó được lấy từ mã nguồn bằng cách sử dụng vị trí của token ``{`` và token đứng sau ``=``.


Định nghĩa ``FSTRING_MIDDLE`` sử dụng
:ref:`negative lookaheads <lexical-lookaheads>` (``!``) để chỉ các ký tự đặc biệt (dấu gạch chéo ngược, dòng mới, ``{``, ``}``) và các chuỗi (``f_quote``).

.. grammar-snippet::
   :group: python-grammar

   fstring:    `FSTRING_START` `fstring_middle`* `FSTRING_END`

   FSTRING_START:      `fstringprefix` ("'" | '"' | "'''" | '"""')
   FSTRING_END:        `f_quote`
   fstringprefix:      <("f" | "fr" | "rf"), case-insensitive>
   f_debug_specifier:  '='
   f_quote:            <the quote character(s) used in FSTRING_START>

   fstring_middle:
      | `fstring_replacement_field`
      | `FSTRING_MIDDLE`
   FSTRING_MIDDLE:
      | (!"\" !`newline` !'{' !'}' !`f_quote`) `source_character`
      | `stringescapeseq`
      | "{{"
      | "}}"
      | <newline, in triple-quoted f-strings only>
   fstring_replacement_field:
      | '{' `f_expression` [`f_debug_specifier`] [`fstring_conversion`]
            [`fstring_full_format_spec`] '}'
   fstring_conversion:
      | "!" ("s" | "r" | "a")
   fstring_full_format_spec:
      | ':' `fstring_format_spec`*
   fstring_format_spec:
      | `FSTRING_MIDDLE`
      | `fstring_replacement_field`
   f_expression:
      | ','.(`conditional_expression` | "*" `or_expr`)+ [","]
      | `yield_expression`

.. note::

   Trong đoạn ngữ pháp trên, các quy tắc ``f_quote`` và ``FSTRING_MIDDLE`` phụ thuộc vào ngữ cảnh -- chúng phụ thuộc vào nội dung của ``FSTRING_START`` của ``fstring`` bao quanh gần nhất.

   Việc xây dựng một ngữ pháp hình thức truyền thống hơn từ mẫu này được để lại như một bài tập cho người đọc.

Ngữ pháp của t-string giống hệt ngữ pháp của f-string, với *t* thay cho *f* ở đầu tên quy tắc và tên token cũng như trong tiền tố.

.. grammar-snippet::
   :group: python-grammar

   tstring:    TSTRING_START tstring_middle* TSTRING_END

   <rest of the t-string grammar is omitted; see above>


.. _numbers:

Literal số
==========

.. index:: number, numeric literal, integer literal
   floating-point literal, hexadecimal literal
   octal literal, binary literal, decimal literal, imaginary literal, complex literal

:data:`~token.NUMBER` token biểu diễn các literal số, gồm ba loại: số nguyên, số dấu phẩy động và số ảo.

.. grammar-snippet::
   :group: python-grammar

   NUMBER: `integer` | `floatnumber` | `imagnumber`

Giá trị số của một literal số giống với giá trị nhận được nếu truyền literal đó dưới dạng chuỗi cho hàm khởi tạo của lớp :class:`int`, :class:`float` hoặc :class:`complex`, tương ứng. Lưu ý rằng không phải mọi đầu vào hợp lệ cho các hàm khởi tạo đó cũng là literal hợp lệ.

Literal số không bao gồm dấu; một cụm như ``-1`` thực chất là một biểu thức gồm toán tử một ngôi '``-``' và literal ``1``.


.. index::
   single: 0b; integer literal
   single: 0o; integer literal
   single: 0x; integer literal
   single: _ (underscore); in numeric literal

.. _integers:

Literal số nguyên
-----------------

Literal số nguyên biểu diễn các số nguyên. Ví dụ:::

   7
   3
   2147483647

Độ dài của literal số nguyên không bị giới hạn, ngoài giới hạn do dung lượng bộ nhớ khả dụng có thể lưu trữ::

   7922816251426433759354395033679228162514264337593543950336

Dấu gạch dưới có thể được dùng để nhóm các chữ số nhằm tăng khả năng đọc, và được bỏ qua khi xác định giá trị số của literal. Ví dụ: các literal sau là tương đương::

   100_000_000_000
   100000000000
   1_00_00_00_00_000

Dấu gạch dưới chỉ có thể xuất hiện giữa các chữ số. Ví dụ: ``_123``, ``321_`` và ``123__321`` *không* phải là các literal hợp lệ.

Số nguyên có thể được chỉ định ở dạng nhị phân (cơ số 2), bát phân (cơ số 8) hoặc thập lục phân (cơ số 16) bằng các tiền tố ``0b``, ``0o`` và ``0x`` tương ứng. Các chữ số thập lục phân từ 10 đến 15 được biểu diễn bằng các chữ cái ``A``-``F``, không phân biệt chữ hoa chữ thường. Ví dụ::

   0b100110111
   0b_1110_0101
   0o177
   0o377
   0xdeadbeef
   0xDead_Beef

Dấu gạch dưới có thể đứng sau phần chỉ định cơ số. Ví dụ: ``0x_1f`` là một literal hợp lệ, nhưng ``0_x1f`` và ``0x__1f`` thì không.

Không được có các số 0 ở đầu một số thập phân khác 0. Ví dụ: ``0123`` không phải là một literal hợp lệ. Quy tắc này nhằm phân biệt với các literal bát phân kiểu C, vốn được Python sử dụng trước phiên bản 3.0.

Về mặt hình thức, các literal số nguyên được mô tả bằng các định nghĩa từ vựng sau:

.. grammar-snippet::
   :group: python-grammar

   integer:      `decinteger` | `bininteger` | `octinteger` | `hexinteger` | `zerointeger`
   decinteger:   `nonzerodigit` (["_"] `digit`)*
   bininteger:   "0" ("b" | "B") (["_"] `bindigit`)+
   octinteger:   "0" ("o" | "O") (["_"] `octdigit`)+
   hexinteger:   "0" ("x" | "X") (["_"] `hexdigit`)+
   zerointeger:  "0"+ (["_"] "0")*
   nonzerodigit: "1"..."9"
   digit:        "0"..."9"
   bindigit:     "0" | "1"
   octdigit:     "0"..."7"
   hexdigit:     `digit` | "a"..."f" | "A"..."F"

.. versionchanged:: 3.6
   Dấu gạch dưới hiện được cho phép trong các literal để phục vụ mục đích nhóm chữ số.


.. index::
   single: . (dot); in numeric literal
   single: e; in numeric literal
   single: _ (underscore); in numeric literal
.. _floating:

Các literal số dấu phẩy động
----------------------------

Các literal số dấu phẩy động (float), chẳng hạn như ``3.14`` hoặc ``1.5``, biểu thị
:ref:`các giá trị xấp xỉ của số thực <datamodel-float>`.

Chúng gồm các phần *số nguyên* và *phần phân số*, mỗi phần được tạo thành từ các chữ số thập phân. Các phần được ngăn cách bằng dấu thập phân, ``.``::

   2.71828
   4.0

Không giống literal số nguyên, các số 0 ở đầu được cho phép. Ví dụ, ``077.010`` là hợp lệ và biểu thị cùng một số với ``77.01``.

Tương tự như trong literal số nguyên, các dấu gạch dưới đơn có thể xuất hiện giữa các chữ số để giúp dễ đọc hơn::

   96_485.332_123
   3.14_15_93

Một trong hai phần này, nhưng không thể là cả hai, có thể để trống. Ví dụ::

   10.  # (tương đương với 10.0)
   .001  # (tương đương với 0.001)

Tùy chọn, phần nguyên và phần thập phân có thể được theo sau bởi *số mũ*: chữ cái ``e`` hoặc ``E``, theo sau là một dấu tùy chọn, ``+`` hoặc ``-``, và một số có cùng định dạng như phần nguyên và phần thập phân. ``e`` hoặc ``E`` biểu thị "nhân với mười lũy thừa"::

   1.0e3  # (biểu thị 1.0×10³, hay 1000.0)
   1.166e-5  # (biểu thị 1.166×10⁻⁵, hay 0.00001166)
   6.02214076e+23  # (biểu thị 6.02214076×10²³, hay 602214076000000000000000.)

Trong các số thực chỉ có phần nguyên và phần số mũ, có thể bỏ qua dấu thập phân::

   1e3  # (tương đương với 1.e3 và 1.0e3)
   0e0  # (tương đương với 0.)

Về mặt hình thức, các literal số thực được mô tả bằng những định nghĩa từ vựng sau:

.. grammar-snippet::
   :group: python-grammar

   floatnumber:
      | `digitpart` "." [`digitpart`] [`exponent`]
      | "." `digitpart` [`exponent`]
      | `digitpart` `exponent`
   digitpart: `digit` (["_"] `digit`)*
   exponent:  ("e" | "E") ["+" | "-"] `digitpart`

.. versionchanged:: 3.6
   Giờ đây, dấu gạch dưới được phép dùng để phân nhóm trong các literal.


.. index::
   single: j; in numeric literal
.. _imaginary:

Literal số ảo
-------------

Python có các đối tượng :ref:`số phức <typesnumeric>`, nhưng không có literal số phức. Thay vào đó, *literal số ảo* biểu diễn các số phức có phần thực bằng không.

Ví dụ, trong toán học, số phức 3+4.2\ *i* được viết là số thực 3 cộng với số ảo 4.2\ *i*. Python sử dụng cú pháp tương tự, ngoại trừ đơn vị ảo được viết là ``j`` thay vì *i*::

   3+4.2j

Đây là một biểu thức gồm :ref:`literal số nguyên <integers>` ``3``, :ref:`toán tử <operators>` '``+``' và :ref:`literal số ảo <imaginary>` ``4.2j``. Vì đây là ba token riêng biệt nên có thể có khoảng trắng giữa chúng::

   3 + 4.2j

Không được phép có khoảng trắng *giữa* mỗi token. Cụ thể, hậu tố ``j`` không được tách khỏi số đứng trước nó.

Số đứng trước ``j`` có cú pháp giống như một literal số thực dấu phẩy động. Do đó, các literal số ảo sau đây là hợp lệ::

   4.2j
   3.14j
   10.j
   .001j
   1e100j
   3.14e-10j
   3.14_15_93j

Không giống literal số thực dấu phẩy động, có thể bỏ dấu chấm thập phân nếu số ảo chỉ có phần nguyên. Số này vẫn được đánh giá là một số dấu phẩy động, không phải số nguyên::

   10j
   0j
   1000000000000000000000000j   # tương đương với 1e+24j

Hậu tố ``j`` không phân biệt chữ hoa chữ thường. Điều đó có nghĩa là bạn có thể dùng ``J`` thay thế::

   3.14J   # tương đương với 3.14j

Về mặt hình thức, các literal số ảo được mô tả bằng định nghĩa từ vựng sau:

.. grammar-snippet::
   :group: python-grammar

   imagnumber: (`floatnumber` | `digitpart`) ("j" | "J")


.. _delimiters:
.. _operators:
.. _lexical-ellipsis:

Toán tử và dấu phân cách
========================

.. index::
   single: operators
   single: delimiters

Ngữ pháp sau định nghĩa các token :dfn:`toán tử` và :dfn:`dấu phân cách`, tức là kiểu token chung :data:`~token.OP`. Một :ref:`danh sách các token này và tên của chúng <token_operators_delimiters>` cũng có trong tài liệu của module :mod:`!token`.

.. grammar-snippet::
   :group: python-grammar

   OP:
      | assignment_operator
      | bitwise_operator
      | comparison_operator
      | enclosing_delimiter
      | other_delimiter
      | arithmetic_operator
      | "..."
      | other_op

   assignment_operator:   "+=" | "-=" | "*=" | "**=" | "/="  | "//=" | "%=" |
                          "&=" | "|=" | "^=" | "<<=" | ">>=" | "@="  | ":="
   bitwise_operator:      "&"  | "|"  | "^"  | "~"   | "<<"  | ">>"
   comparison_operator:   "<=" | ">=" | "<"  | ">"   | "=="  | "!="
   enclosing_delimiter:   "("  | ")"  | "["  | "]"   | "{"   | "}"
   other_delimiter:       ","  | ":"  | "!"  | ";"   | "="   | "->"
   arithmetic_operator:   "+"  | "-"  | "**" | "*"   | "//"  | "/"   | "%"
   other_op:              "."  | "@"

.. note::

   Nhìn chung, *toán tử* được dùng để kết hợp các :ref:`biểu thức <expressions>`, còn *dấu phân cách* phục vụ các mục đích khác. Tuy nhiên, không có sự phân biệt rõ ràng và mang tính hình thức giữa hai nhóm này.

   Một số token có thể đóng vai trò là toán tử hoặc dấu phân cách, tùy vào cách sử dụng. Ví dụ, ``*`` vừa là toán tử nhân vừa là dấu phân cách được dùng để unpack sequence, còn ``@`` vừa là phép nhân ma trận vừa là dấu phân cách mở đầu cho decorator.

   Với một số token, sự phân biệt này không rõ ràng. Ví dụ, một số người xem ``.``, ``(`` và ``)`` là các dấu phân cách, trong khi những người khác xem :py:func:`getattr` là toán tử và xem các toán tử gọi hàm là dấu phân cách.

   Một số toán tử của Python, chẳng hạn như ``and``, ``or`` và ``not in``, sử dụng
   :ref:`keyword <keywords>` token thay vì "symbol" (token toán tử).

Một chuỗi gồm ba dấu chấm liên tiếp (``...``) có ý nghĩa đặc biệt dưới dạng một literal :py:data:`Ellipsis`.

