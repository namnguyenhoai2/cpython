.. _ipc:

*************************************
Mạng và giao tiếp giữa các tiến trình
*************************************

Các module được mô tả trong chương này cung cấp các cơ chế cho mạng và giao tiếp giữa các tiến trình.

Một số module chỉ hoạt động với hai tiến trình trên cùng một máy, ví dụ như
:mod:`signal` và :mod:`mmap`. Các module khác hỗ trợ những giao thức mạng mà hai hoặc nhiều tiến trình có thể sử dụng để giao tiếp giữa các máy.

Danh sách các module được mô tả trong chương này là:


.. toctree::
   :maxdepth: 1

   asyncio.rst
   socket.rst
   ssl.rst
   select.rst
   selectors.rst
   signal.rst
   mmap.rst
