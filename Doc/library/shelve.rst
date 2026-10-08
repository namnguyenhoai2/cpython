:mod:`!shelve` --- Lưu trữ đối tượng Python
===========================================

.. module:: shelve
   :synopsis: Lưu trữ đối tượng Python.

**Mã nguồn:** :source:`Lib/shelve.py`

.. index:: pair: module; pickle

--------------

“Shelf” là một đối tượng giống dictionary có khả năng lưu trữ bền vững. Điểm khác biệt so với các cơ sở dữ liệu “dbm” là các giá trị (không phải các khóa!) trong shelf về cơ bản có thể là những đối tượng Python tùy ý --- bất kỳ đối tượng nào mà module :mod:`pickle` có thể xử lý. Điều này bao gồm hầu hết các thể hiện lớp, các kiểu dữ liệu đệ quy và các đối tượng chứa nhiều đối tượng con được dùng chung. Các khóa là những chuỗi thông thường.


.. function:: open(filename, flag='c', protocol=None, writeback=False)

   Mở một dictionary có khả năng lưu trữ bền vững. Tên tệp được chỉ định là tên tệp cơ sở cho cơ sở dữ liệu bên dưới. Do tác dụng phụ, một phần mở rộng có thể được thêm vào tên tệp và có thể tạo nhiều hơn một tệp. Theo mặc định, tệp cơ sở dữ liệu bên dưới được mở để đọc và ghi. Tham số tùy chọn *flag* có cùng cách diễn giải với tham số *flag* của :func:`dbm.open`.

   Theo mặc định, các pickle được tạo bằng :const:`pickle.DEFAULT_PROTOCOL` sẽ được dùng để tuần tự hóa các giá trị. Có thể chỉ định phiên bản của giao thức pickle bằng tham số *protocol*.

   Do ngữ nghĩa của Python, shelf không thể biết khi nào một mục từ điển bền vững có thể thay đổi bị sửa đổi. Theo mặc định, các đối tượng đã sửa đổi *chỉ* được ghi khi được gán vào shelf (xem :ref:`shelve-example`). Nếu tham số tùy chọn *writeback* được đặt thành ``True``, tất cả các mục đã truy cập cũng được lưu vào bộ nhớ đệm và được ghi trở lại khi :meth:`~Shelf.sync` và
   :meth:`~Shelf.close`; điều này có thể giúp việc thay đổi các mục có thể thay đổi trong persistent dictionary thuận tiện hơn, nhưng nếu truy cập nhiều mục, nó có thể tiêu tốn lượng bộ nhớ khổng lồ cho cache, đồng thời khiến thao tác đóng trở nên rất chậm vì tất cả các mục đã truy cập đều được ghi trở lại (không có cách nào xác định mục nào trong số các mục đã truy cập là có thể thay đổi, cũng như mục nào thực sự đã bị thay đổi).

   .. versionchanged:: 3.10
      :const:`pickle.DEFAULT_PROTOCOL` is now used as the default pickle
      giao thức.

   .. versionchanged:: 3.11
      Chấp nhận :term:`path-like object` cho filename.

   .. note::

      Không nên dựa vào việc shelf sẽ tự động được đóng; hãy luôn gọi
      :meth:`~Shelf.close` một cách rõ ràng khi bạn không còn cần đến nó nữa, hoặc sử dụng :func:`shelve.open` làm context manager::

          with shelve.open('spam') as db:
              db['eggs'] = 'eggs'

.. _shelve-security:

.. warning::

   Vì module :mod:`!shelve` được xây dựng trên :mod:`pickle`, việc tải shelf từ một nguồn không đáng tin cậy là không an toàn. Giống như với pickle, việc tải shelf có thể thực thi mã tùy ý.

Các đối tượng Shelf hỗ trợ hầu hết các phương thức và thao tác được dictionary hỗ trợ (ngoại trừ việc sao chép, các hàm tạo và các toán tử ``|`` và ``|=``). Điều này giúp quá trình chuyển đổi từ các script dựa trên dictionary sang những script yêu cầu lưu trữ bền vững trở nên dễ dàng hơn.

Hai phương thức bổ sung được hỗ trợ:

.. method:: Shelf.sync()

   Ghi lại tất cả các mục trong cache nếu shelf được mở với *writeback* được đặt thành :const:`True`. Đồng thời xóa cache và đồng bộ từ điển persistent trên đĩa, nếu có thể. Việc này được tự động thực hiện khi shelf được đóng bằng :meth:`close`.

.. method:: Shelf.close()

   Đồng bộ và đóng đối tượng *dict* persistent. Các thao tác trên shelf đã đóng sẽ thất bại với một :exc:`ValueError`.


.. seealso::

   `Công thức từ điển persistent <https://code.activestate.com/recipes/576642-persistent-dict-with-multiple-standard-file-format/>`_ với các định dạng lưu trữ được hỗ trợ rộng rãi và tốc độ tương đương từ điển native.


Các hạn chế
-----------

.. index::
   pair: module; dbm.ndbm
   pair: module; dbm.gnu

* Việc chọn gói cơ sở dữ liệu nào sẽ được sử dụng (chẳng hạn như :mod:`dbm.ndbm` hoặc
  :mod:`dbm.gnu`) phụ thuộc vào interface nào khả dụng. Vì vậy, không an toàn khi mở cơ sở dữ liệu trực tiếp bằng :mod:`dbm`. Cơ sở dữ liệu cũng (không may) chịu các hạn chế của :mod:`dbm`, nếu được sử dụng --- điều này có nghĩa là biểu diễn (đã pickle) của các đối tượng được lưu trong cơ sở dữ liệu nên khá nhỏ, và trong một số trường hợp hiếm gặp, các va chạm khóa có thể khiến cơ sở dữ liệu từ chối cập nhật.

* Mô-đun :mod:`!shelve` không hỗ trợ quyền truy cập đọc/ghi *đồng thời* vào các đối tượng được lưu trong shelf. (Nhiều quyền truy cập đọc đồng thời là an toàn.) Khi một chương trình đang mở một shelf để ghi, không chương trình nào khác được mở shelf đó để đọc hoặc ghi. Có thể sử dụng khóa tệp Unix để giải quyết vấn đề này, nhưng cách này khác nhau giữa các phiên bản Unix và yêu cầu hiểu biết về phần triển khai cơ sở dữ liệu được sử dụng.

* Trên macOS, :mod:`dbm.ndbm` có thể âm thầm làm hỏng tệp cơ sở dữ liệu khi cập nhật, điều này có thể gây ra lỗi nghiêm trọng khi cố đọc từ cơ sở dữ liệu.


.. class:: Shelf(dict, protocol=None, writeback=False, keyencoding='utf-8')

   Một lớp con của :class:`collections.abc.MutableMapping` dùng để lưu các giá trị đã pickle trong đối tượng *dict*.

   Theo mặc định, các pickle được tạo bằng :const:`pickle.DEFAULT_PROTOCOL` được dùng để tuần tự hóa các giá trị. Có thể chỉ định phiên bản của giao thức pickle bằng tham số *protocol*. Xem tài liệu :mod:`pickle` để biết thông tin về các giao thức pickle.

   Nếu tham số *writeback* là ``True``, đối tượng sẽ lưu bộ nhớ đệm chứa tất cả các mục đã truy cập và ghi chúng trở lại *dict* khi đồng bộ hóa và đóng. Điều này cho phép thực hiện các thao tác tự nhiên trên các mục có thể thay đổi, nhưng có thể tiêu tốn nhiều bộ nhớ hơn đáng kể và khiến việc đồng bộ hóa và đóng mất nhiều thời gian.

   Tham số *keyencoding* là encoding được dùng để mã hóa các khóa trước khi sử dụng chúng với dict bên dưới.

   Một đối tượng :class:`Shelf` cũng có thể được sử dụng như một context manager; trong trường hợp đó, đối tượng sẽ tự động được đóng khi khối :keyword:`with` kết thúc.

   .. versionchanged:: 3.2
      Đã thêm tham số *keyencoding*; trước đây, các khóa luôn được mã hóa bằng UTF-8.

   .. versionchanged:: 3.4
      Đã thêm hỗ trợ context manager.

   .. versionchanged:: 3.10
      :const:`pickle.DEFAULT_PROTOCOL` is now used as the default pickle
      giao thức.


.. class:: BsdDbShelf(dict, protocol=None, writeback=False, keyencoding='utf-8')

   Một lớp con của :class:`Shelf` cung cấp các phương thức :meth:`!first`, :meth:`!next`,
   :meth:`!previous`, :meth:`!last` và :meth:`!set_location`. Các phương thức này có trong mô-đun :mod:`!bsddb` bên thứ ba từ `pybsddb <https://www.jcea.es/programacion/pybsddb.htm>`_, nhưng không có trong các mô-đun cơ sở dữ liệu khác. Đối tượng *dict* được truyền vào hàm khởi tạo phải hỗ trợ các phương thức đó. Điều này thường được thực hiện bằng cách gọi một trong
   :func:`!bsddb.hashopen`, :func:`!bsddb.btopen` hoặc :func:`!bsddb.rnopen`. Các tham số tùy chọn *protocol*, *writeback* và *keyencoding* có cách diễn giải giống như đối với lớp :class:`Shelf`.


.. class:: DbfilenameShelf(filename, flag='c', protocol=None, writeback=False)

   Một lớp con của :class:`Shelf` chấp nhận *filename* thay vì một đối tượng giống dict. Tệp bên dưới sẽ được mở bằng :func:`dbm.open`. Theo mặc định, tệp sẽ được tạo và mở để đọc và ghi. Tham số tùy chọn *flag* có cách diễn giải giống như đối với hàm :func:`.open`. Các tham số tùy chọn *protocol* và *writeback* có cách diễn giải giống như đối với lớp :class:`Shelf`.


.. _shelve-example:

Ví dụ
-----

Tóm tắt interface (``key`` là một chuỗi, ``data`` là một đối tượng tùy ý)::

   import shelve

   d = shelve.open(filename)  # mở -- tệp có thể được tầng thấp thêm hậu tố
                              # thư viện

   d[key] = data              # lưu dữ liệu tại khóa (ghi đè dữ liệu cũ nếu
                              # sử dụng một khóa hiện có)
   data = d[key]              # lấy một BẢN SAO của dữ liệu tại khóa (phát sinh KeyError
                              # if no such key)
   del d[key]                 # xóa dữ liệu được lưu tại key (gây ra KeyError
                              # if no such key)

   flag = key in d            # true nếu key tồn tại
   klist = list(d.keys())     # danh sách tất cả các key hiện có (chậm!)

   # vì d được mở mà KHÔNG có writeback=True, hãy lưu ý:
   d['xx'] = [0, 1, 2]        # điều này hoạt động như mong đợi, nhưng...
   d['xx'].append(3)          # *điều này không hoạt động!* -- d['xx'] VẪN là [0, 1, 2]!

   # sau khi mở d mà không có writeback=True, bạn cần viết code cẩn thận:
   temp = d['xx']             # trích xuất bản sao
   temp.append(5)             # sửa đổi bản sao
   d['xx'] = temp             # lưu bản sao trở lại để duy trì các thay đổi

   # hoặc, d=shelve.open(filename,writeback=True) sẽ cho phép bạn chỉ cần viết mã
   # d['xx'].append(5) và nó sẽ hoạt động như mong đợi, NHƯNG nó cũng sẽ
   # tốn nhiều bộ nhớ hơn và khiến thao tác d.close() chậm hơn.

   d.close()                  # đóng nó


.. seealso::

   Mô-đun :mod:`dbm`
      Giao diện chung cho các cơ sở dữ liệu kiểu ``dbm``.

   Mô-đun :mod:`pickle`
      Tuần tự hóa đối tượng được :mod:`!shelve` sử dụng.

.. _`Persistent dictionary recipe`: https://code.activestate.com/recipes/576642-persistent-dict-with-multiple-standard-file-format/
.. _`pybsddb`: https://www.jcea.es/programacion/pybsddb.htm
