:mod:`!pyclbr` --- Hỗ trợ trình duyệt mô-đun Python
===================================================

.. module:: pyclbr
   :synopsis: Hỗ trợ trích xuất thông tin cho trình duyệt mô-đun Python.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/pyclbr.py`

--------------

Mô-đun :mod:`!pyclbr` cung cấp thông tin hạn chế về các hàm, lớp và phương thức được định nghĩa trong một mô-đun được viết bằng Python. Thông tin này đủ để triển khai một trình duyệt mô-đun. Thông tin được trích xuất từ mã nguồn Python thay vì bằng cách import mô-đun, vì vậy mô-đun này an toàn khi sử dụng với mã không đáng tin cậy. Hạn chế này khiến không thể sử dụng mô-đun này với các mô-đun không được triển khai bằng Python, bao gồm tất cả các mô-đun mở rộng chuẩn và tùy chọn.


.. function:: readmodule(module, path=None)

   Trả về một dictionary ánh xạ tên lớp cấp mô-đun tới các mô tả lớp. Nếu có thể, các mô tả cho những lớp cơ sở được import cũng được đưa vào. Tham số *module* là một chuỗi chứa tên của mô-đun cần đọc; tên này có thể là tên của một mô-đun trong một package. Nếu được cung cấp, *path* là một chuỗi các đường dẫn thư mục được thêm vào trước ``sys.path``, vốn được dùng để định vị mã nguồn mô-đun.

   Hàm này là giao diện ban đầu và chỉ được giữ lại để tương thích ngược. Hàm trả về một phiên bản đã lọc của nội dung sau.


.. function:: readmodule_ex(module, path=None)

   Trả về một cây dựa trên dictionary chứa mô tả hàm hoặc lớp cho mỗi hàm và lớp được định nghĩa trong mô-đun bằng một câu lệnh ``def`` hoặc ``class``. Dictionary được trả về ánh xạ tên hàm và lớp cấp mô-đun tới các mô tả tương ứng. Các đối tượng lồng nhau được đưa vào dictionary children của đối tượng cha. Giống như readmodule, *module* chỉ định mô-đun cần đọc và *path* được thêm vào trước sys.path. Nếu mô-đun đang được đọc là một package, dictionary được trả về có một khóa ``'__path__'`` với giá trị là danh sách chứa đường dẫn tìm kiếm của package.

.. versionadded:: 3.7
   Các descriptor dành cho những định nghĩa lồng nhau. Chúng được truy cập thông qua attribute children mới. Mỗi descriptor có một attribute parent mới.

Các descriptor được những hàm này trả về là các instance của các class Function và Class. Người dùng không cần tự tạo các instance của những class này.


.. _pyclbr-function-objects:

Đối tượng hàm
-------------

.. class:: Function

   Các instance của class Function :class:`!Function` mô tả những hàm được định nghĩa bằng các câu lệnh def. Chúng có các attribute sau:


   .. attribute:: file

      Tên tệp chứa định nghĩa của hàm.


   .. attribute:: module

      Tên module định nghĩa hàm được mô tả.


   .. attribute:: name

      Tên của hàm.


   .. attribute:: lineno

      Số dòng trong tệp nơi phần định nghĩa bắt đầu.


   .. attribute:: parent

      Đối với các hàm cấp cao nhất, ``None``. Đối với các hàm lồng nhau, là hàm cha.

      .. versionadded:: 3.7


   .. attribute:: children

      Một ánh xạ :class:`dictionary <dict>` tên với các descriptor cho các hàm và lớp lồng nhau.

      .. versionadded:: 3.7


   .. attribute:: is_async

      ``True`` đối với các hàm được định nghĩa bằng tiền tố
      :keyword:`async <async def>` tiền tố, ``False`` nếu không.

      .. versionadded:: 3.10


.. _pyclbr-class-objects:

Đối tượng lớp
-------------

.. class:: Class

   Các thực thể Class :class:`!Class` mô tả những lớp được định nghĩa bằng các câu lệnh class. Chúng có các thuộc tính giống như :class:`Functions <Function>` và thêm hai thuộc tính nữa.


   .. attribute:: file

      Tên tệp trong đó lớp được định nghĩa.


   .. attribute:: module

      Tên module định nghĩa lớp được mô tả.


   .. attribute:: name

      Tên của lớp.


   .. attribute:: lineno

      Số dòng trong tệp nơi định nghĩa bắt đầu.


   .. attribute:: parent

      Đối với các lớp cấp cao nhất, ``None``. Đối với các lớp lồng nhau, lớp cha.

      .. versionadded:: 3.7


   .. attribute:: children

      Một dictionary ánh xạ tên tới các descriptor của những hàm và lớp lồng nhau.

      .. versionadded:: 3.7


   .. attribute:: super

      Danh sách các đối tượng :class:`!Class` mô tả các lớp cơ sở trực tiếp của lớp đang được mô tả. Các lớp được nêu tên là lớp cha nhưng không thể được tìm thấy bằng :func:`readmodule_ex` sẽ được liệt kê dưới dạng một chuỗi chứa tên lớp thay vì dưới dạng
      Các đối tượng :class:`!Class`.


   .. attribute:: methods

      Một :class:`dictionary <dict>` ánh xạ tên phương thức tới số dòng. Có thể suy ra điều này từ từ điển :attr:`children` mới hơn, nhưng vẫn được giữ lại để đảm bảo khả năng tương thích ngược.
