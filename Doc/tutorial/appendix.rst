.. _tut-appendix:

*******
Phụ lục
*******


.. _tut-interac:

Chế độ tương tác
================

Có hai biến thể của :term:`REPL` tương tác. Trình thông dịch cơ bản cổ điển được hỗ trợ trên mọi nền tảng với khả năng điều khiển dòng tối thiểu.

Kể từ Python 3.13, một shell tương tác mới được sử dụng theo mặc định. Shell này hỗ trợ màu sắc, chỉnh sửa nhiều dòng, duyệt lịch sử và chế độ dán. Để tắt màu sắc, hãy xem :ref:`using-on-controlling-color` để biết chi tiết. Các phím chức năng cung cấp thêm một số tính năng.
:kbd:`F1` mở trình duyệt trợ giúp tương tác :mod:`pydoc`.
:kbd:`F2` cho phép duyệt lịch sử dòng lệnh mà không có đầu ra hoặc
các lời nhắc :term:`>>>` và :term:`...`. :kbd:`F3` vào "chế độ dán", giúp việc dán các khối mã lớn dễ dàng hơn. Nhấn :kbd:`F3` để quay lại lời nhắc thông thường.

Khi sử dụng interactive shell mới, hãy thoát khỏi shell bằng cách nhập :kbd:`exit` hoặc :kbd:`quit`. Không bắt buộc phải thêm dấu ngoặc tròn gọi hàm sau các lệnh đó.

Nếu không muốn sử dụng interactive shell mới, bạn có thể vô hiệu hóa nó thông qua biến môi trường :envvar:`PYTHON_BASIC_REPL`.

.. _tut-error:

Xử lý lỗi
---------

Khi xảy ra lỗi, interpreter sẽ in thông báo lỗi và stack trace. Trong interactive mode, sau đó interpreter quay lại primary prompt; khi dữ liệu đầu vào đến từ một tệp, interpreter sẽ thoát với trạng thái thoát khác 0 sau khi in stack trace. (Các ngoại lệ được xử lý bởi mệnh đề :keyword:`except` trong câu lệnh :keyword:`try` không được xem là lỗi trong ngữ cảnh này.) Một số lỗi luôn nghiêm trọng và khiến chương trình thoát với trạng thái thoát khác 0; điều này áp dụng cho các tình trạng không nhất quán nội bộ và một số trường hợp hết bộ nhớ. Tất cả thông báo lỗi được ghi vào luồng standard error; đầu ra thông thường từ các lệnh đã thực thi được ghi vào standard output.

Nhập ký tự ngắt (thường là :kbd:`Control-C` hoặc :kbd:`Delete`) tại primary prompt hoặc secondary prompt sẽ hủy dữ liệu đầu vào và quay lại primary prompt. [#]_ Nhập ký tự ngắt trong khi một lệnh đang thực thi sẽ ném ra
ngoại lệ :exc:`KeyboardInterrupt`, có thể được xử lý bằng câu lệnh :keyword:`try`.


.. _tut-scripts:

Các tập lệnh Python có thể thực thi
-----------------------------------

Trên các hệ thống Unix kiểu BSD, bạn có thể làm cho các tập lệnh Python có thể thực thi trực tiếp, giống như các tập lệnh shell, bằng cách đặt dòng::

   #!/usr/bin/env python3

(với giả định rằng trình thông dịch nằm trong :envvar:`PATH` của người dùng) ở đầu tập lệnh và cấp cho tệp quyền thực thi. ``#!`` phải là hai ký tự đầu tiên của tệp. Trên một số nền tảng, dòng đầu tiên này phải kết thúc bằng ký hiệu kết thúc dòng kiểu Unix (``'\n'``), không phải ký hiệu kết thúc dòng kiểu Windows (``'\r\n'``). Lưu ý rằng ký tự dấu thăng, hay dấu pound, ``'#'``, được dùng để bắt đầu một comment trong Python.

Bạn có thể cấp quyền thực thi, hay quyền (permission), cho tập lệnh bằng cách sử dụng
lệnh :program:`chmod`.

.. code-block:: shell-session

   $ chmod +x myscript.py

Trên các hệ thống Windows, không có khái niệm "quyền thực thi". Trình cài đặt Python tự động liên kết các tệp ``.py`` với ``python.exe``, để việc nhấp đúp vào một tệp Python sẽ chạy tệp đó dưới dạng tập lệnh. Phần mở rộng cũng có thể là ``.pyw``; trong trường hợp đó, cửa sổ console thường xuất hiện sẽ được ẩn đi.


.. _tut-startup:

Tệp Khởi động Tương tác
-----------------------

Khi sử dụng Python ở chế độ tương tác, việc có một số lệnh tiêu chuẩn được thực thi mỗi khi trình thông dịch khởi động thường rất hữu ích. Bạn có thể thực hiện điều này bằng cách đặt một biến môi trường có tên :envvar:`PYTHONSTARTUP` thành tên của một tệp chứa các lệnh khởi động. Điều này tương tự tính năng :file:`.profile` của các shell Unix.

Tệp này chỉ được đọc trong các phiên tương tác, không được đọc khi Python đọc lệnh từ một tập lệnh, và cũng không được đọc khi :file:`/dev/tty` được cung cấp làm nguồn lệnh rõ ràng (trong trường hợp này, nó vẫn hoạt động như một phiên tương tác). Tệp được thực thi trong cùng namespace nơi các lệnh tương tác được thực thi, vì vậy bạn có thể sử dụng mà không cần chỉ định đầy đủ các đối tượng mà tệp định nghĩa hoặc nhập vào trong phiên tương tác. Bạn cũng có thể thay đổi các dấu nhắc ``sys.ps1`` và ``sys.ps2`` trong tệp này.

Nếu muốn đọc thêm một tệp khởi động từ thư mục hiện tại, bạn có thể lập trình việc này trong tệp khởi động toàn cục bằng đoạn mã như ``if os.path.isfile('.pythonrc.py'): exec(open('.pythonrc.py').read())``. Nếu muốn sử dụng tệp khởi động trong một tập lệnh, bạn phải thực hiện việc này một cách rõ ràng trong tập lệnh đó::

   import os
   filename = os.environ.get('PYTHONSTARTUP')
   if filename and os.path.isfile(filename):
       with open(filename) as fobj:
           startup_file = fobj.read()
       exec(startup_file)


.. _tut-customize:

Các mô-đun tùy chỉnh
--------------------

Python cung cấp hai hook để bạn tùy chỉnh nó: :index:`sitecustomize` và
:index:`usercustomize`. Để xem cách hoạt động, trước tiên bạn cần tìm vị trí của thư mục user site-packages. Khởi động Python và chạy đoạn mã này::

   >>> import site
   >>> site.getusersitepackages()
   '/home/user/.local/lib/python3.x/site-packages'

Bây giờ bạn có thể tạo một tệp có tên :file:`usercustomize.py` trong thư mục đó và đặt vào đó bất cứ nội dung nào bạn muốn. Tệp này sẽ ảnh hưởng đến mọi lần gọi Python, trừ khi Python được khởi động với tùy chọn :option:`-s` để tắt việc import tự động.

:index:`sitecustomize` hoạt động theo cách tương tự, nhưng thường được quản trị viên máy tính tạo trong thư mục global site-packages và được import trước :index:`usercustomize`. Xem tài liệu của mô-đun :mod:`site` để biết thêm chi tiết.


.. rubric:: Chú thích

.. [#] Một vấn đề với gói GNU Readline có thể ngăn điều này xảy ra.
