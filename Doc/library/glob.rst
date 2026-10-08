:mod:`!glob` --- Mở rộng mẫu đường dẫn theo kiểu Unix
=====================================================

.. module:: glob
   :synopsis: Mở rộng mẫu đường dẫn theo kiểu Unix shell.

**Mã nguồn:** :source:`Lib/glob.py`

.. index:: single: filenames; pathname expansion

--------------

.. index::
   single: * (asterisk); in glob-style wildcards
   single: ? (question mark); in glob-style wildcards
   single: [] (square brackets); in glob-style wildcards
   single: ! (exclamation); in glob-style wildcards
   single: - (minus); in glob-style wildcards
   single: . (dot); in glob-style wildcards

Mô-đun :mod:`!glob` tìm các pathname bằng cách sử dụng các quy tắc khớp mẫu tương tự shell Unix. Không thực hiện mở rộng dấu ngã, nhưng ``*``, ``?`` và các dải ký tự được biểu diễn bằng ``[]`` sẽ được khớp chính xác. Việc này được thực hiện bằng cách phối hợp sử dụng các hàm :func:`os.scandir` và :func:`fnmatch.fnmatch`, chứ không thực sự gọi một subshell.

.. note::
   Các pathname được trả về theo thứ tự không cố định. Nếu cần một thứ tự cụ thể, hãy sắp xếp các kết quả.

Theo mặc định, các tệp bắt đầu bằng dấu chấm (``.``) chỉ có thể được khớp bằng các mẫu cũng bắt đầu bằng dấu chấm, không giống như :func:`fnmatch.fnmatch` hoặc :func:`pathlib.Path.glob`. Để mở rộng dấu ngã và biến shell, hãy sử dụng :func:`os.path.expanduser` và
:func:`os.path.expandvars`.

Để khớp theo nghĩa đen, hãy đặt các ký tự meta trong dấu ngoặc vuông. Ví dụ, ``'[?]'`` khớp với ký tự ``'?'``.

Mô-đun :mod:`!glob` định nghĩa các hàm sau:


.. function:: glob(pathname, *, root_dir=None, dir_fd=None, recursive=False, \
                   include_hidden=False)

   Trả về một danh sách có thể rỗng gồm các tên đường dẫn khớp với *pathname*, tham số này phải là một chuỗi chứa đặc tả đường dẫn. *pathname* có thể là đường dẫn tuyệt đối (như :file:`/usr/src/Python-1.5/Makefile`) hoặc tương đối (như
   :file:`../../Tools/\*/\*.gif`), và có thể chứa các ký tự đại diện theo kiểu shell. Các symbolic link bị hỏng cũng được đưa vào kết quả (như trong shell). Việc kết quả có được sắp xếp hay không phụ thuộc vào hệ thống tệp. Nếu một tệp thỏa mãn các điều kiện bị xóa hoặc được thêm vào trong khi hàm này đang được gọi, việc tên đường dẫn của tệp đó có được đưa vào hay không là không xác định.

   Nếu *root_dir* không phải là ``None``, thì đó phải là một :term:`path-like object` chỉ định thư mục gốc để tìm kiếm. Nó có tác dụng giống như
   :func:`!glob` khi thay đổi thư mục hiện tại trước khi gọi hàm. Nếu *pathname* là đường dẫn tương đối, kết quả sẽ chứa các đường dẫn tương đối so với *root_dir*.

   Hàm này có thể hỗ trợ :ref:`paths relative to directory descriptors <dir_fd>` với tham số *dir_fd*.

   .. index::
      single: **; in glob-style wildcards

   Nếu *recursive* là true, mẫu "``**``" sẽ khớp với mọi tệp và không hoặc nhiều thư mục, thư mục con cũng như liên kết tượng trưng đến thư mục. Nếu mẫu được theo sau bởi :data:`os.sep` hoặc :data:`os.altsep` thì các tệp sẽ không khớp.

   Nếu *include_hidden* là true, các ký tự đại diện có thể khớp với những thành phần đường dẫn bắt đầu bằng dấu chấm (``.``).

   .. audit-event:: glob.glob pathname,recursive glob.glob
   .. audit-event:: glob.glob/2 pathname,recursive,root_dir,dir_fd glob.glob

   .. note::
      Việc sử dụng mẫu "``**``" trong các cây thư mục lớn có thể mất một khoảng thời gian quá lớn.

   .. note::
      Hàm này có thể trả về các tên đường dẫn trùng lặp nếu *pathname* chứa nhiều mẫu "``**``" và *recursive* là true.

   .. note::
      Mọi ngoại lệ :exc:`OSError` phát sinh trong quá trình quét hệ thống tệp đều bị bỏ qua. Điều này bao gồm :exc:`PermissionError` khi truy cập các thư mục không có quyền đọc.

   .. versionchanged:: 3.5
      Hỗ trợ glob đệ quy bằng cách sử dụng "``**``".

   .. versionchanged:: 3.10
      Đã thêm các tham số *root_dir* và *dir_fd*.

   .. versionchanged:: 3.11
      Đã thêm tham số *include_hidden*.


.. function:: iglob(pathname, *, root_dir=None, dir_fd=None, recursive=False, \
                    include_hidden=False)

   Trả về một :term:`iterator` tạo ra các giá trị giống như :func:`glob` mà không thực sự lưu trữ tất cả chúng cùng lúc.

   .. audit-event:: glob.glob pathname,recursive glob.iglob
   .. audit-event:: glob.glob/2 pathname,recursive,root_dir,dir_fd glob.iglob

   .. note::
      Hàm này có thể trả về các tên đường dẫn trùng lặp nếu *pathname* chứa nhiều mẫu "``**``" và *recursive* là true.

   .. note::
      Mọi ngoại lệ :exc:`OSError` phát sinh trong quá trình quét hệ thống tệp đều bị bỏ qua. Điều này bao gồm :exc:`PermissionError` khi truy cập các thư mục không có quyền đọc.

   .. versionchanged:: 3.5
      Hỗ trợ glob đệ quy bằng cách sử dụng "``**``".

   .. versionchanged:: 3.10
      Đã thêm các tham số *root_dir* và *dir_fd*.

   .. versionchanged:: 3.11
      Đã thêm tham số *include_hidden*.


.. function:: escape(pathname)

   Escape tất cả các ký tự đặc biệt (``'?'``, ``'*'`` và ``'['``). Điều này hữu ích nếu bạn muốn khớp với một chuỗi literal tùy ý có thể chứa các ký tự đặc biệt. Các ký tự đặc biệt trong drive/sharepoint UNC không được Escape; ví dụ, trên Windows, ``escape('//?/c:/Quo vadis?.txt')`` trả về ``'//?/c:/Quo vadis[?].txt'``.

   .. versionadded:: 3.4


.. function:: translate(pathname, *, recursive=False, include_hidden=False, seps=None)

   Chuyển đổi đặc tả đường dẫn đã cho thành một regular expression để sử dụng với
   :func:`re.match`. Đặc tả đường dẫn có thể chứa các wildcard theo kiểu shell.

   Ví dụ:

      >>> import glob, re
      >>>
      >>> regex = glob.translate('**/*.txt', recursive=True, include_hidden=True)
      >>> regex
      '(?s:(?:.+/)?[^/]*\\.txt)\\z'
      >>> reobj = re.compile(regex)
      >>> reobj.match('foo/bar/baz.txt')
      <re.Match object; span=(0, 15), match='foo/bar/baz.txt'>

   Các dấu phân cách và phân đoạn đường dẫn có ý nghĩa đối với hàm này, không giống như
   :func:`fnmatch.translate`. Theo mặc định, wildcard không khớp với các dấu phân cách đường dẫn, và các phân đoạn mẫu ``*`` khớp chính xác với một phân đoạn đường dẫn.

   Nếu *recursive* là true, phân đoạn mẫu "``**``" sẽ khớp với bất kỳ số lượng phân đoạn đường dẫn nào.

   Nếu *include_hidden* là true, các ký tự đại diện có thể khớp với những phân đoạn đường dẫn bắt đầu bằng dấu chấm (``.``).

   Có thể cung cấp một chuỗi dấu phân cách đường dẫn cho đối số *seps*. Nếu không cung cấp, :data:`os.sep` và :data:`~os.altsep` (nếu có) sẽ được sử dụng.

   .. seealso::

     Các phương thức :meth:`pathlib.PurePath.full_match` và :meth:`pathlib.Path.glob`, gọi hàm này để triển khai việc khớp mẫu và globbing.

   .. versionadded:: 3.13


Ví dụ
-----

Xét một thư mục chứa các tệp sau:
:file:`1.gif`, :file:`2.txt`, :file:`card.gif` và một thư mục con :file:`sub` chỉ chứa tệp :file:`3.txt`. :func:`glob` sẽ tạo ra các kết quả sau. Lưu ý rằng mọi thành phần đứng đầu của đường dẫn đều được giữ nguyên.::

   >>> import glob
   >>> glob.glob('./[0-9].*')
   ['./1.gif', './2.txt']
   >>> glob.glob('*.gif')
   ['1.gif', 'card.gif']
   >>> glob.glob('?.gif')
   ['1.gif']
   >>> glob.glob('**/*.txt', recursive=True)
   ['2.txt', 'sub/3.txt']
   >>> glob.glob('./**/', recursive=True)
   ['./', './sub/']

Nếu thư mục chứa các tệp bắt đầu bằng ``.``, theo mặc định chúng sẽ không được khớp. Ví dụ, hãy xét một thư mục chứa :file:`card.gif` và
:file:`.card.gif`::

   >>> import glob
   >>> glob.glob('*.gif')
   ['card.gif']
   >>> glob.glob('.c*')
   ['.card.gif']

.. seealso::
   Mô-đun :mod:`fnmatch` cung cấp chức năng mở rộng tên tệp (không phải đường dẫn) theo kiểu shell.

.. seealso::
   Mô-đun :mod:`pathlib` cung cấp các đối tượng đường dẫn cấp cao.
