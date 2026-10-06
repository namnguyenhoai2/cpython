:mod:`!bz2` --- Hỗ trợ nén bằng :program:`bzip2`
================================================

.. module:: bz2
   :synopsis: Giao diện cho việc nén và giải nén bằng bzip2.

.. moduleauthor:: Gustavo Niemeyer <niemeyer@conectiva.com>
.. moduleauthor:: Nadeem Vawda <nadeem.vawda@gmail.com>
.. sectionauthor:: Gustavo Niemeyer <niemeyer@conectiva.com>
.. sectionauthor:: Nadeem Vawda <nadeem.vawda@gmail.com>

**Mã nguồn:** :source:`Lib/bz2.py`

--------------

Mô-đun này cung cấp giao diện toàn diện để nén và giải nén dữ liệu bằng thuật toán nén bzip2.

Mô-đun :mod:`!bz2` bao gồm:

* Hàm :func:`.open` và lớp :class:`BZ2File` để đọc và ghi các tệp đã nén.
* Các lớp :class:`BZ2Compressor` và :class:`BZ2Decompressor` để nén và giải nén tăng dần.
* Các hàm :func:`compress` và :func:`decompress` để (giải) nén một lần.

.. include:: ../includes/optional-module.rst


(Giải) nén tệp
--------------

.. function:: open(filename, mode='rb', compresslevel=9, encoding=None, errors=None, newline=None)

   Mở tệp được nén bằng bzip2 ở chế độ nhị phân hoặc văn bản, trả về một :term:`file object`.

   Giống như hàm khởi tạo của :class:`BZ2File`, đối số *filename* có thể là tên tệp thực tế (một đối tượng :class:`str` hoặc :class:`bytes`), hoặc một đối tượng tệp hiện có để đọc hoặc ghi.

   Đối số *mode* có thể là bất kỳ giá trị nào trong số ``'r'``, ``'rb'``, ``'w'``, ``'wb'``, ``'x'``, ``'xb'``, ``'a'`` hoặc ``'ab'`` cho chế độ nhị phân, hoặc ``'rt'``, ``'wt'``, ``'xt'`` hoặc ``'at'`` cho chế độ văn bản. Giá trị mặc định là ``'rb'``.

   Đối số *compresslevel* là một số nguyên từ 1 đến 9, giống như đối với
   :class:`BZ2File` hàm khởi tạo.

   Ở chế độ nhị phân, hàm này tương đương với constructor :class:`BZ2File`: ``BZ2File(filename, mode, compresslevel=compresslevel)``. Trong trường hợp này, không được cung cấp các đối số *encoding*, *errors* và *newline*.

   Ở chế độ văn bản, một đối tượng :class:`BZ2File` được tạo và bọc trong một
   instance :class:`io.TextIOWrapper` với encoding, hành vi xử lý lỗi và (các) ký tự kết thúc dòng được chỉ định.

   .. versionadded:: 3.3

   .. versionchanged:: 3.4
      Chế độ ``'x'`` (tạo độc quyền) đã được bổ sung.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. class:: BZ2File(filename, mode='r', *, compresslevel=9)

   Mở một tệp được nén bằng bzip2 ở chế độ nhị phân.

   Nếu *filename* là một đối tượng :class:`str` hoặc :class:`bytes`, hãy mở trực tiếp tệp có tên đó. Nếu không, *filename* phải là một :term:`file object`, được dùng để đọc hoặc ghi dữ liệu đã nén.

   Đối số *mode* có thể là ``'r'`` để đọc (mặc định), ``'w'`` để ghi đè, ``'x'`` để tạo độc quyền hoặc ``'a'`` để nối thêm. Tương ứng, có thể cung cấp các giá trị này dưới dạng ``'rb'``, ``'wb'``, ``'xb'`` và ``'ab'``.

   Nếu *filename* là một đối tượng tệp (thay vì tên tệp thực tế), chế độ ``'w'`` sẽ không cắt ngắn tệp mà tương đương với ``'a'``.

   Nếu *mode* là ``'w'`` hoặc ``'a'``, *compresslevel* có thể là một số nguyên từ ``1`` đến ``9``, chỉ định mức độ nén: ``1`` tạo ra mức nén thấp nhất, còn ``9`` (mặc định) tạo ra mức nén cao nhất.

   Nếu *mode* là ``'r'``, tệp đầu vào có thể là phần nối của nhiều luồng đã nén.

   :class:`BZ2File` cung cấp tất cả các thành phần được chỉ định bởi
   :class:`io.BufferedIOBase`, ngoại trừ :meth:`~io.BufferedIOBase.detach` và :meth:`~io.IOBase.truncate`. Việc lặp và câu lệnh :keyword:`with` được hỗ trợ.

   :class:`BZ2File` cũng cung cấp các phương thức và thuộc tính sau:

   .. method:: peek([n])

      Trả về dữ liệu đã được đệm mà không thay đổi vị trí tệp. Sẽ trả về ít nhất một byte dữ liệu (trừ khi đã đến EOF). Số byte chính xác được trả về không được quy định.

      .. note:: Mặc dù việc gọi :meth:`peek` không làm thay đổi vị trí tệp của :class:`BZ2File`, thao tác này có thể làm thay đổi vị trí của đối tượng tệp bên dưới (ví dụ: nếu :class:`BZ2File` được tạo bằng cách truyền một đối tượng tệp cho *filename*).

      .. versionadded:: 3.3

   .. method:: fileno()

      Trả về file descriptor của tệp bên dưới.

      .. versionadded:: 3.3

   .. method:: readable()

      Trả về liệu tệp có được mở để đọc hay không.

      .. versionadded:: 3.3

   .. method:: seekable()

      Trả về liệu tệp có hỗ trợ thao tác tìm vị trí hay không.

      .. versionadded:: 3.3

   .. method:: writable()

      Trả về liệu tệp có được mở để ghi hay không.

      .. versionadded:: 3.3

   .. method:: read1(size=-1)

      Đọc tối đa *size* byte chưa giải nén, đồng thời cố gắng tránh thực hiện nhiều lần đọc từ stream bên dưới. Đọc tối đa lượng dữ liệu bằng kích thước của bộ đệm nếu size là số âm.

      Trả về ``b''`` nếu tệp ở cuối tệp (EOF).

      .. versionadded:: 3.3

   .. method:: readinto(b)

      Đọc các byte vào *b*.

      Trả về số byte đã đọc (0 khi gặp EOF).

      .. versionadded:: 3.3

   .. attribute:: mode

      ``'rb'`` để đọc và ``'wb'`` để ghi.

      .. versionadded:: 3.13

   .. attribute:: name

      Tên tệp bzip2. Tương đương với thuộc tính :attr:`~io.FileIO.name` của :term:`file object` bên dưới.

      .. versionadded:: 3.13


   .. versionchanged:: 3.1
      Đã bổ sung hỗ trợ cho câu lệnh :keyword:`with`.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ để *filename* là một :term:`file object` thay vì tên tệp thực tế.

      Chế độ ``'a'`` (append) đã được thêm vào, cùng với khả năng đọc các tệp đa luồng.

   .. versionchanged:: 3.4
      Chế độ ``'x'`` (tạo độc quyền) đã được bổ sung.

   .. versionchanged:: 3.5
      Phương thức :meth:`~io.BufferedIOBase.read` hiện chấp nhận một đối số có giá trị là ``None``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.9
      Tham số *buffering* đã bị xóa. Tham số này đã bị bỏ qua và không được khuyến nghị kể từ Python 3.0. Hãy truyền một đối tượng tệp đã mở để kiểm soát cách tệp được mở.

      Tham số *compresslevel* chỉ có thể được truyền dưới dạng keyword.

   .. versionchanged:: 3.10
      Lớp này không an toàn với thread khi có nhiều reader hoặc writer hoạt động đồng thời, giống như các lớp tương đương trong :mod:`gzip` và
      :mod:`lzma` đã luôn như vậy.


Nén và giải nén tăng dần
------------------------

.. class:: BZ2Compressor(compresslevel=9)

   Tạo một đối tượng compressor mới. Bạn có thể dùng đối tượng này để nén dữ liệu tăng dần. Để nén một lần, hãy dùng hàm :func:`compress` thay thế.

   *compresslevel*, nếu được cung cấp, phải là một số nguyên nằm giữa ``1`` và ``9``. Giá trị mặc định là ``9``.

   .. method:: compress(data)

      Cung cấp dữ liệu cho đối tượng compressor. Trả về một đoạn dữ liệu đã nén nếu có thể, hoặc một chuỗi byte rỗng nếu không.

      Khi đã cung cấp xong dữ liệu cho compressor, hãy gọi
      phương thức :meth:`flush` để hoàn tất quá trình nén.


   .. method:: flush()

      Hoàn tất quá trình nén. Trả về dữ liệu đã nén còn lại trong các bộ đệm nội bộ.

      Không được sử dụng đối tượng compressor sau khi gọi phương thức này.


.. class:: BZ2Decompressor()

   Tạo một đối tượng decompressor mới. Có thể sử dụng đối tượng này để giải nén dữ liệu theo từng phần. Để nén một lần, hãy sử dụng hàm :func:`decompress` thay thế.

   .. note::
      Lớp này không tự động xử lý các đầu vào chứa nhiều luồng dữ liệu đã nén, không giống như :func:`decompress` và :class:`BZ2File`. Nếu cần giải nén đầu vào nhiều luồng bằng :class:`BZ2Decompressor`, bạn phải sử dụng một decompressor mới cho mỗi luồng.

   .. method:: decompress(data, max_length=-1)

      Giải nén *data* (một :term:`bytes-like object`), trả về dữ liệu chưa nén dưới dạng byte. Một phần *data* có thể được đệm nội bộ để sử dụng trong các lần gọi :meth:`decompress` sau. Dữ liệu được trả về nên được nối với đầu ra của mọi lần gọi :meth:`decompress` trước đó.

      Nếu *max_length* không âm, trả về nhiều nhất *max_length* byte dữ liệu đã giải nén. Nếu đạt đến giới hạn này và vẫn có thể tạo thêm đầu ra, thuộc tính :attr:`~.needs_input` sẽ được đặt thành ``False``. Trong trường hợp này, lần gọi tiếp theo đến
      :meth:`~.decompress` có thể cung cấp *data* dưới dạng ``b''`` để nhận thêm phần đầu ra.

      Nếu tất cả dữ liệu đầu vào đã được giải nén và trả về (do dữ liệu này có ít hơn *max_length* byte hoặc do *max_length* là số âm), thuộc tính :attr:`~.needs_input` sẽ được đặt thành ``True``.

      Việc cố gắng giải nén dữ liệu sau khi đã đến cuối luồng sẽ gây ra :exc:`EOFError`. Mọi dữ liệu được tìm thấy sau cuối luồng sẽ bị bỏ qua và được lưu trong thuộc tính :attr:`~.unused_data`.

      .. versionchanged:: 3.5
         Đã thêm tham số *max_length*.

   .. attribute:: eof

      ``True`` nếu đã đến dấu hiệu kết thúc luồng.

      .. versionadded:: 3.3


   .. attribute:: unused_data

      Dữ liệu được tìm thấy sau cuối luồng đã nén.

      Nếu truy cập thuộc tính này trước khi đến cuối luồng, giá trị của nó sẽ là ``b''``.

   .. attribute:: needs_input

      ``False`` nếu phương thức :meth:`.decompress` có thể cung cấp thêm dữ liệu đã giải nén trước khi cần dữ liệu đầu vào chưa giải nén mới.

      .. versionadded:: 3.5


Nén (giải nén) một lần
----------------------

.. function:: compress(data, compresslevel=9)

   Nén *data*, một :term:`bytes-like object <bytes-like object>`.

   *compresslevel*, nếu được cung cấp, phải là một số nguyên nằm giữa ``1`` và ``9``. Giá trị mặc định là ``9``.

   Để nén tăng dần, hãy sử dụng một :class:`BZ2Compressor` thay vào đó.


.. function:: decompress(data)

   Giải nén *data*, một :term:`bytes-like object <bytes-like object>`.

   Nếu *data* là phần nối của nhiều luồng đã nén, hãy giải nén tất cả các luồng.

   Để giải nén tăng dần, hãy sử dụng một :class:`BZ2Decompressor` thay vào đó.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ cho đầu vào đa luồng.

.. _bz2-usage-examples:

Ví dụ sử dụng
-------------

Dưới đây là một số ví dụ về cách sử dụng điển hình của mô-đun :mod:`!bz2`.

Sử dụng :func:`compress` và :func:`decompress` để minh họa việc nén và giải nén theo vòng khứ hồi:

    >>> import bz2
    >>> data = b"""\
    ... Donec rhoncus quis sapien sit amet molestie. Fusce scelerisque vel augue
    ... nec ullamcorper. Nam rutrum pretium placerat. Aliquam vel tristique lorem,
    ... sit amet cursus ante. In interdum laoreet mi, sit amet ultrices purus
    ... pulvinar a. Nam gravida euismod magna, non varius justo tincidunt feugiat.
    ... Aliquam pharetra lacus non risus vehicula rutrum. Maecenas aliquam leo
    ... felis. Pellentesque semper nunc sit amet nibh ullamcorper, ac elementum
    ... dolor luctus. Curabitur lacinia mi ornare consectetur vestibulum."""
    >>> c = bz2.compress(data)
    >>> len(data) / len(c)  # Tỷ lệ nén dữ liệu
    1.513595166163142
    >>> d = bz2.decompress(c)
    >>> data == d  # Kiểm tra có bằng đối tượng gốc sau khi nén rồi giải nén hay không
    True

Sử dụng :class:`BZ2Compressor` để nén tăng dần:

    >>> import bz2
    >>> def gen_data(chunks=10, chunksize=1000):
    ...     """Yield incremental blocks of chunksize bytes."""
    ...     for _ in range(chunks):
    ...         yield b"z" * chunksize
    ...
    >>> comp = bz2.BZ2Compressor()
    >>> out = b""
    >>> for chunk in gen_data():
    ...     # Cung cấp dữ liệu cho đối tượng nén
    ...     out = out + comp.compress(chunk)
    ...
    >>> # Hoàn tất quá trình nén. Gọi hàm này sau khi đã
    >>> # cung cấp xong dữ liệu cho đối tượng nén.
    >>> out = out + comp.flush()

Ví dụ trên sử dụng một luồng dữ liệu "không ngẫu nhiên" điển hình (một luồng gồm các khối ``b"z"``). Dữ liệu ngẫu nhiên thường khó nén, trong khi dữ liệu có thứ tự và lặp lại thường cho tỷ lệ nén cao.

Ghi và đọc tệp được nén bằng bzip2 ở chế độ nhị phân:

    >>> import bz2
    >>> data = b"""\
    ... Donec rhoncus quis sapien sit amet molestie. Fusce scelerisque vel augue
    ... nec ullamcorper. Nam rutrum pretium placerat. Aliquam vel tristique lorem,
    ... sit amet cursus ante. In interdum laoreet mi, sit amet ultrices purus
    ... pulvinar a. Nam gravida euismod magna, non varius justo tincidunt feugiat.
    ... Aliquam pharetra lacus non risus vehicula rutrum. Maecenas aliquam leo
    ... felis. Pellentesque semper nunc sit amet nibh ullamcorper, ac elementum
    ... dolor luctus. Curabitur lacinia mi ornare consectetur vestibulum."""
    >>> with bz2.open("myfile.bz2", "wb") as f:
    ...     # Ghi dữ liệu đã nén vào tệp
    ...     unused = f.write(data)
    ...
    >>> with bz2.open("myfile.bz2", "rb") as f:
    ...     # Giải nén dữ liệu từ tệp
    ...     content = f.read()
    ...
    >>> content == data  # Kiểm tra có bằng đối tượng gốc sau khi nén rồi giải nén hay không
    True

.. testcleanup::

   import os
   os.remove("myfile.bz2")
