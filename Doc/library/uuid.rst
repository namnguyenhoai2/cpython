:mod:`!uuid` --- Các đối tượng UUID theo :rfc:`9562`
====================================================

.. module:: uuid
   :synopsis: Các đối tượng UUID (mã định danh duy nhất trên toàn cầu) theo RFC 9562
.. moduleauthor:: Ka-Ping Yee <ping@zesty.ca>
.. sectionauthor:: George Yoshida <quiver@users.sourceforge.net>

**Mã nguồn:** :source:`Lib/uuid.py`

--------------

Mô-đun này cung cấp các đối tượng :class:`UUID` bất biến (lớp :class:`UUID`) và :ref:`hàm <uuid-factory-functions>` để tạo UUID tương ứng với một phiên bản UUID cụ thể như được quy định trong :rfc:`9562` (thay thế :rfc:`4122`), chẳng hạn như :func:`uuid1` cho UUID phiên bản 1, :func:`uuid3` cho UUID phiên bản 3, v.v. Lưu ý rằng UUID phiên bản 2 bị cố ý lược bỏ vì nằm ngoài phạm vi của RFC.

Nếu tất cả những gì bạn cần là một ID duy nhất, có lẽ bạn nên gọi :func:`uuid1` hoặc
:func:`uuid4`.  Lưu ý rằng :func:`uuid1` có thể xâm phạm quyền riêng tư vì nó tạo một UUID chứa địa chỉ mạng của máy tính.  :func:`uuid4` tạo một UUID ngẫu nhiên.

Tùy thuộc vào mức hỗ trợ của nền tảng bên dưới, :func:`uuid1` có thể trả về hoặc không trả về một UUID "an toàn". UUID an toàn là UUID được tạo bằng các phương thức đồng bộ hóa, bảo đảm không có hai tiến trình nào có thể nhận được cùng một UUID. Tất cả các thực thể của :class:`UUID` đều có thuộc tính :attr:`~UUID.is_safe` truyền đạt mọi thông tin về mức độ an toàn của UUID, bằng cách sử dụng enumeration này:

.. class:: SafeUUID

   .. versionadded:: 3.7

   .. attribute:: SafeUUID.safe

      UUID được nền tảng tạo theo cách an toàn khi xử lý đa tiến trình.

   .. attribute:: SafeUUID.unsafe

      UUID không được tạo theo cách an toàn khi xử lý đa tiến trình.

   .. attribute:: SafeUUID.unknown

      Nền tảng không cung cấp thông tin về việc UUID có được tạo một cách an toàn hay không.

.. class:: UUID(hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None, *, is_safe=SafeUUID.unknown)

   Tạo UUID từ một chuỗi gồm 32 chữ số thập lục phân hoặc một chuỗi 16 byte
   đối tượng :class:`bytes` theo thứ tự big-endian làm đối số *bytes*, đối tượng :class:`bytes` 16 byte theo thứ tự little-endian làm đối số *bytes_le*, một tuple gồm sáu số nguyên (32-bit *time_low*, 16-bit *time_mid*, 16-bit *time_hi_version*, 8-bit *clock_seq_hi_variant*, 8-bit *clock_seq_low*, 48-bit *node*) làm đối số *fields*, hoặc một số nguyên 128-bit duy nhất làm đối số *int*. Khi cung cấp một chuỗi chữ số hex, dấu ngoặc nhọn, dấu gạch nối và tiền tố URN đều là tùy chọn. Ví dụ: các biểu thức sau đều tạo ra cùng một UUID::

      UUID('{12345678-1234-5678-1234-567812345678}')
      UUID('12345678123456781234567812345678')
      UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
      UUID(bytes=b'\x12\x34\x56\x78'*4)
      UUID(bytes_le=b'\x78\x56\x34\x12\x34\x12\x78\x56' +
                    b'\x12\x34\x56\x78\x12\x34\x56\x78')
      UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
      UUID(int=0x12345678123456781234567812345678)

   Phải cung cấp chính xác một trong các đối số *hex*, *bytes*, *bytes_le*, *fields* hoặc *int*. Đối số *version* là tùy chọn; nếu được cung cấp, UUID kết quả sẽ có biến thể và số phiên bản được đặt theo :rfc:`9562`, ghi đè các bit trong *hex*, *bytes*, *bytes_le*, *fields* hoặc *int* đã cung cấp.

   Việc so sánh các đối tượng UUID được thực hiện bằng cách so sánh các
   :attr:`UUID.int` các thuộc tính. Việc so sánh với một đối tượng không phải UUID sẽ phát sinh :exc:`TypeError`.

   ``str(uuid)`` trả về một chuỗi có dạng ``12345678-1234-5678-1234-567812345678``, trong đó 32 chữ số thập lục phân biểu diễn UUID.

Các instance :class:`UUID` có những thuộc tính chỉ đọc sau đây:

.. attribute:: UUID.bytes

   UUID dưới dạng một đối tượng :class:`bytes` 16 byte (chứa sáu trường số nguyên theo thứ tự byte big-endian).


.. attribute:: UUID.bytes_le

   UUID dưới dạng một đối tượng :class:`bytes` 16 byte (với *time_low*, *time_mid* và *time_hi_version* theo thứ tự byte little-endian).


.. attribute:: UUID.fields

   Một tuple gồm sáu trường số nguyên của UUID; các trường này cũng có sẵn dưới dạng sáu thuộc tính riêng lẻ và hai thuộc tính dẫn xuất:

.. list-table::

   * - Trường
     - Ý nghĩa

   * - .. attribute:: UUID.time_low
     - 32 bit đầu tiên của UUID. Chỉ liên quan đến phiên bản 1.

   * - .. attribute:: UUID.time_mid
     - 16 bit tiếp theo của UUID. Chỉ liên quan đến phiên bản 1.

   * - .. attribute:: UUID.time_hi_version
     - 16 bit tiếp theo của UUID. Chỉ liên quan đến phiên bản 1.

   * - .. attribute:: UUID.clock_seq_hi_variant
     - 8 bit tiếp theo của UUID. Chỉ liên quan đến các phiên bản 1 và 6.

   * - .. attribute:: UUID.clock_seq_low
     - 8 bit tiếp theo của UUID. Chỉ liên quan đến các phiên bản 1 và 6.

   * - .. attribute:: UUID.node
     - 48 bit cuối cùng của UUID. Chỉ liên quan đến phiên bản 1.

   * - .. attribute:: UUID.time
     - Dấu thời gian 60 bit dưới dạng số lượng khoảng thời gian 100 nano giây kể từ epoch Gregorian (1582-10-15 00:00:00) đối với phiên bản 1 và 6, hoặc dấu thời gian 48 bit tính bằng mili giây kể từ epoch Unix (1970-01-01 00:00:00) đối với phiên bản 7.

   * - .. attribute:: UUID.clock_seq
     - Số thứ tự 14 bit. Chỉ liên quan đến phiên bản 1 và 6.


.. attribute:: UUID.hex

   UUID dưới dạng chuỗi thập lục phân viết thường gồm 32 ký tự.


.. attribute:: UUID.int

   UUID dưới dạng số nguyên 128 bit.


.. attribute:: UUID.urn

   UUID dưới dạng URN như được chỉ định trong :rfc:`9562`.


.. attribute:: UUID.variant

   Biến thể UUID, xác định bố cục nội bộ của UUID. Giá trị này sẽ là một trong các hằng số :const:`RESERVED_NCS`, :const:`RFC_4122`,
   :const:`RESERVED_MICROSOFT`, hoặc :const:`RESERVED_FUTURE`.


.. attribute:: UUID.version

   Số phiên bản UUID (từ 1 đến 8, chỉ có ý nghĩa khi variant là
   :const:`RFC_4122`).

   .. versionchanged:: 3.14
      Đã thêm các phiên bản UUID 6, 7 và 8.


.. attribute:: UUID.is_safe

   Một kiểu liệt kê của :class:`SafeUUID`, cho biết nền tảng đã tạo UUID theo cách an toàn khi multiprocessing hay chưa.

   .. versionadded:: 3.7

Module :mod:`!uuid` định nghĩa các hàm sau:


.. function:: getnode()

   Lấy địa chỉ phần cứng dưới dạng số nguyên dương 48 bit. Lần đầu chạy, hàm này có thể khởi chạy một chương trình riêng, việc này có thể khá chậm. Nếu mọi lần thử lấy địa chỉ phần cứng đều thất bại, chúng ta chọn một số 48 bit ngẫu nhiên với bit multicast (bit ít quan trọng nhất của octet đầu tiên) được đặt thành 1 như khuyến nghị trong :rfc:`4122`. "Địa chỉ phần cứng" có nghĩa là địa chỉ MAC của một giao diện mạng. Trên máy có nhiều giao diện mạng, các địa chỉ MAC được quản trị toàn cục (tức là trong đó bit ít quan trọng thứ hai của octet đầu tiên là *unset*) sẽ được ưu tiên hơn các địa chỉ MAC được quản trị cục bộ, nhưng không có đảm bảo nào khác về thứ tự.

   .. versionchanged:: 3.7
      Các địa chỉ MAC được quản trị toàn cục được ưu tiên hơn các địa chỉ MAC được quản trị cục bộ, vì các địa chỉ trước được đảm bảo là duy nhất trên toàn cầu, còn các địa chỉ sau thì không.


.. _uuid-factory-functions:

.. function:: uuid1(node=None, clock_seq=None)

   Tạo UUID từ ID máy chủ, số thứ tự và thời gian hiện tại theo :rfc:`RFC 9562, §5.1 <9562#section-5.1>`.

   Khi *node* không được chỉ định, :func:`getnode` được dùng để lấy địa chỉ phần cứng dưới dạng số nguyên dương 48 bit. Khi số thứ tự *clock_seq* không được chỉ định, một số nguyên dương 14 bit giả ngẫu nhiên sẽ được tạo.

   Nếu *node* hoặc *clock_seq* vượt quá số bit dự kiến, chỉ các bit có trọng số thấp nhất của chúng được giữ lại.


.. function:: uuid3(namespace, name)

   Tạo UUID dựa trên hàm băm MD5 của một mã định danh namespace (là một UUID) và một tên (là một đối tượng :class:`bytes` hoặc một chuỗi sẽ được mã hóa bằng UTF-8) theo :rfc:`RFC 9562, §5.3 <9562#section-5.3>`.


.. function:: uuid4()

   Tạo một UUID ngẫu nhiên bằng phương thức bảo mật bằng mật mã theo :rfc:`RFC 9562, §5.4 <9562#section-5.4>`.


.. function:: uuid5(namespace, name)

   Tạo UUID dựa trên hàm băm SHA-1 của một mã định danh namespace (là một UUID) và một tên (là một đối tượng :class:`bytes` hoặc một chuỗi sẽ được mã hóa bằng UTF-8) theo :rfc:`RFC 9562, §5.5 <9562#section-5.5>`.


.. function:: uuid6(node=None, clock_seq=None)

   Tạo UUID từ một số thứ tự và thời gian hiện tại theo
   :rfc:`RFC 9562, §5.6 <9562#section-5.6>`.

   Đây là một giải pháp thay thế cho :func:`uuid1` nhằm cải thiện tính cục bộ của cơ sở dữ liệu.

   Khi *node* không được chỉ định, :func:`getnode` được dùng để lấy địa chỉ phần cứng dưới dạng số nguyên dương 48 bit. Khi số thứ tự *clock_seq* không được chỉ định, một số nguyên dương 14 bit giả ngẫu nhiên sẽ được tạo.

   Nếu *node* hoặc *clock_seq* vượt quá số bit dự kiến, chỉ các bit có trọng số thấp nhất của chúng được giữ lại.

   .. versionadded:: 3.14


.. function:: uuid7()

   Tạo UUID dựa trên thời gian theo
   :rfc:`RFC 9562, §5.7 <9562#section-5.7>`.

   Để đảm bảo khả năng tương thích trên các nền tảng thiếu độ chính xác dưới mili giây, các UUID do hàm này tạo ra nhúng một dấu thời gian 48 bit và sử dụng bộ đếm 42 bit để đảm bảo tính đơn điệu trong phạm vi một mili giây.

   .. versionadded:: 3.14


.. function:: uuid8(a=None, b=None, c=None)

   Tạo UUID giả ngẫu nhiên theo
   :rfc:`RFC 9562, §5.8 <9562#section-5.8>`.

   Khi được chỉ định, các tham số *a*, *b* và *c* được kỳ vọng là các số nguyên dương lần lượt có kích thước 48, 12 và 62 bit. Nếu vượt quá số bit dự kiến, chỉ giữ lại các bit ít quan trọng nhất của chúng; các đối số không được chỉ định sẽ được thay thế bằng một số nguyên giả ngẫu nhiên có kích thước phù hợp.

   Theo mặc định, *a*, *b* và *c* không được tạo bởi bộ sinh số giả ngẫu nhiên an toàn về mặt mật mã (CSPRNG). Hãy sử dụng :func:`uuid4` khi UUID cần được sử dụng trong ngữ cảnh nhạy cảm về bảo mật.

   .. versionadded:: 3.14


Mô-đun :mod:`!uuid` định nghĩa các định danh namespace sau để sử dụng với
:func:`uuid3` hoặc :func:`uuid5`.


.. data:: NAMESPACE_DNS

   Khi namespace này được chỉ định, chuỗi *name* là một tên miền đủ điều kiện (FQDN).


.. data:: NAMESPACE_URL

   Khi namespace này được chỉ định, chuỗi *name* là một URL.


.. data:: NAMESPACE_OID

   Khi namespace này được chỉ định, chuỗi *name* là một ISO OID.


.. data:: NAMESPACE_X500

   Khi namespace này được chỉ định, chuỗi *name* là một DN X.500 ở định dạng DER hoặc định dạng đầu ra văn bản.

Mô-đun :mod:`!uuid` định nghĩa các hằng số sau cho những giá trị có thể có của thuộc tính :attr:`~UUID.variant`:.


.. data:: RESERVED_NCS

   Dành riêng cho khả năng tương thích với NCS.


.. data:: RFC_4122

   Chỉ định bố cục UUID được nêu trong :rfc:`4122`. Hằng số này được giữ lại để tương thích ngược, mặc dù :rfc:`4122` đã được thay thế bởi :rfc:`9562`.


.. data:: RESERVED_MICROSOFT

   Dành riêng cho khả năng tương thích với Microsoft.


.. data:: RESERVED_FUTURE

   Dành riêng cho định nghĩa trong tương lai.


Mô-đun :mod:`!uuid` định nghĩa các giá trị UUID Nil và Max đặc biệt:


.. data:: NIL

   Một dạng UUID đặc biệt được quy định là có toàn bộ 128 bit được đặt thành 0 theo :rfc:`RFC 9562, §5.9 <9562#section-5.9>`.

   .. versionadded:: 3.14


.. data:: MAX

   Một dạng UUID đặc biệt được quy định là có toàn bộ 128 bit được đặt thành 1 theo :rfc:`RFC 9562, §5.10 <9562#section-5.10>`.

   .. versionadded:: 3.14


.. seealso::

   :rfc:`9562` - Không gian tên URN của Mã định danh duy nhất trên toàn cầu (UUID)
      Đặc tả này định nghĩa một không gian tên Uniform Resource Name cho UUID, định dạng nội bộ của UUID và các phương pháp tạo UUID.


.. _uuid-cli:

Cách sử dụng trên dòng lệnh
---------------------------

.. versionadded:: 3.12

Mô-đun :mod:`!uuid` có thể được thực thi dưới dạng script từ dòng lệnh.

.. code-block:: sh

   python -m uuid [-h] [-u {uuid1,uuid3,uuid4,uuid5,uuid6,uuid7,uuid8}] [-n NAMESPACE] [-N NAME]

Các tùy chọn sau được chấp nhận:

.. program:: uuid

.. option:: -h, --help

   Hiển thị thông báo trợ giúp và thoát.

.. option:: -u <uuid>
            --uuid <uuid>

   Chỉ định tên hàm dùng để tạo uuid. Theo mặc định, :func:`uuid4` được sử dụng.

   .. versionchanged:: 3.14
      Cho phép tạo UUID phiên bản 6, 7 và 8.

.. option:: -n <namespace>
            --namespace <namespace>

   Namespace là một ``UUID``, hoặc ``@ns`` trong đó ``ns`` là một UUID được định nghĩa sẵn và xác định bằng tên namespace. Ví dụ: ``@dns``, ``@url``, ``@oid`` và ``@x500``. Chỉ bắt buộc đối với các hàm :func:`uuid3` / :func:`uuid5`.

.. option:: -N <name>
            --name <name>

   Tên được sử dụng trong quá trình tạo uuid. Chỉ bắt buộc đối với
   các hàm :func:`uuid3` / :func:`uuid5`.

.. option:: -C <num>
            --count <num>

   Tạo *num* UUID mới.

   .. versionadded:: 3.14


.. _uuid-example:

Ví dụ
-----

Dưới đây là một số ví dụ về cách sử dụng điển hình của mô-đun :mod:`!uuid`::

   >>> import uuid

   >>> # tạo một UUID dựa trên ID máy chủ và thời gian hiện tại
   >>> uuid.uuid1()  # doctest: +SKIP
   UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')

   >>> # tạo một UUID bằng cách sử dụng mã băm MD5 của UUID namespace và một tên
   >>> uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
   UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')

   >>> # tạo một UUID ngẫu nhiên
   >>> uuid.uuid4()
   UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

   >>> # tạo một UUID bằng cách sử dụng hàm băm SHA-1 của một UUID không gian tên và một tên
   >>> uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
   UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

   >>> # tạo một UUID từ chuỗi chữ số thập lục phân (bỏ qua dấu ngoặc nhọn và dấu gạch nối)
   >>> x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')

   >>> # chuyển đổi một UUID thành chuỗi chữ số thập lục phân ở dạng chuẩn
   >>> str(x)
   '00010203-0405-0607-0809-0a0b0c0d0e0f'

   >>> # lấy 16 byte thô của UUID
   >>> x.bytes
   b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'

   >>> # tạo một UUID từ đối tượng bytes 16 byte
   >>> uuid.UUID(bytes=x.bytes)
   UUID('00010203-0405-0607-0809-0a0b0c0d0e0f')

   >>> # lấy UUID Nil
   >>> uuid.NIL
   UUID('00000000-0000-0000-0000-000000000000')

   >>> # lấy UUID Max
   >>> uuid.MAX
   UUID('ffffffff-ffff-ffff-ffff-ffffffffffff')

   >>> # giống UUIDv1 nhưng các trường được sắp xếp lại để cải thiện tính cục bộ của DB
   >>> uuid.uuid6()  # doctest: +SKIP
   UUID('1f0799c0-98b9-62db-92c6-a0d365b91053')

   >>> # lấy thời gian tạo (cục bộ) của UUIDv7 dưới dạng timestamp tính bằng mili giây
   >>> u = uuid.uuid7()
   >>> u.time  # doctest: +SKIP
   1743936859822

   >>> # lấy thời gian tạo (cục bộ) của UUIDv7 dưới dạng đối tượng datetime
   >>> import datetime as dt
   >>> dt.datetime.fromtimestamp(u.time / 1000)  # doctest: +SKIP
   datetime.datetime(...)

   >>> # tạo UUID với các khối tùy chỉnh
   >>> uuid.uuid8(0x12345678, 0x9abcdef0, 0x11223344)
   UUID('00001234-5678-8ef0-8000-000011223344')


.. _uuid-cli-example:

Ví dụ về dòng lệnh
------------------

Dưới đây là một số ví dụ về cách sử dụng điển hình của giao diện dòng lệnh :mod:`!uuid`:

.. code-block:: shell

   # tạo UUID ngẫu nhiên - theo mặc định, uuid4() được sử dụng
   $ python -m uuid

   # tạo UUID bằng uuid1()
   $ python -m uuid -u uuid1

   # tạo UUID bằng uuid5
   $ python -m uuid -u uuid5 -n @url -N example.com

   # tạo 42 UUID ngẫu nhiên
   $ python -m uuid -C 42
