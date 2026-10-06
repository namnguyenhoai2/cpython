.. currentmodule:: asyncio

.. _asyncio-subprocess:

==================
Các tiến trình con
==================

**Mã nguồn:** :source:`Lib/asyncio/subprocess.py`,
:source:`Lib/asyncio/base_subprocess.py`

----------------------------------------

Phần này mô tả các API asyncio cấp cao sử dụng async/await để tạo và quản lý các tiến trình con.

.. _asyncio_example_subprocess_shell:

Sau đây là ví dụ về cách asyncio có thể chạy một lệnh shell và nhận kết quả của lệnh đó::

    import asyncio

    async def run(cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    asyncio.run(run('ls /zzz'))

sẽ in ra::

    ['ls /zzz' exited with 1]
    [stderr]
    ls: /zzz: No such file or directory

Vì tất cả các hàm subprocess của asyncio đều là bất đồng bộ (asynchronous) và asyncio cung cấp nhiều công cụ để làm việc với các hàm như vậy, nên việc thực thi và giám sát nhiều tiến trình con song song rất dễ dàng. Thực tế, việc sửa đổi ví dụ trên để chạy đồng thời một số lệnh là điều hết sức đơn giản::

    async def main():
        await asyncio.gather(
            run('ls /zzz'),
            run('sleep 1; echo "hello"'))

    asyncio.run(main())

Xem thêm phần `Examples`_.


Tạo subprocess
==============

.. function:: create_subprocess_exec(program, *args, stdin=None, \
                 stdout=None, stderr=None, limit=65536, ****kwds)
   :async:

   Tạo một subprocess.

   Đối số *limit* đặt giới hạn bộ đệm cho các wrapper :class:`StreamReader` dành cho :attr:`~asyncio.subprocess.Process.stdout` và :attr:`~asyncio.subprocess.Process.stderr` (nếu :const:`subprocess.PIPE` được truyền vào các đối số *stdout* và *stderr*).

   Trả về một instance :class:`~asyncio.subprocess.Process`.

   Xem tài liệu của :meth:`loop.subprocess_exec` để biết các tham số khác.

   Nếu đối tượng tiến trình được thu gom rác trong khi tiến trình vẫn đang chạy, tiến trình con sẽ bị kết thúc.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.


.. function:: create_subprocess_shell(cmd, stdin=None, \
                 stdout=None, stderr=None, limit=65536, ****kwds)
   :async:

   Chạy lệnh shell *cmd*.

   Đối số *limit* đặt giới hạn bộ đệm cho các wrapper :class:`StreamReader` dành cho :attr:`~asyncio.subprocess.Process.stdout` và :attr:`~asyncio.subprocess.Process.stderr` (nếu :const:`subprocess.PIPE` được truyền vào các đối số *stdout* và *stderr*).

   Trả về một instance :class:`~asyncio.subprocess.Process`.

   Xem tài liệu của :meth:`loop.subprocess_shell` để biết các tham số khác.

   Nếu đối tượng tiến trình được thu gom rác trong khi tiến trình vẫn đang chạy, tiến trình con sẽ bị kết thúc.

   .. important::

      Ứng dụng có trách nhiệm đảm bảo rằng mọi khoảng trắng và ký tự đặc biệt đều được đặt trong dấu trích dẫn phù hợp để tránh các lỗ hổng `shell injection <https://en.wikipedia.org/wiki/Shell_injection#Shell_injection>`_. Có thể sử dụng hàm :func:`shlex.quote` để escape đúng khoảng trắng và các ký tự shell đặc biệt trong những chuỗi sẽ được dùng để tạo các lệnh shell.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

.. note::

   Có thể sử dụng subprocess trên Windows nếu dùng :class:`ProactorEventLoop`. Xem :ref:`Hỗ trợ subprocess trên Windows <asyncio-windows-subprocess>` để biết chi tiết.

.. seealso::

   asyncio cũng có các API *cấp thấp* sau để làm việc với subprocess:
   :meth:`loop.subprocess_exec`, :meth:`loop.subprocess_shell`,
   :meth:`loop.connect_read_pipe`, :meth:`loop.connect_write_pipe`, cũng như :ref:`Transport của subprocess <asyncio-subprocess-transports>` và :ref:`Protocol của subprocess <asyncio-subprocess-protocols>`.


Hằng số
=======

.. data:: asyncio.subprocess.PIPE
   :module:

   Có thể truyền vào các tham số *stdin*, *stdout* hoặc *stderr*.

   Nếu *PIPE* được truyền vào đối số *stdin*, thì
   thuộc tính :attr:`Process.stdin <asyncio.subprocess.Process.stdin>` sẽ trỏ đến một instance :class:`~asyncio.StreamWriter`.

   Nếu *PIPE* được truyền vào đối số *stdout* hoặc *stderr*, thì
   :attr:`Process.stdout <asyncio.subprocess.Process.stdout>` và
   các thuộc tính :attr:`Process.stderr <asyncio.subprocess.Process.stderr>` sẽ trỏ đến các instance :class:`~asyncio.StreamReader`.

.. data:: asyncio.subprocess.STDOUT
   :module:

   Giá trị đặc biệt có thể được dùng làm đối số *stderr* và cho biết rằng standard error sẽ được chuyển hướng vào standard output.

.. data:: asyncio.subprocess.DEVNULL
   :module:

   Giá trị đặc biệt có thể được dùng làm đối số *stdin*, *stdout* hoặc *stderr* cho các hàm tạo tiến trình. Giá trị này cho biết rằng tệp đặc biệt
   :data:`os.devnull` sẽ được sử dụng cho stream của subprocess tương ứng.


Tương tác với Subprocesses
==========================

Cả hai hàm :func:`create_subprocess_exec` và :func:`create_subprocess_shell` đều trả về các thực thể của lớp *Process*. *Process* là một wrapper cấp cao cho phép giao tiếp với các subprocess và theo dõi khi chúng hoàn tất.

.. class:: asyncio.subprocess.Process
   :module:

   Một đối tượng bao bọc các tiến trình OS được tạo bởi
   các hàm :func:`~asyncio.create_subprocess_exec` và :func:`~asyncio.create_subprocess_shell`.

   Lớp này được thiết kế để có API tương tự như lớp
   :class:`subprocess.Popen`, nhưng có một số điểm khác biệt đáng chú ý:

   * không giống Popen, các thực thể Process không có phương thức tương đương với :meth:`~subprocess.Popen.poll`;

   * :meth:`~asyncio.subprocess.Process.communicate` và
     :meth:`~asyncio.subprocess.Process.wait` Các phương thức không có tham số *timeout*: hãy sử dụng :func:`~asyncio.wait_for` hàm;

   * phương thức :meth:`Process.wait() <asyncio.subprocess.Process.wait>` là bất đồng bộ, trong khi phương thức :meth:`subprocess.Popen.wait` được triển khai dưới dạng vòng lặp bận chặn;

   * tham số *universal_newlines* không được hỗ trợ.

   Lớp này :ref:`không an toàn với thread <asyncio-multithreading>`.

   Xem thêm phần :ref:`Subprocess và Threads <asyncio-subprocess-threads>`.

   .. method:: wait()
      :async:

      Chờ tiến trình con kết thúc.

      Thiết lập và trả về thuộc tính :attr:`returncode`.

      .. note::

         Phương thức này có thể bị deadlock khi sử dụng ``stdout=PIPE`` hoặc ``stderr=PIPE`` và tiến trình con tạo ra quá nhiều đầu ra đến mức bị chặn do chờ bộ đệm pipe của hệ điều hành tiếp nhận thêm dữ liệu. Sử dụng phương thức :meth:`communicate` khi dùng pipe để tránh tình trạng này.

   .. method:: communicate(input=None)
      :async:

      Tương tác với tiến trình:

      1. gửi dữ liệu đến *stdin* (nếu *input* không phải là ``None``);
      2. đóng *stdin*;
      3. đọc dữ liệu từ *stdout* và *stderr*, cho đến khi gặp EOF;
      4. chờ tiến trình kết thúc.

      Đối số *input* tùy chọn là dữ liệu (:class:`bytes` object) sẽ được gửi đến tiến trình con.

      Trả về một tuple ``(stdout_data, stderr_data)``.

      Nếu ngoại lệ :exc:`BrokenPipeError` hoặc :exc:`ConnectionResetError` được phát sinh khi ghi *input* vào *stdin*, ngoại lệ đó sẽ bị bỏ qua. Điều kiện này xảy ra khi tiến trình kết thúc trước khi tất cả dữ liệu được ghi vào *stdin*.

      Nếu muốn gửi dữ liệu đến *stdin* của tiến trình, cần tạo tiến trình bằng ``stdin=PIPE``. Tương tự, để nhận được bất kỳ giá trị nào khác ``None`` trong tuple kết quả, phải tạo tiến trình bằng các đối số ``stdout=PIPE`` và/hoặc ``stderr=PIPE``.

      Lưu ý rằng dữ liệu được đọc sẽ được đệm trong bộ nhớ, vì vậy không sử dụng phương thức này nếu kích thước dữ liệu lớn hoặc không giới hạn.

      .. versionchanged:: 3.12

         *stdin* cũng được đóng khi ``input=None``.

   .. method:: send_signal(signal)

      Gửi tín hiệu *signal* đến tiến trình con.

      .. note::

         Trên Windows, :py:const:`~signal.SIGTERM` là bí danh của :meth:`terminate`. ``CTRL_C_EVENT`` và ``CTRL_BREAK_EVENT`` có thể được gửi đến các tiến trình được khởi chạy với tham số *creationflags* bao gồm ``CREATE_NEW_PROCESS_GROUP``.

   .. method:: terminate()

      Dừng tiến trình con.

      Trên các hệ thống POSIX, phương thức này gửi :py:const:`~signal.SIGTERM` đến tiến trình con.

      Trên Windows, hàm API Win32 :c:func:`!TerminateProcess` được gọi để dừng tiến trình con.

   .. method:: kill()

      Buộc dừng tiến trình con.

      Trên các hệ thống POSIX, phương thức này gửi :py:data:`~signal.SIGKILL` đến tiến trình con.

      Trên Windows, phương thức này là bí danh cho :meth:`terminate`.

   .. attribute:: stdin

      Luồng đầu vào tiêu chuẩn (:class:`~asyncio.StreamWriter`) hoặc ``None`` nếu tiến trình được tạo bằng ``stdin=None``.

   .. attribute:: stdout

      Luồng đầu ra tiêu chuẩn (:class:`~asyncio.StreamReader`) hoặc ``None`` nếu tiến trình được tạo bằng ``stdout=None``.

   .. attribute:: stderr

      Luồng lỗi tiêu chuẩn (:class:`~asyncio.StreamReader`) hoặc ``None`` nếu tiến trình được tạo bằng ``stderr=None``.

   .. warning::

      Sử dụng phương thức :meth:`communicate` thay vì
      :attr:`process.stdin.write() <stdin>`,
      :attr:`await process.stdout.read() <stdout>` hoặc
      :attr:`await process.stderr.read() <stderr>`. Điều này tránh deadlock do các luồng tạm dừng việc đọc hoặc ghi và chặn tiến trình con.

   .. attribute:: pid

      Số nhận dạng tiến trình (PID).

      Lưu ý rằng đối với các tiến trình được tạo bởi hàm :func:`~asyncio.create_subprocess_shell`, thuộc tính này là PID của shell được tạo ra.

   .. attribute:: returncode

      Mã trả về của tiến trình khi tiến trình kết thúc.

      Giá trị ``None`` cho biết tiến trình chưa kết thúc.

      Đối với các tiến trình được tạo bằng :func:`~asyncio.create_subprocess_exec`, giá trị âm ``-N`` cho biết tiến trình con đã bị kết thúc bởi signal ``N`` (chỉ dành cho POSIX).

      Đối với các tiến trình được tạo bằng :func:`~asyncio.create_subprocess_shell`, mã trả về phản ánh trạng thái thoát của chính shell (ví dụ: ``/bin/sh``), trạng thái này có thể ánh xạ các signal tới những mã như ``128+N``. Xem tài liệu của shell (chẳng hạn như Exit Status trong hướng dẫn sử dụng Bash) để biết thêm chi tiết.



.. _asyncio-subprocess-threads:

Tiến trình con và Luồng
-----------------------

Vòng lặp sự kiện asyncio tiêu chuẩn hỗ trợ chạy các tiến trình con từ những thread khác theo mặc định.

Trên Windows, các tiến trình con chỉ được cung cấp bởi :class:`ProactorEventLoop` (mặc định),
:class:`SelectorEventLoop` không hỗ trợ tiến trình con.

Lưu ý rằng các triển khai vòng lặp sự kiện thay thế có thể có những giới hạn riêng; vui lòng tham khảo tài liệu của chúng.

.. seealso::

   Mục :ref:`Tính đồng thời và đa luồng trong asyncio <asyncio-multithreading>`.


.. _`Examples`:

Ví dụ
-----

Một ví dụ sử dụng lớp :class:`~asyncio.subprocess.Process` để điều khiển một tiến trình con và lớp :class:`StreamReader` để đọc đầu ra tiêu chuẩn của tiến trình đó.

.. _asyncio_example_create_subprocess_exec:

Tiến trình con được tạo bởi hàm :func:`create_subprocess_exec`::

    import asyncio
    import sys

    async def get_date():
        code = 'import datetime as dt; print(dt.datetime.now())'

        # Tạo tiến trình con; chuyển hướng đầu ra tiêu chuẩn
        # vào một pipe.
        proc = await asyncio.create_subprocess_exec(
            sys.executable, '-c', code,
            stdout=asyncio.subprocess.PIPE)

        # Đọc một dòng đầu ra.
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()

        # Chờ tiến trình con thoát.
        await proc.wait()
        return line

    date = asyncio.run(get_date())
    print(f"Current date: {date}")


Xem thêm :ref:`cùng ví dụ <asyncio_example_subprocess_proto>` được viết bằng các API cấp thấp.

.. _`shell injection`: https://en.wikipedia.org/wiki/Shell_injection#Shell_injection
