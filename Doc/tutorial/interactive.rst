.. _tut-interacting:

****************************************************
Chỉnh sửa đầu vào tương tác và thay thế lịch sử lệnh
****************************************************

Một số phiên bản trình thông dịch Python hỗ trợ chỉnh sửa dòng đầu vào hiện tại và thay thế lịch sử lệnh, tương tự các tính năng có trong shell Korn và shell GNU Bash. Tính năng này được triển khai bằng thư viện `GNU Readline <GNU Readline_>`_, hỗ trợ nhiều kiểu chỉnh sửa khác nhau. Thư viện này có tài liệu riêng mà chúng tôi sẽ không sao chép tại đây.


.. _tut-keybindings:

Hoàn tất bằng phím Tab và chỉnh sửa lịch sử
===========================================

Việc hoàn tất tên biến và mô-đun được
:ref:`tự động bật <rlcompleter-config>` khi trình thông dịch khởi động để phím :kbd:`Tab` gọi hàm hoàn tất; hàm này xem xét tên các câu lệnh Python, các biến cục bộ hiện tại và tên các mô-đun khả dụng. Đối với các biểu thức có dấu chấm như ``string.a``, hàm sẽ đánh giá biểu thức cho đến ``'.'`` cuối cùng, sau đó đề xuất các nội dung hoàn tất từ các thuộc tính của đối tượng nhận được. Lưu ý rằng việc này có thể thực thi mã do ứng dụng định nghĩa nếu một đối tượng có phương thức :meth:`~object.__getattr__` nằm trong biểu thức. Cấu hình mặc định cũng lưu lịch sử của bạn vào một tệp có tên :file:`.python_history` trong thư mục người dùng. Lịch sử sẽ lại khả dụng trong phiên trình thông dịch tương tác tiếp theo.


.. _tut-commentary:

Các lựa chọn thay thế cho trình thông dịch tương tác
====================================================

Tính năng này là một bước tiến rất lớn so với các phiên bản trình thông dịch trước đây; tuy nhiên, vẫn còn một số mong muốn chưa được đáp ứng: Sẽ rất hữu ích nếu thụt lề phù hợp được đề xuất trên các dòng tiếp nối (trình phân tích cú pháp biết liệu một
:data:`~token.INDENT` token là bắt buộc tiếp theo). Cơ chế hoàn tất có thể sử dụng bảng ký hiệu của trình thông dịch. Một lệnh để kiểm tra (hoặc thậm chí gợi ý) các cặp dấu ngoặc, dấu nháy tương ứng, v.v. cũng sẽ rất hữu ích.

Một trình thông dịch tương tác nâng cao khác đã tồn tại từ khá lâu là IPython_, cung cấp tính năng tự động hoàn tất bằng phím Tab, khám phá đối tượng và quản lý lịch sử nâng cao. Nó cũng có thể được tùy chỉnh toàn diện và nhúng vào các ứng dụng khác. Một môi trường tương tác nâng cao tương tự khác là bpython_.


.. _GNU Readline: https://tiswww.case.edu/php/chet/readline/rltop.html
.. _IPython: https://ipython.org/
.. _bpython: https://bpython-interpreter.org/
