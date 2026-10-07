.. _devmode:

Chế độ Phát triển Python
========================

.. versionadded:: 3.7

Chế độ Phát triển Python bổ sung các bước kiểm tra runtime vốn quá tốn kém để bật theo mặc định. Chế độ này không nên dài dòng hơn chế độ mặc định nếu mã nguồn chính xác; các cảnh báo mới chỉ được phát ra khi phát hiện vấn đề.

Có thể bật chế độ này bằng tùy chọn dòng lệnh :option:`-X dev <-X>` hoặc bằng cách đặt biến môi trường :envvar:`PYTHONDEVMODE` thành ``1``.

Xem thêm :ref:`bản dựng debug Python <debug-build>`.

Ảnh hưởng của Chế độ Phát triển Python
--------------------------------------

Việc bật Chế độ Phát triển Python tương tự như lệnh sau, nhưng có thêm các ảnh hưởng được mô tả bên dưới::

    PYTHONMALLOC=debug PYTHONASYNCIODEBUG=1 python -W default -X faulthandler

Ảnh hưởng của Chế độ Phát triển Python:

* Thêm ``default`` :ref:`bộ lọc cảnh báo <describing-warning-filters>`. Các cảnh báo sau được hiển thị:

  * :exc:`DeprecationWarning`
  * :exc:`ImportWarning`
  * :exc:`PendingDeprecationWarning`
  * :exc:`ResourceWarning`

  Thông thường, các cảnh báo trên được lọc bởi :ref:`các bộ lọc cảnh báo <describing-warning-filters>` mặc định.

  Nó hoạt động như thể tùy chọn dòng lệnh :option:`-W default <-W>` được sử dụng.

  Sử dụng tùy chọn dòng lệnh :option:`-W error <-W>` hoặc đặt
  biến môi trường :envvar:`PYTHONWARNINGS` thành ``error`` để coi các cảnh báo là lỗi.

* Cài đặt các debug hook trên bộ cấp phát bộ nhớ để kiểm tra:

  * Tràn bộ đệm
  * Tràn bộ đệm
  * Vi phạm API của bộ cấp phát bộ nhớ
  * Sử dụng GIL không an toàn

  Xem hàm C :c:func:`PyMem_SetupDebugHooks`.

  Hoạt động như thể biến môi trường :envvar:`PYTHONMALLOC` được đặt thành ``debug``.

  Để bật Python Development Mode mà không cài đặt các hook gỡ lỗi trên bộ cấp phát bộ nhớ, hãy đặt biến môi trường :envvar:`PYTHONMALLOC` thành ``default``.

* Gọi :func:`faulthandler.enable` khi Python khởi động để cài đặt các trình xử lý cho :const:`~signal.SIGSEGV`, :const:`~signal.SIGFPE`,
  :const:`~signal.SIGABRT`, :const:`~signal.SIGBUS` và
  :const:`~signal.SIGILL` báo hiệu việc kết xuất traceback của Python khi xảy ra sự cố.

  Hoạt động này tương đương với việc sử dụng tùy chọn dòng lệnh :option:`-X faulthandler <-X>` hoặc đặt biến môi trường :envvar:`PYTHONFAULTHANDLER` thành ``1``.

* Bật :ref:`chế độ debug của asyncio <asyncio-debug-mode>`. Ví dụ:
  :mod:`asyncio` kiểm tra các coroutine chưa được await và ghi nhật ký về chúng.

  Hoạt động này tương đương với việc đặt biến môi trường :envvar:`PYTHONASYNCIODEBUG` thành ``1``.

* Kiểm tra các đối số *encoding* và *errors* cho các thao tác mã hóa và giải mã chuỗi. Ví dụ: :func:`open`, :meth:`str.encode` và
  :meth:`bytes.decode`.

  Theo mặc định, để đạt hiệu năng tốt nhất, đối số *errors* chỉ được kiểm tra ở lỗi mã hóa/giải mã đầu tiên và đối số *encoding* đôi khi bị bỏ qua đối với các chuỗi rỗng.

* :class:`io.IOBase` destructor ghi nhật ký các ``close()`` ngoại lệ.
* Đặt thuộc tính :attr:`~sys.flags.dev_mode` của :data:`sys.flags` thành ``True``.

Python Development Mode không bật mô-đun :mod:`tracemalloc` theo mặc định vì chi phí overhead (đối với hiệu năng và bộ nhớ) sẽ quá lớn. Việc bật mô-đun :mod:`tracemalloc` cung cấp thêm thông tin về nguồn gốc của một số lỗi. Ví dụ, :exc:`ResourceWarning` ghi nhật ký traceback tại đó tài nguyên được cấp phát, còn lỗi tràn bộ đệm ghi nhật ký traceback tại đó khối bộ nhớ được cấp phát.

Python Development Mode không ngăn tùy chọn dòng lệnh :option:`-O` loại bỏ các câu lệnh :keyword:`assert` hoặc đặt
:const:`__debug__` thành ``False``.

Python Development Mode chỉ có thể được bật khi Python khởi động. Có thể đọc giá trị của nó từ :data:`sys.flags.dev_mode <sys.flags>`.

.. versionchanged:: 3.8
   Bộ hủy :class:`io.IOBase` hiện ghi nhật ký các ngoại lệ ``close()``.

.. versionchanged:: 3.9
   Các đối số *encoding* và *errors* hiện được kiểm tra trong các thao tác mã hóa và giải mã chuỗi.


Ví dụ về ResourceWarning
------------------------

Ví dụ về một script đếm số dòng của tệp văn bản được chỉ định trên dòng lệnh::

    import sys

    def main():
        fp = open(sys.argv[1])
        nlines = len(fp.readlines())
        print(nlines)
        # Tệp được đóng ngầm định

    if __name__ == "__main__":
        main()

Script không đóng tệp một cách rõ ràng. Theo mặc định, Python không phát ra cảnh báo nào. Ví dụ sử dụng README.txt, tệp có 269 dòng:

.. code-block:: shell-session

    $ python script.py README.txt
    269

Việc bật Python Development Mode sẽ hiển thị cảnh báo :exc:`ResourceWarning`:

.. code-block:: shell-session

    $ python -X dev script.py README.txt
    269
    script.py:10: ResourceWarning: unclosed file <_io.TextIOWrapper name='README.rst' mode='r' encoding='UTF-8'>
      main()
    ResourceWarning: Enable tracemalloc to get the object allocation traceback

Ngoài ra, việc bật :mod:`tracemalloc` sẽ hiển thị dòng mà tệp được mở:

.. code-block:: shell-session

    $ python -X dev -X tracemalloc=5 script.py README.rst
    269
    script.py:10: ResourceWarning: unclosed file <_io.TextIOWrapper name='README.rst' mode='r' encoding='UTF-8'>
      main()
    Object allocated at (most recent call last):
      File "script.py", lineno 10
        main()
      File "script.py", lineno 4
        fp = open(sys.argv[1])

Cách khắc phục là đóng tệp một cách rõ ràng. Ví dụ sử dụng context manager::

    def main():
        # Đóng tệp một cách rõ ràng khi thoát khỏi khối with
        with open(sys.argv[1]) as fp:
            nlines = len(fp.readlines())
        print(nlines)

Việc không đóng tài nguyên một cách rõ ràng có thể khiến tài nguyên vẫn mở lâu hơn nhiều so với dự kiến; điều này có thể gây ra các sự cố nghiêm trọng khi thoát Python. Đây là vấn đề không tốt trong CPython, nhưng còn tệ hơn trong PyPy. Việc đóng tài nguyên một cách rõ ràng giúp ứng dụng có tính xác định và đáng tin cậy hơn.


Ví dụ về lỗi bad file descriptor
--------------------------------

Script hiển thị dòng đầu tiên của chính nó::

    import os

    def main():
        fp = open(__file__)
        firstline = fp.readline()
        print(firstline.rstrip())
        os.close(fp.fileno())
        # Tệp được đóng ngầm

    main()

Theo mặc định, Python không phát ra cảnh báo nào:

.. code-block:: shell-session

    $ python script.py
    import os

Python Development Mode hiển thị :exc:`ResourceWarning` và ghi nhật ký lỗi "Bad file descriptor" khi hoàn tất đối tượng file:

.. code-block:: shell-session

    $ python -X dev script.py
    import os
    script.py:10: ResourceWarning: unclosed file <_io.TextIOWrapper name='script.py' mode='r' encoding='UTF-8'>
      main()
    ResourceWarning: Enable tracemalloc to get the object allocation traceback
    Exception ignored in: <_io.TextIOWrapper name='script.py' mode='r' encoding='UTF-8'>
    Traceback (most recent call last):
      File "script.py", line 10, in <module>
        main()
    OSError: [Errno 9] Bad file descriptor

``os.close(fp.fileno())`` đóng file descriptor. Khi finalizer của đối tượng file cố gắng đóng file descriptor lần nữa, thao tác này thất bại với lỗi ``Bad file descriptor``. Một file descriptor chỉ được đóng một lần. Trong trường hợp xấu nhất, việc đóng nó hai lần có thể dẫn đến sự cố (xem :issue:`18748` để biết ví dụ).

Cách khắc phục là xóa dòng ``os.close(fp.fileno())`` hoặc mở file bằng ``closefd=False``.
