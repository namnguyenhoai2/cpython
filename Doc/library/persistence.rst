.. _persistence:

***********************
Lưu trữ dữ liệu lâu dài
***********************

Các module được mô tả trong chương này hỗ trợ lưu trữ dữ liệu Python dưới dạng bền vững trên đĩa. Các module :mod:`pickle` và :mod:`marshal` có thể chuyển nhiều kiểu dữ liệu Python thành một luồng byte, sau đó tạo lại các đối tượng từ những byte đó. Các module liên quan đến DBM hỗ trợ một nhóm định dạng tệp dựa trên bảng băm, dùng để lưu ánh xạ từ chuỗi sang các chuỗi khác.

Danh sách các module được mô tả trong chương này là:


.. toctree::

   pickle.rst
   copyreg.rst
   shelve.rst
   marshal.rst
   dbm.rst
   sqlite3.rst
