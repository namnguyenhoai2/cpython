:mod:`!email.errors`: Các lớp Exception và Defect
-------------------------------------------------

.. module:: email.errors
   :synopsis: Các lớp ngoại lệ được gói email sử dụng.

**Mã nguồn:** :source:`Lib/email/errors.py`

--------------

Các lớp ngoại lệ sau được định nghĩa trong mô-đun :mod:`!email.errors`:‎


.. exception:: MessageError()

   Đây là lớp cơ sở cho tất cả các ngoại lệ mà gói :mod:`email` có thể phát sinh. Lớp này kế thừa từ lớp :exc:`Exception` tiêu chuẩn và không định nghĩa thêm phương thức nào.


.. exception:: MessageParseError()

   Đây là lớp cơ sở cho các ngoại lệ được phát sinh bởi
   :class:`~email.parser.Parser` class. Lớp này kế thừa từ
   :exc:`MessageError`. Lớp này cũng được trình phân tích cú pháp được :mod:`~email.headerregistry` sử dụng nội bộ.


.. exception:: HeaderParseError()

   Được phát sinh trong một số điều kiện lỗi khi phân tích cú pháp các header :rfc:`5322` của một message, lớp này kế thừa từ :exc:`MessageParseError`. The
   Phương thức :meth:`~email.message.EmailMessage.set_boundary` sẽ phát sinh lỗi này nếu không xác định được content type khi phương thức được gọi.
   :class:`~email.header.Header` có thể phát sinh lỗi này đối với một số lỗi giải mã base64 và khi có nỗ lực tạo một header có vẻ chứa một header được nhúng (nghĩa là có một continuation line được cho là không có khoảng trắng ở đầu và trông giống một header).


.. exception:: BoundaryError()

   Đã lỗi thời và không còn được sử dụng.


.. exception:: MultipartConversionError()

   Được phát sinh nếu phương thức :meth:`~email.message.Message.attach` được gọi trên một instance của lớp kế thừa từ
   :class:`~email.mime.nonmultipart.MIMENonMultipart` (ví dụ:
   :class:`~email.mime.image.MIMEImage`).
   :exc:`MultipartConversionError` kế thừa đa lớp từ :exc:`MessageError` và :exc:`TypeError` tích hợp sẵn.


.. exception:: HeaderWriteError()

   Được phát sinh khi xảy ra lỗi lúc :mod:`~email.generator` xuất các header.


.. exception:: MessageDefect()

   Đây là lớp cơ sở cho tất cả các defect được phát hiện khi phân tích cú pháp email message. Lớp này được dẫn xuất từ :exc:`ValueError`.

.. exception:: HeaderDefect()

   Đây là lớp cơ sở cho tất cả các defect được phát hiện khi phân tích cú pháp email header. Lớp này được dẫn xuất từ :exc:`MessageDefect`.

Sau đây là danh sách các defect mà :class:`~email.parser.FeedParser` có thể tìm thấy khi phân tích cú pháp message. Lưu ý rằng các defect được thêm vào message nơi phát hiện vấn đề; vì vậy, ví dụ, nếu một message nằm bên trong một
:mimetype:`multipart/alternative` có header không đúng định dạng, thì đối tượng message lồng nhau đó sẽ có một defect, còn các message chứa nó thì không.

Tất cả các lớp defect đều là lớp con của :class:`email.errors.MessageDefect`.

.. exception:: NoBoundaryInMultipartDefect

   Một thư được cho là multipart nhưng không có tham số :mimetype:`boundary`.

.. exception:: StartBoundaryNotFoundDefect

   Không tìm thấy boundary bắt đầu được khai báo trong header :mailheader:`Content-Type`.

.. exception:: CloseBoundaryNotFoundDefect

   Đã tìm thấy boundary bắt đầu nhưng không tìm thấy boundary kết thúc tương ứng.

   .. versionadded:: 3.3

.. exception:: FirstHeaderLineIsContinuationDefect

   Thư có một dòng tiếp diễn làm dòng header đầu tiên.

.. exception:: MisplacedEnvelopeHeaderDefect

   Đã tìm thấy header "Unix From" ở giữa một khối header.

.. exception:: MissingHeaderBodySeparatorDefect

   Trong khi phân tích các header, đã tìm thấy một dòng không có khoảng trắng ở đầu nhưng không chứa ký tự ':'. Quá trình phân tích tiếp tục với giả định rằng dòng này là dòng đầu tiên của phần nội dung.

   .. versionadded:: 3.3

.. exception:: MalformedHeaderDefect

   Đã tìm thấy một header bị thiếu dấu hai chấm hoặc bị sai định dạng theo cách khác.

   .. deprecated:: 3.3
      Lỗi này đã không được sử dụng trong một số phiên bản Python.

.. exception:: MultipartInvariantViolationDefect

   Một thông báo được cho là :mimetype:`multipart`, nhưng không tìm thấy phần con nào. Lưu ý rằng khi một thông báo có lỗi này, phương thức
   :meth:`~email.message.Message.is_multipart` có thể trả về ``False`` mặc dù kiểu nội dung của nó được khai báo là :mimetype:`multipart`.

.. exception:: InvalidBase64PaddingDefect

   Khi giải mã một khối byte được mã hóa bằng base64, phần đệm không chính xác. Phần đệm đủ để thực hiện giải mã sẽ được thêm vào, nhưng các byte sau khi giải mã có thể không hợp lệ.

.. exception:: InvalidBase64CharactersDefect

   Khi giải mã một khối byte được mã hóa bằng base64, đã gặp các ký tự nằm ngoài bảng chữ cái base64. Các ký tự này sẽ bị bỏ qua, nhưng các byte sau khi giải mã có thể không hợp lệ.

.. exception:: InvalidBase64LengthDefect

   Khi giải mã một khối base64, số ký tự base64 không phải ký tự đệm không hợp lệ (lớn hơn một bội số của 4 là 1). Khối đã mã hóa được giữ nguyên.

.. exception:: InvalidDateDefect

   Khi giải mã một trường ngày không hợp lệ hoặc không thể phân tích cú pháp. Giá trị ban đầu được giữ nguyên.
