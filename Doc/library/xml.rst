.. _xml:

Các mô-đun xử lý XML
====================

.. module:: xml
   :synopsis: Gói chứa các mô-đun xử lý XML

.. sectionauthor:: Christian Heimes <christian@python.org>
.. sectionauthor:: Georg Brandl <georg@python.org>

**Mã nguồn:** :source:`Lib/xml/`

--------------

Các giao diện của Python để xử lý XML được nhóm trong gói ``xml``.

.. note::

   Nếu bạn cần phân tích cú pháp dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem
   :ref:`xml-security`.

Điều quan trọng cần lưu ý là các mô-đun trong gói :mod:`!xml` yêu cầu phải có ít nhất một trình phân tích cú pháp XML tuân thủ SAX. Trình phân tích cú pháp Expat được tích hợp trong Python, vì vậy mô-đun :mod:`xml.parsers.expat` sẽ luôn khả dụng.

Tài liệu về các gói :mod:`xml.dom` và :mod:`xml.sax` là định nghĩa về các liên kết Python cho các giao diện DOM và SAX.

Các mô-đun con xử lý XML là:

* :mod:`xml.etree.ElementTree`: API ElementTree, một bộ xử lý XML đơn giản và nhẹ

..

* :mod:`xml.dom`: định nghĩa API DOM
* :mod:`xml.dom.minidom`: một triển khai DOM tối giản
* :mod:`xml.dom.pulldom`: hỗ trợ xây dựng các cây DOM từng phần

..

* :mod:`xml.sax`: các lớp cơ sở và hàm tiện ích SAX2
* :mod:`xml.parsers.expat`: binding trình phân tích cú pháp Expat


.. _xml-security:
.. _xml-vulnerabilities:

Bảo mật XML
-----------

Kẻ tấn công có thể lợi dụng các tính năng của XML để thực hiện các cuộc tấn công từ chối dịch vụ, truy cập các tệp cục bộ, tạo kết nối mạng đến các máy khác hoặc vượt qua tường lửa khi XML do kẻ tấn công kiểm soát được phân tích cú pháp, trong Python hoặc ở nơi khác.

Các trình phân tích cú pháp XML tích hợp sẵn của Python dựa vào thư viện `libexpat`_, thường được gọi là Expat, để phân tích cú pháp XML.

Theo mặc định, bản thân Expat không truy cập các tệp cục bộ hoặc tạo kết nối mạng.

Các phiên bản Expat thấp hơn 2.7.2 có thể dễ bị các lỗ hổng "billion laughs", "quadratic blowup" và "large tokens", hoặc sử dụng bộ nhớ động không tương xứng. Python tích hợp một bản sao của Expat, và việc Python sử dụng Expat đi kèm hay Expat trên toàn hệ thống phụ thuộc vào cách trình thông dịch Python
:option:`has been configured <--with-system-expat>` trong môi trường của bạn. Python có thể dễ bị tấn công nếu sử dụng các phiên bản Expat cũ như vậy. Hãy kiểm tra :const:`!pyexpat.EXPAT_VERSION`.

:mod:`xmlrpc` có **dễ bị tấn công** bởi cuộc tấn công "decompression bomb".


mở rộng thực thể theo cấp số nhân / Billion Laughs
  Cuộc tấn công `Billion Laughs <Billion Laughs_>`_ -- còn được gọi là mở rộng thực thể theo cấp số nhân -- sử dụng nhiều cấp thực thể lồng nhau. Mỗi thực thể tham chiếu đến một thực thể khác nhiều lần, còn định nghĩa thực thể cuối cùng chứa một chuỗi ngắn. Kết quả mở rộng theo cấp số nhân tạo ra vài gigabyte văn bản và tiêu tốn rất nhiều bộ nhớ cũng như thời gian CPU.

mở rộng thực thể gây phình to theo cấp số hai
  Cuộc tấn công gây phình to theo cấp số hai tương tự như cuộc tấn công `Billion Laughs <Billion Laughs_>`_; nó cũng lạm dụng việc mở rộng thực thể. Thay vì các thực thể lồng nhau, nó lặp đi lặp lại một thực thể lớn có vài nghìn ký tự. Cuộc tấn công này không hiệu quả bằng trường hợp theo cấp số nhân, nhưng tránh kích hoạt các biện pháp đối phó của parser nhằm ngăn các thực thể lồng nhau quá sâu.

bom giải nén
  Bom giải nén (còn gọi là `ZIP bomb <ZIP bomb_>`_) ảnh hưởng đến mọi thư viện XML có thể phân tích các luồng XML được nén, chẳng hạn như luồng HTTP được gzip hoặc các tệp được nén bằng LZMA. Đối với kẻ tấn công, cách này có thể giảm lượng dữ liệu truyền đi xuống ba bậc độ lớn hoặc hơn.

token lớn
  Expat cần phân tích cú pháp lại các token chưa hoàn tất; nếu không có cơ chế bảo vệ được giới thiệu trong Expat 2.6.0, điều này có thể dẫn đến thời gian chạy bậc hai, từ đó bị lợi dụng để gây ra cuộc tấn công từ chối dịch vụ trong ứng dụng phân tích cú pháp XML. Vấn đề này được gọi là :cve:`2023-52425`.

.. _libexpat: https://github.com/libexpat/libexpat
.. _Billion Laughs: https://en.wikipedia.org/wiki/Billion_laughs
.. _ZIP bomb: https://en.wikipedia.org/wiki/Zip_bomb
