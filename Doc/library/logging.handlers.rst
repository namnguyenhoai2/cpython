:mod:`!logging.handlers` --- Các handler logging
================================================

.. module:: logging.handlers
   :synopsis: Các handler cho module logging.

.. moduleauthor:: Vinay Sajip <vinay_sajip@red-dove.com>
.. sectionauthor:: Vinay Sajip <vinay_sajip@red-dove.com>

**Mã nguồn:** :source:`Lib/logging/handlers.py`

.. sidebar:: Quan trọng

   Trang này chỉ chứa thông tin tham khảo. Để xem hướng dẫn, vui lòng xem

   * :ref:`Hướng dẫn cơ bản <logging-basic-tutorial>`
   * :ref:`Hướng dẫn nâng cao <logging-advanced-tutorial>`
   * :ref:`Sổ tay Logging <logging-cookbook>`

--------------

.. currentmodule:: logging

Package cung cấp các handler hữu ích sau đây. Lưu ý rằng ba trong số các handler (:class:`StreamHandler`, :class:`FileHandler` và
:class:`NullHandler`) thực tế được định nghĩa ngay trong module :mod:`logging`, nhưng được trình bày tài liệu ở đây cùng với các handler khác.

.. _stream-handler:

StreamHandler
^^^^^^^^^^^^^

Lớp :class:`StreamHandler`, nằm trong package :mod:`logging` cốt lõi, gửi đầu ra logging đến các stream như *sys.stdout*, *sys.stderr* hoặc bất kỳ đối tượng nào giống tệp (chính xác hơn là bất kỳ đối tượng nào hỗ trợ các phương thức :meth:`write` và :meth:`flush`).


.. class:: StreamHandler(stream=None)

   Trả về một instance mới của lớp :class:`StreamHandler`. Nếu *stream* được chỉ định, instance sẽ sử dụng stream đó cho đầu ra logging; nếu không, *sys.stderr* sẽ được sử dụng.


   .. method:: emit(record)

      Nếu một formatter được chỉ định, formatter đó sẽ được dùng để định dạng record. Sau đó, record được ghi vào stream, theo sau là :attr:`terminator`. Nếu có thông tin ngoại lệ, thông tin đó được định dạng bằng :func:`traceback.print_exception` và nối vào stream.


   .. method:: flush()

      Xả stream bằng cách gọi phương thức :meth:`flush` của nó. Lưu ý rằng
      phương thức :meth:`close` được kế thừa từ :class:`~logging.Handler` nên không tạo ra đầu ra nào, vì vậy đôi khi có thể cần gọi :meth:`flush` một cách rõ ràng.

   .. method:: setStream(stream)

      Đặt stream của instance thành giá trị được chỉ định nếu giá trị đó khác với giá trị hiện tại. Stream cũ sẽ được xả trước khi stream mới được thiết lập.

      :param stream: Stream mà handler sẽ sử dụng.

      :return: stream cũ nếu stream đã được thay đổi, hoặc ``None`` nếu chưa thay đổi.

      .. versionadded:: 3.7

   .. attribute:: terminator

      Chuỗi được sử dụng làm dấu kết thúc khi ghi một record đã được định dạng vào stream. Giá trị mặc định là ``'\n'``.

      Nếu không muốn kết thúc bằng ký tự dòng mới, bạn có thể đặt thuộc tính ``terminator`` của instance handler thành chuỗi rỗng.

      Trong các phiên bản trước, terminator được hardcode là ``'\n'``.

      .. versionadded:: 3.2


.. _file-handler:

FileHandler
^^^^^^^^^^^

Lớp :class:`FileHandler`, nằm trong gói :mod:`logging` cốt lõi, gửi đầu ra logging đến một tệp trên đĩa. Lớp này kế thừa chức năng xuất đầu ra từ
:class:`StreamHandler`.


.. class:: FileHandler(filename, mode='a', encoding=None, delay=False, errors=None)

   Trả về một instance mới của lớp :class:`FileHandler`. Tệp được chỉ định sẽ được mở và dùng làm stream cho việc ghi log. Nếu *mode* không được chỉ định, ``'a'`` sẽ được sử dụng. Nếu *encoding* khác ``None``, giá trị đó sẽ được dùng để mở tệp với encoding tương ứng. Nếu *delay* là true, việc mở tệp sẽ được trì hoãn cho đến lần gọi đầu tiên đến :meth:`emit`. Theo mặc định, tệp sẽ tăng kích thước vô hạn. Nếu *errors* được chỉ định, giá trị đó sẽ được dùng để xác định cách xử lý các lỗi encoding.

   .. versionchanged:: 3.6
      Ngoài các giá trị chuỗi, các đối tượng :class:`~pathlib.Path` cũng được chấp nhận cho đối số *filename*.

   .. versionchanged:: 3.9
      Tham số *errors* đã được bổ sung.

   .. method:: close()

      Đóng tệp.

   .. method:: emit(record)

      Ghi bản ghi vào tệp.

      Lưu ý rằng nếu tệp đã bị đóng do quá trình tắt logging khi thoát và chế độ tệp là 'w', bản ghi sẽ không được xuất (xem :issue:`42378`).


.. _null-handler:

NullHandler
^^^^^^^^^^^

.. versionadded:: 3.1

Lớp :class:`NullHandler`, nằm trong gói :mod:`logging` core, không thực hiện định dạng hay xuất dữ liệu. Về cơ bản, đây là một handler 'no-op' để các nhà phát triển thư viện sử dụng.

.. class:: NullHandler()

   Trả về một instance mới của lớp :class:`NullHandler`.

   .. method:: emit(record)

      Phương thức này không thực hiện thao tác nào.

   .. method:: handle(record)

      Phương thức này không thực hiện thao tác nào.

   .. method:: createLock()

      Phương thức này trả về ``None`` cho khóa, vì không có I/O bên dưới nào cần được tuần tự hóa quyền truy cập.


Xem :ref:`library-config` để biết thêm thông tin về cách sử dụng
:class:`NullHandler`.

.. _watched-file-handler:

WatchedFileHandler
^^^^^^^^^^^^^^^^^^

.. currentmodule:: logging.handlers

Lớp :class:`WatchedFileHandler`, nằm trong module :mod:`!logging.handlers`, là một :class:`FileHandler` theo dõi tệp mà nó ghi nhật ký vào. Nếu tệp thay đổi, tệp sẽ được đóng và mở lại bằng tên tệp.

Tệp có thể thay đổi do sử dụng các chương trình như *newsyslog* và *logrotate*, vốn thực hiện việc xoay vòng tệp nhật ký. Handler này, được thiết kế để sử dụng trên Unix/Linux, theo dõi tệp để xem tệp có thay đổi kể từ lần emit gần nhất hay không. (Tệp được xem là đã thay đổi nếu device hoặc inode của tệp đã thay đổi.) Nếu tệp đã thay đổi, stream tệp cũ sẽ được đóng và tệp được mở để tạo stream mới.

Handler này không phù hợp để sử dụng trên Windows, vì trên Windows, các tệp nhật ký đang mở không thể được di chuyển hoặc đổi tên - logging mở các tệp bằng exclusive lock - nên không cần handler như vậy. Ngoài ra, *ST_INO* không được hỗ trợ trên Windows; :func:`~os.stat` luôn trả về 0 cho giá trị này.


.. class:: WatchedFileHandler(filename, mode='a', encoding=None, delay=False, errors=None)

   Trả về một instance mới của lớp :class:`WatchedFileHandler`. Tệp được chỉ định sẽ được mở và dùng làm stream để ghi nhật ký. Nếu *mode* không được chỉ định, ``'a'`` sẽ được sử dụng. Nếu *encoding* không phải là ``None``, nó sẽ được dùng để mở tệp với encoding đó. Nếu *delay* là true, việc mở tệp sẽ được trì hoãn cho đến lần gọi đầu tiên đến :meth:`emit`. Theo mặc định, tệp sẽ tăng kích thước không giới hạn. Nếu *errors* được cung cấp, giá trị này sẽ xác định cách xử lý các lỗi encoding.

   .. versionchanged:: 3.6
      Ngoài các giá trị chuỗi, các đối tượng :class:`~pathlib.Path` cũng được chấp nhận cho đối số *filename*.

   .. versionchanged:: 3.9
      Tham số *errors* đã được thêm vào.

   .. method:: reopenIfNeeded()

      Kiểm tra xem tệp có thay đổi hay không. Nếu có, stream hiện tại sẽ được flush và đóng, sau đó tệp được mở lại, thường là bước chuẩn bị trước khi ghi record vào tệp.

      .. versionadded:: 3.6


   .. method:: emit(record)

      Ghi record vào tệp, nhưng trước tiên gọi :meth:`reopenIfNeeded` để mở lại tệp nếu tệp đã thay đổi.

.. _base-rotating-handler:

BaseRotatingHandler
^^^^^^^^^^^^^^^^^^^

Lớp :class:`BaseRotatingHandler`, nằm trong module :mod:`!logging.handlers`, là lớp cơ sở cho các file handler xoay vòng,
:class:`RotatingFileHandler` và :class:`TimedRotatingFileHandler`. Bạn không cần khởi tạo lớp này, nhưng lớp có các thuộc tính và phương thức mà bạn có thể cần ghi đè.

.. class:: BaseRotatingHandler(filename, mode, encoding=None, delay=False, errors=None)

   Các tham số giống như :class:`FileHandler`. Các thuộc tính gồm:

   .. attribute:: namer

      Nếu thuộc tính này được đặt thành một callable, phương thức :meth:`rotation_filename` sẽ ủy quyền cho callable này. Các tham số được truyền cho callable là những tham số được truyền cho :meth:`rotation_filename`.

      .. note:: Hàm namer được gọi khá nhiều lần trong quá trình rollover, vì vậy hàm này nên đơn giản và nhanh nhất có thể. Hàm cũng nên trả về cùng một kết quả mỗi lần nhận cùng một đầu vào; nếu không, hành vi rollover có thể không hoạt động như mong đợi.

         Cũng cần lưu ý rằng khi sử dụng namer, bạn phải cẩn thận để giữ lại một số thuộc tính nhất định trong tên tệp được dùng trong quá trình rotation. Ví dụ, :class:`RotatingFileHandler` yêu cầu có một tập hợp các tệp nhật ký với tên chứa các số nguyên liên tiếp để rotation hoạt động như mong đợi, còn :class:`TimedRotatingFileHandler` sẽ xóa các tệp nhật ký cũ (dựa trên tham số ``backupCount`` được truyền cho hàm khởi tạo của handler) bằng cách xác định các tệp cũ nhất cần xóa. Để thực hiện điều này, tên tệp phải có thể sắp xếp được bằng phần ngày/giờ của tên tệp, và namer cần tuân thủ yêu cầu này. (Nếu muốn sử dụng một namer không tuân thủ quy ước này, cần sử dụng namer đó trong một lớp con của :class:`TimedRotatingFileHandler` và ghi đè phương thức :meth:`~TimedRotatingFileHandler.getFilesToDelete` để phù hợp với quy ước đặt tên tùy chỉnh.)

      .. versionadded:: 3.3


   .. attribute:: BaseRotatingHandler.rotator

      Nếu thuộc tính này được đặt thành một callable, phương thức :meth:`rotate` sẽ ủy quyền cho callable này. Các tham số được truyền cho callable là những tham số được truyền cho :meth:`rotate`.

      .. versionadded:: 3.3

   .. method:: BaseRotatingHandler.rotation_filename(default_name)

      Thay đổi tên tệp của tệp nhật ký khi rotation.

      Cung cấp khả năng chỉ định tên tệp tùy chỉnh.

      Cài đặt mặc định gọi thuộc tính 'namer' của handler nếu thuộc tính này có thể gọi được, đồng thời truyền tên mặc định cho nó. Nếu thuộc tính này không thể gọi được (giá trị mặc định là ``None``), tên sẽ được trả về không thay đổi.

      :param default_name: Tên mặc định của tệp nhật ký.

      .. versionadded:: 3.3


   .. method:: BaseRotatingHandler.rotate(source, dest)

      Khi xoay vòng, xoay nhật ký hiện tại.

      Cài đặt mặc định gọi thuộc tính 'rotator' của handler nếu thuộc tính này có thể gọi được, đồng thời truyền các đối số source và dest cho nó. Nếu thuộc tính này không thể gọi được (giá trị mặc định là ``None``), source sẽ đơn giản được đổi tên thành đích.

      :param source: Tên tệp nguồn. Thông thường đây là tên tệp cơ sở, chẳng hạn như 'test.log'.
      :param dest:   Tên tệp đích. Thông thường đây là tên mà source được xoay vòng thành, chẳng hạn như 'test.log.1'.

      .. versionadded:: 3.3

Lý do các thuộc tính này tồn tại là để bạn không phải tạo lớp con - bạn có thể sử dụng cùng các đối tượng có thể gọi được cho các thực thể của :class:`RotatingFileHandler` và
:class:`TimedRotatingFileHandler`. Nếu callable namer hoặc rotator phát sinh ngoại lệ, ngoại lệ này sẽ được xử lý giống như mọi ngoại lệ khác trong một lần gọi :meth:`emit`, tức là thông qua phương thức :meth:`handleError` của handler.

Nếu cần thực hiện những thay đổi đáng kể hơn đối với quá trình rotation, bạn có thể override các phương thức này.

Xem :ref:`cookbook-rotator-namer` để biết ví dụ.


.. _rotating-file-handler:

RotatingFileHandler
^^^^^^^^^^^^^^^^^^^

Class :class:`RotatingFileHandler`, nằm trong module :mod:`!logging.handlers`, hỗ trợ rotation các tệp log trên đĩa.


.. class:: RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False, errors=None)

   Trả về một instance mới của class :class:`RotatingFileHandler`. Tệp được chỉ định sẽ được mở và dùng làm stream để ghi log. Nếu *mode* không được chỉ định, ``'a'`` sẽ được sử dụng. Nếu *encoding* không phải là ``None``, giá trị này sẽ được dùng để mở tệp với encoding đó. Nếu *delay* là true, việc mở tệp sẽ được trì hoãn cho đến lần gọi :meth:`emit` đầu tiên. Theo mặc định, tệp sẽ tăng kích thước không giới hạn. Nếu cung cấp *errors*, giá trị này sẽ xác định cách xử lý các lỗi encoding.

   Bạn có thể sử dụng các giá trị *maxBytes* và *backupCount* để cho phép tệp
   Thực hiện :dfn:`rollover` ở một kích thước định trước. Khi kích thước sắp vượt quá giới hạn, tệp sẽ được đóng và một tệp mới sẽ được âm thầm mở để ghi dữ liệu. Rollover xảy ra bất cứ khi nào tệp nhật ký hiện tại gần đạt độ dài *maxBytes*; nhưng nếu *maxBytes* hoặc *backupCount* bằng 0 thì rollover sẽ không bao giờ xảy ra, vì vậy thông thường bạn nên đặt *backupCount* ít nhất là 1 và đặt *maxBytes* khác 0. Khi *backupCount* khác 0, hệ thống sẽ lưu các tệp nhật ký cũ bằng cách nối thêm các phần mở rộng '.1', '.2', v.v. vào tên tệp. Ví dụ: với *backupCount* bằng 5 và tên tệp cơ sở là :file:`app.log`, bạn sẽ nhận được :file:`app.log`,
   :file:`app.log.1`, :file:`app.log.2`, tối đa là :file:`app.log.5`. Tệp đang được ghi luôn là :file:`app.log`. Khi tệp này đầy, nó sẽ được đóng và đổi tên thành :file:`app.log.1`, và nếu các tệp :file:`app.log.1`,
   :file:`app.log.2`, v.v. tồn tại thì chúng sẽ được đổi tên thành :file:`app.log.2`,
   :file:`app.log.3` tương ứng.

   .. versionchanged:: 3.6
      Ngoài các giá trị chuỗi, các đối tượng :class:`~pathlib.Path` cũng được chấp nhận cho đối số *filename*.

   .. versionchanged:: 3.9
      Tham số *errors* đã được thêm vào.

   .. method:: doRollover()

      Thực hiện rollover, như mô tả ở trên.


   .. method:: emit(record)

      Ghi bản ghi vào tệp, xử lý việc rollover như đã mô tả trước đó.

   .. method:: shouldRollover(record)

      Kiểm tra xem bản ghi được cung cấp có khiến tệp vượt quá giới hạn kích thước đã cấu hình hay không.

.. _timed-rotating-file-handler:

TimedRotatingFileHandler
^^^^^^^^^^^^^^^^^^^^^^^^

Lớp :class:`TimedRotatingFileHandler`, nằm trong
module :mod:`!logging.handlers`, hỗ trợ việc xoay vòng các tệp log trên đĩa theo những khoảng thời gian nhất định.


.. class:: TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None, errors=None)

   Trả về một instance mới của lớp :class:`TimedRotatingFileHandler`. Tệp được chỉ định sẽ được mở và dùng làm stream để ghi log. Khi xoay vòng, lớp này cũng đặt hậu tố tên tệp. Việc xoay vòng diễn ra dựa trên tích của *when* và *interval*.

   Bạn có thể sử dụng *when* để chỉ định loại *interval*. Danh sách các giá trị có thể có nằm dưới đây. Lưu ý rằng chúng không phân biệt chữ hoa chữ thường.

   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+
   | Giá trị        | Loại khoảng thời gian                                                                            | Nếu/cách *atTime* được sử dụng               |
   +================+==================================================================================================+==============================================+
   | ``'S'``        | Giây                                                                                             | Bỏ qua                                       |
   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+
   | ``'M'``        | Phút                                                                                             | Bỏ qua                                       |
   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+
   | ``'H'``        | Giờ                                                                                              | Bỏ qua                                       |
   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+
   | ``'D'``        | Ngày                                                                                             | Bỏ qua                                       |
   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+
   | ``'W0'-'W6'``  | Ngày trong tuần (0=Thứ Hai)                                                                      | Được dùng để tính thời điểm rollover ban đầu |
   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+
   | ``'midnight'`` | Thực hiện rollover vào nửa đêm nếu không chỉ định *atTime*, nếu không thì vào thời điểm *atTime* | Được dùng để tính thời điểm rollover ban đầu |
   +----------------+--------------------------------------------------------------------------------------------------+----------------------------------------------+

   Khi sử dụng rotation dựa trên ngày trong tuần, hãy chỉ định 'W0' cho thứ Hai, 'W1' cho thứ Ba, tiếp tục như vậy đến 'W6' cho Chủ nhật. Trong trường hợp này, giá trị được truyền cho *interval* không được sử dụng.

   Hệ thống sẽ lưu các tệp log cũ bằng cách thêm phần mở rộng vào tên tệp. Các phần mở rộng này dựa trên ngày và thời gian, sử dụng định dạng strftime ``%Y-%m-%d_%H-%M-%S`` hoặc một phần đầu của định dạng đó, tùy thuộc vào khoảng thời gian rollover.

   Khi lần đầu tính thời điểm rollover tiếp theo (khi handler được tạo), thời gian sửa đổi cuối cùng của tệp log hiện có hoặc thời gian hiện tại sẽ được dùng để tính thời điểm rotation tiếp theo.

   Nếu đối số *utc* là true, thời gian UTC sẽ được sử dụng; nếu không, thời gian cục bộ sẽ được sử dụng.

   Nếu *backupCount* khác không, tối đa *backupCount* tệp sẽ được giữ lại; nếu khi rollover xảy ra có thêm tệp được tạo, tệp cũ nhất sẽ bị xóa. Logic xóa sử dụng khoảng thời gian để xác định các tệp cần xóa, vì vậy việc thay đổi khoảng thời gian có thể khiến các tệp cũ vẫn còn lại.

   Nếu *delay* là true, việc mở tệp sẽ được trì hoãn cho đến lần gọi đầu tiên tới
   :meth:`emit`.

   Nếu *atTime* không phải là ``None``, thì giá trị này phải là một instance của ``datetime.time``, xác định thời điểm trong ngày diễn ra rollover, trong các trường hợp rollover được đặt để diễn ra "at midnight" hoặc "on a particular weekday". Lưu ý rằng trong các trường hợp này, giá trị *atTime* thực tế được dùng để tính thời điểm *initial* rollover, còn các lần rollover tiếp theo sẽ được tính bằng cách tính khoảng thời gian thông thường.

   Nếu *errors* được chỉ định, giá trị này sẽ được dùng để xác định cách xử lý các lỗi encoding.

   .. note:: Thời điểm rollover ban đầu được tính khi handler được khởi tạo. Thời điểm rollover tiếp theo chỉ được tính khi rollover xảy ra, và rollover chỉ xảy ra khi phát sinh output. Nếu không lưu ý điều này, bạn có thể sẽ thấy khó hiểu. Ví dụ, nếu đặt khoảng thời gian là "every minute", điều đó không có nghĩa là bạn sẽ luôn thấy các tệp log có thời gian (trong tên tệp) cách nhau một phút; nếu trong quá trình ứng dụng thực thi, output ghi log được tạo thường xuyên hơn một lần mỗi phút, *thì* bạn có thể thấy các tệp log có thời gian cách nhau một phút. Ngược lại, nếu các thông báo log chỉ được xuất ra mỗi năm phút một lần (chẳng hạn), thì thời gian của các tệp sẽ có những khoảng trống tương ứng với các phút không có output (và do đó không có rollover).

   .. versionchanged:: 3.4
      Đã thêm tham số *atTime*.

   .. versionchanged:: 3.6
      Ngoài các giá trị chuỗi, các đối tượng :class:`~pathlib.Path` cũng được chấp nhận cho đối số *filename*.

   .. versionchanged:: 3.9
      Đã thêm tham số *errors*.

   .. method:: doRollover()

      Thực hiện rollover như mô tả ở trên.

   .. method:: emit(record)

      Ghi bản ghi vào tệp, xử lý việc rollover như đã mô tả ở trên.

   .. method:: getFilesToDelete()

      Trả về danh sách tên tệp cần được xóa trong quá trình rollover. Đây là các đường dẫn tuyệt đối của những tệp nhật ký sao lưu cũ nhất do handler ghi.

   .. method:: shouldRollover(record)

      Kiểm tra xem đã đủ thời gian để thực hiện rollover hay chưa; nếu rồi, tính thời điểm rollover tiếp theo.

.. _socket-handler:

SocketHandler
^^^^^^^^^^^^^

Lớp :class:`SocketHandler`, nằm trong mô-đun :mod:`!logging.handlers`, gửi đầu ra ghi nhật ký đến một network socket. Lớp cơ sở sử dụng socket TCP.


.. class:: SocketHandler(host, port)

   Trả về một instance mới của lớp :class:`SocketHandler` để giao tiếp với một máy từ xa có địa chỉ được chỉ định bởi *host* và *port*.

   .. versionchanged:: 3.4
      Nếu ``port`` được chỉ định là ``None``, một Unix domain socket sẽ được tạo bằng giá trị trong ``host``; nếu không, một socket TCP sẽ được tạo.

   .. method:: close()

      Đóng socket.


   .. method:: emit()

      Pickle dictionary thuộc tính của record và ghi nó vào socket ở định dạng nhị phân. Nếu socket gặp lỗi, âm thầm loại bỏ packet. Nếu kết nối đã bị mất trước đó, thiết lập lại kết nối. Để unpickle record ở phía nhận thành một
      :class:`~logging.LogRecord`, hãy sử dụng hàm :func:`~logging.makeLogRecord`.


   .. method:: handleError()

      Xử lý lỗi xảy ra trong :meth:`emit`. Nguyên nhân có khả năng nhất là kết nối bị mất. Đóng socket để có thể thử lại ở event tiếp theo.


   .. method:: makeSocket()

      Đây là một factory method cho phép các lớp con xác định chính xác loại socket mà chúng muốn sử dụng. Triển khai mặc định tạo một TCP socket (:const:`socket.SOCK_STREAM`).


   .. method:: makePickle(record)

      Pickle dictionary thuộc tính của record ở định dạng nhị phân với tiền tố độ dài, rồi trả về dữ liệu đã sẵn sàng để truyền qua socket. Chi tiết của thao tác này tương đương với::

          data = pickle.dumps(record_attr_dict, 1)
          datalen = struct.pack('>L', len(data))
          return datalen + data

      Lưu ý rằng pickle không hoàn toàn an toàn. Nếu bạn lo ngại về bảo mật, bạn có thể muốn ghi đè method này để triển khai một cơ chế an toàn hơn. Ví dụ, bạn có thể ký pickle bằng HMAC rồi xác minh chúng ở phía nhận, hoặc tắt việc unpickle các đối tượng global ở phía nhận.


   .. method:: send(packet)

      Gửi một *gói tin* dạng chuỗi byte được pickle tới socket. Định dạng của chuỗi byte được gửi được mô tả trong tài liệu dành cho
      :meth:`~SocketHandler.makePickle`.

      Hàm này cho phép gửi một phần, điều có thể xảy ra khi mạng đang bận.


   .. method:: createSocket()

      Cố gắng tạo một socket; nếu thất bại, hàm sẽ sử dụng thuật toán back-off theo cấp số nhân. Khi thất bại lần đầu, handler sẽ loại bỏ thông báo mà nó đang cố gửi. Khi các thông báo tiếp theo được xử lý bởi cùng một instance, nó sẽ không thử kết nối cho đến khi một khoảng thời gian trôi qua. Các tham số mặc định được thiết lập sao cho độ trễ ban đầu là một giây; nếu sau khoảng thời gian đó vẫn không thể thiết lập kết nối, handler sẽ nhân đôi độ trễ sau mỗi lần thử, tối đa là 30 giây.

      Hành vi này được kiểm soát bởi các thuộc tính handler sau:

      * ``retryStart`` (độ trễ ban đầu, mặc định là 1.0 giây).
      * ``retryFactor`` (hệ số nhân, mặc định là 2.0).
      * ``retryMax`` (độ trễ tối đa, mặc định là 30.0 giây).

      Điều này có nghĩa là nếu listener từ xa khởi động *sau khi* handler đã được sử dụng, bạn có thể làm mất các message (vì handler thậm chí sẽ không thử kết nối cho đến khi hết thời gian trễ, mà chỉ âm thầm loại bỏ các message trong thời gian trễ).


.. _datagram-handler:

DatagramHandler
^^^^^^^^^^^^^^^

Lớp :class:`DatagramHandler`, nằm trong module :mod:`!logging.handlers`, kế thừa từ :class:`SocketHandler` để hỗ trợ gửi các message logging qua socket UDP.


.. class:: DatagramHandler(host, port)

   Trả về một instance mới của lớp :class:`DatagramHandler` để giao tiếp với một máy từ xa có địa chỉ được cung cấp bởi *host* và *port*.

   .. note:: Vì UDP không phải là giao thức streaming nên không có kết nối liên tục giữa một instance của handler này và *host*. Vì lý do này, khi sử dụng network socket, có thể phải thực hiện tra cứu DNS mỗi khi một event được ghi log, điều này có thể gây ra một độ trễ nhất định cho hệ thống. Nếu điều này ảnh hưởng đến bạn, bạn có thể tự tra cứu và khởi tạo handler này bằng địa chỉ IP đã tra cứu thay vì hostname.

   .. versionchanged:: 3.4
      Nếu ``port`` được chỉ định là ``None``, một Unix domain socket sẽ được tạo bằng giá trị trong ``host``; nếu không, một socket UDP sẽ được tạo.

   .. method:: emit()

      Chuyển dictionary thuộc tính của record thành pickle và ghi nó vào socket ở định dạng nhị phân. Nếu socket gặp lỗi, packet sẽ bị âm thầm loại bỏ. Để unpickle record ở đầu nhận thành một
      :class:`~logging.LogRecord`, hãy sử dụng hàm :func:`~logging.makeLogRecord`.


   .. method:: makeSocket()

      Phương thức factory của :class:`SocketHandler` được ghi đè tại đây để tạo một socket UDP (:const:`socket.SOCK_DGRAM`).


   .. method:: send(s)

      Gửi một chuỗi byte đã được pickle đến một socket. Định dạng của chuỗi byte được gửi được mô tả trong tài liệu dành cho :meth:`SocketHandler.makePickle`.


.. _syslog-handler:

SysLogHandler
^^^^^^^^^^^^^

Lớp :class:`SysLogHandler`, nằm trong module :mod:`!logging.handlers`, hỗ trợ gửi các thông báo logging đến syslog Unix từ xa hoặc cục bộ.


.. class:: SysLogHandler(address=('localhost', SYSLOG_UDP_PORT), facility=LOG_USER, socktype=socket.SOCK_DGRAM, timeout=None)

   Trả về một instance mới của lớp :class:`SysLogHandler`, dùng để giao tiếp với một máy Unix từ xa có địa chỉ được chỉ định bởi *address* dưới dạng tuple ``(host, port)``. Nếu không chỉ định *address*, ``('localhost', 514)`` sẽ được sử dụng. Địa chỉ này được dùng để mở một socket. Thay vì cung cấp tuple ``(host, port)``, bạn có thể cung cấp địa chỉ dưới dạng chuỗi, chẳng hạn như '/dev/log'. Trong trường hợp này, một Unix domain socket được dùng để gửi thông báo đến syslog. Nếu không chỉ định *facility*,
   :const:`LOG_USER` sẽ được sử dụng. Loại socket được mở phụ thuộc vào đối số *socktype*, mặc định là :const:`socket.SOCK_DGRAM` và do đó sẽ mở một socket UDP. Để mở một socket TCP (dùng với các syslog daemon mới hơn như rsyslog), hãy chỉ định giá trị :const:`socket.SOCK_STREAM`. Nếu chỉ định *timeout*, giá trị này sẽ đặt thời gian chờ (tính bằng giây) cho các thao tác trên socket. Điều này có thể giúp ngăn chương trình bị treo vô thời hạn nếu không thể truy cập máy chủ syslog. Theo mặc định, *timeout* là ``None``, nghĩa là không áp dụng thời gian chờ.



   Lưu ý rằng nếu máy chủ của bạn không lắng nghe trên cổng UDP 514,
   :class:`SysLogHandler` có thể dường như không hoạt động. Trong trường hợp đó, hãy kiểm tra địa chỉ bạn nên sử dụng cho domain socket - địa chỉ này phụ thuộc vào hệ thống. Ví dụ: trên Linux, địa chỉ này thường là '/dev/log', nhưng trên OS/X là '/var/run/syslog'. Bạn cần kiểm tra nền tảng của mình và sử dụng địa chỉ phù hợp (có thể bạn cần thực hiện việc kiểm tra này tại runtime nếu ứng dụng của bạn cần chạy trên nhiều nền tảng). Trên Windows, về cơ bản bạn phải sử dụng tùy chọn UDP.

   .. note:: Trên macOS 12.x (Monterey), Apple đã thay đổi cách hoạt động của syslog daemon - daemon này không còn lắng nghe trên domain socket. Do đó, bạn không thể mong đợi :class:`SysLogHandler` hoạt động trên hệ thống này.

      Xem :gh:`91070` để biết thêm thông tin.

   .. versionchanged:: 3.2
      *socktype* đã được thêm.

   .. versionchanged:: 3.14
      *timeout* đã được thêm.

   .. method:: close()

      Đóng socket tới máy chủ từ xa.

   .. method:: createSocket()

      Cố gắng tạo một socket và nếu đó không phải là datagram socket thì kết nối nó với đầu bên kia. Phương thức này được gọi trong quá trình khởi tạo handler, nhưng việc đầu bên kia chưa lắng nghe tại thời điểm này không được xem là lỗi - phương thức sẽ được gọi lại khi phát một event nếu tại thời điểm đó không có socket.

      .. versionadded:: 3.11

   .. method:: emit(record)

      Record được định dạng rồi gửi đến máy chủ syslog. Nếu có thông tin ngoại lệ, thông tin đó *không* được gửi đến máy chủ.

      .. versionchanged:: 3.2.1
         (Xem: :issue:`12168`.) Trong các phiên bản trước, thông báo được gửi đến các syslog daemon luôn được kết thúc bằng một byte NUL, vì các phiên bản daemon ban đầu yêu cầu thông báo kết thúc bằng NUL - mặc dù điều này không có trong đặc tả liên quan (:rfc:`5424`). Các phiên bản daemon gần đây hơn không yêu cầu byte NUL nhưng sẽ loại bỏ nó nếu có, còn các daemon mới hơn nữa (tuân thủ RFC 5424 chặt chẽ hơn) sẽ truyền byte NUL như một phần của thông báo.

         Để dễ xử lý các thông báo syslog hơn trước những hành vi khác nhau của các daemon này, việc nối thêm byte NUL đã được cấu hình hóa thông qua một thuộc tính cấp lớp, ``append_nul``. Thuộc tính này mặc định là ``True`` (duy trì hành vi hiện có) nhưng có thể được đặt thành ``False`` trên một instance ``SysLogHandler`` để instance đó *không* nối thêm ký tự kết thúc NUL.

      .. versionchanged:: 3.3
         (Xem: :issue:`12419`.) Trong các phiên bản trước, không có cơ chế để thêm tiền tố "ident" hoặc "tag" nhằm xác định nguồn của thông báo. Hiện có thể chỉ định tiền tố này bằng một thuộc tính cấp lớp, mặc định là ``""`` để duy trì hành vi hiện có, nhưng có thể ghi đè trên một instance ``SysLogHandler`` để instance đó thêm ident vào trước mọi thông báo được xử lý. Lưu ý rằng ident được cung cấp phải là text, không phải bytes, và được thêm vào trước thông báo đúng nguyên trạng.

   .. method:: encodePriority(facility, priority)

      Mã hóa facility và priority thành một số nguyên. Bạn có thể truyền vào chuỗi hoặc số nguyên - nếu truyền chuỗi, các từ điển ánh xạ nội bộ sẽ được sử dụng để chuyển chúng thành số nguyên.

      Các giá trị ``LOG_`` mang tính biểu tượng được định nghĩa trong :class:`SysLogHandler` và tương ứng với các giá trị được định nghĩa trong tệp header ``sys/syslog.h``.

      **Mức độ ưu tiên**

      +----------------------------+---------------------+
      | Tên (chuỗi)                | Giá trị tượng trưng |
      +============================+=====================+
      | ``alert``                  | LOG_ALERT           |
      +----------------------------+---------------------+
      | ``crit`` hoặc ``critical`` | LOG_CRIT            |
      +----------------------------+---------------------+
      | ``debug``                  | LOG_DEBUG           |
      +----------------------------+---------------------+
      | ``emerg`` hoặc ``panic``   | LOG_EMERG           |
      +----------------------------+---------------------+
      | ``err`` hoặc ``error``     | LOG_ERR             |
      +----------------------------+---------------------+
      | ``info``                   | LOG_INFO            |
      +----------------------------+---------------------+
      | ``notice``                 | LOG_NOTICE          |
      +----------------------------+---------------------+
      | ``warn`` hoặc ``warning``  | LOG_WARNING         |
      +----------------------------+---------------------+

      **Cơ sở**

      +--------------+---------------------+
      | Tên (chuỗi)  | Giá trị tượng trưng |
      +==============+=====================+
      | ``auth``     | LOG_AUTH            |
      +--------------+---------------------+
      | ``authpriv`` | LOG_AUTHPRIV        |
      +--------------+---------------------+
      | ``cron``     | LOG_CRON            |
      +--------------+---------------------+
      | ``daemon``   | LOG_DAEMON          |
      +--------------+---------------------+
      | ``ftp``      | LOG_FTP             |
      +--------------+---------------------+
      | ``kern``     | LOG_KERN            |
      +--------------+---------------------+
      | ``lpr``      | LOG_LPR             |
      +--------------+---------------------+
      | ``mail``     | LOG_MAIL            |
      +--------------+---------------------+
      | ``news``     | LOG_NEWS            |
      +--------------+---------------------+
      | ``syslog``   | LOG_SYSLOG          |
      +--------------+---------------------+
      | ``user``     | LOG_USER            |
      +--------------+---------------------+
      | ``uucp``     | LOG_UUCP            |
      +--------------+---------------------+
      | ``local0``   | LOG_LOCAL0          |
      +--------------+---------------------+
      | ``local1``   | LOG_LOCAL1          |
      +--------------+---------------------+
      | ``local2``   | LOG_LOCAL2          |
      +--------------+---------------------+
      | ``local3``   | LOG_LOCAL3          |
      +--------------+---------------------+
      | ``local4``   | LOG_LOCAL4          |
      +--------------+---------------------+
      | ``local5``   | LOG_LOCAL5          |
      +--------------+---------------------+
      | ``local6``   | LOG_LOCAL6          |
      +--------------+---------------------+
      | ``local7``   | LOG_LOCAL7          |
      +--------------+---------------------+

   .. method:: mapPriority(levelname)

      Ánh xạ tên của một logging level với tên độ ưu tiên của syslog. Bạn có thể cần ghi đè ánh xạ này nếu sử dụng các level tùy chỉnh hoặc nếu thuật toán mặc định không phù hợp với nhu cầu của bạn. Thuật toán mặc định ánh xạ ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR`` và ``CRITICAL`` với các tên syslog tương ứng, còn tất cả các tên level khác với 'warning'.

.. _nt-eventlog-handler:

NTEventLogHandler
^^^^^^^^^^^^^^^^^

Lớp :class:`NTEventLogHandler`, nằm trong mô-đun :mod:`!logging.handlers`, hỗ trợ gửi các thông báo logging đến event log cục bộ của Windows NT, Windows 2000 hoặc Windows XP. Trước khi có thể sử dụng lớp này, bạn cần cài đặt Win32 extensions for Python của Mark Hammond.


.. class:: NTEventLogHandler(appname, dllname=None, logtype='Application')

   Trả về một instance mới của lớp :class:`NTEventLogHandler`. *appname* được dùng để xác định tên ứng dụng như tên đó xuất hiện trong event log. Một registry entry phù hợp sẽ được tạo bằng tên này. *dllname* phải cung cấp pathname đầy đủ của một tệp .dll hoặc .exe chứa các định nghĩa thông báo để lưu trong log (nếu không được chỉ định, ``'win32service.pyd'`` được sử dụng
   - thành phần này được cài đặt cùng với các phần mở rộng Win32 và chứa một số định nghĩa cơ bản
   các định nghĩa thông báo giữ chỗ. Lưu ý rằng việc sử dụng các giá trị giữ chỗ này sẽ khiến nhật ký sự kiện lớn, vì toàn bộ nguồn thông báo được lưu trong nhật ký. Nếu muốn nhật ký nhỏ gọn hơn, bạn phải truyền vào tên của tệp .dll hoặc .exe riêng chứa các định nghĩa thông báo mà bạn muốn sử dụng trong nhật ký sự kiện). *logtype* là một trong ``'Application'``, ``'System'`` hoặc ``'Security'``, và mặc định là ``'Application'``.


   .. method:: close()

      Tại thời điểm này, bạn có thể xóa tên ứng dụng khỏi registry với tư cách là nguồn của các mục nhật ký sự kiện. Tuy nhiên, nếu làm vậy, bạn sẽ không thể xem các sự kiện như dự định trong Event Log Viewer - trình này cần truy cập registry để lấy tên tệp .dll. Phiên bản hiện tại không thực hiện việc này.


   .. method:: emit(record)

      Xác định message ID, event category và event type, sau đó ghi thông báo vào NT event log.


   .. method:: getEventCategory(record)

      Trả về event category của bản ghi. Ghi đè phương thức này nếu bạn muốn chỉ định các category của riêng mình. Phiên bản này trả về 0.


   .. method:: getEventType(record)

      Trả về event type của bản ghi. Ghi đè phương thức này nếu bạn muốn chỉ định các type của riêng mình. Phiên bản này thực hiện ánh xạ bằng thuộc tính typemap của handler, được thiết lập trong :meth:`__init__` thành một dictionary chứa các ánh xạ cho :const:`DEBUG`, :const:`INFO`,
      :const:`WARNING`, :const:`ERROR` và :const:`CRITICAL`. Nếu bạn sử dụng các level riêng, bạn sẽ cần ghi đè phương thức này hoặc đặt một dictionary phù hợp trong thuộc tính *typemap* của handler.


   .. method:: getMessageID(record)

      Trả về ID thông báo của bản ghi. Nếu bạn đang sử dụng các thông báo của riêng mình, bạn có thể thực hiện việc này bằng cách truyền *msg* cho logger dưới dạng ID thay vì chuỗi định dạng. Sau đó, tại đây, bạn có thể sử dụng tra cứu từ điển để lấy ID thông báo. Phiên bản này trả về 1, là ID thông báo cơ sở trong :file:`win32service.pyd`.

.. _smtp-handler:

SMTPHandler
^^^^^^^^^^^

Lớp :class:`SMTPHandler`, nằm trong mô-đun :mod:`!logging.handlers`, hỗ trợ gửi các thông báo logging đến một địa chỉ email thông qua SMTP.


.. class:: SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, timeout=1.0)

   Trả về một instance mới của lớp :class:`SMTPHandler`. Instance này được khởi tạo với địa chỉ người gửi, địa chỉ người nhận và dòng tiêu đề của email. *toaddrs* phải là một danh sách các chuỗi. Để chỉ định một cổng SMTP không tiêu chuẩn, hãy sử dụng định dạng tuple (host, port) cho đối số *mailhost*. Nếu bạn sử dụng một chuỗi, cổng SMTP tiêu chuẩn sẽ được sử dụng. Nếu máy chủ SMTP yêu cầu xác thực, bạn có thể chỉ định một tuple (username, password) cho đối số *credentials*.

   Để chỉ định việc sử dụng một giao thức bảo mật (TLS), hãy truyền một tuple vào đối số *secure*. Đối số này chỉ được sử dụng khi cung cấp thông tin xác thực. Tuple phải là một tuple rỗng, hoặc một tuple một giá trị chứa tên của tệp khóa, hoặc một tuple hai giá trị chứa tên của tệp khóa và tệp chứng chỉ. (Tuple này được truyền cho
   phương thức :meth:`smtplib.SMTP.starttls`.)

   Có thể chỉ định thời gian chờ khi giao tiếp với máy chủ SMTP bằng đối số *timeout*.

   .. versionchanged:: 3.3
      Đã thêm tham số *timeout*.

   .. method:: emit(record)

      Định dạng bản ghi và gửi bản ghi đó đến các địa chỉ nhận được chỉ định.


   .. method:: getSubject(record)

      Nếu bạn muốn chỉ định dòng tiêu đề phụ thuộc vào bản ghi, hãy ghi đè phương thức này.

.. _memory-handler:

MemoryHandler
^^^^^^^^^^^^^

Lớp :class:`MemoryHandler`, nằm trong mô-đun :mod:`!logging.handlers`, hỗ trợ việc đệm các bản ghi nhật ký trong bộ nhớ và định kỳ chuyển chúng đến một
bộ xử lý :dfn:`target`. Việc chuyển xảy ra bất cứ khi nào bộ đệm đầy hoặc khi phát hiện một sự kiện có mức độ nghiêm trọng nhất định trở lên.

:class:`MemoryHandler` là một lớp con của
:class:`BufferingHandler`, là một lớp trừu tượng. Lớp này đệm các bản ghi logging trong bộ nhớ. Mỗi khi một bản ghi được thêm vào bộ đệm, một kiểm tra sẽ được thực hiện bằng cách gọi :meth:`shouldFlush` để xác định xem có nên flush bộ đệm hay không. Nếu nên flush, :meth:`flush` sẽ thực hiện việc flush.


.. class:: BufferingHandler(capacity)

   Khởi tạo handler với một bộ đệm có dung lượng được chỉ định. Ở đây, *capacity* có nghĩa là số bản ghi logging được đệm.


   .. method:: emit(record)

      Thêm bản ghi vào bộ đệm. Nếu :meth:`shouldFlush` trả về true, hãy gọi :meth:`flush` để xử lý bộ đệm.


   .. method:: flush()

      Đối với một instance :class:`BufferingHandler`, việc flush có nghĩa là đặt bộ đệm thành một danh sách rỗng. Có thể ghi đè phương thức này để triển khai hành vi flush hữu ích hơn.


   .. method:: shouldFlush(record)

      Trả về ``True`` nếu bộ đệm đã đạt dung lượng tối đa. Có thể ghi đè phương thức này để triển khai các chiến lược flush tùy chỉnh.


.. class:: MemoryHandler(capacity, flushLevel=ERROR, target=None, flushOnClose=True)

   Trả về một instance mới của lớp :class:`MemoryHandler`. Instance được khởi tạo với kích thước bộ đệm là *capacity* (số bản ghi được đệm). Nếu không chỉ định *flushLevel*, :const:`ERROR` sẽ được sử dụng. Nếu không chỉ định *target*, cần đặt target bằng :meth:`setTarget` trước khi handler này có thể thực hiện bất kỳ tác vụ hữu ích nào. Nếu *flushOnClose* được chỉ định là ``False``, bộ đệm sẽ *not* được flush khi handler bị đóng. Nếu không được chỉ định hoặc được chỉ định là ``True``, hành vi flush bộ đệm trước đây sẽ xảy ra khi handler bị đóng.

   .. versionchanged:: 3.6
      Tham số *flushOnClose* đã được thêm vào.


   .. method:: close()

      Gọi :meth:`flush`, đặt target thành ``None`` và xóa buffer.


   .. method:: flush()

      Đối với một instance :class:`MemoryHandler`, việc flush chỉ đơn giản là gửi các bản ghi đã được lưu trong buffer đến target, nếu có. Buffer cũng được xóa khi các bản ghi được lưu trong buffer được gửi đến target. Hãy override nếu bạn muốn hành vi khác.


   .. method:: setTarget(target)

      Đặt target handler cho handler này.


   .. method:: shouldFlush(record)

      Kiểm tra xem buffer đã đầy hay có một record ở mức *flushLevel* trở lên.


.. _http-handler:

HTTPHandler
^^^^^^^^^^^

Lớp :class:`HTTPHandler`, nằm trong module :mod:`!logging.handlers`, hỗ trợ gửi các thông báo logging đến một web server bằng semantics ``GET`` hoặc ``POST``.


.. class:: HTTPHandler(host, url, method='GET', secure=False, credentials=None, context=None)

   Trả về một instance mới của lớp :class:`HTTPHandler`. *host* có thể có dạng ``host:port`` nếu bạn cần sử dụng một số cổng cụ thể. Nếu không chỉ định *method*, ``GET`` sẽ được sử dụng. Nếu *secure* là true, kết nối HTTPS sẽ được sử dụng. Tham số *context* có thể được đặt thành một
   instance :class:`ssl.SSLContext` để cấu hình các thiết lập SSL được sử dụng cho kết nối HTTPS. Nếu chỉ định *credentials*, giá trị này phải là một tuple 2 phần tử gồm userid và password, được đặt trong HTTP header 'Authorization' bằng phương thức xác thực Basic. Nếu chỉ định credentials, bạn cũng nên chỉ định secure=True để userid và password không được truyền dưới dạng văn bản thuần túy qua mạng.

   .. versionchanged:: 3.5
      Tham số *context* đã được thêm vào.

   .. method:: mapLogRecord(record)

      Cung cấp một dictionary dựa trên ``record``, được mã hóa URL và gửi đến web server. Phần triển khai mặc định chỉ trả về ``record.__dict__``. Có thể ghi đè method này nếu chẳng hạn chỉ một tập con của :class:`~logging.LogRecord` cần được gửi đến web server, hoặc nếu cần tùy chỉnh cụ thể hơn nội dung được gửi đến server.

   .. method:: emit(record)

      Gửi record đến web server dưới dạng một dictionary được mã hóa URL. Phần
      method :meth:`mapLogRecord` được sử dụng để chuyển record thành dictionary cần gửi.

   .. note:: Vì việc chuẩn bị một record để gửi đến web server không giống với một thao tác formatting thông thường, việc sử dụng
      :meth:`~logging.Handler.setFormatter` to specify a
      :class:`~logging.Formatter` for a :class:`HTTPHandler` has no effect.
      Thay vì gọi :meth:`~logging.Handler.format`, handler này gọi
      :meth:`mapLogRecord` và sau đó :func:`urllib.parse.urlencode` để mã hóa dictionary ở dạng phù hợp để gửi đến web server.


.. _queue-handler:


QueueHandler
^^^^^^^^^^^^

.. versionadded:: 3.2

Lớp :class:`QueueHandler`, nằm trong mô-đun :mod:`!logging.handlers`, hỗ trợ gửi các thông báo logging đến một queue, chẳng hạn như các queue được triển khai trong
mô-đun :mod:`queue` hoặc :mod:`multiprocessing`.

Cùng với lớp :class:`QueueListener`, :class:`QueueHandler` có thể được sử dụng để cho phép các handler thực hiện công việc của chúng trên một thread riêng với thread thực hiện việc logging. Điều này rất quan trọng trong các ứng dụng web và cả những ứng dụng dịch vụ khác, nơi các thread phục vụ client cần phản hồi nhanh nhất có thể, trong khi mọi thao tác có khả năng chậm (chẳng hạn như gửi email qua
:class:`SMTPHandler`) được thực hiện trên một thread riêng.

.. class:: QueueHandler(queue)

   Trả về một instance mới của lớp :class:`QueueHandler`. Instance này được khởi tạo với queue dùng để gửi các thông báo. *queue* có thể là bất kỳ đối tượng nào có chức năng tương tự queue; nó được :meth:`enqueue` sử dụng nguyên trạng, và phương thức này cần biết cách gửi các thông báo đến queue đó. Queue không *bắt buộc* phải có API theo dõi tác vụ, nghĩa là bạn có thể sử dụng
   các instance của :class:`~queue.SimpleQueue` dành cho *queue*.

   .. note:: Nếu bạn đang sử dụng :mod:`multiprocessing`, bạn nên tránh sử dụng
      :class:`~queue.SimpleQueue` and instead use :class:`multiprocessing.Queue`.

   .. warning::

      Module :mod:`multiprocessing` sử dụng một logger nội bộ được tạo và truy cập thông qua :meth:`~multiprocessing.get_logger`.
      :class:`multiprocessing.Queue` sẽ ghi các thông báo ở cấp độ ``DEBUG`` khi các mục được đưa vào queue. Nếu các thông báo log đó được xử lý bởi một
      :class:`QueueHandler` sử dụng cùng instance :class:`multiprocessing.Queue`, điều này sẽ gây ra deadlock hoặc đệ quy vô hạn.

   .. method:: emit(record)

      Đưa kết quả của việc chuẩn bị LogRecord vào queue. Nếu xảy ra ngoại lệ (ví dụ: do một bounded queue đã đầy),
      phương thức :meth:`~logging.Handler.handleError` được gọi để xử lý lỗi. Điều này có thể khiến bản ghi bị loại bỏ mà không có thông báo (nếu
      :data:`logging.raiseExceptions` là ``False``) hoặc một thông báo được in ra ``sys.stderr`` (nếu :data:`logging.raiseExceptions` là ``True``).

   .. method:: prepare(record)

      Chuẩn bị một record để đưa vào hàng đợi. Đối tượng được phương thức này trả về sẽ được đưa vào hàng đợi.

      Phần triển khai cơ sở định dạng record để gộp thông báo, các đối số, thông tin ngoại lệ và stack nếu có. Phần này cũng loại bỏ các mục không thể pickle khỏi record ngay tại chỗ. Cụ thể, phần này ghi đè các thuộc tính :attr:`msg` và :attr:`message` của record bằng thông báo đã được gộp (nhận được bằng cách gọi phương thức :meth:`format` của handler), đồng thời đặt các thuộc tính :attr:`args`, :attr:`exc_info` và :attr:`exc_text` thành ``None``.

      Bạn có thể muốn ghi đè phương thức này nếu muốn chuyển record thành dict hoặc chuỗi JSON, hoặc gửi một bản sao đã sửa đổi của record trong khi vẫn giữ nguyên bản gốc.

      .. note:: Phần triển khai cơ sở định dạng thông báo cùng các đối số, đặt các thuộc tính ``message`` và ``msg`` thành thông báo đã được định dạng, đồng thời đặt các thuộc tính ``args`` và ``exc_text`` thành ``None`` để cho phép pickle và ngăn các lần định dạng tiếp theo. Điều này có nghĩa là handler ở phía :class:`QueueListener` sẽ không có thông tin để thực hiện định dạng tùy chỉnh, chẳng hạn như định dạng ngoại lệ. Bạn có thể muốn phân lớp ``QueueHandler`` và ghi đè phương thức này, chẳng hạn để tránh đặt ``exc_text`` thành ``None``. Lưu ý rằng các thay đổi đối với ``message`` / ``msg`` / ``args`` liên quan đến việc bảo đảm record có thể pickle, và bạn có thể hoặc không thể tránh việc đó tùy thuộc vào việc ``args`` của bạn có thể pickle hay không. (Lưu ý rằng bạn có thể phải xem xét không chỉ code của mình mà cả code trong bất kỳ thư viện nào bạn sử dụng.)

   .. method:: enqueue(record)

      Đưa record vào hàng đợi bằng ``put_nowait()``; bạn có thể muốn ghi đè phương thức này nếu muốn sử dụng hành vi blocking, timeout hoặc một triển khai hàng đợi tùy chỉnh.

   .. attribute:: listener

      Khi được tạo thông qua cấu hình bằng :func:`~logging.config.dictConfig`, thuộc tính này sẽ chứa một instance :class:`QueueListener` để sử dụng với handler này. Nếu không, thuộc tính sẽ là ``None``.

      .. versionadded:: 3.12

.. _queue-listener:

QueueListener
^^^^^^^^^^^^^

.. versionadded:: 3.2

Lớp :class:`QueueListener`, nằm trong mô-đun :mod:`!logging.handlers`, hỗ trợ nhận các thông điệp ghi nhật ký từ một hàng đợi, chẳng hạn như những hàng đợi được triển khai trong các mô-đun :mod:`queue` hoặc :mod:`multiprocessing`. Các thông điệp được nhận từ một hàng đợi trong một thread nội bộ và được chuyển, trên cùng thread đó, đến một hoặc nhiều handler để xử lý. Trong khi
:class:`QueueListener` bản thân không phải là một handler, lớp này được ghi lại ở đây vì nó hoạt động kết hợp chặt chẽ với :class:`QueueHandler`.

Cùng với lớp :class:`QueueHandler`, :class:`QueueListener` có thể được dùng để cho phép các handler thực hiện công việc của chúng trên một thread riêng với thread thực hiện việc ghi nhật ký. Điều này rất quan trọng trong các ứng dụng web cũng như các ứng dụng dịch vụ khác, nơi các thread phục vụ client cần phản hồi nhanh nhất có thể, còn mọi thao tác có khả năng mất nhiều thời gian (chẳng hạn như gửi email qua
:class:`SMTPHandler`) được thực hiện trên một thread riêng.

.. class:: QueueListener(queue, *handlers, respect_handler_level=False)

   Trả về một instance mới của lớp :class:`QueueListener`. Instance này được khởi tạo với queue để gửi message tới đó và một danh sách các handler sẽ xử lý những entry được đặt vào queue. Queue có thể là bất kỳ đối tượng dạng queue nào; queue được truyền nguyên trạng vào phương thức :meth:`dequeue`, phương thức này cần biết cách lấy message từ đó. Queue không *bắt buộc* phải có task tracking API (dù API này được sử dụng nếu có), nghĩa là bạn có thể sử dụng các :class:`~queue.SimpleQueue` instance cho *queue*.

   .. note:: Nếu bạn đang sử dụng :mod:`multiprocessing`, bạn nên tránh sử dụng
      :class:`~queue.SimpleQueue` and instead use :class:`multiprocessing.Queue`.

   Nếu ``respect_handler_level`` là ``True``, level của handler sẽ được tôn trọng (so sánh với level của message) khi quyết định có chuyển message đến handler đó hay không; nếu không, hành vi sẽ giống như trong các phiên bản Python trước đây - luôn chuyển từng message đến từng handler.

   .. versionchanged:: 3.5
      Đối số ``respect_handler_level`` đã được thêm vào.

   .. versionchanged:: 3.14
      :class:`QueueListener` can now be used as a context manager via
      :keyword:`with`. When entering the context, the listener is started. When
      khi thoát khỏi context, listener sẽ được dừng.
      :meth:`~contextmanager.__enter__` trả về
      đối tượng :class:`QueueListener`.

   .. method:: dequeue(block)

      Lấy một record khỏi queue và trả về record đó, có thể chặn tùy chọn.

      Phần triển khai cơ sở sử dụng ``get()``. Bạn có thể muốn ghi đè phương thức này nếu muốn sử dụng timeout hoặc làm việc với các triển khai queue tùy chỉnh.

   .. method:: prepare(record)

      Chuẩn bị một bản ghi để xử lý.

      Triển khai này chỉ trả về bản ghi được truyền vào. Bạn có thể muốn ghi đè phương thức này nếu cần thực hiện việc marshalling hoặc thao tác tùy chỉnh trên bản ghi trước khi truyền bản ghi đó cho các handler.

   .. method:: handle(record)

      Xử lý một bản ghi.

      Phương thức này chỉ lặp qua các handler và cung cấp cho chúng bản ghi để xử lý. Đối tượng thực tế được truyền cho các handler là đối tượng được trả về từ :meth:`prepare`.

   .. method:: start()

      Khởi động listener.

      Phương thức này khởi động một background thread để giám sát queue và xử lý các LogRecords.

      .. versionchanged:: 3.14
         Phát sinh :exc:`RuntimeError` nếu được gọi khi listener đã đang chạy.

   .. method:: stop()

      Dừng listener.

      Lệnh này yêu cầu thread kết thúc, sau đó chờ thread thực hiện xong. Lưu ý rằng nếu bạn không gọi lệnh này trước khi ứng dụng thoát, vẫn có thể còn một số bản ghi trong queue và chúng sẽ không được xử lý.

   .. method:: enqueue_sentinel()

      Ghi một sentinel vào queue để yêu cầu listener thoát. Cách triển khai này sử dụng ``put_nowait()``. Bạn có thể muốn ghi đè phương thức này nếu muốn sử dụng timeout hoặc làm việc với các triển khai queue tùy chỉnh.

      .. versionadded:: 3.3


.. seealso::

   Mô-đun :mod:`logging`
      Tài liệu tham khảo API cho mô-đun logging.

   Mô-đun :mod:`logging.config`
      API cấu hình cho mô-đun logging.


