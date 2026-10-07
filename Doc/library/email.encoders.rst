:mod:`!email.encoders`: Bộ mã hóa
---------------------------------

.. module:: email.encoders
   :synopsis: Bộ mã hóa cho payload của email.

**Mã nguồn:** :source:`Lib/email/encoders.py`

--------------

Mô-đun này là một phần của email API cũ (``Compat32``). Trong API mới, chức năng này được cung cấp bởi tham số *cte* của phương thức :meth:`~email.message.EmailMessage.set_content`.

Mô-đun này không được dùng nữa trong Python 3. Không nên gọi trực tiếp các hàm được cung cấp ở đây, vì lớp :class:`~email.mime.text.MIMEText` sẽ thiết lập content type và header CTE bằng các giá trị *_subtype* và *_charset* được truyền khi khởi tạo lớp đó.

Phần văn bản còn lại trong mục này là tài liệu gốc của mô-đun.

Khi tạo các đối tượng :class:`~email.message.Message` từ đầu, bạn thường cần mã hóa payload để truyền qua các mail server tuân thủ tiêu chuẩn. Điều này đặc biệt đúng với các thông báo kiểu :mimetype:`image/\*` và :mimetype:`text/\*` có chứa dữ liệu nhị phân.

Gói :mod:`email` cung cấp một số bộ mã hóa tiện dụng trong
mô-đun :mod:`!encoders`. Các bộ mã hóa này thực sự được sử dụng bởi
các hàm khởi tạo lớp :class:`~email.mime.audio.MIMEAudio` và :class:`~email.mime.image.MIMEImage` để cung cấp các kiểu mã hóa mặc định. Tất cả các hàm mã hóa đều nhận chính xác một đối số là đối tượng message cần mã hóa. Chúng thường trích xuất payload, mã hóa payload rồi đặt lại payload thành giá trị vừa được mã hóa này. Chúng cũng cần đặt header :mailheader:`Content-Transfer-Encoding` thích hợp.

Lưu ý rằng các hàm này không có ý nghĩa đối với message multipart. Thay vào đó, phải áp dụng chúng cho từng subpart riêng lẻ; nếu được truyền một
message có kiểu multipart, chúng sẽ phát sinh :exc:`TypeError`.

Sau đây là các hàm mã hóa được cung cấp:


.. function:: encode_quopri(msg)

   Mã hóa payload thành dạng quoted-printable và đặt
   đầu trang :mailheader:`Content-Transfer-Encoding` thành ``quoted-printable`` [#]_. Đây là một kiểu mã hóa phù hợp khi phần lớn payload của bạn là dữ liệu có thể in thông thường nhưng chứa một vài ký tự không thể in.


.. function:: encode_base64(msg)

   Mã hóa payload thành dạng base64 và đặt
   đầu trang :mailheader:`Content-Transfer-Encoding` thành ``base64``. Đây là một kiểu mã hóa phù hợp khi phần lớn payload của bạn là dữ liệu không thể in, vì nó có dạng gọn hơn quoted-printable. Nhược điểm của mã hóa base64 là khiến văn bản không thể đọc được đối với con người.


.. function:: encode_7or8bit(msg)

   Thao tác này thực sự không sửa đổi payload của message, nhưng lại đặt
   đầu trang :mailheader:`Content-Transfer-Encoding` thành ``7bit`` hoặc ``8bit`` tùy trường hợp, dựa trên dữ liệu payload.


.. function:: encode_noop(msg)

   Thao tác này không làm gì cả; thậm chí cũng không đặt
   đầu trang :mailheader:`Content-Transfer-Encoding`.

.. rubric:: Chú thích cuối trang

.. [#] Lưu ý rằng việc mã hóa bằng :meth:`encode_quopri` cũng mã hóa tất cả các ký tự tab và khoảng trắng trong dữ liệu.

