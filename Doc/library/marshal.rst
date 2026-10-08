:mod:`!marshal` --- Tuần tự hóa đối tượng Python nội bộ
=======================================================

.. module:: marshal
   :synopsis: Chuyển đổi các đối tượng Python thành các luồng byte và ngược lại (với những ràng buộc khác nhau).

--------------

Module này chứa các hàm có thể đọc và ghi các giá trị Python ở định dạng nhị phân. Định dạng này dành riêng cho Python nhưng không phụ thuộc vào các vấn đề về kiến trúc máy (ví dụ: bạn có thể ghi một giá trị Python vào tệp trên PC, chuyển tệp đó sang máy Mac và đọc lại ở đó). Chi tiết về định dạng được cố ý không ghi thành tài liệu; định dạng có thể thay đổi giữa các phiên bản Python (mặc dù điều này hiếm khi xảy ra). [#]_

.. index::
   pair: module; pickle
   pair: module; shelve

Đây không phải là module "lưu trữ" đa dụng. Để lưu trữ và truyền các đối tượng Python qua các cuộc gọi RPC nói chung, hãy xem các module :mod:`pickle` và
:mod:`shelve`. Module :mod:`!marshal` chủ yếu tồn tại để hỗ trợ đọc và ghi mã "giả biên dịch" cho các module Python từ các tệp :file:`.pyc`. Vì vậy, các nhà bảo trì Python bảo lưu quyền sửa đổi định dạng marshal theo những cách không tương thích ngược nếu cần. Định dạng của các đối tượng mã không tương thích giữa các phiên bản Python, ngay cả khi phiên bản của định dạng là như nhau. Việc giải tuần tự hóa một đối tượng mã bằng sai phiên bản Python sẽ có hành vi không xác định. Nếu bạn đang tuần tự hóa và giải tuần tự hóa các đối tượng Python, hãy sử dụng module :mod:`pickle` thay thế -- hiệu năng tương đương, đảm bảo tính độc lập giữa các phiên bản, và pickle hỗ trợ phạm vi đối tượng rộng hơn đáng kể so với marshal.

.. warning::

   Module :mod:`!marshal` không được thiết kế để bảo mật trước dữ liệu sai hoặc được tạo một cách độc hại. Không bao giờ giải tuần tự hóa dữ liệu nhận được từ một nguồn không đáng tin cậy hoặc chưa được xác thực.

Có các hàm đọc/ghi tệp cũng như các hàm hoạt động trên các đối tượng giống byte.

.. index:: object; code, code object

Không phải mọi kiểu đối tượng Python đều được hỗ trợ; nhìn chung, chỉ những đối tượng có giá trị độc lập với một lần gọi Python cụ thể mới có thể được ghi và đọc bởi module này. Các kiểu sau được hỗ trợ:

* Các kiểu số: :class:`int`, :class:`bool`, :class:`float`, :class:`complex`.
* Chuỗi (:class:`str`) và :class:`bytes`.
  :term:`Các đối tượng dạng byte <bytes-like object>` như :class:`bytearray` được marshal dưới dạng :class:`!bytes`.
* Các container: :class:`tuple`, :class:`list`, :class:`set`, :class:`frozenset`, và (kể từ :data:`version` 5), :class:`slice`. Cần hiểu rằng các container này chỉ được hỗ trợ nếu bản thân các giá trị chứa bên trong cũng được hỗ trợ. Các container đệ quy được hỗ trợ kể từ :data:`version` 3.
* Các singleton :const:`None`, :const:`Ellipsis` và :exc:`StopIteration`.
* :class:`code` các đối tượng, nếu *allow_code* là true. Xem lưu ý ở trên về sự phụ thuộc vào phiên bản.

.. versionchanged:: 3.4

   * Đã thêm phiên bản định dạng 3, hỗ trợ marshalling các list, set và dictionary đệ quy.
   * Đã thêm phiên bản định dạng 4, hỗ trợ các biểu diễn hiệu quả cho chuỗi ngắn.

.. versionchanged:: 3.14

   Đã thêm phiên bản định dạng 5, cho phép marshalling các slice.


Module định nghĩa các hàm sau:


.. function:: dump(value, file, version=version, /, *, allow_code=True)

   Ghi giá trị vào file đang mở. Giá trị phải thuộc một kiểu được hỗ trợ. File phải là một :term:`binary file` có thể ghi.

   Nếu giá trị có (hoặc chứa một đối tượng có) kiểu không được hỗ trợ, một
   ngoại lệ :exc:`ValueError` sẽ được phát sinh --- nhưng dữ liệu rác cũng sẽ được ghi vào file. Đối tượng sẽ không được :func:`load` đọc lại đúng cách.
   :ref:`Các đối tượng code <code-objects>` chỉ được hỗ trợ nếu *allow_code* là true.

   Đối số *version* cho biết định dạng dữ liệu mà ``dump`` nên sử dụng (xem bên dưới).

   .. audit-event:: marshal.dumps value,version marshal.dump

   .. versionchanged:: 3.13
      Đã thêm tham số *allow_code*.


.. function:: load(file, /, *, allow_code=True)

   Đọc một giá trị từ tệp đang mở và trả về giá trị đó. Nếu không đọc được giá trị hợp lệ nào (ví dụ: vì dữ liệu có định dạng marshal không tương thích của một phiên bản Python khác), hãy phát sinh :exc:`EOFError`, :exc:`ValueError` hoặc :exc:`TypeError`.
   :ref:`Các đối tượng code <code-objects>` chỉ được hỗ trợ nếu *allow_code* là true. Tệp phải là một :term:`binary file` có thể đọc được.

   .. audit-event:: marshal.load "" marshal.load

   .. note::

      Nếu một đối tượng chứa kiểu không được hỗ trợ được marshal bằng :func:`dump`,
      :func:`load` sẽ thay thế ``None`` cho kiểu không thể unmarshall.

   .. versionchanged:: 3.10

      Lệnh gọi này trước đây phát sinh một sự kiện audit ``code.__new__`` cho mỗi đối tượng mã. Hiện tại, lệnh gọi này phát sinh một sự kiện ``marshal.load`` duy nhất cho toàn bộ thao tác tải.

   .. versionchanged:: 3.13
      Đã thêm tham số *allow_code*.


.. function:: dumps(value, version=version, /, *, allow_code=True)

   Trả về đối tượng bytes sẽ được ghi vào tệp bởi ``dump(value, file)``. Giá trị phải thuộc một kiểu được hỗ trợ. Phát sinh ngoại lệ :exc:`ValueError` nếu value có (hoặc chứa một đối tượng có) kiểu không được hỗ trợ.
   :ref:`Các đối tượng code <code-objects>` chỉ được hỗ trợ nếu *allow_code* là true.

   Đối số *version* cho biết định dạng dữ liệu mà ``dumps`` sẽ sử dụng (xem bên dưới).

   .. audit-event:: marshal.dumps value,version marshal.dump

   .. versionchanged:: 3.13
      Đã thêm tham số *allow_code*.


.. function:: loads(bytes, /, *, allow_code=True)

   Chuyển đổi :term:`bytes-like object` thành một giá trị. Nếu không tìm thấy giá trị hợp lệ, hãy phát sinh
   :exc:`EOFError`, :exc:`ValueError` hoặc :exc:`TypeError`.
   :ref:`Các đối tượng mã <code-objects>` chỉ được hỗ trợ nếu *allow_code* là true. Các byte bổ sung trong dữ liệu đầu vào sẽ bị bỏ qua.

   .. audit-event:: marshal.loads bytes marshal.load

   .. versionchanged:: 3.10

      Trước đây, lệnh gọi này phát sinh một sự kiện kiểm tra ``code.__new__`` cho mỗi đối tượng mã. Hiện tại, lệnh gọi này chỉ phát sinh một sự kiện ``marshal.loads`` duy nhất cho toàn bộ thao tác tải.

   .. versionchanged:: 3.13
      Đã thêm tham số *allow_code*.


Ngoài ra, các hằng số sau đây được định nghĩa:

.. data:: version

   Cho biết định dạng mà module sử dụng. Phiên bản 0 là phiên bản đầu tiên trong lịch sử; các phiên bản tiếp theo bổ sung những tính năng mới. Nhìn chung, một phiên bản mới sẽ trở thành mặc định khi được giới thiệu.

   +-----------+-----------------+-----------------------------------------+
   | Phiên bản | Có từ phiên bản | Tính năng mới                           |
   +===========+=================+=========================================+
   | 1         | Python 2.4      | Chia sẻ các chuỗi interned              |
   +-----------+-----------------+-----------------------------------------+
   | 2         | Python 2.5      | Biểu diễn nhị phân của số thực          |
   +-----------+-----------------+-----------------------------------------+
   | 3         | Python 3.4      | Hỗ trợ tạo instance đối tượng và đệ quy |
   +-----------+-----------------+-----------------------------------------+
   | 4         | Python 3.4      | Biểu diễn hiệu quả các chuỗi ngắn       |
   +-----------+-----------------+-----------------------------------------+
   | 5         | Python 3.14     | Hỗ trợ các đối tượng :class:`slice`     |
   +-----------+-----------------+-----------------------------------------+


.. rubric:: Chú thích

.. [#] Tên của module này bắt nguồn từ một thuật ngữ được các nhà thiết kế Modula-3 (cùng những người khác) sử dụng: họ dùng thuật ngữ "marshalling" để chỉ việc truyền dữ liệu dưới dạng khép kín. Nói chính xác, "to marshal" có nghĩa là chuyển đổi dữ liệu từ dạng nội bộ sang dạng bên ngoài (chẳng hạn trong một bộ đệm RPC), còn "unmarshalling" là quá trình ngược lại.
