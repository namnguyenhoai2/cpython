.. highlight:: c

.. _string-conversion:

Chuyển đổi và định dạng chuỗi
=============================

Các hàm chuyển đổi số và xuất chuỗi đã định dạng.


.. c:function:: int PyOS_snprintf(char *str, size_t size,  const char *format, ...)

   Xuất không quá *size* byte vào *str* theo chuỗi định dạng *format* và các đối số bổ sung. Xem trang hướng dẫn Unix :manpage:`snprintf(3)`.


.. c:function:: int PyOS_vsnprintf(char *str, size_t size, const char *format, va_list va)

   Xuất không quá *size* byte vào *str* theo chuỗi định dạng *format* và danh sách đối số biến đổi *va*. Trang hướng dẫn Unix
   :manpage:`vsnprintf(3)`.

:c:func:`PyOS_snprintf` và :c:func:`PyOS_vsnprintf` bao bọc các hàm thư viện Standard C :c:func:`snprintf` và :c:func:`vsnprintf`. Mục đích của chúng là đảm bảo hành vi nhất quán trong các trường hợp đặc biệt, điều mà các hàm Standard C không đảm bảo.

Các hàm bao bọc đảm bảo rằng ``str[size-1]`` luôn là ``'\0'`` khi trả về. Chúng không bao giờ ghi quá *size* byte (bao gồm cả ``'\0'`` ở cuối) vào str. Cả hai hàm đều yêu cầu rằng ``str != NULL``, ``size > 0``, ``format != NULL`` và ``size < INT_MAX``. Lưu ý rằng điều này có nghĩa là không có hàm tương đương với ``n = snprintf(NULL, 0, ...)`` của C99 để xác định kích thước bộ đệm cần thiết.

Giá trị trả về (*rv*) của các hàm này được diễn giải như sau:

* Khi ``0 <= rv < size``, quá trình chuyển đổi đầu ra thành công và *rv* ký tự đã được ghi vào *str* (không bao gồm byte ``'\0'`` ở cuối tại ``str[rv]``).

* Khi ``rv >= size``, quá trình chuyển đổi đầu ra bị cắt ngắn và cần một bộ đệm có ``rv + 1`` byte để thành công. ``str[size-1]`` là ``'\0'`` trong trường hợp này.

* Khi ``rv < 0``, quá trình chuyển đổi đầu ra thất bại và ``str[size-1]`` cũng là ``'\0'`` trong trường hợp này, nhưng phần còn lại của *str* không được xác định. Nguyên nhân chính xác của lỗi phụ thuộc vào nền tảng bên dưới.


Các hàm sau đây cung cấp khả năng chuyển đổi chuỗi thành số không phụ thuộc vào locale.

.. c:function:: unsigned long PyOS_strtoul(const char *str, char **ptr, int base)

   Chuyển đổi phần đầu của chuỗi trong ``str`` thành giá trị :c:expr:`unsigned long` theo ``base`` đã cho, phải nằm trong khoảng từ ``2`` đến ``36`` (bao gồm cả hai), hoặc là giá trị đặc biệt ``0``.

   Khoảng trắng ở đầu và kiểu chữ của các ký tự sẽ bị bỏ qua. Nếu ``base`` bằng 0, hàm sẽ tìm ``0b``, ``0o`` hoặc ``0x`` ở đầu để xác định cơ số. Nếu không có các tiền tố này, cơ số mặc định là ``10``. Cơ số phải bằng 0 hoặc nằm trong khoảng từ 2 đến 36 (bao gồm cả hai). Nếu ``ptr`` khác ``NULL``, nó sẽ chứa một con trỏ đến cuối quá trình quét.

   Nếu giá trị đã chuyển đổi nằm ngoài phạm vi của kiểu trả về tương ứng, sẽ xảy ra lỗi phạm vi (:c:data:`errno` được đặt thành :c:macro:`!ERANGE`) và
   :c:macro:`!ULONG_MAX` được trả về. Nếu không thể thực hiện chuyển đổi, ``0`` được trả về.

   Xem thêm trang hướng dẫn Unix :manpage:`strtoul(3)`.

   .. versionadded:: 3.2


.. c:function:: long PyOS_strtol(const char *str, char **ptr, int base)

   Chuyển đổi phần đầu của chuỗi trong ``str`` thành một giá trị :c:expr:`long` theo ``base`` đã cho, giá trị này phải nằm trong khoảng từ ``2`` đến ``36`` (bao gồm cả hai), hoặc là giá trị đặc biệt ``0``.

   Giống như :c:func:`PyOS_strtoul`, nhưng thay vào đó trả về một giá trị :c:expr:`long` và :c:macro:`LONG_MAX` khi xảy ra tràn.

   Xem thêm trang hướng dẫn Unix :manpage:`strtol(3)`.

   .. versionadded:: 3.2


.. c:function:: double PyOS_string_to_double(const char *s, char **endptr, PyObject *overflow_exception)

   Chuyển đổi chuỗi ``s`` thành một :c:expr:`double`, và phát sinh ngoại lệ Python nếu thất bại. Tập hợp các chuỗi được chấp nhận tương ứng với tập hợp các chuỗi được hàm khởi tạo :func:`float` của Python chấp nhận, ngoại trừ việc ``s`` không được có khoảng trắng ở đầu hoặc cuối. Việc chuyển đổi không phụ thuộc vào locale hiện tại.

   Nếu ``endptr`` là ``NULL``, hãy chuyển đổi toàn bộ chuỗi. Phát sinh
   :exc:`ValueError` và trả về ``-1.0`` nếu chuỗi không phải là biểu diễn hợp lệ của một số dấu phẩy động.

   Nếu endptr không phải là ``NULL``, hãy chuyển đổi phần lớn nhất có thể của chuỗi và đặt ``*endptr`` trỏ đến ký tự đầu tiên chưa được chuyển đổi. Nếu không có đoạn đầu nào của chuỗi là biểu diễn hợp lệ của một số dấu phẩy động, hãy đặt ``*endptr`` trỏ đến đầu chuỗi, phát sinh ValueError và trả về ``-1.0``.

   Nếu ``s`` biểu diễn một giá trị quá lớn để lưu trữ trong một float (ví dụ: ``"1e500"`` là một chuỗi như vậy trên nhiều nền tảng), thì nếu ``overflow_exception`` là ``NULL``, hãy trả về ``Py_INFINITY`` (với dấu thích hợp) và không đặt bất kỳ exception nào. Nếu không, ``overflow_exception`` phải trỏ đến một đối tượng exception Python; hãy phát sinh exception đó và trả về ``-1.0``. Trong cả hai trường hợp, hãy đặt ``*endptr`` trỏ đến ký tự đầu tiên sau giá trị đã chuyển đổi.

   Nếu xảy ra bất kỳ lỗi nào khác trong quá trình chuyển đổi (ví dụ: lỗi hết bộ nhớ), hãy đặt Python exception thích hợp và trả về ``-1.0``.

   .. versionadded:: 3.1


.. c:function:: char* PyOS_double_to_string(double val, char format_code, int precision, int flags, int *ptype)

   Chuyển đổi một :c:expr:`double` *val* thành chuỗi bằng cách sử dụng *format_code*, *precision* và *flags* được cung cấp.

   *format_code* phải là một trong các giá trị ``'e'``, ``'E'``, ``'f'``, ``'F'``, ``'g'``, ``'G'`` hoặc ``'r'``. Đối với ``'r'``, *precision* được cung cấp phải là 0 và sẽ bị bỏ qua. Mã định dạng ``'r'`` chỉ định định dạng :func:`repr` tiêu chuẩn.

   *flags* có thể là không hoặc nhiều giá trị sau được kết hợp bằng phép OR:

   .. c:namespace:: NULL

   .. c:macro:: Py_DTSF_SIGN

      Luôn đặt trước chuỗi được trả về một ký tự dấu, ngay cả khi *val* không âm.

   .. c:macro:: Py_DTSF_ADD_DOT_0

      Đảm bảo rằng chuỗi được trả về sẽ không có dạng một số nguyên.

   .. c:macro:: Py_DTSF_ALT

      Áp dụng các quy tắc định dạng "alternate". Xem tài liệu về specifier :c:func:`PyOS_snprintf` ``'#'`` để biết chi tiết.

   .. c:macro:: Py_DTSF_NO_NEG_0

      Số 0 âm được chuyển đổi thành số 0 dương.

      .. versionadded:: 3.11

   Nếu *ptype* không phải là ``NULL``, thì giá trị mà nó trỏ tới sẽ được đặt thành một trong các hằng số sau đây, tùy thuộc vào kiểu của *val*:

   .. list-table::
      :header-rows: 1
      :align: left

      * - *\*ptype*
        - kiểu của *val*
      * - .. c:macro:: Py_DTST_FINITE
        - số hữu hạn
      * - .. c:macro:: Py_DTST_INFINITE
        - số vô hạn
      * - .. c:macro:: Py_DTST_NAN
        - không phải là số

   Giá trị trả về là một con trỏ tới *buffer* chứa chuỗi đã chuyển đổi hoặc ``NULL`` nếu quá trình chuyển đổi không thành công. Bên gọi chịu trách nhiệm giải phóng chuỗi được trả về bằng cách gọi :c:func:`PyMem_Free`.

   .. versionadded:: 3.1


.. c:function:: int PyOS_mystricmp(const char *str1, const char *str2)
                int PyOS_mystrnicmp(const char *str1, const char *str2, Py_ssize_t size)

   So sánh chuỗi không phân biệt chữ hoa chữ thường. Các hàm này hoạt động gần như giống hệt :c:func:`!strcmp` và :c:func:`!strncmp` (tương ứng), ngoại trừ việc chúng bỏ qua kiểu chữ của các ký tự ASCII.

   Trả về ``0`` nếu các chuỗi bằng nhau, giá trị âm nếu *str1* được sắp xếp theo thứ tự từ điển trước *str2*, hoặc giá trị dương nếu nó được sắp xếp sau.

   Trong các đối số *str1* hoặc *str2*, byte NUL đánh dấu điểm kết thúc chuỗi. Đối với :c:func:`!PyOS_mystrnicmp`, đối số *size* cho biết kích thước tối đa của chuỗi, như thể NUL xuất hiện tại chỉ mục được chỉ định bởi *size*.

   Các hàm này không sử dụng locale.


.. c:function:: int PyOS_stricmp(const char *str1, const char *str2)
                int PyOS_strnicmp(const char *str1, const char *str2, Py_ssize_t  size)

   So sánh chuỗi không phân biệt chữ hoa chữ thường.

   Trên Windows, đây lần lượt là các bí danh của :c:func:`!stricmp` và :c:func:`!strnicmp`.

   Trên các nền tảng khác, chúng là các bí danh của :c:func:`PyOS_mystricmp` và
   :c:func:`PyOS_mystrnicmp`, theo thứ tự tương ứng.


Phân loại và chuyển đổi ký tự
=============================

Các macro sau cung cấp chức năng phân loại và chuyển đổi ký tự không phụ thuộc locale (không giống như ``ctype.h`` của thư viện chuẩn C). Đối số phải là một :c:expr:`char` có dấu hoặc không dấu.


.. c:macro:: Py_ISALNUM(c)

   Trả về true nếu ký tự *c* là ký tự chữ-số.


.. c:macro:: Py_ISALPHA(c)

   Trả về true nếu ký tự *c* là ký tự chữ cái (``a-z`` và ``A-Z``).


.. c:macro:: Py_ISDIGIT(c)

   Trả về true nếu ký tự *c* là chữ số thập phân (``0-9``).


.. c:macro:: Py_ISLOWER(c)

   Trả về true nếu ký tự *c* là chữ cái ASCII viết thường (``a-z``).


.. c:macro:: Py_ISUPPER(c)

   Trả về true nếu ký tự *c* là chữ cái ASCII viết hoa (``A-Z``).


.. c:macro:: Py_ISSPACE(c)

   Trả về true nếu ký tự *c* là ký tự khoảng trắng (dấu cách, tab, xuống dòng đầu dòng, xuống dòng, tab dọc hoặc ký hiệu xuống trang).


.. c:macro:: Py_ISXDIGIT(c)

   Trả về true nếu ký tự *c* là một chữ số thập lục phân (``0-9``, ``a-f`` và ``A-F``).


.. c:macro:: Py_TOLOWER(c)

   Trả về ký tự tương đương viết thường của *c*.


.. c:macro:: Py_TOUPPER(c)

   Trả về ký tự tương đương viết hoa của *c*.
