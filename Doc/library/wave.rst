:mod:`!wave` --- Đọc và ghi tệp WAV
===================================

.. module:: wave
   :synopsis: Cung cấp một giao diện cho định dạng âm thanh WAV.

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>
.. Documentations stolen from comments in file.

**Mã nguồn:** :source:`Lib/wave.py`

--------------

Mô-đun :mod:`!wave` cung cấp một giao diện thuận tiện cho định dạng tệp Waveform Audio "WAVE" (hoặc "WAV"). Chỉ hỗ trợ các tệp wave được mã hóa PCM không nén.

.. versionchanged:: 3.12

   Đã bổ sung hỗ trợ cho các header ``WAVE_FORMAT_EXTENSIBLE``, với điều kiện định dạng mở rộng là ``KSDATAFORMAT_SUBTYPE_PCM``.

Mô-đun :mod:`!wave` định nghĩa hàm và ngoại lệ sau:


.. function:: open(file, mode=None)

   Nếu *tệp* là một chuỗi, hãy mở tệp có tên đó; nếu không, hãy coi đó là một đối tượng giống tệp. *mode* có thể là:

   ``'rb'``
      Chế độ chỉ đọc.

   ``'wb'``
      Chế độ chỉ ghi.

   Lưu ý rằng chế độ này không cho phép đọc/ghi các tệp WAV.

   Một *mode* với ``'rb'`` sẽ trả về một đối tượng :class:`Wave_read`, trong khi một *mode* với ``'wb'`` sẽ trả về một đối tượng :class:`Wave_write`. Nếu *mode* bị bỏ qua và một đối tượng giống tệp được truyền vào dưới dạng *file*, ``file.mode`` được sử dụng làm giá trị mặc định cho *mode*.

   Nếu bạn truyền vào một đối tượng giống tệp, đối tượng wave sẽ không đóng đối tượng đó khi phương thức ``close()`` được gọi; người gọi có trách nhiệm đóng đối tượng tệp.

   Hàm :func:`.open` có thể được sử dụng trong câu lệnh :keyword:`with`. Khi khối :keyword:`!with` hoàn tất, :meth:`Wave_read.close` hoặc
   phương thức :meth:`Wave_write.close` được gọi.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các tệp không thể seek.

.. exception:: Error

   Một lỗi được phát sinh khi một thao tác là không thể thực hiện do vi phạm đặc tả WAV hoặc gặp hạn chế trong quá trình triển khai.


.. _wave-read-objects:

Đối tượng Wave_read
-------------------

.. class:: Wave_read

   Đọc một tệp WAV.

   Các đối tượng Wave_read, được trả về bởi :func:`.open`, có các phương thức sau:


   .. method:: close()

      Đóng stream nếu stream được mở bởi :mod:`!wave`, đồng thời khiến thực thể không thể sử dụng được. Thao tác này được tự động gọi khi đối tượng được thu gom.


   .. method:: getnchannels()

      Trả về số kênh âm thanh (``1`` cho mono, ``2`` cho stereo).


   .. method:: getsampwidth()

      Trả về độ rộng mẫu tính bằng byte.


   .. method:: getframerate()

      Trả về tần số lấy mẫu.


   .. method:: getnframes()

      Trả về số lượng khung âm thanh.


   .. method:: getcomptype()

      Trả về kiểu nén (``'NONE'`` là kiểu duy nhất được hỗ trợ).


   .. method:: getcompname()

      Phiên bản dễ đọc của :meth:`getcomptype`. Thông thường, ``'not compressed'`` tương ứng với ``'NONE'``.


   .. method:: getparams()

      Trả về một :func:`~collections.namedtuple` ``(nchannels, sampwidth, framerate, nframes, comptype, compname)``, tương đương với đầu ra của các phương thức ``get*()``.


   .. method:: readframes(n)

      Đọc và trả về nhiều nhất *n* khung âm thanh dưới dạng một đối tượng :class:`bytes`.


   .. method:: rewind()

      Đưa con trỏ tệp về đầu luồng âm thanh.

   Hai phương thức sau được định nghĩa để tương thích với mô-đun :mod:`!aifc` cũ và không thực hiện điều gì đáng chú ý.


   .. method:: getmarkers()

      Trả về ``None``.

      .. deprecated-removed:: 3.13 3.15
         Phương thức này chỉ tồn tại để tương thích với mô-đun :mod:`!aifc`, mô-đun đã bị xóa trong Python 3.13.


   .. method:: getmark(id)

      Phát sinh lỗi.

      .. deprecated-removed:: 3.13 3.15
         Phương thức này chỉ tồn tại để tương thích với mô-đun :mod:`!aifc`, mô-đun đã bị xóa trong Python 3.13.

   Hai phương thức sau định nghĩa một thuật ngữ "vị trí" tương thích với nhau và phụ thuộc vào cách triển khai trong các trường hợp khác.


   .. method:: setpos(pos)

      Đặt con trỏ tệp tại vị trí được chỉ định.


   .. method:: tell()

      Trả về vị trí hiện tại của con trỏ tệp.


.. _wave-write-objects:

Đối tượng Wave_write
--------------------

.. class:: Wave_write

   Ghi tệp WAV.

   Các đối tượng Wave_write, được trả về bởi :func:`.open`.

   Đối với các luồng đầu ra có thể seek, header ``wave`` sẽ tự động được cập nhật để phản ánh số frame thực tế đã ghi. Đối với các luồng không thể seek, giá trị *nframes* phải chính xác khi dữ liệu frame đầu tiên được ghi. Có thể đạt được giá trị *nframes* chính xác bằng cách gọi
   :meth:`setnframes` hoặc :meth:`setparams` với số frame sẽ được ghi trước khi gọi :meth:`close`, sau đó dùng :meth:`writeframesraw` để ghi dữ liệu frame; hoặc gọi :meth:`writeframes` với toàn bộ dữ liệu frame cần ghi. Trong trường hợp sau, :meth:`writeframes` sẽ tính số frame trong dữ liệu và đặt *nframes* tương ứng trước khi ghi dữ liệu frame.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các tệp không thể seek.

   Các đối tượng Wave_write có những phương thức sau:

   .. method:: close()

      Hãy đảm bảo *nframes* là chính xác và đóng tệp nếu tệp được mở bởi
      :mod:`!wave`. Phương thức này được gọi khi đối tượng được thu gom. Phương thức sẽ phát sinh ngoại lệ nếu luồng đầu ra không thể seek và *nframes* không khớp với số frame thực tế đã ghi.


   .. method:: setnchannels(n)

      Thiết lập số kênh.


   .. method:: getnchannels()

      Trả về số kênh.


   .. method:: setsampwidth(n)

      Thiết lập độ rộng mẫu thành *n* byte.


   .. method:: getsampwidth()

      Trả về độ rộng mẫu theo byte.


   .. method:: setframerate(n)

      Đặt tốc độ khung hình thành *n*.

      .. versionchanged:: 3.2
         Giá trị đầu vào không phải số nguyên của phương thức này sẽ được làm tròn đến số nguyên gần nhất.


   .. method:: getframerate()

      Trả về tốc độ khung hình.


   .. method:: setnframes(n)

      Đặt số lượng khung hình thành *n*. Giá trị này sẽ được thay đổi sau nếu số lượng khung hình thực sự được ghi khác với giá trị đã đặt (lần thử cập nhật này sẽ gây ra lỗi nếu output stream không hỗ trợ seek).


   .. method:: getnframes()

      Trả về số lượng khung hình âm thanh đã được ghi cho đến thời điểm hiện tại.


   .. method:: setcomptype(type, name)

      Đặt kiểu nén và mô tả. Hiện tại, chỉ hỗ trợ kiểu nén ``NONE``, nghĩa là không nén.


   .. method:: getcomptype()

      Trả về kiểu nén (``'NONE'``).


   .. method:: getcompname()

      Trả về tên kiểu nén ở dạng dễ đọc.


   .. method:: setparams(tuple)

      *tuple* phải là ``(nchannels, sampwidth, framerate, nframes, comptype, compname)``, với các giá trị hợp lệ cho những phương thức ``set*()``. Thiết lập tất cả tham số.


   .. method:: getparams()

      Trả về một :func:`~collections.namedtuple` ``(nchannels, sampwidth, framerate, nframes, comptype, compname)`` chứa các tham số đầu ra hiện tại.


   .. method:: tell()

      Trả về vị trí hiện tại trong tệp, với cùng lưu ý như đối với các phương thức
      :meth:`Wave_read.tell` và :meth:`Wave_read.setpos`.


   .. method:: writeframesraw(data)

      Ghi các frame âm thanh mà không điều chỉnh *nframes*.

      .. versionchanged:: 3.4
         Bất kỳ :term:`bytes-like object` nào hiện được chấp nhận.


   .. method:: writeframes(data)

      Ghi các frame âm thanh và đảm bảo *nframes* là chính xác. Thao tác này sẽ gây ra lỗi nếu output stream không hỗ trợ seek và tổng số frame đã được ghi sau khi *data* được ghi không khớp với giá trị *nframes* đã đặt trước đó.

      .. versionchanged:: 3.4
         Bất kỳ :term:`bytes-like object` nào hiện được chấp nhận.

      Lưu ý rằng việc đặt bất kỳ tham số nào sau khi gọi :meth:`writeframes` hoặc :meth:`writeframesraw` là không hợp lệ, và mọi nỗ lực thực hiện việc đó sẽ gây ra
      :exc:`wave.Error`.
