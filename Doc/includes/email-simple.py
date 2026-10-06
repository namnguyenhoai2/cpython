# Nhập smtplib để dùng hàm gửi thực tế
import smtplib

# Nhập các mô-đun email cần dùng
from email.message import EmailMessage

# Mở để đọc tệp văn bản thuần có tên trong textfile.
with open(textfile) as fp:
    # Tạo thư text/plain
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == địa chỉ email người gửi
# you == địa chỉ email người nhận
msg['Subject'] = f'The contents of {textfile}'
msg['From'] = me
msg['To'] = you

# Gửi thư qua máy chủ SMTP của chúng ta.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
