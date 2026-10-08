.. _security-warnings:

.. index:: single: security considerations

Các lưu ý về bảo mật
====================

Các mô-đun sau có những lưu ý cụ thể về bảo mật:

* :mod:`base64`: :ref:`các lưu ý về bảo mật của base64 <base64-security>` trong
  :rfc:`4648`
* :mod:`hashlib`: :ref:`tất cả các constructor đều nhận một đối số chỉ dùng dưới dạng từ khóa "usedforsecurity" để vô hiệu hóa các thuật toán không an toàn và bị chặn đã biết <hashlib-usedforsecurity>`
* :mod:`http.server` không phù hợp để sử dụng trong môi trường production, chỉ triển khai các kiểm tra bảo mật cơ bản. Xem :ref:`các lưu ý về bảo mật <http.server-security>`.
* :mod:`logging`: :ref:`Cấu hình Logging sử dụng eval() <logging-eval-security>`
* :mod:`multiprocessing`: :ref:`Connection.recv() sử dụng pickle <multiprocessing-recv-pickle-security>`
* :mod:`pickle`: :ref:`Hạn chế các đối tượng toàn cục trong pickle <pickle-restrict>`
* :mod:`random` không nên được sử dụng cho mục đích bảo mật; thay vào đó, hãy sử dụng :mod:`secrets`
* :mod:`shelve`: :ref:`shelve dựa trên pickle và do đó không phù hợp để xử lý các nguồn không đáng tin cậy <shelve-security>`
* :mod:`ssl`: :ref:`Các vấn đề cần cân nhắc về bảo mật SSL/TLS <ssl-security>`
* :mod:`subprocess`: :ref:`Các vấn đề cần cân nhắc về bảo mật của Subprocess <subprocess-security>`
* :mod:`tempfile`: :ref:`mktemp không được dùng nữa do dễ bị tấn công bởi các điều kiện tranh chấp <tempfile-mktemp-deprecated>`
* :mod:`xml`: :ref:`Bảo mật XML <xml-security>`
* :mod:`zipfile`: :ref:`các tệp .zip được chuẩn bị một cách độc hại có thể gây cạn kiệt dung lượng ổ đĩa <zipfile-resources-limitations>`

Có thể sử dụng tùy chọn dòng lệnh :option:`-I` để chạy Python ở chế độ cô lập. Khi không thể sử dụng tùy chọn này, có thể sử dụng tùy chọn :option:`-P` hoặc
biến môi trường :envvar:`PYTHONSAFEPATH` để không thêm vào đầu :data:`sys.path` một đường dẫn có khả năng không an toàn, chẳng hạn như thư mục hiện tại, thư mục chứa tập lệnh hoặc một chuỗi rỗng.
