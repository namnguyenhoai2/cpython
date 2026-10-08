:mod:`!logging` --- Cơ chế ghi nhật ký cho Python
=================================================

.. module:: logging
   :synopsis: Hệ thống ghi nhật ký sự kiện linh hoạt cho các ứng dụng.

.. moduleauthor:: Vinay Sajip <vinay_sajip@red-dove.com>
.. sectionauthor:: Vinay Sajip <vinay_sajip@red-dove.com>

**Mã nguồn:** :source:`Lib/logging/__init__.py`

.. index:: pair: Errors; logging

.. sidebar:: Quan trọng

   Trang này chứa thông tin tham chiếu API. Để xem hướng dẫn và thảo luận về các chủ đề nâng cao hơn, hãy xem

   * :ref:`Hướng dẫn cơ bản <logging-basic-tutorial>`
   * :ref:`Hướng dẫn nâng cao <logging-advanced-tutorial>`
   * :ref:`Cẩm nang Logging <logging-cookbook>`

--------------

Mô-đun này định nghĩa các hàm và lớp triển khai một hệ thống ghi nhật ký sự kiện linh hoạt cho các ứng dụng và thư viện.

Lợi ích chính của việc cung cấp API logging thông qua một mô-đun trong thư viện chuẩn là tất cả các mô-đun Python đều có thể tham gia logging, nhờ đó log của ứng dụng có thể bao gồm các thông báo của riêng bạn được tích hợp với thông báo từ các mô-đun bên thứ ba.

Sau đây là một ví dụ đơn giản về cách sử dụng đúng quy chuẩn:::

   # myapp.py
   import logging
   import mylib
   logger = logging.getLogger(__name__)

   def main():
       logging.basicConfig(filename='myapp.log', level=logging.INFO)
       logger.info('Started')
       mylib.do_something()
       logger.info('Finished')

   if __name__ == '__main__':
       main()

::

   # mylib.py
   import logging
   logger = logging.getLogger(__name__)

   def do_something():
       logger.info('Doing something')

Nếu chạy *myapp.py*, bạn sẽ thấy nội dung sau trong *myapp.log*:

.. code-block:: none

   INFO:__main__:Started
   INFO:mylib:Doing something
   INFO:__main__:Finished

Tính năng chính của cách sử dụng đúng theo phong cách này là phần lớn mã chỉ đơn giản là tạo một logger cấp mô-đun bằng ``getLogger(__name__)``, rồi sử dụng logger đó để thực hiện mọi hoạt động ghi nhật ký cần thiết. Cách này ngắn gọn, đồng thời vẫn cho phép mã ở phía sau kiểm soát chi tiết khi cần. Các thông báo được ghi vào logger cấp mô-đun sẽ được chuyển tiếp đến các handler của những logger trong các mô-đun cấp cao hơn, cho đến logger cấp cao nhất được gọi là root logger; cách tiếp cận này được gọi là ghi nhật ký phân cấp.

Để việc ghi nhật ký hữu ích, cần cấu hình nó: thiết lập cấp độ và đích đến cho từng logger, có thể thay đổi cách các mô-đun cụ thể ghi nhật ký, thường dựa trên các đối số dòng lệnh hoặc cấu hình ứng dụng. Trong hầu hết trường hợp, như ví dụ trên, chỉ cần cấu hình root logger theo cách này, vì tất cả logger cấp thấp hơn ở cấp mô-đun cuối cùng đều chuyển tiếp thông báo của chúng đến các handler của root logger. :func:`~logging.basicConfig` cung cấp một cách nhanh chóng để cấu hình root logger, đáp ứng nhiều trường hợp sử dụng.

Mô-đun này cung cấp rất nhiều chức năng và tính linh hoạt. Nếu bạn chưa quen với việc ghi nhật ký, cách tốt nhất để làm quen với nó là xem các hướng dẫn (**xem các liên kết ở trên và bên phải**).

Các lớp cơ bản được định nghĩa bởi mô-đun, cùng với các thuộc tính và phương thức của chúng, được liệt kê trong các phần bên dưới.

* Logger cung cấp giao diện mà mã ứng dụng sử dụng trực tiếp.
* Handler gửi các bản ghi nhật ký (do logger tạo) đến đích thích hợp.
* Filter cung cấp cơ chế chi tiết hơn để xác định bản ghi nhật ký nào sẽ được xuất.
* Formatter chỉ định bố cục của các bản ghi log trong đầu ra cuối cùng.


.. _logger:

Đối tượng Logger
----------------

Các đối tượng Logger có những thuộc tính và phương thức sau. Lưu ý rằng các Logger *KHÔNG BAO GIỜ* được khởi tạo trực tiếp mà luôn phải thông qua hàm cấp mô-đun ``logging.getLogger(name)``. Nhiều lần gọi :func:`getLogger` với cùng một tên sẽ luôn trả về tham chiếu đến cùng một đối tượng Logger.

``name`` có thể là một giá trị phân cấp, được ngăn cách bằng dấu chấm, chẳng hạn như ``foo.bar.baz`` (mặc dù cũng có thể chỉ là ``foo`` đơn thuần, chẳng hạn). Các logger nằm thấp hơn trong danh sách phân cấp là các logger con của những logger nằm cao hơn trong danh sách. Ví dụ, với một logger có tên ``foo``, các logger có tên ``foo.bar``, ``foo.bar.baz`` và ``foo.bam`` đều là hậu duệ của ``foo``. Ngoài ra, mọi logger đều là hậu duệ của root logger. Hệ thống phân cấp tên logger tương tự như hệ thống phân cấp package Python, và sẽ giống hệt nếu bạn tổ chức logger theo từng module bằng cách sử dụng cách khởi tạo được khuyến nghị ``logging.getLogger(__name__)``. Đó là vì trong một module, ``__name__`` là tên của module trong không gian tên package Python.


.. class:: Logger

   .. attribute:: Logger.name

      Đây là tên của logger và là giá trị được truyền cho :func:`getLogger` để lấy logger.

      .. note:: Nên coi thuộc tính này là chỉ đọc.

   .. attribute:: Logger.level

      Ngưỡng của logger này, được thiết lập bằng phương thức :meth:`setLevel`.

      .. note:: Không đặt trực tiếp thuộc tính này - luôn sử dụng :meth:`setLevel`, vì hàm này có các bước kiểm tra đối với cấp độ được truyền vào.

   .. attribute:: Logger.parent

      Logger cha của logger này. Logger này có thể thay đổi dựa trên việc khởi tạo sau đó các logger nằm cao hơn trong hệ thống phân cấp namespace.

      .. note:: Giá trị này nên được coi là chỉ đọc.

   .. attribute:: Logger.propagate

      Nếu thuộc tính này được đánh giá là true, các sự kiện được ghi vào logger này sẽ được chuyển đến các handler của những logger cấp cao hơn (logger tổ tiên), ngoài mọi handler được gắn với logger này. Thông báo được chuyển trực tiếp đến các handler của logger tổ tiên - cả cấp độ lẫn bộ lọc của các logger tổ tiên liên quan đều không được xem xét.

      Nếu giá trị này được đánh giá là false, các thông báo logging sẽ không được chuyển đến các handler của logger tổ tiên.

      Hãy diễn giải bằng một ví dụ: Nếu thuộc tính propagate của logger có tên ``A.B.C`` được đánh giá là true, mọi sự kiện được ghi vào ``A.B.C`` thông qua một lời gọi phương thức như ``logging.getLogger('A.B.C').error(...)`` sẽ [với điều kiện vượt qua các thiết lập cấp độ và bộ lọc của logger đó] lần lượt được chuyển đến mọi handler được gắn với các logger có tên ``A.B``, ``A`` và logger root, sau khi trước đó được chuyển đến mọi handler được gắn với ``A.B.C``. Nếu bất kỳ logger nào trong chuỗi ``A.B.C``, ``A.B``, ``A`` có thuộc tính ``propagate`` được đặt thành false, thì đó là logger cuối cùng mà các handler của nó được cung cấp sự kiện để xử lý, và quá trình lan truyền sẽ dừng tại đó.

      Hàm khởi tạo đặt thuộc tính này thành ``True``.

      .. note:: Nếu bạn gắn một handler vào một logger *and* hoặc nhiều logger tổ tiên của nó, logger đó có thể phát cùng một bản ghi nhiều lần. Nhìn chung, bạn không cần gắn handler vào nhiều hơn một logger - nếu chỉ gắn nó vào logger phù hợp ở vị trí cao nhất trong hệ thống phân cấp logger, thì nó sẽ nhận được tất cả các sự kiện được ghi bởi mọi logger hậu duệ, với điều kiện cài đặt propagate của chúng vẫn được đặt thành ``True``. Một trường hợp phổ biến là chỉ gắn các handler vào root logger và để cơ chế propagation xử lý phần còn lại.

   .. attribute:: Logger.handlers

      Danh sách các handler được gắn trực tiếp vào instance logger này.

      .. note:: Thuộc tính này nên được xem là chỉ-đọc; thông thường, thuộc tính được thay đổi thông qua các phương thức :meth:`addHandler` và :meth:`removeHandler`, vốn sử dụng các khóa để đảm bảo thao tác an toàn trong môi trường đa luồng.

   .. attribute:: Logger.disabled

      Thuộc tính này vô hiệu hóa việc xử lý mọi sự kiện. Thuộc tính được đặt thành ``False`` trong hàm khởi tạo và chỉ được thay đổi bởi mã cấu hình logging.

      .. note:: Nên coi thuộc tính này là chỉ đọc.

   .. method:: Logger.setLevel(level)

      Đặt ngưỡng cho logger này thành *level*. Các thông báo logging có mức độ nghiêm trọng thấp hơn *level* sẽ bị bỏ qua; các thông báo logging có mức độ nghiêm trọng *level* trở lên sẽ được phát bởi handler hoặc các handler phục vụ logger này, trừ khi mức của một handler được đặt thành mức độ nghiêm trọng cao hơn *level*.

      Khi một logger được tạo, level được đặt thành :const:`NOTSET` (khiến mọi thông báo được xử lý nếu logger đó là root logger, hoặc được ủy quyền cho logger cha nếu logger đó không phải root logger). Lưu ý rằng root logger được tạo với level :const:`WARNING`.

      Thuật ngữ 'ủy quyền cho cấp cha' có nghĩa là nếu một logger có mức là NOTSET, chuỗi các logger tổ tiên của nó sẽ được duyệt cho đến khi tìm thấy một logger tổ tiên có mức khác NOTSET hoặc đạt đến root.

      Nếu tìm thấy một logger tổ tiên có mức khác NOTSET, thì mức của logger tổ tiên đó được coi là mức hiệu lực của logger nơi bắt đầu quá trình tìm kiếm logger tổ tiên, và được dùng để xác định cách một sự kiện logging được xử lý.

      Nếu đạt đến root và root có mức NOTSET, thì tất cả thông báo sẽ được xử lý. Nếu không, mức của root sẽ được dùng làm mức hiệu lực.

      Xem :ref:`levels` để biết danh sách các mức.

      .. versionchanged:: 3.2
         Tham số *level* hiện chấp nhận biểu diễn dạng chuỗi của mức, chẳng hạn như 'INFO', thay cho các hằng số dạng số nguyên như :const:`INFO`. Tuy nhiên, lưu ý rằng các mức được lưu trữ nội bộ dưới dạng số nguyên, và các phương thức như :meth:`getEffectiveLevel` và
         :meth:`isEnabledFor` sẽ trả về hoặc yêu cầu được truyền vào các số nguyên.


   .. method:: Logger.isEnabledFor(level)

      Cho biết liệu một thông báo có mức độ nghiêm trọng *level* có được logger này xử lý hay không. Phương thức này trước tiên kiểm tra mức cấp module được đặt bởi ``logging.disable(level)``, sau đó kiểm tra mức hiệu lực của logger được xác định bởi :meth:`getEffectiveLevel`.


   .. method:: Logger.getEffectiveLevel()

      Cho biết level (mức) hiệu lực của logger này. Nếu một giá trị khác với
      :const:`NOTSET` đã được đặt bằng :meth:`setLevel`, thì giá trị đó được trả về. Nếu không, hệ thống duyệt qua hệ phân cấp theo hướng về root cho đến khi tìm thấy một giá trị khác với
      :const:`NOTSET`, rồi trả về giá trị đó. Giá trị được trả về là một số nguyên, thường là một trong các giá trị :const:`logging.DEBUG`, :const:`logging.INFO` v.v.


   .. method:: Logger.getChild(suffix)

      Trả về một logger là hậu duệ của logger này, được xác định theo hậu tố. Vì vậy, ``logging.getLogger('abc').getChild('def.ghi')`` sẽ trả về cùng logger với logger được trả về bởi ``logging.getLogger('abc.def.ghi')``. Đây là một phương thức tiện ích, hữu ích khi logger cha được đặt tên bằng, chẳng hạn, ``__name__`` thay vì một chuỗi ký tự cố định.

      .. versionadded:: 3.2


   .. method:: Logger.getChildren()

      Trả về một tập hợp các logger là con trực tiếp của logger này. Ví dụ, ``logging.getLogger().getChildren()`` có thể trả về một tập hợp chứa các logger có tên ``foo`` và ``bar``, nhưng logger có tên ``foo.bar`` sẽ không được đưa vào tập hợp. Tương tự, ``logging.getLogger('foo').getChildren()`` có thể trả về một tập hợp bao gồm logger có tên ``foo.bar``, nhưng sẽ không bao gồm logger có tên ``foo.bar.baz``.

      .. versionadded:: 3.12


   .. method:: Logger.debug(msg, *args, **kwargs)

      Ghi một thông báo với level :const:`DEBUG` trên logger này. *msg* là chuỗi định dạng thông báo, còn *args* là các đối số được hợp nhất vào *msg* bằng toán tử định dạng chuỗi. (Lưu ý rằng điều này có nghĩa là bạn có thể sử dụng các keyword trong chuỗi định dạng cùng với một đối số kiểu dictionary duy nhất.) Không thực hiện thao tác định dạng % trên *msg* khi không cung cấp *args*.

      Có bốn keyword argument trong *kwargs* được kiểm tra: *exc_info*, *stack_info*, *stacklevel* và *extra*.

      Nếu *exc_info* không cho kết quả là false, thông tin ngoại lệ sẽ được thêm vào thông báo ghi nhật ký. Nếu cung cấp một tuple ngoại lệ (theo định dạng được trả về bởi
      :func:`sys.exc_info`) hoặc một instance ngoại lệ, nó sẽ được sử dụng; nếu không, :func:`sys.exc_info` sẽ được gọi để lấy thông tin ngoại lệ.

      Đối số từ khóa tùy chọn thứ hai là *stack_info*, mặc định là ``False``. Nếu là true, thông tin stack sẽ được thêm vào thông báo ghi nhật ký, bao gồm cả lệnh gọi ghi nhật ký thực tế. Lưu ý rằng đây không phải là thông tin stack giống với thông tin được hiển thị khi chỉ định *exc_info*: thông tin trước là các stack frame từ đáy stack lên đến lệnh gọi ghi nhật ký trong thread hiện tại, còn thông tin sau là thông tin về các stack frame đã được unwind sau một ngoại lệ trong khi tìm kiếm các trình xử lý ngoại lệ.

      Bạn có thể chỉ định *stack_info* độc lập với *exc_info*, chẳng hạn như để chỉ hiển thị cách bạn đã đi đến một điểm nhất định trong mã, ngay cả khi không có ngoại lệ nào được phát sinh. Các stack frame được in sau một dòng tiêu đề có nội dung:

      .. code-block:: none

          Stack (most recent call last):

      Điều này mô phỏng ``Traceback (most recent call last):``, được sử dụng khi hiển thị các frame của ngoại lệ.

      Đối số từ khóa tùy chọn thứ ba là *stacklevel*, mặc định là ``1``. Nếu lớn hơn 1, số lượng stack frame tương ứng sẽ được bỏ qua khi tính số dòng và tên hàm được thiết lập trong :class:`LogRecord` được tạo cho sự kiện ghi nhật ký. Bạn có thể sử dụng đối số này trong các helper ghi nhật ký để tên hàm, tên tệp và số dòng được ghi lại không phải là thông tin của hàm/phương thức helper mà là của bên gọi nó. Tên của tham số này tương tự với tên tương đương trong module :mod:`warnings`.

      Đối số từ khóa thứ tư là *extra*, có thể được sử dụng để truyền một dictionary dùng để điền vào :attr:`~object.__dict__` của
      :class:`LogRecord` được tạo cho sự kiện ghi nhật ký với các thuộc tính do người dùng định nghĩa. Sau đó, bạn có thể sử dụng các thuộc tính tùy chỉnh này theo ý muốn. Chẳng hạn, bạn có thể đưa chúng vào các thông điệp được ghi nhật ký. Ví dụ::

         FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
         logging.basicConfig(format=FORMAT)
         d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
         logger = logging.getLogger('tcpserver')
         logger.warning('Protocol problem: %s', 'connection reset', extra=d)

      sẽ in ra nội dung tương tự như sau

      .. code-block:: none

         2006-02-08 22:20:02,165 192.168.0.1 fbloggs  Protocol problem: connection reset

      Các khóa trong từ điển được truyền vào *extra* không được trùng với các khóa mà hệ thống ghi nhật ký sử dụng. (Xem phần về :ref:`logrecord-attributes` để biết thêm thông tin về các khóa được hệ thống ghi nhật ký sử dụng.)

      Nếu chọn sử dụng các thuộc tính này trong các thông điệp được ghi nhật ký, bạn cần thận trọng. Chẳng hạn, trong ví dụ trên, :class:`Formatter` đã được cấu hình với một chuỗi định dạng yêu cầu 'clientip' và 'user' trong từ điển thuộc tính của :class:`LogRecord`. Nếu thiếu các thuộc tính này, thông điệp sẽ không được ghi vì sẽ xảy ra ngoại lệ định dạng chuỗi. Do đó, trong trường hợp này, bạn luôn cần truyền từ điển *extra* với các khóa này.

      Mặc dù điều này có thể gây khó chịu, tính năng này được thiết kế để sử dụng trong các trường hợp chuyên biệt, chẳng hạn như các máy chủ đa luồng, nơi cùng một đoạn mã thực thi trong nhiều ngữ cảnh và các điều kiện đáng chú ý phát sinh phụ thuộc vào ngữ cảnh đó (chẳng hạn như địa chỉ IP của máy khách từ xa và tên người dùng đã xác thực trong ví dụ trên). Trong những trường hợp như vậy, có khả năng các
      :class:`Formatter`\ s sẽ được sử dụng với các :class:`Handler`\ s cụ thể.

      Nếu không có handler nào được gắn với logger này (hoặc bất kỳ logger cha nào của nó, có tính đến các thuộc tính :attr:`Logger.propagate` liên quan), thông điệp sẽ được gửi đến handler được đặt trên :data:`lastResort`.

      .. versionchanged:: 3.2
         Tham số *stack_info* đã được thêm vào.

      .. versionchanged:: 3.5
         Tham số *exc_info* hiện có thể nhận các instance của exception.

      .. versionchanged:: 3.8
         Tham số *stacklevel* đã được thêm vào.


   .. method:: Logger.info(msg, *args, **kwargs)

      Ghi một thông báo với cấp độ :const:`INFO` trên logger này. Các đối số được diễn giải như đối với :meth:`debug`.


   .. method:: Logger.warning(msg, *args, **kwargs)

      Ghi một thông báo với cấp độ :const:`WARNING` trên logger này. Các đối số được diễn giải như đối với :meth:`debug`.

      .. note:: Có một phương thức lỗi thời ``warn`` có chức năng giống hệt ``warning``. Vì ``warn`` không còn được khuyến nghị sử dụng, vui lòng không dùng nó - hãy sử dụng ``warning`` thay thế.

   .. method:: Logger.error(msg, *args, **kwargs)

      Ghi một thông báo với cấp độ :const:`ERROR` trên logger này. Các đối số được diễn giải như đối với :meth:`debug`.


   .. method:: Logger.critical(msg, *args, **kwargs)

      Ghi một thông báo với mức :const:`CRITICAL` trên logger này. Các đối số được diễn giải như đối với :meth:`debug`.


   .. method:: Logger.log(level, msg, *args, **kwargs)

      Ghi một thông báo với mức nguyên *level* trên logger này. Các đối số khác được diễn giải như đối với :meth:`debug`.


   .. method:: Logger.exception(msg, *args, **kwargs)

      Ghi một thông báo với mức :const:`ERROR` trên logger này. Các đối số được diễn giải như đối với :meth:`debug`. Thông tin ngoại lệ được thêm vào thông báo logging. Chỉ nên gọi phương thức này từ một exception handler.


   .. method:: Logger.addFilter(filter)

      Thêm filter được chỉ định *filter* vào logger này.


   .. method:: Logger.removeFilter(filter)

      Xóa filter được chỉ định *filter* khỏi logger này.


   .. method:: Logger.filter(record)

      Áp dụng các filter của logger này cho record và trả về ``True`` nếu record cần được xử lý. Các filter được kiểm tra lần lượt cho đến khi một trong số chúng trả về giá trị false. Nếu không filter nào trả về giá trị false, record sẽ được xử lý (chuyển đến các handler). Nếu một filter trả về giá trị false, sẽ không thực hiện thêm bước xử lý nào đối với record.


   .. method:: Logger.addHandler(hdlr)

      Thêm handler được chỉ định *hdlr* vào logger này.


   .. method:: Logger.removeHandler(hdlr)

      Xóa handler được chỉ định *hdlr* khỏi logger này.


   .. method:: Logger.findCaller(stack_info=False, stacklevel=1)

      Tìm tên tệp nguồn và số dòng của caller. Trả về tên tệp, số dòng, tên hàm và thông tin stack dưới dạng tuple gồm 4 phần tử. Thông tin stack được trả về dưới dạng ``None`` trừ khi *stack_info* là ``True``.

      Tham số *stacklevel* được truyền từ mã gọi :meth:`debug` và các API khác. Nếu lớn hơn 1, phần vượt quá được dùng để bỏ qua các stack frame trước khi xác định các giá trị cần trả về. Điều này thường hữu ích khi gọi các logging API từ mã helper/wrapper, để thông tin trong event log tham chiếu đến mã gọi nó thay vì mã helper/wrapper.


   .. method:: Logger.handle(record)

      Xử lý một record bằng cách truyền nó cho tất cả handler được liên kết với logger này và các logger cấp trên của nó (cho đến khi tìm thấy giá trị false của *propagate*). Phương thức này được dùng cho các record đã được unpickle nhận từ socket, cũng như các record được tạo cục bộ. Bộ lọc ở cấp logger được áp dụng bằng :meth:`~Logger.filter`.


   .. method:: Logger.makeRecord(name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None)

      Đây là một factory method có thể được ghi đè trong các subclass để tạo các :class:`LogRecord` chuyên biệt.

   .. method:: Logger.hasHandlers()

      Kiểm tra xem logger này có handler nào được cấu hình hay không. Việc này được thực hiện bằng cách tìm handler trong logger này và các logger cấp trên của nó trong hệ thống phân cấp logger. Trả về ``True`` nếu tìm thấy handler, nếu không thì trả về ``False``. Phương thức này dừng tìm kiếm lên cấp trên bất cứ khi nào tìm thấy một logger có thuộc tính 'propagate' được đặt thành false - đó sẽ là logger cuối cùng được kiểm tra để xác định sự tồn tại của handler.

      .. versionadded:: 3.2

   .. versionchanged:: 3.7
      Các logger hiện có thể được pickle và unpickle.

.. _levels:

Các cấp độ ghi nhật ký
----------------------

Các giá trị số của các cấp độ ghi nhật ký được nêu trong bảng sau. Những giá trị này chủ yếu hữu ích nếu bạn muốn định nghĩa các cấp độ riêng và cần chúng có các giá trị cụ thể tương quan với những cấp độ được định nghĩa sẵn. Nếu bạn định nghĩa một cấp độ có cùng giá trị số, cấp độ đó sẽ ghi đè giá trị được định nghĩa sẵn; tên được định nghĩa sẵn sẽ bị mất.

+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Cấp độ                | Giá trị số | Ý nghĩa / Khi sử dụng                                                                                                                                                        |
+=======================+============+==============================================================================================================================================================================+
| .. py:data:: NOTSET   | 0          | Khi được đặt trên một logger, cho biết rằng cần tham vấn các logger tổ tiên để xác định cấp độ hiệu lực. Nếu kết quả đó vẫn phân giải thành                                  |
|                       |            | :const:`!NOTSET`, thì tất cả sự kiện đều được ghi nhật ký. Khi được đặt trên một handler, tất cả sự kiện đều được xử lý.                                                     |
+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .. py:data:: DEBUG    | 10         | Thông tin chi tiết, thường chỉ hữu ích với nhà phát triển đang cố gắng chẩn đoán sự cố.                                                                                      |
+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .. py:data:: INFO     | 20         | Xác nhận rằng mọi thứ đang hoạt động như mong đợi.                                                                                                                           |
+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .. py:data:: WARNING  | 30         | Dấu hiệu cho thấy đã xảy ra điều gì đó bất ngờ hoặc một sự cố có thể xảy ra trong tương lai gần (ví dụ: 'sắp hết dung lượng đĩa'). Phần mềm vẫn đang hoạt động như mong đợi. |
+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .. py:data:: ERROR    | 40         | Do một sự cố nghiêm trọng hơn, phần mềm không thể thực hiện một số chức năng.                                                                                                |
+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .. py:data:: CRITICAL | 50         | Một lỗi nghiêm trọng, cho biết bản thân chương trình có thể không thể tiếp tục chạy.                                                                                         |
+-----------------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


.. _handler:

Đối tượng Handler
-----------------

Handler có các thuộc tính và phương thức sau. Lưu ý rằng :class:`Handler` không bao giờ được khởi tạo trực tiếp; lớp này đóng vai trò là lớp cơ sở cho các lớp con hữu ích hơn. Tuy nhiên, phương thức :meth:`!__init__` trong các lớp con cần gọi
:meth:`Handler.__init__`.

.. class:: Handler

   .. method:: Handler.__init__(level=NOTSET)

      Khởi tạo instance :class:`Handler` bằng cách đặt level cho instance, đặt danh sách bộ lọc thành danh sách rỗng và tạo một lock (sử dụng :meth:`createLock`) để tuần tự hóa quyền truy cập vào cơ chế I/O.


   .. method:: Handler.createLock()

      Khởi tạo một thread lock có thể được sử dụng để tuần tự hóa quyền truy cập vào chức năng I/O bên dưới, vốn có thể không threadsafe.


   .. method:: Handler.acquire()

      Nhận thread lock được tạo bằng :meth:`createLock`.


   .. method:: Handler.release()

      Giải phóng thread lock đã nhận bằng :meth:`acquire`.


   .. method:: Handler.setLevel(level)

      Đặt ngưỡng cho handler này thành *level*. Các thông báo logging ít nghiêm trọng hơn *level* sẽ bị bỏ qua. Khi một handler được tạo, level được đặt thành :const:`NOTSET` (khiến mọi thông báo được xử lý).

      Xem :ref:`levels` để biết danh sách các level.

      .. versionchanged:: 3.2
         Tham số *level* hiện chấp nhận biểu diễn dạng chuỗi của level, chẳng hạn như 'INFO', thay cho các hằng số số nguyên như :const:`INFO`.


   .. method:: Handler.setFormatter(fmt)

      Đặt formatter cho handler này thành *fmt*. Đối số *fmt* phải là một instance của :class:`Formatter` hoặc ``None``.


   .. method:: Handler.addFilter(filter)

      Thêm filter được chỉ định *filter* vào handler này.


   .. method:: Handler.removeFilter(filter)

      Xóa filter được chỉ định *filter* khỏi handler này.


   .. method:: Handler.filter(record)

      Áp dụng các filter của handler này cho record và trả về ``True`` nếu record cần được xử lý. Các filter được kiểm tra lần lượt cho đến khi một filter trả về giá trị false. Nếu không có filter nào trả về giá trị false, record sẽ được phát ra. Nếu một filter trả về giá trị false, handler sẽ không phát ra record.


   .. method:: Handler.flush()

      Đảm bảo mọi đầu ra logging đã được flush. Phiên bản này không thực hiện thao tác nào và được thiết kế để các lớp con triển khai.


   .. method:: Handler.close()

      Dọn dẹp mọi tài nguyên được handler sử dụng. Phiên bản này không tạo đầu ra, nhưng xóa handler khỏi một map nội bộ của các handler, được dùng để tra cứu handler theo tên.

      Các lớp con cần đảm bảo rằng phương thức :meth:`close` được gọi từ các phương thức bị ghi đè.


   .. method:: Handler.handle(record)

      Phát ra bản ghi logging được chỉ định tùy theo các bộ lọc có thể đã được thêm vào handler. Bao quanh việc phát ra bản ghi thực tế bằng thao tác lấy/nhả khóa luồng I/O.


   .. method:: Handler.handleError(record)

      Phương thức này nên được gọi từ các handler khi gặp ngoại lệ trong một lần gọi :meth:`emit`. Nếu thuộc tính cấp mô-đun
      :data:`raiseExceptions` là ``False``, các ngoại lệ sẽ bị bỏ qua một cách im lặng. Đây là điều thường được mong muốn đối với một hệ thống logging - hầu hết người dùng sẽ không quan tâm đến các lỗi trong hệ thống logging mà quan tâm hơn đến các lỗi của ứng dụng. Tuy nhiên, bạn có thể thay thế hành vi này bằng một handler tùy chỉnh nếu muốn. Bản ghi được chỉ định là bản ghi đang được xử lý khi ngoại lệ xảy ra. (Giá trị mặc định của :data:`raiseExceptions` là ``True``, vì giá trị đó hữu ích hơn trong quá trình phát triển).


   .. method:: Handler.format(record)

      Định dạng một bản ghi - nếu đã đặt formatter thì sử dụng formatter đó. Nếu không, sử dụng formatter mặc định của mô-đun.


   .. method:: Handler.emit(record)

      Thực hiện mọi việc cần thiết để thực sự ghi bản ghi logging được chỉ định. Phiên bản này được thiết kế để các lớp con triển khai, vì vậy sẽ phát sinh một
      :exc:`NotImplementedError`.

      .. warning:: Phương thức này được gọi sau khi khóa cấp handler được lấy, và khóa này sẽ được nhả sau khi phương thức trả về. Khi ghi đè phương thức này, hãy lưu ý rằng bạn cần thận trọng khi gọi bất kỳ thứ gì kích hoạt các phần khác của API logging có thể thực hiện thao tác khóa, vì điều đó có thể dẫn đến deadlock. Cụ thể:

         * Các API cấu hình logging lấy khóa cấp mô-đun, sau đó lấy các khóa cấp handler riêng lẻ khi các handler đó được cấu hình.

         * Nhiều logging API khóa khóa cấp mô-đun. Nếu một API như vậy được gọi từ phương thức này, nó có thể gây deadlock nếu một lời gọi cấu hình được thực hiện trên thread khác, vì thread đó sẽ cố gắng giành khóa cấp mô-đun *trước* khóa cấp handler, trong khi thread này cố gắng giành khóa cấp mô-đun *sau* khóa cấp handler (vì trong phương thức này, khóa cấp handler đã được giành trước).

Để xem danh sách các handler được cung cấp theo tiêu chuẩn, hãy xem :mod:`logging.handlers`.

.. _formatter-objects:

Đối tượng Formatter
-------------------

.. currentmodule:: logging

.. class:: Formatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)

   Chịu trách nhiệm chuyển đổi :class:`LogRecord` thành chuỗi đầu ra để con người hoặc hệ thống bên ngoài diễn giải.

   :param fmt: Một chuỗi định dạng theo *style* đã cho cho toàn bộ đầu ra được ghi nhật ký. Các khóa ánh xạ có thể có được lấy từ đối tượng :class:`LogRecord`
       :ref:`logrecord-attributes`. Nếu không được chỉ định, ``'%(message)s'`` sẽ được sử dụng, tức chỉ là thông báo được ghi nhật ký.
   :type fmt: str

   :param datefmt: Một chuỗi định dạng cho phần ngày/giờ của đầu ra được ghi nhật ký. Nếu không được chỉ định, mặc định được mô tả trong :meth:`formatTime` sẽ được sử dụng.
   :type datefmt: str

   :param style: Có thể là ``'%'``, ``'{'`` hoặc ``'$'`` và xác định cách chuỗi định dạng sẽ được kết hợp với dữ liệu tương ứng: bằng một trong các cách sau
       :ref:`old-string-formatting` (``%``), :meth:`str.format` (``{``) hoặc :class:`string.Template` (``$``). Điều này chỉ áp dụng cho *fmt* (ví dụ: ``'%(message)s'`` so với ``'{message}'``), không áp dụng cho các thông báo nhật ký thực tế được truyền vào những phương thức logging. Tuy nhiên, còn có :ref:`những cách khác <formatting-styles>` để sử dụng kiểu định dạng ``{``- và ``$``- cho các thông báo nhật ký.
   :type style: str

   :param validate: Nếu là ``True`` (mặc định), *fmt* và *style* không chính xác hoặc không khớp sẽ gây ra :exc:`ValueError`; ví dụ: ``logging.Formatter('%(asctime)s - %(message)s', style='{')``.
   :type validate: bool

   :param defaults: Một dictionary chứa các giá trị mặc định để sử dụng trong các trường tùy chỉnh. Ví dụ: ``logging.Formatter('%(ip)s %(message)s', defaults={"ip": None})``
   :type defaults: dict[str, Any]

   .. versionchanged:: 3.2
      Đã thêm tham số *style*.

   .. versionchanged:: 3.8
      Đã thêm tham số *validate*.

   .. versionchanged:: 3.10
      Đã thêm tham số *defaults*.


   .. method:: format(record)

      Dictionary thuộc tính của bản ghi được sử dụng làm toán hạng cho một thao tác định dạng chuỗi. Trả về chuỗi kết quả. Trước khi định dạng dictionary, một vài bước chuẩn bị sẽ được thực hiện. Thuộc tính *message* của bản ghi được tính bằng *msg* % *args*. Nếu chuỗi định dạng chứa ``'(asctime)'``, :meth:`formatTime` sẽ được gọi để định dạng thời gian của sự kiện. Nếu có thông tin ngoại lệ, thông tin đó sẽ được định dạng bằng :meth:`formatException` và nối vào thông báo. Lưu ý rằng thông tin ngoại lệ đã định dạng được lưu trong bộ nhớ đệm tại thuộc tính *exc_text*. Điều này hữu ích vì thông tin ngoại lệ có thể được pickle và gửi qua mạng, nhưng bạn cần cẩn thận nếu có nhiều hơn một lớp con :class:`Formatter` tùy chỉnh cách định dạng thông tin ngoại lệ. Trong trường hợp này, bạn sẽ phải xóa giá trị được lưu trong bộ nhớ đệm (bằng cách đặt thuộc tính *exc_text* thành ``None``) sau khi một formatter hoàn tất việc định dạng, để formatter tiếp theo xử lý sự kiện không sử dụng giá trị được lưu trong bộ nhớ đệm mà tính toán lại từ đầu.

      Nếu có thông tin stack, thông tin đó sẽ được nối vào sau thông tin ngoại lệ, sử dụng :meth:`formatStack` để chuyển đổi khi cần.


   .. method:: formatTime(record, datefmt=None)

      Phương thức này nên được gọi từ :meth:`format` bởi một formatter muốn sử dụng thời gian đã được định dạng. Có thể ghi đè phương thức này trong các formatter để đáp ứng mọi yêu cầu cụ thể, nhưng hành vi cơ bản như sau: nếu *datefmt* (một chuỗi) được chỉ định, nó sẽ được dùng cùng với
      :func:`time.strftime` để định dạng thời gian tạo bản ghi. Nếu không, định dạng '%Y-%m-%d %H:%M:%S,uuu' sẽ được sử dụng, trong đó phần uuu là giá trị mili giây và các chữ cái còn lại tuân theo
      :func:`time.strftime` documentation.  An example time in this format is ``2003-01-23 00:29:50,411``.  The resulting string is returned.

      Hàm này sử dụng một hàm do người dùng cấu hình để chuyển đổi thời gian tạo thành một tuple. Theo mặc định, :func:`time.localtime` được sử dụng; để thay đổi hàm này cho một formatter instance cụ thể, hãy đặt thuộc tính ``converter`` thành một hàm có cùng signature với :func:`time.localtime` hoặc
      :func:`time.gmtime`. Để thay đổi cho tất cả formatter, chẳng hạn nếu bạn muốn tất cả thời gian ghi log được hiển thị theo GMT, hãy đặt thuộc tính ``converter`` trong class ``Formatter``.

      .. versionchanged:: 3.3
         Trước đây, định dạng mặc định được hard-code như trong ví dụ này: ``2010-09-06 22:38:15,292``, trong đó phần trước dấu phẩy được xử lý bởi chuỗi định dạng strptime (``'%Y-%m-%d %H:%M:%S'``), còn phần sau dấu phẩy là một giá trị mili giây. Vì strptime không có placeholder định dạng cho mili giây, giá trị mili giây được nối thêm bằng một chuỗi định dạng khác, ``'%s,%03d'`` --- và cả hai chuỗi định dạng này đều được hard-code trong phương thức này. Sau thay đổi này, các chuỗi được định nghĩa dưới dạng thuộc tính cấp class và có thể được ghi đè ở cấp instance khi cần. Tên của các thuộc tính là ``default_time_format`` (dành cho chuỗi định dạng strptime) và ``default_msec_format`` (dành cho việc nối thêm giá trị mili giây).

      .. versionchanged:: 3.9
         ``default_msec_format`` có thể là ``None``.

   .. method:: formatException(exc_info)

      Định dạng thông tin ngoại lệ được chỉ định (một tuple ngoại lệ tiêu chuẩn do :func:`sys.exc_info` trả về) thành một chuỗi. Cách triển khai mặc định này chỉ sử dụng :func:`traceback.print_exception`. Chuỗi kết quả được trả về.

   .. method:: formatStack(stack_info)

      Định dạng thông tin stack được chỉ định (một chuỗi do
      :func:`traceback.print_stack`, nhưng đã loại bỏ ký tự dòng mới cuối cùng) thành một chuỗi. Cách triển khai mặc định này chỉ trả về giá trị đầu vào.

.. class:: BufferingFormatter(linefmt=None)

   Một lớp formatter cơ sở phù hợp để phân lớp con khi bạn muốn định dạng nhiều bản ghi. Bạn có thể truyền một thực thể :class:`Formatter` mà bạn muốn dùng để định dạng từng dòng (tương ứng với một bản ghi). Nếu không chỉ định, formatter mặc định (chỉ xuất thông báo sự kiện) sẽ được dùng làm formatter dòng.

   .. method:: formatHeader(records)

      Trả về phần đầu cho một danh sách *các bản ghi*. Cách triển khai cơ sở chỉ trả về chuỗi rỗng. Bạn cần ghi đè phương thức này nếu muốn có hành vi cụ thể, chẳng hạn như hiển thị số lượng bản ghi, tiêu đề hoặc một dòng phân cách.

   .. method:: formatFooter(records)

      Trả về phần cuối cho một danh sách *các bản ghi*. Cách triển khai cơ sở chỉ trả về chuỗi rỗng. Bạn cần ghi đè phương thức này nếu muốn có hành vi cụ thể, chẳng hạn như hiển thị số lượng bản ghi hoặc một dòng phân cách.

   .. method:: format(records)

      Trả về văn bản đã định dạng cho một danh sách *các bản ghi*. Cách triển khai cơ sở chỉ trả về chuỗi rỗng nếu không có bản ghi; nếu không, nó trả về phép nối của phần đầu, từng bản ghi được định dạng bằng formatter dòng và phần cuối.

.. _filter:

Đối tượng bộ lọc
----------------

``Filters`` có thể được ``Handlers`` và ``Loggers`` sử dụng để thực hiện việc lọc phức tạp hơn so với khả năng lọc theo cấp độ. Lớp bộ lọc cơ sở chỉ cho phép các sự kiện nằm dưới một vị trí nhất định trong hệ thống phân cấp logger. Ví dụ: một bộ lọc được khởi tạo với 'A.B' sẽ cho phép các sự kiện được ghi bởi các logger 'A.B', 'A.B.C', 'A.B.C.D', 'A.B.D', v.v., nhưng không cho phép 'A.BB', 'B.A.B', v.v. Nếu được khởi tạo bằng chuỗi rỗng, mọi sự kiện đều được truyền qua.


.. class:: Filter(name='')

   Trả về một instance của lớp :class:`Filter`. Nếu *name* được chỉ định, nó sẽ xác định một logger mà logger đó cùng các logger con của nó sẽ được phép truyền sự kiện qua bộ lọc. Nếu *name* là chuỗi rỗng, mọi sự kiện đều được cho phép.


   .. method:: filter(record)

      Bản ghi được chỉ định có cần được ghi lại không? Trả về false nếu không, true nếu có. Bộ lọc có thể sửa đổi các bản ghi log trực tiếp hoặc trả về một instance bản ghi hoàn toàn khác để thay thế bản ghi log ban đầu trong mọi bước xử lý tiếp theo của sự kiện.

Lưu ý rằng các bộ lọc được gắn vào handler được kiểm tra trước khi sự kiện được handler phát ra, trong khi các bộ lọc được gắn vào logger được kiểm tra mỗi khi một sự kiện được ghi lại (bằng :meth:`debug`, :meth:`info`, v.v.), trước khi gửi sự kiện đến các handler. Điều này có nghĩa là các sự kiện được tạo bởi các logger hậu duệ sẽ không bị lọc theo thiết lập bộ lọc của logger, trừ khi bộ lọc cũng được áp dụng cho các logger hậu duệ đó.

Bạn thực sự không cần phân lớp ``Filter``: bạn có thể truyền vào bất kỳ instance nào có phương thức ``filter`` với cùng ngữ nghĩa.

.. versionchanged:: 3.2
   Bạn không cần tạo các lớp ``Filter`` chuyên biệt hoặc sử dụng các lớp khác có phương thức ``filter``: bạn có thể sử dụng một hàm (hoặc callable khác) làm bộ lọc. Logic lọc sẽ kiểm tra xem đối tượng bộ lọc có thuộc tính ``filter`` hay không: nếu có, đối tượng đó được coi là một ``Filter`` và phương thức :meth:`~Filter.filter` của nó sẽ được gọi. Nếu không, đối tượng đó được coi là một callable và được gọi với bản ghi làm tham số duy nhất. Giá trị được trả về phải phù hợp với giá trị được trả về bởi
   :meth:`~Filter.filter`.

.. versionchanged:: 3.12
   Giờ đây, bạn có thể trả về một thể hiện :class:`LogRecord` từ các filter để thay thế bản ghi log thay vì sửa đổi bản ghi tại chỗ. Điều này cho phép các filter được gắn vào một :class:`Handler` sửa đổi bản ghi log trước khi bản ghi được phát ra, mà không gây ra tác động phụ lên các handler khác.

Mặc dù filter chủ yếu được dùng để lọc các bản ghi dựa trên những tiêu chí phức tạp hơn level, chúng vẫn xem được mọi bản ghi được handler hoặc logger mà chúng được gắn vào xử lý: điều này có thể hữu ích nếu bạn muốn thực hiện những việc như đếm số bản ghi được một logger hoặc handler cụ thể xử lý, hoặc thêm, thay đổi hay xóa các thuộc tính trong :class:`LogRecord` đang được xử lý. Rõ ràng, việc thay đổi LogRecord cần được thực hiện cẩn thận, nhưng điều đó cho phép đưa thông tin ngữ cảnh vào log (xem :ref:`filters-contextual`).


.. _log-record:

Đối tượng LogRecord
-------------------

Các thể hiện :class:`LogRecord` được :class:`Logger` tự động tạo ra mỗi khi có nội dung được log, và có thể được tạo thủ công thông qua
:func:`makeLogRecord` (ví dụ: từ một event đã được pickle nhận qua mạng).


.. class:: LogRecord(name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None)

   Chứa mọi thông tin liên quan đến event đang được log.

   Thông tin chính được truyền trong *msg* và *args*, sau đó được kết hợp bằng ``msg % args`` để tạo thuộc tính :attr:`!message` của bản ghi.

   :param name: Tên của logger được dùng để ghi lại sự kiện được biểu diễn bởi :class:`!LogRecord`. Lưu ý rằng tên logger trong :class:`!LogRecord` sẽ luôn có giá trị này, ngay cả khi sự kiện có thể được phát ra bởi một handler được gắn với một logger (tổ tiên) khác.
   :type name: str

   :param level: :ref:`mức số <levels>` của sự kiện ghi log (chẳng hạn như ``10`` cho ``DEBUG``, ``20`` cho ``INFO``, v.v.). Lưu ý rằng giá trị này được chuyển đổi thành *hai* thuộc tính của LogRecord:
      :attr:`!levelno` cho giá trị số và :attr:`!levelname` cho tên mức tương ứng.
   :type level: int

   :param pathname: Đường dẫn chuỗi đầy đủ của tệp nguồn nơi thực hiện lệnh gọi ghi log.
   :type pathname: str

   :param lineno: Số dòng trong tệp nguồn nơi lệnh gọi ghi nhật ký được thực hiện.
   :type lineno: int

   :param msg: Thông báo mô tả sự kiện, có thể là chuỗi định dạng %-format với các placeholder cho dữ liệu biến đổi hoặc một đối tượng tùy ý (xem :ref:`arbitrary-object-messages`).
   :type msg: typing.Any

   :param args: Dữ liệu biến đổi được hợp nhất vào đối số *msg* để nhận mô tả sự kiện.
   :type args: tuple | dict[str, typing.Any]

   :param exc_info: Một tuple ngoại lệ chứa thông tin về ngoại lệ hiện tại, do :func:`sys.exc_info` trả về hoặc là ``None`` nếu không có thông tin ngoại lệ.
   :type exc_info: tuple[type[BaseException], BaseException, types.TracebackType] | None

   :param func: Tên của hàm hoặc phương thức nơi lời gọi ghi nhật ký được thực hiện.
   :type func: str | None

   :param sinfo: Một chuỗi văn bản biểu thị thông tin ngăn xếp từ đáy ngăn xếp trong luồng hiện tại đến lời gọi ghi nhật ký.
   :type sinfo: str | None

   .. method:: getMessage()

      Trả về thông báo cho thực thể :class:`LogRecord` này sau khi hợp nhất mọi đối số do người dùng cung cấp với thông báo. Nếu đối số thông báo do người dùng cung cấp cho lời gọi ghi nhật ký không phải là chuỗi, :func:`str` sẽ được gọi trên đối số đó để chuyển đổi thành chuỗi. Điều này cho phép sử dụng các lớp do người dùng định nghĩa làm thông báo, trong đó phương thức ``__str__`` có thể trả về chuỗi định dạng thực tế cần sử dụng.

   .. versionchanged:: 3.2
      Việc tạo một :class:`LogRecord` đã trở nên linh hoạt hơn bằng cách cung cấp một factory được dùng để tạo record. Có thể thiết lập factory bằng :func:`getLogRecordFactory` và :func:`setLogRecordFactory` (xem tại đây chữ ký của factory).

   Chức năng này có thể được sử dụng để đưa các giá trị của riêng bạn vào một
   :class:`LogRecord` tại thời điểm tạo. Bạn có thể sử dụng mẫu sau::

      old_factory = logging.getLogRecordFactory()

      def record_factory(*args, **kwargs):
          record = old_factory(*args, **kwargs)
          record.custom_attribute = 0xdecafbad
          return record

      logging.setLogRecordFactory(record_factory)

   Với mẫu này, có thể nối chuỗi nhiều factory, và miễn là chúng không ghi đè lên các thuộc tính của nhau hoặc vô tình ghi đè lên các thuộc tính tiêu chuẩn được liệt kê ở trên thì sẽ không có điều gì bất ngờ xảy ra.


.. _logrecord-attributes:

Các thuộc tính LogRecord
------------------------

LogRecord có một số thuộc tính, phần lớn trong số đó được lấy từ các tham số của hàm khởi tạo. (Lưu ý rằng tên không phải lúc nào cũng tương ứng chính xác giữa các tham số của hàm khởi tạo LogRecord và các thuộc tính LogRecord.) Bạn có thể sử dụng các thuộc tính này để hợp nhất dữ liệu từ record vào chuỗi định dạng. Bảng sau liệt kê (theo thứ tự bảng chữ cái) tên thuộc tính, ý nghĩa của chúng và placeholder tương ứng trong chuỗi định dạng kiểu %.

Nếu bạn đang sử dụng định dạng {} (:func:`str.format`), bạn có thể dùng ``{attrname}`` làm placeholder trong chuỗi định dạng. Nếu bạn đang sử dụng định dạng $ (:class:`string.Template`), hãy dùng dạng ``${attrname}``. Trong cả hai trường hợp, tất nhiên, hãy thay ``attrname`` bằng tên thuộc tính thực tế mà bạn muốn sử dụng.

Trong trường hợp định dạng {}, bạn có thể chỉ định các cờ định dạng bằng cách đặt chúng sau tên thuộc tính và phân tách với tên bằng dấu hai chấm. Ví dụ: placeholder ``{msecs:03.0f}`` sẽ định dạng giá trị mili giây ``4`` thành ``004``. Hãy tham khảo tài liệu :meth:`str.format` để biết đầy đủ chi tiết về các tùy chọn bạn có thể sử dụng.

+----------------+-------------------------+-----------------------------------------------+
| Attribute name | Format                  | Description                                   |
+================+=========================+===============================================+
| args           | You shouldn't need to   | The tuple of arguments merged into ``msg`` to |
|                | format this yourself.   | produce ``message``, or a dict whose values   |
|                |                         | are used for the merge (when there is only one|
|                |                         | argument, and it is a dictionary).            |
+----------------+-------------------------+-----------------------------------------------+
| asctime        | ``%(asctime)s``         | Human-readable time when the                  |
|                |                         | :class:`LogRecord` was created.  By default   |
|                |                         | this is of the form '2003-07-08 16:49:45,896' |
|                |                         | (the numbers after the comma are millisecond  |
|                |                         | portion of the time).                         |
+----------------+-------------------------+-----------------------------------------------+
| created        | ``%(created)f``         | Time when the :class:`LogRecord` was created  |
|                |                         | (as returned by :func:`time.time_ns` / 1e9).  |
+----------------+-------------------------+-----------------------------------------------+
| exc_info       | You shouldn't need to   | Exception tuple (à la ``sys.exc_info``) or,   |
|                | format this yourself.   | if no exception has occurred, ``None``.       |
+----------------+-------------------------+-----------------------------------------------+
| exc_text       | You shouldn't need to   | Exception information formatted as a string.  |
|                | format this yourself.   | This is set when :meth:`Formatter.format` is  |
|                |                         | invoked, or ``None`` if no exception has      |
|                |                         | occurred.                                     |
+----------------+-------------------------+-----------------------------------------------+
| filename       | ``%(filename)s``        | Filename portion of ``pathname``.             |
+----------------+-------------------------+-----------------------------------------------+
| funcName       | ``%(funcName)s``        | Name of function containing the logging call. |
+----------------+-------------------------+-----------------------------------------------+
| levelname      | ``%(levelname)s``       | Text logging level for the message            |
|                |                         | (``'DEBUG'``, ``'INFO'``, ``'WARNING'``,      |
|                |                         | ``'ERROR'``, ``'CRITICAL'``).                 |
+----------------+-------------------------+-----------------------------------------------+
| levelno        | ``%(levelno)s``         | Numeric logging level for the message         |
|                |                         | (:const:`DEBUG`, :const:`INFO`,               |
|                |                         | :const:`WARNING`, :const:`ERROR`,             |
|                |                         | :const:`CRITICAL`).                           |
+----------------+-------------------------+-----------------------------------------------+
| lineno         | ``%(lineno)d``          | Source line number where the logging call was |
|                |                         | issued (if available).                        |
+----------------+-------------------------+-----------------------------------------------+
| message        | ``%(message)s``         | The logged message, computed as ``msg %       |
|                |                         | args``. This is set when                      |
|                |                         | :meth:`Formatter.format` is invoked.          |
+----------------+-------------------------+-----------------------------------------------+
| module         | ``%(module)s``          | Module (name portion of ``filename``).        |
+----------------+-------------------------+-----------------------------------------------+
| msecs          | ``%(msecs)d``           | Millisecond portion of the time when the      |
|                |                         | :class:`LogRecord` was created.               |
+----------------+-------------------------+-----------------------------------------------+
| msg            | You shouldn't need to   | The format string passed in the original      |
|                | format this yourself.   | logging call. Merged with ``args`` to         |
|                |                         | produce ``message``, or an arbitrary object   |
|                |                         | (see :ref:`arbitrary-object-messages`).       |
+----------------+-------------------------+-----------------------------------------------+
| name           | ``%(name)s``            | Name of the logger used to log the call.      |
+----------------+-------------------------+-----------------------------------------------+
| pathname       | ``%(pathname)s``        | Full pathname of the source file where the    |
|                |                         | logging call was issued (if available).       |
+----------------+-------------------------+-----------------------------------------------+
| process        | ``%(process)d``         | Process ID (if available).                    |
+----------------+-------------------------+-----------------------------------------------+
| processName    | ``%(processName)s``     | Process name (if available).                  |
+----------------+-------------------------+-----------------------------------------------+
| relativeCreated| ``%(relativeCreated)d`` | Time in milliseconds when the LogRecord was   |
|                |                         | created, relative to the time the logging     |
|                |                         | module was loaded.                            |
+----------------+-------------------------+-----------------------------------------------+
| stack_info     | You shouldn't need to   | Stack frame information (where available)     |
|                | format this yourself.   | from the bottom of the stack in the current   |
|                |                         | thread, up to and including the stack frame   |
|                |                         | of the logging call which resulted in the     |
|                |                         | creation of this record.                      |
+----------------+-------------------------+-----------------------------------------------+
| thread         | ``%(thread)d``          | Thread ID (if available).                     |
+----------------+-------------------------+-----------------------------------------------+
| threadName     | ``%(threadName)s``      | Thread name (if available).                   |
+----------------+-------------------------+-----------------------------------------------+
| taskName       | ``%(taskName)s``        | :class:`asyncio.Task` name (if available).    |
+----------------+-------------------------+-----------------------------------------------+

.. versionchanged:: 3.1
   *processName* đã được thêm.

.. versionchanged:: 3.12
   *taskName* đã được thêm.

.. _logger-adapter:

Các đối tượng LoggerAdapter
---------------------------

Các instance :class:`LoggerAdapter` được dùng để truyền thông tin ngữ cảnh vào các lệnh gọi logging một cách thuận tiện. Để xem ví dụ sử dụng, hãy xem phần
:ref:`thêm thông tin ngữ cảnh vào đầu ra logging của bạn <context-info>`.

.. class:: LoggerAdapter(logger, extra=None, merge_extra=False)

   Trả về một instance của :class:`LoggerAdapter`, được khởi tạo với một instance :class:`Logger` bên dưới, một đối tượng dạng dict tùy chọn (*extra*), và một boolean tùy chọn (*merge_extra*) cho biết có hợp nhất đối số *extra* của các lệnh gọi log riêng lẻ với :class:`LoggerAdapter` extra hay không. Theo mặc định, đối số *extra* của các lệnh gọi log riêng lẻ sẽ bị bỏ qua và chỉ sử dụng đối số của instance :class:`LoggerAdapter`

   .. method:: process(msg, kwargs)

      Sửa đổi message và/hoặc các đối số keyword được truyền vào một lệnh gọi logging để chèn thông tin ngữ cảnh. Cách triển khai này lấy đối tượng được truyền dưới dạng *extra* cho hàm khởi tạo và thêm đối tượng đó vào *kwargs* bằng khóa 'extra'. Giá trị trả về là một tuple (*msg*, *kwargs*) chứa các phiên bản (có thể đã được sửa đổi) của các đối số được truyền vào.

   .. attribute:: manager

      Ủy quyền cho :attr:`!manager` bên dưới trên *logger*.

   .. attribute:: _log

      Ủy quyền cho phương thức :meth:`!_log` bên dưới trên *logger*.

   Ngoài những nội dung trên, :class:`LoggerAdapter` hỗ trợ các phương thức sau của :class:`Logger`: :meth:`~Logger.debug`, :meth:`~Logger.info`,
   :meth:`~Logger.warning`, :meth:`~Logger.error`, :meth:`~Logger.exception`,
   :meth:`~Logger.critical`, :meth:`~Logger.log`, :meth:`~Logger.isEnabledFor`,
   :meth:`~Logger.getEffectiveLevel`, :meth:`~Logger.setLevel` và
   :meth:`~Logger.hasHandlers`. Các phương thức này có cùng chữ ký với những phương thức tương ứng trong :class:`Logger`, vì vậy bạn có thể sử dụng thay thế lẫn nhau hai loại instance này.

   .. versionchanged:: 3.2

      Các phương thức :meth:`~Logger.isEnabledFor`, :meth:`~Logger.getEffectiveLevel`,
      :meth:`~Logger.setLevel` và :meth:`~Logger.hasHandlers` đã được thêm vào :class:`LoggerAdapter`. Các phương thức này ủy quyền cho logger bên dưới.

   .. versionchanged:: 3.6

      Thuộc tính :attr:`!manager` và phương thức :meth:`!_log` đã được thêm vào; chúng ủy quyền cho logger bên dưới và cho phép lồng các adapter.

   .. versionchanged:: 3.10

      Đối số *extra* hiện là tùy chọn.

   .. versionchanged:: 3.13

      Tham số *merge_extra* đã được thêm vào.


An toàn luồng
-------------

Mô-đun logging được thiết kế để an toàn luồng mà không yêu cầu client thực hiện bất kỳ thao tác đặc biệt nào. Mô-đun này đạt được điều đó bằng cách sử dụng các khóa threading; có một khóa để tuần tự hóa quyền truy cập vào dữ liệu dùng chung của mô-đun, và mỗi handler cũng tạo một khóa để tuần tự hóa quyền truy cập vào I/O bên dưới.

Nếu bạn triển khai các trình xử lý tín hiệu bất đồng bộ bằng mô-đun :mod:`signal`, bạn có thể không sử dụng được logging bên trong các trình xử lý đó. Nguyên nhân là các cơ chế triển khai khóa trong mô-đun :mod:`threading` không phải lúc nào cũng có thể tái nhập, vì vậy không thể được gọi từ các trình xử lý tín hiệu như vậy.


Các hàm cấp mô-đun
------------------

Ngoài các class được mô tả ở trên, còn có một số hàm cấp module.


.. function:: getLogger(name=None)

   Trả về một logger có tên được chỉ định hoặc, nếu name là ``None``, trả về logger gốc của hệ thống phân cấp. Nếu được chỉ định, name thường là một tên phân cấp được phân tách bằng dấu chấm, chẳng hạn như *'a'*, *'a.b'* hoặc *'a.b.c.d'*. Việc chọn các tên này hoàn toàn phụ thuộc vào developer sử dụng logging, mặc dù bạn nên sử dụng ``__name__`` trừ khi có lý do cụ thể để không làm vậy, như đã đề cập trong :ref:`logger`.

   Mọi lần gọi hàm này với cùng một tên đều trả về cùng một instance logger. Điều này có nghĩa là không cần truyền các instance logger giữa những phần khác nhau của ứng dụng.


.. function:: getLoggerClass()

   Trả về class :class:`Logger` tiêu chuẩn hoặc class cuối cùng được truyền cho
   :func:`setLoggerClass`. Có thể gọi hàm này bên trong định nghĩa một class mới để đảm bảo rằng việc cài đặt một class :class:`Logger` tùy chỉnh không hoàn tác các tùy chỉnh đã được mã khác áp dụng. Ví dụ::

      class MyLogger(logging.getLoggerClass()):
          # ... ghi đè hành vi tại đây


.. function:: getLogRecordFactory()

   Trả về một callable được dùng để tạo :class:`LogRecord`.

   .. versionadded:: 3.2
      Hàm này được cung cấp cùng với :func:`setLogRecordFactory` để cho phép các developer kiểm soát tốt hơn cách xây dựng :class:`LogRecord` đại diện cho một sự kiện ghi log.

   Xem :func:`setLogRecordFactory` để biết thêm thông tin về cách factory được gọi.

.. function:: debug(msg, *args, **kwargs)

   Đây là một hàm tiện ích gọi :meth:`Logger.debug` trên root logger. Cách xử lý các đối số hoàn toàn giống với mô tả trong phương thức đó.

   Điểm khác biệt duy nhất là nếu root logger không có handler nào thì
   :func:`basicConfig` được gọi trước khi gọi ``debug`` trên root logger.

   Đối với các script rất ngắn hoặc phần minh họa nhanh về các tiện ích của ``logging``, ``debug`` và các hàm cấp module khác có thể rất tiện lợi. Tuy nhiên, hầu hết chương trình sẽ muốn kiểm soát cấu hình logging một cách cẩn thận và tường minh, vì vậy nên ưu tiên tạo một logger cấp module và gọi :meth:`Logger.debug` (hoặc các phương thức dành riêng cho cấp độ khác) trên logger đó, như được mô tả ở phần đầu tài liệu này.


.. function:: info(msg, *args, **kwargs)

   Ghi một thông báo với cấp độ :const:`INFO` trên root logger. Các đối số và hành vi về những mặt khác giống như :func:`debug`.


.. function:: warning(msg, *args, **kwargs)

   Ghi nhật ký một thông báo với cấp độ :const:`WARNING` trên root logger. Các đối số và hành vi về cơ bản giống với :func:`debug`.

   .. note:: Có một hàm lỗi thời ``warn`` có chức năng giống hệt ``warning``. Vì ``warn`` đã không còn được dùng, vui lòng không sử dụng nó - thay vào đó hãy dùng ``warning``.


.. function:: error(msg, *args, **kwargs)

   Ghi nhật ký một thông báo với cấp độ :const:`ERROR` trên root logger. Các đối số và hành vi về cơ bản giống với :func:`debug`.


.. function:: critical(msg, *args, **kwargs)

   Ghi nhật ký một thông báo với cấp độ :const:`CRITICAL` trên root logger. Các đối số và hành vi về cơ bản giống với :func:`debug`.


.. function:: exception(msg, *args, **kwargs)

   Ghi nhật ký một thông báo với cấp độ :const:`ERROR` trên root logger. Các đối số và hành vi về cơ bản giống với :func:`debug`. Thông tin về ngoại lệ được thêm vào thông báo nhật ký. Chỉ nên gọi hàm này từ trình xử lý ngoại lệ.

.. function:: log(level, msg, *args, **kwargs)

   Ghi nhật ký một thông báo với cấp độ *level* trên root logger. Các đối số và hành vi về cơ bản giống với :func:`debug`.

.. function:: disable(level=CRITICAL)

   Cung cấp cấp độ ghi đè *level* cho tất cả logger, cấp độ này được ưu tiên hơn cấp độ riêng của logger. Khi cần tạm thời giảm lượng đầu ra nhật ký trên toàn bộ ứng dụng, hàm này có thể hữu ích. Tác dụng của nó là vô hiệu hóa tất cả các lệnh gọi ghi nhật ký có mức độ nghiêm trọng *level* trở xuống, vì vậy nếu gọi hàm này với giá trị INFO thì tất cả sự kiện INFO và DEBUG sẽ bị loại bỏ, trong khi các sự kiện có mức độ nghiêm trọng WARNING trở lên sẽ được xử lý theo cấp độ hiệu lực của logger. Nếu gọi ``logging.disable(logging.NOTSET)``, thao tác này thực tế sẽ xóa cấp độ ghi đè, để đầu ra nhật ký một lần nữa phụ thuộc vào các cấp độ hiệu lực của từng logger.

   Lưu ý rằng nếu bạn đã định nghĩa bất kỳ cấp độ logging tùy chỉnh nào cao hơn ``CRITICAL`` (điều này không được khuyến nghị), bạn sẽ không thể dựa vào giá trị mặc định của tham số *level*, mà sẽ phải cung cấp rõ ràng một giá trị phù hợp.

   .. versionchanged:: 3.7
      Tham số *level* được mặc định ở cấp độ ``CRITICAL``. Xem
      :issue:`28524` để biết thêm thông tin về thay đổi này.

.. function:: addLevelName(level, levelName)

   Liên kết cấp độ *level* với văn bản *levelName* trong một từ điển nội bộ, được dùng để ánh xạ các cấp độ dạng số sang dạng biểu diễn văn bản, chẳng hạn khi một
   :class:`Formatter` định dạng một thông báo. Hàm này cũng có thể được dùng để định nghĩa các cấp độ của riêng bạn. Điều kiện duy nhất là mọi cấp độ được sử dụng phải được đăng ký bằng hàm này, các cấp độ phải là số nguyên dương và phải tăng theo thứ tự mức độ nghiêm trọng tăng dần.

   .. note:: Nếu bạn đang cân nhắc định nghĩa các cấp độ của riêng mình, hãy xem phần về :ref:`custom-levels`.

.. function:: getLevelNamesMapping()

   Trả về một ánh xạ từ tên cấp độ đến các cấp độ logging tương ứng. Ví dụ, chuỗi "CRITICAL" ánh xạ đến :const:`CRITICAL`. Ánh xạ được trả về là bản sao của một ánh xạ nội bộ trong mỗi lần gọi hàm này.

   .. versionadded:: 3.11

.. function:: getLevelName(level)

   Trả về biểu diễn dạng văn bản hoặc dạng số của mức độ ghi nhật ký *level*.

   Nếu *level* là một trong các mức được định nghĩa sẵn :const:`CRITICAL`, :const:`ERROR`,
   :const:`WARNING`, :const:`INFO` hoặc :const:`DEBUG` thì bạn nhận được chuỗi tương ứng. Nếu bạn đã liên kết các mức với tên bằng cách sử dụng
   :func:`addLevelName` thì tên bạn đã liên kết với *level* sẽ được trả về. Nếu truyền vào một giá trị số tương ứng với một trong các mức đã định nghĩa, biểu diễn chuỗi tương ứng sẽ được trả về.

   Tham số *level* cũng chấp nhận biểu diễn dạng chuỗi của mức, chẳng hạn như 'INFO'. Trong những trường hợp đó, hàm này trả về giá trị số tương ứng của mức.

   Nếu không truyền vào giá trị số hoặc chuỗi nào khớp, chuỗi 'Level %s' % level sẽ được trả về.

   .. note:: Các mức nội bộ là số nguyên (vì chúng cần được so sánh trong logic ghi nhật ký). Hàm này được dùng để chuyển đổi giữa mức dạng số nguyên và tên mức được hiển thị trong đầu ra nhật ký đã định dạng thông qua bộ chỉ định định dạng ``%(levelname)s`` (xem :ref:`logrecord-attributes`), và ngược lại.

   .. versionchanged:: 3.4
      Trong các phiên bản Python trước 3.4, hàm này cũng có thể nhận một cấp độ dạng văn bản và trả về giá trị số tương ứng của cấp độ đó. Hành vi không được ghi lại này được xem là một sai sót và đã bị loại bỏ trong Python 3.4, nhưng được khôi phục trong 3.4.2 để duy trì khả năng tương thích ngược.

.. function:: getHandlerByName(name)

   Trả về một handler có *name* được chỉ định, hoặc ``None`` nếu không có handler nào có tên đó.

   .. versionadded:: 3.12

.. function:: getHandlerNames()

   Trả về một tập hợp bất biến gồm tất cả tên handler đã biết.

   .. versionadded:: 3.12

.. function:: makeLogRecord(attrdict)

   Tạo và trả về một instance :class:`LogRecord` mới với các thuộc tính được xác định bởi *attrdict*. Hàm này hữu ích để lấy một
   :class:`LogRecord` dictionary thuộc tính, gửi qua socket, rồi tái tạo nó thành một instance :class:`LogRecord` ở đầu nhận.


.. function:: basicConfig(**kwargs)

   Thực hiện cấu hình cơ bản cho hệ thống logging bằng cách tạo một
   :class:`StreamHandler` với một :class:`Formatter` mặc định và thêm nó vào root logger. Các hàm :func:`debug`, :func:`info`, :func:`warning`,
   :func:`error` và :func:`critical` sẽ tự động gọi :func:`basicConfig` nếu không có handler nào được định nghĩa cho root logger.

   Hàm này không thực hiện thao tác nào nếu root logger đã được cấu hình handler, trừ khi đối số từ khóa *force* được đặt thành ``True``.

   .. note:: Hàm này nên được gọi từ main thread trước khi khởi động các thread khác. Trong các phiên bản Python trước 2.7.1 và 3.2, nếu hàm này được gọi từ nhiều thread, trong một số trường hợp hiếm gặp, một handler có thể được thêm vào root logger nhiều hơn một lần, dẫn đến các kết quả không mong muốn, chẳng hạn như thông báo bị lặp lại trong log.

   Các đối số từ khóa sau được hỗ trợ.

   .. tabularcolumns:: |l|L|

   +--------------+---------------------------------------------+
   | Format       | Description                                 |
   +==============+=============================================+
   | *filename*   | Specifies that a :class:`FileHandler` be    |
   |              | created, using the specified filename,      |
   |              | rather than a :class:`StreamHandler`.       |
   +--------------+---------------------------------------------+
   | *filemode*   | If *filename* is specified, open the file   |
   |              | in this :ref:`mode <filemodes>`. Defaults   |
   |              | to ``'a'``.                                 |
   +--------------+---------------------------------------------+
   | *format*     | Use the specified format string for the     |
   |              | handler. Defaults to attributes             |
   |              | ``levelname``, ``name`` and ``message``     |
   |              | separated by colons.                        |
   +--------------+---------------------------------------------+
   | *datefmt*    | Use the specified date/time format, as      |
   |              | accepted by :func:`time.strftime`.          |
   +--------------+---------------------------------------------+
   | *style*      | If *format* is specified, use this style    |
   |              | for the format string. One of ``'%'``,      |
   |              | ``'{'`` or ``'$'`` for :ref:`printf-style   |
   |              | <old-string-formatting>`,                   |
   |              | :meth:`str.format` or                       |
   |              | :class:`string.Template` respectively.      |
   |              | Defaults to ``'%'``.                        |
   +--------------+---------------------------------------------+
   | *level*      | Set the root logger level to the specified  |
   |              | :ref:`level <levels>`.                      |
   +--------------+---------------------------------------------+
   | *stream*     | Use the specified stream to initialize the  |
   |              | :class:`StreamHandler`. Note that this      |
   |              | argument is incompatible with *filename* -  |
   |              | if both are present, a ``ValueError`` is    |
   |              | raised.                                     |
   +--------------+---------------------------------------------+
   | *handlers*   | If specified, this should be an iterable of |
   |              | already created handlers to add to the root |
   |              | logger. Any handlers which don't already    |
   |              | have a formatter set will be assigned the   |
   |              | default formatter created in this function. |
   |              | Note that this argument is incompatible     |
   |              | with *filename* or *stream* - if both       |
   |              | are present, a ``ValueError`` is raised.    |
   +--------------+---------------------------------------------+
   | *force*      | If this keyword argument is specified as    |
   |              | true, any existing handlers attached to the |
   |              | root logger are removed and closed, before  |
   |              | carrying out the configuration as specified |
   |              | by the other arguments.                     |
   +--------------+---------------------------------------------+
   | *encoding*   | If this keyword argument is specified along |
   |              | with *filename*, its value is used when the |
   |              | :class:`FileHandler` is created, and thus   |
   |              | used when opening the output file.          |
   +--------------+---------------------------------------------+
   | *errors*     | If this keyword argument is specified along |
   |              | with *filename*, its value is used when the |
   |              | :class:`FileHandler` is created, and thus   |
   |              | used when opening the output file. If not   |
   |              | specified, the value 'backslashreplace' is  |
   |              | used. Note that if ``None`` is specified,   |
   |              | it will be passed as such to :func:`open`,  |
   |              | which means that it will be treated the     |
   |              | same as passing 'errors'.                   |
   +--------------+---------------------------------------------+

   .. versionchanged:: 3.2
      Đối số *style* đã được bổ sung.

   .. versionchanged:: 3.3
      Đối số *handlers* đã được bổ sung. Các bước kiểm tra bổ sung cũng được thêm vào để phát hiện những trường hợp chỉ định các đối số không tương thích (ví dụ: *handlers* cùng với *stream* hoặc *filename*, hoặc *stream* cùng với *filename*).

   .. versionchanged:: 3.8
      Đối số *force* đã được bổ sung.

   .. versionchanged:: 3.9
      Các đối số *encoding* và *errors* đã được thêm vào.

.. function:: shutdown()

   Thông báo cho hệ thống logging thực hiện việc tắt theo đúng thứ tự bằng cách flush và đóng tất cả handler. Hàm này nên được gọi khi ứng dụng thoát và không nên tiếp tục sử dụng hệ thống logging sau lần gọi này.

   Khi module logging được import, module này đăng ký hàm này làm exit handler (xem :mod:`atexit`), vì vậy thông thường bạn không cần thực hiện việc đó theo cách thủ công.


.. function:: setLoggerClass(klass)

   Cho hệ thống logging biết sử dụng lớp *klass* khi khởi tạo logger. Lớp này phải định nghĩa :meth:`!__init__` sao cho chỉ cần một đối số name, và :meth:`!__init__` phải gọi :meth:`!Logger.__init__`. Các ứng dụng cần hành vi logger tùy chỉnh thường gọi hàm này trước khi khởi tạo bất kỳ logger nào. Sau lần gọi này, cũng như ở mọi thời điểm khác, không khởi tạo logger trực tiếp bằng subclass; hãy tiếp tục sử dụng API :func:`logging.getLogger` để lấy logger.


.. function:: setLogRecordFactory(factory)

   Đặt một callable được sử dụng để tạo :class:`LogRecord`.

   :param factory: Callable factory được sử dụng để khởi tạo một log record.

   .. versionadded:: 3.2
      Hàm này được cung cấp cùng với :func:`getLogRecordFactory` để cho phép các developer kiểm soát nhiều hơn cách :class:`LogRecord` đại diện cho một sự kiện logging được tạo ra.

   Factory có chữ ký sau:

   ``factory(name, level, fn, lno, msg, args, exc_info, func=None, sinfo=None, **kwargs)``

      :name: Tên logger.
      :level: Mức logging (dạng số).
      :fn: Đường dẫn đầy đủ của tệp nơi lệnh gọi logging được thực hiện.
      :lno: Số dòng trong tệp nơi lệnh gọi logging được thực hiện.
      :msg: Thông báo logging.
      :args: Các đối số của thông báo logging.
      :exc_info: Một exception tuple, hoặc ``None``.
      :func: Tên của function hoặc method đã gọi logging call.
      :sinfo: Một stack traceback như được cung cấp bởi
              :func:`traceback.print_stack`, hiển thị hệ thống phân cấp lệnh gọi.
      :kwargs: Các đối số từ khóa bổ sung.


Các thuộc tính cấp module
-------------------------

.. data:: lastResort

   Một "handler of last resort" được cung cấp thông qua thuộc tính này. Đây là một :class:`StreamHandler` ghi vào ``sys.stderr`` với level là ``WARNING``, và được dùng để xử lý các sự kiện logging khi không có cấu hình logging nào. Kết quả cuối cùng chỉ đơn giản là in thông báo vào ``sys.stderr``. Điều này thay thế thông báo lỗi trước đây cho biết rằng "no handlers could be found for logger XYZ". Nếu vì lý do nào đó bạn cần hành vi trước đây, ``lastResort`` có thể được đặt thành ``None``.

   .. versionadded:: 3.2

.. data:: raiseExceptions

   Dùng để xác định liệu các ngoại lệ phát sinh trong quá trình xử lý có nên được truyền tiếp hay không.

   Mặc định: ``True``.

   Nếu :data:`raiseExceptions` là ``False``, các ngoại lệ sẽ bị bỏ qua một cách im lặng. Đây thường là điều mong muốn đối với một hệ thống logging - hầu hết người dùng sẽ không quan tâm đến các lỗi trong hệ thống logging mà quan tâm nhiều hơn đến các lỗi của ứng dụng.


Tích hợp với mô-đun warnings
----------------------------

Hàm :func:`captureWarnings` có thể được dùng để tích hợp :mod:`!logging` với mô-đun :mod:`warnings`.

.. function:: captureWarnings(capture)

   Hàm này được dùng để bật và tắt việc ghi log các cảnh báo.

   Nếu *capture* là ``True``, các cảnh báo do mô-đun :mod:`warnings` phát hành sẽ được chuyển hướng đến hệ thống logging. Cụ thể, một cảnh báo sẽ được định dạng bằng :func:`warnings.formatwarning` và chuỗi kết quả sẽ được ghi vào một logger có tên ``'py.warnings'`` với mức độ nghiêm trọng :const:`WARNING`.

   Nếu *capture* là ``False``, việc chuyển hướng cảnh báo đến hệ thống ghi nhật ký sẽ dừng lại và các cảnh báo sẽ được chuyển hướng đến đích ban đầu của chúng (tức là những đích đang có hiệu lực trước khi gọi ``captureWarnings(True)``).


.. seealso::

   Mô-đun :mod:`logging.config`
      API cấu hình cho mô-đun ghi nhật ký.

   Mô-đun :mod:`logging.handlers`
      Các handler hữu ích đi kèm với mô-đun ghi nhật ký.

   :pep:`282` - Một hệ thống ghi nhật ký
      Đề xuất mô tả tính năng này để đưa vào thư viện chuẩn Python.

   `Gói logging Python nguyên bản <https://old.red-dove.com/python_logging.html>`_
      Đây là mã nguồn ban đầu của gói :mod:`!logging`. Phiên bản của gói có trên trang này phù hợp để sử dụng với Python 1.5.2, 2.1.x và 2.2.x, những phiên bản không bao gồm gói :mod:`!logging` trong thư viện chuẩn.

.. _`Original Python logging package`: https://old.red-dove.com/python_logging.html
