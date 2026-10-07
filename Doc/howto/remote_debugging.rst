.. _remote-debugging:

Giao thức kết nối gỡ lỗi từ xa
==============================

Giao thức này cho phép các công cụ bên ngoài kết nối với một tiến trình CPython đang chạy và thực thi mã Python từ xa.

Việc kết nối với một tiến trình Python khác có thể yêu cầu thêm quyền hoặc cấu hình, tùy thuộc vào nền tảng.

Tắt gỡ lỗi từ xa
----------------

Để tắt hỗ trợ gỡ lỗi từ xa, hãy sử dụng một trong các cách sau:

* Đặt biến môi trường :envvar:`PYTHON_DISABLE_REMOTE_DEBUG` thành ``1`` trước khi khởi động trình thông dịch.
* Sử dụng tùy chọn dòng lệnh :option:`-X disable_remote_debug`.
* Biên dịch Python với cờ build :option:`--without-remote-debug`.

.. _permission-requirements:

Yêu cầu về quyền
================

Việc đính kèm vào một tiến trình Python đang chạy để remote debugging yêu cầu cấu hình đặc biệt trên hầu hết các nền tảng. Các yêu cầu cụ thể và bước khắc phục sự cố phụ thuộc vào hệ điều hành của bạn:

.. rubric:: Linux

Nhìn chung, bạn có thể debug các tiến trình của chính mình, nhưng có một số cấu hình phổ biến có thể vô hiệu hóa khả năng này. Một số bản phân phối Linux bật **các hạn chế ptrace**, còn gọi là "Yama", như một biện pháp tăng cường bảo mật hệ thống. Các phiên bản gần đây của lệnh ``setpriv`` (util-linux 2.41, phát hành vào tháng 6 năm 2025) cho phép bạn nới lỏng các hạn chế ptrace trên cơ sở từng tiến trình:

  ``setpriv --ptracer any python3``

(Cấu hình này được thiết lập trên tiến trình *đang được debug*.) Bạn cũng có thể tắt các hạn chế ptrace cho tất cả tiến trình cho đến khi khởi động lại bằng:

  ``echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope``

Bạn cũng có thể cấu hình cố định tùy chọn này, thường là trong ``/etc/sysctl.d``.

.. note::

   Việc vô hiệu hóa ``ptrace_scope`` làm giảm mức độ tăng cường bảo mật của hệ thống và chỉ nên được thực hiện trong các môi trường có mức độ bảo mật thấp.

Cũng có khả năng system call ``ptrace`` bị vô hiệu hóa do một bộ lọc bảo mật. Cụ thể, điều này thường xảy ra với các phiên bản cũ của một số phần mềm container. Docker 19.03 trở lên (phát hành năm 2019) và containerd 1.6.7 trở lên (phát hành năm 2022) sẽ tự động cho phép sử dụng system call ``ptrace`` bên trong các container khi chạy trên Linux kernel 4.8 trở lên. Nếu không thể nâng cấp lên các phiên bản này, bạn có thể tạo container bằng một tùy chọn như ``--security-opt seccomp=unconfined`` để vô hiệu hóa bộ lọc bảo mật system call cho container đó. Điều này làm suy yếu khả năng cô lập của container và chỉ nên được thực hiện trong các môi trường có mức độ bảo mật thấp.

Nếu cần trace một process mà bạn *không* sở hữu, bạn sẽ cần quyền superuser hoặc quyền tương đương. Điều này cũng áp dụng cho các process đã thay đổi thông tin xác thực bảo mật, chẳng hạn như các process set-user-ID hoặc set-group-ID (dù trường hợp này không phổ biến đối với Python). Hãy thử chạy lệnh debugging với ``sudo -E``.

.. note::

    Capability ``CAP_SYS_PTRACE`` tương đương với quyền superuser, vì nó cho phép debugging *bất kỳ* process nào, không chỉ process của bạn. Bạn có thể thấy các lời khuyên trên internet đề xuất sử dụng capability này để vượt qua các hạn chế của ptrace hoặc bộ lọc system call. Cách này có thể hiệu quả trên thực tế, cũng như ``sudo``, nhưng nó cấp cho process debugging quyền truy cập nhiều hơn mức cần thiết và chỉ nên được thực hiện trong các môi trường có mức độ bảo mật thấp.

Cuối cùng, hãy lưu ý rằng mỗi process chỉ có thể có một tracer tại một thời điểm. Nếu bạn đã attach vào một process Python bằng ``strace``, ``gdb``, v.v., bạn sẽ không thể đồng thời sử dụng remote debugging. (Quyền superuser cũng không thể vượt qua hạn chế này.)

.. rubric:: macOS

Theo mặc định, macOS vô hiệu hóa khả năng debugging các process khác.

Bạn có thể sửa đổi tệp nhị phân Python để cho phép debug bằng cách cấp cho nó **chữ ký mã ad-hoc** cùng một **entitlement** cho phép debug. (Một "chữ ký" ad-hoc chỉ là một cấu hình không có chữ ký mật mã thực tế và không cần chứng chỉ hay bất kỳ thứ gì khác, chẳng hạn như tư cách thành viên chương trình dành cho nhà phát triển của Apple.)

Các lệnh sau sẽ tạo một tệp ``get-task-allow.plist`` với entitlement cần thiết và thêm tệp đó vào tệp nhị phân Python:

.. code-block:: sh

    echo '{"com.apple.security.get-task-allow": true}' | plutil -convert xml1 -o get-task-allow.plist -
    codesign --sign - --entitlements get-task-allow.plist path/to/bin/python3

trong đó ``path/to/bin/python3`` là đường dẫn đến tệp nhị phân Python của bạn; bạn có thể tìm đường dẫn này, chẳng hạn bằng cách chạy ``which python3`` hoặc đánh giá ``sys.base_executable`` trong Python REPL. (Các hướng dẫn này dành cho bản build Python không sử dụng framework. Các bản build sử dụng framework có thể cần được cấu hình khác.)

Sau đó, bạn sẽ có thể debug các tiến trình Python của chính mình được khởi chạy bằng tệp nhị phân đó.

Ngoài ra, tương tự như trên Linux, các tiến trình có đặc quyền superuser, chẳng hạn như ``sudo``, không chịu kiểm tra này và có thể debug tiến trình của bất kỳ người dùng nào trên hệ thống (mặc dù có các bước kiểm tra bổ sung đối với những tệp nhị phân cụ thể, chẳng hạn như các lệnh do hệ điều hành cung cấp, do System Integrity Protection).

.. rubric:: Windows

Để attach vào một tiến trình khác, bạn thường cần chạy công cụ debug với đặc quyền quản trị. Hãy khởi động command prompt hoặc terminal với quyền Administrator.

Một số tiến trình vẫn có thể không truy cập được ngay cả khi có quyền Administrator, trừ khi bạn đã bật đặc quyền ``SeDebugPrivilege``.

Để giải quyết các vấn đề về quyền truy cập tệp hoặc thư mục, hãy điều chỉnh quyền bảo mật:

  1. Nhấp chuột phải vào tệp hoặc thư mục rồi chọn **Properties**.
  2. Chuyển đến tab **Security** để xem người dùng và nhóm có quyền truy cập.
  3. Nhấp vào **Edit** để sửa đổi quyền.
  4. Chọn tài khoản người dùng của bạn.
  5. Trong **Permissions**, hãy chọn **Read** hoặc **Full control** tùy theo nhu cầu.
  6. Nhấp vào **Apply**, sau đó nhấp vào **OK** để xác nhận.


.. note::

   Hãy đảm bảo bạn đã đáp ứng tất cả :ref:`permission-requirements` trước khi tiếp tục.

Phần này mô tả giao thức cấp thấp cho phép các công cụ bên ngoài chèn và thực thi một tập lệnh Python trong một tiến trình CPython đang chạy.

Cơ chế này là nền tảng của hàm :func:`sys.remote_exec`, hàm này chỉ thị cho một tiến trình Python từ xa thực thi tệp ``.py``. Tuy nhiên, phần này không trình bày cách sử dụng hàm đó. Thay vào đó, phần này giải thích chi tiết giao thức nền tảng, nhận đầu vào là ``pid`` của một tiến trình Python đích và đường dẫn đến tệp mã nguồn Python cần thực thi. Thông tin này hỗ trợ việc tái triển khai độc lập giao thức, bất kể ngôn ngữ lập trình được sử dụng.

.. warning::

    Việc thực thi tập lệnh đã chèn phụ thuộc vào việc trình thông dịch đạt đến một điểm đánh giá an toàn. Do đó, quá trình thực thi có thể bị trì hoãn tùy thuộc vào trạng thái runtime của tiến trình đích.

Sau khi được chèn, tập lệnh sẽ được trình thông dịch thực thi trong tiến trình đích vào lần tiếp theo đạt đến một điểm đánh giá an toàn. Cách tiếp cận này cho phép thực thi từ xa mà không sửa đổi hành vi hoặc cấu trúc của ứng dụng Python đang chạy.

Các phần tiếp theo mô tả giao thức theo từng bước, bao gồm các kỹ thuật định vị cấu trúc của trình thông dịch trong bộ nhớ, truy cập an toàn các trường nội bộ và kích hoạt việc thực thi mã. Các biến thể dành riêng cho từng nền tảng được ghi chú khi thích hợp, đồng thời các bản triển khai mẫu được đưa vào để làm rõ từng thao tác.

Xác định cấu trúc PyRuntime
===========================

CPython đặt cấu trúc ``PyRuntime`` trong một phần nhị phân riêng để giúp các công cụ bên ngoài tìm thấy cấu trúc này khi runtime đang chạy. Tên và định dạng của phần này thay đổi tùy theo nền tảng. Ví dụ, ``.PyRuntime`` được sử dụng trên các hệ thống ELF, còn ``__DATA,__PyRuntime`` được sử dụng trên macOS. Các công cụ có thể tìm vị trí bắt đầu của cấu trúc này bằng cách kiểm tra tệp nhị phân trên đĩa.

Cấu trúc ``PyRuntime`` chứa trạng thái trình thông dịch toàn cục của CPython và cung cấp quyền truy cập vào các dữ liệu nội bộ khác, bao gồm danh sách các trình thông dịch, trạng thái luồng và các trường hỗ trợ trình gỡ lỗi.

Để làm việc với một tiến trình Python từ xa, trình gỡ lỗi trước tiên phải tìm địa chỉ bộ nhớ của cấu trúc ``PyRuntime`` trong tiến trình đích. Không thể hardcode hoặc tính toán địa chỉ này từ tên symbol, vì địa chỉ này phụ thuộc vào vị trí hệ điều hành đã nạp tệp nhị phân.

Phương pháp tìm ``PyRuntime`` phụ thuộc vào nền tảng, nhưng nhìn chung các bước giống nhau:

1. Tìm địa chỉ cơ sở nơi tệp nhị phân Python hoặc shared library được nạp trong tiến trình đích.
2. Sử dụng tệp nhị phân trên đĩa để xác định vị trí bắt đầu của phần ``.PyRuntime``.
3. Cộng độ lệch của section vào địa chỉ cơ sở để tính địa chỉ trong bộ nhớ.

Các section bên dưới giải thích cách thực hiện việc này trên từng nền tảng được hỗ trợ và bao gồm mã ví dụ.

.. rubric:: Linux (ELF)

Để tìm cấu trúc ``PyRuntime`` trên Linux:

1. Đọc memory map của process (ví dụ: ``/proc/<pid>/maps``) để tìm địa chỉ nơi tệp thực thi Python hoặc ``libpython`` được nạp.
2. Phân tích các section header ELF trong binary để lấy độ lệch của section ``.PyRuntime``.
3. Cộng độ lệch đó vào địa chỉ cơ sở từ bước 1 để lấy địa chỉ trong bộ nhớ của ``PyRuntime``.

Sau đây là một cách triển khai mẫu::

    def find_py_runtime_linux(pid: int) -> int:
        # Bước 1: Thử tìm tệp thực thi Python trong bộ nhớ
        binary_path, base_address = find_mapped_binary(
            pid, name_contains="python"
        )

        # Bước 2: Dùng thư viện dùng chung dự phòng nếu không tìm thấy tệp thực thi
        if binary_path is None:
            binary_path, base_address = find_mapped_binary(
                pid, name_contains="libpython"
            )

        # Bước 3: Phân tích các tiêu đề ELF để lấy độ lệch của section .PyRuntime
        section_offset = parse_elf_section_offset(
            binary_path, ".PyRuntime"
        )

        # Bước 4: Tính địa chỉ PyRuntime trong bộ nhớ
        return base_address + section_offset


Trên các hệ thống Linux, có hai cách chính để đọc bộ nhớ từ một tiến trình khác. Cách đầu tiên là thông qua hệ thống tệp ``/proc``, cụ thể là đọc từ ``/proc/[pid]/mem``, nơi cung cấp quyền truy cập trực tiếp vào bộ nhớ của tiến trình. Cách này yêu cầu quyền phù hợp — entweder là cùng người dùng với tiến trình đích hoặc có quyền root. Cách thứ hai là sử dụng system call ``process_vm_readv()``, cung cấp phương thức hiệu quả hơn để sao chép bộ nhớ giữa các tiến trình. Mặc dù cũng có thể sử dụng thao tác ``PTRACE_PEEKTEXT`` của ptrace để đọc bộ nhớ, cách này chậm hơn đáng kể vì mỗi lần chỉ đọc một word và yêu cầu nhiều lần chuyển đổi context giữa các tiến trình tracer và tracee.

Để phân tích các section ELF, quy trình này bao gồm việc đọc và diễn giải các cấu trúc của định dạng tệp ELF từ tệp nhị phân trên đĩa. Tiêu đề ELF chứa một con trỏ đến bảng tiêu đề section. Mỗi tiêu đề section chứa metadata về một section, bao gồm tên của section đó (được lưu trong một string table riêng), độ lệch và kích thước. Để tìm một section cụ thể như .PyRuntime, bạn cần duyệt qua các tiêu đề này và đối chiếu tên section. Sau đó, tiêu đề section cung cấp độ lệch tại đó section tồn tại trong tệp, có thể dùng để tính địa chỉ runtime của section khi tệp nhị phân được nạp vào bộ nhớ.

Bạn có thể đọc thêm về định dạng tệp ELF trong `đặc tả ELF <https://en.wikipedia.org/wiki/Executable_and_Linkable_Format>`_.


.. rubric:: macOS (Mach-O)

Để tìm cấu trúc ``PyRuntime`` trên macOS:

1. Gọi ``task_for_pid()`` để lấy ``mach_port_t`` task port của tiến trình đích. Handle này cần thiết để đọc bộ nhớ bằng các API như ``mach_vm_read_overwrite`` và ``mach_vm_region``.
2. Quét các vùng bộ nhớ để tìm vùng chứa tệp thực thi Python hoặc ``libpython``.
3. Tải tệp nhị phân từ đĩa và phân tích các header Mach-O để tìm section có tên ``PyRuntime`` trong segment ``__DATA``. Trên macOS, tên symbol được tự động thêm tiền tố dấu gạch dưới, vì vậy symbol ``PyRuntime`` xuất hiện dưới dạng ``_PyRuntime`` trong symbol table, nhưng tên section không bị ảnh hưởng.

Sau đây là một cách triển khai mẫu::

    def find_py_runtime_macos(pid: int) -> int:
        # Bước 1: Truy cập bộ nhớ của tiến trình
        handle = get_memory_access_handle(pid)

        # Bước 2: Thử tìm tệp thực thi Python trong bộ nhớ
        binary_path, base_address = find_mapped_binary(
            handle, name_contains="python"
        )

        # Bước 3: Dùng libpython dự phòng nếu không tìm thấy tệp thực thi
        if binary_path is None:
            binary_path, base_address = find_mapped_binary(
                handle, name_contains="libpython"
            )

        # Bước 4: Phân tích các header Mach-O để lấy offset của section __DATA,__PyRuntime
        section_offset = parse_macho_section_offset(
            binary_path, "__DATA", "__PyRuntime"
        )

        # Bước 5: Tính địa chỉ PyRuntime trong bộ nhớ
        return base_address + section_offset

Trên macOS, để truy cập bộ nhớ của một tiến trình khác, cần sử dụng các API và định dạng tệp đặc thù của Mach-O. Bước đầu tiên là lấy một handle ``task_port`` thông qua ``task_for_pid()``, cung cấp quyền truy cập vào không gian bộ nhớ của tiến trình đích. Handle này cho phép thực hiện các thao tác trên bộ nhớ thông qua những API như ``mach_vm_read_overwrite()``.

Có thể kiểm tra bộ nhớ tiến trình bằng ``mach_vm_region()`` để quét qua không gian bộ nhớ ảo, trong khi ``proc_regionfilename()`` giúp xác định những tệp nhị phân nào được tải vào từng vùng bộ nhớ. Khi tìm thấy tệp nhị phân hoặc thư viện Python, cần phân tích các header Mach-O của tệp đó để định vị cấu trúc ``PyRuntime``.

Định dạng Mach-O tổ chức mã và dữ liệu thành các segment và section. Cấu trúc ``PyRuntime`` nằm trong một section có tên ``__PyRuntime`` thuộc segment ``__DATA``. Việc tính địa chỉ runtime thực tế bao gồm tìm segment ``__TEXT``, đóng vai trò là địa chỉ cơ sở của binary, sau đó định vị segment ``__DATA`` chứa section mục tiêu. Địa chỉ cuối cùng được tính bằng cách kết hợp địa chỉ cơ sở với các offset section thích hợp từ các header Mach-O.

Lưu ý rằng việc truy cập bộ nhớ của một process khác trên macOS thường yêu cầu quyền nâng cao - có thể là quyền root hoặc các security entitlement đặc biệt được cấp cho process debug.


.. rubric:: Windows (PE)

Để tìm cấu trúc ``PyRuntime`` trên Windows:

1. Sử dụng ToolHelp API để liệt kê tất cả module được load trong process đích. Việc này được thực hiện bằng các hàm như `CreateToolhelp32Snapshot <https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot>`_, `Module32First <https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-module32first>`_ và `Module32Next <https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-module32next>`_.
2. Xác định module tương ứng với :file:`python.exe` hoặc
   :file:`python{XY}.dll`, trong đó ``X`` và ``Y`` là số phiên bản major và minor của phiên bản Python, rồi ghi lại địa chỉ cơ sở của module.
3. Xác định phần ``PyRuntim``. Do định dạng PE giới hạn tên phần ở 8 ký tự (được định nghĩa là ``IMAGE_SIZEOF_SHORT_NAME``), tên gốc ``PyRuntime`` đã bị cắt ngắn. Phần này chứa cấu trúc ``PyRuntime``.
4. Lấy địa chỉ ảo tương đối (RVA) của phần đó và cộng địa chỉ này với địa chỉ cơ sở của module.

Sau đây là một cách triển khai mẫu::

    def find_py_runtime_windows(pid: int) -> int:
        # Bước 1: Thử tìm tệp thực thi Python trong bộ nhớ
        binary_path, base_address = find_loaded_module(
            pid, name_contains="python"
        )

        # Bước 2: Dự phòng sử dụng pythonXY.dll dùng chung nếu tệp thực thi không được
        # tìm thấy
        if binary_path is None:
            binary_path, base_address = find_loaded_module(
                pid, name_contains="python3"
            )

        # Bước 3: Phân tích các tiêu đề phần PE để lấy RVA của PyRuntime
        # phần. Tên phần xuất hiện là "PyRuntim" do
        # giới hạn 8 ký tự được định nghĩa bởi định dạng PE (IMAGE_SIZEOF_SHORT_NAME).
        section_rva = parse_pe_section_offset(binary_path, "PyRuntim")

        # Bước 4: Tính địa chỉ PyRuntime trong bộ nhớ
        return base_address + section_rva


Trên Windows, việc truy cập bộ nhớ của một tiến trình khác yêu cầu sử dụng các hàm Windows API như ``CreateToolhelp32Snapshot()`` và ``Module32First()/Module32Next()`` để liệt kê các module đã được tải. Hàm ``OpenProcess()`` cung cấp một handle để truy cập không gian bộ nhớ của tiến trình đích, cho phép thực hiện các thao tác bộ nhớ thông qua ``ReadProcessMemory()``.

Có thể kiểm tra bộ nhớ tiến trình bằng cách liệt kê các module đã được tải để tìm binary hoặc DLL của Python. Khi tìm thấy, cần phân tích các PE header của nó để định vị cấu trúc ``PyRuntime``.

Định dạng PE tổ chức mã và dữ liệu thành các section. Cấu trúc ``PyRuntime`` nằm trong một section có tên "PyRuntim" (bị rút ngắn từ "PyRuntime" do giới hạn tên 8 ký tự của PE). Việc tính địa chỉ runtime thực tế bao gồm tìm địa chỉ cơ sở của module từ mục nhập module, sau đó định vị section đích trong các PE header. Địa chỉ cuối cùng được tính bằng cách kết hợp địa chỉ cơ sở với địa chỉ ảo của section từ các PE section header.

Lưu ý rằng việc truy cập bộ nhớ của một tiến trình khác trên Windows thường yêu cầu các đặc quyền phù hợp - либо quyền quản trị hoặc đặc quyền ``SeDebugPrivilege`` được cấp cho tiến trình debug.


Đọc _Py_DebugOffsets
====================

Sau khi xác định được địa chỉ của cấu trúc ``PyRuntime``, bước tiếp theo là đọc cấu trúc ``_Py_DebugOffsets`` nằm ở phần đầu của khối ``PyRuntime``.

Cấu trúc này cung cấp các offset của trường (field offset) dành riêng cho từng phiên bản, cần thiết để đọc an toàn bộ nhớ trạng thái của interpreter và thread. Các offset này thay đổi giữa các phiên bản CPython và phải được kiểm tra trước khi sử dụng để đảm bảo chúng tương thích.

Để đọc và kiểm tra các debug offset, hãy thực hiện các bước sau:

1. Đọc bộ nhớ từ process đích, bắt đầu tại địa chỉ ``PyRuntime``, với số byte bằng với kích thước của cấu trúc ``_Py_DebugOffsets``. Cấu trúc này nằm ngay tại phần đầu của khối bộ nhớ ``PyRuntime``. Bố cục của cấu trúc được định nghĩa trong các header nội bộ của CPython và không thay đổi trong cùng một phiên bản minor, nhưng có thể thay đổi giữa các phiên bản major.

2. Kiểm tra để đảm bảo cấu trúc chứa dữ liệu hợp lệ:

   - Trường ``cookie`` phải khớp với debug marker dự kiến.
   - Trường ``version`` phải khớp với phiên bản trình thông dịch Python được debugger sử dụng.
   - Nếu debugger hoặc tiến trình đích đang sử dụng phiên bản phát hành trước (ví dụ: alpha, beta hoặc release candidate), các phiên bản phải khớp chính xác.
   - Trường ``free_threaded`` phải có cùng giá trị trong cả debugger và tiến trình đích.

3. Nếu cấu trúc hợp lệ, có thể sử dụng các offset mà cấu trúc chứa để định vị các trường trong bộ nhớ. Nếu bất kỳ bước kiểm tra nào không thành công, debugger nên dừng thao tác để tránh đọc bộ nhớ theo sai định dạng.

Sau đây là một triển khai mẫu đọc và kiểm tra ``_Py_DebugOffsets``::

    def read_debug_offsets(pid: int, py_runtime_addr: int) -> DebugOffsets:
        # Bước 1: Đọc bộ nhớ từ tiến trình đích tại địa chỉ PyRuntime
        data = read_process_memory(
            pid, address=py_runtime_addr, size=DEBUG_OFFSETS_SIZE
        )

        # Bước 2: Deserialize các byte thô thành cấu trúc _Py_DebugOffsets
        debug_offsets = parse_debug_offsets(data)

        # Bước 3: Xác thực nội dung của cấu trúc
        if debug_offsets.cookie != EXPECTED_COOKIE:
            raise RuntimeError("Invalid or missing debug cookie")
        if debug_offsets.version != LOCAL_PYTHON_VERSION:
            raise RuntimeError(
                "Mismatch between caller and target Python versions"
            )
        if debug_offsets.free_threaded != LOCAL_FREE_THREADED:
            raise RuntimeError("Mismatch in free-threaded configuration")

        return debug_offsets



.. warning::

   **Khuyến nghị tạm dừng tiến trình**

   Để tránh điều kiện tranh chấp và đảm bảo tính nhất quán của bộ nhớ, chúng tôi đặc biệt khuyến nghị tạm dừng tiến trình đích trước khi thực hiện bất kỳ thao tác nào đọc hoặc ghi trạng thái nội bộ của interpreter. Python runtime có thể đồng thời thay đổi các cấu trúc dữ liệu của interpreter—chẳng hạn như tạo hoặc hủy thread—trong quá trình thực thi bình thường. Điều này có thể dẫn đến việc đọc hoặc ghi bộ nhớ không hợp lệ.

   Debugger có thể tạm dừng quá trình thực thi bằng cách attach vào tiến trình bằng ``ptrace`` hoặc gửi tín hiệu ``SIGSTOP``. Chỉ nên tiếp tục thực thi sau khi các thao tác bộ nhớ phía debugger hoàn tất.

   .. note::

      Một số công cụ, chẳng hạn như profiler hoặc debugger dựa trên sampling, có thể hoạt động trên một tiến trình đang chạy mà không cần tạm dừng. Trong những trường hợp đó, công cụ phải được thiết kế rõ ràng để xử lý bộ nhớ được cập nhật một phần hoặc không nhất quán. Đối với hầu hết các triển khai debugger, tạm dừng tiến trình vẫn là cách an toàn và đáng tin cậy nhất.


Định vị interpreter và trạng thái thread
========================================

Trước khi có thể inject và thực thi code trong một tiến trình Python từ xa, debugger phải chọn một thread để lên lịch thực thi. Điều này là cần thiết vì các trường điều khiển được dùng để thực hiện việc inject code từ xa nằm trong cấu trúc ``_PyRemoteDebuggerSupport``, được nhúng trong một đối tượng ``PyThreadState``. Debugger sửa đổi các trường này để yêu cầu thực thi các script đã inject.

Cấu trúc ``PyThreadState`` đại diện cho một thread đang chạy bên trong trình thông dịch Python. Cấu trúc này duy trì context đánh giá của thread và chứa các trường cần thiết để debugger phối hợp hoạt động. Do đó, việc định vị một ``PyThreadState`` hợp lệ là điều kiện tiên quyết quan trọng để kích hoạt quá trình thực thi từ xa.

Một thread thường được chọn dựa trên vai trò hoặc ID của nó. Trong hầu hết trường hợp, main thread được sử dụng, nhưng một số công cụ có thể nhắm đến một thread cụ thể thông qua native thread ID của thread đó. Sau khi chọn thread đích, debugger phải định vị cả interpreter và các cấu trúc thread state liên kết trong bộ nhớ.

Các cấu trúc nội bộ liên quan được định nghĩa như sau:

- ``PyInterpreterState`` đại diện cho một phiên bản interpreter Python độc lập. Mỗi interpreter duy trì tập hợp riêng gồm các module đã import, trạng thái built-in và danh sách thread state. Mặc dù hầu hết ứng dụng Python chỉ sử dụng một interpreter, CPython hỗ trợ nhiều interpreter trong cùng một process.

- ``PyThreadState`` đại diện cho một thread đang chạy trong một interpreter. Nó chứa trạng thái thực thi và các trường điều khiển được debugger sử dụng.

Để định vị một thread:

1. Sử dụng offset ``runtime_state.interpreters_head`` để lấy địa chỉ của interpreter đầu tiên trong cấu trúc ``PyRuntime``. Đây là điểm bắt đầu của danh sách liên kết các interpreter đang hoạt động.

2. Sử dụng offset ``interpreter_state.threads_main`` để truy cập trạng thái luồng chính liên kết với interpreter đã chọn. Đây thường là luồng đáng tin cậy nhất để nhắm đến.

3. Tùy chọn, sử dụng offset ``interpreter_state.threads_head`` để duyệt qua linked list chứa tất cả trạng thái luồng. Mỗi cấu trúc ``PyThreadState`` chứa một trường ``native_thread_id``, có thể được so sánh với ID luồng đích để tìm một luồng cụ thể.

4. Sau khi tìm thấy một ``PyThreadState`` hợp lệ, địa chỉ của nó có thể được sử dụng trong các bước tiếp theo của giao thức, chẳng hạn như ghi các trường điều khiển debugger và lập lịch thực thi.

Sau đây là một triển khai mẫu để định vị trạng thái luồng chính::

    def find_main_thread_state(
        pid: int, py_runtime_addr: int, debug_offsets: DebugOffsets,
    ) -> int:
        # Bước 1: Đọc interpreters_head từ PyRuntime
        interp_head_ptr = (
            py_runtime_addr + debug_offsets.runtime_state.interpreters_head
        )
        interp_addr = read_pointer(pid, interp_head_ptr)
        if interp_addr == 0:
            raise RuntimeError("No interpreter found in the target process")

        # Bước 2: Đọc con trỏ threads_main từ interpreter
        threads_main_ptr = (
            interp_addr + debug_offsets.interpreter_state.threads_main
        )
        thread_state_addr = read_pointer(pid, threads_main_ptr)
        if thread_state_addr == 0:
            raise RuntimeError("Main thread state is not available")

        return thread_state_addr

Ví dụ sau minh họa cách định vị một luồng theo ID luồng gốc của nó::

    def find_thread_by_id(
        pid: int,
        interp_addr: int,
        debug_offsets: DebugOffsets,
        target_tid: int,
    ) -> int:
        # Bắt đầu tại threads_head và duyệt danh sách liên kết
        thread_ptr = read_pointer(
            pid,
            interp_addr + debug_offsets.interpreter_state.threads_head
        )

        while thread_ptr:
            native_tid_ptr = (
                thread_ptr + debug_offsets.thread_state.native_thread_id
            )
            native_tid = read_int(pid, native_tid_ptr)
            if native_tid == target_tid:
                return thread_ptr
            thread_ptr = read_pointer(
                pid,
                thread_ptr + debug_offsets.thread_state.next
            )

        raise RuntimeError("Thread with the given ID was not found")


Sau khi đã xác định được trạng thái luồng hợp lệ, trình gỡ lỗi có thể tiến hành sửa đổi các trường điều khiển của trạng thái đó và lập lịch thực thi, như mô tả trong phần tiếp theo.

Ghi thông tin điều khiển
========================

Sau khi đã xác định được cấu trúc ``PyThreadState`` hợp lệ, trình gỡ lỗi có thể sửa đổi các trường điều khiển bên trong cấu trúc này để lập lịch thực thi một tập lệnh Python cụ thể. Trình thông dịch kiểm tra định kỳ các trường điều khiển này; khi được thiết lập chính xác, chúng sẽ kích hoạt việc thực thi mã từ xa tại một điểm an toàn trong vòng lặp đánh giá.

Mỗi ``PyThreadState`` chứa một cấu trúc ``_PyRemoteDebuggerSupport`` được dùng để giao tiếp giữa trình gỡ lỗi và trình thông dịch. Vị trí các trường của cấu trúc này được xác định bởi cấu trúc ``_Py_DebugOffsets`` và bao gồm các trường sau:

- ``debugger_script_path``: Một bộ đệm có kích thước cố định chứa đường dẫn đầy đủ đến tệp mã nguồn Python (``.py``). Tệp này phải có thể được tiến trình đích truy cập và đọc khi quá trình thực thi được kích hoạt.

- ``debugger_pending_call``: Một cờ số nguyên. Đặt giá trị này thành ``1`` để báo cho trình thông dịch rằng một tập lệnh đã sẵn sàng được thực thi.

- ``eval_breaker``: Một trường được trình thông dịch kiểm tra trong quá trình thực thi. Việc đặt bit 5 (``_PY_EVAL_PLEASE_STOP_BIT``, giá trị ``1U << 5``) trong trường này khiến trình thông dịch tạm dừng và kiểm tra hoạt động của trình gỡ lỗi.

Để hoàn tất việc injection, trình gỡ lỗi phải thực hiện các bước sau:

1. Ghi đường dẫn đầy đủ của script vào bộ đệm ``debugger_script_path``.
2. Đặt ``debugger_pending_call`` thành ``1``.
3. Đọc giá trị hiện tại của ``eval_breaker``, đặt bit 5 (``_PY_EVAL_PLEASE_STOP_BIT``), rồi ghi lại giá trị đã cập nhật. Thao tác này báo cho trình thông dịch kiểm tra hoạt động của trình gỡ lỗi.

Sau đây là một cách triển khai ví dụ::

    def inject_script(
        pid: int,
        thread_state_addr: int,
        debug_offsets: DebugOffsets,
        script_path: str
    ) -> None:
        # Tính toán offset cơ sở của _PyRemoteDebuggerSupport
        support_base = (
            thread_state_addr +
            debug_offsets.debugger_support.remote_debugger_support
        )

        # Bước 1: Ghi đường dẫn script vào debugger_script_path
        script_path_ptr = (
            support_base +
            debug_offsets.debugger_support.debugger_script_path
        )
        write_string(pid, script_path_ptr, script_path)

        # Bước 2: Đặt debugger_pending_call thành 1
        pending_ptr = (
            support_base +
            debug_offsets.debugger_support.debugger_pending_call
        )
        write_int(pid, pending_ptr, 1)

        # Bước 3: Đặt _PY_EVAL_PLEASE_STOP_BIT (bit 5, giá trị 1 << 5) trong
        # eval_breaker
        eval_breaker_ptr = (
            thread_state_addr +
            debug_offsets.debugger_support.eval_breaker
        )
        breaker = read_int(pid, eval_breaker_ptr)
        breaker |= (1 << 5)
        write_int(pid, eval_breaker_ptr, breaker)


Sau khi các trường này được thiết lập, debugger có thể tiếp tục tiến trình (nếu tiến trình đang bị tạm dừng). Interpreter sẽ xử lý yêu cầu tại điểm đánh giá an toàn tiếp theo, tải script từ đĩa và thực thi script.

Debugger có trách nhiệm đảm bảo tệp script vẫn tồn tại và có thể được tiến trình đích truy cập trong quá trình thực thi.

.. note::

   Việc thực thi script là bất đồng bộ. Không thể xóa tệp script ngay sau khi injection. Debugger nên chờ cho đến khi script được inject tạo ra một hiệu ứng có thể quan sát được rồi mới xóa tệp. Hiệu ứng này phụ thuộc vào chức năng mà script được thiết kế để thực hiện. Ví dụ, debugger có thể chờ đến khi tiến trình từ xa kết nối trở lại một socket rồi mới xóa script. Khi quan sát thấy hiệu ứng như vậy, có thể an toàn giả định rằng tệp không còn cần thiết nữa.

Tóm tắt
=======

Để inject và thực thi một Python script trong một process từ xa:

1. Xác định cấu trúc ``PyRuntime`` trong bộ nhớ của process đích.
2. Đọc và xác thực cấu trúc ``_Py_DebugOffsets`` ở đầu ``PyRuntime``.
3. Sử dụng các offset để xác định một ``PyThreadState`` hợp lệ.
4. Ghi đường dẫn đến một Python script vào ``debugger_script_path``.
5. Đặt cờ ``debugger_pending_call`` thành ``1``.
6. Đặt ``_PY_EVAL_PLEASE_STOP_BIT`` trong trường ``eval_breaker``.
7. Tiếp tục quy trình (nếu bị tạm dừng). Script sẽ thực thi tại điểm đánh giá an toàn tiếp theo.

.. _remote-debugging-threat-model:

Mô hình bảo mật và mối đe dọa
=============================

Giao thức gỡ lỗi từ xa dựa vào các cơ chế nguyên thủy của hệ điều hành giống như những cơ chế được các trình gỡ lỗi native như GDB và LLDB sử dụng. Việc đính kèm vào một quy trình yêu cầu **cùng đặc quyền** mà các trình gỡ lỗi đó yêu cầu, chẳng hạn như ``ptrace`` / Yama LSM trên Linux, ``task_for_pid`` trên macOS và ``SeDebugPrivilege`` trên Windows. Python không tạo thêm bất kỳ đường dẫn nâng quyền nào; nếu kẻ tấn công đã có các quyền cần thiết để đính kèm vào một quy trình, họ cũng có thể sử dụng GDB để đọc bộ nhớ hoặc chèn mã.

Các nguyên tắc sau đây xác định điều gì được và không được xem là lỗ hổng bảo mật trong tính năng này:

Việc đính kèm yêu cầu đặc quyền cấp hệ điều hành
   Trên mọi nền tảng được hỗ trợ, hệ điều hành kiểm soát quyền truy cập bộ nhớ giữa các quy trình thông qua các bước kiểm tra đặc quyền (``CAP_SYS_PTRACE``, quyền root hoặc quyền quản trị viên). Một báo cáo chỉ cho thấy sự cố sau khi các đặc quyền này đã được cấp là **không** phải là một lỗ hổng trong CPython, vì ranh giới bảo mật của hệ điều hành đã bị vượt qua.

Sự cố hoặc lỗi bộ nhớ khi đọc một tiến trình bị xâm phạm không phải là lỗ hổng
   Một công cụ đọc trạng thái nội bộ của interpreter từ một tiến trình đích phải tin rằng vùng nhớ đó có cấu trúc hợp lệ. Nếu tiến trình đích đã bị hỏng hoặc do kẻ tấn công kiểm soát, debugger hoặc profiler có thể bị crash, tạo ra đầu ra rác hoặc hoạt động không thể dự đoán. Đây cũng là rủi ro được mọi debugger dựa trên ``ptrace`` chấp nhận. Các lỗi thuộc nhóm này (tràn bộ đệm, lỗi phân đoạn hoặc hành vi không xác định do đọc trạng thái bị hỏng) **không** được xem là vấn đề bảo mật, dù vẫn hoan nghênh các bản sửa giúp tăng độ ổn định.

Các lỗ hổng trong tiến trình đích không thuộc phạm vi xử lý
   Nếu tiến trình Python đang được debug đã bị xâm phạm, kẻ tấn công đã kiểm soát việc thực thi trong tiến trình đó. Việc chứng minh tác động bổ sung từ điểm khởi đầu này không cấu thành lỗ hổng trong giao thức remote debugging.

Khi nào nên sử dụng ``PYTHON_DISABLE_REMOTE_DEBUG``
---------------------------------------------------

Biến môi trường :envvar:`PYTHON_DISABLE_REMOTE_DEBUG` (và cờ :option:`-X disable_remote_debug` tương đương) cho phép người vận hành vô hiệu hóa phía in-process của giao thức như một biện pháp **phòng thủ nhiều lớp**. Điều này có thể hữu ích trong các môi trường triển khai được harden hoặc sandbox, nơi không dự kiến debug hay profiling tiến trình và việc giảm bề mặt tấn công là ưu tiên, dù các bước kiểm tra đặc quyền ở cấp hệ điều hành đã ngăn truy cập không có đặc quyền.

Việc đặt biến này **không** ảnh hưởng đến các giao diện debugging khác ở cấp hệ điều hành (``ptrace``, ``/proc``, ``task_for_pid``, v.v.), vốn vẫn khả dụng theo các mô hình quyền riêng của chúng.

.. _`ELF specification`: https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
.. _`CreateToolhelp32Snapshot`: https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
.. _`Module32First`: https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-module32first
.. _`Module32Next`: https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-module32next
