:mod:`!logging.config` --- Cấu hình logging
===========================================

.. module:: logging.config
   :synopsis: Cấu hình module logging.

.. moduleauthor:: Vinay Sajip <vinay_sajip@red-dove.com>
.. sectionauthor:: Vinay Sajip <vinay_sajip@red-dove.com>

**Mã nguồn:** :source:`Lib/logging/config.py`

.. sidebar:: Quan trọng

   Trang này chỉ chứa thông tin tham khảo. Để xem hướng dẫn, vui lòng xem

   * :ref:`Hướng dẫn cơ bản <logging-basic-tutorial>`
   * :ref:`Hướng dẫn nâng cao <logging-advanced-tutorial>`
   * :ref:`Sổ tay Logging <logging-cookbook>`

--------------

Phần này mô tả API để cấu hình module logging.

.. _logging-config-api:

Các hàm cấu hình
^^^^^^^^^^^^^^^^

Các hàm sau đây cấu hình module logging. Chúng nằm trong
:mod:`!logging.config` module. Việc sử dụng chúng là tùy chọn --- bạn có thể cấu hình module logging bằng các hàm này hoặc bằng cách gọi main API (được định nghĩa ngay trong :mod:`logging`) và định nghĩa các handler được khai báo trong
:mod:`logging` hoặc :mod:`logging.handlers`.

.. function:: dictConfig(config)

   Lấy cấu hình logging từ một dictionary. Nội dung của dictionary này được mô tả trong :ref:`logging-config-dictschema` bên dưới.

   Nếu gặp lỗi trong quá trình cấu hình, hàm này sẽ ném ra :exc:`ValueError`, :exc:`TypeError`, :exc:`AttributeError` hoặc :exc:`ImportError` cùng với thông báo mô tả phù hợp. Sau đây là danh sách (có thể chưa đầy đủ) các điều kiện sẽ gây ra lỗi:

   * Một ``level`` không phải là chuỗi hoặc là chuỗi không tương ứng với một logging level thực tế.
   * Một giá trị ``propagate`` không phải là boolean.
   * Một id không có destination tương ứng.
   * Tìm thấy handler id không tồn tại trong một incremental call.
   * Tên logger không hợp lệ.
   * Không thể phân giải thành một đối tượng nội bộ hoặc bên ngoài.

   Việc phân tích cú pháp được thực hiện bởi lớp :class:`DictConfigurator`, hàm khởi tạo của lớp nhận từ điển dùng cho cấu hình và có phương thức :meth:`configure`. Mô-đun :mod:`!logging.config` có thuộc tính có thể gọi :attr:`dictConfigClass`, ban đầu được đặt thành :class:`DictConfigurator`. Bạn có thể thay thế giá trị của :attr:`dictConfigClass` bằng một triển khai phù hợp của riêng mình.

   :func:`dictConfig` gọi :attr:`dictConfigClass` với từ điển được chỉ định, sau đó gọi phương thức :meth:`configure` trên đối tượng được trả về để áp dụng cấu hình::

         def dictConfig(config):
             dictConfigClass(config).configure()

   Ví dụ, một lớp con của :class:`DictConfigurator` có thể gọi ``DictConfigurator.__init__()`` trong :meth:`__init__` của chính nó, sau đó thiết lập các tiền tố tùy chỉnh có thể sử dụng trong lần gọi tiếp theo
   :meth:`configure`. :attr:`dictConfigClass` sẽ được liên kết với lớp con mới này, sau đó :func:`dictConfig` có thể được gọi chính xác như trong trạng thái mặc định, chưa tùy chỉnh.

   .. versionadded:: 3.2

.. function:: fileConfig(fname, defaults=None, disable_existing_loggers=True, encoding=None)

   Đọc cấu hình logging từ một tệp :mod:`configparser`\-format. Định dạng của tệp phải được mô tả trong
   :ref:`logging-config-fileformat`. Hàm này có thể được gọi nhiều lần từ một ứng dụng, cho phép người dùng cuối chọn giữa nhiều cấu hình được chuẩn bị sẵn (nếu developer cung cấp cơ chế để hiển thị các lựa chọn và tải cấu hình đã chọn).

   Hàm sẽ phát sinh :exc:`FileNotFoundError` nếu tệp không tồn tại và :exc:`RuntimeError` nếu tệp không hợp lệ hoặc rỗng.

   :param fname: Một tên tệp, hoặc một đối tượng giống tệp, hoặc một thực thể dẫn xuất từ :class:`~configparser.RawConfigParser`. Nếu một
                 thực thể dẫn xuất từ :class:`!RawConfigParser` được truyền vào, thực thể đó được sử dụng nguyên trạng. Nếu không, một :class:`~configparser.ConfigParser` được khởi tạo và đọc cấu hình từ đối tượng được truyền vào ``fname``. Nếu đối tượng đó có phương thức :meth:`readline`, đối tượng đó được xem là một đối tượng giống tệp và được đọc bằng
                 :meth:`~configparser.ConfigParser.read_file`; nếu không, đối tượng đó được xem là một tên tệp và được truyền cho
                 :meth:`~configparser.ConfigParser.read`.


   :param defaults: Có thể chỉ định các giá trị mặc định được truyền cho :class:`!ConfigParser` trong đối số này.

   :param disable_existing_loggers: Nếu được chỉ định là ``False``, các logger đang tồn tại khi lệnh gọi này được thực hiện sẽ tiếp tục được bật. Mặc định là ``True`` vì điều này bật hành vi cũ theo cách tương thích ngược. Hành vi này là vô hiệu hóa mọi logger hiện có không phải root, trừ khi chúng hoặc các logger tổ tiên của chúng được nêu rõ trong cấu hình logging.

   :param encoding: Mã hóa được sử dụng để mở tệp khi *fname* là tên tệp.

   .. versionchanged:: 3.4
      Một thực thể của lớp con của :class:`~configparser.RawConfigParser` hiện được chấp nhận làm giá trị cho ``fname``. Điều này hỗ trợ:

      * Sử dụng tệp cấu hình, trong đó cấu hình logging chỉ là một phần của cấu hình tổng thể của ứng dụng.
      * Sử dụng cấu hình được đọc từ một tệp, sau đó được ứng dụng sử dụng sửa đổi (ví dụ: dựa trên các tham số dòng lệnh hoặc các khía cạnh khác của môi trường runtime) trước khi truyền cho ``fileConfig``.

    .. versionchanged:: 3.10
       Đã thêm tham số *encoding*.

    .. versionchanged:: 3.12
       Một exception sẽ được ném ra nếu tệp được cung cấp không tồn tại, không hợp lệ hoặc rỗng.

.. function:: listen(port=DEFAULT_LOGGING_CONFIG_PORT, verify=None)

   Khởi động một socket server trên port được chỉ định và lắng nghe các cấu hình mới. Nếu không chỉ định port, giá trị mặc định của module
   :const:`DEFAULT_LOGGING_CONFIG_PORT` sẽ được sử dụng. Các cấu hình logging sẽ được gửi dưới dạng tệp phù hợp để :func:`dictConfig` hoặc
   :func:`fileConfig`. Trả về một instance :class:`~threading.Thread`, trên đó bạn có thể gọi :meth:`~threading.Thread.start` để khởi động server và gọi :meth:`~threading.Thread.join` khi thích hợp. Để dừng server, hãy gọi :func:`stopListening`.

   Đối số ``verify``, nếu được chỉ định, phải là một callable có nhiệm vụ xác minh xem các byte nhận được qua socket có hợp lệ và cần được xử lý hay không. Có thể thực hiện việc này bằng cách mã hóa và/hoặc ký dữ liệu được gửi qua socket, để callable ``verify`` có thể xác minh chữ ký và/hoặc giải mã. Callable ``verify`` được gọi với một đối số duy nhất—các byte nhận được qua socket—và phải trả về các byte cần xử lý, hoặc ``None`` để cho biết rằng các byte đó cần bị loại bỏ. Các byte được trả về có thể giống với các byte được truyền vào (ví dụ: khi chỉ thực hiện xác minh), hoặc có thể hoàn toàn khác (chẳng hạn nếu đã thực hiện giải mã).

   Để gửi một cấu hình đến socket, hãy đọc tệp cấu hình rồi gửi tệp đó đến socket dưới dạng một chuỗi byte, đứng trước là một chuỗi độ dài bốn byte được đóng gói ở dạng nhị phân bằng ``struct.pack('>L', n)``.

   .. _logging-eval-security:

   .. note::

      Vì một số phần của cấu hình được truyền qua
      :func:`eval`, việc sử dụng hàm này có thể khiến người dùng đối mặt với rủi ro bảo mật. Mặc dù hàm này chỉ liên kết với một socket trên ``localhost`` nên không chấp nhận kết nối từ các máy từ xa, vẫn có những tình huống trong đó mã không đáng tin cậy có thể được chạy dưới tài khoản của tiến trình gọi
      :func:`listen`. Cụ thể, nếu tiến trình gọi :func:`listen` chạy trên một máy có nhiều người dùng, nơi những người dùng không thể tin tưởng lẫn nhau, thì một người dùng độc hại có thể sắp xếp để chạy gần như mọi mã tùy ý trong tiến trình của người dùng nạn nhân, chỉ bằng cách kết nối tới
      :func:`listen` socket của nạn nhân và gửi một cấu hình chạy bất kỳ mã nào mà kẻ tấn công muốn thực thi trong tiến trình của nạn nhân. Điều này đặc biệt dễ thực hiện nếu sử dụng cổng mặc định, nhưng ngay cả khi sử dụng một cổng khác thì cũng không khó. Để tránh rủi ro này, hãy sử dụng đối số ``verify`` của :func:`listen` để ngăn không cho áp dụng các cấu hình không được nhận dạng.

   .. versionchanged:: 3.4
      Đối số ``verify`` đã được thêm vào.

   .. note::

      Nếu bạn muốn gửi các cấu hình đến listener mà không vô hiệu hóa các logger hiện có, bạn sẽ cần sử dụng định dạng JSON cho cấu hình, trong đó sẽ sử dụng :func:`dictConfig` để cấu hình. Phương thức này cho phép bạn chỉ định ``disable_existing_loggers`` dưới dạng ``False`` trong cấu hình mà bạn gửi.


.. function:: stopListening()

   Dừng listening server được tạo bằng lời gọi đến :func:`listen`. Thông thường, hàm này được gọi trước khi gọi :meth:`join` trên giá trị trả về từ
   :func:`listen`.


Các lưu ý về bảo mật
^^^^^^^^^^^^^^^^^^^^

Chức năng cấu hình logging cố gắng mang lại sự thuận tiện, và một phần trong đó được thực hiện bằng cách cung cấp khả năng chuyển đổi văn bản trong các tệp cấu hình thành các đối tượng Python được sử dụng trong cấu hình logging - ví dụ như được mô tả trong
:ref:`logging-config-dict-userdef`. Tuy nhiên, chính những cơ chế này (nhập các callable từ các module do người dùng định nghĩa và gọi chúng với các tham số từ cấu hình) có thể được sử dụng để gọi bất kỳ đoạn mã nào bạn muốn, và vì lý do này, bạn nên xử lý các tệp cấu hình từ các nguồn không đáng tin cậy với *hết sức thận trọng* và tự đảm bảo rằng không thể xảy ra điều gì nguy hiểm nếu bạn tải chúng, trước khi thực sự tải chúng.


.. _logging-config-dictschema:

Schema của dictionary cấu hình
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mô tả một cấu hình logging yêu cầu liệt kê các đối tượng khác nhau cần tạo và các kết nối giữa chúng; chẳng hạn, bạn có thể tạo một handler có tên 'console', rồi chỉ định rằng logger có tên 'startup' sẽ gửi các thông điệp của nó đến handler 'console'. Các đối tượng này không bị giới hạn ở những đối tượng do module :mod:`logging` cung cấp, vì bạn có thể tự viết lớp formatter hoặc handler của mình. Các tham số của những lớp này cũng có thể cần bao gồm các đối tượng bên ngoài như ``sys.stderr``. Cú pháp để mô tả các đối tượng và kết nối này được định nghĩa trong :ref:`logging-config-dict-connections` bên dưới.

Chi tiết schema của dictionary
""""""""""""""""""""""""""""""

Dictionary được truyền vào :func:`dictConfig` phải chứa các khóa sau:

* *version* - được đặt thành một giá trị số nguyên biểu thị phiên bản schema. Hiện tại, giá trị hợp lệ duy nhất là 1, nhưng việc có khóa này cho phép schema phát triển mà vẫn duy trì khả năng tương thích ngược.

Tất cả các khóa khác đều là tùy chọn, nhưng nếu có thì chúng sẽ được diễn giải như mô tả bên dưới. Trong mọi trường hợp bên dưới khi đề cập đến 'dict cấu hình', dict này sẽ được kiểm tra khóa đặc biệt ``'()'`` để xác định xem có cần khởi tạo tùy chỉnh hay không. Nếu có, cơ chế được mô tả trong
:ref:`logging-config-dict-userdef` bên dưới được dùng để tạo một instance; nếu không, context sẽ được dùng để xác định cần khởi tạo đối tượng nào.

.. _logging-config-dictschema-formatters:

* *formatters* - giá trị tương ứng sẽ là một dict, trong đó mỗi khóa là một formatter id và mỗi giá trị là một dict mô tả cách cấu hình instance :class:`~logging.Formatter` tương ứng.

  Dict cấu hình sẽ được tìm kiếm các khóa tùy chọn sau đây, tương ứng với các đối số được truyền vào để tạo một
  :class:`~logging.Formatter` object:

  * ``format``
  * ``datefmt``
  * ``style``
  * ``validate`` (kể từ phiên bản >=3.8)
  * ``defaults`` (kể từ phiên bản >=3.12)

  Khóa ``class`` tùy chọn cho biết tên class của formatter (dưới dạng tên module và class phân tách bằng dấu chấm). Các đối số khởi tạo giống như đối với :class:`~logging.Formatter`, vì vậy khóa này hữu ích nhất khi khởi tạo một subclass đã tùy chỉnh của
  :class:`~logging.Formatter`. Ví dụ: class thay thế có thể trình bày traceback của exception ở dạng mở rộng hoặc rút gọn. Nếu formatter của bạn yêu cầu các khóa cấu hình khác hoặc bổ sung, bạn nên sử dụng :ref:`logging-config-dict-userdef`.

* *filters* - giá trị tương ứng sẽ là một dict, trong đó mỗi khóa là một filter id và mỗi giá trị là một dict mô tả cách cấu hình instance Filter tương ứng.

  Dict cấu hình được tìm kiếm khóa ``name`` (mặc định là chuỗi rỗng), và khóa này được dùng để tạo một instance :class:`logging.Filter`.

* *handlers* - giá trị tương ứng sẽ là một dict, trong đó mỗi khóa là một ID của handler và mỗi giá trị là một dict mô tả cách cấu hình Handler tương ứng.

  Dict cấu hình được tìm kiếm theo các khóa sau:

  * ``class`` (bắt buộc). Đây là tên đầy đủ của lớp handler.

  * ``level`` (tùy chọn). Mức của handler.

  * ``formatter`` (tùy chọn). ID của formatter cho handler này.

  * ``filters`` (tùy chọn). Danh sách ID của các filter cho handler này.

    .. versionchanged:: 3.11
       ``filters`` có thể nhận các instance của filter ngoài các ID.

  Tất cả các khóa *khác* được truyền dưới dạng đối số từ khóa tới hàm khởi tạo của handler. Ví dụ, với đoạn mã:

  .. code-block:: yaml

      handlers:
        console:
          class : logging.StreamHandler
          formatter: brief
          level   : INFO
          filters: [allow_foo]
          stream  : ext://sys.stdout
        file:
          class : logging.handlers.RotatingFileHandler
          formatter: precise
          filename: logconfig.log
          maxBytes: 1024
          backupCount: 3

  handler có id ``console`` được khởi tạo dưới dạng
  :class:`logging.StreamHandler`, sử dụng ``sys.stdout`` làm stream nền. Handler có id ``file`` được khởi tạo dưới dạng
  :class:`logging.handlers.RotatingFileHandler` với các đối số từ khóa ``filename='logconfig.log', maxBytes=1024, backupCount=3``.

* *loggers* - giá trị tương ứng sẽ là một dict, trong đó mỗi khóa là tên logger và mỗi giá trị là một dict mô tả cách cấu hình thực thể Logger tương ứng.

  Dict cấu hình được tìm kiếm theo các khóa sau:

  * ``level`` (tùy chọn). Cấp độ của logger.

  * ``propagate`` (tùy chọn).  Cài đặt lan truyền của logger.

  * ``filters`` (tùy chọn).  Danh sách ID của các filter cho logger này.

    .. versionchanged:: 3.11
       ``filters`` có thể nhận các instance của filter ngoài các ID.

  * ``handlers`` (tùy chọn).  Danh sách ID của các handler cho logger này.

  Các logger được chỉ định sẽ được cấu hình theo level, propagation, filter và handler được chỉ định.

* *root* - đây sẽ là cấu hình cho root logger. Việc xử lý cấu hình sẽ giống như đối với mọi logger, ngoại trừ việc cài đặt ``propagate`` sẽ không được áp dụng.

* *incremental* - cho biết cấu hình có được diễn giải là phần gia tăng so với cấu hình hiện có hay không.  Giá trị này mặc định là ``False``, nghĩa là cấu hình được chỉ định sẽ thay thế cấu hình hiện có với cùng ngữ nghĩa như API :func:`fileConfig` hiện có.

  Nếu giá trị được chỉ định là ``True``, cấu hình sẽ được xử lý như mô tả trong phần về :ref:`logging-config-dict-incremental`.

* *disable_existing_loggers* - cho biết có vô hiệu hóa mọi logger hiện có không phải root hay không. Thiết lập này phản ánh tham số cùng tên trong
  :func:`fileConfig`. Nếu không có, tham số này mặc định là ``True``. Giá trị này bị bỏ qua nếu *incremental* là ``True``.

.. _logging-config-dict-incremental:

Cấu hình gia tăng
"""""""""""""""""

Rất khó cung cấp đầy đủ tính linh hoạt cho cấu hình gia tăng. Ví dụ, vì các đối tượng như filter và formatter là các đối tượng vô danh, sau khi cấu hình được thiết lập, không thể tham chiếu đến những đối tượng vô danh đó khi bổ sung cho cấu hình.

Hơn nữa, sau khi cấu hình được thiết lập, không có lý do thuyết phục để tùy ý thay đổi object graph của logger, handler, filter và formatter trong runtime; có thể kiểm soát mức độ chi tiết của logger và handler chỉ bằng cách thiết lập level (và với logger là các cờ propagation). Việc tùy ý thay đổi object graph theo cách an toàn là một vấn đề phức tạp trong môi trường đa luồng; dù không phải là bất khả thi, lợi ích đạt được không tương xứng với độ phức tạp mà việc này thêm vào phần triển khai.

Do đó, khi khóa ``incremental`` của một configuration dict hiện diện và có giá trị ``True``, hệ thống sẽ hoàn toàn bỏ qua mọi mục ``formatters`` và ``filters``, chỉ xử lý các thiết lập ``level`` trong các mục ``handlers``, cùng các thiết lập ``level`` và ``propagate`` trong các mục ``loggers`` và ``root``.

Việc sử dụng một giá trị trong configuration dict cho phép gửi các configuration dưới dạng dict đã được pickle qua mạng đến một socket listener. Nhờ đó, mức độ chi tiết của logging trong một ứng dụng chạy lâu dài có thể được thay đổi theo thời gian mà không cần dừng và khởi động lại ứng dụng.

.. _logging-config-dict-connections:

Kết nối giữa các đối tượng
""""""""""""""""""""""""""

Schema mô tả một tập hợp các đối tượng logging - logger, handler, formatter, filter - được kết nối với nhau trong một object graph. Vì vậy, schema cần biểu diễn các kết nối giữa những đối tượng này. Ví dụ, giả sử sau khi được cấu hình, một logger cụ thể được gắn với một handler cụ thể. Trong phạm vi thảo luận này, ta có thể nói logger là nguồn, còn handler là đích của kết nối giữa hai đối tượng. Tất nhiên, trong các đối tượng đã được cấu hình, điều này được biểu diễn bằng việc logger giữ một tham chiếu đến handler. Trong configuration dict, việc này được thực hiện bằng cách cấp cho mỗi đối tượng đích một id để nhận diện đối tượng đó một cách rõ ràng, sau đó sử dụng id này trong cấu hình của đối tượng nguồn để cho biết tồn tại một kết nối giữa đối tượng nguồn và đối tượng đích có id đó.

Ví dụ, hãy xem đoạn YAML sau:

.. code-block:: yaml

    formatters:
      brief:
        # đặt cấu hình cho formatter có id 'brief' tại đây
      precise:
        # đặt cấu hình cho formatter có id 'precise' tại đây
    handlers:
      h1: #Đây là một id
       # đặt cấu hình của handler có id 'h1' tại đây
       formatter: brief
      h2: #Đây là một id khác
       # đặt cấu hình của handler có id 'h2' tại đây
       formatter: precise
    loggers:
      foo.bar.baz:
        # cấu hình khác cho logger 'foo.bar.baz'
        handlers: [h1, h2]

(Lưu ý: YAML được sử dụng ở đây vì dễ đọc hơn một chút so với dạng mã nguồn Python tương đương của dictionary.)

Các id của logger là tên logger được dùng theo lập trình để lấy tham chiếu đến các logger đó, chẳng hạn như ``foo.bar.baz``. Các id của Formatter và Filter có thể là bất kỳ giá trị chuỗi nào (chẳng hạn như ``brief``, ``precise`` ở trên), và chúng là các giá trị tạm thời, nghĩa là chúng chỉ có ý nghĩa khi xử lý dictionary cấu hình và được dùng để xác định các kết nối giữa các đối tượng; chúng không được lưu ở bất kỳ đâu khi lệnh gọi cấu hình hoàn tất.

Đoạn mã trên cho biết logger có tên ``foo.bar.baz`` sẽ có hai handler được gắn vào, được mô tả bằng các id handler ``h1`` và ``h2``. Formatter cho ``h1`` là formatter được mô tả bằng id ``brief``, còn formatter cho ``h2`` là formatter được mô tả bằng id ``precise``.


.. _logging-config-dict-userdef:

Các đối tượng do người dùng định nghĩa
""""""""""""""""""""""""""""""""""""""

Schema hỗ trợ các đối tượng do người dùng định nghĩa cho handlers, filters và formatters. (Logger không cần có các kiểu khác nhau cho những instance khác nhau, vì vậy schema cấu hình này không hỗ trợ các lớp logger do người dùng định nghĩa.)

Các đối tượng cần cấu hình được mô tả bằng các dictionary nêu chi tiết cấu hình của chúng. Ở một số nơi, hệ thống logging có thể suy ra từ context cách khởi tạo một đối tượng, nhưng khi cần khởi tạo một đối tượng do người dùng định nghĩa, hệ thống sẽ không biết phải làm thế nào. Để cung cấp đầy đủ tính linh hoạt cho việc khởi tạo đối tượng do người dùng định nghĩa, người dùng cần cung cấp một 'factory' - một callable được gọi với một dictionary cấu hình và trả về đối tượng đã khởi tạo. Điều này được chỉ báo bằng một absolute import path tới factory được cung cấp dưới key đặc biệt ``'()'``. Sau đây là một ví dụ cụ thể:

.. code-block:: yaml

    formatters:
      brief:
        format: '%(message)s'
      default:
        format: '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
        datefmt: '%Y-%m-%d %H:%M:%S'
      custom:
          (): my.package.customFormatterFactory
          bar: baz
          spam: 99.9
          answer: 42

Đoạn YAML ở trên định nghĩa ba formatter. Formatter đầu tiên, có id ``brief``, là một instance :class:`logging.Formatter` tiêu chuẩn với format string được chỉ định. Formatter thứ hai, có id ``default``, có format dài hơn và cũng định nghĩa rõ ràng time format, đồng thời sẽ tạo ra một :class:`logging.Formatter` được khởi tạo với hai format string đó. Ở dạng mã nguồn Python, các formatter ``brief`` và ``default`` có các sub-dictionary cấu hình::

    {
      'format' : '%(message)s'
    }

và::

    {
      'format' : '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
      'datefmt' : '%Y-%m-%d %H:%M:%S'
    }

tương ứng, và vì các dictionary này không chứa key đặc biệt ``'()'``, việc khởi tạo được suy ra từ context: do đó, các instance :class:`logging.Formatter` tiêu chuẩn được tạo. Sub-dictionary cấu hình của formatter thứ ba, có id ``custom``, là::

  {
    '()' : 'my.package.customFormatterFactory',
    'bar' : 'baz',
    'spam' : 99.9,
    'answer' : 42
  }

và sub-dictionary này chứa key đặc biệt ``'()'``, nghĩa là cần khởi tạo do người dùng định nghĩa. Trong trường hợp này, callable factory được chỉ định sẽ được sử dụng. Nếu đó là một callable thực sự, nó sẽ được sử dụng trực tiếp - nếu không, khi bạn chỉ định một string (như trong ví dụ), callable thực sự sẽ được tìm thấy bằng các cơ chế import thông thường. Callable sẽ được gọi với các item **remaining** trong sub-dictionary cấu hình dưới dạng các keyword argument. Trong ví dụ trên, formatter có id ``custom`` sẽ được giả định là giá trị trả về của lời gọi đó::

    my.package.customFormatterFactory(bar='baz', spam=99.9, answer=42)

.. warning:: Các giá trị của những khóa như ``bar``, ``spam`` và ``answer`` trong ví dụ trên không được là các từ điển cấu hình hoặc các tham chiếu như ``cfg://foo`` hay ``ext://bar``, vì chúng sẽ không được cơ chế cấu hình xử lý mà được truyền nguyên trạng cho callable.

Khóa ``'()'`` được dùng làm khóa đặc biệt vì đây không phải là tên tham số keyword hợp lệ, nên sẽ không xung đột với tên của các đối số keyword được sử dụng trong lời gọi. ``'()'`` cũng là một gợi nhớ rằng giá trị tương ứng là một callable.

.. versionchanged:: 3.11
   Thành viên ``filters`` của ``handlers`` và ``loggers`` có thể nhận các instance của filter ngoài các id.

Bạn cũng có thể chỉ định một khóa đặc biệt ``'.'`` có giá trị là một mapping từ tên thuộc tính đến các giá trị. Nếu tìm thấy, các thuộc tính được chỉ định sẽ được thiết lập trên đối tượng do người dùng định nghĩa trước khi đối tượng này được trả về. Vì vậy, với cấu hình sau đây::

    {
      '()' : 'my.package.customFormatterFactory',
      'bar' : 'baz',
      'spam' : 99.9,
      'answer' : 42,
      '.' : {
        'foo': 'bar',
        'baz': 'bozz'
      }
    }

formatter được trả về sẽ có thuộc tính ``foo`` được thiết lập thành ``'bar'`` và thuộc tính ``baz`` được thiết lập thành ``'bozz'``.

.. warning:: Các giá trị của những thuộc tính như ``foo`` và ``baz`` trong ví dụ trên không được là các từ điển cấu hình hoặc các tham chiếu như ``cfg://foo`` hay ``ext://bar``, vì chúng sẽ không được cơ chế cấu hình xử lý mà được thiết lập nguyên trạng làm các giá trị thuộc tính.


.. _handler-config-dict-order:

Thứ tự cấu hình handler
"""""""""""""""""""""""

Các handler được cấu hình theo thứ tự bảng chữ cái của khóa, và một handler đã được cấu hình sẽ thay thế từ điển cấu hình trong (một bản sao đang hoạt động của) từ điển ``handlers`` trong schema. Nếu bạn sử dụng một cấu trúc như ``cfg://handlers.foo``, thì ban đầu ``handlers['foo']`` trỏ đến từ điển cấu hình của handler có tên ``foo``, và sau đó (khi handler đó đã được cấu hình) nó trỏ đến instance handler đã được cấu hình. Do đó, ``cfg://handlers.foo`` có thể phân giải thành một từ điển hoặc một instance handler. Nhìn chung, nên đặt tên các handler sao cho các handler phụ thuộc được cấu hình *after* mọi handler mà chúng phụ thuộc vào; điều đó cho phép sử dụng một cấu trúc như ``cfg://handlers.foo`` khi cấu hình một handler phụ thuộc vào handler ``foo``. Nếu handler phụ thuộc đó được đặt tên là ``bar``, sẽ phát sinh vấn đề, vì việc cấu hình ``bar`` sẽ được thực hiện trước ``foo``, và ``foo`` vẫn chưa được cấu hình. Tuy nhiên, nếu handler phụ thuộc được đặt tên là ``foobar``, nó sẽ được cấu hình sau ``foo``, nhờ đó ``cfg://handlers.foo`` sẽ phân giải thành handler đã được cấu hình ``foo``, chứ không phải từ điển cấu hình của nó.


.. _logging-config-dict-externalobj:

Truy cập các đối tượng bên ngoài
""""""""""""""""""""""""""""""""

Đôi khi cấu hình cần tham chiếu đến các đối tượng bên ngoài cấu hình, chẳng hạn như ``sys.stderr``. Nếu từ điển cấu hình được tạo bằng mã Python thì việc này rất đơn giản, nhưng vấn đề phát sinh khi cấu hình được cung cấp qua một tệp văn bản (ví dụ: JSON, YAML). Trong tệp văn bản, không có cách tiêu chuẩn nào để phân biệt ``sys.stderr`` với chuỗi ký tự ``'sys.stderr'``. Để hỗ trợ việc phân biệt này, hệ thống cấu hình tìm kiếm một số tiền tố đặc biệt trong các giá trị chuỗi và xử lý chúng theo cách đặc biệt. Ví dụ, nếu chuỗi ký tự ``'ext://sys.stderr'`` được cung cấp làm một giá trị trong cấu hình, thì ``ext://`` sẽ bị loại bỏ và phần giá trị còn lại được xử lý bằng các cơ chế import thông thường.

Việc xử lý các tiền tố như vậy được thực hiện tương tự như việc xử lý protocol: có một cơ chế chung để tìm các tiền tố khớp với biểu thức chính quy ``^(?P<prefix>[a-z]+)://(?P<suffix>.*)$``; theo đó, nếu ``prefix`` được nhận diện, thì ``suffix`` được xử lý theo cách phụ thuộc vào tiền tố và kết quả xử lý sẽ thay thế giá trị chuỗi. Nếu tiền tố không được nhận diện, giá trị chuỗi sẽ được giữ nguyên.


.. _logging-config-dict-internalobj:

Truy cập các đối tượng bên trong
""""""""""""""""""""""""""""""""

Bên cạnh các đối tượng bên ngoài, đôi khi cũng cần tham chiếu đến các đối tượng trong cấu hình. Hệ thống cấu hình sẽ tự động thực hiện việc này đối với những đối tượng mà nó biết. Ví dụ, giá trị chuỗi ``'DEBUG'`` của một ``level`` trong logger hoặc handler sẽ tự động được chuyển đổi thành giá trị ``logging.DEBUG``, còn các mục ``handlers``, ``filters`` và ``formatter`` sẽ nhận một object id và phân giải thành đối tượng đích tương ứng.

Tuy nhiên, cần có một cơ chế tổng quát hơn cho các đối tượng do người dùng định nghĩa mà module :mod:`logging` không biết. Ví dụ, hãy xem xét :class:`logging.handlers.MemoryHandler`, nhận một đối số ``target`` là một handler khác để ủy quyền xử lý. Vì hệ thống đã biết lớp này, nên trong cấu hình, ``target`` được cung cấp chỉ cần là object id của handler đích tương ứng, và hệ thống sẽ phân giải thành handler từ
id.  Tuy nhiên, nếu người dùng định nghĩa một ``my.package.MyHandler`` có
handler ``alternate``, hệ thống cấu hình sẽ không biết rằng ``alternate`` tham chiếu đến một handler. Để đáp ứng trường hợp này, một hệ thống phân giải tổng quát cho phép người dùng chỉ định:

.. code-block:: yaml

    handlers:
      file:
        # cấu hình của file handler đặt tại đây

      custom:
        (): my.package.MyHandler
        alternate: cfg://handlers.file

Chuỗi ký tự nguyên văn ``'cfg://handlers.file'`` sẽ được phân giải tương tự như các chuỗi có tiền tố ``ext://``, nhưng sẽ tìm trong chính cấu hình thay vì namespace import. Cơ chế này cho phép truy cập bằng dấu chấm hoặc chỉ mục, tương tự như cơ chế do ``str.format`` cung cấp. Vì vậy, với đoạn mã sau:

.. code-block:: yaml

    handlers:
      email:
        class: logging.handlers.SMTPHandler
        mailhost: localhost
        fromaddr: my_app@domain.tld
        toaddrs:
          - support_team@domain.tld
          - dev_team@domain.tld
        subject: Houston, we have a problem.

trong cấu hình, chuỗi ``'cfg://handlers'`` sẽ được phân giải thành dict có khóa ``handlers``, chuỗi ``'cfg://handlers.email`` sẽ được phân giải thành dict có khóa ``email`` trong dict ``handlers``, và tương tự. Chuỗi ``'cfg://handlers.email.toaddrs[1]`` sẽ được phân giải thành ``'dev_team@domain.tld'`` và chuỗi ``'cfg://handlers.email.toaddrs[0]'`` sẽ được phân giải thành giá trị ``'support_team@domain.tld'``. Có thể truy cập giá trị ``subject`` bằng ``'cfg://handlers.email.subject'`` hoặc tương đương là ``'cfg://handlers.email[subject]'``. Chỉ cần sử dụng dạng sau nếu khóa chứa khoảng trắng hoặc các ký tự không phải chữ và số. Lưu ý rằng các ký tự ``[`` và ``]`` không được phép xuất hiện trong khóa. Nếu một giá trị chỉ mục chỉ gồm các chữ số thập phân, hệ thống sẽ thử truy cập bằng giá trị số nguyên tương ứng, sau đó chuyển sang giá trị chuỗi nếu cần.

Với chuỗi ``cfg://handlers.myhandler.mykey.123``, chuỗi này sẽ được phân giải thành ``config_dict['handlers']['myhandler']['mykey']['123']``. Nếu chuỗi được chỉ định là ``cfg://handlers.myhandler.mykey[123]``, hệ thống sẽ cố lấy giá trị từ ``config_dict['handlers']['myhandler']['mykey'][123]``, và chuyển sang ``config_dict['handlers']['myhandler']['mykey']['123']`` nếu không thành công.


.. _logging-import-resolution:

Phân giải import và các importer tùy chỉnh
""""""""""""""""""""""""""""""""""""""""""

Theo mặc định, việc phân giải import sử dụng hàm dựng sẵn :func:`__import__` để thực hiện import. Bạn có thể muốn thay thế hàm này bằng cơ chế import của riêng mình; nếu vậy, bạn có thể thay thế thuộc tính :attr:`importer` của
:class:`DictConfigurator` hoặc lớp cha của nó, lớp
:class:`BaseConfigurator` hoặc lớp cha của nó là lớp :class:`BaseConfigurator`. Tuy nhiên, bạn cần cẩn thận vì cách các hàm được truy cập từ lớp thông qua descriptor. Nếu bạn sử dụng một đối tượng callable Python để thực hiện import và muốn định nghĩa nó ở cấp lớp thay vì cấp instance, bạn cần bọc nó bằng :func:`staticmethod`. Ví dụ::

   from importlib import import_module
   from logging.config import BaseConfigurator

   BaseConfigurator.importer = staticmethod(import_module)

Bạn không cần bọc bằng :func:`staticmethod` nếu đặt callable import trên một *instance* của configurator.

.. _configure-queue:

Cấu hình QueueHandler và QueueListener
""""""""""""""""""""""""""""""""""""""

Nếu bạn muốn cấu hình một :class:`~logging.handlers.QueueHandler`, lưu ý rằng thành phần này thường được sử dụng cùng với một :class:`~logging.handlers.QueueListener`, bạn có thể cấu hình cả hai cùng lúc. Sau khi cấu hình, instance ``QueueListener`` sẽ có sẵn dưới dạng thuộc tính :attr:`~logging.handlers.QueueHandler.listener` của handler được tạo, và đến lượt nó sẽ có sẵn cho bạn bằng cách sử dụng
:func:`~logging.getHandlerByName` và truyền vào tên bạn đã sử dụng cho ``QueueHandler`` trong cấu hình. Lược đồ dictionary để cấu hình cặp này được trình bày trong đoạn YAML ví dụ bên dưới.

.. code-block:: yaml

    handlers:
      qhand:
        class: logging.handlers.QueueHandler
        queue: my.module.queue_factory
        listener: my.package.CustomListener
        handlers:
          - hand_name_1
          - hand_name_2
          ...

Các khóa ``queue`` và ``listener`` là tùy chọn.

Nếu có khóa ``queue``, giá trị tương ứng có thể là một trong các loại sau:

* Một đối tượng triển khai API công khai :meth:`Queue.put_nowait <queue.Queue.put_nowait>` và :meth:`Queue.get <queue.Queue.get>`. Ví dụ, đây có thể là một thể hiện thực tế của :class:`queue.Queue` hoặc lớp con của nó, hay một proxy nhận được từ :meth:`multiprocessing.managers.SyncManager.Queue`.

  Tất nhiên, điều này chỉ có thể thực hiện nếu bạn đang tạo hoặc sửa đổi dictionary cấu hình trong code.

* Một chuỗi phân giải thành một callable mà khi được gọi không có đối số sẽ trả về thể hiện queue cần sử dụng. Callable đó có thể là một lớp con của :class:`queue.Queue` hoặc một hàm trả về một thể hiện queue phù hợp, chẳng hạn như ``my.module.queue_factory()``.

* Một dict có khóa ``'()'``, được tạo theo cách thông thường như đã thảo luận trong
  :ref:`logging-config-dict-userdef`. Kết quả của việc tạo này phải là một
  instance :class:`queue.Queue`.

Nếu thiếu khóa ``queue``, một instance :class:`queue.Queue` không giới hạn tiêu chuẩn sẽ được tạo và sử dụng.

Nếu có khóa ``listener``, giá trị tương ứng có thể là một trong các giá trị sau:

* Một lớp con của :class:`logging.handlers.QueueListener`. Tất nhiên, điều này chỉ khả thi nếu bạn đang tạo hoặc sửa đổi dictionary cấu hình trong code.

* Một chuỗi phân giải thành một lớp là lớp con của ``QueueListener``, chẳng hạn như ``'my.package.CustomListener'``.

* Một dict có khóa ``'()'``, được tạo theo cách thông thường như đã thảo luận trong
  :ref:`logging-config-dict-userdef`. Kết quả của việc khởi tạo này phải là một callable có cùng signature với hàm khởi tạo ``QueueListener``.

Nếu khóa ``listener`` không tồn tại, :class:`logging.handlers.QueueListener` sẽ được sử dụng.

Các giá trị dưới khóa ``handlers`` là tên của các handler khác trong cấu hình (không hiển thị trong đoạn trích ở trên), những handler này sẽ được truyền cho queue listener.

Mọi lớp queue handler và listener tùy chỉnh cần được định nghĩa với cùng các chữ ký khởi tạo như :class:`~logging.handlers.QueueHandler` và
:class:`~logging.handlers.QueueListener`.

.. versionadded:: 3.12

.. _logging-config-fileformat:

Định dạng tệp cấu hình
^^^^^^^^^^^^^^^^^^^^^^

Định dạng tệp cấu hình được :func:`fileConfig` hiểu dựa trên
chức năng :mod:`configparser`. Tệp phải chứa các phần có tên ``[loggers]``, ``[handlers]`` và ``[formatters]``, dùng để xác định theo tên các thực thể thuộc từng loại được định nghĩa trong tệp. Với mỗi thực thể như vậy, có một phần riêng xác định cách cấu hình thực thể đó. Do đó, đối với logger có tên ``log01`` trong phần ``[loggers]``, các chi tiết cấu hình liên quan được lưu trong phần ``[logger_log01]``. Tương tự, handler có tên ``hand01`` trong phần ``[handlers]`` sẽ có cấu hình được lưu trong phần có tên ``[handler_hand01]``, còn formatter có tên ``form01`` trong phần ``[formatters]`` sẽ có cấu hình được chỉ định trong phần ``[formatter_form01]``. Cấu hình của root logger phải được chỉ định trong phần có tên ``[logger_root]``.

.. note::

   API :func:`fileConfig` cũ hơn API :func:`dictConfig` và không cung cấp chức năng để xử lý một số khía cạnh nhất định của việc logging. Ví dụ, bạn không thể cấu hình các đối tượng :class:`~logging.Filter`, vốn cho phép lọc thông báo theo các mức ngoài các mức số nguyên đơn giản, bằng :func:`fileConfig`. Nếu cần có các instance của :class:`~logging.Filter` trong cấu hình logging, bạn sẽ cần sử dụng :func:`dictConfig`. Lưu ý rằng các cải tiến trong tương lai đối với chức năng cấu hình sẽ được bổ sung vào
   :func:`dictConfig`, vì vậy đáng cân nhắc chuyển sang API mới hơn này khi thuận tiện.

Dưới đây là các ví dụ về những phần này trong tệp.

.. code-block:: ini

   [loggers]
   keys=root,log02,log03,log04,log05,log06,log07

   [handlers]
   keys=hand01,hand02,hand03,hand04,hand05,hand06,hand07,hand08,hand09

   [formatters]
   keys=form01,form02,form03,form04,form05,form06,form07,form08,form09

Logger gốc phải chỉ định một cấp độ và danh sách các handler. Dưới đây là ví dụ về phần logger gốc.

.. code-block:: ini

   [logger_root]
   level=NOTSET
   handlers=hand01

Mục nhập ``level`` có thể là ``DEBUG, INFO, WARNING, ERROR, CRITICAL`` hoặc ``NOTSET``. Chỉ đối với logger gốc, ``NOTSET`` có nghĩa là tất cả thông báo sẽ được ghi lại. Các giá trị cấp độ được :ref:`đánh giá <func-eval>` trong không gian tên của gói ``logging``.

Mục nhập ``handlers`` là danh sách tên handler được phân tách bằng dấu phẩy; các tên này phải xuất hiện trong phần ``[handlers]``. Những tên này phải xuất hiện trong phần ``[handlers]`` và có các phần tương ứng trong tệp cấu hình.

Đối với các logger khác logger gốc, cần có thêm một số thông tin. Ví dụ sau minh họa điều này.

.. code-block:: ini

   [logger_parser]
   level=DEBUG
   handlers=hand01
   propagate=1
   qualname=compiler.parser

Các mục nhập ``level`` và ``handlers`` được diễn giải như đối với logger gốc, ngoại trừ việc nếu cấp độ của một logger không phải logger gốc được chỉ định là ``NOTSET``, hệ thống sẽ tham khảo các logger ở cấp cao hơn trong hệ thống phân cấp để xác định cấp độ hiệu lực của logger đó. Mục nhập ``propagate`` được đặt thành 1 để cho biết rằng các thông báo phải được truyền đến các handler ở cấp cao hơn trong hệ thống phân cấp logger từ logger này, hoặc thành 0 để cho biết rằng các thông báo **không** được truyền đến các handler ở cấp cao hơn trong hệ thống phân cấp. Mục nhập ``qualname`` là tên kênh phân cấp của logger, tức là tên mà ứng dụng sử dụng để lấy logger.

Các section chỉ định cấu hình handler được minh họa như sau.

.. code-block:: ini

   [handler_hand01]
   class=StreamHandler
   level=NOTSET
   formatter=form01
   args=(sys.stdout,)

Mục ``class`` cho biết class của handler (được xác định bởi :func:`eval` trong namespace của package ``logging``). ``level`` được diễn giải giống như đối với logger, còn ``NOTSET`` được hiểu là “ghi log mọi thứ”.

Mục ``formatter`` cho biết tên khóa của formatter cho handler này. Nếu để trống, formatter mặc định (``logging._defaultFormatter``) sẽ được sử dụng. Nếu chỉ định một tên, tên đó phải xuất hiện trong section ``[formatters]`` và có section tương ứng trong tệp cấu hình.

Mục ``args``, khi :ref:`evaluated <func-eval>` trong ngữ cảnh namespace của package ``logging``, là danh sách các đối số truyền cho constructor của class handler. Hãy tham khảo các constructor của những handler liên quan hoặc các ví dụ bên dưới để xem cách xây dựng các mục điển hình. Nếu không được cung cấp, giá trị mặc định là ``()``.

Mục ``kwargs`` tùy chọn, khi :ref:`evaluated <func-eval>` trong ngữ cảnh namespace của package ``logging``, là dict đối số từ khóa truyền cho constructor của class handler. Nếu không được cung cấp, giá trị mặc định là ``{}``.

.. code-block:: ini

   [handler_hand02]
   class=FileHandler
   level=DEBUG
   formatter=form02
   args=('python.log', 'w')

   [handler_hand03]
   class=handlers.SocketHandler
   level=INFO
   formatter=form03
   args=('localhost', handlers.DEFAULT_TCP_LOGGING_PORT)

   [handler_hand04]
   class=handlers.DatagramHandler
   level=WARN
   formatter=form04
   args=('localhost', handlers.DEFAULT_UDP_LOGGING_PORT)

   [handler_hand05]
   class=handlers.SysLogHandler
   level=ERROR
   formatter=form05
   args=(('localhost', handlers.SYSLOG_UDP_PORT), handlers.SysLogHandler.LOG_USER)

   [handler_hand06]
   class=handlers.NTEventLogHandler
   level=CRITICAL
   formatter=form06
   args=('Python Application', '', 'Application')

   [handler_hand07]
   class=handlers.SMTPHandler
   level=WARN
   formatter=form07
   args=('localhost', 'from@abc', ['user1@abc', 'user2@xyz'], 'Logger Subject')
   kwargs={'timeout': 10.0}

   [handler_hand08]
   class=handlers.MemoryHandler
   level=NOTSET
   formatter=form08
   target=
   args=(10, ERROR)

   [handler_hand09]
   class=handlers.HTTPHandler
   level=NOTSET
   formatter=form09
   args=('localhost:9022', '/log', 'GET')
   kwargs={'secure': True}

Các section chỉ định cấu hình formatter thường có dạng như sau.

.. code-block:: ini

   [formatter_form01]
   format=F1 %(asctime)s %(levelname)s %(message)s %(customfield)s
   datefmt=
   style=%
   validate=True
   defaults={'customfield': 'defaultvalue'}
   class=logging.Formatter

Các đối số cho cấu hình formatter giống với các khóa trong schema từ điển :ref:`formatters section <logging-config-dictschema-formatters>`.

Mục nhập ``defaults``, khi :ref:`được đánh giá <func-eval>` trong ngữ cảnh namespace của package ``logging``, là một dictionary chứa các giá trị mặc định cho những trường định dạng tùy chỉnh. Nếu không được cung cấp, mục này mặc định là ``None``.


.. note::

   Do sử dụng :func:`eval` như mô tả ở trên, việc sử dụng :func:`listen` để gửi và nhận cấu hình qua socket có thể dẫn đến các rủi ro bảo mật. Các rủi ro này chỉ xảy ra khi nhiều người dùng không tin cậy lẫn nhau chạy code trên cùng một máy; xem
   tài liệu :func:`listen` để biết thêm thông tin.

.. seealso::

   Mô-đun :mod:`logging`
      Tài liệu tham khảo API cho mô-đun logging.

   Mô-đun :mod:`logging.handlers`
      Các handler hữu ích đi kèm mô-đun logging.
