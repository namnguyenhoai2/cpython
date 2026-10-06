:mod:`!base64` --- Mã hóa dữ liệu Base16, Base32, Base64, Base85
================================================================

.. module:: base64
   :synopsis: RFC 4648: Mã hóa dữ liệu Base16, Base32, Base64; Base85 và Ascii85

**Mã nguồn:** :source:`Lib/base64.py`

.. index::
   pair: base64; encoding
   single: MIME; base64 encoding

--------------

Mô-đun này cung cấp các hàm để mã hóa dữ liệu nhị phân thành các ký tự ASCII có thể in được và giải mã các kiểu mã hóa đó trở lại thành dữ liệu nhị phân. Các kiểu mã hóa này bao gồm :ref:`được chỉ định trong <base64-rfc-4648>`
:rfc:`4648` (Base64, Base32 và Base16), :ref:`kiểu mã hóa Base85 <base64-base-85>` được chỉ định trong `PDF 2.0 <https://pdfa.org/resource/iso-32000-2/>`_, cùng các biến thể Base85 không theo tiêu chuẩn được sử dụng ở những nơi khác.

Mô-đun này cung cấp hai giao diện. Giao diện hiện đại hỗ trợ mã hóa :term:`các đối tượng bytes-like <bytes-like object>` thành ASCII
:class:`bytes`, và giải mã :term:`các đối tượng bytes-like <bytes-like object>` hoặc chuỗi chứa ASCII thành :class:`bytes`. Cả hai bảng chữ cái base-64 được định nghĩa trong :rfc:`4648` (thông thường và an toàn cho URL cũng như hệ thống tệp) đều được hỗ trợ.

:ref:`Giao diện cũ <base64-legacy>` không hỗ trợ giải mã từ chuỗi, nhưng cung cấp các hàm để mã hóa và giải mã đến và đi từ :term:`đối tượng tệp <file object>`. Giao diện này chỉ hỗ trợ bảng chữ cái Base64 tiêu chuẩn và thêm dòng mới sau mỗi 76 ký tự theo :rfc:`2045`. Lưu ý rằng nếu bạn đang tìm kiếm hỗ trợ :rfc:`2045`, có lẽ bạn nên xem xét package :mod:`email`.


.. versionchanged:: 3.3
   Các chuỗi Unicode chỉ chứa ASCII hiện được các hàm giải mã của giao diện hiện đại chấp nhận.

.. versionchanged:: 3.4
   Mọi :term:`đối tượng tương tự bytes <bytes-like object>` hiện được tất cả các hàm mã hóa và giải mã trong module này chấp nhận. Đã bổ sung hỗ trợ Ascii85/Base85.


.. _base64-rfc-4648:

Mã hóa RFC 4648
---------------

Các phương thức mã hóa :rfc:`4648` phù hợp để mã hóa dữ liệu nhị phân, ताकि dữ liệu có thể được gửi an toàn qua email, được sử dụng làm một phần của URL hoặc được đưa vào một phần của yêu cầu HTTP POST.

.. function:: b64encode(s, altchars=None)

   Mã hóa :term:`bytes-like object` *s* bằng Base64 và trả về phần đã mã hóa
   :class:`bytes`.

   *altchars* tùy chọn phải là một :term:`bytes-like object` có độ dài 2, chỉ định một bảng chữ cái thay thế cho các ký tự ``+`` và ``/``. Điều này cho phép ứng dụng, chẳng hạn, tạo ra các chuỗi Base64 an toàn cho URL hoặc hệ thống tệp. Giá trị mặc định là ``None``, trong đó bảng chữ cái Base64 tiêu chuẩn được sử dụng.

   Có thể assert hoặc raise một :exc:`ValueError` nếu độ dài của *altchars* không phải là 2. Raises a
   :exc:`TypeError` nếu *altchars* không phải là một :term:`bytes-like object`.


.. function:: b64decode(s, altchars=None, validate=False)

   Giải mã :term:`bytes-like object` được mã hóa Base64 hoặc chuỗi ASCII *s* và trả về :class:`bytes` đã được giải mã.

   *altchars* tùy chọn phải là một :term:`bytes-like object` hoặc chuỗi ASCII có độ dài 2, chỉ định bảng chữ cái thay thế được sử dụng thay cho các ký tự ``+`` và ``/``.

   Một ngoại lệ :exc:`binascii.Error` được raise nếu *s* có padding không đúng.

   Nếu *validate* là ``False`` (giá trị mặc định), các ký tự không thuộc bảng chữ cái base-64 thông thường hoặc bảng chữ cái thay thế sẽ bị loại bỏ trước khi kiểm tra padding. Nếu *validate* là ``True``, các ký tự không thuộc bảng chữ cái này trong đầu vào sẽ dẫn đến một
   :exc:`binascii.Error`.

   Để biết thêm thông tin về kiểm tra base64 nghiêm ngặt, hãy xem :func:`binascii.a2b_base64`

   Có thể assert hoặc raise một :exc:`ValueError` nếu độ dài của *altchars* không phải là 2.

.. function:: standard_b64encode(s)

   Mã hóa :term:`bytes-like object` *s* bằng bảng chữ cái Base64 tiêu chuẩn và trả về :class:`bytes` đã được mã hóa.


.. function:: standard_b64decode(s)

   Giải mã :term:`bytes-like object` hoặc chuỗi ASCII *s* bằng bảng chữ cái Base64 tiêu chuẩn và trả về :class:`bytes` đã được giải mã.


.. function:: urlsafe_b64encode(s)

   Mã hóa :term:`bytes-like object` *s* bằng bảng chữ cái an toàn cho URL và hệ thống tệp, trong đó ``-`` được thay cho ``+`` và ``_`` được thay cho ``/`` trong bảng chữ cái Base64 tiêu chuẩn, rồi trả về :class:`bytes` đã được mã hóa. Kết quả vẫn có thể chứa ``=``.


.. function:: urlsafe_b64decode(s)

   Giải mã :term:`bytes-like object` hoặc chuỗi ASCII *s* bằng bảng chữ cái an toàn cho URL và hệ thống tệp, trong đó ``-`` được dùng thay cho ``+`` và ``_`` được dùng thay cho ``/`` trong bảng chữ cái Base64 tiêu chuẩn, rồi trả về chuỗi đã giải mã
   :class:`bytes`.


.. function:: b32encode(s)

   Mã hóa :term:`bytes-like object` *s* bằng Base32 và trả về :class:`bytes` đã được mã hóa.


.. function:: b32decode(s, casefold=False, map01=None)

   Giải mã :term:`bytes-like object` được mã hóa bằng Base32 hoặc chuỗi ASCII *s* rồi trả về :class:`bytes` đã được giải mã.

   *casefold* tùy chọn là một cờ chỉ định liệu bảng chữ cái viết thường có được chấp nhận làm đầu vào hay không. Vì mục đích bảo mật, giá trị mặc định là ``False``.

   :rfc:`4648` cho phép ánh xạ tùy chọn chữ số 0 (zero) thành chữ O (oh), và ánh xạ tùy chọn chữ số 1 (one) thành chữ I (eye) hoặc chữ L (el). Đối số tùy chọn *map01* khi không phải là ``None``, chỉ định chữ cái mà chữ số 1 sẽ được ánh xạ thành (khi *map01* không phải là ``None``, chữ số 0 luôn được ánh xạ thành chữ O). Vì mục đích bảo mật, giá trị mặc định là ``None``, để 0 và 1 không được phép xuất hiện trong đầu vào.

   Một :exc:`binascii.Error` được phát sinh nếu *s* có phần đệm không đúng hoặc nếu đầu vào chứa các ký tự không thuộc bảng chữ cái.


.. function:: b32hexencode(s)

   Tương tự như :func:`b32encode` nhưng sử dụng Extended Hex Alphabet, như được định nghĩa trong
   :rfc:`4648`.

   .. versionadded:: 3.10


.. function:: b32hexdecode(s, casefold=False)

   Tương tự như :func:`b32decode` nhưng sử dụng Extended Hex Alphabet, như được định nghĩa trong
   :rfc:`4648`.

   Phiên bản này không cho phép ánh xạ chữ số 0 (zero) thành chữ O (oh) và chữ số 1 (one) thành chữ I (eye) hoặc chữ L (el); tất cả các ký tự này đều nằm trong Extended Hex Alphabet và không thể thay thế cho nhau.

   .. versionadded:: 3.10


.. function:: b16encode(s)

   Mã hóa :term:`bytes-like object` *s* bằng Base16 và trả về :class:`bytes` đã được mã hóa.


.. function:: b16decode(s, casefold=False)

   Giải mã :term:`bytes-like object` được mã hóa Base16 hoặc chuỗi ASCII *s* và trả về :class:`bytes` đã giải mã.

   *casefold* tùy chọn là một cờ chỉ định liệu bảng chữ cái viết thường có được chấp nhận làm đầu vào hay không. Vì mục đích bảo mật, giá trị mặc định là ``False``.

   Một :exc:`binascii.Error` được phát sinh nếu *s* có phần đệm không đúng hoặc nếu đầu vào chứa các ký tự không thuộc bảng chữ cái.

.. _base64-base-85:

Mã hóa Base85
-------------

Mã hóa Base85 là một họ thuật toán biểu diễn bốn byte bằng năm ký tự ASCII. Ban đầu được triển khai trong tiện ích Unix ``btoa(1)``, một phiên bản của nó sau đó được Adobe áp dụng trong ngôn ngữ PostScript và được chuẩn hóa trong PDF 2.0 (ISO 32000-2). Phiên bản này, ở cả biến thể ``btoa`` và PDF, được triển khai bởi
:func:`a85encode`.

Một phiên bản riêng biệt sử dụng bộ ký tự đầu ra khác được định nghĩa như một trò đùa Cá tháng Tư trong :rfc:`1924`, nhưng hiện được Git và các phần mềm khác sử dụng. Phiên bản này được triển khai bởi :func:`b85encode`.

Cuối cùng, một phiên bản thứ ba sử dụng một bộ ký tự đầu ra khác nữa, được thiết kế để an toàn khi đưa vào các chuỗi trong ngôn ngữ lập trình, được ZeroMQ định nghĩa và triển khai tại đây bởi :func:`z85encode`.

Các hàm có trong mô-đun này khác nhau về cách xử lý những điều sau:

* Có bao gồm và yêu cầu các dấu ``<~`` và ``~>`` bao quanh hay không.
* Có chia đầu vào thành nhiều dòng hay không.
* Tập hợp các ký tự ASCII được sử dụng để mã hóa.
* Cách mã hóa rút gọn các chuỗi dấu cách và byte rỗng.
* Cách mã hóa các byte đệm bằng 0 được thêm vào đầu vào.

Hãy tham khảo tài liệu của từng hàm để biết thêm thông tin.

.. function:: a85encode(b, *, foldspaces=False, wrapcol=0, pad=False, adobe=False)

   Mã hóa :term:`bytes-like object` *b* bằng Ascii85 và trả về :class:`bytes` đã mã hóa.

   *foldspaces* là một cờ tùy chọn sử dụng chuỗi ngắn đặc biệt 'y' thay cho 4 dấu cách liên tiếp (ASCII 0x20), như được 'btoa' hỗ trợ. Tính năng này không được hỗ trợ bởi encoding chuẩn được sử dụng trong PDF.

   *wrapcol* kiểm soát việc có thêm các ký tự newline (``b'\n'``) vào output hay không. Nếu giá trị này khác 0, mỗi dòng output sẽ có nhiều nhất số ký tự tương ứng với giá trị này, không tính newline ở cuối.

   *pad* kiểm soát việc phần đệm bằng số 0 được áp dụng vào cuối input có được giữ lại hoàn toàn trong encoding output hay không, như được thực hiện bởi ``btoa``, tạo ra output có số byte là bội số chính xác của 5. Đây không phải là một phần của encoding chuẩn được sử dụng trong PDF, vì nó không bảo toàn độ dài của dữ liệu.

   *adobe* kiểm soát việc chuỗi byte đã mã hóa có được bao quanh bởi ``<~`` và ``~>`` hay không, như trong một string literal base-85 của PostScript. Lưu ý rằng mặc dù các stream ASCII85Decode trong tài liệu PDF *phải* được kết thúc bằng ``~>``, chúng *không được* sử dụng ``<~`` ở đầu.

   .. versionadded:: 3.4


.. function:: a85decode(b, *, foldspaces=False, adobe=False, ignorechars=b' \t\n\r\v')

   Giải mã :term:`bytes-like object` được mã hóa bằng Ascii85 hoặc chuỗi ASCII *b* và trả về :class:`bytes` đã giải mã.

   *foldspaces* là một cờ chỉ định liệu chuỗi ngắn 'y' có được chấp nhận như cách viết tắt cho 4 dấu cách liên tiếp (ASCII 0x20) hay không. Tính năng này không được hỗ trợ bởi encoding Ascii85 chuẩn được sử dụng trong PDF và PostScript.

   *adobe* kiểm soát việc các dấu ``<~`` và ``~>`` có xuất hiện hay không. Mặc dù ``<~`` ở đầu không bắt buộc, dữ liệu đầu vào phải kết thúc bằng ``~>``, nếu không sẽ phát sinh :exc:`ValueError`.

   *ignorechars* phải là một chuỗi byte chứa các ký tự cần bỏ qua trong dữ liệu đầu vào. Chuỗi này chỉ nên chứa các ký tự khoảng trắng và theo mặc định chứa tất cả ký tự khoảng trắng trong ASCII.

   .. versionadded:: 3.4


.. function:: b85encode(b, pad=False)

   Mã hóa :term:`bytes-like object` *b* bằng base85 (được sử dụng chẳng hạn trong các binary diff kiểu git) và trả về :class:`bytes` đã mã hóa.

   Dữ liệu đầu vào được đệm bằng ``b'\0'`` để độ dài của nó là bội số của 4 byte trước khi mã hóa. Nếu *pad* là true, tất cả các ký tự tạo ra đều được giữ lại trong đầu ra, đầu ra này luôn có độ dài là bội số của 5 byte, vì vậy độ dài dữ liệu có thể không được giữ nguyên khi giải mã.

   .. versionadded:: 3.4


.. function:: b85decode(b)

   Giải mã :term:`bytes-like object` được mã hóa bằng base85 hoặc chuỗi ASCII *b* và trả về :class:`bytes` đã giải mã.

   .. versionadded:: 3.4


.. function:: z85encode(s)

   Mã hóa :term:`bytes-like object` *s* bằng Z85 (được sử dụng trong ZeroMQ) và trả về :class:`bytes` đã mã hóa.

   `ZeroMQ specification <https://rfc.zeromq.org/spec/32/>`_ yêu cầu độ dài của dữ liệu được mã hóa bằng Z85 phải là bội số của 5 byte. Để tạo các khung dữ liệu tuân thủ đặc tả, bạn phải đệm dữ liệu đầu vào của hàm này thành bội số của 4 byte.

   .. versionadded:: 3.13


.. function:: z85decode(s)

   Giải mã chuỗi Z85-encoded :term:`bytes-like object` hoặc ASCII *s* và trả về :class:`bytes` đã được giải mã.

   .. versionadded:: 3.13


.. _base64-legacy:

Giao diện cũ
------------

.. function:: decode(input, output)

   Giải mã nội dung của tệp *input* nhị phân và ghi dữ liệu nhị phân thu được vào tệp *output*. *input* và *output* phải là :term:`các đối tượng tệp <file object>`. *input* sẽ được đọc cho đến khi ``input.readline()`` trả về một đối tượng bytes rỗng.


.. function:: decodebytes(s)

   Giải mã :term:`bytes-like object` *s*, trong đó phải chứa một hoặc nhiều dòng dữ liệu được mã hóa base64, và trả về :class:`bytes` đã được giải mã.

   .. versionadded:: 3.1


.. function:: encode(input, output)

   Mã hóa nội dung của tệp *input* nhị phân và ghi dữ liệu được mã hóa base64 thu được vào tệp *output*. *input* và *output* phải là :term:`các đối tượng tệp <file object>`. *input* sẽ được đọc cho đến khi ``input.read()`` trả về một đối tượng bytes rỗng. :func:`encode` chèn một ký tự xuống dòng (``b'\n'``) sau mỗi 76 byte của đầu ra, đồng thời đảm bảo rằng đầu ra luôn kết thúc bằng một ký tự xuống dòng, theo :rfc:`2045` (MIME).


.. function:: encodebytes(s)

   Mã hóa :term:`bytes-like object` *s*, có thể chứa dữ liệu nhị phân tùy ý, và trả về :class:`bytes` chứa dữ liệu được mã hóa base64, với các ký tự xuống dòng (``b'\n'``) được chèn sau mỗi 76 byte của đầu ra, đồng thời đảm bảo có một ký tự xuống dòng ở cuối, theo :rfc:`2045` (MIME).

   .. versionadded:: 3.1


Ví dụ về cách sử dụng module:

   >>> import base64
   >>> encoded = base64.b64encode(b'data to be encoded')
   >>> encoded
   b'ZGF0YSB0byBiZSBlbmNvZGVk'
   >>> data = base64.b64decode(encoded)
   >>> data
   b'data to be encoded'

.. _base64-security:

Các cân nhắc về bảo mật
-----------------------

Một phần về các cân nhắc bảo mật mới đã được thêm vào :rfc:`4648` (mục 12); bạn nên xem lại phần bảo mật đối với mọi mã được deploy lên môi trường production.

.. seealso::

   Module :mod:`binascii`
      Module hỗ trợ chuyển đổi ASCII sang binary và binary sang ASCII.

   :rfc:`1521` - MIME (Multipurpose Internet Mail Extensions) Phần một: Cơ chế chỉ định và mô tả định dạng của nội dung thư Internet
      Mục 5.2, "Base64 Content-Transfer-Encoding," cung cấp định nghĩa về mã hóa base64.

   `Định dạng tài liệu portable ISO 32000-2 - Phần 2: PDF 2.0 <https://pdfa.org/resource/iso-32000-2/>`_
      Mục 7.4.3, "ASCII85Decode Filter," cung cấp định nghĩa về encoding Ascii85 được sử dụng trong PDF và PostScript, bao gồm tập ký tự đầu ra và chi tiết về việc bảo toàn độ dài dữ liệu bằng cách đệm bằng số không và các nhóm đầu ra một phần.

   `ZeroMQ RFC 32/Z85 <https://rfc.zeromq.org/spec/32/>`_
      Phần "Formal Specification" cung cấp tập ký tự được sử dụng trong Z85.

.. _`PDF 2.0`: https://pdfa.org/resource/iso-32000-2/
.. _`ZeroMQ specification`: https://rfc.zeromq.org/spec/32/
.. _`ISO 32000-2 Portable document format - Part 2: PDF 2.0`: https://pdfa.org/resource/iso-32000-2/
.. _`ZeroMQ RFC 32/Z85`: https://rfc.zeromq.org/spec/32/
