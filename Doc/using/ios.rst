.. _using-ios:

=======================
Sử dụng Python trên iOS
=======================

:Authors:Russell Keith-Magee (2024-03)

Python trên iOS không giống Python trên các nền tảng desktop. Trên nền tảng desktop, Python thường được cài đặt như một tài nguyên hệ thống mà bất kỳ người dùng nào của máy tính đó cũng có thể sử dụng. Sau đó, người dùng tương tác với Python bằng cách chạy tệp thực thi :program:`python` và nhập lệnh tại dấu nhắc tương tác, hoặc bằng cách chạy một tập lệnh Python.

Trên iOS, không có khái niệm cài đặt dưới dạng tài nguyên hệ thống. Đơn vị phân phối phần mềm duy nhất là một "app". Ngoài ra, không có console nơi bạn có thể chạy tệp thực thi :program:`python` hoặc tương tác với Python REPL.

Do đó, cách duy nhất để sử dụng Python trên iOS là ở chế độ nhúng - tức là viết một ứng dụng iOS native, nhúng trình thông dịch Python bằng ``libPython``, rồi gọi mã Python bằng :ref:`Python embedding API <embedding>`. Toàn bộ trình thông dịch Python, thư viện chuẩn và tất cả mã Python của bạn sau đó được đóng gói thành một bundle độc lập có thể được phân phối thông qua iOS App Store.

Nếu bạn muốn lần đầu thử viết một app iOS bằng Python, các dự án như `BeeWare <https://beeware.org>`__ và `Kivy <https://kivy.org>`__ sẽ mang đến trải nghiệm thân thiện hơn nhiều. Các dự án này xử lý những phức tạp liên quan đến việc chạy một dự án iOS, vì vậy bạn chỉ cần tập trung vào chính mã Python.

Python trong runtime trên iOS
=============================

Khả năng tương thích phiên bản iOS
----------------------------------

Phiên bản iOS tối thiểu được hỗ trợ được chỉ định tại thời điểm biên dịch bằng cách sử dụng
:option:`--host` để ``configure``. Theo mặc định, khi được biên dịch cho iOS, Python sẽ được biên dịch với phiên bản iOS tối thiểu được hỗ trợ là 13.0. Để sử dụng phiên bản iOS tối thiểu khác, hãy cung cấp số phiên bản trong
:option:`!--host` argument - ví dụ: ``--host=arm64-apple-ios15.4-simulator`` sẽ biên dịch một bản dựng trình mô phỏng ARM64 với deployment target là 15.4.

Nhận diện nền tảng
------------------

Khi chạy trên iOS, ``sys.platform`` sẽ báo cáo là ``ios``. Giá trị này sẽ được trả về trên iPhone hoặc iPad, bất kể ứng dụng đang chạy trên trình mô phỏng hay thiết bị vật lý.

Có thể lấy thông tin về môi trường runtime cụ thể, bao gồm phiên bản iOS, model thiết bị và việc thiết bị có phải là trình mô phỏng hay không, bằng cách sử dụng
:func:`platform.ios_ver`. :func:`platform.system` sẽ báo cáo ``iOS`` hoặc ``iPadOS``, tùy thuộc vào thiết bị.

:func:`os.uname` báo cáo các chi tiết ở cấp kernel; nó sẽ báo cáo tên là ``Darwin``.

Tính khả dụng của thư viện chuẩn
--------------------------------

Thư viện chuẩn Python có một số thiếu sót và hạn chế đáng chú ý trên iOS. Xem :ref:`hướng dẫn về tính khả dụng của API cho iOS <mobile-availability>` để biết chi tiết.

Các module mở rộng nhị phân
---------------------------

Một điểm khác biệt đáng chú ý của iOS với tư cách là một nền tảng là việc phân phối qua App Store đặt ra các yêu cầu bắt buộc nghiêm ngặt đối với việc đóng gói ứng dụng. Một trong những yêu cầu này quy định cách phân phối các module mở rộng nhị phân.

App Store của iOS yêu cầu *tất cả* các module nhị phân trong một ứng dụng iOS phải là thư viện động, được chứa trong một framework có metadata phù hợp và được lưu trong thư mục ``Frameworks`` của ứng dụng đã đóng gói. Mỗi framework chỉ được có một binary duy nhất và không được có tài liệu binary thực thi nào bên ngoài thư mục ``Frameworks``.

Điều này xung đột với cách tiếp cận thông thường của Python trong việc phân phối các tệp nhị phân, vốn cho phép tải một binary extension module từ bất kỳ vị trí nào trên ``sys.path``. Để đảm bảo tuân thủ các chính sách của App Store, một dự án iOS phải hậu xử lý mọi package Python, chuyển đổi các binary module trên ``.so`` thành các framework độc lập riêng lẻ với metadata và chữ ký phù hợp. Để biết chi tiết về cách thực hiện bước hậu xử lý này, hãy xem hướng dẫn :ref:`thêm Python vào dự án của bạn <adding-ios>`.

Để giúp Python tìm các tệp nhị phân ở vị trí mới, tệp ``.so`` ban đầu trên ``sys.path`` được thay thế bằng một tệp ``.fwork``. Đây là một tệp văn bản chứa vị trí của binary framework, tính tương đối so với app bundle. Để cho phép framework phân giải ngược về vị trí ban đầu, framework phải chứa một tệp ``.origin`` có chứa vị trí của tệp ``.fwork``, tính tương đối so với app bundle.

Ví dụ, hãy xét trường hợp import ``from foo.bar import _whiz``, trong đó ``_whiz`` được triển khai bằng binary module ``sources/foo/bar/_whiz.abi3.so``, với ``sources`` là vị trí được đăng ký trên ``sys.path``, tính tương đối so với application bundle. Module này *phải* được phân phối dưới dạng ``Frameworks/foo.bar._whiz.framework/foo.bar._whiz`` (tạo tên framework từ full import path của module), với một tệp ``Info.plist`` trong thư mục ``.framework`` để xác định binary là một framework. Module ``foo.bar._whiz`` sẽ được biểu diễn tại vị trí ban đầu bằng một tệp marker ``sources/foo/bar/_whiz.abi3.fwork``, chứa đường dẫn ``Frameworks/foo.bar._whiz/foo.bar._whiz``. Framework cũng sẽ chứa ``Frameworks/foo.bar._whiz.framework/foo.bar._whiz.origin``, chứa đường dẫn đến tệp ``.fwork``.

Khi chạy trên iOS, trình thông dịch Python sẽ cài đặt một
:class:`~importlib.machinery.AppleFrameworkLoader` có khả năng đọc và import các tệp ``.fwork``. Sau khi được import, thuộc tính ``__file__`` của binary module sẽ báo cáo vị trí của tệp ``.fwork``. Tuy nhiên,
:class:`~importlib.machinery.ModuleSpec` của module đã tải sẽ báo cáo ``origin`` là vị trí của binary trong thư mục framework.

Các binary stub của compiler
----------------------------

Xcode không cung cấp các trình biên dịch cụ thể cho iOS; thay vào đó, nó sử dụng một script ``xcrun`` để phân giải thành đường dẫn đầy đủ đến trình biên dịch (ví dụ: ``xcrun --sdk iphoneos clang`` để lấy ``clang`` cho một thiết bị iPhone). Tuy nhiên, việc sử dụng script này đặt ra hai vấn đề:

* Đầu ra của ``xcrun`` bao gồm các đường dẫn dành riêng cho từng máy, dẫn đến một module sysconfig không thể được chia sẻ giữa những người dùng; và

* Nó tạo ra các định nghĩa ``CC``/``CPP``/``LD``/``AR`` có chứa khoảng trắng. Nhiều công cụ trong hệ sinh thái C giả định rằng bạn có thể tách một dòng lệnh tại khoảng trắng đầu tiên để lấy đường dẫn đến tệp thực thi của trình biên dịch; điều này không đúng khi sử dụng ``xcrun``.

Để tránh những vấn đề này, Python cung cấp các stub cho những công cụ này. Các stub này là những shell script wrapper quanh các công cụ ``xcrun`` nền tảng, được phân phối trong một thư mục ``bin`` đi kèm với iOS framework đã biên dịch. Các script này có thể được di chuyển và luôn phân giải đến các đường dẫn hệ thống cục bộ thích hợp. Bằng cách đưa các script này vào thư mục bin đi kèm với một framework, nội dung của module ``sysconfig`` trở nên hữu ích cho người dùng cuối khi biên dịch các module của riêng họ. Khi biên dịch các module Python của bên thứ ba cho iOS, bạn nên đảm bảo các stub binary này nằm trong path của mình.

Cài đặt Python trên iOS
=======================

Các công cụ để xây dựng ứng dụng iOS
------------------------------------

Việc xây dựng cho iOS yêu cầu sử dụng bộ công cụ Xcode của Apple. Bạn nên sử dụng bản phát hành ổn định mới nhất của Xcode. Điều này đòi hỏi phải sử dụng phiên bản macOS được phát hành gần đây nhất (hoặc gần đây thứ hai), vì Apple không duy trì Xcode cho các phiên bản macOS cũ hơn. Xcode Command Line Tools không đủ để phát triển iOS; bạn cần một bản cài đặt Xcode *full*.

Nếu muốn chạy mã của mình trên trình mô phỏng iOS, bạn cũng cần cài đặt iOS Simulator Platform. Bạn sẽ được nhắc chọn iOS Simulator Platform khi chạy Xcode lần đầu. Ngoài ra, bạn có thể thêm iOS Simulator Platform bằng cách chọn trong tab Platforms của bảng Xcode Settings.

.. _adding-ios:

Thêm Python vào dự án iOS
-------------------------

Có thể thêm Python vào bất kỳ dự án iOS nào bằng Swift hoặc Objective C. Các ví dụ sau sẽ sử dụng Objective C; nếu bạn dùng Swift, một thư viện như `PythonKit <https://github.com/pvieito/PythonKit>`__ có thể hữu ích.

Để thêm Python vào một dự án iOS trong Xcode:

1. Tạo hoặc lấy một bản dựng Python ``XCFramework``. Xem hướng dẫn trong
   :source:`Apple/iOS/README.md` (trong bản phân phối mã nguồn CPython) để biết chi tiết về cách tạo một ``XCFramework`` Python. Tối thiểu, bạn sẽ cần một bản dựng hỗ trợ ``arm64-apple-ios``, cùng với một trong hai tùy chọn ``arm64-apple-ios-simulator`` hoặc ``x86_64-apple-ios-simulator``.

2. Kéo ``XCframework`` vào dự án iOS của bạn. Trong các hướng dẫn sau, chúng tôi giả định rằng bạn đã thả ``XCframework`` vào thư mục gốc của dự án; tuy nhiên, bạn có thể sử dụng bất kỳ vị trí nào khác bằng cách điều chỉnh các đường dẫn cho phù hợp.

3. Thêm mã ứng dụng của bạn dưới dạng một thư mục trong dự án Xcode. Trong các hướng dẫn sau, chúng tôi giả định rằng mã người dùng của bạn nằm trong một thư mục có tên ``app`` ở thư mục gốc của dự án; bạn có thể sử dụng vị trí khác bằng cách điều chỉnh các đường dẫn khi cần. Đảm bảo rằng thư mục này được liên kết với app target của bạn.

4. Chọn app target bằng cách chọn node gốc của dự án Xcode, sau đó chọn tên target trong sidebar xuất hiện.

5. Trong cài đặt "General", bên dưới "Frameworks, Libraries and Embedded Content", hãy thêm ``Python.xcframework``, với tùy chọn "Embed & Sign" được chọn.

6. Trong tab "Build Settings", hãy sửa đổi các mục sau:

   - Build Options

     * User Script Sandboxing: No
     * Enable Testability: Yes

   - Search Paths

     * Framework Search Paths: ``$(PROJECT_DIR)``
     * Header Search Paths: ``"$(BUILT_PRODUCTS_DIR)/Python.framework/Headers"``

   - Apple Clang - Warnings - All languages

     * Quoted Include In Framework Header: No

7. Thêm một bước build để xử lý Python standard library và các binary dependency Python của riêng bạn. Trong tab "Build Phases", thêm một bước build "Run Script" mới *before* bước "Embed Frameworks", nhưng *after* bước "Copy Bundle Resources". Đặt tên cho bước này là "Process Python libraries", bỏ chọn checkbox "Based on dependency analysis", rồi đặt nội dung script là:

   .. code-block:: bash

      set -e
      source $PROJECT_DIR/Python.xcframework/build/build_utils.sh
      install_python Python.xcframework app

   Nếu bạn đã đặt XCframework ở vị trí khác với thư mục gốc của project, hãy sửa đường dẫn đến đối số đầu tiên.

8. Thêm mã Objective-C để khởi tạo và sử dụng trình thông dịch Python ở chế độ nhúng. Bạn nên đảm bảo rằng:

   * Chế độ UTF-8 (:c:member:`PyPreConfig.utf8_mode`) được *bật*;
   * stdio có bộ đệm (:c:member:`PyConfig.buffered_stdio`) được *tắt*;
   * Việc ghi bytecode (:c:member:`PyConfig.write_bytecode`) được *tắt*;
   * Các trình xử lý tín hiệu (:c:member:`PyConfig.install_signal_handlers`) được *bật*;
   * Ghi nhật ký hệ thống (:c:member:`PyConfig.use_system_logger`) được *bật* (tùy chọn nhưng rất được khuyến nghị; tính năng này được bật theo mặc định);
   * :envvar:`PYTHONHOME` cho trình thông dịch được cấu hình để trỏ đến thư mục con ``python`` trong bundle của ứng dụng; và
   * :envvar:`PYTHONPATH` dành cho interpreter bao gồm:

     - thư mục con ``python/lib/python3.X`` của bundle ứng dụng,
     - thư mục con ``python/lib/python3.X/lib-dynload`` của bundle ứng dụng, và
     - thư mục con ``app`` của bundle ứng dụng

   Có thể xác định vị trí bundle của ứng dụng bằng ``[[NSBundle mainBundle] resourcePath]``.

Bước 7 và 8 trong các hướng dẫn này giả định rằng bạn có một thư mục duy nhất chứa mã ứng dụng Python thuần túy, có tên là ``app``. Nếu ứng dụng của bạn có các module nhị phân của bên thứ ba, bạn sẽ cần thực hiện thêm một số bước:

* Bạn cần đảm bảo rằng mọi thư mục chứa các tệp nhị phân của bên thứ ba либо được liên kết với app target, либо được sao chép rõ ràng như một phần của bước 7. Bước 7 cũng cần loại bỏ mọi tệp nhị phân không phù hợp với nền tảng mà một bản build cụ thể đang nhắm đến (tức là xóa các tệp nhị phân dành cho thiết bị nếu bạn đang build một ứng dụng nhắm đến simulator).

* Nếu bạn đang sử dụng một thư mục riêng cho các package bên thứ ba, hãy đảm bảo thư mục đó được thêm vào cuối lệnh gọi tới ``install_python`` ở bước 7 và được thêm vào cấu hình :envvar:`PYTHONPATH` ở bước 8.

* Nếu bất kỳ thư mục nào chứa các package bên thứ ba sẽ chứa các tệp ``.pth``, bạn nên thêm thư mục đó dưới dạng thư mục *site directory* (bằng cách sử dụng
  :meth:`site.addsitedir`), thay vì thêm vào :envvar:`PYTHONPATH` hoặc
  :attr:`sys.path` trực tiếp.

Kiểm thử một package Python
---------------------------

Cây mã nguồn CPython chứa :source:`a testbed project <Apple/iOS/testbed>`, được sử dụng để chạy bộ kiểm thử CPython trên trình mô phỏng iOS. Môi trường kiểm thử này cũng có thể được sử dụng làm project kiểm thử để chạy bộ kiểm thử thư viện Python của bạn trên iOS.

Sau khi build hoặc có được một iOS XCFramework (xem :source:`Apple/iOS/README.md` để biết chi tiết), hãy tạo một bản sao của project môi trường kiểm thử Python trên iOS. Nếu bạn đã sử dụng build script ``Apple`` để build XCframework, bạn có thể chạy:

.. code-block:: bash

    $ python cross-build/iOS/testbed clone --app <path/to/module1> --app <path/to/module2> app-testbed

Hoặc, nếu bạn đã tự cung cấp XCframework, bằng cách chạy:

.. code-block:: bash

    $ python Apple/testbed clone --platform iOS --framework <path/to/Python.xcframework> --app <path/to/module1> --app <path/to/module2> app-testbed

Mọi thư mục được chỉ định bằng cờ ``--app`` sẽ được sao chép vào dự án testbed đã clone. Testbed kết quả sẽ được tạo trong thư mục ``app-testbed``. Trong ví dụ này, ``module1`` và ``module2`` sẽ là các module có thể import tại runtime. Nếu dự án của bạn có thêm dependencies, bạn có thể cài đặt chúng vào thư mục ``app-testbed/Testbed/app_packages`` (bằng ``pip install --target app-testbed/Testbed/app_packages`` hoặc tương tự).

Sau đó, bạn có thể sử dụng thư mục ``app-testbed`` để chạy test suite cho ứng dụng của mình. Ví dụ, nếu ``module1.tests`` là entry point của test suite, bạn có thể chạy:

.. code-block:: bash

    $ python app-testbed run -- module1.tests

Tương đương với việc chạy ``python -m module1.tests`` trên bản dựng Python cho desktop. Mọi đối số sau ``--`` sẽ được truyền đến testbed như thể chúng là các đối số của ``python -m`` trên máy desktop.

Bạn cũng có thể mở dự án testbed trong Xcode bằng cách chạy:

.. code-block:: bash

    $ open app-testbed/iOSTestbed.xcodeproj

Điều này cho phép bạn sử dụng đầy đủ bộ công cụ Xcode để debugging.

Các đối số được sử dụng để chạy test suite được định nghĩa như một phần của test plan. Để sửa đổi test plan, hãy chọn node test plan trong cây dự án (đây sẽ là node con đầu tiên của node gốc), rồi chọn tab "Configurations". Sửa đổi giá trị "Arguments Passed On Launch" để thay đổi các đối số kiểm thử.

Kế hoạch kiểm thử cũng tắt việc kiểm thử song song và chỉ định sử dụng tệp ``Testbed.lldbinit`` để cung cấp cấu hình cho debugger. Cấu hình debugger mặc định tắt các breakpoint tự động trên các tín hiệu ``SIGINT``, ``SIGUSR1``, ``SIGUSR2`` và ``SIGXFSZ``.

Tuân thủ App Store
==================

Cơ chế duy nhất để phân phối ứng dụng đến các thiết bị iOS của bên thứ ba là gửi ứng dụng lên iOS App Store; các ứng dụng được gửi để phân phối phải vượt qua quy trình xét duyệt ứng dụng của Apple. Quy trình này bao gồm một tập hợp các quy tắc xác thực tự động để kiểm tra application bundle đã gửi nhằm phát hiện mã có vấn đề. Bạn cần thực hiện một số bước để đảm bảo ứng dụng có thể vượt qua các bước xác thực này.

Mã không tương thích trong thư viện chuẩn
-----------------------------------------

Thư viện chuẩn Python chứa một số đoạn mã được biết là vi phạm các quy tắc tự động này. Mặc dù những vi phạm này có vẻ là kết quả dương tính giả, các quy tắc xét duyệt của Apple không thể bị phản biện; vì vậy, cần sửa đổi thư viện chuẩn Python để ứng dụng vượt qua quy trình xét duyệt của App Store.

Cây mã nguồn Python chứa
:source:`a patch file <Mac/Resources/app-store-compliance.patch>` sẽ loại bỏ toàn bộ mã được biết là gây ra sự cố với quy trình xét duyệt của App Store. Bản vá này được tự động áp dụng khi build cho iOS.

Tệp kê khai quyền riêng tư
--------------------------

Vào tháng 4 năm 2025, Apple đã đưa ra yêu cầu `một số thư viện bên thứ ba phải cung cấp Privacy Manifest <https://developer.apple.com/support/third-party-SDK-requirements>`__. Do đó, nếu bạn có một module nhị phân sử dụng một trong các thư viện bị ảnh hưởng, bạn phải cung cấp một tệp ``.xcprivacy`` cho thư viện đó. OpenSSL là một trong những thư viện bị ảnh hưởng bởi yêu cầu này, nhưng vẫn còn các thư viện khác.

Nếu bạn tạo một module nhị phân có tên ``mymodule.so`` và sử dụng script build Xcode được mô tả ở bước 7 ở trên, bạn có thể đặt một tệp ``mymodule.xcprivacy`` bên cạnh ``mymodule.so``, và privacy manifest sẽ được cài đặt vào vị trí bắt buộc khi module nhị phân được chuyển đổi thành framework.
