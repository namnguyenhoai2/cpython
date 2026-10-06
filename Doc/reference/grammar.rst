.. _full-grammar-specification:

Đặc tả ngữ pháp đầy đủ
======================

Đây là ngữ pháp Python đầy đủ, được suy ra trực tiếp từ ngữ pháp được sử dụng để tạo trình phân tích cú pháp CPython (xem :source:`Grammar/python.gram`). Phiên bản này lược bỏ các chi tiết liên quan đến việc sinh mã và khôi phục lỗi.

Ký hiệu được sử dụng ở đây giống như trong tài liệu trước đó và được mô tả trong phần :ref:`notation <notation>`, ngoại trừ một điểm phức tạp bổ sung:

* ``~`` ("cut"): cam kết sử dụng alternative hiện tại; quy tắc sẽ thất bại nếu alternative không phân tích cú pháp được

  Python chủ yếu sử dụng cut để tối ưu hóa hoặc cải thiện thông báo lỗi. Trong danh sách bên dưới, chúng thường có vẻ không cần thiết.

  .. see gh-143054, and CutValidator in the source, if you want to change this:

  Hiện tại, cut không xuất hiện bên trong dấu ngoặc đơn, dấu ngoặc vuông, lookahead và các cấu trúc tương tự. Hành vi của chúng trong các ngữ cảnh này được cố ý để ở trạng thái không xác định.

.. literalinclude:: ../../Grammar/python.gram
  :language: peg
