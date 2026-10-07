.. _freethreading-python-howto:

**********************************
Hỗ trợ free threading trong Python
**********************************

Bắt đầu từ bản phát hành 3.13, CPython hỗ trợ một bản build Python có tên là :term:`free threading` trong đó :term:`global interpreter lock` (GIL) bị vô hiệu hóa.  Việc thực thi free-threaded cho phép tận dụng toàn bộ năng lực xử lý hiện có bằng cách chạy các thread song song trên các lõi CPU khả dụng. Mặc dù không phải mọi phần mềm đều tự động hưởng lợi từ điều này, các chương trình được thiết kế có tính đến threading sẽ chạy nhanh hơn trên phần cứng đa lõi.

Một số package bên thứ ba, đặc biệt là những package có :term:`extension module`, có thể chưa sẵn sàng để sử dụng trong bản build free-threaded và sẽ bật lại :term:`GIL`.

Tài liệu này mô tả những tác động của free threading đối với mã Python.  Xem :ref:`freethreading-extensions-howto` để biết thông tin về cách viết các phần mở rộng C hỗ trợ bản build free-threaded.

.. seealso::

   :pep:`703` – Mô tả tổng quan về việc làm cho Global Interpreter Lock trở thành tùy chọn trong CPython.


Cài đặt
=======

Bắt đầu từ Python 3.13, các trình cài đặt chính thức cho macOS và Windows tùy chọn hỗ trợ cài đặt các binary Python free-threaded.  Các trình cài đặt có tại https://www.python.org/downloads/.

Để biết thông tin về các nền tảng khác, hãy xem `Hướng dẫn cài đặt Python không GIL <https://py-free-threading.github.io/installing-cpython/>`_, một hướng dẫn cài đặt Python không GIL do cộng đồng duy trì.

Khi xây dựng CPython từ mã nguồn, nên sử dụng tùy chọn cấu hình :option:`--disable-gil` để xây dựng một trình thông dịch Python không GIL.


Xác định Python không GIL
=========================

Để kiểm tra xem trình thông dịch hiện tại có hỗ trợ free-threading hay không, :option:`python -VV <-V>` và :data:`sys.version` chứa "free-threading build". Có thể sử dụng hàm :func:`sys._is_gil_enabled` mới để kiểm tra xem GIL có thực sự bị vô hiệu hóa trong tiến trình đang chạy hay không.

Có thể sử dụng biến cấu hình ``sysconfig.get_config_var("Py_GIL_DISABLED")`` để xác định liệu bản build có hỗ trợ free threading hay không. Nếu biến này được đặt thành ``1``, thì bản build hỗ trợ free threading. Đây là cơ chế được khuyến nghị để đưa ra các quyết định liên quan đến cấu hình bản build.


Global interpreter lock trong Python không GIL
==============================================

Các bản build không GIL của CPython hỗ trợ tùy chọn chạy với GIL được bật tại runtime bằng biến môi trường :envvar:`PYTHON_GIL` hoặc tùy chọn dòng lệnh :option:`-X gil`.

GIL cũng có thể được tự động bật khi import một extension module C-API không được đánh dấu rõ ràng là hỗ trợ free threading. Trong trường hợp này, một cảnh báo sẽ được in ra.

Ngoài tài liệu của từng package, các website sau đây theo dõi trạng thái hỗ trợ free threading của các package phổ biến:

* https://py-free-threading.github.io/tracking/
* https://hugovk.github.io/free-threaded-wheels/


Tính an toàn luồng
==================

Bản build free-threaded của CPython hướng đến việc cung cấp hành vi an toàn luồng ở cấp độ Python tương tự bản build mặc định có bật GIL. Các kiểu tích hợp như :class:`dict`, :class:`list` và :class:`set` sử dụng các khóa nội bộ để bảo vệ khỏi những sửa đổi đồng thời theo cách tương tự GIL. Xem :ref:`threadsafety` để biết các đảm bảo do các kiểu tích hợp cung cấp.

.. note::

   Bạn nên sử dụng :class:`threading.Lock` hoặc các primitive đồng bộ hóa khác thay vì dựa vào các khóa nội bộ của kiểu tích hợp, nếu có thể.


Các hạn chế đã biết
===================

Phần này mô tả các hạn chế đã biết của bản build free-threaded CPython.

Bất tử hóa
----------

Trong bản build free-threaded, một số đối tượng được :term:`immortal`. Các đối tượng bất tử không bị giải phóng và có số lượng tham chiếu không bao giờ bị thay đổi. Điều này nhằm tránh tranh chấp số lượng tham chiếu, vốn sẽ ngăn cản việc mở rộng hiệu quả khi chạy đa luồng.

Kể từ bản phát hành 3.14, việc bất tử hóa chỉ giới hạn ở:

* Các hằng số mã: các literal số, literal chuỗi và literal tuple được tạo thành từ các hằng số khác.
* Các chuỗi được intern bởi :func:`sys.intern`.


Đối tượng frame
---------------

Không an toàn khi truy cập :attr:`frame.f_locals` từ một đối tượng :ref:`frame <frame-objects>` nếu frame đó hiện đang được thực thi trong một thread khác; việc này có thể làm trình thông dịch bị crash.


Iterator
--------

Nhìn chung, việc truy cập cùng một đối tượng iterator từ nhiều thread đồng thời là không an toàn với thread, và các thread có thể thấy các phần tử bị trùng lặp hoặc bị thiếu.


Hiệu năng đơn thread
--------------------

Bản build free-threaded có thêm overhead khi thực thi mã Python so với bản build mặc định có bật GIL. Mức overhead phụ thuộc vào workload và phần cứng. Trên bộ benchmark pyperformance, overhead trung bình dao động từ khoảng 1% trên macOS aarch64 đến 8% trên các hệ thống Linux x86-64.


Các thay đổi về hành vi
=======================

Phần này mô tả các thay đổi về hành vi của CPython với bản build free-threaded.


Biến ngữ cảnh
-------------

Trong bản dựng free-threaded, cờ :data:`~sys.flags.thread_inherit_context` được đặt thành true theo mặc định, khiến các thread được tạo bằng
:class:`threading.Thread` bắt đầu với một bản sao của
:class:`~contextvars.Context()` của bên gọi
:meth:`~threading.Thread.start`.  Trong bản dựng bật GIL mặc định, cờ này mặc định là false, vì vậy các thread bắt đầu với một :class:`~contextvars.Context()` trống.


Bộ lọc cảnh báo
---------------

Trong bản dựng free-threaded, cờ :data:`~sys.flags.context_aware_warnings` được đặt thành true theo mặc định.  Trong bản dựng bật GIL mặc định, cờ này mặc định là false.  Nếu cờ là true thì context manager :class:`warnings.catch_warnings` sử dụng một biến context cho các bộ lọc cảnh báo.  Nếu cờ là false thì :class:`~warnings.catch_warnings` sửa đổi danh sách bộ lọc toàn cục, vốn không an toàn khi sử dụng với nhiều thread.  Xem module :mod:`warnings` để biết thêm chi tiết.


Mức sử dụng bộ nhớ tăng
-----------------------

Bản dựng free-threaded thường sẽ sử dụng nhiều bộ nhớ hơn so với bản dựng mặc định. Có nhiều lý do cho điều này, phần lớn bắt nguồn từ các quyết định thiết kế.


Tất cả chuỗi interned đều bất tử
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Đối với các phiên bản Python hiện đại (kể từ phiên bản 2.3), việc intern một chuỗi (ví dụ bằng
:func:`sys.intern`) không khiến chuỗi đó trở thành bất tử. Thay vào đó, nếu tham chiếu cuối cùng đến chuỗi đó biến mất, chuỗi sẽ bị xóa khỏi bảng chuỗi interned. Điều này không đúng với bản dựng free-threaded và mọi chuỗi interned sẽ trở thành bất tử, tồn tại cho đến khi trình thông dịch tắt.


Các đối tượng không thuộc GC có phần header đối tượng lớn hơn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bản dựng free-threaded sử dụng cấu trúc :c:type:`PyObject` khác. Thay vì có thông tin liên quan đến GC được cấp phát trước cấu trúc :c:type:`PyObject` như trong bản dựng mặc định, thông tin liên quan đến GC là một phần của header đối tượng thông thường. Ví dụ, trên nền tảng AMD64, ``None`` sử dụng 32 byte trong bản dựng free-threaded, so với 16 byte trong bản dựng mặc định. Các đối tượng GC (chẳng hạn như dict và list) có cùng kích thước trong cả hai bản dựng, vì bản dựng free-threaded không sử dụng thêm không gian cho thông tin GC.


QSBR có thể trì hoãn việc giải phóng bộ nhớ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để triển khai an toàn các cấu trúc dữ liệu không khóa, một lược đồ thu hồi bộ nhớ an toàn (safe memory reclamation - SMR) được sử dụng, được gọi là thu hồi dựa trên trạng thái ổn định (quiescent state-based reclamation - QSBR). Điều này có nghĩa là bộ nhớ hỗ trợ các cấu trúc dữ liệu cho phép truy cập không khóa sẽ sử dụng QSBR, trì hoãn thao tác giải phóng thay vì giải phóng bộ nhớ ngay lập tức. Hai ví dụ về các cấu trúc dữ liệu này là đối tượng list và đối tượng dictionary keys. Xem ``InternalDocs/qsbr.md`` trong cây mã nguồn CPython để biết thêm chi tiết về cách QSBR được triển khai. Đang chạy
:func:`gc.collect` sẽ khiến toàn bộ bộ nhớ đang được QSBR giữ thực sự được giải phóng. Lưu ý rằng ngay cả khi QSBR giải phóng bộ nhớ, bộ cấp phát bộ nhớ bên dưới có thể không ngay lập tức trả lại bộ nhớ đó cho hệ điều hành, vì vậy kích thước tập thường trú (RSS) của tiến trình có thể không giảm.


bộ cấp phát mimalloc so với pymalloc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bản build mặc định thường sử dụng bộ cấp phát bộ nhớ "pymalloc" cho các lần cấp phát nhỏ (512 byte trở xuống). Bản build free-threaded không sử dụng pymalloc và cấp phát tất cả đối tượng Python bằng bộ cấp phát "mimalloc". Bộ cấp phát pymalloc có các đặc tính sau giúp duy trì mức sử dụng bộ nhớ thấp: chi phí phụ trên mỗi khối được cấp phát thấp, ngăn phân mảnh bộ nhớ hiệu quả và nhanh chóng trả lại bộ nhớ trống cho hệ điều hành. Bộ cấp phát mimalloc cũng hoạt động khá tốt ở những khía cạnh này, nhưng có thể có thêm một phần chi phí phụ.

Trong bản build free-threaded, mimalloc quản lý bộ nhớ trong một số heap riêng biệt (hiện tại là bốn). Ví dụ, tất cả đối tượng hỗ trợ GC được cấp phát từ heap riêng của chúng. Việc sử dụng các heap riêng biệt có nghĩa là bộ nhớ trống trong một heap không thể được dùng cho một lần cấp phát sử dụng heap khác. Ngoài ra, một số heap được cấu hình để sử dụng QSBR (thu hồi dựa trên trạng thái ổn định) khi giải phóng bộ nhớ hỗ trợ heap đó (được gọi là "pages" trong thuật ngữ của mimalloc). Việc sử dụng QSBR tạo ra độ trễ giữa thời điểm tất cả khối bộ nhớ của một page được giải phóng và thời điểm page bộ nhớ được giải phóng để dùng cho các lần cấp phát mới hoặc trả lại cho hệ điều hành.

Bộ cấp phát mimalloc cũng trì hoãn việc trả lại bộ nhớ đã giải phóng cho hệ điều hành. Bạn có thể giảm độ trễ đó bằng cách đặt biến môi trường
:envvar:`!MIMALLOC_PURGE_DELAY` thành ``0``. Lưu ý rằng điều này có thể làm giảm hiệu suất của bộ cấp phát.


Đếm tham chiếu không khóa có thể khiến các đối tượng tồn tại lâu hơn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trong bản dựng mặc định, khi số lượng tham chiếu của một đối tượng về 0, đối tượng đó thường được giải phóng. Bản dựng không khóa sử dụng "biased reference counting", với đường đi nhanh cho các đối tượng được luồng hiện tại "sở hữu" và đường đi chậm cho các đối tượng khác. Xem :pep:`703` để biết thêm chi tiết. Bất cứ khi nào số lượng tham chiếu của một đối tượng kết thúc ở trạng thái "queued", việc giải phóng có thể bị trì hoãn. Trạng thái queued được xóa khỏi phần "eval breaker" của trình đánh giá bytecode.

Bản dựng không khóa cũng cho phép một chế độ đếm tham chiếu khác, được gọi là "deferred reference counting". Chế độ này được bật bằng cách thiết lập một cờ riêng cho từng đối tượng. Đếm tham chiếu trì hoãn được bật cho các kiểu sau:

* các đối tượng module
* các hàm cấp cao nhất của module
* các phương thức lớp được định nghĩa trong phạm vi lớp
* các đối tượng descriptor
* các đối tượng cục bộ theo thread, được tạo bởi :class:`threading.local`

Khi tính reference count trì hoãn được bật, các tham chiếu từ stack của hàm Python không được cộng vào reference count. Cơ chế này làm giảm overhead của việc tính reference count, đặc biệt đối với các đối tượng được sử dụng từ nhiều thread. Vì các tham chiếu trên stack không được tính, các đối tượng sử dụng tính reference count trì hoãn không được giải phóng ngay khi reference count nội bộ của chúng giảm xuống 0. Thay vào đó, chúng được kiểm tra trong lần chạy GC tiếp theo và được giải phóng nếu không tìm thấy tham chiếu nào trên stack đến chúng. Điều này có nghĩa là các đối tượng này được GC giải phóng thay vì được giải phóng khi reference count của chúng giảm xuống 0, như thông thường.


Tính reference count theo từng thread có thể trì hoãn việc giải phóng đối tượng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để tránh tranh chấp trên các trường reference count của những đối tượng thường xuyên được chia sẻ, bản build free-threaded cũng sử dụng "tính reference count theo từng thread" cho một số ít kiểu đối tượng được chọn. Thay vì cập nhật một reference count dùng chung duy nhất, mỗi thread duy trì mảng reference count cục bộ riêng, được lập chỉ mục bằng một ID duy nhất được gán cho đối tượng. Reference count thực chỉ được tính bằng cách cộng các reference count theo từng thread khi reference count cục bộ của đối tượng giảm xuống 0. Hiện tại, tính reference count theo từng thread được sử dụng cho:

* các đối tượng kiểu heap (các lớp được tạo trong Python)
* các đối tượng code
* ``__dict__`` của các đối tượng module

Vì các số đếm theo từng thread phải được hợp nhất trở lại vào đối tượng trước khi đối tượng đó có thể được giải phóng, các đối tượng sử dụng cơ chế đếm tham chiếu theo từng thread thường được giải phóng muộn hơn so với trong bản dựng mặc định. Cụ thể, một đối tượng như vậy thường chỉ được giải phóng khi thread đã tham chiếu đến nó đạt đến một điểm an toàn (chẳng hạn như trong phần "eval breaker" của trình đánh giá bytecode) hoặc thoát. Việc chạy :func:`gc.collect` sẽ hợp nhất các số đếm theo từng thread và cho phép giải phóng các đối tượng này.

.. _`Installing a Free-Threaded Python`: https://py-free-threading.github.io/installing-cpython/
