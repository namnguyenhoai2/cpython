Sắp bị loại bỏ trong các phiên bản tương lai
--------------------------------------------

Các API sau đây sẽ bị loại bỏ trong tương lai, mặc dù hiện chưa có ngày cụ thể được lên lịch cho việc loại bỏ chúng.

* :mod:`argparse`:

  * Việc lồng các nhóm đối số và lồng các nhóm loại trừ lẫn nhau đã không còn được khuyến nghị.
  * Việc truyền đối số từ khóa không được ghi lại *prefix_chars* vào
    :meth:`~argparse.ArgumentParser.add_argument_group` hiện không còn được khuyến nghị.
  * Bộ chuyển đổi kiểu :class:`argparse.FileType` không còn được khuyến nghị.

* :mod:`builtins`:

  * Generators: chữ ký của ``throw(type, exc, tb)`` và ``athrow(type, exc, tb)`` không còn được khuyến nghị: thay vào đó, hãy sử dụng ``throw(exc)`` và ``athrow(exc)``, tức là chữ ký có một đối số.
  * Hiện tại Python chấp nhận các numeric literal ngay trước keyword, chẳng hạn như ``0in x``, ``1or x``, ``0if 1else 2``.  Điều này cho phép các biểu thức gây nhầm lẫn và không rõ ràng như ``[0x1for x in y]`` (có thể được diễn giải là ``[0x1 for x in y]`` hoặc ``[0x1f or x in y]``).  Một cảnh báo cú pháp được đưa ra nếu numeric literal đứng ngay trước một trong các keyword
    :keyword:`and`, :keyword:`else`, :keyword:`for`, :keyword:`if`,
    :keyword:`in`, :keyword:`is` và :keyword:`or`.  Trong một bản phát hành trong tương lai, điều này sẽ được thay đổi thành lỗi cú pháp. (:gh:`87999`)
  * Hỗ trợ cho các phương thức ``__index__()`` và ``__int__()`` trả về kiểu không phải int: các phương thức này sẽ bắt buộc phải trả về một instance của một strict subclass của
    :class:`int`.
  * Hỗ trợ cho phương thức ``__float__()`` trả về một strict subclass của
    :class:`float`: các phương thức này sẽ bắt buộc phải trả về một instance của
    :class:`float`.
  * Hỗ trợ cho phương thức ``__complex__()`` trả về một strict subclass của
    :class:`complex`: các phương thức này sẽ bắt buộc phải trả về một instance của
    :class:`complex`.
  * Việc truyền một số phức làm đối số *real* hoặc *imag* trong
    constructor :func:`complex` hiện đã lỗi thời; chỉ nên truyền nó dưới dạng một đối số vị trí duy nhất. (Do Serhiy Storchaka đóng góp trong :gh:`109218`.)

* :mod:`calendar`: các hằng số ``calendar.January`` và ``calendar.February`` đã lỗi thời và được thay thế bằng :data:`calendar.JANUARY` và
  :data:`calendar.FEBRUARY`. (Do Prince Roshan đóng góp trong :gh:`103636`.)

* :mod:`codecs`: sử dụng :func:`open` thay cho :func:`codecs.open`. (:gh:`133038`)

* :attr:`codeobject.co_lnotab`: thay vào đó, hãy sử dụng phương thức :meth:`codeobject.co_lines`.

* :mod:`datetime`:

  * :meth:`~datetime.datetime.utcnow`: sử dụng ``datetime.datetime.now(tz=datetime.UTC)``.
  * :meth:`~datetime.datetime.utcfromtimestamp`: sử dụng ``datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)``.

* :mod:`gettext`: Giá trị số nhiều phải là một số nguyên.

* :mod:`importlib`:

  * :func:`~importlib.util.cache_from_source` *debug_override* parameter không còn được dùng: thay vào đó, hãy sử dụng parameter *optimization*.

* :mod:`importlib.metadata`:

  * ``EntryPoints`` giao diện tuple.
  * ``None`` ngầm định trên các giá trị trả về.

* :mod:`logging`: method ``warn()`` đã không còn được dùng kể từ Python 3.3, thay vào đó hãy sử dụng :meth:`~logging.warning`.

* :mod:`mailbox`: Việc sử dụng đầu vào StringIO và chế độ văn bản không còn được dùng, thay vào đó hãy sử dụng BytesIO và chế độ nhị phân.

* :mod:`os`: Việc gọi :func:`os.register_at_fork` trong tiến trình đa luồng.

* :class:`!pydoc.ErrorDuringImport`: Giá trị tuple cho tham số *exc_info* đã lỗi thời, hãy sử dụng một instance của exception.

* :mod:`re`: Các quy tắc nghiêm ngặt hơn hiện được áp dụng cho các tham chiếu nhóm số và tên nhóm trong biểu thức chính quy. Hiện chỉ chấp nhận chuỗi gồm các chữ số ASCII làm tham chiếu số. Tên nhóm trong các mẫu bytes và chuỗi thay thế giờ đây chỉ có thể chứa chữ cái ASCII, chữ số và dấu gạch dưới. (Đóng góp của Serhiy Storchaka trong :gh:`91760`.)

* Các mô-đun :mod:`!sre_compile`, :mod:`!sre_constants` và :mod:`!sre_parse`.

* :mod:`shutil`: Tham số :func:`~shutil.rmtree`'s *onerror* của :func:`~shutil.rmtree` đã lỗi thời trong Python 3.12; hãy sử dụng tham số *onexc* thay thế.

* Các tùy chọn và giao thức của :mod:`ssl`:

  * :class:`ssl.SSLContext` không có đối số protocol đã lỗi thời.
  * :class:`ssl.SSLContext`: :meth:`~ssl.SSLContext.set_npn_protocols` và
    :meth:`!selected_npn_protocol` không còn được khuyến nghị: hãy sử dụng ALPN thay thế.
  * Các tùy chọn ``ssl.OP_NO_SSL*``
  * Các tùy chọn ``ssl.OP_NO_TLS*``
  * ``ssl.PROTOCOL_SSLv3``
  * ``ssl.PROTOCOL_TLS``
  * ``ssl.PROTOCOL_TLSv1``
  * ``ssl.PROTOCOL_TLSv1_1``
  * ``ssl.PROTOCOL_TLSv1_2``
  * ``ssl.TLSVersion.SSLv3``
  * ``ssl.TLSVersion.TLSv1``
  * ``ssl.TLSVersion.TLSv1_1``

* Các phương thức :mod:`threading`:

  * :meth:`!threading.Condition.notifyAll`: hãy sử dụng :meth:`~threading.Condition.notify_all`.
  * :meth:`!threading.Event.isSet`: hãy sử dụng :meth:`~threading.Event.is_set`.
  * :meth:`!threading.Thread.isDaemon`, :meth:`threading.Thread.setDaemon`: hãy sử dụng thuộc tính :attr:`threading.Thread.daemon`.
  * :meth:`!threading.Thread.getName`, :meth:`threading.Thread.setName`: hãy sử dụng thuộc tính :attr:`threading.Thread.name`.
  * :meth:`!threading.currentThread`: hãy sử dụng :meth:`threading.current_thread`.
  * :meth:`!threading.activeCount`: hãy sử dụng :meth:`threading.active_count`.

* :class:`typing.Text` (:gh:`92332`).

* Lớp nội bộ ``typing._UnionGenericAlias`` không còn được sử dụng để triển khai
  :class:`typing.Union`. Để duy trì khả năng tương thích với người dùng sử dụng lớp riêng tư này, một compatibility shim sẽ được cung cấp cho đến ít nhất Python 3.17. (Do Jelle Zijlstra đóng góp trong :gh:`105499`.)

* :class:`unittest.IsolatedAsyncioTestCase`: việc trả về một giá trị không phải ``None`` từ test case được coi là deprecated.

* :mod:`urllib.parse` các hàm đã bị deprecated: thay vào đó dùng :func:`~urllib.parse.urlparse`

  * ``splitattr()``
  * ``splithost()``
  * ``splitnport()``
  * ``splitpasswd()``
  * ``splitport()``
  * ``splitquery()``
  * ``splittag()``
  * ``splittype()``
  * ``splituser()``
  * ``splitvalue()``
  * ``to_bytes()``

* :mod:`wsgiref`: ``SimpleHandler.stdout.write()`` không nên thực hiện việc ghi từng phần.

* :mod:`xml.etree.ElementTree`: Kiểm tra giá trị đúng/sai của một
  :class:`~xml.etree.ElementTree.Element` đã bị deprecated. Trong một bản phát hành tương lai, nó sẽ luôn trả về ``True``. Thay vào đó, hãy ưu tiên các phép kiểm tra ``len(elem)`` hoặc ``elem is not None`` rõ ràng.

* :func:`sys._clear_type_cache` đã bị deprecated: thay vào đó dùng :func:`sys._clear_internal_caches`.
