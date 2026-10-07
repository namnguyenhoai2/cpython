:mod:`!email` --- Gói xử lý email và MIME
=========================================

.. module:: email
   :synopsis: Gói hỗ trợ phân tích cú pháp, thao tác và tạo các thư email.
.. moduleauthor:: Barry A. Warsaw <barry@python.org>,
                  R. David Murray <rdmurray@bitdance.com>
.. sectionauthor:: R. David Murray <rdmurray@bitdance.com>

**Mã nguồn:** :source:`Lib/email/__init__.py`

--------------

Gói :mod:`!email` là một thư viện dùng để quản lý các thư email. Gói này cụ thể *không* được thiết kế để thực hiện việc gửi thư email đến SMTP (:rfc:`2821`), NNTP hoặc các máy chủ khác; đó là chức năng của các mô-đun như
:mod:`smtplib`. Gói :mod:`!email` cố gắng tuân thủ RFC ở mức cao nhất có thể, hỗ trợ :rfc:`5322` và :rfc:`6532`, cũng như các RFC liên quan đến MIME như :rfc:`2045`, :rfc:`2046`, :rfc:`2047`, :rfc:`2183` và :rfc:`2231`.

Cấu trúc tổng thể của gói email có thể được chia thành ba thành phần chính, cùng với một thành phần thứ tư dùng để kiểm soát hoạt động của các thành phần còn lại.

Thành phần trung tâm của gói là một "mô hình đối tượng" đại diện cho các thư email. Ứng dụng chủ yếu tương tác với gói thông qua giao diện mô hình đối tượng được định nghĩa trong mô-đun con :mod:`~email.message`. Ứng dụng có thể sử dụng API này để truy vấn một email hiện có, tạo email mới hoặc thêm hay xóa các thành phần con của email vốn cũng sử dụng cùng giao diện mô hình đối tượng. Nói cách khác, theo đặc điểm của các thư email và các thành phần con MIME, mô hình đối tượng email là một cấu trúc cây gồm các đối tượng đều cung cấp API :class:`~email.message.EmailMessage`.

Hai thành phần chính còn lại của package là :mod:`~email.parser` và :mod:`~email.generator`. Parser nhận phiên bản đã được tuần tự hóa của một email message (một luồng byte) và chuyển đổi nó thành một cây gồm
các đối tượng :class:`~email.message.EmailMessage`. Generator nhận một
:class:`~email.message.EmailMessage` và chuyển đổi nó trở lại thành một luồng byte đã được tuần tự hóa. (Parser và generator cũng xử lý các luồng ký tự văn bản, nhưng không khuyến khích cách sử dụng này vì rất dễ tạo ra các message không hợp lệ theo cách này hay cách khác.)

Thành phần điều khiển là mô-đun :mod:`~email.policy`. Mỗi
:class:`~email.message.EmailMessage`, mỗi :mod:`~email.generator`, và mỗi
:mod:`~email.parser` đều có một đối tượng :mod:`~email.policy` liên kết để kiểm soát hành vi của nó. Thông thường, ứng dụng chỉ cần chỉ định policy khi tạo một :class:`~email.message.EmailMessage`, bằng cách trực tiếp khởi tạo một :class:`~email.message.EmailMessage` để tạo email mới, hoặc phân tích cú pháp một luồng đầu vào bằng :mod:`~email.parser`. Tuy nhiên, policy có thể được thay đổi khi message được tuần tự hóa bằng :mod:`~email.generator`. Điều này cho phép, chẳng hạn, phân tích cú pháp một email message tổng quát từ đĩa, nhưng tuần tự hóa nó bằng các thiết lập SMTP tiêu chuẩn khi gửi đến email server.

Package email cố gắng hết sức để che giấu các chi tiết của nhiều RFC chi phối khác nhau khỏi ứng dụng. Về mặt khái niệm, ứng dụng có thể xử lý email message như một cây có cấu trúc gồm văn bản Unicode và các tệp đính kèm nhị phân, mà không cần lo lắng về cách chúng được biểu diễn khi tuần tự hóa. Tuy nhiên, trên thực tế, thường cần nắm được ít nhất một số quy tắc chi phối các message MIME và cấu trúc của chúng, cụ thể là tên và bản chất của các "content type" MIME cũng như cách chúng xác định các tài liệu multipart. Phần lớn thời gian, kiến thức này chỉ cần thiết đối với các ứng dụng phức tạp hơn; ngay cả khi đó, chỉ cần nắm cấu trúc cấp cao đang được đề cập, chứ không cần biết chi tiết về cách các cấu trúc đó được biểu diễn. Vì content type MIME được sử dụng rộng rãi trong phần mềm Internet hiện đại (không chỉ email), đây sẽ là một khái niệm quen thuộc với nhiều lập trình viên.

Các phần sau đây mô tả chức năng của gói :mod:`!email`. Trước tiên, chúng ta tìm hiểu mô hình đối tượng :mod:`~email.message`, là giao diện chính mà một ứng dụng sẽ sử dụng, sau đó là
các thành phần :mod:`~email.parser` và :mod:`~email.generator`. Tiếp theo, chúng ta tìm hiểu
các cơ chế điều khiển :mod:`~email.policy`, qua đó hoàn tất phần trình bày về những thành phần chính của thư viện.

Ba phần tiếp theo trình bày các ngoại lệ mà gói có thể phát sinh và những khiếm khuyết (không tuân thủ các RFC) mà :mod:`~email.parser` có thể phát hiện. Sau đó, chúng ta tìm hiểu :mod:`~email.headerregistry` và
các thành phần con :mod:`~email.contentmanager`, lần lượt cung cấp các công cụ để thao tác chi tiết hơn với các header và payload. Cả hai thành phần này đều chứa các tính năng hữu ích khi tiếp nhận và tạo các message phức tạp, đồng thời cũng ghi lại các API mở rộng của chúng, vốn sẽ được các ứng dụng nâng cao quan tâm.

Sau đó là một tập hợp các ví dụ về cách sử dụng những phần nền tảng của các API được trình bày trong các phần trước.

Những nội dung trên trình bày API hiện đại (thân thiện với Unicode) của gói email. Các phần còn lại, bắt đầu với lớp :class:`~email.message.Message`, trình bày API :data:`~email.policy.compat32` cũ, vốn làm việc trực tiếp hơn nhiều với các chi tiết về cách các email message được biểu diễn. Phần
:data:`~email.policy.compat32` API *không* che giấu các chi tiết của RFC khỏi ứng dụng, nhưng đối với những ứng dụng cần hoạt động ở cấp độ đó, chúng có thể là những công cụ hữu ích. Tài liệu này cũng phù hợp với các ứng dụng vẫn đang sử dụng API :mod:`~email.policy.compat32` vì lý do tương thích ngược.

.. versionchanged:: 3.6
   Tài liệu được sắp xếp lại và viết lại để quảng bá phiên bản mới của
   :class:`~email.message.EmailMessage`/:class:`~email.policy.EmailPolicy` API.

Nội dung tài liệu của package :mod:`!email`:

.. toctree::

   email.message.rst
   email.parser.rst
   email.generator.rst
   email.policy.rst

   email.errors.rst
   email.headerregistry.rst
   email.contentmanager.rst

   email.examples.rst

API cũ:

.. toctree::

   email.compat32-message.rst
   email.mime.rst
   email.header.rst
   email.charset.rst
   email.encoders.rst
   email.utils.rst
   email.iterators.rst


.. seealso::

   Mô-đun :mod:`smtplib`
      client SMTP (Simple Mail Transport Protocol)

   Mô-đun :mod:`poplib`
      client POP (Post Office Protocol)

   Mô-đun :mod:`imaplib`
      client IMAP (Internet Message Access Protocol)

   Mô-đun :mod:`mailbox`
      Các công cụ để tạo, đọc và quản lý các tập hợp thư trên đĩa bằng nhiều định dạng tiêu chuẩn.
