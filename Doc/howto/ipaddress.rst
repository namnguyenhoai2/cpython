.. testsetup::

   import ipaddress

.. _ipaddress-howto:

******************************
Giới thiệu về module ipaddress
******************************

:author: Peter Moody
:author: Nick Coghlan

.. topic:: Tổng quan

   Tài liệu này nhằm cung cấp phần giới thiệu dễ hiểu về
   :mod:`ipaddress` module. Tài liệu chủ yếu dành cho những người chưa quen với thuật ngữ mạng IP, nhưng cũng có thể hữu ích cho các kỹ sư mạng muốn có cái nhìn tổng quan về cách :mod:`ipaddress` biểu diễn các khái niệm địa chỉ mạng IP.


Tạo các đối tượng Address/Network/Interface
===========================================

Vì :mod:`ipaddress` là một module dùng để kiểm tra và thao tác với các địa chỉ IP, việc đầu tiên bạn cần làm là tạo một số đối tượng. Bạn có thể sử dụng
:mod:`ipaddress` để tạo các đối tượng từ chuỗi và số nguyên.


Lưu ý về các phiên bản IP
-------------------------

Đối với những độc giả chưa thật sự quen thuộc với việc định địa chỉ IP, điều quan trọng cần biết là Internet Protocol (IP) hiện đang trong quá trình chuyển từ phiên bản 4 sang phiên bản 6. Quá trình chuyển đổi này chủ yếu diễn ra vì phiên bản 4 của giao thức không cung cấp đủ địa chỉ để đáp ứng nhu cầu của toàn thế giới, đặc biệt khi số lượng thiết bị có kết nối trực tiếp với internet ngày càng tăng.

Việc giải thích chi tiết sự khác biệt giữa hai phiên bản của giao thức nằm ngoài phạm vi của phần giới thiệu này, nhưng độc giả ít nhất cần biết rằng có hai phiên bản này và đôi khi sẽ cần buộc sử dụng phiên bản này hoặc phiên bản kia.


Địa chỉ máy chủ IP
------------------

Địa chỉ, thường được gọi là "địa chỉ máy chủ", là đơn vị cơ bản nhất khi làm việc với việc định địa chỉ IP. Cách đơn giản nhất để tạo địa chỉ là sử dụng hàm factory :func:`ipaddress.ip_address`, hàm này tự động xác định nên tạo địa chỉ IPv4 hay IPv6 dựa trên giá trị được truyền vào:

   >>> ipaddress.ip_address('192.0.2.1')
   IPv4Address('192.0.2.1')
   >>> ipaddress.ip_address('2001:DB8::1')
   IPv6Address('2001:db8::1')

Địa chỉ cũng có thể được tạo trực tiếp từ các số nguyên. Các giá trị vừa trong phạm vi 32 bit được mặc định là địa chỉ IPv4::

   >>> ipaddress.ip_address(3221225985)
   IPv4Address('192.0.2.1')
   >>> ipaddress.ip_address(42540766411282592856903984951653826561)
   IPv6Address('2001:db8::1')

Để buộc sử dụng địa chỉ IPv4 hoặc IPv6, bạn có thể gọi trực tiếp các lớp tương ứng. Điều này đặc biệt hữu ích khi muốn buộc tạo địa chỉ IPv6 từ các số nguyên nhỏ::

   >>> ipaddress.ip_address(1)
   IPv4Address('0.0.0.1')
   >>> ipaddress.IPv4Address(1)
   IPv4Address('0.0.0.1')
   >>> ipaddress.IPv6Address(1)
   IPv6Address('::1')


Định nghĩa mạng
---------------

Các địa chỉ máy chủ thường được nhóm lại thành các mạng IP, vì vậy
:mod:`ipaddress` cung cấp cách tạo, kiểm tra và thao tác với các định nghĩa mạng. Đối tượng mạng IP được xây dựng từ các chuỗi xác định phạm vi địa chỉ máy chủ thuộc mạng đó. Dạng đơn giản nhất của thông tin này là một cặp "địa chỉ mạng/prefix mạng", trong đó prefix xác định số bit đầu tiên được so sánh để xác định một địa chỉ có thuộc mạng hay không, còn địa chỉ mạng xác định giá trị mong đợi của các bit đó.

Tương tự như với địa chỉ, một hàm factory được cung cấp để tự động xác định phiên bản IP phù hợp::

   >>> ipaddress.ip_network('192.0.2.0/24')
   IPv4Network('192.0.2.0/24')
   >>> ipaddress.ip_network('2001:db8::0/96')
   IPv6Network('2001:db8::/96')

Đối tượng mạng không thể có bất kỳ bit máy chủ nào được thiết lập. Hệ quả thực tế là ``192.0.2.1/24`` không mô tả một mạng. Những định nghĩa như vậy được gọi là đối tượng interface vì ký hiệu ip-on-a-network thường được dùng để mô tả các interface mạng của một máy tính trên một mạng nhất định; chúng sẽ được mô tả thêm trong phần tiếp theo.

Theo mặc định, việc cố tạo một đối tượng network có các bit host được thiết lập sẽ khiến :exc:`ValueError` được phát sinh. Để yêu cầu các bit bổ sung thay vào đó được ép về 0, có thể truyền cờ ``strict=False`` cho constructor::

   >>> ipaddress.ip_network('192.0.2.1/24')
   Traceback (most recent call last):
      ...
   ValueError: 192.0.2.1/24 has host bits set
   >>> ipaddress.ip_network('192.0.2.1/24', strict=False)
   IPv4Network('192.0.2.0/24')

Mặc dù dạng chuỗi linh hoạt hơn đáng kể, network cũng có thể được định nghĩa bằng số nguyên, giống như địa chỉ host. Trong trường hợp này, network được xem là chỉ chứa một địa chỉ duy nhất được xác định bởi số nguyên đó, vì vậy tiền tố network bao gồm toàn bộ địa chỉ network::

   >>> ipaddress.ip_network(3221225984)
   IPv4Network('192.0.2.0/32')
   >>> ipaddress.ip_network(42540766411282592856903984951653826560)
   IPv6Network('2001:db8::/128')

Cũng như với các địa chỉ, có thể buộc tạo một loại network cụ thể bằng cách gọi trực tiếp constructor của class thay vì sử dụng factory function.


Giao diện Host
--------------

Như đã đề cập ngay trên, nếu cần mô tả một địa chỉ trên một network cụ thể thì cả class địa chỉ lẫn class network đều không đủ. Ký hiệu như ``192.0.2.1/24`` thường được các kỹ sư network và những người viết công cụ cho firewall và router sử dụng như cách viết tắt cho "host ``192.0.2.1`` trên network ``192.0.2.0/24``", Theo đó, :mod:`ipaddress` cung cấp một tập hợp các class kết hợp một địa chỉ với một network cụ thể. Giao diện để tạo đối tượng giống hệt giao diện dùng để định nghĩa các đối tượng network, ngoại trừ việc phần địa chỉ không bị giới hạn phải là một địa chỉ network.

   >>> ipaddress.ip_interface('192.0.2.1/24')
   IPv4Interface('192.0.2.1/24')
   >>> ipaddress.ip_interface('2001:db8::1/96')
   IPv6Interface('2001:db8::1/96')

Có thể sử dụng đầu vào là số nguyên (tương tự như với network), và có thể buộc sử dụng một phiên bản IP cụ thể bằng cách gọi trực tiếp constructor tương ứng.


Kiểm tra các đối tượng Address/Network/Interface
================================================

Bạn đã mất công tạo một đối tượng IPv(4|6)(Address|Network|Interface), vì vậy có lẽ bạn muốn lấy thông tin về đối tượng đó. :mod:`ipaddress` cố gắng giúp việc này trở nên dễ dàng và trực quan.

Trích xuất phiên bản IP::

   >>> addr4 = ipaddress.ip_address('192.0.2.1')
   >>> addr6 = ipaddress.ip_address('2001:db8::1')
   >>> addr6.version
   6
   >>> addr4.version
   4

Lấy network từ một interface::

   >>> host4 = ipaddress.ip_interface('192.0.2.1/24')
   >>> host4.network
   IPv4Network('192.0.2.0/24')
   >>> host6 = ipaddress.ip_interface('2001:db8::1/96')
   >>> host6.network
   IPv6Network('2001:db8::/96')

Tìm số lượng địa chỉ riêng lẻ trong một network::

   >>> net4 = ipaddress.ip_network('192.0.2.0/24')
   >>> net4.num_addresses
   256
   >>> net6 = ipaddress.ip_network('2001:db8::0/96')
   >>> net6.num_addresses
   4294967296

Duyệt qua các địa chỉ "có thể sử dụng" trên một network::

   >>> net4 = ipaddress.ip_network('192.0.2.0/24')
   >>> for x in net4.hosts():
   ...     print(x)  # doctest: +ELLIPSIS
   192.0.2.1
   192.0.2.2
   192.0.2.3
   192.0.2.4
   ...
   192.0.2.252
   192.0.2.253
   192.0.2.254


Lấy netmask (tức là các bit được thiết lập tương ứng với network prefix) hoặc hostmask (bất kỳ bit nào không thuộc netmask):

   >>> net4 = ipaddress.ip_network('192.0.2.0/24')
   >>> net4.netmask
   IPv4Address('255.255.255.0')
   >>> net4.hostmask
   IPv4Address('0.0.0.255')
   >>> net6 = ipaddress.ip_network('2001:db8::0/96')
   >>> net6.netmask
   IPv6Address('ffff:ffff:ffff:ffff:ffff:ffff::')
   >>> net6.hostmask
   IPv6Address('::ffff:ffff')


Mở rộng hoặc nén địa chỉ::

   >>> addr6.exploded
   '2001:0db8:0000:0000:0000:0000:0000:0001'
   >>> addr6.compressed
   '2001:db8::1'
   >>> net6.exploded
   '2001:0db8:0000:0000:0000:0000:0000:0000/96'
   >>> net6.compressed
   '2001:db8::/96'

Mặc dù IPv4 không hỗ trợ việc mở rộng hoặc nén, các đối tượng liên quan vẫn cung cấp những thuộc tính tương ứng để code không phụ thuộc phiên bản có thể dễ dàng bảo đảm sử dụng dạng ngắn gọn nhất hoặc đầy đủ nhất cho các địa chỉ IPv6, đồng thời vẫn xử lý chính xác các địa chỉ IPv4.


Mạng dưới dạng danh sách Address
================================

Đôi khi việc xem các mạng như những danh sách rất hữu ích. Điều này cho phép lập chỉ mục cho chúng như sau::

   >>> net4[1]
   IPv4Address('192.0.2.1')
   >>> net4[-1]
   IPv4Address('192.0.2.255')
   >>> net6[1]
   IPv6Address('2001:db8::1')
   >>> net6[-1]
   IPv6Address('2001:db8::ffff:ffff')


Điều này cũng có nghĩa là các đối tượng mạng phù hợp với việc sử dụng cú pháp kiểm tra phần tử trong danh sách như sau::

   if address in network:
       # thực hiện thao tác gì đó

Việc kiểm tra bao hàm được thực hiện hiệu quả dựa trên network prefix::

   >>> addr4 = ipaddress.ip_address('192.0.2.1')
   >>> addr4 in ipaddress.ip_network('192.0.2.0/24')
   True
   >>> addr4 in ipaddress.ip_network('192.0.3.0/24')
   False


So sánh
=======

:mod:`ipaddress` cung cấp một số cách đơn giản, hy vọng là trực quan, để so sánh các đối tượng khi điều đó hợp lý::

   >>> ipaddress.ip_address('192.0.2.1') < ipaddress.ip_address('192.0.2.2')
   True

Một ngoại lệ :exc:`TypeError` sẽ được phát sinh nếu bạn cố so sánh các đối tượng thuộc các phiên bản khác nhau hoặc có kiểu khác nhau.


Sử dụng địa chỉ IP với các mô-đun khác
======================================

Các mô-đun khác sử dụng địa chỉ IP (chẳng hạn như :mod:`socket`) thường không chấp nhận trực tiếp các đối tượng từ mô-đun này. Thay vào đó, chúng phải được chuyển đổi thành một số nguyên hoặc chuỗi mà mô-đun kia chấp nhận::

   >>> addr4 = ipaddress.ip_address('192.0.2.1')
   >>> str(addr4)
   '192.0.2.1'
   >>> int(addr4)
   3221225985


Nhận thêm thông tin chi tiết khi tạo thực thể không thành công
==============================================================

Khi tạo các đối tượng địa chỉ/mạng/giao diện bằng các hàm factory không phụ thuộc phiên bản, mọi lỗi sẽ được báo cáo dưới dạng :exc:`ValueError` với thông báo lỗi chung, chỉ cho biết rằng giá trị được truyền vào không được nhận dạng là một đối tượng thuộc kiểu đó. Việc không có lỗi cụ thể là vì cần biết liệu giá trị đó có *supposed* là IPv4 hay IPv6 thì mới có thể cung cấp thêm chi tiết về lý do giá trị đó bị từ chối.

Để hỗ trợ các trường hợp sử dụng cần truy cập vào thông tin chi tiết bổ sung này, các hàm khởi tạo của từng lớp thực sự sẽ raise
:exc:`ValueError` là lớp con của :exc:`ipaddress.AddressValueError` và
:exc:`ipaddress.NetmaskValueError` để chỉ ra chính xác phần nào trong định nghĩa không thể được phân tích cú pháp chính xác.

Các thông báo lỗi sẽ chi tiết hơn đáng kể khi sử dụng trực tiếp các hàm khởi tạo của lớp. Ví dụ::

   >>> ipaddress.ip_address("192.168.0.256")
   Traceback (most recent call last):
     ...
   ValueError: '192.168.0.256' does not appear to be an IPv4 or IPv6 address
   >>> ipaddress.IPv4Address("192.168.0.256")
   Traceback (most recent call last):
     ...
   ipaddress.AddressValueError: Octet 256 (> 255) not permitted in '192.168.0.256'

   >>> ipaddress.ip_network("192.168.0.1/64")
   Traceback (most recent call last):
     ...
   ValueError: '192.168.0.1/64' does not appear to be an IPv4 or IPv6 network
   >>> ipaddress.IPv4Network("192.168.0.1/64")
   Traceback (most recent call last):
     ...
   ipaddress.NetmaskValueError: '64' is not a valid netmask

Tuy nhiên, cả hai exception dành riêng cho module đều có :exc:`ValueError` làm lớp cha, vì vậy nếu bạn không quan tâm đến loại lỗi cụ thể, bạn vẫn có thể viết mã như sau::

   try:
       network = ipaddress.IPv4Network(address)
   except ValueError:
       print('address/netmask is invalid for IPv4:', address)

