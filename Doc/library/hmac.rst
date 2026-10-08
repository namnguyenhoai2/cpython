:mod:`!hmac` --- Băm có khóa để xác thực thông điệp
===================================================

.. module:: hmac
   :synopsis: Triển khai thuật toán Băm có khóa để xác thực thông điệp (HMAC)

.. moduleauthor:: Gerhard Häring <ghaering@users.sourceforge.net>
.. sectionauthor:: Gerhard Häring <ghaering@users.sourceforge.net>

**Mã nguồn:** :source:`Lib/hmac.py`

--------------

Module này triển khai thuật toán HMAC như được mô tả trong :rfc:`2104`. Giao diện cho phép sử dụng bất kỳ hàm băm nào có kích thước digest *cố định*. Cụ thể, không thể sử dụng các hàm đầu ra có thể mở rộng như SHAKE-128 hoặc SHAKE-256 với HMAC.


.. function:: new(key, msg=None, digestmod)

   Trả về một đối tượng hmac mới. *key* là đối tượng bytes hoặc bytearray chứa khóa bí mật. Nếu có *msg*, lệnh gọi phương thức ``update(msg)`` sẽ được thực hiện. *digestmod* là tên digest, hàm khởi tạo digest hoặc module dùng cho đối tượng HMAC. Nó có thể là bất kỳ tên nào phù hợp với :func:`hashlib.new`. Mặc dù nằm ở vị trí đối số này, tham số này là bắt buộc.

   .. versionchanged:: 3.4
      Tham số *key* có thể là một đối tượng bytes hoặc bytearray. Tham số *msg* có thể thuộc bất kỳ kiểu nào được :mod:`hashlib` hỗ trợ. Tham số *digestmod* có thể là tên của một thuật toán băm.

   .. versionchanged:: 3.8
      Đối số *digestmod* hiện là bắt buộc. Hãy truyền đối số này dưới dạng đối số từ khóa để tránh bất tiện khi bạn không có *msg* ban đầu.


.. function:: digest(key, msg, digest)

   Trả về digest của *msg* cho secret *key* và *digest* đã cho. Hàm này tương đương với ``HMAC(key, msg, digest).digest()``, nhưng sử dụng triển khai C được tối ưu hóa hoặc triển khai inline, nhanh hơn đối với các message vừa với bộ nhớ. Các tham số *key*, *msg* và *digest* có cùng ý nghĩa như trong :func:`~hmac.new`.

   Theo chi tiết triển khai của CPython, triển khai C được tối ưu hóa chỉ được sử dụng khi *digest* là chuỗi và là tên của một thuật toán digest được OpenSSL hỗ trợ.

   .. versionadded:: 3.7


.. class:: HMAC

   Một đối tượng HMAC có các phương thức sau:

.. method:: HMAC.update(msg)

   Cập nhật đối tượng hmac với *msg*. Các lần gọi lặp lại tương đương với một lần gọi duy nhất có phần nối của tất cả các đối số: ``m.update(a); m.update(b)`` tương đương với ``m.update(a + b)``.

   .. versionchanged:: 3.4
      Tham số *msg* có thể thuộc bất kỳ kiểu nào được :mod:`hashlib` hỗ trợ.


.. method:: HMAC.digest()

   Trả về digest của các byte đã được truyền cho phương thức :meth:`update` cho đến thời điểm hiện tại. Đối tượng bytes này sẽ có cùng độ dài với *digest_size* của digest được truyền cho hàm khởi tạo. Nó có thể chứa các byte không phải ASCII, bao gồm cả byte NUL.

   .. warning::

      Khi so sánh đầu ra của :meth:`digest` với một digest được cung cấp từ bên ngoài trong quy trình xác minh, bạn nên sử dụng
      hàm :func:`compare_digest` thay vì toán tử ``==`` để giảm mức độ dễ bị tấn công theo thời gian.


.. method:: HMAC.hexdigest()

   Tương tự như :meth:`digest`, ngoại trừ việc digest được trả về dưới dạng chuỗi có độ dài gấp đôi và chỉ chứa các chữ số thập lục phân. Có thể dùng cách này để trao đổi giá trị an toàn qua email hoặc trong các môi trường phi nhị phân khác.

   .. warning::

      Khi so sánh đầu ra của :meth:`hexdigest` với digest được cung cấp từ bên ngoài trong quy trình xác minh, bạn nên sử dụng
      hàm :func:`compare_digest` thay vì toán tử ``==`` để giảm mức độ dễ bị tấn công theo thời gian.


.. method:: HMAC.copy()

   Trả về một bản sao ("clone") của đối tượng hmac. Có thể dùng bản sao này để tính digest một cách hiệu quả cho các chuỗi có cùng chuỗi con ban đầu.


Một đối tượng hash có các thuộc tính sau:

.. attribute:: HMAC.digest_size

   Kích thước tính theo byte của digest HMAC thu được.

.. attribute:: HMAC.block_size

   Kích thước khối nội bộ của thuật toán băm, tính bằng byte.

   .. versionadded:: 3.4

.. attribute:: HMAC.name

   Tên chuẩn của HMAC này, luôn viết thường, ví dụ ``hmac-md5``.

   .. versionadded:: 3.4


.. versionchanged:: 3.10
   Đã xóa các thuộc tính chưa được ghi lại ``HMAC.digest_cons``, ``HMAC.inner`` và ``HMAC.outer``.

Mô-đun này cũng cung cấp hàm trợ giúp sau:

.. function:: compare_digest(a, b)

   Trả về ``a == b``. Hàm này sử dụng một phương pháp được thiết kế để ngăn việc phân tích thời gian bằng cách tránh hành vi đoản mạch dựa trên nội dung, khiến hàm phù hợp cho mật mã. *a* và *b* phải cùng một kiểu: либо :class:`str` (chỉ ASCII, chẳng hạn như giá trị được trả về bởi
   :meth:`HMAC.hexdigest`), hoặc một :term:`bytes-like object`.

   .. note::

      Nếu *a* và *b* có độ dài khác nhau, hoặc nếu xảy ra lỗi, về lý thuyết một cuộc tấn công timing có thể tiết lộ thông tin về kiểu và độ dài của *a* và *b*—nhưng không tiết lộ giá trị của chúng.

   .. versionadded:: 3.3

   .. versionchanged:: 3.10

      Hàm này sử dụng ``CRYPTO_memcmp()`` của OpenSSL ở bên trong khi có sẵn.


.. seealso::

   Mô-đun :mod:`hashlib`
      Mô-đun Python cung cấp các hàm băm bảo mật.
