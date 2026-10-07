Sắp bị loại bỏ trong Python 3.16
--------------------------------

* Hệ thống import:

  * Việc thiết lập :attr:`~module.__loader__` trên một module nhưng không thiết lập :attr:`__spec__.loader <importlib.machinery.ModuleSpec.loader>` đã không còn được khuyến nghị. Trong Python 3.16, :attr:`!__loader__` sẽ không còn được hệ thống import hoặc thư viện chuẩn thiết lập hay xem xét nữa.

* :mod:`array`:

  * Mã định dạng ``'u'`` (:c:type:`wchar_t`) đã không còn được khuyến nghị trong tài liệu kể từ Python 3.3 và tại runtime kể từ Python 3.13. Thay vào đó, hãy sử dụng mã định dạng ``'w'`` (:c:type:`Py_UCS4`) cho các ký tự Unicode.

* :mod:`asyncio`:

  * :func:`!asyncio.iscoroutinefunction` không còn được khuyến nghị và sẽ bị loại bỏ trong Python 3.16; hãy sử dụng :func:`inspect.iscoroutinefunction` thay thế. (Do Jiahao Li và Kumar Aditya đóng góp trong :gh:`122875`.)

  * Hệ thống policy :mod:`asyncio` không còn được khuyến nghị và sẽ bị loại bỏ trong Python 3.16. Cụ thể, các class và function sau đây không còn được khuyến nghị:

    * :class:`asyncio.AbstractEventLoopPolicy`
    * :class:`asyncio.DefaultEventLoopPolicy`
    * :class:`asyncio.WindowsSelectorEventLoopPolicy`
    * :class:`asyncio.WindowsProactorEventLoopPolicy`
    * :func:`asyncio.get_event_loop_policy`
    * :func:`asyncio.set_event_loop_policy`

    Người dùng nên sử dụng :func:`asyncio.run` hoặc :class:`asyncio.Runner` cùng với *loop_factory* để sử dụng implementation event loop mong muốn.

    Ví dụ, để sử dụng :class:`asyncio.SelectorEventLoop` trên Windows::

      import asyncio

      async def main():
          ...

      asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)

    (Do Kumar Aditya đóng góp trong :gh:`127949`.)

* :mod:`builtins`:

  * Phép đảo bit trên các kiểu boolean, ``~True`` hoặc ``~False`` đã không còn được khuyến nghị kể từ Python 3.12, vì nó tạo ra các kết quả bất ngờ và phản trực giác (``-2`` và ``-1``). Thay vào đó, hãy dùng ``not x`` để phủ định logic của một Boolean. Trong trường hợp hiếm khi cần phép đảo bit của số nguyên cơ sở, hãy chuyển đổi rõ ràng sang ``int`` (``~int(x)``).

* :mod:`functools`:

  * Việc gọi implementation Python của :func:`functools.reduce` với *function* hoặc *sequence* làm keyword argument đã không còn được khuyến nghị kể từ Python 3.14.

* :mod:`logging`:

  Hỗ trợ các logging handler tùy chỉnh với đối số *strm* đã không còn được khuyến nghị và dự kiến sẽ bị loại bỏ trong Python 3.16. Thay vào đó, hãy định nghĩa handler với đối số *stream*. (Do Mariusz Felisiak đóng góp trong :gh:`115032`.)

* :mod:`mimetypes`:

  * Các phần mở rộng hợp lệ bắt đầu bằng '.' hoặc là chuỗi rỗng đối với
    :meth:`mimetypes.MimeTypes.add_type`. Các phần mở rộng không có dấu chấm đã không còn được khuyến nghị và sẽ gây ra :exc:`ValueError` trong Python 3.16. (Do Hugo van Kemenade đóng góp trong :gh:`75223`.)

* :mod:`shutil`:

  * Ngoại lệ :class:`!ExecError` đã bị phản đối kể từ Python 3.14. Ngoại lệ này không được bất kỳ hàm nào trong :mod:`!shutil` sử dụng kể từ Python 3.4 và hiện là bí danh của :exc:`RuntimeError`.

* :mod:`symtable`:

  * Phương thức :meth:`Class.get_methods <symtable.Class.get_methods>` đã bị phản đối kể từ Python 3.14.

* :mod:`sys`:

  * Hàm :func:`~sys._enablelegacywindowsfsencoding` đã bị phản đối kể từ Python 3.13. Thay vào đó, hãy sử dụng biến môi trường :envvar:`PYTHONLEGACYWINDOWSFSENCODING`.

* :mod:`sysconfig`:

  * Hàm :func:`!sysconfig.expand_makefile_vars` đã bị phản đối kể từ Python 3.14. Thay vào đó, hãy sử dụng đối số ``vars`` của :func:`sysconfig.get_paths`.

* :mod:`tarfile`:

  * Thuộc tính :attr:`!TarFile.tarfile` không được ghi chép và không được sử dụng đã bị phản đối kể từ Python 3.13.
