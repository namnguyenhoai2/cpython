:mod:`!__main__` --- Môi trường mã cấp cao nhất
===============================================

.. module:: __main__
   :synopsis: The environment where top-level code is run. Covers command-line
              interfaces, import-time behavior, and ``__name__ == '__main__'``.

--------------

Trong Python, tên đặc biệt ``__main__`` được sử dụng cho hai cấu trúc quan trọng:

1. tên của môi trường cấp cao nhất của chương trình, có thể được kiểm tra bằng biểu thức ``__name__ == '__main__'``; và
2. tệp ``__main__.py`` trong các package Python.

Cả hai cơ chế này đều liên quan đến các module Python; cách người dùng tương tác với chúng và cách chúng tương tác với nhau. Chúng được giải thích chi tiết bên dưới. Nếu bạn mới làm quen với các module Python, hãy xem phần hướng dẫn
:ref:`tut-modules` để tìm hiểu phần giới thiệu.


.. _name_equals_main:

``__name__ == '__main__'``
---------------------------

Khi một module hoặc package Python được import, ``__name__`` được đặt thành tên của module. Thông thường, đây là tên của chính tệp Python đó nhưng không có phần mở rộng ``.py``::

    >>> import configparser
    >>> configparser.__name__
    'configparser'

Nếu tệp là một phần của package, ``__name__`` cũng sẽ bao gồm đường dẫn của package cha::

    >>> from concurrent.futures import process
    >>> process.__name__
    'concurrent.futures.process'

Tuy nhiên, nếu module được thực thi trong môi trường mã cấp cao nhất, ``__name__`` của nó được đặt thành chuỗi ``'__main__'``.

"Môi trường mã cấp cao nhất" là gì?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``__main__`` là tên của môi trường nơi mã cấp cao nhất được chạy. "Mã cấp cao nhất" là module Python đầu tiên do người dùng chỉ định và bắt đầu chạy. Nó được gọi là "cấp cao nhất" vì nó import tất cả các module khác mà chương trình cần. Đôi khi, "mã cấp cao nhất" còn được gọi là *điểm vào* của ứng dụng.

Môi trường mã cấp cao nhất có thể là:

* phạm vi của một lời nhắc tương tác::

   >>> __name__
   '__main__'

* module Python được truyền cho trình thông dịch Python dưới dạng đối số tệp:

  .. code-block:: shell-session

     $ python helloworld.py
     Hello, world!

* mô-đun hoặc gói Python được truyền cho trình thông dịch Python cùng với
  đối số :option:`-m`:

  .. code-block:: shell-session

     $ python -m tarfile
     usage: tarfile.py [-h] [-v] (...)

* mã Python được trình thông dịch Python đọc từ đầu vào tiêu chuẩn:

  .. code-block:: shell-session

     $ echo "import this" | python
     The Zen of Python, by Tim Peters

     Beautiful is better than ugly.
     Explicit is better than implicit.
     ...

* mã Python được truyền cho trình thông dịch Python bằng đối số :option:`-c`:

  .. code-block:: shell-session

     $ python -c "import this"
     The Zen of Python, by Tim Peters

     Beautiful is better than ugly.
     Explicit is better than implicit.
     ...

Trong mỗi tình huống này, ``__name__`` của mô-đun cấp cao nhất được đặt thành ``'__main__'``.

Do đó, một mô-đun có thể xác định liệu nó có đang chạy trong môi trường cấp cao nhất hay không bằng cách kiểm tra ``__name__`` của chính nó. Điều này cho phép sử dụng một thành ngữ phổ biến để thực thi có điều kiện mã khi mô-đun không được khởi tạo từ một câu lệnh import::

   if __name__ == '__main__':
       # Thực thi khi mô-đun không được khởi tạo từ một câu lệnh import.
       ...

.. seealso::

   Để tìm hiểu chi tiết hơn về cách ``__name__`` được thiết lập trong mọi tình huống, hãy xem phần hướng dẫn :ref:`tut-modules`.


Cách sử dụng theo thông lệ
^^^^^^^^^^^^^^^^^^^^^^^^^^

Một số module chứa mã chỉ предназнач cho việc sử dụng như script, chẳng hạn như phân tích các đối số dòng lệnh hoặc lấy dữ liệu từ đầu vào chuẩn. Nếu một module như vậy được import từ một module khác, chẳng hạn để kiểm thử đơn vị, mã script cũng sẽ vô tình được thực thi.

Đây là lúc việc sử dụng khối mã ``if __name__ == '__main__'`` trở nên hữu ích. Mã trong khối này sẽ không chạy trừ khi module được thực thi trong môi trường cấp cao nhất.

Đặt càng ít câu lệnh càng tốt trong khối bên dưới ``if __name__ == '__main__'`` có thể giúp mã rõ ràng và chính xác hơn. Thông thường nhất, một hàm có tên ``main`` sẽ đóng gói hành vi chính của chương trình::

    # echo.py

    import shlex
    import sys

    def echo(phrase: str) -> None:
       """A dummy wrapper around print."""
       # để minh họa, bạn có thể hình dung rằng có một
       # logic có giá trị và có thể tái sử dụng bên trong hàm này
       print(phrase)

    def main() -> int:
        """Echo the input arguments to standard output"""
        phrase = shlex.join(sys.argv)
        echo(phrase)
        return 0

    if __name__ == '__main__':
        sys.exit(main())  # phần tiếp theo giải thích cách sử dụng sys.exit

Lưu ý rằng nếu module không đóng gói mã bên trong hàm ``main`` mà đặt trực tiếp mã đó trong khối ``if __name__ == '__main__'``, biến ``phrase`` sẽ có phạm vi global trong toàn bộ module. Điều này dễ gây lỗi vì các hàm khác trong module có thể vô tình sử dụng biến global thay vì tên local. Hàm ``main`` giải quyết vấn đề này.

Việc sử dụng hàm ``main`` còn có thêm lợi ích là bản thân hàm ``echo`` được cô lập và có thể import ở nơi khác. Khi ``echo.py`` được import, các hàm ``echo`` và ``main`` sẽ được định nghĩa, nhưng không hàm nào trong số đó được gọi, vì ``__name__ != '__main__'``.


Các lưu ý về đóng gói
^^^^^^^^^^^^^^^^^^^^^

Các hàm ``main`` thường được dùng để tạo công cụ dòng lệnh bằng cách chỉ định chúng làm entry point cho console script. Khi thực hiện việc này, `pip <https://pip.pypa.io/>`_ chèn lời gọi hàm vào một template script, trong đó giá trị trả về của ``main`` được truyền vào :func:`sys.exit`. Ví dụ::

    sys.exit(main())

Vì lời gọi đến ``main`` được bọc trong :func:`sys.exit`, hàm của bạn được kỳ vọng sẽ trả về một giá trị có thể chấp nhận làm đầu vào cho
:func:`sys.exit`; thường là một số nguyên hoặc ``None`` (được trả về ngầm nếu hàm của bạn không có câu lệnh return).

Bằng cách chủ động tuân theo quy ước này, module của chúng ta sẽ có cùng hành vi khi được chạy trực tiếp (tức là ``python echo.py``) cũng như khi sau này được đóng gói thành một console script entry-point trong một package có thể cài đặt bằng pip.

Đặc biệt, hãy cẩn thận khi trả về các chuỗi từ hàm ``main`` của bạn.
:func:`sys.exit` sẽ diễn giải một đối số chuỗi là thông báo lỗi, vì vậy chương trình của bạn sẽ có mã thoát là ``1``, cho biết đã xảy ra lỗi, và chuỗi này sẽ được ghi vào :data:`sys.stderr`. Ví dụ ``echo.py`` ở phần trước minh họa việc sử dụng quy ước ``sys.exit(main())``.

.. seealso::

   `Python Packaging User Guide <https://packaging.python.org/>`_ chứa một tập hợp các hướng dẫn và tài liệu tham khảo về cách phân phối và cài đặt các package Python bằng những công cụ hiện đại.


``__main__.py`` trong các package Python
----------------------------------------

Nếu bạn chưa quen với các package Python, hãy xem mục :ref:`tut-packages` trong hướng dẫn. Thông thường nhất, file ``__main__.py`` được dùng để cung cấp giao diện dòng lệnh cho một package. Hãy xem package giả định sau đây, "bandclass":

.. code-block:: text

   bandclass
     ├── __init__.py
     ├── __main__.py
     └── student.py

``__main__.py`` sẽ được thực thi khi chính package được gọi trực tiếp từ dòng lệnh bằng cờ :option:`-m`. Ví dụ:

.. code-block:: shell-session

   $ python -m bandclass

Lệnh này sẽ khiến ``__main__.py`` chạy. Cách bạn sử dụng cơ chế này sẽ phụ thuộc vào bản chất của package bạn đang viết, nhưng trong trường hợp giả định này, có thể hợp lý nếu cho phép giáo viên tìm kiếm học sinh::

    # bandclass/__main__.py

    import sys
    from .student import search_students

    student_name = sys.argv[1] if len(sys.argv) >= 2 else ''
    print(f'Found student: {search_students(student_name)}')

Lưu ý rằng ``from .student import search_students`` là một ví dụ về relative import. Kiểu import này có thể được sử dụng khi tham chiếu đến các module bên trong một package. Để biết thêm chi tiết, hãy xem :ref:`intra-package-references` trong
phần :ref:`tut-modules` của hướng dẫn.

Cách sử dụng theo thông lệ
^^^^^^^^^^^^^^^^^^^^^^^^^^

Nội dung của ``__main__.py`` thường không được đặt trong một block ``if __name__ == '__main__'`` có fencing. Thay vào đó, các file này được giữ ngắn gọn và import các function cần thực thi từ những module khác. Nhờ đó, các module kia có thể dễ dàng được unit test và có khả năng tái sử dụng đúng cách.

Nếu được sử dụng, một khối ``if __name__ == '__main__'`` vẫn hoạt động như mong đợi đối với tệp ``__main__.py`` nằm trong một package, vì thuộc tính ``__name__`` của nó sẽ bao gồm đường dẫn của package nếu được import::

    >>> import asyncio.__main__
    >>> asyncio.__main__.__name__
    'asyncio.__main__'

Tuy nhiên, cách này sẽ không hoạt động đối với các tệp ``__main__.py`` trong thư mục gốc của tệp ``.zip``. Vì vậy, để nhất quán, nên sử dụng ``__main__.py`` tối thiểu mà không có kiểm tra ``__name__``.

.. seealso::

   Xem :mod:`venv` để biết ví dụ về một package có ``__main__.py`` tối thiểu trong standard library. Nó không chứa khối ``if __name__ == '__main__'``. Bạn có thể gọi nó bằng ``python -m venv [directory]``.

   Xem :mod:`runpy` để biết thêm chi tiết về cờ :option:`-m` của tệp thực thi interpreter.

   Xem :mod:`zipapp` để biết cách chạy các ứng dụng được đóng gói dưới dạng tệp *.zip*. Trong trường hợp này, Python sẽ tìm tệp ``__main__.py`` trong thư mục gốc của archive.



``import __main__``
-------------------

Bất kể chương trình Python được khởi động với module nào, các module khác đang chạy trong cùng chương trình đó đều có thể import scope của môi trường cấp cao nhất (:term:`namespace`) bằng cách import module ``__main__``. Việc này không import tệp ``__main__.py`` mà là module đã nhận tên đặc biệt ``'__main__'``.

Sau đây là một module ví dụ sử dụng namespace ``__main__``::

    # namely.py

    import __main__

    def did_user_define_their_name():
        return 'my_name' in dir(__main__)

    def print_user_name():
        if not did_user_define_their_name():
            raise ValueError('Define the variable `my_name`!')

        print(__main__.my_name)

Ví dụ sử dụng module này có thể như sau::

    # start.py

    import sys

    from namely import print_user_name

    # my_name = "Dinsdale"

    def main():
        try:
            print_user_name()
        except ValueError as ve:
            return str(ve)

    if __name__ == "__main__":
        sys.exit(main())

Bây giờ, nếu chúng ta chạy chương trình, kết quả sẽ như sau:

.. code-block:: shell-session

   $ python start.py
   Define the variable `my_name`!

Mã thoát của chương trình sẽ là 1, cho biết đã xảy ra lỗi. Bỏ chú thích dòng chứa ``my_name = "Dinsdale"`` sẽ khắc phục chương trình, và giờ đây chương trình sẽ thoát với mã trạng thái 0, cho biết đã thành công:

.. code-block:: shell-session

   $ python start.py
   Dinsdale

Lưu ý rằng việc import ``__main__`` không gây ra vấn đề nào do vô tình chạy code cấp cao nhất dành cho việc sử dụng dưới dạng script, vốn được đặt trong khối ``if __name__ == "__main__"`` của module ``start``. Tại sao cách này lại hoạt động?

Python chèn một module ``__main__`` trống vào :data:`sys.modules` khi interpreter khởi động, rồi điền nội dung cho module đó bằng cách chạy mã ở cấp cao nhất. Trong ví dụ của chúng ta, đây là module ``start``, module này chạy từng dòng một và import ``namely``. Đổi lại, ``namely`` import ``__main__`` (thực ra là ``start``). Đó là một chu kỳ import! May mắn là vì module ``__main__`` mới chỉ được điền một phần đã có mặt trong :data:`sys.modules`, Python truyền module đó cho ``namely``. Xem :ref:`Các lưu ý đặc biệt đối với __main__ <import-dunder-main>` trong tài liệu tham chiếu về hệ thống import để biết chi tiết về cách thức hoạt động này.

Python REPL là một ví dụ khác về "môi trường cấp cao nhất", vì vậy mọi thứ được định nghĩa trong REPL đều trở thành một phần của phạm vi ``__main__``::

    >>> import namely
    >>> namely.did_user_define_their_name()
    False
    >>> namely.print_user_name()
    Traceback (most recent call last):
    ...
    ValueError: Define the variable `my_name`!
    >>> my_name = 'Jabberwocky'
    >>> namely.did_user_define_their_name()
    True
    >>> namely.print_user_name()
    Jabberwocky

Phạm vi ``__main__`` được sử dụng trong quá trình triển khai :mod:`pdb` và
:mod:`rlcompleter`.

.. _`pip`: https://pip.pypa.io/
.. _`Python Packaging User Guide`: https://packaging.python.org/
