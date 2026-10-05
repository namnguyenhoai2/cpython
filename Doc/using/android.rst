.. _using-android:

===========================
Sử dụng Python trên Android
===========================

Python trên Android khác với Python trên các nền tảng máy tính để bàn. Trên nền tảng máy tính để bàn, Python thường được cài đặt dưới dạng tài nguyên hệ thống mà bất kỳ người dùng nào trên máy tính đó cũng có thể sử dụng. Sau đó, người dùng tương tác với Python bằng cách chạy tệp thực thi :program:`python` và nhập lệnh tại lời nhắc tương tác, hoặc chạy một tập lệnh Python.

Trên Android, không có khái niệm cài đặt dưới dạng tài nguyên hệ thống. Đơn vị phân phối phần mềm duy nhất là một "app". Cũng không có console nơi bạn có thể chạy tệp thực thi :program:`python` hoặc tương tác với Python REPL.

Do đó, cách duy nhất để sử dụng Python trên Android là ở embedded mode – tức là viết một ứng dụng Android native, nhúng trình thông dịch Python bằng ``libpython``, rồi gọi mã Python bằng :ref:`Python embedding API <embedding>`. Sau đó, toàn bộ trình thông dịch Python, standard library và tất cả mã Python của bạn được đóng gói vào ứng dụng để ứng dụng sử dụng riêng.

Python standard library có một số thiếu sót và hạn chế đáng chú ý trên Android. Xem :ref:`hướng dẫn về khả năng cung cấp API <mobile-availability>` để biết chi tiết.

Thêm Python vào ứng dụng Android
--------------------------------

Hầu hết nhà phát triển ứng dụng nên sử dụng một trong các công cụ sau, vì chúng mang lại trải nghiệm dễ dàng hơn nhiều:

* `Briefcase <https://briefcase.beeware.org>`__, từ dự án BeeWare
* `Buildozer <https://buildozer.readthedocs.io>`__, từ dự án Kivy
* `Chaquopy <https://chaquo.com/chaquopy>`__
* `pyqtdeploy <https://www.riverbankcomputing.com/static/Docs/pyqtdeploy/>`__
* `Termux <https://termux.dev/en/>`__

Nếu bạn chắc chắn muốn tự mình thực hiện tất cả các bước này, hãy đọc tiếp. Bạn có thể sử dụng
:source:`testbed app <Android/testbed>` làm hướng dẫn; mỗi bước dưới đây đều có liên kết đến tệp liên quan.

* Trước tiên, hãy lấy một bản build Python dành cho Android:

  * Cách dễ nhất là tải xuống một bản phát hành Android từ `python.org <https://www.python.org/downloads/android/>`__. Thư mục ``prefix`` được đề cập bên dưới nằm ở cấp cao nhất của package.

  * Hoặc nếu bạn muốn tự build, hãy làm theo hướng dẫn trong
    :source:`Android/README.md`. Thư mục ``prefix`` sẽ được tạo bên dưới
    :samp:`cross-build/{HOST}`.

* Thêm code vào tệp :source:`build.gradle <Android/testbed/app/build.gradle.kts>` của bạn để sao chép các mục sau vào project. Bạn có thể sao chép tất cả các mục, ngoại trừ code Python của riêng bạn, từ ``prefix/lib``:

  * Trong các thư viện JNI của bạn:

    * ``libpython*.*.so``
    * ``lib*_python.so`` (các thư viện bên ngoài như OpenSSL)

  * Trong assets của bạn:

    * ``python*.*`` (thư viện chuẩn của Python)
    * ``python*.*/site-packages`` (mã Python của riêng bạn)

* Thêm mã vào ứng dụng của bạn để :source:`extract the assets to the filesystem <Android/testbed/app/src/main/java/org/python/testbed/MainActivity.kt>`.

* Thêm mã vào ứng dụng của bạn để :source:`start Python in embedded mode <Android/testbed/app/src/main/c/main_activity.c>`. Mã này cần là mã C được gọi thông qua JNI.

Xây dựng một package Python cho Android
---------------------------------------

Các package Python có thể được xây dựng cho Android dưới dạng wheel và phát hành trên PyPI. Công cụ được khuyến nghị để thực hiện việc này là `cibuildwheel <https://cibuildwheel.pypa.io/en/stable/platforms/#android>`__, công cụ tự động hóa mọi chi tiết trong việc thiết lập môi trường cross-compilation, xây dựng wheel và kiểm thử trên emulator.
