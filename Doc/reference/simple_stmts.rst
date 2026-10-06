
.. _simple:

*****************
Câu lệnh đơn giản
*****************

.. index:: pair: simple; statement

Một câu lệnh đơn giản nằm trong một dòng logic duy nhất. Một dòng có thể chứa nhiều câu lệnh đơn giản, được phân tách bằng dấu chấm phẩy. Cú pháp của câu lệnh đơn giản là:

.. productionlist:: python-grammar
   simple_stmt: `expression_stmt`
              : | `assert_stmt`
              : | `assignment_stmt`
              : | `augmented_assignment_stmt`
              : | `annotated_assignment_stmt`
              : | `pass_stmt`
              : | `del_stmt`
              : | `return_stmt`
              : | `yield_stmt`
              : | `raise_stmt`
              : | `break_stmt`
              : | `continue_stmt`
              : | `import_stmt`
              : | `future_stmt`
              : | `global_stmt`
              : | `nonlocal_stmt`
              : | `type_stmt`


.. _exprstmts:

Câu lệnh biểu thức
==================

.. index::
   pair: expression; statement
   pair: expression; list
.. index:: pair: expression; list

Câu lệnh biểu thức được sử dụng (chủ yếu trong chế độ tương tác) để tính toán và ghi một giá trị, hoặc (thường là) gọi một thủ tục (một hàm không trả về kết quả có ý nghĩa; trong Python, thủ tục trả về giá trị ``None``). Các cách sử dụng khác của câu lệnh biểu thức cũng được cho phép và đôi khi hữu ích. Cú pháp của câu lệnh biểu thức là:

.. productionlist:: python-grammar
   expression_stmt: `starred_expression`

Một câu lệnh biểu thức đánh giá danh sách biểu thức (có thể chỉ gồm một biểu thức).

.. index::
   pair: built-in function; repr
   pair: object; None
   pair: string; conversion
   single: output
   pair: standard; output
   pair: writing; values
   pair: procedure; call

Trong chế độ tương tác, nếu giá trị không phải là ``None``, giá trị đó được chuyển đổi thành chuỗi bằng hàm tích hợp sẵn :func:`repr`, rồi chuỗi kết quả được ghi ra đầu ra tiêu chuẩn trên một dòng riêng (trừ khi kết quả là ``None``, để các lệnh gọi thủ tục không tạo ra đầu ra nào.)

.. _assignment:

Câu lệnh gán
============

.. index::
   single: = (equals); assignment statement
   pair: assignment; statement
   pair: binding; name
   pair: rebinding; name
   pair: object; mutable
   pair: attribute; assignment

Câu lệnh gán được dùng để (gán lại) tên với các giá trị và sửa đổi các thuộc tính hoặc mục của những đối tượng có thể thay đổi:

.. productionlist:: python-grammar
   assignment_stmt: (`target_list` "=")+ (`starred_expression` | `yield_expression`)
   target_list: `target` ("," `target`)* [","]
   target: `identifier`
         : | "(" [`target_list`] ")"
         : | "[" [`target_list`] "]"
         : | `attributeref`
         : | `subscription`
         : | "*" `target`

(Xem mục :ref:`primaries` để biết định nghĩa cú pháp của *attributeref* và *subscription*.)

Một câu lệnh gán đánh giá danh sách biểu thức (hãy nhớ rằng danh sách này có thể là một biểu thức duy nhất hoặc một danh sách được phân tách bằng dấu phẩy; trường hợp sau tạo ra một tuple) và gán đối tượng duy nhất thu được cho từng danh sách đích, từ trái sang phải.

.. index::
   single: target
   pair: target; list

Việc gán được định nghĩa đệ quy tùy thuộc vào dạng của đích (list). Khi một đích là một phần của đối tượng có thể thay đổi (một tham chiếu thuộc tính hoặc phép subscription), đối tượng có thể thay đổi đó cuối cùng phải thực hiện phép gán và quyết định tính hợp lệ của nó, đồng thời có thể phát sinh một exception nếu phép gán không được chấp nhận. Các quy tắc được những kiểu khác nhau tuân theo và các exception được phát sinh được nêu cùng với định nghĩa của các kiểu đối tượng (xem mục :ref:`types`).

.. index:: triple: target; list; assignment
   single: , (comma); in target list
   single: * (asterisk); in assignment target list
   single: [] (square brackets); in assignment target list
   single: () (parentheses); in assignment target list

Việc gán một đối tượng cho một danh sách đích, tùy chọn được đặt trong dấu ngoặc đơn hoặc dấu ngoặc vuông, được định nghĩa đệ quy như sau.

* Nếu danh sách đích là một đích duy nhất không có dấu phẩy ở cuối, tùy chọn được đặt trong dấu ngoặc đơn, thì đối tượng được gán cho đích đó.

* Ngược lại:

  * Nếu danh sách đích chứa một đích có tiền tố là dấu hoa thị, được gọi là đích "có dấu sao": Đối tượng phải là một iterable có ít nhất số lượng phần tử bằng số đích trong danh sách đích trừ đi một. Các phần tử đầu tiên của iterable được gán, từ trái sang phải, cho các đích nằm trước đích có dấu sao. Các phần tử cuối cùng của iterable được gán cho các đích nằm sau đích có dấu sao. Sau đó, một danh sách gồm các phần tử còn lại trong iterable được gán cho đích có dấu sao (danh sách này có thể rỗng).

  * Nếu không: Đối tượng phải là một iterable có số lượng phần tử bằng số đích trong danh sách đích, và các phần tử được gán, từ trái sang phải, cho các đích tương ứng.

Việc gán một đối tượng cho một đích duy nhất được định nghĩa đệ quy như sau.

* Nếu đích là một identifier (tên):

  * Nếu tên không xuất hiện trong câu lệnh :keyword:`global` hoặc :keyword:`nonlocal` trong khối mã hiện tại: tên được liên kết với đối tượng trong namespace cục bộ hiện tại.

  * Nếu không: tên được liên kết với đối tượng trong namespace toàn cục hoặc namespace bên ngoài do :keyword:`nonlocal` xác định, tương ứng.

  .. index:: single: destructor

  Tên được liên kết lại nếu trước đó nó đã được liên kết. Điều này có thể khiến số lượng tham chiếu của đối tượng trước đó được liên kết với tên giảm xuống 0, làm đối tượng được giải phóng và destructor của nó (nếu có) được gọi.

  .. index:: pair: attribute; assignment

* Nếu đích là một tham chiếu thuộc tính: Biểu thức chính trong tham chiếu được đánh giá. Biểu thức này phải trả về một đối tượng có các thuộc tính có thể gán; nếu không, :exc:`TypeError` sẽ được phát sinh. Sau đó, đối tượng đó được yêu cầu gán đối tượng được gán vào thuộc tính đã cho; nếu không thể thực hiện phép gán, nó sẽ phát sinh một ngoại lệ (thường nhưng không nhất thiết
  :exc:`AttributeError`).

  .. _attr-target-note:

  Lưu ý: Nếu đối tượng là một thể hiện của lớp và tham chiếu thuộc tính xuất hiện ở cả hai vế của toán tử gán, biểu thức ở vế phải, ``a.x`` có thể truy cập một thuộc tính của thể hiện hoặc (nếu không có thuộc tính của thể hiện) một thuộc tính của lớp. Đích ở vế trái ``a.x`` luôn được đặt làm thuộc tính của thể hiện, tạo thuộc tính đó nếu cần. Vì vậy, hai lần xuất hiện của ``a.x`` không nhất thiết tham chiếu đến cùng một thuộc tính: nếu biểu thức ở vế phải tham chiếu đến một thuộc tính của lớp, vế trái sẽ tạo một thuộc tính mới của thể hiện làm đích của phép gán::

     class Cls:
         x = 3             # biến lớp
     inst = Cls()
     inst.x = inst.x + 1   # ghi inst.x là 4, giữ Cls.x là 3

  Mô tả này không nhất thiết áp dụng cho các thuộc tính descriptor, chẳng hạn như các property được tạo bằng :deco:`property`.

  .. index::
     pair: subscription; assignment
     pair: object; mutable

* Nếu đích là một phép truy cập theo chỉ số: Biểu thức chính trong tham chiếu được đánh giá. Tiếp theo, biểu thức chỉ số được đánh giá. Sau đó, phương thức :meth:`~object.__setitem__` của biểu thức chính được gọi với hai đối số: chỉ số và đối tượng được gán.

  Thông thường, :meth:`~object.__setitem__` được định nghĩa trên các đối tượng sequence có thể thay đổi (chẳng hạn như list) và các đối tượng mapping (chẳng hạn như dictionary), và hoạt động như sau.

  .. index::
     pair: object; sequence
     pair: object; list

  Nếu đối tượng chính là một sequence object có thể thay đổi (chẳng hạn như list), chỉ mục con phải cho kết quả là một số nguyên. Nếu số đó là số âm, độ dài của sequence được cộng vào nó. Giá trị thu được phải là một số nguyên không âm, nhỏ hơn độ dài của sequence, và sequence được yêu cầu gán object được gán vào phần tử có chỉ mục đó. Nếu chỉ mục nằm ngoài phạm vi, :exc:`IndexError` sẽ được phát sinh (phép gán cho sequence được lập chỉ mục không thể thêm phần tử mới vào list).

  .. index::
     pair: object; mapping
     pair: object; dictionary

  Nếu đối tượng chính là một mapping object (chẳng hạn như dictionary), chỉ mục con phải có kiểu tương thích với kiểu khóa của mapping, sau đó mapping được yêu cầu tạo một cặp khóa/giá trị ánh xạ chỉ mục con tới object được gán. Thao tác này có thể thay thế một cặp khóa/giá trị hiện có với cùng giá trị khóa, hoặc chèn một cặp khóa/giá trị mới (nếu chưa tồn tại khóa có cùng giá trị).

  .. index:: pair: slicing; assignment

  Nếu đích là một slicing: Biểu thức chính phải đánh giá thành một sequence object có thể thay đổi (chẳng hạn như list). Object được gán phải là :term:`iterable`. Cận dưới và cận trên của slicing phải là các số nguyên; nếu chúng là ``None`` (hoặc không hiện diện), giá trị mặc định lần lượt là 0 và độ dài của sequence. Nếu một trong hai cận là số âm, độ dài của sequence được cộng vào cận đó. Các cận thu được được giới hạn để nằm trong khoảng từ 0 đến độ dài của sequence, bao gồm cả hai đầu mút. Cuối cùng, sequence object được yêu cầu thay thế slice bằng các phần tử của sequence được gán. Độ dài của slice có thể khác với độ dài của sequence được gán, do đó làm thay đổi độ dài của target sequence, nếu target sequence cho phép điều đó.

Mặc dù định nghĩa phép gán ngụ ý rằng các phần chồng lấp giữa vế trái và vế phải là “đồng thời” (chẳng hạn ``a, b = b, a`` hoán đổi hai biến), các phần chồng lấp *trong* tập hợp các biến được gán diễn ra từ trái sang phải, đôi khi gây nhầm lẫn. Ví dụ, chương trình sau in ra ``[0, 2]``::

   x = [0, 1]
   i = 0
   i, x[i] = 1, 2         # i được cập nhật, sau đó x[i] được cập nhật
   print(x)


.. seealso::

   :pep:`3132` - Giải nén Iterable mở rộng
      Đặc tả cho tính năng ``*target``.


.. _augassign:

Các câu lệnh gán tăng cường
---------------------------

.. index::
   pair: augmented; assignment
   single: statement; assignment, augmented
   single: +=; augmented assignment
   single: -=; augmented assignment
   single: *=; augmented assignment
   single: /=; augmented assignment
   single: %=; augmented assignment
   single: &=; augmented assignment
   single: ^=; augmented assignment
   single: |=; augmented assignment
   single: **=; augmented assignment
   single: //=; augmented assignment
   single: >>=; augmented assignment
   single: <<=; augmented assignment

Phép gán tăng cường là sự kết hợp, trong một câu lệnh duy nhất, của một phép toán nhị phân và một câu lệnh gán:

.. productionlist:: python-grammar
   augmented_assignment_stmt: `augtarget` `augop` (`expression_list` | `yield_expression`)
   augtarget: `identifier` | `attributeref` | `subscription`
   augop: "+=" | "-=" | "*=" | "@=" | "/=" | "//=" | "%=" | "**="
        : | ">>=" | "<<=" | "&=" | "^=" | "|="

(Xem phần :ref:`primaries` để biết định nghĩa cú pháp của ba ký hiệu cuối.)

Phép gán tăng cường đánh giá đích (không giống các câu lệnh gán thông thường, đích không thể là một phép giải nén) và danh sách biểu thức, thực hiện phép toán nhị phân tương ứng với kiểu phép gán trên hai toán hạng, rồi gán kết quả cho đích ban đầu. Đích chỉ được đánh giá một lần.

Một câu lệnh gán tăng cường như ``x += 1`` có thể được viết lại thành ``x = x + 1`` để đạt được hiệu ứng tương tự, nhưng không hoàn toàn giống nhau. Trong phiên bản tăng cường, ``x`` chỉ được đánh giá một lần. Ngoài ra, khi có thể, phép toán thực tế được thực hiện *in-place*, nghĩa là thay vì tạo một đối tượng mới và gán đối tượng đó cho đích, đối tượng cũ được sửa đổi.

Không giống các phép gán thông thường, phép gán tăng cường đánh giá vế trái *before* vế phải. Ví dụ, ``a[i] += f(x)`` trước tiên tra cứu ``a[i]``, sau đó đánh giá ``f(x)`` và thực hiện phép cộng, cuối cùng ghi kết quả trở lại ``a[i]``.

Ngoại trừ việc gán cho tuple và nhiều đích trong một câu lệnh duy nhất, phép gán do các câu lệnh gán tăng cường thực hiện được xử lý giống như phép gán thông thường. Tương tự, ngoại trừ hành vi *in-place* có thể xảy ra, phép toán nhị phân do phép gán tăng cường thực hiện cũng giống như các phép toán nhị phân thông thường.

Đối với các đích là tham chiếu thuộc tính, :ref:`lưu ý tương tự về thuộc tính lớp và thuộc tính thể hiện <attr-target-note>` cũng được áp dụng như đối với các phép gán thông thường.


.. _annassign:

Các câu lệnh gán có chú thích kiểu
----------------------------------

.. index::
   pair: annotated; assignment
   single: statement; assignment, annotated
   single: : (colon); annotated variable

Phép gán :term:`chú thích kiểu <variable annotation>` là sự kết hợp, trong một câu lệnh duy nhất, của chú thích kiểu cho biến hoặc thuộc tính và một câu lệnh gán tùy chọn:

.. productionlist:: python-grammar
   annotated_assignment_stmt: `augtarget` ":" `expression`
                            : ["=" (`starred_expression` | `yield_expression`)]

Điểm khác biệt so với :ref:`assignment` thông thường là chỉ cho phép một đích duy nhất.

Đích gán được xem là "đơn giản" nếu nó chỉ gồm một tên không được đặt trong dấu ngoặc đơn. Đối với các đích gán đơn giản, nếu ở phạm vi lớp hoặc mô-đun, các chú thích kiểu sẽ được tập hợp trong một
:ref:`phạm vi chú thích <annotation-scopes>` được đánh giá một cách trì hoãn. Có thể đánh giá các chú thích kiểu bằng thuộc tính :attr:`~object.__annotations__` của một lớp hoặc mô-đun, hoặc bằng các tiện ích trong mô-đun :mod:`annotationlib`.

Nếu đích gán không đơn giản (một thuộc tính, nút chỉ mục hoặc tên được đặt trong dấu ngoặc đơn), chú thích kiểu sẽ không bao giờ được đánh giá.

Nếu một tên được chú thích trong phạm vi hàm, thì tên đó là cục bộ đối với phạm vi đó. Các chú thích không bao giờ được đánh giá và lưu trữ trong phạm vi hàm.

Nếu vế bên phải hiện diện, phép gán có chú thích thực hiện việc gán thực tế như thể không có chú thích. Nếu vế bên phải không hiện diện đối với một đích biểu thức, thì trình thông dịch đánh giá đích đó, ngoại trừ phần cuối
lời gọi :meth:`~object.__setitem__` hoặc :meth:`~object.__setattr__` cuối cùng.

.. seealso::

   :pep:`526` - Cú pháp cho chú thích biến
      Đề xuất bổ sung cú pháp để chú thích kiểu của các biến (bao gồm biến lớp và biến thực thể), thay vì biểu diễn chúng thông qua các chú thích.

   :pep:`484` - Gợi ý kiểu
      Đề xuất bổ sung mô-đun :mod:`typing` để cung cấp cú pháp chuẩn cho chú thích kiểu, có thể được sử dụng trong các công cụ phân tích tĩnh và IDE.

.. versionchanged:: 3.8
   Giờ đây, phép gán có chú thích cho phép sử dụng cùng các biểu thức ở vế phải như phép gán thông thường. Trước đây, một số biểu thức (chẳng hạn như biểu thức tuple không có dấu ngoặc) gây ra lỗi cú pháp.

.. versionchanged:: 3.14
   Các chú thích giờ đây được đánh giá một cách lười biếng trong một :ref:`phạm vi chú thích <annotation-scopes>` riêng. Nếu đích gán không đơn giản, các chú thích sẽ không bao giờ được đánh giá.


.. _assert:

Câu lệnh :keyword:`!assert`
===========================

.. index::
   ! pair: statement; assert
   pair: debugging; assertions
   single: , (comma); expression list

Câu lệnh assert là một cách thuận tiện để chèn các phép kiểm tra gỡ lỗi vào chương trình:

.. productionlist:: python-grammar
   assert_stmt: "assert" `expression` ["," `expression`]

Dạng đơn giản, ``assert expression``, tương đương với::

   if __debug__:
       if not expression: raise AssertionError

Dạng mở rộng, ``assert expression1, expression2``, tương đương với::

   if __debug__:
       if not expression1: raise AssertionError(expression2)

.. index::
   single: __debug__
   pair: exception; AssertionError

Các tương đương này giả định rằng :const:`__debug__` và :exc:`AssertionError` tham chiếu đến các biến tích hợp có những tên đó. Trong triển khai hiện tại, biến tích hợp ``__debug__`` là ``True`` trong những trường hợp bình thường và là ``False`` khi yêu cầu tối ưu hóa (tùy chọn dòng lệnh :option:`-O`). Trình tạo mã hiện tại không phát sinh mã cho câu lệnh :keyword:`assert` khi yêu cầu tối ưu hóa tại thời điểm biên dịch. Lưu ý rằng không cần đưa mã nguồn của biểu thức gây lỗi vào thông báo lỗi; biểu thức đó sẽ được hiển thị như một phần của stack trace.

Việc gán cho :const:`__debug__` là không hợp lệ. Giá trị của biến tích hợp sẵn này được xác định khi trình thông dịch khởi động.


.. _pass:

Câu lệnh :keyword:`!pass`
=========================

.. index::
   pair: statement; pass
   pair: null; operation
           pair: null; operation

.. productionlist:: python-grammar
   pass_stmt: "pass"

:keyword:`pass` là một thao tác rỗng --- khi được thực thi, không có gì xảy ra. Nó hữu ích như một phần giữ chỗ khi cú pháp yêu cầu một câu lệnh nhưng không cần thực thi mã nào, chẳng hạn như::

   def f(arg): pass    # một hàm hiện chưa thực hiện thao tác nào

   class C: pass       # một lớp hiện chưa có phương thức nào


.. _del:

Câu lệnh :keyword:`!del`
========================

.. index::
   ! pair: statement; del
   pair: deletion; target
   triple: deletion; target; list

.. productionlist:: python-grammar
   del_stmt: "del" `target_list`

Việc xóa được định nghĩa đệ quy rất giống với cách định nghĩa việc gán. Thay vì trình bày đầy đủ mọi chi tiết, dưới đây là một số gợi ý.

Việc xóa một danh sách đích sẽ đệ quy xóa từng đích, từ trái sang phải.

.. index::
   pair: statement; global
   pair: unbinding; name

Việc xóa một tên sẽ loại bỏ liên kết của tên đó khỏi namespace cục bộ hoặc toàn cục, tùy thuộc vào việc tên đó có xuất hiện trong câu lệnh :keyword:`global` trong cùng một khối mã hay không. Việc cố xóa một tên chưa được liên kết sẽ phát sinh một
ngoại lệ :exc:`NameError`.

.. index:: pair: attribute; deletion

Việc xóa các tham chiếu thuộc tính và phép đăng ký được chuyển cho đối tượng chính liên quan; nhìn chung, việc xóa một phép cắt tương đương với việc gán một lát cắt rỗng thuộc kiểu thích hợp (nhưng ngay cả điều này cũng do đối tượng được cắt quyết định).

.. versionchanged:: 3.2
   Trước đây, việc xóa một tên khỏi namespace cục bộ là không hợp lệ nếu tên đó xuất hiện dưới dạng biến tự do trong một khối lồng nhau.


.. _return:

Câu lệnh :keyword:`!return`
===========================

.. index::
   ! pair: statement; return
   pair: function; definition
   pair: class; definition

.. productionlist:: python-grammar
   return_stmt: "return" [`expression_list`]

:keyword:`return` chỉ có thể xuất hiện về mặt cú pháp bên trong định nghĩa hàm, không nằm trong định nghĩa lớp lồng nhau.

Nếu có danh sách biểu thức, danh sách đó được đánh giá; nếu không, ``None`` được thay thế.

:keyword:`return` thoát khỏi lệnh gọi hàm hiện tại với danh sách biểu thức (hoặc ``None``) làm giá trị trả về.

.. index:: pair: keyword; finally

Khi :keyword:`return` chuyển quyền điều khiển ra khỏi một câu lệnh :keyword:`try` có một
mệnh đề :keyword:`finally`, mệnh đề :keyword:`!finally` đó sẽ được thực thi trước khi thực sự thoát khỏi hàm.

Trong một hàm generator, câu lệnh :keyword:`return` cho biết generator đã hoàn tất và sẽ khiến :exc:`StopIteration` được phát sinh. Giá trị được trả về (nếu có) được dùng làm đối số để khởi tạo :exc:`StopIteration` và trở thành thuộc tính :attr:`StopIteration.value`.

Trong một hàm generator bất đồng bộ, câu lệnh :keyword:`return` rỗng cho biết generator bất đồng bộ đã hoàn tất và sẽ khiến
:exc:`StopAsyncIteration` được phát sinh. Câu lệnh :keyword:`!return` không rỗng là lỗi cú pháp trong một hàm generator bất đồng bộ.

.. _yield:

Câu lệnh :keyword:`!yield`
==========================

.. index::
   pair: statement; yield
   single: generator; function
   single: generator; iterator
   single: function; generator
   pair: exception; StopIteration

.. productionlist:: python-grammar
   yield_stmt: `yield_expression`

Một câu lệnh :keyword:`yield` tương đương về ngữ nghĩa với một :ref:`biểu thức yield <yieldexpr>`. Câu lệnh ``yield`` có thể được dùng để bỏ qua cặp dấu ngoặc vốn cần có trong câu lệnh biểu thức yield tương đương. Ví dụ, các câu lệnh yield::

  yield <expr>
  yield from <expr>

tương đương với các câu lệnh biểu thức yield::

  (yield <expr>)
  (yield from <expr>)

Các biểu thức và câu lệnh Yield chỉ được sử dụng khi định nghĩa một hàm :term:`generator`, và chỉ được sử dụng trong phần thân của hàm generator. Việc sử dụng :keyword:`yield` trong định nghĩa hàm là đủ để khiến định nghĩa đó tạo ra một hàm generator thay vì một hàm thông thường.

Để biết đầy đủ chi tiết về ngữ nghĩa của :keyword:`yield`, hãy tham khảo
phần :ref:`yieldexpr`.

.. _raise:

Câu lệnh :keyword:`!raise`
==========================

.. index::
   ! pair: statement; raise
   single: exception
   pair: raising; exception
   single: __traceback__ (exception attribute)

.. productionlist:: python-grammar
   raise_stmt: "raise" [`expression` ["from" `expression`]]

Nếu không có biểu thức nào, :keyword:`raise` sẽ raise lại exception hiện đang được xử lý, còn được gọi là *exception đang hoạt động*. Nếu hiện không có exception nào đang hoạt động, một exception :exc:`RuntimeError` sẽ được raise để cho biết đây là lỗi.

Nếu không, :keyword:`raise` đánh giá biểu thức đầu tiên thành đối tượng exception. Đối tượng này phải là một subclass hoặc instance của :class:`BaseException`. Nếu đó là một class, instance của exception sẽ được tạo khi cần bằng cách khởi tạo class mà không có đối số.

:dfn:`Kiểu` của exception là class của instance exception, còn
:dfn:`giá trị` là chính instance đó.

.. index:: pair: object; traceback

Đối tượng traceback thường được tự động tạo khi một exception được raise và được gắn vào exception dưới dạng thuộc tính :attr:`~BaseException.__traceback__`. Bạn có thể tạo một exception và thiết lập traceback riêng trong cùng một bước bằng cách sử dụng
:meth:`~BaseException.with_traceback` method của exception (trả về chính instance exception đó, với traceback được đặt thành đối số của method), như sau::

   raise Exception("foo occurred").with_traceback(tracebackobj)

.. index:: pair: exception; chaining
           __cause__ (exception attribute)
           __context__ (exception attribute)

Mệnh đề ``from`` được dùng cho việc chain exception: nếu được cung cấp, *biểu thức* thứ hai phải là một class hoặc instance exception khác. Nếu biểu thức thứ hai là một instance exception, nó sẽ được gắn vào exception được raise dưới dạng thuộc tính :attr:`~BaseException.__cause__` (thuộc tính này có thể ghi được). Nếu biểu thức là một class exception, class đó sẽ được khởi tạo và instance exception thu được sẽ được gắn vào exception được raise dưới dạng
thuộc tính :attr:`!__cause__`. Nếu ngoại lệ được phát sinh không được xử lý, cả hai ngoại lệ sẽ được in ra:

.. code-block:: pycon

   >>> try:
   ...     print(1 / 0)
   ... except Exception as exc:
   ...     raise RuntimeError("Something bad happened") from exc
   ...
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       print(1 / 0)
             ~~^~~
   ZeroDivisionError: division by zero

   The above exception was the direct cause of the following exception:

   Traceback (most recent call last):
     File "<stdin>", line 4, in <module>
       raise RuntimeError("Something bad happened") from exc
   RuntimeError: Something bad happened

Cơ chế tương tự cũng hoạt động ngầm nếu một ngoại lệ mới được phát sinh khi một ngoại lệ khác đang được xử lý. Một ngoại lệ có thể được xử lý khi sử dụng mệnh đề :keyword:`except` hoặc :keyword:`finally`, hoặc một
câu lệnh :keyword:`with`. Khi đó, ngoại lệ trước đó được gắn vào thuộc tính :attr:`~BaseException.__context__` của ngoại lệ mới:

.. code-block:: pycon

   >>> try:
   ...     print(1 / 0)
   ... except:
   ...     raise RuntimeError("Something bad happened")
   ...
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       print(1 / 0)
             ~~^~~
   ZeroDivisionError: division by zero

   During handling of the above exception, another exception occurred:

   Traceback (most recent call last):
     File "<stdin>", line 4, in <module>
       raise RuntimeError("Something bad happened")
   RuntimeError: Something bad happened

Có thể ngăn chặn việc liên kết ngoại lệ một cách rõ ràng bằng cách chỉ định :const:`None` trong mệnh đề ``from``:

.. doctest::

   >>> try:
   ...     print(1 / 0)
   ... except:
   ...     raise RuntimeError("Something bad happened") from None
   ...
   Traceback (most recent call last):
     File "<stdin>", line 4, in <module>
   RuntimeError: Something bad happened

Bạn có thể tìm thấy thêm thông tin về các ngoại lệ trong phần :ref:`exceptions`, còn thông tin về cách xử lý ngoại lệ nằm trong phần :ref:`try`.

.. versionchanged:: 3.3
    :const:`None` is now permitted as ``Y`` in ``raise X from Y``.

    Đã thêm thuộc tính :attr:`~BaseException.__suppress_context__` để ngăn việc tự động hiển thị ngữ cảnh của ngoại lệ.

.. versionchanged:: 3.11
    Nếu traceback của ngoại lệ đang hoạt động được sửa đổi trong mệnh đề :keyword:`except`, thì câu lệnh ``raise`` tiếp theo sẽ phát sinh lại ngoại lệ với traceback đã sửa đổi. Trước đây, ngoại lệ được phát sinh lại với traceback mà nó có khi được bắt.

.. _break:

Câu lệnh :keyword:`!break`
==========================

.. index::
   ! pair: statement; break
   pair: statement; for
   pair: statement; while
   pair: loop; statement

.. productionlist:: python-grammar
   break_stmt: "break"

:keyword:`break` chỉ có thể xuất hiện về mặt cú pháp bên trong một :keyword:`for` hoặc
:keyword:`while` loop, nhưng không được lồng trong định nghĩa hàm hoặc lớp bên trong loop đó.

.. index:: pair: keyword; else
           pair: loop control; target

Nó kết thúc loop bao quanh gần nhất, bỏ qua mệnh đề :keyword:`!else` tùy chọn nếu loop có mệnh đề này.

Nếu một :keyword:`for` loop bị kết thúc bởi :keyword:`break`, đích điều khiển của loop vẫn giữ nguyên giá trị hiện tại.

.. index:: pair: keyword; finally

Khi :keyword:`break` chuyển quyền điều khiển ra khỏi một câu lệnh :keyword:`try` có
mệnh đề :keyword:`finally`, mệnh đề :keyword:`!finally` đó được thực thi trước khi thực sự rời khỏi loop.


.. _continue:

Câu lệnh :keyword:`!continue`
=============================

.. index::
   ! pair: statement; continue
   pair: statement; for
   pair: statement; while
   pair: loop; statement
   pair: keyword; finally

.. productionlist:: python-grammar
   continue_stmt: "continue"

:keyword:`continue` chỉ có thể xuất hiện về mặt cú pháp bên trong một :keyword:`for` hoặc
:keyword:`while` vòng lặp, nhưng không được lồng trong một định nghĩa hàm hoặc lớp bên trong vòng lặp đó. Nó tiếp tục với chu kỳ tiếp theo của vòng lặp bao quanh gần nhất.

Khi :keyword:`continue` chuyển quyền điều khiển ra khỏi một câu lệnh :keyword:`try` có
mệnh đề :keyword:`finally`, mệnh đề :keyword:`!finally` đó sẽ được thực thi trước khi thực sự bắt đầu chu kỳ vòng lặp tiếp theo.


.. _import:
.. _from:

Câu lệnh :keyword:`!import`
===========================

.. index::
   ! pair: statement; import
   single: module; importing
   pair: name; binding
   pair: keyword; from
   pair: keyword; as
   pair: exception; ImportError
   single: , (comma); import statement

.. productionlist:: python-grammar
   import_stmt: "import" `module` ["as" `identifier`] ("," `module` ["as" `identifier`])*
              : | "from" `relative_module` "import" `identifier` ["as" `identifier`]
              : ("," `identifier` ["as" `identifier`])*
              : | "from" `relative_module` "import" "(" `identifier` ["as" `identifier`]
              : ("," `identifier` ["as" `identifier`])* [","] ")"
              : | "from" `relative_module` "import" "*"
   module: (`identifier` ".")* `identifier`
   relative_module: "."* `module` | "."+

Câu lệnh import cơ bản (không có mệnh đề :keyword:`from`) được thực thi theo hai bước:

#. tìm một mô-đun, tải và khởi tạo mô-đun đó nếu cần
#. định nghĩa một hoặc nhiều tên trong namespace hiện tại cho phạm vi chứa câu lệnh :keyword:`import`, giống như một câu lệnh gán (bao gồm ngữ nghĩa của :keyword:`global` và :keyword:`nonlocal`).

Khi câu lệnh chứa nhiều mệnh đề (được phân tách bằng dấu phẩy), hai bước này được thực hiện riêng biệt cho từng mệnh đề, giống như khi các mệnh đề được tách thành các câu lệnh import riêng lẻ.

Thông tin chi tiết về bước đầu tiên, tìm và tải các mô-đun, được mô tả cụ thể hơn trong phần về :ref:`import system <importsystem>`, phần này cũng mô tả các loại package và mô-đun khác nhau có thể được import, cũng như tất cả các hook có thể dùng để tùy chỉnh import system. Lưu ý rằng lỗi ở bước này có thể cho biết mô-đun không thể được định vị, *hoặc* đã xảy ra lỗi trong khi khởi tạo mô-đun, bao gồm cả việc thực thi mã của mô-đun.

Nếu mô-đun được yêu cầu được truy xuất thành công, mô-đun đó sẽ được cung cấp trong namespace cục bộ theo một trong ba cách:

.. index:: single: as; import statement

* Nếu sau tên mô-đun là :keyword:`!as`, thì tên đứng sau :keyword:`!as` được liên kết trực tiếp với mô-đun đã import.
* Nếu không chỉ định tên nào khác và mô-đun đang được import là mô-đun cấp cao nhất, tên của mô-đun được liên kết trong namespace cục bộ dưới dạng tham chiếu đến mô-đun đã import
* Nếu module được import *không* phải là module cấp cao nhất, thì tên của package cấp cao nhất chứa module đó sẽ được liên kết trong namespace cục bộ như một tham chiếu đến package cấp cao nhất. Module được import phải được truy cập bằng tên đầy đủ của nó thay vì truy cập trực tiếp


.. index::
   pair: name; binding
   single: from; import statement

Dạng :keyword:`from` sử dụng một quy trình phức tạp hơn một chút:

#. tìm module được chỉ định trong mệnh đề :keyword:`from`, tải và khởi tạo module nếu cần;
#. với mỗi định danh được chỉ định trong các mệnh đề :keyword:`import`:

   #. kiểm tra xem module được import có thuộc tính mang tên đó hay không
   #. nếu không, thử import submodule có tên đó rồi kiểm tra lại module được import để tìm thuộc tính đó
   #. nếu không tìm thấy thuộc tính, :exc:`ImportError` sẽ được raise.
   #. nếu không, một tham chiếu đến giá trị đó được lưu trong namespace hiện tại, sử dụng tên trong mệnh đề :keyword:`!as` nếu có, nếu không thì sử dụng tên thuộc tính

Ví dụ::

   import foo                 # foo được import và liên kết trong phạm vi cục bộ
   import foo.bar.baz         # foo, foo.bar và foo.bar.baz được import, foo được liên kết trong phạm vi cục bộ
   import foo.bar.baz as fbb  # foo, foo.bar và foo.bar.baz được import, foo.bar.baz được liên kết với tên fbb
   from foo.bar import baz    # foo, foo.bar và foo.bar.baz được import, foo.bar.baz được liên kết với tên baz
   from foo import attr       # foo được import và foo.attr được liên kết với tên attr

.. index:: single: * (asterisk); import statement

Nếu danh sách các định danh được thay thế bằng dấu sao (``'*'``), tất cả các tên public được định nghĩa trong module sẽ được liên kết trong namespace cục bộ của phạm vi nơi câu lệnh :keyword:`import` xuất hiện.

.. index:: single: __all__ (optional module attribute)

.. attribute:: module.__all__
   :no-typesetting:

Các *tên public* được định nghĩa bởi một module được xác định bằng cách kiểm tra namespace của module để tìm một biến có tên ``__all__``; nếu được định nghĩa, biến này phải là một chuỗi các tên được module đó định nghĩa hoặc import. Các tên chứa ký tự không phải ASCII phải ở dạng `chuẩn hóa <normalization form_>`_ NFKC; xem :ref:`lexical-names-nonascii` để biết chi tiết. Tất cả các tên được nêu trong ``__all__`` đều được xem là public và bắt buộc phải tồn tại. Nếu ``__all__`` chưa được định nghĩa, tập hợp tên public sẽ bao gồm tất cả các tên được tìm thấy trong namespace của module mà không bắt đầu bằng ký tự gạch dưới (``'_'``). ``__all__`` nên chứa toàn bộ public API. Nó nhằm tránh vô tình export các mục không thuộc API (chẳng hạn như các library module được import và sử dụng bên trong module).

Dạng import wildcard --- ``from module import *`` --- chỉ được phép ở cấp module. Việc cố gắng sử dụng dạng này trong định nghĩa class hoặc function sẽ gây ra :exc:`SyntaxError`.

.. index::
    single: relative; import

Khi chỉ định module cần import, bạn không phải chỉ định tên tuyệt đối của module. Khi một module hoặc package nằm trong một package khác, bạn có thể thực hiện relative import trong cùng top package mà không cần nêu tên package. Bằng cách sử dụng các dấu chấm ở đầu trong module hoặc package được chỉ định sau :keyword:`from`, bạn có thể chỉ định cần đi lên bao nhiêu cấp trong hệ thống phân cấp package hiện tại mà không cần nêu tên cụ thể. Một dấu chấm ở đầu biểu thị package hiện tại, nơi module thực hiện import tồn tại. Hai dấu chấm nghĩa là đi lên một cấp package. Ba dấu chấm nghĩa là đi lên hai cấp, v.v. Vì vậy, nếu bạn thực thi ``from . import mod`` từ một module trong package ``pkg``, bạn sẽ import ``pkg.mod``. Nếu bạn thực thi ``from ..subpkg2 import mod`` từ bên trong ``pkg.subpkg1``, bạn sẽ import ``pkg.subpkg2.mod``. Đặc tả về relative import nằm trong phần :ref:`relativeimports`.

:func:`importlib.import_module` được cung cấp để hỗ trợ các ứng dụng xác định động các module cần tải.

.. audit-event:: import module,filename,sys.path,sys.meta_path,sys.path_hooks import

.. _normalization form: https://www.unicode.org/reports/tr15/#Norm_Forms

.. _future:

Các câu lệnh Future
-------------------

.. index::
   pair: future; statement
   single: __future__; future statement

Một :dfn:`câu lệnh future` là một chỉ thị cho compiler rằng một module cụ thể phải được biên dịch bằng cú pháp hoặc ngữ nghĩa sẽ có trong một bản phát hành Python tương lai được chỉ định, nơi tính năng đó trở thành tiêu chuẩn.

Câu lệnh future nhằm hỗ trợ quá trình chuyển đổi sang các phiên bản Python trong tương lai, vốn giới thiệu những thay đổi không tương thích với ngôn ngữ. Câu lệnh này cho phép sử dụng các tính năng mới theo từng module trước khi phát hành phiên bản mà trong đó tính năng trở thành tiêu chuẩn.

.. productionlist:: python-grammar
   future_stmt: "from" "__future__" "import" `feature` ["as" `identifier`]
              : ("," `feature` ["as" `identifier`])*
              : | "from" "__future__" "import" "(" `feature` ["as" `identifier`]
              : ("," `feature` ["as" `identifier`])* [","] ")"
   feature: `identifier`

Câu lệnh future phải xuất hiện gần đầu module. Các dòng duy nhất có thể xuất hiện trước câu lệnh future là:

* docstring của module (nếu có),
* comment,
* các dòng trống, và
* các câu lệnh future khác.

Tính năng duy nhất bắt buộc phải sử dụng câu lệnh future là ``annotations`` (xem :pep:`563`).

Tất cả các tính năng lịch sử được bật bởi câu lệnh future vẫn được Python 3 nhận diện. Danh sách này bao gồm ``absolute_import``, ``division``, ``generators``, ``generator_stop``, ``unicode_literals``, ``print_function``, ``nested_scopes`` và ``with_statement``. Tất cả đều dư thừa vì luôn được bật và chỉ được giữ lại để đảm bảo khả năng tương thích ngược.

Câu lệnh future được nhận diện và xử lý đặc biệt tại thời điểm biên dịch: Các thay đổi về ngữ nghĩa của những cấu trúc cốt lõi thường được triển khai bằng cách tạo ra mã khác. Thậm chí một tính năng mới có thể đưa vào cú pháp không tương thích mới (chẳng hạn như một từ dành riêng mới), trong trường hợp đó trình biên dịch có thể cần phân tích module theo cách khác. Những quyết định như vậy không thể trì hoãn cho đến thời gian chạy.

Đối với mỗi bản phát hành cụ thể, trình biên dịch biết những tên tính năng nào đã được định nghĩa và sẽ phát sinh lỗi tại thời điểm biên dịch nếu một câu lệnh future chứa tính năng mà nó không biết.

Ngữ nghĩa runtime trực tiếp giống như đối với bất kỳ câu lệnh import nào: có một module tiêu chuẩn :mod:`__future__`, được mô tả ở phần sau, và module này sẽ được import theo cách thông thường tại thời điểm câu lệnh future được thực thi.

Ngữ nghĩa runtime đáng chú ý phụ thuộc vào tính năng cụ thể được bật bởi câu lệnh future.

Lưu ý rằng câu lệnh này không có gì đặc biệt::

   import __future__ [as name]

Đó không phải là câu lệnh future; mà là một câu lệnh import thông thường, không có ngữ nghĩa đặc biệt hay hạn chế cú pháp nào.

Mã được biên dịch bởi các lệnh gọi đến các hàm tích hợp :func:`exec` và :func:`compile` xuất hiện trong một mô-đun :mod:`!M` có chứa câu lệnh future, theo mặc định sẽ sử dụng cú pháp hoặc ngữ nghĩa mới liên kết với câu lệnh future đó. Có thể kiểm soát điều này bằng các đối số tùy chọn của :func:`compile` --- xem tài liệu về hàm đó để biết chi tiết.

Một câu lệnh future được nhập tại dấu nhắc của trình thông dịch tương tác sẽ có hiệu lực trong phần còn lại của phiên trình thông dịch. Nếu trình thông dịch được khởi động với
tùy chọn :option:`-i`, được truyền tên một tập lệnh để thực thi và tập lệnh đó có chứa một câu lệnh future, câu lệnh này sẽ có hiệu lực trong phiên tương tác được khởi động sau khi tập lệnh được thực thi.

.. seealso::

   :pep:`236` - Quay lại __future__
      Đề xuất ban đầu cho cơ chế __future__.


.. _global:

Câu lệnh :keyword:`!global`
===========================

.. index::
   ! pair: statement; global
   triple: global; name; binding
   single: , (comma); identifier list

.. productionlist:: python-grammar
   global_stmt: "global" `identifier` ("," `identifier`)*

Câu lệnh :keyword:`global` khiến các mã định danh được liệt kê được diễn giải là biến toàn cục. Sẽ không thể gán cho một biến toàn cục nếu không
:keyword:`!global`, mặc dù các biến tự do có thể tham chiếu đến các biến toàn cục mà không cần được khai báo là global.

Câu lệnh :keyword:`!global` áp dụng cho toàn bộ scope hiện tại (module, thân hàm hoặc định nghĩa lớp). Một :exc:`SyntaxError` sẽ được raised nếu một biến được sử dụng hoặc gán trước khi được khai báo là global trong scope.

Ở cấp module, tất cả biến đều là biến toàn cục, vì vậy câu lệnh :keyword:`!global` không có tác dụng. Tuy nhiên, các biến vẫn không được sử dụng hoặc gán trước khi có khai báo :keyword:`!global` tương ứng. Yêu cầu này được nới lỏng trong dấu nhắc tương tác (:term:`REPL`).

.. index::
   pair: built-in function; exec
   pair: built-in function; eval
   pair: built-in function; compile

**Ghi chú cho lập trình viên:** :keyword:`global` là một chỉ thị dành cho parser. Nó chỉ áp dụng cho mã được phân tích cú pháp cùng lúc với câu lệnh :keyword:`!global`. Cụ thể, một câu lệnh :keyword:`!global` nằm trong chuỗi hoặc code object được cung cấp cho hàm dựng sẵn :func:`exec` không ảnh hưởng đến khối mã *chứa* lệnh gọi hàm, và mã nằm trong chuỗi đó không bị ảnh hưởng bởi các câu lệnh :keyword:`!global` trong mã chứa lệnh gọi hàm. Điều tương tự cũng áp dụng cho các hàm :func:`eval` và :func:`compile`.


.. _nonlocal:

Câu lệnh :keyword:`!nonlocal`
=============================

.. index:: pair: statement; nonlocal
   single: , (comma); identifier list

.. productionlist:: python-grammar
   nonlocal_stmt: "nonlocal" `identifier` ("," `identifier`)*

Khi định nghĩa một hàm hoặc lớp được lồng (nằm bên trong) các định nghĩa của những hàm khác, các scope nonlocal của nó là các scope cục bộ của những hàm bao quanh. Câu lệnh :keyword:`nonlocal` khiến các identifier được liệt kê tham chiếu đến những tên đã được liên kết trước đó trong các scope nonlocal. Câu lệnh này cho phép mã được đóng gói liên kết lại các identifier nonlocal đó. Nếu một tên được liên kết trong nhiều scope nonlocal, liên kết gần nhất sẽ được sử dụng. Nếu một tên không được liên kết trong bất kỳ scope nonlocal nào, hoặc nếu không có scope nonlocal, một :exc:`SyntaxError` sẽ được raised.

Câu lệnh :keyword:`nonlocal` áp dụng cho toàn bộ scope của một hàm hoặc thân lớp. Một :exc:`SyntaxError` sẽ được raised nếu một biến được sử dụng hoặc gán trước khi có khai báo nonlocal tương ứng trong scope.

.. seealso::

   :pep:`3104` - Truy cập các tên trong phạm vi bên ngoài
      Đặc tả cho câu lệnh :keyword:`nonlocal`.

**Ghi chú của lập trình viên:** :keyword:`nonlocal` là một chỉ thị dành cho trình phân tích cú pháp và chỉ áp dụng cho mã được phân tích cùng với nó. Xem ghi chú cho
câu lệnh :keyword:`global`.


.. _type:

Câu lệnh :keyword:`!type`
=========================

.. index:: pair: statement; type

.. productionlist:: python-grammar
   type_stmt: 'type' `identifier` [`type_params`] "=" `expression`

Câu lệnh :keyword:`!type` khai báo một bí danh kiểu, là một thể hiện của :class:`typing.TypeAliasType`.

Ví dụ, câu lệnh sau đây tạo một bí danh kiểu::

   type Point = tuple[float, float]

Mã này gần tương đương với::

   annotation-def VALUE_OF_Point():
       return tuple[float, float]
   Point = typing.TypeAliasType("Point", VALUE_OF_Point())

``annotation-def`` cho biết một :ref:`phạm vi chú thích <annotation-scopes>`, hoạt động hầu hết như một hàm, nhưng có một số khác biệt nhỏ.

Giá trị của bí danh kiểu được đánh giá trong phạm vi chú thích. Giá trị này không được đánh giá khi bí danh kiểu được tạo, mà chỉ khi được truy cập thông qua
:attr:`!__value__` thuộc tính (xem :ref:`lazy-evaluation`). Điều này cho phép bí danh kiểu tham chiếu đến những tên chưa được định nghĩa.

Có thể biến bí danh kiểu thành generic bằng cách thêm một :ref:`danh sách tham số kiểu <type-params>` sau tên. Xem :ref:`generic-type-aliases` để biết thêm thông tin.

:keyword:`!type` là một :ref:`từ khóa mềm <soft-keywords>`.

.. versionadded:: 3.12

.. seealso::

   :pep:`695` - Cú pháp tham số kiểu
      Đã giới thiệu câu lệnh và cú pháp :keyword:`!type` cho các lớp và hàm generic.
