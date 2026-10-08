:mod:`!lzma` --- Nén bằng thuật toán LZMA
=========================================

.. module:: lzma
   :synopsis: Lớp bao bọc Python cho thư viện nén liblzma.

.. moduleauthor:: Nadeem Vawda <nadeem.vawda@gmail.com>
.. sectionauthor:: Nadeem Vawda <nadeem.vawda@gmail.com>

.. versionadded:: 3.3

**Mã nguồn:** :source:`Lib/lzma.py`

--------------

Mô-đun này cung cấp các lớp và hàm tiện ích để nén và giải nén dữ liệu bằng thuật toán nén LZMA. Mô-đun cũng bao gồm một giao diện tệp hỗ trợ các định dạng tệp ``.xz`` và ``.lzma`` cũ được sử dụng bởi
:program:`xz` tiện ích, cũng như các luồng nén thô.

Giao diện do mô-đun này cung cấp rất giống với giao diện của mô-đun :mod:`bz2`. Lưu ý rằng :class:`LZMAFile` và :class:`bz2.BZ2File` *không* thread-safe, vì vậy nếu bạn cần sử dụng một đối tượng :class:`LZMAFile` duy nhất từ nhiều thread, bạn cần bảo vệ nó bằng một lock.

.. include:: ../includes/optional-module.rst


.. exception:: LZMAError

   Ngoại lệ này được phát sinh khi xảy ra lỗi trong quá trình nén hoặc giải nén, hoặc khi khởi tạo trạng thái của bộ nén/bộ giải nén.


Đọc và ghi các tệp được nén
---------------------------

.. function:: open(filename, mode="rb", *, format=None, check=-1, preset=None, filters=None, encoding=None, errors=None, newline=None)

   Mở một tệp được nén bằng LZMA ở chế độ nhị phân hoặc văn bản, trả về một :term:`file object`.

   Đối số *filename* có thể là tên tệp thực tế (được cung cấp dưới dạng
   :class:`str`, :class:`bytes` hoặc đối tượng :term:`path-like <path-like object>`), trong trường hợp đó tệp được chỉ định sẽ được mở, hoặc có thể là một file object hiện có để đọc từ đó hoặc ghi vào đó.

   Đối số *mode* có thể là bất kỳ giá trị nào trong số ``"r"``, ``"rb"``, ``"w"``, ``"wb"``, ``"x"``, ``"xb"``, ``"a"`` hoặc ``"ab"`` cho chế độ nhị phân, hoặc ``"rt"``, ``"wt"``, ``"xt"`` hoặc ``"at"`` cho chế độ văn bản. Giá trị mặc định là ``"rb"``.

   Khi mở một tệp để đọc, các đối số *format* và *filters* có cùng ý nghĩa như trong :class:`LZMADecompressor`. Trong trường hợp này, không nên sử dụng các đối số *check* và *preset*.

   Khi mở một tệp để ghi, các đối số *format*, *check*, *preset* và *filters* có cùng ý nghĩa như trong :class:`LZMACompressor`.

   Ở chế độ nhị phân, hàm này tương đương với constructor :class:`LZMAFile`: ``LZMAFile(filename, mode, ...)``. Trong trường hợp này, không được cung cấp các đối số *encoding*, *errors* và *newline*.

   Ở chế độ văn bản, một đối tượng :class:`LZMAFile` được tạo và được bọc trong một
   instance :class:`io.TextIOWrapper` với encoding, cách xử lý lỗi và (các) ký tự kết thúc dòng được chỉ định.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các chế độ ``"x"``, ``"xb"`` và ``"xt"``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. class:: LZMAFile(filename=None, mode="r", *, format=None, check=-1, preset=None, filters=None)

   Mở một tệp được nén bằng LZMA ở chế độ nhị phân.

   Một :class:`LZMAFile` có thể bọc một :term:`file object` đã được mở hoặc hoạt động trực tiếp trên một tệp có tên. Đối số *filename* chỉ định đối tượng tệp cần bọc hoặc tên tệp cần mở (dưới dạng một :class:`str`,
   :class:`bytes` hoặc đối tượng :term:`path-like <path-like object>`). Khi bao bọc một đối tượng tệp hiện có, tệp được bao bọc sẽ không bị đóng khi
   :class:`LZMAFile` được đóng.

   Đối số *mode* có thể là ``"r"`` để đọc (mặc định), ``"w"`` để ghi đè, ``"x"`` để tạo độc quyền hoặc ``"a"`` để nối thêm. Tương ứng, bạn cũng có thể cung cấp các giá trị này dưới dạng ``"rb"``, ``"wb"``, ``"xb"`` và ``"ab"``.

   Nếu *filename* là một đối tượng tệp (thay vì tên tệp thực tế), chế độ ``"w"`` sẽ không cắt ngắn tệp mà tương đương với ``"a"``.

   Khi mở một tệp để đọc, tệp đầu vào có thể là phép nối của nhiều luồng nén riêng biệt. Các luồng này sẽ được giải mã trong suốt như một luồng logic duy nhất.

   Khi mở một tệp để đọc, các đối số *format* và *filters* có cùng ý nghĩa như trong :class:`LZMADecompressor`. Trong trường hợp này, không nên sử dụng các đối số *check* và *preset*.

   Khi mở một tệp để ghi, các đối số *format*, *check*, *preset* và *filters* có cùng ý nghĩa như trong :class:`LZMACompressor`.

   :class:`LZMAFile` hỗ trợ tất cả các thành viên được chỉ định bởi
   :class:`io.BufferedIOBase`, ngoại trừ :meth:`~io.BufferedIOBase.detach` và :meth:`~io.IOBase.truncate`. Việc lặp và câu lệnh :keyword:`with` được hỗ trợ.

   Các phương thức và thuộc tính sau đây cũng được cung cấp:

   .. method:: peek(size=-1)

      Trả về dữ liệu đã được đệm mà không thay đổi vị trí tệp. Ít nhất một byte dữ liệu sẽ được trả về, trừ khi đã đạt EOF. Số byte được trả về chính xác không được quy định (đối số *size* bị bỏ qua).

      .. note:: Mặc dù việc gọi :meth:`peek` không thay đổi vị trí tệp của :class:`LZMAFile`, thao tác này có thể thay đổi vị trí của đối tượng tệp bên dưới (ví dụ: nếu :class:`LZMAFile` được tạo bằng cách truyền một đối tượng tệp cho *filename*).

   .. attribute:: mode

      ``'rb'`` để đọc và ``'wb'`` để ghi.

      .. versionadded:: 3.13

   .. attribute:: name

      Tên tệp lzma. Tương đương với thuộc tính :attr:`~io.FileIO.name` của :term:`file object` bên dưới.

      .. versionadded:: 3.13


   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các chế độ ``"x"`` và ``"xb"``.

   .. versionchanged:: 3.5
      Phương thức :meth:`~io.BufferedIOBase.read` hiện chấp nhận đối số có giá trị ``None``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


Nén và giải nén dữ liệu trong bộ nhớ
------------------------------------

.. class:: LZMACompressor(format=FORMAT_XZ, check=-1, preset=None, filters=None)

   Tạo một đối tượng compressor, có thể dùng để nén dữ liệu tăng dần.

   Để có cách thuận tiện hơn khi nén một khối dữ liệu đơn lẻ, hãy xem
   :func:`compress`.

   Đối số *format* chỉ định định dạng container cần sử dụng. Các giá trị có thể có là :const:`FORMAT_XZ` (mặc định),
   :const:`FORMAT_ALONE` và :const:`FORMAT_RAW`.

   Đối số *check* chỉ định loại kiểm tra tính toàn vẹn cần đưa vào dữ liệu đã nén. Kiểm tra này được sử dụng khi giải nén để đảm bảo dữ liệu không bị hỏng. Các giá trị có thể có là :const:`CHECK_NONE`,
   :const:`CHECK_CRC32`, :const:`CHECK_CRC64` (mặc định cho
   :const:`FORMAT_XZ`) và :const:`CHECK_SHA256`.

   Nếu kiểm tra được chỉ định không được hỗ trợ, một :class:`LZMAError` sẽ được phát sinh.

   Các thiết lập nén có thể được chỉ định dưới dạng mức nén đặt sẵn (với đối số *preset*) hoặc chỉ định chi tiết dưới dạng một chuỗi bộ lọc tùy chỉnh (với đối số *filters*).

   Đối số *preset* (nếu được cung cấp) phải là một số nguyên từ ``0`` đến ``9`` (bao gồm cả hai đầu), tùy chọn được OR với hằng số
   :const:`PRESET_EXTREME`. Nếu không cung cấp *preset* hoặc *filters*, hành vi mặc định là sử dụng :const:`PRESET_DEFAULT` (mức preset ``6``). Các preset cao hơn tạo ra đầu ra nhỏ hơn nhưng khiến quá trình nén chậm hơn.

   .. note::

      Ngoài việc tiêu tốn nhiều CPU hơn, việc nén bằng các preset cao hơn cũng yêu cầu nhiều bộ nhớ hơn đáng kể (và tạo ra đầu ra cần nhiều bộ nhớ hơn để giải nén). Chẳng hạn, với preset ``9``, phần chi phí phụ trội cho một
      đối tượng :class:`LZMACompressor` có thể lên tới 800 MiB. Vì lý do này, nhìn chung tốt nhất là sử dụng preset mặc định.

   Đối số *filters* (nếu được cung cấp) phải là một filter chain specifier. Xem :ref:`filter-chain-specs` để biết chi tiết.

   .. method:: compress(data)

      Nén *data* (một đối tượng :class:`bytes`), trả về một đối tượng :class:`bytes` chứa dữ liệu đã nén cho ít nhất một phần dữ liệu đầu vào. Một phần *data* có thể được lưu đệm nội bộ để sử dụng trong các lần gọi sau tới
      :meth:`compress` và :meth:`flush`. Dữ liệu được trả về phải được nối với đầu ra của mọi lần gọi trước đó tới :meth:`compress`.

   .. method:: flush()

      Kết thúc quá trình nén, trả về một đối tượng :class:`bytes` chứa mọi dữ liệu được lưu trong các bộ đệm nội bộ của compressor.

      Không thể sử dụng compressor sau khi phương thức này được gọi.


.. class:: LZMADecompressor(format=FORMAT_AUTO, memlimit=None, filters=None)

   Tạo một đối tượng decompressor, có thể được dùng để giải nén dữ liệu từng phần.

   Để có cách thuận tiện hơn nhằm giải nén toàn bộ compressed stream cùng một lúc, hãy xem :func:`decompress`.

   Đối số *format* chỉ định container format cần sử dụng. Giá trị mặc định là :const:`FORMAT_AUTO`, có thể giải nén cả tệp ``.xz`` và ``.lzma``. Các giá trị khả dụng khác là :const:`FORMAT_XZ`,
   :const:`FORMAT_ALONE` và :const:`FORMAT_RAW`.

   Đối số *memlimit* chỉ định giới hạn (tính bằng byte) về lượng bộ nhớ mà decompressor có thể sử dụng. Khi sử dụng đối số này, quá trình giải nén sẽ thất bại với :class:`LZMAError` nếu không thể giải nén đầu vào trong giới hạn bộ nhớ đã cho.

   Đối số *filters* chỉ định filter chain được sử dụng để tạo stream đang được giải nén. Đối số này là bắt buộc nếu *format* là
   :const:`FORMAT_RAW`, nhưng không nên được sử dụng cho các định dạng khác. Xem :ref:`filter-chain-specs` để biết thêm thông tin về các chuỗi bộ lọc.

   .. note::
      Lớp này không tự động xử lý các đầu vào chứa nhiều luồng đã nén, không giống như :func:`decompress` và :class:`LZMAFile`. Để giải nén đầu vào gồm nhiều luồng bằng :class:`LZMADecompressor`, bạn phải tạo một bộ giải nén mới cho mỗi luồng.

   .. method:: decompress(data, max_length=-1)

      Giải nén *data* (một :term:`bytes-like object`), trả về dữ liệu chưa nén dưới dạng bytes. Một phần *data* có thể được đệm nội bộ để sử dụng trong các lần gọi :meth:`decompress` sau. Dữ liệu được trả về nên được nối với đầu ra của mọi lần gọi :meth:`decompress` trước đó.

      Nếu *max_length* không âm, trả về nhiều nhất *max_length* byte dữ liệu đã giải nén. Nếu đạt đến giới hạn này và vẫn có thể tạo thêm đầu ra, thuộc tính :attr:`~.needs_input` sẽ được đặt thành ``False``. Trong trường hợp này, lần gọi tiếp theo đến
      :meth:`~.decompress` có thể cung cấp *data* dưới dạng ``b''`` để lấy thêm đầu ra.

      Nếu toàn bộ dữ liệu đầu vào đã được giải nén và trả về (do dữ liệu này ít hơn *max_length* byte, hoặc do *max_length* là số âm), thuộc tính :attr:`~.needs_input` sẽ được đặt thành ``True``.

      Việc cố gắng giải nén dữ liệu sau khi đạt đến cuối luồng sẽ phát sinh một :exc:`EOFError`. Mọi dữ liệu được tìm thấy sau cuối luồng sẽ bị bỏ qua và được lưu trong thuộc tính :attr:`~.unused_data`.

      .. versionchanged:: 3.5
         Đã thêm tham số *max_length*.

   .. attribute:: check

      Mã định danh của phép kiểm tra tính toàn vẹn được luồng đầu vào sử dụng. Giá trị này có thể là
      :const:`CHECK_UNKNOWN` cho đến khi đã giải mã đủ dữ liệu đầu vào để xác định phép kiểm tra tính toàn vẹn mà luồng sử dụng.

   .. attribute:: eof

      ``True`` nếu đã đạt đến dấu kết thúc luồng.

   .. attribute:: unused_data

      Dữ liệu được tìm thấy sau phần cuối của luồng đã nén.

      Trước khi đạt đến phần cuối của luồng, giá trị này sẽ là ``b""``.

   .. attribute:: needs_input

      ``False`` nếu phương thức :meth:`.decompress` có thể cung cấp thêm dữ liệu đã giải nén trước khi cần dữ liệu đầu vào chưa nén mới.

      .. versionadded:: 3.5

.. function:: compress(data, format=FORMAT_XZ, check=-1, preset=None, filters=None)

   Nén *data* (một đối tượng :class:`bytes`), trả về dữ liệu đã nén dưới dạng
   đối tượng :class:`bytes`.

   Xem :class:`LZMACompressor` ở trên để biết mô tả về các đối số *format*, *check*, *preset* và *filters*.


.. function:: decompress(data, format=FORMAT_AUTO, memlimit=None, filters=None)

   Giải nén *data* (một đối tượng :class:`bytes`), trả về dữ liệu chưa nén dưới dạng đối tượng :class:`bytes`.

   Nếu *data* là phép nối của nhiều stream đã nén riêng biệt, hãy giải nén tất cả các stream này và trả về phép nối của các kết quả.

   Xem :class:`LZMADecompressor` ở trên để biết mô tả về các đối số *format*, *memlimit* và *filters*.


Linh tinh
---------

.. function:: is_check_supported(check)

   Trả về ``True`` nếu phép kiểm tra tính toàn vẹn đã cho được hệ thống này hỗ trợ.

   :const:`CHECK_NONE` và :const:`CHECK_CRC32` luôn được hỗ trợ.
   :const:`CHECK_CRC64` và :const:`CHECK_SHA256` có thể không khả dụng nếu bạn đang sử dụng một phiên bản :program:`liblzma` được biên dịch với tập tính năng hạn chế.


.. _filter-chain-specs:

Chỉ định chuỗi bộ lọc tùy chỉnh
-------------------------------

Bộ chỉ định chuỗi bộ lọc là một chuỗi các dictionary, trong đó mỗi dictionary chứa ID và các tùy chọn cho một bộ lọc. Mỗi dictionary phải chứa khóa ``"id"``, và có thể chứa các khóa bổ sung để chỉ định các tùy chọn phụ thuộc vào bộ lọc. Các ID bộ lọc hợp lệ như sau:

* Bộ lọc nén:

  * :const:`FILTER_LZMA1` (dùng với :const:`FORMAT_ALONE`)
  * :const:`FILTER_LZMA2` (dùng với :const:`FORMAT_XZ` và :const:`FORMAT_RAW`)

* Bộ lọc Delta:

  * :const:`FILTER_DELTA`

* Bộ lọc Branch-Call-Jump (BCJ):

  * :const:`!FILTER_X86`
  * :const:`!FILTER_IA64`
  * :const:`!FILTER_ARM`
  * :const:`!FILTER_ARMTHUMB`
  * :const:`!FILTER_POWERPC`
  * :const:`!FILTER_SPARC`

Một chuỗi bộ lọc có thể gồm tối đa 4 bộ lọc và không được để trống. Bộ lọc cuối cùng trong chuỗi phải là bộ lọc nén, còn các bộ lọc khác phải là bộ lọc Delta hoặc BCJ.

Bộ lọc nén hỗ trợ các tùy chọn sau (được chỉ định dưới dạng các mục bổ sung trong dictionary đại diện cho bộ lọc):

* ``preset``: Compression preset được dùng làm nguồn các giá trị mặc định cho những tùy chọn không được chỉ định rõ ràng.
* ``dict_size``: Kích thước dictionary tính bằng byte. Giá trị này phải nằm trong khoảng từ 4 KiB đến 1.5 GiB (bao gồm cả hai đầu mút).
* ``lc``: Số lượng bit ngữ cảnh literal.
* ``lp``: Số lượng bit vị trí literal. Tổng ``lc + lp`` phải tối đa là 4.
* ``pb``: Số lượng bit vị trí; phải tối đa là 4.
* ``mode``: :const:`MODE_FAST` hoặc :const:`MODE_NORMAL`.
* ``nice_len``: Độ dài nào nên được xem là "độ dài phù hợp" cho một kết quả khớp. Giá trị này phải là 273 hoặc nhỏ hơn.
* ``mf``: Trình tìm kiếm kết quả khớp cần sử dụng -- :const:`MF_HC3`, :const:`MF_HC4`,
  :const:`MF_BT2`, :const:`MF_BT3`, hoặc :const:`MF_BT4`.
* ``depth``: Độ sâu tìm kiếm tối đa được bộ tìm kiếm khớp sử dụng. 0 (mặc định) có nghĩa là tự động chọn dựa trên các tùy chọn bộ lọc khác.

Bộ lọc delta lưu trữ sự khác biệt giữa các byte, tạo ra dữ liệu đầu vào có tính lặp lại cao hơn cho bộ nén trong một số trường hợp. Bộ lọc này hỗ trợ một tùy chọn, ``dist``. Tùy chọn này cho biết khoảng cách giữa các byte cần lấy hiệu. Giá trị mặc định là 1, tức là lấy hiệu giữa các byte liền kề.

Các bộ lọc BCJ được thiết kế để áp dụng cho mã máy. Chúng chuyển đổi các nhánh, lệnh gọi và lệnh nhảy tương đối trong mã để sử dụng địa chỉ tuyệt đối, nhằm tăng tính dư thừa mà bộ nén có thể khai thác. Các bộ lọc này hỗ trợ một tùy chọn, ``start_offset``. Tùy chọn này chỉ định địa chỉ cần được ánh xạ tới đầu dữ liệu đầu vào. Giá trị mặc định là 0.


Hằng số
-------

Các hằng số cấp mô-đun sau đây được cung cấp để sử dụng làm các đối số *format*, *check*, *preset* và *filters* của các lớp và hàm ở trên.

Các định dạng container:

.. data:: FORMAT_XZ

   Định dạng container ``.xz``.

.. data:: FORMAT_ALONE

   Định dạng container ``.lzma`` cũ. Định dạng này bị giới hạn hơn ``.xz`` -- nó không hỗ trợ kiểm tra tính toàn vẹn hoặc nhiều bộ lọc.

.. data:: FORMAT_RAW

   Một luồng dữ liệu thô, không sử dụng bất kỳ định dạng container nào. Bộ chỉ định định dạng này không hỗ trợ kiểm tra tính toàn vẹn và yêu cầu bạn luôn chỉ định một chuỗi bộ lọc tùy chỉnh (cho cả quá trình nén và giải nén). Ngoài ra, dữ liệu được nén theo cách này không thể được giải nén bằng
   :const:`FORMAT_AUTO`.

.. data:: FORMAT_AUTO

   Chỉ được sử dụng để giải nén. Định dạng container được tự động phát hiện, vì vậy cả tệp ``.xz`` và ``.lzma`` đều có thể được giải nén.

Kiểm tra tính toàn vẹn:

.. data:: CHECK_NONE

   Không kiểm tra tính toàn vẹn. Đây là giá trị mặc định (và là giá trị duy nhất được chấp nhận) cho
   :const:`FORMAT_ALONE` và :const:`FORMAT_RAW`.

.. data:: CHECK_CRC32

   Một mã kiểm tra dư vòng (Cyclic Redundancy Check) 32-bit.

.. data:: CHECK_CRC64

   Một mã kiểm tra dư vòng 64-bit (Cyclic Redundancy Check). Đây là giá trị mặc định cho
   :const:`FORMAT_XZ`.

.. data:: CHECK_SHA256

   Một Thuật toán Băm An toàn 256-bit (Secure Hash Algorithm).

.. data:: CHECK_UNKNOWN

   Chưa thể xác định được phép kiểm tra tính toàn vẹn mà một stream sử dụng. Đây có thể là giá trị của thuộc tính :attr:`LZMADecompressor.check` cho đến khi đủ dữ liệu đầu vào được giải mã.

.. data:: CHECK_ID_MAX

   ID kiểm tra tính toàn vẹn lớn nhất được hỗ trợ.

Các preset nén:

.. data:: PRESET_DEFAULT

   Preset nén mặc định, tương đương với mức preset ``6``.

.. data:: PRESET_EXTREME

   Một cờ có thể được OR theo bit với một mức preset (từ ``0`` đến ``9``) để chọn biến thể chậm hơn nhưng kiểm tra kỹ lưỡng hơn của preset đó.

ID bộ lọc và các tùy chọn:

.. data:: FILTER_LZMA1
          FILTER_LZMA2

   Các bộ lọc nén LZMA1 và LZMA2. :const:`FILTER_LZMA1` được dùng với :const:`FORMAT_ALONE`, còn :const:`FILTER_LZMA2` được dùng với
   :const:`FORMAT_XZ` và :const:`FORMAT_RAW`.

.. data:: FILTER_DELTA

   Bộ lọc delta.

.. data:: MODE_FAST
          MODE_NORMAL

   Các chế độ nén có thể được dùng làm tùy chọn ``mode`` của bộ chỉ định bộ lọc (xem :ref:`filter-chain-specs`).

.. data:: MF_HC3
          MF_HC4 MF_BT2 MF_BT3 MF_BT4

   Các match finder có thể được sử dụng làm tùy chọn ``mf`` của bộ chỉ định bộ lọc (xem :ref:`filter-chain-specs`).


Ví dụ
-----

Đọc tệp đã nén::

   import lzma
   with lzma.open("file.xz") as f:
       file_content = f.read()

Tạo tệp nén::

   import lzma
   data = b"Insert Data Here"
   with lzma.open("file.xz", "w") as f:
       f.write(data)

Nén dữ liệu trong bộ nhớ::

   import lzma
   data_in = b"Insert Data Here"
   data_out = lzma.compress(data_in)

Nén tăng dần::

   import lzma
   lzc = lzma.LZMACompressor()
   out1 = lzc.compress(b"Some data\n")
   out2 = lzc.compress(b"Another piece of data\n")
   out3 = lzc.compress(b"Even more data\n")
   out4 = lzc.flush()
   # Nối tất cả các kết quả từng phần:
   result = b"".join([out1, out2, out3, out4])

Ghi dữ liệu đã nén vào một tệp đã được mở sẵn::

   import lzma
   with open("file.xz", "wb") as f:
       f.write(b"This data will not be compressed\n")
       with lzma.open(f, "w") as lzf:
           lzf.write(b"This *will* be compressed\n")
       f.write(b"Not compressed\n")

Tạo tệp đã nén bằng chuỗi bộ lọc tùy chỉnh::

   import lzma
   my_filters = [
       {"id": lzma.FILTER_DELTA, "dist": 5},
       {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
   ]
   with lzma.open("file.xz", "w", filters=my_filters) as f:
       f.write(b"blah blah blah")
