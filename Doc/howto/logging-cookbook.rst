.. _logging-cookbook:

==============
Sổ tay Logging
==============

:Author: Vinay Sajip <vinay_sajip at red-dove dot com>

Trang này chứa một số công thức liên quan đến logging đã được chứng minh là hữu ích trong thực tế. Để xem các liên kết đến thông tin hướng dẫn và tham khảo, vui lòng xem
:ref:`cookbook-ref-links`.

.. currentmodule:: logging

Sử dụng logging trong nhiều module
----------------------------------

Nhiều lần gọi ``logging.getLogger('someLogger')`` sẽ trả về tham chiếu đến cùng một đối tượng logger. Điều này đúng không chỉ trong cùng một module mà còn giữa các module, miễn là chúng nằm trong cùng một tiến trình Python interpreter. Điều này đúng với các tham chiếu đến cùng một đối tượng; ngoài ra, mã ứng dụng có thể định nghĩa và cấu hình một logger cha trong một module, rồi tạo (nhưng không cấu hình) một logger con trong một module riêng biệt, và tất cả các lệnh gọi logger đến logger con sẽ được chuyển tiếp lên logger cha. Dưới đây là một module chính::

    import logging
    import auxiliary_module

    # tạo logger với 'spam_application'
    logger = logging.getLogger('spam_application')
    logger.setLevel(logging.DEBUG)
    # tạo file handler ghi lại cả các thông báo debug
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # tạo console handler với mức log cao hơn
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # tạo formatter và thêm vào các handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # thêm các handler vào logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('creating an instance of auxiliary_module.Auxiliary')
    a = auxiliary_module.Auxiliary()
    logger.info('created an instance of auxiliary_module.Auxiliary')
    logger.info('calling auxiliary_module.Auxiliary.do_something')
    a.do_something()
    logger.info('finished auxiliary_module.Auxiliary.do_something')
    logger.info('calling auxiliary_module.some_function()')
    auxiliary_module.some_function()
    logger.info('done with auxiliary_module.some_function()')

Đây là module hỗ trợ::

    import logging

    # tạo logger
    module_logger = logging.getLogger('spam_application.auxiliary')

    class Auxiliary:
        def __init__(self):
            self.logger = logging.getLogger('spam_application.auxiliary.Auxiliary')
            self.logger.info('creating an instance of Auxiliary')

        def do_something(self):
            self.logger.info('doing something')
            a = 1 + 1
            self.logger.info('done doing something')

    def some_function():
        module_logger.info('received a call to "some_function"')

Kết quả hiển thị như sau:

.. code-block:: none

    2005-03-23 23:47:11,663 - spam_application - INFO -
       creating an instance of auxiliary_module.Auxiliary
    2005-03-23 23:47:11,665 - spam_application.auxiliary.Auxiliary - INFO -
       creating an instance of Auxiliary
    2005-03-23 23:47:11,665 - spam_application - INFO -
       created an instance of auxiliary_module.Auxiliary
    2005-03-23 23:47:11,668 - spam_application - INFO -
       calling auxiliary_module.Auxiliary.do_something
    2005-03-23 23:47:11,668 - spam_application.auxiliary.Auxiliary - INFO -
       doing something
    2005-03-23 23:47:11,669 - spam_application.auxiliary.Auxiliary - INFO -
       done doing something
    2005-03-23 23:47:11,670 - spam_application - INFO -
       finished auxiliary_module.Auxiliary.do_something
    2005-03-23 23:47:11,671 - spam_application - INFO -
       calling auxiliary_module.some_function()
    2005-03-23 23:47:11,672 - spam_application.auxiliary - INFO -
       received a call to 'some_function'
    2005-03-23 23:47:11,673 - spam_application - INFO -
       done with auxiliary_module.some_function()

Ghi log từ nhiều thread
-----------------------

Ghi nhật ký từ nhiều thread không đòi hỏi nỗ lực đặc biệt. Ví dụ sau đây minh họa việc ghi nhật ký từ thread chính (thread ban đầu) và một thread khác::

    import logging
    import threading
    import time

    def worker(arg):
        while not arg['stop']:
            logging.debug('Hi from myfunc')
            time.sleep(0.5)

    def main():
        logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
        info = {'stop': False}
        thread = threading.Thread(target=worker, args=(info,))
        thread.start()
        while True:
            try:
                logging.debug('Hello from main')
                time.sleep(0.75)
            except KeyboardInterrupt:
                info['stop'] = True
                break
        thread.join()

    if __name__ == '__main__':
        main()

Khi chạy, script sẽ in ra nội dung tương tự như sau:

.. code-block:: none

     0 Thread-1 Hi from myfunc
     3 MainThread Hello from main
   505 Thread-1 Hi from myfunc
   755 MainThread Hello from main
  1007 Thread-1 Hi from myfunc
  1507 MainThread Hello from main
  1508 Thread-1 Hi from myfunc
  2010 Thread-1 Hi from myfunc
  2258 MainThread Hello from main
  2512 Thread-1 Hi from myfunc
  3009 MainThread Hello from main
  3013 Thread-1 Hi from myfunc
  3515 Thread-1 Hi from myfunc
  3761 MainThread Hello from main
  4017 Thread-1 Hi from myfunc
  4513 MainThread Hello from main
  4518 Thread-1 Hi from myfunc

Điều này cho thấy đầu ra ghi nhật ký được xen kẽ như mong đợi. Tất nhiên, cách tiếp cận này cũng hoạt động với nhiều thread hơn ví dụ này.

Nhiều handler và formatter
--------------------------

Logger là các đối tượng Python thuần túy. Phương thức :meth:`~Logger.addHandler` không đặt giới hạn tối thiểu hoặc tối đa cho số lượng handler mà bạn có thể thêm. Đôi khi, ứng dụng sẽ cần ghi tất cả thông báo ở mọi mức độ nghiêm trọng vào một tệp văn bản, đồng thời ghi các lỗi trở lên vào console. Để thiết lập việc này, chỉ cần cấu hình các handler thích hợp. Các lệnh ghi nhật ký trong mã ứng dụng vẫn không thay đổi. Sau đây là một sửa đổi nhỏ đối với ví dụ cấu hình đơn giản dựa trên module ở phần trước::

    import logging

    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)
    # tạo file handler ghi cả các thông báo debug
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # tạo console handler với mức ghi nhật ký cao hơn
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # tạo formatter và thêm nó vào các handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # thêm các handler vào logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    # mã 'application'
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

Lưu ý rằng mã 'application' không quan tâm đến việc có nhiều handler. Điều duy nhất thay đổi là việc thêm và cấu hình một handler mới có tên *fh*.

Khả năng tạo các handler mới với bộ lọc có mức độ nghiêm trọng cao hơn hoặc thấp hơn có thể rất hữu ích khi viết và kiểm thử một application. Thay vì sử dụng nhiều câu lệnh ``print`` để debug, hãy sử dụng ``logger.debug``: Không giống các câu lệnh print mà sau này bạn sẽ phải xóa hoặc comment out, các câu lệnh logger.debug có thể vẫn được giữ nguyên trong mã nguồn và ở trạng thái không hoạt động cho đến khi bạn cần chúng lại. Khi đó, thay đổi duy nhất cần thực hiện là sửa mức độ nghiêm trọng của logger và/hoặc handler thành debug.

.. _multiple-destinations:

Ghi log đến nhiều đích
----------------------

Giả sử bạn muốn ghi log ra console và file với các định dạng thông báo khác nhau trong những trường hợp khác nhau. Giả sử bạn muốn ghi các thông báo có mức DEBUG trở lên vào file, còn các thông báo có mức INFO trở lên vào console. Đồng thời, giả sử file cần chứa timestamp, còn các thông báo trên console thì không. Sau đây là cách bạn có thể thực hiện điều này::

   import logging

   # thiết lập logging vào tệp - xem phần trước để biết thêm chi tiết
   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                       datefmt='%m-%d %H:%M',
                       filename='/tmp/myapp.log',
                       filemode='w')
   # định nghĩa một Handler ghi các thông báo INFO trở lên vào sys.stderr
   console = logging.StreamHandler()
   console.setLevel(logging.INFO)
   # đặt một format đơn giản hơn để sử dụng trên console
   formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
   # bảo Handler sử dụng format này
   console.setFormatter(formatter)
   # thêm Handler vào root logger
   logging.getLogger().addHandler(console)

   # Bây giờ, chúng ta có thể ghi log vào root logger hoặc bất kỳ logger nào khác. Trước hết là root...
   logging.info('Jackdaws love my big sphinx of quartz.')

   # Bây giờ, định nghĩa một vài logger khác có thể đại diện cho các khu vực trong
   # ứng dụng:

   logger1 = logging.getLogger('myapp.area1')
   logger2 = logging.getLogger('myapp.area2')

   logger1.debug('Quick zephyrs blow, vexing daft Jim.')
   logger1.info('How quickly daft jumping zebras vex.')
   logger2.warning('Jail zesty vixen who grabbed pay from quack.')
   logger2.error('The five boxing wizards jump quickly.')

Khi chạy đoạn mã này, trên console bạn sẽ thấy

.. code-block:: none

   root        : INFO     Jackdaws love my big sphinx of quartz.
   myapp.area1 : INFO     How quickly daft jumping zebras vex.
   myapp.area2 : WARNING  Jail zesty vixen who grabbed pay from quack.
   myapp.area2 : ERROR    The five boxing wizards jump quickly.

và trong tệp, bạn sẽ thấy nội dung tương tự như sau

.. code-block:: none

   10-22 22:19 root         INFO     Jackdaws love my big sphinx of quartz.
   10-22 22:19 myapp.area1  DEBUG    Quick zephyrs blow, vexing daft Jim.
   10-22 22:19 myapp.area1  INFO     How quickly daft jumping zebras vex.
   10-22 22:19 myapp.area2  WARNING  Jail zesty vixen who grabbed pay from quack.
   10-22 22:19 myapp.area2  ERROR    The five boxing wizards jump quickly.

Như bạn có thể thấy, thông báo DEBUG chỉ xuất hiện trong tệp. Các thông báo khác được gửi đến cả hai đích.

Ví dụ này sử dụng các handler cho console và tệp, nhưng bạn có thể sử dụng bất kỳ số lượng và tổ hợp handler nào mình muốn.

Lưu ý rằng lựa chọn tên tệp nhật ký ``/tmp/myapp.log`` ở trên ngụ ý việc sử dụng vị trí chuẩn dành cho các tệp tạm thời trên hệ thống POSIX. Trên Windows, bạn có thể cần chọn một tên thư mục khác cho nhật ký—chỉ cần đảm bảo thư mục đó tồn tại và bạn có quyền tạo cũng như cập nhật các tệp trong đó.


.. _custom-level-handling:

Tùy chỉnh cách xử lý các cấp độ
-------------------------------

Đôi khi, bạn có thể muốn xử lý hơi khác so với cách xử lý mức độ tiêu chuẩn trong các handler, trong đó mọi mức độ cao hơn một ngưỡng đều được handler xử lý. Để làm điều này, bạn cần sử dụng các filter. Hãy xem một tình huống trong đó bạn muốn sắp xếp mọi thứ như sau:

* Gửi các thông báo có mức độ nghiêm trọng ``INFO`` và ``WARNING`` đến ``sys.stdout``
* Gửi các thông báo có mức độ nghiêm trọng ``ERROR`` trở lên đến ``sys.stderr``
* Gửi các thông báo có mức độ nghiêm trọng ``DEBUG`` trở lên đến tệp ``app.log``

Giả sử bạn cấu hình logging bằng JSON sau:

.. code-block:: json

    {
        "version": 1,
        "disable_existing_loggers": false,
        "formatters": {
            "simple": {
                "format": "%(levelname)-8s - %(message)s"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "simple",
                "stream": "ext://sys.stderr"
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "filename": "app.log",
                "mode": "w"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stderr",
                "stdout",
                "file"
            ]
        }
    }

Cấu hình này *gần như* thực hiện đúng điều chúng ta muốn, ngoại trừ việc ``sys.stdout`` sẽ hiển thị các thông báo có mức độ nghiêm trọng ``ERROR``, và chỉ các event có mức độ này trở lên mới được theo dõi, cùng với các thông báo ``INFO`` và ``WARNING``. Để ngăn điều này, chúng ta có thể thiết lập một filter loại trừ những thông báo đó rồi thêm filter này vào handler liên quan. Có thể cấu hình việc này bằng cách thêm một phần ``filters`` song song với ``formatters`` và ``handlers``:

.. code-block:: json

    {
        "filters": {
            "warnings_and_below": {
                "()" : "__main__.filter_maker",
                "level": "WARNING"
            }
        }
    }

và thay đổi phần dành cho handler ``stdout`` để thêm phần đó:

.. code-block:: json

    {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
            "filters": ["warnings_and_below"]
        }
    }

Bộ lọc chỉ là một hàm, vì vậy ta có thể định nghĩa ``filter_maker`` (một hàm factory) như sau:

.. code-block:: python

    def filter_maker(level):
        level = getattr(logging, level)

        def filter(record):
            return record.levelno <= level

        return filter

Hàm này chuyển đổi đối số chuỗi được truyền vào thành một level dạng số, rồi trả về một hàm chỉ trả về ``True`` nếu level của record được truyền vào nhỏ hơn hoặc bằng level đã chỉ định. Lưu ý rằng trong ví dụ này, tôi đã định nghĩa ``filter_maker`` trong một test script ``main.py`` được chạy từ command line, vì vậy module của nó sẽ là ``__main__`` — do đó có ``__main__.filter_maker`` trong cấu hình bộ lọc. Bạn sẽ cần thay đổi giá trị đó nếu định nghĩa nó trong một module khác.

Sau khi thêm bộ lọc, ta có thể chạy ``main.py``, đầy đủ là:

.. code-block:: python

    import json
    import logging
    import logging.config

    CONFIG = '''
    {
        "version": 1,
        "disable_existing_loggers": false,
        "formatters": {
            "simple": {
                "format": "%(levelname)-8s - %(message)s"
            }
        },
        "filters": {
            "warnings_and_below": {
                "()" : "__main__.filter_maker",
                "level": "WARNING"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
                "filters": ["warnings_and_below"]
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "simple",
                "stream": "ext://sys.stderr"
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "filename": "app.log",
                "mode": "w"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stderr",
                "stdout",
                "file"
            ]
        }
    }
    '''

    def filter_maker(level):
        level = getattr(logging, level)

        def filter(record):
            return record.levelno <= level

        return filter

    logging.config.dictConfig(json.loads(CONFIG))
    logging.debug('A DEBUG message')
    logging.info('An INFO message')
    logging.warning('A WARNING message')
    logging.error('An ERROR message')
    logging.critical('A CRITICAL message')

Và sau khi chạy như sau:

.. code-block:: shell

    python main.py 2>stderr.log >stdout.log

Ta có thể thấy kết quả đúng như mong đợi:

.. code-block:: shell

    $ more *.log
    ::::::::::::::
    app.log
    ::::::::::::::
    DEBUG    - A DEBUG message
    INFO     - An INFO message
    WARNING  - A WARNING message
    ERROR    - An ERROR message
    CRITICAL - A CRITICAL message
    ::::::::::::::
    stderr.log
    ::::::::::::::
    ERROR    - An ERROR message
    CRITICAL - A CRITICAL message
    ::::::::::::::
    stdout.log
    ::::::::::::::
    INFO     - An INFO message
    WARNING  - A WARNING message


Ví dụ về máy chủ cấu hình
-------------------------

Sau đây là ví dụ về một module sử dụng máy chủ cấu hình logging::

    import logging
    import logging.config
    import time
    import os

    # đọc tệp cấu hình ban đầu
    logging.config.fileConfig('logging.conf')

    # tạo và khởi động listener trên cổng 9999
    t = logging.config.listen(9999)
    t.start()

    logger = logging.getLogger('simpleExample')

    try:
        # lặp qua các lệnh gọi logging để thấy sự khác biệt
        # tạo các cấu hình mới cho đến khi nhấn Ctrl+C
        while True:
            logger.debug('debug message')
            logger.info('info message')
            logger.warning('warn message')
            logger.error('error message')
            logger.critical('critical message')
            time.sleep(5)
    except KeyboardInterrupt:
        # dọn dẹp
        logging.config.stopListening()
        t.join()

Sau đây là một script nhận tên tệp và gửi tệp đó đến server, với độ dài được mã hóa nhị phân đặt ngay trước nội dung, làm cấu hình logging mới::

    #!/usr/bin/env python
    import socket, sys, struct

    with open(sys.argv[1], 'rb') as f:
        data_to_send = f.read()

    HOST = 'localhost'
    PORT = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting...')
    s.connect((HOST, PORT))
    print('sending config...')
    s.send(struct.pack('>L', len(data_to_send)))
    s.send(data_to_send)
    s.close()
    print('complete')


.. _blocking-handlers:

Xử lý các handler bị chặn
-------------------------

.. currentmodule:: logging.handlers

Đôi khi bạn cần các logging handler thực hiện công việc mà không chặn thread đang thực hiện việc ghi log. Điều này thường gặp trong các ứng dụng web, dù tất nhiên nó cũng xảy ra trong những tình huống khác.

Một thủ phạm phổ biến thường thể hiện hành vi chậm chạp là
:class:`SMTPHandler`: việc gửi email có thể mất nhiều thời gian vì một số nguyên nhân nằm ngoài tầm kiểm soát của developer (chẳng hạn như hạ tầng mail hoặc network hoạt động kém). Tuy nhiên, hầu như bất kỳ handler dựa trên network nào cũng có thể chặn: Ngay cả một thao tác :class:`SocketHandler` cũng có thể ngầm thực hiện truy vấn DNS quá chậm (và truy vấn này có thể nằm sâu trong mã của socket library, bên dưới lớp Python và ngoài tầm kiểm soát của bạn).

Một giải pháp là sử dụng phương pháp gồm hai phần. Trước tiên, chỉ gắn một
:class:`QueueHandler` vào những logger được truy cập từ các thread quan trọng về hiệu năng. Chúng chỉ cần ghi vào queue, queue này có thể được cấp dung lượng đủ lớn hoặc được khởi tạo mà không giới hạn kích thước tối đa. Việc ghi vào queue thường sẽ được chấp nhận nhanh chóng, dù có lẽ bạn vẫn cần bắt ngoại lệ :exc:`queue.Full` để đề phòng trong code của mình. Nếu bạn là library developer và code của bạn có các thread quan trọng về hiệu năng, hãy nhớ ghi rõ điều này trong tài liệu (kèm theo đề xuất chỉ gắn ``QueueHandlers`` vào các logger của bạn) để các developer khác sử dụng code của bạn được thuận tiện.

Phần thứ hai của giải pháp là :class:`QueueListener`, được thiết kế như thành phần đối ứng với :class:`QueueHandler`. Một
:class:`QueueListener` rất đơn giản: nó nhận một queue và một số handler, rồi khởi động một thread nội bộ lắng nghe queue để nhận các LogRecord được gửi từ ``QueueHandlers`` (hoặc từ bất kỳ nguồn ``LogRecords`` nào khác). Các ``LogRecords`` được lấy khỏi queue và chuyển cho các handler để xử lý.

Ưu điểm của việc có một lớp :class:`QueueListener` riêng là bạn có thể sử dụng cùng một instance để phục vụ nhiều ``QueueHandlers``. Cách này tiết kiệm tài nguyên hơn so với việc tạo các phiên bản có thread của những lớp handler hiện có, vốn sẽ chiếm một thread cho mỗi handler mà không mang lại lợi ích cụ thể nào.

Sau đây là ví dụ về cách sử dụng hai lớp này (đã lược bỏ phần import)::

    que = queue.Queue(-1)  # không giới hạn kích thước
    queue_handler = QueueHandler(que)
    handler = logging.StreamHandler()
    listener = QueueListener(que, handler)
    root = logging.getLogger()
    root.addHandler(queue_handler)
    formatter = logging.Formatter('%(threadName)s: %(message)s')
    handler.setFormatter(formatter)
    listener.start()
    # Đầu ra nhật ký sẽ hiển thị thread đã tạo ra
    # event (thread chính) thay vì thread nội bộ
    # theo dõi queue nội bộ. Đây là điều
    # bạn muốn xảy ra.
    root.warning('Look out!')
    listener.stop()

mà khi chạy sẽ tạo ra:

.. code-block:: none

    MainThread: Look out!

.. note:: Mặc dù phần thảo luận trước đó không nói cụ thể về mã async mà nói về các logging handler chậm, cần lưu ý rằng khi ghi log từ mã async, các network handler và thậm chí cả file handler cũng có thể gây ra sự cố (làm block event loop) vì một phần hoạt động ghi log được thực hiện từ
   :mod:`asyncio` internals. It might be best, if any async code is used in an
   ứng dụng, để sử dụng cách tiếp cận trên cho việc ghi log, sao cho mọi mã có thể block chỉ chạy trong thread ``QueueListener``.

.. versionchanged:: 3.5
   Trước Python 3.5, :class:`QueueListener` luôn chuyển mọi message nhận được từ queue đến mọi handler mà nó được khởi tạo cùng. (Điều này là vì người ta cho rằng việc lọc theo level đã được thực hiện hoàn toàn ở phía bên kia, nơi queue được điền.) Từ phiên bản 3.5 trở đi, hành vi này có thể được thay đổi bằng cách truyền keyword argument ``respect_handler_level=True`` vào constructor của listener. Khi đó, listener sẽ so sánh level của từng message với level của handler và chỉ chuyển message đến handler nếu phù hợp.

.. versionchanged:: 3.14
   Có thể khởi động (và dừng) :class:`QueueListener` thông qua
   statement :keyword:`with`. Ví dụ:

   .. code-block:: python

      with QueueListener(que, handler) as listener:
          # Queue listener tự động khởi động
          # khi khối 'with' được thực thi.
          pass
      # Trình lắng nghe queue tự động dừng ngay khi
      # khối 'with' kết thúc.

.. _network-logging:

Gửi và nhận các sự kiện logging qua mạng
----------------------------------------

Giả sử bạn muốn gửi các sự kiện logging qua mạng và xử lý chúng ở đầu nhận. Một cách đơn giản để thực hiện việc này là gắn một
:class:`SocketHandler` instance vào root logger ở đầu gửi::

   import logging, logging.handlers

   rootLogger = logging.getLogger()
   rootLogger.setLevel(logging.DEBUG)
   socketHandler = logging.handlers.SocketHandler('localhost',
                       logging.handlers.DEFAULT_TCP_LOGGING_PORT)
   # không cần dùng formatter, vì socket handler gửi sự kiện dưới dạng
   # một pickle chưa được định dạng
   rootLogger.addHandler(socketHandler)

   # Bây giờ, chúng ta có thể ghi log vào root logger hoặc bất kỳ logger nào khác. Trước tiên là root...
   logging.info('Jackdaws love my big sphinx of quartz.')

   # Bây giờ, hãy định nghĩa một vài logger khác, có thể đại diện cho các phần trong
   # ứng dụng:

   logger1 = logging.getLogger('myapp.area1')
   logger2 = logging.getLogger('myapp.area2')

   logger1.debug('Quick zephyrs blow, vexing daft Jim.')
   logger1.info('How quickly daft jumping zebras vex.')
   logger2.warning('Jail zesty vixen who grabbed pay from quack.')
   logger2.error('The five boxing wizards jump quickly.')

Ở phía nhận, bạn có thể thiết lập một receiver bằng module :mod:`socketserver`. Đây là một ví dụ cơ bản có thể hoạt động::

   import pickle
   import logging
   import logging.handlers
   import socketserver
   import struct


   class LogRecordStreamHandler(socketserver.StreamRequestHandler):
       """Handler for a streaming logging request.

       This basically logs the record using whatever logging policy is
       configured locally.
       """

       def handle(self):
           """
           Handle multiple requests - each expected to be a 4-byte length,
           followed by the LogRecord in pickle format. Logs the record
           according to whatever policy is configured locally.
           """
           while True:
               chunk = self.connection.recv(4)
               if len(chunk) < 4:
                   break
               slen = struct.unpack('>L', chunk)[0]
               chunk = self.connection.recv(slen)
               while len(chunk) < slen:
                   chunk = chunk + self.connection.recv(slen - len(chunk))
               obj = self.unPickle(chunk)
               record = logging.makeLogRecord(obj)
               self.handleLogRecord(record)

       def unPickle(self, data):
           return pickle.loads(data)

       def handleLogRecord(self, record):
           # nếu có chỉ định tên, chúng ta sử dụng logger có tên đó thay vì logger
           # được suy ra từ record.
           if self.server.logname is not None:
               name = self.server.logname
           else:
               name = record.name
           logger = logging.getLogger(name)
           # LƯU Ý: MỌI bản ghi đều được ghi lại. Điều này là do Logger.handle
           # thường được gọi SAU khi lọc ở cấp logger. Nếu bạn muốn
           # thực hiện lọc, hãy thực hiện ở phía client để tránh lãng phí
           # chu kỳ xử lý và băng thông mạng!
           logger.handle(record)

   class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
       """
       Simple TCP socket-based logging receiver suitable for testing.
       """

       allow_reuse_address = True

       def __init__(self, host='localhost',
                    port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                    handler=LogRecordStreamHandler):
           socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
           self.abort = 0
           self.timeout = 1
           self.logname = None

       def serve_until_stopped(self):
           import select
           abort = 0
           while not abort:
               rd, wr, ex = select.select([self.socket.fileno()],
                                          [], [],
                                          self.timeout)
               if rd:
                   self.handle_request()
               abort = self.abort

   def main():
       logging.basicConfig(
           format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
       tcpserver = LogRecordSocketReceiver()
       print('About to start TCP server...')
       tcpserver.serve_until_stopped()

   if __name__ == '__main__':
       main()

Trước tiên hãy chạy server, sau đó chạy client. Ở phía client, không có gì được in ra console; ở phía server, bạn sẽ thấy nội dung tương tự như sau:

.. code-block:: none

   About to start TCP server...
      59 root            INFO     Jackdaws love my big sphinx of quartz.
      59 myapp.area1     DEBUG    Quick zephyrs blow, vexing daft Jim.
      69 myapp.area1     INFO     How quickly daft jumping zebras vex.
      69 myapp.area2     WARNING  Jail zesty vixen who grabbed pay from quack.
      69 myapp.area2     ERROR    The five boxing wizards jump quickly.

Lưu ý rằng pickle có thể gây ra một số vấn đề bảo mật trong một số tình huống. Nếu những vấn đề này ảnh hưởng đến bạn, bạn có thể sử dụng một cơ chế serialization thay thế bằng cách ghi đè phương thức :meth:`~SocketHandler.makePickle` và triển khai cơ chế thay thế của mình tại đó, đồng thời điều chỉnh script ở trên để sử dụng cơ chế serialization thay thế đó.


.. _`Running a logging socket listener in production`:

Chạy socket listener ghi log trong môi trường production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _socket-listener-gist: https://gist.github.com/vsajip/4b227eeec43817465ca835ca66f75e2b

Để chạy một logging listener trong môi trường production, bạn có thể cần sử dụng một công cụ quản lý tiến trình như `Supervisor <http://supervisord.org/>`_. `Đây là một Gist <socket-listener-gist_>`__ cung cấp các tệp tối thiểu cần thiết để chạy chức năng trên bằng Supervisor. Gist này gồm các tệp sau:

+-------------------------+-------------------------------------------------------------------------------------------------+
| Tệp                     | Mục đích                                                                                        |
+=========================+=================================================================================================+
| :file:`prepare.sh`      | Một tập lệnh Bash để chuẩn bị môi trường cho việc kiểm thử                                      |
+-------------------------+-------------------------------------------------------------------------------------------------+
| :file:`supervisor.conf` | Tệp cấu hình Supervisor, chứa các mục cho listener và một web application đa tiến trình         |
+-------------------------+-------------------------------------------------------------------------------------------------+
| :file:`ensure_app.sh`   | Một tập lệnh Bash để đảm bảo Supervisor đang chạy với cấu hình trên                             |
+-------------------------+-------------------------------------------------------------------------------------------------+
| :file:`log_listener.py` | Chương trình socket listener nhận các sự kiện log và ghi chúng vào một tệp                      |
+-------------------------+-------------------------------------------------------------------------------------------------+
| :file:`main.py`         | Một ứng dụng web đơn giản thực hiện việc ghi nhật ký thông qua socket được kết nối với listener |
+-------------------------+-------------------------------------------------------------------------------------------------+
| :file:`webapp.json`     | Một tệp cấu hình JSON cho ứng dụng web                                                          |
+-------------------------+-------------------------------------------------------------------------------------------------+
| :file:`client.py`       | Một tập lệnh Python để kiểm thử ứng dụng web                                                    |
+-------------------------+-------------------------------------------------------------------------------------------------+

Ứng dụng web sử dụng `Gunicorn <https://gunicorn.org/>`_, một web application server phổ biến khởi chạy nhiều worker process để xử lý các yêu cầu. Thiết lập ví dụ này cho thấy cách các worker có thể ghi vào cùng một tệp nhật ký mà không xung đột với nhau --- tất cả đều đi qua socket listener.

Để kiểm thử các tệp này, hãy thực hiện các bước sau trong môi trường POSIX:

#. Tải `Gist <socket-listener-gist_>`__ xuống dưới dạng tệp ZIP bằng nút :guilabel:`Download ZIP`.

#. Giải nén các tệp trên từ kho lưu trữ vào một thư mục tạm.

#. Trong thư mục tạm, chạy ``bash prepare.sh`` để chuẩn bị mọi thứ. Thao tác này tạo một thư mục con :file:`run` để chứa các tệp liên quan đến Supervisor và các tệp nhật ký, đồng thời tạo một thư mục con :file:`venv` để chứa một môi trường ảo, trong đó ``bottle``, ``gunicorn`` và ``supervisor`` được cài đặt.

#. Chạy ``bash ensure_app.sh`` để đảm bảo Supervisor đang chạy với cấu hình ở trên.

#. Chạy ``venv/bin/python client.py`` để kiểm thử ứng dụng web; thao tác này sẽ khiến các bản ghi được ghi vào nhật ký.

#. Kiểm tra các tệp nhật ký trong thư mục con :file:`run`. Bạn sẽ thấy các dòng nhật ký mới nhất trong những tệp khớp với mẫu :file:`app.log*`. Chúng sẽ không theo bất kỳ thứ tự cụ thể nào, vì đã được các quy trình worker khác nhau xử lý đồng thời theo cách không xác định.

#. Bạn có thể tắt listener và ứng dụng web bằng cách chạy ``venv/bin/supervisorctl -c supervisor.conf shutdown``.

Bạn có thể cần điều chỉnh các tệp cấu hình trong trường hợp hiếm gặp khi các cổng đã cấu hình xung đột với một thành phần khác trong môi trường kiểm thử của bạn.

Cấu hình mặc định sử dụng TCP socket trên cổng 9020. Bạn có thể sử dụng Unix Domain socket thay cho TCP socket bằng cách thực hiện như sau:

#. Trong :file:`listener.json`, thêm một khóa ``socket`` với đường dẫn đến domain socket bạn muốn sử dụng. Nếu khóa này hiện diện, listener sẽ lắng nghe trên domain socket tương ứng thay vì trên TCP socket (khóa ``port`` sẽ bị bỏ qua).

#. Trong :file:`webapp.json`, thay đổi dictionary cấu hình socket handler để giá trị ``host`` là đường dẫn đến domain socket, và đặt giá trị ``port`` thành ``null``.


.. currentmodule:: logging

.. _context-info:

Thêm thông tin ngữ cảnh vào đầu ra logging
------------------------------------------

Đôi khi bạn muốn đầu ra logging chứa thông tin ngữ cảnh bên cạnh các tham số được truyền vào lời gọi logging. Ví dụ: trong một ứng dụng nối mạng, bạn có thể muốn ghi lại thông tin dành riêng cho client trong log (ví dụ: username hoặc địa chỉ IP của client từ xa). Mặc dù bạn có thể sử dụng tham số *extra* để thực hiện việc này, nhưng việc truyền thông tin theo cách này không phải lúc nào cũng thuận tiện. Mặc dù bạn có thể muốn tạo
các instance :class:`Logger` cho từng connection, đây không phải là ý hay vì các instance này không được garbage collection. Mặc dù trên thực tế điều này không gây vấn đề, khi số lượng instance :class:`Logger` phụ thuộc vào mức độ chi tiết bạn muốn sử dụng trong việc logging một ứng dụng, việc quản lý có thể trở nên khó khăn nếu số lượng instance :class:`Logger` tăng lên không có giới hạn thực tế.


Sử dụng LoggerAdapters để truyền thông tin ngữ cảnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một cách dễ dàng để truyền thông tin ngữ cảnh nhằm xuất cùng với thông tin về sự kiện logging là sử dụng class :class:`LoggerAdapter`. Class này được thiết kế để trông giống như một :class:`Logger`, vì vậy bạn có thể gọi
:meth:`debug`, :meth:`info`, :meth:`warning`, :meth:`error`,
:meth:`exception`, :meth:`critical` và :meth:`log`. Các phương thức này có cùng chữ ký với các phương thức tương ứng trong :class:`Logger`, vì vậy bạn có thể sử dụng thay thế lẫn nhau hai loại instance này.

Khi tạo một instance của :class:`LoggerAdapter`, bạn truyền vào đó một
instance :class:`Logger` và một đối tượng dạng dict chứa thông tin ngữ cảnh của bạn. Khi gọi một trong các phương thức logging trên một instance của
:class:`LoggerAdapter`, nó chuyển tiếp lệnh gọi đến instance nền tảng của
:class:`Logger` được truyền vào hàm khởi tạo, đồng thời sắp xếp để truyền thông tin ngữ cảnh trong lệnh gọi được chuyển tiếp. Dưới đây là một đoạn trích từ mã của
:class:`LoggerAdapter`::

    def debug(self, msg, /, *args, **kwargs):
        """
        Delegate a debug call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)

Phương thức :meth:`~LoggerAdapter.process` của :class:`LoggerAdapter` là nơi thông tin ngữ cảnh được thêm vào đầu ra logging. Phương thức này nhận thông báo và các đối số từ khóa của lệnh gọi logging, rồi trả về các phiên bản (có thể đã được sửa đổi) của chúng để sử dụng trong lệnh gọi đến logger nền tảng. Cách triển khai mặc định của phương thức này giữ nguyên thông báo, nhưng chèn một khóa 'extra' vào đối số từ khóa, với giá trị là đối tượng dạng dict được truyền vào hàm khởi tạo. Tất nhiên, nếu bạn đã truyền một đối số từ khóa 'extra' trong lệnh gọi đến adapter, đối số đó sẽ bị ghi đè một cách im lặng.

Ưu điểm của việc sử dụng 'extra' là các giá trị trong đối tượng dạng dict được hợp nhất vào __dict__ của instance :class:`LogRecord`, cho phép bạn sử dụng các chuỗi tùy chỉnh với các instance :class:`Formatter` biết các khóa của đối tượng dạng dict. Nếu cần một phương thức khác, chẳng hạn như muốn thêm thông tin ngữ cảnh vào đầu hoặc cuối chuỗi thông báo, bạn chỉ cần tạo lớp con của :class:`LoggerAdapter` và ghi đè
:meth:`~LoggerAdapter.process` để thực hiện việc bạn cần. Dưới đây là một ví dụ đơn giản::

    class CustomAdapter(logging.LoggerAdapter):
        """
        This example adapter expects the passed in dict-like object to have a
        'connid' key, whose value in brackets is prepended to the log message.
        """
        def process(self, msg, kwargs):
            return '[%s] %s' % (self.extra['connid'], msg), kwargs

mà bạn có thể sử dụng như sau::

    logger = logging.getLogger(__name__)
    adapter = CustomAdapter(logger, {'connid': some_conn_id})

Sau đó, mọi sự kiện bạn ghi nhật ký vào adapter sẽ có giá trị của ``some_conn_id`` được thêm vào trước các thông báo nhật ký.

Sử dụng các đối tượng khác dict để truyền đạt thông tin theo ngữ cảnh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bạn không cần truyền một dict thực sự vào một :class:`LoggerAdapter` - bạn có thể truyền một instance của một class triển khai ``__getitem__`` và ``__iter__`` để logging xem nó như một dict. Điều này hữu ích nếu bạn muốn tạo các giá trị một cách động (trong khi các giá trị trong dict sẽ là hằng số).


.. _filters-contextual:

Sử dụng Filters để truyền đạt thông tin theo ngữ cảnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bạn cũng có thể bổ sung thông tin theo ngữ cảnh vào đầu ra nhật ký bằng cách sử dụng một do người dùng định nghĩa
:class:`Filter`. Các instance ``Filter`` được phép sửa đổi ``LogRecords`` được truyền cho chúng, bao gồm việc thêm các thuộc tính bổ sung, sau đó có thể xuất các thuộc tính này bằng một format string phù hợp hoặc, nếu cần, một :class:`Formatter` tùy chỉnh.

Ví dụ, trong một ứng dụng web, request đang được xử lý (hoặc ít nhất là những phần đáng chú ý của request) có thể được lưu trong một biến threadlocal (:class:`threading.local`), sau đó được truy cập từ một ``Filter`` để thêm, chẳng hạn, thông tin từ request — cụ thể là địa chỉ IP từ xa và username của người dùng từ xa — vào ``LogRecord``, bằng cách sử dụng các tên thuộc tính 'ip' và 'user' như trong ví dụ ``LoggerAdapter`` ở trên. Khi đó, có thể sử dụng cùng một format string để tạo ra kết quả tương tự như kết quả đã trình bày ở trên. Dưới đây là một script mẫu::

    import logging
    from random import choice

    class ContextFilter(logging.Filter):
        """
        This is a filter which injects contextual information into the log.

        Rather than use actual contextual information, we just use random
        data in this demo.
        """

        USERS = ['jim', 'fred', 'sheila']
        IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']

        def filter(self, record):

            record.ip = choice(ContextFilter.IPS)
            record.user = choice(ContextFilter.USERS)
            return True

    if __name__ == '__main__':
        levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)-15s %(name)-5s %(levelname)-8s IP: %(ip)-15s User: %(user)-8s %(message)s')
        a1 = logging.getLogger('a.b.c')
        a2 = logging.getLogger('d.e.f')

        f = ContextFilter()
        a1.addFilter(f)
        a2.addFilter(f)
        a1.debug('A debug message')
        a1.info('An info message with %s', 'some parameters')
        for x in range(10):
            lvl = choice(levels)
            lvlname = logging.getLevelName(lvl)
            a2.log(lvl, 'A message at %s level with %d %s', lvlname, 2, 'parameters')

khi chạy sẽ tạo ra kết quả tương tự như sau:

.. code-block:: none

    2010-09-06 22:38:15,292 a.b.c DEBUG    IP: 123.231.231.123 User: fred     A debug message
    2010-09-06 22:38:15,300 a.b.c INFO     IP: 192.168.0.1     User: sheila   An info message with some parameters
    2010-09-06 22:38:15,300 d.e.f CRITICAL IP: 127.0.0.1       User: sheila   A message at CRITICAL level with 2 parameters
    2010-09-06 22:38:15,300 d.e.f ERROR    IP: 127.0.0.1       User: jim      A message at ERROR level with 2 parameters
    2010-09-06 22:38:15,300 d.e.f DEBUG    IP: 127.0.0.1       User: sheila   A message at DEBUG level with 2 parameters
    2010-09-06 22:38:15,300 d.e.f ERROR    IP: 123.231.231.123 User: fred     A message at ERROR level with 2 parameters
    2010-09-06 22:38:15,300 d.e.f CRITICAL IP: 192.168.0.1     User: jim      A message at CRITICAL level with 2 parameters
    2010-09-06 22:38:15,300 d.e.f CRITICAL IP: 127.0.0.1       User: sheila   A message at CRITICAL level with 2 parameters
    2010-09-06 22:38:15,300 d.e.f DEBUG    IP: 192.168.0.1     User: jim      A message at DEBUG level with 2 parameters
    2010-09-06 22:38:15,301 d.e.f ERROR    IP: 127.0.0.1       User: sheila   A message at ERROR level with 2 parameters
    2010-09-06 22:38:15,301 d.e.f DEBUG    IP: 123.231.231.123 User: fred     A message at DEBUG level with 2 parameters
    2010-09-06 22:38:15,301 d.e.f INFO     IP: 123.231.231.123 User: fred     A message at INFO level with 2 parameters

Sử dụng ``contextvars``
-----------------------

Kể từ Python 3.7, module :mod:`contextvars` đã cung cấp bộ nhớ lưu trữ cục bộ theo context, hoạt động cho cả nhu cầu xử lý :mod:`threading` và :mod:`asyncio`. Vì vậy, loại bộ nhớ này nhìn chung có thể phù hợp hơn thread-local. Ví dụ sau đây cho thấy trong một môi trường đa luồng, log có thể được bổ sung thông tin theo context, chẳng hạn như các thuộc tính của request do các ứng dụng web xử lý.

Để minh họa, giả sử bạn có nhiều ứng dụng web khác nhau, mỗi ứng dụng độc lập với các ứng dụng còn lại nhưng chạy trong cùng một tiến trình Python và sử dụng một thư viện dùng chung. Làm thế nào để mỗi ứng dụng có log riêng, trong đó tất cả thông báo log từ thư viện (và phần code xử lý request khác) đều được ghi vào file log của ứng dụng tương ứng, đồng thời bao gồm các thông tin bổ sung theo context như IP của client, phương thức HTTP request và username của client?

Giả sử thư viện có thể được mô phỏng bằng đoạn code sau:

.. code-block:: python

    # webapplib.py
    import logging
    import time

    logger = logging.getLogger(__name__)

    def useful():
        # Chỉ là một sự kiện đại diện được ghi lại từ thư viện
        logger.debug('Hello from webapplib!')
        # Chỉ cần tạm nghỉ một lát để các thread khác có thể chạy
        time.sleep(0.01)

Chúng ta có thể mô phỏng nhiều ứng dụng web bằng hai lớp đơn giản, ``Request`` và ``WebApp``. Các lớp này mô phỏng cách những ứng dụng web đa thread thực hoạt động - mỗi request được xử lý bởi một thread:

.. code-block:: python

    # main.py
    import argparse
    from contextvars import ContextVar
    import logging
    import os
    from random import choice
    import threading
    import webapplib

    logger = logging.getLogger(__name__)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    class Request:
        """
        A simple dummy request class which just holds dummy HTTP request method,
        client IP address and client username
        """
        def __init__(self, method, ip, user):
            self.method = method
            self.ip = ip
            self.user = user

    # Một tập hợp request giả sẽ được dùng trong mô phỏng - chúng ta sẽ chỉ chọn ngẫu nhiên
    # từ danh sách này. Lưu ý rằng tất cả request GET đều đến từ 192.168.2.XXX
    # các địa chỉ, trong khi các yêu cầu POST đến từ các địa chỉ 192.16.3.XXX. Ba người dùng
    # được biểu diễn trong các yêu cầu mẫu.

    REQUESTS = [
        Request('GET', '192.168.2.20', 'jim'),
        Request('POST', '192.168.3.20', 'fred'),
        Request('GET', '192.168.2.21', 'sheila'),
        Request('POST', '192.168.3.21', 'jim'),
        Request('GET', '192.168.2.22', 'fred'),
        Request('POST', '192.168.3.22', 'sheila'),
    ]

    # Lưu ý rằng chuỗi định dạng bao gồm các tham chiếu đến thông tin ngữ cảnh của yêu cầu
    # chẳng hạn như phương thức HTTP, IP máy khách và tên người dùng

    formatter = logging.Formatter('%(threadName)-11s %(appName)s %(name)-9s %(user)-6s %(ip)s %(method)-4s %(message)s')

    # Tạo các biến ngữ cảnh của chúng ta. Các biến này sẽ được điền vào lúc bắt đầu xử lý yêu cầu
    # và được sử dụng trong hoạt động ghi nhật ký diễn ra trong quá trình xử lý đó

    ctx_request = ContextVar('request')
    ctx_appname = ContextVar('appname')

    class InjectingFilter(logging.Filter):
        """
        A filter which injects context-specific information into logs and ensures
        that only information for a specific webapp is included in its log
        """
        def __init__(self, app):
            self.app = app

        def filter(self, record):
            request = ctx_request.get()
            record.method = request.method
            record.ip = request.ip
            record.user = request.user
            record.appName = appName = ctx_appname.get()
            return appName == self.app.name

    class WebApp:
        """
        A dummy web application class which has its own handler and filter for a
        webapp-specific log.
        """
        def __init__(self, name):
            self.name = name
            handler = logging.FileHandler(name + '.log', 'w')
            f = InjectingFilter(self)
            handler.setFormatter(formatter)
            handler.addFilter(f)
            root.addHandler(handler)
            self.num_requests = 0

        def process_request(self, request):
            """
            This is the dummy method for processing a request. It's called on a
            different thread for every request. We store the context information into
            the context vars before doing anything else.
            """
            ctx_request.set(request)
            ctx_appname.set(self.name)
            self.num_requests += 1
            logger.debug('Request processing started')
            webapplib.useful()
            logger.debug('Request processing finished')

    def main():
        fn = os.path.splitext(os.path.basename(__file__))[0]
        adhf = argparse.ArgumentDefaultsHelpFormatter
        ap = argparse.ArgumentParser(formatter_class=adhf, prog=fn,
                                     description='Simulate a couple of web '
                                                 'applications handling some '
                                                 'requests, showing how request '
                                                 'context can be used to '
                                                 'populate logs')
        aa = ap.add_argument
        aa('--count', '-c', type=int, default=100, help='How many requests to simulate')
        options = ap.parse_args()

        # Tạo các webapp giả và đưa chúng vào một danh sách mà chúng ta có thể dùng để chọn
        # một cách ngẫu nhiên
        app1 = WebApp('app1')
        app2 = WebApp('app2')
        apps = [app1, app2]
        threads = []
        # Thêm một handler dùng chung để capture tất cả sự kiện
        handler = logging.FileHandler('app.log', 'w')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        # Tạo các lệnh gọi để xử lý request
        for i in range(options.count):
            try:
                # Chọn ngẫu nhiên một app và một request để app đó xử lý
                app = choice(apps)
                request = choice(REQUESTS)
                # Xử lý request trong thread riêng
                t = threading.Thread(target=app.process_request, args=(request,))
                threads.append(t)
                t.start()
            except KeyboardInterrupt:
                break

        # Chờ các thread kết thúc
        for t in threads:
            t.join()

        for app in apps:
            print('%s processed %s requests' % (app.name, app.num_requests))

    if __name__ == '__main__':
        main()

Nếu chạy đoạn mã trên, bạn sẽ thấy khoảng một nửa số request được ghi vào :file:`app1.log` và số còn lại được ghi vào :file:`app2.log`, đồng thời tất cả request đều được ghi log vào :file:`app.log`. Mỗi log dành riêng cho một webapp sẽ chỉ chứa các mục log của chính webapp đó, và thông tin request sẽ được hiển thị nhất quán trong log (tức là thông tin trong mỗi dummy request sẽ luôn xuất hiện cùng nhau trên một dòng log). Điều này được minh họa bằng kết quả shell sau:

.. code-block:: shell

    ~/logging-contextual-webapp$ python main.py
    app1 processed 51 requests
    app2 processed 49 requests
    ~/logging-contextual-webapp$ wc -l *.log
      153 app1.log
      147 app2.log
      300 app.log
      600 total
    ~/logging-contextual-webapp$ head -3 app1.log
    Thread-3 (process_request) app1 __main__  jim    192.168.3.21 POST Request processing started
    Thread-3 (process_request) app1 webapplib jim    192.168.3.21 POST Hello from webapplib!
    Thread-5 (process_request) app1 __main__  jim    192.168.3.21 POST Request processing started
    ~/logging-contextual-webapp$ head -3 app2.log
    Thread-1 (process_request) app2 __main__  sheila 192.168.2.21 GET  Request processing started
    Thread-1 (process_request) app2 webapplib sheila 192.168.2.21 GET  Hello from webapplib!
    Thread-2 (process_request) app2 __main__  jim    192.168.2.20 GET  Request processing started
    ~/logging-contextual-webapp$ head app.log
    Thread-1 (process_request) app2 __main__  sheila 192.168.2.21 GET  Request processing started
    Thread-1 (process_request) app2 webapplib sheila 192.168.2.21 GET  Hello from webapplib!
    Thread-2 (process_request) app2 __main__  jim    192.168.2.20 GET  Request processing started
    Thread-3 (process_request) app1 __main__  jim    192.168.3.21 POST Request processing started
    Thread-2 (process_request) app2 webapplib jim    192.168.2.20 GET  Hello from webapplib!
    Thread-3 (process_request) app1 webapplib jim    192.168.3.21 POST Hello from webapplib!
    Thread-4 (process_request) app2 __main__  fred   192.168.2.22 GET  Request processing started
    Thread-5 (process_request) app1 __main__  jim    192.168.3.21 POST Request processing started
    Thread-4 (process_request) app2 webapplib fred   192.168.2.22 GET  Hello from webapplib!
    Thread-6 (process_request) app1 __main__  jim    192.168.3.21 POST Request processing started
    ~/logging-contextual-webapp$ grep app1 app1.log | wc -l
    153
    ~/logging-contextual-webapp$ grep app2 app2.log | wc -l
    147
    ~/logging-contextual-webapp$ grep app1 app.log | wc -l
    153
    ~/logging-contextual-webapp$ grep app2 app.log | wc -l
    147


Truyền thông tin ngữ cảnh trong các handler
-------------------------------------------

Mỗi :class:`~Handler` có chuỗi filter riêng. Nếu muốn thêm thông tin ngữ cảnh vào một :class:`LogRecord` mà không làm lộ thông tin đó cho các handler khác, bạn có thể sử dụng một filter trả về một :class:`~LogRecord` mới thay vì sửa đổi nó tại chỗ, như trong script sau::

    import copy
    import logging

    def filter(record: logging.LogRecord):
        record = copy.copy(record)
        record.user = 'jim'
        return record

    if __name__ == '__main__':
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s from %(user)-8s')
        handler.setFormatter(formatter)
        handler.addFilter(filter)
        logger.addHandler(handler)

        logger.info('A log message')

.. _multiple-processes:

Ghi log vào một tệp duy nhất từ nhiều tiến trình
------------------------------------------------

Mặc dù logging an toàn với thread và việc ghi log vào một tệp duy nhất từ nhiều thread trong một tiến trình *được* hỗ trợ, việc ghi log vào một tệp duy nhất từ *nhiều tiến trình* *không* được hỗ trợ, vì trong Python không có cách tiêu chuẩn nào để tuần tự hóa quyền truy cập vào một tệp duy nhất giữa nhiều tiến trình. Nếu cần ghi log vào một tệp duy nhất từ nhiều tiến trình, một cách thực hiện là để tất cả các tiến trình ghi log vào một :class:`~handlers.SocketHandler`, đồng thời có một tiến trình riêng triển khai socket server để đọc dữ liệu từ socket và ghi vào tệp. (Nếu muốn, bạn có thể dành riêng một thread trong một trong các tiến trình hiện có để thực hiện chức năng này.)
:ref:`Phần này <network-logging>` trình bày chi tiết hơn về cách tiếp cận này và bao gồm một socket receiver hoạt động được, có thể dùng làm điểm khởi đầu để bạn điều chỉnh cho các ứng dụng của mình.

Bạn cũng có thể tự viết một handler sử dụng class :class:`~multiprocessing.Lock` từ module :mod:`multiprocessing` để tuần tự hóa quyền truy cập vào tệp từ các tiến trình của mình. :class:`FileHandler` trong stdlib và các lớp con của nó không sử dụng :mod:`multiprocessing`.

.. currentmodule:: logging.handlers

Ngoài ra, bạn có thể sử dụng một ``Queue`` và một :class:`QueueHandler` để gửi tất cả các sự kiện logging đến một trong các tiến trình trong ứng dụng đa tiến trình của mình. Script ví dụ sau minh họa cách thực hiện việc này; trong ví dụ, một tiến trình listener riêng lắng nghe các sự kiện do những tiến trình khác gửi đến và ghi log theo cấu hình logging riêng của nó. Mặc dù ví dụ chỉ minh họa một cách thực hiện (chẳng hạn, bạn có thể muốn dùng một listener thread thay vì một tiến trình listener riêng — cách triển khai sẽ tương tự), nhưng nó cho phép áp dụng các cấu hình logging hoàn toàn khác nhau cho listener và các tiến trình khác trong ứng dụng của bạn, đồng thời có thể dùng làm cơ sở cho code đáp ứng các yêu cầu cụ thể của riêng bạn::

    # Bạn sẽ cần các import này trong mã của riêng mình
    import logging
    import logging.handlers
    import multiprocessing

    # Hai dòng import tiếp theo chỉ dành cho bản minh họa này
    from random import choice, random
    import time

    #
    # Vì bạn sẽ muốn định nghĩa các cấu hình logging cho listener và worker, các hàm
    # listener và worker process nhận một tham số configurer, là một callable
    # dùng để cấu hình logging cho process đó. Các hàm này cũng nhận queue,
    # mà chúng sử dụng để giao tiếp.
    #
    # Trên thực tế, bạn có thể cấu hình listener theo bất kỳ cách nào mình muốn, nhưng lưu ý rằng trong
    # ví dụ đơn giản, listener không áp dụng logic level hoặc filter cho các record nhận được.
    # Trong thực tế, có lẽ bạn sẽ muốn thực hiện logic này trong các worker process để tránh
    # gửi các event sẽ bị filter giữa các process.
    #
    # Kích thước của các tệp được xoay vòng được đặt nhỏ để bạn có thể dễ dàng xem kết quả.
    def listener_configurer():
        root = logging.getLogger()
        h = logging.handlers.RotatingFileHandler('mptest.log', 'a', 300, 10)
        f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
        h.setFormatter(f)
        root.addHandler(h)

    # Đây là vòng lặp cấp cao nhất của listener process: chờ các event logging
    # (LogRecords) trong queue và xử lý chúng, thoát khi nhận được None cho một
    # LogRecord.
    def listener_process(queue, configurer):
        configurer()
        while True:
            try:
                record = queue.get()
                if record is None:  # Gửi giá trị này như một sentinel để báo cho listener thoát.
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)  # Không áp dụng logic level hoặc filter - chỉ cần thực hiện!
            except Exception:
                import sys, traceback
                print('Whoops! Problem:', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    # Các array được dùng để chọn ngẫu nhiên trong demo này

    LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
              logging.ERROR, logging.CRITICAL]

    LOGGERS = ['a.b.c', 'd.e.f']

    MESSAGES = [
        'Random message #1',
        'Random message #2',
        'Random message #3',
    ]

    # Cấu hình worker được thực hiện khi bắt đầu chạy tiến trình worker.
    # Lưu ý rằng trên Windows, bạn không thể dựa vào ngữ nghĩa fork, vì vậy mỗi tiến trình
    # sẽ chạy mã cấu hình logging khi khởi động.
    def worker_configurer(queue):
        h = logging.handlers.QueueHandler(queue)  # Chỉ cần một handler
        root = logging.getLogger()
        root.addHandler(h)
        # gửi tất cả thông báo để minh họa; không áp dụng logic cấp độ hoặc bộ lọc nào khác.
        root.setLevel(logging.DEBUG)

    # Đây là vòng lặp cấp cao nhất của tiến trình worker, chỉ ghi nhật ký mười sự kiện với
    # các khoảng trễ ngẫu nhiên xen kẽ trước khi kết thúc.
    # Các thông báo print chỉ để bạn biết chương trình đang thực hiện một việc gì đó!
    def worker_process(queue, configurer):
        configurer(queue)
        name = multiprocessing.current_process().name
        print('Worker started: %s' % name)
        for i in range(10):
            time.sleep(random())
            logger = logging.getLogger(choice(LOGGERS))
            level = choice(LEVELS)
            message = choice(MESSAGES)
            logger.log(level, message)
        print('Worker finished: %s' % name)

    # Đây là nơi điều phối bản demo. Tạo queue, tạo và khởi động
    # listener, tạo mười worker và khởi động chúng, chờ chúng hoàn tất,
    # sau đó gửi None vào queue để báo cho listener kết thúc.
    def main():
        queue = multiprocessing.Queue(-1)
        listener = multiprocessing.Process(target=listener_process,
                                           args=(queue, listener_configurer))
        listener.start()
        workers = []
        for i in range(10):
            worker = multiprocessing.Process(target=worker_process,
                                             args=(queue, worker_configurer))
            workers.append(worker)
            worker.start()
        for w in workers:
            w.join()
        queue.put_nowait(None)
        listener.join()

    if __name__ == '__main__':
        main()

Một biến thể của script trên giữ việc ghi nhật ký trong tiến trình chính, ở một thread riêng::

    import logging
    import logging.config
    import logging.handlers
    from multiprocessing import Process, Queue
    import random
    import threading
    import time

    def logger_thread(q):
        while True:
            record = q.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)


    def worker_process(q):
        qh = logging.handlers.QueueHandler(q)
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(qh)
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
                  logging.CRITICAL]
        loggers = ['foo', 'foo.bar', 'foo.bar.baz',
                   'spam', 'spam.ham', 'spam.ham.eggs']
        for i in range(100):
            lvl = random.choice(levels)
            logger = logging.getLogger(random.choice(loggers))
            logger.log(lvl, 'Message no. %d', i)

    if __name__ == '__main__':
        q = Queue()
        d = {
            'version': 1,
            'formatters': {
                'detailed': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog.log',
                    'mode': 'w',
                    'formatter': 'detailed',
                },
                'foofile': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog-foo.log',
                    'mode': 'w',
                    'formatter': 'detailed',
                },
                'errors': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog-errors.log',
                    'mode': 'w',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                },
            },
            'loggers': {
                'foo': {
                    'handlers': ['foofile']
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console', 'file', 'errors']
            },
        }
        workers = []
        for i in range(5):
            wp = Process(target=worker_process, name='worker %d' % (i + 1), args=(q,))
            workers.append(wp)
            wp.start()
        logging.config.dictConfig(d)
        lp = threading.Thread(target=logger_thread, args=(q,))
        lp.start()
        # Đến đây, tiến trình chính có thể tự thực hiện một số công việc hữu ích
        # Sau khi hoàn tất, tiến trình này có thể chờ các worker kết thúc...
        for wp in workers:
            wp.join()
        # Bây giờ cũng yêu cầu thread ghi nhật ký hoàn tất
        q.put(None)
        lp.join()

Biến thể này cho thấy cách bạn có thể áp dụng cấu hình, chẳng hạn, cho các logger cụ thể
- chẳng hạn, logger ``foo`` có một handler đặc biệt lưu trữ tất cả các sự kiện trong
subsystem ``foo`` vào một file ``mplog-foo.log``. Cơ chế logging trong tiến trình chính sẽ sử dụng file này (mặc dù các sự kiện logging được tạo trong các tiến trình worker) để chuyển các thông báo đến những đích phù hợp.

Sử dụng concurrent.futures.ProcessPoolExecutor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu bạn muốn sử dụng :class:`concurrent.futures.ProcessPoolExecutor` để khởi động các worker process, bạn cần tạo queue theo cách hơi khác. Thay vì

.. code-block:: python

   queue = multiprocessing.Queue(-1)

bạn nên sử dụng

.. code-block:: python

   queue = multiprocessing.Manager().Queue(-1)  # cũng hoạt động với các ví dụ ở trên

sau đó bạn có thể thay thế việc tạo worker từ đoạn này::

    workers = []
    for i in range(10):
        worker = multiprocessing.Process(target=worker_process,
                                         args=(queue, worker_configurer))
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()

thành đoạn này (nhớ import :mod:`concurrent.futures` trước)::

    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for i in range(10):
            executor.submit(worker_process, queue, worker_configurer)

Triển khai ứng dụng web bằng Gunicorn và uWSGI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi deploy các ứng dụng web bằng `Gunicorn <https://gunicorn.org/>`_ hoặc `uWSGI <https://uwsgi-docs.readthedocs.io/en/latest/>`_ (hoặc công cụ tương tự), nhiều worker process được tạo để xử lý các request từ client. Trong những môi trường như vậy, tránh tạo trực tiếp các handler dựa trên tệp trong ứng dụng web. Thay vào đó, hãy sử dụng một
:class:`SocketHandler` để ghi log từ ứng dụng web đến một listener trong một process riêng biệt. Bạn có thể thiết lập việc này bằng một công cụ quản lý process như Supervisor - xem `Running a logging socket listener in production <Running a logging socket listener in production_>`_ để biết thêm chi tiết.


Sử dụng tính năng xoay tệp
--------------------------

.. sectionauthor:: Doug Hellmann, Vinay Sajip (changes)
.. (see <https://pymotw.com/3/logging/>)

Đôi khi, bạn muốn cho phép tệp log tăng đến một kích thước nhất định, sau đó mở một tệp mới và ghi log vào đó. Bạn có thể muốn giữ lại một số lượng tệp nhất định, và khi đã tạo đủ số lượng tệp đó, xoay các tệp để cả số lượng tệp lẫn kích thước tệp đều được giới hạn. Đối với mẫu sử dụng này, package logging cung cấp một :class:`RotatingFileHandler`::

   import glob
   import logging
   import logging.handlers

   LOG_FILENAME = 'logging_rotatingfile_example.out'

   # Thiết lập một logger cụ thể với mức output mong muốn
   my_logger = logging.getLogger('MyLogger')
   my_logger.setLevel(logging.DEBUG)

   # Thêm log message handler vào logger
   handler = logging.handlers.RotatingFileHandler(
                 LOG_FILENAME, maxBytes=20, backupCount=5)

   my_logger.addHandler(handler)

   # Ghi một số message
   for i in range(20):
       my_logger.debug('i = %d' % i)

   # Xem các tệp được tạo
   logfiles = glob.glob('%s*' % LOG_FILENAME)

   for filename in logfiles:
       print(filename)

Kết quả sẽ là 6 tệp riêng biệt, mỗi tệp chứa một phần lịch sử nhật ký của ứng dụng:

.. code-block:: none

   logging_rotatingfile_example.out
   logging_rotatingfile_example.out.1
   logging_rotatingfile_example.out.2
   logging_rotatingfile_example.out.3
   logging_rotatingfile_example.out.4
   logging_rotatingfile_example.out.5

Tệp hiện tại luôn là :file:`logging_rotatingfile_example.out`, và mỗi khi đạt đến giới hạn kích thước, tệp sẽ được đổi tên với hậu tố ``.1``. Mỗi tệp sao lưu hiện có sẽ được đổi tên để tăng hậu tố (``.1`` trở thành ``.2``, v.v.), còn tệp ``.6`` sẽ bị xóa.

Rõ ràng, ví dụ này đặt độ dài nhật ký quá nhỏ một cách cực đoan. Bạn nên đặt *maxBytes* thành một giá trị phù hợp.

.. currentmodule:: logging

.. _format-styles:

Sử dụng các kiểu định dạng thay thế
-----------------------------------

Khi chức năng ghi nhật ký được thêm vào thư viện chuẩn Python, cách duy nhất để định dạng thông báo có nội dung biến đổi là sử dụng phương pháp định dạng %. Kể từ đó, Python đã có thêm hai cách tiếp cận định dạng mới:
:class:`string.Template` (được thêm trong Python 2.4) và :meth:`str.format` (được thêm trong Python 2.6).

Logging (kể từ phiên bản 3.2) cung cấp hỗ trợ được cải thiện cho hai kiểu định dạng bổ sung này. Lớp :class:`Formatter` đã được nâng cấp để nhận thêm một tham số từ khóa tùy chọn có tên là ``style``. Giá trị mặc định là ``'%'``, nhưng các giá trị khả dụng khác là ``'{'`` và ``'$'``, tương ứng với hai kiểu định dạng còn lại. Theo mặc định, khả năng tương thích ngược vẫn được duy trì (như bạn mong đợi), nhưng bằng cách chỉ định rõ một tham số style, bạn có thể chỉ định các chuỗi định dạng hoạt động với
:meth:`str.format` hoặc :class:`string.Template`. Sau đây là một phiên console minh họa các khả năng này:

.. code-block:: pycon

    >>> import logging
    >>> root = logging.getLogger()
    >>> root.setLevel(logging.DEBUG)
    >>> handler = logging.StreamHandler()
    >>> bf = logging.Formatter('{asctime} {name} {levelname:8s} {message}',
    ...                        style='{')
    >>> handler.setFormatter(bf)
    >>> root.addHandler(handler)
    >>> logger = logging.getLogger('foo.bar')
    >>> logger.debug('This is a DEBUG message')
    2010-10-28 15:11:55,341 foo.bar DEBUG    This is a DEBUG message
    >>> logger.critical('This is a CRITICAL message')
    2010-10-28 15:12:11,526 foo.bar CRITICAL This is a CRITICAL message
    >>> df = logging.Formatter('$asctime $name ${levelname} $message',
    ...                        style='$')
    >>> handler.setFormatter(df)
    >>> logger.debug('This is a DEBUG message')
    2010-10-28 15:13:06,924 foo.bar DEBUG This is a DEBUG message
    >>> logger.critical('This is a CRITICAL message')
    2010-10-28 15:13:11,494 foo.bar CRITICAL This is a CRITICAL message
    >>>

Lưu ý rằng cách định dạng các thông báo logging khi xuất cuối cùng vào log hoàn toàn độc lập với cách xây dựng từng thông báo logging. Bạn vẫn có thể sử dụng %-formatting cho việc đó, như minh họa ở đây::

    >>> logger.error('This is an%s %s %s', 'other,', 'ERROR,', 'message')
    2010-10-28 15:19:29,833 foo.bar ERROR This is another, ERROR, message
    >>>

Các lệnh gọi logging (``logger.debug()``, ``logger.info()`` v.v.) chỉ nhận các tham số vị trí cho chính thông báo logging, còn các tham số từ khóa chỉ được dùng để xác định các tùy chọn xử lý lệnh gọi logging thực tế (ví dụ: tham số từ khóa ``exc_info`` để cho biết cần ghi thông tin traceback, hoặc tham số từ khóa ``extra`` để cho biết cần thêm thông tin ngữ cảnh). Vì vậy, bạn không thể trực tiếp thực hiện các lệnh gọi logging bằng :meth:`str.format` hoặc
cú pháp :class:`string.Template`, vì bên trong, package logging sử dụng %-formatting để hợp nhất chuỗi định dạng và các đối số biến. Không thể thay đổi điều này mà vẫn duy trì khả năng tương thích ngược, vì mọi lệnh gọi logging hiện có trong mã nguồn đều sẽ sử dụng các chuỗi định dạng %-format.

Tuy nhiên, có một cách để bạn sử dụng định dạng {} và $ để xây dựng từng thông báo log riêng lẻ. Hãy nhớ rằng đối với một thông báo, bạn có thể sử dụng một đối tượng tùy ý làm chuỗi định dạng thông báo, và package logging sẽ gọi ``str()`` trên đối tượng đó để lấy chuỗi định dạng thực tế. Hãy xem xét hai lớp sau::

    class BraceMessage:
        def __init__(self, fmt, /, *args, **kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args, **self.kwargs)

    class DollarMessage:
        def __init__(self, fmt, /, **kwargs):
            self.fmt = fmt
            self.kwargs = kwargs

        def __str__(self):
            from string import Template
            return Template(self.fmt).substitute(**self.kwargs)

Bạn có thể sử dụng một trong hai lớp này thay cho chuỗi định dạng, cho phép dùng định dạng {} hoặc $ để tạo phần "message" thực tế xuất hiện trong đầu ra log đã định dạng, thay cho "%(message)s", "{message}" hoặc "$message". Việc sử dụng tên lớp mỗi khi muốn ghi log hơi bất tiện, nhưng sẽ khá dễ dùng nếu bạn tạo một alias chẳng hạn như __ (hai dấu gạch dưới --- không nên nhầm với _, một dấu gạch dưới được dùng làm từ đồng nghĩa/alias cho :func:`gettext.gettext` hoặc các biến thể tương tự).

Các lớp trên không được tích hợp sẵn trong Python, dù chúng đủ dễ để sao chép và dán vào mã của riêng bạn. Bạn có thể sử dụng chúng như sau (giả sử chúng được khai báo trong một module có tên ``wherever``):

.. code-block:: pycon

    >>> from wherever import BraceMessage as __
    >>> print(__('Message with {0} {name}', 2, name='placeholders'))
    Message with 2 placeholders
    >>> class Point: pass
    ...
    >>> p = Point()
    >>> p.x = 0.5
    >>> p.y = 0.5
    >>> print(__('Message with coordinates: ({point.x:.2f}, {point.y:.2f})',
    ...       point=p))
    Message with coordinates: (0.50, 0.50)
    >>> from wherever import DollarMessage as __
    >>> print(__('Message with $num $what', num=2, what='placeholders'))
    Message with 2 placeholders
    >>>

Mặc dù các ví dụ trên sử dụng ``print()`` để minh họa cách hoạt động của việc định dạng, tất nhiên bạn sẽ sử dụng ``logger.debug()`` hoặc tương tự để thực sự ghi nhật ký theo cách tiếp cận này.

Một điều cần lưu ý là cách tiếp cận này không gây ảnh hưởng đáng kể đến hiệu năng: việc định dạng thực tế không diễn ra khi bạn gọi hàm ghi nhật ký, mà diễn ra khi (và nếu) thông báo đã ghi nhật ký thực sự sắp được một handler xuất ra log. Vì vậy, điều hơi bất thường duy nhất có thể khiến bạn nhầm lẫn là dấu ngoặc đơn bao quanh chuỗi định dạng và các đối số, chứ không chỉ chuỗi định dạng. Đó là vì ký hiệu __ chỉ là cú pháp viết tắt cho một lời gọi hàm khởi tạo đến một trong các lớp :samp:`{XXX}Message`.

Nếu muốn, bạn có thể sử dụng một :class:`LoggerAdapter` để đạt được hiệu ứng tương tự như trên, như trong ví dụ sau::

    import logging

    class Message:
        def __init__(self, fmt, args):
            self.fmt = fmt
            self.args = args

        def __str__(self):
            return self.fmt.format(*self.args)

    class StyleAdapter(logging.LoggerAdapter):
        def log(self, level, msg, /, *args, stacklevel=1, **kwargs):
            if self.isEnabledFor(level):
                msg, kwargs = self.process(msg, kwargs)
                self.logger.log(level, Message(msg, args), **kwargs,
                                stacklevel=stacklevel+1)

    logger = StyleAdapter(logging.getLogger(__name__))

    def main():
        logger.debug('Hello, {}', 'world!')

    if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG)
        main()

Khi chạy bằng Python 3.8 trở lên, đoạn mã trên sẽ ghi thông báo ``Hello, world!`` vào log.


.. currentmodule:: logging

.. _custom-logrecord:

Tùy chỉnh ``LogRecord``
-----------------------

Mỗi sự kiện ghi nhật ký được biểu diễn bằng một instance :class:`LogRecord`. Khi một sự kiện được ghi nhật ký và không bị lọc bởi level của logger, một
:class:`LogRecord` được tạo, điền thông tin về sự kiện, sau đó được chuyển đến các handler của logger đó (và các logger tổ tiên của nó, cho đến và bao gồm cả logger nơi việc truyền tiếp lên trong hệ phân cấp bị vô hiệu hóa). Trước Python 3.2, chỉ có hai nơi thực hiện việc tạo này:

* :meth:`Logger.makeRecord`, được gọi trong quy trình ghi log một sự kiện thông thường. Hàm này trực tiếp gọi :class:`LogRecord` để tạo một instance.
* :func:`makeLogRecord`, được gọi với một dictionary chứa các thuộc tính cần thêm vào LogRecord. Hàm này thường được gọi khi một dictionary phù hợp được nhận qua mạng (ví dụ: ở dạng pickle thông qua một :class:`~handlers.SocketHandler`, hoặc ở dạng JSON thông qua một
  :class:`~handlers.HTTPHandler`).

Điều này thường có nghĩa là nếu bạn cần thực hiện điều gì đó đặc biệt với một
:class:`LogRecord`, bạn phải thực hiện một trong các cách sau.

* Tạo lớp con :class:`Logger` của riêng bạn, lớp này ghi đè
  :meth:`Logger.makeRecord`, và thiết lập nó bằng :func:`~logging.setLoggerClass` trước khi khởi tạo bất kỳ logger nào mà bạn quan tâm.
* Thêm một :class:`Filter` vào logger hoặc handler, thực hiện thao tác đặc biệt cần thiết khi phương thức của nó
  :meth:`~Filter.filter` được gọi.

Cách tiếp cận đầu tiên sẽ hơi cồng kềnh trong trường hợp (chẳng hạn) một số thư viện khác nhau muốn thực hiện những việc khác nhau. Mỗi thư viện sẽ cố gắng đặt lớp con :class:`Logger` của riêng mình, và thư viện thực hiện việc này sau cùng sẽ chiếm ưu thế.

Cách tiếp cận thứ hai hoạt động khá tốt trong nhiều trường hợp, nhưng không cho phép bạn, chẳng hạn, sử dụng một lớp con chuyên biệt của :class:`LogRecord`. Các nhà phát triển thư viện có thể đặt một filter phù hợp trên các logger của mình, nhưng họ sẽ phải nhớ thực hiện việc này mỗi khi thêm một logger mới (bằng cách đơn giản là thêm các package hoặc module mới và thực hiện::

   logger = logging.getLogger(__name__)

ở cấp module). Có lẽ đây là thêm một việc cần phải ghi nhớ. Các nhà phát triển cũng có thể thêm filter vào một :class:`~logging.NullHandler` gắn với logger cấp cao nhất của họ, nhưng filter này sẽ không được gọi nếu nhà phát triển ứng dụng gắn một handler vào logger cấp thấp hơn của thư viện — vì vậy đầu ra từ handler đó sẽ không phản ánh ý định của nhà phát triển thư viện.

Trong Python 3.2 trở lên, việc tạo :class:`~logging.LogRecord` được thực hiện thông qua một factory mà bạn có thể chỉ định. Factory chỉ là một callable mà bạn có thể thiết lập bằng
:func:`~logging.setLogRecordFactory`, và truy vấn bằng
:func:`~logging.getLogRecordFactory`. Factory được gọi với cùng chữ ký như constructor :class:`~logging.LogRecord`, vì :class:`LogRecord` là thiết lập mặc định cho factory.

Cách tiếp cận này cho phép một factory tùy chỉnh kiểm soát mọi khía cạnh của việc tạo LogRecord. Ví dụ, bạn có thể trả về một subclass hoặc chỉ cần thêm một số thuộc tính bổ sung vào record sau khi tạo, bằng cách sử dụng một mẫu tương tự như sau::

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.custom_attribute = 0xdecafbad
        return record

    logging.setLogRecordFactory(record_factory)

Mẫu này cho phép các thư viện khác nhau nối tiếp các factory với nhau, và miễn là chúng không ghi đè lên thuộc tính của nhau hoặc vô tình ghi đè lên các thuộc tính được cung cấp theo tiêu chuẩn thì sẽ không có bất ngờ nào. Tuy nhiên, cần lưu ý rằng mỗi mắt xích trong chuỗi đều làm tăng run-time overhead cho mọi hoạt động logging, và chỉ nên sử dụng kỹ thuật này khi việc sử dụng :class:`Filter` không mang lại kết quả mong muốn.

.. currentmodule:: logging.handlers

.. _zeromq-handlers:

Phân lớp QueueHandler và QueueListener—một ví dụ về ZeroMQ
----------------------------------------------------------

Phân lớp ``QueueHandler``
^^^^^^^^^^^^^^^^^^^^^^^^^

Bạn có thể sử dụng một subclass của :class:`QueueHandler` để gửi thông báo đến các loại queue khác, chẳng hạn như socket 'publish' của ZeroMQ. Trong ví dụ dưới đây, socket được tạo riêng và truyền vào handler (dưới dạng 'queue')::

    import zmq   # sử dụng pyzmq, Python binding cho ZeroMQ
    import json  # để tuần tự hóa các record theo cách portable

    ctx = zmq.Context()
    sock = zmq.Socket(ctx, zmq.PUB)  # hoặc zmq.PUSH, hoặc giá trị phù hợp khác
    sock.bind('tcp://*:5556')        # hoặc bất cứ đâu

    class ZeroMQSocketHandler(QueueHandler):
        def enqueue(self, record):
            self.queue.send_json(record.__dict__)


    handler = ZeroMQSocketHandler(sock)


Tất nhiên, có những cách khác để tổ chức việc này, chẳng hạn như truyền dữ liệu cần thiết vào handler để tạo socket::

    class ZeroMQSocketHandler(QueueHandler):
        def __init__(self, uri, socktype=zmq.PUB, ctx=None):
            self.ctx = ctx or zmq.Context()
            socket = zmq.Socket(self.ctx, socktype)
            socket.bind(uri)
            super().__init__(socket)

        def enqueue(self, record):
            self.queue.send_json(record.__dict__)

        def close(self):
            self.queue.close()


Phân lớp ``QueueListener``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Bạn cũng có thể phân lớp :class:`QueueListener` để nhận thông báo từ các loại queue khác, chẳng hạn như socket 'subscribe' của ZeroMQ. Đây là một ví dụ::

    class ZeroMQSocketListener(QueueListener):
        def __init__(self, uri, /, *handlers, **kwargs):
            self.ctx = kwargs.get('ctx') or zmq.Context()
            socket = zmq.Socket(self.ctx, zmq.SUB)
            socket.setsockopt_string(zmq.SUBSCRIBE, '')  # subscribe mọi thứ
            socket.connect(uri)
            super().__init__(socket, *handlers, **kwargs)

        def dequeue(self):
            msg = self.queue.recv_json()
            return logging.makeLogRecord(msg)

.. _pynng-handlers:

Tạo lớp con cho QueueHandler và QueueListener - một ví dụ về ``pynng``
----------------------------------------------------------------------

Tương tự như phần trên, chúng ta có thể triển khai listener và handler bằng :pypi:`pynng`, một binding Python cho `NNG <https://nng.nanomsg.org/>`_, được xem là thế hệ kế nhiệm về mặt tinh thần của ZeroMQ. Các đoạn mã sau minh họa cách thực hiện -- bạn có thể thử chúng trong một môi trường đã cài đặt ``pynng``. Để đa dạng hơn, chúng tôi trình bày listener trước.


Phân lớp ``QueueListener``
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # listener.py
    import json
    import logging
    import logging.handlers

    import pynng

    DEFAULT_ADDR = "tcp://localhost:13232"

    interrupted = False

    class NNGSocketListener(logging.handlers.QueueListener):

        def __init__(self, uri, /, *handlers, **kwargs):
            # Đặt thời gian chờ để có thể ngắt, và mở một
            # socket subscriber
            socket = pynng.Sub0(listen=uri, recv_timeout=500)
            # Subscription b'' khớp với mọi topic
            topics = kwargs.pop('topics', None) or b''
            socket.subscribe(topics)
            # Coi socket như một hàng đợi
            super().__init__(socket, *handlers, **kwargs)

        def dequeue(self, block):
            data = None
            # Tiếp tục lặp khi chưa bị ngắt và chưa nhận được dữ liệu qua
            # socket
            while not interrupted:
                try:
                    data = self.queue.recv(block=block)
                    break
                except pynng.Timeout:
                    pass
                except pynng.Closed:  # đôi khi xảy ra khi bạn nhấn Ctrl-C
                    break
            if data is None:
                return None
            # Nhận sự kiện logging được gửi từ publisher
            event = json.loads(data.decode('utf-8'))
            return logging.makeLogRecord(event)

        def enqueue_sentinel(self):
            # Không được dùng trong cách triển khai này, vì socket thực sự không phải là một
            # hàng đợi
            pass

    logging.getLogger('pynng').propagate = False
    listener = NNGSocketListener(DEFAULT_ADDR, logging.StreamHandler(), topics=b'')
    listener.start()
    print('Press Ctrl-C to stop.')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        interrupted = True
    finally:
        listener.stop()


Phân lớp ``QueueHandler``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: logging

.. code-block:: python

    # sender.py
    import json
    import logging
    import logging.handlers
    import time
    import random

    import pynng

    DEFAULT_ADDR = "tcp://localhost:13232"

    class NNGSocketHandler(logging.handlers.QueueHandler):

        def __init__(self, uri):
            socket = pynng.Pub0(dial=uri, send_timeout=500)
            super().__init__(socket)

        def enqueue(self, record):
            # Gửi record dưới dạng JSON được mã hóa UTF-8
            d = dict(record.__dict__)
            data = json.dumps(d)
            self.queue.send(data.encode('utf-8'))

        def close(self):
            self.queue.close()

    logging.getLogger('pynng').propagate = False
    handler = NNGSocketHandler(DEFAULT_ADDR)
    # Đảm bảo đầu ra có chứa ID của process
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[logging.StreamHandler(), handler],
                        format='%(levelname)-8s %(name)10s %(process)6s %(message)s')
    levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL)
    logger_names = ('myapp', 'myapp.lib1', 'myapp.lib2')
    msgno = 1
    while True:
        # Chỉ cần chọn ngẫu nhiên một số logger và level rồi ghi log
        level = random.choice(levels)
        logger = logging.getLogger(random.choice(logger_names))
        logger.log(level, 'Message no. %5d' % msgno)
        msgno += 1
        delay = random.random() * 2 + 0.5
        time.sleep(delay)

Bạn có thể chạy hai đoạn mã trên trong các cửa sổ lệnh riêng biệt. Nếu chạy listener trong một cửa sổ và chạy sender trong hai cửa sổ riêng biệt, bạn sẽ thấy kết quả tương tự như sau. Trong cửa sổ sender thứ nhất:

.. code-block:: console

    $ python sender.py
    DEBUG         myapp    613 Message no.     1
    WARNING  myapp.lib2    613 Message no.     2
    CRITICAL myapp.lib2    613 Message no.     3
    WARNING  myapp.lib2    613 Message no.     4
    CRITICAL myapp.lib1    613 Message no.     5
    DEBUG         myapp    613 Message no.     6
    CRITICAL myapp.lib1    613 Message no.     7
    INFO     myapp.lib1    613 Message no.     8
    (and so on)

Trong cửa sổ sender thứ hai:

.. code-block:: console

    $ python sender.py
    INFO     myapp.lib2    657 Message no.     1
    CRITICAL myapp.lib2    657 Message no.     2
    CRITICAL      myapp    657 Message no.     3
    CRITICAL myapp.lib1    657 Message no.     4
    INFO     myapp.lib1    657 Message no.     5
    WARNING  myapp.lib2    657 Message no.     6
    CRITICAL      myapp    657 Message no.     7
    DEBUG    myapp.lib1    657 Message no.     8
    (and so on)

Trong listener shell:

.. code-block:: console

    $ python listener.py
    Press Ctrl-C to stop.
    DEBUG         myapp    613 Message no.     1
    WARNING  myapp.lib2    613 Message no.     2
    INFO     myapp.lib2    657 Message no.     1
    CRITICAL myapp.lib2    613 Message no.     3
    CRITICAL myapp.lib2    657 Message no.     2
    CRITICAL      myapp    657 Message no.     3
    WARNING  myapp.lib2    613 Message no.     4
    CRITICAL myapp.lib1    613 Message no.     5
    CRITICAL myapp.lib1    657 Message no.     4
    INFO     myapp.lib1    657 Message no.     5
    DEBUG         myapp    613 Message no.     6
    WARNING  myapp.lib2    657 Message no.     6
    CRITICAL      myapp    657 Message no.     7
    CRITICAL myapp.lib1    613 Message no.     7
    INFO     myapp.lib1    613 Message no.     8
    DEBUG    myapp.lib1    657 Message no.     8
    (and so on)

Như bạn có thể thấy, nhật ký từ hai tiến trình sender được xen kẽ trong đầu ra của listener.


Ví dụ về cấu hình dựa trên dictionary
-------------------------------------

Dưới đây là một ví dụ về dictionary cấu hình logging - được lấy từ `tài liệu <https://docs.djangoproject.com/en/stable/topics/logging/#configuring-logging>`_ trên dự án Django. Dictionary này được truyền vào :func:`~config.dictConfig` để áp dụng cấu hình::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'filters': {
            'special': {
                '()': 'project.logging.SpecialFilter',
                'foo': 'bar',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['special']
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'myproject.custom': {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
                'filters': ['special']
            }
        }
    }

Để biết thêm thông tin về cấu hình này, bạn có thể xem `phần liên quan <https://docs.djangoproject.com/en/stable/topics/logging/#configuring-logging>`_ trong tài liệu Django.

.. _cookbook-rotator-namer:

Sử dụng rotator và namer để tùy chỉnh quá trình xoay vòng log
-------------------------------------------------------------

Script có thể chạy sau đây minh họa cách bạn định nghĩa namer và rotator, đồng thời cho thấy cách nén tệp log bằng gzip::

    import gzip
    import logging
    import logging.handlers
    import os
    import shutil

    def namer(name):
        return name + ".gz"

    def rotator(source, dest):
        with open(source, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(source)


    rh = logging.handlers.RotatingFileHandler('rotated.log', maxBytes=128, backupCount=5)
    rh.rotator = rotator
    rh.namer = namer

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(rh)
    f = logging.Formatter('%(asctime)s %(message)s')
    rh.setFormatter(f)
    for i in range(1000):
        root.info(f'Message no. {i + 1}')

Sau khi chạy lệnh này, bạn sẽ thấy sáu tệp mới, trong đó có năm tệp được nén:

.. code-block:: shell-session

    $ ls rotated.log*
    rotated.log       rotated.log.2.gz  rotated.log.4.gz
    rotated.log.1.gz  rotated.log.3.gz  rotated.log.5.gz
    $ zcat rotated.log.1.gz
    2023-01-20 02:28:17,767 Message no. 996
    2023-01-20 02:28:17,767 Message no. 997
    2023-01-20 02:28:17,767 Message no. 998

Một ví dụ multiprocessing phức tạp hơn
--------------------------------------

Ví dụ hoạt động sau đây cho thấy cách sử dụng logging với multiprocessing bằng các tệp cấu hình. Các cấu hình khá đơn giản, nhưng giúp minh họa cách triển khai những cấu hình phức tạp hơn trong một kịch bản multiprocessing thực tế.

Trong ví dụ này, tiến trình chính tạo một tiến trình listener và một số tiến trình worker. Tiến trình chính, listener và các worker đều có ba cấu hình riêng biệt (tất cả worker dùng chung một cấu hình). Ta có thể thấy cách ghi log trong tiến trình chính, cách các worker ghi log vào một QueueHandler, cũng như cách listener triển khai một QueueListener và một cấu hình logging phức tạp hơn, đồng thời sắp xếp để chuyển các sự kiện nhận được qua queue đến các handler được chỉ định trong cấu hình. Lưu ý rằng các cấu hình này chỉ nhằm mục đích minh họa, nhưng bạn có thể điều chỉnh ví dụ này cho kịch bản của riêng mình.

Đây là script - hy vọng các docstring và comment sẽ giải thích cách script hoạt động::

    import logging
    import logging.config
    import logging.handlers
    from multiprocessing import Process, Queue, Event, current_process
    import os
    import random
    import time

    class MyHandler:
        """
        A simple handler for logging events. It runs in the listener process and
        dispatches events to loggers based on the name in the received record,
        which then get dispatched, by the logging system, to the handlers
        configured for those loggers.
        """

        def handle(self, record):
            if record.name == "root":
                logger = logging.getLogger()
            else:
                logger = logging.getLogger(record.name)

            if logger.isEnabledFor(record.levelno):
                # Biến đổi tên tiến trình chỉ để cho thấy đây là listener
                # thực hiện ghi log vào các tệp và console
                record.processName = '%s (for %s)' % (current_process().name, record.processName)
                logger.handle(record)

    def listener_process(q, stop_event, config):
        """
        This could be done in the main process, but is just done in a separate
        process for illustrative purposes.

        This initialises logging according to the specified configuration,
        starts the listener and waits for the main process to signal completion
        via the event. The listener is then stopped, and the process exits.
        """
        logging.config.dictConfig(config)
        listener = logging.handlers.QueueListener(q, MyHandler())
        listener.start()
        if os.name == 'posix':
            # Trên POSIX, setup logger đã được cấu hình trong tiến trình cha
            # nhưng lẽ ra đã bị vô hiệu hóa sau lệnh gọi
            # dictConfig.
            # Trên Windows, vì fork không được sử dụng, setup logger sẽ không
            # tồn tại trong tiến trình con, nên nó sẽ được tạo và thông báo
            # sẽ xuất hiện — do đó có mệnh đề "if posix".
            logger = logging.getLogger('setup')
            logger.critical('Should not appear, because of disabled logger ...')
        stop_event.wait()
        listener.stop()

    def worker_process(config):
        """
        A number of these are spawned for the purpose of illustration. In
        practice, they could be a heterogeneous bunch of processes rather than
        ones which are identical to each other.

        This initialises logging according to the specified configuration,
        and logs a hundred messages with random levels to randomly selected
        loggers.

        A small sleep is added to allow other processes a chance to run. This
        is not strictly needed, but it mixes the output from the different
        processes a bit more than if it's left out.
        """
        logging.config.dictConfig(config)
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
                  logging.CRITICAL]
        loggers = ['foo', 'foo.bar', 'foo.bar.baz',
                   'spam', 'spam.ham', 'spam.ham.eggs']
        if os.name == 'posix':
            # Trên POSIX, setup logger đã được cấu hình trong tiến trình cha
            # nhưng lẽ ra đã bị vô hiệu hóa sau lệnh gọi
            # dictConfig.
            # Trên Windows, vì fork không được sử dụng, setup logger sẽ không
            # tồn tại trong tiến trình con, nên nó sẽ được tạo và thông báo
            # sẽ xuất hiện — do đó có mệnh đề "if posix".
            logger = logging.getLogger('setup')
            logger.critical('Should not appear, because of disabled logger ...')
        for i in range(100):
            lvl = random.choice(levels)
            logger = logging.getLogger(random.choice(loggers))
            logger.log(lvl, 'Message no. %d', i)
            time.sleep(0.01)

    def main():
        q = Queue()
        # Tiến trình chính nhận một cấu hình đơn giản để in ra console.
        config_initial = {
            'version': 1,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO'
                }
            },
            'root': {
                'handlers': ['console'],
                'level': 'DEBUG'
            }
        }
        # Cấu hình của tiến trình worker chỉ là một QueueHandler được gắn vào
        # root logger, cho phép gửi tất cả thông báo vào queue.
        # Vô hiệu hóa các logger hiện có để vô hiệu hóa logger "setup" được sử dụng trong
        # process cha. Điều này cần thiết trên POSIX vì logger sẽ
        # có trong process con sau khi fork().
        config_worker = {
            'version': 1,
            'disable_existing_loggers': True,
            'handlers': {
                'queue': {
                    'class': 'logging.handlers.QueueHandler',
                    'queue': q
                }
            },
            'root': {
                'handlers': ['queue'],
                'level': 'DEBUG'
            }
        }
        # Cấu hình process listener cho thấy toàn bộ tính linh hoạt của
        # cấu hình logging đều khả dụng để phân phối các sự kiện đến các handler theo cách
        # bạn muốn.
        # Vô hiệu hóa các logger hiện có để vô hiệu hóa logger "setup" được sử dụng trong
        # process cha. Điều này cần thiết trên POSIX vì logger sẽ
        # có trong process con sau khi fork().
        config_listener = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'detailed': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                },
                'simple': {
                    'class': 'logging.Formatter',
                    'format': '%(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                    'level': 'INFO'
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog.log',
                    'mode': 'w',
                    'formatter': 'detailed'
                },
                'foofile': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog-foo.log',
                    'mode': 'w',
                    'formatter': 'detailed'
                },
                'errors': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog-errors.log',
                    'mode': 'w',
                    'formatter': 'detailed',
                    'level': 'ERROR'
                }
            },
            'loggers': {
                'foo': {
                    'handlers': ['foofile']
                }
            },
            'root': {
                'handlers': ['console', 'file', 'errors'],
                'level': 'DEBUG'
            }
        }
        # Ghi lại một số sự kiện ban đầu để cho thấy việc ghi log trong tiến trình cha hoạt động
        # bình thường.
        logging.config.dictConfig(config_initial)
        logger = logging.getLogger('setup')
        logger.info('About to create workers ...')
        workers = []
        for i in range(5):
            wp = Process(target=worker_process, name='worker %d' % (i + 1),
                         args=(config_worker,))
            workers.append(wp)
            wp.start()
            logger.info('Started worker: %s', wp.name)
        logger.info('About to create listener ...')
        stop_event = Event()
        lp = Process(target=listener_process, name='listener',
                     args=(q, stop_event, config_listener))
        lp.start()
        logger.info('Started listener')
        # Bây giờ chờ các worker hoàn tất công việc.
        for wp in workers:
            wp.join()
        # Tất cả worker đã hoàn tất, giờ có thể dừng việc lắng nghe.
        # Việc ghi log trong tiến trình cha vẫn hoạt động bình thường.
        logger.info('Telling listener to stop ...')
        stop_event.set()
        lp.join()
        logger.info('All done.')

    if __name__ == '__main__':
        main()


Chèn BOM vào các thông điệp được gửi đến SysLogHandler
------------------------------------------------------

:rfc:`5424` yêu cầu một thông điệp Unicode được gửi đến daemon syslog dưới dạng một tập hợp byte có cấu trúc sau: một thành phần chỉ gồm ASCII tùy chọn, tiếp theo là Byte Order Mark (BOM) UTF-8, tiếp theo là Unicode được mã hóa bằng UTF-8. (Xem
:rfc:`relevant section of the specification <5424#section-6>`.)

Trong Python 3.1, mã đã được thêm vào
:class:`~logging.handlers.SysLogHandler` để chèn BOM vào thông điệp, nhưng không may là nó được triển khai không đúng, khiến BOM xuất hiện ở đầu thông điệp và do đó không cho phép bất kỳ thành phần chỉ gồm ASCII nào xuất hiện trước nó.

Vì hành vi này bị lỗi, mã chèn BOM không đúng sẽ bị loại bỏ khỏi Python 3.2.4 trở lên. Tuy nhiên, mã này không được thay thế, và nếu bạn muốn tạo các thông điệp tuân thủ :rfc:`5424` có chứa BOM, một chuỗi chỉ gồm ASCII tùy chọn trước BOM và Unicode bất kỳ sau BOM, được mã hóa bằng UTF-8, thì bạn cần thực hiện như sau:

#. Gắn một instance :class:`~logging.Formatter` vào
   :class:`~logging.handlers.SysLogHandler` instance, với một format string chẳng hạn như::

      'ASCII section\ufeffUnicode section'

   Điểm mã Unicode U+FEFF, khi được mã hóa bằng UTF-8, sẽ được mã hóa thành BOM UTF-8 -- chuỗi byte ``b'\xef\xbb\xbf'``.

#. Thay thế phần ASCII bằng bất kỳ placeholder nào bạn muốn, nhưng hãy đảm bảo rằng dữ liệu xuất hiện ở đó sau khi thay thế luôn là ASCII (nhờ vậy, dữ liệu sẽ không thay đổi sau khi được mã hóa bằng UTF-8).

#. Thay thế phần Unicode bằng bất kỳ placeholder nào bạn muốn; nếu dữ liệu xuất hiện ở đó sau khi thay thế chứa các ký tự nằm ngoài phạm vi ASCII thì cũng không sao -- dữ liệu sẽ được mã hóa bằng UTF-8.

Thông báo đã được định dạng *sẽ* được mã hóa bằng UTF-8 bởi ``SysLogHandler``. Nếu tuân theo các quy tắc trên, bạn sẽ có thể tạo ra
các thông báo tuân thủ :rfc:`5424`. Nếu không, logging có thể không báo lỗi, nhưng các thông báo của bạn sẽ không tuân thủ RFC 5424 và daemon syslog của bạn có thể báo lỗi.


Triển khai structured logging
-----------------------------

Mặc dù hầu hết thông báo ghi nhật ký được viết để con người đọc, nên không dễ phân tích bằng máy, nhưng trong một số trường hợp, bạn có thể muốn xuất thông báo ở định dạng có cấu trúc mà *có khả năng* được một chương trình phân tích (mà không cần các biểu thức chính quy phức tạp để phân tích thông báo nhật ký). Việc này có thể dễ dàng thực hiện bằng package logging. Có một số cách để thực hiện, nhưng cách tiếp cận đơn giản sau đây sử dụng JSON để tuần tự hóa sự kiện theo cách mà máy có thể phân tích được::

    import json
    import logging

    class StructuredMessage:
        def __init__(self, message, /, **kwargs):
            self.message = message
            self.kwargs = kwargs

        def __str__(self):
            return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

    _ = StructuredMessage   # tùy chọn, để cải thiện khả năng đọc

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.info(_('message 1', foo='bar', bar='baz', num=123, fnum=123.456))

Nếu chạy script trên, kết quả in ra là:

.. code-block:: none

    message 1 >>> {"fnum": 123.456, "num": 123, "bar": "baz", "foo": "bar"}

Lưu ý rằng thứ tự của các mục có thể khác nhau tùy theo phiên bản Python được sử dụng.

Nếu cần xử lý chuyên biệt hơn, bạn có thể sử dụng một JSON encoder tùy chỉnh, như trong ví dụ hoàn chỉnh sau đây::

    import json
    import logging


    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, set):
                return tuple(o)
            elif isinstance(o, str):
                return o.encode('unicode_escape').decode('ascii')
            return super().default(o)

    class StructuredMessage:
        def __init__(self, message, /, **kwargs):
            self.message = message
            self.kwargs = kwargs

        def __str__(self):
            s = Encoder().encode(self.kwargs)
            return '%s >>> %s' % (self.message, s)

    _ = StructuredMessage   # tùy chọn, để cải thiện khả năng đọc

    def main():
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        logging.info(_('message 1', set_value={1, 2, 3}, snowman='\u2603'))

    if __name__ == '__main__':
        main()

Khi chạy script trên, kết quả in ra là:

.. code-block:: none

    message 1 >>> {"snowman": "\u2603", "set_value": [1, 2, 3]}

Lưu ý rằng thứ tự của các mục có thể khác nhau tùy theo phiên bản Python được sử dụng.


.. _custom-handlers:

.. currentmodule:: logging.config

Tùy chỉnh các handler bằng :func:`dictConfig`
---------------------------------------------

Đôi khi bạn muốn tùy chỉnh các logging handler theo những cách cụ thể, và nếu sử dụng :func:`dictConfig`, bạn có thể thực hiện việc này mà không cần tạo lớp con. Ví dụ, bạn có thể muốn thiết lập quyền sở hữu cho một tệp nhật ký. Trên POSIX, việc này dễ dàng thực hiện bằng :func:`shutil.chown`, nhưng các file handler trong stdlib không tích hợp sẵn tính năng hỗ trợ này. Bạn có thể tùy chỉnh việc tạo handler bằng một hàm thông thường như sau::

    def owned_file_handler(filename, mode='a', encoding=None, owner=None):
        if owner:
            if not os.path.exists(filename):
                open(filename, 'a').close()
            shutil.chown(filename, *owner)
        return logging.FileHandler(filename, mode, encoding)

Sau đó, trong cấu hình logging được truyền vào :func:`dictConfig`, bạn có thể chỉ định rằng một logging handler được tạo bằng cách gọi hàm này::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            },
        },
        'handlers': {
            'file':{
                # Các giá trị bên dưới sẽ được lấy ra khỏi dictionary này và
                # được dùng để tạo handler, thiết lập mức của handler và
                # formatter của nó.
                '()': owned_file_handler,
                'level':'DEBUG',
                'formatter': 'default',
                # Các giá trị dưới đây được truyền cho callable tạo handler
                # dưới dạng các đối số từ khóa.
                'owner': ['pulse', 'pulse'],
                'filename': 'chowntest.log',
                'mode': 'w',
                'encoding': 'utf-8',
            },
        },
        'root': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }

Trong ví dụ này, tôi thiết lập quyền sở hữu bằng người dùng và nhóm ``pulse``, chỉ nhằm mục đích minh họa. Ghép lại thành một script hoạt động, ``chowntest.py``::

    import logging, logging.config, os, shutil

    def owned_file_handler(filename, mode='a', encoding=None, owner=None):
        if owner:
            if not os.path.exists(filename):
                open(filename, 'a').close()
            shutil.chown(filename, *owner)
        return logging.FileHandler(filename, mode, encoding)

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            },
        },
        'handlers': {
            'file':{
                # Các giá trị bên dưới sẽ được lấy ra khỏi dictionary này và
                # được dùng để tạo handler, thiết lập mức của handler và
                # formatter của nó.
                '()': owned_file_handler,
                'level':'DEBUG',
                'formatter': 'default',
                # Các giá trị dưới đây được truyền cho callable tạo handler
                # dưới dạng các đối số từ khóa.
                'owner': ['pulse', 'pulse'],
                'filename': 'chowntest.log',
                'mode': 'w',
                'encoding': 'utf-8',
            },
        },
        'root': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }

    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('mylogger')
    logger.debug('A debug message')

Để chạy đoạn này, có lẽ bạn cần chạy dưới quyền ``root``:

.. code-block:: shell-session

    $ sudo python3.3 chowntest.py
    $ cat chowntest.log
    2013-11-05 09:34:51,128 DEBUG mylogger A debug message
    $ ls -l chowntest.log
    -rw-r--r-- 1 pulse pulse 55 2013-11-05 09:34 chowntest.log

Lưu ý rằng ví dụ này sử dụng Python 3.3 vì đây là phiên bản đầu tiên xuất hiện :func:`shutil.chown`. Cách tiếp cận này sẽ hoạt động với mọi phiên bản Python hỗ trợ :func:`dictConfig` - cụ thể là Python 2.7, 3.2 trở lên. Với các phiên bản trước 3.3, bạn sẽ cần triển khai việc thay đổi quyền sở hữu thực tế bằng cách, chẳng hạn như
:func:`os.chown`.

Trên thực tế, hàm tạo handler có thể nằm trong một module tiện ích nào đó trong project của bạn. Thay vì dòng trong cấu hình::

    '()': owned_file_handler,

bạn có thể dùng, chẳng hạn như::

    '()': 'ext://project.util.owned_file_handler',

trong đó ``project.util`` có thể được thay thế bằng tên thực tế của package chứa hàm. Trong script hoạt động ở trên, sử dụng ``'ext://__main__.owned_file_handler'`` sẽ phù hợp. Ở đây, callable thực tế được :func:`dictConfig` phân giải từ đặc tả ``ext://``.

Hy vọng ví dụ này cũng gợi ý cách bạn có thể triển khai các kiểu thay đổi file khác - chẳng hạn như thiết lập các bit quyền POSIX cụ thể - theo cùng cách, bằng cách sử dụng :func:`os.chmod`.

Tất nhiên, cách tiếp cận này cũng có thể được mở rộng cho các kiểu handler khác ngoài một
:class:`~logging.FileHandler` - chẳng hạn như một trong các rotating file handler hoặc hoàn toàn là một kiểu handler khác.


.. currentmodule:: logging

.. _formatting-styles:

Sử dụng các kiểu định dạng cụ thể trong toàn bộ ứng dụng của bạn
----------------------------------------------------------------

Trong Python 3.2, :class:`~logging.Formatter` đã được bổ sung tham số từ khóa ``style``, mặc dù mặc định là ``%`` để đảm bảo khả năng tương thích ngược, cho phép chỉ định ``{`` hoặc ``$`` nhằm hỗ trợ các phương thức định dạng được :meth:`str.format` và :class:`string.Template` hỗ trợ. Lưu ý rằng tham số này chi phối việc định dạng các thông báo logging để xuất ra log cuối cùng và hoàn toàn độc lập với cách một thông báo logging riêng lẻ được tạo.

Các lệnh gọi logging (:meth:`~Logger.debug`, :meth:`~Logger.info` v.v.) chỉ nhận các tham số vị trí cho chính thông báo logging, còn các tham số từ khóa chỉ được dùng để xác định các tùy chọn về cách xử lý lệnh gọi logging (ví dụ: tham số từ khóa ``exc_info`` để chỉ ra rằng thông tin traceback cần được ghi log, hoặc tham số từ khóa ``extra`` để chỉ ra thông tin ngữ cảnh bổ sung cần được thêm vào log). Vì vậy, bạn không thể trực tiếp thực hiện các lệnh gọi logging bằng cú pháp :meth:`str.format` hoặc :class:`string.Template`, vì bên trong, package logging sử dụng định dạng %-formatting để hợp nhất chuỗi định dạng và các đối số biến. Không thể thay đổi điều này mà vẫn đảm bảo khả năng tương thích ngược, vì tất cả các lệnh gọi logging hiện có trong mã nguồn đều sẽ sử dụng các chuỗi định dạng %-format.

Đã có những đề xuất gắn các kiểu định dạng với những logger cụ thể, nhưng cách tiếp cận đó cũng gặp phải các vấn đề về khả năng tương thích ngược, vì bất kỳ mã nguồn hiện có nào cũng có thể đang sử dụng một tên logger nhất định cùng với %-formatting.

Để logging hoạt động tương thích giữa mọi thư viện bên thứ ba và mã nguồn của bạn, các quyết định về định dạng cần được đưa ra ở cấp độ của từng lệnh gọi logging. Điều này mở ra một vài cách để hỗ trợ các kiểu định dạng thay thế.


Sử dụng các factory LogRecord
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trong Python 3.2, cùng với những thay đổi về :class:`~logging.Formatter` được đề cập ở trên, gói logging có thêm khả năng cho phép người dùng tự thiết lập
các lớp con :class:`LogRecord`, bằng cách sử dụng hàm :func:`setLogRecordFactory`. Bạn có thể dùng cách này để thiết lập lớp con riêng của :class:`LogRecord`, lớp này thực hiện đúng chức năng bằng cách ghi đè phương thức :meth:`~LogRecord.getMessage`. Phần triển khai phương thức này trong lớp cơ sở là nơi diễn ra việc định dạng ``msg % args``, và là nơi bạn có thể thay thế bằng cách định dạng khác; tuy nhiên, bạn nên đảm bảo hỗ trợ mọi kiểu định dạng và cho phép %-formatting làm mặc định để bảo đảm khả năng tương tác với mã khác. Bạn cũng cần chú ý gọi ``str(self.msg)``, giống như phần triển khai trong lớp cơ sở.

Xem tài liệu tham khảo về :func:`setLogRecordFactory` và
:class:`LogRecord` để biết thêm thông tin.


Sử dụng các đối tượng message tùy chỉnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có một cách khác, có lẽ đơn giản hơn, cho phép bạn sử dụng định dạng {} và $ để tạo từng message log riêng. Có thể bạn còn nhớ (từ
:ref:`arbitrary-object-messages`) rằng khi ghi nhật ký, bạn có thể sử dụng một đối tượng tùy ý làm chuỗi định dạng thông báo, và gói logging sẽ gọi
:func:`str` trên đối tượng đó để lấy chuỗi định dạng thực tế. Hãy xem xét hai lớp sau đây::

    class BraceMessage:
        def __init__(self, fmt, /, *args, **kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args, **self.kwargs)

    class DollarMessage:
        def __init__(self, fmt, /, **kwargs):
            self.fmt = fmt
            self.kwargs = kwargs

        def __str__(self):
            from string import Template
            return Template(self.fmt).substitute(**self.kwargs)

Bạn có thể sử dụng bất kỳ lớp nào trong hai lớp này thay cho chuỗi định dạng, cho phép dùng định dạng {} hoặc $ để tạo phần "message" thực tế, phần này sẽ xuất hiện trong đầu ra log đã định dạng thay cho “%(message)s” hoặc “{message}” hoặc “$message”. Nếu bạn thấy việc sử dụng tên lớp mỗi khi muốn ghi nhật ký hơi bất tiện, bạn có thể làm cho cách này dễ dùng hơn bằng cách sử dụng một bí danh như ``M`` hoặc ``_`` cho message (hoặc có thể là ``__``, nếu bạn đang sử dụng ``_`` để bản địa hóa).

Các ví dụ về cách tiếp cận này được đưa ra dưới đây. Trước tiên, định dạng bằng
:meth:`str.format`::

    >>> __ = BraceMessage
    >>> print(__('Message with {0} {1}', 2, 'placeholders'))
    Message with 2 placeholders
    >>> class Point: pass
    ...
    >>> p = Point()
    >>> p.x = 0.5
    >>> p.y = 0.5
    >>> print(__('Message with coordinates: ({point.x:.2f}, {point.y:.2f})', point=p))
    Message with coordinates: (0.50, 0.50)

Thứ hai, định dạng bằng :class:`string.Template`::

    >>> __ = DollarMessage
    >>> print(__('Message with $num $what', num=2, what='placeholders'))
    Message with 2 placeholders
    >>>

Điều cần lưu ý là cách tiếp cận này không gây tổn thất đáng kể về hiệu năng: việc định dạng thực tế không diễn ra khi bạn thực hiện lệnh gọi logging, mà diễn ra khi (và nếu) thông báo đã ghi thực sự sắp được một handler ghi ra log. Vì vậy, điều hơi bất thường duy nhất có thể khiến bạn gặp khó khăn là dấu ngoặc đơn bao quanh chuỗi định dạng và các đối số, chứ không chỉ riêng chuỗi định dạng. Đó là vì __ notation chỉ là cú pháp rút gọn cho một lời gọi hàm khởi tạo của một trong các lớp :samp:`{XXX}Message` được trình bày ở trên.


.. _filters-dictconfig:

.. currentmodule:: logging.config

Cấu hình filter bằng :func:`dictConfig`
---------------------------------------

Bạn *có thể* cấu hình các filter bằng :func:`~logging.config.dictConfig`, mặc dù thoạt nhìn có thể không rõ cách thực hiện (do đó có công thức này). Vì
:class:`~logging.Filter` là lớp filter duy nhất được cung cấp trong standard library và khó có thể đáp ứng nhiều yêu cầu (nó chỉ tồn tại dưới dạng lớp cơ sở), thông thường bạn sẽ cần định nghĩa một lớp con :class:`~logging.Filter` của riêng mình với phương thức :meth:`~logging.Filter.filter` được ghi đè. Để làm vậy, hãy chỉ định khóa ``()`` trong dictionary cấu hình của filter, với một callable sẽ được dùng để tạo filter (lớp là lựa chọn rõ ràng nhất, nhưng bạn có thể cung cấp bất kỳ callable nào trả về một
:class:`~logging.Filter` instance). Sau đây là một ví dụ hoàn chỉnh::

    import logging
    import logging.config
    import sys

    class MyFilter(logging.Filter):
        def __init__(self, param=None):
            self.param = param

        def filter(self, record):
            if self.param is None:
                allow = True
            else:
                allow = self.param not in record.msg
            if allow:
                record.msg = 'changed: ' + record.msg
            return allow

    LOGGING = {
        'version': 1,
        'filters': {
            'myfilter': {
                '()': MyFilter,
                'param': 'noshow',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'filters': ['myfilter']
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }

    if __name__ == '__main__':
        logging.config.dictConfig(LOGGING)
        logging.debug('hello')
        logging.debug('hello - noshow')

Ví dụ này cho thấy bạn có thể truyền dữ liệu cấu hình cho callable tạo instance dưới dạng các tham số keyword. Khi chạy, script trên sẽ in:

.. code-block:: none

    changed: hello

qua đó cho thấy filter đang hoạt động theo đúng cấu hình.

Có một vài điểm bổ sung cần lưu ý:

* Nếu bạn không thể tham chiếu trực tiếp đến callable trong cấu hình (ví dụ: nếu nó nằm trong một module khác và bạn không thể import trực tiếp tại nơi có dictionary cấu hình), bạn có thể sử dụng dạng ``ext://...`` như được mô tả trong :ref:`logging-config-dict-externalobj`. Ví dụ, trong ví dụ trên, bạn có thể đã sử dụng văn bản ``'ext://__main__.MyFilter'`` thay cho ``MyFilter``.

* Ngoài bộ lọc, kỹ thuật này cũng có thể được dùng để cấu hình các handler và formatter tùy chỉnh. Xem :ref:`logging-config-dict-userdef` để biết thêm thông tin về cách logging hỗ trợ sử dụng các đối tượng do người dùng định nghĩa trong cấu hình, và xem công thức cookbook khác :ref:`custom-handlers` ở trên.


.. _custom-format-exception:

Tùy chỉnh định dạng ngoại lệ
----------------------------

Có những lúc bạn muốn tùy chỉnh định dạng ngoại lệ—ví dụ, giả sử bạn muốn mỗi sự kiện được ghi log chỉ chiếm đúng một dòng, ngay cả khi có thông tin ngoại lệ. Bạn có thể thực hiện điều này bằng một lớp formatter tùy chỉnh, như trong ví dụ sau::

    import logging

    class OneLineExceptionFormatter(logging.Formatter):
        def formatException(self, exc_info):
            """
            Format an exception so that it prints on a single line.
            """
            result = super().formatException(exc_info)
            return repr(result)  # hoặc định dạng thành một dòng theo cách bạn muốn

        def format(self, record):
            s = super().format(record)
            if record.exc_text:
                s = s.replace('\n', '') + '|'
            return s

    def configure_logging():
        fh = logging.FileHandler('output.txt', 'w')
        f = OneLineExceptionFormatter('%(asctime)s|%(levelname)s|%(message)s|',
                                      '%d/%m/%Y %H:%M:%S')
        fh.setFormatter(f)
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(fh)

    def main():
        configure_logging()
        logging.info('Sample message')
        try:
            x = 1 / 0
        except ZeroDivisionError as e:
            logging.exception('ZeroDivisionError: %s', e)

    if __name__ == '__main__':
        main()

Khi chạy, đoạn mã này tạo ra một tệp có đúng hai dòng:

.. code-block:: none

    28/01/2015 07:21:23|INFO|Sample message|
    28/01/2015 07:21:23|ERROR|ZeroDivisionError: division by zero|'Traceback (most recent call last):\n  File "logtest7.py", line 30, in main\n    x = 1 / 0\nZeroDivisionError: division by zero'|

Mặc dù cách xử lý ở trên còn đơn giản, nó cho thấy cách định dạng thông tin ngoại lệ theo ý muốn. Mô-đun :mod:`traceback` có thể hữu ích cho các nhu cầu chuyên biệt hơn.

.. _spoken-messages:

Đọc thành tiếng các thông báo logging
-------------------------------------

Có thể có những tình huống trong đó việc hiển thị các thông báo ghi nhật ký ở dạng âm thanh thay vì dạng trực quan là điều mong muốn. Việc này rất dễ thực hiện nếu hệ thống của bạn có chức năng chuyển văn bản thành giọng nói (TTS), ngay cả khi hệ thống đó không có binding Python. Hầu hết các hệ thống TTS đều có một chương trình dòng lệnh mà bạn có thể chạy, và chương trình này có thể được gọi từ một handler bằng :mod:`subprocess`. Ở đây, giả định rằng các chương trình dòng lệnh TTS không yêu cầu tương tác với người dùng hoặc mất nhiều thời gian để hoàn tất, tần suất các thông báo ghi nhật ký không quá cao đến mức khiến người dùng bị dồn dập bởi các thông báo, và việc đọc các thông báo lần lượt thay vì đồng thời là chấp nhận được. Phần triển khai ví dụ dưới đây chờ một thông báo được đọc xong trước khi xử lý thông báo tiếp theo, điều này có thể khiến các handler khác phải chờ. Dưới đây là một ví dụ ngắn minh họa cách tiếp cận này, với giả định rằng gói TTS ``espeak`` khả dụng::

    import logging
    import subprocess
    import sys

    class TTSHandler(logging.Handler):
        def emit(self, record):
            msg = self.format(record)
            # Đọc chậm bằng giọng nữ tiếng Anh
            cmd = ['espeak', '-s150', '-ven+f3', msg]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            # chờ chương trình hoàn tất
            p.communicate()

    def configure_logging():
        h = TTSHandler()
        root = logging.getLogger()
        root.addHandler(h)
        # formatter mặc định chỉ trả về thông báo
        root.setLevel(logging.DEBUG)

    def main():
        logging.info('Hello')
        logging.debug('Goodbye')

    if __name__ == '__main__':
        configure_logging()
        sys.exit(main())

Khi chạy, script này sẽ đọc "Hello" rồi "Goodbye" bằng giọng nữ.

Tất nhiên, cách tiếp cận trên có thể được điều chỉnh cho các hệ thống TTS khác, thậm chí cho những hệ thống hoàn toàn khác có thể xử lý thông báo thông qua các chương trình bên ngoài được chạy từ dòng lệnh.


.. _buffered-logging:

Đệm các thông báo ghi nhật ký và xuất chúng có điều kiện
--------------------------------------------------------

Có thể có những tình huống bạn muốn ghi các thông báo vào một vùng tạm thời và chỉ xuất chúng khi một điều kiện nhất định xảy ra. Ví dụ: bạn có thể muốn bắt đầu ghi các sự kiện debug trong một hàm; nếu hàm hoàn tất mà không có lỗi, bạn không muốn làm rối log bằng thông tin debug đã thu thập, nhưng nếu có lỗi, bạn muốn xuất toàn bộ thông tin debug cùng với lỗi đó.

Dưới đây là một ví dụ cho thấy cách bạn có thể thực hiện việc này bằng cách sử dụng decorator cho các hàm mà bạn muốn logging hoạt động theo cách này. Ví dụ sử dụng
:class:`logging.handlers.MemoryHandler`, cho phép lưu đệm các sự kiện đã ghi cho đến khi một điều kiện nào đó xảy ra; khi đó, các sự kiện đã lưu đệm sẽ được ``flushed``
- chuyển đến một handler khác (handler ``target``) để xử lý. Theo mặc định,
``MemoryHandler`` được flush khi bộ đệm đầy hoặc khi gặp một sự kiện có level lớn hơn hoặc bằng một ngưỡng được chỉ định. Bạn có thể sử dụng công thức này với một subclass chuyên biệt hơn của ``MemoryHandler`` nếu muốn có hành vi flush tùy chỉnh.

Script ví dụ có một hàm đơn giản, ``foo``, chỉ lần lượt đi qua tất cả các level logging, ghi vào ``sys.stderr`` để cho biết nó sắp log ở level nào, rồi thực sự ghi một thông báo ở level đó. Bạn có thể truyền một tham số vào ``foo``; nếu tham số này là true, hàm sẽ log ở các level ERROR và CRITICAL; nếu không, hàm chỉ log ở các level DEBUG, INFO và WARNING.

Script chỉ cần gắn một decorator cho ``foo``, trong đó decorator này thực hiện việc logging có điều kiện cần thiết. Decorator nhận một logger làm tham số và gắn một memory handler trong suốt thời gian lời gọi đến hàm được decorate. Ngoài ra, bạn có thể cấu hình decorator bằng một target handler, một level tại đó việc flush sẽ xảy ra và một capacity cho bộ đệm (số lượng record được lưu đệm). Theo mặc định, các giá trị này lần lượt là :class:`~logging.StreamHandler` ghi vào ``sys.stderr``, ``logging.ERROR`` và ``100``.

Đây là script::

    import logging
    from logging.handlers import MemoryHandler
    import sys

    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    def log_if_errors(logger, target_handler=None, flush_level=None, capacity=None):
        if target_handler is None:
            target_handler = logging.StreamHandler()
        if flush_level is None:
            flush_level = logging.ERROR
        if capacity is None:
            capacity = 100
        handler = MemoryHandler(capacity, flushLevel=flush_level, target=target_handler)

        def decorator(fn):
            def wrapper(*args, **kwargs):
                logger.addHandler(handler)
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    logger.exception('call failed')
                    raise
                finally:
                    super(MemoryHandler, handler).flush()
                    logger.removeHandler(handler)
            return wrapper

        return decorator

    def write_line(s):
        sys.stderr.write('%s\n' % s)

    def foo(fail=False):
        write_line('about to log at DEBUG ...')
        logger.debug('Actually logged at DEBUG')
        write_line('about to log at INFO ...')
        logger.info('Actually logged at INFO')
        write_line('about to log at WARNING ...')
        logger.warning('Actually logged at WARNING')
        if fail:
            write_line('about to log at ERROR ...')
            logger.error('Actually logged at ERROR')
            write_line('about to log at CRITICAL ...')
            logger.critical('Actually logged at CRITICAL')
        return fail

    decorated_foo = log_if_errors(logger)(foo)

    if __name__ == '__main__':
        logger.setLevel(logging.DEBUG)
        write_line('Calling undecorated foo with False')
        assert not foo(False)
        write_line('Calling undecorated foo with True')
        assert foo(True)
        write_line('Calling decorated foo with False')
        assert not decorated_foo(False)
        write_line('Calling decorated foo with True')
        assert decorated_foo(True)

Khi chạy script này, bạn sẽ thấy kết quả sau:

.. code-block:: none

    Calling undecorated foo with False
    about to log at DEBUG ...
    about to log at INFO ...
    about to log at WARNING ...
    Calling undecorated foo with True
    about to log at DEBUG ...
    about to log at INFO ...
    about to log at WARNING ...
    about to log at ERROR ...
    about to log at CRITICAL ...
    Calling decorated foo with False
    about to log at DEBUG ...
    about to log at INFO ...
    about to log at WARNING ...
    Calling decorated foo with True
    about to log at DEBUG ...
    about to log at INFO ...
    about to log at WARNING ...
    about to log at ERROR ...
    Actually logged at DEBUG
    Actually logged at INFO
    Actually logged at WARNING
    Actually logged at ERROR
    about to log at CRITICAL ...
    Actually logged at CRITICAL

Như bạn có thể thấy, kết quả ghi nhật ký thực tế chỉ xuất hiện khi một sự kiện được ghi nhật ký có mức độ nghiêm trọng là ERROR hoặc cao hơn; tuy nhiên, trong trường hợp đó, mọi sự kiện trước đó có mức độ nghiêm trọng thấp hơn cũng được ghi nhật ký.

Tất nhiên, bạn có thể sử dụng các phương thức trang trí thông thường::

    @log_if_errors(logger)
    def foo(fail=False):
        ...


.. _buffered-smtp:

Gửi thông báo ghi nhật ký qua email cùng với bộ đệm
---------------------------------------------------

Để minh họa cách gửi thông báo nhật ký qua email, sao cho mỗi email chứa một số lượng thông báo nhất định, bạn có thể tạo lớp con của
:class:`~logging.handlers.BufferingHandler`. Trong ví dụ sau, bạn có thể điều chỉnh cho phù hợp với nhu cầu cụ thể của mình, một bộ kiểm thử đơn giản được cung cấp để cho phép bạn chạy script với các đối số dòng lệnh chỉ định những gì bạn thường cần để gửi dữ liệu qua SMTP. (Chạy script đã tải xuống với đối số ``-h`` để xem các đối số bắt buộc và tùy chọn.)

.. code-block:: python

    import logging
    import logging.handlers
    import smtplib

    class BufferingSMTPHandler(logging.handlers.BufferingHandler):
        def __init__(self, mailhost, port, username, password, fromaddr, toaddrs,
                     subject, capacity):
            logging.handlers.BufferingHandler.__init__(self, capacity)
            self.mailhost = mailhost
            self.mailport = port
            self.username = username
            self.password = password
            self.fromaddr = fromaddr
            if isinstance(toaddrs, str):
                toaddrs = [toaddrs]
            self.toaddrs = toaddrs
            self.subject = subject
            self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))

        def flush(self):
            if len(self.buffer) > 0:
                try:
                    smtp = smtplib.SMTP(self.mailhost, self.mailport)
                    smtp.starttls()
                    smtp.login(self.username, self.password)
                    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (self.fromaddr, ','.join(self.toaddrs), self.subject)
                    for record in self.buffer:
                        s = self.format(record)
                        msg = msg + s + "\r\n"
                    smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                    smtp.quit()
                except Exception:
                    if logging.raiseExceptions:
                        raise
                self.buffer = []

    if __name__ == '__main__':
        import argparse

        ap = argparse.ArgumentParser()
        aa = ap.add_argument
        aa('host', metavar='HOST', help='SMTP server')
        aa('--port', '-p', type=int, default=587, help='SMTP port')
        aa('user', metavar='USER', help='SMTP username')
        aa('password', metavar='PASSWORD', help='SMTP password')
        aa('to', metavar='TO', help='Addressee for emails')
        aa('sender', metavar='SENDER', help='Sender email address')
        aa('--subject', '-s',
           default='Test Logging email from Python logging module (buffering)',
           help='Subject of email')
        options = ap.parse_args()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        h = BufferingSMTPHandler(options.host, options.port, options.user,
                                 options.password, options.sender,
                                 options.to, options.subject, 10)
        logger.addHandler(h)
        for i in range(102):
            logger.info("Info index = %d", i)
        h.flush()
        h.close()

Nếu chạy script này và máy chủ SMTP của bạn được thiết lập chính xác, bạn sẽ thấy script gửi mười một email đến người nhận mà bạn chỉ định. Mười email đầu tiên mỗi email sẽ có mười thông báo nhật ký, còn email thứ mười một sẽ có hai thông báo. Tổng cộng là 102 thông báo như được chỉ định trong script.

.. _utc-formatting:

Định dạng thời gian bằng UTC (GMT) thông qua cấu hình
-----------------------------------------------------

Đôi khi bạn muốn định dạng thời gian bằng UTC; bạn có thể thực hiện việc này bằng một lớp như ``UTCFormatter``, được minh họa bên dưới::

    import logging
    import time

    class UTCFormatter(logging.Formatter):
        converter = time.gmtime

sau đó bạn có thể sử dụng ``UTCFormatter`` trong mã của mình thay cho
:class:`~logging.Formatter`. Nếu muốn thực hiện việc đó thông qua cấu hình, bạn có thể sử dụng API :func:`~logging.config.dictConfig` theo cách được minh họa trong ví dụ hoàn chỉnh sau đây::

    import logging
    import logging.config
    import time

    class UTCFormatter(logging.Formatter):
        converter = time.gmtime

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'utc': {
                '()': UTCFormatter,
                'format': '%(asctime)s %(message)s',
            },
            'local': {
                'format': '%(asctime)s %(message)s',
            }
        },
        'handlers': {
            'console1': {
                'class': 'logging.StreamHandler',
                'formatter': 'utc',
            },
            'console2': {
                'class': 'logging.StreamHandler',
                'formatter': 'local',
            },
        },
        'root': {
            'handlers': ['console1', 'console2'],
       }
    }

    if __name__ == '__main__':
        logging.config.dictConfig(LOGGING)
        logging.warning('The local time is %s', time.asctime())

Khi chạy script này, kết quả in ra sẽ tương tự như sau:

.. code-block:: none

    2015-10-17 12:53:29,501 The local time is Sat Oct 17 13:53:29 2015
    2015-10-17 13:53:29,501 The local time is Sat Oct 17 13:53:29 2015

cho thấy thời gian được định dạng cả theo giờ địa phương và UTC, mỗi handler một kiểu.


.. _context-manager:

Sử dụng context manager để logging có chọn lọc
----------------------------------------------

Có những lúc bạn cần tạm thời thay đổi cấu hình logging rồi khôi phục lại sau khi thực hiện một thao tác nào đó. Trong trường hợp này, context manager là cách rõ ràng nhất để lưu và khôi phục context của logging. Sau đây là một ví dụ đơn giản về context manager như vậy, cho phép bạn tùy chọn thay đổi mức logging và thêm một logging handler chỉ trong phạm vi của context manager::

    import logging
    import sys

    class LoggingContext:
        def __init__(self, logger, level=None, handler=None, close=True):
            self.logger = logger
            self.level = level
            self.handler = handler
            self.close = close

        def __enter__(self):
            if self.level is not None:
                self.old_level = self.logger.level
                self.logger.setLevel(self.level)
            if self.handler:
                self.logger.addHandler(self.handler)

        def __exit__(self, et, ev, tb):
            if self.level is not None:
                self.logger.setLevel(self.old_level)
            if self.handler:
                self.logger.removeHandler(self.handler)
            if self.handler and self.close:
                self.handler.close()
            # ngầm trả về None => không nuốt ngoại lệ

Nếu chỉ định một giá trị level, level của logger sẽ được đặt thành giá trị đó trong phạm vi của khối with được context manager bao phủ. Nếu chỉ định một handler, handler đó sẽ được thêm vào logger khi bắt đầu khối và bị xóa khi kết thúc khối. Bạn cũng có thể yêu cầu manager đóng handler khi thoát khỏi khối — bạn có thể làm vậy nếu không còn cần handler này nữa.

Để minh họa cách hoạt động, chúng ta có thể thêm khối mã sau vào phần mã ở trên::

    if __name__ == '__main__':
        logger = logging.getLogger('foo')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
        logger.info('1. This should appear just once on stderr.')
        logger.debug('2. This should not appear.')
        with LoggingContext(logger, level=logging.DEBUG):
            logger.debug('3. This should appear once on stderr.')
        logger.debug('4. This should not appear.')
        h = logging.StreamHandler(sys.stdout)
        with LoggingContext(logger, level=logging.DEBUG, handler=h, close=True):
            logger.debug('5. This should appear twice - once on stderr and once on stdout.')
        logger.info('6. This should appear just once on stderr.')
        logger.debug('7. This should not appear.')

Ban đầu, chúng ta đặt level của logger thành ``INFO``, vì vậy message #1 xuất hiện còn message #2 thì không. Sau đó, chúng ta tạm thời đổi level thành ``DEBUG`` trong khối ``with`` sau đây, vì vậy message #3 xuất hiện. Sau khi thoát khỏi khối, level của logger được khôi phục về ``INFO``, nên message #4 không xuất hiện. Trong khối ``with`` tiếp theo, chúng ta lại đặt level thành ``DEBUG``, đồng thời thêm một handler ghi vào ``sys.stdout``. Do đó, message #5 xuất hiện hai lần trên console (một lần thông qua ``stderr`` và một lần thông qua ``stdout``). Sau khi câu lệnh ``with`` hoàn tất, trạng thái trở về như trước, nên message #6 xuất hiện (giống message #1), còn message #7 thì không (giống message #2).

Nếu chạy script thu được, kết quả sẽ như sau:

.. code-block:: shell-session

    $ python logctx.py
    1. This should appear just once on stderr.
    3. This should appear once on stderr.
    5. This should appear twice - once on stderr and once on stdout.
    5. This should appear twice - once on stderr and once on stdout.
    6. This should appear just once on stderr.

Nếu chúng ta chạy lại, nhưng chuyển ``stderr`` vào ``/dev/null``, chúng ta thấy kết quả sau đây; đây là thông báo duy nhất được ghi vào ``stdout``:

.. code-block:: shell-session

    $ python logctx.py 2>/dev/null
    5. This should appear twice - once on stderr and once on stdout.

Một lần nữa, nhưng chuyển ``stdout`` vào ``/dev/null``, chúng ta nhận được:

.. code-block:: shell-session

    $ python logctx.py >/dev/null
    1. This should appear just once on stderr.
    3. This should appear once on stderr.
    5. This should appear twice - once on stderr and once on stdout.
    6. This should appear just once on stderr.

Trong trường hợp này, thông báo số 5 được in vào ``stdout`` không xuất hiện, đúng như mong đợi.

Tất nhiên, cách tiếp cận được mô tả ở đây có thể được khái quát hóa, chẳng hạn như để tạm thời đính kèm các bộ lọc logging. Lưu ý rằng đoạn mã trên hoạt động cả trong Python 2 và Python 3.


.. _starter-template:

Mẫu khởi đầu cho ứng dụng CLI
-----------------------------

Dưới đây là một ví dụ cho thấy bạn có thể:

* Sử dụng mức logging dựa trên các đối số dòng lệnh
* Điều phối đến nhiều subcommand trong các tệp riêng biệt, tất cả đều ghi log ở cùng một cấp độ theo cách nhất quán
* Sử dụng cấu hình đơn giản, tối thiểu

Giả sử chúng ta có một ứng dụng dòng lệnh có nhiệm vụ dừng, khởi động hoặc khởi động lại một số service. Để minh họa, ứng dụng này có thể được tổ chức thành một tệp ``app.py`` đóng vai trò là script chính của ứng dụng, với các lệnh riêng lẻ được triển khai trong ``start.py``, ``stop.py`` và ``restart.py``. Giả sử thêm rằng chúng ta muốn kiểm soát mức độ chi tiết của ứng dụng thông qua một đối số dòng lệnh, với giá trị mặc định là ``logging.INFO``. Đây là một cách để viết ``app.py``::

    import argparse
    import importlib
    import logging
    import os
    import sys

    def main(args=None):
        scriptname = os.path.basename(__file__)
        parser = argparse.ArgumentParser(scriptname)
        levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        parser.add_argument('--log-level', default='INFO', choices=levels)
        subparsers = parser.add_subparsers(dest='command',
                                           help='Available commands:')
        start_cmd = subparsers.add_parser('start', help='Start a service')
        start_cmd.add_argument('name', metavar='NAME',
                               help='Name of service to start')
        stop_cmd = subparsers.add_parser('stop',
                                         help='Stop one or more services')
        stop_cmd.add_argument('names', metavar='NAME', nargs='+',
                              help='Name of service to stop')
        restart_cmd = subparsers.add_parser('restart',
                                            help='Restart one or more services')
        restart_cmd.add_argument('names', metavar='NAME', nargs='+',
                                 help='Name of service to restart')
        options = parser.parse_args()
        # code để điều phối các lệnh có thể nằm toàn bộ trong tệp này. Nhằm mục đích
        # minh họa בלבד, chúng ta triển khai mỗi lệnh trong một module riêng biệt.
        try:
            mod = importlib.import_module(options.command)
            cmd = getattr(mod, 'command')
        except (ImportError, AttributeError):
            print('Unable to find the code for command \'%s\'' % options.command)
            return 1
        # Có thể làm phức tạp hơn ở đây và tải cấu hình từ tệp hoặc dictionary
        logging.basicConfig(level=options.log_level,
                            format='%(levelname)s %(name)s %(message)s')
        cmd(options)

    if __name__ == '__main__':
        sys.exit(main())

Các lệnh ``start``, ``stop`` và ``restart`` có thể được triển khai trong các module riêng biệt, như sau đối với lệnh khởi động::

    # start.py
    import logging

    logger = logging.getLogger(__name__)

    def command(options):
        logger.debug('About to start %s', options.name)
        # thực hiện xử lý lệnh tại đây ...
        logger.info('Started the \'%s\' service.', options.name)

và tương tự để dừng::

    # stop.py
    import logging

    logger = logging.getLogger(__name__)

    def command(options):
        n = len(options.names)
        if n == 1:
            plural = ''
            services = '\'%s\'' % options.names[0]
        else:
            plural = 's'
            services = ', '.join('\'%s\'' % name for name in options.names)
            i = services.rfind(', ')
            services = services[:i] + ' and ' + services[i + 2:]
        logger.debug('About to stop %s', services)
        # thực hiện xử lý lệnh tại đây ...
        logger.info('Stopped the %s service%s.', services, plural)

và tương tự để khởi động lại::

    # restart.py
    import logging

    logger = logging.getLogger(__name__)

    def command(options):
        n = len(options.names)
        if n == 1:
            plural = ''
            services = '\'%s\'' % options.names[0]
        else:
            plural = 's'
            services = ', '.join('\'%s\'' % name for name in options.names)
            i = services.rfind(', ')
            services = services[:i] + ' and ' + services[i + 2:]
        logger.debug('About to restart %s', services)
        # thực hiện xử lý lệnh tại đây ...
        logger.info('Restarted the %s service%s.', services, plural)

Nếu chạy ứng dụng này với cấp độ ghi nhật ký mặc định, chúng ta sẽ nhận được kết quả như sau:

.. code-block:: shell-session

    $ python app.py start foo
    INFO start Started the 'foo' service.

    $ python app.py stop foo bar
    INFO stop Stopped the 'foo' and 'bar' services.

    $ python app.py restart foo bar baz
    INFO restart Restarted the 'foo', 'bar' and 'baz' services.

Từ đầu tiên là cấp độ ghi nhật ký, còn từ thứ hai là tên module hoặc package của nơi sự kiện được ghi lại.

Nếu thay đổi cấp độ ghi nhật ký, chúng ta có thể thay đổi thông tin được gửi vào log. Ví dụ, nếu muốn có thêm thông tin:

.. code-block:: shell-session

    $ python app.py --log-level DEBUG start foo
    DEBUG start About to start foo
    INFO start Started the 'foo' service.

    $ python app.py --log-level DEBUG stop foo bar
    DEBUG stop About to stop 'foo' and 'bar'
    INFO stop Stopped the 'foo' and 'bar' services.

    $ python app.py --log-level DEBUG restart foo bar baz
    DEBUG restart About to restart 'foo', 'bar' and 'baz'
    INFO restart Restarted the 'foo', 'bar' and 'baz' services.

Còn nếu muốn ít thông tin hơn:

.. code-block:: shell-session

    $ python app.py --log-level WARNING start foo
    $ python app.py --log-level WARNING stop foo bar
    $ python app.py --log-level WARNING restart foo bar baz

Trong trường hợp này, các lệnh không in gì ra console, vì chúng không ghi nhật ký ở cấp độ ``WARNING`` hoặc cao hơn.

.. _qt-gui:

GUI Qt cho việc ghi nhật ký
---------------------------

Một câu hỏi thỉnh thoảng được đặt ra là làm thế nào để ghi log vào một ứng dụng GUI. Framework `Qt <https://www.qt.io/>`_ là một framework UI đa nền tảng phổ biến, có các binding Python sử dụng thư viện :pypi:`PySide2` hoặc :pypi:`PyQt5`.

Ví dụ sau đây minh họa cách ghi log vào một GUI Qt. Ví dụ này giới thiệu một lớp ``QtHandler`` đơn giản, nhận vào một callable, vốn phải là một slot trong main thread để thực hiện các cập nhật GUI. Một worker thread cũng được tạo để minh họa cách ghi log vào GUI từ chính UI (thông qua một nút để ghi log thủ công) cũng như từ một worker thread đang thực hiện công việc trong nền (ở đây chỉ ghi các thông báo ở những mức ngẫu nhiên, với khoảng thời gian trễ ngắn và ngẫu nhiên giữa các lần ghi).

Worker thread được triển khai bằng lớp ``QThread`` của Qt thay vì
module :mod:`threading`, vì có những trường hợp cần sử dụng ``QThread``, vốn cung cấp khả năng tích hợp tốt hơn với các component ``Qt`` khác.

Mã sẽ hoạt động với các bản phát hành gần đây của bất kỳ thư viện nào trong số ``PySide6``, ``PyQt6``, ``PySide2`` hoặc ``PyQt5``. Bạn có thể điều chỉnh cách tiếp cận này cho các phiên bản Qt cũ hơn. Vui lòng tham khảo các chú thích trong đoạn mã để biết thêm thông tin chi tiết.

.. code-block:: python3

    import logging
    import random
    import sys
    import time

    # Xử lý những khác biệt nhỏ giữa các package Qt khác nhau
    try:
        from PySide6 import QtCore, QtGui, QtWidgets
        Signal = QtCore.Signal
        Slot = QtCore.Slot
    except ImportError:
        try:
            from PyQt6 import QtCore, QtGui, QtWidgets
            Signal = QtCore.pyqtSignal
            Slot = QtCore.pyqtSlot
        except ImportError:
            try:
                from PySide2 import QtCore, QtGui, QtWidgets
                Signal = QtCore.Signal
                Slot = QtCore.Slot
            except ImportError:
                from PyQt5 import QtCore, QtGui, QtWidgets
                Signal = QtCore.pyqtSignal
                Slot = QtCore.pyqtSlot

    logger = logging.getLogger(__name__)


    #
    # Các signal cần được chứa trong một QObject hoặc lớp con để được xử lý chính xác
    # đã được khởi tạo.
    #
    class Signaller(QtCore.QObject):
        signal = Signal(str, logging.LogRecord)

    #
    # Việc xuất ra Qt GUI chỉ nên được thực hiện trên main thread. Vì vậy, đây là
    # handler được thiết kế để nhận một hàm slot được thiết lập để chạy trên main
    # thread. Trong ví dụ này, hàm nhận một đối số chuỗi là
    # thông báo log đã được định dạng và log record đã tạo ra nó. Chuỗi đã được định dạng
    # chỉ là một tiện ích - bạn có thể định dạng chuỗi để xuất ra theo bất kỳ cách nào
    # bạn muốn ngay trong hàm slot.
    #
    # Bạn chỉ định hàm slot để thực hiện mọi cập nhật GUI mong muốn. Handler
    # không biết hoặc không quan tâm đến các phần tử UI cụ thể.
    #
    class QtHandler(logging.Handler):
        def __init__(self, slotfunc, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.signaller = Signaller()
            self.signaller.signal.connect(slotfunc)

        def emit(self, record):
            s = self.format(record)
            self.signaller.signal.emit(s, record)

    #
    # Ví dụ này sử dụng QThreads, nghĩa là các thread ở cấp Python
    # được đặt tên dạng như "Dummy-1". Hàm bên dưới lấy tên Qt của
    # thread hiện tại.
    #
    def ctname():
        return QtCore.QThread.currentThread().objectName()


    #
    # Dùng để tạo các level ngẫu nhiên cho việc logging.
    #
    LEVELS = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL)

    #
    # Lớp worker này đại diện cho công việc được thực hiện trong một thread riêng với
    # luồng chính. Cách khởi chạy luồng để thực hiện công việc là thông qua thao tác nhấn nút
    # kết nối với một slot trong worker.
    #
    # Vì giá trị threadName mặc định trong LogRecord không hữu ích lắm, chúng ta thêm
    # qThreadName chứa tên QThread được tính như trên, rồi truyền giá trị đó trong
    # một dictionary "extra" dùng để cập nhật LogRecord với tên
    # QThread.
    #
    # Worker trong ví dụ này chỉ tuần tự xuất các thông báo, xen kẽ với
    # các khoảng trễ ngẫu nhiên cỡ vài giây.
    #
    class Worker(QtCore.QObject):
        @Slot()
        def start(self):
            extra = {'qThreadName': ctname() }
            logger.debug('Started work', extra=extra)
            i = 1
            # Cho thread chạy cho đến khi bị ngắt. Điều này cho phép kết thúc thread tương đối gọn gàng
            # .
            while not QtCore.QThread.currentThread().isInterruptionRequested():
                delay = 0.5 + random.random() * 2
                time.sleep(delay)
                try:
                    if random.random() < 0.1:
                        raise ValueError('Exception raised: %d' % i)
                    else:
                        level = random.choice(LEVELS)
                        logger.log(level, 'Message after delay of %3.1f: %d', delay, i, extra=extra)
                except ValueError as e:
                    logger.exception('Failed: %s', e, extra=extra)
                i += 1

    #
    # Triển khai một UI đơn giản cho ví dụ trong cookbook này. Thành phần gồm:
    #
    # * Một cửa sổ soạn thảo văn bản chỉ đọc chứa các thông báo log đã định dạng
    # * Một nút để bắt đầu công việc và ghi log trong một thread riêng
    # * Một nút để ghi log một nội dung nào đó từ main thread
    # * Nút để xóa cửa sổ log
    #
    class Window(QtWidgets.QWidget):

        COLORS = {
            logging.DEBUG: 'black',
            logging.INFO: 'blue',
            logging.WARNING: 'orange',
            logging.ERROR: 'red',
            logging.CRITICAL: 'purple',
        }

        def __init__(self, app):
            super().__init__()
            self.app = app
            self.textedit = te = QtWidgets.QPlainTextEdit(self)
            # Đặt phông chữ monospace mặc định của nền tảng
            f = QtGui.QFont('nosuchfont')
            if hasattr(f, 'Monospace'):
                f.setStyleHint(f.Monospace)
            else:
                f.setStyleHint(f.StyleHint.Monospace)  # cho Qt6
            te.setFont(f)
            te.setReadOnly(True)
            PB = QtWidgets.QPushButton
            self.work_button = PB('Start background work', self)
            self.log_button = PB('Log a message at a random level', self)
            self.clear_button = PB('Clear log window', self)
            self.handler = h = QtHandler(self.update_status)
            # Nhớ dùng qThreadName thay vì threadName trong chuỗi định dạng.
            fs = '%(asctime)s %(qThreadName)-12s %(levelname)-8s %(message)s'
            formatter = logging.Formatter(fs)
            h.setFormatter(formatter)
            logger.addHandler(h)
            # Thiết lập để kết thúc QThread khi thoát
            app.aboutToQuit.connect(self.force_quit)

            # Bố trí tất cả widget
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(te)
            layout.addWidget(self.work_button)
            layout.addWidget(self.log_button)
            layout.addWidget(self.clear_button)
            self.setFixedSize(900, 400)

            # Kết nối các slot và signal không thuộc worker
            self.log_button.clicked.connect(self.manual_update)
            self.clear_button.clicked.connect(self.clear_display)

            # Khởi động một worker thread mới và kết nối các slot cho worker
            self.start_thread()
            self.work_button.clicked.connect(self.worker.start)
            # Sau khi khởi động, nút này sẽ bị vô hiệu hóa
            self.work_button.clicked.connect(lambda : self.work_button.setEnabled(False))

        def start_thread(self):
            self.worker = Worker()
            self.worker_thread = QtCore.QThread()
            self.worker.setObjectName('Worker')
            self.worker_thread.setObjectName('WorkerThread')  # cho qThreadName
            self.worker.moveToThread(self.worker_thread)
            # Thao tác này sẽ khởi động một event loop trong worker thread
            self.worker_thread.start()

        def kill_thread(self):
            # Chỉ cần yêu cầu worker dừng, sau đó yêu cầu nó thoát và chờ việc đó
            # xảy ra
            self.worker_thread.requestInterruption()
            if self.worker_thread.isRunning():
                self.worker_thread.quit()
                self.worker_thread.wait()
            else:
                print('worker has already exited.')

        def force_quit(self):
            # Dùng khi cửa sổ được đóng
            if self.worker_thread.isRunning():
                self.kill_thread()

        # Các hàm dưới đây cập nhật UI và chạy trên main thread vì
        # đó là nơi các slot được thiết lập

        @Slot(str, logging.LogRecord)
        def update_status(self, status, record):
            color = self.COLORS.get(record.levelno, 'black')
            s = '<pre><font color="%s">%s</font></pre>' % (color, status)
            self.textedit.appendHtml(s)

        @Slot()
        def manual_update(self):
            # Hàm này sử dụng thông báo đã truyền vào ở dạng đã định dạng, nhưng cũng sử dụng
            # thông tin từ bản ghi để định dạng thông báo theo một
            # màu phù hợp với mức độ nghiêm trọng (level) của nó.
            level = random.choice(LEVELS)
            extra = {'qThreadName': ctname() }
            logger.log(level, 'Manually logged!', extra=extra)

        @Slot()
        def clear_display(self):
            self.textedit.clear()


    def main():
        QtCore.QThread.currentThread().setObjectName('MainThread')
        logging.getLogger().setLevel(logging.DEBUG)
        app = QtWidgets.QApplication(sys.argv)
        example = Window(app)
        example.show()
        if hasattr(app, 'exec'):
            rc = app.exec()
        else:
            rc = app.exec_()
        sys.exit(rc)

    if __name__=='__main__':
        main()

Ghi log vào syslog với hỗ trợ RFC5424
-------------------------------------

Mặc dù :rfc:`5424` có từ năm 2009, hầu hết các máy chủ syslog được cấu hình mặc định để sử dụng :rfc:`3164` cũ hơn, ra đời năm 2001. Khi ``logging`` được thêm vào Python năm 2003, nó hỗ trợ giao thức trước đó (và là giao thức duy nhất tồn tại) tại thời điểm đó. Kể từ khi RFC 5424 được công bố, do giao thức này chưa được triển khai rộng rãi trên các máy chủ syslog, chức năng :class:`~logging.handlers.SysLogHandler` vẫn chưa được cập nhật.

RFC 5424 có một số tính năng hữu ích, chẳng hạn như hỗ trợ dữ liệu có cấu trúc; nếu bạn cần ghi nhật ký vào một máy chủ syslog có hỗ trợ tính năng này, bạn có thể thực hiện bằng một handler được phân lớp, có dạng tương tự như sau::

    import datetime as dt
    import logging.handlers
    import re
    import socket
    import time

    class SysLogHandler5424(logging.handlers.SysLogHandler):

        tz_offset = re.compile(r'([+-]\d{2})(\d{2})$')
        escaped = re.compile(r'([\]"\\])')

        def __init__(self, *args, **kwargs):
            self.msgid = kwargs.pop('msgid', None)
            self.appname = kwargs.pop('appname', None)
            super().__init__(*args, **kwargs)

        def format(self, record):
            version = 1
            asctime = dt.datetime.fromtimestamp(record.created).isoformat()
            m = self.tz_offset.match(time.strftime('%z'))
            has_offset = False
            if m and time.timezone:
                hrs, mins = m.groups()
                if int(hrs) or int(mins):
                    has_offset = True
            if not has_offset:
                asctime += 'Z'
            else:
                asctime += f'{hrs}:{mins}'
            try:
                hostname = socket.gethostname()
            except Exception:
                hostname = '-'
            appname = self.appname or '-'
            procid = record.process
            msgid = '-'
            msg = super().format(record)
            sdata = '-'
            if hasattr(record, 'structured_data'):
                sd = record.structured_data
                # Đây phải là một dict trong đó các khóa là SD-ID và giá trị là một
                # dict ánh xạ PARAM-NAME với PARAM-VALUE (hãy tham khảo RFC để biết các giá trị này
                # có nghĩa là gì)
                # Ở đây không có kiểm tra lỗi—đoạn mã này chỉ nhằm mục đích minh họa, và bạn
                # có thể điều chỉnh đoạn mã này để sử dụng trong môi trường production
                parts = []

                def replacer(m):
                    g = m.groups()
                    return '\\' + g[0]

                for sdid, dv in sd.items():
                    part = f'[{sdid}'
                    for k, v in dv.items():
                        s = str(v)
                        s = self.escaped.sub(replacer, s)
                        part += f' {k}="{s}"'
                    part += ']'
                    parts.append(part)
                sdata = ''.join(parts)
            return f'{version} {asctime} {hostname} {appname} {procid} {msgid} {sdata} {msg}'

Bạn cần quen thuộc với RFC 5424 để hiểu đầy đủ đoạn mã trên, và có thể bạn có những nhu cầu hơi khác (ví dụ: cách bạn truyền dữ liệu có cấu trúc vào log). Tuy vậy, bạn vẫn có thể điều chỉnh đoạn mã trên cho phù hợp với nhu cầu cụ thể của mình. Với handler trên, bạn sẽ truyền dữ liệu có cấu trúc bằng cách tương tự như sau::

    sd = {
        'foo@12345': {'bar': 'baz', 'baz': 'bozz', 'fizz': r'buzz'},
        'foo@54321': {'rab': 'baz', 'zab': 'bozz', 'zzif': r'buzz'}
    }
    extra = {'structured_data': sd}
    i = 1
    logger.debug('Message %d', i, extra=extra)

Cách sử dụng logger như một output stream
-----------------------------------------

Đôi khi, bạn cần tương tác với một API của bên thứ ba yêu cầu một đối tượng dạng tệp để ghi dữ liệu vào, nhưng bạn muốn chuyển đầu ra của API đến một logger. Bạn có thể thực hiện việc này bằng một class bao bọc logger với API dạng tệp. Sau đây là một script ngắn minh họa cho class đó:

.. code-block:: python

    import logging

    class LoggerWriter:
        def __init__(self, logger, level):
            self.logger = logger
            self.level = level

        def write(self, message):
            if message != '\n':  # tránh in các dòng mới trống nếu muốn
                self.logger.log(self.level, message)

        def flush(self):
            # thực ra không làm gì, nhưng có thể được mong đợi ở một đối tượng dạng tệp
            # object - nên tùy trường hợp mà có thể bỏ qua
            pass

        def close(self):
            # thực ra không làm gì, nhưng có thể được mong đợi ở một đối tượng dạng tệp
            # object - nên tùy trường hợp mà có thể bỏ qua. Bạn có thể muốn
            # đặt một cờ để các lần gọi write sau đó phát sinh ngoại lệ
            pass

    def main():
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger('demo')
        info_fp = LoggerWriter(logger, logging.INFO)
        debug_fp = LoggerWriter(logger, logging.DEBUG)
        print('An INFO message', file=info_fp)
        print('A DEBUG message', file=debug_fp)

    if __name__ == "__main__":
        main()

Khi chạy script này, nó sẽ in ra

.. code-block:: text

    INFO:demo:An INFO message
    DEBUG:demo:A DEBUG message

Bạn cũng có thể sử dụng ``LoggerWriter`` để chuyển hướng ``sys.stdout`` và ``sys.stderr`` bằng cách làm như sau:

.. code-block:: python

    import sys

    sys.stdout = LoggerWriter(logger, logging.INFO)
    sys.stderr = LoggerWriter(logger, logging.WARNING)

Bạn nên thực hiện việc này *sau khi* cấu hình logging theo nhu cầu của mình. Trong ví dụ trên, lời gọi :func:`~logging.basicConfig` thực hiện việc này (sử dụng giá trị ``sys.stderr`` *trước khi* nó bị ghi đè bởi một instance ``LoggerWriter``). Sau đó, bạn sẽ nhận được kết quả như sau:

.. code-block:: pycon

    >>> print('Foo')
    INFO:demo:Foo
    >>> print('Bar', file=sys.stderr)
    WARNING:demo:Bar
    >>>

Tất nhiên, các ví dụ trên hiển thị đầu ra theo định dạng được sử dụng bởi
:func:`~logging.basicConfig`, nhưng bạn có thể sử dụng formatter khác khi cấu hình logging.

Lưu ý rằng với sơ đồ trên, bạn phần nào phụ thuộc vào buffering và chuỗi các lần gọi write mà bạn đang intercept. Ví dụ, với định nghĩa của ``LoggerWriter`` ở trên, nếu bạn có đoạn mã

.. code-block:: python

    sys.stderr = LoggerWriter(logger, logging.WARNING)
    1 / 0

sau đó chạy script sẽ cho kết quả là

.. code-block:: text

    WARNING:demo:Traceback (most recent call last):

    WARNING:demo:  File "/home/runner/cookbook-loggerwriter/test.py", line 53, in <module>

    WARNING:demo:
    WARNING:demo:main()
    WARNING:demo:  File "/home/runner/cookbook-loggerwriter/test.py", line 49, in main

    WARNING:demo:
    WARNING:demo:1 / 0
    WARNING:demo:ZeroDivisionError
    WARNING:demo::
    WARNING:demo:division by zero

Như bạn có thể thấy, kết quả này chưa lý tưởng. Đó là vì mã bên dưới ghi vào ``sys.stderr`` thực hiện nhiều lần ghi, và mỗi lần ghi lại tạo ra một dòng nhật ký riêng (ví dụ: ba dòng cuối ở trên). Để khắc phục vấn đề này, bạn cần đệm dữ liệu và chỉ xuất các dòng nhật ký khi gặp ký tự xuống dòng. Hãy sử dụng một cách triển khai ``LoggerWriter`` tốt hơn một chút:

.. code-block:: python

    class BufferingLoggerWriter(LoggerWriter):
        def __init__(self, logger, level):
            super().__init__(logger, level)
            self.buffer = ''

        def write(self, message):
            if '\n' not in message:
                self.buffer += message
            else:
                parts = message.split('\n')
                if self.buffer:
                    s = self.buffer + parts.pop(0)
                    self.logger.log(self.level, s)
                self.buffer = parts.pop()
                for part in parts:
                    self.logger.log(self.level, part)

Cách này chỉ đệm dữ liệu cho đến khi gặp ký tự xuống dòng, rồi ghi các dòng hoàn chỉnh vào nhật ký. Với cách tiếp cận này, kết quả sẽ tốt hơn:

.. code-block:: text

    WARNING:demo:Traceback (most recent call last):
    WARNING:demo:  File "/home/runner/cookbook-loggerwriter/main.py", line 55, in <module>
    WARNING:demo:    main()
    WARNING:demo:  File "/home/runner/cookbook-loggerwriter/main.py", line 52, in main
    WARNING:demo:    1/0
    WARNING:demo:ZeroDivisionError: division by zero

Cách xử lý thống nhất các ký tự xuống dòng trong kết quả ghi nhật ký
--------------------------------------------------------------------

Thông thường, các thông báo được ghi vào nhật ký (chẳng hạn như vào console hoặc tệp) chỉ gồm một dòng văn bản. Tuy nhiên, đôi khi cần xử lý các thông báo nhiều dòng — có thể vì chuỗi định dạng ghi nhật ký chứa ký tự xuống dòng hoặc dữ liệu được ghi chứa ký tự xuống dòng. Nếu muốn xử lý thống nhất các thông báo như vậy, để mỗi dòng trong thông báo được ghi nhật ký có định dạng nhất quán như thể được ghi riêng, bạn có thể thực hiện việc này bằng một handler mixin, như trong đoạn mã sau:

.. code-block:: python

    # Giả sử đoạn mã này nằm trong module mymixins.py
    import copy

    class MultilineMixin:
        def emit(self, record):
            s = record.getMessage()
            if '\n' not in s:
                super().emit(record)
            else:
                lines = s.splitlines()
                rec = copy.copy(record)
                rec.args = None
                for line in lines:
                    rec.msg = line
                    super().emit(rec)

Bạn có thể sử dụng mixin như trong script sau:

.. code-block:: python

    import logging

    from mymixins import MultilineMixin

    logger = logging.getLogger(__name__)

    class StreamHandler(MultilineMixin, logging.StreamHandler):
        pass

    if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-9s %(message)s',
                            handlers = [StreamHandler()])
        logger.debug('Single line')
        logger.debug('Multiple lines:\nfool me once ...')
        logger.debug('Another single line')
        logger.debug('Multiple lines:\n%s', 'fool me ...\ncan\'t get fooled again')

Khi chạy, script sẽ in ra nội dung tương tự như sau:

.. code-block:: text

    2025-07-02 13:54:47,234 DEBUG     Single line
    2025-07-02 13:54:47,234 DEBUG     Multiple lines:
    2025-07-02 13:54:47,234 DEBUG     fool me once ...
    2025-07-02 13:54:47,234 DEBUG     Another single line
    2025-07-02 13:54:47,234 DEBUG     Multiple lines:
    2025-07-02 13:54:47,234 DEBUG     fool me ...
    2025-07-02 13:54:47,234 DEBUG     can't get fooled again

Mặt khác, nếu bạn lo ngại về `log injection <https://owasp.org/www-community/attacks/Log_Injection>`_, bạn có thể sử dụng formatter để escape các dòng mới, như trong ví dụ sau:

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    class EscapingFormatter(logging.Formatter):
        def format(self, record):
            s = super().format(record)
            return s.replace('\n', r'\n')

    if __name__ == '__main__':
        h = logging.StreamHandler()
        h.setFormatter(EscapingFormatter('%(asctime)s %(levelname)-9s %(message)s'))
        logging.basicConfig(level=logging.DEBUG, handlers = [h])
        logger.debug('Single line')
        logger.debug('Multiple lines:\nfool me once ...')
        logger.debug('Another single line')
        logger.debug('Multiple lines:\n%s', 'fool me ...\ncan\'t get fooled again')

Tất nhiên, bạn có thể sử dụng bất kỳ scheme escape nào phù hợp nhất với mình. Khi chạy, script sẽ tạo ra đầu ra tương tự như sau:

.. code-block:: text

    2025-07-09 06:47:33,783 DEBUG     Single line
    2025-07-09 06:47:33,783 DEBUG     Multiple lines:\nfool me once ...
    2025-07-09 06:47:33,783 DEBUG     Another single line
    2025-07-09 06:47:33,783 DEBUG     Multiple lines:\nfool me ...\ncan't get fooled again

Hành vi escape không thể là mặc định của stdlib, vì điều đó sẽ phá vỡ khả năng tương thích ngược.

.. patterns-to-avoid:

Các mẫu cần tránh
-----------------

Mặc dù các phần trước đã mô tả những cách thực hiện hoặc xử lý một số việc mà bạn có thể cần, vẫn cần đề cập đến một số mẫu sử dụng *không hữu ích* và do đó nên tránh trong hầu hết các trường hợp. Các phần sau không được sắp xếp theo thứ tự cụ thể nào.

Mở cùng một tệp log nhiều lần
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trên Windows, nhìn chung bạn sẽ không thể mở cùng một tệp nhiều lần vì điều này sẽ dẫn đến lỗi "file is in use by another process". Tuy nhiên, trên các nền tảng POSIX, bạn sẽ không gặp lỗi nếu mở cùng một tệp nhiều lần. Điều này có thể vô tình xảy ra, chẳng hạn như do:

* Thêm một file handler nhiều hơn một lần nhưng cùng tham chiếu đến một tệp (ví dụ: do lỗi sao chép/dán/quên thay đổi).

* Mở hai tệp trông có vẻ khác nhau vì có tên khác nhau, nhưng thực chất là cùng một tệp do một tệp là symbolic link trỏ đến tệp kia.

* Fork một process, sau đó cả process cha và process con đều có tham chiếu đến cùng một tệp. Ví dụ, điều này có thể xảy ra khi sử dụng module :mod:`multiprocessing`.

Việc mở một tệp nhiều lần có thể *trông như* hoạt động bình thường trong hầu hết thời gian, nhưng trên thực tế có thể dẫn đến một số vấn đề:

* Đầu ra logging có thể bị lộn xộn vì nhiều thread hoặc process cố gắng ghi vào cùng một tệp. Mặc dù logging ngăn việc nhiều thread sử dụng đồng thời cùng một handler instance, không có cơ chế bảo vệ tương tự nếu hai thread khác nhau thực hiện ghi đồng thời bằng hai handler instance khác nhau nhưng tình cờ trỏ đến cùng một tệp.

* Nỗ lực xóa một tệp (ví dụ: trong quá trình xoay vòng tệp) âm thầm thất bại vì có một tham chiếu khác đang trỏ đến tệp đó. Điều này có thể gây nhầm lẫn và làm lãng phí thời gian debug - các mục log kết thúc ở những vị trí không mong muốn hoặc bị mất hoàn toàn. Hoặc một tệp lẽ ra phải được di chuyển vẫn nằm nguyên vị trí và tăng kích thước ngoài dự kiến, dù việc xoay vòng dựa trên kích thước được cho là đang được áp dụng.

Sử dụng các kỹ thuật được trình bày trong :ref:`multiple-processes` để khắc phục những vấn đề như vậy.

Sử dụng logger làm thuộc tính trong một class hoặc truyền logger dưới dạng tham số
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mặc dù có thể có những trường hợp đặc biệt mà bạn cần làm như vậy, nhưng nhìn chung điều này không có ý nghĩa vì logger là singleton. Code luôn có thể truy cập một instance logger cụ thể theo tên bằng cách sử dụng ``logging.getLogger(name)``, vì vậy việc truyền các instance xung quanh và lưu giữ chúng làm thuộc tính của instance là vô nghĩa. Lưu ý rằng trong các ngôn ngữ khác như Java và C#, logger thường là thuộc tính static của class. Tuy nhiên, mẫu này không phù hợp trong Python, nơi module (chứ không phải class) là đơn vị phân rã phần mềm.

Thêm các handler khác ngoài :class:`~logging.NullHandler` vào logger trong một thư viện
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Việc cấu hình logging bằng cách thêm handler, formatter và filter là trách nhiệm của nhà phát triển ứng dụng, không phải nhà phát triển thư viện. Nếu bạn đang duy trì một thư viện, hãy đảm bảo rằng bạn không thêm handler vào bất kỳ logger nào ngoài một instance :class:`~logging.NullHandler`.

Tạo quá nhiều logger
^^^^^^^^^^^^^^^^^^^^

Logger là các singleton không bao giờ được giải phóng trong suốt quá trình thực thi một script, vì vậy việc tạo quá nhiều logger sẽ sử dụng bộ nhớ mà sau đó không thể được giải phóng. Thay vì tạo một logger cho mỗi, chẳng hạn, tệp được xử lý hoặc kết nối mạng được thiết lập, hãy sử dụng :ref:`existing mechanisms <context-info>` để truyền thông tin ngữ cảnh vào log của bạn và giới hạn các logger được tạo ở những logger mô tả các khu vực trong ứng dụng của bạn (thường là các module, nhưng đôi khi có phạm vi chi tiết hơn một chút).

.. _cookbook-ref-links:

Tài nguyên khác
---------------

.. seealso::

   Mô-đun :mod:`logging`
      Tài liệu tham khảo API cho mô-đun logging.

   Mô-đun :mod:`logging.config`
      API cấu hình cho mô-đun logging.

   Mô-đun :mod:`logging.handlers`
      Các handler hữu ích đi kèm mô-đun logging.

   :ref:`Hướng dẫn cơ bản <logging-basic-tutorial>`

   :ref:`Hướng dẫn nâng cao <logging-advanced-tutorial>`

.. _`Supervisor`: http://supervisord.org/
.. _`Gunicorn`: https://gunicorn.org/
.. _`uWSGI`: https://uwsgi-docs.readthedocs.io/en/latest/
.. _`NNG`: https://nng.nanomsg.org/
.. _`documentation on the Django project`: https://docs.djangoproject.com/en/stable/topics/logging/#configuring-logging
.. _`relevant section`: https://docs.djangoproject.com/en/stable/topics/logging/#configuring-logging
.. _`Qt`: https://www.qt.io/
.. _`log injection`: https://owasp.org/www-community/attacks/Log_Injection
