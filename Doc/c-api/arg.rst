.. highlight:: c

.. _arg-parsing:

Phân tích đối số và xây dựng giá trị
====================================

Các hàm này hữu ích khi tạo các hàm và phương thức mở rộng của riêng bạn. Thông tin bổ sung và các ví dụ có sẵn trong
:ref:`extending-index`.

Ba hàm đầu tiên được mô tả trong số này, :c:func:`PyArg_ParseTuple`,
:c:func:`PyArg_ParseTupleAndKeywords`, và :c:func:`PyArg_Parse`, đều sử dụng *chuỗi định dạng* để cho hàm biết các đối số được mong đợi. Các chuỗi định dạng sử dụng cùng một cú pháp cho mỗi hàm này.

----------------
Phân tích đối số
----------------

Một chuỗi định dạng bao gồm không hoặc nhiều "đơn vị định dạng". Một đơn vị định dạng mô tả một đối tượng Python; thông thường, đó là một ký tự đơn hoặc một chuỗi các đơn vị định dạng được đặt trong ngoặc đơn. Với một vài ngoại lệ, một đơn vị định dạng không phải là một chuỗi được đặt trong ngoặc đơn thường tương ứng với một đối số địa chỉ duy nhất của các hàm này. Trong phần mô tả sau đây, dạng được đặt trong dấu ngoặc kép là đơn vị định dạng; mục trong ngoặc đơn là kiểu đối tượng Python khớp với đơn vị định dạng; còn mục trong ngoặc vuông là kiểu của (các) biến C mà địa chỉ của chúng cần được truyền vào.

.. _arg-parsing-string-and-buffers:

Chuỗi và bộ đệm
---------------

.. note::

   Trên Python 3.12 và các phiên bản cũ hơn, macro :c:macro:`!PY_SSIZE_T_CLEAN` phải được định nghĩa trước khi include :file:`Python.h` để sử dụng tất cả các biến thể ``#`` của các định dạng (``s#``, ``y#``, v.v.) được giải thích bên dưới. Điều này không cần thiết trên Python 3.13 và các phiên bản mới hơn.

Các định dạng này cho phép truy cập một object dưới dạng một vùng bộ nhớ liền kề. Bạn không cần cung cấp vùng lưu trữ thô cho vùng unicode hoặc bytes được trả về.

Trừ khi có ghi chú khác, các buffer không được kết thúc bằng NUL.

Có ba cách để chuyển đổi strings và buffers sang C:

*  Các định dạng như ``y*`` và ``s*`` điền vào một cấu trúc :c:type:`Py_buffer`. Việc này khóa buffer bên dưới để caller sau đó có thể sử dụng buffer ngay cả bên trong một khối :c:type:`Py_BEGIN_ALLOW_THREADS` mà không có nguy cơ dữ liệu mutable bị thay đổi kích thước hoặc bị hủy. Do đó, **bạn phải gọi** :c:func:`PyBuffer_Release` sau khi xử lý xong dữ liệu (hoặc trong bất kỳ trường hợp hủy sớm nào).

*  Các định dạng ``es``, ``es#``, ``et`` và ``et#`` cấp phát buffer kết quả. **Bạn phải gọi** :c:func:`PyMem_Free` sau khi xử lý xong dữ liệu (hoặc trong bất kỳ trường hợp hủy sớm nào).

*  .. _c-arg-borrowed-buffer:

   Các format khác nhận một :class:`str` hoặc một :term:`bytes-like object` chỉ đọc, chẳng hạn như :class:`bytes`, và cung cấp một con trỏ ``const char *`` tới buffer của nó. Trong trường hợp này, buffer được “mượn”: nó do đối tượng Python tương ứng quản lý và có cùng vòng đời với đối tượng này. Bạn không cần tự giải phóng bộ nhớ.

   Để bảo đảm buffer bên dưới có thể được mượn một cách an toàn, trường
   :c:member:`PyBufferProcs.bf_releasebuffer` của đối tượng phải là ``NULL``. Điều này không cho phép các đối tượng có thể thay đổi phổ biến như :class:`bytearray`, đồng thời cũng loại trừ một số đối tượng chỉ đọc như :class:`memoryview` của
   :class:`bytes`.

   Ngoài yêu cầu về ``bf_releasebuffer`` này, không có bước kiểm tra nào để xác minh liệu đối tượng đầu vào có bất biến hay không (ví dụ: liệu đối tượng đó có đáp ứng yêu cầu về một buffer có thể ghi hay không, hoặc một thread khác có thể thay đổi dữ liệu hay không).

``s`` (:class:`str`) [const char \*]
   Chuyển đổi một đối tượng Unicode thành con trỏ C trỏ tới một chuỗi ký tự. Con trỏ tới chuỗi hiện có được lưu trong biến con trỏ ký tự có địa chỉ được bạn truyền vào. Chuỗi C được kết thúc bằng NUL. Chuỗi Python không được chứa các code point null nằm bên trong; nếu có, một ngoại lệ :exc:`ValueError` sẽ được phát sinh. Các đối tượng Unicode được chuyển đổi thành chuỗi C bằng encoding ``'utf-8'``. Nếu quá trình chuyển đổi này thất bại, một
   :exc:`UnicodeError` sẽ được phát sinh.

   .. note::
      Định dạng này không chấp nhận :term:`các đối tượng dạng bytes <bytes-like object>`. Nếu bạn muốn chấp nhận các đường dẫn hệ thống tệp và chuyển đổi chúng thành chuỗi ký tự C, tốt hơn nên sử dụng định dạng ``O&`` với :c:func:`PyUnicode_FSConverter` làm *converter*.

   .. versionchanged:: 3.5
      Trước đây, :exc:`TypeError` được phát sinh khi gặp các điểm mã null nhúng trong chuỗi Python.

``s*`` (:class:`str` hoặc :term:`bytes-like object`) [Py_buffer]
   Định dạng này chấp nhận cả đối tượng Unicode và các đối tượng dạng bytes. Nó điền vào cấu trúc :c:type:`Py_buffer` do bên gọi cung cấp. Trong trường hợp này, chuỗi C kết quả có thể chứa các byte NUL nhúng. Các đối tượng Unicode được chuyển đổi thành chuỗi C bằng cách sử dụng encoding ``'utf-8'``.

``s#`` (:class:`str`, chỉ đọc :term:`bytes-like object`) [const char \*, :c:type:`Py_ssize_t`]
   Tương tự ``s*``, nhưng cung cấp một :ref:`buffer mượn <c-arg-borrowed-buffer>`. Kết quả được lưu vào hai biến C, biến thứ nhất là một con trỏ tới chuỗi C, biến thứ hai là độ dài của chuỗi đó. Chuỗi này có thể chứa các byte null nhúng. Các đối tượng Unicode được chuyển đổi thành chuỗi C bằng cách sử dụng encoding ``'utf-8'``.

``z`` (:class:`str` hoặc ``None``) [const char \*]
   Giống như ``s``, nhưng đối tượng Python cũng có thể là ``None``, trong trường hợp đó con trỏ C được đặt thành ``NULL``.

``z*`` (:class:`str`, :term:`bytes-like object` hoặc ``None``) [Py_buffer]
   Giống như ``s*``, nhưng đối tượng Python cũng có thể là ``None``, trong trường hợp đó thành viên ``buf`` của cấu trúc :c:type:`Py_buffer` được đặt thành ``NULL``.

``z#`` (:class:`str`, :term:`bytes-like object` chỉ đọc hoặc ``None``) [const char \*, :c:type:`Py_ssize_t`]
   Giống như ``s#``, nhưng đối tượng Python cũng có thể là ``None``, trong trường hợp đó con trỏ C được đặt thành ``NULL``.

``y`` (:term:`bytes-like object` chỉ đọc) [const char \*]
   Định dạng này chuyển đổi một đối tượng giống bytes thành một con trỏ C tới một
   :ref:`borrowed <c-arg-borrowed-buffer>` chuỗi ký tự; nó không chấp nhận các đối tượng Unicode. Bộ đệm bytes không được chứa byte null nằm bên trong; nếu có, một ngoại lệ :exc:`ValueError` sẽ được nâng lên.

   .. versionchanged:: 3.5
      Trước đây, :exc:`TypeError` được nâng lên khi phát hiện byte null nằm bên trong bộ đệm bytes.

``y*`` (:term:`bytes-like object`) [Py_buffer]
   Biến thể này của ``s*`` không chấp nhận các đối tượng Unicode, chỉ chấp nhận các đối tượng dạng bytes. **Đây là cách được khuyến nghị để chấp nhận dữ liệu nhị phân.**

``y#`` (chỉ đọc :term:`bytes-like object`) [const char \*, :c:type:`Py_ssize_t`]
   Biến thể này của ``s#`` không chấp nhận các đối tượng Unicode, chỉ chấp nhận các đối tượng dạng bytes.

``S`` (:class:`bytes`) [PyBytesObject \*]
   Yêu cầu đối tượng Python là một đối tượng :class:`bytes`, mà không cố gắng thực hiện bất kỳ chuyển đổi nào. Gây ra :exc:`TypeError` nếu đối tượng không phải là đối tượng bytes. Biến C cũng có thể được khai báo là :c:expr:`PyObject*`.

``Y`` (:class:`bytearray`) [PyByteArrayObject \*]
   Yêu cầu đối tượng Python là một đối tượng :class:`bytearray`, mà không cố gắng thực hiện bất kỳ chuyển đổi nào. Gây ra :exc:`TypeError` nếu đối tượng không phải là đối tượng :class:`bytearray`. Biến C cũng có thể được khai báo là :c:expr:`PyObject*`.

``U`` (:class:`str`) [PyObject \*]
   Yêu cầu đối tượng Python là một đối tượng Unicode, mà không cố gắng thực hiện bất kỳ chuyển đổi nào. Gây ra :exc:`TypeError` nếu đối tượng không phải là đối tượng Unicode. Biến C cũng có thể được khai báo là :c:expr:`PyObject*`.

``w*`` (đọc-ghi :term:`bytes-like object`) [Py_buffer]
   Định dạng này chấp nhận mọi đối tượng triển khai giao diện bộ đệm đọc-ghi. Nó điền vào một cấu trúc :c:type:`Py_buffer` do bên gọi cung cấp. Bộ đệm có thể chứa các byte null nhúng. Bên gọi phải gọi
   :c:func:`PyBuffer_Release` khi hoàn tất việc sử dụng buffer.

``es`` (:class:`str`) [const char \*encoding, char \*\*buffer]
   Biến thể này của ``s`` được dùng để mã hóa Unicode vào một buffer ký tự. Nó chỉ hoạt động với dữ liệu đã mã hóa không chứa các byte NUL nhúng.

   Định dạng này yêu cầu hai đối số. Đối số đầu tiên chỉ được dùng làm đầu vào và phải là một :c:expr:`const char*` trỏ đến tên của một encoding dưới dạng chuỗi kết thúc bằng NUL, hoặc ``NULL``, trong trường hợp đó encoding ``'utf-8'`` sẽ được sử dụng. Python sẽ phát sinh ngoại lệ nếu không biết encoding được nêu tên. Đối số thứ hai phải là một :c:expr:`char**`; giá trị của con trỏ mà nó tham chiếu sẽ được đặt thành một buffer chứa nội dung của văn bản đối số. Văn bản sẽ được mã hóa bằng encoding được chỉ định bởi đối số đầu tiên.

   :c:func:`PyArg_ParseTuple` sẽ cấp phát một buffer có kích thước cần thiết, sao chép dữ liệu đã mã hóa vào buffer này và điều chỉnh *\*buffer* để tham chiếu đến vùng lưu trữ vừa được cấp phát. Bên gọi chịu trách nhiệm gọi :c:func:`PyMem_Free` để giải phóng buffer đã cấp phát sau khi sử dụng.

``et`` (:class:`str`, :class:`bytes` or :class:`bytearray`) [const char \*encoding, char \*\*buffer]
   Tương tự như ``es``, ngoại trừ việc các đối tượng byte string được truyền qua mà không được mã hóa lại. Thay vào đó, phần triển khai giả định rằng đối tượng byte string sử dụng encoding được truyền vào dưới dạng tham số.

``es#`` (:class:`str`) [const char \*encoding, char \*\*buffer, :c:type:`Py_ssize_t` \*buffer_length]
   Biến thể này của ``s#`` được dùng để mã hóa Unicode vào một bộ đệm ký tự. Không giống định dạng ``es``, biến thể này cho phép dữ liệu đầu vào chứa các ký tự NUL.

   Nó yêu cầu ba đối số. Đối số đầu tiên chỉ được dùng làm đầu vào và phải là một
   :c:expr:`const char*` trỏ đến tên của một encoding dưới dạng chuỗi kết thúc bằng NUL, hoặc ``NULL``, trong trường hợp đó encoding ``'utf-8'`` sẽ được sử dụng. Một ngoại lệ sẽ được phát sinh nếu Python không biết encoding được đặt tên. Đối số thứ hai phải là một :c:expr:`char**`; giá trị của con trỏ mà nó tham chiếu sẽ được đặt thành một bộ đệm chứa nội dung của văn bản đối số. Văn bản sẽ được mã hóa bằng encoding được chỉ định bởi đối số đầu tiên. Đối số thứ ba phải là một con trỏ đến một số nguyên; số nguyên được tham chiếu sẽ được đặt thành số byte trong bộ đệm đầu ra.

   Có hai chế độ hoạt động:

   Nếu *\*buffer* trỏ đến một con trỏ ``NULL``, hàm sẽ cấp phát một bộ đệm có kích thước cần thiết, sao chép dữ liệu đã mã hóa vào bộ đệm này và đặt *\*buffer* để tham chiếu đến vùng lưu trữ mới được cấp phát. Người gọi chịu trách nhiệm gọi
   :c:func:`PyMem_Free` để giải phóng bộ đệm đã cấp phát sau khi sử dụng.

   Nếu *\*buffer* trỏ đến một con trỏ không phải ``NULL`` (một buffer đã được cấp phát),
   :c:func:`PyArg_ParseTuple` sẽ sử dụng vị trí này làm buffer và diễn giải giá trị ban đầu của *\*buffer_length* là kích thước của buffer. Sau đó, nó sẽ sao chép dữ liệu đã mã hóa vào buffer và thêm ký tự kết thúc NUL. Nếu buffer không đủ lớn, một :exc:`ValueError` sẽ được thiết lập.

   Trong cả hai trường hợp, *\*buffer_length* được đặt thành độ dài của dữ liệu đã mã hóa, không bao gồm byte NUL ở cuối.

``et#`` (:class:`str`, :class:`bytes` hoặc :class:`bytearray`) [const char \*encoding, char \*\*buffer, :c:type:`Py_ssize_t` \*buffer_length]
   Tương tự như ``es#``, ngoại trừ việc các đối tượng chuỗi byte được truyền qua mà không được mã hóa lại. Thay vào đó, implementation giả định rằng đối tượng chuỗi byte sử dụng encoding được truyền vào dưới dạng tham số.

.. versionchanged:: 3.12
   ``u``, ``u#``, ``Z`` và ``Z#`` bị loại bỏ vì chúng sử dụng biểu diễn ``Py_UNICODE*`` kế thừa.


Số
--

Các định dạng này cho phép biểu diễn số Python hoặc ký tự đơn dưới dạng số C. Các định dạng yêu cầu :class:`int`, :class:`float` hoặc :class:`complex` cũng có thể sử dụng các phương thức đặc biệt tương ứng :meth:`~object.__index__`,
:meth:`~object.__float__` hoặc :meth:`~object.__complex__` để chuyển đổi đối tượng Python sang kiểu cần thiết.

Đối với các định dạng số nguyên có dấu, :exc:`OverflowError` được phát sinh nếu giá trị nằm ngoài phạm vi của kiểu C. Đối với các định dạng số nguyên không dấu, không thực hiện kiểm tra phạm vi --- các bit có trọng số cao nhất sẽ bị cắt ngầm khi trường nhận không đủ lớn để chứa giá trị.

``b`` (:class:`int`) [unsigned char]
   Chuyển đổi một số nguyên Python không âm thành một số nguyên cực nhỏ không dấu, được lưu trữ trong một C
   :c:expr:`unsigned char`.

``B`` (:class:`int`) [unsigned char]
   Chuyển đổi một số nguyên Python thành một số nguyên cực nhỏ mà không kiểm tra tràn, được lưu trữ trong một C
   :c:expr:`unsigned char`.

``h`` (:class:`int`) [short int]
   Chuyển một số nguyên Python thành :c:expr:`short int` C.

``H`` (:class:`int`) [unsigned short int]
   Chuyển một số nguyên Python thành :c:expr:`unsigned short int` C mà không kiểm tra tràn.

``i`` (:class:`int`) [int]
   Chuyển một số nguyên Python thành :c:expr:`int` C thuần.

``I`` (:class:`int`) [unsigned int]
   Chuyển một số nguyên Python thành :c:expr:`unsigned int` của C mà không kiểm tra tràn số.

``l`` (:class:`int`) [long int]
   Chuyển một số nguyên Python thành :c:expr:`long int` của C.

``k`` (:class:`int`) [unsigned long]
   Chuyển một số nguyên Python thành :c:expr:`unsigned long` của C mà không kiểm tra tràn số.

   .. versionchanged:: 3.14
      Sử dụng :meth:`~object.__index__` nếu có.

``L`` (:class:`int`) [long long]
   Chuyển một số nguyên Python thành một :c:expr:`long long` trong C.

``K`` (:class:`int`) [unsigned long long]
   Chuyển một số nguyên Python thành một :c:expr:`unsigned long long` trong C mà không kiểm tra tràn số.

   .. versionchanged:: 3.14
      Sử dụng :meth:`~object.__index__` nếu có.

``n`` (:class:`int`) [:c:type:`Py_ssize_t`]
   Chuyển một số nguyên Python thành một :c:type:`Py_ssize_t` trong C.

``c`` (:class:`bytes` hoặc :class:`bytearray` có độ dài 1) [char]
   Chuyển một byte Python, được biểu diễn dưới dạng :class:`bytes` hoặc
   :class:`bytearray` đối tượng có độ dài 1, thành một :c:expr:`char` trong C.

   .. versionchanged:: 3.3
      Cho phép các đối tượng :class:`bytearray`.

``C`` (:class:`str` có độ dài 1) [int]
   Chuyển đổi một ký tự Python, được biểu diễn dưới dạng đối tượng :class:`str` có độ dài 1, thành một :c:expr:`int` trong C.

``f`` (:class:`float`) [float]
   Chuyển đổi một số dấu phẩy động Python thành một :c:expr:`float` trong C.

``d`` (:class:`float`) [double]
   Chuyển đổi một số dấu phẩy động Python thành :c:expr:`double` của C.

``D`` (:class:`complex`) [Py_complex]
   Chuyển đổi một số phức Python thành cấu trúc :c:type:`Py_complex` của C.

Các đối tượng khác
------------------

``O`` (object) [PyObject \*]
   Lưu trữ một object Python (không qua chuyển đổi) trong một con trỏ object của C. Do đó, chương trình C nhận chính object thực tế đã được truyền vào. Một
   :term:`strong reference` tới object không được tạo (tức là reference count của nó không tăng). Con trỏ được lưu trữ không phải là ``NULL``.

``O!`` (object) [*typeobject*, PyObject \*]
   Lưu một đối tượng Python vào con trỏ đối tượng C. Tương tự như ``O``, nhưng nhận hai đối số C: đối số đầu tiên là địa chỉ của một đối tượng kiểu Python, đối số thứ hai là địa chỉ của biến C (kiểu :c:expr:`PyObject*`) dùng để lưu con trỏ đối tượng. Nếu đối tượng Python không có kiểu bắt buộc, :exc:`TypeError` sẽ được phát sinh.

.. _o_ampersand:

``O&`` (object) [*converter*, *address*]
   Chuyển đổi một đối tượng Python thành một biến C thông qua hàm *converter*. Hàm này nhận hai đối số: đối số đầu tiên là một hàm, đối số thứ hai là địa chỉ của một biến C (kiểu bất kỳ), được chuyển đổi thành :c:expr:`void *`. Sau đó, hàm *converter* được gọi như sau::

      status = converter(object, address);

   trong đó *object* là đối tượng Python cần chuyển đổi và *address* là
   :c:expr:`void*` đối số đã được truyền cho hàm ``PyArg_Parse*``. Giá trị *status* trả về phải là ``1`` nếu chuyển đổi thành công và ``0`` nếu chuyển đổi thất bại. Khi chuyển đổi thất bại, hàm *converter* phải phát sinh một exception và giữ nguyên nội dung của *address*.

   .. c:macro:: Py_CLEANUP_SUPPORTED
      :no-typesetting:

   Nếu *converter* trả về :c:macro:`!Py_CLEANUP_SUPPORTED`, hàm này có thể được gọi lần thứ hai nếu quá trình phân tích đối số cuối cùng thất bại, cho phép converter giải phóng mọi vùng nhớ mà nó đã cấp phát trước đó. Trong lần gọi thứ hai này, tham số *object* sẽ là ``NULL``; *address* sẽ có cùng giá trị như trong lần gọi ban đầu.

   Ví dụ về các converter: :c:func:`PyUnicode_FSConverter` và
   :c:func:`PyUnicode_FSDecoder`.

   .. versionchanged:: 3.1
      :c:macro:`!Py_CLEANUP_SUPPORTED` was added.

``p`` (:class:`bool`) [int]
   Kiểm tra giá trị được truyền vào về tính đúng (một **p**\ redicate boolean) và chuyển đổi kết quả thành giá trị số nguyên C true/false tương đương. Đặt int thành ``1`` nếu biểu thức đúng và thành ``0`` nếu biểu thức sai. Giá trị này chấp nhận mọi giá trị Python hợp lệ. Xem :ref:`truth` để biết thêm thông tin về cách Python kiểm tra tính đúng của các giá trị.

   .. versionadded:: 3.3

``(items)`` (sequence) [*matching-items*]
   Đối tượng phải là một sequence Python (ngoại trừ :class:`str`, :class:`bytes` hoặc :class:`bytearray`) có độ dài bằng số đơn vị định dạng trong *items*. Các đối số C phải tương ứng với từng đơn vị định dạng trong *items*. Các đơn vị định dạng cho sequence có thể được lồng nhau.

   Nếu *items* chứa các đơn vị định dạng lưu trữ một :ref:`bộ đệm mượn <c-arg-borrowed-buffer>` (``s``, ``s#``, ``z``, ``z#``, ``y``, hoặc ``y#``) hoặc một :term:`borrowed reference` (``S``, ``Y``, ``U``, ``O``, hoặc ``O!``), đối tượng phải là một tuple Python. *bộ chuyển đổi* cho ``O&`` đơn vị định dạng trong *items* không được lưu trữ bộ đệm mượn hoặc tham chiếu mượn.

   .. versionchanged:: 3.14
      :class:`str` and :class:`bytearray` objects no longer accepted as a sequence.

   .. deprecated:: 3.14
      Các sequence không phải tuple không được khuyến nghị sử dụng nếu *items* chứa các đơn vị định dạng lưu trữ bộ đệm mượn hoặc tham chiếu mượn.

Một vài ký tự khác có ý nghĩa trong chuỗi định dạng. Các ký tự này không được xuất hiện bên trong dấu ngoặc đơn lồng nhau. Đó là:

``|``
   Cho biết rằng các đối số còn lại trong danh sách đối số Python là tùy chọn. Các biến C tương ứng với những đối số tùy chọn phải được khởi tạo bằng giá trị mặc định --- khi một đối số tùy chọn không được chỉ định,
   :c:func:`PyArg_ParseTuple` không tác động đến nội dung của (các) biến C tương ứng. Ví dụ, chuỗi định dạng ``"OO|OO"`` tương ứng với chữ ký Python ``f(a, b, c=None, d=None)``.

``$``
   Chỉ :c:func:`PyArg_ParseTupleAndKeywords`: Cho biết rằng các đối số còn lại trong danh sách đối số Python chỉ có thể được truyền theo từ khóa. Chúng là tùy chọn nếu ``|`` được chỉ định trước ``$``, và là bắt buộc trong trường hợp ngược lại. Không thể chỉ định ``|`` sau ``$``. Ví dụ, chuỗi định dạng ``"O|O$O"`` tương ứng với chữ ký Python ``f(a, b=None, *, c=None)``, còn chuỗi định dạng ``"OO$OO"`` tương ứng với ``f(a, b, *, c, d)``.

   .. versionadded:: 3.3

``:``
   Danh sách các đơn vị định dạng kết thúc tại đây; chuỗi sau dấu hai chấm được dùng làm tên hàm trong các thông báo lỗi ("giá trị liên kết" của ngoại lệ mà
   :c:func:`PyArg_ParseTuple` phát sinh).

``;``
   Danh sách các đơn vị định dạng kết thúc tại đây; chuỗi sau dấu chấm phẩy được dùng làm thông báo lỗi *thay vì* thông báo lỗi mặc định. ``:`` và ``;`` loại trừ lẫn nhau.

Lưu ý rằng mọi tham chiếu đến đối tượng Python được cung cấp cho caller đều là tham chiếu *mượn*; không giải phóng chúng (tức là không giảm reference count của chúng)!

Các đối số bổ sung được truyền cho những hàm này phải là địa chỉ của các biến có kiểu được xác định bởi format string; chúng được dùng để lưu trữ các giá trị từ input tuple. Có một vài trường hợp, như được mô tả trong danh sách các format unit ở trên, khi những tham số này được dùng làm giá trị đầu vào; trong trường hợp đó, chúng phải khớp với nội dung được chỉ định cho format unit tương ứng.

Để quá trình chuyển đổi thành công, đối tượng *arg* phải khớp với format và format phải được xử lý hết. Khi thành công, các hàm ``PyArg_Parse*`` trả về true; nếu không, chúng trả về false và raise exception phù hợp. Khi các hàm ``PyArg_Parse*`` thất bại do lỗi chuyển đổi trong một format unit, các biến tại những địa chỉ tương ứng với format unit đó và các format unit tiếp theo sẽ không bị thay đổi.

Các hàm API
-----------

.. c:function:: int PyArg_ParseTuple(PyObject *args, const char *format, ...)

   Phân tích các tham số của một hàm chỉ nhận tham số positional vào các biến cục bộ. Trả về true khi thành công; khi thất bại, trả về false và raise exception phù hợp.


.. c:function:: int PyArg_VaParse(PyObject *args, const char *format, va_list vargs)

   Tương tự :c:func:`PyArg_ParseTuple`, ngoại trừ việc hàm này nhận va_list thay vì một số lượng đối số thay đổi.


.. c:function:: int PyArg_ParseTupleAndKeywords(PyObject *args, PyObject *kw, const char *format, char * const *keywords, ...)

   Phân tích các tham số của một hàm nhận cả tham số positional và keyword vào các biến cục bộ. Đối số *keywords* là một mảng được kết thúc bằng ``NULL`` gồm các tên tham số keyword được chỉ định dưới dạng các chuỗi C ASCII hoặc UTF-8 kết thúc bằng null. Tên rỗng biểu thị
   :ref:`tham số chỉ theo vị trí <positional-only_parameter>`. Trả về true nếu thành công; nếu thất bại, hàm trả về false và phát sinh ngoại lệ thích hợp.

   .. note::

      Khai báo tham số *keywords* là :c:expr:`char * const *` trong C và
      :c:expr:`const char * const *` trong C++. Có thể ghi đè điều này bằng macro :c:macro:`PY_CXX_CONST`.

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ cho :ref:`tham số chỉ theo vị trí <positional-only_parameter>`.

   .. versionchanged:: 3.13
      Tham số *keywords* hiện có kiểu :c:expr:`char * const *` trong C và
      :c:expr:`const char * const *` trong C++, thay vì :c:expr:`char **`. Đã bổ sung hỗ trợ cho tên tham số keyword không phải ASCII.



.. c:function:: int PyArg_VaParseTupleAndKeywords(PyObject *args, PyObject *kw, const char *format, char * const *keywords, va_list vargs)

   Tương tự :c:func:`PyArg_ParseTupleAndKeywords`, ngoại trừ việc hàm này nhận một va_list thay vì một số lượng đối số thay đổi.


.. c:function:: int PyArg_ValidateKeywordArguments(PyObject *)

   Đảm bảo rằng các khóa trong dictionary đối số keywords là các chuỗi. Việc này chỉ cần thiết nếu không sử dụng :c:func:`PyArg_ParseTupleAndKeywords`, vì đối tượng sau đã thực hiện bước kiểm tra này.

   .. versionadded:: 3.2


.. c:function:: int PyArg_Parse(PyObject *args, const char *format, ...)

   Phân tích tham số của một hàm nhận một tham số positional duy nhất vào một biến cục bộ. Trả về true nếu thành công; nếu thất bại, trả về false và phát sinh exception thích hợp.

   Ví dụ::

       // Function using METH_O calling convention
       static PyObject*
       my_function(PyObject *module, PyObject *arg)
       {
           int value;
           if (!PyArg_Parse(arg, "i:my_function", &value)) {
               return NULL;
           }
           // ... use value ...
       }


.. c:function:: int PyArg_UnpackTuple(PyObject *args, const char *name, Py_ssize_t min, Py_ssize_t max, ...)

   Một cách đơn giản hơn để lấy tham số, không sử dụng format string để chỉ định kiểu của các đối số. Các hàm sử dụng phương thức này để lấy tham số phải được khai báo là :c:macro:`METH_VARARGS` trong các bảng hàm hoặc phương thức. Tuple chứa các tham số thực tế phải được truyền dưới dạng *args*; nó thực sự phải là một tuple. Độ dài của tuple phải ít nhất là *min* và không quá *max*; *min* và *max* có thể bằng nhau. Các đối số bổ sung phải được truyền cho hàm, mỗi đối số trong đó phải là một con trỏ tới một
   :c:expr:`PyObject*` biến; các biến này sẽ được điền bằng các giá trị từ *args*; chúng sẽ chứa :term:`borrowed references <borrowed reference>`. Các biến tương ứng với những tham số tùy chọn không được cung cấp trong *args* sẽ không được điền; bên gọi phải khởi tạo chúng. Hàm này trả về true nếu thành công và false nếu *args* không phải là một tuple hoặc chứa số phần tử không đúng; một exception sẽ được thiết lập nếu xảy ra lỗi.

   Đây là ví dụ về cách sử dụng hàm này, được lấy từ mã nguồn của
   :mod:`!_weakref` mô-đun trợ giúp dành cho weak references::

      static PyObject *
      weakref_ref(PyObject *self, PyObject *args)
      {
          PyObject *object;
          PyObject *callback = NULL;
          PyObject *result = NULL;

          if (PyArg_UnpackTuple(args, "ref", 1, 2, &object, &callback)) {
              result = PyWeakref_NewRef(object, callback);
          }
          return result;
      }

   Lời gọi :c:func:`PyArg_UnpackTuple` trong ví dụ này hoàn toàn tương đương với lời gọi :c:func:`PyArg_ParseTuple`::

      PyArg_ParseTuple(args, "O|O:ref", &object, &callback)

.. c:macro:: PY_CXX_CONST

   Giá trị cần chèn, nếu có, trước :c:expr:`char * const *` trong khai báo tham số *keywords* của
   :c:func:`PyArg_ParseTupleAndKeywords` và
   :c:func:`PyArg_VaParseTupleAndKeywords`. Mặc định là rỗng đối với C và ``const`` đối với C++ (:c:expr:`const char * const *`). Để ghi đè, hãy định nghĩa nó thành giá trị mong muốn trước khi include
   :file:`Python.h`.

   .. versionadded:: 3.13


--------------------
Xây dựng các giá trị
--------------------

.. c:function:: PyObject* Py_BuildValue(const char *format, ...)

   Tạo một giá trị mới dựa trên chuỗi định dạng tương tự các chuỗi được ``PyArg_Parse*`` và họ hàm của nó chấp nhận, cùng với một dãy giá trị. Trả về giá trị hoặc ``NULL`` nếu xảy ra lỗi; một ngoại lệ sẽ được phát sinh nếu ``NULL`` được trả về.

   :c:func:`Py_BuildValue` không phải lúc nào cũng xây dựng một tuple. Nó chỉ xây dựng một tuple nếu chuỗi định dạng chứa từ hai đơn vị định dạng trở lên. Nếu chuỗi định dạng rỗng, nó trả về ``None``; nếu chuỗi chứa chính xác một đơn vị định dạng, nó trả về đối tượng được mô tả bởi đơn vị định dạng đó. Để buộc nó trả về một tuple có kích thước 0 hoặc 1, hãy đặt chuỗi định dạng trong dấu ngoặc đơn.

   Khi các buffer bộ nhớ được truyền dưới dạng tham số để cung cấp dữ liệu xây dựng đối tượng, như đối với các định dạng ``s`` và ``s#``, dữ liệu cần thiết sẽ được sao chép. Các buffer do bên gọi cung cấp không bao giờ được các đối tượng được tạo bởi
   :c:func:`Py_BuildValue` tham chiếu. Nói cách khác, nếu mã của bạn gọi :c:func:`malloc` và truyền vùng nhớ đã cấp phát cho :c:func:`Py_BuildValue`, mã của bạn có trách nhiệm gọi :c:func:`free` cho vùng nhớ đó sau khi
   :c:func:`Py_BuildValue` trả về.

   Trong phần mô tả sau, dạng được đặt trong dấu ngoặc kép là đơn vị định dạng; mục trong dấu ngoặc tròn là kiểu đối tượng Python mà đơn vị định dạng sẽ trả về; còn mục trong dấu ngoặc vuông là kiểu của (các) giá trị C cần truyền vào.

   Các ký tự khoảng trắng, tab, dấu hai chấm và dấu phẩy được bỏ qua trong chuỗi định dạng (nhưng không bị bỏ qua bên trong các đơn vị định dạng như ``s#``). Có thể tận dụng điều này để làm cho các chuỗi định dạng dài dễ đọc hơn một chút.

   ``s`` (:class:`str` hoặc ``None``) [const char \*]
      Chuyển đổi một chuỗi C kết thúc bằng null thành đối tượng Python :class:`str` bằng cách sử dụng encoding ``'utf-8'``. Nếu con trỏ chuỗi C là ``NULL``, thì ``None`` được sử dụng.

   ``s#`` (:class:`str` or ``None``) [const char \*, :c:type:`Py_ssize_t`]
      Chuyển đổi một chuỗi C và độ dài của nó thành đối tượng :class:`str` của Python bằng encoding ``'utf-8'``. Nếu con trỏ chuỗi C là ``NULL``, độ dài sẽ bị bỏ qua và ``None`` được trả về.

   ``y`` (:class:`bytes`) [const char \*]
      Hàm này chuyển đổi một chuỗi C thành đối tượng :class:`bytes` của Python. Nếu con trỏ chuỗi C là ``NULL``, ``None`` được trả về.

   ``y#`` (:class:`bytes`) [const char \*, :c:type:`Py_ssize_t`]
      Hàm này chuyển đổi một chuỗi C và các độ dài của nó thành một đối tượng Python. Nếu con trỏ chuỗi C là ``NULL``, ``None`` được trả về.

   ``z`` (:class:`str` or ``None``) [const char \*]
      Giống như ``s``.

   ``z#`` (:class:`str` hoặc ``None``) [const char \*, :c:type:`Py_ssize_t`]
      Giống như ``s#``.

   ``u`` (:class:`str`) [const wchar_t \*]
      Chuyển đổi buffer :c:type:`wchar_t` kết thúc bằng null chứa dữ liệu Unicode (UTF-16 hoặc UCS-4) thành một đối tượng Unicode của Python. Nếu con trỏ buffer Unicode là ``NULL``, ``None`` được trả về.

   ``u#`` (:class:`str`) [const wchar_t \*, :c:type:`Py_ssize_t`]
      Chuyển đổi buffer dữ liệu Unicode (UTF-16 hoặc UCS-4) và độ dài của buffer thành một đối tượng Unicode của Python. Nếu con trỏ buffer Unicode là ``NULL``, độ dài sẽ bị bỏ qua và ``None`` được trả về.

   ``U`` (:class:`str` or ``None``) [const char \*]
      Giống như ``s``.

   ``U#`` (:class:`str` or ``None``) [const char \*, :c:type:`Py_ssize_t`]
      Giống như ``s#``.

   ``i`` (:class:`int`) [int]
      Chuyển đổi một :c:expr:`int` C thuần túy thành một đối tượng số nguyên Python.

   ``b`` (:class:`int`) [char]
      Chuyển đổi một :c:expr:`char` C thuần túy thành một đối tượng số nguyên Python.

   ``h`` (:class:`int`) [short int]
      Chuyển đổi một :c:expr:`short int` C thuần túy thành một đối tượng số nguyên Python.

   ``l`` (:class:`int`) [long int]
      Chuyển đổi một :c:expr:`long int` C thành một đối tượng số nguyên Python.

   ``B`` (:class:`int`) [unsigned char]
      Chuyển đổi một :c:expr:`unsigned char` C thành một đối tượng số nguyên Python.

   ``H`` (:class:`int`) [unsigned short int]
      Chuyển đổi một :c:expr:`unsigned short int` C thành một đối tượng số nguyên Python.

   ``I`` (:class:`int`) [unsigned int]
      Chuyển đổi một :c:expr:`unsigned int` C thành một đối tượng số nguyên Python.

   ``k`` (:class:`int`) [unsigned long]
      Chuyển đổi một :c:expr:`unsigned long` C thành một đối tượng số nguyên Python.

   ``L`` (:class:`int`) [long long]
      Chuyển đổi một :c:expr:`long long` của C thành một đối tượng số nguyên Python.

   .. _capi-py-buildvalue-format-K:

   ``K`` (:class:`int`) [unsigned long long]
      Chuyển đổi một :c:expr:`unsigned long long` của C thành một đối tượng số nguyên Python.

   ``n`` (:class:`int`) [:c:type:`Py_ssize_t`]
      Chuyển đổi một :c:type:`Py_ssize_t` của C thành một số nguyên Python.

   ``p`` (:class:`bool`) [int]
      Chuyển đổi một :c:expr:`int` của C thành một đối tượng :class:`bool` Python.

      Lưu ý rằng định dạng này yêu cầu một đối số ``int``. Không giống như hầu hết các ngữ cảnh khác trong C, các đối số biến thiên không được tự động chuyển đổi sang kiểu phù hợp. Bạn có thể chuyển đổi một kiểu khác (ví dụ: một con trỏ hoặc một số thực) thành một giá trị ``int`` phù hợp bằng cách sử dụng ``(x) ? 1 : 0`` hoặc ``!!x``.

      .. versionadded:: 3.14

   ``c`` (:class:`bytes` có độ dài 1) [char]
      Chuyển đổi một :c:expr:`int` trong C đại diện cho một byte thành một đối tượng :class:`bytes` trong Python có độ dài 1.

   ``C`` (:class:`str` có độ dài 1) [int]
      Chuyển đổi một :c:expr:`int` trong C đại diện cho một ký tự thành một đối tượng :class:`str` trong Python có độ dài 1.

   ``d`` (:class:`float`) [double]
      Chuyển đổi một :c:expr:`double` trong C thành một số dấu phẩy động trong Python.

   ``f`` (:class:`float`) [float]
      Chuyển đổi một :c:expr:`float` trong C thành một số dấu phẩy động Python.

   ``D`` (:class:`complex`) [Py_complex \*]
      Chuyển đổi một cấu trúc :c:type:`Py_complex` trong C thành một số phức Python.

   ``O`` (object) [PyObject \*]
      Truyền nguyên trạng một đối tượng Python nhưng tạo mới một
      :term:`strong reference` cho nó (tức là số lượng tham chiếu của nó được tăng thêm một). Nếu đối tượng được truyền vào là một con trỏ ``NULL``, giả định là điều này xảy ra vì lời gọi tạo ra đối số đã phát hiện lỗi và đặt một exception. Do đó, :c:func:`Py_BuildValue` sẽ trả về ``NULL`` nhưng sẽ không phát sinh exception. Nếu chưa có exception nào được phát sinh, :exc:`SystemError` được đặt.

   ``S`` (object) [PyObject \*]
      Giống như ``O``.

   ``N`` (đối tượng) [PyObject \*]
      Giống như ``O``, ngoại trừ việc nó không tạo một :term:`strong reference` mới. Hữu ích khi đối tượng được tạo bằng một lệnh gọi đến hàm khởi tạo đối tượng trong danh sách đối số.

   ``O&`` (đối tượng) [*bộ chuyển đổi*, *bất kỳ*]
      Chuyển đổi *bất kỳ* thành một đối tượng Python thông qua hàm *bộ chuyển đổi*. Hàm này được gọi với *bất kỳ* (phải tương thích với :c:expr:`void*`) làm đối số và phải trả về một đối tượng Python "mới", hoặc ``NULL`` nếu xảy ra lỗi.

   ``(items)`` (:class:`tuple`) [*các mục khớp*]
      Chuyển đổi một chuỗi các giá trị C thành một tuple Python có cùng số lượng mục.

   ``[items]`` (:class:`list`) [*matching-items*]
      Chuyển đổi một chuỗi các giá trị C thành một danh sách Python có cùng số lượng phần tử.

   ``{items}`` (:class:`dict`) [*matching-items*]
      Chuyển đổi một chuỗi các giá trị C thành một từ điển Python. Mỗi cặp giá trị C liên tiếp sẽ thêm một phần tử vào từ điển, lần lượt đóng vai trò là khóa và giá trị.

   Nếu có lỗi trong chuỗi định dạng, ngoại lệ :exc:`SystemError` sẽ được thiết lập và ``NULL`` được trả về.

.. c:function:: PyObject* Py_VaBuildValue(const char *format, va_list vargs)

   Tương tự như :c:func:`Py_BuildValue`, ngoại trừ việc hàm này nhận một va_list thay vì một số lượng đối số thay đổi.
