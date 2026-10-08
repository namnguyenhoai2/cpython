:mod:`!venv` --- Tạo môi trường ảo
==================================

.. module:: venv
   :synopsis: Tạo môi trường ảo.

.. moduleauthor:: Vinay Sajip <vinay_sajip@yahoo.co.uk>
.. sectionauthor:: Vinay Sajip <vinay_sajip@yahoo.co.uk>

.. versionadded:: 3.3

**Mã nguồn:** :source:`Lib/venv/`

.. index:: pair: Environments; virtual

--------------

.. _venv-def:
.. _venv-intro:

Mô-đun :mod:`!venv` hỗ trợ tạo các "môi trường ảo" nhẹ, mỗi môi trường có một tập gói Python độc lập được cài đặt trong các thư mục :mod:`site` của riêng chúng. Một môi trường ảo được tạo dựa trên một bản cài đặt Python hiện có, được gọi là Python "cơ sở" của môi trường ảo, và theo mặc định được tách biệt khỏi các gói trong môi trường cơ sở, vì vậy chỉ những gói được cài đặt rõ ràng trong môi trường ảo mới khả dụng. Xem :ref:`sys-path-init-virtual-environments` và :mod:`site` của
:ref:`tài liệu về môi trường ảo <site-virtual-environments-configuration>` để biết thêm thông tin.

Khi được sử dụng bên trong một môi trường ảo, các công cụ cài đặt phổ biến như
:pypi:`pip` sẽ cài đặt các gói Python vào một môi trường ảo mà không cần được yêu cầu thực hiện việc đó một cách rõ ràng.

Môi trường ảo có những đặc điểm sau (ngoài ra còn có):

* Được dùng để chứa một Python interpreter cụ thể cùng các thư viện và binary cần thiết để hỗ trợ một dự án (library hoặc application). Theo mặc định, chúng được cách ly với phần mềm trong các môi trường ảo khác, cũng như với các Python interpreter và thư viện được cài đặt trong hệ điều hành.

* Được chứa trong một thư mục, theo quy ước được đặt tên là ``.venv`` hoặc ``venv`` trong thư mục dự án, hoặc bên dưới một thư mục chứa nhiều môi trường ảo, chẳng hạn như ``~/.virtualenvs``.

* Không được đưa vào các hệ thống quản lý source control như Git.

* Được xem là có thể loại bỏ -- việc xóa và tạo lại từ đầu phải đơn giản. Bạn không đặt bất kỳ code dự án nào trong môi trường này.

* Không được xem là có thể di chuyển hoặc sao chép -- bạn chỉ cần tạo lại cùng một môi trường tại vị trí đích.

Xem :pep:`405` để biết thêm thông tin cơ bản về các môi trường ảo Python.

.. seealso::

   `Hướng dẫn sử dụng Python Packaging: Tạo và sử dụng môi trường ảo <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments>`__

.. include:: ../includes/wasm-mobile-notavail.rst

Tạo môi trường ảo
-----------------

:ref:`Môi trường ảo <venv-def>` được tạo bằng cách thực thi module ``venv``:

.. code-block:: shell

    python -m venv /path/to/new/virtual/environment

Thao tác này tạo thư mục đích (bao gồm các thư mục cha nếu cần) và đặt một tệp :file:`pyvenv.cfg` vào đó với khóa ``home`` trỏ đến bản cài đặt Python mà từ đó lệnh được chạy. Thao tác này cũng tạo một thư mục con :file:`bin` (hoặc :file:`Scripts` trên Windows) chứa một bản sao hoặc symlink của tệp thực thi Python (tùy theo nền tảng hoặc các đối số được sử dụng tại thời điểm tạo môi trường). Thao tác này cũng tạo một thư mục con :file:`lib/pythonX.Y/site-packages` (trên Windows, đây là :file:`Lib\\site-packages`). Nếu chỉ định một thư mục hiện có, thư mục đó sẽ được sử dụng lại.

.. versionchanged:: 3.5
   Hiện nay, việc sử dụng ``venv`` được khuyến nghị để tạo môi trường ảo.

.. deprecated-removed:: 3.6 3.8
   :program:`pyvenv` was the recommended tool for creating virtual environments
   cho Python 3.3 và 3.4, và được thay thế trong 3.5 bằng cách thực thi trực tiếp ``venv``.

.. highlight:: none

Trên Windows, gọi lệnh ``venv`` như sau:

.. code-block:: ps1con

   PS> python -m venv C:\path\to\new\virtual\environment

Lệnh này, nếu được chạy với ``-h``, sẽ hiển thị các tùy chọn khả dụng::

   usage: venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear]
               [--upgrade] [--without-pip] [--prompt PROMPT] [--upgrade-deps]
               [--without-scm-ignore-files]
               ENV_DIR [ENV_DIR ...]

   Creates virtual Python environments in one or more target directories.

   Once an environment has been created, you may wish to activate it, e.g. by
   sourcing an activate script in its bin directory.

.. _venv-cli:
.. program:: venv

.. option:: ENV_DIR

   Đối số bắt buộc chỉ định thư mục sẽ được dùng để tạo môi trường.

.. option:: --system-site-packages

   Cho phép môi trường ảo truy cập thư mục site-packages của hệ thống.

.. option:: --symlinks

   Cố gắng sử dụng symlink thay vì bản sao khi symlink không phải là mặc định trên nền tảng.

.. option:: --copies

   Cố gắng sử dụng bản sao thay vì symlink, ngay cả khi symlink là mặc định trên nền tảng.

.. option:: --clear

   Xóa nội dung của thư mục môi trường nếu thư mục đó đã tồn tại trước khi tạo môi trường.

.. option:: --upgrade

   Nâng cấp thư mục môi trường để sử dụng phiên bản Python này, với giả định Python đã được nâng cấp tại chỗ.

.. option:: --without-pip

   Bỏ qua việc cài đặt hoặc nâng cấp pip trong môi trường ảo (pip được bootstrap theo mặc định).

.. option:: --prompt <PROMPT>

   Cung cấp tiền tố prompt thay thế cho môi trường này.

.. option:: --upgrade-deps

   Nâng cấp các dependency cốt lõi (pip) lên phiên bản mới nhất trên PyPI.

.. option:: --without-scm-ignore-files

   Bỏ qua việc thêm các tệp ignore của SCM vào thư mục môi trường (Git được hỗ trợ theo mặc định).


.. versionchanged:: 3.4
   Cài đặt pip theo mặc định, đồng thời bổ sung các tùy chọn ``--without-pip`` và ``--copies``.

.. versionchanged:: 3.4
   Trong các phiên bản trước, nếu thư mục đích đã tồn tại thì sẽ phát sinh lỗi, trừ khi cung cấp tùy chọn ``--clear`` hoặc ``--upgrade``.

.. versionchanged:: 3.9
   Thêm tùy chọn ``--upgrade-deps`` để nâng cấp pip + setuptools lên phiên bản mới nhất trên PyPI.

.. versionchanged:: 3.12

   ``setuptools`` không còn là dependency cốt lõi của venv.

.. versionchanged:: 3.13

   Đã thêm tùy chọn ``--without-scm-ignore-files``.
.. versionchanged:: 3.13
   ``venv`` hiện tạo tệp :file:`.gitignore` cho Git theo mặc định.

.. note::
   Mặc dù symlink được hỗ trợ trên Windows, chúng không được khuyến nghị. Đáng lưu ý là việc nhấp đúp vào ``python.exe`` trong File Explorer sẽ phân giải symlink ngay lập tức và bỏ qua môi trường ảo.

.. note::
   Trên Microsoft Windows, bạn có thể cần bật script ``Activate.ps1`` bằng cách đặt execution policy cho người dùng. Bạn có thể thực hiện việc này bằng cách chạy lệnh PowerShell sau:

   .. code-block:: powershell

      PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

   Xem `About Execution Policies <https://go.microsoft.com/fwlink/?LinkID=135170>`_ để biết thêm thông tin.

Tệp :file:`pyvenv.cfg` được tạo cũng bao gồm khóa ``include-system-site-packages``, được đặt thành ``true`` nếu ``venv`` được chạy với tùy chọn ``--system-site-packages``, và ``false`` trong các trường hợp khác.

Trừ khi cung cấp tùy chọn ``--without-pip``, :mod:`ensurepip` sẽ được gọi để khởi tạo ``pip`` trong môi trường ảo.

Có thể cung cấp nhiều đường dẫn cho ``venv``; khi đó, một môi trường ảo giống hệt nhau sẽ được tạo theo các tùy chọn đã cho tại mỗi đường dẫn được cung cấp.

.. _venv-explanation:

Cách venv hoạt động
-------------------

Khi một trình thông dịch Python đang chạy từ môi trường ảo,
:data:`sys.prefix` và :data:`sys.exec_prefix` trỏ đến các thư mục của môi trường ảo, trong khi :data:`sys.base_prefix` và :data:`sys.base_exec_prefix` trỏ đến các thư mục của Python cơ sở được dùng để tạo môi trường. Chỉ cần kiểm tra ``sys.prefix != sys.base_prefix`` là đủ để xác định trình thông dịch hiện tại có đang chạy từ môi trường ảo hay không.

Một môi trường ảo có thể được "kích hoạt" bằng một script trong thư mục binary của nó (``bin`` trên POSIX; ``Scripts`` trên Windows). Thao tác này sẽ thêm thư mục đó vào đầu :envvar:`PATH`, để khi chạy
:program:`python`, trình thông dịch Python của môi trường sẽ được gọi và bạn có thể chạy các script đã cài đặt mà không cần sử dụng đường dẫn đầy đủ của chúng. Cách gọi activation script phụ thuộc vào nền tảng (:samp:`{<venv>}` phải được thay thế bằng đường dẫn đến thư mục chứa môi trường ảo):

+-------------+------------+--------------------------------------------------+
| Platform    | Shell      | Command to activate virtual environment          |
+=============+============+==================================================+
| POSIX       | bash/zsh   | :samp:`$ source {<venv>}/bin/activate`           |
|             +------------+--------------------------------------------------+
|             | fish       | :samp:`$ source {<venv>}/bin/activate.fish`      |
|             +------------+--------------------------------------------------+
|             | csh/tcsh   | :samp:`$ source {<venv>}/bin/activate.csh`       |
|             +------------+--------------------------------------------------+
|             | pwsh       | :samp:`$ {<venv>}/bin/Activate.ps1`              |
+-------------+------------+--------------------------------------------------+
| Windows     | cmd.exe    | :samp:`C:\\> {<venv>}\\Scripts\\activate.bat`    |
|             +------------+--------------------------------------------------+
|             | PowerShell | :samp:`PS C:\\> {<venv>}\\Scripts\\Activate.ps1` |
+-------------+------------+--------------------------------------------------+

.. versionadded:: 3.4
   :program:`fish` and :program:`csh` activation scripts.

.. versionadded:: 3.8
   Các tập lệnh kích hoạt PowerShell được cài đặt trên POSIX để hỗ trợ PowerShell Core.

Bạn không nhất thiết *cần* kích hoạt một môi trường ảo, vì bạn chỉ cần chỉ định đường dẫn đầy đủ đến trình thông dịch Python của môi trường đó khi gọi Python. Hơn nữa, tất cả các tập lệnh được cài đặt trong môi trường đều có thể chạy mà không cần kích hoạt môi trường.

Để thực hiện điều này, các tập lệnh được cài đặt vào môi trường ảo có một dòng "shebang" trỏ đến trình thông dịch Python của môi trường đó,
:samp:`#!/{<path-to-venv>}/bin/python`. Điều này có nghĩa là tập lệnh sẽ chạy bằng trình thông dịch đó bất kể giá trị của :envvar:`PATH`. Trên Windows, việc xử lý dòng "shebang" được hỗ trợ nếu bạn đã cài đặt :ref:`launcher`. Do đó, việc nhấp đúp vào một tập lệnh đã cài đặt trong cửa sổ Windows Explorer sẽ chạy tập lệnh đó bằng trình thông dịch chính xác mà không cần kích hoạt môi trường hoặc đưa môi trường vào :envvar:`PATH`.

Khi một môi trường ảo được kích hoạt, biến môi trường :envvar:`!VIRTUAL_ENV` được đặt thành đường dẫn của môi trường đó. Vì không bắt buộc phải kích hoạt rõ ràng một môi trường ảo để sử dụng nó,
không thể dựa vào :envvar:`!VIRTUAL_ENV` để xác định liệu một môi trường ảo có đang được sử dụng hay không.

.. warning:: Vì các tập lệnh được cài đặt trong môi trường không nên giả định rằng môi trường đã được kích hoạt, các dòng shebang của chúng chứa đường dẫn tuyệt đối đến các trình thông dịch trong môi trường. Vì vậy, xét trong trường hợp tổng quát, các môi trường vốn không có tính di động. Bạn luôn nên có một cách đơn giản để tạo lại môi trường (ví dụ: nếu bạn có tệp requirements ``requirements.txt``, bạn có thể gọi ``pip install -r requirements.txt`` bằng ``pip`` của môi trường để cài đặt tất cả các gói mà môi trường cần). Nếu vì bất kỳ lý do nào bạn cần di chuyển môi trường đến một vị trí mới, hãy tạo lại môi trường tại vị trí mong muốn và xóa môi trường ở vị trí cũ. Nếu bạn di chuyển môi trường vì đã di chuyển thư mục cha của nó, hãy tạo lại môi trường ở vị trí mới. Nếu không, phần mềm được cài đặt vào môi trường có thể không hoạt động như mong đợi.

Bạn có thể hủy kích hoạt một môi trường ảo bằng cách nhập ``deactivate`` trong shell. Cơ chế chính xác phụ thuộc vào nền tảng và là một chi tiết triển khai nội bộ (thông thường, một script hoặc hàm shell sẽ được sử dụng).


.. _venv-api:

API
---

.. highlight:: python

Phương thức cấp cao được mô tả ở trên sử dụng một API đơn giản, cung cấp các cơ chế để những bên thứ ba tạo môi trường ảo có thể tùy chỉnh việc tạo môi trường theo nhu cầu của họ, thông qua lớp :class:`EnvBuilder`.

.. class:: EnvBuilder(system_site_packages=False, clear=False, \
                      symlinks=False, upgrade=False, with_pip=False, \ prompt=None, upgrade_deps=False, \ *, scm_ignore_files=frozenset()

    Lớp :class:`EnvBuilder` chấp nhận các đối số keyword sau khi khởi tạo:

    * *system_site_packages* -- một giá trị boolean cho biết các site-packages của Python hệ thống có khả dụng trong môi trường hay không (mặc định là ``False``).

    * *clear* -- một giá trị boolean mà nếu là true sẽ xóa nội dung của mọi thư mục đích hiện có trước khi tạo môi trường.

    * *symlinks* -- một giá trị boolean cho biết có thử tạo symlink cho binary Python thay vì sao chép hay không.

    * *upgrade* -- một giá trị boolean mà nếu là true sẽ nâng cấp một environment hiện có bằng Python đang chạy - dùng khi Python đó đã được nâng cấp tại chỗ (mặc định là ``False``).

    * *with_pip* -- một giá trị boolean mà nếu là true sẽ đảm bảo pip được cài đặt trong virtual environment. Tùy chọn này sử dụng :mod:`ensurepip` với tùy chọn ``--default-pip``.

    * *prompt* -- một chuỗi được sử dụng sau khi virtual environment được kích hoạt (mặc định là ``None``, nghĩa là tên thư mục của environment sẽ được sử dụng). Nếu cung cấp chuỗi đặc biệt ``"."``, tên cơ sở của thư mục hiện tại sẽ được sử dụng làm prompt.

    * *upgrade_deps* -- Cập nhật các module venv cơ sở lên phiên bản mới nhất trên PyPI

    * *scm_ignore_files* -- Tạo các tệp ignore dựa trên những source control manager (SCM) được chỉ định trong iterable. Tính năng hỗ trợ được xác định bằng cách có một phương thức tên là ``create_{scm}_ignore_file``. Giá trị duy nhất được hỗ trợ theo mặc định là ``"git"`` thông qua :meth:`create_git_ignore_file`.


    .. versionchanged:: 3.4
       Đã thêm tham số ``with_pip``

    .. versionchanged:: 3.6
       Đã thêm tham số ``prompt``

    .. versionchanged:: 3.9
       Đã thêm tham số ``upgrade_deps``

    .. versionchanged:: 3.13
       Đã thêm tham số ``scm_ignore_files``

    :class:`EnvBuilder` có thể được sử dụng làm lớp cơ sở.

    .. method:: create(env_dir)

        Tạo một môi trường ảo bằng cách chỉ định thư mục đích (đường dẫn tuyệt đối hoặc tương đối so với thư mục hiện tại) để chứa môi trường ảo. Phương thức ``create`` sẽ tạo môi trường trong thư mục được chỉ định hoặc phát sinh ngoại lệ phù hợp.

        Phương thức ``create`` của lớp :class:`EnvBuilder` minh họa các hook có sẵn để tùy chỉnh lớp con::

            def create(self, env_dir):
                """
                Create a virtualized Python environment in a directory.
                env_dir is the target directory to create an environment in.
                """
                env_dir = os.path.abspath(env_dir)
                context = self.ensure_directories(env_dir)
                self.create_configuration(context)
                self.setup_python(context)
                self.setup_scripts(context)
                self.post_setup(context)

        Mỗi phương thức :meth:`ensure_directories`,
        :meth:`create_configuration`, :meth:`setup_python`,
        :meth:`setup_scripts` và :meth:`post_setup` có thể được ghi đè.

    .. method:: ensure_directories(env_dir)

        Tạo thư mục environment và tất cả thư mục con cần thiết chưa tồn tại, đồng thời trả về một đối tượng context. Đối tượng context này chỉ là nơi lưu giữ các thuộc tính (chẳng hạn như các đường dẫn) để các phương thức khác sử dụng. Nếu :class:`EnvBuilder` được tạo với đối số ``clear=True``, nội dung của thư mục environment sẽ được xóa, sau đó tất cả thư mục con cần thiết sẽ được tạo lại.

        Đối tượng context được trả về là một :class:`types.SimpleNamespace` với các thuộc tính sau:

        * ``env_dir`` - Vị trí của virtual environment. Được dùng cho ``__VENV_DIR__`` trong các activation script (xem :meth:`install_scripts`).

        * ``env_name`` - Tên của virtual environment. Được dùng cho ``__VENV_NAME__`` trong các activation script (xem :meth:`install_scripts`).

        * ``prompt`` - Prompt được các activation script sử dụng. Được dùng cho ``__VENV_PROMPT__`` trong các activation script (xem :meth:`install_scripts`).

        * ``executable`` - Python executable nền tảng được virtual environment sử dụng. Điều này учиты đến trường hợp virtual environment được tạo từ một virtual environment khác.

        * ``inc_path`` - Đường dẫn include cho môi trường ảo.

        * ``lib_path`` - Đường dẫn purelib cho môi trường ảo.

        * ``bin_path`` - Đường dẫn script cho môi trường ảo.

        * ``bin_name`` - Tên của đường dẫn script tương đối so với vị trí môi trường ảo. Được sử dụng cho ``__VENV_BIN_NAME__`` trong các activation script (xem :meth:`install_scripts`).

        * ``env_exe`` - Tên của trình thông dịch Python trong môi trường ảo. Được sử dụng cho ``__VENV_PYTHON__`` trong các activation script (xem :meth:`install_scripts`).

        * ``env_exec_cmd`` - Tên của trình thông dịch Python, có tính đến các chuyển hướng của hệ thống tệp. Có thể dùng tên này để chạy Python trong môi trường ảo.


        .. versionchanged:: 3.11
           *venv*
           :ref:`lược đồ cài đặt sysconfig <installation_paths>` được sử dụng để tạo các đường dẫn của những thư mục được tạo.

        .. versionchanged:: 3.12
           Thuộc tính ``lib_path`` đã được thêm vào context và đối tượng context đã được ghi tài liệu.

    .. method:: create_configuration(context)

        Tạo tệp cấu hình ``pyvenv.cfg`` trong environment.

    .. method:: setup_python(context)

        Tạo một bản sao hoặc symlink đến Python executable trong environment. Trên các hệ thống POSIX, nếu một executable cụ thể ``python3.x`` được sử dụng, các symlink đến ``python`` và ``python3`` sẽ được tạo và trỏ đến executable đó, trừ khi các tệp có những tên đó đã tồn tại.

    .. method:: setup_scripts(context)

        Cài đặt các activation script phù hợp với nền tảng vào virtual environment.

    .. method:: upgrade_dependencies(context)

       Nâng cấp các gói dependency cốt lõi của venv (hiện là :pypi:`pip`) trong environment. Việc này được thực hiện bằng cách gọi executable ``pip`` trong environment từ shell.

       .. versionadded:: 3.9
       .. versionchanged:: 3.12

          :pypi:`setuptools` không còn là dependency cốt lõi của venv.

    .. method:: post_setup(context)

        Một phương thức giữ chỗ có thể được ghi đè trong các triển khai của bên thứ ba để cài đặt trước các gói vào virtual environment hoặc thực hiện các bước khác sau khi tạo.

    .. method:: install_scripts(context, path)

        Phương thức này có thể được gọi từ :meth:`setup_scripts` hoặc :meth:`post_setup` trong các lớp con để hỗ trợ cài đặt các script tùy chỉnh vào virtual environment.

        *path* là đường dẫn đến một thư mục chứa các thư mục con ``common``, ``posix``, ``nt``; mỗi thư mục chứa các script dành cho thư mục ``bin`` trong environment. Nội dung của ``common`` và thư mục tương ứng với :data:`os.name` được sao chép sau khi thực hiện một số thay thế văn bản cho các placeholder:

        * ``__VENV_DIR__`` được thay thế bằng đường dẫn tuyệt đối của thư mục environment.

        * ``__VENV_NAME__`` được thay thế bằng tên environment (phần đường dẫn cuối cùng của thư mục environment).

        * ``__VENV_PROMPT__`` được thay thế bằng prompt (tên environment được đặt trong dấu ngoặc đơn và theo sau là một khoảng trắng).

        * ``__VENV_BIN_NAME__`` được thay thế bằng tên của thư mục bin (either ``bin`` hoặc ``Scripts``).

        * ``__VENV_PYTHON__`` được thay thế bằng đường dẫn tuyệt đối của tệp thực thi trong môi trường.

        Các thư mục được phép tồn tại (trong trường hợp một môi trường hiện có đang được nâng cấp).

    .. method:: create_git_ignore_file(context)

       Tạo một tệp ``.gitignore`` בתוך môi trường ảo, khiến toàn bộ thư mục bị trình quản lý kiểm soát mã nguồn Git bỏ qua.

       .. versionadded:: 3.13

    .. versionchanged:: 3.7.2
       Windows hiện sử dụng các script redirector cho ``python[w].exe`` thay vì sao chép các tệp nhị phân thực tế. Trong 3.7.2, chỉ :meth:`setup_python` không thực hiện gì trừ khi chạy từ một bản build trong cây mã nguồn.

    .. versionchanged:: 3.7.3
       Windows sao chép các script redirector như một phần của :meth:`setup_python` thay vì :meth:`setup_scripts`. Điều này không đúng trong 3.7.2. Khi sử dụng symlink, các tệp thực thi gốc sẽ được liên kết.

Ngoài ra còn có một hàm tiện ích ở cấp module:

.. function:: create(env_dir, system_site_packages=False, clear=False, \
                     symlinks=False, with_pip=False, prompt=None, \ upgrade_deps=False, *, scm_ignore_files=frozenset()

    Tạo một :class:`EnvBuilder` với các đối số từ khóa đã cho và gọi
    phương thức :meth:`~EnvBuilder.create` với đối số *env_dir*.

    .. versionadded:: 3.3

    .. versionchanged:: 3.4
       Đã thêm tham số *with_pip*

    .. versionchanged:: 3.6
       Đã thêm tham số *prompt*

    .. versionchanged:: 3.9
       Đã thêm tham số *upgrade_deps*

    .. versionchanged:: 3.13
       Đã thêm tham số *scm_ignore_files*

Ví dụ về việc mở rộng ``EnvBuilder``
------------------------------------

Script sau đây minh họa cách mở rộng :class:`EnvBuilder` bằng cách triển khai một lớp con để cài đặt setuptools và pip vào virtual environment được tạo::

    import os
    import os.path
    from subprocess import Popen, PIPE
    import sys
    from threading import Thread
    from urllib.parse import urlsplit
    from urllib.request import urlretrieve
    import venv

    class ExtendedEnvBuilder(venv.EnvBuilder):
        """
        This builder installs setuptools and pip so that you can pip or
        easy_install other packages into the created virtual environment.

        :param nodist: If true, setuptools and pip are not installed into the
                       created virtual environment.
        :param nopip: If true, pip is not installed into the created
                      virtual environment.
        :param progress: If setuptools or pip are installed, the progress of the
                         installation can be monitored by passing a progress
                         callable. If specified, it is called with two
                         arguments: a string indicating some progress, and a
                         context indicating where the string is coming from.
                         The context argument can have one of three values:
                         'main', indicating that it is called from virtualize()
                         itself, and 'stdout' and 'stderr', which are obtained
                         by reading lines from the output streams of a subprocess
                         which is used to install the app.

                         If a callable is not specified, default progress
                         information is output to sys.stderr.
        """

        def __init__(self, *args, **kwargs):
            self.nodist = kwargs.pop('nodist', False)
            self.nopip = kwargs.pop('nopip', False)
            self.progress = kwargs.pop('progress', None)
            self.verbose = kwargs.pop('verbose', False)
            super().__init__(*args, **kwargs)

        def post_setup(self, context):
            """
            Set up any packages which need to be pre-installed into the
            virtual environment being created.

            :param context: The information for the virtual environment
                            creation request being processed.
            """
            os.environ['VIRTUAL_ENV'] = context.env_dir
            if not self.nodist:
                self.install_setuptools(context)
            # Không thể cài đặt pip nếu không có setuptools
            if not self.nopip and not self.nodist:
                self.install_pip(context)

        def reader(self, stream, context):
            """
            Read lines from a subprocess' output stream and either pass to a progress
            callable (if specified) or write progress information to sys.stderr.
            """
            progress = self.progress
            while True:
                s = stream.readline()
                if not s:
                    break
                if progress is not None:
                    progress(s, context)
                else:
                    if not self.verbose:
                        sys.stderr.write('.')
                    else:
                        sys.stderr.write(s.decode('utf-8'))
                    sys.stderr.flush()
            stream.close()

        def install_script(self, context, name, url):
            _, _, path, _, _ = urlsplit(url)
            fn = os.path.split(path)[-1]
            binpath = context.bin_path
            distpath = os.path.join(binpath, fn)
            # Tải script vào thư mục binaries của virtual environment
            urlretrieve(url, distpath)
            progress = self.progress
            if self.verbose:
                term = '\n'
            else:
                term = ''
            if progress is not None:
                progress('Installing %s ...%s' % (name, term), 'main')
            else:
                sys.stderr.write('Installing %s ...%s' % (name, term))
                sys.stderr.flush()
            # Cài đặt trong virtual environment
            args = [context.env_exe, fn]
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
            t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
            t1.start()
            t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
            t2.start()
            p.wait()
            t1.join()
            t2.join()
            if progress is not None:
                progress('done.', 'main')
            else:
                sys.stderr.write('done.\n')
            # Dọn dẹp - không còn cần thiết nữa
            os.unlink(distpath)

        def install_setuptools(self, context):
            """
            Install setuptools in the virtual environment.

            :param context: The information for the virtual environment
                            creation request being processed.
            """
            url = "https://bootstrap.pypa.io/ez_setup.py"
            self.install_script(context, 'setuptools', url)
            # xóa archive setuptools đã được tải xuống
            pred = lambda o: o.startswith('setuptools-') and o.endswith('.tar.gz')
            files = filter(pred, os.listdir(context.bin_path))
            for f in files:
                f = os.path.join(context.bin_path, f)
                os.unlink(f)

        def install_pip(self, context):
            """
            Install pip in the virtual environment.

            :param context: The information for the virtual environment
                            creation request being processed.
            """
            url = 'https://bootstrap.pypa.io/get-pip.py'
            self.install_script(context, 'pip', url)


    def main(args=None):
        import argparse

        parser = argparse.ArgumentParser(prog=__name__,
                                         description='Creates virtual Python '
                                                     'environments in one or '
                                                     'more target '
                                                     'directories.')
        parser.add_argument('dirs', metavar='ENV_DIR', nargs='+',
                            help='A directory in which to create the '
                                 'virtual environment.')
        parser.add_argument('--no-setuptools', default=False,
                            action='store_true', dest='nodist',
                            help="Don't install setuptools or pip in the "
                                 "virtual environment.")
        parser.add_argument('--no-pip', default=False,
                            action='store_true', dest='nopip',
                            help="Don't install pip in the virtual "
                                 "environment.")
        parser.add_argument('--system-site-packages', default=False,
                            action='store_true', dest='system_site',
                            help='Give the virtual environment access to the '
                                 'system site-packages dir.')
        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks = True
        parser.add_argument('--symlinks', default=use_symlinks,
                            action='store_true', dest='symlinks',
                            help='Try to use symlinks rather than copies, '
                                 'when symlinks are not the default for '
                                 'the platform.')
        parser.add_argument('--clear', default=False, action='store_true',
                            dest='clear', help='Delete the contents of the '
                                               'virtual environment '
                                               'directory if it already '
                                               'exists, before virtual '
                                               'environment creation.')
        parser.add_argument('--upgrade', default=False, action='store_true',
                            dest='upgrade', help='Upgrade the virtual '
                                                 'environment directory to '
                                                 'use this version of '
                                                 'Python, assuming Python '
                                                 'has been upgraded '
                                                 'in-place.')
        parser.add_argument('--verbose', default=False, action='store_true',
                            dest='verbose', help='Display the output '
                                                 'from the scripts which '
                                                 'install setuptools and pip.')
        options = parser.parse_args(args)
        if options.upgrade and options.clear:
            raise ValueError('you cannot supply --upgrade and --clear together.')
        builder = ExtendedEnvBuilder(system_site_packages=options.system_site,
                                       clear=options.clear,
                                       symlinks=options.symlinks,
                                       upgrade=options.upgrade,
                                       nodist=options.nodist,
                                       nopip=options.nopip,
                                       verbose=options.verbose)
        for d in options.dirs:
            builder.create(d)

    if __name__ == '__main__':
        rc = 1
        try:
            main()
            rc = 0
        except Exception as e:
            print('Error: %s' % e, file=sys.stderr)
        sys.exit(rc)


Script này cũng có sẵn để tải xuống `trực tuyến <https://gist.github.com/vsajip/4673395>`_.

.. _`About Execution Policies`: https://go.microsoft.com/fwlink/?LinkID=135170
.. _`online`: https://gist.github.com/vsajip/4673395
