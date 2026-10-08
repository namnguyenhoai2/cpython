:mod:`!hashlib` --- Băm bảo mật và thông báo tóm lược
=====================================================

.. module:: hashlib
   :synopsis: Các thuật toán băm bảo mật và thông báo tóm lược.

.. moduleauthor:: Gregory P. Smith <greg@krypto.org>
.. sectionauthor:: Gregory P. Smith <greg@krypto.org>

**Mã nguồn:** :source:`Lib/hashlib.py`

.. index::
   single: message digest, MD5
   single: secure hash algorithm, SHA1, SHA2, SHA224, SHA256, SHA384, SHA512, SHA3, Shake, Blake2

.. testsetup::

   import hashlib


--------------

Mô-đun này triển khai một giao diện chung cho nhiều thuật toán băm khác nhau. Bao gồm các thuật toán băm bảo mật FIPS SHA224, SHA256, SHA384, SHA512 (được định nghĩa trong `tiêu chuẩn FIPS 180-4 <the FIPS 180-4 standard_>`_), dòng SHA-3 (được định nghĩa trong `tiêu chuẩn FIPS 202 <the FIPS 202 standard_>`_), cũng như các thuật toán cũ SHA1 (`trước đây là một phần của FIPS <formerly part of FIPS_>`_) và thuật toán MD5 (được định nghĩa trong :rfc:`1321`).

.. note::

   Nếu bạn muốn các hàm băm adler32 hoặc crc32, chúng có sẵn trong mô-đun :mod:`zlib`.


.. _hash-algorithms:

Các thuật toán băm
------------------

Có một phương thức khởi tạo được đặt tên theo từng loại :dfn:`hàm băm`. Tất cả đều trả về một đối tượng băm với cùng một giao diện đơn giản. Ví dụ: sử dụng :func:`sha256` để tạo một đối tượng băm SHA-256. Bây giờ bạn có thể cung cấp dữ liệu cho đối tượng này bằng
:term:`các đối tượng dạng bytes <bytes-like object>` (thông thường là :class:`bytes`) bằng phương thức :meth:`update<hash.update>`. Bất cứ lúc nào, bạn cũng có thể yêu cầu nó cung cấp
:dfn:`digest` của phép nối các dữ liệu đã được truyền vào nó cho đến thời điểm đó bằng cách sử dụng
các phương thức :meth:`digest()<hash.digest>` hoặc :meth:`hexdigest()<hash.hexdigest>`.

Để cho phép đa luồng, :term:`GIL` của Python được giải phóng trong khi tính toán một hash được cung cấp hơn 2047 byte dữ liệu cùng lúc trong hàm khởi tạo hoặc
phương thức :meth:`.update<hash.update>`.


.. index:: single: OpenSSL; (use in module hashlib)

Các hàm khởi tạo cho những thuật toán hash luôn có trong module này là
:func:`sha1`, :func:`sha224`, :func:`sha256`, :func:`sha384`, :func:`sha512`,
:func:`sha3_224`, :func:`sha3_256`, :func:`sha3_384`, :func:`sha3_512`,
:func:`shake_128`, :func:`shake_256`, :func:`blake2b` và :func:`blake2s`.
:func:`md5` cũng thường có sẵn, mặc dù có thể bị thiếu hoặc bị chặn nếu bạn đang sử dụng một bản build Python "tuân thủ FIPS" hiếm gặp. Các thuật toán này tương ứng với :data:`algorithms_guaranteed`.

Các thuật toán bổ sung cũng có thể có sẵn nếu bản phân phối Python của bạn
:mod:`!hashlib` được liên kết với một bản build OpenSSL cung cấp các thuật toán khác. Các thuật toán khác *không được đảm bảo là có sẵn* trên mọi bản cài đặt và chỉ có thể được truy cập theo tên thông qua :func:`new`. Xem :data:`algorithms_available`.

.. warning::

   Một số thuật toán có các điểm yếu đã biết về va chạm hash (bao gồm MD5 và SHA1). Hãy tham khảo `Các cuộc tấn công vào thuật toán hash mật mã <Attacks on cryptographic hash algorithms_>`_ và phần `hashlib-seealso`_ ở cuối tài liệu này.

.. versionadded:: 3.6
   Các hàm khởi tạo SHA3 (Keccak) và SHAKE :func:`sha3_224`, :func:`sha3_256`,
   :func:`sha3_384`, :func:`sha3_512`, :func:`shake_128`, :func:`shake_256` đã được thêm vào.
   :func:`blake2b` và :func:`blake2s` đã được thêm vào.

.. _hashlib-usedforsecurity:

.. versionchanged:: 3.9
   Tất cả các constructor của hashlib đều nhận một đối số chỉ nhận bằng từ khóa *usedforsecurity*, có giá trị mặc định là ``True``. Giá trị false cho phép sử dụng các thuật toán băm không an toàn và bị chặn trong những môi trường bị hạn chế. ``False`` cho biết thuật toán băm không được sử dụng trong ngữ cảnh bảo mật, chẳng hạn như một hàm nén một chiều không mang tính mật mã.

.. versionchanged:: 3.9
   Hashlib hiện sử dụng SHA3 và SHAKE từ OpenSSL nếu OpenSSL cung cấp các thuật toán này.

.. versionchanged:: 3.12
   Đối với bất kỳ thuật toán MD5, SHA1, SHA2 hoặc SHA3 nào không được OpenSSL được liên kết cung cấp, chúng tôi sẽ chuyển sang sử dụng một triển khai đã được xác minh từ dự án `HACL\* project <HACL\* project_>`_.

Cách sử dụng
------------

Để lấy digest của chuỗi byte ``b"Nobody inspects the spammish repetition"``::

   >>> import hashlib
   >>> m = hashlib.sha256()
   >>> m.update(b"Nobody inspects")
   >>> m.update(b" the spammish repetition")
   >>> m.digest()
   b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
   >>> m.hexdigest()
   '031edd7d41651593c5fe5c006fa5752b37fddff7bc4e843aa6af0c950f4b9406'

Viết cô đọng hơn:

   >>> hashlib.sha256(b"Nobody inspects the spammish repetition").hexdigest()
   '031edd7d41651593c5fe5c006fa5752b37fddff7bc4e843aa6af0c950f4b9406'

Các constructor
---------------

.. function:: new(name[, data], *, usedforsecurity=True)

   Là một hàm khởi tạo tổng quát nhận chuỗi *name* của thuật toán mong muốn làm tham số đầu tiên. Hàm này cũng cho phép truy cập các hàm băm được liệt kê ở trên, cũng như mọi thuật toán khác mà thư viện OpenSSL của bạn có thể cung cấp.

Sử dụng :func:`new` với tên thuật toán:

   >>> h = hashlib.new('sha256')
   >>> h.update(b"Nobody inspects the spammish repetition")
   >>> h.hexdigest()
   '031edd7d41651593c5fe5c006fa5752b37fddff7bc4e843aa6af0c950f4b9406'


.. function:: md5([, data], *, usedforsecurity=True)
.. function:: sha1([, data], *, usedforsecurity=True)
.. function:: sha224([, data], *, usedforsecurity=True)
.. function:: sha256([, data], *, usedforsecurity=True)
.. function:: sha384([, data], *, usedforsecurity=True)
.. function:: sha512([, data], *, usedforsecurity=True)
.. function:: sha3_224([, data], *, usedforsecurity=True)
.. function:: sha3_256([, data], *, usedforsecurity=True)
.. function:: sha3_384([, data], *, usedforsecurity=True)
.. function:: sha3_512([, data], *, usedforsecurity=True)

Các hàm khởi tạo có tên như thế này nhanh hơn việc truyền tên thuật toán cho
:func:`new`.

Thuộc tính
----------

Hashlib cung cấp các thuộc tính hằng số mô-đun sau:

.. data:: algorithms_guaranteed

   Một tập hợp chứa tên của các thuật toán băm được đảm bảo hỗ trợ bởi mô-đun này trên mọi nền tảng. Lưu ý rằng 'md5' vẫn nằm trong danh sách này, mặc dù một số nhà cung cấp upstream cung cấp một bản dựng Python "tuân thủ FIPS" khác thường nhưng loại trừ thuật toán này.

   .. versionadded:: 3.2

.. data:: algorithms_available

   Một tập hợp chứa tên của các thuật toán băm có sẵn trong trình thông dịch Python đang chạy. Các tên này sẽ được nhận dạng khi được truyền cho
   :func:`new`.  :attr:`algorithms_guaranteed` sẽ luôn là một tập hợp con.  Cùng một thuật toán có thể xuất hiện nhiều lần trong tập hợp này dưới các tên khác nhau (nhờ OpenSSL).

   .. versionadded:: 3.2

Đối tượng Hash
--------------

Các giá trị sau được cung cấp dưới dạng các thuộc tính hằng của những đối tượng hash được các hàm khởi tạo trả về:

.. data:: hash.digest_size

   Kích thước của hash tạo ra, tính bằng byte.

.. data:: hash.block_size

   Kích thước khối nội bộ của thuật toán hash, tính bằng byte.

Một đối tượng hash có các thuộc tính sau:

.. attribute:: hash.name

   Tên chuẩn của hash này, luôn được viết bằng chữ thường và luôn phù hợp để dùng làm tham số cho :func:`new` nhằm tạo một hash khác cùng loại.

   .. versionchanged:: 3.4
      Thuộc tính name đã có trong CPython ngay từ khi được khởi tạo, nhưng cho đến Python 3.4 vẫn chưa được đặc tả chính thức, vì vậy có thể không tồn tại trên một số nền tảng.

Một đối tượng hash có các phương thức sau:


.. method:: hash.update(data)

   Cập nhật đối tượng hash với :term:`bytes-like object`. Việc gọi lặp lại tương đương với một lần gọi duy nhất có phép nối của tất cả các đối số: ``m.update(a); m.update(b)`` tương đương với ``m.update(a+b)``.


.. method:: hash.digest()

   Trả về digest của dữ liệu đã được truyền cho phương thức :meth:`update` tính đến thời điểm hiện tại. Đây là một đối tượng bytes có kích thước :attr:`digest_size`, có thể chứa các byte trong toàn bộ phạm vi từ 0 đến 255.


.. method:: hash.hexdigest()

   Giống như :meth:`digest`, ngoại trừ việc digest được trả về dưới dạng một đối tượng string có độ dài gấp đôi, chỉ chứa các chữ số thập lục phân. Có thể dùng cách này để trao đổi giá trị một cách an toàn qua email hoặc trong các môi trường không nhị phân khác.


.. method:: hash.copy()

   Trả về một bản sao ("clone") của đối tượng hash. Có thể dùng cách này để tính hiệu quả các digest của những dữ liệu có chung một chuỗi con ban đầu.


Digest SHAKE có độ dài thay đổi
-------------------------------

.. function:: shake_128([, data], *, usedforsecurity=True)
.. function:: shake_256([, data], *, usedforsecurity=True)

Các thuật toán :func:`shake_128` và :func:`shake_256` cung cấp digest có độ dài thay đổi, với độ dài theo bit//2 mang lại mức độ bảo mật lên đến 128 hoặc 256 bit. Do đó, các phương thức digest của chúng yêu cầu một độ dài. Độ dài tối đa không bị giới hạn bởi thuật toán SHAKE.

.. method:: shake.digest(length)

   Trả về digest của dữ liệu đã được truyền cho phương thức :meth:`~hash.update` tính đến thời điểm hiện tại. Đây là một đối tượng bytes có kích thước *length*, có thể chứa các byte trong toàn bộ phạm vi từ 0 đến 255.


.. method:: shake.hexdigest(length)

   Tương tự như :meth:`digest`, nhưng digest được trả về dưới dạng một đối tượng string có độ dài gấp đôi, chỉ chứa các chữ số thập lục phân. Có thể dùng cách này để trao đổi giá trị qua email hoặc các môi trường không nhị phân khác.

Ví dụ sử dụng:

   >>> h = hashlib.shake_256(b'Nobody inspects the spammish repetition')
   >>> h.hexdigest(20)
   '44709d6fcb83d92a76dcb0b668c98e1b1d3dafe7'

Băm tệp
-------

Mô-đun hashlib cung cấp một hàm trợ giúp để băm hiệu quả một tệp hoặc đối tượng giống tệp.

.. function:: file_digest(fileobj, digest, /)

   Trả về một đối tượng digest đã được cập nhật bằng nội dung của đối tượng tệp.

   *fileobj* phải là một đối tượng dạng tệp được mở để đọc ở chế độ nhị phân. Nó chấp nhận các đối tượng tệp từ builtin :func:`open`, các thực thể :class:`~io.BytesIO`, các đối tượng SocketIO từ :meth:`socket.socket.makefile` và những đối tượng tương tự. *fileobj* phải được mở ở chế độ blocking, nếu không thì một
   :exc:`BlockingIOError` có thể được phát sinh.

   Hàm có thể bỏ qua I/O của Python và sử dụng trực tiếp file descriptor từ :meth:`~io.IOBase.fileno`. *fileobj* phải được giả định là ở trạng thái không xác định sau khi hàm này trả về hoặc phát sinh ngoại lệ. Người gọi có trách nhiệm đóng *fileobj*.

   *digest* phải là tên của một thuật toán băm dưới dạng *str*, một hash constructor hoặc một callable trả về một hash object.

   Ví dụ:

      >>> import io, hashlib, hmac
      >>> with open("library/hashlib.rst", "rb") as f:
      ...     digest = hashlib.file_digest(f, "sha256")
      ...
      >>> digest.hexdigest()  # doctest: +ELLIPSIS
      '...'

      >>> buf = io.BytesIO(b"somedata")
      >>> mac1 = hmac.HMAC(b"key", digestmod=hashlib.sha512)
      >>> digest = hashlib.file_digest(buf, lambda: mac1)

      >>> digest is mac1
      True
      >>> mac2 = hmac.HMAC(b"key", b"somedata", digestmod=hashlib.sha512)
      >>> mac1.digest() == mac2.digest()
      True

   .. versionadded:: 3.11

   .. versionchanged:: 3.14
      Hiện sẽ phát sinh một :exc:`BlockingIOError` nếu tệp được mở ở chế độ non-blocking. Trước đây, các byte null không mong muốn được thêm vào digest.


Dẫn xuất khóa
-------------

Các thuật toán dẫn xuất khóa và kéo giãn khóa được thiết kế để băm mật khẩu an toàn. Các thuật toán ngây thơ như ``sha1(password)`` không chống được các cuộc tấn công brute-force. Một hàm băm mật khẩu tốt phải có thể điều chỉnh, chậm và bao gồm một `salt <https://en.wikipedia.org/wiki/Salt_%28cryptography%29>`_.


.. function:: pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)

   Hàm này cung cấp hàm dẫn xuất khóa dựa trên mật khẩu 2 của PKCS#5. Hàm sử dụng HMAC làm hàm giả ngẫu nhiên.

   Chuỗi *hash_name* là tên mong muốn của thuật toán băm dùng cho HMAC, ví dụ 'sha1' hoặc 'sha256'. *password* và *salt* được diễn giải là các buffer byte. Ứng dụng và thư viện nên giới hạn *password* ở độ dài hợp lý (ví dụ: 1024). *salt* nên có khoảng 16 byte trở lên, lấy từ một nguồn thích hợp, ví dụ :func:`os.urandom`.

   Số lượng *iterations* nên được chọn dựa trên thuật toán băm và năng lực tính toán. Tính đến năm 2022, người ta khuyến nghị thực hiện hàng trăm nghìn vòng lặp SHA-256. Để biết lý do và cách chọn giá trị phù hợp nhất cho ứng dụng của bạn, hãy đọc *Appendix A.2.2* của NIST-SP-800-132_. Các câu trả lời trong `stackexchange pbkdf2 iterations question <stackexchange pbkdf2 iterations question_>`_ giải thích chi tiết.

   *dklen* là độ dài tính theo byte của khóa được dẫn xuất. Nếu *dklen* là ``None`` thì kích thước digest của thuật toán băm *hash_name* sẽ được sử dụng, ví dụ 64 đối với SHA-512.

   >>> from hashlib import pbkdf2_hmac
   >>> our_app_iters = 500_000  # Dành riêng cho ứng dụng, xem phần trên.
   >>> dk = pbkdf2_hmac('sha256', b'password', b'bad salt' * 2, our_app_iters)
   >>> dk.hex()
   '15530bba69924174860db778f2c6f8104d3aaf9d26241840c8c4a641c8d000a9'

   Hàm chỉ khả dụng khi Python được biên dịch với OpenSSL.

   .. versionadded:: 3.4

   .. versionchanged:: 3.12
      Hàm hiện chỉ khả dụng khi Python được build với OpenSSL. Việc triển khai Python thuần túy chậm đã bị loại bỏ.

.. function:: scrypt(password, *, salt, n, r, p, maxmem=0, dklen=64)

   Hàm này cung cấp hàm dẫn xuất khóa dựa trên mật khẩu scrypt như được định nghĩa trong :rfc:`7914`.

   *password* và *salt* phải là :term:`các đối tượng tương tự bytes <bytes-like object>`. Các ứng dụng và thư viện nên giới hạn *password* ở độ dài hợp lý (ví dụ: 1024). *salt* nên có khoảng 16 byte trở lên từ một nguồn thích hợp, chẳng hạn như :func:`os.urandom`.

   *n* là hệ số chi phí CPU/bộ nhớ, *r* là kích thước khối, *p* là hệ số song song hóa và *maxmem* giới hạn bộ nhớ (OpenSSL 1.1.0 mặc định là 32 MiB). *dklen* là độ dài tính bằng byte của khóa được dẫn xuất.

   .. versionadded:: 3.6


.. _hashlib-blake2:

BLAKE2
------

.. sectionauthor:: Dmitry Chestnykh

.. index::
   single: blake2b, blake2s

BLAKE2_ là một hàm băm mật mã được định nghĩa trong :rfc:`7693` và có hai biến thể:

* **BLAKE2b**, được tối ưu hóa cho các nền tảng 64-bit và tạo ra các digest có kích thước bất kỳ từ 1 đến 64 byte,

* **BLAKE2s**, được tối ưu hóa cho các nền tảng từ 8 đến 32-bit và tạo ra các digest có kích thước bất kỳ từ 1 đến 32 byte.

BLAKE2 hỗ trợ **chế độ keyed** (một phương án thay thế nhanh hơn và đơn giản hơn cho HMAC_), **băm salted**, **cá nhân hóa** và **băm dạng cây**.

Các đối tượng hash từ module này tuân theo API của thư viện chuẩn
:mod:`!hashlib`.


Tạo các đối tượng hash
^^^^^^^^^^^^^^^^^^^^^^

Các đối tượng hash mới được tạo bằng cách gọi các hàm constructor:


.. function:: blake2b(data=b'', *, digest_size=64, key=b'', salt=b'', \
                person=b'', fanout=1, depth=1, leaf_size=0, node_offset=0,  \ node_depth=0, inner_size=0, last_node=False, \ usedforsecurity=True)

.. function:: blake2s(data=b'', *, digest_size=32, key=b'', salt=b'', \
                person=b'', fanout=1, depth=1, leaf_size=0, node_offset=0,  \ node_depth=0, inner_size=0, last_node=False, \ usedforsecurity=True)


Các hàm này trả về các đối tượng hash tương ứng để tính BLAKE2b hoặc BLAKE2s. Chúng có thể nhận các tham số chung sau:

* *data*: phần dữ liệu ban đầu cần băm, phải là
  :term:`bytes-like object`.  Chỉ có thể truyền dưới dạng đối số vị trí.

* *digest_size*: kích thước của digest đầu ra tính bằng byte.

* *key*: khóa dùng để băm có khóa (tối đa 64 byte đối với BLAKE2b, tối đa 32 byte đối với BLAKE2s).

* *salt*: salt dùng cho hashing ngẫu nhiên (tối đa 16 byte đối với BLAKE2b, tối đa 8 byte đối với BLAKE2s).

* *person*: chuỗi cá nhân hóa (tối đa 16 byte đối với BLAKE2b, tối đa 8 byte đối với BLAKE2s).

Bảng sau đây cho biết các giới hạn đối với những tham số chung (tính bằng byte):

+---------+-------------+----------+-----------+-------------+
| Hash    | digest_size | len(key) | len(salt) | len(person) |
+=========+=============+==========+===========+=============+
| BLAKE2b | 64          | 64       | 16        | 16          |
+---------+-------------+----------+-----------+-------------+
| BLAKE2s | 32          | 32       | 8         | 8           |
+---------+-------------+----------+-----------+-------------+

.. note::

    Đặc tả BLAKE2 định nghĩa độ dài cố định cho các tham số salt và personalization, tuy nhiên, để thuận tiện, bản triển khai này chấp nhận các chuỗi byte có kích thước bất kỳ lên đến độ dài được chỉ định. Nếu độ dài của tham số nhỏ hơn độ dài được chỉ định, tham số sẽ được đệm bằng các số 0; do đó, chẳng hạn, ``b'salt'`` và ``b'salt\x00'`` là cùng một giá trị. (Điều này không đúng với *key*.)

Các kích thước này khả dụng dưới dạng module `constants`_ được mô tả bên dưới.

Các hàm constructor cũng chấp nhận những tham số hashing theo cây sau:

* *fanout*: fanout (từ 0 đến 255, bằng 0 nếu không giới hạn, bằng 1 ở chế độ tuần tự).

* *depth*: độ sâu tối đa của cây (từ 1 đến 255, 255 nếu không giới hạn, 1 ở chế độ tuần tự).

* *leaf_size*: độ dài tối đa của lá tính bằng byte (từ 0 đến ``2**32-1``, 0 nếu không giới hạn hoặc ở chế độ tuần tự).

* *node_offset*: độ lệch của nút (từ 0 đến ``2**64-1`` đối với BLAKE2b, từ 0 đến ``2**48-1`` đối với BLAKE2s, 0 đối với lá đầu tiên, ngoài cùng bên trái hoặc ở chế độ tuần tự).

* *node_depth*: độ sâu của nút (từ 0 đến 255, 0 đối với các lá hoặc ở chế độ tuần tự).

* *inner_size*: kích thước digest bên trong (từ 0 đến 64 đối với BLAKE2b, từ 0 đến 32 đối với BLAKE2s, 0 ở chế độ tuần tự).

* *last_node*: giá trị boolean cho biết nút đang được xử lý có phải là nút cuối cùng hay không (``False`` ở chế độ tuần tự).

.. figure:: hashlib-blake2-tree.png
   :alt: Giải thích các tham số của chế độ cây.
   :class: invert-in-dark-mode

Xem mục 2.10 trong `đặc tả BLAKE2 <https://www.blake2.net/blake2_20130129.pdf>`_ để có phần xem xét toàn diện về tree hashing.


.. _`Constants`:

Hằng số
^^^^^^^

.. data:: blake2b.SALT_SIZE
.. data:: blake2s.SALT_SIZE

Độ dài salt (độ dài tối đa được các constructor chấp nhận).


.. data:: blake2b.PERSON_SIZE
.. data:: blake2s.PERSON_SIZE

Độ dài chuỗi personalization (độ dài tối đa được các constructor chấp nhận).


.. data:: blake2b.MAX_KEY_SIZE
.. data:: blake2s.MAX_KEY_SIZE

Kích thước key tối đa.


.. data:: blake2b.MAX_DIGEST_SIZE
.. data:: blake2s.MAX_DIGEST_SIZE

Kích thước digest tối đa mà hàm băm có thể xuất ra.


Ví dụ
^^^^^

Băm đơn giản
""""""""""""

Để tính giá trị băm của một số dữ liệu, trước tiên bạn nên tạo một đối tượng hash bằng cách gọi hàm khởi tạo thích hợp (:func:`blake2b` hoặc
:func:`blake2s`), sau đó cập nhật đối tượng bằng dữ liệu bằng cách gọi :meth:`~hash.update` trên đối tượng và cuối cùng lấy giá trị băm từ đối tượng bằng cách gọi
:meth:`~hash.digest` (hoặc :meth:`~hash.hexdigest` để tạo chuỗi được mã hóa ở dạng thập lục phân).

    >>> from hashlib import blake2b
    >>> h = blake2b()
    >>> h.update(b'Hello world')
    >>> h.hexdigest()
    '6ff843ba685842aa82031d3f53c48b66326df7639a63d128974c5c14f31a0f33343a8c65551134ed1ae0f2b0dd2bb495dc81039e3eeb0aa1bb0388bbeac29183'


Để rút gọn, bạn có thể truyền trực tiếp phần dữ liệu đầu tiên cần cập nhật vào hàm khởi tạo dưới dạng đối số vị trí:

    >>> from hashlib import blake2b
    >>> blake2b(b'Hello world').hexdigest()
    '6ff843ba685842aa82031d3f53c48b66326df7639a63d128974c5c14f31a0f33343a8c65551134ed1ae0f2b0dd2bb495dc81039e3eeb0aa1bb0388bbeac29183'

Bạn có thể gọi :meth:`hash.update` bao nhiêu lần tùy ý để cập nhật hash lặp đi lặp lại:

    >>> from hashlib import blake2b
    >>> items = [b'Hello', b' ', b'world']
    >>> h = blake2b()
    >>> for item in items:
    ...     h.update(item)
    ...
    >>> h.hexdigest()
    '6ff843ba685842aa82031d3f53c48b66326df7639a63d128974c5c14f31a0f33343a8c65551134ed1ae0f2b0dd2bb495dc81039e3eeb0aa1bb0388bbeac29183'


Sử dụng các kích thước giá trị băm khác nhau
""""""""""""""""""""""""""""""""""""""""""""

BLAKE2 có kích thước digest có thể cấu hình lên đến 64 byte đối với BLAKE2b và lên đến 32 byte đối với BLAKE2s. Ví dụ, để thay thế SHA-1 bằng BLAKE2b mà không thay đổi kích thước đầu ra, chúng ta có thể yêu cầu BLAKE2b tạo digest dài 20 byte:

    >>> from hashlib import blake2b
    >>> h = blake2b(digest_size=20)
    >>> h.update(b'Replacing SHA1 with the more secure function')
    >>> h.hexdigest()
    'd24f26cf8de66472d58d4e1b1774b4c9158b1f4c'
    >>> h.digest_size
    20
    >>> len(h.digest())
    20

Các đối tượng hash có kích thước digest khác nhau cho đầu ra hoàn toàn khác nhau (các hash ngắn hơn *không* phải là tiền tố của các hash dài hơn); BLAKE2b và BLAKE2s tạo ra đầu ra khác nhau ngay cả khi độ dài đầu ra giống nhau:

    >>> from hashlib import blake2b, blake2s
    >>> blake2b(digest_size=10).hexdigest()
    '6fa1d8fcfd719046d762'
    >>> blake2b(digest_size=11).hexdigest()
    'eb6ec15daf9546254f0809'
    >>> blake2s(digest_size=10).hexdigest()
    '1bf21a98c78a1c376ae9'
    >>> blake2s(digest_size=11).hexdigest()
    '567004bf96e4a25773ebf4'


Hash có khóa
""""""""""""

Hash có khóa có thể được dùng để xác thực, thay thế nhanh hơn và đơn giản hơn cho `Hash-based message authentication code <https://en.wikipedia.org/wiki/HMAC>`_ (HMAC). BLAKE2 có thể được sử dụng an toàn ở chế độ prefix-MAC nhờ thuộc tính không thể phân biệt (indifferentiability) kế thừa từ BLAKE.

Ví dụ này cho thấy cách lấy mã xác thực 128 bit (được mã hóa dạng hex) cho thông điệp ``b'message data'`` với khóa ``b'pseudorandom key'``::

    >>> from hashlib import blake2b
    >>> h = blake2b(key=b'pseudorandom key', digest_size=16)
    >>> h.update(b'message data')
    >>> h.hexdigest()
    '3d363ff7401e02026f4a4687d4863ced'


Ví dụ thực tế, một ứng dụng web có thể ký đối xứng các cookie được gửi đến người dùng, sau đó xác minh chúng để đảm bảo chúng không bị giả mạo::

    >>> from hashlib import blake2b
    >>> from hmac import compare_digest
    >>>
    >>> SECRET_KEY = b'pseudorandomly generated server secret key'
    >>> AUTH_SIZE = 16
    >>>
    >>> def sign(cookie):
    ...     h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    ...     h.update(cookie)
    ...     return h.hexdigest().encode('utf-8')
    >>>
    >>> def verify(cookie, sig):
    ...     good_sig = sign(cookie)
    ...     return compare_digest(good_sig, sig)
    >>>
    >>> cookie = b'user-alice'
    >>> sig = sign(cookie)
    >>> print("{0},{1}".format(cookie.decode('utf-8'), sig))
    user-alice,b'43b3c982cf697e0c5ab22172d1ca7421'
    >>> verify(cookie, sig)
    True
    >>> verify(b'user-bob', sig)
    False
    >>> verify(cookie, b'0102030405060708090a0b0c0d0e0f00')
    False

Mặc dù có chế độ hash có khóa riêng, tất nhiên BLAKE2 vẫn có thể được sử dụng trong cấu trúc HMAC với module :mod:`hmac`::

    >>> import hmac, hashlib
    >>> m = hmac.new(b'secret key', digestmod=hashlib.blake2s)
    >>> m.update(b'message')
    >>> m.hexdigest()
    'e3c8102868d28b5ff85fc35dda07329970d1a01e273c37481326fe0c861c8142'


Băm ngẫu nhiên
""""""""""""""

Bằng cách đặt tham số *salt*, người dùng có thể đưa tính ngẫu nhiên vào hàm băm. Băm ngẫu nhiên hữu ích để bảo vệ khỏi các cuộc tấn công va chạm nhằm vào hàm băm được sử dụng trong chữ ký số.

    Băm ngẫu nhiên được thiết kế cho các tình huống trong đó một bên, bên chuẩn bị thông điệp, tạo toàn bộ hoặc một phần thông điệp để bên thứ hai, bên ký thông điệp, ký. Nếu bên chuẩn bị thông điệp có thể tìm thấy các va chạm trong hàm băm mật mã (tức là hai thông điệp tạo ra cùng một giá trị băm), họ có thể chuẩn bị các phiên bản có ý nghĩa của thông điệp tạo ra cùng giá trị băm và chữ ký số, nhưng dẫn đến các kết quả khác nhau (ví dụ: chuyển $1,000,000 vào một tài khoản thay vì $10). Các hàm băm mật mã được thiết kế với khả năng chống va chạm là một mục tiêu quan trọng, nhưng việc tập trung hiện nay vào tấn công các hàm băm mật mã có thể khiến một hàm băm mật mã cụ thể cung cấp khả năng chống va chạm thấp hơn dự kiến. Băm ngẫu nhiên cung cấp cho bên ký khả năng bảo vệ bổ sung bằng cách giảm khả năng bên chuẩn bị có thể tạo ra hai hoặc nhiều thông điệp mà cuối cùng cho cùng một giá trị băm trong quá trình tạo chữ ký số --- ngay cả khi việc tìm va chạm cho hàm băm là khả thi trên thực tế. Tuy nhiên, việc sử dụng băm ngẫu nhiên có thể làm giảm mức độ bảo mật mà chữ ký số cung cấp khi bên ký chuẩn bị tất cả các phần của thông điệp.

    (`NIST SP-800-106 "Randomized Hashing for Digital Signatures" <https://csrc.nist.gov/pubs/sp/800/106/final>`_)

Trong BLAKE2, salt được xử lý như một đầu vào chỉ dùng một lần cho hàm băm trong quá trình khởi tạo, thay vì làm đầu vào cho mỗi hàm nén.

.. warning::

    *Băm có salt* (hoặc chỉ băm) với BLAKE2 hoặc bất kỳ hàm băm mật mã đa dụng nào khác, chẳng hạn như SHA-256, không phù hợp để băm mật khẩu. Xem `BLAKE2 FAQ <https://www.blake2.net/#qa>`_ để biết thêm thông tin.
..

    >>> import os
    >>> from hashlib import blake2b
    >>> msg = b'some message'
    >>> # Tính giá trị băm đầu tiên với một salt ngẫu nhiên.
    >>> salt1 = os.urandom(blake2b.SALT_SIZE)
    >>> h1 = blake2b(salt=salt1)
    >>> h1.update(msg)
    >>> # Tính hash thứ hai bằng một salt ngẫu nhiên khác.
    >>> salt2 = os.urandom(blake2b.SALT_SIZE)
    >>> h2 = blake2b(salt=salt2)
    >>> h2.update(msg)
    >>> # Các digest khác nhau.
    >>> h1.digest() != h2.digest()
    True


Cá nhân hóa
"""""""""""

Đôi khi, việc buộc hàm hash tạo ra các digest khác nhau cho cùng một đầu vào vì những mục đích khác nhau là hữu ích. Trích lời các tác giả của hàm hash Skein:

    Chúng tôi khuyến nghị tất cả những người thiết kế ứng dụng nghiêm túc cân nhắc thực hiện việc này; chúng tôi đã thấy nhiều giao thức trong đó một hash được tính ở một phần của giao thức có thể được sử dụng ở một phần hoàn toàn khác, vì hai phép tính hash được thực hiện trên dữ liệu tương tự hoặc có liên quan, và kẻ tấn công có thể buộc ứng dụng làm cho các đầu vào của hash giống nhau. Cá nhân hóa từng hàm hash được sử dụng trong giao thức sẽ lập tức ngăn chặn kiểu tấn công này.

    (`Họ hàm hash Skein <https://www.schneier.com/wp-content/uploads/2016/02/skein.pdf>`_,
    p. 21)

BLAKE2 có thể được cá nhân hóa bằng cách truyền các byte vào đối số *person*::

    >>> from hashlib import blake2b
    >>> FILES_HASH_PERSON = b'MyApp Files Hash'
    >>> BLOCK_HASH_PERSON = b'MyApp Block Hash'
    >>> h = blake2b(digest_size=32, person=FILES_HASH_PERSON)
    >>> h.update(b'the same content')
    >>> h.hexdigest()
    '20d9cd024d4fb086aae819a1432dd2466de12947831b75c5a30cf2676095d3b4'
    >>> h = blake2b(digest_size=32, person=BLOCK_HASH_PERSON)
    >>> h.update(b'the same content')
    >>> h.hexdigest()
    'cf68fb5761b9c44e7878bfb2c4c9aea52264a80b75005e65619778de59f383a3'

Personalization cùng với keyed mode cũng có thể được dùng để tạo ra các key khác nhau từ một key duy nhất.

    >>> from hashlib import blake2s
    >>> from base64 import b64decode, b64encode
    >>> orig_key = b64decode(b'Rm5EPJai72qcK3RGBpW3vPNfZy5OZothY+kHY6h21KM=')
    >>> enc_key = blake2s(key=orig_key, person=b'kEncrypt').digest()
    >>> mac_key = blake2s(key=orig_key, person=b'kMAC').digest()
    >>> print(b64encode(enc_key).decode('utf-8'))
    rbPb15S/Z9t+agffno5wuhB77VbRi6F9Iv2qIxU7WHw=
    >>> print(b64encode(mac_key).decode('utf-8'))
    G9GtHFE1YluXY1zWPlYk1e/nWfu0WSEb0KRcjhDeP/o=

Chế độ cây
""""""""""

Dưới đây là ví dụ về cách hash một cây tối giản với hai nút lá::

       10
      /  \
     00  01

Ví dụ này sử dụng các digest nội bộ 64 byte và trả về digest cuối cùng 32 byte::

    >>> from hashlib import blake2b
    >>>
    >>> FANOUT = 2
    >>> DEPTH = 2
    >>> LEAF_SIZE = 4096
    >>> INNER_SIZE = 64
    >>>
    >>> buf = bytearray(6000)
    >>>
    >>> # Lá trái
    ... h00 = blake2b(buf[0:LEAF_SIZE], fanout=FANOUT, depth=DEPTH,
    ...               leaf_size=LEAF_SIZE, inner_size=INNER_SIZE,
    ...               node_offset=0, node_depth=0, last_node=False)
    >>> # Lá phải
    ... h01 = blake2b(buf[LEAF_SIZE:], fanout=FANOUT, depth=DEPTH,
    ...               leaf_size=LEAF_SIZE, inner_size=INNER_SIZE,
    ...               node_offset=1, node_depth=0, last_node=True)
    >>> # Nút gốc
    ... h10 = blake2b(digest_size=32, fanout=FANOUT, depth=DEPTH,
    ...               leaf_size=LEAF_SIZE, inner_size=INNER_SIZE,
    ...               node_offset=0, node_depth=1, last_node=True)
    >>> h10.update(h00.digest())
    >>> h10.update(h01.digest())
    >>> h10.hexdigest()
    '3ad2a9b37c6070e374c7a8c508fe20ca86b6ed54e286e93a0318e95e881db5aa'

Ghi công
^^^^^^^^

BLAKE2_ được thiết kế bởi *Jean-Philippe Aumasson*, *Samuel Neves*, *Zooko Wilcox-O'Hearn* và *Christian Winnerlein* dựa trên SHA-3_ ứng viên vào vòng chung kết BLAKE_ do *Jean-Philippe Aumasson*, *Luca Henzen*, *Willi Meier* và *Raphael C.-W. Phan* tạo ra.

Nó sử dụng thuật toán cốt lõi từ mật mã ChaCha_ do *Daniel J.  Bernstein* thiết kế.

Triển khai trong stdlib dựa trên module pyblake2_. Module này do *Dmitry Chestnykh* viết, dựa trên bản triển khai C do *Samuel Neves* viết. Tài liệu được sao chép từ pyblake2_ và do *Dmitry Chestnykh* viết.

Mã C đã được *Christian Heimes* viết lại một phần cho Python.

Tuyên bố hiến tặng vào phạm vi công cộng sau đây áp dụng cho cả bản triển khai hàm băm C, mã mở rộng và tài liệu này:

   Trong phạm vi pháp luật cho phép, (các) tác giả đã hiến tặng toàn bộ bản quyền cùng các quyền liên quan và quyền lân cận đối với phần mềm này vào phạm vi công cộng trên toàn thế giới. Phần mềm này được phân phối mà không kèm theo bất kỳ bảo đảm nào.

   Bạn đáng lẽ đã nhận được một bản sao của Tuyên bố Đặt tác phẩm vào Phạm vi công cộng CC0 cùng với phần mềm này. Nếu chưa, hãy xem https://creativecommons.org/publicdomain/zero/1.0/.

Những người sau đây đã hỗ trợ phát triển hoặc đóng góp các thay đổi của họ cho dự án và đưa chúng vào phạm vi công cộng theo Tuyên bố Đặt tác phẩm vào Phạm vi công cộng Creative Commons 1.0 Universal:

* *Alexandr Sokolovskiy*

.. _BLAKE2: https://www.blake2.net
.. _HMAC: https://en.wikipedia.org/wiki/Hash-based_message_authentication_code
.. _BLAKE: https://web.archive.org/web/20200918190133/https://131002.net/blake/
.. _SHA-3: https://en.wikipedia.org/wiki/Secure_Hash_Algorithms
.. _ChaCha: https://cr.yp.to/chacha.html
.. _pyblake2: https://pythonhosted.org/pyblake2/
.. _NIST-SP-800-132: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf
.. _stackexchange pbkdf2 iterations question: https://security.stackexchange.com/questions/3959/recommended-of-iterations-when-using-pbkdf2-sha256/
.. _Attacks on cryptographic hash algorithms: https://en.wikipedia.org/wiki/Cryptographic_hash_function#Attacks_on_cryptographic_hash_algorithms
.. _the FIPS 180-4 standard: https://csrc.nist.gov/pubs/fips/180-4/upd1/final
.. _the FIPS 202 standard: https://csrc.nist.gov/pubs/fips/202/final
.. _HACL\* project: https://github.com/hacl-star/hacl-star
.. _formerly part of FIPS: https://csrc.nist.gov/news/2023/decision-to-revise-fips-180-4


.. _hashlib-seealso:

.. seealso::

   Mô-đun :mod:`hmac`
      Một mô-đun để tạo mã xác thực thông điệp bằng cách sử dụng các hàm băm.

   Mô-đun :mod:`base64`
      Một cách khác để mã hóa các hàm băm nhị phân cho những môi trường không nhị phân.

   https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.180-4.pdf
      Ấn phẩm FIPS 180-4 về các Thuật toán băm an toàn.

   https://csrc.nist.gov/pubs/fips/202/final
      Ấn phẩm FIPS 202 về Tiêu chuẩn SHA-3.

   https://www.blake2.net/
      Trang web chính thức của BLAKE2.

   https://en.wikipedia.org/wiki/Cryptographic_hash_function
      Bài viết trên Wikipedia cung cấp thông tin về những thuật toán đã được xác định là có vấn đề và ý nghĩa của điều đó đối với việc sử dụng chúng.

   https://www.ietf.org/rfc/rfc8018.txt
      PKCS #5: Đặc tả mật mã dựa trên mật khẩu Phiên bản 2.1

   https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf
      Khuyến nghị của NIST về Dẫn xuất khóa dựa trên mật khẩu.

.. _`salt`: https://en.wikipedia.org/wiki/Salt_%28cryptography%29
.. _`BLAKE2 specification`: https://www.blake2.net/blake2_20130129.pdf
.. _`Hash-based message authentication code`: https://en.wikipedia.org/wiki/HMAC
.. _`NIST SP-800-106 "Randomized Hashing for Digital Signatures"`: https://csrc.nist.gov/pubs/sp/800/106/final
.. _`BLAKE2 FAQ`: https://www.blake2.net/#qa
.. _`The Skein Hash Function Family`: https://www.schneier.com/wp-content/uploads/2016/02/skein.pdf
