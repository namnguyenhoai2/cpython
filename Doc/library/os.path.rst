:mod:`!os.path` --- Các thao tác phổ biến với pathname
======================================================

.. module:: os.path
   :synopsis: Các thao tác trên pathname.

**Mã nguồn:** :source:`Lib/genericpath.py`, :source:`Lib/posixpath.py` (cho POSIX) và
:source:`Lib/ntpath.py` (cho Windows).

.. index:: single: path; operations

--------------

Mô-đun này triển khai một số hàm hữu ích trên pathname. Để đọc hoặc ghi tệp, hãy xem :func:`open`, còn để truy cập hệ thống tệp, hãy xem mô-đun :mod:`os`. Các tham số đường dẫn có thể được truyền dưới dạng chuỗi, bytes hoặc bất kỳ đối tượng nào triển khai giao thức :class:`os.PathLike`.

Không giống như Unix shell, Python không thực hiện bất kỳ việc mở rộng đường dẫn *tự động* nào. Các hàm như :func:`expanduser` và :func:`expandvars` có thể được gọi một cách rõ ràng khi ứng dụng cần mở rộng đường dẫn giống shell. (Xem thêm mô-đun :mod:`glob`.)


.. seealso::
   Mô-đun :mod:`pathlib` cung cấp các đối tượng đường dẫn cấp cao.


.. note::

   Tất cả các hàm này chỉ chấp nhận các đối số là đối tượng bytes hoặc chỉ là đối tượng chuỗi. Nếu trả về một đường dẫn hoặc tên tệp, kết quả sẽ là một đối tượng cùng kiểu.

.. note::

   Vì các hệ điều hành khác nhau có quy ước đặt tên đường dẫn khác nhau nên thư viện chuẩn có một số phiên bản của mô-đun này.
   :mod:`!os.path` mô-đun luôn là mô-đun đường dẫn phù hợp với hệ điều hành mà Python đang chạy, do đó có thể dùng cho các đường dẫn cục bộ. Tuy nhiên, bạn cũng có thể import và sử dụng từng mô-đun riêng lẻ nếu muốn thao tác với một đường dẫn *luôn* ở một trong các định dạng khác nhau. Tất cả đều có cùng một interface:

   * :mod:`!posixpath` cho các đường dẫn kiểu UNIX
   * :mod:`!ntpath` cho các đường dẫn Windows


.. versionchanged:: 3.8

   :func:`exists`, :func:`lexists`, :func:`isdir`, :func:`isfile`,
   :func:`islink` và :func:`ismount` hiện trả về ``False`` thay vì phát sinh ngoại lệ đối với các đường dẫn chứa ký tự hoặc byte không thể biểu diễn ở cấp hệ điều hành.


.. function:: abspath(path)

   Trả về phiên bản tuyệt đối đã chuẩn hóa của tên đường dẫn *path*. Trên hầu hết các nền tảng, kết quả này tương đương với việc gọi ``normpath(join(os.getcwd(), path))``.

   Trên Windows, đường dẫn được hệ điều hành chuẩn hóa, do đó kết quả có thể khác với ``normpath(join(os.getcwd(), path))``. Đường dẫn tương đối theo ổ đĩa được phân giải dựa trên thư mục hiện tại của ổ đĩa được chỉ định và ký tự ổ đĩa được viết hoa. Các dấu chấm và khoảng trắng ở cuối sẽ bị loại bỏ. Ví dụ::

      >>> os.path.abspath('c:spam')
      'C:\\Temp\\spam'
      >>> os.path.abspath('c:/temp/spam. . .')
      'c:\\temp\\spam'

   .. seealso:: :func:`os.path.join` và :func:`os.path.normpath`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: basename(path, /)

   Trả về tên cơ sở của pathname *path*. Đây là phần tử thứ hai trong cặp được trả về khi truyền *path* cho hàm :func:`split`. Lưu ý rằng kết quả của hàm này khác với chương trình Unix :program:`basename`; trong đó :program:`basename` cho ``'/foo/bar/'`` trả về ``'bar'``, còn hàm :func:`basename` trả về một chuỗi rỗng (``''``).

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: commonpath(paths)

   Trả về đường dẫn con chung dài nhất của mỗi pathname trong iterable *paths*. Ném :exc:`ValueError` nếu *paths* chứa cả pathname tuyệt đối và tương đối, nếu *paths* nằm trên các ổ đĩa khác nhau hoặc nếu *paths* rỗng. Không giống :func:`commonprefix`, hàm này trả về một đường dẫn hợp lệ.

   .. versionadded:: 3.5

   .. versionchanged:: 3.6
      Chấp nhận một chuỗi các :term:`path-like objects <path-like object>`.

   .. versionchanged:: 3.13
      Giờ đây có thể truyền vào bất kỳ iterable nào, thay vì chỉ các sequence.


.. function:: commonprefix(list, /)

   Trả về tiền tố chuỗi dài nhất (được lấy theo từng ký tự) là tiền tố của tất cả các chuỗi trong *list*. Nếu *list* trống, trả về chuỗi rỗng (``''``).

   .. warning::

      Hàm này có thể trả về các path không hợp lệ vì nó xử lý từng ký tự một. Nếu bạn cần **common path prefix**, thì thuật toán được triển khai trong hàm này không an toàn. Hãy dùng
      :func:`commonpath` để tìm common path prefix.

      ::

        >>> os.path.commonprefix(['/usr/lib', '/usr/local/lib'])
        '/usr/l'

        >>> os.path.commonpath(['/usr/lib', '/usr/local/lib'])
        '/usr'

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: dirname(path, /)

   Trả về tên thư mục của pathname *path*. Đây là phần tử đầu tiên trong cặp được trả về khi truyền *path* vào hàm :func:`split`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: exists(path)

   Trả về ``True`` nếu *path* trỏ đến một đường dẫn hiện có hoặc một file descriptor đang mở. Trả về ``False`` đối với các liên kết tượng trưng bị hỏng. Trên một số nền tảng, hàm này có thể trả về ``False`` nếu không được cấp quyền thực thi :func:`os.stat` trên tệp được yêu cầu, ngay cả khi *path* thực sự tồn tại.

   .. versionchanged:: 3.3
      *path* giờ đây có thể là một số nguyên: ``True`` được trả về nếu đó là một
       file descriptor đang mở, ngược lại là ``False``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: lexists(path)

   Trả về ``True`` nếu *path* trỏ đến một đường dẫn hiện có, bao gồm cả các liên kết tượng trưng bị hỏng.   Tương đương với :func:`exists` trên các nền tảng không hỗ trợ
   :func:`os.lstat`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. index:: single: ~ (tilde); home directory expansion

.. function:: expanduser(path)

   Trên Unix và Windows, trả về đối số với thành phần đầu tiên là ``~`` hoặc ``~user`` được thay thế bằng thư mục chính của *user*.

   .. index:: pair: module; pwd

   Trên Unix, ``~`` ở đầu được thay thế bằng biến môi trường :envvar:`HOME` nếu biến này được thiết lập; nếu không, thư mục chính của người dùng hiện tại được tra cứu trong cơ sở dữ liệu mật khẩu thông qua mô-đun tích hợp :mod:`pwd`. ``~user`` ở đầu được tra cứu trực tiếp trong cơ sở dữ liệu mật khẩu.

   Trên Windows, :envvar:`USERPROFILE` sẽ được sử dụng nếu được thiết lập; nếu không, kết hợp giữa :envvar:`HOMEPATH` và :envvar:`HOMEDRIVE` sẽ được sử dụng. ``~user`` ở đầu được xử lý bằng cách kiểm tra xem thành phần thư mục cuối cùng trong thư mục chính của người dùng hiện tại có khớp với :envvar:`USERNAME` hay không, rồi thay thế thành phần đó nếu khớp.

   Nếu việc mở rộng không thành công hoặc đường dẫn không bắt đầu bằng dấu ngã, đường dẫn sẽ được trả về mà không thay đổi.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.8
      Không còn sử dụng :envvar:`HOME` trên Windows.

.. index::
   single: $ (dollar); environment variables expansion
   single: % (percent); environment variables expansion (Windows)

.. function:: expandvars(path)

   Trả về đối số với các biến môi trường đã được mở rộng. Các chuỗi con có dạng ``$name`` hoặc ``${name}`` được thay thế bằng giá trị của biến môi trường *name*. Tên biến không hợp lệ và các tham chiếu đến biến không tồn tại được giữ nguyên.

   Trên Windows, các phần mở rộng ``%name%`` được hỗ trợ bên cạnh ``$name`` và ``${name}``.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: getatime(path, /)

   Trả về thời điểm truy cập gần nhất của *path*. Giá trị trả về là một số dấu phẩy động biểu thị số giây kể từ epoch (xem mô-đun :mod:`time`). Phát sinh
   :exc:`OSError` nếu tệp không tồn tại hoặc không thể truy cập.


.. function:: getmtime(path, /)

   Trả về thời điểm sửa đổi gần nhất của *path*. Giá trị trả về là một số dấu phẩy động biểu thị số giây kể từ epoch (xem mô-đun :mod:`time`). Phát sinh :exc:`OSError` nếu tệp không tồn tại hoặc không thể truy cập.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: getctime(path, /)

   Trả về ctime của hệ thống, trên một số hệ thống (như Unix) là thời điểm thay đổi siêu dữ liệu gần nhất, còn trên các hệ thống khác (như Windows) là thời điểm tạo *path*. Giá trị trả về là một số biểu thị số giây kể từ epoch (xem mô-đun :mod:`time`). Phát sinh :exc:`OSError` nếu tệp không tồn tại hoặc không thể truy cập.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: getsize(path, /)

   Trả về kích thước, tính bằng byte, của *path*. Ném :exc:`OSError` nếu tệp không tồn tại hoặc không thể truy cập.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: isabs(path, /)

   Trả về ``True`` nếu *path* là tên đường dẫn tuyệt đối. Trên Unix, điều đó có nghĩa là tên đường dẫn bắt đầu bằng dấu gạch chéo, còn trên Windows, tên đường dẫn bắt đầu bằng hai dấu gạch chéo ngược, hoặc gồm một ký tự ổ đĩa, dấu hai chấm và dấu gạch chéo ngược.

   .. seealso:: :func:`abspath`

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.13
      Trên Windows, trả về ``False`` nếu đường dẫn đã cho bắt đầu bằng chính xác một dấu gạch chéo ngược.


.. function:: isfile(path)

   Trả về ``True`` nếu *path* là một :func:`existing <exists>` tệp thông thường. Hàm này đi theo các symbolic link, vì vậy cả :func:`islink` và :func:`isfile` đều có thể đúng với cùng một đường dẫn.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: isdir(path, /)

   Trả về ``True`` nếu *path* là một thư mục :func:`existing <exists>`. Thao tác này lần theo các symbolic link, vì vậy cả :func:`islink` và :func:`isdir` đều có thể đúng với cùng một đường dẫn.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: isjunction(path)

   Trả về ``True`` nếu *path* tham chiếu đến một mục thư mục :func:`existing <lexists>` là junction. Luôn trả về ``False`` nếu nền tảng hiện tại không hỗ trợ junction.

   .. versionadded:: 3.12


.. function:: islink(path)

   Trả về ``True`` nếu *path* tham chiếu đến một mục thư mục :func:`existing <exists>` là symbolic link. Luôn ``False`` nếu Python runtime không hỗ trợ symbolic link.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: ismount(path)

   Trả về ``True`` nếu pathname *path* là một :dfn:`mount point`: một điểm trong hệ thống tệp nơi một hệ thống tệp khác được mount. Trên POSIX, hàm này kiểm tra xem thư mục cha của *path*, là :file:`{path}/..`, có nằm trên thiết bị khác với *path* hay không, hoặc liệu :file:`{path}/..` và *path* có trỏ đến cùng một i-node trên cùng một thiết bị hay không --- điều này sẽ phát hiện mount point trên mọi biến thể Unix và POSIX. Hàm này không thể phát hiện một cách đáng tin cậy các bind mount trên cùng một hệ thống tệp. Trên các hệ thống Linux, hàm sẽ luôn trả về ``True`` cho các subvolume btrfs, ngay cả khi chúng không phải là mount point. Trên Windows, thư mục gốc của drive letter và một share UNC luôn là mount point; với mọi đường dẫn khác, ``GetVolumePathName`` được gọi để kiểm tra xem nó có khác với đường dẫn đầu vào hay không.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ phát hiện các mount point không phải thư mục gốc trên Windows.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: isdevdrive(path)

   Trả về ``True`` nếu pathname *path* nằm trên Windows Dev Drive. Dev Drive được tối ưu hóa cho các tình huống dành cho nhà phát triển và mang lại hiệu suất cao hơn khi đọc và ghi tệp. Dev Drive được khuyến nghị sử dụng cho mã nguồn, thư mục build tạm thời, bộ nhớ đệm package và các thao tác sử dụng nhiều IO khác.

   Có thể phát sinh lỗi đối với đường dẫn không hợp lệ, chẳng hạn như đường dẫn không có ổ đĩa được nhận dạng, nhưng trả về ``False`` trên các nền tảng không hỗ trợ Dev Drive. Xem `tài liệu Windows <https://learn.microsoft.com/windows/dev-drive/>`_ để biết thông tin về cách bật và tạo Dev Drive.

   .. versionadded:: 3.12

   .. versionchanged:: 3.13
      Hàm này hiện khả dụng trên tất cả các nền tảng và sẽ luôn trả về ``False`` trên những nền tảng không hỗ trợ Dev Drive


.. function:: isreserved(path)

   Trả về ``True`` nếu *path* là pathname dành riêng trên hệ thống hiện tại.

   Trên Windows, các tên tệp dành riêng bao gồm những tên kết thúc bằng dấu cách hoặc dấu chấm; những tên chứa dấu hai chấm (tức là các luồng tệp như "name:stream"), ký tự đại diện (tức là ``'*?"<>'``), ký tự pipe hoặc ký tự điều khiển ASCII; cũng như các tên thiết bị DOS như "NUL", "CON", "CONIN$", "CONOUT$", "AUX", "PRN", "COM1" và "LPT1".

   .. note::

      Hàm này mô phỏng các quy tắc dành cho đường dẫn dành riêng trên hầu hết các hệ thống Windows. Các quy tắc này thay đổi theo thời gian trong những bản phát hành Windows khác nhau. Hàm này có thể được cập nhật trong các bản phát hành Python tương lai khi những thay đổi đối với các quy tắc được cung cấp rộng rãi.

   .. availability:: Windows.

   .. versionadded:: 3.13


.. function:: join(path, /, *paths)

   Nối một hoặc nhiều đoạn đường dẫn một cách hợp lý. Giá trị trả về là phép nối của *path* và tất cả các phần tử của *\*paths*, với chính xác một dấu phân cách thư mục sau mỗi phần không rỗng, ngoại trừ phần cuối. Nghĩa là, kết quả chỉ kết thúc bằng dấu phân cách nếu phần cuối cùng либо rỗng hoặc kết thúc bằng một dấu phân cách.

   Nếu một đoạn là đường dẫn tuyệt đối (trên Windows cần có cả ổ đĩa và thư mục gốc), thì tất cả các đoạn trước đó sẽ bị bỏ qua và việc nối tiếp tục từ đoạn đường dẫn tuyệt đối. Ví dụ, trên Linux::

      >>> os.path.join('/home/foo', 'bar')
      '/home/foo/bar'
      >>> os.path.join('/home/foo', '/home/bar')
      '/home/bar'

   Trên Windows, ổ đĩa không được đặt lại khi gặp một đoạn đường dẫn có thư mục gốc (ví dụ: ``r'\foo'``). Nếu một đoạn nằm trên ổ đĩa khác hoặc là đường dẫn tuyệt đối, tất cả các đoạn trước đó sẽ bị bỏ qua và ổ đĩa được đặt lại. Ví dụ::

      >>> os.path.join('c:\\', 'foo')
      'c:\\foo'
      >>> os.path.join('c:\\foo', 'd:\\bar')
      'd:\\bar'

   Lưu ý rằng vì mỗi ổ đĩa có một thư mục hiện tại, ``os.path.join("c:", "foo")`` biểu thị một đường dẫn tương đối so với thư mục hiện tại trên ổ đĩa :file:`C:` (:file:`c:foo`), chứ không phải :file:`c:\\foo`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *path* và *paths*.


.. function:: normcase(path, /)

   Chuẩn hóa kiểu chữ của một đường dẫn. Trên Windows, chuyển tất cả ký tự trong đường dẫn thành chữ thường, đồng thời chuyển dấu gạch chéo xuôi thành dấu gạch chéo ngược. Trên các hệ điều hành khác, trả về đường dẫn không thay đổi.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: normpath(path)

   Chuẩn hóa một pathname bằng cách gộp các dấu phân cách dư thừa và các tham chiếu lên cấp trên để ``A//B``, ``A/B/``, ``A/./B`` và ``A/foo/../B`` đều trở thành ``A/B``. Thao tác trên chuỗi này có thể làm thay đổi ý nghĩa của một đường dẫn chứa symbolic link. Trên Windows, hàm chuyển dấu gạch chéo xuôi thành dấu gạch chéo ngược. Để chuẩn hóa chữ hoa chữ thường, hãy sử dụng :func:`normcase`.

   .. note::
      Trên các hệ thống POSIX, theo `Tiêu chuẩn IEEE Std 1003.1, Ấn bản 2013; 4.13 Giải quyết pathname <https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html#tag_04_13>`_, nếu một pathname bắt đầu bằng chính xác hai dấu gạch chéo, thành phần đầu tiên sau các ký tự mở đầu có thể được diễn giải theo cách do từng implementation quy định, mặc dù nhiều hơn hai ký tự mở đầu sẽ được xử lý như một ký tự duy nhất.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: realpath(path, /, *, strict=False)

   Trả về đường dẫn chuẩn của filename được chỉ định, loại bỏ mọi symbolic link gặp phải trong đường dẫn (nếu hệ điều hành hỗ trợ). Trên Windows, hàm này cũng sẽ phân giải các tên theo kiểu MS-DOS (còn gọi là 8.3), chẳng hạn như ``C:\\PROGRA~1`` thành ``C:\\Program Files``. Đường dẫn trả về sử dụng kiểu chữ do hệ điều hành cung cấp, có thể khác với kiểu chữ của *path*; cụ thể, ký tự ổ đĩa được viết hoa.

   Theo mặc định, đường dẫn được đánh giá cho đến thành phần đầu tiên không tồn tại, là một vòng lặp symlink hoặc việc đánh giá thành phần đó gây ra :exc:`OSError`. Tất cả các thành phần như vậy được nối nguyên trạng vào phần hiện có của đường dẫn.

   Một số lỗi được xử lý theo cách này bao gồm "access denied", "not a directory" hoặc "bad argument to internal function". Vì vậy, đường dẫn kết quả có thể không tồn tại hoặc không thể truy cập, vẫn có thể chứa link hoặc vòng lặp và có thể đi qua các đối tượng không phải thư mục.

   Có thể thay đổi hành vi này bằng các keyword argument:

   Nếu *strict* là ``True``, lỗi đầu tiên gặp phải khi đánh giá đường dẫn sẽ được ném lại. Cụ thể, :exc:`FileNotFoundError` sẽ được ném nếu *path* không tồn tại, hoặc một :exc:`OSError` khác nếu đường dẫn không thể truy cập vì lý do khác.

   Nếu *strict* là :py:data:`os.path.ALLOW_MISSING`, các lỗi khác ngoài
   :exc:`FileNotFoundError` sẽ được ném lại (như với ``strict=True``). Do đó, đường dẫn được trả về sẽ không chứa liên kết tượng trưng nào, nhưng tệp được chỉ định và một số thư mục cha của nó có thể không tồn tại.

   .. note::
      Hàm này mô phỏng quy trình của hệ điều hành để tạo đường dẫn canonical, quy trình này hơi khác nhau giữa Windows và UNIX về cách các liên kết tương tác với các thành phần đường dẫn tiếp theo.

      Các API của hệ điều hành tạo đường dẫn canonical khi cần, vì vậy thông thường không cần gọi hàm này.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.8
      Các liên kết tượng trưng và junction hiện được phân giải trên Windows.

   .. versionchanged:: 3.10
      Tham số *strict* đã được thêm.

   .. versionchanged:: 3.14
      Giá trị :py:data:`~os.path.ALLOW_MISSING` của tham số *strict* đã được thêm.

.. data:: ALLOW_MISSING

   Giá trị đặc biệt được sử dụng cho đối số *strict* trong :func:`realpath`.

   .. versionadded:: 3.14

.. function:: relpath(path, start=os.curdir)

   Trả về đường dẫn tệp tương đối đến *path*, tính từ thư mục hiện tại hoặc từ thư mục *start* tùy chọn. Đây là phép tính đường dẫn: hệ thống tệp không được truy cập để xác nhận sự tồn tại hoặc loại của *path* hay *start*. Trên Windows, :exc:`ValueError` được phát sinh khi *path* và *start* nằm trên các ổ đĩa khác nhau.

   *start* mặc định là :data:`os.curdir`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: samefile(path1, path2, /)

   Trả về ``True`` nếu cả hai đối số đường dẫn đều trỏ đến cùng một tệp hoặc thư mục. Điều này được xác định bằng số thiết bị và số i-node, đồng thời một ngoại lệ sẽ được phát sinh nếu lệnh gọi :func:`os.stat` trên một trong hai đường dẫn không thành công.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ Windows.

   .. versionchanged:: 3.4
      Windows hiện sử dụng cùng một triển khai như tất cả các nền tảng khác.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: sameopenfile(fp1, fp2)

   Trả về ``True`` nếu các file descriptor *fp1* và *fp2* trỏ đến cùng một tệp.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ Windows.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: samestat(stat1, stat2, /)

   Trả về ``True`` nếu các tuple stat *stat1* và *stat2* trỏ đến cùng một tệp. Các cấu trúc này có thể được trả về bởi :func:`os.fstat`,
   :func:`os.lstat`, hoặc :func:`os.stat`. Hàm này triển khai phép so sánh nền tảng được :func:`samefile` và :func:`sameopenfile` sử dụng.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ Windows.


.. function:: split(path, /)

   Phân tách pathname *path* thành một cặp, ``(head, tail)`` trong đó *tail* là thành phần pathname cuối cùng còn *head* là mọi phần đứng trước nó. Phần *tail* sẽ không bao giờ chứa dấu gạch chéo; nếu *path* kết thúc bằng dấu gạch chéo, *tail* sẽ rỗng. Nếu không có dấu gạch chéo trong *path*, *head* sẽ rỗng. Nếu *path* rỗng, cả *head* và *tail* đều rỗng. Các dấu gạch chéo ở cuối sẽ bị loại bỏ khỏi *head* trừ khi đó là thư mục gốc (chỉ gồm một hoặc nhiều dấu gạch chéo). Trong mọi trường hợp, ``join(head, tail)`` trả về một đường dẫn đến cùng vị trí với *path* (nhưng các chuỗi có thể khác nhau). Cũng xem các hàm :func:`join`,
   :func:`dirname` và :func:`basename`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: splitdrive(path, /)

   Phân tách pathname *path* thành một cặp ``(drive, tail)`` trong đó *drive* là điểm gắn kết hoặc chuỗi rỗng. Trên các hệ thống không sử dụng đặc tả ổ đĩa, *drive* sẽ luôn là chuỗi rỗng. Trong mọi trường hợp, ``drive
   + tail`` sẽ giống với *path*.

   Trên Windows, tách pathname thành drive/UNC sharepoint và relative path.

   Nếu path chứa drive letter, drive sẽ chứa mọi thứ cho đến và bao gồm cả dấu hai chấm::

      >>> splitdrive("c:/dir")
      ("c:", "/dir")

   Nếu path chứa UNC path, drive sẽ chứa tên máy chủ và share::

      >>> splitdrive("//host/computer/dir")
      ("//host/computer", "/dir")

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: splitroot(path, /)

   Tách pathname *path* thành một tuple gồm 3 phần ``(drive, root, tail)`` trong đó *drive* là tên thiết bị hoặc mount point, *root* là một chuỗi các dấu phân cách sau drive, còn *tail* là mọi thứ sau root. Bất kỳ phần nào trong số này cũng có thể là chuỗi rỗng. Trong mọi trường hợp, ``drive + root + tail`` sẽ giống với *path*.

   Trên các hệ thống POSIX, *drive* luôn rỗng. *root* có thể rỗng (nếu *path* là relative), là một dấu gạch chéo xuôi (nếu *path* là absolute), hoặc hai dấu gạch chéo xuôi (do triển khai xác định theo `IEEE Std 1003.1-2017; 4.13 Pathname Resolution <https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html#tag_04_13>`_). Ví dụ::

      >>> splitroot('/home/sam')
      ('', '/', 'home/sam')
      >>> splitroot('//home/sam')
      ('', '//', 'home/sam')
      >>> splitroot('///home/sam')
      ('', '/', '//home/sam')

   Trên Windows, *drive* có thể rỗng, là tên drive-letter, UNC share hoặc tên thiết bị. *root* có thể rỗng, là dấu gạch chéo xuôi hoặc dấu gạch chéo ngược. Ví dụ::

      >>> splitroot('C:/Users/Sam')
      ('C:', '/', 'Users/Sam')
      >>> splitroot('//Server/Share/Users/Sam')
      ('//Server/Share', '/', 'Users/Sam')

   .. versionadded:: 3.12


.. function:: splitext(path, /)

   Tách pathname *path* thành một cặp ``(root, ext)`` sao cho ``root + ext == path``, còn phần mở rộng *ext* thì rỗng hoặc bắt đầu bằng dấu chấm và chứa nhiều nhất một dấu chấm.

   Nếu path không chứa phần mở rộng, *ext* sẽ là ``''``::

      >>> splitext('bar')
      ('bar', '')

   Nếu path chứa phần mở rộng, *ext* sẽ được đặt thành phần mở rộng này, bao gồm cả dấu chấm ở đầu. Lưu ý rằng các dấu chấm trước đó sẽ bị bỏ qua::

      >>> splitext('foo.bar.exe')
      ('foo.bar', '.exe')
      >>> splitext('/foo/bar.exe')
      ('/foo/bar', '.exe')

   Các dấu chấm ở đầu thành phần cuối cùng của path được xem là một phần của root::

      >>> splitext('.cshrc')
      ('.cshrc', '')
      >>> splitext('/foo/....jpg')
      ('/foo/....jpg', '')

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. data:: supports_unicode_filenames

   ``True`` nếu có thể sử dụng các chuỗi Unicode tùy ý làm tên tệp (trong các giới hạn do hệ thống tệp áp đặt).

.. _`the Windows documentation`: https://learn.microsoft.com/windows/dev-drive/
.. _`IEEE Std 1003.1 2013 Edition; 4.13 Pathname Resolution`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html#tag_04_13
.. _`IEEE Std 1003.1-2017; 4.13 Pathname Resolution`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html#tag_04_13
