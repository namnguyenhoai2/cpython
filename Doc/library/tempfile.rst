:mod:`!tempfile` --- Tạo các tệp và thư mục tạm thời
====================================================

.. module:: tempfile
   :synopsis: Tạo các tệp và thư mục tạm thời.

.. sectionauthor:: Zack Weinberg <zack@codesourcery.com>

**Mã nguồn:** :source:`Lib/tempfile.py`

.. index::
   pair: temporary; file name
   pair: temporary; file

--------------

Mô-đun này tạo các tệp và thư mục tạm thời.  Nó hoạt động trên tất cả các nền tảng được hỗ trợ. :class:`TemporaryFile`, :class:`NamedTemporaryFile`,
:class:`TemporaryDirectory`, và :class:`SpooledTemporaryFile` là các giao diện cấp cao cung cấp khả năng dọn dẹp tự động và có thể được sử dụng làm
:term:`trình quản lý ngữ cảnh <context manager>`. :func:`mkstemp` và
:func:`mkdtemp` là các hàm cấp thấp hơn, yêu cầu dọn dẹp thủ công.

Tất cả các hàm và constructor mà người dùng có thể gọi đều nhận thêm các đối số cho phép kiểm soát trực tiếp vị trí và tên của các tệp và thư mục tạm thời. Tên tệp được mô-đun này sử dụng bao gồm một chuỗi ký tự ngẫu nhiên, cho phép tạo các tệp đó một cách an toàn trong các thư mục tạm thời dùng chung. Để duy trì khả năng tương thích ngược, thứ tự đối số hơi khác thường; bạn nên sử dụng các đối số từ khóa để mã rõ ràng hơn.

Mô-đun định nghĩa các mục sau đây mà người dùng có thể gọi:

.. function:: TemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, *, errors=None)

   Trả về một :term:`file-like object` có thể được dùng làm vùng lưu trữ tạm thời. Tệp được tạo một cách an toàn, sử dụng cùng các quy tắc như :func:`mkstemp`. Tệp sẽ bị hủy ngay khi được đóng (bao gồm cả thao tác đóng ngầm khi đối tượng được thu gom rác). Trên Unix, mục thư mục của tệp либо không được tạo hoặc được xóa ngay sau khi tệp được tạo. Các nền tảng khác không hỗ trợ điều này; mã của bạn không nên dựa vào việc tệp tạm thời được tạo bằng hàm này có hoặc không có tên hiển thị trong hệ thống tệp.

   Đối tượng kết quả có thể được sử dụng như một :term:`context manager` (xem
   :ref:`tempfile-examples`). Khi ngữ cảnh kết thúc hoặc đối tượng tệp bị hủy, tệp tạm thời sẽ bị xóa khỏi hệ thống tệp.

   Tham số *mode* mặc định là ``'w+b'`` để tệp được tạo có thể được đọc và ghi mà không cần đóng. Chế độ nhị phân được sử dụng để đảm bảo hành vi nhất quán trên mọi nền tảng, không phụ thuộc vào dữ liệu được lưu trữ. *buffering*, *encoding*, *errors* và *newline* được diễn giải giống như trong
   :func:`open`.

   Các tham số *dir*, *prefix* và *suffix* có cùng ý nghĩa và giá trị mặc định như trong :func:`mkstemp`.

   Đối tượng được trả về là một đối tượng tệp thực sự trên các nền tảng POSIX. Trên các nền tảng khác, đây là một đối tượng giống tệp có thuộc tính :attr:`!file` trỏ đến đối tượng tệp thực sự bên dưới.

   Cờ :py:const:`os.O_TMPFILE` được sử dụng nếu có sẵn và hoạt động (chỉ dành cho Linux, yêu cầu Linux kernel 3.11 trở lên).

   Trên các nền tảng không phải Posix hoặc Cygwin, TemporaryFile là bí danh của NamedTemporaryFile.

   .. audit-event:: tempfile.mkstemp fullpath tempfile.TemporaryFile

   .. versionchanged:: 3.5

      Cờ :py:const:`os.O_TMPFILE` hiện được sử dụng nếu có sẵn.

   .. versionchanged:: 3.8
      Đã thêm tham số *errors*.


.. function:: NamedTemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, delete=True, *, errors=None, delete_on_close=True)

   Hàm này hoạt động chính xác như :func:`TemporaryFile`, ngoại trừ những điểm khác biệt sau:

   * Hàm này trả về một tệp được đảm bảo có tên hiển thị trong hệ thống tệp.
   * Để quản lý tệp có tên, hàm này mở rộng các tham số của
     :func:`TemporaryFile` với các tham số *delete* và *delete_on_close* để xác định liệu tệp có tên có được tự động xóa hay không và xóa như thế nào.

   Đối tượng được trả về luôn là một :term:`file-like object` có thuộc tính :attr:`!file` là đối tượng tệp thực bên dưới. Đối tượng giống tệp này có thể được sử dụng trong câu lệnh :keyword:`with`, giống như một tệp thông thường. Có thể lấy tên của tệp tạm thời từ thuộc tính :attr:`!name` của đối tượng giống tệp được trả về. Trên Unix, không giống như với
   :func:`TemporaryFile`, mục nhập thư mục không bị hủy liên kết ngay sau khi tệp được tạo.

   Nếu *delete* là true (mặc định) và *delete_on_close* là true (mặc định), tệp sẽ bị xóa ngay khi được đóng. Nếu *delete* là true và *delete_on_close* là false, tệp chỉ bị xóa khi thoát khỏi context manager hoặc khi :term:`file-like object` được hoàn tất. Trong trường hợp này, việc xóa không phải lúc nào cũng được đảm bảo (xem :meth:`object.__del__`). Nếu *delete* là false, giá trị của *delete_on_close* sẽ bị bỏ qua.

   Do đó, để sử dụng tên của tệp tạm thời nhằm mở lại tệp sau khi đóng, hãy đảm bảo không xóa tệp khi đóng (đặt tham số *delete* thành false) hoặc, trong trường hợp tệp tạm thời được tạo trong câu lệnh :keyword:`with`, đặt tham số *delete_on_close* thành false. Cách tiếp cận sau được khuyến nghị vì hỗ trợ tự động dọn dẹp tệp tạm thời khi thoát khỏi context manager.

   Việc mở lại tệp tạm thời bằng tên của nó trong khi tệp vẫn đang mở hoạt động như sau:

   * Trên POSIX, tệp luôn có thể được mở lại.
   * Trên Windows, hãy đảm bảo ít nhất một trong các điều kiện sau được đáp ứng:

     * *delete* là false
     * các thao tác mở bổ sung chia sẻ quyền truy cập delete (ví dụ: bằng cách gọi :func:`os.open` với cờ ``O_TEMPORARY``)
     * *delete* là true nhưng *delete_on_close* là false. Lưu ý rằng trong trường hợp này, các thao tác mở bổ sung không chia sẻ quyền truy cập delete (ví dụ: được tạo thông qua :func:`open` tích hợp sẵn) phải được đóng trước khi thoát khỏi context manager; nếu không, lệnh gọi :func:`os.unlink` khi context manager thoát sẽ thất bại với lỗi :exc:`PermissionError`.

   Trên Windows, nếu *delete_on_close* là false và tệp được tạo trong một thư mục mà người dùng không có quyền truy cập delete, thì lệnh gọi :func:`os.unlink` khi context manager thoát sẽ thất bại với lỗi :exc:`PermissionError`. Điều này không thể xảy ra khi *delete_on_close* là true, vì thao tác mở sẽ yêu cầu quyền truy cập delete và thất bại ngay lập tức nếu quyền truy cập được yêu cầu không được cấp.

   Chỉ trên POSIX, một tiến trình bị kết thúc đột ngột bằng SIGKILL không thể tự động xóa bất kỳ NamedTemporaryFiles nào mà nó đã tạo.

   .. audit-event:: tempfile.mkstemp fullpath tempfile.NamedTemporaryFile

   .. versionchanged:: 3.8
      Đã thêm tham số *errors*.

   .. versionchanged:: 3.12
      Đã thêm tham số *delete_on_close*.


.. class:: SpooledTemporaryFile(max_size=0, mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, *, errors=None)

   Lớp này hoạt động chính xác như :func:`TemporaryFile`, ngoại trừ việc dữ liệu được lưu tạm trong bộ nhớ cho đến khi kích thước tệp vượt quá *max_size*, hoặc cho đến khi phương thức :func:`~io.IOBase.fileno` của tệp được gọi; tại thời điểm đó, nội dung được ghi vào đĩa và quá trình hoạt động tiếp tục như với
   :func:`TemporaryFile`.

   .. method:: SpooledTemporaryFile.rollover

      Tệp kết quả có thêm một phương thức, :meth:`!rollover`, khiến tệp chuyển sang tệp trên đĩa bất kể kích thước của nó.

   Đối tượng được trả về là một đối tượng giống tệp, có thuộc tính :attr:`!_file` là một đối tượng :class:`io.BytesIO` hoặc :class:`io.TextIOWrapper` (tùy thuộc vào việc chỉ định *mode* nhị phân hay văn bản), hoặc là một đối tượng tệp thực, tùy thuộc vào việc :meth:`rollover` đã được gọi hay chưa. Đối tượng giống tệp này có thể được sử dụng trong câu lệnh :keyword:`with`, giống như một tệp thông thường.

   .. versionchanged:: 3.3
      Phương thức truncate hiện chấp nhận đối số *size*.

   .. versionchanged:: 3.8
      Đã thêm tham số *errors*.

   .. versionchanged:: 3.11
      Triển khai đầy đủ :class:`io.BufferedIOBase` và
      các lớp cơ sở trừu tượng :class:`io.TextIOBase` (tùy thuộc vào việc chỉ định *chế độ nhị phân hoặc văn bản*).


.. class:: TemporaryDirectory(suffix=None, prefix=None, dir=None, ignore_cleanup_errors=False, *, delete=True)

   Lớp này tạo một thư mục tạm thời một cách an toàn, sử dụng cùng các quy tắc như :func:`mkdtemp`. Đối tượng kết quả có thể được sử dụng như một :term:`context manager` (xem
   :ref:`tempfile-examples`). Khi ngữ cảnh kết thúc hoặc đối tượng thư mục tạm thời bị hủy, thư mục tạm thời mới tạo cùng toàn bộ nội dung của nó sẽ bị xóa khỏi hệ thống tệp.

   .. attribute:: TemporaryDirectory.name

      Có thể lấy tên thư mục từ thuộc tính :attr:`!name` của đối tượng được trả về. Khi đối tượng được trả về được sử dụng như một :term:`context manager`, thì
      :attr:`!name` sẽ được gán cho đích của mệnh đề :keyword:`!as` trong câu lệnh :keyword:`with`, nếu có.

   .. method:: TemporaryDirectory.cleanup

      Có thể dọn dẹp thư mục một cách rõ ràng bằng cách gọi
      phương thức :meth:`!cleanup`. Nếu *ignore_cleanup_errors* là true, mọi ngoại lệ chưa được xử lý trong quá trình dọn dẹp tường minh hoặc ngầm (chẳng hạn như
      :exc:`PermissionError` việc xóa các tệp đang mở trên Windows) sẽ bị bỏ qua, còn các mục còn lại có thể xóa được sẽ bị xóa trên cơ sở "cố gắng hết sức". Nếu không, lỗi sẽ được phát sinh trong bất kỳ bối cảnh nào mà việc dọn dẹp diễn ra (cuộc gọi :meth:`!cleanup` , khi thoát khỏi context manager, khi đối tượng được garbage-collected hoặc trong quá trình interpreter shutdown).

   Có thể sử dụng tham số *delete* để tắt việc dọn dẹp cây thư mục khi thoát khỏi context. Mặc dù việc một context manager tắt hành động được thực hiện khi thoát có vẻ bất thường, điều này có thể hữu ích khi gỡ lỗi hoặc khi bạn cần hành vi dọn dẹp của mình phụ thuộc có điều kiện vào logic khác.

   .. audit-event:: tempfile.mkdtemp fullpath tempfile.TemporaryDirectory

   .. versionadded:: 3.2

   .. versionchanged:: 3.10
      Đã thêm tham số *ignore_cleanup_errors*.

   .. versionchanged:: 3.12
      Đã thêm tham số *delete*.


.. function:: mkstemp(suffix=None, prefix=None, dir=None, text=False)

   Tạo một tệp tạm thời theo cách bảo mật nhất có thể. Không xảy ra điều kiện tranh chấp trong quá trình tạo tệp, với điều kiện nền tảng triển khai đúng :const:`os.O_EXCL` flag cho :func:`os.open`. Tệp chỉ có thể được đọc và ghi bởi user ID tạo ra nó. Nếu nền tảng sử dụng các bit quyền để cho biết tệp có thể thực thi hay không, thì không ai có thể thực thi tệp này.

   File descriptor này :ref:`không được kế thừa bởi các tiến trình con <fd_inheritance>`.

   Không giống như :func:`TemporaryFile`, người dùng :func:`mkstemp` chịu trách nhiệm đóng file descriptor (ví dụ: sử dụng :func:`os.close`) và xóa tệp tạm thời (ví dụ: sử dụng :func:`os.remove`).

   Nếu *suffix* không phải là ``None``, tên tệp sẽ kết thúc bằng hậu tố đó; nếu không, tệp sẽ không có hậu tố. :func:`mkstemp` không chèn dấu chấm giữa tên tệp và hậu tố; nếu cần, hãy đặt dấu chấm ở đầu *suffix*.

   Nếu *prefix* không phải là ``None``, tên tệp sẽ bắt đầu bằng tiền tố đó; nếu không, tiền tố mặc định sẽ được sử dụng. Giá trị mặc định là giá trị trả về của
   :func:`gettempprefix` hoặc :func:`gettempprefixb`, tùy trường hợp.

   Nếu *dir* không phải là ``None``, tệp sẽ được tạo trong thư mục đó; nếu không, một thư mục mặc định sẽ được sử dụng. Thư mục mặc định được chọn từ một danh sách phụ thuộc vào nền tảng, nhưng người dùng ứng dụng có thể kiểm soát vị trí thư mục bằng cách đặt các biến môi trường *TMPDIR*, *TEMP* hoặc *TMP*. Do đó, không có gì đảm bảo rằng tên tệp được tạo sẽ có các thuộc tính thuận tiện, chẳng hạn như không cần đặt trong dấu ngoặc kép khi truyền cho các lệnh bên ngoài thông qua ``os.popen()``.

   Nếu bất kỳ đối số nào trong số *suffix*, *prefix* và *dir* không phải là ``None``, chúng phải cùng kiểu. Nếu chúng là bytes, tên được trả về sẽ là bytes thay vì str. Nếu muốn buộc giá trị trả về là bytes trong khi vẫn giữ hành vi mặc định, hãy truyền ``suffix=b''``.

   Nếu *text* được chỉ định và có giá trị true, tệp sẽ được mở ở chế độ văn bản. Nếu không, tệp sẽ được mở ở chế độ nhị phân (mặc định).

   :func:`mkstemp` trả về một tuple chứa handle cấp hệ điều hành đến một tệp đang mở (như được :func:`os.open` trả về) và pathname tuyệt đối của tệp đó, theo thứ tự này.

   .. audit-event:: tempfile.mkstemp fullpath tempfile.mkstemp

   .. versionchanged:: 3.5
      *suffix*, *prefix* và *dir* giờ đây có thể được cung cấp dưới dạng bytes để nhận về giá trị kiểu bytes. Trước đây, chỉ str mới được phép. *suffix* và *prefix* giờ đây chấp nhận và mặc định là ``None`` để sử dụng giá trị mặc định thích hợp.

   .. versionchanged:: 3.6
      Tham số *dir* giờ đây chấp nhận một :term:`path-like object`.


.. function:: mkdtemp(suffix=None, prefix=None, dir=None)

   Tạo một thư mục tạm thời theo cách bảo mật nhất có thể. Không có điều kiện tranh đua nào trong quá trình tạo thư mục. Chỉ user ID tạo thư mục mới có quyền đọc, ghi và tìm kiếm trong thư mục đó.

   Người dùng :func:`mkdtemp` có trách nhiệm xóa thư mục tạm thời và nội dung của thư mục khi không còn sử dụng.

   Các đối số *prefix*, *suffix* và *dir* giống như đối với
   :func:`mkstemp`.

   :func:`mkdtemp` trả về pathname tuyệt đối của thư mục mới.

   .. audit-event:: tempfile.mkdtemp fullpath tempfile.mkdtemp

   .. versionchanged:: 3.5
      *suffix*, *prefix* và *dir* giờ đây có thể được cung cấp dưới dạng bytes để nhận về giá trị kiểu bytes. Trước đây, chỉ str mới được phép. *suffix* và *prefix* giờ đây chấp nhận và mặc định là ``None`` để sử dụng giá trị mặc định thích hợp.

   .. versionchanged:: 3.6
      Tham số *dir* giờ đây chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.12
      :func:`mkdtemp` now always returns an absolute path, even if *dir* is relative.


.. function:: gettempdir()

   Trả về tên của thư mục được dùng cho các tệp tạm thời. Giá trị này xác định giá trị mặc định cho đối số *dir* của tất cả các hàm trong mô-đun này.

   Python tìm kiếm một danh sách thư mục tiêu chuẩn để tìm thư mục mà người dùng gọi hàm có thể tạo tệp trong đó. Danh sách này là:

   #. Thư mục được chỉ định bởi biến môi trường :envvar:`TMPDIR`.

   #. Thư mục được chỉ định bởi biến môi trường :envvar:`TEMP`.

   #. Thư mục được chỉ định bởi biến môi trường :envvar:`TMP`.

   #. Vị trí dành riêng cho nền tảng:

      * Trên Windows, các thư mục
        :file:`%USERPROFILE%\\AppData\\Local\\Temp`,
        :file:`%SYSTEMROOT%\\Temp`, :file:`C:\\TEMP`,
        :file:`C:\\TMP`, :file:`\\TEMP`, và
        :file:`\\TMP`, theo thứ tự đó.

      * Trên tất cả các nền tảng khác, các thư mục :file:`/tmp`, :file:`/var/tmp`, và
        :file:`/usr/tmp`, theo thứ tự đó.

   #. Cuối cùng, thư mục làm việc hiện tại.

   Kết quả của tìm kiếm này được lưu vào bộ nhớ đệm, xem phần mô tả của
   :data:`tempdir` bên dưới.

   .. versionchanged:: 3.10

      Luôn trả về một str. Trước đây, hàm sẽ trả về bất kỳ giá trị :data:`tempdir` nào bất kể kiểu dữ liệu, miễn là giá trị đó không phải là ``None``.

.. function:: gettempdirb()

   Tương tự như :func:`gettempdir`, nhưng giá trị trả về ở dạng bytes.

   .. versionadded:: 3.5

.. function:: gettempprefix()

   Trả về tiền tố tên tệp được dùng để tạo các tệp tạm thời. Tiền tố này không chứa thành phần thư mục.

.. function:: gettempprefixb()

   Tương tự như :func:`gettempprefix`, nhưng giá trị trả về ở dạng bytes.

   .. versionadded:: 3.5

Module này sử dụng một biến toàn cục để lưu tên thư mục được dùng cho các tệp tạm thời do :func:`gettempdir` trả về. Có thể đặt trực tiếp biến này để ghi đè quá trình lựa chọn, nhưng không nên làm vậy. Tất cả các hàm trong module này nhận một đối số *dir*, dùng để chỉ định thư mục. Đây là cách được khuyến nghị vì không làm thay đổi hành vi API toàn cục và gây bất ngờ cho các đoạn mã khác.

.. data:: tempdir

   Khi được đặt thành một giá trị khác ``None``, biến này xác định giá trị mặc định cho đối số *dir* của các hàm được định nghĩa trong module này, bao gồm kiểu của đối số đó là bytes hay str. Đối số này không thể là
   :term:`path-like object`.

   Nếu ``tempdir`` là ``None`` (giá trị mặc định) trong bất kỳ lần gọi nào đến các hàm nêu trên, ngoại trừ :func:`gettempprefix`, thì nó được khởi tạo theo thuật toán được mô tả trong :func:`gettempdir`.

   .. note::

      Lưu ý rằng nếu bạn đặt ``tempdir`` thành một giá trị bytes, sẽ có một tác dụng phụ khó chịu: Kiểu trả về mặc định toàn cục của
      :func:`mkstemp` và :func:`mkdtemp` sẽ chuyển thành bytes khi không cung cấp rõ ràng các đối số ``prefix``, ``suffix`` hoặc ``dir`` có kiểu str. Vui lòng không viết mã dựa vào hoặc phụ thuộc vào điều này. Hành vi bất tiện này được duy trì để tương thích với cách triển khai trước đây.

.. _tempfile-examples:

Ví dụ
-----

Sau đây là một số ví dụ về cách sử dụng điển hình của module :mod:`!tempfile`::

    >>> import tempfile

    # tạo một tệp tạm thời và ghi một số dữ liệu vào đó
    >>> fp = tempfile.TemporaryFile()
    >>> fp.write(b'Hello world!')
    # đọc dữ liệu từ tệp
    >>> fp.seek(0)
    >>> fp.read()
    b'Hello world!'
    # đóng tệp, tệp sẽ bị xóa
    >>> fp.close()

    # tạo tệp tạm thời bằng trình quản lý ngữ cảnh
    >>> with tempfile.TemporaryFile() as fp:
    ...     fp.write(b'Hello world!')
    ...     fp.seek(0)
    ...     fp.read()
    b'Hello world!'
    >>>
    # tệp hiện đã được đóng và xóa

    # tạo tệp tạm thời bằng trình quản lý ngữ cảnh
    # đóng tệp, sử dụng tên để mở lại tệp
    >>> with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
    ...     fp.write(b'Hello world!')
    ...     fp.close()
    ... # tệp đã được đóng nhưng chưa bị xóa
    ... # mở lại tệp bằng cách sử dụng tên của nó
    ...     with open(fp.name, mode='rb') as f:
    ...         f.read()
    b'Hello world!'
    >>>
    # tệp hiện đã bị xóa

    # tạo một thư mục tạm thời bằng context manager
    >>> with tempfile.TemporaryDirectory() as tmpdirname:
    ...     print('created temporary directory', tmpdirname)
    >>>
    # thư mục và nội dung đã bị xóa

.. _tempfile-mktemp-deprecated:

Các hàm và biến đã lỗi thời
---------------------------

Một cách trước đây để tạo tệp tạm thời là trước tiên tạo tên tệp bằng hàm :func:`mktemp`, sau đó tạo tệp bằng tên này. Tuy nhiên, cách này không an toàn, vì một tiến trình khác có thể tạo tệp bằng tên này trong khoảng thời gian giữa lần gọi :func:`mktemp` và lần thử tiếp theo của tiến trình đầu tiên để tạo tệp. Giải pháp là kết hợp hai bước này và tạo tệp ngay lập tức. Cách tiếp cận này được :func:`mkstemp` và các hàm khác được mô tả ở trên sử dụng.

.. function:: mktemp(suffix='', prefix='tmp', dir=None)

   .. deprecated:: 2.3
      Thay vào đó, hãy sử dụng :func:`mkstemp`.

   Trả về một pathname tuyệt đối của một tệp không tồn tại tại thời điểm thực hiện lệnh gọi. Các đối số *prefix*, *suffix* và *dir* tương tự như các đối số của :func:`mkstemp`, ngoại trừ việc không hỗ trợ tên tệp dạng bytes, ``suffix=None`` và ``prefix=None``.

   .. warning::

      Việc sử dụng hàm này có thể tạo ra lỗ hổng bảo mật trong chương trình của bạn. Đến khi bạn bắt đầu thực hiện bất kỳ thao tác nào với tên tệp mà hàm trả về, người khác có thể đã nhanh tay sử dụng nó trước bạn. Có thể dễ dàng thay thế việc sử dụng :func:`mktemp` bằng :func:`NamedTemporaryFile`, truyền cho nó tham số ``delete=False``::

         >>> f = NamedTemporaryFile(delete=False)
         >>> f.name
         '/tmp/tmptjujjt'
         >>> f.write(b"Hello World!\n")
         13
         >>> f.close()
         >>> os.unlink(f.name)
         >>> os.path.exists(f.name)
         False
