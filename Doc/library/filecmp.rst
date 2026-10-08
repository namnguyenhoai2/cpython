:mod:`!filecmp` --- So sánh tệp và thư mục
==========================================

.. module:: filecmp
   :synopsis: So sánh tệp một cách hiệu quả.

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/filecmp.py`

--------------

Mô-đun :mod:`!filecmp` định nghĩa các hàm để so sánh tệp và thư mục, với nhiều mức đánh đổi tùy chọn giữa thời gian và độ chính xác. Để so sánh tệp, hãy xem thêm mô-đun :mod:`difflib`.

Mô-đun :mod:`!filecmp` định nghĩa các hàm sau:


.. function:: cmp(f1, f2, shallow=True)

   So sánh các tệp có tên *f1* và *f2*, trả về ``True`` nếu chúng có vẻ giống nhau, và ``False`` nếu không.

   Nếu *shallow* là true và :func:`os.stat` chữ ký (loại tệp, kích thước và thời gian sửa đổi) của cả hai tệp giống hệt nhau, các tệp được xem là giống nhau.

   Nếu không, các tệp được xem là khác nhau nếu kích thước hoặc nội dung của chúng khác nhau.

   Lưu ý rằng hàm này không gọi chương trình bên ngoài nào, nhờ đó có tính khả chuyển và hiệu quả.

   Hàm này sử dụng bộ nhớ đệm cho các lần so sánh trước đó và kết quả, với các mục trong bộ nhớ đệm sẽ bị vô hiệu hóa nếu thông tin :func:`os.stat` của tệp thay đổi. Có thể xóa toàn bộ bộ nhớ đệm bằng :func:`clear_cache`.


.. function:: cmpfiles(a, b, common, shallow=True)

   So sánh các tệp trong hai thư mục *a* và *b* có tên được cung cấp bởi *common*.

   Trả về ba danh sách tên tệp: *match*, *mismatch*, *errors*. *match* chứa danh sách các tệp khớp nhau, *mismatch* chứa tên của các tệp không khớp, còn *errors* liệt kê tên các tệp không thể so sánh. Các tệp được liệt kê trong *errors* nếu chúng không tồn tại trong một trong hai thư mục, người dùng không có quyền đọc chúng hoặc không thể thực hiện so sánh vì một lý do nào khác.

   Tham số *shallow* có ý nghĩa và giá trị mặc định giống như trong
   :func:`filecmp.cmp`.

   Ví dụ: ``cmpfiles('a', 'b', ['c', 'd/e'])`` sẽ so sánh ``a/c`` với ``b/c`` và ``a/d/e`` với ``b/d/e``. ``'c'`` và ``'d/e'`` sẽ lần lượt nằm trong một trong ba danh sách được trả về.


.. function:: clear_cache()

   Xóa bộ nhớ đệm filecmp. Điều này có thể hữu ích nếu một tệp được so sánh ngay sau khi được sửa đổi đến mức thời điểm sửa đổi nằm trong độ phân giải mtime của hệ thống tệp bên dưới.

   .. versionadded:: 3.4


.. _dircmp-objects:

Lớp :class:`dircmp`
-------------------

.. class:: dircmp(a, b, ignore=None, hide=None, *, shallow=True)

   Tạo một đối tượng so sánh thư mục mới để so sánh các thư mục *a* và *b*.  *ignore* là một danh sách các tên cần bỏ qua và mặc định là
   :const:`filecmp.DEFAULT_IGNORES`.  *hide* là một danh sách các tên cần ẩn và mặc định là ``[os.curdir, os.pardir]``.

   Lớp :class:`dircmp` so sánh các tệp bằng cách thực hiện các phép so sánh *shallow* như được mô tả cho :func:`filecmp.cmp` theo mặc định bằng cách sử dụng tham số *shallow*.

   .. versionchanged:: 3.13

      Đã thêm tham số *shallow*.

   Lớp :class:`dircmp` cung cấp các phương thức sau:

   .. method:: report()

      In (to :data:`sys.stdout`), in một phép so sánh giữa *a* và *b*.

   .. method:: report_partial_closure()

      In một phép so sánh giữa *a* và *b*, cùng các thư mục con trực tiếp chung.

   .. method:: report_full_closure()

      In một phép so sánh giữa *a* và *b*, cùng các thư mục con chung (theo cách đệ quy).

   Lớp :class:`dircmp` cung cấp một số thuộc tính thú vị có thể được dùng để lấy nhiều thông tin khác nhau về các cây thư mục đang được so sánh.

   Lưu ý rằng thông qua các hook :meth:`~object.__getattr__`, mọi thuộc tính đều được tính toán một cách lười biếng, vì vậy sẽ không có bất lợi về tốc độ nếu chỉ sử dụng những thuộc tính có chi phí tính toán thấp.


   .. attribute:: left

      Thư mục *a*.


   .. attribute:: right

      Thư mục *b*.


   .. attribute:: left_list

      Các tệp và thư mục con trong *a*, được lọc theo *hide* và *ignore*.


   .. attribute:: right_list

      Các tệp và thư mục con trong *b*, được lọc theo *hide* và *ignore*.


   .. attribute:: common

      Các tệp và thư mục con có trong cả *a* và *b*.


   .. attribute:: left_only

      Các tệp và thư mục con chỉ có trong *a*.


   .. attribute:: right_only

      Các tệp và thư mục con chỉ có trong *b*.


   .. attribute:: common_dirs

      Các thư mục con có trong cả *a* và *b*.


   .. attribute:: common_files

      Các tệp có trong cả *a* và *b*.


   .. attribute:: common_funny

      Tên xuất hiện trong cả *a* và *b*, với kiểu khác nhau giữa các thư mục, hoặc tên mà :func:`os.stat` báo lỗi.


   .. attribute:: same_files

      Các tệp giống hệt nhau trong cả *a* và *b*, được xác định bằng toán tử so sánh tệp của lớp.


   .. attribute:: diff_files

      Các tệp có trong cả *a* và *b*, nhưng nội dung khác nhau theo toán tử so sánh tệp của lớp.


   .. attribute:: funny_files

      Các tệp có trong cả *a* và *b*, nhưng không thể so sánh.


   .. attribute:: subdirs

      Một dictionary ánh xạ các tên trong :attr:`common_dirs` tới các đối tượng :class:`dircmp` (hoặc các đối tượng MyDirCmp nếu đối tượng này có kiểu MyDirCmp, một lớp con của :class:`dircmp`).

      .. versionchanged:: 3.10
         Trước đây, các mục luôn là các đối tượng :class:`dircmp`. Hiện nay, các mục có cùng kiểu với *self*, nếu *self* là lớp con của
         :class:`dircmp`.

.. data:: DEFAULT_IGNORES

   .. versionadded:: 3.4

   Danh sách các thư mục bị :class:`dircmp` bỏ qua theo mặc định.


Dưới đây là một ví dụ đơn giản sử dụng thuộc tính ``subdirs`` để tìm kiếm đệ quy qua hai thư mục nhằm hiển thị các tệp chung và khác nhau::

    >>> from filecmp import dircmp
    >>> def print_diff_files(dcmp):
    ...     for name in dcmp.diff_files:
    ...         print("diff_file %s found in %s and %s" % (name, dcmp.left,
    ...               dcmp.right))
    ...     for sub_dcmp in dcmp.subdirs.values():
    ...         print_diff_files(sub_dcmp)
    ...
    >>> dcmp = dircmp('dir1', 'dir2') # doctest: +SKIP
    >>> print_diff_files(dcmp) # doctest: +SKIP

