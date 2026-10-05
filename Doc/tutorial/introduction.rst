.. _tut-informal:

*************************************
Giới thiệu không chính thức về Python
*************************************

Trong các ví dụ sau, phần nhập và phần xuất được phân biệt bằng việc có hoặc không có dấu nhắc (:term:`>>>` và :term:`...`): để lặp lại ví dụ, bạn phải nhập mọi thứ sau dấu nhắc khi dấu nhắc xuất hiện; các dòng không bắt đầu bằng dấu nhắc là phần xuất từ trình thông dịch. Lưu ý rằng dấu nhắc phụ đứng một mình trên một dòng trong ví dụ có nghĩa là bạn phải nhập một dòng trống; cách này được dùng để kết thúc một lệnh nhiều dòng.

.. only:: html

   Bạn có thể dùng nút "Copy" (nút này xuất hiện ở góc trên bên phải khi di chuột qua hoặc chạm vào một ví dụ mã), nút này sẽ loại bỏ các dấu nhắc và bỏ qua phần xuất, để sao chép và dán các dòng nhập vào trình thông dịch.

.. index:: single: # (hash); comment

Nhiều ví dụ trong tài liệu này, kể cả những ví dụ được nhập tại dấu nhắc tương tác, có chứa chú thích. Chú thích trong Python bắt đầu bằng ký tự dấu thăng, ``#``, và kéo dài đến hết dòng vật lý. Chú thích có thể xuất hiện ở đầu dòng hoặc sau khoảng trắng hay mã, nhưng không được nằm trong literal chuỗi. Ký tự dấu thăng bên trong literal chuỗi chỉ đơn giản là một ký tự dấu thăng. Vì chú thích dùng để làm rõ mã và không được Python diễn giải, bạn có thể bỏ qua chúng khi nhập các ví dụ.

Một số ví dụ::

   # đây là chú thích đầu tiên
   spam = 1  # và đây là chú thích thứ hai
             # ... và giờ là lần thứ ba!
   text = "# This is not a comment because it's inside quotes."


.. _tut-calculator:

Dùng Python làm máy tính
========================

Hãy thử một số lệnh Python đơn giản. Khởi động trình thông dịch và chờ dấu nhắc chính, ``>>>``. (Việc này sẽ không mất nhiều thời gian.)


.. _tut-numbers:

Các số
------

Trình thông dịch hoạt động như một máy tính đơn giản: bạn có thể nhập một biểu thức và nó sẽ hiển thị giá trị. Cú pháp biểu thức rất đơn giản: có thể dùng các toán tử ``+``, ``-``, ``*`` và ``/`` để thực hiện phép tính; có thể dùng dấu ngoặc đơn (``()``) để nhóm các phần tử. Ví dụ::

   >>> 2 + 2
   4
   >>> 50 - 5*6
   20
   >>> (50 - 5*6) / 4
   5.0
   >>> 8 / 5  # phép chia luôn trả về một số dấu phẩy động
   1.6

Các số nguyên (ví dụ: ``2``, ``4``, ``20``) có kiểu :class:`int`, còn các số có phần thập phân (ví dụ: ``5.0``, ``1.6``) có kiểu
:class:`float`. Chúng ta sẽ tìm hiểu thêm về các kiểu số sau trong hướng dẫn này.

Phép chia (``/``) luôn trả về một số thực. Để thực hiện :term:`floor division` và nhận được kết quả là số nguyên, bạn có thể sử dụng toán tử ``//``; để tính phần dư, bạn có thể sử dụng ``%``::

   >>> 17 / 3  # phép chia thông thường trả về một số thực
   5.666666666666667
   >>>
   >>> 17 // 3  # phép chia lấy phần nguyên loại bỏ phần thập phân
   5
   >>> 17 % 3  # toán tử % trả về phần dư của phép chia
   2
   >>> 5 * 3 + 2  # thương làm tròn xuống * số chia + phần dư
   17

Trong Python, bạn có thể sử dụng toán tử ``**`` để tính lũy thừa [#]_::

   >>> 5 ** 2  # 5 bình phương
   25
   >>> 2 ** 7  # 2 mũ 7
   128

Dấu bằng (``=``) được dùng để gán một giá trị cho một biến. Sau đó, không có kết quả nào được hiển thị trước dấu nhắc tương tác tiếp theo::

   >>> width = 20
   >>> height = 5 * 9
   >>> width * height
   900

Nếu một biến chưa được "defined" (gán một giá trị), việc cố gắng sử dụng biến đó sẽ gây ra lỗi::

   >>> n  # thử truy cập một biến chưa được định nghĩa
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'n' is not defined

Python hỗ trợ đầy đủ số dấu phẩy động; các toán tử với các toán hạng có kiểu hỗn hợp sẽ chuyển toán hạng số nguyên thành số dấu phẩy động::

   >>> 4 * 3.75 - 1
   14.0

Trong chế độ tương tác, biểu thức được in cuối cùng được gán cho biến ``_``. Điều này có nghĩa là khi sử dụng Python như một máy tính để bàn, bạn có thể tiếp tục các phép tính dễ dàng hơn, chẳng hạn như::

   >>> tax = 12.5 / 100
   >>> price = 100.50
   >>> price * tax
   12.5625
   >>> price + _
   113.0625
   >>> round(_, 2)
   113.06

Người dùng nên coi biến này là chỉ-đọc. Đừng gán giá trị cho biến này một cách rõ ràng --- nếu không, bạn sẽ tạo một biến cục bộ độc lập có cùng tên, che khuất biến dựng sẵn cùng hành vi đặc biệt của nó.

Ngoài :class:`int` và :class:`float`, Python còn hỗ trợ các kiểu số khác, chẳng hạn như :class:`~decimal.Decimal` và :class:`~fractions.Fraction`. Python cũng tích hợp sẵn hỗ trợ cho :ref:`số phức <typesnumeric>`, đồng thời sử dụng hậu tố ``j`` hoặc ``J`` để biểu thị phần ảo (ví dụ ``3+5j``).


.. _tut-strings:

Văn bản
-------

Python có thể thao tác với văn bản (được biểu diễn bằng kiểu :class:`str`, thường gọi là "chuỗi") cũng như các số. Điều này bao gồm các ký tự "``!``", từ "``rabbit``", tên "``Paris``", câu "``Got your back.``", v.v. "``Yay! :)``". Chúng có thể được đặt trong dấu nháy đơn (``'...'``) hoặc dấu nháy kép (``"..."``) với cùng một kết quả [#]_.

.. code-block:: pycon

   >>> 'spam eggs'  # dấu nháy đơn
   'spam eggs'
   >>> "Paris rabbit got your back :)! Yay!"  # dấu nháy kép
   'Paris rabbit got your back :)! Yay!'
   >>> '1975'  # các chữ số và số được đặt trong dấu nháy cũng là chuỗi
   '1975'

Để trích dẫn một câu trích dẫn, chúng ta cần "escape" nó bằng cách đặt ``\`` trước nó. Ngoài ra, chúng ta có thể sử dụng kiểu dấu ngoặc kép còn lại::

   >>> 'doesn\'t'  # sử dụng \' để escape dấu nháy đơn...
   "doesn't"
   >>> "doesn't"  # ...hoặc thay vào đó sử dụng dấu ngoặc kép
   "doesn't"
   >>> '"Yes," they said.'
   '"Yes," they said.'
   >>> "\"Yes,\" they said."
   '"Yes," they said.'
   >>> '"Isn\'t," they said.'
   '"Isn\'t," they said.'

Trong Python shell, phần định nghĩa chuỗi và chuỗi đầu ra có thể trông khác nhau. Hàm :func:`print` tạo ra đầu ra dễ đọc hơn bằng cách bỏ qua các dấu ngoặc kép bao quanh, đồng thời in các ký tự đã được escape và các ký tự đặc biệt::

   >>> s = 'First line.\nSecond line.'  # \n có nghĩa là ký tự xuống dòng
   >>> s  # không có print(), các ký tự đặc biệt được giữ nguyên trong chuỗi
   'First line.\nSecond line.'
   >>> print(s)  # với print(), các ký tự đặc biệt được diễn giải, vì vậy \n tạo ra dòng mới
   First line.
   Second line.

Nếu bạn không muốn các ký tự đứng trước ``\`` được diễn giải là ký tự đặc biệt, bạn có thể sử dụng *chuỗi raw* bằng cách thêm một ``r`` trước dấu ngoặc kép đầu tiên::

   >>> print('C:\this\name')  # ở đây \t có nghĩa là tab, \n có nghĩa là dòng mới
   C:      his
   ame
   >>> print(r'C:\this\name')  # hãy lưu ý chữ r trước dấu ngoặc kép
   C:\this\name

Có một điểm tinh tế đối với chuỗi raw: một chuỗi raw không được kết thúc bằng số lẻ ký tự ``\``; xem
:ref:`mục FAQ <faq-programming-raw-string-backslash>` để biết thêm thông tin và các cách khắc phục.

Chuỗi ký tự có thể kéo dài qua nhiều dòng. Một cách là sử dụng dấu ngoặc kép ba lần: ``"""..."""`` hoặc ``'''...'''``. Các ký tự cuối dòng được tự động đưa vào chuỗi, nhưng có thể ngăn điều này bằng cách thêm một ``\`` ở cuối dòng. Trong ví dụ sau, ký tự dòng mới ban đầu không được đưa vào::

   >>> print("""\
   ... Usage: thingy [OPTIONS]
   ...      -h                        Display this usage message
   ...      -H hostname               Hostname to connect to
   ... """)
   Usage: thingy [OPTIONS]
        -h                        Display this usage message
        -H hostname               Hostname to connect to

   >>>

Các chuỗi có thể được nối (ghép lại) bằng toán tử ``+``, và được lặp lại bằng ``*``::

   >>> # 3 lần 'un', tiếp theo là 'ium'
   >>> 3 * 'un' + 'ium'
   'unununium'

Hai hoặc nhiều *chuỗi ký tự* (tức là các chuỗi được đặt giữa dấu ngoặc kép) nằm cạnh nhau sẽ được tự động nối lại.::

   >>> 'Py' 'thon'
   'Python'

Tính năng này đặc biệt hữu ích khi bạn muốn ngắt các chuỗi dài::

   >>> text = ('Put several strings within parentheses '
   ...         'to have them joined together.')
   >>> text
   'Put several strings within parentheses to have them joined together.'

Tuy nhiên, cách này chỉ hoạt động với hai chuỗi ký tự, không áp dụng cho biến hoặc biểu thức::

   >>> prefix = 'Py'
   >>> prefix 'thon'  # không thể nối một biến với một chuỗi ký tự
     File "<stdin>", line 1
       prefix 'thon'
              ^^^^^^
   SyntaxError: invalid syntax
   >>> ('un' * 3) 'ium'
     File "<stdin>", line 1
       ('un' * 3) 'ium'
                  ^^^^^
   SyntaxError: invalid syntax

Nếu muốn nối các biến hoặc một biến với một chuỗi ký tự, hãy sử dụng ``+``::

   >>> prefix + 'thon'
   'Python'

Có thể *lập chỉ mục* (subscript) các chuỗi, trong đó ký tự đầu tiên có chỉ mục là 0. Không có kiểu ký tự riêng biệt; một ký tự đơn giản là một chuỗi có kích thước bằng một::

   >>> word = 'Python'
   >>> word[0]  # ký tự ở vị trí 0
   'P'
   >>> word[5]  # ký tự ở vị trí 5
   'n'

Chỉ mục cũng có thể là số âm để bắt đầu đếm từ bên phải::

   >>> word[-1]  # ký tự cuối cùng
   'n'
   >>> word[-2]  # ký tự áp chót
   'o'
   >>> word[-6]
   'P'

Lưu ý rằng vì -0 giống với 0 nên các chỉ mục âm bắt đầu từ -1.

Ngoài việc lập chỉ mục, *slicing* cũng được hỗ trợ.  Trong khi lập chỉ mục được dùng để lấy từng ký tự riêng lẻ, *slicing* cho phép bạn lấy một chuỗi con::

   >>> word[0:2]  # các ký tự từ vị trí 0 (bao gồm) đến vị trí 2 (không bao gồm)
   'Py'
   >>> word[2:5]  # các ký tự từ vị trí 2 (bao gồm) đến vị trí 5 (không bao gồm)
   'tho'

Các chỉ số lát cắt có các giá trị mặc định hữu ích; nếu bỏ qua chỉ số đầu tiên thì mặc định là số không, còn nếu bỏ qua chỉ số thứ hai thì mặc định là kích thước của chuỗi được lát cắt.::

   >>> word[:2]   # ký tự từ đầu đến vị trí 2 (không bao gồm)
   'Py'
   >>> word[4:]   # các ký tự từ vị trí 4 (bao gồm) đến cuối
   'on'
   >>> word[-2:]  # các ký tự từ vị trí áp chót (bao gồm) đến cuối
   'on'

Lưu ý rằng phần bắt đầu luôn được bao gồm, còn phần kết thúc luôn không được bao gồm. Điều này đảm bảo rằng ``s[:i] + s[i:]`` luôn bằng ``s``::

   >>> word[:2] + word[2:]
   'Python'
   >>> word[:4] + word[4:]
   'Python'

Một cách để ghi nhớ cách hoạt động của các slice là hình dung các chỉ mục trỏ *giữa* các ký tự, trong đó cạnh trái của ký tự đầu tiên được đánh số 0. Khi đó, cạnh phải của ký tự cuối cùng trong một chuỗi gồm *n* ký tự có chỉ mục là *n*, chẳng hạn::

    +---+---+---+---+---+---+
    | P | y | t | h | o | n |
    +---+---+---+---+---+---+
    0   1   2   3   4   5   6
   -6  -5  -4  -3  -2  -1

Hàng số đầu tiên cho biết vị trí của các chỉ mục 0...6 trong chuỗi; hàng thứ hai cho biết các chỉ mục âm tương ứng. Slice từ *i* đến *j* gồm tất cả các ký tự nằm giữa các cạnh lần lượt được gắn nhãn *i* và *j*.

Đối với các chỉ mục không âm, độ dài của một slice là hiệu của các chỉ mục nếu cả hai đều nằm trong giới hạn. Ví dụ: độ dài của ``word[1:3]`` là 2.

Việc cố sử dụng một chỉ mục quá lớn sẽ dẫn đến lỗi::

   >>> word[42]  # từ này chỉ có 6 ký tự
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   IndexError: string index out of range

Tuy nhiên, các chỉ mục slice nằm ngoài phạm vi sẽ được xử lý phù hợp khi dùng để tạo slice::

   >>> word[4:42]
   'on'
   >>> word[42:]
   ''

Các chuỗi Python không thể bị thay đổi --- chúng là :term:`immutable`. Vì vậy, việc gán vào một vị trí được lập chỉ mục trong chuỗi sẽ dẫn đến lỗi::

   >>> word[0] = 'J'
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: 'str' object does not support item assignment
   >>> word[2:] = 'py'
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: 'str' object does not support item assignment

Nếu cần một chuỗi khác, bạn nên tạo một chuỗi mới::

   >>> 'J' + word[1:]
   'Jython'
   >>> word[:2] + 'py'
   'Pypy'

Hàm tích hợp :func:`len` trả về độ dài của một chuỗi::

   >>> s = 'supercalifragilisticexpialidocious'
   >>> len(s)
   34


.. seealso::

   :ref:`textseq`
      Chuỗi là ví dụ về *các kiểu sequence*, và hỗ trợ các thao tác phổ biến được các kiểu này hỗ trợ.

   :ref:`string-methods`
      Chuỗi hỗ trợ rất nhiều phương thức để thực hiện các phép biến đổi và tìm kiếm cơ bản.

   :ref:`f-strings`
      Các string literal có chứa biểu thức nhúng.

   :ref:`formatstrings`
      Thông tin về việc định dạng chuỗi bằng :meth:`str.format`.

   :ref:`old-string-formatting`
      Các thao tác định dạng cũ được gọi khi chuỗi là toán hạng bên trái của toán tử ``%`` được mô tả chi tiết hơn tại đây.


.. _tut-lists:

Danh sách
---------

Python biết một số kiểu dữ liệu *phức hợp*, được dùng để nhóm các giá trị khác lại với nhau. Kiểu linh hoạt nhất là *danh sách*, có thể được viết dưới dạng một danh sách các giá trị (phần tử) được phân tách bằng dấu phẩy và đặt giữa các dấu ngoặc vuông. Danh sách có thể chứa các phần tử thuộc những kiểu khác nhau, nhưng thông thường tất cả các phần tử đều có cùng một kiểu.::

   >>> squares = [1, 4, 9, 16, 25]
   >>> squares
   [1, 4, 9, 16, 25]

Giống như chuỗi (và tất cả các kiểu :term:`sequence` dựng sẵn khác), danh sách có thể được lập chỉ mục và cắt lát::

   >>> squares[0]  # lập chỉ mục trả về phần tử
   1
   >>> squares[-1]
   25
   >>> squares[-3:]  # cắt lát trả về một danh sách mới
   [9, 16, 25]

Danh sách cũng hỗ trợ các phép toán như phép nối::

   >>> squares + [36, 49, 64, 81, 100]
   [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

Không giống như chuỗi, vốn :term:`immutable`, danh sách là một kiểu :term:`mutable`, tức là có thể thay đổi nội dung của chúng::

    >>> cubes = [1, 8, 27, 65, 125]  # có gì đó không đúng ở đây
    >>> 4 ** 3  # lũy thừa bậc ba của 4 là 64, không phải 65!
    64
    >>> cubes[3] = 64  # thay thế giá trị sai
    >>> cubes
    [1, 8, 27, 64, 125]

Bạn cũng có thể thêm các mục mới vào cuối danh sách bằng cách sử dụng :meth:`list.append` *phương thức* (chúng ta sẽ tìm hiểu thêm về các phương thức sau này)::

   >>> cubes.append(216)  # thêm lũy thừa bậc ba của 6
   >>> cubes.append(7 ** 3)  # và lũy thừa bậc ba của 7
   >>> cubes
   [1, 8, 27, 64, 125, 216, 343]

Trong Python, phép gán đơn giản không bao giờ sao chép dữ liệu. Khi bạn gán một danh sách cho một biến, biến đó tham chiếu đến *danh sách hiện có*. Mọi thay đổi bạn thực hiện đối với danh sách thông qua một biến sẽ được nhìn thấy qua tất cả các biến khác tham chiếu đến danh sách đó.::

   >>> rgb = ["Red", "Green", "Blue"]
   >>> rgba = rgb
   >>> id(rgb) == id(rgba)  # chúng tham chiếu đến cùng một đối tượng
   True
   >>> rgba.append("Alph")
   >>> rgb
   ["Red", "Green", "Blue", "Alph"]

Mọi thao tác cắt đều trả về một danh sách mới chứa các phần tử được yêu cầu. Điều này có nghĩa là lát cắt sau đây trả về một
:ref:`bản sao nông (shallow copy) <shallow_vs_deep_copy>` của danh sách::

   >>> correct_rgba = rgba[:]
   >>> correct_rgba[-1] = "Alpha"
   >>> correct_rgba
   ["Red", "Green", "Blue", "Alpha"]
   >>> rgba
   ["Red", "Green", "Blue", "Alph"]

Bạn cũng có thể gán cho các lát cắt, và thao tác này thậm chí có thể thay đổi kích thước danh sách hoặc xóa toàn bộ danh sách::

   >>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
   >>> letters
   ['a', 'b', 'c', 'd', 'e', 'f', 'g']
   >>> # thay thế một số giá trị
   >>> letters[2:5] = ['C', 'D', 'E']
   >>> letters
   ['a', 'b', 'C', 'D', 'E', 'f', 'g']
   >>> # bây giờ xóa chúng
   >>> letters[2:5] = []
   >>> letters
   ['a', 'b', 'f', 'g']
   >>> # xóa danh sách bằng cách thay thế tất cả các phần tử bằng một danh sách rỗng
   >>> letters[:] = []
   >>> letters
   []

Hàm tích hợp sẵn :func:`len` cũng áp dụng cho các danh sách::

   >>> letters = ['a', 'b', 'c', 'd']
   >>> len(letters)
   4

Có thể lồng các danh sách (tạo các danh sách chứa những danh sách khác), chẳng hạn như::

   >>> a = ['a', 'b', 'c']
   >>> n = [1, 2, 3]
   >>> x = [a, n]
   >>> x
   [['a', 'b', 'c'], [1, 2, 3]]
   >>> x[0]
   ['a', 'b', 'c']
   >>> x[0][1]
   'b'

.. _tut-firststeps:

Những bước đầu tiên trong lập trình
===================================

Tất nhiên, chúng ta có thể sử dụng Python cho những tác vụ phức tạp hơn việc cộng hai với hai. Chẳng hạn, chúng ta có thể viết một dãy con ban đầu của `dãy Fibonacci <https://en.wikipedia.org/wiki/Fibonacci_sequence>`_ như sau::

   >>> # dãy Fibonacci:
   >>> # tổng của hai phần tử xác định phần tử tiếp theo
   >>> a, b = 0, 1
   >>> while a < 10:
   ...     print(a)
   ...     a, b = b, a+b
   ...
   0
   1
   1
   2
   3
   5
   8

Ví dụ này giới thiệu một số tính năng mới.

* Dòng đầu tiên chứa một *phép gán nhiều biến*: các biến ``a`` và ``b`` đồng thời nhận các giá trị mới là 0 và 1.  Ở dòng cuối, cách này lại được sử dụng, cho thấy rằng tất cả biểu thức ở vế phải trước tiên đều được đánh giá, rồi sau đó các phép gán mới được thực hiện.  Các biểu thức ở vế phải được đánh giá từ trái sang phải.

* Vòng lặp :keyword:`while` thực thi miễn là điều kiện (ở đây là: ``a < 10``) vẫn đúng.  Trong Python, cũng như trong C, mọi giá trị số nguyên khác không đều được xem là đúng; số 0 là sai.  Điều kiện cũng có thể là một chuỗi hoặc giá trị danh sách, thực tế là bất kỳ sequence nào; mọi sequence có độ dài khác không đều đúng, còn sequence rỗng thì sai.  Phép kiểm tra được sử dụng trong ví dụ là một phép so sánh đơn giản.  Các toán tử so sánh chuẩn được viết giống như trong C: ``<`` (nhỏ hơn), ``>`` (lớn hơn), ``==`` (bằng), ``<=`` (nhỏ hơn hoặc bằng), ``>=`` (lớn hơn hoặc bằng) và ``!=`` (khác).

* *Thân* của vòng lặp được *thụt lề*: thụt lề là cách Python dùng để nhóm các câu lệnh.  Tại dấu nhắc tương tác, bạn phải nhập một tab hoặc một hay nhiều dấu cách cho mỗi dòng được thụt lề.  Trên thực tế, bạn sẽ chuẩn bị phần nhập phức tạp hơn cho Python bằng một trình soạn thảo văn bản; mọi trình soạn thảo văn bản tốt đều có tính năng tự động thụt lề.  Khi nhập một câu lệnh phức hợp theo cách tương tác, phải theo sau câu lệnh đó bằng một dòng trống để cho biết đã hoàn tất (vì parser không thể đoán khi nào bạn đã nhập dòng cuối cùng).  Lưu ý rằng mỗi dòng trong một basic block phải được thụt lề cùng một mức.

* Hàm :func:`print` ghi giá trị của các đối số được truyền vào. Hàm này khác với việc chỉ ghi biểu thức bạn muốn ghi (như chúng ta đã làm trước đó trong các ví dụ về calculator) ở cách xử lý nhiều đối số, các giá trị floating-point và các chuỗi.  Chuỗi được in ra không có dấu ngoặc kép, và một dấu cách được chèn giữa các mục, vì vậy bạn có thể định dạng mọi thứ đẹp mắt, như sau::

     >>> i = 256*256
     >>> print('The value of i is', i)
     The value of i is 65536

  Đối số từ khóa *end* có thể được sử dụng để tránh ký tự xuống dòng sau phần đầu ra hoặc kết thúc phần đầu ra bằng một chuỗi khác::

     >>> a, b = 0, 1
     >>> while a < 1000:
     ...     print(a, end=',')
     ...     a, b = b, a+b
     ...
     0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,


.. rubric:: Chú thích

.. [#] Vì ``**`` có độ ưu tiên cao hơn ``-``, ``-3**2`` sẽ được hiểu là ``-(3**2)`` và do đó cho kết quả là ``-9``.  Để tránh điều này và nhận được ``9``, bạn có thể sử dụng ``(-3)**2``.

.. [#] Không giống như các ngôn ngữ khác, các ký tự đặc biệt như ``\n`` có cùng ý nghĩa khi đặt trong dấu nháy đơn (``'...'``) và dấu nháy kép (``"..."``). Điểm khác biệt duy nhất giữa hai loại này là trong dấu nháy đơn, bạn không cần escape ``"`` (nhưng phải escape ``\'``) và ngược lại.

.. _`Fibonacci series`: https://en.wikipedia.org/wiki/Fibonacci_sequence
