:mod:`!traceback` --- In hoặc truy xuất traceback của ngăn xếp
==============================================================

.. module:: traceback
   :synopsis: In hoặc truy xuất traceback của ngăn xếp.

**Mã nguồn:** :source:`Lib/traceback.py`

--------------

Mô-đun này cung cấp một giao diện chuẩn để trích xuất, định dạng và in các stack trace của chương trình Python. Mô-đun này linh hoạt hơn cách trình thông dịch hiển thị traceback theo mặc định, do đó cho phép cấu hình một số khía cạnh của đầu ra. Cuối cùng, mô-đun này chứa một tiện ích để thu thập đủ thông tin về một exception nhằm in thông tin đó sau này mà không cần lưu tham chiếu đến chính exception đó. Vì các exception có thể là gốc của một đồ thị đối tượng lớn, tiện ích này có thể cải thiện đáng kể việc quản lý bộ nhớ.

.. index:: pair: object; traceback

Mô-đun sử dụng các :ref:`đối tượng traceback <traceback-objects>` --- đây là các đối tượng thuộc kiểu :class:`types.TracebackType`, được gán cho trường :attr:`~BaseException.__traceback__` của
:class:`BaseException` các instance.

.. seealso::

   Mô-đun :mod:`faulthandler`
      Dùng để kết xuất rõ ràng các traceback của Python khi xảy ra lỗi, sau một khoảng thời gian chờ hoặc khi nhận tín hiệu từ người dùng.

   Mô-đun :mod:`pdb`
      Trình debugger mã nguồn tương tác dành cho các chương trình Python.

API của mô-đun có thể được chia thành hai phần:

* Các hàm cấp mô-đun cung cấp chức năng cơ bản, hữu ích để kiểm tra tương tác các exception và traceback.

* Lớp :class:`TracebackException` và các lớp trợ giúp của nó
  :class:`StackSummary` và :class:`FrameSummary`. Các thành phần này vừa cung cấp nhiều tính linh hoạt hơn trong đầu ra được tạo, vừa cho phép lưu trữ thông tin cần thiết để định dạng sau này mà không phải giữ tham chiếu đến các đối tượng exception và traceback thực tế.

.. versionadded:: 3.13
   Theo mặc định, đầu ra được tô màu và có thể được
   :ref:`điều khiển bằng các biến môi trường <using-on-controlling-color>`.


Các hàm cấp mô-đun
------------------

.. function:: print_tb(tb, limit=None, file=None)

   In tối đa *limit* mục trong dấu vết ngăn xếp từ
   :ref:`đối tượng traceback <traceback-objects>` *tb* (bắt đầu từ frame của caller) nếu *limit* là số dương. Nếu không, in các mục cuối cùng ``abs(limit)``. Nếu *limit* bị bỏ qua hoặc là ``None``, tất cả các mục sẽ được in. Nếu *file* bị bỏ qua hoặc là ``None``, đầu ra sẽ được chuyển đến
   :data:`sys.stderr`; nếu không, đó phải là một tệp đang mở
   :term:`file <file object>` hoặc :term:`file-like object` để nhận đầu ra.

   .. note::

      Ý nghĩa của tham số *limit* khác với ý nghĩa của :const:`sys.tracebacklimit`. Một giá trị *limit* âm tương ứng với một giá trị dương của :const:`!sys.tracebacklimit`, trong khi không thể đạt được hành vi của một giá trị *limit* dương bằng
      :const:`!sys.tracebacklimit`.

   .. versionchanged:: 3.5
       Đã bổ sung hỗ trợ *limit* âm.


.. function:: print_exception(exc, /[, value, tb], limit=None, \
                              file=None, chain=True)

   In thông tin về ngoại lệ và các mục trong stack trace từ
   :ref:`đối tượng traceback <traceback-objects>` *tb* đến *file*. Điều này khác với :func:`print_tb` theo những cách sau:

   * nếu *tb* không phải là ``None``, hàm sẽ in một tiêu đề ``Traceback (most recent call last):``

   * in kiểu ngoại lệ và *value* sau stack trace

   .. index:: single: ^ (caret); marker

   * nếu *type(value)* là :exc:`SyntaxError` và *value* có định dạng phù hợp, nó sẽ in dòng xảy ra lỗi cú pháp với dấu mũ chỉ vị trí gần đúng của lỗi.

   Kể từ Python 3.10, thay vì truyền *value* và *tb*, bạn có thể truyền một đối tượng exception làm đối số đầu tiên. Nếu cung cấp *value* và *tb*, đối số đầu tiên sẽ bị bỏ qua để đảm bảo khả năng tương thích ngược.

   Đối số tùy chọn *limit* có cùng ý nghĩa như đối với :func:`print_tb`. Nếu *chain* là true (mặc định), các exception được liên kết (the
   :attr:`~BaseException.__cause__` hoặc :attr:`~BaseException.__context__` của exception) cũng sẽ được in, giống như chính interpreter khi in một exception chưa được xử lý.

   .. versionchanged:: 3.5
      Đối số *etype* bị bỏ qua và được suy ra từ kiểu của *value*.

   .. versionchanged:: 3.10
      Tham số *etype* đã được đổi tên thành *exc* và hiện chỉ được truyền theo vị trí.


.. function:: print_exc(limit=None, file=None, chain=True)

   Đây là cách viết tắt của ``print_exception(sys.exception(), limit=limit, file=file, chain=chain)``.


.. function:: print_last(limit=None, file=None, chain=True)

   Đây là cách viết tắt của ``print_exception(sys.last_exc, limit=limit, file=file, chain=chain)``.  Nhìn chung, cách này chỉ hoạt động sau khi một exception đã đến interactive prompt (xem :data:`sys.last_exc`).


.. function:: print_stack(f=None, limit=None, file=None)

   In tối đa *limit* mục stack trace (bắt đầu từ điểm gọi) nếu *limit* là số dương.  Nếu không, in ``abs(limit)`` mục cuối cùng.  Nếu *limit* bị bỏ qua hoặc là ``None``, tất cả các mục sẽ được in. Có thể sử dụng đối số tùy chọn *f* để chỉ định một
   :ref:`stack frame <frame-objects>` thay thế để bắt đầu.  Đối số tùy chọn *file* có cùng ý nghĩa như đối số của
   :func:`print_tb`.

   .. versionchanged:: 3.5
          Đã bổ sung hỗ trợ *limit* âm.


.. function:: extract_tb(tb, limit=None)

   Trả về một đối tượng :class:`StackSummary` đại diện cho danh sách các mục stack trace đã được "tiền xử lý", được trích xuất từ
   :ref:`traceback object <traceback-objects>` *tb*.  Đối tượng này hữu ích khi cần định dạng stack trace theo cách khác.  Đối số tùy chọn *limit* có cùng ý nghĩa như đối số của :func:`print_tb`.  Một mục stack trace đã được "tiền xử lý" là một đối tượng :class:`FrameSummary` có các thuộc tính biểu diễn thông tin thường được in cho một stack trace.


.. function:: extract_stack(f=None, limit=None)

   Trích xuất traceback thô từ
   :ref:`stack frame <frame-objects>`. Giá trị trả về có cùng định dạng như đối với :func:`extract_tb`. Các đối số tùy chọn *f* và *limit* có cùng ý nghĩa như đối với :func:`print_stack`.


.. function:: print_list(extracted_list, file=None)

   In danh sách các tuple như được trả về bởi :func:`extract_tb` hoặc
   :func:`extract_stack` dưới dạng một stack trace được định dạng vào tệp được chỉ định. Nếu *file* là ``None``, đầu ra sẽ được ghi vào :data:`sys.stderr`.


.. function:: format_list(extracted_list)

   Với một danh sách các tuple hoặc các đối tượng :class:`FrameSummary` như được trả về bởi
   :func:`extract_tb` hoặc :func:`extract_stack`, trả về một danh sách các chuỗi sẵn sàng để in. Mỗi chuỗi trong danh sách kết quả tương ứng với mục có cùng chỉ mục trong danh sách đối số. Mỗi chuỗi kết thúc bằng một dòng mới; các chuỗi cũng có thể chứa những dòng mới bên trong, đối với những mục có dòng văn bản nguồn không phải là ``None``.


.. function:: format_exception_only(exc, /[, value], *, show_group=False)

   Định dạng phần exception của một traceback bằng một giá trị exception, chẳng hạn như giá trị được cung cấp bởi :data:`sys.last_exc`. Giá trị trả về là một danh sách các chuỗi, mỗi chuỗi kết thúc bằng một dòng mới. Danh sách này chứa thông báo của exception, thường là một chuỗi đơn; tuy nhiên, đối với các exception :exc:`SyntaxError`, danh sách chứa nhiều dòng, khi được in ra sẽ hiển thị thông tin chi tiết về vị trí xảy ra lỗi cú pháp. Sau thông báo, danh sách chứa :attr:`notes <BaseException.__notes__>` của exception.

   Kể từ Python 3.10, thay vì truyền *value*, có thể truyền một đối tượng exception làm đối số đầu tiên. Nếu cung cấp *value*, đối số đầu tiên sẽ bị bỏ qua để duy trì khả năng tương thích ngược.

   Khi *show_group* là ``True``, và ngoại lệ là một thể hiện của
   :exc:`BaseExceptionGroup`, các ngoại lệ lồng nhau cũng được bao gồm theo cách đệ quy, với mức thụt lề tương ứng với độ sâu lồng nhau của chúng.

   .. versionchanged:: 3.10
      Tham số *etype* đã được đổi tên thành *exc* và hiện chỉ được truyền theo vị trí.

   .. versionchanged:: 3.11
      Danh sách được trả về giờ đây bao gồm mọi
      :attr:`notes <BaseException.__notes__>` được đính kèm với ngoại lệ.

   .. versionchanged:: 3.13
      Đã thêm tham số *show_group*.


.. function:: format_exception(exc, /[, value, tb], limit=None, chain=True)

   Định dạng stack trace và thông tin ngoại lệ. Các đối số có cùng ý nghĩa với những đối số tương ứng của :func:`print_exception`. Giá trị trả về là một danh sách các chuỗi, mỗi chuỗi kết thúc bằng một dòng mới và một số chuỗi chứa các dòng mới bên trong. Khi các dòng này được nối lại và in ra, chính xác cùng một văn bản được in ra như khi gọi :func:`print_exception`.

   .. versionchanged:: 3.5
      Đối số *etype* bị bỏ qua và được suy ra từ kiểu của *value*.

   .. versionchanged:: 3.10
      Hành vi và chữ ký của hàm này đã được sửa đổi để khớp với
      :func:`print_exception`.


.. function:: format_exc(limit=None, chain=True)

   Tương tự như ``print_exc(limit)`` nhưng trả về một chuỗi thay vì in ra tệp.


.. function:: format_tb(tb, limit=None)

   Cách viết tắt của ``format_list(extract_tb(tb, limit))``.


.. function:: format_stack(f=None, limit=None)

   Cách viết tắt của ``format_list(extract_stack(f, limit))``.

.. function:: clear_frames(tb)

   Xóa các biến cục bộ của tất cả các khung ngăn xếp trong một
   :ref:`traceback <traceback-objects>` *tb* bằng cách gọi phương thức :meth:`~frame.clear` của mỗi
   :ref:`đối tượng frame <frame-objects>`.

   .. versionadded:: 3.4

.. function:: walk_stack(f)

   Duyệt qua một stack theo :attr:`f.f_back <frame.f_back>` từ frame đã cho, trả về frame và số dòng cho từng frame. Nếu *f* là ``None``, stack hiện tại sẽ được sử dụng. Helper này được dùng với :meth:`StackSummary.extract`.

   .. versionadded:: 3.5

   .. versionchanged:: 3.14
      Trước đây, hàm này trả về một generator sẽ duyệt qua stack khi được lặp lần đầu. Generator được trả về hiện nay chứa trạng thái của stack tại thời điểm ``walk_stack`` được gọi.

.. function:: walk_tb(tb)

   Duyệt qua một traceback theo :attr:`~traceback.tb_next`, trả về frame và số dòng cho từng frame. Helper này được dùng với :meth:`StackSummary.extract`.

   .. versionadded:: 3.5


:class:`!TracebackException` Đối tượng
--------------------------------------

.. versionadded:: 3.5

:class:`!TracebackException` được tạo từ các exception thực tế để thu thập dữ liệu cho việc in sau này. Chúng cung cấp một phương thức nhẹ hơn để lưu trữ thông tin này bằng cách tránh giữ tham chiếu đến
:ref:`traceback <traceback-objects>` và :ref:`frame <frame-objects>`. Ngoài ra, chúng cung cấp nhiều tùy chọn hơn để cấu hình đầu ra so với các hàm cấp module được mô tả ở trên.

.. class:: TracebackException(exc_type, exc_value, exc_traceback, *, limit=None, lookup_lines=True, capture_locals=False, compact=False, max_group_width=15, max_group_depth=10)

   Ghi lại một exception để kết xuất sau. Ý nghĩa của *limit*, *lookup_lines* và *capture_locals* giống như đối với lớp :class:`StackSummary`.

   Nếu *compact* là true, chỉ dữ liệu cần thiết cho
   Phương thức :meth:`format` của :class:`!TracebackException` được lưu trong các thuộc tính của lớp. Cụ thể,
   Trường :attr:`__context__` chỉ được tính nếu :attr:`__cause__` là ``None`` và :attr:`__suppress_context__` là false.

   Lưu ý rằng khi các biến cục bộ được ghi lại, chúng cũng được hiển thị trong traceback.

   *max_group_width* và *max_group_depth* kiểm soát việc định dạng các exception group (xem :exc:`BaseExceptionGroup`). Độ sâu đề cập đến cấp độ lồng nhau của group, còn chiều rộng đề cập đến kích thước của mảng exceptions thuộc một exception group. Kết quả được định dạng sẽ bị cắt bớt khi vượt quá một trong hai giới hạn.

   .. versionchanged:: 3.10
      Đã thêm tham số *compact*.

   .. versionchanged:: 3.11
      Đã thêm các tham số *max_group_width* và *max_group_depth*.

   .. attribute:: __cause__

      Một :class:`!TracebackException` của đối tượng ban đầu
      :attr:`~BaseException.__cause__`.

   .. attribute:: __context__

      Một :class:`!TracebackException` của đối tượng ban đầu
      :attr:`~BaseException.__context__`.

   .. attribute:: exceptions

      Nếu ``self`` đại diện cho một :exc:`ExceptionGroup`, trường này chứa một danh sách
      các thực thể :class:`!TracebackException` đại diện cho những ngoại lệ lồng nhau. Nếu không, nó là ``None``.

      .. versionadded:: 3.11

   .. attribute:: __suppress_context__

      Giá trị :attr:`~BaseException.__suppress_context__` từ ngoại lệ ban đầu.

   .. attribute:: __notes__

      Giá trị :attr:`~BaseException.__notes__` từ ngoại lệ ban đầu, hoặc ``None`` nếu ngoại lệ không có ghi chú nào. Nếu nó không phải là ``None``, nó sẽ được định dạng trong traceback sau chuỗi ngoại lệ.

      .. versionadded:: 3.11

   .. attribute:: stack

      Một :class:`StackSummary` biểu diễn traceback.

   .. attribute:: exc_type

      Lớp của exception ban đầu.

      .. deprecated:: 3.13

   .. attribute:: exc_type_str

      Hiển thị dưới dạng chuỗi của lớp exception ban đầu.

      .. versionadded:: 3.13

   .. attribute:: filename

      Đối với lỗi cú pháp - tên tệp nơi xảy ra lỗi.

   .. attribute:: lineno

      Đối với lỗi cú pháp - số dòng nơi xảy ra lỗi.

   .. attribute:: end_lineno

      Đối với lỗi cú pháp - số dòng kết thúc nơi xảy ra lỗi. Có thể là ``None`` nếu không có.

      .. versionadded:: 3.10

   .. attribute:: text

      Đối với lỗi cú pháp - văn bản tại nơi xảy ra lỗi.

   .. attribute:: offset

      Đối với lỗi cú pháp - offset trong văn bản tại vị trí xảy ra lỗi.

   .. attribute:: end_offset

      Đối với lỗi cú pháp - offset kết thúc trong văn bản tại vị trí xảy ra lỗi. Có thể là ``None`` nếu không có.

      .. versionadded:: 3.10

   .. attribute:: msg

      Đối với lỗi cú pháp - thông báo lỗi của compiler.

   .. classmethod:: from_exception(exc, *, limit=None, lookup_lines=True, capture_locals=False, compact=False, max_group_width=15, max_group_depth=10)

      Ghi lại một exception để kết xuất sau. *limit*, *lookup_lines* và *capture_locals* giống như đối với class :class:`StackSummary`.

      Lưu ý rằng khi các biến cục bộ được ghi lại, chúng cũng được hiển thị trong traceback.

   .. method::  print(*, file=None, chain=True)

      In thông tin exception được trả về bởi vào *file* (mặc định là ``sys.stderr``).
      :meth:`format`.

      .. versionadded:: 3.11

   .. method:: format(*, chain=True)

      Định dạng exception.

      Nếu *chain* không phải là ``True``, :attr:`__cause__` và :attr:`__context__` sẽ không được định dạng.

      Giá trị trả về là một generator gồm các chuỗi, mỗi chuỗi kết thúc bằng một ký tự xuống dòng và một số chuỗi có chứa các ký tự xuống dòng bên trong. :func:`~traceback.print_exception` là một wrapper của phương thức này, chỉ thực hiện việc in các dòng vào một tệp.

   .. method::  format_exception_only(*, show_group=False)

      Định dạng phần exception của traceback.

      Giá trị trả về là một generator gồm các chuỗi, mỗi chuỗi kết thúc bằng một ký tự xuống dòng.

      Khi *show_group* là ``False``, generator sẽ phát ra thông báo của exception, sau đó là các ghi chú của exception đó (nếu có). Thông báo của exception thường là một chuỗi duy nhất; tuy nhiên, đối với các exception :exc:`SyntaxError`, thông báo gồm nhiều dòng mà khi được in ra sẽ hiển thị thông tin chi tiết về vị trí xảy ra lỗi cú pháp.

      Khi *show_group* là ``True`` và exception là một instance của
      :exc:`BaseExceptionGroup`, các exception lồng nhau cũng được đưa vào, theo cách đệ quy, với mức thụt lề tương ứng với độ sâu lồng nhau của chúng.

      .. versionchanged:: 3.11
         :attr:`notes <BaseException.__notes__>` của exception hiện được đưa vào output.

      .. versionchanged:: 3.13
         Đã thêm tham số *show_group*.


Các đối tượng :class:`!StackSummary`
------------------------------------

.. versionadded:: 3.5

Các đối tượng :class:`!StackSummary` đại diện cho một call stack sẵn sàng để format.

.. class:: StackSummary

   .. classmethod:: extract(frame_gen, *, limit=None, lookup_lines=True, capture_locals=False)

      Tạo một đối tượng :class:`!StackSummary` từ trình tạo frame (chẳng hạn như trình được trả về bởi :func:`~traceback.walk_stack` hoặc
      :func:`~traceback.walk_tb`).

      Nếu cung cấp *limit*, chỉ số frame này được lấy từ *frame_gen*. Nếu *lookup_lines* là ``False``, các đối tượng :class:`FrameSummary` được trả về sẽ chưa đọc các dòng của chúng, giúp giảm chi phí tạo :class:`!StackSummary` (điều này có thể hữu ích nếu đối tượng có thể không thực sự được format). Nếu *capture_locals* là ``True``, các biến cục bộ trong mỗi :class:`!FrameSummary` sẽ được ghi lại dưới dạng biểu diễn đối tượng.

      .. versionchanged:: 3.12
         Các exception phát sinh từ :func:`repr` trên một biến cục bộ (khi *capture_locals* là ``True``) không còn được truyền tiếp đến caller.

   .. classmethod:: from_list(a_list)

      Tạo một đối tượng :class:`!StackSummary` từ một danh sách được cung cấp gồm
      Các đối tượng :class:`FrameSummary` hoặc danh sách tuple kiểu cũ. Mỗi tuple phải là một tuple gồm 4 phần tử, lần lượt là *filename*, *lineno*, *name* và *line*.

   .. method:: format()

      Trả về một danh sách các chuỗi sẵn sàng để in. Mỗi chuỗi trong danh sách kết quả tương ứng với một :ref:`frame <frame-objects>` duy nhất từ stack. Mỗi chuỗi kết thúc bằng một ký tự xuống dòng; các chuỗi cũng có thể chứa những ký tự xuống dòng bên trong, đối với các mục có dòng văn bản nguồn.

      Đối với các chuỗi dài gồm cùng frame và dòng, một vài lần lặp đầu tiên sẽ được hiển thị, sau đó là một dòng tóm tắt cho biết chính xác số lần lặp tiếp theo.

      .. versionchanged:: 3.6
         Các chuỗi frame lặp lại dài hiện được rút gọn.

   .. method:: format_frame_summary(frame_summary)

      Trả về một chuỗi để in một trong các :ref:`frames <frame-objects>` có trong stack. Phương thức này được gọi cho từng đối tượng :class:`FrameSummary` cần được in bởi :meth:`StackSummary.format`. Nếu trả về ``None``, frame sẽ được bỏ qua trong đầu ra.

      .. versionadded:: 3.11


:class:`!FrameSummary` Đối tượng
--------------------------------

.. versionadded:: 3.5

Một đối tượng :class:`!FrameSummary` biểu diễn một :ref:`frame <frame-objects>` duy nhất trong một :ref:`traceback <traceback-objects>`.

.. class:: FrameSummary(filename, lineno, name, *,\
                        lookup_line=True, locals=None,\ line=None, end_lineno=None, colno=None, end_colno=None)

   Biểu diễn một :ref:`frame <frame-objects>` duy nhất trong
   :ref:`traceback <traceback-objects>` hoặc stack đang được định dạng hoặc in ra. Đối tượng này có thể tùy chọn chứa phiên bản được chuyển thành chuỗi của các biến cục bộ của frame. Nếu *lookup_line* là ``False``, mã nguồn sẽ không được tra cứu cho đến khi thuộc tính :attr:`~FrameSummary.line` của :class:`!FrameSummary` được truy cập (điều này cũng xảy ra khi chuyển nó thành một :class:`tuple`).
   :attr:`~FrameSummary.line` có thể được cung cấp trực tiếp và sẽ ngăn hoàn toàn việc tra cứu dòng. *locals* là một ánh xạ biến cục bộ tùy chọn; nếu được cung cấp, các biểu diễn của biến sẽ được lưu trong bản tóm tắt để hiển thị sau.

   Các instance :class:`!FrameSummary` có những thuộc tính sau:

   .. attribute:: FrameSummary.filename

      Tên tệp của mã nguồn cho frame này. Tương đương với việc truy cập
      :attr:`f.f_code.co_filename <codeobject.co_filename>` trên một
      :ref:`đối tượng frame <frame-objects>` *f*.

   .. attribute:: FrameSummary.lineno

      Số dòng của mã nguồn cho frame này.

   .. attribute:: FrameSummary.name

      Tương đương với việc truy cập :attr:`f.f_code.co_name <codeobject.co_name>` trên một :ref:`đối tượng frame <frame-objects>` *f*.

   .. attribute:: FrameSummary.line

      Một chuỗi đại diện cho mã nguồn của frame này, trong đó khoảng trắng ở đầu và cuối đã được loại bỏ. Nếu không có mã nguồn, giá trị là ``None``.

   .. attribute:: FrameSummary.end_lineno

      Số dòng cuối cùng của mã nguồn cho frame này. Theo mặc định, giá trị này được đặt thành ``lineno`` và việc đánh số bắt đầu từ 1.

      .. versionchanged:: 3.13
         Giá trị mặc định đã thay đổi từ ``None`` thành ``lineno``.

   .. attribute:: FrameSummary.colno

      Số cột của mã nguồn cho frame này. Theo mặc định, giá trị là ``None`` và việc đánh chỉ mục bắt đầu từ 0.

   .. attribute:: FrameSummary.end_colno

      Số cột cuối cùng của mã nguồn cho frame này. Theo mặc định, giá trị là ``None`` và việc đánh chỉ mục bắt đầu từ 0.


.. _traceback-example:

Ví dụ về cách sử dụng các hàm cấp mô-đun
----------------------------------------

Ví dụ đơn giản này triển khai một vòng lặp đọc-đánh giá-in cơ bản, tương tự như vòng lặp trình thông dịch tương tác Python tiêu chuẩn (nhưng kém hữu ích hơn). Để xem cách triển khai đầy đủ hơn của vòng lặp trình thông dịch, hãy tham khảo mô-đun :mod:`code`.::

   import sys, traceback

   def run_user_code(envdir):
       source = input(">>> ")
       try:
           exec(source, envdir)
       except Exception:
           print("Exception in user code:")
           print("-"*60)
           traceback.print_exc(file=sys.stdout)
           print("-"*60)

   envdir = {}
   while True:
       run_user_code(envdir)


Ví dụ sau đây minh họa các cách khác nhau để in và định dạng exception và traceback:

.. testcode::

   import sys, traceback

   def lumberjack():
       bright_side_of_life()

   def bright_side_of_life():
       return tuple()[0]

   try:
       lumberjack()
   except IndexError as exc:
       print("*** print_tb:")
       traceback.print_tb(exc.__traceback__, limit=1, file=sys.stdout)
       print("*** print_exception:")
       traceback.print_exception(exc, limit=2, file=sys.stdout)
       print("*** print_exc:")
       traceback.print_exc(limit=2, file=sys.stdout)
       print("*** format_exc, first and last line:")
       formatted_lines = traceback.format_exc().splitlines()
       print(formatted_lines[0])
       print(formatted_lines[-1])
       print("*** format_exception:")
       print(repr(traceback.format_exception(exc)))
       print("*** extract_tb:")
       print(repr(traceback.extract_tb(exc.__traceback__)))
       print("*** format_tb:")
       print(repr(traceback.format_tb(exc.__traceback__)))
       print("*** tb_lineno:", exc.__traceback__.tb_lineno)

Kết quả của ví dụ sẽ có dạng tương tự như sau:

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

   *** print_tb:
     File "<doctest...>", line 10, in <module>
       lumberjack()
       ~~~~~~~~~~^^
   *** print_exception:
   Traceback (most recent call last):
     File "<doctest...>", line 10, in <module>
       lumberjack()
       ~~~~~~~~~~^^
     File "<doctest...>", line 4, in lumberjack
       bright_side_of_life()
       ~~~~~~~~~~~~~~~~~~~^^
   IndexError: tuple index out of range
   *** print_exc:
   Traceback (most recent call last):
     File "<doctest...>", line 10, in <module>
       lumberjack()
       ~~~~~~~~~~^^
     File "<doctest...>", line 4, in lumberjack
       bright_side_of_life()
       ~~~~~~~~~~~~~~~~~~~^^
   IndexError: tuple index out of range
   *** format_exc, first and last line:
   Traceback (most recent call last):
   IndexError: tuple index out of range
   *** format_exception:
   ['Traceback (most recent call last):\n',
    '  File "<doctest default[0]>", line 10, in <module>\n    lumberjack()\n    ~~~~~~~~~~^^\n',
    '  File "<doctest default[0]>", line 4, in lumberjack\n    bright_side_of_life()\n    ~~~~~~~~~~~~~~~~~~~^^\n',
    '  File "<doctest default[0]>", line 7, in bright_side_of_life\n    return tuple()[0]\n           ~~~~~~~^^^\n',
    'IndexError: tuple index out of range\n']
   *** extract_tb:
   [<FrameSummary file <doctest...>, line 10 in <module>>,
    <FrameSummary file <doctest...>, line 4 in lumberjack>,
    <FrameSummary file <doctest...>, line 7 in bright_side_of_life>]
   *** format_tb:
   ['  File "<doctest default[0]>", line 10, in <module>\n    lumberjack()\n    ~~~~~~~~~~^^\n',
    '  File "<doctest default[0]>", line 4, in lumberjack\n    bright_side_of_life()\n    ~~~~~~~~~~~~~~~~~~~^^\n',
    '  File "<doctest default[0]>", line 7, in bright_side_of_life\n    return tuple()[0]\n           ~~~~~~~^^^\n']
   *** tb_lineno: 10


Ví dụ sau đây trình bày các cách khác nhau để in và định dạng stack::

   >>> import traceback
   >>> def another_function():
   ...     lumberstack()
   ...
   >>> def lumberstack():
   ...     traceback.print_stack()
   ...     print(repr(traceback.extract_stack()))
   ...     print(repr(traceback.format_stack()))
   ...
   >>> another_function()
     File "<doctest>", line 10, in <module>
       another_function()
     File "<doctest>", line 3, in another_function
       lumberstack()
     File "<doctest>", line 6, in lumberstack
       traceback.print_stack()
   [('<doctest>', 10, '<module>', 'another_function()'),
    ('<doctest>', 3, 'another_function', 'lumberstack()'),
    ('<doctest>', 7, 'lumberstack', 'print(repr(traceback.extract_stack()))')]
   ['  File "<doctest>", line 10, in <module>\n    another_function()\n',
    '  File "<doctest>", line 3, in another_function\n    lumberstack()\n',
    '  File "<doctest>", line 8, in lumberstack\n    print(repr(traceback.format_stack()))\n']


Ví dụ cuối cùng này minh họa một vài hàm định dạng cuối cùng:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> import traceback
   >>> traceback.format_list([('spam.py', 3, '<module>', 'spam.eggs()'),
   ...                        ('eggs.py', 42, 'eggs', 'return "bacon"')])
   ['  File "spam.py", line 3, in <module>\n    spam.eggs()\n',
    '  File "eggs.py", line 42, in eggs\n    return "bacon"\n']
   >>> an_error = IndexError('tuple index out of range')
   >>> traceback.format_exception_only(an_error)
   ['IndexError: tuple index out of range\n']


Ví dụ về việc sử dụng :class:`TracebackException`
-------------------------------------------------

Với lớp trợ giúp, chúng ta có thêm nhiều tùy chọn::

   >>> import sys
   >>> from traceback import TracebackException
   >>>
   >>> def lumberjack():
   ...     bright_side_of_life()
   ...
   >>> def bright_side_of_life():
   ...     t = "bright", "side", "of", "life"
   ...     return t[5]
   ...
   >>> try:
   ...     lumberjack()
   ... except IndexError as e:
   ...     exc = e
   ...
   >>> try:
   ...     try:
   ...         lumberjack()
   ...     except:
   ...         1/0
   ... except Exception as e:
   ...     chained_exc = e
   ...
   >>> # limit hoạt động giống như trong các hàm cấp mô-đun
   >>> TracebackException.from_exception(exc, limit=-2).print()
   Traceback (most recent call last):
     File "<python-input-1>", line 6, in lumberjack
       bright_side_of_life()
       ~~~~~~~~~~~~~~~~~~~^^
     File "<python-input-1>", line 10, in bright_side_of_life
       return t[5]
              ~^^^
   IndexError: tuple index out of range

   >>> # capture_locals thêm các biến cục bộ trong các frame
   >>> TracebackException.from_exception(exc, limit=-2, capture_locals=True).print()
   Traceback (most recent call last):
     File "<python-input-1>", line 6, in lumberjack
       bright_side_of_life()
       ~~~~~~~~~~~~~~~~~~~^^
     File "<python-input-1>", line 10, in bright_side_of_life
       return t[5]
              ~^^^
       t = ("bright", "side", "of", "life")
   IndexError: tuple index out of range

   >>> # kwarg *chain* truyền cho print() kiểm soát việc các exception liên kết có được
   >>> # hiển thị hay không
   >>> TracebackException.from_exception(chained_exc).print()
   Traceback (most recent call last):
     File "<python-input-19>", line 4, in <module>
       lumberjack()
       ~~~~~~~~~~^^
     File "<python-input-8>", line 7, in lumberjack
       bright_side_of_life()
       ~~~~~~~~~~~~~~~~~~~^^
     File "<python-input-8>", line 11, in bright_side_of_life
       return t[5]
              ~^^^
   IndexError: tuple index out of range

   During handling of the above exception, another exception occurred:

   Traceback (most recent call last):
     File "<python-input-19>", line 6, in <module>
       1/0
       ~^~
   ZeroDivisionError: division by zero

   >>> TracebackException.from_exception(chained_exc).print(chain=False)
   Traceback (most recent call last):
     File "<python-input-19>", line 6, in <module>
       1/0
       ~^~
   ZeroDivisionError: division by zero

