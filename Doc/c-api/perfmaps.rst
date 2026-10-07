.. highlight:: c

.. _perfmaps:

Hỗ trợ Perf Maps
----------------

Trên các nền tảng được hỗ trợ (tại thời điểm viết tài liệu này, chỉ có Linux), runtime có thể tận dụng *các tệp perf map* để hiển thị các hàm Python trong một công cụ profiling bên ngoài (chẳng hạn như `perf <https://perf.wiki.kernel.org/index.php/Main_Page>`_). Một tiến trình đang chạy có thể tạo một tệp trong thư mục ``/tmp``, tệp này chứa các mục có thể ánh xạ một đoạn mã thực thi với một tên. Giao diện này được mô tả trong `tài liệu về công cụ Linux Perf <https://git.kernel.org/pub/scm/linux/ kernel/git/torvalds/linux.git/tree/tools/perf/Documentation/jit-interface.txt>`_.

Trong Python, các helper API này có thể được các thư viện và tính năng dựa vào việc tạo mã máy ngay trong lúc chạy sử dụng.

Lưu ý rằng không cần phải nắm giữ :term:`attached thread state` để sử dụng các API này.

.. c:function:: int PyUnstable_PerfMapState_Init(void)

   Mở tệp ``/tmp/perf-$pid.map``, trừ khi tệp đã được mở, rồi tạo một lock để đảm bảo việc ghi vào tệp an toàn đối với thread (với điều kiện việc ghi được thực hiện thông qua :c:func:`PyUnstable_WritePerfMapEntry`). Thông thường, bạn không cần gọi hàm này một cách rõ ràng; chỉ cần sử dụng :c:func:`PyUnstable_WritePerfMapEntry` và trạng thái sẽ được khởi tạo trong lần gọi đầu tiên.

   Trả về ``0`` nếu thành công, ``-1`` nếu không tạo hoặc mở được tệp perf map, hoặc ``-2`` nếu không tạo được lock. Kiểm tra ``errno`` để biết thêm thông tin về nguyên nhân gây ra lỗi.

.. c:function:: int PyUnstable_WritePerfMapEntry(const void *code_addr, unsigned int code_size, const char *entry_name)

   Ghi một mục duy nhất vào tệp ``/tmp/perf-$pid.map``. Hàm này an toàn đối với thread. Dưới đây là một mục mẫu::

      # địa chỉ      kích thước  tên
      7f3529fcf759 b     py::bar:/run/t.py

   Sẽ gọi :c:func:`PyUnstable_PerfMapState_Init` trước khi ghi mục nhập, nếu tệp perf map chưa được mở. Trả về ``0`` khi thành công hoặc các mã lỗi giống như :c:func:`PyUnstable_PerfMapState_Init` khi thất bại.

.. c:function:: void PyUnstable_PerfMapState_Fini(void)

   Đóng tệp perf map được mở bởi :c:func:`PyUnstable_PerfMapState_Init`. Runtime tự gọi hàm này trong quá trình tắt trình thông dịch. Nhìn chung, không có lý do gì để gọi hàm này một cách rõ ràng, ngoại trừ việc xử lý các tình huống cụ thể như tạo fork.

.. c:function:: int PyUnstable_CopyPerfMapFile(const char *parent_filename)

   Mở tệp ``/tmp/perf-$pid.map`` và nối nội dung của *parent_filename* vào tệp đó.

   Hàm này khả dụng trên mọi nền tảng nhưng chỉ tạo đầu ra trên các nền tảng hỗ trợ perf map (hiện tại chỉ có Linux). Trên các nền tảng khác, hàm không thực hiện thao tác nào.

   .. versionadded:: 3.13

.. c:function:: int PyUnstable_PerfTrampoline_CompileCode(PyCodeObject *code)

   Biên dịch code object đã cho bằng perf trampoline hiện tại.

   Trampoline “hiện tại” là trampoline được runtime thiết lập hoặc trampoline gần nhất
   Gọi :c:func:`PyUnstable_PerfTrampoline_SetPersistAfterFork`.

   Nếu không thiết lập trampoline, hệ thống sẽ chuyển sang biên dịch thông thường (không có mục perf map).

   :param code: Đối tượng code cần biên dịch.
   :return: 0 nếu thành công, -1 nếu thất bại.

   .. versionadded:: 3.13

.. c:function:: int PyUnstable_PerfTrampoline_SetPersistAfterFork(int enable)

   Thiết lập liệu perf trampoline có tiếp tục tồn tại sau fork hay không.

   * Nếu ``enable`` là true (khác 0): tệp perf map vẫn mở/hợp lệ sau fork. Tiến trình con kế thừa tất cả các mục perf map hiện có.
   * Nếu ``enable`` là false (bằng 0): perf map sẽ đóng sau fork. Tiến trình con nhận được perf map trống.

   Mặc định: false (bị xóa khi fork).

   :param enable: 1 để bật, 0 để tắt.
   :return: 0 nếu thành công, -1 nếu thất bại.

   .. versionadded:: 3.13

.. _`perf`: https://perf.wiki.kernel.org/index.php/Main_Page
.. _`documentation of the Linux Perf tool`: https://git.kernel.org/pub/scm/linux/ kernel/git/torvalds/linux.git/tree/tools/perf/Documentation/jit-interface.txt
