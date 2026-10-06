
.. _importsystem:

***************
Hệ thống import
***************

.. index:: single: import machinery

Mã Python trong một :term:`module` có quyền truy cập vào mã trong một module khác thông qua quá trình :term:`importing` nó. Câu lệnh :keyword:`import` là cách phổ biến nhất để gọi cơ chế import, nhưng không phải là cách duy nhất. Các hàm như :func:`importlib.import_module` và hàm tích hợp sẵn
:func:`__import__` cũng có thể được sử dụng để gọi cơ chế import.

Câu lệnh :keyword:`import` kết hợp hai thao tác; nó tìm kiếm module được đặt tên, sau đó liên kết kết quả của việc tìm kiếm đó với một tên trong phạm vi cục bộ. Thao tác tìm kiếm của câu lệnh :keyword:`!import` được định nghĩa là một lệnh gọi đến hàm :func:`__import__`, với các đối số phù hợp. Giá trị trả về của :func:`__import__` được dùng để thực hiện thao tác liên kết tên của câu lệnh :keyword:`!import`. Xem
câu lệnh :keyword:`!import` để biết chi tiết chính xác về thao tác liên kết tên đó.

Một lệnh gọi trực tiếp đến :func:`__import__` chỉ thực hiện việc tìm kiếm module và, nếu tìm thấy, thao tác tạo module. Mặc dù có thể xảy ra một số tác dụng phụ, chẳng hạn như import các package cha và cập nhật nhiều bộ nhớ đệm khác nhau (bao gồm :data:`sys.modules`), chỉ câu lệnh :keyword:`import` mới thực hiện thao tác liên kết tên.

Khi một câu lệnh :keyword:`import` được thực thi, hàm tích hợp sẵn tiêu chuẩn
:func:`__import__` function được gọi. Các cơ chế khác để gọi import system (chẳng hạn như :func:`importlib.import_module`) có thể chọn bỏ qua
:func:`__import__` và sử dụng các giải pháp riêng để triển khai ngữ nghĩa import.

Khi một module được import lần đầu, Python tìm kiếm module đó và nếu tìm thấy, nó tạo một đối tượng module [#fnmo]_ rồi khởi tạo đối tượng đó. Nếu không tìm thấy module được chỉ định, một :exc:`ModuleNotFoundError` sẽ được phát sinh. Python triển khai nhiều chiến lược khác nhau để tìm kiếm module được chỉ định khi import machinery được gọi. Có thể sửa đổi và mở rộng các chiến lược này bằng cách sử dụng nhiều hook khác nhau được mô tả trong các phần bên dưới.

.. versionchanged:: 3.3
   Import system đã được cập nhật để triển khai đầy đủ giai đoạn thứ hai của :pep:`302`. Không còn import machinery ngầm nào nữa - toàn bộ import system được cung cấp thông qua :data:`sys.meta_path`. Ngoài ra, hỗ trợ native namespace package đã được triển khai (xem :pep:`420`).


:mod:`importlib`
================

Module :mod:`importlib` cung cấp một API phong phú để tương tác với import system. Ví dụ, :func:`importlib.import_module` cung cấp một API đơn giản hơn và được khuyến nghị dùng thay cho :func:`__import__` tích hợp sẵn để gọi import machinery. Tham khảo tài liệu thư viện :mod:`importlib` để biết thêm chi tiết.



Các package
===========

.. index::
    single: package

Python chỉ có một loại đối tượng module, và tất cả module đều thuộc loại này, bất kể module được triển khai bằng Python, C hay một thứ gì khác. Để giúp tổ chức các module và cung cấp một hệ thống phân cấp tên, Python có khái niệm về :term:`package <package>`.

Bạn có thể hình dung packages là các thư mục trên hệ thống tệp và modules là các tệp bên trong thư mục, nhưng đừng hiểu phép tương tự này theo nghĩa quá sát vì packages và modules không nhất thiết phải bắt nguồn từ hệ thống tệp. Trong phạm vi tài liệu này, chúng ta sẽ sử dụng phép tương tự thuận tiện giữa thư mục và tệp. Giống như các thư mục trong hệ thống tệp, packages được tổ chức theo cấp bậc, và bản thân packages có thể chứa các subpackages cũng như các modules thông thường.

Điều quan trọng cần ghi nhớ là mọi package đều là module, nhưng không phải mọi module đều là package. Nói cách khác, packages chỉ là một loại module đặc biệt. Cụ thể, mọi module chứa thuộc tính ``__path__`` đều được xem là package.

Mọi module đều có một tên. Tên của subpackage được phân tách với tên package cha bằng dấu chấm, tương tự cú pháp truy cập thuộc tính tiêu chuẩn của Python. Vì vậy, bạn có thể có một package tên là :mod:`email`, package này lại có một subpackage tên là :mod:`email.mime` và một module bên trong subpackage đó có tên là
:mod:`email.mime.text`.


Packages thông thường
---------------------

.. index::
    pair: package; regular

Python định nghĩa hai loại package: :term:`packages thông thường <regular package>` và :term:`namespace packages <namespace package>`. Packages thông thường là các package truyền thống từng tồn tại trong Python 3.2 và các phiên bản trước đó. Một package thông thường thường được triển khai dưới dạng một thư mục chứa tệp ``__init__.py``. Khi một package thông thường được import, tệp ``__init__.py`` này sẽ được thực thi ngầm, và các đối tượng mà tệp định nghĩa được liên kết với các tên trong namespace của package. Tệp ``__init__.py`` có thể chứa cùng loại mã Python như bất kỳ module nào khác, và Python sẽ thêm một số thuộc tính bổ sung vào module khi module được import.

Ví dụ: bố cục hệ thống tệp sau đây định nghĩa một package ``parent`` cấp cao nhất với ba subpackage::

    parent/
        __init__.py
        one/
            __init__.py
        two/
            __init__.py
        three/
            __init__.py

Việc import ``parent.one`` sẽ ngầm thực thi ``parent/__init__.py`` và ``parent/one/__init__.py``. Các lần import tiếp theo đối với ``parent.two`` hoặc ``parent.three`` sẽ lần lượt thực thi ``parent/two/__init__.py`` và ``parent/three/__init__.py``.

Một thư mục con bên trong một package thông thường không chứa tệp ``__init__.py`` được coi là một
:ref:`namespace package <reference-namespace-package>` (một “namespace subpackage”) nằm trong package cha đó.  Xem :pep:`420` để biết đặc tả cơ sở.


.. _reference-namespace-package:

Namespace package
-----------------

.. index::
    pair: package; namespace
    pair: package; portion

Một namespace package là sự kết hợp của nhiều :term:`portion <portion>` khác nhau, trong đó mỗi portion đóng góp một subpackage cho package cha.  Các portion có thể nằm ở những vị trí khác nhau trên hệ thống tệp.  Các portion cũng có thể nằm trong tệp zip, trên mạng hoặc bất kỳ nơi nào khác mà Python tìm kiếm trong quá trình import.  Namespace package có thể tương ứng trực tiếp hoặc không với các đối tượng trên hệ thống tệp; chúng có thể là các module ảo không có biểu diễn cụ thể.

Namespace package không sử dụng một danh sách thông thường cho thuộc tính ``__path__`` của chúng. Thay vào đó, chúng sử dụng một kiểu iterable tùy chỉnh, kiểu này sẽ tự động thực hiện một lần tìm kiếm mới các portion của package trong lần thử import tiếp theo bên trong package đó nếu đường dẫn của package cha (hoặc :data:`sys.path` đối với package cấp cao nhất) thay đổi.

Với namespace package, không có tệp ``parent/__init__.py``.  Trên thực tế, có thể có nhiều thư mục ``parent`` được tìm thấy trong quá trình tìm kiếm import, trong đó mỗi thư mục được cung cấp bởi một portion khác nhau.  Vì vậy, ``parent/one`` có thể không nằm trên thực tế cạnh ``parent/two``.  Trong trường hợp này, Python sẽ tạo một namespace package cho package ``parent`` cấp cao nhất bất cứ khi nào package đó hoặc một trong các subpackage của nó được import.

Namespace package cũng có thể được lồng bên trong một package thông thường.  Khi hệ thống import tìm kiếm ``__path__`` của một package thông thường và gặp một thư mục con không chứa tệp ``__init__.py``, thư mục con đó trở thành một :term:`portion`, đóng góp vào một namespace subpackage của package thông thường bao quanh.

Xem thêm :pep:`420` để biết đặc tả về namespace package.


Tìm kiếm
========

Để bắt đầu quá trình tìm kiếm, Python cần tên :term:`đầy đủ <qualified name>` của module (hoặc package, nhưng trong phạm vi thảo luận này, sự khác biệt là không đáng kể) đang được import. Tên này có thể đến từ nhiều đối số khác nhau của câu lệnh :keyword:`import`, hoặc từ các tham số của
hàm :func:`importlib.import_module` hoặc :func:`__import__`.

Tên này sẽ được sử dụng trong nhiều giai đoạn khác nhau của quá trình tìm kiếm import và có thể là đường dẫn phân tách bằng dấu chấm đến một submodule, ví dụ ``foo.bar.baz``. Trong trường hợp này, Python trước tiên thử import ``foo``, sau đó ``foo.bar``, và cuối cùng là ``foo.bar.baz``. Nếu bất kỳ lần import trung gian nào thất bại, một :exc:`ModuleNotFoundError` sẽ được đưa ra.


Bộ nhớ đệm module
-----------------

.. index::
    single: sys.modules

Nơi đầu tiên được kiểm tra trong quá trình tìm kiếm import là :data:`sys.modules`. Ánh xạ này đóng vai trò là bộ nhớ đệm của tất cả module đã được import trước đó, bao gồm cả các đường dẫn trung gian. Vì vậy, nếu ``foo.bar.baz`` đã được import trước đó, :data:`sys.modules` sẽ chứa các mục cho ``foo``, ``foo.bar`` và ``foo.bar.baz``. Mỗi khóa sẽ có giá trị là đối tượng module tương ứng.

Trong quá trình import, tên module được tra cứu trong :data:`sys.modules` và nếu có, giá trị tương ứng là module đáp ứng việc import, quá trình sẽ hoàn tất. Tuy nhiên, nếu giá trị là ``None``, thì một
:exc:`ModuleNotFoundError` được phát sinh. Nếu không tìm thấy tên module, Python sẽ tiếp tục tìm kiếm module đó.

:data:`sys.modules` có thể ghi. Việc xóa một khóa có thể không hủy module tương ứng (vì các module khác có thể vẫn giữ tham chiếu đến module đó), nhưng sẽ làm mất hiệu lực mục nhập bộ nhớ đệm của module được đặt tên, khiến Python tìm lại module đó trong lần import tiếp theo. Khóa này cũng có thể được gán cho ``None``, buộc lần import module tiếp theo phải dẫn đến :exc:`ModuleNotFoundError`.

Tuy nhiên, hãy cẩn thận: nếu bạn giữ một tham chiếu đến đối tượng module, làm mất hiệu lực mục nhập bộ nhớ đệm của nó trong :data:`sys.modules`, rồi import lại module được đặt tên, thì hai đối tượng module sẽ *không* giống nhau. Ngược lại,
:func:`importlib.reload` sẽ sử dụng lại đối tượng module *giống*, và chỉ khởi tạo lại nội dung module bằng cách chạy lại mã của module.


.. _finders-and-loaders:

Finder và loader
----------------

.. index::
    single: finder
    single: loader
    single: module spec

Nếu không tìm thấy module được đặt tên trong :data:`sys.modules`, giao thức import của Python sẽ được gọi để tìm và tải module. Giao thức này bao gồm hai đối tượng mang tính khái niệm, :term:`finder <finder>` và :term:`loader <loader>`. Nhiệm vụ của finder là xác định xem nó có thể tìm thấy module được đặt tên bằng chiến lược mà nó biết hay không. Các đối tượng triển khai cả hai giao diện này được gọi là :term:`importer <importer>` - chúng trả về chính mình khi phát hiện rằng mình có thể tải module được yêu cầu.

Python bao gồm một số finder và importer mặc định. Finder đầu tiên biết cách định vị các module tích hợp sẵn, còn importer thứ hai biết cách định vị các module frozen. Một finder mặc định thứ ba tìm kiếm các module trong :term:`import path`. :term:`import path` là danh sách các vị trí có thể là đường dẫn hệ thống tệp hoặc tệp zip. Nó cũng có thể được mở rộng để tìm kiếm mọi tài nguyên có thể định vị, chẳng hạn như các tài nguyên được xác định bằng URL.

Cơ chế import có thể mở rộng, vì vậy có thể thêm các finder mới để mở rộng phạm vi và quy mô tìm kiếm module.

Finder không thực sự tải module. Nếu có thể tìm thấy module được chỉ định, chúng trả về một :dfn:`module spec`, là một đối tượng đóng gói thông tin liên quan đến việc import module, sau đó được cơ chế import sử dụng khi tải module.

Các phần sau mô tả chi tiết hơn về giao thức dành cho finder và loader, bao gồm cách bạn có thể tạo và đăng ký các thành phần mới để mở rộng cơ chế import.

.. versionchanged:: 3.4
   Trong các phiên bản Python trước đây, finder trả về trực tiếp :term:`loaders <loader>`, trong khi hiện nay chúng trả về module spec, các module spec này *contain* loader. Loader vẫn được sử dụng trong quá trình import nhưng có ít trách nhiệm hơn.

Import hook
-----------

.. index::
   single: import hooks
   single: meta hooks
   single: path hooks
   pair: hooks; import
   pair: hooks; meta
   pair: hooks; path

Cơ chế import được thiết kế để có thể mở rộng; cơ chế chính cho việc này là *import hooks*. Có hai loại import hook: *meta hooks* và *import path hooks*.

Meta hook được gọi khi bắt đầu quá trình import, trước khi bất kỳ quá trình import nào khác diễn ra, ngoại trừ việc tra cứu cache :data:`sys.modules`. Điều này cho phép meta hook ghi đè quá trình xử lý :data:`sys.path`, các frozen module hoặc thậm chí các built-in module. Meta hook được đăng ký bằng cách thêm các đối tượng finder mới vào :data:`sys.meta_path`, như mô tả bên dưới.

Import path hook được gọi trong quá trình xử lý :data:`sys.path` (hoặc ``package.__path__``), tại thời điểm gặp path item liên kết với chúng. Import path hook được đăng ký bằng cách thêm các callable mới vào :data:`sys.path_hooks` như mô tả bên dưới.


Meta path
---------

.. index::
    single: sys.meta_path
    pair: finder; find_spec

Khi không tìm thấy module có tên trong :data:`sys.modules`, Python tiếp tục tìm kiếm trong :data:`sys.meta_path`, nơi chứa danh sách các đối tượng meta path finder. Các finder này được truy vấn theo thứ tự để xem chúng có biết cách xử lý module có tên đó hay không. Meta path finder phải triển khai một phương thức có tên
:meth:`~importlib.abc.MetaPathFinder.find_spec`, phương thức này nhận ba đối số: một tên, một import path và một target module (tùy chọn). Meta path finder có thể sử dụng bất kỳ chiến lược nào để xác định liệu nó có thể xử lý module có tên đó hay không.

Nếu meta path finder biết cách xử lý module có tên đó, nó trả về một spec object. Nếu không thể xử lý module có tên đó, nó trả về ``None``. Nếu
Quá trình xử lý :data:`sys.meta_path` đi đến cuối danh sách mà không trả về spec, một :exc:`ModuleNotFoundError` sẽ được raised. Mọi exception khác được raised sẽ פשוט được truyền lên, khiến quá trình import bị hủy bỏ.

Phương thức :meth:`~importlib.abc.MetaPathFinder.find_spec` của các meta path finder được gọi với hai hoặc ba đối số. Đối số đầu tiên là tên đầy đủ của module đang được import, chẳng hạn như ``foo.bar.baz``. Đối số thứ hai là các mục đường dẫn được sử dụng để tìm kiếm module. Đối với các module cấp cao nhất, đối số thứ hai là ``None``, nhưng đối với các submodule hoặc subpackage, đối số thứ hai là giá trị của thuộc tính ``__path__`` của package cha. Nếu không thể truy cập thuộc tính ``__path__`` thích hợp, một :exc:`ModuleNotFoundError` sẽ được raise. Đối số thứ ba là một đối tượng module hiện có, sẽ là đối tượng đích để load sau đó. Hệ thống import chỉ truyền vào một module đích trong quá trình reload.

Meta path có thể được duyệt nhiều lần cho một yêu cầu import duy nhất. Ví dụ, giả sử chưa có module nào liên quan được cache, khi import ``foo.bar.baz``, trước tiên sẽ thực hiện một lần import cấp cao nhất, gọi ``mpf.find_spec("foo", None, None)`` trên từng meta path finder (``mpf``). Sau khi ``foo`` được import, ``foo.bar`` sẽ được import bằng cách duyệt meta path lần thứ hai và gọi ``mpf.find_spec("foo.bar", foo.__path__, None)``. Sau khi ``foo.bar`` được import, lần duyệt cuối cùng sẽ gọi ``mpf.find_spec("foo.bar.baz", foo.bar.__path__, None)``.

Một số meta path finder chỉ hỗ trợ import cấp cao nhất. Các importer này sẽ luôn trả về ``None`` khi đối số thứ hai được truyền vào là bất kỳ giá trị nào khác ``None``.

:data:`sys.meta_path` mặc định của Python có ba meta path finder: một finder biết cách import các module tích hợp sẵn, một finder biết cách import các module frozen, và một finder biết cách import module từ một :term:`import path` (tức là :term:`path based finder`).

.. versionchanged:: 3.4
   Phương thức :meth:`~importlib.abc.MetaPathFinder.find_spec` của các meta path finder đã thay thế :meth:`!find_module`, hiện đã deprecated. Mặc dù phương thức này vẫn sẽ tiếp tục hoạt động mà không cần thay đổi, cơ chế import sẽ chỉ thử phương thức này nếu finder không triển khai
   :meth:`~importlib.abc.MetaPathFinder.find_spec`.

.. versionchanged:: 3.10
   Việc hệ thống import sử dụng :meth:`!find_module` hiện sẽ raise :exc:`ImportWarning`.

.. versionchanged:: 3.12
   :meth:`!find_module` has been removed.
   Thay vào đó, hãy sử dụng :meth:`~importlib.abc.MetaPathFinder.find_spec`.


Đang tải
========

Nếu và khi tìm thấy module spec, cơ chế import sẽ sử dụng nó (cùng với loader mà nó chứa) khi tải module. Dưới đây là mô phỏng gần đúng những gì xảy ra trong phần tải của quá trình import::

    module = None
    if spec.loader is not None and hasattr(spec.loader, 'create_module'):
        # Giả định rằng 'exec_module' cũng được định nghĩa trên loader.
        module = spec.loader.create_module(spec)
    if module is None:
        module = ModuleType(spec.name)
    # Các thuộc tính liên quan đến import được thiết lập tại đây:
    _init_module_attrs(spec, module)

    if spec.loader is None:
        # không được hỗ trợ
        raise ImportError
    if spec.origin is None and spec.submodule_search_locations is not None:
        # gói namespace
        sys.modules[spec.name] = module
    elif not hasattr(spec.loader, 'exec_module'):
        module = spec.loader.load_module(spec.name)
    else:
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            try:
                del sys.modules[spec.name]
            except KeyError:
                pass
            raise
    return sys.modules[spec.name]

Lưu ý các chi tiết sau:

* Nếu đã có một đối tượng module với tên đã cho trong
  :data:`sys.modules`, thao tác import sẽ trả về đối tượng đó.

* Module sẽ tồn tại trong :data:`sys.modules` trước khi loader thực thi mã của module. Điều này rất quan trọng vì mã của module có thể import chính nó (trực tiếp hoặc gián tiếp); việc thêm module vào :data:`sys.modules` trước đó sẽ ngăn đệ quy vô hạn trong trường hợp xấu nhất và ngăn việc tải nhiều lần trong trường hợp tốt nhất.

* Nếu việc tải thất bại, module bị lỗi -- và chỉ module bị lỗi đó -- sẽ bị xóa khỏi :data:`sys.modules`. Bất kỳ module nào đã có trong
  bộ nhớ đệm :data:`sys.modules`, cũng như bất kỳ module nào được tải thành công dưới dạng tác dụng phụ, đều phải vẫn nằm trong bộ nhớ đệm. Điều này khác với việc tải lại, khi ngay cả module bị lỗi cũng vẫn được giữ trong :data:`sys.modules`.

* Sau khi module được tạo nhưng trước khi thực thi, cơ chế import sẽ thiết lập các thuộc tính của module liên quan đến import ("_init_module_attrs" trong ví dụ mã giả ở trên), như được tóm tắt trong
  :ref:`phần sau <import-mod-attrs>`.

* Thực thi module là thời điểm then chốt trong quá trình tải, khi namespace của module được điền dữ liệu. Việc thực thi hoàn toàn do loader đảm nhiệm; loader quyết định nội dung nào được điền và cách điền.

* Module được tạo trong quá trình tải và được truyền vào exec_module() có thể không phải là module được trả về khi kết thúc import [#fnlo]_.

.. versionchanged:: 3.4
   Hệ thống import đã tiếp quản các trách nhiệm mã mẫu (boilerplate) của loader. Trước đây, những trách nhiệm này được thực hiện bởi
   phương thức :meth:`importlib.abc.Loader.load_module`.

Loaders
-------

Loader của module cung cấp chức năng cốt lõi của việc tải: thực thi module. Bộ máy import gọi phương thức :meth:`importlib.abc.Loader.exec_module` với một đối số duy nhất là đối tượng module cần thực thi. Mọi giá trị được trả về từ :meth:`~importlib.abc.Loader.exec_module` đều bị bỏ qua.

Loader phải đáp ứng các yêu cầu sau:

* Nếu module là một Python module (không phải module tích hợp sẵn hoặc extension được tải động), loader phải thực thi mã của module trong không gian tên toàn cục của module (``module.__dict__``).

* Nếu loader không thể thực thi module, nó phải phát sinh một
  :exc:`ImportError`, mặc dù mọi ngoại lệ khác phát sinh trong quá trình
  :meth:`~importlib.abc.Loader.exec_module` sẽ được truyền tiếp.

Trong nhiều trường hợp, finder và loader có thể là cùng một đối tượng; trong những trường hợp đó, phương thức
:meth:`~importlib.abc.MetaPathFinder.find_spec` chỉ cần trả về một spec với loader được đặt thành ``self``.

Các module loader có thể chọn tạo đối tượng module trong quá trình loading bằng cách triển khai phương thức :meth:`~importlib.abc.Loader.create_module`. Phương thức này nhận một đối số, là module spec, và trả về đối tượng module mới để sử dụng trong quá trình loading. ``create_module()`` không cần thiết lập bất kỳ thuộc tính nào trên đối tượng module. Nếu phương thức trả về ``None``, cơ chế import sẽ tự tạo module mới.

.. versionadded:: 3.4
   Phương thức :meth:`~importlib.abc.Loader.create_module` của các loader.

.. versionchanged:: 3.4
   Phương thức :meth:`~importlib.abc.Loader.load_module` đã được thay thế bởi
   :meth:`~importlib.abc.Loader.exec_module` và cơ chế import đã đảm nhiệm mọi công việc khung cần thiết cho việc nạp.

   Để tương thích với các loader hiện có, cơ chế import sẽ sử dụng phương thức ``load_module()`` của loader nếu phương thức này tồn tại và loader không đồng thời triển khai ``exec_module()``. Tuy nhiên, ``load_module()`` đã không còn được khuyến nghị và loader nên triển khai ``exec_module()`` thay thế.

   Phương thức ``load_module()`` phải triển khai toàn bộ chức năng khung cần thiết cho việc nạp được mô tả ở trên, ngoài việc thực thi module. Mọi ràng buộc tương tự vẫn được áp dụng, cùng một số điểm làm rõ bổ sung:

   * Nếu đã có một đối tượng module với tên đã cho trong
     :data:`sys.modules`, loader phải sử dụng module hiện có đó. (Nếu không, :func:`importlib.reload` sẽ không hoạt động chính xác.) Nếu module có tên không tồn tại trong :data:`sys.modules`, loader phải tạo một đối tượng module mới và thêm đối tượng đó vào :data:`sys.modules`.

   * Mô-đun *must* tồn tại trong :data:`sys.modules` trước khi loader thực thi mã của mô-đun, nhằm ngăn đệ quy không bị giới hạn hoặc việc tải nhiều lần.

   * Nếu việc tải thất bại, loader phải xóa mọi mô-đun mà nó đã chèn vào :data:`sys.modules`, nhưng chỉ được xóa **only** các mô-đun bị lỗi và chỉ khi chính loader đã tải các mô-đun đó một cách tường minh.

.. versionchanged:: 3.5
   Một :exc:`DeprecationWarning` được phát sinh khi ``exec_module()`` được định nghĩa nhưng ``create_module()`` thì không.

.. versionchanged:: 3.6
   Một :exc:`ImportError` được phát sinh khi ``exec_module()`` được định nghĩa nhưng ``create_module()`` thì không.

.. versionchanged:: 3.10
   Việc sử dụng ``load_module()`` sẽ phát sinh :exc:`ImportWarning`.

Mô-đun con
----------

Khi một mô-đun con được tải bằng bất kỳ cơ chế nào (ví dụ: các API ``importlib``, các câu lệnh ``import`` hoặc ``import-from``, hay ``__import__()`` tích hợp sẵn), một binding được đặt trong namespace của mô-đun cha để trỏ đến đối tượng mô-đun con. Ví dụ, nếu package ``spam`` có một mô-đun con ``foo``, sau khi import ``spam.foo``, ``spam`` sẽ có một thuộc tính ``foo`` được liên kết với mô-đun con. Giả sử bạn có cấu trúc thư mục sau đây::

    spam/
        __init__.py
        foo.py

và ``spam/__init__.py`` có dòng sau trong đó::

    from .foo import Foo

sau đó thực thi nội dung sau sẽ đặt các liên kết tên cho ``foo`` và ``Foo`` trong module ``spam``::

    >>> import spam
    >>> spam.foo
    <module 'spam.foo' from '/tmp/imports/spam/foo.py'>
    >>> spam.Foo
    <class 'spam.foo.Foo'>

Với các quy tắc liên kết tên quen thuộc của Python, điều này có vẻ đáng ngạc nhiên, nhưng thực ra đây là một tính năng nền tảng của hệ thống import. Bất biến được duy trì là nếu bạn có ``sys.modules['spam']`` và ``sys.modules['spam.foo']`` (như sau thao tác import ở trên), thì ``sys.modules['spam.foo']`` phải xuất hiện dưới dạng thuộc tính ``foo`` của ``sys.modules['spam']``.

.. _module-specs:

Đặc tả module
-------------

Cơ chế import sử dụng nhiều loại thông tin về từng module trong quá trình import, đặc biệt là trước khi tải. Phần lớn thông tin là chung cho mọi module. Mục đích của đặc tả module là đóng gói thông tin liên quan đến import này theo từng module.

Việc sử dụng đặc tả trong quá trình import cho phép truyền trạng thái giữa các thành phần của hệ thống import, chẳng hạn giữa finder tạo đặc tả module và loader thực thi đặc tả đó. Quan trọng nhất, nó cho phép cơ chế import thực hiện các thao tác soạn sẵn để tải, trong khi nếu không có đặc tả module thì loader phải chịu trách nhiệm đó.

Đặc tả của module được cung cấp dưới dạng :attr:`module.__spec__`. Việc thiết lập
:attr:`!__spec__` cũng áp dụng tương tự cho
:ref:`các mô-đun được khởi tạo trong quá trình khởi động trình thông dịch <programs>`. Ngoại lệ duy nhất là ``__main__``, trong đó :attr:`!__spec__` là
:ref:`được đặt thành None trong một số trường hợp <main_spec>`.

Xem :class:`~importlib.machinery.ModuleSpec` để biết chi tiết về nội dung của module spec.

.. versionadded:: 3.4

.. _package-path-rules:

Các thuộc tính __path__ trên mô-đun
-----------------------------------

Thuộc tính :attr:`~module.__path__` phải là một (có thể rỗng)
:term:`sequence` gồm các chuỗi liệt kê những vị trí chứa các submodule của package. Theo định nghĩa, nếu một mô-đun có thuộc tính :attr:`!__path__`, thì đó là một :term:`package`.

Thuộc tính :attr:`~module.__path__` của một package được sử dụng khi import các subpackage của package đó. Trong cơ chế import, thuộc tính này hoạt động gần như :data:`sys.path`, tức là cung cấp danh sách các vị trí cần tìm module trong quá trình import. Tuy nhiên, :attr:`!__path__` thường bị giới hạn hơn nhiều so với
:data:`!sys.path`.

Các quy tắc tương tự được áp dụng cho :data:`sys.path` cũng áp dụng cho
:attr:`!__path__`. :data:`sys.path_hooks` (được mô tả bên dưới) được tham chiếu khi duyệt qua :attr:`!__path__` của một package.

Tệp ``__init__.py`` của một package có thể thiết lập hoặc thay đổi thuộc tính
:attr:`~module.__path__` của package, và trước :pep:`420`, đây thường là cách các namespace package được triển khai. Với việc áp dụng :pep:`420`, namespace package không còn cần cung cấp các tệp ``__init__.py`` chỉ chứa mã thao tác với :attr:`!__path__`; cơ chế import sẽ tự động thiết lập đúng :attr:`!__path__` cho namespace package.

repr của module
---------------

Theo mặc định, tất cả module đều có repr có thể sử dụng; tuy nhiên, tùy thuộc vào các thuộc tính được thiết lập ở trên và trong spec của module, bạn có thể kiểm soát rõ ràng hơn repr của các đối tượng module.

Nếu module có một spec (``__spec__``), cơ chế import sẽ cố gắng tạo repr từ spec đó. Nếu không thành công hoặc không có spec, hệ thống import sẽ tạo repr mặc định bằng bất kỳ thông tin nào có sẵn trên module. Hệ thống sẽ cố gắng sử dụng ``module.__name__``, ``module.__file__`` và ``module.__loader__`` làm đầu vào cho repr, đồng thời dùng giá trị mặc định cho mọi thông tin còn thiếu.

Dưới đây là các quy tắc chính xác được sử dụng:

* Nếu module có thuộc tính ``__spec__``, thông tin trong spec sẽ được sử dụng để tạo repr. Các thuộc tính "name", "loader", "origin" và "has_location" sẽ được kiểm tra.

* Nếu module có thuộc tính ``__file__``, thuộc tính này sẽ được sử dụng như một phần của repr của module.

* Nếu module không có ``__file__`` nhưng có ``__loader__`` khác ``None``, repr của loader sẽ được sử dụng như một phần của repr của module.

* Nếu không, chỉ cần sử dụng ``__name__`` của module trong repr.

.. versionchanged:: 3.12
   Việc sử dụng :meth:`!module_repr`, vốn đã bị deprecated từ Python 3.4, đã bị loại bỏ trong Python 3.12 và không còn được gọi trong quá trình xác định repr của module.

.. _pyc-invalidation:

Vô hiệu hóa bytecode đã lưu trong bộ nhớ đệm
--------------------------------------------

Trước khi Python tải bytecode đã lưu trong bộ nhớ đệm từ tệp ``.pyc``, nó kiểm tra xem bộ nhớ đệm có được cập nhật theo tệp nguồn ``.py`` hay không. Theo mặc định, Python thực hiện việc này bằng cách lưu dấu thời gian sửa đổi lần cuối và kích thước của tệp nguồn vào tệp bộ nhớ đệm khi ghi tệp đó. Khi runtime chạy, hệ thống import sẽ xác thực tệp bộ nhớ đệm bằng cách đối chiếu siêu dữ liệu được lưu trong tệp bộ nhớ đệm với siêu dữ liệu của tệp nguồn.

Python cũng hỗ trợ các tệp bộ nhớ đệm "dựa trên hash", lưu hash của nội dung tệp nguồn thay vì siêu dữ liệu của tệp. Có hai biến thể của tệp ``.pyc`` dựa trên hash: được kiểm tra và không được kiểm tra. Đối với các tệp ``.pyc`` dựa trên hash được kiểm tra, Python xác thực tệp bộ nhớ đệm bằng cách tính hash của tệp nguồn rồi so sánh hash thu được với hash trong tệp bộ nhớ đệm. Nếu một tệp bộ nhớ đệm dựa trên hash được kiểm tra được phát hiện là không hợp lệ, Python sẽ tạo lại tệp đó và ghi một tệp bộ nhớ đệm mới dựa trên hash được kiểm tra. Đối với các tệp ``.pyc`` dựa trên hash không được kiểm tra, Python chỉ cần giả định rằng tệp bộ nhớ đệm hợp lệ nếu tệp đó tồn tại. Hành vi xác thực các tệp ``.pyc`` dựa trên hash có thể được ghi đè bằng cờ :option:`--check-hash-based-pycs`.

.. versionchanged:: 3.7
   Đã bổ sung các tệp ``.pyc`` dựa trên hash. Trước đây, Python chỉ hỗ trợ cơ chế vô hiệu hóa dựa trên dấu thời gian đối với các bộ nhớ đệm bytecode.


Trình tìm kiếm dựa trên đường dẫn
=================================

.. index::
    single: path based finder

Như đã đề cập trước đó, Python đi kèm với một số trình tìm kiếm meta path mặc định. Một trong số đó, được gọi là :term:`path based finder` (:class:`~importlib.machinery.PathFinder`), tìm kiếm trong một :term:`import path`, chứa danh sách các mục :term:`path entries <path entry>`. Mỗi mục đường dẫn chỉ định một vị trí để tìm kiếm các module.

Bản thân trình tìm kiếm dựa trên đường dẫn không biết cách import bất cứ thứ gì. Thay vào đó, nó duyệt qua từng mục đường dẫn, liên kết mỗi mục với một trình tìm kiếm mục đường dẫn biết cách xử lý loại đường dẫn cụ thể đó.

Tập hợp mặc định các trình tìm mục đường dẫn triển khai toàn bộ ngữ nghĩa để tìm module trên hệ thống tệp, xử lý các loại tệp đặc biệt như mã nguồn Python (các tệp ``.py``), byte code Python (các tệp ``.pyc``) và thư viện dùng chung (ví dụ: các tệp ``.so``). Khi được module :mod:`zipimport` trong thư viện chuẩn hỗ trợ, các trình tìm mục đường dẫn mặc định cũng xử lý việc tải tất cả các loại tệp này (ngoại trừ thư viện dùng chung) từ các tệp zip.

Các mục đường dẫn không nhất thiết phải giới hạn ở những vị trí trên hệ thống tệp. Chúng có thể tham chiếu đến URL, truy vấn cơ sở dữ liệu hoặc bất kỳ vị trí nào khác có thể được chỉ định dưới dạng chuỗi.

Trình tìm dựa trên đường dẫn cung cấp các hook và protocol bổ sung để bạn có thể mở rộng và tùy chỉnh các loại mục đường dẫn có thể tìm kiếm. Ví dụ: nếu muốn hỗ trợ các mục đường dẫn dưới dạng URL mạng, bạn có thể viết một hook triển khai ngữ nghĩa HTTP để tìm module trên web. Hook này (một callable) sẽ trả về một :term:`path entry finder` hỗ trợ protocol được mô tả bên dưới, sau đó được dùng để lấy loader cho module từ web.

Xin lưu ý: phần này và phần trước đều sử dụng thuật ngữ *finder*, phân biệt chúng bằng cách sử dụng các thuật ngữ :term:`meta path finder` và
:term:`path entry finder`. Hai loại finder này rất giống nhau, hỗ trợ các protocol tương tự và hoạt động theo những cách tương tự trong quá trình import, nhưng điều quan trọng là cần nhớ rằng chúng khác nhau một cách tinh tế. Cụ thể, meta path finder hoạt động ở đầu quá trình import, dựa trên quá trình duyệt :data:`sys.meta_path`.

Ngược lại, các trình tìm mục đường dẫn theo một nghĩa nào đó là chi tiết triển khai của trình tìm dựa trên đường dẫn; trên thực tế, nếu trình tìm dựa trên đường dẫn bị xóa khỏi :data:`sys.meta_path`, thì sẽ không có ngữ nghĩa nào của trình tìm mục đường dẫn được gọi.


Các trình tìm mục đường dẫn
---------------------------

.. index::
    single: sys.path
    single: sys.path_hooks
    single: sys.path_importer_cache
    single: PYTHONPATH

:term:`path based finder` chịu trách nhiệm tìm và tải các module và package Python có vị trí được chỉ định bằng một chuỗi
:term:`path entry`. Hầu hết các mục đường dẫn đều chỉ đến các vị trí trong hệ thống tệp, nhưng không nhất thiết phải giới hạn ở đó.

Với vai trò là một meta path finder, :term:`path based finder` triển khai
giao thức :meth:`~importlib.abc.MetaPathFinder.find_spec` đã được mô tả trước đó, tuy nhiên nó cung cấp thêm các hook có thể được sử dụng để tùy chỉnh cách tìm và tải module từ :term:`import path`.

Ba biến được :term:`path based finder`, :data:`sys.path` sử dụng,
:data:`sys.path_hooks` và :data:`sys.path_importer_cache`. Các thuộc tính ``__path__`` trên các đối tượng package cũng được sử dụng. Những thành phần này cung cấp thêm các cách để tùy chỉnh cơ chế import.

:data:`sys.path` chứa một danh sách các chuỗi cung cấp các vị trí tìm kiếm cho module và package. Nó được khởi tạo từ biến môi trường :envvar:`PYTHONPATH` và nhiều giá trị mặc định khác phụ thuộc vào quá trình cài đặt và implementation. Các mục trong :data:`sys.path` có thể chỉ đến các thư mục trong hệ thống tệp, các tệp zip và có khả năng là những “vị trí” khác (xem module :mod:`site`) cần được tìm kiếm để tìm module, chẳng hạn như URL hoặc truy vấn cơ sở dữ liệu. Chỉ các chuỗi mới nên xuất hiện trong
:data:`sys.path`; tất cả các kiểu dữ liệu khác đều bị bỏ qua.

:term:`path based finder` là một :term:`meta path finder`, vì vậy cơ chế import bắt đầu quá trình tìm kiếm :term:`import path` bằng cách gọi phương thức :meth:`~importlib.machinery.PathFinder.find_spec` của path-based finder như đã mô tả trước đó. Khi đối số ``path`` được truyền cho
:meth:`~importlib.machinery.PathFinder.find_spec`, nó sẽ là một danh sách các path dạng chuỗi cần duyệt qua — thường là thuộc tính ``__path__`` của một package khi thực hiện import bên trong package đó. Nếu đối số ``path`` là ``None``, điều này cho biết đây là một import cấp cao nhất và :data:`sys.path` được sử dụng.

path-based finder lặp qua mọi entry trong search path và, với mỗi entry, tìm một :term:`path entry finder` (:class:`~importlib.abc.PathEntryFinder`) thích hợp cho path entry đó. Vì đây có thể là một thao tác tốn kém (ví dụ: việc tìm kiếm này có thể phát sinh chi phí gọi ``stat()``), path-based finder duy trì một cache ánh xạ các path entry với các path entry finder. Cache này được duy trì trong :data:`sys.path_importer_cache` (dù tên gọi như vậy, cache này thực tế lưu các finder object thay vì chỉ giới hạn ở các object :term:`importer`). Nhờ đó, việc tìm kiếm tốn kém để xác định :term:`path entry` của một vị trí cụ thể và :term:`path entry finder` của vị trí đó chỉ cần thực hiện một lần. Mã người dùng có thể tự do xóa các mục cache khỏi :data:`sys.path_importer_cache`, buộc path-based finder thực hiện lại việc tìm kiếm path entry.

Nếu path entry không có trong cache, path-based finder lặp qua mọi callable trong :data:`sys.path_hooks`. Mỗi :term:`hook path entry <path entry hook>` trong danh sách này được gọi với một đối số duy nhất là path entry cần tìm kiếm. Callable này có thể trả về một :term:`path entry finder` có khả năng xử lý path entry, hoặc có thể phát sinh
:exc:`ImportError`. Một :exc:`ImportError` được path-based finder sử dụng để báo hiệu rằng hook không thể tìm thấy :term:`path entry finder` cho :term:`path entry` đó. Exception bị bỏ qua và quá trình lặp :term:`import path` tiếp tục. Hook nên chờ một object dạng chuỗi hoặc bytes; encoding của các object bytes tùy thuộc vào hook (ví dụ: có thể là encoding của file system, UTF-8 hoặc một encoding khác), và nếu hook không thể decode đối số đó, nó nên phát sinh
:exc:`ImportError`.

Nếu quá trình lặp :data:`sys.path_hooks` kết thúc mà không trả về :term:`path entry finder`, thì path-based finder sẽ
Phương thức :meth:`~importlib.machinery.PathFinder.find_spec` sẽ lưu ``None`` vào :data:`sys.path_importer_cache` (để cho biết rằng không có finder nào cho mục nhập đường dẫn này) và trả về ``None``, cho biết rằng điều này
:term:`meta path finder` không thể tìm thấy module.

Nếu một :term:`path entry finder` *được* trả về bởi một trong các callable :term:`path entry hook` trên :data:`sys.path_hooks`, thì giao thức sau được sử dụng để yêu cầu finder cung cấp module spec, sau đó spec này được dùng khi tải module.

Thư mục làm việc hiện tại -- được biểu thị bằng một chuỗi rỗng -- được xử lý hơi khác so với các mục nhập khác trên :data:`sys.path`. Trước tiên, nếu không thể xác định thư mục làm việc hiện tại hoặc phát hiện thư mục này không tồn tại, không có giá trị nào được lưu trong :data:`sys.path_importer_cache`. Thứ hai, giá trị của thư mục làm việc hiện tại được tra cứu lại cho mỗi lần tra cứu module. Thứ ba, đường dẫn được dùng cho :data:`sys.path_importer_cache` và được trả về bởi
:meth:`importlib.machinery.PathFinder.find_spec` sẽ là thư mục làm việc hiện tại thực tế, không phải chuỗi rỗng.

Giao thức finder của mục nhập đường dẫn
---------------------------------------

Để hỗ trợ việc import các module và package đã được khởi tạo, đồng thời đóng góp các phần cho namespace package, các path entry finder phải triển khai phương thức :meth:`~importlib.abc.PathEntryFinder.find_spec`.

:meth:`~importlib.abc.PathEntryFinder.find_spec` nhận hai đối số: tên đầy đủ của module đang được import và module đích (tùy chọn). ``find_spec()`` trả về spec được điền đầy đủ cho module. Spec này luôn có "loader" được thiết lập (ngoại trừ một trường hợp).

Để cho cơ chế import biết rằng spec đại diện cho một namespace
:term:`portion`, path entry finder đặt ``submodule_search_locations`` thành một danh sách chứa phần đó.

.. versionchanged:: 3.4
   :meth:`~importlib.abc.PathEntryFinder.find_spec` replaced
   :meth:`!find_loader` and
   :meth:`!find_module`, both of which
   hiện đã bị deprecated, nhưng sẽ được sử dụng nếu ``find_spec()`` chưa được định nghĩa.

   Các path entry finder cũ có thể triển khai một trong hai phương thức đã bị deprecated này thay cho ``find_spec()``. Các phương thức này vẫn được tôn trọng để đảm bảo khả năng tương thích ngược. Tuy nhiên, nếu ``find_spec()`` được triển khai trên path entry finder, các phương thức cũ sẽ bị bỏ qua.

   :meth:`!find_loader` nhận một đối số, là tên đầy đủ của module đang được import. ``find_loader()`` trả về một tuple 2 phần, trong đó phần tử đầu tiên là loader và phần tử thứ hai là một namespace :term:`portion`.

   Để tương thích ngược với các triển khai khác của import protocol, nhiều path entry finder cũng hỗ trợ phương thức ``find_module()`` truyền thống, giống như meta path finder. Tuy nhiên, các phương thức ``find_module()`` của path entry finder không bao giờ được gọi với đối số ``path`` (chúng được kỳ vọng sẽ ghi nhận thông tin path thích hợp từ lần gọi ban đầu tới path hook).

   Phương thức ``find_module()`` trên các trình tìm mục đường dẫn đã lỗi thời vì không cho phép trình tìm mục đường dẫn đóng góp các phần vào các namespace package. Nếu cả ``find_loader()`` và ``find_module()`` đều tồn tại trên một trình tìm mục đường dẫn, hệ thống import sẽ luôn gọi ``find_loader()`` thay vì ``find_module()``.

.. versionchanged:: 3.10
    Các lệnh gọi đến :meth:`!find_module` và
    :meth:`!find_loader` của hệ thống import sẽ phát sinh :exc:`ImportWarning`.

.. versionchanged:: 3.12
    ``find_module()`` và ``find_loader()`` đã bị xóa.


Thay thế hệ thống import tiêu chuẩn
===================================

Cơ chế đáng tin cậy nhất để thay thế toàn bộ hệ thống import là xóa nội dung mặc định của :data:`sys.meta_path`, rồi thay thế hoàn toàn bằng một meta path hook tùy chỉnh.

Nếu chỉ thay đổi hành vi của các câu lệnh import mà không ảnh hưởng đến các API khác truy cập hệ thống import là đủ, thì việc thay thế hàm builtin :func:`__import__` có thể đáp ứng yêu cầu.

Để ngăn có chọn lọc việc import một số module từ một hook ở đầu meta path (thay vì vô hiệu hóa hoàn toàn hệ thống import chuẩn), chỉ cần raise :exc:`ModuleNotFoundError` trực tiếp từ
:meth:`~importlib.abc.MetaPathFinder.find_spec` thay vì trả về ``None``. Giá trị sau cho biết việc tìm kiếm trên meta path nên tiếp tục, còn việc raise một exception sẽ kết thúc ngay lập tức.

.. _relativeimports:

Import tương đối trong package
==============================

Import tương đối sử dụng các dấu chấm ở đầu. Một dấu chấm ở đầu biểu thị một import tương đối, bắt đầu từ package hiện tại. Hai hoặc nhiều dấu chấm ở đầu biểu thị một import tương đối đến package cha (hoặc các package cha) của package hiện tại, mỗi cấp tương ứng với một dấu chấm sau dấu đầu tiên. Ví dụ, với bố cục package sau đây::

    package/
        __init__.py
        subpackage1/
            __init__.py
            moduleX.py
            moduleY.py
        subpackage2/
            __init__.py
            moduleZ.py
        moduleA.py

Trong cả ``subpackage1/moduleX.py`` lẫn ``subpackage1/__init__.py``, các import tương đối sau đây đều hợp lệ::

    from .moduleY import spam
    from .moduleY import spam as ham
    from . import moduleY
    from ..subpackage1 import moduleY
    from ..subpackage2.moduleZ import eggs
    from ..moduleA import foo

Import tuyệt đối có thể sử dụng cú pháp ``import <>`` hoặc ``from <> import <>``, nhưng import tương đối chỉ có thể sử dụng dạng thứ hai; lý do là::

    import XXX.YYY.ZZZ

phải cung cấp ``XXX.YYY.ZZZ`` dưới dạng một biểu thức có thể sử dụng, nhưng .moduleY không phải là một biểu thức hợp lệ.


.. _import-dunder-main:

Các lưu ý đặc biệt đối với __main__
===================================

Mô-đun :mod:`__main__` là một trường hợp đặc biệt trong hệ thống import của Python. Như đã lưu ý :ref:`ở nơi khác <programs>`, mô-đun ``__main__`` được khởi tạo trực tiếp khi trình thông dịch khởi động, tương tự như :mod:`sys` và
:mod:`builtins`. Tuy nhiên, không giống hai mô-đun đó, nó không hoàn toàn đáp ứng tiêu chí của một mô-đun tích hợp sẵn. Điều này là do cách ``__main__`` được khởi tạo phụ thuộc vào các cờ và tùy chọn khác được sử dụng khi gọi trình thông dịch.

.. _main_spec:

__main__.__spec__
-----------------

Tùy thuộc vào cách :mod:`__main__` được khởi tạo, ``__main__.__spec__`` được thiết lập phù hợp hoặc thành ``None``.

Khi Python được khởi động với tùy chọn :option:`-m`, ``__spec__`` được thiết lập thành module spec của mô-đun hoặc package tương ứng. ``__spec__`` cũng được điền khi mô-đun ``__main__`` được tải trong quá trình thực thi một thư mục, zipfile hoặc mục nhập :data:`sys.path` khác.

Trong :ref:`các trường hợp còn lại <using-on-interface-options>`, ``__main__.__spec__`` được thiết lập thành ``None``, vì mã được sử dụng để điền
:mod:`__main__` không tương ứng trực tiếp với một module có thể import:

- dấu nhắc tương tác
- tùy chọn :option:`-c`
- chạy từ stdin
- chạy trực tiếp từ tệp mã nguồn hoặc bytecode

Lưu ý rằng ``__main__.__spec__`` luôn là ``None`` trong trường hợp cuối cùng, *ngay cả khi* về mặt kỹ thuật, tệp này có thể được import trực tiếp như một module. Sử dụng tùy chọn :option:`-m` nếu muốn có metadata module hợp lệ trong :mod:`__main__`.

Cũng lưu ý rằng ngay cả khi ``__main__`` tương ứng với một module có thể import và ``__main__.__spec__`` được thiết lập tương ứng, chúng vẫn được xem là các module *riêng biệt*. Nguyên nhân là các khối được bảo vệ bởi các kiểm tra ``if __name__ == "__main__":`` chỉ được thực thi khi module được dùng để điền vào namespace ``__main__``, chứ không được thực thi trong quá trình import thông thường.


Tài liệu tham khảo
==================

Cơ chế import đã phát triển đáng kể kể từ những ngày đầu của Python. Bản `đặc tả về các package <https://www.python.org/doc/essays/packages/>`_ ban đầu vẫn có thể đọc được, mặc dù một số chi tiết đã thay đổi kể từ khi tài liệu đó được soạn thảo.

Đặc tả ban đầu cho :data:`sys.meta_path` là :pep:`302`, sau đó được mở rộng trong :pep:`420`.

:pep:`420` đã giới thiệu :term:`namespace packages <namespace package>` cho Python 3.3. :pep:`420` cũng giới thiệu giao thức :meth:`!find_loader` như một lựa chọn thay thế cho :meth:`!find_module`.

:pep:`366` mô tả việc bổ sung thuộc tính ``__package__`` cho các import tương đối tường minh trong các module chính.

:pep:`328` đã giới thiệu các import tuyệt đối và tương đối tường minh, đồng thời ban đầu đề xuất ``__name__`` cho ngữ nghĩa mà :pep:`366` sau này sẽ đặc tả cho ``__package__``.

:pep:`338` định nghĩa việc thực thi các module dưới dạng script.

:pep:`451` bổ sung việc đóng gói trạng thái import theo từng module trong các đối tượng spec. Đồng thời, phần lớn trách nhiệm xử lý mã dựng sẵn của loader được chuyển trở lại cho cơ chế import. Những thay đổi này cho phép loại bỏ dần một số API trong hệ thống import, đồng thời bổ sung các phương thức mới cho finder và loader.

.. rubric:: Chú thích cuối trang

.. [#fnmo] Xem :class:`types.ModuleType`.

.. [#fnlo] Cài đặt importlib không sử dụng trực tiếp giá trị trả về. Thay vào đó, nó lấy đối tượng module bằng cách tra cứu tên module trong :data:`sys.modules`. Hệ quả gián tiếp của việc này là một module đã import có thể tự thay thế nó trong :data:`sys.modules`. Đây là hành vi phụ thuộc vào cách triển khai và không được đảm bảo sẽ hoạt động trong các bản triển khai Python khác.

.. _`specification for packages`: https://www.python.org/doc/essays/packages/
