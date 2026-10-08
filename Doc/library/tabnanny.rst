:mod:`!tabnanny` --- Phát hiện thụt lề mơ hồ
============================================

.. module:: tabnanny
   :synopsis: Công cụ phát hiện các vấn đề liên quan đến khoảng trắng trong các tệp mã nguồn Python trong một cây thư mục.

.. moduleauthor:: Tim Peters <tim_one@users.sourceforge.net>
.. sectionauthor:: Peter Funk <pf@artcom-gmbh.de>

.. rudimentary documentation based on module comments

**Mã nguồn:** :source:`Lib/tabnanny.py`

--------------

Hiện tại, mô-đun này được thiết kế để gọi dưới dạng một script. Tuy nhiên, bạn có thể import mô-đun này vào một IDE và sử dụng hàm :func:`check` được mô tả bên dưới.

.. note::

   API do mô-đun này cung cấp có thể sẽ thay đổi trong các bản phát hành tương lai; những thay đổi đó có thể không tương thích ngược.


.. function:: check(file_or_dir)

   Nếu *file_or_dir* là một thư mục và không phải là liên kết tượng trưng, mô-đun sẽ đệ quy duyệt qua cây thư mục có tên là *file_or_dir*, kiểm tra tất cả các tệp :file:`.py` trên đường đi. Nếu *file_or_dir* là một tệp mã nguồn Python thông thường, tệp đó sẽ được kiểm tra các vấn đề liên quan đến khoảng trắng. Các thông báo chẩn đoán được ghi vào đầu ra chuẩn bằng hàm :func:`print`.


.. data:: verbose

   Cờ cho biết có in các thông báo chi tiết hay không. Cờ này được tăng lên bởi tùy chọn ``-v`` nếu được gọi dưới dạng một script.


.. data:: filename_only

   Cờ cho biết có chỉ in tên tệp của các tệp chứa vấn đề liên quan đến khoảng trắng hay không. Cờ này được đặt thành true bởi tùy chọn ``-q`` nếu được gọi dưới dạng một script.


.. exception:: NannyNag

   Được :func:`process_tokens` phát sinh khi phát hiện thụt đầu dòng không rõ ràng. Được bắt và xử lý trong :func:`check`.


.. function:: process_tokens(tokens)

   Hàm này được :func:`check` sử dụng để xử lý các token được tạo bởi
   module :mod:`tokenize`.

.. XXX document errprint, format_witnesses, Whitespace, check_equal, indents,
   reset_globals


.. seealso::

   Module :mod:`tokenize`
      Trình quét từ vựng cho mã nguồn Python.
