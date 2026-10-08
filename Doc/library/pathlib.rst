:mod:`!pathlib` --- Đường dẫn hệ thống tệp hướng đối tượng
==========================================================

.. module:: pathlib
   :synopsis: Đường dẫn hệ thống tệp hướng đối tượng

.. versionadded:: 3.4

**Mã nguồn:** :source:`Lib/pathlib/`

.. index:: single: path; operations

--------------

Mô-đun này cung cấp các lớp biểu diễn đường dẫn hệ thống tệp với ngữ nghĩa phù hợp cho từng hệ điều hành. Các lớp đường dẫn được chia thành :ref:`đường dẫn thuần <pure-paths>`, chỉ cung cấp các thao tác tính toán mà không thực hiện I/O, và :ref:`đường dẫn cụ thể <concrete-paths>`, kế thừa từ các đường dẫn thuần nhưng cũng cung cấp các thao tác I/O.

.. image:: pathlib-inheritance.png
   :align: center
   :class: invert-in-dark-mode
   :alt: Sơ đồ kế thừa cho thấy các lớp có trong pathlib. Lớp cơ bản nhất là PurePath, có ba lớp con trực tiếp: PurePosixPath, PureWindowsPath và Path. Ngoài bốn lớp này, có hai lớp sử dụng đa kế thừa: PosixPath kế thừa PurePosixPath và Path, còn WindowsPath kế thừa PureWindowsPath và Path.

Nếu bạn chưa từng sử dụng mô-đun này hoặc không chắc lớp nào phù hợp với tác vụ của mình, thì :class:`Path` rất có thể là thứ bạn cần. Nó khởi tạo một :ref:`đường dẫn cụ thể <concrete-paths>` cho nền tảng nơi mã đang chạy.

Đường dẫn thuần hữu ích trong một số trường hợp đặc biệt; ví dụ:

#. Nếu bạn muốn thao tác với các đường dẫn Windows trên máy Unix (hoặc ngược lại). Bạn không thể khởi tạo :class:`WindowsPath` khi chạy trên Unix, nhưng có thể khởi tạo :class:`PureWindowsPath`.
#. Bạn muốn đảm bảo rằng mã của mình chỉ thao tác với các đường dẫn mà không thực sự truy cập vào OS. Trong trường hợp này, việc khởi tạo một trong các lớp pure có thể hữu ích vì chúng đơn giản là không có bất kỳ thao tác nào truy cập OS.

.. seealso::
   :pep:`428`: The pathlib module -- object-oriented filesystem paths.

.. seealso::
   Để thao tác với đường dẫn cấp thấp trên các chuỗi, bạn cũng có thể sử dụng
   module :mod:`os.path`.


Cách sử dụng cơ bản
-------------------

Nhập lớp chính::

   >>> from pathlib import Path

Liệt kê các thư mục con::

   >>> p = Path('.')
   >>> [x for x in p.iterdir() if x.is_dir()]
   [PosixPath('.hg'), PosixPath('docs'), PosixPath('dist'),
    PosixPath('__pycache__'), PosixPath('build')]

Liệt kê các tệp mã nguồn Python trong cây thư mục này::

   >>> list(p.glob('**/*.py'))
   [PosixPath('test_pathlib.py'), PosixPath('setup.py'),
    PosixPath('pathlib.py'), PosixPath('docs/conf.py'),
    PosixPath('build/lib/pathlib.py')]

Điều hướng trong cây thư mục::

   >>> p = Path('/etc')
   >>> q = p / 'init.d' / 'reboot'
   >>> q
   PosixPath('/etc/init.d/reboot')
   >>> q.resolve()
   PosixPath('/etc/rc.d/init.d/halt')

Truy vấn các thuộc tính của đường dẫn::

   >>> q.exists()
   True
   >>> q.is_dir()
   False

Mở một tệp::

   >>> with q.open() as f: f.readline()
   ...
   '#!/bin/bash\n'


Ngoại lệ
--------

.. exception:: UnsupportedOperation

   Một ngoại lệ kế thừa :exc:`NotImplementedError` và được phát sinh khi một thao tác không được hỗ trợ được gọi trên đối tượng đường dẫn.

   .. versionadded:: 3.13


.. _pure-paths:

Đường dẫn thuần túy
-------------------

Các đối tượng đường dẫn thuần túy cung cấp các thao tác xử lý đường dẫn nhưng không thực sự truy cập hệ thống tệp. Có ba cách để truy cập các lớp này, còn được gọi là *biến thể*:

.. class:: PurePath(*pathsegments)

   Một lớp tổng quát đại diện cho biến thể đường dẫn của hệ thống (việc khởi tạo lớp này sẽ tạo ra một :class:`PurePosixPath` hoặc một :class:`PureWindowsPath`)::

      >>> PurePath('setup.py')      # Chạy trên máy Unix
      PurePosixPath('setup.py')

   Mỗi phần tử của *các phân đoạn đường dẫn* có thể là một chuỗi đại diện cho một phân đoạn đường dẫn hoặc một đối tượng triển khai giao diện :class:`os.PathLike`, trong đó phương thức :meth:`~os.PathLike.__fspath__` trả về một chuỗi, chẳng hạn như một đối tượng đường dẫn khác::

      >>> PurePath('foo', 'some/path', 'bar')
      PurePosixPath('foo/some/path/bar')
      >>> PurePath(Path('foo'), Path('bar'))
      PurePosixPath('foo/bar')

   Khi *các phân đoạn đường dẫn* trống hoặc chỉ gồm các chuỗi rỗng, thư mục hiện tại sẽ được sử dụng::

      >>> PurePath(), PurePath('')
      (PurePosixPath('.'), PurePosixPath('.'))

   Nếu một phân đoạn là đường dẫn tuyệt đối, mọi phân đoạn trước đó sẽ bị bỏ qua (giống như :func:`os.path.join`)::

      >>> PurePath('/etc', '/usr', 'lib64')
      PurePosixPath('/usr/lib64')
      >>> PureWindowsPath('c:/Windows', 'd:bar')
      PureWindowsPath('d:bar')

   Trên Windows, ổ đĩa không được đặt lại khi gặp một phân đoạn đường dẫn tương đối có gốc (ví dụ: ``r'\foo'``)::

      >>> PureWindowsPath('c:/Windows', '/Program Files')
      PureWindowsPath('c:/Program Files')

   Các dấu gạch chéo thừa và dấu chấm đơn được thu gọn, nhưng dấu chấm đôi (``'..'``) và dấu gạch chéo đôi ở đầu (``'//'``) thì không, vì việc này sẽ làm thay đổi ý nghĩa của đường dẫn vì nhiều lý do (ví dụ: symbolic link, đường dẫn UNC)::

      >>> PurePath('foo//bar')
      PurePosixPath('foo/bar')
      >>> PurePath('//foo/bar')
      PurePosixPath('//foo/bar')
      >>> PurePath('foo/./bar')
      PurePosixPath('foo/bar')
      >>> PurePath('foo/../bar')
      PurePosixPath('foo/../bar')

   (một cách tiếp cận ngây thơ sẽ khiến ``PurePosixPath('foo/../bar')`` tương đương với ``PurePosixPath('bar')``, điều này là sai nếu ``foo`` là một symbolic link trỏ đến thư mục khác)

   Các đối tượng pure path triển khai interface :class:`os.PathLike`, cho phép chúng được sử dụng ở bất kỳ nơi nào chấp nhận interface này.

   .. versionchanged:: 3.6
      Đã thêm hỗ trợ cho interface :class:`os.PathLike`.

.. class:: PurePosixPath(*pathsegments)

   Là một lớp con của :class:`PurePath`, biến thể đường dẫn này biểu diễn các đường dẫn hệ thống tệp không phải Windows::

      >>> PurePosixPath('/etc/hosts')
      PurePosixPath('/etc/hosts')

   *pathsegments* được chỉ định tương tự như :class:`PurePath`.

.. class:: PureWindowsPath(*pathsegments)

   Là một lớp con của :class:`PurePath`, biến thể đường dẫn này biểu diễn các đường dẫn hệ thống tệp Windows, bao gồm `UNC paths <UNC paths_>`_::

      >>> PureWindowsPath('c:/', 'Users', 'Ximénez')
      PureWindowsPath('c:/Users/Ximénez')
      >>> PureWindowsPath('//server/share/file')
      PureWindowsPath('//server/share/file')

   *pathsegments* được chỉ định tương tự như :class:`PurePath`.

   .. _unc paths: https://en.wikipedia.org/wiki/Path_(computing)#UNC

Bất kể bạn đang chạy trên hệ thống nào, bạn đều có thể khởi tạo tất cả các lớp này, vì chúng không cung cấp bất kỳ thao tác nào thực hiện các lệnh gọi hệ thống.


Các thuộc tính chung
^^^^^^^^^^^^^^^^^^^^

Các đường dẫn là bất biến và :term:`hashable`.  Các đường dẫn cùng loại có thể được so sánh và sắp xếp.  Những thuộc tính này tuân theo ngữ nghĩa chuyển đổi chữ hoa/chữ thường của loại đó::

   >>> PurePosixPath('foo') == PurePosixPath('FOO')
   False
   >>> PureWindowsPath('foo') == PureWindowsPath('FOO')
   True
   >>> PureWindowsPath('FOO') in { PureWindowsPath('foo') }
   True
   >>> PureWindowsPath('C:') < PureWindowsPath('d:')
   True

Các đường dẫn khác loại được xem là không bằng nhau và không thể sắp xếp::

   >>> PureWindowsPath('foo') == PurePosixPath('foo')
   False
   >>> PureWindowsPath('foo') < PurePosixPath('foo')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: '<' not supported between instances of 'PureWindowsPath' and 'PurePosixPath'


Toán tử
^^^^^^^

Toán tử dấu gạch chéo giúp tạo các đường dẫn con, chẳng hạn như :func:`os.path.join`. Nếu đối số là một đường dẫn tuyệt đối, đường dẫn trước đó sẽ bị bỏ qua. Trên Windows, ổ đĩa không được đặt lại khi đối số là một đường dẫn tương đối bắt đầu từ thư mục gốc (ví dụ: ``r'\foo'``)::

   >>> p = PurePath('/etc')
   >>> p
   PurePosixPath('/etc')
   >>> p / 'init.d' / 'apache2'
   PurePosixPath('/etc/init.d/apache2')
   >>> q = PurePath('bin')
   >>> '/usr' / q
   PurePosixPath('/usr/bin')
   >>> p / '/an_absolute_path'
   PurePosixPath('/an_absolute_path')
   >>> PureWindowsPath('c:/Windows', '/Program Files')
   PureWindowsPath('c:/Program Files')

Một đối tượng path có thể được sử dụng ở bất kỳ đâu chấp nhận một đối tượng triển khai :class:`os.PathLike`::

   >>> import os
   >>> p = PurePath('/etc')
   >>> os.fspath(p)
   '/etc'

Biểu diễn chuỗi của một path chính là đường dẫn hệ thống tệp thô (ở dạng gốc, chẳng hạn dùng dấu gạch chéo ngược trên Windows), và bạn có thể truyền nó cho bất kỳ hàm nào nhận đường dẫn tệp dưới dạng chuỗi::

   >>> p = PurePath('/etc')
   >>> str(p)
   '/etc'
   >>> p = PureWindowsPath('c:/Program Files')
   >>> str(p)
   'c:\\Program Files'

Tương tự, việc gọi :class:`bytes` trên một path sẽ trả về đường dẫn hệ thống tệp thô dưới dạng đối tượng bytes, được mã hóa bởi :func:`os.fsencode`::

   >>> bytes(p)
   b'/etc'

.. note::
   Chỉ nên gọi :class:`bytes` trên Unix. Trên Windows, dạng Unicode là biểu diễn chuẩn của các đường dẫn hệ thống tệp.


Truy cập các phần riêng lẻ
^^^^^^^^^^^^^^^^^^^^^^^^^^

Để truy cập các "phần" (thành phần) riêng lẻ của một path, hãy sử dụng thuộc tính sau:

.. attribute:: PurePath.parts

   Một tuple cho phép truy cập các thành phần khác nhau của path::

      >>> p = PurePath('/usr/bin/python3')
      >>> p.parts
      ('/', 'usr', 'bin', 'python3')

      >>> p = PureWindowsPath('c:/Program Files/PSF')
      >>> p.parts
      ('c:\\', 'Program Files', 'PSF')

   (lưu ý cách ổ đĩa và thư mục gốc cục bộ được nhóm lại trong một phần duy nhất)


Phương thức và thuộc tính
^^^^^^^^^^^^^^^^^^^^^^^^^

.. testsetup::

   from pathlib import PurePath, PurePosixPath, PureWindowsPath

Đường dẫn thuần cung cấp các phương thức và thuộc tính sau:

.. attribute:: PurePath.parser

   Việc triển khai module :mod:`os.path` được dùng để phân tích cú pháp và nối đường dẫn ở cấp thấp: :mod:`!posixpath` hoặc :mod:`!ntpath`.

   .. versionadded:: 3.13

.. attribute:: PurePath.drive

   Một chuỗi biểu thị ký tự hoặc tên ổ đĩa, nếu có::

      >>> PureWindowsPath('c:/Program Files/').drive
      'c:'
      >>> PureWindowsPath('/Program Files/').drive
      ''
      >>> PurePosixPath('/etc').drive
      ''

   Các thư mục chia sẻ UNC cũng được xem là ổ đĩa::

      >>> PureWindowsPath('//host/share/foo.txt').drive
      '\\\\host\\share'

.. attribute:: PurePath.root

   Một chuỗi biểu thị thư mục gốc (cục bộ hoặc toàn cục), nếu có::

      >>> PureWindowsPath('c:/Program Files/').root
      '\\'
      >>> PureWindowsPath('c:Program Files/').root
      ''
      >>> PurePosixPath('/etc').root
      '/'

   Các UNC share luôn có root::

      >>> PureWindowsPath('//host/share').root
      '\\'

   Nếu đường dẫn bắt đầu bằng nhiều hơn hai dấu gạch chéo liên tiếp,
   :class:`~pathlib.PurePosixPath` gộp chúng lại::

      >>> PurePosixPath('//etc').root
      '//'
      >>> PurePosixPath('///etc').root
      '/'
      >>> PurePosixPath('////etc').root
      '/'

   .. note::

      Hành vi này phù hợp với *The Open Group Base Specifications Issue 6*, đoạn `4.11 Pathname Resolution <https://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap04.html#tag_04_11>`_:

      *"Một pathname bắt đầu bằng hai dấu gạch chéo liên tiếp có thể được diễn giải theo cách do implementation xác định, mặc dù nhiều hơn hai dấu gạch chéo ở đầu phải được xử lý như một dấu gạch chéo duy nhất."*

.. attribute:: PurePath.anchor

   Phép nối của drive và root::

      >>> PureWindowsPath('c:/Program Files/').anchor
      'c:\\'
      >>> PureWindowsPath('c:Program Files/').anchor
      'c:'
      >>> PurePosixPath('/etc').anchor
      '/'
      >>> PureWindowsPath('//host/share').anchor
      '\\\\host\\share\\'


.. attribute:: PurePath.parents

   Một chuỗi bất biến cung cấp quyền truy cập vào các ancestor logic của đường dẫn::

      >>> p = PureWindowsPath('c:/foo/bar/setup.py')
      >>> p.parents[0]
      PureWindowsPath('c:/foo/bar')
      >>> p.parents[1]
      PureWindowsPath('c:/foo')
      >>> p.parents[2]
      PureWindowsPath('c:/')

   .. versionchanged:: 3.10
      Chuỗi parents hiện hỗ trợ :term:`các lát cắt <slice>` và các giá trị chỉ mục âm.

.. attribute:: PurePath.parent

   Parent logic của đường dẫn::

      >>> p = PurePosixPath('/a/b/c/d')
      >>> p.parent
      PurePosixPath('/a/b/c')

   Bạn không thể đi qua một anchor hoặc đường dẫn rỗng::

      >>> p = PurePosixPath('/')
      >>> p.parent
      PurePosixPath('/')
      >>> p = PurePosixPath('.')
      >>> p.parent
      PurePosixPath('.')

   .. note::
      Đây hoàn toàn là một thao tác từ vựng, do đó có hành vi sau::

         >>> p = PurePosixPath('foo/..')
         >>> p.parent
         PurePosixPath('foo')

      Nếu muốn duyệt ngược lên trên một đường dẫn hệ thống tệp bất kỳ, bạn nên gọi :meth:`Path.resolve` trước để phân giải các symlink và loại bỏ các thành phần ``".."``.


.. attribute:: PurePath.name

   Một chuỗi biểu diễn thành phần cuối cùng của đường dẫn, không bao gồm ổ đĩa và thư mục gốc, nếu có::

      >>> PurePosixPath('my/library/setup.py').name
      'setup.py'

   Tên ổ đĩa UNC không được xét đến::

      >>> PureWindowsPath('//some/share/setup.py').name
      'setup.py'
      >>> PureWindowsPath('//some/share').name
      ''


.. attribute:: PurePath.suffix

   Phần cuối cùng được phân tách bằng dấu chấm của thành phần cuối, nếu có::

      >>> PurePosixPath('my/library/setup.py').suffix
      '.py'
      >>> PurePosixPath('my/library.tar.gz').suffix
      '.gz'
      >>> PurePosixPath('my/library').suffix
      ''

   Phần này thường được gọi là phần mở rộng tệp.

   .. versionchanged:: 3.14

      Một dấu chấm đơn ("``.``") được xem là một hậu tố hợp lệ.

.. attribute:: PurePath.suffixes

   Danh sách các hậu tố của đường dẫn, thường được gọi là phần mở rộng tệp::

      >>> PurePosixPath('my/library.tar.gar').suffixes
      ['.tar', '.gar']
      >>> PurePosixPath('my/library.tar.gz').suffixes
      ['.tar', '.gz']
      >>> PurePosixPath('my/library').suffixes
      []

   .. versionchanged:: 3.14

      Một dấu chấm đơn ("``.``") được xem là một hậu tố hợp lệ.


.. attribute:: PurePath.stem

   Thành phần cuối cùng của đường dẫn, không có hậu tố::

      >>> PurePosixPath('my/library.tar.gz').stem
      'library.tar'
      >>> PurePosixPath('my/library.tar').stem
      'library'
      >>> PurePosixPath('my/library').stem
      'library'

   .. versionchanged:: 3.14

      Một dấu chấm đơn ("``.``") được xem là một hậu tố hợp lệ.


.. method:: PurePath.as_posix()

   Trả về biểu diễn chuỗi của đường dẫn với dấu gạch chéo xuôi (``/``)::

      >>> p = PureWindowsPath('c:\\windows')
      >>> str(p)
      'c:\\windows'
      >>> p.as_posix()
      'c:/windows'


.. method:: PurePath.is_absolute()

   Cho biết đường dẫn có phải là đường dẫn tuyệt đối hay không. Một đường dẫn được xem là tuyệt đối nếu có cả root và (nếu kiểu đường dẫn cho phép) drive::

      >>> PurePosixPath('/a/b').is_absolute()
      True
      >>> PurePosixPath('a/b').is_absolute()
      False

      >>> PureWindowsPath('c:/a/b').is_absolute()
      True
      >>> PureWindowsPath('/a/b').is_absolute()
      False
      >>> PureWindowsPath('c:').is_absolute()
      False
      >>> PureWindowsPath('//some/share').is_absolute()
      True


.. method:: PurePath.is_relative_to(other)

   Cho biết đường dẫn này có tương đối với đường dẫn *other* hay không.

      >>> p = PurePath('/etc/passwd')
      >>> p.is_relative_to('/etc')
      True
      >>> p.is_relative_to('/usr')
      False

   Phương thức này dựa trên chuỗi; nó không truy cập hệ thống tệp và cũng không xử lý đặc biệt các phân đoạn "``..``". Đoạn mã sau tương đương:

      >>> u = PurePath('/usr')
      >>> u == p or u in p.parents
      False

   .. versionadded:: 3.9

   .. deprecated-removed:: 3.12 3.14

      Việc truyền thêm đối số đã không còn được khuyến nghị; nếu được cung cấp, chúng sẽ được nối với *other*.

.. method:: PurePath.is_reserved()

   Với :class:`PureWindowsPath`, trả về ``True`` nếu đường dẫn được xem là reserved trong Windows, và ``False`` nếu không. Với :class:`PurePosixPath`, luôn trả về ``False``.

   .. versionchanged:: 3.13
      Tên đường dẫn Windows có chứa dấu hai chấm hoặc kết thúc bằng dấu chấm hay khoảng trắng được xem là reserved. Các đường dẫn UNC có thể là reserved.

   .. deprecated-removed:: 3.13 3.15
      Phương thức này đã bị deprecated; hãy sử dụng :func:`os.path.isreserved` để phát hiện các đường dẫn dành riêng trên Windows.

.. method:: PurePath.joinpath(*pathsegments)

   Việc gọi phương thức này tương đương với việc lần lượt kết hợp đường dẫn với từng *pathsegments* đã cho::

      >>> PurePosixPath('/etc').joinpath('passwd')
      PurePosixPath('/etc/passwd')
      >>> PurePosixPath('/etc').joinpath(PurePosixPath('passwd'))
      PurePosixPath('/etc/passwd')
      >>> PurePosixPath('/etc').joinpath('init.d', 'apache2')
      PurePosixPath('/etc/init.d/apache2')
      >>> PureWindowsPath('c:').joinpath('/Program Files')
      PureWindowsPath('c:/Program Files')


.. method:: PurePath.full_match(pattern, *, case_sensitive=None)

   Đối sánh đường dẫn này với mẫu kiểu glob được cung cấp. Trả về ``True`` nếu đối sánh thành công, nếu không thì trả về ``False``. Ví dụ::

      >>> PurePath('a/b.py').full_match('a/*.py')
      True
      >>> PurePath('a/b.py').full_match('*.py')
      False
      >>> PurePath('/a/b/c.py').full_match('/a/**')
      True
      >>> PurePath('/a/b/c.py').full_match('**/*.py')
      True

   .. seealso::
      :ref:`pathlib-pattern-language` documentation.

   Giống như các phương thức khác, việc phân biệt chữ hoa chữ thường tuân theo mặc định của nền tảng::

      >>> PurePosixPath('b.py').full_match('*.PY')
      False
      >>> PureWindowsPath('b.py').full_match('*.PY')
      True

   Đặt *case_sensitive* thành ``True`` hoặc ``False`` để ghi đè hành vi này.

   .. versionadded:: 3.13


.. method:: PurePath.match(pattern, *, case_sensitive=None)

   Đối sánh đường dẫn này với mẫu kiểu glob không đệ quy được cung cấp. Trả về ``True`` nếu đối sánh thành công, nếu không thì trả về ``False``.

   Phương thức này tương tự như :meth:`~PurePath.full_match`, nhưng không cho phép mẫu trống (sẽ phát sinh :exc:`ValueError`), không hỗ trợ wildcard đệ quy "``**``" (hoạt động như "``*``" không đệ quy), và nếu cung cấp một mẫu tương đối thì việc đối sánh sẽ được thực hiện từ bên phải::

      >>> PurePath('a/b.py').match('*.py')
      True
      >>> PurePath('/a/b/c.py').match('b/*.py')
      True
      >>> PurePath('/a/b/c.py').match('a/*.py')
      False

   .. versionchanged:: 3.12
      Tham số *pattern* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.12
      Tham số *case_sensitive* đã được thêm.


.. method:: PurePath.relative_to(other, walk_up=False)

   Tính toán phiên bản của đường dẫn này tương đối so với đường dẫn được biểu diễn bởi *other*. Nếu không thể thực hiện, :exc:`ValueError` sẽ được phát sinh::

      >>> p = PurePosixPath('/etc/passwd')
      >>> p.relative_to('/')
      PurePosixPath('etc/passwd')
      >>> p.relative_to('/etc')
      PurePosixPath('passwd')
      >>> p.relative_to('/usr')
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "pathlib.py", line 941, in relative_to
          raise ValueError(error_message.format(str(self), str(formatted)))
      ValueError: '/etc/passwd' is not in the subpath of '/usr' OR one path is relative and the other is absolute.

   Khi *walk_up* là false (giá trị mặc định), đường dẫn phải bắt đầu bằng *other*. Khi đối số là true, có thể thêm các mục ``..`` để tạo thành đường dẫn tương đối. Trong mọi trường hợp khác, chẳng hạn như khi các đường dẫn tham chiếu đến những ổ đĩa khác nhau, :exc:`ValueError` sẽ được phát sinh.::

      >>> p.relative_to('/usr', walk_up=True)
      PurePosixPath('../etc/passwd')
      >>> p.relative_to('foo', walk_up=True)
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "pathlib.py", line 941, in relative_to
          raise ValueError(error_message.format(str(self), str(formatted)))
      ValueError: '/etc/passwd' is not on the same drive as 'foo' OR one path is relative and the other is absolute.

   .. warning::
      Hàm này thuộc :class:`PurePath` và hoạt động với các chuỗi. Hàm không kiểm tra hoặc truy cập cấu trúc tệp bên dưới. Điều này có thể ảnh hưởng đến tùy chọn *walk_up* vì tùy chọn này giả định rằng không có symlink nào trong đường dẫn; nếu cần, trước tiên hãy gọi :meth:`~Path.resolve` để phân giải symlink.

   .. versionchanged:: 3.12
      Tham số *walk_up* đã được thêm (hành vi cũ giống với ``walk_up=False``).

   .. deprecated-removed:: 3.12 3.14

      Việc truyền thêm các đối số positional đã lỗi thời; nếu được cung cấp, chúng sẽ được nối với *other*.

.. method:: PurePath.with_name(name)

   Trả về một path mới với :attr:`name` được thay đổi. Nếu path ban đầu không có tên, ValueError sẽ được phát sinh::

      >>> p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
      >>> p.with_name('setup.py')
      PureWindowsPath('c:/Downloads/setup.py')
      >>> p = PureWindowsPath('c:/')
      >>> p.with_name('setup.py')
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/home/antoine/cpython/default/Lib/pathlib.py", line 751, in with_name
          raise ValueError("%r has an empty name" % (self,))
      ValueError: PureWindowsPath('c:/') has an empty name


.. method:: PurePath.with_stem(stem)

   Trả về một path mới với :attr:`stem` được thay đổi. Nếu path ban đầu không có tên, ValueError sẽ được phát sinh::

      >>> p = PureWindowsPath('c:/Downloads/draft.txt')
      >>> p.with_stem('final')
      PureWindowsPath('c:/Downloads/final.txt')
      >>> p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
      >>> p.with_stem('lib')
      PureWindowsPath('c:/Downloads/lib.gz')
      >>> p = PureWindowsPath('c:/')
      >>> p.with_stem('')
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/home/antoine/cpython/default/Lib/pathlib.py", line 861, in with_stem
          return self.with_name(stem + self.suffix)
        File "/home/antoine/cpython/default/Lib/pathlib.py", line 851, in with_name
          raise ValueError("%r has an empty name" % (self,))
      ValueError: PureWindowsPath('c:/') has an empty name

   .. versionadded:: 3.9


.. method:: PurePath.with_suffix(suffix)

   Trả về một path mới với :attr:`suffix` được thay đổi. Nếu path ban đầu không có hậu tố, *suffix* mới sẽ được nối thêm. Nếu *suffix* là một chuỗi rỗng, hậu tố ban đầu sẽ bị xóa::

      >>> p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
      >>> p.with_suffix('.bz2')
      PureWindowsPath('c:/Downloads/pathlib.tar.bz2')
      >>> p = PureWindowsPath('README')
      >>> p.with_suffix('.txt')
      PureWindowsPath('README.txt')
      >>> p = PureWindowsPath('README.txt')
      >>> p.with_suffix('')
      PureWindowsPath('README')

   .. versionchanged:: 3.14

      Một dấu chấm đơn ("``.``") được xem là hậu tố hợp lệ. Trong các phiên bản trước, :exc:`ValueError` sẽ được phát sinh nếu cung cấp một dấu chấm đơn.


.. method:: PurePath.with_segments(*pathsegments)

   Tạo một đối tượng path mới cùng kiểu bằng cách kết hợp các *pathsegments* đã cho. Phương thức này được gọi mỗi khi một path dẫn xuất được tạo, chẳng hạn từ :attr:`parent` và :meth:`relative_to`. Các lớp con có thể ghi đè phương thức này để truyền thông tin đến các path dẫn xuất, ví dụ::

      from pathlib import PurePosixPath

      class MyPath(PurePosixPath):
          def __init__(self, *pathsegments, session_id):
              super().__init__(*pathsegments)
              self.session_id = session_id

          def with_segments(self, *pathsegments):
              return type(self)(*pathsegments, session_id=self.session_id)

      etc = MyPath('/etc', session_id=42)
      hosts = etc / 'hosts'
      print(hosts.session_id)  # 42

   .. versionadded:: 3.12


.. _concrete-paths:


Các path cụ thể
---------------

Các path cụ thể là các lớp con của những lớp pure path. Ngoài các thao tác do các lớp sau cung cấp, chúng còn cung cấp các phương thức để thực hiện system call trên các đối tượng path. Có ba cách để khởi tạo các path cụ thể:

.. class:: Path(*pathsegments)

   Là lớp con của :class:`PurePath`, lớp này biểu diễn các đường dẫn cụ thể theo kiểu đường dẫn của hệ thống (khi khởi tạo, nó sẽ tạo ra một
   :class:`PosixPath` hoặc một :class:`WindowsPath`)“},{::

      >>> Path('setup.py')
      PosixPath('setup.py')

   *pathsegments* được chỉ định tương tự như :class:`PurePath`.

.. class:: PosixPath(*pathsegments)

   Là lớp con của :class:`Path` và :class:`PurePosixPath`, lớp này biểu diễn các đường dẫn hệ thống tệp cụ thể không phải Windows::

      >>> PosixPath('/etc/hosts')
      PosixPath('/etc/hosts')

   *pathsegments* được chỉ định tương tự như :class:`PurePath`.

   .. versionchanged:: 3.13
      Trên Windows, sẽ raise :exc:`UnsupportedOperation`. Trong các phiên bản trước đây,
      thay vào đó, :exc:`NotImplementedError` được raise.


.. class:: WindowsPath(*pathsegments)

   Là lớp con của :class:`Path` và :class:`PureWindowsPath`, lớp này biểu diễn các đường dẫn hệ thống tệp Windows cụ thể::

      >>> WindowsPath('c:/', 'Users', 'Ximénez')
      WindowsPath('c:/Users/Ximénez')

   *pathsegments* được chỉ định tương tự như :class:`PurePath`.

   .. versionchanged:: 3.13
      Gây ra :exc:`UnsupportedOperation` trên các nền tảng không phải Windows. Trong các phiên bản trước, thay vào đó :exc:`NotImplementedError` được gây ra.


Bạn chỉ có thể khởi tạo loại lớp tương ứng với hệ thống của mình (việc cho phép gọi hệ thống trên các loại đường dẫn không tương thích có thể dẫn đến lỗi hoặc sự cố trong ứng dụng của bạn)::

   >>> import os
   >>> os.name
   'posix'
   >>> Path('setup.py')
   PosixPath('setup.py')
   >>> PosixPath('setup.py')
   PosixPath('setup.py')
   >>> WindowsPath('setup.py')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "pathlib.py", line 798, in __new__
       % (cls.__name__,))
   UnsupportedOperation: cannot instantiate 'WindowsPath' on your system

Một số phương thức đường dẫn cụ thể có thể gây ra :exc:`OSError` nếu lệnh gọi hệ thống không thành công (chẳng hạn vì đường dẫn không tồn tại).


Phân tích cú pháp và tạo URI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các đối tượng đường dẫn cụ thể có thể được tạo từ và biểu diễn dưới dạng URI 'file' tuân thủ :rfc:`8089`.

.. note::

   File URI không thể di chuyển giữa các máy có các
   :ref:`bộ mã hóa hệ thống tệp khác nhau <filesystem-encoding>`.

.. classmethod:: Path.from_uri(uri)

   Trả về một đối tượng đường dẫn mới bằng cách phân tích cú pháp một URI 'file'. Ví dụ::

      >>> p = Path.from_uri('file:///etc/hosts')
      PosixPath('/etc/hosts')

   Trên Windows, các đường dẫn thiết bị DOS và UNC có thể được phân tích cú pháp từ URI::

      >>> p = Path.from_uri('file:///c:/windows')
      WindowsPath('c:/windows')
      >>> p = Path.from_uri('file://server/share')
      WindowsPath('//server/share')

   Một số dạng biến thể được hỗ trợ::

      >>> p = Path.from_uri('file:////server/share')
      WindowsPath('//server/share')
      >>> p = Path.from_uri('file://///server/share')
      WindowsPath('//server/share')
      >>> p = Path.from_uri('file:c:/windows')
      WindowsPath('c:/windows')
      >>> p = Path.from_uri('file:/c|/windows')
      WindowsPath('c:/windows')

   :exc:`ValueError` được phát sinh nếu URI không bắt đầu bằng ``file:``, hoặc đường dẫn đã phân tích cú pháp không phải là đường dẫn tuyệt đối.

   .. versionadded:: 3.13

   .. versionchanged:: 3.14
      Authority của URL sẽ bị loại bỏ nếu khớp với hostname cục bộ. Nếu không, khi authority không rỗng hoặc không phải là ``localhost``, thì trên Windows, một đường dẫn UNC sẽ được trả về (như trước đây), còn trên các nền tảng khác, một
      :exc:`ValueError` được phát sinh.


.. method:: Path.as_uri()

   Biểu diễn đường dẫn dưới dạng URI 'file'. :exc:`ValueError` được phát sinh nếu đường dẫn không phải là đường dẫn tuyệt đối.

   .. code-block:: pycon

      >>> p = PosixPath('/etc/passwd')
      >>> p.as_uri()
      'file:///etc/passwd'
      >>> p = WindowsPath('c:/Windows')
      >>> p.as_uri()
      'file:///c:/Windows'

   .. deprecated-removed:: 3.14 3.19

      Có thể gọi phương thức này từ :class:`PurePath` thay vì :class:`Path`, nhưng cách này đã lỗi thời. Việc phương thức sử dụng :func:`os.fsencode` khiến nó hoàn toàn không thuần túy.


Mở rộng và phân giải đường dẫn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. classmethod:: Path.home()

   Trả về một đối tượng đường dẫn mới biểu diễn thư mục chính của người dùng (như được trả về bởi :func:`os.path.expanduser` với cấu trúc ``~``). Nếu không thể phân giải thư mục chính, :exc:`RuntimeError` được phát sinh.

   ::

      >>> Path.home()
      PosixPath('/home/antoine')

   .. versionadded:: 3.5


.. method:: Path.expanduser()

   Trả về một đường dẫn mới với các cấu trúc ``~`` và ``~user`` được mở rộng, như được trả về bởi :meth:`os.path.expanduser`. Nếu không thể phân giải thư mục chính, :exc:`RuntimeError` được phát sinh.

   ::

      >>> p = PosixPath('~/films/Monty Python')
      >>> p.expanduser()
      PosixPath('/home/eric/films/Monty Python')

   .. versionadded:: 3.5


.. classmethod:: Path.cwd()

   Trả về một đối tượng đường dẫn mới biểu diễn thư mục hiện tại (như được trả về bởi :func:`os.getcwd`)::

      >>> Path.cwd()
      PosixPath('/home/antoine/pathlib')


.. method:: Path.absolute()

   Chuyển đường dẫn thành đường dẫn tuyệt đối, không chuẩn hóa hoặc phân giải các liên kết tượng trưng. Trả về một đối tượng đường dẫn mới::

      >>> p = Path('tests')
      >>> p
      PosixPath('tests')
      >>> p.absolute()
      PosixPath('/home/antoine/pathlib/tests')


.. method:: Path.resolve(strict=False)

   Chuyển đường dẫn thành đường dẫn tuyệt đối, phân giải mọi liên kết tượng trưng. Trả về một đối tượng đường dẫn mới::

      >>> p = Path()
      >>> p
      PosixPath('.')
      >>> p.resolve()
      PosixPath('/home/antoine/pathlib')

   Các thành phần "``..``" cũng được loại bỏ (đây là phương thức duy nhất để thực hiện việc này)::

      >>> p = Path('docs/../setup.py')
      >>> p.resolve()
      PosixPath('/home/antoine/pathlib/setup.py')

   Nếu một đường dẫn không tồn tại hoặc gặp vòng lặp liên kết tượng trưng, và *strict* là ``True``, :exc:`OSError` sẽ được phát sinh. Nếu *strict* là ``False``, đường dẫn sẽ được phân giải đến mức có thể và mọi phần còn lại sẽ được nối thêm mà không kiểm tra xem chúng có tồn tại hay không.

   .. versionchanged:: 3.6
      Tham số *strict* đã được thêm vào (hành vi trước phiên bản 3.6 là strict).

   .. versionchanged:: 3.13
      Vòng lặp liên kết tượng trưng được xử lý như các lỗi khác: :exc:`OSError` được phát sinh ở chế độ strict và không có ngoại lệ nào được phát sinh ở chế độ non-strict. Trong các phiên bản trước, :exc:`RuntimeError` được phát sinh bất kể giá trị của *strict*.


.. method:: Path.readlink()

   Trả về đường dẫn mà liên kết tượng trưng trỏ tới (như được trả về bởi
   :func:`os.readlink`)::

      >>> p = Path('mylink')
      >>> p.symlink_to('setup.py')
      >>> p.readlink()
      PosixPath('setup.py')

   .. versionadded:: 3.9

   .. versionchanged:: 3.13
      Nêu ra :exc:`UnsupportedOperation` nếu :func:`os.readlink` không khả dụng. Trong các phiên bản trước, :exc:`NotImplementedError` được nêu ra.


Truy vấn loại và trạng thái tệp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionchanged:: 3.8

   :meth:`~Path.exists`, :meth:`~Path.is_dir`, :meth:`~Path.is_file`,
   :meth:`~Path.is_mount`, :meth:`~Path.is_symlink`,
   :meth:`~Path.is_block_device`, :meth:`~Path.is_char_device`,
   :meth:`~Path.is_fifo`, :meth:`~Path.is_socket` hiện trả về ``False`` thay vì nêu ra một exception đối với các đường dẫn chứa những ký tự không thể biểu diễn ở cấp hệ điều hành.

.. versionchanged:: 3.14

   Các phương thức nêu trên hiện trả về ``False`` thay vì nêu ra bất kỳ
   exception :exc:`OSError` nào từ hệ điều hành. Trong các phiên bản trước, một số loại exception :exc:`OSError` được nêu ra, còn những loại khác bị bỏ qua. Hành vi mới nhất quán với :func:`os.path.exists`,
   :func:`os.path.isdir`, v.v. Sử dụng :meth:`~Path.stat` để lấy trạng thái tệp mà không bỏ qua các exception.


.. method:: Path.stat(*, follow_symlinks=True)

   Trả về một đối tượng :class:`os.stat_result` chứa thông tin về đường dẫn này, chẳng hạn như :func:`os.stat`. Kết quả được tra cứu ở mỗi lần gọi phương thức này.

   Phương thức này thường đi theo các symlink; để lấy thông tin của một symlink, hãy thêm đối số ``follow_symlinks=False``, hoặc sử dụng :meth:`~Path.lstat`.

   ::

      >>> p = Path('setup.py')
      >>> p.stat().st_size
      956
      >>> p.stat().st_mtime
      1327883547.852554

   .. versionchanged:: 3.10
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.lstat()

   Tương tự :meth:`Path.stat`, nhưng nếu đường dẫn trỏ đến một symbolic link, trả về thông tin của symbolic link đó thay vì thông tin của đích mà nó trỏ tới.


.. method:: Path.exists(*, follow_symlinks=True)

   Trả về ``True`` nếu đường dẫn trỏ đến một tệp hoặc thư mục hiện có và ``False`` nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại. Sử dụng :meth:`Path.stat` để phân biệt các trường hợp này.

   Phương thức này thường đi theo các symlink; để kiểm tra xem một symlink có tồn tại hay không, hãy thêm đối số ``follow_symlinks=False``.

   ::

      >>> Path('').exists()  # Thư mục hiện tại.
      True
      >>> Path('.').exists()
      True
      >>> Path('setup.py').exists()
      True
      >>> Path('/etc').exists()
      True
      >>> Path('nonexistentfile').exists()
      False

   .. versionchanged:: 3.12
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.is_file(*, follow_symlinks=True)

   Trả về ``True`` nếu đường dẫn trỏ đến một tệp thông thường. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ đến một đối tượng không phải là tệp thông thường. Sử dụng :meth:`Path.stat` để phân biệt các trường hợp này.

   Theo mặc định, phương thức này tuân theo các symlink; để loại trừ symlink, hãy thêm đối số ``follow_symlinks=False``.

   .. versionchanged:: 3.13
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.is_dir(*, follow_symlinks=True)

   Trả về ``True`` nếu đường dẫn trỏ đến một thư mục. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ đến một đối tượng không phải là thư mục. Sử dụng :meth:`Path.stat` để phân biệt các trường hợp này.

   Theo mặc định, phương thức này tuân theo các symlink; để loại trừ symlink đến các thư mục, hãy thêm đối số ``follow_symlinks=False``.

   .. versionchanged:: 3.13
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.is_symlink()

   Trả về ``True`` nếu đường dẫn trỏ đến một symbolic link, ngay cả khi symbolic link đó bị hỏng. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ đến một đối tượng không phải là symbolic link. Sử dụng
   :meth:`Path.stat` để phân biệt giữa các trường hợp này.


.. method:: Path.is_junction()

   Trả về ``True`` nếu đường dẫn trỏ đến một junction và ``False`` đối với mọi loại tệp khác. Hiện tại, chỉ Windows hỗ trợ junction.

   .. versionadded:: 3.12


.. method:: Path.is_mount()

   Trả về ``True`` nếu đường dẫn là một :dfn:`mount point`: một vị trí trong hệ thống tệp nơi một hệ thống tệp khác được gắn vào. Trên POSIX, hàm kiểm tra xem thư mục cha của *path*, là :file:`path/..`, có nằm trên một thiết bị khác với *path* hay không, hoặc xem :file:`path/..` và *path* có trỏ đến cùng một i-node trên cùng một thiết bị hay không --- cách này sẽ phát hiện mount point cho mọi biến thể Unix và POSIX. Trên Windows, mount point được xem là thư mục gốc của ký tự ổ đĩa (ví dụ ``c:\``), một UNC share (ví dụ ``\\server\share``) hoặc một thư mục hệ thống tệp đã được gắn vào.

   .. versionadded:: 3.7

   .. versionchanged:: 3.12
      Đã bổ sung hỗ trợ Windows.

.. method:: Path.is_socket()

   Trả về ``True`` nếu đường dẫn trỏ đến một Unix socket. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ đến một đối tượng không phải Unix socket. Sử dụng :meth:`Path.stat` để phân biệt giữa các trường hợp này.


.. method:: Path.is_fifo()

   Trả về ``True`` nếu đường dẫn trỏ đến một FIFO. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ đến một đối tượng không phải FIFO. Sử dụng :meth:`Path.stat` để phân biệt giữa các trường hợp này.


.. method:: Path.is_block_device()

   Trả về ``True`` nếu đường dẫn trỏ đến một block device. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ đến một đối tượng không phải block device. Sử dụng :meth:`Path.stat` để phân biệt giữa các trường hợp này.


.. method:: Path.is_char_device()

   Trả về ``True`` nếu đường dẫn trỏ tới một thiết bị ký tự. ``False`` sẽ được trả về nếu đường dẫn không hợp lệ, không thể truy cập hoặc không tồn tại, hoặc nếu đường dẫn trỏ tới đối tượng không phải là thiết bị ký tự. Sử dụng :meth:`Path.stat` để phân biệt các trường hợp này.


.. method:: Path.samefile(other_path)

   Trả về liệu đường dẫn này có trỏ tới cùng một tệp với *other_path* hay không; đối tượng này có thể là một đối tượng Path hoặc một chuỗi. Ngữ nghĩa tương tự như :func:`os.path.samefile` và :func:`os.path.samestat`.

   Có thể phát sinh một :exc:`OSError` nếu vì lý do nào đó không thể truy cập một trong hai tệp.

   ::

      >>> p = Path('spam')
      >>> q = Path('eggs')
      >>> p.samefile(q)
      False
      >>> p.samefile('spam')
      True

   .. versionadded:: 3.5


.. attribute:: Path.info

   Một đối tượng :class:`~pathlib.types.PathInfo` hỗ trợ truy vấn thông tin về loại tệp. Đối tượng này cung cấp các phương thức lưu kết quả vào bộ nhớ đệm, giúp giảm số lần gọi hệ thống cần thiết khi chuyển đổi theo loại tệp. Ví dụ::

      >>> p = Path('src')
      >>> if p.info.is_symlink():
      ...     print('symlink')
      ... elif p.info.is_dir():
      ...     print('directory')
      ... elif p.info.exists():
      ...     print('something else')
      ... else:
      ...     print('not found')
      ...
      directory

   Nếu đường dẫn được tạo từ :meth:`Path.iterdir` thì thuộc tính này được khởi tạo với một số thông tin về loại tệp, thu được từ việc quét thư mục cha. Chỉ truy cập :attr:`Path.info` sẽ không thực hiện bất kỳ truy vấn hệ thống tệp nào.

   Để lấy thông tin mới nhất, tốt nhất là gọi :meth:`Path.is_dir`,
   :meth:`~Path.is_file` và :meth:`~Path.is_symlink` thay vì các phương thức của thuộc tính này. Không có cách nào để đặt lại bộ nhớ đệm; thay vào đó, bạn có thể tạo một đối tượng đường dẫn mới với bộ nhớ đệm thông tin trống bằng ``p = Path(p)``.

   .. versionadded:: 3.14


Đọc và ghi tệp
^^^^^^^^^^^^^^


.. method:: Path.open(mode='r', buffering=-1, encoding=None, errors=None, newline=None)

   Mở tệp được chỉ định bởi đường dẫn, giống như hàm dựng sẵn :func:`open` thực hiện::

      >>> p = Path('setup.py')
      >>> with p.open() as f:
      ...     f.readline()
      ...
      '#!/usr/bin/env python3\n'


.. method:: Path.read_text(encoding=None, errors=None, newline=None)

   Trả về nội dung đã giải mã của tệp được chỉ định dưới dạng chuỗi::

      >>> p = Path('my_text_file')
      >>> p.write_text('Text file contents')
      18
      >>> p.read_text()
      'Text file contents'

   Tệp được mở rồi đóng. Các tham số tùy chọn có cùng ý nghĩa như trong :func:`open`.

   .. versionadded:: 3.5

   .. versionchanged:: 3.13
      Đã thêm tham số *newline*.


.. method:: Path.read_bytes()

   Trả về nội dung nhị phân của tệp được chỉ định dưới dạng đối tượng bytes::

      >>> p = Path('my_binary_file')
      >>> p.write_bytes(b'Binary file contents')
      20
      >>> p.read_bytes()
      b'Binary file contents'

   .. versionadded:: 3.5


.. method:: Path.write_text(data, encoding=None, errors=None, newline=None)

   Mở tệp được chỉ định ở chế độ văn bản, ghi *data* vào tệp rồi đóng tệp::

      >>> p = Path('my_text_file')
      >>> p.write_text('Text file contents')
      18
      >>> p.read_text()
      'Text file contents'

   Một tệp hiện có cùng tên sẽ bị ghi đè. Các tham số tùy chọn có cùng ý nghĩa như trong :func:`open`.

   .. versionadded:: 3.5

   .. versionchanged:: 3.10
      Đã thêm tham số *newline*.


.. method:: Path.write_bytes(data)

   Mở tệp được chỉ định ở chế độ byte, ghi *data* vào tệp đó rồi đóng tệp::

      >>> p = Path('my_binary_file')
      >>> p.write_bytes(b'Binary file contents')
      20
      >>> p.read_bytes()
      b'Binary file contents'

   Một tệp hiện có cùng tên sẽ bị ghi đè.

   .. versionadded:: 3.5


Đọc thư mục
^^^^^^^^^^^

.. method:: Path.iterdir()

   Khi đường dẫn trỏ đến một thư mục, trả về các đối tượng đường dẫn của nội dung thư mục::

      >>> p = Path('docs')
      >>> for child in p.iterdir(): child
      ...
      PosixPath('docs/conf.py')
      PosixPath('docs/_templates')
      PosixPath('docs/make.bat')
      PosixPath('docs/index.rst')
      PosixPath('docs/_build')
      PosixPath('docs/_static')
      PosixPath('docs/Makefile')

   Các mục con được trả về theo thứ tự tùy ý, còn các mục đặc biệt ``'.'`` và ``'..'`` không được bao gồm. Nếu một tệp bị xóa khỏi hoặc được thêm vào thư mục sau khi tạo iterator, không xác định được liệu đối tượng đường dẫn cho tệp đó có được bao gồm hay không.

   Nếu đường dẫn không phải là một thư mục hoặc không thể truy cập vì lý do khác, :exc:`OSError` sẽ được raise.


.. method:: Path.glob(pattern, *, case_sensitive=None, recurse_symlinks=False)

   Glob *pattern* tương đối đã cho trong thư mục được biểu diễn bởi đường dẫn này, trả về tất cả các tệp khớp (thuộc mọi loại)::

      >>> sorted(Path('.').glob('*.py'))
      [PosixPath('pathlib.py'), PosixPath('setup.py'), PosixPath('test_pathlib.py')]
      >>> sorted(Path('.').glob('*/*.py'))
      [PosixPath('docs/conf.py')]
      >>> sorted(Path('.').glob('**/*.py'))
      [PosixPath('build/lib/pathlib.py'),
       PosixPath('docs/conf.py'),
       PosixPath('pathlib.py'),
       PosixPath('setup.py'),
       PosixPath('test_pathlib.py')]

   .. note::
      Các đường dẫn được trả về theo thứ tự bất kỳ. Nếu cần một thứ tự cụ thể, hãy sắp xếp các kết quả.

   .. seealso::
      :ref:`pathlib-pattern-language` documentation.

   Theo mặc định, hoặc khi đối số chỉ dành cho keyword *case_sensitive* được đặt thành ``None``, phương thức này khớp các đường dẫn bằng quy tắc phân biệt chữ hoa chữ thường riêng của nền tảng: thường là phân biệt chữ hoa chữ thường trên POSIX và không phân biệt trên Windows. Đặt *case_sensitive* thành ``True`` hoặc ``False`` để ghi đè hành vi này.

   Theo mặc định, hoặc khi đối số chỉ dành cho keyword *recurse_symlinks* được đặt thành ``False``, phương thức này đi theo các symlink, ngoại trừ khi mở rộng các wildcard "``**``". Đặt *recurse_symlinks* thành ``True`` để luôn đi theo các symlink.

   .. note::
      Mọi ngoại lệ :exc:`OSError` phát sinh khi quét hệ thống tệp đều bị bỏ qua. Trong đó có :exc:`PermissionError` khi truy cập các thư mục không có quyền đọc.

   .. audit-event:: pathlib.Path.glob self,pattern pathlib.Path.glob

   .. versionchanged:: 3.12
      Tham số *case_sensitive* đã được thêm vào.

   .. versionchanged:: 3.13
      Tham số *recurse_symlinks* đã được thêm vào.

   .. versionchanged:: 3.13
      Tham số *pattern* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.13
      Mọi ngoại lệ :exc:`OSError` phát sinh khi quét hệ thống tệp đều bị bỏ qua. Trong các phiên bản trước, những ngoại lệ như vậy được bỏ qua trong nhiều trường hợp, nhưng không phải tất cả.


.. method:: Path.rglob(pattern, *, case_sensitive=None, recurse_symlinks=False)

   Duyệt đệ quy *pattern* tương đối đã cho. Điều này tương tự như việc gọi
   :func:`Path.glob` với "``**/``" được thêm vào trước *pattern*.

   .. note::
      Các đường dẫn được trả về theo thứ tự bất kỳ. Nếu cần một thứ tự cụ thể, hãy sắp xếp các kết quả.

   .. note::
      Mọi ngoại lệ :exc:`OSError` phát sinh khi quét hệ thống tệp đều bị bỏ qua. Trong đó có :exc:`PermissionError` khi truy cập các thư mục không có quyền đọc.

   .. seealso::
      :ref:`pathlib-pattern-language` and :meth:`Path.glob` documentation.

   .. audit-event:: pathlib.Path.rglob self,pattern pathlib.Path.rglob

   .. versionchanged:: 3.12
      Tham số *case_sensitive* đã được thêm vào.

   .. versionchanged:: 3.13
      Tham số *recurse_symlinks* đã được thêm vào.

   .. versionchanged:: 3.13
      Tham số *pattern* chấp nhận một :term:`path-like object`.


.. method:: Path.walk(top_down=True, on_error=None, follow_symlinks=False)

   Tạo tên tệp trong một cây thư mục bằng cách duyệt cây theo hướng từ trên xuống hoặc từ dưới lên.

   Đối với mỗi thư mục trong cây thư mục có gốc tại *self* (bao gồm *self* nhưng không bao gồm '.' và '..'), phương thức trả về một bộ 3 phần tử gồm ``(dirpath, dirnames, filenames)``.

   *dirpath* là một :class:`Path` đến thư mục hiện đang được duyệt, *dirnames* là danh sách các chuỗi chứa tên của các thư mục con trong *dirpath* (không bao gồm ``'.'`` và ``'..'``), còn *filenames* là danh sách các chuỗi chứa tên của những tệp không phải thư mục trong *dirpath*. Để lấy đường dẫn đầy đủ (bắt đầu bằng *self*) đến một tệp hoặc thư mục trong *dirpath*, hãy thực hiện ``dirpath / name``. Việc các danh sách có được sắp xếp hay không phụ thuộc vào hệ thống tệp.

   Nếu đối số tùy chọn *top_down* là true (đây là giá trị mặc định), bộ ba của một thư mục được tạo trước các bộ ba của mọi thư mục con của nó (các thư mục được duyệt từ trên xuống). Nếu *top_down* là false, bộ ba của một thư mục được tạo sau các bộ ba của tất cả thư mục con của nó (các thư mục được duyệt từ dưới lên). Bất kể giá trị của *top_down* là gì, danh sách các thư mục con được lấy trước khi duyệt các bộ ba của thư mục và các thư mục con của nó.

   Khi *top_down* là true, bên gọi có thể sửa trực tiếp danh sách *dirnames* (ví dụ: sử dụng :keyword:`del` hoặc phép gán lát cắt), và :meth:`Path.walk` sẽ chỉ đệ quy vào các thư mục con có tên vẫn còn trong *dirnames*. Bạn có thể dùng cách này để thu hẹp phạm vi tìm kiếm, áp đặt một thứ tự truy cập cụ thể, hoặc thậm chí thông báo cho :meth:`Path.walk` về các thư mục mà bên gọi tạo hoặc đổi tên trước khi tiếp tục :meth:`Path.walk` lại. Việc sửa đổi *dirnames* khi *top_down* là false không ảnh hưởng đến hành vi của :meth:`Path.walk`, vì các thư mục trong *dirnames* đã được tạo ra trước khi *dirnames* được trả về cho bên gọi.

   Theo mặc định, các lỗi từ :func:`os.scandir` sẽ bị bỏ qua. Nếu chỉ định đối số tùy chọn *on_error*, đối số này phải là một callable; nó sẽ được gọi với một đối số là một đối tượng :exc:`OSError`. Callable này có thể xử lý lỗi để tiếp tục quá trình duyệt hoặc raise lại lỗi để dừng quá trình duyệt. Lưu ý rằng tên tệp có sẵn trong thuộc tính ``filename`` của đối tượng exception.

   Theo mặc định, :meth:`Path.walk` không đi theo các symbolic link mà thay vào đó thêm chúng vào danh sách *filenames*. Đặt *follow_symlinks* thành true để resolve các symbolic link và đưa chúng vào *dirnames* và *filenames* tương ứng với đích của chúng, qua đó truy cập các thư mục được symbolic link trỏ tới (nếu được hỗ trợ).

   .. note::

      Hãy lưu ý rằng việc đặt *follow_symlinks* thành true có thể dẫn đến đệ quy vô hạn nếu một link trỏ tới thư mục cha của chính nó. :meth:`Path.walk` không theo dõi các thư mục mà nó đã truy cập.

   .. note::
      :meth:`Path.walk` assumes the directories it walks are not modified during
      quá trình thực thi. Ví dụ: nếu một thư mục trong *dirnames* đã được thay thế bằng một symbolic link và *follow_symlinks* là false, :meth:`Path.walk` vẫn sẽ cố gắng đi vào thư mục đó. Để ngăn hành vi này, hãy xóa các thư mục khỏi *dirnames* khi thích hợp.

   .. note::

      Không giống :func:`os.walk`, :meth:`Path.walk` liệt kê các symbolic link trỏ tới thư mục trong *filenames* nếu *follow_symlinks* là false.

   Ví dụ này hiển thị số byte được tất cả các tệp trong mỗi thư mục sử dụng, đồng thời bỏ qua các thư mục ``__pycache__``::

      from pathlib import Path
      for root, dirs, files in Path("cpython/Lib/concurrent").walk(on_error=print):
        print(
            root,
            "consumes",
            sum((root / file).stat().st_size for file in files),
            "bytes in",
            len(files),
            "non-directory files"
        )
        if '__pycache__' in dirs:
              dirs.remove('__pycache__')

   Ví dụ tiếp theo là một cách triển khai đơn giản của :func:`shutil.rmtree`. Việc duyệt cây từ dưới lên là cần thiết vì :func:`rmdir` không cho phép xóa một thư mục trước khi thư mục đó rỗng::

      # Xóa mọi thứ có thể truy cập từ thư mục "top".
      # CẢNH BÁO: Thao tác này nguy hiểm! Ví dụ, nếu top == Path('/'),
      # thao tác này có thể xóa toàn bộ tệp của bạn.
      for root, dirs, files in top.walk(top_down=False):
          for name in files:
              (root / name).unlink()
          for name in dirs:
              (root / name).rmdir()

   .. versionadded:: 3.12


Tạo tệp và thư mục
^^^^^^^^^^^^^^^^^^

.. method:: Path.touch(mode=0o666, exist_ok=True)

   Tạo một tệp tại đường dẫn đã cho. Nếu chỉ định *mode*, giá trị này được kết hợp với giá trị ``umask`` của process để xác định chế độ tệp và các cờ truy cập. Nếu tệp đã tồn tại, hàm sẽ thành công khi *exist_ok* là true (đồng thời thời gian sửa đổi của tệp được cập nhật thành thời gian hiện tại); nếu không, :exc:`FileExistsError` sẽ được raised.

   .. seealso::
      :meth:`~Path.open`, :meth:`~Path.write_text` và
      Các phương thức :meth:`~Path.write_bytes` thường được dùng để tạo tệp.


.. method:: Path.mkdir(mode=0o777, parents=False, exist_ok=False)

   Tạo một thư mục mới tại đường dẫn đã cho. Nếu chỉ định *mode*, giá trị này được kết hợp với giá trị ``umask`` của tiến trình để xác định chế độ tệp và các cờ truy cập. Nếu đường dẫn đã tồn tại, :exc:`FileExistsError` sẽ được phát sinh.

   Nếu *parents* là true, mọi thư mục cha còn thiếu của đường dẫn này sẽ được tạo khi cần; chúng được tạo với quyền mặc định mà không xét đến *mode* (mô phỏng lệnh POSIX ``mkdir -p``).

   Nếu *parents* là false (mặc định), thư mục cha còn thiếu sẽ phát sinh
   :exc:`FileNotFoundError`.

   Nếu *exist_ok* là false (mặc định), :exc:`FileExistsError` sẽ được phát sinh nếu thư mục đích đã tồn tại.

   Nếu *exist_ok* là true, :exc:`FileExistsError` sẽ không được phát sinh trừ khi đường dẫn đã cho đã tồn tại trong hệ thống tệp nhưng không phải là một thư mục (hành vi giống lệnh POSIX ``mkdir -p``).

   .. versionchanged:: 3.5
      Tham số *exist_ok* đã được thêm vào.


.. method:: Path.symlink_to(target, target_is_directory=False)

   Biến đường dẫn này thành một symbolic link trỏ đến *target*.

   Trên Windows, symlink đại diện cho một tệp hoặc một thư mục và không tự động thay đổi theo target. Nếu target tồn tại, loại symlink sẽ được tạo để khớp với target. Nếu không, symlink sẽ được tạo dưới dạng thư mục nếu *target_is_directory* là true; nếu không, symlink đến tệp sẽ được tạo (mặc định). Trên các nền tảng không phải Windows, *target_is_directory* sẽ bị bỏ qua.

   ::

      >>> p = Path('mylink')
      >>> p.symlink_to('setup.py')
      >>> p.resolve()
      PosixPath('/home/antoine/pathlib/setup.py')
      >>> p.stat().st_size
      956
      >>> p.lstat().st_size
      8

   .. note::
      Thứ tự các đối số (link, target) ngược với :func:`os.symlink`'s.

   .. versionchanged:: 3.13
      Gây ra :exc:`UnsupportedOperation` nếu :func:`os.symlink` không khả dụng. Trong các phiên bản trước, :exc:`NotImplementedError` sẽ được gây ra.


.. method:: Path.hardlink_to(target)

   Biến đường dẫn này thành một hard link đến cùng tệp với *target*.

   .. note::
      Thứ tự các đối số (link, target) ngược với :func:`os.link`'s.

   .. versionadded:: 3.10

   .. versionchanged:: 3.13
      Gây ra :exc:`UnsupportedOperation` nếu :func:`os.link` không khả dụng. Trong các phiên bản trước, :exc:`NotImplementedError` sẽ được gây ra.


Sao chép, di chuyển và xóa
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: Path.copy(target, *, follow_symlinks=True, preserve_metadata=False)

   Sao chép cây tệp hoặc thư mục này vào *target* đã cho và trả về một
   :class:`!Path` instance mới trỏ đến *target*.

   Nếu nguồn là một tệp, target sẽ được thay thế nếu đó là một tệp hiện có. Nếu nguồn là một symlink và *follow_symlinks* là true (mặc định), target của symlink sẽ được sao chép. Nếu không, symlink sẽ được tạo lại tại đích.

   Nếu *preserve_metadata* là false (mặc định), chỉ cấu trúc thư mục và dữ liệu tệp được đảm bảo sao chép. Đặt *preserve_metadata* thành true để đảm bảo quyền truy cập tệp và thư mục, các flag, thời gian truy cập và sửa đổi gần nhất, cùng các thuộc tính mở rộng được sao chép khi được hỗ trợ. Đối số này không có tác dụng khi sao chép tệp trên Windows (nơi metadata luôn được bảo toàn).

   .. note::
      Khi được hệ điều hành và hệ thống tệp hỗ trợ, phương thức này thực hiện một bản sao nhẹ, trong đó các khối dữ liệu chỉ được sao chép khi bị sửa đổi. Cách này được gọi là copy-on-write.

   .. versionadded:: 3.14


.. method:: Path.copy_into(target_dir, *, follow_symlinks=True, \
                           preserve_metadata=False)

   Sao chép tệp hoặc cây thư mục này vào *target_dir* đã cho, đây phải là một thư mục hiện có. Các đối số khác được xử lý giống hệt như
   :meth:`Path.copy`. Trả về một thực thể :class:`!Path` mới trỏ đến bản sao.

   .. versionadded:: 3.14


.. method:: Path.rename(target)

   Đổi tên tệp hoặc thư mục này thành *target* đã cho, rồi trả về một
   :class:`!Path` mới trỏ đến *target*.  Trên Unix, nếu *target* tồn tại và là một tệp, nó sẽ được âm thầm thay thế nếu người dùng có quyền. Trên Windows, nếu *target* tồn tại, :exc:`FileExistsError` sẽ được nâng lên. *target* có thể là một chuỗi hoặc một đối tượng path khác::

      >>> p = Path('foo')
      >>> p.open('w').write('some text')
      9
      >>> target = Path('bar')
      >>> p.rename(target)
      PosixPath('bar')
      >>> target.open().read()
      'some text'

   Đường dẫn đích có thể là đường dẫn tuyệt đối hoặc tương đối. Các đường dẫn tương đối được diễn giải tương đối với thư mục làm việc hiện tại, *not* thư mục của
   :class:`!Path` object.

   Nó được triển khai dựa trên :func:`os.rename` và cung cấp các đảm bảo tương tự.

   .. versionchanged:: 3.8
      Đã bổ sung giá trị trả về, trả về instance :class:`!Path` mới.


.. method:: Path.replace(target)

   Đổi tên tệp hoặc thư mục này thành *target* đã cho, rồi trả về một
   instance :class:`!Path` trỏ tới *target*. Nếu *target* trỏ tới một tệp hoặc thư mục trống hiện có, nó sẽ bị thay thế vô điều kiện.

   Đường dẫn đích có thể là đường dẫn tuyệt đối hoặc tương đối. Các đường dẫn tương đối được diễn giải tương đối với thư mục làm việc hiện tại, *not* thư mục của
   :class:`!Path` object.

   .. versionchanged:: 3.8
      Đã bổ sung giá trị trả về, trả về instance :class:`!Path` mới.


.. method:: Path.move(target)

   Di chuyển tệp hoặc cây thư mục này tới *target* đã cho và trả về một
   :class:`!Path` instance mới trỏ đến *target*.

   Nếu *target* không tồn tại, nó sẽ được tạo. Nếu cả đường dẫn này và *target* đều là các tệp hiện có, thì target sẽ bị ghi đè. Nếu cả hai đường dẫn trỏ đến cùng một tệp hoặc thư mục, hoặc *target* là một thư mục không rỗng, thì :exc:`OSError` sẽ được raised.

   Nếu cả hai đường dẫn nằm trên cùng một filesystem, thao tác di chuyển được thực hiện bằng
   :func:`os.replace`. Nếu không, đường dẫn này sẽ được sao chép (giữ nguyên metadata và symlink), sau đó bị xóa.

   .. versionadded:: 3.14


.. method:: Path.move_into(target_dir)

   Di chuyển tệp hoặc cây thư mục này vào *target_dir* đã cho, vốn phải là một thư mục hiện có. Trả về một instance :class:`!Path` mới trỏ đến đường dẫn đã di chuyển.

   .. versionadded:: 3.14


.. method:: Path.unlink(missing_ok=False)

   Xóa tệp hoặc symbolic link này. Nếu đường dẫn trỏ đến một thư mục, hãy sử dụng :func:`Path.rmdir` thay thế.

   Nếu *missing_ok* là false (giá trị mặc định), :exc:`FileNotFoundError` sẽ được raised nếu đường dẫn không tồn tại.

   Nếu *missing_ok* là true, :exc:`FileNotFoundError` các ngoại lệ sẽ bị bỏ qua (có cùng hành vi với lệnh POSIX ``rm -f`` này).

   .. versionchanged:: 3.8
      Tham số *missing_ok* đã được thêm vào.


.. method:: Path.rmdir()

   Xóa thư mục này. Thư mục phải rỗng.


Quyền và quyền sở hữu
^^^^^^^^^^^^^^^^^^^^^

.. method:: Path.owner(*, follow_symlinks=True)

   Trả về tên của người dùng sở hữu tệp. :exc:`KeyError` sẽ được phát sinh nếu không tìm thấy mã định danh người dùng (UID) của tệp trong cơ sở dữ liệu hệ thống.

   Phương thức này thường đi theo các symlink; để lấy chủ sở hữu của symlink, hãy thêm đối số ``follow_symlinks=False``.

   .. versionchanged:: 3.13
      Phát sinh :exc:`UnsupportedOperation` nếu module :mod:`pwd` không khả dụng. Trong các phiên bản trước, :exc:`NotImplementedError` được phát sinh.

   .. versionchanged:: 3.13
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.group(*, follow_symlinks=True)

   Trả về tên của nhóm sở hữu tệp. :exc:`KeyError` được phát sinh nếu không tìm thấy mã định danh nhóm (GID) của tệp trong cơ sở dữ liệu hệ thống.

   Phương thức này thường đi theo các symlink; để lấy nhóm của symlink, hãy thêm đối số ``follow_symlinks=False``.

   .. versionchanged:: 3.13
      Phát sinh :exc:`UnsupportedOperation` nếu module :mod:`grp` không khả dụng. Trong các phiên bản trước, :exc:`NotImplementedError` được phát sinh.

   .. versionchanged:: 3.13
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.chmod(mode, *, follow_symlinks=True)

   Thay đổi mode và quyền của tệp, chẳng hạn như :func:`os.chmod`.

   Phương thức này thường đi theo các symlink. Một số biến thể Unix hỗ trợ thay đổi quyền trên chính symlink; trên các nền tảng này, bạn có thể thêm đối số ``follow_symlinks=False`` hoặc sử dụng :meth:`~Path.lchmod`.

   ::

      >>> p = Path('setup.py')
      >>> p.stat().st_mode
      33277
      >>> p.chmod(0o444)
      >>> p.stat().st_mode
      33060

   .. versionchanged:: 3.10
      Tham số *follow_symlinks* đã được thêm vào.


.. method:: Path.lchmod(mode)

   Giống như :meth:`Path.chmod`, nhưng nếu đường dẫn trỏ đến một symbolic link, mode của symbolic link sẽ được thay đổi thay vì mode của đích liên kết.


.. _pathlib-pattern-language:

Ngôn ngữ mẫu
------------

Các ký tự đại diện sau được hỗ trợ trong các mẫu cho
:meth:`~PurePath.full_match`, :meth:`~Path.glob` và :meth:`~Path.rglob`:

``**`` (toàn bộ phân đoạn)
  Khớp với bất kỳ số lượng phân đoạn tệp hoặc thư mục nào, kể cả không có phân đoạn nào.
``*`` (toàn bộ phân đoạn)
  Khớp với một phân đoạn tệp hoặc thư mục.
``*`` (một phần của phân đoạn)
  Khớp với bất kỳ số lượng ký tự không phải ký tự phân tách nào, kể cả không có ký tự nào.
``?``
  Khớp với một ký tự không phải ký tự phân tách.
``[seq]``
  Khớp với một ký tự trong *seq*, trong đó *seq* là một chuỗi ký tự. Các biểu thức phạm vi được hỗ trợ; ví dụ: ``[a-z]`` khớp với bất kỳ chữ cái ASCII viết thường nào. Có thể kết hợp nhiều phạm vi: ``[a-zA-Z0-9_]`` khớp với bất kỳ chữ cái ASCII, chữ số hoặc dấu gạch dưới nào.

``[!seq]``
  Khớp với một ký tự không nằm trong *seq*, trong đó *seq* tuân theo các quy tắc tương tự như trên.

Để khớp theo nghĩa đen, hãy đặt các ký tự meta trong dấu ngoặc vuông. Ví dụ: ``"[?]"`` khớp với ký tự ``"?"``.

Ký tự đại diện "``**``" cho phép glob đệ quy. Một vài ví dụ:

+-------------------+------------------------------------------------------------------------------+
| Mẫu               | Ý nghĩa                                                                      |
+===================+==============================================================================+
| "``**/*``"        | Bất kỳ đường dẫn nào có ít nhất một phân đoạn.                               |
+-------------------+------------------------------------------------------------------------------+
| "``**/*.py``"     | Bất kỳ đường dẫn nào có phân đoạn cuối kết thúc bằng "``.py``".              |
+-------------------+------------------------------------------------------------------------------+
| "``assets/**``"   | Bất kỳ đường dẫn nào bắt đầu bằng "``assets/``".                             |
+-------------------+------------------------------------------------------------------------------+
| "``assets/**/*``" | Mọi đường dẫn bắt đầu bằng "``assets/``", không bao gồm chính "``assets/``". |
+-------------------+------------------------------------------------------------------------------+

.. note::
   Globbing với ký tự đại diện "``**``" sẽ duyệt qua mọi thư mục trong cây. Việc tìm kiếm trong các cây thư mục lớn có thể mất nhiều thời gian.

.. versionchanged:: 3.13
   Globbing với một pattern kết thúc bằng "``**``" sẽ trả về cả tệp và thư mục. Trong các phiên bản trước, chỉ có thư mục được trả về.

Trong :meth:`Path.glob` và :meth:`~Path.rglob`, có thể thêm dấu gạch chéo ở cuối pattern để chỉ khớp với các thư mục.

.. versionchanged:: 3.11
   Globbing với một pattern kết thúc bằng dấu phân cách các thành phần pathname (:data:`~os.sep` hoặc :data:`~os.altsep`) sẽ chỉ trả về các thư mục.


So sánh với module :mod:`glob`
------------------------------

Các pattern được :meth:`Path.glob` chấp nhận và kết quả do :meth:`Path.glob` tạo ra
:meth:`Path.rglob` hơi khác so với các giá trị được trả về bởi mô-đun :mod:`glob`:

1. Các tệp bắt đầu bằng dấu chấm không được xem là đặc biệt trong pathlib. Điều này giống với việc truyền ``include_hidden=True`` cho :func:`glob.glob`.
2. Các thành phần mẫu "``**``" luôn có tính đệ quy trong pathlib. Điều này giống với việc truyền ``recursive=True`` cho :func:`glob.glob`.
3. Theo mặc định, các thành phần mẫu "``**``" không đi theo symlink trong pathlib. Hành vi này không có tương đương trong :func:`glob.glob`, nhưng bạn có thể truyền ``recurse_symlinks=True`` cho :meth:`Path.glob` để có hành vi tương thích.
4. Giống như mọi đối tượng :class:`PurePath` và :class:`Path`, các giá trị được trả về từ :meth:`Path.glob` và :meth:`Path.rglob` không bao gồm dấu gạch chéo ở cuối.
5. Các giá trị được trả về từ ``path.glob()`` và ``path.rglob()`` của pathlib bao gồm *path* làm tiền tố, không giống kết quả của ``glob.glob(root_dir=path)``.
6. Các giá trị được trả về từ ``path.glob()`` và ``path.rglob()`` của pathlib có thể bao gồm chính *path*, chẳng hạn khi glob "``**``", trong khi kết quả của ``glob.glob(root_dir=path)`` không bao giờ bao gồm chuỗi rỗng tương ứng với *path*.


So sánh với các mô-đun :mod:`os` và :mod:`os.path`
--------------------------------------------------

pathlib triển khai các thao tác trên đường dẫn bằng các đối tượng :class:`PurePath` và :class:`Path`, vì vậy nó được xem là *hướng đối tượng*. Mặt khác,
các mô-đun :mod:`os` và :mod:`os.path` cung cấp các hàm làm việc với các đối tượng ``str`` và ``bytes`` cấp thấp, đây là cách tiếp cận *thủ tục* hơn. Một số người dùng cho rằng phong cách hướng đối tượng dễ đọc hơn.

Nhiều hàm trong :mod:`os` và :mod:`os.path` hỗ trợ các đường dẫn ``bytes`` và
:ref:`các đường dẫn tương đối đến bộ mô tả thư mục <dir_fd>`. Những tính năng này không có trong pathlib.

Các kiểu ``str`` và ``bytes`` của Python, cùng với một số phần của các mô-đun :mod:`os` và
:mod:`os.path`, được viết bằng C và có tốc độ rất nhanh. pathlib được viết hoàn toàn bằng Python và thường chậm hơn, nhưng hiếm khi chậm đến mức đáng kể.

Việc chuẩn hóa đường dẫn của pathlib có tính áp đặt và nhất quán hơn một chút so với
:mod:`os.path`. Ví dụ, trong khi :func:`os.path.abspath` loại bỏ các đoạn "``..``" khỏi một đường dẫn, điều này có thể làm thay đổi ý nghĩa của đường dẫn nếu có liên quan đến symlink, thì :meth:`Path.absolute` giữ lại các đoạn này để an toàn hơn.

Việc chuẩn hóa đường dẫn của pathlib có thể khiến nó không phù hợp với một số ứng dụng:

1. pathlib chuẩn hóa ``Path("my_folder/")`` thành ``Path("my_folder")``, làm thay đổi ý nghĩa của đường dẫn khi được truyền cho nhiều API của hệ điều hành và tiện ích dòng lệnh. Cụ thể, việc không có dấu phân cách ở cuối có thể cho phép đường dẫn được phân giải thành tệp hoặc thư mục, thay vì chỉ là thư mục.
2. pathlib chuẩn hóa ``Path("./my_program")`` thành ``Path("my_program")``, làm thay đổi ý nghĩa của đường dẫn khi được sử dụng làm đường dẫn tìm kiếm executable, chẳng hạn như trong shell hoặc khi khởi chạy một tiến trình con. Cụ thể, việc không có dấu phân cách trong đường dẫn có thể buộc đường dẫn được tìm kiếm trong :envvar:`PATH` thay vì thư mục hiện tại.

Do những khác biệt này, pathlib không phải là một lựa chọn thay thế trực tiếp cho :mod:`os.path`.


Các công cụ tương ứng
^^^^^^^^^^^^^^^^^^^^^

Dưới đây là bảng ánh xạ nhiều hàm :mod:`os` khác nhau với hàm tương ứng
tương đương với :class:`PurePath`/:class:`Path`.

+---------------------------------------+------------------------------------------------+
| :mod:`os` và :mod:`os.path`           | :mod:`!pathlib`                                |
+=======================================+================================================+
| :func:`os.path.dirname`               | :attr:`PurePath.parent`                        |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.basename`              | :attr:`PurePath.name`                          |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.splitext`              | :attr:`PurePath.stem`, :attr:`PurePath.suffix` |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.join`                  | :meth:`PurePath.joinpath`                      |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.isabs`                 | :meth:`PurePath.is_absolute`                   |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.relpath`               | :meth:`PurePath.relative_to` [1]_              |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.expanduser`            | :meth:`Path.expanduser` [2]_                   |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.realpath`              | :meth:`Path.resolve`                           |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.abspath`               | :meth:`Path.absolute` [3]_                     |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.exists`                | :meth:`Path.exists`                            |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.isfile`                | :meth:`Path.is_file`                           |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.isdir`                 | :meth:`Path.is_dir`                            |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.islink`                | :meth:`Path.is_symlink`                        |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.isjunction`            | :meth:`Path.is_junction`                       |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.ismount`               | :meth:`Path.is_mount`                          |
+---------------------------------------+------------------------------------------------+
| :func:`os.path.samefile`              | :meth:`Path.samefile`                          |
+---------------------------------------+------------------------------------------------+
| :func:`os.getcwd`                     | :meth:`Path.cwd`                               |
+---------------------------------------+------------------------------------------------+
| :func:`os.stat`                       | :meth:`Path.stat`                              |
+---------------------------------------+------------------------------------------------+
| :func:`os.lstat`                      | :meth:`Path.lstat`                             |
+---------------------------------------+------------------------------------------------+
| :func:`os.listdir`                    | :meth:`Path.iterdir`                           |
+---------------------------------------+------------------------------------------------+
| :func:`os.walk`                       | :meth:`Path.walk` [4]_                         |
+---------------------------------------+------------------------------------------------+
| :func:`os.mkdir`, :func:`os.makedirs` | :meth:`Path.mkdir`                             |
+---------------------------------------+------------------------------------------------+
| :func:`os.link`                       | :meth:`Path.hardlink_to`                       |
+---------------------------------------+------------------------------------------------+
| :func:`os.symlink`                    | :meth:`Path.symlink_to`                        |
+---------------------------------------+------------------------------------------------+
| :func:`os.readlink`                   | :meth:`Path.readlink`                          |
+---------------------------------------+------------------------------------------------+
| :func:`os.rename`                     | :meth:`Path.rename`                            |
+---------------------------------------+------------------------------------------------+
| :func:`os.replace`                    | :meth:`Path.replace`                           |
+---------------------------------------+------------------------------------------------+
| :func:`os.remove`, :func:`os.unlink`  | :meth:`Path.unlink`                            |
+---------------------------------------+------------------------------------------------+
| :func:`os.rmdir`                      | :meth:`Path.rmdir`                             |
+---------------------------------------+------------------------------------------------+
| :func:`os.chmod`                      | :meth:`Path.chmod`                             |
+---------------------------------------+------------------------------------------------+
| :func:`os.lchmod`                     | :meth:`Path.lchmod`                            |
+---------------------------------------+------------------------------------------------+

.. rubric:: Chú thích cuối trang

.. [1] :func:`os.path.relpath` gọi :func:`~os.path.abspath` để chuyển các đường dẫn thành đường dẫn tuyệt đối và loại bỏ các phần "``..``", trong khi :meth:`PurePath.relative_to` là một phép toán từ vựng, sẽ raise :exc:`ValueError` khi các điểm neo của đầu vào khác nhau (ví dụ: khi một đường dẫn là tuyệt đối còn đường dẫn kia là tương đối.)
.. [2] :func:`os.path.expanduser` trả về đường dẫn không thay đổi nếu không thể phân giải thư mục home, trong khi :meth:`Path.expanduser` sẽ raise
   :exc:`RuntimeError`.
.. [3] :func:`os.path.abspath` loại bỏ các thành phần "``..``" mà không phân giải symbolic link, điều này có thể làm thay đổi ý nghĩa của đường dẫn, trong khi
   :meth:`Path.absolute` giữ nguyên mọi thành phần "``..``" trong đường dẫn.
.. [4] :func:`os.walk` luôn đi theo các symbolic link khi phân loại đường dẫn thành *dirnames* và *filenames*, trong khi :meth:`Path.walk` phân loại mọi symbolic link thành *filenames* khi *follow_symlinks* là false (giá trị mặc định).


Protocols
---------

.. module:: pathlib.types
   :synopsis: các kiểu pathlib để kiểm tra kiểu tĩnh


Module :mod:`!pathlib.types` cung cấp các kiểu để kiểm tra kiểu tĩnh.

.. versionadded:: 3.14


.. class:: PathInfo()

   Một :class:`typing.Protocol` mô tả
   thuộc tính :attr:`Path.info <pathlib.Path.info>`. Các triển khai có thể trả về kết quả được lưu trong bộ nhớ đệm từ các phương thức của chúng.

   .. method:: exists(*, follow_symlinks=True)

      Trả về ``True`` nếu đường dẫn là một tệp hoặc thư mục hiện có, hoặc bất kỳ loại tệp nào khác; trả về ``False`` nếu đường dẫn không tồn tại.

      Nếu *follow_symlinks* là ``False``, trả về ``True`` cho các symlink mà không kiểm tra đích của chúng có tồn tại hay không.

   .. method:: is_dir(*, follow_symlinks=True)

      Trả về ``True`` nếu đường dẫn là một thư mục hoặc một symbolic link trỏ đến một thư mục; trả về ``False`` nếu đường dẫn là (hoặc trỏ đến) bất kỳ loại tệp nào khác, hoặc nếu đường dẫn không tồn tại.

      Nếu *follow_symlinks* là ``False``, chỉ trả về ``True`` nếu đường dẫn là một thư mục (không theo symbolic link); trả về ``False`` nếu đường dẫn là bất kỳ loại tệp nào khác, hoặc nếu đường dẫn không tồn tại.

   .. method:: is_file(*, follow_symlinks=True)

      Trả về ``True`` nếu đường dẫn là một tệp hoặc một symbolic link trỏ đến một tệp; trả về ``False`` nếu đường dẫn là (hoặc trỏ đến) một thư mục hoặc đối tượng không phải tệp khác, hoặc nếu đường dẫn không tồn tại.

      Nếu *follow_symlinks* là ``False``, chỉ trả về ``True`` nếu đường dẫn là một tệp (không theo symbolic link); trả về ``False`` nếu đường dẫn là một thư mục hoặc đối tượng không phải tệp khác, hoặc nếu đường dẫn không tồn tại.

   .. method:: is_symlink()

      Trả về ``True`` nếu đường dẫn là một symbolic link (ngay cả khi bị hỏng); trả về ``False`` nếu đường dẫn là một thư mục hoặc bất kỳ loại tệp nào, hoặc nếu đường dẫn không tồn tại.

.. _`4.11 Pathname Resolution`: https://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap04.html#tag_04_11
