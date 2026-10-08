:mod:`!importlib` --- Việc triển khai :keyword:`!import`
========================================================

.. module:: importlib
   :synopsis: Việc triển khai cơ chế import.

.. moduleauthor:: Brett Cannon <brett@python.org>
.. sectionauthor:: Brett Cannon <brett@python.org>

.. versionadded:: 3.1

**Mã nguồn:** :source:`Lib/importlib/__init__.py`

--------------


Giới thiệu
----------

Mục đích của gói :mod:`!importlib` có ba phần.

Một mục đích là cung cấp triển khai câu lệnh :keyword:`import` (và do đó, mở rộng ra, triển khai
hàm :func:`__import__`) trong mã nguồn Python. Điều này cung cấp một triển khai :keyword:`!import` có thể chuyển đổi giữa mọi trình thông dịch Python. Đồng thời, đây cũng là một triển khai dễ hiểu hơn so với triển khai bằng một ngôn ngữ lập trình khác ngoài Python.

Thứ hai, các thành phần cần triển khai :keyword:`import` được cung cấp trong gói này, giúp người dùng dễ dàng tạo các đối tượng tùy chỉnh của riêng mình (thường được gọi là :term:`importer`) để tham gia vào quá trình import.

Thứ ba, gói này chứa các mô-đun cung cấp thêm chức năng để quản lý các khía cạnh của các gói Python:

* :mod:`importlib.metadata` cung cấp quyền truy cập vào siêu dữ liệu từ các distribution bên thứ ba.
* :mod:`importlib.resources` cung cấp các routine để truy cập vào "resource" không phải mã từ các gói Python.

.. seealso::

    :ref:`import`
        Tài liệu tham chiếu ngôn ngữ cho câu lệnh :keyword:`import`.

    `Đặc tả các gói Python <https://www.python.org/doc/essays/packages/>`__
        Đặc tả ban đầu của các gói. Một số ngữ nghĩa đã thay đổi kể từ khi tài liệu này được soạn thảo (ví dụ: chuyển hướng dựa trên ``None`` trong :data:`sys.modules`).

    Hàm :func:`.__import__`
        Câu lệnh :keyword:`import` là cú pháp rút gọn cho hàm này.

    :ref:`sys-path-init`
        Việc khởi tạo :data:`sys.path`.

    :pep:`235`
        Import trên các nền tảng không phân biệt chữ hoa chữ thường

    :pep:`263`
        Xác định mã hóa mã nguồn Python

    :pep:`302`
        Các import hook mới

    :pep:`328`
        Import: Nhiều dòng và Tuyệt đối/Tương đối

    :pep:`366`
        Nhập tương đối rõ ràng trong module chính

    :pep:`420`
        Các gói namespace ngầm định

    :pep:`451`
        Kiểu ModuleSpec cho hệ thống import

    :pep:`488`
        Loại bỏ các tệp PYO

    :pep:`489`
        Khởi tạo module mở rộng theo nhiều giai đoạn

    :pep:`552`
        Các tệp pyc xác định

    :pep:`3120`
        Sử dụng UTF-8 làm mã hóa nguồn mặc định

    :pep:`3147`
        Các thư mục của PYC Repository


Hàm
---

.. function:: __import__(name, globals=None, locals=None, fromlist=(), level=0)

    Một cách triển khai hàm :func:`__import__` tích hợp sẵn.

    .. note::
       Việc import module bằng lập trình nên sử dụng :func:`import_module` thay vì hàm này.

.. function:: import_module(name, package=None)

    Import một module. Đối số *name* chỉ định module cần import theo dạng tuyệt đối hoặc tương đối (ví dụ: ``pkg.mod`` hoặc ``..mod``). Nếu tên được chỉ định theo dạng tương đối, đối số *package* phải được đặt thành tên của package dùng làm mốc để phân giải tên package (ví dụ, ``import_module('..mod', 'pkg.subpkg')`` sẽ import ``pkg.mod``).

    Hàm :func:`import_module` hoạt động như một wrapper đơn giản hóa cho
    :func:`importlib.__import__`. Điều này có nghĩa là toàn bộ ngữ nghĩa của hàm được kế thừa từ :func:`importlib.__import__`. Điểm khác biệt quan trọng nhất giữa hai hàm này là :func:`import_module` trả về package hoặc module được chỉ định (ví dụ: ``pkg.mod``), trong khi :func:`__import__` trả về package hoặc module cấp cao nhất (ví dụ: ``pkg``).

    Nếu bạn đang import động một module được tạo sau khi interpreter bắt đầu thực thi (ví dụ: tạo một tệp mã nguồn Python), bạn có thể cần gọi :func:`invalidate_caches` để hệ thống import nhận biết module mới.

    .. versionchanged:: 3.3
       Các package cha được tự động import.

.. function:: invalidate_caches()

   Vô hiệu hóa các bộ nhớ đệm nội bộ của các finder được lưu tại
   :data:`sys.meta_path`. Nếu một finder triển khai ``invalidate_caches()`` thì nó sẽ được gọi để thực hiện việc vô hiệu hóa. Hàm này nên được gọi nếu có module được tạo/cài đặt trong khi chương trình đang chạy, nhằm đảm bảo mọi finder đều nhận biết sự tồn tại của module mới.

   .. versionadded:: 3.3

   .. versionchanged:: 3.10
      Các namespace package được tạo/cài đặt tại một vị trí :data:`sys.path` khác sau khi cùng namespace đã được import sẽ được nhận biết.

.. function:: reload(module)

   Tải lại *module* đã được import trước đó. Đối số phải là một đối tượng module, vì vậy module đó phải được import thành công trước đó. Điều này hữu ích nếu bạn đã chỉnh sửa tệp mã nguồn của module bằng trình soạn thảo bên ngoài và muốn thử phiên bản mới mà không cần thoát khỏi Python interpreter. Giá trị trả về là đối tượng module (có thể khác nếu việc import lại khiến một đối tượng khác được đặt vào :data:`sys.modules`).

   Khi :func:`reload` được thực thi:

   * Mã của module Python được biên dịch lại và mã cấp module được thực thi lại, tạo ra một tập đối tượng mới được liên kết với các tên trong dictionary của module bằng cách sử dụng lại :term:`loader` đã tải module ban đầu. Hàm ``init`` của các extension module không được gọi lần thứ hai.

   * Cũng như mọi đối tượng khác trong Python, các đối tượng cũ chỉ được thu hồi sau khi số lượng tham chiếu của chúng giảm xuống bằng không.

   * Các tên trong namespace của module được cập nhật để trỏ đến mọi đối tượng mới hoặc đã thay đổi.

   * Các tham chiếu khác đến những đối tượng cũ (chẳng hạn như các tên bên ngoài module) không được liên kết lại để trỏ đến các đối tượng mới và phải được cập nhật trong từng namespace nơi chúng xuất hiện nếu muốn như vậy.

   Có một số điểm cần lưu ý khác:

   Khi một module được tải lại, dictionary của module (chứa các biến toàn cục của module) được giữ lại. Việc định nghĩa lại các tên sẽ ghi đè các định nghĩa cũ, vì vậy nhìn chung đây không phải là vấn đề. Nếu phiên bản mới của module không định nghĩa một tên đã được định nghĩa trong phiên bản cũ, định nghĩa cũ vẫn được giữ lại. Tính năng này có thể được tận dụng nếu module duy trì một bảng hoặc cache toàn cục của các đối tượng --- với một câu lệnh :keyword:`try`, module có thể kiểm tra sự tồn tại của bảng và bỏ qua việc khởi tạo nếu muốn.::

      try:
          cache
      except NameError:
          cache = {}

   Nhìn chung, việc tải lại các module tích hợp sẵn hoặc được tải động không mang lại nhiều ích lợi. Không nên tải lại :mod:`sys`, :mod:`__main__`, :mod:`builtins` và các module cốt lõi khác. Trong nhiều trường hợp, các extension module không được thiết kế để khởi tạo nhiều hơn một lần và có thể gặp lỗi theo những cách không thể dự đoán khi được tải lại.

   Nếu một module import các đối tượng từ module khác bằng :keyword:`from` ...
   :keyword:`import` ..., việc gọi :func:`reload` cho module kia không định nghĩa lại các đối tượng được import từ đó --- một cách để khắc phục là thực thi lại câu lệnh :keyword:`!from`, cách khác là sử dụng :keyword:`!import` và các tên đủ điều kiện (*module.name*) thay thế.

   Nếu một module khởi tạo các instance của một class, việc tải lại module định nghĩa class đó không ảnh hưởng đến các định nghĩa phương thức của các instance --- chúng tiếp tục sử dụng định nghĩa class cũ. Điều tương tự cũng đúng với các class dẫn xuất.

   .. versionadded:: 3.4
   .. versionchanged:: 3.7
       :exc:`ModuleNotFoundError` is raised when the module being reloaded lacks
       một :class:`~importlib.machinery.ModuleSpec`.

   .. warning::
      Hàm này không an toàn khi sử dụng trong nhiều thread. Việc gọi hàm này từ nhiều thread có thể dẫn đến hành vi không mong muốn. Bạn nên sử dụng :class:`threading.Lock` hoặc các primitive đồng bộ hóa khác để tải lại module một cách an toàn khi sử dụng trong nhiều thread.

:mod:`!importlib.abc` -- Các abstract base class liên quan đến import
---------------------------------------------------------------------

.. module:: importlib.abc
    :synopsis: Các abstract base class liên quan đến import

**Mã nguồn:** :source:`Lib/importlib/abc.py`

--------------


Mô-đun :mod:`!importlib.abc` chứa tất cả các abstract base class cốt lõi được :keyword:`import` sử dụng. Mô-đun cũng cung cấp một số lớp con của các abstract base class cốt lõi để hỗ trợ việc triển khai các ABC cốt lõi.

Cấu trúc phân cấp ABC::

    object
     +-- MetaPathFinder
     +-- PathEntryFinder
     +-- Loader
          +-- ResourceLoader --------+
          +-- InspectLoader          |
               +-- ExecutionLoader --+
                                     +-- FileLoader
                                     +-- SourceLoader


.. class:: MetaPathFinder

   Một abstract base class đại diện cho :term:`meta path finder`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.10
      Không còn là lớp con của :class:`!Finder`.

   .. method:: find_spec(fullname, path, target=None)

      Một phương thức trừu tượng để tìm :term:`spec <module spec>` cho mô-đun được chỉ định. Nếu đây là một import cấp cao nhất, *path* sẽ là ``None``. Nếu không, đây là một tìm kiếm đối với subpackage hoặc mô-đun, và *path* sẽ là giá trị của :attr:`~module.__path__` từ package cha. Nếu không tìm thấy spec, ``None`` sẽ được trả về. Khi được truyền vào, ``target`` là một đối tượng mô-đun mà finder có thể sử dụng để đưa ra phán đoán chính xác hơn về spec cần trả về.
      :func:`importlib.util.spec_from_loader` có thể hữu ích khi triển khai các ``MetaPathFinders`` cụ thể.

      .. versionadded:: 3.4

   .. method:: invalidate_caches()

      Một phương thức tùy chọn mà khi được gọi sẽ vô hiệu hóa mọi bộ nhớ đệm nội bộ được finder sử dụng. Được :func:`importlib.invalidate_caches` sử dụng khi vô hiệu hóa bộ nhớ đệm của tất cả finder trên :data:`sys.meta_path`.

      .. versionchanged:: 3.4
         Trả về ``None`` khi được gọi thay vì :data:`NotImplemented`.


.. class:: PathEntryFinder

   Một lớp cơ sở trừu tượng đại diện cho một :term:`path entry finder`. Mặc dù có một số điểm tương đồng với :class:`MetaPathFinder`, ``PathEntryFinder`` chỉ được dùng trong subsystem import dựa trên đường dẫn do :class:`importlib.machinery.PathFinder` cung cấp.

   .. versionadded:: 3.3

   .. versionchanged:: 3.10
      Không còn là lớp con của :class:`!Finder`.

   .. method:: find_spec(fullname, target=None)

      Một phương thức trừu tượng dùng để tìm :term:`spec <module spec>` cho mô-đun được chỉ định. Finder sẽ chỉ tìm kiếm mô-đun trong :term:`path entry` mà nó được gán vào. Nếu không tìm thấy spec, ``None`` sẽ được trả về. Khi được truyền vào, ``target`` là một đối tượng mô-đun mà finder có thể sử dụng để đưa ra phỏng đoán chính xác hơn về spec cần trả về. :func:`importlib.util.spec_from_loader` có thể hữu ích khi triển khai các ``PathEntryFinders`` cụ thể.

      .. versionadded:: 3.4

   .. method:: invalidate_caches()

      Một phương thức tùy chọn mà khi được gọi sẽ vô hiệu hóa mọi bộ nhớ đệm nội bộ được finder sử dụng. Được sử dụng bởi
      :meth:`importlib.machinery.PathFinder.invalidate_caches` khi vô hiệu hóa bộ nhớ đệm của tất cả finder đã lưu trong bộ nhớ đệm.


.. class:: Loader

    Một abstract base class cho :term:`loader`. Xem :pep:`302` để biết định nghĩa chính xác dành cho loader.

    Các loader muốn hỗ trợ việc đọc resource nên triển khai một
    phương thức :meth:`!get_resource_reader` như được quy định trong
    :class:`importlib.resources.abc.ResourceReader`.

    .. versionchanged:: 3.7
       Đã giới thiệu phương thức :meth:`!get_resource_reader` tùy chọn.

    .. method:: create_module(spec)

       Một phương thức trả về đối tượng module sẽ được sử dụng khi import một module. Phương thức này có thể trả về ``None``, cho biết các ngữ nghĩa tạo module mặc định sẽ được áp dụng.

       .. versionadded:: 3.4

       .. versionchanged:: 3.6
          Phương thức này không còn là tùy chọn khi
          :meth:`exec_module` được định nghĩa.

    .. method:: exec_module(module)

       Một phương thức trừu tượng thực thi module trong không gian tên riêng của module khi module được import hoặc tải lại. Module phải được khởi tạo trước khi gọi :meth:`exec_module`. Khi phương thức này tồn tại,
       :meth:`create_module` phải được định nghĩa.

       .. versionadded:: 3.4

       .. versionchanged:: 3.6
          :meth:`create_module` must also be defined.

    .. method:: load_module(fullname)

        Một phương thức cũ dùng để tải module. Nếu không thể tải module, :exc:`ImportError` sẽ được phát sinh; nếu không, module đã tải sẽ được trả về.

        Nếu module được yêu cầu đã tồn tại trong :data:`sys.modules`, module đó phải được sử dụng và tải lại. Nếu không, loader phải tạo một module mới và chèn module đó vào
        :data:`sys.modules` trước khi bắt đầu tải để ngăn việc import đệ quy. Nếu loader đã chèn một module nhưng quá trình tải thất bại, loader phải xóa module đó khỏi :data:`sys.modules`; các module đã có trong :data:`sys.modules` trước khi loader bắt đầu thực thi phải được giữ nguyên.

        Loader phải thiết lập một số thuộc tính trên module (lưu ý rằng một số thuộc tính có thể thay đổi khi module được tải lại):

        - :attr:`module.__name__`
        - :attr:`module.__file__`
        - :attr:`module.__cached__` *(không dùng nữa)*
        - :attr:`module.__path__`
        - :attr:`module.__package__` *(không còn được khuyến nghị)*
        - :attr:`module.__loader__` *(không còn được khuyến nghị)*

        Khi :meth:`exec_module` khả dụng, chức năng tương thích ngược sẽ được cung cấp.

        .. versionchanged:: 3.4
           Ném :exc:`ImportError` khi được gọi thay cho
           :exc:`NotImplementedError`. Chức năng được cung cấp khi
           :meth:`exec_module` khả dụng.

        .. deprecated-removed:: 3.4 3.15
           API được khuyến nghị để tải một module là :meth:`exec_module` (và :meth:`create_module`). Loader nên triển khai API này thay cho
           :meth:`load_module`. Bộ máy nhập đảm nhiệm tất cả các trách nhiệm khác của :meth:`load_module` khi
           :meth:`exec_module` được triển khai.


.. class:: ResourceLoader

   *Được thay thế bởi TraversableResources*

    Một lớp cơ sở trừu tượng cho một :term:`loader` triển khai tùy chọn
    :pep:`302` protocol để tải các tài nguyên tùy ý từ phần lưu trữ phía sau.

    .. deprecated:: 3.7
       ABC này không còn được khuyến nghị; thay vào đó, hãy hỗ trợ tải tài nguyên thông qua :class:`importlib.resources.abc.TraversableResources`. Lớp này chỉ tồn tại để duy trì khả năng tương thích ngược với các ABC khác trong mô-đun này.

    .. method:: get_data(path)
       :abstractmethod:

        An abstract method to return the bytes for the data located at *path*.
        Loaders that have a file-like storage back-end
        that allows storing arbitrary data
        can implement this abstract method to give direct access
        to the data stored. :exc:`OSError` is to be raised if the *path* cannot
        be found. The *path* is expected to be constructed using a module's
        :attr:`~module.__file__` attribute or an item from a package's
        :attr:`~module.__path__`.

        .. versionchanged:: 3.4
           Raises :exc:`OSError` instead of :exc:`NotImplementedError`.


.. class:: InspectLoader

    Một lớp cơ sở trừu tượng cho một :term:`loader` triển khai tùy chọn
    :pep:`302` protocol dành cho các loader kiểm tra module.

    .. method:: get_code(fullname)

        Trả về đối tượng mã cho một module hoặc ``None`` nếu module không có đối tượng mã (chẳng hạn như đối với một module tích hợp sẵn). Phát sinh :exc:`ImportError` nếu loader không tìm thấy module được yêu cầu.

        .. note::
           Mặc dù phương thức này có triển khai mặc định, bạn nên ghi đè nó nếu có thể để cải thiện hiệu suất.

        .. index::
           single: universal newlines; importlib.abc.InspectLoader.get_source method

        .. versionchanged:: 3.4
           Không còn là abstract và đã cung cấp một triển khai cụ thể.

    .. method:: get_source(fullname)
       :abstractmethod:

        An abstract method to return the source of a module. It is returned as
        a text string using :term:`universal newlines`, translating all
        recognized line separators into ``'\n'`` characters.  Returns ``None``
        if no source is available (e.g. a built-in module). Raises
        :exc:`ImportError` if the loader cannot find the module specified.

        .. versionchanged:: 3.4
           Raises :exc:`ImportError` instead of :exc:`NotImplementedError`.

    .. method:: is_package(fullname)

        Một phương thức tùy chọn trả về giá trị true nếu module là một package, nếu không thì trả về giá trị false. :exc:`ImportError` được phát sinh nếu
        :term:`loader` không thể tìm thấy module.

        .. versionchanged:: 3.4
           Phát sinh :exc:`ImportError` thay vì :exc:`NotImplementedError`.

    .. staticmethod:: source_to_code(data, path='<string>')

        Tạo một đối tượng code từ mã nguồn Python.

        Đối số *data* có thể là bất kỳ kiểu dữ liệu nào mà hàm :func:`compile` hỗ trợ (tức là chuỗi hoặc bytes). Đối số *path* phải là "đường dẫn" đến nơi mã nguồn bắt nguồn, có thể là một khái niệm trừu tượng (ví dụ: vị trí trong tệp zip).

        Với đối tượng code tiếp theo, bạn có thể thực thi nó trong một module bằng cách chạy ``exec(code, module.__dict__)``.

        .. versionadded:: 3.4

        .. versionchanged:: 3.5
           Đã chuyển phương thức thành static.

    .. method:: exec_module(module)

       Triển khai :meth:`Loader.exec_module`.

       .. versionadded:: 3.4

    .. method:: load_module(fullname)

       Triển khai :meth:`Loader.load_module`.

       .. deprecated-removed:: 3.4 3.15
          hãy sử dụng :meth:`exec_module` thay vào đó.


.. class:: ExecutionLoader

    Một lớp cơ sở trừu tượng kế thừa từ :class:`InspectLoader` mà khi được triển khai sẽ giúp một mô-đun được thực thi như một tập lệnh. ABC này đại diện cho một giao thức :pep:`302` tùy chọn.

    .. method:: get_filename(fullname)
       :abstractmethod:

        An abstract method that is to return the value of
        :attr:`~module.__file__` for the specified module. If no path is
        available, :exc:`ImportError` is raised.

        If source code is available, then the method should return the path to
        the source file, regardless of whether a bytecode was used to load the
        module.

        .. versionchanged:: 3.4
           Raises :exc:`ImportError` instead of :exc:`NotImplementedError`.


.. class:: FileLoader(fullname, path)

   Một lớp cơ sở trừu tượng kế thừa từ :class:`ResourceLoader` và
   :class:`ExecutionLoader`, cung cấp các triển khai cụ thể của
   :meth:`ResourceLoader.get_data` và :meth:`ExecutionLoader.get_filename`.

   Đối số *fullname* là tên đầy đủ đã được phân giải của mô-đun mà loader sẽ xử lý. Đối số *path* là đường dẫn đến tệp của mô-đun.

   .. versionadded:: 3.3

   .. attribute:: name

      Tên của mô-đun mà loader có thể xử lý.

   .. attribute:: path

      Đường dẫn đến tệp của mô-đun.

   .. method:: load_module(fullname)

      Gọi ``load_module()`` của lớp cha.

      .. deprecated-removed:: 3.4 3.15
         Thay vào đó, hãy sử dụng :meth:`Loader.exec_module`.

   .. method:: get_filename(fullname)
      :abstractmethod:

      Trả về :attr:`path`.

   .. method:: get_data(path)
      :abstractmethod:

      Đọc *path* dưới dạng tệp nhị phân và trả về các byte từ tệp đó.


.. class:: SourceLoader

    Một lớp cơ sở trừu tượng để triển khai việc tải tệp mã nguồn (và tùy chọn cả bytecode). Lớp này kế thừa từ cả :class:`ResourceLoader` và
    :class:`ExecutionLoader`, yêu cầu triển khai:

    * :meth:`ResourceLoader.get_data`
    * :meth:`ExecutionLoader.get_filename`
          Chỉ nên trả về đường dẫn đến tệp mã nguồn; không hỗ trợ tải không có mã nguồn.

    Các phương thức trừu tượng được định nghĩa bởi lớp này dùng để bổ sung khả năng hỗ trợ tệp bytecode tùy chọn. Nếu không triển khai các phương thức tùy chọn này (hoặc khiến chúng phát sinh :exc:`NotImplementedError`) thì loader chỉ hoạt động với mã nguồn. Việc triển khai các phương thức này cho phép loader hoạt động với mã nguồn *và* các tệp bytecode; nhưng không cho phép nạp *sourceless* khi chỉ cung cấp bytecode. Các tệp bytecode là một tối ưu hóa giúp tăng tốc quá trình nạp bằng cách loại bỏ bước phân tích cú pháp của compiler Python, vì vậy không có API dành riêng cho bytecode nào được cung cấp.

    .. method:: path_stats(path)

        Phương thức trừu tượng tùy chọn trả về một :class:`dict` chứa siêu dữ liệu về path được chỉ định. Các khóa dictionary được hỗ trợ gồm:

        - ``'mtime'`` (bắt buộc): một số nguyên hoặc số dấu phẩy động biểu thị thời gian sửa đổi của mã nguồn;
        - ``'size'`` (tùy chọn): kích thước của mã nguồn tính bằng byte.

        Mọi khóa khác trong dictionary đều bị bỏ qua để cho phép mở rộng trong tương lai. Nếu không thể xử lý path, :exc:`OSError` sẽ được phát sinh.

        .. versionadded:: 3.3

        .. versionchanged:: 3.4
           Phát sinh :exc:`OSError` thay vì :exc:`NotImplementedError`.

    .. method:: path_mtime(path)

        Phương thức trừu tượng tùy chọn trả về thời gian sửa đổi của path được chỉ định.

        .. deprecated:: 3.3
           Phương thức này không còn được khuyến nghị sử dụng và được thay thế bằng :meth:`path_stats`. Bạn không bắt buộc phải triển khai phương thức này, nhưng nó vẫn được cung cấp để đảm bảo khả năng tương thích. Hãy raise :exc:`OSError` nếu không thể xử lý đường dẫn.

        .. versionchanged:: 3.4
           Phát sinh :exc:`OSError` thay vì :exc:`NotImplementedError`.

    .. method:: set_data(path, data)

        Phương thức trừu tượng tùy chọn ghi các byte được chỉ định vào một đường dẫn tệp. Mọi thư mục trung gian chưa tồn tại sẽ được tự động tạo.

        Khi việc ghi vào đường dẫn không thành công vì đường dẫn chỉ có quyền đọc (:const:`errno.EACCES`/:exc:`PermissionError`), không truyền tiếp ngoại lệ.

        .. versionchanged:: 3.4
           Không còn raise :exc:`NotImplementedError` khi được gọi.

    .. method:: get_code(fullname)

        Triển khai cụ thể của :meth:`InspectLoader.get_code`.

    .. method:: exec_module(module)

       Triển khai cụ thể của :meth:`Loader.exec_module`.

       .. versionadded:: 3.4

    .. method:: load_module(fullname)

       Triển khai cụ thể của :meth:`Loader.load_module`.

       .. deprecated-removed:: 3.4 3.15
          Thay vào đó, hãy sử dụng :meth:`exec_module`.

    .. method:: get_source(fullname)

        Triển khai cụ thể của :meth:`InspectLoader.get_source`.

    .. method:: is_package(fullname)

        Triển khai cụ thể của :meth:`InspectLoader.is_package`. Một mô-đun được xác định là một package nếu đường dẫn tệp của nó (do
        :meth:`ExecutionLoader.get_filename` cung cấp) là một tệp có tên ``__init__`` sau khi loại bỏ phần mở rộng tệp **và** tên mô-đun không kết thúc bằng ``__init__``.


:mod:`!importlib.machinery` -- Trình nhập và path hook
------------------------------------------------------

.. module:: importlib.machinery
    :synopsis: Trình nhập và path hook

**Mã nguồn:** :source:`Lib/importlib/machinery.py`

--------------

Mô-đun này chứa nhiều đối tượng khác nhau giúp :keyword:`import` tìm và tải các mô-đun.

.. data:: SOURCE_SUFFIXES

   Danh sách các chuỗi biểu thị các hậu tố tệp được nhận diện cho các mô-đun mã nguồn.

   .. versionadded:: 3.3

.. data:: DEBUG_BYTECODE_SUFFIXES

   Danh sách các chuỗi biểu thị các hậu tố tệp cho các mô-đun bytecode chưa được tối ưu hóa.

   .. versionadded:: 3.3

   .. deprecated:: 3.5
      Thay vào đó, hãy sử dụng :const:`BYTECODE_SUFFIXES`.

.. data:: OPTIMIZED_BYTECODE_SUFFIXES

   Danh sách các chuỗi biểu thị các hậu tố tệp cho các mô-đun bytecode đã được tối ưu hóa.

   .. versionadded:: 3.3

   .. deprecated:: 3.5
      Thay vào đó, hãy sử dụng :const:`BYTECODE_SUFFIXES`.

.. data:: BYTECODE_SUFFIXES

   Danh sách các chuỗi biểu diễn những hậu tố tệp được nhận diện cho các module bytecode (bao gồm cả dấu chấm ở đầu).

   .. versionadded:: 3.3

   .. versionchanged:: 3.5
      Giá trị này không còn phụ thuộc vào ``__debug__``.

.. data:: EXTENSION_SUFFIXES

   Danh sách các chuỗi biểu diễn những hậu tố tệp được nhận diện cho các module mở rộng.

   .. versionadded:: 3.3

.. function:: all_suffixes()

   Trả về danh sách kết hợp các chuỗi biểu diễn tất cả hậu tố tệp của những module được cơ chế import tiêu chuẩn nhận diện. Đây là một hàm trợ giúp cho mã chỉ cần xác định liệu một đường dẫn hệ thống tệp có khả năng trỏ đến một module hay không mà không cần biết chi tiết về loại module (ví dụ: :func:`inspect.getmodulename`).

   .. versionadded:: 3.3


.. class:: BuiltinImporter

    Một :term:`importer` dành cho các module tích hợp sẵn. Tất cả các module tích hợp sẵn đã biết được liệt kê trong :data:`sys.builtin_module_names`. Lớp này triển khai
    :class:`importlib.abc.MetaPathFinder` và
    các ABC :class:`importlib.abc.InspectLoader`.

    Lớp này chỉ định nghĩa các phương thức lớp để tránh nhu cầu khởi tạo đối tượng.

    .. versionchanged:: 3.5
       Là một phần của :pep:`489`, trình nhập tích hợp sẵn hiện triển khai
       :meth:`Loader.create_module <importlib.abc.Loader.create_module>` và :meth:`Loader.exec_module <importlib.abc.Loader.exec_module>`


.. class:: FrozenImporter

    Một :term:`importer` dành cho các module đóng băng. Lớp này triển khai
    :class:`importlib.abc.MetaPathFinder` và
    các ABC :class:`importlib.abc.InspectLoader`.

    Lớp này chỉ định nghĩa các phương thức lớp để tránh nhu cầu khởi tạo đối tượng.

    .. versionchanged:: 3.4
       Được bổ sung :meth:`~importlib.abc.Loader.create_module` và
       :meth:`~importlib.abc.Loader.exec_module` các phương thức.


.. class:: WindowsRegistryFinder

   :term:`Finder <finder>` cho các module được khai báo trong Windows registry. Lớp này triển khai ABC :class:`importlib.abc.MetaPathFinder`.

   Lớp này chỉ định nghĩa các phương thức lớp để tránh nhu cầu khởi tạo đối tượng.

   .. versionadded:: 3.3

   .. deprecated:: 3.6
      Thay vào đó, hãy sử dụng cấu hình :mod:`site`. Các phiên bản Python trong tương lai có thể không bật finder này theo mặc định.


.. class:: PathFinder

   Một :term:`Finder <finder>` cho :data:`sys.path` và các thuộc tính ``__path__`` của package. Lớp này triển khai ABC :class:`importlib.abc.MetaPathFinder`.

   Lớp này chỉ định nghĩa các phương thức lớp để tránh nhu cầu khởi tạo đối tượng.

   .. classmethod:: find_spec(fullname, path=None, target=None)

      Phương thức lớp cố gắng tìm một :term:`spec <module spec>` cho module được chỉ định bởi *fullname* trên :data:`sys.path` hoặc, nếu được định nghĩa, trên *path*. Với mỗi mục đường dẫn được tìm kiếm,
      :data:`sys.path_importer_cache` được kiểm tra. Nếu tìm thấy một đối tượng khác false thì đối tượng đó được dùng làm :term:`path entry finder` để tìm module đang được tìm kiếm. Nếu không tìm thấy mục nào trong
      :data:`sys.path_importer_cache`, thì :data:`sys.path_hooks` được tìm kiếm để tìm finder cho mục đường dẫn và, nếu tìm thấy, được lưu vào :data:`sys.path_importer_cache` đồng thời được truy vấn về module. Nếu không tìm thấy finder nào thì ``None`` vừa được lưu vào cache vừa được trả về.

      .. versionadded:: 3.4

      .. versionchanged:: 3.5
         Nếu thư mục làm việc hiện tại -- được biểu diễn bằng một chuỗi rỗng -- không còn hợp lệ thì ``None`` được trả về nhưng không có giá trị nào được lưu vào cache trong :data:`sys.path_importer_cache`.

   .. classmethod:: invalidate_caches()

      Gọi :meth:`importlib.abc.PathEntryFinder.invalidate_caches` trên tất cả finder được lưu trong :data:`sys.path_importer_cache` có định nghĩa phương thức này. Nếu không, các mục trong :data:`sys.path_importer_cache` được đặt thành ``None`` sẽ bị xóa.

      .. versionchanged:: 3.7
         Các mục của ``None`` trong :data:`sys.path_importer_cache` sẽ bị xóa.

   .. versionchanged:: 3.4
      Gọi các đối tượng trong :data:`sys.path_hooks` với thư mục làm việc hiện tại cho ``''`` (tức là chuỗi rỗng).


.. class:: FileFinder(path, *loader_details)

   Một triển khai cụ thể của :class:`importlib.abc.PathEntryFinder` dùng bộ nhớ đệm để lưu các kết quả từ hệ thống tệp.

   Đối số *path* là thư mục mà finder chịu trách nhiệm tìm kiếm.

   Đối số *loader_details* là một số lượng biến đổi các tuple gồm 2 phần tử, mỗi tuple chứa một loader và một chuỗi hậu tố tệp mà loader đó nhận dạng. Các loader được kỳ vọng là những callable nhận hai đối số: tên của module và đường dẫn đến tệp được tìm thấy.

   Finder sẽ lưu nội dung thư mục vào bộ nhớ đệm khi cần, thực hiện các lệnh gọi stat cho mỗi lần tìm kiếm module để xác minh bộ nhớ đệm chưa lỗi thời. Vì độ lỗi thời của bộ nhớ đệm phụ thuộc vào độ phân giải của thông tin trạng thái hệ điều hành về hệ thống tệp, nên có thể xảy ra điều kiện tranh đua khi tìm kiếm một module, tạo một tệp mới, rồi tìm kiếm module mà tệp mới đó đại diện. Nếu các thao tác diễn ra đủ nhanh để nằm trong độ phân giải của các lệnh gọi stat, việc tìm kiếm module sẽ thất bại. Để ngăn điều này xảy ra, khi tạo module một cách động, hãy nhớ gọi :func:`importlib.invalidate_caches`.

   .. versionadded:: 3.3

   .. attribute:: path

      Đường dẫn mà finder sẽ tìm kiếm.

   .. method:: find_spec(fullname, target=None)

      Cố gắng tìm spec để xử lý *fullname* trong :attr:`path`.

      .. versionadded:: 3.4

   .. method:: invalidate_caches()

      Xóa bộ nhớ đệm nội bộ.

   .. classmethod:: path_hook(*loader_details)

      Một phương thức lớp trả về một closure để sử dụng trên :data:`sys.path_hooks`. Closure trả về một thể hiện của :class:`FileFinder` bằng cách sử dụng trực tiếp đối số path được truyền cho closure và gián tiếp *loader_details*.

      Nếu đối số truyền cho closure không phải là một thư mục hiện có,
      :exc:`ImportError` sẽ được phát sinh.


.. class:: SourceFileLoader(fullname, path)

   Một triển khai cụ thể của :class:`importlib.abc.SourceLoader` bằng cách tạo lớp con của :class:`importlib.abc.FileLoader` và cung cấp một số triển khai cụ thể cho các phương thức khác.

   .. versionadded:: 3.3

   .. attribute:: name

      Tên của module mà loader này sẽ xử lý.

   .. attribute:: path

      Đường dẫn đến tệp nguồn.

   .. method:: is_package(fullname)

      Trả về ``True`` nếu :attr:`path` có vẻ là một package.

   .. method:: path_stats(path)

      Triển khai cụ thể của :meth:`importlib.abc.SourceLoader.path_stats`.

   .. method:: set_data(path, data)

      Triển khai cụ thể của :meth:`importlib.abc.SourceLoader.set_data`.

   .. method:: load_module(name=None)

      Triển khai cụ thể của :meth:`importlib.abc.Loader.load_module`, trong đó việc chỉ định tên mô-đun cần tải là tùy chọn.

      .. deprecated-removed:: 3.6 3.15

         Thay vào đó, hãy sử dụng :meth:`importlib.abc.Loader.exec_module`.


.. class:: SourcelessFileLoader(fullname, path)

   Một triển khai cụ thể của :class:`importlib.abc.FileLoader` có thể nhập các tệp bytecode (tức là không có tệp mã nguồn).

   Xin lưu ý rằng việc sử dụng trực tiếp các tệp bytecode (và do đó không sử dụng các tệp mã nguồn) khiến các mô-đun của bạn không thể được sử dụng bởi mọi triển khai Python hoặc các phiên bản Python mới thay đổi định dạng bytecode.

   .. versionadded:: 3.3

   .. attribute:: name

      Tên của mô-đun mà trình nạp sẽ xử lý.

   .. attribute:: path

      Đường dẫn đến tệp bytecode.

   .. method:: is_package(fullname)

      Xác định module có phải là package hay không dựa trên :attr:`path`.

   .. method:: get_code(fullname)

      Trả về đối tượng code cho :attr:`name` được tạo từ :attr:`path`.

   .. method:: get_source(fullname)

      Trả về ``None`` vì các tệp bytecode không có mã nguồn khi sử dụng loader này.

   .. method:: load_module(name=None)

   Triển khai cụ thể của :meth:`importlib.abc.Loader.load_module`, trong đó việc chỉ định tên mô-đun cần tải là tùy chọn.

   .. deprecated-removed:: 3.6 3.15

      Thay vào đó, hãy sử dụng :meth:`importlib.abc.Loader.exec_module`.


.. class:: ExtensionFileLoader(fullname, path)

   Một triển khai cụ thể của :class:`importlib.abc.ExecutionLoader` dành cho các module mở rộng.

   Đối số *fullname* chỉ định tên của module mà loader sẽ hỗ trợ. Đối số *path* là đường dẫn đến tệp của extension module.

   Lưu ý rằng theo mặc định, việc import extension module sẽ thất bại trong các subinterpreter nếu module đó không triển khai multi-phase init (xem :pep:`489`), ngay cả khi trong các trường hợp khác việc import vẫn thành công.

   .. versionadded:: 3.3

   .. versionchanged:: 3.12
      Hiện tại, multi-phase init là bắt buộc để sử dụng trong các subinterpreter.

   .. attribute:: name

      Tên của module mà loader hỗ trợ.

   .. attribute:: path

      Đường dẫn đến extension module.

   .. method:: create_module(spec)

      Tạo đối tượng module từ specification đã cho theo :pep:`489`.

      .. versionadded:: 3.5

   .. method:: exec_module(module)

      Khởi tạo đối tượng module đã cho theo :pep:`489`.

      .. versionadded:: 3.5

   .. method:: is_package(fullname)

      Trả về ``True`` nếu đường dẫn tệp trỏ đến module ``__init__`` của một package dựa trên :const:`EXTENSION_SUFFIXES`.

   .. method:: get_code(fullname)

      Trả về ``None`` vì các extension module không có code object.

   .. method:: get_source(fullname)

      Trả về ``None`` vì các extension module không có mã nguồn.

   .. method:: get_filename(fullname)

      Trả về :attr:`path`.

      .. versionadded:: 3.4


.. class:: NamespaceLoader(name, path, path_finder)

   Một triển khai cụ thể của :class:`importlib.abc.InspectLoader` dành cho namespace package. Đây là bí danh của một class riêng tư và chỉ được công khai để kiểm tra thuộc tính ``__loader__`` trên các namespace package::

       >>> from importlib.machinery import NamespaceLoader
       >>> import my_namespace
       >>> isinstance(my_namespace.__loader__, NamespaceLoader)
       True
       >>> import importlib.abc
       >>> isinstance(my_namespace.__loader__, importlib.abc.Loader)
       True

   .. versionadded:: 3.11


.. class:: ModuleSpec(name, loader, *, origin=None, loader_state=None, is_package=None)

   Một đặc tả cho trạng thái liên quan đến import system của một module. Đặc tả này thường được cung cấp dưới dạng thuộc tính :attr:`~module.__spec__` của module. Nhiều thuộc tính trong số này cũng có sẵn trực tiếp trên một module: ví dụ: ``module.__spec__.origin == module.__file__``. Tuy nhiên, lưu ý rằng mặc dù *các giá trị* thường tương đương, chúng có thể khác nhau vì không có cơ chế đồng bộ giữa hai đối tượng. Ví dụ, bạn có thể cập nhật :attr:`~module.__file__` của module tại runtime và thay đổi này sẽ không tự động được phản ánh trong thuộc tính của module
   :attr:`__spec__.origin <ModuleSpec.origin>`, và ngược lại.

   .. versionadded:: 3.4

   .. attribute:: name

      Tên đầy đủ của module (xem :attr:`module.__name__`). :term:`finder` luôn phải đặt thuộc tính này thành một chuỗi không rỗng.

   .. attribute:: loader

      :term:`loader` được dùng để tải module (xem :attr:`module.__loader__`). :term:`finder` luôn phải đặt thuộc tính này.

   .. attribute:: origin

      Vị trí mà :term:`loader` nên sử dụng để tải module (xem :attr:`module.__file__`). Ví dụ, đối với các module được tải từ tệp ``.py``, đây là tên tệp. :term:`finder` luôn phải đặt thuộc tính này thành một giá trị có ý nghĩa để :term:`loader` sử dụng. Trong trường hợp không phổ biến khi không có vị trí này (chẳng hạn như với các namespace package), thuộc tính này phải được đặt thành ``None``.

   .. attribute:: submodule_search_locations

      Một :term:`sequence` các chuỗi (có thể rỗng) liệt kê những vị trí mà tại đó các submodule của package sẽ được tìm thấy (xem :attr:`module.__path__`). Phần lớn thời gian, danh sách này sẽ chỉ có một thư mục duy nhất.

      :term:`finder` phải đặt thuộc tính này thành một sequence, kể cả sequence rỗng, để cho hệ thống import biết rằng module là một package. Với các module không phải package, thuộc tính này phải được đặt thành ``None``. Sau đó, thuộc tính này sẽ tự động được đặt thành một đối tượng đặc biệt đối với namespace package.

   .. attribute:: loader_state

      :term:`finder` có thể đặt thuộc tính này thành một đối tượng chứa dữ liệu bổ sung dành riêng cho module để sử dụng khi tải module. Nếu không, thuộc tính này phải được đặt thành ``None``.

   .. attribute:: cached

      Tên tệp của phiên bản đã biên dịch của mã module (xem :attr:`module.__cached__`). :term:`finder` luôn phải đặt thuộc tính này, nhưng thuộc tính có thể là ``None`` đối với các module không cần lưu trữ mã đã biên dịch.

   .. attribute:: parent

      (Chỉ đọc) Tên đầy đủ của package chứa module (hoặc chuỗi rỗng đối với module cấp cao nhất). Xem :attr:`module.__package__`. Nếu module là một package thì tên này giống với :attr:`name`.

   .. attribute:: has_location

      ``True`` nếu :attr:`origin` của spec tham chiếu đến một vị trí có thể tải, nếu không thì là ``False``. Giá trị này ảnh hưởng đến cách diễn giải :attr:`!origin` và cách điền :attr:`~module.__file__` của module.


.. class:: AppleFrameworkLoader(name, path)

   Một dạng chuyên biệt của :class:`importlib.machinery.ExtensionFileLoader` có khả năng tải các extension module ở định dạng Framework.

   Để tương thích với iOS App Store, *all* binary module trong một ứng dụng iOS phải là dynamic library, được chứa trong một framework có metadata phù hợp và được lưu trong thư mục ``Frameworks`` của ứng dụng đã đóng gói. Mỗi framework chỉ được có một binary duy nhất và không được có dữ liệu binary thực thi nào bên ngoài thư mục Frameworks.

   Để đáp ứng yêu cầu này, khi chạy trên iOS, các binary của extension module *not* được đóng gói dưới dạng các tệp ``.so`` trên ``sys.path``, mà dưới dạng các framework độc lập riêng lẻ. Để phát hiện các framework đó, loader này được đăng ký với phần mở rộng tệp ``.fwork``, trong đó một tệp ``.fwork`` đóng vai trò là placeholder tại vị trí ban đầu của binary trên ``sys.path``. Tệp ``.fwork`` chứa đường dẫn đến binary thực tế trong thư mục ``Frameworks``, tương đối so với app bundle. Để cho phép ánh xạ một binary được đóng gói trong framework trở về vị trí ban đầu, framework được kỳ vọng phải chứa một tệp ``.origin`` chứa vị trí của tệp ``.fwork``, tương đối so với app bundle.

   Ví dụ, hãy xét trường hợp import ``from foo.bar import _whiz``, trong đó ``_whiz`` được triển khai bằng binary module ``sources/foo/bar/_whiz.abi3.so``, với ``sources`` là vị trí được đăng ký trên ``sys.path``, tương đối so với application bundle. Module này *must* được phân phối dưới dạng ``Frameworks/foo.bar._whiz.framework/foo.bar._whiz`` (tạo tên framework từ đường dẫn import đầy đủ của module), với một tệp ``Info.plist`` trong thư mục ``.framework`` xác định binary là một framework. Module ``foo.bar._whiz`` sẽ được biểu diễn tại vị trí ban đầu bằng một tệp đánh dấu ``sources/foo/bar/_whiz.abi3.fwork``, chứa đường dẫn ``Frameworks/foo.bar._whiz/foo.bar._whiz``. Framework cũng sẽ chứa ``Frameworks/foo.bar._whiz.framework/foo.bar._whiz.origin``, chứa đường dẫn đến tệp ``.fwork``.

   Khi một module được tải bằng loader này, ``__file__`` của module sẽ báo cáo vị trí của tệp ``.fwork``. Điều này cho phép code sử dụng ``__file__`` của một module làm mốc để duyệt hệ thống tệp. Tuy nhiên, origin của spec sẽ tham chiếu đến vị trí của binary *actual* trong thư mục ``.framework``.

   Dự án Xcode xây dựng ứng dụng chịu trách nhiệm chuyển đổi mọi tệp ``.so`` từ bất kỳ vị trí nào trong ``PYTHONPATH`` thành các framework trong thư mục ``Frameworks`` (bao gồm việc loại bỏ phần mở rộng khỏi tệp module, thêm metadata của framework và ký framework kết quả), đồng thời tạo các tệp ``.fwork`` và ``.origin``. Thông thường, việc này sẽ được thực hiện bằng một build step trong dự án Xcode; xem tài liệu iOS để biết chi tiết về cách xây dựng build step này.

   .. versionadded:: 3.13

   .. availability:: iOS.

   .. attribute:: name

      Tên của module mà loader hỗ trợ.

   .. attribute:: path

      Đường dẫn đến tệp ``.fwork`` của mô-đun mở rộng.


:mod:`!importlib.util` -- Mã tiện ích cho các importer
------------------------------------------------------

.. module:: importlib.util
    :synopsis: Mã tiện ích cho các importer


**Mã nguồn:** :source:`Lib/importlib/util.py`

--------------

Mô-đun này chứa nhiều đối tượng hỗ trợ việc xây dựng một :term:`importer`.

.. data:: MAGIC_NUMBER

   Các byte biểu diễn số phiên bản bytecode. Nếu cần trợ giúp về việc tải/ghi bytecode, hãy xem :class:`importlib.abc.SourceLoader`.

   .. versionadded:: 3.4

.. function:: cache_from_source(path, debug_override=None, *, optimization=None)

   Trả về đường dẫn :pep:`3147`/:pep:`488` đến tệp đã biên dịch thành bytecode tương ứng với *path* nguồn. Ví dụ: nếu *path* là ``/foo/bar/baz.py`` thì giá trị trả về sẽ là ``/foo/bar/__pycache__/baz.cpython-32.pyc`` đối với Python 3.2. Chuỗi ``cpython-32`` lấy từ thẻ magic hiện tại (xem
   :attr:`sys.implementation.cache_tag <sys.implementation>`; nếu chưa được định nghĩa thì sẽ phát sinh :exc:`NotImplementedError`).

   Tham số *optimization* được dùng để chỉ định mức tối ưu hóa của tệp bytecode. Chuỗi rỗng biểu thị không tối ưu hóa, vì vậy ``/foo/bar/baz.py`` với *optimization* là ``''`` sẽ cho kết quả là đường dẫn bytecode ``/foo/bar/__pycache__/baz.cpython-32.pyc``. ``None`` khiến interpreter sử dụng mức tối ưu hóa của nó. Chuỗi biểu diễn của mọi giá trị khác sẽ được sử dụng, vì vậy ``/foo/bar/baz.py`` với *optimization* là ``2`` sẽ dẫn đến đường dẫn bytecode ``/foo/bar/__pycache__/baz.cpython-32.opt-2.pyc``. Chuỗi biểu diễn của *optimization* chỉ được chứa chữ và số; nếu không, :exc:`ValueError` sẽ được phát sinh.

   Tham số *debug_override* đã lỗi thời và có thể được dùng để ghi đè giá trị hệ thống cho ``__debug__``. Giá trị ``True`` tương đương với việc đặt *optimization* thành chuỗi rỗng. Giá trị ``False`` tương đương với việc đặt *optimization* thành ``1``. Nếu cả *debug_override* và *optimization* đều không phải là ``None`` thì :exc:`TypeError` sẽ được phát sinh.

   .. versionadded:: 3.4

   .. versionchanged:: 3.5
      Tham số *optimization* được bổ sung và tham số *debug_override* đã lỗi thời.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: source_from_cache(path)

   Với *path* trỏ đến tên :pep:`3147` tệp, trả về đường dẫn tệp mã nguồn tương ứng. Ví dụ: nếu *path* là ``/foo/bar/__pycache__/baz.cpython-32.pyc``, đường dẫn được trả về sẽ là ``/foo/bar/baz.py``. Tuy nhiên, *path* không nhất thiết phải tồn tại; nếu không đúng định dạng :pep:`3147` hoặc :pep:`488`, một :exc:`ValueError` sẽ được đưa ra. Nếu
   :attr:`sys.implementation.cache_tag <sys.implementation>` chưa được định nghĩa,
   :exc:`NotImplementedError` được đưa ra.

   .. versionadded:: 3.4

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

.. function:: decode_source(source_bytes)

   Giải mã các byte đã cho biểu diễn mã nguồn và trả về dưới dạng chuỗi với ký tự xuống dòng phổ quát (universal newlines), theo yêu cầu của
   :meth:`importlib.abc.InspectLoader.get_source`).

   .. versionadded:: 3.4

.. function:: resolve_name(name, package)

   Chuyển đổi tên module tương đối thành tên tuyệt đối.

   Nếu **name** không có dấu chấm ở đầu, thì **name** được trả về nguyên trạng. Điều này cho phép sử dụng như ``importlib.util.resolve_name('sys', __spec__.parent)`` mà không cần kiểm tra xem đối số **package** có cần thiết hay không.

   :exc:`ImportError` được phát sinh nếu **name** là tên mô-đun tương đối nhưng **package** có giá trị false (ví dụ: ``None`` hoặc chuỗi rỗng).
   :exc:`ImportError` cũng được phát sinh nếu một tên tương đối thoát ra khỏi package chứa nó (ví dụ: yêu cầu ``..bacon`` từ bên trong package ``spam``).

   .. versionadded:: 3.3

   .. versionchanged:: 3.9
      Để tăng tính nhất quán với các câu lệnh import, hãy phát sinh
      :exc:`ImportError` thay vì :exc:`ValueError` cho các lần thử import tương đối không hợp lệ.

.. function:: find_spec(name, package=None)

   Tìm :term:`spec <module spec>` của một mô-đun, có thể tìm tương đối với tên **package** được chỉ định. Nếu mô-đun nằm trong :data:`sys.modules`, thì ``sys.modules[name].__spec__`` được trả về (trừ khi spec là ``None`` hoặc chưa được thiết lập, trong trường hợp đó :exc:`ValueError` được phát sinh). Nếu không, một tìm kiếm bằng :data:`sys.meta_path` sẽ được thực hiện. ``None`` được trả về nếu không tìm thấy spec.

   Nếu **name** là tên của một submodule (có chứa dấu chấm), module cha sẽ được tự động import.

   **name** và **package** hoạt động giống như đối với
   :func:`importlib.import_module`.

   .. versionadded:: 3.4

   .. versionchanged:: 3.7
      Nêu :exc:`ModuleNotFoundError` thay vì :exc:`AttributeError` nếu **package** thực tế không phải là một package (tức là thiếu một
      thuộc tính :attr:`~module.__path__`).

.. function:: module_from_spec(spec)

   Tạo một module mới dựa trên **spec** và
   :meth:`spec.loader.create_module <importlib.abc.Loader.create_module>`.

   Nếu :meth:`spec.loader.create_module <importlib.abc.Loader.create_module>` không trả về ``None``, thì mọi thuộc tính đã tồn tại trước đó sẽ không được đặt lại. Ngoài ra, sẽ không có :exc:`AttributeError` nào được nêu ra nếu lỗi xảy ra khi truy cập **spec** hoặc đặt một thuộc tính trên module.

   Nên dùng hàm này thay vì sử dụng :class:`types.ModuleType` để tạo module mới, vì **spec** được dùng để đặt nhiều thuộc tính do quá trình import kiểm soát nhất có thể trên module.

   .. versionadded:: 3.5

.. function:: spec_from_loader(name, loader, *, origin=None, is_package=None)

   Một hàm factory để tạo một thực thể :class:`~importlib.machinery.ModuleSpec` dựa trên một loader. Các tham số có cùng ý nghĩa như trong ModuleSpec. Hàm này sử dụng các API :term:`loader` có sẵn, chẳng hạn như
   :meth:`InspectLoader.is_package <importlib.abc.InspectLoader.is_package>`, để điền mọi thông tin còn thiếu vào spec.

   .. versionadded:: 3.4

.. function:: spec_from_file_location(name, location, *, loader=None, submodule_search_locations=None)

   Một factory function để tạo một instance :class:`~importlib.machinery.ModuleSpec` dựa trên đường dẫn đến một tệp. Thông tin còn thiếu sẽ được điền vào spec bằng cách sử dụng các API của loader và dựa trên giả định rằng module này sẽ dựa trên tệp.

   .. versionadded:: 3.4

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

.. function:: source_hash(source_bytes)

   Trả về giá trị băm của *source_bytes* dưới dạng bytes. Một tệp ``.pyc`` dựa trên giá trị băm sẽ nhúng :func:`source_hash` nội dung của tệp nguồn tương ứng vào phần header.

   .. versionadded:: 3.7

.. function:: _incompatible_extension_module_restrictions(*, disable_check)

   Một context manager có thể tạm thời bỏ qua việc kiểm tra tính tương thích đối với các extension module. Theo mặc định, việc kiểm tra được bật và sẽ thất bại khi một module khởi tạo một pha được import trong subinterpreter. Việc kiểm tra cũng sẽ thất bại đối với một module khởi tạo nhiều pha không hỗ trợ rõ ràng GIL riêng cho từng interpreter, khi được import trong một interpreter có GIL riêng.

   Lưu ý rằng function này nhằm xử lý một trường hợp bất thường, có khả năng sẽ biến mất hoàn toàn trong tương lai. Khả năng khá cao là đây không phải điều bạn đang tìm kiếm.

   Bạn có thể đạt được hiệu ứng tương tự như function này bằng cách triển khai interface cơ bản của khởi tạo nhiều pha (:pep:`489`) và khai báo không đúng về khả năng hỗ trợ nhiều interpreter (hoặc GIL riêng cho từng interpreter).

   .. warning::
      Việc sử dụng function này để tắt kiểm tra có thể dẫn đến hành vi không mong đợi, thậm chí gây crash. Chỉ nên sử dụng function này trong quá trình phát triển extension module.

   .. versionadded:: 3.12

.. class:: LazyLoader(loader)

   Một lớp trì hoãn việc thực thi loader của một module cho đến khi một thuộc tính của module được truy cập.

   Lớp này **chỉ** hoạt động với các loader định nghĩa
   :meth:`~importlib.abc.Loader.exec_module` vì cần kiểm soát loại module được sử dụng cho module. Vì những lý do tương tự, phương thức của loader
   :meth:`~importlib.abc.Loader.create_module` phải trả về ``None`` hoặc một kiểu mà thuộc tính ``__class__`` của nó có thể được thay đổi, đồng thời không sử dụng :term:`slots <__slots__>`. Cuối cùng, các module thay thế đối tượng được đặt vào :data:`sys.modules` sẽ không hoạt động vì không có cách nào thay thế đúng cách các tham chiếu đến module trên toàn bộ interpreter một cách an toàn;
   :exc:`ValueError` được phát sinh nếu phát hiện việc thay thế như vậy.

   .. note::
      Đối với các dự án mà thời gian khởi động rất quan trọng, lớp này có thể giúp giảm chi phí tải một module nếu module đó không bao giờ được sử dụng. Đối với các dự án mà thời gian khởi động không thiết yếu, việc sử dụng lớp này bị **khuyến nghị mạnh mẽ** không nên dùng do các thông báo lỗi phát sinh trong quá trình tải bị trì hoãn và vì thế xuất hiện không đúng ngữ cảnh.

   .. versionadded:: 3.5

   .. versionchanged:: 3.6
      Bắt đầu gọi :meth:`~importlib.abc.Loader.create_module`, loại bỏ cảnh báo tương thích đối với :class:`importlib.machinery.BuiltinImporter` và
      :class:`importlib.machinery.ExtensionFileLoader`.

   .. classmethod:: factory(loader)

      Một phương thức của lớp trả về một callable tạo ra lazy loader. Phương thức này được dùng trong những trường hợp loader được truyền vào dưới dạng lớp
      thay vì dưới dạng instance.
      :::::::::::::::::::::::::::

        suffixes = importlib.machinery.SOURCE_SUFFIXES loader = importlib.machinery.SourceFileLoader lazy_loader = importlib.util.LazyLoader.factory(loader) finder = importlib.machinery.FileFinder(path, (lazy_loader, suffixes))

.. _importlib-examples:

Ví dụ
-----

Import theo cách lập trình
''''''''''''''''''''''''''

Để import một module theo cách lập trình, hãy sử dụng :func:`importlib.import_module`.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

  import importlib

  itertools = importlib.import_module('itertools')


Kiểm tra xem một module có thể được import hay không
''''''''''''''''''''''''''''''''''''''''''''''''''''

Nếu bạn cần xác định xem một module có thể được import hay không mà không thực sự thực hiện việc import, bạn nên sử dụng :func:`importlib.util.find_spec`.

Lưu ý rằng nếu ``name`` là một submodule (có chứa dấu chấm),
:func:`importlib.util.find_spec` sẽ import module cha.
::::::::::::::::::::::::::::::::::::::::::::::::::::::

  import importlib.util import sys

  # Chỉ nhằm minh họa. name = 'itertools'

  if name in sys.modules:
      print(f"{name!r} already in sys.modules")
  elif (spec := importlib.util.find_spec(name)) is not None:
      # Nếu bạn chọn thực hiện import thực tế ... module = importlib.util.module_from_spec(spec) sys.modules[name] = module spec.loader.exec_module(module) print(f"{name!r} has been imported")
  else:
      print(f"can't find the {name!r} module")


Import trực tiếp một tệp nguồn
''''''''''''''''''''''''''''''

Thận trọng khi sử dụng công thức này: đây là cách gần đúng để thực hiện câu lệnh import trong đó đường dẫn tệp được chỉ định trực tiếp, thay vì
:data:`sys.path` được tìm kiếm. Trước tiên nên cân nhắc các phương án khác, chẳng hạn như sửa đổi :data:`sys.path` khi cần một module phù hợp, hoặc sử dụng
:func:`runpy.run_path` khi namespace toàn cục tạo ra từ việc chạy tệp Python là phù hợp.

Để import trực tiếp tệp mã nguồn Python từ một đường dẫn, hãy sử dụng công thức sau::

    import importlib.util
    import sys


    def import_from_path(module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module


    # Chỉ nhằm mục đích minh họa (việc sử dụng `json` là tùy ý).
    import json
    file_path = json.__file__
    module_name = json.__name__

    # Kết quả tương tự như `import json`.
    json = import_from_path(module_name, file_path)


Triển khai lazy import
''''''''''''''''''''''

Ví dụ dưới đây cho thấy cách triển khai lazy import::

    >>> import importlib.util
    >>> import sys
    >>> def lazy_import(name):
    ...     spec = importlib.util.find_spec(name)
    ...     loader = importlib.util.LazyLoader(spec.loader)
    ...     spec.loader = loader
    ...     module = importlib.util.module_from_spec(spec)
    ...     sys.modules[name] = module
    ...     loader.exec_module(module)
    ...     return module
    ...
    >>> lazy_typing = lazy_import("typing")
    >>> #lazy_typing là một đối tượng module thực sự,
    >>> #nhưng hiện vẫn chưa được tải vào bộ nhớ.
    >>> lazy_typing.TYPE_CHECKING
    False


Thiết lập importer
''''''''''''''''''

Để tùy chỉnh sâu việc import, thông thường bạn sẽ muốn triển khai một
:term:`importer`. Điều này có nghĩa là quản lý cả phần :term:`finder` và :term:`loader`. Đối với finder, có hai dạng để lựa chọn tùy theo nhu cầu: :term:`meta path finder` hoặc :term:`path entry finder`. Dạng đầu tiên là thứ bạn sẽ đặt trên :data:`sys.meta_path`, còn dạng sau là thứ bạn tạo bằng một :term:`path entry hook` trên :data:`sys.path_hooks`, hoạt động với các mục :data:`sys.path` để có thể tạo ra một finder. Ví dụ này sẽ hướng dẫn bạn cách đăng ký các importer của riêng mình để import sử dụng chúng (để tạo một importer cho chính bạn, hãy đọc tài liệu về các class thích hợp được định nghĩa trong package này)::

  import importlib.machinery
  import sys

  # Chỉ nhằm mục đích minh họa.
  SpamMetaPathFinder = importlib.machinery.PathFinder
  SpamPathEntryFinder = importlib.machinery.FileFinder
  loader_details = (importlib.machinery.SourceFileLoader,
                    importlib.machinery.SOURCE_SUFFIXES)

  # Thiết lập bộ tìm kiếm meta path.
  # Đảm bảo đặt bộ tìm kiếm ở vị trí thích hợp trong danh sách xét theo
  # độ ưu tiên.
  sys.meta_path.append(SpamMetaPathFinder)

  # Thiết lập bộ tìm kiếm mục nhập đường dẫn.
  # Đảm bảo đặt path hook ở vị trí thích hợp trong danh sách xét theo
  # độ ưu tiên.
  sys.path_hooks.append(SpamPathEntryFinder.path_hook(loader_details))


Mô phỏng :func:`importlib.import_module`
''''''''''''''''''''''''''''''''''''''''

Bản thân thao tác import được triển khai bằng mã Python, nhờ đó có thể cung cấp hầu hết cơ chế import thông qua importlib. Phần sau minh họa các API khác nhau mà importlib cung cấp bằng cách đưa ra một cách triển khai gần đúng của
:func:`importlib.import_module`::

  import importlib.util
  import sys

  def import_module(name, package=None):
      """An approximate implementation of import."""
      absolute_name = importlib.util.resolve_name(name, package)
      try:
          return sys.modules[absolute_name]
      except KeyError:
          pass

      path = None
      if '.' in absolute_name:
          parent_name, _, child_name = absolute_name.rpartition('.')
          parent_module = import_module(parent_name)
          path = parent_module.__spec__.submodule_search_locations
      for finder in sys.meta_path:
          spec = finder.find_spec(absolute_name, path)
          if spec is not None:
              break
      else:
          msg = f'No module named {absolute_name!r}'
          raise ModuleNotFoundError(msg, name=absolute_name)
      module = importlib.util.module_from_spec(spec)
      sys.modules[absolute_name] = module
      spec.loader.exec_module(module)
      if path is not None:
          setattr(parent_module, child_name, module)
      return module
