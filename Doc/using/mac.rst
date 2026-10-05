.. highlight:: none

.. _using-on-mac:

*************************
Sử dụng Python trên macOS
*************************

.. sectionauthor:: Bob Savage <bobsavage@mac.com>
.. sectionauthor:: Ned Deily <nad@python.org>

Tài liệu này nhằm cung cấp tổng quan về những hành vi đặc thù của macOS mà bạn cần biết để bắt đầu sử dụng Python trên máy Mac. Python trên máy Mac chạy macOS rất giống Python trên các nền tảng có nguồn gốc Unix khác, nhưng có một số khác biệt trong quá trình cài đặt và một số tính năng.

Có nhiều cách để tải và cài đặt Python cho macOS. Các phiên bản dựng sẵn của những phiên bản Python mới nhất có sẵn từ một số nhà phân phối. Phần lớn tài liệu này mô tả việc sử dụng các bản Python do nhóm phát hành CPython cung cấp để tải xuống từ trang web `python.org <https://www.python.org/downloads/>`_. Xem
:ref:`alternative_bundles` để biết một số tùy chọn khác.

.. _getting-osx:
.. _getting-and-installing-macpython:

Sử dụng Python cho macOS từ ``python.org``
==========================================

Các bước cài đặt
----------------

Đối với `các phiên bản Python hiện tại <https://www.python.org/downloads/>`_ (ngoài những phiên bản ở trạng thái ``security``), nhóm phát hành tạo một gói cài đặt **Python cho macOS** cho mỗi bản phát hành mới. Danh sách các trình cài đặt hiện có được cung cấp `tại đây <https://www.python.org/downloads/macos/>`_. Khi có thể, chúng tôi khuyến nghị sử dụng phiên bản Python được hỗ trợ mới nhất. Các trình cài đặt hiện tại cung cấp bản dựng `universal2 binary <https://en.wikipedia.org/wiki/Universal_binary>`_ của Python, chạy nguyên bản trên tất cả máy Mac (Apple Silicon và Intel) được nhiều phiên bản macOS hỗ trợ, hiện thường từ **macOS 10.15 Catalina** trở lên.

Tệp đã tải xuống là một tệp gói trình cài đặt macOS tiêu chuẩn (``.pkg``). Thông tin về tính toàn vẹn của tệp (checksum, kích thước, chữ ký sigstore, v.v.) cho từng tệp được cung cấp trên trang tải xuống bản phát hành. Các gói trình cài đặt và nội dung của chúng được ký và notarize bằng chứng chỉ Apple Developer ID ``Python Software Foundation`` để đáp ứng `các yêu cầu của macOS Gatekeeper <https://support.apple.com/en-us/102445>`_.

Để cài đặt theo thiết lập mặc định, hãy bấm đúp vào tệp gói trình cài đặt đã tải xuống. Thao tác này sẽ khởi chạy ứng dụng macOS Installer tiêu chuẩn và hiển thị bước đầu tiên trong một số cửa sổ trình cài đặt.

.. image:: mac_installer_01_introduction.png

Bấm vào nút **Continue** sẽ mở **Read Me** của trình cài đặt này. Ngoài các thông tin quan trọng khác, **Read Me** cho biết phiên bản Python sẽ được cài đặt và những phiên bản macOS nào được hỗ trợ. Bạn có thể cần cuộn qua để đọc toàn bộ tệp. Theo mặc định, **Read Me** này cũng sẽ được cài đặt tại |applications_python_version_literal| và có thể đọc bất cứ lúc nào.

.. image:: mac_installer_02_readme.png

Bấm vào **Continue** để tiếp tục hiển thị giấy phép của Python và các phần mềm đi kèm khác. Sau đó, bạn cần **Agree** với các điều khoản cấp phép trước khi chuyển sang bước tiếp theo. Tệp giấy phép này cũng sẽ được cài đặt và có thể đọc sau.

.. image:: mac_installer_03_license.png

Sau khi chấp nhận các điều khoản cấp phép, bước tiếp theo là màn hình **Installation Type**. Đối với hầu hết mục đích sử dụng, bộ thao tác cài đặt tiêu chuẩn là phù hợp.

.. image:: mac_installer_04_installation_type.png

Bằng cách nhấn nút **Customize**, bạn có thể chọn bỏ qua hoặc chọn một số thành phần gói nhất định của trình cài đặt. Bấm vào từng tên gói để xem mô tả về nội dung được cài đặt. Để cài đặt thêm hỗ trợ cho tính năng free-threaded tùy chọn, hãy xem :ref:`install-freethreaded-macos`.

.. image:: mac_installer_05_custom_install.png

Trong cả hai trường hợp, bấm **Install** sẽ bắt đầu quá trình cài đặt bằng cách yêu cầu quyền cài đặt phần mềm mới. Cần có tên người dùng macOS với đặc quyền ``Administrator``, vì Python được cài đặt sẽ khả dụng cho tất cả người dùng của máy Mac.

Khi quá trình cài đặt hoàn tất, cửa sổ **Summary** sẽ xuất hiện.

.. image:: mac_installer_06_summary.png

Nhấp đúp vào biểu tượng hoặc tệp :command:`Install Certificates.command` trong cửa sổ |applications_python_version_literal| để hoàn tất quá trình cài đặt.

.. image:: mac_installer_07_applications.png

Thao tác này sẽ mở một cửa sổ :program:`Terminal` shell tạm thời, sử dụng Python mới để tải xuống và cài đặt các chứng chỉ gốc SSL cho Python.

.. image:: mac_installer_08_install_certificates.png

Nếu ``Successfully installed certifi`` và ``update complete`` xuất hiện trong cửa sổ terminal, quá trình cài đặt đã hoàn tất. Hãy đóng cửa sổ terminal này và cửa sổ trình cài đặt.

Bản cài đặt mặc định sẽ bao gồm:

* Một thư mục |python_version_literal| trong thư mục :file:`Applications` của bạn. Trong đó, bạn sẽ tìm thấy :program:`IDLE`, môi trường phát triển là một thành phần tiêu chuẩn của các bản phân phối Python chính thức; và :program:`Python Launcher`, thành phần xử lý việc nhấp đúp vào các tập lệnh Python từ `Finder <https://support.apple.com/en-us/HT201732>`_ của macOS.

* Một :file:`/Library/Frameworks/Python.framework` framework, bao gồm tệp thực thi Python và các thư viện. Trình cài đặt thêm vị trí này vào shell path của bạn. Để gỡ cài đặt Python, bạn có thể xóa ba thành phần này. Các symlink đến tệp thực thi Python được đặt trong :file:`/usr/local/bin/`.

.. note::

   Các phiên bản macOS gần đây bao gồm lệnh :command:`python3` trong :file:`/usr/bin/python3`, liên kết đến một phiên bản Python thường cũ hơn và chưa đầy đủ, được cung cấp bởi và dành cho các công cụ phát triển của Apple, :program:`Xcode` hoặc :program:`Command Line Tools for Xcode`. Bạn không bao giờ nên sửa đổi hoặc cố gắng xóa bản cài đặt này, vì bản cài đặt này do Apple kiểm soát và được phần mềm do Apple cung cấp hoặc phần mềm bên thứ ba sử dụng. Nếu chọn cài đặt phiên bản Python mới hơn từ ``python.org``, bạn sẽ có hai bản cài đặt Python khác nhau nhưng đều hoạt động trên máy tính của mình và có thể cùng tồn tại. Các tùy chọn mặc định của trình cài đặt sẽ bảo đảm rằng :command:`python3` của bản cài đặt đó sẽ được sử dụng thay cho :command:`python3` của hệ thống.

Cách chạy một tập lệnh Python
-----------------------------

Có hai cách để gọi trình thông dịch Python. Nếu bạn đã quen sử dụng Unix shell trong cửa sổ terminal, bạn có thể gọi |python_x_dot_y_literal| hoặc ``python3``, tùy chọn theo sau là một hoặc nhiều tùy chọn dòng lệnh (được mô tả trong :ref:`using-on-general`). Hướng dẫn Python cũng có một phần hữu ích về
:ref:`sử dụng Python ở chế độ tương tác từ shell <tut-interac>`.

Bạn cũng có thể gọi trình thông dịch thông qua một môi trường phát triển tích hợp.
:ref:`idle` là một môi trường trình soạn thảo và trình thông dịch cơ bản, được tích hợp trong bản phân phối Python tiêu chuẩn.
:program:`IDLE` có một menu Help cho phép bạn truy cập tài liệu Python. Nếu hoàn toàn mới làm quen với Python, bạn có thể đọc phần giới thiệu về hướng dẫn trong tài liệu đó.

Có nhiều editor và IDE khác khả dụng; xem :ref:`editors` để biết thêm thông tin.

Để chạy một tệp script Python từ cửa sổ terminal, bạn có thể gọi interpreter cùng với tên của tệp script:

    |python_x_dot_y_literal| ``myscript.py``

Để chạy script từ Finder, bạn có thể thực hiện một trong các cách sau:

* Kéo script vào :program:`Python Launcher`.

* Chọn :program:`Python Launcher` làm ứng dụng mặc định để mở script (hoặc bất kỳ script ``.py`` nào) thông qua cửa sổ Finder Info, rồi bấm đúp vào script.
  :program:`Python Launcher` có nhiều tùy chọn để kiểm soát cách script được khởi chạy. Kéo trong khi giữ phím Option cho phép bạn thay đổi các tùy chọn này cho một lần chạy, hoặc sử dụng menu ``Preferences`` của ứng dụng để thay đổi chúng trên toàn hệ thống.

Lưu ý rằng việc chạy script trực tiếp từ Finder của macOS có thể cho kết quả khác với khi chạy từ cửa sổ terminal, vì script sẽ không chạy trong môi trường shell thông thường, bao gồm cả việc thiết lập các biến môi trường trong các shell profile. Và cũng như với mọi script hoặc chương trình khác, hãy chắc chắn về nội dung bạn sắp chạy.

.. _alternative_bundles:

Các bản phân phối thay thế
==========================

Ngoài ``python.org`` tiêu chuẩn cho trình cài đặt macOS, còn có các bản phân phối bên thứ ba dành cho macOS có thể bao gồm chức năng bổ sung. Một số bản phân phối phổ biến và các tính năng chính của chúng:

`ActivePython <https://www.activestate.com/products/python/>`_
    Trình cài đặt tương thích đa nền tảng, kèm tài liệu

`Anaconda <https://www.anaconda.com/download/>`_
    Các module khoa học phổ biến (chẳng hạn như numpy, scipy và pandas) cùng ``conda`` trình quản lý gói.

`Homebrew <https://brew.sh>`_
    Trình quản lý gói dành cho macOS, bao gồm nhiều phiên bản Python và nhiều gói bên thứ ba dựa trên Python (bao gồm numpy, scipy và pandas).

`MacPorts <https://www.macports.org>`_
    Một trình quản lý gói khác dành cho macOS, bao gồm nhiều phiên bản Python và nhiều gói bên thứ ba dựa trên Python. Có thể bao gồm các phiên bản dựng sẵn của Python và nhiều gói dành cho các phiên bản macOS cũ hơn.

Lưu ý rằng các bản phân phối có thể không bao gồm những phiên bản mới nhất của Python hoặc các thư viện khác, đồng thời không được nhóm Python cốt lõi duy trì hoặc hỗ trợ.

.. _mac-package-manager:

Lập trình GUI
=============

Tham khảo `Python Packaging User Guide <Python Packaging User Guide_>`_ để biết thêm thông tin.

.. _Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/installing-packages/


.. _osx-gui-scripts:

.. _gui-programming-on-the-mac:

Lập trình GUI
=============

Có một số lựa chọn để xây dựng ứng dụng GUI trên máy Mac bằng Python.

Bộ công cụ GUI tiêu chuẩn của Python là :mod:`tkinter`, dựa trên bộ công cụ Tk đa nền tảng (https://www.tcl.tk). Một phiên bản Tk dành riêng cho macOS được tích hợp trong trình cài đặt.

*PyObjC* là một binding Python cho framework Objective-C/Cocoa của Apple. Thông tin về PyObjC có tại :pypi:`pyobjc`.

Có một số bộ công cụ GUI macOS thay thế, bao gồm:

* `PySide <https://www.qt.io/qt-for-python>`_: Binding Python chính thức cho `bộ công cụ GUI Qt <https://wiki.qt.io/Qt_for_Python>`_.

* `PyQt <https://riverbankcomputing.com/software/pyqt/>`_: Binding Python thay thế cho Qt.

* `Kivy <https://kivy.org>`_: Bộ công cụ GUI đa nền tảng hỗ trợ nền tảng máy tính và thiết bị di động.

* `Toga <https://toga.readthedocs.io>`_: Một phần của `BeeWare Project <https://beeware.org>`_; hỗ trợ các ứng dụng desktop, mobile, web và console.

* `wxPython <https://wxpython.org>`_: Một toolkit đa nền tảng hỗ trợ các hệ điều hành desktop.


Chủ đề nâng cao
===============

.. _install-freethreaded-macos:

Cài đặt các bản binary free-threaded
------------------------------------

.. versionadded:: 3.13

Gói cài đặt ``python.org`` :ref:`Python for macOS <getting-and-installing-macpython>` có thể tùy chọn cài đặt thêm một bản build Python |version| hỗ trợ :pep:`703`, tính năng free-threading (chạy khi :term:`global interpreter lock` bị tắt). Hãy kiểm tra trang phát hành trên ``python.org`` để xem thông tin cập nhật nếu có.

Chế độ free-threaded đang hoạt động và tiếp tục được cải thiện, nhưng có thêm một phần overhead trong các workload đơn luồng so với bản build thông thường. Ngoài ra, các package bên thứ ba, đặc biệt là những package có :term:`extension module`, có thể chưa sẵn sàng để sử dụng trong bản build free-threaded và sẽ bật lại :term:`GIL`. Vì vậy, hỗ trợ free-threading không được cài đặt theo mặc định. Tính năng này được đóng gói dưới dạng một tùy chọn cài đặt riêng, có thể truy cập bằng cách nhấp vào nút **Customize** tại bước **Installation Type** của trình cài đặt như mô tả ở trên.

.. image:: mac_installer_09_custom_install_free_threaded.png

Nếu ô bên cạnh tên package **Free-threaded Python** được chọn, một :file:`PythonT.framework` riêng cũng sẽ được cài đặt cùng với :file:`Python.framework` thông thường trong :file:`/Library/Frameworks`. Cấu hình này cho phép một bản build Python |version| free-threaded cùng tồn tại trên hệ thống với một bản build Python |version| truyền thống (chỉ GIL), với rủi ro tối thiểu trong quá trình cài đặt hoặc kiểm thử. Bố cục cài đặt này có thể thay đổi trong các bản phát hành sau.

Các cảnh báo và hạn chế đã biết:

- Gói **công cụ dòng lệnh UNIX**, được chọn theo mặc định, sẽ cài đặt các liên kết trong :file:`/usr/local/bin` cho |python_x_dot_y_t_literal|, trình thông dịch free-threaded, và |python_x_dot_y_t_literal_config|, một tiện ích cấu hình có thể hữu ích cho các trình xây dựng package. Vì :file:`/usr/local/bin` thường được 포함 trong ``PATH`` của shell, nên trong hầu hết trường hợp, bạn không cần thay đổi các biến môi trường ``PATH`` để sử dụng |python_x_dot_y_t_literal|.

- Trong bản phát hành này, gói **Trình cập nhật profile Shell** và
  :file:`Update Shell Profile.command` trong |applications_python_version_literal| không hỗ trợ package free-threaded.

- Bản build free-threaded và bản build truyền thống có các đường dẫn tìm kiếm riêng biệt và các thư mục :file:`site-packages` riêng biệt, vì vậy theo mặc định, nếu bạn cần một package có sẵn trong cả hai bản build, có thể bạn phải cài đặt package đó trong cả hai. Package free-threaded sẽ cài đặt một phiên bản riêng của :program:`pip` để sử dụng với |python_x_dot_y_t_literal|.

  - Để cài đặt một package bằng :command:`pip` mà không có :command:`venv`:

    .. parsed-literal::

       python\ |version|\ t -m pip install <package_name>

- Khi làm việc với nhiều môi trường Python, cách thường an toàn và dễ dàng nhất là :ref:`tạo và sử dụng các môi trường ảo <tut-venv>`. Việc này có thể tránh xung đột tên lệnh và nhầm lẫn về Python đang được sử dụng:

  .. parsed-literal::

     python\ |version|\ t -m venv <venv_name>


  sau đó :command:`activate`.

- Để chạy phiên bản free-threaded của IDLE:

  .. parsed-literal::

     python\ |version|\ t -m idlelib


- Các trình thông dịch trong cả hai bản dựng đều phản hồi với cùng một
  :ref:`biến môi trường PYTHON <using-on-envvars>`, những biến này có thể gây ra kết quả không mong muốn, chẳng hạn như khi bạn đã đặt ``PYTHONPATH`` trong shell profile. Nếu cần, có
  :ref:`các tùy chọn dòng lệnh <using-on-interface-options>` như ``-E`` để bỏ qua các biến môi trường này.

- Bản dựng free-threaded liên kết với các thư viện dùng chung của bên thứ ba, chẳng hạn như ``OpenSSL`` và ``Tk``, được cài đặt trong framework truyền thống. Điều này có nghĩa là cả hai bản dựng cũng dùng chung một bộ chứng chỉ tin cậy được cài đặt bởi script :command:`Install Certificates.command`, vì vậy script này chỉ cần được chạy một lần.

- Nếu bạn không thể dựa vào liên kết trong ``/usr/local/bin`` trỏ đến ``python.org`` free-threaded |python_x_dot_y_t_literal| (ví dụ: nếu bạn muốn cài đặt phiên bản riêng của mình ở đó hoặc một bản phân phối khác thực hiện việc này), bạn có thể đặt rõ ràng biến môi trường shell ``PATH`` của mình để bao gồm thư mục ``PythonT`` framework ``bin``:

  .. parsed-literal::

     export PATH="/Library/Frameworks/PythonT.framework/Versions/\ |version|\ /bin":"$PATH"

  Cài đặt framework truyền thống theo mặc định thực hiện điều tương tự, ngoại trừ :file:`Python.framework`. Hãy lưu ý rằng việc có cả hai thư mục ``bin`` của framework trong ``PATH`` có thể gây nhầm lẫn nếu có các tên trùng lặp như |python_x_dot_y_literal| trong cả hai; thư mục nào thực sự được sử dụng phụ thuộc vào thứ tự xuất hiện của chúng trong ``PATH``. Các lệnh ``which python3.x`` hoặc ``which python3.xt`` có thể hiển thị đường dẫn đang được sử dụng. Sử dụng môi trường ảo có thể giúp tránh những sự mơ hồ như vậy. Một lựa chọn khác là tạo shell :command:`alias` trỏ đến trình thông dịch mong muốn, như sau:

  .. parsed-literal::

     alias py\ |version|\ ="/Library/Frameworks/Python.framework/Versions/\ |version|\ /bin/python\ |version|\ "
     alias py\ |version|\ t="/Library/Frameworks/PythonT.framework/Versions/\ |version|\ /bin/python\ |version|\ t"

Cài đặt bằng dòng lệnh
----------------------

Nếu muốn sử dụng automation để cài đặt gói trình cài đặt ``python.org`` (thay vì sử dụng ứng dụng GUI :program:`Installer` quen thuộc của macOS), tiện ích :command:`installer` trên dòng lệnh của macOS cũng cho phép bạn chọn các tùy chọn không mặc định. Nếu chưa quen với :command:`installer`, bạn có thể thấy nó hơi khó hiểu (xem :command:`man installer` để biết thêm thông tin). Ví dụ, đoạn mã shell sau đây minh họa một cách thực hiện, sử dụng bản phát hành |x_dot_y_b2_literal| và chọn tùy chọn trình thông dịch free-threaded:

.. parsed-literal::

    RELEASE="python-\ |version|\ 0b2-macos11.pkg"

    # download installer pkg
    curl -O \https://www.python.org/ftp/python/\ |version|\ .0/${RELEASE}

    # create installer choicechanges to customize the install:
    #    enable the PythonTFramework-\ |version|\  package
    #    while accepting the other defaults (install all other packages)
    cat > ./choicechanges.plist <<EOF
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "\http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <array>
            <dict>
                    <key>attributeSetting</key>
                    <integer>1</integer>
                    <key>choiceAttribute</key>
                    <string>selected</string>
                    <key>choiceIdentifier</key>
                    <string>org.python.Python.PythonTFramework-\ |version|\ </string>
            </dict>
    </array>
    </plist>
    EOF

    sudo installer -pkg ./${RELEASE} -applyChoiceChangesXML ./choicechanges.plist -target /


Sau đó, bạn có thể kiểm tra xem cả hai bản build của trình cài đặt hiện đã khả dụng bằng lệnh tương tự như sau:

.. parsed-literal::

    $ # test that the free-threaded interpreter was installed if the Unix Command Tools package was enabled
    $ /usr/local/bin/python\ |version|\ t -VV
    Python \ |version|\ .0b2 free-threading build (v\ |version|\ .0b2:3a83b172af, Jun  5 2024, 12:57:31) [Clang 15.0.0 (clang-1500.3.9.4)]
    $ #    and the traditional interpreter
    $ /usr/local/bin/python\ |version|\  -VV
    Python \ |version|\ .0b2 (v\ |version|\ .0b2:3a83b172af, Jun  5 2024, 12:50:24) [Clang 15.0.0 (clang-1500.3.9.4)]
    $ # test that they are also available without the prefix if /usr/local/bin is on $PATH
    $ python\ |version|\ t -VV
    Python \ |version|\ .0b2 free-threading build (v\ |version|\ .0b2:3a83b172af, Jun  5 2024, 12:57:31) [Clang 15.0.0 (clang-1500.3.9.4)]
    $ python\ |version|\  -VV
    Python \ |version|\ .0b2 (v\ |version|\ .0b2:3a83b172af, Jun  5 2024, 12:50:24) [Clang 15.0.0 (clang-1500.3.9.4)]

.. note::

   Các trình cài đặt ``python.org`` hiện tại chỉ cài đặt vào những vị trí cố định như
   :file:`/Library/Frameworks/`, :file:`/Applications` và :file:`/usr/local/bin`. Bạn không thể sử dụng tùy chọn :command:`installer` ``-domain`` để cài đặt vào các vị trí khác.

.. _distributing-python-applications-on-the-mac:

Phân phối ứng dụng Python
-------------------------

Có nhiều công cụ để chuyển mã Python của bạn thành một ứng dụng độc lập có thể phân phối:

* :pypi:`py2app`: Hỗ trợ tạo các bundle macOS ``.app`` từ một dự án Python.

* `Briefcase <https://briefcase.readthedocs.io>`_: Là một phần của `BeeWare Project <https://beeware.org>`_; đây là công cụ đóng gói đa nền tảng hỗ trợ tạo các bundle ``.app`` trên macOS, đồng thời quản lý việc signing và notarization.

* `PyInstaller <https://pyinstaller.org/>`_: Công cụ đóng gói đa nền tảng tạo ra một tệp hoặc thư mục duy nhất làm artifact có thể phân phối.

Tuân thủ App Store
------------------

Các ứng dụng được gửi để phân phối thông qua macOS App Store phải vượt qua quy trình xét duyệt ứng dụng của Apple. Quy trình này bao gồm một tập hợp các quy tắc xác thực tự động, dùng để kiểm tra bundle ứng dụng được gửi nhằm phát hiện mã có vấn đề.

Thư viện chuẩn Python chứa một số mã được biết là vi phạm các quy tắc tự động này. Mặc dù những vi phạm này có vẻ là false positive, các quy tắc xét duyệt của Apple không thể bị khiếu nại. Vì vậy, cần sửa đổi thư viện chuẩn Python để ứng dụng vượt qua quy trình xét duyệt của App Store.

Cây mã nguồn Python chứa
:source:`a patch file <Mac/Resources/app-store-compliance.patch>` sẽ loại bỏ toàn bộ mã được biết là gây ra sự cố trong quy trình xét duyệt của App Store. Bản vá này được áp dụng tự động khi CPython được cấu hình với
:option:`--with-app-store-compliance` tùy chọn.

Bản vá này thường không cần thiết để sử dụng CPython trên máy Mac; cũng không cần thiết nếu bạn phân phối ứng dụng *bên ngoài* macOS App Store. Bản vá này *chỉ* cần thiết nếu bạn sử dụng macOS App Store làm kênh phân phối.

Các tài nguyên khác
===================

`Trang trợ giúp Python.org <https://www.python.org/about/help/>`_ có liên kết đến nhiều tài nguyên hữu ích. `Danh sách thư Pythonmac-SIG <https://www.python.org/community/sigs/current/pythonmac-sig/>`_ là một tài nguyên hỗ trợ khác dành riêng cho người dùng và nhà phát triển Python trên máy Mac.

.. _`python.org website`: https://www.python.org/downloads/
.. _`current Python versions`: https://www.python.org/downloads/
.. _`here`: https://www.python.org/downloads/macos/
.. _`universal2 binary`: https://en.wikipedia.org/wiki/Universal_binary
.. _`macOS Gatekeeper requirements`: https://support.apple.com/en-us/102445
.. _`Finder`: https://support.apple.com/en-us/HT201732
.. _`ActivePython`: https://www.activestate.com/products/python/
.. _`Anaconda`: https://www.anaconda.com/download/
.. _`Homebrew`: https://brew.sh
.. _`MacPorts`: https://www.macports.org
.. _`PySide`: https://www.qt.io/qt-for-python
.. _`Qt GUI toolkit`: https://wiki.qt.io/Qt_for_Python
.. _`PyQt`: https://riverbankcomputing.com/software/pyqt/
.. _`Kivy`: https://kivy.org
.. _`Toga`: https://toga.readthedocs.io
.. _`BeeWare Project`: https://beeware.org
.. _`wxPython`: https://wxpython.org
.. _`Briefcase`: https://briefcase.readthedocs.io
.. _`PyInstaller`: https://pyinstaller.org/
.. _`python.org Help page`: https://www.python.org/about/help/
.. _`Pythonmac-SIG mailing list`: https://www.python.org/community/sigs/current/pythonmac-sig/
