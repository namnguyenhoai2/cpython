.. highlight:: sh

.. _using-on-unix:

*************************************
Sử dụng Python trên các nền tảng Unix
*************************************

.. sectionauthor:: Shriphani Palakodety


Tải và cài đặt phiên bản Python mới nhất
========================================

Trên Linux
----------

Python được cài sẵn trên hầu hết các bản phân phối Linux và có sẵn dưới dạng gói trên tất cả các bản phân phối còn lại. Tuy nhiên, có một số tính năng bạn có thể muốn sử dụng nhưng không có trong gói của bản phân phối. Bạn có thể biên dịch phiên bản Python mới nhất từ mã nguồn.

Trong trường hợp phiên bản Python mới nhất không được cài sẵn và cũng không có trong các repository, bạn có thể tạo các gói cho bản phân phối của riêng mình. Hãy xem các liên kết sau:

.. seealso::

   https://www.debian.org/doc/manuals/maint-guide/first.en.html
      dành cho người dùng Debian
   https://en.opensuse.org/Portal:Packaging
      dành cho người dùng OpenSuse
   https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/
      dành cho người dùng Fedora
   https://slackbook.org/html/package-management-making-packages.html
      dành cho người dùng Slackware

.. _installing_idle_on_linux:

Cài đặt IDLE
~~~~~~~~~~~~

Trong một số trường hợp, IDLE có thể không được bao gồm trong bản cài đặt Python của bạn.

* Dành cho người dùng Debian và Ubuntu::

   sudo apt update
   sudo apt install idle

* Dành cho người dùng Fedora, RHEL và CentOS::

   sudo dnf install python3-idle

* Dành cho người dùng SUSE và OpenSUSE::

   sudo zypper install python3-idle

* Dành cho người dùng Alpine Linux::

   sudo apk add python3-idle



Trên FreeBSD và OpenBSD
-----------------------

* Người dùng FreeBSD, để thêm package, hãy dùng::

     pkg install python3

* Người dùng OpenBSD, để thêm package, hãy dùng::

     pkg_add -r python

     pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/<insert your architecture here>/python-<version>.tgz

  For example i386 users get the 2.5.1 version of Python using::

     pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/i386/python-2.5.1p2.tgz


.. _building-python-on-unix:

Biên dịch Python
================

.. seealso::

   Nếu bạn muốn đóng góp cho CPython, hãy tham khảo `devguide <https://devguide.python.org/getting-started/setup-building/>`_, trong đó có hướng dẫn biên dịch và các mẹo khác về việc thiết lập môi trường.

Nếu bạn muốn tự biên dịch CPython, việc đầu tiên bạn nên làm là lấy `mã nguồn <https://www.python.org/downloads/source/>`_. Bạn có thể tải mã nguồn của bản phát hành mới nhất hoặc lấy một `bản clone <https://devguide.python.org/setup/#get-the-source-code>`_ mới. Bạn cũng cần cài đặt :ref:`các yêu cầu để biên dịch <build-requirements>`.

Quá trình build bao gồm các lệnh thông thường::

   ./configure
   make
   make install

:ref:`Các tùy chọn cấu hình <configure-options>` và các lưu ý đối với từng nền tảng Unix cụ thể được ghi chép đầy đủ trong tệp :source:`README.rst` ở thư mục gốc của cây mã nguồn Python.

.. warning::

   ``make install`` có thể ghi đè hoặc giả dạng tệp nhị phân :file:`python3`. Vì vậy, nên dùng ``make altinstall`` thay vì ``make install`` vì lệnh này chỉ cài đặt :file:`{exec_prefix}/bin/python{version}`.


Các đường dẫn và tệp liên quan đến Python
=========================================

Những mục này có thể khác nhau tùy theo quy ước cài đặt trên hệ thống;
:option:`prefix <--prefix>` và :option:`exec_prefix <--exec-prefix>` phụ thuộc vào cách cài đặt và nên được hiểu theo cách dùng trong phần mềm GNU; chúng có thể giống nhau.

Ví dụ, trên hầu hết các hệ thống Linux, giá trị mặc định cho cả hai là :file:`/usr`.

+-----------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| Tệp/thư mục                                   | Ý nghĩa                                                                                                                           |
+===============================================+===================================================================================================================================+
| :file:`{exec_prefix}/bin/python3`             | Vị trí đề xuất của trình thông dịch.                                                                                              |
+-----------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| :file:`{prefix}/lib/python{version}`,         | Các vị trí đề xuất của những thư mục chứa các module chuẩn.                                                                       |
| :file:`{exec_prefix}/lib/python{version}`     |                                                                                                                                   |
+-----------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| :file:`{prefix}/include/python{version}`,     | Các vị trí đề xuất của những thư mục chứa các tệp include cần thiết để phát triển các extension Python và nhúng trình thông dịch. |
| :file:`{exec_prefix}/include/python{version}` |                                                                                                                                   |
+-----------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+


Linh tinh
=========

Để dễ dàng sử dụng các script Python trên Unix, bạn cần làm cho chúng có thể thực thi, chẳng hạn bằng

.. code-block:: shell-session

   $ chmod +x script

và đặt một dòng Shebang thích hợp ở đầu script. Một lựa chọn thường phù hợp là::

   #!/usr/bin/env python3

tìm kiếm trình thông dịch Python trong toàn bộ :envvar:`PATH`. Tuy nhiên, một số hệ điều hành Unix có thể không có lệnh :program:`env`, vì vậy bạn có thể cần ghi cứng ``/usr/bin/python3`` làm đường dẫn đến trình thông dịch.

Để sử dụng các lệnh shell trong script Python, hãy xem module :mod:`subprocess`.

.. _unix_custom_openssl:

OpenSSL tùy chỉnh
=================

1. Để sử dụng cấu hình OpenSSL và kho tin cậy hệ thống của nhà cung cấp, hãy tìm thư mục chứa tệp hoặc liên kết tượng trưng ``openssl.cnf`` trong ``/etc``. Trên hầu hết các bản phân phối, tệp này nằm trong ``/etc/ssl`` hoặc ``/etc/pki/tls``. Thư mục này cũng phải chứa tệp ``cert.pem`` và/hoặc thư mục ``certs``.

   .. code-block:: shell-session

      $ find /etc/ -name openssl.cnf -printf "%h\n"
      /etc/ssl

2. Tải xuống, xây dựng và cài đặt OpenSSL. Hãy chắc chắn rằng bạn sử dụng ``install_sw`` chứ không phải ``install``. Target ``install_sw`` không ghi đè ``openssl.cnf``.

   .. code-block:: shell-session

      $ curl -O https://www.openssl.org/source/openssl-VERSION.tar.gz
      $ tar xzf openssl-VERSION
      $ pushd openssl-VERSION
      $ ./config \
          --prefix=/usr/local/custom-openssl \
          --libdir=lib \
          --openssldir=/etc/ssl
      $ make -j1 depend
      $ make -j8
      $ make install_sw
      $ popd

3. Xây dựng Python với OpenSSL tùy chỉnh (xem các tùy chọn configure ``--with-openssl`` và ``--with-openssl-rpath``)

   .. code-block:: shell-session

      $ pushd python-3.x.x
      $ ./configure -C \
          --with-openssl=/usr/local/custom-openssl \
          --with-openssl-rpath=auto \
          --prefix=/usr/local/python-3.x.x
      $ make -j8
      $ make altinstall

.. note::

   Các bản phát hành bản vá của OpenSSL có ABI tương thích ngược. Bạn không cần biên dịch lại Python để cập nhật OpenSSL. Chỉ cần thay thế bản cài đặt OpenSSL tùy chỉnh bằng một phiên bản mới hơn.

.. _`devguide`: https://devguide.python.org/getting-started/setup-building/
.. _`source`: https://www.python.org/downloads/source/
.. _`clone`: https://devguide.python.org/setup/#get-the-source-code
