:mod:`!email.contentmanager`: Quản lý nội dung MIME
---------------------------------------------------

.. module:: email.contentmanager
   :synopsis: Lưu trữ và truy xuất nội dung từ các phần MIME

.. moduleauthor:: R. David Murray <rdmurray@bitdance.com>
.. sectionauthor:: R. David Murray <rdmurray@bitdance.com>

**Mã nguồn:** :source:`Lib/email/contentmanager.py`

------------

.. versionadded:: 3.6 [1]_


.. class:: ContentManager()

   Lớp cơ sở cho các content manager. Cung cấp các cơ chế registry tiêu chuẩn để đăng ký các converter giữa nội dung MIME và những dạng biểu diễn khác, cũng như các phương thức dispatch ``get_content`` và ``set_content``.


   .. method:: get_content(msg, *args, **kw)

      Tra cứu một hàm handler dựa trên ``mimetype`` của *msg* (xem đoạn tiếp theo), gọi hàm đó, truyền vào tất cả đối số và trả về kết quả của lệnh gọi. Handler được kỳ vọng sẽ trích xuất payload từ *msg* và trả về một đối tượng mã hóa thông tin về dữ liệu đã trích xuất.

      Để tìm handler, hãy tìm các khóa sau trong registry và dừng lại ở khóa đầu tiên được tìm thấy:

      * chuỗi biểu thị loại MIME đầy đủ (``maintype/subtype``)
      * chuỗi biểu diễn ``maintype``
      * chuỗi rỗng

      Nếu không có khóa nào trong số này tạo ra handler, hãy raise một :exc:`KeyError` cho kiểu MIME đầy đủ.


   .. method:: set_content(msg, obj, *args, **kw)

      Nếu ``maintype`` là ``multipart``, hãy raise một :exc:`TypeError`; nếu không, hãy tra cứu một hàm handler dựa trên kiểu của *obj* (xem đoạn tiếp theo), gọi :meth:`~email.message.EmailMessage.clear_content` trên *msg*, rồi gọi hàm handler, truyền tất cả các đối số. Dự kiến handler sẽ chuyển đổi và lưu trữ *obj* vào *msg*, đồng thời có thể thực hiện các thay đổi khác đối với *msg*, chẳng hạn như thêm nhiều header MIME khác nhau để mã hóa thông tin cần thiết nhằm diễn giải dữ liệu đã lưu trữ.

      Để tìm handler, hãy lấy kiểu của *obj* (``typ = type(obj)``) và tìm các khóa sau trong registry, dừng lại ở khóa đầu tiên được tìm thấy:

      * chính kiểu đó (``typ``)
      * tên đầy đủ của kiểu (``typ.__module__ + '.' + typ.__qualname__``).
      * của kiểu :attr:`qualname <type.__qualname__>` (``typ.__qualname__``)
      * của kiểu :attr:`name <type.__name__>` (``typ.__name__``).

      Nếu không có trường hợp nào ở trên khớp, hãy lặp lại tất cả các bước kiểm tra trên cho từng kiểu trong :term:`MRO` (:attr:`typ.__mro__ <type.__mro__>`). Cuối cùng, nếu không có key nào khác cung cấp handler, hãy kiểm tra handler cho key ``None``. Nếu không có handler cho ``None``, hãy raise một :exc:`KeyError` cho tên đầy đủ của kiểu.

      Đồng thời thêm header :mailheader:`MIME-Version` nếu header này chưa tồn tại (xem thêm :class:`.MIMEPart`).


   .. method:: add_get_handler(key, handler)

      Đăng ký hàm *handler* làm handler cho *key*. Để biết các giá trị có thể có của *key*, hãy xem :meth:`get_content`.


   .. method:: add_set_handler(typekey, handler)

      Đăng ký *handler* làm hàm được gọi khi một object có kiểu khớp với *typekey* được truyền vào :meth:`set_content`. Để biết các giá trị có thể có của *typekey*, hãy xem :meth:`set_content`.


Các instance của Content Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hiện tại, package email chỉ cung cấp một content manager cụ thể duy nhất,
:data:`raw_data_manager`, mặc dù có thể sẽ có thêm các content manager khác trong tương lai.
:data:`raw_data_manager` là
:attr:`~email.policy.EmailPolicy.content_manager` được cung cấp bởi
:attr:`~email.policy.EmailPolicy` và các lớp dẫn xuất của nó.


.. data:: raw_data_manager

   Content manager này chỉ cung cấp một interface tối thiểu, mở rộng interface do chính :class:`~email.message.Message` cung cấp: nó chỉ xử lý văn bản, raw bytes và các đối tượng :class:`~email.message.Message`. Tuy nhiên, nó mang lại những lợi thế đáng kể so với API cơ sở: ``get_content`` trên một phần văn bản sẽ trả về một chuỗi mà ứng dụng không cần tự giải mã, ``set_content`` cung cấp một tập hợp tùy chọn phong phú để kiểm soát các header được thêm vào một phần và kiểm soát content transfer encoding, đồng thời cho phép sử dụng nhiều phương thức ``add_``, qua đó đơn giản hóa việc tạo các multipart message.

   .. method:: get_content(msg, errors='replace')

      Trả về payload của phần đó dưới dạng chuỗi (đối với các phần ``text``), hoặc một
      đối tượng :class:`~email.message.EmailMessage` (dành cho các phần ``message/rfc822``), hoặc đối tượng ``bytes`` (dành cho tất cả các kiểu không phải multipart khác). Phát sinh :exc:`KeyError` nếu được gọi trên ``multipart``. Nếu phần này là phần ``text`` và *errors* được chỉ định, hãy dùng nó làm trình xử lý lỗi khi giải mã payload thành chuỗi. Trình xử lý lỗi mặc định là ``replace``.

   .. method:: set_content(msg, <'str'>, subtype="plain", charset='utf-8', \
                           cte=None, \ disposition=None, filename=None, cid=None, \ params=None, headers=None)
               set_content(msg, <'bytes'>, maintype, subtype, cte="base64", \
                           disposition=None, filename=None, cid=None, \ params=None, headers=None)
               set_content(msg, <'EmailMessage'>, cte=None, \
                           disposition=None, filename=None, cid=None, \ params=None, headers=None)

       Thêm header và payload vào *msg*:

       Thêm một header :mailheader:`Content-Type` với giá trị ``maintype/subtype``.

       * Đối với ``str``, đặt MIME ``maintype`` thành ``text``, và đặt subtype thành *subtype* nếu được chỉ định, hoặc ``plain`` nếu không.
       * Đối với ``bytes``, sử dụng *maintype* và *subtype* đã chỉ định, hoặc raise một :exc:`TypeError` nếu chúng không được chỉ định.
       * Đối với các đối tượng :class:`~email.message.EmailMessage`, đặt maintype thành ``message``, và đặt subtype thành *subtype* nếu được chỉ định hoặc ``rfc822`` nếu không. Nếu *subtype* là ``partial``, raise một lỗi (phải sử dụng các đối tượng ``bytes`` để tạo các phần ``message/partial``).

       Nếu *charset* được cung cấp (chỉ hợp lệ cho ``str``), hãy mã hóa chuỗi thành bytes bằng bộ ký tự được chỉ định. Mặc định là ``utf-8``. Nếu *charset* được chỉ định là bí danh đã biết của một tên bộ ký tự MIME tiêu chuẩn, hãy sử dụng bộ ký tự tiêu chuẩn đó.

       Nếu *cte* được đặt, hãy mã hóa payload bằng encoding truyền nội dung được chỉ định và đặt header :mailheader:`Content-Transfer-Encoding` thành giá trị đó. Các giá trị có thể có của *cte* là ``quoted-printable``, ``base64``, ``7bit``, ``8bit`` và ``binary``. Nếu đầu vào không thể được mã hóa bằng encoding được chỉ định (ví dụ: chỉ định *cte* là ``7bit`` cho đầu vào chứa các giá trị không phải ASCII), hãy raise một
       :exc:`ValueError`.

       * Đối với các đối tượng ``str``, nếu *cte* chưa được đặt, hãy sử dụng heuristic để xác định encoding nhỏ gọn nhất. Trước khi mã hóa,
         :meth:`str.splitlines` được sử dụng để chuẩn hóa tất cả ranh giới dòng, đảm bảo rằng mỗi dòng của payload đều được kết thúc bằng thuộc tính :data:`~email.policy.Policy.linesep` của policy hiện tại (ngay cả khi chuỗi ban đầu không kết thúc bằng thuộc tính này).
       * Đối với các đối tượng ``bytes``, *cte* được xem là base64 nếu chưa được đặt và phép chuyển đổi newline nói trên sẽ không được thực hiện.
       * Đối với :class:`~email.message.EmailMessage`, theo :rfc:`2046`, hãy phát sinh lỗi nếu yêu cầu một *cte* có giá trị ``quoted-printable`` hoặc ``base64`` cho *subtype* ``rfc822``, cũng như bất kỳ *cte* nào khác ``7bit`` cho *subtype* ``external-body``. Đối với ``message/rfc822``, hãy sử dụng ``8bit`` nếu *cte* chưa được chỉ định. Với mọi giá trị khác của *subtype*, hãy sử dụng ``7bit``.

       .. note:: Một *cte* có giá trị ``binary`` hiện vẫn chưa hoạt động chính xác. Đối tượng ``EmailMessage`` sau khi được ``set_content`` sửa đổi là chính xác, nhưng :class:`~email.generator.BytesGenerator` không serialize đối tượng đó đúng cách.

       Nếu *disposition* được đặt, hãy sử dụng nó làm giá trị của
       :mailheader:`Content-Disposition` header. Nếu không được chỉ định và *filename* được chỉ định, hãy thêm header với giá trị ``attachment``. Nếu *disposition* không được chỉ định và *filename* cũng không được chỉ định, không thêm header. Các giá trị hợp lệ duy nhất cho *disposition* là ``attachment`` và ``inline``.

       Nếu *filename* được chỉ định, hãy sử dụng nó làm giá trị của tham số ``filename`` trong header :mailheader:`Content-Disposition`.

       Nếu *cid* được chỉ định, hãy thêm một header :mailheader:`Content-ID` với *cid* làm giá trị.

       Nếu *params* được chỉ định, hãy lặp qua phương thức ``items`` của nó và sử dụng các cặp ``(key, value)`` thu được để đặt các tham số bổ sung trên
       header :mailheader:`Content-Type`.

       Nếu *headers* được chỉ định và là một danh sách các chuỗi có dạng ``headername: headervalue`` hoặc một danh sách các đối tượng ``header`` (được phân biệt với chuỗi vì có thuộc tính ``name``), hãy thêm các header vào *msg*.


.. rubric:: Chú thích cuối trang

.. [1] Được thêm lần đầu trong 3.4 dưới dạng :term:`module tạm thời <provisional package>`
