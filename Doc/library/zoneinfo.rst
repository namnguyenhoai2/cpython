:mod:`!zoneinfo` --- hỗ trợ múi giờ IANA
========================================

.. module:: zoneinfo
    :synopsis: hỗ trợ múi giờ IANA

.. versionadded:: 3.9

.. moduleauthor:: Paul Ganssle <paul@ganssle.io>
.. sectionauthor:: Paul Ganssle <paul@ganssle.io>

**Mã nguồn:** :source:`Lib/zoneinfo`

--------------

Mô-đun :mod:`!zoneinfo` cung cấp một triển khai múi giờ cụ thể để hỗ trợ cơ sở dữ liệu múi giờ IANA như được đặc tả ban đầu trong :pep:`615`. Theo mặc định, :mod:`!zoneinfo` sử dụng dữ liệu múi giờ của hệ thống nếu có; nếu không có dữ liệu múi giờ của hệ thống, thư viện sẽ chuyển sang sử dụng gói :pypi:`tzdata` chính chủ có trên PyPI.

.. seealso::

    Mô-đun: :mod:`datetime`
        Cung cấp các kiểu :class:`~datetime.time` và :class:`~datetime.datetime`, được thiết kế để sử dụng cùng với lớp :class:`ZoneInfo`.

    Gói :pypi:`tzdata`
        Gói first-party do các nhà phát triển cốt lõi của CPython duy trì để cung cấp dữ liệu múi giờ thông qua PyPI.

.. include:: ../includes/wasm-notavail.rst

Sử dụng ``ZoneInfo``
--------------------

:class:`ZoneInfo` là một triển khai cụ thể của lớp cơ sở trừu tượng :class:`datetime.tzinfo`, và được thiết kế để gắn vào ``tzinfo``, thông qua hàm khởi tạo, phương thức :meth:`datetime.replace <datetime.datetime.replace>` hoặc :meth:`datetime.astimezone <datetime.datetime.astimezone>`::

    >>> from zoneinfo import ZoneInfo
    >>> import datetime as dt

    >>> when = dt.datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("America/Los_Angeles"))
    >>> print(when)
    2020-10-31 12:00:00-07:00

    >>> when.tzname()
    'PDT'

Các đối tượng datetime được tạo theo cách này tương thích với phép tính toán datetime và xử lý các quá trình chuyển đổi giờ mùa hè mà không cần can thiệp thêm::

    >>> when_add = when + dt.timedelta(days=1)

    >>> print(when_add)
    2020-11-01 12:00:00-08:00

    >>> when_add.tzname()
    'PST'

Các múi giờ này cũng hỗ trợ thuộc tính :attr:`~datetime.datetime.fold` được giới thiệu trong :pep:`495`. Trong các quá trình chuyển đổi độ lệch gây ra thời điểm không rõ ràng (chẳng hạn như quá trình chuyển từ giờ mùa hè sang giờ chuẩn), độ lệch từ *trước* quá trình chuyển đổi được sử dụng khi ``fold=0``, còn độ lệch *sau* quá trình chuyển đổi được sử dụng khi ``fold=1``, chẳng hạn::

    >>> when = dt.datetime(2020, 11, 1, 1, tzinfo=ZoneInfo("America/Los_Angeles"))
    >>> print(when)
    2020-11-01 01:00:00-07:00

    >>> print(when.replace(fold=1))
    2020-11-01 01:00:00-08:00

Khi chuyển đổi từ một múi giờ khác, fold sẽ được đặt thành giá trị chính xác::

    >>> LOS_ANGELES = ZoneInfo("America/Los_Angeles")
    >>> when_utc = dt.datetime(2020, 11, 1, 8, tzinfo=dt.timezone.utc)

    >>> # Trước quá trình chuyển đổi PDT -> PST
    >>> print(when_utc.astimezone(LOS_ANGELES))
    2020-11-01 01:00:00-07:00

    >>> # Sau khi chuyển từ PDT -> PST
    >>> print((when_utc + dt.timedelta(hours=1)).astimezone(LOS_ANGELES))
    2020-11-01 01:00:00-08:00

Nguồn dữ liệu
-------------

Mô-đun ``zoneinfo`` không trực tiếp cung cấp dữ liệu múi giờ mà lấy thông tin múi giờ từ cơ sở dữ liệu múi giờ của hệ thống hoặc gói PyPI chính thức :pypi:`tzdata`, nếu có. Một số hệ thống, đáng chú ý là các hệ thống Windows, không có sẵn cơ sở dữ liệu IANA, vì vậy đối với các dự án hướng đến khả năng tương thích đa nền tảng và yêu cầu dữ liệu múi giờ, bạn nên khai báo phụ thuộc vào tzdata. Nếu không có dữ liệu hệ thống hoặc tzdata, mọi lệnh gọi đến :class:`ZoneInfo` sẽ phát sinh
:exc:`ZoneInfoNotFoundError`.

.. _zoneinfo_data_configuration:

Cấu hình nguồn dữ liệu
**********************

Khi ``ZoneInfo(key)`` được gọi, constructor trước tiên tìm kiếm trong các thư mục được chỉ định trong :data:`TZPATH` một tệp khớp với ``key``, và nếu không thành công thì tìm tệp khớp trong gói tzdata. Hành vi này có thể được cấu hình theo ba cách:

1. :data:`TZPATH` mặc định khi không được chỉ định theo cách khác có thể được cấu hình tại
   :ref:`thời điểm biên dịch <zoneinfo_data_compile_time_config>`.
2. :data:`TZPATH` có thể được cấu hình bằng :ref:`một biến môi trường <zoneinfo_data_environment_var>`.
3. Tại :ref:`runtime <zoneinfo_data_runtime_config>`, đường dẫn tìm kiếm có thể được điều chỉnh bằng hàm :func:`reset_tzpath`.

.. _zoneinfo_data_compile_time_config:

Cấu hình tại thời điểm biên dịch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:data:`TZPATH` mặc định bao gồm một số vị trí triển khai phổ biến của cơ sở dữ liệu múi giờ (trừ Windows, nơi không có các vị trí "đã biết" cho dữ liệu múi giờ). Trên các hệ thống POSIX, các nhà phân phối và những người xây dựng Python từ mã nguồn biết dữ liệu múi giờ của hệ thống được triển khai ở đâu có thể thay đổi đường dẫn múi giờ mặc định bằng cách chỉ định tùy chọn tại thời điểm biên dịch ``TZPATH`` (hoặc nhiều khả năng hơn là :option:`configure flag --with-tzpath <--with-tzpath>`), tùy chọn này phải là một chuỗi được phân tách bằng
:data:`os.pathsep`.

Trên tất cả các nền tảng, giá trị được cấu hình có sẵn dưới dạng khóa ``TZPATH`` trong
:func:`sysconfig.get_config_var`.

.. _zoneinfo_data_environment_var:

Cấu hình môi trường
^^^^^^^^^^^^^^^^^^^

Khi khởi tạo :data:`TZPATH` (tại thời điểm import hoặc bất cứ khi nào
:func:`reset_tzpath` được gọi mà không có đối số), mô-đun ``zoneinfo`` sẽ sử dụng biến môi trường ``PYTHONTZPATH``, nếu biến này tồn tại, để thiết lập đường dẫn tìm kiếm.

.. envvar:: PYTHONTZPATH

    Đây là một chuỗi được phân tách bằng :data:`os.pathsep`, chứa đường dẫn tìm kiếm múi giờ cần sử dụng. Chuỗi này chỉ được chứa các đường dẫn tuyệt đối, không phải đường dẫn tương đối. Các thành phần tương đối được chỉ định trong ``PYTHONTZPATH`` sẽ không được sử dụng, nhưng ngoài điều đó, hành vi khi chỉ định một đường dẫn tương đối là do triển khai quyết định; CPython sẽ phát sinh :exc:`InvalidTZPathWarning`, nhưng các triển khai khác có thể bỏ qua thành phần không hợp lệ một cách im lặng hoặc phát sinh một ngoại lệ.

Để thiết lập hệ thống bỏ qua dữ liệu hệ thống và sử dụng gói tzdata thay thế, hãy đặt ``PYTHONTZPATH=""``.

.. _zoneinfo_data_runtime_config:

Cấu hình runtime
^^^^^^^^^^^^^^^^

Bạn cũng có thể cấu hình đường dẫn tìm kiếm TZ tại runtime bằng cách sử dụng
hàm :func:`reset_tzpath`. Nhìn chung, đây không phải là thao tác được khuyến nghị, mặc dù việc sử dụng hàm này trong các hàm kiểm thử yêu cầu sử dụng một đường dẫn múi giờ cụ thể (hoặc yêu cầu vô hiệu hóa quyền truy cập vào các múi giờ của hệ thống) là hợp lý.


Lớp ``ZoneInfo``
----------------

.. class:: ZoneInfo(key)

    Một lớp con :class:`datetime.tzinfo` cụ thể, đại diện cho múi giờ IANA được chỉ định bằng chuỗi ``key``. Các lệnh gọi đến hàm khởi tạo chính sẽ luôn trả về các đối tượng so sánh giống hệt nhau; nói cách khác, ngoại trừ trường hợp bộ nhớ đệm bị vô hiệu hóa thông qua :meth:`ZoneInfo.clear_cache`, với mọi giá trị của ``key``, assertion sau đây sẽ luôn đúng:

    .. code-block:: python

        a = ZoneInfo(key)
        b = ZoneInfo(key)
        assert a is b

    ``key`` phải có dạng đường dẫn POSIX tương đối, đã được chuẩn hóa và không chứa tham chiếu lên cấp trên. Hàm khởi tạo sẽ phát sinh :exc:`ValueError` nếu được truyền một key không phù hợp.

    Nếu không tìm thấy tệp nào khớp với ``key``, hàm khởi tạo sẽ phát sinh
    :exc:`ZoneInfoNotFoundError`.


Lớp ``ZoneInfo`` có hai hàm khởi tạo thay thế:

.. classmethod:: ZoneInfo.from_file(file_obj, /, key=None)

    Tạo một đối tượng ``ZoneInfo`` từ một đối tượng giống tệp trả về các byte (ví dụ: một tệp được mở ở chế độ nhị phân hoặc một đối tượng :class:`io.BytesIO`). Không giống hàm khởi tạo chính, hàm này luôn tạo một đối tượng mới.

    Tham số ``key`` đặt tên của múi giờ cho mục đích
    :py:meth:`~object.__str__` và :py:meth:`~object.__repr__`.

    Các đối tượng được tạo thông qua hàm khởi tạo này không thể được pickle (xem `pickling`_).

    :exc:`ValueError` được phát sinh nếu dữ liệu đọc từ *file_obj* không phải là tệp TZif hợp lệ.

.. classmethod:: ZoneInfo.no_cache(key)

    Một hàm khởi tạo thay thế bỏ qua cache của hàm khởi tạo. Hàm này giống hệt hàm khởi tạo chính, nhưng trả về một đối tượng mới trong mỗi lần gọi. Hàm này có nhiều khả năng hữu ích cho mục đích kiểm thử hoặc minh họa, nhưng cũng có thể được dùng để tạo một hệ thống với chiến lược vô hiệu hóa cache khác.

    Các đối tượng được tạo thông qua hàm khởi tạo này cũng sẽ bỏ qua cache của tiến trình deserializing khi được unpickle.

    .. TODO: Add "See `cache_behavior`_" reference when that section is ready.

    .. caution::

        Việc sử dụng hàm khởi tạo này có thể làm thay đổi semantics của datetime theo những cách khó lường; chỉ sử dụng nó nếu bạn biết chắc mình cần đến nó.

Các phương thức lớp sau đây cũng khả dụng:

.. classmethod:: ZoneInfo.clear_cache(*, only_keys=None)

    Một phương thức dùng để vô hiệu hóa cache trên lớp ``ZoneInfo``. Nếu không truyền đối số nào, tất cả cache sẽ bị vô hiệu hóa và lần gọi tiếp theo đến hàm khởi tạo chính cho mỗi key sẽ trả về một instance mới.

    Nếu truyền một iterable gồm các tên khóa vào tham số ``only_keys``, chỉ những khóa được chỉ định mới bị xóa khỏi cache. Các khóa được truyền vào ``only_keys`` nhưng không được tìm thấy trong cache sẽ bị bỏ qua.

    .. TODO: Add "See `cache_behavior`_" reference when that section is ready.

    .. warning::

        Việc gọi hàm này có thể thay đổi ngữ nghĩa của các datetime sử dụng ``ZoneInfo`` theo những cách khó lường; thao tác này sửa đổi trạng thái của module và do đó có thể gây ra những ảnh hưởng trên phạm vi rộng. Chỉ sử dụng hàm này nếu bạn biết chắc mình cần đến nó.

Lớp này có một thuộc tính:

.. attribute:: ZoneInfo.key

    Đây là một :term:`attribute` chỉ đọc, trả về giá trị của ``key`` được truyền vào constructor, giá trị này phải là một khóa tra cứu trong cơ sở dữ liệu múi giờ IANA (ví dụ: ``America/New_York``, ``Europe/Paris`` hoặc ``Asia/Tokyo``).

    Đối với các zone được tạo từ tệp mà không chỉ định tham số ``key``, giá trị này sẽ được đặt thành ``None``.

    .. note::

        Mặc dù việc cung cấp các giá trị này cho người dùng cuối là một thực hành khá phổ biến, chúng được thiết kế làm khóa chính để biểu diễn các zone tương ứng và không nhất thiết là các thành phần hướng đến người dùng. Các dự án như CLDR (Unicode Common Locale Data Repository) có thể được sử dụng để lấy các chuỗi thân thiện hơn với người dùng từ những khóa này.

Biểu diễn chuỗi
***************

Biểu diễn chuỗi được trả về khi gọi :py:class:`str` trên một
đối tượng :class:`ZoneInfo` mặc định sử dụng thuộc tính :attr:`ZoneInfo.key` (xem lưu ý về cách sử dụng trong tài liệu về thuộc tính)::

    >>> zone = ZoneInfo("Pacific/Kwajalein")
    >>> str(zone)
    'Pacific/Kwajalein'

    >>> when = dt.datetime(2020, 4, 1, 3, 15, tzinfo=zone)
    >>> f"{when.isoformat()} [{when.tzinfo}]"
    '2020-04-01T03:15:00+12:00 [Pacific/Kwajalein]'

Đối với các đối tượng được tạo từ một tệp mà không chỉ định tham số ``key``, ``str`` sẽ chuyển sang gọi :func:`repr`. ``repr`` của ``ZoneInfo`` được xác định theo cách triển khai và không nhất thiết ổn định giữa các phiên bản, nhưng được đảm bảo không phải là một khóa ``ZoneInfo`` hợp lệ.

.. _pickling:

Tuần tự hóa Pickle
******************

Thay vì tuần tự hóa tất cả dữ liệu chuyển đổi, các đối tượng ``ZoneInfo`` được tuần tự hóa theo khóa, và các đối tượng ``ZoneInfo`` được tạo từ tệp (kể cả những đối tượng có chỉ định giá trị cho ``key``) không thể được pickle.

Hành vi của một tệp ``ZoneInfo`` phụ thuộc vào cách tệp đó được tạo:

1. ``ZoneInfo(key)``: Khi được tạo bằng hàm khởi tạo chính, một đối tượng ``ZoneInfo`` được tuần tự hóa theo khóa; khi được giải tuần tự, quá trình giải tuần tự sử dụng hàm khởi tạo chính, vì vậy đối tượng này được kỳ vọng là cùng một đối tượng với các tham chiếu khác đến cùng múi giờ. Ví dụ: nếu ``europe_berlin_pkl`` là một chuỗi chứa một pickle được tạo từ ``ZoneInfo("Europe/Berlin")``, ta sẽ kỳ vọng hành vi sau:

   .. code-block:: pycon

       >>> a = ZoneInfo("Europe/Berlin")
       >>> b = pickle.loads(europe_berlin_pkl)
       >>> a is b
       True

2. ``ZoneInfo.no_cache(key)``: Khi được tạo bằng constructor bỏ qua cache, đối tượng ``ZoneInfo`` cũng được tuần tự hóa theo key, nhưng khi được giải tuần tự hóa, quá trình giải tuần tự hóa sử dụng constructor bỏ qua cache. Nếu ``europe_berlin_pkl_nc`` là một chuỗi chứa một pickle được tạo từ ``ZoneInfo.no_cache("Europe/Berlin")``, ta sẽ kỳ vọng hành vi sau:

   .. code-block:: pycon

       >>> a = ZoneInfo("Europe/Berlin")
       >>> b = pickle.loads(europe_berlin_pkl_nc)
       >>> a is b
       False

3. ``ZoneInfo.from_file(file_obj, /, key=None)``: Khi được tạo từ một tệp, đối tượng ``ZoneInfo`` sẽ phát sinh ngoại lệ khi pickle. Nếu người dùng cuối muốn pickle một ``ZoneInfo`` được tạo từ một tệp, họ nên sử dụng một kiểu wrapper hoặc một hàm tuần tự hóa tùy chỉnh: либо tuần tự hóa theo key hoặc lưu trữ nội dung của đối tượng tệp rồi tuần tự hóa nội dung đó.

Phương thức tuần tự hóa này yêu cầu dữ liệu múi giờ cho key bắt buộc phải có ở cả phía tuần tự hóa và phía giải tuần tự hóa, tương tự như cách các tham chiếu đến class và function được yêu cầu phải tồn tại trong cả môi trường tuần tự hóa và giải tuần tự hóa. Điều này cũng có nghĩa là không có bảo đảm nào về tính nhất quán của kết quả khi giải pickle một ``ZoneInfo`` được pickle trong môi trường sử dụng phiên bản dữ liệu múi giờ khác.

Các hàm
-------

.. function:: available_timezones()

    Lấy một tập hợp chứa tất cả các key hợp lệ cho múi giờ IANA có ở bất kỳ vị trí nào trên đường dẫn múi giờ. Tập hợp này được tính toán lại trong mỗi lần gọi function.

    Function này chỉ bao gồm các tên vùng chuẩn và không bao gồm các vùng "đặc biệt", chẳng hạn như những vùng nằm trong các thư mục ``posix/`` và ``right/``, hoặc vùng ``posixrules``.

    .. caution::

        Function này có thể mở một số lượng lớn tệp, vì cách tốt nhất để xác định một tệp trên đường dẫn múi giờ có phải là múi giờ hợp lệ hay không là đọc "chuỗi ma thuật" ở phần đầu tệp.

    .. note::

        Các giá trị này không được thiết kế để hiển thị cho người dùng cuối; đối với các phần tử hướng tới người dùng, ứng dụng nên sử dụng một công cụ như CLDR (Unicode Common Locale Data Repository) để lấy các chuỗi thân thiện hơn với người dùng. Xem thêm ghi chú cảnh báo về :attr:`ZoneInfo.key`.

.. function:: reset_tzpath(to=None)

    Thiết lập hoặc đặt lại đường dẫn tìm kiếm múi giờ (:data:`TZPATH`) cho module. Khi được gọi mà không có đối số, :data:`TZPATH` được đặt thành giá trị mặc định.

    Việc gọi ``reset_tzpath`` sẽ không làm mất hiệu lực bộ nhớ đệm :class:`ZoneInfo`, do đó các lệnh gọi đến hàm khởi tạo ``ZoneInfo`` chính chỉ sử dụng ``TZPATH`` mới trong trường hợp bộ nhớ đệm không có mục tương ứng.

    Tham số ``to`` phải là một :term:`sequence` gồm các chuỗi hoặc
    :class:`os.PathLike` chứ không phải một chuỗi, và tất cả chúng phải là các đường dẫn tuyệt đối.
    :exc:`ValueError` sẽ được phát sinh nếu truyền vào bất kỳ giá trị nào khác ngoài một đường dẫn tuyệt đối.

Biến toàn cục
-------------

.. data:: TZPATH

    Một sequence chỉ đọc biểu diễn search path của múi giờ -- khi tạo một ``ZoneInfo`` từ một key, key được nối vào từng mục trong ``TZPATH``, và file đầu tiên được tìm thấy sẽ được sử dụng.

    ``TZPATH`` chỉ có thể chứa các đường dẫn tuyệt đối, không bao giờ chứa đường dẫn tương đối, bất kể được cấu hình như thế nào.

    Đối tượng mà ``zoneinfo.TZPATH`` trỏ tới có thể thay đổi khi gọi :func:`reset_tzpath`, vì vậy bạn nên sử dụng ``zoneinfo.TZPATH`` thay vì import ``TZPATH`` từ ``zoneinfo`` hoặc gán ``zoneinfo.TZPATH`` cho một biến tồn tại lâu dài.

    Để biết thêm thông tin về cách cấu hình search path của múi giờ, hãy xem
    :ref:`zoneinfo_data_configuration`.

Ngoại lệ và cảnh báo
--------------------

.. exception:: ZoneInfoNotFoundError

    Được đưa ra khi việc tạo đối tượng :class:`ZoneInfo` thất bại vì không tìm thấy key được chỉ định trên hệ thống. Đây là một lớp con của
    :exc:`KeyError`.

.. exception:: InvalidTZPathWarning

    Được đưa ra khi :envvar:`PYTHONTZPATH` chứa một thành phần không hợp lệ sẽ bị lọc bỏ, chẳng hạn như một đường dẫn tương đối.

.. Links and references:
