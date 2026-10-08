:mod:`!locale` --- Dịch vụ quốc tế hóa
======================================

.. module:: locale
   :synopsis: Dịch vụ quốc tế hóa.

.. moduleauthor:: Martin von Löwis <martin@v.loewis.de>
.. sectionauthor:: Martin von Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/locale.py`

--------------

Mô-đun :mod:`!locale` cung cấp quyền truy cập vào cơ sở dữ liệu locale POSIX và các chức năng liên quan. Cơ chế locale POSIX cho phép lập trình viên xử lý một số vấn đề văn hóa trong ứng dụng mà không cần biết mọi đặc điểm cụ thể của từng quốc gia nơi phần mềm được thực thi.

.. index:: pair: module; _locale

Mô-đun :mod:`!locale` được triển khai dựa trên mô-đun :mod:`!_locale`, đến lượt mô-đun này sử dụng triển khai locale ANSI C nếu có.

Mô-đun :mod:`!locale` định nghĩa ngoại lệ và các hàm sau đây:


.. exception:: Error

   Ngoại lệ được phát sinh khi locale được truyền vào :func:`setlocale` không được nhận dạng.


.. function:: setlocale(category, locale=None)

   Nếu *locale* được cung cấp và không phải ``None``, :func:`setlocale` sẽ thay đổi thiết lập locale cho *category*. Các category khả dụng được liệt kê trong phần mô tả dữ liệu bên dưới. *locale* có thể là một :ref:`string <locale_name>`, hoặc một cặp gồm mã ngôn ngữ và encoding. Chuỗi rỗng chỉ định các thiết lập mặc định của người dùng. Nếu việc thay đổi locale không thành công, ngoại lệ
   :exc:`Error` sẽ được nêu ra. Nếu thành công, thiết lập locale mới sẽ được trả về.

   Nếu *locale* là một cặp, cặp này được chuyển đổi thành tên locale bằng công cụ alias locale. Mã ngôn ngữ có cùng định dạng với :ref:`locale name <locale_name>`, nhưng không có encoding và bộ sửa đổi ``@``. Mã ngôn ngữ và encoding có thể được ``None``.

   Nếu *locale* bị bỏ qua hoặc là ``None``, thiết lập hiện tại cho *category* sẽ được trả về.

   Ví dụ::

      >>> import locale
      >>> loc = locale.setlocale(locale.LC_ALL)  # lấy locale hiện tại
      # sử dụng locale tiếng Đức; tên và khả năng cung cấp thay đổi tùy nền tảng
      >>> locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
      >>> locale.strcoll('f\xe4n', 'foo')  # so sánh một chuỗi chứa ký tự umlaut
      >>> locale.setlocale(locale.LC_ALL, '')   # sử dụng locale người dùng предпоч thích
      >>> locale.setlocale(locale.LC_ALL, 'C')  # sử dụng locale mặc định (C)
      >>> locale.setlocale(locale.LC_ALL, loc)  # khôi phục locale đã lưu

   :func:`setlocale` không an toàn với luồng trên hầu hết các hệ thống. Các ứng dụng thường bắt đầu bằng một lệnh gọi đến::

      import locale
      locale.setlocale(locale.LC_ALL, '')

   Thao tác này đặt locale cho tất cả các danh mục thành thiết lập mặc định của người dùng (thường được chỉ định trong biến môi trường :envvar:`LANG`). Nếu locale không được thay đổi sau đó, việc sử dụng đa luồng sẽ không gây ra vấn đề.


.. function:: localeconv()

   Trả về cơ sở dữ liệu về các quy ước địa phương dưới dạng một dictionary. Dictionary này có các chuỗi sau làm khóa:

   .. tabularcolumns:: |l|l|L|

   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   | Danh mục             | Khóa                                | Ý nghĩa                                                                                                                               |
   +======================+=====================================+=======================================================================================================================================+
   | :const:`LC_NUMERIC`  | ``'decimal_point'``                 | Ký tự dấu thập phân.                                                                                                                  |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'grouping'``                      | Chuỗi các số chỉ định những vị trí tương đối mà ``'thousands_sep'`` được mong đợi. Nếu chuỗi kết thúc bằng                            |
   |                      |                                     | :const:`CHAR_MAX`, sẽ không thực hiện nhóm nào nữa. Nếu chuỗi kết thúc bằng ``0``, kích thước nhóm cuối cùng sẽ được sử dụng lặp lại. |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'thousands_sep'``                 | Ký tự được sử dụng giữa các nhóm.                                                                                                     |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`LC_MONETARY` | ``'int_curr_symbol'``               | Ký hiệu tiền tệ quốc tế.                                                                                                              |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'currency_symbol'``               | Ký hiệu tiền tệ địa phương.                                                                                                           |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'p_cs_precedes/n_cs_precedes'``   | Ký hiệu tiền tệ có đứng trước giá trị hay không (đối với các giá trị dương và âm tương ứng).                                          |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'p_sep_by_space/n_sep_by_space'`` | Ký hiệu tiền tệ có được ngăn cách với giá trị bằng một dấu cách hay không (đối với các giá trị dương và âm tương ứng).                |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'mon_decimal_point'``             | Dấu thập phân được sử dụng cho các giá trị tiền tệ.                                                                                   |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'frac_digits'``                   | Số chữ số phần thập phân được sử dụng khi định dạng các giá trị tiền tệ theo địa phương.                                              |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'int_frac_digits'``               | Số chữ số phần thập phân được sử dụng khi định dạng các giá trị tiền tệ theo quốc tế.                                                 |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'mon_thousands_sep'``             | Dấu phân cách nhóm được dùng cho các giá trị tiền tệ.                                                                                 |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'mon_grouping'``                  | Tương đương với ``'grouping'``, được dùng cho các giá trị tiền tệ.                                                                    |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'positive_sign'``                 | Ký hiệu dùng để chú thích một giá trị tiền tệ dương.                                                                                  |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'negative_sign'``                 | Ký hiệu dùng để chú thích một giá trị tiền tệ âm.                                                                                     |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
   |                      | ``'p_sign_posn/n_sign_posn'``       | Vị trí của dấu (tương ứng với các giá trị dương và âm), xem bên dưới.                                                                 |
   +----------------------+-------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+

   Tất cả các giá trị số có thể được đặt thành :const:`CHAR_MAX` để cho biết rằng không có giá trị nào được chỉ định trong locale này.

   Các giá trị có thể có của ``'p_sign_posn'`` và ``'n_sign_posn'`` được nêu bên dưới.

   +--------------+---------------------------------------------------------+
   | Giá trị      | Giải thích                                              |
   +==============+=========================================================+
   | ``0``        | Đơn vị tiền tệ và giá trị được đặt trong dấu ngoặc đơn. |
   +--------------+---------------------------------------------------------+
   | ``1``        | Dấu phải đứng trước giá trị và ký hiệu tiền tệ.         |
   +--------------+---------------------------------------------------------+
   | ``2``        | Dấu phải đứng sau giá trị và ký hiệu tiền tệ.           |
   +--------------+---------------------------------------------------------+
   | ``3``        | Dấu phải đứng ngay trước giá trị.                       |
   +--------------+---------------------------------------------------------+
   | ``4``        | Dấu phải đứng ngay sau giá trị.                         |
   +--------------+---------------------------------------------------------+
   | ``CHAR_MAX`` | Không có thông tin nào được chỉ định trong locale này.  |
   +--------------+---------------------------------------------------------+

   Hàm này tạm thời đặt locale ``LC_CTYPE`` thành locale ``LC_NUMERIC`` hoặc locale ``LC_MONETARY`` nếu các locale khác nhau và các chuỗi số hoặc tiền tệ không phải ASCII. Thay đổi tạm thời này ảnh hưởng đến các thread khác.

   .. versionchanged:: 3.7
      Trong một số trường hợp, hàm này hiện tạm thời đặt locale ``LC_CTYPE`` thành locale ``LC_NUMERIC``.


.. function:: nl_langinfo(option)

   Trả về một số thông tin dành riêng cho locale dưới dạng chuỗi. Hàm này không có trên tất cả các hệ thống và tập hợp tùy chọn có thể có cũng khác nhau giữa các nền tảng. Các giá trị đối số có thể có là các số, với các hằng số tượng trưng tương ứng có trong module locale.

   Hàm :func:`nl_langinfo` chấp nhận một trong các khóa sau. Phần lớn mô tả được lấy từ mô tả tương ứng trong thư viện GNU C.

   .. data:: CODESET

      Lấy một chuỗi chứa tên của encoding ký tự được sử dụng trong locale đã chọn.

   .. data:: D_T_FMT

      Lấy một chuỗi có thể được sử dụng làm chuỗi định dạng cho :func:`time.strftime` để biểu diễn ngày và giờ theo cách dành riêng cho locale.

   .. data:: D_FMT

      Lấy một chuỗi có thể được dùng làm chuỗi định dạng cho :func:`time.strftime` để biểu diễn ngày theo cách phù hợp với từng locale.

   .. data:: T_FMT

      Lấy một chuỗi có thể được dùng làm chuỗi định dạng cho :func:`time.strftime` để biểu diễn thời gian theo cách phù hợp với từng locale.

   .. data:: T_FMT_AMPM

      Lấy một chuỗi định dạng cho :func:`time.strftime` để biểu diễn thời gian theo định dạng am/pm.

   .. data:: DAY_1
             DAY_2 DAY_3 DAY_4 DAY_5 DAY_6 DAY_7

      Lấy tên của ngày thứ n trong tuần.

      .. note::

         Điều này tuân theo quy ước của Hoa Kỳ, trong đó :const:`DAY_1` là Chủ nhật, thay vì quy ước quốc tế (ISO 8601), theo đó thứ Hai là ngày đầu tiên trong tuần.

   .. data:: ABDAY_1
             ABDAY_2 ABDAY_3 ABDAY_4 ABDAY_5 ABDAY_6 ABDAY_7

      Lấy tên viết tắt của ngày thứ n trong tuần.

   .. data:: MON_1
             MON_2 MON_3 MON_4 MON_5 MON_6 MON_7 MON_8 MON_9 MON_10 MON_11 MON_12

      Lấy tên của tháng thứ n.

   .. data:: ABMON_1
             ABMON_2 ABMON_3 ABMON_4 ABMON_5 ABMON_6 ABMON_7 ABMON_8 ABMON_9 ABMON_10 ABMON_11 ABMON_12

      Lấy tên viết tắt của tháng thứ n.

   .. data:: RADIXCHAR

      Lấy ký tự cơ số (dấu chấm thập phân, dấu phẩy thập phân, v.v.).

   .. data:: THOUSEP

      Lấy ký tự phân cách hàng nghìn (các nhóm gồm ba chữ số).

   .. data:: YESEXPR

      Lấy một biểu thức chính quy có thể được sử dụng với hàm regex để nhận diện câu trả lời khẳng định cho câu hỏi có/không.

   .. data:: NOEXPR

      Lấy một biểu thức chính quy có thể được sử dụng với hàm ``regex(3)`` để nhận diện câu trả lời phủ định cho câu hỏi có/không.

      .. note::

         Các biểu thức chính quy cho :const:`YESEXPR` và
         :const:`NOEXPR` sử dụng cú pháp phù hợp với hàm ``regex`` từ thư viện C, có thể khác với cú pháp được sử dụng trong :mod:`re`.

   .. data:: CRNCYSTR

      Lấy ký hiệu tiền tệ, có thêm "-" ở trước nếu ký hiệu phải xuất hiện trước giá trị, "+" nếu ký hiệu phải xuất hiện sau giá trị hoặc "." nếu ký hiệu phải thay thế ký tự phân cách phần nguyên.

   .. data:: ERA

      Lấy một chuỗi mô tả cách tính và hiển thị năm cho từng thời đại trong một locale.

      Hầu hết locale không định nghĩa giá trị này. Một ví dụ về locale có định nghĩa giá trị này là locale Nhật Bản. Ở Nhật Bản, cách biểu diễn ngày tháng truyền thống bao gồm tên thời đại tương ứng với triều đại của vị hoàng đế đương thời.

      Thông thường, không cần thiết phải sử dụng trực tiếp giá trị này. Việc chỉ định bổ từ ``E`` trong các chuỗi định dạng của chúng khiến hàm :func:`time.strftime` sử dụng thông tin này. Định dạng của chuỗi được trả về được quy định trong *The Open Group Base Specifications Issue 8*, đoạn `7.3.5.2 LC_TIME C-Language Access <https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap07.html#tag_07_03_05_02>`_.

   .. data:: ERA_D_T_FMT

      Lấy một chuỗi định dạng cho :func:`time.strftime` để biểu diễn ngày và giờ theo cách dựa trên kỷ nguyên, đặc thù theo locale.

   .. data:: ERA_D_FMT

      Lấy một chuỗi định dạng cho :func:`time.strftime` để biểu diễn ngày theo cách dựa trên kỷ nguyên, đặc thù theo locale.

   .. data:: ERA_T_FMT

      Lấy một chuỗi định dạng cho :func:`time.strftime` để biểu diễn giờ theo cách dựa trên kỷ nguyên, đặc thù theo locale.

   .. data:: ALT_DIGITS

      Lấy một chuỗi gồm tối đa 100 ký hiệu, được phân tách bằng dấu chấm phẩy, dùng để biểu diễn các giá trị từ 0 đến 99 theo cách đặc thù theo locale. Trong hầu hết locale, đây là một chuỗi rỗng.

   Hàm tạm thời đặt locale ``LC_CTYPE`` thành locale của category xác định giá trị được yêu cầu (``LC_TIME``, ``LC_NUMERIC``, ``LC_MONETARY`` hoặc ``LC_MESSAGES``) nếu các locale khác nhau và chuỗi kết quả không phải ASCII. Thay đổi tạm thời này ảnh hưởng đến các thread khác.

   .. versionchanged:: 3.14
      Hàm hiện tạm thời đặt locale ``LC_CTYPE`` trong một số trường hợp.


.. function:: getdefaultlocale([envvars])

   Cố gắng xác định các thiết lập locale mặc định và trả về chúng dưới dạng một tuple có dạng ``(language code, encoding)``.

   Theo POSIX, một chương trình chưa gọi ``setlocale(LC_ALL, '')`` sẽ chạy bằng locale ``'C'`` khả chuyển. Việc gọi ``setlocale(LC_ALL, '')`` cho phép chương trình sử dụng locale mặc định được xác định bởi biến :envvar:`LANG`. Vì không muốn can thiệp vào thiết lập locale hiện tại, chúng ta mô phỏng hành vi theo cách được mô tả ở trên.

   Để duy trì khả năng tương thích với các nền tảng khác, không chỉ biến :envvar:`LANG` được kiểm tra mà còn có một danh sách các biến được cung cấp dưới dạng tham số envvars. Biến đầu tiên được tìm thấy là đã được định nghĩa sẽ được sử dụng. *envvars* mặc định là đường dẫn tìm kiếm được GNU gettext sử dụng; đường dẫn này luôn phải chứa tên biến ``'LANG'``. Đường dẫn tìm kiếm của GNU gettext chứa ``'LC_ALL'``, ``'LC_CTYPE'``, ``'LANG'`` và ``'LANGUAGE'``, theo thứ tự đó.

   Mã ngôn ngữ có cùng định dạng với :ref:`tên locale <locale_name>`, nhưng không có encoding và ``@``-modifier. Mã ngôn ngữ và encoding có thể là ``None`` nếu không thể xác định được giá trị của chúng. Locale "C" được biểu diễn bằng ``(None, None)``.


.. function:: getlocale(category=LC_CTYPE)

   Trả về thiết lập hiện tại của danh mục locale đã cho dưới dạng một tuple chứa mã ngôn ngữ và encoding. *category* có thể là một trong các giá trị :const:`!LC_\*`, ngoại trừ :const:`LC_ALL`. Giá trị mặc định là :const:`LC_CTYPE`.

   Mã ngôn ngữ có cùng định dạng với :ref:`tên locale <locale_name>`, nhưng không có encoding và ``@``-modifier. Mã ngôn ngữ và encoding có thể là ``None`` nếu không thể xác định được giá trị của chúng. Locale "C" được biểu diễn bằng ``(None, None)``.


.. function:: getpreferredencoding(do_setlocale=True)

   Trả về :term:`locale encoding` được sử dụng cho dữ liệu văn bản theo tùy chọn của người dùng. Tùy chọn của người dùng được biểu đạt khác nhau trên các hệ thống khác nhau và có thể không khả dụng theo cách lập trình trên một số hệ thống, vì vậy hàm này chỉ trả về một phỏng đoán.

   Trên một số hệ thống, cần gọi :func:`setlocale` để lấy tùy chọn của người dùng, vì vậy hàm này không an toàn khi sử dụng trong nhiều luồng. Nếu không cần hoặc không muốn gọi setlocale, *do_setlocale* nên được đặt thành ``False``.

   Trên Android hoặc khi :ref:`Python UTF-8 Mode <utf8-mode>` được bật, luôn trả về ``'utf-8'``; đối số :term:`locale encoding` và *do_setlocale* sẽ bị bỏ qua.

   :ref:`Python preinitialization <c-preinit>` cấu hình locale LC_CTYPE. Xem thêm :term:`filesystem encoding and error handler`.

   .. versionchanged:: 3.7
      Hàm này hiện luôn trả về ``"utf-8"`` trên Android hoặc khi
      :ref:`Python UTF-8 Mode <utf8-mode>` được bật.


.. function:: getencoding()

   Lấy :term:`locale encoding` hiện tại:

   * Trên Android và VxWorks, trả về ``"utf-8"``.
   * Trên Unix, trả về encoding của locale :data:`LC_CTYPE` hiện tại. Trả về ``"utf-8"`` nếu ``nl_langinfo(CODESET)`` trả về chuỗi rỗng, chẳng hạn khi locale LC_CTYPE hiện tại không được hỗ trợ.
   * Trên Windows, trả về trang mã ANSI.

   :ref:`Python preinitialization <c-preinit>` cấu hình locale LC_CTYPE. Xem thêm :term:`filesystem encoding and error handler`.

   Hàm này tương tự như
   :func:`getpreferredencoding(False) <getpreferredencoding>`, ngoại trừ việc hàm này bỏ qua :ref:`Python UTF-8 Mode <utf8-mode>`.

   .. versionadded:: 3.11


.. function:: normalize(localename)

   Trả về mã locale đã được chuẩn hóa cho tên locale đã cho. Mã locale được trả về có định dạng để sử dụng với :func:`setlocale`. Nếu chuẩn hóa không thành công, tên ban đầu được trả về mà không thay đổi.

   Nếu encoding đã cho không xác định, hàm sẽ sử dụng encoding mặc định cho mã locale, giống như :func:`setlocale`.


.. function:: strcoll(string1, string2)

   So sánh hai chuỗi theo thiết lập :const:`LC_COLLATE` hiện tại. Giống như mọi hàm so sánh khác, hàm này trả về một giá trị âm, dương hoặc ``0``, tùy thuộc vào việc *string1* được sắp xếp trước hay sau *string2*, hoặc bằng với chuỗi đó.


.. function:: strxfrm(string)

   Chuyển đổi một chuỗi thành chuỗi có thể được dùng trong các phép so sánh phụ thuộc vào locale. Ví dụ: ``strxfrm(s1) < strxfrm(s2)`` tương đương với ``strcoll(s1, s2) < 0``. Có thể dùng hàm này khi một chuỗi được so sánh nhiều lần, chẳng hạn như khi sắp xếp một chuỗi các chuỗi.


.. function:: format_string(format, val, grouping=False, monetary=False)

   Định dạng một số *val* theo thiết lập :const:`LC_NUMERIC` hiện tại. Định dạng này tuân theo quy ước của toán tử ``%``. Đối với các giá trị dấu phẩy động, dấu thập phân sẽ được thay đổi nếu thích hợp. Nếu *grouping* là ``True``, hàm cũng tính đến việc phân nhóm.

   Nếu *monetary* là true, phép chuyển đổi sẽ sử dụng chuỗi phân cách hàng nghìn và phân nhóm tiền tệ.

   Xử lý các bộ chỉ định định dạng như trong ``format % val``, nhưng có tính đến các thiết lập locale hiện tại.

   .. versionchanged:: 3.7
      Đã thêm tham số từ khóa *monetary*.


.. function:: currency(val, symbol=True, grouping=False, international=False)

   Định dạng một số *val* theo các thiết lập :const:`LC_MONETARY` hiện tại.

   Chuỗi được trả về bao gồm ký hiệu tiền tệ nếu *symbol* là true, đây là giá trị mặc định. Nếu *grouping* là ``True`` (không phải giá trị mặc định), việc nhóm được thực hiện bằng giá trị đó. Nếu *international* là ``True`` (không phải giá trị mặc định), ký hiệu tiền tệ quốc tế sẽ được sử dụng.

   .. note::

     Hàm này sẽ không hoạt động với locale 'C', vì vậy trước tiên bạn phải đặt locale thông qua :func:`setlocale`.


.. function:: str(float)

   Định dạng một số dấu phẩy động bằng cùng định dạng với hàm tích hợp sẵn ``str(float)``, nhưng có tính đến dấu thập phân.


.. function:: delocalize(string)

    Chuyển đổi một chuỗi thành chuỗi số đã chuẩn hóa, theo các
    thiết lập :const:`LC_NUMERIC`.

    .. versionadded:: 3.5


.. function:: localize(string, grouping=False, monetary=False)

    Chuyển đổi một chuỗi số đã chuẩn hóa thành chuỗi đã định dạng theo các
    thiết lập :const:`LC_NUMERIC`.

    .. versionadded:: 3.10


.. function:: atof(string, func=float)

   Chuyển đổi một chuỗi thành một số theo các thiết lập :const:`LC_NUMERIC`, bằng cách gọi *func* trên kết quả của việc gọi :func:`delocalize` với *string*.


.. function:: atoi(string)

   Chuyển đổi một chuỗi thành một số nguyên theo các quy ước :const:`LC_NUMERIC`.


.. data:: LC_CTYPE

   Danh mục locale dành cho các hàm về kiểu ký tự. Quan trọng nhất, danh mục này xác định mã hóa văn bản, tức là cách diễn giải các byte thành các codepoint Unicode. Xem :pep:`538` và :pep:`540` để biết cách biến này có thể được tự động chuyển thành ``C.UTF-8`` nhằm tránh các vấn đề do thiết lập không hợp lệ trong container hoặc các thiết lập không tương thích được truyền qua kết nối SSH từ xa.

   Python không sử dụng nội bộ các hàm chuyển đổi ký tự phụ thuộc vào locale từ ``ctype.h``. Thay vào đó, ``pyctype.h`` cung cấp các hàm tương đương không phụ thuộc vào locale như :c:macro:`Py_TOLOWER`.


.. data:: LC_COLLATE

   Danh mục locale dành cho việc sắp xếp chuỗi. Các hàm :func:`strcoll` và
   :func:`strxfrm` của mô-đun :mod:`!locale` bị ảnh hưởng.


.. data:: LC_TIME

   Danh mục locale dành cho việc định dạng thời gian. Hàm :func:`time.strftime` tuân theo các quy ước này.


.. data:: LC_MONETARY

   Loại locale dùng để định dạng các giá trị tiền tệ. Các tùy chọn khả dụng được cung cấp bởi hàm :func:`localeconv`.


.. data:: LC_MESSAGES

   Loại locale dùng để hiển thị thông báo. Hiện tại Python không hỗ trợ các thông báo phụ thuộc locale dành riêng cho ứng dụng. Các thông báo do hệ điều hành hiển thị, chẳng hạn như những thông báo được trả về bởi :func:`os.strerror`, có thể bị ảnh hưởng bởi loại này.

   Giá trị này có thể không khả dụng trên các hệ điều hành không tuân theo tiêu chuẩn POSIX, đặc biệt là Windows.


.. data:: LC_NUMERIC

   Loại locale dùng để định dạng số. Các hàm :func:`format_string`,
   :func:`atoi`, :func:`atof` và :func:`.str` của mô-đun :mod:`!locale` chịu ảnh hưởng của loại này. Tất cả các thao tác định dạng số khác đều không bị ảnh hưởng.


.. data:: LC_ALL

   Kết hợp tất cả các thiết lập locale. Nếu cờ này được sử dụng khi locale được thay đổi, hệ thống sẽ cố gắng thiết lập locale cho tất cả các loại. Nếu việc đó thất bại đối với bất kỳ loại nào, sẽ không có loại nào bị thay đổi. Khi locale được truy xuất bằng cờ này, một chuỗi cho biết thiết lập của tất cả các loại sẽ được trả về. Sau đó, có thể sử dụng chuỗi này để khôi phục các thiết lập.


.. data:: CHAR_MAX

   Đây là một hằng số tượng trưng được sử dụng cho các giá trị khác nhau được trả về bởi
   :func:`localeconv`.


Bối cảnh, chi tiết, gợi ý, mẹo và lưu ý
---------------------------------------

Tiêu chuẩn C định nghĩa locale là một thuộc tính trên toàn chương trình và việc thay đổi nó có thể tương đối tốn kém. Ngoài ra, một số implementation bị lỗi đến mức việc thay đổi locale thường xuyên có thể gây ra core dump. Vì vậy, việc sử dụng locale đúng cách có phần khó khăn.

Ban đầu, khi một chương trình được khởi động, locale là locale ``C``, bất kể locale ưa thích của người dùng là gì. Có một ngoại lệ:
category :data:`LC_CTYPE` được thay đổi khi khởi động để đặt encoding locale hiện tại thành encoding locale ưa thích của người dùng. Chương trình phải nói rõ rằng nó muốn sử dụng các cài đặt locale ưa thích của người dùng cho những category khác bằng cách gọi ``setlocale(LC_ALL, '')``.

Nhìn chung, gọi :func:`setlocale` trong một routine của library là một ý tưởng tồi, vì như một tác dụng phụ, nó ảnh hưởng đến toàn bộ chương trình. Việc lưu và khôi phục nó cũng gần như tệ không kém: thao tác này tốn kém và ảnh hưởng đến các thread khác tình cờ chạy trước khi cài đặt được khôi phục.

Nếu khi viết một module dùng chung, bạn cần một phiên bản không phụ thuộc vào locale của một thao tác chịu ảnh hưởng bởi locale (chẳng hạn như một số format được dùng với :func:`time.strftime`), bạn sẽ phải tìm cách thực hiện việc đó mà không sử dụng routine của standard library. Tốt hơn nữa là tự thuyết phục mình rằng việc sử dụng các cài đặt locale là ổn. Chỉ nên xem việc ghi rõ rằng module của bạn không tương thích với các cài đặt locale không phải \ ``C`` là phương án cuối cùng.

Cách duy nhất để thực hiện các thao tác số theo locale là sử dụng các hàm đặc biệt được định nghĩa bởi module này: :func:`atof`, :func:`atoi`,
:func:`format_string`, :func:`.str`.

Không có cách nào thực hiện việc chuyển đổi kiểu chữ và phân loại ký tự theo locale. Đối với các chuỗi văn bản (Unicode), những thao tác này chỉ dựa trên giá trị ký tự, còn đối với các chuỗi byte, việc chuyển đổi và phân loại dựa trên giá trị ASCII của byte; các byte có bit cao được bật (tức là các byte không phải ASCII) không bao giờ được chuyển đổi hoặc được xem là thuộc một lớp ký tự như chữ cái hay khoảng trắng.


.. _locale_name:

Tên locale
----------

Định dạng của tên locale phụ thuộc vào nền tảng và tập hợp locale được hỗ trợ có thể phụ thuộc vào cấu hình hệ thống.

Trên các nền tảng Posix, tên này thường có định dạng [1]_:

.. productionlist:: locale_name
   : language ["_" territory] ["." charset] ["@" modifier]

trong đó *language* là mã ngôn ngữ gồm hai hoặc ba chữ cái theo `ISO 639 <ISO 639_>`_, *territory* là mã quốc gia hoặc khu vực gồm hai chữ cái theo `ISO 3166 <ISO 3166_>`_, *charset* là encoding của locale, còn *modifier* là tên tập lệnh, language subtag, mã nhận dạng thứ tự sắp xếp hoặc modifier khác của locale (ví dụ: "latin", "valencia", "stroke" và "euro").

Trên Windows, có một số định dạng được hỗ trợ. [2]_ [3]_ Một tập con các thẻ `IETF BCP 47 <IETF BCP 47_>`_:

.. productionlist:: locale_name
   : language ["-" script] ["-" territory] ["." charset]
   : language ["-" script] "-" territory "-" modifier

trong đó *language* và *territory* có cùng ý nghĩa như trên Posix, *script* là mã tập lệnh gồm bốn chữ cái theo `ISO 15924 <ISO 15924_>`_, còn *modifier* là language subtag, mã nhận dạng thứ tự sắp xếp hoặc modifier tùy chỉnh (ví dụ: "valencia", "stroke" hoặc "x-python"). Cả dấu gạch nối (``'-'``) và dấu gạch dưới (``'_'``) đều được hỗ trợ làm dấu phân cách. Chỉ cho phép encoding UTF-8 đối với các thẻ BCP 47.

Windows cũng hỗ trợ tên locale theo định dạng:

.. productionlist:: locale_name
   : language ["_" territory] ["." charset]

trong đó *ngôn ngữ* và *lãnh thổ* là tên đầy đủ, chẳng hạn như "English" và "United States", còn *bộ ký tự* là số code page (ví dụ: "1252") hoặc UTF-8. Chỉ dấu phân cách dấu gạch dưới được hỗ trợ trong định dạng này.

Locale "C" được hỗ trợ trên mọi nền tảng.

.. _ISO 639: https://www.iso.org/iso-639-language-code
.. _ISO 3166: https://www.iso.org/iso-3166-country-codes.html
.. _IETF BCP 47: https://www.rfc-editor.org/info/bcp47
.. _ISO 15924: https://www.unicode.org/iso15924/

.. [1] `IEEE Std 1003.1-2024; 8.2 Internationalization Variables <https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html#tag_08_02>`_
.. [2] `UCRT Locale names, Languages, and Country/Region strings <https://learn.microsoft.com/en-us/cpp/c-runtime-library/locale-names-languages-and-country-region-strings>`_
.. [3] `Locale Names <https://learn.microsoft.com/en-us/windows/win32/intl/locale-names>`_


.. _embedding-locale:

Dành cho người viết extension và các chương trình nhúng Python
--------------------------------------------------------------

Các module mở rộng không bao giờ được gọi :func:`setlocale`, ngoại trừ để tìm hiểu locale hiện tại là gì. Tuy nhiên, vì giá trị trả về chỉ có thể được sử dụng một cách khả chuyển để khôi phục locale, nên việc này không mấy hữu ích (ngoại trừ có lẽ để tìm hiểu locale có phải là ``C`` hay không).

Khi mã Python sử dụng module :mod:`!locale` để thay đổi locale, điều này cũng ảnh hưởng đến ứng dụng nhúng. Nếu ứng dụng nhúng không muốn điều này xảy ra, ứng dụng đó nên loại bỏ module mở rộng :mod:`!_locale` (module thực hiện toàn bộ công việc) khỏi bảng các module dựng sẵn trong tệp :file:`config.c`, đồng thời bảo đảm module :mod:`!_locale` không thể được truy cập dưới dạng shared library.


.. _locale-gettext:

Truy cập các message catalog
----------------------------

.. function:: gettext(msg)
.. function:: dgettext(domain, msg)
.. function:: dcgettext(domain, msg, category)
.. function:: textdomain(domain)
.. function:: bindtextdomain(domain, dir)
.. function:: bind_textdomain_codeset(domain, codeset)

Module locale cung cấp interface gettext của thư viện C trên các hệ thống có hỗ trợ interface này. Interface này gồm các hàm :func:`gettext`,
:func:`dgettext`, :func:`dcgettext`, :func:`textdomain`, :func:`bindtextdomain`, và :func:`bind_textdomain_codeset`. Các hàm này tương tự những hàm cùng tên trong module :mod:`gettext`, nhưng sử dụng định dạng nhị phân của thư viện C cho message catalog và các thuật toán tìm kiếm của thư viện C để định vị message catalog.

Các ứng dụng Python thông thường không cần gọi những hàm này và nên sử dụng :mod:`gettext` thay vào đó. Một ngoại lệ đã biết đối với quy tắc này là các ứng dụng liên kết với những thư viện C bổ sung, vốn gọi nội bộ các hàm C ``gettext`` hoặc ``dcgettext``. Với các ứng dụng này, có thể cần bind text domain để các thư viện có thể định vị đúng message catalog của chúng.

.. _`7.3.5.2 LC_TIME C-Language Access`: https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap07.html#tag_07_03_05_02
.. _`IEEE Std 1003.1-2024; 8.2 Internationalization Variables`: https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html#tag_08_02
.. _`UCRT Locale names, Languages, and Country/Region strings`: https://learn.microsoft.com/en-us/cpp/c-runtime-library/locale-names-languages-and-country-region-strings
.. _`Locale Names`: https://learn.microsoft.com/en-us/windows/win32/intl/locale-names
