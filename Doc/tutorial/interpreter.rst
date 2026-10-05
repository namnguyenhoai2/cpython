.. _tut-using:

**************************
Sử dụng Python Interpreter
**************************


.. _tut-invoking:

Gọi Interpreter
===============

Python interpreter thường được cài đặt dưới dạng |usr_local_bin_python_x_dot_y_literal| trên những máy có hỗ trợ; việc thêm :file:`/usr/local/bin` vào đường dẫn tìm kiếm của Unix shell cho phép bạn khởi động nó bằng cách nhập lệnh sau:

.. code-block:: text

   python3.14

vào shell. [#]_ Vì việc chọn thư mục chứa interpreter là một tùy chọn khi cài đặt, nên có thể có các vị trí khác; hãy hỏi chuyên gia Python hoặc quản trị viên hệ thống tại địa phương. (Ví dụ: :file:`/usr/local/python` là một vị trí thay thế phổ biến.)

Trên các máy Windows mà bạn đã cài đặt Python từ :ref:`Microsoft Store <windows-store>`, lệnh |python_x_dot_y_literal| sẽ khả dụng. Nếu đã cài đặt :ref:`py.exe launcher <launcher>`, bạn có thể sử dụng lệnh :file:`py`. Xem :ref:`setting-envvars` để biết các cách khác khởi chạy Python.

Nhập ký tự kết thúc tệp (:kbd:`Control-D` trên Unix, :kbd:`Control-Z` trên Windows) tại dấu nhắc chính sẽ khiến interpreter thoát với mã trạng thái bằng không. Nếu cách đó không hiệu quả, bạn có thể thoát khỏi interpreter bằng cách nhập lệnh sau: ``quit()``.

Các tính năng chỉnh sửa dòng của interpreter bao gồm chỉnh sửa tương tác, thay thế lịch sử và hoàn tất mã trên hầu hết các hệ thống. Có lẽ cách nhanh nhất để kiểm tra xem tính năng chỉnh sửa dòng lệnh có được hỗ trợ hay không là nhập một từ tại dấu nhắc Python, sau đó nhấn Left arrow (hoặc :kbd:`Control-b`). Nếu con trỏ di chuyển, bạn có tính năng chỉnh sửa dòng lệnh; xem Phụ lục
:ref:`tut-interacting` để tìm hiểu phần giới thiệu về các phím. Nếu không có gì xảy ra hoặc nếu xuất hiện một chuỗi như ``^[[D`` hay ``^B``, thì tính năng chỉnh sửa dòng lệnh không khả dụng; bạn chỉ có thể dùng phím backspace để xóa các ký tự khỏi dòng hiện tại.

Trình thông dịch hoạt động phần nào giống shell Unix: khi được gọi với đầu vào chuẩn kết nối với thiết bị tty, nó đọc và thực thi các lệnh theo cách tương tác; khi được gọi với một đối số là tên tệp hoặc với một tệp làm đầu vào chuẩn, nó đọc và thực thi một *tập lệnh* từ tệp đó.

Một cách thứ hai để khởi động trình thông dịch là ``python -c command [arg] ...``, cách này thực thi (các) câu lệnh trong *lệnh*, tương tự như shell
tùy chọn :option:`-c`. Vì các câu lệnh Python thường chứa khoảng trắng hoặc các ký tự khác có ý nghĩa đặc biệt đối với shell, thông thường bạn nên đặt toàn bộ *lệnh* trong dấu trích dẫn.

Một số module Python cũng hữu ích dưới dạng tập lệnh. Bạn có thể gọi chúng bằng ``python -m module [arg] ...``, cách này thực thi tệp mã nguồn của *mô-đun* như thể bạn đã ghi đầy đủ tên của mô-đun đó trên dòng lệnh.

Khi sử dụng một tệp tập lệnh, đôi khi bạn muốn có thể chạy tập lệnh rồi chuyển sang chế độ tương tác. Bạn có thể thực hiện việc này bằng cách truyền :option:`-i` trước tập lệnh.

Tất cả các tùy chọn dòng lệnh được mô tả trong :ref:`using-on-general`.


.. _tut-argpassing:

Truyền đối số
-------------

Khi được trình thông dịch nhận diện, tên script và các đối số bổ sung theo sau sẽ được chuyển thành một danh sách các chuỗi và gán cho biến ``argv`` trong mô-đun ``sys``. Bạn có thể truy cập danh sách này bằng cách thực thi ``import sys``. Độ dài của danh sách ít nhất là một; khi không cung cấp script và không có đối số nào, ``sys.argv[0]`` là một chuỗi rỗng. Khi tên script được cung cấp dưới dạng ``'-'`` (nghĩa là đầu vào chuẩn), ``sys.argv[0]`` được đặt thành ``'-'``. Khi
:option:`-c` *command* được sử dụng, ``sys.argv[0]`` được đặt thành ``'-c'``. Khi
:option:`-m` *module* được sử dụng, ``sys.argv[0]`` được đặt thành tên đầy đủ của mô-đun được tìm thấy. Các tùy chọn xuất hiện sau :option:`-c` *command* hoặc :option:`-m` *module* không bị trình thông dịch Python xử lý mà được giữ lại trong ``sys.argv`` để command hoặc module xử lý.


.. _tut-interactive:

Chế độ tương tác
----------------

Khi các lệnh được đọc từ tty, trình thông dịch được cho là đang ở *interactive mode*. Ở chế độ này, trình thông dịch nhắc nhập lệnh tiếp theo bằng *primary prompt*, thường là ba dấu lớn hơn (``>>>``); đối với các dòng tiếp diễn, trình thông dịch nhắc bằng *secondary prompt*, theo mặc định là ba dấu chấm (``...``). Trình thông dịch in một thông báo chào mừng nêu số phiên bản và thông báo bản quyền trước khi in lời nhắc đầu tiên:

.. code-block:: shell-session

   $ python3.14
   Python 3.14 (default, April 4 2024, 09:25:04)
   [GCC 10.2.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

.. XXX update for new releases

Các dòng tiếp diễn là cần thiết khi nhập một cấu trúc nhiều dòng. Ví dụ, hãy xem :keyword:`if` statement này::

   >>> the_world_is_flat = True
   >>> if the_world_is_flat:
   ...     print("Be careful not to fall off!")
   ...
   Be careful not to fall off!


Để biết thêm về chế độ tương tác, hãy xem :ref:`tut-interac`.


.. _tut-interp:

Trình thông dịch và môi trường của nó
=====================================


.. _tut-source-encoding:

Mã hóa mã nguồn
---------------

Theo mặc định, các tệp mã nguồn Python được coi là được mã hóa theo UTF-8. Với encoding đó, ký tự của hầu hết các ngôn ngữ trên thế giới có thể được sử dụng đồng thời trong string literal, identifier và comment --- mặc dù standard library chỉ sử dụng ký tự ASCII cho identifier, một quy ước mà mọi mã có tính portable nên tuân theo. Để hiển thị đúng tất cả các ký tự này, editor của bạn phải nhận biết rằng tệp sử dụng UTF-8 và phải sử dụng font hỗ trợ tất cả các ký tự trong tệp.

Để khai báo một encoding khác với encoding mặc định, cần thêm một dòng comment đặc biệt làm dòng *đầu tiên* của tệp. Cú pháp như sau::

   # -*- coding: encoding -*-

trong đó *encoding* là một trong các :mod:`codecs` hợp lệ được Python hỗ trợ.

Ví dụ, để khai báo rằng encoding Windows-1252 sẽ được sử dụng, dòng đầu tiên của tệp source code phải là::

   # -*- coding: cp1252 -*-

Một ngoại lệ đối với quy tắc *dòng đầu tiên* là khi source code bắt đầu bằng một
:ref:`dòng UNIX "shebang" <tut-scripts>`.  Trong trường hợp này, khai báo encoding phải được thêm vào dòng thứ hai của tệp.  Ví dụ::

   #!/usr/bin/env python3
   # -*- coding: cp1252 -*-

.. rubric:: Chú thích cuối trang

.. [#] Trên Unix, trình thông dịch Python 3.x theo mặc định không được cài đặt với tên tệp thực thi là ``python``, để không xung đột với tệp thực thi Python 2.x được cài đặt đồng thời.
