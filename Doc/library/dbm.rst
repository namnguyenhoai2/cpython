:mod:`!dbm` --- Giao diện với các "cơ sở dữ liệu" Unix
======================================================

.. module:: dbm
   :synopsis: Giao diện với nhiều định dạng "cơ sở dữ liệu" Unix khác nhau.

**Mã nguồn:** :source:`Lib/dbm/__init__.py`

--------------

:mod:`!dbm` là giao diện chung cho các biến thể của cơ sở dữ liệu DBM:

* :mod:`dbm.sqlite3`
* :mod:`dbm.gnu`
* :mod:`dbm.ndbm`

Nếu không có module nào trong số này được cài đặt, triển khai đơn giản nhưng chậm trong module :mod:`dbm.dumb` sẽ được sử dụng. Có một `giao diện của bên thứ ba <https://www.jcea.es/programacion/pybsddb.htm>`_ cho Oracle Berkeley DB.

.. exception:: error

   Một tuple chứa các ngoại lệ có thể được đưa ra bởi từng module được hỗ trợ, với một ngoại lệ duy nhất cũng có tên là :exc:`dbm.error` ở vị trí đầu tiên --- ngoại lệ sau được sử dụng khi :exc:`dbm.error` được đưa ra.


.. function:: whichdb(filename)

   Hàm này cố gắng đoán xem nên sử dụng module cơ sở dữ liệu đơn giản nào trong số các module hiện có --- :mod:`dbm.sqlite3`, :mod:`dbm.gnu`, :mod:`dbm.ndbm` hoặc :mod:`dbm.dumb` --- để mở một tệp cụ thể.

   Trả về một trong các giá trị sau:

   * ``None`` nếu không thể mở tệp vì tệp không thể đọc được hoặc không tồn tại
   * chuỗi rỗng (``''``) nếu không thể xác định định dạng của tệp
   * một chuỗi chứa tên module bắt buộc, chẳng hạn như ``'dbm.ndbm'`` hoặc ``'dbm.gnu'``

   .. versionchanged:: 3.11
      *filename* chấp nhận một :term:`path-like object`.

.. Substitutions for the open() flag param docs;
   all submodules use the same text.

.. |flag_r| replace::Mở cơ sở dữ liệu hiện có chỉ để đọc.

.. |flag_w| replace::Mở cơ sở dữ liệu hiện có để đọc và ghi.

.. |flag_c| replace::Mở cơ sở dữ liệu để đọc và ghi, đồng thời tạo cơ sở dữ liệu nếu cơ sở dữ liệu đó chưa tồn tại.

.. |flag_n| replace::Luôn tạo một cơ sở dữ liệu mới, rỗng, để đọc và ghi.

.. |mode_param_doc| replace::Chế độ truy cập tệp Unix của tệp (mặc định: bát phân ``0o666``), chỉ được sử dụng khi cần tạo cơ sở dữ liệu.

.. function:: open(file, flag='r', mode=0o666)

   Mở một cơ sở dữ liệu và trả về đối tượng cơ sở dữ liệu tương ứng.

   :param file:Tệp cơ sở dữ liệu cần mở.

      Nếu tệp cơ sở dữ liệu đã tồn tại, hàm :func:`whichdb` được sử dụng để xác định loại của tệp và module thích hợp sẽ được sử dụng; nếu tệp chưa tồn tại, submodule đầu tiên được liệt kê ở trên có thể được import sẽ được sử dụng.
   :type file: :term:`path-like object`

   :param str flag:
      * ``'r'`` (mặc định): |flag_r|
      * ``'w'``: |flag_w|
      * ``'c'``: |flag_c|
      * ``'n'``: |flag_n|

   :param int mode:
      |mode_param_doc|

   .. versionchanged:: 3.11
      *tệp* chấp nhận một :term:`path-like object`.

Đối tượng được :func:`~dbm.open` trả về hỗ trợ chức năng cơ bản của các :term:`ánh xạ <mapping>` có thể thay đổi; các khóa và giá trị tương ứng có thể được lưu trữ, truy xuất và xóa, đồng thời hỗ trợ phép lặp, toán tử :keyword:`in` và các phương thức :meth:`!keys`,
:meth:`!get`, :meth:`!setdefault` và :meth:`!clear` đều khả dụng. Phương thức :meth:`!keys` trả về một danh sách thay vì một đối tượng view. Phương thức :meth:`!setdefault` yêu cầu hai đối số.

Khóa và giá trị luôn được lưu trữ dưới dạng :class:`bytes`. Điều này có nghĩa là khi sử dụng chuỗi, chúng sẽ được chuyển đổi ngầm sang encoding mặc định trước khi được lưu trữ.

Các đối tượng này cũng hỗ trợ được sử dụng trong câu lệnh :keyword:`with`, câu lệnh này sẽ tự động đóng chúng khi hoàn tất.

.. versionchanged:: 3.2
   :meth:`!get` and :meth:`!setdefault` methods are now available for all
   :mod:`!dbm` backends.

.. versionchanged:: 3.4
   Đã bổ sung hỗ trợ gốc cho context management protocol đối với các đối tượng được :func:`~dbm.open` trả về.

.. versionchanged:: 3.8
   Việc xóa một khóa khỏi cơ sở dữ liệu chỉ đọc sẽ phát sinh ngoại lệ dành riêng cho module cơ sở dữ liệu thay vì :exc:`KeyError`.

.. versionchanged:: 3.13
   :meth:`!clear` methods are now available for all :mod:`!dbm` backends.


Ví dụ sau ghi lại một số hostname cùng với tiêu đề tương ứng, rồi in nội dung của cơ sở dữ liệu::

   import dbm

   # Mở cơ sở dữ liệu, tạo cơ sở dữ liệu nếu cần.
   with dbm.open('cache', 'c') as db:

       # Ghi lại một số giá trị
       db[b'hello'] = b'there'
       db['www.python.org'] = 'Python Website'
       db['www.cnn.com'] = 'Cable News Network'

       # Lưu ý rằng các khóa hiện được coi là byte.
       assert db[b'www.python.org'] == b'Python Website'
       # Hãy chú ý rằng giá trị hiện ở dạng byte.
       assert db['www.cnn.com'] == b'Cable News Network'

       # Các phương thức thường dùng của dict interface cũng hoạt động.
       print(db.get('python.org', b'not present'))

       # Lưu trữ khóa hoặc giá trị không phải chuỗi sẽ gây ra một ngoại lệ (hầu hết
       # có thể là một TypeError).
       db['www.yahoo.com'] = 4

   # db được tự động đóng khi thoát khỏi câu lệnh with.


.. seealso::

   Mô-đun :mod:`shelve`
      Mô-đun persistence lưu trữ dữ liệu không phải chuỗi.


Các submodule riêng lẻ được mô tả trong các phần sau.

:mod:`!dbm.sqlite3` --- Backend SQLite cho dbm
----------------------------------------------

.. module:: dbm.sqlite3
   :synopsis: Backend SQLite cho dbm

.. versionadded:: 3.13

**Mã nguồn:** :source:`Lib/dbm/sqlite3.py`

--------------

Mô-đun này sử dụng mô-đun :mod:`sqlite3` trong thư viện chuẩn để cung cấp backend SQLite cho mô-đun :mod:`!dbm`. Do đó, các tệp được tạo bởi :mod:`!dbm.sqlite3` có thể được mở bằng :mod:`sqlite3` hoặc bất kỳ trình duyệt SQLite nào khác, bao gồm cả SQLite CLI.

.. include:: ../includes/wasm-notavail.rst

.. function:: open(filename, /, flag="r", mode=0o666)

   Mở cơ sở dữ liệu SQLite.

   :param filename:Đường dẫn đến cơ sở dữ liệu cần mở.
   :type filename: :term:`path-like object`

   :param str flag:

      * ``'r'`` (mặc định): |flag_r|
      * ``'w'``: |flag_w|
      * ``'c'``: |flag_c|
      * ``'n'``: |flag_n|

   :param mode:Chế độ truy cập tệp Unix của tệp (mặc định: bát phân ``0o666``), chỉ được sử dụng khi cơ sở dữ liệu cần được tạo.

   Đối tượng cơ sở dữ liệu được trả về hoạt động tương tự như một :term:`mapping` có thể thay đổi, nhưng phương thức :meth:`!keys` trả về một danh sách và phương thức :meth:`!setdefault` yêu cầu hai đối số. Đối tượng này cũng hỗ trợ context manager "closing" thông qua từ khóa :keyword:`with`.

   Phương thức sau đây cũng được cung cấp:

   .. method:: sqlite3.close()

      Đóng cơ sở dữ liệu SQLite.


:mod:`!dbm.gnu` --- Trình quản lý cơ sở dữ liệu GNU
---------------------------------------------------

.. module:: dbm.gnu
   :synopsis: Trình quản lý cơ sở dữ liệu GNU

**Mã nguồn:** :source:`Lib/dbm/gnu.py`

--------------

Mô-đun :mod:`!dbm.gnu` cung cấp giao diện cho thư viện :abbr:`GDBM (GNU dbm)`, tương tự mô-đun :mod:`dbm.ndbm`, nhưng có thêm các chức năng như khả năng chịu lỗi khi gặp sự cố.

.. note::

   Các định dạng tệp được tạo bởi :mod:`!dbm.gnu` và :mod:`dbm.ndbm` không tương thích và không thể sử dụng thay thế cho nhau.

.. include:: ../includes/wasm-mobile-notavail.rst

.. availability:: Unix.

.. exception:: error

   Được nêu ra khi xảy ra các lỗi cụ thể của :mod:`!dbm.gnu`, chẳng hạn như lỗi I/O. :exc:`KeyError` được nêu ra cho các lỗi ánh xạ chung, chẳng hạn như chỉ định một khóa không chính xác.


.. data:: open_flags

   Một chuỗi ký tự được tham số *flag* của :meth:`~dbm.gnu.open` hỗ trợ.


.. function:: open(filename, flag="r", mode=0o666, /)

   Mở cơ sở dữ liệu GDBM và trả về một đối tượng :class:`!gdbm`.

   :param filename:Tệp cơ sở dữ liệu cần mở.
   :type filename: :term:`path-like object`

   :param str flag:
      * ``'r'`` (mặc định): |flag_r|
      * ``'w'``: |flag_w|
      * ``'c'``: |flag_c|
      * ``'n'``: |flag_n|

      Có thể nối thêm các ký tự bổ sung sau đây để kiểm soát cách mở cơ sở dữ liệu:

      * ``'f'``: Mở cơ sở dữ liệu ở chế độ nhanh. Các thao tác ghi vào cơ sở dữ liệu sẽ không được đồng bộ hóa.
      * ``'s'``: Chế độ đồng bộ. Các thay đổi đối với cơ sở dữ liệu sẽ được ghi ngay vào tệp.
      * ``'u'``: Không khóa cơ sở dữ liệu.

      Không phải mọi cờ đều hợp lệ đối với tất cả các phiên bản của GDBM. Xem thành viên :data:`open_flags` để biết danh sách các ký tự cờ được hỗ trợ.

   :param int mode:
      |mode_param_doc|

   :raises error:Khi truyền một đối số *flag* không hợp lệ.

   .. versionchanged:: 3.11
      *filename* chấp nhận một :term:`path-like object`.

   Các đối tượng :class:`!gdbm` hoạt động tương tự như các :term:`ánh xạ có thể thay đổi <mapping>`, nhưng các phương thức :meth:`!items`, :meth:`!values`, :meth:`!pop`, :meth:`!popitem` và :meth:`!update` không được hỗ trợ, phương thức :meth:`!keys` trả về một danh sách, và phương thức :meth:`!setdefault` yêu cầu hai đối số. Nó cũng hỗ trợ một context manager "closing" thông qua từ khóa :keyword:`with`.

   .. versionchanged:: 3.2
      Đã bổ sung các phương thức :meth:`!get` và :meth:`!setdefault`.

   .. versionchanged:: 3.13
      Đã thêm phương thức :meth:`!clear`.

   Các phương thức sau cũng được cung cấp:

   .. method:: gdbm.close()

      Đóng cơ sở dữ liệu GDBM.

   .. method:: gdbm.firstkey()

      Bạn có thể dùng phương thức này và phương thức
      :meth:`nextkey` để lặp qua mọi khóa trong cơ sở dữ liệu. Việc duyệt được sắp xếp theo các giá trị băm nội bộ của GDBM và sẽ không được sắp xếp theo giá trị khóa. Phương thức này trả về khóa bắt đầu.

   .. method:: gdbm.nextkey(key)

      Trả về khóa đứng sau *key* trong quá trình duyệt. Đoạn mã sau in mọi khóa trong cơ sở dữ liệu ``db``, mà không cần tạo một danh sách trong bộ nhớ chứa tất cả các khóa đó::

         k = db.firstkey()
         while k is not None:
             print(k)
             k = db.nextkey(k)

   .. method:: gdbm.reorganize()

      Nếu bạn đã thực hiện nhiều thao tác xóa và muốn thu nhỏ dung lượng mà tệp GDBM sử dụng, thủ tục này sẽ tổ chức lại cơ sở dữ liệu. Các đối tượng :class:`!gdbm` sẽ không làm giảm độ dài của tệp cơ sở dữ liệu, ngoại trừ bằng cách sử dụng thao tác tổ chức lại này; nếu không, dung lượng tệp đã xóa sẽ được giữ lại và tái sử dụng khi các cặp (khóa, giá trị) mới được thêm vào.

   .. method:: gdbm.sync()

      Khi cơ sở dữ liệu được mở ở chế độ nhanh, phương thức này buộc mọi dữ liệu chưa được ghi phải được ghi vào đĩa.


:mod:`!dbm.ndbm` --- Trình quản lý cơ sở dữ liệu mới
----------------------------------------------------

.. module:: dbm.ndbm
   :synopsis: Trình quản lý cơ sở dữ liệu mới

**Mã nguồn:** :source:`Lib/dbm/ndbm.py`

--------------

Mô-đun :mod:`!dbm.ndbm` cung cấp giao diện cho
:abbr:`NDBM (thư viện Trình quản lý cơ sở dữ liệu mới)`. Mô-đun này có thể được sử dụng với giao diện NDBM "cổ điển" hoặc
giao diện tương thích với :abbr:`GDBM (GNU dbm)`.

.. note::

   Các định dạng tệp được tạo bởi :mod:`dbm.gnu` và :mod:`!dbm.ndbm` không tương thích và không thể sử dụng thay thế cho nhau.

.. warning::

   Thư viện NDBM đi kèm với macOS có một giới hạn không được ghi nhận trong tài liệu về kích thước của các giá trị, điều này có thể khiến các tệp cơ sở dữ liệu bị hỏng khi lưu trữ các giá trị lớn hơn giới hạn này. Việc đọc các tệp bị hỏng như vậy có thể dẫn đến lỗi nghiêm trọng (segmentation fault).

.. include:: ../includes/wasm-mobile-notavail.rst

.. availability:: Unix.

.. exception:: error

   Được phát sinh khi xảy ra các lỗi đặc thù của :mod:`!dbm.ndbm`, chẳng hạn như lỗi I/O. :exc:`KeyError` được phát sinh đối với các lỗi ánh xạ chung, chẳng hạn như chỉ định một khóa không chính xác.


.. data:: library

   Tên của thư viện triển khai NDBM được sử dụng.


.. function:: open(filename, flag="r", mode=0o666, /)

   Mở một cơ sở dữ liệu NDBM và trả về một đối tượng :class:`!ndbm`.

   :param filename:Tên cơ sở của tệp cơ sở dữ liệu (không có phần mở rộng :file:`.dir` hoặc :file:`.pag`).
   :type filename: :term:`path-like object`

   :param str flag:
      * ``'r'`` (mặc định): |flag_r|
      * ``'w'``: |flag_w|
      * ``'c'``: |flag_c|
      * ``'n'``: |flag_n|

   :param int mode:
      |mode_param_doc|

   .. versionchanged:: 3.11
      Chấp nhận :term:`path-like object` làm tên tệp.

   Các đối tượng :class:`!ndbm` hoạt động tương tự như các :term:`ánh xạ <mapping>` có thể thay đổi, nhưng các phương thức :meth:`!items`, :meth:`!values`, :meth:`!pop`, :meth:`!popitem` và :meth:`!update` không được hỗ trợ, phương thức :meth:`!keys` trả về một danh sách, còn phương thức :meth:`!setdefault` yêu cầu hai đối số. Đối tượng này cũng hỗ trợ context manager "closing" thông qua từ khóa :keyword:`with`.

   .. versionchanged:: 3.2
      Đã thêm các phương thức :meth:`!get` và :meth:`!setdefault`.

   .. versionchanged:: 3.13
      Đã thêm phương thức :meth:`!clear`.

   Phương thức sau đây cũng được cung cấp:

   .. method:: ndbm.close()

      Đóng cơ sở dữ liệu NDBM.


:mod:`!dbm.dumb` --- Triển khai DBM khả chuyển
----------------------------------------------

.. module:: dbm.dumb
   :synopsis: Bản triển khai portable của giao diện DBM đơn giản.

**Mã nguồn:** :source:`Lib/dbm/dumb.py`

.. index:: single: databases

.. note::

   Mô-đun :mod:`!dbm.dumb` được dùng như một phương án dự phòng cuối cùng cho
   mô-đun :mod:`!dbm` khi không có mô-đun mạnh mẽ hơn. Mô-đun :mod:`!dbm.dumb` không được viết để đạt tốc độ cao và cũng không được sử dụng rộng rãi như các mô-đun cơ sở dữ liệu khác.

--------------

Mô-đun :mod:`!dbm.dumb` cung cấp một giao diện kiểu :class:`dict` có khả năng lưu trữ bền vững, được viết hoàn toàn bằng Python. Không giống các backend :mod:`!dbm` khác, chẳng hạn như :mod:`dbm.gnu`, mô-đun này không yêu cầu thư viện bên ngoài.

Mô-đun :mod:`!dbm.dumb` định nghĩa các thành phần sau:

.. exception:: error

   Được phát sinh khi xảy ra các lỗi đặc thù của :mod:`!dbm.dumb`, chẳng hạn như lỗi I/O. :exc:`KeyError` được phát sinh đối với các lỗi ánh xạ nói chung, chẳng hạn như chỉ định một khóa không đúng.


.. function:: open(filename, flag="c", mode=0o666)

   Mở một cơ sở dữ liệu :mod:`!dbm.dumb`.

   :param filename:Tên cơ sở của tệp cơ sở dữ liệu (không có phần mở rộng). Một cơ sở dữ liệu mới sẽ tạo các tệp sau:

      - :file:`{filename}.dat`
      - :file:`{filename}.dir`
   :type database: :term:`path-like object`

   :param str flag:
      * ``'r'``: |flag_r|
      * ``'w'``: |flag_w|
      * ``'c'`` (mặc định): |flag_c|
      * ``'n'``: |flag_n|

   :param int mode:
      |mode_param_doc|

   .. warning::
      Có thể làm trình thông dịch Python gặp sự cố khi tải một cơ sở dữ liệu có mục nhập đủ lớn/phức tạp do các giới hạn về độ sâu ngăn xếp trong trình biên dịch AST của Python.

   .. versionchanged:: 3.5
      :func:`~dbm.dumb.open` always creates a new database when *flag* is ``'n'``.

   .. versionchanged:: 3.8
      Cơ sở dữ liệu được mở ở chế độ chỉ đọc nếu *flag* là ``'r'``. Cơ sở dữ liệu sẽ không được tạo nếu chưa tồn tại nếu *flag* là ``'r'`` hoặc ``'w'``.

   .. versionchanged:: 3.11
      *filename* chấp nhận một :term:`path-like object`.

   Đối tượng cơ sở dữ liệu được trả về hoạt động tương tự như một :term:`mapping` có thể thay đổi, nhưng các phương thức :meth:`!keys` và :meth:`!items` trả về danh sách, còn phương thức :meth:`!setdefault` yêu cầu hai đối số. Đối tượng này cũng hỗ trợ trình quản lý ngữ cảnh "closing" thông qua từ khóa :keyword:`with`.

   Các phương thức sau cũng được cung cấp:

   .. method:: dumbdbm.close()

      Đóng cơ sở dữ liệu.

   .. method:: dumbdbm.sync()

      Đồng bộ hóa thư mục và các tệp dữ liệu trên đĩa. Phương thức này được gọi bởi phương thức :meth:`shelve.Shelf.sync`.

.. _`third party interface`: https://www.jcea.es/programacion/pybsddb.htm
