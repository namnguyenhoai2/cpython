# Nhập các mô-đun email cần dùng
#from email.parser import BytesParser
from email.parser import Parser
from email.policy import default

# Nếu phần đầu email nằm trong tệp, bỏ chú thích hai dòng này:
# with open(messagefile, 'rb') as fp:
#     headers = BytesParser(policy=default).parse(fp)

#  Hoặc để phân tích phần đầu trong một chuỗi (ít khi cần), hãy dùng:
headers = Parser(policy=default).parsestr(
        'From: Foo Bar <user@example.com>\n'
        'To: <someone_else@example.com>\n'
        'Subject: Test message\n'
        '\n'
        'Body would go here\n')

#  Giờ có thể truy cập các mục phần đầu như một từ điển:
print('To: {}'.format(headers['to']))
print('From: {}'.format(headers['from']))
print('Subject: {}'.format(headers['subject']))

# Bạn cũng có thể truy cập các thành phần của địa chỉ:
print('Recipient username: {}'.format(headers['to'].addresses[0].username))
print('Sender name: {}'.format(headers['from'].addresses[0].display_name))
