:mod:`!winsound` --- Giao diện phát âm thanh cho Windows
========================================================

.. module:: winsound
   :synopsis: Truy cập vào cơ chế phát âm thanh cho Windows.

.. moduleauthor:: Toby Dickenson <htrd90@zepler.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

--------------

Mô-đun :mod:`!winsound` cung cấp quyền truy cập vào cơ chế phát âm thanh cơ bản do các nền tảng Windows cung cấp. Mô-đun này bao gồm các hàm và một số hằng số.

.. availability:: Windows.


.. function:: Beep(frequency, duration)

   Phát tiếng bíp từ loa của PC. Tham số *frequency* chỉ định tần số của âm thanh, tính bằng hertz, và phải nằm trong khoảng từ 37 đến 32.767. Tham số *duration* chỉ định số mili giây mà âm thanh sẽ kéo dài. Nếu hệ thống không thể phát tiếng bíp từ loa, :exc:`RuntimeError` sẽ được phát sinh.


.. function:: PlaySound(sound, flags)

   Gọi hàm :c:func:`!PlaySound` bên dưới từ Platform API. Tham số *sound* có thể là tên tệp, bí danh âm thanh hệ thống, dữ liệu âm thanh dưới dạng một
   :term:`bytes-like object`, hoặc ``None``. Cách diễn giải tham số này phụ thuộc vào giá trị của *flags*, có thể là sự kết hợp các hằng số được mô tả dưới đây bằng phép OR theo bit. Nếu tham số *sound* là ``None``, mọi âm thanh dạng waveform đang phát sẽ bị dừng. Nếu hệ thống cho biết có lỗi, :exc:`RuntimeError` sẽ được phát sinh.


.. function:: MessageBeep(type=MB_OK)

   Gọi hàm :c:func:`!MessageBeep` bên dưới từ Platform API. Hàm này phát âm thanh như được chỉ định trong registry. Đối số *type* chỉ định âm thanh cần phát; các giá trị có thể là ``-1``, ``MB_ICONASTERISK``, ``MB_ICONEXCLAMATION``, ``MB_ICONHAND``, ``MB_ICONQUESTION`` và ``MB_OK``, tất cả đều được mô tả dưới đây. Giá trị ``-1`` tạo ra một "tiếng bíp đơn giản"; đây là phương án dự phòng cuối cùng nếu không thể phát âm thanh theo cách khác. Nếu hệ thống cho biết có lỗi, :exc:`RuntimeError` sẽ được phát sinh.


.. data:: SND_FILENAME

   Tham số *sound* là tên của một tệp WAV. Không sử dụng cùng với
   :const:`SND_ALIAS`.


.. data:: SND_ALIAS

   Tham số *sound* là tên liên kết âm thanh từ registry. Nếu registry không chứa tên đó, hãy phát âm thanh mặc định của hệ thống, trừ khi
   :const:`SND_NODEFAULT` cũng được chỉ định. Nếu không đăng ký âm thanh mặc định nào, hãy raise :exc:`RuntimeError`. Không sử dụng cùng với :const:`SND_FILENAME`.

   Tất cả các hệ thống Win32 đều hỗ trợ ít nhất những mục sau; hầu hết các hệ thống còn hỗ trợ nhiều mục khác:

   +-------------------------+-----------------------------------------+
   | :func:`PlaySound` *tên* | Tên Sound tương ứng trong Control Panel |
   +=========================+=========================================+
   | ``'SystemAsterisk'``    | Asterisk                                |
   +-------------------------+-----------------------------------------+
   | ``'SystemExclamation'`` | Dấu chấm than                           |
   +-------------------------+-----------------------------------------+
   | ``'SystemExit'``        | Thoát Windows                           |
   +-------------------------+-----------------------------------------+
   | ``'SystemHand'``        | Dừng nghiêm trọng                       |
   +-------------------------+-----------------------------------------+
   | ``'SystemQuestion'``    | Câu hỏi                                 |
   +-------------------------+-----------------------------------------+

   Ví dụ::

      import winsound
      # Phát âm thanh thoát Windows.
      winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

      # Có lẽ phát âm thanh mặc định của Windows, nếu có âm thanh nào được đăng ký (vì
      # "*" có lẽ không phải là tên đã đăng ký của bất kỳ âm thanh nào).
      winsound.PlaySound("*", winsound.SND_ALIAS)


.. data:: SND_LOOP

   Phát âm thanh lặp lại. Cũng phải sử dụng cờ :const:`SND_ASYNC` để tránh chặn. Không thể sử dụng với :const:`SND_MEMORY`.


.. data:: SND_MEMORY

   Tham số *sound* của :func:`PlaySound` là một ảnh bộ nhớ của tệp WAV, dưới dạng
   :term:`bytes-like object`.

   .. note::

      Module này không hỗ trợ phát từ ảnh bộ nhớ một cách bất đồng bộ, vì vậy việc kết hợp cờ này với :const:`SND_ASYNC` sẽ phát sinh :exc:`RuntimeError`.


.. data:: SND_PURGE

   Dừng phát tất cả các phiên bản của âm thanh được chỉ định.

   .. note::

      Cờ này không được hỗ trợ trên các nền tảng Windows hiện đại.


.. data:: SND_ASYNC

   Trả về ngay lập tức, cho phép âm thanh phát không đồng bộ.


.. data:: SND_NODEFAULT

   Nếu không tìm thấy âm thanh được chỉ định, không phát âm thanh mặc định của hệ thống.


.. data:: SND_NOSTOP

   Không ngắt các âm thanh hiện đang phát.


.. data:: SND_NOWAIT

   Trả về ngay lập tức nếu sound driver đang bận.

   .. note::

      Cờ này không được hỗ trợ trên các nền tảng Windows hiện đại.


.. data:: SND_APPLICATION

   Tham số *sound* là bí danh dành riêng cho ứng dụng trong registry. Có thể kết hợp flag này với flag :const:`SND_ALIAS` để chỉ định bí danh âm thanh do ứng dụng định nghĩa.


.. data:: SND_SENTRY

   Kích hoạt một sự kiện SoundSentry khi âm thanh được phát.

   .. versionadded:: 3.14


.. data:: SND_SYNC

   Âm thanh được phát đồng bộ. Đây là hành vi mặc định.

   .. versionadded:: 3.14


.. data:: SND_SYSTEM

   Gán âm thanh cho phiên âm thanh dành cho các âm thanh thông báo của hệ thống.

   .. versionadded:: 3.14


.. data:: MB_ICONASTERISK

   Phát âm thanh ``SystemDefault``.


.. data:: MB_ICONEXCLAMATION

   Phát âm thanh ``SystemExclamation``.


.. data:: MB_ICONHAND

   Phát âm thanh ``SystemHand``.


.. data:: MB_ICONQUESTION

   Phát âm thanh ``SystemQuestion``.


.. data:: MB_OK

   Phát âm thanh ``SystemDefault``.


.. data:: MB_ICONERROR

   Phát âm thanh ``SystemHand``.

   .. versionadded:: 3.14


.. data:: MB_ICONINFORMATION

   Phát âm thanh ``SystemDefault``.

   .. versionadded:: 3.14


.. data:: MB_ICONSTOP

   Phát âm thanh ``SystemHand``.

   .. versionadded:: 3.14


.. data:: MB_ICONWARNING

   Phát âm thanh ``SystemExclamation``.

   .. versionadded:: 3.14
