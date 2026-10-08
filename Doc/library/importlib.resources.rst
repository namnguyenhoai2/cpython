:mod:`!importlib.resources` -- Đọc, mở và truy cập tài nguyên của package
-------------------------------------------------------------------------

.. module:: importlib.resources
    :synopsis: Đọc, mở và truy cập tài nguyên của package

**Mã nguồn:** :source:`Lib/importlib/resources/__init__.py`

--------------

.. versionadded:: 3.7

Module này tận dụng hệ thống import của Python để cung cấp quyền truy cập vào *tài nguyên* bên trong *package*.

“Tài nguyên” là các tài nguyên dạng tệp được liên kết với một module hoặc package trong Python. Tài nguyên có thể nằm trực tiếp trong một package, bên trong một thư mục con thuộc package đó hoặc nằm cạnh các module bên ngoài package. Tài nguyên có thể là văn bản hoặc dữ liệu nhị phân. Do đó, mã nguồn module Python của một package (.py), các artifact biên dịch (pycache) và các artifact cài đặt (như :func:`reserved filenames <os.path.isreserved>` trong các thư mục) về mặt kỹ thuật đều là tài nguyên trên thực tế của package đó. Tuy nhiên, trong thực tế, tài nguyên chủ yếu là các artifact không phải Python được tác giả package cung cấp riêng.

Có thể mở hoặc đọc tài nguyên ở chế độ nhị phân hoặc văn bản.

Tài nguyên gần giống như các tệp bên trong thư mục, dù cần lưu ý rằng đây chỉ là một phép ẩn dụ. Tài nguyên và package **không** nhất thiết phải tồn tại dưới dạng các tệp và thư mục vật lý trên hệ thống tệp: chẳng hạn, có thể import một package cùng các tài nguyên của nó từ tệp zip bằng cách sử dụng
:py:mod:`zipimport`.

.. warning::

   :mod:`importlib.resources` tuân theo cùng mô hình bảo mật như thành phần tích hợp sẵn
   :func:`open` function. Việc truyền đầu vào không đáng tin cậy cho các hàm trong mô-đun này là không an toàn.

.. note::

   Bản backport độc lập của mô-đun này cung cấp thêm thông tin về `sử dụng importlib.resources <https://importlib-resources.readthedocs.io/en/latest/using.html>`_ và `di chuyển từ pkg_resources sang importlib.resources <https://importlib-resources.readthedocs.io/en/latest/migration.html>`_.

:class:`Loaders <importlib.abc.Loader>` muốn hỗ trợ việc đọc tài nguyên nên triển khai phương thức ``get_resource_reader(fullname)`` theo đặc tả của
:class:`importlib.resources.abc.ResourceReader`.

.. class:: Anchor

    Đại diện cho một anchor của tài nguyên, có thể là :class:`module object <types.ModuleType>` hoặc tên mô-đun dưới dạng chuỗi. Được định nghĩa là ``Union[str, ModuleType]``.

.. function:: files(anchor: Optional[Anchor] = None)

    Trả về một đối tượng :class:`~importlib.resources.abc.Traversable` đại diện cho vùng chứa tài nguyên (hãy hình dung là thư mục) và các tài nguyên của vùng chứa đó (hãy hình dung là các tệp). Một Traversable có thể chứa các vùng chứa khác (hãy hình dung là các thư mục con).

    *anchor* là một :class:`Anchor` tùy chọn. Nếu anchor là một package, các tài nguyên được phân giải từ package đó. Nếu là một mô-đun, các tài nguyên được phân giải bên cạnh mô-đun đó (trong cùng package hoặc thư mục gốc của package). Nếu bỏ qua anchor, mô-đun của bên gọi sẽ được sử dụng.

    .. versionadded:: 3.9

    .. versionchanged:: 3.12
       Tham số *package* đã được đổi tên thành *anchor*. Giờ đây, *anchor* có thể là một module không phải package và nếu bị bỏ qua, tham số này sẽ mặc định là module của caller. *package* vẫn được chấp nhận để tương thích nhưng sẽ raise một :exc:`DeprecationWarning`. Hãy cân nhắc truyền anchor theo vị trí hoặc sử dụng ``importlib_resources >= 5.10`` để có interface tương thích trên các phiên bản Python cũ hơn.

.. function:: as_file(traversable)

    Với một đối tượng :class:`~importlib.resources.abc.Traversable` đại diện cho một tệp hoặc thư mục, thường lấy từ :func:`importlib.resources.files`, hãy trả về một context manager để sử dụng trong câu lệnh :keyword:`with`. Context manager này cung cấp một đối tượng :class:`pathlib.Path`.

    Khi thoát khỏi context manager, mọi tệp hoặc thư mục tạm được tạo khi resource được trích xuất, chẳng hạn từ tệp zip, sẽ được dọn dẹp.

    Sử dụng ``as_file`` khi các phương thức Traversable (``read_text``, v.v.) không đủ và cần một tệp hoặc thư mục thực trên file system.

    .. versionadded:: 3.9

    .. versionchanged:: 3.12
       Đã bổ sung hỗ trợ cho *traversable* đại diện cho một thư mục.


.. _importlib_resources_functional:

Functional API
^^^^^^^^^^^^^^

Có một tập hợp các helper đơn giản hóa và tương thích ngược. Các helper này cho phép thực hiện những thao tác phổ biến trong một lần gọi hàm.

Đối với tất cả các hàm sau:

- *anchor* là một :class:`~importlib.resources.Anchor`, như trong :func:`~importlib.resources.files`. Không giống như trong ``files``, nó không được phép bỏ qua.

- *path_names* là các thành phần của tên đường dẫn của một tài nguyên, tính tương đối so với anchor. Ví dụ, để lấy văn bản của tài nguyên có tên ``info.txt``, hãy sử dụng::

      importlib.resources.read_text(my_module, "info.txt")

  Giống như :meth:`Traversable.joinpath <importlib.resources.abc.Traversable>`, các thành phần riêng lẻ phải sử dụng dấu gạch chéo xuôi (``/``) làm dấu phân cách đường dẫn. Ví dụ, các cách sau đây là tương đương::

      importlib.resources.read_binary(my_module, "pics/painting.png")
      importlib.resources.read_binary(my_module, "pics", "painting.png")

  Vì lý do tương thích ngược, các hàm đọc văn bản yêu cầu đối số *encoding* tường minh nếu có nhiều *path_names*. Ví dụ, để lấy văn bản của ``info/chapter1.txt``, hãy sử dụng::

      importlib.resources.read_text(my_module, "info", "chapter1.txt",
                                    encoding='utf-8')

.. function:: open_binary(anchor, *path_names)

    Mở tài nguyên có tên để đọc nhị phân.

    Xem :ref:`the introduction <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*.

    Hàm này trả về một đối tượng :class:`~typing.BinaryIO`, tức là một luồng nhị phân mở để đọc.

    Hàm này gần tương đương với::

        files(anchor).joinpath(*path_names).open('rb')

    .. versionchanged:: 3.13
        Có thể cung cấp nhiều *path_names*.


.. function:: open_text(anchor, *path_names, encoding='utf-8', errors='strict')

    Mở tài nguyên có tên để đọc văn bản. Theo mặc định, nội dung được đọc dưới dạng UTF-8 nghiêm ngặt.

    Xem :ref:`phần giới thiệu <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*. *encoding* và *errors* có cùng ý nghĩa như trong :func:`open` dựng sẵn.

    Vì lý do tương thích ngược, phải cung cấp tường minh đối số *encoding* nếu có nhiều *path_names*. Hạn chế này dự kiến sẽ được loại bỏ trong Python 3.15.

    Hàm này trả về một đối tượng :class:`~typing.TextIO`, tức là một luồng văn bản mở để đọc.

    Hàm này gần tương đương với::

          files(anchor).joinpath(*path_names).open('r', encoding=encoding)

    .. versionchanged:: 3.13
        Có thể cung cấp nhiều *path_names*. Phải cung cấp *encoding* và *errors* dưới dạng đối số từ khóa.


.. function:: read_binary(anchor, *path_names)

    Đọc và trả về nội dung của tài nguyên được chỉ định dưới dạng :class:`bytes`.

    Xem :ref:`the introduction <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*.

    Hàm này gần tương đương với::

          files(anchor).joinpath(*path_names).read_bytes()

    .. versionchanged:: 3.13
        Có thể cung cấp nhiều *path_names*.


.. function:: read_text(anchor, *path_names, encoding='utf-8', errors='strict')

    Đọc và trả về nội dung của tài nguyên được chỉ định dưới dạng :class:`str`. Theo mặc định, nội dung được đọc dưới dạng UTF-8 strict.

    Xem :ref:`phần giới thiệu <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*. *encoding* và *errors* có cùng ý nghĩa như trong :func:`open` dựng sẵn.

    Vì lý do tương thích ngược, phải cung cấp tường minh đối số *encoding* nếu có nhiều *path_names*. Hạn chế này dự kiến sẽ được loại bỏ trong Python 3.15.

    Hàm này gần tương đương với::

          files(anchor).joinpath(*path_names).read_text(encoding=encoding)

    .. versionchanged:: 3.13
        Có thể cung cấp nhiều *path_names*. Phải cung cấp *encoding* và *errors* dưới dạng đối số từ khóa.


.. function:: path(anchor, *path_names)

    Cung cấp đường dẫn đến *tài nguyên* dưới dạng một đường dẫn hệ thống tệp thực. Hàm này trả về một context manager để sử dụng trong câu lệnh :keyword:`with`. Context manager cung cấp một đối tượng :class:`pathlib.Path`.

    Việc thoát khỏi context manager sẽ dọn dẹp mọi tệp tạm thời đã tạo, chẳng hạn như khi tài nguyên cần được trích xuất từ tệp zip.

    Ví dụ: phương thức :meth:`~pathlib.Path.stat` yêu cầu một đường dẫn hệ thống tệp thực; bạn có thể sử dụng như sau::

        with importlib.resources.path(anchor, "resource.txt") as fspath:
            result = fspath.stat()

    Xem :ref:`the introduction <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*.

    Hàm này gần tương đương với::

          as_file(files(anchor).joinpath(*path_names))

    .. versionchanged:: 3.13
        Có thể cung cấp nhiều *path_names*.


.. function:: is_resource(anchor, *path_names)

    Trả về ``True`` nếu tài nguyên được đặt tên tồn tại, nếu không thì trả về ``False``. Hàm này không coi thư mục là tài nguyên.

    Xem :ref:`the introduction <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*.

    Hàm này gần tương đương với::

          files(anchor).joinpath(*path_names).is_file()

    .. versionchanged:: 3.13
        Có thể cung cấp nhiều *path_names*.


.. function:: contents(anchor, *path_names)

    Trả về một đối tượng có thể lặp qua các mục được đặt tên trong package hoặc đường dẫn. Đối tượng có thể lặp này trả về tên của các tài nguyên (ví dụ: tệp) và các mục không phải tài nguyên (ví dụ: thư mục) dưới dạng :class:`str`. Đối tượng có thể lặp này không đệ quy vào các thư mục con.

    Xem :ref:`the introduction <importlib_resources_functional>` để biết chi tiết về *anchor* và *path_names*.

    Hàm này gần tương đương với::

        for resource in files(anchor).joinpath(*path_names).iterdir():
            yield resource.name

    .. deprecated:: 3.11
        Ưu tiên sử dụng ``iterdir()`` như trên, vì cách này cho phép kiểm soát kết quả tốt hơn và cung cấp nhiều chức năng hơn.

.. _`using importlib.resources`: https://importlib-resources.readthedocs.io/en/latest/using.html
.. _`migrating from pkg_resources to importlib.resources`: https://importlib-resources.readthedocs.io/en/latest/migration.html
