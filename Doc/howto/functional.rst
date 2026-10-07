.. _functional-howto:

***********************
HƯỚNG DẪN LẬP TRÌNH HÀM
***********************

:Author: \A. M. Kuchling
:Release: 0.32

Trong tài liệu này, chúng ta sẽ tìm hiểu các tính năng của Python phù hợp để triển khai chương trình theo phong cách lập trình hàm. Sau phần giới thiệu về các khái niệm của lập trình hàm, chúng ta sẽ xem xét những tính năng của ngôn ngữ như
:term:`iterator`\s và :term:`generator`\s, cùng các mô-đun thư viện liên quan như
:mod:`itertools` và :mod:`functools`.


Giới thiệu
==========

Phần này giải thích khái niệm cơ bản của lập trình hàm; nếu bạn chỉ quan tâm đến việc tìm hiểu các tính năng của ngôn ngữ Python, hãy chuyển đến phần tiếp theo về :ref:`functional-howto-iterators`.

Các ngôn ngữ lập trình hỗ trợ phân rã bài toán theo một số cách khác nhau:

* Hầu hết các ngôn ngữ lập trình đều là ngôn ngữ **thủ tục**: chương trình là danh sách các chỉ dẫn cho máy tính biết cần làm gì với dữ liệu đầu vào của chương trình. C, Pascal và thậm chí cả Unix shell đều là các ngôn ngữ thủ tục.

* Trong các ngôn ngữ **khai báo**, bạn viết một đặc tả mô tả bài toán cần giải quyết, còn phần triển khai của ngôn ngữ sẽ xác định cách thực hiện phép tính một cách hiệu quả. SQL là ngôn ngữ khai báo mà bạn có nhiều khả năng đã quen thuộc nhất; một truy vấn SQL mô tả tập dữ liệu bạn muốn truy xuất, còn công cụ SQL quyết định nên quét các bảng hay sử dụng các chỉ mục, mệnh đề con nào nên được thực hiện trước, v.v.

* Các chương trình **hướng đối tượng** thao tác trên các tập hợp đối tượng. Đối tượng có trạng thái nội bộ và hỗ trợ các phương thức truy vấn hoặc sửa đổi trạng thái nội bộ này theo một cách nào đó. Smalltalk và Java là các ngôn ngữ hướng đối tượng. C++ và Python là những ngôn ngữ hỗ trợ lập trình hướng đối tượng, nhưng không bắt buộc phải sử dụng các tính năng hướng đối tượng.

* Lập trình **hàm** phân rã bài toán thành một tập hợp các hàm. Lý tưởng nhất, các hàm chỉ nhận đầu vào và tạo ra đầu ra, đồng thời không có trạng thái nội bộ nào ảnh hưởng đến đầu ra được tạo ra với một đầu vào nhất định. Các ngôn ngữ hàm nổi tiếng bao gồm họ ML (Standard ML, OCaml và các biến thể khác) và Haskell.

Các nhà thiết kế một số ngôn ngữ máy tính chọn nhấn mạnh một cách tiếp cận cụ thể đối với việc lập trình. Điều này thường khiến việc viết các chương trình sử dụng một cách tiếp cận khác trở nên khó khăn. Những ngôn ngữ khác là ngôn ngữ đa mô hình, hỗ trợ một số cách tiếp cận khác nhau. Lisp, C++ và Python là các ngôn ngữ đa mô hình; trong tất cả những ngôn ngữ này, bạn có thể viết các chương trình hoặc thư viện chủ yếu mang tính thủ tục, hướng đối tượng hoặc hàm. Trong một chương trình lớn, các phần khác nhau có thể được viết bằng những cách tiếp cận khác nhau; chẳng hạn, GUI có thể mang tính hướng đối tượng, trong khi logic xử lý mang tính thủ tục hoặc hàm.

Trong một chương trình hàm, dữ liệu đầu vào chảy qua một tập hợp các hàm. Mỗi hàm xử lý đầu vào của mình và tạo ra một số đầu ra. Phong cách hàm không khuyến khích các hàm có side effect làm thay đổi trạng thái nội bộ hoặc tạo ra những thay đổi khác không thể hiện trong giá trị trả về của hàm. Các hàm hoàn toàn không có side effect được gọi là **hàm thuần**. Việc tránh side effect đồng nghĩa với việc không sử dụng các cấu trúc dữ liệu được cập nhật trong quá trình chương trình chạy; đầu ra của mỗi hàm chỉ được phụ thuộc vào đầu vào của nó.

Một số ngôn ngữ rất nghiêm ngặt về tính thuần khiết và thậm chí không có các câu lệnh gán như ``a=3`` hoặc ``c = a + b``, nhưng rất khó tránh mọi side effect, chẳng hạn như in ra màn hình hoặc ghi vào tệp trên đĩa. Một ví dụ khác là lời gọi đến hàm :func:`print` hoặc :func:`time.sleep`, cả hai đều không trả về giá trị hữu ích. Chúng chỉ được gọi vì side effect là gửi một đoạn văn bản nào đó lên màn hình hoặc tạm dừng thực thi trong một giây.

Các chương trình Python được viết theo phong cách functional thường không đi đến mức cực đoan là tránh mọi thao tác I/O hoặc mọi phép gán; thay vào đó, chúng cung cấp một interface có vẻ mang tính functional nhưng sử dụng các tính năng phi functional ở bên trong. Ví dụ, phần triển khai của một hàm vẫn sử dụng phép gán cho các biến cục bộ, nhưng không sửa đổi các biến toàn cục hoặc tạo ra side effect khác.

Lập trình functional có thể được xem là đối lập với lập trình hướng đối tượng. Các object là những capsule nhỏ chứa một số trạng thái nội bộ cùng với một tập hợp các lời gọi method cho phép bạn sửa đổi trạng thái này, và chương trình bao gồm việc thực hiện đúng tập hợp các thay đổi trạng thái. Lập trình functional muốn tránh thay đổi trạng thái nhiều nhất có thể và làm việc với dữ liệu truyền qua các hàm. Trong Python, bạn có thể kết hợp hai cách tiếp cận này bằng cách viết các hàm nhận vào và trả về các instance đại diện cho những object trong ứng dụng của bạn (thư điện tử, giao dịch, v.v.).

Thiết kế functional có thể giống như một ràng buộc kỳ lạ phải tuân theo. Tại sao bạn nên tránh object và side effect? Phong cách functional có những ưu điểm cả về lý thuyết lẫn thực tiễn:

* Khả năng chứng minh hình thức.
* Tính module hóa.
* Khả năng kết hợp.
* Dễ gỡ lỗi và kiểm thử.


Khả năng chứng minh hình thức
-----------------------------

Một lợi ích mang tính lý thuyết là việc xây dựng một chứng minh toán học cho thấy một chương trình functional là đúng sẽ dễ dàng hơn.

Từ lâu, các nhà nghiên cứu đã quan tâm đến việc tìm ra những cách chứng minh tính đúng đắn của chương trình bằng toán học. Điều này khác với việc kiểm thử một chương trình trên vô số đầu vào rồi kết luận rằng đầu ra của nó thường đúng, hoặc đọc mã nguồn của chương trình rồi kết luận rằng mã có vẻ đúng; thay vào đó, mục tiêu là một chứng minh chặt chẽ rằng chương trình tạo ra kết quả đúng với mọi đầu vào có thể.

Kỹ thuật được dùng để chứng minh tính đúng đắn của chương trình là ghi ra **bất biến**, tức các thuộc tính của dữ liệu đầu vào và các biến của chương trình luôn đúng. Với mỗi dòng mã, bạn sẽ chứng minh rằng nếu các bất biến X và Y đúng **trước khi** thực thi dòng đó, thì các bất biến X' và Y' hơi khác sẽ đúng **sau khi** thực thi dòng đó. Quá trình này tiếp tục cho đến khi bạn đến cuối chương trình; tại thời điểm đó, các bất biến phải khớp với những điều kiện mong muốn đối với đầu ra của chương trình.

Việc tránh phép gán trong functional programming bắt nguồn từ việc các phép gán khó xử lý bằng kỹ thuật này; phép gán có thể phá vỡ các bất biến vốn đúng trước khi gán mà không tạo ra bất kỳ bất biến mới nào để tiếp tục truyền đi.

Đáng tiếc là việc chứng minh tính đúng đắn của chương trình phần lớn không thực tế và không liên quan đến phần mềm Python. Ngay cả những chương trình đơn giản cũng cần các chứng minh dài vài trang; chứng minh tính đúng đắn của một chương trình phức tạp vừa phải sẽ rất đồ sộ, và hầu như không có chương trình nào bạn sử dụng hằng ngày (trình thông dịch Python, bộ phân tích cú pháp XML, trình duyệt web) có thể được chứng minh là đúng. Ngay cả khi bạn tự viết hoặc tạo ra một chứng minh, khi đó vẫn còn câu hỏi về việc xác minh chứng minh ấy; có thể nó chứa lỗi và bạn đã lầm tưởng rằng mình chứng minh được tính đúng đắn của chương trình.


Tính mô-đun
-----------

Một lợi ích thiết thực hơn của lập trình hàm là nó buộc bạn phải chia nhỏ vấn đề thành những phần nhỏ. Nhờ đó, các chương trình có tính mô-đun cao hơn. Việc xác định và viết một hàm nhỏ chỉ thực hiện một việc sẽ dễ hơn so với một hàm lớn thực hiện một phép biến đổi phức tạp. Các hàm nhỏ cũng dễ đọc và kiểm tra lỗi hơn.


Dễ gỡ lỗi và kiểm thử
---------------------

Việc kiểm thử và gỡ lỗi một chương trình theo phong cách hàm sẽ dễ dàng hơn.

Việc gỡ lỗi được đơn giản hóa vì các hàm thường nhỏ và được đặc tả rõ ràng. Khi chương trình không hoạt động, mỗi hàm là một điểm giao diện để bạn kiểm tra xem dữ liệu có chính xác hay không. Bạn có thể xem các đầu vào và đầu ra trung gian để nhanh chóng xác định hàm gây ra lỗi.

Việc kiểm thử dễ dàng hơn vì mỗi hàm đều có thể là đối tượng của một unit test. Các hàm không phụ thuộc vào trạng thái hệ thống cần được tái tạo trước khi chạy kiểm thử; thay vào đó, bạn chỉ cần tạo đúng đầu vào rồi kiểm tra xem đầu ra có khớp với kết quả mong đợi hay không.


Khả năng kết hợp
----------------

Khi xây dựng một chương trình theo phong cách hàm, bạn sẽ viết nhiều hàm với các đầu vào và đầu ra khác nhau. Một số hàm trong đó chắc chắn sẽ được chuyên biệt cho một ứng dụng cụ thể, nhưng những hàm khác sẽ hữu ích trong nhiều loại chương trình. Ví dụ, một hàm nhận đường dẫn thư mục và trả về tất cả các tệp XML trong thư mục, hoặc một hàm nhận tên tệp và trả về nội dung của tệp đó, có thể được áp dụng trong nhiều tình huống khác nhau.

Theo thời gian, bạn sẽ hình thành một thư viện tiện ích của riêng mình. Thông thường, bạn sẽ tạo các chương trình mới bằng cách sắp xếp những hàm hiện có theo một cấu hình mới và viết thêm một vài hàm được chuyên biệt cho tác vụ hiện tại.


.. _functional-howto-iterators:

Iterator
========

Tôi sẽ bắt đầu bằng cách xem xét một tính năng của ngôn ngữ Python, nền tảng quan trọng để viết các chương trình theo phong cách hàm: iterator.

Iterator là một đối tượng biểu diễn một luồng dữ liệu; đối tượng này trả về dữ liệu từng phần tử một. Một iterator trong Python phải hỗ trợ một phương thức có tên là
:meth:`~iterator.__next__` không nhận đối số nào và luôn trả về phần tử tiếp theo của luồng. Nếu không còn phần tử nào trong luồng,
:meth:`~iterator.__next__` phải raise exception :exc:`StopIteration`. Tuy nhiên, iterator không nhất thiết phải hữu hạn; việc viết một iterator tạo ra một luồng dữ liệu vô hạn là hoàn toàn hợp lý.

Hàm :func:`iter` tích hợp sẵn nhận một đối tượng bất kỳ và cố gắng trả về một iterator sẽ trả về nội dung hoặc các phần tử của đối tượng đó, đồng thời phát sinh
:exc:`TypeError` nếu đối tượng không hỗ trợ iteration. Một số kiểu dữ liệu tích hợp sẵn của Python hỗ trợ iteration, phổ biến nhất là list và dictionary. Một đối tượng được gọi là :term:`iterable` nếu bạn có thể lấy iterator cho đối tượng đó.

Bạn có thể tự thực nghiệm với interface iteration:

    >>> L = [1, 2, 3]
    >>> it = iter(L)
    >>> it  #doctest: +ELLIPSIS
    <...iterator object at ...>
    >>> it.__next__()  # giống như next(it)
    1
    >>> next(it)
    2
    >>> next(it)
    3
    >>> next(it)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration
    >>>

Python yêu cầu các đối tượng iterable trong một số ngữ cảnh khác nhau, quan trọng nhất là câu lệnh :keyword:`for`. Trong câu lệnh ``for X in Y``, Y phải là một iterator hoặc một đối tượng mà :func:`iter` có thể tạo iterator cho nó. Hai câu lệnh này tương đương::


    for i in iter(obj):
        print(i)

    for i in obj:
        print(i)

Iterator có thể được chuyển thành list hoặc tuple bằng cách sử dụng :func:`list` hoặc
:func:`tuple` các hàm khởi tạo:

    >>> L = [1, 2, 3]
    >>> iterator = iter(L)
    >>> t = tuple(iterator)
    >>> t
    (1, 2, 3)

Phép unpacking chuỗi cũng hỗ trợ iterator: nếu biết một iterator sẽ trả về N phần tử, bạn có thể unpack chúng vào một tuple gồm N phần tử:

    >>> L = [1, 2, 3]
    >>> iterator = iter(L)
    >>> a, b, c = iterator
    >>> a, b, c
    (1, 2, 3)

Các hàm tích hợp như :func:`max` và :func:`min` có thể nhận một iterator duy nhất và sẽ trả về phần tử lớn nhất hoặc nhỏ nhất. Các toán tử ``"in"`` và ``"not in"`` cũng hỗ trợ iterator: ``X in iterator`` là true nếu tìm thấy X trong luồng do iterator trả về. Bạn sẽ gặp các vấn đề rõ ràng nếu iterator là vô hạn; :func:`max`, :func:`min` sẽ không bao giờ trả về, và nếu phần tử X không bao giờ xuất hiện trong luồng, các toán tử ``"in"`` và ``"not in"`` cũng sẽ không trả về.

Lưu ý rằng bạn chỉ có thể tiến về phía trước trong một iterator; không có cách nào lấy phần tử trước đó, đặt lại iterator hoặc tạo một bản sao của nó. Các đối tượng iterator có thể tùy chọn cung cấp những khả năng bổ sung này, nhưng iterator protocol chỉ quy định phương thức :meth:`~iterator.__next__`. Do đó, các hàm có thể tiêu thụ toàn bộ đầu ra của iterator, và nếu cần thực hiện việc khác với cùng luồng đó, bạn sẽ phải tạo một iterator mới.



Các kiểu dữ liệu hỗ trợ iterator
--------------------------------

Chúng ta đã thấy list và tuple hỗ trợ iterator như thế nào. Trên thực tế, bất kỳ kiểu sequence nào của Python, chẳng hạn như string, cũng sẽ tự động hỗ trợ việc tạo iterator.

Gọi :func:`iter` trên một dictionary sẽ trả về một iterator lặp qua các key của dictionary::

    >>> m = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    ...      'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    >>> for key in m:
    ...     print(key, m[key])
    Jan 1
    Feb 2
    Mar 3
    Apr 4
    May 5
    Jun 6
    Jul 7
    Aug 8
    Sep 9
    Oct 10
    Nov 11
    Dec 12

Lưu ý rằng начиная từ Python 3.7, thứ tự lặp qua dictionary được đảm bảo giống với thứ tự chèn. Ở các phiên bản trước, hành vi này không được xác định và có thể khác nhau giữa các implementation.

Áp dụng :func:`iter` cho một dictionary luôn lặp qua các key, nhưng dictionary có các method trả về những iterator khác. Nếu muốn lặp qua các value hoặc các cặp key/value, bạn có thể gọi rõ ràng các
method :meth:`~dict.values` hoặc :meth:`~dict.items` để lấy iterator thích hợp.

Constructor :func:`dict` có thể nhận một iterator trả về một luồng hữu hạn gồm các tuple ``(key, value)``:

    >>> L = [('Italy', 'Rome'), ('France', 'Paris'), ('US', 'Washington DC')]
    >>> dict(iter(L))
    {'Italy': 'Rome', 'France': 'Paris', 'US': 'Washington DC'}

File cũng hỗ trợ việc lặp bằng cách gọi method :meth:`~io.TextIOBase.readline` cho đến khi không còn dòng nào trong file. Điều này có nghĩa là bạn có thể đọc từng dòng của file như sau::

    for line in file:
        # thực hiện thao tác cho từng dòng
        ...

Set có thể lấy nội dung từ một iterable và cho phép bạn lặp qua các phần tử của set::

    >>> S = {2, 3, 5, 7, 11, 13}
    >>> for i in S:
    ...     print(i)
    2
    3
    5
    7
    11
    13



Biểu thức generator và list comprehension
=========================================

Hai thao tác phổ biến trên đầu ra của một iterator là 1) thực hiện một thao tác nào đó với mọi phần tử, 2) chọn một tập hợp con các phần tử đáp ứng một điều kiện nào đó. Ví dụ, với một danh sách chuỗi, bạn có thể muốn loại bỏ khoảng trắng ở cuối mỗi dòng hoặc trích xuất tất cả các chuỗi chứa một chuỗi con nhất định.

List comprehension và biểu thức generator (viết tắt: "listcomps" và "genexps") là ký hiệu ngắn gọn cho các thao tác như vậy, được mượn từ ngôn ngữ lập trình hàm Haskell (https://www.haskell.org/).  Bạn có thể loại bỏ toàn bộ khoảng trắng khỏi một luồng chuỗi bằng đoạn mã sau::

    >>> line_list = ['  line 1\n', 'line 2  \n', ' \n', '']

    >>> # Biểu thức generator -- trả về iterator
    >>> stripped_iter = (line.strip() for line in line_list)

    >>> # List comprehension -- trả về list
    >>> stripped_list = [line.strip() for line in line_list]

Bạn có thể chỉ chọn một số phần tử nhất định bằng cách thêm điều kiện ``"if"``::

    >>> stripped_list = [line.strip() for line in line_list
    ...                  if line != ""]

Với list comprehension, bạn nhận được một Python list; ``stripped_list`` là một list chứa các dòng kết quả, không phải một iterator. Biểu thức generator trả về một iterator tính toán các giá trị khi cần, không cần tạo ra tất cả giá trị cùng lúc. Điều này có nghĩa là list comprehension không hữu ích nếu bạn đang làm việc với các iterator trả về một luồng vô hạn hoặc một lượng dữ liệu rất lớn. Trong những tình huống này, nên dùng biểu thức generator.

Biểu thức generator được bao quanh bởi dấu ngoặc đơn ("()"), còn list comprehension được bao quanh bởi dấu ngoặc vuông ("[]"). Biểu thức generator có dạng::

    ( expression for expr in sequence1
                 if condition1
                 for expr2 in sequence2
                 if condition2
                 for expr3 in sequence3
                 ...
                 if condition3
                 for exprN in sequenceN
                 if conditionN )

Một lần nữa, đối với list comprehension, chỉ có các dấu ngoặc bên ngoài là khác nhau (dấu ngoặc vuông thay vì dấu ngoặc đơn).

Các phần tử của kết quả được tạo ra sẽ là các giá trị liên tiếp của ``expression``. Các mệnh đề ``if`` đều là tùy chọn; nếu có, ``expression`` chỉ được đánh giá và thêm vào kết quả khi ``condition`` là true.

Biểu thức generator luôn phải được viết bên trong dấu ngoặc đơn, nhưng dấu ngoặc biểu thị một lệnh gọi hàm cũng được tính. Nếu bạn muốn tạo một iterator sẽ được truyền ngay cho một hàm, bạn có thể viết::

    obj_total = sum(obj.count for obj in list_all_objects())

Các mệnh đề ``for...in`` chứa những sequence cần được lặp qua. Các sequence không cần có cùng độ dài, vì chúng được lặp từ trái sang phải, **not** song song. Với mỗi phần tử trong ``sequence1``, ``sequence2`` được lặp lại từ đầu. Sau đó, ``sequence3`` được lặp qua cho từng cặp phần tử tạo ra từ ``sequence1`` và ``sequence2``.

Nói cách khác, list comprehension hoặc biểu thức generator tương đương với đoạn mã Python sau::

    for expr1 in sequence1:
        if not (condition1):
            continue   # Bỏ qua phần tử này
        for expr2 in sequence2:
            if not (condition2):
                continue   # Bỏ qua phần tử này
            ...
            for exprN in sequenceN:
                if not (conditionN):
                    continue   # Bỏ qua phần tử này

                # Xuất giá trị của
                # biểu thức.

Điều này có nghĩa là khi có nhiều mệnh đề ``for...in`` nhưng không có mệnh đề ``if``, độ dài của đầu ra thu được sẽ bằng tích độ dài của tất cả các dãy. Nếu bạn có hai danh sách có độ dài là 3, danh sách đầu ra sẽ có 9 phần tử:

    >>> seq1 = 'abc'
    >>> seq2 = (1, 2, 3)
    >>> [(x, y) for x in seq1 for y in seq2]  #doctest: +NORMALIZE_WHITESPACE
    [('a', 1), ('a', 2), ('a', 3),
     ('b', 1), ('b', 2), ('b', 3),
     ('c', 1), ('c', 2), ('c', 3)]

Để tránh tạo ra sự mơ hồ trong ngữ pháp của Python, nếu ``expression`` đang tạo một tuple, nó phải được đặt trong dấu ngoặc đơn. Phép list comprehension đầu tiên bên dưới là một lỗi cú pháp, còn phép thứ hai thì đúng::

    # Lỗi cú pháp
    [x, y for x in seq1 for y in seq2]
    # Đúng
    [(x, y) for x in seq1 for y in seq2]


Generator
=========

Generator là một lớp hàm đặc biệt giúp đơn giản hóa việc viết iterator. Các hàm thông thường tính toán một giá trị rồi trả về giá trị đó, còn generator trả về một iterator tạo ra một luồng giá trị.

Chắc hẳn bạn đã quen với cách các lời gọi hàm thông thường hoạt động trong Python hoặc C. Khi bạn gọi một hàm, hàm đó nhận được một namespace riêng, nơi các biến cục bộ của nó được tạo ra. Khi hàm thực thi đến câu lệnh ``return``, các biến cục bộ bị hủy và giá trị được trả về cho bên gọi. Một lần gọi sau đó đến cùng hàm sẽ tạo một namespace riêng mới cùng một tập biến cục bộ mới. Nhưng điều gì sẽ xảy ra nếu các biến cục bộ không bị loại bỏ khi thoát khỏi hàm? Nếu sau đó bạn có thể tiếp tục hàm từ nơi nó đã dừng thì sao? Đây chính là điều generator cung cấp; có thể xem chúng như các hàm có thể tiếp tục thực thi.

Sau đây là ví dụ đơn giản nhất về một hàm generator:

    >>> def generate_ints(N):
    ...    for i in range(N):
    ...        yield i

Mọi hàm chứa từ khóa :keyword:`yield` đều là một hàm generator; trình biên dịch :term:`bytecode` của Python sẽ phát hiện điều này và biên dịch hàm theo cách đặc biệt.

Khi bạn gọi một hàm generator, hàm đó không trả về một giá trị duy nhất; thay vào đó, nó trả về một đối tượng generator hỗ trợ iterator protocol. Khi thực thi biểu thức ``yield``, generator xuất ra giá trị của ``i``, tương tự như một câu lệnh ``return``. Điểm khác biệt lớn giữa ``yield`` và một câu lệnh ``return`` là khi gặp ``yield``, trạng thái thực thi của generator sẽ bị tạm dừng và các biến cục bộ được bảo toàn. Ở lần gọi tiếp theo đến phương thức :meth:`~generator.__next__` của generator, hàm sẽ tiếp tục thực thi.

Dưới đây là một ví dụ sử dụng generator ``generate_ints()``:

    >>> gen = generate_ints(3)
    >>> gen  #doctest: +ELLIPSIS
    <generator object generate_ints at ...>
    >>> next(gen)
    0
    >>> next(gen)
    1
    >>> next(gen)
    2
    >>> next(gen)
    Traceback (most recent call last):
      File "stdin", line 1, in <module>
      File "stdin", line 2, in generate_ints
    StopIteration

Bạn cũng có thể viết ``for i in generate_ints(5)``, hoặc ``a, b, c = generate_ints(3)``.

Bên trong một hàm generator, ``return value`` khiến ``StopIteration(value)`` được phát sinh từ phương thức :meth:`~generator.__next__`. Khi điều này xảy ra hoặc khi đã đến cuối hàm, quá trình phát ra các giá trị kết thúc và generator không thể tạo thêm giá trị nào nữa.

Bạn có thể tự thực hiện hiệu ứng của generator bằng cách viết lớp riêng và lưu tất cả các biến cục bộ của generator dưới dạng biến thể hiện. Ví dụ, để trả về một danh sách các số nguyên, bạn có thể đặt ``self.count`` thành 0, rồi cho phương thức :meth:`~iterator.__next__` tăng ``self.count`` lên và trả về nó. Tuy nhiên, với một generator phức tạp vừa phải, việc viết lớp tương ứng có thể rắc rối hơn nhiều.

Bộ kiểm thử đi kèm với thư viện của Python,
:source:`Lib/test/test_generators.py`, chứa một số ví dụ thú vị hơn. Đây là một generator triển khai việc duyệt cây theo thứ tự trung tố bằng cách sử dụng các generator đệ quy.::

    # Generator đệ quy tạo ra các lá của Tree theo thứ tự trung tố.
    def inorder(t):
        if t:
            for x in inorder(t.left):
                yield x

            yield t.label

            for x in inorder(t.right):
                yield x

Hai ví dụ khác trong ``test_generators.py`` tạo ra lời giải cho bài toán N-Queens (đặt N quân hậu trên bàn cờ NxN sao cho không quân hậu nào đe dọa quân hậu khác) và Knight's Tour (tìm một lộ trình đưa một quân mã đi qua mọi ô của bàn cờ NxN mà không đi qua bất kỳ ô nào hai lần).



Truyền giá trị vào một generator
--------------------------------

Trong Python 2.4 và các phiên bản trước đó, generator chỉ tạo ra đầu ra. Khi mã của một generator được gọi để tạo một iterator, không có cách nào truyền thông tin mới vào hàm khi quá trình thực thi của nó được tiếp tục. Bạn có thể tạm tạo khả năng này bằng cách để generator đọc một biến toàn cục hoặc truyền vào một đối tượng mutable mà sau đó caller sẽ sửa đổi, nhưng những cách tiếp cận này khá rắc rối.

Trong Python 2.5, có một cách đơn giản để truyền giá trị vào một generator.
:keyword:`yield` trở thành một expression, trả về một giá trị có thể được gán cho một biến hoặc được xử lý theo cách khác::

    val = (yield i)

Tôi khuyên bạn **luôn** đặt dấu ngoặc đơn quanh một ``yield`` biểu thức khi bạn thực hiện thao tác với giá trị được trả về, như trong ví dụ trên. Dấu ngoặc đơn không phải lúc nào cũng cần thiết, nhưng luôn thêm chúng sẽ dễ hơn so với việc phải nhớ khi nào chúng cần thiết.

(:pep:`342` giải thích các quy tắc chính xác: một biểu thức ``yield`` luôn phải được đặt trong dấu ngoặc đơn, trừ khi nó xuất hiện ở cấp cao nhất của biểu thức bên phải phép gán. Điều này có nghĩa là bạn có thể viết ``val = yield i``, nhưng phải dùng dấu ngoặc đơn khi có phép toán, như trong ``val = (yield i)
+ 12``.)

Các giá trị được truyền vào generator bằng cách gọi phương thức :meth:`send(value) <generator.send>` của nó. Phương thức này tiếp tục thực thi mã của generator và biểu thức ``yield`` trả về giá trị được chỉ định. Nếu phương thức thông thường
:meth:`~generator.__next__` được gọi, ``yield`` trả về ``None``.

Sau đây là một bộ đếm đơn giản tăng thêm 1 và cho phép thay đổi giá trị của bộ đếm nội bộ.

.. testcode::

    def counter(maximum):
        i = 0
        while i < maximum:
            val = (yield i)
            # Nếu có giá trị được cung cấp, thay đổi bộ đếm
            if val is not None:
                i = val
            else:
                i += 1

Và đây là một ví dụ về việc thay đổi bộ đếm:

    >>> it = counter(10)  #doctest: +SKIP
    >>> next(it)  #doctest: +SKIP
    0
    >>> next(it)  #doctest: +SKIP
    1
    >>> it.send(8)  #doctest: +SKIP
    8
    >>> next(it)  #doctest: +SKIP
    9
    >>> next(it)  #doctest: +SKIP
    Traceback (most recent call last):
      File "t.py", line 15, in <module>
        it.next()
    StopIteration

Vì ``yield`` thường sẽ trả về ``None``, bạn luôn nên kiểm tra trường hợp này. Đừng chỉ sử dụng giá trị của nó trong các biểu thức trừ khi bạn chắc chắn rằng
Phương thức :meth:`~generator.send` sẽ là phương thức duy nhất được sử dụng để tiếp tục hàm generator của bạn.

Ngoài :meth:`~generator.send`, generator còn có hai phương thức khác:

* :meth:`throw(value) <generator.throw>` được dùng để raise một exception bên trong generator; exception được raise bởi biểu thức ``yield`` tại nơi quá trình thực thi của generator đang tạm dừng.

* :meth:`~generator.close` gửi một exception :exc:`GeneratorExit` đến generator để kết thúc việc lặp. Khi nhận exception này, mã của generator phải raise :exc:`GeneratorExit` hoặc
  :exc:`StopIteration`; việc bắt exception rồi thực hiện bất kỳ điều gì khác là không hợp lệ và sẽ kích hoạt một :exc:`RuntimeError`. :meth:`~generator.close` cũng sẽ được Python garbage collector gọi khi generator được garbage-collect.

  Nếu cần chạy mã cleanup khi xảy ra :exc:`GeneratorExit`, tôi khuyên bạn nên dùng một suite ``try: ... finally:`` thay vì bắt :exc:`GeneratorExit`.

Tác động tổng thể của những thay đổi này là biến generator từ các bộ tạo thông tin một chiều thành cả bộ tạo lẫn bộ tiếp nhận thông tin.

Generators cũng trở thành **coroutines**, một dạng tổng quát hơn của subroutine. Subroutine được bắt đầu tại một điểm và kết thúc tại một điểm khác (ở đầu hàm và một câu lệnh ``return``), nhưng coroutine có thể được bắt đầu, kết thúc và tiếp tục lại tại nhiều điểm khác nhau (các câu lệnh ``yield``).


Các hàm dựng sẵn
================

Hãy xem chi tiết hơn về các hàm dựng sẵn thường được sử dụng với iterator.

Hai hàm dựng sẵn của Python, :func:`map` và :func:`filter`, có các tính năng trùng với generator expression:

:func:`map(f, iterA, iterB, ...) <map>` trả về một iterator trên sequence
 ``f(iterA[0], iterB[0]), f(iterA[1], iterB[1]), f(iterA[2], iterB[2]), ...``.

    >>> def upper(s):
    ...     return s.upper()

    >>> list(map(upper, ['sentence', 'fragment']))
    ['SENTENCE', 'FRAGMENT']
    >>> [upper(s) for s in ['sentence', 'fragment']]
    ['SENTENCE', 'FRAGMENT']

Tất nhiên, bạn cũng có thể đạt được hiệu ứng tương tự bằng list comprehension.

:func:`filter(predicate, iter) <filter>` trả về một iterator trên tất cả các phần tử của sequence thỏa mãn một điều kiện nhất định và cũng tương tự như list comprehension. Một **predicate** là một hàm trả về giá trị đúng/sai của một điều kiện nào đó; khi sử dụng với :func:`filter`, predicate phải nhận một giá trị duy nhất.

    >>> def is_even(x):
    ...     return (x % 2) == 0

    >>> list(filter(is_even, range(10)))
    [0, 2, 4, 6, 8]


Điều này cũng có thể được viết dưới dạng list comprehension:

    >>> list(x for x in range(10) if is_even(x))
    [0, 2, 4, 6, 8]


:func:`enumerate(iter, start=0) <enumerate>` duyệt qua các phần tử trong iterable và trả về các tuple 2 phần tử chứa số đếm (bắt đầu từ *start*) và từng phần tử.::

    >>> for item in enumerate(['subject', 'verb', 'object']):
    ...     print(item)
    (0, 'subject')
    (1, 'verb')
    (2, 'object')

:func:`enumerate` thường được sử dụng khi lặp qua một danh sách và ghi lại các chỉ mục tại đó một số điều kiện nhất định được thỏa mãn::

    f = open('data.txt', 'r')
    for i, line in enumerate(f):
        if line.strip() == '':
            print('Blank line at line #%i' % i)

:func:`sorted(iterable, key=None, reverse=False) <sorted>` tập hợp tất cả phần tử của iterable vào một danh sách, sắp xếp danh sách rồi trả về kết quả đã sắp xếp. Các đối số *key* và *reverse* được truyền cho phương thức :meth:`~list.sort` của danh sách được tạo.::

    >>> import random
    >>> # Tạo 8 số ngẫu nhiên trong khoảng [0, 10000)
    >>> rand_list = random.sample(range(10000), 8)
    >>> rand_list  #doctest: +SKIP
    [769, 7953, 9828, 6431, 8442, 9878, 6213, 2207]
    >>> sorted(rand_list)  #doctest: +SKIP
    [769, 2207, 6213, 6431, 7953, 8442, 9828, 9878]
    >>> sorted(rand_list, reverse=True)  #doctest: +SKIP
    [9878, 9828, 8442, 7953, 6431, 6213, 2207, 769]

(Để xem phần giải thích chi tiết hơn về việc sắp xếp, hãy xem :ref:`sortinghowto`.)


Các built-in :func:`any(iter) <any>` và :func:`all(iter) <all>` kiểm tra các giá trị đúng của nội dung trong một iterable. :func:`any` trả về ``True`` nếu bất kỳ phần tử nào trong iterable là giá trị đúng, còn :func:`all` trả về ``True`` nếu tất cả các phần tử đều là giá trị đúng:

    >>> any([0, 1, 0])
    True
    >>> any([0, 0, 0])
    False
    >>> any([1, 1, 1])
    True
    >>> all([0, 1, 0])
    False
    >>> all([0, 0, 0])
    False
    >>> all([1, 1, 1])
    True


:func:`zip(iterA, iterB, ...) <zip>` lấy một phần tử từ mỗi iterable và trả về các phần tử đó trong một tuple::

    zip(['a', 'b', 'c'], (1, 2, 3)) =>
      ('a', 1), ('b', 2), ('c', 3)

Nó không tạo một list trong bộ nhớ rồi :term:`tiêu thụ <exhausted>` tất cả các iterator đầu vào trước khi trả về; thay vào đó, các tuple chỉ được tạo và trả về khi chúng được yêu cầu. (Thuật ngữ kỹ thuật cho hành vi này là `lazy evaluation <https://en.wikipedia.org/wiki/Lazy_evaluation>`__.)

Iterator này được thiết kế để sử dụng với các iterable có cùng độ dài. Nếu các iterable có độ dài khác nhau, stream kết quả sẽ có độ dài bằng iterable ngắn nhất.::

    zip(['a', 'b'], (1, 2, 3)) =>
      ('a', 1), ('b', 2)

Tuy nhiên, bạn nên tránh làm vậy, vì một phần tử có thể được lấy từ các iterator dài hơn rồi bị loại bỏ. Điều này có nghĩa là bạn không thể tiếp tục sử dụng các iterator đó, vì có nguy cơ bỏ qua một phần tử đã bị loại bỏ.


Mô-đun itertools
================

Mô-đun :mod:`itertools` chứa một số iterator thường dùng cũng như các hàm để kết hợp nhiều iterator. Phần này sẽ giới thiệu nội dung của mô-đun bằng cách trình bày các ví dụ nhỏ.

Các hàm của mô-đun được chia thành một vài nhóm lớn:

* Các hàm tạo một iterator mới dựa trên một iterator hiện có.
* Các hàm dùng để xử lý các phần tử của iterator như các đối số hàm.
* Các hàm dùng để chọn một phần đầu ra của iterator.
* Một hàm dùng để nhóm đầu ra của iterator.

Tạo iterator mới
----------------

:func:`itertools.count(start, step) <itertools.count>` trả về một luồng vô hạn gồm các giá trị cách đều nhau. Bạn có thể tùy chọn cung cấp số bắt đầu, mặc định là 0, và khoảng cách giữa các số, mặc định là 1::

    itertools.count() =>
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...
    itertools.count(10) =>
      10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ...
    itertools.count(10, 5) =>
      10, 15, 20, 25, 30, 35, 40, 45, 50, 55, ...

:func:`itertools.cycle(iter) <itertools.cycle>` lưu một bản sao nội dung của iterable được cung cấp và trả về một iterator mới, lần lượt trả về các phần tử từ đầu đến cuối. Iterator mới sẽ lặp lại vô hạn các phần tử này.::

    itertools.cycle([1, 2, 3, 4, 5]) =>
      1, 2, 3, 4, 5, 1, 2, 3, 4, 5, ...

:func:`itertools.repeat(elem, [n]) <itertools.repeat>` trả về phần tử được cung cấp *n* lần, hoặc trả về phần tử liên tục nếu không cung cấp *n*.::

    itertools.repeat('abc') =>
      abc, abc, abc, abc, abc, abc, abc, abc, abc, abc, ...
    itertools.repeat('abc', 5) =>
      abc, abc, abc, abc, abc

:func:`itertools.chain(iterA, iterB, ...) <itertools.chain>` nhận một số lượng iterable tùy ý làm đầu vào và trả về tất cả phần tử của iterator đầu tiên, sau đó là tất cả phần tử của iterator thứ hai, cứ tiếp tục như vậy cho đến khi tất cả iterable đã được :term:`exhausted`.::

    itertools.chain(['a', 'b', 'c'], (1, 2, 3)) =>
      a, b, c, 1, 2, 3

:func:`itertools.islice(iter, [start], stop, [step]) <itertools.islice>` trả về một luồng là một lát cắt của iterator. Với một đối số *stop* duy nhất, hàm sẽ trả về *stop* phần tử đầu tiên. Nếu cung cấp chỉ mục bắt đầu, bạn sẽ nhận được *stop-start* phần tử; nếu cung cấp giá trị cho *step*, các phần tử sẽ được bỏ qua tương ứng. Không giống như việc cắt chuỗi và list trong Python, bạn không thể sử dụng giá trị âm cho *start*, *stop* hoặc *step*.::

    itertools.islice(range(10), 8) =>
      0, 1, 2, 3, 4, 5, 6, 7
    itertools.islice(range(10), 2, 8) =>
      2, 3, 4, 5, 6, 7
    itertools.islice(range(10), 2, 8, 2) =>
      2, 4, 6

:func:`itertools.tee(iter, [n]) <itertools.tee>` nhân bản một iterator; hàm trả về *n* iterator độc lập, tất cả đều trả về nội dung của iterator nguồn. Nếu không cung cấp giá trị cho *n*, giá trị mặc định là 2. Việc nhân bản iterator yêu cầu lưu một phần nội dung của iterator nguồn, vì vậy có thể tiêu tốn đáng kể bộ nhớ nếu iterator lớn và một trong các iterator mới được dùng nhiều hơn những iterator còn lại.::

        itertools.tee( itertools.count() ) =>
           iterA, iterB

        where iterA ->
           0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...

        and   iterB ->
           0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...


Gọi các hàm trên các phần tử
----------------------------

Mô-đun :mod:`operator` chứa một tập hợp các hàm tương ứng với các toán tử của Python. Một số ví dụ là :func:`operator.add(a, b) <operator.add>` (cộng hai giá trị), :func:`operator.ne(a, b)  <operator.ne>` (giống với ``a != b``), và
:func:`operator.attrgetter('id') <operator.attrgetter>` (trả về một callable dùng để lấy thuộc tính ``.id``).

:func:`itertools.starmap(func, iter) <itertools.starmap>` giả định rằng iterable sẽ trả về một luồng các tuple và gọi *func* bằng cách sử dụng các tuple này làm đối số::

    itertools.starmap(os.path.join,
                      [('/bin', 'python'), ('/usr', 'bin', 'java'),
                       ('/usr', 'bin', 'perl'), ('/usr', 'bin', 'ruby')])
    =>
      /bin/python, /usr/bin/java, /usr/bin/perl, /usr/bin/ruby


Chọn các phần tử
----------------

Một nhóm hàm khác chọn một tập con các phần tử của iterator dựa trên một predicate.

:func:`itertools.filterfalse(predicate, iter) <itertools.filterfalse>` là ngược lại với :func:`filter`, trả về tất cả các phần tử mà predicate trả về false::

    itertools.filterfalse(is_even, itertools.count()) =>
      1, 3, 5, 7, 9, 11, 13, 15, ...

:func:`itertools.takewhile(predicate, iter) <itertools.takewhile>` trả về các phần tử chừng nào predicate còn trả về true. Khi predicate trả về false, iterator sẽ báo hiệu rằng các kết quả đã kết thúc.::

    def less_than_10(x):
        return x < 10

    itertools.takewhile(less_than_10, itertools.count()) =>
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9

    itertools.takewhile(is_even, itertools.count()) =>
      0

:func:`itertools.dropwhile(predicate, iter) <itertools.dropwhile>` loại bỏ các phần tử trong khi predicate trả về true, sau đó trả về phần còn lại của các kết quả trong iterable.::

    itertools.dropwhile(less_than_10, itertools.count()) =>
      10, 11, 12, 13, 14, 15, 16, 17, 18, 19, ...

    itertools.dropwhile(is_even, itertools.count()) =>
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...

:func:`itertools.compress(data, selectors) <itertools.compress>` nhận hai iterator và chỉ trả về những phần tử của *data* mà phần tử tương ứng của *selectors* là true, dừng lại ngay khi một trong hai :term:`exhausted`::

    itertools.compress([1, 2, 3, 4, 5], [True, True, False, False, True]) =>
       1, 2, 5


Các hàm tổ hợp
--------------

:func:`itertools.combinations(iterable, r) <itertools.combinations>` trả về một iterator cung cấp mọi tổ hợp tuple có thể có gồm *r* phần tử chứa trong *iterable*.::

    itertools.combinations([1, 2, 3, 4, 5], 2) =>
      (1, 2), (1, 3), (1, 4), (1, 5),
      (2, 3), (2, 4), (2, 5),
      (3, 4), (3, 5),
      (4, 5)

    itertools.combinations([1, 2, 3, 4, 5], 3) =>
      (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5),
      (2, 3, 4), (2, 3, 5), (2, 4, 5),
      (3, 4, 5)

Các phần tử trong mỗi tuple vẫn giữ nguyên thứ tự như khi *iterable* trả về chúng. Ví dụ, số 1 luôn đứng trước 2, 3, 4 hoặc 5 trong các ví dụ trên. Một hàm tương tự,
:func:`itertools.permutations(iterable, r=None) <itertools.permutations>`, loại bỏ ràng buộc về thứ tự này và trả về mọi cách sắp xếp có thể có với độ dài *r*::

    itertools.permutations([1, 2, 3, 4, 5], 2) =>
      (1, 2), (1, 3), (1, 4), (1, 5),
      (2, 1), (2, 3), (2, 4), (2, 5),
      (3, 1), (3, 2), (3, 4), (3, 5),
      (4, 1), (4, 2), (4, 3), (4, 5),
      (5, 1), (5, 2), (5, 3), (5, 4)

    itertools.permutations([1, 2, 3, 4, 5]) =>
      (1, 2, 3, 4, 5), (1, 2, 3, 5, 4), (1, 2, 4, 3, 5),
      ...
      (5, 4, 3, 2, 1)

Nếu bạn không cung cấp giá trị cho *r*, độ dài của iterable sẽ được sử dụng, nghĩa là tất cả các phần tử đều được hoán vị.

Lưu ý rằng các hàm này tạo ra mọi tổ hợp khả dĩ theo vị trí và không yêu cầu nội dung của *iterable* phải là duy nhất::

    itertools.permutations('aba', 3) =>
      ('a', 'b', 'a'), ('a', 'a', 'b'), ('b', 'a', 'a'),
      ('b', 'a', 'a'), ('a', 'a', 'b'), ('a', 'b', 'a')

Tuple giống hệt nhau ``('a', 'a', 'b')`` xuất hiện hai lần, nhưng hai chuỗi 'a' đến từ các vị trí khác nhau.

Hàm :func:`itertools.combinations_with_replacement(iterable, r) <itertools.combinations_with_replacement>` nới lỏng một ràng buộc khác: các phần tử có thể được lặp lại trong cùng một tuple. Về mặt khái niệm, một phần tử được chọn cho vị trí đầu tiên của mỗi tuple, sau đó được thay thế trước khi phần tử thứ hai được chọn.::

    itertools.combinations_with_replacement([1, 2, 3, 4, 5], 2) =>
      (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
      (2, 2), (2, 3), (2, 4), (2, 5),
      (3, 3), (3, 4), (3, 5),
      (4, 4), (4, 5),
      (5, 5)


Nhóm các phần tử
----------------

Hàm cuối cùng tôi sẽ thảo luận, :func:`itertools.groupby(iter, key_func=None) <itertools.groupby>`, là hàm phức tạp nhất. ``key_func(elem)`` là một hàm có thể tính một giá trị key cho mỗi phần tử do iterable trả về. Nếu bạn không cung cấp hàm key, key đơn giản là chính mỗi phần tử.

:func:`~itertools.groupby` thu thập tất cả các phần tử liên tiếp từ iterable bên dưới có cùng giá trị key, rồi trả về một stream gồm các 2-tuple chứa một giá trị key và một iterator cho các phần tử có key đó.

::

    city_list = [('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL'),
                 ('Anchorage', 'AK'), ('Nome', 'AK'),
                 ('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ'),
                 ...
                ]

    def get_state(city_state):
        return city_state[1]

    itertools.groupby(city_list, get_state) =>
      ('AL', iterator-1),
      ('AK', iterator-2),
      ('AZ', iterator-3), ...

    where
    iterator-1 =>
      ('Decatur', 'AL'), ('Huntsville', 'AL'), ('Selma', 'AL')
    iterator-2 =>
      ('Anchorage', 'AK'), ('Nome', 'AK')
    iterator-3 =>
      ('Flagstaff', 'AZ'), ('Phoenix', 'AZ'), ('Tucson', 'AZ')

:func:`~itertools.groupby` giả định rằng nội dung của iterable nền đã được sắp xếp theo key. Lưu ý rằng các iterator được trả về cũng sử dụng iterable nền, vì vậy bạn phải xử lý hết kết quả của iterator-1 trước khi yêu cầu iterator-2 và key tương ứng của nó.


Mô-đun functools
================

Mô-đun :mod:`functools` chứa một số hàm bậc cao. Một **hàm bậc cao** nhận một hoặc nhiều hàm làm đầu vào và trả về một hàm mới. Công cụ hữu ích nhất trong mô-đun này là
hàm :func:`functools.partial`.

Khi viết chương trình theo phong cách hàm, đôi khi bạn sẽ muốn tạo các biến thể của những hàm hiện có với một số tham số đã được điền sẵn. Hãy xét một hàm Python ``f(a, b, c)``; bạn có thể muốn tạo một hàm mới ``g(b, c)`` tương đương với ``f(1, b, c)``; tức là bạn đang điền một giá trị cho một trong các tham số của ``f()``. Đây được gọi là "áp dụng hàm từng phần".

Hàm khởi tạo của :func:`~functools.partial` nhận các đối số ``(function, arg1, arg2, ..., kwarg1=value1, kwarg2=value2)``. Đối tượng kết quả có thể gọi được, vì vậy bạn chỉ cần gọi nó để gọi ``function`` với các đối số đã được điền sẵn.

Đây là một ví dụ nhỏ nhưng thực tế::

    import functools

    def log(message, subsystem):
        """Write the contents of 'message' to the specified subsystem."""
        print('%s: %s' % (subsystem, message))
        ...

    server_log = functools.partial(log, subsystem='server')
    server_log('Unable to open socket')

:func:`functools.reduce(func, iter, [initial_value]) <functools.reduce>` thực hiện một phép toán lần lượt trên tất cả các phần tử của iterable và vì vậy không thể áp dụng cho các iterable vô hạn. *func* phải là một hàm nhận vào hai phần tử và trả về một giá trị duy nhất. :func:`functools.reduce` lấy hai phần tử đầu tiên A và B do iterator trả về rồi tính ``func(A, B)``. Sau đó, nó yêu cầu phần tử thứ ba, C, tính ``func(func(A, B), C)``, kết hợp kết quả này với phần tử thứ tư được trả về và tiếp tục cho đến khi iterable :term:`exhausted`. Nếu iterable hoàn toàn không trả về giá trị nào, một ngoại lệ :exc:`TypeError` sẽ được đưa ra. Nếu giá trị ban đầu được cung cấp, giá trị đó được dùng làm điểm bắt đầu và ``func(initial_value, A)`` là phép tính đầu tiên.::

    >>> import operator, functools
    >>> functools.reduce(operator.concat, ['A', 'BB', 'C'])
    'ABBC'
    >>> functools.reduce(operator.concat, [])
    Traceback (most recent call last):
      ...
    TypeError: reduce() of empty iterable with no initial value
    >>> functools.reduce(operator.mul, [1, 2, 3], 1)
    6
    >>> functools.reduce(operator.mul, [], 1)
    1

Nếu bạn dùng :func:`operator.add` với :func:`functools.reduce`, bạn sẽ cộng tất cả các phần tử của iterable. Trường hợp này phổ biến đến mức có một hàm dựng sẵn đặc biệt là :func:`sum` để tính giá trị đó:

    >>> import functools, operator
    >>> functools.reduce(operator.add, [1, 2, 3, 4], 0)
    10
    >>> sum([1, 2, 3, 4])
    10
    >>> sum([])
    0

Tuy nhiên, với nhiều trường hợp sử dụng :func:`functools.reduce`, việc chỉ viết vòng lặp :keyword:`for` hiển nhiên sẽ rõ ràng hơn::

   import functools
   # Thay vì:
   product = functools.reduce(operator.mul, [1, 2, 3], 1)

   # Bạn có thể viết:
   product = 1
   for i in [1, 2, 3]:
       product *= i

Một hàm liên quan là :func:`itertools.accumulate(iterable, func=operator.add) <itertools.accumulate>`. Hàm này thực hiện cùng phép tính, nhưng thay vì chỉ trả về kết quả cuối cùng, :func:`~itertools.accumulate` trả về một iterator đồng thời cho ra từng kết quả trung gian::

    itertools.accumulate([1, 2, 3, 4, 5]) =>
      1, 3, 6, 10, 15

    itertools.accumulate([1, 2, 3, 4, 5], operator.mul) =>
      1, 2, 6, 24, 120


Mô-đun operator
---------------

Module :mod:`operator` đã được đề cập trước đó. Module này chứa một tập hợp các hàm tương ứng với các toán tử của Python. Những hàm này thường hữu ích trong code theo phong cách hàm (functional-style) vì giúp bạn không phải viết các hàm tầm thường chỉ thực hiện một phép toán đơn lẻ.

Một số hàm trong module này gồm:

* Các phép toán số học: ``add()``, ``sub()``, ``mul()``, ``floordiv()``, ``abs()``, ...
* Các phép toán logic: ``not_()``, ``truth()``.
* Các phép toán bit: ``and_()``, ``or_()``, ``invert()``.
* Các phép so sánh: ``eq()``, ``ne()``, ``lt()``, ``le()``, ``gt()``, và ``ge()``.
* Định danh đối tượng: ``is_()``, ``is_not()``.

Hãy xem tài liệu của module operator để biết danh sách đầy đủ.


Các hàm nhỏ và biểu thức lambda
===============================

Khi viết các chương trình theo phong cách functional, bạn sẽ thường cần những hàm nhỏ hoạt động như các predicate hoặc kết hợp các phần tử theo một cách nào đó.

Nếu đã có một hàm dựng sẵn của Python hoặc một hàm module phù hợp, bạn không cần tự định nghĩa hàm mới.::

    stripped_lines = [line.strip() for line in lines]
    existing_files = filter(os.path.exists, file_list)

Nếu hàm bạn cần không tồn tại, bạn phải viết nó. Một cách để viết các hàm nhỏ là sử dụng biểu thức :keyword:`lambda`. ``lambda`` nhận một số tham số và một biểu thức kết hợp các tham số đó, rồi tạo ra một hàm anonymous trả về giá trị của biểu thức.::

    adder = lambda x, y: x+y

    print_assign = lambda name, value: name + '=' + str(value)

Một lựa chọn khác là chỉ cần sử dụng câu lệnh ``def`` và định nghĩa hàm theo cách thông thường.::

    def adder(x, y):
        return x + y

    def print_assign(name, value):
        return name + '=' + str(value)

Lựa chọn nào tốt hơn? Đó là vấn đề về phong cách; thông thường tôi tránh sử dụng ``lambda``.

Một lý do khiến tôi thích ``lambda`` là nó khá hạn chế về các hàm mà nó có thể định nghĩa. Kết quả phải có thể được tính bằng một biểu thức duy nhất, nghĩa là bạn không thể có các phép so sánh ``if... elif... else`` nhiều nhánh hoặc các câu lệnh ``try... except``. Nếu cố thực hiện quá nhiều việc trong một câu lệnh ``lambda``, bạn sẽ tạo ra một biểu thức quá phức tạp và khó đọc. Thử trả lời nhanh xem đoạn mã sau đang làm gì?::

    import functools
    total = functools.reduce(lambda a, b: (0, a[1] + b[1]), items)[1]

Bạn có thể tìm ra, nhưng sẽ mất thời gian để tháo gỡ biểu thức và hiểu chuyện gì đang diễn ra. Việc sử dụng các câu lệnh ``def`` lồng nhau ngắn gọn khiến mọi thứ khá hơn một chút::

    import functools
    def combine(a, b):
        return 0, a[1] + b[1]

    total = functools.reduce(combine, items)[1]

Nhưng tốt nhất vẫn là nếu tôi chỉ cần sử dụng một vòng lặp ``for``::

     total = 0
     for a, b in items:
         total += b

Hoặc hàm dựng sẵn :func:`sum` và một generator expression::

     total = sum(b for a, b in items)

Nhiều cách sử dụng :func:`functools.reduce` sẽ rõ ràng hơn khi được viết dưới dạng các vòng lặp ``for``.

Fredrik Lundh từng đề xuất tập hợp quy tắc sau để refactor các cách sử dụng ``lambda``:

1. Viết một hàm lambda.
2. Viết một chú thích giải thích chính xác lambda đó làm gì.
3. Đọc kỹ chú thích một lúc, rồi nghĩ ra một cái tên nắm bắt được nội dung cốt lõi của chú thích.
4. Chuyển lambda thành câu lệnh def, sử dụng tên đó.
5. Xóa chú thích.

Tôi thực sự thích những quy tắc này, nhưng bạn hoàn toàn có thể không đồng ý về việc phong cách không dùng lambda này có tốt hơn hay không.


Lịch sử sửa đổi và lời cảm ơn
=============================

Tác giả xin cảm ơn những người sau đây đã đưa ra các đề xuất, chỉnh sửa và hỗ trợ cho nhiều bản thảo khác nhau của bài viết này: Ian Bicking, Nick Coghlan, Nick Efford, Raymond Hettinger, Jim Jewett, Mike Krell, Leandro Lameiro, Jussi Salmela, Collin Winter, Blake Winton.

Phiên bản 0.1: đăng ngày 30 tháng 6 năm 2006.

Phiên bản 0.11: đăng ngày 1 tháng 7 năm 2006. Sửa lỗi chính tả.

Phiên bản 0.2: đăng ngày 10 tháng 7 năm 2006. Gộp các phần genexp và listcomp thành một phần. Sửa lỗi chính tả.

Phiên bản 0.21: Bổ sung thêm các tài liệu tham khảo được đề xuất trên mailing list của tutor.

Phiên bản 0.30: Bổ sung một phần về module ``functional`` do Collin Winter viết; bổ sung một phần ngắn về module operator; và một số chỉnh sửa khác.


Tài liệu tham khảo
==================

Chung
-----

**Cấu trúc và Diễn giải các Chương trình Máy tính**, của Harold Abelson và Gerald Jay Sussman cùng Julie Sussman. Cuốn sách có thể được tìm thấy tại https://mitpress.mit.edu/sicp.  Trong giáo trình kinh điển về khoa học máy tính này, chương 2 và 3 thảo luận về việc sử dụng các sequence và stream để tổ chức luồng dữ liệu bên trong một chương trình. Cuốn sách sử dụng Scheme cho các ví dụ, nhưng nhiều phương pháp thiết kế được mô tả trong các chương này có thể áp dụng cho mã Python theo phong cách functional.

https://defmacro.org/2006/06/19/fp.html: Một phần giới thiệu tổng quan về lập trình functional, sử dụng các ví dụ Java và có phần giới thiệu lịch sử dài.

https://en.wikipedia.org/wiki/Functional_programming: Mục Wikipedia tổng quan mô tả lập trình functional.

https://en.wikipedia.org/wiki/Coroutine: Mục về coroutine.

https://en.wikipedia.org/wiki/Partial_application: Mục về khái niệm partial function application.

https://en.wikipedia.org/wiki/Currying: Mục về khái niệm currying.

Đặc thù cho Python
------------------

https://gnosis.cx/TPiP/: Chương đầu tiên trong cuốn sách của David Mertz
:title-reference:`Xử lý văn bản trong Python` thảo luận về lập trình hàm trong xử lý văn bản, trong phần có tiêu đề "Sử dụng các hàm bậc cao trong xử lý văn bản".

Mertz cũng viết một loạt bài gồm 3 phần về lập trình hàm cho trang DeveloperWorks của IBM; xem `phần 1 <https://developer.ibm.com/articles/l-prog/>`__, `phần 2 <https://developer.ibm.com/tutorials/l-prog2/>`__ và `phần 3 <https://developer.ibm.com/tutorials/l-prog3/>`__,


Tài liệu Python
---------------

Tài liệu dành cho module :mod:`itertools`.

Tài liệu dành cho module :mod:`functools`.

Tài liệu dành cho module :mod:`operator`.

:pep:`289`: "Biểu thức Generator"

:pep:`342`: "Coroutine thông qua Generator được cải tiến" mô tả các tính năng generator mới trong Python 2.5.

.. comment

    Handy little function for printing part of an iterator -- used
    while writing this document.

    import itertools
    def print_iter(it):
         slice = itertools.islice(it, 10)
         for elem in slice[:-1]:
             sys.stdout.write(str(elem))
             sys.stdout.write(', ')
        print(elem[-1])
