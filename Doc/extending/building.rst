.. highlight:: c

.. _building:

******************************
Xây dựng phần mở rộng C và C++
******************************

Phần mở rộng C cho CPython là một thư viện dùng chung (ví dụ: tệp ``.so`` trên Linux, ``.pyd`` trên Windows), trong đó xuất một *hàm khởi tạo*.

Xem :ref:`extension-modules` để biết chi tiết.


.. highlight:: c

.. _install-index:
.. _setuptools-index:

Xây dựng phần mở rộng C và C++ bằng setuptools
==============================================


Việc xây dựng, đóng gói và phân phối các module mở rộng nên được thực hiện bằng các công cụ bên thứ ba, và nằm ngoài phạm vi của tài liệu này. Một công cụ phù hợp là Setuptools; bạn có thể xem tài liệu của công cụ này tại https://setuptools.pypa.io/en/latest/setuptools.html.

Mô-đun :mod:`distutils`, vốn được đưa vào thư viện chuẩn cho đến Python 3.12, hiện được duy trì như một phần của Setuptools.
