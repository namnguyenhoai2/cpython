:mod:`!struct` --- Diễn giải byte dưới dạng dữ liệu nhị phân đóng gói
=====================================================================

.. testsetup:: *

   from struct import *

.. module:: struct
   :synopsis: Diễn giải byte dưới dạng dữ liệu nhị phân đóng gói.

**Mã nguồn:** :source:`Lib/struct.py`

.. index::
   pair: C; structures
   triple: packing; binary; data

--------------

Mô-đun này chuyển đổi giữa các giá trị Python và các cấu trúc C được biểu diễn dưới dạng các đối tượng Python :class:`bytes`. Các :ref:`chuỗi định dạng <struct-format-strings>` ngắn gọn mô tả những chuyển đổi dự kiến sang/từ các giá trị Python. Các hàm và đối tượng của mô-đun có thể được dùng cho hai ứng dụng phần lớn tách biệt: trao đổi dữ liệu với các nguồn bên ngoài (tệp hoặc kết nối mạng), hoặc truyền dữ liệu giữa ứng dụng Python và lớp C.

.. note::

   Khi không cung cấp ký tự tiền tố, chế độ native là mặc định. Mô-đun sẽ đóng gói hoặc giải nén dữ liệu dựa trên nền tảng và trình biên dịch mà trình thông dịch Python được xây dựng trên đó. Kết quả của việc đóng gói một cấu trúc C nhất định bao gồm các byte đệm để duy trì căn chỉnh thích hợp cho các kiểu C liên quan; tương tự, việc căn chỉnh cũng được tính đến khi giải nén. Ngược lại, khi trao đổi dữ liệu giữa các nguồn bên ngoài, lập trình viên chịu trách nhiệm xác định thứ tự byte và phần đệm giữa các phần tử. Xem :ref:`struct-alignment` để biết chi tiết.

Một số :mod:`!struct` hàm (và các phương thức của :class:`Struct`) nhận một đối số *bộ đệm*. Đối số này đề cập đến các đối tượng triển khai :ref:`bufferobjects` và cung cấp bộ đệm chỉ đọc hoặc đọc-ghi. Các kiểu phổ biến nhất được dùng cho mục đích này là :class:`bytes` và :class:`bytearray`, nhưng nhiều kiểu khác có thể được xem như một mảng byte cũng triển khai buffer protocol, nhờ đó chúng có thể được đọc/điền mà không cần sao chép bổ sung từ một đối tượng :class:`bytes`.


Hàm và Ngoại lệ
---------------

Mô-đun định nghĩa exception và các hàm sau:


.. exception:: error

   Exception được raised trong nhiều trường hợp khác nhau; đối số là một chuỗi mô tả vấn đề.


.. function:: pack(format, v1, v2, ...)

   Trả về một đối tượng bytes chứa các giá trị *v1*, *v2*, ... được đóng gói theo chuỗi định dạng *format*. Các đối số phải khớp chính xác với những giá trị mà định dạng yêu cầu.


.. function:: pack_into(format, buffer, offset, v1, v2, ...)

   Đóng gói các giá trị *v1*, *v2*, ... theo chuỗi định dạng *format* và ghi các byte đã đóng gói vào buffer có thể ghi *buffer*, bắt đầu tại vị trí *offset*. Lưu ý rằng *offset* là đối số bắt buộc. *offset* âm sẽ được tính từ cuối *buffer*.


.. function:: unpack(format, buffer)

   Unpack từ buffer *buffer* (có lẽ được đóng gói bởi ``pack(format, ...)``) theo chuỗi định dạng *format*. Kết quả là một tuple, ngay cả khi nó chỉ chứa đúng một phần tử. Kích thước của buffer tính theo byte phải khớp với kích thước mà định dạng yêu cầu, như được thể hiện bởi :func:`calcsize`.


.. function:: unpack_from(format, /, buffer, offset=0)

   Unpack từ *buffer*, bắt đầu tại vị trí *offset*, theo chuỗi định dạng *format*. Kết quả là một tuple, ngay cả khi nó chỉ chứa đúng một phần tử. Kích thước của buffer tính theo byte, bắt đầu từ vị trí *offset*, phải ít nhất bằng kích thước mà định dạng yêu cầu, như được thể hiện bởi :func:`calcsize`. *offset* âm sẽ được tính từ cuối *buffer*.


.. function:: iter_unpack(format, buffer)

   Unpack lặp đi lặp lại từ buffer *buffer* theo chuỗi định dạng *format*. Hàm này trả về một iterator, iterator này sẽ đọc các phần có kích thước bằng nhau từ buffer cho đến khi toàn bộ nội dung được đọc hết. Kích thước của buffer tính theo byte phải là bội số của kích thước mà định dạng yêu cầu, như được thể hiện bởi :func:`calcsize`.

   Mỗi lần lặp trả về một tuple như được chỉ định bởi chuỗi định dạng.

   .. versionadded:: 3.4


.. function:: calcsize(format)

   Trả về kích thước của struct (và do đó là kích thước của đối tượng bytes được tạo bởi ``pack(format, ...)``) tương ứng với chuỗi định dạng *định dạng*.


.. _struct-format-strings:

Chuỗi định dạng
---------------

Chuỗi định dạng mô tả bố cục dữ liệu khi đóng gói và giải nén dữ liệu. Chúng được tạo thành từ :ref:`các ký tự định dạng <format-characters>`, dùng để chỉ định kiểu dữ liệu đang được đóng gói/giải nén. Ngoài ra, các ký tự đặc biệt kiểm soát :ref:`thứ tự byte, kích thước và căn chỉnh <struct-alignment>`. Mỗi chuỗi định dạng gồm một ký tự tiền tố tùy chọn mô tả các thuộc tính tổng thể của dữ liệu và một hoặc nhiều ký tự định dạng mô tả các giá trị dữ liệu thực tế cùng phần đệm.


.. _struct-alignment:

Thứ tự byte, kích thước và căn chỉnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Theo mặc định, các kiểu C được biểu diễn theo định dạng và thứ tự byte gốc của máy, đồng thời được căn chỉnh thích hợp bằng cách bỏ qua các byte đệm nếu cần (theo các quy tắc mà trình biên dịch C sử dụng). Hành vi này được chọn để các byte của một struct đã đóng gói tương ứng chính xác với bố cục bộ nhớ của struct C tương ứng. Việc sử dụng thứ tự byte và phần đệm gốc hay các định dạng chuẩn phụ thuộc vào ứng dụng.

.. index::
   single: @ (at); in struct format strings
   single: = (equals); in struct format strings
   single: < (less); in struct format strings
   single: > (greater); in struct format strings
   single: ! (exclamation); in struct format strings

Ngoài ra, ký tự đầu tiên của chuỗi định dạng có thể được dùng để chỉ báo thứ tự byte, kích thước và căn chỉnh của dữ liệu đã đóng gói, theo bảng sau:

+-------+------------------------+------------+-----------+
| Ký tự | Thứ tự byte            | Kích thước | Căn chỉnh |
+=======+========================+============+===========+
| ``@`` | native                 | native     | native    |
+-------+------------------------+------------+-----------+
| ``=`` | gốc                    | tiêu chuẩn | không có  |
+-------+------------------------+------------+-----------+
| ``<`` | little-endian          | tiêu chuẩn | không có  |
+-------+------------------------+------------+-----------+
| ``>`` | big-endian             | tiêu chuẩn | không có  |
+-------+------------------------+------------+-----------+
| ``!`` | network (= big-endian) | tiêu chuẩn | không có  |
+-------+------------------------+------------+-----------+

Nếu ký tự đầu tiên không phải là một trong các ký tự này, ``'@'`` được giả định.

.. note::

   Số 1023 (``0x3ff`` ở dạng thập lục phân) có các biểu diễn byte sau đây:

   * ``03 ff`` theo thứ tự byte big-endian (``>``)
   * ``ff 03`` theo thứ tự byte little-endian (``<``)

   Ví dụ Python:

       >>> import struct
       >>> struct.pack('>h', 1023)
       b'\x03\xff'
       >>> struct.pack('<h', 1023)
       b'\xff\x03'

Thứ tự byte native là big-endian hoặc little-endian, tùy thuộc vào hệ thống máy chủ. Ví dụ, Intel x86, AMD64 (x86-64) và Apple M1 sử dụng little-endian; IBM z và nhiều kiến trúc cũ sử dụng big-endian. Sử dụng :data:`sys.byteorder` để kiểm tra thứ tự byte của hệ thống.

Kích thước và alignment native được xác định bằng biểu thức ``sizeof`` của trình biên dịch C. Điều này luôn được kết hợp với thứ tự byte native.

Kích thước chuẩn chỉ phụ thuộc vào ký tự định dạng; xem bảng trong phần :ref:`format-characters`.

Lưu ý sự khác biệt giữa ``'@'`` và ``'='``: cả hai đều sử dụng thứ tự byte native, nhưng kích thước và alignment của thành phần sau được chuẩn hóa.

Dạng ``'!'`` biểu thị thứ tự byte mạng, luôn là big-endian như được định nghĩa trong `IETF RFC 1700 <IETF RFC 1700_>`_.

Không có cách nào để chỉ định thứ tự byte không phải native (bắt buộc hoán đổi byte); hãy sử dụng lựa chọn thích hợp là ``'<'`` hoặc ``'>'``.

Lưu ý:

(1) Padding chỉ được tự động thêm vào giữa các thành viên cấu trúc kế tiếp nhau. Không có padding nào được thêm vào đầu hoặc cuối struct đã mã hóa.

(2) Không có padding nào được thêm khi sử dụng kích thước và căn chỉnh không phải native, chẳng hạn với '<', '>', '=', và '!'.

(3) Để căn chỉnh phần cuối của một cấu trúc theo yêu cầu căn chỉnh của một kiểu cụ thể, hãy kết thúc format bằng mã của kiểu đó với số lần lặp bằng không. Xem :ref:`struct-examples`.


.. _format-characters:

Ký tự định dạng
^^^^^^^^^^^^^^^

Các ký tự định dạng có ý nghĩa như sau; việc chuyển đổi giữa các giá trị C và Python sẽ trở nên rõ ràng dựa trên kiểu của chúng. Cột 'Standard size' chỉ kích thước tính bằng byte của giá trị đã đóng gói khi sử dụng kích thước chuẩn; tức là khi chuỗi định dạng bắt đầu bằng một trong ``'<'``, ``'>'``, ``'!'`` hoặc ``'='``. Khi sử dụng kích thước native, kích thước của giá trị đã đóng gói phụ thuộc vào nền tảng.

+--------+--------------------------+--------------------+----------------+------------+
| Format | C Type                   | Python type        | Standard size  | Notes      |
+========+==========================+====================+================+============+
| ``x``  | pad byte                 | no value           |                | \(7)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``c``  | :c:expr:`char`           | bytes of length 1  | 1              |            |
+--------+--------------------------+--------------------+----------------+------------+
| ``b``  | :c:expr:`signed char`    | int                | 1              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``B``  | :c:expr:`unsigned char`  | int                | 1              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``?``  | :c:expr:`_Bool`          | bool               | 1              | \(1)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``h``  | :c:expr:`short`          | int                | 2              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``H``  | :c:expr:`unsigned short` | int                | 2              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``i``  | :c:expr:`int`            | int                | 4              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``I``  | :c:expr:`unsigned int`   | int                | 4              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``l``  | :c:expr:`long`           | int                | 4              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``L``  | :c:expr:`unsigned long`  | int                | 4              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``q``  | :c:expr:`long long`      | int                | 8              | \(2)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``Q``  | :c:expr:`unsigned long   | int                | 8              | \(2)       |
|        | long`                    |                    |                |            |
+--------+--------------------------+--------------------+----------------+------------+
| ``n``  | :c:type:`ssize_t`        | int                |                | \(2), \(3) |
+--------+--------------------------+--------------------+----------------+------------+
| ``N``  | :c:type:`size_t`         | int                |                | \(2), \(3) |
+--------+--------------------------+--------------------+----------------+------------+
| ``e``  | :c:expr:`_Float16`       | float              | 2              | \(4), \(6) |
+--------+--------------------------+--------------------+----------------+------------+
| ``f``  | :c:expr:`float`          | float              | 4              | \(4)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``d``  | :c:expr:`double`         | float              | 8              | \(4)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``F``  | :c:expr:`float complex`  | complex            | 8              | \(10)      |
+--------+--------------------------+--------------------+----------------+------------+
| ``D``  | :c:expr:`double complex` | complex            | 16             | \(10)      |
+--------+--------------------------+--------------------+----------------+------------+
| ``s``  | :c:expr:`char[]`         | bytes              |                | \(9)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``p``  | :c:expr:`char[]`         | bytes              |                | \(8)       |
+--------+--------------------------+--------------------+----------------+------------+
| ``P``  | :c:expr:`void \*`        | int                |                | \(2), \(5) |
+--------+--------------------------+--------------------+----------------+------------+

.. versionchanged:: 3.3
   Đã bổ sung hỗ trợ cho các định dạng ``'n'`` và ``'N'``.

.. versionchanged:: 3.6
   Đã bổ sung hỗ trợ cho định dạng ``'e'``.

.. versionchanged:: 3.14
   Đã bổ sung hỗ trợ cho các định dạng ``'F'`` và ``'D'``.

.. seealso::

   Các module :mod:`array` và :ref:`ctypes <ctypes-fundamental-data-types>`, cũng như các module bên thứ ba như `numpy <https://numpy.org/doc/stable/reference/arrays.interface.html#object.__array_interface__>`__, sử dụng các mã kiểu tương tự -- nhưng hơi khác nhau --.


Lưu ý:

(1)
   .. index:: single: ? (question mark); in struct format strings

   Mã chuyển đổi ``'?'`` tương ứng với kiểu :c:expr:`_Bool` được định nghĩa trong các tiêu chuẩn C kể từ C99.  Ở chế độ chuẩn, mã này được biểu diễn bằng một byte.

(2)
   Khi cố gắng đóng gói một giá trị không phải số nguyên bằng bất kỳ mã chuyển đổi số nguyên nào, nếu giá trị đó có phương thức :meth:`~object.__index__` thì phương thức này sẽ được gọi để chuyển đối số thành số nguyên trước khi đóng gói.

   .. versionchanged:: 3.2
      Đã bổ sung việc sử dụng phương thức :meth:`~object.__index__` cho các giá trị không phải số nguyên.

(3)
   Các mã chuyển đổi ``'n'`` và ``'N'`` chỉ khả dụng cho kích thước native (được chọn theo mặc định hoặc bằng ký tự thứ tự byte ``'@'``). Đối với kích thước chuẩn, bạn có thể sử dụng bất kỳ định dạng số nguyên nào khác phù hợp với ứng dụng của mình.

(4)
   Đối với các mã chuyển đổi ``'f'``, ``'d'`` và ``'e'``, biểu diễn được đóng gói sử dụng định dạng IEEE 754 binary32, binary64 hoặc binary16 (tương ứng với ``'f'``, ``'d'`` hoặc ``'e'``), bất kể định dạng dấu phẩy động được nền tảng sử dụng.

(5)
   Ký tự định dạng ``'P'`` chỉ khả dụng cho thứ tự byte native (được chọn theo mặc định hoặc bằng ký tự thứ tự byte ``'@'``). Ký tự thứ tự byte ``'='`` chọn thứ tự little-endian hoặc big-endian dựa trên hệ thống máy chủ. Mô-đun struct không diễn giải đây là thứ tự native, vì vậy định dạng ``'P'`` không khả dụng.

(6)
   Kiểu "độ chính xác nửa" binary16 của IEEE 754 được giới thiệu trong bản sửa đổi năm 2008 của tiêu chuẩn `IEEE 754 standard <ieee 754 standard_>`_. Kiểu này có một bit dấu, một số mũ 5 bit và độ chính xác 11 bit (trong đó 10 bit được lưu trữ rõ ràng), đồng thời có thể biểu diễn các số trong khoảng từ xấp xỉ ``6.1e-05`` đến ``6.5e+04`` với đầy đủ độ chính xác. Kiểu này không được các trình biên dịch C hỗ trợ rộng rãi: nó khả dụng dưới dạng kiểu :c:expr:`_Float16`, nếu trình biên dịch hỗ trợ Annex H của tiêu chuẩn C23. Trên một máy tính thông thường, có thể sử dụng unsigned short để lưu trữ, nhưng không thể dùng cho các phép toán. Xem trang Wikipedia về `half-precision floating-point format <half precision format_>`_ để biết thêm thông tin.

(7)
   Khi đóng gói, ``'x'`` chèn một byte NUL.

(8)
   Ký tự định dạng ``'p'`` mã hóa một "Pascal string", nghĩa là một chuỗi có độ dài biến đổi ngắn được lưu trữ trong *số byte cố định*, được xác định bởi count. Byte đầu tiên được lưu trữ là độ dài của chuỗi hoặc 255, tùy giá trị nào nhỏ hơn. Các byte của chuỗi được lưu tiếp theo. Nếu byte string được truyền vào
   :func:`pack` quá dài (dài hơn count trừ 1), chỉ các byte đầu tiên ``count-1`` của chuỗi được lưu trữ. Nếu byte string ngắn hơn ``count-1``, nó được đệm bằng các byte null để tổng cộng sử dụng đúng count byte. Lưu ý rằng đối với :func:`unpack`, ký tự định dạng ``'p'`` sử dụng ``count`` byte, nhưng đối tượng :class:`!bytes` được trả về không bao giờ có thể chứa quá 255 byte. Khi packing, chấp nhận các đối số có kiểu :class:`bytes` và :class:`bytearray`.

(9)
   Đối với ký tự định dạng ``'s'``, count được hiểu là độ dài của byte string, không phải số lần lặp như đối với các ký tự định dạng khác; ví dụ, ``'10s'`` biểu thị một chuỗi duy nhất dài 10 byte ánh xạ tới hoặc từ một Python byte string duy nhất, trong khi ``'10c'`` biểu thị 10 phần tử ký tự, mỗi phần tử dài một byte (ví dụ: ``cccccccccc``), ánh xạ tới hoặc từ mười Python byte object khác nhau. (Xem :ref:`struct-examples` để biết minh họa cụ thể về sự khác biệt này.) Nếu không cung cấp count, giá trị mặc định là 1. Khi packing, byte string được cắt ngắn hoặc đệm bằng các byte null nếu thích hợp để vừa với kích thước yêu cầu. Khi unpacking, đối tượng :class:`!bytes` kết quả luôn có đúng số byte được chỉ định. Trường hợp đặc biệt, ``'0s'`` biểu thị một byte string rỗng duy nhất (trong khi ``'0c'`` biểu thị 0 ký tự). Khi packing, chấp nhận các đối số có kiểu :class:`bytes` và :class:`bytearray`.

(10)
   Đối với các ký tự định dạng ``'F'`` và ``'D'``, biểu diễn đã pack sử dụng định dạng IEEE 754 binary32 và binary64 cho các thành phần của số phức, bất kể định dạng dấu phẩy động được nền tảng sử dụng. Lưu ý rằng các kiểu phức (``F`` và ``D``) luôn khả dụng, mặc dù kiểu phức là một tính năng tùy chọn trong C. Theo quy định của tiêu chuẩn C11, mỗi kiểu phức được biểu diễn bằng một mảng C gồm hai phần tử, lần lượt chứa phần thực và phần ảo.


Một ký tự định dạng có thể được đặt trước bởi một count lặp dạng số nguyên. Ví dụ, chuỗi định dạng ``'4h'`` hoàn toàn tương đương với ``'hhhh'``.

Các ký tự khoảng trắng giữa các định dạng sẽ bị bỏ qua; tuy nhiên, count và định dạng tương ứng không được chứa khoảng trắng.

Khi packing một giá trị ``x`` bằng một trong các định dạng số nguyên (``'b'``, ``'B'``, ``'h'``, ``'H'``, ``'i'``, ``'I'``, ``'l'``, ``'L'``, ``'q'``, ``'Q'``), nếu ``x`` nằm ngoài phạm vi hợp lệ của định dạng đó thì :exc:`struct.error` sẽ được raise.

.. versionchanged:: 3.1
   Trước đây, một số định dạng số nguyên đã chuyển vòng các giá trị nằm ngoài phạm vi và phát sinh :exc:`DeprecationWarning` thay vì :exc:`struct.error`.

.. index:: single: ? (question mark); in struct format strings

Đối với ký tự định dạng ``'?'``, giá trị trả về là :const:`True` hoặc
:const:`False`. Khi đóng gói, giá trị đúng/sai của đối tượng đối số được sử dụng. Giá trị 0 hoặc 1 ở dạng bool native hoặc standard sẽ được đóng gói, còn mọi giá trị khác 0 sẽ là ``True`` khi giải nén.



.. _struct-examples:

Ví dụ
^^^^^

.. note::
   Các ví dụ về thứ tự byte native (được chỉ định bằng tiền tố định dạng ``'@'`` hoặc không có ký tự tiền tố nào) có thể không khớp với kết quả do máy của người đọc tạo ra, vì điều đó phụ thuộc vào nền tảng và trình biên dịch.

Đóng gói và giải nén các số nguyên có ba kích thước khác nhau, sử dụng thứ tự big endian::

    >>> from struct import *
    >>> pack(">bhl", 1, 2, 3)
    b'\x01\x00\x02\x00\x00\x00\x03'
    >>> unpack('>bhl', b'\x01\x00\x02\x00\x00\x00\x03')
    (1, 2, 3)
    >>> calcsize('>bhl')
    7

Thử đóng gói một số nguyên quá lớn so với trường đã định nghĩa::

    >>> pack(">h", 99999)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    struct.error: 'h' format requires -32768 <= number <= 32767

Minh họa sự khác biệt giữa các ký tự định dạng ``'s'`` và ``'c'``::

    >>> pack("@ccc", b'1', b'2', b'3')
    b'123'
    >>> pack("@3s", b'123')
    b'123'

Các trường đã unpack có thể được đặt tên bằng cách gán chúng cho các biến hoặc bằng cách bọc kết quả trong một named tuple::

    >>> record = b'raymond   \x32\x12\x08\x01\x08'
    >>> name, serialnum, school, gradelevel = unpack('<10sHHb', record)

    >>> from collections import namedtuple
    >>> Student = namedtuple('Student', 'name serialnum school gradelevel')
    >>> Student._make(unpack('<10sHHb', record))
    Student(name=b'raymond   ', serialnum=4658, school=264, gradelevel=8)

Thứ tự của các ký tự định dạng có thể ảnh hưởng đến kích thước trong native mode vì phần đệm được thêm ngầm. Trong standard mode, người dùng chịu trách nhiệm chèn phần đệm mong muốn. Lưu ý trong lệnh gọi ``pack`` đầu tiên bên dưới rằng ba byte NUL đã được thêm sau ``'#'`` đã đóng gói để căn chỉnh số nguyên tiếp theo theo ranh giới bốn byte. Trong ví dụ này, đầu ra được tạo trên một máy little endian::

    >>> pack('@ci', b'#', 0x12131415)
    b'#\x00\x00\x00\x15\x14\x13\x12'
    >>> pack('@ic', 0x12131415, b'#')
    b'\x15\x14\x13\x12#'
    >>> calcsize('@ci')
    8
    >>> calcsize('@ic')
    5

Định dạng sau đây ``'llh0l'`` dẫn đến việc thêm hai byte đệm ở cuối, với giả định rằng các long của nền tảng được căn chỉnh theo ranh giới 4 byte::

    >>> pack('@llh0l', 1, 2, 3)
    b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x03\x00\x00'


.. seealso::

   Mô-đun :mod:`array`
      Lưu trữ nhị phân được đóng gói của dữ liệu đồng nhất.

   Mô-đun :mod:`json`
      Bộ mã hóa và giải mã JSON.

   Mô-đun :mod:`pickle`
      Tuần tự hóa đối tượng Python.


.. _applications:

Ứng dụng
--------

Mô-đun :mod:`!struct` có hai ứng dụng chính: trao đổi dữ liệu giữa mã Python và mã C trong một ứng dụng hoặc một ứng dụng khác được biên dịch bằng cùng một trình biên dịch (:ref:`định dạng gốc <struct-native-formats>`), và trao đổi dữ liệu giữa các ứng dụng sử dụng bố cục dữ liệu đã thống nhất (:ref:`định dạng tiêu chuẩn <struct-standard-formats>`). Nói chung, các chuỗi định dạng được xây dựng cho hai miền này là khác nhau.


.. _struct-native-formats:

Định dạng gốc
^^^^^^^^^^^^^

Khi xây dựng các chuỗi định dạng mô phỏng bố cục gốc, trình biên dịch và kiến trúc máy sẽ xác định thứ tự byte và phần đệm. Trong những trường hợp như vậy, nên sử dụng ký tự định dạng ``@`` để chỉ định thứ tự byte và kích thước dữ liệu gốc. Các byte đệm bên trong thường được tự động chèn vào. Có thể cần một mã định dạng lặp bằng không ở cuối chuỗi định dạng để làm tròn đến đúng ranh giới byte, nhằm căn chỉnh chính xác các khối dữ liệu liên tiếp.

Hãy xem xét hai ví dụ đơn giản sau (trên một máy 64-bit, little-endian)::

    >>> calcsize('@lhl')
    24
    >>> calcsize('@llh')
    18

Dữ liệu không được đệm đến ranh giới 8 byte ở cuối chuỗi định dạng thứ hai nếu không sử dụng phần đệm bổ sung. Mã định dạng lặp bằng 0 giải quyết vấn đề đó::

    >>> calcsize('@llh0l')
    24

Có thể sử dụng mã định dạng ``'x'`` để chỉ định số lần lặp, nhưng đối với các định dạng native, tốt hơn nên sử dụng một định dạng lặp bằng 0 như ``'0l'``.

Theo mặc định, thứ tự byte và alignment native được sử dụng, nhưng tốt hơn nên chỉ rõ và sử dụng ký tự tiền tố ``'@'``.


.. _struct-standard-formats:

Các định dạng tiêu chuẩn
^^^^^^^^^^^^^^^^^^^^^^^^

Khi trao đổi dữ liệu bên ngoài process của bạn, chẳng hạn như qua mạng hoặc bộ nhớ lưu trữ, hãy chỉ rõ chính xác. Hãy chỉ định thứ tự byte, kích thước và alignment chính xác. Đừng giả định rằng chúng trùng với thứ tự native của một máy cụ thể. Ví dụ, thứ tự byte mạng là big-endian, trong khi nhiều CPU phổ biến là little-endian. Bằng cách định nghĩa rõ ràng điều này, người dùng không cần quan tâm đến các đặc điểm cụ thể của nền tảng mà mã của họ đang chạy trên đó. Ký tự đầu tiên thường nên là ``<`` hoặc ``>`` (hoặc ``!``). Việc đệm là trách nhiệm của lập trình viên. Ký tự định dạng lặp bằng 0 sẽ không hoạt động. Thay vào đó, người dùng phải thêm rõ ràng ``'x'`` byte đệm khi cần. Xem lại các ví dụ trong phần trước, ta có::

    >>> calcsize('<qh6xq')
    24
    >>> pack('<qh6xq', 1, 2, 3) == pack('@lhl', 1, 2, 3)
    True
    >>> calcsize('@llh')
    18
    >>> pack('@llh', 1, 2, 3) == pack('<qqh', 1, 2, 3)
    True
    >>> calcsize('<qqh6x')
    24
    >>> calcsize('@llh0l')
    24
    >>> pack('@llh0l', 1, 2, 3) == pack('<qqh6x', 1, 2, 3)
    True

Các kết quả trên (được thực thi trên một máy 64-bit) không được đảm bảo sẽ giống nhau khi thực thi trên các máy khác. Ví dụ, các ví dụ dưới đây được thực thi trên một máy 32-bit::

    >>> calcsize('<qqh6x')
    24
    >>> calcsize('@llh0l')
    12
    >>> pack('@llh0l', 1, 2, 3) == pack('<qqh6x', 1, 2, 3)
    False


.. _struct-objects:

Các lớp
-------

Mô-đun :mod:`!struct` cũng định nghĩa kiểu sau:


.. class:: Struct(format)

   Trả về một đối tượng Struct mới, dùng để ghi và đọc dữ liệu nhị phân theo chuỗi định dạng *format*. Việc tạo một đối tượng ``Struct`` một lần rồi gọi các phương thức của đối tượng đó sẽ hiệu quả hơn việc gọi các hàm cấp mô-đun với cùng định dạng, vì chuỗi định dạng chỉ được biên dịch một lần.

   .. note::

      Các phiên bản đã biên dịch của những chuỗi định dạng gần đây nhất được truyền cho các hàm cấp mô-đun sẽ được lưu vào bộ nhớ đệm, vì vậy các chương trình chỉ sử dụng một vài chuỗi định dạng không cần phải lo lắng về việc tái sử dụng một thực thể :class:`Struct` duy nhất.

   Các đối tượng Struct đã biên dịch hỗ trợ những phương thức và thuộc tính sau:

   .. method:: pack(v1, v2, ...)

      Tương tự hàm :func:`pack`, sử dụng định dạng đã biên dịch. (``len(result)`` sẽ bằng :attr:`size`.)


   .. method:: pack_into(buffer, offset, v1, v2, ...)

      Tương tự hàm :func:`pack_into`, sử dụng định dạng đã biên dịch.


   .. method:: unpack(buffer)

      Giống hệt hàm :func:`unpack`, sử dụng định dạng đã biên dịch. Kích thước của buffer tính theo byte phải bằng :attr:`size`.


   .. method:: unpack_from(buffer, offset=0)

      Giống hệt hàm :func:`unpack_from`, sử dụng định dạng đã biên dịch. Kích thước của buffer tính theo byte, bắt đầu từ vị trí *offset*, phải ít nhất là
      :attr:`size`.


   .. method:: iter_unpack(buffer)

      Giống hệt hàm :func:`iter_unpack`, sử dụng định dạng đã biên dịch. Kích thước của buffer tính theo byte phải là bội số của :attr:`size`.

      .. versionadded:: 3.4

   .. attribute:: format

      Chuỗi định dạng được sử dụng để tạo đối tượng Struct này.

      .. versionchanged:: 3.7
         Kiểu chuỗi định dạng hiện là :class:`str` thay vì :class:`bytes`.

   .. attribute:: size

      Kích thước được tính toán của struct (và do đó là của đối tượng bytes được tạo bởi phương thức :meth:`pack`) tương ứng với :attr:`format`.

   .. versionchanged:: 3.13 *repr()* của các struct đã thay đổi. Nó
      hiện là:

         >>> Struct('i')
         Struct('i')

.. _half precision format: https://en.wikipedia.org/wiki/Half-precision_floating-point_format

.. _ieee 754 standard: https://en.wikipedia.org/wiki/IEEE_754-2008_revision

.. _IETF RFC 1700: https://datatracker.ietf.org/doc/html/rfc1700

.. _`half-precision floating-point format`: half precision format_
