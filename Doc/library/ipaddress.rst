:mod:`!ipaddress` --- Thư viện thao tác IPv4/IPv6
=================================================

.. module:: ipaddress
   :synopsis: Thư viện thao tác IPv4/IPv6.

.. moduleauthor:: Peter Moody

**Mã nguồn:** :source:`Lib/ipaddress.py`

--------------

:mod:`!ipaddress` cung cấp các khả năng để tạo, thao tác và làm việc với các địa chỉ và mạng IPv4 và IPv6.

Các hàm và lớp trong mô-đun này giúp dễ dàng thực hiện nhiều tác vụ liên quan đến địa chỉ IP, bao gồm kiểm tra xem hai host có nằm trên cùng một subnet hay không, lặp qua tất cả host trong một subnet cụ thể, kiểm tra xem một chuỗi có biểu diễn một địa chỉ IP hoặc định nghĩa mạng hợp lệ hay không, v.v.

Đây là tài liệu tham khảo đầy đủ về API của mô-đun—để xem phần tổng quan và giới thiệu, hãy xem
:ref:`ipaddress-howto`.

.. versionadded:: 3.3

.. testsetup::

   import ipaddress
   from ipaddress import (
       ip_network, IPv4Address, IPv4Interface, IPv4Network,
   )

Các hàm factory tiện lợi
------------------------

Mô-đun :mod:`!ipaddress` cung cấp các hàm factory để thuận tiện tạo địa chỉ IP, mạng và interface:

.. function:: ip_address(address)

   Trả về đối tượng :class:`IPv4Address` hoặc :class:`IPv6Address` tùy thuộc vào địa chỉ IP được truyền dưới dạng đối số. Có thể cung cấp địa chỉ IPv4 hoặc IPv6; theo mặc định, các số nguyên nhỏ hơn ``2**32`` sẽ được coi là IPv4. Một :exc:`ValueError` sẽ được phát sinh nếu *address* không biểu diễn một địa chỉ IPv4 hoặc IPv6 hợp lệ.

   >>> ipaddress.ip_address('192.168.0.1')
   IPv4Address('192.168.0.1')
   >>> ipaddress.ip_address('2001:db8::')
   IPv6Address('2001:db8::')


.. function:: ip_network(address, strict=True)

   Trả về đối tượng :class:`IPv4Network` hoặc :class:`IPv6Network` tùy thuộc vào địa chỉ IP được truyền dưới dạng đối số. *address* là một chuỗi hoặc số nguyên biểu diễn mạng IP. Có thể cung cấp mạng IPv4 hoặc IPv6; theo mặc định, các số nguyên nhỏ hơn ``2**32`` sẽ được coi là IPv4. *strict* được truyền cho constructor :class:`IPv4Network` hoặc :class:`IPv6Network`. Một
   :exc:`ValueError` sẽ được phát sinh nếu *address* không biểu diễn một địa chỉ IPv4 hoặc IPv6 hợp lệ, hoặc nếu mạng có các bit máy chủ được thiết lập.

   >>> ipaddress.ip_network('192.168.0.0/28')
   IPv4Network('192.168.0.0/28')


.. function:: ip_interface(address)

   Trả về đối tượng :class:`IPv4Interface` hoặc :class:`IPv6Interface` tùy thuộc vào địa chỉ IP được truyền dưới dạng đối số. *address* là một chuỗi hoặc số nguyên biểu diễn địa chỉ IP. Có thể cung cấp địa chỉ IPv4 hoặc IPv6; theo mặc định, các số nguyên nhỏ hơn ``2**32`` sẽ được coi là IPv4. Một
   :exc:`ValueError` sẽ được phát sinh nếu *address* không biểu diễn một địa chỉ IPv4 hoặc IPv6 hợp lệ.

Một hạn chế của các hàm tiện ích này là việc cần xử lý cả định dạng IPv4 và IPv6 khiến các thông báo lỗi cung cấp rất ít thông tin về lỗi cụ thể, vì các hàm không biết định dạng IPv4 hay IPv6 được dự định sử dụng. Có thể nhận được báo cáo lỗi chi tiết hơn bằng cách gọi trực tiếp các constructor của lớp tương ứng với từng phiên bản.


Địa chỉ IP
----------

Đối tượng địa chỉ
^^^^^^^^^^^^^^^^^

Các đối tượng :class:`IPv4Address` và :class:`IPv6Address` có nhiều thuộc tính chung. Một số thuộc tính chỉ có ý nghĩa đối với địa chỉ IPv6 cũng được triển khai cho các đối tượng :class:`IPv4Address`, giúp việc viết mã xử lý đúng cả hai phiên bản IP trở nên dễ dàng hơn. Các đối tượng địa chỉ là
:term:`hashable`, nên có thể được dùng làm khóa trong dictionary.

.. class:: IPv4Address(address)

   Tạo một địa chỉ IPv4. :exc:`AddressValueError` sẽ được phát sinh nếu *address* không phải là một địa chỉ IPv4 hợp lệ.

   Các dạng sau đây tạo thành một địa chỉ IPv4 hợp lệ:

   1. Một chuỗi ở dạng ký hiệu thập phân có dấu chấm, gồm bốn số nguyên thập phân trong phạm vi từ 0--255, bao gồm cả hai đầu mút, được phân tách bằng dấu chấm (ví dụ: ``192.168.0.1``). Mỗi số nguyên biểu diễn một octet (byte) trong địa chỉ. Không chấp nhận các số 0 đứng đầu để tránh nhầm lẫn với ký hiệu bát phân.
   2. Một số nguyên vừa trong 32 bit.
   3. Một số nguyên được đóng gói vào một đối tượng :class:`bytes` có độ dài 4 (octet có ý nghĩa lớn nhất đứng trước).

   >>> ipaddress.IPv4Address('192.168.0.1')
   IPv4Address('192.168.0.1')
   >>> ipaddress.IPv4Address(3232235521)
   IPv4Address('192.168.0.1')
   >>> ipaddress.IPv4Address(b'\xC0\xA8\x00\x01')
   IPv4Address('192.168.0.1')

   .. versionchanged:: 3.8

      Các số 0 ở đầu được chấp nhận, kể cả trong những trường hợp không rõ ràng trông giống ký hiệu bát phân.

   .. versionchanged:: 3.9.5

      Các số 0 ở đầu không còn được chấp nhận và bị xem là lỗi. Các chuỗi địa chỉ IPv4 hiện được phân tích nghiêm ngặt như glibc
      :func:`~socket.inet_pton`.

   .. attribute:: version

      Số phiên bản thích hợp: ``4`` cho IPv4, ``6`` cho IPv6.

      .. versionchanged:: 3.14

         Có sẵn trên class.

   .. attribute:: max_prefixlen

      Tổng số bit trong biểu diễn địa chỉ của phiên bản này: ``32`` cho IPv4, ``128`` cho IPv6.

      Prefix xác định số bit đứng đầu trong một địa chỉ được so sánh để xác định địa chỉ đó có thuộc một mạng hay không.

      .. versionchanged:: 3.14

         Có sẵn trên class.

   .. attribute:: compressed
   .. attribute:: exploded

      Biểu diễn chuỗi theo ký hiệu thập phân có dấu chấm. Các số 0 ở đầu không bao giờ được đưa vào biểu diễn.

      Vì IPv4 không định nghĩa ký hiệu rút gọn cho các địa chỉ có octet được đặt thành 0, hai thuộc tính này luôn giống ``str(addr)`` đối với địa chỉ IPv4. Việc cung cấp các thuộc tính này giúp dễ dàng viết mã hiển thị có thể xử lý cả địa chỉ IPv4 và IPv6.

   .. attribute:: packed

      Biểu diễn nhị phân của địa chỉ này - một đối tượng :class:`bytes` có độ dài phù hợp (octet có trọng số cao nhất đứng trước). Địa chỉ IPv4 có 4 byte và IPv6 có 16 byte.

   .. attribute:: reverse_pointer

      Tên của bản ghi DNS ngược PTR cho địa chỉ IP, ví dụ:::

          >>> ipaddress.ip_address("127.0.0.1").reverse_pointer
          '1.0.0.127.in-addr.arpa'
          >>> ipaddress.ip_address("2001:db8::1").reverse_pointer
          '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa'

      Đây là tên có thể được sử dụng để thực hiện tra cứu PTR, không phải chính hostname được phân giải.

      .. versionadded:: 3.5

   .. attribute:: is_multicast

      ``True`` nếu địa chỉ được dành riêng cho mục đích sử dụng multicast. Xem
      :RFC:`3171` (đối với IPv4) hoặc :RFC:`2373` (đối với IPv6).

   .. attribute:: is_private

      ``True`` nếu địa chỉ được xác định là không thể truy cập trên phạm vi toàn cầu bởi iana-ipv4-special-registry_ (đối với IPv4) hoặc iana-ipv6-special-registry_ (đối với IPv6), với các ngoại lệ sau:

      * ``is_private`` là ``False`` đối với không gian địa chỉ dùng chung (``100.64.0.0/10``)
      * Đối với các địa chỉ IPv6 ánh xạ IPv4, giá trị ``is_private`` được xác định theo ngữ nghĩa của các địa chỉ IPv4 bên dưới và điều kiện sau được áp dụng (xem :attr:`IPv6Address.ipv4_mapped`)::

            address.is_private == address.ipv4_mapped.is_private

      ``is_private`` có giá trị trái ngược với :attr:`is_global`, ngoại trừ không gian địa chỉ dùng chung (dải ``100.64.0.0/10``), trong đó cả hai đều là ``False``.

      .. versionchanged:: 3.13

         Đã sửa một số trường hợp dương tính giả và âm tính giả.

         * ``192.0.0.0/24`` được coi là riêng tư, ngoại trừ ``192.0.0.9/32`` và ``192.0.0.10/32`` (trước đây: chỉ phạm vi con ``192.0.0.0/29`` được coi là riêng tư).
         * ``64:ff9b:1::/48`` được coi là riêng tư.
         * ``2002::/16`` được coi là riêng tư.
         * Có các ngoại lệ trong ``2001::/23`` (nếu không thì được coi là riêng tư): ``2001:1::1/128``, ``2001:1::2/128``, ``2001:3::/32``, ``2001:4:112::/48``, ``2001:20::/28``, ``2001:30::/28``. Các ngoại lệ không được coi là riêng tư.

   .. attribute:: is_global

      ``True`` nếu địa chỉ được iana-ipv4-special-registry_ (đối với IPv4) hoặc iana-ipv6-special-registry_ (đối với IPv6) xác định là có thể truy cập trên toàn cầu, với ngoại lệ sau:

      Đối với các địa chỉ IPv6 được ánh xạ IPv4, giá trị ``is_private`` được xác định theo ngữ nghĩa của các địa chỉ IPv4 cơ sở và điều kiện sau được thỏa mãn (xem :attr:`IPv6Address.ipv4_mapped`)::

         address.is_global == address.ipv4_mapped.is_global

      ``is_global`` có giá trị trái ngược với :attr:`is_private`, ngoại trừ không gian địa chỉ dùng chung (phạm vi ``100.64.0.0/10``), trong đó cả hai đều là ``False``.

      .. versionadded:: 3.4

      .. versionchanged:: 3.13

         Đã sửa một số trường hợp dương tính giả và âm tính giả; xem :attr:`is_private` để biết chi tiết.

   .. attribute:: is_unspecified

      ``True`` nếu địa chỉ không được chỉ định. Xem :RFC:`5735` (đối với IPv4) hoặc :RFC:`2373` (đối với IPv6).

   .. attribute:: is_reserved

      ``True`` nếu địa chỉ được IETF ghi nhận là dành riêng. Đối với IPv4, đây chỉ là ``240.0.0.0/4``, khối địa chỉ ``Reserved``. Đối với IPv6, đây là tất cả các địa chỉ `được phân bổ <iana-ipv6-address-space_>`__ dưới dạng ``Reserved by IETF`` để sử dụng trong tương lai.

      .. note:: Đối với IPv4, ``is_reserved`` không liên quan đến giá trị khối địa chỉ của cột ``Reserved-by-Protocol`` trong iana-ipv4-special-registry_.

      .. caution:: Đối với IPv6, ``fec0::/10`` một tiền tố địa chỉ có phạm vi Site-Local trước đây hiện bị loại khỏi danh sách đó (xem :attr:`~IPv6Address.is_site_local` & :rfc:`3879`).

   .. attribute:: is_loopback

      ``True`` nếu đây là địa chỉ loopback. Xem :RFC:`3330` (đối với IPv4) hoặc :RFC:`2373` (đối với IPv6).

   .. attribute:: is_link_local

      ``True`` nếu địa chỉ được dành riêng cho mục đích sử dụng liên kết cục bộ. Xem
      :RFC:`3927`.

   .. attribute:: ipv6_mapped

      :class:`IPv6Address` đối tượng biểu diễn địa chỉ IPv6 ánh xạ IPv4. Xem :RFC:`4291`.

      .. versionadded:: 3.13


.. _iana-ipv4-special-registry: https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
.. _iana-ipv6-special-registry: https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml
.. _iana-ipv6-address-space: https://www.iana.org/assignments/ipv6-address-space/ipv6-address-space.xhtml

.. method:: IPv4Address.__format__(fmt)

   Trả về biểu diễn chuỗi của địa chỉ IP, được điều khiển bởi chuỗi định dạng rõ ràng. *fmt* có thể là một trong các giá trị sau: ``'s'``, tùy chọn mặc định, tương đương với :func:`str`; ``'b'`` cho chuỗi nhị phân được đệm bằng số 0; ``'X'`` hoặc ``'x'`` cho biểu diễn hệ thập lục phân viết hoa hoặc viết thường; hoặc ``'n'``, tương đương với ``'b'`` đối với địa chỉ IPv4 và ``'x'`` đối với IPv6. Đối với các biểu diễn nhị phân và hệ thập lục phân, có thể sử dụng mã chỉ định dạng ``'#'`` và tùy chọn nhóm ``'_'``. ``__format__`` được ``format``, ``str.format`` và f-string sử dụng.

      >>> format(ipaddress.IPv4Address('192.168.0.1'))
      '192.168.0.1'
      >>> '{:#b}'.format(ipaddress.IPv4Address('192.168.0.1'))
      '0b11000000101010000000000000000001'
      >>> f'{ipaddress.IPv6Address("2001:db8::1000"):s}'
      '2001:db8::1000'
      >>> format(ipaddress.IPv6Address('2001:db8::1000'), '_X')
      '2001_0DB8_0000_0000_0000_0000_0000_1000'
      >>> '{:#_n}'.format(ipaddress.IPv6Address('2001:db8::1000'))
      '0x2001_0db8_0000_0000_0000_0000_0000_1000'

   .. versionadded:: 3.9


.. class:: IPv6Address(address)

   Tạo một địa chỉ IPv6. Một :exc:`AddressValueError` được phát sinh nếu *address* không phải là địa chỉ IPv6 hợp lệ.

   Sau đây là một địa chỉ IPv6 hợp lệ:

   1. Một chuỗi gồm tám nhóm, mỗi nhóm có bốn chữ số thập lục phân, trong đó mỗi nhóm biểu diễn 16 bit. Các nhóm được phân tách bằng dấu hai chấm. Đây là ký hiệu *exploded* (dạng đầy đủ). Chuỗi cũng có thể được *compressed* (ký hiệu rút gọn) bằng nhiều cách. Xem
      :RFC:`4291` để biết chi tiết. Ví dụ: ``"0000:0000:0000:0000:0000:0abc:0007:0def"`` có thể được rút gọn thành ``"::abc:7:def"``.

      Chuỗi cũng có thể có ID vùng phạm vi, được biểu diễn bằng hậu tố ``%scope_id``. Nếu có, ID phạm vi phải không rỗng và không được chứa ``%``. Xem :RFC:`4007` để biết chi tiết. Ví dụ: ``fe80::1234%1`` có thể xác định địa chỉ ``fe80::1234`` trên liên kết đầu tiên của nút.
   2. Một số nguyên có thể chứa trong 128 bit.
   3. Một số nguyên được đóng gói vào một đối tượng :class:`bytes` có độ dài 16, theo thứ tự byte lớn (big-endian).


   >>> ipaddress.IPv6Address('2001:db8::1000')
   IPv6Address('2001:db8::1000')
   >>> ipaddress.IPv6Address('ff02::5678%1')
   IPv6Address('ff02::5678%1')

   .. attribute:: compressed

   Dạng ngắn của biểu diễn địa chỉ, trong đó các số 0 đứng đầu trong các nhóm được lược bỏ và chuỗi dài nhất gồm các nhóm hoàn toàn là số 0 được rút gọn thành một nhóm rỗng duy nhất.

   Đây cũng là giá trị được ``str(addr)`` trả về cho các địa chỉ IPv6.

   .. attribute:: exploded

   Dạng đầy đủ của biểu diễn địa chỉ, trong đó tất cả các số 0 đứng đầu và các nhóm hoàn toàn là số 0 đều được giữ lại.


   Đối với các thuộc tính và phương thức sau, hãy xem tài liệu tương ứng của lớp :class:`IPv4Address`:

   .. attribute:: packed
   .. attribute:: reverse_pointer
   .. attribute:: version
   .. attribute:: max_prefixlen
   .. attribute:: is_multicast
   .. attribute:: is_private
   .. attribute:: is_global

      .. versionadded:: 3.4

   .. attribute:: is_unspecified
   .. attribute:: is_reserved
   .. attribute:: is_loopback
   .. attribute:: is_link_local

   .. attribute:: is_site_local

      ``True`` nếu địa chỉ được dành riêng cho mục đích sử dụng cục bộ trong site. Lưu ý rằng không gian địa chỉ cục bộ trong site đã bị :RFC:`3879` phản đối. Sử dụng
      :attr:`~IPv4Address.is_private` để kiểm tra xem địa chỉ này có thuộc không gian địa chỉ cục bộ duy nhất theo định nghĩa của :RFC:`4193` hay không.

   .. attribute:: ipv4_mapped

      Đối với các địa chỉ có vẻ là địa chỉ IPv4 được ánh xạ trong phạm vi ``::FFFF:0:0/96`` theo định nghĩa của :RFC:`4291`, thuộc tính này trả về địa chỉ IPv4 được nhúng. Với mọi địa chỉ khác, thuộc tính này sẽ là ``None``.

   .. attribute:: scope_id

      Đối với các địa chỉ có phạm vi theo định nghĩa của :RFC:`4007`, thuộc tính này xác định vùng cụ thể trong phạm vi của địa chỉ mà địa chỉ đó thuộc về, dưới dạng chuỗi. Khi không chỉ định vùng phạm vi, thuộc tính này sẽ là ``None``.

   .. attribute:: sixtofour

      Đối với các địa chỉ có vẻ là địa chỉ 6to4 (bắt đầu bằng ``2002::/16``) theo định nghĩa của :RFC:`3056`, thuộc tính này trả về địa chỉ IPv4 được nhúng. Với mọi địa chỉ khác, thuộc tính này sẽ là ``None``.

   .. attribute:: teredo

      Đối với các địa chỉ có vẻ là địa chỉ Teredo (bắt đầu bằng ``2001::/32``) theo định nghĩa của :RFC:`4380`, thuộc tính này trả về cặp địa chỉ IP ``(server, client)`` được nhúng. Với mọi địa chỉ khác, thuộc tính này sẽ là ``None``.

.. method:: IPv6Address.__format__(fmt)

   Tham khảo tài liệu về phương thức tương ứng trong
   :class:`IPv4Address`.

   .. versionadded:: 3.9

Chuyển đổi sang Chuỗi và Số nguyên
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để tương tác với các giao diện mạng như mô-đun socket, địa chỉ phải được chuyển đổi thành chuỗi hoặc số nguyên. Việc này được thực hiện bằng các hàm dựng sẵn :func:`str` và :func:`int`::

   >>> str(ipaddress.IPv4Address('192.168.0.1'))
   '192.168.0.1'
   >>> int(ipaddress.IPv4Address('192.168.0.1'))
   3232235521
   >>> str(ipaddress.IPv6Address('::1'))
   '::1'
   >>> int(ipaddress.IPv6Address('::1'))
   1

Lưu ý rằng các địa chỉ IPv6 có phạm vi được chuyển đổi thành số nguyên mà không có ID vùng phạm vi.


Toán tử
^^^^^^^

Đối tượng địa chỉ hỗ trợ một số toán tử.  Trừ khi có nêu khác, toán tử chỉ có thể được áp dụng giữa các đối tượng tương thích (tức là IPv4 với IPv4, IPv6 với IPv6).


Toán tử so sánh
"""""""""""""""

Các đối tượng địa chỉ có thể được so sánh bằng các toán tử so sánh thông thường. Các địa chỉ IPv6 giống nhau nhưng có ID vùng phạm vi khác nhau thì không bằng nhau. Một số ví dụ::

   >>> IPv4Address('127.0.0.2') > IPv4Address('127.0.0.1')
   True
   >>> IPv4Address('127.0.0.2') == IPv4Address('127.0.0.1')
   False
   >>> IPv4Address('127.0.0.2') != IPv4Address('127.0.0.1')
   True
   >>> IPv6Address('fe80::1234') == IPv6Address('fe80::1234%1')
   False
   >>> IPv6Address('fe80::1234%1') != IPv6Address('fe80::1234%2')
   True


Toán tử số học
""""""""""""""

Có thể cộng hoặc trừ số nguyên vào các đối tượng địa chỉ. Một số ví dụ::

   >>> IPv4Address('127.0.0.2') + 3
   IPv4Address('127.0.0.5')
   >>> IPv4Address('127.0.0.2') - 3
   IPv4Address('126.255.255.255')
   >>> IPv4Address('255.255.255.255') + 1
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ipaddress.AddressValueError: 4294967296 (>= 2**32) is not permitted as an IPv4 address


Định nghĩa mạng IP
------------------

Các đối tượng :class:`IPv4Network` và :class:`IPv6Network` cung cấp cơ chế để định nghĩa và kiểm tra các định nghĩa mạng IP. Một định nghĩa mạng bao gồm *mask* và *network address*, qua đó xác định một phạm vi địa chỉ IP bằng với địa chỉ mạng khi được áp dụng phép mask (AND nhị phân) với mask. Ví dụ: một định nghĩa mạng có mask ``255.255.255.0`` và địa chỉ mạng ``192.168.1.0`` bao gồm các địa chỉ IP trong phạm vi bao gồm cả hai đầu từ ``192.168.1.0`` đến ``192.168.1.255``.


Prefix, net mask và host mask
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có một số cách tương đương để chỉ định mask mạng IP. *prefix* ``/<nbits>`` là ký hiệu cho biết có bao nhiêu bit bậc cao được đặt trong net mask. *net mask* là một địa chỉ IP có một số bit bậc cao được đặt. Do đó, prefix ``/24`` tương đương với net mask ``255.255.255.0`` trong IPv4 hoặc ``ffff:ff00::`` trong IPv6. Ngoài ra, *host mask* là nghịch đảo logic của *net mask* và đôi khi được dùng (ví dụ: trong các danh sách kiểm soát truy cập của Cisco) để biểu thị một mask mạng. Host mask tương đương với ``/24`` trong IPv4 là ``0.0.0.255``.


Đối tượng mạng
^^^^^^^^^^^^^^

Tất cả các thuộc tính được triển khai bởi đối tượng địa chỉ cũng được triển khai bởi đối tượng mạng. Ngoài ra, đối tượng mạng triển khai thêm các thuộc tính. Tất cả những thuộc tính này đều dùng chung cho :class:`IPv4Network` và :class:`IPv6Network`, vì vậy để tránh trùng lặp, chúng chỉ được lập tài liệu cho :class:`IPv4Network`. Đối tượng mạng là :term:`hashable`, nên có thể được dùng làm khóa trong các dictionary.

.. class:: IPv4Network(address, strict=True)

   Tạo định nghĩa mạng IPv4. *address* có thể là một trong các dạng sau:

   1. Một chuỗi gồm địa chỉ IP và mặt nạ tùy chọn, được phân tách bằng dấu gạch chéo (``/``). Địa chỉ IP là địa chỉ mạng, còn mặt nạ có thể là một số đơn, nghĩa là *prefix*, hoặc là biểu diễn chuỗi của một địa chỉ IPv4. Nếu là dạng sau, mặt nạ được hiểu là *net mask* nếu bắt đầu bằng một trường khác không, hoặc là *host mask* nếu bắt đầu bằng một trường bằng không; ngoại lệ duy nhất là mặt nạ toàn số không, được xem là *net mask*. Nếu không cung cấp mặt nạ, giá trị này được xem là ``/32``.

      Ví dụ, các đặc tả *address* sau đây là tương đương: ``192.168.1.0/24``, ``192.168.1.0/255.255.255.0`` và ``192.168.1.0/0.0.0.255``.

   2. Một số nguyên vừa trong 32 bit. Giá trị này tương đương với một mạng đơn địa chỉ, trong đó địa chỉ mạng là *address* và mặt nạ là ``/32``.

   3. Một số nguyên được đóng gói vào một đối tượng :class:`bytes` có độ dài 4, theo thứ tự byte big-endian. Cách diễn giải tương tự như đối với *address* dạng số nguyên.

   4. Một bộ hai phần gồm mô tả địa chỉ và netmask, trong đó mô tả địa chỉ có thể là một chuỗi, một số nguyên 32 bit, một số nguyên được đóng gói thành 4 byte hoặc một đối tượng :class:`IPv4Address` hiện có; còn netmask có thể là một số nguyên biểu thị độ dài prefix (ví dụ: ``24``) hoặc một chuỗi biểu thị mặt nạ prefix (ví dụ: ``255.255.255.0``).

   Một :exc:`AddressValueError` được phát sinh nếu *address* không phải là địa chỉ IPv4 hợp lệ. Một :exc:`NetmaskValueError` được phát sinh nếu mặt nạ không hợp lệ đối với địa chỉ IPv4.

   Nếu *strict* là ``True`` và các bit host được thiết lập trong địa chỉ được cung cấp, thì :exc:`ValueError` sẽ được raise. Nếu không, các bit host sẽ được loại bỏ để xác định địa chỉ mạng phù hợp.

   Trừ khi có quy định khác, tất cả các phương thức mạng chấp nhận các đối tượng mạng/địa chỉ khác sẽ raise :exc:`TypeError` nếu phiên bản IP của đối số không tương thích với ``self``.

   .. versionchanged:: 3.5

      Đã bổ sung dạng tuple hai phần tử cho tham số constructor *address*.

   .. attribute:: version
   .. attribute:: max_prefixlen

      Tham khảo tài liệu về thuộc tính tương ứng tại
      :class:`IPv4Address`.

   .. attribute:: is_multicast
   .. attribute:: is_private
   .. attribute:: is_unspecified
   .. attribute:: is_reserved
   .. attribute:: is_loopback
   .. attribute:: is_link_local

      Các thuộc tính này đúng với toàn bộ mạng nếu chúng đúng với cả địa chỉ mạng và địa chỉ broadcast.

   .. attribute:: network_address

      Địa chỉ mạng của mạng. Địa chỉ mạng và độ dài tiền tố cùng nhau xác định duy nhất một mạng.

   .. attribute:: broadcast_address

      Địa chỉ broadcast của mạng. Các gói được gửi đến địa chỉ broadcast sẽ được mọi host trên mạng nhận.

   .. attribute:: hostmask

      Mặt nạ máy chủ, dưới dạng đối tượng :class:`IPv4Address`.

   .. attribute:: netmask

      Mặt nạ mạng, dưới dạng đối tượng :class:`IPv4Address`.

   .. attribute:: with_prefixlen
   .. attribute:: compressed
   .. attribute:: exploded

      Biểu diễn chuỗi của mạng, với mặt nạ ở dạng ký hiệu tiền tố.

      ``with_prefixlen`` và ``compressed`` luôn giống với ``str(network)``. ``exploded`` sử dụng dạng đầy đủ của địa chỉ mạng.

   .. attribute:: with_netmask

      Biểu diễn chuỗi của mạng, với mặt nạ ở dạng ký hiệu mặt nạ mạng.

   .. attribute:: with_hostmask

      Biểu diễn chuỗi của mạng, với mặt nạ ở dạng ký hiệu mặt nạ máy chủ.

   .. attribute:: num_addresses

      Tổng số địa chỉ trong mạng.

   .. attribute:: prefixlen

      Độ dài của tiền tố mạng, tính bằng bit.

   .. method:: hosts()

      Trả về một iterator chứa các host có thể sử dụng trong mạng. Các host có thể sử dụng là tất cả địa chỉ IP thuộc về mạng, ngoại trừ chính địa chỉ mạng và địa chỉ broadcast của mạng. Đối với các mạng có độ dài mask là 31, địa chỉ mạng và địa chỉ broadcast của mạng cũng được bao gồm trong kết quả. Các mạng có mask là 32 sẽ trả về một danh sách chứa một địa chỉ host duy nhất.

         >>> list(ip_network('192.0.2.0/29').hosts())  #doctest: +NORMALIZE_WHITESPACE
         [IPv4Address('192.0.2.1'), IPv4Address('192.0.2.2'),
          IPv4Address('192.0.2.3'), IPv4Address('192.0.2.4'),
          IPv4Address('192.0.2.5'), IPv4Address('192.0.2.6')]
         >>> list(ip_network('192.0.2.0/31').hosts())
         [IPv4Address('192.0.2.0'), IPv4Address('192.0.2.1')]
         >>> list(ip_network('192.0.2.1/32').hosts())
         [IPv4Address('192.0.2.1')]

   .. method:: overlaps(other)

      ``True`` nếu mạng này nằm một phần hoặc hoàn toàn trong *other* hoặc *other* nằm hoàn toàn trong mạng này.

   .. method:: address_exclude(network)

      Tính toán các định nghĩa mạng thu được bằng cách loại bỏ *network* đã cho khỏi mạng này. Trả về một iterator chứa các đối tượng mạng. Gây ra :exc:`ValueError` nếu *network* không hoàn toàn nằm trong mạng này.

         >>> n1 = ip_network('192.0.2.0/28')
         >>> n2 = ip_network('192.0.2.1/32')
         >>> list(n1.address_exclude(n2))  #doctest: +NORMALIZE_WHITESPACE
         [IPv4Network('192.0.2.8/29'), IPv4Network('192.0.2.4/30'),
          IPv4Network('192.0.2.2/31'), IPv4Network('192.0.2.0/32')]

   .. method:: subnets(prefixlen_diff=1, new_prefix=None)

      Các subnet hợp thành định nghĩa mạng hiện tại, tùy thuộc vào giá trị của các đối số. *prefixlen_diff* là lượng tăng của độ dài tiền tố. *new_prefix* là tiền tố mới mong muốn của các subnet; nó phải lớn hơn tiền tố hiện tại. Chỉ một và duy nhất một trong *prefixlen_diff* và *new_prefix* được đặt. Trả về một iterator chứa các đối tượng mạng.

         >>> list(ip_network('192.0.2.0/24').subnets())
         [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/25')]
         >>> list(ip_network('192.0.2.0/24').subnets(prefixlen_diff=2))  #doctest: +NORMALIZE_WHITESPACE
         [IPv4Network('192.0.2.0/26'), IPv4Network('192.0.2.64/26'),
          IPv4Network('192.0.2.128/26'), IPv4Network('192.0.2.192/26')]
         >>> list(ip_network('192.0.2.0/24').subnets(new_prefix=26))  #doctest: +NORMALIZE_WHITESPACE
         [IPv4Network('192.0.2.0/26'), IPv4Network('192.0.2.64/26'),
          IPv4Network('192.0.2.128/26'), IPv4Network('192.0.2.192/26')]
         >>> list(ip_network('192.0.2.0/24').subnets(new_prefix=23))
         Traceback (most recent call last):
           File "<stdin>", line 1, in <module>
             raise ValueError('new prefix must be longer')
         ValueError: new prefix must be longer
         >>> list(ip_network('192.0.2.0/24').subnets(new_prefix=25))
         [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/25')]

   .. method:: supernet(prefixlen_diff=1, new_prefix=None)

      Mạng siêu chứa định nghĩa mạng này, tùy thuộc vào các giá trị đối số. *prefixlen_diff* là lượng mà độ dài tiền tố của chúng ta phải giảm xuống. *new_prefix* là tiền tố mới mong muốn của mạng siêu; nó phải nhỏ hơn tiền tố của chúng ta. Chỉ một và duy nhất một trong *prefixlen_diff* và *new_prefix* được phép được thiết lập. Trả về một đối tượng mạng duy nhất.

         >>> ip_network('192.0.2.0/24').supernet()
         IPv4Network('192.0.2.0/23')
         >>> ip_network('192.0.2.0/24').supernet(prefixlen_diff=2)
         IPv4Network('192.0.0.0/22')
         >>> ip_network('192.0.2.0/24').supernet(new_prefix=20)
         IPv4Network('192.0.0.0/20')

   .. method:: subnet_of(other)

      Trả về ``True`` nếu mạng này là mạng con của *other*.

        >>> a = ip_network('192.168.1.0/24')
        >>> b = ip_network('192.168.1.128/30')
        >>> b.subnet_of(a)
        True

      .. versionadded:: 3.7

   .. method:: supernet_of(other)

      Trả về ``True`` nếu mạng này là mạng siêu của *other*.

        >>> a = ip_network('192.168.1.0/24')
        >>> b = ip_network('192.168.1.128/30')
        >>> a.supernet_of(b)
        True

      .. versionadded:: 3.7

   .. method:: compare_networks(other)

      So sánh mạng này với *other*. Trong phép so sánh này, chỉ các địa chỉ mạng được xét đến; các bit máy chủ không được xét đến. Trả về một trong ``-1``, ``0`` hoặc ``1``.

         >>> ip_network('192.0.2.1/32').compare_networks(ip_network('192.0.2.2/32'))
         -1
         >>> ip_network('192.0.2.1/32').compare_networks(ip_network('192.0.2.0/32'))
         1
         >>> ip_network('192.0.2.1/32').compare_networks(ip_network('192.0.2.1/32'))
         0

      .. deprecated:: 3.7
         Phương thức này sử dụng cùng thuật toán sắp xếp và so sánh như "<", "==" và ">"


.. class:: IPv6Network(address, strict=True)

   Xây dựng một định nghĩa mạng IPv6. *address* có thể là một trong các dạng sau:

   1. Một chuỗi gồm địa chỉ IP và độ dài tiền tố tùy chọn, được phân tách bằng dấu gạch chéo (``/``). Địa chỉ IP là địa chỉ mạng, và độ dài tiền tố phải là một số duy nhất, *prefix*. Nếu không cung cấp độ dài tiền tố, giá trị này được xem là ``/128``.

      Lưu ý rằng hiện tại không hỗ trợ netmask dạng mở rộng. Điều đó có nghĩa là ``2001:db00::0/24`` là một đối số hợp lệ, còn ``2001:db00::0/ffff:ff00::`` thì không.

   2. Một số nguyên nằm trong phạm vi 128 bit. Giá trị này tương đương với một mạng có một địa chỉ duy nhất, trong đó địa chỉ mạng là *address* và mask là ``/128``.

   3. Một số nguyên được đóng gói vào một đối tượng :class:`bytes` có độ dài 16, theo thứ tự byte lớn. Cách diễn giải tương tự như một số nguyên *address*.

   4. Một bộ hai phần gồm mô tả địa chỉ và netmask, trong đó mô tả địa chỉ có thể là một chuỗi, một số nguyên 128 bit, một số nguyên được đóng gói thành 16 byte hoặc một đối tượng :class:`IPv6Address` hiện có; còn netmask là một số nguyên biểu thị độ dài tiền tố.

   Một :exc:`AddressValueError` được phát sinh nếu *address* không phải là địa chỉ IPv6 hợp lệ. Một :exc:`NetmaskValueError` được phát sinh nếu mask không hợp lệ đối với địa chỉ IPv6.

   Nếu *strict* là ``True`` và các bit host được thiết lập trong địa chỉ được cung cấp, thì :exc:`ValueError` sẽ được raise. Nếu không, các bit host sẽ được loại bỏ để xác định địa chỉ mạng phù hợp.

   .. versionchanged:: 3.5

      Đã bổ sung dạng tuple hai phần tử cho tham số constructor *address*.

   .. attribute:: version
   .. attribute:: max_prefixlen
   .. attribute:: is_multicast
   .. attribute:: is_private
   .. attribute:: is_unspecified
   .. attribute:: is_reserved
   .. attribute:: is_loopback
   .. attribute:: is_link_local
   .. attribute:: network_address
   .. attribute:: broadcast_address
   .. attribute:: hostmask
   .. attribute:: netmask
   .. attribute:: with_prefixlen
   .. attribute:: compressed
   .. attribute:: exploded
   .. attribute:: with_netmask
   .. attribute:: with_hostmask
   .. attribute:: num_addresses
   .. attribute:: prefixlen
   .. method:: hosts()

      Trả về một iterator chứa các host có thể sử dụng trong mạng. Các host có thể sử dụng là tất cả địa chỉ IP thuộc về mạng, ngoại trừ địa chỉ anycast Subnet-Router. Đối với các mạng có độ dài mặt nạ là 127, địa chỉ anycast Subnet-Router cũng được включ vào kết quả. Các mạng có mặt nạ là 128 sẽ trả về một danh sách chứa một địa chỉ host duy nhất.

   .. method:: overlaps(other)
   .. method:: address_exclude(network)
   .. method:: subnets(prefixlen_diff=1, new_prefix=None)
   .. method:: supernet(prefixlen_diff=1, new_prefix=None)
   .. method:: subnet_of(other)
   .. method:: supernet_of(other)
   .. method:: compare_networks(other)

      Tham khảo tài liệu về thuộc tính tương ứng tại
      :class:`IPv4Network`.

   .. attribute:: is_site_local

      Thuộc tính này là true đối với toàn bộ mạng nếu nó là true đối với cả địa chỉ mạng và địa chỉ broadcast.


Toán tử
^^^^^^^

Các đối tượng mạng hỗ trợ một số toán tử. Nếu không có quy định khác, các toán tử chỉ có thể được áp dụng giữa những đối tượng tương thích (tức là IPv4 với IPv4, IPv6 với IPv6).


Các toán tử logic
"""""""""""""""""

Các đối tượng mạng có thể được so sánh bằng tập toán tử logic thông dụng. Các đối tượng mạng được sắp xếp trước theo địa chỉ mạng, sau đó theo mặt nạ mạng.


Lặp
"""

Có thể lặp qua các đối tượng mạng để liệt kê tất cả địa chỉ thuộc mạng. Khi lặp, *tất cả* máy chủ đều được trả về, bao gồm cả những máy chủ không thể sử dụng (để lấy các máy chủ có thể sử dụng, hãy dùng phương thức :meth:`~IPv4Network.hosts`). Một ví dụ::

   >>> for addr in IPv4Network('192.0.2.0/28'):
   ...     addr
   ...
   IPv4Address('192.0.2.0')
   IPv4Address('192.0.2.1')
   IPv4Address('192.0.2.2')
   IPv4Address('192.0.2.3')
   IPv4Address('192.0.2.4')
   IPv4Address('192.0.2.5')
   IPv4Address('192.0.2.6')
   IPv4Address('192.0.2.7')
   IPv4Address('192.0.2.8')
   IPv4Address('192.0.2.9')
   IPv4Address('192.0.2.10')
   IPv4Address('192.0.2.11')
   IPv4Address('192.0.2.12')
   IPv4Address('192.0.2.13')
   IPv4Address('192.0.2.14')
   IPv4Address('192.0.2.15')


Mạng dưới dạng các vùng chứa địa chỉ
""""""""""""""""""""""""""""""""""""

Các đối tượng mạng có thể hoạt động như các vùng chứa địa chỉ. Một số ví dụ::

   >>> IPv4Network('192.0.2.0/28')[0]
   IPv4Address('192.0.2.0')
   >>> IPv4Network('192.0.2.0/28')[15]
   IPv4Address('192.0.2.15')
   >>> IPv4Address('192.0.2.6') in IPv4Network('192.0.2.0/28')
   True
   >>> IPv4Address('192.0.3.6') in IPv4Network('192.0.2.0/28')
   False


Các đối tượng interface
-----------------------

Các đối tượng Interface là :term:`hashable`, vì vậy có thể được dùng làm khóa trong từ điển.

.. class:: IPv4Interface(address)

   Tạo một interface IPv4. Ý nghĩa của *address* giống như trong hàm khởi tạo của :class:`IPv4Network`, ngoại trừ việc các địa chỉ host tùy ý luôn được chấp nhận.

   :class:`IPv4Interface` là một lớp con của :class:`IPv4Address`, vì vậy nó kế thừa tất cả các thuộc tính từ lớp đó. Ngoài ra, các thuộc tính sau đây cũng khả dụng:

   .. attribute:: ip

      Địa chỉ (:class:`IPv4Address`) không có thông tin mạng.

         >>> interface = IPv4Interface('192.0.2.5/24')
         >>> interface.ip
         IPv4Address('192.0.2.5')

   .. attribute:: network

      Mạng (:class:`IPv4Network`) mà interface này thuộc về.

         >>> interface = IPv4Interface('192.0.2.5/24')
         >>> interface.network
         IPv4Network('192.0.2.0/24')

   .. attribute:: with_prefixlen

      Biểu diễn chuỗi của interface với mask ở dạng ký hiệu prefix.

         >>> interface = IPv4Interface('192.0.2.5/24')
         >>> interface.with_prefixlen
         '192.0.2.5/24'

   .. attribute:: with_netmask

      Biểu diễn chuỗi của interface với mạng ở dạng net mask.

         >>> interface = IPv4Interface('192.0.2.5/24')
         >>> interface.with_netmask
         '192.0.2.5/255.255.255.0'

   .. attribute:: with_hostmask

      Biểu diễn chuỗi của interface với network làm host mask.

         >>> interface = IPv4Interface('192.0.2.5/24')
         >>> interface.with_hostmask
         '192.0.2.5/0.0.0.255'


.. class:: IPv6Interface(address)

   Tạo một interface IPv6. Ý nghĩa của *address* cũng giống như trong hàm khởi tạo của :class:`IPv6Network`, ngoại trừ việc các địa chỉ host tùy ý luôn được chấp nhận.

   :class:`IPv6Interface` là một lớp con của :class:`IPv6Address`, vì vậy nó kế thừa tất cả các thuộc tính từ lớp đó. Ngoài ra, các thuộc tính sau đây cũng khả dụng:

   .. attribute:: ip
   .. attribute:: network
   .. attribute:: with_prefixlen
   .. attribute:: with_netmask
   .. attribute:: with_hostmask

      Tham khảo tài liệu về thuộc tính tương ứng trong
      :class:`IPv4Interface`.


Toán tử
^^^^^^^

Các đối tượng interface hỗ trợ một số toán tử. Trừ khi có nêu khác, các toán tử chỉ có thể được áp dụng giữa những đối tượng tương thích (tức là IPv4 với IPv4, IPv6 với IPv6).


Các toán tử logic
"""""""""""""""""

Các đối tượng interface có thể được so sánh bằng các toán tử logic thông thường.

Đối với phép so sánh bằng (``==`` và ``!=``), cả địa chỉ IP và network đều phải giống nhau thì các đối tượng mới bằng nhau. Một interface sẽ không được so sánh bằng với bất kỳ đối tượng địa chỉ hoặc network nào.

Đối với phép sắp thứ tự (``<``, ``>``, v.v.), các quy tắc sẽ khác. Có thể so sánh các đối tượng interface và địa chỉ có cùng phiên bản IP, trong đó các đối tượng địa chỉ sẽ luôn được sắp xếp trước các đối tượng interface. Hai đối tượng interface trước tiên được so sánh theo network của chúng và nếu các network giống nhau thì tiếp tục được so sánh theo địa chỉ IP.


Các hàm khác ở cấp module
-------------------------

Module này cũng cung cấp các hàm sau ở cấp module:

.. function:: v4_int_to_packed(address)

   Biểu diễn một địa chỉ dưới dạng 4 byte được đóng gói theo thứ tự network (big-endian). *địa chỉ* là biểu diễn số nguyên của một địa chỉ IP IPv4. Một
   :exc:`ValueError` sẽ được ném ra nếu số nguyên là số âm hoặc quá lớn để biểu diễn một địa chỉ IP IPv4.

   >>> ipaddress.ip_address(3221225985)
   IPv4Address('192.0.2.1')
   >>> ipaddress.v4_int_to_packed(3221225985)
   b'\xc0\x00\x02\x01'


.. function:: v6_int_to_packed(address)

   Biểu diễn một địa chỉ dưới dạng 16 byte được đóng gói theo thứ tự mạng (big-endian). *address* là biểu diễn số nguyên của một địa chỉ IP IPv6. Một
   :exc:`ValueError` sẽ được phát sinh nếu số nguyên là số âm hoặc quá lớn để biểu diễn một địa chỉ IP IPv6.


.. function:: summarize_address_range(first, last)

   Trả về một iterator của dải mạng đã được tóm tắt, dựa trên địa chỉ IP đầu tiên và cuối cùng. *first* là :class:`IPv4Address` đầu tiên hoặc
   :class:`IPv6Address` trong dải và *last* là :class:`IPv4Address` cuối cùng hoặc :class:`IPv6Address` trong dải. Một :exc:`TypeError` sẽ được phát sinh nếu *first* hoặc *last* không phải là địa chỉ IP hoặc không cùng phiên bản. Một
   :exc:`ValueError` sẽ được phát sinh nếu *last* không lớn hơn *first* hoặc nếu phiên bản địa chỉ của *first* không phải là 4 hoặc 6.

   >>> [ipaddr for ipaddr in ipaddress.summarize_address_range(
   ...    ipaddress.IPv4Address('192.0.2.0'),
   ...    ipaddress.IPv4Address('192.0.2.130'))]
   [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/31'), IPv4Network('192.0.2.130/32')]


.. function:: collapse_addresses(addresses)

   Trả về một iterator của các :class:`IPv4Network` đã được gộp hoặc
   các đối tượng :class:`IPv6Network`. *addresses* là một :term:`iterable` của
   các đối tượng :class:`IPv4Network` hoặc :class:`IPv6Network`. Một :exc:`TypeError` được phát sinh nếu *addresses* chứa các đối tượng thuộc nhiều phiên bản khác nhau.

   >>> [ipaddr for ipaddr in
   ... ipaddress.collapse_addresses([ipaddress.IPv4Network('192.0.2.0/25'),
   ... ipaddress.IPv4Network('192.0.2.128/25')])]
   [IPv4Network('192.0.2.0/24')]


.. function:: get_mixed_type_key(obj)

   Trả về một key phù hợp để sắp xếp giữa các network và address. Các đối tượng Address và Network không thể được sắp xếp theo mặc định; về bản chất chúng khác nhau, vì vậy biểu thức này không có ý nghĩa.::

     IPv4Address('192.0.2.0') <= IPv4Network('192.0.2.0/24')

   Tuy nhiên, đôi khi bạn có thể muốn :mod:`!ipaddress` vẫn sắp xếp chúng. Nếu cần làm vậy, bạn có thể sử dụng hàm này làm đối số *key* của :func:`sorted`.

   *obj* là một đối tượng network hoặc address.


Ngoại lệ tùy chỉnh
------------------

Để hỗ trợ việc báo cáo lỗi cụ thể hơn từ các hàm khởi tạo lớp, module định nghĩa các ngoại lệ sau:

.. exception:: AddressValueError(ValueError)

   Bất kỳ lỗi giá trị nào liên quan đến address.


.. exception:: NetmaskValueError(ValueError)

   Mọi lỗi giá trị liên quan đến net mask.
