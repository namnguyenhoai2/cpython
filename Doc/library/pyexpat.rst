:mod:`!xml.parsers.expat` --- Phân tích XML nhanh bằng Expat
============================================================

.. module:: xml.parsers.expat
   :synopsis: Giao diện cho trình phân tích cú pháp XML không xác thực Expat.

.. moduleauthor:: Paul Prescod <paul@prescod.net>

--------------

.. Markup notes:

   Many of the attributes of the XMLParser objects are callbacks.  Since
   signature information must be presented, these are described using the method
   directive.  Since they are attributes which are set by client code, in-text
   references to these attributes should be marked using the :member: role.


.. note::

   Nếu bạn cần phân tích dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem
   :ref:`xml-security`.


.. index:: single: Expat

Mô-đun :mod:`!xml.parsers.expat` là một giao diện Python cho trình phân tích cú pháp XML không xác thực Expat. Mô-đun này cung cấp một kiểu mở rộng duy nhất,
:class:`xmlparser`, đại diện cho trạng thái hiện tại của một trình phân tích cú pháp XML. Sau khi một đối tượng :class:`xmlparser` được tạo, bạn có thể đặt nhiều thuộc tính của đối tượng này thành các hàm handler. Khi một tài liệu XML được đưa vào trình phân tích cú pháp, các hàm handler sẽ được gọi cho dữ liệu ký tự và markup trong tài liệu XML.

.. index:: pair: module; pyexpat

Mô-đun này sử dụng mô-đun :mod:`pyexpat` để cung cấp quyền truy cập vào trình phân tích cú pháp Expat. Việc sử dụng trực tiếp mô-đun :mod:`pyexpat` đã bị ngừng sử dụng.

Mô-đun này cung cấp ngoại lệ, đối tượng kiểu và các mục dữ liệu sau đây:


.. exception:: ExpatError

   Ngoại lệ được phát sinh khi Expat báo lỗi. Xem phần
   :ref:`expaterror-objects` để biết thêm thông tin về cách diễn giải các lỗi của Expat.


.. exception:: error

   Bí danh của :exc:`ExpatError`.


.. data:: XMLParserType

   Kiểu của các giá trị trả về từ hàm :func:`ParserCreate`.


.. data:: EXPAT_VERSION

   Chuỗi phiên bản của thư viện Expat được trình thông dịch tải, chẳng hạn như ``'expat_2.8.4'``.


.. data:: version_info

   Phiên bản của thư viện Expat được trình thông dịch tải, dưới dạng một bộ gồm ba số nguyên: phiên bản major, minor và micro.


.. data:: features

   Danh sách các tính năng mà thư viện Expat được tải đã được biên dịch cùng, dưới dạng các cặp ``(name, value)``. Giá trị này chỉ có ý nghĩa đối với những tính năng có giá trị, chẳng hạn như ``'XML_CONTEXT_BYTES'`` hoặc các giới hạn bảo vệ mặc định ``'XML_BLAP_ACT_THRES'`` và ``'XML_AT_MAX_AMP'``; đối với các tính năng khác, như ``'XML_DTD'`` và ``'XML_NS'``, giá trị là ``0`` và chỉ sự hiện diện của tên mới quan trọng.

Mô-đun :mod:`!xml.parsers.expat` chứa hai hàm:


.. function:: ErrorString(errno)

   Trả về một chuỗi giải thích cho số lỗi *errno* đã cho.


.. function:: ParserCreate(encoding=None, namespace_separator=None, intern=None)

   Tạo và trả về một đối tượng :class:`xmlparser` mới.   *encoding*, nếu được chỉ định, phải là một chuỗi chỉ rõ encoding được dữ liệu XML sử dụng. Expat không hỗ trợ nhiều encoding như Python và không thể mở rộng tập hợp encoding của nó; nó hỗ trợ UTF-8, UTF-16, ISO-8859-1 (Latin1) và ASCII. Nếu *encoding* [1]_ được cung cấp, nó sẽ ghi đè encoding ngầm định hoặc tường minh của tài liệu.

   .. _xmlparser-non-root:

   Các parser được tạo thông qua :func:`!ParserCreate` được gọi là parser "root", theo nghĩa là chúng không có parser cha nào được gắn vào. Các parser không phải root được tạo bởi :meth:`parser.ExternalEntityParserCreate <xmlparser.ExternalEntityParserCreate>`.

   Expat có thể tùy chọn thực hiện xử lý XML namespace cho bạn; tính năng này được bật bằng cách cung cấp một giá trị cho *namespace_separator*. Giá trị này phải là một chuỗi gồm một ký tự; một
   :exc:`ValueError` sẽ được phát sinh nếu chuỗi có độ dài không hợp lệ (``None`` được xem là tương đương với việc bỏ qua). Khi bật xử lý namespace, tên kiểu phần tử và tên thuộc tính thuộc về một namespace sẽ được mở rộng. Tên phần tử được truyền cho các trình xử lý phần tử
   :attr:`StartElementHandler` và :attr:`EndElementHandler` sẽ là phần ghép của URI namespace, ký tự phân tách namespace và phần cục bộ của tên. Nếu dấu phân tách namespace là một byte 0 (``chr(0)``) thì URI namespace và phần cục bộ sẽ được ghép lại mà không có dấu phân tách.

   Ví dụ: nếu *namespace_separator* được đặt thành một ký tự khoảng trắng (``' '``) và tài liệu sau được phân tích cú pháp:

   .. code-block:: xml

      <?xml version="1.0"?>
      <root xmlns    = "http://default-namespace.org/"
            xmlns:py = "http://www.python.org/ns/">
        <py:elem1 />
        <elem2 xmlns="" />
      </root>

   :attr:`StartElementHandler` sẽ nhận các chuỗi sau cho từng phần tử::

      http://default-namespace.org/ root
      http://www.python.org/ns/ elem1
      elem2

   *intern*, nếu được cung cấp, phải là một dictionary. Nó được dùng để intern tên của các phần tử và thuộc tính, đồng thời có sẵn dưới dạng thuộc tính :attr:`~xmlparser.intern`. Theo mặc định, một dictionary trống mới được tạo cho mỗi parser.

   Do các hạn chế trong thư viện ``Expat`` được :mod:`pyexpat` sử dụng, instance :class:`xmlparser` được trả về chỉ có thể được dùng để phân tích cú pháp một tài liệu XML duy nhất. Gọi ``ParserCreate`` cho mỗi tài liệu để cung cấp các parser instance duy nhất.


.. seealso::

   `Trình phân tích cú pháp XML Expat <http://www.libexpat.org/>`_
      Trang chủ của dự án Expat.


.. _xmlparser-objects:

Các đối tượng XMLParser
-----------------------

Các đối tượng :class:`xmlparser` có các phương thức sau:


.. method:: xmlparser.Parse(data[, isfinal])

   Phân tích nội dung của *data*, gọi các hàm handler thích hợp để xử lý dữ liệu đã phân tích. *data* có thể là một :term:`bytes-like object` hoặc một chuỗi. Nếu là một chuỗi, khai báo encoding trong dữ liệu XML sẽ bị bỏ qua và dữ liệu được phân tích như văn bản đã được giải mã. *isfinal* phải là true trong lần gọi cuối cùng đến phương thức này; điều này cho phép phân tích một tệp duy nhất theo từng phần, chứ không phải gửi nhiều tệp. *data* có thể trống tại bất kỳ thời điểm nào.


.. method:: xmlparser.ParseFile(file)

   Phân tích dữ liệu XML bằng cách đọc từ đối tượng *file*. *file* chỉ cần cung cấp phương thức ``read(nbytes)``, phương thức này trả về bytes và một đối tượng bytes rỗng khi không còn dữ liệu. Không hỗ trợ tệp văn bản; hãy sử dụng :meth:`Parse` cho dữ liệu đã được giải mã.


.. method:: xmlparser.SetBase(base)

   Đặt base được dùng để phân giải các URI tương đối trong các định danh hệ thống ở các khai báo. Việc phân giải các định danh tương đối do ứng dụng thực hiện: giá trị này sẽ được truyền nguyên vẹn dưới dạng đối số *base* cho
   :func:`ExternalEntityRefHandler`, :func:`NotationDeclHandler`, và
   Các hàm :func:`UnparsedEntityDeclHandler`.


.. method:: xmlparser.GetBase()

   Trả về một chuỗi chứa base được thiết lập bởi lần gọi trước đó đến :meth:`SetBase`, hoặc ``None`` nếu :meth:`SetBase` chưa được gọi.


.. method:: xmlparser.GetInputContext()

   Trả về dữ liệu đầu vào đã tạo ra event hiện tại dưới dạng đối tượng :class:`bytes`. Dữ liệu sử dụng encoding của entity chứa văn bản. Dữ liệu kéo dài đến cuối phần input hiện đang được buffer, vì vậy nó cũng có thể chứa dữ liệu của các event tiếp theo; và nếu event được tạo ra bởi một lượng văn bản lớn thì có thể không phải toàn bộ dữ liệu đều khả dụng. Khi được gọi trong lúc không có event handler nào đang hoạt động, giá trị trả về là ``None``.


.. method:: xmlparser.ExternalEntityParserCreate(context[, encoding])

   Tạo một parser "con" có thể được dùng để phân tích một external parsed entity được tham chiếu bởi nội dung do parser cha phân tích. Tham số *context* phải là chuỗi được truyền cho hàm handler :meth:`ExternalEntityRefHandler`, được mô tả bên dưới. Parser con được tạo với
   :attr:`ordered_attributes` và :attr:`specified_attributes` được thiết lập thành các giá trị của parser này.

.. method:: xmlparser.SetParamEntityParsing(flag)

   Điều khiển việc phân tích các parameter entity (bao gồm external DTD subset). Các giá trị có thể có của *flag* là :const:`XML_PARAM_ENTITY_PARSING_NEVER`,
   :const:`XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE` và
   :const:`XML_PARAM_ENTITY_PARSING_ALWAYS`.  Trả về true nếu việc thiết lập cờ thành công.

.. method:: xmlparser.UseForeignDTD([flag])

   Việc gọi phương thức này với giá trị true cho *flag* (mặc định) sẽ khiến Expat gọi :attr:`ExternalEntityRefHandler` với :const:`None` cho mọi đối số, cho phép tải một DTD thay thế.  Nếu tài liệu không chứa khai báo kiểu tài liệu, :attr:`ExternalEntityRefHandler` vẫn sẽ được gọi, nhưng :attr:`StartDoctypeDeclHandler` và
   :attr:`EndDoctypeDeclHandler` sẽ không được gọi.

   Việc truyền giá trị false cho *flag* sẽ hủy một lệnh gọi trước đó đã truyền giá trị true, nhưng nếu không thì không có tác dụng.

   Phương thức này chỉ có thể được gọi trước khi các phương thức :meth:`Parse` hoặc :meth:`ParseFile` được gọi; việc gọi phương thức này sau khi một trong hai phương thức đó đã được gọi sẽ khiến
   :exc:`ExpatError` được phát sinh với thuộc tính :attr:`code` được đặt thành ``errors.codes[errors.XML_ERROR_CANT_CHANGE_FEATURE_ONCE_PARSING]``.

.. method:: xmlparser.SetReparseDeferralEnabled(enabled)

   .. warning::

      Việc gọi ``SetReparseDeferralEnabled(False)`` có những hệ quả về bảo mật như được trình bày bên dưới; hãy đảm bảo hiểu rõ những hệ quả này trước khi sử dụng phương thức ``SetReparseDeferralEnabled``.

   Expat 2.6.0 đã giới thiệu một cơ chế bảo mật có tên là "reparse deferral" (trì hoãn phân tích cú pháp lại), theo đó thay vì gây ra tình trạng từ chối dịch vụ do thời gian chạy bậc hai khi phân tích cú pháp lại các token lớn, việc phân tích cú pháp lại các token chưa hoàn chỉnh giờ đây mặc định được trì hoãn cho đến khi nhận đủ lượng input cần thiết. Do sự trì hoãn này, các handler đã đăng ký có thể — tùy thuộc vào kích thước của các phần input được đẩy vào Expat — không còn được gọi ngay sau khi đẩy input mới vào parser. Khi cần phản hồi tức thì và muốn tự chịu trách nhiệm bảo vệ chống lại tình trạng từ chối dịch vụ do các token lớn, việc gọi ``SetReparseDeferralEnabled(False)`` sẽ tắt reparse deferral cho instance Expat parser hiện tại, tạm thời hoặc hoàn toàn. Việc gọi ``SetReparseDeferralEnabled(True)`` cho phép bật lại reparse deferral.

   Lưu ý rằng :meth:`SetReparseDeferralEnabled` đã được backport vào một số bản phát hành trước đây của CPython dưới dạng bản sửa lỗi bảo mật. Kiểm tra tính khả dụng của
   :meth:`SetReparseDeferralEnabled` bằng :func:`hasattr` nếu được sử dụng trong mã chạy trên nhiều phiên bản Python khác nhau.

   .. versionadded:: 3.13

.. method:: xmlparser.GetReparseDeferralEnabled()

   Trả về cho biết reparse deferral hiện có được bật cho instance Expat parser đã cho hay không.

   .. versionadded:: 3.13


Các đối tượng :class:`!xmlparser` có các phương thức sau để điều chỉnh các cơ chế bảo vệ chống lại một số lỗ hổng XML phổ biến.

.. method:: xmlparser.SetBillionLaughsAttackProtectionActivationThreshold(threshold, /)

   Đặt số byte output cần thiết để kích hoạt cơ chế bảo vệ chống lại các cuộc tấn công `billion laughs <billion laughs_>`_.

   Số byte output bao gồm cả phần khuếch đại từ việc mở rộng entity và đọc các tệp DTD.

   Các đối tượng Parser thường có ngưỡng kích hoạt cơ chế bảo vệ là 8 MiB, nhưng giá trị mặc định thực tế phụ thuộc vào thư viện Expat bên dưới.

   Một :exc:`ExpatError` sẽ được phát sinh nếu phương thức này được gọi trên một parser |xml-non-root-parser|. Không nên sử dụng :attr:`~ExpatError.lineno` và :attr:`~ExpatError.offset` tương ứng vì chúng có thể không có ý nghĩa đặc biệt.

   .. note::

      Các ngưỡng kích hoạt thấp hơn 4 MiB được biết là làm hỏng khả năng hỗ trợ payload DITA 1.3 và do đó không được khuyến nghị.

   .. versionadded:: 3.14.6

.. method:: xmlparser.SetBillionLaughsAttackProtectionMaximumAmplification(max_factor, /)

   Đặt hệ số khuếch đại tối đa được chấp nhận để bảo vệ khỏi các cuộc tấn công `billion laughs <billion laughs_>`_.

   Hệ số khuếch đại được tính là ``(direct + indirect) / direct`` trong khi phân tích cú pháp, trong đó ``direct`` là số byte được đọc từ tài liệu chính khi phân tích cú pháp và ``indirect`` là số byte được thêm vào do mở rộng các thực thể và đọc các tệp DTD bên ngoài.

   Giá trị *max_factor* phải là giá trị :class:`float` không phải NaN và lớn hơn hoặc bằng 1.0. Trong thực tế, đã quan sát thấy mức khuếch đại cực đại là 15.000 lần đối với toàn bộ payload và 30.000 lần ở giữa quá trình phân tích cú pháp với các tệp nhỏ, không độc hại. Đặc biệt, cần lựa chọn ngưỡng kích hoạt cẩn thận để tránh các kết quả dương tính giả.

   Các đối tượng Parser thường có hệ số khuếch đại tối đa là 100, nhưng giá trị mặc định thực tế phụ thuộc vào thư viện Expat bên dưới.

   Một :exc:`ExpatError` được phát sinh nếu phương thức này được gọi trên trình phân tích cú pháp |xml-non-root-parser| hoặc nếu *max_factor* nằm ngoài phạm vi hợp lệ. Không nên sử dụng :attr:`~ExpatError.lineno` và :attr:`~ExpatError.offset` tương ứng vì chúng có thể không có ý nghĩa đặc biệt.

   .. note::

      Hệ số khuếch đại tối đa chỉ được xét khi vượt quá ngưỡng có thể điều chỉnh bằng :meth:`.SetBillionLaughsAttackProtectionActivationThreshold`.

   .. versionadded:: 3.14.6

.. method:: xmlparser.SetAllocTrackerActivationThreshold(threshold, /)

   Đặt số byte bộ nhớ động được cấp phát cần thiết để kích hoạt cơ chế bảo vệ chống sử dụng RAM không cân đối.

   Các đối tượng parser thường có ngưỡng kích hoạt cấp phát là 64 MiB, nhưng giá trị mặc định thực tế phụ thuộc vào thư viện Expat nền tảng.

   Một :exc:`ExpatError` sẽ được phát sinh nếu phương thức này được gọi trên một parser |xml-non-root-parser|. Không nên sử dụng :attr:`~ExpatError.lineno` và :attr:`~ExpatError.offset` tương ứng vì chúng có thể không có ý nghĩa đặc biệt.

   .. versionadded:: 3.14.1

.. method:: xmlparser.SetAllocTrackerMaximumAmplification(max_factor, /)

   Đặt hệ số khuếch đại tối đa giữa dữ liệu đầu vào trực tiếp và số byte bộ nhớ động được cấp phát.

   Hệ số khuếch đại được tính là ``allocated / direct`` trong khi phân tích cú pháp, trong đó ``direct`` là số byte được đọc từ tài liệu chính trong quá trình phân tích cú pháp và ``allocated`` là số byte bộ nhớ động được cấp phát trong hệ thống phân cấp parser.

   Giá trị *max_factor* phải là một giá trị :class:`float` không phải NaN và lớn hơn hoặc bằng 1.0. Trong thực tế, các hệ số khuếch đại lớn hơn 100.0 có thể được quan sát thấy gần thời điểm bắt đầu phân tích cú pháp, ngay cả với các tệp không chứa nội dung bất thường. Đặc biệt, cần lựa chọn ngưỡng kích hoạt cẩn thận để tránh các kết quả dương tính giả.

   Các đối tượng Parser thường có hệ số khuếch đại tối đa là 100, nhưng giá trị mặc định thực tế phụ thuộc vào thư viện Expat bên dưới.

   Một :exc:`ExpatError` được phát sinh nếu phương thức này được gọi trên trình phân tích cú pháp |xml-non-root-parser| hoặc nếu *max_factor* nằm ngoài phạm vi hợp lệ. Không nên sử dụng :attr:`~ExpatError.lineno` và :attr:`~ExpatError.offset` tương ứng vì chúng có thể không có ý nghĩa đặc biệt.

   .. note::

      Hệ số khuếch đại tối đa chỉ được xét đến nếu vượt quá ngưỡng có thể điều chỉnh bằng :meth:`.SetAllocTrackerActivationThreshold`.

   .. versionadded:: 3.14.1


Các đối tượng :class:`xmlparser` có các thuộc tính sau:


.. attribute:: xmlparser.buffer_size

   Kích thước của bộ đệm được sử dụng khi :attr:`buffer_text` là true. Có thể đặt kích thước bộ đệm mới bằng cách gán một giá trị số nguyên mới cho thuộc tính này. Khi kích thước thay đổi, bộ đệm sẽ được xóa.


.. attribute:: xmlparser.buffer_text

   Đặt giá trị này thành true khiến đối tượng :class:`xmlparser` lưu nội dung văn bản do Expat trả về vào bộ đệm để tránh phải gọi nhiều lần đến
   :meth:`CharacterDataHandler` callback bất cứ khi nào có thể. Điều này có thể cải thiện đáng kể hiệu năng vì Expat thường chia dữ liệu ký tự thành các khối tại mỗi dòng mới. Thuộc tính này mặc định là false và có thể được thay đổi bất cứ lúc nào. Lưu ý rằng khi thuộc tính này là false, dữ liệu không chứa dòng mới cũng có thể bị chia thành các khối.


.. attribute:: xmlparser.buffer_used

   Nếu :attr:`buffer_text` được bật, số byte được lưu trong buffer. Các byte này biểu diễn văn bản được mã hóa UTF-8. Thuộc tính này không có ý nghĩa diễn giải đáng kể khi :attr:`buffer_text` là false.


.. attribute:: xmlparser.ordered_attributes

   Đặt thuộc tính này thành một số nguyên khác không sẽ khiến các thuộc tính được báo cáo dưới dạng danh sách thay vì từ điển. Các thuộc tính được trình bày theo thứ tự xuất hiện trong văn bản tài liệu. Với mỗi thuộc tính, hai mục trong danh sách được trình bày: tên thuộc tính và giá trị thuộc tính. (Các phiên bản cũ hơn của module này cũng sử dụng định dạng này.) Theo mặc định, thuộc tính này là false; có thể thay đổi thuộc tính này bất cứ lúc nào.


.. attribute:: xmlparser.specified_attributes

   Nếu được đặt thành một số nguyên khác không, parser sẽ chỉ báo cáo những thuộc tính được chỉ định trong thể hiện tài liệu, không báo cáo những thuộc tính được suy ra từ các khai báo thuộc tính. Các ứng dụng đặt thuộc tính này cần đặc biệt cẩn thận sử dụng thông tin bổ sung có sẵn từ các khai báo khi cần để tuân thủ các tiêu chuẩn về hành vi của bộ xử lý XML. Theo mặc định, thuộc tính này là false; có thể thay đổi thuộc tính này bất cứ lúc nào.


.. attribute:: xmlparser.intern

   Từ điển được dùng để intern tên của các phần tử và thuộc tính. Đây là từ điển được truyền dưới dạng đối số *intern* của :func:`ParserCreate`, hoặc là một từ điển mới được tạo cho parser này.


.. attribute:: xmlparser.namespace_prefixes

   Nếu được đặt thành giá trị true và việc xử lý namespace được bật, tiền tố namespace sẽ được báo cáo là phần thứ ba của tên mở rộng, được phân tách bằng dấu phân cách namespace. Các tên không có tiền tố không bị ảnh hưởng. Theo mặc định, thuộc tính này là false; có thể thay đổi thuộc tính này bất cứ lúc nào.


Các thuộc tính sau chứa các giá trị liên quan đến lỗi gần đây nhất gặp phải bởi một đối tượng :class:`xmlparser`, và sẽ chỉ có giá trị chính xác sau khi một lệnh gọi đến :meth:`Parse` hoặc :meth:`ParseFile` đã phát sinh một
Ngoại lệ :exc:`xml.parsers.expat.ExpatError`.


.. attribute:: xmlparser.ErrorByteIndex

   Chỉ số byte tại vị trí xảy ra lỗi.


.. attribute:: xmlparser.ErrorCode

   Mã số chỉ định vấn đề. Giá trị này có thể được truyền cho
   hàm :func:`ErrorString`, hoặc được so sánh với một trong các hằng số được định nghĩa trong đối tượng ``errors``.


.. attribute:: xmlparser.ErrorColumnNumber

   Số cột tại vị trí xảy ra lỗi.


.. attribute:: xmlparser.ErrorLineNumber

   Số dòng tại vị trí xảy ra lỗi.

Các thuộc tính sau chứa các giá trị liên quan đến vị trí phân tích hiện tại trong một đối tượng :class:`xmlparser`. Trong một callback báo cáo sự kiện phân tích, chúng cho biết vị trí của ký tự đầu tiên trong chuỗi ký tự đã tạo ra sự kiện. Khi được gọi bên ngoài một callback, vị trí được chỉ báo sẽ ngay sau sự kiện phân tích cuối cùng (bất kể có callback tương ứng hay không).


.. attribute:: xmlparser.CurrentByteIndex

   Chỉ mục byte hiện tại trong dữ liệu đầu vào của parser.


.. attribute:: xmlparser.CurrentColumnNumber

   Số cột hiện tại trong dữ liệu đầu vào của parser.


.. attribute:: xmlparser.CurrentLineNumber

   Số dòng hiện tại trong dữ liệu đầu vào của parser.

Sau đây là danh sách các handler có thể được thiết lập.  Để thiết lập một handler trên một
:class:`xmlparser` object *o*, hãy sử dụng ``o.handlername = func``.  *handlername* phải được lấy từ danh sách sau, và *func* phải là một callable object nhận đúng số lượng đối số.  Tất cả các đối số đều là chuỗi, trừ khi có quy định khác.


.. method:: xmlparser.XmlDeclHandler(version, encoding, standalone)

   Được gọi khi khai báo XML được phân tích cú pháp.  Khai báo XML là khai báo (tùy chọn) về phiên bản áp dụng của khuyến nghị XML, encoding của văn bản tài liệu và một khai báo "standalone" tùy chọn. *version* và *encoding* sẽ là các chuỗi, còn *standalone* sẽ là ``1`` nếu tài liệu được khai báo là standalone, ``0`` nếu tài liệu được khai báo không phải standalone hoặc ``-1`` nếu mệnh đề standalone bị lược bỏ.


.. method:: xmlparser.StartDoctypeDeclHandler(doctypeName, systemId, publicId, has_internal_subset)

   Được gọi khi Expat bắt đầu phân tích cú pháp khai báo kiểu tài liệu (``<!DOCTYPE ...``).  *doctypeName* được cung cấp chính xác như đã trình bày.  Các tham số *systemId* và *publicId* cung cấp các mã định danh hệ thống và công khai nếu được chỉ định, hoặc ``None`` nếu bị lược bỏ.  *has_internal_subset* sẽ là true nếu tài liệu chứa một tập con khai báo tài liệu nội bộ.


.. method:: xmlparser.EndDoctypeDeclHandler()

   Được gọi khi Expat hoàn tất việc phân tích khai báo kiểu tài liệu.


.. method:: xmlparser.ElementDeclHandler(name, model)

   Được gọi một lần cho mỗi khai báo kiểu phần tử. *name* là tên của kiểu phần tử, còn *model* là biểu diễn của mô hình nội dung.


.. method:: xmlparser.AttlistDeclHandler(elname, attname, type, default, required)

   Được gọi cho mỗi thuộc tính được khai báo của một kiểu phần tử. Nếu một khai báo danh sách thuộc tính khai báo ba thuộc tính, trình xử lý này được gọi ba lần, mỗi lần cho một thuộc tính. *elname* là tên của phần tử áp dụng khai báo, còn *attname* là tên của thuộc tính được khai báo. Kiểu thuộc tính là một chuỗi được truyền dưới dạng *type*: ``'CDATA'``, ``'ID'``, ``'IDREF'``, ``'IDREFS'``, ``'ENTITY'``, ``'ENTITIES'``, ``'NMTOKEN'`` hoặc ``'NMTOKENS'``, một enumeration như ``'(x|y)'``, hoặc một danh sách notation như ``'NOTATION(n1|n2)'``. *default* cung cấp giá trị mặc định cho thuộc tính được sử dụng khi thuộc tính không được chỉ định trong instance tài liệu, hoặc ``None`` nếu không có giá trị mặc định (``#IMPLIED`` values). Nếu thuộc tính bắt buộc phải được cung cấp trong instance tài liệu, *required* sẽ là true.


.. method:: xmlparser.StartElementHandler(name, attributes)

   Được gọi khi bắt đầu mỗi phần tử. *name* là một chuỗi chứa tên phần tử, còn *attributes* là các thuộc tính của phần tử. Nếu
   :attr:`ordered_attributes` là true, đây là một danh sách (xem
   :attr:`ordered_attributes` để biết mô tả đầy đủ). Nếu không, đây là một dictionary ánh xạ tên với giá trị.


.. method:: xmlparser.EndElementHandler(name)

   Được gọi khi kết thúc mỗi phần tử.


.. method:: xmlparser.ProcessingInstructionHandler(target, data)

   Được gọi cho mọi chỉ thị xử lý.


.. method:: xmlparser.CharacterDataHandler(data)

   Được gọi cho dữ liệu ký tự. Phương thức này được gọi cho dữ liệu ký tự thông thường, nội dung được đánh dấu CDATA và khoảng trắng có thể bỏ qua. Các ứng dụng cần phân biệt những trường hợp này có thể sử dụng các callback :attr:`StartCdataSectionHandler`,
   :attr:`EndCdataSectionHandler`, và :attr:`ElementDeclHandler` để thu thập thông tin cần thiết. Lưu ý rằng dữ liệu ký tự có thể được chia thành nhiều phần ngay cả khi dữ liệu ngắn, vì vậy bạn có thể nhận được nhiều hơn một lần gọi đến
   :meth:`CharacterDataHandler`. Đặt thuộc tính instance :attr:`buffer_text` thành ``True`` để tránh điều đó.


.. method:: xmlparser.UnparsedEntityDeclHandler(entityName, base, systemId, publicId, notationName)

   Được gọi cho các khai báo entity chưa phân tích (NDATA). Nếu handler này chưa được thiết lập, các khai báo như vậy sẽ được báo cáo bởi
   :attr:`EntityDeclHandler`, vốn được ưu tiên sử dụng trong code mới. (Hàm bên dưới trong thư viện Expat đã được tuyên bố là lỗi thời.)


.. method:: xmlparser.EntityDeclHandler(entityName, is_parameter_entity, value, base, systemId, publicId, notationName)

   Được gọi cho mọi khai báo entity. Đối với entity tham số và entity nội bộ, *value* sẽ là một chuỗi chứa nội dung đã khai báo của entity; đối với entity bên ngoài, giá trị này sẽ là ``None``. Tham số *notationName* sẽ là ``None`` đối với các entity đã phân tích và là tên của notation đối với các entity chưa phân tích. *is_parameter_entity* sẽ là true nếu entity là entity tham số hoặc false đối với general entity (hầu hết ứng dụng chỉ cần quan tâm đến general entity).


.. method:: xmlparser.NotationDeclHandler(notationName, base, systemId, publicId)

   Được gọi cho các khai báo notation.  *notationName*, *base*, *systemId* và *publicId* là các chuỗi nếu được cung cấp.  Nếu bỏ qua định danh public, *publicId* sẽ là ``None``.


.. method:: xmlparser.StartNamespaceDeclHandler(prefix, uri)

   Được gọi khi một element chứa khai báo namespace.  Các khai báo namespace được xử lý trước khi gọi :attr:`StartElementHandler` cho element nơi các khai báo được đặt.


.. method:: xmlparser.EndNamespaceDeclHandler(prefix)

   Được gọi khi đến thẻ đóng của một element chứa khai báo namespace.  Hàm này được gọi một lần cho mỗi khai báo namespace trên element, theo thứ tự ngược lại với thứ tự mà
   :attr:`StartNamespaceDeclHandler` được gọi để biểu thị phần bắt đầu phạm vi của từng khai báo namespace.  Các lần gọi handler này được thực hiện sau :attr:`EndElementHandler` tương ứng cho phần kết thúc của element.


.. method:: xmlparser.CommentHandler(data)

   Được gọi cho các comment.  *data* là nội dung của comment, không bao gồm ``'<!-``\ ``-'`` ở đầu và ``'-``\ ``->'`` ở cuối.


.. method:: xmlparser.StartCdataSectionHandler()

   Được gọi khi bắt đầu một phần CDATA.  Cần có phần này và :attr:`EndCdataSectionHandler` để có thể xác định điểm bắt đầu và kết thúc cú pháp của các phần CDATA.


.. method:: xmlparser.EndCdataSectionHandler()

   Được gọi khi kết thúc một phần CDATA.


.. method:: xmlparser.DefaultHandler(data)

   Được gọi cho mọi ký tự trong tài liệu XML mà chưa có trình xử lý phù hợp nào được chỉ định. Điều này có nghĩa là các ký tự thuộc một cấu trúc có thể được báo cáo, nhưng chưa có trình xử lý nào được cung cấp.


.. method:: xmlparser.DefaultHandlerExpand(data)

   Điều này giống với :attr:`DefaultHandler`, nhưng không ngăn việc mở rộng các thực thể nội bộ. Tham chiếu thực thể sẽ không được truyền cho trình xử lý mặc định.


.. method:: xmlparser.NotStandaloneHandler()

   Được gọi nếu tài liệu XML chưa được khai báo là một tài liệu độc lập. Điều này xảy ra khi có tập con bên ngoài hoặc tham chiếu đến một thực thể tham số, nhưng khai báo XML không đặt standalone thành ``yes`` trong khai báo XML. Nếu trình xử lý này trả về ``0``, trình phân tích cú pháp sẽ phát sinh một
   lỗi :const:`XML_ERROR_NOT_STANDALONE`. Nếu trình xử lý này không được thiết lập, trình phân tích cú pháp sẽ không phát sinh ngoại lệ nào do điều kiện này.


.. method:: xmlparser.ExternalEntityRefHandler(context, base, systemId, publicId)

   .. warning::

      Việc triển khai một trình xử lý truy cập các tệp cục bộ và/hoặc mạng có thể tạo ra lỗ hổng đối với các `cuộc tấn công thực thể bên ngoài <https://en.wikipedia.org/wiki/XML_external_entity_attack>`_ nếu sử dụng :class:`xmlparser` với nội dung XML do người dùng cung cấp. Hãy xem xét `mô hình mối đe dọa <https://en.wikipedia.org/wiki/Threat_model>`_ của bạn trước khi triển khai trình xử lý này.

   Được gọi cho các tham chiếu đến thực thể bên ngoài. *base* là base hiện tại, được thiết lập bởi một lần gọi trước đó đến :meth:`SetBase`. Các mã định danh public và system, *systemId* và *publicId*, là các chuỗi nếu được cung cấp; nếu không cung cấp mã định danh public, *publicId* sẽ là ``None``. Giá trị *context* là giá trị không trong suốt và chỉ nên được sử dụng như mô tả bên dưới.

   Để phân tích cú pháp các thực thể bên ngoài, trình xử lý này phải được triển khai. Trình xử lý này chịu trách nhiệm tạo trình phân tích cú pháp con bằng ``ExternalEntityParserCreate(context)``, khởi tạo nó với các callback thích hợp và phân tích cú pháp thực thể. Trình xử lý này phải trả về một số nguyên; nếu trả về ``0``, trình phân tích cú pháp sẽ phát sinh một
   :const:`XML_ERROR_EXTERNAL_ENTITY_HANDLING` lỗi; nếu không, quá trình phân tích cú pháp sẽ tiếp tục.

   Nếu handler này không được cung cấp, các external entity sẽ được báo cáo bởi
   :attr:`DefaultHandler` callback, nếu được cung cấp.


.. method:: xmlparser.SkippedEntityHandler(entityName, is_parameter_entity)

   Được gọi cho các tham chiếu entity không được mở rộng vì parser chưa đọc khai báo của entity. Điều này xảy ra khi external DTD subset hoặc external parameter entity không được phân tích cú pháp. *is_parameter_entity* có giá trị true đối với parameter entity và false đối với general entity.


.. _expaterror-objects:

Ngoại lệ ExpatError
-------------------

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>


:exc:`ExpatError` các ngoại lệ có một số thuộc tính đáng chú ý:


.. attribute:: ExpatError.code

   Số hiệu lỗi nội bộ của Expat đối với lỗi cụ thể.  Giá trị này
   :data:`errors.messages <xml.parsers.expat.errors.messages>` ánh xạ các số lỗi này tới thông báo lỗi của Expat. Ví dụ::

      from xml.parsers.expat import ParserCreate, ExpatError, errors

      p = ParserCreate()
      try:
          p.Parse(some_xml_document)
      except ExpatError as err:
          print("Error:", errors.messages[err.code])

   Mô-đun :mod:`~xml.parsers.expat.errors` cũng cung cấp các hằng số thông báo lỗi và một từ điển :data:`~xml.parsers.expat.errors.codes` ánh xạ các thông báo này ngược lại về mã lỗi, như bên dưới.


.. attribute:: ExpatError.lineno

   Số dòng nơi phát hiện lỗi. Dòng đầu tiên được đánh số ``1``.


.. attribute:: ExpatError.offset

   Vị trí ký tự trong dòng nơi xảy ra lỗi. Cột đầu tiên được đánh số ``0``.


.. _expat-example:

Ví dụ
-----

Chương trình sau đây định nghĩa ba handler chỉ in ra các đối số của chúng.::

   import xml.parsers.expat

   # 3 hàm handler
   def start_element(name, attrs):
       print('Start element:', name, attrs)
   def end_element(name):
       print('End element:', name)
   def char_data(data):
       print('Character data:', repr(data))

   p = xml.parsers.expat.ParserCreate()

   p.StartElementHandler = start_element
   p.EndElementHandler = end_element
   p.CharacterDataHandler = char_data

   p.Parse("""<?xml version="1.0"?>
   <parent id="top"><child1 name="paul">Text goes here</child1>
   <child2 name="fred">More text</child2>
   </parent>""", 1)

Đầu ra của chương trình này là::

   Start element: parent {'id': 'top'}
   Start element: child1 {'name': 'paul'}
   Character data: 'Text goes here'
   End element: child1
   Character data: '\n'
   Start element: child2 {'name': 'fred'}
   Character data: 'More text'
   End element: child2
   Character data: '\n'
   End element: parent


.. _expat-content-models:

Mô tả mô hình nội dung
----------------------

.. module:: xml.parsers.expat.model

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

Các mô hình nội dung được mô tả bằng các tuple lồng nhau. Mỗi tuple chứa bốn giá trị: kiểu, bộ lượng từ, tên và một tuple gồm các phần tử con. Các phần tử con chỉ đơn giản là những mô tả mô hình nội dung bổ sung.

Giá trị của hai trường đầu tiên là các hằng số được định nghĩa trong
:mod:`!xml.parsers.expat.model` module. Các hằng số này có thể được tập hợp thành hai nhóm: nhóm kiểu mô hình và nhóm bộ lượng từ.

Các hằng số trong nhóm kiểu mô hình là:


.. data:: XML_CTYPE_ANY

   Phần tử có tên được chỉ định bởi tên mô hình được khai báo là có mô hình nội dung ``ANY``.


.. data:: XML_CTYPE_CHOICE

   Phần tử được nêu tên cho phép chọn một trong nhiều tùy chọn; kiểu này được dùng cho các content model như ``(A | B | C)``.


.. data:: XML_CTYPE_EMPTY

   Các phần tử được khai báo là ``EMPTY`` có kiểu content model này.


.. data:: XML_CTYPE_MIXED

   Phần tử được nêu tên cho phép dữ liệu ký tự, có thể xen kẽ với các phần tử con được nêu tên; kiểu này được dùng cho các content model như ``(#PCDATA)`` và ``(#PCDATA | A | B)*``.


.. data:: XML_CTYPE_NAME

   Content model này chỉ định một phần tử duy nhất, như trong ``A``.


.. data:: XML_CTYPE_SEQ

   Các content model biểu thị một chuỗi các content model nối tiếp nhau được chỉ báo bằng kiểu content model này. Kiểu này được dùng cho các content model như ``(A, B, C)``.

Các hằng số trong nhóm quantifier là:


.. data:: XML_CQUANT_NONE

   Không có modifier nào được chỉ định, vì vậy nó có thể xuất hiện chính xác một lần, như trong ``A``.


.. data:: XML_CQUANT_OPT

   Mô hình là tùy chọn: nó có thể xuất hiện một lần hoặc không xuất hiện, như trong ``A?``.


.. data:: XML_CQUANT_PLUS

   Mô hình phải xuất hiện một hoặc nhiều lần (như ``A+``).


.. data:: XML_CQUANT_REP

   Mô hình phải xuất hiện từ không đến nhiều lần, như trong ``A*``.


.. _expat-errors:

Các hằng số lỗi của Expat
-------------------------

.. module:: xml.parsers.expat.errors

Mô-đun :mod:`!xml.parsers.expat.errors` cung cấp các hằng số sau. Các hằng số này hữu ích khi diễn giải một số thuộc tính của các đối tượng ngoại lệ :exc:`ExpatError` được phát sinh khi xảy ra lỗi. Vì lý do tương thích ngược, giá trị của các hằng số là *message* lỗi chứ không phải *code* lỗi dạng số, nên bạn thực hiện việc này bằng cách so sánh thuộc tính của nó với
thuộc tính :attr:`code` của nó với
:samp:`errors.codes[errors.XML_ERROR_{CONSTANT_NAME}]`.

Mô-đun ``errors`` có các thuộc tính sau:

.. data:: codes

   Một dictionary ánh xạ các mô tả lỗi dạng chuỗi tới mã lỗi tương ứng.

   .. versionadded:: 3.2


.. data:: messages

   Một dictionary ánh xạ các mã lỗi dạng số tới mô tả lỗi dạng chuỗi tương ứng.

   .. versionadded:: 3.2


.. data:: XML_ERROR_ASYNC_ENTITY


.. data:: XML_ERROR_ATTRIBUTE_EXTERNAL_ENTITY_REF

   Một tham chiếu thực thể trong giá trị thuộc tính tham chiếu tới một thực thể bên ngoài thay vì một thực thể nội bộ.


.. data:: XML_ERROR_BAD_CHAR_REF

   Một tham chiếu ký tự tham chiếu tới một ký tự không hợp lệ trong XML (ví dụ: ký tự ``0``, hoặc '``&#0;``').


.. data:: XML_ERROR_BINARY_ENTITY_REF

   Một tham chiếu thực thể tham chiếu tới một thực thể được khai báo bằng một notation, nên không thể được phân tích cú pháp.


.. data:: XML_ERROR_DUPLICATE_ATTRIBUTE

   Một thuộc tính được sử dụng nhiều hơn một lần trong thẻ bắt đầu.


.. data:: XML_ERROR_INCORRECT_ENCODING


.. data:: XML_ERROR_INVALID_TOKEN

   Được phát sinh khi một byte đầu vào không thể được gán chính xác cho một ký tự; ví dụ: một byte NUL (giá trị ``0``) trong luồng đầu vào UTF-8.


.. data:: XML_ERROR_JUNK_AFTER_DOC_ELEMENT

   Có nội dung khác ngoài khoảng trắng xuất hiện sau phần tử tài liệu.


.. data:: XML_ERROR_MISPLACED_XML_PI

   Một khai báo XML được tìm thấy ở vị trí khác với phần đầu của dữ liệu đầu vào.


.. data:: XML_ERROR_NO_ELEMENTS

   Tài liệu không chứa phần tử nào (XML yêu cầu mọi tài liệu phải chứa chính xác một phần tử cấp cao nhất).


.. data:: XML_ERROR_NO_MEMORY

   Expat không thể cấp phát bộ nhớ nội bộ.


.. data:: XML_ERROR_PARAM_ENTITY_REF

   Một tham chiếu thực thể tham số được tìm thấy ở nơi không được phép.


.. data:: XML_ERROR_PARTIAL_CHAR

   Một ký tự chưa hoàn chỉnh được tìm thấy trong dữ liệu đầu vào.


.. data:: XML_ERROR_RECURSIVE_ENTITY_REF

   Một tham chiếu thực thể chứa một tham chiếu khác đến chính thực thể đó; có thể thông qua một tên khác và cũng có thể là gián tiếp.


.. data:: XML_ERROR_SYNTAX

   Đã gặp một lỗi cú pháp không xác định.


.. data:: XML_ERROR_TAG_MISMATCH

   Thẻ kết thúc không khớp với thẻ bắt đầu đang mở ở trong cùng.


.. data:: XML_ERROR_UNCLOSED_TOKEN

   Một token nào đó (chẳng hạn như thẻ bắt đầu) chưa được đóng trước khi luồng kết thúc hoặc token tiếp theo xuất hiện.


.. data:: XML_ERROR_UNDEFINED_ENTITY

   Đã tham chiếu đến một entity chưa được định nghĩa.


.. data:: XML_ERROR_UNKNOWN_ENCODING

   Expat không hỗ trợ encoding của tài liệu.


.. data:: XML_ERROR_UNCLOSED_CDATA_SECTION

   Một phần được đánh dấu CDATA chưa được đóng.


.. data:: XML_ERROR_EXTERNAL_ENTITY_HANDLING


.. data:: XML_ERROR_NOT_STANDALONE

   Bộ phân tích cú pháp xác định rằng tài liệu không phải là "standalone" mặc dù tài liệu tự khai báo là như vậy trong khai báo XML, và :attr:`NotStandaloneHandler` được đặt thành và trả về ``0``.


.. data:: XML_ERROR_UNEXPECTED_STATE


.. data:: XML_ERROR_ENTITY_DECLARED_IN_PE


.. data:: XML_ERROR_FEATURE_REQUIRES_XML_DTD

   Đã yêu cầu một thao tác cần được biên dịch kèm hỗ trợ DTD, nhưng Expat được cấu hình mà không có hỗ trợ DTD. Điều này không bao giờ được báo cáo bởi bản build tiêu chuẩn của mô-đun :mod:`!xml.parsers.expat`.


.. data:: XML_ERROR_CANT_CHANGE_FEATURE_ONCE_PARSING

   Đã yêu cầu thay đổi hành vi sau khi quá trình phân tích cú pháp bắt đầu, nhưng thay đổi này chỉ có thể được thực hiện trước khi quá trình phân tích cú pháp bắt đầu. Hiện tại, lỗi này chỉ được phát sinh bởi
   :meth:`UseForeignDTD`.


.. data:: XML_ERROR_UNBOUND_PREFIX

   Đã tìm thấy một prefix chưa được khai báo khi tính năng xử lý namespace được bật.


.. data:: XML_ERROR_UNDECLARING_PREFIX

   Tài liệu đã cố gắng xóa khai báo namespace liên kết với một prefix.


.. data:: XML_ERROR_INCOMPLETE_PE

   Một parameter entity chứa markup chưa hoàn chỉnh.


.. data:: XML_ERROR_XML_DECL

   Đã xảy ra lỗi khi phân tích cú pháp khai báo XML.


.. data:: XML_ERROR_TEXT_DECL

   Đã xảy ra lỗi khi phân tích cú pháp khai báo văn bản trong một entity bên ngoài.


.. data:: XML_ERROR_PUBLICID

   Đã tìm thấy các ký tự không được phép trong public id.


.. data:: XML_ERROR_SUSPENDED

   Đã thực hiện thao tác được yêu cầu trên một parser đang bị tạm dừng, nhưng thao tác này không được phép. Điều này bao gồm cả việc cố cung cấp thêm dữ liệu đầu vào hoặc dừng parser.


.. data:: XML_ERROR_NOT_SUSPENDED

   Đã cố tiếp tục parser trong khi parser chưa bị tạm dừng.


.. data:: XML_ERROR_ABORTED

   Điều này không nên được báo cáo cho các ứng dụng Python.


.. data:: XML_ERROR_FINISHED

   Đã thực hiện thao tác được yêu cầu trên một parser đã hoàn tất việc phân tích dữ liệu đầu vào, nhưng thao tác này không được phép. Điều này bao gồm cả việc cố cung cấp thêm dữ liệu đầu vào hoặc dừng parser.


.. data:: XML_ERROR_SUSPEND_PE


.. data:: XML_ERROR_RESERVED_PREFIX_XML

   Đã cố hủy khai báo tiền tố namespace dành riêng ``xml`` hoặc liên kết tiền tố này với một URI namespace khác.


.. data:: XML_ERROR_RESERVED_PREFIX_XMLNS

   Đã cố khai báo hoặc hủy khai báo tiền tố namespace dành riêng ``xmlns``.


.. data:: XML_ERROR_RESERVED_NAMESPACE_URI

   Đã có nỗ lực liên kết URI của một trong các tiền tố namespace dành riêng ``xml`` và ``xmlns`` với một tiền tố namespace khác.


.. data:: XML_ERROR_INVALID_ARGUMENT

   Điều này không nên được báo cáo cho các ứng dụng Python.


.. data:: XML_ERROR_NO_BUFFER

   Điều này không nên được báo cáo cho các ứng dụng Python.


.. data:: XML_ERROR_AMPLIFICATION_LIMIT_BREACH

   Đã vượt quá giới hạn về hệ số khuếch đại đầu vào (từ DTD và các entity).


.. data:: XML_ERROR_NOT_STARTED

   Đã cố gắng dừng hoặc tạm ngưng parser trước khi parser bắt đầu.

   .. versionadded:: 3.14


.. rubric:: Chú thích cuối trang

.. [1] Chuỗi encoding có trong đầu ra XML phải tuân thủ các tiêu chuẩn thích hợp. Ví dụ: "UTF-8" là hợp lệ, nhưng "UTF8" thì không. Xem https://www.w3.org/TR/2006/REC-xml11-20060816/#NT-EncodingDecl và https://www.iana.org/assignments/character-sets/character-sets.xhtml.


.. _billion laughs: https://en.wikipedia.org/wiki/Billion_laughs_attack
.. |xml-non-root-parser| replace:: :ref:`không phải root <xmlparser-non-root>`

.. _`The Expat XML Parser`: http://www.libexpat.org/
.. _`external entity attacks`: https://en.wikipedia.org/wiki/XML_external_entity_attack
.. _`threat model`: https://en.wikipedia.org/wiki/Threat_model
