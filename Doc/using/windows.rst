.. highlight:: none

.. _python.org/downloads: https://www.python.org/downloads/

.. _Microsoft Store app: https://apps.microsoft.com/detail/9NQ7512CXL7T

.. _legacy launcher: https://www.python.org/ftp/python/3.14.0/win32/launcher.msi

.. _using-on-windows:

***************************
Sử dụng Python trên Windows
***************************

.. sectionauthor:: Steve Dower <steve.dower@python.org>

Tài liệu này nhằm cung cấp tổng quan về những hành vi đặc thù của Windows mà bạn nên biết khi sử dụng Python trên Microsoft Windows.

Không giống hầu hết các hệ thống và dịch vụ Unix, Windows không bao gồm bản cài đặt Python được hệ thống hỗ trợ. Thay vào đó, Python có thể được cung cấp bởi nhiều nhà phân phối, trong đó có chính nhóm CPython. Tuy nhiên, mỗi bản phân phối Python sẽ có những ưu điểm và nhược điểm riêng; nhìn chung, tính nhất quán với các công cụ khác mà bạn đang sử dụng thường là một lợi ích đáng cân nhắc. Trước khi quyết định thực hiện theo quy trình được mô tả ở đây, chúng tôi khuyến nghị bạn kiểm tra các công cụ hiện có để xem chúng có thể cung cấp Python trực tiếp hay không.

Để tải Python từ nhóm CPython, hãy sử dụng Python Install Manager. Đây là một công cụ độc lập giúp Python khả dụng dưới dạng các lệnh toàn cục trên máy Windows của bạn, tích hợp với hệ thống và hỗ trợ cập nhật theo thời gian. Bạn có thể tải Python Install Manager từ `python.org/downloads`_ hoặc thông qua `ứng dụng Microsoft Store <Microsoft Store app_>`_.

Sau khi cài đặt Python Install Manager, bạn có thể sử dụng lệnh toàn cục ``python`` từ bất kỳ terminal nào để khởi chạy phiên bản Python mới nhất hiện tại. Phiên bản này có thể thay đổi theo thời gian khi bạn thêm hoặc xóa các phiên bản khác nhau, và lệnh ``py list`` sẽ hiển thị phiên bản hiện tại.

Nhìn chung, chúng tôi khuyến nghị bạn tạo một :ref:`môi trường ảo <tut-venv>` cho mỗi dự án và chạy ``<env>\Scripts\Activate`` trong terminal để sử dụng môi trường đó. Điều này giúp cô lập các dự án, duy trì tính nhất quán theo thời gian và đảm bảo rằng các lệnh bổ sung do các package thêm vào cũng khả dụng trong phiên làm việc của bạn. Tạo một môi trường ảo bằng ``python -m venv <env path>``.

Nếu các lệnh ``python`` hoặc ``py`` dường như không hoạt động, hãy xem các
Xem phần :ref:`Khắc phục sự cố <pymanager-troubleshoot>` bên dưới. Đôi khi cần thực hiện thêm một số bước thủ công để cấu hình PC của bạn.

Ngoài việc sử dụng Python install manager, bạn cũng có thể tải Python dưới dạng các gói NuGet. Xem :ref:`windows-nuget` bên dưới để biết thêm thông tin về các gói này.

Các bản phân phối nhúng là những gói Python tối giản, phù hợp để nhúng vào các ứng dụng lớn hơn. Bạn có thể cài đặt chúng bằng Python install manager. Xem :ref:`windows-embeddable` bên dưới để biết thêm thông tin về các gói này.


.. _pymanager:
.. _windows-store:
.. _setting-envvars:
.. _windows-path-mod:
.. _launcher:

Python install manager
======================

Cài đặt
-------

Bạn có thể cài đặt Python install manager từ ứng dụng `Microsoft Store <Microsoft Store app_>`_ hoặc tải xuống và cài đặt từ `python.org/downloads`_. Hai phiên bản này giống hệt nhau.

Để cài đặt thông qua Store, chỉ cần nhấp vào "Install". Sau khi hoàn tất, hãy mở terminal và nhập ``python`` để bắt đầu.

Để cài đặt tệp đã tải xuống từ python.org, hãy nhấp đúp và chọn "Install", hoặc chạy ``Add-AppxPackage <path to MSIX>`` trong Windows Powershell.

Sau khi cài đặt, các lệnh ``python``, ``py`` và ``pymanager`` sẽ khả dụng. Nếu bạn đã cài đặt Python trước đó hoặc đã sửa đổi biến :envvar:`PATH`, bạn có thể cần xóa các bản cài đặt đó hoặc hoàn tác các sửa đổi. Xem :ref:`pymanager-troubleshoot` để được trợ giúp thêm về cách khắc phục các lệnh không hoạt động.

Khi cài đặt runtime lần đầu, bạn có thể sẽ được nhắc thêm một thư mục vào :envvar:`PATH`. Đây là tùy chọn nếu bạn muốn sử dụng lệnh ``py``, nhưng được cung cấp cho những người muốn có đầy đủ các bí danh (chẳng hạn như ``python3.14.exe``) khả dụng. Thư mục này sẽ là
:file:`%LocalAppData%\\Python\\bin` theo mặc định, nhưng quản trị viên có thể tùy chỉnh. Nhấp vào Start và tìm kiếm "Edit environment variables for your account" để mở trang cài đặt hệ thống và thêm đường dẫn.

Mỗi Python runtime bạn cài đặt sẽ có thư mục riêng dành cho các script. Bạn cũng cần thêm các thư mục này vào :envvar:`PATH` nếu muốn sử dụng chúng.

Python install manager sẽ được tự động cập nhật lên các bản phát hành mới. Điều này không ảnh hưởng đến bất kỳ Python runtime nào đã cài đặt. Việc gỡ cài đặt Python install manager không gỡ cài đặt bất kỳ Python runtime nào.

Nếu bạn không thể cài đặt MSIX trong môi trường của mình, chẳng hạn như khi bạn đang sử dụng phần mềm triển khai tự động không hỗ trợ định dạng này hoặc đang nhắm đến Windows Server 2019, vui lòng xem :ref:`pymanager-advancedinstall` bên dưới để biết thêm thông tin.


Cách sử dụng cơ bản
-------------------

Lệnh được khuyến nghị để khởi chạy Python là ``python``, lệnh này sẽ khởi chạy phiên bản được script đang chạy yêu cầu, một virtual environment đang hoạt động hoặc phiên bản mặc định đã cài đặt; phiên bản mặc định sẽ là bản phát hành ổn định mới nhất, trừ khi được cấu hình khác đi. Nếu không có phiên bản nào được yêu cầu cụ thể và hoàn toàn không có runtime nào được cài đặt, bản phát hành mới nhất hiện tại sẽ được tự động cài đặt.

Đối với mọi tình huống liên quan đến nhiều phiên bản runtime, lệnh được khuyến nghị là ``py``. Lệnh này có thể được sử dụng ở bất kỳ đâu thay cho ``python`` hoặc launcher ``py.exe`` cũ hơn. Theo mặc định, ``py`` hoạt động giống ``python``, nhưng cũng cho phép sử dụng các tùy chọn dòng lệnh để chọn một phiên bản cụ thể, cũng như các subcommand để quản lý việc cài đặt. Những nội dung này được trình bày chi tiết bên dưới.

Vì lệnh ``py`` có thể đã được phiên bản trước đó sử dụng, nên cũng có lệnh ``pymanager`` không gây nhầm lẫn. Các bản cài đặt có script dự định sử dụng Python install manager nên cân nhắc dùng ``pymanager``, do ít có khả năng xung đột với các bản cài đặt hiện có hơn. Điểm khác biệt duy nhất giữa hai lệnh là khi chạy mà không có đối số: ``py`` sẽ khởi chạy interpreter mặc định của bạn, còn ``pymanager`` sẽ hiển thị trợ giúp (``pymanager exec ...`` có hành vi tương đương với ``py ...``).

Mỗi lệnh trong số này cũng có một phiên bản chạy không hiển thị cửa sổ, giúp tránh tạo cửa sổ console. Các lệnh đó là ``pyw``, ``pythonw`` và ``pywmanager``. Ngoài ra còn có lệnh ``python3`` mô phỏng lệnh ``python``. Lệnh này nhằm phát hiện các trường hợp vô tình sử dụng lệnh POSIX thường dùng trên Windows, nhưng không предназначена để được sử dụng rộng rãi hoặc khuyến nghị.

Để khởi chạy runtime mặc định, hãy chạy ``python`` hoặc ``py`` cùng với các đối số bạn muốn truyền cho runtime (chẳng hạn như các tệp script hoặc module cần khởi chạy):

.. code::

   $> py
   ...
   $> python my-script.py
   ...
   $> py -m this
   ...

Có thể ghi đè runtime mặc định bằng biến môi trường :envvar:`PYTHON_MANAGER_DEFAULT` hoặc một tệp cấu hình. Xem :ref:`pymanager-config` để biết thông tin về các thiết lập cấu hình.

Để khởi chạy một runtime cụ thể, lệnh ``py`` chấp nhận tùy chọn ``-V:<TAG>``. Tùy chọn này phải được chỉ định trước mọi tùy chọn khác. Thẻ là một phần hoặc toàn bộ mã định danh của runtime; đối với các runtime do nhóm CPython cung cấp, thẻ có dạng phiên bản, có thể kèm theo nền tảng. Để đảm bảo tương thích, ``V:`` có thể được bỏ qua trong trường hợp thẻ đề cập đến một bản phát hành chính thức và bắt đầu bằng ``3``.

.. code::

   $> py -V:3.14 ...
   $> py -V:3-arm64 ...

Các runtime từ những nhà phân phối khác có thể yêu cầu phải bao gồm cả *công ty*. Giá trị này phải được phân tách khỏi thẻ bằng dấu gạch chéo (``/`` hoặc ``\``), và có thể được rút gọn thành bất kỳ tiền tố nào của giá trị đầy đủ. Việc chỉ định công ty là tùy chọn khi công ty là ``PythonCore``, còn việc chỉ định thẻ là tùy chọn (nhưng không được bỏ dấu gạch chéo) khi bạn muốn bản phát hành mới nhất từ một công ty cụ thể.

.. code::

   $> py -V:Distributor\1.0 ...
   $> py -V:distrib/ ...

Nếu không chỉ định phiên bản nhưng có truyền tệp script, script sẽ được kiểm tra để tìm *dòng shebang*. Đây là một định dạng đặc biệt cho dòng đầu tiên trong tệp, cho phép ghi đè lệnh. Xem :ref:`pymanager-shebang` để biết thêm thông tin. Khi không có dòng shebang hoặc không thể phân giải dòng này, script sẽ được khởi chạy bằng runtime mặc định.

Nếu bạn đang chạy trong một môi trường ảo đang hoạt động, chưa yêu cầu một phiên bản cụ thể và không có dòng shebang, runtime mặc định sẽ là môi trường ảo đó. Trong trường hợp này, lệnh ``python`` có thể đã được ghi đè từ trước nên không có kiểm tra nào trong số này được thực hiện. Tuy nhiên, hành vi này đảm bảo rằng lệnh ``py`` có thể được sử dụng thay thế cho nhau.

Khi chưa cài đặt runtime nào, mọi lệnh khởi chạy sẽ cố gắng cài đặt phiên bản được yêu cầu rồi khởi chạy phiên bản đó. Tuy nhiên, sau khi đã cài đặt bất kỳ phiên bản nào, chỉ các lệnh ``py exec ...`` và ``pymanager exec ...`` mới cài đặt nếu không tìm thấy phiên bản được yêu cầu. Các dạng lệnh khác sẽ hiển thị lỗi và hướng dẫn bạn sử dụng ``py install`` trước.


Trợ giúp về lệnh
----------------

Lệnh ``py help`` sẽ hiển thị danh sách đầy đủ các lệnh được hỗ trợ cùng với các tùy chọn của chúng. Có thể truyền tùy chọn ``-?`` cho bất kỳ lệnh nào để hiển thị trợ giúp của lệnh đó, hoặc truyền tên lệnh cho ``py help``.

.. code::

   $> py help
   $> py help install
   $> py install /?


Tất cả các lệnh đều hỗ trợ một số tùy chọn chung, được hiển thị bằng ``py help``. Các tùy chọn này phải được chỉ định sau mọi subcommand. Việc chỉ định ``-v`` hoặc ``--verbose`` sẽ tăng lượng đầu ra được hiển thị, còn ``-vv`` sẽ tăng thêm nữa để phục vụ mục đích gỡ lỗi. Truyền ``-q`` hoặc ``--quiet`` sẽ giảm lượng đầu ra, còn ``-qq`` sẽ giảm thêm nữa.

Tùy chọn ``--config=<PATH>`` cho phép chỉ định một tệp cấu hình để ghi đè nhiều thiết lập cùng lúc. Xem :ref:`pymanager-config` bên dưới để biết thêm thông tin về các tệp này.


Liệt kê các runtime
-------------------

.. code::

   $> py list [-f=|--format=<FMT>] [-1|--one] [--online|-s=|--source=<URL>] [<TAG>...]

Có thể xem danh sách các runtime đã cài đặt bằng ``py list``. Có thể thêm bộ lọc dưới dạng một hoặc nhiều tag (có hoặc không có bộ chỉ định công ty), và mỗi tag có thể bao gồm tiền tố ``<``, ``<=``, ``>=`` hoặc ``>`` để giới hạn trong một khoảng.

Có nhiều định dạng được hỗ trợ và có thể truyền dưới dạng tùy chọn ``--format=<FMT>`` hoặc ``-f <FMT>``. Các định dạng bao gồm ``table`` (bảng dễ đọc đối với người dùng), ``csv`` (bảng phân tách bằng dấu phẩy), ``json`` (một JSON blob duy nhất), ``jsonl`` (mỗi kết quả một JSON blob), ``exe`` (chỉ đường dẫn đến tệp thực thi), ``prefix`` (chỉ đường dẫn prefix).

Tùy chọn ``--one`` hoặc ``-1`` chỉ hiển thị một kết quả duy nhất. Nếu runtime mặc định được bao gồm, đó sẽ là runtime được chọn. Nếu không, kết quả "tốt nhất" sẽ được hiển thị ("tốt nhất" được cố ý định nghĩa khá mơ hồ, nhưng thường sẽ là phiên bản mới nhất). Kết quả được hiển thị bởi ``py list --one <TAG>`` sẽ khớp với runtime được khởi chạy bởi ``py -V:<TAG>``.

Tùy chọn ``--only-managed`` loại trừ các kết quả không được cài đặt bởi Python install manager. Điều này hữu ích khi xác định runtime nào có thể được cập nhật hoặc gỡ cài đặt thông qua lệnh ``py``.

Tùy chọn ``--online`` là dạng viết tắt để truyền ``--source=<URL>`` với source mặc định. Việc truyền một trong hai tùy chọn này sẽ tìm kiếm index trực tuyến các runtime có thể cài đặt. Kết quả do ``py list --online --one <TAG>`` hiển thị sẽ khớp với runtime được cài đặt bởi ``py install <TAG>``.

.. code::

   $> py list --online 3.14

Để tương thích với launcher cũ, các lệnh ``--list``, ``--list-paths``, ``-0`` và ``-0p`` (ví dụ: ``py -0p``) vẫn được giữ lại. Chúng không cho phép thêm tùy chọn và sẽ tạo đầu ra theo định dạng cũ.


Cài đặt runtime
---------------

.. code::

   $> py install [-s=|--source=<URL>] [-f|--force] [-u|--update] [--dry-run] [<TAG>...]

Có thể thêm các phiên bản runtime mới bằng ``py install``. Có thể chỉ định một hoặc nhiều tag, và có thể sử dụng tag đặc biệt ``default`` để chọn phiên bản mặc định. Không hỗ trợ range khi cài đặt.

Tùy chọn ``--source=<URL>`` cho phép ghi đè index trực tuyến được sử dụng để lấy runtime. Tùy chọn này có thể được dùng với index ngoại tuyến, như minh họa trong
:ref:`pymanager-offline`.

Việc truyền ``--force`` sẽ bỏ qua mọi tệp đã lưu trong cache và xóa mọi bản cài đặt hiện có để thay thế bằng bản được chỉ định.

Việc truyền ``--update`` sẽ thay thế các bản cài đặt hiện có nếu phiên bản mới hơn. Nếu không, các bản cài đặt đó sẽ được giữ nguyên. Nếu không cung cấp tag nào cùng với ``--update``, tất cả bản cài đặt do Python install manager quản lý sẽ được cập nhật nếu có phiên bản mới hơn. Việc cập nhật sẽ xóa mọi sửa đổi đã thực hiện đối với bản cài đặt, bao gồm các package được cài đặt global, nhưng các virtual environment vẫn sẽ tiếp tục hoạt động.

Việc truyền ``--dry-run`` sẽ tạo đầu ra và nhật ký, nhưng không sửa đổi bất kỳ bản cài đặt nào.

Việc truyền ``--refresh`` sẽ cập nhật tất cả đăng ký cho các runtime đã cài đặt. Thao tác này sẽ tạo lại các shortcut trong menu Start, khóa registry và các alias toàn cục (chẳng hạn như ``python3.14.exe`` hoặc cho bất kỳ script nào đã cài đặt). Các mục này được tự động làm mới khi cài đặt bất kỳ runtime nào, nhưng có thể cần được làm mới thủ công sau khi cài đặt các package.

Ngoài các tùy chọn trên, tùy chọn ``--target`` sẽ giải nén runtime vào thư mục được chỉ định thay vì thực hiện cài đặt thông thường. Tùy chọn này hữu ích khi nhúng runtime vào các ứng dụng lớn hơn. Không giống như cài đặt thông thường, ``py`` sẽ không nhận biết runtime đã giải nén và sẽ không tạo shortcut trong menu Start hay các shortcut khác. Để khởi chạy runtime, hãy thực thi trực tiếp tệp thực thi chính (thường là ``python.exe``) trong thư mục đích.

.. code::

   $> py install ... [-t=|--target=<PATH>] <TAG>

Lệnh ``py exec`` sẽ cài đặt runtime được yêu cầu nếu runtime đó chưa có. Điều này được kiểm soát bởi cấu hình ``automatic_install`` (:envvar:`PYTHON_MANAGER_AUTOMATIC_INSTALL`) và được bật theo mặc định. Nếu hoàn toàn không có runtime nào, tất cả lệnh khởi chạy sẽ tự động cài đặt nếu tùy chọn cấu hình cho phép. Điều này nhằm đảm bảo trải nghiệm tốt cho người dùng mới, nhưng nhìn chung không nên dựa vào cơ chế này thay cho lệnh ``py exec`` hoặc các lệnh cài đặt rõ ràng.


.. _pymanager-offline:

Cài đặt ngoại tuyến
-------------------

Để thực hiện cài đặt Python ngoại tuyến, trước tiên bạn cần tạo một index ngoại tuyến trên máy có quyền truy cập mạng.

.. code::

   $> py install --download=<PATH> ... <TAG>...

Tùy chọn ``--download=<PATH>`` sẽ tải xuống các package cho những tag được liệt kê và tạo một thư mục chứa chúng cùng với tệp ``index.json`` phù hợp để cài đặt sau. Có thể di chuyển toàn bộ thư mục này sang máy ngoại tuyến và sử dụng để cài đặt một hoặc nhiều runtime đi kèm:

.. code::

   $> py install --source="<PATH>\index.json" <TAG>...

Trình quản lý cài đặt Python có thể được cài đặt bằng cách tải xuống trình cài đặt rồi chuyển trình cài đặt đó sang một máy khác trước khi cài đặt.

Ngoài ra, bạn có thể chỉ cần chuyển các tệp ZIP trong thư mục chỉ mục ngoại tuyến sang một máy khác rồi giải nén. Cách này sẽ không đăng ký bản cài đặt theo bất kỳ cách nào, vì vậy bạn phải khởi chạy bằng cách tham chiếu trực tiếp đến các tệp thực thi trong thư mục đã giải nén, nhưng đôi khi đây là cách phù hợp hơn trong trường hợp không thể hoặc không thuận tiện để cài đặt trình quản lý cài đặt Python.

Bằng cách này, bạn có thể cài đặt và quản lý các runtime Python trên một máy không có quyền truy cập internet.


Gỡ cài đặt runtime
------------------

.. code::

   $> py uninstall [-y|--yes] <TAG>...

Có thể xóa runtime bằng lệnh ``py uninstall``. Phải chỉ định một hoặc nhiều thẻ. Tính năng này không hỗ trợ phạm vi.

Tùy chọn ``--yes`` bỏ qua lời nhắc xác nhận trước khi gỡ cài đặt.

Thay vì truyền từng thẻ riêng lẻ, bạn có thể chỉ định tùy chọn ``--purge``. Tùy chọn này sẽ xóa tất cả runtime do trình quản lý cài đặt Python quản lý, bao gồm cả việc dọn dẹp Start menu, registry và mọi bộ nhớ đệm tải xuống. Các runtime không được cài đặt bởi trình quản lý cài đặt Python sẽ không bị ảnh hưởng, và các tệp cấu hình được tạo thủ công cũng vậy.

.. code::

   $> py uninstall [-y|--yes] --purge

Python install manager có thể được gỡ cài đặt thông qua trang cài đặt "Installed apps" của Windows. Thao tác này không xóa bất kỳ runtime nào và bạn vẫn có thể sử dụng chúng, mặc dù các lệnh ``python`` và ``py`` trên toàn hệ thống sẽ bị xóa. Cài đặt lại Python install manager sẽ cho phép bạn quản lý các runtime này lần nữa. Để dọn dẹp hoàn toàn tất cả runtime Python, hãy chạy với ``--purge`` trước khi gỡ cài đặt Python install manager.

.. _pymanager-config:

Cấu hình
--------

Python install manager được cấu hình bằng hệ thống phân cấp gồm các tệp cấu hình, biến môi trường, tùy chọn dòng lệnh và cài đặt registry. Nhìn chung, tệp cấu hình có thể cấu hình mọi thứ, bao gồm cả vị trí của các tệp cấu hình khác, trong khi cài đặt registry chỉ dành cho quản trị viên và sẽ ghi đè các tệp cấu hình. Tùy chọn dòng lệnh ghi đè mọi cài đặt khác, nhưng không phải tùy chọn nào cũng khả dụng.

Phần này sẽ mô tả các giá trị mặc định, nhưng hãy lưu ý rằng các bản cài đặt đã được sửa đổi hoặc ghi đè có thể phân giải cài đặt theo cách khác.

Quản trị viên có thể cấu hình một tệp cấu hình toàn cục và tệp này sẽ được đọc đầu tiên. Tệp cấu hình người dùng được lưu tại
:file:`%AppData%\\Python\\pymanager.json` (lưu ý rằng vị trí này nằm dưới ``Roaming``, không phải ``Local``) và được đọc tiếp theo, ghi đè mọi cài đặt từ các tệp trước đó. Có thể chỉ định thêm một tệp cấu hình dưới dạng biến môi trường ``PYTHON_MANAGER_CONFIG`` hoặc tùy chọn dòng lệnh ``--config`` (nhưng không thể dùng cả hai). Các vị trí này có thể được sửa đổi bằng các tùy chọn tùy chỉnh dành cho quản trị viên được liệt kê ở phần sau.

Các cài đặt sau đây là những cài đặt được xem là có khả năng được sửa đổi trong quá trình sử dụng thông thường. Các phần sau liệt kê những cài đặt dành cho tùy chỉnh của quản trị viên.

.. Sphinx bug with text writer; remove widths & caption temporarily
.. :widths: 2, 2, 4

.. rubric:: Các tùy chọn cấu hình tiêu chuẩn

.. list-table::
   :header-rows: 1

   * - Khóa cấu hình
     - Biến môi trường
     - Mô tả

   * - ``default_tag``
     - .. envvar:: PYTHON_MANAGER_DEFAULT
     - Phiên bản mặc định ưu tiên để khởi chạy hoặc cài đặt. Theo mặc định, phiên bản này được hiểu là phiên bản gần đây nhất không phải bản phát hành thử nghiệm từ nhóm CPython.

   * - ``default_platform``
     - ``PYTHON_MANAGER_DEFAULT_PLATFORM``
     - Nền tảng mặc định ưu tiên để khởi chạy hoặc cài đặt. Nền tảng này được xem như hậu tố của thẻ đã chỉ định, sao cho ``py -V:3.14`` sẽ ưu tiên cài đặt cho ``3.14-64`` nếu tồn tại (và ``default_platform`` là ``-64``), nhưng sẽ sử dụng ``3.14`` nếu không có bản cài đặt được gắn thẻ.

   * - ``logs_dir``
     - ``PYTHON_MANAGER_LOGS``
     - Vị trí ghi các tệp nhật ký. Theo mặc định, :file:`%TEMP%`.

   * - ``automatic_install``
     - .. envvar:: PYTHON_MANAGER_AUTOMATIC_INSTALL
     - Đặt thành True để cho phép tự động cài đặt khi sử dụng ``py exec`` để khởi chạy (hoặc ``py`` khi chưa cài đặt runtime nào). Các lệnh khác sẽ không tự động cài đặt, bất kể cài đặt này. Theo mặc định, true.

   * - ``include_unmanaged``
     - ``PYTHON_MANAGER_INCLUDE_UNMANAGED``
     - Đặt thành True để cho phép liệt kê và khởi chạy các runtime không được Python install manager cài đặt, hoặc false để loại trừ chúng. Theo mặc định, true.

   * - ``shebang_can_run_anything``
     - ``PYTHON_MANAGER_SHEBANG_CAN_RUN_ANYTHING``
     - Đặt thành True để cho phép shebang trong các tệp ``.py`` khởi chạy các ứng dụng không phải runtime Python, hoặc false để ngăn việc này. Theo mặc định, true.

   * - ``shebang_templates``
     - (không có)
     - Ánh xạ từ mẫu dòng shebang đến lệnh thay thế, chẳng hạn như ``py -V:<tag>`` hoặc một chuỗi thay thế. Xem :ref:`pymanager-shebang` để biết thêm chi tiết.

   * - ``log_level``
     - ``PYMANAGER_VERBOSE``, ``PYMANAGER_DEBUG``
     - Đặt mức mặc định của đầu ra (0-50). Mặc định là 20. Các giá trị thấp hơn tạo ra nhiều đầu ra hơn. Các biến môi trường có kiểu boolean và có thể tạo thêm đầu ra trong quá trình khởi động, nhưng đầu ra này sẽ bị các cấu hình khác loại bỏ sau đó.

   * - ``confirm``
     - ``PYTHON_MANAGER_CONFIRM``
     - Đặt là true để xác nhận một số thao tác trước khi thực hiện (chẳng hạn như gỡ cài đặt), hoặc false để bỏ qua bước xác nhận. Mặc định là true.

   * - ``install.source``
     - ``PYTHON_MANAGER_SOURCE_URL``
     - Ghi đè index feed dùng để nhận các gói cài đặt mới.

   * - ``install.enable_entrypoints``
     - (không có)
     - Đặt là true để tạo các lệnh toàn cục cho những package đã cài đặt (chẳng hạn như ``pip.exe``). Các lệnh này do chính các package định nghĩa. Nếu đặt là false, chỉ trình thông dịch Python được tạo các lệnh toàn cục. Mặc định là true. Bạn nên chạy ``py install --refresh`` sau khi thay đổi cài đặt này.

   * - ``list.format``
     - ``PYTHON_MANAGER_LIST_FORMAT``
     - Chỉ định định dạng mặc định được sử dụng bởi lệnh ``py list``. Mặc định là ``table``.

   * - ``install_dir``
     - (không có)
     - Chỉ định thư mục gốc nơi các runtime sẽ được cài đặt. Nếu thay đổi cài đặt này, các runtime đã cài đặt trước đó sẽ không thể sử dụng được trừ khi bạn di chuyển chúng đến vị trí mới.

   * - ``global_dir``
     - (không có)
     - Chỉ định thư mục nơi các lệnh toàn cục (chẳng hạn như ``python3.14.exe`` và ``pip.exe``) được lưu trữ. Thư mục này nên được thêm vào :envvar:`PATH` để các lệnh có thể sử dụng được từ terminal của bạn.

   * - ``download_dir``
     - (không có)
     - Chỉ định thư mục nơi các tệp đã tải xuống được lưu trữ. Đây là bộ nhớ đệm tạm thời và bạn có thể dọn dẹp thư mục này định kỳ.


Tên có dấu chấm nên được lồng bên trong các đối tượng JSON; ví dụ: ``list.format`` sẽ được chỉ định là ``{"list": {"format": "table"}}``.

.. _pymanager-shebang:

Các dòng shebang
----------------

Nếu dòng đầu tiên của tệp script bắt đầu bằng ``#!``, dòng đó được gọi là dòng "shebang". Linux và các hệ điều hành tương tự Unix có hỗ trợ nguyên bản cho những dòng này, và chúng thường được dùng trên các hệ thống đó để cho biết cách thực thi một script. Các lệnh ``python`` và ``py`` cho phép sử dụng các tính năng tương tự với các script Python trên Windows.

Để cho phép các dòng shebang trong script Python có thể chuyển đổi giữa Unix và Windows, một số lệnh 'ảo' được hỗ trợ nhằm chỉ định interpreter cần sử dụng. Các lệnh ảo được hỗ trợ là:

* ``/usr/bin/env <ALIAS>``
* ``/usr/bin/env -S <ALIAS>``
* ``/usr/bin/<ALIAS>``
* ``/usr/local/bin/<ALIAS>``
* ``<ALIAS>``

Ví dụ: nếu dòng đầu tiên trong script của bạn bắt đầu bằng

.. code-block:: sh

  #! /usr/bin/python

Python mặc định hoặc virtual environment đang hoạt động sẽ được tìm thấy và sử dụng. Vì nhiều script Python được viết để hoạt động trên Unix đã có sẵn dòng này, bạn có thể sử dụng các script đó với launcher mà không cần sửa đổi. Nếu bạn đang viết một script mới trên Windows và hy vọng script đó sẽ hữu ích trên Unix, bạn nên sử dụng một trong các dòng shebang bắt đầu bằng ``/usr``.

Có thể thay thế ``<ALIAS>`` trong bất kỳ lệnh ảo nào ở trên bằng một alias từ runtime đã cài đặt. Nghĩa là, bất kỳ lệnh nào được tạo trong thư mục global aliases (mà bạn có thể đã thêm vào biến môi trường :envvar:`PATH`) đều có thể được sử dụng trong shebang, ngay cả khi lệnh đó không nằm trên :envvar:`PATH`. Điều này cho phép sử dụng các shebang như ``/usr/bin/python3.12`` để chọn một runtime cụ thể.

Nếu chưa cài đặt runtime nào hoặc tính năng cài đặt tự động được bật, runtime được yêu cầu sẽ được cài đặt nếu cần. Xem :ref:`pymanager-config` để biết thông tin về các thiết lập cấu hình.

Dạng dòng shebang ``/usr/bin/env`` cũng sẽ tìm kiếm các lệnh không nhận dạng được trong biến môi trường :envvar:`PATH`. Điều này tương ứng với hành vi của chương trình Unix ``env``, chương trình cũng thực hiện cùng một tìm kiếm nhưng ưu tiên khởi chạy các lệnh Python đã biết. Một cảnh báo có thể được hiển thị khi tìm kiếm các tệp thực thi tùy ý, và có thể tắt tính năng tìm kiếm này bằng tùy chọn cấu hình ``shebang_can_run_anything``.

Các dòng shebang không khớp với bất kỳ mẫu nào được xử lý dưới dạng đường dẫn tệp thực thi *Windows* tuyệt đối hoặc tương đối so với thư mục chứa tệp script. Đây là một tiện ích dành cho các script chỉ chạy trên Windows, chẳng hạn như các script do trình cài đặt tạo ra, vì hành vi này không tương thích với các shell kiểu Unix. Các đường dẫn này có thể được đặt trong dấu ngoặc kép và có thể bao gồm nhiều đối số; sau đó, đường dẫn đến script cùng mọi đối số bổ sung sẽ được nối vào. Có thể tắt chức năng này bằng tùy chọn cấu hình ``shebang_can_run_anything``.

Kể từ phiên bản 26.3 của Python install manager, bạn có thể thêm các mẫu shebang tùy chỉnh vào tệp cấu hình. Thêm đối tượng ``shebang_templates`` với một thành viên cho mỗi mẫu (chuỗi cần khớp) và lệnh cần sử dụng khi mẫu đó khớp. Hầu hết các lệnh nên là ``py -V:<tag>`` (hoặc ``pyw``) để khởi chạy một trong các runtime đã cài đặt. Dạng ``py -3.<version>`` cũng được cho phép, cũng như ``py`` đơn thuần để khởi chạy runtime mặc định. Không hỗ trợ đối số nào khác.

.. code:: json5

   {
       "shebang_templates": {
           "/usr/bin/python": "py",
           "/usr/bin/my_custom_python": "py -V:MyCustomPython/3"
       }
   }

Nếu lệnh thay thế không phải là ``py`` hoặc ``pyw``, lệnh đó sẽ được ghi trở lại vào shebang và quá trình xử lý thông thường sẽ tiếp tục. Nếu cho phép khởi chạy các tệp thực thi tùy ý, việc cung cấp đường dẫn đầy đủ sẽ cho phép bạn chuyển hướng từ Python sang bất kỳ tệp thực thi nào. Mẫu phải khớp với toàn bộ dòng (bỏ qua khoảng trắng ở đầu và cuối) hoặc khớp đến dấu cách đầu tiên trong dòng shebang.


.. note::

   Hành vi của shebang trong Python install manager hơi khác so với trình khởi chạy ``py.exe`` trước đây, và các tùy chọn cấu hình cũ không còn được áp dụng. Nếu bạn đặc biệt phụ thuộc vào hành vi hoặc cấu hình cũ, chúng tôi khuyến nghị cài đặt `legacy launcher <legacy launcher_>`_. Theo mặc định, lệnh ``py`` của legacy launcher sẽ ghi đè lệnh của PyManager, và bạn sẽ cần sử dụng các lệnh ``pymanager`` để cài đặt và gỡ cài đặt.

.. _Add-AppxPackage: https://learn.microsoft.com/powershell/module/appx/add-appxpackage

.. _Remove-AppxPackage: https://learn.microsoft.com/powershell/module/appx/remove-appxpackage

.. _Add-AppxProvisionedPackage: https://learn.microsoft.com/powershell/module/dism/add-appxprovisionedpackage

.. _PackageManager: https://learn.microsoft.com/uwp/api/windows.management.deployment.packagemanager

.. _pymanager-advancedinstall:

Cài đặt nâng cao
----------------

Trong những trường hợp không thể cài đặt MSIX, chẳng hạn như trên một số nền tảng phân phối quản trị cũ hơn, có một MSI trên trang tải xuống của python.org. MSI này không có giao diện người dùng và chỉ có thể thực hiện cài đặt cho toàn máy vào vị trí mặc định trong Program Files. MSI sẽ cố gắng sửa đổi biến môi trường hệ thống :envvar:`PATH` để bao gồm vị trí cài đặt này, nhưng hãy nhớ xác thực điều đó trên cấu hình của bạn.

.. note::

   Windows Server 2019 là phiên bản Windows duy nhất được CPython hỗ trợ nhưng không hỗ trợ MSIX. Đối với Windows Server 2019, bạn nên sử dụng MSI.

Lưu ý rằng gói MSI không đi kèm bất kỳ runtime nào, vì vậy không phù hợp để cài đặt trong môi trường ngoại tuyến nếu không đồng thời tạo chỉ mục cài đặt ngoại tuyến. Xem :ref:`pymanager-offline` và :ref:`pymanager-admin-config` để biết thông tin về cách xử lý các trường hợp này.

Các runtime được cài đặt bởi MSI được dùng chung với các runtime được cài đặt bởi MSIX và tất cả chỉ dành cho từng người dùng. Python install manager không hỗ trợ cài đặt runtime trên toàn máy. Để mô phỏng việc cài đặt trên toàn máy, bạn có thể chạy ``py install --target=<shared location>`` với quyền quản trị viên và thêm các thay đổi trên toàn hệ thống của riêng mình vào :envvar:`PATH`, registry hoặc Start menu.

Khi MSIX đã được cài đặt nhưng các lệnh không có trong biến môi trường :envvar:`PATH`, bạn có thể tìm thấy chúng tại
:file:`%LocalAppData%\\Microsoft\\WindowsApps\\PythonSoftwareFoundation.PythonManager_3847v3x7pw1km` hoặc
:file:`%LocalAppData%\\Microsoft\\WindowsApps\\PythonSoftwareFoundation.PythonManager_qbz5n2kfra8p0`, tùy thuộc vào việc gói được cài đặt từ python.org hay thông qua Windows Store. Không nên cố chạy trực tiếp tệp thực thi từ Program Files.

Để cài đặt Python install manager bằng lập trình, cách dễ nhất là sử dụng WinGet, công cụ được tích hợp trong tất cả các phiên bản Windows được hỗ trợ:

.. code-block:: powershell

   $> winget install 9NQ7512CXL7T -e --accept-package-agreements --disable-interactivity

   # Tùy chọn chạy trình kiểm tra cấu hình và chấp nhận mọi thay đổi
   $> py install --configure -y

Để tải xuống trình quản lý cài đặt Python và cài đặt trên một máy khác, lệnh WinGet sau đây sẽ tải các tệp cần thiết từ Store vào thư mục Downloads của bạn (thêm ``-d <location>`` để tùy chỉnh vị trí đầu ra). Lệnh này cũng tạo một tệp YAML có vẻ không cần thiết, vì MSIX đã tải xuống có thể được cài đặt bằng cách khởi chạy hoặc sử dụng các lệnh bên dưới.

.. code-block:: powershell

   $> winget download 9NQ7512CXL7T -e --skip-license --accept-package-agreements --accept-source-agreements

Để cài đặt hoặc gỡ cài đặt MSIX theo cách lập trình chỉ bằng PowerShell, bạn nên sử dụng các cmdlet PowerShell `Add-AppxPackage`_ và `Remove-AppxPackage`_:

.. code-block:: powershell

   $> Add-AppxPackage C:\Downloads\python-manager-25.0.msix
   ...
   $> Get-AppxPackage PythonSoftwareFoundation.PythonManager | Remove-AppxPackage

Có thể tải xuống và cài đặt bản phát hành mới nhất bằng Windows bằng cách truyền tệp AppInstaller vào lệnh Add-AppxPackage. Cách này cài đặt bằng MSIX trên python.org và chỉ được khuyến nghị trong trường hợp không thể cài đặt thông qua Store (theo cách tương tác hoặc bằng WinGet).

.. code-block:: powershell

   $> Add-AppxPackage -AppInstallerFile https://www.python.org/ftp/python/pymanager/pymanager.appinstaller

Các công cụ và API khác cũng có thể được sử dụng để cung cấp gói MSIX cho tất cả người dùng trên một máy, nhưng Python không xem đây là kịch bản được hỗ trợ. Chúng tôi đề xuất tìm hiểu cmdlet PowerShell `Add-AppxProvisionedPackage`_, lớp Windows gốc `PackageManager`_, hoặc tài liệu và dịch vụ hỗ trợ cho công cụ triển khai của bạn.

Bất kể phương thức cài đặt nào được sử dụng, người dùng vẫn cần cài đặt bản sao Python của riêng mình, vì không có cách nào kích hoạt các quá trình cài đặt đó nếu không phải là người dùng đã đăng nhập. Khi sử dụng MSIX, phiên bản Python mới nhất sẽ khả dụng để tất cả người dùng cài đặt mà không cần truy cập mạng.

Lưu ý rằng MSIX có thể tải xuống từ Store và từ trang web Python hơi khác nhau và không thể được cài đặt đồng thời. Khi có thể, chúng tôi đề xuất sử dụng các lệnh WinGet ở trên để tải gói từ Store nhằm giảm nguy cơ thiết lập các bản cài đặt xung đột. Không có hạn chế cấp phép nào đối với trình quản lý cài đặt Python ngăn việc sử dụng gói từ Store theo cách này.


.. _pymanager-admin-config:

Cấu hình quản trị
-----------------

Có một số tùy chọn có thể hữu ích để quản trị viên ghi đè cấu hình của trình quản lý cài đặt Python. Các tùy chọn này có thể được dùng để cung cấp bộ nhớ đệm cục bộ, vô hiệu hóa một số loại shortcut nhất định và ghi đè nội dung đi kèm. Bạn có thể đặt tất cả các tùy chọn cấu hình nêu trên cũng như các tùy chọn bên dưới.

Có thể ghi đè các tùy chọn cấu hình trong registry bằng cách đặt các giá trị bên dưới
:file:`HKEY_LOCAL_MACHINE\\Software\\Policies\\Python\\PyManager`, trong đó tên giá trị khớp với khóa cấu hình và kiểu giá trị là ``REG_SZ``. Lưu ý rằng bản thân khóa này có thể được tùy chỉnh, nhưng chỉ bằng cách sửa đổi tệp cấu hình cốt lõi được phân phối cùng trình quản lý cài đặt Python. Tuy nhiên, chúng tôi khuyến nghị chỉ sử dụng các giá trị registry để đặt ``base_config`` thành một tệp JSON chứa toàn bộ các giá trị ghi đè. Các giá trị ghi đè trong registry key sẽ thay thế mọi thiết lập đã được cấu hình khác, trong khi ``base_config`` cho phép người dùng tiếp tục sửa đổi các thiết lập mà họ có thể cần.

Lưu ý rằng hầu hết các thiết lập có biến môi trường hỗ trợ các biến đó vì thiết lập mặc định của chúng chỉ định biến. Nếu bạn ghi đè chúng, biến môi trường sẽ không còn hoạt động, trừ khi bạn ghi đè bằng một biến khác. Ví dụ: giá trị mặc định của ``confirm`` theo nghĩa đen là ``%PYTHON_MANAGER_CONFIRM%``, giá trị này sẽ phân giải biến tại thời điểm tải. Nếu bạn ghi đè giá trị thành ``yes``, biến môi trường sẽ không còn được sử dụng. Nếu bạn ghi đè giá trị thành ``%CONFIRM%``, thì biến môi trường đó sẽ được sử dụng thay thế.

Các thiết lập cấu hình là đường dẫn được diễn giải tương đối so với thư mục chứa tệp cấu hình đã chỉ định chúng.

.. Sphinx bug with text writer; remove widths & caption temporarily
.. :widths: 1, 4

.. rubric:: Tùy chọn cấu hình dành cho quản trị viên

.. list-table::
   :header-rows: 1

   * - Khóa cấu hình
     - Mô tả

   * - ``base_config``
     - Tệp cấu hình có mức ưu tiên cao nhất cần đọc. Lưu ý rằng chỉ tệp cấu hình tích hợp sẵn và Registry mới có thể sửa đổi thiết lập này.

   * - ``user_config``
     - Tệp cấu hình thứ hai cần đọc.

   * - ``additional_config``
     - Tệp cấu hình thứ ba cần đọc.

   * - ``registry_override_key``
     - Vị trí Registry cần kiểm tra để tìm các giá trị ghi đè. Lưu ý rằng chỉ tệp cấu hình tích hợp sẵn mới có thể sửa đổi thiết lập này.

   * - ``bundled_dir``
     - Thư mục chỉ đọc chứa các tệp được lưu trong bộ nhớ đệm cục bộ.

   * - ``install.fallback_source``
     - Đường dẫn hoặc URL đến chỉ mục cần tham khảo khi không thể truy cập chỉ mục chính.

   * - ``install.enable_shortcut_kinds``
     - Danh sách phân tách bằng dấu phẩy gồm các loại shortcut được phép (ví dụ: ``"pep514,start"``). Các shortcut được bật vẫn có thể bị vô hiệu hóa bởi ``disable_shortcut_kinds``.

   * - ``install.disable_shortcut_kinds``
     - Danh sách phân tách bằng dấu phẩy gồm các loại shortcut cần loại trừ (ví dụ: ``"pep514,start"``). Các shortcut bị vô hiệu hóa sẽ không được kích hoạt lại bởi ``enable_shortcut_kinds``.

   * - ``install.hard_link_entrypoints``
     - Đặt là True để sử dụng liên kết cứng cho các shortcut toàn cục nhằm tiết kiệm dung lượng đĩa. Nếu là false, thay vào đó, mỗi tệp thực thi của shortcut sẽ được sao chép. Sau khi thay đổi thiết lập này, bạn phải chạy ``py install --refresh --force`` để cập nhật các lệnh hiện có. Theo mặc định là true. Có thể cần tắt tùy chọn này để khắc phục sự cố hoặc trên các hệ thống gặp vấn đề với liên kết tệp.

   * - ``pep514_root``
     - Vị trí Registry để đọc và ghi các mục PEP 514. Theo mặc định là :file:`HKEY_CURRENT_USER\\Software\\Python`.

   * - ``start_folder``
     - Thư mục Start menu để ghi các shortcut vào. Theo mặc định là ``Python``. Đường dẫn này tương đối với thư mục Programs của người dùng.

   * - ``virtual_env``
     - Đường dẫn đến virtual environment đang hoạt động. Theo mặc định, đây là ``%VIRTUAL_ENV%``, nhưng có thể đặt thành rỗng để tắt tính năng phát hiện venv.

   * - ``shebang_can_run_anything_silently``
     - Đặt là True để ẩn các cảnh báo hiển thị khi shebang khởi chạy một ứng dụng không phải là Python runtime.

   * - ``source_settings``
     - Ánh xạ từ URL nguồn đến các cài đặt dành riêng cho chỉ mục đó. Khi nhiều tệp cấu hình chứa phần này, các cài đặt URL sẽ được thêm vào hoặc ghi đè, nhưng từng cài đặt riêng lẻ sẽ không được hợp nhất. Hiện tại, các cài đặt này chỉ dành cho :ref:`chữ ký chỉ mục <pymanager-index-signatures>`.


.. _install-freethreaded-windows:

Cài đặt các bản dựng free-threaded
----------------------------------

.. versionadded:: 3.13

Các bản phân phối dựng sẵn của bản dựng free-threaded có sẵn bằng cách cài đặt các tag có hậu tố ``t``.

.. code::

   $> py install 3.14t
   $> py install 3.14t-arm64
   $> py install 3.14t-32

Thao tác này sẽ cài đặt và đăng ký như bình thường. Nếu bạn không cài đặt runtime nào khác, thì ``python`` sẽ khởi chạy runtime này. Nếu không, bạn sẽ cần sử dụng ``py -V:3.14t ...`` hoặc, nếu bạn đã thêm thư mục bí danh toàn cục vào
biến môi trường :envvar:`PATH`, các lệnh ``python3.14t.exe``.


.. _pymanager-index-signatures:

Chữ ký chỉ mục
--------------

.. versionadded:: 26.2

Các tệp chỉ mục có thể được ký để phát hiện việc giả mạo. Chữ ký là một tệp catalog tại cùng URL với chỉ mục, có thêm ``.cat`` vào tên tệp. Tệp catalog phải chứa mã băm của tệp chỉ mục tương ứng và phải được ký bằng chữ ký Authenticode hợp lệ. Điều này cho phép các công cụ tiêu chuẩn (trên Windows) tạo chữ ký, và có thể sử dụng bất kỳ chứng chỉ nào miễn là hệ điều hành máy khách đã tin cậy cơ quan chứng thực (CA gốc) của chứng chỉ đó.

Chữ ký index chỉ được tải xuống và kiểm tra khi phần ``source_settings`` trong cấu hình cục bộ bao gồm URL của index và ``requires_signature`` là true, hoặc JSON của index chứa ``requires_signature`` được đặt thành true. Khi thiết lập này tồn tại trong cấu hình cục bộ, ngay cả khi có giá trị false, các thiết lập trong index cũng sẽ bị bỏ qua.

Ngoài việc yêu cầu chữ ký hợp lệ, các thiết lập ``required_root_subject`` và ``required_publisher_subject`` còn có thể giới hạn thêm các chữ ký được chấp nhận dựa trên các trường Subject của chứng chỉ. Mọi thuộc tính được chỉ định trong cấu hình phải khớp với thuộc tính trong chứng chỉ (các thuộc tính bổ sung trong chứng chỉ sẽ bị bỏ qua). Các thuộc tính thường dùng là ``CN=`` cho common name, ``O=`` cho organizational unit và ``C=`` cho quốc gia của nhà phát hành.

Cuối cùng, thiết lập ``required_publisher_eku`` cho phép yêu cầu một Enhanced Key Usage (EKU) cụ thể đã được gán cho chứng chỉ của nhà phát hành. Ví dụ, EKU ``1.3.6.1.5.5.7.3.3`` cho biết chứng chỉ được dùng để ký mã (thay vì xác thực máy chủ hoặc máy khách). Khi kết hợp với một root CA cụ thể, thiết lập này cung cấp thêm một cơ chế để xác minh chữ ký hợp lệ.

Đây là một ví dụ về phần ``source_settings`` trong tệp cấu hình. Trong trường hợp này, nhà phát hành của feed được xác định duy nhất bởi sự kết hợp giữa root Microsoft Identity Verification và EKU được root đó gán. Chữ ký cho trường hợp này sẽ được tìm thấy tại ``https://www.python.org/ftp/python/index-windows.json.cat``.

.. code:: json5

   {
     "source_settings": {
       "https://www.python.org/ftp/python/index-windows.json": {
         "requires_signature": true,
         "required_root_subject": "CN=Microsoft Identity Verification Root Certificate Authority 2020",
         "required_publisher_subject": "CN=Python Software Foundation",
         "required_publisher_eku": "1.3.6.1.4.1.311.97.608394634.79987812.305991749.578777327"
       }
     }
   }

Các thiết lập tương tự cũng có thể được chỉ định trong tệp ``index.json``. Trong trường hợp này, root và EKU bị bỏ qua, nghĩa là chữ ký phải hợp lệ và có common name cụ thể trong chứng chỉ của nhà phát hành, nhưng không thực hiện kiểm tra nào khác.

.. code:: json5

   {
     "requires_signature": true,
     "required_publisher_subject": "CN=Python Software Foundation",
     "versions": [
       // ...
     ]
   }

Khi sử dụng các thiết lập bên trong feed, người dùng sẽ được thông báo và các thiết lập này được hiển thị trong tệp nhật ký hoặc đầu ra chi tiết. Bạn nên sao chép các thiết lập này vào tệp cấu hình cục bộ đối với những feed sẽ được sử dụng thường xuyên, ताकि các sửa đổi trái phép đối với feed không thể vô hiệu hóa việc xác minh.

Không thể ghi đè vị trí của tệp chữ ký trong feed hoặc thông qua tệp cấu hình. Quản trị viên có thể cung cấp ``source_settings`` của riêng họ trong một tệp cấu hình bắt buộc (xem
:ref:`pymanager-admin-config`).

Nếu việc xác thực chữ ký không thành công, bạn sẽ được thông báo và nhắc chọn tiếp tục. Khi không được phép xác nhận tương tác (ví dụ: vì đã chỉ định ``--yes``), thao tác sẽ luôn bị hủy. Để sử dụng feed có cấu hình không hợp lệ trong trường hợp này, bạn phải cung cấp tệp cấu hình vô hiệu hóa việc kiểm tra chữ ký cho feed đó.

.. code:: json5

   "source_settings": {
     "https://www.example.com/feed-with-invalid-signature.json": {
       "requires_signature": false
     }
   }


Cài đặt proxy
-------------

.. versionadded:: 26.4

Theo mặc định, Python install manager sẽ sử dụng cài đặt proxy trên toàn hệ thống của bạn, bao gồm cả xác thực tự động. Với hầu hết người dùng, cách này hoạt động giống như trình duyệt và các ứng dụng khác.

Để ghi đè các cài đặt này, hãy sử dụng các biến môi trường ``NO_PROXY``, ``HTTP_PROXY`` và ``HTTPS_PROXY``. Bạn nên đặt các biến này trong phiên terminal trước khi sử dụng Python install manager. Các ứng dụng khác cũng có thể sử dụng các biến này, vì vậy hãy thận trọng trước khi đặt chúng trên toàn cục cho cả máy của bạn.

Đặt ``NO_PROXY`` thành bất kỳ giá trị không rỗng nào sẽ vô hiệu hóa việc sử dụng mọi proxy. Sử dụng cách này để bỏ qua cài đặt proxy mặc định của hệ thống và thử truy cập trực tiếp vào máy chủ index.

Đặt ``HTTPS_PROXY`` thành một chuỗi như ``example.com:8080`` sẽ kết nối với máy chủ proxy đó cho tất cả kết nối HTTPS. Đối với index mặc định, mọi kết nối đều sử dụng HTTPS, vì vậy đây là cài đặt thông thường để ghi đè.

Có thể cần biến ``HTTP_PROXY`` nếu bạn đang sử dụng máy chủ index riêng không dùng kết nối được mã hóa nhưng yêu cầu ghi đè máy chủ proxy mặc định. Biến này tuân theo cùng định dạng với ``HTTPS_PROXY``.

Thông tin xác thực có thể được nhúng trong một trong hai thiết lập; tuy nhiên, khi ``HTTPS_PROXY`` có thông tin xác thực được nhúng, chúng sẽ được ưu tiên sử dụng hơn các thông tin xác thực khác. Chỉ một bộ thông tin xác thực sẽ được sử dụng cho cả hai loại proxy.

.. _pymanager-troubleshoot:

Khắc phục sự cố
---------------

Nếu trình quản lý cài đặt Python của bạn có vẻ không hoạt động chính xác, hãy lần lượt thực hiện các bước kiểm tra và cách khắc phục này để xem sự cố có được giải quyết không. Nếu không, vui lòng báo cáo sự cố tại `trình theo dõi lỗi của chúng tôi <https://github.com/python/pymanager/issues>`_, kèm theo mọi tệp nhật ký liên quan (theo mặc định được ghi vào thư mục :file:`%TEMP%` của bạn).

.. Sphinx bug with text writer; remove widths & caption temporarily
.. :widths: 1, 1

.. rubric:: Khắc phục sự cố

.. list-table::
   :header-rows: 1

   * - Triệu chứng
     - Những việc cần thử

   * - ``python`` báo lỗi "không tìm thấy lệnh" hoặc mở ứng dụng Store khi tôi nhập lệnh này trong terminal.
     - Bạn đã :ref:`cài đặt Python install manager <pymanager>` chưa?

   * -
     - Bấm Start, mở "Manage app execution aliases" và kiểm tra xem các bí danh cho "Python (default)" đã được bật chưa. Nếu đã bật, hãy thử tắt rồi bật lại để cập nhật lệnh. Các lệnh "Python (default windowed)" và "Python install manager" cũng có thể cần được cập nhật lại.

   * -
     - Hãy kiểm tra xem các lệnh ``py`` và ``pymanager`` có hoạt động không.

   * -
     - Hãy đảm bảo biến :envvar:`PATH` của bạn có chứa mục nhập cho ``%UserProfile%\AppData\Local\Microsoft\WindowsApps``. Hệ điều hành mặc định thêm mục nhập này một lần, sau các đường dẫn người dùng khác. Nếu mục nhập bị xóa, các shortcut sẽ không được tìm thấy.

   * - Lệnh ``py`` báo lỗi "command not found" khi tôi nhập lệnh này vào terminal.
     - Bạn đã :ref:`cài đặt Python install manager <pymanager>` chưa?

   * -
     - Bấm Start, mở "Manage app execution aliases" và kiểm tra xem các bí danh cho "Python (default)" đã được bật chưa. Nếu đã bật, hãy thử tắt rồi bật lại để cập nhật lệnh. Các lệnh "Python (default windowed)" và "Python install manager" cũng có thể cần được cập nhật lại.

   * -
     - Hãy đảm bảo biến :envvar:`PATH` của bạn có chứa mục nhập cho ``%UserProfile%\AppData\Local\Microsoft\WindowsApps``. Hệ điều hành mặc định thêm mục nhập này một lần, sau các đường dẫn người dùng khác. Nếu mục nhập bị xóa, các shortcut sẽ không được tìm thấy.

   * - ``py`` báo lỗi "can't open file" khi tôi nhập lệnh trong terminal.
     - Điều này thường có nghĩa là bạn đã cài launcher cũ và nó được ưu tiên hơn Python install manager. Để gỡ bỏ, hãy nhấp vào Start, mở "Installed apps", tìm "Python launcher" rồi gỡ cài đặt.

   * - ``python`` không khởi chạy cùng runtime với ``py``
     - Nhấp vào Start, mở "Installed apps", tìm mọi runtime Python hiện có, rồi gỡ chúng hoặc chọn Modify và tắt các tùy chọn :envvar:`PATH`.

   * -
     - Nhấp vào Start, mở "Manage app execution aliases" và kiểm tra để đảm bảo alias ``python.exe`` của bạn được đặt thành "Python (default)".

   * - ``python`` và ``py`` không khởi chạy runtime mà tôi mong đợi
     - Kiểm tra biến môi trường :envvar:`PYTHON_MANAGER_DEFAULT` hoặc cấu hình ``default_tag`` của bạn. Lệnh ``py list`` sẽ hiển thị giá trị mặc định dựa trên các cài đặt này.

   * -
     - Các bản cài đặt do Python install manager quản lý sẽ được ưu tiên trước các bản cài đặt không được quản lý. Sử dụng ``py install`` để cài đặt runtime bạn mong muốn, hoặc cấu hình default tag của bạn.

   * -
     - Các bản cài đặt prerelease và experimental không do Python install manager quản lý có thể được ưu tiên trước các bản phát hành stable. Hãy cấu hình default tag hoặc gỡ cài đặt runtime prerelease rồi cài đặt lại bằng ``py install``.

   * - ``pythonw`` hoặc ``pyw`` không khởi chạy cùng runtime với ``python`` hoặc ``py``
     - Nhấp vào Start, mở "Manage app execution aliases" và kiểm tra để các alias ``pythonw.exe`` và ``pyw.exe`` nhất quán với những alias khác.

   * - ``pip`` hiển thị lỗi "command not found" khi tôi nhập lệnh này trong terminal.
     - Bạn đã kích hoạt virtual environment chưa? Chạy script ``.venv\Scripts\activate`` trong terminal để kích hoạt.

   * -
     - Gói có thể đã có sẵn nhưng lại thiếu tệp thực thi được tạo. Chúng tôi khuyên bạn nên sử dụng lệnh ``python -m pip`` thay thế. Việc chạy ``py install --refresh`` và đảm bảo thư mục shortcut toàn cục nằm trên :envvar:`PATH` (thư mục này sẽ được hiển thị trong đầu ra của lệnh nếu chưa có) sẽ giúp các lệnh như ``pip`` (và các gói đã cài đặt khác) khả dụng.

   * - Tôi đã cài đặt một gói bằng ``pip`` nhưng không tìm thấy lệnh của gói đó.
     - Bạn đã kích hoạt virtual environment chưa? Chạy script ``.venv\Scripts\activate`` trong terminal để kích hoạt.

   * -
     - Các gói mới không tự động được Python install manager tạo shortcut toàn cục. Tương tự, shortcut của các gói đã gỡ cài đặt cũng không bị xóa. Chạy ``py install --refresh`` để cập nhật shortcut toàn cục cho các gói mới cài đặt.

   * - Việc nhập ``script-name.py`` trong terminal sẽ mở một cửa sổ mới.
     - Đây là một hạn chế đã biết của hệ điều hành. Hãy chỉ định ``py`` trước tên script, tạo một tệp batch chứa ``@py "%~dpn0.py" %*`` với cùng tên với script, hoặc cài đặt `trình khởi chạy cũ <legacy launcher_>`_ và chọn nó làm liên kết cho các script.

   * - Không thể kéo và thả tệp vào script
     - Đây là một hạn chế đã biết của hệ điều hành. Tính năng này được hỗ trợ với `legacy launcher <legacy launcher_>`_ hoặc với Python install manager khi được cài đặt từ MSI.

   * - Tôi đã cài đặt Python install manager nhiều lần.
     - Có thể cài đặt cùng lúc từ Store hoặc WinGet, từ MSIX trên website Python và từ MSI. Tất cả đều tương thích với nhau và sẽ dùng chung cấu hình cũng như các runtime.

   * -
     - Xem :ref:`pymanager-advancedinstall` ở trên để biết các cách gỡ cài đặt install manager khác ngoài trang cài đặt Installed Apps (Add and Remove Programs) thông thường.

   * - Các thiết lập ``py.ini`` cũ của tôi không còn hoạt động.
     - Python install manager mới không còn hỗ trợ tệp cấu hình này hoặc các thiết lập của tệp, vì vậy chúng sẽ bị bỏ qua. Xem :ref:`pymanager-config` để biết thông tin về các thiết lập cấu hình.

.. _windows-embeddable:

Gói embeddable
==============

.. versionadded:: 3.5

Bản phân phối nhúng là một tệp ZIP chứa môi trường Python tối thiểu. Bản phân phối này được dùng như một phần của ứng dụng khác, thay vì được người dùng cuối truy cập trực tiếp.

Để cài đặt bản phân phối nhúng, chúng tôi khuyến nghị sử dụng ``py install`` với tùy chọn ``--target``:

.. code::

   $> py install 3.14-embed --target=<directory>

Khi được giải nén, bản phân phối nhúng gần như hoàn toàn độc lập với hệ thống của người dùng, bao gồm các biến môi trường, cài đặt system registry và các package đã cài đặt. Standard library được tích hợp dưới dạng các tệp ``.pyc`` đã được biên dịch trước và tối ưu hóa trong một tệp ZIP, đồng thời ``python3.dll``, ``python313.dll``, ``python.exe`` và ``pythonw.exe`` đều được cung cấp. Tcl/tk (bao gồm tất cả các thành phần phụ thuộc, chẳng hạn như Idle), pip và tài liệu Python không được tích hợp.

Một tệp ``._pth`` mặc định được tích hợp, giúp hạn chế thêm các đường dẫn tìm kiếm mặc định (như được mô tả bên dưới trong :ref:`windows_finding_modules`). Tệp này dành cho các nhà tích hợp sửa đổi khi cần.

Các package của bên thứ ba nên được trình cài đặt ứng dụng cài đặt cùng với bản phân phối nhúng. Không hỗ trợ sử dụng pip để quản lý các dependency như khi cài đặt Python thông thường với bản phân phối này, mặc dù nếu thực hiện cẩn thận thì vẫn có thể tích hợp và sử dụng pip để tự động cập nhật. Nhìn chung, các package của bên thứ ba nên được xem là một phần của ứng dụng ("vendoring") để developer có thể đảm bảo tính tương thích với các phiên bản mới hơn trước khi cung cấp bản cập nhật cho người dùng.

Hai trường hợp sử dụng được khuyến nghị cho bản phân phối này được mô tả bên dưới.

Ứng dụng Python
---------------

Một ứng dụng được viết bằng Python không nhất thiết yêu cầu người dùng phải biết điều đó. Trong trường hợp này, có thể sử dụng bản phân phối nhúng để đưa một phiên bản Python riêng vào gói cài đặt. Tùy thuộc vào mức độ minh bạch mong muốn (hoặc ngược lại, mức độ chuyên nghiệp mà ứng dụng nên thể hiện), có hai tùy chọn.

Việc sử dụng một executable chuyên dụng làm launcher yêu cầu viết một chút mã, nhưng mang lại trải nghiệm minh bạch nhất cho người dùng. Với launcher được tùy chỉnh, không có dấu hiệu rõ ràng nào cho thấy chương trình đang chạy trên Python: có thể tùy chỉnh biểu tượng, chỉ định thông tin công ty và phiên bản, đồng thời các liên kết tệp hoạt động chính xác. Trong hầu hết trường hợp, một launcher tùy chỉnh chỉ cần có khả năng gọi ``Py_Main`` bằng một dòng lệnh được ghi sẵn.

Cách tiếp cận đơn giản hơn là cung cấp một tệp batch hoặc shortcut được tạo sẵn, trực tiếp gọi ``python.exe`` hoặc ``pythonw.exe`` với các đối số dòng lệnh cần thiết. Trong trường hợp này, ứng dụng sẽ được hiển thị là Python thay vì tên thực tế của ứng dụng, và người dùng có thể gặp khó khăn khi phân biệt ứng dụng đó với các tiến trình Python khác đang chạy hoặc các liên kết tệp.

Với cách tiếp cận sau, các package nên được cài đặt dưới dạng các thư mục nằm cạnh executable Python để bảo đảm chúng có sẵn trên path. Với launcher chuyên dụng, các package có thể được đặt ở những vị trí khác vì có thể chỉ định search path trước khi khởi chạy ứng dụng.

Nhúng Python
------------

Các ứng dụng được viết bằng mã native thường yêu cầu một dạng ngôn ngữ scripting, và bản phân phối Python nhúng có thể được sử dụng cho mục đích này. Nhìn chung, phần lớn ứng dụng được viết bằng mã native, và một phần trong đó sẽ gọi ``python.exe`` hoặc trực tiếp sử dụng ``python3.dll``. Trong cả hai trường hợp, chỉ cần giải nén bản phân phối nhúng vào một thư mục con của thư mục cài đặt ứng dụng là đủ để cung cấp một Python interpreter có thể tải được.

Cũng như khi sử dụng cho ứng dụng, các package có thể được cài đặt ở bất kỳ vị trí nào vì có thể chỉ định các search path trước khi khởi tạo interpreter. Ngoài ra, không có khác biệt cơ bản nào giữa việc sử dụng bản phân phối nhúng và một bản cài đặt thông thường.


.. _windows-nuget:

Các package nuget.org
=====================

.. versionadded:: 3.5.2

Package nuget.org là một môi trường Python có kích thước được thu gọn, предназначено để sử dụng trên các hệ thống continuous integration và build không có bản cài đặt Python trên toàn hệ thống. Mặc dù nuget là "trình quản lý package cho .NET", nó cũng hoạt động hoàn toàn tốt với các package chứa công cụ dùng trong thời gian build.

Truy cập `nuget.org <https://www.nuget.org/>`_ để xem thông tin cập nhật mới nhất về cách sử dụng nuget. Phần dưới đây là bản tóm tắt đủ cho các nhà phát triển Python.

Có thể tải trực tiếp công cụ dòng lệnh ``nuget.exe`` từ ``https://dist.nuget.org/win-x86-commandline/latest/nuget.exe``, chẳng hạn bằng curl hoặc PowerShell. Với công cụ này, phiên bản Python mới nhất cho máy 64-bit hoặc 32-bit được cài đặt bằng::

   nuget.exe install python -ExcludeVersion -OutputDirectory .
   nuget.exe install pythonx86 -ExcludeVersion -OutputDirectory .

Để chọn một phiên bản cụ thể, hãy thêm ``-Version 3.x.y``. Có thể thay đổi thư mục đầu ra từ ``.``, và package sẽ được cài đặt vào một thư mục con. Theo mặc định, thư mục con được đặt tên giống với package, và nếu không có tùy chọn ``-ExcludeVersion``, tên này sẽ bao gồm phiên bản cụ thể được cài đặt. Bên trong thư mục con là một thư mục ``tools`` chứa bản cài đặt Python:

.. code-block:: doscon

   # Without -ExcludeVersion
   > .\python.3.5.2\tools\python.exe -V
   Python 3.5.2

   # With -ExcludeVersion
   > .\python\tools\python.exe -V
   Python 3.5.2

Nhìn chung, các package nuget không thể được nâng cấp, và nên cài đặt các phiên bản mới hơn cạnh nhau rồi tham chiếu bằng đường dẫn đầy đủ. Ngoài ra, bạn có thể xóa thủ công thư mục package rồi cài đặt lại. Nhiều hệ thống CI sẽ tự động thực hiện việc này nếu chúng không giữ lại các tệp giữa những lần build.

Cùng cấp với thư mục ``tools`` là thư mục ``build\native``. Thư mục này chứa tệp thuộc tính MSBuild ``python.props``, có thể được sử dụng trong một dự án C++ để tham chiếu đến bản cài đặt Python. Việc đưa các thiết lập này vào sẽ tự động sử dụng các header và thư viện import trong quá trình build.

Các trang thông tin gói trên nuget.org là `www.nuget.org/packages/python <https://www.nuget.org/packages/python>`_ cho phiên bản 64-bit, `www.nuget.org/packages/pythonx86 <https://www.nuget.org/packages/pythonx86>`_ cho phiên bản 32-bit và `www.nuget.org/packages/pythonarm64 <https://www.nuget.org/packages/pythonarm64>`_ cho phiên bản ARM64

Các gói free-threaded
---------------------

.. versionadded:: 3.13

Các gói chứa binary free-threaded có tên `python-freethreaded <https://www.nuget.org/packages/python-freethreaded>`_ cho phiên bản 64-bit, `pythonx86-freethreaded <https://www.nuget.org/packages/pythonx86-freethreaded>`_ cho phiên bản 32-bit và `pythonarm64-freethreaded <https://www.nuget.org/packages/pythonarm64-freethreaded>`_ cho phiên bản ARM64. Các gói này chứa cả hai entry point ``python3.13t.exe`` và ``python.exe``, cả hai đều chạy ở chế độ free-threaded.


Các gói thay thế
================

Ngoài bản phân phối CPython tiêu chuẩn, còn có các gói đã được sửa đổi và bổ sung thêm chức năng. Sau đây là danh sách các phiên bản phổ biến cùng những tính năng chính của chúng:

`ActivePython <https://www.activestate.com/products/python/>`_
    Trình cài đặt tương thích với nhiều nền tảng, có tài liệu và PyWin32

`Anaconda <https://www.anaconda.com/download/>`_
    Các module khoa học phổ biến (chẳng hạn như numpy, scipy và pandas) cùng trình quản lý gói ``conda``.

`Enthought Deployment Manager <https://assets.enthought.com/downloads/edm/>`_
    "Môi trường Python và Trình quản lý gói thế hệ tiếp theo".

    Trước đây Enthought cung cấp Canopy, nhưng sản phẩm này đã `hết vòng đời vào năm 2016 <https://support.enthought.com/hc/en-us/articles/360038600051-Canopy-GUI-end-of-life-transition-to-the-Enthought-Deployment-Manager-EDM-and-Visual-Studio-Code>`_.

`WinPython <https://winpython.github.io/>`_
    Bản phân phối dành riêng cho Windows với các gói khoa học được dựng sẵn và các công cụ để xây dựng gói.

Lưu ý rằng các gói này có thể không bao gồm phiên bản mới nhất của Python hoặc các thư viện khác, đồng thời không được nhóm Python nòng cốt duy trì hoặc hỗ trợ.


Các phiên bản Windows được hỗ trợ
=================================

Như được nêu trong :pep:`11`, một bản phát hành Python chỉ hỗ trợ một nền tảng Windows trong thời gian Microsoft xem nền tảng đó là đang được hỗ trợ mở rộng. Điều này có nghĩa là Python |version| hỗ trợ Windows 10 trở lên. Nếu bạn cần hỗ trợ Windows 7, hãy cài đặt Python 3.8. Nếu bạn cần hỗ trợ Windows 8.1, hãy cài đặt Python 3.12.


.. _max-path:

Loại bỏ giới hạn MAX_PATH
=========================

Theo cách thức hoạt động trước đây, Windows giới hạn độ dài đường dẫn ở mức 260 ký tự. Điều này có nghĩa là các đường dẫn dài hơn mức này sẽ không được phân giải và gây ra lỗi.

Trong các phiên bản Windows mới nhất, giới hạn này có thể được mở rộng lên hơn 32.000 ký tự. Quản trị viên của bạn cần kích hoạt chính sách nhóm "Enable Win32 long paths" hoặc đặt ``LongPathsEnabled`` thành ``1`` trong khóa registry ``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem``.

Điều này cho phép hàm :func:`open`, module :mod:`os` và hầu hết chức năng xử lý đường dẫn khác chấp nhận và trả về các đường dẫn dài hơn 260 ký tự.

Sau khi thay đổi tùy chọn trên và khởi động lại, không cần thực hiện thêm cấu hình nào.


.. _win-utf8-mode:

Chế độ UTF-8
============

.. versionadded:: 3.7

Windows vẫn sử dụng các encoding cũ cho encoding hệ thống (ANSI Code Page). Python sử dụng encoding này làm encoding mặc định cho các tệp văn bản (ví dụ
:func:`locale.getencoding`).

Điều này có thể gây ra sự cố vì UTF-8 được sử dụng rộng rãi trên internet và trong hầu hết các hệ thống Unix, bao gồm WSL (Windows Subsystem for Linux).

Bạn có thể sử dụng :ref:`Python UTF-8 Mode <utf8-mode>` để thay đổi encoding văn bản mặc định thành UTF-8. Bạn có thể bật :ref:`Python UTF-8 Mode <utf8-mode>` thông qua tùy chọn ``-X utf8`` dòng lệnh hoặc biến môi trường ``PYTHONUTF8=1``. Xem :envvar:`PYTHONUTF8` để biết cách bật chế độ UTF-8 và
:ref:`setting-envvars` để biết cách sửa đổi các biến môi trường.

Khi :ref:`Python UTF-8 Mode <utf8-mode>` được bật, bạn vẫn có thể sử dụng encoding hệ thống (ANSI Code Page) thông qua codec "mbcs".

Lưu ý rằng việc thêm ``PYTHONUTF8=1`` vào các biến môi trường mặc định sẽ ảnh hưởng đến tất cả ứng dụng Python 3.7+ trên hệ thống của bạn. Nếu bạn có bất kỳ ứng dụng Python 3.7+ nào phụ thuộc vào encoding hệ thống cũ, bạn nên đặt biến môi trường này tạm thời hoặc sử dụng tùy chọn dòng lệnh ``-X utf8``.

.. note::
   Ngay cả khi UTF-8 mode bị tắt, Python vẫn sử dụng UTF-8 theo mặc định trên Windows cho:

   * I/O console, bao gồm cả I/O chuẩn (xem :pep:`528` để biết chi tiết).
   * :term:`encoding của hệ thống tệp <filesystem encoding and error handler>` (xem :pep:`529` để biết chi tiết).


.. _windows_finding_modules:

Tìm mô-đun
==========

Các ghi chú này bổ sung cho phần mô tả tại :ref:`sys-path-init` bằng các ghi chú chi tiết dành cho Windows.

Khi không tìm thấy tệp ``._pth``, :data:`sys.path` được điền trên Windows như sau:

* Một mục trống được thêm vào đầu, tương ứng với thư mục hiện tại.

* Nếu biến môi trường :envvar:`PYTHONPATH` tồn tại, như được mô tả trong
  :ref:`using-on-envvars`, các mục của biến này sẽ được thêm tiếp theo. Lưu ý rằng trên Windows, các đường dẫn trong biến này phải được phân tách bằng dấu chấm phẩy để phân biệt với dấu hai chấm được dùng trong các mã ổ đĩa (``C:\``, v.v.).

* Có thể thêm các "đường dẫn ứng dụng" bổ sung vào registry dưới dạng các subkey của
  :samp:`\\SOFTWARE\\Python\\PythonCore\\{version}\\PythonPath` trong cả hai hive ``HKEY_CURRENT_USER`` và ``HKEY_LOCAL_MACHINE``. Các subkey có giá trị mặc định là các chuỗi đường dẫn được phân tách bằng dấu chấm phẩy sẽ khiến từng đường dẫn được thêm vào :data:`sys.path`. (Lưu ý rằng tất cả các trình cài đặt đã biết chỉ sử dụng HKLM, vì vậy HKCU thường để trống.)

* Nếu biến môi trường :envvar:`PYTHONHOME` được đặt, biến này được xem là "Python Home". Nếu không, đường dẫn của tệp thực thi Python chính được dùng để tìm một "tệp mốc" (hoặc ``Lib\os.py`` hoặc ``pythonXY.zip``) nhằm suy ra "Python Home". Nếu tìm thấy Python home, các thư mục con liên quan được thêm vào :data:`sys.path` (``Lib``, ``plat-win``, v.v.) sẽ dựa trên thư mục đó. Nếu không, đường dẫn Python cốt lõi được xây dựng từ PythonPath được lưu trong registry.

* Nếu không thể xác định Python Home, không có :envvar:`PYTHONPATH` nào được chỉ định trong môi trường và không tìm thấy mục registry nào, một đường dẫn mặc định có các mục tương đối sẽ được sử dụng (ví dụ: ``.\Lib;.\plat-win``, v.v.).

Nếu tìm thấy tệp ``pyvenv.cfg`` nằm cùng với tệp thực thi chính hoặc trong thư mục ngay phía trên tệp thực thi, các biến thể sau sẽ được áp dụng:

* Nếu ``home`` là một đường dẫn tuyệt đối và :envvar:`PYTHONHOME` chưa được đặt, đường dẫn này sẽ được sử dụng thay cho đường dẫn đến tệp thực thi chính khi suy ra vị trí thư mục home.

Kết quả cuối cùng của tất cả những điều này là:

* Khi chạy :file:`python.exe` hoặc bất kỳ tệp .exe nào khác trong thư mục Python chính (dù là phiên bản đã cài đặt hay chạy trực tiếp từ thư mục PCbuild), đường dẫn lõi sẽ được suy ra và các đường dẫn lõi trong registry sẽ bị bỏ qua. Các "application paths" khác trong registry luôn được đọc.

* Khi Python được lưu trữ trong một tệp .exe khác (thư mục khác, được nhúng qua COM, v.v.), "Python Home" sẽ không được suy ra, vì vậy đường dẫn lõi từ registry sẽ được sử dụng. Các "application paths" khác trong registry luôn được đọc.

* Nếu Python không thể tìm thấy thư mục home của nó và không có giá trị nào trong registry (tệp .exe đóng băng, một số thiết lập cài đặt rất bất thường), bạn sẽ nhận được một đường dẫn có một số đường dẫn mặc định nhưng ở dạng tương đối.

Đối với những người muốn tích hợp Python vào ứng dụng hoặc bản phân phối của mình, lời khuyên sau đây sẽ giúp ngăn xung đột với các bản cài đặt khác:

* Đặt một tệp ``._pth`` bên cạnh tệp thực thi của bạn, trong đó chứa các thư mục cần đưa vào. Thao tác này sẽ bỏ qua các đường dẫn được liệt kê trong registry và các biến môi trường, đồng thời cũng bỏ qua :mod:`site` trừ khi ``import site`` được liệt kê.

* Nếu bạn đang tải :file:`python3.dll` hoặc :file:`python37.dll` trong tệp thực thi của riêng mình, hãy đặt rõ ràng :c:member:`PyConfig.module_search_paths` trước khi
  :c:func:`Py_InitializeFromConfig`.

* Xóa và/hoặc ghi đè :envvar:`PYTHONPATH`, rồi đặt :envvar:`PYTHONHOME` trước khi khởi chạy :file:`python.exe` từ ứng dụng của bạn.

* Nếu bạn không thể sử dụng các đề xuất trước đó (ví dụ: bạn là một bản phân phối cho phép người dùng chạy trực tiếp :file:`python.exe`), hãy đảm bảo tệp mốc (:file:`Lib\\os.py`) tồn tại trong thư mục cài đặt của bạn. (Lưu ý rằng tệp này sẽ không được phát hiện bên trong tệp ZIP, nhưng một tệp ZIP được đặt tên chính xác sẽ được phát hiện thay thế.)

Những cách này sẽ đảm bảo các tệp trong bản cài đặt trên toàn hệ thống không được ưu tiên hơn bản sao của standard library đi kèm với ứng dụng của bạn. Nếu không, người dùng có thể gặp sự cố khi sử dụng ứng dụng của bạn. Lưu ý rằng đề xuất đầu tiên là tốt nhất, vì các đề xuất còn lại vẫn có thể bị ảnh hưởng bởi các đường dẫn không chuẩn trong registry và user site-packages.

.. versionchanged:: 3.6

   Bổ sung hỗ trợ tệp ``._pth`` và loại bỏ tùy chọn ``applocal`` khỏi ``pyvenv.cfg``.

.. versionchanged:: 3.6

   Bổ sung :file:`python{XX}.zip` làm một mốc tiềm năng khi nằm ngay cạnh tệp thực thi.

.. deprecated:: 3.6

   Các module được chỉ định trong registry tại ``Modules`` (không phải ``PythonPath``) có thể được :class:`importlib.machinery.WindowsRegistryFinder` import. Finder này được bật trên Windows trong phiên bản 3.6.0 trở về trước, nhưng trong tương lai có thể cần được thêm một cách rõ ràng vào :data:`sys.meta_path`.

Các module bổ sung
==================

Mặc dù Python hướng đến khả năng hoạt động trên mọi nền tảng, vẫn có những tính năng chỉ dành riêng cho Windows. Có một vài module, cả trong thư viện chuẩn lẫn bên ngoài, cùng các đoạn mã mẫu để sử dụng những tính năng này.

Các module chuẩn dành riêng cho Windows được ghi lại trong
:ref:`mswin-specific-services`.

PyWin32
-------

Module :pypi:`PyWin32` do Mark Hammond phát triển là một tập hợp các module hỗ trợ nâng cao dành riêng cho Windows. Tập hợp này bao gồm các tiện ích cho:

* `Component Object Model <https://learn.microsoft.com/windows/win32/com/component-object-model--com--portal>`_ (COM)
* Các lệnh gọi API Win32
* Registry
* Nhật ký sự kiện
* `Giao diện người dùng Microsoft Foundation Classes <https://learn.microsoft.com/cpp/mfc/mfc-desktop-applications>`_ (MFC)

`PythonWin <https://web.archive.org/web/20060524042422/ https://www.python.org/windows/pythonwin/>`_ là một ứng dụng MFC mẫu được cung cấp cùng PyWin32. Đây là một IDE có thể nhúng với trình gỡ lỗi tích hợp.

.. seealso::

   `Win32 How Do I...? <https://timgolden.me.uk/python/win32_how_do_i.html>`_
      của Tim Golden

   `Python và COM <https://www.boddie.org.uk/python/COM.html>`_
      bởi David và Paul Boddie


cx_Freeze
---------

`cx_Freeze <https://cx-freeze.readthedocs.io/en/latest/>`_ đóng gói các script Python thành các chương trình Windows thực thi (:file:`{*}.exe` tệp). Sau khi hoàn tất, bạn có thể phân phối ứng dụng của mình mà không yêu cầu người dùng cài đặt Python.


Biên dịch Python trên Windows
=============================

Nếu muốn tự biên dịch CPython, việc đầu tiên bạn nên làm là lấy `mã nguồn <https://www.python.org/downloads/source/>`_. Bạn có thể tải mã nguồn của bản phát hành mới nhất hoặc chỉ cần lấy một `bản checkout <https://devguide.python.org/setup/#get-the-source-code>`_ mới.

Cây mã nguồn chứa một solution build và các tệp project dành cho Microsoft Visual Studio, trình biên dịch được sử dụng để build các bản phát hành Python chính thức. Các tệp này nằm trong :file:`PCbuild` thư mục.

Xem :file:`PCbuild/readme.txt` để biết thông tin chung về quy trình build.

Đối với các extension module, hãy tham khảo :ref:`building-on-windows`.



.. _windows-full:

Trình cài đặt đầy đủ (đã ngừng sử dụng)
=======================================

.. deprecated:: 3.14

   Trình cài đặt này đã ngừng sử dụng kể từ phiên bản 3.14 và sẽ không được tạo cho Python 3.16 trở lên. Xem :ref:`pymanager` để biết thông tin về trình cài đặt hiện đại.


Các bước cài đặt
----------------

Có bốn trình cài đặt Python |version| để tải xuống - mỗi phiên bản 32-bit và 64-bit của trình thông dịch có hai trình cài đặt. *web installer* là một gói tải xuống ban đầu nhỏ và sẽ tự động tải xuống các thành phần cần thiết khi cần. *offline installer* bao gồm các thành phần cần thiết cho một bản cài đặt mặc định và chỉ yêu cầu kết nối internet đối với các tính năng tùy chọn. Xem :ref:`install-layout-option` để biết các cách khác nhằm tránh tải xuống trong quá trình cài đặt.

Sau khi khởi động trình cài đặt, bạn có thể chọn một trong hai tùy chọn:

.. image:: win_installer.png

Nếu bạn chọn "Install Now":

* Bạn sẽ *không* cần có quyền quản trị viên (trừ khi cần cập nhật hệ thống cho C Runtime Library hoặc bạn cài đặt :ref:`launcher` cho tất cả người dùng)
* Python sẽ được cài đặt vào thư mục người dùng của bạn
* :ref:`launcher` sẽ được cài đặt theo tùy chọn ở cuối trang đầu tiên
* Standard library, test suite, launcher và pip sẽ được cài đặt
* Nếu được chọn, thư mục cài đặt sẽ được thêm vào :envvar:`PATH` của bạn
* Các shortcut sẽ chỉ hiển thị đối với người dùng hiện tại

Chọn "Customize installation" sẽ cho phép bạn chọn các tính năng cần cài đặt, vị trí cài đặt cùng các tùy chọn hoặc hành động sau khi cài đặt khác. Để cài đặt các debugging symbols hoặc binaries, bạn sẽ cần sử dụng tùy chọn này.

Để thực hiện cài đặt cho tất cả người dùng, bạn nên chọn "Customize installation". Trong trường hợp này:

* Bạn có thể được yêu cầu cung cấp thông tin xác thực hoặc phê duyệt của quản trị viên
* Python sẽ được cài đặt vào thư mục Program Files
* :ref:`launcher` sẽ được cài đặt vào thư mục Windows
* Bạn có thể chọn các tính năng tùy chọn trong quá trình cài đặt
* Thư viện chuẩn có thể được biên dịch trước thành bytecode
* Nếu được chọn, thư mục cài đặt sẽ được thêm vào :envvar:`PATH` của hệ thống
* Các shortcut khả dụng cho tất cả người dùng


Loại bỏ giới hạn MAX_PATH
-------------------------

Theo cách thức hoạt động trước đây, Windows giới hạn độ dài đường dẫn ở mức 260 ký tự. Điều này có nghĩa là các đường dẫn dài hơn mức này sẽ không được phân giải và gây ra lỗi.

Trong các phiên bản Windows mới nhất, giới hạn này có thể được mở rộng lên khoảng 32.000 ký tự. Quản trị viên của bạn cần kích hoạt group policy "Enable Win32 long paths" hoặc đặt ``LongPathsEnabled`` thành ``1`` trong khóa registry ``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem``.

Điều này cho phép hàm :func:`open`, module :mod:`os` và hầu hết chức năng xử lý đường dẫn khác chấp nhận và trả về các đường dẫn dài hơn 260 ký tự.

Sau khi thay đổi tùy chọn trên, không cần cấu hình thêm.

.. versionchanged:: 3.6

   Python đã hỗ trợ các đường dẫn dài.

.. _install-quiet-option:

Cài đặt không có giao diện người dùng
-------------------------------------

Tất cả các tùy chọn có trong giao diện trình cài đặt cũng có thể được chỉ định từ dòng lệnh, cho phép các trình cài đặt được lập script tái tạo quá trình cài đặt trên nhiều máy mà không cần người dùng tương tác. Các tùy chọn này cũng có thể được thiết lập mà không ẩn giao diện người dùng để thay đổi một số giá trị mặc định.

Có thể truyền các tùy chọn sau đây (được tìm thấy bằng cách thực thi trình cài đặt với ``/?``) vào trình cài đặt:

+---------------------+-------------------------------------------------------------------------+
| Tên                 | Mô tả                                                                   |
+=====================+=========================================================================+
| /passive            | để hiển thị tiến trình mà không yêu cầu người dùng tương tác            |
+---------------------+-------------------------------------------------------------------------+
| /quiet              | để cài đặt/gỡ cài đặt mà không hiển thị bất kỳ giao diện người dùng nào |
+---------------------+-------------------------------------------------------------------------+
| /simple             | để ngăn người dùng tùy chỉnh                                            |
+---------------------+-------------------------------------------------------------------------+
| /uninstall          | để gỡ bỏ Python (không cần xác nhận)                                    |
+---------------------+-------------------------------------------------------------------------+
| /layout [directory] | để tải trước tất cả các thành phần                                      |
+---------------------+-------------------------------------------------------------------------+
| /log [filename]     | để chỉ định vị trí các tệp nhật ký                                      |
+---------------------+-------------------------------------------------------------------------+

Tất cả các tùy chọn khác được truyền dưới dạng ``name=value``, trong đó giá trị thường là ``0`` để tắt một tính năng, ``1`` để bật một tính năng hoặc một đường dẫn. Danh sách đầy đủ các tùy chọn hiện có được hiển thị bên dưới.

+---------------------------+--------------------------------------+--------------------------+
| Name                      | Description                          | Default                  |
+===========================+======================================+==========================+
| InstallAllUsers           | Perform a system-wide installation.  | 0                        |
+---------------------------+--------------------------------------+--------------------------+
| TargetDir                 | The installation directory           | Selected based on        |
|                           |                                      | InstallAllUsers          |
+---------------------------+--------------------------------------+--------------------------+
| DefaultAllUsersTargetDir  | The default installation directory   | :file:`%ProgramFiles%\\\ |
|                           | for all-user installs                | Python X.Y` or :file:`\  |
|                           |                                      | %ProgramFiles(x86)%\\\   |
|                           |                                      | Python X.Y`              |
+---------------------------+--------------------------------------+--------------------------+
| DefaultJustForMeTargetDir | The default install directory for    | :file:`%LocalAppData%\\\ |
|                           | just-for-me installs                 | Programs\\Python\\\      |
|                           |                                      | PythonXY` or             |
|                           |                                      | :file:`%LocalAppData%\\\ |
|                           |                                      | Programs\\Python\\\      |
|                           |                                      | PythonXY-32` or          |
|                           |                                      | :file:`%LocalAppData%\\\ |
|                           |                                      | Programs\\Python\\\      |
|                           |                                      | PythonXY-64`             |
+---------------------------+--------------------------------------+--------------------------+
| DefaultCustomTargetDir    | The default custom install directory | (empty)                  |
|                           | displayed in the UI                  |                          |
+---------------------------+--------------------------------------+--------------------------+
| AssociateFiles            | Create file associations if the      | 1                        |
|                           | launcher is also installed.          |                          |
+---------------------------+--------------------------------------+--------------------------+
| CompileAll                | Compile all ``.py`` files to         | 0                        |
|                           | ``.pyc``.                            |                          |
+---------------------------+--------------------------------------+--------------------------+
| PrependPath               | Prepend install and Scripts          | 0                        |
|                           | directories  to :envvar:`PATH` and   |                          |
|                           | add ``.PY`` to :envvar:`PATHEXT`     |                          |
+---------------------------+--------------------------------------+--------------------------+
| AppendPath                | Append install and Scripts           | 0                        |
|                           | directories  to :envvar:`PATH` and   |                          |
|                           | add ``.PY`` to :envvar:`PATHEXT`     |                          |
+---------------------------+--------------------------------------+--------------------------+
| Shortcuts                 | Create shortcuts for the interpreter,| 1                        |
|                           | documentation and IDLE if installed. |                          |
+---------------------------+--------------------------------------+--------------------------+
| Include_doc               | Install Python manual                | 1                        |
+---------------------------+--------------------------------------+--------------------------+
| Include_debug             | Install debug binaries               | 0                        |
+---------------------------+--------------------------------------+--------------------------+
| Include_dev               | Install developer headers and        | 1                        |
|                           | libraries. Omitting this may lead to |                          |
|                           | an unusable installation.            |                          |
+---------------------------+--------------------------------------+--------------------------+
| Include_exe               | Install :file:`python.exe` and       | 1                        |
|                           | related files. Omitting this may     |                          |
|                           | lead to an unusable installation.    |                          |
+---------------------------+--------------------------------------+--------------------------+
| Include_launcher          | Install :ref:`launcher`.             | 1                        |
+---------------------------+--------------------------------------+--------------------------+
| InstallLauncherAllUsers   | Installs the launcher for all        | 1                        |
|                           | users. Also requires                 |                          |
|                           | ``Include_launcher`` to be set to 1  |                          |
+---------------------------+--------------------------------------+--------------------------+
| Include_lib               | Install standard library and         | 1                        |
|                           | extension modules. Omitting this may |                          |
|                           | lead to an unusable installation.    |                          |
+---------------------------+--------------------------------------+--------------------------+
| Include_pip               | Install bundled pip and setuptools   | 1                        |
+---------------------------+--------------------------------------+--------------------------+
| Include_symbols           | Install debugging symbols (``*.pdb``)| 0                        |
+---------------------------+--------------------------------------+--------------------------+
| Include_tcltk             | Install Tcl/Tk support and IDLE      | 1                        |
+---------------------------+--------------------------------------+--------------------------+
| Include_test              | Install standard library test suite  | 1                        |
+---------------------------+--------------------------------------+--------------------------+
| Include_tools             | Install utility scripts              | 1                        |
+---------------------------+--------------------------------------+--------------------------+
| LauncherOnly              | Only installs the launcher. This     | 0                        |
|                           | will override most other options.    |                          |
+---------------------------+--------------------------------------+--------------------------+
| SimpleInstall             | Disable most install UI              | 0                        |
+---------------------------+--------------------------------------+--------------------------+
| SimpleInstallDescription  | A custom message to display when the | (empty)                  |
|                           | simplified install UI is used.       |                          |
+---------------------------+--------------------------------------+--------------------------+

Ví dụ: để cài đặt ngầm một bản cài đặt Python mặc định trên toàn hệ thống, bạn có thể sử dụng lệnh sau (từ command prompt có quyền nâng cao)::

    python-3.9.0.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

Để cho phép người dùng dễ dàng cài đặt một bản sao Python cá nhân mà không có bộ kiểm thử, bạn có thể cung cấp một shortcut bằng lệnh sau. Lệnh này sẽ hiển thị một trang ban đầu đơn giản hóa và không cho phép tùy chỉnh::

    python-3.9.0.exe InstallAllUsers=0 Include_launcher=0 Include_test=0
        SimpleInstall=1 SimpleInstallDescription="Just for me, no test suite."

(Lưu ý rằng việc bỏ qua launcher cũng đồng nghĩa với việc bỏ qua các liên kết tệp và chỉ được khuyến nghị khi cài đặt cho từng người dùng nếu đồng thời đã có một bản cài đặt trên toàn hệ thống bao gồm launcher.)

Các tùy chọn được liệt kê ở trên cũng có thể được cung cấp trong một tệp có tên ``unattend.xml`` nằm cùng thư mục với tệp thực thi. Tệp này chỉ định một danh sách các tùy chọn và giá trị. Khi một giá trị được cung cấp dưới dạng thuộc tính, giá trị đó sẽ được chuyển đổi thành số nếu có thể. Các giá trị được cung cấp dưới dạng văn bản phần tử luôn được giữ ở dạng chuỗi. Tệp ví dụ này thiết lập các tùy chọn giống như ví dụ trước:

.. code-block:: xml

    <Options>
        <Option Name="InstallAllUsers" Value="no" />
        <Option Name="Include_launcher" Value="0" />
        <Option Name="Include_test" Value="no" />
        <Option Name="SimpleInstall" Value="yes" />
        <Option Name="SimpleInstallDescription">Just for me, no test suite</Option>
    </Options>

.. _install-layout-option:

Cài đặt mà không cần tải xuống
------------------------------

Vì một số tính năng của Python không được bao gồm trong lần tải xuống trình cài đặt ban đầu, việc chọn các tính năng đó có thể yêu cầu kết nối internet. Để tránh yêu cầu này, có thể tải xuống theo yêu cầu tất cả các thành phần có thể có nhằm tạo một *layout* hoàn chỉnh, sau đó sẽ không còn yêu cầu kết nối internet bất kể các tính năng được chọn. Lưu ý rằng gói tải xuống này có thể lớn hơn mức cần thiết, nhưng khi cần thực hiện số lượng lớn lần cài đặt, việc có một bản sao được lưu trong bộ nhớ đệm cục bộ sẽ rất hữu ích.

Thực thi lệnh sau từ Command Prompt để tải xuống tất cả các tệp có thể cần thiết. Hãy nhớ thay thế ``python-3.9.0.exe`` bằng tên thực tế của trình cài đặt và tạo các layout trong các thư mục riêng để tránh xung đột giữa các tệp có cùng tên.

::

    python-3.9.0.exe /layout [optional target directory]

Bạn cũng có thể chỉ định tùy chọn ``/quiet`` để ẩn phần hiển thị tiến trình.

Sửa đổi bản cài đặt
-------------------

Sau khi Python được cài đặt, bạn có thể thêm hoặc xóa các tính năng thông qua công cụ Programs and Features có sẵn trong Windows. Chọn mục Python rồi chọn "Uninstall/Change" để mở trình cài đặt ở chế độ bảo trì.

"Modify" cho phép bạn thêm hoặc xóa các tính năng bằng cách thay đổi các ô kiểm; những ô kiểm không thay đổi sẽ không cài đặt hoặc xóa bất kỳ thứ gì. Một số tùy chọn không thể thay đổi ở chế độ này, chẳng hạn như thư mục cài đặt; để thay đổi các tùy chọn này, bạn sẽ cần xóa rồi cài đặt lại hoàn toàn Python.

"Repair" sẽ xác minh tất cả các tệp cần được cài đặt theo các thiết lập hiện tại và thay thế những tệp đã bị xóa hoặc sửa đổi.

"Uninstall" sẽ xóa hoàn toàn Python, ngoại trừ
:ref:`launcher`, mục này có mục riêng trong Programs and Features.


Cài đặt các bản dựng free-threaded
----------------------------------

.. versionadded:: 3.13

Để cài đặt các binary dựng sẵn có bật free-threading (xem :pep:`703`), bạn nên chọn "Customize installation". Trang tùy chọn thứ hai có ô kiểm "Download free-threaded binaries".

.. image:: win_install_freethreaded.png

Việc chọn tùy chọn này sẽ tải xuống và cài đặt các binary bổ sung vào cùng vị trí với bản cài Python chính. Tệp thực thi chính có tên là ``python3.13t.exe``, còn các binary khác либо nhận hậu tố ``t`` hoặc hậu tố ABI đầy đủ. Các tệp mã nguồn Python và các dependency bên thứ ba đi kèm được dùng chung với bản cài chính.

Phiên bản free-threaded được đăng ký dưới dạng bản cài Python thông thường với thẻ ``3.13t`` (với hậu tố ``-32`` hoặc ``-arm64`` như thông thường đối với các nền tảng đó). Điều này cho phép các công cụ phát hiện phiên bản này, đồng thời cho phép :ref:`launcher` hỗ trợ ``py.exe -3.13t``. Lưu ý rằng launcher sẽ diễn giải ``py.exe -3`` (hoặc shebang ``python3``) là "bản cài 3.x mới nhất", trong đó các binary free-threaded sẽ được ưu tiên hơn các binary thông thường, còn ``py.exe -3.13`` thì không. Nếu bạn sử dụng kiểu tùy chọn rút gọn, có thể bạn sẽ không muốn cài đặt các binary free-threaded vào lúc này.

Để chỉ định tùy chọn cài đặt trên command line, hãy sử dụng ``Include_freethreaded=1``. Xem :ref:`install-layout-option` để biết hướng dẫn tải trước các binary bổ sung nhằm cài đặt ngoại tuyến. Các tùy chọn bao gồm symbol debug và binary cũng áp dụng cho các bản build free-threaded.

Các binary free-threaded cũng có sẵn :ref:`trên nuget.org <windows-nuget>`.


Python launcher cho Windows (đã lỗi thời)
=========================================

.. deprecated:: 3.14

   Launcher và tài liệu này đã được thay thế bởi Python Install Manager được mô tả ở trên. Nội dung này tạm thời được giữ lại để tham khảo lịch sử.

.. versionadded:: 3.3

Python launcher cho Windows là một tiện ích hỗ trợ xác định vị trí và thực thi các phiên bản Python khác nhau. Tiện ích này cho phép các script (hoặc command line) chỉ ra phiên bản Python cụ thể được ưu tiên, rồi xác định vị trí và thực thi phiên bản đó.

Không giống biến :envvar:`PATH`, launcher sẽ chọn chính xác phiên bản Python phù hợp nhất. Launcher sẽ ưu tiên các bản cài đặt theo từng người dùng hơn các bản cài đặt trên toàn hệ thống, đồng thời sắp xếp theo phiên bản ngôn ngữ thay vì sử dụng phiên bản được cài đặt gần đây nhất.

Launcher ban đầu được đặc tả trong :pep:`397`.

Bắt đầu
-------

Từ dòng lệnh
^^^^^^^^^^^^

.. versionchanged:: 3.6

Các bản cài đặt Python 3.3 trở lên trên toàn hệ thống sẽ đặt launcher vào
:envvar:`PATH`. Launcher tương thích với mọi phiên bản Python hiện có, vì vậy phiên bản nào được cài đặt cũng không quan trọng. Để kiểm tra launcher có khả dụng hay không, hãy thực thi lệnh sau trong Command Prompt::

  py

Bạn sẽ thấy phiên bản Python mới nhất đã cài đặt được khởi chạy - bạn có thể thoát như bình thường, và mọi đối số dòng lệnh bổ sung được chỉ định sẽ được chuyển trực tiếp đến Python.

Nếu bạn đã cài đặt nhiều phiên bản Python (ví dụ: 3.7 và |version|), bạn sẽ nhận thấy rằng Python |version| đã được khởi động - để khởi động Python 3.7, hãy thử lệnh::

  py -3.7

Nếu bạn muốn sử dụng phiên bản Python 2 mới nhất đã được cài đặt, hãy thử lệnh::

  py -2

Nếu bạn thấy lỗi sau, nghĩa là bạn chưa cài đặt launcher::

  'py' is not recognized as an internal or external command,
  operable program or batch file.

Lệnh::

  py --list

hiển thị (các) phiên bản Python hiện đang được cài đặt.

Đối số ``-x.y`` là dạng viết ngắn của đối số ``-V:Company/Tag``, cho phép chọn một runtime Python cụ thể, bao gồm cả những runtime có thể đến từ nơi khác ngoài python.org. Mọi runtime được đăng ký bằng cách làm theo
:pep:`514` sẽ có thể được phát hiện. Lệnh ``--list`` liệt kê tất cả runtime khả dụng bằng định dạng ``-V:``.

Khi sử dụng đối số ``-V:``, việc chỉ định Company sẽ giới hạn lựa chọn ở các runtime từ nhà cung cấp đó, còn chỉ chỉ định Tag sẽ cho phép lựa chọn từ tất cả nhà cung cấp. Lưu ý rằng việc bỏ qua dấu gạch chéo ngầm định đó là một tag::

  # Select any '3.*' tagged runtime
  py -V:3

  # Select any 'PythonCore' released runtime
  py -V:PythonCore/

  # Select PythonCore's latest Python 3 runtime
  py -V:PythonCore/3

Dạng ngắn của đối số (``-3``) chỉ chọn các bản phát hành Python lõi, không chọn các bản phân phối khác. Tuy nhiên, dạng dài hơn (``-V:3``) sẽ chọn từ bất kỳ bản nào.

Company được đối sánh với toàn bộ chuỗi, không phân biệt chữ hoa chữ thường. Tag được đối sánh với toàn bộ chuỗi hoặc một tiền tố, miễn là ký tự tiếp theo là dấu chấm hoặc dấu gạch nối. Điều này cho phép ``-V:3.1`` khớp với ``3.1-32``, nhưng không khớp với ``3.10``. Các Tag được sắp xếp theo thứ tự số (``3.10`` mới hơn ``3.1``), nhưng được so sánh dưới dạng văn bản (``-V:3.01`` không khớp với ``3.1``).


Môi trường ảo
^^^^^^^^^^^^^

.. versionadded:: 3.5

Nếu launcher được chạy mà không chỉ định rõ phiên bản Python, và một môi trường ảo (được tạo bằng module :mod:`venv` thuộc standard library hoặc công cụ ``virtualenv`` bên ngoài) đang hoạt động, launcher sẽ chạy interpreter của môi trường ảo thay vì interpreter toàn cục. Để chạy interpreter toàn cục, hãy hủy kích hoạt môi trường ảo hoặc chỉ định rõ phiên bản Python toàn cục.

Từ một script
^^^^^^^^^^^^^

Hãy tạo một script Python thử nghiệm - tạo một tệp có tên ``hello.py`` với nội dung sau

.. code-block:: python

    #! python
    import sys
    sys.stdout.write("hello from Python %s\n" % (sys.version,))

Từ thư mục chứa hello.py, hãy thực thi lệnh::

   py hello.py

Bạn sẽ thấy số phiên bản của bản cài đặt Python 2.x mới nhất được in ra. Bây giờ hãy thử thay đổi dòng đầu tiên thành:

.. code-block:: python

    #! python3

Việc thực thi lại lệnh giờ đây sẽ in ra thông tin Python 3.x mới nhất. Cũng như các ví dụ dòng lệnh ở trên, bạn có thể chỉ định bộ định tính phiên bản cụ thể hơn. Giả sử bạn đã cài đặt Python 3.7, hãy thử thay đổi dòng đầu tiên thành ``#! python3.7`` và bạn sẽ thấy thông tin phiên bản 3.7 được in ra.

Lưu ý rằng, không giống như khi sử dụng tương tác, "python" không kèm đối số sẽ sử dụng phiên bản Python 2.x mới nhất mà bạn đã cài đặt. Điều này nhằm đảm bảo khả năng tương thích ngược và khả năng tương thích với Unix, nơi lệnh ``python`` thường chỉ Python 2.

Từ liên kết tệp
^^^^^^^^^^^^^^^

Trình khởi chạy lẽ ra đã được liên kết với các tệp Python (tức là các tệp ``.py``, ``.pyw``, ``.pyc``) khi được cài đặt. Điều này có nghĩa là khi bạn bấm đúp vào một trong các tệp này từ Windows Explorer, trình khởi chạy sẽ được sử dụng; do đó, bạn có thể sử dụng các tính năng tương tự được mô tả ở trên để tập lệnh chỉ định phiên bản cần sử dụng.

Lợi ích chính của cách này là một trình khởi chạy duy nhất có thể hỗ trợ đồng thời nhiều phiên bản Python, tùy thuộc vào nội dung của dòng đầu tiên.

Các dòng shebang
----------------

Nếu dòng đầu tiên của một tệp script bắt đầu bằng ``#!``, dòng đó được gọi là dòng "shebang". Linux và các hệ điều hành tương tự Unix có hỗ trợ gốc cho những dòng này, và chúng thường được sử dụng trên các hệ thống đó để cho biết cách thực thi một script. Trình khởi chạy này cho phép sử dụng các tính năng tương tự với các script Python trên Windows, và các ví dụ ở trên minh họa cách sử dụng chúng.

Để cho phép các dòng shebang trong script Python có thể hoạt động linh hoạt giữa Unix và Windows, trình khởi chạy này hỗ trợ một số lệnh 'ảo' để chỉ định interpreter cần sử dụng. Các lệnh ảo được hỗ trợ là:

* ``/usr/bin/env``
* ``/usr/bin/python``
* ``/usr/local/bin/python``
* ``python``

Ví dụ: nếu dòng đầu tiên trong script của bạn bắt đầu bằng

.. code-block:: sh

  #! /usr/bin/python

Python mặc định hoặc virtual environment đang hoạt động sẽ được tìm thấy và sử dụng. Vì nhiều script Python được viết để hoạt động trên Unix đã có sẵn dòng này, bạn có thể sử dụng các script đó với launcher mà không cần sửa đổi. Nếu bạn đang viết một script mới trên Windows và hy vọng script đó sẽ hữu ích trên Unix, bạn nên sử dụng một trong các dòng shebang bắt đầu bằng ``/usr``.

Bất kỳ lệnh ảo nào ở trên cũng có thể được thêm hậu tố là một phiên bản cụ thể (chỉ phiên bản chính hoặc cả phiên bản chính và phiên bản phụ). Ngoài ra, có thể yêu cầu phiên bản 32-bit bằng cách thêm "-32" sau phiên bản phụ. Tức là ``/usr/bin/python3.7-32`` sẽ yêu cầu sử dụng Python 3.7 32-bit. Nếu một môi trường ảo đang hoạt động, phiên bản sẽ bị bỏ qua và môi trường đó sẽ được sử dụng.

.. versionadded:: 3.7

   Bắt đầu từ python launcher 3.7, có thể yêu cầu phiên bản 64-bit bằng hậu tố "-64". Ngoài ra, có thể chỉ định phiên bản chính và kiến trúc mà không cần phiên bản phụ (tức là ``/usr/bin/python3-64``).

.. versionchanged:: 3.11

   Hậu tố "-64" không còn được khuyến nghị và hiện có nghĩa là "bất kỳ kiến trúc nào không được chứng minh là i386/32-bit". Để yêu cầu một môi trường cụ thể, hãy sử dụng dạng mới
   đối số :samp:`-V:{TAG}` cùng với thẻ hoàn chỉnh.

.. versionchanged:: 3.13

   Các lệnh ảo tham chiếu đến ``python`` giờ đây ưu tiên một môi trường ảo đang hoạt động thay vì tìm kiếm :envvar:`PATH`. Điều này xử lý các trường hợp shebang chỉ định ``/usr/bin/env python3`` nhưng :file:`python3.exe` không có trong môi trường đang hoạt động.

Dạng ``/usr/bin/env`` của dòng shebang còn có một thuộc tính đặc biệt khác. Trước khi tìm các trình thông dịch Python đã cài đặt, dạng này sẽ tìm trong tệp thực thi :envvar:`PATH` một tệp thực thi Python khớp với tên được cung cấp làm đối số đầu tiên. Điều này tương ứng với hành vi của chương trình Unix ``env``, chương trình thực hiện việc tìm kiếm :envvar:`PATH`. Nếu không tìm thấy tệp thực thi khớp với đối số đầu tiên sau lệnh ``env``, nhưng đối số đó bắt đầu bằng ``python``, nó sẽ được xử lý như mô tả đối với các lệnh ảo khác. Có thể đặt biến môi trường :envvar:`!PYLAUNCHER_NO_SEARCH_PATH` (thành bất kỳ giá trị nào) để bỏ qua việc tìm kiếm này trong :envvar:`PATH`.

Các dòng shebang không khớp với bất kỳ mẫu nào trong số này sẽ được tra cứu trong mục ``[commands]`` của launcher’s :ref:`.INI file <launcher-ini>`. Bạn có thể dùng mục này để xử lý một số lệnh theo cách phù hợp với hệ thống của mình. Tên lệnh phải là một đối số duy nhất (không có khoảng trắng trong tệp thực thi shebang), và giá trị được thay thế là đường dẫn đầy đủ đến tệp thực thi (các đối số bổ sung được chỉ định trong .INI sẽ được đặt trong dấu ngoặc kép như một phần của tên tệp).

.. code-block:: ini

   [commands]
   /bin/xpython=C:\Program Files\XPython\python.exe

Mọi lệnh không tìm thấy trong tệp .INI đều được coi là các đường dẫn đến tệp thực thi **Windows** tuyệt đối hoặc tương đối so với thư mục chứa tệp script. Đây là một tiện ích dành cho các script chỉ chạy trên Windows, chẳng hạn như những script do trình cài đặt tạo ra, vì hành vi này không tương thích với các shell kiểu Unix. Các đường dẫn này có thể được đặt trong dấu ngoặc kép và có thể bao gồm nhiều đối số; sau đó, đường dẫn đến script cùng mọi đối số bổ sung sẽ được nối thêm.


Các đối số trong dòng shebang
-----------------------------

Các dòng shebang cũng có thể chỉ định các tùy chọn bổ sung để truyền cho trình thông dịch Python. Ví dụ, nếu bạn có một dòng shebang:

.. code-block:: sh

  #! /usr/bin/python -v

Khi đó Python sẽ được khởi động với tùy chọn ``-v``

Tùy chỉnh
---------

.. _launcher-ini:

Tùy chỉnh thông qua các tệp INI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trình khởi chạy sẽ tìm kiếm hai tệp .ini - ``py.ini`` trong thư mục dữ liệu ứng dụng của người dùng hiện tại (``%LOCALAPPDATA%`` hoặc ``$env:LocalAppData``) và ``py.ini`` trong cùng thư mục với trình khởi chạy. Các tệp .ini giống nhau được sử dụng cho cả phiên bản 'console' của trình khởi chạy (tức là py.exe) và phiên bản 'windows' (tức là pyw.exe).

Tùy chỉnh được chỉ định trong "thư mục ứng dụng" sẽ được ưu tiên hơn tùy chỉnh nằm cạnh tệp thực thi, vì vậy người dùng không có quyền ghi vào tệp .ini cạnh trình khởi chạy vẫn có thể ghi đè các lệnh trong tệp .ini toàn cục đó.

Tùy chỉnh các phiên bản Python mặc định
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trong một số trường hợp, có thể đưa qualifier phiên bản vào một command để chỉ định phiên bản Python mà command sẽ sử dụng. Qualifier phiên bản bắt đầu bằng số phiên bản major và có thể tùy chọn được theo sau bởi dấu chấm ('.') và mã chỉ định phiên bản minor. Ngoài ra, có thể chỉ định yêu cầu implementation 32 hoặc 64 bit bằng cách thêm "-32" hoặc "-64".

Ví dụ: dòng shebang ``#!python`` không có qualifier phiên bản, trong khi ``#!python3`` có qualifier phiên bản chỉ chỉ định phiên bản major.

Nếu không tìm thấy qualifier phiên bản nào trong một command, có thể đặt biến môi trường :envvar:`!PY_PYTHON` để chỉ định qualifier phiên bản mặc định. Nếu biến này chưa được đặt, giá trị mặc định là "3". Biến này có thể chỉ định bất kỳ giá trị nào có thể được truyền trên command line, chẳng hạn như "3", "3.7", "3.7-32" hoặc "3.7-64". (Lưu ý rằng tùy chọn "-64" chỉ khả dụng với launcher đi kèm Python 3.7 trở lên.)

Nếu không tìm thấy qualifier phiên bản minor nào, có thể đặt biến môi trường ``PY_PYTHON{major}`` (trong đó ``{major}`` là qualifier phiên bản major hiện tại được xác định như trên) để chỉ định phiên bản đầy đủ. Nếu không tìm thấy tùy chọn như vậy, launcher sẽ liệt kê các phiên bản Python đã cài đặt và sử dụng bản phát hành minor mới nhất được tìm thấy cho phiên bản major đó; nhiều khả năng, dù không được đảm bảo, đây là phiên bản được cài đặt gần đây nhất trong nhóm phiên bản đó.

Trên Windows 64 bit khi đã cài đặt cả implementation 32 bit và 64 bit của cùng một phiên bản Python (major.minor), phiên bản 64 bit sẽ luôn được ưu tiên. Điều này đúng với cả launcher 32 bit và 64 bit - launcher 32 bit sẽ ưu tiên thực thi bản cài đặt Python 64 bit của phiên bản được chỉ định nếu có. Cách này giúp có thể dự đoán hành vi của launcher chỉ dựa trên các phiên bản đã cài đặt trên PC mà không phụ thuộc vào thứ tự cài đặt (tức là không cần biết phiên bản Python 32 hay 64 bit và launcher tương ứng được cài đặt sau cùng). Như đã lưu ý ở trên, có thể sử dụng hậu tố "-32" hoặc "-64" tùy chọn trong mã chỉ định phiên bản để thay đổi hành vi này.

Ví dụ:

* Nếu không đặt tùy chọn liên quan nào, các command ``python`` và ``python2`` sẽ sử dụng phiên bản Python 2.x mới nhất đã cài đặt, còn command ``python3`` sẽ sử dụng phiên bản Python 3.x mới nhất đã cài đặt.

* Lệnh ``python3.7`` sẽ hoàn toàn không tham chiếu đến bất kỳ tùy chọn nào vì các phiên bản đã được chỉ định đầy đủ.

* Nếu ``PY_PYTHON=3``, các lệnh ``python`` và ``python3`` đều sẽ sử dụng phiên bản Python 3 mới nhất đã được cài đặt.

* Nếu ``PY_PYTHON=3.7-32``, lệnh ``python`` sẽ sử dụng bản triển khai 32-bit của 3.7, trong khi lệnh ``python3`` sẽ sử dụng phiên bản Python mới nhất đã được cài đặt (PY_PYTHON hoàn toàn không được xem xét vì một phiên bản chính đã được chỉ định.)

* Nếu ``PY_PYTHON=3`` và ``PY_PYTHON3=3.7``, các lệnh ``python`` và ``python3`` đều sẽ sử dụng cụ thể phiên bản 3.7

Ngoài các biến môi trường, bạn cũng có thể cấu hình các thiết lập tương tự trong tệp .INI được launcher sử dụng. Phần trong tệp INI có tên là ``[defaults]`` và tên khóa sẽ giống với các biến môi trường nhưng không có tiền tố ``PY_`` ở đầu (lưu ý rằng tên khóa trong tệp INI không phân biệt chữ hoa chữ thường). Nội dung của một biến môi trường sẽ ghi đè các thiết lập được chỉ định trong tệp INI.

Ví dụ:

* Việc đặt ``PY_PYTHON=3.7`` tương đương với việc tệp INI chứa:

.. code-block:: ini

  [defaults]
  python=3.7

* Việc thiết lập ``PY_PYTHON=3`` và ``PY_PYTHON3=3.7`` tương đương với việc tệp INI chứa:

.. code-block:: ini

  [defaults]
  python=3
  python3=3.7

Chẩn đoán
---------

Nếu biến môi trường :envvar:`!PYLAUNCHER_DEBUG` được thiết lập (với bất kỳ giá trị nào), launcher sẽ in thông tin chẩn đoán ra stderr (tức là ra console). Mặc dù thông tin này vừa dài dòng *và* vừa ngắn gọn, thông tin này vẫn cho phép bạn xem những phiên bản Python nào đã được tìm thấy, lý do một phiên bản cụ thể được chọn và command-line chính xác được dùng để thực thi Python đích. Thông tin này chủ yếu nhằm phục vụ việc kiểm thử và gỡ lỗi.

Chạy thử
--------

Nếu biến môi trường :envvar:`!PYLAUNCHER_DRYRUN` được thiết lập (với bất kỳ giá trị nào), launcher sẽ xuất command mà nó sẽ chạy, nhưng sẽ không thực sự khởi chạy Python. Điều này có thể hữu ích cho các công cụ muốn sử dụng launcher để phát hiện rồi khởi chạy Python trực tiếp. Lưu ý rằng command được ghi ra standard output luôn được mã hóa bằng UTF-8 và có thể không hiển thị chính xác trong console.

Cài đặt theo yêu cầu
--------------------

Nếu biến môi trường :envvar:`!PYLAUNCHER_ALLOW_INSTALL` được thiết lập (với bất kỳ giá trị nào) và phiên bản Python được yêu cầu chưa được cài đặt nhưng có sẵn trên Microsoft Store, launcher sẽ cố gắng cài đặt phiên bản đó. Quá trình này có thể yêu cầu người dùng tương tác để hoàn tất và bạn có thể cần chạy lại command.

Một biến :envvar:`!PYLAUNCHER_ALWAYS_INSTALL` bổ sung khiến launcher luôn cố gắng cài đặt Python, ngay cả khi Python đã được phát hiện. Biến này chủ yếu dành cho việc kiểm thử (và nên được sử dụng cùng với :envvar:`!PYLAUNCHER_DRYRUN`).

Mã trả về
---------

Python launcher có thể trả về các mã thoát sau. Đáng tiếc là không có cách nào phân biệt các mã này với mã thoát của chính Python.

Tên của các mã được sử dụng trong mã nguồn và chỉ nhằm mục đích tham khảo. Không có cách nào truy cập hoặc tra cứu chúng ngoài việc đọc trang này. Các mục được liệt kê theo thứ tự bảng chữ cái của tên.

+-------------------+---------+-----------------------------------------------------------------------------+
| Tên               | Giá trị | Mô tả                                                                       |
+===================+=========+=============================================================================+
| RC_BAD_VENV_CFG   | 107     | Đã tìm thấy một :file:`pyvenv.cfg` nhưng nó bị hỏng.                        |
+-------------------+---------+-----------------------------------------------------------------------------+
| RC_CREATE_PROCESS | 101     | Không thể khởi chạy Python.                                                 |
+-------------------+---------+-----------------------------------------------------------------------------+
| RC_INSTALLING     | 111     | Đã bắt đầu cài đặt, nhưng cần chạy lại lệnh sau khi quá trình này hoàn tất. |
+-------------------+---------+-----------------------------------------------------------------------------+
| RC_INTERNAL_ERROR | 109     | Đã xảy ra lỗi không mong muốn. Vui lòng báo lỗi.                            |
+-------------------+---------+-----------------------------------------------------------------------------+
| RC_NO_COMMANDLINE | 108     | Không thể lấy command line từ hệ điều hành.                                 |
+-------------------+---------+-----------------------------------------------------------------------------+
| RC_NO_PYTHON      | 103     | Không thể tìm thấy phiên bản được yêu cầu.                                  |
+-------------------+---------+-----------------------------------------------------------------------------+
| RC_NO_VENV_CFG    | 106     | Đã yêu cầu :file:`pyvenv.cfg` nhưng không tìm thấy.                         |
+-------------------+---------+-----------------------------------------------------------------------------+

.. _`our bug tracker`: https://github.com/python/pymanager/issues
.. _`nuget.org`: https://www.nuget.org/
.. _`www.nuget.org/packages/python`: https://www.nuget.org/packages/python
.. _`www.nuget.org/packages/pythonx86`: https://www.nuget.org/packages/pythonx86
.. _`www.nuget.org/packages/pythonarm64`: https://www.nuget.org/packages/pythonarm64
.. _`python-freethreaded`: https://www.nuget.org/packages/python-freethreaded
.. _`pythonx86-freethreaded`: https://www.nuget.org/packages/pythonx86-freethreaded
.. _`pythonarm64-freethreaded`: https://www.nuget.org/packages/pythonarm64-freethreaded
.. _`ActivePython`: https://www.activestate.com/products/python/
.. _`Anaconda`: https://www.anaconda.com/download/
.. _`Enthought Deployment Manager`: https://assets.enthought.com/downloads/edm/
.. _`reached end of life in 2016`: https://support.enthought.com/hc/en-us/articles/360038600051-Canopy-GUI-end-of-life-transition-to-the-Enthought-Deployment-Manager-EDM-and-Visual-Studio-Code
.. _`WinPython`: https://winpython.github.io/
.. _`Component Object Model`: https://learn.microsoft.com/windows/win32/com/component-object-model--com--portal
.. _`Microsoft Foundation Classes`: https://learn.microsoft.com/cpp/mfc/mfc-desktop-applications
.. _`PythonWin`: https://web.archive.org/web/20060524042422/ https://www.python.org/windows/pythonwin/
.. _`Win32 How Do I...?`: https://timgolden.me.uk/python/win32_how_do_i.html
.. _`Python and COM`: https://www.boddie.org.uk/python/COM.html
.. _`cx_Freeze`: https://cx-freeze.readthedocs.io/en/latest/
.. _`source`: https://www.python.org/downloads/source/
.. _`checkout`: https://devguide.python.org/setup/#get-the-source-code
