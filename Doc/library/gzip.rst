:mod:`!gzip` --- Hỗ trợ các tệp :program:`gzip`
===============================================

.. module:: gzip
   :synopsis: Các giao diện để nén và giải nén gzip bằng các đối tượng tệp.

**Mã nguồn:** :source:`Lib/gzip.py`

--------------

Mô-đun này cung cấp một giao diện đơn giản để nén và giải nén tệp, giống như các chương trình GNU :program:`gzip` và :program:`gunzip`.

.. include:: ../includes/optional-module.rst

Mô-đun :mod:`zlib` cung cấp chức năng nén dữ liệu.

Mô-đun :mod:`!gzip` cung cấp lớp :class:`GzipFile`, cùng với các
:func:`.open`, :func:`compress` và :func:`decompress` hàm tiện ích. Lớp :class:`GzipFile` đọc và ghi các tệp định dạng :program:`gzip`\ , tự động nén hoặc giải nén dữ liệu để dữ liệu trông giống như một :term:`file object` thông thường.

Lưu ý rằng các định dạng tệp bổ sung có thể được giải nén bằng các
:program:`gzip` và :program:`gunzip` chương trình, chẳng hạn như những chương trình được tạo bởi
:program:`compress` và :program:`pack`, không được mô-đun này hỗ trợ.

Mô-đun này định nghĩa các mục sau:


.. function:: open(filename, mode='rb', compresslevel=9, encoding=None, errors=None, newline=None)

   Mở một tệp được nén bằng gzip ở chế độ nhị phân hoặc văn bản, trả về một :term:`file object`.

   Đối số *filename* có thể là một tên tệp thực tế (một :class:`str` hoặc
   :class:`bytes` object), hoặc một đối tượng tệp hiện có để đọc hoặc ghi.

   Đối số *mode* có thể là bất kỳ giá trị nào trong số ``'r'``, ``'rb'``, ``'a'``, ``'ab'``, ``'w'``, ``'wb'``, ``'x'`` hoặc ``'xb'`` cho chế độ nhị phân, hoặc ``'rt'``, ``'at'``, ``'wt'`` hoặc ``'xt'`` cho chế độ văn bản. Giá trị mặc định là ``'rb'``.

   Đối số *compresslevel* là một số nguyên từ 0 đến 9, tương tự như
   hàm khởi tạo :class:`GzipFile`.

   Đối với chế độ nhị phân, hàm này tương đương với hàm khởi tạo :class:`GzipFile`: ``GzipFile(filename, mode, compresslevel)``. Trong trường hợp này, không được cung cấp các đối số *encoding*, *errors* và *newline*.

   Đối với chế độ văn bản, một đối tượng :class:`GzipFile` được tạo và bọc trong một
   :class:`io.TextIOWrapper` instance với encoding, cách xử lý lỗi và (các) ký tự kết thúc dòng được chỉ định.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ để *filename* là một đối tượng tệp, hỗ trợ chế độ văn bản và các đối số *encoding*, *errors* và *newline*.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các chế độ ``'x'``, ``'xb'`` và ``'xt'``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

.. exception:: BadGzipFile

   Một ngoại lệ được đưa ra khi tệp gzip không hợp lệ. Ngoại lệ này kế thừa từ :exc:`OSError`.
   :exc:`EOFError` và :exc:`zlib.error` cũng có thể được đưa ra khi tệp gzip không hợp lệ.

   .. versionadded:: 3.8

.. class:: GzipFile(filename=None, mode=None, compresslevel=9, fileobj=None, mtime=None)

   Hàm khởi tạo cho lớp :class:`GzipFile`, mô phỏng hầu hết các phương thức của một :term:`file object`, ngoại trừ phương thức :meth:`~io.IOBase.truncate`. Ít nhất một trong *fileobj* và *filename* phải được cung cấp một giá trị khác rỗng.

   Thể hiện lớp mới dựa trên *fileobj*, có thể là một tệp thông thường, một
   đối tượng :class:`io.BytesIO`, hoặc bất kỳ đối tượng nào khác mô phỏng một tệp. Mặc định là ``None``; trong trường hợp đó, *filename* được mở để cung cấp một đối tượng tệp.

   Khi *fileobj* không phải là ``None``, đối số *filename* chỉ được dùng để đưa vào phần đầu :program:`gzip` của tệp, phần này có thể chứa tên tệp gốc của tệp chưa nén. Theo mặc định, đối số này là tên tệp của *fileobj*, nếu có thể xác định được; nếu không, mặc định là chuỗi rỗng, và trong trường hợp này tên tệp gốc sẽ không được đưa vào phần đầu tệp.

   Đối số *mode* có thể là bất kỳ giá trị nào trong số ``'r'``, ``'rb'``, ``'a'``, ``'ab'``, ``'w'``, ``'wb'``, ``'x'`` hoặc ``'xb'``, tùy thuộc vào việc tệp sẽ được đọc hay ghi. Mặc định là mode của *fileobj* nếu có thể xác định được; nếu không, mặc định là ``'rb'``. Trong các bản phát hành Python sau này, mode của *fileobj* sẽ không được sử dụng. Tốt hơn hết là luôn chỉ định *mode* khi ghi.

   Lưu ý rằng tệp luôn được mở ở binary mode. Để mở tệp đã nén ở text mode, hãy dùng :func:`.open` (hoặc bọc :class:`GzipFile` của bạn bằng một
   :class:`io.TextIOWrapper`).

   Đối số *compresslevel* là một số nguyên từ ``0`` đến ``9``, dùng để điều khiển mức độ nén; ``1`` nhanh nhất và cho mức nén thấp nhất, còn ``9`` chậm nhất và cho mức nén cao nhất. ``0`` là không nén. Giá trị mặc định là ``9``.

   Đối số tùy chọn *mtime* là dấu thời gian được gzip yêu cầu. Thời gian được biểu diễn theo định dạng Unix, tức là số giây kể từ 00:00:00 UTC ngày 1 tháng 1 năm 1970. Nếu *mtime* bị bỏ qua hoặc là ``None``, thời gian hiện tại sẽ được sử dụng. Dùng *mtime* = 0 để tạo một luồng đã nén không phụ thuộc vào thời điểm tạo.

   Xem phần bên dưới để biết thuộc tính :attr:`mtime` được thiết lập khi giải nén.

   Việc gọi phương thức :meth:`!close` của một đối tượng :class:`GzipFile` không đóng *fileobj*, vì bạn có thể muốn nối thêm dữ liệu sau phần dữ liệu đã nén. Điều này cũng cho phép bạn truyền một đối tượng :class:`io.BytesIO` được mở để ghi làm *fileobj*, rồi lấy bộ đệm bộ nhớ thu được bằng cách sử dụng
   :class:`io.BytesIO` phương thức :meth:`~io.BytesIO.getvalue` của đối tượng.

   :class:`GzipFile` hỗ trợ giao diện :class:`io.BufferedIOBase`, bao gồm phép lặp và câu lệnh :keyword:`with`. Chỉ
   Phương thức :meth:`~io.IOBase.truncate` chưa được triển khai.

   :class:`GzipFile` cũng cung cấp phương thức và thuộc tính sau:

   .. method:: peek(n)

      Đọc *n* byte chưa nén mà không làm thay đổi vị trí tệp. Số byte được trả về có thể nhiều hơn hoặc ít hơn số lượng được yêu cầu.

      .. note:: Mặc dù việc gọi :meth:`peek` không thay đổi vị trí tệp của :class:`GzipFile`, nó có thể thay đổi vị trí của đối tượng tệp bên dưới (ví dụ: nếu :class:`GzipFile` được tạo bằng tham số *fileobj*).

      .. versionadded:: 3.2

   .. attribute:: mode

      ``'rb'`` để đọc và ``'wb'`` để ghi.

      .. versionchanged:: 3.13
         Trong các phiên bản trước, đây là một số nguyên ``1`` hoặc ``2``.

   .. attribute:: mtime

      Khi giải nén, thuộc tính này được đặt thành dấu thời gian cuối cùng trong header được đọc gần đây nhất. Đây là một số nguyên, chứa số giây kể từ Unix epoch (00:00:00 UTC, ngày 1 tháng 1 năm 1970). Giá trị ban đầu trước khi đọc bất kỳ header nào là ``None``.

   .. attribute:: name

      Đường dẫn đến tệp gzip trên đĩa, dưới dạng :class:`str` hoặc :class:`bytes`. Tương đương với kết quả của :func:`os.fspath` trên đường dẫn đầu vào ban đầu, không thực hiện bất kỳ việc chuẩn hóa, phân giải hoặc mở rộng nào khác.

   .. versionchanged:: 3.1
      Đã bổ sung hỗ trợ cho câu lệnh :keyword:`with`, cùng với đối số constructor *mtime* và thuộc tính :attr:`mtime`.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ cho các tệp có đệm bằng số 0 và các tệp không thể seek.

   .. versionchanged:: 3.3
      Phương thức :meth:`io.BufferedIOBase.read1` hiện đã được triển khai.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các chế độ ``'x'`` và ``'xb'``.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ ghi các
      :term:`đối tượng giống bytes <bytes-like object>`. Phương thức :meth:`~io.BufferedIOBase.read` hiện chấp nhận một đối số thuộc ``None``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. deprecated:: 3.9
      Việc mở :class:`GzipFile` để ghi mà không chỉ định đối số *mode* đã không còn được khuyến nghị.

   .. versionchanged:: 3.12
      Xóa thuộc tính ``filename``, thay vào đó hãy sử dụng thuộc tính :attr:`~GzipFile.name`.


.. function:: compress(data, compresslevel=9, *, mtime=0)

   Nén *dữ liệu*, trả về một đối tượng :class:`bytes` chứa dữ liệu đã nén. *compresslevel* và *mtime* có cùng ý nghĩa như trong hàm khởi tạo :class:`GzipFile` ở trên, nhưng *mtime* mặc định là 0 để tạo đầu ra có thể tái lập.

   .. versionadded:: 3.2
   .. versionchanged:: 3.8
      Đã bổ sung tham số *mtime* để tạo đầu ra có thể tái lập.
   .. versionchanged:: 3.11
      Tốc độ được cải thiện bằng cách nén toàn bộ dữ liệu cùng lúc thay vì theo kiểu streaming. Các lệnh gọi có *mtime* được đặt thành ``0`` sẽ được ủy quyền cho
      :func:`zlib.compress` để có tốc độ tốt hơn. Trong trường hợp này, đầu ra có thể chứa giá trị byte "OS" trong header gzip khác với 255 "unknown" do triển khai zlib bên dưới cung cấp.

   .. versionchanged:: 3.13
      Byte OS trong header gzip được đảm bảo đặt thành 255 khi sử dụng hàm này, như trong 3.10 và các phiên bản trước.
   .. versionchanged:: 3.14
      Tham số *mtime* hiện mặc định là 0 để tạo đầu ra có thể tái lập. Để sử dụng hành vi trước đây là dùng thời gian hiện tại, hãy truyền ``None`` cho *mtime*.

.. function:: decompress(data)

   Giải nén *data*, trả về một đối tượng :class:`bytes` chứa dữ liệu chưa nén. Hàm này có khả năng giải nén dữ liệu gzip gồm nhiều member (nhiều khối gzip được nối với nhau). Khi chắc chắn dữ liệu chỉ chứa một member, hàm :func:`zlib.decompress` với *wbits* được đặt thành 31 sẽ nhanh hơn.

   .. versionadded:: 3.2
   .. versionchanged:: 3.11
      Tốc độ được cải thiện bằng cách giải nén các member cùng lúc trong bộ nhớ thay vì theo kiểu streaming.

.. _gzip-usage-examples:

Ví dụ sử dụng
-------------

Ví dụ về cách đọc tệp đã nén::

   import gzip
   with gzip.open('/home/joe/file.txt.gz', 'rb') as f:
       file_content = f.read()

Ví dụ về cách tạo tệp GZIP đã nén::

   import gzip
   content = b"Lots of content here"
   with gzip.open('/home/joe/file.txt.gz', 'wb') as f:
       f.write(content)

Ví dụ về cách nén GZIP một tệp hiện có::

   import gzip
   import shutil
   with open('/home/joe/file.txt', 'rb') as f_in:
       with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
           shutil.copyfileobj(f_in, f_out)

Ví dụ về cách nén GZIP một chuỗi nhị phân::

   import gzip
   s_in = b"Lots of content here"
   s_out = gzip.compress(s_in)

.. seealso::

   Mô-đun :mod:`zlib`
      Mô-đun nén dữ liệu cơ bản cần thiết để hỗ trợ định dạng tệp :program:`gzip`.

   Trong trường hợp (giải) nén bằng gzip là một nút thắt cổ chai, gói `python-isal`_ sẽ tăng tốc quá trình (giải) nén với API phần lớn tương thích.

   .. _python-isal: https://github.com/pycompression/python-isal

.. program:: gzip

.. _gzip-cli:

Giao diện dòng lệnh
-------------------

Mô-đun :mod:`!gzip` cung cấp một giao diện dòng lệnh đơn giản để nén hoặc giải nén tệp.

Sau khi được thực thi, mô-đun :mod:`!gzip` sẽ giữ lại (các) tệp đầu vào.

.. versionchanged:: 3.8

   Thêm một giao diện dòng lệnh mới kèm theo hướng dẫn sử dụng. Theo mặc định, khi bạn thực thi CLI, mức nén mặc định là 6.

Các tùy chọn dòng lệnh
^^^^^^^^^^^^^^^^^^^^^^

.. option:: file

   Nếu *file* không được chỉ định, hãy đọc từ :data:`sys.stdin`.

.. option:: --fast

   Cho biết phương pháp nén nhanh nhất (độ nén thấp hơn).

.. option:: --best

   Cho biết phương thức nén chậm nhất (nén tốt nhất).

.. option:: -d, --decompress

   Giải nén tệp đã cho.

.. option:: -h, --help

   Hiển thị thông báo trợ giúp.
