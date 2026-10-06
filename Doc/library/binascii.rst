:mod:`!binascii` --- Chuyển đổi giữa nhị phân và ASCII
======================================================

.. module:: binascii
   :synopsis: Các công cụ để chuyển đổi giữa dữ liệu nhị phân và nhiều dạng biểu diễn nhị phân được mã hóa bằng ASCII.

.. index::
   pair: module; base64

--------------

Mô-đun :mod:`!binascii` chứa một số phương thức để chuyển đổi giữa dữ liệu nhị phân và nhiều dạng biểu diễn nhị phân được mã hóa bằng ASCII. Thông thường, bạn sẽ không sử dụng trực tiếp các hàm này mà sử dụng các mô-đun wrapper như
:mod:`base64` thay vào đó. Mô-đun :mod:`!binascii` chứa các hàm cấp thấp được viết bằng C để có tốc độ cao hơn và được các mô-đun cấp cao hơn sử dụng.

.. note::

   Các hàm ``a2b_*`` chấp nhận các chuỗi Unicode chỉ chứa ký tự ASCII. Các hàm khác chỉ chấp nhận các :term:`bytes-like objects <bytes-like object>` (chẳng hạn như
   :class:`bytes`, :class:`bytearray` và các đối tượng khác hỗ trợ buffer protocol).

   .. versionchanged:: 3.3
      Các chuỗi unicode chỉ chứa ASCII hiện được các hàm ``a2b_*`` chấp nhận.


Mô-đun :mod:`!binascii` định nghĩa các hàm sau:


.. function:: a2b_uu(string)

   Chuyển đổi một dòng dữ liệu uuencoded về dạng nhị phân và trả về dữ liệu nhị phân. Các dòng thường chứa 45 byte (nhị phân), ngoại trừ dòng cuối cùng. Dữ liệu trên dòng có thể được theo sau bởi khoảng trắng.


.. function:: b2a_uu(data, *, backtick=False)

   Chuyển đổi dữ liệu nhị phân thành một dòng ký tự ASCII; giá trị trả về là dòng đã chuyển đổi, bao gồm cả ký tự xuống dòng. Độ dài của *data* tối đa là
   45. Nếu *backtick* là true, các số 0 sẽ được biểu diễn bằng ``'`'`` thay vì khoảng trắng.

   .. versionchanged:: 3.7
      Đã thêm tham số *backtick*.


.. function:: a2b_base64(string, /, *, strict_mode=False)

   Chuyển đổi một khối dữ liệu base64 về dạng nhị phân và trả về dữ liệu nhị phân. Có thể truyền vào nhiều dòng cùng một lúc.

   Nếu *strict_mode* là true, chỉ dữ liệu base64 hợp lệ mới được chuyển đổi. Dữ liệu base64 không hợp lệ sẽ gây ra :exc:`binascii.Error`.

   base64 hợp lệ:

   * Tuân theo :rfc:`3548`.
   * Chỉ chứa các ký tự trong bảng chữ cái base64.
   * Không chứa dữ liệu thừa sau phần đệm (bao gồm phần đệm thừa, ký tự xuống dòng, v.v.).
   * Không bắt đầu bằng phần đệm.

   .. versionchanged:: 3.11
      Đã thêm tham số *strict_mode*.


.. function:: b2a_base64(data, *, newline=True)

   Chuyển đổi dữ liệu nhị phân thành một dòng ký tự ASCII theo mã hóa base64. Giá trị trả về là dòng đã chuyển đổi, bao gồm một ký tự xuống dòng nếu *newline* là true. Đầu ra của hàm này tuân theo :rfc:`3548`.

   .. versionchanged:: 3.6
      Đã thêm tham số *newline*.


.. function:: a2b_qp(data, header=False)

   Chuyển một khối dữ liệu quoted-printable đã được trích dẫn trở lại dạng binary và trả về dữ liệu binary. Có thể truyền nhiều dòng cùng một lúc. Nếu đối số tùy chọn *header* được cung cấp và có giá trị true, dấu gạch dưới sẽ được giải mã thành khoảng trắng.


.. function:: b2a_qp(data, quotetabs=False, istext=True, header=False)

   Chuyển dữ liệu binary thành một hoặc nhiều dòng ký tự ASCII ở dạng mã hóa quoted-printable. Giá trị trả về là các dòng đã được chuyển đổi. Nếu đối số tùy chọn *quotetabs* được cung cấp và có giá trị true, tất cả tab và khoảng trắng sẽ được mã hóa. Nếu đối số tùy chọn *istext* được cung cấp và có giá trị true, ký tự xuống dòng sẽ không được mã hóa, nhưng khoảng trắng ở cuối dòng sẽ được mã hóa. Nếu đối số tùy chọn *header* được cung cấp và có giá trị true, khoảng trắng sẽ được mã hóa thành dấu gạch dưới theo :rfc:`1522`. Nếu đối số tùy chọn *header* được cung cấp và có giá trị false, các ký tự xuống dòng cũng sẽ được mã hóa; nếu không, việc chuyển đổi linefeed có thể làm hỏng luồng dữ liệu binary.


.. function:: crc_hqx(data, value)

   Tính giá trị CRC 16-bit của *data*, bắt đầu với *value* làm CRC ban đầu, rồi trả về kết quả. Giá trị này sử dụng đa thức CRC-CCITT *x*:sup:`16` + *x*:sup:`12` + *x*:sup:`5` + 1, thường được biểu diễn là 0x1021. CRC này được sử dụng trong định dạng binhex4.


.. function:: crc32(data[, value])

   Tính CRC-32, checksum 32-bit không dấu của *data*, bắt đầu với CRC ban đầu là *value*. CRC ban đầu mặc định là 0. Thuật toán này nhất quán với checksum của tệp ZIP. Vì thuật toán được thiết kế để sử dụng làm thuật toán checksum, nó không phù hợp để sử dụng làm thuật toán hash tổng quát. Sử dụng như sau::

      print(binascii.crc32(b"hello world"))
      # Hoặc, chia thành hai phần:
      crc = binascii.crc32(b"hello")
      crc = binascii.crc32(b" world", crc)
      print('crc32 = {:#010x}'.format(crc))

   .. versionchanged:: 3.0
      Kết quả luôn là số không dấu.

.. function:: b2a_hex(data[, sep[, bytes_per_sep=1]])
              hexlify(data[, sep[, bytes_per_sep=1]])

   Trả về biểu diễn hệ thập lục phân của dữ liệu nhị phân *data*. Mỗi byte của *data* được chuyển đổi thành biểu diễn hệ thập lục phân gồm 2 chữ số tương ứng. Do đó, đối tượng bytes được trả về có độ dài gấp đôi độ dài của *data*.

   Bạn cũng có thể dễ dàng truy cập chức năng tương tự (nhưng trả về chuỗi văn bản) bằng phương thức :meth:`bytes.hex`.

   Nếu chỉ định *sep*, giá trị này phải là một đối tượng str hoặc bytes gồm một ký tự duy nhất. Giá trị này sẽ được chèn vào kết quả sau mỗi *bytes_per_sep* byte đầu vào. Theo mặc định, vị trí của dấu phân cách được tính từ cuối bên phải của kết quả; nếu muốn tính từ bên trái, hãy cung cấp giá trị *bytes_per_sep* âm.

      >>> import binascii
      >>> binascii.b2a_hex(b'\xb9\x01\xef')
      b'b901ef'
      >>> binascii.hexlify(b'\xb9\x01\xef', '-')
      b'b9-01-ef'
      >>> binascii.b2a_hex(b'\xb9\x01\xef', b'_', 2)
      b'b9_01ef'
      >>> binascii.b2a_hex(b'\xb9\x01\xef', b' ', -2)
      b'b901 ef'

   .. versionchanged:: 3.8
      Các tham số *sep* và *bytes_per_sep* đã được thêm vào.

.. function:: a2b_hex(hexstr)
              unhexlify(hexstr)

   Trả về dữ liệu nhị phân được biểu diễn bởi chuỗi hệ thập lục phân *hexstr*. Hàm này là phép đảo của :func:`b2a_hex`. *hexstr* phải chứa số chữ số hệ thập lục phân chẵn (có thể viết hoa hoặc viết thường), nếu không thì một
   Ngoại lệ :exc:`Error` được nâng lên.

   Chức năng tương tự (nhưng linh hoạt hơn đối với khoảng trắng) cũng có thể được truy cập bằng phương thức lớp :meth:`bytes.fromhex`.

.. exception:: Error

   Ngoại lệ được nâng lên khi xảy ra lỗi. Đây thường là các lỗi lập trình.


.. exception:: Incomplete

   Ngoại lệ được nâng lên khi dữ liệu chưa hoàn chỉnh. Đây thường không phải là lỗi lập trình, nhưng có thể được xử lý bằng cách đọc thêm một ít dữ liệu rồi thử lại.


.. seealso::

   Mô-đun :mod:`base64`
      Hỗ trợ mã hóa kiểu base64 tuân thủ RFC ở cơ số 16, 32, 64 và 85.

   Mô-đun :mod:`quopri`
      Hỗ trợ mã hóa quoted-printable được sử dụng trong các thư email MIME.
