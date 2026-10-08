:mod:`!warnings` --- Kiểm soát cảnh báo
=======================================

.. module:: warnings
   :synopsis: Phát hành thông báo cảnh báo và kiểm soát cách xử lý chúng.

**Mã nguồn:** :source:`Lib/warnings.py`

.. index:: single: warnings

--------------

Thông báo cảnh báo thường được phát hành trong những tình huống mà việc cảnh báo người dùng về một điều kiện nào đó trong chương trình là hữu ích, trong đó điều kiện đó (thông thường) không đến mức cần raise một exception và kết thúc chương trình. Ví dụ, có thể muốn phát hành cảnh báo khi chương trình sử dụng một module đã lỗi thời.

Lập trình viên Python phát hành cảnh báo bằng cách gọi hàm :func:`warn` được định nghĩa trong module này. (Lập trình viên C sử dụng :c:func:`PyErr_WarnEx`; xem
:ref:`exceptionhandling` để biết chi tiết).

Thông báo cảnh báo thường được ghi vào :data:`sys.stderr`, nhưng cách xử lý chúng có thể được thay đổi linh hoạt, từ việc bỏ qua mọi cảnh báo cho đến biến chúng thành các exception. Cách xử lý cảnh báo có thể thay đổi tùy theo :ref:`danh mục cảnh báo <warning-categories>`, nội dung thông báo cảnh báo và vị trí mã nguồn nơi cảnh báo được phát hành. Các lần lặp lại của một cảnh báo cụ thể tại cùng một vị trí mã nguồn thường bị loại bỏ.

Việc kiểm soát cảnh báo gồm hai giai đoạn: trước tiên, mỗi khi một cảnh báo được phát hành, hệ thống sẽ xác định có nên phát hành thông báo hay không; tiếp theo, nếu cần phát hành thông báo, thông báo sẽ được định dạng và in ra bằng một hook do người dùng thiết lập.

Việc quyết định có phát hành thông báo cảnh báo hay không được kiểm soát bởi
:ref:`bộ lọc cảnh báo <warning-filter>`, là một chuỗi các quy tắc so khớp và hành động. Có thể thêm quy tắc vào bộ lọc bằng cách gọi :func:`filterwarnings` và đặt lại bộ lọc về trạng thái mặc định bằng cách gọi :func:`resetwarnings`.

Thông báo cảnh báo được in ra bằng cách gọi :func:`showwarning`, hàm này có thể được ghi đè; cách triển khai mặc định của hàm này định dạng thông báo bằng cách gọi :func:`formatwarning`, hàm này cũng có thể được các cách triển khai tùy chỉnh sử dụng.

.. seealso::
   :func:`logging.captureWarnings` allows you to handle all warnings with
   cơ sở hạ tầng logging tiêu chuẩn.


.. _warning-categories:

Các loại cảnh báo
-----------------

Có một số exception tích hợp sẵn đại diện cho các loại cảnh báo. Việc phân loại này hữu ích khi cần lọc ra các nhóm cảnh báo.

Mặc dù về mặt kỹ thuật là
:ref:`các ngoại lệ tích hợp sẵn <warning-categories-as-exceptions>`, chúng được trình bày ở đây vì về mặt khái niệm, chúng thuộc về cơ chế cảnh báo.

Mã do người dùng viết có thể định nghĩa thêm các danh mục cảnh báo bằng cách tạo lớp con từ một trong các danh mục cảnh báo tiêu chuẩn. Một danh mục cảnh báo luôn phải là lớp con của lớp :exc:`Warning`.

Hiện các lớp danh mục cảnh báo sau đã được định nghĩa:

.. tabularcolumns:: |l|p{0.6\linewidth}|

+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Lớp                              | Mô tả                                                                                                                                                                                                                  |
+==================================+========================================================================================================================================================================================================================+
| :exc:`Warning`                   | Lớp cơ sở cho các danh mục cảnh báo. Đây là lớp con của :exc:`Exception`.                                                                                                                                              |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`UserWarning`               | Lớp cơ sở cho các cảnh báo được tạo bởi mã do người dùng viết. Danh mục mặc định cho :func:`warn`.                                                                                                                     |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`DeprecationWarning`        | Lớp cơ sở cho các cảnh báo về những tính năng không còn được khuyến nghị sử dụng khi các cảnh báo đó dành cho những nhà phát triển Python khác (mặc định bị bỏ qua, trừ khi được kích hoạt bởi mã trong ``__main__``). |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`PendingDeprecationWarning` | Lớp cơ sở cho các cảnh báo về những tính năng sẽ không còn được khuyến nghị sử dụng trong tương lai (mặc định bị bỏ qua).                                                                                              |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`SyntaxWarning`             | Lớp cơ sở cho các cảnh báo về cú pháp đáng ngờ (thường được phát ra khi biên dịch mã nguồn Python, do đó có thể không bị loại bỏ bởi các bộ lọc runtime).                                                              |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`RuntimeWarning`            | Lớp cơ sở cho các cảnh báo về hành vi runtime đáng ngờ.                                                                                                                                                                |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`FutureWarning`             | Lớp cơ sở cho các cảnh báo về những tính năng không còn được khuyến nghị sử dụng khi các cảnh báo đó dành cho người dùng cuối của các ứng dụng được viết bằng Python.                                                  |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`ImportWarning`             | Lớp cơ sở cho các cảnh báo được kích hoạt trong quá trình import một module (mặc định bị bỏ qua).                                                                                                                      |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`UnicodeWarning`            | Lớp cơ sở cho các cảnh báo liên quan đến Unicode.                                                                                                                                                                      |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`EncodingWarning`           | Lớp cơ sở cho các cảnh báo liên quan đến encoding. Xem :ref:`io-encoding-warning` để biết chi tiết.                                                                                                                    |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`BytesWarning`              | Lớp cơ sở cho các cảnh báo liên quan đến                                                                                                                                                                               |
|                                  | :class:`bytes` và :class:`bytearray`.                                                                                                                                                                                  |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :exc:`ResourceWarning`           | Lớp cơ sở cho các cảnh báo liên quan đến việc sử dụng tài nguyên (mặc định bị bỏ qua).                                                                                                                                 |
+----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. versionchanged:: 3.7
   Trước đây, :exc:`DeprecationWarning` và :exc:`FutureWarning` được phân biệt dựa trên việc một tính năng bị loại bỏ hoàn toàn hay thay đổi hành vi. Hiện nay, chúng được phân biệt dựa trên đối tượng hướng đến và cách chúng được xử lý bởi các bộ lọc cảnh báo mặc định.


.. _warning-filter:

Bộ lọc cảnh báo
---------------

Bộ lọc cảnh báo kiểm soát việc các cảnh báo bị bỏ qua, hiển thị hay chuyển thành lỗi (phát sinh một ngoại lệ).

Về mặt khái niệm, bộ lọc cảnh báo duy trì một danh sách có thứ tự gồm các đặc tả bộ lọc; mỗi cảnh báo cụ thể lần lượt được đối chiếu với từng đặc tả bộ lọc trong danh sách cho đến khi tìm thấy kết quả khớp; bộ lọc xác định cách xử lý kết quả khớp đó. Mỗi mục nhập là một tuple có dạng (*action*, *message*, *category*, *module*, *lineno*), trong đó:

* *action* là một trong các chuỗi sau:

  +---------------+-------------------------------------------------------------------------------------------------------------+
  | Giá trị       | Cách xử lý                                                                                                  |
  +===============+=============================================================================================================+
  | ``"default"`` | in lần xuất hiện đầu tiên của các cảnh báo khớp cho mỗi vị trí (module + số dòng) nơi cảnh báo được phát ra |
  +---------------+-------------------------------------------------------------------------------------------------------------+
  | ``"error"``   | chuyển các cảnh báo khớp thành ngoại lệ                                                                     |
  +---------------+-------------------------------------------------------------------------------------------------------------+
  | ``"ignore"``  | không bao giờ in các cảnh báo khớp                                                                          |
  +---------------+-------------------------------------------------------------------------------------------------------------+
  | ``"always"``  | luôn in các cảnh báo khớp                                                                                   |
  +---------------+-------------------------------------------------------------------------------------------------------------+
  | ``"all"``     | bí danh của "always"                                                                                        |
  +---------------+-------------------------------------------------------------------------------------------------------------+
  | ``"module"``  | in lần xuất hiện đầu tiên của các cảnh báo khớp cho từng module nơi cảnh báo được phát ra (bất kể số dòng)  |
  +---------------+-------------------------------------------------------------------------------------------------------------+
  | ``"once"``    | chỉ in lần xuất hiện đầu tiên của các cảnh báo khớp, bất kể vị trí                                          |
  +---------------+-------------------------------------------------------------------------------------------------------------+

* *message* là một chuỗi chứa biểu thức chính quy mà phần bắt đầu của thông báo cảnh báo phải khớp, không phân biệt chữ hoa chữ thường. Trong :option:`-W` và
  :envvar:`PYTHONWARNINGS`, *message* là một chuỗi ký tự nguyên văn mà phần bắt đầu của thông báo cảnh báo phải chứa (không phân biệt chữ hoa chữ thường), đồng thời bỏ qua mọi khoảng trắng ở đầu hoặc cuối của *message*.

* *category* là một lớp (lớp con của :exc:`Warning`) mà loại cảnh báo phải là lớp con của nó để khớp.

* *module* là một chuỗi chứa biểu thức chính quy mà phần đầu của tên module đầy đủ phải khớp, có phân biệt chữ hoa chữ thường.  Trong :option:`-W` và
  :envvar:`PYTHONWARNINGS`, *module* là một chuỗi cố định mà tên module đầy đủ phải bằng với nó (có phân biệt chữ hoa chữ thường), bỏ qua mọi khoảng trắng ở đầu hoặc cuối *module*.

* *lineno* là một số nguyên mà số dòng nơi cảnh báo xảy ra phải khớp, hoặc ``0`` để khớp với mọi số dòng.

Vì lớp :exc:`Warning` được dẫn xuất từ lớp tích hợp sẵn :exc:`Exception`, để chuyển một cảnh báo thành lỗi, chúng ta chỉ cần raise ``category(message)``.

Nếu một cảnh báo được báo cáo và không khớp với bất kỳ bộ lọc nào đã đăng ký, hành động "default" sẽ được áp dụng (do đó có tên như vậy).



.. _repeated-warning-suppression-criteria:

Tiêu chí loại bỏ cảnh báo lặp lại
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Các bộ lọc dùng để ngăn chặn cảnh báo lặp lại áp dụng các tiêu chí sau để xác định một cảnh báo có được xem là lặp lại hay không:

- ``"default"``: Một cảnh báo chỉ được xem là lặp lại nếu (*message*, *category*, *module*, *lineno*) đều giống nhau.
- ``"module"``: Một cảnh báo được xem là lặp lại nếu (*message*, *category*, *module*) giống nhau, không xét số dòng.
- ``"once"``: Một cảnh báo được xem là lặp lại nếu (*message*, *category*) giống nhau, không xét module và số dòng.


.. _describing-warning-filters:

Mô tả các bộ lọc cảnh báo
~~~~~~~~~~~~~~~~~~~~~~~~~

Bộ lọc cảnh báo được khởi tạo bằng các tùy chọn :option:`-W` được truyền trên dòng lệnh của trình thông dịch Python và biến môi trường :envvar:`PYTHONWARNINGS`. Trình thông dịch lưu các đối số của tất cả các mục được cung cấp mà không diễn giải chúng trong :data:`sys.warnoptions`; module :mod:`!warnings` sẽ phân tích cú pháp các đối số này khi được import lần đầu (các tùy chọn không hợp lệ sẽ bị bỏ qua sau khi in thông báo tới :data:`sys.stderr`).

Các bộ lọc cảnh báo riêng lẻ được chỉ định dưới dạng một chuỗi các trường được phân tách bằng dấu hai chấm::

   action:message:category:module:line

Ý nghĩa của từng trường này được mô tả như trong :ref:`warning-filter`. Khi liệt kê nhiều filter trên một dòng (như trong
:envvar:`PYTHONWARNINGS`), các filter riêng lẻ được phân tách bằng dấu phẩy và những filter được liệt kê sau sẽ được ưu tiên hơn những filter đứng trước (vì chúng được áp dụng từ trái sang phải, và các filter được áp dụng gần nhất sẽ được ưu tiên hơn các filter trước đó).

Các filter cảnh báo thường dùng áp dụng cho tất cả cảnh báo, các cảnh báo thuộc một danh mục cụ thể hoặc các cảnh báo được phát sinh bởi những module hoặc package cụ thể. Một số ví dụ::

   default                      # Hiển thị tất cả cảnh báo (kể cả những cảnh báo bị bỏ qua theo mặc định)
   ignore                       # Bỏ qua tất cả cảnh báo
   error                        # Chuyển tất cả cảnh báo thành lỗi
   error::ResourceWarning       # Xử lý các thông báo ResourceWarning như lỗi
   default::DeprecationWarning  # Hiển thị các thông báo DeprecationWarning
   ignore,default:::mymodule    # Chỉ báo cáo các cảnh báo được kích hoạt bởi "mymodule"
   error:::mymodule             # Chuyển các cảnh báo thành lỗi trong "mymodule"


.. _default-warning-filter:

Bộ lọc cảnh báo mặc định
~~~~~~~~~~~~~~~~~~~~~~~~

Theo mặc định, Python cài đặt một số bộ lọc cảnh báo, có thể được ghi đè bằng tùy chọn dòng lệnh :option:`-W`, biến môi trường :envvar:`PYTHONWARNINGS` và các lệnh gọi đến :func:`filterwarnings`.

Trong các bản dựng phát hành thông thường, bộ lọc cảnh báo mặc định có các mục sau (theo thứ tự ưu tiên)::

    default::DeprecationWarning:__main__
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore::ImportWarning
    ignore::ResourceWarning

Trong một :ref:`bản dựng debug <debug-build>`, danh sách các bộ lọc cảnh báo mặc định là rỗng.

.. versionchanged:: 3.2
   :exc:`DeprecationWarning` is now ignored by default in addition to
   :exc:`PendingDeprecationWarning`.

.. versionchanged:: 3.7
  :exc:`DeprecationWarning` is once again shown by default when triggered
  trực tiếp bằng mã trong ``__main__``.

.. versionchanged:: 3.7
  :exc:`BytesWarning` no longer appears in the default filter list and is
  thay vào đó được cấu hình thông qua :data:`sys.warnoptions` khi :option:`-b` được chỉ định hai lần.


.. _warning-disable:

Ghi đè bộ lọc mặc định
~~~~~~~~~~~~~~~~~~~~~~

Các nhà phát triển ứng dụng được viết bằng Python có thể muốn ẩn *tất cả* các cảnh báo ở cấp Python khỏi người dùng theo mặc định và chỉ hiển thị chúng khi chạy các bài kiểm thử hoặc trong quá trình phát triển ứng dụng. Thuộc tính :data:`sys.warnoptions` được dùng để truyền cấu hình bộ lọc cho trình thông dịch có thể được dùng như một dấu hiệu cho biết có nên tắt cảnh báo hay không::

    import sys

    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

Các nhà phát triển test runner cho mã Python được khuyến nghị thay vào đó đảm bảo rằng *tất cả* cảnh báo được hiển thị theo mặc định đối với mã đang được kiểm thử, bằng cách sử dụng mã như sau::

    import sys

    if not sys.warnoptions:
        import os, warnings
        warnings.simplefilter("default") # Thay đổi bộ lọc trong tiến trình này
        os.environ["PYTHONWARNINGS"] = "default" # Cũng áp dụng cho các subprocess

Cuối cùng, các nhà phát triển interactive shell chạy mã người dùng trong một namespace khác với ``__main__`` được khuyến nghị đảm bảo rằng các thông báo :exc:`DeprecationWarning` được hiển thị theo mặc định, bằng cách sử dụng mã như sau (trong đó ``user_ns`` là module được dùng để thực thi mã được nhập một cách tương tác)::

    import warnings
    warnings.filterwarnings("default", category=DeprecationWarning,
                                       module=user_ns.get("__name__"))


.. _warning-suppress:

Tạm thời ẩn cảnh báo
--------------------

Nếu bạn đang sử dụng đoạn mã mà mình biết chắc sẽ tạo ra cảnh báo, chẳng hạn như một hàm đã deprecated, nhưng không muốn thấy cảnh báo đó (ngay cả khi các cảnh báo đã được cấu hình rõ ràng thông qua command line), bạn có thể ẩn cảnh báo bằng context manager :class:`catch_warnings`::

    import warnings

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()

Trong phạm vi của context manager, mọi cảnh báo sẽ פשוט bị bỏ qua. Điều này cho phép bạn sử dụng mã đã biết là deprecated mà không phải thấy cảnh báo, đồng thời không ẩn cảnh báo đối với những đoạn mã khác có thể không biết rằng mình đang sử dụng mã deprecated.

    .. note::

        Xem :ref:`warning-concurrent-safe` để biết chi tiết về tính an toàn đồng thời của context manager :class:`catch_warnings` khi được sử dụng trong các chương trình dùng nhiều thread hoặc async function.

.. _warning-testing:

Kiểm thử cảnh báo
-----------------

Để kiểm thử các cảnh báo do mã tạo ra, hãy sử dụng context manager :class:`catch_warnings`. Với context manager này, bạn có thể tạm thời thay đổi bộ lọc cảnh báo để hỗ trợ việc kiểm thử. Ví dụ, hãy thực hiện như sau để thu thập tất cả cảnh báo được tạo ra nhằm kiểm tra::

    import warnings

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings(record=True) as w:
        # Khiến mọi cảnh báo luôn được kích hoạt.
        warnings.simplefilter("always")
        # Kích hoạt một cảnh báo.
        fxn()
        # Xác minh một số điều
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)

Cũng có thể khiến mọi cảnh báo trở thành ngoại lệ bằng cách sử dụng ``error`` thay vì ``always``. Một điều cần lưu ý là nếu một cảnh báo đã được đưa ra do quy tắc ``once``/``default``, thì bất kể các bộ lọc được thiết lập như thế nào, cảnh báo sẽ không được thấy lại trừ khi registry cảnh báo liên quan đến cảnh báo đó đã được xóa.

Sau khi trình quản lý ngữ cảnh kết thúc, bộ lọc cảnh báo được khôi phục về trạng thái tại thời điểm ngữ cảnh được bắt đầu. Điều này ngăn các bài kiểm thử thay đổi bộ lọc cảnh báo theo những cách không mong muốn giữa các bài kiểm thử và dẫn đến kết quả kiểm thử không xác định.

    .. note::

        Xem :ref:`warning-concurrent-safe` để biết chi tiết về tính an toàn đối với việc chạy đồng thời của trình quản lý ngữ cảnh :class:`catch_warnings` khi được sử dụng trong các chương trình dùng nhiều thread hoặc các hàm async.

Khi kiểm thử nhiều thao tác tạo ra cùng một loại cảnh báo, điều quan trọng là phải kiểm thử chúng theo cách xác nhận mỗi thao tác tạo ra một cảnh báo mới (ví dụ: đặt cảnh báo được tạo ra dưới dạng ngoại lệ và kiểm tra rằng các thao tác tạo ra ngoại lệ, kiểm tra để đảm bảo độ dài của danh sách cảnh báo tiếp tục tăng sau mỗi thao tác, hoặc xóa các mục trước đó khỏi danh sách cảnh báo trước mỗi thao tác mới).


.. _warning-ignored:

Cập nhật mã cho các phiên bản mới của dependencies
--------------------------------------------------

Theo mặc định, các danh mục cảnh báo chủ yếu dành cho các nhà phát triển Python (thay vì người dùng cuối của các ứng dụng viết bằng Python) sẽ bị bỏ qua.

Đáng chú ý, danh sách "bị bỏ qua theo mặc định" này bao gồm :exc:`DeprecationWarning` (đối với mọi module ngoại trừ ``__main__``), điều đó có nghĩa là các nhà phát triển nên đảm bảo kiểm thử mã của mình với những cảnh báo thường bị bỏ qua được hiển thị, để nhận được thông báo kịp thời về các thay đổi API có thể gây lỗi trong tương lai (dù là trong thư viện chuẩn hay các package bên thứ ba).

Trong trường hợp lý tưởng, mã sẽ có một test suite phù hợp và test runner sẽ tự động bật tất cả cảnh báo khi chạy các bài kiểm thử (test runner do module :mod:`unittest` cung cấp thực hiện điều này).

Trong những trường hợp kém lý tưởng hơn, có thể kiểm tra ứng dụng để phát hiện việc sử dụng các interface đã bị deprecated bằng cách truyền :option:`-Wd <-W>` cho trình thông dịch Python (đây là dạng viết tắt của :option:`!-W default`) hoặc thiết lập ``PYTHONWARNINGS=default`` trong môi trường. Cách này bật cơ chế xử lý mặc định cho tất cả cảnh báo, bao gồm cả những cảnh báo bị bỏ qua theo mặc định. Để thay đổi hành động được thực hiện đối với các cảnh báo gặp phải, bạn có thể thay đổi đối số được truyền cho :option:`-W` (ví dụ:
:option:`!-W error`). Xem cờ :option:`-W` để biết thêm chi tiết về các tùy chọn có thể sử dụng.


.. _warning-functions:

Các hàm khả dụng
----------------


.. function:: warn(message, category=None, stacklevel=1, source=None, *, skip_file_prefixes=())

   Phát ra một cảnh báo, hoặc có thể bỏ qua cảnh báo đó hay raise một exception. Đối số *category*, nếu được cung cấp, phải là một :ref:`warning category class <warning-categories>`; mặc định là :exc:`UserWarning`. Ngoài ra, *message* có thể là một :exc:`Warning` instance, trong trường hợp đó *category* sẽ bị bỏ qua và ``message.__class__`` sẽ được sử dụng. Trong trường hợp này, văn bản thông báo sẽ là ``str(message)``. Hàm này raise một exception nếu cảnh báo cụ thể được phát ra bị chuyển thành lỗi bởi
   :ref:`warnings filter <warning-filter>`. Đối số *stacklevel* có thể được các hàm wrapper viết bằng Python sử dụng, như sau::

      def deprecated_api(message):
          warnings.warn(message, DeprecationWarning, stacklevel=2)

   Điều này khiến cảnh báo đề cập đến trình gọi của ``deprecated_api``, thay vì đến nguồn của chính ``deprecated_api`` (vì cách sau sẽ làm mất mục đích của thông báo cảnh báo).

   Đối số từ khóa *skip_file_prefixes* có thể được dùng để chỉ ra những stack frame nào được bỏ qua khi đếm các cấp độ stack. Điều này hữu ích khi bạn muốn cảnh báo luôn xuất hiện tại các vị trí gọi bên ngoài một package, trong trường hợp một *stacklevel* cố định không phù hợp với mọi đường dẫn gọi hoặc khó duy trì theo cách khác. Nếu được cung cấp, đối số này phải là một tuple các chuỗi. Khi cung cấp các tiền tố, stacklevel mặc nhiên bị ghi đè thành ``max(2, stacklevel)``. Để cảnh báo được quy cho trình gọi từ bên ngoài package hiện tại, bạn có thể viết::

      # example/lower.py
      _warn_skips = (os.path.dirname(__file__),)

      def one_way(r_luxury_yacht=None, t_wobbler_mangrove=None):
          if r_luxury_yacht:
              warnings.warn("Please migrate to t_wobbler_mangrove=.",
                            skip_file_prefixes=_warn_skips)

      # example/higher.py
      from . import lower

      def another_way(**kw):
          lower.one_way(**kw)

   Điều này khiến cảnh báo chỉ đề cập đến cả các vị trí gọi ``example.lower.one_way()`` và ``example.higher.another_way()`` từ mã gọi nằm bên ngoài package ``example``.

   *source*, nếu được cung cấp, là đối tượng đã bị hủy và phát ra một
   :exc:`ResourceWarning`.

   .. versionchanged:: 3.6
      Đã thêm tham số *source*.

   .. versionchanged:: 3.12
      Đã thêm *skip_file_prefixes*.


.. function:: warn_explicit(message, category, filename, lineno, module=None, registry=None, module_globals=None, source=None)

   Đây là giao diện cấp thấp cho chức năng của :func:`warn`, truyền rõ ràng message, category, filename và số dòng, cùng với các đối số khác tùy chọn. *message* phải là một chuỗi và *category* phải là một lớp con của :exc:`Warning` hoặc *message* có thể là một thực thể :exc:`Warning`, trong trường hợp đó *category* sẽ bị bỏ qua.

   *module*, nếu được cung cấp, phải là tên module. Nếu không truyền module, filename sau khi loại bỏ ``.py`` sẽ được sử dụng.

   *registry*, nếu được cung cấp, phải là dictionary ``__warningregistry__`` của module. Nếu không truyền registry, mỗi warning được xử lý như lần xuất hiện đầu tiên; nghĩa là các hành động lọc ``"default"``, ``"module"`` và ``"once"`` được xử lý như ``"always"``.

   *module_globals*, nếu được cung cấp, phải là global namespace đang được code sử dụng và là nơi phát ra warning. (Đối số này được dùng để hỗ trợ hiển thị source cho các module được tìm thấy trong zipfile hoặc các nguồn import không thuộc filesystem khác).

   *source*, nếu được cung cấp, là đối tượng đã bị hủy và phát ra một
   :exc:`ResourceWarning`.

   .. versionchanged:: 3.6
      Thêm tham số *source*.


.. function:: showwarning(message, category, filename, lineno, file=None, line=None)

   Ghi cảnh báo vào một tệp. Triển khai mặc định gọi ``formatwarning(message, category, filename, lineno, line)`` và ghi chuỗi kết quả vào *file*, với giá trị mặc định là :data:`sys.stderr`. Bạn có thể thay thế hàm này bằng bất kỳ đối tượng callable nào bằng cách gán cho ``warnings.showwarning``. *line* là một dòng mã nguồn được đưa vào thông báo cảnh báo; nếu không cung cấp *line*, :func:`showwarning` sẽ cố đọc dòng được chỉ định bởi *filename* và *lineno*.


.. function:: formatwarning(message, category, filename, lineno, line=None)

   Định dạng cảnh báo theo cách chuẩn. Hàm này trả về một chuỗi có thể chứa các ký tự xuống dòng nhúng và kết thúc bằng một ký tự xuống dòng. *line* là một dòng mã nguồn được đưa vào thông báo cảnh báo; nếu không cung cấp *line*,
   :func:`formatwarning` sẽ cố đọc dòng được chỉ định bởi *filename* và *lineno*.


.. function:: filterwarnings(action, message='', category=Warning, module='', lineno=0, append=False)

   Chèn một mục vào danh sách :ref:`warnings filter specifications <warning-filter>`. Theo mặc định, mục này được chèn vào đầu danh sách; nếu *append* là true, mục này được chèn vào cuối danh sách. Hàm này kiểm tra kiểu của các đối số, biên dịch các biểu thức chính quy *message* và *module*, rồi chèn chúng dưới dạng một tuple vào danh sách bộ lọc cảnh báo. Các mục ở gần đầu danh sách hơn sẽ ghi đè các mục ở phía sau nếu cả hai cùng khớp với một cảnh báo cụ thể. Các đối số bị bỏ qua sẽ mặc định nhận một giá trị khớp với mọi thứ.


.. function:: simplefilter(action, category=Warning, lineno=0, append=False)

   Chèn một mục đơn giản vào danh sách :ref:`warnings filter specifications <warning-filter>`. Ý nghĩa của các tham số hàm giống như
   :func:`filterwarnings`, nhưng không cần biểu thức chính quy vì bộ lọc được chèn luôn khớp với mọi thông báo trong mọi mô-đun, miễn là danh mục và số dòng khớp nhau.


.. function:: resetwarnings()

   Đặt lại bộ lọc cảnh báo. Thao tác này loại bỏ tác động của mọi lần gọi trước đó đến
   :func:`filterwarnings`, bao gồm cả tác động của các tùy chọn dòng lệnh :option:`-W` và các lần gọi đến :func:`simplefilter`.


.. decorator:: deprecated(message, /, *, category=DeprecationWarning, stacklevel=1)

   Decorator cho biết một lớp, hàm hoặc overload đã lỗi thời.

   Khi decorator này được áp dụng cho một đối tượng, cảnh báo về việc lỗi thời có thể được phát ra tại runtime khi đối tượng đó được sử dụng.
   :term:`trình kiểm tra kiểu tĩnh <static type checker>` cũng sẽ tạo chẩn đoán khi đối tượng đã lỗi thời được sử dụng.

   Cách sử dụng::

      from warnings import deprecated
      from typing import overload

      @deprecated("Use B instead")
      class A:
          pass

      @deprecated("Use g instead")
      def f():
          pass

      @overload
      @deprecated("int support is deprecated")
      def g(x: int) -> int: ...
      @overload
      def g(x: str) -> int: ...

   Cảnh báo được chỉ định bởi *category* sẽ được phát ra trong runtime khi sử dụng các đối tượng đã deprecated. Đối với hàm, điều đó xảy ra khi gọi hàm; đối với lớp, xảy ra khi khởi tạo và khi tạo các lớp con. Nếu *category* là ``None``, sẽ không có cảnh báo nào được phát ra trong runtime. *stacklevel* xác định vị trí phát ra cảnh báo. Nếu giá trị là ``1`` (mặc định), cảnh báo được phát ra tại caller trực tiếp của đối tượng đã deprecated; nếu giá trị cao hơn, cảnh báo được phát ra ở vị trí cao hơn trong stack. Hành vi của static type checker không bị ảnh hưởng bởi các đối số *category* và *stacklevel*.

   Thông báo deprecation được truyền cho decorator sẽ được lưu trong thuộc tính ``__deprecated__`` trên đối tượng được decorator áp dụng. Nếu được áp dụng cho một overload, decorator phải được đặt sau decorator :deco:`~typing.overload` để thuộc tính này tồn tại trên overload do
   :func:`typing.get_overloads`.

   .. versionadded:: 3.13
      Xem :pep:`702`.


Các Context Manager khả dụng
----------------------------

.. class:: catch_warnings(*, record=False, module=None, action=None, category=Warning, lineno=0, append=False)

    Một context manager sao chép và khi thoát sẽ khôi phục bộ lọc warnings và hàm :func:`showwarning`. Nếu đối số *record* là :const:`False` (mặc định), context manager sẽ trả về :class:`None` khi bắt đầu. Nếu *record* là :const:`True`, một danh sách được trả về và liên tục được bổ sung các đối tượng như được nhìn thấy bởi một
    hàm :func:`showwarning` (đồng thời ngăn đầu ra tới ``sys.stderr``). Mỗi đối tượng trong danh sách được đảm bảo có các thuộc tính sau:

      - ``message``: thông báo cảnh báo (một thể hiện của :exc:`Warning`)
      - ``category``: danh mục cảnh báo (một lớp con của :exc:`Warning`)
      - ``filename``: tên tệp nơi cảnh báo xảy ra (:class:`str`)
      - ``lineno``: số dòng trong tệp (:class:`int`)
      - ``file``: đối tượng tệp được dùng để xuất (nếu có), hoặc ``None``
      - ``line``: dòng mã nguồn (nếu có), hoặc ``None``
      - ``source``: đối tượng ban đầu tạo ra cảnh báo (nếu có), hoặc ``None``

    .. versionchanged:: 3.6
      Thuộc tính ``source`` đã được thêm.

    Kiểu của các đối tượng này không được chỉ định và có thể thay đổi; chỉ sự hiện diện của các thuộc tính này được đảm bảo.

    Đối số *module* nhận một module sẽ được sử dụng thay cho module được trả về khi bạn import :mod:`!warnings`, là module có filter được bảo vệ. Đối số này chủ yếu tồn tại để kiểm thử chính module :mod:`!warnings`.

    Nếu đối số *action* không phải là ``None``, các đối số còn lại được truyền cho :func:`simplefilter` như thể nó được gọi ngay khi vào context.

    Xem :ref:`warning-filter` để biết ý nghĩa của các tham số *category* và *lineno*.

    .. note::

        Xem :ref:`warning-concurrent-safe` để biết chi tiết về tính an toàn khi chạy đồng thời của context manager :class:`catch_warnings` khi được sử dụng trong các chương trình dùng nhiều thread hoặc async function.


    .. versionchanged:: 3.11

        Đã thêm các tham số *action*, *category*, *lineno* và *append*.


.. _warning-concurrent-safe:

Tính an toàn khi chạy đồng thời của Context Managers
----------------------------------------------------

Hành vi của trình quản lý ngữ cảnh :class:`catch_warnings` phụ thuộc vào
:data:`sys.flags.context_aware_warnings` flag. Nếu flag này là true, trình quản lý ngữ cảnh sẽ hoạt động theo cách an toàn khi chạy đồng thời, còn nếu không thì sẽ không như vậy. An toàn khi chạy đồng thời nghĩa là vừa an toàn với thread vừa an toàn khi sử dụng trong
:ref:`asyncio coroutines <coroutine>` và task. An toàn với thread nghĩa là hành vi có thể dự đoán được trong chương trình đa thread. flag này mặc định là true đối với các bản build free-threaded và false trong các trường hợp khác.

Nếu :data:`~sys.flags.context_aware_warnings` flag là false thì
:class:`catch_warnings` sẽ sửa đổi các thuộc tính toàn cục của
:mod:`!warnings` module. Điều này không an toàn khi được sử dụng trong chương trình chạy đồng thời (sử dụng nhiều thread hoặc sử dụng asyncio coroutine). Ví dụ: nếu hai hoặc nhiều thread sử dụng class :class:`catch_warnings` cùng lúc thì hành vi là không xác định.

Nếu flag là true, :class:`catch_warnings` sẽ không sửa đổi các thuộc tính toàn cục mà thay vào đó sẽ sử dụng một :class:`~contextvars.ContextVar` để lưu trữ trạng thái lọc cảnh báo mới được thiết lập. Biến ngữ cảnh cung cấp bộ nhớ lưu trữ cục bộ theo thread và giúp việc sử dụng :class:`catch_warnings` an toàn với thread.

Tham số *record* của context handler cũng hoạt động khác nhau tùy thuộc vào giá trị của flag. Khi *record* là true còn flag là false, context manager hoạt động bằng cách thay thế rồi sau đó khôi phục hàm :func:`showwarning` của module. Cách này không an toàn khi chạy đồng thời.

Khi *record* là true và flag là true, hàm :func:`showwarning` không bị thay thế. Thay vào đó, trạng thái ghi được biểu thị bằng một thuộc tính nội bộ trong biến context. Trong trường hợp này, hàm :func:`showwarning` sẽ không được khôi phục khi thoát khỏi context handler.

Có thể đặt flag :data:`~sys.flags.context_aware_warnings` bằng tùy chọn dòng lệnh :option:`-X context_aware_warnings<-X>` hoặc bằng
biến môi trường :envvar:`PYTHON_CONTEXT_AWARE_WARNINGS`.

    .. note::

        Nhiều khả năng hầu hết các chương trình muốn module warnings hoạt động an toàn với thread cũng sẽ muốn đặt flag
        :data:`~sys.flags.thread_inherit_context` thành true. Flag đó khiến các thread do :class:`threading.Thread` tạo ra bắt đầu với một bản sao các biến context từ thread tạo ra chúng. Khi là true, context được thiết lập bởi :class:`catch_warnings` trong một thread cũng sẽ áp dụng cho các thread mới do thread đó tạo ra. Nếu là false, các thread mới sẽ bắt đầu với một biến context warnings trống, nghĩa là mọi hoạt động lọc được thiết lập bởi một
        context manager :class:`catch_warnings` sẽ không còn hoạt động.

.. versionchanged:: 3.14

   Đã thêm cờ :data:`sys.flags.context_aware_warnings` và việc sử dụng một biến ngữ cảnh cho :class:`catch_warnings` nếu cờ này là true. Các phiên bản Python trước đây hoạt động như thể cờ này luôn được đặt thành false.
