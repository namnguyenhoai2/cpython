.. _tut-structures:

****************
Cấu trúc dữ liệu
****************

Chương này mô tả chi tiết hơn một số nội dung bạn đã học, đồng thời bổ sung thêm một số nội dung mới.

.. _tut-morelists:

Tìm hiểu thêm về List
=====================

Kiểu dữ liệu :ref:`list <typesseq-list>` có thêm một số phương thức. Sau đây là tất cả các phương thức của đối tượng list:

.. method:: list.append(value, /)
   :noindex:

   Thêm một mục vào cuối list. Tương tự như ``a[len(a):] = [x]``.


.. method:: list.extend(iterable, /)
   :noindex:

   Mở rộng list bằng cách thêm tất cả các mục từ iterable. Tương tự như ``a[len(a):] = iterable``.


.. method:: list.insert(index, value, /)
   :noindex:

   Chèn một mục vào vị trí đã cho. Đối số đầu tiên là chỉ mục của phần tử đứng trước vị trí cần chèn, vì vậy ``a.insert(0, x)`` sẽ chèn vào đầu list, còn ``a.insert(len(a), x)`` tương đương với ``a.append(x)``.


.. method:: list.remove(value, /)
   :noindex:

   Xóa phần tử đầu tiên trong danh sách có giá trị bằng *value*. Phương thức này sẽ phát sinh
   :exc:`ValueError` nếu không có phần tử nào như vậy.


.. method:: list.pop(index=-1, /)
   :noindex:

   Xóa phần tử tại vị trí đã cho trong danh sách và trả về phần tử đó. Nếu không chỉ định chỉ mục, ``a.pop()`` sẽ xóa và trả về phần tử cuối cùng trong danh sách. Phương thức này sẽ phát sinh :exc:`IndexError` nếu danh sách trống hoặc chỉ mục nằm ngoài phạm vi của danh sách.


.. method:: list.clear()
   :noindex:

   Xóa tất cả phần tử khỏi danh sách. Tương tự như ``del a[:]``.


.. method:: list.index(value[, start[, stop]])
   :noindex:

   Trả về chỉ mục bắt đầu từ 0 của lần xuất hiện đầu tiên của *value* trong danh sách. Phương thức này sẽ phát sinh :exc:`ValueError` nếu không có phần tử nào như vậy.

   Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt và dùng để giới hạn việc tìm kiếm vào một dãy con cụ thể của danh sách. Chỉ mục được trả về được tính tương đối so với phần đầu của toàn bộ dãy, thay vì đối số *start*.


.. method:: list.count(value, /)
   :noindex:

   Trả về số lần *value* xuất hiện trong danh sách.


.. method:: list.sort(*, key=None, reverse=False)
   :noindex:

   Sắp xếp các phần tử của danh sách ngay tại chỗ (các đối số có thể được dùng để tùy chỉnh việc sắp xếp, xem :func:`sorted` để biết giải thích về chúng).


.. method:: list.reverse()
   :noindex:

   Đảo ngược các phần tử của danh sách ngay tại chỗ.


.. method:: list.copy()
   :noindex:

   Trả về một bản sao nông của danh sách. Tương tự như ``a[:]``.


Một ví dụ sử dụng hầu hết các phương thức của danh sách::

    >>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
    >>> fruits.count('apple')
    2
    >>> fruits.count('tangerine')
    0
    >>> fruits.index('banana')
    3
    >>> fruits.index('banana', 4)  # Tìm quả chuối tiếp theo, bắt đầu từ vị trí 4
    6
    >>> fruits.reverse()
    >>> fruits
    ['banana', 'apple', 'kiwi', 'banana', 'pear', 'apple', 'orange']
    >>> fruits.append('grape')
    >>> fruits
    ['banana', 'apple', 'kiwi', 'banana', 'pear', 'apple', 'orange', 'grape']
    >>> fruits.sort()
    >>> fruits
    ['apple', 'apple', 'banana', 'banana', 'grape', 'kiwi', 'orange', 'pear']
    >>> fruits.pop()
    'pear'

Có thể bạn đã nhận thấy rằng các phương thức như ``insert``, ``remove`` hoặc ``sort`` chỉ sửa đổi danh sách không có giá trị trả về được in ra — chúng trả về giá trị mặc định ``None``. [#]_ Đây là một nguyên tắc thiết kế áp dụng cho tất cả các cấu trúc dữ liệu có thể thay đổi trong Python.

Một điều khác bạn có thể nhận thấy là không phải mọi dữ liệu đều có thể được sắp xếp hoặc so sánh. Chẳng hạn, ``[None, 'hello', 10]`` không sắp xếp được vì số nguyên không thể so sánh với chuỗi, còn ``None`` không thể được so sánh với các kiểu khác. Ngoài ra, có một số kiểu không có quan hệ thứ tự được định nghĩa. Ví dụ, ``3+4j < 5+7j`` không phải là phép so sánh hợp lệ.


.. _tut-lists-as-stacks:

Sử dụng List làm Stack
----------------------

.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>


Các phương thức của list giúp bạn dễ dàng sử dụng một list làm stack (ngăn xếp), trong đó phần tử được thêm vào sau cùng sẽ là phần tử được lấy ra đầu tiên ("last-in, first-out"). Để thêm một mục vào đầu stack, hãy sử dụng :meth:`~list.append`. Để lấy một mục ở đầu stack, hãy sử dụng :meth:`~list.pop` mà không chỉ định chỉ mục rõ ràng. Ví dụ::

   >>> stack = [3, 4, 5]
   >>> stack.append(6)
   >>> stack.append(7)
   >>> stack
   [3, 4, 5, 6, 7]
   >>> stack.pop()
   7
   >>> stack
   [3, 4, 5, 6]
   >>> stack.pop()
   6
   >>> stack.pop()
   5
   >>> stack
   [3, 4]


.. _tut-lists-as-queues:

Sử dụng List làm Queue
----------------------

.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>

Bạn cũng có thể sử dụng một list làm queue (hàng đợi), trong đó phần tử được thêm vào đầu tiên sẽ là phần tử được lấy ra đầu tiên ("first-in, first-out"); tuy nhiên, list không hiệu quả cho mục đích này. Mặc dù thao tác append và pop ở cuối list rất nhanh, việc insert hoặc pop ở đầu list lại chậm (vì tất cả các phần tử khác phải được dịch chuyển một vị trí). Xem
:ref:`time-complexity` để biết thêm thông tin.

Để triển khai một queue, hãy sử dụng :class:`collections.deque`, được thiết kế để thực hiện thao tác append và pop nhanh ở cả hai đầu. Ví dụ::

   >>> from collections import deque
   >>> queue = deque(["Eric", "John", "Michael"])
   >>> queue.append("Terry")           # Terry đến
   >>> queue.append("Graham")          # Graham đến
   >>> queue.popleft()                 # Người đến đầu tiên rời đi
   'Eric'
   >>> queue.popleft()                 # Người đến thứ hai rời đi
   'John'
   >>> queue                           # Hàng đợi còn lại theo thứ tự đến
   deque(['Michael', 'Terry', 'Graham'])


.. _tut-listcomps:

Phép suy diễn danh sách
-----------------------

Phép suy diễn danh sách cung cấp một cách ngắn gọn để tạo danh sách. Các ứng dụng phổ biến là tạo danh sách mới trong đó mỗi phần tử là kết quả của một số phép toán được áp dụng lên từng phần tử của một chuỗi hoặc iterable khác, hoặc tạo một chuỗi con gồm những phần tử thỏa mãn một điều kiện nhất định.

Ví dụ, giả sử chúng ta muốn tạo một danh sách các số bình phương, như sau::

   >>> squares = []
   >>> for x in range(10):
   ...     squares.append(x**2)
   ...
   >>> squares
   [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

Lưu ý rằng điều này tạo ra (hoặc ghi đè) một biến có tên ``x`` vẫn tồn tại sau khi vòng lặp hoàn tất. Chúng ta có thể tính danh sách các bình phương mà không gây ra bất kỳ side effect nào bằng cách sử dụng::

   squares = list(map(lambda x: x**2, range(10)))

hoặc tương đương là::

   squares = [x**2 for x in range(10)]

cách này ngắn gọn và dễ đọc hơn.

List comprehension bao gồm các dấu ngoặc vuông chứa một biểu thức, theo sau là mệnh đề :keyword:`!for`, rồi đến không hoặc nhiều mệnh đề :keyword:`!for` hoặc :keyword:`!if`. Kết quả sẽ là một danh sách mới thu được bằng cách đánh giá biểu thức trong ngữ cảnh của các mệnh đề :keyword:`!for` và :keyword:`!if` theo sau nó. Ví dụ, listcomp này kết hợp các phần tử của hai danh sách nếu chúng không bằng nhau::

   >>> [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
   [(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]

và tương đương với::

   >>> combs = []
   >>> for x in [1,2,3]:
   ...     for y in [3,1,4]:
   ...         if x != y:
   ...             combs.append((x, y))
   ...
   >>> combs
   [(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]

Hãy chú ý rằng thứ tự của các câu lệnh :keyword:`for` và :keyword:`if` là giống nhau trong cả hai đoạn mã này.

Nếu biểu thức là một tuple (ví dụ: ``(x, y)`` trong ví dụ trước), biểu thức đó phải được đặt trong dấu ngoặc đơn.::

   >>> vec = [-4, -2, 0, 2, 4]
   >>> # tạo một list mới với các giá trị được nhân đôi
   >>> [x*2 for x in vec]
   [-8, -4, 0, 4, 8]
   >>> # lọc list để loại bỏ các số âm
   >>> [x for x in vec if x >= 0]
   [0, 2, 4]
   >>> # áp dụng một hàm cho tất cả các phần tử
   >>> [abs(x) for x in vec]
   [4, 2, 0, 2, 4]
   >>> # gọi một method trên mỗi phần tử
   >>> freshfruit = ['  banana', '  loganberry ', 'passion fruit  ']
   >>> [weapon.strip() for weapon in freshfruit]
   ['banana', 'loganberry', 'passion fruit']
   >>> # tạo một list gồm các 2-tuple như (number, square)
   >>> [(x, x**2) for x in range(6)]
   [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]
   >>> # tuple phải được đặt trong dấu ngoặc đơn, nếu không sẽ phát sinh lỗi
   >>> [x, x**2 for x in range(6)]
     File "<stdin>", line 1
       [x, x**2 for x in range(6)]
        ^^^^^^^
   SyntaxError: did you forget parentheses around the comprehension target?
   >>> # làm phẳng một list bằng listcomp với hai 'for'
   >>> vec = [[1,2,3], [4,5,6], [7,8,9]]
   >>> [num for elem in vec for num in elem]
   [1, 2, 3, 4, 5, 6, 7, 8, 9]

Phép hiểu danh sách có thể chứa các biểu thức phức tạp và các hàm lồng nhau::

   >>> from math import pi
   >>> [str(round(pi, i)) for i in range(1, 6)]
   ['3.1', '3.14', '3.142', '3.1416', '3.14159']

Phép hiểu danh sách lồng nhau
-----------------------------

Biểu thức ban đầu trong một phép hiểu danh sách có thể là bất kỳ biểu thức tùy ý nào, bao gồm cả một phép hiểu danh sách khác.

Hãy xem xét ví dụ sau về một ma trận 3x4 được triển khai dưới dạng danh sách gồm 3 danh sách có độ dài 4::

   >>> matrix = [
   ...     [1, 2, 3, 4],
   ...     [5, 6, 7, 8],
   ...     [9, 10, 11, 12],
   ... ]

Phép hiểu danh sách sau đây sẽ chuyển vị các hàng và cột::

   >>> [[row[i] for row in matrix] for i in range(4)]
   [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

Như đã thấy trong phần trước, phép hiểu danh sách bên trong được đánh giá trong ngữ cảnh của :keyword:`for` đứng sau nó, vì vậy ví dụ này tương đương với::

   >>> transposed = []
   >>> for i in range(4):
   ...     transposed.append([row[i] for row in matrix])
   ...
   >>> transposed
   [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

đến lượt nó, điều này cũng giống như::

   >>> transposed = []
   >>> for i in range(4):
   ...     # 3 dòng sau triển khai listcomp lồng nhau
   ...     transposed_row = []
   ...     for row in matrix:
   ...         transposed_row.append(row[i])
   ...     transposed.append(transposed_row)
   ...
   >>> transposed
   [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

Trong thực tế, bạn nên ưu tiên các hàm dựng sẵn thay cho các câu lệnh điều khiển luồng phức tạp. Hàm :func:`zip` sẽ rất phù hợp với trường hợp sử dụng này::

   >>> list(zip(*matrix))
   [(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]

Xem :ref:`tut-unpacking-arguments` để biết chi tiết về dấu hoa thị trong dòng này.

.. _tut-del:

Câu lệnh :keyword:`!del`
========================

Có một cách để xóa một phần tử khỏi danh sách dựa trên chỉ mục của phần tử đó thay vì giá trị của nó: câu lệnh :keyword:`del`. Cách này khác với phương thức :meth:`~list.pop`, vốn trả về một giá trị. Câu lệnh :keyword:`!del` cũng có thể được dùng để xóa các lát cắt khỏi danh sách hoặc xóa toàn bộ danh sách (việc mà trước đó chúng ta đã thực hiện bằng cách gán một danh sách rỗng cho lát cắt). Ví dụ::

   >>> a = [-1, 1, 66.25, 333, 333, 1234.5]
   >>> del a[0]
   >>> a
   [1, 66.25, 333, 333, 1234.5]
   >>> del a[2:4]
   >>> a
   [1, 66.25, 1234.5]
   >>> del a[:]
   >>> a
   []

:keyword:`del` cũng có thể được dùng để xóa toàn bộ biến::

   >>> del a

Việc tham chiếu đến tên ``a`` từ đây về sau sẽ gây ra lỗi (ít nhất là cho đến khi một giá trị khác được gán cho nó). Sau này chúng ta sẽ tìm thấy những cách sử dụng khác của :keyword:`del`.


.. _tut-tuples:

Tuple và Sequence
=================

Chúng ta đã thấy rằng list và string có nhiều thuộc tính chung, chẳng hạn như các thao tác lập chỉ mục và cắt. Đây là hai ví dụ về kiểu dữ liệu *sequence* (xem
:ref:`typesseq`). Vì Python là một ngôn ngữ không ngừng phát triển, các kiểu dữ liệu sequence khác có thể được bổ sung. Ngoài ra còn có một kiểu dữ liệu sequence tiêu chuẩn khác: *tuple*.

Một tuple gồm một số giá trị được phân tách bằng dấu phẩy, chẳng hạn như::

   >>> t = 12345, 54321, 'hello!'
   >>> t[0]
   12345
   >>> t
   (12345, 54321, 'hello!')
   >>> # Tuple có thể được lồng nhau:
   >>> u = t, (1, 2, 3, 4, 5)
   >>> u
   ((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))
   >>> # Tuple là bất biến:
   >>> t[0] = 88888
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: 'tuple' object does not support item assignment
   >>> # nhưng chúng có thể chứa các đối tượng khả biến:
   >>> v = ([1, 2, 3], [3, 2, 1])
   >>> v
   ([1, 2, 3], [3, 2, 1])


Như bạn thấy, khi xuất ra, các tuple luôn được đặt trong dấu ngoặc đơn để các tuple lồng nhau được diễn giải chính xác; chúng có thể được nhập vào có hoặc không có dấu ngoặc đơn bao quanh, mặc dù trong nhiều trường hợp, dấu ngoặc vẫn cần thiết (nếu tuple là một phần của biểu thức lớn hơn). Tuy nhiên, không thể gán cho từng phần tử riêng lẻ của tuple, nhưng có thể tạo các tuple chứa các đối tượng có thể thay đổi (mutable), chẳng hạn như list.

Mặc dù tuple có vẻ tương tự list, chúng thường được dùng trong các tình huống và cho những mục đích khác nhau. Tuple là :term:`immutable`, và thường chứa một chuỗi phần tử không đồng nhất được truy cập thông qua unpacking (xem phần sau trong mục này) hoặc indexing (hoặc thậm chí bằng thuộc tính trong trường hợp của :func:`namedtuples <collections.namedtuple>`). List là :term:`mutable`, và các phần tử của chúng thường đồng nhất, được truy cập bằng cách lặp qua list.

Một vấn đề đặc biệt là việc tạo tuple chứa 0 hoặc 1 phần tử: cú pháp có thêm một số điểm đặc biệt để hỗ trợ các trường hợp này. Tuple rỗng được tạo bằng một cặp dấu ngoặc đơn rỗng; tuple có một phần tử được tạo bằng cách đặt dấu phẩy sau một giá trị (chỉ đặt một giá trị trong dấu ngoặc đơn là chưa đủ). Hơi xấu, nhưng hiệu quả. Ví dụ:::

   >>> empty = ()
   >>> singleton = 'hello',    # <-- lưu ý dấu phẩy ở cuối
   >>> len(empty)
   0
   >>> len(singleton)
   1
   >>> singleton
   ('hello',)

Câu lệnh ``t = 12345, 54321, 'hello!'`` là một ví dụ về *đóng gói tuple*: các giá trị ``12345``, ``54321`` và ``'hello!'`` được đóng gói cùng nhau trong một tuple. Thao tác ngược lại cũng có thể thực hiện được::

   >>> x, y, z = t

Điều này được gọi, khá đúng với tên gọi, là *giải nén chuỗi* và hoạt động với mọi sequence ở vế phải. Việc giải nén sequence yêu cầu có số lượng biến ở bên trái dấu bằng bằng số phần tử trong sequence. Lưu ý rằng phép gán nhiều biến thực chất chỉ là sự kết hợp giữa đóng gói tuple và giải nén sequence.


.. _tut-sets:

Tập hợp
=======

Python cũng bao gồm một kiểu dữ liệu cho :ref:`sets <types-set>`. Set là một tập hợp không có thứ tự và không chứa các phần tử trùng lặp. Các cách sử dụng cơ bản gồm kiểm tra phần tử và loại bỏ các mục trùng lặp. Đối tượng set cũng hỗ trợ các phép toán trong toán học như hợp, giao, hiệu và hiệu đối xứng.

Có thể sử dụng dấu ngoặc nhọn hoặc hàm :func:`set` để tạo set. Lưu ý: để tạo một set rỗng, bạn phải sử dụng ``set()``, không phải ``{}``; cách sau tạo một dictionary rỗng, một cấu trúc dữ liệu được thảo luận trong phần tiếp theo.

Vì set không có thứ tự, việc lặp qua chúng hoặc in chúng có thể cho ra các phần tử theo thứ tự khác với dự kiến.

Sau đây là một minh họa ngắn gọn::

   >>> basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
   >>> print(basket)                      # cho thấy các phần tử trùng lặp đã được loại bỏ
   {'orange', 'banana', 'pear', 'apple'}
   >>> 'orange' in basket                 # kiểm tra phần tử nhanh chóng
   True
   >>> 'crabgrass' in basket
   False

   >>> # Minh họa các phép toán trên set gồm các chữ cái duy nhất từ hai từ
   >>>
   >>> a = set('abracadabra')
   >>> b = set('alacazam')
   >>> a                                  # các chữ cái duy nhất trong a
   {'a', 'r', 'b', 'c', 'd'}
   >>> a - b                              # các chữ cái có trong a nhưng không có trong b
   {'r', 'd', 'b'}
   >>> a | b                              # các chữ cái có trong a hoặc b hoặc cả hai
   {'a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'}
   >>> a & b                              # các chữ cái có trong cả a và b
   {'a', 'c'}
   >>> a ^ b                              # các chữ cái có trong a hoặc b nhưng không có trong cả hai
   {'r', 'd', 'b', 'm', 'z', 'l'}

Tương tự như :ref:`list comprehensions <tut-listcomps>`, set comprehensions cũng được hỗ trợ::

   >>> a = {x for x in 'abracadabra' if x not in 'abc'}
   >>> a
   {'r', 'd'}


.. _tut-dictionaries:

Dictionaries
============

Một kiểu dữ liệu hữu ích khác được tích hợp sẵn trong Python là *từ điển* (xem
:ref:`typesmapping`). Trong một số ngôn ngữ khác, từ điển đôi khi được gọi là "bộ nhớ liên kết" hoặc "mảng liên kết". Không giống các sequence, vốn được lập chỉ mục bằng một dải số, từ điển được lập chỉ mục bằng *khóa*, có thể là bất kỳ kiểu bất biến nào; chuỗi và số luôn có thể làm khóa. Tuple có thể được dùng làm khóa nếu chúng chỉ chứa chuỗi, số hoặc tuple; nếu một tuple chứa bất kỳ đối tượng khả biến nào, dù trực tiếp hay gián tiếp, thì không thể dùng nó làm khóa. Bạn không thể dùng list làm khóa, vì list có thể được sửa đổi tại chỗ bằng phép gán chỉ mục, phép gán lát cắt hoặc các phương thức như :meth:`~list.append` và
:meth:`~list.extend`.

Tốt nhất là hãy hình dung một từ điển như một tập hợp các cặp *khóa: giá trị*, với yêu cầu các khóa phải là duy nhất (trong cùng một từ điển). Một cặp dấu ngoặc nhọn tạo ra một từ điển rỗng: ``{}``. Đặt một danh sách các cặp khóa:giá trị được phân tách bằng dấu phẩy בתוך cặp dấu ngoặc nhọn sẽ thêm các cặp khóa:giá trị ban đầu vào từ điển; đây cũng là cách từ điển được ghi khi xuất ra.

Các thao tác chính trên một từ điển là lưu một giá trị với một khóa nào đó và trích xuất giá trị tương ứng với khóa đó. Cũng có thể xóa một cặp khóa:giá trị bằng ``del``. Nếu bạn lưu bằng một khóa đã được sử dụng, giá trị cũ liên kết với khóa đó sẽ bị quên.

Việc trích xuất giá trị cho một khóa không tồn tại bằng cách lập chỉ mục (``d[key]``) sẽ phát sinh một
:exc:`KeyError`. Để tránh gặp lỗi này khi cố truy cập một khóa có thể không tồn tại, hãy sử dụng phương thức :meth:`~dict.get` thay thế; phương thức này trả về ``None`` (hoặc một giá trị mặc định được chỉ định) nếu khóa không có trong từ điển.

Thực hiện ``list(d)`` trên một từ điển sẽ trả về danh sách tất cả các khóa được sử dụng trong từ điển, theo thứ tự chèn (nếu muốn sắp xếp, chỉ cần sử dụng ``sorted(d)`` thay thế). Để kiểm tra xem một khóa cụ thể có nằm trong từ điển hay không, hãy sử dụng từ khóa :keyword:`in`.

Sau đây là một ví dụ nhỏ sử dụng dictionary::

   >>> tel = {'jack': 4098, 'sape': 4139}
   >>> tel['guido'] = 4127
   >>> tel
   {'jack': 4098, 'sape': 4139, 'guido': 4127}
   >>> tel['jack']
   4098
   >>> tel['irv']
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   KeyError: 'irv'
   >>> print(tel.get('irv'))
   None
   >>> del tel['sape']
   >>> tel['irv'] = 4127
   >>> tel
   {'jack': 4098, 'guido': 4127, 'irv': 4127}
   >>> list(tel)
   ['jack', 'guido', 'irv']
   >>> sorted(tel)
   ['guido', 'irv', 'jack']
   >>> 'guido' in tel
   True
   >>> 'jack' not in tel
   False

Constructor :func:`dict` tạo trực tiếp các dictionary từ các chuỗi gồm những cặp key-value::

   >>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
   {'sape': 4139, 'guido': 4127, 'jack': 4098}

Ngoài ra, có thể sử dụng dict comprehension để tạo dictionary từ các biểu thức key và value tùy ý::

   >>> {x: x**2 for x in (2, 4, 6)}
   {2: 4, 4: 16, 6: 36}

Khi các key là những chuỗi đơn giản, đôi khi việc chỉ định các cặp bằng keyword arguments sẽ dễ dàng hơn::

   >>> dict(sape=4139, guido=4127, jack=4098)
   {'sape': 4139, 'guido': 4127, 'jack': 4098}


.. _tut-loopidioms:

Kỹ thuật lặp
============

Khi lặp qua các dictionary, có thể truy xuất đồng thời key và value tương ứng bằng method :meth:`~dict.items`.::

   >>> knights = {'gallahad': 'the pure', 'robin': 'the brave'}
   >>> for k, v in knights.items():
   ...     print(k, v)
   ...
   gallahad the pure
   robin the brave

Khi lặp qua một sequence, có thể truy xuất đồng thời chỉ mục vị trí và value tương ứng bằng function :func:`enumerate`.::

   >>> for i, v in enumerate(['tic', 'tac', 'toe']):
   ...     print(i, v)
   ...
   0 tic
   1 tac
   2 toe

Để lặp qua hai hoặc nhiều sequence cùng lúc, có thể ghép các phần tử tương ứng bằng hàm :func:`zip`.::

   >>> questions = ['name', 'quest', 'favorite color']
   >>> answers = ['lancelot', 'the holy grail', 'blue']
   >>> for q, a in zip(questions, answers):
   ...     print('What is your {0}?  It is {1}.'.format(q, a))
   ...
   What is your name?  It is lancelot.
   What is your quest?  It is the holy grail.
   What is your favorite color?  It is blue.

Để lặp qua một sequence theo thứ tự ngược, trước tiên hãy chỉ định sequence theo hướng xuôi, sau đó gọi hàm :func:`reversed`.::

   >>> for i in reversed(range(1, 10, 2)):
   ...     print(i)
   ...
   9
   7
   5
   3
   1

Để lặp qua một sequence theo thứ tự đã sắp xếp, hãy sử dụng hàm :func:`sorted`, hàm này trả về một danh sách mới đã được sắp xếp mà không thay đổi dữ liệu nguồn.::

   >>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
   >>> for i in sorted(basket):
   ...     print(i)
   ...
   apple
   apple
   banana
   orange
   orange
   pear

Sử dụng :func:`set` trên một sequence sẽ loại bỏ các phần tử trùng lặp. Việc sử dụng
:func:`sorted` kết hợp với :func:`set` trên một sequence là cách phổ biến để lặp qua các phần tử duy nhất của sequence theo thứ tự đã sắp xếp.::

   >>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
   >>> for f in sorted(set(basket)):
   ...     print(f)
   ...
   apple
   banana
   orange
   pear

Đôi khi bạn có thể muốn thay đổi một danh sách trong khi đang lặp qua danh sách đó; tuy nhiên, việc tạo một danh sách mới thường đơn giản và an toàn hơn.::

   >>> import math
   >>> raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
   >>> filtered_data = []
   >>> for value in raw_data:
   ...     if not math.isnan(value):
   ...         filtered_data.append(value)
   ...
   >>> filtered_data
   [56.2, 51.7, 55.3, 52.5, 47.8]


.. _tut-conditions:

Thông tin thêm về điều kiện
===========================

Các điều kiện được sử dụng trong các câu lệnh ``while`` và ``if`` có thể chứa bất kỳ toán tử nào, không chỉ các phép so sánh.


Các toán tử so sánh ``in`` và ``not in`` là các phép kiểm tra membership, xác định xem một giá trị có nằm trong (hoặc không nằm trong) một container hay không. Các toán tử ``is`` và ``is not`` so sánh xem hai đối tượng có thực sự là cùng một đối tượng hay không. Tất cả các toán tử so sánh có cùng độ ưu tiên, thấp hơn độ ưu tiên của tất cả các toán tử số học.

Các phép so sánh có thể được nối chuỗi. Ví dụ: ``a < b == c`` kiểm tra xem ``a`` có nhỏ hơn ``b`` hay không, đồng thời ``b`` có bằng ``c`` hay không.

Các phép so sánh có thể được kết hợp bằng các toán tử Boolean ``and`` và ``or``, đồng thời kết quả của một phép so sánh (hoặc của bất kỳ biểu thức Boolean nào khác) có thể được phủ định bằng ``not``. Các toán tử này có độ ưu tiên thấp hơn các toán tử so sánh; giữa chúng, ``not`` có độ ưu tiên cao nhất và ``or`` thấp nhất, vì vậy ``A and not B or C`` tương đương với ``(A and (not B)) or C``. Như mọi khi, có thể sử dụng dấu ngoặc để thể hiện cấu trúc kết hợp mong muốn.

Các toán tử Boolean ``and`` và ``or`` được gọi là các toán tử *short-circuit*: các đối số của chúng được đánh giá từ trái sang phải và quá trình đánh giá dừng ngay khi kết quả được xác định. Ví dụ, nếu ``A`` và ``C`` là đúng nhưng ``B`` là sai, ``A and B and C`` sẽ không đánh giá biểu thức ``C``. Khi được sử dụng như một giá trị tổng quát thay vì như một giá trị Boolean, giá trị trả về của một toán tử short-circuit là đối số được đánh giá cuối cùng.

Bạn có thể gán kết quả của một phép so sánh hoặc biểu thức Boolean khác cho một biến. Ví dụ:::

   >>> string1, string2, string3 = '', 'Trondheim', 'Hammer Dance'
   >>> non_null = string1 or string2 or string3
   >>> non_null
   'Trondheim'

Lưu ý rằng trong Python, không giống như C, phép gán bên trong các biểu thức phải được thực hiện một cách tường minh bằng
:ref:`walrus operator <why-can-t-i-use-an-assignment-in-an-expression>` ``:=``. Điều này tránh được một nhóm vấn đề phổ biến trong các chương trình C: gõ ``=`` trong một biểu thức khi thực ra ``==`` mới là điều được dự định.


.. _tut-comparing:

So sánh các sequence và các kiểu khác
=====================================
Các đối tượng sequence thường có thể được so sánh với các đối tượng khác cùng kiểu sequence. Việc so sánh sử dụng thứ tự *lexicographical*: trước tiên, hai phần tử đầu tiên được so sánh; nếu chúng khác nhau, điều này quyết định kết quả so sánh; nếu chúng bằng nhau, hai phần tử tiếp theo được so sánh, và cứ tiếp tục như vậy cho đến khi một trong hai sequence cạn phần tử. Nếu hai phần tử được so sánh bản thân chúng là các sequence cùng kiểu, phép so sánh lexicographical được thực hiện đệ quy. Nếu mọi phần tử của hai sequence đều được xem là bằng nhau, hai sequence được coi là bằng nhau. Nếu một sequence là subsequence ban đầu của sequence kia, sequence ngắn hơn là sequence nhỏ hơn. Thứ tự lexicographical đối với chuỗi sử dụng số code point Unicode để sắp xếp từng ký tự. Sau đây là một số ví dụ về việc so sánh các sequence cùng kiểu::

   (1, 2, 3)              < (1, 2, 4)
   [1, 2, 3]              < [1, 2, 4]
   'ABC' < 'C' < 'Pascal' < 'Python'
   (1, 2, 3, 4)           < (1, 2, 4)
   (1, 2)                 < (1, 2, -1)
   (1, 2, 3)             == (1.0, 2.0, 3.0)
   (1, 2, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4)

Lưu ý rằng việc so sánh các đối tượng thuộc các kiểu khác nhau bằng ``<`` hoặc ``>`` là hợp lệ, miễn là các đối tượng có các phương thức so sánh phù hợp. Ví dụ, các kiểu số hỗn hợp được so sánh theo giá trị số của chúng, vì vậy 0 bằng 0.0, v.v. Nếu không, thay vì cung cấp một thứ tự tùy ý, interpreter sẽ raise một ngoại lệ :exc:`TypeError`.


.. rubric:: Chú thích cuối trang

.. [#] Các ngôn ngữ khác có thể trả về đối tượng đã được biến đổi, cho phép method chaining, chẳng hạn như ``d->insert("a")->remove("b")->sort();``.
