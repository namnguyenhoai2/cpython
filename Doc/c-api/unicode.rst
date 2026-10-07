.. highlight:: c

.. _unicodeobjects:

Đối tượng Unicode và Codec
--------------------------

.. sectionauthor:: Marc-André Lemburg <mal@lemburg.com>
.. sectionauthor:: Georg Brandl <georg@python.org>

Đối tượng Unicode
^^^^^^^^^^^^^^^^^

Kể từ khi triển khai :pep:`393` trong Python 3.3, các đối tượng Unicode sử dụng nhiều dạng biểu diễn khác nhau ở bên trong, nhằm cho phép xử lý toàn bộ phạm vi ký tự Unicode mà vẫn tiết kiệm bộ nhớ. Có các trường hợp đặc biệt dành cho những chuỗi trong đó tất cả điểm mã đều nhỏ hơn 128, 256 hoặc 65536; nếu không, các điểm mã phải nhỏ hơn 1114112 (là toàn bộ phạm vi Unicode).

Biểu diễn UTF-8 được tạo theo yêu cầu và được lưu trong bộ nhớ đệm của đối tượng Unicode.

.. note::
   Biểu diễn :c:type:`Py_UNICODE` đã bị loại bỏ kể từ Python 3.12 cùng với các API đã deprecated. Xem :pep:`623` để biết thêm thông tin.


Kiểu Unicode
""""""""""""

Đây là các kiểu đối tượng Unicode cơ bản được sử dụng cho việc triển khai Unicode trong Python:

.. c:var:: PyTypeObject PyUnicode_Type

   Đối tượng này của :c:type:`PyTypeObject` đại diện cho kiểu Unicode của Python. Nó được cung cấp cho mã Python dưới dạng :py:class:`str`.


.. c:var:: PyTypeObject PyUnicodeIter_Type

   Đối tượng này của :c:type:`PyTypeObject` đại diện cho kiểu iterator Unicode của Python. Nó được dùng để lặp qua các đối tượng chuỗi Unicode.


.. c:type:: Py_UCS4
            Py_UCS2 Py_UCS1

   Các kiểu này là những typedef cho các kiểu số nguyên không dấu đủ rộng để chứa lần lượt các ký tự có độ dài 32 bit, 16 bit và 8 bit. Khi làm việc với các ký tự Unicode riêng lẻ, hãy sử dụng :c:type:`Py_UCS4`.

   .. versionadded:: 3.3


.. c:type:: PyASCIIObject
            PyCompactUnicodeObject PyUnicodeObject

   Các kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng Unicode của Python. Trong hầu hết các trường hợp, không nên sử dụng trực tiếp chúng, vì tất cả các hàm API làm việc với đối tượng Unicode đều nhận và trả về các con trỏ :c:type:`PyObject`.

   .. versionadded:: 3.3


   Có thể xác định cấu trúc của một đối tượng cụ thể bằng các macro sau. Các macro này không thể thất bại; hành vi của chúng không được xác định nếu đối số không phải là một đối tượng Unicode của Python.

   .. c:namespace:: NULL

   .. c:macro:: PyUnicode_IS_COMPACT(o)

      Đúng nếu *o* sử dụng cấu trúc :c:struct:`PyCompactUnicodeObject`.

      .. versionadded:: 3.3


   .. c:macro:: PyUnicode_IS_COMPACT_ASCII(o)

      Đúng nếu *o* sử dụng cấu trúc :c:struct:`PyASCIIObject`.

      .. versionadded:: 3.3


Các API sau đây là các macro C và hàm được inline tĩnh để kiểm tra nhanh và truy cập dữ liệu chỉ đọc nội bộ của các đối tượng Unicode:

.. c:function:: int PyUnicode_Check(PyObject *obj)

   Trả về true nếu đối tượng *obj* là một đối tượng Unicode hoặc một instance của kiểu con Unicode. Hàm này luôn thực hiện thành công.


.. c:function:: int PyUnicode_CheckExact(PyObject *obj)

   Trả về true nếu đối tượng *obj* là một đối tượng Unicode, nhưng không phải là một instance của kiểu con. Hàm này luôn thực hiện thành công.


.. c:function:: Py_ssize_t PyUnicode_GET_LENGTH(PyObject *unicode)

   Trả về độ dài của chuỗi Unicode, tính theo code point. *unicode* phải là một đối tượng Unicode ở dạng biểu diễn "canonical" (không được kiểm tra).

   .. versionadded:: 3.3


.. c:function:: Py_UCS1* PyUnicode_1BYTE_DATA(PyObject *unicode)
                Py_UCS2* PyUnicode_2BYTE_DATA(PyObject *unicode) Py_UCS4* PyUnicode_4BYTE_DATA(PyObject *unicode)

   Trả về một con trỏ đến biểu diễn chuẩn được chuyển kiểu thành các kiểu số nguyên UCS1, UCS2 hoặc UCS4 để truy cập ký tự trực tiếp. Không thực hiện kiểm tra nếu biểu diễn chuẩn có kích thước ký tự chính xác; hãy sử dụng
   :c:func:`PyUnicode_KIND` để chọn hàm phù hợp.

   .. versionadded:: 3.3


.. c:macro:: PyUnicode_1BYTE_KIND
             PyUnicode_2BYTE_KIND PyUnicode_4BYTE_KIND

   Trả về các giá trị của macro :c:func:`PyUnicode_KIND`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.12
      ``PyUnicode_WCHAR_KIND`` đã bị loại bỏ.


.. c:function:: int PyUnicode_KIND(PyObject *unicode)

   Trả về một trong các hằng số kind của PyUnicode (xem ở trên), cho biết đối tượng Unicode này sử dụng bao nhiêu byte cho mỗi ký tự để lưu trữ dữ liệu. *unicode* phải là một đối tượng Unicode ở dạng biểu diễn "chuẩn" (không kiểm tra).

   .. versionadded:: 3.3


.. c:function:: void* PyUnicode_DATA(PyObject *unicode)

   Trả về một con trỏ void đến bộ đệm Unicode thô. *unicode* phải là một đối tượng Unicode ở dạng biểu diễn "chuẩn" (không kiểm tra).

   .. versionadded:: 3.3


.. c:function:: void PyUnicode_WRITE(int kind, void *data, \
                                     Py_ssize_t index, Py_UCS4 value)

   Ghi code point *value* vào *index* đã cho, tính từ 0, trong một chuỗi.

   Giá trị *kind* và con trỏ *data* tương ứng phải được lấy từ một chuỗi bằng :c:func:`PyUnicode_KIND` và :c:func:`PyUnicode_DATA`. Bạn phải giữ một tham chiếu đến chuỗi đó trong khi gọi
   :c:func:`!PyUnicode_WRITE`. Tất cả các yêu cầu của
   :c:func:`PyUnicode_WriteChar` cũng được áp dụng.

   Hàm không kiểm tra bất kỳ yêu cầu nào trong số này và được thiết kế để sử dụng trong các vòng lặp.

   .. versionadded:: 3.3


.. c:function:: Py_UCS4 PyUnicode_READ(int kind, void *data, \
                                       Py_ssize_t index)

   Đọc một code point từ biểu diễn chuẩn *data* (như thu được bằng
   :c:func:`PyUnicode_DATA`). Không thực hiện kiểm tra hoặc gọi các hàm ready.

   .. versionadded:: 3.3


.. c:function:: Py_UCS4 PyUnicode_READ_CHAR(PyObject *unicode, Py_ssize_t index)

   Đọc một ký tự từ đối tượng Unicode *unicode*, đối tượng này phải ở dạng biểu diễn "canonical". Cách này kém hiệu quả hơn :c:func:`PyUnicode_READ` nếu bạn thực hiện nhiều lần đọc liên tiếp.

   .. versionadded:: 3.3


.. c:function:: Py_UCS4 PyUnicode_MAX_CHAR_VALUE(PyObject *unicode)

   Trả về code point lớn nhất phù hợp để tạo một chuỗi khác dựa trên *unicode*, đối tượng này phải ở dạng biểu diễn "canonical". Kết quả luôn chỉ là giá trị xấp xỉ nhưng hiệu quả hơn so với việc lặp qua chuỗi.

   .. versionadded:: 3.3


.. c:function:: int PyUnicode_IsIdentifier(PyObject *unicode)

   Trả về ``1`` nếu chuỗi là một identifier hợp lệ theo định nghĩa ngôn ngữ, mục :ref:`identifiers`. Nếu không, trả về ``0``.

   .. versionchanged:: 3.9
      Hàm không còn gọi :c:func:`Py_FatalError` nếu chuỗi chưa sẵn sàng.


.. c:function:: unsigned int PyUnicode_IS_ASCII(PyObject *unicode)

   Trả về true nếu chuỗi chỉ chứa các ký tự ASCII. Tương đương với :py:meth:`str.isascii`.

   .. versionadded:: 3.2


Các thuộc tính ký tự Unicode
""""""""""""""""""""""""""""

Unicode cung cấp nhiều thuộc tính ký tự khác nhau. Những thuộc tính thường cần dùng nhất có sẵn thông qua các macro này, được ánh xạ tới các hàm C tùy thuộc vào cấu hình Python.


.. c:function:: int Py_UNICODE_ISSPACE(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự khoảng trắng hay không.


.. c:function:: int Py_UNICODE_ISLOWER(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự chữ thường hay không.


.. c:function:: int Py_UNICODE_ISUPPER(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự chữ hoa hay không.


.. c:function:: int Py_UNICODE_ISTITLE(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự viết hoa đầu câu hay không.


.. c:function:: int Py_UNICODE_ISLINEBREAK(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự ngắt dòng hay không.


.. c:function:: int Py_UNICODE_ISDECIMAL(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự thập phân hay không.


.. c:function:: int Py_UNICODE_ISDIGIT(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự chữ số hay không.


.. c:function:: int Py_UNICODE_ISNUMERIC(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự số hay không.


.. c:function:: int Py_UNICODE_ISALPHA(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự chữ cái hay không.


.. c:function:: int Py_UNICODE_ISALNUM(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự chữ và số hay không.


.. c:function:: int Py_UNICODE_ISPRINTABLE(Py_UCS4 ch)

   Trả về ``1`` hoặc ``0`` tùy thuộc vào việc *ch* có phải là ký tự in được theo nghĩa của :meth:`str.isprintable` hay không.


Các API này có thể được sử dụng để chuyển đổi ký tự trực tiếp nhanh chóng:


.. c:function:: Py_UCS4 Py_UNICODE_TOLOWER(Py_UCS4 ch)

   Trả về ký tự *ch* được chuyển thành chữ thường.


.. c:function:: Py_UCS4 Py_UNICODE_TOUPPER(Py_UCS4 ch)

   Trả về ký tự *ch* được chuyển thành chữ hoa.


.. c:function:: Py_UCS4 Py_UNICODE_TOTITLE(Py_UCS4 ch)

   Trả về ký tự *ch* được chuyển thành kiểu viết hoa chữ cái đầu.


.. c:function:: int Py_UNICODE_TODECIMAL(Py_UCS4 ch)

   Trả về ký tự *ch* được chuyển thành một số nguyên dương thập phân. Trả về ``-1`` nếu không thể thực hiện việc này. Hàm này không phát sinh ngoại lệ.


.. c:function:: int Py_UNICODE_TODIGIT(Py_UCS4 ch)

   Trả về ký tự *ch* được chuyển thành một số nguyên có một chữ số. Trả về ``-1`` nếu không thể thực hiện việc này. Hàm này không phát sinh ngoại lệ.


.. c:function:: double Py_UNICODE_TONUMERIC(Py_UCS4 ch)

   Trả về ký tự *ch* được chuyển thành một số double. Trả về ``-1.0`` nếu không thể thực hiện việc này. Hàm này không phát sinh ngoại lệ.


Có thể sử dụng các API này để làm việc với surrogate:

.. c:function:: int Py_UNICODE_IS_SURROGATE(Py_UCS4 ch)

   Kiểm tra xem *ch* có phải là một surrogate (``0xD800 <= ch <= 0xDFFF``) hay không.

.. c:function:: int Py_UNICODE_IS_HIGH_SURROGATE(Py_UCS4 ch)

   Kiểm tra xem *ch* có phải là một high surrogate (``0xD800 <= ch <= 0xDBFF``) hay không.

.. c:function:: int Py_UNICODE_IS_LOW_SURROGATE(Py_UCS4 ch)

   Kiểm tra xem *ch* có phải là một low surrogate (``0xDC00 <= ch <= 0xDFFF``) hay không.

.. c:function:: Py_UCS4 Py_UNICODE_HIGH_SURROGATE(Py_UCS4 ch)

    Trả về high UTF-16 surrogate (``0xD800`` đến ``0xDBFF``) cho một điểm mã Unicode trong phạm vi ``[0x10000; 0x10FFFF]``.

.. c:function:: Py_UCS4 Py_UNICODE_LOW_SURROGATE(Py_UCS4 ch)

    Trả về low UTF-16 surrogate (``0xDC00`` đến ``0xDFFF``) cho một điểm mã Unicode trong phạm vi ``[0x10000; 0x10FFFF]``.

.. c:function:: Py_UCS4 Py_UNICODE_JOIN_SURROGATES(Py_UCS4 high, Py_UCS4 low)

   Nối hai điểm mã surrogate và trả về một giá trị :c:type:`Py_UCS4` duy nhất. *high* và *low* lần lượt là surrogate đứng đầu và đứng cuối trong một cặp surrogate. *high* phải nằm trong phạm vi ``[0xD800; 0xDBFF]`` và *low* phải nằm trong phạm vi ``[0xDC00; 0xDFFF]``.


Tạo và truy cập các chuỗi Unicode
"""""""""""""""""""""""""""""""""

Để tạo các đối tượng Unicode và truy cập các thuộc tính sequence cơ bản của chúng, hãy sử dụng các API sau:

.. c:function:: PyObject* PyUnicode_New(Py_ssize_t size, Py_UCS4 maxchar)

   Tạo một đối tượng Unicode mới. *maxchar* phải là code point tối đa thực sự sẽ được đặt vào chuỗi. Để ước lượng, có thể làm tròn lên giá trị gần nhất trong dãy 127, 255, 65535, 1114111.

   Khi xảy ra lỗi, hãy đặt một exception và trả về ``NULL``.

   Sau khi được tạo, chuỗi có thể được điền bằng :c:func:`PyUnicode_WriteChar`,
   :c:func:`PyUnicode_CopyCharacters`, :c:func:`PyUnicode_Fill`,
   :c:func:`PyUnicode_WRITE` hoặc tương tự. Vì chuỗi được cho là immutable, hãy cẩn thận không “sử dụng” kết quả trong khi nó đang được sửa đổi. Cụ thể, trước khi được điền nội dung cuối cùng, một chuỗi:

   - không được hash,
   - không được :c:func:`converted to UTF-8 <PyUnicode_AsUTF8AndSize>`, hoặc chuyển đổi sang một biểu diễn không phải là “canonical” khác,
   - không được thay đổi số lượng tham chiếu của nó,
   - không được chia sẻ với mã có thể thực hiện một trong các thao tác trên.

   Danh sách này chưa đầy đủ. Bạn có trách nhiệm tránh những cách sử dụng này; Python không phải lúc nào cũng kiểm tra các yêu cầu này.

   Để tránh vô tình để lộ một đối tượng chuỗi mới chỉ được ghi một phần, hãy ưu tiên sử dụng API :c:type:`PyUnicodeWriter`, hoặc một trong các hàm ``PyUnicode_From*`` dưới đây.


   .. versionadded:: 3.3


.. c:function:: PyObject* PyUnicode_FromKindAndData(int kind, const void *buffer, \
                                                    Py_ssize_t size)

   Tạo một đối tượng Unicode mới với *kind* đã cho (các giá trị có thể là
   :c:macro:`PyUnicode_1BYTE_KIND` v.v., như được trả về bởi
   :c:func:`PyUnicode_KIND`). *buffer* phải trỏ đến một mảng gồm *size* đơn vị, với 1, 2 hoặc 4 byte cho mỗi ký tự, tùy theo kind.

   Nếu cần, *buffer* đầu vào sẽ được sao chép và chuyển đổi thành biểu diễn chuẩn. Ví dụ: nếu *buffer* là một chuỗi UCS4 (:c:macro:`PyUnicode_4BYTE_KIND`) và chỉ gồm các codepoint trong phạm vi UCS1, nó sẽ được chuyển đổi thành UCS1 (:c:macro:`PyUnicode_1BYTE_KIND`).

   .. versionadded:: 3.3


.. c:function:: PyObject* PyUnicode_FromStringAndSize(const char *str, Py_ssize_t size)

   Tạo một đối tượng Unicode từ bộ đệm char *str*. Các byte sẽ được diễn giải là được mã hóa theo UTF-8. Bộ đệm được sao chép vào đối tượng mới. Giá trị trả về có thể là một đối tượng dùng chung, tức là không được phép sửa đổi dữ liệu.

   Hàm này phát sinh :exc:`SystemError` khi:

   * *size* < 0,
   * *str* là ``NULL`` và *size* > 0

   .. versionchanged:: 3.12
      *str* == ``NULL`` với *size* > 0 không còn được phép nữa.


.. c:function:: PyObject *PyUnicode_FromString(const char *str)

   Tạo một đối tượng Unicode từ bộ đệm ký tự kết thúc bằng null được mã hóa UTF-8 *str*.


.. c:function:: PyObject* PyUnicode_FromFormat(const char *format, ...)

   Nhận một chuỗi kiểu C :c:func:`printf`\ -style *format* và một số lượng đối số thay đổi, tính kích thước của chuỗi Unicode Python kết quả rồi trả về một chuỗi có các giá trị được định dạng trong đó. Các đối số thay đổi phải là kiểu C và phải tương ứng chính xác với các ký tự định dạng trong chuỗi được mã hóa ASCII *format*.

   Một conversion specifier chứa từ hai ký tự trở lên và có các thành phần sau, phải xuất hiện theo thứ tự này:

   #. Ký tự ``'%'``, đánh dấu phần bắt đầu của specifier.

   #. Các cờ chuyển đổi (tùy chọn), ảnh hưởng đến kết quả của một số kiểu chuyển đổi.

   #. Độ rộng trường tối thiểu (tùy chọn). Nếu được chỉ định là ``'*'`` (dấu hoa thị), độ rộng thực tế được lấy từ đối số tiếp theo, đối số này phải có kiểu :c:expr:`int`, và đối tượng cần chuyển đổi nằm sau độ rộng trường tối thiểu và độ chính xác tùy chọn.

   #. Độ chính xác (tùy chọn), được chỉ định bằng ``'.'`` (dấu chấm) theo sau là độ chính xác. Nếu được chỉ định là ``'*'`` (dấu hoa thị), độ chính xác thực tế được lấy từ đối số tiếp theo, đối số này phải có kiểu :c:expr:`int`, và giá trị cần chuyển đổi nằm sau độ chính xác.

   #. Bộ điều chỉnh độ dài (tùy chọn).

   #. Kiểu chuyển đổi.

   Các ký tự cờ chuyển đổi là:

   .. tabularcolumns:: |l|L|

   +-------+---------------------------------------------------------------------------------+
   | Cờ    | Ý nghĩa                                                                         |
   +=======+=================================================================================+
   | ``0`` | Giá trị chuyển đổi sẽ được đệm bằng số 0 đối với các giá trị số.                |
   +-------+---------------------------------------------------------------------------------+
   | ``-`` | Giá trị đã chuyển đổi được căn trái (ghi đè cờ ``0`` nếu cả hai được cung cấp). |
   +-------+---------------------------------------------------------------------------------+

   Các length modifier cho những phép chuyển đổi số nguyên sau (``d``, ``i``, ``o``, ``u``, ``x`` hoặc ``X``) xác định kiểu của đối số (:c:expr:`int` theo mặc định):

   .. tabularcolumns:: |l|L|

   +----------+-------------------------------------------------------+
   | Modifier | Types                                                 |
   +==========+=======================================================+
   | ``l``    | :c:expr:`long` hoặc :c:expr:`unsigned long`           |
   +----------+-------------------------------------------------------+
   | ``ll``   | :c:expr:`long long` hoặc :c:expr:`unsigned long long` |
   +----------+-------------------------------------------------------+
   | ``j``    | :c:type:`intmax_t` hoặc :c:type:`uintmax_t`           |
   +----------+-------------------------------------------------------+
   | ``z``    | :c:type:`size_t` hoặc :c:type:`ssize_t`               |
   +----------+-------------------------------------------------------+
   | ``t``    | :c:type:`ptrdiff_t`                                   |
   +----------+-------------------------------------------------------+

   Bộ bổ nghĩa độ dài ``l`` cho các phép chuyển đổi sau đây, ``s`` hoặc ``V``, chỉ rõ rằng kiểu của đối số là :c:expr:`const wchar_t*`.

   Các bộ chỉ định chuyển đổi là:

   .. list-table::
      :widths: auto
      :header-rows: 1

      * - Bộ chỉ định chuyển đổi
        - Kiểu
        - Chú thích

      * - ``%``
        - *n/a*
        - Ký tự ``%`` theo nghĩa đen.

      * - ``d``, ``i``
        - Được chỉ định bởi bộ bổ nghĩa độ dài
        - Biểu diễn thập phân của một số nguyên C có dấu.

      * - ``u``
        - Được chỉ định bởi bộ bổ nghĩa độ dài
        - Biểu diễn thập phân của một số nguyên C không dấu.

      * - ``o``
        - Được chỉ định bởi bộ bổ nghĩa độ dài
        - Biểu diễn bát phân của một số nguyên C không dấu.

      * - ``x``
        - Được chỉ định bởi bộ bổ nghĩa độ dài
        - Biểu diễn thập lục phân của một số nguyên C không dấu (chữ thường).

      * - ``X``
        - Được chỉ định bởi bộ bổ nghĩa độ dài
        - Biểu diễn thập lục phân của một số nguyên C không dấu (chữ hoa).

      * - ``c``
        - :c:expr:`int`
        - Một ký tự đơn.

      * - ``s``
        - :c:expr:`const char*` hoặc :c:expr:`const wchar_t*`
        - Một mảng ký tự C kết thúc bằng null.

      * - ``p``
        - :c:expr:`const void*`
        - Biểu diễn thập lục phân của một con trỏ C. Phần lớn tương đương với ``printf("%p")``, ngoại trừ việc nó được đảm bảo bắt đầu bằng chuỗi ký tự ``0x`` bất kể ``printf`` của nền tảng trả về giá trị gì.

      * - ``A``
        - :c:expr:`PyObject*`
        - Kết quả của việc gọi :func:`ascii`.

      * - ``U``
        - :c:expr:`PyObject*`
        - Một đối tượng Unicode.

      * - ``V``
        - :c:expr:`PyObject*`, :c:expr:`const char*` hoặc :c:expr:`const wchar_t*`
        - Một đối tượng Unicode (có thể là ``NULL``) và một mảng ký tự C kết thúc bằng null làm tham số thứ hai (sẽ được sử dụng nếu tham số thứ nhất là ``NULL``).

      * - ``S``
        - :c:expr:`PyObject*`
        - Kết quả của việc gọi :c:func:`PyObject_Str`.

      * - ``R``
        - :c:expr:`PyObject*`
        - Kết quả của việc gọi :c:func:`PyObject_Repr`.

      * - ``T``
        - :c:expr:`PyObject*`
        - Lấy tên đầy đủ của một kiểu đối tượng; gọi :c:func:`PyType_GetFullyQualifiedName`.

      * - ``#T``
        - :c:expr:`PyObject*`
        - Tương tự định dạng ``T``, nhưng sử dụng dấu hai chấm (``:``) làm dấu phân cách giữa tên module và tên đủ điều kiện.

      * - ``N``
        - :c:expr:`PyTypeObject*`
        - Lấy tên đủ điều kiện của một kiểu; gọi :c:func:`PyType_GetFullyQualifiedName`.

      * - ``#N``
        - :c:expr:`PyTypeObject*`
        - Tương tự định dạng ``N``, nhưng sử dụng dấu hai chấm (``:``) làm dấu phân cách giữa tên module và tên đủ điều kiện.

   .. note::
      Đơn vị của formatter độ rộng là số ký tự thay vì số byte. Đơn vị của formatter độ chính xác là số byte hoặc số mục :c:type:`wchar_t` (nếu sử dụng modifier độ dài ``l``) cho ``"%s"`` và ``"%V"`` (nếu đối số ``PyObject*`` là ``NULL``), và là số ký tự cho ``"%A"``, ``"%U"``, ``"%S"``, ``"%R"`` và ``"%V"`` (nếu đối số ``PyObject*`` không phải là ``NULL``).

   .. note::
      Không giống như trong C :c:func:`printf` cờ ``0`` vẫn có tác dụng ngay cả khi độ chính xác được chỉ định cho các phép chuyển đổi số nguyên (``d``, ``i``, ``u``, ``o``, ``x`` hoặc ``X``).

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ cho ``"%lld"`` và ``"%llu"``.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ cho ``"%li"``, ``"%lli"`` và ``"%zi"``.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ bộ định dạng width và precision cho ``"%s"``, ``"%A"``, ``"%U"``, ``"%V"``, ``"%S"``, ``"%R"``.

   .. versionchanged:: 3.12
      Hỗ trợ các conversion specifier ``o`` và ``X``. Hỗ trợ các length modifier ``j`` và ``t``. Length modifier hiện được áp dụng cho tất cả các phép chuyển đổi số nguyên. Length modifier ``l`` hiện được áp dụng cho các conversion specifier ``s`` và ``V``. Hỗ trợ width và precision biến đổi ``*``. Hỗ trợ flag ``-``.

      Ký tự định dạng không được nhận dạng hiện đặt một :exc:`SystemError`. Trong các phiên bản trước, ký tự này khiến toàn bộ phần còn lại của format string được sao chép nguyên trạng vào chuỗi kết quả và mọi đối số bổ sung đều bị loại bỏ.

   .. versionchanged:: 3.13
      Đã bổ sung hỗ trợ các định dạng ``%T``, ``%#T``, ``%N`` và ``%#N``.


.. c:function:: PyObject* PyUnicode_FromFormatV(const char *format, va_list vargs)

   Giống hệt :c:func:`PyUnicode_FromFormat`, ngoại trừ việc nó nhận chính xác hai đối số.


.. c:function:: PyObject* PyUnicode_FromObject(PyObject *obj)

   Sao chép một instance của Unicode subtype sang một đối tượng Unicode thực mới nếu cần. Nếu *obj* đã là một đối tượng Unicode thực (không phải subtype), trả về một :term:`strong reference` mới cho đối tượng đó.

   Các đối tượng không phải Unicode hoặc subtype của Unicode sẽ gây ra một :exc:`TypeError`.


.. c:function:: PyObject* PyUnicode_FromOrdinal(int ordinal)

   Tạo một Đối tượng Unicode từ điểm mã Unicode đã cho *ordinal*.

   Giá trị ordinal phải nằm trong ``range(0x110000)``. Một :exc:`ValueError` sẽ được phát sinh nếu không.


.. c:function:: PyObject* PyUnicode_FromEncodedObject(PyObject *obj, \
                               const char *encoding, const char *errors)

   Giải mã một đối tượng đã mã hóa *obj* thành một đối tượng Unicode.

   :class:`bytes`, :class:`bytearray` và các đối tượng khác
   Các :term:`bytes-like objects <bytes-like object>` được giải mã theo *encoding* đã cho và sử dụng cơ chế xử lý lỗi được định nghĩa bởi *errors*. Cả hai có thể là ``NULL`` để giao diện sử dụng các giá trị mặc định (xem :ref:`builtincodecs` để biết chi tiết).

   Tất cả các đối tượng khác, bao gồm cả các đối tượng Unicode, sẽ khiến một :exc:`TypeError` được thiết lập.

   API trả về ``NULL`` nếu xảy ra lỗi. Bên gọi chịu trách nhiệm giảm đếm tham chiếu cho các đối tượng được trả về.


.. c:function:: void PyUnicode_Append(PyObject **p_left, PyObject *right)

   Nối chuỗi *right* vào cuối *p_left*. *p_left* phải trỏ đến một :term:`strong reference` tới một đối tượng Unicode;
   :c:func:`!PyUnicode_Append` giải phóng (":term:`steals <steal>`") tham chiếu này.

   Khi xảy ra lỗi, đặt *\*p_left* thành ``NULL`` và đặt một exception.

   Khi thành công, đặt *\*p_left* thành một tham chiếu mạnh mới đến kết quả.


.. c:function:: void PyUnicode_AppendAndDel(PyObject **p_left, PyObject *right)

   Hàm này tương tự :c:func:`PyUnicode_Append`, điểm khác biệt duy nhất là nó giảm số lượng tham chiếu của *right* đi một.


.. c:function:: PyObject* PyUnicode_BuildEncodingMap(PyObject* string)

   Trả về một ánh xạ thích hợp để giải mã một encoding một byte tùy chỉnh. Với một chuỗi Unicode *string* có tối đa 256 ký tự biểu diễn một bảng encoding, hàm này trả về một đối tượng ánh xạ nội bộ nhỏ gọn hoặc một từ điển ánh xạ số thứ tự ký tự tới các giá trị byte. Phát sinh một :exc:`TypeError` và trả về ``NULL`` nếu đầu vào không hợp lệ.

   .. versionadded:: 3.2


.. c:function:: const char* PyUnicode_GetDefaultEncoding(void)

   Trả về tên của encoding chuỗi mặc định, ``"utf-8"``. Xem :func:`sys.getdefaultencoding`.

   Chuỗi được trả về không cần được giải phóng và vẫn hợp lệ cho đến khi trình thông dịch tắt.


.. c:function:: Py_ssize_t PyUnicode_GetLength(PyObject *unicode)

   Trả về độ dài của đối tượng Unicode, tính theo điểm mã.

   Khi xảy ra lỗi, đặt một exception và trả về ``-1``.

   .. versionadded:: 3.3


.. c:function:: Py_ssize_t PyUnicode_CopyCharacters(PyObject *to, \
                                                    Py_ssize_t to_start, \ PyObject *from, \ Py_ssize_t from_start, \ Py_ssize_t how_many)

   Sao chép các ký tự từ một đối tượng Unicode sang một đối tượng khác. Hàm này thực hiện chuyển đổi ký tự khi cần thiết và chuyển sang :c:func:`!memcpy` nếu có thể. Trả về ``-1`` và đặt một exception khi xảy ra lỗi; nếu không, trả về số ký tự đã sao chép.

   Chuỗi chưa được “sử dụng”. Xem :c:func:`PyUnicode_New` để biết chi tiết.

   .. versionadded:: 3.3


.. c:function:: int PyUnicode_Resize(PyObject **unicode, Py_ssize_t length);

   Đổi kích thước một đối tượng Unicode *\*unicode* thành *length* mới theo các code point.

   Hãy thử đổi kích thước chuỗi tại chỗ (thường nhanh hơn việc cấp phát một chuỗi mới và sao chép các ký tự), hoặc tạo một chuỗi mới.

   *\*unicode* được sửa đổi để trỏ đến đối tượng mới (đã đổi kích thước), và ``0`` được trả về khi thành công. Nếu không, ``-1`` được trả về và một exception được thiết lập, còn *\*unicode* không bị thay đổi.

   Hàm này không kiểm tra nội dung chuỗi, vì vậy kết quả có thể không phải là chuỗi ở dạng biểu diễn chuẩn.


.. c:function:: Py_ssize_t PyUnicode_Fill(PyObject *unicode, Py_ssize_t start, \
                        Py_ssize_t length, Py_UCS4 fill_char)

   Điền một chuỗi bằng một ký tự: ghi *fill_char* vào ``unicode[start:start+length]``.

   Không thành công nếu *fill_char* lớn hơn ký tự lớn nhất của chuỗi hoặc nếu chuỗi có nhiều hơn 1 tham chiếu.

   Chuỗi chưa được “sử dụng”. Xem :c:func:`PyUnicode_New` để biết chi tiết.

   Trả về số ký tự đã ghi hoặc trả về ``-1`` và phát sinh một ngoại lệ khi có lỗi.

   .. versionadded:: 3.3


.. c:function:: int PyUnicode_WriteChar(PyObject *unicode, Py_ssize_t index, \
                                        ký tự Py_UCS4)

   Ghi một ký tự *character* vào chuỗi *unicode* tại *index* bắt đầu từ 0. Trả về ``0`` khi thành công và ``-1`` khi có lỗi, đồng thời đặt một ngoại lệ.

   Hàm này kiểm tra rằng *unicode* là một đối tượng Unicode, chỉ mục không nằm ngoài phạm vi và số lượng tham chiếu của đối tượng là một. Xem :c:func:`PyUnicode_WRITE` để biết phiên bản bỏ qua các kiểm tra này, qua đó bạn phải tự chịu trách nhiệm thực hiện chúng.

   Chuỗi chưa được “sử dụng”. Xem :c:func:`PyUnicode_New` để biết chi tiết.

   .. versionadded:: 3.3


.. c:function:: Py_UCS4 PyUnicode_ReadChar(PyObject *unicode, Py_ssize_t index)

   Đọc một ký tự từ chuỗi. Hàm này kiểm tra rằng *unicode* là một đối tượng Unicode và chỉ mục không nằm ngoài phạm vi, trái với
   :c:func:`PyUnicode_READ_CHAR`, không thực hiện kiểm tra lỗi.

   Trả về ký tự nếu thành công, ``-1`` nếu có lỗi kèm theo một exception đã được thiết lập.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyUnicode_Substring(PyObject *unicode, Py_ssize_t start, \
                                              Py_ssize_t end)

   Trả về một chuỗi con của *unicode*, từ chỉ mục ký tự *start* (được bao gồm) đến chỉ mục ký tự *end* (không được bao gồm). Không hỗ trợ chỉ mục âm. Khi có lỗi, thiết lập một exception và trả về ``NULL``.

   .. versionadded:: 3.3


.. c:function:: Py_UCS4* PyUnicode_AsUCS4(PyObject *unicode, Py_UCS4 *buffer, \
                                          Py_ssize_t buflen, int copy_null)

   Sao chép chuỗi *unicode* vào một bộ đệm UCS4, bao gồm một ký tự null nếu *copy_null* được thiết lập. Trả về ``NULL`` và thiết lập một exception khi có lỗi (đặc biệt là một :exc:`SystemError` nếu *buflen* nhỏ hơn độ dài của *unicode*). Trả về *buffer* nếu thành công.

   .. versionadded:: 3.3


.. c:function:: Py_UCS4* PyUnicode_AsUCS4Copy(PyObject *unicode)

   Sao chép chuỗi *unicode* vào một bộ đệm UCS4 mới được cấp phát bằng cách sử dụng
   :c:func:`PyMem_Malloc`. Nếu thao tác này không thành công, ``NULL`` sẽ được trả về cùng với một
   :exc:`MemoryError` được thiết lập. Bộ đệm được trả về luôn có thêm một điểm mã null được nối vào.

   .. versionadded:: 3.3


Mã hóa Locale
"""""""""""""

Có thể sử dụng mã hóa locale hiện tại để giải mã văn bản từ hệ điều hành.

.. c:function:: PyObject* PyUnicode_DecodeLocaleAndSize(const char *str, \
                                                        Py_ssize_t length, \ const char *errors)

   Giải mã một chuỗi từ UTF-8 trên Android và VxWorks, hoặc từ mã hóa locale hiện tại trên các nền tảng khác. Các trình xử lý lỗi được hỗ trợ là ``"strict"`` và ``"surrogateescape"`` (:pep:`383`). Bộ giải mã sử dụng trình xử lý lỗi ``"strict"`` nếu *errors* là ``NULL``. *str* phải kết thúc bằng một ký tự null nhưng không được chứa các ký tự null lồng bên trong.

   Sử dụng :c:func:`PyUnicode_DecodeFSDefaultAndSize` để giải mã một chuỗi từ :term:`filesystem encoding and error handler`.

   Hàm này bỏ qua :ref:`Python UTF-8 Mode <utf8-mode>`.

   .. seealso::

      Hàm :c:func:`Py_DecodeLocale`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.7
      Hàm này hiện cũng sử dụng encoding của locale hiện tại cho ``surrogateescape`` error handler, ngoại trừ trên Android. Trước đây, :c:func:`Py_DecodeLocale` được sử dụng cho ``surrogateescape``, còn encoding của locale hiện tại được sử dụng cho ``strict``.


.. c:function:: PyObject* PyUnicode_DecodeLocale(const char *str, const char *errors)

   Tương tự :c:func:`PyUnicode_DecodeLocaleAndSize`, nhưng tính độ dài chuỗi bằng :c:func:`!strlen`.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyUnicode_EncodeLocale(PyObject *unicode, const char *errors)

   Mã hóa một đối tượng Unicode thành UTF-8 trên Android và VxWorks, hoặc thành encoding của locale hiện tại trên các nền tảng khác. Các error handler được hỗ trợ là ``"strict"`` và ``"surrogateescape"`` (:pep:`383`). Bộ mã hóa sử dụng ``"strict"`` error handler nếu *errors* là ``NULL``. Trả về một đối tượng :class:`bytes`. *unicode* không được chứa các ký tự null nhúng.

   Sử dụng :c:func:`PyUnicode_EncodeFSDefault` để mã hóa một chuỗi thành
   :term:`filesystem encoding and error handler`.

   Hàm này bỏ qua :ref:`Python UTF-8 Mode <utf8-mode>`.

   .. seealso::

      Hàm :c:func:`Py_EncodeLocale`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.7
      Hàm này hiện cũng sử dụng mã hóa locale hiện tại cho trình xử lý lỗi ``surrogateescape``, ngoại trừ trên Android. Trước đây,
      :c:func:`Py_EncodeLocale` được sử dụng cho ``surrogateescape``, còn mã hóa locale hiện tại được sử dụng cho ``strict``.


Mã hóa hệ thống tệp
"""""""""""""""""""

Các hàm mã hóa sang và giải mã từ :term:`filesystem encoding and error handler` (:pep:`383` và :pep:`529`).

Để mã hóa tên tệp thành :class:`bytes` trong quá trình phân tích đối số, nên sử dụng bộ chuyển đổi ``"O&"``, truyền :c:func:`!PyUnicode_FSConverter` làm hàm chuyển đổi:

.. c:function:: int PyUnicode_FSConverter(PyObject* obj, void* result)

   :ref:`PyArg_Parse\* converter <arg-parsing>`: mã hóa các đối tượng :class:`str` -- nhận trực tiếp hoặc thông qua giao diện :class:`os.PathLike` -- thành :class:`bytes` bằng cách sử dụng
   :c:func:`PyUnicode_EncodeFSDefault`; các đối tượng :class:`bytes` được xuất nguyên trạng. *result* phải là địa chỉ của một biến C có kiểu :c:expr:`PyObject*` (hoặc :c:expr:`PyBytesObject*`). Khi thành công, gán cho biến này một :term:`strong reference` mới trỏ đến đối tượng :ref:`byte <bytesobjects>`, đối tượng này phải được giải phóng khi không còn được sử dụng, rồi trả về một giá trị khác không (:c:macro:`Py_CLEANUP_SUPPORTED`). Không cho phép các byte null nằm trong kết quả. Khi thất bại, trả về ``0`` cùng với một ngoại lệ đã được thiết lập.

   Nếu *obj* là ``NULL``, hàm sẽ giải phóng tham chiếu mạnh được lưu trong biến được *result* tham chiếu đến và trả về ``1``.

   .. versionadded:: 3.1

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

Để giải mã tên tệp thành :class:`str` trong quá trình phân tích đối số, nên sử dụng bộ chuyển đổi ``"O&"``, truyền :c:func:`!PyUnicode_FSDecoder` làm hàm chuyển đổi:

.. c:function:: int PyUnicode_FSDecoder(PyObject* obj, void* result)

   :ref:`PyArg_Parse\* converter <arg-parsing>`: giải mã các đối tượng :class:`bytes` -- thu được trực tiếp hoặc gián tiếp thông qua giao diện :class:`os.PathLike` -- thành
   :class:`str` bằng cách sử dụng :c:func:`PyUnicode_DecodeFSDefaultAndSize`; :class:`str` các đối tượng được xuất nguyên trạng. *kết quả* phải là địa chỉ của một biến C thuộc kiểu :c:expr:`PyObject*` (hoặc :c:expr:`PyUnicodeObject*`). Khi thành công, hãy đặt biến này thành một :term:`strong reference` mới trỏ đến một :ref:`đối tượng Unicode <unicodeobjects>` mà phải được giải phóng khi không còn được sử dụng và trả về một giá trị khác không (:c:macro:`Py_CLEANUP_SUPPORTED`). Không cho phép các ký tự null được nhúng trong kết quả. Khi thất bại, trả về ``0`` với một exception đã được thiết lập.

   Nếu *obj* là ``NULL``, giải phóng tham chiếu mạnh đến đối tượng được *result* tham chiếu đến và trả về ``1``.

   .. versionadded:: 3.2

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. c:function:: PyObject* PyUnicode_DecodeFSDefaultAndSize(const char *str, Py_ssize_t size)

   Giải mã một chuỗi từ :term:`filesystem encoding and error handler`.

   Nếu bạn cần giải mã một chuỗi từ encoding của locale hiện tại, hãy sử dụng
   :c:func:`PyUnicode_DecodeLocaleAndSize`.

   .. seealso::

      Hàm :c:func:`Py_DecodeLocale`.

   .. versionchanged:: 3.6
      :term:`bộ xử lý lỗi hệ thống tệp <filesystem encoding and error handler>` hiện được sử dụng.


.. c:function:: PyObject* PyUnicode_DecodeFSDefault(const char *str)

   Giải mã một chuỗi kết thúc bằng null từ :term:`filesystem encoding and error handler`.

   Nếu đã biết độ dài chuỗi, hãy sử dụng
   :c:func:`PyUnicode_DecodeFSDefaultAndSize`.

   .. versionchanged:: 3.6
      :term:`bộ xử lý lỗi hệ thống tệp <filesystem encoding and error handler>` hiện được sử dụng.


.. c:function:: PyObject* PyUnicode_EncodeFSDefault(PyObject *unicode)

   Mã hóa một đối tượng Unicode thành :term:`filesystem encoding and error handler` và trả về :class:`bytes`. Lưu ý rằng đối tượng :class:`bytes` thu được có thể chứa các byte null.

   Nếu bạn cần mã hóa một chuỗi theo encoding của locale hiện tại, hãy sử dụng
   :c:func:`PyUnicode_EncodeLocale`.

   .. seealso::

      hàm :c:func:`Py_EncodeLocale`.

   .. versionadded:: 3.2

   .. versionchanged:: 3.6
      :term:`bộ xử lý lỗi hệ thống tệp <filesystem encoding and error handler>` hiện được sử dụng.

Hỗ trợ wchar_t
""""""""""""""

Hỗ trợ :c:type:`wchar_t` trên các nền tảng hỗ trợ nó:

.. c:function:: PyObject* PyUnicode_FromWideChar(const wchar_t *wstr, Py_ssize_t size)

   Tạo một đối tượng Unicode từ vùng đệm :c:type:`wchar_t` *wstr* có *size* đã cho. Việc truyền ``-1`` vào *size* cho biết hàm phải tự tính độ dài bằng :c:func:`!wcslen`. Trả về ``NULL`` nếu thất bại.


.. c:function:: Py_ssize_t PyUnicode_AsWideChar(PyObject *unicode, wchar_t *wstr, Py_ssize_t size)

   Sao chép nội dung của đối tượng Unicode vào vùng đệm :c:type:`wchar_t` *wstr*. Tối đa *size* :c:type:`wchar_t` ký tự được sao chép (không tính ký tự kết thúc null có thể xuất hiện ở cuối). Trả về số :c:type:`wchar_t` ký tự được sao chép hoặc ``-1`` trong trường hợp xảy ra lỗi.

   Khi *wstr* là ``NULL``, thay vào đó trả về *size* cần thiết để lưu toàn bộ *unicode*, bao gồm cả ký tự kết thúc null.

   Lưu ý rằng chuỗi :c:expr:`wchar_t*` kết quả có thể được kết thúc bằng null hoặc không. Người gọi có trách nhiệm bảo đảm chuỗi :c:expr:`wchar_t*` được kết thúc bằng null nếu ứng dụng yêu cầu. Ngoài ra, lưu ý rằng chuỗi :c:expr:`wchar_t*` có thể chứa các ký tự null, khiến chuỗi bị cắt ngắn khi được sử dụng với hầu hết các hàm C.


.. c:function:: wchar_t* PyUnicode_AsWideCharString(PyObject *unicode, Py_ssize_t *size)

   Chuyển đổi đối tượng Unicode thành chuỗi ký tự wide. Chuỗi đầu ra luôn kết thúc bằng ký tự null. Nếu *size* không phải là ``NULL``, ghi số ký tự wide (không tính ký tự kết thúc null) vào *\*size*. Lưu ý rằng chuỗi :c:type:`wchar_t` kết quả có thể chứa các ký tự null, khiến chuỗi bị cắt ngắn khi được sử dụng với hầu hết các hàm C. Nếu *size* là ``NULL`` và chuỗi :c:expr:`wchar_t*` chứa các ký tự null, một :exc:`ValueError` sẽ được phát sinh.

   Trả về một bộ đệm được :c:macro:`PyMem_New` cấp phát (dùng
   :c:func:`PyMem_Free` để giải phóng bộ đệm đó) khi thành công. Khi xảy ra lỗi, trả về ``NULL`` và *\*size* không được xác định. Phát sinh :exc:`MemoryError` nếu cấp phát bộ nhớ thất bại.

   .. versionadded:: 3.2

   .. versionchanged:: 3.7
      Phát sinh :exc:`ValueError` nếu *size* là ``NULL`` và chuỗi :c:expr:`wchar_t*` chứa các ký tự null.


.. _builtincodecs:

Các codec tích hợp sẵn
^^^^^^^^^^^^^^^^^^^^^^

Python cung cấp một tập hợp các codec tích hợp sẵn được viết bằng C để đạt tốc độ cao. Tất cả các codec này có thể được sử dụng trực tiếp thông qua các hàm sau.

Nhiều API sau đây nhận hai đối số encoding và errors, và chúng có cùng ngữ nghĩa với các đối số của hàm khởi tạo đối tượng chuỗi tích hợp sẵn :func:`str`.

Việc đặt encoding thành ``NULL`` khiến encoding mặc định, là UTF-8, được sử dụng. Các lệnh gọi hệ thống tệp nên sử dụng
:c:func:`PyUnicode_FSConverter` để mã hóa tên tệp. Thành phần này sử dụng
:term:`filesystem encoding and error handler` ở bên trong.

Việc xử lý lỗi được thiết lập bằng errors, tham số này cũng có thể được đặt thành ``NULL`` để sử dụng cách xử lý mặc định được xác định cho codec. Cách xử lý lỗi mặc định cho tất cả codec tích hợp sẵn là "strict" (:exc:`ValueError` được phát sinh).

Tất cả codec đều sử dụng một giao diện tương tự. Để đơn giản, tài liệu chỉ nêu những điểm khác biệt so với các giao diện tổng quát sau đây.


Codec tổng quát
"""""""""""""""

Macro sau được cung cấp:


.. c:macro:: Py_UNICODE_REPLACEMENT_CHARACTER

   Điểm mã Unicode ``U+FFFD`` (ký tự thay thế).

   Ký tự Unicode này được sử dụng làm ký tự thay thế trong quá trình giải mã nếu đối số *errors* được đặt thành "replace".


Đây là các API codec tổng quát:


.. c:function:: PyObject* PyUnicode_Decode(const char *str, Py_ssize_t size, \
                              const char *encoding, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi đã mã hóa *str*. *encoding* và *errors* có cùng ý nghĩa với các tham số cùng tên trong hàm :func:`str` built-in. Codec được sử dụng sẽ được tra cứu bằng registry codec của Python. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_AsEncodedString(PyObject *unicode, \
                              const char *encoding, const char *errors)

   Mã hóa một đối tượng Unicode và trả về kết quả dưới dạng đối tượng bytes của Python. *encoding* và *errors* có cùng ý nghĩa với các tham số cùng tên trong phương thức Unicode :meth:`~str.encode`. Codec được sử dụng sẽ được tra cứu bằng registry codec của Python. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


Codec UTF-8
"""""""""""

Đây là các API codec UTF-8:


.. c:function:: PyObject* PyUnicode_DecodeUTF8(const char *str, Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa UTF-8 *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_DecodeUTF8Stateful(const char *str, Py_ssize_t size, \
                              const char *errors, Py_ssize_t *consumed)

   Nếu *consumed* là ``NULL``, hãy xử lý như :c:func:`PyUnicode_DecodeUTF8`. Nếu *consumed* không phải là ``NULL``, các chuỗi byte UTF-8 chưa hoàn chỉnh ở cuối sẽ không được xem là lỗi. Các byte đó sẽ không được giải mã và số byte đã được giải mã sẽ được lưu trong *consumed*.


.. c:function:: PyObject* PyUnicode_AsUTF8String(PyObject *unicode)

   Mã hóa một đối tượng Unicode bằng UTF-8 và trả về kết quả dưới dạng đối tượng bytes của Python. Việc xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh một ngoại lệ.

   Hàm sẽ thất bại nếu chuỗi chứa các code point surrogate (``U+D800`` - ``U+DFFF``).


.. c:function:: const char* PyUnicode_AsUTF8AndSize(PyObject *unicode, Py_ssize_t *size)

   Trả về một con trỏ đến mã hóa UTF-8 của đối tượng Unicode và lưu kích thước của biểu diễn đã mã hóa (tính bằng byte) vào *size*. Đối số *size* có thể là ``NULL``; trong trường hợp này, không có kích thước nào được lưu. Bộ đệm được trả về luôn có thêm một byte null ở cuối (không được tính trong *size*), bất kể có bất kỳ code point null nào khác hay không.

   Khi xảy ra lỗi, hãy đặt một ngoại lệ, đặt *size* thành ``-1`` (nếu nó không phải là NULL) và trả về ``NULL``.

   Hàm sẽ thất bại nếu chuỗi chứa các code point surrogate (``U+D800`` - ``U+DFFF``).

   Lệnh này lưu bộ nhớ đệm cho biểu diễn UTF-8 của chuỗi trong đối tượng Unicode, và các lần gọi tiếp theo sẽ trả về con trỏ đến cùng một vùng đệm. Bên gọi không chịu trách nhiệm giải phóng vùng đệm. Vùng đệm sẽ được giải phóng và các con trỏ trỏ đến đó trở nên không hợp lệ khi đối tượng Unicode được garbage collection.

   .. versionadded:: 3.3

   .. versionchanged:: 3.7
      Kiểu trả về hiện là ``const char *`` thay vì ``char *``.

   .. versionchanged:: 3.10
      Hàm này là một phần của :ref:`limited API <limited-c-api>`.


.. c:function:: const char* PyUnicode_AsUTF8(PyObject *unicode)

   Tương tự :c:func:`PyUnicode_AsUTF8AndSize`, nhưng không lưu kích thước.

   .. warning::

      Hàm này không có hành vi đặc biệt đối với `ký tự null <https://en.wikipedia.org/wiki/Null_character>`_ được nhúng trong *Unicode*. Do đó, các chuỗi chứa ký tự null sẽ vẫn tồn tại trong chuỗi được trả về; một số hàm C có thể diễn giải ký tự này là phần kết thúc chuỗi, dẫn đến việc chuỗi bị cắt ngắn. Nếu việc cắt ngắn gây ra vấn đề, bạn nên sử dụng :c:func:`PyUnicode_AsUTF8AndSize` thay thế.

   .. versionadded:: 3.3

   .. versionchanged:: 3.7
      Kiểu trả về hiện là ``const char *`` thay vì ``char *``.


Bộ mã hóa UTF-32
""""""""""""""""

Đây là các API codec UTF-32:


.. c:function:: PyObject* PyUnicode_DecodeUTF32(const char *str, Py_ssize_t size, \
                              const char *errors, int *byteorder)

   Giải mã *size* byte từ một chuỗi bộ đệm được mã hóa UTF-32 và trả về đối tượng Unicode tương ứng. *errors* (nếu không phải ``NULL``) xác định cách xử lý lỗi. Giá trị mặc định là "strict".

   Nếu *byteorder* khác ``NULL``, bộ giải mã bắt đầu giải mã bằng thứ tự byte đã cho::

      *byteorder == -1: little endian
      *byteorder == 0:  native order
      *byteorder == 1:  big endian

   Nếu ``*byteorder`` bằng không và bốn byte đầu tiên của dữ liệu đầu vào là dấu thứ tự byte (BOM), bộ giải mã chuyển sang thứ tự byte này và BOM không được sao chép vào chuỗi Unicode kết quả. Nếu ``*byteorder`` là ``-1`` hoặc ``1``, mọi dấu thứ tự byte đều được sao chép vào đầu ra.

   Sau khi hoàn tất, *\*byteorder* được đặt thành thứ tự byte hiện tại ở cuối dữ liệu đầu vào.

   Nếu *byteorder* là ``NULL``, codec bắt đầu ở chế độ thứ tự bản địa.

   Trả về ``NULL`` nếu codec phát sinh một exception.


.. c:function:: PyObject* PyUnicode_DecodeUTF32Stateful(const char *str, Py_ssize_t size, \
                              const char *errors, int *byteorder, Py_ssize_t *consumed)

   Nếu *consumed* là ``NULL``, hãy hoạt động giống như :c:func:`PyUnicode_DecodeUTF32`. Nếu *consumed* không phải là ``NULL``, :c:func:`PyUnicode_DecodeUTF32Stateful` sẽ không coi các chuỗi byte UTF-32 chưa hoàn chỉnh ở cuối (chẳng hạn như số byte không chia hết cho bốn) là lỗi. Các byte đó sẽ không được giải mã và số byte đã được giải mã sẽ được lưu vào *consumed*.


.. c:function:: PyObject* PyUnicode_AsUTF32String(PyObject *unicode)

   Trả về một chuỗi byte Python sử dụng encoding UTF-32 theo thứ tự byte native. Chuỗi luôn bắt đầu bằng dấu BOM. Việc xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh một exception.


Codec UTF-16
""""""""""""

Đây là các API codec UTF-16:


.. c:function:: PyObject* PyUnicode_DecodeUTF16(const char *str, Py_ssize_t size, \
                              const char *errors, int *byteorder)

   Giải mã *size* byte từ chuỗi bộ đệm được mã hóa UTF-16 và trả về đối tượng Unicode tương ứng. *errors* (nếu không phải ``NULL``) xác định cách xử lý lỗi. Giá trị mặc định là "strict".

   Nếu *byteorder* khác ``NULL``, bộ giải mã bắt đầu giải mã bằng thứ tự byte đã cho::

      *byteorder == -1: little endian
      *byteorder == 0:  native order
      *byteorder == 1:  big endian

   Nếu ``*byteorder`` bằng 0 và hai byte đầu tiên của dữ liệu đầu vào là dấu thứ tự byte (BOM), bộ giải mã chuyển sang thứ tự byte này và BOM không được sao chép vào chuỗi Unicode kết quả. Nếu ``*byteorder`` là ``-1`` hoặc ``1``, mọi dấu thứ tự byte đều được sao chép vào đầu ra (khi đó sẽ tạo thành ký tự ``\ufeff`` hoặc ``\ufffe``).

   Sau khi hoàn tất, ``*byteorder`` được đặt thành thứ tự byte hiện tại ở cuối dữ liệu đầu vào.

   Nếu *byteorder* là ``NULL``, codec bắt đầu ở chế độ thứ tự byte gốc.

   Trả về ``NULL`` nếu codec phát sinh một ngoại lệ.


.. c:function:: PyObject* PyUnicode_DecodeUTF16Stateful(const char *str, Py_ssize_t size, \
                              const char *errors, int *byteorder, Py_ssize_t *consumed)

   Nếu *consumed* là ``NULL``, hoạt động như :c:func:`PyUnicode_DecodeUTF16`. Nếu *consumed* không phải là ``NULL``, :c:func:`PyUnicode_DecodeUTF16Stateful` sẽ không xem các chuỗi byte UTF-16 chưa hoàn chỉnh ở cuối (chẳng hạn như số byte lẻ hoặc một cặp surrogate bị tách) là lỗi. Các byte đó sẽ không được giải mã và số byte đã được giải mã sẽ được lưu trong *consumed*.


.. c:function:: PyObject* PyUnicode_AsUTF16String(PyObject *unicode)

   Trả về một chuỗi byte Python sử dụng encoding UTF-16 theo thứ tự byte gốc. Chuỗi luôn bắt đầu bằng dấu BOM. Việc xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


Codec UTF-7
"""""""""""

Đây là các API codec UTF-7:


.. c:function:: PyObject* PyUnicode_DecodeUTF7(const char *str, Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa UTF-7 *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_DecodeUTF7Stateful(const char *str, Py_ssize_t size, \
                              const char *errors, Py_ssize_t *consumed)

   Nếu *consumed* là ``NULL``, hoạt động như :c:func:`PyUnicode_DecodeUTF7`. Nếu *consumed* không phải là ``NULL``, các phần base-64 UTF-7 chưa hoàn chỉnh ở cuối sẽ không được xem là lỗi. Các byte đó sẽ không được giải mã và số byte đã được giải mã sẽ được lưu trong *consumed*.


Các codec Unicode-Escape
""""""""""""""""""""""""

Đây là các API codec "Unicode Escape":


.. c:function:: PyObject* PyUnicode_DecodeUnicodeEscape(const char *str, \
                              Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa bằng Unicode-Escape *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_AsUnicodeEscapeString(PyObject *unicode)

   Mã hóa một đối tượng Unicode bằng Unicode-Escape và trả về kết quả dưới dạng đối tượng bytes. Cách xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


Các codec Raw-Unicode-Escape
""""""""""""""""""""""""""""

Đây là các API codec "Raw Unicode Escape":


.. c:function:: PyObject* PyUnicode_DecodeRawUnicodeEscape(const char *str, \
                              Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa bằng Raw-Unicode-Escape *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_AsRawUnicodeEscapeString(PyObject *unicode)

   Mã hóa một đối tượng Unicode bằng Raw-Unicode-Escape và trả về kết quả dưới dạng đối tượng bytes. Xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


Codec Latin-1
"""""""""""""

Đây là các API codec Latin-1: Latin-1 tương ứng với 256 ordinal Unicode đầu tiên và chỉ những ordinal này được codec chấp nhận trong quá trình mã hóa.


.. c:function:: PyObject* PyUnicode_DecodeLatin1(const char *str, Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa bằng Latin-1 *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_AsLatin1String(PyObject *unicode)

   Mã hóa một đối tượng Unicode bằng Latin-1 và trả về kết quả dưới dạng đối tượng bytes của Python. Xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


Bộ mã ASCII
"""""""""""

Đây là các API codec ASCII. Chỉ chấp nhận dữ liệu ASCII 7 bit. Tất cả các mã khác đều tạo ra lỗi.


.. c:function:: PyObject* PyUnicode_DecodeASCII(const char *str, Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa ASCII *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_AsASCIIString(PyObject *unicode)

   Mã hóa một đối tượng Unicode bằng ASCII và trả về kết quả dưới dạng đối tượng bytes của Python. Cách xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


Bộ mã ánh xạ ký tự
""""""""""""""""""

Codec này đặc biệt ở chỗ có thể được dùng để triển khai nhiều codec khác nhau (và thực tế đây chính là cách hầu hết các codec tiêu chuẩn có trong gói :mod:`!encodings` được tạo ra). Codec sử dụng các ánh xạ để mã hóa và giải mã ký tự. Các đối tượng ánh xạ được cung cấp phải hỗ trợ
:meth:`~object.__getitem__` giao diện ánh xạ; từ điển và dãy đều hoạt động tốt.

Đây là các API codec ánh xạ:

.. c:function:: PyObject* PyUnicode_DecodeCharmap(const char *str, Py_ssize_t length, \
                              PyObject *mapping, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi đã mã hóa *str* bằng đối tượng *mapping* đã cho. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.

   Nếu *mapping* là ``NULL``, thao tác giải mã Latin-1 sẽ được áp dụng. Nếu không, *mapping* phải ánh xạ các ordinal của byte (số nguyên trong phạm vi từ 0 đến 255) thành các chuỗi Unicode, số nguyên (sau đó được diễn giải là ordinal Unicode) hoặc ``None``. Các byte dữ liệu chưa được ánh xạ -- những byte khiến
   :exc:`LookupError`, cũng như những byte được ánh xạ thành ``None``, ``0xFFFE`` hoặc ``'\ufffe'``, đều được coi là các ánh xạ chưa xác định và gây ra lỗi.


.. c:function:: PyObject* PyUnicode_AsCharmapString(PyObject *unicode, PyObject *mapping)

   Mã hóa một đối tượng Unicode bằng đối tượng *mapping* đã cho và trả về kết quả dưới dạng một đối tượng bytes. Cách xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.

   Đối tượng *mapping* phải ánh xạ các số nguyên ordinal Unicode thành các đối tượng bytes, các số nguyên trong phạm vi từ 0 đến 255 hoặc ``None``. Các ordinal của ký tự chưa được ánh xạ (những ordinal khiến :exc:`LookupError`) cũng như các ordinal được ánh xạ thành ``None`` đều được coi là "ánh xạ chưa xác định" và gây ra lỗi.


API codec sau đây đặc biệt ở chỗ ánh xạ Unicode sang Unicode.

.. c:function:: PyObject* PyUnicode_Translate(PyObject *unicode, PyObject *table, const char *errors)

   Dịch một chuỗi bằng cách áp dụng bảng ánh xạ ký tự vào chuỗi đó rồi trả về đối tượng Unicode kết quả. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.

   Bảng ánh xạ phải ánh xạ các số nguyên thứ tự Unicode sang các số nguyên thứ tự Unicode hoặc ``None`` (khiến ký tự bị xóa).

   Bảng ánh xạ chỉ cần cung cấp giao diện :meth:`~object.__getitem__`; dictionary và sequence hoạt động tốt. Các số thứ tự ký tự không được ánh xạ (những số gây ra một
   :exc:`LookupError`) được giữ nguyên và sao chép như hiện tại.

   *errors* có ý nghĩa thông thường đối với codec. Giá trị này có thể là ``NULL``, cho biết sử dụng cách xử lý lỗi mặc định.


Codec MBCS cho Windows
""""""""""""""""""""""

Đây là các API codec MBCS. Hiện tại, chúng chỉ khả dụng trên Windows và sử dụng các bộ chuyển đổi MBCS của Win32 để thực hiện việc chuyển đổi. Lưu ý rằng MBCS (hoặc DBCS) là một nhóm các encoding, không chỉ là một encoding duy nhất. Encoding đích được xác định bởi cài đặt người dùng trên máy chạy codec.

.. c:function:: PyObject* PyUnicode_DecodeMBCS(const char *str, Py_ssize_t size, const char *errors)

   Tạo một đối tượng Unicode bằng cách giải mã *size* byte của chuỗi được mã hóa MBCS *str*. Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_DecodeMBCSStateful(const char *str, Py_ssize_t size, \
                              const char *errors, Py_ssize_t *consumed)

   Nếu *consumed* là ``NULL``, hoạt động như :c:func:`PyUnicode_DecodeMBCS`. Nếu *consumed* không phải là ``NULL``, :c:func:`PyUnicode_DecodeMBCSStateful` sẽ không giải mã byte dẫn đầu còn lại và số byte đã được giải mã sẽ được lưu trong *consumed*.


.. c:function:: PyObject* PyUnicode_DecodeCodePageStateful(int code_page, const char *str, \
                              Py_ssize_t size, const char *errors, Py_ssize_t *consumed)

   Tương tự như :c:func:`PyUnicode_DecodeMBCSStateful`, nhưng sử dụng code page được chỉ định bởi *code_page*.


.. c:function:: PyObject* PyUnicode_AsMBCSString(PyObject *unicode)

   Mã hóa một đối tượng Unicode bằng MBCS và trả về kết quả dưới dạng đối tượng bytes của Python. Cách xử lý lỗi là "strict". Trả về ``NULL`` nếu codec phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_EncodeCodePage(int code_page, PyObject *unicode, const char *errors)

   Mã hóa đối tượng Unicode bằng trang mã được chỉ định và trả về một đối tượng bytes của Python. Trả về ``NULL`` nếu codec phát sinh ngoại lệ. Sử dụng
   trang mã :c:macro:`!CP_ACP` để lấy MBCS encoder.

   .. versionadded:: 3.3


.. _unicodemethodsandslots:

Các phương thức và hàm slot
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các API sau đây có khả năng xử lý các đối tượng Unicode và chuỗi ở đầu vào (trong phần mô tả, chúng tôi gọi chúng là chuỗi) và trả về các đối tượng Unicode hoặc số nguyên tương ứng.

Tất cả đều trả về ``NULL`` hoặc ``-1`` nếu xảy ra ngoại lệ.


.. c:function:: PyObject* PyUnicode_Concat(PyObject *left, PyObject *right)

   Nối hai chuỗi để tạo thành một chuỗi Unicode mới.


.. c:function:: PyObject* PyUnicode_Split(PyObject *unicode, PyObject *sep, Py_ssize_t maxsplit)

   Tách một chuỗi và trả về danh sách các chuỗi Unicode. Nếu *sep* là ``NULL``, việc tách sẽ được thực hiện tại tất cả các chuỗi con khoảng trắng. Nếu không, các phần tách sẽ xảy ra tại dấu phân cách đã cho. Tối đa *maxsplit* lần tách sẽ được thực hiện. Nếu là số âm, sẽ không đặt giới hạn. Các dấu phân cách không được đưa vào danh sách kết quả.

   Khi xảy ra lỗi, trả về ``NULL`` và thiết lập ngoại lệ.

   Tương đương với :py:meth:`str.split`.


.. c:function:: PyObject* PyUnicode_RSplit(PyObject *unicode, PyObject *sep, Py_ssize_t maxsplit)

   Tương tự :c:func:`PyUnicode_Split`, nhưng việc tách sẽ bắt đầu từ cuối chuỗi.

   Khi xảy ra lỗi, trả về ``NULL`` và thiết lập ngoại lệ.

   Tương đương với :py:meth:`str.rsplit`.


.. c:function:: PyObject* PyUnicode_Splitlines(PyObject *unicode, int keepends)

   Tách một chuỗi Unicode tại các ngắt dòng, trả về danh sách các chuỗi Unicode. CRLF được xem là một ngắt dòng. Nếu *keepends* là ``0``, các ký tự ngắt dòng không được đưa vào các chuỗi kết quả.


.. c:function:: PyObject* PyUnicode_Partition(PyObject *unicode, PyObject *sep)

   Tách một chuỗi Unicode tại lần xuất hiện đầu tiên của *sep*, rồi trả về một bộ 3 phần tử gồm phần trước dấu phân tách, chính dấu phân tách và phần sau dấu phân tách. Nếu không tìm thấy dấu phân tách, trả về một bộ 3 phần tử gồm chính chuỗi đó, theo sau là hai chuỗi rỗng.

   *sep* không được để trống.

   Khi xảy ra lỗi, trả về ``NULL`` và thiết lập ngoại lệ.

   Tương đương với :py:meth:`str.partition`.


.. c:function:: PyObject* PyUnicode_RPartition(PyObject *unicode, PyObject *sep)

   Tương tự như :c:func:`PyUnicode_Partition`, nhưng tách một chuỗi Unicode tại lần xuất hiện cuối cùng của *sep*. Nếu không tìm thấy dấu phân tách, trả về một tuple 3 phần tử chứa hai chuỗi rỗng, theo sau là chính chuỗi đó.

   *sep* không được để trống.

   Khi xảy ra lỗi, trả về ``NULL`` và thiết lập ngoại lệ.

   Tương đương với :py:meth:`str.rpartition`.


.. c:function:: PyObject* PyUnicode_Join(PyObject *separator, PyObject *seq)

   Nối một chuỗi các chuỗi bằng *dấu phân cách* đã cho và trả về chuỗi Unicode kết quả.


.. c:function:: Py_ssize_t PyUnicode_Tailmatch(PyObject *unicode, PyObject *substr, \
                        Py_ssize_t start, Py_ssize_t end, int direction)

   Trả về ``1`` nếu *substr* khớp với ``unicode[start:end]`` ở phần cuối đã cho (*direction* == ``-1`` nghĩa là thực hiện so khớp tiền tố, *direction* == ``1`` là so khớp hậu tố), ``0`` nếu không. Trả về ``-1`` nếu xảy ra lỗi.


.. c:function:: Py_ssize_t PyUnicode_Find(PyObject *unicode, PyObject *substr, \
                               Py_ssize_t start, Py_ssize_t end, int direction)

   Trả về vị trí đầu tiên của *substr* trong ``unicode[start:end]`` bằng cách sử dụng *direction* đã cho (*direction* == ``1`` nghĩa là thực hiện tìm kiếm xuôi, *direction* == ``-1`` là tìm kiếm ngược). Giá trị trả về là chỉ mục của kết quả khớp đầu tiên; giá trị ``-1`` cho biết không tìm thấy kết quả khớp nào, còn ``-2`` cho biết đã xảy ra lỗi và một exception đã được thiết lập.


.. c:function:: Py_ssize_t PyUnicode_FindChar(PyObject *unicode, Py_UCS4 ch, \
                               Py_ssize_t start, Py_ssize_t end, int direction)

   Trả về vị trí đầu tiên của ký tự *ch* trong ``unicode[start:end]`` bằng cách sử dụng *direction* đã cho (*direction* == ``1`` nghĩa là thực hiện tìm kiếm xuôi, *direction* == ``-1`` là tìm kiếm ngược). Giá trị trả về là chỉ mục của kết quả khớp đầu tiên; giá trị ``-1`` cho biết không tìm thấy kết quả khớp nào, còn ``-2`` cho biết đã xảy ra lỗi và một exception đã được thiết lập.

   .. versionadded:: 3.3

   .. versionchanged:: 3.7
      *start* và *end* hiện được điều chỉnh để hoạt động như ``unicode[start:end]``.


.. c:function:: Py_ssize_t PyUnicode_Count(PyObject *unicode, PyObject *substr, \
                               Py_ssize_t start, Py_ssize_t end)

   Trả về số lần xuất hiện không chồng lấp của *substr* trong ``unicode[start:end]``.  Trả về ``-1`` nếu xảy ra lỗi.


.. c:function:: PyObject* PyUnicode_Replace(PyObject *unicode, PyObject *substr, \
                              PyObject *replstr, Py_ssize_t maxcount)

   Thay thế nhiều nhất *maxcount* lần xuất hiện của *substr* trong *unicode* bằng *replstr* và trả về đối tượng Unicode thu được. *maxcount* == ``-1`` nghĩa là thay thế tất cả các lần xuất hiện.


.. c:function:: int PyUnicode_Compare(PyObject *left, PyObject *right)

   So sánh hai chuỗi và lần lượt trả về ``-1``, ``0``, ``1`` tương ứng với nhỏ hơn, bằng và lớn hơn.

   Hàm này trả về ``-1`` khi thất bại, vì vậy cần gọi
   :c:func:`PyErr_Occurred` để kiểm tra lỗi.

   .. seealso::

      Hàm :c:func:`PyUnicode_Equal`.


.. c:function:: int PyUnicode_Equal(PyObject *a, PyObject *b)

   Kiểm tra xem hai chuỗi có bằng nhau không:

   * Trả về ``1`` nếu *a* bằng *b*.
   * Trả về ``0`` nếu *a* không bằng *b*.
   * Đặt một ngoại lệ :exc:`TypeError` và trả về ``-1`` nếu *a* hoặc *b* không phải là một
     :class:`str` đối tượng.

   Hàm luôn thành công nếu *a* và *b* là các đối tượng :class:`str`.

   Hàm hoạt động với các lớp con của :class:`str`, nhưng không tuân theo phương thức ``__eq__()`` tùy chỉnh.

   .. seealso::

      Hàm :c:func:`PyUnicode_Compare`.

   .. versionadded:: 3.14


.. c:function:: int PyUnicode_EqualToUTF8AndSize(PyObject *unicode, const char *string, Py_ssize_t size)

   So sánh một đối tượng Unicode với bộ đệm char được diễn giải là mã hóa UTF-8 hoặc ASCII và trả về true (``1``) nếu chúng bằng nhau, hoặc false (``0``) nếu không. Nếu đối tượng Unicode chứa các điểm mã surrogate (``U+D800`` - ``U+DFFF``) hoặc chuỗi C không phải là UTF-8 hợp lệ, false (``0``) sẽ được trả về.

   Hàm này không phát sinh ngoại lệ.

   .. versionadded:: 3.13


.. c:function:: int PyUnicode_EqualToUTF8(PyObject *unicode, const char *string)

   Tương tự :c:func:`PyUnicode_EqualToUTF8AndSize`, nhưng tính độ dài *string* bằng :c:func:`!strlen`. Nếu đối tượng Unicode chứa các ký tự null, false (``0``) sẽ được trả về.

   .. versionadded:: 3.13


.. c:function:: int PyUnicode_CompareWithASCIIString(PyObject *unicode, const char *string)

   So sánh một đối tượng Unicode, *unicode*, với *string* và lần lượt trả về ``-1``, ``0``, ``1`` khi nhỏ hơn, bằng và lớn hơn. Tốt nhất chỉ nên truyền các chuỗi được mã hóa ASCII, nhưng hàm sẽ diễn giải chuỗi đầu vào là ISO-8859-1 nếu chuỗi chứa các ký tự không phải ASCII.

   Hàm này không phát sinh ngoại lệ.


.. c:function:: PyObject* PyUnicode_RichCompare(PyObject *left,  PyObject *right, int op)

   So sánh phong phú hai chuỗi Unicode và trả về một trong các giá trị sau:

   * ``NULL`` trong trường hợp xảy ra ngoại lệ
   * :c:data:`Py_True` hoặc :c:data:`Py_False` đối với các phép so sánh thành công
   * :c:data:`Py_NotImplemented` trong trường hợp không xác định được tổ hợp kiểu

   Các giá trị có thể có của *op* là :c:macro:`Py_GT`, :c:macro:`Py_GE`, :c:macro:`Py_EQ`,
   :c:macro:`Py_NE`, :c:macro:`Py_LT` và :c:macro:`Py_LE`.


.. c:function:: PyObject* PyUnicode_Format(PyObject *format, PyObject *args)

   Trả về một đối tượng chuỗi mới từ *format* và *args*; tương tự như ``format % args``.


.. c:function:: int PyUnicode_Contains(PyObject *unicode, PyObject *substr)

   Kiểm tra xem *substr* có nằm trong *unicode* hay không, rồi trả về true hoặc false tương ứng.

   *substr* phải được ép kiểu thành một chuỗi Unicode gồm một phần tử. ``-1`` được trả về nếu có lỗi.


.. c:function:: void PyUnicode_InternInPlace(PyObject **p_unicode)

   Intern đối số :c:expr:`*p_unicode` tại chỗ. Đối số phải là địa chỉ của một biến con trỏ trỏ đến một đối tượng chuỗi Unicode Python. Nếu đã có một chuỗi được intern giống với :c:expr:`*p_unicode`, hàm đặt :c:expr:`*p_unicode` trỏ đến chuỗi đó (giải phóng tham chiếu đến đối tượng chuỗi cũ và tạo một
   :term:`strong reference` mới trỏ đến đối tượng chuỗi đã được intern), nếu không thì giữ nguyên
   :c:expr:`*p_unicode` và intern nó.

   (Làm rõ: mặc dù có nhiều đề cập đến các tham chiếu, hãy xem hàm này là trung tính về tham chiếu. Bạn phải sở hữu đối tượng truyền vào; sau khi gọi hàm, bạn không còn sở hữu tham chiếu đã truyền vào, nhưng sẽ sở hữu kết quả mới.)

   Hàm này không bao giờ phát sinh ngoại lệ. Khi xảy ra lỗi, hàm giữ nguyên đối số mà không intern đối số đó.

   Các instance của lớp con của :py:class:`str` có thể không được intern, tức là
   :c:expr:`PyUnicode_CheckExact(*p_unicode)` phải là true. Nếu không, thì -- cũng như mọi lỗi khác -- đối số sẽ được giữ nguyên.

   Lưu ý rằng các chuỗi đã được intern không phải là “bất tử”. Bạn phải giữ một tham chiếu đến kết quả để hưởng lợi từ việc interning.


.. c:function:: PyObject* PyUnicode_InternFromString(const char *str)

   Một tổ hợp của :c:func:`PyUnicode_FromString` và
   :c:func:`PyUnicode_InternInPlace`, dành cho các chuỗi được cấp phát tĩnh.

   Trả về một tham chiếu mới ("owned") đến một đối tượng chuỗi Unicode mới đã được intern hoặc một đối tượng chuỗi đã được intern trước đó có cùng giá trị.

   Python có thể giữ một tham chiếu đến kết quả hoặc làm cho kết quả trở thành :term:`immortal`, khiến kết quả không được thu gom rác kịp thời. Để intern một số lượng không giới hạn các chuỗi khác nhau, chẳng hạn như các chuỗi đến từ dữ liệu đầu vào của người dùng, hãy ưu tiên gọi :c:func:`PyUnicode_FromString` và
   :c:func:`PyUnicode_InternInPlace` trực tiếp.


.. c:function:: unsigned int PyUnicode_CHECK_INTERNED(PyObject *str)

   Trả về một giá trị khác không nếu *str* đã được intern, hoặc bằng không nếu chưa. Đối số *str* phải là một chuỗi; điều này không được kiểm tra. Hàm này luôn thành công.

   .. impl-detail::

      Giá trị trả về khác không có thể chứa thêm thông tin về *how* chuỗi được intern. Ý nghĩa của các giá trị khác không đó, cũng như thông tin liên quan đến việc intern của từng chuỗi cụ thể, có thể thay đổi giữa các phiên bản CPython.


PyUnicodeWriter
^^^^^^^^^^^^^^^

API :c:type:`PyUnicodeWriter` có thể được dùng để tạo một đối tượng :class:`str` của Python.

.. versionadded:: 3.14

.. c:type:: PyUnicodeWriter

   Một thực thể trình ghi Unicode.

   Đối tượng phải được hủy bằng :c:func:`PyUnicodeWriter_Finish` khi thành công hoặc bằng :c:func:`PyUnicodeWriter_Discard` khi có lỗi.

.. c:function:: PyUnicodeWriter* PyUnicodeWriter_Create(Py_ssize_t length)

   Tạo một đối tượng PyUnicodeWriter.

   *length* phải lớn hơn hoặc bằng ``0``.

   Nếu *length* lớn hơn ``0``, hãy cấp phát trước một bộ đệm nội bộ gồm *length* ký tự.

   Đặt một exception và trả về ``NULL`` khi có lỗi.

.. c:function:: PyObject* PyUnicodeWriter_Finish(PyUnicodeWriter *writer)

   Trả về đối tượng Python :class:`str` cuối cùng và hủy đối tượng writer.

   Đặt một exception và trả về ``NULL`` khi có lỗi.

   Đối tượng writer không hợp lệ sau lời gọi này.

.. c:function:: void PyUnicodeWriter_Discard(PyUnicodeWriter *writer)

   Hủy bộ đệm Unicode nội bộ và hủy đối tượng writer.

   Nếu *writer* là ``NULL``, không thực hiện thao tác nào.

   Đối tượng writer không hợp lệ sau lời gọi này.

.. c:function:: int PyUnicodeWriter_WriteChar(PyUnicodeWriter *writer, Py_UCS4 ch)

   Ghi ký tự Unicode duy nhất *ch* vào *writer*.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

.. c:function:: int PyUnicodeWriter_WriteUTF8(PyUnicodeWriter *writer, const char *str, Py_ssize_t size)

   Giải mã chuỗi *str* từ UTF-8 ở strict mode và ghi kết quả vào *writer*.

   *size* là độ dài chuỗi tính bằng byte. Nếu *size* bằng ``-1``, hãy gọi ``strlen(str)`` để lấy độ dài chuỗi.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

   Xem thêm :c:func:`PyUnicodeWriter_DecodeUTF8Stateful`.

.. c:function:: int PyUnicodeWriter_WriteASCII(PyUnicodeWriter *writer, const char *str, Py_ssize_t size)

   Ghi chuỗi ASCII *str* vào *writer*.

   *size* là độ dài chuỗi tính bằng byte. Nếu *size* bằng ``-1``, hãy gọi ``strlen(str)`` để lấy độ dài chuỗi.

   *str* chỉ được chứa các ký tự ASCII. Hành vi không được xác định nếu *str* chứa các ký tự không phải ASCII.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

.. c:function:: int PyUnicodeWriter_WriteWideChar(PyUnicodeWriter *writer, const wchar_t *str, Py_ssize_t size)

   Ghi chuỗi wide *str* vào *writer*.

   *size* là số lượng ký tự wide. Nếu *size* bằng ``-1``, hãy gọi ``wcslen(str)`` để lấy độ dài chuỗi.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

.. c:function:: int PyUnicodeWriter_WriteUCS4(PyUnicodeWriter *writer, Py_UCS4 *str, Py_ssize_t size)

   Ghi chuỗi UCS4 *str* vào *writer*.

   *size* là số lượng ký tự UCS4.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

.. c:function:: int PyUnicodeWriter_WriteStr(PyUnicodeWriter *writer, PyObject *obj)

   Gọi :c:func:`PyObject_Str` trên *obj* và ghi đầu ra vào *writer*.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

   Để viết một lớp con :class:`str` ghi đè phương thức :meth:`~object.__str__`, có thể sử dụng :c:func:`PyUnicode_FromObject` để lấy chuỗi ban đầu.

.. c:function:: int PyUnicodeWriter_WriteRepr(PyUnicodeWriter *writer, PyObject *obj)

   Gọi :c:func:`PyObject_Repr` trên *obj* và ghi đầu ra vào *writer*.

   Nếu *obj* là ``NULL``, hãy ghi chuỗi ``"<NULL>"`` vào *writer*.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

   .. versionchanged:: 3.14.4

      Đã bổ sung hỗ trợ cho ``NULL``.

.. c:function:: int PyUnicodeWriter_WriteSubstring(PyUnicodeWriter *writer, PyObject *str, Py_ssize_t start, Py_ssize_t end)

   Ghi chuỗi con ``str[start:end]`` vào *writer*.

   *str* phải là một đối tượng Python :class:`str` . *start* phải lớn hơn hoặc bằng 0 và nhỏ hơn hoặc bằng *end*. *end* phải nhỏ hơn hoặc bằng độ dài của *str*.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

.. c:function:: int PyUnicodeWriter_Format(PyUnicodeWriter *writer, const char *format, ...)

   Tương tự như :c:func:`PyUnicode_FromFormat`, nhưng ghi trực tiếp đầu ra vào *writer*.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

.. c:function:: int PyUnicodeWriter_DecodeUTF8Stateful(PyUnicodeWriter *writer, const char *string, Py_ssize_t length, const char *errors, Py_ssize_t *consumed)

   Giải mã chuỗi *str* từ UTF-8 bằng trình xử lý lỗi *errors* và ghi đầu ra vào *writer*.

   *size* là độ dài chuỗi tính bằng byte. Nếu *size* bằng ``-1``, hãy gọi ``strlen(str)`` để lấy độ dài chuỗi.

   *errors* là tên của một :ref:`error handler <error-handlers>`, chẳng hạn như ``"replace"``. Nếu *errors* là ``NULL``, hãy sử dụng trình xử lý lỗi strict.

   Nếu *consumed* không phải là ``NULL``, hãy đặt *\*consumed* thành số byte đã giải mã khi thành công. Nếu *consumed* là ``NULL``, hãy coi các chuỗi byte UTF-8 chưa hoàn chỉnh ở cuối là lỗi.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, đặt một exception, giữ nguyên writer và trả về ``-1``.

   Xem thêm :c:func:`PyUnicodeWriter_WriteUTF8`.

API đã lỗi thời
^^^^^^^^^^^^^^^

API sau đây đã lỗi thời.

.. c:type:: Py_UNICODE

   Đây là một typedef của :c:type:`wchar_t`, là kiểu 16 bit hoặc 32 bit tùy thuộc vào nền tảng. Thay vào đó, hãy sử dụng trực tiếp :c:type:`wchar_t`.

   .. versionchanged:: 3.3
      Trong các phiên bản trước, đây là kiểu 16 bit hoặc 32 bit tùy thuộc vào việc bạn chọn phiên bản Unicode "narrow" hay "wide" của Python khi xây dựng.

   .. deprecated-removed:: 3.13 3.15


.. c:function:: int PyUnicode_READY(PyObject *unicode)

   Không làm gì và trả về ``0``. API này chỉ được giữ lại để đảm bảo khả năng tương thích ngược, nhưng hiện chưa có kế hoạch loại bỏ nó.

   .. versionadded:: 3.3

   .. deprecated:: 3.10
      API này không thực hiện thao tác nào kể từ Python 3.12. Trước đây, cần gọi API này cho mỗi chuỗi được tạo bằng API cũ (:c:func:`!PyUnicode_FromUnicode` hoặc tương tự).


.. c:function:: unsigned int PyUnicode_IS_READY(PyObject *unicode)

   Không làm gì và trả về ``1``. API này chỉ được giữ lại để đảm bảo khả năng tương thích ngược, nhưng hiện chưa có kế hoạch loại bỏ nó.

   .. versionadded:: 3.3

   .. deprecated:: 3.14
      API này không thực hiện thao tác nào kể từ Python 3.12. Trước đây, có thể gọi API này để kiểm tra xem
      :c:func:`PyUnicode_READY` có cần thiết hay không.

.. _`null characters`: https://en.wikipedia.org/wiki/Null_character
