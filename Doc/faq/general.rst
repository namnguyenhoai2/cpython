:tocdepth: 2

============================
Câu hỏi thường gặp về Python
============================

.. only:: html

   .. contents::


Thông tin chung
===============

Python là gì?
-------------

Python là một ngôn ngữ lập trình thông dịch, tương tác và hướng đối tượng. Ngôn ngữ này tích hợp các module, exception, kiểu động, các kiểu dữ liệu động cấp cao và class. Python hỗ trợ nhiều mô hình lập trình ngoài lập trình hướng đối tượng, chẳng hạn như lập trình thủ tục và lập trình hàm. Python kết hợp sức mạnh đáng kể với cú pháp rất rõ ràng. Python có các interface dành cho nhiều lời gọi hệ thống và thư viện, cũng như nhiều hệ thống cửa sổ khác nhau, đồng thời có thể mở rộng bằng C hoặc C++. Python cũng có thể được sử dụng làm ngôn ngữ mở rộng cho các ứng dụng cần một interface có khả năng lập trình. Cuối cùng, Python có tính portable: chạy được trên nhiều biến thể Unix, bao gồm Linux và macOS, cũng như trên Windows.

Để tìm hiểu thêm, hãy bắt đầu với :ref:`tutorial-index`. `Hướng dẫn Python cho người mới bắt đầu <https://wiki.python.org/moin/BeginnersGuide>`_ liên kết đến các tutorial nhập môn và tài nguyên khác để học Python.


Python Software Foundation là gì?
---------------------------------

Python Software Foundation là một tổ chức độc lập, phi lợi nhuận, nắm giữ bản quyền đối với các phiên bản Python 2.1 trở lên. Sứ mệnh của PSF là thúc đẩy công nghệ nguồn mở liên quan đến ngôn ngữ lập trình Python và quảng bá việc sử dụng Python. Trang chủ của PSF nằm tại https://www.python.org/psf/.

Các khoản quyên góp cho PSF được miễn thuế tại Hoa Kỳ. Nếu bạn sử dụng Python và thấy Python hữu ích, vui lòng đóng góp thông qua `trang quyên góp cho PSF <https://www.python.org/psf/donations/>`_.


Việc sử dụng Python có bị hạn chế bởi bản quyền không?
------------------------------------------------------

Bạn có thể làm bất cứ điều gì mình muốn với mã nguồn, miễn là giữ nguyên thông tin bản quyền và hiển thị những thông tin bản quyền đó trong mọi tài liệu về Python mà bạn tạo ra. Nếu tuân thủ các quy định về bản quyền, bạn có thể sử dụng Python cho mục đích thương mại, bán các bản sao Python ở dạng mã nguồn hoặc mã nhị phân (đã sửa đổi hoặc chưa sửa đổi), hoặc bán các sản phẩm tích hợp Python dưới bất kỳ hình thức nào. Tất nhiên, chúng tôi vẫn muốn biết về mọi hoạt động sử dụng Python cho mục đích thương mại.

Xem `trang giấy phép <https://docs.python.org/3/license.html>`_ để biết thêm giải thích và toàn văn Giấy phép PSF.

Logo Python là nhãn hiệu đã được đăng ký, và trong một số trường hợp, bạn cần được cấp phép để sử dụng logo này. Hãy tham khảo `Chính sách Sử dụng Nhãn hiệu <https://www.python.org/psf/trademarks/>`__ để biết thêm thông tin.


Tại sao Python được tạo ra ngay từ đầu?
---------------------------------------

Dưới đây là bản tóm tắt *rất* ngắn gọn về nguồn gốc của mọi chuyện, do Guido van Rossum viết:

   Tôi đã có nhiều kinh nghiệm trong việc triển khai một ngôn ngữ thông dịch trong nhóm ABC tại CWI, và qua quá trình làm việc với nhóm này, tôi đã học được rất nhiều về thiết kế ngôn ngữ. Đây là nguồn gốc của nhiều tính năng Python, bao gồm việc sử dụng thụt lề để nhóm các câu lệnh và việc đưa vào các kiểu dữ liệu cấp rất cao (mặc dù các chi tiết trong Python đều khác).

   Tôi có một số điều không hài lòng về ngôn ngữ ABC, nhưng cũng thích nhiều tính năng của nó. Không thể mở rộng ngôn ngữ ABC (hoặc phần triển khai của nó) để khắc phục những vấn đề tôi phàn nàn — trên thực tế, việc thiếu khả năng mở rộng là một trong những vấn đề lớn nhất của nó. Tôi từng có một chút kinh nghiệm sử dụng Modula-2+ và đã trao đổi với các nhà thiết kế Modula-3, cũng như đọc tài liệu về Modula-3. Modula-3 là nguồn gốc của cú pháp và ngữ nghĩa được sử dụng cho các exception, cùng một số tính năng Python khác.

   Tôi đang làm việc trong nhóm phát triển hệ điều hành phân tán Amoeba tại CWI. Chúng tôi cần một cách tốt hơn để thực hiện việc quản trị hệ thống thay vì viết các chương trình C hoặc Bourne shell script, vì Amoeba có giao diện system call riêng mà Bourne shell không dễ truy cập. Kinh nghiệm xử lý lỗi trong Amoeba khiến tôi nhận thức sâu sắc về tầm quan trọng của exception như một tính năng của ngôn ngữ lập trình.

   Tôi chợt nhận ra rằng một ngôn ngữ scripting có cú pháp giống ABC nhưng có thể truy cập các system call của Amoeba sẽ đáp ứng được nhu cầu này. Tôi hiểu rằng việc viết một ngôn ngữ dành riêng cho Amoeba sẽ là điều không khôn ngoan, nên quyết định rằng mình cần một ngôn ngữ có khả năng mở rộng một cách tổng quát.

   Trong kỳ nghỉ Giáng sinh năm 1989, tôi có rất nhiều thời gian rảnh, nên quyết định thử thực hiện việc đó. Trong năm tiếp theo, dù phần lớn vẫn làm dự án trong thời gian riêng, Python đã được sử dụng trong dự án Amoeba với mức độ thành công ngày càng cao, và phản hồi từ các đồng nghiệp đã giúp tôi bổ sung nhiều cải tiến ban đầu.

   Vào tháng 2 năm 1991, sau hơn một năm phát triển một chút, tôi quyết định đăng bài lên USENET. Phần còn lại nằm trong tệp ``Misc/HISTORY``.


Python phù hợp để làm gì?
-------------------------

Python là một ngôn ngữ lập trình đa mục đích cấp cao, có thể được áp dụng cho nhiều lớp bài toán khác nhau.

Ngôn ngữ này đi kèm một thư viện chuẩn lớn, bao quát các lĩnh vực như xử lý chuỗi (biểu thức chính quy, Unicode, tính toán khác biệt giữa các tệp), giao thức Internet (HTTP, FTP, SMTP, XML-RPC, POP, IMAP), công nghệ phần mềm (kiểm thử đơn vị, ghi nhật ký, profiling, phân tích cú pháp mã Python) và giao diện hệ điều hành (lệnh gọi hệ thống, hệ thống tệp, socket TCP/IP). Hãy xem mục lục của :ref:`library-index` để hình dung những gì hiện có. Ngoài ra, có rất nhiều phần mở rộng của bên thứ ba. Hãy tham khảo `the Python Package Index <https://pypi.org>`_ để tìm các package phù hợp với nhu cầu của bạn.


.. _faq-version-numbering-scheme:

Cơ chế đánh số phiên bản Python hoạt động như thế nào?
------------------------------------------------------

Các phiên bản Python được đánh số theo dạng "A.B.C" hoặc "A.B":

* *A* là số phiên bản chính -- chỉ được tăng khi ngôn ngữ có những thay đổi thực sự lớn.
* *B* là số phiên bản phụ -- được tăng khi có những thay đổi ít lớn hơn.
* *C* là số phiên bản vi mô -- được tăng sau mỗi bản phát hành sửa lỗi.

Không phải mọi bản phát hành đều là bản sửa lỗi. Trong giai đoạn chuẩn bị cho một bản phát hành tính năng mới, một loạt bản phát hành phát triển sẽ được thực hiện, được gọi là alpha, beta hoặc release candidate. Các bản alpha là những bản phát hành sớm, trong đó các interface vẫn chưa được hoàn thiện; việc interface thay đổi giữa hai bản phát hành alpha là điều không bất ngờ. Các bản beta ổn định hơn, giữ nguyên các interface hiện có nhưng có thể bổ sung các module mới, còn các release candidate đã được đóng băng, không thay đổi trừ khi cần sửa các lỗi nghiêm trọng.

Các phiên bản alpha, beta và release candidate có thêm một hậu tố:

* Hậu tố của phiên bản alpha là "aN", trong đó N là một số nhỏ *N*.
* Hậu tố của phiên bản beta là "bN", trong đó N là một số nhỏ *N*.
* Hậu tố của phiên bản release candidate là "rcN", trong đó N là một số nhỏ *N*.

Nói cách khác, tất cả các phiên bản được gắn nhãn *2.0aN* đều đứng trước các phiên bản được gắn nhãn *2.0bN*, vốn đứng trước các phiên bản được gắn nhãn *2.0rcN*, và *những phiên bản đó* đứng trước 2.0.

Bạn cũng có thể bắt gặp các số phiên bản có hậu tố "+", chẳng hạn như "2.2+". Đây là các phiên bản chưa phát hành, được xây dựng trực tiếp từ repository phát triển CPython. Trên thực tế, sau khi một bản phát hành minor cuối cùng được thực hiện, phiên bản sẽ được tăng lên thành phiên bản minor tiếp theo, phiên bản này trở thành phiên bản "a0", chẳng hạn như "2.4a0".

Xem `Hướng dẫn dành cho nhà phát triển <https://devguide.python.org/developer-workflow/development-cycle/>`__ để biết thêm thông tin về chu kỳ phát triển, và
:pep:`387` để tìm hiểu thêm về chính sách tương thích ngược của Python.  Xem thêm tài liệu về :data:`sys.version`, :data:`sys.hexversion`, và
:data:`sys.version_info`.


Làm thế nào để lấy một bản sao mã nguồn Python?
-----------------------------------------------

Bản phân phối mã nguồn Python mới nhất luôn có sẵn trên python.org, tại https://www.python.org/downloads/.  Mã nguồn phát triển mới nhất có thể lấy tại https://github.com/python/cpython/.

Bản phân phối mã nguồn là một tệp tar nén gzip chứa đầy đủ mã nguồn C, tài liệu được định dạng bằng Sphinx, các mô-đun thư viện Python, các chương trình ví dụ và một số phần mềm hữu ích được phép phân phối tự do.  Mã nguồn sẽ biên dịch và chạy ngay trên hầu hết các nền tảng UNIX.

Tham khảo `phần Bắt đầu trong Hướng dẫn dành cho nhà phát triển Python <https://devguide.python.org/setup/>`__ để biết thêm thông tin về cách lấy mã nguồn và biên dịch mã nguồn.


Làm thế nào để lấy tài liệu về Python?
--------------------------------------

Tài liệu chuẩn cho phiên bản ổn định hiện tại của Python có tại https://docs.python.org/3/.  Các phiên bản EPUB, văn bản thuần túy và HTML có thể tải xuống cũng có tại https://docs.python.org/3/download.html.

Tài liệu được viết bằng reStructuredText và được xử lý bởi `công cụ tài liệu Sphinx <https://www.sphinx-doc.org/>`__.  Mã nguồn reStructuredText của tài liệu là một phần của bản phân phối mã nguồn Python.


Tôi chưa từng lập trình. Có hướng dẫn Python nào không?
-------------------------------------------------------

Có rất nhiều hướng dẫn và sách.  Tài liệu chuẩn bao gồm :ref:`tutorial-index`.

Hãy tham khảo `Hướng dẫn cho người mới bắt đầu <https://wiki.python.org/moin/BeginnersGuide>`_ để tìm thông tin dành cho những người mới học Python, bao gồm danh sách các hướng dẫn.


Có newsgroup hoặc mailing list nào dành riêng cho Python không?
---------------------------------------------------------------

Có một newsgroup là :newsgroup:`comp.lang.python` và một mailing list là `python-list <https://mail.python.org/mailman/listinfo/python-list>`_.  Newsgroup và mailing list được kết nối với nhau -- nếu bạn có thể đọc tin tức thì không cần đăng ký mailing list.
:newsgroup:`comp.lang.python` có lưu lượng truy cập cao, nhận được hàng trăm bài đăng mỗi ngày, và người đọc Usenet thường có khả năng xử lý khối lượng này tốt hơn.

Thông báo về các bản phát hành phần mềm và sự kiện mới có thể được tìm thấy trên comp.lang.python.announce, một danh sách được kiểm duyệt có lưu lượng thấp, nhận khoảng năm bài đăng mỗi ngày. Danh sách này có tại `the python-announce mailing list <https://mail.python.org/mailman3/lists/python-announce-list.python.org/>`_.

Bạn có thể tìm thêm thông tin về các mailing list và newsgroup khác tại https://www.python.org/community/lists/.


Làm thế nào để tôi có được bản beta của Python?
-----------------------------------------------

Các bản phát hành alpha và beta có tại https://www.python.org/downloads/.  Mọi bản phát hành đều được thông báo trên các newsgroup comp.lang.python và comp.lang.python.announce cũng như trên trang chủ Python tại https://www.python.org/; và có một RSS feed cung cấp tin tức.

Bạn cũng có thể truy cập phiên bản đang được phát triển của Python thông qua Git. Xem `The Python Developer's Guide <https://devguide.python.org/>`_ để biết thêm chi tiết.


Làm thế nào để tôi gửi báo cáo lỗi và bản vá cho Python?
--------------------------------------------------------

Để báo cáo lỗi hoặc gửi bản vá, hãy sử dụng hệ thống theo dõi issue tại https://github.com/python/cpython/issues.

Để biết thêm thông tin về cách Python được phát triển, hãy tham khảo `Python Developer's Guide <https://devguide.python.org/>`_.


Có bài viết nào đã xuất bản về Python mà tôi có thể trích dẫn không?
--------------------------------------------------------------------

Có lẽ tốt nhất là trích dẫn cuốn sách yêu thích của bạn về Python.

`Bài viết đầu tiên <https://ir.cwi.nl/pub/18204>`_ về Python được viết vào năm 1991 và hiện đã khá lỗi thời.

    Guido van Rossum và Jelke de Boer, "Interactively Testing Remote Servers Using the Python Programming Language", CWI Quarterly, Tập 4, Số 4 (tháng 12 năm 1991), Amsterdam, trang 283--303.


Có sách nào về Python không?
----------------------------

Có, có rất nhiều sách, và ngày càng có thêm sách được xuất bản. Xem wiki của python.org tại https://wiki.python.org/moin/PythonBooks để biết danh sách.

Bạn cũng có thể tìm kiếm trên các hiệu sách trực tuyến với từ khóa "Python" rồi lọc bỏ các kết quả liên quan đến Monty Python; hoặc có thể tìm kiếm với từ khóa "Python" và "language".


www.python.org nằm ở đâu trên thế giới?
---------------------------------------

Cơ sở hạ tầng của dự án Python nằm ở khắp nơi trên thế giới và được Python Infrastructure Team quản lý. Xem chi tiết `tại đây <https://infra.psf.io>`__.


Tại sao nó được gọi là Python?
------------------------------

Khi bắt đầu triển khai Python, Guido van Rossum cũng đang đọc các kịch bản đã xuất bản của `"Monty Python's Flying Circus" <https://en.wikipedia.org/wiki/Monty_Python>`__, một loạt chương trình hài của BBC từ những năm 1970. Van Rossum nghĩ rằng mình cần một cái tên ngắn gọn, độc đáo và hơi bí ẩn, nên ông quyết định gọi ngôn ngữ này là Python.


Tôi có phải thích "Monty Python's Flying Circus" không?
-------------------------------------------------------

Không, nhưng thích thì sẽ giúp ích.  :)


Python trong thực tế
====================

Python ổn định đến mức nào?
---------------------------

Rất ổn định. Các bản phát hành mới, ổn định đã được phát hành khoảng 6 đến 18 tháng một lần kể từ năm 1991, và nhiều khả năng điều này sẽ tiếp tục. Kể từ phiên bản 3.9, Python sẽ có một bản phát hành tính năng mới mỗi 12 tháng (:pep:`602`).

Các nhà phát triển phát hành các bản sửa lỗi cho những phiên bản cũ, vì vậy độ ổn định của các bản phát hành hiện có dần được cải thiện. Các bản phát hành sửa lỗi, được biểu thị bằng thành phần thứ ba của số phiên bản (ví dụ: 3.5.3, 3.6.2), được quản lý để đảm bảo tính ổn định; chỉ các bản sửa lỗi cho những vấn đề đã biết mới được đưa vào bản phát hành sửa lỗi, và các giao diện được đảm bảo sẽ không thay đổi trong suốt một chuỗi các bản phát hành sửa lỗi.

Các bản phát hành ổn định mới nhất luôn có trên `trang tải xuống Python <https://www.python.org/downloads/>`_. Python 3.x là phiên bản được khuyến nghị và được hầu hết các thư viện được sử dụng rộng rãi hỗ trợ. Python 2.x :pep:`is not maintained anymore <373>`.

Có bao nhiêu người đang sử dụng Python?
---------------------------------------

Có lẽ có hàng triệu người dùng, mặc dù rất khó xác định con số chính xác.

Python được cung cấp để tải xuống miễn phí, vì vậy không có số liệu bán hàng; hơn nữa, Python có sẵn trên nhiều trang web khác nhau và được đóng gói cùng với nhiều bản phân phối Linux, nên số liệu tải xuống cũng không phản ánh đầy đủ.

Nhóm tin comp.lang.python rất sôi nổi, nhưng không phải tất cả người dùng Python đều đăng bài trong nhóm hoặc thậm chí đọc nhóm.


Có dự án quan trọng nào được thực hiện bằng Python không?
---------------------------------------------------------

Xem https://www.python.org/about/success để biết danh sách các dự án sử dụng Python. Tham khảo kỷ yếu của `các hội nghị Python trước đây <https://www.python.org/community/workshops/>`_ sẽ cho thấy những đóng góp từ nhiều công ty và tổ chức khác nhau.

Các dự án Python nổi bật bao gồm `trình quản lý danh sách thư Mailman <https://www.list.org>`_ và `máy chủ ứng dụng Zope <https://www.zope.dev>`_. Một số bản phân phối Linux, nổi bật nhất là `Red Hat <https://www.redhat.com>`_, đã viết một phần hoặc toàn bộ phần mềm cài đặt và quản trị hệ thống bằng Python. Các công ty sử dụng Python nội bộ bao gồm Google, Yahoo và Lucasfilm Ltd.


Những phát triển mới nào được dự kiến cho Python trong tương lai?
-----------------------------------------------------------------

Xem https://peps.python.org/ để biết về Python Enhancement Proposals (PEPs). PEP là các tài liệu thiết kế mô tả một tính năng mới được đề xuất cho Python, cung cấp đặc tả kỹ thuật súc tích và cơ sở lý do. Hãy tìm PEP có tiêu đề "Python X.Y Release Schedule", trong đó X.Y là một phiên bản chưa được phát hành công khai.

Các phát triển mới được thảo luận trên `danh sách thư python-dev <https://mail.python.org/mailman3/lists/python-dev.python.org/>`_.


Có hợp lý khi đề xuất các thay đổi không tương thích với Python không?
----------------------------------------------------------------------

Nhìn chung là không. Hiện đã có hàng triệu dòng mã Python trên khắp thế giới, vì vậy mọi thay đổi trong ngôn ngữ làm cho hơn một phần rất nhỏ các chương trình hiện có không còn hợp lệ đều phải bị phản đối. Ngay cả khi bạn có thể cung cấp một chương trình chuyển đổi, vẫn còn vấn đề cập nhật toàn bộ tài liệu; nhiều cuốn sách đã được viết về Python, và chúng ta không muốn làm cho tất cả chúng trở nên lỗi thời chỉ sau một lần thay đổi.

Cần cung cấp một lộ trình nâng cấp dần nếu một tính năng phải được thay đổi.
:pep:`5` mô tả quy trình được tuân theo để đưa vào các thay đổi không tương thích ngược, đồng thời giảm thiểu gián đoạn cho người dùng.


Python có phải là một ngôn ngữ tốt cho những người mới bắt đầu lập trình không?
-------------------------------------------------------------------------------

Có.

Việc bắt đầu cho sinh viên học một ngôn ngữ thủ tục và kiểu tĩnh như Pascal, C hoặc một tập con của C++ hay Java vẫn còn phổ biến. Sinh viên có thể được phục vụ tốt hơn nếu học Python làm ngôn ngữ đầu tiên. Python có cú pháp rất đơn giản và nhất quán cùng một thư viện chuẩn lớn; quan trọng nhất là việc sử dụng Python trong khóa học lập trình nhập môn cho phép sinh viên tập trung vào những kỹ năng lập trình quan trọng như phân rã bài toán và thiết kế kiểu dữ liệu. Với Python, sinh viên có thể nhanh chóng được làm quen với các khái niệm cơ bản như vòng lặp và thủ tục. Thậm chí ngay trong khóa học đầu tiên, họ có thể đã làm việc với các đối tượng do người dùng định nghĩa.

Đối với một sinh viên chưa từng lập trình, việc sử dụng một ngôn ngữ kiểu tĩnh có vẻ không tự nhiên. Nó tạo thêm sự phức tạp mà sinh viên phải nắm vững và làm chậm tiến độ của khóa học. Sinh viên đang cố gắng học cách tư duy như máy tính, phân rã bài toán, thiết kế các interface nhất quán và đóng gói dữ liệu. Mặc dù việc học cách sử dụng một ngôn ngữ kiểu tĩnh rất quan trọng về lâu dài, đây không nhất thiết là chủ đề tốt nhất để đề cập trong khóa học lập trình đầu tiên của sinh viên.

Nhiều khía cạnh khác của Python khiến đây trở thành một ngôn ngữ đầu tiên tốt. Giống như Java, Python có một thư viện chuẩn lớn, nhờ đó sinh viên có thể được giao các dự án lập trình ngay từ đầu khóa học để *thực hiện* một việc gì đó. Bài tập không bị giới hạn ở chương trình máy tính bốn phép tính cơ bản và chương trình kiểm tra cân bằng dấu ngoặc. Bằng cách sử dụng thư viện chuẩn, sinh viên có thể cảm nhận được sự hài lòng khi làm việc với các ứng dụng thực tế trong lúc học những kiến thức nền tảng về lập trình. Việc sử dụng thư viện chuẩn cũng dạy sinh viên về tái sử dụng code. Các module bên thứ ba như PyGame cũng hữu ích trong việc mở rộng khả năng của sinh viên.

Trình thông dịch tương tác của Python cho phép sinh viên kiểm thử các tính năng của ngôn ngữ trong khi lập trình. Họ có thể giữ một cửa sổ chạy trình thông dịch trong lúc nhập mã nguồn của chương trình vào một cửa sổ khác. Nếu không nhớ các phương thức của một list, họ có thể làm như sau::

   >>> L = []
   >>> dir(L) # doctest: +NORMALIZE_WHITESPACE
   ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__',
   '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
   '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__',
   '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__',
   '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
   '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__',
   '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear',
   'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove',
   'reverse', 'sort']
   >>> [d for d in dir(L) if '__' not in d]
   ['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']

   >>> help(L.append)
   Help on built-in function append:
   <BLANKLINE>
   append(...)
       L.append(object) -> None -- append object to end
   <BLANKLINE>
   >>> L.append(1)
   >>> L
   [1]

Với trình thông dịch, tài liệu luôn ở ngay bên cạnh sinh viên trong khi họ lập trình.

Python cũng có những IDE tốt. IDLE là một IDE đa nền tảng dành cho Python, được viết bằng Python bằng cách sử dụng Tkinter. Người dùng Emacs sẽ hài lòng khi biết rằng Emacs có một Python mode rất tốt. Tất cả các môi trường lập trình này đều cung cấp tính năng tô sáng cú pháp, tự động thụt lề và truy cập trình thông dịch tương tác trong khi viết mã. Hãy tham khảo `wiki Python <https://wiki.python.org/moin/PythonEditors>`_ để xem danh sách đầy đủ các môi trường chỉnh sửa Python.

Nếu bạn muốn thảo luận về việc sử dụng Python trong giáo dục, bạn có thể quan tâm đến việc tham gia `danh sách thư edu-sig <https://www.python.org/community/sigs/current/edu-sig>`_.

.. _`Beginner's Guide to Python`: https://wiki.python.org/moin/BeginnersGuide
.. _`the PSF donation page`: https://www.python.org/psf/donations/
.. _`the license page`: https://docs.python.org/3/license.html
.. _`the Python Package Index`: https://pypi.org
.. _`the Beginner's Guide`: https://wiki.python.org/moin/BeginnersGuide
.. _`python-list`: https://mail.python.org/mailman/listinfo/python-list
.. _`the python-announce mailing list`: https://mail.python.org/mailman3/lists/python-announce-list.python.org/
.. _`the Python Developer's Guide`: https://devguide.python.org/
.. _`very first article`: https://ir.cwi.nl/pub/18204
.. _`Python download page`: https://www.python.org/downloads/
.. _`past Python conferences`: https://www.python.org/community/workshops/
.. _`the Mailman mailing list manager`: https://www.list.org
.. _`the Zope application server`: https://www.zope.dev
.. _`Red Hat`: https://www.redhat.com
.. _`the python-dev mailing list`: https://mail.python.org/mailman3/lists/python-dev.python.org/
.. _`the Python wiki`: https://wiki.python.org/moin/PythonEditors
.. _`the edu-sig mailing list`: https://www.python.org/community/sigs/current/edu-sig
