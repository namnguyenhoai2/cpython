.. _compound:

*****************
Câu lệnh phức hợp
*****************

.. index:: pair: compound; statement

Câu lệnh phức hợp chứa (các nhóm) câu lệnh khác; chúng tác động hoặc kiểm soát việc thực thi các câu lệnh đó theo một cách nào đó. Nhìn chung, câu lệnh phức hợp trải dài trên nhiều dòng, mặc dù trong những trường hợp đơn giản, toàn bộ câu lệnh phức hợp có thể nằm trên một dòng.

Các câu lệnh :keyword:`if`, :keyword:`while` và :keyword:`for` triển khai các cấu trúc điều khiển luồng truyền thống. :keyword:`try` chỉ định các exception handler và/hoặc mã dọn dẹp cho một nhóm câu lệnh, trong khi
câu lệnh :keyword:`with` cho phép thực thi mã khởi tạo và mã hoàn tất xung quanh một khối mã. Các định nghĩa hàm và lớp cũng là các câu lệnh phức hợp về mặt cú pháp.

.. index::
   single: clause
   single: suite
   single: ; (semicolon)

Một câu lệnh phức hợp bao gồm một hoặc nhiều “mệnh đề”. Một mệnh đề gồm có phần đầu và một “suite”. Các phần đầu mệnh đề của một câu lệnh phức hợp cụ thể đều nằm ở cùng một mức thụt lề. Mỗi phần đầu mệnh đề bắt đầu bằng một từ khóa nhận diện duy nhất và kết thúc bằng dấu hai chấm. Suite là một nhóm các câu lệnh được một mệnh đề kiểm soát. Suite có thể là một hoặc nhiều câu lệnh đơn giản được phân tách bằng dấu chấm phẩy, nằm trên cùng dòng với phần đầu và theo sau dấu hai chấm của phần đầu, hoặc có thể là một hoặc nhiều câu lệnh được thụt lề trên các dòng tiếp theo. Chỉ dạng suite sau mới có thể chứa các câu lệnh phức hợp lồng nhau; đoạn sau là không hợp lệ, chủ yếu vì sẽ không rõ một mệnh đề :keyword:`if` tiếp theo
sẽ thuộc về mệnh đề :keyword:`else` nào::

   if test1: if test2: print(x)

Cũng lưu ý rằng trong ngữ cảnh này, dấu chấm phẩy có mức ưu tiên liên kết cao hơn dấu hai chấm, vì vậy trong ví dụ sau, tất cả hoặc không có lệnh gọi :func:`print` nào được thực thi::

   if x < y < z: print(x); print(y); print(z)

Tóm tắt:


.. productionlist:: python-grammar
   compound_stmt: `if_stmt`
                : | `while_stmt`
                : | `for_stmt`
                : | `try_stmt`
                : | `with_stmt`
                : | `match_stmt`
                : | `funcdef`
                : | `classdef`
                : | `async_with_stmt`
                : | `async_for_stmt`
                : | `async_funcdef`
   suite: `stmt_list` NEWLINE | NEWLINE INDENT `statement`+ DEDENT
   statement: `stmt_list` NEWLINE | `compound_stmt`
   stmt_list: `simple_stmt` (";" `simple_stmt`)* [";"]

.. index::
   single: NEWLINE token
   single: DEDENT token
   pair: dangling; else

Lưu ý rằng các câu lệnh luôn kết thúc bằng ``NEWLINE``, có thể theo sau là ``DEDENT``.  Cũng lưu ý rằng các mệnh đề tiếp diễn tùy chọn luôn bắt đầu bằng một từ khóa không thể bắt đầu một câu lệnh, vì vậy không có sự mơ hồ nào (vấn đề “:keyword:`else` treo” được giải quyết trong Python bằng cách yêu cầu các câu lệnh ``NEWLINE`` lồng nhau phải được thụt lề).
câu lệnh :keyword:`if`.

Để rõ ràng, cách định dạng các quy tắc ngữ pháp trong những phần sau đặt mỗi mệnh đề trên một dòng riêng.


.. _if:
.. _elif:
.. _else:

Câu lệnh :keyword:`!if`
=======================

.. index::
   ! pair: statement; if
   pair: keyword; elif
   pair: keyword; else
   single: : (colon); compound statement

Câu lệnh :keyword:`if` được dùng để thực thi có điều kiện:

.. productionlist:: python-grammar
   if_stmt: "if" `assignment_expression` ":" `suite`
          : ("elif" `assignment_expression` ":" `suite`)*
          : ["else" ":" `suite`]

Nó chọn chính xác một trong các khối lệnh bằng cách lần lượt đánh giá các biểu thức cho đến khi tìm thấy một biểu thức đúng (xem phần :ref:`booleans` để biết định nghĩa về đúng và sai); sau đó khối lệnh đó được thực thi (và không có phần nào khác của
câu lệnh :keyword:`if` được thực thi hoặc đánh giá). Nếu tất cả các biểu thức đều sai, khối lệnh của mệnh đề :keyword:`else`, nếu có, sẽ được thực thi.


.. _while:

Câu lệnh :keyword:`!while`
==========================

.. index::
   ! pair: statement; while
   pair: keyword; else
   pair: loop; statement
   single: : (colon); compound statement

Câu lệnh :keyword:`while` được dùng để thực thi lặp lại chừng nào một biểu thức còn đúng:

.. productionlist:: python-grammar
   while_stmt: "while" `assignment_expression` ":" `suite`
             : ["else" ":" `suite`]

Biểu thức được kiểm tra lặp đi lặp lại và nếu đúng, khối lệnh đầu tiên sẽ được thực thi; nếu biểu thức sai (có thể ngay lần đầu tiên được kiểm tra), khối lệnh của mệnh đề :keyword:`!else`, nếu có, sẽ được thực thi và vòng lặp kết thúc.

.. index::
   pair: statement; break
   pair: statement; continue

Một câu lệnh :keyword:`break` được thực thi trong khối lệnh đầu tiên sẽ kết thúc vòng lặp mà không thực thi khối lệnh của mệnh đề :keyword:`!else`. Một câu lệnh :keyword:`continue` được thực thi trong khối lệnh đầu tiên sẽ bỏ qua phần còn lại của khối lệnh và quay lại kiểm tra biểu thức.


.. _for:

Câu lệnh :keyword:`!for`
========================

.. index::
   ! pair: statement; for
   pair: keyword; in
   pair: keyword; else
   pair: target; list
   pair: loop; statement
   pair: object; sequence
   single: : (colon); compound statement

Câu lệnh :keyword:`for` được dùng để lặp qua các phần tử của một sequence (chẳng hạn như chuỗi, tuple hoặc list) hoặc đối tượng iterable khác:

.. productionlist:: python-grammar
   for_stmt: "for" `target_list` "in" `starred_expression_list` ":" `suite`
           : ["else" ":" `suite`]

Biểu thức :token:`~python-grammar:starred_expression_list` được đánh giá một lần; biểu thức này sẽ trả về một đối tượng :term:`iterable`. Một :term:`iterator` được tạo cho iterable đó. Sau đó, mục đầu tiên do iterator cung cấp được gán vào danh sách đích theo các quy tắc chuẩn dành cho phép gán (xem :ref:`assignment`), rồi suite được thực thi. Quá trình này lặp lại với từng mục do iterator cung cấp. Khi iterator là :term:`exhausted`, suite trong mệnh đề :keyword:`!else`, nếu có, sẽ được thực thi và vòng lặp kết thúc.

.. index::
   pair: statement; break
   pair: statement; continue

Một câu lệnh :keyword:`break` được thực thi trong suite đầu tiên sẽ kết thúc vòng lặp mà không thực thi suite của mệnh đề :keyword:`!else`. Một câu lệnh :keyword:`continue` được thực thi trong suite đầu tiên sẽ bỏ qua phần còn lại của suite và tiếp tục với mục tiếp theo, hoặc với mệnh đề :keyword:`!else` nếu không còn mục nào.

Vòng lặp for thực hiện phép gán cho các biến trong danh sách đích. Thao tác này ghi đè mọi phép gán trước đó cho các biến đó, bao gồm cả những phép gán được thực hiện trong suite của vòng lặp for.::

   for i in range(10):
       print(i)
       i = 5             # điều này sẽ không ảnh hưởng đến vòng lặp for
                         # vì i sẽ bị ghi đè bằng
                         # chỉ mục tiếp theo trong phạm vi


.. index::
   pair: built-in function; range

Các tên trong danh sách đích không bị xóa khi vòng lặp kết thúc, nhưng nếu dãy rỗng thì vòng lặp sẽ hoàn toàn không gán giá trị cho chúng. Gợi ý: kiểu dựng sẵn :func:`range` biểu diễn các dãy số học bất biến gồm các số nguyên. Chẳng hạn, lặp qua ``range(3)`` lần lượt cho kết quả 0, 1 rồi 2.

.. versionchanged:: 3.11
   Các phần tử có dấu sao hiện được phép trong danh sách biểu thức.


.. _try:

Câu lệnh :keyword:`!try`
========================

.. index::
   ! pair: statement; try
   pair: keyword; except
   pair: keyword; finally
   pair: keyword; else
   pair: keyword; as
   single: : (colon); compound statement

Câu lệnh :keyword:`!try` chỉ định các trình xử lý ngoại lệ và/hoặc mã dọn dẹp cho một nhóm câu lệnh:

.. productionlist:: python-grammar
   try_stmt: `try1_stmt` | `try2_stmt` | `try3_stmt`
   try1_stmt: "try" ":" `suite`
            : ("except" [`expression` ["as" `identifier`]] ":" `suite`)+
            : ["else" ":" `suite`]
            : ["finally" ":" `suite`]
   try2_stmt: "try" ":" `suite`
            : ("except" "*" `expression` ["as" `identifier`] ":" `suite`)+
            : ["else" ":" `suite`]
            : ["finally" ":" `suite`]
   try3_stmt: "try" ":" `suite`
            : "finally" ":" `suite`

Bạn có thể tìm thấy thêm thông tin về các ngoại lệ trong mục :ref:`exceptions`, còn thông tin về cách sử dụng câu lệnh :keyword:`raise` để tạo ngoại lệ có trong mục :ref:`raise`.

.. versionchanged:: 3.14
   Hỗ trợ tùy chọn bỏ dấu ngoặc nhóm khi sử dụng nhiều kiểu ngoại lệ. Xem :pep:`758`.

.. _except:

Mệnh đề :keyword:`!except`
--------------------------

Các mệnh đề :keyword:`!except` chỉ định một hoặc nhiều trình xử lý ngoại lệ. Khi không xảy ra ngoại lệ trong mệnh đề :keyword:`try`, không có trình xử lý ngoại lệ nào được thực thi. Khi xảy ra ngoại lệ trong khối lệnh :keyword:`!try`, quá trình tìm kiếm trình xử lý ngoại lệ bắt đầu. Quá trình tìm kiếm này lần lượt kiểm tra các mệnh đề :keyword:`!except` cho đến khi tìm thấy mệnh đề khớp với ngoại lệ. Nếu có mệnh đề :keyword:`!except` không có biểu thức, mệnh đề này phải ở cuối; nó khớp với mọi ngoại lệ.

Đối với mệnh đề :keyword:`!except` có biểu thức, biểu thức đó phải đánh giá thành một kiểu ngoại lệ hoặc một tuple gồm các kiểu ngoại lệ. Có thể bỏ dấu ngoặc nếu cung cấp nhiều kiểu ngoại lệ và không sử dụng mệnh đề ``as``. Ngoại lệ được phát sinh sẽ khớp với mệnh đề :keyword:`!except` có biểu thức đánh giá thành lớp của đối tượng ngoại lệ, một :term:`lớp cơ sở không ảo <abstract base class>` của đối tượng ngoại lệ hoặc một tuple chứa lớp như vậy.

Nếu không có mệnh đề :keyword:`!except` nào khớp với ngoại lệ, việc tìm kiếm trình xử lý ngoại lệ sẽ tiếp tục trong mã bao quanh và trên ngăn xếp lời gọi.  [#]_

Nếu việc đánh giá một biểu thức trong phần đầu của mệnh đề :keyword:`!except` phát sinh một ngoại lệ, việc tìm kiếm trình xử lý ban đầu sẽ bị hủy bỏ và một lượt tìm kiếm sẽ bắt đầu cho ngoại lệ mới trong mã bao quanh và trên ngăn xếp lời gọi (ngoại lệ này được xử lý như thể toàn bộ câu lệnh :keyword:`try` đã phát sinh ngoại lệ).

.. index:: single: as; except clause

Khi tìm thấy một mệnh đề :keyword:`!except` khớp, ngoại lệ sẽ được gán cho đích được chỉ định sau từ khóa :keyword:`!as` trong mệnh đề :keyword:`!except` đó, nếu có, rồi suite của mệnh đề :keyword:`!except` sẽ được thực thi. Tất cả các mệnh đề :keyword:`!except` phải có một khối mã thực thi được. Khi đến cuối khối này, quá trình thực thi sẽ tiếp tục bình thường sau toàn bộ câu lệnh :keyword:`try`. (Điều này có nghĩa là nếu có hai trình xử lý lồng nhau cho cùng một ngoại lệ và ngoại lệ xảy ra trong mệnh đề :keyword:`!try` của trình xử lý bên trong, trình xử lý bên ngoài sẽ không xử lý ngoại lệ đó.)

Khi một ngoại lệ đã được gán bằng ``as target``, ngoại lệ đó sẽ được xóa ở cuối mệnh đề :keyword:`!except`. Điều này tương đương với việc::

   except E as N:
       foo

được chuyển thành::

   except E as N:
       try:
           foo
       finally:
           del N

Điều này có nghĩa là phải gán ngoại lệ cho một tên khác để có thể tham chiếu đến ngoại lệ đó sau mệnh đề :keyword:`!except`. Các ngoại lệ được xóa vì khi có traceback đính kèm, chúng tạo thành một chu kỳ tham chiếu với stack frame, khiến tất cả biến cục bộ trong frame đó vẫn tồn tại cho đến khi lần thu gom rác tiếp theo diễn ra.

.. index::
   pair: module; sys
   pair: object; traceback

Trước khi khối lệnh của mệnh đề :keyword:`!except` được thực thi, ngoại lệ được lưu trong module :mod:`sys`, nơi có thể truy cập ngoại lệ từ bên trong phần thân của mệnh đề :keyword:`!except` bằng cách gọi
:func:`sys.exception`. Khi rời khỏi trình xử lý ngoại lệ, ngoại lệ được lưu trong module :mod:`sys` sẽ được đặt lại về giá trị trước đó::

   >>> print(sys.exception())
   None
   >>> try:
   ...     raise TypeError
   ... except:
   ...     print(repr(sys.exception()))
   ...     try:
   ...          raise ValueError
   ...     except:
   ...         print(repr(sys.exception()))
   ...     print(repr(sys.exception()))
   ...
   TypeError()
   ValueError()
   TypeError()
   >>> print(sys.exception())
   None


.. index::
   pair: keyword; except_star

.. _except_star:

mệnh đề :keyword:`!except*`
---------------------------

Các mệnh đề :keyword:`!except*` chỉ định một hoặc nhiều trình xử lý cho các nhóm ngoại lệ (các thực thể :exc:`BaseExceptionGroup`). Một câu lệnh :keyword:`try` có thể có các mệnh đề :keyword:`except` hoặc :keyword:`!except*`, nhưng không thể có cả hai. Kiểu ngoại lệ dùng để đối sánh là bắt buộc trong trường hợp :keyword:`!except*`, vì vậy ``except*:`` là lỗi cú pháp. Kiểu này được diễn giải như trong trường hợp
:keyword:`!except`, nhưng việc đối sánh được thực hiện trên các ngoại lệ chứa trong nhóm đang được xử lý. Một :exc:`TypeError` sẽ được phát sinh nếu kiểu đối sánh là lớp con của :exc:`!BaseExceptionGroup`, vì điều đó sẽ có ngữ nghĩa không rõ ràng.

Khi một nhóm ngoại lệ được phát sinh trong khối try, mỗi mệnh đề :keyword:`!except*` sẽ tách (xem :meth:`~BaseExceptionGroup.split`) nhóm đó thành các nhóm con gồm các ngoại lệ khớp và không khớp. Nếu nhóm con khớp không rỗng, nhóm này trở thành ngoại lệ được xử lý (giá trị do :func:`sys.exception` trả về) và được gán cho đích của mệnh đề :keyword:`!except*` (nếu có). Sau đó, phần thân của mệnh đề :keyword:`!except*` được thực thi. Nếu nhóm con không khớp không rỗng, nhóm này sẽ được xử lý bởi :keyword:`!except*` tiếp theo theo cách tương tự. Quá trình này tiếp tục cho đến khi tất cả ngoại lệ trong nhóm đã được đối sánh hoặc mệnh đề :keyword:`!except*` cuối cùng đã chạy.

Sau khi tất cả các mệnh đề :keyword:`!except*` thực thi, nhóm các ngoại lệ chưa được xử lý sẽ được hợp nhất với mọi ngoại lệ được phát sinh hoặc phát sinh lại từ bên trong
các mệnh đề :keyword:`!except*`. Nhóm ngoại lệ đã hợp nhất này được truyền tiếp trên::

   >>> try:
   ...     raise ExceptionGroup("eg",
   ...         [ValueError(1), TypeError(2), OSError(3), OSError(4)])
   ... except* TypeError as e:
   ...     print(f'caught {type(e)} with nested {e.exceptions}')
   ... except* OSError as e:
   ...     print(f'caught {type(e)} with nested {e.exceptions}')
   ...
   caught <class 'ExceptionGroup'> with nested (TypeError(2),)
   caught <class 'ExceptionGroup'> with nested (OSError(3), OSError(4))
     + Exception Group Traceback (most recent call last):
     |   File "<doctest default[0]>", line 2, in <module>
     |     raise ExceptionGroup("eg",
     |         [ValueError(1), TypeError(2), OSError(3), OSError(4)])
     | ExceptionGroup: eg (1 sub-exception)
     +-+---------------- 1 ----------------
       | ValueError: 1
       +------------------------------------

Nếu ngoại lệ được phát sinh từ khối :keyword:`try` không phải là một nhóm ngoại lệ và kiểu của nó khớp với một trong các mệnh đề :keyword:`!except*`, thì nó sẽ bị bắt và được bọc trong một nhóm ngoại lệ có chuỗi thông báo rỗng. Điều này đảm bảo rằng kiểu của ``e`` đích luôn là :exc:`BaseExceptionGroup`::

   >>> try:
   ...     raise BlockingIOError
   ... except* BlockingIOError as e:
   ...     print(repr(e))
   ...
   ExceptionGroup('', (BlockingIOError(),))

:keyword:`break`, :keyword:`continue` và :keyword:`return` không thể xuất hiện trong một mệnh đề :keyword:`!except*`.


.. index::
   pair: keyword; else
   pair: statement; return
   pair: statement; break
   pair: statement; continue

.. _except_else:

Mệnh đề :keyword:`!else`
------------------------

Mệnh đề :keyword:`!else` tùy chọn được thực thi nếu luồng điều khiển rời khỏi
khối :keyword:`try`, không có ngoại lệ nào được phát sinh và không có câu lệnh :keyword:`return` nào,
:keyword:`continue`, hoặc :keyword:`break` được thực thi. Các ngoại lệ trong mệnh đề :keyword:`!else` không được xử lý bởi các mệnh đề :keyword:`except` đứng trước.


.. index:: pair: keyword; finally

.. _finally:

mệnh đề :keyword:`!finally`
---------------------------

Nếu có :keyword:`!finally`, nó chỉ định một trình xử lý 'dọn dẹp'.  Phần
mệnh đề :keyword:`try` được thực thi, bao gồm mọi mệnh đề :keyword:`except` và :keyword:`else <except_else>`. Nếu một ngoại lệ xảy ra trong bất kỳ mệnh đề nào và không được xử lý, ngoại lệ đó sẽ được lưu tạm thời. Mệnh đề :keyword:`!finally` được thực thi.  Nếu có ngoại lệ đã lưu, ngoại lệ đó sẽ được raise lại ở cuối mệnh đề :keyword:`!finally`. Nếu mệnh đề :keyword:`!finally` raise một ngoại lệ khác, ngoại lệ đã lưu sẽ được đặt làm context của ngoại lệ mới. Nếu mệnh đề :keyword:`!finally` thực thi một câu lệnh :keyword:`return`, :keyword:`break` hoặc :keyword:`continue`, ngoại lệ đã lưu sẽ bị loại bỏ. Ví dụ: hàm này trả về 42.

.. code-block::

   def f():
       try:
           1/0
       finally:
           return 42

Thông tin về ngoại lệ không khả dụng cho chương trình trong quá trình thực thi mệnh đề :keyword:`!finally`.

.. index::
   pair: statement; return
   pair: statement; break
   pair: statement; continue

Khi một câu lệnh :keyword:`return`, :keyword:`break` hoặc :keyword:`continue` được thực thi trong suite :keyword:`try` của một câu lệnh :keyword:`!try`...\ :keyword:`!finally`, mệnh đề :keyword:`!finally` cũng được thực thi 'trên đường thoát.'

Giá trị trả về của một hàm được xác định bởi câu lệnh :keyword:`return` cuối cùng được thực thi.  Vì mệnh đề :keyword:`!finally` luôn được thực thi, một
câu lệnh :keyword:`!return` được thực thi trong mệnh đề :keyword:`!finally` sẽ luôn là câu lệnh cuối cùng được thực thi. Hàm sau đây trả về 'finally'.

.. code-block::

   def foo():
       try:
           return 'try'
       finally:
           return 'finally'

.. versionchanged:: 3.8
   Trước Python 3.8, một câu lệnh :keyword:`continue` là bất hợp lệ trong
   mệnh đề :keyword:`!finally` do một vấn đề trong quá trình triển khai.

.. versionchanged:: 3.14
   Trình biên dịch phát ra một :exc:`SyntaxWarning` khi một :keyword:`return`,
   :keyword:`break` hoặc :keyword:`continue` xuất hiện trong một khối :keyword:`!finally` (xem :pep:`765`).


.. _with:
.. _as:

Câu lệnh :keyword:`!with`
=========================

.. index::
   ! pair: statement; with
   pair: keyword; as
   single: as; with statement
   single: , (comma); with statement
   single: : (colon); compound statement

Câu lệnh :keyword:`with` được dùng để bao bọc việc thực thi một khối bằng các phương thức được định nghĩa bởi một context manager (xem mục :ref:`context-managers`). Điều này cho phép các mẫu sử dụng :keyword:`try`...\ :keyword:`except`...\ :keyword:`finally` phổ biến được đóng gói để thuận tiện tái sử dụng.

.. productionlist:: python-grammar
   with_stmt: "with" ( "(" `with_stmt_contents` ","? ")" | `with_stmt_contents` ) ":" `suite`
   with_stmt_contents: `with_item` ("," `with_item`)*
   with_item: `expression` ["as" `target`]

Việc thực thi câu lệnh :keyword:`with` với một "item" diễn ra như sau:

#. Biểu thức context (biểu thức được cung cấp trong
   :token:`~python-grammar:with_item`) được đánh giá để lấy một context manager (trình quản lý ngữ cảnh).

#. :meth:`~object.__enter__` của context manager được nạp để sử dụng sau.

#. :meth:`~object.__exit__` của context manager được nạp để sử dụng sau.

#. Phương thức :meth:`~object.__enter__` của context manager được gọi.

#. Nếu một đích được đưa vào câu lệnh :keyword:`with`, giá trị trả về từ :meth:`~object.__enter__` sẽ được gán cho đích đó.

   .. note::

      Câu lệnh :keyword:`with` đảm bảo rằng nếu phương thức :meth:`~object.__enter__` trả về mà không có lỗi, thì :meth:`~object.__exit__` sẽ luôn được gọi. Do đó, nếu xảy ra lỗi trong quá trình gán cho danh sách đích, lỗi đó sẽ được xử lý giống như lỗi xảy ra bên trong suite. Xem bước 7 bên dưới.

#. Khối lệnh được thực thi.

#. Phương thức :meth:`~object.__exit__` của context manager được gọi. Nếu một ngoại lệ khiến khối lệnh kết thúc, kiểu, giá trị và traceback của ngoại lệ đó được truyền làm đối số cho :meth:`~object.__exit__`. Nếu không, ba đối số :const:`None` được cung cấp.

   Nếu khối lệnh kết thúc do một ngoại lệ và giá trị trả về từ
   phương thức :meth:`~object.__exit__` là false, ngoại lệ sẽ được raise lại. Nếu giá trị trả về là true, ngoại lệ được bỏ qua và quá trình thực thi tiếp tục với câu lệnh theo sau câu lệnh :keyword:`with`.

   Nếu khối lệnh kết thúc vì bất kỳ lý do nào khác ngoài ngoại lệ, giá trị trả về từ :meth:`~object.__exit__` sẽ bị bỏ qua và quá trình thực thi tiếp tục tại vị trí thông thường tương ứng với loại kết thúc đã xảy ra.

Đoạn mã sau::

    with EXPRESSION as TARGET:
        SUITE

tương đương về mặt ngữ nghĩa với::

    manager = (EXPRESSION)
    enter = manager.__enter__
    exit = manager.__exit__
    value = enter()
    hit_except = False

    try:
        TARGET = value
        SUITE
    except:
        hit_except = True
        if not exit(*sys.exc_info()):
            raise
    finally:
        if not hit_except:
            exit(None, None, None)

ngoại trừ việc tra cứu :ref:`phương thức đặc biệt <special-lookup>` ngầm định được sử dụng cho :meth:`~object.__enter__` và :meth:`~object.__exit__`.

Với nhiều hơn một mục, các context manager được xử lý như thể nhiều
:keyword:`with` câu lệnh được lồng nhau::

   with A() as a, B() as b:
       SUITE

tương đương về mặt ngữ nghĩa với::

   with A() as a:
       with B() as b:
           SUITE

Bạn cũng có thể viết các context manager nhiều mục trên nhiều dòng nếu các mục được đặt trong dấu ngoặc đơn. Ví dụ::

   with (
       A() as a,
       B() as b,
   ):
       SUITE

.. versionchanged:: 3.1
   Hỗ trợ nhiều biểu thức context.

.. versionchanged:: 3.10
   Hỗ trợ sử dụng dấu ngoặc đơn dùng để nhóm nhằm ngắt câu lệnh thành nhiều dòng.

.. seealso::

   :pep:`343` - Câu lệnh "with"
      Đặc tả, bối cảnh và các ví dụ về câu lệnh Python :keyword:`with`.

.. _match:
.. _case:

Câu lệnh :keyword:`!match`
==========================

.. index::
   ! pair: statement; match
   ! pair: keyword; case
   ! single: pattern matching
   pair: keyword; if
   pair: keyword; as
   pair: match; case
   single: as; match statement
   single: : (colon); compound statement

.. versionadded:: 3.10

Câu lệnh match được dùng để đối sánh mẫu.  Cú pháp:

.. productionlist:: python-grammar
   match_stmt: 'match' `subject_expr` ":" NEWLINE INDENT `case_block`+ DEDENT
   subject_expr: `flexible_expression` "," [`flexible_expression_list` [',']]
               : | `assignment_expression`
   case_block: 'case' `patterns` [`guard`] ":" `suite`

.. note::
   Phần này sử dụng dấu nháy đơn để biểu thị
   :ref:`các từ khóa mềm <soft-keywords>`.

Đối sánh mẫu nhận một mẫu làm đầu vào (sau ``case``) và một giá trị chủ thể (sau ``match``).  Mẫu (có thể chứa các mẫu con) được đối sánh với giá trị chủ thể.  Các kết quả là:

* Một phép khớp thành công hoặc thất bại (còn được gọi là phép khớp mẫu thành công hoặc thất bại).

* Có thể liên kết các giá trị đã khớp với một tên. Các điều kiện tiên quyết cho việc này sẽ được thảo luận thêm bên dưới.

Các từ khóa ``match`` và ``case`` là :ref:`từ khóa mềm <soft-keywords>`.

.. seealso::

   * :pep:`634` -- Đối sánh mẫu cấu trúc: Đặc tả
   * :pep:`636` -- Đối sánh mẫu cấu trúc: Hướng dẫn


Tổng quan
---------

Dưới đây là tổng quan về luồng logic của một câu lệnh match:


#. Biểu thức subject ``subject_expr`` được đánh giá và thu được một giá trị subject. Nếu biểu thức subject chứa dấu phẩy, một tuple sẽ được tạo theo :ref:`các quy tắc chuẩn <typesseq-tuple>`.

#. Mỗi pattern trong một ``case_block`` được thử để khớp với giá trị subject. Các quy tắc cụ thể về thành công hoặc thất bại được mô tả bên dưới. Việc thử khớp cũng có thể liên kết một phần hoặc toàn bộ các tên độc lập trong pattern. Các quy tắc liên kết pattern chính xác thay đổi tùy theo loại pattern và được chỉ rõ bên dưới.  **Các liên kết tên được tạo trong quá trình khớp pattern thành công vẫn tồn tại sau khi block được thực thi và có thể được sử dụng sau câu lệnh match**.

   .. note::

      Trong quá trình khớp pattern thất bại, một số subpattern có thể thành công. Không dựa vào việc các liên kết đã được tạo cho một lần khớp thất bại. Ngược lại, cũng không dựa vào việc các biến vẫn không thay đổi sau một lần khớp thất bại. Hành vi chính xác phụ thuộc vào implementation và có thể thay đổi. Đây là một quyết định có chủ ý nhằm cho phép các implementation khác nhau bổ sung các tối ưu hóa.

#. Nếu pattern thành công, guard tương ứng (nếu có) sẽ được đánh giá. Trong trường hợp này, mọi liên kết tên đều được đảm bảo đã được thực hiện.

   * Nếu guard được đánh giá là true hoặc không tồn tại, phần ``block`` bên trong ``case_block`` sẽ được thực thi.

   * Nếu không, ``case_block`` tiếp theo sẽ được thử như mô tả ở trên.

   * Nếu không còn block case nào, câu lệnh match được hoàn tất.

.. note::

   Nhìn chung, người dùng không nên dựa vào việc một pattern sẽ được đánh giá. Tùy thuộc vào cách triển khai, interpreter có thể lưu các giá trị vào bộ nhớ đệm hoặc sử dụng những tối ưu hóa khác để bỏ qua các lần đánh giá lặp lại.

Một câu lệnh match mẫu::

   >>> flag = False
   >>> match (100, 200):
   ...    case (100, 300):  # Không khớp: 200 != 300
   ...        print('Case 1')
   ...    case (100, 200) if flag:  # Khớp thành công nhưng guard không thỏa mãn
   ...        print('Case 2')
   ...    case (100, y):  # Khớp và liên kết y với 200
   ...        print(f'Case 3, y: {y}')
   ...    case _:  # Pattern không được thử
   ...        print('Case 4, I match anything!')
   ...
   Case 3, y: 200


Trong trường hợp này, ``if flag`` là một guard. Đọc thêm về guard trong phần tiếp theo.

Guard
-----

.. index:: ! guard

.. productionlist:: python-grammar
   guard: "if" `assignment_expression`

Một ``guard`` (là một phần của ``case``) phải thành công để mã bên trong khối ``case`` được thực thi. Nó có dạng: :keyword:`if` theo sau bởi một biểu thức.


Luồng logic của một khối ``case`` với ``guard`` diễn ra như sau:

#. Kiểm tra xem mẫu trong khối ``case`` có thành công hay không. Nếu mẫu không khớp, ``guard`` sẽ không được đánh giá và khối ``case`` tiếp theo sẽ được kiểm tra.

#. Nếu mẫu khớp, hãy đánh giá ``guard``.

   * Nếu điều kiện ``guard`` được đánh giá là đúng, khối case sẽ được chọn.

   * Nếu điều kiện ``guard`` được đánh giá là sai, khối case sẽ không được chọn.

   * Nếu ``guard`` phát sinh ngoại lệ trong quá trình đánh giá, ngoại lệ đó sẽ lan truyền lên.

Guards được phép có side effect vì chúng là các biểu thức. Việc đánh giá guard phải tiến hành lần lượt từ khối case đầu tiên đến khối cuối cùng, từng khối một, bỏ qua các khối case mà không phải tất cả pattern của chúng đều thành công. (Tức là việc đánh giá guard phải diễn ra theo thứ tự.) Việc đánh giá guard phải dừng ngay khi một khối case được chọn.


.. _irrefutable_case:

Các khối Case không thể bác bỏ
------------------------------

.. index:: irrefutable case block, case block

Một khối case không thể bác bỏ là khối case khớp với mọi trường hợp. Một câu lệnh match có nhiều nhất một khối case không thể bác bỏ và khối này phải đứng cuối cùng.

Một khối case được xem là không thể bác bỏ nếu không có guard và pattern của nó là pattern không thể bác bỏ. Một pattern được xem là không thể bác bỏ nếu chỉ từ cú pháp của nó, ta có thể chứng minh rằng nó sẽ luôn thành công. Chỉ các pattern sau đây là không thể bác bỏ:

* :ref:`as-patterns` có vế trái không thể bác bỏ

* :ref:`or-patterns` chứa ít nhất một pattern không thể bác bỏ

* :ref:`capture-patterns`

* :ref:`wildcard-patterns`

* các pattern irrefutable được đặt trong ngoặc


Các pattern
-----------

.. index::
   single: ! patterns
   single: AS pattern, OR pattern, capture pattern, wildcard pattern

.. note::
   Phần này sử dụng các ký hiệu ngữ pháp ngoài EBNF tiêu chuẩn:

   * ký hiệu ``SEP.RULE+`` là dạng viết tắt của ``RULE (SEP RULE)*``

   * ký hiệu ``!RULE`` là dạng viết tắt của một khẳng định lookahead phủ định


Cú pháp cấp cao nhất cho ``patterns`` là:

.. productionlist:: python-grammar
   patterns: `open_sequence_pattern` | `pattern`
   pattern: `as_pattern` | `or_pattern`
   closed_pattern: | `literal_pattern`
                 : | `capture_pattern`
                 : | `wildcard_pattern`
                 : | `value_pattern`
                 : | `group_pattern`
                 : | `sequence_pattern`
                 : | `mapping_pattern`
                 : | `class_pattern`

Các mô tả dưới đây sẽ bao gồm phần mô tả "theo cách đơn giản" về tác dụng của một pattern nhằm mục đích minh họa (cảm ơn Raymond Hettinger vì một tài liệu đã truyền cảm hứng cho hầu hết các phần mô tả này). Lưu ý rằng các mô tả này chỉ nhằm mục đích minh họa và **có thể không** phản ánh cách triển khai bên dưới. Ngoài ra, chúng không bao quát tất cả các dạng hợp lệ.


.. _or-patterns:

Mẫu OR
^^^^^^

Mẫu OR là hai hoặc nhiều mẫu được phân tách bằng dấu gạch đứng ``|``.  Cú pháp:

.. productionlist:: python-grammar
   or_pattern: "|".`closed_pattern`+

Chỉ mẫu con cuối cùng mới có thể là :ref:`irrefutable <irrefutable_case>`, và mỗi mẫu con phải liên kết cùng một tập hợp tên để tránh sự mơ hồ.

Mẫu OR lần lượt đối chiếu từng mẫu con của nó với giá trị đối tượng cho đến khi một mẫu thành công.  Khi đó, mẫu OR được xem là thành công.  Ngược lại, nếu không có mẫu con nào thành công, mẫu OR sẽ thất bại.

Nói một cách đơn giản, ``P1 | P2 | ...`` sẽ cố gắng đối chiếu ``P1``; nếu thất bại, nó sẽ cố gắng đối chiếu ``P2``, thành công ngay lập tức nếu bất kỳ mẫu nào thành công, nếu không thì thất bại.

.. _as-patterns:

Mẫu AS
^^^^^^

Mẫu AS đối chiếu một mẫu OR ở bên trái từ khóa :keyword:`as` với một đối tượng.  Cú pháp:

.. productionlist:: python-grammar
   as_pattern: `or_pattern` "as" `capture_pattern`

Nếu mẫu OR không khớp, mẫu AS sẽ không khớp. Nếu không, mẫu AS sẽ liên kết subject với tên ở bên phải từ khóa as và khớp thành công. ``capture_pattern`` không thể là một ``_``.

Nói một cách đơn giản, ``P as NAME`` sẽ khớp với ``P``, và khi khớp thành công, nó sẽ đặt ``NAME = <subject>``.


.. _literal-patterns:

Mẫu Literal
^^^^^^^^^^^

Một mẫu literal tương ứng với hầu hết
:ref:`các literal <literals>` trong Python. Cú pháp:

.. productionlist:: python-grammar
   literal_pattern: `signed_number`
                  : | `signed_number` "+" NUMBER
                  : | `signed_number` "-" NUMBER
                  : | `strings`
                  : | "None"
                  : | "True"
                  : | "False"
   signed_number: ["-"] NUMBER

Quy tắc ``strings`` và token ``NUMBER`` được định nghĩa trong
:doc:`ngữ pháp Python chuẩn <./grammar>`. Chuỗi nằm trong dấu ngoặc kép ba lần được hỗ trợ. Chuỗi raw và chuỗi byte được hỗ trợ. :ref:`f-strings` và :ref:`t-strings` không được hỗ trợ.

Các dạng ``signed_number '+' NUMBER`` và ``signed_number '-' NUMBER`` dùng để biểu diễn :ref:`số phức <imaginary>`; chúng yêu cầu một số thực ở bên trái và một số ảo ở bên phải. Ví dụ: ``3 + 4j``.

Nói một cách đơn giản, ``LITERAL`` chỉ thành công khi ``<subject> == LITERAL``. Đối với các singleton ``None``, ``True`` và ``False``, toán tử :keyword:`is` được sử dụng.

.. _capture-patterns:

Mẫu bắt giữ
^^^^^^^^^^^

Mẫu bắt giữ liên kết giá trị subject với một tên. Cú pháp:

.. productionlist:: python-grammar
   capture_pattern: !'_' NAME

Một dấu gạch dưới ``_`` không phải là mẫu bắt giữ (đây là cách ``!'_'`` được biểu diễn). Thay vào đó, nó được xử lý như một
:token:`~python-grammar:wildcard_pattern`.

Trong một mẫu nhất định, một tên nhất định chỉ có thể được liên kết một lần.  Ví dụ: ``case x, x: ...`` không hợp lệ, còn ``case [x] | x: ...`` thì được phép.

Các mẫu bắt giữ luôn thành công.  Việc liên kết tuân theo các quy tắc phạm vi được thiết lập bởi toán tử biểu thức gán trong :pep:`572`; tên này trở thành một biến cục bộ trong phạm vi hàm bao quanh gần nhất, trừ khi có câu lệnh :keyword:`global` hoặc :keyword:`nonlocal` phù hợp.

Nói đơn giản, ``NAME`` sẽ luôn thành công và sẽ thiết lập ``NAME = <subject>``.

.. _wildcard-patterns:

Mẫu ký tự đại diện
^^^^^^^^^^^^^^^^^^

Mẫu ký tự đại diện luôn thành công (khớp với mọi thứ) và không liên kết với tên nào. Cú pháp:

.. productionlist:: python-grammar
   wildcard_pattern: '_'

``_`` là một :ref:`từ khóa mềm <soft-keywords>` trong bất kỳ mẫu nào, nhưng chỉ trong các mẫu. Như thường lệ, nó là một định danh, ngay cả trong các biểu thức ``match`` subject, các ``guard``\ s và các khối ``case``.

Nói đơn giản, ``_`` sẽ luôn thành công.

.. _value-patterns:

Mẫu giá trị
^^^^^^^^^^^

Mẫu giá trị đại diện cho một giá trị được đặt tên trong Python. Cú pháp:

.. productionlist:: python-grammar
   value_pattern: `attr`
   attr: `name_or_attr` "." NAME
   name_or_attr: `attr` | NAME

Tên có dấu chấm trong pattern được tra cứu bằng cách sử dụng các quy tắc chuẩn của Python
:ref:`quy tắc phân giải tên <resolve_names>`. Pattern thành công nếu giá trị được tìm thấy so sánh bằng với giá trị subject (sử dụng ``==`` toán tử bằng).

Nói một cách đơn giản, ``NAME1.NAME2`` sẽ thành công chỉ khi ``<subject> == NAME1.NAME2``

.. note::

  Nếu cùng một giá trị xuất hiện nhiều lần trong cùng một câu lệnh match, interpreter có thể lưu vào bộ nhớ đệm giá trị được tìm thấy đầu tiên và sử dụng lại thay vì thực hiện lại cùng một lần tra cứu. Bộ nhớ đệm này chỉ gắn với một lần thực thi cụ thể của một câu lệnh match cụ thể.

.. _group-patterns:

Pattern nhóm
^^^^^^^^^^^^

Pattern nhóm cho phép người dùng thêm dấu ngoặc đơn quanh các pattern để nhấn mạnh cách nhóm dự định. Ngoài ra, pattern này không có cú pháp bổ sung nào. Cú pháp:

.. productionlist:: python-grammar
   group_pattern: "(" `pattern` ")"

Nói một cách đơn giản, ``(P)`` có cùng tác dụng với ``P``.

.. _sequence-patterns:

Mẫu hình chuỗi
^^^^^^^^^^^^^^

Một mẫu hình chuỗi chứa một số mẫu hình con để khớp với các phần tử của chuỗi. Cú pháp tương tự như thao tác unpacking một list hoặc tuple.

.. productionlist:: python-grammar
  sequence_pattern: "[" [`maybe_sequence_pattern`] "]"
                  : | "(" [`open_sequence_pattern`] ")"
  open_sequence_pattern: `maybe_star_pattern` "," [`maybe_sequence_pattern`]
  maybe_sequence_pattern: ",".`maybe_star_pattern`+ ","?
  maybe_star_pattern: `star_pattern` | `pattern`
  star_pattern: "*" (`capture_pattern` | `wildcard_pattern`)

Không có sự khác biệt khi sử dụng dấu ngoặc đơn hoặc dấu ngoặc vuông cho các mẫu hình chuỗi (tức là ``(...)`` so với ``[...]`` ).

.. note::
   Một mẫu hình đơn được đặt trong dấu ngoặc đơn mà không có dấu phẩy ở cuối (ví dụ: ``(3 | 4)``) là một :ref:`mẫu hình nhóm <group-patterns>`. Trong khi đó, một mẫu hình đơn được đặt trong dấu ngoặc vuông (ví dụ: ``[3 | 4]``) vẫn là một mẫu hình chuỗi.

Một mẫu hình con có dấu sao xuất hiện nhiều nhất một lần trong một mẫu hình chuỗi. Mẫu hình con có dấu sao có thể xuất hiện ở bất kỳ vị trí nào. Nếu không có mẫu hình con có dấu sao, mẫu hình chuỗi là mẫu hình chuỗi có độ dài cố định; nếu không, đó là mẫu hình chuỗi có độ dài thay đổi.

Sau đây là luồng logic để khớp một mẫu hình chuỗi với một giá trị đối tượng:

#. Nếu giá trị đối tượng không phải là một chuỗi [#]_, mẫu hình chuỗi sẽ không khớp.

#. Nếu giá trị subject là một instance của ``str``, ``bytes`` hoặc ``bytearray``, sequence pattern sẽ thất bại.

#. Các bước tiếp theo phụ thuộc vào việc sequence pattern có độ dài cố định hay biến đổi.

   Nếu sequence pattern có độ dài cố định:

   #. Nếu độ dài của chuỗi subject không bằng số lượng subpattern, sequence pattern sẽ thất bại

   #. Các subpattern trong sequence pattern được đối sánh với các phần tử tương ứng trong chuỗi subject từ trái sang phải. Việc đối sánh dừng ngay khi một subpattern thất bại. Nếu tất cả subpattern đều đối sánh thành công với phần tử tương ứng, sequence pattern sẽ thành công.

   Nếu không, nếu sequence pattern có độ dài biến đổi:

   #. Nếu độ dài của chuỗi subject nhỏ hơn số lượng subpattern không có dấu sao, sequence pattern sẽ thất bại.

   #. Các subpattern không có dấu sao ở đầu được khớp với các phần tử tương ứng như đối với các sequence có độ dài cố định.

   #. Nếu bước trước đó thành công, subpattern có dấu sao sẽ khớp với một danh sách được tạo từ các phần tử còn lại của đối tượng cần khớp, không bao gồm các phần tử còn lại tương ứng với những subpattern không có dấu sao đứng sau subpattern có dấu sao.

   #. Các subpattern không có dấu sao còn lại được khớp với các phần tử tương ứng của đối tượng cần khớp, như đối với một sequence có độ dài cố định.

   .. note:: Độ dài của sequence đối tượng cần khớp được lấy thông qua
      :func:`len` (i.e. via the :meth:`~object.__len__` protocol).
      Trình thông dịch có thể lưu vào bộ nhớ đệm độ dài này theo cách tương tự như
      :ref:`value patterns <value-patterns>`.


Nói một cách đơn giản, ``[P1, P2, P3,`` ... ``, P<N>]`` chỉ khớp nếu tất cả những điều sau đây xảy ra:

* kiểm tra ``<subject>`` là một sequence
* ``len(subject) == <N>``
* ``P1`` khớp với ``<subject>[0]`` (lưu ý rằng phép khớp này cũng có thể liên kết các tên)
* ``P2`` khớp với ``<subject>[1]`` (lưu ý rằng phép khớp này cũng có thể liên kết các tên)
* ... và tương tự đối với mẫu/phần tử tương ứng.

.. _mapping-patterns:

Mẫu mapping
^^^^^^^^^^^

Mẫu mapping chứa một hoặc nhiều mẫu khóa-giá trị. Cú pháp tương tự như cách tạo một dictionary. Cú pháp:

.. productionlist:: python-grammar
   mapping_pattern: "{" [`items_pattern`] "}"
   items_pattern: ",".`key_value_pattern`+ ","?
   key_value_pattern: (`literal_pattern` | `value_pattern`) ":" `pattern`
                    : | `double_star_pattern`
   double_star_pattern: "**" `capture_pattern`

Một mẫu mapping có nhiều nhất một mẫu double star. Mẫu double star phải là subpattern cuối cùng trong mẫu mapping.

Các khóa trùng lặp trong mẫu ánh xạ không được phép. Các khóa literal trùng lặp sẽ gây ra :exc:`SyntaxError`. Hai khóa có cùng giá trị theo cách khác sẽ gây ra :exc:`ValueError` trong runtime.

Sau đây là luồng logic để khớp một mẫu ánh xạ với một giá trị đối tượng:

#. Nếu giá trị đối tượng không phải là một [#]_,mẫu ánh xạ sẽ không khớp.

#. Nếu mọi khóa được cung cấp trong mẫu ánh xạ đều có trong ánh xạ đối tượng, và mẫu cho từng khóa đều khớp với phần tử tương ứng của ánh xạ đối tượng, mẫu ánh xạ sẽ khớp.

#. Nếu phát hiện các khóa trùng lặp trong mẫu ánh xạ, mẫu này được xem là không hợp lệ. Một :exc:`SyntaxError` sẽ được nêu ra cho các giá trị literal trùng lặp; hoặc một :exc:`ValueError` cho các khóa được đặt tên có cùng giá trị.

.. note:: Các cặp khóa-giá trị được khớp bằng dạng có hai đối số của phương thức ``get()`` của đối tượng ánh xạ. Các cặp khóa-giá trị đã khớp phải có sẵn trong ánh xạ, không được tạo nhanh qua :meth:`~object.__missing__` hoặc :meth:`~object.__getitem__`.

Nói một cách đơn giản, ``{KEY1: P1, KEY2: P2, ... }`` chỉ khớp nếu tất cả những điều sau đây xảy ra:

* kiểm tra xem ``<subject>`` có phải là một mapping hay không
* ``KEY1 in <subject>``
* ``P1`` khớp với ``<subject>[KEY1]``
* ... và tương tự đối với từng cặp KEY/mẫu tương ứng.


.. _class-patterns:

Mẫu lớp
^^^^^^^

Mẫu lớp biểu diễn một lớp cùng các đối số vị trí và đối số từ khóa của lớp đó (nếu có). Cú pháp:

.. productionlist:: python-grammar
  class_pattern: `name_or_attr` "(" [`pattern_arguments` ","?] ")"
  pattern_arguments: `positional_patterns` ["," `keyword_patterns`]
                   : | `keyword_patterns`
  positional_patterns: ",".`pattern`+
  keyword_patterns: ",".`keyword_pattern`+
  keyword_pattern: NAME "=" `pattern`

Không nên lặp lại cùng một từ khóa trong các mẫu lớp.

Sau đây là luồng logic để khớp một mẫu lớp với một giá trị subject:

#. Nếu ``name_or_attr`` không phải là một thể hiện của :class:`type` tích hợp sẵn, hãy raise
   :exc:`TypeError`.

#. Nếu giá trị subject không phải là một thể hiện của ``name_or_attr`` (được kiểm tra thông qua
   :func:`isinstance`), mẫu lớp sẽ không khớp.

#. Nếu không có đối số mẫu, mẫu sẽ khớp. Nếu không, các bước tiếp theo phụ thuộc vào việc có các mẫu đối số từ khóa hay đối số vị trí.

   Đối với một số kiểu tích hợp sẵn (được nêu bên dưới), một subpattern vị trí duy nhất được chấp nhận và sẽ khớp với toàn bộ subject; đối với các kiểu này, các mẫu từ khóa cũng hoạt động như với những kiểu khác.

   Nếu chỉ có các mẫu từ khóa, chúng được xử lý lần lượt như sau:

   I. Từ khóa được tra cứu dưới dạng một thuộc tính trên subject.

      * Nếu thao tác này gây ra một ngoại lệ khác với :exc:`AttributeError`, ngoại lệ đó sẽ được lan truyền lên.

      * Nếu thao tác này gây ra :exc:`AttributeError`, mẫu lớp không khớp.

      * Nếu không, mẫu con liên kết với mẫu từ khóa sẽ được khớp với giá trị thuộc tính của đối tượng cần khớp. Nếu bước này thất bại, mẫu lớp không khớp; nếu thành công, quá trình khớp tiếp tục với từ khóa tiếp theo.


   II. Nếu tất cả các mẫu từ khóa đều thành công, mẫu lớp sẽ khớp.

   Nếu có bất kỳ mẫu vị trí nào, chúng sẽ được chuyển đổi thành các mẫu từ khóa bằng cách sử dụng thuộc tính :data:`~object.__match_args__` trên lớp ``name_or_attr`` trước khi khớp:

   I. Tương đương với ``getattr(cls, "__match_args__", ())`` được gọi.

      * Nếu thao tác này gây ra một ngoại lệ, ngoại lệ đó sẽ được lan truyền lên.

      * Nếu giá trị được trả về không phải là một tuple, quá trình chuyển đổi sẽ thất bại và
        :exc:`TypeError` được raised.

      * Nếu có nhiều positional pattern hơn ``len(cls.__match_args__)``, thì
        :exc:`TypeError` được raised.

      * Nếu không, positional pattern ``i`` được chuyển đổi thành keyword pattern bằng cách sử dụng ``__match_args__[i]`` làm keyword. ``__match_args__[i]`` phải là một chuỗi; nếu không, :exc:`TypeError` sẽ được raised.

      * Nếu có các keyword trùng lặp, :exc:`TypeError` sẽ được raised.

      .. seealso:: :ref:`class-pattern-matching`

   II. Sau khi tất cả positional pattern được chuyển đổi thành keyword pattern, quá trình so khớp sẽ diễn ra như thể chỉ có keyword pattern.

   Đối với các kiểu tích hợp sẵn sau đây, cách xử lý các mẫu con theo vị trí sẽ khác:

   * :class:`bool`
   * :class:`bytearray`
   * :class:`bytes`
   * :class:`dict`
   * :class:`float`
   * :class:`frozenset`
   * :class:`int`
   * :class:`list`
   * :class:`set`
   * :class:`str`
   * :class:`tuple`

   Các lớp này chấp nhận một đối số theo vị trí duy nhất, và mẫu ở đó được đối chiếu với toàn bộ đối tượng thay vì một thuộc tính. Ví dụ, ``int(0|1)`` khớp với giá trị ``0``, nhưng không khớp với giá trị ``0.0``.

Nói một cách đơn giản, ``CLS(P1, attr=P2)`` chỉ khớp nếu xảy ra tất cả những điều sau:

* ``isinstance(<subject>, CLS)``
* chuyển ``P1`` thành một mẫu từ khóa bằng cách sử dụng ``CLS.__match_args__``
* Đối với mỗi đối số từ khóa ``attr=P2``:

  * ``hasattr(<subject>, "attr")``
  * ``P2`` khớp với ``<subject>.attr``

* ... và tương tự đối với cặp đối số từ khóa/mẫu tương ứng.

.. seealso::

   * :pep:`634` -- Đối sánh mẫu cấu trúc: Đặc tả
   * :pep:`636` -- Đối sánh mẫu cấu trúc: Hướng dẫn


.. index::
   single: parameter; function definition

.. _function:
.. _def:

Định nghĩa hàm
==============

.. index::
   pair: statement; def
   pair: function; definition
   pair: function; name
   pair: name; binding
   pair: object; user-defined function
   pair: object; function
   pair: function; name
   pair: name; binding
   single: () (parentheses); function definition
   single: , (comma); parameter list
   single: : (colon); compound statement

Định nghĩa hàm định nghĩa một đối tượng hàm do người dùng định nghĩa (xem phần
:ref:`types`):

.. productionlist:: python-grammar
   funcdef: [`decorators`] "def" `funcname` [`type_params`] "(" [`parameter_list`] ")"
          : ["->" `expression`] ":" `suite`
   decorators: `decorator`+
   decorator: "@" `assignment_expression` NEWLINE
   parameter_list: `defparameter` ("," `defparameter`)* "," "/" ["," [`parameter_list_no_posonly`]]
                 :   | `parameter_list_no_posonly`
   parameter_list_no_posonly: `defparameter` ("," `defparameter`)* ["," [`parameter_list_starargs`]]
                            : | `parameter_list_starargs`
   parameter_list_starargs: "*" `star_parameter` ("," `defparameter`)* ["," [`parameter_star_kwargs`]]
                          : | "*" ("," `defparameter`)+ ["," [`parameter_star_kwargs`]]
                          : | `parameter_star_kwargs`
   parameter_star_kwargs: "**" `parameter` [","]
   parameter: `identifier` [":" `expression`]
   star_parameter: `identifier` [":" ["*"] `expression`]
   defparameter: `parameter` ["=" `expression`]
   funcname: `identifier`


Định nghĩa hàm là một câu lệnh có thể thực thi. Việc thực thi câu lệnh này liên kết tên hàm trong namespace cục bộ hiện tại với một đối tượng hàm (một wrapper bao quanh mã có thể thực thi của hàm). Đối tượng hàm này chứa một tham chiếu đến namespace toàn cục hiện tại, được dùng làm namespace toàn cục khi hàm được gọi.

Định nghĩa hàm không thực thi thân hàm; thân hàm chỉ được thực thi khi hàm được gọi. [#]_

.. index::
   single: @ (at); function definition

Một định nghĩa hàm có thể được bao bọc bởi một hoặc nhiều biểu thức :term:`decorator`. Các biểu thức decorator được đánh giá khi hàm được định nghĩa, trong phạm vi chứa định nghĩa hàm. Kết quả phải là một đối tượng có thể gọi, đối tượng này được gọi với đối số duy nhất là đối tượng hàm. Giá trị trả về được liên kết với tên hàm thay cho đối tượng hàm. Nhiều decorator được áp dụng theo cách lồng nhau. Ví dụ, đoạn mã sau đây::

   @f1(arg)
   @f2
   def func(): pass

tương đương về cơ bản với::

   def func(): pass
   func = f1(arg)(f2(func))

ngoại trừ việc hàm ban đầu không được tạm thời liên kết với tên ``func``.

.. versionchanged:: 3.9
   Các hàm có thể được trang trí bằng bất kỳ
   :token:`~python-grammar:assignment_expression` hợp lệ nào. Trước đây, cú pháp bị hạn chế hơn nhiều; xem :pep:`614` để biết chi tiết.

Có thể cung cấp một danh sách :ref:`tham số kiểu <type-params>` trong dấu ngoặc vuông giữa tên hàm và dấu ngoặc đơn mở đầu cho danh sách tham số của hàm. Điều này cho các trình kiểm tra kiểu tĩnh biết rằng hàm là generic. Trong runtime, có thể truy xuất các tham số kiểu từ
thuộc tính :attr:`~function.__type_params__`. Xem :ref:`generic-functions` để biết thêm.

.. versionchanged:: 3.12
   Danh sách tham số kiểu là tính năng mới trong Python 3.12.

.. index::
   triple: default; parameter; value
   single: argument; function definition
   single: = (equals); function definition

Khi một hoặc nhiều :term:`tham số <parameter>` có dạng *tham số* ``=`` *biểu thức*, hàm được gọi là có "giá trị tham số mặc định". Đối với tham số có giá trị mặc định, :term:`argument` tương ứng có thể được lược bỏ khi gọi hàm; khi đó, giá trị mặc định của tham số sẽ được thay thế. Nếu một tham số có giá trị mặc định, tất cả các tham số tiếp theo cho đến "``*``" cũng phải có giá trị mặc định — đây là một hạn chế cú pháp không được thể hiện trong grammar.

**Giá trị tham số mặc định được đánh giá từ trái sang phải khi định nghĩa hàm được thực thi.** Điều này có nghĩa là biểu thức được đánh giá một lần, khi hàm được định nghĩa, và cùng một giá trị "được tính toán trước" sẽ được sử dụng cho mỗi lần gọi. Điều này đặc biệt quan trọng khi giá trị tham số mặc định là một đối tượng mutable, chẳng hạn như list hoặc dictionary: nếu hàm sửa đổi đối tượng đó (ví dụ: thêm một phần tử vào list), thì giá trị tham số mặc định trên thực tế cũng bị sửa đổi. Đây thường không phải là điều mong muốn. Một cách giải quyết là sử dụng ``None`` làm giá trị mặc định, rồi kiểm tra rõ ràng giá trị này trong phần thân hàm, ví dụ::

   def whats_on_the_telly(penguin=None):
       if penguin is None:
           penguin = []
       penguin.append("property of the zoo")
       return penguin

.. index::
   single: / (slash); function definition
   single: * (asterisk); function definition
   single: **; function definition

Ngữ nghĩa của việc gọi hàm được mô tả chi tiết hơn trong phần :ref:`calls`. Một lệnh gọi hàm luôn gán giá trị cho tất cả các tham số được nêu trong danh sách tham số, từ đối số vị trí, đối số keyword hoặc giá trị mặc định. Nếu có dạng "``*identifier``", nó được khởi tạo thành một tuple nhận mọi tham số vị trí dư thừa, mặc định là tuple rỗng. Nếu có dạng "``**identifier``", nó được khởi tạo thành một ordered mapping mới nhận mọi đối số keyword dư thừa, mặc định là một mapping rỗng mới cùng kiểu. Các tham số đứng sau "``*``" hoặc "``*identifier``" là các tham số chỉ dùng keyword và chỉ có thể được truyền bằng đối số keyword. Các tham số đứng trước "``/``" là các tham số chỉ dùng vị trí và chỉ có thể được truyền bằng đối số vị trí.

.. versionchanged:: 3.8
   Cú pháp tham số hàm ``/`` có thể được dùng để chỉ ra các tham số chỉ dùng vị trí. Xem :pep:`570` để biết chi tiết.

.. index::
   pair: function; annotations
   single: ->; function annotations
   single: : (colon); function annotations

Tham số có thể có :term:`chú thích <function annotation>` với dạng "``: expression``" theo sau tên tham số. Bất kỳ tham số nào cũng có thể có chú thích, kể cả các tham số có dạng ``*identifier`` hoặc ``**identifier``. (Một trường hợp đặc biệt là các tham số có dạng ``*identifier`` có thể có chú thích "``: *expression``".) Hàm có thể có chú thích "return" với dạng "``-> expression``" sau danh sách tham số. Các chú thích này có thể là bất kỳ biểu thức Python hợp lệ nào. Sự hiện diện của chú thích không làm thay đổi ngữ nghĩa của hàm. Xem :ref:`annotations` để biết thêm thông tin về chú thích.

.. versionchanged:: 3.11
   Các tham số có dạng "``*identifier``" có thể có chú thích "``: *expression``". Xem :pep:`646`.

.. index:: pair: lambda; expression

Cũng có thể tạo các hàm ẩn danh (những hàm không được liên kết với tên) để sử dụng ngay trong các biểu thức. Cách này sử dụng các biểu thức lambda, được mô tả trong phần :ref:`lambda`. Lưu ý rằng biểu thức lambda chỉ là cách viết tắt cho một định nghĩa hàm đơn giản hóa; một hàm được định nghĩa trong câu lệnh ":keyword:`def`" có thể được truyền qua hoặc gán cho một tên khác giống như một hàm được định nghĩa bằng biểu thức lambda. Dạng ":keyword:`!def`" thực sự mạnh hơn vì cho phép thực thi nhiều câu lệnh và chú thích.

**Ghi chú dành cho lập trình viên:** Các hàm là những đối tượng hạng nhất. Một câu lệnh "``def``" được thực thi bên trong phần định nghĩa hàm sẽ định nghĩa một hàm cục bộ có thể được trả về hoặc truyền đi. Các biến tự do được sử dụng trong hàm lồng nhau có thể truy cập các biến cục bộ của hàm chứa câu lệnh def. Xem phần
:ref:`naming` để biết chi tiết.

.. seealso::

   :pep:`3107` - Chú thích hàm
      Đặc tả ban đầu cho chú thích hàm.

   :pep:`484` - Gợi ý kiểu
      Định nghĩa ý nghĩa tiêu chuẩn cho các chú thích: gợi ý kiểu.

   :pep:`526` - Cú pháp cho chú thích biến
      Khả năng thêm type hint cho các khai báo biến, bao gồm biến lớp và biến thực thể.

   :pep:`563` - Đánh giá trì hoãn các chú thích
      Hỗ trợ các tham chiếu chuyển tiếp trong chú thích bằng cách giữ chú thích ở dạng chuỗi trong runtime thay vì đánh giá ngay.

   :pep:`318` - Decorator cho hàm và phương thức
      Decorator cho hàm và phương thức đã được giới thiệu. Decorator cho lớp đã được giới thiệu trong :pep:`3129`.

.. _class:

Khai báo lớp
============

.. index::
   pair: object; class
   pair: statement; class
   pair: class; definition
   pair: class; name
   pair: name; binding
   pair: execution; frame
   single: inheritance
   single: docstring
   single: () (parentheses); class definition
   single: , (comma); expression list
   single: : (colon); compound statement

Một khai báo lớp định nghĩa một đối tượng lớp (xem phần :ref:`types`):

.. productionlist:: python-grammar
   classdef: [`decorators`] "class" `classname` [`type_params`] [`inheritance`] ":" `suite`
   inheritance: "(" [`argument_list`] ")"
   classname: `identifier`

Định nghĩa lớp là một câu lệnh có thể thực thi. Danh sách kế thừa thường cung cấp danh sách các lớp cơ sở (xem :ref:`metaclasses` để biết các cách sử dụng nâng cao hơn), vì vậy mỗi mục trong danh sách phải được đánh giá thành một đối tượng lớp cho phép tạo lớp con. Các lớp không có danh sách kế thừa mặc định kế thừa từ lớp cơ sở :class:`object`; do đó,::

   class Foo:
       pass

tương đương với::

   class Foo(object):
       pass

Sau đó, suite của lớp được thực thi trong một frame thực thi mới (xem :ref:`naming`), sử dụng một namespace cục bộ mới được tạo và namespace toàn cục ban đầu. (Thông thường, suite chủ yếu chứa các định nghĩa hàm.) Khi suite của lớp hoàn tất việc thực thi, frame thực thi của nó bị loại bỏ nhưng namespace cục bộ được lưu lại. [#]_ Sau đó, một đối tượng lớp được tạo bằng cách sử dụng danh sách kế thừa cho các lớp cơ sở và namespace cục bộ đã lưu cho từ điển thuộc tính. Tên lớp được liên kết với đối tượng lớp này trong namespace cục bộ ban đầu.

Thứ tự định nghĩa các thuộc tính trong phần thân lớp được giữ nguyên trong :attr:`~type.__dict__` của lớp mới. Lưu ý rằng điều này chỉ đáng tin cậy ngay sau khi lớp được tạo và chỉ áp dụng cho các lớp được định nghĩa bằng cú pháp định nghĩa.

Việc tạo lớp có thể được tùy chỉnh rất nhiều bằng cách sử dụng :ref:`metaclasses <metaclasses>`.

.. index::
   single: @ (at); class definition

Các lớp cũng có thể được áp dụng decorator: cũng giống như khi áp dụng decorator cho các hàm,::

   @f1(arg)
   @f2
   class Foo: pass

tương đương gần đúng với::

   class Foo: pass
   Foo = f1(arg)(f2(Foo))

Các quy tắc đánh giá đối với các biểu thức decorator cũng giống như đối với decorator của hàm. Sau đó, kết quả được gán cho tên lớp.

.. versionchanged:: 3.9
   Các lớp có thể được decorate bằng bất kỳ
   :token:`~python-grammar:assignment_expression`. Trước đây, ngữ pháp hạn chế hơn nhiều; xem :pep:`614` để biết chi tiết.

Một danh sách :ref:`tham số kiểu <type-params>` có thể được đặt trong dấu ngoặc vuông ngay sau tên lớp. Điều này cho các trình kiểm tra kiểu tĩnh biết rằng lớp này là generic. Trong runtime, có thể lấy các tham số kiểu từ
:attr:`~type.__type_params__` thuộc tính của lớp. Xem :ref:`generic-classes` để biết thêm.

.. versionchanged:: 3.12
   Danh sách tham số kiểu là tính năng mới trong Python 3.12.

**Lưu ý của lập trình viên:** Các biến được định nghĩa trong phần định nghĩa lớp là thuộc tính lớp; chúng được dùng chung bởi các instance. Có thể thiết lập thuộc tính instance trong một method bằng ``self.name = value``. Cả thuộc tính lớp và thuộc tính instance đều có thể được truy cập bằng ký hiệu "``self.name``", và thuộc tính instance sẽ ẩn thuộc tính lớp có cùng tên khi được truy cập theo cách này. Có thể dùng thuộc tính lớp làm giá trị mặc định cho thuộc tính instance, nhưng việc sử dụng các giá trị có thể thay đổi ở đó có thể dẫn đến kết quả không mong muốn. Có thể dùng :ref:`bộ mô tả <descriptors>` để tạo các biến instance với các chi tiết triển khai khác nhau.


.. seealso::

   :pep:`3115` - Các metaclass trong Python 3000
      Đề xuất đã thay đổi cách khai báo metaclass sang cú pháp hiện tại, cũng như ngữ nghĩa về cách các lớp có metaclass được tạo.

   :pep:`3129` - Các decorator của lớp
      Đề xuất đã bổ sung decorator cho lớp. Decorator cho hàm và phương thức được giới thiệu trong :pep:`318`.


.. _async:

Coroutine
=========

.. versionadded:: 3.5

.. index:: pair: statement; async def
.. _`async def`:

Định nghĩa hàm coroutine
------------------------

.. productionlist:: python-grammar
   async_funcdef: [`decorators`] "async" "def" `funcname` "(" [`parameter_list`] ")"
                : ["->" `expression`] ":" `suite`

.. index::
   pair: keyword; async
   pair: keyword; await

Việc thực thi các coroutine Python có thể bị tạm dừng và tiếp tục tại nhiều điểm (xem :term:`coroutine`). Các biểu thức :keyword:`await`, :keyword:`async for` và
:keyword:`async with` chỉ có thể được sử dụng trong phần thân của một hàm coroutine.

Các hàm được định nghĩa bằng cú pháp ``async def`` luôn là hàm coroutine, ngay cả khi chúng không chứa các từ khóa ``await`` hoặc ``async``.

Việc sử dụng một biểu thức ``yield from`` trong phần thân của hàm coroutine là một :exc:`SyntaxError`.

Một ví dụ về hàm coroutine::

    async def func(param1, param2):
        do_stuff()
        await some_coroutine()

.. versionchanged:: 3.7
   ``await`` và ``async`` hiện là các từ khóa; trước đây, chúng chỉ được xử lý như vậy bên trong phần thân của hàm coroutine.

.. index:: pair: statement; async for
.. _`async for`:

Câu lệnh :keyword:`!async for`
------------------------------

.. productionlist:: python-grammar
   async_for_stmt: "async" `for_stmt`

Một :term:`asynchronous iterable` cung cấp một phương thức ``__aiter__`` trực tiếp trả về một :term:`asynchronous iterator`, cho phép gọi mã bất đồng bộ trong phương thức ``__anext__`` của nó.

Câu lệnh ``async for`` cho phép lặp thuận tiện qua các iterable bất đồng bộ.

Đoạn mã sau đây::

    async for TARGET in ITER:
        SUITE
    else:
        SUITE2

Về mặt ngữ nghĩa tương đương với::

    iter = (ITER).__aiter__()
    running = True

    while running:
        try:
            TARGET = await iter.__anext__()
        except StopAsyncIteration:
            running = False
        else:
            SUITE
    else:
        SUITE2

ngoại trừ việc tra cứu :ref:`phương thức đặc biệt <special-lookup>` ngầm định được sử dụng cho :meth:`~object.__aiter__` và :meth:`~object.__anext__`.

Việc sử dụng câu lệnh ``async for`` bên ngoài thân của một hàm coroutine sẽ gây ra :exc:`SyntaxError`.


.. index:: pair: statement; async with
.. _`async with`:

Câu lệnh :keyword:`!async with`
-------------------------------

.. productionlist:: python-grammar
   async_with_stmt: "async" `with_stmt`

Một :term:`asynchronous context manager` là một :term:`context manager` có khả năng tạm dừng quá trình thực thi trong các phương thức *enter* và *exit*.

Đoạn mã sau::

    async with EXPRESSION as TARGET:
        SUITE

tương đương về mặt ngữ nghĩa với::

    manager = (EXPRESSION)
    aenter = manager.__aenter__
    aexit = manager.__aexit__
    value = await aenter()
    hit_except = False

    try:
        TARGET = value
        SUITE
    except:
        hit_except = True
        if not await aexit(*sys.exc_info()):
            raise
    finally:
        if not hit_except:
            await aexit(None, None, None)

ngoại trừ việc tra cứu :ref:`phương thức đặc biệt <special-lookup>` ngầm định được sử dụng cho :meth:`~object.__aenter__` và :meth:`~object.__aexit__`.

Đây là một :exc:`SyntaxError` khi sử dụng một câu lệnh ``async with`` bên ngoài thân của một hàm coroutine.

.. seealso::

   :pep:`492` - Coroutine với cú pháp async và await
      Đề xuất biến coroutine thành một khái niệm độc lập đúng nghĩa trong Python và bổ sung cú pháp hỗ trợ.

.. _type-params:

Danh sách tham số kiểu
======================

.. versionadded:: 3.12

.. versionchanged:: 3.13
   Hỗ trợ các giá trị mặc định đã được bổ sung (xem :pep:`696`).

.. index::
   single: type parameters

.. productionlist:: python-grammar
   type_params: "[" `type_param` ("," `type_param`)* "]"
   type_param: `typevar` | `typevartuple` | `paramspec`
   typevar: `identifier` (":" `expression`)? ("=" `expression`)?
   typevartuple: "*" `identifier` ("=" `expression`)?
   paramspec: "**" `identifier` ("=" `expression`)?

:ref:`Hàm <def>` (bao gồm :ref:`coroutine <async def>`),
:ref:`lớp <class>` và :ref:`bí danh kiểu <type>` có thể chứa danh sách tham số kiểu::

   def max[T](args: list[T]) -> T:
       ...

   async def amax[T](args: list[T]) -> T:
       ...

   class Bag[T]:
       def __iter__(self) -> Iterator[T]:
           ...

       def add(self, arg: T) -> None:
           ...

   type ListOrSet[T] = list[T] | set[T]

Về mặt ngữ nghĩa, điều này cho biết rằng hàm, lớp hoặc bí danh kiểu là generic trên một biến kiểu. Thông tin này chủ yếu được trình kiểm tra kiểu tĩnh sử dụng; tại thời điểm chạy, các đối tượng generic hoạt động gần giống như các đối tượng không generic tương ứng.

Các tham số kiểu được khai báo trong dấu ngoặc vuông (``[]``) ngay sau tên của hàm, lớp hoặc bí danh kiểu. Các tham số kiểu có thể được truy cập trong phạm vi của đối tượng generic, nhưng không thể truy cập ở nơi khác. Vì vậy, sau một khai báo ``def func[T](): pass``, tên ``T`` không khả dụng trong phạm vi module. Phần dưới đây mô tả chính xác hơn ngữ nghĩa của các đối tượng generic. Phạm vi của các tham số kiểu được mô hình hóa bằng một hàm đặc biệt (về mặt kỹ thuật là :ref:`phạm vi chú thích <annotation-scopes>`) bao bọc việc tạo đối tượng generic.

Các hàm, lớp và bí danh kiểu generic có một
:attr:`~definition.__type_params__` thuộc tính liệt kê các tham số kiểu của chúng.

Tham số kiểu có ba loại:

* :data:`typing.TypeVar`, được giới thiệu bằng một tên đơn (ví dụ: ``T``). Về mặt ngữ nghĩa, tham số này biểu diễn một kiểu duy nhất đối với trình kiểm tra kiểu.
* :data:`typing.TypeVarTuple`, được giới thiệu bằng một tên có tiền tố là một dấu hoa thị (ví dụ: ``*Ts``). Về mặt ngữ nghĩa, tham số này đại diện cho một tuple chứa bất kỳ số lượng kiểu nào.
* :data:`typing.ParamSpec`, được giới thiệu bằng một tên có tiền tố là hai dấu hoa thị (ví dụ: ``**P``). Về mặt ngữ nghĩa, tham số này đại diện cho các tham số của một callable.

Các khai báo :data:`typing.TypeVar` có thể định nghĩa *giới hạn* và *ràng buộc* bằng dấu hai chấm (``:``) theo sau là một biểu thức. Một biểu thức duy nhất sau dấu hai chấm cho biết một giới hạn (ví dụ: ``T: int``). Về mặt ngữ nghĩa, điều này có nghĩa là :data:`!typing.TypeVar` chỉ có thể đại diện cho các kiểu là kiểu con của giới hạn này. Một tuple biểu thức được đặt trong dấu ngoặc đơn sau dấu hai chấm cho biết một tập hợp các ràng buộc (ví dụ: ``T: (str, bytes)``). Mỗi phần tử trong tuple phải là một kiểu (một lần nữa, điều này không được thực thi tại runtime). Các biến kiểu bị ràng buộc chỉ có thể nhận một trong các kiểu thuộc danh sách ràng buộc.

Đối với :data:`!typing.TypeVar`\ s được khai báo bằng cú pháp danh sách tham số kiểu, giới hạn và các ràng buộc không được đánh giá khi đối tượng generic được tạo mà chỉ được đánh giá khi giá trị được truy cập rõ ràng thông qua các thuộc tính ``__bound__`` và ``__constraints__``. Để thực hiện điều này, các giới hạn hoặc ràng buộc được đánh giá trong một :ref:`phạm vi chú thích <annotation-scopes>` riêng biệt.

:data:`typing.TypeVarTuple`\ s và :data:`typing.ParamSpec`\ s không thể có giới hạn hoặc ràng buộc.

Cả ba dạng tham số kiểu đều có thể có *giá trị mặc định*, được sử dụng khi tham số kiểu không được cung cấp một cách rõ ràng. Giá trị này được thêm bằng cách nối một dấu bằng đơn (``=``) theo sau là một biểu thức. Giống như các bound và constraint của biến kiểu, giá trị mặc định không được đánh giá khi đối tượng được tạo, mà chỉ khi thuộc tính ``__default__`` của tham số kiểu được truy cập. Vì mục đích này, giá trị mặc định được đánh giá trong một
:ref:`phạm vi chú thích <annotation-scopes>`. Nếu không chỉ định giá trị mặc định cho tham số kiểu, thuộc tính ``__default__`` sẽ được đặt thành đối tượng sentinel đặc biệt :data:`typing.NoDefault`.

Ví dụ sau đây cho biết đầy đủ các khai báo tham số kiểu được phép::

   def overly_generic[
      SimpleTypeVar,
      TypeVarWithDefault = int,
      TypeVarWithBound: int,
      TypeVarWithConstraints: (str, bytes),
      *SimpleTypeVarTuple = (int, float),
      **SimpleParamSpec = (str, bytearray),
   ](
      a: SimpleTypeVar,
      b: TypeVarWithDefault,
      c: TypeVarWithBound,
      d: Callable[SimpleParamSpec, TypeVarWithConstraints],
      *e: SimpleTypeVarTuple,
   ): ...

.. _generic-functions:

Các hàm generic
---------------

Các hàm generic được khai báo như sau::

   def func[T](arg: T): ...

Cú pháp này tương đương với::

   annotation-def TYPE_PARAMS_OF_func():
       T = typing.TypeVar("T")
       def func(arg: T): ...
       func.__type_params__ = (T,)
       return func
   func = TYPE_PARAMS_OF_func()

Ở đây, ``annotation-def`` cho biết một :ref:`phạm vi chú thích <annotation-scopes>`, trên thực tế không được liên kết với bất kỳ tên nào trong runtime. (Một điểm linh hoạt khác được áp dụng trong bản dịch: cú pháp này không thực hiện truy cập thuộc tính trên module :mod:`typing`, mà tạo một thực thể của
:data:`typing.TypeVar` trực tiếp.)

Các chú thích của generic function được đánh giá trong phạm vi chú thích được sử dụng để khai báo các tham số kiểu, nhưng các giá trị mặc định và decorator của hàm thì không.

Ví dụ sau minh họa các quy tắc về phạm vi cho những trường hợp này, cũng như các dạng tham số kiểu bổ sung::

   @decorator
   def func[T: int, *Ts, **P](*args: *Ts, arg: Callable[P, T] = some_default):
       ...

Ngoại trừ việc :ref:`đánh giá lười <lazy-evaluation>` của
:class:`~typing.TypeVar` đã được liên kết, điều này tương đương với::

   DEFAULT_OF_arg = some_default

   annotation-def TYPE_PARAMS_OF_func():

       annotation-def BOUND_OF_T():
           return int
       # Trên thực tế, BOUND_OF(T)() chỉ được đánh giá khi có yêu cầu.
       T = typing.TypeVar("T", bound=BOUND_OF_T())

       Ts = typing.TypeVarTuple("Ts")
       P = typing.ParamSpec("P")

       def func(*args: *Ts, arg: Callable[P, T] = DEFAULT_OF_arg):
           ...

       func.__type_params__ = (T, Ts, P)
       return func
   func = decorator(TYPE_PARAMS_OF_func())

Các tên viết hoa như ``DEFAULT_OF_arg`` thực tế không được liên kết trong runtime.

.. _generic-classes:

Các lớp generic
---------------

Các lớp generic được khai báo như sau::

   class Bag[T]: ...

Cú pháp này tương đương với::

   annotation-def TYPE_PARAMS_OF_Bag():
       T = typing.TypeVar("T")
       class Bag(typing.Generic[T]):
           __type_params__ = (T,)
           ...
       return Bag
   Bag = TYPE_PARAMS_OF_Bag()

Ở đây, một lần nữa ``annotation-def`` (không phải từ khóa thực) chỉ một
:ref:`phạm vi annotation <annotation-scopes>`, còn tên ``TYPE_PARAMS_OF_Bag`` thực tế không được liên kết trong runtime.

Các lớp generic ngầm kế thừa từ :data:`typing.Generic`. Các lớp cơ sở và đối số từ khóa của các lớp generic được đánh giá trong phạm vi kiểu dành cho các tham số kiểu, còn các decorator được đánh giá bên ngoài phạm vi đó. Ví dụ sau minh họa điều này::

   @decorator
   class Bag(Base[T], arg=T): ...

Điều này tương đương với::

   annotation-def TYPE_PARAMS_OF_Bag():
       T = typing.TypeVar("T")
       class Bag(Base[T], typing.Generic[T], arg=T):
           __type_params__ = (T,)
           ...
       return Bag
   Bag = decorator(TYPE_PARAMS_OF_Bag())

.. _generic-type-aliases:

Bí danh kiểu generic
--------------------

Câu lệnh :keyword:`type` cũng có thể được dùng để tạo bí danh kiểu generic::

   type ListOrSet[T] = list[T] | set[T]

Ngoại trừ :ref:`việc đánh giá lười <lazy-evaluation>` của giá trị, điều này tương đương với::

   annotation-def TYPE_PARAMS_OF_ListOrSet():
       T = typing.TypeVar("T")

       annotation-def VALUE_OF_ListOrSet():
           return list[T] | set[T]
       # Trên thực tế, giá trị được đánh giá lười
       return typing.TypeAliasType("ListOrSet", VALUE_OF_ListOrSet(), type_params=(T,))
   ListOrSet = TYPE_PARAMS_OF_ListOrSet()

Ở đây, ``annotation-def`` (không phải là một từ khóa thực sự) biểu thị một
:ref:`phạm vi chú thích <annotation-scopes>`. Các tên viết hoa như ``TYPE_PARAMS_OF_ListOrSet`` thực tế không được liên kết trong runtime.

.. _annotations:

Chú thích
=========

.. versionchanged:: 3.14
   Giờ đây, chú thích được đánh giá một cách lười biếng theo mặc định.

Biến và tham số hàm có thể mang :term:`chú thích <annotation>`, được tạo bằng cách thêm dấu hai chấm sau tên, tiếp theo là một biểu thức::

   x: annotation = 1
   def f(param: annotation): ...

Hàm cũng có thể mang chú thích giá trị trả về theo sau một mũi tên::

   def f() -> annotation: ...

Chú thích thường được dùng cho :term:`gợi ý kiểu (type hints) <type hint>`, nhưng điều này không được ngôn ngữ bắt buộc, và nhìn chung chú thích có thể chứa các biểu thức tùy ý. Sự hiện diện của chú thích không làm thay đổi ngữ nghĩa runtime của mã, trừ khi có một cơ chế được sử dụng để kiểm tra nội quan và dùng các chú thích đó (chẳng hạn như :mod:`dataclasses` hoặc :deco:`functools.singledispatch`).

Theo mặc định, chú thích được đánh giá một cách lười biếng trong một :ref:`phạm vi chú thích <annotation-scopes>`. Điều này có nghĩa là chúng không được đánh giá khi mã chứa chú thích được đánh giá. Thay vào đó, trình thông dịch lưu thông tin có thể được dùng để đánh giá chú thích sau này nếu được yêu cầu. Mô-đun :mod:`annotationlib` cung cấp các công cụ để đánh giá chú thích.

Nếu :ref:`câu lệnh future <future>` ``from __future__ import annotations`` xuất hiện, tất cả chú thích sẽ được lưu trữ dưới dạng chuỗi::

   >>> from __future__ import annotations
   >>> def f(param: annotation): ...
   >>> f.__annotations__
   {'param': 'annotation'}

Câu lệnh future này sẽ bị phản đối và loại bỏ trong một phiên bản Python trong tương lai, nhưng không sớm hơn thời điểm Python 3.13 kết thúc vòng đời (xem :pep:`749`). Khi được sử dụng, các công cụ kiểm tra nội quan như
:func:`annotationlib.get_annotations` và :func:`typing.get_type_hints` ít có khả năng phân giải được các annotation tại runtime hơn.


.. rubric:: Chú thích cuối trang

.. [#] Ngoại lệ được truyền lên ngăn xếp gọi, trừ khi có một mệnh đề :keyword:`finally` vô tình phát sinh một ngoại lệ khác. Ngoại lệ mới đó khiến ngoại lệ cũ bị mất.

.. [#] Trong pattern matching, một sequence được định nghĩa là một trong những dạng sau:

   * một class kế thừa từ :class:`collections.abc.Sequence`
   * một Python class đã được đăng ký là :class:`collections.abc.Sequence`
   * một builtin class có bit :c:macro:`Py_TPFLAGS_SEQUENCE` (CPython) được thiết lập
   * một class kế thừa từ bất kỳ class nào ở trên

   Các class trong standard library sau đây là sequence:

   * :class:`array.array`
   * :class:`collections.deque`
   * :class:`list`
   * :class:`memoryview`
   * :class:`range`
   * :class:`tuple`

   .. note:: Các giá trị subject thuộc kiểu ``str``, ``bytes`` và ``bytearray`` không khớp với các sequence pattern.

.. [#] Trong pattern matching, mapping được định nghĩa là một trong các dạng sau:

   * một class kế thừa từ :class:`collections.abc.Mapping`
   * một Python class đã được đăng ký làm :class:`collections.abc.Mapping`
   * một built-in class có bit :c:macro:`Py_TPFLAGS_MAPPING` (CPython) được thiết lập
   * một class kế thừa từ bất kỳ class nào ở trên

   Các lớp trong thư viện chuẩn :class:`dict` và :class:`types.MappingProxyType` là các ánh xạ.

.. [#] Một string literal xuất hiện dưới dạng câu lệnh đầu tiên trong phần thân hàm sẽ được chuyển thành thuộc tính :attr:`~function.__doc__` của hàm và do đó trở thành :term:`docstring` của hàm.

.. [#] Một string literal xuất hiện dưới dạng câu lệnh đầu tiên trong phần thân lớp sẽ được chuyển thành mục :attr:`~type.__doc__` của namespace và do đó trở thành :term:`docstring` của lớp.
