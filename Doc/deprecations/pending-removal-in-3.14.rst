Sắp bị loại bỏ trong Python 3.14
--------------------------------

* :mod:`argparse`: Các tham số *type*, *choices* và *metavar* của :class:`!argparse.BooleanOptionalAction` không còn được khuyến nghị sử dụng và sẽ bị loại bỏ trong 3.14. (Do Nikita Sobolev đóng góp trong :gh:`92248`.)

* :mod:`ast`: Các tính năng sau đây đã không còn được khuyến nghị sử dụng trong tài liệu kể từ Python 3.8, hiện khiến một :exc:`DeprecationWarning` được phát ra tại runtime khi chúng được truy cập hoặc sử dụng, và sẽ bị loại bỏ trong Python 3.14:

  * :class:`!ast.Num`
  * :class:`!ast.Str`
  * :class:`!ast.Bytes`
  * :class:`!ast.NameConstant`
  * :class:`!ast.Ellipsis`

  Hãy sử dụng :class:`ast.Constant` thay thế. (Do Serhiy Storchaka đóng góp trong :gh:`90953`.)

* :mod:`asyncio`:

  * Các lớp child watcher :class:`!asyncio.MultiLoopChildWatcher`,
    :class:`!asyncio.FastChildWatcher`, :class:`!asyncio.AbstractChildWatcher` và :class:`!asyncio.SafeChildWatcher` không còn được khuyến nghị sử dụng và sẽ bị loại bỏ trong Python 3.14. (Do Kumar Aditya đóng góp trong :gh:`94597`.)

  * :func:`!asyncio.set_child_watcher`, :func:`!asyncio.get_child_watcher`,
    :meth:`!asyncio.AbstractEventLoopPolicy.set_child_watcher` và
    :meth:`!asyncio.AbstractEventLoopPolicy.get_child_watcher` đã bị ngừng sử dụng và sẽ bị xóa trong Python 3.14. (Do Kumar Aditya đóng góp trong :gh:`94597`.)

  * Phương thức :meth:`~asyncio.get_event_loop` của chính sách event loop mặc định hiện phát ra một :exc:`DeprecationWarning` nếu chưa thiết lập event loop hiện tại và phương thức này quyết định tạo một event loop. (Do Serhiy Storchaka và Guido van Rossum đóng góp trong :gh:`100160`.)

* :mod:`email`: Đã ngừng sử dụng tham số *isdst* trong :func:`email.utils.localtime`. (Do Alan Williams đóng góp trong :gh:`72346`.)

* Các lớp :mod:`importlib.abc` đã bị ngừng sử dụng:

  * :class:`!importlib.abc.ResourceReader`
  * :class:`!importlib.abc.Traversable`
  * :class:`!importlib.abc.TraversableResources`

  Thay vào đó, hãy sử dụng các lớp :mod:`importlib.resources.abc`:

  * :class:`importlib.resources.abc.Traversable`
  * :class:`importlib.resources.abc.TraversableResources`

  (Do Jason R. Coombs và Hugo van Kemenade đóng góp trong :gh:`93963`.)

* :mod:`itertools` có hỗ trợ không được ghi lại, kém hiệu quả, có nhiều lỗi trong lịch sử và không nhất quán đối với các thao tác copy, deepcopy và pickle. Hỗ trợ này sẽ bị xóa trong 3.14 nhằm giảm đáng kể khối lượng mã và gánh nặng bảo trì. (Do Raymond Hettinger đóng góp trong :gh:`101588`.)

* :mod:`multiprocessing`: Phương thức khởi động mặc định sẽ chuyển sang một phương thức an toàn hơn trên Linux, BSD và các nền tảng POSIX không phải macOS khác, nơi ``'fork'`` hiện đang là mặc định (:gh:`84559`). Việc thêm cảnh báo runtime về thay đổi này được xem là quá gây gián đoạn vì phần lớn mã được cho là không cần quan tâm. Sử dụng
  :func:`~multiprocessing.get_context` hoặc
  :func:`~multiprocessing.set_start_method` API để chỉ định rõ ràng khi mã của bạn *requires* ``'fork'``. Xem :ref:`multiprocessing-start-methods`.

* :mod:`pathlib`: :meth:`~pathlib.PurePath.is_relative_to` và
  :meth:`~pathlib.PurePath.relative_to`: việc truyền các đối số bổ sung đã lỗi thời.

* :mod:`pkgutil`: :func:`!pkgutil.find_loader` và :func:`!pkgutil.get_loader` hiện phát sinh :exc:`DeprecationWarning`; thay vào đó hãy sử dụng :func:`importlib.util.find_spec`. (Do Nikita Sobolev đóng góp trong :gh:`97850`.)

* :mod:`pty`:

  * ``master_open()``: sử dụng :func:`pty.openpty`.
  * ``slave_open()``: hãy sử dụng :func:`pty.openpty`.

* :mod:`sqlite3`:

  * :data:`!version` và :data:`!version_info`.

  * :meth:`~sqlite3.Cursor.execute` và :meth:`~sqlite3.Cursor.executemany` nếu sử dụng :ref:`các placeholder có tên <sqlite3-placeholders>` và *parameters* là một sequence thay vì một :class:`dict`.

* :mod:`urllib`:
  :class:`!urllib.parse.Quoter` không được dùng nữa: nó không được thiết kế để trở thành một API công khai. (Đóng góp bởi Gregory P. Smith trong :gh:`88168`.)
