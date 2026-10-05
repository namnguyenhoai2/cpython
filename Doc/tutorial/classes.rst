.. _tut-classes:

***
Lớp
***

Lớp cung cấp một cách để đóng gói dữ liệu và chức năng lại với nhau. Việc tạo một lớp mới sẽ tạo ra một *kiểu* đối tượng mới, cho phép tạo các *thể hiện* mới của kiểu đó. Mỗi thể hiện của lớp có thể được gắn các thuộc tính để duy trì trạng thái của nó. Các thể hiện của lớp cũng có thể có các phương thức (được định nghĩa bởi lớp đó) để sửa đổi trạng thái của chúng.

So với các ngôn ngữ lập trình khác, cơ chế lớp của Python bổ sung các lớp với tối thiểu cú pháp và ngữ nghĩa mới. Đây là sự kết hợp giữa các cơ chế lớp trong C++ và Modula-3. Các lớp Python cung cấp mọi tính năng tiêu chuẩn của Lập trình hướng đối tượng: cơ chế kế thừa lớp cho phép có nhiều lớp cơ sở, một lớp dẫn xuất có thể ghi đè bất kỳ phương thức nào của lớp hoặc các lớp cơ sở, và một phương thức có thể gọi phương thức của lớp cơ sở có cùng tên. Đối tượng có thể chứa lượng và kiểu dữ liệu tùy ý. Cũng như module, lớp mang bản chất động của Python: chúng được tạo tại runtime và có thể tiếp tục được sửa đổi sau khi tạo.

Theo thuật ngữ C++, thông thường các thành viên của lớp (bao gồm cả thành viên dữ liệu) là *public* (ngoại trừ trường hợp được nêu bên dưới :ref:`tut-private`), và tất cả các hàm thành viên đều là *virtual*. Giống như trong Modula-3, không có cách viết tắt nào để tham chiếu đến các thành viên của đối tượng từ các phương thức của nó: hàm phương thức được khai báo với một đối số đầu tiên tường minh đại diện cho đối tượng, và đối số này được truyền ngầm định khi gọi. Giống như trong Smalltalk, bản thân các lớp cũng là đối tượng. Điều này cung cấp ngữ nghĩa cho việc import và đổi tên. Không giống C++ và Modula-3, các kiểu dựng sẵn có thể được dùng làm lớp cơ sở để người dùng mở rộng. Ngoài ra, cũng như trong C++, hầu hết các toán tử dựng sẵn có cú pháp đặc biệt (toán tử số học, phép lập chỉ mục, v.v.) đều có thể được định nghĩa lại cho các thể hiện của lớp.

(Do chưa có thuật ngữ được chấp nhận rộng rãi để nói về các lớp, đôi khi tôi sẽ sử dụng các thuật ngữ của Smalltalk và C++. Tôi sẽ dùng các thuật ngữ của Modula-3, vì ngữ nghĩa hướng đối tượng của nó gần với Python hơn C++, nhưng tôi cho rằng ít độc giả từng nghe về ngôn ngữ này.)


.. _tut-object:

Đôi Lời Về Tên và Đối Tượng
===========================

Đối tượng có tính riêng biệt, và nhiều tên (trong nhiều phạm vi khác nhau) có thể được liên kết với cùng một đối tượng. Trong các ngôn ngữ khác, điều này được gọi là aliasing. Điều này thường không dễ nhận thấy khi mới tìm hiểu Python, và có thể an toàn bỏ qua khi làm việc với các kiểu cơ bản bất biến (số, chuỗi, tuple). Tuy nhiên, aliasing có thể gây ra ảnh hưởng bất ngờ đến ngữ nghĩa của mã Python khi mã đó liên quan đến các đối tượng khả biến như danh sách, từ điển và hầu hết các kiểu khác. Điều này thường được tận dụng để có lợi cho chương trình, vì trong một số khía cạnh, các alias hoạt động giống như con trỏ. Ví dụ, việc truyền một đối tượng rất tiết kiệm vì trong quá trình triển khai chỉ có một con trỏ được truyền; và nếu một hàm sửa đổi đối tượng được truyền dưới dạng đối số, bên gọi sẽ thấy thay đổi đó — điều này loại bỏ nhu cầu về hai cơ chế truyền đối số khác nhau như trong Pascal.


.. _tut-scopes:

Phạm vi và không gian tên trong Python
======================================

Trước khi giới thiệu về các lớp, trước hết tôi phải nói với bạn một chút về các quy tắc phạm vi của Python. Các định nghĩa lớp thực hiện một số thủ thuật thú vị với không gian tên, và bạn cần biết cách hoạt động của phạm vi và không gian tên để hiểu đầy đủ những gì đang diễn ra. Nhân tiện, kiến thức về chủ đề này hữu ích cho mọi lập trình viên Python nâng cao.

Hãy bắt đầu với một số định nghĩa.

Một *không gian tên* là một ánh xạ từ tên đến đối tượng. Hầu hết không gian tên hiện được triển khai dưới dạng dictionary của Python, nhưng điều đó thường không thể nhận thấy theo bất kỳ cách nào (ngoại trừ hiệu năng), và có thể thay đổi trong tương lai. Ví dụ về không gian tên gồm: tập hợp các tên dựng sẵn (chứa các hàm như :func:`abs`, và các tên ngoại lệ dựng sẵn); các tên toàn cục trong một module; và các tên cục bộ trong một lần gọi hàm. Theo một nghĩa nào đó, tập hợp các thuộc tính của một đối tượng cũng tạo thành một không gian tên. Điều quan trọng cần biết về không gian tên là hoàn toàn không có mối liên hệ nào giữa các tên trong những không gian tên khác nhau; chẳng hạn, hai module khác nhau đều có thể định nghĩa một hàm ``maximize`` mà không gây nhầm lẫn --- người dùng của các module phải thêm tên module vào trước nó.

Nhân tiện, tôi dùng từ *thuộc tính* cho mọi tên đứng sau dấu chấm --- ví dụ, trong biểu thức ``z.real``, ``real`` là một thuộc tính của đối tượng ``z``. Nói chính xác, các tham chiếu đến tên trong module là các tham chiếu thuộc tính: trong biểu thức ``modname.funcname``, ``modname`` là một đối tượng module và ``funcname`` là một thuộc tính của nó. Trong trường hợp này, tình cờ có một ánh xạ trực tiếp giữa các thuộc tính của module và các tên toàn cục được định nghĩa trong module: chúng dùng chung một không gian tên! [#]_

Các thuộc tính có thể chỉ đọc hoặc có thể ghi. Trong trường hợp sau, có thể gán giá trị cho thuộc tính. Các thuộc tính của module có thể ghi: bạn có thể viết ``modname.the_answer = 42``. Các thuộc tính có thể ghi cũng có thể bị xóa bằng
câu lệnh :keyword:`del`. Ví dụ, ``del modname.the_answer`` sẽ xóa thuộc tính :attr:`!the_answer` khỏi đối tượng được đặt tên bởi ``modname``.

Các namespace được tạo tại những thời điểm khác nhau và có thời gian tồn tại khác nhau. Namespace chứa các tên dựng sẵn được tạo khi trình thông dịch Python khởi động và không bao giờ bị xóa. Namespace toàn cục của một module được tạo khi phần định nghĩa module được đọc vào; thông thường, các namespace của module cũng tồn tại cho đến khi trình thông dịch kết thúc. Các câu lệnh được thực thi bởi lần gọi cấp cao nhất của trình thông dịch, dù được đọc từ một tệp script hay được nhập tương tác, được xem là một phần của module có tên :mod:`__main__`, vì vậy chúng có namespace toàn cục riêng. (Thực tế, các tên dựng sẵn cũng nằm trong một module; module này có tên :mod:`builtins`.)

Namespace cục bộ của một hàm được tạo khi hàm được gọi và bị xóa khi hàm trả về hoặc phát sinh một ngoại lệ không được xử lý bên trong hàm. (Thực ra, "quên đi" sẽ là cách mô tả chính xác hơn những gì thực sự xảy ra.) Tất nhiên, mỗi lần gọi đệ quy đều có namespace cục bộ riêng.

*Phạm vi* là một vùng văn bản của chương trình Python, nơi một namespace có thể được truy cập trực tiếp. Ở đây, "có thể được truy cập trực tiếp" nghĩa là một tham chiếu không đủ định danh đến một tên sẽ cố gắng tìm tên đó trong namespace.

Mặc dù các phạm vi được xác định tĩnh, chúng được sử dụng động. Tại bất kỳ thời điểm nào trong quá trình thực thi, có 3 hoặc 4 phạm vi lồng nhau mà các namespace của chúng có thể được truy cập trực tiếp:

* phạm vi bên trong cùng, được tìm kiếm trước tiên, chứa các tên cục bộ
* các phạm vi của mọi hàm bao quanh, được tìm kiếm bắt đầu từ phạm vi bao quanh gần nhất, chứa các tên không cục bộ nhưng cũng không toàn cục
* phạm vi áp chót chứa các tên toàn cục của module hiện tại
* phạm vi ngoài cùng (được tìm kiếm sau cùng) là namespace chứa các tên dựng sẵn

Nếu một tên được khai báo là global, thì mọi tham chiếu và phép gán đều trỏ trực tiếp đến phạm vi kế ngoài cùng chứa các tên global của module. Để gán lại các biến được tìm thấy bên ngoài phạm vi trong cùng, có thể sử dụng câu lệnh :keyword:`nonlocal`; nếu không được khai báo là nonlocal, các biến đó chỉ được đọc (việc cố gắng ghi vào một biến như vậy sẽ đơn giản tạo một biến cục bộ *new* trong phạm vi trong cùng, và giữ nguyên biến bên ngoài có cùng tên).

Thông thường, phạm vi cục bộ tham chiếu đến các tên cục bộ của hàm hiện tại (theo văn bản). Bên ngoài các hàm, phạm vi cục bộ tham chiếu đến cùng namespace với phạm vi global: namespace của module. Các định nghĩa lớp đặt thêm một namespace khác vào phạm vi cục bộ.

Điều quan trọng là nhận ra rằng các phạm vi được xác định theo văn bản: phạm vi global của một hàm được định nghĩa trong một module là namespace của module đó, bất kể hàm được gọi từ đâu hoặc bằng bí danh nào. Mặt khác, việc tìm kiếm tên thực tế được thực hiện một cách động, tại thời điểm chạy --- tuy nhiên, định nghĩa ngôn ngữ đang tiến tới việc phân giải tên tĩnh, tại thời điểm "biên dịch", vì vậy đừng dựa vào việc phân giải tên động! (Trên thực tế, các biến cục bộ đã được xác định một cách tĩnh.)

Một đặc điểm đặc biệt của Python là -- nếu không có câu lệnh :keyword:`global` hoặc :keyword:`nonlocal` nào có hiệu lực -- việc gán cho các tên luôn diễn ra trong phạm vi trong cùng. Phép gán không sao chép dữ liệu --- chúng chỉ liên kết tên với các đối tượng. Điều tương tự cũng đúng với việc xóa: câu lệnh ``del x`` xóa liên kết của ``x`` khỏi namespace được phạm vi cục bộ tham chiếu đến. Trên thực tế, mọi thao tác giới thiệu tên mới đều sử dụng phạm vi cục bộ: cụ thể là các câu lệnh :keyword:`import` và các định nghĩa hàm liên kết tên module hoặc hàm trong phạm vi cục bộ.

Câu lệnh :keyword:`global` có thể được sử dụng để chỉ ra rằng các biến cụ thể nằm trong phạm vi global và cần được gán lại tại đó; còn
Câu lệnh :keyword:`nonlocal` chỉ ra rằng các biến cụ thể nằm trong một phạm vi bao quanh và cần được gán lại tại đó.

.. _tut-scopeexample:

Ví dụ về Phạm vi và Namespace
-----------------------------

Đây là một ví dụ minh họa cách tham chiếu đến các phạm vi và namespace khác nhau, cũng như cách :keyword:`global` và :keyword:`nonlocal` ảnh hưởng đến việc liên kết biến::

   def scope_test():
       def do_local():
           spam = "local spam"

       def do_nonlocal():
           nonlocal spam
           spam = "nonlocal spam"

       def do_global():
           global spam
           spam = "global spam"

       spam = "test spam"
       do_local()
       print("After local assignment:", spam)
       do_nonlocal()
       print("After nonlocal assignment:", spam)
       do_global()
       print("After global assignment:", spam)

   scope_test()
   print("In global scope:", spam)

Kết quả của mã ví dụ là:

.. code-block:: none

   After local assignment: test spam
   After nonlocal assignment: nonlocal spam
   After global assignment: nonlocal spam
   In global scope: global spam

Lưu ý rằng phép gán *local* (mặc định) không thay đổi liên kết *scope_test*\'s của *spam*.  Phép gán :keyword:`nonlocal` đã thay đổi liên kết *scope_test*\'s của *spam*, còn phép gán :keyword:`global` đã thay đổi liên kết ở cấp module.

Bạn cũng có thể thấy rằng trước đó chưa có liên kết nào cho *spam* trước
:keyword:`global` phép gán.


.. _tut-firstclasses:

Tìm hiểu sơ lược về Class
=========================

Các class giới thiệu một chút cú pháp mới, ba kiểu đối tượng mới và một số ngữ nghĩa mới.


.. _tut-classdefinition:

Cú pháp định nghĩa class
------------------------

Dạng đơn giản nhất của định nghĩa class có dạng như sau::

   class ClassName:
       <statement-1>
       .
       .
       .
       <statement-N>

Các định nghĩa lớp, giống như các định nghĩa hàm (các câu lệnh :keyword:`def`), phải được thực thi trước khi chúng có bất kỳ tác dụng nào. (Về mặt lý thuyết, bạn có thể đặt một định nghĩa lớp trong một nhánh của câu lệnh :keyword:`if`, hoặc bên trong một hàm.)

Trong thực tế, các câu lệnh bên trong một định nghĩa class thường sẽ là các định nghĩa hàm, nhưng những câu lệnh khác cũng được cho phép và đôi khi hữu ích — chúng ta sẽ quay lại vấn đề này sau. Các định nghĩa hàm bên trong một class thường có một dạng danh sách đối số đặc biệt, do quy ước gọi dành cho các method quy định — vấn đề này cũng sẽ được giải thích sau.

Khi một định nghĩa class được thực thi, một namespace mới được tạo và dùng làm phạm vi cục bộ — do đó, mọi phép gán cho các biến cục bộ đều được đưa vào namespace mới này. Cụ thể, các định nghĩa hàm sẽ liên kết tên của hàm mới tại đây.

Khi một định nghĩa class kết thúc bình thường (thông qua lệnh kết thúc), một *đối tượng class* được tạo. Về cơ bản, đây là một wrapper bao quanh nội dung của namespace được tạo bởi định nghĩa class; chúng ta sẽ tìm hiểu thêm về các đối tượng class trong phần tiếp theo. Phạm vi cục bộ ban đầu (phạm vi có hiệu lực ngay trước khi định nghĩa class được thực thi) được khôi phục, và đối tượng class được liên kết tại đây với tên class được nêu trong phần đầu của định nghĩa class (:class:`!ClassName` trong ví dụ).


.. _tut-classobjects:

Đối tượng lớp
-------------

Đối tượng lớp hỗ trợ hai loại thao tác: tham chiếu thuộc tính và khởi tạo.

*Tham chiếu thuộc tính* sử dụng cú pháp tiêu chuẩn được dùng cho mọi tham chiếu thuộc tính trong Python: ``obj.name``.  Các tên thuộc tính hợp lệ là tất cả những tên có trong namespace của lớp tại thời điểm đối tượng lớp được tạo.  Vì vậy, nếu định nghĩa lớp có dạng như sau::

   class MyClass:
       """A simple example class"""
       i = 12345

       def f(self):
           return 'hello world'

thì ``MyClass.i`` và ``MyClass.f`` là các tham chiếu thuộc tính hợp lệ, lần lượt trả về một số nguyên và một đối tượng hàm. Bạn cũng có thể gán cho các thuộc tính lớp, vì vậy có thể thay đổi giá trị của ``MyClass.i`` bằng phép gán.
:attr:`~type.__doc__` cũng là một thuộc tính hợp lệ, trả về docstring của lớp: ``"A simple example class"``.

*Khởi tạo* lớp sử dụng ký hiệu hàm.  Chỉ cần coi đối tượng lớp như một hàm không có tham số, trả về một instance mới của lớp. Ví dụ (giả sử lớp ở trên)::

   x = MyClass()

tạo một *instance* mới của lớp và gán đối tượng này cho biến cục bộ ``x``.

Thao tác khởi tạo ("gọi" một đối tượng lớp) tạo ra một đối tượng rỗng. Nhiều lớp muốn tạo các đối tượng có các instance được tùy chỉnh theo một trạng thái ban đầu cụ thể. Vì vậy, một lớp có thể định nghĩa một phương thức đặc biệt có tên
:meth:`~object.__init__`, như sau::

   def __init__(self):
       self.data = []

Khi một lớp định nghĩa phương thức :meth:`~object.__init__`, thao tác khởi tạo lớp sẽ tự động gọi :meth:`!__init__` cho instance lớp mới được tạo. Vì vậy, trong ví dụ này, có thể nhận được một instance mới đã được khởi tạo bằng cách::

   x = MyClass()

Tất nhiên, phương thức :meth:`~object.__init__` có thể nhận các đối số để tăng tính linh hoạt. Trong trường hợp đó, các đối số được truyền cho toán tử khởi tạo lớp sẽ được chuyển tiếp đến :meth:`!__init__`. Ví dụ:::

   >>> class Complex:
   ...     def __init__(self, realpart, imagpart):
   ...         self.r = realpart
   ...         self.i = imagpart
   ...
   >>> x = Complex(3.0, -4.5)
   >>> x.r, x.i
   (3.0, -4.5)


.. _tut-instanceobjects:

Các đối tượng instance
----------------------

Vậy chúng ta có thể làm gì với các đối tượng instance? Các thao tác duy nhất mà đối tượng instance hiểu được là tham chiếu thuộc tính. Có hai loại tên thuộc tính hợp lệ: thuộc tính dữ liệu và phương thức.

*Thuộc tính dữ liệu* tương ứng với "biến instance" trong Smalltalk và "thành viên dữ liệu" trong C++. Không cần khai báo thuộc tính dữ liệu; giống như các biến cục bộ, chúng xuất hiện khi được gán lần đầu. Ví dụ: nếu ``x`` là instance của :class:`!MyClass` được tạo ở trên, đoạn mã sau sẽ in ra giá trị ``16`` mà không để lại dấu vết::

   x.counter = 1
   while x.counter < 10:
       x.counter = x.counter * 2
   print(x.counter)
   del x.counter

Loại tham chiếu thuộc tính instance còn lại là một *method*. Method là một hàm "thuộc về" một object.

.. index:: pair: object; method

Các tên method hợp lệ của một instance object phụ thuộc vào class của nó. Theo định nghĩa, mọi thuộc tính của một class là các function object đều định nghĩa các method tương ứng của các instance thuộc class đó. Vì vậy, trong ví dụ của chúng ta, ``x.f`` là một tham chiếu method hợp lệ, vì ``MyClass.f`` là một function, nhưng ``x.i`` thì không, vì ``MyClass.i`` không phải là một function. Tuy nhiên, ``x.f`` không giống với ``MyClass.f`` --- nó là một *method object*, không phải một function object.


.. _tut-methodobjects:

Các Method Object
-----------------

Thông thường, một method được gọi ngay sau khi nó được gắn vào object::

   x.f()

Nếu ``x = MyClass()``, như ở trên, thì thao tác này sẽ trả về chuỗi ``'hello world'``. Tuy nhiên, không nhất thiết phải gọi method ngay lập tức: ``x.f`` là một method object, có thể được lưu lại và gọi vào thời điểm sau. Ví dụ::

   xf = x.f
   while True:
       print(xf())

sẽ tiếp tục in ``hello world`` cho đến tận cùng thời gian.

Chính xác thì điều gì xảy ra khi một method được gọi? Có thể bạn đã nhận thấy rằng ``x.f()`` được gọi mà không có đối số ở trên, mặc dù định nghĩa function cho :meth:`!f` chỉ rõ một đối số. Đối số đó đã biến đi đâu? Chắc chắn Python sẽ phát sinh một exception khi một function yêu cầu đối số được gọi mà không có đối số nào --- ngay cả khi đối số đó thực tế không được sử dụng...

Thực ra, có thể bạn đã đoán được câu trả lời: điểm đặc biệt của các method là đối tượng instance được truyền làm đối số đầu tiên của hàm. Trong ví dụ của chúng ta, lời gọi ``x.f()`` hoàn toàn tương đương với ``MyClass.f(x)``. Nói chung, việc gọi một method với danh sách gồm *n* đối số tương đương với việc gọi hàm tương ứng bằng một danh sách đối số được tạo ra bằng cách chèn đối tượng instance của method vào trước đối số đầu tiên.

Nói chung, các method hoạt động như sau. Khi tham chiếu đến một thuộc tính không phải dữ liệu của một instance, lớp của instance đó sẽ được tìm kiếm. Nếu tên đó biểu thị một thuộc tính hợp lệ của lớp và thuộc tính này là một đối tượng hàm, các tham chiếu đến cả đối tượng instance lẫn đối tượng hàm sẽ được đóng gói thành một đối tượng method. Khi đối tượng method được gọi với một danh sách đối số, một danh sách đối số mới được tạo từ đối tượng instance và danh sách đối số, rồi đối tượng hàm được gọi với danh sách đối số mới này.


.. _tut-class-and-instance-variables:

Biến lớp và biến instance
-------------------------

Nói chung, biến instance dùng cho dữ liệu riêng của từng instance, còn biến lớp dùng cho các thuộc tính và method được mọi instance của lớp chia sẻ::

    class Dog:

        kind = 'canine'         # biến lớp được mọi instance chia sẻ

        def __init__(self, name):
            self.name = name    # biến instance riêng của từng instance

    >>> d = Dog('Fido')
    >>> e = Dog('Buddy')
    >>> d.kind                  # được mọi dog chia sẻ
    'canine'
    >>> e.kind                  # được mọi dog chia sẻ
    'canine'
    >>> d.name                  # duy nhất đối với d
    'Fido'
    >>> e.name                  # duy nhất đối với e
    'Buddy'

Như đã thảo luận trong :ref:`tut-object`, dữ liệu dùng chung có thể gây ra những tác động không ngờ tới, liên quan đến các đối tượng :term:`mutable` như lists và dictionaries. Ví dụ: không nên sử dụng danh sách *tricks* trong đoạn mã sau làm class variable, vì chỉ một danh sách duy nhất sẽ được chia sẻ cho tất cả các instance của *Dog*::

    class Dog:

        tricks = []             # sử dụng nhầm class variable

        def __init__(self, name):
            self.name = name

        def add_trick(self, trick):
            self.tricks.append(trick)

    >>> d = Dog('Fido')
    >>> e = Dog('Buddy')
    >>> d.add_trick('roll over')
    >>> e.add_trick('play dead')
    >>> d.tricks                # được chia sẻ ngoài dự kiến cho tất cả các dog
    ['roll over', 'play dead']

Thiết kế đúng của class nên sử dụng instance variable thay thế::

    class Dog:

        def __init__(self, name):
            self.name = name
            self.tricks = []    # tạo một danh sách trống mới cho mỗi con chó

        def add_trick(self, trick):
            self.tricks.append(trick)

    >>> d = Dog('Fido')
    >>> e = Dog('Buddy')
    >>> d.add_trick('roll over')
    >>> e.add_trick('play dead')
    >>> d.tricks
    ['roll over']
    >>> e.tricks
    ['play dead']


.. _tut-remarks:

Những nhận xét khác
===================

.. These should perhaps be placed more carefully...

Nếu cùng một tên thuộc tính xuất hiện cả trong instance và trong class, thì việc tra cứu thuộc tính sẽ ưu tiên instance::

    >>> class Warehouse:
    ...    purpose = 'storage'
    ...    region = 'west'
    ...
    >>> w1 = Warehouse()
    >>> print(w1.purpose, w1.region)
    storage west
    >>> w2 = Warehouse()
    >>> w2.region = 'east'
    >>> print(w2.purpose, w2.region)
    storage east

Các thuộc tính dữ liệu có thể được các method tham chiếu, cũng như được người dùng thông thường ("client") của một đối tượng tham chiếu. Nói cách khác, không thể sử dụng các class để triển khai các kiểu dữ liệu trừu tượng thuần túy. Trên thực tế, không có điều gì trong Python khiến việc thực thi data hiding trở nên khả thi --- mọi thứ đều dựa trên quy ước. (Mặt khác, triển khai Python được viết bằng C có thể ẩn hoàn toàn các chi tiết triển khai và kiểm soát quyền truy cập vào một đối tượng nếu cần; các extension cho Python được viết bằng C có thể sử dụng khả năng này.)

Các client nên cẩn thận khi sử dụng các thuộc tính dữ liệu --- client có thể làm hỏng các bất biến do các method duy trì bằng cách ghi đè lên các thuộc tính dữ liệu của chúng. Lưu ý rằng client có thể thêm các thuộc tính dữ liệu của riêng mình vào một instance object mà không ảnh hưởng đến tính hợp lệ của các method, miễn là tránh xung đột tên --- một lần nữa, một quy ước đặt tên có thể giúp tránh rất nhiều rắc rối ở đây.

Không có cách viết tắt nào để tham chiếu các thuộc tính dữ liệu (hoặc các method khác!) từ bên trong các method. Tôi nhận thấy điều này thực sự làm tăng khả năng dễ đọc của các method: khi xem lướt qua một method, không có khả năng nhầm lẫn giữa các biến cục bộ và các biến instance.

Thông thường, đối số đầu tiên của một method được gọi là ``self``. Đây không gì khác ngoài một quy ước: tên ``self`` hoàn toàn không có ý nghĩa đặc biệt nào đối với Python. Tuy nhiên, hãy lưu ý rằng nếu không tuân theo quy ước, code của bạn có thể kém dễ đọc hơn đối với các lập trình viên Python khác, và cũng có thể có một chương trình *trình duyệt class* được viết dựa trên quy ước như vậy.

Bất kỳ đối tượng hàm nào là thuộc tính lớp đều định nghĩa một phương thức cho các thể hiện của lớp đó. Định nghĩa hàm không nhất thiết phải được đặt về mặt văn bản bên trong định nghĩa lớp: việc gán một đối tượng hàm cho một biến cục bộ trong lớp cũng được. Ví dụ::

   # Hàm được định nghĩa bên ngoài lớp
   def f1(self, x, y):
       return min(x, x+y)

   class C:
       f = f1

       def g(self):
           return 'hello world'

       h = g

Bây giờ ``f``, ``g`` và ``h`` đều là các thuộc tính của lớp :class:`!C` tham chiếu đến các đối tượng hàm, và do đó chúng đều là các phương thức của các thể hiện của
:class:`!C` --- ``h`` hoàn toàn tương đương với ``g``. Lưu ý rằng cách làm này thường chỉ khiến người đọc chương trình bối rối.

Các phương thức có thể gọi những phương thức khác bằng cách sử dụng các thuộc tính phương thức của đối số ``self``::

   class Bag:
       def __init__(self):
           self.data = []

       def add(self, x):
           self.data.append(x)

       def addtwice(self, x):
           self.add(x)
           self.add(x)

Các phương thức có thể tham chiếu đến các tên toàn cục theo cùng cách như các hàm thông thường. Phạm vi toàn cục liên kết với một phương thức là module chứa định nghĩa của phương thức đó. (Một lớp không bao giờ được dùng làm phạm vi toàn cục.) Mặc dù hiếm khi có lý do chính đáng để sử dụng dữ liệu toàn cục trong một phương thức, phạm vi toàn cục vẫn có nhiều công dụng hợp lệ: chẳng hạn, các hàm và module được import vào phạm vi toàn cục có thể được các phương thức sử dụng, cũng như các hàm và lớp được định nghĩa trong đó. Thông thường, lớp chứa phương thức cũng được định nghĩa trong phạm vi toàn cục này, và trong phần tiếp theo, chúng ta sẽ thấy một số lý do chính đáng khiến một phương thức muốn tham chiếu đến chính lớp của nó.

Mỗi giá trị là một đối tượng, và do đó có một *class* (còn gọi là *type*). Nó được lưu trữ dưới dạng ``object.__class__``.


.. _tut-inheritance:

Kế thừa
=======

Tất nhiên, một tính năng của ngôn ngữ sẽ không xứng đáng với tên gọi "class" nếu không hỗ trợ tính kế thừa. Cú pháp định nghĩa một derived class có dạng như sau::

   class DerivedClassName(BaseClassName):
       <statement-1>
       .
       .
       .
       <statement-N>

Tên :class:`!BaseClassName` phải được định nghĩa trong một namespace có thể truy cập từ scope chứa định nghĩa derived class. Thay cho tên base class, cũng có thể sử dụng các biểu thức tùy ý khác. Điều này có thể hữu ích, chẳng hạn khi base class được định nghĩa trong một module khác::

   class DerivedClassName(modname.BaseClassName):

Việc thực thi định nghĩa derived class diễn ra giống như đối với base class. Khi class object được tạo, base class sẽ được ghi nhớ. Thông tin này được dùng để phân giải các tham chiếu thuộc tính: nếu không tìm thấy thuộc tính được yêu cầu trong class, quá trình tìm kiếm sẽ tiếp tục trong base class. Quy tắc này được áp dụng đệ quy nếu bản thân base class được derived từ một class khác.

Không có gì đặc biệt trong việc khởi tạo derived class: ``DerivedClassName()`` tạo một instance mới của class. Các tham chiếu đến method được phân giải như sau: thuộc tính tương ứng của class được tìm kiếm, đi xuống theo chuỗi các base class nếu cần, và tham chiếu đến method hợp lệ nếu kết quả là một function object.

Derived class có thể override các method của base class. Vì các method không có đặc quyền đặc biệt khi gọi các method khác của cùng một object, một method của base class gọi một method khác được định nghĩa trong cùng base class có thể kết thúc bằng việc gọi method của derived class đã override method đó. (Dành cho các lập trình viên C++: mọi method trong Python về cơ bản đều là ``virtual``.)

Một overriding method trong derived class thực tế có thể muốn mở rộng thay vì chỉ thay thế method cùng tên của base class. Có một cách đơn giản để gọi trực tiếp method của base class: chỉ cần gọi ``BaseClassName.methodname(self, arguments)``. Điều này đôi khi cũng hữu ích cho các client. (Lưu ý rằng cách này chỉ hoạt động nếu base class có thể được truy cập dưới dạng ``BaseClassName`` trong global scope.)

Python có hai hàm tích hợp sẵn hoạt động với tính kế thừa:

* Sử dụng :func:`isinstance` để kiểm tra kiểu của một instance: ``isinstance(obj, int)`` sẽ là ``True`` chỉ khi ``obj.__class__`` là :class:`int` hoặc một lớp dẫn xuất từ :class:`int`.

* Sử dụng :func:`issubclass` để kiểm tra tính kế thừa của lớp: ``issubclass(bool, int)`` là ``True`` vì :class:`bool` là lớp con của :class:`int`. Tuy nhiên, ``issubclass(float, int)`` là ``False`` vì :class:`float` không phải là lớp con của :class:`int`.



.. _tut-multiple:

Đa kế thừa
----------

Python cũng hỗ trợ một dạng đa kế thừa. Định nghĩa một lớp với nhiều lớp cơ sở có dạng như sau::

   class DerivedClassName(Base1, Base2, Base3):
       <statement-1>
       .
       .
       .
       <statement-N>

Trong hầu hết mục đích sử dụng và các trường hợp đơn giản, bạn có thể hình dung việc tìm kiếm các thuộc tính được kế thừa từ lớp cha là tìm kiếm theo chiều sâu, từ trái sang phải, không tìm kiếm cùng một lớp hai lần khi có phần chồng lấp trong hệ phân cấp. Do đó, nếu không tìm thấy một thuộc tính trong :class:`!DerivedClassName`, thuộc tính đó sẽ được tìm kiếm trong :class:`!Base1`, rồi (đệ quy) trong các lớp cơ sở của :class:`!Base1`; nếu vẫn không tìm thấy ở đó, thuộc tính đó sẽ được tìm kiếm trong :class:`!Base2`, và tiếp tục như vậy.

Thực tế, vấn đề phức tạp hơn một chút; thứ tự phân giải phương thức thay đổi động để hỗ trợ các lời gọi phối hợp đến :func:`super`. Cách tiếp cận này được gọi trong một số ngôn ngữ đa kế thừa khác là call-next-method và mạnh mẽ hơn lời gọi super trong các ngôn ngữ chỉ hỗ trợ đơn kế thừa.

Việc sắp xếp động là cần thiết vì mọi trường hợp đa kế thừa đều thể hiện một hoặc nhiều quan hệ hình thoi (trong đó có ít nhất một lớp cha có thể được truy cập qua nhiều đường dẫn từ lớp thấp nhất). Ví dụ, mọi lớp đều kế thừa từ :class:`object`, nên mọi trường hợp đa kế thừa đều cung cấp nhiều hơn một đường dẫn để đến :class:`object`. Để ngăn các lớp cơ sở bị truy cập nhiều hơn một lần, thuật toán động tuyến tính hóa thứ tự tìm kiếm theo cách bảo toàn thứ tự từ trái sang phải được chỉ định trong mỗi lớp, gọi mỗi lớp cha đúng một lần và có tính đơn điệu (nghĩa là một lớp có thể được tạo lớp con mà không ảnh hưởng đến thứ tự ưu tiên của các lớp cha). Kết hợp lại, những thuộc tính này giúp có thể thiết kế các lớp đáng tin cậy và có khả năng mở rộng bằng đa kế thừa. Để biết thêm chi tiết, hãy xem
:ref:`python_2.3_mro`.


.. _tut-private:

Biến riêng tư
=============

Các biến instance “riêng tư” không thể được truy cập ngoại trừ từ bên trong một đối tượng không tồn tại trong Python. Tuy nhiên, hầu hết mã Python đều tuân theo một quy ước: một tên có tiền tố là dấu gạch dưới (ví dụ: ``_spam``) nên được xem là một phần không công khai của API (dù đó là một function, method hay data member). Nó nên được xem là chi tiết triển khai và có thể thay đổi mà không cần thông báo.

.. index::
   pair: name; mangling

Vì có trường hợp sử dụng hợp lệ cho các thành viên riêng tư của lớp (cụ thể là để tránh xung đột tên với các tên được định nghĩa bởi các lớp con), Python hỗ trợ hạn chế cho cơ chế như vậy, gọi là :dfn:`name mangling`. Mọi identifier có dạng ``__spam`` (ít nhất hai dấu gạch dưới ở đầu và nhiều nhất một dấu gạch dưới ở cuối) đều được thay thế về mặt văn bản bằng ``_classname__spam``, trong đó ``classname`` là tên lớp hiện tại sau khi đã loại bỏ các dấu gạch dưới ở đầu. Việc đổi tên này được thực hiện mà không xét đến vị trí cú pháp của identifier, miễn là nó xuất hiện trong phần định nghĩa của một lớp.

.. seealso::

   :ref:`Các đặc tả về đổi tên tên riêng tư <private-name-mangling>` để biết chi tiết và các trường hợp đặc biệt.

Việc đổi tên giúp các lớp con ghi đè các method mà không làm hỏng các lệnh gọi method giữa các thành phần trong cùng lớp. Ví dụ::

   class Mapping:
       def __init__(self, iterable):
           self.items_list = []
           self.__update(iterable)

       def update(self, iterable):
           for item in iterable:
               self.items_list.append(item)

       __update = update   # bản sao riêng tư của method update() gốc

   class MappingSubclass(Mapping):

       def update(self, keys, values):
           # cung cấp chữ ký mới cho update()
           # nhưng không làm hỏng __init__()
           for item in zip(keys, values):
               self.items_list.append(item)

Ví dụ trên vẫn hoạt động ngay cả khi ``MappingSubclass`` giới thiệu một định danh ``__update`` vì nó được thay thế bằng ``_Mapping__update`` trong lớp ``Mapping`` và ``_MappingSubclass__update`` trong lớp ``MappingSubclass`` tương ứng.

Lưu ý rằng các quy tắc đổi tên chủ yếu được thiết kế để tránh những sự cố vô tình; bạn vẫn có thể truy cập hoặc sửa đổi một biến được coi là private. Điều này thậm chí có thể hữu ích trong những trường hợp đặc biệt, chẳng hạn như khi sử dụng debugger.

Lưu ý rằng code được truyền cho ``exec()`` hoặc ``eval()`` không coi tên lớp của lớp gọi là lớp hiện tại; điều này tương tự hiệu ứng của câu lệnh ``global``, mà hiệu ứng của nó cũng chỉ giới hạn ở code được byte-compile cùng nhau. Hạn chế tương tự áp dụng cho ``getattr()``, ``setattr()`` và ``delattr()``, cũng như khi tham chiếu trực tiếp đến ``__dict__``.


.. _tut-odds:

Những điều lặt vặt khác
=======================

Đôi khi, việc có một kiểu dữ liệu tương tự như "record" của Pascal hoặc "struct" của C, dùng để nhóm một vài mục dữ liệu có tên, sẽ rất hữu ích. Cách tiếp cận theo phong cách Python là sử dụng :mod:`dataclasses` cho mục đích này::

    from dataclasses import dataclass

    @dataclass
    class Employee:
        name: str
        dept: str
        salary: int

::

    >>> john = Employee('john', 'computer lab', 1000)
    >>> john.dept
    'computer lab'
    >>> john.salary
    1000

Một đoạn mã Python yêu cầu một kiểu dữ liệu trừu tượng cụ thể thường có thể được truyền vào một lớp mô phỏng các phương thức của kiểu dữ liệu đó. Ví dụ: nếu bạn có một hàm định dạng dữ liệu từ một đối tượng tệp, bạn có thể định nghĩa một lớp với các phương thức :meth:`~io.TextIOBase.read` và
:meth:`~io.TextIOBase.readline` để lấy dữ liệu từ một bộ đệm chuỗi thay thế, rồi truyền lớp đó làm đối số.

.. (Unfortunately, this technique has its limitations: a class can't define
   operations that are accessed by special syntax such as sequence subscripting
   or arithmetic operators, and assigning such a "pseudo-file" to sys.stdin will
   not cause the interpreter to read further input from it.)

:ref:`Đối tượng phương thức instance <instance-methods>` cũng có các thuộc tính:
:attr:`m.__self__ <method.__self__>` là đối tượng instance chứa phương thức :meth:`!m`, còn :attr:`m.__func__ <method.__func__>` là :ref:`đối tượng hàm <user-defined-funcs>` tương ứng với phương thức.


.. _tut-iterators:

Bộ lặp
======

Đến lúc này, có lẽ bạn đã nhận thấy rằng hầu hết các đối tượng container đều có thể được lặp qua bằng câu lệnh :keyword:`for`::

   for element in [1, 2, 3]:
       print(element)
   for element in (1, 2, 3):
       print(element)
   for key in {'one':1, 'two':2}:
       print(key)
   for char in "123":
       print(char)
   for line in open("myfile.txt"):
       print(line, end='')

Cách truy cập này rõ ràng, ngắn gọn và thuận tiện. Việc sử dụng iterator xuất hiện xuyên suốt và thống nhất Python. Phía sau, câu lệnh :keyword:`for` gọi :func:`iter` trên đối tượng container. Hàm này trả về một đối tượng iterator định nghĩa phương thức :meth:`~iterator.__next__`, dùng để truy cập từng phần tử trong container. Khi không còn phần tử nào,
:meth:`~iterator.__next__` phát sinh một ngoại lệ :exc:`StopIteration`, báo cho vòng lặp biết phải kết thúc
Vòng lặp :keyword:`!for` sẽ kết thúc. Bạn có thể gọi phương thức :meth:`~iterator.__next__` bằng hàm dựng sẵn :func:`next`; ví dụ này cho thấy mọi thứ hoạt động như thế nào::

   >>> s = 'abc'
   >>> it = iter(s)
   >>> it
   <str_iterator object at 0x10c90e650>
   >>> next(it)
   'a'
   >>> next(it)
   'b'
   >>> next(it)
   'c'
   >>> next(it)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       next(it)
   StopIteration

Sau khi đã hiểu cơ chế đằng sau iterator protocol, bạn có thể dễ dàng thêm hành vi iterator vào các lớp của mình. Hãy định nghĩa một phương thức :meth:`~container.__iter__` trả về một đối tượng có phương thức :meth:`~iterator.__next__`. Nếu lớp định nghĩa :meth:`!__next__`, thì :meth:`!__iter__` chỉ cần trả về ``self``::

   class Reverse:
       """Iterator for looping over a sequence backwards."""
       def __init__(self, data):
           self.data = data
           self.index = len(data)

       def __iter__(self):
           return self

       def __next__(self):
           if self.index == 0:
               raise StopIteration
           self.index = self.index - 1
           return self.data[self.index]

::

   >>> rev = Reverse('spam')
   >>> iter(rev)
   <__main__.Reverse object at 0x00A1DB50>
   >>> for char in rev:
   ...     print(char)
   ...
   m
   a
   p
   s


.. _tut-generators:

Generator
=========

:term:`Generator <generator>` là một công cụ đơn giản nhưng mạnh mẽ để tạo iterator. Chúng được viết như các hàm thông thường nhưng sử dụng câu lệnh :keyword:`yield` mỗi khi muốn trả về dữ liệu. Mỗi lần gọi :func:`next` trên generator, generator sẽ tiếp tục từ nơi đã dừng lại trước đó (nó ghi nhớ tất cả các giá trị dữ liệu và câu lệnh được thực thi gần nhất). Ví dụ này cho thấy việc tạo generator có thể dễ dàng đến mức nào::

   def reverse(data):
       for index in range(len(data)-1, -1, -1):
           yield data[index]

::

   >>> for char in reverse('golf'):
   ...     print(char)
   ...
   f
   l
   o
   g

Mọi việc có thể thực hiện bằng generator cũng có thể thực hiện bằng iterator dựa trên lớp như được mô tả trong phần trước. Điều khiến generator trở nên ngắn gọn là các phương thức :meth:`~iterator.__iter__` và :meth:`~generator.__next__` được tự động tạo ra.

Một tính năng quan trọng khác là các biến cục bộ và trạng thái thực thi được tự động lưu lại giữa các lần gọi. Nhờ đó, việc viết hàm trở nên dễ dàng hơn và rõ ràng hơn nhiều so với cách tiếp cận sử dụng các biến thể hiện như ``self.index`` và ``self.data``.

Ngoài việc tự động tạo method và lưu trạng thái chương trình, khi generator kết thúc, chúng còn tự động phát sinh :exc:`StopIteration`. Kết hợp lại, các tính năng này giúp dễ dàng tạo iterator mà không tốn nhiều công sức hơn so với việc viết một hàm thông thường.


.. _tut-genexps:

Generator Expression
====================

Một số generator đơn giản có thể được viết ngắn gọn dưới dạng expression bằng cú pháp tương tự list comprehension nhưng sử dụng dấu ngoặc tròn thay vì dấu ngoặc vuông. Các expression này được thiết kế cho những trường hợp generator được một hàm bao ngoài sử dụng ngay lập tức. Generator expression ngắn gọn hơn nhưng kém linh hoạt hơn các định nghĩa generator đầy đủ, đồng thời thường sử dụng bộ nhớ hiệu quả hơn so với list comprehension tương đương.

Ví dụ::

   >>> sum(i*i for i in range(10))                 # tổng các bình phương
   285

   >>> xvec = [10, 20, 30]
   >>> yvec = [7, 5, 3]
   >>> sum(x*y for x,y in zip(xvec, yvec))         # tích vô hướng
   260

   >>> unique_words = set(word for line in page  for word in line.split())

   >>> valedictorian = max((student.gpa, student.name) for student in graduates)

   >>> data = 'golf'
   >>> list(data[i] for i in range(len(data)-1, -1, -1))
   ['f', 'l', 'o', 'g']



.. rubric:: Chú thích cuối trang

.. [#] Ngoại trừ một điều. Các đối tượng module có một thuộc tính chỉ đọc bí mật được gọi là
   :attr:`~object.__dict__`, thuộc tính này trả về dictionary được dùng để triển khai namespace của module; tên ``__dict__`` là một thuộc tính nhưng không phải là tên toàn cục. Rõ ràng, việc sử dụng thuộc tính này vi phạm tính trừu tượng của việc triển khai namespace và nên chỉ được giới hạn cho những thứ như trình gỡ lỗi post-mortem.
