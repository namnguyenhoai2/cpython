=========================================
Câu hỏi thường gặp về Thiết kế và Lịch sử
=========================================

.. only:: html

   .. contents::


Tại sao Python sử dụng thụt lề để nhóm các câu lệnh?
----------------------------------------------------

Guido van Rossum cho rằng việc sử dụng thụt lề để nhóm các câu lệnh cực kỳ tinh tế và góp phần rất lớn vào tính rõ ràng của một chương trình Python điển hình. Sau một thời gian, hầu hết mọi người đều học cách yêu thích tính năng này.

Vì không có dấu ngoặc begin/end nên không thể xảy ra bất đồng giữa cách nhóm mà trình phân tích cú pháp nhận biết và cách người đọc hiểu. Đôi khi các lập trình viên C sẽ gặp một đoạn mã như sau::

   if (x <= y)
           x++;
           y--;
   z++;

Chỉ câu lệnh ``x++`` được thực thi nếu điều kiện đúng, nhưng cách thụt lề khiến nhiều người tin rằng không phải vậy. Ngay cả những lập trình viên C giàu kinh nghiệm đôi khi cũng sẽ nhìn chằm chằm vào đoạn mã này trong một thời gian dài và tự hỏi tại sao ``y`` lại bị giảm ngay cả khi ``x > y``.

Vì không có dấu ngoặc begin/end, Python ít có khả năng phát sinh xung đột về coding style hơn nhiều. Trong C, có rất nhiều cách khác nhau để đặt dấu ngoặc. Sau khi quen với việc đọc và viết mã theo một style cụ thể, việc cảm thấy hơi không thoải mái khi đọc (hoặc được yêu cầu viết) theo một style khác là điều bình thường.


Nhiều coding style đặt dấu ngoặc begin/end trên một dòng riêng. Điều này khiến chương trình dài hơn đáng kể và lãng phí không gian màn hình quý giá, làm việc có được cái nhìn tổng quan về chương trình trở nên khó khăn hơn. Lý tưởng nhất là một function nên vừa trên một màn hình (chẳng hạn 20--30 dòng). 20 dòng Python có thể thực hiện nhiều công việc hơn đáng kể so với 20 dòng C. Điều này không chỉ là do thiếu dấu ngoặc begin/end -- việc thiếu các khai báo và các kiểu dữ liệu cấp cao cũng góp phần -- nhưng cú pháp dựa trên thụt lề chắc chắn giúp ích.


Tại sao tôi nhận được kết quả kỳ lạ với các phép toán số học đơn giản?
----------------------------------------------------------------------

Xem câu hỏi tiếp theo.


Tại sao các phép tính số thực dấu phẩy động lại thiếu chính xác đến vậy?
------------------------------------------------------------------------

Người dùng thường ngạc nhiên trước những kết quả như thế này::

    >>> 1.2 - 1.0
    0.19999999999999996

và cho rằng đó là lỗi trong Python.  Không phải vậy.  Điều này ít liên quan đến Python, mà liên quan nhiều hơn đến cách nền tảng bên dưới xử lý các số dấu phẩy động.

Kiểu :class:`float` trong CPython sử dụng một ``double`` của C để lưu trữ.  Một
đối tượng :class:`float` được lưu trữ dưới dạng số dấu phẩy động nhị phân với độ chính xác cố định (thường là 53 bit), và Python sử dụng các phép toán của C, vốn lần lượt phụ thuộc vào cách triển khai phần cứng trong bộ xử lý, để thực hiện các phép toán dấu phẩy động. Điều này có nghĩa là, xét về các phép toán dấu phẩy động, Python hoạt động giống như nhiều ngôn ngữ phổ biến khác, bao gồm C và Java.

Nhiều số có thể dễ dàng viết dưới dạng thập phân lại không thể được biểu diễn chính xác dưới dạng số dấu phẩy động nhị phân. Ví dụ, sau đây::

    >>> x = 1.2

giá trị được lưu cho ``x`` là một giá trị xấp xỉ (rất tốt) cho giá trị thập phân ``1.2``, nhưng không hoàn toàn bằng nó. Trên một máy tính điển hình, giá trị thực sự được lưu là::

    1.0011001100110011001100110011001100110011001100110011 (binary)

giá trị này chính xác là::

    1.1999999999999999555910790149937383830547332763671875 (decimal)

Độ chính xác thông thường là 53 bit, cung cấp cho các số float của Python độ chính xác từ 15--16 chữ số thập phân.

Để xem phần giải thích đầy đủ hơn, vui lòng tham khảo chương :ref:`phép tính số dấu phẩy động <tut-fp-issues>` trong hướng dẫn Python.


Tại sao chuỗi Python là bất biến?
---------------------------------

Có một số ưu điểm.

Một lý do là hiệu năng: khi biết rằng một chuỗi là bất biến, chúng ta có thể cấp phát không gian cho chuỗi ngay khi tạo, và các yêu cầu lưu trữ là cố định, không thay đổi. Đây cũng là một trong những lý do có sự phân biệt giữa tuple và list.

Một ưu điểm khác là trong Python, chuỗi được xem là có tính "elemental" như các số. Không hoạt động nào có thể thay đổi giá trị 8 thành một giá trị khác, và trong Python, không hoạt động nào có thể thay đổi chuỗi "eight" thành một chuỗi khác.


.. _why-self:

Tại sao phải sử dụng 'self' một cách tường minh trong định nghĩa và lời gọi method?
-----------------------------------------------------------------------------------

Ý tưởng này được mượn từ Modula-3. Hóa ra nó rất hữu ích vì nhiều lý do khác nhau.

Trước hết, điều này giúp nhận thấy rõ hơn rằng bạn đang sử dụng một method hoặc thuộc tính instance thay vì một biến cục bộ. Khi đọc ``self.x`` hoặc ``self.meth()``, bạn có thể hoàn toàn chắc chắn rằng một biến instance hoặc method đang được sử dụng, ngay cả khi bạn không thuộc lòng định nghĩa class. Trong C++, bạn có thể phần nào nhận biết điều này nhờ không có khai báo biến cục bộ (giả sử biến toàn cục hiếm gặp hoặc dễ nhận ra) -- nhưng trong Python không có khai báo biến cục bộ, vì vậy bạn sẽ phải tra cứu định nghĩa class để chắc chắn. Một số tiêu chuẩn viết mã C++ và Java yêu cầu thuộc tính instance có tiền tố ``m_``, vì vậy tính tường minh này vẫn hữu ích trong cả những ngôn ngữ đó.

Thứ hai, điều này có nghĩa là không cần cú pháp đặc biệt nếu bạn muốn tham chiếu hoặc gọi tường minh method từ một class cụ thể. Trong C++, nếu muốn sử dụng một method từ base class bị override trong derived class, bạn phải dùng toán tử ``::`` -- còn trong Python, bạn có thể viết ``baseclass.methodname(self, <argument list>)``. Điều này đặc biệt hữu ích cho các method :meth:`~object.__init__`, và nói chung trong những trường hợp method của derived class muốn mở rộng method của base class có cùng tên, nên phải gọi method của base class bằng cách nào đó.

Cuối cùng, đối với các biến instance, cách này giải quyết một vấn đề cú pháp khi gán: vì các biến cục bộ trong Python (theo định nghĩa!) là những biến được gán một giá trị trong phần thân hàm (và không được khai báo tường minh là biến toàn cục), cần có cách để cho trình thông dịch biết rằng phép gán nhằm gán cho một biến instance thay vì một biến cục bộ, và tốt nhất cách đó nên thể hiện qua cú pháp (vì lý do hiệu năng). C++ thực hiện điều này thông qua các khai báo, nhưng Python không có khai báo và sẽ thật đáng tiếc nếu phải đưa chúng vào chỉ vì mục đích này. Việc sử dụng ``self.var`` tường minh giải quyết vấn đề này một cách gọn gàng. Tương tự, khi sử dụng các biến instance, việc phải viết ``self.var`` có nghĩa là các tham chiếu đến những tên không đủ định tính bên trong một method không cần phải tìm trong các namespace của instance. Nói cách khác, biến cục bộ và biến instance nằm trong hai namespace khác nhau, và bạn cần cho Python biết nên sử dụng namespace nào.


.. _why-can-t-i-use-an-assignment-in-an-expression:

Tại sao tôi không thể sử dụng phép gán trong một biểu thức?
-----------------------------------------------------------

Bắt đầu từ Python 3.8, bạn có thể làm vậy!

Biểu thức gán sử dụng toán tử walrus ``:=`` để gán một biến trong một biểu thức::

   while chunk := fp.read(200):
      print(chunk)

Xem :pep:`572` để biết thêm thông tin.



Tại sao Python sử dụng phương thức cho một số chức năng (ví dụ: list.index()) nhưng lại sử dụng hàm cho những chức năng khác (ví dụ: len(list))?
------------------------------------------------------------------------------------------------------------------------------------------------

Như Guido đã nói:

    (a) Đối với một số phép toán, ký pháp tiền tố dễ đọc hơn
    Các phép toán hậu tố -- tiền tố (và trung tố!) có truyền thống lâu đời trong toán học, vốn ưa chuộng những ký hiệu trực quan giúp các nhà toán học suy nghĩ về một bài toán. Hãy so sánh sự dễ dàng khi viết lại một công thức như x*(a+b) thành x*a + x*b với sự vụng về khi thực hiện điều tương tự bằng ký hiệu OO thuần túy.

    (b) Khi đọc đoạn mã viết len(x), tôi *biết* rằng nó đang yêu cầu
    độ dài của một thứ gì đó. Điều này cho tôi biết hai điều: kết quả là một số nguyên và đối số là một dạng container nào đó. Ngược lại, khi đọc x.len(), tôi phải biết trước rằng x là một dạng container nào đó triển khai một interface hoặc kế thừa từ một class có len() chuẩn. Hãy thử xem sự nhầm lẫn đôi khi xảy ra khi một class không triển khai mapping lại có phương thức get() hoặc keys(), hoặc một thứ không phải là file lại có phương thức write().

    -- https://mail.python.org/pipermail/python-3000/2006-November/004643.html


Tại sao join() lại là một phương thức của string thay vì của list hoặc tuple?
-----------------------------------------------------------------------------

String trở nên giống các kiểu chuẩn khác hơn nhiều bắt đầu từ Python 1.6, khi các phương thức được bổ sung để cung cấp chức năng tương tự như chức năng vốn luôn có sẵn thông qua các hàm của module string. Hầu hết các phương thức mới này đã được chấp nhận rộng rãi, nhưng phương thức khiến một số lập trình viên cảm thấy không thoải mái là::

   ", ".join(['1', '2', '4', '8', '16'])

cho kết quả::

   "1, 2, 4, 8, 16"

Có hai lập luận phổ biến phản đối cách sử dụng này.

Lập luận đầu tiên thường được diễn đạt như sau: "Việc sử dụng một method của string literal (string constant) trông thực sự rất xấu", và câu trả lời là có thể đúng, nhưng string literal chỉ là một giá trị cố định. Nếu cho phép sử dụng các method trên những tên được liên kết với các string thì không có lý do hợp lý nào để không cho phép sử dụng chúng trên các literal.

Phản đối thứ hai thường được diễn đạt như sau: "Tôi thực sự đang yêu cầu một sequence nối các phần tử của nó lại với nhau bằng một string constant". Đáng tiếc là không phải vậy. Vì một lý do nào đó, dường như mọi người ít thấy khó chịu hơn khi :meth:`~str.split` là một string method, vì trong trường hợp đó, ta dễ dàng thấy rằng::

   "1, 2, 4, 8, 16".split(", ")

là một chỉ thị yêu cầu string literal trả về các substring được phân tách bằng separator đã cho (hoặc mặc định là các chuỗi khoảng trắng liên tiếp tùy ý).

:meth:`~str.join` là một string method vì khi sử dụng nó, bạn đang yêu cầu separator string lặp qua một sequence gồm các string và chèn chính nó giữa những phần tử liền kề. Method này có thể được sử dụng với bất kỳ đối số nào tuân theo các quy tắc dành cho sequence object, bao gồm cả những class mới mà bạn có thể tự định nghĩa. Các method tương tự cũng tồn tại cho các object bytes và bytearray.


Exception nhanh đến mức nào?
----------------------------

Một block :keyword:`try`/:keyword:`except` cực kỳ hiệu quả nếu không có exception nào được raised. Thực sự bắt một exception thì tốn kém. Trong các phiên bản Python trước 2.0, người ta thường sử dụng idiom này::

   try:
       value = mydict[key]
   except KeyError:
       mydict[key] = getvalue(key)
       value = mydict[key]

Điều này chỉ hợp lý khi bạn dự kiến dict hầu như lúc nào cũng có key đó. Nếu không phải vậy, bạn sẽ viết code như sau::

   if key in mydict:
       value = mydict[key]
   else:
       value = mydict[key] = getvalue(key)

Trong trường hợp cụ thể này, bạn cũng có thể sử dụng ``value = dict.setdefault(key, getvalue(key))``, nhưng chỉ khi lời gọi ``getvalue()`` đủ rẻ vì nó được đánh giá trong mọi trường hợp.


Tại sao Python không có câu lệnh switch hoặc case?
--------------------------------------------------

Nhìn chung, các câu lệnh switch có cấu trúc sẽ thực thi một khối mã khi một biểu thức có một giá trị hoặc tập hợp giá trị cụ thể. Kể từ Python 3.10, bạn có thể dễ dàng so khớp các giá trị literal hoặc các hằng số trong một namespace bằng câu lệnh ``match ... case``. Xem :ref:`đặc tả <match>` và :ref:`hướng dẫn <tut-match>` để biết thêm thông tin về các câu lệnh :keyword:`match`. Một lựa chọn cũ hơn là một chuỗi ``if... elif... elif... else``.

Trong trường hợp cần lựa chọn trong một số lượng rất lớn khả năng, bạn có thể tạo một dictionary ánh xạ các giá trị case với những hàm cần gọi. Ví dụ:::

   functions = {'a': function_1,
                'b': function_2,
                'c': self.method_1}

   func = functions[value]
   func()

Để gọi các phương thức trên đối tượng, bạn còn có thể đơn giản hóa hơn nữa bằng cách sử dụng
:func:`getattr` tích hợp sẵn để lấy các phương thức có một tên cụ thể::

   class MyVisitor:
       def visit_a(self):
           ...

       def dispatch(self, value):
           method_name = 'visit_' + str(value)
           method = getattr(self, method_name)
           method()

Bạn nên dùng một tiền tố cho tên các phương thức, chẳng hạn như ``visit_`` trong ví dụ này. Nếu không có tiền tố như vậy, khi các giá trị đến từ một nguồn không đáng tin cậy, kẻ tấn công sẽ có thể gọi bất kỳ phương thức nào trên đối tượng của bạn.

Việc mô phỏng switch có fallthrough, như switch-case-default của C, là có thể, nhưng khó hơn nhiều và ít cần thiết hơn.


Không thể mô phỏng thread trong interpreter thay vì dựa vào một implementation thread đặc thù cho hệ điều hành sao?
-------------------------------------------------------------------------------------------------------------------

Câu trả lời 1: Đáng tiếc là interpreter đẩy ít nhất một C stack frame cho mỗi Python stack frame. Ngoài ra, các extension có thể gọi ngược vào Python ở gần như bất kỳ thời điểm nào. Do đó, một implementation thread hoàn chỉnh cần có hỗ trợ thread cho C.

Câu trả lời 2: May mắn thay, có `Stackless Python <https://github.com/stackless-dev/stackless/wiki>`_, với vòng lặp interpreter được thiết kế lại hoàn toàn để tránh C stack.


Tại sao biểu thức lambda không thể chứa statement?
--------------------------------------------------

Biểu thức lambda của Python không thể chứa statement vì khung cú pháp của Python không thể xử lý statement lồng bên trong biểu thức. Tuy nhiên, trong Python, đây không phải là vấn đề nghiêm trọng. Không giống các dạng lambda trong những ngôn ngữ khác, nơi chúng bổ sung chức năng, lambda của Python chỉ là một cách viết tắt nếu bạn quá lười định nghĩa một function.

Function vốn đã là first-class object trong Python và có thể được khai báo trong phạm vi cục bộ. Vì vậy, lợi ích duy nhất của việc dùng lambda thay cho một function được định nghĩa cục bộ là bạn không cần nghĩ ra tên cho function — nhưng đó chỉ là một biến cục bộ được gán cho function object (chính xác là cùng kiểu object mà một biểu thức lambda tạo ra)!


Python có thể được biên dịch thành mã máy, C hoặc một ngôn ngữ nào khác không?
------------------------------------------------------------------------------

`Cython <https://cython.org/>`_ biên dịch một phiên bản Python đã được sửa đổi, có thêm các chú thích tùy chọn, thành các phần mở rộng C. `Nuitka <https://nuitka.net/>`_ là một trình biên dịch Python mới nổi, chuyển Python thành mã C++, với mục tiêu hỗ trợ đầy đủ ngôn ngữ Python.


Python quản lý bộ nhớ như thế nào?
----------------------------------

Chi tiết về việc quản lý bộ nhớ của Python phụ thuộc vào bản triển khai. Bản triển khai tiêu chuẩn của Python, :term:`CPython`, sử dụng cơ chế đếm tham chiếu để phát hiện các đối tượng không thể truy cập, cùng một cơ chế khác để thu gom các chu trình tham chiếu; định kỳ, cơ chế này thực thi một thuật toán phát hiện chu trình để tìm các chu trình không thể truy cập và xóa những đối tượng liên quan. Mô-đun :mod:`gc` cung cấp các hàm để thực hiện thu gom rác, lấy số liệu thống kê gỡ lỗi và điều chỉnh các tham số của bộ thu gom.

Tuy nhiên, các bản triển khai khác (chẳng hạn như `Jython <https://www.jython.org>`_ hoặc `PyPy <https://pypy.org>`_) có thể dựa vào một cơ chế khác, chẳng hạn như một bộ thu gom rác đầy đủ. Sự khác biệt này có thể gây ra một số vấn đề chuyển mã tinh vi nếu mã Python của bạn phụ thuộc vào hành vi của bản triển khai sử dụng cơ chế đếm tham chiếu.

Trong một số bản triển khai Python, đoạn mã sau (hoạt động bình thường trong CPython) có thể sẽ dùng hết các bộ mô tả tệp::

   for file in very_long_list_of_files:
       f = open(file)
       c = f.read(1)

Quả thực, với cơ chế đếm tham chiếu và lược đồ destructor của CPython, mỗi phép gán mới cho ``f`` sẽ đóng tệp trước đó. Tuy nhiên, với một GC truyền thống, các đối tượng tệp đó chỉ được thu gom (và đóng) theo những khoảng thời gian khác nhau, có thể khá dài.

Nếu bạn muốn viết mã hoạt động với mọi triển khai Python, bạn nên đóng tệp một cách rõ ràng hoặc sử dụng câu lệnh :keyword:`with`; cách này sẽ hoạt động bất kể cơ chế quản lý bộ nhớ nào được sử dụng::

   for file in very_long_list_of_files:
       with open(file) as f:
           c = f.read(1)


Tại sao CPython không sử dụng một cơ chế garbage collection truyền thống hơn?
-----------------------------------------------------------------------------

Trước hết, đây không phải là một tính năng của tiêu chuẩn C nên không có tính portable. (Đúng vậy, chúng tôi biết về thư viện Boehm GC. Thư viện này có các đoạn mã assembler cho *hầu hết* các nền tảng phổ biến, nhưng không phải tất cả, và mặc dù phần lớn hoạt động minh bạch, nó không hoàn toàn minh bạch; cần có các bản vá để Python hoạt động với thư viện này.)

GC truyền thống cũng trở thành một vấn đề khi Python được nhúng vào các ứng dụng khác. Trong một Python độc lập, việc thay thế ``malloc()`` tiêu chuẩn và ``free()`` bằng các phiên bản do thư viện GC cung cấp là điều ổn, nhưng một ứng dụng nhúng Python có thể muốn có *bộ thay thế* ``malloc()`` và ``free()`` riêng, đồng thời có thể không muốn sử dụng các phiên bản của Python. Hiện tại, CPython hoạt động với mọi thứ triển khai đúng ``malloc()`` và ``free()``.


Tại sao không phải toàn bộ bộ nhớ đều được giải phóng khi CPython thoát?
------------------------------------------------------------------------

Các đối tượng được tham chiếu từ không gian tên toàn cục của các mô-đun Python không phải lúc nào cũng được giải phóng khi Python thoát. Điều này có thể xảy ra nếu tồn tại các tham chiếu vòng. Ngoài ra, có một số phần bộ nhớ được thư viện C cấp phát nhưng không thể giải phóng (ví dụ: một công cụ như Purify sẽ cảnh báo về chúng). Tuy nhiên, Python rất tích cực dọn dẹp bộ nhớ khi thoát và cố gắng hủy từng đối tượng.

Nếu muốn buộc Python xóa một số thứ khi giải phóng bộ nhớ, hãy sử dụng
module :mod:`atexit` để chạy một hàm buộc giải phóng các đối tượng đó.


Tại sao lại có các kiểu dữ liệu tuple và list riêng biệt?
---------------------------------------------------------

Mặc dù tuple và list giống nhau ở nhiều khía cạnh, chúng thường được sử dụng theo những cách hoàn toàn khác nhau. Có thể hình dung tuple tương tự như ``records`` của Pascal hoặc ``structs`` của C; chúng là những tập hợp nhỏ gồm các dữ liệu có liên quan, có thể thuộc các kiểu khác nhau và được xử lý như một nhóm. Ví dụ, một tọa độ Descartes thích hợp được biểu diễn dưới dạng tuple gồm hai hoặc ba số.

Mặt khác, list giống với mảng trong các ngôn ngữ khác hơn. Chúng thường chứa một số lượng đối tượng thay đổi, tất cả đều cùng kiểu và được xử lý từng đối tượng một. Ví dụ, :func:`os.listdir('.') <os.listdir>` trả về một list các chuỗi đại diện cho những tệp trong thư mục hiện tại. Các hàm xử lý kết quả này nhìn chung sẽ không bị ảnh hưởng nếu bạn thêm một hoặc hai tệp vào thư mục.

Tuple là bất biến, nghĩa là một khi tuple đã được tạo, bạn không thể thay thế bất kỳ phần tử nào của nó bằng một giá trị mới. List là khả biến, nghĩa là bạn luôn có thể thay đổi các phần tử của list. Chỉ các phần tử bất biến mới có thể được dùng làm khóa dictionary, vì vậy chỉ tuple, chứ không phải list, mới có thể được dùng làm khóa.


.. _how-are-lists-implemented:

List được triển khai trong CPython như thế nào?
-----------------------------------------------

List của CPython thực chất là các mảng có độ dài thay đổi, không phải linked list theo kiểu Lisp. Cách triển khai này sử dụng một mảng liên tục chứa các tham chiếu đến những đối tượng khác, đồng thời lưu một con trỏ đến mảng đó và độ dài của mảng trong một cấu trúc đầu list.

Điều này khiến việc lập chỉ mục một danh sách ``a[i]`` trở thành một thao tác có chi phí không phụ thuộc vào kích thước của danh sách hay giá trị của chỉ mục.

Khi các phần tử được thêm vào cuối hoặc chèn vào, mảng tham chiếu sẽ được thay đổi kích thước. Một số kỹ thuật được áp dụng để cải thiện hiệu suất khi liên tục thêm phần tử vào cuối; khi mảng cần được mở rộng, một phần không gian bổ sung sẽ được cấp phát để vài lần tiếp theo không cần thực sự thay đổi kích thước.

Xem :ref:`time-complexity` để biết chi phí của các thao tác danh sách khác nhau.


.. _how-are-dictionaries-implemented:

Từ điển được triển khai như thế nào trong CPython?
--------------------------------------------------

Từ điển của CPython được triển khai dưới dạng các bảng băm có thể thay đổi kích thước. So với cây B, cách này cho hiệu suất tra cứu tốt hơn (cho đến nay là thao tác phổ biến nhất) trong hầu hết trường hợp, đồng thời việc triển khai cũng đơn giản hơn.

Từ điển hoạt động bằng cách tính mã băm cho mỗi khóa được lưu trong từ điển bằng hàm dựng sẵn :func:`hash`. Mã băm thay đổi rất lớn tùy thuộc vào khóa và một seed riêng cho mỗi process; chẳng hạn, ``'Python'`` có thể được băm thành ``-539294296``, trong khi ``'python'``, một chuỗi chỉ khác một bit, có thể được băm thành ``1142331976``. Sau đó, mã băm được dùng để tính vị trí trong một mảng nội bộ, nơi giá trị sẽ được lưu trữ. Nếu giả định rằng bạn đang lưu các khóa có giá trị băm khác nhau, điều này có nghĩa là từ điển mất thời gian hằng số -- *O*\ (1), theo ký hiệu Big-O -- để truy xuất một khóa.

Xem :ref:`time-complexity` để biết chi phí của các thao tác từ điển khác nhau.


Tại sao các khóa của dictionary phải là bất biến?
-------------------------------------------------

Cài đặt bảng băm của dictionary sử dụng một giá trị băm được tính từ giá trị của khóa để tìm khóa đó. Nếu khóa là một đối tượng có thể thay đổi, giá trị của nó có thể thay đổi, và do đó giá trị băm của nó cũng có thể thay đổi. Tuy nhiên, vì người thay đổi đối tượng khóa không biết rằng nó đang được dùng làm khóa dictionary nên không thể di chuyển mục nhập đó trong dictionary. Khi bạn cố tra cứu lại chính đối tượng đó trong dictionary, nó sẽ không được tìm thấy vì giá trị băm của nó đã khác. Nếu bạn cố tra cứu giá trị cũ thì cũng không tìm thấy, vì giá trị của đối tượng nằm trong bin băm đó đã khác.

Nếu muốn lập chỉ mục dictionary bằng một list, chỉ cần chuyển list thành tuple trước; hàm ``tuple(L)`` tạo một tuple có các phần tử giống với list ``L``. Tuple là bất biến và do đó có thể được dùng làm khóa dictionary.

Một số giải pháp không thể chấp nhận đã được đề xuất:

- Băm list theo địa chỉ của chúng (ID đối tượng). Cách này không hiệu quả vì nếu bạn tạo một list mới có cùng giá trị thì nó sẽ không được tìm thấy; ví dụ:::

     mydict = {[1, 2]: '12'}
     print(mydict[[1, 2]])

  sẽ gây ra ngoại lệ :exc:`KeyError` vì ID của ``[1, 2]`` được dùng ở dòng thứ hai khác với ID ở dòng đầu tiên. Nói cách khác, các khóa dictionary nên được so sánh bằng ``==``, không phải bằng :keyword:`is`.

- Tạo một bản sao khi dùng list làm khóa. Cách này không hiệu quả vì list, vốn là một đối tượng có thể thay đổi, có thể chứa một tham chiếu đến chính nó, và khi đó mã sao chép sẽ rơi vào vòng lặp vô hạn.

- Cho phép các list làm khóa nhưng hãy nói rõ với người dùng rằng không được sửa đổi chúng. Điều này có thể dẫn đến một nhóm lỗi khó truy vết trong chương trình khi bạn vô tình quên hoặc sửa đổi một list. Nó cũng làm mất một bất biến quan trọng của dictionary: mọi giá trị trong ``d.keys()`` đều có thể được dùng làm khóa của dictionary.

- Đánh dấu các list là chỉ đọc ngay khi chúng được dùng làm khóa dictionary. Vấn đề là không chỉ đối tượng cấp cao nhất mới có thể thay đổi giá trị của nó; bạn có thể dùng một tuple chứa một list làm khóa. Việc đưa bất kỳ thứ gì vào dictionary làm khóa sẽ yêu cầu đánh dấu tất cả đối tượng có thể truy cập từ đó là chỉ đọc — và một lần nữa, các đối tượng tự tham chiếu có thể gây ra vòng lặp vô hạn.

Có một mẹo để xử lý vấn đề này nếu bạn cần, nhưng hãy tự chịu rủi ro khi sử dụng: Bạn có thể bọc một cấu trúc có thể thay đổi bên trong một thể hiện lớp có cả một
:meth:`~object.__eq__` và một phương thức :meth:`~object.__hash__`. Sau đó, bạn phải bảo đảm rằng giá trị băm của tất cả các đối tượng wrapper như vậy đang nằm trong một dictionary (hoặc cấu trúc dựa trên hash khác) vẫn cố định trong thời gian đối tượng nằm trong dictionary (hoặc cấu trúc khác đó).::

   class ListWrapper:
       def __init__(self, the_list):
           self.the_list = the_list

       def __eq__(self, other):
           return self.the_list == other.the_list

       def __hash__(self):
           l = self.the_list
           result = 98767 - len(l)*555
           for i, el in enumerate(l):
               try:
                   result = result + (hash(el) % 9999999) * 1001 + i
               except Exception:
                   result = (result % 7777777) + i * 333
           return result

Lưu ý rằng việc tính hash trở nên phức tạp do khả năng một số phần tử của list có thể không hash được, cũng như khả năng xảy ra tràn số học.

Hơn nữa, luôn phải đúng rằng nếu ``o1 == o2`` (tức là ``o1.__eq__(o2) is True``) thì ``hash(o1) == hash(o2)`` (tức là ``o1.__hash__() == o2.__hash__()``), bất kể đối tượng có nằm trong dictionary hay không. Nếu không đáp ứng các giới hạn này, dictionary và những cấu trúc dựa trên hash khác sẽ hoạt động sai.

Trong trường hợp :class:`!ListWrapper`, bất cứ khi nào đối tượng wrapper nằm trong dictionary, list được bọc không được thay đổi để tránh các hành vi bất thường. Đừng làm điều này trừ khi bạn sẵn sàng suy nghĩ cẩn thận về các yêu cầu và hậu quả của việc không đáp ứng đúng chúng. Hãy coi đây là lời cảnh báo.


Tại sao list.sort() không trả về danh sách đã sắp xếp?
------------------------------------------------------

Trong những tình huống cần quan tâm đến hiệu năng, việc tạo một bản sao của danh sách chỉ để sắp xếp sẽ rất lãng phí. Vì vậy, :meth:`list.sort` sắp xếp danh sách ngay tại chỗ. Để nhắc bạn về điều đó, hàm này không trả về danh sách đã sắp xếp. Nhờ vậy, bạn sẽ không vô tình ghi đè lên một danh sách khi cần một bản sao đã sắp xếp nhưng vẫn muốn giữ lại phiên bản chưa sắp xếp.

Nếu muốn trả về một danh sách mới, thay vào đó hãy sử dụng hàm :func:`sorted` tích hợp sẵn. Hàm này tạo một danh sách mới từ một iterable được cung cấp, sắp xếp danh sách đó rồi trả về. Ví dụ, sau đây là cách lặp qua các khóa của một dictionary theo thứ tự đã sắp xếp::

   for key in sorted(mydict):
       ...  # thực hiện bất cứ điều gì với mydict[key]...


Làm thế nào để chỉ định và thực thi một đặc tả interface trong Python?
----------------------------------------------------------------------

Đặc tả interface cho một module, như được cung cấp bởi các ngôn ngữ như C++ và Java, mô tả các prototype của những method và function trong module. Nhiều người cho rằng việc thực thi đặc tả interface tại thời điểm biên dịch giúp ích cho việc xây dựng các chương trình lớn.

Python 2.6 bổ sung module :mod:`abc`, cho phép bạn định nghĩa Abstract Base Class (ABC). Sau đó, bạn có thể sử dụng :func:`isinstance` và :func:`issubclass` để kiểm tra xem một instance hoặc một class có triển khai một ABC cụ thể hay không.
Mô-đun :mod:`collections.abc` định nghĩa một tập hợp các ABC hữu ích như
:class:`~collections.abc.Iterable`, :class:`~collections.abc.Container`, và
:class:`~collections.abc.MutableMapping`.

Trong Python, nhiều ưu điểm của các đặc tả interface có thể đạt được bằng một quy trình kiểm thử phù hợp cho các component.

Một test suite tốt cho một module vừa có thể cung cấp kiểm thử hồi quy, vừa đóng vai trò là đặc tả interface của module và một tập hợp các ví dụ. Nhiều module Python có thể được chạy dưới dạng script để cung cấp một "self test" đơn giản. Ngay cả những module sử dụng các interface bên ngoài phức tạp thường cũng có thể được kiểm thử độc lập bằng các mô phỏng "stub" đơn giản của interface bên ngoài. :mod:`doctest` và
các module :mod:`unittest` hoặc các test framework của bên thứ ba có thể được dùng để xây dựng các test suite toàn diện, thực thi mọi dòng mã trong một module.

Một quy trình kiểm thử phù hợp có thể giúp xây dựng các ứng dụng lớn, phức tạp bằng Python cũng hiệu quả như khi có các đặc tả interface. Trên thực tế, cách này có thể tốt hơn vì một đặc tả interface không thể kiểm thử một số thuộc tính nhất định của chương trình. Ví dụ, phương thức :meth:`list.append` được kỳ vọng sẽ thêm các phần tử mới vào cuối một danh sách nội bộ; một đặc tả interface không thể kiểm thử việc triển khai :meth:`list.append` của bạn có thực sự thực hiện đúng điều này hay không, nhưng việc kiểm tra thuộc tính này trong một test suite lại rất đơn giản.

Viết các test suite rất hữu ích, và bạn có thể muốn thiết kế mã của mình sao cho dễ kiểm thử. Một kỹ thuật ngày càng phổ biến, test-driven development, yêu cầu viết trước một phần test suite, trước khi viết bất kỳ mã thực tế nào. Tất nhiên, Python cho phép bạn làm qua loa và hoàn toàn không viết các test case.


Tại sao không có goto?
----------------------

Vào những năm 1970, người ta nhận ra rằng goto không bị hạn chế có thể dẫn đến mã "spaghetti" rối rắm, khó hiểu và khó sửa đổi. Trong một ngôn ngữ cấp cao, goto cũng không cần thiết miễn là có các cách để rẽ nhánh (trong Python, bằng các câu lệnh :keyword:`if` và :keyword:`or`,
:keyword:`and`, và các biểu thức :keyword:`if`/:keyword:`else`) và lặp (bằng các câu lệnh :keyword:`while` và :keyword:`for`, có thể chứa :keyword:`continue` và :keyword:`break`).

Bạn cũng có thể sử dụng exception để cung cấp một "goto có cấu trúc" hoạt động ngay cả khi đi qua các lần gọi hàm. Nhiều người cho rằng exception có thể mô phỏng thuận tiện mọi cách sử dụng hợp lý của các cấu trúc ``go`` hoặc ``goto`` trong C, Fortran và các ngôn ngữ khác. Ví dụ::

   class label(Exception): pass  # khai báo một nhãn

   try:
       ...
       if condition: raise label()  # goto đến nhãn
       ...
   except label:  # điểm cần goto đến
       pass
   ...

Điều này không cho phép bạn nhảy vào giữa một vòng lặp, nhưng việc đó thường bị xem là lạm dụng ``goto`` dù sao đi nữa. Hãy sử dụng một cách hạn chế.


Tại sao chuỗi thô (r-strings) không thể kết thúc bằng dấu gạch chéo ngược?
--------------------------------------------------------------------------

Chính xác hơn, chúng không thể kết thúc bằng một số lẻ dấu gạch chéo ngược: dấu gạch chéo ngược không đi cặp ở cuối sẽ escape ký tự dấu ngoặc kép đóng, khiến chuỗi không được kết thúc.

Chuỗi thô được thiết kế để giúp dễ dàng tạo đầu vào cho các bộ xử lý (chủ yếu là các regular expression engine) muốn tự xử lý việc escape dấu gạch chéo ngược. Các bộ xử lý như vậy vốn cũng xem dấu gạch chéo ngược đơn độc ở cuối là một lỗi, nên chuỗi thô không cho phép điều đó. Đổi lại, chúng cho phép bạn truyền nguyên ký tự dấu ngoặc kép của chuỗi bằng cách escape ký tự đó với một dấu gạch chéo ngược. Những quy tắc này hoạt động hiệu quả khi r-strings được sử dụng cho mục đích đã định.

Nếu bạn đang cố tạo pathname cho Windows, hãy lưu ý rằng mọi system call của Windows cũng chấp nhận dấu gạch chéo xuôi::

   f = open("/mydir/file.txt")  # hoạt động hoàn toàn tốt!

Nếu bạn đang cố tạo pathname cho một lệnh DOS, hãy thử một trong các cách sau::

   dir = r"\this\is\my\dos\dir" "\\"
   dir = r"\this\is\my\dos\dir\ "[:-1]
   dir = "\\this\\is\\my\\dos\\dir\\"


Tại sao Python không có câu lệnh "with" để gán thuộc tính?
----------------------------------------------------------

Python có câu lệnh :keyword:`with` bao bọc việc thực thi một khối lệnh, gọi mã khi bắt đầu và kết thúc khối lệnh. Một số ngôn ngữ có một cấu trúc trông như sau::

   with obj:
       a = 1               # tương đương với obj.a = 1
       total = total + 1   # obj.total = obj.total + 1

Trong Python, một cấu trúc như vậy sẽ gây ra sự mơ hồ.

Các ngôn ngữ khác, chẳng hạn như Object Pascal, Delphi và C++, sử dụng kiểu tĩnh, vì vậy có thể xác định một cách rõ ràng thành viên nào đang được gán. Đây là điểm chính của việc định kiểu tĩnh -- trình biên dịch *always* biết phạm vi của mọi biến tại thời điểm biên dịch.

Python sử dụng kiểu động. Không thể biết trước thuộc tính nào sẽ được tham chiếu trong runtime. Các thuộc tính thành viên có thể được thêm vào hoặc xóa khỏi đối tượng ngay trong lúc chạy. Điều này khiến việc xác định thuộc tính nào đang được tham chiếu chỉ bằng cách đọc đơn giản trở nên bất khả thi: thuộc tính cục bộ, thuộc tính toàn cục hay thuộc tính thành viên?

Ví dụ, hãy xem đoạn mã chưa hoàn chỉnh sau đây::

   def foo(a):
       with a:
           print(x)

Đoạn mã giả định rằng ``a`` phải có một thuộc tính thành viên có tên là ``x``. Tuy nhiên, không có gì trong Python cho trình thông dịch biết điều này. Điều gì sẽ xảy ra nếu ``a``, chẳng hạn, là một số nguyên? Nếu có một biến toàn cục tên là ``x``, biến đó có được sử dụng bên trong khối :keyword:`with` không? Như bạn thấy, tính động của Python khiến những lựa chọn như vậy khó hơn nhiều.

Tuy nhiên, lợi ích chính của :keyword:`with` và các tính năng tương tự của ngôn ngữ (giảm lượng mã) có thể dễ dàng đạt được trong Python bằng phép gán. Thay vì::

   function(args).mydict[index][index].a = 21
   function(args).mydict[index][index].b = 42
   function(args).mydict[index][index].c = 63

viết như sau::

   ref = function(args).mydict[index][index]
   ref.a = 21
   ref.b = 42
   ref.c = 63

Điều này cũng có tác dụng phụ là tăng tốc độ thực thi, vì các liên kết tên được phân giải tại thời điểm chạy trong Python, còn phiên bản thứ hai chỉ cần thực hiện việc phân giải một lần.

Các đề xuất tương tự nhằm đưa vào cú pháp để tiếp tục giảm lượng mã, chẳng hạn như sử dụng 'leading dot', đã bị từ chối để ưu tiên tính rõ ràng (xem https://mail.python.org/pipermail/python-ideas/2016-May/040070.html).


Tại sao generator không hỗ trợ câu lệnh with?
---------------------------------------------

Vì lý do kỹ thuật, generator được sử dụng trực tiếp như một context manager sẽ không hoạt động chính xác. Trong trường hợp phổ biến nhất, khi generator được sử dụng như một iterator chạy đến khi hoàn tất thì không cần đóng nó. Khi cần đóng, hãy bọc nó dưới dạng :func:`contextlib.closing(generator) <contextlib.closing>` trong câu lệnh :keyword:`with`.


Tại sao cần có dấu hai chấm cho các câu lệnh if/while/def/class?
----------------------------------------------------------------

Dấu hai chấm chủ yếu được yêu cầu để tăng khả năng đọc (một trong những kết quả của ngôn ngữ ABC thử nghiệm). Hãy xem xét điều này::

   if a == b
       print(a)

so với::

   if a == b:
       print(a)

Hãy chú ý rằng cách thứ hai dễ đọc hơn một chút. Hơn nữa, hãy chú ý cách dấu hai chấm tách riêng ví dụ trong câu trả lời FAQ này; đây là cách dùng tiêu chuẩn trong tiếng Anh.

Một lý do nhỏ khác là dấu hai chấm giúp các trình soạn thảo có syntax highlighting dễ xử lý hơn; chúng có thể tìm dấu hai chấm để quyết định khi nào cần tăng mức thụt lề, thay vì phải phân tích văn bản chương trình phức tạp hơn.


Tại sao Python cho phép có dấu phẩy ở cuối các list và tuple?
-------------------------------------------------------------

Python cho phép bạn thêm dấu phẩy ở cuối danh sách, tuple và dictionary::

   [1, 2, 3,]
   ('a', 'b', 'c',)
   d = {
       "A": [1, 5],
       "B": [6, 7],  # dấu phẩy ở cuối cùng là tùy chọn nhưng là phong cách tốt
   }


Có một số lý do để cho phép điều này.

Khi một giá trị literal của danh sách, tuple hoặc dictionary được trải dài trên nhiều dòng, việc thêm phần tử sẽ dễ dàng hơn vì bạn không phải nhớ thêm dấu phẩy vào dòng trước đó. Các dòng cũng có thể được sắp xếp lại mà không gây ra lỗi cú pháp.

Vô tình bỏ sót dấu phẩy có thể dẫn đến những lỗi khó chẩn đoán. Ví dụ:::

       x = [
         "fee",
         "fie"
         "foo",
         "fum"
       ]

Danh sách này trông như có bốn phần tử, nhưng thực tế chỉ chứa ba phần tử: "fee", "fiefoo" và "fum". Luôn thêm dấu phẩy sẽ tránh được nguồn gây lỗi này.

Việc cho phép dấu phẩy ở cuối cũng có thể giúp việc tạo mã bằng chương trình dễ dàng hơn.

.. _`Stackless Python`: https://github.com/stackless-dev/stackless/wiki
.. _`Cython`: https://cython.org/
.. _`Nuitka`: https://nuitka.net/
.. _`Jython`: https://www.jython.org
.. _`PyPy`: https://pypy.org
