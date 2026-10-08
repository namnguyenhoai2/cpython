:mod:`!zipimport` --- Nhập các mô-đun từ kho lưu trữ Zip
========================================================

.. module:: zipimport
   :synopsis: Hỗ trợ nhập các mô-đun Python từ kho lưu trữ ZIP.

.. moduleauthor:: Just van Rossum <just@letterror.com>

**Mã nguồn:** :source:`Lib/zipimport.py`

--------------

Mô-đun này bổ sung khả năng nhập các mô-đun Python (:file:`\*.py`,
:file:`\*.pyc`) và các package từ kho lưu trữ định dạng ZIP. Thông thường không cần sử dụng rõ ràng mô-đun :mod:`!zipimport`; cơ chế :keyword:`import` tích hợp sẵn sẽ tự động sử dụng mô-đun này cho các mục :data:`sys.path` là những đường dẫn đến kho lưu trữ ZIP.

Thông thường, :data:`sys.path` là một danh sách các tên thư mục dưới dạng chuỗi. Mô-đun này cũng cho phép một mục của :data:`sys.path` là một chuỗi chỉ định tên của tệp lưu trữ ZIP. Kho lưu trữ ZIP có thể chứa cấu trúc thư mục con để hỗ trợ việc nhập package, và có thể chỉ định một đường dẫn bên trong kho lưu trữ để chỉ nhập từ một thư mục con. Ví dụ: đường dẫn :file:`example.zip/lib/` sẽ chỉ nhập từ thư mục con :file:`lib/` bên trong kho lưu trữ.

Kho lưu trữ ZIP có thể chứa bất kỳ tệp nào, nhưng các importer chỉ được gọi cho
:file:`.py` và :file:`.pyc` files. Không cho phép nhập ZIP các dynamic module (:file:`.pyd`, :file:`.so`). Lưu ý rằng nếu một archive chỉ chứa
:file:`.py` files, Python sẽ không cố sửa đổi archive bằng cách thêm file :file:`.pyc` tương ứng, nghĩa là nếu một ZIP archive không chứa các file :file:`.pyc`, việc import có thể khá chậm.

.. versionchanged:: 3.13
   ZIP64 được hỗ trợ

.. versionchanged:: 3.8
   Trước đây, các ZIP archive có archive comment không được hỗ trợ.

.. seealso::

   `Ghi chú ứng dụng PKZIP <https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT>`_
      Tài liệu về định dạng tệp ZIP do Phil Katz, người tạo ra định dạng và các thuật toán được sử dụng, viết.

   :pep:`273` - Nhập module từ các ZIP archive
      Được viết bởi James C. Ahlstrom, người cũng cung cấp một implementation. Python 2.3 tuân theo đặc tả trong :pep:`273`, nhưng sử dụng một implementation do Just van Rossum viết, sử dụng các import hook được mô tả trong :pep:`302`.

   :mod:`importlib` - Implementation của cơ chế import
      Package cung cấp các protocol liên quan để mọi importer triển khai.


Module này định nghĩa một exception:

.. exception:: ZipImportError

   Exception được các đối tượng zipimporter phát sinh. Đây là một subclass của :exc:`ImportError`, nên cũng có thể được bắt dưới dạng :exc:`ImportError`.


.. _zipimporter-objects:

Các đối tượng zipimporter
-------------------------

:class:`zipimporter` là class dùng để import các tệp ZIP.

.. class:: zipimporter(archivepath)

   Tạo một instance zipimporter mới. *archivepath* phải là đường dẫn đến một tệp ZIP hoặc đến một đường dẫn cụ thể bên trong tệp ZIP. Ví dụ: *archivepath* có giá trị :file:`foo/bar.zip/lib` sẽ tìm các module trong thư mục :file:`lib` bên trong tệp ZIP :file:`foo/bar.zip` (với điều kiện thư mục này tồn tại).

   :exc:`ZipImportError` được phát sinh nếu *archivepath* không trỏ đến một kho lưu trữ ZIP hợp lệ.

   .. versionchanged:: 3.12

      Các phương thức ``find_loader()`` và ``find_module()``, đã bị deprecated trong 3.10, hiện đã bị xóa. Thay vào đó, hãy sử dụng :meth:`find_spec`.

   .. method:: create_module(spec)

      Triển khai :meth:`importlib.abc.Loader.create_module` trả về
      :const:`None` để yêu cầu rõ ràng các ngữ nghĩa mặc định.

      .. versionadded:: 3.10


   .. method:: exec_module(module)

      Triển khai :meth:`importlib.abc.Loader.exec_module`.

      .. versionadded:: 3.10


   .. method:: find_spec(fullname, target=None)

      Một triển khai của :meth:`importlib.abc.PathEntryFinder.find_spec`.

      .. versionadded:: 3.10


   .. method:: get_code(fullname)

      Trả về đối tượng mã cho mô-đun được chỉ định. Phát sinh
      :exc:`ZipImportError` nếu không thể import mô-đun.


   .. method:: get_data(pathname)

      Trả về dữ liệu liên kết với *pathname*. Phát sinh :exc:`OSError` nếu không tìm thấy tệp.

      .. versionchanged:: 3.3
         :exc:`IOError` used to be raised, it is now an alias of :exc:`OSError`.


   .. method:: get_filename(fullname)

      Trả về giá trị mà ``__file__`` sẽ được gán nếu mô-đun được chỉ định được import. Phát sinh :exc:`ZipImportError` nếu không thể import mô-đun.

      .. versionadded:: 3.1


   .. method:: get_source(fullname)

      Trả về mã nguồn cho mô-đun được chỉ định. Phát sinh
      :exc:`ZipImportError` nếu không tìm thấy mô-đun, trả về
      :const:`None` nếu tệp lưu trữ có chứa mô-đun nhưng không có mã nguồn cho mô-đun đó.


   .. method:: is_package(fullname)

      Trả về ``True`` nếu module được chỉ định bởi *fullname* là một package. Phát sinh
      :exc:`ZipImportError` nếu không thể tìm thấy module.


   .. method:: load_module(fullname)

      Tải module được chỉ định bởi *fullname*. *fullname* phải là tên module đủ điều kiện (dạng dấu chấm). Trả về module đã import khi thành công và phát sinh :exc:`ZipImportError` khi thất bại.

      .. deprecated-removed:: 3.10 3.15

         Thay vào đó, sử dụng :meth:`exec_module`.


   .. method:: invalidate_caches()

      Xóa bộ nhớ đệm nội bộ chứa thông tin về các tệp được tìm thấy trong kho lưu trữ ZIP.

      .. versionadded:: 3.10


   .. attribute:: archive

      Tên tệp ZIP liên kết với importer, không bao gồm phần đường dẫn con nếu có.


   .. attribute:: prefix

      Đường dẫn con bên trong tệp ZIP nơi các module được tìm kiếm. Đây là chuỗi rỗng đối với các đối tượng zipimporter trỏ đến thư mục gốc của tệp ZIP.

   Các thuộc tính :attr:`archive` và :attr:`prefix`, khi kết hợp với dấu gạch chéo, tương đương với đối số *archivepath* ban đầu được truyền cho
   hàm khởi tạo :class:`zipimporter`.


.. _zipimport-examples:

Ví dụ
-----

Sau đây là một ví dụ nhập một mô-đun từ kho lưu trữ ZIP - lưu ý rằng
mô-đun :mod:`!zipimport` không được sử dụng một cách rõ ràng.

.. code-block:: shell-session

   $ unzip -l example_archive.zip
   Archive:  example_archive.zip
     Length     Date   Time    Name
    --------    ----   ----    ----
        8467  01-01-00 12:30   example.py
    --------                   -------
        8467                   1 file

.. code-block:: pycon

   >>> import sys
   >>> # Thêm kho lưu trữ vào đầu đường dẫn tìm kiếm mô-đun
   >>> sys.path.insert(0, 'example_archive.zip')
   >>> import example
   >>> example.__file__
   'example_archive.zip/example.py'

.. _`PKZIP Application Note`: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
