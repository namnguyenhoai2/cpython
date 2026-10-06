# Nhập smtplib để dùng hàm gửi thực tế.
import smtplib

# Đây là các mô-đun gói email cần dùng.
from email.message import EmailMessage

# Tạo thư email chứa các phần khác.
msg = EmailMessage()
msg['Subject'] = 'Our family reunion'
# me == địa chỉ email người gửi
# family = danh sách địa chỉ email của mọi người nhận
msg['From'] = me
msg['To'] = ', '.join(family)
msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

# Mở tệp ở chế độ nhị phân. Bạn cũng có thể bỏ subtype
# nếu muốn MIMEImage tự suy đoán.
for file in pngfiles:
    with open(file, 'rb') as fp:
        img_data = fp.read()
    msg.add_attachment(img_data, maintype='image',
                                 subtype='png')

# Gửi email qua máy chủ SMTP của chúng ta.
with smtplib.SMTP('localhost') as s:
    s.send_message(msg)
