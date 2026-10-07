Dự kiến loại bỏ trong Python 3.18
---------------------------------

* :mod:`decimal`:

  * Bộ chỉ định định dạng không chuẩn và không được ghi tài liệu :class:`~decimal.Decimal` format specifier ``'N'``, vốn chỉ được hỗ trợ trong phần triển khai C của :mod:`!decimal` mô-đun, đã không còn được dùng kể từ Python 3.13. (Đóng góp của Serhiy Storchaka trong :gh:`89902`.)
