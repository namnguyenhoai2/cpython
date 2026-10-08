:mod:`!subprocess` --- Quản lý tiến trình con
=============================================

.. module:: subprocess
   :synopsis: Quản lý tiến trình con.

.. moduleauthor:: Peter Åstrand <astrand@lysator.liu.se>
.. sectionauthor:: Peter Åstrand <astrand@lysator.liu.se>

**Mã nguồn:** :source:`Lib/subprocess.py`

--------------

Module :mod:`!subprocess` cho phép bạn tạo các tiến trình mới, kết nối với các pipe đầu vào/đầu ra/lỗi của chúng và nhận mã trả về. Module này nhằm thay thế một số module và hàm cũ hơn::

   os.system
   os.spawn*

Bạn có thể tìm thấy thông tin về cách sử dụng module :mod:`!subprocess` để thay thế các module và hàm này trong các phần sau.

.. seealso::

   :pep:`324` -- PEP đề xuất module subprocess

.. include:: ../includes/wasm-mobile-notavail.rst

Sử dụng module :mod:`!subprocess`
---------------------------------

Cách tiếp cận được khuyến nghị để gọi các subprocess là sử dụng hàm :func:`run` cho mọi trường hợp mà hàm này có thể xử lý. Với các trường hợp nâng cao hơn, có thể sử dụng trực tiếp interface :class:`Popen` bên dưới.


.. function:: run(args, *, stdin=None, input=None, stdout=None, stderr=None,\
                  capture_output=False, shell=False, cwd=None, timeout=None, \ check=False, encoding=None, errors=None, text=None, env=None, \ universal_newlines=None, ****other_popen_kwargs)

   Chạy lệnh được mô tả bởi *args*. Chờ lệnh hoàn tất, sau đó trả về một instance :class:`CompletedProcess`.

   Các đối số được trình bày ở trên chỉ là những đối số phổ biến nhất, được mô tả bên dưới trong :ref:`frequently-used-arguments` (do đó mới sử dụng ký hiệu chỉ dành cho keyword trong chữ ký rút gọn). Chữ ký đầy đủ của hàm phần lớn giống với chữ ký của constructor :class:`Popen` - hầu hết đối số của hàm này được truyền tiếp đến interface đó. (*timeout*, *input*, *check* và *capture_output* thì không.)

   Nếu *capture_output* là true, stdout và stderr sẽ được capture. Khi sử dụng tùy chọn này, đối tượng :class:`Popen` nội bộ sẽ tự động được tạo với *stdout* và *stderr* đều được đặt thành :data:`~subprocess.PIPE`. Không được cung cấp các đối số *stdout* và *stderr* đồng thời với *capture_output*. Nếu muốn capture và kết hợp cả hai stream thành một, hãy đặt *stdout* thành :data:`~subprocess.PIPE` và *stderr* thành :data:`~subprocess.STDOUT`, thay vì sử dụng *capture_output*.

   Có thể chỉ định *timeout* tính bằng giây; giá trị này được truyền nội bộ cho
   :meth:`Popen.communicate`. Nếu hết thời gian chờ, tiến trình con sẽ bị kết thúc và được chờ xử lý. Ngoại lệ :exc:`TimeoutExpired` sẽ được ném lại sau khi tiến trình con đã kết thúc. Bản thân việc tạo tiến trình ban đầu không thể bị gián đoạn trên nhiều API nền tảng, vì vậy không đảm bảo rằng bạn sẽ thấy ngoại lệ timeout cho đến ít nhất sau khoảng thời gian cần để tạo tiến trình.

   Đối số *input* được truyền đến :meth:`Popen.communicate` và do đó đến stdin của subprocess. Nếu được sử dụng, đối số này phải là một chuỗi byte hoặc một chuỗi nếu *encoding* hoặc *errors* được chỉ định, hoặc *text* là true. Khi được sử dụng, đối tượng :class:`Popen` nội bộ sẽ tự động được tạo với *stdin* được đặt thành :data:`~subprocess.PIPE`, và không được đồng thời sử dụng đối số *stdin*.

   Nếu *check* là true và quy trình kết thúc với mã thoát khác 0, một
   :exc:`CalledProcessError` exception sẽ được phát sinh. Các thuộc tính của exception đó chứa các đối số, mã thoát, stdout và stderr nếu chúng được capture.

   Nếu *encoding* hoặc *errors* được chỉ định, hoặc *text* là true, các file object cho stdin, stdout và stderr sẽ được mở ở chế độ text bằng *encoding* và *errors* được chỉ định hoặc giá trị mặc định :class:`io.TextIOWrapper`. Đối số *universal_newlines* tương đương với *text* và được cung cấp để tương thích ngược. Theo mặc định, các file object được mở ở chế độ binary.

   Nếu *env* không phải là ``None``, nó phải là một mapping xác định các biến môi trường cho quy trình mới; các biến này được sử dụng thay cho hành vi mặc định là kế thừa môi trường của quy trình hiện tại. Mapping này được truyền trực tiếp đến :class:`Popen`. Mapping này có thể là str thành str trên mọi nền tảng hoặc bytes thành bytes trên các nền tảng POSIX, tương tự như :data:`os.environ` hoặc
   :data:`os.environb`.

   Các ví dụ::

      >>> subprocess.run(["ls", "-l"])  # không capture output
      CompletedProcess(args=['ls', '-l'], returncode=0)

      >>> subprocess.run("exit 1", shell=True, check=True)
      Traceback (most recent call last):
        ...
      subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

      >>> subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
      CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
      stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')

   .. versionadded:: 3.5

   .. versionchanged:: 3.6

      Đã thêm các tham số *encoding* và *errors*

   .. versionchanged:: 3.7

      Đã thêm tham số *text*, làm bí danh dễ hiểu hơn cho *universal_newlines*. Đã thêm tham số *capture_output*.

   .. versionchanged:: 3.12

      Đã thay đổi thứ tự tìm kiếm shell trên Windows cho ``shell=True``. Thư mục hiện tại và ``%PATH%`` được thay thế bằng ``%COMSPEC%`` và ``%SystemRoot%\System32\cmd.exe``. Do đó, việc đặt một chương trình độc hại có tên ``cmd.exe`` vào thư mục hiện tại sẽ không còn hiệu quả.

.. class:: CompletedProcess

   Giá trị trả về từ :func:`run`, đại diện cho một process đã kết thúc.

   .. attribute:: args

      Các đối số được sử dụng để khởi chạy process. Đây có thể là một danh sách hoặc một chuỗi.

   .. attribute:: returncode

      Trạng thái thoát của tiến trình con. Thông thường, trạng thái thoát bằng 0 cho biết tiến trình đã chạy thành công.

      Một giá trị âm ``-N`` cho biết tiến trình con đã bị kết thúc bởi signal ``N`` (chỉ dành cho POSIX).

   .. attribute:: stdout

      stdout được ghi lại từ tiến trình con. Một chuỗi byte hoặc một chuỗi nếu
      :func:`run` được gọi với encoding, errors hoặc text=True. ``None`` nếu stdout không được ghi lại.

      Nếu bạn chạy tiến trình với ``stderr=subprocess.STDOUT``, stdout và stderr sẽ được kết hợp trong thuộc tính này, và :attr:`stderr` sẽ là ``None``.

   .. attribute:: stderr

      stderr được ghi lại từ tiến trình con. Một chuỗi byte hoặc một chuỗi nếu
      :func:`run` được gọi với encoding, errors hoặc text=True. ``None`` nếu stderr không được ghi lại.

   .. method:: check_returncode()

      Nếu :attr:`returncode` khác không, hãy raise một :exc:`CalledProcessError`.

   .. versionadded:: 3.5

.. data:: DEVNULL

   Giá trị đặc biệt có thể được dùng làm đối số *stdin*, *stdout* hoặc *stderr* cho :class:`Popen`, cho biết rằng tệp đặc biệt :data:`os.devnull` sẽ được sử dụng.

   .. versionadded:: 3.3


.. data:: PIPE

   Giá trị đặc biệt có thể được dùng làm đối số *stdin*, *stdout* hoặc *stderr* cho :class:`Popen`, cho biết rằng cần mở một pipe đến stream chuẩn. Hữu ích nhất khi dùng với :meth:`Popen.communicate`.


.. data:: STDOUT

   Giá trị đặc biệt có thể được dùng làm đối số *stderr* cho :class:`Popen`, cho biết rằng standard error sẽ được chuyển vào cùng handle với standard output.


.. exception:: SubprocessError

    Lớp cơ sở cho tất cả các exception khác từ module này.

    .. versionadded:: 3.3


.. exception:: TimeoutExpired

    Lớp con của :exc:`SubprocessError`, được phát sinh khi hết thời gian chờ trong lúc đợi một tiến trình con.

    .. attribute:: cmd

        Lệnh được dùng để khởi chạy tiến trình con.

    .. attribute:: timeout

        Thời gian chờ tính bằng giây.

    .. attribute:: output

        Đầu ra của tiến trình con nếu được thu thập bởi :func:`run` hoặc
        :func:`check_output`.  Nếu không, ``None``.  Điều này luôn
        :class:`bytes` khi bất kỳ đầu ra nào được thu thập, bất kể thiết lập ``text=True``.  Nó có thể vẫn là ``None`` thay vì ``b''`` khi không quan sát thấy đầu ra nào.

    .. attribute:: stdout

        Bí danh cho output, để đối xứng với :attr:`stderr`.

    .. attribute:: stderr

        Đầu ra stderr của tiến trình con nếu được thu thập bởi :func:`run`. Nếu không, ``None``.  Đây luôn là :class:`bytes` khi đầu ra stderr được thu thập, bất kể thiết lập ``text=True``.  Nó có thể vẫn là ``None`` thay vì ``b''`` khi không quan sát thấy đầu ra stderr nào.

    .. versionadded:: 3.3

    .. versionchanged:: 3.5
        *stdout* và *stderr* các thuộc tính được thêm vào

.. exception:: CalledProcessError

    Lớp con của :exc:`SubprocessError`, được nâng lên khi một tiến trình do
    :func:`check_call`, :func:`check_output`, hoặc :func:`run` (với ``check=True``) trả về trạng thái thoát khác không.


    .. attribute:: returncode

        Trạng thái thoát của tiến trình con, là một số nguyên. Nếu tiến trình thoát do một tín hiệu, giá trị này sẽ là số tín hiệu âm.

    .. attribute:: cmd

        Lệnh được dùng để khởi chạy tiến trình con.

    .. attribute:: output

        Đầu ra của tiến trình con nếu được thu thập bởi :func:`run` hoặc
        :func:`check_output`. Nếu không, ``None``.

    .. attribute:: stdout

        Bí danh cho output, để đối xứng với :attr:`stderr`.

    .. attribute:: stderr

        Đầu ra stderr của tiến trình con nếu được ghi lại bởi :func:`run`. Nếu không, ``None``.

    .. versionchanged:: 3.5
        *stdout* và *stderr* các thuộc tính được thêm vào


.. _frequently-used-arguments:

Các đối số thường dùng
^^^^^^^^^^^^^^^^^^^^^^

Để hỗ trợ nhiều trường hợp sử dụng khác nhau, hàm khởi tạo :class:`Popen` (và các hàm tiện ích) chấp nhận một số lượng lớn đối số tùy chọn. Trong hầu hết các trường hợp sử dụng thông thường, bạn có thể an toàn để nhiều đối số trong số này ở giá trị mặc định. Các đối số thường cần dùng nhất là:

   *args* là bắt buộc trong mọi lệnh gọi và phải là một chuỗi hoặc một chuỗi các đối số chương trình. Thông thường, nên cung cấp một chuỗi các đối số vì điều này cho phép module tự xử lý việc escape và trích dẫn cần thiết cho các đối số (ví dụ: để cho phép có khoảng trắng trong tên tệp). Nếu truyền một chuỗi đơn, *shell* phải là :const:`True` (xem bên dưới), nếu không thì chuỗi đó chỉ được chứa tên chương trình cần thực thi mà không chỉ định bất kỳ đối số nào.

   *stdin*, *stdout* và *stderr* lần lượt chỉ định các handle tệp cho đầu vào chuẩn, đầu ra chuẩn và lỗi chuẩn của chương trình được thực thi. Các giá trị hợp lệ là ``None``, :data:`PIPE`, :data:`DEVNULL`, một file descriptor hiện có (một số nguyên dương) và một :term:`file object` hiện có với file descriptor hợp lệ. Với cài đặt mặc định của ``None``, sẽ không có chuyển hướng nào xảy ra. :data:`PIPE` cho biết cần tạo một pipe mới đến tiến trình con. :data:`DEVNULL` cho biết tệp đặc biệt :data:`os.devnull` sẽ được sử dụng. Ngoài ra, *stderr* có thể là :data:`STDOUT`, cho biết dữ liệu stderr từ tiến trình con sẽ được thu vào cùng handle tệp với *stdout*.

   .. index::
      single: universal newlines; subprocess module

   Nếu chỉ định *encoding* hoặc *errors*, hoặc *text* (còn được gọi là *universal_newlines*) là true, các đối tượng tệp *stdin*, *stdout* và *stderr* sẽ được mở ở chế độ văn bản bằng *encoding* và *errors* được chỉ định trong lệnh gọi hoặc bằng các giá trị mặc định của :class:`io.TextIOWrapper`.

   Đối với *stdin*, các ký tự kết thúc dòng ``'\n'`` trong đầu vào sẽ được chuyển đổi thành dấu phân cách dòng mặc định :data:`os.linesep`. Đối với *stdout* và *stderr*, mọi ký tự kết thúc dòng trong đầu ra sẽ được chuyển đổi thành ``'\n'``. Để biết thêm thông tin, hãy xem tài liệu về lớp :class:`io.TextIOWrapper` khi đối số *newline* trong hàm khởi tạo của lớp này là ``None``.

   Nếu không sử dụng chế độ văn bản, *stdin*, *stdout* và *stderr* sẽ được mở dưới dạng các luồng nhị phân. Không thực hiện chuyển đổi encoding hoặc ký tự kết thúc dòng.

   .. versionchanged:: 3.6
      Đã thêm các tham số *encoding* và *errors*.

   .. versionchanged:: 3.7
      Đã thêm tham số *text* làm bí danh cho *universal_newlines*.

   .. note::

      Thuộc tính newlines của các đối tượng tệp :attr:`Popen.stdin`,
      :attr:`Popen.stdout` và :attr:`Popen.stderr` không được cập nhật bởi phương thức :meth:`Popen.communicate`.

   Nếu *shell* là ``True``, lệnh được chỉ định sẽ được thực thi thông qua shell. Điều này có thể hữu ích nếu bạn chủ yếu sử dụng Python vì khả năng kiểm soát luồng thực thi nâng cao hơn hầu hết các shell hệ thống, nhưng vẫn muốn truy cập thuận tiện vào các tính năng shell khác như pipe shell, ký tự đại diện cho tên tệp, mở rộng biến môi trường và mở rộng ``~`` thành thư mục chính của người dùng. Tuy nhiên, lưu ý rằng bản thân Python cung cấp các triển khai của nhiều tính năng giống shell (đặc biệt là :mod:`glob`,
   :mod:`fnmatch`, :func:`os.walk`, :func:`os.path.expandvars`,
   :func:`os.path.expanduser`, và :mod:`shutil`).

   .. versionchanged:: 3.3
      Khi *universal_newlines* là ``True``, lớp này sử dụng encoding
      :func:`locale.getpreferredencoding(False) <locale.getpreferredencoding>` thay cho ``locale.getpreferredencoding()``. Xem
      lớp :class:`io.TextIOWrapper` để biết thêm thông tin về thay đổi này.

   .. note::

      Đọc phần `Security Considerations <Security Considerations_>`_ trước khi sử dụng ``shell=True``.

Các tùy chọn này, cùng với tất cả các tùy chọn khác, được mô tả chi tiết hơn trong tài liệu về hàm khởi tạo :class:`Popen`.


Hàm khởi tạo Popen
^^^^^^^^^^^^^^^^^^

Việc tạo và quản lý tiến trình bên dưới trong module này do lớp :class:`Popen` đảm nhiệm. Lớp này cung cấp nhiều khả năng tùy chỉnh, giúp các developer xử lý những trường hợp ít phổ biến hơn mà các hàm tiện ích không hỗ trợ.


.. class:: Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, \
                 stderr=None, preexec_fn=None, close_fds=True, shell=False, \ cwd=None, env=None, universal_newlines=None, \ startupinfo=None, creationflags=0, restore_signals=True, \ start_new_session=False, pass_fds=(), *, group=None, \ extra_groups=None, user=None, umask=-1, \ encoding=None, errors=None, text=None, pipesize=-1, \ process_group=None)

   Thực thi một chương trình con trong một tiến trình mới. Trên POSIX, lớp này sử dụng
   :meth:`os.execvpe` để thực thi chương trình con. Trên Windows, lớp này sử dụng hàm Windows ``CreateProcess()``. Các đối số của
   :class:`Popen` như sau.

   *args* phải là một sequence gồm các đối số của chương trình hoặc một chuỗi đơn hay :term:`path-like object`. Theo mặc định, chương trình được thực thi là mục đầu tiên trong *args* nếu *args* là một sequence. Nếu *args* là một chuỗi, cách diễn giải sẽ phụ thuộc vào nền tảng và được mô tả bên dưới. Xem các đối số *shell* và *executable* để biết thêm những khác biệt so với hành vi mặc định. Trừ khi có quy định khác, nên truyền *args* dưới dạng một sequence.

   .. warning::

      Để đạt độ tin cậy tối đa, hãy sử dụng đường dẫn đầy đủ đến executable. Để tìm kiếm một tên không đầy đủ trên :envvar:`PATH`, hãy sử dụng
      :meth:`shutil.which`. Trên tất cả các nền tảng, truyền :data:`sys.executable` là cách được khuyến nghị để khởi chạy lại trình thông dịch Python hiện tại, và sử dụng định dạng dòng lệnh ``-m`` để khởi chạy một module đã cài đặt.

      Việc phân giải đường dẫn của *executable* (hoặc mục đầu tiên của *args*) phụ thuộc vào nền tảng. Đối với POSIX, hãy xem :meth:`os.execvpe`, đồng thời lưu ý rằng khi phân giải hoặc tìm kiếm đường dẫn đến executable, *cwd* sẽ ghi đè thư mục làm việc hiện tại và *env* có thể ghi đè biến môi trường ``PATH``. Đối với Windows, hãy xem tài liệu về các tham số ``lpApplicationName`` và ``lpCommandLine`` của WinAPI ``CreateProcess``, đồng thời lưu ý rằng khi phân giải hoặc tìm kiếm đường dẫn đến executable với ``shell=False``, *cwd* không ghi đè thư mục làm việc hiện tại và *env* không thể ghi đè biến môi trường ``PATH``. Việc sử dụng đường dẫn đầy đủ sẽ tránh được tất cả những khác biệt này.

   Ví dụ về cách truyền một số đối số cho chương trình bên ngoài dưới dạng một chuỗi là::

     Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])

   Trên POSIX, nếu *args* là một chuỗi, chuỗi đó được hiểu là tên hoặc đường dẫn của chương trình cần thực thi. Tuy nhiên, chỉ có thể làm như vậy khi không truyền đối số cho chương trình.

   .. note::

      Có thể không dễ nhận ra cách tách một lệnh shell thành một chuỗi đối số, đặc biệt trong các trường hợp phức tạp. :meth:`shlex.split` có thể minh họa cách xác định việc tokenization chính xác cho *args*::

         >>> import shlex, subprocess
         >>> command_line = input()
         /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
         >>> args = shlex.split(command_line)
         >>> print(args)
         ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
         >>> p = subprocess.Popen(args) # Thành công!

      Lưu ý cụ thể rằng các tùy chọn (chẳng hạn như *-input*) và các đối số (chẳng hạn như *eggs.txt*) được phân tách bằng khoảng trắng trong shell sẽ nằm trong các phần tử danh sách riêng biệt, trong khi các đối số cần được đặt trong dấu ngoặc kép hoặc escape bằng dấu gạch chéo ngược khi được sử dụng trong shell (chẳng hạn như tên tệp chứa khoảng trắng hoặc lệnh *echo* được hiển thị ở trên) sẽ là các phần tử danh sách đơn.

   Trên Windows, nếu *args* là một chuỗi, nó sẽ được chuyển đổi thành một chuỗi theo cách được mô tả trong :ref:`converting-argument-sequence`. Điều này là do ``CreateProcess()`` bên dưới hoạt động trên các chuỗi.

   .. versionchanged:: 3.6
      Tham số *args* chấp nhận một :term:`path-like object` nếu *shell* là ``False`` và một chuỗi chứa các đối tượng dạng đường dẫn trên POSIX.

   .. versionchanged:: 3.8
      Tham số *args* chấp nhận một :term:`path-like object` nếu *shell* là ``False`` và một sequence chứa các đối tượng bytes và path-like trên Windows.

   Đối số *shell* (mặc định là ``False``) chỉ định có sử dụng shell làm chương trình cần thực thi hay không. Nếu *shell* là ``True``, bạn nên truyền *args* dưới dạng chuỗi thay vì sequence.

   Trên POSIX với ``shell=True``, shell mặc định là :file:`/bin/sh`. Nếu *args* là một chuỗi, chuỗi đó chỉ định lệnh cần thực thi thông qua shell. Điều này có nghĩa là chuỗi phải được định dạng chính xác như khi bạn nhập tại dấu nhắc shell. Ví dụ, điều này bao gồm việc đặt trong dấu ngoặc kép hoặc escape bằng dấu gạch chéo ngược đối với các tên tệp chứa khoảng trắng. Nếu *args* là một sequence, phần tử đầu tiên chỉ định chuỗi lệnh, còn mọi phần tử bổ sung sẽ được xử lý như các đối số bổ sung cho chính shell. Nói cách khác, :class:`Popen` thực hiện tương đương với::

      Popen(['/bin/sh', '-c', args[0], args[1], ...])

   Trên Windows với ``shell=True``, biến môi trường :envvar:`COMSPEC` chỉ định shell mặc định. Trường hợp duy nhất bạn cần chỉ định ``shell=True`` trên Windows là khi lệnh bạn muốn thực thi được tích hợp trong shell (ví dụ: :command:`dir` hoặc :command:`copy`). Bạn không cần ``shell=True`` để chạy tệp batch hoặc tệp thực thi dựa trên console.

   .. note::

      Đọc phần `Security Considerations <Security Considerations_>`_ trước khi sử dụng ``shell=True``.

   *bufsize* sẽ được cung cấp làm đối số tương ứng cho
   :func:`open` function khi tạo các đối tượng tệp pipe stdin/stdout/stderr:

   - ``0`` có nghĩa là không đệm (việc đọc và ghi nằm trong một system call và có thể trả về dữ liệu ngắn)
   - ``1`` có nghĩa là đệm theo dòng (chỉ có thể sử dụng nếu ``text=True`` hoặc ``universal_newlines=True``)
   - bất kỳ giá trị dương nào khác có nghĩa là sử dụng bộ đệm có kích thước xấp xỉ giá trị đó
   - bufsize âm (mặc định) có nghĩa là hệ thống sẽ sử dụng giá trị mặc định của io.DEFAULT_BUFFER_SIZE.

   .. versionchanged:: 3.3.1
      *bufsize* hiện mặc định là -1 để bật buffering theo mặc định, phù hợp với hành vi mà hầu hết mã nguồn mong đợi. Trong các phiên bản trước Python 3.2.4 và 3.3.1, giá trị này không chính xác được mặc định là ``0``, tức là không đệm và cho phép các lần đọc ngắn. Đây là hành vi ngoài ý muốn và không phù hợp với hành vi của Python 2 như hầu hết mã nguồn mong đợi.

   Đối số *executable* chỉ định một chương trình thay thế để thực thi. Đối số này rất hiếm khi cần thiết. Khi ``shell=False``, *executable* sẽ thay thế chương trình cần thực thi được chỉ định bởi *args*. Tuy nhiên, *args* ban đầu vẫn được truyền cho chương trình. Hầu hết chương trình coi chương trình được chỉ định bởi *args* là tên lệnh, và tên này có thể khác với chương trình thực sự được thực thi. Trên POSIX, tên *args* trở thành tên hiển thị của executable trong các tiện ích như
   :program:`ps`. Nếu ``shell=True``, trên POSIX, đối số *executable* chỉ định một shell thay thế cho :file:`/bin/sh` mặc định.

   .. versionchanged:: 3.6
      Tham số *executable* chấp nhận một :term:`path-like object` trên POSIX.

   .. versionchanged:: 3.8
      Tham số *executable* chấp nhận một bytes và :term:`path-like object` trên Windows.

   .. versionchanged:: 3.12

      Đã thay đổi thứ tự tìm kiếm shell của Windows cho ``shell=True``. Thư mục hiện tại và ``%PATH%`` được thay thế bằng ``%COMSPEC%`` và ``%SystemRoot%\System32\cmd.exe``. Do đó, việc đặt một chương trình độc hại có tên ``cmd.exe`` vào thư mục hiện tại sẽ không còn hiệu quả.

   *stdin*, *stdout* và *stderr* lần lượt chỉ định các handle tệp cho standard input, standard output và standard error của chương trình được thực thi. Các giá trị hợp lệ là ``None``, :data:`PIPE`, :data:`DEVNULL`, một file descriptor hiện có (một số nguyên dương) và một :term:`file object` hiện có với file descriptor hợp lệ. Với cài đặt mặc định của ``None``, sẽ không xảy ra chuyển hướng nào. :data:`PIPE` cho biết cần tạo một pipe mới tới tiến trình con. :data:`DEVNULL` cho biết sẽ sử dụng tệp đặc biệt :data:`os.devnull`. Ngoài ra, *stderr* có thể là :data:`STDOUT`, cho biết dữ liệu stderr từ các ứng dụng sẽ được thu thập vào cùng handle tệp như *stdout*.

   Nếu *preexec_fn* được đặt thành một đối tượng callable, đối tượng này sẽ được gọi trong tiến trình con ngay trước khi tiến trình con được thực thi. (Chỉ POSIX)

   .. warning::

      Tham số *preexec_fn* KHÔNG AN TOÀN khi sử dụng trong ứng dụng có thread. Tiến trình con có thể bị deadlock trước khi exec được gọi.

   .. note::

      Nếu cần sửa đổi môi trường cho tiến trình con, hãy sử dụng tham số *env* thay vì thực hiện việc đó trong *preexec_fn*. Các tham số *start_new_session* và *process_group* nên thay thế cho mã sử dụng *preexec_fn* để gọi :func:`os.setsid` hoặc :func:`os.setpgid` trong tiến trình con.

   .. versionchanged:: 3.8

      Tham số *preexec_fn* không còn được hỗ trợ trong các subinterpreter. Việc sử dụng tham số này trong một subinterpreter sẽ gây ra
      :exc:`RuntimeError`. Hạn chế mới này có thể ảnh hưởng đến các ứng dụng được triển khai trong mod_wsgi, uWSGI và các môi trường nhúng khác.

   Nếu *close_fds* là true, tất cả file descriptor ngoại trừ ``0``, ``1`` và ``2`` sẽ bị đóng trước khi tiến trình con được thực thi. Ngược lại, khi *close_fds* là false, các file descriptor sẽ tuân theo cờ inheritable của chúng như được mô tả trong :ref:`fd_inheritance`.

   Trên Windows, nếu *close_fds* là true thì không handle nào được kế thừa bởi tiến trình con, trừ khi được truyền rõ ràng trong phần tử ``handle_list`` của
   :attr:`STARTUPINFO.lpAttributeList`, hoặc thông qua việc chuyển hướng standard handle.

   .. versionchanged:: 3.2
      Giá trị mặc định của *close_fds* đã được thay đổi từ :const:`False` thành giá trị được mô tả ở trên.

   .. versionchanged:: 3.7
      Trên Windows, giá trị mặc định của *close_fds* đã được thay đổi từ :const:`False` thành
      :const:`True` khi chuyển hướng các handle chuẩn. Giờ đây có thể đặt *close_fds* thành :const:`True` khi chuyển hướng các handle chuẩn.

   *pass_fds* là một chuỗi tùy chọn gồm các mô tả tệp cần được giữ mở giữa tiến trình cha và tiến trình con. Việc cung cấp bất kỳ *pass_fds* nào sẽ buộc *close_fds* có giá trị là :const:`True`. (Chỉ POSIX)

   .. versionchanged:: 3.2
      Tham số *pass_fds* đã được thêm vào.

   Nếu *cwd* không phải là ``None``, hàm sẽ đổi thư mục làm việc thành *cwd* trước khi thực thi tiến trình con. *cwd* có thể là một chuỗi, bytes hoặc
   :term:`path-like <path-like object>` object. Trên POSIX, hàm sẽ tìm *executable* (hoặc mục đầu tiên trong *args*) tương đối với *cwd* nếu đường dẫn đến executable là đường dẫn tương đối.

   .. versionchanged:: 3.6
      Tham số *cwd* chấp nhận một :term:`path-like object` trên POSIX.

   .. versionchanged:: 3.7
      Tham số *cwd* chấp nhận một :term:`path-like object` trên Windows.

   .. versionchanged:: 3.8
      Tham số *cwd* chấp nhận một đối tượng bytes trên Windows.

   Nếu *restore_signals* là true (mặc định), tất cả các signal mà Python đã đặt thành SIG_IGN sẽ được khôi phục về SIG_DFL trong tiến trình con trước khi thực hiện exec. Hiện tại, các signal này bao gồm SIGPIPE, SIGXFZ và SIGXFSZ. (Chỉ dành cho POSIX)

   .. versionchanged:: 3.2
      *restore_signals* đã được thêm.

   Nếu *start_new_session* là true, lệnh gọi hệ thống ``setsid()`` sẽ được thực hiện trong tiến trình con trước khi thực thi subprocess.

   .. availability:: POSIX
   .. versionchanged:: 3.2
      *start_new_session* đã được thêm.

   Nếu *process_group* là một số nguyên không âm, lệnh gọi hệ thống ``setpgid(0, value)`` sẽ được thực hiện trong tiến trình con trước khi thực thi subprocess.

   .. availability:: POSIX
   .. versionchanged:: 3.11
      *process_group* đã được thêm.

   Nếu *group* không phải là ``None``, lệnh gọi hệ thống setregid() sẽ được thực hiện trong tiến trình con trước khi thực thi subprocess. Nếu giá trị được cung cấp là một chuỗi, giá trị đó sẽ được tra cứu thông qua :func:`grp.getgrnam` và giá trị trong ``gr_gid`` sẽ được sử dụng. Nếu giá trị là một số nguyên, giá trị đó sẽ được truyền nguyên vẹn. (Chỉ dành cho POSIX)

   .. availability:: POSIX
   .. versionadded:: 3.9

   Nếu *extra_groups* không phải là ``None``, lệnh gọi hệ thống setgroups() sẽ được thực hiện trong tiến trình con trước khi thực thi subprocess. Các chuỗi được cung cấp trong *extra_groups* sẽ được tra cứu thông qua
   :func:`grp.getgrnam` và các giá trị trong ``gr_gid`` sẽ được sử dụng. Các giá trị số nguyên sẽ được truyền nguyên vẹn. (Chỉ dành cho POSIX)

   .. availability:: POSIX
   .. versionadded:: 3.9

   Nếu *user* không phải là ``None``, lệnh gọi hệ thống setreuid() sẽ được thực hiện trong tiến trình con trước khi thực thi subprocess. Nếu giá trị được cung cấp là một chuỗi, giá trị đó sẽ được tra cứu thông qua :func:`pwd.getpwnam` và giá trị trong ``pw_uid`` sẽ được sử dụng. Nếu giá trị là một số nguyên, giá trị đó sẽ được truyền nguyên vẹn. (Chỉ dành cho POSIX)

   .. note::

      Việc chỉ định *user* sẽ không loại bỏ các thành viên nhóm bổ sung hiện có! Caller cũng phải truyền ``extra_groups=()`` để giảm các thành viên nhóm của tiến trình con vì mục đích bảo mật.

   .. availability:: POSIX
   .. versionadded:: 3.9

   Nếu *umask* không âm, lệnh gọi hệ thống umask() sẽ được thực hiện trong tiến trình con trước khi thực thi subprocess.

   .. availability:: POSIX
   .. versionadded:: 3.9

   Nếu *env* không phải là ``None``, nó phải là một ánh xạ xác định các biến môi trường cho tiến trình mới; các biến này được sử dụng thay cho hành vi mặc định là kế thừa môi trường của tiến trình hiện tại. Ánh xạ này có thể là str sang str trên mọi nền tảng hoặc bytes sang bytes trên các nền tảng POSIX, tương tự như
   :data:`os.environ` hoặc :data:`os.environb`.

   .. note::

      Nếu được chỉ định, *env* phải cung cấp mọi biến cần thiết để chương trình thực thi. Trên Windows, để chạy một `side-by-side assembly <side-by-side assembly_>`_, *env* được chỉ định **phải** bao gồm một ``%SystemRoot%`` hợp lệ.

   .. _side-by-side assembly: https://en.wikipedia.org/wiki/Side-by-Side_Assembly

   Nếu *encoding* hoặc *errors* được chỉ định, hoặc *text* là true, các đối tượng tệp *stdin*, *stdout* và *stderr* được mở ở chế độ văn bản với *encoding* và *errors* đã chỉ định, như mô tả ở trên trong :ref:`frequently-used-arguments`. Đối số *universal_newlines* tương đương với *text* và được cung cấp để duy trì khả năng tương thích ngược. Theo mặc định, các đối tượng tệp được mở ở chế độ nhị phân.

   .. versionadded:: 3.6
      *encoding* và *errors* đã được thêm vào.

   .. versionadded:: 3.7
      *text* được thêm vào như một bí danh dễ đọc hơn cho *universal_newlines*.

   Nếu được cung cấp, *startupinfo* sẽ là một đối tượng :class:`STARTUPINFO`, được truyền cho hàm ``CreateProcess`` bên dưới.

   Nếu được cung cấp, *creationflags* có thể là một hoặc nhiều cờ sau:

   * :data:`CREATE_NEW_CONSOLE`
   * :data:`CREATE_NEW_PROCESS_GROUP`
   * :data:`ABOVE_NORMAL_PRIORITY_CLASS`
   * :data:`BELOW_NORMAL_PRIORITY_CLASS`
   * :data:`HIGH_PRIORITY_CLASS`
   * :data:`IDLE_PRIORITY_CLASS`
   * :data:`NORMAL_PRIORITY_CLASS`
   * :data:`REALTIME_PRIORITY_CLASS`
   * :data:`CREATE_NO_WINDOW`
   * :data:`DETACHED_PROCESS`
   * :data:`CREATE_DEFAULT_ERROR_MODE`
   * :data:`CREATE_BREAKAWAY_FROM_JOB`

   *pipesize* có thể được sử dụng để thay đổi kích thước của pipe khi
   :data:`PIPE` được sử dụng cho *stdin*, *stdout* hoặc *stderr*. Kích thước của pipe chỉ được thay đổi trên các nền tảng hỗ trợ tính năng này (tại thời điểm viết tài liệu này, chỉ có Linux). Các nền tảng khác sẽ bỏ qua tham số này.

   .. versionchanged:: 3.10
      Đã thêm tham số *pipesize*.

   Các đối tượng Popen được hỗ trợ dưới dạng context manager thông qua câu lệnh :keyword:`with`:
   khi thoát, các bộ mô tả tệp tiêu chuẩn sẽ được đóng và tiến trình sẽ được chờ xử lý.
   ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

      with Popen(["ifconfig"], stdout=PIPE) as proc:
          log.write(proc.stdout.read())

   .. audit-event:: subprocess.Popen executable,args,cwd,env subprocess.Popen

      Popen và các hàm khác trong mô-đun này sử dụng nó sẽ phát sinh một
      :ref:`sự kiện auditing <auditing>` ``subprocess.Popen`` với các đối số ``executable``, ``args``, ``cwd`` và ``env``. Giá trị của ``args`` có thể là một chuỗi hoặc một danh sách chuỗi, tùy thuộc vào nền tảng.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ context manager.

   .. versionchanged:: 3.6
      Bộ hủy Popen hiện phát ra :exc:`ResourceWarning` cảnh báo nếu tiến trình con vẫn đang chạy.

   .. versionchanged:: 3.8
      Trong một số trường hợp, Popen có thể sử dụng :func:`os.posix_spawn` để cải thiện hiệu suất. Trên Windows Subsystem for Linux và QEMU User Emulation, hàm khởi tạo Popen sử dụng :func:`os.posix_spawn` không còn phát sinh ngoại lệ đối với các lỗi như thiếu chương trình, nhưng tiến trình con sẽ kết thúc với :attr:`~Popen.returncode` khác không.


Ngoại lệ
^^^^^^^^

Các ngoại lệ phát sinh trong tiến trình con, trước khi chương trình mới bắt đầu thực thi, sẽ được ném lại trong tiến trình cha.

Ngoại lệ phổ biến nhất được phát sinh là :exc:`OSError`. Điều này xảy ra, chẳng hạn, khi cố thực thi một tệp không tồn tại. Ứng dụng nên chuẩn bị cho
các ngoại lệ :exc:`OSError`. Lưu ý rằng khi ``shell=True``, :exc:`OSError` sẽ chỉ được tiến trình con phát sinh nếu chính shell được chọn không được tìm thấy. Để xác định liệu shell có không tìm thấy ứng dụng được yêu cầu hay không, cần kiểm tra mã trả về hoặc đầu ra từ subprocess.

Một :exc:`ValueError` sẽ được phát sinh nếu :class:`Popen` được gọi với các đối số không hợp lệ.

:func:`check_call` và :func:`check_output` sẽ phát sinh
:exc:`CalledProcessError` nếu tiến trình được gọi trả về mã trả về khác không.

Tất cả các hàm và phương thức chấp nhận tham số *timeout*, chẳng hạn như
:func:`run` và :meth:`Popen.communicate` sẽ phát sinh :exc:`TimeoutExpired` nếu thời gian chờ hết trước khi tiến trình kết thúc.

Các ngoại lệ được định nghĩa trong mô-đun này đều kế thừa từ :exc:`SubprocessError`.

.. versionadded:: 3.3
   Lớp cơ sở :exc:`SubprocessError` đã được thêm vào.

.. _subprocess-security:

.. _`Security Considerations`:

Các cân nhắc về bảo mật
-----------------------

Không giống một số hàm popen khác, thư viện này sẽ không ngầm quyết định gọi system shell. Điều này có nghĩa là mọi ký tự, bao gồm cả shell metacharacter, đều có thể được truyền an toàn đến các tiến trình con. Nếu shell được gọi một cách rõ ràng thông qua ``shell=True``, ứng dụng có trách nhiệm đảm bảo rằng mọi khoảng trắng và metacharacter đều được đặt trong dấu ngoặc thích hợp để tránh các lỗ hổng `shell injection <https://en.wikipedia.org/wiki/Shell_injection#Shell_injection>`_. Trên :ref:`một số nền tảng <shlex-quote-warning>`, có thể sử dụng :func:`shlex.quote` để thực hiện việc escape này.

Trên Windows, các tệp batch (:file:`*.bat` hoặc :file:`*.cmd`) có thể được hệ điều hành khởi chạy trong system shell bất kể các đối số được truyền đến thư viện này. Điều này có thể khiến các đối số được phân tích theo quy tắc của shell, nhưng không có bất kỳ thao tác escape nào do Python thêm vào. Nếu bạn cố ý khởi chạy một tệp batch với các đối số từ các nguồn không đáng tin cậy, hãy cân nhắc truyền ``shell=True`` để cho phép Python escape các ký tự đặc biệt. Xem :gh:`114539` để biết thêm thảo luận.


Các đối tượng Popen
-------------------

Các instance của lớp :class:`Popen` có những phương thức sau:


.. method:: Popen.poll()

   Kiểm tra xem tiến trình con đã kết thúc chưa. Đặt và trả về
   :attr:`~Popen.returncode` thuộc tính. Nếu không, trả về ``None``.


.. method:: Popen.wait(timeout=None)

   Chờ tiến trình con kết thúc. Đặt và trả về
   :attr:`~Popen.returncode` thuộc tính.

   Nếu tiến trình không kết thúc sau *timeout* giây, phát sinh một
   :exc:`TimeoutExpired` exception. Bạn có thể an toàn bắt exception này và thử lại thao tác chờ.

   .. note::

      Điều này sẽ gây deadlock khi sử dụng ``stdout=PIPE`` hoặc ``stderr=PIPE`` và tiến trình con tạo ra đủ dữ liệu đầu ra vào một pipe khiến tiến trình bị chặn trong khi chờ bộ đệm pipe của OS tiếp nhận thêm dữ liệu. Hãy sử dụng :meth:`Popen.communicate` khi dùng pipe để tránh điều đó.

   .. note::

      Khi tham số ``timeout`` không phải là ``None``, thì (trên POSIX) hàm được triển khai bằng một vòng lặp bận (lời gọi không chặn và các lần ngủ ngắn). Hãy sử dụng module :mod:`asyncio` để chờ bất đồng bộ: xem
      :class:`asyncio.create_subprocess_exec`.

   .. versionchanged:: 3.3
      *timeout* đã được thêm vào.

.. method:: Popen.communicate(input=None, timeout=None)

   Tương tác với tiến trình: Gửi dữ liệu vào stdin. Đọc dữ liệu từ stdout và stderr cho đến khi gặp cuối tệp. Chờ tiến trình kết thúc và đặt
   :attr:`~Popen.returncode` thuộc tính. Đối số *input* tùy chọn phải là dữ liệu sẽ được gửi đến tiến trình con hoặc ``None`` nếu không có dữ liệu nào được gửi đến tiến trình con. Nếu các stream được mở ở chế độ văn bản, *input* phải là một chuỗi. Nếu không, nó phải là bytes.

   :meth:`communicate` trả về một tuple ``(stdout_data, stderr_data)``. Dữ liệu sẽ là các chuỗi nếu các stream được mở ở chế độ văn bản; nếu không, sẽ là bytes.

   Lưu ý rằng nếu muốn gửi dữ liệu vào stdin của tiến trình, bạn cần tạo đối tượng Popen với ``stdin=PIPE``. Tương tự, để nhận được bất kỳ giá trị nào khác ngoài ``None`` trong tuple kết quả, bạn cũng cần cung cấp ``stdout=PIPE`` và/hoặc ``stderr=PIPE``.

   Nếu tiến trình không kết thúc sau *timeout* giây, một
   Ngoại lệ :exc:`TimeoutExpired` sẽ được phát sinh. Việc bắt ngoại lệ này và thử lại quá trình giao tiếp sẽ không làm mất bất kỳ đầu ra nào. Việc cung cấp *input* cho một lần gọi :meth:`communicate` tiếp theo sau khi timeout sẽ dẫn đến hành vi không xác định và có thể trở thành lỗi trong tương lai.

   Tiến trình con không bị kết thúc nếu timeout hết hạn, vì vậy để dọn dẹp đúng cách, một ứng dụng hoạt động đúng nên kết thúc tiến trình con và hoàn tất việc giao tiếp::

      proc = subprocess.Popen(...)
      try:
          outs, errs = proc.communicate(timeout=15)
      except TimeoutExpired:
          proc.kill()
          outs, errs = proc.communicate()

   Sau khi một lần gọi :meth:`~Popen.communicate` phát sinh :exc:`TimeoutExpired`, không gọi :meth:`~Popen.wait`. Sử dụng thêm một lần gọi :meth:`~Popen.communicate` để hoàn tất việc xử lý các pipe và điền thuộc tính :attr:`~Popen.returncode`.

   .. note::

      Dữ liệu được đọc sẽ được đệm trong bộ nhớ, vì vậy không sử dụng phương thức này nếu kích thước dữ liệu lớn hoặc không giới hạn.

   .. versionchanged:: 3.3
      *timeout* đã được thêm vào.


.. method:: Popen.send_signal(signal)

   Gửi tín hiệu *signal* đến tiến trình con.

   Không làm gì nếu tiến trình đã hoàn tất.

   .. note::

      Trên Windows, SIGTERM là bí danh của :meth:`terminate`. CTRL_C_EVENT và CTRL_BREAK_EVENT có thể được gửi đến các tiến trình được khởi chạy với tham số *creationflags* có chứa ``CREATE_NEW_PROCESS_GROUP``.


.. method:: Popen.terminate()

   Dừng tiến trình con. Trên các hệ điều hành POSIX, phương thức này gửi :py:const:`~signal.SIGTERM` đến tiến trình con. Trên Windows, hàm API Win32 :c:func:`!TerminateProcess` được gọi để dừng tiến trình con.


.. method:: Popen.kill()

   Buộc dừng tiến trình con. Trên các hệ điều hành POSIX, hàm này gửi SIGKILL đến tiến trình con. Trên Windows, :meth:`kill` là bí danh của :meth:`terminate`.


Lớp cũng thiết lập các thuộc tính sau để bạn truy cập. Không hỗ trợ việc gán lại chúng bằng các giá trị mới:

.. attribute:: Popen.args

   Đối số *args* như được truyền vào :class:`Popen` — một chuỗi các đối số chương trình hoặc một chuỗi đơn.

   .. versionadded:: 3.3

.. attribute:: Popen.stdin

   Nếu đối số *stdin* là :data:`PIPE`, thuộc tính này là một đối tượng stream có thể ghi do :func:`open` trả về. Nếu đã chỉ định các đối số *encoding* hoặc *errors*, hoặc đối số *text* hoặc *universal_newlines* là ``True``, stream này là text stream; nếu không, đây là byte stream. Nếu đối số *stdin* không phải là :data:`PIPE`, thuộc tính này là ``None``.


.. attribute:: Popen.stdout

   Nếu đối số *stdout* là :data:`PIPE`, thuộc tính này là một đối tượng stream có thể đọc do :func:`open` trả về. Việc đọc stream này cung cấp đầu ra từ tiến trình con. Nếu đã chỉ định các đối số *encoding* hoặc *errors*, hoặc đối số *text* hoặc *universal_newlines* là ``True``, stream này là text stream; nếu không, đây là byte stream. Nếu đối số *stdout* không phải là :data:`PIPE`, thuộc tính này là ``None``.


.. attribute:: Popen.stderr

   Nếu đối số *stderr* là :data:`PIPE`, thuộc tính này là một đối tượng luồng có thể đọc được do :func:`open` trả về. Việc đọc từ luồng cung cấp đầu ra lỗi từ tiến trình con. Nếu đã chỉ định các đối số *encoding* hoặc *errors*, hay đối số *text* hoặc *universal_newlines* là ``True``, thì luồng là luồng văn bản; nếu không, đó là luồng byte. Nếu đối số *stderr* không phải là :data:`PIPE`, thuộc tính này là ``None``.

.. warning::

   Sử dụng :meth:`~Popen.communicate` thay vì :attr:`.stdin.write <Popen.stdin>`,
   :attr:`.stdout.read <Popen.stdout>` hoặc :attr:`.stderr.read <Popen.stderr>` để tránh deadlock do bất kỳ bộ đệm pipe OS nào khác bị đầy và chặn tiến trình con.


.. attribute:: Popen.pid

   ID tiến trình của tiến trình con.

   Lưu ý rằng nếu bạn đặt đối số *shell* thành ``True``, đây là ID tiến trình của shell đã được tạo.


.. attribute:: Popen.returncode

   Mã trả về của tiến trình con. Ban đầu là ``None``, :attr:`returncode` được đặt bằng một lệnh gọi đến phương thức :meth:`poll`, :meth:`wait` hoặc :meth:`communicate` nếu chúng phát hiện tiến trình đã kết thúc.

   Giá trị ``None`` cho biết tiến trình vẫn chưa kết thúc tại thời điểm gọi phương thức gần nhất.

   Giá trị âm ``-N`` cho biết tiến trình con đã bị kết thúc bởi tín hiệu ``N`` (chỉ dành cho POSIX).

   Khi ``shell=True``, mã trả về phản ánh trạng thái thoát của chính shell (ví dụ: ``/bin/sh``), trạng thái này có thể ánh xạ các tín hiệu thành những mã như ``128+N``. Xem tài liệu của shell (chẳng hạn như mục Exit Status trong hướng dẫn sử dụng Bash) để biết chi tiết.


Các trình trợ giúp Popen trên Windows
-------------------------------------

Lớp :class:`STARTUPINFO` và các hằng số sau chỉ khả dụng trên Windows.

.. class:: STARTUPINFO(*, dwFlags=0, hStdInput=None, hStdOutput=None, \
                       hStdError=None, wShowWindow=0, lpAttributeList=None)

   Một phần hỗ trợ cho cấu trúc `STARTUPINFO <https://msdn.microsoft.com/en-us/library/ms686331(v=vs.85).aspx>`__ của Windows được sử dụng để tạo :class:`Popen`. Có thể thiết lập các thuộc tính sau bằng cách truyền chúng dưới dạng đối số chỉ dùng từ khóa.

   .. versionchanged:: 3.7
      Đã bổ sung hỗ trợ cho các đối số chỉ dùng từ khóa.

   .. attribute:: dwFlags

      Một trường bit xác định liệu một số thuộc tính :class:`STARTUPINFO` nhất định có được sử dụng khi tiến trình tạo một cửa sổ hay không.::

         si = subprocess.STARTUPINFO()
         si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW

   .. attribute:: hStdInput

      Nếu :attr:`dwFlags` chỉ định :data:`STARTF_USESTDHANDLES`, thuộc tính này là handle đầu vào chuẩn của tiến trình. Nếu
      :data:`STARTF_USESTDHANDLES` không được chỉ định, mặc định cho đầu vào chuẩn là bộ đệm bàn phím.

   .. attribute:: hStdOutput

      Nếu :attr:`dwFlags` chỉ định :data:`STARTF_USESTDHANDLES`, thuộc tính này là handle đầu ra chuẩn của tiến trình. Nếu không, thuộc tính này bị bỏ qua và mặc định cho đầu ra chuẩn là bộ đệm của cửa sổ console.

   .. attribute:: hStdError

      Nếu :attr:`dwFlags` chỉ định :data:`STARTF_USESTDHANDLES`, thuộc tính này là handle lỗi chuẩn của tiến trình. Nếu không, thuộc tính này bị bỏ qua và mặc định cho lỗi chuẩn là bộ đệm của cửa sổ console.

   .. attribute:: wShowWindow

      Nếu :attr:`dwFlags` chỉ định :data:`STARTF_USESHOWWINDOW`, thuộc tính này có thể là bất kỳ giá trị nào có thể được chỉ định trong tham số ``nCmdShow`` cho hàm `ShowWindow <https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx>`__, ngoại trừ ``SW_SHOWDEFAULT``. Nếu không, thuộc tính này bị bỏ qua.

      :data:`SW_HIDE` được cung cấp cho thuộc tính này. Nó được sử dụng khi
      :class:`Popen` được gọi với ``shell=True``.

   .. attribute:: lpAttributeList

      Một dictionary gồm các thuộc tính bổ sung để tạo process như được cung cấp trong ``STARTUPINFOEX``, xem `UpdateProcThreadAttribute <https://msdn.microsoft.com/en-us/library/windows/desktop/ms686880(v=vs.85).aspx>`__.

      Các thuộc tính được hỗ trợ:

      **handle_list**
         Chuỗi các handle sẽ được kế thừa. *close_fds* phải là true nếu chuỗi không rỗng.

         Các handle phải tạm thời được đặt ở trạng thái có thể kế thừa bằng
         :func:`os.set_handle_inheritable` khi được truyền vào constructor :class:`Popen`, nếu không :class:`OSError` sẽ được raise với lỗi Windows ``ERROR_INVALID_PARAMETER`` (87).

         .. warning::

            Trong một tiến trình đa luồng, hãy thận trọng để tránh làm rò rỉ các handle được đánh dấu là có thể kế thừa khi kết hợp tính năng này với các lệnh gọi đồng thời đến những hàm tạo tiến trình khác kế thừa tất cả handle, chẳng hạn như :func:`os.system`. Điều này cũng áp dụng cho việc chuyển hướng handle chuẩn, vốn tạm thời tạo ra các handle có thể kế thừa.

      .. versionadded:: 3.7

Hằng số Windows
^^^^^^^^^^^^^^^

Mô-đun :mod:`!subprocess` cung cấp các hằng số sau.

.. data:: STD_INPUT_HANDLE

   Thiết bị đầu vào chuẩn. Ban đầu, đây là bộ đệm đầu vào của console, ``CONIN$``.

.. data:: STD_OUTPUT_HANDLE

   Thiết bị đầu ra chuẩn. Ban đầu, đây là bộ đệm màn hình console đang hoạt động, ``CONOUT$``.

.. data:: STD_ERROR_HANDLE

   Thiết bị lỗi chuẩn. Ban đầu, đây là bộ đệm màn hình console đang hoạt động, ``CONOUT$``.

.. data:: SW_HIDE

   Ẩn cửa sổ. Một cửa sổ khác sẽ được kích hoạt.

.. data:: STARTF_USESTDHANDLES

   Chỉ định rằng :attr:`STARTUPINFO.hStdInput`,
   :attr:`STARTUPINFO.hStdOutput`, và các thuộc tính :attr:`STARTUPINFO.hStdError` chứa thông tin bổ sung.

.. data:: STARTF_USESHOWWINDOW

   Chỉ định rằng thuộc tính :attr:`STARTUPINFO.wShowWindow` chứa thông tin bổ sung.

.. data:: STARTF_FORCEONFEEDBACK

   Một tham số :attr:`STARTUPINFO.dwFlags` để chỉ định rằng con trỏ chuột *Working in Background* sẽ được hiển thị trong khi một tiến trình đang khởi chạy. Đây là hành vi mặc định đối với các tiến trình GUI.

   .. versionadded:: 3.13

.. data:: STARTF_FORCEOFFFEEDBACK

   Một tham số :attr:`STARTUPINFO.dwFlags` để chỉ định rằng con trỏ chuột sẽ không thay đổi khi khởi chạy một tiến trình.

   .. versionadded:: 3.13

.. data:: CREATE_NEW_CONSOLE

   Tiến trình mới có một console mới, thay vì kế thừa console của tiến trình cha (mặc định).

.. data:: CREATE_NEW_PROCESS_GROUP

   Một tham số :class:`Popen` ``creationflags`` để chỉ định rằng một nhóm tiến trình mới sẽ được tạo. Cờ này cần thiết để sử dụng :func:`os.kill` trên subprocess.

   Cờ này bị bỏ qua nếu :data:`CREATE_NEW_CONSOLE` được chỉ định.

.. data:: ABOVE_NORMAL_PRIORITY_CLASS

   Tham số :class:`Popen` ``creationflags`` để chỉ định rằng một tiến trình mới sẽ có mức độ ưu tiên cao hơn mức trung bình.

   .. versionadded:: 3.7

.. data:: BELOW_NORMAL_PRIORITY_CLASS

   Tham số :class:`Popen` ``creationflags`` để chỉ định rằng một tiến trình mới sẽ có mức độ ưu tiên thấp hơn mức trung bình.

   .. versionadded:: 3.7

.. data:: HIGH_PRIORITY_CLASS

   Tham số :class:`Popen` ``creationflags`` để chỉ định rằng một tiến trình mới sẽ có mức độ ưu tiên cao.

   .. versionadded:: 3.7

.. data:: IDLE_PRIORITY_CLASS

   Tham số :class:`Popen` ``creationflags`` để chỉ định rằng một tiến trình mới sẽ có mức độ ưu tiên nhàn rỗi (thấp nhất).

   .. versionadded:: 3.7

.. data:: NORMAL_PRIORITY_CLASS

   Tham số :class:`Popen` ``creationflags`` để chỉ định rằng một tiến trình mới sẽ có mức độ ưu tiên bình thường. (mặc định)

   .. versionadded:: 3.7

.. data:: REALTIME_PRIORITY_CLASS

   Tham số :class:`Popen` ``creationflags`` để chỉ định rằng một tiến trình mới sẽ có mức độ ưu tiên realtime. Bạn hầu như không bao giờ nên sử dụng REALTIME_PRIORITY_CLASS, vì điều này làm gián đoạn các system thread quản lý thao tác nhập từ chuột, thao tác nhập từ bàn phím và việc flush đĩa trong nền. Class này có thể phù hợp với các ứng dụng "giao tiếp" trực tiếp với phần cứng hoặc thực hiện các tác vụ ngắn cần bị gián đoạn ở mức tối thiểu.

   .. versionadded:: 3.7

.. data:: CREATE_NO_WINDOW

   Một tham số :class:`Popen` ``creationflags`` để chỉ định rằng một process mới sẽ không tạo cửa sổ.

   .. versionadded:: 3.7

.. data:: DETACHED_PROCESS

   Một tham số :class:`Popen` ``creationflags`` để chỉ định rằng một process mới sẽ không kế thừa console của process cha. Không thể sử dụng giá trị này cùng với CREATE_NEW_CONSOLE.

   .. versionadded:: 3.7

.. data:: CREATE_DEFAULT_ERROR_MODE

   Một tham số :class:`Popen` ``creationflags`` để chỉ định rằng một process mới không kế thừa error mode của process gọi. Thay vào đó, process mới sẽ nhận error mode mặc định. Tính năng này đặc biệt hữu ích cho các ứng dụng shell đa luồng chạy khi hard errors bị vô hiệu hóa.

   .. versionadded:: 3.7

.. data:: CREATE_BREAKAWAY_FROM_JOB

   Một tham số :class:`Popen` ``creationflags`` để chỉ định rằng một process mới không được liên kết với job.

   .. versionadded:: 3.7

.. _call-function-trio:

API cấp cao cũ
--------------

Trước Python 3.5, ba hàm này cấu thành API cấp cao cho subprocess. Hiện nay, trong nhiều trường hợp, bạn có thể sử dụng :func:`run`, nhưng rất nhiều mã hiện có vẫn gọi các hàm này.

.. function:: call(args, *, stdin=None, stdout=None, stderr=None, \
                   shell=False, cwd=None, timeout=None, ****other_popen_kwargs)

   Chạy lệnh được mô tả bởi *args*. Chờ lệnh hoàn tất, sau đó trả về thuộc tính :attr:`~Popen.returncode`.

   Mã cần thu thập stdout hoặc stderr nên sử dụng :func:`run` thay thế::

       run(...).returncode

   Để loại bỏ stdout hoặc stderr, hãy cung cấp giá trị :data:`DEVNULL`.

   Các đối số được trình bày ở trên chỉ là một số đối số thường dùng. Chữ ký hàm đầy đủ giống với chữ ký của hàm khởi tạo :class:`Popen` - hàm này truyền trực tiếp tất cả đối số được cung cấp, ngoại trừ *timeout*, đến interface đó.

   .. note::

      Không sử dụng ``stdout=PIPE`` hoặc ``stderr=PIPE`` với hàm này. Tiến trình con sẽ bị chặn nếu tạo đủ đầu ra vào một pipe để lấp đầy bộ đệm pipe của hệ điều hành, vì các pipe không được đọc.

   .. versionchanged:: 3.3
      Đã thêm *timeout*.

   .. versionchanged:: 3.12

      Đã thay đổi thứ tự tìm kiếm shell của Windows cho ``shell=True``. Thư mục hiện tại và ``%PATH%`` được thay thế bằng ``%COMSPEC%`` và ``%SystemRoot%\System32\cmd.exe``. Do đó, việc đặt một chương trình độc hại có tên ``cmd.exe`` vào thư mục hiện tại sẽ không còn hiệu quả.

.. function:: check_call(args, *, stdin=None, stdout=None, stderr=None, \
                         shell=False, cwd=None, timeout=None, \ ****other_popen_kwargs)

   Chạy lệnh với các đối số. Chờ lệnh hoàn tất. Nếu mã trả về bằng không thì trả về, nếu không thì raise :exc:`CalledProcessError`. Phương thức
   :exc:`CalledProcessError` sẽ có mã trả về trong thuộc tính
   :attr:`~CalledProcessError.returncode`. Nếu :func:`check_call` không thể khởi động tiến trình, nó sẽ truyền tiếp ngoại lệ đã được raised.

   Mã cần thu thập stdout hoặc stderr nên sử dụng :func:`run` thay thế::

       run(..., check=True)

   Để loại bỏ stdout hoặc stderr, hãy cung cấp giá trị :data:`DEVNULL`.

   Các đối số được trình bày ở trên chỉ là một số đối số thường dùng. Chữ ký hàm đầy đủ giống với chữ ký của hàm khởi tạo :class:`Popen` - hàm này truyền trực tiếp tất cả đối số được cung cấp, ngoại trừ *timeout*, đến interface đó.

   .. note::

      Không sử dụng ``stdout=PIPE`` hoặc ``stderr=PIPE`` với hàm này. Tiến trình con sẽ bị chặn nếu tạo đủ đầu ra vào một pipe để lấp đầy bộ đệm pipe của hệ điều hành, vì các pipe không được đọc.

   .. versionchanged:: 3.3
      Đã thêm *timeout*.

   .. versionchanged:: 3.12

      Đã thay đổi thứ tự tìm kiếm shell của Windows cho ``shell=True``. Thư mục hiện tại và ``%PATH%`` được thay thế bằng ``%COMSPEC%`` và ``%SystemRoot%\System32\cmd.exe``. Do đó, việc đặt một chương trình độc hại có tên ``cmd.exe`` vào thư mục hiện tại sẽ không còn hiệu quả.


.. function:: check_output(args, *, stdin=None, stderr=None, shell=False, \
                           cwd=None, encoding=None, errors=None, \ universal_newlines=None, timeout=None, text=None, \ ****other_popen_kwargs)

   Chạy lệnh với các đối số và trả về đầu ra của lệnh.

   Nếu mã trả về khác 0, hàm sẽ raise một :exc:`CalledProcessError`.
   :exc:`CalledProcessError` sẽ có mã trả về trong thuộc tính
   thuộc tính :attr:`~CalledProcessError.returncode` và mọi đầu ra trong
   thuộc tính :attr:`~CalledProcessError.output`.

   Điều này tương đương với::

       run(..., check=True, stdout=PIPE).stdout

   Các đối số được trình bày ở trên chỉ là một số đối số thường dùng. Chữ ký đầy đủ của hàm phần lớn giống với chữ ký của :func:`run` - hầu hết các đối số được truyền trực tiếp đến giao diện đó. Có một điểm khác biệt về API so với hành vi của :func:`run`: truyền ``input=None`` sẽ hoạt động giống như ``input=b''`` (hoặc ``input=''``, tùy thuộc vào các đối số khác) thay vì sử dụng handle tệp đầu vào tiêu chuẩn của tiến trình cha.

   Theo mặc định, hàm này sẽ trả về dữ liệu dưới dạng các byte đã mã hóa. Kiểu mã hóa thực tế của dữ liệu đầu ra có thể phụ thuộc vào lệnh được gọi, vì vậy việc giải mã thành văn bản thường cần được xử lý ở cấp ứng dụng.

   Có thể ghi đè hành vi này bằng cách đặt *text*, *encoding*, *errors*, hoặc *universal_newlines* thành ``True`` như được mô tả trong
   :ref:`frequently-used-arguments` và :func:`run`.

   Để cũng thu thập standard error trong kết quả, hãy sử dụng ``stderr=subprocess.STDOUT``::

      >>> subprocess.check_output(
      ...     "ls non_existent_file; exit 0",
      ...     stderr=subprocess.STDOUT,
      ...     shell=True)
      'ls: non_existent_file: No such file or directory\n'

   .. versionadded:: 3.1

   .. versionchanged:: 3.3
      Đã thêm *timeout*.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho đối số từ khóa *input*.

   .. versionchanged:: 3.6
      Đã bổ sung *encoding* và *errors*. Xem :func:`run` để biết chi tiết.

   .. versionadded:: 3.7
      *text* được bổ sung dưới dạng bí danh dễ đọc hơn cho *universal_newlines*.

   .. versionchanged:: 3.12

      Đã thay đổi thứ tự tìm kiếm shell của Windows cho ``shell=True``. Thư mục hiện tại và ``%PATH%`` được thay thế bằng ``%COMSPEC%`` và ``%SystemRoot%\System32\cmd.exe``. Do đó, việc đặt một chương trình độc hại có tên ``cmd.exe`` vào thư mục hiện tại sẽ không còn hiệu quả.


.. _subprocess-replacements:

Thay thế các hàm cũ bằng mô-đun :mod:`!subprocess`
--------------------------------------------------

Trong phần này, "a trở thành b" có nghĩa là có thể dùng b để thay thế cho a.

.. note::

   Tất cả các hàm "a" trong phần này đều (ít nhiều) âm thầm thất bại nếu không tìm thấy chương trình được thực thi; thay vào đó, các hàm "b" sẽ raise :exc:`OSError`.

   Ngoài ra, các hàm thay thế sử dụng :func:`check_output` sẽ thất bại với một
   :exc:`CalledProcessError` nếu thao tác được yêu cầu tạo ra mã trả về khác không. Kết quả vẫn có sẵn dưới dạng thuộc tính
   :attr:`~CalledProcessError.output` của exception được raise.

Trong các ví dụ sau, giả sử rằng các hàm liên quan đã được import từ module :mod:`!subprocess`.


Thay thế việc thay thế lệnh shell :program:`/bin/sh`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   output=$(mycmd myarg)

trở thành::

   output = check_output(["mycmd", "myarg"])

Thay thế pipeline của shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   output=$(dmesg | grep hda)

trở thành::

   p1 = Popen(["dmesg"], stdout=PIPE)
   p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
   p1.stdout.close()  # Cho phép p1 nhận SIGPIPE nếu p2 thoát.
   output = p2.communicate()[0]

Lệnh gọi ``p1.stdout.close()`` sau khi khởi động p2 rất quan trọng để p1 nhận SIGPIPE nếu p2 thoát trước p1.

Ngoài ra, với đầu vào đáng tin cậy, bạn vẫn có thể sử dụng trực tiếp tính năng pipeline của shell:

.. code-block:: bash

   output=$(dmesg | grep hda)

trở thành::

   output = check_output("dmesg | grep hda", shell=True)


Thay thế :func:`os.system`
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   sts = os.system("mycmd" + " myarg")
   # trở thành
   retcode = call("mycmd" + " myarg", shell=True)

Lưu ý:

* Thông thường không cần gọi chương trình thông qua shell.
* Giá trị trả về của :func:`call` được mã hóa khác với giá trị của
  :func:`os.system`.

* Hàm :func:`os.system` bỏ qua các tín hiệu SIGINT và SIGQUIT trong khi lệnh đang chạy, nhưng người gọi phải tự thực hiện điều này khi sử dụng module :mod:`!subprocess`.

Một ví dụ thực tế hơn sẽ trông như sau::

   try:
       retcode = call("mycmd" + " myarg", shell=True)
       if retcode < 0:
           print("Child was terminated by signal", -retcode, file=sys.stderr)
       else:
           print("Child returned", retcode, file=sys.stderr)
   except OSError as e:
       print("Execution failed:", e, file=sys.stderr)


Thay thế họ :func:`os.spawn <os.spawnl>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ví dụ về P_NOWAIT::

   pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
   ==>
   pid = Popen(["/bin/mycmd", "myarg"]).pid

Ví dụ về P_WAIT::

   retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
   ==>
   retcode = call(["/bin/mycmd", "myarg"])

Ví dụ về vector::

   os.spawnvp(os.P_NOWAIT, path, args)
   ==>
   Popen([path] + args[1:])

Ví dụ về môi trường::

   os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
   ==>
   Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})



Thay thế :func:`os.popen`
^^^^^^^^^^^^^^^^^^^^^^^^^

Xử lý mã trả về được chuyển đổi như sau::

   pipe = os.popen(cmd, 'w')
   ...
   rc = pipe.close()
   if rc is not None and rc >> 8:
       print("There were some errors")
   ==>
   process = Popen(cmd, stdin=PIPE)
   ...
   process.stdin.close()
   if process.wait() != 0:
       print("There were some errors")


Các hàm gọi Shell kế thừa
-------------------------

Mô-đun này cũng cung cấp các hàm kế thừa sau đây từ mô-đun ``commands`` phiên bản 2.x. Các thao tác này ngầm gọi system shell, vì vậy không có bảo đảm nào được mô tả ở trên về tính bảo mật và tính nhất quán trong xử lý ngoại lệ áp dụng cho các hàm này.

.. function:: getstatusoutput(cmd, *, encoding=None, errors=None)

   Trả về ``(exitcode, output)`` của việc thực thi *cmd* trong shell.

   Thực thi chuỗi *cmd* trong shell với :func:`check_output` và trả về một tuple 2 phần tử ``(exitcode, output)``. *encoding* và *errors* được dùng để giải mã đầu ra; xem các ghi chú về :ref:`frequently-used-arguments` để biết thêm chi tiết.

   Ký tự xuống dòng ở cuối được loại bỏ khỏi đầu ra. Mã thoát của lệnh có thể được diễn giải là mã trả về của subprocess.  Ví dụ::

      >>> subprocess.getstatusoutput('ls /bin/ls')
      (0, '/bin/ls')
      >>> subprocess.getstatusoutput('cat /bin/junk')
      (1, 'cat: /bin/junk: No such file or directory')
      >>> subprocess.getstatusoutput('/bin/junk')
      (127, 'sh: /bin/junk: not found')
      >>> subprocess.getstatusoutput('/bin/kill $$')
      (-15, '')

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.3.4
      Đã bổ sung hỗ trợ Windows.

      Hàm hiện trả về (exitcode, output) thay vì (status, output) như trong Python 3.3.3 và các phiên bản cũ hơn.  exitcode có cùng giá trị với
      :attr:`~Popen.returncode`.

   .. versionchanged:: 3.11
      Đã thêm các tham số *encoding* và *errors*.

.. function:: getoutput(cmd, *, encoding=None, errors=None)

   Trả về đầu ra (stdout và stderr) của việc thực thi *cmd* trong shell.

   Tương tự như :func:`getstatusoutput`, ngoại trừ mã thoát bị bỏ qua và giá trị trả về là một chuỗi chứa đầu ra của lệnh. Ví dụ::

      >>> subprocess.getoutput('ls /bin/ls')
      '/bin/ls'

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.3.4
      Đã thêm hỗ trợ Windows

   .. versionchanged:: 3.11
      Đã thêm các tham số *encoding* và *errors*.


Ghi chú
-------

.. _subprocess-timeout-behavior:

Hành vi khi hết thời gian chờ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi sử dụng tham số ``timeout`` trong các hàm như :func:`run`,
:meth:`Popen.wait`, hoặc :meth:`Popen.communicate`, người dùng nên lưu ý các hành vi sau:

1. **Độ trễ khi tạo process**: Bản thân việc tạo process ban đầu không thể bị ngắt trên nhiều API nền tảng. Điều này có nghĩa là ngay cả khi chỉ định timeout, bạn cũng không được đảm bảo sẽ nhận được ngoại lệ timeout cho đến ít nhất là sau khoảng thời gian cần để tạo process.

2. **Giá trị timeout cực nhỏ**: Việc đặt giá trị timeout rất nhỏ (chẳng hạn vài mili giây) có thể dẫn đến các ngoại lệ :exc:`TimeoutExpired` gần như ngay lập tức, vì việc tạo process và lập lịch hệ thống vốn cần có thời gian.

.. _converting-argument-sequence:

Chuyển đổi chuỗi đối số thành một chuỗi trên Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trên Windows, một chuỗi *args* được chuyển đổi thành một chuỗi có thể được phân tích theo các quy tắc sau (tương ứng với các quy tắc được MS C runtime sử dụng):

1. Các đối số được phân tách bằng khoảng trắng, có thể là dấu cách hoặc tab.

2. Một chuỗi được bao quanh bởi dấu ngoặc kép được hiểu là một đối số duy nhất, bất kể khoảng trắng bên trong chuỗi. Một chuỗi được đặt trong dấu ngoặc kép có thể được nhúng trong một đối số.

3. Dấu ngoặc kép được đặt trước bởi dấu gạch chéo ngược được hiểu là một dấu ngoặc kép theo nghĩa đen.

4. Các dấu gạch chéo ngược được hiểu theo nghĩa đen, trừ khi chúng đứng ngay trước một dấu ngoặc kép.

5. Nếu các dấu gạch chéo ngược đứng ngay trước một dấu ngoặc kép, mỗi cặp dấu gạch chéo ngược được hiểu là một dấu gạch chéo ngược theo nghĩa đen. Nếu số lượng dấu gạch chéo ngược là số lẻ, dấu gạch chéo ngược cuối cùng sẽ escape dấu ngoặc kép tiếp theo như được mô tả trong quy tắc 3.


.. seealso::

   :mod:`shlex`
      Module cung cấp các hàm để phân tích cú pháp và escape command line.


.. _disable_posix_spawn:

Tắt việc sử dụng ``posix_spawn()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trên Linux, :mod:`!subprocess` mặc định sử dụng nội bộ system call ``vfork()`` khi có thể thực hiện an toàn, thay vì ``fork()``. Điều này cải thiện đáng kể hiệu suất.

::

   subprocess._USE_POSIX_SPAWN = False  # Xem issue gh-NNNNNN của CPython.

Bạn có thể an toàn đặt giá trị này thành false trên mọi phiên bản Python. Trên các phiên bản cũ hơn hoặc mới hơn, nơi thuộc tính này không được hỗ trợ, việc đặt giá trị sẽ không có tác dụng. Đừng mặc định rằng bạn có thể đọc thuộc tính này. Dù tên gọi là như vậy, giá trị true không cho biết hàm tương ứng sẽ được sử dụng, mà chỉ cho biết hàm đó có thể được sử dụng.

Vui lòng tạo issue mỗi khi bạn phải sử dụng các tùy chọn private này, đồng thời cung cấp cách tái hiện vấn đề đã gặp. Liên kết đến issue đó trong một comment trong mã của bạn.

.. versionadded:: 3.8 ``_USE_POSIX_SPAWN``

.. _`shell injection`: https://en.wikipedia.org/wiki/Shell_injection#Shell_injection
