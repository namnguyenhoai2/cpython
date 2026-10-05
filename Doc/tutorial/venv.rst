
.. _tut-venv:

************************
Môi trường ảo và Package
************************

Giới thiệu
==========

Các ứng dụng Python thường sử dụng những package và module không có sẵn trong standard library. Đôi khi, ứng dụng cần một phiên bản cụ thể của một thư viện, vì ứng dụng có thể yêu cầu một lỗi cụ thể đã được sửa hoặc có thể được viết bằng cách sử dụng interface đã lỗi thời của thư viện.

Điều này có nghĩa là một bản cài đặt Python có thể không đáp ứng được yêu cầu của mọi ứng dụng. Nếu ứng dụng A cần phiên bản 1.0 của một module cụ thể nhưng ứng dụng B cần phiên bản 2.0, thì các yêu cầu xung đột với nhau và việc cài đặt phiên bản 1.0 hoặc 2.0 sẽ khiến một trong hai ứng dụng không thể chạy.

Giải pháp cho vấn đề này là tạo một :term:`virtual environment`, một cây thư mục độc lập chứa một bản cài đặt Python cho một phiên bản Python cụ thể, cùng với một số package bổ sung.

Sau đó, các ứng dụng khác nhau có thể sử dụng những môi trường ảo khác nhau. Để giải quyết ví dụ về các yêu cầu xung đột ở trên, ứng dụng A có thể có môi trường ảo riêng với phiên bản 1.0 được cài đặt, trong khi ứng dụng B có một môi trường ảo khác với phiên bản 2.0. Nếu ứng dụng B yêu cầu nâng cấp một thư viện lên phiên bản 3.0, điều này sẽ không ảnh hưởng đến môi trường của ứng dụng A.


Tạo môi trường ảo
=================

Mô-đun được dùng để tạo và quản lý các môi trường ảo có tên là
:mod:`venv`. :mod:`venv` sẽ cài đặt phiên bản Python mà từ đó lệnh được chạy (như được báo cáo bởi tùy chọn :option:`--version`). Ví dụ, thực thi lệnh với ``python3.12`` sẽ cài đặt phiên bản 3.12.

Để tạo một môi trường ảo, hãy chọn một thư mục nơi bạn muốn đặt môi trường đó, rồi chạy mô-đun :mod:`venv` dưới dạng script với đường dẫn thư mục::

   python -m venv tutorial-env

Lệnh này sẽ tạo thư mục ``tutorial-env`` nếu thư mục đó chưa tồn tại, đồng thời tạo các thư mục bên trong chứa một bản sao của trình thông dịch Python và nhiều tệp hỗ trợ khác.

Một vị trí thư mục phổ biến cho môi trường ảo là ``.venv``. Tên này thường giữ cho thư mục được ẩn trong shell, nhờ đó không gây vướng víu, đồng thời cho nó một cái tên giải thích lý do thư mục tồn tại. Tên này cũng ngăn xung đột với các tệp định nghĩa biến môi trường ``.env`` mà một số công cụ hỗ trợ.

Sau khi tạo môi trường ảo, bạn có thể kích hoạt môi trường đó.

Trên Windows, chạy::

  tutorial-env\Scripts\activate

Trên Unix hoặc MacOS, hãy chạy::

  source tutorial-env/bin/activate

(Tập lệnh này được viết cho bash shell. Nếu bạn sử dụng
:program:`csh` hoặc :program:`fish` shell, có các tập lệnh ``activate.csh`` và ``activate.fish`` thay thế mà bạn nên sử dụng.)

Việc kích hoạt virtual environment sẽ thay đổi dấu nhắc của shell để hiển thị virtual environment bạn đang sử dụng, đồng thời sửa đổi môi trường để khi chạy ``python``, bạn sẽ nhận được phiên bản và bản cài đặt Python cụ thể đó. Ví dụ:

.. code-block:: console

  $ source ~/envs/tutorial-env/bin/activate
  (tutorial-env) $ python
  Python 3.5.1 (default, May  6 2016, 10:59:36)
    ...
  >>> import sys
  >>> sys.path
  ['', '/usr/local/lib/python35.zip', ...,
  '~/envs/tutorial-env/lib/python3.5/site-packages']
  >>>

Lưu ý rằng virtual environment đã kích hoạt không thay đổi biến ``PYTHONPATH`` theo bất kỳ cách nào. Điều này có thể dẫn đến kết quả không mong muốn nếu đường dẫn chứa các tham chiếu đến mã không tương thích với phiên bản Python mà virtual environment đang sử dụng. Cách tốt nhất là ``unset PYTHONPATH`` trong bash hoặc lệnh tương đương đối với shell bạn đang sử dụng.

Để hủy kích hoạt virtual environment, hãy nhập::

    deactivate

vào terminal.

Quản lý các gói bằng pip
========================

Bạn có thể cài đặt, nâng cấp và gỡ bỏ các gói bằng một chương trình có tên là
:program:`pip`. Theo mặc định, ``pip`` sẽ cài đặt các gói từ `Python Package Index <https://pypi.org>`_. Bạn có thể duyệt Python Package Index bằng cách truy cập dịch vụ này trong trình duyệt web.

``pip`` có một số subcommand: "install", "uninstall", "freeze", v.v. (Tham khảo :ref:`installing-index` để xem tài liệu đầy đủ về ``pip``.)

Bạn có thể cài đặt phiên bản mới nhất của một gói bằng cách chỉ định tên gói:

.. code-block:: console

  (tutorial-env) $ python -m pip install novas
  Collecting novas
    Downloading novas-3.1.1.3.tar.gz (136kB)
  Installing collected packages: novas
    Running setup.py install for novas
  Successfully installed novas-3.1.1.3

Bạn cũng có thể cài đặt một phiên bản cụ thể của gói bằng cách cung cấp tên gói, theo sau là ``==`` và số phiên bản:

.. code-block:: console

  (tutorial-env) $ python -m pip install requests==2.6.0
  Collecting requests==2.6.0
    Using cached requests-2.6.0-py2.py3-none-any.whl
  Installing collected packages: requests
  Successfully installed requests-2.6.0

Nếu chạy lại lệnh này, ``pip`` sẽ nhận thấy phiên bản được yêu cầu đã được cài đặt và không làm gì cả. Bạn có thể cung cấp một số phiên bản khác để cài đặt phiên bản đó, hoặc có thể chạy ``python -m pip install --upgrade`` để nâng cấp gói lên phiên bản mới nhất:

.. code-block:: console

  (tutorial-env) $ python -m pip install --upgrade requests
  Collecting requests
  Installing collected packages: requests
    Found existing installation: requests 2.6.0
      Uninstalling requests-2.6.0:
        Successfully uninstalled requests-2.6.0
  Successfully installed requests-2.7.0

``python -m pip uninstall`` theo sau bởi một hoặc nhiều tên package sẽ xóa các package đó khỏi virtual environment.

``python -m pip show`` sẽ hiển thị thông tin về một package cụ thể:

.. code-block:: console

  (tutorial-env) $ python -m pip show requests
  ---
  Metadata-Version: 2.0
  Name: requests
  Version: 2.7.0
  Summary: Python HTTP for Humans.
  Home-page: http://python-requests.org
  Author: Kenneth Reitz
  Author-email: me@kennethreitz.com
  License: Apache 2.0
  Location: /Users/akuchling/envs/tutorial-env/lib/python3.4/site-packages
  Requires:

``python -m pip list`` sẽ hiển thị tất cả package đã được cài đặt trong virtual environment:

.. code-block:: console

  (tutorial-env) $ python -m pip list
  novas (3.1.1.3)
  numpy (1.9.2)
  pip (7.0.3)
  requests (2.7.0)
  setuptools (16.0)

``python -m pip freeze`` sẽ tạo ra danh sách tương tự các package đã cài đặt, nhưng kết quả sử dụng định dạng mà ``python -m pip install`` yêu cầu. Một quy ước phổ biến là đặt danh sách này trong tệp ``requirements.txt``:

.. code-block:: console

  (tutorial-env) $ python -m pip freeze > requirements.txt
  (tutorial-env) $ cat requirements.txt
  novas==3.1.1.3
  numpy==1.9.2
  requests==2.7.0

Sau đó, ``requirements.txt`` có thể được commit vào hệ thống quản lý phiên bản và đóng gói cùng với một ứng dụng. Người dùng có thể cài đặt tất cả package cần thiết bằng ``install -r``:

.. code-block:: console

  (tutorial-env) $ python -m pip install -r requirements.txt
  Collecting novas==3.1.1.3 (from -r requirements.txt (line 1))
    ...
  Collecting numpy==1.9.2 (from -r requirements.txt (line 2))
    ...
  Collecting requests==2.7.0 (from -r requirements.txt (line 3))
    ...
  Installing collected packages: novas, numpy, requests
    Running setup.py install for novas
  Successfully installed novas-3.1.1.3 numpy-1.9.2 requests-2.7.0

``pip`` còn có nhiều tùy chọn khác. Hãy tham khảo hướng dẫn :ref:`installing-index` để xem tài liệu đầy đủ về ``pip``. Khi bạn đã viết xong một package và muốn cung cấp package đó trên Python Package Index, hãy tham khảo `hướng dẫn sử dụng về đóng gói Python <Python packaging user guide_>`_.

.. _Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/

.. _`Python Package Index`: https://pypi.org
