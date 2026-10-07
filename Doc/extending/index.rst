.. _extending-index:

########################################
Mở rộng và nhúng trình thông dịch Python
########################################

Tài liệu này mô tả cách viết các module bằng C hoặc C++ để mở rộng trình thông dịch Python bằng các module mới. Các module đó không chỉ có thể định nghĩa các hàm mới mà còn cả các kiểu đối tượng mới và các phương thức của chúng. Tài liệu cũng mô tả cách nhúng trình thông dịch Python vào một ứng dụng khác để sử dụng làm ngôn ngữ mở rộng. Cuối cùng, tài liệu trình bày cách biên dịch và liên kết các module mở rộng để chúng có thể được tải động (trong thời gian chạy) vào trình thông dịch, nếu hệ điều hành nền hỗ trợ tính năng này.

Tài liệu này giả định bạn có kiến thức cơ bản về C và Python. Để xem phần giới thiệu không chính thức về Python, hãy xem :ref:`tutorial-index`. :ref:`reference-index` đưa ra định nghĩa chính thức hơn về ngôn ngữ này. :ref:`builtins-index` ghi lại các hàm dựng sẵn và kiểu đối tượng, còn :ref:`library-index` ghi lại các module (cả module dựng sẵn và module được viết bằng Python) giúp ngôn ngữ này có phạm vi ứng dụng rộng rãi.

Để xem mô tả chi tiết về toàn bộ Python/C API, hãy xem tài liệu riêng
:ref:`c-api-index`.


Các công cụ bên thứ ba được khuyến nghị
=======================================

Hướng dẫn này chỉ đề cập đến các công cụ cơ bản để tạo extension được cung cấp trong phiên bản CPython này. Một số :ref:`công cụ bên thứ ba <c-api-tools>` cung cấp cả những phương pháp đơn giản hơn lẫn tinh vi hơn để tạo extension C và C++ cho Python.


Tạo extension mà không dùng công cụ bên thứ ba
==============================================

Phần này của tài liệu hướng dẫn trình bày cách tạo các phần mở rộng C và C++ mà không cần đến công cụ của bên thứ ba. Nội dung chủ yếu dành cho những người tạo ra các công cụ đó, thay vì là cách được khuyến nghị để bạn tự tạo phần mở rộng C của mình.

.. seealso::

   :pep:`489` -- Khởi tạo module phần mở rộng theo nhiều giai đoạn

.. toctree::
   :maxdepth: 2
   :numbered:

   extending.rst
   newtypes_tutorial.rst
   newtypes.rst
   building.rst
   windows.rst

Nhúng runtime CPython vào một ứng dụng lớn hơn
==============================================

Đôi khi, thay vì tạo một phần mở rộng chạy bên trong trình thông dịch Python với vai trò là ứng dụng chính, việc nhúng runtime CPython vào một ứng dụng lớn hơn sẽ phù hợp hơn. Phần này trình bày một số chi tiết liên quan đến việc thực hiện điều đó thành công.

.. toctree::
   :maxdepth: 2
   :numbered:

   embedding.rst
