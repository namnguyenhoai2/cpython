:mod:`!linecache` --- Truy cập ngẫu nhiên các dòng văn bản
==========================================================

.. module:: linecache
   :synopsis: Cung cấp quyền truy cập ngẫu nhiên đến từng dòng trong các tệp văn bản.

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/linecache.py`

--------------

Mô-đun :mod:`!linecache` cho phép lấy bất kỳ dòng nào từ tệp mã nguồn Python, đồng thời cố gắng tối ưu nội bộ bằng cách sử dụng bộ nhớ đệm cho trường hợp phổ biến là đọc nhiều dòng từ cùng một tệp. Mô-đun :mod:`traceback` sử dụng chức năng này để truy xuất các dòng mã nguồn nhằm đưa vào traceback đã được định dạng.

Hàm :func:`tokenize.open` được sử dụng để mở tệp. Hàm này sử dụng :func:`tokenize.detect_encoding` để lấy encoding của tệp; nếu không có token encoding, encoding của tệp mặc định là UTF-8.

Mô-đun :mod:`!linecache` định nghĩa các hàm sau:


.. function:: getline(filename, lineno, module_globals=None)

   Lấy dòng *lineno* từ tệp có tên *filename*. Hàm này sẽ không bao giờ phát sinh ngoại lệ --- khi gặp lỗi, hàm sẽ trả về ``''`` (ký tự xuống dòng kết thúc sẽ được bao gồm đối với các dòng tìm thấy).

   .. index:: triple: module; search; path

   Nếu *filename* cho biết một frozen module (bắt đầu bằng ``'<frozen '``), hàm sẽ cố gắng lấy tên tệp thực từ ``module_globals['__file__']`` nếu *module_globals* không phải là ``None``.

   Nếu không tìm thấy tệp có tên *filename*, trước tiên hàm sẽ kiểm tra :pep:`302` ``__loader__`` trong *module_globals*. Nếu có loader như vậy và loader định nghĩa một phương thức ``get_source``, thì phương thức đó sẽ xác định các dòng mã nguồn (nếu ``get_source()`` trả về ``None``, thì ``''`` sẽ được trả về). Cuối cùng, nếu *filename* là tên tệp tương đối, nó sẽ được tìm kiếm tương ứng với các mục trong đường dẫn tìm kiếm module, ``sys.path``.

   .. versionchanged:: 3.14

      Hỗ trợ *filename* của các frozen module.


.. function:: clearcache()

   Xóa cache. Sử dụng hàm này nếu bạn không còn cần các dòng từ những tệp đã được đọc trước đó bằng :func:`getline`.


.. function:: checkcache(filename=None)

   Kiểm tra tính hợp lệ của cache. Sử dụng hàm này nếu các tệp trong cache có thể đã thay đổi trên đĩa và bạn cần phiên bản cập nhật. Nếu bỏ qua *filename*, hàm sẽ kiểm tra tất cả các mục trong cache.

.. function:: lazycache(filename, module_globals)

   Lưu đủ thông tin chi tiết về một module không dựa trên tệp để sau này có thể lấy các dòng của module đó qua :func:`getline`, ngay cả khi *module_globals* là ``None`` trong lần gọi sau. Điều này giúp trì hoãn việc I/O cho đến khi thực sự cần một dòng, mà không phải giữ các biến toàn cục của module vô thời hạn.

   .. versionadded:: 3.5

Ví dụ::

   >>> import linecache
   >>> linecache.getline(linecache.__file__, 8)
   'import sys\n'
