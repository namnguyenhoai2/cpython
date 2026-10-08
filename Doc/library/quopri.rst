:mod:`!quopri` --- Mã hóa và giải mã dữ liệu MIME quoted-printable
==================================================================

.. module:: quopri
   :synopsis: Mã hóa và giải mã các tệp bằng encoding MIME quoted-printable.

**Mã nguồn:** :source:`Lib/quopri.py`

.. index::
   pair: quoted-printable; encoding
   single: MIME; quoted-printable encoding

--------------

Module này thực hiện việc mã hóa và giải mã truyền tải quoted-printable, như được định nghĩa trong :rfc:`1521`: "MIME (Multipurpose Internet Mail Extensions) Part One: Mechanisms for Specifying and Describing the Format of Internet Message Bodies". Encoding quoted-printable được thiết kế cho dữ liệu có tương đối ít ký tự không in được; scheme encoding base64 có trong
:mod:`base64` module nhỏ gọn hơn nếu có nhiều ký tự như vậy, chẳng hạn khi gửi một tệp đồ họa.

.. function:: decode(input, output, header=False)

   Giải mã nội dung của tệp *input* và ghi dữ liệu nhị phân đã giải mã vào tệp *output*. *input* và *output* phải là :term:`các đối tượng tệp nhị phân <file object>`. Nếu đối số tùy chọn *header* hiện diện và có giá trị true, dấu gạch dưới sẽ được giải mã thành dấu cách. Tùy chọn này được dùng để giải mã các header được mã hóa theo "Q", như mô tả trong :rfc:`1522`: "MIME (Multipurpose Internet Mail Extensions) Part Two: Message Header Extensions for Non-ASCII Text".


.. function:: encode(input, output, quotetabs, header=False)

   Mã hóa nội dung của tệp *input* và ghi dữ liệu quoted-printable thu được vào tệp *output*. *input* và *output* phải là
   :term:`các đối tượng tệp nhị phân <file object>`. *quotetabs*, một cờ bắt buộc, điều khiển việc mã hóa các khoảng trắng và tab được nhúng; khi có giá trị true, cờ này mã hóa các khoảng trắng đó, còn khi có giá trị false, cờ này để chúng ở dạng chưa mã hóa. Lưu ý rằng các khoảng trắng và tab xuất hiện ở cuối dòng luôn được mã hóa, theo :rfc:`1521`.  *header* là một cờ điều khiển việc các khoảng trắng có được mã hóa thành dấu gạch dưới theo :rfc:`1522` hay không.


.. function:: decodestring(s, header=False)

   Tương tự :func:`decode`, ngoại trừ việc hàm này nhận một :class:`bytes` nguồn và trả về :class:`bytes` đã giải mã tương ứng.


.. function:: encodestring(s, quotetabs=False, header=False)

   Tương tự :func:`encode`, ngoại trừ việc hàm này nhận một :class:`bytes` nguồn và trả về :class:`bytes` đã mã hóa tương ứng. Theo mặc định, hàm này truyền giá trị ``False`` cho tham số *quotetabs* của hàm :func:`encode`.



.. seealso::

   Module :mod:`base64`
      Mã hóa và giải mã dữ liệu MIME base64
