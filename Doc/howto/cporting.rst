.. highlight:: c

.. _cporting-howto:

***************************************
Chuyển các mô-đun mở rộng sang Python 3
***************************************

Chúng tôi khuyến nghị các tài nguyên sau để chuyển các mô-đun mở rộng sang Python 3:

* Chương `Migrating C extensions <Migrating C extensions_>`_ trong *Supporting Python 3: An in-depth guide*, một cuốn sách hướng dẫn việc chuyển từ Python 2 sang Python 3 nói chung, sẽ hướng dẫn bạn đọc cách chuyển một mô-đun mở rộng.
* `Porting guide <Porting guide_>`_ của dự án *py3c* đưa ra các đề xuất có định hướng kèm theo mã hỗ trợ.
* :ref:`Recommended third party tools <c-api-tools>` cung cấp các lớp trừu tượng trên C API của Python. Nhìn chung, các phần mở rộng cần được viết lại để sử dụng một trong các công cụ này, nhưng sau đó thư viện sẽ xử lý những khác biệt giữa các phiên bản và bản triển khai Python khác nhau.

.. _Migrating C extensions: http://python3porting.com/cextensions.html
.. _Porting guide: https://py3c.readthedocs.io/en/latest/guide.html
