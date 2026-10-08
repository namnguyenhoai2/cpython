.. _filesys:

***********************
Truy cập tệp và thư mục
***********************

Các mô-đun được mô tả trong chương này xử lý các tệp và thư mục trên đĩa. Ví dụ: có các mô-đun để đọc thuộc tính của tệp, thao tác với đường dẫn theo cách portable và tạo tệp tạm thời. Danh sách đầy đủ các mô-đun trong chương này là:


.. toctree::

   pathlib.rst
   os.path.rst
   stat.rst
   filecmp.rst
   tempfile.rst
   glob.rst
   fnmatch.rst
   linecache.rst
   shutil.rst


.. seealso::

   Mô-đun :mod:`os`
      Các giao diện hệ điều hành, bao gồm các hàm làm việc với tệp ở mức thấp hơn các đối tượng :term:`file objects <file object>` của Python.

   Mô-đun :mod:`io`
      Thư viện I/O tích hợp sẵn của Python, bao gồm cả các lớp trừu tượng và một số lớp cụ thể như I/O tệp.

   Hàm tích hợp sẵn :func:`open`
      Cách tiêu chuẩn để mở tệp nhằm đọc và ghi bằng Python.
