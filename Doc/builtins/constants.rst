.. _built-in-consts:

Hằng số tích hợp sẵn
====================

Một số ít hằng số nằm trong namespace tích hợp sẵn. Chúng là:

.. data:: False

   Giá trị false của kiểu :class:`bool`. Không được phép gán cho ``False`` và thao tác này sẽ gây ra :exc:`SyntaxError`.


.. data:: True

   Giá trị true của kiểu :class:`bool`. Không được phép gán cho ``True`` và thao tác này sẽ gây ra :exc:`SyntaxError`.


.. data:: None

   Một đối tượng thường được dùng để biểu thị sự vắng mặt của một giá trị, chẳng hạn khi các đối số mặc định không được truyền cho một hàm. Không được phép gán cho ``None`` và thao tác này sẽ gây ra :exc:`SyntaxError`. ``None`` là thể hiện duy nhất của kiểu :class:`~types.NoneType`.


.. data:: NotImplemented

   Một giá trị đặc biệt nên được các phương thức đặc biệt nhị phân (ví dụ: :meth:`~object.__eq__`, :meth:`~object.__lt__`, :meth:`~object.__add__`, :meth:`~object.__rsub__`, v.v.) trả về để cho biết rằng thao tác chưa được triển khai đối với kiểu còn lại; các phương thức đặc biệt nhị phân tại chỗ (ví dụ: :meth:`~object.__imul__`, :meth:`~object.__iand__`, v.v.) cũng có thể trả về giá trị này với cùng mục đích. Không nên đánh giá giá trị này trong ngữ cảnh boolean.
   :data:`!NotImplemented` là thể hiện duy nhất của kiểu :class:`types.NotImplementedType`.

   .. note::

      Khi một phương thức nhị phân (hoặc tại chỗ) trả về :data:`!NotImplemented`, trình thông dịch sẽ thử thực hiện phép toán phản chiếu trên kiểu còn lại (hoặc một phương án dự phòng khác, tùy thuộc vào toán tử). Nếu mọi lần thử đều trả về
      :data:`!NotImplemented`, trình thông dịch sẽ đưa ra một ngoại lệ thích hợp. Việc trả về :data:`!NotImplemented` không chính xác sẽ dẫn đến thông báo lỗi gây hiểu nhầm hoặc giá trị :data:`!NotImplemented` được trả về cho mã Python.

      Xem :ref:`implementing-the-arithmetic-operations` để biết các ví dụ.

   .. caution::

      :data:`!NotImplemented` và :exc:`!NotImplementedError` không thể thay thế cho nhau. Chỉ nên sử dụng hằng số này như mô tả ở trên; xem :exc:`NotImplementedError` để biết chi tiết về cách sử dụng ngoại lệ này đúng cách.

   .. versionchanged:: 3.9
      Việc đánh giá :data:`!NotImplemented` trong ngữ cảnh boolean đã không còn được khuyến nghị.

   .. versionchanged:: 3.14
      Việc đánh giá :data:`!NotImplemented` trong ngữ cảnh boolean hiện sẽ đưa ra một :exc:`TypeError`. Trước đây, nó được đánh giá thành :const:`True` và phát ra một :exc:`DeprecationWarning` kể từ Python 3.9.


.. index:: single: ...; ellipsis literal
.. data:: Ellipsis

   Tương tự literal dấu ba chấm "``...``", đây là một đối tượng thường được dùng để biểu thị rằng một phần nào đó bị lược bỏ. Có thể gán giá trị cho ``Ellipsis``, nhưng việc gán giá trị cho ``...`` sẽ đưa ra một :exc:`SyntaxError`. ``Ellipsis`` là thể hiện duy nhất của kiểu :class:`types.EllipsisType`.


.. data:: __debug__

   Hằng số này là true nếu Python không được khởi động với tùy chọn :option:`-O`. Xem thêm câu lệnh :keyword:`assert`.


.. note::

   Các tên :data:`None`, :data:`False`, :data:`True` và :data:`__debug__` không thể được gán lại (việc gán cho chúng, ngay cả khi làm tên thuộc tính, sẽ gây ra
   :exc:`SyntaxError`), vì vậy chúng có thể được xem là các hằng số "true".


.. _site-consts:

Các hằng số được thêm bởi module :mod:`site`
--------------------------------------------

Module :mod:`site` (được tự động import trong quá trình khởi động, trừ khi cung cấp tùy chọn dòng lệnh :option:`-S`) thêm một số hằng số vào namespace tích hợp sẵn. Chúng hữu ích cho shell của trình thông dịch tương tác và không nên được sử dụng trong các chương trình.

.. data:: quit(code=None)
          exit(code=None)

   Các đối tượng này khi được in sẽ in một thông báo như "Use quit() or Ctrl-D (i.e. EOF) to exit", còn khi được truy cập trực tiếp trong trình thông dịch tương tác hoặc được gọi như các hàm, sẽ raise :exc:`SystemExit` với mã thoát được chỉ định.

.. data:: help
   :noindex:

   Đối tượng khi được in ra sẽ in thông báo "Type help() for interactive help, or help(object) for help about object.", và khi được truy cập trực tiếp trong trình thông dịch tương tác, sẽ gọi hệ thống trợ giúp tích hợp sẵn (xem :func:`help`).

.. data:: copyright
          credits

   Các đối tượng khi được in ra hoặc được gọi sẽ lần lượt in nội dung bản quyền hoặc credits.

.. data:: license

   Đối tượng khi được in ra sẽ in thông báo "Type license() to see the full license text", và khi được gọi sẽ hiển thị toàn bộ nội dung giấy phép theo cách giống trình phân trang (mỗi lần một màn hình).
