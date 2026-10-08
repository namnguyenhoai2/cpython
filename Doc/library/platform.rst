:mod:`!platform` ---  Truy cập dữ liệu nhận dạng của nền tảng cơ sở
===================================================================

.. module:: platform
   :synopsis: Truy xuất nhiều nhất có thể dữ liệu nhận dạng của nền tảng.

.. moduleauthor:: Marc-André Lemburg <mal@egenix.com>
.. sectionauthor:: Bjorn Pettersen <bpettersen@corp.fairisaac.com>

**Mã nguồn:** :source:`Lib/platform.py`

--------------

.. note::

   Các nền tảng cụ thể được liệt kê theo thứ tự bảng chữ cái, trong đó Linux được đưa vào phần Unix.


Đa nền tảng
-----------


.. function:: architecture(executable=sys.executable, bits='', linkage='')

   Truy vấn tệp thực thi đã cho (mặc định là tệp nhị phân trình thông dịch Python) để lấy nhiều thông tin khác nhau về kiến trúc.

   Trả về một tuple ``(bits, linkage)`` chứa thông tin về kiến trúc bit và định dạng liên kết được sử dụng cho tệp thực thi. Cả hai giá trị đều được trả về dưới dạng chuỗi.

   Các giá trị không thể xác định sẽ được trả về theo các giá trị đặt trước của tham số. Nếu bits được cung cấp dưới dạng ``''``, thì ``sizeof(pointer)`` (hoặc ``sizeof(long)`` trên Python phiên bản < 1.5.2) được sử dụng làm chỉ báo cho kích thước con trỏ được hỗ trợ.

   Hàm này dựa vào lệnh :file:`file` của hệ thống để thực hiện công việc thực tế. Lệnh này có sẵn trên hầu hết, nếu không phải tất cả, các nền tảng Unix và một số nền tảng không phải Unix, nhưng chỉ khi tệp thực thi trỏ đến trình thông dịch Python. Các giá trị mặc định hợp lý được sử dụng khi các yêu cầu nêu trên không được đáp ứng.

   .. note::

      Trên macOS (và có thể cả các nền tảng khác), các tệp thực thi có thể là các tệp universal chứa nhiều kiến trúc.

      Để xác định "64-bit" của trình thông dịch hiện tại, việc truy vấn thuộc tính :data:`sys.maxsize` đáng tin cậy hơn::

         is_64bits = sys.maxsize > 2**32


.. function:: machine()

   Trả về loại máy, ví dụ: ``'AMD64'``. Nếu không thể xác định giá trị, một chuỗi rỗng sẽ được trả về.

   Kết quả phụ thuộc vào nền tảng và có thể khác nhau về cách viết hoa cũng như quy ước đặt tên.


.. function:: node()

   Trả về tên mạng của máy tính (có thể chưa đầy đủ!). Nếu không thể xác định giá trị, một chuỗi rỗng sẽ được trả về.


.. function:: platform(aliased=False, terse=False)

   Trả về một chuỗi duy nhất nhận dạng nền tảng cơ sở với nhiều thông tin hữu ích nhất có thể.

   Đầu ra nhằm mục đích *dễ đọc đối với con người* thay vì có thể được phân tích cú pháp bằng máy. Đầu ra có thể khác nhau trên các nền tảng khác nhau và đây là điều được dự kiến.

   Nếu *aliased* là true, hàm sẽ sử dụng bí danh cho nhiều nền tảng báo cáo tên hệ thống khác với tên thông dụng của chúng; chẳng hạn, SunOS sẽ được báo cáo là Solaris. Hàm :func:`system_alias` được dùng để triển khai việc này.

   Đặt *terse* thành true khiến hàm chỉ trả về lượng thông tin tối thiểu tuyệt đối cần thiết để nhận dạng nền tảng.

   .. versionchanged:: 3.8
      Trên macOS, giờ đây hàm sử dụng :func:`mac_ver`, nếu hàm này trả về một chuỗi release không rỗng, để lấy phiên bản macOS thay vì phiên bản darwin.


.. function:: processor()

   Trả về tên bộ xử lý (thực), ví dụ: ``'amdk6'``.

   Trả về một chuỗi rỗng nếu không thể xác định giá trị. Lưu ý rằng nhiều nền tảng không cung cấp thông tin này hoặc đơn giản trả về cùng một giá trị như
   :func:`machine`. NetBSD thực hiện việc này.


.. function:: python_build()

   Trả về một tuple ``(buildno, builddate)`` cho biết số bản build và ngày build của Python dưới dạng chuỗi.


.. function:: python_compiler()

   Trả về một chuỗi cho biết compiler được sử dụng để biên dịch Python.


.. function:: python_branch()

   Trả về một chuỗi cho biết branch SCM của Python implementation.


.. function:: python_implementation()

   Trả về một chuỗi cho biết Python implementation. Các giá trị có thể trả về là: 'CPython', 'IronPython', 'Jython', 'PyPy'.


.. function:: python_revision()

   Trả về một chuỗi cho biết revision SCM của Python implementation.


.. function:: python_version()

   Trả về phiên bản Python dưới dạng chuỗi ``'major.minor.patchlevel'``.

   Lưu ý rằng, không giống ``sys.version`` của Python, giá trị trả về luôn bao gồm patchlevel (mặc định là 0).


.. function:: python_version_tuple()

   Trả về phiên bản Python dưới dạng tuple ``(major, minor, patchlevel)`` gồm các chuỗi.

   Lưu ý rằng, không giống ``sys.version`` của Python, giá trị trả về luôn bao gồm patchlevel (mặc định là ``'0'``).


.. function:: release()

   Trả về bản phát hành của hệ thống, chẳng hạn như ``'2.2.0'`` hoặc ``'NT'``. Nếu không thể xác định giá trị, một chuỗi rỗng sẽ được trả về.

   Trên iOS và Android, đây là bản phát hành hệ điều hành dành cho người dùng. Để lấy bản phát hành kernel Darwin hoặc Linux, hãy sử dụng :func:`os.uname`.

.. function:: system()

   Trả về tên hệ thống/hệ điều hành, chẳng hạn như ``'Linux'``, ``'Darwin'``, ``'Java'``, ``'Windows'``. Nếu không thể xác định giá trị, một chuỗi rỗng sẽ được trả về.

   Trên iOS và Android, giá trị này trả về tên hệ điều hành dành cho người dùng (tức là ``'iOS``, ``'iPadOS'`` hoặc ``'Android'``). Để lấy tên kernel (``'Darwin'`` hoặc ``'Linux'``), hãy sử dụng :func:`os.uname`.

.. function:: system_alias(system, release, version)

   Trả về ``(system, release, version)`` được đặt bí danh theo các tên tiếp thị phổ biến được sử dụng cho một số hệ thống. Trong một số trường hợp, hàm cũng sắp xếp lại thông tin để tránh gây nhầm lẫn.


.. function:: version()

   Trả về phiên bản phát hành của hệ thống, ví dụ: ``'#3 on degas'``. Trả về một chuỗi rỗng nếu không thể xác định giá trị.

.. function:: uname()

   Giao diện uname tương đối khả chuyển. Trả về một :func:`~collections.namedtuple` chứa sáu thuộc tính: :attr:`system`, :attr:`node`, :attr:`release`,
   :attr:`version`, :attr:`machine` và :attr:`processor`.

   :attr:`processor` được phân giải trễ, khi có yêu cầu.

   Lưu ý: tên của hai thuộc tính đầu tiên khác với các tên được trình bày bởi
   :func:`os.uname`, trong đó chúng được đặt tên là :attr:`!sysname` và
   :attr:`!nodename`.

   Các mục không thể xác định được đặt thành ``''``.

   .. versionchanged:: 3.3
      Kết quả đã thay đổi từ một tuple thành một :func:`~collections.namedtuple`.

   .. versionchanged:: 3.9
      :attr:`processor` is resolved late instead of immediately.

.. function:: invalidate_caches()

   Xóa bộ nhớ đệm nội bộ chứa thông tin, chẳng hạn như :func:`uname`. Điều này thường hữu ích khi :func:`node` của nền tảng bị một tiến trình bên ngoài thay đổi và cần lấy giá trị đã cập nhật.

   .. versionadded:: 3.14


Nền tảng Java
-------------


.. function:: java_ver(release='', vendor='', vminfo=('','',''), osinfo=('','',''))

   Giao diện phiên bản cho Jython.

   Trả về một tuple ``(release, vendor, vminfo, osinfo)`` với *vminfo* là một tuple ``(vm_name, vm_release, vm_vendor)`` và *osinfo* là một tuple ``(os_name, os_version, os_arch)``. Các giá trị không thể xác định được đặt thành các giá trị mặc định được cung cấp dưới dạng tham số (tất cả đều mặc định là ``''``).

   .. deprecated-removed:: 3.13 3.15
      Nó hầu như chưa được kiểm thử, có API khó hiểu và chỉ hữu ích cho việc hỗ trợ Jython.


Nền tảng Windows
----------------


.. function:: win32_ver(release='', version='', csd='', ptype='')

   Lấy thêm thông tin phiên bản từ Windows Registry và trả về một tuple ``(release, version, csd, ptype)`` chứa bản phát hành hệ điều hành, số phiên bản, cấp độ CSD (service pack) và loại hệ điều hành (đa bộ xử lý/đơn bộ xử lý). Các giá trị không thể xác định sẽ được đặt thành các giá trị mặc định được cung cấp dưới dạng tham số (tất cả đều mặc định là chuỗi rỗng).

   Gợi ý: *ptype* là ``'Uniprocessor Free'`` trên các máy NT dùng một bộ xử lý và là ``'Multiprocessor Free'`` trên các máy dùng nhiều bộ xử lý. ``'Free'`` cho biết phiên bản hệ điều hành không chứa mã gỡ lỗi. Giá trị này cũng có thể là ``'Checked'``, nghĩa là phiên bản hệ điều hành sử dụng mã gỡ lỗi, tức mã kiểm tra các đối số, phạm vi, v.v.

.. function:: win32_edition()

   Trả về một chuỗi biểu thị phiên bản Windows hiện tại hoặc ``None`` nếu không thể xác định giá trị. Các giá trị có thể bao gồm nhưng không giới hạn ở ``'Enterprise'``, ``'IoTUAP'``, ``'ServerStandard'`` và ``'nanoserver'``.

   .. versionadded:: 3.8

.. function:: win32_is_iot()

   Trả về ``True`` nếu phiên bản Windows được :func:`win32_edition` trả về được nhận diện là phiên bản IoT.

   .. versionadded:: 3.8


Nền tảng macOS
--------------

.. function:: mac_ver(release='', versioninfo=('','',''), machine='')

   Lấy thông tin phiên bản macOS và trả về dưới dạng tuple ``(release, versioninfo, machine)``, trong đó *versioninfo* là một tuple ``(version, dev_stage, non_release_version)``.

   Các mục không thể xác định được sẽ được đặt thành ``''``. Tất cả các mục của tuple đều là chuỗi.

Nền tảng iOS
------------

.. function:: ios_ver(system='', release='', model='', is_simulator=False)

   Lấy thông tin phiên bản iOS và trả về dưới dạng một
   :func:`~collections.namedtuple` với các thuộc tính sau:

   * ``system`` là tên hệ điều hành; có thể là ``'iOS'`` hoặc ``'iPadOS'``.
   * ``release`` là số phiên bản iOS dưới dạng chuỗi (ví dụ: ``'17.2'``).
   * ``model`` là mã định danh kiểu thiết bị; đây sẽ là một chuỗi như ``'iPhone13,2'`` đối với thiết bị thật hoặc ``'iPhone'`` trên trình mô phỏng.
   * ``is_simulator`` là một boolean mô tả liệu ứng dụng đang chạy trên simulator hay thiết bị vật lý.

   Các mục không thể xác định sẽ được đặt thành các giá trị mặc định được cung cấp dưới dạng tham số.


Các nền tảng Unix
-----------------

.. function:: libc_ver(executable=sys.executable, lib='', version='', chunksize=16384)

   Cố gắng xác định phiên bản libc mà file executable (mặc định là trình thông dịch Python) được liên kết với. Trả về một tuple gồm các chuỗi ``(lib, version)``, mặc định là các tham số đã cho nếu việc tra cứu không thành công.

   Lưu ý rằng hàm này hiểu rất rõ cách các phiên bản libc khác nhau thêm symbol vào executable và có lẽ chỉ có thể sử dụng cho các executable được biên dịch bằng :program:`gcc`.

   File được đọc và quét theo từng phần có kích thước *chunksize* byte.


Các nền tảng Linux
------------------

.. function:: freedesktop_os_release()

   Lấy thông tin nhận dạng hệ điều hành từ tệp ``os-release`` và trả về dưới dạng dict. Tệp ``os-release`` là `tiêu chuẩn freedesktop.org <https://www.freedesktop.org/software/systemd/man/os-release.html>`_ và có sẵn trong hầu hết các bản phân phối Linux. Android và các bản phân phối dựa trên Android là ngoại lệ đáng chú ý.

   Gây ra :exc:`OSError` hoặc lớp con của nó khi không thể đọc ``/etc/os-release`` và ``/usr/lib/os-release``.

   Khi thành công, hàm trả về một dictionary trong đó các khóa và giá trị đều là chuỗi. Các ký tự đặc biệt trong giá trị, chẳng hạn như ``"`` và ``$``, không được đặt trong dấu ngoặc kép. Các trường ``NAME``, ``ID`` và ``PRETTY_NAME`` luôn được định nghĩa theo tiêu chuẩn. Tất cả các trường khác là tùy chọn. Nhà cung cấp có thể bổ sung các trường khác.

   Lưu ý rằng các trường như ``NAME``, ``VERSION`` và ``VARIANT`` là các chuỗi phù hợp để hiển thị cho người dùng. Chương trình nên sử dụng các trường như ``ID``, ``ID_LIKE``, ``VERSION_ID`` hoặc ``VARIANT_ID`` để xác định các bản phân phối Linux.

   Ví dụ::

      def get_like_distro():
          info = platform.freedesktop_os_release()
          ids = [info["ID"]]
          if "ID_LIKE" in info:
              # các id được phân tách bằng dấu cách và sắp xếp theo độ ưu tiên
              ids.extend(info["ID_LIKE"].split())
          return ids

   .. versionadded:: 3.10


Nền tảng Android
----------------

.. function:: android_ver(release="", api_level=0, manufacturer="", \
                          model="", device="", is_emulator=False)

   Lấy thông tin thiết bị Android. Trả về một :func:`~collections.namedtuple` với các thuộc tính sau. Những giá trị không thể xác định được sẽ được đặt thành các giá trị mặc định được cung cấp dưới dạng tham số.

   * ``release`` - phiên bản Android, dưới dạng chuỗi (ví dụ: ``"14"``).

   * ``api_level`` - API level của thiết bị đang chạy, dưới dạng số nguyên (ví dụ: ``34`` cho Android 14). Để lấy API level mà Python được build dựa trên đó, hãy xem
     :func:`sys.getandroidapilevel`.

   * ``manufacturer`` - `Tên nhà sản xuất <https://developer.android.com/reference/android/os/Build#MANUFACTURER>`__.

   * ``model`` - `Tên model <https://developer.android.com/reference/android/os/Build#MODEL>`__ – thường là tên thương mại hoặc số model.

   * ``device`` - `Tên thiết bị <https://developer.android.com/reference/android/os/Build#DEVICE>`__ – thường là số model hoặc tên mã.

   * ``is_emulator`` - ``True`` nếu thiết bị là emulator; ``False`` nếu đó là thiết bị vật lý.

   Google duy trì `danh sách các tên model và thiết bị đã biết <https://storage.googleapis.com/play_public/supported_devices.html>`__.

   .. versionadded:: 3.13

.. _platform-cli:

Cách sử dụng trên dòng lệnh
---------------------------

:mod:`!platform` cũng có thể được gọi trực tiếp bằng switch :option:`-m` của interpreter::

   python -m platform [--terse] [--nonaliased] [{nonaliased,terse} ...]

Các tùy chọn sau được chấp nhận:

.. program:: platform

.. option:: --terse

   In thông tin ngắn gọn về platform. Tương đương với việc gọi :func:`platform.platform` với đối số *terse* được đặt thành ``True``.

.. option:: --nonaliased

   In thông tin về platform mà không bí danh hóa tên system/OS. Tương đương với việc gọi :func:`platform.platform` với đối số *aliased* được đặt thành ``True``.

Bạn cũng có thể truyền một hoặc nhiều đối số vị trí (``terse``, ``nonaliased``) để kiểm soát rõ ràng định dạng đầu ra. Các đối số này hoạt động tương tự như những tùy chọn tương ứng.

.. _`freedesktop.org standard`: https://www.freedesktop.org/software/systemd/man/os-release.html
