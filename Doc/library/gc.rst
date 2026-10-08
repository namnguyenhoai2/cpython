:mod:`!gc` --- Giao diện Garbage Collector
==========================================

.. module:: gc
   :synopsis: Giao diện cho garbage collector phát hiện chu kỳ.

.. moduleauthor:: Neil Schemenauer <nas@arctrix.com>
.. sectionauthor:: Neil Schemenauer <nas@arctrix.com>

--------------

Mô-đun này cung cấp giao diện cho garbage collector tùy chọn. Mô-đun cho phép vô hiệu hóa collector, điều chỉnh tần suất thu gom và thiết lập các tùy chọn gỡ lỗi. Mô-đun cũng cung cấp quyền truy cập vào các đối tượng không thể truy cập mà collector đã tìm thấy nhưng không thể giải phóng. Vì collector bổ sung cho cơ chế đếm tham chiếu vốn đã được sử dụng trong Python, bạn có thể vô hiệu hóa collector nếu chắc chắn chương trình của mình không tạo ra các chu kỳ tham chiếu. Có thể vô hiệu hóa việc thu gom tự động bằng cách gọi ``gc.disable()``. Để gỡ lỗi một chương trình bị rò rỉ, hãy gọi ``gc.set_debug(gc.DEBUG_LEAK)``. Lưu ý rằng thao tác này bao gồm ``gc.DEBUG_SAVEALL``, khiến các đối tượng được garbage collector thu gom được lưu trong gc.garbage để kiểm tra.

Mô-đun :mod:`!gc` cung cấp các hàm sau:


.. function:: enable()

   Bật garbage collection tự động.


.. function:: disable()

   Tắt garbage collection tự động.


.. function:: isenabled()

   Trả về ``True`` nếu việc thu gom tự động được bật.


.. function:: collect(generation=2)

   Không truyền đối số, hãy thực hiện một lần thu gom đầy đủ. Đối số tùy chọn *generation* có thể là một số nguyên chỉ định thế hệ cần thu gom (từ 0 đến 2). Một
   :exc:`ValueError` sẽ được phát sinh nếu số thế hệ không hợp lệ. Tổng số đối tượng đã thu gom và đối tượng không thể thu gom sẽ được trả về.

   Các free list được duy trì cho một số kiểu dựng sẵn sẽ bị xóa mỗi khi thực hiện thu gom đầy đủ hoặc thu gom thế hệ cao nhất (2). Do cách triển khai cụ thể, không phải mọi mục trong một số free list đều có thể được giải phóng, đặc biệt là :class:`float`.

   Hiệu ứng của việc gọi ``gc.collect()`` trong khi interpreter đang thực hiện thu gom là không xác định.

   .. versionchanged:: 3.14
      ``generation=1`` thực hiện một lần thu gom tăng dần.

   .. versionchanged:: 3.14.5
      ``generation=1`` thực hiện việc thu gom thế hệ trung gian.


.. function:: set_debug(flags)

   Thiết lập các cờ gỡ lỗi của garbage collection. Thông tin gỡ lỗi sẽ được ghi vào ``sys.stderr``. Xem danh sách các cờ gỡ lỗi bên dưới; chúng có thể được kết hợp bằng các phép toán bit để điều khiển hoạt động gỡ lỗi.


.. function:: get_debug()

   Trả về các cờ debugging hiện đang được thiết lập.


.. function:: get_objects(generation=None)

   Trả về danh sách tất cả các đối tượng được collector theo dõi, không bao gồm danh sách được trả về. Nếu *generation* không phải là ``None``, chỉ trả về các đối tượng được collector theo dõi thuộc thế hệ đó.

   .. versionchanged:: 3.8
      Tham số *generation* mới.

   .. versionchanged:: 3.14
      Thế hệ 1 bị loại bỏ

   .. versionchanged:: 3.14.5
      Thế hệ 1 được giới thiệu lại để duy trì hành vi GC từ phiên bản 3.13.

   .. audit-event:: gc.get_objects generation gc.get_objects

.. function:: get_stats()

   Trả về danh sách gồm ba dictionary theo từng thế hệ, chứa các thống kê về việc thu gom kể từ khi trình thông dịch khởi động. Số lượng khóa có thể thay đổi trong tương lai, nhưng hiện tại mỗi dictionary sẽ chứa các mục sau:

   * ``collections`` là số lần thế hệ này được thu gom;

   * ``collected`` là tổng số đối tượng được thu gom trong thế hệ này;

   * ``uncollectable`` là tổng số đối tượng được phát hiện là không thể thu gom (và do đó được chuyển vào danh sách :data:`garbage`) trong thế hệ này.

   .. versionadded:: 3.4


.. function:: set_threshold(threshold0, [threshold1, [threshold2]])

   Đặt các ngưỡng thu gom rác (tần suất thu gom). Đặt *threshold0* thành 0 sẽ tắt tính năng thu gom.

   GC phân loại các đối tượng thành ba thế hệ, tùy thuộc vào số lượt quét thu gom mà chúng đã vượt qua. Các đối tượng mới được đặt vào thế hệ nhỏ tuổi nhất (thế hệ ``0``). Nếu một đối tượng sống sót sau một lần thu gom, nó sẽ được chuyển vào thế hệ lớn tuổi hơn tiếp theo. Vì thế hệ ``2`` là thế hệ lớn tuổi nhất, các đối tượng trong thế hệ đó vẫn ở lại đó sau khi thu gom. Để quyết định thời điểm chạy, bộ thu gom theo dõi số lần cấp phát và giải phóng đối tượng kể từ lần thu gom gần nhất. Khi số lần cấp phát trừ đi số lần giải phóng vượt quá *threshold0*, quá trình thu gom bắt đầu. Ban đầu, chỉ thế hệ ``0`` được kiểm tra. Nếu thế hệ ``0`` đã được kiểm tra nhiều hơn *threshold1* lần kể từ khi thế hệ ``1`` được kiểm tra, thì thế hệ ``1`` cũng được kiểm tra. Với thế hệ thứ ba, mọi việc phức tạp hơn một chút; xem `Thu gom thế hệ lớn tuổi nhất <https://github.com/python/cpython/blob/ff0ef0a54bef26fc507fbf9b7a6009eb7d3f17f5/InternalDocs/garbage_collector.md#collecting-the-oldest-generation>`_ để biết thêm thông tin.

   Trong bản dựng free-threaded, mức tăng mức sử dụng bộ nhớ của tiến trình cũng được kiểm tra trước khi chạy bộ thu gom. Nếu mức sử dụng bộ nhớ chưa tăng 10% kể từ lần thu gom gần nhất và số lần cấp phát đối tượng ròng chưa vượt quá 40 lần *threshold0*, thì quá trình thu gom sẽ không chạy.

   Xem `Thiết kế bộ thu gom rác <https://github.com/python/cpython/blob/3.14/InternalDocs/garbage_collector.md>`_ để biết thêm thông tin.

   .. versionchanged:: 3.14
      *threshold2* bị bỏ qua

   .. versionchanged:: 3.14.5
      *threshold2* được khôi phục để khớp với hành vi của Python 3.13.


.. function:: get_count()

   Trả về các số đếm của quá trình thu gom hiện tại dưới dạng một tuple gồm ``(count0, count1, count2)``.


.. function:: get_threshold()

   Trả về các ngưỡng thu gom hiện tại dưới dạng một tuple gồm ``(threshold0, threshold1, threshold2)``.


.. function:: get_referrers(*objs)

   Trả về danh sách các đối tượng tham chiếu trực tiếp đến bất kỳ đối tượng nào trong objs. Hàm này chỉ tìm các container hỗ trợ garbage collection; những extension type có tham chiếu đến các đối tượng khác nhưng không hỗ trợ garbage collection sẽ không được tìm thấy.

   Lưu ý rằng các đối tượng đã bị hủy tham chiếu nhưng vẫn nằm trong các chu kỳ và chưa được garbage collector thu gom có thể xuất hiện trong danh sách các đối tượng tham chiếu kết quả. Để chỉ lấy các đối tượng hiện đang tồn tại, hãy gọi :func:`collect` trước khi gọi :func:`get_referrers`.

   .. warning::
      Cần thận trọng khi sử dụng các đối tượng được :func:`get_referrers` trả về vì một số đối tượng trong đó có thể vẫn đang được khởi tạo và do đó đang ở trạng thái tạm thời không hợp lệ. Tránh sử dụng :func:`get_referrers` cho bất kỳ mục đích nào ngoài việc debug.

   .. audit-event:: gc.get_referrers objs gc.get_referrers


.. function:: get_referents(*objs)

   Trả về danh sách các đối tượng được bất kỳ đối số nào tham chiếu trực tiếp. Các đối tượng được tham chiếu trả về là những đối tượng được các đối số duyệt qua ở cấp độ C
   các phương thức :c:member:`~PyTypeObject.tp_traverse` (nếu có), và có thể không bao gồm tất cả các đối tượng thực sự có thể truy cập trực tiếp. Các phương thức :c:member:`~PyTypeObject.tp_traverse` chỉ được hỗ trợ bởi những đối tượng hỗ trợ garbage collection và chỉ bắt buộc phải duyệt qua các đối tượng có thể liên quan đến một chu trình. Vì vậy, chẳng hạn, nếu một số nguyên có thể truy cập trực tiếp từ một đối số, đối tượng số nguyên đó có thể xuất hiện hoặc không xuất hiện trong danh sách kết quả.

   .. audit-event:: gc.get_referents objs gc.get_referents

.. function:: is_tracked(obj)

   Trả về ``True`` nếu đối tượng hiện đang được garbage collector theo dõi, ngược lại trả về ``False``. Theo nguyên tắc chung, các instance của kiểu atomic không được theo dõi, còn các instance của kiểu non-atomic (container, đối tượng do người dùng định nghĩa...) thì được theo dõi. Tuy nhiên, một số tối ưu hóa dành riêng cho từng kiểu có thể được áp dụng để giảm footprint của garbage collector đối với các instance đơn giản (ví dụ: dict chỉ chứa các key và value atomic).::

      >>> gc.is_tracked(0)
      False
      >>> gc.is_tracked("a")
      False
      >>> gc.is_tracked([])
      True
      >>> gc.is_tracked({})
      False
      >>> gc.is_tracked({"a": 1})
      True

   .. versionadded:: 3.1


.. function:: is_finalized(obj)

   Trả về ``True`` nếu đối tượng đã cho đã được garbage collector hoàn tất việc xử lý, ngược lại trả về ``False``.::

      >>> x = None
      >>> class Lazarus:
      ...     def __del__(self):
      ...         global x
      ...         x = self
      ...
      >>> lazarus = Lazarus()
      >>> gc.is_finalized(lazarus)
      False
      >>> del lazarus
      >>> gc.is_finalized(x)
      True

   .. versionadded:: 3.9


.. function:: freeze()

   Đóng băng tất cả các đối tượng được garbage collector theo dõi; chuyển chúng vào một generation vĩnh viễn và bỏ qua chúng trong tất cả các lần collection sau này.

   Nếu một process sẽ ``fork()`` mà không ``exec()``, việc tránh copy-on-write không cần thiết trong các process con sẽ tối đa hóa việc chia sẻ bộ nhớ và giảm mức sử dụng bộ nhớ tổng thể. Điều này đòi hỏi vừa tránh tạo các "lỗ trống" đã được giải phóng trong các trang bộ nhớ của process cha, vừa đảm bảo rằng các lần collection của GC trong các process con sẽ không chạm đến bộ đếm ``gc_refs`` của các đối tượng tồn tại lâu có nguồn gốc từ process cha. Để thực hiện cả hai điều này, hãy gọi ``gc.disable()`` sớm trong process cha, ``gc.freeze()`` ngay trước ``fork()``, và ``gc.enable()`` sớm trong các process con.

   .. versionadded:: 3.7


.. function:: unfreeze()

   Bỏ đóng băng các đối tượng trong generation vĩnh viễn, đưa chúng trở lại generation cũ nhất.

   .. versionadded:: 3.7


.. function:: get_freeze_count()

   Trả về số lượng đối tượng trong generation vĩnh viễn.

   .. versionadded:: 3.7


Các biến sau đây được cung cấp để truy cập chỉ đọc (bạn có thể thay đổi các giá trị, nhưng không nên gán lại chúng):

.. data:: garbage

   Danh sách các đối tượng mà bộ thu gom phát hiện là không thể truy cập nhưng không thể giải phóng (các đối tượng không thể thu gom). Kể từ Python 3.4, danh sách này hầu hết thời gian sẽ trống, ngoại trừ khi sử dụng các thực thể của kiểu phần mở rộng C có slot ``NULL`` ``tp_del`` không phải là.

   Nếu :const:`DEBUG_SAVEALL` được đặt, tất cả các đối tượng không thể truy cập sẽ được thêm vào danh sách này thay vì được giải phóng.

   .. versionchanged:: 3.2
      Nếu danh sách này không trống tại :term:`interpreter shutdown`, một
      :exc:`ResourceWarning` sẽ được phát ra, mặc định không hiển thị gì. Nếu
      :const:`DEBUG_UNCOLLECTABLE` được đặt, ngoài ra tất cả các đối tượng không thể thu gom cũng sẽ được in ra.

   .. versionchanged:: 3.4
      Sau :pep:`442`, các đối tượng có phương thức :meth:`~object.__del__` sẽ không còn được đưa vào :data:`gc.garbage` nữa.

.. data:: callbacks

   Danh sách các callback sẽ được garbage collector gọi trước và sau khi thu gom. Các callback sẽ được gọi với hai đối số, *phase* và *info*.

   *phase* có thể là một trong hai giá trị sau:

      "start": Hoạt động thu gom rác sắp bắt đầu.

      "stop": Hoạt động thu gom rác đã hoàn tất.

   *info* là một dict cung cấp thêm thông tin cho callback. Hiện tại, các khóa sau được định nghĩa:

      "generation": Thế hệ cũ nhất đang được thu gom.

      "collected": Khi *phase* là "stop", số lượng đối tượng đã được thu gom thành công.

      "uncollectable": Khi *phase* là "stop", số lượng đối tượng không thể được thu gom và đã được đưa vào :data:`garbage`.

   Ứng dụng có thể thêm callback riêng vào danh sách này. Các trường hợp sử dụng chính là:

      Thu thập thống kê về quá trình thu gom rác, chẳng hạn như tần suất thu gom các thế hệ khác nhau và thời gian thực hiện việc thu gom.

      Cho phép ứng dụng xác định và xóa các kiểu không thể thu gom của riêng mình khi chúng xuất hiện trong :data:`garbage`.

   .. versionadded:: 3.3


Các hằng số sau được cung cấp để sử dụng với :func:`set_debug`:


.. data:: DEBUG_STATS

   In thống kê trong quá trình thu gom. Thông tin này có thể hữu ích khi điều chỉnh tần suất thu gom.


.. data:: DEBUG_COLLECTABLE

   In thông tin về các đối tượng có thể thu gom được tìm thấy.


.. data:: DEBUG_UNCOLLECTABLE

   In thông tin về các đối tượng không thể thu gom được (các đối tượng không thể truy cập nhưng không thể được bộ thu gom giải phóng). Các đối tượng này sẽ được thêm vào danh sách ``garbage``.

   .. versionchanged:: 3.2
      Đồng thời in nội dung của danh sách :data:`garbage` tại
      :term:`interpreter shutdown`, nếu danh sách này không rỗng.

.. data:: DEBUG_SAVEALL

   Khi được thiết lập, tất cả các đối tượng không thể truy cập được tìm thấy sẽ được thêm vào *garbage* thay vì được giải phóng. Điều này có thể hữu ích khi gỡ lỗi một chương trình bị rò rỉ bộ nhớ.


.. data:: DEBUG_LEAK

   Các cờ gỡ lỗi cần thiết để bộ thu gom in thông tin về một chương trình bị rò rỉ bộ nhớ (tương đương với ``DEBUG_COLLECTABLE | DEBUG_UNCOLLECTABLE | DEBUG_SAVEALL``).

.. _`Collecting the oldest generation`: https://github.com/python/cpython/blob/ff0ef0a54bef26fc507fbf9b7a6009eb7d3f17f5/InternalDocs/garbage_collector.md#collecting-the-oldest-generation
.. _`Garbage collector design`: https://github.com/python/cpython/blob/3.14/InternalDocs/garbage_collector.md
