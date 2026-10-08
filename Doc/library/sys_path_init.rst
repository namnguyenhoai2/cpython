.. _sys-path-init:

Việc khởi tạo đường dẫn tìm kiếm module :data:`sys.path`
========================================================

Đường dẫn tìm kiếm module được khởi tạo khi Python khởi động. Có thể truy cập đường dẫn tìm kiếm module này tại :data:`sys.path`.

Mục đầu tiên trong đường dẫn tìm kiếm module là thư mục chứa script đầu vào, nếu có. Nếu không, mục đầu tiên là thư mục hiện tại, áp dụng khi thực thi shell tương tác, lệnh :option:`-c`, hoặc module :option:`-m`.

Biến môi trường :envvar:`PYTHONPATH` thường được dùng để thêm các thư mục vào đường dẫn tìm kiếm. Nếu tìm thấy biến môi trường này, nội dung của nó sẽ được thêm vào đường dẫn tìm kiếm module.

.. note::

   :envvar:`PYTHONPATH` sẽ ảnh hưởng đến tất cả các phiên bản/môi trường Python đã cài đặt. Hãy thận trọng khi đặt biến này trong shell profile hoặc các biến môi trường toàn cục. Module :mod:`site` cung cấp những kỹ thuật tinh vi hơn như được đề cập bên dưới.

Các mục tiếp theo được thêm vào là những thư mục chứa các module Python chuẩn, cũng như bất kỳ :term:`extension module`\s nào mà các module này phụ thuộc vào. Các extension module là các tệp ``.pyd`` trên Windows và các tệp ``.so`` trên các nền tảng khác. Thư mục chứa các module Python độc lập với nền tảng được gọi là ``prefix``. Thư mục chứa các extension module được gọi là ``exec_prefix``.

Có thể sử dụng biến môi trường :envvar:`PYTHONHOME` để đặt vị trí của ``prefix`` và ``exec_prefix``. Nếu không, các thư mục này được tìm thấy bằng cách lấy tệp thực thi Python làm điểm bắt đầu, sau đó tìm nhiều tệp và thư mục 'mốc' khác nhau. Lưu ý rằng mọi symbolic link đều được truy theo, vì vậy vị trí thực của tệp thực thi Python được dùng làm điểm bắt đầu tìm kiếm. Vị trí của tệp thực thi Python được gọi là ``home``.

Sau khi ``home`` được xác định, thư mục ``prefix`` được tìm thấy bằng cách trước tiên tìm :file:`python{majorversion}{minorversion}.zip` (``python311.zip``). Trên Windows, kho lưu trữ zip được tìm trong ``home``, còn trên Unix, kho lưu trữ được dự kiến nằm trong :file:`lib`. Lưu ý rằng vị trí dự kiến của kho lưu trữ zip được thêm vào đường dẫn tìm kiếm module ngay cả khi kho lưu trữ không tồn tại. Nếu không tìm thấy kho lưu trữ nào, Python trên Windows sẽ tiếp tục tìm ``prefix`` bằng cách tìm :file:`Lib\\os.py`. Python trên Unix sẽ tìm :file:`lib/python{majorversion}.{minorversion}/os.py` (``lib/python3.11/os.py``). Trên Windows, ``prefix`` và ``exec_prefix`` là một, tuy nhiên trên các nền tảng khác, :file:`lib/python{majorversion}.{minorversion}/lib-dynload` (``lib/python3.11/lib-dynload``) được tìm kiếm và sử dụng làm mốc cho ``exec_prefix``. Trên một số nền tảng, :file:`lib` có thể là :file:`lib64` hoặc một giá trị khác; xem :data:`sys.platlibdir` và :envvar:`PYTHONPLATLIBDIR`.

Sau khi được tìm thấy, ``prefix`` và ``exec_prefix`` sẽ khả dụng tại
:data:`sys.base_prefix` và :data:`sys.base_exec_prefix`, tương ứng.

Nếu :envvar:`PYTHONHOME` chưa được thiết lập và tìm thấy tệp ``pyvenv.cfg`` bên cạnh tệp thực thi chính hoặc trong thư mục cha của nó, :data:`sys.prefix` và
:data:`sys.exec_prefix` được đặt thành thư mục chứa ``pyvenv.cfg``; nếu không, chúng được đặt thành cùng giá trị với :data:`sys.base_prefix` và
:data:`sys.base_exec_prefix`, tương ứng. Điều này được :ref:`sys-path-init-virtual-environments` sử dụng.

Cuối cùng, module :mod:`site` được xử lý và các thư mục :file:`site-packages` được thêm vào đường dẫn tìm kiếm module. Một cách phổ biến để tùy chỉnh đường dẫn tìm kiếm là tạo các module :mod:`sitecustomize` hoặc :mod:`usercustomize` như được mô tả trong tài liệu module :mod:`site`.

.. note::

   Một số tùy chọn dòng lệnh có thể tiếp tục ảnh hưởng đến việc tính toán đường dẫn. Xem :option:`-E`, :option:`-I`, :option:`-s` và :option:`-S` để biết thêm chi tiết.

.. versionchanged:: 3.14

   :data:`sys.prefix` và :data:`sys.exec_prefix` hiện được đặt thành thư mục ``pyvenv.cfg`` trong quá trình khởi tạo đường dẫn. Trước đây, việc này được thực hiện bởi :mod:`site`, vì vậy chịu ảnh hưởng của :option:`-S`.

.. _sys-path-init-virtual-environments:

Môi trường ảo
-------------

Môi trường ảo đặt một tệp ``pyvenv.cfg`` trong prefix của chúng, khiến
:data:`sys.prefix` và :data:`sys.exec_prefix` trỏ đến chúng thay vì bản cài đặt cơ sở.

Các giá trị ``prefix`` và ``exec_prefix`` của bản cài đặt cơ sở có tại :data:`sys.base_prefix` và :data:`sys.base_exec_prefix`.

Ngoài việc được sử dụng làm dấu hiệu để nhận diện các môi trường ảo, ``pyvenv.cfg`` cũng có thể được sử dụng để cấu hình việc khởi tạo :mod:`site`. Vui lòng tham khảo :mod:`site`'s
:ref:`tài liệu về môi trường ảo <site-virtual-environments-configuration>`.

.. note::

   :envvar:`PYTHONHOME` ghi đè việc phát hiện ``pyvenv.cfg``.

.. note::

   Có những cách khác để triển khai "môi trường ảo"; tài liệu này đề cập đến các cách triển khai dựa trên cơ chế ``pyvenv.cfg``, chẳng hạn như :mod:`venv`. Hầu hết các triển khai môi trường ảo đều tuân theo mô hình do :mod:`venv` thiết lập, nhưng cũng có thể có những triển khai đặc biệt không tuân theo mô hình này.

_pth files
----------

Để ghi đè hoàn toàn :data:`sys.path`, hãy tạo tệp ``._pth`` có cùng tên với thư viện dùng chung hoặc tệp thực thi (``python._pth`` hoặc ``python311._pth``). Trên Windows, đường dẫn đến thư viện dùng chung luôn được biết, tuy nhiên đường dẫn này có thể không khả dụng trên các nền tảng khác. Trong tệp ``._pth``, hãy chỉ định mỗi đường dẫn cần thêm vào :data:`sys.path` trên một dòng riêng. Tệp dựa trên tên thư viện dùng chung sẽ ghi đè tệp dựa trên tệp thực thi, nhờ đó có thể hạn chế các đường dẫn cho mọi chương trình tải runtime nếu muốn.

Khi tệp này tồn tại, mọi biến registry và biến môi trường đều bị bỏ qua, chế độ cô lập được bật, và :mod:`site` không được import trừ khi một dòng trong tệp chỉ định ``import site``. Các đường dẫn trống và những dòng bắt đầu bằng ``#`` sẽ bị bỏ qua. Mỗi đường dẫn có thể là đường dẫn tuyệt đối hoặc tương đối so với vị trí của tệp. Không cho phép các câu lệnh import ngoài câu lệnh import ``site``, và không thể chỉ định mã tùy ý.

Lưu ý rằng các tệp ``.pth`` (không có dấu gạch dưới ở đầu) sẽ được module :mod:`site` xử lý bình thường khi ``import site`` đã được chỉ định.

Python nhúng
------------

Nếu Python được nhúng trong một ứng dụng khác :c:func:`Py_InitializeFromConfig` thì có thể sử dụng cấu trúc :c:type:`PyConfig` để khởi tạo Python. Các chi tiết cụ thể về đường dẫn được mô tả tại :ref:`init-path-config`.

.. seealso::

   * :ref:`windows_finding_modules` để xem các ghi chú chi tiết dành cho Windows.
   * :ref:`using-on-unix` để xem thông tin chi tiết dành cho Unix.
