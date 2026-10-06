Gói :mod:`!compression`
=======================

.. module:: compression

.. versionadded:: 3.14

Gói :mod:`!compression` chứa các mô-đun nén chính thức, cung cấp các interface cho một số thuật toán nén khác nhau. Một số mô-đun trong số này trước đây từng được cung cấp dưới dạng các mô-đun riêng biệt; vì lý do tương thích, chúng sẽ tiếp tục khả dụng dưới tên ban đầu và sẽ không bị xóa nếu chưa trải qua một chu kỳ ngừng hỗ trợ. Việc sử dụng các mô-đun trong
:mod:`!compression` được khuyến khích khi phù hợp.

* :mod:`!compression.bz2` -- Tái xuất :mod:`bz2`
* :mod:`!compression.gzip` -- Tái xuất :mod:`gzip`
* :mod:`!compression.lzma` -- Tái xuất :mod:`lzma`
* :mod:`!compression.zlib` -- Tái xuất :mod:`zlib`
* :mod:`compression.zstd` -- Bộ bao bọc cho thư viện nén Zstandard

