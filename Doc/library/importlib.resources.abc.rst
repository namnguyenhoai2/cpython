:mod:`!importlib.resources.abc` -- Các lớp cơ sở trừu tượng cho tài nguyên
--------------------------------------------------------------------------

.. module:: importlib.resources.abc
    :synopsis: Các lớp cơ sở trừu tượng cho tài nguyên

**Mã nguồn:** :source:`Lib/importlib/resources/abc.py`

--------------

.. versionadded:: 3.11

.. class:: ResourceReader

    *Được thay thế bởi TraversableResources*

    Một :term:`abstract base class` để cung cấp khả năng đọc *tài nguyên*.

    Theo góc nhìn của ABC này, một *tài nguyên* là một tạo phẩm nhị phân được đóng gói bên trong một package. Thông thường, đó là một tệp dữ liệu nằm cùng với tệp ``__init__.py`` của package. Mục đích của lớp này là trừu tượng hóa việc truy cập các tệp dữ liệu như vậy, để không phụ thuộc vào việc package và (các) tệp dữ liệu của nó được lưu trữ trong một tệp zip hay trên hệ thống tệp.

    Đối với mọi phương thức của lớp này, đối số *tài nguyên* được kỳ vọng là một :term:`path-like object`, về mặt khái niệm chỉ đại diện cho một tên tệp. Điều này có nghĩa là không được chứa đường dẫn thư mục con trong đối số *tài nguyên*. Lý do là vị trí của package mà reader phục vụ đóng vai trò là "thư mục". Vì vậy, phép ẩn dụ cho thư mục và tên tệp lần lượt là package và tài nguyên. Đây cũng là lý do các thực thể của lớp này được kỳ vọng tương ứng trực tiếp với một package cụ thể (thay vì có thể đại diện cho nhiều package hoặc một module).

    Các loader muốn hỗ trợ việc đọc tài nguyên được yêu cầu cung cấp một phương thức có tên ``get_resource_reader(fullname)``, phương thức này trả về một đối tượng triển khai giao diện của ABC này. Nếu module được chỉ định bởi fullname không phải là package, phương thức này nên trả về
    :const:`None`. Chỉ nên trả về một đối tượng tương thích với ABC này khi module được chỉ định là một package.

    .. deprecated:: 3.12
       Thay vào đó, hãy sử dụng :class:`importlib.resources.abc.TraversableResources`.

    .. method:: open_resource(resource)
       :abstractmethod:

       Trả về một :term:`file-like object` đã mở để đọc nhị phân *tài nguyên*.

       Nếu không tìm thấy tài nguyên, :exc:`FileNotFoundError` sẽ được raise.

    .. method:: resource_path(resource)
       :abstractmethod:

       Trả về đường dẫn hệ thống tệp tới *tài nguyên*.

       Nếu tài nguyên không thực sự tồn tại trên hệ thống tệp, hãy raise :exc:`FileNotFoundError`.

    .. method:: is_resource(path)
       :abstractmethod:

       Trả về ``True`` nếu *path* được coi là một tài nguyên.
       :exc:`FileNotFoundError` được phát sinh nếu *path* không tồn tại.

       .. versionchanged:: 3.10
          Đối số *name* đã được đổi tên thành *path*.

    .. method:: contents()
       :abstractmethod:

       Trả về một :term:`iterable` gồm các chuỗi về nội dung của package. Lưu ý rằng không bắt buộc tất cả các tên được iterator trả về phải là tài nguyên thực tế; chẳng hạn, việc trả về các tên mà :meth:`is_resource` sẽ là sai là hoàn toàn hợp lệ.

       Cho phép trả về các tên không phải tài nguyên nhằm hỗ trợ những trường hợp đã biết trước cách package và các tài nguyên của package được lưu trữ, và các tên không phải tài nguyên sẽ hữu ích. Chẳng hạn, cho phép trả về tên các thư mục con để khi biết package và các tài nguyên được lưu trữ trên hệ thống tệp thì có thể sử dụng trực tiếp các tên thư mục con đó.

       Phương thức abstract trả về một iterable không chứa phần tử nào.


.. class:: Traversable

    Một đối tượng có một tập hợp con các phương thức :class:`pathlib.Path`, phù hợp để duyệt qua các thư mục và mở tệp.

    Để biểu diễn đối tượng trên hệ thống tệp, hãy sử dụng
    :meth:`importlib.resources.as_file`.

    .. attribute:: name

       Trừu tượng. Tên cơ sở của đối tượng này, không bao gồm bất kỳ tham chiếu nào đến đối tượng cha.

    .. method:: iterdir()
       :abstractmethod:

       Sinh các đối tượng Traversable trong self.

    .. method:: is_dir()
       :abstractmethod:

       Trả về ``True`` nếu self là một thư mục.

    .. method:: is_file()
       :abstractmethod:

       Trả về ``True`` nếu self là một tệp.

    .. method:: joinpath(*pathsegments)
       :abstractmethod:

       Duyệt qua các thư mục theo *pathsegments* và trả về kết quả dưới dạng :class:`!Traversable`.

       Mỗi đối số *pathsegments* có thể chứa nhiều tên được phân tách bằng dấu gạch chéo xuôi (``/``, ``posixpath.sep``). Ví dụ, các cách sau là tương đương::

           files.joinpath('subdir', 'subsuddir', 'file.txt')
           files.joinpath('subdir/subsuddir/file.txt')

       Lưu ý rằng một số triển khai :class:`!Traversable` có thể chưa được cập nhật lên phiên bản mới nhất của giao thức. Để tương thích với các triển khai như vậy, hãy cung cấp một đối số duy nhất không chứa dấu phân cách đường dẫn cho mỗi lần gọi ``joinpath``. Ví dụ::

           files.joinpath('subdir').joinpath('subsubdir').joinpath('file.txt')

       .. versionchanged:: 3.11

          ``joinpath`` chấp nhận nhiều *pathsegments*, và các đoạn này có thể chứa dấu gạch chéo xuôi làm dấu phân cách đường dẫn. Trước đây, chỉ chấp nhận một đối số *child* duy nhất.

    .. method:: __truediv__(child)
       :abstractmethod:

       Trả về đối tượng Traversable con trong self. Tương đương với ``joinpath(child)``.

    .. method:: open(mode='r', *args, **kwargs)
       :abstractmethod:

       *mode* có thể là 'r' hoặc 'rb' để mở ở dạng văn bản hoặc nhị phân. Trả về một handle phù hợp để đọc (giống như :attr:`pathlib.Path.open`).

       Khi mở ở dạng văn bản, chấp nhận các tham số encoding như những tham số được :class:`io.TextIOWrapper` chấp nhận.

    .. method:: read_bytes()

       Đọc nội dung của self dưới dạng bytes.

    .. method:: read_text(encoding=None)

       Đọc nội dung của self dưới dạng văn bản.


.. class:: TraversableResources

    Một lớp cơ sở trừu tượng dành cho các resource reader có khả năng cung cấp giao diện :meth:`importlib.resources.files`. Các lớp con
    :class:`ResourceReader` và cung cấp các triển khai cụ thể cho các phương thức trừu tượng của :class:`!ResourceReader`. Do đó, mọi loader cung cấp
    :class:`!TraversableResources` cũng cung cấp :class:`!ResourceReader`.

    Các loader muốn hỗ trợ việc đọc resource được kỳ vọng sẽ triển khai giao diện này.

    .. method:: files()
       :abstractmethod:

       Trả về một đối tượng :class:`importlib.resources.abc.Traversable` cho package đã được tải.
