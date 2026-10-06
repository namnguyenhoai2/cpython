:mod:`!configparser` --- Trình phân tích cú pháp tệp cấu hình
=============================================================

.. module:: configparser
   :synopsis: Trình phân tích cú pháp tệp cấu hình.

.. moduleauthor:: Ken Manheimer <klm@zope.com>
.. moduleauthor:: Barry Warsaw <bwarsaw@python.org>
.. moduleauthor:: Eric S. Raymond <esr@thyrsus.com>
.. moduleauthor:: Łukasz Langa <lukasz@langa.pl>
.. sectionauthor:: Christopher G. Petrilli <petrilli@amber.org>
.. sectionauthor:: Łukasz Langa <lukasz@langa.pl>

**Mã nguồn:** :source:`Lib/configparser.py`

.. index::
   pair: .ini; file
   pair: configuration; file
   single: ini file
   single: Windows ini file

--------------

Mô-đun này cung cấp lớp :class:`ConfigParser`, triển khai một ngôn ngữ cấu hình cơ bản có cấu trúc tương tự như cấu trúc trong các tệp INI của Microsoft Windows. Bạn có thể sử dụng lớp này để viết các chương trình Python mà người dùng cuối có thể dễ dàng tùy chỉnh.

.. note::

   Thư viện này *không* diễn giải hoặc ghi các tiền tố kiểu giá trị được sử dụng trong phiên bản mở rộng của cú pháp INI trong Windows Registry.

.. seealso::

   Mô-đun :mod:`tomllib`
      TOML là một định dạng được đặc tả rõ ràng dành cho các tệp cấu hình ứng dụng. Định dạng này được thiết kế chuyên biệt để trở thành một phiên bản cải tiến của INI.

   Mô-đun :mod:`shlex`
      Hỗ trợ tạo các mini-language giống shell Unix, cũng có thể được dùng cho các tệp cấu hình ứng dụng.

   Mô-đun :mod:`json`
      Mô-đun ``json`` triển khai một tập hợp con cú pháp JavaScript đôi khi được dùng cho cấu hình, nhưng không hỗ trợ chú thích.


.. testsetup::

   import configparser

.. testcleanup::

   import os
   os.remove("example.ini")
   os.remove("override.ini")


Bắt đầu nhanh
-------------

Hãy xem xét một tệp cấu hình rất cơ bản có dạng như sau:

.. code-block:: ini

   [DEFAULT]
   ServerAliveInterval = 45
   Compression = yes
   CompressionLevel = 9
   ForwardX11 = yes

   [forge.example]
   User = hg

   [topsecret.server.example]
   Port = 50022
   ForwardX11 = no

Cấu trúc của các tệp INI được mô tả `trong phần sau <#supported-ini-file-structure>`_. Về cơ bản, tệp bao gồm các section, mỗi section chứa các key cùng với value.
:mod:`!configparser` các lớp có thể đọc và ghi những tệp như vậy. Hãy bắt đầu bằng cách tạo tệp cấu hình ở trên theo phương thức lập trình.

.. doctest::

   >>> import configparser
   >>> config = configparser.ConfigParser()
   >>> config['DEFAULT'] = {'ServerAliveInterval': '45',
   ...                      'Compression': 'yes',
   ...                      'CompressionLevel': '9'}
   >>> config['forge.example'] = {}
   >>> config['forge.example']['User'] = 'hg'
   >>> config['topsecret.server.example'] = {}
   >>> topsecret = config['topsecret.server.example']
   >>> topsecret['Port'] = '50022'     # thay đổi parser
   >>> topsecret['ForwardX11'] = 'no'  # ở đây cũng vậy
   >>> config['DEFAULT']['ForwardX11'] = 'yes'
   >>> with open('example.ini', 'w') as configfile:
   ...   config.write(configfile)
   ...

Như bạn có thể thấy, chúng ta có thể sử dụng config parser gần giống như một dictionary. Có một số điểm khác biệt, `được trình bày ở phần sau <#mapping-protocol-access>`_, nhưng hành vi của nó rất gần với những gì bạn mong đợi từ một dictionary.

Bây giờ chúng ta đã tạo và lưu tệp cấu hình, hãy đọc lại tệp đó và khám phá dữ liệu mà nó chứa.

.. doctest::

   >>> config = configparser.ConfigParser()
   >>> config.sections()
   []
   >>> config.read('example.ini')
   ['example.ini']
   >>> config.sections()
   ['forge.example', 'topsecret.server.example']
   >>> 'forge.example' in config
   True
   >>> 'python.org' in config
   False
   >>> config['forge.example']['User']
   'hg'
   >>> config['DEFAULT']['Compression']
   'yes'
   >>> topsecret = config['topsecret.server.example']
   >>> topsecret['ForwardX11']
   'no'
   >>> topsecret['Port']
   '50022'
   >>> for key in config['forge.example']:  # doctest: +SKIP
   ...     print(key)
   user
   compressionlevel
   serveraliveinterval
   compression
   forwardx11
   >>> config['forge.example']['ForwardX11']
   'yes'

Như có thể thấy ở trên, API khá dễ sử dụng. Phần duy nhất có chút đặc biệt liên quan đến ``DEFAULT`` section, cung cấp các giá trị mặc định cho tất cả các section khác [1]_. Cũng lưu ý rằng các key trong section không phân biệt chữ hoa chữ thường và được lưu ở dạng chữ thường [1]_.

Có thể đọc nhiều cấu hình vào một
:class:`ConfigParser`, trong đó cấu hình được thêm gần đây nhất có độ ưu tiên cao nhất. Mọi khóa xung đột sẽ được lấy từ cấu hình mới hơn, còn các khóa đã tồn tại trước đó vẫn được giữ lại. Ví dụ dưới đây đọc một tệp ``override.ini``, tệp này sẽ ghi đè mọi khóa xung đột từ tệp ``example.ini``.

.. code-block:: ini

   [DEFAULT]
   ServerAliveInterval = -1

.. doctest::

   >>> config_override = configparser.ConfigParser()
   >>> config_override['DEFAULT'] = {'ServerAliveInterval': '-1'}
   >>> with open('override.ini', 'w') as configfile:
   ...     config_override.write(configfile)
   ...
   >>> config_override = configparser.ConfigParser()
   >>> config_override.read(['example.ini', 'override.ini'])
   ['example.ini', 'override.ini']
   >>> print(config_override.get('DEFAULT', 'ServerAliveInterval'))
   -1


Hành vi này tương đương với một lời gọi :meth:`ConfigParser.read` có nhiều tệp được truyền vào tham số *filenames*.


Các kiểu dữ liệu được hỗ trợ
----------------------------

Các trình phân tích cấu hình không tự đoán kiểu dữ liệu của các giá trị trong tệp cấu hình mà luôn lưu trữ chúng nội bộ dưới dạng chuỗi. Điều này có nghĩa là nếu cần các kiểu dữ liệu khác, bạn nên tự chuyển đổi:

.. doctest::

   >>> int(topsecret['Port'])
   50022
   >>> float(topsecret['CompressionLevel'])
   9.0

Vì tác vụ này rất phổ biến, các trình phân tích cấu hình cung cấp nhiều phương thức getter tiện dụng để xử lý số nguyên, số thực và giá trị Boolean. Loại cuối cùng thú vị nhất vì việc chỉ truyền giá trị vào ``bool()`` sẽ không có tác dụng, bởi ``bool('False')`` vẫn là ``True``. Vì vậy, các trình phân tích cấu hình cũng cung cấp :meth:`~ConfigParser.getboolean`. Phương thức này không phân biệt chữ hoa chữ thường và nhận diện các giá trị Boolean từ ``'yes'``/``'no'``, ``'on'``/``'off'``, ``'true'``/``'false'`` và ``'1'``/``'0'`` [1]_. Ví dụ:

.. doctest::

   >>> topsecret.getboolean('ForwardX11')
   False
   >>> config['forge.example'].getboolean('ForwardX11')
   True
   >>> config.getboolean('forge.example', 'Compression')
   True

Ngoài :meth:`~ConfigParser.getboolean`, các trình phân tích cấu hình cũng cung cấp :meth:`~ConfigParser.getint` tương đương và
:meth:`~ConfigParser.getfloat` phương thức. Bạn có thể đăng ký các converter của riêng mình và tùy chỉnh những converter được cung cấp. [1]_

Giá trị dự phòng
----------------

Tương tự như với dictionary, bạn có thể sử dụng phương thức :meth:`~ConfigParser.get` của một section để cung cấp các giá trị dự phòng:

.. doctest::

   >>> topsecret.get('Port')
   '50022'
   >>> topsecret.get('CompressionLevel')
   '9'
   >>> topsecret.get('Cipher')
   >>> topsecret.get('Cipher', '3des-cbc')
   '3des-cbc'

Lưu ý rằng các giá trị mặc định được ưu tiên hơn các giá trị dự phòng. Chẳng hạn, trong ví dụ của chúng ta, key ``'CompressionLevel'`` chỉ được chỉ định trong section ``'DEFAULT'``. Nếu thử lấy key này từ section ``'topsecret.server.example'``, chúng ta sẽ luôn nhận được giá trị mặc định, ngay cả khi chỉ định một giá trị dự phòng:

.. doctest::

   >>> topsecret.get('CompressionLevel', '3')
   '9'

Một điều nữa cần lưu ý là phương thức :meth:`~ConfigParser.get` ở cấp parser cung cấp một interface tùy chỉnh, phức tạp hơn, được duy trì để đảm bảo khả năng tương thích ngược. Khi sử dụng phương thức này, bạn có thể cung cấp giá trị dự phòng thông qua đối số chỉ dành cho keyword ``fallback``:

.. doctest::

   >>> config.get('forge.example', 'monster',
   ...            fallback='No such things as monsters')
   'No such things as monsters'

Có thể sử dụng cùng đối số ``fallback`` với
:meth:`~ConfigParser.getint`, :meth:`~ConfigParser.getfloat` và
:meth:`~ConfigParser.getboolean` phương thức, ví dụ:

.. doctest::

   >>> 'BatchMode' in topsecret
   False
   >>> topsecret.getboolean('BatchMode', fallback=True)
   True
   >>> config['DEFAULT']['BatchMode'] = 'no'
   >>> topsecret.getboolean('BatchMode', fallback=True)
   False


Cấu trúc tệp INI được hỗ trợ
----------------------------

Một tệp cấu hình bao gồm các phần, mỗi phần bắt đầu bằng tiêu đề ``[section]``, theo sau là các mục khóa/giá trị được phân tách bằng một chuỗi cụ thể (``=`` hoặc ``:`` theo mặc định [1]_). Theo mặc định, tên phần phân biệt chữ hoa chữ thường nhưng khóa thì không [1]_. Khoảng trắng ở đầu và cuối được loại bỏ khỏi khóa và giá trị. Có thể bỏ qua giá trị nếu parser được cấu hình cho phép điều đó [1]_, trong trường hợp đó dấu phân cách khóa/giá trị cũng có thể được bỏ qua. Giá trị cũng có thể trải dài trên nhiều dòng, miễn là chúng được thụt lề sâu hơn dòng đầu tiên của giá trị. Tùy thuộc vào chế độ của parser, các dòng trống có thể được coi là một phần của giá trị nhiều dòng hoặc bị bỏ qua.

Theo mặc định, tên phần hợp lệ có thể là bất kỳ chuỗi nào không chứa '\\n'. Để thay đổi điều này, hãy xem :attr:`ConfigParser.SECTCRE`.

Có thể bỏ qua tên phần đầu tiên nếu parser được cấu hình cho phép một phần cấp cao nhất không có tên bằng ``allow_unnamed_section=True``. Trong trường hợp này, có thể truy xuất các khóa/giá trị bằng :const:`UNNAMED_SECTION` như trong ``config[UNNAMED_SECTION]``.

Tệp cấu hình có thể chứa chú thích, được bắt đầu bằng các ký tự cụ thể (``#`` và ``;`` theo mặc định [1]_). Chú thích có thể xuất hiện riêng trên một dòng vốn trống, và có thể được thụt lề. [1]_

Ví dụ:

.. code-block:: ini

   [Simple Values]
   key=value
   spaces in keys=allowed
   spaces in values=allowed as well
   spaces around the delimiter = obviously
   you can also use : to delimit keys from values

   [All Values Are Strings]
   values like this: 1000000
   or this: 3.14159265359
   are they treated as numbers? : no
   integers, floats and booleans are held as: strings
   can use the API to get converted values directly: true

   [Multiline Values]
   chorus: I'm a lumberjack, and I'm okay
       I sleep all night and I work all day

   [No Values]
   key_without_value
   empty string value here =

   [You can use comments]
   # như thế này
   ; or this

   # Theo mặc định, chỉ trên một dòng trống.
   # Chú thích cùng dòng có thể gây hại vì chúng ngăn người dùng
   # sử dụng các ký tự phân cách làm một phần của giá trị.
   # Tuy vậy, bạn có thể tùy chỉnh điều này.

       [Sections Can Be Indented]
           can_values_be_as_well = True
           does_that_mean_anything_special = False
           purpose = formatting for readability
           multiline_values = are
               handled just fine as
               long as they are indented
               deeper than the first line
               of a value
           # Tôi đã đề cập rằng chúng ta cũng có thể thụt lề chú thích chưa?


.. _unnamed-sections:

Các phần không tên
------------------

Có thể bỏ qua tên của section đầu tiên (hoặc section duy nhất) và truy xuất các giá trị bằng thuộc tính :const:`UNNAMED_SECTION`.

.. doctest::

   >>> config = """
   ... option = value
   ...
   ... [  Section 2  ]
   ... another = val
   ... """
   >>> unnamed = configparser.ConfigParser(allow_unnamed_section=True)
   >>> unnamed.read_string(config)
   >>> unnamed.get(configparser.UNNAMED_SECTION, 'option')
   'value'

Nội suy giá trị
---------------

Ngoài chức năng cốt lõi, :class:`ConfigParser` hỗ trợ nội suy. Điều này có nghĩa là các giá trị có thể được tiền xử lý trước khi trả về từ các lần gọi ``get()``.

.. index:: single: % (percent); interpolation in configuration files

.. class:: BasicInterpolation()

   Triển khai mặc định được :class:`ConfigParser` sử dụng. Triển khai này cho phép các giá trị chứa các chuỗi định dạng tham chiếu đến các giá trị khác trong cùng section hoặc các giá trị trong section mặc định đặc biệt [1]_. Có thể cung cấp thêm các giá trị mặc định khi khởi tạo.

   Ví dụ:

   .. code-block:: ini

      [Paths]
      home_dir: /Users
      my_dir: %(home_dir)s/lumberjack
      my_pictures: %(my_dir)s/Pictures

      [Escape]
      # dùng %% để escape dấu % (% là ký tự duy nhất cần được escape):
      gain: 80%%

   Trong ví dụ trên, :class:`ConfigParser` với *interpolation* được đặt thành ``BasicInterpolation()`` sẽ phân giải ``%(home_dir)s`` thành giá trị của ``home_dir`` (``/Users`` trong trường hợp này). ``%(my_dir)s`` thực tế sẽ được phân giải thành ``/Users/lumberjack``. Tất cả nội suy đều được thực hiện theo yêu cầu, vì vậy các khóa được sử dụng trong chuỗi tham chiếu không cần phải được chỉ định theo bất kỳ thứ tự cụ thể nào trong tệp cấu hình.

   Khi ``interpolation`` được đặt thành ``None``, parser sẽ chỉ trả về ``%(my_dir)s/Pictures`` làm giá trị của ``my_pictures`` và ``%(home_dir)s/lumberjack`` làm giá trị của ``my_dir``.

.. index:: single: $ (dollar); interpolation in configuration files

.. class:: ExtendedInterpolation()

   Một handler thay thế cho interpolation, triển khai cú pháp nâng cao hơn và được sử dụng chẳng hạn trong ``zc.buildout``. Extended interpolation sử dụng ``${section:option}`` để biểu thị một giá trị từ một section khác. Interpolation có thể trải qua nhiều cấp. Để thuận tiện, nếu bỏ qua phần ``section:``, interpolation sẽ mặc định sử dụng section hiện tại (và có thể cả các giá trị mặc định từ section đặc biệt).

   Ví dụ: cấu hình được chỉ định ở trên với basic interpolation sẽ có dạng như sau khi sử dụng extended interpolation:

   .. code-block:: ini

      [Paths]
      home_dir: /Users
      my_dir: ${home_dir}/lumberjack
      my_pictures: ${my_dir}/Pictures

      [Escape]
      # dùng $$ để escape dấu $ ($ là ký tự duy nhất cần được escape):
      cost: $$80

   Bạn cũng có thể lấy các giá trị từ những section khác:

   .. code-block:: ini

      [Common]
      home_dir: /Users
      library_dir: /Library
      system_dir: /System
      macports_dir: /opt/local

      [Frameworks]
      Python: 3.2
      path: ${Common:system_dir}/Library/Frameworks/

      [Arthur]
      nickname: Two Sheds
      last_name: Jackson
      my_dir: ${Common:home_dir}/twosheds
      my_pictures: ${my_dir}/Pictures
      python_dir: ${Frameworks:path}/Python/Versions/${Frameworks:Python}

Truy cập theo giao thức ánh xạ
------------------------------

.. versionadded:: 3.2

Truy cập theo giao thức ánh xạ là tên gọi chung cho chức năng cho phép sử dụng các đối tượng tùy chỉnh như thể chúng là dictionary. Trong trường hợp :mod:`!configparser`, việc triển khai mapping interface sử dụng ký hiệu ``parser['section']['option']``.

``parser['section']`` cụ thể trả về một proxy cho dữ liệu của section trong parser. Điều này có nghĩa là các giá trị không được sao chép mà được lấy từ parser gốc khi cần. Quan trọng hơn nữa, khi các giá trị được thay đổi trên proxy của section, chúng thực sự được thay đổi trong parser gốc.

Các đối tượng :mod:`!configparser` hoạt động gần giống các dictionary thực tế nhất có thể. Giao diện mapping được hoàn thiện và tuân theo
ABC :class:`~collections.abc.MutableMapping`. Tuy nhiên, có một vài điểm khác biệt cần lưu ý:

* Theo mặc định, tất cả các khóa trong section đều có thể được truy cập theo cách không phân biệt chữ hoa chữ thường [1]_. Ví dụ: ``for option in parser["section"]`` chỉ trả về các tên khóa tùy chọn đã được ``optionxform``'ed. Điều này có nghĩa là các khóa được chuyển thành chữ thường theo mặc định. Đồng thời, đối với một section chứa khóa ``'a'``, cả hai biểu thức đều trả về ``True``::

     "a" in parser["section"]
     "A" in parser["section"]

* Tất cả các section cũng bao gồm các giá trị ``DEFAULTSECT``, nghĩa là ``.clear()`` trên một section có thể không khiến section đó trống theo cách nhìn thấy được. Điều này là vì không thể xóa các giá trị mặc định khỏi section (vì về mặt kỹ thuật, chúng không nằm trong đó). Nếu chúng bị ghi đè trong section, thao tác xóa sẽ khiến giá trị mặc định hiển thị lại. Cố gắng xóa một giá trị mặc định sẽ gây ra :exc:`KeyError`.

* Không thể xóa ``DEFAULTSECT`` khỏi parser:

  * cố gắng xóa nó sẽ gây ra :exc:`ValueError`,

  * ``parser.clear()`` giữ nguyên nó,

  * ``parser.popitem()`` không bao giờ trả về nó.

* ``parser.get(section, option, **kwargs)`` - đối số thứ hai là **not** một giá trị dự phòng. Tuy nhiên, lưu ý rằng các phương thức ``get()`` cấp section tương thích cả với mapping protocol và API configparser cổ điển.

* ``parser.items()`` tương thích với mapping protocol (trả về danh sách các cặp *section_name*, *section_proxy* bao gồm cả DEFAULTSECT). Tuy nhiên, phương thức này cũng có thể được gọi với các đối số: ``parser.items(section, raw, vars)``. Lệnh gọi sau trả về danh sách các cặp *option*, *value* cho một ``section`` được chỉ định, với tất cả các phép nội suy được mở rộng (trừ khi ``raw=True`` được cung cấp).

mapping protocol được triển khai trên API legacy hiện có, vì vậy các subclass ghi đè interface ban đầu vẫn sẽ có mapping hoạt động như mong đợi.


.. _`Customizing Parser Behaviour`:

Tùy chỉnh hành vi của Parser
----------------------------

Số lượng biến thể của định dạng INI gần tương đương với số lượng ứng dụng sử dụng nó.
:mod:`!configparser` hỗ trợ rất nhiều kiểu INI hợp lý nhất có thể. Chức năng mặc định chủ yếu được quyết định bởi bối cảnh lịch sử, và rất có thể bạn sẽ muốn tùy chỉnh một số tính năng.

Cách phổ biến nhất để thay đổi cách một config parser cụ thể hoạt động là sử dụng các tùy chọn :meth:`!__init__`:

* *defaults*, giá trị mặc định: ``None``

  Tùy chọn này chấp nhận một dictionary gồm các cặp key-value, ban đầu sẽ được đưa vào section ``DEFAULT``. Đây là một cách hiệu quả để hỗ trợ các tệp cấu hình ngắn gọn, trong đó không cần chỉ định những giá trị trùng với giá trị mặc định đã được ghi trong tài liệu.

  Gợi ý: nếu bạn muốn chỉ định các giá trị mặc định cho một section cụ thể, hãy sử dụng
  :meth:`~ConfigParser.read_dict` trước khi đọc tệp thực tế.

* *dict_type*, giá trị mặc định: :class:`dict`

  Tùy chọn này có ảnh hưởng lớn đến cách mapping protocol hoạt động và hình thức của các tệp cấu hình được ghi. Với dictionary tiêu chuẩn, mỗi section được lưu theo thứ tự chúng được thêm vào parser. Điều tương tự cũng áp dụng cho các option trong section.

  Có thể sử dụng một kiểu dictionary thay thế, chẳng hạn để sắp xếp các section và option khi ghi lại.

  Lưu ý: có những cách để thêm một tập hợp các cặp key-value trong một thao tác duy nhất. Khi sử dụng dictionary thông thường trong các thao tác đó, thứ tự các key sẽ được sắp xếp. Ví dụ:

  .. doctest::

     >>> parser = configparser.ConfigParser()
     >>> parser.read_dict({'section1': {'key1': 'value1',
     ...                                'key2': 'value2',
     ...                                'key3': 'value3'},
     ...                   'section2': {'keyA': 'valueA',
     ...                                'keyB': 'valueB',
     ...                                'keyC': 'valueC'},
     ...                   'section3': {'foo': 'x',
     ...                                'bar': 'y',
     ...                                'baz': 'z'}
     ... })
     >>> parser.sections()
     ['section1', 'section2', 'section3']
     >>> [option for option in parser['section3']]
     ['foo', 'bar', 'baz']

* *allow_no_value*, giá trị mặc định: ``False``

  Một số tệp cấu hình được biết là có các thiết lập không có giá trị, nhưng vẫn tuân theo cú pháp được :mod:`!configparser` hỗ trợ. Có thể sử dụng tham số *allow_no_value* của constructor để cho biết rằng các giá trị như vậy được chấp nhận:

  .. doctest::

     >>> import configparser

     >>> sample_config = """
     ... [mysqld]
     ...   user = mysql
     ...   pid-file = /var/run/mysqld/mysqld.pid
     ...   skip-external-locking
     ...   old_passwords = 1
     ...   skip-bdb
     ...   # hôm nay chúng ta không cần ACID
     ...   skip-innodb
     ... """
     >>> config = configparser.ConfigParser(allow_no_value=True)
     >>> config.read_string(sample_config)

     >>> # Các thiết lập có giá trị được xử lý như trước:
     >>> config["mysqld"]["user"]
     'mysql'

     >>> # Các thiết lập không có giá trị sẽ cung cấp None:
     >>> config["mysqld"]["skip-bdb"]

     >>> # Các thiết lập không được chỉ định vẫn gây ra lỗi:
     >>> config["mysqld"]["does-not-exist"]
     Traceback (most recent call last):
       ...
     KeyError: 'does-not-exist'

* *delimiters*, giá trị mặc định: ``('=', ':')``

  Delimiters là các chuỗi con dùng để phân tách khóa khỏi giá trị trong một section. Lần xuất hiện đầu tiên của chuỗi con phân tách trên một dòng được xem là delimiter. Điều này có nghĩa là các giá trị (nhưng không phải khóa) có thể chứa delimiters.

  Xem thêm đối số *space_around_delimiters*
  :meth:`ConfigParser.write`.

* *comment_prefixes*, giá trị mặc định: ``('#', ';')``

* *inline_comment_prefixes*, giá trị mặc định: ``None``

  Tiền tố comment là các chuỗi cho biết vị trí bắt đầu của một comment hợp lệ trong tệp cấu hình. *comment_prefixes* chỉ được sử dụng trên các dòng vốn trống (có thể được thụt lề), trong khi *inline_comment_prefixes* có thể được sử dụng sau mọi giá trị hợp lệ (chẳng hạn như tên section, option và cả các dòng trống). Theo mặc định, comment inline bị vô hiệu hóa, còn ``'#'`` và ``';'`` được dùng làm tiền tố cho comment trên toàn dòng.

  .. versionchanged:: 3.2
     Trong các phiên bản trước, hành vi của :mod:`!configparser` khớp với ``comment_prefixes=('#',';')`` và ``inline_comment_prefixes=(';',)``.

  Lưu ý rằng các config parser không hỗ trợ việc escape tiền tố comment, vì vậy việc sử dụng *inline_comment_prefixes* có thể ngăn người dùng chỉ định các giá trị option chứa những ký tự được dùng làm tiền tố comment. Khi không chắc chắn, hãy tránh thiết lập *inline_comment_prefixes*. Trong mọi trường hợp, cách duy nhất để lưu các ký tự tiền tố comment ở đầu một dòng trong các giá trị nhiều dòng là nội suy tiền tố, chẳng hạn như::

    >>> from configparser import ConfigParser, ExtendedInterpolation
    >>> parser = ConfigParser(interpolation=ExtendedInterpolation())
    >>> # cũng có thể sử dụng BasicInterpolation mặc định
    >>> parser.read_string("""
    ... [DEFAULT]
    ... hash = #
    ...
    ... [hashes]
    ... shebang =
    ...   ${hash}!/usr/bin/env python
    ...   ${hash} -*- coding: utf-8 -*-
    ...
    ... extensions =
    ...   enabled_extension
    ...   another_extension
    ...   #disabled_by_comment
    ...   yet_another_extension
    ...
    ... interpolation not necessary = if # không ở đầu dòng
    ... even in multiline values = line #1
    ...   line #2
    ...   line #3
    ... """)
    >>> print(parser['hashes']['shebang'])
    <BLANKLINE>
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    >>> print(parser['hashes']['extensions'])
    <BLANKLINE>
    enabled_extension
    another_extension
    yet_another_extension
    >>> print(parser['hashes']['interpolation not necessary'])
    if # không ở đầu dòng
    >>> print(parser['hashes']['even in multiline values'])
    line #1
    line #2
    line #3

* *strict*, giá trị mặc định: ``True``

  Khi được đặt thành ``True``, parser sẽ không cho phép bất kỳ section hoặc option nào bị trùng lặp trong khi đọc từ một nguồn duy nhất (sử dụng :meth:`~ConfigParser.read_file`,
  :meth:`~ConfigParser.read_string` hoặc :meth:`~ConfigParser.read_dict`). Bạn nên sử dụng strict parser trong các ứng dụng mới.

  .. versionchanged:: 3.2
     Trong các phiên bản trước, hành vi của :mod:`!configparser` khớp với ``strict=False``.

* *empty_lines_in_values*, giá trị mặc định: ``True``

  Trong các config parser, giá trị có thể trải dài trên nhiều dòng miễn là chúng được thụt lề nhiều hơn key chứa chúng. Theo mặc định, parser cũng cho phép các dòng trống là một phần của giá trị. Đồng thời, bản thân các key có thể được thụt lề tùy ý để cải thiện khả năng đọc. Do đó, khi các file cấu hình trở nên lớn và phức tạp, người dùng rất dễ mất dấu cấu trúc của file. Ví dụ:

  .. code-block:: ini

     [Section]
     key = multiline
       value with a gotcha

      this = is still a part of the multiline value of 'key'

  Điều này có thể đặc biệt gây khó khăn cho người dùng khi xem nếu cô ấy đang sử dụng phông chữ tỷ lệ để chỉnh sửa tệp. Đó là lý do vì sao khi ứng dụng của bạn không cần các giá trị có dòng trống, bạn nên cân nhắc không cho phép chúng. Khi đó, các dòng trống sẽ luôn phân tách các khóa. Trong ví dụ trên, kết quả sẽ là hai khóa, ``key`` và ``this``.

* *default_section*, giá trị mặc định: ``configparser.DEFAULTSECT`` (tức là: ``"DEFAULT"``)

  Quy ước cho phép một section đặc biệt chứa các giá trị mặc định cho những section khác hoặc phục vụ mục đích interpolation là một khái niệm mạnh mẽ của thư viện này, cho phép người dùng tạo các cấu hình khai báo phức tạp. Section này thường được gọi là ``"DEFAULT"``, nhưng có thể tùy chỉnh để trỏ đến bất kỳ tên section hợp lệ nào khác. Một số giá trị thường dùng gồm: ``"general"`` hoặc ``"common"``. Tên được cung cấp sẽ được dùng để nhận diện các section mặc định khi đọc từ bất kỳ nguồn nào và được dùng khi ghi cấu hình trở lại tệp. Có thể lấy giá trị hiện tại của tên này bằng thuộc tính ``parser_instance.default_section`` và có thể thay đổi nó trong runtime (tức là để chuyển đổi tệp từ định dạng này sang định dạng khác).

* *interpolation*, giá trị mặc định: ``configparser.BasicInterpolation``

  Có thể tùy chỉnh hành vi interpolation bằng cách cung cấp một handler tùy chỉnh thông qua đối số *interpolation*. Có thể dùng ``None`` để tắt hoàn toàn interpolation; ``ExtendedInterpolation()`` cung cấp một biến thể nâng cao hơn, lấy cảm hứng từ ``zc.buildout``. Xem thêm về chủ đề này trong `phần tài liệu chuyên biệt <#interpolation-of-values>`_.
  :class:`RawConfigParser` có giá trị mặc định là ``None``.

* *converters*, giá trị mặc định: chưa thiết lập

  Bộ phân tích cấu hình cung cấp các getter giá trị tùy chọn thực hiện chuyển đổi kiểu. Theo mặc định :meth:`~ConfigParser.getint`, :meth:`~ConfigParser.getfloat`, và
  :meth:`~ConfigParser.getboolean` được triển khai. Nếu cần các getter khác, người dùng có thể định nghĩa chúng trong một lớp con hoặc truyền vào một dictionary, trong đó mỗi khóa là tên của bộ chuyển đổi và mỗi giá trị là một callable thực hiện việc chuyển đổi đó. Ví dụ, việc truyền ``{'decimal': decimal.Decimal}`` sẽ thêm
  :meth:`!getdecimal` vào cả đối tượng parser và tất cả section proxy. Nói cách khác, có thể viết cả ``parser_instance.getdecimal('section', 'key', fallback=0)`` và ``parser_instance['section'].getdecimal('key', 0)``.

  Nếu bộ chuyển đổi cần truy cập trạng thái của parser, bạn có thể triển khai nó dưới dạng một method trên lớp con của config parser. Nếu tên của method này bắt đầu bằng ``get``, nó sẽ khả dụng trên tất cả section proxy, dưới dạng tương thích với dict (xem ví dụ ``getdecimal()`` ở trên).

Có thể thực hiện việc tùy chỉnh nâng cao hơn bằng cách ghi đè các giá trị mặc định của những thuộc tính parser này. Các giá trị mặc định được định nghĩa trên các lớp, vì vậy có thể ghi đè chúng trong các lớp con hoặc bằng phép gán thuộc tính.

.. attribute:: ConfigParser.BOOLEAN_STATES

   Theo mặc định khi sử dụng :meth:`~ConfigParser.getboolean`, config parser coi các giá trị sau là ``True``: ``'1'``, ``'yes'``, ``'true'``, ``'on'`` và các giá trị sau là ``False``: ``'0'``, ``'no'``, ``'false'``, ``'off'``. Bạn có thể ghi đè hành vi này bằng cách chỉ định một dictionary tùy chỉnh gồm các chuỗi và kết quả Boolean tương ứng. Ví dụ:

   .. doctest::

      >>> custom = configparser.ConfigParser()
      >>> custom['section1'] = {'funky': 'nope'}
      >>> custom['section1'].getboolean('funky')
      Traceback (most recent call last):
      ...
      ValueError: Not a boolean: nope
      >>> custom.BOOLEAN_STATES = {'sure': True, 'nope': False}
      >>> custom['section1'].getboolean('funky')
      False

   Các cặp Boolean điển hình khác bao gồm ``accept``/``reject`` hoặc ``enabled``/``disabled``.

.. method:: ConfigParser.optionxform(option)
   :noindex:

   Phương thức này chuyển đổi tên tùy chọn trong mọi thao tác đọc, get hoặc set. Theo mặc định, tên được chuyển thành chữ thường. Điều này cũng có nghĩa là khi tệp cấu hình được ghi, tất cả các khóa sẽ ở dạng chữ thường. Hãy ghi đè phương thức này nếu cách xử lý đó không phù hợp. Ví dụ:

   .. doctest::

      >>> config = """
      ... [Section1]
      ... Key = Value
      ...
      ... [Section2]
      ... AnotherKey = Value
      ... """
      >>> typical = configparser.ConfigParser()
      >>> typical.read_string(config)
      >>> list(typical['Section1'].keys())
      ['key']
      >>> list(typical['Section2'].keys())
      ['anotherkey']
      >>> custom = configparser.RawConfigParser()
      >>> custom.optionxform = lambda option: option
      >>> custom.read_string(config)
      >>> list(custom['Section1'].keys())
      ['Key']
      >>> list(custom['Section2'].keys())
      ['AnotherKey']

   .. note::
      Hàm optionxform chuyển đổi tên tùy chọn thành dạng chuẩn. Đây nên là một hàm lũy đẳng (idempotent): nếu tên đã ở dạng chuẩn thì phải trả về tên đó mà không thay đổi.


.. attribute:: ConfigParser.SECTCRE

   Một biểu thức chính quy đã biên dịch được dùng để phân tích cú pháp tiêu đề section. Theo mặc định, biểu thức này khớp với ``[section]`` để lấy tên ``"section"``. Khoảng trắng được xem là một phần của tên section, vì vậy ``[  larch  ]`` sẽ được đọc là section có tên ``"  larch  "``. Hãy ghi đè thuộc tính này nếu cách xử lý đó không phù hợp. Ví dụ:

   .. doctest::

      >>> import re
      >>> config = """
      ... [Section 1]
      ... option = value
      ...
      ... [  Section 2  ]
      ... another = val
      ... """
      >>> typical = configparser.ConfigParser()
      >>> typical.read_string(config)
      >>> typical.sections()
      ['Section 1', '  Section 2  ']
      >>> custom = configparser.ConfigParser()
      >>> custom.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
      >>> custom.read_string(config)
      >>> custom.sections()
      ['Section 1', 'Section 2']

   .. note::

      Mặc dù các đối tượng ConfigParser cũng sử dụng thuộc tính ``OPTCRE`` để nhận diện các dòng tùy chọn, bạn không nên ghi đè thuộc tính này vì điều đó sẽ ảnh hưởng đến các tùy chọn constructor *allow_no_value* và *delimiters*.


Các ví dụ về API cũ
-------------------

Chủ yếu do các mối lo ngại về khả năng tương thích ngược, :mod:`!configparser` cũng cung cấp một API cũ với các phương thức ``get``/``set`` tường minh. Mặc dù các phương thức được trình bày dưới đây có những trường hợp sử dụng hợp lệ, việc truy cập theo mapping protocol được ưu tiên cho các dự án mới. API cũ đôi khi nâng cao hơn, ở mức thấp hơn và hoàn toàn không trực quan.

Ví dụ về cách ghi vào tệp cấu hình::

   import configparser

   config = configparser.RawConfigParser()

   # Lưu ý rằng khi sử dụng các hàm set của RawConfigParser, bạn có thể gán
   # các giá trị không phải chuỗi cho các khóa ở bên trong, nhưng sẽ nhận được lỗi khi
   # cố ghi vào tệp hoặc khi lấy giá trị ở chế độ không raw. Việc thiết lập
   # giá trị bằng mapping protocol hoặc set() của ConfigParser không cho phép
   # thực hiện các phép gán như vậy.
   config.add_section('Section1')
   config.set('Section1', 'an_int', '15')
   config.set('Section1', 'a_bool', 'true')
   config.set('Section1', 'a_float', '3.1415')
   config.set('Section1', 'baz', 'fun')
   config.set('Section1', 'bar', 'Python')
   config.set('Section1', 'foo', '%(bar)s is %(baz)s!')

   # Ghi tệp cấu hình của chúng ta vào 'example.cfg'
   with open('example.cfg', 'w') as configfile:
       config.write(configfile)

Ví dụ về việc đọc lại tệp cấu hình::

   import configparser

   config = configparser.RawConfigParser()
   config.read('example.cfg')

   # getfloat() sẽ phát sinh ngoại lệ nếu giá trị không phải là số thực
   # getint() và getboolean() cũng thực hiện điều tương tự với các kiểu tương ứng
   a_float = config.getfloat('Section1', 'a_float')
   an_int = config.getint('Section1', 'an_int')
   print(a_float + an_int)

   # Lưu ý rằng kết quả tiếp theo không nội suy '%(bar)s' hoặc '%(baz)s'.
   # Điều này là do chúng ta đang sử dụng RawConfigParser().
   if config.getboolean('Section1', 'a_bool'):
       print(config.get('Section1', 'foo'))

Để thực hiện nội suy, hãy sử dụng :class:`ConfigParser`::

   import configparser

   cfg = configparser.ConfigParser()
   cfg.read('example.cfg')

   # Đặt đối số tùy chọn *raw* của get() thành True nếu bạn muốn tắt
   # tính nội suy trong một thao tác get đơn lẻ.
   print(cfg.get('Section1', 'foo', raw=False))  # -> "Python is fun!"
   print(cfg.get('Section1', 'foo', raw=True))   # -> "%(bar)s is %(baz)s!"

   # Đối số tùy chọn *vars* là một dict chứa các thành viên sẽ được ưu tiên
   # khi nội suy.
   print(cfg.get('Section1', 'foo', vars={'bar': 'Documentation',
                                          'baz': 'evil'}))

   # Đối số tùy chọn *fallback* có thể được dùng để cung cấp một giá trị dự phòng
   print(cfg.get('Section1', 'foo'))
         # -> "Python is fun!"

   print(cfg.get('Section1', 'foo', fallback='Monty is not.'))
         # -> "Python is fun!"

   print(cfg.get('Section1', 'monster', fallback='No such things as monsters.'))
         # -> "Không có quái vật nào cả."

   # Lệnh gọi print(cfg.get('Section1', 'monster')) đơn thuần sẽ raise NoOptionError
   # nhưng chúng ta cũng có thể sử dụng:

   print(cfg.get('Section1', 'monster', fallback=None))
         # -> None

Giá trị mặc định có sẵn trong cả hai loại ConfigParsers. Chúng được sử dụng trong quá trình interpolation nếu một option được sử dụng nhưng chưa được định nghĩa ở nơi khác.::

   import configparser

   # Instance mới với 'bar' và 'baz' lần lượt có giá trị mặc định là 'Life' và 'hard'
   config = configparser.ConfigParser({'bar': 'Life', 'baz': 'hard'})
   config.read('example.cfg')

   print(config.get('Section1', 'foo'))     # -> "Python is fun!"
   config.remove_option('Section1', 'bar')
   config.remove_option('Section1', 'baz')
   print(config.get('Section1', 'foo'))     # -> "Cuộc sống thật khó khăn!"


.. _configparser-objects:

Đối tượng ConfigParser
----------------------

.. class:: ConfigParser(defaults=None, dict_type=dict, allow_no_value=False, *, \
                        delimiters=('=', ':'), comment_prefixes=('#', ';'), \ inline_comment_prefixes=None, strict=True, \ empty_lines_in_values=True, \ default_section=configparser.DEFAULTSECT, \ interpolation=BasicInterpolation(), converters={}, \ allow_unnamed_section=False)

   Trình phân tích cú pháp cấu hình chính. Khi *defaults* được cung cấp, nó sẽ được khởi tạo vào dictionary của các giá trị mặc định tích hợp sẵn. Khi *dict_type* được cung cấp, nó sẽ được dùng để tạo các đối tượng dictionary cho danh sách section, các tùy chọn trong một section và các giá trị mặc định.

   Khi *delimiters* được cung cấp, nó được dùng làm tập hợp các chuỗi con phân tách khóa khỏi giá trị. Khi *comment_prefixes* được cung cấp, nó sẽ được dùng làm tập hợp các chuỗi con đứng trước comment trong các dòng vốn trống. Comment có thể được thụt lề. Khi *inline_comment_prefixes* được cung cấp, nó sẽ được dùng làm tập hợp các chuỗi con đứng trước comment trong các dòng không trống.

   Khi *strict* là ``True`` (mặc định), trình phân tích cú pháp sẽ không cho phép bất kỳ section hoặc tùy chọn trùng lặp nào khi đọc từ một nguồn duy nhất (tệp, chuỗi hoặc dictionary), và sẽ phát sinh :exc:`DuplicateSectionError` hoặc
   :exc:`DuplicateOptionError`. Khi *empty_lines_in_values* là ``False`` (mặc định: ``True``), mỗi dòng trống đánh dấu kết thúc của một tùy chọn. Nếu không, các dòng trống bên trong của một tùy chọn nhiều dòng sẽ được giữ lại như một phần của giá trị. Khi *allow_no_value* là ``True`` (mặc định: ``False``), các tùy chọn không có giá trị được chấp nhận; giá trị được lưu cho các tùy chọn này là ``None`` và chúng được tuần tự hóa mà không có dấu phân tách ở cuối.

   Khi *default_section* được cung cấp, nó chỉ định tên cho section đặc biệt chứa các giá trị mặc định của những section khác và phục vụ mục đích nội suy (thông thường có tên là ``"DEFAULT"``). Có thể truy xuất và thay đổi giá trị này trong runtime bằng thuộc tính instance ``default_section``. Việc này sẽ không đánh giá lại tệp cấu hình đã được phân tích cú pháp, nhưng sẽ được sử dụng khi ghi các thiết lập đã phân tích cú pháp vào một tệp cấu hình mới.

   Có thể tùy chỉnh hành vi nội suy bằng cách cung cấp một handler tùy chỉnh thông qua đối số *interpolation*. Có thể sử dụng ``None`` để tắt hoàn toàn nội suy; ``ExtendedInterpolation()`` cung cấp một biến thể nâng cao hơn lấy cảm hứng từ ``zc.buildout``. Tìm hiểu thêm về chủ đề này trong `phần tài liệu chuyên biệt <#interpolation-of-values>`_.

   Tất cả tên option được sử dụng trong nội suy sẽ được truyền qua
   :meth:`optionxform` method giống như mọi tham chiếu tên option khác. Ví dụ, khi sử dụng triển khai mặc định của :meth:`optionxform` (chuyển tên option thành chữ thường), các giá trị ``foo %(bar)s`` và ``foo %(BAR)s`` là tương đương.

   Khi *converters* được cung cấp, nó phải là một dictionary trong đó mỗi key đại diện cho tên của một type converter, còn mỗi value là một callable thực hiện việc chuyển đổi từ string sang datatype mong muốn. Mỗi converter sẽ có method :meth:`!get*` tương ứng riêng trên parser object và các section proxy.

   Khi *allow_unnamed_section* là ``True`` (mặc định: ``False``), có thể bỏ qua tên section đầu tiên. Xem phần `"Unnamed Sections" <#unnamed-sections>`_.

   Có thể đọc nhiều cấu hình vào một
   :class:`ConfigParser`, trong đó cấu hình được thêm gần đây nhất có mức ưu tiên cao nhất. Mọi khóa xung đột sẽ được lấy từ cấu hình mới hơn, còn các khóa đã tồn tại trước đó vẫn được giữ lại. Ví dụ dưới đây đọc một tệp ``override.ini``, tệp này sẽ ghi đè mọi khóa xung đột từ tệp ``example.ini``.

   .. code-block:: ini

      [DEFAULT]
      ServerAliveInterval = -1

   .. doctest::

      >>> config_override = configparser.ConfigParser()
      >>> config_override['DEFAULT'] = {'ServerAliveInterval': '-1'}
      >>> with open('override.ini', 'w') as configfile:
      ...     config_override.write(configfile)
      ...
      >>> config_override = configparser.ConfigParser()
      >>> config_override.read(['example.ini', 'override.ini'])
      ['example.ini', 'override.ini']
      >>> print(config_override.get('DEFAULT', 'ServerAliveInterval'))
      -1

   .. versionchanged:: 3.1
      *dict_type* mặc định là :class:`collections.OrderedDict`.

   .. versionchanged:: 3.2
      *allow_no_value*, *delimiters*, *comment_prefixes*, *strict*, *empty_lines_in_values*, *default_section* và *interpolation* đã được thêm vào.

   .. versionchanged:: 3.5
      Đối số *converters* đã được thêm vào.

   .. versionchanged:: 3.7
      Đối số *defaults* được đọc bằng :meth:`read_dict`, mang lại hành vi nhất quán trên toàn bộ parser: các khóa và giá trị không phải chuỗi sẽ được chuyển đổi ngầm thành chuỗi.

   .. versionchanged:: 3.8
      *dict_type* mặc định là :class:`dict`, vì hiện tại nó bảo toàn thứ tự chèn.

   .. versionchanged:: 3.13
      Ném một :exc:`MultilineContinuationError` khi *allow_no_value* là ``True``, và một khóa không có giá trị được tiếp tục bằng một dòng thụt lề.

   .. versionchanged:: 3.13
      Đối số *allow_unnamed_section* đã được thêm vào.

   .. method:: defaults()

      Trả về một dictionary chứa các giá trị mặc định áp dụng trên toàn instance.


   .. method:: sections()

      Trả về danh sách các section hiện có; *default section* không được đưa vào danh sách.


   .. method:: add_section(section)

      Thêm một section có tên *section* vào instance. Nếu section có tên đã cho đã tồn tại, :exc:`DuplicateSectionError` sẽ được raise. Nếu truyền tên *default section*, :exc:`ValueError` sẽ được raise. Tên của section phải là một chuỗi; nếu không, :exc:`TypeError` sẽ được raise.

      .. versionchanged:: 3.2
         Tên section không phải chuỗi sẽ raise :exc:`TypeError`.


   .. method:: has_section(section)

      Cho biết *section* đã chỉ định có tồn tại trong cấu hình hay không. *default section* không được tính đến.


   .. method:: options(section)

      Trả về danh sách các option có sẵn trong *section* được chỉ định.


   .. method:: has_option(section, option)

      Nếu *section* đã cho tồn tại và chứa *option* đã cho, trả về
      :const:`True`; nếu không, trả về :const:`False`. Nếu *section* được chỉ định là :const:`None` hoặc chuỗi rỗng, DEFAULT sẽ được giả định.


   .. method:: read(filenames, encoding=None)

      Thử đọc và phân tích cú pháp một iterable gồm các tên tệp, rồi trả về danh sách các tên tệp đã được phân tích cú pháp thành công.

      Nếu *filenames* là một chuỗi, một đối tượng :class:`bytes` hoặc một
      :term:`path-like object`, nó được xem là một tên tệp duy nhất. Nếu không thể mở tệp được nêu trong *filenames*, tệp đó sẽ bị bỏ qua. Cách này cho phép bạn chỉ định một iterable gồm các vị trí tệp cấu hình có thể có (ví dụ: thư mục hiện tại, thư mục home của người dùng và một thư mục toàn hệ thống), đồng thời tất cả các tệp cấu hình hiện có trong iterable sẽ được đọc.

      Nếu không có tệp nào được nêu tồn tại, thực thể :class:`ConfigParser` sẽ chứa một dataset trống. Ứng dụng yêu cầu tải các giá trị ban đầu từ tệp nên tải tệp hoặc các tệp cần thiết bằng :meth:`read_file` trước khi gọi :meth:`read` cho bất kỳ tệp tùy chọn nào::

         import configparser, os

         config = configparser.ConfigParser()
         config.read_file(open('defaults.cfg'))
         config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')],
                     encoding='cp1250')

      .. versionchanged:: 3.2
         Đã thêm tham số *encoding*. Trước đây, tất cả các tệp đều được đọc bằng encoding mặc định của :func:`open`.

      .. versionchanged:: 3.6.1
         Tham số *filenames* chấp nhận một :term:`path-like object`.

      .. versionchanged:: 3.7
         Tham số *filenames* chấp nhận một đối tượng :class:`bytes`.


   .. method:: read_file(f, source=None)

      Đọc và phân tích dữ liệu cấu hình từ *f*, đối tượng này phải là một iterable trả về các chuỗi Unicode (ví dụ: các tệp được mở ở chế độ văn bản).

      Đối số tùy chọn *source* chỉ định tên của tệp đang được đọc. Nếu không được cung cấp và *f* có một :attr:`!name` thuộc tính, thuộc tính đó được dùng cho *source*; giá trị mặc định là ``'<???>'``.

      .. versionadded:: 3.2
         Thay thế :meth:`!readfp`.

   .. method:: read_string(string, source='<string>')

      Phân tích cú pháp dữ liệu cấu hình từ một chuỗi.

      Đối số tùy chọn *source* chỉ định tên theo ngữ cảnh của chuỗi được truyền vào. Nếu không được cung cấp, ``'<string>'`` được sử dụng. Giá trị này thường nên là một đường dẫn hệ thống tệp hoặc một URL.

      .. versionadded:: 3.2


   .. method:: read_dict(dictionary, source='<dict>')

      Tải cấu hình từ bất kỳ đối tượng nào cung cấp phương thức ``items()`` giống dict. Các khóa là tên phần, còn các giá trị là những từ điển chứa các khóa và giá trị cần có trong phần đó. Nếu kiểu từ điển được sử dụng có bảo toàn thứ tự, các phần và khóa của chúng sẽ được thêm theo thứ tự. Các giá trị sẽ được tự động chuyển thành chuỗi.

      Đối số tùy chọn *source* chỉ định tên dành riêng cho ngữ cảnh của từ điển được truyền vào. Nếu không được cung cấp, ``<dict>`` sẽ được sử dụng.

      Có thể sử dụng phương thức này để sao chép trạng thái giữa các parser.

      .. versionadded:: 3.2


   .. method:: get(section, option, *, raw=False, vars=None[, fallback])

      Lấy giá trị *option* cho *section* có tên. Nếu cung cấp *vars*, đối số này phải là một từ điển. *option* được tra cứu lần lượt trong *vars* (nếu được cung cấp), *section* và *DEFAULTSECT*. Nếu không tìm thấy khóa và cung cấp *fallback*, giá trị này sẽ được sử dụng làm giá trị dự phòng. Có thể cung cấp ``None`` làm giá trị *fallback*.

      Tất cả các phép nội suy ``'%'`` được mở rộng trong các giá trị trả về, trừ khi đối số *raw* là true. Các giá trị của khóa nội suy được tra cứu theo cùng cách như tùy chọn.

      .. versionchanged:: 3.2
         Các đối số *raw*, *vars* và *fallback* chỉ được truyền dưới dạng từ khóa để ngăn người dùng cố sử dụng đối số thứ ba làm giá trị dự phòng *fallback* (đặc biệt khi sử dụng mapping protocol).


   .. method:: getint(section, option, *, raw=False, vars=None[, fallback])

      Một phương thức tiện ích chuyển *option* trong *section* được chỉ định thành số nguyên. Xem :meth:`get` để biết giải thích về *raw*, *vars* và *fallback*.


   .. method:: getfloat(section, option, *, raw=False, vars=None[, fallback])

      Một phương thức tiện ích chuyển đổi *option* trong *section* được chỉ định thành một số dấu phẩy động. Xem :meth:`get` để biết giải thích về *raw*, *vars* và *fallback*.


   .. method:: getboolean(section, option, *, raw=False, vars=None[, fallback])

      Một phương thức tiện ích chuyển đổi *option* trong *section* được chỉ định thành một giá trị Boolean. Lưu ý rằng các giá trị được chấp nhận cho tùy chọn này là ``'1'``, ``'yes'``, ``'true'`` và ``'on'``, khiến phương thức này trả về ``True``; còn ``'0'``, ``'no'``, ``'false'`` và ``'off'`` khiến phương thức trả về ``False``. Các giá trị chuỗi này được kiểm tra không phân biệt chữ hoa chữ thường. Bất kỳ giá trị nào khác sẽ khiến phương thức này raise
      :exc:`ValueError`. Xem :meth:`get` để biết giải thích về *raw*, *vars* và *fallback*.


   .. method:: items(raw=False, vars=None)
               items(section, raw=False, vars=None)

      Khi không cung cấp *section*, trả về một danh sách các cặp *section_name*, *section_proxy*, bao gồm DEFAULTSECT.

      Nếu không, trả về một danh sách các cặp *name*, *value* cho các tùy chọn trong *section* đã cho. Các đối số tùy chọn có ý nghĩa giống như đối với
      :meth:`get` phương thức.

      .. versionchanged:: 3.8
         Các mục có trong *vars* sẽ không còn xuất hiện trong kết quả. Hành vi trước đây đã trộn lẫn các tùy chọn parser thực tế với các biến được cung cấp để nội suy.


   .. method:: set(section, option, value)

      Nếu section đã cho tồn tại, đặt option đã cho thành giá trị được chỉ định; nếu không, phát sinh :exc:`NoSectionError`. *option* và *value* phải là các chuỗi; nếu không, :exc:`TypeError` sẽ được phát sinh.


   .. method:: write(fileobject, space_around_delimiters=True)

      Ghi biểu diễn của cấu hình vào :term:`file object` đã chỉ định, đối tượng này phải được mở ở chế độ văn bản (chấp nhận các chuỗi). Biểu diễn này có thể được phân tích cú pháp bằng một lệnh gọi :meth:`read` trong tương lai. Nếu *space_around_delimiters* là true, các dấu phân cách giữa khóa và giá trị sẽ được bao quanh bởi khoảng trắng.

      .. versionchanged:: 3.14
         Phát sinh InvalidWriteError nếu thao tác này sẽ ghi một biểu diễn không thể được phân tích cú pháp chính xác bằng một lệnh gọi :meth:`read` trong tương lai từ parser này.

   .. note::

      Các chú thích trong tệp cấu hình ban đầu không được giữ lại khi ghi cấu hình trở lại. Nội dung nào được xem là chú thích phụ thuộc vào các giá trị đã cho của *comment_prefix* và *inline_comment_prefix*.


   .. method:: remove_option(section, option)

      Xóa *option* đã chỉ định khỏi *section* đã chỉ định. Nếu section không tồn tại, phát sinh :exc:`NoSectionError`. Nếu option cần xóa tồn tại, trả về :const:`True`; nếu không, trả về
      :const:`False`.


   .. method:: remove_section(section)

      Xóa *section* đã chỉ định khỏi cấu hình. Nếu section thực sự tồn tại, trả về ``True``. Nếu không, trả về ``False``.


   .. method:: optionxform(option)

      Chuyển đổi tên tùy chọn *option* được tìm thấy trong tệp đầu vào hoặc được mã client truyền vào thành dạng nên được sử dụng trong các cấu trúc nội bộ. Cách triển khai mặc định trả về phiên bản viết thường của *option*; các lớp con có thể ghi đè cách này hoặc mã client có thể đặt một thuộc tính có tên này trên các instance để thay đổi hành vi.

      Bạn không cần tạo lớp con của parser để sử dụng phương thức này; bạn cũng có thể đặt nó trên một instance thành một hàm nhận một đối số chuỗi và trả về một chuỗi. Ví dụ, đặt nó thành ``str`` sẽ khiến tên tùy chọn phân biệt chữ hoa chữ thường::

         cfgparser = ConfigParser()
         cfgparser.optionxform = str

      Lưu ý rằng khi đọc các tệp cấu hình, khoảng trắng xung quanh tên tùy chọn sẽ bị loại bỏ trước khi gọi :meth:`optionxform`.


.. data:: UNNAMED_SECTION

   Một đối tượng đặc biệt biểu diễn tên section dùng để tham chiếu đến section không có tên (xem :ref:`unnamed-sections`).


.. data:: MAX_INTERPOLATION_DEPTH

   Độ sâu tối đa cho phép nội suy đệ quy đối với :meth:`~configparser.ConfigParser.get` khi tham số *raw* là false. Điều này chỉ liên quan khi sử dụng *interpolation* mặc định.


.. _rawconfigparser-objects:

Đối tượng RawConfigParser
-------------------------

.. class:: RawConfigParser(defaults=None, dict_type=dict, \
                           allow_no_value=False, *, delimiters=('=', ':'), \ comment_prefixes=('#', ';'), \ inline_comment_prefixes=None, strict=True, \ empty_lines_in_values=True, \ default_section=configparser.DEFAULTSECT, \ interpolation=BasicInterpolation(), converters={}, \ allow_unnamed_section=False

   Biến thể cũ của :class:`ConfigParser`. Theo mặc định, tính năng interpolation bị vô hiệu hóa và cho phép tên section, tên tùy chọn và giá trị không phải chuỗi thông qua các phương thức không an toàn ``add_section`` và ``set``, cũng như cách xử lý đối số từ khóa ``defaults=`` kiểu cũ.

   .. versionchanged:: 3.2
      *allow_no_value*, *delimiters*, *comment_prefixes*, *strict*, *empty_lines_in_values*, *default_section* và *interpolation* đã được thêm vào.

   .. versionchanged:: 3.5
      Đối số *converters* đã được thêm vào.

   .. versionchanged:: 3.8
      *dict_type* mặc định là :class:`dict`, vì hiện tại nó bảo toàn thứ tự chèn.

   .. versionchanged:: 3.13
      Đối số *allow_unnamed_section* đã được thêm vào.

   .. note::
      Hãy cân nhắc sử dụng :class:`ConfigParser` thay vào đó, vì nó kiểm tra kiểu của các giá trị được lưu trữ nội bộ. Nếu không muốn sử dụng interpolation, bạn có thể dùng ``ConfigParser(interpolation=None)``.


   .. method:: add_section(section)

      Thêm section có tên *section* hoặc :const:`UNNAMED_SECTION` vào instance.

      Nếu section đã cho đã tồn tại, :exc:`DuplicateSectionError` sẽ được ném ra. Nếu truyền tên *default section*, :exc:`ValueError` sẽ được ném ra. Nếu truyền :const:`UNNAMED_SECTION` và hỗ trợ bị tắt,
      :exc:`UnnamedSectionDisabledError` sẽ được ném ra.

      Kiểu của *section* không được kiểm tra, cho phép người dùng tạo các section có tên không phải chuỗi. Hành vi này không được hỗ trợ và có thể gây ra lỗi nội bộ.

   .. versionchanged:: 3.14
      Đã bổ sung hỗ trợ cho :const:`UNNAMED_SECTION`.


   .. method:: set(section, option, value)

      Nếu section đã cho tồn tại, đặt option đã cho thành giá trị được chỉ định; nếu không thì ném ra :exc:`NoSectionError`. Mặc dù có thể sử dụng
      :class:`RawConfigParser` (hoặc :class:`ConfigParser` với các tham số *raw* được đặt thành true) để *lưu trữ* nội bộ các giá trị không phải chuỗi, chỉ có thể đạt được đầy đủ chức năng (bao gồm interpolation và xuất ra tệp) bằng cách sử dụng các giá trị chuỗi.

      Phương thức này cho phép người dùng gán các giá trị không phải chuỗi cho các key ở bên trong. Hành vi này không được hỗ trợ và sẽ gây ra lỗi khi cố gắng ghi vào tệp hoặc lấy dữ liệu ở chế độ không raw. **Sử dụng API mapping protocol**, API này không cho phép thực hiện các phép gán như vậy.


Ngoại lệ
--------

.. exception:: Error

   Lớp cơ sở cho tất cả các ngoại lệ :mod:`!configparser` khác.


.. exception:: NoSectionError

   Ngoại lệ được phát sinh khi không tìm thấy phần được chỉ định.


.. exception:: DuplicateSectionError

   Ngoại lệ được phát sinh nếu :meth:`~ConfigParser.add_section` được gọi với tên của một phần đã tồn tại hoặc trong các parser strict khi một phần được tìm thấy nhiều hơn một lần trong cùng một tệp, chuỗi hoặc dictionary đầu vào.

   .. versionchanged:: 3.2
      Đã thêm các thuộc tính và tham số tùy chọn *source* và *lineno* vào
      :meth:`!__init__`.


.. exception:: DuplicateOptionError

   Ngoại lệ được các parser strict phát sinh nếu một tùy chọn xuất hiện hai lần trong quá trình đọc từ cùng một tệp, chuỗi hoặc dictionary. Điều này phát hiện các lỗi chính tả và lỗi liên quan đến phân biệt chữ hoa chữ thường; ví dụ, một dictionary có thể có hai khóa đại diện cho cùng một khóa cấu hình không phân biệt chữ hoa chữ thường.


.. exception:: NoOptionError

   Ngoại lệ được phát sinh khi không tìm thấy tùy chọn được chỉ định trong phần được chỉ định.


.. exception:: InterpolationError

   Lớp cơ sở cho các ngoại lệ phát sinh khi xảy ra sự cố trong quá trình nội suy chuỗi.


.. exception:: InterpolationDepthError

   Ngoại lệ phát sinh khi không thể hoàn tất quá trình nội suy chuỗi vì số lần lặp vượt quá :const:`MAX_INTERPOLATION_DEPTH`.  Lớp con của
   :exc:`InterpolationError`.


.. exception:: InterpolationMissingOptionError

   Ngoại lệ phát sinh khi một tùy chọn được tham chiếu từ một giá trị không tồn tại. Lớp con của :exc:`InterpolationError`.


.. exception:: InterpolationSyntaxError

   Ngoại lệ phát sinh khi văn bản nguồn được dùng để thực hiện các phép thay thế không tuân theo cú pháp bắt buộc.  Lớp con của :exc:`InterpolationError`.


.. exception:: MissingSectionHeaderError

   Ngoại lệ phát sinh khi cố gắng phân tích cú pháp một tệp không có tiêu đề phần.

.. exception:: ParsingError

   Ngoại lệ phát sinh khi xảy ra lỗi trong quá trình cố gắng phân tích cú pháp một tệp.

   .. versionchanged:: 3.12
      Thuộc tính ``filename`` và đối số hàm khởi tạo :meth:`!__init__` đã bị xóa.  Chúng đã có thể được sử dụng với tên ``source`` kể từ phiên bản 3.2.

.. exception:: MultilineContinuationError

   Ngoại lệ được đưa ra khi một khóa không có giá trị tương ứng được tiếp nối bằng một dòng thụt lề.

   .. versionadded:: 3.13

.. exception:: UnnamedSectionDisabledError

   Ngoại lệ được đưa ra khi cố gắng sử dụng
   :const:`UNNAMED_SECTION` mà không bật nó.

    .. versionadded:: 3.14

.. exception:: InvalidWriteError

   Ngoại lệ được đưa ra khi một :meth:`ConfigParser.write` được cố gắng thực hiện sẽ không được phân tích chính xác bằng một lệnh gọi :meth:`ConfigParser.read` trong tương lai.

   Ví dụ: Việc ghi một khóa bắt đầu bằng mẫu :attr:`ConfigParser.SECTCRE` sẽ được phân tích thành tiêu đề phần khi đọc. Cố gắng ghi khóa này sẽ đưa ra ngoại lệ này.

   .. versionadded:: 3.14

.. rubric:: Chú thích

.. [1] Trình phân tích cú pháp cấu hình cho phép tùy chỉnh sâu. Nếu bạn muốn thay đổi hành vi được nêu trong tham chiếu chú thích, hãy tham khảo phần `Customizing Parser Behaviour <Customizing Parser Behaviour_>`_.

.. _`in the following section`: #supported-ini-file-structure
.. _`outlined later`: #mapping-protocol-access
.. _`dedicated documentation section`: #interpolation-of-values
.. _`"Unnamed Sections" section`: #unnamed-sections
