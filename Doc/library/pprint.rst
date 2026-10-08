:mod:`!pprint` --- Bộ in dữ liệu đẹp
====================================

.. module:: pprint
   :synopsis: Bộ in dữ liệu đẹp.

.. moduleauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/pprint.py`

--------------

Mô-đun :mod:`!pprint` cung cấp khả năng "in đẹp" các cấu trúc dữ liệu Python tùy ý theo định dạng có thể dùng làm đầu vào cho trình thông dịch. Nếu các cấu trúc được định dạng bao gồm những đối tượng không phải là kiểu Python cơ bản, biểu diễn đó có thể không nạp được. Điều này có thể xảy ra nếu bao gồm các đối tượng như tệp, socket hoặc lớp, cũng như nhiều đối tượng khác không thể biểu diễn dưới dạng literal Python.

Biểu diễn đã định dạng giữ các đối tượng trên một dòng nếu có thể, và ngắt chúng thành nhiều dòng nếu không vừa với độ rộng cho phép. Độ rộng này có thể điều chỉnh bằng tham số *width*, mặc định là 80 ký tự.

.. versionchanged:: 3.9
   Đã bổ sung hỗ trợ in đẹp :class:`types.SimpleNamespace`.

.. versionchanged:: 3.10
   Đã bổ sung hỗ trợ in đẹp :class:`dataclasses.dataclass`.

.. _pprint-functions:

Hàm
---

.. function:: pp(object, stream=None, indent=1, width=80, depth=None, *, \
                     compact=False, sort_dicts=False, underscore_numbers=False)

   In ra biểu diễn đã được định dạng của *object*, theo sau là một ký tự xuống dòng. Có thể sử dụng hàm này trong trình thông dịch tương tác thay cho hàm :func:`print` để kiểm tra các giá trị. Mẹo: bạn có thể gán lại ``print = pprint.pp`` để sử dụng trong một phạm vi.

   :param object:Đối tượng cần in.

   :param stream:Một đối tượng giống tệp mà đầu ra sẽ được ghi vào bằng cách gọi phương thức :meth:`!write`. Nếu là ``None`` (mặc định), :data:`sys.stdout` sẽ được sử dụng.
   :type stream: :term:`file-like object` | None

   :param int indent:Mức thụt lề được thêm vào cho mỗi cấp độ lồng nhau.

   :param int width:Số ký tự tối đa mong muốn trên mỗi dòng trong đầu ra. Nếu không thể định dạng một cấu trúc trong giới hạn độ rộng, hệ thống sẽ cố gắng hết sức.

   :param depth:Số cấp độ lồng nhau có thể được in. Nếu cấu trúc dữ liệu đang được in quá sâu, cấp độ tiếp theo bên trong sẽ được thay thế bằng ``...``. Nếu ``None`` (mặc định), độ sâu của các đối tượng được định dạng không bị giới hạn.
   :type depth: int | None

   :param bool compact:Kiểm soát cách định dạng các :term:`chuỗi <sequence>` dài. Nếu ``False`` (mặc định), mỗi mục trong một chuỗi sẽ được định dạng trên một dòng riêng; nếu không, mỗi dòng đầu ra sẽ định dạng nhiều mục nhất có thể vừa trong *độ rộng*.

   :param bool sort_dicts:Nếu ``True``, các dictionary sẽ được định dạng với các khóa đã sắp xếp; nếu không, chúng sẽ được hiển thị theo thứ tự chèn (mặc định).

   :param bool underscore_numbers:Nếu ``True``, các số nguyên sẽ được định dạng với ký tự ``_`` làm dấu phân cách hàng nghìn; nếu không, dấu gạch dưới sẽ không được hiển thị (mặc định).

   >>> import pprint
   >>> stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
   >>> stuff.insert(0, stuff)
   >>> pprint.pp(stuff)
   [<Recursion on list with id=...>,
    'spam',
    'eggs',
    'lumberjack',
    'knights',
    'ni']

   .. versionadded:: 3.8


.. function:: pprint(object, stream=None, indent=1, width=80, depth=None, *, \
                     compact=False, sort_dicts=True, underscore_numbers=False)

   Bí danh cho :func:`~pprint.pp` với *sort_dicts* được đặt thành ``True`` theo mặc định, tùy chọn này sẽ tự động sắp xếp các khóa của dictionary; bạn có thể muốn sử dụng :func:`~pprint.pp` thay vào đó, trong đó tùy chọn này là ``False`` theo mặc định.


.. function:: pformat(object, indent=1, width=80, depth=None, *, \
                      compact=False, sort_dicts=True, underscore_numbers=False)

   Trả về biểu diễn đã được định dạng của *object* dưới dạng chuỗi. *indent*, *width*, *depth*, *compact*, *sort_dicts* và *underscore_numbers* được truyền cho hàm khởi tạo :class:`PrettyPrinter` dưới dạng các tham số định dạng; ý nghĩa của chúng được mô tả trong tài liệu ở trên.


.. function:: isreadable(object)

   .. index:: pair: built-in function; eval

   Xác định xem biểu diễn đã được định dạng của *object* có "dễ đọc" hay không, hoặc có thể được dùng để tái tạo giá trị bằng :func:`eval`. Hàm này luôn trả về ``False`` đối với các object đệ quy.

      >>> pprint.isreadable(stuff)
      False


.. function:: isrecursive(object)

   Xác định xem *object* có yêu cầu biểu diễn đệ quy hay không. Hàm này chịu cùng các giới hạn như được nêu trong :func:`saferepr` bên dưới và có thể phát sinh một
   :exc:`RecursionError` nếu không phát hiện được object đệ quy.


.. function:: saferepr(object)

   Trả về biểu diễn chuỗi của *object*, được bảo vệ khỏi đệ quy trong một số cấu trúc dữ liệu phổ biến, cụ thể là các instance của :class:`dict`, :class:`list` và :class:`tuple` hoặc các lớp con mà ``__repr__`` của chúng chưa được ghi đè. Nếu biểu diễn của object hiển thị một mục nhập đệ quy, tham chiếu đệ quy sẽ được biểu diễn dưới dạng ``<Recursion on typename with id=number>``. Biểu diễn này không được định dạng theo cách nào khác.

   >>> pprint.saferepr(stuff)
   "[<Recursion on list with id=...>, 'spam', 'eggs', 'lumberjack', 'knights', 'ni']"

.. _prettyprinter-objects:

Các đối tượng PrettyPrinter
---------------------------

.. index:: single: ...; placeholder

.. class:: PrettyPrinter(indent=1, width=80, depth=None, stream=None, *, \
                         compact=False, sort_dicts=True, underscore_numbers=False)

   Tạo một thực thể :class:`PrettyPrinter`.

   Các đối số có cùng ý nghĩa như đối với :func:`~pprint.pp`. Lưu ý rằng chúng có thứ tự khác nhau và *sort_dicts* mặc định là ``True``.

   >>> import pprint
   >>> stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
   >>> stuff.insert(0, stuff[:])
   >>> pp = pprint.PrettyPrinter(indent=4)
   >>> pp.pprint(stuff)
   [   ['spam', 'eggs', 'lumberjack', 'knights', 'ni'],
       'spam',
       'eggs',
       'lumberjack',
       'knights',
       'ni']
   >>> pp = pprint.PrettyPrinter(width=41, compact=True)
   >>> pp.pprint(stuff)
   [['spam', 'eggs', 'lumberjack',
     'knights', 'ni'],
    'spam', 'eggs', 'lumberjack', 'knights',
    'ni']
   >>> tup = ('spam', ('eggs', ('lumberjack', ('knights', ('ni', ('dead',
   ... ('parrot', ('fresh fruit',))))))))
   >>> pp = pprint.PrettyPrinter(depth=6)
   >>> pp.pprint(tup)
   ('spam', ('eggs', ('lumberjack', ('knights', ('ni', ('dead', (...)))))))


   .. versionchanged:: 3.4
      Đã thêm tham số *compact*.

   .. versionchanged:: 3.8
      Đã thêm tham số *sort_dicts*.

   .. versionchanged:: 3.10
      Đã thêm tham số *underscore_numbers*.

   .. versionchanged:: 3.11
      Không còn cố gắng ghi vào :data:`!sys.stdout` nếu nó là ``None``.


Các instance của :class:`PrettyPrinter` có các phương thức sau:


.. method:: PrettyPrinter.pformat(object)

   Trả về biểu diễn đã được định dạng của *object*. Phương thức này tính đến các tùy chọn được truyền cho hàm khởi tạo :class:`PrettyPrinter`.


.. method:: PrettyPrinter.pprint(object)

   In biểu diễn đã được định dạng của *object* trên stream đã cấu hình, kèm theo một dòng mới.

Các phương thức sau cung cấp phần triển khai cho những hàm tương ứng có cùng tên. Việc sử dụng các phương thức này trên một instance hiệu quả hơn một chút vì không cần tạo các đối tượng :class:`PrettyPrinter` mới.


.. method:: PrettyPrinter.isreadable(object)

   .. index:: pair: built-in function; eval

   Xác định xem biểu diễn đã được định dạng của đối tượng có "thể đọc được" hay không, hoặc có thể được dùng để tái tạo giá trị bằng :func:`eval`. Lưu ý rằng phương thức này trả về ``False`` đối với các đối tượng đệ quy. Nếu tham số *depth* của
   :class:`PrettyPrinter` được thiết lập và đối tượng sâu hơn mức cho phép, phương thức này trả về ``False``.


.. method:: PrettyPrinter.isrecursive(object)

   Xác định xem đối tượng có cần biểu diễn đệ quy hay không.

Phương thức này được cung cấp dưới dạng một hook để cho phép các lớp con sửa đổi cách đối tượng được chuyển đổi thành chuỗi. Cài đặt mặc định sử dụng phần nội bộ của
:func:`saferepr` implementation.


.. method:: PrettyPrinter.format(object, context, maxlevels, level)

   Trả về ba giá trị: phiên bản được định dạng của *object* dưới dạng chuỗi, một cờ cho biết kết quả có dễ đọc hay không và một cờ cho biết có phát hiện đệ quy hay không. Đối số thứ nhất là đối tượng cần trình bày. Đối số thứ hai là một từ điển chứa :func:`id` của các đối tượng nằm trong ngữ cảnh trình bày hiện tại (các container trực tiếp và gián tiếp của *object* đang ảnh hưởng đến việc trình bày) làm các khóa; nếu cần trình bày một đối tượng đã được biểu diễn trong *context*, giá trị trả về thứ ba phải là ``True``. Các lời gọi đệ quy đến phương thức :meth:`.format` phải thêm các mục bổ sung cho các container vào từ điển này. Đối số thứ ba, *maxlevels*, chỉ định giới hạn đệ quy được yêu cầu; giá trị này sẽ là ``0`` nếu không có giới hạn nào được yêu cầu. Đối số này phải được truyền nguyên vẹn cho các lời gọi đệ quy. Đối số thứ tư, *level*, chỉ định cấp hiện tại; các lời gọi đệ quy phải được truyền một giá trị nhỏ hơn cấp của lời gọi hiện tại.


.. _pprint-example:

Ví dụ
-----

Để minh họa một số cách sử dụng hàm :func:`~pprint.pp` và các tham số của hàm, hãy lấy thông tin về một project từ `PyPI <https://pypi.org>`_::

   >>> import json
   >>> import pprint
   >>> from urllib.request import urlopen
   >>> with urlopen('https://pypi.org/pypi/sampleproject/1.2.0/json') as resp:
   ...     project_info = json.load(resp)['info']

Ở dạng cơ bản, :func:`~pprint.pp` hiển thị toàn bộ đối tượng::

   >>> pprint.pp(project_info)
   {'author': 'The Python Packaging Authority',
    'author_email': 'pypa-dev@googlegroups.com',
    'bugtrack_url': None,
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.2',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Topic :: Software Development :: Build Tools'],
    'description': 'A sample Python project\n'
                   '=======================\n'
                   '\n'
                   'This is the description file for the project.\n'
                   '\n'
                   'The file should use UTF-8 encoding and be written using '
                   'ReStructured Text. It\n'
                   'will be used to generate the project webpage on PyPI, and '
                   'should be written for\n'
                   'that purpose.\n'
                   '\n'
                   'Typical contents for this file would include an overview of '
                   'the project, basic\n'
                   'usage examples, etc. Generally, including the project '
                   'changelog in here is not\n'
                   'a good idea, although a simple "What\'s New" section for the '
                   'most recent version\n'
                   'may be appropriate.',
    'description_content_type': None,
    'docs_url': None,
    'download_url': 'UNKNOWN',
    'downloads': {'last_day': -1, 'last_month': -1, 'last_week': -1},
    'home_page': 'https://github.com/pypa/sampleproject',
    'keywords': 'sample setuptools development',
    'license': 'MIT',
    'maintainer': None,
    'maintainer_email': None,
    'name': 'sampleproject',
    'package_url': 'https://pypi.org/project/sampleproject/',
    'platform': 'UNKNOWN',
    'project_url': 'https://pypi.org/project/sampleproject/',
    'project_urls': {'Download': 'UNKNOWN',
                     'Homepage': 'https://github.com/pypa/sampleproject'},
    'release_url': 'https://pypi.org/project/sampleproject/1.2.0/',
    'requires_dist': None,
    'requires_python': None,
    'summary': 'A sample Python project',
    'version': '1.2.0'}

Kết quả có thể được giới hạn ở một *độ sâu* nhất định (dấu ba chấm được dùng cho nội dung ở các cấp sâu hơn)::

   >>> pprint.pp(project_info, depth=1)
   {'author': 'The Python Packaging Authority',
    'author_email': 'pypa-dev@googlegroups.com',
    'bugtrack_url': None,
    'classifiers': [...],
    'description': 'A sample Python project\n'
                   '=======================\n'
                   '\n'
                   'This is the description file for the project.\n'
                   '\n'
                   'The file should use UTF-8 encoding and be written using '
                   'ReStructured Text. It\n'
                   'will be used to generate the project webpage on PyPI, and '
                   'should be written for\n'
                   'that purpose.\n'
                   '\n'
                   'Typical contents for this file would include an overview of '
                   'the project, basic\n'
                   'usage examples, etc. Generally, including the project '
                   'changelog in here is not\n'
                   'a good idea, although a simple "What\'s New" section for the '
                   'most recent version\n'
                   'may be appropriate.',
    'description_content_type': None,
    'docs_url': None,
    'download_url': 'UNKNOWN',
    'downloads': {...},
    'home_page': 'https://github.com/pypa/sampleproject',
    'keywords': 'sample setuptools development',
    'license': 'MIT',
    'maintainer': None,
    'maintainer_email': None,
    'name': 'sampleproject',
    'package_url': 'https://pypi.org/project/sampleproject/',
    'platform': 'UNKNOWN',
    'project_url': 'https://pypi.org/project/sampleproject/',
    'project_urls': {...},
    'release_url': 'https://pypi.org/project/sampleproject/1.2.0/',
    'requires_dist': None,
    'requires_python': None,
    'summary': 'A sample Python project',
    'version': '1.2.0'}

Ngoài ra, có thể đề xuất *chiều rộng* tối đa tính theo số ký tự. Nếu không thể tách một đối tượng dài, chiều rộng được chỉ định sẽ bị vượt quá::

   >>> pprint.pp(project_info, depth=1, width=60)
   {'author': 'The Python Packaging Authority',
    'author_email': 'pypa-dev@googlegroups.com',
    'bugtrack_url': None,
    'classifiers': [...],
    'description': 'A sample Python project\n'
                   '=======================\n'
                   '\n'
                   'This is the description file for the '
                   'project.\n'
                   '\n'
                   'The file should use UTF-8 encoding and be '
                   'written using ReStructured Text. It\n'
                   'will be used to generate the project '
                   'webpage on PyPI, and should be written '
                   'for\n'
                   'that purpose.\n'
                   '\n'
                   'Typical contents for this file would '
                   'include an overview of the project, '
                   'basic\n'
                   'usage examples, etc. Generally, including '
                   'the project changelog in here is not\n'
                   'a good idea, although a simple "What\'s '
                   'New" section for the most recent version\n'
                   'may be appropriate.',
    'description_content_type': None,
    'docs_url': None,
    'download_url': 'UNKNOWN',
    'downloads': {...},
    'home_page': 'https://github.com/pypa/sampleproject',
    'keywords': 'sample setuptools development',
    'license': 'MIT',
    'maintainer': None,
    'maintainer_email': None,
    'name': 'sampleproject',
    'package_url': 'https://pypi.org/project/sampleproject/',
    'platform': 'UNKNOWN',
    'project_url': 'https://pypi.org/project/sampleproject/',
    'project_urls': {...},
    'release_url': 'https://pypi.org/project/sampleproject/1.2.0/',
    'requires_dist': None,
    'requires_python': None,
    'summary': 'A sample Python project',
    'version': '1.2.0'}

.. _`PyPI`: https://pypi.org
