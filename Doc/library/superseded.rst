.. _superseded:

***************************
Các mô-đun đã được thay thế
***************************

Các mô-đun được mô tả trong chương này đã được thay thế bằng các mô-đun khác cho hầu hết trường hợp sử dụng và được giữ lại chủ yếu để duy trì khả năng tương thích ngược.

Các mô-đun có thể xuất hiện trong chương này vì chúng chỉ giải quyết một tập hợp con giới hạn của một vấn đề, trong khi một giải pháp có phạm vi áp dụng tổng quát hơn đã có ở nơi khác trong thư viện chuẩn (ví dụ: :mod:`getopt` bao quát tác vụ rất cụ thể là "mô phỏng API :c:func:`!getopt` của C trong Python", thay vì các khả năng phân tích tùy chọn dòng lệnh và phân tích đối số rộng hơn do
:mod:`optparse` và :mod:`argparse` cung cấp).

Ngoài ra, các mô-đun có thể xuất hiện trong chương này vì chúng đã hoàn toàn bị phản đối và đang chờ bị loại bỏ trong một bản phát hành tương lai, hoặc chúng là
:term:`soft deprecated` và việc sử dụng chúng hoàn toàn không được khuyến khích trong các dự án mới. Với việc loại bỏ nhiều mô-đun lỗi thời thông qua :pep:`594`, hiện không có mô-đun nào thuộc nhóm sau.

.. toctree::
   :maxdepth: 1

   getopt.rst
