Sắp bị loại bỏ trong Python 3.15
--------------------------------

* Hệ thống import:

  * Việc đặt :attr:`~module.__cached__` trên một module nhưng không đặt :attr:`__spec__.cached <importlib.machinery.ModuleSpec.cached>` đã không còn được khuyến nghị. Trong Python 3.15, :attr:`!__cached__` sẽ không còn được hệ thống import hoặc thư viện chuẩn đặt hay xem xét nữa. (:gh:`97879`)

  * Việc đặt :attr:`~module.__package__` trên một module nhưng không đặt :attr:`__spec__.parent <importlib.machinery.ModuleSpec.parent>` đã không còn được khuyến nghị. Trong Python 3.15, :attr:`!__package__` sẽ không còn được hệ thống import hoặc thư viện chuẩn đặt hay xem xét nữa. (:gh:`97879`)

* :mod:`ctypes`:

  * Hàm :func:`!ctypes.SetPointerType` chưa được ghi chép đã không còn được khuyến nghị kể từ Python 3.13.

* :mod:`http.server`:

  * :class:`~http.server.CGIHTTPRequestHandler` lỗi thời và hiếm khi được sử dụng đã không còn được khuyến nghị kể từ Python 3.13. Không có phương án thay thế trực tiếp. *Bất kỳ thứ gì* đều tốt hơn CGI để kết nối một web server với một request handler.

  * Cờ :option:`!--cgi` của giao diện dòng lệnh :program:`python -m http.server` đã không còn được khuyến nghị kể từ Python 3.13.

* :mod:`importlib`:

  * Phương thức ``load_module()``: hãy sử dụng ``exec_module()`` thay thế.

* :mod:`pathlib`:

  * :meth:`.PurePath.is_reserved` đã bị deprecated kể từ Python 3.13. Sử dụng :func:`os.path.isreserved` để phát hiện các đường dẫn dành riêng trên Windows.

* :mod:`platform`:

  * :func:`~platform.java_ver` đã bị deprecated kể từ Python 3.13. Hàm này chỉ hữu ích để hỗ trợ Jython, có API khó hiểu và hầu như chưa được kiểm thử.

* :mod:`sysconfig`:

  * Đối số *check_home* của :func:`sysconfig.is_python_build` đã bị deprecated kể từ Python 3.12.

* :mod:`threading`:

  * :func:`~threading.RLock` sẽ không nhận đối số nào trong Python 3.15. Việc truyền bất kỳ đối số nào đã bị deprecated kể từ Python 3.14, vì phiên bản Python không cho phép bất kỳ đối số nào, nhưng phiên bản C cho phép mọi số lượng đối số vị trí hoặc đối số từ khóa và bỏ qua tất cả các đối số.

* :mod:`types`:

  * :class:`types.CodeType`: Việc truy cập :attr:`~codeobject.co_lnotab` đã bị deprecated trong :pep:`626` kể từ 3.10 và dự kiến bị xóa trong 3.12, nhưng chỉ nhận được một :exc:`DeprecationWarning` chính thức trong 3.12. Có thể bị xóa trong 3.15. (Do Nikita Sobolev đóng góp trong :gh:`101866`.)

* :mod:`typing`:

  * Cú pháp đối số từ khóa không được ghi lại để tạo
    Các lớp :class:`~typing.NamedTuple` (ví dụ: ``Point = NamedTuple("Point", x=int, y=int)``) đã không còn được dùng kể từ Python 3.13. Thay vào đó, hãy sử dụng cú pháp dựa trên lớp hoặc cú pháp hàm.

  * Khi sử dụng cú pháp hàm của :class:`~typing.TypedDict`\s, việc không truyền giá trị cho tham số *fields* (``TD = TypedDict("TD")``) hoặc truyền ``None`` (``TD = TypedDict("TD", None)``) đã không còn được dùng kể từ Python 3.13. Hãy sử dụng ``class TD(TypedDict): pass`` hoặc ``TD = TypedDict("TD", {})`` để tạo một TypedDict không có trường.

  * Hàm decorator :deco:`typing.no_type_check_decorator` đã không còn được dùng kể từ Python 3.13. Sau tám năm trong module :mod:`typing`, hàm này vẫn chưa được bất kỳ type checker lớn nào hỗ trợ.

* :mod:`wave`:

  * Các phương thức :meth:`~wave.Wave_read.getmark`, :meth:`!setmark` và :meth:`~wave.Wave_read.getmarkers` của các lớp :class:`~wave.Wave_read` và :class:`~wave.Wave_write` đã không còn được dùng kể từ Python 3.13.

* :mod:`zipimport`:

  * :meth:`~zipimport.zipimporter.load_module` đã không còn được dùng kể từ Python 3.10. Thay vào đó, hãy sử dụng :meth:`~zipimport.zipimporter.exec_module`. (Do Jiahao Li đóng góp trong :gh:`125746`.)
