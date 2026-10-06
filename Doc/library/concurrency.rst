.. _concurrency:

******************
Thực thi đồng thời
******************

Các module được mô tả trong chương này cung cấp khả năng hỗ trợ thực thi mã đồng thời. Việc chọn công cụ phù hợp sẽ phụ thuộc vào tác vụ cần thực hiện (phụ thuộc CPU hay phụ thuộc I/O) và phong cách phát triển được ưu tiên (điều phối đa nhiệm hợp tác theo hướng sự kiện hay đa nhiệm đan xen cưỡng chế). Dưới đây là tổng quan:


.. toctree::

   threading.rst
   multiprocessing.rst
   multiprocessing.shared_memory.rst
   concurrent.rst
   concurrent.futures.rst
   concurrent.interpreters.rst
   subprocess.rst
   sched.rst
   queue.rst
   contextvars.rst


Sau đây là các module hỗ trợ cho một số dịch vụ nêu trên:

.. toctree::

   _thread.rst
