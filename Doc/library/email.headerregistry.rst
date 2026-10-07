:mod:`!email.headerregistry`: Các đối tượng Header tùy chỉnh
------------------------------------------------------------

.. module:: email.headerregistry
   :synopsis: Tự động phân tích cú pháp các header dựa trên tên trường

.. moduleauthor:: R. David Murray <rdmurray@bitdance.com>
.. sectionauthor:: R. David Murray <rdmurray@bitdance.com>

**Mã nguồn:** :source:`Lib/email/headerregistry.py`

--------------

.. versionadded:: 3.6 [1]_

Các header được biểu diễn bằng các lớp con tùy chỉnh của :class:`str`. Lớp cụ thể được dùng để biểu diễn một header nhất định được xác định bởi
:attr:`~email.policy.EmailPolicy.header_factory` của :mod:`~email.policy` đang có hiệu lực tại thời điểm các header được tạo. Phần này mô tả ``header_factory`` cụ thể được gói email triển khai để xử lý các thông điệp email tuân thủ :RFC:`5322`, không chỉ cung cấp các đối tượng header tùy chỉnh cho nhiều loại header khác nhau mà còn cung cấp cơ chế mở rộng để các ứng dụng thêm các loại header tùy chỉnh của riêng mình.

Khi sử dụng bất kỳ đối tượng policy nào được dẫn xuất từ
:data:`~email.policy.EmailPolicy`, tất cả header đều được tạo bởi
:class:`.HeaderRegistry` và có :class:`.BaseHeader` làm lớp cơ sở cuối cùng. Mỗi lớp header có thêm một lớp cơ sở được xác định bởi loại của header. Ví dụ, nhiều header có lớp
:class:`.UnstructuredHeader` làm lớp cơ sở còn lại. Lớp thứ hai chuyên biệt cho một header được xác định bởi tên của header, bằng cách sử dụng một bảng tra cứu được lưu trong :class:`.HeaderRegistry`. Tất cả những việc này được quản lý minh bạch đối với chương trình ứng dụng thông thường, nhưng các giao diện được cung cấp để sửa đổi hành vi mặc định nhằm phục vụ những ứng dụng phức tạp hơn.

Các phần bên dưới trước tiên mô tả các lớp cơ sở của header và các thuộc tính của chúng, tiếp theo là API để sửa đổi hành vi của :class:`.HeaderRegistry`, và cuối cùng là các lớp hỗ trợ dùng để biểu diễn dữ liệu được phân tích từ các header có cấu trúc.


.. class:: BaseHeader(name, value)

   *name* và *value* được truyền vào ``BaseHeader`` từ
   :attr:`~email.policy.EmailPolicy.header_factory` call. Giá trị chuỗi của bất kỳ đối tượng header nào là *value* được giải mã hoàn toàn thành một chuỗi.

   Lớp cơ sở này định nghĩa các thuộc tính chỉ đọc sau:


   .. attribute:: name

      Tên của header (phần của trường nằm trước ':'). Đây chính xác là giá trị được truyền vào
      Lệnh gọi :attr:`~email.policy.EmailPolicy.header_factory` cho *name*; tức là, chữ hoa chữ thường được giữ nguyên.


   .. attribute:: defects

      Một tuple gồm các thực thể :exc:`~email.errors.HeaderDefect` báo cáo mọi vấn đề về tính tuân thủ RFC được phát hiện trong quá trình phân tích cú pháp. Gói email cố gắng phát hiện đầy đủ các vấn đề về tính tuân thủ. Xem module :mod:`~email.errors` để biết thêm về các loại lỗi có thể được báo cáo.


   .. attribute:: max_count

      Số lượng header tối đa thuộc loại này có thể có cùng ``name``. Giá trị ``None`` có nghĩa là không giới hạn. Giá trị ``BaseHeader`` của thuộc tính này là ``None``; dự kiến các lớp header chuyên biệt sẽ ghi đè giá trị này khi cần.

   ``BaseHeader`` cũng cung cấp phương thức sau, được mã email gọi và nhìn chung không nên được các chương trình ứng dụng gọi:

   .. method:: fold(*, policy)

      Trả về một chuỗi chứa các ký tự :attr:`~email.policy.Policy.linesep` cần thiết để gấp header đúng theo *policy*. Một :attr:`~email.policy.Policy.cte_type` có giá trị ``8bit`` sẽ được xử lý như thể nó là ``7bit``, vì header không được chứa dữ liệu nhị phân tùy ý. Nếu :attr:`~email.policy.EmailPolicy.utf8` là ``False``, dữ liệu non-ASCII sẽ được mã hóa bằng :rfc:`2047`.


   Bản thân ``BaseHeader`` không thể được dùng để tạo đối tượng header. Nó định nghĩa một protocol mà mỗi header chuyên biệt phối hợp để tạo ra đối tượng header. Cụ thể, ``BaseHeader`` yêu cầu lớp chuyên biệt cung cấp một :func:`classmethod` có tên ``parse``. Phương thức này được gọi như sau::

       parse(string, kwds)

   ``kwds`` là một từ điển chứa một khóa được khởi tạo sẵn, ``defects``. ``defects`` là một danh sách trống. Phương thức parse phải thêm mọi lỗi được phát hiện vào danh sách này. Khi trả về, từ điển ``kwds`` *phải* chứa giá trị cho ít nhất các khóa ``decoded``, ``defects`` và ``parse_tree``. ``decoded`` phải là giá trị chuỗi của header (tức là giá trị header đã được giải mã hoàn toàn thành một chuỗi). ``parse_tree`` được đặt thành cây phân tích cú pháp thu được khi phân tích header. Phương thức parse phải giả định rằng *string* có thể chứa các phần được mã hóa bằng content-transfer, nhưng cũng phải xử lý chính xác mọi ký tự Unicode hợp lệ để có thể phân tích các giá trị header chưa được mã hóa.

   ``BaseHeader``'s ``__new__`` sau đó tạo instance của header và gọi phương thức ``init`` của nó. Lớp chuyên biệt chỉ cần cung cấp phương thức ``init`` nếu muốn thiết lập các thuộc tính bổ sung ngoài những thuộc tính do chính ``BaseHeader`` cung cấp. Một phương thức ``init`` như vậy sẽ có dạng sau::

       def init(self, /, *args, **kw):
           self._myattr = kw.pop('myattr')
           super().init(*args, **kw)

   Nói cách khác, mọi nội dung bổ sung mà lớp chuyên biệt đưa vào dictionary ``kwds`` đều phải được loại bỏ và xử lý, còn các nội dung còn lại của ``kw`` (và ``args``) được truyền vào phương thức ``init`` ``BaseHeader``.


.. class:: UnstructuredHeader

   Header "unstructured" là kiểu header mặc định trong :rfc:`5322`. Mọi header không có cú pháp được chỉ định đều được xử lý dưới dạng unstructured. Ví dụ kinh điển về một header unstructured là
   header :mailheader:`Subject`.

   Trong :rfc:`5322`, header unstructured là một chuỗi văn bản tùy ý trong bộ ký tự ASCII. Tuy nhiên, :rfc:`2047` có một cơ chế tương thích với :rfc:`5322` để mã hóa văn bản không phải ASCII thành các ký tự ASCII trong giá trị header. Khi một *value* chứa các encoded word được truyền vào hàm khởi tạo, parser ``UnstructuredHeader`` sẽ chuyển các encoded word đó thành một chuỗi, tuân theo các quy tắc :rfc:`2047` đối với văn bản unstructured. Parser sử dụng các heuristic để cố gắng giải mã một số encoded word không tuân thủ. Trong những trường hợp này, các lỗi sẽ được đăng ký; tương tự, lỗi cũng được đăng ký đối với những vấn đề như ký tự không hợp lệ bên trong encoded word hoặc văn bản không được mã hóa.

   Kiểu header này không cung cấp thuộc tính bổ sung nào.


.. class:: DateHeader

   :rfc:`5322` quy định một định dạng rất cụ thể cho ngày tháng trong các email header. Parser ``DateHeader`` nhận dạng định dạng ngày tháng đó, đồng thời nhận dạng một số dạng biến thể đôi khi được tìm thấy "trong thực tế".

   Loại header này cung cấp các thuộc tính bổ sung sau:

   .. attribute:: datetime

      Nếu giá trị header có thể được nhận dạng là một ngày hợp lệ dưới dạng này hay dạng khác, thuộc tính này sẽ chứa một instance :class:`~datetime.datetime` biểu diễn ngày đó. Nếu múi giờ của ngày đầu vào được chỉ định là ``-0000`` (cho biết ngày ở UTC nhưng không chứa thông tin về múi giờ nguồn), thì :attr:`.datetime` sẽ là một :class:`~datetime.datetime` ngây thơ (naive). Nếu tìm thấy một độ lệch múi giờ cụ thể (bao gồm ``+0000``), thì :attr:`.datetime` sẽ chứa một ``datetime`` có thông tin múi giờ (aware), sử dụng :class:`datetime.timezone` để ghi lại độ lệch múi giờ.

   Giá trị ``decoded`` của header được xác định bằng cách định dạng ``datetime`` theo các quy tắc :rfc:`5322`; tức là, nó được đặt thành::

       email.utils.format_datetime(self.datetime)

   Khi tạo một ``DateHeader``, *value* có thể là
   Một instance :class:`~datetime.datetime`. Điều này có nghĩa là, chẳng hạn, đoạn mã sau đây hợp lệ và thực hiện đúng như mong đợi::

       msg['Date'] = datetime(2011, 7, 15, 21)

   Vì đây là một ``datetime`` ngây thơ (naive), nó sẽ được diễn giải là một timestamp UTC, và giá trị kết quả sẽ có múi giờ là ``-0000``. Hữu ích hơn nhiều là sử dụng hàm :func:`~email.utils.localtime` từ
   module :mod:`~email.utils`::

       msg['Date'] = utils.localtime()

   Ví dụ này đặt tiêu đề ngày thành thời gian và ngày hiện tại bằng cách sử dụng độ lệch múi giờ hiện tại.


.. class:: AddressHeader

   Các tiêu đề địa chỉ là một trong những kiểu tiêu đề có cấu trúc phức tạp nhất. Lớp ``AddressHeader`` cung cấp một giao diện tổng quát cho mọi tiêu đề địa chỉ.

   Loại header này cung cấp các thuộc tính bổ sung sau:


   .. attribute:: groups

      Một tuple gồm các đối tượng :class:`.Group` mã hóa các địa chỉ và nhóm được tìm thấy trong giá trị tiêu đề. Các địa chỉ không thuộc một nhóm nào được biểu diễn trong danh sách này dưới dạng ``Groups`` chỉ chứa một địa chỉ, trong đó :attr:`~.Group.display_name` là ``None``.


   .. attribute:: addresses

      Một tuple gồm các đối tượng :class:`.Address` mã hóa tất cả địa chỉ riêng lẻ trong giá trị tiêu đề. Nếu giá trị tiêu đề chứa bất kỳ nhóm nào, các địa chỉ riêng lẻ trong nhóm sẽ được đưa vào danh sách tại vị trí nhóm xuất hiện trong giá trị (nghĩa là danh sách địa chỉ được "làm phẳng" thành danh sách một chiều).

   Giá trị ``decoded`` của tiêu đề sẽ có tất cả các từ được mã hóa được giải mã thành một chuỗi. Tên miền được mã hóa theo :class:`~encodings.idna` cũng được giải mã thành một chuỗi. Giá trị ``decoded`` được thiết lập bằng cách :ref:`nối <meth-str-join>` các
   Giá trị :class:`str` của các phần tử thuộc thuộc tính ``groups`` với ``', '``.

   Có thể sử dụng danh sách các đối tượng :class:`.Address` và :class:`.Group` theo bất kỳ tổ hợp nào để đặt giá trị của address header. Các đối tượng ``Group`` có ``display_name`` là ``None`` sẽ được diễn giải là các địa chỉ đơn, cho phép sao chép danh sách địa chỉ với các nhóm được giữ nguyên bằng cách sử dụng danh sách lấy từ thuộc tính ``groups`` của header nguồn.


.. class:: SingleAddressHeader

   Một lớp con của :class:`.AddressHeader` bổ sung thêm một thuộc tính:


   .. attribute:: address

      Địa chỉ duy nhất được mã hóa bởi giá trị header. Nếu giá trị header thực sự chứa nhiều hơn một địa chỉ (vi phạm RFC theo :mod:`~email.policy` mặc định), việc truy cập thuộc tính này sẽ dẫn đến :exc:`ValueError`.


Nhiều lớp ở trên cũng có một biến thể ``Unique`` (ví dụ: ``UniqueUnstructuredHeader``). Điểm khác biệt duy nhất là trong biến thể ``Unique``, :attr:`~.BaseHeader.max_count` được đặt thành 1.


.. class:: MIMEVersionHeader

   Thực tế chỉ có một giá trị hợp lệ cho header :mailheader:`MIME-Version`, đó là ``1.0``. Để đảm bảo khả năng tương thích trong tương lai, lớp header này hỗ trợ các số phiên bản hợp lệ khác. Nếu một số phiên bản có giá trị hợp lệ theo :rfc:`2045`, đối tượng header sẽ có các giá trị khác ``None`` cho những thuộc tính sau:

   .. attribute:: version

      Số phiên bản dưới dạng chuỗi, với mọi khoảng trắng và/hoặc chú thích đã được loại bỏ.

   .. attribute:: major

      Số phiên bản chính dưới dạng số nguyên

   .. attribute:: minor

      Số phiên bản phụ dưới dạng số nguyên


.. class:: ParameterizedMIMEHeader

    Tất cả MIME header đều bắt đầu bằng tiền tố 'Content-'. Mỗi header cụ thể có một giá trị nhất định, được mô tả trong phần về class của header đó. Một số header cũng có thể nhận một danh sách các tham số bổ sung theo một định dạng chung. Class này đóng vai trò là class cơ sở cho tất cả MIME header nhận tham số.

    .. attribute:: params

       Một dictionary ánh xạ tên tham số với giá trị tham số.


.. class:: ContentTypeHeader

    Một class :class:`ParameterizedMIMEHeader` xử lý
    header :mailheader:`Content-Type`.

    .. attribute:: content_type

       Chuỗi content type, có dạng ``maintype/subtype``.

    .. attribute:: maintype

    .. attribute:: subtype


.. class:: ContentDispositionHeader

    Một class :class:`ParameterizedMIMEHeader` xử lý
    :mailheader:`Content-Disposition` header.

    .. attribute:: content_disposition

       ``inline`` và ``attachment`` là các giá trị hợp lệ duy nhất thường được sử dụng.


.. class:: ContentTransferEncodingHeader

   Xử lý header :mailheader:`Content-Transfer-Encoding`.

   .. attribute:: cte

      Các giá trị hợp lệ là ``7bit``, ``8bit``, ``base64`` và ``quoted-printable``. Xem :rfc:`2045` để biết thêm thông tin.



.. class:: HeaderRegistry(base_class=BaseHeader, \
                          default_class=UnstructuredHeader, \ use_default_map=True)

    Đây là factory được :class:`~email.policy.EmailPolicy` sử dụng theo mặc định. ``HeaderRegistry`` xây dựng lớp được dùng để tạo một thể hiện header một cách linh động, bằng cách sử dụng *base_class* và một lớp chuyên biệt được lấy từ registry mà nó lưu giữ. Khi một tên header nhất định không xuất hiện trong registry, lớp được chỉ định bởi *default_class* sẽ được dùng làm lớp chuyên biệt. Khi *use_default_map* là ``True`` (giá trị mặc định), ánh xạ tiêu chuẩn từ tên header đến các lớp sẽ được sao chép vào registry trong quá trình khởi tạo. *base_class* luôn là lớp cuối cùng trong danh sách :class:`~type.__bases__` của lớp được tạo.

    Các ánh xạ mặc định là:

      :subject:                   UniqueUnstructuredHeader
      :date:                      UniqueDateHeader
      :resent-date:               DateHeader
      :orig-date:                 UniqueDateHeader
      :sender:                    UniqueSingleAddressHeader
      :resent-sender:             SingleAddressHeader
      :to:                        UniqueAddressHeader
      :resent-to:                 AddressHeader
      :cc:                        UniqueAddressHeader
      :resent-cc:                 AddressHeader
      :bcc:                       UniqueAddressHeader
      :resent-bcc:                AddressHeader
      :from:                      UniqueAddressHeader
      :resent-from:               AddressHeader
      :reply-to:                  UniqueAddressHeader
      :mime-version:              MIMEVersionHeader
      :content-type:              ContentTypeHeader
      :content-disposition:       ContentDispositionHeader
      :content-transfer-encoding: ContentTransferEncodingHeader
      :message-id:                MessageIDHeader

    ``HeaderRegistry`` có các phương thức sau:


    .. method:: map_to_type(self, name, cls)

       *name* là tên của header cần ánh xạ. Tên này sẽ được chuyển thành chữ thường trong registry. *cls* là lớp chuyên biệt được sử dụng cùng với *base_class* để tạo lớp dùng để khởi tạo các header khớp với *name*.


    .. method:: __getitem__(name)

       Xây dựng và trả về một lớp để xử lý việc tạo header *name*.


    .. method:: __call__(name, value)

       Lấy header chuyên biệt liên kết với *name* từ registry (sử dụng *default_class* nếu *name* không xuất hiện trong registry), kết hợp nó với *base_class* để tạo ra một lớp, gọi hàm khởi tạo của lớp được xây dựng bằng cách truyền vào cùng danh sách đối số, rồi cuối cùng trả về instance của lớp được tạo theo cách đó.


Các lớp sau đây được dùng để biểu diễn dữ liệu được phân tích từ các header có cấu trúc và nhìn chung có thể được chương trình ứng dụng sử dụng để xây dựng các giá trị có cấu trúc nhằm gán cho những header cụ thể.


.. class:: Address(display_name='', username='', domain='', addr_spec=None)

   Lớp dùng để biểu diễn một địa chỉ email. Dạng tổng quát của một địa chỉ là::

      [display_name] <username@domain>

   hoặc::

      username@domain

   trong đó mỗi phần phải tuân theo các quy tắc cú pháp cụ thể được nêu trong
   :rfc:`5322`.

   Để thuận tiện, có thể chỉ định *addr_spec* thay cho *username* và *domain*; trong trường hợp đó, *username* và *domain* sẽ được phân tích từ *addr_spec*. Một *addr_spec* phải là một chuỗi được trích dẫn đúng theo RFC; nếu không, ``Address`` sẽ phát sinh lỗi. Các ký tự Unicode được cho phép và sẽ được mã hóa đúng cách khi tuần tự hóa. Tuy nhiên, theo các RFC, Unicode *not* được phép trong phần username của địa chỉ.

   .. attribute:: display_name

      Phần tên hiển thị của địa chỉ, nếu có, sau khi đã loại bỏ mọi dấu trích dẫn. Nếu địa chỉ không có tên hiển thị, thuộc tính này sẽ là một chuỗi rỗng.

   .. attribute:: username

      Phần ``username`` của địa chỉ, sau khi đã loại bỏ mọi dấu trích dẫn.

   .. attribute:: domain

      Phần ``domain`` của địa chỉ.

   .. attribute:: addr_spec

      Phần ``username@domain`` của địa chỉ, được trích dẫn đúng cách để sử dụng làm địa chỉ không kèm tên (dạng thứ hai được minh họa ở trên). Thuộc tính này không thể thay đổi.

   .. method:: __str__()

      Giá trị ``str`` của đối tượng là địa chỉ được trích dẫn theo
      các quy tắc :rfc:`5322`, nhưng không áp dụng Content Transfer Encoding cho bất kỳ ký tự non-ASCII nào.

   Để hỗ trợ SMTP (:rfc:`5321`), ``Address`` xử lý một trường hợp đặc biệt: nếu ``username`` và ``domain`` đều là chuỗi rỗng (hoặc ``None``), thì giá trị chuỗi của ``Address`` là ``<>``.


.. class:: Group(display_name=None, addresses=None)

   Lớp được dùng để biểu diễn một nhóm địa chỉ. Dạng tổng quát của một nhóm địa chỉ là::

     display_name: [address-list];

   Để thuận tiện khi xử lý các danh sách địa chỉ gồm hỗn hợp nhóm và địa chỉ đơn lẻ, bạn cũng có thể dùng ``Group`` để biểu diễn các địa chỉ đơn lẻ không thuộc nhóm nào bằng cách đặt *display_name* thành ``None`` và cung cấp danh sách địa chỉ đơn lẻ dưới dạng *addresses*.

   .. attribute:: display_name

      ``display_name`` của nhóm. Nếu nó là ``None`` và có đúng một ``Address`` trong ``addresses``, thì ``Group`` biểu diễn một địa chỉ đơn lẻ không thuộc nhóm nào.

   .. attribute:: addresses

      Một tuple :class:`.Address` có thể rỗng, biểu diễn các địa chỉ trong nhóm.

   .. method:: __str__()

      Giá trị ``str`` của một ``Group`` được định dạng theo :rfc:`5322`, nhưng không áp dụng Content Transfer Encoding cho bất kỳ ký tự non-ASCII nào. Nếu ``display_name`` là none và có một ``Address`` duy nhất trong danh sách ``addresses``, thì giá trị ``str`` sẽ giống với ``str`` của ``Address`` duy nhất đó.


.. rubric:: Chú thích cuối trang

.. [1] Được bổ sung lần đầu trong phiên bản 3.3 dưới dạng :term:`mô-đun tạm thời <provisional package>`
