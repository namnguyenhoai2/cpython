:mod:`!site` --- Móc cấu hình dành riêng cho từng site
======================================================

.. module:: site
   :synopsis: Mô-đun chịu trách nhiệm về cấu hình dành riêng cho từng site.

**Mã nguồn:** :source:`Lib/site.py`

--------------

.. highlight:: none

**Mô-đun này được tự động import trong quá trình khởi tạo.** Có thể ngăn việc import tự động bằng tùy chọn :option:`-S` của trình thông dịch.

.. index:: triple: module; search; path

Việc import mô-đun này thường thêm các đường dẫn dành riêng cho từng site vào đường dẫn tìm kiếm mô-đun và thêm :ref:`callables <site-consts>`, bao gồm :func:`help` vào namespace tích hợp sẵn. Tuy nhiên, tùy chọn khởi động Python :option:`-S` sẽ ngăn điều này, và có thể import mô-đun này một cách an toàn mà không tự động sửa đổi đường dẫn tìm kiếm mô-đun hoặc bổ sung vào builtins. Để kích hoạt rõ ràng các bổ sung dành riêng cho site như thông thường, hãy gọi hàm :func:`main`.

.. versionchanged:: 3.3
   Việc import mô-đun này trước đây vẫn kích hoạt thao tác thay đổi đường dẫn ngay cả khi sử dụng
   :option:`-S`.

.. index::
   pair: site-packages; directory

Mô-đun bắt đầu bằng cách tạo tối đa bốn thư mục từ một phần đầu và một phần đuôi. Đối với phần đầu, mô-đun sử dụng ``sys.prefix`` và ``sys.exec_prefix``; các phần đầu rỗng sẽ bị bỏ qua. Đối với phần đuôi, mô-đun sử dụng chuỗi rỗng rồi
:file:`lib/site-packages` (trên Windows) hoặc
:file:`lib/python{X.Y[t]}/site-packages` (trên Unix và macOS). (Hậu tố tùy chọn "t" cho biết :term:`free-threaded build`, và được thêm vào nếu ``"t"`` có trong hằng số :data:`sys.abiflags`.) Với mỗi tổ hợp head-tail khác nhau, hàm này kiểm tra xem tổ hợp đó có trỏ đến một thư mục hiện có hay không; nếu có, hàm thêm thư mục đó vào ``sys.path`` và cũng kiểm tra đường dẫn mới được thêm để tìm các tệp cấu hình.

.. versionchanged:: 3.5
   Đã xóa hỗ trợ cho thư mục "site-python".

.. versionchanged:: 3.13
   Trên Unix, các bản cài đặt Python :term:`Free threading <free threading>` được nhận diện bằng hậu tố "t" trong tên thư mục dành riêng cho từng phiên bản, chẳng hạn như
   :file:`lib/python3.13t/`.

.. versionchanged:: 3.14

   :mod:`!site` không còn chịu trách nhiệm cập nhật :data:`sys.prefix` và
   :data:`sys.exec_prefix` trên :ref:`sys-path-init-virtual-environments`. Việc này hiện được thực hiện trong quá trình :ref:`khởi tạo path <sys-path-init>`. Do đó, trong :ref:`sys-path-init-virtual-environments`, :data:`sys.prefix` và
   :data:`sys.exec_prefix` không còn phụ thuộc vào quá trình khởi tạo :mod:`!site`, vì vậy không bị ảnh hưởng bởi :option:`-S`.

.. _site-virtual-environments-configuration:

Khi chạy trong :ref:`môi trường ảo <sys-path-init-virtual-environments>`, hệ thống sẽ kiểm tra tệp ``pyvenv.cfg`` trong :data:`sys.prefix` để tìm các cấu hình dành riêng cho hệ thống. Nếu khóa ``include-system-site-packages`` tồn tại và được đặt thành ``true`` (không phân biệt chữ hoa chữ thường), các tiền tố cấp hệ thống sẽ được tìm kiếm để tìm site-packages; nếu không thì sẽ không tìm kiếm.

.. index::
   single: # (hash); comment
   pair: statement; import

Tệp cấu hình đường dẫn là tệp có tên theo dạng :file:`{name}.pth` và tồn tại trong một trong bốn thư mục được đề cập ở trên; nội dung của tệp là các mục bổ sung (mỗi mục một dòng) sẽ được thêm vào ``sys.path``. Các mục không tồn tại sẽ không bao giờ được thêm vào ``sys.path``, và hệ thống không kiểm tra xem mục đó trỏ đến một thư mục thay vì một tệp. Không có mục nào được thêm vào ``sys.path`` quá một lần. Các dòng trống và các dòng bắt đầu bằng ``#`` sẽ được bỏ qua. Các dòng bắt đầu bằng ``import`` (theo sau là dấu cách hoặc tab) sẽ được thực thi.

.. note::

   Một dòng có thể thực thi trong tệp :file:`.pth` sẽ được chạy mỗi khi Python khởi động, bất kể một module cụ thể có thực sự được sử dụng hay không. Vì vậy, tác động của dòng này nên được giữ ở mức tối thiểu. Mục đích chính của các dòng có thể thực thi là giúp các module tương ứng có thể được import (tải các import hook của bên thứ ba, điều chỉnh :envvar:`PATH` v.v.). Mọi thao tác khởi tạo khác được cho là sẽ thực hiện khi module thực sự được import, nếu và khi điều đó xảy ra. Việc giới hạn một đoạn mã chỉ trong một dòng là biện pháp có chủ ý nhằm ngăn việc đặt bất cứ thứ gì phức tạp hơn vào đây.

.. versionchanged:: 3.13
   Các tệp :file:`.pth` hiện được giải mã trước bằng UTF-8 rồi bằng
   :term:`locale encoding` nếu việc đó thất bại.

.. index::
   single: package
   triple: path; configuration; file

Ví dụ, giả sử ``sys.prefix`` và ``sys.exec_prefix`` được đặt thành
:file:`/usr/local`. Khi đó, thư viện Python X.Y được cài đặt trong
:file:`/usr/local/lib/python{X.Y}`.  Giả sử thư mục này có một thư mục con :file:`/usr/local/lib/python{X.Y}/site-packages` với ba thư mục con cấp dưới là :file:`foo`, :file:`bar` và :file:`spam`, cùng hai tệp cấu hình đường dẫn là :file:`foo.pth` và :file:`bar.pth`.  Giả sử
:file:`foo.pth` chứa nội dung sau::

   # cấu hình package foo

   foo
   bar
   bletch

và :file:`bar.pth` chứa::

   # cấu hình package bar

   bar

Sau đó, các thư mục dành riêng cho từng phiên bản sau đây được thêm vào ``sys.path`` theo thứ tự này::

   /usr/local/lib/pythonX.Y/site-packages/bar
   /usr/local/lib/pythonX.Y/site-packages/foo

Lưu ý rằng :file:`bletch` bị bỏ qua vì không tồn tại; thư mục :file:`bar` đứng trước thư mục :file:`foo` vì :file:`bar.pth` được sắp xếp theo thứ tự bảng chữ cái trước :file:`foo.pth`; và :file:`spam` bị bỏ qua vì không được đề cập trong cả hai tệp cấu hình đường dẫn.

:mod:`!sitecustomize`
---------------------

.. module:: sitecustomize

Sau các thao tác điều chỉnh đường dẫn này, hệ thống sẽ cố gắng nhập một module có tên
:mod:`!sitecustomize`, có thể thực hiện các tùy chỉnh tùy ý dành riêng cho từng hệ thống. Module này thường được quản trị viên hệ thống tạo trong thư mục site-packages. Nếu thao tác nhập này thất bại với :exc:`ImportError` hoặc một exception lớp con của nó, và thuộc tính :attr:`~ImportError.name` của exception bằng ``'sitecustomize'``, lỗi sẽ được âm thầm bỏ qua. Nếu Python được khởi động mà không có các luồng đầu ra, như với :file:`pythonw.exe` trên Windows (được dùng theo mặc định để khởi động IDLE), đầu ra do :mod:`!sitecustomize` tạo ra sẽ bị bỏ qua. Bất kỳ exception nào khác đều khiến tiến trình thất bại trong im lặng và có thể khó hiểu.

:mod:`!usercustomize`
---------------------

.. module:: usercustomize

Sau đó, hệ thống sẽ cố gắng nhập một module có tên :mod:`!usercustomize`, có thể thực hiện các tùy chỉnh tùy ý dành riêng cho người dùng, nếu
:data:`~site.ENABLE_USER_SITE` là true. Tệp này предназначены để được tạo trong thư mục site-packages của người dùng (xem bên dưới), vốn là một phần của ``sys.path`` trừ khi bị vô hiệu hóa bởi :option:`-s`. Nếu thao tác nhập này thất bại với :exc:`ImportError` hoặc một exception lớp con của nó, và thuộc tính :attr:`~ImportError.name` của exception bằng ``'usercustomize'``, lỗi sẽ được âm thầm bỏ qua.

Lưu ý rằng trên một số hệ thống không phải Unix, ``sys.prefix`` và ``sys.exec_prefix`` là các giá trị rỗng, nên các thao tác điều chỉnh đường dẫn sẽ được bỏ qua; tuy nhiên, hệ thống vẫn cố gắng nhập
:mod:`sitecustomize` và :mod:`!usercustomize`.

.. currentmodule:: site

.. _rlcompleter-config:

Cấu hình Readline
-----------------

Trên các hệ thống hỗ trợ :mod:`readline`, module này cũng sẽ import và cấu hình module :mod:`rlcompleter`, nếu Python được khởi động ở
:ref:`chế độ tương tác <tut-interactive>` và không có tùy chọn :option:`-S`. Hành vi mặc định là bật tính năng hoàn tất bằng phím Tab và sử dụng
:file:`~/.python_history` làm tệp lưu lịch sử. Để tắt tính năng này, hãy xóa (hoặc ghi đè) thuộc tính :data:`sys.__interactivehook__` trong
:mod:`sitecustomize` hoặc module :mod:`usercustomize` của bạn, hoặc trong
tệp :envvar:`PYTHONSTARTUP`.

.. versionchanged:: 3.4
   Việc kích hoạt rlcompleter và history được thực hiện tự động.


Nội dung module
---------------

.. data:: PREFIXES

   Danh sách các tiền tố cho các thư mục site-packages.


.. data:: ENABLE_USER_SITE

   Cờ cho biết trạng thái của thư mục site-packages của người dùng.  ``True`` có nghĩa là thư mục này được bật và đã được thêm vào ``sys.path``.  ``False`` có nghĩa là thư mục này đã bị tắt theo yêu cầu của người dùng (với :option:`-s` hoặc
   :envvar:`PYTHONNOUSERSITE`).  ``None`` có nghĩa là thư mục này bị tắt vì lý do bảo mật (id người dùng hoặc nhóm không khớp với effective id) hoặc bởi quản trị viên.


.. data:: USER_SITE

   Đường dẫn đến site-packages của người dùng cho Python đang chạy.  Có thể là ``None`` nếu
   :func:`getusersitepackages` vẫn chưa được gọi.  Giá trị mặc định là
   :file:`~/.local/lib/python{X.Y}[t]/site-packages` đối với các bản build UNIX và macOS không phải framework, :file:`~/Library/Python/{X.Y}/lib/python/site-packages` đối với các bản build macOS framework và :file:`{%APPDATA%}\\Python\\Python{XY}\\site-packages` trên Windows.  "t" tùy chọn cho biết đây là bản build free-threaded.  Đây là một thư mục site, nghĩa là các tệp :file:`.pth` trong đó sẽ được xử lý.


.. data:: USER_BASE

   Đường dẫn đến thư mục cơ sở của site-packages của người dùng.  Có thể là ``None`` nếu
   :func:`getuserbase` vẫn chưa được gọi. Giá trị mặc định là
   :file:`~/.local` cho các bản build UNIX và macOS không dùng framework,
   :file:`~/Library/Python/{X.Y}` cho các bản build macOS dùng framework, và
   :file:`{%APPDATA%}\\Python` cho Windows. Giá trị này được dùng để tính các thư mục cài đặt cho script, tệp dữ liệu, module Python, v.v. theo :ref:`chế độ cài đặt cho người dùng <sysconfig-user-scheme>`. Xem thêm :envvar:`PYTHONUSERBASE`.


.. function:: main()

   Thêm tất cả các thư mục dành riêng cho site tiêu chuẩn vào đường dẫn tìm kiếm module. Hàm này được tự động gọi khi module này được import, trừ khi trình thông dịch Python được khởi động với cờ :option:`-S`.

   .. versionchanged:: 3.3
      Trước đây, hàm này luôn được gọi.


.. function:: addsitedir(sitedir, known_paths=None)

   Thêm một thư mục vào sys.path và xử lý các tệp :file:`.pth` của thư mục đó. Thường được dùng trong :mod:`sitecustomize` hoặc :mod:`usercustomize` (xem ở trên).


.. function:: getsitepackages(prefixes=None)

   Trả về một danh sách chứa tất cả các thư mục site-packages toàn cục.

   Đối với mỗi thư mục được cung cấp trong *prefixes* (hoặc :data:`PREFIXES` nếu *prefixes* là ``None``), hàm này sẽ tính thư mục site-packages con của thư mục đó tùy theo môi trường hệ thống, rồi trả về một danh sách các đường dẫn đầy đủ, không kiểm tra xem các đường dẫn đó có tồn tại hay không.

   .. versionadded:: 3.2

   .. versionchanged:: 3.3
      Đã thêm tham số *prefixes* tùy chọn.


.. function:: getuserbase()

   Trả về đường dẫn của thư mục cơ sở của người dùng, :data:`USER_BASE`.  Nếu thư mục này chưa được khởi tạo, hàm này cũng sẽ thiết lập nó, tuân theo
   :envvar:`PYTHONUSERBASE`.

   .. versionadded:: 3.2


.. function:: getusersitepackages()

   Trả về đường dẫn của thư mục site-packages dành riêng cho người dùng,
   :data:`USER_SITE`.  Nếu thư mục này chưa được khởi tạo, hàm này cũng sẽ thiết lập nó, tuân theo :data:`USER_BASE`.  Để xác định xem site-packages dành riêng cho người dùng đã được thêm vào ``sys.path`` hay chưa, nên sử dụng :data:`ENABLE_USER_SITE`.

   .. versionadded:: 3.2


.. _site-commandline:

Giao diện dòng lệnh
-------------------

.. program:: site

Mô-đun :mod:`!site` cũng cung cấp một cách để lấy các thư mục của người dùng từ dòng lệnh:

.. code-block:: shell-session

   $ python -m site --user-site
   /home/user/.local/lib/python3.11/site-packages

Nếu được gọi mà không có đối số, mô-đun sẽ in nội dung của
:data:`sys.path` ra đầu ra tiêu chuẩn, theo sau là giá trị của
:data:`USER_BASE` và cho biết thư mục đó có tồn tại hay không, sau đó thực hiện tương tự với
:data:`USER_SITE`, và cuối cùng là giá trị của :data:`ENABLE_USER_SITE`.

.. option:: --user-base

   In đường dẫn đến thư mục cơ sở của người dùng.

.. option:: --user-site

   In đường dẫn đến thư mục site-packages của người dùng.

Nếu cung cấp cả hai tùy chọn, thư mục user base và user site sẽ được in ra (luôn theo thứ tự này), phân tách bằng :data:`os.pathsep`.

Nếu cung cấp bất kỳ tùy chọn nào, script sẽ thoát với một trong các giá trị sau: ``0`` nếu thư mục site-packages của người dùng được bật, ``1`` nếu bị người dùng tắt, ``2`` nếu bị tắt vì lý do bảo mật hoặc bởi quản trị viên, và giá trị lớn hơn 2 nếu xảy ra lỗi.

.. seealso::

   * :pep:`370` -- Thư mục site-packages theo người dùng
   * :ref:`sys-path-init` -- Quá trình khởi tạo :data:`sys.path`.

