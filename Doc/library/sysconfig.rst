:mod:`!sysconfig` --- Cung cấp quyền truy cập vào thông tin cấu hình của Python
===============================================================================

.. module:: sysconfig
   :synopsis: Thông tin cấu hình của Python

.. moduleauthor:: Tarek Ziadé <tarek@ziade.org>
.. sectionauthor:: Tarek Ziadé <tarek@ziade.org>

.. versionadded:: 3.2

**Mã nguồn:** :source:`Lib/sysconfig`

.. index::
   single: configuration information

--------------

Mô-đun :mod:`!sysconfig` cung cấp quyền truy cập vào thông tin cấu hình của Python, chẳng hạn như danh sách các đường dẫn cài đặt và các biến cấu hình liên quan đến nền tảng hiện tại.


Các biến cấu hình
-----------------

Một bản phân phối Python chứa tệp tiêu đề :file:`Makefile` và :file:`pyconfig.h`, cần thiết để xây dựng cả tệp nhị phân Python và các phần mở rộng C của bên thứ ba được biên dịch bằng ``setuptools``.

:mod:`!sysconfig` đưa tất cả các biến được tìm thấy trong những tệp này vào một dictionary có thể được truy cập bằng :func:`get_config_vars` hoặc :func:`get_config_var`.

Lưu ý rằng trên Windows, tập hợp này nhỏ hơn nhiều.

.. function:: get_config_vars(*args)

   Khi không có đối số, trả về một dictionary chứa tất cả các biến cấu hình liên quan đến nền tảng hiện tại.

   Khi có đối số, trả về danh sách các giá trị thu được bằng cách tra cứu từng đối số trong dictionary biến cấu hình.

   Với mỗi đối số, nếu không tìm thấy giá trị, trả về ``None``.


.. function:: get_config_var(name)

   Trả về giá trị của một biến duy nhất *name*. Tương đương với ``get_config_vars().get(name)``.

   Nếu không tìm thấy *name*, trả về ``None``.

Ví dụ sử dụng::

   >>> import sysconfig
   >>> sysconfig.get_config_var('Py_ENABLE_SHARED')
   0
   >>> sysconfig.get_config_var('LIBDIR')
   '/usr/local/lib'
   >>> sysconfig.get_config_vars('AR', 'CXX')
   ['ar', 'g++']


.. _installation_paths:

Đường dẫn cài đặt
-----------------

Python sử dụng một lược đồ cài đặt khác nhau tùy thuộc vào nền tảng và các tùy chọn cài đặt. Các lược đồ này được lưu trữ trong :mod:`!sysconfig` dưới các mã định danh duy nhất dựa trên giá trị do :const:`os.name` trả về. Các trình cài đặt gói sử dụng những lược đồ này để xác định nơi sao chép tệp.

Python hiện hỗ trợ chín lược đồ:

- *posix_prefix*: lược đồ dành cho các nền tảng POSIX như Linux hoặc macOS. Đây là lược đồ mặc định được sử dụng khi Python hoặc một thành phần được cài đặt.
- *posix_home*: lược đồ dành cho các nền tảng POSIX khi sử dụng tùy chọn *home*. Lược đồ này xác định các đường dẫn nằm dưới một tiền tố home cụ thể.
- *posix_user*: lược đồ dành cho các nền tảng POSIX khi sử dụng tùy chọn *user*. Lược đồ này xác định các đường dẫn nằm dưới thư mục home của người dùng (:const:`site.USER_BASE`).
- *posix_venv*: lược đồ dành cho :mod:`Python virtual environments <venv>` trên các nền tảng POSIX; theo mặc định, lược đồ này giống với *posix_prefix*.
- *nt*: scheme dành cho Windows. Đây là scheme mặc định được sử dụng khi Python hoặc một thành phần được cài đặt.
- *nt_user*: scheme dành cho Windows khi sử dụng tùy chọn *user*.
- *nt_venv*: scheme dành cho :mod:`Python virtual environments <venv>` trên Windows; theo mặc định, nó giống với *nt*.
- *venv*: scheme có các giá trị từ *posix_venv* hoặc *nt_venv* tùy thuộc vào nền tảng mà Python đang chạy.
- *osx_framework_user*: scheme dành cho macOS khi sử dụng tùy chọn *user*.

Mỗi scheme được cấu thành từ một loạt đường dẫn và mỗi đường dẫn có một mã định danh duy nhất. Hiện tại Python sử dụng tám đường dẫn:

- *stdlib*: thư mục chứa các tệp thư viện Python chuẩn không phụ thuộc vào nền tảng.
- *platstdlib*: thư mục chứa các tệp thư viện Python chuẩn dành riêng cho nền tảng.
- *platlib*: thư mục dành cho các tệp dành riêng cho site và nền tảng.
- *purelib*: thư mục dành cho các tệp dành riêng cho site nhưng không phụ thuộc nền tảng (Python 'thuần').
- *include*: thư mục dành cho các tệp header không phụ thuộc nền tảng của Python C-API.
- *platinclude*: thư mục dành cho các tệp header dành riêng cho nền tảng của Python C-API.
- *scripts*: thư mục dành cho các tệp script.
- *data*: thư mục dành cho các tệp dữ liệu.


.. _sysconfig-user-scheme:

Scheme dành cho người dùng
--------------------------

Scheme này được thiết kế để trở thành giải pháp thuận tiện nhất cho những người dùng không có quyền ghi vào thư mục global site-packages hoặc không muốn cài đặt vào đó.

Các tệp sẽ được cài đặt vào các thư mục con của :const:`site.USER_BASE` (sau đây được viết là :file:`{userbase}`). Scheme này cài đặt các module Python thuần túy và các module mở rộng tại cùng một vị trí (còn được gọi là :const:`site.USER_SITE`).

``posix_user``
^^^^^^^^^^^^^^

+--------------+--------------------------------------------------+
| Đường dẫn    | Thư mục cài đặt                                  |
+==============+==================================================+
| *stdlib*     | :file:`{userbase}/lib/python{X.Y}`               |
+--------------+--------------------------------------------------+
| *platstdlib* | :file:`{userbase}/lib/python{X.Y}`               |
+--------------+--------------------------------------------------+
| *platlib*    | :file:`{userbase}/lib/python{X.Y}/site-packages` |
+--------------+--------------------------------------------------+
| *purelib*    | :file:`{userbase}/lib/python{X.Y}/site-packages` |
+--------------+--------------------------------------------------+
| *include*    | :file:`{userbase}/include/python{X.Y}`           |
+--------------+--------------------------------------------------+
| *scripts*    | :file:`{userbase}/bin`                           |
+--------------+--------------------------------------------------+
| *data*       | :file:`{userbase}`                               |
+--------------+--------------------------------------------------+

``nt_user``
^^^^^^^^^^^

+--------------+-----------------------------------------------+
| Đường dẫn    | Thư mục cài đặt                               |
+==============+===============================================+
| *stdlib*     | :file:`{userbase}\\Python{XY}`                |
+--------------+-----------------------------------------------+
| *platstdlib* | :file:`{userbase}\\Python{XY}`                |
+--------------+-----------------------------------------------+
| *platlib*    | :file:`{userbase}\\Python{XY}\\site-packages` |
+--------------+-----------------------------------------------+
| *purelib*    | :file:`{userbase}\\Python{XY}\\site-packages` |
+--------------+-----------------------------------------------+
| *include*    | :file:`{userbase}\\Python{XY}\\Include`       |
+--------------+-----------------------------------------------+
| *scripts*    | :file:`{userbase}\\Python{XY}\\Scripts`       |
+--------------+-----------------------------------------------+
| *data*       | :file:`{userbase}`                            |
+--------------+-----------------------------------------------+

``osx_framework_user``
^^^^^^^^^^^^^^^^^^^^^^

+--------------+---------------------------------------------+
| Đường dẫn    | Thư mục cài đặt                             |
+==============+=============================================+
| *stdlib*     | :file:`{userbase}/lib/python`               |
+--------------+---------------------------------------------+
| *platstdlib* | :file:`{userbase}/lib/python`               |
+--------------+---------------------------------------------+
| *platlib*    | :file:`{userbase}/lib/python/site-packages` |
+--------------+---------------------------------------------+
| *purelib*    | :file:`{userbase}/lib/python/site-packages` |
+--------------+---------------------------------------------+
| *include*    | :file:`{userbase}/include/python{X.Y}`      |
+--------------+---------------------------------------------+
| *scripts*    | :file:`{userbase}/bin`                      |
+--------------+---------------------------------------------+
| *data*       | :file:`{userbase}`                          |
+--------------+---------------------------------------------+


.. _sysconfig-home-scheme:

Lược đồ home
------------

Ý tưởng đằng sau "lược đồ home" là bạn xây dựng và duy trì một bộ sưu tập cá nhân các module Python. Tên của lược đồ này bắt nguồn từ ý tưởng về một thư mục "home" trên Unix, vì người dùng Unix thường tạo thư mục home của họ với bố cục tương tự :file:`/usr/` hoặc :file:`/usr/local/`. Bất kỳ ai cũng có thể sử dụng lược đồ này, bất kể hệ điều hành mà họ đang cài đặt cho nó.

``posix_home``
^^^^^^^^^^^^^^

+---------------+-------------------------------+
| Đường dẫn     | Thư mục cài đặt               |
+===============+===============================+
| *stdlib*      | :file:`{home}/lib/python`     |
+---------------+-------------------------------+
| *platstdlib*  | :file:`{home}/lib/python`     |
+---------------+-------------------------------+
| *platlib*     | :file:`{home}/lib/python`     |
+---------------+-------------------------------+
| *purelib*     | :file:`{home}/lib/python`     |
+---------------+-------------------------------+
| *include*     | :file:`{home}/include/python` |
+---------------+-------------------------------+
| *platinclude* | :file:`{home}/include/python` |
+---------------+-------------------------------+
| *scripts*     | :file:`{home}/bin`            |
+---------------+-------------------------------+
| *data*        | :file:`{home}`                |
+---------------+-------------------------------+


.. _sysconfig-prefix-scheme:

Lược đồ tiền tố
---------------

“Lược đồ tiền tố” hữu ích khi bạn muốn sử dụng một bản cài đặt Python để thực hiện quá trình build/install (tức là chạy script setup), nhưng cài đặt các module vào thư mục module bên thứ ba của một bản cài đặt Python khác (hoặc một thứ trông giống như một bản cài đặt Python khác). Nếu điều này nghe có vẻ hơi bất thường thì đúng là như vậy---đó là lý do các lược đồ user và home được trình bày trước. Tuy nhiên, có ít nhất hai trường hợp đã biết mà lược đồ tiền tố sẽ hữu ích.

Trước tiên, hãy xét việc nhiều bản phân phối Linux đặt Python trong :file:`/usr`, thay vì :file:`/usr/local` theo cách truyền thống hơn. Điều này hoàn toàn phù hợp, vì trong những trường hợp đó Python là một phần của “hệ thống”, chứ không phải một phần bổ sung cục bộ. Tuy nhiên, nếu bạn đang cài đặt các module Python từ mã nguồn, có lẽ bạn muốn chúng được đặt trong :file:`/usr/local/lib/python2.{X}` thay vì
:file:`/usr/lib/python2.{X}`.

Một khả năng khác là một filesystem mạng, trong đó tên được dùng để ghi vào một thư mục từ xa khác với tên được dùng để đọc thư mục đó: ví dụ, trình thông dịch Python được truy cập dưới dạng :file:`/usr/local/bin/python` có thể tìm kiếm các module trong :file:`/usr/local/lib/python2.{X}`, nhưng các module đó sẽ phải được cài đặt vào, chẳng hạn, :file:`/mnt/{@server}/export/lib/python2.{X}`.

``posix_prefix``
^^^^^^^^^^^^^^^^

+---------------+------------------------------------------------+
| Đường dẫn     | Thư mục cài đặt                                |
+===============+================================================+
| *stdlib*      | :file:`{prefix}/lib/python{X.Y}`               |
+---------------+------------------------------------------------+
| *platstdlib*  | :file:`{prefix}/lib/python{X.Y}`               |
+---------------+------------------------------------------------+
| *platlib*     | :file:`{prefix}/lib/python{X.Y}/site-packages` |
+---------------+------------------------------------------------+
| *purelib*     | :file:`{prefix}/lib/python{X.Y}/site-packages` |
+---------------+------------------------------------------------+
| *include*     | :file:`{prefix}/include/python{X.Y}`           |
+---------------+------------------------------------------------+
| *platinclude* | :file:`{prefix}/include/python{X.Y}`           |
+---------------+------------------------------------------------+
| *scripts*     | :file:`{prefix}/bin`                           |
+---------------+------------------------------------------------+
| *data*        | :file:`{prefix}`                               |
+---------------+------------------------------------------------+

``nt``
^^^^^^

+---------------+--------------------------------------+
| Đường dẫn     | Thư mục cài đặt                      |
+===============+======================================+
| *stdlib*      | :file:`{prefix}\\Lib`                |
+---------------+--------------------------------------+
| *platstdlib*  | :file:`{prefix}\\Lib`                |
+---------------+--------------------------------------+
| *platlib*     | :file:`{prefix}\\Lib\\site-packages` |
+---------------+--------------------------------------+
| *purelib*     | :file:`{prefix}\\Lib\\site-packages` |
+---------------+--------------------------------------+
| *include*     | :file:`{prefix}\\Include`            |
+---------------+--------------------------------------+
| *platinclude* | :file:`{prefix}\\Include`            |
+---------------+--------------------------------------+
| *scripts*     | :file:`{prefix}\\Scripts`            |
+---------------+--------------------------------------+
| *data*        | :file:`{prefix}`                     |
+---------------+--------------------------------------+


Các hàm về đường dẫn cài đặt
----------------------------

:mod:`!sysconfig` cung cấp một số hàm để xác định các đường dẫn cài đặt này.

.. function:: get_scheme_names()

   Trả về một tuple chứa tất cả các scheme hiện được hỗ trợ trong
   :mod:`!sysconfig`.


.. function:: get_default_scheme()

   Trả về tên scheme mặc định cho nền tảng hiện tại.

   .. versionadded:: 3.10
      Hàm này trước đây có tên là ``_get_default_scheme()`` và được xem là chi tiết triển khai.

   .. versionchanged:: 3.11
      Khi Python chạy trong một môi trường ảo, scheme *venv* được trả về.

.. function:: get_preferred_scheme(key)

   Trả về tên scheme ưu tiên cho bố cục cài đặt được chỉ định bởi *key*.

   *key* phải là ``"prefix"``, ``"home"`` hoặc ``"user"``.

   Giá trị trả về là một tên scheme được liệt kê trong :func:`get_scheme_names`. Nó có thể được truyền cho các hàm :mod:`!sysconfig` nhận đối số *scheme*, chẳng hạn như :func:`get_paths`.

   .. versionadded:: 3.10

   .. versionchanged:: 3.11
      Khi Python chạy trong một môi trường ảo và ``key="prefix"``, scheme *venv* được trả về.


.. function:: _get_preferred_schemes()

   Trả về một dict chứa các tên scheme ưu tiên trên nền tảng hiện tại. Các nhà triển khai và nhà phân phối lại Python có thể thêm các scheme ưu tiên của họ vào giá trị toàn cục cấp mô-đun ``_INSTALL_SCHEMES`` và sửa đổi hàm này để trả về các tên scheme đó, chẳng hạn nhằm cung cấp các scheme khác nhau cho trình quản lý gói hệ thống và trình quản lý gói ngôn ngữ sử dụng, để các gói được cài đặt bởi một bên không bị trộn lẫn với các gói được cài đặt bởi bên kia.

   Người dùng cuối không nên sử dụng hàm này, mà nên dùng :func:`get_default_scheme` và
   :func:`get_preferred_scheme` thay vào đó.

   .. versionadded:: 3.10


.. function:: get_path_names()

   Trả về một tuple chứa tất cả tên đường dẫn hiện được hỗ trợ trong
   :mod:`!sysconfig`.


.. function:: get_path(name, [scheme, [vars, [expand]]])

   Trả về đường dẫn cài đặt tương ứng với tên đường dẫn *name*, từ lược đồ cài đặt có tên *scheme*.

   *name* phải là một giá trị trong danh sách do :func:`get_path_names` trả về.

   :mod:`!sysconfig` lưu trữ các đường dẫn cài đặt tương ứng với từng tên đường dẫn cho mỗi nền tảng, cùng với các biến cần được mở rộng. Ví dụ: đường dẫn *stdlib* cho lược đồ *nt* là: ``{base}/Lib``.

   :func:`get_path` sẽ sử dụng các biến do :func:`get_config_vars` trả về để mở rộng đường dẫn. Tất cả biến đều có giá trị mặc định cho mỗi nền tảng, vì vậy có thể gọi hàm này để nhận giá trị mặc định.

   Nếu *scheme* được cung cấp, giá trị này phải nằm trong danh sách được trả về bởi
   :func:`get_scheme_names`. Nếu không, scheme mặc định cho nền tảng hiện tại sẽ được sử dụng.

   Nếu *vars* được cung cấp, giá trị này phải là một dictionary chứa các biến dùng để cập nhật dictionary được trả về bởi :func:`get_config_vars`.

   Nếu *expand* được đặt thành ``False``, đường dẫn sẽ không được mở rộng bằng các biến.

   Nếu không tìm thấy *name*, hãy raise một :exc:`KeyError`.


.. function:: get_paths([scheme, [vars, [expand]]])

   Trả về một dictionary chứa tất cả các đường dẫn cài đặt tương ứng với một scheme cài đặt. Xem :func:`get_path` để biết thêm thông tin.

   Nếu *scheme* không được cung cấp, scheme mặc định cho nền tảng hiện tại sẽ được sử dụng.

   Nếu *vars* được cung cấp, nó phải là một dictionary chứa các biến sẽ cập nhật dictionary được dùng để mở rộng các đường dẫn.

   Nếu *expand* được đặt thành false, các đường dẫn sẽ không được mở rộng.

   Nếu *scheme* không phải là một scheme hiện có, :func:`get_paths` sẽ phát sinh một
   :exc:`KeyError`.


Các hàm khác
------------

.. function:: get_python_version()

   Trả về số phiên bản Python của ``MAJOR.MINOR`` dưới dạng chuỗi. Tương tự như ``'%d.%d' % sys.version_info[:2]``.


.. function:: get_platform()

   Trả về một chuỗi xác định platform hiện tại.

   Chuỗi này chủ yếu được dùng để phân biệt các thư mục build dành riêng cho platform và các bản phân phối đã build dành riêng cho platform. Thông thường, chuỗi bao gồm tên và phiên bản hệ điều hành cùng kiến trúc (do :func:`os.uname` cung cấp), mặc dù thông tin cụ thể được bao gồm phụ thuộc vào hệ điều hành; ví dụ: trên Linux, phiên bản kernel không đặc biệt quan trọng.

   Ví dụ về các giá trị được trả về:


   Windows:

   - win-amd64 (Windows 64 bit trên AMD64, còn được gọi là x86_64, Intel64 và EM64T)
   - win-arm64 (Windows 64 bit trên ARM64, còn được gọi là AArch64)
   - win32 (tất cả các trường hợp khác - cụ thể là, sys.platform được trả về)

   Hệ điều hành dựa trên POSIX:

   - linux-x86_64
   - macosx-15.5-arm64
   - macosx-26.0-universal2 (macOS trên Apple Silicon hoặc Intel)
   - android-24-arm64_v8a

   Đối với các nền tảng không phải POSIX khác, hiện chỉ trả về :data:`sys.platform`.


.. function:: is_python_build()

   Trả về ``True`` nếu trình thông dịch Python đang chạy được xây dựng từ mã nguồn và đang được chạy từ vị trí đã xây dựng, chứ không phải từ một vị trí có được do, chẳng hạn, chạy ``make install`` hoặc cài đặt bằng trình cài đặt nhị phân.


.. function:: parse_config_h(fp[, vars])

   Phân tích cú pháp tệp kiểu :file:`config.h`\-.

   *fp* là một đối tượng giống tệp trỏ đến tệp giống :file:`config.h`\-.

   Một dictionary chứa các cặp name/value được trả về. Nếu truyền một dictionary tùy chọn vào làm đối số thứ hai, dictionary đó sẽ được sử dụng thay cho một dictionary mới và được cập nhật bằng các giá trị đọc từ tệp.


.. function:: get_config_h_filename()

   Trả về đường dẫn của :file:`pyconfig.h`.

.. function:: get_makefile_filename()

   Trả về đường dẫn của :file:`Makefile`.

.. _sysconfig-cli:
.. _using-sysconfig-as-a-script:

Cách sử dụng trên dòng lệnh
---------------------------

Bạn có thể sử dụng :mod:`!sysconfig` như một script với tùy chọn *-m* của Python:

.. code-block:: shell-session

    $ python -m sysconfig
    Platform: "macosx-10.4-i386"
    Python version: "3.2"
    Current installation scheme: "posix_prefix"

    Paths:
            data = "/usr/local"
            include = "/Users/tarek/Dev/svn.python.org/py3k/Include"
            platinclude = "."
            platlib = "/usr/local/lib/python3.2/site-packages"
            platstdlib = "/usr/local/lib/python3.2"
            purelib = "/usr/local/lib/python3.2/site-packages"
            scripts = "/usr/local/bin"
            stdlib = "/usr/local/lib/python3.2"

    Variables:
            AC_APPLE_UNIVERSAL_BUILD = "0"
            AIX_GENUINE_CPLUSPLUS = "0"
            AR = "ar"
            ARFLAGS = "rc"
            ...

Lệnh gọi này sẽ in thông tin được trả về bởi ra đầu ra tiêu chuẩn
:func:`get_platform`, :func:`get_python_version`, :func:`get_path` và
:func:`get_config_vars`.
