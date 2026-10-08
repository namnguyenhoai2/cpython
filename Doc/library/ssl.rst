:mod:`!ssl` --- Trình bọc TLS/SSL cho các đối tượng socket
==========================================================

.. module:: ssl
   :synopsis: Trình bọc TLS/SSL cho các đối tượng socket

.. moduleauthor:: Bill Janssen <bill.janssen@gmail.com>
.. sectionauthor::  Bill Janssen <bill.janssen@gmail.com>

**Mã nguồn:** :source:`Lib/ssl.py`

.. index:: single: OpenSSL; (use in module ssl)

.. index:: TLS, SSL, Transport Layer Security, Secure Sockets Layer

--------------

Mô-đun này cung cấp quyền truy cập vào các tính năng mã hóa Transport Layer Security (thường được gọi là "Secure Sockets Layer") và xác thực đối tác cho các socket mạng, cả phía client lẫn phía server. Mô-đun này sử dụng thư viện OpenSSL.

.. include:: ../includes/optional-module.rst

.. note::

   Một số hành vi có thể phụ thuộc vào nền tảng, vì các lời gọi được thực hiện đến các API socket của hệ điều hành. Phiên bản OpenSSL được cài đặt cũng có thể gây ra những khác biệt trong hành vi. Ví dụ, TLSv1.3 đi kèm với OpenSSL phiên bản 1.1.1.

.. warning::
   Đừng sử dụng mô-đun này nếu chưa đọc :ref:`ssl-security`. Làm như vậy có thể tạo ra cảm giác an toàn sai lầm, vì các cài đặt mặc định của mô-đun ssl không nhất thiết phù hợp với ứng dụng của bạn.

.. include:: ../includes/wasm-notavail.rst

Phần này ghi lại các đối tượng và hàm trong mô-đun ``ssl``; để biết thêm thông tin chung về TLS, SSL và chứng chỉ, bạn đọc được khuyến nghị xem các tài liệu trong phần "Xem thêm" ở cuối trang.

Mô-đun này cung cấp một class, :class:`ssl.SSLSocket`, được dẫn xuất từ
kiểu :class:`socket.socket`, và cung cấp một wrapper giống socket, đồng thời mã hóa và giải mã dữ liệu truyền qua socket bằng SSL. Nó hỗ trợ các phương thức bổ sung như :meth:`getpeercert`, dùng để lấy chứng chỉ của phía bên kia kết nối, :meth:`cipher`, dùng để lấy cipher đang được sử dụng cho kết nối bảo mật hoặc
:meth:`get_verified_chain`, :meth:`get_unverified_chain` dùng để lấy chuỗi chứng chỉ.

Đối với các ứng dụng phức tạp hơn, class :class:`ssl.SSLContext` giúp quản lý các cài đặt và chứng chỉ, sau đó có thể được kế thừa bởi các SSL socket được tạo thông qua phương thức :meth:`SSLContext.wrap_socket`.

.. versionchanged:: 3.5.3
   Đã cập nhật để hỗ trợ liên kết với OpenSSL 1.1.0

.. versionchanged:: 3.6

   OpenSSL 0.9.8, 1.0.0 và 1.0.1 đã lỗi thời và không còn được hỗ trợ. Trong tương lai, mô-đun ssl sẽ yêu cầu ít nhất OpenSSL 1.0.2 hoặc 1.1.0.

.. versionchanged:: 3.10

   :pep:`644` đã được triển khai. Mô-đun ssl yêu cầu OpenSSL 1.1.1 hoặc mới hơn.

   Việc sử dụng các hằng số và hàm đã lỗi thời sẽ tạo ra cảnh báo về việc ngừng hỗ trợ.


Các hàm, hằng số và ngoại lệ
----------------------------


Tạo socket
^^^^^^^^^^

Các thực thể :class:`SSLSocket` phải được tạo bằng
phương thức :meth:`SSLContext.wrap_socket`. Hàm trợ giúp
:func:`create_default_context` trả về một context mới với các thiết lập mặc định an toàn.

Ví dụ về socket phía client với context mặc định và dual stack IPv4/IPv6::

    import socket
    import ssl

    hostname = 'www.python.org'
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())


Ví dụ về client socket với context tùy chỉnh và IPv4::

    hostname = 'www.python.org'
    # PROTOCOL_TLS_CLIENT yêu cầu chuỗi chứng chỉ và hostname hợp lệ
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('path/to/cabundle.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())


Ví dụ về server socket lắng nghe trên localhost IPv4::

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/path/to/certchain.pem', '/path/to/private.key')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('127.0.0.1', 8443))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            ...


Tạo context
^^^^^^^^^^^

Một hàm tiện ích giúp tạo các đối tượng :class:`SSLContext` cho những mục đích phổ biến.

.. function:: create_default_context(purpose=Purpose.SERVER_AUTH, *,\
                                     cafile=None, capath=None, cadata=None)

   Trả về một đối tượng :class:`SSLContext` mới với các thiết lập mặc định cho *mục đích* đã cho. Các thiết lập được chọn bởi mô-đun :mod:`!ssl`, và thường biểu thị mức bảo mật cao hơn so với khi gọi
   :class:`SSLContext` constructor trực tiếp.

   *cafile*, *capath*, *cadata* đại diện cho các chứng chỉ CA tùy chọn được tin cậy để xác minh chứng chỉ, như trong
   :meth:`SSLContext.load_verify_locations`. Nếu cả ba đều là
   :const:`None`, hàm này có thể chọn tin cậy các chứng chỉ CA mặc định của hệ thống.

   Các thiết lập là: :data:`PROTOCOL_TLS_CLIENT` hoặc
   :data:`PROTOCOL_TLS_SERVER`, :data:`OP_NO_SSLv2` và :data:`OP_NO_SSLv3` với các bộ mật mã mã hóa mạnh, không có RC4 và không có các bộ mật mã không xác thực. Truyền :const:`~Purpose.SERVER_AUTH` làm *purpose* sẽ đặt :data:`~SSLContext.verify_mode` thành :data:`CERT_REQUIRED` và либо tải các chứng chỉ CA (khi có ít nhất một trong các giá trị *cafile*, *capath* hoặc *cadata*) hoặc sử dụng :meth:`SSLContext.load_default_certs` để tải các chứng chỉ CA mặc định.

   Khi :attr:`~SSLContext.keylog_filename` được hỗ trợ và biến môi trường :envvar:`SSLKEYLOGFILE` được đặt, :func:`create_default_context` sẽ bật tính năng ghi nhật ký khóa.

   Các cài đặt mặc định cho context này bao gồm
   :data:`VERIFY_X509_PARTIAL_CHAIN` và :data:`VERIFY_X509_STRICT`. Các cài đặt này khiến triển khai OpenSSL bên dưới hoạt động giống hơn với một triển khai tuân thủ :rfc:`5280`, đổi lại là một mức độ không tương thích nhỏ với các chứng chỉ X.509 cũ hơn.

   .. note::
      Giao thức, tùy chọn, cipher và các cài đặt khác có thể được thay đổi thành các giá trị hạn chế hơn bất kỳ lúc nào mà không cần thông báo ngừng hỗ trợ trước. Các giá trị này thể hiện sự cân bằng hợp lý giữa khả năng tương thích và bảo mật.

      Nếu ứng dụng của bạn cần các cài đặt cụ thể, bạn nên tạo một
      :class:`SSLContext` và tự áp dụng các cài đặt đó.

   .. note::
      Nếu bạn nhận thấy rằng khi một số client hoặc server cũ cố gắng kết nối bằng một :class:`SSLContext` được tạo bởi hàm này, chúng nhận được lỗi có nội dung "Protocol or cipher suite mismatch", có thể là do chúng chỉ hỗ trợ SSL3.0, vốn bị hàm này loại trừ bằng cách sử dụng
      :data:`OP_NO_SSLv3`. SSL3.0 được nhiều người xem là `hoàn toàn bị phá vỡ <https://en.wikipedia.org/wiki/POODLE>`_. Nếu bạn vẫn muốn tiếp tục sử dụng hàm này nhưng vẫn cho phép các kết nối SSL 3.0, bạn có thể bật lại chúng bằng cách sử dụng::

         ctx = ssl.create_default_context(Purpose.CLIENT_AUTH)
         ctx.options &= ~ssl.OP_NO_SSLv3

   .. note::
      Ngữ cảnh này mặc định bật :data:`VERIFY_X509_STRICT`, điều này có thể khiến các chứng chỉ trước :rfc:`5280` hoặc chứng chỉ không hợp lệ bị từ chối, dù triển khai OpenSSL bên dưới vẫn chấp nhận chúng. Mặc dù không khuyến nghị vô hiệu hóa tùy chọn này, bạn có thể thực hiện bằng cách sử dụng::

         ctx = ssl.create_default_context()
         ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT

   .. versionadded:: 3.4

   .. versionchanged:: 3.4.4

     RC4 đã bị loại khỏi chuỗi cipher mặc định.

   .. versionchanged:: 3.6

     ChaCha20/Poly1305 đã được thêm vào chuỗi cipher mặc định.

     3DES đã bị loại khỏi chuỗi cipher mặc định.

   .. versionchanged:: 3.8

      Đã thêm hỗ trợ ghi nhật ký khóa vào :envvar:`SSLKEYLOGFILE`.

   .. versionchanged:: 3.10

      Ngữ cảnh hiện sử dụng :data:`PROTOCOL_TLS_CLIENT` hoặc
      giao thức :data:`PROTOCOL_TLS_SERVER` thay vì giao thức chung
      :data:`PROTOCOL_TLS`.

   .. versionchanged:: 3.13

      Context hiện sử dụng :data:`VERIFY_X509_PARTIAL_CHAIN` và
      :data:`VERIFY_X509_STRICT` trong các cờ verify mặc định của nó.


Ngoại lệ
^^^^^^^^

.. exception:: SSLError

   Được phát sinh để báo hiệu lỗi từ triển khai SSL bên dưới (hiện do thư viện OpenSSL cung cấp). Điều này cho biết có vấn đề trong lớp mã hóa và xác thực cấp cao hơn được phủ lên kết nối mạng bên dưới. Lỗi này là một kiểu con của :exc:`OSError`. Mã lỗi và thông báo của
   các thực thể :exc:`SSLError` được thư viện OpenSSL cung cấp.

   .. versionchanged:: 3.3
      :exc:`SSLError` used to be a subtype of :exc:`socket.error`.

   .. attribute:: library

      Một mnemonic dạng chuỗi chỉ định phân hệ OpenSSL nơi xảy ra lỗi, chẳng hạn như ``SSL``, ``PEM`` hoặc ``X509``. Phạm vi các giá trị có thể có phụ thuộc vào phiên bản OpenSSL.

      .. versionadded:: 3.3

   .. attribute:: reason

      Một mnemonic dạng chuỗi chỉ định lý do xảy ra lỗi này, ví dụ ``CERTIFICATE_VERIFY_FAILED``. Phạm vi các giá trị có thể có phụ thuộc vào phiên bản OpenSSL.

      .. versionadded:: 3.3

.. exception:: SSLZeroReturnError

   Một lớp con của :exc:`SSLError` được phát sinh khi cố gắng đọc hoặc ghi và kết nối SSL đã được đóng một cách an toàn. Lưu ý rằng điều này không có nghĩa là transport bên dưới (read TCP) đã được đóng.

   .. versionadded:: 3.3

.. exception:: SSLWantReadError

   Một lớp con của :exc:`SSLError` được phát sinh bởi một socket SSL không chặn :ref:`non-blocking SSL socket <ssl-nonblocking>` khi cố gắng đọc hoặc ghi dữ liệu, nhưng cần nhận thêm dữ liệu trên transport TCP bên dưới trước khi có thể hoàn tất yêu cầu.

   .. versionadded:: 3.3

.. exception:: SSLWantWriteError

   Một lớp con của :exc:`SSLError` được phát sinh bởi một socket SSL không chặn :ref:`non-blocking SSL socket <ssl-nonblocking>` khi cố gắng đọc hoặc ghi dữ liệu, nhưng cần gửi thêm dữ liệu trên transport TCP bên dưới trước khi có thể hoàn tất yêu cầu.

   .. versionadded:: 3.3

.. exception:: SSLSyscallError

   Một lớp con của :exc:`SSLError` được phát sinh khi gặp lỗi hệ thống trong lúc cố gắng thực hiện một thao tác trên socket SSL. Đáng tiếc là không có cách dễ dàng nào để kiểm tra số errno ban đầu.

   .. versionadded:: 3.3

.. exception:: SSLEOFError

   Một lớp con của :exc:`SSLError` được phát sinh khi kết nối SSL bị chấm dứt đột ngột. Nhìn chung, bạn không nên cố gắng sử dụng lại transport bên dưới khi gặp lỗi này.

   .. versionadded:: 3.3

.. exception:: SSLCertVerificationError

   Một lớp con của :exc:`SSLError` được phát sinh khi việc xác thực chứng chỉ không thành công.

   .. versionadded:: 3.7

   .. attribute:: verify_code

      Một số lỗi dạng số biểu thị lỗi xác minh.

   .. attribute:: verify_message

      Chuỗi dễ đọc đối với con người của lỗi xác minh.

.. exception:: CertificateError

   Bí danh của :exc:`SSLCertVerificationError`.

   .. versionchanged:: 3.7
      Ngoại lệ này hiện là bí danh của :exc:`SSLCertVerificationError`.


Sinh ngẫu nhiên
^^^^^^^^^^^^^^^

.. function:: RAND_bytes(num, /)

   Trả về *num* byte giả ngẫu nhiên có độ mạnh mật mã. Phát sinh một
   :class:`SSLError` nếu PRNG chưa được khởi tạo bằng đủ dữ liệu hoặc nếu thao tác này không được phương thức RAND hiện tại hỗ trợ. Có thể dùng :func:`RAND_status` để kiểm tra trạng thái của PRNG và dùng :func:`RAND_add` để khởi tạo PRNG.

   Đối với gần như mọi ứng dụng, :func:`os.urandom` được ưu tiên.

   Đọc bài viết Wikipedia, `Bộ tạo số giả ngẫu nhiên an toàn về mặt mật mã (CSPRNG) <https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator>`_, để biết các yêu cầu đối với một bộ tạo mạnh về mặt mật mã.

   .. versionadded:: 3.3

.. function:: RAND_status()

   Trả về ``True`` nếu bộ tạo số giả ngẫu nhiên SSL đã được khởi tạo bằng đủ tính ngẫu nhiên, và ``False`` trong trường hợp ngược lại. Bạn có thể sử dụng
   :func:`ssl.RAND_egd` và :func:`ssl.RAND_add` để tăng tính ngẫu nhiên của bộ tạo số giả ngẫu nhiên.

.. function:: RAND_add(bytes, entropy, /)

   Trộn *bytes* đã cho vào bộ tạo số giả ngẫu nhiên SSL. Tham số *entropy* (một số thực) là cận dưới của entropy chứa trong chuỗi (vì vậy bạn luôn có thể sử dụng ``0.0``). Xem :rfc:`1750` để biết thêm thông tin về các nguồn entropy.

   .. versionchanged:: 3.5
      :term:`bytes-like object` có thể ghi hiện đã được chấp nhận.

Xử lý chứng chỉ
^^^^^^^^^^^^^^^

.. testsetup::

   import ssl

.. function:: cert_time_to_seconds(cert_time)

   Trả về thời gian tính bằng giây kể từ epoch, với ``cert_time`` là chuỗi biểu diễn ngày "notBefore" hoặc "notAfter" từ một chứng chỉ theo định dạng strptime của ``"%b %d %H:%M:%S %Y %Z"`` (locale C).

   Dưới đây là một ví dụ:

   .. doctest:: newcontext

      >>> import ssl
      >>> import datetime as dt
      >>> timestamp = ssl.cert_time_to_seconds("Jan  5 09:34:43 2018 GMT")
      >>> timestamp  # doctest: +SKIP
      1515144883
      >>> print(dt.datetime.fromtimestamp(timestamp, dt.UTC))  # doctest: +SKIP
      2018-01-05 09:34:43+00:00

   Ngày "notBefore" hoặc "notAfter" phải sử dụng GMT (:rfc:`5280`).

   .. versionchanged:: 3.5
      Diễn giải thời gian đầu vào là thời gian theo UTC như được chỉ định bởi múi giờ 'GMT' trong chuỗi đầu vào. Trước đây, múi giờ cục bộ đã được sử dụng. Trả về một số nguyên (định dạng đầu vào không có phần lẻ của giây)

.. function:: get_server_certificate(addr, ssl_version=PROTOCOL_TLS_CLIENT, \
                                     ca_certs=None[, timeout])

   Với địa chỉ ``addr`` của một server được bảo vệ bằng SSL, dưới dạng một cặp (*hostname*, *port-number*), hàm này lấy certificate của server và trả về certificate đó dưới dạng chuỗi được mã hóa PEM. Nếu ``ssl_version`` được chỉ định, hàm sẽ sử dụng phiên bản đó của giao thức SSL để thử kết nối với server. Nếu *ca_certs* được chỉ định, giá trị này phải là một tệp chứa danh sách các root certificate, có cùng định dạng như định dạng được sử dụng cho tham số *cafile* trong
   :meth:`SSLContext.load_verify_locations`. Lệnh gọi sẽ cố gắng xác thực chứng chỉ máy chủ dựa trên tập hợp chứng chỉ gốc đó và sẽ thất bại nếu quá trình xác thực không thành công. Có thể chỉ định thời gian chờ bằng tham số ``timeout``.

   .. versionchanged:: 3.3
      Hàm này hiện tương thích với IPv6.

   .. versionchanged:: 3.5
      Giá trị mặc định của *ssl_version* được thay đổi từ :data:`PROTOCOL_SSLv3` thành
      :data:`PROTOCOL_TLS` để đạt khả năng tương thích tối đa với các máy chủ hiện đại.

   .. versionchanged:: 3.10
      Đã thêm tham số *timeout*.

.. function:: DER_cert_to_PEM_cert(der_cert_bytes)

   Với một chứng chỉ ở dạng blob byte được mã hóa DER, trả về phiên bản chuỗi được mã hóa PEM của chính chứng chỉ đó.

.. function:: PEM_cert_to_DER_cert(pem_cert_string)

   Với một chứng chỉ ở dạng chuỗi ASCII PEM, trả về một chuỗi byte được mã hóa DER cho chính chứng chỉ đó.

.. function:: get_default_verify_paths()

   Trả về một named tuple chứa các đường dẫn đến cafile và capath mặc định của OpenSSL. Các đường dẫn này giống với những đường dẫn được sử dụng bởi
   :meth:`SSLContext.set_default_verify_paths`. Giá trị trả về là một
   :term:`named tuple` ``DefaultVerifyPaths``:

   * :attr:`cafile` - đường dẫn đã được phân giải đến cafile hoặc ``None`` nếu tệp không tồn tại,
   * :attr:`capath` - đường dẫn đã được phân giải đến capath hoặc ``None`` nếu thư mục không tồn tại,
   * :attr:`openssl_cafile_env` - khóa môi trường của OpenSSL trỏ đến một cafile,
   * :attr:`openssl_cafile` - đường dẫn được hard-code đến một cafile,
   * :attr:`openssl_capath_env` - khóa môi trường của OpenSSL trỏ đến một capath,
   * :attr:`openssl_capath` - đường dẫn được ghi cứng tới thư mục capath

   .. versionadded:: 3.4

.. function:: enum_certificates(store_name)

   Lấy chứng chỉ từ kho chứng chỉ hệ thống của Windows. *store_name* có thể là một trong các giá trị ``CA``, ``ROOT`` hoặc ``MY``. Windows cũng có thể cung cấp thêm các kho chứng chỉ khác.

   Hàm trả về một danh sách các tuple (cert_bytes, encoding_type, trust). encoding_type chỉ định kiểu mã hóa của cert_bytes. Giá trị này có thể là
   :const:`x509_asn` cho dữ liệu X.509 ASN.1 hoặc :const:`pkcs_7_asn` cho dữ liệu PKCS#7 ASN.1. trust chỉ định mục đích của chứng chỉ dưới dạng một tập hợp các OIDS hoặc chính xác là ``True`` nếu chứng chỉ đáng tin cậy cho mọi mục đích.

   Ví dụ::

      >>> ssl.enum_certificates("CA")
      [(b'data...', 'x509_asn', {'1.3.6.1.5.5.7.3.1', '1.3.6.1.5.5.7.3.2'}),
       (b'data...', 'x509_asn', True)]

   .. availability:: Windows.

   .. versionadded:: 3.4

.. function:: enum_crls(store_name)

   Lấy CRL từ kho chứng chỉ hệ thống của Windows. *store_name* có thể là một trong các giá trị ``CA``, ``ROOT`` hoặc ``MY``. Windows cũng có thể cung cấp thêm các kho chứng chỉ khác.

   Hàm trả về một danh sách các tuple (cert_bytes, encoding_type, trust). encoding_type chỉ định kiểu mã hóa của cert_bytes. Giá trị này có thể là
   :const:`x509_asn` cho dữ liệu ASN.1 X.509 hoặc :const:`pkcs_7_asn` cho dữ liệu ASN.1 PKCS#7.

   .. availability:: Windows.

   .. versionadded:: 3.4


Hằng số
^^^^^^^

   Tất cả các hằng số hiện là các collection :class:`enum.IntEnum` hoặc :class:`enum.IntFlag`.

   .. versionadded:: 3.6

.. data:: CERT_NONE

   Giá trị có thể có cho :attr:`SSLContext.verify_mode`. Ngoại trừ :const:`PROTOCOL_TLS_CLIENT`, đây là chế độ mặc định. Với socket phía client, gần như mọi certificate đều được chấp nhận. Các lỗi validation, chẳng hạn như certificate không đáng tin cậy hoặc đã hết hạn, sẽ bị bỏ qua và không hủy quá trình TLS/SSL handshake.

   Ở chế độ server, không có certificate nào được yêu cầu từ client, vì vậy client không gửi certificate nào để xác thực client cert.

   Xem phần thảo luận về :ref:`ssl-security` bên dưới.

.. data:: CERT_OPTIONAL

   Giá trị có thể có cho :attr:`SSLContext.verify_mode`. Ở chế độ client, :const:`CERT_OPTIONAL` có cùng ý nghĩa với :const:`CERT_REQUIRED`. Thay vào đó, nên sử dụng :const:`CERT_REQUIRED` cho socket phía client.

   Ở chế độ server, một yêu cầu chứng chỉ client được gửi đến client. Client có thể bỏ qua yêu cầu hoặc gửi chứng chỉ để thực hiện xác thực chứng chỉ client TLS. Nếu client chọn gửi chứng chỉ, chứng chỉ đó sẽ được xác minh. Bất kỳ lỗi xác minh nào cũng lập tức hủy quá trình bắt tay TLS.

   Việc sử dụng cài đặt này yêu cầu truyền một tập hợp chứng chỉ CA hợp lệ vào :meth:`SSLContext.load_verify_locations`.

.. data:: CERT_REQUIRED

   Giá trị khả dụng cho :attr:`SSLContext.verify_mode`. Ở chế độ này, chứng chỉ được yêu cầu từ phía bên kia của kết nối socket; một :class:`SSLError` sẽ được phát sinh nếu không cung cấp chứng chỉ hoặc nếu việc xác thực chứng chỉ không thành công. Chế độ này **không** đủ để xác minh chứng chỉ ở chế độ client vì không đối chiếu tên máy chủ. Cũng phải bật :attr:`~SSLContext.check_hostname` để xác minh tính xác thực của chứng chỉ.
   :const:`PROTOCOL_TLS_CLIENT` sử dụng :const:`CERT_REQUIRED` và bật :attr:`~SSLContext.check_hostname` theo mặc định.

   Với socket server, chế độ này cung cấp khả năng xác thực chứng chỉ client TLS bắt buộc. Một yêu cầu chứng chỉ client được gửi đến client và client phải cung cấp một chứng chỉ hợp lệ, đáng tin cậy.

   Việc sử dụng cài đặt này yêu cầu truyền một tập hợp chứng chỉ CA hợp lệ vào :meth:`SSLContext.load_verify_locations`.

.. class:: VerifyMode

   Tập hợp các hằng số CERT_* của :class:`enum.IntEnum`.

   .. versionadded:: 3.6

.. data:: VERIFY_DEFAULT

   Giá trị có thể có cho :attr:`SSLContext.verify_flags`. Ở chế độ này, danh sách thu hồi chứng chỉ (CRL) không được kiểm tra. Theo mặc định, OpenSSL không yêu cầu cũng không xác minh CRL.

   .. versionadded:: 3.4

.. data:: VERIFY_CRL_CHECK_LEAF

   Giá trị có thể có cho :attr:`SSLContext.verify_flags`. Ở chế độ này, chỉ chứng chỉ của peer được kiểm tra, còn các chứng chỉ CA trung gian thì không. Chế độ này yêu cầu một CRL hợp lệ được ký bởi bên phát hành chứng chỉ của peer (CA cấp trực tiếp). Nếu chưa tải CRL phù hợp bằng
   :attr:`SSLContext.load_verify_locations`, việc xác thực sẽ thất bại.

   .. versionadded:: 3.4

.. data:: VERIFY_CRL_CHECK_CHAIN

   Giá trị có thể có cho :attr:`SSLContext.verify_flags`. Ở chế độ này, CRL của tất cả chứng chỉ trong chuỗi chứng chỉ của peer đều được kiểm tra.

   .. versionadded:: 3.4

.. data:: VERIFY_X509_STRICT

   Giá trị có thể có cho :attr:`SSLContext.verify_flags` để tắt các biện pháp khắc phục dành cho chứng chỉ X.509 bị lỗi.

   .. versionadded:: 3.4

.. data:: VERIFY_ALLOW_PROXY_CERTS

   Giá trị có thể có cho :attr:`SSLContext.verify_flags` để bật tính năng xác minh chứng chỉ proxy.

   .. versionadded:: 3.10

.. data:: VERIFY_X509_TRUSTED_FIRST

   Giá trị có thể có cho :attr:`SSLContext.verify_flags`. Giá trị này yêu cầu OpenSSL ưu tiên các chứng chỉ đáng tin cậy khi xây dựng chuỗi tin cậy để xác thực một chứng chỉ. Cờ này được bật theo mặc định.

   .. versionadded:: 3.4.4

.. data:: VERIFY_X509_PARTIAL_CHAIN

   Giá trị khả dĩ của :attr:`SSLContext.verify_flags`. Giá trị này hướng dẫn OpenSSL coi các CA trung gian trong kho lưu trữ tin cậy là các trust anchor, tương tự như các chứng chỉ CA gốc tự ký. Nhờ đó, bạn có thể tin cậy các chứng chỉ do CA trung gian cấp mà không cần tin cậy CA gốc tổ tiên của CA đó.

   .. versionadded:: 3.10


.. class:: VerifyFlags

   :class:`enum.IntFlag` tập hợp các hằng số VERIFY_*.

   .. versionadded:: 3.6

.. data:: PROTOCOL_TLS

   Chọn phiên bản giao thức cao nhất mà cả client và server đều hỗ trợ. Mặc dù có tên như vậy, tùy chọn này có thể chọn cả giao thức "SSL" và "TLS".

   .. versionadded:: 3.6

   .. deprecated:: 3.10

      Client và server TLS yêu cầu các thiết lập mặc định khác nhau để giao tiếp an toàn. Hằng số giao thức TLS chung đã không còn được dùng và được thay thế bằng :data:`PROTOCOL_TLS_CLIENT` và :data:`PROTOCOL_TLS_SERVER`.

.. data:: PROTOCOL_TLS_CLIENT

   Tự động thương lượng phiên bản giao thức cao nhất mà cả client và server đều hỗ trợ, đồng thời cấu hình context cho các kết nối phía client. Giao thức này bật :data:`CERT_REQUIRED` và
   :attr:`~SSLContext.check_hostname` theo mặc định.

   .. versionadded:: 3.6

.. data:: PROTOCOL_TLS_SERVER

   Tự động thương lượng phiên bản giao thức cao nhất mà cả client và server đều hỗ trợ, đồng thời cấu hình context cho các kết nối phía server.

   .. versionadded:: 3.6

.. data:: PROTOCOL_SSLv23

   Bí danh của :data:`PROTOCOL_TLS`.

   .. deprecated:: 3.6

      Thay vào đó, hãy sử dụng :data:`PROTOCOL_TLS`.

.. data:: PROTOCOL_SSLv3

   Chọn SSL phiên bản 3 làm giao thức mã hóa kênh.

   Giao thức này không khả dụng nếu OpenSSL được biên dịch với tùy chọn ``no-ssl3``.

   .. warning::

      SSL phiên bản 3 không an toàn.  Rất không nên sử dụng giao thức này.

   .. deprecated:: 3.6

      OpenSSL đã loại bỏ tất cả các giao thức dành riêng cho từng phiên bản. Sử dụng giao thức mặc định :data:`PROTOCOL_TLS_SERVER` hoặc :data:`PROTOCOL_TLS_CLIENT` với :attr:`SSLContext.minimum_version` và
      :attr:`SSLContext.maximum_version` thay vào đó.


.. data:: PROTOCOL_TLSv1

   Chọn TLS phiên bản 1.0 làm giao thức mã hóa kênh.

   .. deprecated:: 3.6

      OpenSSL đã loại bỏ tất cả các giao thức dành riêng cho từng phiên bản.

.. data:: PROTOCOL_TLSv1_1

   Chọn TLS phiên bản 1.1 làm giao thức mã hóa kênh. Chỉ khả dụng với openssl phiên bản 1.0.1 trở lên.

   .. versionadded:: 3.4

   .. deprecated:: 3.6

      OpenSSL đã loại bỏ tất cả các giao thức dành riêng cho từng phiên bản.

.. data:: PROTOCOL_TLSv1_2

   Chọn TLS phiên bản 1.2 làm giao thức mã hóa kênh. Chỉ khả dụng với openssl phiên bản 1.0.1 trở lên.

   .. versionadded:: 3.4

   .. deprecated:: 3.6

      OpenSSL đã loại bỏ tất cả các giao thức dành riêng cho từng phiên bản.

.. data:: OP_ALL

   Bật các biện pháp khắc phục cho nhiều lỗi hiện diện trong những triển khai SSL khác. Tùy chọn này được đặt theo mặc định. Tùy chọn này không nhất thiết đặt các cờ giống với hằng số ``SSL_OP_ALL`` của OpenSSL.

   .. versionadded:: 3.2

.. data:: OP_NO_SSLv2

   Ngăn kết nối SSLv2. Tùy chọn này chỉ áp dụng khi kết hợp với :const:`PROTOCOL_TLS`. Tùy chọn này ngăn các peer chọn SSLv2 làm phiên bản giao thức.

   .. versionadded:: 3.2

   .. deprecated:: 3.6

      SSLv2 không được dùng nữa

.. data:: OP_NO_SSLv3

   Ngăn kết nối SSLv3. Tùy chọn này chỉ áp dụng khi kết hợp với :const:`PROTOCOL_TLS`. Tùy chọn này ngăn các peer chọn SSLv3 làm phiên bản giao thức.

   .. versionadded:: 3.2

   .. deprecated:: 3.6

      SSLv3 không được dùng nữa

.. data:: OP_NO_TLSv1

   Ngăn kết nối TLSv1. Tùy chọn này chỉ áp dụng khi kết hợp với :const:`PROTOCOL_TLS`. Tùy chọn này ngăn các peer chọn TLSv1 làm phiên bản giao thức.

   .. versionadded:: 3.2

   .. deprecated:: 3.7
      Tùy chọn này không còn được dùng kể từ OpenSSL 1.1.0, hãy sử dụng tùy chọn mới
      :attr:`SSLContext.minimum_version` và
      :attr:`SSLContext.maximum_version` thay vào đó.

.. data:: OP_NO_TLSv1_1

   Ngăn kết nối TLSv1.1. Tùy chọn này chỉ áp dụng khi kết hợp với :const:`PROTOCOL_TLS`. Tùy chọn này ngăn các phía chọn TLSv1.1 làm phiên bản giao thức. Chỉ khả dụng với openssl phiên bản 1.0.1 trở lên.

   .. versionadded:: 3.4

   .. deprecated:: 3.7
      Tùy chọn này không còn được khuyến nghị kể từ OpenSSL 1.1.0.

.. data:: OP_NO_TLSv1_2

   Ngăn kết nối TLSv1.2. Tùy chọn này chỉ áp dụng khi kết hợp với :const:`PROTOCOL_TLS`. Tùy chọn này ngăn các phía chọn TLSv1.2 làm phiên bản giao thức. Chỉ khả dụng với openssl phiên bản 1.0.1 trở lên.

   .. versionadded:: 3.4

   .. deprecated:: 3.7
      Tùy chọn này không còn được khuyến nghị kể từ OpenSSL 1.1.0.

.. data:: OP_NO_TLSv1_3

   Ngăn kết nối TLSv1.3. Tùy chọn này chỉ áp dụng khi kết hợp với :const:`PROTOCOL_TLS`. Tùy chọn này ngăn các phía chọn TLSv1.3 làm phiên bản giao thức. TLS 1.3 khả dụng với OpenSSL 1.1.1 trở lên. Khi Python được biên dịch với phiên bản OpenSSL cũ hơn, cờ này mặc định là *0*.

   .. versionadded:: 3.6.3

   .. deprecated:: 3.7
      Tùy chọn này không còn được khuyến nghị kể từ OpenSSL 1.1.0. Tùy chọn này được thêm vào 2.7.15 và 3.6.3 để đảm bảo khả năng tương thích ngược với OpenSSL 1.0.2.

.. data:: OP_NO_RENEGOTIATION

   Tắt mọi hoạt động thương lượng lại trong TLSv1.2 và các phiên bản cũ hơn. Không gửi các thông báo HelloRequest và bỏ qua các yêu cầu thương lượng lại qua ClientHello.

   Tùy chọn này chỉ khả dụng với OpenSSL 1.1.0h trở lên.

   .. versionadded:: 3.7

.. data:: OP_CIPHER_SERVER_PREFERENCE

   Sử dụng thứ tự ưu tiên cipher của server thay vì của client. Tùy chọn này không có tác dụng trên các client socket và server socket SSLv2.

   .. versionadded:: 3.3

.. data:: OP_SINGLE_DH_USE

   Ngăn việc sử dụng lại cùng một khóa DH cho các phiên SSL riêng biệt. Điều này cải thiện tính bảo mật chuyển tiếp (forward secrecy) nhưng yêu cầu nhiều tài nguyên tính toán hơn. Tùy chọn này chỉ áp dụng cho server socket.

   .. versionadded:: 3.3

.. data:: OP_SINGLE_ECDH_USE

   Ngăn việc sử dụng lại cùng một khóa ECDH cho các phiên SSL riêng biệt. Điều này cải thiện tính bảo mật chuyển tiếp (forward secrecy) nhưng yêu cầu nhiều tài nguyên tính toán hơn. Tùy chọn này chỉ áp dụng cho server socket.

   .. versionadded:: 3.3

.. data:: OP_ENABLE_MIDDLEBOX_COMPAT

   Gửi các thông báo Change Cipher Spec (CCS) giả trong quá trình bắt tay TLS 1.3 để khiến một kết nối TLS 1.3 trông giống một kết nối TLS 1.2 hơn.

   Tùy chọn này chỉ khả dụng với OpenSSL 1.1.1 trở lên.

   .. versionadded:: 3.8

.. data:: OP_NO_COMPRESSION

   Tắt tính năng nén trên kênh SSL. Tính năng này hữu ích nếu giao thức ứng dụng hỗ trợ cơ chế nén riêng.

   .. versionadded:: 3.3

.. class:: Options

   :class:`enum.IntFlag` tập hợp các hằng số OP_*.

.. data:: OP_NO_TICKET

   Ngăn phía client yêu cầu session ticket.

   .. versionadded:: 3.6

.. data:: OP_IGNORE_UNEXPECTED_EOF

   Bỏ qua việc đóng bất ngờ các kết nối TLS.

   Tùy chọn này chỉ khả dụng với OpenSSL 3.0.0 trở lên.

   .. versionadded:: 3.10

.. data:: OP_ENABLE_KTLS

   Bật việc sử dụng kernel TLS. Để tận dụng tính năng này, OpenSSL phải được biên dịch với hỗ trợ cho tính năng đó, đồng thời các cipher suite và extension đã thương lượng cũng phải được tính năng này hỗ trợ (danh sách các thành phần được hỗ trợ có thể thay đổi tùy theo nền tảng và phiên bản kernel).

   Lưu ý rằng khi bật kernel TLS, một số thao tác mật mã được kernel thực hiện trực tiếp thay vì thông qua bất kỳ OpenSSL Provider nào khả dụng. Điều này có thể không mong muốn nếu, chẳng hạn, ứng dụng yêu cầu mọi thao tác mật mã đều được thực hiện bởi FIPS provider.

   Tùy chọn này chỉ khả dụng với OpenSSL 3.0.0 trở lên.

   .. versionadded:: 3.12

.. data:: OP_LEGACY_SERVER_CONNECT

   Chỉ cho phép cơ chế thương lượng lại không an toàn kiểu cũ giữa OpenSSL và các máy chủ chưa được vá.

   .. versionadded:: 3.12

.. data:: HAS_ALPN

   Liệu thư viện OpenSSL có tích hợp sẵn hỗ trợ cho phần mở rộng TLS *Application-Layer Protocol Negotiation* như được mô tả trong :rfc:`7301` hay không.

   .. versionadded:: 3.5

.. data:: HAS_NEVER_CHECK_COMMON_NAME

   Liệu thư viện OpenSSL có tích hợp sẵn hỗ trợ không kiểm tra common name của subject và :attr:`SSLContext.hostname_checks_common_name` có thể ghi hay không.

   .. versionadded:: 3.7

.. data:: HAS_ECDH

   Liệu thư viện OpenSSL có tích hợp sẵn hỗ trợ cho việc trao đổi khóa Diffie-Hellman dựa trên đường cong elliptic hay không. Giá trị này phải là true, trừ khi tính năng đã bị nhà phân phối vô hiệu hóa rõ ràng.

   .. versionadded:: 3.3

.. data:: HAS_SNI

   Liệu thư viện OpenSSL có tích hợp sẵn hỗ trợ cho phần mở rộng *Server Name Indication* (như được định nghĩa trong :rfc:`6066`) hay không.

   .. versionadded:: 3.2

.. data:: HAS_NPN

   Liệu thư viện OpenSSL có tích hợp sẵn hỗ trợ cho *Next Protocol Negotiation* như được mô tả trong `Application Layer Protocol Negotiation <https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation>`_ hay không. Khi là true, bạn có thể sử dụng phương thức :meth:`SSLContext.set_npn_protocols` để thông báo các protocol mà bạn muốn hỗ trợ.

   .. versionadded:: 3.3

.. data:: HAS_SSLv2

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho giao thức SSL 2.0 hay không.

   .. versionadded:: 3.7

.. data:: HAS_SSLv3

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho giao thức SSL 3.0 hay không.

   .. versionadded:: 3.7

.. data:: HAS_TLSv1

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho giao thức TLS 1.0 hay không.

   .. versionadded:: 3.7

.. data:: HAS_TLSv1_1

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho giao thức TLS 1.1 hay không.

   .. versionadded:: 3.7

.. data:: HAS_TLSv1_2

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho giao thức TLS 1.2 hay không.

   .. versionadded:: 3.7

.. data:: HAS_TLSv1_3

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho giao thức TLS 1.3 hay không.

   .. versionadded:: 3.7

.. data:: HAS_PSK

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho TLS-PSK hay không.

   .. versionadded:: 3.13

.. data:: HAS_PHA

   Thư viện OpenSSL có hỗ trợ tích hợp sẵn cho TLS-PHA hay không.

   .. versionadded:: 3.14

.. data:: CHANNEL_BINDING_TYPES

   Danh sách các loại liên kết kênh TLS được hỗ trợ. Các chuỗi trong danh sách này có thể được dùng làm đối số cho :meth:`SSLSocket.get_channel_binding`.

   .. versionadded:: 3.3

.. data:: OPENSSL_VERSION

   Chuỗi phiên bản của thư viện OpenSSL được trình thông dịch nạp::

    >>> ssl.OPENSSL_VERSION
    'OpenSSL 1.0.2k  26 Jan 2017'

   .. versionadded:: 3.2

.. data:: OPENSSL_VERSION_INFO

   Một tuple gồm năm số nguyên đại diện cho thông tin phiên bản về thư viện OpenSSL::

    >>> ssl.OPENSSL_VERSION_INFO
    (1, 0, 2, 11, 15)

   .. versionadded:: 3.2

.. data:: OPENSSL_VERSION_NUMBER

   Số phiên bản thô của thư viện OpenSSL, dưới dạng một số nguyên duy nhất::

    >>> ssl.OPENSSL_VERSION_NUMBER
    268443839
    >>> hex(ssl.OPENSSL_VERSION_NUMBER)
    '0x100020bf'

   .. versionadded:: 3.2

.. data:: ALERT_DESCRIPTION_HANDSHAKE_FAILURE
          ALERT_DESCRIPTION_INTERNAL_ERROR ALERT_DESCRIPTION_*

   Các mô tả cảnh báo từ :rfc:`5246` và các nguồn khác. `IANA TLS Alert Registry <https://www.iana.org/assignments/tls-parameters/tls-parameters.xml#tls-parameters-6>`_ chứa danh sách này cùng các tham chiếu đến những RFC định nghĩa ý nghĩa của chúng.

   Được dùng làm giá trị trả về của hàm callback trong
   :meth:`SSLContext.set_servername_callback`.

   .. versionadded:: 3.4

.. class:: AlertDescription

   Tập hợp :class:`enum.IntEnum` các hằng số ALERT_DESCRIPTION_*.

   .. versionadded:: 3.6

.. data:: Purpose.SERVER_AUTH

   Tùy chọn cho :func:`create_default_context` và
   :meth:`SSLContext.load_default_certs`. Giá trị này cho biết ngữ cảnh có thể được dùng để xác thực các web server (do đó, nó sẽ được dùng để tạo các socket phía client).

   .. versionadded:: 3.4

.. data:: Purpose.CLIENT_AUTH

   Tùy chọn cho :func:`create_default_context` và
   :meth:`SSLContext.load_default_certs`. Giá trị này cho biết ngữ cảnh có thể được dùng để xác thực các web client (do đó, nó sẽ được dùng để tạo các socket phía server).

   .. versionadded:: 3.4

.. class:: SSLErrorNumber

   Tập hợp :class:`enum.IntEnum` các hằng số SSL_ERROR_*.

   .. versionadded:: 3.6

.. class:: TLSVersion

   :class:`enum.IntEnum` tập hợp các phiên bản SSL và TLS của
   :attr:`SSLContext.maximum_version` và :attr:`SSLContext.minimum_version`.

   .. versionadded:: 3.7

.. attribute:: TLSVersion.MINIMUM_SUPPORTED
.. attribute:: TLSVersion.MAXIMUM_SUPPORTED

   Phiên bản SSL hoặc TLS tối thiểu hoặc tối đa được hỗ trợ. Đây là các hằng số đặc biệt. Giá trị của chúng không phản ánh các phiên bản TLS/SSL thấp nhất và cao nhất hiện có.

.. attribute:: TLSVersion.SSLv3
.. attribute:: TLSVersion.TLSv1
.. attribute:: TLSVersion.TLSv1_1
.. attribute:: TLSVersion.TLSv1_2
.. attribute:: TLSVersion.TLSv1_3

   SSL 3.0 đến TLS 1.3.

   .. deprecated:: 3.10

      Tất cả thành viên :class:`TLSVersion` ngoại trừ :attr:`TLSVersion.TLSv1_2` và
      :attr:`TLSVersion.TLSv1_3` đều đã lỗi thời.


Socket SSL
----------

.. class:: SSLSocket(socket.socket)

   SSL sockets cung cấp các phương thức sau đây của :ref:`socket-objects`:

   - :meth:`~socket.socket.accept`
   - :meth:`~socket.socket.bind`
   - :meth:`~socket.socket.close`
   - :meth:`~socket.socket.connect`
   - :meth:`~socket.socket.detach`
   - :meth:`~socket.socket.fileno`
   - :meth:`~socket.socket.getpeername`, :meth:`~socket.socket.getsockname`
   - :meth:`~socket.socket.getsockopt`, :meth:`~socket.socket.setsockopt`
   - :meth:`~socket.socket.gettimeout`, :meth:`~socket.socket.settimeout`,
     :meth:`~socket.socket.setblocking`
   - :meth:`~socket.socket.listen`
   - :meth:`~socket.socket.makefile`
   - :meth:`~socket.socket.recv`, :meth:`~socket.socket.recv_into` (nhưng không được truyền đối số ``flags`` khác 0)
   - :meth:`~socket.socket.send`, :meth:`~socket.socket.sendall` (với cùng hạn chế)
   - :meth:`~socket.socket.sendfile` (nhưng :mod:`os.sendfile` sẽ chỉ được sử dụng cho các socket văn bản thuần túy, nếu không thì sẽ sử dụng :meth:`~socket.socket.send`)
   - :meth:`~socket.socket.shutdown`

   Tuy nhiên, vì giao thức SSL (và TLS) có cơ chế framing riêng ở trên TCP, lớp trừu tượng SSL sockets trong một số trường hợp có thể khác với đặc tả của các socket thông thường ở cấp hệ điều hành. Đặc biệt, hãy xem
   :ref:`ghi chú về các socket không chặn <ssl-nonblocking>`.

   Các instance của :class:`SSLSocket` phải được tạo bằng cách sử dụng
   phương thức :meth:`SSLContext.wrap_socket`.

   .. versionchanged:: 3.5
      Phương thức :meth:`sendfile` đã được thêm vào.

   .. versionchanged:: 3.5
      :meth:`shutdown` không đặt lại thời gian chờ của socket mỗi khi nhận hoặc gửi byte. Thời gian chờ của socket hiện là tổng thời lượng tối đa của quá trình tắt.

   .. deprecated:: 3.6
      Không nên tạo trực tiếp một thực thể :class:`SSLSocket`, hãy sử dụng
      :meth:`SSLContext.wrap_socket` để bọc một socket.

   .. versionchanged:: 3.7
      :class:`SSLSocket` instances must be created with
      :meth:`~SSLContext.wrap_socket`. In earlier versions, it was possible
      để tạo các thực thể trực tiếp. Điều này chưa bao giờ được ghi lại tài liệu hoặc được hỗ trợ chính thức.

   .. versionchanged:: 3.10
      Python hiện sử dụng ``SSL_read_ex`` và ``SSL_write_ex`` internally. Các hàm này hỗ trợ đọc và ghi dữ liệu lớn hơn 2 GB. Việc ghi dữ liệu có độ dài bằng 0 không còn thất bại với lỗi vi phạm giao thức.

SSL socket cũng có các phương thức và thuộc tính bổ sung sau:

.. method:: SSLSocket.read(len=1024, buffer=None)

   Đọc tối đa *len* byte dữ liệu từ SSL socket và trả về kết quả dưới dạng một instance ``bytes``. Nếu chỉ định *buffer*, dữ liệu sẽ được đọc vào buffer thay thế và trả về số byte đã đọc.

   Phát sinh :exc:`SSLWantReadError` hoặc :exc:`SSLWantWriteError` nếu socket ở trạng thái
   :ref:`non-blocking <ssl-nonblocking>` và thao tác đọc sẽ bị chặn.

   Vì việc tái thương lượng có thể xảy ra bất kỳ lúc nào, một lệnh gọi đến :meth:`read` cũng có thể gây ra các thao tác ghi.

   .. versionchanged:: 3.5
      Thời gian chờ của socket không còn được đặt lại mỗi khi nhận hoặc gửi byte. Thời gian chờ của socket hiện là tổng thời lượng tối đa để đọc tối đa *len* byte.

   .. deprecated:: 3.6
      Sử dụng :meth:`~SSLSocket.recv` thay vì :meth:`~SSLSocket.read`.

.. method:: SSLSocket.write(data)

   Ghi *data* vào socket SSL và trả về số byte đã ghi. Đối số *data* phải là một đối tượng hỗ trợ buffer interface.

   Phát sinh :exc:`SSLWantReadError` hoặc :exc:`SSLWantWriteError` nếu socket ở trạng thái
   :ref:`non-blocking <ssl-nonblocking>` và thao tác ghi sẽ bị chặn.

   Vì việc thương lượng lại có thể xảy ra bất cứ lúc nào, một lệnh gọi đến :meth:`write` cũng có thể gây ra các thao tác đọc.

   .. versionchanged:: 3.5
      Thời gian chờ của socket không còn được đặt lại mỗi khi nhận hoặc gửi byte. Thời gian chờ của socket hiện là tổng thời lượng tối đa để ghi *data*.

   .. deprecated:: 3.6
      Sử dụng :meth:`~SSLSocket.send` thay cho :meth:`~SSLSocket.write`.

.. note::

   Các phương thức :meth:`~SSLSocket.read` và :meth:`~SSLSocket.write` là những phương thức cấp thấp dùng để đọc và ghi dữ liệu cấp ứng dụng chưa mã hóa, đồng thời giải mã/mã hóa dữ liệu đó thành dữ liệu cấp đường truyền đã mã hóa. Các phương thức này yêu cầu một kết nối SSL đang hoạt động, tức là quá trình bắt tay đã hoàn tất và
   :meth:`SSLSocket.unwrap` không được gọi.

   Thông thường, bạn nên sử dụng các phương thức socket API như
   :meth:`~socket.socket.recv` và :meth:`~socket.socket.send` thay cho các phương thức này.

.. method:: SSLSocket.do_handshake(block=False)

   Thực hiện handshake thiết lập SSL.

   Nếu *block* là true và thời gian chờ nhận được từ :meth:`~socket.socket.gettimeout` bằng 0, socket sẽ được đặt ở chế độ blocking cho đến khi handshake được thực hiện.

   .. versionchanged:: 3.4
      Phương thức handshake cũng thực hiện :func:`!match_hostname` khi
      thuộc tính :attr:`~SSLContext.check_hostname` của socket
      :attr:`~SSLSocket.context` là true.

   .. versionchanged:: 3.5
      Thời gian chờ của socket không còn được đặt lại mỗi khi nhận hoặc gửi byte. Thời gian chờ của socket hiện là tổng thời lượng tối đa của quá trình handshake.

   .. versionchanged:: 3.7
      Tên máy chủ hoặc địa chỉ IP được OpenSSL đối chiếu trong quá trình handshake. Hàm :func:`!match_hostname` không còn được sử dụng. Nếu OpenSSL từ chối tên máy chủ hoặc địa chỉ IP, quá trình handshake sẽ bị hủy sớm và một thông báo cảnh báo TLS được gửi đến peer.

.. method:: SSLSocket.getpeercert(binary_form=False)

   Nếu không có chứng chỉ cho peer ở đầu kia của kết nối, trả về ``None``. Nếu SSL handshake chưa được thực hiện, hãy raise
   :exc:`ValueError`.

   Nếu tham số ``binary_form`` là :const:`False` và đã nhận được chứng chỉ từ peer, phương thức này trả về một đối tượng :class:`dict`. Nếu chứng chỉ chưa được xác thực, dict sẽ trống. Nếu chứng chỉ đã được xác thực, phương thức trả về một dict với nhiều key, trong đó có ``subject`` (principal được cấp chứng chỉ) và ``issuer`` (principal cấp chứng chỉ). Nếu chứng chỉ chứa một extension *Subject Alternative Name* (xem :rfc:`3280`), dict cũng sẽ có key ``subjectAltName``.

   Các trường ``subject`` và ``issuer`` là các tuple chứa chuỗi distinguished name tương đối (RDN) được cung cấp trong cấu trúc dữ liệu của chứng chỉ cho các trường tương ứng, và mỗi RDN là một chuỗi các cặp name-value. Dưới đây là một ví dụ thực tế::

      {'issuer': ((('countryName', 'IL'),),
                  (('organizationName', 'StartCom Ltd.'),),
                  (('organizationalUnitName',
                    'Secure Digital Certificate Signing'),),
                  (('commonName',
                    'StartCom Class 2 Primary Intermediate Server CA'),)),
       'notAfter': 'Nov 22 08:15:19 2013 GMT',
       'notBefore': 'Nov 21 03:09:52 2011 GMT',
       'serialNumber': '95F0',
       'subject': ((('description', '571208-SLe257oHY9fVQ07Z'),),
                   (('countryName', 'US'),),
                   (('stateOrProvinceName', 'California'),),
                   (('localityName', 'San Francisco'),),
                   (('organizationName', 'Electronic Frontier Foundation, Inc.'),),
                   (('commonName', '*.eff.org'),),
                   (('emailAddress', 'hostmaster@eff.org'),)),
       'subjectAltName': (('DNS', '*.eff.org'), ('DNS', 'eff.org')),
       'version': 3}

   Nếu tham số ``binary_form`` là :const:`True` và đã cung cấp chứng chỉ, phương thức này trả về toàn bộ chứng chỉ ở dạng được mã hóa DER dưới dạng một chuỗi byte, hoặc :const:`None` nếu peer không cung cấp chứng chỉ. Việc peer có cung cấp chứng chỉ hay không phụ thuộc vào vai trò của SSL socket:

   * đối với socket SSL của client, server sẽ luôn cung cấp một certificate, bất kể có yêu cầu validation hay không;

   * đối với socket SSL của server, client chỉ cung cấp certificate khi server yêu cầu; do đó :meth:`getpeercert` sẽ trả về
     :const:`None` nếu bạn đã sử dụng :const:`CERT_NONE` (thay vì
     :const:`CERT_OPTIONAL` hoặc :const:`CERT_REQUIRED`).

   Xem thêm :attr:`SSLContext.check_hostname`.

   .. versionchanged:: 3.2
      Dictionary được trả về bao gồm các mục bổ sung như ``issuer`` và ``notBefore``.

   .. versionchanged:: 3.4
      :exc:`ValueError` is raised when the handshake isn't done.
      Dictionary được trả về bao gồm các mục mở rộng X509v3 bổ sung
        chẳng hạn như các URI ``crlDistributionPoints``, ``caIssuers`` và ``OCSP``.

   .. versionchanged:: 3.9
      Các chuỗi địa chỉ IPv6 không còn có ký tự xuống dòng ở cuối.

.. method:: SSLSocket.get_verified_chain()

   Trả về chuỗi chứng chỉ đã được xác minh do đầu bên kia của kênh SSL cung cấp dưới dạng danh sách các byte được mã hóa DER. Nếu việc xác minh chứng chỉ bị vô hiệu hóa, phương thức sẽ hoạt động giống như
   :meth:`~SSLSocket.get_unverified_chain`.

   .. versionadded:: 3.13

.. method:: SSLSocket.get_unverified_chain()

   Trả về chuỗi chứng chỉ thô do đầu bên kia của kênh SSL cung cấp dưới dạng danh sách các byte được mã hóa DER.

   .. versionadded:: 3.13

.. method:: SSLSocket.cipher()

   Trả về một tuple gồm ba giá trị, chứa tên của cipher đang được sử dụng, phiên bản của giao thức SSL quy định việc sử dụng cipher đó và số bit bí mật đang được sử dụng. Nếu chưa thiết lập kết nối, trả về ``None``.

.. method:: SSLSocket.shared_ciphers()

   Trả về danh sách các cipher có sẵn ở cả client và server. Mỗi mục trong danh sách trả về là một tuple gồm ba giá trị, chứa tên của cipher, phiên bản của giao thức SSL quy định việc sử dụng cipher đó và số bit bí mật mà cipher sử dụng. :meth:`~SSLSocket.shared_ciphers` trả về ``None`` nếu chưa thiết lập kết nối hoặc socket là socket client.

   .. versionadded:: 3.5

.. method:: SSLSocket.compression()

   Trả về thuật toán nén đang được sử dụng dưới dạng chuỗi hoặc ``None`` nếu kết nối không được nén.

   Nếu giao thức cấp cao hơn hỗ trợ cơ chế nén riêng, bạn có thể sử dụng :data:`OP_NO_COMPRESSION` để tắt tính năng nén ở cấp SSL.

   .. versionadded:: 3.3

.. method:: SSLSocket.get_channel_binding(cb_type="tls-unique")

   Lấy dữ liệu channel binding cho kết nối hiện tại dưới dạng đối tượng bytes. Trả về ``None`` nếu chưa kết nối hoặc quá trình handshake chưa hoàn tất.

   Tham số *cb_type* cho phép chọn kiểu channel binding mong muốn. Các kiểu channel binding hợp lệ được liệt kê trong
   :data:`CHANNEL_BINDING_TYPES` list. Hiện tại chỉ hỗ trợ channel binding 'tls-unique', được định nghĩa bởi :rfc:`5929`. :exc:`ValueError` sẽ được phát sinh nếu yêu cầu một kiểu channel binding không được hỗ trợ.

   .. versionadded:: 3.3

.. method:: SSLSocket.selected_alpn_protocol()

   Trả về giao thức được chọn trong quá trình TLS handshake. Nếu
   :meth:`SSLContext.set_alpn_protocols` chưa được gọi, nếu bên kia không hỗ trợ ALPN, nếu socket này không hỗ trợ bất kỳ giao thức nào do client đề xuất hoặc nếu handshake chưa diễn ra, thì ``None`` sẽ được trả về.

   .. versionadded:: 3.5

.. method:: SSLSocket.selected_npn_protocol()

   Trả về giao thức cấp cao hơn được chọn trong quá trình TLS/SSL handshake. Nếu :meth:`SSLContext.set_npn_protocols` chưa được gọi, nếu bên kia không hỗ trợ NPN hoặc nếu handshake chưa diễn ra, phương thức này sẽ trả về ``None``.

   .. versionadded:: 3.3

   .. deprecated:: 3.10

      NPN đã được thay thế bằng ALPN

.. method:: SSLSocket.unwrap()

   Thực hiện quá trình bắt tay tắt SSL, thao tác này loại bỏ lớp TLS khỏi socket bên dưới và trả về đối tượng socket bên dưới. Có thể sử dụng thao tác này để chuyển từ hoạt động được mã hóa trên một kết nối sang hoạt động không mã hóa. Luôn sử dụng socket được trả về cho các giao tiếp tiếp theo với phía bên kia của kết nối, thay vì socket ban đầu.

.. method:: SSLSocket.verify_client_post_handshake()

   Yêu cầu xác thực sau bắt tay (PHA) từ một client TLS 1.3. PHA chỉ có thể được khởi tạo cho một kết nối TLS 1.3 từ socket phía server, sau quá trình bắt tay TLS ban đầu và khi PHA đã được bật ở cả hai phía, xem
   :attr:`SSLContext.post_handshake_auth`.

   Phương thức này không thực hiện trao đổi chứng chỉ ngay lập tức. Phía server sẽ gửi CertificateRequest trong sự kiện ghi tiếp theo và mong đợi client phản hồi bằng một chứng chỉ trong sự kiện đọc tiếp theo.

   Nếu bất kỳ điều kiện tiên quyết nào không được đáp ứng (ví dụ: không phải TLS 1.3, PHA chưa được bật), thì
   :exc:`SSLError` sẽ được phát sinh.

   .. note::
      Chỉ khả dụng với OpenSSL 1.1.1 và khi TLS 1.3 được bật. Nếu không hỗ trợ TLS 1.3, phương thức sẽ phát sinh :exc:`NotImplementedError`.

   .. versionadded:: 3.8

.. method:: SSLSocket.version()

   Trả về phiên bản giao thức SSL thực tế được thỏa thuận bởi kết nối dưới dạng chuỗi hoặc ``None`` nếu không thiết lập kết nối bảo mật. Tại thời điểm viết tài liệu này, các giá trị trả về có thể bao gồm ``"SSLv2"``, ``"SSLv3"``, ``"TLSv1"``, ``"TLSv1.1"`` và ``"TLSv1.2"``. Các phiên bản OpenSSL gần đây có thể định nghĩa thêm các giá trị trả về.

   .. versionadded:: 3.5

.. method:: SSLSocket.pending()

   Trả về số byte đã được giải mã và hiện có thể đọc, đang chờ trên kết nối.

.. attribute:: SSLSocket.context

   Đối tượng :class:`SSLContext` mà SSL socket này được liên kết.

   .. versionadded:: 3.2

.. attribute:: SSLSocket.server_side

   Một giá trị boolean là ``True`` đối với socket phía máy chủ và ``False`` đối với socket phía máy khách.

   .. versionadded:: 3.2

.. attribute:: SSLSocket.server_hostname

   Tên máy chủ: kiểu :class:`str`, hoặc ``None`` đối với socket phía máy chủ hoặc khi tên máy chủ không được chỉ định trong hàm khởi tạo.

   .. versionadded:: 3.2

   .. versionchanged:: 3.7
      Thuộc tính này hiện luôn là văn bản ASCII. Khi ``server_hostname`` là một tên miền quốc tế hóa (IDN), thuộc tính này hiện lưu dạng A-label (``"xn--pythn-mua.org"``) thay vì dạng U-label (``"pythön.org"``).

.. attribute:: SSLSocket.session

   :class:`SSLSession` cho kết nối SSL này. Session khả dụng cho socket phía máy khách và phía máy chủ sau khi quá trình bắt tay TLS được thực hiện. Đối với socket phía máy khách, session có thể được thiết lập trước
   :meth:`~SSLSocket.do_handshake` đã được gọi để tái sử dụng một session.

   .. versionadded:: 3.6

.. attribute:: SSLSocket.session_reused

   .. versionadded:: 3.6


Ngữ cảnh SSL
------------

.. versionadded:: 3.2

Một ngữ cảnh SSL chứa nhiều dữ liệu có thời gian tồn tại lâu hơn các kết nối SSL riêng lẻ, chẳng hạn như các tùy chọn cấu hình SSL, (các) certificate và (các) private key. Ngữ cảnh này cũng quản lý một cache các SSL session cho socket phía server nhằm tăng tốc các kết nối lặp lại từ cùng một client.

.. class:: SSLContext(protocol=None)

   Tạo một ngữ cảnh SSL mới. Bạn có thể truyền *protocol*, giá trị này phải là một trong các hằng số ``PROTOCOL_*`` được định nghĩa trong module này. Tham số này chỉ định phiên bản giao thức SSL sẽ sử dụng. Thông thường, server chọn một phiên bản giao thức cụ thể và client phải thích ứng với lựa chọn của server. Hầu hết các phiên bản không tương thích với những phiên bản khác. Nếu không được chỉ định, giá trị mặc định là
   :data:`PROTOCOL_TLS`; giá trị này cung cấp khả năng tương thích cao nhất với các phiên bản khác.

   Dưới đây là bảng cho biết những phiên bản trong client (theo chiều dọc) có thể kết nối với những phiên bản trong server (theo chiều ngang):

   .. table::

      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *client* / **server** | **SSLv2**  | **SSLv3**  | **TLS** [3]_ | **TLSv1** | **TLSv1.1** | **TLSv1.2** |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *SSLv2*               | có         | không      | không [1]_   | không     | không       | không       |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *SSLv3*               | không      | có         | không [2]_   | không     | không       | không       |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *TLS* (*SSLv23*) [3]_ | không [1]_ | không [2]_ | có           | có        | có          | có          |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *TLSv1*               | không      | không      | có           | có        | không       | không       |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *TLSv1.1*             | không      | không      | có           | không     | có          | không       |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+
      | *TLSv1.2*             | không      | không      | có           | không     | không       | có          |
      +-----------------------+------------+------------+--------------+-----------+-------------+-------------+

   .. rubric:: Chú thích
   .. [1] :class:`SSLContext` mặc định vô hiệu hóa SSLv2 bằng :data:`OP_NO_SSLv2`.
   .. [2] :class:`SSLContext` mặc định vô hiệu hóa SSLv3 bằng :data:`OP_NO_SSLv3`.
   .. [3] Giao thức TLS 1.3 sẽ khả dụng với :data:`PROTOCOL_TLS` trong OpenSSL >= 1.1.1. Không có hằng số PROTOCOL riêng chỉ dành cho TLS 1.3.

   .. seealso::
      :func:`create_default_context` lets the :mod:`!ssl` module choose
      các thiết lập bảo mật cho một mục đích nhất định.

   .. versionchanged:: 3.6

      Context được tạo với các giá trị mặc định an toàn. Các tùy chọn
      :data:`OP_NO_COMPRESSION`, :data:`OP_CIPHER_SERVER_PREFERENCE`,
      :data:`OP_SINGLE_DH_USE`, :data:`OP_SINGLE_ECDH_USE`,
      :data:`OP_NO_SSLv2`, và :data:`OP_NO_SSLv3` (ngoại trừ :data:`PROTOCOL_SSLv3`) được thiết lập theo mặc định. Danh sách bộ cipher ban đầu chỉ chứa các cipher ``HIGH``, không chứa cipher ``NULL`` và không chứa cipher ``MD5``.

   .. deprecated:: 3.10

      :class:`SSLContext` không có đối số protocol đã lỗi thời. Lớp context sẽ yêu cầu :data:`PROTOCOL_TLS_CLIENT` hoặc
      giao thức :data:`PROTOCOL_TLS_SERVER` trong tương lai.

   .. versionchanged:: 3.10

      Các bộ mã hóa mặc định hiện chỉ bao gồm các bộ mã hóa AES và ChaCha20 an toàn với tính bảo mật chuyển tiếp và cấp độ bảo mật 2. Các khóa RSA và DH có độ dài dưới 2048 bit và các khóa ECC có độ dài dưới 224 bit đều bị cấm.
      :data:`PROTOCOL_TLS`, :data:`PROTOCOL_TLS_CLIENT`, và
      :data:`PROTOCOL_TLS_SERVER` sử dụng TLS 1.2 làm phiên bản TLS tối thiểu.

   .. note::

      :class:`SSLContext` chỉ hỗ trợ thay đổi ở mức hạn chế sau khi đã được một kết nối sử dụng. Bạn có thể thêm chứng chỉ mới vào kho tin cậy nội bộ, nhưng việc thay đổi bộ mã hóa, cài đặt xác minh hoặc chứng chỉ mTLS có thể dẫn đến hành vi bất ngờ.

   .. note::

      :class:`SSLContext` được thiết kế để dùng chung và được nhiều kết nối sử dụng. Do đó, đối tượng này an toàn với thread miễn là không được cấu hình lại sau khi đã được một kết nối sử dụng.

Các đối tượng :class:`SSLContext` có các phương thức và thuộc tính sau:

.. method:: SSLContext.cert_store_stats()

   Lấy số liệu thống kê dưới dạng từ điển về số lượng chứng chỉ X.509 đã tải, số lượng chứng chỉ X.509 được đánh dấu là chứng chỉ CA và các danh sách thu hồi chứng chỉ.

   Ví dụ về một context có một chứng chỉ CA và một chứng chỉ khác::

      >>> context.cert_store_stats()
      {'crl': 0, 'x509_ca': 1, 'x509': 2}

   .. versionadded:: 3.4


.. method:: SSLContext.load_cert_chain(certfile, keyfile=None, password=None)

   Tải khóa riêng và chứng chỉ tương ứng. Chuỗi *certfile* phải là đường dẫn đến một tệp duy nhất ở định dạng PEM, chứa chứng chỉ cùng với bất kỳ số lượng chứng chỉ CA nào cần thiết để xác thực chứng chỉ. Nếu có chuỗi *keyfile*, chuỗi này phải trỏ đến một tệp chứa khóa riêng. Nếu không, khóa riêng cũng sẽ được lấy từ *certfile*. Xem phần thảo luận về
   :ref:`ssl-certificates` để biết thêm thông tin về cách chứng chỉ được lưu trong *certfile*.

   Đối số *password* có thể là một hàm được gọi để lấy mật khẩu giải mã khóa riêng. Hàm này chỉ được gọi khi khóa riêng được mã hóa và cần mật khẩu. Hàm sẽ được gọi không có đối số và phải trả về một chuỗi, bytes hoặc bytearray. Nếu giá trị trả về là một chuỗi, chuỗi đó sẽ được mã hóa bằng UTF-8 trước khi được dùng để giải mã khóa. Ngoài ra, có thể cung cấp trực tiếp một giá trị kiểu chuỗi, bytes hoặc bytearray làm đối số *password*. Giá trị này sẽ bị bỏ qua nếu khóa riêng không được mã hóa và không cần mật khẩu.

   Nếu không chỉ định đối số *password* và cần mật khẩu, cơ chế nhắc nhập mật khẩu tích hợp của OpenSSL sẽ được sử dụng để tương tác yêu cầu người dùng nhập mật khẩu.

   Một :class:`SSLError` sẽ được phát sinh nếu khóa riêng không khớp với chứng chỉ.

   .. versionchanged:: 3.3
      Đối số tùy chọn mới *password*.

.. method:: SSLContext.load_default_certs(purpose=Purpose.SERVER_AUTH)

   Tải một tập hợp chứng chỉ "cơ quan cấp chứng chỉ" (CA) mặc định từ các vị trí mặc định. Trên Windows, hàm này tải chứng chỉ CA từ các kho hệ thống ``CA`` và ``ROOT``. Trên tất cả các hệ thống, hàm này gọi
   :meth:`SSLContext.set_default_verify_paths`. Trong tương lai, phương thức này cũng có thể tải chứng chỉ CA từ các vị trí khác.

   Cờ *purpose* chỉ định loại chứng chỉ CA được tải. Thiết lập mặc định :const:`Purpose.SERVER_AUTH` tải các chứng chỉ được đánh dấu và tin cậy để xác thực máy chủ web TLS (socket phía client). :const:`Purpose.CLIENT_AUTH` tải các chứng chỉ CA để xác minh chứng chỉ client ở phía máy chủ.

   .. versionadded:: 3.4

.. method:: SSLContext.load_verify_locations(cafile=None, capath=None, cadata=None)

   Tải một tập hợp chứng chỉ "cơ quan cấp chứng chỉ" (CA) được dùng để xác thực chứng chỉ của các peer khác khi :data:`verify_mode` khác với
   :data:`CERT_NONE`. Phải chỉ định ít nhất một trong *cafile* hoặc *capath*.

   Phương thức này cũng có thể tải các danh sách thu hồi chứng chỉ (CRL) ở định dạng PEM hoặc DER. Để sử dụng CRL, :attr:`SSLContext.verify_flags` phải được cấu hình đúng cách.

   Chuỗi *cafile*, nếu có, là đường dẫn đến một tệp chứa các chứng chỉ CA được nối tiếp ở định dạng PEM. Xem phần thảo luận về
   :ref:`ssl-certificates` để biết thêm thông tin về cách sắp xếp các chứng chỉ trong tệp này.

   Chuỗi *capath*, nếu có, là đường dẫn đến một thư mục chứa một số chứng chỉ CA ở định dạng PEM, theo `bố cục dành riêng cho OpenSSL <https://docs.openssl.org/master/man3/SSL_CTX_load_verify_locations/>`_.

   Đối tượng *cadata*, nếu có, là một chuỗi ASCII chứa một hoặc nhiều chứng chỉ được mã hóa PEM hoặc một :term:`bytes-like object` chứa các chứng chỉ được mã hóa DER. Tương tự như với *capath*, các dòng bổ sung xung quanh những chứng chỉ được mã hóa PEM sẽ bị bỏ qua, nhưng phải có ít nhất một chứng chỉ.

   .. versionchanged:: 3.4
      Đối số tùy chọn mới *cadata*

.. method:: SSLContext.get_ca_certs(binary_form=False)

   Lấy danh sách các chứng chỉ của "cơ quan cấp chứng chỉ" (CA) đã được tải. Nếu tham số ``binary_form`` là :const:`False`, mỗi mục trong danh sách là một dict tương tự như đầu ra của :meth:`SSLSocket.getpeercert`. Nếu không, phương thức trả về danh sách các chứng chỉ được mã hóa DER. Danh sách được trả về không chứa các chứng chỉ từ *capath* trừ khi một chứng chỉ đã được yêu cầu và tải bởi một kết nối SSL.

   .. note::
      Các chứng chỉ trong thư mục capath sẽ không được tải trừ khi chúng đã được sử dụng ít nhất một lần.

   .. versionadded:: 3.4

.. method:: SSLContext.get_ciphers()

   Lấy danh sách các cipher đã bật. Danh sách được sắp xếp theo độ ưu tiên của cipher. Xem :meth:`SSLContext.set_ciphers`.

   Ví dụ::

       >>> ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
       >>> ctx.set_ciphers('ECDHE+AESGCM:!ECDSA')
       >>> ctx.get_ciphers()
       [{'aead': True,
         'alg_bits': 256,
         'auth': 'auth-rsa',
         'description': 'ECDHE-RSA-AES256-GCM-SHA384 TLSv1.2 Kx=ECDH     Au=RSA  '
                        'Enc=AESGCM(256) Mac=AEAD',
         'digest': None,
         'id': 50380848,
         'kea': 'kx-ecdhe',
         'name': 'ECDHE-RSA-AES256-GCM-SHA384',
         'protocol': 'TLSv1.2',
         'strength_bits': 256,
         'symmetric': 'aes-256-gcm'},
        {'aead': True,
         'alg_bits': 128,
         'auth': 'auth-rsa',
         'description': 'ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 Kx=ECDH     Au=RSA  '
                        'Enc=AESGCM(128) Mac=AEAD',
         'digest': None,
         'id': 50380847,
         'kea': 'kx-ecdhe',
         'name': 'ECDHE-RSA-AES128-GCM-SHA256',
         'protocol': 'TLSv1.2',
         'strength_bits': 128,
         'symmetric': 'aes-128-gcm'}]

   .. versionadded:: 3.6

.. method:: SSLContext.set_default_verify_paths()

   Tải một tập hợp chứng chỉ "cơ quan cấp chứng chỉ" (CA) mặc định từ đường dẫn hệ thống tệp được xác định khi xây dựng thư viện OpenSSL. Đáng tiếc là không có cách dễ dàng nào để biết phương thức này có thành công hay không: sẽ không có lỗi nào được trả về nếu không tìm thấy chứng chỉ. Tuy nhiên, khi thư viện OpenSSL được cung cấp như một phần của hệ điều hành, thư viện này có khả năng đã được cấu hình đúng.

.. method:: SSLContext.set_ciphers(ciphers, /)

   Đặt các cipher khả dụng cho những socket được tạo bằng context này. Giá trị phải là một chuỗi theo `định dạng danh sách cipher của OpenSSL <https://docs.openssl.org/master/man1/ciphers/>`_. Nếu không thể chọn cipher nào (do các tùy chọn tại thời điểm biên dịch hoặc cấu hình khác ngăn việc sử dụng tất cả các cipher đã chỉ định), một
   :class:`SSLError` sẽ được phát sinh.

   .. note::
      khi được kết nối, phương thức :meth:`SSLSocket.cipher` của các socket SSL sẽ cung cấp cipher hiện đang được chọn.

      Không thể vô hiệu hóa các bộ cipher TLS 1.3 bằng
      :meth:`~SSLContext.set_ciphers`.

.. method:: SSLContext.set_alpn_protocols(alpn_protocols)

   Chỉ định các giao thức mà socket nên quảng bá trong quá trình bắt tay SSL/TLS. Đây phải là một danh sách các chuỗi ASCII, chẳng hạn như ``['http/1.1', 'spdy/2']``, được sắp xếp theo thứ tự ưu tiên. Việc lựa chọn giao thức sẽ diễn ra trong quá trình bắt tay và tuân theo :rfc:`7301`. Sau khi bắt tay thành công, phương thức :meth:`SSLSocket.selected_alpn_protocol` sẽ trả về giao thức đã thỏa thuận.

   Phương thức này sẽ phát sinh :exc:`NotImplementedError` nếu :data:`HAS_ALPN` là ``False``.

   .. versionadded:: 3.5

.. method:: SSLContext.set_npn_protocols(npn_protocols)

   Chỉ định các giao thức mà socket nên quảng bá trong quá trình bắt tay SSL/TLS. Đây phải là một danh sách các chuỗi, chẳng hạn như ``['http/1.1', 'spdy/2']``, được sắp xếp theo thứ tự ưu tiên. Việc lựa chọn giao thức sẽ diễn ra trong quá trình bắt tay và tuân theo `Application Layer Protocol Negotiation <https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation>`_. Sau khi bắt tay thành công, phương thức :meth:`SSLSocket.selected_npn_protocol` sẽ trả về giao thức đã thỏa thuận.

   Phương thức này sẽ phát sinh :exc:`NotImplementedError` nếu :data:`HAS_NPN` là ``False``.

   .. versionadded:: 3.3

   .. deprecated:: 3.10

      NPN đã được thay thế bởi ALPN

.. attribute:: SSLContext.sni_callback

   Đăng ký một hàm callback sẽ được gọi sau khi máy chủ SSL/TLS nhận được thông báo bắt tay TLS Client Hello, khi máy khách TLS chỉ định chỉ báo tên máy chủ. Cơ chế chỉ báo tên máy chủ được quy định trong :rfc:`6066` mục 3 - Server Name Indication.

   Mỗi ``SSLContext`` chỉ có thể đặt một callback. Nếu *sni_callback* được đặt thành ``None`` thì callback sẽ bị vô hiệu hóa. Việc gọi hàm này lần tiếp theo sẽ vô hiệu hóa callback đã đăng ký trước đó.

   Hàm callback sẽ được gọi với ba đối số; đối số đầu tiên là :class:`ssl.SSLSocket`, đối số thứ hai là một chuỗi biểu thị tên máy chủ mà client dự định giao tiếp (hoặc :const:`None` nếu TLS Client Hello không chứa tên máy chủ), còn đối số thứ ba là :class:`SSLContext` ban đầu. Đối số tên máy chủ là văn bản. Đối với tên miền quốc tế hóa, tên máy chủ là một IDN A-label (``"xn--pythn-mua.org"``).

   Một cách sử dụng điển hình của callback này là thay đổi :class:`ssl.SSLSocket`'s
   :attr:`SSLSocket.context` attribute thành một đối tượng mới thuộc kiểu
   :class:`SSLContext` biểu thị một chuỗi chứng chỉ phù hợp với tên máy chủ.

   Với việc diễn ra trong giai đoạn thương lượng sớm của kết nối TLS, nếu callback gán một context mới cho :attr:`SSLSocket.context`, mọi thông báo ClientHello tiếp theo trên cùng kết nối (ví dụ sau TLS 1.3 HelloRetryRequest) sẽ được chuyển đến *sni_callback* của context mới, nếu có; callback ban đầu sẽ không được gọi lại cho kết nối đó.

   Do giai đoạn thương lượng sớm của kết nối TLS, chỉ có một số phương thức và thuộc tính hạn chế có thể sử dụng, chẳng hạn như
   :meth:`SSLSocket.selected_alpn_protocol` và :attr:`SSLSocket.context`. :meth:`SSLSocket.getpeercert`, :meth:`SSLSocket.get_verified_chain`,
   Các phương thức :meth:`SSLSocket.get_unverified_chain` :meth:`SSLSocket.cipher` và :meth:`SSLSocket.compression` yêu cầu kết nối TLS đã tiến triển vượt qua TLS Client Hello, do đó sẽ không trả về các giá trị có ý nghĩa và cũng không thể được gọi một cách an toàn.

   Hàm *sni_callback* phải trả về ``None`` để cho phép quá trình thương lượng TLS tiếp tục. Nếu cần xảy ra lỗi TLS, một hằng số
   :const:`ALERT_DESCRIPTION_* <ALERT_DESCRIPTION_INTERNAL_ERROR>` có thể được trả về. Các giá trị trả về khác sẽ dẫn đến lỗi nghiêm trọng TLS với
   :const:`ALERT_DESCRIPTION_INTERNAL_ERROR`.

   Nếu một ngoại lệ được phát sinh từ hàm *sni_callback*, kết nối TLS sẽ kết thúc cùng một thông báo cảnh báo TLS nghiêm trọng
   :const:`ALERT_DESCRIPTION_HANDSHAKE_FAILURE`.

   Phương thức này sẽ phát sinh :exc:`NotImplementedError` nếu thư viện OpenSSL được xây dựng với OPENSSL_NO_TLSEXT được định nghĩa.

   .. versionadded:: 3.7

   .. versionchanged:: 3.14.8
      Sau khi callback gán một :attr:`SSLSocket.context` mới, các thông báo ClientHello tiếp theo trên kết nối sẽ được chuyển đến *sni_callback* của context mới.

.. method:: SSLContext.set_servername_callback(server_name_callback)

   Đây là một API cũ được giữ lại để tương thích ngược. Khi có thể, bạn nên sử dụng :attr:`sni_callback` thay thế. *server_name_callback* đã cho tương tự như *sni_callback*, ngoại trừ khi hostname của máy chủ là một tên miền quốc tế hóa được mã hóa IDN, *server_name_callback* sẽ nhận một U-label đã giải mã (``"pythön.org"``).

   Nếu xảy ra lỗi giải mã tên máy chủ, kết nối TLS sẽ kết thúc bằng thông báo cảnh báo TLS nghiêm trọng :const:`ALERT_DESCRIPTION_INTERNAL_ERROR` gửi đến máy khách.

   .. versionadded:: 3.4

.. method:: SSLContext.load_dh_params(dhfile, /)

   Tải các tham số tạo khóa cho quá trình trao đổi khóa Diffie-Hellman (DH). Sử dụng trao đổi khóa DH giúp cải thiện tính bí mật chuyển tiếp, nhưng tiêu tốn thêm tài nguyên tính toán (cả trên máy chủ và máy khách). Tham số *dhfile* phải là đường dẫn đến một tệp chứa các tham số DH ở định dạng PEM.

   Thiết lập này không áp dụng cho client sockets. Bạn cũng có thể sử dụng
   :data:`OP_SINGLE_DH_USE` tùy chọn để tăng cường bảo mật hơn nữa.

   .. versionadded:: 3.3

.. method:: SSLContext.set_ecdh_curve(curve_name, /)

   Đặt tên đường cong cho quá trình trao đổi khóa Diffie-Hellman dựa trên đường cong elip (ECDH). ECDH nhanh hơn đáng kể so với DH thông thường nhưng được cho là có mức độ bảo mật tương đương. Tham số *curve_name* phải là một chuỗi mô tả một đường cong elip phổ biến, chẳng hạn như ``prime256v1`` cho một đường cong được hỗ trợ rộng rãi.

   Thiết lập này không áp dụng cho client sockets. Bạn cũng có thể sử dụng
   :data:`OP_SINGLE_ECDH_USE` tùy chọn để tăng cường bảo mật hơn nữa.

   Phương thức này không khả dụng nếu :data:`HAS_ECDH` là ``False``.

   .. versionadded:: 3.3

   .. seealso::
      `SSL/TLS & Perfect Forward Secrecy <https://vincent.bernat.ch/en/blog/2011-ssl-perfect-forward-secrecy>`_
         Vincent Bernat.

.. method:: SSLContext.wrap_socket(sock, server_side=False, \
      do_handshake_on_connect=True, suppress_ragged_eofs=True, \ server_hostname=None, session=None)

   Bọc một socket Python hiện có *sock* và trả về một instance của
   :attr:`SSLContext.sslsocket_class` (mặc định :class:`SSLSocket`). SSL socket được trả về gắn với context, các thiết lập và chứng chỉ của context đó. *sock* phải là một socket :const:`~socket.SOCK_STREAM`; các loại socket khác không được hỗ trợ.

   Tham số ``server_side`` là một boolean xác định socket này sẽ hoạt động theo phía máy chủ hay phía máy khách.

   Đối với các socket phía client, việc xây dựng context được thực hiện một cách lazy; nếu socket nền tảng chưa được kết nối, việc xây dựng context sẽ được thực hiện sau khi gọi :meth:`connect` trên socket. Đối với các socket phía server, nếu socket không có peer từ xa, socket đó được giả định là socket đang lắng nghe, và việc bọc SSL phía server sẽ tự động được thực hiện trên các kết nối client được chấp nhận thông qua
   phương thức :meth:`accept`. Phương thức này có thể phát sinh :exc:`SSLError`.

   Trên các kết nối client, tham số tùy chọn *server_hostname* chỉ định hostname của dịch vụ mà chúng ta đang kết nối đến. Điều này cho phép một server duy nhất lưu trữ nhiều dịch vụ dựa trên SSL với các certificate riêng biệt, khá tương tự như các virtual host HTTP. Việc chỉ định *server_hostname* sẽ phát sinh một :exc:`ValueError` nếu *server_side* là true.

   Tham số ``do_handshake_on_connect`` chỉ định có thực hiện SSL handshake tự động sau khi thực hiện :meth:`socket.connect` hay để chương trình ứng dụng gọi nó một cách rõ ràng bằng cách gọi
   phương thức :meth:`SSLSocket.do_handshake`. Việc gọi
   :meth:`SSLSocket.do_handshake` một cách rõ ràng cho phép chương trình kiểm soát hành vi blocking của thao tác I/O trên socket liên quan đến quá trình handshake.

   Tham số ``suppress_ragged_eofs`` chỉ định cách thức mà
   Phương thức :meth:`SSLSocket.recv` phải báo hiệu EOF bất ngờ từ đầu bên kia của kết nối. Nếu được chỉ định là :const:`True` (giá trị mặc định), phương thức trả về EOF bình thường (một đối tượng bytes rỗng) khi gặp các lỗi EOF bất ngờ do socket bên dưới phát sinh; nếu là :const:`False`, phương thức sẽ ném lại các ngoại lệ cho caller.

   *session*, xem :attr:`~SSLSocket.session`.

   Để bọc một :class:`SSLSocket` trong một :class:`SSLSocket` khác, hãy sử dụng
   :meth:`SSLContext.wrap_bio`.

   .. versionchanged:: 3.5
      Luôn cho phép truyền server_hostname, ngay cả khi OpenSSL không có SNI.

   .. versionchanged:: 3.6
      Đã bổ sung đối số *session*.

   .. versionchanged:: 3.7
      Phương thức trả về một instance của :attr:`SSLContext.sslsocket_class` thay vì :class:`SSLSocket` được hard-code.

.. attribute:: SSLContext.sslsocket_class

   Kiểu trả về của :meth:`SSLContext.wrap_socket`, mặc định là
   :class:`SSLSocket`. Thuộc tính này có thể được gán cho các instance của
   :class:`SSLContext` để trả về một subclass tùy chỉnh của
   :class:`SSLSocket`.

   .. versionadded:: 3.7

.. method:: SSLContext.wrap_bio(incoming, outgoing, server_side=False, \
                                server_hostname=None, session=None)

   Bọc các đối tượng BIO *incoming* và *outgoing*, rồi trả về một instance của
   :attr:`SSLContext.sslobject_class` (mặc định là :class:`SSLObject`). Các routine SSL sẽ đọc dữ liệu đầu vào từ BIO incoming và ghi dữ liệu vào BIO outgoing.

   Các tham số *server_side*, *server_hostname* và *session* có cùng ý nghĩa như trong :meth:`SSLContext.wrap_socket` và được kiểm tra theo cùng cách: cụ thể, một :exc:`ValueError` sẽ được đưa ra khi
   :attr:`~SSLContext.check_hostname` được bật nhưng không cung cấp *server_hostname*, vì khi đó sẽ không có tên nào để đối chiếu với chứng chỉ của peer.

   .. versionchanged:: 3.6
      Đã bổ sung đối số *session*.

   .. versionchanged:: 3.7
      Phương thức này trả về một thực thể của :attr:`SSLContext.sslobject_class` thay vì :class:`SSLObject` được ghi cứng.

   .. versionchanged:: 3.14.8
      Các tham số *server_side*, *server_hostname* và *session* hiện được xác thực giống như cách :meth:`SSLContext.wrap_socket` xác thực chúng. Trước đây, một context bật :attr:`~SSLContext.check_hostname` nhưng không có *server_hostname* vẫn được chấp nhận và xác minh chuỗi chứng chỉ, nhưng không bao giờ xác minh danh tính của peer.

.. attribute:: SSLContext.sslobject_class

   Kiểu trả về của :meth:`SSLContext.wrap_bio` mặc định là
   :class:`SSLObject`. Có thể ghi đè thuộc tính này trên một instance của class để trả về một subclass tùy chỉnh của :class:`SSLObject`.

   .. versionadded:: 3.7

.. method:: SSLContext.session_stats()

   Lấy số liệu thống kê về các SSL session do context này tạo hoặc quản lý. Một dictionary được trả về, ánh xạ tên của từng `mục thông tin <https://docs.openssl.org/1.1.1/man3/SSL_CTX_sess_number/>`_ với các giá trị số tương ứng. Ví dụ: sau đây là tổng số lượt truy cập và bỏ lỡ trong session cache kể từ khi context được tạo::

      >>> stats = context.session_stats()
      >>> stats['hits'], stats['misses']
      (0, 0)

.. attribute:: SSLContext.check_hostname

   Có khớp hostname của chứng chỉ peer trong
   :meth:`SSLSocket.do_handshake`. Thuộc tính của context
   :attr:`~SSLContext.verify_mode` phải được đặt thành :data:`CERT_OPTIONAL` hoặc
   :data:`CERT_REQUIRED`, và bạn phải truyền *server_hostname* vào
   :meth:`~SSLContext.wrap_socket` để khớp với hostname. Việc bật kiểm tra hostname sẽ tự động đặt :attr:`~SSLContext.verify_mode` từ
   :data:`CERT_NONE` thành :data:`CERT_REQUIRED`. Không thể đặt lại thành
   :data:`CERT_NONE` chừng nào việc kiểm tra hostname còn được bật. Giao thức
   :data:`PROTOCOL_TLS_CLIENT` bật kiểm tra hostname theo mặc định. Với các giao thức khác, phải bật kiểm tra hostname một cách tường minh.

   Ví dụ::

      import socket, ssl

      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
      context.verify_mode = ssl.CERT_REQUIRED
      context.check_hostname = True
      context.load_default_certs()

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      ssl_sock = context.wrap_socket(s, server_hostname='www.verisign.com')
      ssl_sock.connect(('www.verisign.com', 443))

   .. versionadded:: 3.4

   .. versionchanged:: 3.7

      :attr:`~SSLContext.verify_mode` hiện được tự động thay đổi thành :data:`CERT_REQUIRED` khi tính năng kiểm tra hostname được bật và
      :attr:`~SSLContext.verify_mode` là :data:`CERT_NONE`. Trước đây, thao tác tương tự sẽ thất bại với :exc:`ValueError`.

.. attribute:: SSLContext.keylog_filename

   Ghi các khóa TLS vào tệp keylog bất cứ khi nào key material được tạo hoặc nhận. Tệp keylog chỉ được thiết kế cho mục đích debug. Định dạng tệp do NSS quy định và được nhiều traffic analyzer như Wireshark sử dụng. Tệp log được mở ở chế độ chỉ ghi nối tiếp. Các thao tác ghi được đồng bộ giữa các thread, nhưng không được đồng bộ giữa các process.

   .. versionadded:: 3.8

.. attribute:: SSLContext.maximum_version

   Một thành viên enum :class:`TLSVersion` đại diện cho phiên bản TLS được hỗ trợ cao nhất. Giá trị mặc định là :attr:`TLSVersion.MAXIMUM_SUPPORTED`. Thuộc tính này ở chế độ chỉ đọc đối với các protocol khác với :const:`PROTOCOL_TLS`,
   :const:`PROTOCOL_TLS_CLIENT`, và :const:`PROTOCOL_TLS_SERVER`.

   Các thuộc tính :attr:`~SSLContext.maximum_version`,
   :attr:`~SSLContext.minimum_version` và
   :attr:`SSLContext.options` tất cả đều ảnh hưởng đến các phiên bản SSL và TLS được context hỗ trợ. Phần triển khai không ngăn chặn các tổ hợp không hợp lệ. Ví dụ: một context có
   :attr:`OP_NO_TLSv1_2` trong :attr:`~SSLContext.options` và
   :attr:`~SSLContext.maximum_version` được đặt thành :attr:`TLSVersion.TLSv1_2` sẽ không thể thiết lập kết nối TLS 1.2.

   .. versionadded:: 3.7

.. attribute:: SSLContext.minimum_version

   Tương tự như :attr:`SSLContext.maximum_version`, ngoại trừ đây là phiên bản được hỗ trợ thấp nhất hoặc :attr:`TLSVersion.MINIMUM_SUPPORTED`.

   .. versionadded:: 3.7

.. attribute:: SSLContext.num_tickets

   Điều khiển số lượng session ticket TLS 1.3 của một
   :const:`PROTOCOL_TLS_SERVER` context. Thiết lập này không ảnh hưởng đến các kết nối TLS 1.0 đến 1.2.

   .. versionadded:: 3.8

.. attribute:: SSLContext.options

   Một số nguyên biểu thị tập hợp các tùy chọn SSL được bật trên ngữ cảnh này. Giá trị mặc định là :data:`OP_ALL`, nhưng bạn có thể chỉ định các tùy chọn khác như :data:`OP_NO_SSLv2` bằng cách OR chúng với nhau.

   .. versionchanged:: 3.6
      :attr:`SSLContext.options` returns :class:`Options` flags:

         >>> ssl.create_default_context().options  # doctest: +SKIP
         <Options.OP_ALL|OP_NO_SSLv3|OP_NO_SSLv2|OP_NO_COMPRESSION: 2197947391>

   .. deprecated:: 3.7

      Tất cả các tùy chọn ``OP_NO_SSL*`` và ``OP_NO_TLS*`` đã bị deprecated kể từ Python 3.7. Hãy sử dụng :attr:`SSLContext.minimum_version` và
      :attr:`SSLContext.maximum_version` thay thế.

.. attribute:: SSLContext.post_handshake_auth

   Bật xác thực client sau handshake TLS 1.3. Xác thực sau handshake bị tắt theo mặc định và server chỉ có thể yêu cầu chứng chỉ client TLS trong handshake ban đầu. Khi được bật, server có thể yêu cầu chứng chỉ client TLS vào bất kỳ thời điểm nào sau handshake.

   Khi được bật trên các socket phía client, client sẽ báo hiệu cho server rằng nó hỗ trợ xác thực sau handshake.

   Khi được bật trên các socket phía server, :attr:`SSLContext.verify_mode` cũng phải được đặt thành :data:`CERT_OPTIONAL` hoặc :data:`CERT_REQUIRED`. Việc trao đổi chứng chỉ client thực tế được trì hoãn cho đến khi
   :meth:`SSLSocket.verify_client_post_handshake` được gọi và một số thao tác I/O được thực hiện.

   .. versionadded:: 3.8

.. attribute:: SSLContext.protocol

   Phiên bản giao thức được chọn khi xây dựng context. Thuộc tính này chỉ có thể đọc.

.. attribute:: SSLContext.hostname_checks_common_name

   Liệu :attr:`~SSLContext.check_hostname` có chuyển sang xác minh common name của subject trong cert khi không có phần mở rộng subject alternative name hay không (mặc định: true).

   .. versionadded:: 3.7

   .. versionchanged:: 3.10

      Cờ này không có tác dụng với OpenSSL trước phiên bản 1.1.1l. Python 3.8.9, 3.9.3 và 3.10 có các giải pháp khắc phục cho những phiên bản trước đó.

.. attribute:: SSLContext.security_level

   Một số nguyên biểu thị `security level <https://docs.openssl.org/master/man3/SSL_CTX_get_security_level/>`_ cho context. Thuộc tính này chỉ có thể đọc.

   .. versionadded:: 3.10

.. attribute:: SSLContext.verify_flags

   Các cờ cho những thao tác xác minh chứng chỉ. Bạn có thể đặt các cờ như
   :data:`VERIFY_CRL_CHECK_LEAF` bằng cách OR chúng với nhau. Theo mặc định, OpenSSL không yêu cầu cũng không xác minh danh sách thu hồi chứng chỉ (CRL).

   .. versionadded:: 3.4

   .. versionchanged:: 3.6
      :attr:`SSLContext.verify_flags` returns :class:`VerifyFlags` flags:

         >>> ssl.create_default_context().verify_flags  # doctest: +SKIP
         <VerifyFlags.VERIFY_X509_TRUSTED_FIRST: 32768>

.. attribute:: SSLContext.verify_mode

   Liệu có thử xác minh chứng chỉ của các peer khác hay không và sẽ xử lý thế nào nếu việc xác minh thất bại. Thuộc tính này phải là một trong các giá trị
   :data:`CERT_NONE`, :data:`CERT_OPTIONAL` hoặc :data:`CERT_REQUIRED`.

   .. versionchanged:: 3.6
      :attr:`SSLContext.verify_mode` returns :class:`VerifyMode` enum:

         >>> ssl.create_default_context().verify_mode  # doctest: +SKIP
         <VerifyMode.CERT_REQUIRED: 2>

.. method:: SSLContext.set_psk_client_callback(callback)

   Bật xác thực TLS-PSK (khóa chia sẻ trước) trên kết nối phía client.

   Nhìn chung, nên ưu tiên xác thực dựa trên certificate hơn phương thức này.

   Tham số ``callback`` là một đối tượng callable có chữ ký: ``def callback(hint: str | None) -> tuple[str | None, bytes]``. Tham số ``hint`` là gợi ý identity tùy chọn được server gửi. Giá trị trả về là một tuple có dạng (client-identity, psk). Client-identity là một chuỗi tùy chọn mà server có thể dùng để chọn PSK tương ứng cho client. Chuỗi này phải có độ dài nhỏ hơn hoặc bằng ``256`` octet khi được mã hóa bằng UTF-8. PSK là một
   :term:`bytes-like object` đại diện cho khóa chia sẻ trước. Trả về PSK có độ dài bằng 0 để từ chối kết nối.

   Đặt ``callback`` thành :const:`None` sẽ xóa mọi callback hiện có.

   .. note::
      Khi sử dụng TLS 1.3:

      - tham số ``hint`` luôn là :const:`None`.
      - client-identity phải là một chuỗi không rỗng.

   Ví dụ sử dụng::

      context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
      context.check_hostname = False
      context.verify_mode = ssl.CERT_NONE
      context.maximum_version = ssl.TLSVersion.TLSv1_2
      context.set_ciphers('PSK')

      # Một lambda đơn giản:
      psk = bytes.fromhex('c0ffee')
      context.set_psk_client_callback(lambda hint: (None, psk))

      # Một bảng sử dụng gợi ý từ server:
      psk_table = { 'ServerId_1': bytes.fromhex('c0ffee'),
                    'ServerId_2': bytes.fromhex('facade')
      }
      def callback(hint):
          return 'ClientId_1', psk_table.get(hint, b'')
      context.set_psk_client_callback(callback)

   Phương thức này sẽ phát sinh :exc:`NotImplementedError` nếu :data:`HAS_PSK` là ``False``.

   .. versionadded:: 3.13

.. method:: SSLContext.set_psk_server_callback(callback, identity_hint=None)

   Bật xác thực TLS-PSK (pre-shared key) trên kết nối phía server.

   Nhìn chung, nên ưu tiên xác thực dựa trên certificate hơn phương thức này.

   Tham số ``callback`` là một đối tượng có thể gọi với signature: ``def callback(identity: str | None) -> bytes``. Tham số ``identity`` là một identity tùy chọn do client gửi, có thể được dùng để chọn PSK tương ứng. Giá trị trả về là một :term:`bytes-like object` đại diện cho khóa được chia sẻ trước. Trả về PSK có độ dài bằng 0 để từ chối kết nối.

   Đặt ``callback`` thành :const:`None` sẽ xóa mọi callback hiện có.

   Tham số ``identity_hint`` là một chuỗi gợi ý identity tùy chọn được gửi đến client. Chuỗi này phải có độ dài nhỏ hơn hoặc bằng ``256`` octet khi được mã hóa bằng UTF-8.

   .. note::
      Khi sử dụng TLS 1.3, tham số ``identity_hint`` không được gửi đến client.

   Ví dụ sử dụng::

      context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
      context.maximum_version = ssl.TLSVersion.TLSv1_2
      context.set_ciphers('PSK')

      # Một lambda đơn giản:
      psk = bytes.fromhex('c0ffee')
      context.set_psk_server_callback(lambda identity: psk)

      # Một bảng sử dụng danh tính của client:
      psk_table = { 'ClientId_1': bytes.fromhex('c0ffee'),
                    'ClientId_2': bytes.fromhex('facade')
      }
      def callback(identity):
          return psk_table.get(identity, b'')
      context.set_psk_server_callback(callback, 'ServerId_1')

   Phương thức này sẽ phát sinh :exc:`NotImplementedError` nếu :data:`HAS_PSK` là ``False``.

   .. versionadded:: 3.13

.. index:: single: certificates

.. index:: single: X509 certificate

.. _ssl-certificates:

Chứng chỉ
---------

Chứng chỉ nói chung là một phần của hệ thống khóa công khai / khóa riêng tư. Trong hệ thống này, mỗi *principal* (có thể là máy, cá nhân hoặc tổ chức) được gán một khóa mã hóa gồm hai phần duy nhất. Một phần của khóa được công khai và gọi là *public key*; phần còn lại được giữ bí mật và gọi là *private key*. Hai phần này có mối liên hệ với nhau: nếu bạn mã hóa một thông điệp bằng một phần, bạn có thể giải mã thông điệp đó bằng phần còn lại, và **chỉ** bằng phần còn lại.

Một chứng chỉ chứa thông tin về hai principal. Chứng chỉ chứa tên của *subject* và public key của subject. Chứng chỉ cũng chứa một tuyên bố của principal thứ hai, *issuer*, rằng subject đúng là người mà họ tự nhận và đây thực sự là public key của subject. Tuyên bố của issuer được ký bằng private key của issuer, chỉ issuer biết khóa này. Tuy nhiên, bất kỳ ai cũng có thể xác minh tuyên bố của issuer bằng cách tìm public key của issuer, giải mã tuyên bố bằng khóa đó rồi so sánh với các thông tin khác trong chứng chỉ. Chứng chỉ cũng chứa thông tin về khoảng thời gian chứng chỉ có hiệu lực. Khoảng thời gian này được thể hiện bằng hai trường có tên là "notBefore" và "notAfter".

Trong Python, client hoặc server có thể dùng chứng chỉ để chứng minh danh tính của mình. Phía bên kia của kết nối mạng cũng có thể được yêu cầu cung cấp chứng chỉ, và chứng chỉ đó có thể được xác thực theo yêu cầu của client hoặc server thực hiện việc xác thực. Có thể thiết lập để lần thử kết nối phát sinh một exception nếu quá trình xác thực thất bại. Việc xác thực được thực hiện tự động bởi framework OpenSSL bên dưới; ứng dụng không cần quan tâm đến cơ chế này. Tuy nhiên, ứng dụng thường cần cung cấp các bộ chứng chỉ để quá trình này có thể diễn ra.

Python sử dụng các tệp để chứa chứng chỉ. Các tệp này phải được định dạng dưới dạng "PEM" (xem :rfc:`1422`), đây là dạng mã hóa base-64 được bao quanh bởi một dòng tiêu đề và một dòng chân trang::

      -----BEGIN CERTIFICATE-----
      ... (certificate in base64 PEM encoding) ...
      -----END CERTIFICATE-----

Chuỗi chứng chỉ
^^^^^^^^^^^^^^^

Các tệp Python chứa chứng chỉ có thể chứa một chuỗi chứng chỉ, đôi khi được gọi là *chuỗi chứng chỉ*. Chuỗi này nên bắt đầu bằng chứng chỉ cụ thể của principal "là" client hoặc server, tiếp theo là chứng chỉ của bên cấp chứng chỉ đó, rồi đến chứng chỉ của bên cấp *chứng chỉ đó*, cứ tiếp tục như vậy lên chuỗi cho đến khi gặp một chứng chỉ *tự ký*, tức là chứng chỉ có subject và issuer giống nhau, đôi khi được gọi là *chứng chỉ gốc*. Các chứng chỉ chỉ cần được nối liên tiếp trong tệp chứng chỉ. Ví dụ, giả sử chúng ta có một chuỗi gồm ba chứng chỉ, từ chứng chỉ máy chủ đến chứng chỉ của certification authority đã ký chứng chỉ máy chủ, rồi đến chứng chỉ gốc của cơ quan đã cấp chứng chỉ cho certification authority đó::

      -----BEGIN CERTIFICATE-----
      ... (certificate for your server)...
      -----END CERTIFICATE-----
      -----BEGIN CERTIFICATE-----
      ... (the certificate for the CA)...
      -----END CERTIFICATE-----
      -----BEGIN CERTIFICATE-----
      ... (the root certificate for the CA's issuer)...
      -----END CERTIFICATE-----

Chứng chỉ CA
^^^^^^^^^^^^

Nếu bạn yêu cầu xác thực chứng chỉ của phía bên kia kết nối, bạn cần cung cấp một tệp "CA certs", chứa các chuỗi chứng chỉ cho từng bên cấp chứng chỉ mà bạn sẵn sàng tin cậy. Một lần nữa, tệp này chỉ chứa các chuỗi đó được nối liên tiếp với nhau. Để xác thực, Python sẽ sử dụng chuỗi đầu tiên trong tệp khớp với yêu cầu. Có thể sử dụng tệp chứng chỉ của nền tảng bằng cách gọi :meth:`SSLContext.load_default_certs`; thao tác này được thực hiện tự động với :func:`.create_default_context`.

Khóa và chứng chỉ kết hợp
^^^^^^^^^^^^^^^^^^^^^^^^^

Thông thường, khóa riêng được lưu trong cùng tệp với chứng chỉ; trong trường hợp này, chỉ cần truyền tham số ``certfile`` cho :meth:`SSLContext.load_cert_chain`. Nếu khóa riêng được lưu cùng chứng chỉ, khóa riêng phải nằm trước chứng chỉ đầu tiên trong chuỗi chứng chỉ::

   -----BEGIN RSA PRIVATE KEY-----
   ... (private key in base64 encoding) ...
   -----END RSA PRIVATE KEY-----
   -----BEGIN CERTIFICATE-----
   ... (certificate in base64 PEM encoding) ...
   -----END CERTIFICATE-----

Chứng chỉ tự ký
^^^^^^^^^^^^^^^

Nếu bạn định tạo một server cung cấp các dịch vụ kết nối được mã hóa bằng SSL, bạn sẽ cần có chứng chỉ cho dịch vụ đó. Có nhiều cách để có được chứng chỉ phù hợp, chẳng hạn như mua chứng chỉ từ một certification authority. Một cách phổ biến khác là tạo chứng chỉ tự ký. Cách đơn giản nhất để thực hiện việc này là dùng gói OpenSSL, với nội dung tương tự như sau::

  % openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
  Generating a 1024 bit RSA private key
  .......++++++
  .............................++++++
  writing new private key to 'cert.pem'
  -----
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [AU]:US
  State or Province Name (full name) [Some-State]:MyState
  Locality Name (eg, city) []:Some City
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:My Organization, Inc.
  Organizational Unit Name (eg, section) []:My Group
  Common Name (eg, YOUR name) []:myserver.mygroup.myorganization.com
  Email Address []:ops@myserver.mygroup.myorganization.com
  %

Nhược điểm của chứng chỉ tự ký là nó chính là root certificate của chính nó, và không ai khác có chứng chỉ này trong bộ nhớ đệm các root certificate đã biết (và đáng tin cậy) của họ.


Ví dụ
-----

Kiểm tra khả năng hỗ trợ SSL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để kiểm tra sự hiện diện của khả năng hỗ trợ SSL trong một bản cài đặt Python, code của người dùng nên sử dụng cách viết sau::

   try:
       import ssl
   except ImportError:
       pass
   else:
       ...  # thực hiện thao tác yêu cầu hỗ trợ SSL

Thao tác phía client
^^^^^^^^^^^^^^^^^^^^

Ví dụ này tạo một ngữ cảnh SSL với các thiết lập bảo mật được khuyến nghị cho socket máy khách, bao gồm cả việc tự động xác minh chứng chỉ::

   >>> context = ssl.create_default_context()

Nếu muốn tự điều chỉnh các thiết lập bảo mật, bạn có thể tạo một ngữ cảnh từ đầu (nhưng hãy lưu ý rằng bạn có thể thiết lập không đúng)::

   >>> context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
   >>> context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")

(đoạn mã này giả định hệ điều hành của bạn đặt một gói chứa tất cả chứng chỉ CA tại ``/etc/ssl/certs/ca-bundle.crt``; nếu không, bạn sẽ gặp lỗi và phải điều chỉnh vị trí này)

Giao thức :data:`PROTOCOL_TLS_CLIENT` cấu hình ngữ cảnh để xác thực chứng chỉ và xác minh hostname. :attr:`~SSLContext.verify_mode` được đặt thành :data:`CERT_REQUIRED` và :attr:`~SSLContext.check_hostname` được đặt thành ``True``. Tất cả các giao thức khác đều tạo ngữ cảnh SSL với các giá trị mặc định không an toàn.

Khi sử dụng ngữ cảnh để kết nối với máy chủ, :const:`CERT_REQUIRED` và :attr:`~SSLContext.check_hostname` sẽ xác thực chứng chỉ máy chủ: chúng đảm bảo chứng chỉ máy chủ được ký bằng một trong các chứng chỉ CA, kiểm tra tính chính xác của chữ ký và xác minh các thuộc tính khác như thời hạn hiệu lực và danh tính của hostname::

   >>> conn = context.wrap_socket(socket.socket(socket.AF_INET),
   ...                            server_hostname="www.python.org")
   >>> conn.connect(("www.python.org", 443))

Sau đó, bạn có thể lấy chứng chỉ::

   >>> cert = conn.getpeercert()

Kiểm tra trực quan cho thấy chứng chỉ thực sự xác định đúng dịch vụ mong muốn (tức là máy chủ HTTPS ``www.python.org``)::

   >>> pprint.pprint(cert)
   {'OCSP': ('http://ocsp.digicert.com',),
    'caIssuers': ('http://cacerts.digicert.com/DigiCertSHA2ExtendedValidationServerCA.crt',),
    'crlDistributionPoints': ('http://crl3.digicert.com/sha2-ev-server-g1.crl',
                              'http://crl4.digicert.com/sha2-ev-server-g1.crl'),
    'issuer': ((('countryName', 'US'),),
               (('organizationName', 'DigiCert Inc'),),
               (('organizationalUnitName', 'www.digicert.com'),),
               (('commonName', 'DigiCert SHA2 Extended Validation Server CA'),)),
    'notAfter': 'Sep  9 12:00:00 2016 GMT',
    'notBefore': 'Sep  5 00:00:00 2014 GMT',
    'serialNumber': '01BB6F00122B177F36CAB49CEA8B6B26',
    'subject': ((('businessCategory', 'Private Organization'),),
                (('1.3.6.1.4.1.311.60.2.1.3', 'US'),),
                (('1.3.6.1.4.1.311.60.2.1.2', 'Delaware'),),
                (('serialNumber', '3359300'),),
                (('streetAddress', '16 Allen Rd'),),
                (('postalCode', '03894-4801'),),
                (('countryName', 'US'),),
                (('stateOrProvinceName', 'NH'),),
                (('localityName', 'Wolfeboro'),),
                (('organizationName', 'Python Software Foundation'),),
                (('commonName', 'www.python.org'),)),
    'subjectAltName': (('DNS', 'www.python.org'),
                       ('DNS', 'python.org'),
                       ('DNS', 'pypi.org'),
                       ('DNS', 'docs.python.org'),
                       ('DNS', 'testpypi.org'),
                       ('DNS', 'bugs.python.org'),
                       ('DNS', 'wiki.python.org'),
                       ('DNS', 'hg.python.org'),
                       ('DNS', 'mail.python.org'),
                       ('DNS', 'packaging.python.org'),
                       ('DNS', 'pythonhosted.org'),
                       ('DNS', 'www.pythonhosted.org'),
                       ('DNS', 'test.pythonhosted.org'),
                       ('DNS', 'us.pycon.org'),
                       ('DNS', 'id.python.org')),
    'version': 3}

Bây giờ kênh SSL đã được thiết lập và chứng chỉ đã được xác minh, bạn có thể tiếp tục trao đổi với máy chủ::

   >>> conn.sendall(b"HEAD / HTTP/1.0\r\nHost: linuxfr.org\r\n\r\n")
   >>> pprint.pprint(conn.recv(1024).split(b"\r\n"))
   [b'HTTP/1.1 200 OK',
    b'Date: Sat, 18 Oct 2014 18:27:20 GMT',
    b'Server: nginx',
    b'Content-Type: text/html; charset=utf-8',
    b'X-Frame-Options: SAMEORIGIN',
    b'Content-Length: 45679',
    b'Accept-Ranges: bytes',
    b'Via: 1.1 varnish',
    b'Age: 2188',
    b'X-Served-By: cache-lcy1134-LCY',
    b'X-Cache: HIT',
    b'X-Cache-Hits: 11',
    b'Vary: Cookie',
    b'Strict-Transport-Security: max-age=63072000; includeSubDomains',
    b'Connection: close',
    b'',
    b'']

Xem phần thảo luận về :ref:`ssl-security` bên dưới.


Thao tác phía máy chủ
^^^^^^^^^^^^^^^^^^^^^

Để vận hành phía máy chủ, thông thường bạn sẽ cần một chứng chỉ máy chủ và khóa riêng, mỗi thứ nằm trong một tệp. Trước tiên, bạn sẽ tạo một context chứa khóa và chứng chỉ để các client có thể kiểm tra tính xác thực của bạn. Sau đó, bạn sẽ mở một socket, liên kết nó với một cổng, gọi :meth:`listen` trên đó và bắt đầu chờ các client kết nối::

   import socket, ssl

   context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
   context.load_cert_chain(certfile="mycertfile", keyfile="mykeyfile")

   bindsocket = socket.socket()
   bindsocket.bind(('myaddr.example.com', 10023))
   bindsocket.listen(5)

Khi một client kết nối, bạn sẽ gọi :meth:`accept` trên socket để lấy socket mới từ phía bên kia, rồi sử dụng phương thức :meth:`SSLContext.wrap_socket` của context để tạo một socket SSL phía máy chủ cho kết nối đó::

   while True:
       newsocket, fromaddr = bindsocket.accept()
       connstream = context.wrap_socket(newsocket, server_side=True)
       try:
           deal_with_client(connstream)
       finally:
           connstream.shutdown(socket.SHUT_RDWR)
           connstream.close()

Sau đó, bạn sẽ đọc dữ liệu từ ``connstream`` và xử lý dữ liệu đó cho đến khi bạn hoàn tất với client (hoặc client hoàn tất với bạn)::

   def deal_with_client(connstream):
       data = connstream.recv(1024)
       # dữ liệu rỗng nghĩa là client đã hoàn tất với chúng ta
       while data:
           if not do_something(connstream, data):
               # giả sử do_something trả về False
               # khi chúng ta hoàn tất với client
               break
           data = connstream.recv(1024)
       # đã hoàn tất với client

Và quay lại chờ các kết nối client mới (tất nhiên, một server thực tế có thể sẽ xử lý từng kết nối client trong một thread riêng, hoặc đặt các socket ở :ref:`chế độ non-blocking <ssl-nonblocking>` và sử dụng một event loop).


.. _ssl-nonblocking:

Lưu ý về socket non-blocking
----------------------------

Socket SSL hoạt động hơi khác so với socket thông thường ở chế độ non-blocking. Vì vậy, khi làm việc với socket non-blocking, bạn cần lưu ý một số điều sau:

- Hầu hết :class:`SSLSocket` các phương thức sẽ raise một trong hai
  :exc:`SSLWantWriteError` hoặc :exc:`SSLWantReadError` thay vì
  :exc:`BlockingIOError` nếu một thao tác I/O có thể bị block. :exc:`SSLWantReadError` sẽ được phát sinh nếu cần thực hiện thao tác đọc trên socket bên dưới, và :exc:`SSLWantWriteError` nếu cần thực hiện thao tác ghi trên socket bên dưới. Lưu ý rằng các lần thử *write* vào một SSL socket có thể yêu cầu *reading* từ socket bên dưới trước, và các lần thử *read* từ SSL socket có thể yêu cầu thực hiện *write* trước đó vào socket bên dưới.

  .. versionchanged:: 3.5

     Trong các phiên bản Python trước đây, phương thức :meth:`!SSLSocket.send` trả về giá trị 0 thay vì phát sinh :exc:`SSLWantWriteError` hoặc
     :exc:`SSLWantReadError`.

- Việc gọi :func:`~select.select` cho biết socket ở cấp hệ điều hành có thể được đọc (hoặc ghi), nhưng không có nghĩa là có đủ dữ liệu ở lớp SSL bên trên. Ví dụ: chỉ một phần của SSL frame có thể đã đến. Do đó, bạn phải sẵn sàng xử lý các lỗi :meth:`SSLSocket.recv` và :meth:`SSLSocket.send`, rồi thử lại sau một lần gọi khác đến
  :func:`~select.select`.

- Ngược lại, vì lớp SSL có cơ chế framing riêng, một SSL socket vẫn có thể còn dữ liệu để đọc mà :func:`~select.select` không biết. Do đó, trước tiên bạn nên gọi
  :meth:`SSLSocket.recv` để lấy hết mọi dữ liệu có thể đang sẵn có, rồi chỉ block trên một lần gọi :func:`~select.select` nếu vẫn cần thiết.

  (dĩ nhiên, các quy định tương tự cũng áp dụng khi sử dụng những primitive khác như
  :func:`~select.poll`, hoặc những socket trong module :mod:`selectors`)

- Bản thân quá trình bắt tay SSL sẽ không chặn:
  Phương thức :meth:`SSLSocket.do_handshake` phải được thử lại cho đến khi trả về thành công. Sau đây là phần tóm lược sử dụng :func:`~select.select` để chờ socket sẵn sàng::

    while True:
        try:
            sock.do_handshake()
            break
        except ssl.SSLWantReadError:
            select.select([sock], [], [])
        except ssl.SSLWantWriteError:
            select.select([], [sock], [])

.. seealso::

   Module :mod:`asyncio` hỗ trợ :ref:`các socket SSL không chặn <ssl-nonblocking>` và cung cấp :ref:`Streams API <asyncio-streams>` ở cấp độ cao hơn. Module này thăm dò các sự kiện bằng module :mod:`selectors` và xử lý :exc:`SSLWantWriteError`, :exc:`SSLWantReadError` và
   :exc:`BlockingIOError` ngoại lệ. Nó cũng thực hiện bắt tay SSL một cách bất đồng bộ.


Hỗ trợ Memory BIO
-----------------

.. versionadded:: 3.5

Kể từ khi mô-đun SSL được giới thiệu trong Python 2.6, lớp :class:`SSLSocket` đã cung cấp hai lĩnh vực chức năng có liên quan nhưng khác biệt:

- Xử lý giao thức SSL
- I/O mạng

API I/O mạng giống hệt API do :class:`socket.socket` cung cấp, từ đó :class:`SSLSocket` cũng kế thừa. Điều này cho phép sử dụng một SSL socket để thay thế trực tiếp cho socket thông thường, nhờ đó việc thêm hỗ trợ SSL vào một ứng dụng hiện có trở nên rất dễ dàng.

Việc kết hợp xử lý giao thức SSL và I/O mạng thường hoạt động tốt, nhưng có một số trường hợp không như vậy. Một ví dụ là các framework async IO muốn sử dụng mô hình ghép kênh I/O khác với mô hình "select/poll trên một file descriptor" (dựa trên trạng thái sẵn sàng) mà :class:`socket.socket` và các routine I/O socket nội bộ của OpenSSL giả định. Điều này đặc biệt liên quan đến các nền tảng như Windows, nơi mô hình này không hiệu quả. Vì mục đích này, một biến thể có phạm vi chức năng thu gọn của :class:`SSLSocket` có tên là :class:`SSLObject` được cung cấp.

.. class:: SSLObject

   Một biến thể có phạm vi chức năng thu gọn của :class:`SSLSocket`, đại diện cho một thực thể giao thức SSL không chứa bất kỳ phương thức I/O mạng nào. Lớp này thường được các tác giả framework sử dụng khi muốn triển khai I/O bất đồng bộ cho SSL thông qua các bộ đệm bộ nhớ.

   Lớp này triển khai một interface trên một đối tượng SSL cấp thấp do OpenSSL triển khai. Đối tượng này lưu giữ trạng thái của một kết nối SSL nhưng bản thân không cung cấp I/O mạng. I/O cần được thực hiện thông qua các đối tượng "BIO" riêng biệt, là lớp trừu tượng I/O của OpenSSL.

   Lớp này không có constructor công khai. Một instance :class:`SSLObject` phải được tạo bằng phương thức :meth:`~SSLContext.wrap_bio`. Phương thức này sẽ tạo instance :class:`SSLObject` và liên kết nó với một cặp BIO. BIO *incoming* được dùng để truyền dữ liệu từ Python đến thực thể giao thức SSL, trong khi BIO *outgoing* được dùng để truyền dữ liệu theo chiều ngược lại.

   Các phương thức sau đây khả dụng:

   - :attr:`~SSLSocket.context`
   - :attr:`~SSLSocket.server_side`
   - :attr:`~SSLSocket.server_hostname`
   - :attr:`~SSLSocket.session`
   - :attr:`~SSLSocket.session_reused`
   - :meth:`~SSLSocket.read`
   - :meth:`~SSLSocket.write`
   - :meth:`~SSLSocket.getpeercert`
   - :meth:`~SSLSocket.get_verified_chain`
   - :meth:`~SSLSocket.get_unverified_chain`
   - :meth:`~SSLSocket.selected_alpn_protocol`
   - :meth:`~SSLSocket.selected_npn_protocol`
   - :meth:`~SSLSocket.cipher`
   - :meth:`~SSLSocket.shared_ciphers`
   - :meth:`~SSLSocket.compression`
   - :meth:`~SSLSocket.pending`
   - :meth:`~SSLSocket.do_handshake`
   - :meth:`~SSLSocket.verify_client_post_handshake`
   - :meth:`~SSLSocket.unwrap`
   - :meth:`~SSLSocket.get_channel_binding`
   - :meth:`~SSLSocket.version`

   So với :class:`SSLSocket`, đối tượng này thiếu các tính năng sau:

   - Không có bất kỳ dạng I/O mạng nào; ``recv()`` và ``send()`` chỉ đọc và ghi vào các bộ đệm :class:`MemoryBIO` bên dưới.

   - Không có cơ chế *do_handshake_on_connect*. Bạn luôn phải tự gọi :meth:`~SSLSocket.do_handshake` để bắt đầu handshake.

   - Không có cơ chế xử lý *suppress_ragged_eofs*. Mọi điều kiện kết thúc tệp vi phạm giao thức đều được báo cáo thông qua
     :exc:`SSLEOFError` exception.

   - Lệnh gọi phương thức :meth:`~SSLSocket.unwrap` không trả về gì cả, không giống như đối với một SSL socket, khi nó trả về socket bên dưới.

   - Callback *server_name_callback* được truyền vào
     :meth:`SSLContext.set_servername_callback` sẽ nhận một instance :class:`SSLObject` thay vì một instance :class:`SSLSocket` làm tham số đầu tiên.

   Một số lưu ý liên quan đến việc sử dụng :class:`SSLObject`:

   - Mọi thao tác IO trên :class:`SSLObject` đều :ref:`không chặn <ssl-nonblocking>`. Điều này có nghĩa là, chẳng hạn, :meth:`~SSLSocket.read` sẽ gây ra một
     :exc:`SSLWantReadError` nếu nó cần nhiều dữ liệu hơn lượng dữ liệu BIO đầu vào hiện có.

   .. versionchanged:: 3.7
      :class:`SSLObject` instances must be created with
      :meth:`~SSLContext.wrap_bio`. In earlier versions, it was possible to
      tạo trực tiếp các instance. Điều này chưa bao giờ được ghi lại trong tài liệu hoặc được hỗ trợ chính thức.

Một SSLObject giao tiếp với thế giới bên ngoài bằng các bộ đệm bộ nhớ. Lớp :class:`MemoryBIO` cung cấp một bộ đệm bộ nhớ có thể được sử dụng cho mục đích này. Nó bao bọc một đối tượng BIO bộ nhớ OpenSSL (Basic IO):

.. class:: MemoryBIO

   Một bộ đệm bộ nhớ có thể được sử dụng để truyền dữ liệu giữa Python và một phiên bản giao thức SSL.

   .. attribute:: MemoryBIO.pending

      Trả về số byte hiện có trong bộ đệm bộ nhớ.

   .. attribute:: MemoryBIO.eof

      Một giá trị boolean cho biết BIO bộ nhớ hiện đang ở vị trí cuối tệp hay không.

   .. method:: MemoryBIO.read(n=-1, /)

      Đọc tối đa *n* byte từ bộ đệm bộ nhớ. Nếu không chỉ định *n* hoặc giá trị này là số âm, tất cả byte sẽ được trả về.

   .. method:: MemoryBIO.write(buf, /)

      Ghi các byte từ *buf* vào BIO bộ nhớ. Đối số *buf* phải là một đối tượng hỗ trợ buffer protocol.

      Giá trị trả về là số byte đã ghi, luôn bằng độ dài của *buf*.

   .. method:: MemoryBIO.write_eof()

      Ghi một dấu EOF vào BIO bộ nhớ. Sau khi phương thức này được gọi, việc gọi :meth:`~MemoryBIO.write` là không hợp lệ. Thuộc tính :attr:`eof` sẽ trở thành true sau khi tất cả dữ liệu hiện có trong bộ đệm đã được đọc.


phiên SSL
---------

.. versionadded:: 3.6

.. class:: SSLSession

   Đối tượng phiên được :attr:`~SSLSocket.session` sử dụng.

   .. attribute:: id
   .. attribute:: time
   .. attribute:: timeout
   .. attribute:: ticket_lifetime_hint
   .. attribute:: has_ticket


.. _ssl-security:

Các vấn đề về bảo mật
---------------------

Các thiết lập mặc định tốt nhất
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để sử dụng **client use**, nếu bạn không có yêu cầu đặc biệt nào đối với chính sách bảo mật, bạn rất nên sử dụng
hàm :func:`create_default_context`. Hàm này sẽ tải các chứng chỉ CA đáng tin cậy của hệ thống, bật tính năng xác thực chứng chỉ và kiểm tra hostname, đồng thời cố gắng chọn các thiết lập giao thức và cipher tương đối an toàn.

Ví dụ: sau đây là cách bạn sử dụng lớp :class:`smtplib.SMTP` để tạo một kết nối đáng tin cậy và an toàn tới máy chủ SMTP::

   >>> import ssl, smtplib
   >>> smtp = smtplib.SMTP("mail.python.org", port=587)
   >>> context = ssl.create_default_context()
   >>> smtp.starttls(context=context)
   (220, b'2.0.0 Ready to start TLS')

Nếu cần chứng chỉ client cho kết nối, bạn có thể thêm chứng chỉ này bằng
:meth:`SSLContext.load_cert_chain`.

Ngược lại, nếu bạn tự tạo SSL context bằng cách gọi constructor :class:`SSLContext`, theo mặc định, context này sẽ không bật tính năng xác thực chứng chỉ hoặc kiểm tra hostname. Nếu làm như vậy, hãy đọc các đoạn bên dưới để đạt được mức bảo mật tốt.

Cài đặt thủ công
^^^^^^^^^^^^^^^^

Xác minh chứng chỉ
''''''''''''''''''

Khi gọi trực tiếp constructor :class:`SSLContext`,
:const:`CERT_NONE` là giá trị mặc định. Vì không xác thực peer còn lại, tùy chọn này có thể không an toàn, đặc biệt ở client mode, khi phần lớn thời gian bạn muốn đảm bảo tính xác thực của server mà mình đang kết nối. Do đó, khi ở client mode, bạn rất nên sử dụng
:const:`CERT_REQUIRED`. Tuy nhiên, chỉ riêng tùy chọn này vẫn chưa đủ; bạn cũng phải kiểm tra chứng chỉ server, có thể lấy được bằng cách gọi
:meth:`SSLSocket.getpeercert`, khớp với dịch vụ mong muốn. Đối với nhiều giao thức và ứng dụng, dịch vụ có thể được xác định bằng hostname. Kiểm tra phổ biến này được tự động thực hiện khi
:attr:`SSLContext.check_hostname` được bật.

.. versionchanged:: 3.7
   Việc đối sánh hostname hiện do OpenSSL thực hiện. Python không còn sử dụng
   :func:`!match_hostname`.

Ở chế độ máy chủ, nếu bạn muốn xác thực các client bằng lớp SSL (thay vì sử dụng cơ chế xác thực cấp cao hơn), bạn cũng sẽ phải chỉ định :const:`CERT_REQUIRED` và tương tự kiểm tra certificate của client.


Các phiên bản giao thức
'''''''''''''''''''''''

SSL phiên bản 2 và 3 được xem là không an toàn và do đó rất nguy hiểm khi sử dụng. Nếu bạn muốn đạt khả năng tương thích tối đa giữa client và máy chủ, nên sử dụng :const:`PROTOCOL_TLS_CLIENT` hoặc
:const:`PROTOCOL_TLS_SERVER` làm phiên bản giao thức. SSLv2 và SSLv3 bị tắt theo mặc định.

::

   >>> client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
   >>> client_context.minimum_version = ssl.TLSVersion.TLSv1_2
   >>> client_context.maximum_version = ssl.TLSVersion.TLSv1_3


Ngữ cảnh SSL client được tạo ở trên sẽ chỉ cho phép các kết nối TLSv1.2 và TLSv1.3 (nếu hệ thống của bạn hỗ trợ) đến máy chủ. :const:`PROTOCOL_TLS_CLIENT` mặc định bao hàm việc xác thực chứng chỉ và kiểm tra hostname. Bạn phải tải các chứng chỉ vào ngữ cảnh.


Lựa chọn cipher
'''''''''''''''

Nếu bạn có các yêu cầu bảo mật nâng cao, có thể tinh chỉnh các cipher được bật khi thương lượng một phiên SSL thông qua
phương thức :meth:`SSLContext.set_ciphers`. Kể từ Python 3.2.3, mô-đun ssl mặc định vô hiệu hóa một số cipher yếu, nhưng bạn có thể muốn hạn chế thêm lựa chọn cipher. Hãy đọc tài liệu của OpenSSL về định dạng danh sách cipher `cipher list format <https://docs.openssl.org/1.1.1/man1/ciphers/#cipher-list-format>`_. Nếu muốn kiểm tra những cipher nào được bật bởi một danh sách cipher cụ thể, hãy sử dụng
:meth:`SSLContext.get_ciphers` hoặc lệnh ``openssl ciphers`` trên hệ thống của bạn.

Đa tiến trình
^^^^^^^^^^^^^

Nếu sử dụng mô-đun này trong một ứng dụng đa tiến trình (chẳng hạn như sử dụng các mô-đun :mod:`multiprocessing` hoặc :mod:`concurrent.futures`), hãy lưu ý rằng trình tạo số ngẫu nhiên nội bộ của OpenSSL không xử lý đúng các tiến trình được tạo bằng fork. Ứng dụng phải thay đổi trạng thái PRNG của tiến trình cha nếu sử dụng bất kỳ tính năng SSL nào với :func:`os.fork`. Mọi lần gọi thành công :func:`~ssl.RAND_add` hoặc :func:`~ssl.RAND_bytes` đều đáp ứng yêu cầu.


.. _ssl-tlsv1_3:

TLS 1.3
-------

.. versionadded:: 3.7

Giao thức TLS 1.3 hoạt động hơi khác so với các phiên bản TLS/SSL trước đây. Một số tính năng mới của TLS 1.3 hiện chưa khả dụng.

- TLS 1.3 sử dụng một nhóm cipher suite riêng. Tất cả cipher suite AES-GCM và ChaCha20 đều được bật theo mặc định. Phương thức
  :meth:`SSLContext.set_ciphers` hiện chưa thể bật hoặc tắt bất kỳ cipher TLS 1.3 nào, nhưng :meth:`SSLContext.get_ciphers` sẽ trả về chúng.
- Session ticket không còn được gửi trong quá trình bắt tay ban đầu và được xử lý theo cách khác. :attr:`SSLSocket.session` và :class:`SSLSession` không tương thích với TLS 1.3.
- Certificate phía client cũng không còn được xác minh trong quá trình bắt tay ban đầu. Server có thể yêu cầu certificate bất kỳ lúc nào. Client xử lý các yêu cầu certificate trong khi gửi hoặc nhận dữ liệu ứng dụng từ server.
- Các tính năng TLS 1.3 như dữ liệu sớm, yêu cầu certificate client TLS trì hoãn, cấu hình thuật toán chữ ký và rekeying hiện chưa được hỗ trợ.


.. seealso::

   Lớp :class:`socket.socket`
       Tài liệu về lớp nền tảng :mod:`socket`

   `Mã hóa mạnh SSL/TLS: Giới thiệu <https://httpd.apache.org/docs/trunk/en/ssl/ssl_intro.html>`_
       Phần giới thiệu từ tài liệu Apache HTTP Server

   :rfc:`RFC 1422: Privacy Enhancement for Internet Electronic Mail: Part II: Certificate-Based Key Management <1422>`
       Steve Kent

   :rfc:`RFC 4086: Randomness Requirements for Security <4086>`
       Donald E. Eastlake, Jeffrey I. Schiller, Steve Crocker

   :rfc:`RFC 5280: Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile <5280>`
       David Cooper và cộng sự

   :rfc:`RFC 5246: The Transport Layer Security (TLS) Protocol Version 1.2 <5246>`
       Tim Dierks và Eric Rescorla.

   :rfc:`RFC 6066: Transport Layer Security (TLS) Extensions <6066>`
       Donald E. Eastlake

   `Các tham số IANA TLS: Bảo mật tầng truyền tải (TLS) <https://www.iana.org/assignments/tls-parameters/tls-parameters.xml>`_
       IANA

   :rfc:`RFC 7525: Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS) <7525>`
       IETF

   `Các khuyến nghị TLS phía máy chủ của Mozilla <https://wiki.mozilla.org/Security/Server_Side_TLS>`_
       Mozilla

.. _`completely broken`: https://en.wikipedia.org/wiki/POODLE
.. _`Cryptographically secure pseudorandom number generator (CSPRNG)`: https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator
.. _`Application Layer Protocol Negotiation`: https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation
.. _`IANA TLS Alert Registry`: https://www.iana.org/assignments/tls-parameters/tls-parameters.xml#tls-parameters-6
.. _`OpenSSL specific layout`: https://docs.openssl.org/master/man3/SSL_CTX_load_verify_locations/
.. _`OpenSSL cipher list format`: https://docs.openssl.org/master/man1/ciphers/
.. _`SSL/TLS & Perfect Forward Secrecy`: https://vincent.bernat.ch/en/blog/2011-ssl-perfect-forward-secrecy
.. _`piece of information`: https://docs.openssl.org/1.1.1/man3/SSL_CTX_sess_number/
.. _`security level`: https://docs.openssl.org/master/man3/SSL_CTX_get_security_level/
.. _`cipher list format`: https://docs.openssl.org/1.1.1/man1/ciphers/#cipher-list-format
.. _`SSL/TLS Strong Encryption: An Introduction`: https://httpd.apache.org/docs/trunk/en/ssl/ssl_intro.html
.. _`IANA TLS: Transport Layer Security (TLS) Parameters`: https://www.iana.org/assignments/tls-parameters/tls-parameters.xml
.. _`Mozilla's Server Side TLS recommendations`: https://wiki.mozilla.org/Security/Server_Side_TLS
