:mod:`!pkgutil` --- Tiện ích mở rộng package
============================================

.. module:: pkgutil
   :synopsis: Các tiện ích cho hệ thống import.

**Mã nguồn:** :source:`Lib/pkgutil.py`

--------------

Module này cung cấp các tiện ích cho hệ thống import, đặc biệt là hỗ trợ package.

.. class:: ModuleInfo(module_finder, name, ispkg)

    Một namedtuple chứa bản tóm tắt ngắn gọn về thông tin của một module.

    .. versionadded:: 3.6

.. function:: extend_path(path, name)

   Mở rộng đường dẫn tìm kiếm cho các module cấu thành một package. Mục đích sử dụng là đặt đoạn mã sau trong :file:`__init__.py` của một package::

      from pkgutil import extend_path
      __path__ = extend_path(__path__, __name__)

   Đối với mỗi thư mục trên :data:`sys.path` có một thư mục con khớp với tên package, hãy thêm thư mục con đó vào
   :attr:`~module.__path__`. Điều này hữu ích nếu muốn phân phối các phần khác nhau của một package logic duy nhất dưới dạng nhiều thư mục.

   Nó cũng tìm các tệp :file:`\*.pkg` bắt đầu tại vị trí mà ``*`` khớp với đối số *name*. Tính năng này tương tự các tệp :file:`\*.pth` (xem
   module :mod:`site` để biết thêm thông tin), ngoại trừ việc nó không xử lý đặc biệt các dòng bắt đầu bằng ``import``. Một tệp :file:`\*.pkg` được tin cậy hoàn toàn: ngoài việc bỏ qua các dòng trống và bỏ qua chú thích, mọi mục được tìm thấy trong tệp :file:`\*.pkg` đều được thêm vào path, bất kể chúng có tồn tại trên hệ thống tệp hay không (đây là một tính năng).

   Nếu input path không phải là một danh sách (như trong trường hợp các package frozen), nó được trả về không thay đổi. Input path không bị sửa đổi; một bản sao mở rộng được trả về. Các mục chỉ được thêm vào bản sao ở cuối.

   Giả định rằng :data:`sys.path` là một sequence. Các mục của :data:`sys.path` không phải là chuỗi trỏ đến các thư mục hiện có sẽ bị bỏ qua. Các mục Unicode trên :data:`sys.path` gây ra lỗi khi được dùng làm tên tệp có thể khiến hàm này phát sinh exception (phù hợp với hành vi của :func:`os.path.isdir`).


.. function:: get_importer(path_item)

   Truy xuất một :term:`finder` cho *path_item* đã cho.

   Finder được trả về sẽ được lưu vào cache trong :data:`sys.path_importer_cache` nếu nó vừa được tạo bởi một path hook.

   Bộ nhớ đệm (hoặc một phần của nó) có thể được xóa thủ công nếu cần quét lại
   :data:`sys.path_hooks`.

   .. versionchanged:: 3.3
      Đã cập nhật để dựa trực tiếp trên :mod:`importlib` thay vì dựa vào cơ chế mô phỏng import :pep:`302` nội bộ của package.


.. function:: iter_importers(fullname='')

   Trả về các đối tượng :term:`finder` cho tên module đã cho.

   Nếu *fullname* chứa một ``'.'``, các finder sẽ là những finder của package chứa *fullname*; nếu không, chúng sẽ là tất cả các finder cấp cao nhất đã đăng ký (tức là những finder có trên cả :data:`sys.meta_path` và :data:`sys.path_hooks`).

   Nếu module được chỉ định nằm trong một package, package đó sẽ được import như một tác dụng phụ của việc gọi hàm này.

   Nếu không chỉ định tên module, tất cả các finder cấp cao nhất sẽ được tạo ra.

   .. versionchanged:: 3.3
      Đã cập nhật để dựa trực tiếp trên :mod:`importlib` thay vì dựa vào cơ chế mô phỏng import :pep:`302` nội bộ của package.


.. function:: iter_modules(path=None, prefix='')

   Sinh :class:`ModuleInfo` cho tất cả các submodule trong *path*, hoặc nếu *path* là ``None``, cho tất cả các module cấp cao nhất trong :data:`sys.path`.

   *path* phải là ``None`` hoặc một danh sách các đường dẫn để tìm module.

   *prefix* là một chuỗi được xuất ở phía trước tên của mọi module trong đầu ra.

   .. note::

      Chỉ hoạt động với một :term:`finder` định nghĩa phương thức ``iter_modules()``. Giao diện này không theo chuẩn, vì vậy module cũng cung cấp các triển khai cho :class:`importlib.machinery.FileFinder` và
      :class:`zipimport.zipimporter`.

   .. versionchanged:: 3.3
      Đã cập nhật để dựa trực tiếp trên :mod:`importlib` thay vì dựa vào cơ chế mô phỏng import :pep:`302` nội bộ của package.


.. function:: walk_packages(path=None, prefix='', onerror=None)

   Sinh :class:`ModuleInfo` cho tất cả các module một cách đệ quy trong *path*, hoặc nếu *path* là ``None``, cho tất cả các module có thể truy cập.

   *path* phải là ``None`` hoặc một danh sách các đường dẫn để tìm module.

   *prefix* là một chuỗi được xuất ở phía trước tên của mọi module trong đầu ra.

   Lưu ý rằng hàm này phải import tất cả *packages* (*not* tất cả các module!) trên *path* đã cho, để truy cập thuộc tính ``__path__`` nhằm tìm các submodule.

   *onerror* là một hàm được gọi với một đối số (tên của package đang được import) nếu xảy ra bất kỳ ngoại lệ nào trong khi cố gắng import một package. Nếu không cung cấp hàm *onerror*, :exc:`ImportError`\s sẽ được bắt và bỏ qua, trong khi mọi ngoại lệ khác sẽ được chuyển tiếp, khiến quá trình tìm kiếm kết thúc.

   Ví dụ::

      # liệt kê tất cả các module mà python có thể truy cập
      walk_packages()

      # liệt kê tất cả các submodule của ctypes
      walk_packages(ctypes.__path__, ctypes.__name__ + '.')

   .. note::

      Chỉ hoạt động với một :term:`finder` định nghĩa phương thức ``iter_modules()``. Giao diện này không theo chuẩn, vì vậy module cũng cung cấp các triển khai cho :class:`importlib.machinery.FileFinder` và
      :class:`zipimport.zipimporter`.

   .. versionchanged:: 3.3
      Đã cập nhật để dựa trực tiếp trên :mod:`importlib` thay vì dựa vào cơ chế mô phỏng import :pep:`302` nội bộ của package.


.. function:: get_data(package, resource)

   Lấy một tài nguyên từ một package.

   Đây là một wrapper cho :term:`loader`
   API :meth:`get_data <importlib.abc.ResourceLoader.get_data>`. Đối số *package* phải là tên của một package, ở định dạng module chuẩn (``foo.bar``). Đối số *resource* phải có dạng tên tệp tương đối, sử dụng ``/`` làm dấu phân cách đường dẫn.

   Hàm trả về một chuỗi nhị phân chứa nội dung của tài nguyên được chỉ định.

   Hàm này sử dụng phương thức :term:`loader`
   :func:`~importlib.abc.FileLoader.get_data` để hỗ trợ các module được cài đặt trong hệ thống tệp, cũng như trong các tệp zip, cơ sở dữ liệu hoặc những nơi khác.

   Đối với các package nằm trong hệ thống tệp và đã được import, cách này gần tương đương với::

      d = os.path.dirname(sys.modules[package].__file__)
      data = open(os.path.join(d, resource), 'rb').read()

   Giống như hàm :func:`open`, :func:`!get_data` có thể đi theo các thư mục cha (``../``) và các đường dẫn tuyệt đối (chẳng hạn bắt đầu bằng ``/`` hoặc ``C:/``). Hàm này có thể mở các tệp tạo tác biên dịch/cài đặt như các tệp ``.py`` và ``.pyc`` hoặc các tệp có :func:`reserved filenames <os.path.isreserved>`. Để tương thích với các loader không dựa trên hệ thống tệp, hãy tránh sử dụng các tính năng này.

   .. warning::

      Hàm này dành cho dữ liệu đầu vào đáng tin cậy. Hàm không xác minh rằng *resource* có "thuộc về" *package* hay không.

   Nếu sử dụng đường dẫn *resource* do người dùng cung cấp, hãy cân nhắc xác minh đường dẫn đó. Ví dụ: yêu cầu tên tệp gồm chữ và số với phần mở rộng đã biết, hoặc cài đặt và kiểm tra một danh sách các resource đã biết.

   Nếu không thể định vị hoặc tải package, hoặc package sử dụng một :term:`loader` không hỗ trợ :meth:`get_data <importlib.abc.ResourceLoader.get_data>`, thì ``None`` được trả về. Cụ thể, :term:`loader` của
   :term:`namespace packages <namespace package>` không hỗ trợ
   :meth:`get_data <importlib.abc.ResourceLoader.get_data>`.

   .. seealso::

      Mô-đun :mod:`importlib.resources` cung cấp quyền truy cập có cấu trúc vào các tài nguyên của mô-đun.

.. function:: resolve_name(name)

   Phân giải một tên thành một đối tượng.

   Chức năng này được sử dụng ở nhiều nơi trong thư viện chuẩn (xem
   :issue:`12915`) - và chức năng tương đương cũng có trong các gói bên thứ ba được sử dụng rộng rãi như setuptools, Django và Pyramid.

   Dự kiến *tên* sẽ là một chuỗi theo một trong các định dạng sau, trong đó W là viết tắt của một định danh Python hợp lệ và dấu chấm biểu thị một dấu chấm theo nghĩa đen trong các pseudo-regex này:

   * ``W(.W)*``
   * ``W(.W)*:(W(.W)*)?``

   Dạng đầu tiên chỉ nhằm mục đích tương thích ngược. Dạng này giả định rằng một phần nào đó của tên có dấu chấm là một package, còn phần còn lại là một đối tượng ở đâu đó bên trong package đó, có thể được lồng bên trong các đối tượng khác. Vì không thể suy ra bằng cách kiểm tra vị trí package kết thúc và hệ thống phân cấp đối tượng bắt đầu, nên phải thực hiện nhiều lần thử import với dạng này.

   Ở dạng thứ hai, bên gọi làm rõ điểm phân chia bằng cách cung cấp một dấu hai chấm: tên có dấu chấm ở bên trái dấu hai chấm là một package cần được import, còn tên có dấu chấm ở bên phải là hệ thống phân cấp đối tượng bên trong package đó. Dạng này chỉ cần một lần import. Nếu tên kết thúc bằng dấu hai chấm, thì một đối tượng module sẽ được trả về.

   Hàm sẽ trả về một đối tượng (có thể là một module) hoặc phát sinh một trong các ngoại lệ sau:

   :exc:`ValueError` -- nếu *name* không ở định dạng được nhận diện.

   :exc:`ImportError` -- nếu quá trình import không thành công trong khi lẽ ra không được như vậy.

   :exc:`AttributeError` -- Nếu xảy ra lỗi khi duyệt qua hệ phân cấp đối tượng bên trong package đã import để đi đến đối tượng mong muốn.

   .. versionadded:: 3.9
