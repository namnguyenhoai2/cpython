:mod:`!email.charset`: Biểu diễn các bộ ký tự
---------------------------------------------

.. module:: email.charset
   :synopsis: Bộ ký tự

**Mã nguồn:** :source:`Lib/email/charset.py`

--------------

Mô-đun này là một phần của API email cũ (``Compat32``). Trong API mới, chỉ có bảng bí danh được sử dụng.

Phần văn bản còn lại trong mục này là tài liệu gốc của mô-đun.

Mô-đun này cung cấp một lớp :class:`Charset` để biểu diễn các bộ ký tự và việc chuyển đổi bộ ký tự trong các thông điệp email, cùng với một registry bộ ký tự và một số phương thức tiện ích để thao tác với registry này. Các thực thể của :class:`Charset` được sử dụng trong một số mô-đun khác thuộc
:mod:`email`.

Import lớp này từ mô-đun :mod:`!email.charset`.


.. class:: Charset(input_charset=DEFAULT_CHARSET)

   Ánh xạ các bộ ký tự với các thuộc tính email của chúng.

   Lớp này cung cấp thông tin về các yêu cầu áp dụng cho email đối với một bộ ký tự cụ thể. Lớp cũng cung cấp các routine tiện ích để chuyển đổi giữa các bộ ký tự, khi có các codec thích hợp. Với một bộ ký tự cho trước, lớp sẽ cố gắng hết sức để cung cấp thông tin về cách sử dụng bộ ký tự đó trong thông điệp email theo cách tuân thủ RFC.

   Một số bộ ký tự phải được mã hóa bằng quoted-printable hoặc base64 khi được sử dụng trong tiêu đề hoặc nội dung email. Một số bộ ký tự phải được chuyển đổi hoàn toàn và không được phép sử dụng trong email.

   *input_charset* tùy chọn được mô tả bên dưới; giá trị này luôn được chuyển thành chữ thường. Sau khi được chuẩn hóa bí danh, giá trị này cũng được dùng để tra cứu trong registry của các bộ ký tự nhằm xác định encoding cho tiêu đề, encoding cho nội dung và codec chuyển đổi đầu ra cần dùng cho bộ ký tự đó. Ví dụ, nếu *input_charset* là ``iso-8859-1``, thì tiêu đề và nội dung sẽ được mã hóa bằng quoted-printable và không cần codec chuyển đổi đầu ra. Nếu *input_charset* là ``euc-jp``, thì tiêu đề sẽ được mã hóa bằng base64, nội dung sẽ không được mã hóa, nhưng văn bản đầu ra sẽ được chuyển đổi từ bộ ký tự ``euc-jp`` sang bộ ký tự ``iso-2022-jp``.

   Các instance :class:`Charset` có những thuộc tính dữ liệu sau:

   .. attribute:: input_charset

      Bộ ký tự được chỉ định ban đầu. Các bí danh phổ biến được chuyển đổi thành tên email *official* tương ứng (ví dụ: ``latin_1`` được chuyển đổi thành ``iso-8859-1``). Mặc định là ``us-ascii`` 7-bit.


   .. attribute:: header_encoding

      Nếu bộ ký tự phải được mã hóa trước khi có thể sử dụng trong tiêu đề email, thuộc tính này sẽ được đặt thành ``charset.QP`` (đối với quoted-printable), ``charset.BASE64`` (đối với mã hóa base64) hoặc ``charset.SHORTEST`` cho kiểu mã hóa ngắn hơn giữa QP và BASE64. Nếu không, giá trị sẽ là ``None``.


   .. attribute:: body_encoding

      Tương tự *header_encoding*, nhưng mô tả kiểu mã hóa cho phần thân của thông điệp thư, vốn có thể khác với kiểu mã hóa tiêu đề. ``charset.SHORTEST`` không được phép đối với *body_encoding*.


   .. attribute:: output_charset

      Một số bộ ký tự phải được chuyển đổi trước khi có thể sử dụng trong tiêu đề hoặc phần thân email. Nếu *input_charset* thuộc một trong số đó, thuộc tính này sẽ chứa tên của bộ ký tự mà đầu ra sẽ được chuyển đổi thành. Nếu không, giá trị sẽ là ``None``.


   .. attribute:: input_codec

      Tên của Python codec được dùng để chuyển đổi *input_charset* thành Unicode. Nếu không cần codec chuyển đổi, thuộc tính này sẽ là ``None``.


   .. attribute:: output_codec

      Tên của Python codec được dùng để chuyển đổi Unicode thành *output_charset*. Nếu không cần codec chuyển đổi, thuộc tính này sẽ có cùng giá trị với *input_codec*.


   Các instance :class:`Charset` cũng có các phương thức sau:

   .. method:: get_body_encoding()

      Trả về kiểu mã hóa truyền nội dung được sử dụng để mã hóa phần thân.

      Đây có thể là chuỗi ``quoted-printable`` hoặc ``base64`` tùy thuộc vào encoding được sử dụng, hoặc có thể là một hàm; trong trường hợp đó, bạn nên gọi hàm với một đối số duy nhất là đối tượng Message đang được encoding. Sau đó, hàm sẽ tự đặt header :mailheader:`Content-Transfer-Encoding` thành giá trị phù hợp.

      Trả về chuỗi ``quoted-printable`` nếu *body_encoding* là ``QP``, trả về chuỗi ``base64`` nếu *body_encoding* là ``BASE64``, và trả về chuỗi ``7bit`` trong các trường hợp khác.


   .. method:: get_output_charset()

      Trả về bộ ký tự đầu ra.

      Đây là thuộc tính *output_charset* nếu thuộc tính đó không phải là ``None``, nếu không thì đây là *input_charset*.


   .. method:: header_encode(string)

      Mã hóa header cho chuỗi *string*.

      Loại encoding (base64 hoặc quoted-printable) sẽ dựa trên thuộc tính *header_encoding*.


   .. method:: header_encode_lines(string, maxlengths)

      Mã hóa header cho một *string* bằng cách trước tiên chuyển đổi chuỗi đó thành các byte.

      Điều này tương tự như :meth:`header_encode`, ngoại trừ việc chuỗi được định dạng theo độ dài dòng tối đa được cung cấp bởi đối số *maxlengths*, đối số này phải là một iterator: mỗi phần tử được trả về từ iterator này sẽ cung cấp độ dài dòng tối đa tiếp theo.


   .. method:: body_encode(string)

      Mã hóa phần thân của chuỗi *string*.

      Loại encoding (base64 hoặc quoted-printable) sẽ dựa trên thuộc tính *body_encoding*.

   Lớp :class:`Charset` cũng cung cấp một số phương thức để hỗ trợ các phép toán tiêu chuẩn và các hàm tích hợp sẵn.


   .. method:: __str__()

      Trả về *input_charset* dưới dạng chuỗi được chuyển thành chữ thường. :meth:`!__repr__` là bí danh của :meth:`!__str__`.


   .. method:: __eq__(other)

      Phương thức này cho phép bạn so sánh hai thực thể :class:`Charset` xem chúng có bằng nhau hay không.


   .. method:: __ne__(other)

      Phương thức này cho phép bạn so sánh hai thực thể :class:`Charset` xem chúng có khác nhau hay không.

Mô-đun :mod:`!email.charset` cũng cung cấp các hàm sau để thêm các mục mới vào các registry toàn cục về character set, alias và codec:


.. function:: add_charset(charset, header_enc=None, body_enc=None, output_charset=None)

   Thêm các thuộc tính của character set vào registry toàn cục.

   *charset* là character set đầu vào và phải là tên chuẩn của một character set.

   *header_enc* và *body_enc* tùy chọn có thể là ``charset.QP`` để dùng quoted-printable, ``charset.BASE64`` để mã hóa bằng base64, ``charset.SHORTEST`` để dùng cách mã hóa ngắn hơn giữa quoted-printable và base64, hoặc ``None`` để không mã hóa. ``SHORTEST`` chỉ hợp lệ với *header_enc*. Mặc định là ``None`` để không mã hóa.

   *output_charset* tùy chọn là character set mà đầu ra sẽ sử dụng. Khi phương thức :meth:`Charset.convert` được gọi, quá trình chuyển đổi sẽ diễn ra từ character set đầu vào sang Unicode, rồi sang character set đầu ra. Mặc định, đầu ra sử dụng cùng character set với đầu vào.

   Cả *input_charset* và *output_charset* đều phải có các mục codec Unicode trong ánh xạ character set-to-codec của mô-đun; hãy dùng :func:`add_codec` để thêm các codec mà mô-đun chưa biết. Xem tài liệu của mô-đun :mod:`codecs` để biết thêm thông tin.

   Registry character set toàn cục được lưu trong dictionary toàn cục của mô-đun ``CHARSETS``.


.. function:: add_alias(alias, canonical)

   Thêm một alias cho bộ ký tự. *alias* là tên alias, ví dụ: ``latin-1``. *canonical* là tên chuẩn của bộ ký tự, ví dụ: ``iso-8859-1``.

   Registry alias charset toàn cục được lưu trong dictionary toàn cục của module ``ALIASES``.


.. function:: add_codec(charset, codecname)

   Thêm một codec ánh xạ các ký tự trong bộ ký tự đã cho sang Unicode và ngược lại.

   *charset* là tên chuẩn của một bộ ký tự. *codecname* là tên của một Python codec, phù hợp làm đối số thứ hai cho :class:`str`'s
   :meth:`~str.encode` phương thức.

