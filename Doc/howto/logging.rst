.. _logging-howto:

=====================
HƯỚNG DẪN GHI NHẬT KÝ
=====================

:Author: Vinay Sajip <vinay_sajip at red-dove dot com>

.. _logging-basic-tutorial:

.. currentmodule:: logging

Trang này chứa thông tin hướng dẫn. Để xem các liên kết đến thông tin tham khảo và sổ tay ghi nhật ký, vui lòng xem :ref:`tutorial-ref-links`.

Hướng dẫn ghi nhật ký cơ bản
----------------------------

Ghi nhật ký là một phương thức theo dõi các sự kiện xảy ra khi một phần mềm chạy. Nhà phát triển phần mềm thêm các lệnh gọi ghi nhật ký vào mã của họ để cho biết một số sự kiện nhất định đã xảy ra. Một sự kiện được mô tả bằng một thông báo diễn giải, trong đó có thể tùy chọn chứa dữ liệu biến đổi (tức là dữ liệu có thể khác nhau trong mỗi lần sự kiện xảy ra). Các sự kiện cũng có mức độ quan trọng do nhà phát triển gán cho sự kiện; mức độ quan trọng này cũng có thể được gọi là *level* hoặc *severity*.

Khi nào nên sử dụng ghi nhật ký
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bạn có thể truy cập chức năng ghi nhật ký bằng cách tạo một logger thông qua ``logger = logging.getLogger(__name__)``, sau đó gọi :meth:`~Logger.debug` của logger,
:meth:`~Logger.info`, :meth:`~Logger.warning`, :meth:`~Logger.error` và
Các phương thức :meth:`~Logger.critical`. Để xác định khi nào nên sử dụng logging và xem nên dùng phương thức logger nào trong từng trường hợp, hãy xem bảng bên dưới. Bảng nêu công cụ tốt nhất cho từng tác vụ trong số các tác vụ phổ biến.

+-------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Tác vụ bạn muốn thực hiện                                                                                                           | Công cụ tốt nhất cho tác vụ                                                                                                                 |
+=====================================================================================================================================+=============================================================================================================================================+
| Hiển thị đầu ra trên console cho việc sử dụng thông thường của một script hoặc chương trình dòng lệnh                               | :func:`print`                                                                                                                               |
+-------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Báo cáo các sự kiện xảy ra trong quá trình hoạt động bình thường của chương trình (ví dụ: để theo dõi trạng thái hoặc điều tra lỗi) | :meth:`~Logger.info` của logger (hoặc                                                                                                       |
|                                                                                                                                     | phương thức :meth:`~Logger.debug` để xuất thông tin rất chi tiết cho mục đích chẩn đoán)                                                    |
+-------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Đưa ra cảnh báo về một sự kiện cụ thể trong runtime                                                                                 | :func:`warnings.warn` trong mã thư viện nếu có thể tránh được vấn đề và ứng dụng client nên được sửa đổi để loại bỏ cảnh báo                |
|                                                                                                                                     |                                                                                                                                             |
|                                                                                                                                     | Phương thức :meth:`~Logger.warning` của logger nếu ứng dụng client không thể làm gì với tình huống này, nhưng sự kiện vẫn cần được ghi nhận |
+-------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Báo cáo lỗi liên quan đến một sự kiện cụ thể trong runtime                                                                          | Phát sinh một exception                                                                                                                     |
+-------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Báo cáo việc suppress một lỗi mà không phát sinh exception (ví dụ: error handler trong một server process chạy lâu dài)             | :meth:`~Logger.error` của logger,                                                                                                           |
|                                                                                                                                     | :meth:`~Logger.exception` hoặc                                                                                                              |
|                                                                                                                                     | phương thức :meth:`~Logger.critical` tùy theo lỗi cụ thể và lĩnh vực ứng dụng                                                               |
+-------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------+

Các phương thức của logger được đặt tên theo cấp độ hoặc mức độ nghiêm trọng của các sự kiện mà chúng được dùng để theo dõi. Các cấp độ tiêu chuẩn và phạm vi áp dụng của chúng được mô tả dưới đây (theo thứ tự tăng dần về mức độ nghiêm trọng):

.. tabularcolumns:: |l|L|

+--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Cấp độ       | Được sử dụng khi                                                                                                                                                         |
+==============+==========================================================================================================================================================================+
| ``DEBUG``    | Thông tin chi tiết, thường chỉ hữu ích khi chẩn đoán sự cố.                                                                                                              |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``INFO``     | Xác nhận rằng mọi thứ đang hoạt động như mong đợi.                                                                                                                       |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``WARNING``  | Một dấu hiệu cho thấy đã xảy ra điều gì đó bất ngờ hoặc có thể sắp xảy ra một vấn đề nào đó (ví dụ: 'sắp hết dung lượng đĩa'). Phần mềm vẫn đang hoạt động như mong đợi. |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``ERROR``    | Do một vấn đề nghiêm trọng hơn, phần mềm không thể thực hiện một chức năng nào đó.                                                                                       |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``CRITICAL`` | Một lỗi nghiêm trọng, cho thấy bản thân chương trình có thể không thể tiếp tục chạy.                                                                                     |
+--------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Mức mặc định là ``WARNING``, nghĩa là chỉ những sự kiện có mức độ nghiêm trọng này hoặc cao hơn mới được theo dõi, trừ khi gói logging được cấu hình theo cách khác.

Các sự kiện được theo dõi có thể được xử lý theo nhiều cách khác nhau. Cách đơn giản nhất để xử lý các sự kiện được theo dõi là in chúng ra console. Một cách phổ biến khác là ghi chúng vào một tệp trên đĩa.


.. _howto-minimal-example:

Một ví dụ đơn giản
^^^^^^^^^^^^^^^^^^

Một ví dụ rất đơn giản là::

   import logging
   logging.warning('Watch out!')  # sẽ in một thông báo ra console
   logging.info('I told you so')  # sẽ không in gì cả

Nếu bạn nhập những dòng này vào một script rồi chạy nó, bạn sẽ thấy:

.. code-block:: none

   WARNING:root:Watch out!

được in ra console. Thông báo ``INFO`` không xuất hiện vì cấp độ mặc định là ``WARNING``. Thông báo được in bao gồm chỉ báo về cấp độ và phần mô tả sự kiện được cung cấp trong lời gọi logging, tức là 'Watch out!'. Nếu cần, bạn có thể định dạng đầu ra thực tế khá linh hoạt; các tùy chọn định dạng cũng sẽ được giải thích ở phần sau.

Lưu ý rằng trong ví dụ này, chúng ta sử dụng trực tiếp các hàm trên module ``logging``, chẳng hạn như ``logging.debug``, thay vì tạo một logger rồi gọi các hàm trên đó. Các hàm này hoạt động trên root logger, nhưng có thể hữu ích vì chúng sẽ gọi :func:`~logging.basicConfig` thay bạn nếu hàm này chưa được gọi, như trong ví dụ này. Tuy nhiên, trong các chương trình lớn hơn, bạn thường sẽ muốn kiểm soát rõ ràng cấu hình logging; vì lý do đó cũng như các lý do khác, tốt hơn là tạo các logger và gọi các phương thức của chúng.

Ghi log vào tệp
^^^^^^^^^^^^^^^

Một tình huống rất phổ biến là ghi các sự kiện logging vào một tệp, vì vậy tiếp theo chúng ta hãy xem xét trường hợp đó. Hãy nhớ thử các bước sau trong một Python interpreter mới khởi động, đừng chỉ tiếp tục từ phiên làm việc được mô tả ở trên::

   import logging
   logger = logging.getLogger(__name__)
   logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
   logger.debug('This message should go to the log file')
   logger.info('So should this')
   logger.warning('And this, too')
   logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

.. versionchanged:: 3.9
   Đối số *encoding* đã được thêm vào. Trong các phiên bản Python trước đây, hoặc khi không được chỉ định, encoding được sử dụng là giá trị mặc định mà :func:`open` sử dụng. Mặc dù không được hiển thị trong ví dụ trên, hiện nay bạn cũng có thể truyền đối số *errors*, đối số này xác định cách xử lý các lỗi encoding. Để biết các giá trị khả dụng và giá trị mặc định, hãy xem tài liệu về :func:`open`.

Và bây giờ, nếu chúng ta mở tệp và xem nội dung, chúng ta sẽ thấy các thông báo log:

.. code-block:: none

   DEBUG:__main__:This message should go to the log file
   INFO:__main__:So should this
   WARNING:__main__:And this, too
   ERROR:__main__:And non-ASCII stuff, too, like Øresund and Malmö

Ví dụ này cũng cho thấy cách bạn có thể đặt logging level, đóng vai trò là ngưỡng để theo dõi. Trong trường hợp này, vì chúng ta đặt ngưỡng thành ``DEBUG``, tất cả các thông báo đều được in ra.

Nếu bạn muốn đặt logging level từ một tùy chọn dòng lệnh như sau:

.. code-block:: none

   --log=INFO

và bạn có giá trị của tham số được truyền cho ``--log`` trong một biến *loglevel*, bạn có thể sử dụng::

   getattr(logging, loglevel.upper())

để lấy giá trị mà bạn sẽ truyền cho :func:`basicConfig` thông qua đối số *level*. Bạn có thể muốn kiểm tra lỗi đối với mọi giá trị đầu vào của người dùng, chẳng hạn như trong ví dụ sau::

   # giả sử loglevel được liên kết với giá trị chuỗi nhận được từ
   # đối số dòng lệnh. Chuyển thành chữ hoa để cho phép người dùng
   # chỉ định --log=DEBUG hoặc --log=debug
   numeric_level = getattr(logging, loglevel.upper(), None)
   if not isinstance(numeric_level, int):
       raise ValueError('Invalid log level: %s' % loglevel)
   logging.basicConfig(level=numeric_level, ...)

Lệnh gọi :func:`basicConfig` nên được thực hiện *trước* mọi lệnh gọi đến các phương thức của logger như :meth:`~Logger.debug`, :meth:`~Logger.info`, v.v. Nếu không, sự kiện ghi nhật ký đó có thể không được xử lý theo cách mong muốn.

Nếu bạn chạy tập lệnh trên nhiều lần, các thông báo từ những lần chạy liên tiếp sẽ được nối thêm vào tệp *example.log*. Nếu muốn mỗi lần chạy bắt đầu lại từ đầu và không ghi nhớ các thông báo từ những lần chạy trước, bạn có thể chỉ định đối số *filemode* bằng cách thay đổi lệnh gọi trong ví dụ trên thành::

   logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

Kết quả sẽ giống như trước, nhưng tệp nhật ký không còn được nối thêm, vì vậy các thông báo từ những lần chạy trước sẽ bị mất.


Ghi dữ liệu biến
^^^^^^^^^^^^^^^^

Để ghi nhật ký dữ liệu biến, hãy sử dụng một chuỗi định dạng cho thông báo mô tả sự kiện và thêm dữ liệu biến làm các đối số. Ví dụ:::

   import logging
   logging.warning('%s before you %s', 'Look', 'leap!')

sẽ hiển thị:

.. code-block:: none

   WARNING:root:Look before you leap!

Như bạn có thể thấy, việc hợp nhất dữ liệu biến vào thông báo mô tả sự kiện sử dụng kiểu định dạng chuỗi cũ, theo kiểu %. Điều này nhằm đảm bảo khả năng tương thích ngược: package logging có trước các tùy chọn định dạng mới hơn như
:meth:`str.format` và :class:`string.Template`. Các tùy chọn định dạng mới hơn này *are* được hỗ trợ, nhưng việc tìm hiểu chúng nằm ngoài phạm vi của tutorial này: xem :ref:`formatting-styles` để biết thêm thông tin.


Thay đổi định dạng của các thông báo được hiển thị
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để thay đổi định dạng được sử dụng nhằm hiển thị các thông báo, bạn cần chỉ định định dạng muốn sử dụng::

   import logging
   logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
   logging.debug('This message should appear on the console')
   logging.info('So should this')
   logging.warning('And this, too')

sẽ in ra:

.. code-block:: none

   DEBUG:This message should appear on the console
   INFO:So should this
   WARNING:And this, too

Lưu ý rằng 'root' xuất hiện trong các ví dụ trước đã biến mất. Để xem đầy đủ các thành phần có thể xuất hiện trong chuỗi format, bạn có thể tham khảo tài liệu về :ref:`logrecord-attributes`, nhưng với cách sử dụng đơn giản, bạn chỉ cần *levelname* (mức độ nghiêm trọng), *message* (mô tả sự kiện, bao gồm dữ liệu biến) và có thể thêm thời điểm sự kiện xảy ra. Nội dung này được mô tả trong phần tiếp theo.


Hiển thị ngày/giờ trong thông báo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để hiển thị ngày và giờ của một sự kiện, bạn đặt '%(asctime)s' vào chuỗi format::

   import logging
   logging.basicConfig(format='%(asctime)s %(message)s')
   logging.warning('is when this event was logged.')

khi đó kết quả in ra sẽ tương tự như sau:

.. code-block:: none

   2010-12-12 11:41:42,612 is when this event was logged.

Định dạng mặc định để hiển thị ngày/giờ (như ở trên) tương tự ISO8601 hoặc
:rfc:`3339`. Nếu cần kiểm soát nhiều hơn đối với việc định dạng ngày/giờ, hãy cung cấp đối số *datefmt* cho ``basicConfig``, như trong ví dụ này::

   import logging
   logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
   logging.warning('is when this event was logged.')

khi đó kết quả hiển thị sẽ tương tự như sau:

.. code-block:: none

   12/12/2010 11:46:36 AM is when this event was logged.

Định dạng của đối số *datefmt* giống với định dạng được hỗ trợ bởi
:func:`time.strftime`.


Các bước tiếp theo
^^^^^^^^^^^^^^^^^^

Đến đây là kết thúc phần hướng dẫn cơ bản. Nội dung này hẳn đã đủ để bạn bắt đầu sử dụng logging. Gói logging còn cung cấp nhiều tính năng khác, nhưng để tận dụng tốt nhất, bạn sẽ cần dành thêm một chút thời gian đọc các phần sau. Nếu đã sẵn sàng, hãy lấy một thức uống yêu thích và tiếp tục.

Nếu nhu cầu logging của bạn đơn giản, hãy sử dụng các ví dụ trên để tích hợp logging vào các script của riêng bạn. Nếu gặp vấn đề hoặc không hiểu điều gì, hãy đăng câu hỏi trong danh mục Help của `diễn đàn thảo luận Python <https://discuss.python.org/c/help/7>`_, và bạn sẽ sớm nhận được sự trợ giúp.

Vẫn còn ở đây sao? Bạn có thể tiếp tục đọc vài phần tiếp theo, trong đó có phần hướng dẫn nâng cao và chuyên sâu hơn một chút so với phần cơ bản ở trên. Sau đó, bạn có thể xem qua :ref:`logging-cookbook`.

.. _logging-advanced-tutorial:


Hướng dẫn logging nâng cao
--------------------------

Thư viện logging sử dụng cách tiếp cận theo mô-đun và cung cấp một số nhóm thành phần: logger, handler, filter và formatter.

* Loggers cung cấp giao diện mà mã ứng dụng sử dụng trực tiếp.
* Handlers gửi các bản ghi log (do loggers tạo) đến đích phù hợp.
* Filters cung cấp một cơ chế chi tiết hơn để xác định những bản ghi log nào sẽ được xuất.
* Formatters chỉ định bố cục của các bản ghi log trong đầu ra cuối cùng.

Thông tin về sự kiện log được truyền giữa loggers, handlers, filters và formatters trong một thực thể :class:`LogRecord`.

Logging được thực hiện bằng cách gọi các phương thức trên các thực thể thuộc lớp :class:`Logger` (sau đây gọi là :dfn:`loggers`). Mỗi thực thể có một tên và về mặt khái niệm được sắp xếp theo một hệ phân cấp namespace, sử dụng dấu chấm (dấu chấm câu) làm dấu phân cách. Ví dụ: logger có tên 'scan' là cha của các logger 'scan.text', 'scan.html' và 'scan.pdf'. Tên logger có thể là bất kỳ tên nào bạn muốn và cho biết khu vực của ứng dụng nơi bắt nguồn của thông báo được ghi log.

Một quy ước tốt khi đặt tên logger là sử dụng logger cấp module trong mỗi module có sử dụng logging, được đặt tên như sau::

   logger = logging.getLogger(__name__)

Điều này có nghĩa là tên logger phản ánh hệ thống phân cấp package/module, và chỉ cần nhìn vào tên logger là có thể dễ dàng biết các sự kiện được ghi ở đâu.

Gốc của hệ thống phân cấp logger được gọi là root logger. Đây là logger được các hàm :func:`debug`, :func:`info`, :func:`warning`, sử dụng,
:func:`error` và :func:`critical`, vốn chỉ gọi phương thức cùng tên của root logger. Các hàm và phương thức này có cùng chữ ký. Tên của root logger được in là 'root' trong đầu ra log.

Tất nhiên, bạn có thể ghi thông báo vào các đích khác nhau. Package này hỗ trợ ghi thông báo log vào tệp, các địa chỉ HTTP GET/POST, email qua SMTP, socket chung, queue hoặc các cơ chế logging dành riêng cho hệ điều hành như syslog hoặc Windows NT event log. Các đích được phục vụ bởi các lớp :dfn:`handler`. Bạn có thể tự tạo lớp đích log nếu có yêu cầu đặc biệt mà không lớp handler tích hợp sẵn nào đáp ứng được.

Theo mặc định, không có đích nào được thiết lập cho bất kỳ thông báo log nào. Bạn có thể chỉ định một đích (chẳng hạn như console hoặc tệp) bằng cách sử dụng :func:`basicConfig` như trong các ví dụ của tutorial. Nếu bạn gọi các hàm  :func:`debug`, :func:`info`,
:func:`warning`, :func:`error` và :func:`critical`, chúng sẽ kiểm tra xem có đích nào được thiết lập hay chưa; nếu chưa, chúng sẽ thiết lập console (``sys.stderr``) làm đích và đặt định dạng mặc định cho thông báo được hiển thị, rồi ủy quyền cho root logger thực hiện việc xuất thông báo thực tế.

Định dạng mặc định do :func:`basicConfig` thiết lập cho các thông báo là:

.. code-block:: none

   severity:logger name:message

Bạn có thể thay đổi điều này bằng cách truyền một chuỗi định dạng cho :func:`basicConfig` với đối số từ khóa *format*. Để xem tất cả các tùy chọn liên quan đến cách xây dựng chuỗi định dạng, hãy xem :ref:`formatter-objects`.

Luồng ghi log
^^^^^^^^^^^^^

Luồng thông tin của sự kiện log trong các logger và handler được minh họa trong sơ đồ sau.

.. only:: not html

   .. image:: logging_flow.*

.. raw:: html
   :file: logging_flow.svg


.. raw:: html

   <script>
   /*
    * This snippet is needed to handle the case where a light or dark theme is
    * chosen via the theme is selected in the page. We call the existing handler
    * and then add a dark-theme class to the body when the dark theme is selected.
    * The SVG styling (above) then does the rest.
    *
    * If the pydoc theme is updated to set the dark-theme class, this snippet
    * won't be needed any more.
    */
   (function() {
     var oldActivateTheme = activateTheme;

     function updateBody(theme) {
        let elem = document.body;

        elem.classList.remove('dark-theme');
        elem.classList.remove('light-theme');
        if (theme === 'dark') {
            elem.classList.add('dark-theme');
        }
        else if (theme === 'light') {
            elem.classList.add('light-theme');
        }
     }

     activateTheme = function(theme) {
        oldActivateTheme(theme);
        updateBody(theme);
     };
     /*
      * If the page is refreshed, make sure we update the body - the overriding
      * of activateTheme won't have taken effect yet.
      */
      updateBody(localStorage.getItem('currentTheme') || 'auto');
   })();
   </script>

Logger
^^^^^^

Các đối tượng :class:`Logger` có ba nhiệm vụ. Thứ nhất, chúng cung cấp một số phương thức cho mã ứng dụng để các ứng dụng có thể ghi thông báo tại runtime. Thứ hai, các đối tượng logger xác định những thông báo log cần xử lý dựa trên mức độ nghiêm trọng (cơ chế lọc mặc định) hoặc các đối tượng filter. Thứ ba, các đối tượng logger chuyển tiếp những thông báo log liên quan đến tất cả log handler quan tâm.

Các phương thức được sử dụng phổ biến nhất trên các đối tượng logger thuộc hai loại: cấu hình và gửi thông báo.

Sau đây là các phương thức cấu hình phổ biến nhất:

* :meth:`Logger.setLevel` chỉ định thông báo log có mức độ nghiêm trọng thấp nhất mà logger sẽ xử lý, trong đó debug là mức độ nghiêm trọng tích hợp thấp nhất và critical là mức độ nghiêm trọng tích hợp cao nhất. Ví dụ: nếu mức độ nghiêm trọng là INFO, logger sẽ chỉ xử lý các thông báo INFO, WARNING, ERROR và CRITICAL, đồng thời bỏ qua các thông báo DEBUG.

* :meth:`Logger.addHandler` và :meth:`Logger.removeHandler` thêm và xóa các đối tượng handler khỏi đối tượng logger. Các handler được trình bày chi tiết hơn trong :ref:`handler-basic`.

* :meth:`Logger.addFilter` và :meth:`Logger.removeFilter` thêm và xóa các đối tượng filter khỏi đối tượng logger. Các filter được trình bày chi tiết hơn trong
  :ref:`filter`.

Bạn không cần luôn gọi các phương thức này trên mọi logger mà bạn tạo. Hãy xem hai đoạn cuối trong phần này.

Sau khi cấu hình đối tượng logger, các phương thức sau đây sẽ tạo thông báo log:

* :meth:`Logger.debug`, :meth:`Logger.info`, :meth:`Logger.warning`,
  :meth:`Logger.error`, và :meth:`Logger.critical` đều tạo các bản ghi log với một thông báo và một cấp độ tương ứng với tên phương thức. Thông báo thực chất là một chuỗi định dạng, có thể chứa cú pháp thay thế chuỗi tiêu chuẩn của ``%s``, ``%d``, ``%f``, v.v. Các đối số còn lại của chúng là danh sách các đối tượng tương ứng với các trường thay thế trong thông báo. Đối với ``**kwargs``, các phương thức logging chỉ quan tâm đến một từ khóa là ``exc_info`` và sử dụng từ khóa này để xác định có ghi thông tin ngoại lệ hay không.

* :meth:`Logger.exception` tạo một thông báo log tương tự như
  :meth:`Logger.error`. Điểm khác biệt là :meth:`Logger.exception` kết xuất stack trace cùng với nó. Chỉ gọi phương thức này từ một exception handler.

* :meth:`Logger.log` nhận log level làm đối số tường minh. Cách này dài dòng hơn một chút khi ghi các thông báo log so với việc sử dụng những phương thức tiện ích cho log level được liệt kê ở trên, nhưng đây là cách ghi log ở các log level tùy chỉnh.

:func:`getLogger` trả về một tham chiếu đến instance logger có tên được chỉ định nếu tên đó được cung cấp, hoặc ``root`` nếu không. Tên có cấu trúc phân cấp, được phân tách bằng dấu chấm. Nhiều lần gọi :func:`getLogger` với cùng một tên sẽ trả về tham chiếu đến cùng một đối tượng logger. Các logger nằm sâu hơn trong danh sách phân cấp là con của những logger nằm cao hơn trong danh sách. Ví dụ, với một logger có tên ``foo``, các logger có tên ``foo.bar``, ``foo.bar.baz`` và ``foo.bam`` đều là hậu duệ của ``foo``.

Logger có khái niệm *mức hiệu lực*. Nếu một level không được thiết lập tường minh trên logger, level của logger cha sẽ được dùng làm mức hiệu lực của nó. Nếu logger cha không có level được thiết lập tường minh, *cha của nó* sẽ được kiểm tra, và tiếp tục như vậy — tất cả các logger tổ tiên đều được tìm kiếm cho đến khi tìm thấy một level được thiết lập tường minh. Root logger luôn có một level được thiết lập tường minh (``WARNING`` theo mặc định). Khi quyết định có xử lý một sự kiện hay không, mức hiệu lực của logger được dùng để xác định liệu sự kiện có được chuyển đến các handler của logger hay không.

Các logger con truyền các thông báo lên các handler được liên kết với những logger tổ tiên của chúng. Vì vậy, không cần định nghĩa và cấu hình handler cho tất cả logger mà ứng dụng sử dụng. Chỉ cần cấu hình handler cho một logger cấp cao nhất và tạo các logger con khi cần. (Tuy nhiên, bạn có thể tắt cơ chế truyền này bằng cách đặt thuộc tính *propagate* của logger thành ``False``.)


.. _handler-basic:

Handlers
^^^^^^^^

Các đối tượng :class:`~logging.Handler` chịu trách nhiệm phân phối những thông báo log phù hợp (dựa trên mức độ nghiêm trọng của thông báo log) đến đích được chỉ định của handler. Các đối tượng :class:`Logger` có thể tự thêm không hoặc nhiều đối tượng handler bằng phương thức :meth:`~Logger.addHandler`. Ví dụ, một ứng dụng có thể muốn gửi tất cả thông báo log đến một tệp log, tất cả thông báo log có mức error trở lên đến stdout và tất cả thông báo có mức critical đến một địa chỉ email. Kịch bản này yêu cầu ba handler riêng lẻ, trong đó mỗi handler chịu trách nhiệm gửi các thông báo có một mức độ nghiêm trọng cụ thể đến một vị trí cụ thể.

Thư viện chuẩn bao gồm khá nhiều loại handler (xem
:ref:`useful-handlers`); các tutorial chủ yếu sử dụng :class:`StreamHandler` và
:class:`FileHandler` trong các ví dụ của mình.

Có rất ít phương thức trong một handler mà các nhà phát triển ứng dụng cần quan tâm. Chỉ có những phương thức của handler có vẻ phù hợp với các nhà phát triển ứng dụng đang sử dụng các đối tượng handler tích hợp sẵn (tức là không tạo handler tùy chỉnh) là các phương thức cấu hình sau:

* Phương thức :meth:`~Handler.setLevel`, giống như trong các đối tượng logger, chỉ định mức độ nghiêm trọng thấp nhất sẽ được chuyển đến đích tương ứng. Tại sao lại có hai phương thức :meth:`~Handler.setLevel`? Mức được đặt trong logger xác định mức độ nghiêm trọng của các thông báo mà logger sẽ chuyển cho các handler. Mức được đặt trong mỗi handler xác định những thông báo mà handler đó sẽ gửi đi.

* :meth:`~Handler.setFormatter` chọn một đối tượng Formatter để handler này sử dụng.

* :meth:`~Handler.addFilter` và :meth:`~Handler.removeFilter` lần lượt cấu hình và hủy cấu hình các đối tượng filter trên các handler.

Mã ứng dụng không nên trực tiếp khởi tạo và sử dụng các thể hiện của
:class:`Handler`.  Thay vào đó, lớp :class:`Handler` là một lớp cơ sở định nghĩa giao diện mà tất cả handler cần có, đồng thời thiết lập một số hành vi mặc định mà các lớp con có thể sử dụng (hoặc ghi đè).


Formatter
^^^^^^^^^

Các đối tượng formatter cấu hình thứ tự, cấu trúc và nội dung cuối cùng của thông báo log.  Không giống lớp cơ sở :class:`logging.Handler`, mã ứng dụng có thể khởi tạo các lớp formatter, mặc dù nhiều khả năng bạn có thể tạo lớp con của formatter nếu ứng dụng cần hành vi đặc biệt.  Hàm khởi tạo nhận ba đối số tùy chọn -- một chuỗi định dạng thông báo, một chuỗi định dạng ngày và một chỉ báo style.

.. method:: logging.Formatter.__init__(fmt=None, datefmt=None, style='%')

Nếu không có chuỗi định dạng thông báo, mặc định là sử dụng thông báo thô.  Nếu không có chuỗi định dạng ngày, định dạng ngày mặc định là:

.. code-block:: none

    %Y-%m-%d %H:%M:%S

với phần mili giây được nối thêm ở cuối. ``style`` là một trong ``'%'``, ``'{'`` hoặc ``'$'``. Nếu không chỉ định một trong các giá trị này, thì ``'%'`` sẽ được sử dụng.

Nếu ``style`` là ``'%'``, chuỗi định dạng thông báo sử dụng phép thay thế chuỗi theo style ``%(<dictionary key>)s``; các khóa có thể sử dụng được ghi lại trong :ref:`logrecord-attributes`. Nếu style là ``'{'``, chuỗi định dạng thông báo được giả định là tương thích với :meth:`str.format` (sử dụng các đối số từ khóa), còn nếu style là ``'$'`` thì chuỗi định dạng thông báo phải tuân theo định dạng mà :meth:`string.Template.substitute` yêu cầu.

.. versionchanged:: 3.2
   Đã thêm tham số ``style``.

Chuỗi định dạng thông báo sau sẽ ghi nhật ký thời gian theo định dạng dễ đọc, mức độ nghiêm trọng của thông báo và nội dung của thông báo, theo thứ tự đó::

    '%(asctime)s - %(levelname)s - %(message)s'

Formatter sử dụng một hàm do người dùng cấu hình để chuyển đổi thời điểm tạo bản ghi thành một tuple. Theo mặc định, :func:`time.localtime` được sử dụng; để thay đổi tùy theo một instance formatter cụ thể, hãy đặt thuộc tính ``converter`` của instance đó thành một hàm có cùng chữ ký với :func:`time.localtime` hoặc
:func:`time.gmtime`. Để thay đổi cho tất cả formatter, chẳng hạn nếu bạn muốn mọi thời điểm ghi nhật ký đều được hiển thị theo GMT, hãy đặt thuộc tính ``converter`` trong lớp Formatter (thành ``time.gmtime`` để hiển thị theo GMT).


Cấu hình Logging
^^^^^^^^^^^^^^^^

.. currentmodule:: logging.config

Lập trình viên có thể cấu hình logging theo ba cách:

1. Tạo tường minh các logger, handler và formatter bằng mã Python gọi các phương thức cấu hình được liệt kê ở trên.
2. Tạo tệp cấu hình logging và đọc tệp đó bằng hàm :func:`fileConfig`.
3. Tạo một dictionary chứa thông tin cấu hình và truyền nó vào hàm :func:`dictConfig`.

Để xem tài liệu tham khảo về hai tùy chọn cuối cùng, hãy xem
:ref:`logging-config-api`. Ví dụ sau đây cấu hình một logger rất đơn giản, một console handler và một formatter đơn giản bằng mã Python::

    import logging

    # tạo logger
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)

    # tạo console handler và đặt level thành debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # tạo formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # thêm formatter vào ch
    ch.setFormatter(formatter)

    # thêm ch vào logger
    logger.addHandler(ch)

    # mã 'application'
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

Chạy module này từ dòng lệnh sẽ tạo ra kết quả sau:

.. code-block:: shell-session

    $ python simple_logging_module.py
    2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
    2005-03-19 15:10:26,620 - simple_example - INFO - info message
    2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
    2005-03-19 15:10:26,697 - simple_example - ERROR - error message
    2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message

Module Python sau đây tạo một logger, handler và formatter gần như giống hệt những thành phần trong ví dụ ở trên, điểm khác biệt duy nhất là tên của các đối tượng::

    import logging
    import logging.config

    logging.config.fileConfig('logging.conf')

    # tạo logger
    logger = logging.getLogger('simpleExample')

    # mã 'application'
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

Đây là tệp logging.conf:

.. code-block:: ini

    [loggers]
    keys=root,simpleExample

    [handlers]
    keys=consoleHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=DEBUG
    handlers=consoleHandler

    [logger_simpleExample]
    level=DEBUG
    handlers=consoleHandler
    qualname=simpleExample
    propagate=0

    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=simpleFormatter
    args=(sys.stdout,)

    [formatter_simpleFormatter]
    format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

Kết quả gần như giống hệt kết quả của ví dụ không dựa trên tệp cấu hình:

.. code-block:: shell-session

    $ python simple_logging_config.py
    2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
    2005-03-19 15:38:55,979 - simpleExample - INFO - info message
    2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
    2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
    2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message

Bạn có thể thấy cách tiếp cận bằng tệp cấu hình có một số ưu điểm so với cách tiếp cận bằng mã Python, chủ yếu là tách biệt cấu hình và mã, cũng như cho phép những người không viết mã dễ dàng sửa đổi các thuộc tính logging.

.. warning:: Hàm :func:`fileConfig` nhận một tham số mặc định là ``disable_existing_loggers``, với giá trị mặc định là ``True`` vì lý do tương thích ngược. Đây có thể là điều bạn muốn hoặc không, vì nó sẽ khiến mọi logger không phải root tồn tại trước lời gọi :func:`fileConfig` bị vô hiệu hóa, trừ khi chúng (hoặc một logger tổ tiên) được nêu rõ trong cấu hình. Vui lòng tham khảo tài liệu tham chiếu để biết thêm thông tin và chỉ định ``False`` cho tham số này nếu bạn muốn.

   Dictionary được truyền vào :func:`dictConfig` cũng có thể chỉ định một giá trị Boolean với khóa ``disable_existing_loggers``; nếu không được chỉ định rõ ràng trong dictionary, giá trị này cũng mặc định được diễn giải là ``True``. Điều này dẫn đến hành vi vô hiệu hóa logger được mô tả ở trên, có thể không phải điều bạn muốn — trong trường hợp đó, hãy cung cấp khóa này một cách rõ ràng với giá trị ``False``.


.. currentmodule:: logging

Lưu ý rằng tên lớp được tham chiếu trong các tệp cấu hình cần là tên tương đối với module logging hoặc là các giá trị tuyệt đối có thể được phân giải bằng các cơ chế import thông thường. Vì vậy, bạn có thể sử dụng một trong hai cách sau:
:class:`~logging.handlers.WatchedFileHandler` (tương đối với module logging) hoặc ``mypackage.mymodule.MyHandler`` (dành cho một lớp được định nghĩa trong package ``mypackage`` và module ``mymodule``, trong đó ``mypackage`` có sẵn trên Python import path).

Trong Python 3.2, một phương thức mới để cấu hình logging đã được giới thiệu, sử dụng các dictionary để lưu thông tin cấu hình. Phương thức này cung cấp một tập chức năng bao quát hơn so với cách tiếp cận dựa trên tệp cấu hình được trình bày ở trên, và là phương thức cấu hình được khuyến nghị cho các ứng dụng và hoạt động triển khai mới. Vì một dictionary trong Python được dùng để lưu thông tin cấu hình, đồng thời bạn có thể điền dictionary đó bằng nhiều cách khác nhau, nên bạn có nhiều lựa chọn hơn khi cấu hình. Ví dụ: bạn có thể sử dụng tệp cấu hình ở định dạng JSON hoặc, nếu có quyền truy cập vào chức năng xử lý YAML, một tệp ở định dạng YAML để điền dictionary cấu hình. Hoặc tất nhiên, bạn có thể tạo dictionary trong mã Python, nhận dictionary ở dạng pickled qua socket, hoặc sử dụng bất kỳ phương pháp nào phù hợp với ứng dụng của mình.

Dưới đây là ví dụ về cấu hình tương tự như trên, ở định dạng YAML cho phương thức mới dựa trên dictionary:

.. code-block:: yaml

    version: 1
    formatters:
      simple:
        format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple
        stream: ext://sys.stdout
    loggers:
      simpleExample:
        level: DEBUG
        handlers: [console]
        propagate: no
    root:
      level: DEBUG
      handlers: [console]

Để biết thêm thông tin về việc sử dụng dictionary cho logging, hãy xem
:ref:`logging-config-api`.

Điều gì xảy ra nếu không cung cấp cấu hình
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu không cung cấp cấu hình logging, có thể xảy ra trường hợp một sự kiện logging cần được xuất ra nhưng không tìm thấy handler nào để xuất sự kiện đó.

Sự kiện được xuất ra bằng một 'handler dự phòng cuối cùng', được lưu trong
:data:`lastResort`. Handler nội bộ này không được liên kết với bất kỳ logger nào và hoạt động như một :class:`~logging.StreamHandler`, ghi thông báo mô tả sự kiện vào giá trị hiện tại của ``sys.stderr`` (do đó tuân theo mọi chuyển hướng đang có hiệu lực). Thông báo không được định dạng — chỉ thông báo mô tả sự kiện nguyên bản được in ra. Mức của handler được đặt thành ``WARNING``, vì vậy tất cả các sự kiện có mức độ nghiêm trọng này hoặc cao hơn sẽ được xuất ra.

.. versionchanged:: 3.2

   Đối với các phiên bản Python trước 3.2, hành vi như sau:

   * Nếu :data:`raiseExceptions` là ``False`` (chế độ production), sự kiện sẽ bị loại bỏ một cách im lặng.

   * Nếu :data:`raiseExceptions` là ``True`` (chế độ development), một thông báo 'No handlers could be found for logger X.Y.Z' sẽ được in ra một lần.

   Để có được hành vi trước phiên bản 3.2,
   :data:`lastResort` có thể được đặt thành ``None``.

.. _library-config:

Cấu hình Logging cho một Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi phát triển một library sử dụng logging, bạn nên chú ý ghi lại cách library sử dụng logging — chẳng hạn như tên của các logger được sử dụng. Cũng cần cân nhắc đến cấu hình logging của library. Nếu ứng dụng sử dụng library không dùng logging nhưng mã của library lại thực hiện các lệnh gọi logging, thì (như đã mô tả trong phần trước) các sự kiện có mức độ nghiêm trọng ``WARNING`` trở lên sẽ được in ra ``sys.stderr``. Đây được xem là hành vi mặc định tốt nhất.

Nếu vì một lý do nào đó bạn *không* muốn các thông báo này được in ra khi chưa có cấu hình logging, bạn có thể gắn một handler không thực hiện thao tác nào vào logger cấp cao nhất dành cho thư viện của mình. Việc này ngăn thông báo được in ra, vì một handler sẽ luôn được tìm thấy cho các sự kiện của thư viện: chỉ là handler đó không tạo ra bất kỳ đầu ra nào. Nếu người dùng thư viện cấu hình logging để dùng cho ứng dụng, có lẽ cấu hình đó sẽ thêm một số handler, và nếu các level được cấu hình phù hợp thì những lời gọi logging trong mã thư viện sẽ gửi đầu ra đến các handler đó như bình thường.

Một handler không thực hiện thao tác nào được cung cấp trong package logging:
:class:`~logging.NullHandler` (kể từ Python 3.1). Một instance của handler này có thể được thêm vào logger cấp cao nhất của namespace logging được thư viện sử dụng (*nếu* bạn muốn ngăn các sự kiện được ghi log bởi thư viện của mình được xuất ra ``sys.stderr`` khi chưa có cấu hình logging). Nếu toàn bộ hoạt động logging của một thư viện *foo* được thực hiện bằng các logger có tên khớp với 'foo.x', 'foo.x.y', v.v. thì mã nguồn::

    import logging
    logging.getLogger('foo').addHandler(logging.NullHandler())

sẽ có tác dụng như mong muốn. Nếu một tổ chức phát triển nhiều thư viện, tên logger được chỉ định có thể là 'orgname.foo' thay vì chỉ 'foo'.

.. note:: Bạn được khuyến cáo mạnh mẽ *không ghi log vào root logger* trong thư viện của mình. Thay vào đó, hãy sử dụng một logger có tên duy nhất và dễ nhận biết, chẳng hạn như ``__name__`` cho package hoặc module cấp cao nhất của thư viện. Việc ghi log vào root logger sẽ khiến nhà phát triển ứng dụng khó hoặc không thể cấu hình mức độ chi tiết của logging hay các handler của thư viện theo mong muốn.

.. note:: Bạn được khuyến cáo mạnh mẽ *không thêm bất kỳ handler nào khác ngoài* :class:`~logging.NullHandler` *vào các logger của thư viện*. Lý do là việc cấu hình handler thuộc quyền quyết định của nhà phát triển ứng dụng sử dụng thư viện của bạn. Nhà phát triển ứng dụng hiểu rõ đối tượng người dùng mục tiêu và những handler nào phù hợp nhất với ứng dụng của họ: nếu bạn âm thầm thêm handler, bạn có thể cản trở khả năng thực hiện unit test và cung cấp các log đáp ứng yêu cầu của họ.


Các mức độ Logging
------------------

Giá trị số của các mức độ ghi log được nêu trong bảng sau. Những giá trị này chủ yếu đáng quan tâm nếu bạn muốn định nghĩa các mức độ riêng và cần chúng có các giá trị cụ thể tương quan với những mức độ được định nghĩa sẵn. Nếu bạn định nghĩa một mức độ có cùng giá trị số, mức độ được định nghĩa sẵn sẽ bị ghi đè; tên được định nghĩa sẵn sẽ bị mất.

+--------------+------------+
| Mức độ       | Giá trị số |
+==============+============+
| ``CRITICAL`` | 50         |
+--------------+------------+
| ``ERROR``    | 40         |
+--------------+------------+
| ``WARNING``  | 30         |
+--------------+------------+
| ``INFO``     | 20         |
+--------------+------------+
| ``DEBUG``    | 10         |
+--------------+------------+
| ``NOTSET``   | 0          |
+--------------+------------+

Các mức độ cũng có thể được liên kết với logger, được thiết lập bởi developer hoặc thông qua việc tải cấu hình ghi log đã lưu. Khi một phương thức ghi log được gọi trên logger, logger sẽ so sánh mức độ của chính nó với mức độ được liên kết với lời gọi phương thức. Nếu mức độ của logger cao hơn mức độ của lời gọi phương thức, thực tế sẽ không có thông báo log nào được tạo ra. Đây là cơ chế cơ bản kiểm soát mức độ chi tiết của đầu ra ghi log.

Các thông báo log được mã hóa dưới dạng các instance của lớp :class:`~logging.LogRecord`. Khi một logger quyết định thực sự ghi log một sự kiện, một
instance :class:`~logging.LogRecord` được tạo từ thông báo log.

Các thông báo log được đưa qua một cơ chế dispatch bằng cách sử dụng
:dfn:`handlers`, là các thể hiện của các lớp con của lớp :class:`Handler`. Các handler chịu trách nhiệm đảm bảo rằng một thông báo đã được ghi (dưới dạng :class:`LogRecord`) được đưa đến một vị trí cụ thể (hoặc một tập hợp vị trí) hữu ích cho đối tượng mục tiêu của thông báo đó (chẳng hạn như người dùng cuối, nhân viên bộ phận hỗ trợ, quản trị viên hệ thống, nhà phát triển). Các handler được truyền
:class:`LogRecord` các thể hiện dành cho những đích cụ thể. Mỗi logger có thể không có, có một hoặc có nhiều handler được liên kết với nó (thông qua phương thức
:meth:`~Logger.addHandler` của :class:`Logger`). Ngoài mọi handler được liên kết trực tiếp với một logger, *tất cả các handler được liên kết với mọi logger cấp trên của logger* đều được gọi để điều phối thông báo (trừ khi cờ *propagate* của logger được đặt thành giá trị false; khi đó, việc chuyển tiếp đến các handler cấp trên sẽ dừng lại).

Cũng như logger, handler có thể được gán các level. Level của handler hoạt động như một bộ lọc theo cùng cách với level của logger. Nếu một handler quyết định thực sự điều phối một sự kiện, phương thức :meth:`~Handler.emit` được dùng để gửi thông báo đến đích của nó. Hầu hết các lớp con của
:class:`Handler` do người dùng định nghĩa sẽ cần ghi đè :meth:`~Handler.emit` này.

.. _custom-levels:

Các level tùy chỉnh
^^^^^^^^^^^^^^^^^^^

Bạn có thể tự định nghĩa các level, nhưng điều này không cần thiết vì các level hiện có đã được lựa chọn dựa trên kinh nghiệm thực tế. Tuy nhiên, nếu bạn tin chắc rằng mình cần các level tùy chỉnh, hãy hết sức thận trọng khi thực hiện, và có thể *việc định nghĩa các level tùy chỉnh là một ý tưởng rất tồi nếu bạn đang phát triển một thư viện*. Đó là vì nếu nhiều tác giả thư viện cùng định nghĩa các level tùy chỉnh riêng, đầu ra logging từ những thư viện đó khi được sử dụng cùng nhau có thể sẽ khó kiểm soát và/hoặc diễn giải đối với nhà phát triển sử dụng chúng, bởi vì cùng một giá trị số có thể mang những ý nghĩa khác nhau trong các thư viện khác nhau.

.. _useful-handlers:

Các Handler hữu ích
-------------------

Ngoài lớp cơ sở :class:`Handler`, còn cung cấp nhiều lớp con hữu ích:

#. Các thực thể :class:`StreamHandler` gửi thông báo đến các stream (đối tượng giống tệp).

#. Các thực thể :class:`FileHandler` gửi thông báo đến các tệp trên đĩa.

#. :class:`~handlers.BaseRotatingHandler` là lớp cơ sở cho các Handler thực hiện xoay tệp nhật ký tại một thời điểm nhất định. Lớp này không предназнач để được khởi tạo trực tiếp. Thay vào đó, hãy sử dụng :class:`~handlers.RotatingFileHandler` hoặc
   :class:`~handlers.TimedRotatingFileHandler`.

#. Các thực thể :class:`~handlers.RotatingFileHandler` gửi thông báo đến các tệp trên đĩa, hỗ trợ kích thước tệp nhật ký tối đa và xoay tệp nhật ký.

#. Các thực thể :class:`~handlers.TimedRotatingFileHandler` gửi thông báo đến các tệp trên đĩa, xoay tệp nhật ký theo các khoảng thời gian nhất định.

#. Các instance :class:`~handlers.SocketHandler` gửi thông báo đến socket TCP/IP. Kể từ phiên bản 3.4, Unix domain socket cũng được hỗ trợ.

#. Các instance :class:`~handlers.DatagramHandler` gửi thông báo đến socket UDP. Kể từ phiên bản 3.4, Unix domain socket cũng được hỗ trợ.

#. Các instance :class:`~handlers.SMTPHandler` gửi thông báo đến một địa chỉ email được chỉ định.

#. Các instance :class:`~handlers.SysLogHandler` gửi thông báo đến daemon syslog Unix, có thể nằm trên một máy từ xa.

#. Các instance :class:`~handlers.NTEventLogHandler` gửi thông báo đến event log của Windows NT/2000/XP.

#. Các instance :class:`~handlers.MemoryHandler` gửi thông báo đến một bộ đệm trong bộ nhớ; bộ đệm này được flush bất cứ khi nào các tiêu chí cụ thể được đáp ứng.

#. Các instance :class:`~handlers.HTTPHandler` gửi thông báo đến máy chủ HTTP bằng ngữ nghĩa ``GET`` hoặc ``POST``.

#. Các instance :class:`~handlers.WatchedFileHandler` theo dõi tệp mà chúng ghi log vào. Nếu tệp thay đổi, tệp sẽ được đóng và mở lại bằng tên tệp đó. Handler này chỉ hữu ích trên các hệ thống tương tự Unix; Windows không hỗ trợ cơ chế nền tảng được sử dụng.

#. Các instance :class:`~handlers.QueueHandler` gửi thông báo vào một queue, chẳng hạn như các queue được triển khai trong các module :mod:`queue` hoặc :mod:`multiprocessing`.

#. Các instance :class:`NullHandler` không xử lý các thông báo lỗi. Chúng được các nhà phát triển thư viện sử dụng khi muốn dùng logging nhưng muốn tránh thông báo 'No handlers could be found for logger *XXX*', vốn có thể xuất hiện nếu người dùng thư viện chưa cấu hình logging. Xem :ref:`library-config` để biết thêm thông tin.

.. versionadded:: 3.1
   Lớp :class:`NullHandler`.

.. versionadded:: 3.2
   Lớp :class:`~handlers.QueueHandler`.

Các lớp :class:`NullHandler`, :class:`StreamHandler` và :class:`FileHandler` được định nghĩa trong gói logging cốt lõi. Các handler khác được định nghĩa trong một module con, :mod:`logging.handlers`. (Ngoài ra còn có một module con khác, :mod:`logging.config`, dành cho chức năng cấu hình.)

Các thông báo log được định dạng để trình bày thông qua các instance của
lớp :class:`Formatter`. Chúng được khởi tạo bằng một chuỗi định dạng thích hợp để sử dụng với toán tử % và một dictionary.

Để định dạng nhiều thông báo theo một batch, có thể sử dụng các instance của
:class:`BufferingFormatter`. Ngoài chuỗi định dạng (được áp dụng cho từng thông báo trong batch), còn có các chuỗi định dạng cho phần header và trailer.

Khi việc lọc dựa trên level của logger và/hoặc level của handler là chưa đủ, có thể thêm các instance của :class:`Filter` vào cả :class:`Logger` và
các instance của :class:`Handler` (thông qua method :meth:`~Handler.addFilter` của chúng). Trước khi quyết định xử lý tiếp một thông báo, cả logger và handler đều kiểm tra tất cả filter của mình để xác định quyền xử lý. Nếu bất kỳ filter nào trả về giá trị false, thông báo sẽ không được xử lý tiếp.

Chức năng cơ bản của :class:`Filter` cho phép lọc theo tên logger cụ thể. Nếu sử dụng tính năng này, các thông báo được gửi đến logger có tên đó và các logger con của nó sẽ được filter cho phép, còn tất cả các thông báo khác sẽ bị loại bỏ.


.. _logging-exceptions:

Các exception phát sinh trong quá trình logging
-----------------------------------------------

Gói logging được thiết kế để nuốt các ngoại lệ xảy ra trong quá trình ghi nhật ký ở môi trường production. Điều này nhằm bảo đảm các lỗi xảy ra khi xử lý các sự kiện ghi nhật ký
- chẳng hạn như cấu hình logging sai, lỗi mạng hoặc các lỗi tương tự khác - không
khiến ứng dụng sử dụng logging kết thúc sớm.

Các ngoại lệ :class:`SystemExit` và :class:`KeyboardInterrupt` không bao giờ bị nuốt. Các ngoại lệ khác xảy ra trong phương thức :meth:`~Handler.emit` của một lớp con :class:`Handler` sẽ được chuyển đến phương thức :meth:`~Handler.handleError` của lớp đó.

Cài đặt mặc định của :meth:`~Handler.handleError` trong :class:`Handler` kiểm tra xem một biến cấp mô-đun, :data:`raiseExceptions`, có được thiết lập hay không. Nếu được thiết lập, một traceback sẽ được in ra :data:`sys.stderr`. Nếu không, ngoại lệ sẽ bị nuốt.

.. note::
   Giá trị mặc định của :data:`raiseExceptions` là ``True``. Điều này là vì trong quá trình phát triển, bạn thường muốn được thông báo về mọi ngoại lệ xảy ra. Bạn nên đặt :data:`raiseExceptions` thành ``False`` khi sử dụng trong môi trường production.

.. currentmodule:: logging

.. _arbitrary-object-messages:

Sử dụng các đối tượng tùy ý làm thông điệp
------------------------------------------

Trong các phần và ví dụ trước, ta giả định rằng thông điệp được truyền khi ghi nhật ký sự kiện là một chuỗi. Tuy nhiên, đây không phải là khả năng duy nhất. Bạn có thể truyền một đối tượng tùy ý làm thông điệp, và
:meth:`~object.__str__` sẽ được gọi khi hệ thống ghi nhật ký cần chuyển đối tượng đó thành dạng biểu diễn chuỗi. Thực tế, nếu muốn, bạn có thể hoàn toàn tránh việc tính toán dạng biểu diễn chuỗi - ví dụ như
:class:`~handlers.SocketHandler` phát ra một event bằng cách pickle đối tượng đó rồi gửi qua mạng.


Tối ưu hóa
----------

Việc định dạng các đối số của thông điệp được trì hoãn cho đến khi không thể tránh khỏi. Tuy nhiên, việc tính toán các đối số truyền cho phương thức ghi nhật ký cũng có thể tốn kém, và bạn có thể muốn tránh thực hiện việc đó nếu logger chỉ loại bỏ sự kiện của bạn. Để quyết định cần làm gì, bạn có thể gọi
:meth:`~Logger.isEnabledFor`, một phương thức nhận đối số level và trả về true nếu Logger sẽ tạo sự kiện cho level gọi đó. Bạn có thể viết mã như sau::

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Message with %s, %s', expensive_func1(),
                                            expensive_func2())

để nếu ngưỡng của logger được đặt cao hơn ``DEBUG``, các lệnh gọi tới ``expensive_func1`` và ``expensive_func2`` sẽ không bao giờ được thực hiện.

.. note:: Trong một số trường hợp, :meth:`~Logger.isEnabledFor` có thể tốn nhiều chi phí hơn mức bạn mong muốn (ví dụ: với các logger lồng nhau sâu, trong đó level tường minh chỉ được thiết lập ở vị trí cao trong hệ thống phân cấp logger). Trong những trường hợp như vậy (hoặc nếu bạn muốn tránh gọi một method trong các vòng lặp chặt), bạn có thể lưu kết quả của một lần gọi :meth:`~Logger.isEnabledFor` vào một biến cục bộ hoặc biến instance, rồi sử dụng kết quả đó thay vì gọi method mỗi lần. Giá trị được lưu trong cache này chỉ cần được tính toán lại khi cấu hình logging thay đổi động trong lúc ứng dụng đang chạy (điều này không thường xuyên xảy ra).

Có thể thực hiện các tối ưu hóa khác cho những ứng dụng cụ thể cần kiểm soát chính xác hơn thông tin logging được thu thập. Sau đây là danh sách những việc bạn có thể làm để tránh thực hiện các thao tác xử lý logging không cần thiết:

+--------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Thông tin bạn không muốn thu thập                                                    | Cách tránh thu thập thông tin đó                                                                                                                                                         |
+======================================================================================+==========================================================================================================================================================================================+
| Thông tin về nơi các lần gọi được thực hiện.                                         | Đặt ``logging._srcfile`` thành ``None``. Cách này tránh việc gọi :func:`sys._getframe`, có thể giúp tăng tốc mã của bạn trong các môi trường như PyPy (vốn không thể tăng tốc mã sử dụng |
|                                                                                      | :func:`sys._getframe`).                                                                                                                                                                  |
+--------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Thông tin về threading.                                                              | Đặt ``logging.logThreads`` thành ``False``.                                                                                                                                              |
+--------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ID tiến trình hiện tại (:func:`os.getpid`) chỉ muốn thu thập                         | Đặt ``logging.logProcesses`` thành ``False``.                                                                                                                                            |
+--------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tên tiến trình hiện tại khi sử dụng ``multiprocessing`` để quản lý nhiều tiến trình. | Đặt ``logging.logMultiprocessing`` thành ``False``.                                                                                                                                      |
+--------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tên :class:`asyncio.Task` hiện tại khi sử dụng ``asyncio``.                          | Đặt ``logging.logAsyncioTasks`` thành ``False``.                                                                                                                                         |
+--------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Cũng lưu ý rằng mô-đun logging cốt lõi chỉ bao gồm các handler cơ bản. Nếu bạn không import :mod:`logging.handlers` và :mod:`logging.config`, chúng sẽ không chiếm dụng bộ nhớ.

.. _tutorial-ref-links:

Tài nguyên khác
---------------

.. seealso::

   Mô-đun :mod:`logging`
      Tài liệu tham khảo API cho mô-đun logging.

   Mô-đun :mod:`logging.config`
      API cấu hình cho mô-đun logging.

   Mô-đun :mod:`logging.handlers`
      Các handler hữu ích được tích hợp trong module logging.

   :ref:`Sổ tay hướng dẫn logging <logging-cookbook>`

.. _`Python discussion forum`: https://discuss.python.org/c/help/7
