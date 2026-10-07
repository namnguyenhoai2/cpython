.. _codec-registry:

Registry codec và các hàm hỗ trợ
================================

.. c:function:: int PyCodec_Register(PyObject *search_function)

   Đăng ký một hàm tìm kiếm codec mới.

   Là một tác dụng phụ, hàm này cố gắng tải gói :mod:`!encodings`, nếu gói chưa được tải, để đảm bảo gói này luôn đứng đầu danh sách các hàm tìm kiếm.

.. c:function:: int PyCodec_Unregister(PyObject *search_function)

   Hủy đăng ký một hàm tìm kiếm codec và xóa bộ nhớ đệm của registry. Nếu hàm tìm kiếm chưa được đăng ký, không thực hiện thao tác nào. Trả về 0 nếu thành công. Phát sinh một ngoại lệ và trả về -1 nếu xảy ra lỗi.

   .. versionadded:: 3.10

.. c:function:: int PyCodec_KnownEncoding(const char *encoding)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc có codec nào được đăng ký cho *encoding* đã cho hay không. Hàm này luôn thành công.

.. c:function:: PyObject* PyCodec_Encode(PyObject *object, const char *encoding, const char *errors)

   API mã hóa chung dựa trên codec.

   Đối tượng *object* được truyền qua hàm encoder được tìm thấy cho *encoding* đã cho bằng phương thức xử lý lỗi được định nghĩa bởi *errors*. *errors* có thể là ``NULL`` để sử dụng phương thức mặc định được định nghĩa cho codec. Phát sinh một
   :exc:`LookupError` nếu không tìm thấy encoder nào.

.. c:function:: PyObject* PyCodec_Decode(PyObject *object, const char *encoding, const char *errors)

   API giải mã tổng quát dựa trên codec.

   *object* được truyền qua hàm decoder được tìm thấy cho *encoding* đã cho, sử dụng phương thức xử lý lỗi được xác định bởi *errors*.  *errors* có thể là ``NULL`` để sử dụng phương thức mặc định được xác định cho codec.  Raises a
   :exc:`LookupError` nếu không tìm thấy decoder nào.


API tra cứu codec
-----------------

Trong các hàm sau, chuỗi *encoding* được tra cứu sau khi chuyển thành các ký tự viết thường, nhờ đó các encoding được tra cứu thông qua cơ chế này thực tế không phân biệt chữ hoa chữ thường.  Nếu không tìm thấy codec, một :exc:`KeyError` được thiết lập và ``NULL`` được trả về.

.. c:function:: PyObject* PyCodec_Encoder(const char *encoding)

   Lấy một hàm encoder cho *encoding* đã cho.

.. c:function:: PyObject* PyCodec_Decoder(const char *encoding)

   Lấy một hàm decoder cho *encoding* đã cho.

.. c:function:: PyObject* PyCodec_IncrementalEncoder(const char *encoding, const char *errors)

   Lấy một đối tượng :class:`~codecs.IncrementalEncoder` cho *encoding* đã cho.

.. c:function:: PyObject* PyCodec_IncrementalDecoder(const char *encoding, const char *errors)

   Lấy một đối tượng :class:`~codecs.IncrementalDecoder` cho *encoding* đã cho.

.. c:function:: PyObject* PyCodec_StreamReader(const char *encoding, PyObject *stream, const char *errors)

   Lấy một hàm factory :class:`~codecs.StreamReader` cho *encoding* đã cho.

.. c:function:: PyObject* PyCodec_StreamWriter(const char *encoding, PyObject *stream, const char *errors)

   Lấy một hàm factory :class:`~codecs.StreamWriter` cho *encoding* đã cho.


API registry cho các trình xử lý lỗi encoding Unicode
-----------------------------------------------------

.. c:function:: int PyCodec_RegisterError(const char *name, PyObject *error)

   Đăng ký hàm callback xử lý lỗi *error* với *name* đã cho. Hàm callback này sẽ được codec gọi khi gặp các ký tự không thể encoding hoặc các byte không thể decoding, và *name* được chỉ định làm tham số lỗi trong lệnh gọi đến hàm encode/decode.

   Callback nhận một đối số duy nhất, là một thể hiện của
   :exc:`UnicodeEncodeError`, :exc:`UnicodeDecodeError` hoặc
   :exc:`UnicodeTranslateError` chứa thông tin về chuỗi ký tự hoặc byte có vấn đề và vị trí của chúng trong chuỗi ban đầu (xem
   :ref:`unicodeexceptions` để biết các hàm trích xuất thông tin này). Callback phải ném exception được cung cấp hoặc trả về một tuple gồm hai phần tử chứa phần thay thế cho chuỗi có vấn đề và một số nguyên cho biết vị trí trong chuỗi ban đầu tại đó quá trình encoding/decoding sẽ được tiếp tục.

   Trả về ``0`` khi thành công, ``-1`` khi có lỗi.

.. c:function:: PyObject* PyCodec_LookupError(const char *name)

   Tra cứu hàm callback xử lý lỗi được đăng ký dưới *name*. Trường hợp đặc biệt, có thể truyền ``NULL``, khi đó callback xử lý lỗi cho "strict" sẽ được trả về.

.. c:function:: PyObject* PyCodec_StrictErrors(PyObject *exc)

   Ném *exc* dưới dạng exception.

.. c:function:: PyObject* PyCodec_IgnoreErrors(PyObject *exc)

   Bỏ qua lỗi Unicode, bỏ qua dữ liệu đầu vào bị lỗi.

.. c:function:: PyObject* PyCodec_ReplaceErrors(PyObject *exc)

   Thay thế lỗi mã hóa Unicode bằng ``?`` hoặc ``U+FFFD``.

.. c:function:: PyObject* PyCodec_XMLCharRefReplaceErrors(PyObject *exc)

   Thay thế lỗi mã hóa Unicode bằng các tham chiếu ký tự XML.

.. c:function:: PyObject* PyCodec_BackslashReplaceErrors(PyObject *exc)

   Thay thế lỗi mã hóa Unicode bằng các chuỗi thoát backslash (``\x``, ``\u`` và ``\U``).

.. c:function:: PyObject* PyCodec_NameReplaceErrors(PyObject *exc)

   Thay thế lỗi mã hóa Unicode bằng các chuỗi thoát ``\N{...}``.

   .. versionadded:: 3.5


Các biến tiện ích của codec
---------------------------

.. c:var:: const char *Py_hexdigits

   Một hằng chuỗi chứa các chữ số thập lục phân viết thường: ``"0123456789abcdef"``.

   .. versionadded:: 3.3
