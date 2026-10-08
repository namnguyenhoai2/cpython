:mod:`!runpy` --- Định vị và thực thi các module Python
=======================================================

.. module:: runpy
   :synopsis: Định vị và chạy các module Python mà không cần import chúng trước.

.. moduleauthor:: Nick Coghlan <ncoghlan@gmail.com>

**Mã nguồn:** :source:`Lib/runpy.py`

--------------

Module :mod:`!runpy` được dùng để định vị và chạy các module Python mà không cần import chúng trước. Công dụng chính của module này là triển khai tùy chọn dòng lệnh :option:`-m`, cho phép định vị các tập lệnh bằng namespace module Python thay vì hệ thống tệp.

Lưu ý rằng đây *không* phải là một module sandbox - mọi mã đều được thực thi trong tiến trình hiện tại và mọi tác dụng phụ (chẳng hạn như các module khác được import và lưu vào bộ nhớ đệm) sẽ vẫn tồn tại sau khi các hàm trả về.

Ngoài ra, mọi hàm và lớp được định nghĩa bởi mã đã thực thi không được đảm bảo sẽ hoạt động chính xác sau khi hàm :mod:`!runpy` trả về. Nếu giới hạn này không thể chấp nhận trong một trường hợp sử dụng cụ thể, :mod:`importlib` có thể sẽ là lựa chọn phù hợp hơn module này.

Module :mod:`!runpy` cung cấp hai hàm:


.. function:: run_module(mod_name, init_globals=None, run_name=None, alter_sys=False)

   .. index::
      pair: module; __main__

   Thực thi mã của module được chỉ định và trả về từ điển biến toàn cục của module kết quả. Mã của module trước tiên được định vị bằng cơ chế import tiêu chuẩn (xem :pep:`302` để biết chi tiết), sau đó được thực thi trong một namespace module mới.

   Đối số *mod_name* phải là tên module tuyệt đối. Nếu tên module tham chiếu đến một package thay vì một module thông thường, package đó sẽ được import, sau đó module con :mod:`__main__` trong package đó sẽ được thực thi và từ điển biến toàn cục của module kết quả sẽ được trả về.

   Có thể sử dụng đối số từ điển tùy chọn *init_globals* để điền trước từ điển biến toàn cục của module trước khi mã được thực thi. *init_globals* sẽ không bị sửa đổi. Nếu bất kỳ biến toàn cục đặc biệt nào bên dưới được định nghĩa trong *init_globals*, các định nghĩa đó sẽ bị :func:`run_module` ghi đè.

   Các biến toàn cục đặc biệt ``__name__``, ``__spec__``, ``__file__``, ``__cached__``, ``__loader__`` và ``__package__`` được thiết lập trong từ điển biến toàn cục trước khi mã module được thực thi. (Lưu ý rằng đây là tập biến tối thiểu - các biến khác có thể được thiết lập ngầm như một chi tiết triển khai của trình thông dịch.)

   ``__name__`` được đặt thành *run_name* nếu đối số tùy chọn này không
   :const:`None`, thành ``mod_name + '.__main__'`` nếu module được đặt tên là một package và thành đối số *mod_name* trong các trường hợp khác.

   ``__spec__`` sẽ được thiết lập phù hợp với module được import *actually* (nghĩa là, ``__spec__.name`` sẽ luôn là *mod_name* hoặc ``mod_name + '.__main__'``, không bao giờ là *run_name*).

   ``__file__``, ``__cached__``, ``__loader__`` và ``__package__`` là
   :ref:`được đặt như bình thường <import-mod-attrs>` dựa trên đặc tả mô-đun.

   Nếu cung cấp đối số *alter_sys* và đối số này cho kết quả là :const:`True`, thì ``sys.argv[0]`` được cập nhật bằng giá trị của ``__file__`` và ``sys.modules[__name__]`` được cập nhật bằng một đối tượng mô-đun tạm thời cho mô-đun đang được thực thi. Cả ``sys.argv[0]`` và ``sys.modules[__name__]`` đều được khôi phục về giá trị ban đầu trước khi hàm trả về.

   Lưu ý rằng việc thao tác với :mod:`sys` này không an toàn đối với thread. Các thread khác có thể thấy mô-đun mới chỉ được khởi tạo một phần, cũng như danh sách đối số đã bị thay đổi. Khuyến nghị không can thiệp vào mô-đun ``sys`` khi gọi hàm này từ mã sử dụng nhiều thread.

   .. seealso::
      Tùy chọn :option:`-m` cung cấp chức năng tương đương từ dòng lệnh.

   .. versionchanged:: 3.1
      Đã bổ sung khả năng thực thi các package bằng cách tìm một mô-đun con :mod:`__main__`.

   .. versionchanged:: 3.2
      Đã bổ sung biến toàn cục ``__cached__`` (xem :pep:`3147`).

   .. versionchanged:: 3.4
      Đã được cập nhật để tận dụng tính năng module spec được bổ sung trong
      :pep:`451`. Điều này cho phép ``__cached__`` được thiết lập chính xác cho các module được chạy theo cách này, đồng thời đảm bảo tên module thực luôn có thể truy cập dưới dạng ``__spec__.name``.

   .. versionchanged:: 3.12
      Việc thiết lập ``__cached__``, ``__loader__`` và ``__package__`` đã bị loại bỏ. Xem
      :class:`~importlib.machinery.ModuleSpec` để biết các lựa chọn thay thế.

.. function:: run_path(path_name, init_globals=None, run_name=None)

   .. index::
      pair: module; __main__

   Thực thi mã tại vị trí được đặt tên trên hệ thống tệp và trả về dictionary globals của module tạo ra. Tương tự tên script được cung cấp cho dòng lệnh CPython, *file_path* có thể tham chiếu đến tệp mã nguồn Python, tệp bytecode đã biên dịch hoặc mục nhập :data:`sys.path` hợp lệ chứa một
   :mod:`__main__` module (ví dụ: một zipfile chứa tệp :file:`__main__.py` ở cấp cao nhất).

   Đối với một script đơn giản, mã được chỉ định sẽ được thực thi trực tiếp trong một namespace module mới. Đối với một mục nhập :data:`sys.path` hợp lệ (thường là một zipfile hoặc thư mục), mục nhập đó trước tiên được thêm vào đầu ``sys.path``. Sau đó, hàm tìm và thực thi một module :mod:`__main__` bằng đường dẫn đã cập nhật. Lưu ý rằng không có cơ chế bảo vệ đặc biệt nào chống lại việc gọi một mục nhập ``__main__`` hiện có nằm ở nơi khác trên ``sys.path`` nếu tại vị trí được chỉ định không có module như vậy.

   Đối số từ điển tùy chọn *init_globals* có thể được dùng để điền trước từ điển biến toàn cục của module trước khi thực thi mã. *init_globals* sẽ không bị sửa đổi. Nếu bất kỳ biến toàn cục đặc biệt nào dưới đây được định nghĩa trong *init_globals*, các định nghĩa đó sẽ bị :func:`run_path` ghi đè.

   Các biến toàn cục đặc biệt ``__name__``, ``__spec__``, ``__file__``, ``__cached__``, ``__loader__`` và ``__package__`` được thiết lập trong từ điển biến toàn cục trước khi mã module được thực thi. (Lưu ý rằng đây là tập biến tối thiểu - các biến khác có thể được thiết lập ngầm như một chi tiết triển khai của trình thông dịch.)

   ``__name__`` được đặt thành *run_name* nếu đối số tùy chọn này không
   :const:`None` và thành ``'<run_path>'`` trong trường hợp ngược lại.

   Nếu *file_path* tham chiếu trực tiếp đến một tệp script (dù là mã nguồn hay byte code đã biên dịch trước), thì ``__file__`` sẽ được đặt thành *file_path*, còn ``__spec__``, ``__cached__``, ``__loader__`` và ``__package__`` đều sẽ được đặt thành :const:`None`.

   Nếu *file_path* tham chiếu đến một mục nhập :data:`sys.path` hợp lệ, thì ``__spec__`` sẽ được đặt phù hợp với module :mod:`__main__` đã import (nghĩa là ``__spec__.name`` sẽ luôn là ``__main__``). ``__file__``, ``__cached__``, ``__loader__`` và ``__package__`` sẽ là
   :ref:`được đặt như bình thường <import-mod-attrs>` dựa trên đặc tả mô-đun.

   Một số thay đổi cũng được thực hiện đối với mô-đun :mod:`sys`. Trước tiên,
   :data:`sys.path` có thể được thay đổi như mô tả ở trên. ``sys.argv[0]`` được cập nhật với giá trị của *file_path* và ``sys.modules[__name__]`` được cập nhật bằng một đối tượng mô-đun tạm thời cho mô-đun đang được thực thi. Mọi thay đổi đối với các mục trong :mod:`sys` sẽ được hoàn tác trước khi hàm trả về.

   Lưu ý rằng, không giống như :func:`run_module`, các thay đổi được thực hiện đối với :mod:`sys` không phải là tùy chọn trong hàm này, vì những điều chỉnh này rất cần thiết để cho phép thực thi các mục :data:`sys.path`. Do các hạn chế về tính an toàn luồng vẫn được áp dụng, việc sử dụng hàm này trong mã đa luồng phải được tuần tự hóa bằng import lock hoặc ủy thác cho một quy trình riêng.

   .. seealso::
      :ref:`using-on-interface-options` for equivalent functionality on the
      dòng lệnh (``python path/to/script``).

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Đã được cập nhật để tận dụng tính năng module spec được bổ sung trong
      :pep:`451`. Điều này cho phép đặt ``__cached__`` đúng cách trong trường hợp ``__main__`` được import từ một mục :data:`sys.path` hợp lệ thay vì được thực thi trực tiếp.

   .. versionchanged:: 3.12
      Việc thiết lập ``__cached__``, ``__loader__`` và ``__package__`` không còn được khuyến nghị.

.. seealso::

   :pep:`338` -- Thực thi các mô-đun dưới dạng tập lệnh
      PEP do Nick Coghlan viết và triển khai.

   :pep:`366` -- Nhập tương đối tường minh trong mô-đun chính
      PEP do Nick Coghlan viết và triển khai.

   :pep:`451` -- Kiểu ModuleSpec cho hệ thống import
      PEP do Eric Snow viết và triển khai

   :ref:`using-on-general` - Chi tiết dòng lệnh CPython

   Hàm :func:`importlib.import_module`
