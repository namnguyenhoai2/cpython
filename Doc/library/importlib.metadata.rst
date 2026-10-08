.. _using:

===========================================================
:mod:`!importlib.metadata` -- Truy cập metadata của package
===========================================================

.. module:: importlib.metadata
   :synopsis: Truy cập metadata của package

.. versionadded:: 3.8
.. versionchanged:: 3.10
   ``importlib.metadata`` không còn là thử nghiệm.

**Mã nguồn:** :source:`Lib/importlib/metadata/__init__.py`

``importlib.metadata`` là một thư viện cung cấp quyền truy cập vào metadata của một `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ đã cài đặt, chẳng hạn như các entry point hoặc tên cấp cao nhất của nó (`Import Package <https://packaging.python.org/en/latest/glossary/#term-Import-Package>`_\s, các module nếu có). Được xây dựng một phần dựa trên hệ thống import của Python, thư viện này cung cấp các API về entry point và metadata trước đây được cung cấp bởi package ``pkg_resources`` đã bị loại bỏ. Cùng với
:mod:`importlib.resources`, thư viện này thay thế ``pkg_resources``.

``importlib.metadata`` hoạt động trên các *distribution packages* của bên thứ ba được cài đặt vào thư mục ``site-packages`` của Python bằng các công cụ như
:pypi:`pip`. Cụ thể, nó hoạt động với các distribution có thư mục ``dist-info`` hoặc ``egg-info`` có thể phát hiện được, cùng metadata được định nghĩa bởi `các đặc tả Core metadata <https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata>`_.

.. important::

   Các distribution này *không* nhất thiết tương đương hoặc tương ứng 1:1 với tên *import package* cấp cao nhất có thể được import bên trong mã Python. Một *distribution package* có thể chứa nhiều *import package* (và các module đơn lẻ), còn một *import package* cấp cao nhất có thể ánh xạ tới nhiều *distribution package* nếu đó là namespace package. Bạn có thể sử dụng :ref:`packages_distributions() <package-distributions>` để lấy ánh xạ giữa chúng.

Theo mặc định, metadata của distribution có thể nằm trên hệ thống tệp hoặc trong các kho lưu trữ zip trên
:data:`sys.path`. Thông qua một cơ chế mở rộng, metadata có thể nằm ở hầu như bất kỳ đâu.


.. seealso::

   https://importlib-metadata.readthedocs.io/
      Tài liệu dành cho ``importlib_metadata``, cung cấp bản backport của ``importlib.metadata``. Tài liệu này bao gồm `tài liệu tham chiếu API <https://importlib-metadata.readthedocs.io/en/latest/api.html>`__ cho các lớp và hàm của module này, cũng như `hướng dẫn chuyển đổi <https://importlib-metadata.readthedocs.io/en/latest/migration.html>`__ dành cho những người dùng hiện tại của ``pkg_resources``.


Tổng quan
=========

Giả sử bạn muốn lấy chuỗi phiên bản của một `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ mà bạn đã cài đặt bằng ``pip``. Trước tiên, chúng ta tạo một môi trường ảo và cài đặt một gói vào đó:

.. code-block:: shell-session

    $ python -m venv example
    $ source example/bin/activate
    (example) $ python -m pip install wheel

Bạn có thể lấy chuỗi phiên bản của ``wheel`` bằng cách chạy lệnh sau:

.. code-block:: pycon

    (example) $ python
    >>> from importlib.metadata import version  # doctest: +SKIP
    >>> version('wheel')  # doctest: +SKIP
    '0.32.3'

Bạn cũng có thể lấy một tập hợp các entry point có thể được chọn theo các thuộc tính của EntryPoint (thường là 'group' hoặc 'name'), chẳng hạn như ``console_scripts``, ``distutils.commands`` và các entry point khác. Mỗi group chứa một tập hợp các đối tượng :ref:`EntryPoint <entry-points>`.

Bạn có thể lấy :ref:`siêu dữ liệu của một bản phân phối <metadata>`::

    >>> from importlib.metadata import metadata  # doctest: +SKIP
    >>> list(metadata('wheel'))  # doctest: +SKIP
    ['Metadata-Version', 'Name', 'Version', 'Summary', 'Home-page', 'Author', 'Author-email', 'Maintainer', 'Maintainer-email', 'License', 'Project-URL', 'Project-URL', 'Project-URL', 'Keywords', 'Platform', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Classifier', 'Requires-Python', 'Provides-Extra', 'Requires-Dist', 'Requires-Dist']

Bạn cũng có thể lấy số phiên bản của một :ref:`bản phân phối <version>`, liệt kê các
:ref:`tệp cấu thành <files>`, và lấy danh sách các thành phần của bản phân phối
:ref:`requirements`.


.. exception:: PackageNotFoundError

   Lớp con của :class:`ModuleNotFoundError` được một số hàm trong mô-đun này đưa ra khi truy vấn một gói phân phối chưa được cài đặt trong môi trường Python hiện tại.


API hàm
=======

Gói này cung cấp các chức năng sau thông qua API công khai.


.. _entry-points:

Entry points
------------

.. function:: entry_points(**select_params)

   Trả về một thực thể :class:`EntryPoints` mô tả các entry point cho môi trường hiện tại. Mọi tham số từ khóa được cung cấp đều được truyền cho
   phương thức :meth:`!select` để so sánh với các thuộc tính của từng định nghĩa entry point.

   Lưu ý: hiện không thể truy vấn entry point dựa trên thuộc tính :attr:`!EntryPoint.dist` của chúng (vì các instance :class:`!Distribution` khác nhau hiện không so sánh bằng nhau, ngay cả khi chúng có cùng các thuộc tính)

.. class:: EntryPoints

   Thông tin chi tiết về một tập hợp entry point đã cài đặt.

   Cũng cung cấp thuộc tính ``.groups`` báo cáo tất cả các nhóm entry point được xác định, và thuộc tính ``.names`` báo cáo tất cả tên entry point được xác định.

.. class:: EntryPoint

   Thông tin chi tiết về một entry point đã cài đặt.

   Mỗi instance :class:`!EntryPoint` có các thuộc tính ``.name``, ``.group`` và ``.value``, cùng phương thức ``.load()`` để phân giải giá trị. Ngoài ra còn có các thuộc tính ``.module``, ``.attr`` và ``.extras`` để lấy các thành phần của thuộc tính ``.value``, cùng ``.dist`` để lấy thông tin về distribution package cung cấp entry point.

Truy vấn tất cả entry point::

    >>> eps = entry_points()  # doctest: +SKIP

Hàm :func:`!entry_points` trả về một đối tượng :class:`!EntryPoints`, một tập hợp gồm tất cả các đối tượng :class:`!EntryPoint` có các thuộc tính ``names`` và ``groups`` để thuận tiện::

    >>> sorted(eps.groups)  # doctest: +SKIP
    ['console_scripts', 'distutils.commands', 'distutils.setup_keywords', 'egg_info.writers', 'setuptools.installation']

:class:`!EntryPoints` có một phương thức :meth:`!select` để chọn các entry point khớp với những thuộc tính cụ thể. Chọn các entry point trong nhóm ``console_scripts``::

    >>> scripts = eps.select(group='console_scripts')  # doctest: +SKIP

Tương đương, vì :func:`!entry_points` truyền các đối số từ khóa cho select::

    >>> scripts = entry_points(group='console_scripts')  # doctest: +SKIP

Chọn một script cụ thể có tên "wheel" (có trong dự án wheel)::

    >>> 'wheel' in scripts.names  # doctest: +SKIP
    True
    >>> wheel = scripts['wheel']  # doctest: +SKIP

Tương đương, hãy truy vấn điểm vào đó trong quá trình chọn::

    >>> (wheel,) = entry_points(group='console_scripts', name='wheel')  # doctest: +SKIP
    >>> (wheel,) = entry_points().select(group='console_scripts', name='wheel')  # doctest: +SKIP

Kiểm tra điểm vào đã được phân giải::

    >>> wheel  # doctest: +SKIP
    EntryPoint(name='wheel', value='wheel.cli:main', group='console_scripts')
    >>> wheel.module  # doctest: +SKIP
    'wheel.cli'
    >>> wheel.attr  # doctest: +SKIP
    'main'
    >>> wheel.extras  # doctest: +SKIP
    []
    >>> main = wheel.load()  # doctest: +SKIP
    >>> main  # doctest: +SKIP
    <function main at 0x103528488>

``group`` và ``name`` là các giá trị tùy ý do tác giả package định nghĩa và thông thường client sẽ muốn resolve tất cả entry points cho một nhóm cụ thể. Đọc `tài liệu setuptools <https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`_ để biết thêm thông tin về entry points, cách định nghĩa và cách sử dụng chúng.

.. versionchanged:: 3.12
   Các entry point "selectable" được giới thiệu trong ``importlib_metadata`` 3.6 và Python 3.10. Trước những thay đổi đó, ``entry_points`` không chấp nhận tham số nào và luôn trả về một từ điển các entry point, được lập chỉ mục theo group. Với ``importlib_metadata`` 5.0 và Python 3.12, ``entry_points`` luôn trả về một đối tượng ``EntryPoints``. Xem
   :pypi:`backports.entry_points_selectable` để biết các tùy chọn tương thích.

.. versionchanged:: 3.13
   Các đối tượng ``EntryPoint`` không còn cung cấp giao diện giống tuple (:meth:`~object.__getitem__`).

.. _metadata:

Siêu dữ liệu bản phân phối
--------------------------

.. function:: metadata(distribution_name)

   Trả về siêu dữ liệu bản phân phối tương ứng với gói bản phân phối được đặt tên dưới dạng một thực thể :class:`PackageMetadata`.

   Phát sinh :exc:`PackageNotFoundError` nếu gói bản phân phối được đặt tên chưa được cài đặt trong môi trường Python hiện tại.

.. class:: PackageMetadata

   Một triển khai cụ thể của giao thức `PackageMetadata protocol <https://importlib-metadata.readthedocs.io/en/latest/api.html#importlib_metadata.PackageMetadata>`_.

   Ngoài việc cung cấp các phương thức và thuộc tính giao thức đã định nghĩa, sử dụng phép lập chỉ mục trên instance tương đương với việc gọi phương thức :meth:`!get`.

Mỗi `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ đều bao gồm một số metadata mà bạn có thể trích xuất bằng hàm :func:`!metadata`::

    >>> wheel_metadata = metadata('wheel')  # doctest: +SKIP

Các khóa của cấu trúc dữ liệu được trả về là tên của các từ khóa metadata, còn các giá trị được trả về ở dạng chưa phân tích cú pháp từ metadata của distribution::

    >>> wheel_metadata['Requires-Python']  # doctest: +SKIP
    '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'

:class:`PackageMetadata` cũng cung cấp một thuộc tính :attr:`!json` trả về toàn bộ metadata ở dạng tương thích với JSON theo :PEP:`566`::

    >>> wheel_metadata.json['requires_python']
    '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'

Toàn bộ metadata hiện có không được mô tả ở đây. Hãy xem `Core metadata specification <https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata>`_ của PyPA để biết thêm chi tiết.

.. versionchanged:: 3.10
   ``Description`` hiện được đưa vào metadata khi được trình bày qua payload. Các ký tự tiếp tục dòng đã được loại bỏ.

   Thuộc tính ``json`` đã được thêm vào.


.. _version:

Các phiên bản distribution
--------------------------

.. function:: version(distribution_name)

   Trả về `version <https://packaging.python.org/en/latest/specifications/core-metadata/#version>`__ của distribution package đã cài đặt có tên được chỉ định.

   Phát sinh :exc:`PackageNotFoundError` nếu distribution package có tên được chỉ định chưa được cài đặt trong Python environment hiện tại.

Hàm :func:`!version` là cách nhanh nhất để lấy số phiên bản của `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ dưới dạng chuỗi::

    >>> version('wheel')  # doctest: +SKIP
    '0.32.3'


.. _files:

Các tệp của gói phân phối
-------------------------

.. function:: files(distribution_name)

   Trả về toàn bộ tập hợp tệp có trong gói phân phối được chỉ định.

   Phát sinh :exc:`PackageNotFoundError` nếu gói phân phối được chỉ định chưa được cài đặt trong môi trường Python hiện tại.

   Trả về :const:`None` nếu tìm thấy gói phân phối nhưng thiếu các bản ghi trong cơ sở dữ liệu cài đặt dùng để báo cáo những tệp liên kết với gói phân phối.

.. class:: PackagePath

    Một đối tượng dẫn xuất từ :class:`pathlib.PurePath` với các thuộc tính ``dist``, ``size`` và ``hash`` bổ sung, tương ứng với siêu dữ liệu cài đặt của gói phân phối cho tệp đó.

Hàm :func:`!files` nhận tên của `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ và trả về tất cả các tệp được bản phân phối này cài đặt. Mỗi tệp được báo cáo dưới dạng một thực thể :class:`PackagePath`. Ví dụ::

    >>> util = [p for p in files('wheel') if 'util.py' in str(p)][0]  # doctest: +SKIP
    >>> util  # doctest: +SKIP
    PackagePath('wheel/util.py')
    >>> util.size  # doctest: +SKIP
    859
    >>> util.dist  # doctest: +SKIP
    <importlib.metadata._hooks.PathDistribution object at 0x101e0cef0>
    >>> util.hash  # doctest: +SKIP
    <FileHash mode: sha256 value: bYkw5oMccfazVCoYQwKkkemoVyMAFoR34mmKBx8R1NI>

Sau khi có tệp, bạn cũng có thể đọc nội dung của tệp::

    >>> print(util.read_text())  # doctest: +SKIP
    import base64
    import sys
    ...
    def as_bytes(s):
        if isinstance(s, text_type):
            return s.encode('utf-8')
        return s

Bạn cũng có thể sử dụng phương thức :meth:`!locate` để lấy đường dẫn tuyệt đối đến tệp::

    >>> util.locate()  # doctest: +SKIP
    PosixPath('/home/gustav/example/lib/site-packages/wheel/util.py')

Trong trường hợp tệp metadata liệt kê các tệp (``RECORD`` hoặc ``SOURCES.txt``) bị thiếu, :func:`!files` sẽ trả về :const:`None`. Người gọi có thể muốn bọc các lệnh gọi đến
:func:`!files` trong `always_iterable <https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.always_iterable>`_ hoặc bằng cách khác kiểm tra điều kiện này nếu không biết chắc bản phân phối đích có metadata hay không.

.. _requirements:

Các yêu cầu của bản phân phối
-----------------------------

.. function:: requires(distribution_name)

   Trả về các bộ chỉ định dependency đã khai báo cho gói distribution có tên đã cho.

   Gây ra :exc:`PackageNotFoundError` nếu gói distribution có tên đã cho chưa được cài đặt trong môi trường Python hiện tại.

Để lấy toàn bộ tập hợp các yêu cầu cho một `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_, hãy sử dụng hàm :func:`!requires`::

    >>> requires('wheel')  # doctest: +SKIP
    ["pytest (>=3.0.0) ; extra == 'test'", "pytest-cov ; extra == 'test'"]


.. _package-distributions:
.. _import-distribution-package-mapping:

Ánh xạ import tới các gói phân phối
-----------------------------------

.. function:: packages_distributions()

   Trả về một ánh xạ từ tên module cấp cao nhất và tên import package được tìm thấy thông qua :data:`sys.meta_path` tới tên của các gói phân phối (nếu có) cung cấp những tệp tương ứng.

   Để hỗ trợ các namespace package (có thể có thành viên do nhiều gói phân phối cung cấp), mỗi tên import cấp cao nhất được ánh xạ tới một danh sách tên distribution thay vì ánh xạ trực tiếp tới một tên duy nhất.

Một phương thức tiện ích để phân giải tên `Gói phân phối <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ (hoặc các tên, trong trường hợp là namespace package) cung cấp từng module Python cấp cao nhất có thể import hoặc `Gói import <https://packaging.python.org/en/latest/glossary/#term-Import-Package>`_::

    >>> packages_distributions()
    {'importlib_metadata': ['importlib-metadata'], 'yaml': ['PyYAML'], 'jaraco': ['jaraco.classes', 'jaraco.functools'], ...}

Một số bản cài đặt editable, `không cung cấp tên cấp cao nhất <https://github.com/pypa/packaging-problems/issues/609>`_, vì vậy hàm này không đáng tin cậy với những bản cài đặt như vậy.

.. versionadded:: 3.10

.. _distributions:

Các bản phân phối
=================

.. function:: distribution(distribution_name)

   Trả về một instance :class:`Distribution` mô tả package distribution được chỉ định.

   Phát sinh :exc:`PackageNotFoundError` nếu package distribution được chỉ định chưa được cài đặt trong môi trường Python hiện tại.

.. class:: Distribution

   Thông tin chi tiết về package distribution đã cài đặt.

   Lưu ý: các instance :class:`!Distribution` khác nhau hiện không được so sánh là bằng nhau, ngay cả khi chúng liên quan đến cùng một distribution đã cài đặt và do đó có cùng các thuộc tính.

Mặc dù API cấp module được mô tả ở trên là cách sử dụng phổ biến và thuận tiện nhất, bạn có thể lấy toàn bộ thông tin đó từ class :class:`!Distribution`.
:class:`!Distribution` là một đối tượng trừu tượng đại diện cho metadata của một `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ Python. Bạn có thể lấy instance của subclass :class:`!Distribution` cụ thể cho một package distribution đã cài đặt bằng cách gọi hàm :func:`distribution`::

    >>> from importlib.metadata import distribution  # doctest: +SKIP
    >>> dist = distribution('wheel')  # doctest: +SKIP
    >>> type(dist)  # doctest: +SKIP
    <class 'importlib.metadata.PathDistribution'>

Do đó, một cách khác để lấy số phiên bản là thông qua
:class:`!Distribution` instance::

    >>> dist.version  # doctest: +SKIP
    '0.32.3'

Có đủ loại siêu dữ liệu bổ sung trên :class:`!Distribution` instance::

    >>> dist.metadata['Requires-Python']  # doctest: +SKIP
    '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'
    >>> dist.metadata['License']  # doctest: +SKIP
    'MIT'

Đối với các package có thể chỉnh sửa, một thuộc tính ``origin`` có thể cung cấp metadata :pep:`610`::

    >>> dist.origin.url
    'file:///path/to/wheel-0.32.3.editable-py3-none-any.whl'

Bộ metadata đầy đủ hiện có không được mô tả ở đây. Xem `Đặc tả metadata cốt lõi <https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata>`_ của PyPA để biết thêm chi tiết.

.. versionadded:: 3.13
   Thuộc tính ``.origin`` đã được thêm.

Khám phá bản phân phối
======================

Theo mặc định, package này tích hợp sẵn khả năng khám phá metadata cho hệ thống tệp và `Gói phân phối <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_\s tệp zip. Trình tìm metadata này mặc định tìm kiếm trong ``sys.path``, nhưng cách diễn giải các giá trị đó hơi khác so với các cơ chế import khác. Cụ thể:

- ``importlib.metadata`` không tuân theo các đối tượng :class:`bytes` trên ``sys.path``.
- ``importlib.metadata`` cũng sẽ tình cờ tôn trọng các đối tượng :py:class:`pathlib.Path` trên ``sys.path``, mặc dù những giá trị như vậy sẽ bị bỏ qua khi import.


Triển khai Providers tùy chỉnh
==============================

``importlib.metadata`` cung cấp hai API surface, một dành cho *consumers* và một dành cho *providers*. Hầu hết người dùng là consumers, sử dụng metadata do các package cung cấp. Tuy nhiên, có những trường hợp sử dụng khác mà người dùng muốn cung cấp metadata thông qua một cơ chế khác, chẳng hạn như đi kèm với một importer tùy chỉnh. Trường hợp sử dụng như vậy cần đến một *custom provider*.

Vì metadata của `Distribution Package <https://packaging.python.org/en/latest/glossary/#term-Distribution-Package>`_ không khả dụng trực tiếp thông qua các phép :data:`sys.path` tìm kiếm hoặc các package loader, metadata của một distribution được tìm thấy thông qua các :ref:`finder <finders-and-loaders>` của hệ thống import. Để tìm metadata của một distribution package, ``importlib.metadata`` truy vấn danh sách các :term:`meta path finder <meta path finder>` trên
:data:`sys.meta_path`.

Phần triển khai có các hook được tích hợp vào ``PathFinder``, cung cấp metadata cho các distribution package được tìm thấy trên hệ thống tệp.

Lớp trừu tượng :py:class:`importlib.abc.MetaPathFinder` định nghĩa interface mà các finder của hệ thống import của Python phải tuân theo. ``importlib.metadata`` mở rộng protocol này bằng cách tìm một ``find_distributions`` callable tùy chọn trên các finder từ
:data:`sys.meta_path` và cung cấp interface mở rộng này dưới dạng lớp cơ sở trừu tượng ``DistributionFinder``, trong đó định nghĩa phương thức trừu tượng này::

    @abc.abstractmethod
    def find_distributions(context=DistributionFinder.Context()) -> Iterable[Distribution]:
        """Return an iterable of all Distribution instances capable of
        loading the metadata for packages for the indicated ``context``.
        """

Đối tượng ``DistributionFinder.Context`` cung cấp các thuộc tính ``.path`` và ``.name``, cho biết đường dẫn cần tìm kiếm và tên cần khớp, đồng thời có thể cung cấp ngữ cảnh liên quan khác mà bên sử dụng cần.

Trên thực tế, để hỗ trợ việc tìm metadata của distribution package ở những vị trí khác ngoài hệ thống tệp, hãy phân lớp ``Distribution`` và triển khai các phương thức abstract. Sau đó, từ một custom finder, hãy trả về các thực thể của ``Distribution`` dẫn xuất này trong phương thức ``find_distributions()``.

Ví dụ
-----

Hãy tưởng tượng một custom finder tải các Python module từ cơ sở dữ liệu::

    class DatabaseImporter(importlib.abc.MetaPathFinder):
        def __init__(self, db):
            self.db = db

        def find_spec(self, fullname, target=None) -> ModuleSpec:
            return self.db.spec_from_name(fullname)

    sys.meta_path.append(DatabaseImporter(connect_db(...)))

Khi đó, importer này có lẽ đã cung cấp các module có thể import từ cơ sở dữ liệu, nhưng chưa cung cấp metadata hoặc entry point nào. Để custom importer này cung cấp metadata, nó cũng cần triển khai ``DistributionFinder``::

    from importlib.metadata import DistributionFinder

    class DatabaseImporter(DistributionFinder):
        ...

        def find_distributions(self, context=DistributionFinder.Context()):
            query = dict(name=context.name) if context.name else {}
            for dist_record in self.db.query_distributions(query):
                yield DatabaseDistribution(dist_record)

Theo cách này, ``query_distributions`` sẽ trả về các bản ghi cho từng distribution do cơ sở dữ liệu cung cấp và khớp với truy vấn. Ví dụ, nếu ``requests-1.0`` có trong cơ sở dữ liệu, ``find_distributions`` sẽ tạo ra một ``DatabaseDistribution`` cho ``Context(name='requests')`` hoặc ``Context(name=None)``.

Để đơn giản, ví dụ này bỏ qua ``context.path``\. Thuộc tính ``path`` mặc định là ``sys.path`` và là tập hợp các đường dẫn import được xem xét trong quá trình tìm kiếm. Một ``DatabaseImporter`` về lý thuyết có thể hoạt động mà không cần quan tâm đến đường dẫn tìm kiếm. Giả sử importer không phân vùng, thì "path" sẽ không liên quan. Để minh họa mục đích của ``path``, ví dụ này cần minh họa một ``DatabaseImporter`` phức tạp hơn, với hành vi thay đổi tùy theo ``sys.path``/``PYTHONPATH``. Trong trường hợp đó, ``find_distributions`` phải tuân theo ``context.path`` và chỉ tạo ra các ``Distribution``\ s phù hợp với đường dẫn đó.

``DatabaseDistribution``, khi đó, sẽ có dạng như sau::

    class DatabaseDistribution(importlib.metadata.Distribution):
        def __init__(self, record):
            self.record = record

        def read_text(self, filename):
            """
            Read a file like "METADATA" for the current distribution.
            """
            if filename == "METADATA":
                return f"""Name: {self.record.name}
    Version: {self.record.version}
    """
            if filename == "entry_points.txt":
                return "\n".join(
                  f"""[{ep.group}]\n{ep.name}={ep.value}"""
                  for ep in self.record.entry_points)

        def locate_file(self, path):
            raise RuntimeError("This distribution has no file system")

Bản triển khai cơ bản này sẽ cung cấp metadata và các entry point cho những package được ``DatabaseImporter`` cung cấp, với điều kiện ``record`` cung cấp các thuộc tính ``.name``, ``.version`` và ``.entry_points`` phù hợp.

``DatabaseDistribution`` cũng có thể cung cấp các tệp metadata khác, chẳng hạn như ``RECORD`` (bắt buộc đối với ``Distribution.files``) hoặc ghi đè triển khai của ``Distribution.files``. Hãy xem mã nguồn để có thêm ý tưởng.

.. _`Distribution Package`: https://packaging.python.org/en/latest/glossary/#term-Distribution-Package
.. _`Import Package`: https://packaging.python.org/en/latest/glossary/#term-Import-Package
.. _`Core metadata specifications`: https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata
.. _`the setuptools docs`: https://setuptools.pypa.io/en/latest/userguide/entry_point.html
.. _`PackageMetadata protocol`: https://importlib-metadata.readthedocs.io/en/latest/api.html#importlib_metadata.PackageMetadata
.. _`Core metadata specification`: https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata
.. _`always_iterable`: https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.always_iterable
.. _`do not supply top-level names`: https://github.com/pypa/packaging-problems/issues/609
