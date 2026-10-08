:mod:`!socket` --- Giao diện mạng cấp thấp
==========================================

.. module:: socket
   :synopsis: Giao diện mạng cấp thấp.

**Mã nguồn:** :source:`Lib/socket.py`

--------------

Mô-đun này cung cấp quyền truy cập vào giao diện *socket* của BSD. Giao diện này có trên mọi hệ thống Unix hiện đại, Windows, MacOS và có thể cả các nền tảng khác.

.. note::

   Một số hành vi có thể phụ thuộc vào nền tảng, vì các lệnh gọi được thực hiện đến các API socket của hệ điều hành.


.. include:: ../includes/wasm-notavail.rst

.. index:: pair: object; socket

Giao diện Python là bản chuyển đổi trực tiếp của giao diện system call và thư viện Unix dành cho socket sang phong cách hướng đối tượng của Python:
hàm :func:`~socket.socket` trả về một :dfn:`đối tượng socket` có các phương thức triển khai nhiều system call socket khác nhau. Kiểu tham số có mức trừu tượng cao hơn đôi chút so với giao diện C: tương tự như các thao tác :meth:`read` và :meth:`write` trên tệp Python, việc cấp phát buffer trong các thao tác nhận được thực hiện tự động, còn độ dài buffer được ngầm định trong các thao tác gửi.


.. seealso::

   Mô-đun :mod:`socketserver`
      Các class giúp đơn giản hóa việc viết network server.

   Mô-đun :mod:`ssl`
      Wrapper TLS/SSL cho các socket object.


.. _socket-addresses:

Các họ socket
-------------

Tùy thuộc vào hệ thống và các tùy chọn build, mô-đun này hỗ trợ nhiều họ socket khác nhau.

Định dạng địa chỉ cần thiết cho một socket object cụ thể sẽ được tự động chọn dựa trên họ địa chỉ được chỉ định khi socket object được tạo. Địa chỉ socket được biểu diễn như sau:

- Địa chỉ của socket :const:`AF_UNIX` được liên kết với một nút hệ thống tệp được biểu diễn dưới dạng chuỗi, sử dụng encoding của hệ thống tệp và trình xử lý lỗi ``'surrogateescape'`` (xem :pep:`383`). Địa chỉ trong namespace trừu tượng của Linux được trả về dưới dạng :term:`bytes-like object` với một byte null ở đầu; lưu ý rằng các socket trong namespace này có thể giao tiếp với các socket hệ thống tệp thông thường, vì vậy các chương trình dự định chạy trên Linux có thể cần xử lý cả hai loại địa chỉ. Có thể sử dụng đối tượng dạng chuỗi hoặc tương tự bytes cho cả hai loại địa chỉ khi truyền làm đối số.

  .. versionchanged:: 3.3
     Trước đây, các đường dẫn socket :const:`AF_UNIX` được mặc định sử dụng encoding UTF-8.

  .. versionchanged:: 3.5
     Hiện đã chấp nhận :term:`bytes-like object` có thể ghi.

.. _host_port:

- Một cặp ``(host, port)`` được sử dụng cho họ địa chỉ :const:`AF_INET`, trong đó *host* là một chuỗi biểu diễn hostname theo ký hiệu miền Internet như ``'daring.cwi.nl'`` hoặc một địa chỉ IPv4 như ``'100.50.200.5'``, còn *port* là một số nguyên.

  - Đối với địa chỉ IPv4, hai dạng đặc biệt được chấp nhận thay cho địa chỉ host: ``''`` biểu diễn :const:`INADDR_ANY`, được dùng để liên kết với tất cả các interface, còn chuỗi ``'<broadcast>'`` biểu diễn
    :const:`INADDR_BROADCAST`. Hành vi này không tương thích với IPv6, do đó bạn có thể muốn tránh sử dụng các dạng này nếu dự định hỗ trợ IPv6 trong các chương trình Python của mình.

- Đối với họ địa chỉ :const:`AF_INET6`, một bộ bốn ``(host, port, flowinfo, scope_id)`` được sử dụng, trong đó *flowinfo* và *scope_id* biểu diễn các thành viên ``sin6_flowinfo`` và ``sin6_scope_id`` trong :const:`struct sockaddr_in6` ở C. Đối với
  :mod:`!socket` các phương thức của module, *flowinfo* và *scope_id* có thể được bỏ qua chỉ để duy trì khả năng tương thích ngược. Tuy nhiên, lưu ý rằng việc bỏ qua *scope_id* có thể gây ra vấn đề khi thao tác với các địa chỉ IPv6 có phạm vi.

  .. versionchanged:: 3.7
     Đối với các địa chỉ multicast (trong đó *scope_id* có ý nghĩa), *address* có thể không chứa phần ``%scope_id`` (hoặc ``zone id``). Thông tin này là dư thừa và có thể được bỏ qua an toàn (khuyến nghị).

- :const:`AF_NETLINK` các socket được biểu diễn dưới dạng các cặp ``(pid, groups)``.

- TIPC chỉ được hỗ trợ trên Linux thông qua họ địa chỉ :const:`AF_TIPC`. TIPC là một giao thức mạng mở, không dựa trên IP, được thiết kế để sử dụng trong các môi trường máy tính phân cụm. Các địa chỉ được biểu diễn bằng một tuple và các trường phụ thuộc vào loại địa chỉ. Dạng tuple tổng quát là ``(addr_type, v1, v2, v3 [, scope])``, trong đó:

  - *addr_type* là một trong :const:`TIPC_ADDR_NAMESEQ`, :const:`TIPC_ADDR_NAME` hoặc :const:`TIPC_ADDR_ID`.
  - *scope* là một trong :const:`TIPC_ZONE_SCOPE`, :const:`TIPC_CLUSTER_SCOPE` và
    :const:`TIPC_NODE_SCOPE`.
  - Nếu *addr_type* là :const:`TIPC_ADDR_NAME`, thì *v1* là loại máy chủ, *v2* là mã định danh cổng và *v3* phải là 0.

    Nếu *addr_type* là :const:`TIPC_ADDR_NAMESEQ`, thì *v1* là loại máy chủ, *v2* là số cổng nhỏ hơn, và *v3* là số cổng lớn hơn.

    Nếu *addr_type* là :const:`TIPC_ADDR_ID`, thì *v1* là node, *v2* là tham chiếu, và *v3* phải được đặt thành 0.

- Một tuple ``(interface, )`` được sử dụng cho họ địa chỉ :const:`AF_CAN`, trong đó *interface* là một chuỗi biểu thị tên giao diện mạng như ``'can0'``. Có thể sử dụng tên giao diện mạng ``''`` để nhận các gói tin từ tất cả giao diện mạng thuộc họ này.

  - :const:`CAN_ISOTP` protocol yêu cầu một tuple ``(interface, rx_addr, tx_addr)``, trong đó cả hai tham số bổ sung đều là số nguyên unsigned long biểu thị một CAN identifier (tiêu chuẩn hoặc mở rộng).
  - :const:`CAN_J1939` protocol yêu cầu một tuple ``(interface, name, pgn, addr)``, trong đó các tham số bổ sung lần lượt là số nguyên unsigned 64-bit biểu thị tên ECU, số nguyên unsigned 32-bit biểu thị Parameter Group Number (PGN), và số nguyên 8-bit biểu thị địa chỉ.

- Một chuỗi hoặc tuple ``(id, unit)`` được sử dụng cho protocol :const:`SYSPROTO_CONTROL` của họ :const:`PF_SYSTEM`. Chuỗi này là tên của một kernel control sử dụng ID được gán động. Tuple có thể được sử dụng nếu đã biết ID và số đơn vị của kernel control hoặc nếu sử dụng một ID đã đăng ký.

  .. versionadded:: 3.3

- :const:`AF_BLUETOOTH` hỗ trợ các protocol và định dạng địa chỉ sau đây:

  - :const:`BTPROTO_L2CAP` nhận một tuple ``(bdaddr, psm[, cid[, bdaddr_type]])`` trong đó:

    - ``bdaddr`` là một chuỗi chỉ định địa chỉ Bluetooth.
    - ``psm`` là một số nguyên chỉ định Protocol/Service Multiplexer.
    - ``cid`` là một số nguyên tùy chọn chỉ định Channel Identifier. Nếu không được cung cấp, giá trị mặc định là không.
    - ``bdaddr_type`` là một số nguyên tùy chọn chỉ định loại địa chỉ; một trong :const:`BDADDR_BREDR` (mặc định), :const:`BDADDR_LE_PUBLIC`,
      :const:`BDADDR_LE_RANDOM`.

    .. versionchanged:: 3.14
       Đã thêm các trường ``cid`` và ``bdaddr_type``.

  - :const:`BTPROTO_RFCOMM` nhận ``(bdaddr, channel)``, trong đó ``bdaddr`` là địa chỉ Bluetooth dưới dạng chuỗi và ``channel`` là một số nguyên.

  - :const:`BTPROTO_HCI` chấp nhận một định dạng phụ thuộc vào hệ điều hành của bạn.

    - Trên Linux, nó chấp nhận một số nguyên ``device_id`` hoặc một tuple ``(device_id, [channel])``, trong đó ``device_id`` chỉ định số của thiết bị Bluetooth, còn ``channel`` là một số nguyên tùy chọn chỉ định kênh HCI (:const:`HCI_CHANNEL_RAW` theo mặc định).
    - Trên FreeBSD, NetBSD và DragonFly BSD, nó chấp nhận ``bdaddr``, trong đó ``bdaddr`` là địa chỉ Bluetooth dưới dạng chuỗi.

    .. versionchanged:: 3.2
       Đã bổ sung hỗ trợ cho NetBSD và DragonFlyBSD.

    .. versionchanged:: 3.13.3
       Đã bổ sung hỗ trợ cho FreeBSD.

    .. versionchanged:: 3.14
       Đã bổ sung trường ``channel``. Hiện đã chấp nhận ``device_id`` không được đóng gói trong tuple.

  - :const:`BTPROTO_SCO` chấp nhận ``bdaddr``, trong đó ``bdaddr`` là địa chỉ Bluetooth dưới dạng chuỗi hoặc đối tượng :class:`bytes`. (ví dụ: ``'12:23:34:45:56:67'`` hoặc ``b'12:23:34:45:56:67'``)

    .. versionchanged:: 3.14
       Đã bổ sung hỗ trợ cho FreeBSD.

- :const:`AF_ALG` là giao diện dựa trên socket chỉ dành cho Linux để truy cập chức năng mật mã của Kernel. Một socket thuật toán được cấu hình bằng một tuple gồm từ hai đến bốn phần tử ``(type, name [, feat [, mask]])``, trong đó:

  - *type* là kiểu thuật toán dưới dạng chuỗi, ví dụ ``aead``, ``hash``, ``skcipher`` hoặc ``rng``.

  - *name* là tên thuật toán và chế độ hoạt động dưới dạng chuỗi, ví dụ ``sha256``, ``hmac(sha256)``, ``cbc(aes)`` hoặc ``drbg_nopr_ctr_aes256``.

  - *feat* và *mask* là các số nguyên 32 bit không dấu.

  .. availability:: Linux >= 2.6.38.

     Một số kiểu thuật toán yêu cầu Kernel mới hơn.

  .. versionadded:: 3.6

- :const:`AF_VSOCK` cho phép giao tiếp giữa các máy ảo và máy chủ của chúng. Các socket được biểu diễn dưới dạng một tuple ``(CID, port)``, trong đó context ID hoặc CID và port là các số nguyên.

  .. availability:: Linux >= 3.9

     Xem :manpage:`vsock(7)`

  .. versionadded:: 3.7

- :const:`AF_PACKET` là một giao diện cấp thấp kết nối trực tiếp với các thiết bị mạng. Các địa chỉ được biểu diễn bằng tuple ``(ifname, proto[, pkttype[, hatype[, addr]]])``, trong đó:

  - *ifname* - Chuỗi chỉ định tên thiết bị.
  - *proto* - Số giao thức Ethernet. Có thể là :data:`ETH_P_ALL` để bắt tất cả giao thức, một trong các hằng số :ref:`ETHERTYPE_* <socket-ethernet-types>` hoặc bất kỳ số giao thức Ethernet nào khác.
  - *pkttype* - Số nguyên tùy chọn chỉ định loại gói tin:

    - ``PACKET_HOST`` (mặc định) - Gói tin được gửi đến máy chủ cục bộ.
    - ``PACKET_BROADCAST`` - Gói tin broadcast ở tầng vật lý.
    - ``PACKET_MULTICAST`` - Gói tin được gửi đến một địa chỉ multicast ở tầng vật lý.
    - ``PACKET_OTHERHOST`` - Gói tin gửi đến một máy chủ khác nhưng bị driver thiết bị bắt ở chế độ promiscuous.
    - ``PACKET_OUTGOING`` - Gói tin bắt nguồn từ máy chủ cục bộ và được loopback về một packet socket.
  - *hatype* - Số nguyên tùy chọn chỉ định loại địa chỉ phần cứng ARP.
  - *addr* - Đối tượng giống bytes tùy chọn chỉ định địa chỉ vật lý phần cứng, cách diễn giải địa chỉ này phụ thuộc vào thiết bị.

  .. availability:: Linux >= 2.2.

- :const:`AF_QIPCRTR` là một interface dựa trên socket chỉ dành cho Linux để giao tiếp với các service chạy trên co-processor trong các nền tảng Qualcomm. Họ địa chỉ được biểu diễn dưới dạng một tuple ``(node, port)``, trong đó *node* và *port* là các số nguyên không âm.

  .. availability:: Linux >= 4.7.

  .. versionadded:: 3.8

- :const:`IPPROTO_UDPLITE` là một biến thể của UDP cho phép bạn chỉ định phần nào của gói tin được kiểm tra bằng checksum. Nó bổ sung hai socket option mà bạn có thể thay đổi. ``self.setsockopt(IPPROTO_UDPLITE, UDPLITE_SEND_CSCOV, length)`` sẽ thay đổi phần của các gói tin gửi đi được kiểm tra bằng checksum, còn ``self.setsockopt(IPPROTO_UDPLITE, UDPLITE_RECV_CSCOV, length)`` sẽ lọc các gói tin kiểm tra quá ít dữ liệu của chúng. Trong cả hai trường hợp, ``length`` phải nằm trong ``range(8, 2**16, 8)``.

  Một socket như vậy phải được tạo bằng ``socket(AF_INET, SOCK_DGRAM, IPPROTO_UDPLITE)`` cho IPv4 hoặc ``socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDPLITE)`` cho IPv6.

  .. availability:: Linux >= 2.6.20, FreeBSD >= 10.1

  .. versionadded:: 3.9

- :const:`AF_HYPERV` là một giao diện dựa trên socket chỉ có trên Windows để giao tiếp với các máy chủ và máy khách Hyper-V. Họ địa chỉ được biểu diễn dưới dạng một tuple ``(vm_id, service_id)``, trong đó ``vm_id`` và ``service_id`` là các chuỗi UUID.

  ``vm_id`` là mã định danh máy ảo hoặc một tập hợp các giá trị VMID đã biết nếu đích không phải là một máy ảo cụ thể. Các hằng số VMID đã biết được định nghĩa trên ``socket`` là:

  - ``HV_GUID_ZERO``
  - ``HV_GUID_BROADCAST``
  - ``HV_GUID_WILDCARD`` - Dùng để bind chính nó và chấp nhận kết nối từ tất cả các partition.
  - ``HV_GUID_CHILDREN`` - Dùng để bind chính nó và chấp nhận kết nối từ các partition con.
  - ``HV_GUID_LOOPBACK`` - Dùng làm đích đến chính nó.
  - ``HV_GUID_PARENT`` - Khi được dùng làm bind, nó chấp nhận kết nối từ partition cha. Khi được dùng làm địa chỉ đích, nó sẽ kết nối đến partition cha.

  ``service_id`` là mã định danh dịch vụ của dịch vụ đã đăng ký.

  .. versionadded:: 3.12

Nếu sử dụng tên máy chủ trong phần *host* của địa chỉ socket IPv4/v6, chương trình có thể biểu hiện hành vi không xác định, vì Python sử dụng địa chỉ đầu tiên được trả về từ quá trình phân giải DNS. Địa chỉ socket sẽ được phân giải thành một địa chỉ IPv4/v6 thực tế theo cách khác nhau, tùy thuộc vào kết quả phân giải DNS và/hoặc cấu hình máy chủ. Để có hành vi xác định, hãy sử dụng địa chỉ dạng số trong phần *host*.

Tất cả lỗi đều phát sinh ngoại lệ. Các ngoại lệ thông thường đối với kiểu đối số không hợp lệ và tình trạng hết bộ nhớ có thể được phát sinh. Các lỗi liên quan đến ngữ nghĩa của socket hoặc địa chỉ sẽ phát sinh :exc:`OSError` hoặc một trong các lớp con của nó.

Chế độ không chặn được hỗ trợ thông qua :meth:`~socket.setblocking`. Một dạng tổng quát hóa dựa trên thời gian chờ được hỗ trợ thông qua
:meth:`~socket.settimeout`.


Nội dung mô-đun
---------------

Mô-đun :mod:`!socket` xuất các thành phần sau.


Ngoại lệ
^^^^^^^^

.. exception:: error

   Một bí danh đã lỗi thời của :exc:`OSError`.

   .. versionchanged:: 3.3
      Sau :pep:`3151`, lớp này được đặt làm bí danh của :exc:`OSError`.


.. exception:: herror

   Là một lớp con của :exc:`OSError`, ngoại lệ này được phát sinh đối với các lỗi liên quan đến địa chỉ, tức là đối với các hàm sử dụng *h_errno* trong POSIX C API, bao gồm :func:`gethostbyname_ex` và :func:`gethostbyaddr`. Giá trị đi kèm là một cặp ``(h_errno, string)`` biểu thị một lỗi do lệnh gọi thư viện trả về. *h_errno* là một giá trị số, còn *string* biểu thị mô tả của *h_errno*, do hàm
   :c:func:`hstrerror` C trả về.

   .. versionchanged:: 3.3
      Lớp này đã được chuyển thành lớp con của :exc:`OSError`.

.. exception:: gaierror

   Là một lớp con của :exc:`OSError`, ngoại lệ này được phát sinh đối với các lỗi liên quan đến địa chỉ bởi :func:`getaddrinfo` và :func:`getnameinfo`. Giá trị đi kèm là một cặp ``(error, string)`` biểu thị một lỗi do lệnh gọi thư viện trả về. *string* biểu thị mô tả của *error*, do hàm C :c:func:`gai_strerror` trả về. Giá trị số của *error* sẽ khớp với một trong các hằng số :const:`!EAI_\*` được định nghĩa trong mô-đun này.

   .. versionchanged:: 3.3
      Lớp này đã được chuyển thành lớp con của :exc:`OSError`.

.. exception:: timeout

   Bí danh đã lỗi thời của :exc:`TimeoutError`.

   Là một lớp con của :exc:`OSError`, ngoại lệ này được phát sinh khi xảy ra timeout trên một socket đã bật timeout thông qua một lần gọi trước đó đến
   :meth:`~socket.settimeout` (hoặc ngầm định thông qua
   :func:`~socket.setdefaulttimeout`). Giá trị đi kèm là một chuỗi mà hiện tại luôn có giá trị là "timed out".

   .. versionchanged:: 3.3
      Lớp này đã được chuyển thành lớp con của :exc:`OSError`.

   .. versionchanged:: 3.10
      Lớp này đã trở thành bí danh của :exc:`TimeoutError`.


Hằng số
^^^^^^^

Các hằng số AF_* và SOCK_* hiện là :class:`AddressFamily` và
:class:`SocketKind` :class:`.IntEnum` collections.

.. versionadded:: 3.4

.. data:: AF_UNIX
          AF_INET AF_INET6

   Các hằng số này đại diện cho các họ địa chỉ (và giao thức), được dùng làm đối số đầu tiên cho :func:`~socket.socket`. Nếu hằng số :const:`AF_UNIX` không được định nghĩa thì giao thức này không được hỗ trợ. Tùy thuộc vào hệ thống, có thể có thêm các hằng số khác.

.. data:: AF_UNSPEC

   :const:`AF_UNSPEC` có nghĩa là
   :func:`getaddrinfo` sẽ trả về các địa chỉ socket cho bất kỳ họ địa chỉ nào (IPv4, IPv6 hoặc bất kỳ họ nào khác) có thể được sử dụng.

.. data:: SOCK_STREAM
          SOCK_DGRAM SOCK_RAW SOCK_RDM SOCK_SEQPACKET

   Các hằng số này biểu thị các loại socket, được dùng làm đối số thứ hai cho
   :func:`~socket.socket`. Có thể có thêm các hằng số tùy thuộc vào hệ thống. (Chỉ :const:`SOCK_STREAM` và :const:`SOCK_DGRAM` dường như thường hữu ích.)

.. data:: SOCK_CLOEXEC
          SOCK_NONBLOCK

   Nếu được định nghĩa, hai hằng số này có thể được kết hợp với các loại socket và cho phép bạn thiết lập một số cờ một cách nguyên tử (do đó tránh các điều kiện tranh chấp có thể xảy ra và nhu cầu thực hiện các lệnh gọi riêng biệt).

   .. seealso::

      `Xử lý bộ mô tả tệp an toàn <https://udrepper.livejournal.com/20407.html>`_ để xem phần giải thích chi tiết hơn.

   .. availability:: Linux >= 2.6.27.

   .. versionadded:: 3.2

.. _socket-unix-constants:

.. data:: SO_*
          SOMAXCONN MSG_* SOL_* SCM_* IPPROTO_* IPPORT_* INADDR_* IP_* IPV6_* EAI_* AI_* NI_* TCP_*

   Nhiều hằng số có các dạng này, được ghi chép trong tài liệu Unix về socket và/hoặc giao thức IP, cũng được định nghĩa trong module socket. Chúng thường được dùng làm đối số cho các phương thức :meth:`~socket.setsockopt` và :meth:`~socket.getsockopt` của các đối tượng socket. Trong hầu hết trường hợp, chỉ những ký hiệu được định nghĩa trong các tệp header Unix mới được định nghĩa; đối với một vài ký hiệu, các giá trị mặc định được cung cấp.

   .. versionchanged:: 3.6
      Đã bổ sung ``SO_DOMAIN``, ``SO_PROTOCOL``, ``SO_PEERSEC``, ``SO_PASSSEC``, ``TCP_USER_TIMEOUT``, ``TCP_CONGESTION``.

   .. versionchanged:: 3.6.5
      Đã bổ sung hỗ trợ cho ``TCP_FASTOPEN``, ``TCP_KEEPCNT`` trên các nền tảng Windows khi khả dụng.

   .. versionchanged:: 3.7
      Đã bổ sung ``TCP_NOTSENT_LOWAT``.

      Đã bổ sung hỗ trợ cho ``TCP_KEEPIDLE``, ``TCP_KEEPINTVL`` trên các nền tảng Windows khi khả dụng.

   .. versionchanged:: 3.10
      Đã bổ sung ``IP_RECVTOS``.
       Đã bổ sung ``TCP_KEEPALIVE``. Trên MacOS, hằng số này có thể được sử dụng giống như ``TCP_KEEPIDLE`` trên Linux.

   .. versionchanged:: 3.11
      Đã bổ sung ``TCP_CONNECTION_INFO``. Trên MacOS, hằng số này có thể được sử dụng giống như ``TCP_INFO`` trên Linux và BSD.

   .. versionchanged:: 3.12
      Đã thêm ``SO_RTABLE`` và ``SO_USER_COOKIE``. Trên OpenBSD và FreeBSD, các hằng số tương ứng này có thể được sử dụng theo cách ``SO_MARK`` được sử dụng trên Linux. Đồng thời đã thêm các tùy chọn socket TCP còn thiếu từ Linux: ``TCP_MD5SIG``, ``TCP_THIN_LINEAR_TIMEOUTS``, ``TCP_THIN_DUPACK``, ``TCP_REPAIR``, ``TCP_REPAIR_QUEUE``, ``TCP_QUEUE_SEQ``, ``TCP_REPAIR_OPTIONS``, ``TCP_TIMESTAMP``, ``TCP_CC_INFO``, ``TCP_SAVE_SYN``, ``TCP_SAVED_SYN``, ``TCP_REPAIR_WINDOW``, ``TCP_FASTOPEN_CONNECT``, ``TCP_ULP``, ``TCP_MD5SIG_EXT``, ``TCP_FASTOPEN_KEY``, ``TCP_FASTOPEN_NO_COOKIE``, ``TCP_ZEROCOPY_RECEIVE``, ``TCP_INQ``, ``TCP_TX_DELAY``. Đã thêm ``IP_PKTINFO``, ``IP_UNBLOCK_SOURCE``, ``IP_BLOCK_SOURCE``, ``IP_ADD_SOURCE_MEMBERSHIP``, ``IP_DROP_SOURCE_MEMBERSHIP``.

   .. versionchanged:: 3.13
      Đã thêm ``SO_BINDTOIFINDEX``. Trên Linux, hằng số này có thể được sử dụng theo cách ``SO_BINDTODEVICE`` được sử dụng, nhưng với chỉ mục của network interface thay vì tên của nó.

   .. versionchanged:: 3.14
      Đã thêm ``IP_FREEBIND``, ``IP_RECVERR``, ``IPV6_RECVERR``, ``IP_RECVTTL`` và ``IP_RECVORIGDSTADDR`` còn thiếu trên Linux.

   .. versionchanged:: 3.14
      Đã thêm hỗ trợ cho ``TCP_QUICKACK`` trên các nền tảng Windows khi khả dụng.


.. data:: AF_CAN
          PF_CAN SOL_CAN_* CAN_*

   Nhiều hằng số thuộc các dạng này, được ghi lại trong tài liệu Linux, cũng được định nghĩa trong socket module.

   .. availability:: Linux >= 2.6.25, NetBSD >= 8.

   .. versionadded:: 3.3

   .. versionchanged:: 3.11
      Đã bổ sung hỗ trợ NetBSD.

   .. versionchanged:: 3.14
      Đã khôi phục ``CAN_RAW_ERR_FILTER`` bị thiếu trên Linux.

.. data:: CAN_BCM
          CAN_BCM_*

   CAN_BCM, trong họ giao thức CAN, là giao thức broadcast manager (BCM). Các hằng số của broadcast manager, được ghi chép trong tài liệu Linux, cũng được định nghĩa trong mô-đun socket.

   .. availability:: Linux >= 2.6.25.

   .. note::
      Cờ :data:`CAN_BCM_CAN_FD_FRAME` chỉ khả dụng trên Linux >= 4.8.

   .. versionadded:: 3.4

.. data:: CAN_RAW_FD_FRAMES

   Bật hỗ trợ CAN FD trong socket CAN_RAW. Theo mặc định, tính năng này bị tắt. Điều này cho phép ứng dụng gửi cả frame CAN và CAN FD; tuy nhiên, khi đọc từ socket, bạn phải chấp nhận cả frame CAN và CAN FD.

   Hằng số này được ghi chép trong tài liệu Linux.

   .. availability:: Linux >= 3.6.

   .. versionadded:: 3.5

.. data:: CAN_RAW_JOIN_FILTERS

   Kết hợp các bộ lọc CAN đã áp dụng sao cho chỉ những frame CAN khớp với tất cả các bộ lọc CAN đã cho mới được chuyển đến không gian người dùng.

   Hằng số này được ghi chép trong tài liệu Linux.

   .. availability:: Linux >= 4.1.

   .. versionadded:: 3.9

.. data:: CAN_ISOTP

   CAN_ISOTP, trong họ giao thức CAN, là giao thức ISO-TP (ISO 15765-2). Các hằng số ISO-TP được ghi chép trong tài liệu Linux.

   .. availability:: Linux >= 2.6.25.

   .. versionadded:: 3.7

.. data:: CAN_J1939

   CAN_J1939, trong họ giao thức CAN, là giao thức SAE J1939. Các hằng số J1939 được ghi chép trong tài liệu Linux.

   .. availability:: Linux >= 5.4.

   .. versionadded:: 3.9


.. data:: AF_DIVERT
          PF_DIVERT

   Hai hằng số này, được ghi chép trong trang hướng dẫn divert(4) của FreeBSD, cũng được định nghĩa trong module socket.

   .. availability:: FreeBSD >= 14.0.

   .. versionadded:: 3.12


.. data:: AF_PACKET
          PF_PACKET PACKET_*

   Nhiều hằng số thuộc các dạng này, được ghi lại trong tài liệu Linux, cũng được định nghĩa trong socket module.

   .. availability:: Linux >= 2.2.


.. data:: ETH_P_ALL

   :data:`!ETH_P_ALL` có thể được sử dụng trong hàm khởi tạo :class:`~socket.socket` dưới dạng *proto* cho họ :const:`AF_PACKET` để bắt mọi gói tin, bất kể giao thức.

   Để biết thêm thông tin, hãy xem trang man :manpage:`packet(7)`.

   .. availability:: Linux.

   .. versionadded:: 3.12


.. data:: AF_RDS
          PF_RDS SOL_RDS RDS_*

   Nhiều hằng số thuộc các dạng này, được ghi lại trong tài liệu Linux, cũng được định nghĩa trong socket module.

   .. availability:: Linux >= 2.6.30.

   .. versionadded:: 3.3


.. data:: SIO_RCVALL
          SIO_KEEPALIVE_VALS SIO_LOOPBACK_FAST_PATH RCVALL_*

   Các hằng số dành cho WSAIoctl() của Windows. Các hằng số này được dùng làm đối số cho
   phương thức :meth:`~socket.socket.ioctl` của các đối tượng socket.

   .. versionchanged:: 3.6
      ``SIO_LOOPBACK_FAST_PATH`` đã được thêm vào.


.. data:: TIPC_*

   Các hằng số liên quan đến TIPC, tương ứng với những hằng số được API socket C xuất ra. Xem tài liệu TIPC để biết thêm thông tin.

.. data:: AF_ALG
          SOL_ALG ALG_*

   Các hằng số cho chức năng mật mã của Linux Kernel.

   .. availability:: Linux >= 2.6.38.

   .. versionadded:: 3.6


.. data:: AF_VSOCK
          IOCTL_VM_SOCKETS_GET_LOCAL_CID VMADDR* SO_VM*

   Các hằng số cho việc giao tiếp giữa máy chủ Linux và máy khách.

   .. availability:: Linux >= 4.8.

   .. versionadded:: 3.7

.. data:: AF_LINK

  .. availability:: BSD, macOS.

  .. versionadded:: 3.4

.. data:: has_ipv6

   Hằng số này chứa một giá trị boolean cho biết IPv6 có được nền tảng này hỗ trợ hay không.

.. data:: AF_BLUETOOTH
          BTPROTO_L2CAP BTPROTO_RFCOMM BTPROTO_HCI BTPROTO_SCO

   Các hằng số kiểu Integer dùng với địa chỉ Bluetooth.

.. data:: BDADDR_ANY
          BDADDR_LOCAL

   Đây là các hằng số chuỗi chứa địa chỉ Bluetooth với những ý nghĩa đặc biệt. Ví dụ: :const:`BDADDR_ANY` có thể được dùng để chỉ bất kỳ địa chỉ nào khi chỉ định socket binding với
   :const:`BTPROTO_RFCOMM`.

.. data:: BDADDR_BREDR
          BDADDR_LE_PUBLIC BDADDR_LE_RANDOM

   Các hằng số này mô tả loại địa chỉ Bluetooth khi binding hoặc kết nối một socket :const:`BTPROTO_L2CAP`.

   .. availability:: Linux, FreeBSD

   .. versionadded:: 3.14

.. data:: SOL_RFCOMM
          SOL_L2CAP SOL_HCI SOL_SCO SOL_BLUETOOTH

   Được dùng trong đối số level của :meth:`~socket.setsockopt` và
   Các phương thức :meth:`~socket.getsockopt` của đối tượng Bluetooth socket.

   :const:`SOL_BLUETOOTH` chỉ khả dụng trên Linux. Các hằng số khác khả dụng nếu giao thức tương ứng được hỗ trợ.

.. data:: SO_L2CAP_*
          L2CAP_LM L2CAP_LM_* SO_RFCOMM_* RFCOMM_LM_* SO_SCO_* SO_BTH_* BT_*

   Được sử dụng trong đối số tên tùy chọn và giá trị của các phương thức :meth:`~socket.setsockopt` và :meth:`~socket.getsockopt` của đối tượng Bluetooth socket.

   :const:`!BT_*` và :const:`L2CAP_LM` chỉ khả dụng trên Linux.
   :const:`!SO_BTH_*` chỉ khả dụng trên Windows. Các hằng số khác có thể khả dụng trên Linux và nhiều nền tảng BSD khác nhau.

   .. versionadded:: 3.14

.. data:: HCI_FILTER
          HCI_TIME_STAMP HCI_DATA_DIR SO_HCI_EVT_FILTER SO_HCI_PKT_FILTER

   Tên tùy chọn dùng với :const:`BTPROTO_HCI`. Tính khả dụng và định dạng của các giá trị tùy chọn phụ thuộc vào nền tảng.

   .. versionchanged:: 3.14
      Đã thêm :const:`!SO_HCI_EVT_FILTER` và :const:`!SO_HCI_PKT_FILTER` trên NetBSD và DragonFly BSD. Đã thêm :const:`!HCI_DATA_DIR` trên FreeBSD, NetBSD và DragonFly BSD.

.. data:: HCI_DEV_NONE

   Giá trị ``device_id`` dùng để tạo một socket HCI không dành riêng cho một bộ điều hợp Bluetooth cụ thể.

   .. availability:: Linux

   .. versionadded:: 3.14

.. data:: HCI_CHANNEL_RAW
          HCI_CHANNEL_USER HCI_CHANNEL_MONITOR HCI_CHANNEL_CONTROL HCI_CHANNEL_LOGGING

   Các giá trị có thể có cho trường ``channel`` trong địa chỉ :const:`BTPROTO_HCI`.

   .. availability:: Linux

   .. versionadded:: 3.14

.. data:: AF_QIPCRTR

   Hằng số cho giao thức bộ định tuyến IPC của Qualcomm, được dùng để giao tiếp với dịch vụ cung cấp các bộ xử lý từ xa.

   .. availability:: Linux >= 4.7.

.. data:: SCM_CREDS2
          LOCAL_CREDS LOCAL_CREDS_PERSISTENT

   LOCAL_CREDS và LOCAL_CREDS_PERSISTENT có thể được sử dụng với các socket SOCK_DGRAM, SOCK_STREAM, tương đương với SO_PASSCRED của Linux/DragonFlyBSD; trong khi LOCAL_CREDS gửi thông tin xác thực khi đọc lần đầu, LOCAL_CREDS_PERSISTENT gửi thông tin này ở mỗi lần đọc; với loại thông báo sau, phải sử dụng SCM_CREDS2.

   .. versionadded:: 3.11

   .. availability:: FreeBSD.

.. data:: SO_INCOMING_CPU

   Hằng số để tối ưu tính cục bộ của CPU, được sử dụng cùng với
   :data:`SO_REUSEPORT`.

   .. versionadded:: 3.11

   .. availability:: Linux >= 3.9

.. data:: SO_REUSEPORT_LB

   Hằng số để bật việc liên kết trùng lặp địa chỉ và cổng với tính năng load balancing.

  .. versionadded:: 3.14

  .. availability:: FreeBSD >= 12.0

.. data:: AF_HYPERV
          HV_PROTOCOL_RAW HVSOCKET_CONNECT_TIMEOUT HVSOCKET_CONNECT_TIMEOUT_MAX HVSOCKET_CONNECTED_SUSPEND HVSOCKET_ADDRESS_FLAG_PASSTHRU HV_GUID_ZERO HV_GUID_WILDCARD HV_GUID_BROADCAST HV_GUID_CHILDREN HV_GUID_LOOPBACK HV_GUID_PARENT

   Các hằng số cho Hyper-V sockets của Windows để giao tiếp giữa host và guest.

   .. availability:: Windows.

   .. versionadded:: 3.12

.. _socket-ethernet-types:

.. data:: ETHERTYPE_ARP
          ETHERTYPE_IP ETHERTYPE_IPV6 ETHERTYPE_VLAN

   `số giao thức IEEE 802.3 <https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.txt>`_. các hằng số.

   .. availability:: Linux, FreeBSD, macOS.

   .. versionadded:: 3.12

.. data:: SHUT_RD
          SHUT_WR SHUT_RDWR

   Các hằng số này được phương thức :meth:`~socket.socket.shutdown` của các đối tượng socket sử dụng.

   .. availability:: not WASI.

Các hàm
^^^^^^^

Tạo socket
''''''''''

Các hàm sau đây đều tạo :ref:`đối tượng socket <socket-objects>`.


Hàm khởi tạo lớp :class:`socket <socket.socket>` tạo trực tiếp một socket mới; xem :ref:`socket-objects` để biết các tham số và mô tả đầy đủ.

.. function:: socketpair([family[, type[, proto]]])

   Tạo một cặp đối tượng socket được kết nối bằng cách sử dụng họ địa chỉ, loại socket và số giao thức đã cho. Họ địa chỉ, loại socket và số giao thức giống như đối với hàm :func:`~socket.socket`. Họ địa chỉ mặc định là :const:`AF_UNIX` nếu được định nghĩa trên nền tảng; nếu không, giá trị mặc định là :const:`AF_INET`.

   Các socket mới được tạo là :ref:`không thể kế thừa <fd_inheritance>`.

   .. versionchanged:: 3.2
      Các đối tượng socket được trả về giờ đây hỗ trợ toàn bộ socket API thay vì chỉ một phần.

   .. versionchanged:: 3.4
      Các socket được trả về giờ đây không thể kế thừa.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ Windows.


.. function:: create_connection(address, timeout=GLOBAL_DEFAULT, source_address=None, *, all_errors=False)

   Kết nối đến một dịch vụ TCP đang lắng nghe trên *địa chỉ* internet (một bộ 2 giá trị ``(host, port)``) và trả về đối tượng socket. Đây là một hàm cấp cao hơn :meth:`socket.connect`: nếu *tên máy chủ* không phải là tên máy chủ dạng số, hàm sẽ thử phân giải tên đó cho cả :data:`AF_INET` và :data:`AF_INET6`, sau đó lần lượt thử kết nối đến tất cả các địa chỉ có thể cho đến khi kết nối thành công. Điều này giúp dễ dàng viết các client tương thích với cả IPv4 và IPv6.

   Việc truyền tham số tùy chọn *thời gian chờ* sẽ thiết lập thời gian chờ trên instance socket trước khi thử kết nối. Nếu không cung cấp *thời gian chờ*, thiết lập thời gian chờ mặc định toàn cục được trả về bởi
   :func:`getdefaulttimeout` sẽ được sử dụng.

   Nếu được cung cấp, *source_address* phải là một bộ 2 phần ``(host, port)`` để socket liên kết với nó làm địa chỉ nguồn trước khi kết nối. Nếu host hoặc port lần lượt là '' hoặc 0, hành vi mặc định của hệ điều hành sẽ được sử dụng.

   Khi không thể tạo kết nối, một ngoại lệ sẽ được phát sinh. Theo mặc định, đó là ngoại lệ từ địa chỉ cuối cùng trong danh sách. Nếu *all_errors* là ``True``, đó là một :exc:`ExceptionGroup` chứa các lỗi của mọi lần thử.

   .. versionchanged:: 3.2
      *source_address* đã được thêm.

   .. versionchanged:: 3.11
      *all_errors* đã được thêm.


.. function:: create_server(address, *, family=AF_INET, backlog=None, reuse_port=False, dualstack_ipv6=False)

   Hàm tiện ích tạo một TCP socket liên kết với *address* (một bộ 2 phần ``(host, port)``) và trả về đối tượng socket.

   *family* phải là :data:`AF_INET` hoặc :data:`AF_INET6`. *backlog* là kích thước hàng đợi được truyền cho :meth:`socket.listen`; nếu không được chỉ định, một giá trị mặc định hợp lý sẽ được chọn. *reuse_port* quy định có đặt tùy chọn socket :data:`SO_REUSEPORT` hay không.

   Nếu *dualstack_ipv6* là true, *family* là :data:`AF_INET6` và nền tảng hỗ trợ tính năng này, socket sẽ có thể chấp nhận cả kết nối IPv4 và IPv6; nếu không, nó sẽ phát sinh :exc:`ValueError`. Hầu hết các nền tảng POSIX và Windows được cho là hỗ trợ chức năng này. Khi chức năng này được bật, địa chỉ được trả về bởi
   :meth:`socket.getpeername` khi xảy ra kết nối IPv4 sẽ là một địa chỉ IPv6 được biểu diễn dưới dạng địa chỉ IPv6 ánh xạ IPv4. Nếu *dualstack_ipv6* là false, tham số này sẽ tắt rõ ràng chức năng đó trên các nền tảng bật chức năng này theo mặc định (ví dụ: Linux). Có thể sử dụng tham số này cùng với :func:`has_dualstack_ipv6`:

   ::

     import socket

     addr = ("", 8080)  # tất cả interface, cổng 8080
     if socket.has_dualstack_ipv6():
         s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
     else:
         s = socket.create_server(addr)

   .. note::
    Trên các nền tảng POSIX, tùy chọn socket :data:`SO_REUSEADDR` được thiết lập để ngay lập tức sử dụng lại các socket trước đó đã được bind trên cùng *address* và vẫn ở trạng thái TIME_WAIT.

   .. versionadded:: 3.8

.. function:: has_dualstack_ipv6()

   Trả về ``True`` nếu nền tảng hỗ trợ tạo một TCP socket có thể xử lý cả kết nối IPv4 và IPv6.

   .. versionadded:: 3.8

.. function:: fromfd(fd, family, type, proto=0)

   Sao chép file descriptor *fd* (một số nguyên do phương thức của đối tượng tệp trả về)
   :meth:`~io.IOBase.fileno` phương thức) và xây dựng một đối tượng socket từ kết quả đó. Họ địa chỉ, kiểu socket và số giao thức được xác định như đối với hàm :func:`~socket.socket`. File descriptor phải tham chiếu đến một socket, nhưng điều này không được kiểm tra --- các thao tác tiếp theo trên đối tượng có thể thất bại nếu file descriptor không hợp lệ. Hàm này hiếm khi cần thiết, nhưng có thể được dùng để lấy hoặc đặt các tùy chọn socket trên một socket được truyền cho chương trình dưới dạng đầu vào hoặc đầu ra tiêu chuẩn (chẳng hạn như một server do Unix inet daemon khởi chạy). Socket được giả định đang ở chế độ blocking.

   Socket mới tạo không thể kế thừa (:ref:`non-inheritable <fd_inheritance>`).

   .. versionchanged:: 3.4
      Socket được trả về hiện không còn có thể kế thừa.


.. function:: fromshare(data)

   Khởi tạo một socket từ dữ liệu nhận được từ phương thức :meth:`socket.share`. Socket được giả định đang ở chế độ blocking.

   .. availability:: Windows.

   .. versionadded:: 3.3


Các hàm khác
''''''''''''

Mô-đun :mod:`!socket` cũng cung cấp nhiều dịch vụ liên quan đến mạng:


.. function:: close(fd)

   Đóng một bộ mô tả tệp socket. Thao tác này tương tự :func:`os.close`, nhưng dành cho socket. Trên một số nền tảng, đáng chú ý là Windows, :func:`os.close` không hoạt động với các bộ mô tả tệp socket.

   .. versionadded:: 3.7

.. function:: getaddrinfo(host, port, family=AF_UNSPEC, type=0, proto=0, flags=0)

   Hàm này bao bọc hàm C ``getaddrinfo`` của hệ thống bên dưới.

   Chuyển đổi đối số *host*/*port* thành một chuỗi gồm các bộ 5 phần tử chứa mọi đối số cần thiết để tạo một socket được kết nối đến dịch vụ đó. *host* có thể là tên miền, biểu diễn dạng chuỗi của địa chỉ IPv4/v6 hoặc ``None``. *port* có thể là tên dịch vụ dạng chuỗi như ``'http'``, số cổng hoặc ``None``. Bằng cách truyền ``None`` làm giá trị của *host* và *port*, bạn có thể truyền ``NULL`` đến API C bên dưới.

   Các đối số *family*, *type* và *proto* có thể được chỉ định tùy chọn để cung cấp các tùy chọn và giới hạn danh sách địa chỉ được trả về. Truyền các giá trị mặc định của chúng (:data:`AF_UNSPEC`, 0 và 0, tương ứng) để không giới hạn kết quả. Xem lưu ý bên dưới để biết chi tiết.

   Đối số *flags* có thể là một hoặc nhiều hằng số ``AI_*``, và sẽ ảnh hưởng đến cách tính toán và trả về kết quả. Ví dụ, :const:`AI_NUMERICHOST` sẽ vô hiệu hóa việc phân giải tên miền và gây ra lỗi nếu *host* là một tên miền.

   Hàm trả về một danh sách các tuple 5 phần tử có cấu trúc sau:

   ``(family, type, proto, canonname, sockaddr)``

   Trong các tuple này, *family*, *type*, *proto* đều là số nguyên và được dùng để truyền vào hàm :func:`~socket.socket`. *canonname* sẽ là một chuỗi biểu thị tên chuẩn của *host* nếu
   :const:`AI_CANONNAME` là một phần của đối số *flags*; nếu không, *canonname* sẽ trống.  *sockaddr* là một tuple mô tả địa chỉ socket, có định dạng phụ thuộc vào *family* được trả về (một ``(address, port)`` 2-tuple cho
   :const:`AF_INET`, một ``(address, port, flowinfo, scope_id)`` 4-tuple cho
   :const:`AF_INET6`), và được dùng để truyền vào phương thức :meth:`socket.connect`.

   .. note::

      Nếu bạn định sử dụng kết quả từ :func:`!getaddrinfo` để tạo một socket (thay vì, chẳng hạn, truy xuất *canonname*), hãy cân nhắc giới hạn kết quả theo *type* (ví dụ: :data:`SOCK_STREAM` hoặc
      :data:`SOCK_DGRAM`) và/hoặc *proto* (ví dụ: :data:`IPPROTO_TCP` hoặc
      :data:`IPPROTO_UDP`) mà ứng dụng của bạn có thể xử lý.

      Hành vi đối với các giá trị mặc định của *family*, *type*, *proto* và *flags* phụ thuộc vào hệ thống.

      Nhiều hệ thống (chẳng hạn như hầu hết các cấu hình Linux) sẽ trả về danh sách đã sắp xếp gồm tất cả các địa chỉ phù hợp. Thông thường, bạn nên thử các địa chỉ này theo thứ tự cho đến khi kết nối thành công (có thể thử song song, chẳng hạn bằng thuật toán `Happy Eyeballs <Happy Eyeballs_>`_). Trong những trường hợp này, việc giới hạn *type* và/hoặc *proto* có thể giúp loại bỏ các lần thử kết nối không thành công hoặc không thể sử dụng.

      Tuy nhiên, một số hệ thống sẽ chỉ trả về một địa chỉ duy nhất. (Chẳng hạn, điều này đã được ghi nhận trên các cấu hình Solaris và AIX.) Trên những hệ thống này, việc giới hạn *type* và/hoặc *proto* giúp đảm bảo địa chỉ này có thể sử dụng được.

   .. audit-event:: socket.getaddrinfo host,port,family,type,protocol socket.getaddrinfo

   Ví dụ sau đây lấy thông tin địa chỉ cho một kết nối TCP giả định tới ``example.org`` trên cổng 80 (kết quả có thể khác trên hệ thống của bạn nếu IPv6 chưa được bật)::

      >>> socket.getaddrinfo("example.org", 80, proto=socket.IPPROTO_TCP)
      [(socket.AF_INET6, socket.SOCK_STREAM,
       6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
       (socket.AF_INET, socket.SOCK_STREAM,
       6, '', ('93.184.216.34', 80))]

   .. versionchanged:: 3.2
      Các tham số giờ đây có thể được truyền bằng đối số từ khóa.

   .. versionchanged:: 3.7
      đối với các địa chỉ multicast IPv6, chuỗi biểu diễn một địa chỉ sẽ không chứa phần ``%scope_id``.

.. _Happy Eyeballs: https://en.wikipedia.org/wiki/Happy_Eyeballs

.. function:: getfqdn([name])

   Trả về tên miền đủ điều kiện cho *name*. Nếu *name* bị bỏ qua hoặc để trống, nó được hiểu là máy chủ cục bộ. Để tìm tên đầy đủ, tên máy chủ do :func:`gethostbyaddr` trả về sẽ được kiểm tra, sau đó là các bí danh của máy chủ, nếu có. Tên đầu tiên có chứa dấu chấm sẽ được chọn. Nếu không có tên miền đủ điều kiện nào và *name* đã được cung cấp, tên đó sẽ được trả về không thay đổi. Nếu *name* để trống hoặc bằng ``'0.0.0.0'``, tên máy chủ từ :func:`gethostname` sẽ được trả về.


.. function:: gethostbyname(hostname)

   Chuyển đổi tên máy chủ sang định dạng địa chỉ IPv4. Địa chỉ IPv4 được trả về dưới dạng chuỗi, chẳng hạn như ``'100.50.200.5'``. Nếu bản thân tên máy chủ là một địa chỉ IPv4, tên đó sẽ được trả về không thay đổi. Xem :func:`gethostbyname_ex` để biết giao diện đầy đủ hơn. :func:`gethostbyname` không hỗ trợ phân giải tên IPv6, và
   :func:`getaddrinfo` nên được sử dụng thay thế để hỗ trợ dual stack IPv4/v6.

   .. audit-event:: socket.gethostbyname hostname socket.gethostbyname

   .. availability:: not WASI.


.. function:: gethostbyname_ex(hostname)

   Chuyển đổi tên máy chủ sang định dạng địa chỉ IPv4, với giao diện mở rộng. Trả về một bộ 3 phần tử ``(hostname, aliaslist, ipaddrlist)``, trong đó *hostname* là tên máy chủ chính của máy chủ, *aliaslist* là một danh sách (có thể rỗng) các tên máy chủ thay thế cho cùng địa chỉ, còn *ipaddrlist* là danh sách các địa chỉ IPv4 cho cùng giao diện trên cùng máy chủ (thường nhưng không phải lúc nào cũng chỉ có một địa chỉ). :func:`gethostbyname_ex` không hỗ trợ phân giải tên IPv6, và thay vào đó nên sử dụng :func:`getaddrinfo` để hỗ trợ dual stack IPv4/v6.

   .. audit-event:: socket.gethostbyname hostname socket.gethostbyname_ex

   .. availability:: not WASI.


.. function:: gethostname()

   Trả về một chuỗi chứa tên máy chủ của máy mà trình thông dịch Python hiện đang thực thi.

   .. audit-event:: socket.gethostname "" socket.gethostname

   Lưu ý: :func:`gethostname` không phải lúc nào cũng trả về tên miền đầy đủ; hãy dùng :func:`getfqdn` cho mục đích đó.

   .. availability:: not WASI.


.. function:: gethostbyaddr(ip_address)

   Trả về một bộ 3 giá trị ``(hostname, aliaslist, ipaddrlist)``, trong đó *hostname* là tên máy chủ chính phản hồi *ip_address* đã cho, *aliaslist* là một danh sách (có thể rỗng) các tên máy chủ thay thế cho cùng địa chỉ đó, còn *ipaddrlist* là danh sách các địa chỉ IPv4/v6 cho cùng giao diện trên cùng máy chủ (nhiều khả năng chỉ chứa một địa chỉ). Để tìm tên miền đầy đủ, hãy dùng hàm :func:`getfqdn`. :func:`gethostbyaddr` hỗ trợ cả IPv4 và IPv6.

   .. audit-event:: socket.gethostbyaddr ip_address socket.gethostbyaddr

   .. availability:: not WASI.


.. function:: getnameinfo(sockaddr, flags)

   Chuyển đổi một địa chỉ socket *sockaddr* thành một bộ 2 giá trị ``(host, port)``. Tùy thuộc vào các thiết lập của *flags*, kết quả trong *host* có thể chứa tên miền đầy đủ hoặc biểu diễn địa chỉ dạng số. Tương tự, *port* có thể chứa tên cổng dạng chuỗi hoặc số cổng.

   Đối với các địa chỉ IPv6, ``%scope_id`` được nối vào phần host nếu *sockaddr* chứa *scope_id* có ý nghĩa. Điều này thường xảy ra với các địa chỉ multicast.

   Để biết thêm thông tin về *flags*, bạn có thể tham khảo :manpage:`getnameinfo(3)`.

   .. audit-event:: socket.getnameinfo sockaddr socket.getnameinfo

   .. availability:: not WASI.


.. function:: getprotobyname(protocolname)

   Chuyển đổi tên giao thức internet (ví dụ: ``'icmp'``) thành một hằng số phù hợp để truyền dưới dạng đối số thứ ba (tùy chọn) cho hàm :func:`~socket.socket`. Điều này thường chỉ cần thiết đối với các socket được mở ở chế độ "raw" (:const:`SOCK_RAW`); đối với các chế độ socket thông thường, giao thức chính xác sẽ được tự động chọn nếu giao thức bị bỏ qua hoặc có giá trị bằng không.

   .. availability:: not WASI.


.. function:: getservbyname(servicename[, protocolname])

   Chuyển đổi tên dịch vụ internet và tên giao thức thành số cổng cho dịch vụ đó. Tên giao thức tùy chọn, nếu được cung cấp, phải là ``'tcp'`` hoặc ``'udp'``; nếu không, mọi giao thức đều sẽ khớp.

   .. audit-event:: socket.getservbyname servicename,protocolname socket.getservbyname

   .. availability:: not WASI.


.. function:: getservbyport(port[, protocolname])

   Dịch số cổng Internet và tên giao thức thành tên dịch vụ tương ứng. Tên giao thức tùy chọn, nếu được cung cấp, phải là ``'tcp'`` hoặc ``'udp'``; nếu không, mọi giao thức đều khớp.

   .. audit-event:: socket.getservbyport port,protocolname socket.getservbyport

   .. availability:: not WASI.


.. function:: ntohl(x)

   Chuyển các số nguyên dương 32 bit từ thứ tự byte mạng sang thứ tự byte máy chủ. Trên các máy có thứ tự byte máy chủ giống thứ tự byte mạng, đây là thao tác không làm gì; nếu không, thao tác này thực hiện hoán đổi 4 byte.


.. function:: ntohs(x)

   Chuyển các số nguyên dương 16 bit từ thứ tự byte mạng sang thứ tự byte máy chủ. Trên các máy có thứ tự byte máy chủ giống thứ tự byte mạng, đây là thao tác không làm gì; nếu không, thao tác này thực hiện hoán đổi 2 byte.

   .. versionchanged:: 3.10
      Gây ra :exc:`OverflowError` nếu *x* không vừa với một số nguyên không dấu 16 bit.


.. function:: htonl(x)

   Chuyển các số nguyên dương 32 bit từ thứ tự byte máy chủ sang thứ tự byte mạng. Trên các máy có thứ tự byte máy chủ giống thứ tự byte mạng, đây là thao tác không làm gì; nếu không, thao tác này thực hiện hoán đổi 4 byte.


.. function:: htons(x)

   Chuyển các số nguyên dương 16 bit từ thứ tự byte máy chủ sang thứ tự byte mạng. Trên các máy có thứ tự byte máy chủ giống thứ tự byte mạng, đây là thao tác không làm gì; nếu không, thao tác này thực hiện hoán đổi 2 byte.

   .. versionchanged:: 3.10
      Gây ra :exc:`OverflowError` nếu *x* không vừa với một số nguyên không dấu 16 bit.


.. function:: inet_aton(ip_string)

   Chuyển đổi một địa chỉ IPv4 từ định dạng chuỗi dotted-quad (ví dụ: '123.45.67.89') sang định dạng nhị phân đóng gói 32 bit, dưới dạng đối tượng bytes có độ dài bốn ký tự. Điều này hữu ích khi giao tiếp với một chương trình sử dụng thư viện C chuẩn và cần các đối tượng thuộc kiểu :c:struct:`in_addr`, là kiểu C cho dữ liệu nhị phân đóng gói 32 bit mà hàm này trả về.

   :func:`inet_aton` cũng chấp nhận các chuỗi có ít hơn ba dấu chấm; hãy xem trang hướng dẫn Unix :manpage:`inet(3)` để biết chi tiết.

   Nếu chuỗi địa chỉ IPv4 được truyền cho hàm này không hợp lệ,
   :exc:`OSError` sẽ được phát sinh. Lưu ý rằng chính xác giá trị nào được xem là hợp lệ phụ thuộc vào cách triển khai C bên dưới của :c:func:`inet_aton`.

   :func:`inet_aton` không hỗ trợ IPv6, và nên sử dụng :func:`inet_pton` thay thế để hỗ trợ dual stack IPv4/v6.


.. function:: inet_ntoa(packed_ip)

   Chuyển đổi một địa chỉ IPv4 32 bit được đóng gói (một :term:`bytes-like object` dài bốn byte) sang biểu diễn chuỗi dotted-quad tiêu chuẩn (ví dụ: '123.45.67.89'). Điều này hữu ích khi giao tiếp với một chương trình sử dụng thư viện C chuẩn và cần các đối tượng thuộc kiểu :c:struct:`in_addr`, là kiểu C cho dữ liệu nhị phân đóng gói 32 bit mà hàm này nhận làm đối số.

   Nếu chuỗi byte được truyền cho hàm này không có độ dài chính xác là 4 byte, :exc:`OSError` sẽ được phát sinh. :func:`inet_ntoa` không hỗ trợ IPv6, và nên sử dụng :func:`inet_ntop` thay thế để hỗ trợ dual stack IPv4/v6.

   .. versionchanged:: 3.5
      Writable :term:`bytes-like object` hiện được chấp nhận.


.. function:: inet_pton(address_family, ip_string)

   Chuyển đổi địa chỉ IP từ định dạng chuỗi dành riêng cho họ địa chỉ sang định dạng nhị phân được đóng gói. :func:`inet_pton` hữu ích khi một thư viện hoặc giao thức mạng yêu cầu một đối tượng thuộc kiểu :c:struct:`in_addr` (tương tự như
   :func:`inet_aton`) hoặc :c:struct:`in6_addr`.

   Các giá trị được hỗ trợ cho *address_family* hiện là :const:`AF_INET` và
   :const:`AF_INET6`. Nếu chuỗi địa chỉ IP *ip_string* không hợp lệ,
   :exc:`OSError` sẽ được phát sinh. Lưu ý rằng giá trị nào được xem là hợp lệ phụ thuộc cả vào giá trị của *address_family* và cách triển khai bên dưới của
   :c:func:`inet_pton`.

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ Windows


.. function:: inet_ntop(address_family, packed_ip)

   Chuyển đổi địa chỉ IP dạng packed (một :term:`bytes-like object` gồm một số byte) thành biểu diễn chuỗi chuẩn, dành riêng cho từng family (ví dụ: ``'7.10.0.5'`` hoặc ``'5aef:2b::8'``).
   :func:`inet_ntop` hữu ích khi một thư viện hoặc giao thức mạng trả về một đối tượng thuộc kiểu :c:struct:`in_addr` (tương tự :func:`inet_ntoa`) hoặc
   :c:struct:`in6_addr`.

   Các giá trị được hỗ trợ cho *address_family* hiện là :const:`AF_INET` và
   :const:`AF_INET6`. Nếu đối tượng bytes *packed_ip* không có độ dài phù hợp với address family được chỉ định, :exc:`ValueError` sẽ được phát sinh.
   :exc:`OSError` được phát sinh đối với các lỗi từ lệnh gọi đến :func:`inet_ntop`.

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ Windows

   .. versionchanged:: 3.5
      Writable :term:`bytes-like object` hiện được chấp nhận.


..
   XXX: sendmsg(), recvmsg() và CMSG_*() có khả dụng trên bất kỳ nền tảng không phải Unix nào không? Dạng giao diện 4.2BSD cũ (đã lỗi thời?) trong đó struct msghdr không có các thành viên msg_control hoặc msg_controllen hiện chưa được hỗ trợ.

.. function:: CMSG_LEN(length)

   Trả về tổng độ dài, không bao gồm phần đệm ở cuối, của một mục dữ liệu phụ trợ có dữ liệu đi kèm với *length* đã cho. Giá trị này thường có thể được dùng làm kích thước bộ đệm cho :meth:`~socket.recvmsg` để nhận một mục dữ liệu phụ trợ duy nhất, nhưng :rfc:`3542` yêu cầu các ứng dụng có tính khả chuyển sử dụng :func:`CMSG_SPACE` và do đó phải bao gồm cả khoảng trống cho phần đệm, ngay cả khi mục đó là mục cuối cùng trong bộ đệm. Phát sinh :exc:`OverflowError` nếu *length* nằm ngoài phạm vi giá trị cho phép.

   .. availability:: Unix, not WASI.

      Hầu hết các nền tảng Unix.

   .. versionadded:: 3.3


.. function:: CMSG_SPACE(length)

   Trả về kích thước bộ đệm cần thiết để :meth:`~socket.recvmsg` nhận một mục dữ liệu phụ trợ có dữ liệu đi kèm với *length* đã cho, cùng với mọi phần đệm ở cuối. Khoảng trống bộ đệm cần thiết để nhận nhiều mục là tổng các giá trị :func:`CMSG_SPACE` tương ứng với độ dài dữ liệu đi kèm của chúng. Phát sinh
   :exc:`OverflowError` nếu *length* nằm ngoài phạm vi giá trị cho phép.

   Lưu ý rằng một số hệ thống có thể hỗ trợ dữ liệu phụ trợ mà không cung cấp hàm này. Cũng lưu ý rằng việc đặt kích thước bộ đệm bằng kết quả của hàm này có thể không giới hạn chính xác lượng dữ liệu phụ trợ có thể nhận, vì có thể có thêm dữ liệu vừa với vùng đệm.

   .. availability:: Unix, not WASI.

      hầu hết các nền tảng Unix.

   .. versionadded:: 3.3


.. function:: getdefaulttimeout()

   Trả về thời gian chờ mặc định tính bằng giây (float) cho các đối tượng socket mới. Giá trị ``None`` cho biết các đối tượng socket mới không có thời gian chờ. Khi module socket được import lần đầu, giá trị mặc định là ``None``.


.. function:: setdefaulttimeout(timeout)

   Đặt thời gian chờ mặc định tính bằng giây (float) cho các đối tượng socket mới. Khi module socket được import lần đầu, giá trị mặc định là ``None``. Xem
   :meth:`~socket.settimeout` để biết các giá trị có thể có và ý nghĩa tương ứng của chúng.


.. function:: sethostname(name)

   Đặt hostname của máy thành *name*. Thao tác này sẽ gây ra
   :exc:`OSError` nếu bạn không có đủ quyền.

   .. audit-event:: socket.sethostname name socket.sethostname

   .. availability:: Unix, not Android.

   .. versionadded:: 3.3


.. function:: if_nameindex()

   Trả về danh sách các tuple chứa thông tin về các network interface (index int, name string).
   :exc:`OSError` nếu system call không thành công.

   .. availability:: Unix, Windows, not WASI.

   .. versionadded:: 3.3

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ Windows.

   .. note::

      Trên Windows, các giao diện mạng có những tên khác nhau trong các ngữ cảnh khác nhau (tất cả tên dưới đây chỉ là ví dụ):

      * UUID: ``{FB605B73-AAC2-49A6-9A2F-25416AEA0573}``
      * name: ``ethernet_32770``
      * friendly name: ``vEthernet (nat)``
      * description: ``Hyper-V Virtual Ethernet Adapter``

      Hàm này trả về các tên thuộc dạng thứ hai trong danh sách, trong trường hợp ví dụ này là ``ethernet_32770``.


.. function:: if_nametoindex(if_name)

   Trả về số chỉ mục giao diện mạng tương ứng với tên giao diện.
   :exc:`OSError` nếu không tồn tại giao diện có tên đã cho.

   .. availability:: Unix, Windows, not WASI.

   .. versionadded:: 3.3

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ Windows.

   .. seealso::
      "Tên giao diện" là tên được mô tả trong :func:`if_nameindex`.


.. function:: if_indextoname(if_index)

   Trả về tên giao diện mạng tương ứng với số chỉ mục giao diện.
   :exc:`OSError` nếu không tồn tại giao diện có chỉ mục đã cho.

   .. availability:: Unix, Windows, not WASI.

   .. versionadded:: 3.3

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ Windows.

   .. seealso::
      "Tên giao diện" là tên được mô tả trong :func:`if_nameindex`.


.. function:: send_fds(sock, buffers, fds[, flags[, address]])

   Gửi danh sách bộ mô tả tệp *fds* qua một :const:`AF_UNIX` socket *sock*. Tham số *fds* là một chuỗi các bộ mô tả tệp. Tham khảo :meth:`~socket.sendmsg` để xem tài liệu về các tham số này.

   .. availability:: Unix, not WASI.

      Các nền tảng Unix hỗ trợ cơ chế :meth:`~socket.sendmsg` và :const:`SCM_RIGHTS`.

   .. versionadded:: 3.9


.. function:: recv_fds(sock, bufsize, maxfds[, flags])

   Nhận tối đa *maxfds* bộ mô tả tệp từ một :const:`AF_UNIX` socket *sock*. Trả về ``(msg, list(fds), flags, addr)``. Tham khảo :meth:`~socket.recvmsg` để xem tài liệu về các tham số này.

   .. availability:: Unix, not WASI.

      Các nền tảng Unix hỗ trợ cơ chế :meth:`~socket.recvmsg` và :const:`SCM_RIGHTS`.

   .. versionadded:: 3.9

   .. note::

      Mọi số nguyên bị cắt ngắn ở cuối danh sách các bộ mô tả tệp.


.. _socket-objects:

Đối tượng Socket
----------------

.. class:: socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)

   Tạo một socket mới bằng họ địa chỉ, kiểu socket và số giao thức đã cho. Họ địa chỉ phải là :const:`AF_INET` (mặc định),
   :const:`AF_INET6`, :const:`AF_UNIX`, :const:`AF_CAN`, :const:`AF_PACKET` hoặc :const:`AF_RDS`. Kiểu socket phải là :const:`SOCK_STREAM` (mặc định), :const:`SOCK_DGRAM`, :const:`SOCK_RAW` hoặc có thể là một trong các hằng số ``SOCK_`` khác. Số giao thức thường là 0 và có thể được bỏ qua; hoặc trong trường hợp họ địa chỉ là :const:`AF_CAN`, giao thức phải là một trong các giao thức :const:`CAN_RAW`, :const:`CAN_BCM`, :const:`CAN_ISOTP` hoặc
   :const:`CAN_J1939`.

   Nếu *fileno* được chỉ định, các giá trị cho *family*, *type* và *proto* sẽ được tự động phát hiện từ bộ mô tả tệp đã chỉ định. Có thể ghi đè tính năng tự động phát hiện bằng cách gọi hàm với các đối số *family*, *type* hoặc *proto* cụ thể. Điều này chỉ ảnh hưởng đến cách Python biểu diễn, chẳng hạn như giá trị trả về của :meth:`socket.getpeername`, chứ không ảnh hưởng đến tài nguyên thực tế của hệ điều hành. Không giống như
   :func:`socket.fromfd`, *fileno* sẽ trả về cùng một socket chứ không phải một bản sao. Điều này có thể giúp đóng một socket đã tách rời bằng cách sử dụng
   :meth:`~socket.socket.close`.

   Socket mới tạo là :ref:`không thể kế thừa <fd_inheritance>`.

   .. audit-event:: socket.__new__ self,family,type,protocol socket.socket

   .. versionchanged:: 3.3
      Họ AF_CAN đã được thêm vào. Họ AF_RDS đã được thêm vào.

   .. versionchanged:: 3.4
       Giao thức CAN_BCM đã được thêm vào.

   .. versionchanged:: 3.4
      Socket được trả về giờ đây không còn được kế thừa.

   .. versionchanged:: 3.7
       Giao thức CAN_ISOTP đã được thêm vào.

   .. versionchanged:: 3.7
      Khi các cờ bit :const:`SOCK_NONBLOCK` hoặc :const:`SOCK_CLOEXEC` được áp dụng cho *type*, chúng sẽ bị xóa, và
      :attr:`socket.type` sẽ không phản ánh chúng. Chúng vẫn được truyền đến lệnh gọi ``socket()`` của hệ thống bên dưới. Do đó,

      ::

          sock = socket.socket(
              socket.AF_INET,
              socket.SOCK_STREAM | socket.SOCK_NONBLOCK)

      vẫn sẽ tạo một socket không chặn trên các hệ điều hành hỗ trợ ``SOCK_NONBLOCK``, nhưng ``sock.type`` sẽ được đặt thành ``socket.SOCK_STREAM``.

   .. versionchanged:: 3.9
       Giao thức CAN_J1939 đã được thêm vào.

   .. versionchanged:: 3.10
       Giao thức IPPROTO_MPTCP đã được thêm vào.

   Các đối tượng socket có những phương thức sau. Ngoại trừ
   :meth:`~socket.makefile`, các phương thức này tương ứng với các lệnh gọi hệ thống Unix áp dụng cho socket.

   .. versionchanged:: 3.2
      Hỗ trợ cho giao thức :term:`context manager` đã được bổ sung. Việc thoát khỏi context manager tương đương với việc gọi :meth:`~socket.socket.close`.


   .. method:: accept()

      Chấp nhận một kết nối. Socket phải được liên kết với một địa chỉ và đang lắng nghe các kết nối. Giá trị trả về là một cặp ``(conn, address)`` trong đó *conn* là một đối tượng socket *new* có thể dùng để gửi và nhận dữ liệu trên kết nối, còn *address* là địa chỉ được liên kết với socket ở đầu kia của kết nối.

      Socket mới tạo là :ref:`không thể kế thừa <fd_inheritance>`.

      .. versionchanged:: 3.4
         Socket hiện không còn được kế thừa.

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


   .. method:: bind(address)

      Liên kết socket với *address*. Socket không được liên kết từ trước. Định dạng của *address* phụ thuộc vào họ địa chỉ --- xem :ref:`socket-addresses`.

      .. audit-event:: socket.bind self,address socket.socket.bind

      .. availability:: not WASI.


   .. method:: close()

      Đánh dấu socket là đã đóng. Tài nguyên hệ thống bên dưới (ví dụ: bộ mô tả tệp) cũng sẽ được đóng khi tất cả các đối tượng tệp từ :meth:`makefile` được đóng. Sau khi điều đó xảy ra, mọi thao tác tiếp theo trên đối tượng socket sẽ thất bại. Đầu bên kia sẽ không nhận thêm dữ liệu nào (sau khi dữ liệu đang xếp hàng được gửi hết).

      Socket sẽ tự động được đóng khi được thu gom rác, nhưng bạn nên :meth:`close` chúng một cách rõ ràng hoặc sử dụng
      câu lệnh :keyword:`with` bao quanh chúng.

      .. versionchanged:: 3.6
         :exc:`OSError` is now raised if an error occurs when the underlying
         :c:func:`!close` call is made.

      .. note::

         :meth:`close` giải phóng tài nguyên liên kết với một kết nối nhưng không nhất thiết đóng kết nối ngay lập tức. Nếu muốn đóng kết nối kịp thời, hãy gọi :meth:`shutdown` trước :meth:`close`.


   .. method:: connect(address)

      Kết nối với socket từ xa tại *address*. Định dạng của *address* phụ thuộc vào họ địa chỉ --- xem :ref:`socket-addresses`.

      Nếu kết nối bị gián đoạn bởi một tín hiệu, phương thức sẽ chờ cho đến khi kết nối hoàn tất hoặc phát sinh :exc:`TimeoutError` khi hết thời gian chờ, nếu trình xử lý tín hiệu không phát sinh ngoại lệ và socket đang ở chế độ blocking hoặc có thời gian chờ. Đối với socket non-blocking, phương thức sẽ phát sinh một
      :exc:`InterruptedError` ngoại lệ nếu kết nối bị gián đoạn bởi một tín hiệu (hoặc ngoại lệ do trình xử lý tín hiệu gây ra).

      .. audit-event:: socket.connect self,address socket.socket.connect

      .. versionchanged:: 3.5
         Phương thức này hiện chờ cho đến khi kết nối hoàn tất thay vì phát sinh một
         :exc:`InterruptedError` ngoại lệ nếu kết nối bị gián đoạn bởi một tín hiệu, trình xử lý tín hiệu không phát sinh ngoại lệ và socket đang ở chế độ blocking hoặc có thời gian chờ (xem :pep:`475` để biết lý do).

      .. availability:: not WASI.


   .. method:: connect_ex(address)

      Tương tự ``connect(address)``, nhưng trả về một chỉ báo lỗi thay vì phát sinh ngoại lệ đối với các lỗi do lời gọi :c:func:`!connect` ở cấp C trả về (các vấn đề khác, chẳng hạn như "không tìm thấy máy chủ", vẫn có thể phát sinh ngoại lệ). Chỉ báo lỗi là ``0`` nếu thao tác thành công; nếu không, đó là giá trị của
      biến :c:data:`errno`. Điều này hữu ích để hỗ trợ, chẳng hạn, các kết nối bất đồng bộ.

      .. audit-event:: socket.connect self,address socket.socket.connect_ex

      .. availability:: not WASI.

   .. method:: detach()

      Đưa đối tượng socket vào trạng thái đã đóng mà không thực sự đóng bộ mô tả tệp nền. Bộ mô tả tệp được trả về và có thể được tái sử dụng cho các mục đích khác.

      .. versionadded:: 3.2


   .. method:: dup()

      Sao chép socket.

      Socket mới tạo là :ref:`không thể kế thừa <fd_inheritance>`.

      .. versionchanged:: 3.4
         Socket hiện không còn được kế thừa.

      .. availability:: not WASI.


   .. method:: fileno()

      Trả về bộ mô tả tệp của socket (một số nguyên nhỏ), hoặc -1 nếu xảy ra lỗi. Điều này hữu ích khi dùng với :func:`select.select`.

      Trên Windows, số nguyên nhỏ được phương thức này trả về không thể được sử dụng ở những nơi có thể sử dụng bộ mô tả tệp (chẳng hạn như :func:`os.fdopen`). Unix không có hạn chế này.

   .. method:: get_inheritable()

      Lấy :ref:`cờ có thể kế thừa <fd_inheritance>` của bộ mô tả tệp hoặc handle của socket: ``True`` nếu socket có thể được kế thừa trong các tiến trình con, ``False`` nếu không thể.

      .. versionadded:: 3.4


   .. method:: getpeername()

      Trả về địa chỉ từ xa mà socket được kết nối tới. Chẳng hạn, điều này hữu ích để tìm số cổng của một socket IPv4/v6 từ xa. Định dạng của địa chỉ được trả về phụ thuộc vào họ địa chỉ --- xem :ref:`socket-addresses`. Trên một số hệ thống, hàm này không được hỗ trợ.


   .. method:: getsockname()

      Trả về địa chỉ riêng của socket. Chẳng hạn, điều này hữu ích để tìm số cổng của một socket IPv4/v6. Định dạng của địa chỉ được trả về phụ thuộc vào họ địa chỉ --- xem :ref:`socket-addresses`.


   .. method:: getsockopt(level, optname[, buflen])

      Trả về giá trị của tùy chọn socket đã cho (xem trang hướng dẫn Unix
      :manpage:`getsockopt(2)`). Các hằng số ký hiệu cần thiết (:ref:`SO_\* v.v. <socket-unix-constants>`) được định nghĩa trong module này. Nếu không có *buflen*, hàm sẽ giả định đây là một tùy chọn số nguyên và trả về giá trị số nguyên của tùy chọn đó. Nếu có *buflen*, tham số này chỉ định độ dài tối đa của bộ đệm được dùng để nhận tùy chọn, và bộ đệm này được trả về dưới dạng đối tượng bytes. Người gọi có trách nhiệm giải mã nội dung của bộ đệm (xem module tích hợp tùy chọn :mod:`struct` để biết cách giải mã các cấu trúc C được mã hóa dưới dạng chuỗi byte).

      .. availability:: not WASI.


   .. method:: getblocking()

      Trả về ``True`` nếu socket ở chế độ blocking, và ``False`` nếu ở chế độ non-blocking.

      Tương đương với việc kiểm tra ``socket.gettimeout() != 0``.

      .. versionadded:: 3.7


   .. method:: gettimeout()

      Trả về thời gian chờ tính bằng giây (float) gắn với các thao tác socket, hoặc ``None`` nếu chưa đặt thời gian chờ. Giá trị này phản ánh lần gọi gần nhất tới
      :meth:`setblocking` hoặc :meth:`settimeout`.


   .. method:: ioctl(control, option)

      Phương thức :meth:`ioctl` là một giao diện giới hạn đối với giao diện hệ thống WSAIoctl. Vui lòng tham khảo `tài liệu Win32 <https://msdn.microsoft.com/en-us/library/ms741621%28VS.85%29.aspx>`_ để biết thêm thông tin.

      Trên các nền tảng khác, có thể sử dụng các hàm generic :func:`fcntl.fcntl` và :func:`fcntl.ioctl`; chúng nhận một đối tượng socket làm đối số đầu tiên.

      Hiện tại chỉ hỗ trợ các mã điều khiển sau: ``SIO_RCVALL``, ``SIO_KEEPALIVE_VALS`` và ``SIO_LOOPBACK_FAST_PATH``.

      .. availability:: Windows

      .. versionchanged:: 3.6
         ``SIO_LOOPBACK_FAST_PATH`` đã được thêm vào.


   .. method:: listen([backlog])

      Cho phép một server chấp nhận các kết nối. Nếu chỉ định *backlog*, giá trị này phải ít nhất là 0 (nếu nhỏ hơn, giá trị sẽ được đặt thành 0); giá trị này chỉ định số lượng kết nối chưa được chấp nhận mà hệ thống cho phép trước khi từ chối các kết nối mới. Nếu không chỉ định, hệ thống sẽ chọn một giá trị mặc định hợp lý.

      .. availability:: not WASI.

      .. versionchanged:: 3.5
         Tham số *backlog* hiện là tùy chọn.


   .. method:: makefile(mode='r', buffering=None, *, encoding=None, \
                               errors=None, newline=None)

      .. index:: single: I/O control; buffering

      Trả về một :term:`file object` được liên kết với socket. Kiểu chính xác được trả về phụ thuộc vào các đối số được truyền cho :meth:`makefile`. Các đối số này được diễn giải giống như bởi hàm tích hợp sẵn :func:`open`, ngoại trừ các giá trị *mode* được hỗ trợ chỉ là ``'r'`` (mặc định), ``'w'``, ``'b'`` hoặc kết hợp các giá trị đó.

      Socket phải ở chế độ blocking; socket có thể có thời gian chờ, nhưng bộ đệm nội bộ của đối tượng file có thể rơi vào trạng thái không nhất quán nếu xảy ra thời gian chờ.

      Việc đóng đối tượng file được trả về bởi :meth:`makefile` sẽ không đóng socket ban đầu trừ khi tất cả các đối tượng file khác đã được đóng và
      :meth:`~socket.socket.close` đã được gọi trên đối tượng socket.

      .. note::

         Trên Windows, đối tượng giống file được tạo bởi :meth:`makefile` không thể được sử dụng ở nơi yêu cầu một đối tượng file có file descriptor, chẳng hạn như các đối số stream của :meth:`subprocess.Popen`.


   .. method:: recv(bufsize[, flags])

      Nhận dữ liệu từ socket. Giá trị trả về là một đối tượng bytes biểu diễn dữ liệu đã nhận. Lượng dữ liệu tối đa có thể nhận cùng một lúc được chỉ định bởi *bufsize*. Đối tượng bytes rỗng được trả về cho biết client đã ngắt kết nối. Xem trang hướng dẫn Unix :manpage:`recv(2)` để biết ý nghĩa của đối số tùy chọn *flags*; đối số này mặc định bằng 0.

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


   .. method:: recvfrom(bufsize[, flags])

      Nhận dữ liệu từ socket. Giá trị trả về là một cặp ``(bytes, address)`` trong đó *bytes* là một đối tượng bytes biểu diễn dữ liệu đã nhận, còn *address* là địa chỉ của socket gửi dữ liệu. Xem trang hướng dẫn Unix
      :manpage:`recv(2)` để biết ý nghĩa của đối số tùy chọn *flags*; giá trị mặc định là zero. Định dạng của *address* phụ thuộc vào họ địa chỉ --- xem
      :ref:`socket-addresses`.

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).

      .. versionchanged:: 3.7
         Đối với địa chỉ IPv6 multicast, mục đầu tiên của *address* không còn chứa phần ``%scope_id`` nữa. Để lấy địa chỉ IPv6 đầy đủ, hãy sử dụng
         :func:`getnameinfo`.

   .. method:: recvmsg(bufsize[, ancbufsize[, flags]])

      Nhận dữ liệu thông thường (tối đa *bufsize* byte) và dữ liệu ancillary từ socket. Đối số *ancbufsize* đặt kích thước tính bằng byte của bộ đệm nội bộ dùng để nhận dữ liệu ancillary; giá trị mặc định là 0, nghĩa là sẽ không nhận dữ liệu ancillary. Có thể tính kích thước bộ đệm phù hợp cho dữ liệu ancillary bằng cách sử dụng
      :func:`CMSG_SPACE` hoặc :func:`CMSG_LEN`, và các mục không vừa với bộ đệm có thể bị cắt bớt hoặc loại bỏ. Đối số *flags* có giá trị mặc định là 0 và có cùng ý nghĩa như đối số của
      :meth:`recv`.

      Giá trị trả về là một bộ 4 phần tử: ``(data, ancdata, msg_flags, address)``. Mục *data* là một đối tượng :class:`bytes` chứa dữ liệu không phải ancillary đã nhận. Mục *ancdata* là danh sách gồm không hoặc nhiều tuple ``(cmsg_level, cmsg_type, cmsg_data)`` đại diện cho dữ liệu ancillary (các thông báo điều khiển) đã nhận: *cmsg_level* và *cmsg_type* lần lượt là các số nguyên chỉ định cấp giao thức và loại dành riêng cho giao thức, còn *cmsg_data* là một
      :class:`bytes` đối tượng chứa dữ liệu liên quan. Mục *msg_flags* là phép OR theo bit của nhiều flag biểu thị các điều kiện của thông báo đã nhận; hãy xem tài liệu hệ thống để biết chi tiết. Nếu socket nhận chưa được kết nối, *address* là địa chỉ của socket gửi, nếu có; nếu không, giá trị của nó không được xác định.

      Trên một số hệ thống, :meth:`sendmsg` và :meth:`recvmsg` có thể được dùng để truyền các file descriptor giữa các tiến trình qua một socket :const:`AF_UNIX`. Khi sử dụng tính năng này (tính năng này thường bị giới hạn ở
      socket :const:`SOCK_STREAM`), :meth:`recvmsg` sẽ trả về, trong dữ liệu phụ trợ, các mục có dạng ``(socket.SOL_SOCKET, socket.SCM_RIGHTS, fds)``, trong đó *fds* là một đối tượng :class:`bytes` biểu diễn các file descriptor mới dưới dạng một mảng nhị phân có kiểu :c:expr:`int` gốc của C. Nếu :meth:`recvmsg` phát sinh ngoại lệ sau khi system call trả về, trước tiên hàm sẽ cố gắng đóng mọi file descriptor nhận được qua cơ chế này.

      Một số hệ thống không cho biết độ dài bị cắt của các mục dữ liệu phụ trợ chỉ được nhận một phần. Nếu một mục có vẻ mở rộng quá cuối buffer, :meth:`recvmsg` sẽ phát ra :exc:`RuntimeWarning` và trả về phần nằm trong buffer, miễn là phần đó chưa bị cắt trước phần bắt đầu của dữ liệu liên kết với nó.

      Trên các hệ thống hỗ trợ cơ chế :const:`!SCM_RIGHTS`, hàm sau đây sẽ nhận tối đa *maxfds* file descriptor, trả về dữ liệu thông báo cùng một danh sách chứa các descriptor (đồng thời bỏ qua những điều kiện bất ngờ như nhận được các thông báo điều khiển không liên quan). Xem thêm :meth:`sendmsg`.::

         import socket, array

         def recv_fds(sock, msglen, maxfds):
             fds = array.array("i")   # Mảng số nguyên
             msg, ancdata, flags, addr = sock.recvmsg(msglen, socket.CMSG_LEN(maxfds * fds.itemsize))
             for cmsg_level, cmsg_type, cmsg_data in ancdata:
                 if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
                     # Nối dữ liệu, bỏ qua mọi số nguyên bị cắt ở cuối.
                     fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
             return msg, list(fds)

      .. availability:: Unix.

         Hầu hết các nền tảng Unix.

      .. versionadded:: 3.3

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


   .. method:: recvmsg_into(buffers[, ancbufsize[, flags]])

      Nhận dữ liệu thông thường và dữ liệu phụ trợ từ socket, hoạt động như
      :meth:`recvmsg` sẽ làm, nhưng phân tán dữ liệu không phụ trợ vào một loạt buffer thay vì trả về một đối tượng bytes mới. Đối số *buffers* phải là một iterable gồm các đối tượng cung cấp buffer có thể ghi (ví dụ: các đối tượng :class:`bytearray`); các buffer này sẽ được điền bằng những phần liên tiếp của dữ liệu không phụ trợ cho đến khi toàn bộ dữ liệu được ghi xong hoặc không còn buffer nào. Hệ điều hành có thể đặt giới hạn (:func:`~os.sysconf` giá trị ``SC_IOV_MAX``) đối với số lượng buffer có thể sử dụng. Các đối số *ancbufsize* và *flags* có cùng ý nghĩa như đối với :meth:`recvmsg`.

      Giá trị trả về là một tuple gồm 4 phần tử: ``(nbytes, ancdata, msg_flags, address)``, trong đó *nbytes* là tổng số byte dữ liệu không phụ trợ được ghi vào các buffer, còn *ancdata*, *msg_flags* và *address* có cùng ý nghĩa như đối với :meth:`recvmsg`.

      Ví dụ::

         >>> import socket
         >>> s1, s2 = socket.socketpair()
         >>> b1 = bytearray(b'----')
         >>> b2 = bytearray(b'0123456789')
         >>> b3 = bytearray(b'--------------')
         >>> s1.send(b'Mary had a little lamb')
         22
         >>> s2.recvmsg_into([b1, memoryview(b2)[2:9], b3])
         (22, [], 0, None)
         >>> [b1, b2, b3]
         [bytearray(b'Mary'), bytearray(b'01 had a 9'), bytearray(b'little lamb---')]

      .. availability:: Unix.

         Hầu hết các nền tảng Unix.

      .. versionadded:: 3.3


   .. method:: recvfrom_into(buffer[, nbytes[, flags]])

      Nhận dữ liệu từ socket và ghi dữ liệu vào *buffer* thay vì tạo một chuỗi byte mới. Giá trị trả về là một cặp ``(nbytes, address)``, trong đó *nbytes* là số byte đã nhận, còn *address* là địa chỉ của socket gửi dữ liệu. Xem trang hướng dẫn Unix :manpage:`recv(2)` để biết ý nghĩa của đối số tùy chọn *flags*; giá trị mặc định là 0. Định dạng của *address* phụ thuộc vào họ địa chỉ — xem :ref:`socket-addresses`.


   .. method:: recv_into(buffer[, nbytes[, flags]])

      Nhận tối đa *nbytes* byte từ socket, lưu dữ liệu vào buffer thay vì tạo một bytestring mới. Nếu *nbytes* không được chỉ định (hoặc bằng 0), nhận tối đa lượng dữ liệu tương ứng với kích thước có sẵn trong buffer đã cho. Trả về số byte đã nhận. Xem trang hướng dẫn Unix :manpage:`recv(2)` để biết ý nghĩa của đối số tùy chọn *flags*; mặc định là 0.


   .. method:: send(bytes[, flags])

      Gửi dữ liệu đến socket. Socket phải được kết nối với một socket từ xa. Đối số tùy chọn *flags* có cùng ý nghĩa như đối số :meth:`recv`. Trả về số byte đã gửi. Ứng dụng có trách nhiệm kiểm tra xem toàn bộ dữ liệu đã được gửi hay chưa; nếu chỉ một phần dữ liệu được truyền đi, ứng dụng cần cố gắng gửi phần dữ liệu còn lại. Để biết thêm thông tin về chủ đề này, hãy tham khảo :ref:`socket-howto`.

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


   .. method:: sendall(bytes[, flags])

      Gửi dữ liệu đến socket. Socket phải được kết nối với một socket từ xa. Đối số tùy chọn *flags* có cùng ý nghĩa như đối số :meth:`recv`. Không giống như :meth:`send`, phương thức này tiếp tục gửi dữ liệu từ *bytes* cho đến khi toàn bộ dữ liệu được gửi hoặc xảy ra lỗi. Khi thành công, ``None`` được trả về. Khi có lỗi, một ngoại lệ được phát sinh và không có cách nào xác định được bao nhiêu dữ liệu, nếu có, đã được gửi thành công.

      .. versionchanged:: 3.5
         Thời gian chờ của socket không còn được đặt lại mỗi khi dữ liệu được gửi thành công. Hiện tại, thời gian chờ của socket là tổng thời lượng tối đa để gửi toàn bộ dữ liệu.

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


   .. method:: sendto(bytes, address)
               sendto(bytes, flags, address)

      Gửi dữ liệu đến socket. Socket không nên được kết nối với một socket từ xa, vì socket đích được chỉ định bởi *address*. Đối số *flags* tùy chọn có cùng ý nghĩa như đối với :meth:`recv`. Trả về số byte đã gửi. Định dạng của *address* phụ thuộc vào họ địa chỉ --- xem
      :ref:`socket-addresses`.

      .. audit-event:: socket.sendto self,address socket.socket.sendto

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


   .. method:: sendmsg(buffers[, ancdata[, flags[, address]]])

      Gửi dữ liệu thông thường và dữ liệu ancillary đến socket, tập hợp dữ liệu không ancillary từ một chuỗi bộ đệm rồi nối chúng thành một thông báo duy nhất. Đối số *buffers* chỉ định dữ liệu không ancillary dưới dạng một iterable gồm
      :term:`bytes-like objects <bytes-like object>` (ví dụ: :class:`bytes` objects:func:`~os.sysconf`); hệ điều hành có thể đặt giới hạn (:func:`~os.sysconf` value ``SC_IOV_MAX``) đối với số lượng bộ đệm có thể sử dụng. Đối số *ancdata* chỉ định dữ liệu ancillary (các thông báo điều khiển) dưới dạng một iterable gồm không hoặc nhiều tuple ``(cmsg_level, cmsg_type, cmsg_data)``, trong đó *cmsg_level* và *cmsg_type* là các số nguyên lần lượt chỉ định cấp độ giao thức và kiểu dành riêng cho giao thức, còn *cmsg_data* là một bytes-like object chứa dữ liệu liên quan. Lưu ý rằng một số hệ thống (đặc biệt là các hệ thống không có :func:`CMSG_SPACE`) có thể chỉ hỗ trợ gửi một thông báo điều khiển trong mỗi lần gọi. Đối số *flags* mặc định là 0 và có cùng ý nghĩa như đối với
      :meth:`send`. Nếu cung cấp *address* và không phải ``None``, đối số này sẽ đặt địa chỉ đích cho thông báo. Giá trị trả về là số byte dữ liệu không ancillary đã gửi.

      Hàm sau đây gửi danh sách các bộ mô tả tệp *fds* qua một socket :const:`AF_UNIX`, trên các hệ thống hỗ trợ cơ chế
      :const:`!SCM_RIGHTS`. Xem thêm :meth:`recvmsg`.::

         import socket, array

         def send_fds(sock, msg, fds):
             return sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", fds))])

      .. availability:: Unix, not WASI.

         Hầu hết các nền tảng Unix.

      .. audit-event:: socket.sendmsg self,address socket.socket.sendmsg

      .. versionadded:: 3.3

      .. versionchanged:: 3.5
         Nếu lệnh gọi hệ thống bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ, phương thức này giờ đây sẽ thử lại lệnh gọi hệ thống thay vì phát sinh ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).

   .. method:: sendmsg_afalg([msg], *, op[, iv[, assoclen[, flags]]])

      Phiên bản chuyên biệt của :meth:`~socket.sendmsg` dành cho socket :const:`AF_ALG`. Thiết lập mode, IV, độ dài dữ liệu liên kết AEAD và các cờ cho socket :const:`AF_ALG`.

      .. availability:: Linux >= 2.6.38.

      .. versionadded:: 3.6

   .. method:: sendfile(file, offset=0, count=None)

      Gửi tệp cho đến khi đạt EOF bằng cách sử dụng phương thức hiệu suất cao
      :mod:`os.sendfile` và trả về tổng số byte đã gửi. *file* phải là đối tượng tệp thông thường được mở ở mode nhị phân. Nếu
      :mod:`os.sendfile` không khả dụng (ví dụ: trên Windows) hoặc *file* không phải là tệp thông thường, thì sẽ sử dụng :meth:`send`. *offset* cho biết vị trí bắt đầu đọc tệp. Nếu được chỉ định, *count* là tổng số byte cần truyền, thay vì gửi tệp cho đến khi đạt EOF. Vị trí tệp được cập nhật khi trả về hoặc cả trong trường hợp xảy ra lỗi, khi đó
      :meth:`file.tell() <io.IOBase.tell>` có thể được dùng để xác định số byte đã gửi. Socket phải thuộc kiểu :const:`SOCK_STREAM`. Không hỗ trợ socket non-blocking.

      .. versionadded:: 3.5

   .. method:: set_inheritable(inheritable)

      Đặt :ref:`cờ inheritable <fd_inheritance>` của file descriptor hoặc handle của socket.

      .. versionadded:: 3.4


   .. method:: setblocking(flag)

      Đặt socket ở chế độ blocking hoặc non-blocking: nếu *cờ* là false, socket sẽ được đặt ở chế độ non-blocking, nếu không thì ở chế độ blocking.

      Phương thức này là cách viết tắt cho một số :meth:`~socket.settimeout` lệnh gọi:

      * ``sock.setblocking(True)`` tương đương với ``sock.settimeout(None)``

      * ``sock.setblocking(False)`` tương đương với ``sock.settimeout(0.0)``

      .. versionchanged:: 3.7
         Phương thức này không còn áp dụng :const:`SOCK_NONBLOCK` cờ trên
         :attr:`socket.type`.


   .. method:: settimeout(value)

      Đặt thời gian chờ cho các thao tác blocking của socket. Đối số *giá trị* có thể là một số thực không âm biểu thị số giây hoặc ``None``. Nếu cung cấp giá trị khác không, các thao tác socket tiếp theo sẽ phát sinh một
      :exc:`timeout` ngoại lệ nếu khoảng thời gian chờ *value* đã trôi qua trước khi thao tác hoàn tất. Nếu cung cấp giá trị bằng 0, socket sẽ được đặt ở chế độ non-blocking. Nếu cung cấp ``None``, socket sẽ được đặt ở chế độ blocking.

      Để biết thêm thông tin, vui lòng tham khảo :ref:`ghi chú về thời gian chờ của socket <socket-timeouts>`.

      .. versionchanged:: 3.7
         Phương thức này không còn bật/tắt :const:`SOCK_NONBLOCK` cờ trên
         :attr:`socket.type`.


   .. method:: setsockopt(level, optname, value: int | Buffer)
               setsockopt(level, optname, None, optlen: int)

      .. index:: pair: module; struct

      Đặt giá trị của tùy chọn socket đã cho (xem trang hướng dẫn Unix
      :manpage:`setsockopt(2)`). Các hằng số tượng trưng cần thiết được định nghĩa trong module này (:ref:`!SO_\* v.v. <socket-unix-constants>`). Giá trị có thể là một số nguyên, ``None`` hoặc một :term:`bytes-like object` đại diện cho một bộ đệm. Trong trường hợp sau, người gọi phải đảm bảo rằng bytestring chứa các bit thích hợp (xem module tích hợp tùy chọn :mod:`struct` để biết cách mã hóa các cấu trúc C thành bytestring). Khi *value* được đặt thành ``None``, đối số *optlen* là bắt buộc. Điều này tương đương với việc gọi hàm C :c:func:`!setsockopt` với ``optval=NULL`` và ``optlen=optlen``.

      .. versionchanged:: 3.5
         :term:`bytes-like object` có thể ghi hiện được chấp nhận.

      .. versionchanged:: 3.6
         Đã thêm dạng setsockopt(level, optname, None, optlen: int).

      .. availability:: not WASI.


   .. method:: shutdown(how)

      Tắt một hoặc cả hai chiều của kết nối. Nếu *how* là :const:`SHUT_RD`, không cho phép nhận thêm dữ liệu. Nếu *how* là :const:`SHUT_WR`, không cho phép gửi thêm dữ liệu. Nếu *how* là :const:`SHUT_RDWR`, không cho phép gửi hoặc nhận thêm dữ liệu.

      .. availability:: not WASI.


   .. method:: share(process_id)

      Sao chép một socket và chuẩn bị socket đó để chia sẻ với một tiến trình đích. Tiến trình đích phải được cung cấp *process_id*. Sau đó, có thể truyền đối tượng bytes kết quả đến tiến trình đích bằng một hình thức giao tiếp liên tiến trình nào đó, rồi tạo lại socket tại đó bằng :func:`fromshare`. Sau khi gọi phương thức này, bạn có thể đóng socket một cách an toàn vì hệ điều hành đã sao chép socket cho tiến trình đích.

      .. availability:: Windows.

      .. versionadded:: 3.3


   Lưu ý rằng không có các phương thức :meth:`!read` hoặc :meth:`!write`; thay vào đó, hãy sử dụng
   :meth:`~socket.recv` và :meth:`~socket.send` mà không có đối số *flags*.

   Các đối tượng socket cũng có những thuộc tính sau (chỉ đọc), tương ứng với các giá trị được truyền cho hàm khởi tạo :class:`~socket.socket`.


   .. attribute:: family

      Họ socket.


   .. attribute:: type

      Kiểu socket.


   .. attribute:: proto

      Giao thức socket.


.. class:: SocketType

   Lớp cơ sở của kiểu :class:`~socket.socket`, được tái xuất từ
   :mod:`!_socket`.  Một phép kiểm tra instance như ``isinstance(socket(...), SocketType)`` cho kết quả đúng, nhưng ``SocketType`` không giống ``type(socket(...))``, vốn chính là :class:`~socket.socket`.


.. _socket-timeouts:

Lưu ý về thời gian chờ của socket
---------------------------------

Một đối tượng socket có thể ở một trong ba chế độ: blocking, non-blocking hoặc timeout.  Theo mặc định, socket luôn được tạo ở chế độ blocking, nhưng bạn có thể thay đổi điều này bằng cách gọi :func:`setdefaulttimeout`.

* Ở chế độ *blocking mode*, các thao tác sẽ bị chặn cho đến khi hoàn tất hoặc hệ thống trả về lỗi (chẳng hạn như kết nối hết thời gian chờ).

* Trong *chế độ không chặn*, các thao tác sẽ thất bại (với một lỗi không may phụ thuộc vào hệ thống) nếu không thể hoàn tất ngay lập tức: các hàm từ
  mô-đun :mod:`select` có thể được sử dụng để biết khi nào và liệu một socket có sẵn sàng để đọc hoặc ghi hay không.

* Trong *chế độ thời gian chờ*, các thao tác sẽ thất bại nếu không thể hoàn tất trong khoảng thời gian chờ được chỉ định cho socket (chúng sẽ phát sinh một ngoại lệ :exc:`timeout`) hoặc nếu hệ thống trả về lỗi.

.. note::
   Ở cấp độ hệ điều hành, các socket trong *chế độ thời gian chờ* được thiết lập nội bộ ở chế độ không chặn. Ngoài ra, chế độ chặn và chế độ thời gian chờ được dùng chung giữa các bộ mô tả tệp và các đối tượng socket tham chiếu đến cùng một endpoint mạng. Chi tiết triển khai này có thể gây ra những hệ quả dễ nhận thấy nếu chẳng hạn bạn quyết định sử dụng :meth:`~socket.fileno` của một socket.

Thời gian chờ và phương thức ``connect``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Thao tác :meth:`~socket.connect` cũng chịu ảnh hưởng của thiết lập thời gian chờ; nhìn chung, bạn nên gọi :meth:`~socket.settimeout` trước khi gọi :meth:`~socket.connect` hoặc truyền tham số thời gian chờ cho
:meth:`create_connection`. Tuy nhiên, ngăn xếp mạng của hệ thống cũng có thể trả về lỗi hết thời gian chờ kết nối riêng, bất kể thiết lập thời gian chờ socket của Python.

Thời gian chờ và phương thức ``accept``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu :func:`getdefaulttimeout` không phải là :const:`None`, các socket được phương thức :meth:`~socket.accept` trả về sẽ kế thừa thời gian chờ đó. Nếu không, hành vi sẽ phụ thuộc vào các thiết lập của socket đang lắng nghe:

* nếu socket đang lắng nghe ở *blocking mode* hoặc *timeout mode*, socket được :meth:`~socket.accept` trả về sẽ ở *blocking mode*;

* nếu socket đang lắng nghe ở *non-blocking mode*, việc socket được :meth:`~socket.accept` trả về ở chế độ blocking hay non-blocking sẽ phụ thuộc vào hệ điều hành. Nếu muốn đảm bảo hành vi nhất quán trên nhiều nền tảng, bạn nên tự ghi đè thiết lập này.


.. _socket-example:

Ví dụ
-----

Dưới đây là bốn chương trình ví dụ tối giản sử dụng giao thức TCP/IP: một server phản hồi lại toàn bộ dữ liệu mà nó nhận được (chỉ phục vụ một client) và một client sử dụng server đó. Lưu ý rằng server phải thực hiện chuỗi :func:`~socket.socket`,
:meth:`~socket.bind`, :meth:`~socket.listen`, :meth:`~socket.accept` (có thể lặp lại :meth:`~socket.accept` để phục vụ nhiều client), trong khi client chỉ cần chuỗi :func:`~socket.socket`, :meth:`~socket.connect`. Cũng lưu ý rằng server không thực hiện :meth:`~socket.sendall`/:meth:`~socket.recv` trên socket mà nó dùng để lắng nghe, mà trên socket mới được trả về bởi
:meth:`~socket.accept`.

Hai ví dụ đầu tiên chỉ hỗ trợ IPv4.::

   # Chương trình máy chủ echo
   import socket

   HOST = ''                 # Tên tượng trưng chỉ tất cả các interface khả dụng
   PORT = 50007              # Cổng không đặc quyền tùy ý
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.bind((HOST, PORT))
       s.listen(1)
       conn, addr = s.accept()
       with conn:
           print('Connected by', addr)
           while True:
               data = conn.recv(1024)
               if not data: break
               conn.sendall(data)

::

   # Chương trình client echo
   import socket

   HOST = 'daring.cwi.nl'    # Máy chủ từ xa
   PORT = 50007              # Cùng cổng với cổng được máy chủ sử dụng
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       s.connect((HOST, PORT))
       s.sendall(b'Hello, world')
       data = s.recv(1024)
   print('Received', repr(data))

Hai ví dụ tiếp theo giống hệt hai ví dụ trên, nhưng hỗ trợ cả IPv4 và IPv6. Phía máy chủ sẽ lắng nghe họ địa chỉ đầu tiên khả dụng (đáng lẽ phải lắng nghe cả hai). Trên hầu hết các hệ thống hỗ trợ IPv6, IPv6 sẽ được ưu tiên và máy chủ có thể không tiếp nhận lưu lượng IPv4. Phía máy khách sẽ cố gắng kết nối đến tất cả các địa chỉ được trả về sau khi phân giải tên, rồi gửi lưu lượng đến địa chỉ đầu tiên kết nối thành công.::

   # Chương trình máy chủ echo
   import socket
   import sys

   HOST = None               # Tên tượng trưng chỉ tất cả các interface khả dụng
   PORT = 50007              # Cổng không đặc quyền tùy ý
   s = None
   for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                 socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
       af, socktype, proto, canonname, sa = res
       try:
           s = socket.socket(af, socktype, proto)
       except OSError as msg:
           s = None
           continue
       try:
           s.bind(sa)
           s.listen(1)
       except OSError as msg:
           s.close()
           s = None
           continue
       break
   if s is None:
       print('could not open socket')
       sys.exit(1)
   conn, addr = s.accept()
   with conn:
       print('Connected by', addr)
       while True:
           data = conn.recv(1024)
           if not data: break
           conn.send(data)

::

   # Chương trình client echo
   import socket
   import sys

   HOST = 'daring.cwi.nl'    # Máy chủ từ xa
   PORT = 50007              # Cùng cổng với cổng được máy chủ sử dụng
   s = None
   for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
       af, socktype, proto, canonname, sa = res
       try:
           s = socket.socket(af, socktype, proto)
       except OSError as msg:
           s = None
           continue
       try:
           s.connect(sa)
       except OSError as msg:
           s.close()
           s = None
           continue
       break
   if s is None:
       print('could not open socket')
       sys.exit(1)
   with s:
       s.sendall(b'Hello, world')
       data = s.recv(1024)
   print('Received', repr(data))

Ví dụ tiếp theo cho thấy cách viết một network sniffer rất đơn giản bằng raw socket trên Windows. Ví dụ này yêu cầu quyền quản trị viên để sửa đổi giao diện::

   import socket

   # giao diện mạng công khai
   HOST = socket.gethostbyname(socket.gethostname())

   # tạo một raw socket và bind nó với giao diện công khai
   s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
   s.bind((HOST, 0))

   # Include IP headers
   s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

   # nhận tất cả các gói tin
   s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

   # nhận một gói tin
   print(s.recvfrom(65565))

   # đã tắt chế độ promiscuous
   s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

Ví dụ tiếp theo cho thấy cách sử dụng giao diện socket để giao tiếp với một mạng CAN bằng giao thức raw socket. Để sử dụng CAN với giao thức broadcast manager thay thế, hãy mở một socket bằng::

    socket.socket(socket.AF_CAN, socket.SOCK_DGRAM, socket.CAN_BCM)

Sau khi bind (:const:`CAN_RAW`) hoặc connect (:const:`CAN_BCM`) socket, bạn có thể sử dụng các thao tác :meth:`socket.send` và :meth:`socket.recv` (cùng các thao tác tương ứng) trên đối tượng socket như bình thường.

Ví dụ cuối cùng này có thể yêu cầu các đặc quyền đặc biệt::

   import socket
   import struct


   # Đóng gói/giải nén frame CAN (xem 'struct can_frame' trong <linux/can.h>)

   can_frame_fmt = "=IB3x8s"
   can_frame_size = struct.calcsize(can_frame_fmt)

   def build_can_frame(can_id, data):
       can_dlc = len(data)
       data = data.ljust(8, b'\x00')
       return struct.pack(can_frame_fmt, can_id, can_dlc, data)

   def dissect_can_frame(frame):
       can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
       return (can_id, can_dlc, data[:can_dlc])


   # tạo một raw socket và bind nó vào interface 'vcan0'
   s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
   s.bind(('vcan0',))

   while True:
       cf, addr = s.recvfrom(can_frame_size)

       print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))

       try:
           s.send(cf)
       except OSError:
           print('Error sending CAN frame')

       try:
           s.send(build_can_frame(0x01, b'\x01\x02\x03'))
       except OSError:
           print('Error sending CAN frame')

Chạy một ví dụ nhiều lần với khoảng trễ giữa các lần thực thi quá ngắn có thể dẫn đến lỗi này::

   OSError: [Errno 98] Address already in use

Nguyên nhân là lần thực thi trước đã để socket ở trạng thái ``TIME_WAIT`` và không thể tái sử dụng ngay lập tức.

Có một cờ :mod:`!socket` cần đặt để ngăn điều này,
:const:`socket.SO_REUSEADDR`::

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((HOST, PORT))

cờ :data:`SO_REUSEADDR` cho kernel biết có thể tái sử dụng một socket cục bộ đang ở trạng thái ``TIME_WAIT`` mà không cần chờ hết thời gian timeout tự nhiên.


.. seealso::

   Để tìm hiểu phần giới thiệu về lập trình socket (bằng C), hãy xem các tài liệu sau:

   - *Hướng dẫn nhập môn về giao tiếp giữa các tiến trình trong 4.3BSD*, của Stuart Sechrest

   - *Hướng dẫn nâng cao về giao tiếp giữa các tiến trình trong 4.3BSD*, của Samuel J.  Leffler và cộng sự,

   cả hai đều nằm trong UNIX Programmer's Manual, Supplementary Documents 1 (các phần PS1:7 và PS1:8). Tài liệu tham khảo dành riêng cho từng nền tảng về các system call liên quan đến socket cũng là nguồn thông tin hữu ích để tìm hiểu chi tiết về ngữ nghĩa của socket. Đối với Unix, hãy tham khảo các trang hướng dẫn; đối với Windows, hãy xem đặc tả WinSock (hoặc Winsock 2). Đối với các API hỗ trợ IPv6, bạn có thể tham khảo :rfc:`3493` có tiêu đề Basic Socket Interface Extensions for IPv6.

.. _`Secure File Descriptor Handling`: https://udrepper.livejournal.com/20407.html
.. _`IEEE 802.3 protocol number`: https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.txt
.. _`Win32 documentation`: https://msdn.microsoft.com/en-us/library/ms741621%28VS.85%29.aspx
