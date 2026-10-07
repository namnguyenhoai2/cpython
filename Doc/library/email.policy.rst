:mod:`!email.policy`: Đối tượng Policy
--------------------------------------

.. module:: email.policy
   :synopsis: Kiểm soát việc phân tích cú pháp và tạo thư

.. moduleauthor:: R. David Murray <rdmurray@bitdance.com>
.. sectionauthor:: R. David Murray <rdmurray@bitdance.com>

.. versionadded:: 3.3

**Mã nguồn:** :source:`Lib/email/policy.py`

--------------

Mục tiêu chính của gói :mod:`email` là xử lý các thông điệp email theo mô tả trong nhiều RFC về email và MIME. Tuy nhiên, định dạng chung của thông điệp email (một khối gồm các trường header, mỗi trường bao gồm một tên theo sau là dấu hai chấm rồi đến một giá trị; toàn bộ khối được theo sau bởi một dòng trống và một “body” tùy ý) đã được sử dụng hữu ích bên ngoài phạm vi email. Một số cách sử dụng này khá phù hợp với các RFC chính về email, trong khi một số cách khác thì không. Ngay cả khi làm việc với email, đôi khi việc không tuân thủ nghiêm ngặt các RFC vẫn là điều mong muốn, chẳng hạn như khi tạo email có thể hoạt động với các email server vốn không tuân theo các tiêu chuẩn này, hoặc triển khai các extension mà bạn muốn sử dụng theo những cách vi phạm tiêu chuẩn.

Các đối tượng Policy giúp gói email đủ linh hoạt để xử lý tất cả những trường hợp sử dụng khác nhau này.

Một đối tượng :class:`Policy` đóng gói một tập hợp các thuộc tính và phương thức kiểm soát cách hoạt động của nhiều thành phần khác nhau trong gói email khi được sử dụng.
Các instance :class:`Policy` có thể được truyền cho nhiều lớp và phương thức khác nhau trong gói email để thay đổi hành vi mặc định. Các giá trị có thể thiết lập và giá trị mặc định của chúng được mô tả bên dưới.

Có một policy mặc định được tất cả các lớp trong gói email sử dụng. Đối với tất cả các lớp :mod:`~email.parser` và các hàm tiện ích liên quan, cũng như lớp :class:`~email.message.Message`, đây là policy :class:`Compat32`, thông qua instance được định nghĩa sẵn tương ứng :const:`compat32`. Policy này cung cấp khả năng tương thích ngược hoàn toàn (trong một số trường hợp, bao gồm cả khả năng tương thích với lỗi) với phiên bản gói email trước Python 3.3.

Giá trị mặc định của từ khóa *policy* dành cho
:class:`~email.message.EmailMessage` là policy :class:`EmailPolicy`, thông qua instance được định nghĩa sẵn :data:`~default`.

Khi một đối tượng :class:`~email.message.Message` hoặc :class:`~email.message.EmailMessage` được tạo, nó sẽ nhận một policy. Nếu thông điệp được tạo bởi một
:mod:`~email.parser`, policy được truyền cho trình phân tích cú pháp sẽ là policy được thông điệp mà trình phân tích cú pháp đó tạo ra sử dụng. Nếu thông điệp được chương trình tạo ra, policy có thể được chỉ định khi thông điệp được tạo. Khi một thông điệp được truyền cho một
:mod:`~email.generator`, generator mặc định sẽ sử dụng policy từ thông điệp, nhưng bạn cũng có thể truyền một policy cụ thể cho generator để ghi đè policy được lưu trên đối tượng thông điệp.

Giá trị mặc định của từ khóa *policy* dành cho các lớp :mod:`email.parser` và các hàm tiện ích của trình phân tích cú pháp **sẽ thay đổi** trong một phiên bản Python tương lai. Vì vậy, bạn nên **luôn chỉ định rõ ràng policy mà bạn muốn sử dụng** khi gọi bất kỳ lớp và hàm nào được mô tả trong
mô-đun :mod:`~email.parser`.

Phần đầu tiên của tài liệu này trình bày các tính năng của :class:`Policy`, một
:term:`abstract base class` định nghĩa các tính năng chung cho tất cả các đối tượng policy, bao gồm cả :const:`compat32`. Phần này cũng bao gồm một số hook method được package email gọi nội bộ; custom policy có thể ghi đè chúng để có hành vi khác. Phần thứ hai mô tả các lớp cụ thể :class:`EmailPolicy` và :class:`Compat32`, lần lượt triển khai các hook cung cấp hành vi tiêu chuẩn và hành vi tương thích ngược cùng các tính năng tương ứng.

Các thực thể :class:`Policy` là bất biến, nhưng có thể được sao chép bằng cách nhận các đối số từ khóa giống như hàm khởi tạo của lớp và trả về một
thực thể :class:`Policy` mới, là bản sao của thực thể ban đầu nhưng có các giá trị thuộc tính được chỉ định đã thay đổi.

Ví dụ, đoạn mã sau có thể được dùng để đọc một email từ tệp trên đĩa và truyền nó cho chương trình ``sendmail`` của hệ thống trên Unix:

.. testsetup::

   from unittest import mock
   mocker = mock.patch('subprocess.Popen')
   m = mocker.start()
   proc = mock.MagicMock()
   m.return_value = proc
   proc.stdin.close.return_value = None
   mymsg = open('mymsg.txt', 'w')
   mymsg.write('To: abc@xyz.com\n\n')
   mymsg.flush()

.. doctest::

   >>> from email import message_from_binary_file
   >>> from email.generator import BytesGenerator
   >>> from email import policy
   >>> from subprocess import Popen, PIPE
   >>> with open('mymsg.txt', 'rb') as f:
   ...     msg = message_from_binary_file(f, policy=policy.default)
   ...
   >>> p = Popen(['sendmail', msg['To'].addresses[0]], stdin=PIPE)
   >>> g = BytesGenerator(p.stdin, policy=msg.policy.clone(linesep='\r\n'))
   >>> g.flatten(msg)
   >>> p.stdin.close()
   >>> rc = p.wait()

.. testcleanup::

   mymsg.close()
   mocker.stop()
   import os
   os.remove('mymsg.txt')

Ở đây, chúng ta yêu cầu :class:`~email.generator.BytesGenerator` sử dụng các ký tự phân cách dòng đúng theo RFC khi tạo chuỗi nhị phân để truyền vào ``sendmail's`` ``stdin``, trong khi policy mặc định sẽ sử dụng các ký tự phân cách dòng ``\n``.

Một số phương thức của gói email chấp nhận đối số từ khóa *policy*, cho phép ghi đè policy cho phương thức đó. Ví dụ, đoạn mã sau sử dụng phương thức :meth:`~email.message.Message.as_bytes` của đối tượng *msg* từ ví dụ trước và ghi message vào một tệp bằng cách sử dụng các dấu phân cách dòng gốc của nền tảng mà nó đang chạy trên đó::

   >>> import os
   >>> with open('converted.txt', 'wb') as f:
   ...     f.write(msg.as_bytes(policy=msg.policy.clone(linesep=os.linesep)))
   17

Các đối tượng policy cũng có thể được kết hợp bằng toán tử cộng, tạo ra một đối tượng policy có các thiết lập là sự kết hợp của những giá trị không mặc định trong các đối tượng được cộng::

   >>> compat_SMTP = policy.compat32.clone(linesep='\r\n')
   >>> compat_strict = policy.compat32.clone(raise_on_defect=True)
   >>> compat_strict_SMTP = compat_SMTP + compat_strict

Phép toán này không giao hoán; nghĩa là thứ tự cộng các đối tượng có ảnh hưởng. Để minh họa::

   >>> policy100 = policy.compat32.clone(max_line_length=100)
   >>> policy80 = policy.compat32.clone(max_line_length=80)
   >>> apolicy = policy100 + policy80
   >>> apolicy.max_line_length
   80
   >>> apolicy = policy80 + policy100
   >>> apolicy.max_line_length
   100


.. class:: Policy(**kw)

   Đây là :term:`abstract base class` cho tất cả các lớp policy. Nó cung cấp các triển khai mặc định cho một vài phương thức đơn giản, cũng như triển khai thuộc tính bất biến, phương thức :meth:`clone` và ngữ nghĩa của hàm khởi tạo.

   Hàm khởi tạo của một lớp policy có thể nhận nhiều đối số từ khóa khác nhau. Các đối số có thể được chỉ định là mọi thuộc tính không phải phương thức trên lớp này, cùng với mọi thuộc tính không phải phương thức bổ sung trên lớp cụ thể. Giá trị được chỉ định trong hàm khởi tạo sẽ ghi đè giá trị mặc định của thuộc tính tương ứng.

   Lớp này định nghĩa các thuộc tính sau, vì vậy các giá trị tương ứng có thể được truyền vào hàm khởi tạo của bất kỳ lớp policy nào:


   .. attribute:: max_line_length

      Độ dài tối đa của bất kỳ dòng nào trong đầu ra đã được tuần tự hóa, không tính (các) ký tự kết thúc dòng. Giá trị mặc định là 78, theo :rfc:`5322`. Giá trị ``0`` hoặc :const:`None` cho biết rằng hoàn toàn không được ngắt dòng.


   .. attribute:: linesep

      Chuỗi được sử dụng để kết thúc các dòng trong đầu ra đã tuần tự hóa.  Giá trị mặc định là ``\n`` vì đó là quy tắc kết thúc dòng nội bộ được Python sử dụng, mặc dù ``\r\n`` là bắt buộc theo các RFC.


   .. attribute:: cte_type

      Kiểm soát các loại Content Transfer Encodings có thể hoặc bắt buộc phải được sử dụng.  Các giá trị có thể có là:

      .. tabularcolumns:: |l|L|

      +----------+-----------------------------------------------------------------------------------------------------------------------------------------+
      | ``7bit`` | tất cả dữ liệu phải "7 bit clean" (chỉ ASCII).  Điều này có nghĩa là khi cần, dữ liệu sẽ được mã hóa bằng quoted-printable hoặc base64. |
      +----------+-----------------------------------------------------------------------------------------------------------------------------------------+
      | ``8bit`` | dữ liệu không bị giới hạn ở dạng 7 bit clean.  Dữ liệu trong header vẫn phải chỉ chứa ASCII và do đó sẽ được mã hóa (xem                |
      |          | :meth:`fold_binary` và :attr:`~EmailPolicy.utf8` bên dưới để biết các ngoại lệ), nhưng các phần thân có thể sử dụng CTE ``8bit``.       |
      +----------+-----------------------------------------------------------------------------------------------------------------------------------------+

      Giá trị ``cte_type`` là ``8bit`` chỉ hoạt động với ``BytesGenerator``, không phải ``Generator``, vì chuỗi không thể chứa dữ liệu nhị phân.  Nếu một ``Generator`` đang hoạt động theo policy chỉ định ``cte_type=8bit``, nó sẽ hoạt động như thể ``cte_type`` là ``7bit``.


   .. attribute:: raise_on_defect

      Nếu :const:`True`, mọi lỗi gặp phải sẽ được ném dưới dạng lỗi.  Nếu
      :const:`False` (mặc định), các lỗi sẽ được chuyển vào
      phương thức :meth:`register_defect`.


   .. attribute:: mangle_from_

      Nếu :const:`True`, các dòng bắt đầu bằng *"From "* trong phần thân sẽ được escape bằng cách đặt một ``>`` ở phía trước chúng. Tham số này được sử dụng khi thư đang được serialize bởi một generator. Mặc định: :const:`False`.

      .. versionadded:: 3.5


   .. attribute:: message_factory

      Một hàm factory dùng để tạo một đối tượng message mới, rỗng. Được parser sử dụng khi xây dựng các message. Mặc định là ``None``, trong trường hợp đó :class:`~email.message.Message` được sử dụng.

      .. versionadded:: 3.6


   .. attribute:: verify_generated_headers

      Nếu ``True`` (mặc định), generator sẽ raise
      :exc:`~email.errors.HeaderWriteError` thay vì ghi một header bị ngắt dòng hoặc phân tách không đúng, khiến nó bị phân tích thành nhiều header hoặc được nối với dữ liệu liền kề. Các header như vậy có thể được tạo bởi các custom header class hoặc do lỗi trong module ``email``.

      Vì đây là một tính năng bảo mật, giá trị này mặc định là ``True`` ngay cả trong
      :class:`~email.policy.Compat32` chính sách. Để có hành vi tương thích ngược nhưng không an toàn, phải đặt nó thành ``False`` một cách tường minh.

      .. versionadded:: 3.13


   Phương thức :class:`Policy` sau đây được thiết kế để code sử dụng thư viện email gọi nhằm tạo các instance policy với các thiết lập tùy chỉnh:


   .. method:: clone(**kw)

      Trả về một instance :class:`Policy` mới có các thuộc tính cùng giá trị với instance hiện tại, ngoại trừ những thuộc tính được các keyword argument chỉ định giá trị mới.


   Các phương thức :class:`Policy` còn lại được code của package email gọi và không предназначены để ứng dụng sử dụng package email gọi trực tiếp. Một policy tùy chỉnh phải triển khai tất cả các phương thức này.


   .. method:: handle_defect(obj, defect)

      Xử lý một *defect* được phát hiện trên *obj*. Khi package email gọi phương thức này, *defect* sẽ luôn là một lớp con của
      :class:`~email.errors.MessageDefect`.

      Cách triển khai mặc định kiểm tra cờ :attr:`raise_on_defect`. Nếu cờ là ``True``, *defect* sẽ được raise dưới dạng exception. Nếu cờ là ``False`` (mặc định), *obj* và *defect* được truyền cho :meth:`register_defect`.


   .. method:: register_defect(obj, defect)

      Đăng ký một *defect* trên *obj*. Trong package email, *defect* sẽ luôn là một lớp con của :class:`~email.errors.MessageDefect`.

      Cách triển khai mặc định gọi phương thức ``append`` của thuộc tính ``defects`` của *obj*. Khi gói email gọi :attr:`handle_defect`, *obj* thường sẽ có một thuộc tính ``defects`` có phương thức ``append``. Các kiểu đối tượng tùy chỉnh được sử dụng với gói email (ví dụ: các đối tượng ``Message`` tùy chỉnh) cũng nên cung cấp thuộc tính như vậy; nếu không, các lỗi trong những message đã phân tích sẽ gây ra các lỗi không mong muốn.


   .. method:: header_max_count(name)

      Trả về số lượng header tối đa được phép có tên *name*.

      Được gọi khi một header được thêm vào đối tượng :class:`~email.message.EmailMessage` hoặc :class:`~email.message.Message`. Nếu giá trị trả về không phải là ``0`` hoặc ``None``, và đã có số lượng header có tên *name* lớn hơn hoặc bằng giá trị được trả về, một
      :exc:`ValueError` sẽ được ném ra.

      Vì hành vi mặc định của ``Message.__setitem__`` là nối giá trị vào danh sách header, bạn rất dễ vô tình tạo ra các header trùng lặp. Phương thức này cho phép giới hạn số lượng instance của một số header nhất định có thể được thêm vào một ``Message`` theo cách lập trình. (Giới hạn này không được parser áp dụng; parser sẽ trung thực tạo ra số header tương ứng với số header tồn tại trong message đang được phân tích.)

      Cách triển khai mặc định trả về ``None`` cho mọi tên header.


   .. method:: header_source_parse(sourcelines)

      Gói email gọi phương thức này với một danh sách các chuỗi, trong đó mỗi chuỗi kết thúc bằng các ký tự phân tách dòng được tìm thấy trong nguồn đang được phân tích. Dòng đầu tiên chứa tên field header và dấu phân tách. Tất cả khoảng trắng trong nguồn đều được giữ nguyên. Phương thức này phải trả về tuple ``(name, value)`` được lưu trữ trong ``Message`` để biểu diễn header đã phân tích.

      Nếu một triển khai muốn duy trì khả năng tương thích với các policy hiện có của gói email, *name* phải là tên được giữ nguyên phân biệt hoa thường (tất cả ký tự cho đến dấu phân cách '``:``'), còn *value* phải là giá trị đã được loại bỏ ngắt dòng (đã loại bỏ tất cả ký tự phân cách dòng nhưng vẫn giữ nguyên khoảng trắng), sau khi loại bỏ khoảng trắng ở đầu.

      *sourcelines* có thể chứa dữ liệu nhị phân được xử lý bằng surrogateescape.

      Không có triển khai mặc định


   .. method:: header_store_parse(name, value)

      Gói email gọi phương thức này với tên và giá trị do chương trình ứng dụng cung cấp khi chương trình ứng dụng đang sửa đổi một ``Message`` theo cách lập trình (trái với một ``Message`` được tạo bởi parser). Phương thức này phải trả về tuple ``(name, value)`` được lưu trữ trong ``Message`` để biểu diễn header.

      Nếu một triển khai muốn duy trì khả năng tương thích với các policy hiện có của gói email, *name* và *value* phải là các chuỗi hoặc lớp con của chuỗi không thay đổi nội dung của các đối số được truyền vào.

      Không có triển khai mặc định


   .. method:: header_fetch_parse(name, value)

      Gói email gọi phương thức này với *name* và *value* hiện đang được lưu trữ trong ``Message`` khi header đó được chương trình ứng dụng yêu cầu, và bất cứ giá trị nào phương thức trả về sẽ được truyền lại cho ứng dụng dưới dạng giá trị của header đang được truy xuất. Lưu ý rằng có thể có nhiều header cùng tên được lưu trữ trong ``Message``; phương thức nhận được tên và giá trị cụ thể của header sẽ được trả về cho ứng dụng.

      *value* có thể chứa dữ liệu nhị phân được escape bằng surrogate. Giá trị do phương thức trả về không được chứa dữ liệu nhị phân được escape bằng surrogate.

      Không có triển khai mặc định


   .. method:: fold(name, value)

      Gói email gọi phương thức này với *name* và *value* hiện đang được lưu trữ trong ``Message`` cho một header cụ thể. Phương thức này phải trả về một chuỗi biểu diễn header đã được "fold" đúng cách (theo các thiết lập policy) bằng cách ghép *name* với *value* và chèn
      các ký tự :attr:`linesep` vào những vị trí thích hợp. Xem :rfc:`5322` để biết thêm về các quy tắc folding header email.

      *value* có thể chứa dữ liệu nhị phân được escape bằng surrogate. Chuỗi do phương thức trả về không được chứa dữ liệu nhị phân được escape bằng surrogate.


   .. method:: fold_binary(name, value)

      Tương tự như :meth:`fold`, ngoại trừ việc giá trị trả về phải là một đối tượng bytes thay vì một chuỗi.

      *value* có thể chứa dữ liệu nhị phân được escape bằng surrogate. Dữ liệu này có thể được chuyển đổi trở lại thành dữ liệu nhị phân trong đối tượng bytes được trả về.



.. class:: EmailPolicy(**kw)

   :class:`Policy` cụ thể này cung cấp hành vi được thiết kế để hoàn toàn tuân thủ các RFC email hiện hành. Các RFC này bao gồm nhưng không giới hạn ở :rfc:`5322`, :rfc:`2047` và các RFC MIME hiện hành.

   Policy này bổ sung các thuật toán mới để phân tích cú pháp và folding header. Thay vì là các chuỗi đơn giản, header là các lớp con của ``str`` với các thuộc tính phụ thuộc vào kiểu của field. Thuật toán phân tích cú pháp và folding triển khai đầy đủ
   :rfc:`2047` và :rfc:`5322`.

   Giá trị mặc định của thuộc tính :attr:`~email.policy.Policy.message_factory` là :class:`~email.message.EmailMessage`.

   Ngoài các thuộc tính có thể thiết lập được liệt kê ở trên và áp dụng cho mọi policy, policy này bổ sung các thuộc tính sau:

   .. versionadded:: 3.6 [1]_


   .. attribute:: utf8

      Nếu ``False``, hãy làm theo :rfc:`5322`, hỗ trợ các ký tự không phải ASCII trong header bằng cách mã hóa chúng thành "encoded words". Nếu ``True``, hãy làm theo
      :rfc:`6532` và sử dụng mã hóa ``utf-8`` cho header. Các message được định dạng theo cách này có thể được chuyển đến các SMTP server hỗ trợ extension ``SMTPUTF8`` (:rfc:`6531`).


   .. attribute:: refold_source

      Nếu giá trị của một header trong đối tượng ``Message`` bắt nguồn từ một
      :mod:`~email.parser` (thay vì được chương trình thiết lập), thuộc tính này cho biết generator có nên gấp lại giá trị đó khi chuyển đổi message trở lại dạng đã tuần tự hóa hay không. Các giá trị có thể có là:

      +----------+----------------------------------------------------------------------------------+
      | ``none`` | tất cả giá trị nguồn sử dụng cách gấp ban đầu                                    |
      +----------+----------------------------------------------------------------------------------+
      | ``long`` | các giá trị nguồn có bất kỳ dòng nào dài hơn ``max_line_length`` sẽ được gấp lại |
      +----------+----------------------------------------------------------------------------------+
      | ``all``  | tất cả các giá trị đều được gấp lại.                                             |
      +----------+----------------------------------------------------------------------------------+

      Giá trị mặc định là ``long``.


   .. attribute:: header_factory

      Một callable nhận hai đối số, ``name`` và ``value``, trong đó ``name`` là tên trường header và ``value`` là giá trị trường header đã được bỏ gấp, rồi trả về một lớp con của string đại diện cho header đó. Một ``header_factory`` mặc định (xem :mod:`~email.headerregistry`) được cung cấp để hỗ trợ phân tích cú pháp tùy chỉnh cho các kiểu trường header địa chỉ và ngày tháng :RFC:`5322`, cũng như các kiểu trường header MIME chính. Hỗ trợ phân tích cú pháp tùy chỉnh bổ sung sẽ được thêm trong tương lai.


   .. attribute:: content_manager

      Một đối tượng có ít nhất hai phương thức: get_content và set_content. Khi :meth:`~email.message.EmailMessage.get_content` hoặc
      :meth:`~email.message.EmailMessage.set_content` là phương thức của một
      Khi :class:`~email.message.EmailMessage` được gọi như một đối tượng, nó sẽ gọi phương thức tương ứng của đối tượng này, truyền đối tượng message cho phương thức đó làm đối số đầu tiên, cùng với mọi đối số hoặc keyword đã được truyền cho nó dưới dạng các đối số bổ sung. Theo mặc định ``content_manager`` được đặt thành
      :data:`~email.contentmanager.raw_data_manager`.

      .. versionadded:: 3.4


   Lớp này cung cấp các triển khai cụ thể sau đây của các phương thức trừu tượng của :class:`Policy`:


   .. method:: header_max_count(name)

      Trả về giá trị của thuộc tính
      :attr:`~email.headerregistry.BaseHeader.max_count` của lớp chuyên biệt được dùng để biểu diễn header có tên đã cho.


   .. method:: header_source_parse(sourcelines)


      Tên được phân tích cú pháp là mọi thứ cho đến '``:``' và được trả về không sửa đổi. Giá trị được xác định bằng cách loại bỏ khoảng trắng ở đầu phần còn lại của dòng đầu tiên, nối tất cả các dòng tiếp theo lại với nhau, rồi loại bỏ mọi ký tự carriage return hoặc linefeed ở cuối.


   .. method:: header_store_parse(name, value)

      Tên được trả về không thay đổi. Nếu giá trị đầu vào có thuộc tính ``name`` và thuộc tính đó khớp với *name* mà không phân biệt chữ hoa chữ thường, giá trị được trả về không thay đổi. Nếu không, *name* và *value* được truyền vào ``header_factory``, rồi đối tượng header kết quả được trả về làm giá trị. Trong trường hợp này, một ``ValueError`` được phát sinh nếu giá trị đầu vào chứa các ký tự CR hoặc LF.


   .. method:: header_fetch_parse(name, value)

      Nếu giá trị có thuộc tính ``name``, giá trị đó được trả về không thay đổi. Nếu không, *name* và *value* sau khi đã loại bỏ mọi ký tự CR hoặc LF được truyền vào ``header_factory``, rồi đối tượng header kết quả được trả về. Mọi byte được escape bằng surrogate sẽ được chuyển thành ký hiệu ký tự không xác định Unicode.


   .. method:: fold(name, value)

      Việc gấp header được kiểm soát bằng thiết lập policy :attr:`refold_source`. Một giá trị được xem là 'source value' khi và chỉ khi nó không có thuộc tính ``name`` (có thuộc tính ``name`` nghĩa là đó là một loại đối tượng header). Nếu một source value cần được gấp lại theo policy, nó được chuyển thành đối tượng header bằng cách truyền *name* và *value* sau khi đã loại bỏ mọi ký tự CR và LF vào ``header_factory``. Việc gấp một đối tượng header được thực hiện bằng cách gọi phương thức ``fold`` của đối tượng đó với policy hiện tại.

      Các source value được tách thành từng dòng bằng :meth:`~str.splitlines`. Nếu giá trị không cần được gấp lại, các dòng được nối lại bằng ``linesep`` từ policy rồi trả về. Ngoại lệ là các dòng chứa dữ liệu nhị phân không phải ASCII. Trong trường hợp đó, giá trị luôn được gấp lại bất kể thiết lập ``refold_source``, khiến dữ liệu nhị phân được mã hóa CTE bằng charset ``unknown-8bit``.


   .. method:: fold_binary(name, value)

      Giống :meth:`fold` khi :attr:`~Policy.cte_type` là ``7bit``, ngoại trừ việc giá trị được trả về là bytes.

      Nếu :attr:`~Policy.cte_type` là ``8bit``, dữ liệu nhị phân không phải ASCII được chuyển đổi trở lại thành bytes. Các header chứa dữ liệu nhị phân không được gấp lại, bất kể thiết lập ``refold_header``, vì không có cách nào biết dữ liệu nhị phân đó gồm các ký tự một byte hay các ký tự nhiều byte.


Các instance sau đây của :class:`EmailPolicy` cung cấp các giá trị mặc định phù hợp với những miền ứng dụng cụ thể. Lưu ý rằng trong tương lai, hành vi của các instance này (đặc biệt là instance ``HTTP``) có thể được điều chỉnh để phù hợp hơn nữa với các RFC liên quan đến những miền đó.


.. data:: default

   Một instance của ``EmailPolicy`` với tất cả giá trị mặc định được giữ nguyên. Policy này sử dụng kiểu kết thúc dòng ``\n`` tiêu chuẩn của Python thay vì ``\r\n`` đúng theo RFC.


.. data:: SMTP

   Phù hợp để tuần tự hóa các message tuân thủ những RFC về email. Giống ``default``, nhưng ``linesep`` được đặt thành ``\r\n``, tuân thủ RFC.


.. data:: SMTPUTF8

   Giống ``SMTP``, ngoại trừ việc :attr:`~EmailPolicy.utf8` là ``True``. Hữu ích khi tuần tự hóa các message vào message store mà không sử dụng encoded words trong các header. Chỉ nên được sử dụng để truyền qua SMTP nếu địa chỉ người gửi hoặc người nhận có ký tự non-ASCII (the
   phương thức :meth:`smtplib.SMTP.send_message` tự động xử lý việc này).


.. data:: HTTP

   Phù hợp để tuần tự hóa các header dùng trong lưu lượng HTTP. Giống ``SMTP``, ngoại trừ việc ``max_line_length`` được đặt thành ``None`` (không giới hạn).


.. data:: strict

   Instance tiện lợi. Giống ``default``, ngoại trừ việc ``raise_on_defect`` được đặt thành ``True``. Điều này cho phép làm cho bất kỳ policy nào trở nên strict bằng cách viết::

        somepolicy + policy.strict


Với tất cả các :class:`EmailPolicies <.EmailPolicy>` này, API hiệu lực của package email được thay đổi so với API Python 3.2 theo những cách sau:

* Việc đặt một header trên :class:`~email.message.Message` sẽ khiến header đó được phân tích cú pháp và một header object được tạo.

* Việc lấy giá trị header từ :class:`~email.message.Message` sẽ khiến header đó được phân tích cú pháp, một header object được tạo và trả về.

* Mọi header object hoặc mọi header được gấp lại do các thiết lập policy sẽ được gấp bằng một thuật toán triển khai đầy đủ các thuật toán gấp của RFC, bao gồm cả việc xác định vị trí các encoded word được yêu cầu và được phép.

Theo cách nhìn từ phía ứng dụng, điều này có nghĩa là bất kỳ header nào được lấy thông qua
:class:`~email.message.EmailMessage` đều là một header object có thêm các thuộc tính, trong đó giá trị chuỗi là giá trị đã được giải mã hoàn toàn của header. Tương tự, một header có thể được gán giá trị mới hoặc tạo header mới bằng một chuỗi, và policy sẽ đảm nhiệm việc chuyển đổi chuỗi đó sang dạng được mã hóa đúng theo RFC.

Các header object và thuộc tính của chúng được mô tả trong
:mod:`~email.headerregistry`.



.. class:: Compat32(**kw)

   :class:`Policy` cụ thể này là policy tương thích ngược. Nó mô phỏng hành vi của email package trong Python 3.2. The
   Mô-đun :mod:`!policy` cũng định nghĩa một thực thể của lớp này,
   :const:`compat32`, được sử dụng làm policy mặc định. Do đó, hành vi mặc định của package email là duy trì khả năng tương thích với Python 3.2.

   Các thuộc tính sau đây có các giá trị khác với
   mặc định của :class:`Policy`:


   .. attribute:: mangle_from_

      Giá trị mặc định là ``True``.


   Lớp này cung cấp các triển khai cụ thể sau đây của các phương thức trừu tượng của :class:`Policy`:


   .. method:: header_source_parse(sourcelines)

      Tên được phân tích cú pháp là mọi thứ cho đến '``:``' và được trả về không sửa đổi. Giá trị được xác định bằng cách loại bỏ khoảng trắng ở đầu phần còn lại của dòng đầu tiên, nối tất cả các dòng tiếp theo lại với nhau, rồi loại bỏ mọi ký tự carriage return hoặc linefeed ở cuối.


   .. method:: header_store_parse(name, value)

      Tên và giá trị được trả về mà không sửa đổi.


   .. method:: header_fetch_parse(name, value)

      Nếu giá trị chứa dữ liệu nhị phân, nó được chuyển đổi thành một
      :class:`~email.header.Header` object bằng charset ``unknown-8bit``. Nếu không, nó được trả về mà không sửa đổi.


   .. method:: fold(name, value)

      Headers được gấp dòng bằng thuật toán folding :class:`~email.header.Header`, giữ nguyên các ngắt dòng hiện có trong giá trị và bọc mỗi dòng kết quả theo ``max_line_length``. Dữ liệu nhị phân không phải ASCII được mã hóa CTE bằng charset ``unknown-8bit``.


   .. method:: fold_binary(name, value)

      Headers được gấp dòng bằng thuật toán folding :class:`~email.header.Header`, giữ nguyên các ngắt dòng hiện có trong giá trị và bọc mỗi dòng kết quả theo ``max_line_length``. Nếu ``cte_type`` là ``7bit``, dữ liệu nhị phân không phải ASCII được mã hóa CTE bằng charset ``unknown-8bit``. Nếu không, header nguồn ban đầu được sử dụng, cùng các ngắt dòng hiện có và mọi dữ liệu nhị phân (không hợp lệ theo RFC) mà nó có thể chứa.


.. data:: compat32

   Một instance của :class:`Compat32`, cung cấp khả năng tương thích ngược với hành vi của package email trong Python 3.2.

   .. note::

      Policy :const:`compat32` không nên được sử dụng làm policy cho
      :class:`~email.message.EmailMessage` đối tượng và chỉ nên được sử dụng để tuần tự hóa các thư được tạo bằng chính sách :const:`compat32`.


.. rubric:: Chú thích cuối trang

.. [1] Được bổ sung lần đầu trong phiên bản 3.3 dưới dạng một :term:`tính năng thử nghiệm <provisional package>`.
