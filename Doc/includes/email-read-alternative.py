import os
import sys
import tempfile
import mimetypes
import webbrowser

# Nhập các mô-đun email cần dùng
from email import policy
from email.parser import BytesParser


def magic_html_parser(html_text, partfiles):
    """Return safety-sanitized html linked to partfiles.

    Rewrite the href="cid:...." attributes to point to the filenames in partfiles.
    Though not trivial, this should be possible using html.parser.
    """
    raise NotImplementedError("Add the magic needed")


# Trong chương trình thực tế, bạn sẽ lấy tên tệp từ đối số.
with open('outgoing.msg', 'rb') as fp:
    msg = BytesParser(policy=policy.default).parse(fp)

# Giờ có thể truy cập các mục phần đầu như một từ điển; mọi ký tự ngoài ASCII
# sẽ được chuyển thành Unicode:
print('To:', msg['to'])
print('From:', msg['from'])
print('Subject:', msg['subject'])

# Nếu muốn in bản xem trước nội dung thư, ta có thể trích xuất phần tải ít định
# dạng nhất và in ba dòng đầu. Dĩ nhiên, nếu thư không có phần văn bản thuần thì
# in ba dòng đầu của HTML có lẽ vô ích, nhưng đây chỉ là ví dụ minh họa.
simplest = msg.get_body(preferencelist=('plain', 'html'))
print()
print(''.join(simplest.get_content().splitlines(keepends=True)[:3]))

ans = input("View full message?")
if ans.lower()[0] == 'n':
    sys.exit()

# Ta có thể trích xuất phương án thay thế giàu định dạng nhất để hiển thị:
richest = msg.get_body()
partfiles = {}
if richest['content-type'].maintype == 'text':
    if richest['content-type'].subtype == 'plain':
        for line in richest.get_content().splitlines():
            print(line)
        sys.exit()
    elif richest['content-type'].subtype == 'html':
        body = richest
    else:
        print("Don't know how to display {}".format(richest.get_content_type()))
        sys.exit()
elif richest['content-type'].content_type == 'multipart/related':
    body = richest.get_body(preferencelist=('html'))
    for part in richest.iter_attachments():
        fn = part.get_filename()
        if fn:
            extension = os.path.splitext(part.get_filename())[1]
        else:
            extension = mimetypes.guess_extension(part.get_content_type())
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as f:
            f.write(part.get_content())
            # Lại bỏ <> để chuyển cid từ dạng email sang dạng HTML.
            partfiles[part['content-id'][1:-1]] = f.name
else:
    print("Don't know how to display {}".format(richest.get_content_type()))
    sys.exit()
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(magic_html_parser(body.get_content(), partfiles))
webbrowser.open(f.name)
os.remove(f.name)
for fn in partfiles.values():
    os.remove(fn)

# Dĩ nhiên, nhiều thư email có thể làm hỏng chương trình đơn giản này, nhưng nó
# sẽ xử lý được các trường hợp phổ biến nhất.
