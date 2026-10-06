#!/usr/bin/env python3

import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

# Tạo thư văn bản cơ sở.
msg = EmailMessage()
msg['Subject'] = "Pourquoi pas des asperges pour ce midi ?"
msg['From'] = Address("Pepé Le Pew", "pepe", "example.com")
msg['To'] = (Address("Penelope Pussycat", "penelope", "example.com"),
             Address("Fabrette Pussycat", "fabrette", "example.com"))
msg.set_content("""\
Salut!

Cette recette [1] sera sûrement un très bon repas.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Pepé
""")

# Thêm phiên bản HTML. Việc này chuyển thư thành vùng chứa multipart/alternative,
# trong đó thư văn bản gốc là phần đầu và thư HTML mới là phần thứ hai.
asparagus_cid = make_msgid()
msg.add_alternative("""\
<html>
  <head></head>
  <body>
    <p>Salut!</p>
    <p>Cette
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recette
        </a> sera sûrement un très bon repas.
    </p>
    <img src="cid:{asparagus_cid}">
  </body>
</html>
""".format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
# Lưu ý rằng cần bỏ <> khỏi msgid để dùng trong HTML.

# Bây giờ thêm ảnh liên quan vào phần HTML.
with open("roasted-asparagus.jpg", 'rb') as img:
    msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                     cid=asparagus_cid)

# Tạo bản sao cục bộ của nội dung sắp gửi.
with open('outgoing.msg', 'wb') as f:
    f.write(bytes(msg))

# Gửi thư qua máy chủ SMTP cục bộ.
with smtplib.SMTP('localhost') as s:
    s.send_message(msg)
