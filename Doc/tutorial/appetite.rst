.. _tut-intro:

*****************
Khơi gợi hứng thú
*****************

Nếu bạn làm việc nhiều với máy tính, cuối cùng bạn sẽ nhận ra có một số tác vụ mà mình muốn tự động hóa. Ví dụ: bạn có thể muốn thực hiện thao tác tìm kiếm và thay thế trên một số lượng lớn tệp văn bản, hoặc đổi tên và sắp xếp lại một loạt tệp ảnh theo cách phức tạp. Có lẽ bạn muốn viết một cơ sở dữ liệu tùy chỉnh nhỏ, một ứng dụng GUI chuyên biệt hoặc một trò chơi đơn giản.

Nếu là một software developer chuyên nghiệp, bạn có thể phải làm việc với một số thư viện C/C++/Java nhưng nhận thấy chu trình viết/biên dịch/kiểm thử/biên dịch lại thông thường quá chậm. Có lẽ bạn đang viết một bộ kiểm thử cho một thư viện như vậy và thấy việc viết mã kiểm thử thật tẻ nhạt. Hoặc có thể bạn đã viết một chương trình có thể sử dụng một ngôn ngữ mở rộng, nhưng không muốn thiết kế và triển khai cả một ngôn ngữ mới cho ứng dụng của mình.

Python chính là ngôn ngữ dành cho bạn.

Bạn có thể viết một shell script Unix hoặc các tệp batch của Windows cho một số tác vụ này, nhưng shell script phù hợp nhất với việc di chuyển tệp và thay đổi dữ liệu văn bản, chứ không phù hợp với các ứng dụng GUI hoặc trò chơi. Bạn có thể viết một chương trình C/C++/Java, nhưng để có được ngay cả một chương trình bản nháp đầu tiên cũng có thể mất rất nhiều thời gian phát triển. Python dễ sử dụng hơn, có sẵn trên các hệ điều hành Windows, macOS và Unix, đồng thời giúp bạn hoàn thành công việc nhanh hơn.

Python dễ sử dụng, nhưng là một ngôn ngữ lập trình thực thụ, cung cấp cấu trúc và khả năng hỗ trợ cho các chương trình lớn tốt hơn nhiều so với shell script hoặc tệp batch. Mặt khác, Python cũng cung cấp khả năng kiểm tra lỗi tốt hơn nhiều so với C, và vì là *ngôn ngữ cấp rất cao*, Python có sẵn các kiểu dữ liệu cấp cao, chẳng hạn như mảng linh hoạt và từ điển. Nhờ các kiểu dữ liệu tổng quát hơn, Python có thể áp dụng cho một phạm vi vấn đề lớn hơn nhiều so với Awk hoặc thậm chí Perl, nhưng nhiều việc trong Python ít nhất cũng dễ dàng như trong các ngôn ngữ đó.

Python cho phép bạn chia chương trình thành các module có thể được tái sử dụng trong những chương trình Python khác. Python đi kèm một bộ sưu tập lớn các module tiêu chuẩn mà bạn có thể dùng làm nền tảng cho chương trình của mình --- hoặc làm ví dụ để bắt đầu học lập trình bằng Python. Một số module này cung cấp các chức năng như I/O tệp, system call, socket và thậm chí cả các interface với những bộ công cụ graphical user interface như Tk.

Python là một ngôn ngữ thông dịch, nhờ đó có thể giúp bạn tiết kiệm đáng kể thời gian trong quá trình phát triển chương trình vì không cần biên dịch và liên kết. Trình thông dịch có thể được sử dụng tương tác, giúp bạn dễ dàng thử nghiệm các tính năng của ngôn ngữ, viết các chương trình dùng một lần hoặc kiểm thử các hàm trong quá trình phát triển chương trình theo hướng từ dưới lên. Đây cũng là một công cụ tính toán để bàn tiện dụng.

Python cho phép viết các chương trình ngắn gọn và dễ đọc. Các chương trình viết bằng Python thường ngắn hơn nhiều so với các chương trình C, C++ hoặc Java tương đương, vì một số lý do sau:

* các kiểu dữ liệu cấp cao cho phép bạn biểu đạt những thao tác phức tạp trong một câu lệnh duy nhất;

* việc nhóm các câu lệnh được thực hiện bằng thụt lề thay vì dùng dấu ngoặc mở và đóng;

* không cần khai báo biến hoặc đối số.

Python *có khả năng mở rộng*: nếu bạn biết lập trình bằng C, bạn có thể dễ dàng thêm một hàm hoặc module tích hợp mới vào trình thông dịch, είτε để thực hiện các thao tác quan trọng với tốc độ tối đa, είτε để liên kết các chương trình Python với những thư viện có thể chỉ tồn tại ở dạng nhị phân (chẳng hạn như thư viện đồ họa dành riêng cho một nhà cung cấp). Khi đã thực sự say mê, bạn có thể nhúng trình thông dịch Python vào một ứng dụng viết bằng C và sử dụng nó như một ngôn ngữ mở rộng hoặc ngôn ngữ lệnh cho ứng dụng đó.

Nhân tiện, ngôn ngữ này được đặt tên theo chương trình truyền hình của BBC có tên "Monty Python's Flying Circus" và hoàn toàn không liên quan đến loài bò sát. Việc nhắc đến các tiểu phẩm của Monty Python trong tài liệu không chỉ được cho phép mà còn được khuyến khích!

Giờ đây, khi đã hào hứng với Python, bạn sẽ muốn tìm hiểu kỹ hơn về nó. Vì cách tốt nhất để học một ngôn ngữ là sử dụng ngôn ngữ đó, tài liệu hướng dẫn sẽ mời bạn thực hành với Python interpreter trong khi đọc.

Trong chương tiếp theo, tài liệu giải thích cách sử dụng interpreter. Đây là những thông tin khá tẻ nhạt nhưng thiết yếu để thử các ví dụ được trình bày ở phần sau.

Phần còn lại của tài liệu hướng dẫn giới thiệu nhiều tính năng khác nhau của ngôn ngữ và hệ thống Python thông qua các ví dụ, bắt đầu với những biểu thức, câu lệnh và kiểu dữ liệu đơn giản, tiếp đến là các hàm và module, rồi cuối cùng đề cập đến những khái niệm nâng cao như exception và lớp do người dùng định nghĩa.


