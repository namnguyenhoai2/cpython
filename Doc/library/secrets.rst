:mod:`!secrets` --- secrets --- Tạo các số ngẫu nhiên an toàn để quản lý secret
===============================================================================

.. module:: secrets
   :synopsis: Tạo các số ngẫu nhiên an toàn để quản lý secret.

.. moduleauthor:: Steven D'Aprano <steve+python@pearwood.info>
.. sectionauthor:: Steven D'Aprano <steve+python@pearwood.info>
.. versionadded:: 3.6

.. testsetup::

   from secrets import *
   __name__ = '<doctest>'

**Mã nguồn:** :source:`Lib/secrets.py`

-------------

Module :mod:`!secrets` được dùng để tạo các số ngẫu nhiên có độ mạnh mật mã, phù hợp để quản lý những dữ liệu như mật khẩu, thông tin xác thực tài khoản, security token và các secret liên quan.

Cụ thể, nên ưu tiên sử dụng :mod:`!secrets` thay cho bộ tạo số giả ngẫu nhiên mặc định trong module :mod:`random`, vốn được thiết kế cho việc lập mô hình và mô phỏng, không phải cho bảo mật hay mật mã.

.. seealso::

   :pep:`506`


Các số ngẫu nhiên
-----------------

Module :mod:`!secrets` cung cấp quyền truy cập vào nguồn ngẫu nhiên an toàn nhất mà hệ điều hành của bạn cung cấp.

.. class:: SystemRandom

   Lớp dùng để tạo số ngẫu nhiên bằng các nguồn có chất lượng cao nhất do hệ điều hành cung cấp. Xem
   :class:`random.SystemRandom` để biết thêm chi tiết.

.. function:: choice(seq)

   Trả về một phần tử được chọn ngẫu nhiên từ một sequence không rỗng.

.. function:: randbelow(exclusive_upper_bound)

   Trả về một số nguyên ngẫu nhiên trong phạm vi [0, *exclusive_upper_bound*).

.. function:: randbits(k)

   Trả về một số nguyên không âm có *k* bit ngẫu nhiên.


Tạo token
---------

Module :mod:`!secrets` cung cấp các hàm để tạo token bảo mật, phù hợp cho các ứng dụng như đặt lại mật khẩu, URL khó đoán và những trường hợp tương tự.

.. function:: token_bytes(nbytes=None)

   Trả về một chuỗi byte ngẫu nhiên chứa *nbytes* byte.

   Nếu *nbytes* không được chỉ định hoặc ``None``, :const:`DEFAULT_ENTROPY` được sử dụng thay thế.

   .. doctest::

      >>> token_bytes(16)  # doctest: +SKIP
      b'\xebr\x17D*t\xae\xd4\xe3S\xb6\xe2\xebP1\x8b'


.. function:: token_hex(nbytes=None)

   Trả về một chuỗi văn bản ngẫu nhiên ở dạng thập lục phân. Chuỗi này có *nbytes* byte ngẫu nhiên, mỗi byte được chuyển thành hai chữ số hex.

   Nếu *nbytes* không được chỉ định hoặc ``None``, :const:`DEFAULT_ENTROPY` được sử dụng thay thế.

   .. doctest::

      >>> token_hex(16)  # doctest: +SKIP
      'f9bf78b9a18ce6d46a0cd2b0b86df9da'

.. function:: token_urlsafe(nbytes=None)

   Trả về một chuỗi văn bản ngẫu nhiên an toàn cho URL, chứa *nbytes* byte ngẫu nhiên. Văn bản được mã hóa Base64, vì vậy trung bình mỗi byte tạo ra khoảng 1,3 ký tự.

   Nếu *nbytes* không được chỉ định hoặc ``None``, :const:`DEFAULT_ENTROPY` được sử dụng thay thế.

   .. doctest::

      >>> token_urlsafe(16)  # doctest: +SKIP
      'Drmhze6EPcv0fN_81Bj-nA'


Token nên sử dụng bao nhiêu byte?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để an toàn trước các cuộc tấn công `brute-force attacks <https://en.wikipedia.org/wiki/Brute-force_attack>`_, token cần có đủ tính ngẫu nhiên. Đáng tiếc là mức được xem là đủ chắc chắn sẽ tăng lên khi máy tính trở nên mạnh hơn và có khả năng thực hiện nhiều lần đoán hơn trong thời gian ngắn hơn. Tính đến năm 2015, người ta cho rằng 32 byte (256 bit) tính ngẫu nhiên là đủ cho trường hợp sử dụng điển hình dự kiến của module :mod:`!secrets`.

Nếu muốn tự quản lý độ dài token, bạn có thể chỉ định rõ lượng tính ngẫu nhiên được sử dụng cho token bằng cách cung cấp một đối số :class:`int` cho các hàm ``token_*`` khác nhau. Đối số đó được hiểu là số byte tính ngẫu nhiên cần sử dụng.

Nếu không cung cấp đối số hoặc đối số là ``None``, các hàm ``token_*`` sẽ sử dụng :const:`DEFAULT_ENTROPY` thay thế.

.. data:: DEFAULT_ENTROPY

   Số byte tính ngẫu nhiên mặc định được các hàm ``token_*`` sử dụng.

   Giá trị chính xác có thể thay đổi bất cứ lúc nào, kể cả trong các bản phát hành bảo trì.


Các hàm khác
------------

.. function:: compare_digest(a, b)

   Trả về ``True`` nếu các chuỗi hoặc
   :term:`đối tượng dạng byte <bytes-like object>` *a* và *b* bằng nhau; nếu không thì ``False``, sử dụng phép so sánh "constant-time" để giảm nguy cơ `tấn công timing <https://web.archive.org/web/20250815071532/https://codahale.com/a-lesson-in-timing-attacks/>`__. Xem :func:`hmac.compare_digest` để biết thêm chi tiết.


Công thức và phương pháp hay nhất
---------------------------------

Phần này trình bày các công thức và phương pháp hay nhất để sử dụng :mod:`!secrets` nhằm quản lý mức độ bảo mật cơ bản.

Tạo mật khẩu chữ và số gồm tám ký tự:

.. testcode::

   import string
   import secrets
   alphabet = string.ascii_letters + string.digits
   password = ''.join(secrets.choice(alphabet) for i in range(8))


.. note::

   Ứng dụng không nên
   :cwe:`store passwords in a recoverable format <257>`, dù ở dạng văn bản thuần túy hay được mã hóa. Chúng nên được thêm salt và băm bằng hàm băm một chiều mạnh về mặt mật mã (không thể đảo ngược).


Tạo mật khẩu gồm mười ký tự chữ và số, trong đó có ít nhất một ký tự viết thường, ít nhất một ký tự viết hoa và ít nhất ba chữ số:

.. testcode::

   import string
   import secrets
   alphabet = string.ascii_letters + string.digits
   while True:
       password = ''.join(secrets.choice(alphabet) for i in range(10))
       if (any(c.islower() for c in password)
               and any(c.isupper() for c in password)
               and sum(c.isdigit() for c in password) >= 3):
           break


Tạo một `cụm mật khẩu theo phong cách XKCD <https://xkcd.com/936/>`_:

.. testcode::

   import secrets
   # Trên các hệ thống Linux tiêu chuẩn, hãy sử dụng một tệp từ điển tiện lợi.
   # Các nền tảng khác có thể cần cung cấp danh sách từ riêng.
   with open('/usr/share/dict/words') as f:
       words = [word.strip() for word in f]
       password = ' '.join(secrets.choice(words) for i in range(4))


Tạo một URL tạm thời khó đoán, chứa security token phù hợp cho các ứng dụng khôi phục mật khẩu:

.. testcode::

   import secrets
   url = 'https://example.com/reset=' + secrets.token_urlsafe()



..
   # Dòng modeline này phải xuất hiện trong mười dòng cuối cùng của tệp. kate: indent-width 3; remove-trailing-space on; replace-tabs on; encoding utf-8;

.. _`brute-force attacks`: https://en.wikipedia.org/wiki/Brute-force_attack
.. _`XKCD-style passphrase`: https://xkcd.com/936/
