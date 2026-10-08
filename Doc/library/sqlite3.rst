:mod:`!sqlite3` --- Giao diện DB-API 2.0 cho cơ sở dữ liệu SQLite
=================================================================

.. module:: sqlite3
   :synopsis: Một triển khai DB-API 2.0 sử dụng SQLite 3.x.

.. sectionauthor:: Gerhard Häring <gh@ghaering.de>

**Mã nguồn:** :source:`Lib/sqlite3/`

.. Make sure we always doctest the tutorial with an empty database.

.. testsetup::

   import sqlite3
   src = sqlite3.connect(":memory:", isolation_level=None)
   dst = sqlite3.connect("tutorial.db", isolation_level=None)
   src.backup(dst)
   src.close()
   dst.close()
   del src, dst

.. _sqlite3-intro:

SQLite là một thư viện C cung cấp cơ sở dữ liệu nhẹ trên đĩa, không yêu cầu một tiến trình máy chủ riêng và cho phép truy cập cơ sở dữ liệu bằng một biến thể không chuẩn của ngôn ngữ truy vấn SQL. Một số ứng dụng có thể sử dụng SQLite để lưu trữ dữ liệu nội bộ. Bạn cũng có thể tạo nguyên mẫu ứng dụng bằng SQLite rồi chuyển mã sang một cơ sở dữ liệu lớn hơn như PostgreSQL hoặc Oracle.

Mô-đun :mod:`!sqlite3` do Gerhard Häring viết. Mô-đun này cung cấp giao diện SQL tuân thủ đặc tả DB-API 2.0 được mô tả bởi :pep:`249`, và yêu cầu thư viện `SQLite <https://sqlite.org/>`_ của bên thứ ba.

.. include:: ../includes/optional-module.rst

Tài liệu này gồm bốn phần chính:

* :ref:`sqlite3-tutorial` hướng dẫn cách sử dụng mô-đun :mod:`!sqlite3`.
* :ref:`sqlite3-reference` mô tả các lớp và hàm mà module này định nghĩa.
* :ref:`sqlite3-howtos` trình bày chi tiết cách xử lý các tác vụ cụ thể.
* :ref:`sqlite3-explanation` cung cấp thông tin nền tảng chuyên sâu về việc kiểm soát giao dịch.

.. seealso::

   https://www.sqlite.org
      Trang web SQLite; tài liệu mô tả cú pháp và các kiểu dữ liệu hiện có cho phương ngữ SQL được hỗ trợ.

   https://www.w3schools.com/sql/
      Hướng dẫn, tài liệu tham khảo và ví dụ để học cú pháp SQL.

   :pep:`249` - Đặc tả Database API 2.0
      PEP do Marc-André Lemburg viết.


.. We use the following practices for SQL code:
   - UPPERCASE for keywords
   - snake_case for schema
   - single quotes for string literals
   - singular for table names
   - if needed, use double quotes for table and column names

.. _sqlite3-tutorial:

Hướng dẫn
---------

Trong hướng dẫn này, bạn sẽ tạo một cơ sở dữ liệu về các bộ phim của Monty Python bằng chức năng :mod:`!sqlite3` cơ bản. Hướng dẫn này giả định bạn đã nắm được những khái niệm nền tảng về cơ sở dữ liệu, bao gồm `cursors`_ và `transactions`_.

Trước tiên, chúng ta cần tạo một cơ sở dữ liệu mới và mở một kết nối cơ sở dữ liệu để :mod:`!sqlite3` có thể làm việc với cơ sở dữ liệu đó. Gọi :func:`sqlite3.connect` để tạo kết nối đến cơ sở dữ liệu :file:`tutorial.db` trong thư mục làm việc hiện tại; cơ sở dữ liệu sẽ được tạo ngầm nếu chưa tồn tại:

.. testcode::

   import sqlite3
   con = sqlite3.connect("tutorial.db")

Đối tượng :class:`Connection` được trả về, ``con``, đại diện cho kết nối đến cơ sở dữ liệu trên đĩa.

Để thực thi các câu lệnh SQL và lấy kết quả từ các truy vấn SQL, chúng ta cần sử dụng một database cursor. Gọi :meth:`con.cursor() <Connection.cursor>` để tạo :class:`Cursor`:

.. testcode::

   cur = con.cursor()

Giờ đây, khi đã có kết nối cơ sở dữ liệu và cursor, chúng ta có thể tạo một bảng cơ sở dữ liệu ``movie`` với các cột cho tiêu đề, năm phát hành và điểm đánh giá. Để đơn giản, chúng ta chỉ cần sử dụng tên cột trong khai báo bảng — nhờ tính năng `kiểu dữ liệu linh hoạt <flexible typing_>`_ của SQLite, việc chỉ định kiểu dữ liệu là tùy chọn. Thực thi câu lệnh ``CREATE TABLE`` bằng cách gọi :meth:`cur.execute(...) <Cursor.execute>`:

.. testcode::

   cur.execute("CREATE TABLE movie(title, year, score)")

.. Ideally, we'd use sqlite_schema instead of sqlite_master below,
   but SQLite versions older than 3.33.0 do not recognise that variant.

Chúng ta có thể xác minh rằng bảng mới đã được tạo bằng cách truy vấn bảng ``sqlite_master`` tích hợp sẵn trong SQLite. Bảng này hiện sẽ chứa một mục cho định nghĩa bảng ``movie`` (xem `Bảng lược đồ <The Schema Table_>`_ để biết chi tiết). Thực thi truy vấn đó bằng cách gọi :meth:`cur.execute(...) <Cursor.execute>`, gán kết quả cho ``res``, rồi gọi :meth:`res.fetchone() <Cursor.fetchone>` để lấy hàng kết quả:

.. doctest::

   >>> res = cur.execute("SELECT name FROM sqlite_master")
   >>> res.fetchone()
   ('movie',)

Ta có thể thấy bảng đã được tạo, vì truy vấn trả về một :class:`tuple` chứa tên bảng. Nếu truy vấn ``sqlite_master`` cho một bảng không tồn tại ``spam``,
:meth:`!res.fetchone` sẽ trả về ``None``:

.. doctest::

   >>> res = cur.execute("SELECT name FROM sqlite_master WHERE name='spam'")
   >>> res.fetchone() is None
   True

Bây giờ, thêm hai hàng dữ liệu được cung cấp dưới dạng SQL literal bằng cách thực thi một câu lệnh ``INSERT``, một lần nữa bằng cách gọi :meth:`cur.execute(...) <Cursor.execute>`:

.. testcode::

   cur.execute("""
       INSERT INTO movie VALUES
           ('Monty Python and the Holy Grail', 1975, 8.2),
           ('And Now for Something Completely Different', 1971, 7.5)
   """)

Câu lệnh ``INSERT`` ngầm mở một transaction, transaction này cần được commit trước khi các thay đổi được lưu vào cơ sở dữ liệu (xem :ref:`sqlite3-controlling-transactions` để biết chi tiết). Gọi :meth:`con.commit() <Connection.commit>` trên đối tượng connection để commit transaction:

.. testcode::

   con.commit()

Ta có thể xác minh rằng dữ liệu đã được chèn chính xác bằng cách thực thi một truy vấn ``SELECT``. Sử dụng :meth:`cur.execute(...) <Cursor.execute>` vốn đã quen thuộc để gán kết quả cho ``res``, rồi gọi :meth:`res.fetchall() <Cursor.fetchall>` để trả về tất cả các hàng thu được:

.. doctest::

   >>> res = cur.execute("SELECT score FROM movie")
   >>> res.fetchall()
   [(8.2,), (7.5,)]

Kết quả là một :class:`list` gồm hai :class:`!tuple`\s, mỗi phần tương ứng với một hàng và chứa giá trị ``score`` của hàng đó.

Bây giờ, chèn thêm ba hàng bằng cách gọi
:meth:`cur.executemany(...) <Cursor.executemany>`:

.. testcode::

   data = [
       ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
       ("Monty Python's The Meaning of Life", 1983, 7.5),
       ("Monty Python's Life of Brian", 1979, 8.0),
   ]
   cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
   con.commit()  # Nhớ commit transaction sau khi thực thi INSERT.

Lưu ý rằng các placeholder ``?`` được dùng để liên kết ``data`` với query. Luôn sử dụng placeholder thay vì :ref:`string formatting <tut-formatting>` để liên kết các giá trị Python với câu lệnh SQL, nhằm tránh `SQL injection attacks <SQL injection attacks_>`_ (xem :ref:`sqlite3-placeholders` để biết thêm chi tiết).

Bạn có thể xác minh rằng các hàng mới đã được chèn bằng cách thực thi query ``SELECT``, lần này lặp qua các kết quả của query:

.. doctest::

   >>> for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
   ...     print(row)
   (1971, 'And Now for Something Completely Different')
   (1975, 'Monty Python and the Holy Grail')
   (1979, "Monty Python's Life of Brian")
   (1982, 'Monty Python Live at the Hollywood Bowl')
   (1983, "Monty Python's The Meaning of Life")

Mỗi hàng là một :class:`tuple` gồm hai phần tử thuộc ``(year, title)``, tương ứng với các cột được chọn trong query.

Cuối cùng, hãy xác minh rằng cơ sở dữ liệu đã được ghi vào đĩa bằng cách gọi :meth:`con.close() <Connection.close>` để đóng connection hiện có, mở một connection mới, tạo một cursor mới, rồi truy vấn cơ sở dữ liệu:

.. doctest::

   >>> con.close()
   >>> new_con = sqlite3.connect("tutorial.db")
   >>> new_cur = new_con.cursor()
   >>> res = new_cur.execute("SELECT title, year FROM movie ORDER BY score DESC")
   >>> title, year = res.fetchone()
   >>> print(f'The highest scoring Monty Python movie is {title!r}, released in {year}')
   The highest scoring Monty Python movie is 'Monty Python and the Holy Grail', released in 1975
   >>> new_con.close()

Bạn đã tạo một cơ sở dữ liệu SQLite bằng module :mod:`!sqlite3`, chèn dữ liệu và truy xuất các giá trị từ đó theo nhiều cách.

.. _SQL injection attacks: https://en.wikipedia.org/wiki/SQL_injection
.. _The Schema Table: https://www.sqlite.org/schematab.html
.. _cursors: https://en.wikipedia.org/wiki/Cursor_(databases)
.. _flexible typing: https://www.sqlite.org/flextypegood.html
.. _sqlite_master: https://www.sqlite.org/schematab.html
.. _transactions: https://en.wikipedia.org/wiki/Database_transaction

.. seealso::

   * :ref:`sqlite3-howtos` để đọc thêm:

     * :ref:`sqlite3-placeholders`
     * :ref:`sqlite3-adapters`
     * :ref:`sqlite3-converters`
     * :ref:`sqlite3-connection-context-manager`
     * :ref:`sqlite3-howto-row-factory`

   * :ref:`sqlite3-explanation` để biết thông tin nền tảng chuyên sâu về việc kiểm soát giao dịch.

.. _sqlite3-reference:

Tài liệu tham khảo
------------------

.. We keep the old sqlite3-module-contents ref to prevent breaking links.
.. _sqlite3-module-contents:

.. _sqlite3-module-functions:

Các hàm mô-đun
^^^^^^^^^^^^^^

.. function:: connect(database, timeout=5.0, detect_types=0, \
                      isolation_level="DEFERRED", check_same_thread=True, \ factory=sqlite3.Connection, cached_statements=128, \ uri=False, *, \ autocommit=sqlite3.LEGACY_TRANSACTION_CONTROL)

   Mở kết nối đến cơ sở dữ liệu SQLite.

   :param database:Đường dẫn đến tệp cơ sở dữ liệu cần mở. Bạn có thể truyền ``":memory:"`` để tạo một `cơ sở dữ liệu SQLite chỉ tồn tại trong bộ nhớ <https://sqlite.org/inmemorydb.html>`_ và mở kết nối đến cơ sở dữ liệu đó.
   :type database: :term:`path-like object`

   :param float timeout:Số giây mà kết nối sẽ chờ trước khi phát sinh :exc:`OperationalError` khi một bảng bị khóa. Nếu một kết nối khác mở giao dịch để sửa đổi một bảng, bảng đó sẽ bị khóa cho đến khi giao dịch được commit. Mặc định là năm giây.

   :param int detect_types:Kiểm soát việc có tra cứu và cách tra cứu các kiểu dữ liệu không
       :ref:`được SQLite hỗ trợ gốc <sqlite3-types>` để chuyển đổi thành các kiểu Python, bằng cách sử dụng các converter đã đăng ký với :func:`register_converter`. Đặt giá trị này thành bất kỳ tổ hợp nào (sử dụng ``|``, phép OR theo bit) của
       :const:`PARSE_DECLTYPES` và :const:`PARSE_COLNAMES` để bật tính năng này. Tên cột được ưu tiên hơn các kiểu đã khai báo nếu cả hai cờ đều được đặt. Theo mặc định (``0``), tính năng phát hiện kiểu bị vô hiệu hóa.

   :param isolation_level:Kiểm soát hành vi xử lý giao dịch legacy. Xem :attr:`Connection.isolation_level` và
       :ref:`sqlite3-transaction-control-isolation-level` để biết thêm thông tin. Có thể là ``"DEFERRED"`` (mặc định), ``"EXCLUSIVE"`` hoặc ``"IMMEDIATE"``; hoặc ``None`` để vô hiệu hóa việc ngầm mở các giao dịch. Không có tác dụng trừ khi :attr:`Connection.autocommit` được đặt thành
       :const:`~sqlite3.LEGACY_TRANSACTION_CONTROL` (mặc định).
   :type isolation_level: str | None

   :param bool check_same_thread:Nếu ``True`` (mặc định), :exc:`ProgrammingError` sẽ được phát sinh nếu kết nối cơ sở dữ liệu được sử dụng bởi một thread khác với thread đã tạo kết nối đó. Nếu ``False``, kết nối có thể được truy cập trong nhiều thread; người dùng có thể cần tuần tự hóa các thao tác ghi để tránh làm hỏng dữ liệu. Xem :attr:`threadsafety` để biết thêm thông tin.

   :param ~sqlite3.Connection factory:Một lớp con tùy chỉnh của :class:`Connection` dùng để tạo kết nối, nếu không sử dụng lớp :class:`Connection` mặc định.

   :param int cached_statements:Số lượng câu lệnh mà :mod:`!sqlite3` nên lưu vào bộ nhớ đệm nội bộ cho kết nối này để tránh chi phí phân tích cú pháp. Theo mặc định là 128 câu lệnh.

   :param bool uri:Nếu được đặt thành ``True``, *database* sẽ được diễn giải là một
       :abbr:`URI (Uniform Resource Identifier)` có đường dẫn tệp và chuỗi truy vấn tùy chọn. Phần scheme *must* là ``"file:"``, còn đường dẫn có thể là tương đối hoặc tuyệt đối. Chuỗi truy vấn cho phép truyền tham số vào SQLite, qua đó bật nhiều :ref:`sqlite3-uri-tricks` khác nhau.

   :param autocommit:Kiểm soát hành vi xử lý giao dịch của :pep:`249`. Xem :attr:`Connection.autocommit` và
       :ref:`sqlite3-transaction-control-autocommit` để biết thêm thông tin. *autocommit* hiện được mặc định là
       :const:`~sqlite3.LEGACY_TRANSACTION_CONTROL`. Giá trị mặc định sẽ thay đổi thành ``False`` trong một bản phát hành Python trong tương lai.
   :type autocommit: bool

   :rtype: ~sqlite3.Connection

   .. audit-event:: sqlite3.connect database sqlite3.connect
   .. audit-event:: sqlite3.connect/handle connection_handle sqlite3.connect

   .. versionchanged:: 3.4
      Đã thêm tham số *uri*.

   .. versionchanged:: 3.7
      *database* giờ đây cũng có thể là một :term:`path-like object`, không chỉ là một chuỗi.

   .. versionchanged:: 3.10
      Đã thêm sự kiện kiểm tra (auditing event) ``sqlite3.connect/handle``.

   .. versionchanged:: 3.12
      Đã thêm tham số *autocommit*.

   .. versionchanged:: 3.13
      Việc sử dụng theo vị trí các tham số *timeout*, *detect_types*, *isolation_level*, *check_same_thread*, *factory*, *cached_statements* và *uri* đã không còn được khuyến nghị. Chúng sẽ trở thành các tham số chỉ dùng theo từ khóa trong Python 3.15.

.. function:: complete_statement(statement)

   Trả về ``True`` nếu chuỗi *statement* dường như chứa một hoặc nhiều câu lệnh SQL hoàn chỉnh. Không thực hiện bất kỳ việc xác minh cú pháp hoặc phân tích cú pháp nào, ngoại trừ kiểm tra để bảo đảm không có literal chuỗi nào chưa được đóng và câu lệnh được kết thúc bằng dấu chấm phẩy.

   Ví dụ:

   .. doctest::

      >>> sqlite3.complete_statement("SELECT foo FROM bar;")
      True
      >>> sqlite3.complete_statement("SELECT foo")
      False

   Hàm này có thể hữu ích khi nhập liệu trên command line để xác định xem văn bản đã nhập có vẻ tạo thành một câu lệnh SQL hoàn chỉnh hay chưa, hoặc có cần thêm dữ liệu đầu vào trước khi gọi :meth:`~Cursor.execute` hay không.

   Xem :func:`!runsource` trong :source:`Lib/sqlite3/__main__.py` để biết cách sử dụng trong thực tế.

.. function:: enable_callback_tracebacks(flag, /)

   Bật hoặc tắt traceback của callback. Theo mặc định, bạn sẽ không nhận được traceback nào trong các hàm, aggregate, converter, callback authorizer do người dùng định nghĩa, v.v. Nếu muốn debug chúng, bạn có thể gọi hàm này với *flag* được đặt thành ``True``. Sau đó, bạn sẽ nhận được traceback từ các callback trên :data:`sys.stderr`. Sử dụng ``False`` để tắt lại tính năng này.

   .. note::

      Các lỗi trong callback của hàm do người dùng định nghĩa được ghi lại dưới dạng các exception không thể raise. Sử dụng một :func:`unraisable hook handler <sys.unraisablehook>` để kiểm tra callback bị lỗi.

.. function:: register_adapter(type, adapter, /)

   Đăng ký một *adapter* :term:`callable` để điều chỉnh kiểu Python *type* thành một kiểu SQLite. Adapter nhận một đối tượng Python thuộc kiểu *type* làm đối số duy nhất và phải trả về một giá trị thuộc
   :ref:`kiểu mà SQLite hiểu một cách nguyên bản <sqlite3-types>`.

.. function:: register_converter(typename, converter, /)

   Đăng ký *converter* :term:`callable` để chuyển đổi các đối tượng SQLite thuộc kiểu *typename* thành một đối tượng Python thuộc kiểu cụ thể. Converter được gọi cho mọi giá trị SQLite thuộc kiểu *typename*; nó nhận một đối tượng :class:`bytes` và phải trả về một đối tượng thuộc kiểu Python mong muốn. Tham khảo tham số *detect_types* của
   :func:`connect` để biết thông tin về cách hoạt động của việc phát hiện kiểu.

   Lưu ý: *typename* và tên của kiểu trong truy vấn sẽ được đối sánh không phân biệt chữ hoa chữ thường.


.. _sqlite3-module-constants:

Các hằng số của module
^^^^^^^^^^^^^^^^^^^^^^

.. data:: LEGACY_TRANSACTION_CONTROL

   Đặt :attr:`~Connection.autocommit` thành hằng số này để chọn hành vi kiểm soát giao dịch kiểu cũ (trước Python 3.12). Xem :ref:`sqlite3-transaction-control-isolation-level` để biết thêm thông tin.

.. data:: PARSE_DECLTYPES

   Truyền giá trị cờ này vào tham số *detect_types* của
   :func:`connect` để tra cứu một hàm chuyển đổi bằng cách sử dụng các kiểu được khai báo cho từng cột. Các kiểu được khai báo khi bảng cơ sở dữ liệu được tạo.
   :mod:`!sqlite3` sẽ tra cứu một hàm chuyển đổi bằng cách sử dụng từ đầu tiên của kiểu đã khai báo làm khóa của từ điển bộ chuyển đổi. Ví dụ:

   .. code-block:: sql

      CREATE TABLE test(
         i integer primary key,  ! will look up a converter named "integer"
         p point,                ! will look up a converter named "point"
         n number(10)            ! will look up a converter named "number"
       )

   Cờ này có thể được kết hợp với :const:`PARSE_COLNAMES` bằng toán tử ``|`` (OR theo bit).

   .. note::

      Các trường được tạo (ví dụ ``MAX(p)``) được trả về dưới dạng :class:`str`. Sử dụng :const:`!PARSE_COLNAMES` để thực thi các kiểu cho những truy vấn như vậy.

.. data:: PARSE_COLNAMES

   Truyền giá trị cờ này vào tham số *detect_types* của
   :func:`connect` để tra cứu một hàm chuyển đổi bằng cách sử dụng tên kiểu, được phân tích từ tên cột truy vấn, làm khóa của từ điển bộ chuyển đổi. Tên cột truy vấn phải được đặt trong dấu ngoặc kép (``"``) và tên kiểu phải được đặt trong dấu ngoặc vuông (``[]``).

   .. code-block:: sql

      SELECT MAX(p) as "p [point]" FROM test;  ! will look up converter "point"

   Cờ này có thể được kết hợp với :const:`PARSE_DECLTYPES` bằng toán tử ``|`` (bitwise or).

.. data:: SQLITE_OK
          SQLITE_DENY SQLITE_IGNORE

   Các cờ cần được trả về bởi *authorizer_callback* :term:`callable` được truyền vào :meth:`Connection.set_authorizer`, để cho biết liệu:

   * Quyền truy cập được cho phép (:const:`!SQLITE_OK`),
   * Câu lệnh SQL sẽ bị hủy bỏ kèm theo lỗi (:const:`!SQLITE_DENY`)
   * Cột sẽ được coi là giá trị ``NULL`` (:const:`!SQLITE_IGNORE`)

.. data:: apilevel

   Chuỗi hằng cho biết cấp độ DB-API được hỗ trợ. DB-API yêu cầu hằng này. Được hard-code thành ``"2.0"``.

.. data:: paramstyle

   Hằng số chuỗi nêu rõ kiểu định dạng dấu đánh dấu tham số mà module :mod:`!sqlite3` yêu cầu. Đây là yêu cầu của DB-API. Được hard-code thành ``"qmark"``.

   .. note::

      Kiểu tham số ``named`` của DB-API cũng được hỗ trợ.

.. data:: sqlite_version

   Số phiên bản của thư viện SQLite runtime dưới dạng một :class:`string <str>`.

.. data:: sqlite_version_info

   Số phiên bản của thư viện SQLite runtime dưới dạng một :class:`tuple` của
   :class:`integers <int>`.

.. data:: threadsafety

   Hằng số số nguyên do DB-API 2.0 yêu cầu, nêu rõ mức độ an toàn luồng mà module :mod:`!sqlite3` hỗ trợ. Thuộc tính này được thiết lập dựa trên `threading mode <https://sqlite.org/threadsafe.html>`_ mặc định mà thư viện SQLite bên dưới được biên dịch cùng. Các chế độ luồng của SQLite là:

   1. **Đơn luồng**: Ở chế độ này, tất cả mutex đều bị vô hiệu hóa và SQLite không an toàn khi được sử dụng đồng thời trong nhiều hơn một luồng.
   2. **Đa luồng**: Ở chế độ này, SQLite có thể được nhiều luồng sử dụng an toàn, với điều kiện không có một kết nối cơ sở dữ liệu nào được sử dụng đồng thời trong hai hoặc nhiều luồng.
   3. **Serialized**: Ở chế độ Serialized, SQLite có thể được nhiều thread sử dụng an toàn mà không bị hạn chế.

   Ánh xạ từ các chế độ threading của SQLite sang các cấp độ threadsafety của DB-API 2.0 như sau:

   +------------------+----------------------+----------------------+-------------------------------+
   | SQLite threading | :pep:`threadsafety   | `SQLITE_THREADSAFE`_ | DB-API 2.0 meaning            |
   | mode             | <0249#threadsafety>` |                      |                               |
   +==================+======================+======================+===============================+
   | single-thread    | 0                    | 0                    | Threads may not share the     |
   |                  |                      |                      | module                        |
   +------------------+----------------------+----------------------+-------------------------------+
   | multi-thread     | 1                    | 2                    | Threads may share the module, |
   |                  |                      |                      | but not connections           |
   +------------------+----------------------+----------------------+-------------------------------+
   | serialized       | 3                    | 1                    | Threads may share the module, |
   |                  |                      |                      | connections and cursors       |
   +------------------+----------------------+----------------------+-------------------------------+

   .. _SQLITE_THREADSAFE: https://sqlite.org/compile.html#threadsafe

   .. versionchanged:: 3.11
      Đặt *threadsafety* một cách động thay vì hard-code thành ``1``.

.. _sqlite3-dbconfig-constants:

.. data:: SQLITE_DBCONFIG_DEFENSIVE
          SQLITE_DBCONFIG_DQS_DDL SQLITE_DBCONFIG_DQS_DML SQLITE_DBCONFIG_ENABLE_FKEY SQLITE_DBCONFIG_ENABLE_FTS3_TOKENIZER SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION SQLITE_DBCONFIG_ENABLE_QPSG SQLITE_DBCONFIG_ENABLE_TRIGGER SQLITE_DBCONFIG_ENABLE_VIEW SQLITE_DBCONFIG_LEGACY_ALTER_TABLE SQLITE_DBCONFIG_LEGACY_FILE_FORMAT SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE SQLITE_DBCONFIG_RESET_DATABASE SQLITE_DBCONFIG_TRIGGER_EQP SQLITE_DBCONFIG_TRUSTED_SCHEMA SQLITE_DBCONFIG_WRITABLE_SCHEMA

   Các hằng số này được sử dụng cho các phương thức :meth:`Connection.setconfig` và :meth:`~Connection.getconfig`.

   Tính khả dụng của các hằng số này thay đổi tùy thuộc vào phiên bản SQLite mà Python được biên dịch cùng.

   .. versionadded:: 3.12

   .. seealso::

     https://www.sqlite.org/c3ref/c_dbconfig_defensive.html
        Tài liệu SQLite: Tùy chọn cấu hình kết nối cơ sở dữ liệu

.. deprecated-removed:: 3.12 3.14
   Các hằng số :data:`!version` và :data:`!version_info`.

.. _sqlite3-connection-objects:

Các đối tượng kết nối
^^^^^^^^^^^^^^^^^^^^^

.. class:: Connection

   Mỗi cơ sở dữ liệu SQLite đang mở được biểu diễn bằng một đối tượng ``Connection``, được tạo bằng :func:`sqlite3.connect`. Mục đích chính của chúng là tạo các đối tượng :class:`Cursor` và :ref:`sqlite3-controlling-transactions`.

   .. seealso::

      * :ref:`sqlite3-connection-shortcuts`
      * :ref:`sqlite3-connection-context-manager`


   .. versionchanged:: 3.13

      Một :exc:`ResourceWarning` được phát ra nếu :meth:`close` không được gọi trước khi một đối tượng :class:`!Connection` bị xóa.

   Một kết nối cơ sở dữ liệu SQLite có các thuộc tính và phương thức sau:

   .. method:: cursor(factory=Cursor)

      Tạo và trả về một đối tượng :class:`Cursor`. Phương thức cursor chấp nhận một tham số tùy chọn duy nhất là *factory*. Nếu được cung cấp, tham số này phải là một :term:`callable` trả về một thực thể của :class:`Cursor` hoặc các lớp con của nó.

   .. method:: blobopen(table, column, rowid, /, *, readonly=False, name="main")

      Mở một handle :class:`Blob` tới một đối tượng hiện có
      :abbr:`BLOB (Đối tượng nhị phân lớn)`.

      :param str table:Tên của bảng nơi blob nằm.

      :param str column:Tên của cột nơi blob nằm.

      :param int rowid:ID của hàng nơi blob nằm.

      :param bool readonly:Đặt thành ``True`` nếu blob cần được mở mà không có quyền ghi. Mặc định là ``False``.

      :param str name:Tên của cơ sở dữ liệu nơi blob nằm. Mặc định là ``"main"``.

      :raises OperationalError:Khi cố gắng mở một blob trong bảng ``WITHOUT ROWID``.

      :rtype: Blob

      .. note::

         Không thể thay đổi kích thước blob bằng lớp :class:`Blob`. Sử dụng hàm SQL ``zeroblob`` để tạo blob có kích thước cố định.

      .. versionadded:: 3.11

   .. method:: commit()

      Commit mọi giao dịch đang chờ vào cơ sở dữ liệu. Nếu :attr:`autocommit` là ``True``, hoặc không có giao dịch nào đang mở, phương thức này không thực hiện thao tác nào. Nếu :attr:`!autocommit` là ``False``, một giao dịch mới sẽ được ngầm mở nếu giao dịch đang chờ đã được commit bởi phương thức này.

   .. method:: rollback()

      Rollback về thời điểm bắt đầu của mọi giao dịch đang chờ. Nếu :attr:`autocommit` là ``True``, hoặc không có giao dịch nào đang mở, phương thức này không thực hiện thao tác nào. Nếu :attr:`!autocommit` là ``False``, một giao dịch mới sẽ được ngầm mở nếu giao dịch đang chờ đã được rollback bởi phương thức này.

   .. method:: close()

      Đóng kết nối cơ sở dữ liệu. Nếu :attr:`autocommit` là ``False``, mọi giao dịch đang chờ sẽ được ngầm rollback. Nếu :attr:`!autocommit` là ``True`` hoặc :data:`LEGACY_TRANSACTION_CONTROL`, sẽ không thực hiện việc kiểm soát giao dịch ngầm nào. Hãy đảm bảo :meth:`commit` trước khi đóng để tránh mất các thay đổi đang chờ.

   .. method:: execute(sql, parameters=(), /)

      Tạo một đối tượng :class:`Cursor` mới và gọi
      :meth:`~Cursor.execute` trên đối tượng đó với *sql* và *parameters* đã cho. Trả về đối tượng cursor mới.

   .. method:: executemany(sql, parameters, /)

      Tạo một đối tượng :class:`Cursor` mới và gọi
      :meth:`~Cursor.executemany` trên đó với *sql* và *parameters* đã cho. Trả về đối tượng cursor mới.

   .. method:: executescript(sql_script, /)

      Tạo một đối tượng :class:`Cursor` mới và gọi
      :meth:`~Cursor.executescript` trên đó với *sql_script* đã cho. Trả về đối tượng cursor mới.

   .. method:: create_function(name, narg, func, *, deterministic=False)

      Tạo hoặc xóa một hàm SQL do người dùng định nghĩa.

      :param str name:Tên của hàm SQL.

      :param int narg:Số lượng đối số mà hàm SQL có thể nhận. Nếu là ``-1``, hàm có thể nhận bất kỳ số lượng đối số nào.

      :param func:Một :term:`callable` được gọi khi hàm SQL được gọi. Callable phải trả về :ref:`một kiểu được SQLite hỗ trợ nguyên bản <sqlite3-types>`. Đặt thành ``None`` để xóa một hàm SQL hiện có.
      :type func: :term:`callback` | None

      :param bool deterministic:Nếu ``True``, hàm SQL được tạo sẽ được đánh dấu là `deterministic <https://sqlite.org/deterministic.html>`_, cho phép SQLite thực hiện thêm các tối ưu hóa.

      .. versionchanged:: 3.8
         Đã thêm tham số *deterministic*.

      Ví dụ:

      .. doctest::

         >>> import hashlib
         >>> def md5sum(t):
         ...     return hashlib.md5(t).hexdigest()
         >>> con = sqlite3.connect(":memory:")
         >>> con.create_function("md5", 1, md5sum)
         >>> for row in con.execute("SELECT md5(?)", (b"foo",)):
         ...     print(row)
         ('acbd18db4cc2f85cedef654fccc4a4d8',)
         >>> con.close()

      .. versionchanged:: 3.13

         Việc truyền *name*, *narg* và *func* dưới dạng đối số từ khóa không được khuyến nghị. Các tham số này sẽ chỉ có thể được truyền theo vị trí trong Python 3.15.


   .. method:: create_aggregate(name, n_arg, aggregate_class)

      Tạo hoặc xóa một hàm aggregate SQL do người dùng định nghĩa.

      :param str name:Tên của hàm aggregate SQL.

      :param int n_arg:Số lượng đối số mà hàm aggregate SQL có thể nhận. Nếu ``-1``, hàm có thể nhận bất kỳ số lượng đối số nào.

      :param aggregate_class:Một class phải triển khai các phương thức sau:

          * ``step()``: Thêm một hàng vào aggregate.
          * ``finalize()``: Trả về kết quả cuối cùng của aggregate dưới dạng
            :ref:`một kiểu được SQLite hỗ trợ nguyên bản <sqlite3-types>`.

          Số lượng đối số mà phương thức ``step()`` phải chấp nhận được kiểm soát bởi *n_arg*.

          Đặt thành ``None`` để xóa một hàm aggregate SQL hiện có.
      :type aggregate_class: :term:`class` | None

      Ví dụ:

      .. testcode::

         class MySum:
             def __init__(self):
                 self.count = 0

             def step(self, value):
                 self.count += value

             def finalize(self):
                 return self.count

         con = sqlite3.connect(":memory:")
         con.create_aggregate("mysum", 1, MySum)
         cur = con.execute("CREATE TABLE test(i)")
         cur.execute("INSERT INTO test(i) VALUES(1)")
         cur.execute("INSERT INTO test(i) VALUES(2)")
         cur.execute("SELECT mysum(i) FROM test")
         print(cur.fetchone()[0])

         con.close()

      .. testoutput::
         :hide:

         3

      .. versionchanged:: 3.13

         Việc truyền *name*, *n_arg* và *aggregate_class* dưới dạng đối số từ khóa đã không còn được khuyến nghị. Các tham số này sẽ chỉ được phép truyền theo vị trí trong Python 3.15.


   .. method:: create_window_function(name, num_params, aggregate_class, /)

      Tạo hoặc xóa một hàm cửa sổ aggregate do người dùng định nghĩa.

      :param str name:Tên của hàm cửa sổ aggregate SQL cần tạo hoặc xóa.

      :param int num_params:Số lượng đối số mà hàm cửa sổ aggregate SQL có thể nhận. Nếu là ``-1``, hàm có thể nhận số lượng đối số bất kỳ.

      :param aggregate_class:Một lớp phải triển khai các phương thức sau:

          * ``step()``: Thêm một hàng vào cửa sổ hiện tại.
          * ``value()``: Trả về giá trị hiện tại của aggregate.
          * ``inverse()``: Xóa một hàng khỏi cửa sổ hiện tại.
          * ``finalize()``: Trả về kết quả cuối cùng của aggregate dưới dạng
            :ref:`một kiểu được SQLite hỗ trợ nguyên bản <sqlite3-types>`.

          Số lượng đối số mà các phương thức ``step()`` và ``value()`` phải chấp nhận được kiểm soát bởi *num_params*.

          Đặt thành ``None`` để xóa một hàm cửa sổ tổng hợp SQL hiện có.

      :raises NotSupportedError:Nếu được sử dụng với phiên bản SQLite cũ hơn 3.25.0, phiên bản không hỗ trợ các hàm cửa sổ tổng hợp.

      :type aggregate_class: :term:`class` | None

      .. versionadded:: 3.11

      Ví dụ:

      .. testcode::

         # Ví dụ lấy từ https://www.sqlite.org/windowfunctions.html#udfwinfunc
         class WindowSumInt:
             def __init__(self):
                 self.count = 0

             def step(self, value):
                 """Add a row to the current window."""
                 self.count += value

             def value(self):
                 """Return the current value of the aggregate."""
                 return self.count

             def inverse(self, value):
                 """Remove a row from the current window."""
                 self.count -= value

             def finalize(self):
                 """Return the final value of the aggregate.

                 Any clean-up actions should be placed here.
                 """
                 return self.count


         con = sqlite3.connect(":memory:")
         cur = con.execute("CREATE TABLE test(x, y)")
         values = [
             ("a", 4),
             ("b", 5),
             ("c", 3),
             ("d", 8),
             ("e", 1),
         ]
         cur.executemany("INSERT INTO test VALUES(?, ?)", values)
         con.create_window_function("sumint", 1, WindowSumInt)
         cur.execute("""
             SELECT x, sumint(y) OVER (
                 ORDER BY x ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
             ) AS sum_y
             FROM test ORDER BY x
         """)
         print(cur.fetchall())
         con.close()

      .. testoutput::
         :hide:

         [('a', 9), ('b', 12), ('c', 16), ('d', 12), ('e', 9)]

   .. method:: create_collation(name, callable, /)

      Tạo một collation có tên *name* bằng hàm đối chiếu *callable*. *callable* nhận hai đối số :class:`string <str>`, và hàm này nên trả về một :class:`integer <int>`:

      * ``1`` nếu phần tử thứ nhất được sắp xếp cao hơn phần tử thứ hai
      * ``-1`` nếu phần tử thứ nhất được sắp xếp trước phần tử thứ hai
      * ``0`` nếu thứ tự của chúng bằng nhau

      Ví dụ sau đây minh họa một collation dùng để sắp xếp theo thứ tự ngược:

      .. testcode::

         def collate_reverse(string1, string2):
             if string1 == string2:
                 return 0
             elif string1 < string2:
                 return 1
             else:
                 return -1

         con = sqlite3.connect(":memory:")
         con.create_collation("reverse", collate_reverse)

         cur = con.execute("CREATE TABLE test(x)")
         cur.executemany("INSERT INTO test(x) VALUES(?)", [("a",), ("b",)])
         cur.execute("SELECT x FROM test ORDER BY x COLLATE reverse")
         for row in cur:
             print(row)
         con.close()

      .. testoutput::
         :hide:

         ('b',)
         ('a',)

      Xóa một hàm collation bằng cách đặt *callable* thành ``None``.

      .. versionchanged:: 3.11
         Tên collation có thể chứa bất kỳ ký tự Unicode nào. Trước đây, chỉ cho phép các ký tự ASCII.


   .. method:: interrupt()

      Gọi phương thức này từ một thread khác để hủy mọi truy vấn có thể đang thực thi trên connection. Các truy vấn bị hủy sẽ phát sinh một :exc:`OperationalError`.


   .. method:: set_authorizer(authorizer_callback)

      Đăng ký :term:`callable` *authorizer_callback* để được gọi cho mỗi lần thử truy cập một cột của một bảng trong cơ sở dữ liệu. Callback phải trả về một trong các giá trị sau: :const:`SQLITE_OK`,
      :const:`SQLITE_DENY`, hoặc :const:`SQLITE_IGNORE` để báo hiệu cách thư viện SQLite bên dưới cần xử lý quyền truy cập vào cột.

      Đối số đầu tiên của callback cho biết loại thao tác cần được cấp quyền. Đối số thứ hai và thứ ba sẽ là các đối số hoặc ``None`` tùy thuộc vào đối số đầu tiên. Đối số thứ 4 là tên cơ sở dữ liệu ("main", "temp", v.v.) nếu có. Đối số thứ 5 là tên của trigger hoặc view ở trong cùng chịu trách nhiệm cho lần thử truy cập, hoặc ``None`` nếu lần thử truy cập này đến trực tiếp từ mã SQL đầu vào.

      Vui lòng tham khảo tài liệu SQLite để biết các giá trị có thể có của đối số đầu tiên cũng như ý nghĩa của đối số thứ hai và thứ ba tùy thuộc vào đối số đầu tiên. Tất cả các hằng số cần thiết đều có trong mô-đun :mod:`!sqlite3`.

      Truyền ``None`` làm *authorizer_callback* sẽ vô hiệu hóa authorizer.

      .. versionchanged:: 3.11
         Đã bổ sung hỗ trợ vô hiệu hóa authorizer bằng ``None``.

      .. versionchanged:: 3.13
         Việc truyền *authorizer_callback* dưới dạng đối số từ khóa đã không còn được khuyến nghị. Tham số này sẽ chỉ được phép truyền theo vị trí trong Python 3.15.


   .. method:: set_progress_handler(progress_handler, n)

      Đăng ký :term:`callable` *progress_handler* để được gọi sau mỗi *n* lệnh của máy ảo SQLite. Điều này hữu ích nếu bạn muốn được gọi từ SQLite trong các thao tác chạy lâu, chẳng hạn như để cập nhật GUI.

      Nếu muốn xóa mọi progress handler đã được cài đặt trước đó, hãy gọi phương thức với ``None`` cho *progress_handler*.

      Việc trả về một giá trị khác không từ hàm handler sẽ chấm dứt truy vấn hiện đang thực thi và khiến truy vấn đó phát sinh ngoại lệ :exc:`DatabaseError`.

      .. versionchanged:: 3.13
         Việc truyền *progress_handler* dưới dạng đối số từ khóa không còn được khuyến nghị. Tham số này sẽ chỉ nhận đối số theo vị trí trong Python 3.15.


   .. method:: set_trace_callback(trace_callback)

      Đăng ký :term:`callable` *trace_callback* để callback được gọi cho mỗi câu lệnh SQL thực sự được backend SQLite thực thi.

      Đối số duy nhất được truyền cho callback là câu lệnh (dưới dạng
      :class:`str`) đang được thực thi. Giá trị trả về của callback bị bỏ qua. Lưu ý rằng backend không chỉ chạy các câu lệnh được truyền cho
      :meth:`Cursor.execute` các phương thức. Các nguồn khác bao gồm
      :ref:`quản lý giao dịch <sqlite3-controlling-transactions>` của
      :mod:`!sqlite3` module và việc thực thi các trigger được định nghĩa trong cơ sở dữ liệu hiện tại.

      Truyền ``None`` làm *trace_callback* sẽ vô hiệu hóa trace callback.

      .. note::
         Các exception được phát sinh trong trace callback không được truyền đi. Để hỗ trợ phát triển và gỡ lỗi, hãy sử dụng
         :meth:`~sqlite3.enable_callback_tracebacks` để bật việc in traceback từ các exception được phát sinh trong trace callback.

      .. versionadded:: 3.3

      .. versionchanged:: 3.13
         Việc truyền *trace_callback* dưới dạng keyword argument đã không còn được khuyến nghị. Tham số này sẽ chỉ có thể được truyền theo vị trí trong Python 3.15.


   .. method:: enable_load_extension(enabled, /)

      Cho phép SQLite engine tải các SQLite extension từ shared library nếu *enabled* là ``True``; nếu không, không cho phép tải SQLite extension. SQLite extension có thể định nghĩa các function, aggregate mới hoặc toàn bộ implementation của virtual table mới. Một extension nổi tiếng là extension tìm kiếm toàn văn được phân phối cùng SQLite.

      .. note::

         Mô-đun :mod:`!sqlite3` theo mặc định không được xây dựng với hỗ trợ extension có thể nạp, vì một số nền tảng (đáng chú ý là macOS) có các thư viện SQLite được biên dịch mà không có tính năng này. Để có hỗ trợ extension có thể nạp, bạn phải truyền tùy chọn :option:`--enable-loadable-sqlite-extensions` cho :program:`configure`.

      .. audit-event:: sqlite3.enable_load_extension connection,enabled sqlite3.Connection.enable_load_extension

      .. versionadded:: 3.2

      .. versionchanged:: 3.10
         Đã thêm sự kiện auditing ``sqlite3.enable_load_extension``.

      .. We cannot doctest the load extension API, since there is no convenient
         way to skip it.

      .. code-block::

         con.enable_load_extension(True)

         # Nạp extension tìm kiếm toàn văn
         con.execute("select load_extension('./fts3.so')")

         # hoặc bạn có thể nạp extension bằng một lệnh gọi API:
         # con.load_extension("./fts3.so")

         # tắt lại việc nạp extension
         con.enable_load_extension(False)

         # ví dụ từ wiki SQLite
         con.execute("CREATE VIRTUAL TABLE recipe USING fts3(name, ingredients)")
         con.executescript("""
             INSERT INTO recipe (name, ingredients) VALUES('broccoli stew', 'broccoli peppers cheese tomatoes');
             INSERT INTO recipe (name, ingredients) VALUES('pumpkin stew', 'pumpkin onions garlic celery');
             INSERT INTO recipe (name, ingredients) VALUES('broccoli pie', 'broccoli cheese onions flour');
             INSERT INTO recipe (name, ingredients) VALUES('pumpkin pie', 'pumpkin sugar flour butter');
             """)
         for row in con.execute("SELECT rowid, name, ingredients FROM recipe WHERE name MATCH 'pie'"):
             print(row)

   .. method:: load_extension(path, /, *, entrypoint=None)

      Tải một extension của SQLite từ thư viện dùng chung. Bật tính năng tải extension bằng :meth:`enable_load_extension` trước khi gọi phương thức này.

      :param str path:

         Đường dẫn đến extension của SQLite.

      :param entrypoint:

         Tên entry point. Nếu ``None`` (giá trị mặc định), SQLite sẽ tự chọn tên entry point; xem tài liệu SQLite `Loading an Extension <Loading an Extension_>`_ để biết chi tiết.

      :type entrypoint: str | None

      .. audit-event:: sqlite3.load_extension connection,path sqlite3.Connection.load_extension

      .. versionadded:: 3.2

      .. versionchanged:: 3.10
         Đã thêm sự kiện auditing ``sqlite3.load_extension``.

      .. versionchanged:: 3.12
         Đã thêm tham số *entrypoint*.

   .. _Loading an Extension: https://www.sqlite.org/loadext.html#loading_an_extension

   .. method:: iterdump(*, filter=None)

      Trả về một :term:`iterator` để kết xuất cơ sở dữ liệu dưới dạng mã nguồn SQL. Hữu ích khi lưu cơ sở dữ liệu trong bộ nhớ để khôi phục sau này. Tương tự lệnh ``.dump`` trong shell :program:`sqlite3`.

      :param filter:

        Một mẫu ``LIKE`` tùy chọn cho các đối tượng cơ sở dữ liệu cần dump, ví dụ: ``prefix_%``. Nếu là ``None`` (mặc định), tất cả các đối tượng cơ sở dữ liệu sẽ được đưa vào.

      :type filter: str | None

      Ví dụ:

      .. testcode::

         # Chuyển đổi tệp example.db thành tệp dump SQL dump.sql
         con = sqlite3.connect('example.db')
         with open('dump.sql', 'w') as f:
             for line in con.iterdump():
                 f.write('%s\n' % line)
         con.close()

      .. seealso::

         :ref:`sqlite3-howto-encoding`

      .. versionchanged:: 3.13
         Đã thêm tham số *filter*.

   .. method:: backup(target, *, pages=-1, progress=None, name="main", sleep=0.250)

      Tạo bản sao lưu của cơ sở dữ liệu SQLite.

      Vẫn hoạt động ngay cả khi cơ sở dữ liệu đang được các client khác truy cập hoặc được cùng một connection truy cập đồng thời.

      :param ~sqlite3.Connection target:Kết nối cơ sở dữ liệu để lưu bản sao lưu vào.

      :param int pages:Số trang cần sao chép mỗi lần. Nếu nhỏ hơn hoặc bằng ``0``, toàn bộ cơ sở dữ liệu sẽ được sao chép trong một bước duy nhất. Mặc định là ``-1``.

      :param progress:Nếu được đặt thành một :term:`callable`, nó sẽ được gọi với ba đối số số nguyên cho mỗi lần lặp sao lưu: *trạng thái* của lần lặp trước, *số trang còn lại* vẫn cần sao chép và *tổng số trang*. Mặc định là ``None``.
      :type progress: :term:`callback` | None

      :param str name:Tên cơ sở dữ liệu cần sao lưu. Có thể là ``"main"`` (mặc định) cho cơ sở dữ liệu chính, ``"temp"`` cho cơ sở dữ liệu tạm thời hoặc tên của cơ sở dữ liệu tùy chỉnh được đính kèm bằng câu lệnh SQL ``ATTACH DATABASE``.

      :param float sleep:Số giây tạm dừng giữa các lần thử liên tiếp để sao lưu các trang còn lại.

      Ví dụ 1: sao chép một cơ sở dữ liệu hiện có vào một cơ sở dữ liệu khác:

      .. testcode::

         def progress(status, remaining, total):
             print(f'Copied {total-remaining} of {total} pages...')

         src = sqlite3.connect('example.db')
         dst = sqlite3.connect('backup.db')
         with dst:
             src.backup(dst, pages=1, progress=progress)
         dst.close()
         src.close()

      .. testoutput::
         :hide:

         Copied 0 of 0 pages...

      Ví dụ 2, sao chép một cơ sở dữ liệu hiện có vào một bản sao tạm thời:

      .. testcode::

         src = sqlite3.connect('example.db')
         dst = sqlite3.connect(':memory:')
         src.backup(dst)
         dst.close()
         src.close()

      .. versionadded:: 3.7

      .. seealso::

         :ref:`sqlite3-howto-encoding`

   .. method:: getlimit(category, /)

      Lấy giới hạn runtime của kết nối.

      :param int category:`Danh mục giới hạn SQLite <SQLite limit category_>`_ cần truy vấn.

      :rtype: int

      :raises ProgrammingError:Nếu *category* không được thư viện SQLite bên dưới nhận diện.

      Ví dụ, truy vấn độ dài tối đa của một câu lệnh SQL cho :class:`Connection` ``con`` (mặc định là 1000000000):

      .. testsetup:: sqlite3.limits

         import sqlite3
         con = sqlite3.connect(":memory:")
         con.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 1_000_000_000)
         con.setlimit(sqlite3.SQLITE_LIMIT_ATTACHED, 10)

      .. doctest:: sqlite3.limits

         >>> con.getlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH)
         1000000000

      .. versionadded:: 3.11


   .. method:: setlimit(category, limit, /)

      Đặt giới hạn runtime của kết nối. Các nỗ lực tăng giới hạn vượt quá cận trên cố định sẽ bị âm thầm cắt giảm về cận trên cố định. Bất kể giới hạn có được thay đổi hay không, giá trị trước đó của giới hạn sẽ được trả về.

      :param int category:Danh mục `giới hạn SQLite <SQLite limit category_>`_ cần đặt.

      :param int limit:Giá trị của giới hạn mới. Nếu là số âm, giới hạn hiện tại sẽ không thay đổi.

      :rtype: int

      :raises ProgrammingError:Nếu *category* không được thư viện SQLite bên dưới nhận diện.

      Ví dụ, giới hạn số cơ sở dữ liệu được đính kèm ở mức 1 cho :class:`Connection` ``con`` (giới hạn mặc định là 10):

      .. doctest:: sqlite3.limits

         >>> con.setlimit(sqlite3.SQLITE_LIMIT_ATTACHED, 1)
         10
         >>> con.getlimit(sqlite3.SQLITE_LIMIT_ATTACHED)
         1

      .. testcleanup:: sqlite3.limits

         con.close()

      .. versionadded:: 3.11

   .. _SQLite limit category: https://www.sqlite.org/c3ref/c_limit_attached.html


   .. method:: getconfig(op, /)

      Truy vấn một tùy chọn cấu hình kết nối kiểu boolean.

      :param int op:Một :ref:`mã SQLITE_DBCONFIG <sqlite3-dbconfig-constants>`.

      :rtype: bool

      .. versionadded:: 3.12

   .. method:: setconfig(op, enable=True, /)

      Đặt một tùy chọn cấu hình kết nối kiểu boolean.

      :param int op:Một :ref:`mã SQLITE_DBCONFIG <sqlite3-dbconfig-constants>`.

      :param bool enable:``True`` nếu tùy chọn cấu hình cần được bật (mặc định); ``False`` nếu tùy chọn này cần được tắt.

      .. versionadded:: 3.12

   .. method:: serialize(*, name="main")

      Tuần tự hóa một cơ sở dữ liệu thành một đối tượng :class:`bytes`. Đối với tệp cơ sở dữ liệu thông thường trên đĩa, dữ liệu tuần tự hóa chỉ là một bản sao của tệp trên đĩa. Đối với cơ sở dữ liệu trong bộ nhớ hoặc cơ sở dữ liệu "temp", dữ liệu tuần tự hóa là cùng một chuỗi byte sẽ được ghi vào đĩa nếu cơ sở dữ liệu đó được sao lưu vào đĩa.

      :param str name:Tên cơ sở dữ liệu cần được tuần tự hóa. Mặc định là ``"main"``.

      :rtype: bytes

      .. note::

         Phương thức này chỉ khả dụng nếu thư viện SQLite bên dưới có API serialize.

      .. versionadded:: 3.11


   .. method:: deserialize(data, /, *, name="main")

      Giải tuần tự một cơ sở dữ liệu :meth:`serialized <serialize>` thành một
      :class:`Connection`. Phương thức này khiến kết nối cơ sở dữ liệu ngắt kết nối khỏi cơ sở dữ liệu có tên *name*, rồi mở lại *name* dưới dạng cơ sở dữ liệu trong bộ nhớ dựa trên nội dung tuần tự hóa trong *data*.

      :param bytes data:Một cơ sở dữ liệu đã được tuần tự hóa.

      :param str name:Tên cơ sở dữ liệu để giải tuần tự vào đó. Mặc định là ``"main"``.

      :raises OperationalError:Nếu kết nối cơ sở dữ liệu hiện đang tham gia vào một giao dịch đọc hoặc thao tác sao lưu.

      :raises DatabaseError:Nếu *data* không chứa một cơ sở dữ liệu SQLite hợp lệ.

      :raises OverflowError:Nếu :func:`len(data) <len>` lớn hơn ``2**63 - 1``.

      .. note::

         Phương thức này chỉ khả dụng nếu thư viện SQLite nền tảng có API deserialize.

      .. versionadded:: 3.11

   .. attribute:: autocommit

      Thuộc tính này kiểm soát hành vi giao dịch tuân thủ :pep:`249`.
      :attr:`!autocommit` có ba giá trị được phép:

      * ``False``: Chọn hành vi giao dịch tuân thủ :pep:`249`, ngụ ý rằng :mod:`!sqlite3` đảm bảo một giao dịch luôn mở. Sử dụng :meth:`commit` và :meth:`rollback` để đóng các giao dịch.

        Đây là giá trị được khuyến nghị cho :attr:`!autocommit`.

      * ``True``: Sử dụng `chế độ autocommit của SQLite <autocommit mode_>`_.
        :meth:`commit` và :meth:`rollback` không có tác dụng ở chế độ này.

      * :data:`LEGACY_TRANSACTION_CONTROL`: Kiểm soát giao dịch trước Python 3.12 (không tuân thủ :pep:`249`). Xem :attr:`isolation_level` để biết thêm chi tiết.

        Đây hiện là giá trị mặc định của :attr:`!autocommit`.

      Thay đổi :attr:`!autocommit` thành ``False`` sẽ mở một giao dịch mới, còn thay đổi thành ``True`` sẽ commit mọi giao dịch đang chờ xử lý.

      Xem :ref:`sqlite3-transaction-control-autocommit` để biết thêm chi tiết.

      .. note::

         Thuộc tính :attr:`isolation_level` không có tác dụng trừ khi
         :attr:`autocommit` là :data:`LEGACY_TRANSACTION_CONTROL`.

      .. versionadded:: 3.12

   .. attribute:: in_transaction

      Thuộc tính chỉ đọc này tương ứng với `chế độ autocommit cấp thấp <autocommit mode_>`_ của SQLite.

      ``True`` nếu một giao dịch đang hoạt động (có các thay đổi chưa commit), ``False`` nếu không.

      .. versionadded:: 3.2

   .. attribute:: isolation_level

      Kiểm soát :ref:`chế độ xử lý giao dịch legacy <sqlite3-transaction-control-isolation-level>` của :mod:`!sqlite3`. Nếu được đặt thành ``None``, các giao dịch sẽ không bao giờ được mở ngầm. Nếu được đặt thành một trong ``"DEFERRED"``, ``"IMMEDIATE"`` hoặc ``"EXCLUSIVE"``, tương ứng với `hành vi giao dịch SQLite <SQLite transaction behaviour_>`_ cơ bản,
      :ref:`việc quản lý giao dịch ngầm <sqlite3-transaction-control-isolation-level>` sẽ được thực hiện.

      Nếu không bị ghi đè bởi tham số *isolation_level* của :func:`connect`, giá trị mặc định là ``""``, đây là bí danh của ``"DEFERRED"``.

      .. note::

         Khuyến nghị sử dụng :attr:`autocommit` để kiểm soát việc xử lý giao dịch thay vì sử dụng :attr:`!isolation_level`.
         :attr:`!isolation_level` không có tác dụng trừ khi :attr:`autocommit` được đặt thành :data:`LEGACY_TRANSACTION_CONTROL` (mặc định).

   .. attribute:: row_factory

      :attr:`~Cursor.row_factory` ban đầu cho các đối tượng :class:`Cursor` được tạo từ kết nối này. Việc gán cho thuộc tính này không ảnh hưởng đến :attr:`!row_factory` của các cursor hiện có thuộc kết nối này, mà chỉ ảnh hưởng đến các cursor mới. Theo mặc định, thuộc tính này là ``None``, nghĩa là mỗi hàng được trả về dưới dạng :class:`tuple`.

      Xem :ref:`sqlite3-howto-row-factory` để biết thêm chi tiết.

      .. versionchanged:: 3.14.6
         Không còn được phép xóa thuộc tính ``row_factory``.

   .. attribute:: text_factory

      Một :term:`callable` nhận tham số :class:`bytes` và trả về biểu diễn dạng văn bản của tham số đó. Callable này được gọi cho các giá trị SQLite có kiểu dữ liệu ``TEXT``. Theo mặc định, thuộc tính này được đặt thành :class:`str`.

      Xem :ref:`sqlite3-howto-encoding` để biết thêm chi tiết.

      .. versionchanged:: 3.14.6
         Không còn được phép xóa thuộc tính ``text_factory``.

   .. attribute:: total_changes

      Trả về tổng số hàng trong cơ sở dữ liệu đã được sửa đổi, chèn hoặc xóa kể từ khi kết nối cơ sở dữ liệu được mở.


.. _sqlite3-cursor-objects:

Đối tượng cursor
^^^^^^^^^^^^^^^^

   Một đối tượng ``Cursor`` đại diện cho `con trỏ cơ sở dữ liệu <database cursor_>`_ được dùng để thực thi các câu lệnh SQL và quản lý ngữ cảnh của thao tác fetch. Cursor được tạo bằng :meth:`Connection.cursor` hoặc bằng bất kỳ :ref:`phương thức tắt nào của connection <sqlite3-connection-shortcuts>`.

   Đối tượng cursor là :term:`iterator <iterator>`, nghĩa là nếu bạn :meth:`~Cursor.execute` thực thi một ``SELECT`` truy vấn, bạn chỉ cần lặp qua cursor để lấy các hàng kết quả:

   .. testsetup:: sqlite3.cursor

      import sqlite3
      con = sqlite3.connect(":memory:", isolation_level=None)
      cur = con.execute("CREATE TABLE data(t)")
      cur.execute("INSERT INTO data VALUES(1)")

   .. testcode:: sqlite3.cursor

      for row in cur.execute("SELECT t FROM data"):
          print(row)

   .. testoutput:: sqlite3.cursor
      :hide:

      (1,)

   .. _database cursor: https://en.wikipedia.org/wiki/Cursor_(databases)

.. class:: Cursor

   Một :class:`Cursor` instance có các thuộc tính và phương thức sau đây.

   .. index:: single: ? (question mark); in SQL statements
   .. index:: single: : (colon); in SQL statements

   .. method:: execute(sql, parameters=(), /)

      Thực thi một câu lệnh SQL duy nhất, tùy chọn binding các giá trị Python bằng cách sử dụng
      :ref:`placeholder <sqlite3-placeholders>`.

      :param str sql:Một câu lệnh SQL duy nhất.

      :param parameters:Các giá trị Python để liên kết với các placeholder trong *sql*. Một :class:`!dict` nếu sử dụng placeholder có tên. Một :term:`!sequence` nếu sử dụng placeholder không có tên. Xem :ref:`sqlite3-placeholders`.
      :type parameters: :class:`dict` | :term:`sequence`

      :raises ProgrammingError:Khi *sql* chứa nhiều câu lệnh SQL. Khi sử dụng :ref:`named placeholders <sqlite3-placeholders>` và *parameters* là một sequence thay vì một :class:`dict`.

      Nếu :attr:`~Connection.autocommit` là
      :data:`LEGACY_TRANSACTION_CONTROL`,
      Nếu :attr:`~Connection.isolation_level` không phải là ``None``, *sql* là một câu lệnh ``INSERT``, ``UPDATE``, ``DELETE`` hoặc ``REPLACE``, và không có transaction nào đang mở, một transaction sẽ được ngầm mở trước khi thực thi *sql*.

      .. versionchanged:: 3.14

         :exc:`ProgrammingError` sẽ được phát ra nếu
         Khi sử dụng :ref:`named placeholders <sqlite3-placeholders>` và *parameters* là một sequence thay vì một :class:`dict`.

      Sử dụng :meth:`executescript` để thực thi nhiều câu lệnh SQL.

   .. method:: executemany(sql, parameters, /)

      Với mỗi mục trong *parameters*, thực thi lặp lại :ref:`parameterized <sqlite3-placeholders>`
      Câu lệnh SQL :abbr:`DML (Ngôn ngữ thao tác dữ liệu)` *sql*.

      Sử dụng cùng cách xử lý giao dịch ngầm định như :meth:`~Cursor.execute`.

      :param str sql:Một câu lệnh SQL DML duy nhất.

      :param parameters:Một :term:`!iterable` gồm các tham số để liên kết với các placeholder trong *sql*. Xem :ref:`sqlite3-placeholders`.
      :type parameters: :term:`iterable`

      :raises ProgrammingError:Khi *sql* chứa nhiều hơn một câu lệnh SQL hoặc không phải là câu lệnh DML, khi sử dụng :ref:`placeholder được đặt tên <sqlite3-placeholders>` và các mục trong *parameters* là các sequence thay vì :class:`dict`\s.

      Ví dụ:

      .. testcode:: sqlite3.cursor

         rows = [
             ("row1",),
             ("row2",),
         ]
         # cur là một đối tượng sqlite3.Cursor
         cur.executemany("INSERT INTO data VALUES(?)", rows)

      .. testcleanup:: sqlite3.cursor

         con.close()

      .. note::

         Mọi hàng kết quả đều bị loại bỏ, bao gồm cả các câu lệnh DML có mệnh đề `RETURNING clauses <RETURNING clauses_>`_.

      .. _RETURNING clauses: https://www.sqlite.org/lang_returning.html

      .. versionchanged:: 3.14

         :exc:`ProgrammingError` sẽ được phát ra nếu
         :ref:`named placeholders <sqlite3-placeholders>` được sử dụng và các mục trong *parameters* là các sequence thay vì :class:`dict`\s.

   .. method:: executescript(sql_script, /)

      Thực thi các câu lệnh SQL trong *sql_script*. Nếu :attr:`~Connection.autocommit` là
      :data:`LEGACY_TRANSACTION_CONTROL` và có một giao dịch đang chờ xử lý, trước tiên sẽ thực thi một câu lệnh ``COMMIT`` ngầm định. Không thực hiện bất kỳ thao tác kiểm soát giao dịch ngầm định nào khác; mọi thao tác kiểm soát giao dịch phải được thêm vào *sql_script*.

      *sql_script* phải là một :class:`string <str>`.

      Ví dụ:

      .. testcode:: sqlite3.cursor

         # cur là một đối tượng sqlite3.Cursor
         cur.executescript("""
             BEGIN;
             CREATE TABLE person(firstname, lastname, age);
             CREATE TABLE book(title, author, published);
             CREATE TABLE publisher(name, address);
             COMMIT;
         """)

   .. method:: fetchone()

      Nếu :attr:`~Cursor.row_factory` là ``None``, trả về tập kết quả của truy vấn hàng tiếp theo dưới dạng :class:`tuple`. Nếu không, truyền kết quả đó cho row factory và trả về kết quả của nó. Trả về ``None`` nếu không còn dữ liệu.


   .. method:: fetchmany(size=cursor.arraysize)

      Trả về tập các hàng tiếp theo của kết quả truy vấn dưới dạng :class:`list`. Trả về một danh sách rỗng nếu không còn hàng nào.

      Số hàng cần lấy trong mỗi lần gọi được chỉ định bởi tham số *size*. Nếu không cung cấp *size*, :attr:`arraysize` sẽ xác định số hàng cần lấy. Nếu có ít hơn *size* hàng, số hàng hiện có sẽ được trả về.

      Lưu ý rằng tham số *size* có những cân nhắc về hiệu năng. Để đạt hiệu năng tối ưu, thông thường nên sử dụng thuộc tính arraysize. Nếu sử dụng tham số *size*, tốt nhất là giữ nguyên giá trị của tham số này từ lần gọi :meth:`fetchmany` này đến lần gọi tiếp theo.

      .. versionchanged:: 3.14.1
         Các giá trị *size* âm sẽ bị từ chối bằng cách nêu ra :exc:`ValueError`.

   .. method:: fetchall()

      Trả về tất cả các hàng (còn lại) của kết quả truy vấn dưới dạng một :class:`list`. Trả về một danh sách rỗng nếu không có hàng nào. Lưu ý rằng thuộc tính :attr:`arraysize` có thể ảnh hưởng đến hiệu suất của thao tác này.

   .. method:: close()

      Đóng cursor ngay bây giờ (thay vì khi ``__del__`` được gọi).

      Cursor sẽ không thể sử dụng kể từ thời điểm này; một ngoại lệ :exc:`ProgrammingError` sẽ được phát sinh nếu cố thực hiện bất kỳ thao tác nào với cursor.

   .. method:: setinputsizes(sizes, /)

      Bắt buộc theo DB-API. Không thực hiện thao tác nào trong :mod:`!sqlite3`.

   .. method:: setoutputsize(size, column=None, /)

      Bắt buộc theo DB-API. Không thực hiện thao tác nào trong :mod:`!sqlite3`.

   .. attribute:: arraysize

      Thuộc tính đọc/ghi kiểm soát số lượng hàng được trả về bởi :meth:`fetchmany`. Giá trị mặc định là 1, nghĩa là mỗi lần gọi sẽ lấy một hàng duy nhất.

      .. versionchanged:: 3.14.1
         Các giá trị âm sẽ bị từ chối bằng cách phát sinh :exc:`ValueError`.

   .. attribute:: connection

      Thuộc tính chỉ đọc cung cấp cơ sở dữ liệu SQLite :class:`Connection` thuộc về cursor. Một đối tượng :class:`Cursor` được tạo bằng cách gọi :meth:`con.cursor() <Connection.cursor>` sẽ có
      thuộc tính :attr:`connection` tham chiếu đến *con*:

      .. doctest::

         >>> con = sqlite3.connect(":memory:")
         >>> cur = con.cursor()
         >>> cur.connection == con
         True
         >>> con.close()

   .. attribute:: description

      Thuộc tính chỉ đọc cung cấp tên các cột của truy vấn gần nhất. Để duy trì khả năng tương thích với Python DB API, thuộc tính này trả về một bộ 7 phần tử cho mỗi cột, trong đó sáu phần tử cuối của mỗi bộ là ``None``.

      Thuộc tính này cũng được thiết lập cho các câu lệnh ``SELECT`` không có hàng nào khớp.

   .. attribute:: lastrowid

      Thuộc tính chỉ đọc cung cấp row id của hàng được chèn gần nhất. Thuộc tính này chỉ được cập nhật sau các câu lệnh ``INSERT`` hoặc ``REPLACE`` thực thi thành công bằng phương thức :meth:`execute`. Đối với các câu lệnh khác, sau khi
      :meth:`executemany` hoặc :meth:`executescript`, hoặc nếu thao tác chèn thất bại, giá trị của ``lastrowid`` vẫn không thay đổi. Giá trị ban đầu của ``lastrowid`` là ``None``.

      .. note::
         Các thao tác chèn vào bảng ``WITHOUT ROWID`` không được ghi lại.

      .. versionchanged:: 3.6
         Đã bổ sung hỗ trợ cho câu lệnh ``REPLACE``.

   .. attribute:: rowcount

      Thuộc tính chỉ đọc cung cấp số hàng đã được sửa đổi đối với các câu lệnh ``INSERT``, ``UPDATE``, ``DELETE`` và ``REPLACE``; là ``-1`` đối với các câu lệnh khác, bao gồm cả các truy vấn :abbr:`CTE (Common Table Expression)`. Thuộc tính này chỉ được cập nhật bởi các phương thức :meth:`execute` và :meth:`executemany`, sau khi câu lệnh chạy hoàn tất. Điều này có nghĩa là mọi hàng được trả về phải được lấy để
      :attr:`!rowcount` được cập nhật.

   .. attribute:: row_factory

      Kiểm soát cách biểu diễn một hàng được lấy từ :class:`!Cursor` này. Nếu là ``None``, một hàng sẽ được biểu diễn dưới dạng :class:`tuple`. Có thể đặt thành :class:`sqlite3.Row` đi kèm; hoặc một :term:`callable` nhận hai đối số, một đối tượng :class:`Cursor` và :class:`!tuple` các giá trị hàng, rồi trả về một đối tượng tùy chỉnh đại diện cho một hàng SQLite.

      Mặc định là giá trị mà :attr:`Connection.row_factory` được đặt thành khi :class:`!Cursor` được tạo. Việc gán cho thuộc tính này không ảnh hưởng đến
      :attr:`Connection.row_factory` của connection cha.

      Xem :ref:`sqlite3-howto-row-factory` để biết thêm chi tiết.

      .. versionchanged:: 3.14.6
         Việc xóa thuộc tính ``row_factory`` không còn được phép.


.. The sqlite3.Row example used to be a how-to. It has now been incorporated
   into the Row reference. We keep the anchor here in order not to break
   existing links.

.. _sqlite3-columns-by-name:
.. _sqlite3-row-objects:

Đối tượng hàng
^^^^^^^^^^^^^^

.. class:: Row

   Một instance :class:`!Row` đóng vai trò là một
   :attr:`~Connection.row_factory` được tối ưu hóa cao cho các đối tượng :class:`Connection`. Nó hỗ trợ việc lặp, kiểm tra tính bằng nhau, :func:`len` và truy cập :term:`mapping` theo tên và chỉ mục cột.

   Hai đối tượng :class:`!Row` được xem là bằng nhau nếu chúng có tên cột và giá trị giống hệt nhau.

   Xem :ref:`sqlite3-howto-row-factory` để biết thêm chi tiết.

   .. method:: keys

      Trả về một :class:`list` gồm tên cột dưới dạng :class:`strings <str>`. Ngay sau một truy vấn, đây là phần tử đầu tiên của mỗi tuple trong :attr:`Cursor.description`.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ slicing.


.. _sqlite3-blob-objects:

Đối tượng Blob
^^^^^^^^^^^^^^

.. class:: Blob

   .. versionadded:: 3.11

   Một thực thể :class:`Blob` là một :term:`file-like object` có thể đọc và ghi dữ liệu trong một SQLite :abbr:`BLOB (Binary Large OBject)`. Gọi :func:`len(blob) <len>` để lấy kích thước (số byte) của blob. Sử dụng các chỉ mục và :term:`slices <slice>` để truy cập trực tiếp vào dữ liệu blob.

   Sử dụng :class:`Blob` như một :term:`context manager` để đảm bảo handle của blob được đóng sau khi sử dụng.

   .. testcode::

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE test(blob_col blob)")
      con.execute("INSERT INTO test(blob_col) VALUES(zeroblob(13))")

      # Ghi vào blob của chúng ta bằng hai thao tác ghi:
      with con.blobopen("test", "blob_col", 1) as blob:
          blob.write(b"hello, ")
          blob.write(b"world.")
          # Sửa đổi byte đầu tiên và byte cuối cùng của blob
          blob[0] = ord("H")
          blob[-1] = ord("!")

      # Đọc nội dung của blob
      with con.blobopen("test", "blob_col", 1) as blob:
          greeting = blob.read()

      print(greeting)  # xuất "b'Hello, world!'"
      con.close()

   .. testoutput::
      :hide:

      b'Hello, world!'

   .. method:: close()

      Đóng blob.

      Blob sẽ không thể sử dụng được kể từ thời điểm này. Một
      :class:`~sqlite3.Error` (hoặc lớp con) exception sẽ được phát sinh nếu thực hiện bất kỳ thao tác nào khác với blob.

   .. method:: read(length=-1, /)

      Đọc *length* byte dữ liệu từ blob tại vị trí offset hiện tại. Nếu đã đến cuối blob, dữ liệu cho đến
      :abbr:`EOF (End of File)` sẽ được trả về. Khi không chỉ định *length*, hoặc giá trị này là số âm, :meth:`~Blob.read` sẽ đọc cho đến cuối blob.

   .. method:: write(data, /)

      Ghi *data* vào blob tại offset hiện tại. Hàm này không thể thay đổi độ dài blob. Việc ghi vượt quá cuối blob sẽ phát sinh
      :exc:`ValueError`.

   .. method:: tell()

      Trả về vị trí truy cập hiện tại của blob.

   .. method:: seek(offset, origin=os.SEEK_SET, /)

      Đặt vị trí truy cập hiện tại của blob thành *offset*. Đối số *origin* mặc định là :const:`os.SEEK_SET` (định vị blob tuyệt đối). Các giá trị khác của *origin* là :const:`os.SEEK_CUR` (tìm kiếm tương đối so với vị trí hiện tại) và :const:`os.SEEK_END` (tìm kiếm tương đối so với cuối blob).


Đối tượng PrepareProtocol
^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: PrepareProtocol

   Mục đích duy nhất của kiểu PrepareProtocol là hoạt động như một giao thức điều chỉnh kiểu :pep:`246` cho các đối tượng có thể :ref:`tự điều chỉnh <sqlite3-conform>` thành :ref:`các kiểu SQLite gốc <sqlite3-types>`.


.. _sqlite3-exceptions:

Ngoại lệ
^^^^^^^^

Hệ thống phân cấp ngoại lệ được định nghĩa bởi DB-API 2.0 (:pep:`249`).

.. exception:: Warning

   Ngoại lệ này hiện không được module :mod:`!sqlite3` đưa ra, nhưng có thể được đưa ra bởi các ứng dụng sử dụng :mod:`!sqlite3`, chẳng hạn như khi một hàm do người dùng định nghĩa cắt ngắn dữ liệu trong quá trình chèn. ``Warning`` là lớp con của :exc:`Exception`.

.. exception:: Error

   Lớp cơ sở của các ngoại lệ khác trong mô-đun này. Dùng lớp này để bắt tất cả lỗi chỉ bằng một câu lệnh :keyword:`except`. ``Error`` là lớp con của :exc:`Exception`.

   Nếu ngoại lệ bắt nguồn từ bên trong thư viện SQLite, hai thuộc tính sau sẽ được thêm vào ngoại lệ:

   .. attribute:: sqlite_errorcode

      Mã lỗi dạng số từ `SQLite API <https://sqlite.org/rescode.html>`_

      .. versionadded:: 3.11

   .. attribute:: sqlite_errorname

      Tên ký hiệu của mã lỗi dạng số từ `SQLite API <https://sqlite.org/rescode.html>`_

      .. versionadded:: 3.11

.. exception:: InterfaceError

   Ngoại lệ được nâng lên khi sử dụng sai SQLite C API cấp thấp. Nói cách khác, nếu ngoại lệ này được nâng lên, có thể nó cho biết có lỗi trong
   :mod:`!sqlite3` mô-đun. ``InterfaceError`` là lớp con của :exc:`Error`.

.. exception:: DatabaseError

   Ngoại lệ được nâng lên cho các lỗi liên quan đến cơ sở dữ liệu. Đây là ngoại lệ cơ sở cho một số loại lỗi cơ sở dữ liệu. Ngoại lệ này chỉ được nâng lên một cách ngầm định thông qua các lớp con chuyên biệt. ``DatabaseError`` là lớp con của :exc:`Error`.

.. exception:: DataError

   Ngoại lệ được phát sinh cho các lỗi do vấn đề với dữ liệu được xử lý, chẳng hạn như giá trị số nằm ngoài phạm vi và chuỗi quá dài. ``DataError`` là lớp con của :exc:`DatabaseError`.

.. exception:: OperationalError

   Ngoại lệ được phát sinh cho các lỗi liên quan đến hoạt động của cơ sở dữ liệu và không nhất thiết nằm trong quyền kiểm soát của lập trình viên. Ví dụ: không tìm thấy đường dẫn cơ sở dữ liệu hoặc không thể xử lý một giao dịch. ``OperationalError`` là lớp con của :exc:`DatabaseError`.

.. exception:: IntegrityError

   Ngoại lệ được phát sinh khi tính toàn vẹn quan hệ của cơ sở dữ liệu bị ảnh hưởng, chẳng hạn như khi kiểm tra khóa ngoại không thành công. Đây là lớp con của :exc:`DatabaseError`.

.. exception:: InternalError

   Ngoại lệ được phát sinh khi SQLite gặp lỗi nội bộ. Nếu ngoại lệ này được phát sinh, có thể runtime SQLite library đang gặp vấn đề. ``InternalError`` là lớp con của :exc:`DatabaseError`.

.. exception:: ProgrammingError

   Ngoại lệ được phát sinh đối với các lỗi lập trình API của :mod:`!sqlite3`, chẳng hạn như cung cấp sai số lượng binding cho một truy vấn hoặc cố thao tác trên một :class:`Connection` đã đóng. ``ProgrammingError`` là lớp con của :exc:`DatabaseError`.

.. exception:: NotSupportedError

   Ngoại lệ được phát sinh khi một phương thức hoặc API cơ sở dữ liệu không được SQLite library bên dưới hỗ trợ. Ví dụ: đặt *deterministic* thành ``True`` trong :meth:`~Connection.create_function` nếu SQLite library bên dưới không hỗ trợ các hàm deterministic. ``NotSupportedError`` là lớp con của :exc:`DatabaseError`.


.. _sqlite3-types:

Các kiểu SQLite và Python
^^^^^^^^^^^^^^^^^^^^^^^^^

SQLite hỗ trợ nguyên bản các kiểu sau: ``NULL``, ``INTEGER``, ``REAL``, ``TEXT``, ``BLOB``.

Do đó, các kiểu Python sau có thể được gửi đến SQLite mà không gặp vấn đề gì:

+----------------+-------------+
| Kiểu Python    | Kiểu SQLite |
+================+=============+
| ``None``       | ``NULL``    |
+----------------+-------------+
| :class:`int`   | ``INTEGER`` |
+----------------+-------------+
| :class:`float` | ``REAL``    |
+----------------+-------------+
| :class:`str`   | ``TEXT``    |
+----------------+-------------+
| :class:`bytes` | ``BLOB``    |
+----------------+-------------+


Theo mặc định, các kiểu SQLite được chuyển đổi sang kiểu Python như sau:

+-------------+-------------------------------------------------+
| Kiểu SQLite | Kiểu Python                                     |
+=============+=================================================+
| ``NULL``    | ``None``                                        |
+-------------+-------------------------------------------------+
| ``INTEGER`` | :class:`int`                                    |
+-------------+-------------------------------------------------+
| ``REAL``    | :class:`float`                                  |
+-------------+-------------------------------------------------+
| ``TEXT``    | phụ thuộc vào :attr:`~Connection.text_factory`, |
|             | :class:`str` theo mặc định                      |
+-------------+-------------------------------------------------+
| ``BLOB``    | :class:`bytes`                                  |
+-------------+-------------------------------------------------+

Hệ thống kiểu của mô-đun :mod:`!sqlite3` có thể mở rộng theo hai cách: bạn có thể lưu trữ các kiểu Python bổ sung trong cơ sở dữ liệu SQLite thông qua
:ref:`bộ điều hợp đối tượng <sqlite3-adapters>`, và bạn có thể để mô-đun :mod:`!sqlite3` chuyển đổi các kiểu SQLite thành các kiểu Python thông qua :ref:`bộ chuyển đổi <sqlite3-converters>`.


.. _sqlite3-default-converters:

Bộ điều hợp và bộ chuyển đổi mặc định (đã lỗi thời)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   Các bộ điều hợp và bộ chuyển đổi mặc định đã lỗi thời kể từ Python 3.12. Thay vào đó, hãy sử dụng :ref:`sqlite3-adapter-converter-recipes` và điều chỉnh chúng cho phù hợp với nhu cầu của bạn.

Các bộ điều hợp và bộ chuyển đổi mặc định đã lỗi thời bao gồm:

* Bộ chuyển đổi cho các đối tượng :class:`datetime.date` sang :class:`strings <str>` ở định dạng `ISO 8601 <ISO 8601_>`_.
* Bộ chuyển đổi cho các đối tượng :class:`datetime.datetime` sang chuỗi ở định dạng ISO 8601.
* Bộ chuyển đổi cho các kiểu "date" :ref:`được khai báo <sqlite3-converters>` sang
  các đối tượng :class:`datetime.date`.
* Bộ chuyển đổi cho các kiểu "timestamp" đã khai báo sang
  các đối tượng :class:`datetime.datetime`. Phần thập phân sẽ bị cắt ngắn còn 6 chữ số (độ chính xác microsecond).

.. note::

   Bộ chuyển đổi "timestamp" mặc định bỏ qua các độ lệch UTC trong cơ sở dữ liệu và luôn trả về một đối tượng :class:`datetime.datetime` không có thông tin múi giờ. Để giữ lại các độ lệch UTC trong timestamp, hãy tắt các bộ chuyển đổi hoặc đăng ký một bộ chuyển đổi có hỗ trợ độ lệch với :func:`register_converter`.

.. deprecated:: 3.12

.. _ISO 8601: https://en.wikipedia.org/wiki/ISO_8601


.. _sqlite3-cli:

Giao diện dòng lệnh
^^^^^^^^^^^^^^^^^^^

Có thể gọi module :mod:`!sqlite3` như một script bằng switch :option:`-m` của trình thông dịch để cung cấp một shell SQLite đơn giản. Cú pháp đối số như sau::

   python -m sqlite3 [-h] [-v] [filename] [sql]

Nhập ``.quit`` hoặc CTRL-D để thoát shell.

.. program:: python -m sqlite3 [-h] [-v] [filename] [sql]

.. option:: -h, --help

   In trợ giúp CLI.

.. option:: -v, --version

   In phiên bản thư viện SQLite nền tảng.

.. versionadded:: 3.12


.. _sqlite3-howtos:

Hướng dẫn thực hiện
-------------------

.. _sqlite3-placeholders:

Cách sử dụng placeholder để liên kết giá trị trong các truy vấn SQL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các thao tác SQL thường cần sử dụng các giá trị từ biến Python. Tuy nhiên, hãy cẩn thận khi dùng các thao tác chuỗi của Python để ghép truy vấn, vì chúng dễ bị `tấn công SQL injection <SQL injection attacks_>`_. Ví dụ, kẻ tấn công có thể chỉ cần đóng dấu nháy đơn rồi chèn ``OR TRUE`` để chọn tất cả các hàng::

   >>> # Tuyệt đối không làm như vậy -- không an toàn!
   >>> symbol = input()
   ' OR TRUE; --
   >>> sql = "SELECT * FROM stocks WHERE symbol = '%s'" % symbol
   >>> print(sql)
   SELECT * FROM stocks WHERE symbol = '' OR TRUE; --'
   >>> cur.execute(sql)

Thay vào đó, hãy sử dụng cơ chế thay thế tham số của DB-API. Để chèn một biến vào chuỗi truy vấn, hãy sử dụng một placeholder trong chuỗi, rồi thay thế các giá trị thực tế vào truy vấn bằng cách cung cấp chúng dưới dạng một :class:`tuple` gồm các giá trị cho đối số thứ hai của phương thức :meth:`~Cursor.execute` của cursor.

Một câu lệnh SQL có thể sử dụng một trong hai loại placeholder: dấu chấm hỏi (kiểu qmark) hoặc placeholder có tên (kiểu named). Với kiểu qmark, *parameters* phải là một
:term:`sequence` có độ dài phải khớp với số lượng placeholder, nếu không sẽ phát sinh :exc:`ProgrammingError`. Với kiểu named, *parameters* phải là một thể hiện của :class:`dict` (hoặc một lớp con), và phải chứa khóa cho tất cả các tham số có tên; mọi phần tử thừa sẽ bị bỏ qua. Dưới đây là ví dụ về cả hai kiểu:

.. testcode::

   con = sqlite3.connect(":memory:")
   cur = con.execute("CREATE TABLE lang(name, first_appeared)")

   # Đây là kiểu named được sử dụng với executemany():
   data = (
       {"name": "C", "year": 1972},
       {"name": "Fortran", "year": 1957},
       {"name": "Python", "year": 1991},
       {"name": "Go", "year": 2009},
   )
   cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)

   # Đây là kiểu qmark được sử dụng trong truy vấn SELECT:
   params = (1972,)
   cur.execute("SELECT * FROM lang WHERE first_appeared = ?", params)
   print(cur.fetchall())
   con.close()

.. testoutput::
   :hide:

   [('C', 1972)]

.. note::

   :pep:`249` các placeholder dạng số *không* được hỗ trợ. Nếu được sử dụng, chúng sẽ được diễn giải là các placeholder có tên.


.. _sqlite3-adapters:

Cách điều chỉnh các kiểu Python tùy chỉnh cho các giá trị SQLite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SQLite chỉ hỗ trợ nguyên bản một tập hợp kiểu dữ liệu hạn chế. Để lưu trữ các kiểu Python tùy chỉnh trong cơ sở dữ liệu SQLite, hãy *điều chỉnh* chúng thành một trong các
:ref:`kiểu Python mà SQLite hiểu nguyên bản <sqlite3-types>`.

Có hai cách để điều chỉnh các đối tượng Python cho phù hợp với các kiểu SQLite: để đối tượng tự điều chỉnh hoặc sử dụng một *adapter callable*. Cách thứ hai sẽ được ưu tiên hơn cách thứ nhất. Đối với một thư viện cung cấp một kiểu tùy chỉnh, việc cho phép kiểu đó tự điều chỉnh có thể là lựa chọn hợp lý. Với vai trò nhà phát triển ứng dụng, việc trực tiếp kiểm soát bằng cách đăng ký các hàm adapter tùy chỉnh có thể phù hợp hơn.


.. _sqlite3-conform:

Cách viết các đối tượng có thể điều chỉnh
"""""""""""""""""""""""""""""""""""""""""

Giả sử chúng ta có một :class:`!Point` lớp đại diện cho một cặp tọa độ, ``x`` và ``y``, trong hệ tọa độ Descartes. Cặp tọa độ này sẽ được lưu trữ dưới dạng chuỗi văn bản trong cơ sở dữ liệu, dùng dấu chấm phẩy để phân tách các tọa độ. Có thể triển khai điều này bằng cách thêm một phương thức ``__conform__(self, protocol)`` trả về giá trị đã điều chỉnh. Đối tượng được truyền cho *protocol* sẽ có kiểu :class:`PrepareProtocol`.

.. testcode::

   class Point:
       def __init__(self, x, y):
           self.x, self.y = x, y

       def __conform__(self, protocol):
           if protocol is sqlite3.PrepareProtocol:
               return f"{self.x};{self.y}"

   con = sqlite3.connect(":memory:")
   cur = con.cursor()

   cur.execute("SELECT ?", (Point(4.0, -3.2),))
   print(cur.fetchone()[0])
   con.close()

.. testoutput::
   :hide:

   4.0;-3.2


Cách đăng ký các callable adapter
"""""""""""""""""""""""""""""""""

Một khả năng khác là tạo một hàm chuyển đổi đối tượng Python thành kiểu tương thích với SQLite. Sau đó, có thể đăng ký hàm này bằng :func:`register_adapter`.

.. testcode::

   class Point:
       def __init__(self, x, y):
           self.x, self.y = x, y

   def adapt_point(point):
       return f"{point.x};{point.y}"

   sqlite3.register_adapter(Point, adapt_point)

   con = sqlite3.connect(":memory:")
   cur = con.cursor()

   cur.execute("SELECT ?", (Point(1.0, 2.5),))
   print(cur.fetchone()[0])
   con.close()

.. testoutput::
   :hide:

   1.0;2.5


.. _sqlite3-converters:

Cách chuyển đổi các giá trị SQLite thành các kiểu Python tùy chỉnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Việc viết một adapter cho phép bạn chuyển đổi *từ* các kiểu Python tùy chỉnh *sang* các giá trị SQLite. Để có thể chuyển đổi *từ* các giá trị SQLite *sang* các kiểu Python tùy chỉnh, chúng ta sử dụng *converters*.

Hãy quay lại lớp :class:`!Point`. Chúng ta đã lưu tọa độ x và y, được phân tách bằng dấu chấm phẩy, dưới dạng chuỗi trong SQLite.

Trước tiên, chúng ta sẽ định nghĩa một hàm converter nhận chuỗi làm tham số và tạo một đối tượng :class:`!Point` từ chuỗi đó.

.. note::

   Các hàm converter **luôn** nhận một :class:`bytes` object, bất kể kiểu dữ liệu SQLite bên dưới là gì.

.. testcode::

   def convert_point(s):
       x, y = map(float, s.split(b";"))
       return Point(x, y)

Bây giờ, chúng ta cần cho :mod:`!sqlite3` biết khi nào nó nên chuyển đổi một giá trị SQLite đã cho. Việc này được thực hiện khi kết nối với cơ sở dữ liệu, bằng cách sử dụng tham số *detect_types* của :func:`connect`. Có ba tùy chọn:

* Ngầm định: đặt *detect_types* thành :const:`PARSE_DECLTYPES`
* Tường minh: đặt *detect_types* thành :const:`PARSE_COLNAMES`
* Cả hai: đặt *detect_types* thành ``sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES``. Tên cột được ưu tiên hơn các kiểu đã khai báo.

Ví dụ sau minh họa các phương pháp ngầm định và tường minh:

.. testcode::

   class Point:
       def __init__(self, x, y):
           self.x, self.y = x, y

       def __repr__(self):
           return f"Point({self.x}, {self.y})"

   def adapt_point(point):
       return f"{point.x};{point.y}"

   def convert_point(s):
       x, y = list(map(float, s.split(b";")))
       return Point(x, y)

   # Đăng ký adapter và converter
   sqlite3.register_adapter(Point, adapt_point)
   sqlite3.register_converter("point", convert_point)

   # 1) Phân tích cú pháp bằng các kiểu đã khai báo
   p = Point(4.0, -3.2)
   con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
   cur = con.execute("CREATE TABLE test(p point)")

   cur.execute("INSERT INTO test(p) VALUES(?)", (p,))
   cur.execute("SELECT p FROM test")
   print("with declared types:", cur.fetchone()[0])
   cur.close()
   con.close()

   # 2) Phân tích bằng tên cột
   con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_COLNAMES)
   cur = con.execute("CREATE TABLE test(p)")

   cur.execute("INSERT INTO test(p) VALUES(?)", (p,))
   cur.execute('SELECT p AS "p [point]" FROM test')
   print("with column names:", cur.fetchone()[0])
   cur.close()
   con.close()

.. testoutput::
   :hide:

   with declared types: Point(4.0, -3.2)
   with column names: Point(4.0, -3.2)


.. _sqlite3-adapter-converter-recipes:

Các công thức adapter và converter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phần này trình bày các công thức cho những adapter và converter phổ biến.

.. testcode::

   import datetime as dt
   import sqlite3

   def adapt_date_iso(val):
       """Adapt datetime.date to ISO 8601 date."""
       return val.isoformat()

   def adapt_datetime_iso(val):
       """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
       return val.replace(tzinfo=None).isoformat()

   def adapt_datetime_epoch(val):
       """Adapt datetime.datetime to Unix timestamp."""
       return int(val.timestamp())

   sqlite3.register_adapter(dt.date, adapt_date_iso)
   sqlite3.register_adapter(dt.datetime, adapt_datetime_iso)
   sqlite3.register_adapter(dt.datetime, adapt_datetime_epoch)

   def convert_date(val):
       """Convert ISO 8601 date to datetime.date object."""
       return dt.date.fromisoformat(val.decode())

   def convert_datetime(val):
       """Convert ISO 8601 datetime to datetime.datetime object."""
       return dt.datetime.fromisoformat(val.decode())

   def convert_timestamp(val):
       """Convert Unix epoch timestamp to datetime.datetime object."""
       return dt.datetime.fromtimestamp(int(val))

   sqlite3.register_converter("date", convert_date)
   sqlite3.register_converter("datetime", convert_datetime)
   sqlite3.register_converter("timestamp", convert_timestamp)

.. testcode::
   :hide:

   when = dt.datetime(2019, 5, 18, 15, 17, 8, 123456)

   assert adapt_date_iso(when.date()) == "2019-05-18"
   assert convert_date(b"2019-05-18") == when.date()

   assert adapt_datetime_iso(when) == "2019-05-18T15:17:08.123456"
   assert convert_datetime(b"2019-05-18T15:17:08.123456") == when

   # Sử dụng thời gian hiện tại vì fromtimestamp() trả về ngày/giờ cục bộ.
   # Loại bỏ micro giây vì adapt_datetime_epoch cắt bớt phần giây lẻ.
   now = dt.datetime.now().replace(microsecond=0)
   current_timestamp = int(now.timestamp())

   assert adapt_datetime_epoch(now) == current_timestamp
   assert convert_timestamp(str(current_timestamp).encode()) == now


.. _sqlite3-connection-shortcuts:

Cách sử dụng các phương thức tắt của connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sử dụng :meth:`~Connection.execute`,
Với các phương thức :meth:`~Connection.executemany` và :meth:`~Connection.executescript` của lớp :class:`Connection`, mã của bạn có thể được viết ngắn gọn hơn vì bạn không phải tạo rõ ràng các đối tượng :class:`Cursor` (thường là không cần thiết). Thay vào đó, các đối tượng :class:`Cursor` được tạo ngầm và những phương thức shortcut này trả về các đối tượng cursor. Nhờ đó, bạn có thể thực thi một câu lệnh ``SELECT`` và lặp trực tiếp trên đó chỉ bằng một lần gọi đối tượng :class:`Connection`.

.. testcode::

   # Tạo và điền dữ liệu vào bảng.
   con = sqlite3.connect(":memory:")
   con.execute("CREATE TABLE lang(name, first_appeared)")
   data = [
       ("C++", 1985),
       ("Objective-C", 1984),
   ]
   con.executemany("INSERT INTO lang(name, first_appeared) VALUES(?, ?)", data)

   # In nội dung bảng
   for row in con.execute("SELECT name, first_appeared FROM lang"):
       print(row)

   print("I just deleted", con.execute("DELETE FROM lang").rowcount, "rows")

   # close() không phải là phương thức shortcut và không được tự động gọi;
   # đối tượng connection phải được đóng thủ công
   con.close()

.. testoutput::
   :hide:

   ('C++', 1985)
   ('Objective-C', 1984)
   I just deleted 2 rows


.. _sqlite3-connection-context-manager:

Cách sử dụng connection context manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một đối tượng :class:`Connection` có thể được dùng làm context manager để tự động commit hoặc rollback các giao dịch đang mở khi rời khỏi phần thân của context manager. Nếu phần thân của câu lệnh :keyword:`with` kết thúc mà không có ngoại lệ, giao dịch sẽ được commit. Nếu thao tác commit này thất bại hoặc nếu phần thân của câu lệnh ``with`` phát sinh một ngoại lệ không được bắt, giao dịch sẽ được rollback. Nếu :attr:`~Connection.autocommit` là ``False``, một giao dịch mới sẽ được mở ngầm sau khi commit hoặc rollback.

Nếu không có transaction nào đang mở khi rời khỏi phần thân của câu lệnh ``with``, hoặc nếu :attr:`~Connection.autocommit` là ``True``, context manager sẽ không làm gì.

.. note::
   Context manager không tự động mở transaction mới cũng không đóng connection. Nếu cần một context manager có chức năng đóng, hãy cân nhắc sử dụng :meth:`contextlib.closing`.

.. testcode::

   con = sqlite3.connect(":memory:")
   con.execute("CREATE TABLE lang(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE)")

   # Nếu thành công, con.commit() sẽ được gọi tự động sau đó
   with con:
       con.execute("INSERT INTO lang(name) VALUES(?)", ("Python",))

   # con.rollback() được gọi sau khi khối with kết thúc do có exception,
   # exception vẫn được raise và phải được catch
   try:
       with con:
           con.execute("INSERT INTO lang(name) VALUES(?)", ("Python",))
   except sqlite3.IntegrityError:
       print("couldn't add Python twice")

   # Đối tượng Connection được dùng làm context manager chỉ commit hoặc rollback các transaction,
   # do đó đối tượng connection phải được đóng thủ công
   con.close()

.. testoutput::
   :hide:

   couldn't add Python twice


.. _sqlite3-uri-tricks:

Cách làm việc với SQLite URI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một số thủ thuật URI hữu ích bao gồm:

* Mở cơ sở dữ liệu ở chế độ chỉ đọc:

.. doctest::

   >>> con = sqlite3.connect("file:tutorial.db?mode=ro", uri=True)
   >>> con.execute("CREATE TABLE readonly(data)")
   Traceback (most recent call last):
   OperationalError: attempt to write a readonly database
   >>> con.close()

* Không tự động tạo tệp cơ sở dữ liệu mới nếu tệp đó chưa tồn tại; sẽ phát sinh :exc:`~sqlite3.OperationalError` nếu không thể tạo tệp mới:

.. doctest::

   >>> con = sqlite3.connect("file:nosuchdb.db?mode=rw", uri=True)
   Traceback (most recent call last):
   OperationalError: unable to open database file


* Tạo cơ sở dữ liệu trong bộ nhớ có tên dùng chung:

.. testcode::

   db = "file:mem1?mode=memory&cache=shared"
   con1 = sqlite3.connect(db, uri=True)
   con2 = sqlite3.connect(db, uri=True)
   with con1:
       con1.execute("CREATE TABLE shared(data)")
       con1.execute("INSERT INTO shared VALUES(28)")
   res = con2.execute("SELECT data FROM shared")
   assert res.fetchone() == (28,)

   con1.close()
   con2.close()

Bạn có thể tìm thêm thông tin về tính năng này, bao gồm danh sách các tham số, trong tài liệu `SQLite URI documentation <SQLite URI documentation_>`_.

.. _SQLite URI documentation: https://www.sqlite.org/uri.html


.. _sqlite3-howto-row-factory:

Cách tạo và sử dụng row factory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Theo mặc định, :mod:`!sqlite3` biểu diễn mỗi hàng dưới dạng :class:`tuple`. Nếu :class:`!tuple` không đáp ứng nhu cầu của bạn, bạn có thể sử dụng class :class:`sqlite3.Row` hoặc một :attr:`~Cursor.row_factory` tùy chỉnh.

Mặc dù :attr:`!row_factory` là một thuộc tính của cả
:class:`Cursor` và :class:`Connection`, bạn nên thiết lập :class:`Connection.row_factory` để tất cả cursor được tạo từ connection đều sử dụng cùng một row factory.

:class:`!Row` cung cấp khả năng truy cập các cột theo chỉ mục và theo tên không phân biệt chữ hoa chữ thường, với mức tiêu tốn bộ nhớ và ảnh hưởng hiệu năng tối thiểu so với :class:`!tuple`. Để sử dụng :class:`!Row` làm row factory, hãy gán nó cho thuộc tính :attr:`!row_factory`:

.. doctest::

   >>> con = sqlite3.connect(":memory:")
   >>> con.row_factory = sqlite3.Row

Các truy vấn giờ đây trả về các đối tượng :class:`!Row`:

.. doctest::

   >>> res = con.execute("SELECT 'Earth' AS name, 6378 AS radius")
   >>> row = res.fetchone()
   >>> row.keys()
   ['name', 'radius']
   >>> row[0]         # Truy cập theo chỉ mục.
   'Earth'
   >>> row["name"]    # Truy cập theo tên.
   'Earth'
   >>> row["RADIUS"]  # Tên cột không phân biệt chữ hoa chữ thường.
   6378
   >>> con.close()

.. note::

    Mệnh đề ``FROM`` có thể được bỏ qua trong câu lệnh ``SELECT``, như trong ví dụ trên. Trong những trường hợp này, SQLite trả về một hàng duy nhất với các cột được xác định bởi các biểu thức, chẳng hạn như các giá trị literal, cùng với các bí danh đã cho ``expr AS alias``.

Bạn có thể tạo một :attr:`~Cursor.row_factory` tùy chỉnh để trả về mỗi hàng dưới dạng :class:`dict`, trong đó tên cột được ánh xạ tới các giá trị:

.. testcode::

   def dict_factory(cursor, row):
       fields = [column[0] for column in cursor.description]
       return {key: value for key, value in zip(fields, row)}

Khi sử dụng nó, các truy vấn giờ đây trả về một :class:`!dict` thay vì một :class:`!tuple`:

.. doctest::

   >>> con = sqlite3.connect(":memory:")
   >>> con.row_factory = dict_factory
   >>> for row in con.execute("SELECT 1 AS a, 2 AS b"):
   ...     print(row)
   {'a': 1, 'b': 2}
   >>> con.close()

Row factory sau đây trả về một :term:`named tuple`:

.. testcode::

   from collections import namedtuple

   def namedtuple_factory(cursor, row):
       fields = [column[0] for column in cursor.description]
       cls = namedtuple("Row", fields)
       return cls._make(row)

Có thể sử dụng :func:`!namedtuple_factory` như sau:

.. doctest::

   >>> con = sqlite3.connect(":memory:")
   >>> con.row_factory = namedtuple_factory
   >>> cur = con.execute("SELECT 1 AS a, 2 AS b")
   >>> row = cur.fetchone()
   >>> row
   Row(a=1, b=2)
   >>> row[0]  # Truy cập theo chỉ mục.
   1
   >>> row.b   # Truy cập thuộc tính.
   2
   >>> con.close()

Sau một số điều chỉnh, công thức trên có thể được điều chỉnh để sử dụng một
:class:`~dataclasses.dataclass`, hoặc bất kỳ lớp tùy chỉnh nào khác, thay vì một :class:`~collections.namedtuple`.


.. _sqlite3-howto-encoding:

Cách xử lý mã hóa văn bản không phải UTF-8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Theo mặc định, :mod:`!sqlite3` sử dụng :class:`str` để điều chỉnh các giá trị SQLite có kiểu dữ liệu ``TEXT``. Cách này hoạt động tốt với văn bản được mã hóa UTF-8, nhưng có thể không thành công với các mã hóa khác và UTF-8 không hợp lệ. Bạn có thể sử dụng một :attr:`~Connection.text_factory` tùy chỉnh để xử lý những trường hợp như vậy.

Do `kiểu dữ liệu linh hoạt <flexible typing_>`_ của SQLite, không hiếm khi gặp các cột bảng có kiểu dữ liệu ``TEXT`` chứa mã hóa không phải UTF-8, hoặc thậm chí dữ liệu tùy ý. Để minh họa, hãy giả sử chúng ta có một cơ sở dữ liệu chứa văn bản được mã hóa bằng ISO-8859-2 (Latin-2), chẳng hạn như một bảng các mục từ điển Séc-Anh. Giả sử hiện tại chúng ta có một thực thể :class:`Connection` :py:data:`!con` được kết nối với cơ sở dữ liệu này, chúng ta có thể giải mã văn bản được mã hóa Latin-2 bằng :attr:`~Connection.text_factory` này:

.. testcode::

   con.text_factory = lambda data: str(data, encoding="latin2")

Đối với UTF-8 không hợp lệ hoặc dữ liệu tùy ý được lưu trong các cột bảng ``TEXT``, bạn có thể sử dụng kỹ thuật sau đây, được lấy từ :ref:`unicode-howto`:

.. testcode::

   con.text_factory = lambda data: str(data, errors="surrogateescape")

.. note::

   API của module :mod:`!sqlite3` không hỗ trợ các chuỗi chứa surrogate.

.. seealso::

   :ref:`unicode-howto`


.. _sqlite3-explanation:

Giải thích
----------

.. _sqlite3-transaction-control:
.. _sqlite3-controlling-transactions:

Kiểm soát giao dịch
^^^^^^^^^^^^^^^^^^^

:mod:`!sqlite3` cung cấp nhiều phương thức để kiểm soát việc các giao dịch cơ sở dữ liệu có được mở và đóng hay không, thời điểm mở và đóng, cũng như cách thức thực hiện.
:ref:`sqlite3-transaction-control-autocommit` được khuyến nghị, còn :ref:`sqlite3-transaction-control-isolation-level` vẫn giữ nguyên hành vi trước Python 3.12.

.. _sqlite3-transaction-control-autocommit:

Kiểm soát giao dịch thông qua thuộc tính ``autocommit``
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

Cách được khuyến nghị để kiểm soát hành vi giao dịch là thông qua thuộc tính :attr:`Connection.autocommit`, thuộc tính này nên được thiết lập bằng tham số *autocommit* của :func:`connect`.

Nên đặt *autocommit* thành ``False``, điều này ngụ ý cơ chế kiểm soát giao dịch tuân thủ :pep:`249`. Điều này có nghĩa là:

* :mod:`!sqlite3` đảm bảo rằng luôn có một giao dịch đang mở, vì vậy :func:`connect`, :meth:`Connection.commit` và :meth:`Connection.rollback` sẽ ngầm mở một giao dịch mới (ngay sau khi đóng giao dịch đang chờ đối với hai thao tác sau).
  :mod:`!sqlite3` sử dụng các câu lệnh ``BEGIN DEFERRED`` khi mở giao dịch.
* Các giao dịch nên được commit một cách tường minh bằng :meth:`!commit`.
* Các giao dịch nên được rollback một cách tường minh bằng :meth:`!rollback`.
* Một thao tác rollback ngầm được thực hiện nếu cơ sở dữ liệu bị
  :meth:`~Connection.close`-ed khi còn các thay đổi chưa được ghi nhận.

Đặt *autocommit* thành ``True`` để bật `chế độ autocommit <autocommit mode_>`_ của SQLite. Trong chế độ này, :meth:`Connection.commit` và :meth:`Connection.rollback` không có tác dụng. Lưu ý rằng chế độ autocommit của SQLite khác với thuộc tính :pep:`249`-compliant :attr:`Connection.autocommit`; sử dụng :attr:`Connection.in_transaction` để truy vấn chế độ autocommit cấp thấp của SQLite.

Đặt *autocommit* thành :data:`LEGACY_TRANSACTION_CONTROL` để giao việc kiểm soát giao dịch cho
thuộc tính :attr:`Connection.isolation_level`. Xem :ref:`sqlite3-transaction-control-isolation-level` để biết thêm thông tin.


.. _sqlite3-transaction-control-isolation-level:

Kiểm soát giao dịch thông qua thuộc tính ``isolation_level``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. note::

   Cách được khuyến nghị để kiểm soát giao dịch là thông qua
   thuộc tính :attr:`~Connection.autocommit`. Xem :ref:`sqlite3-transaction-control-autocommit`.

Nếu :attr:`Connection.autocommit` được đặt thành
:data:`LEGACY_TRANSACTION_CONTROL` (mặc định), hành vi giao dịch được kiểm soát bằng thuộc tính :attr:`Connection.isolation_level`. Nếu không, :attr:`!isolation_level` không có tác dụng.

Nếu thuộc tính kết nối :attr:`~Connection.isolation_level` không phải là ``None``, các giao dịch mới sẽ được mở ngầm trước khi
:meth:`~Cursor.execute` và :meth:`~Cursor.executemany` thực thi các câu lệnh ``INSERT``, ``UPDATE``, ``DELETE`` hoặc ``REPLACE``; với các câu lệnh khác, không thực hiện xử lý giao dịch ngầm. Sử dụng các phương thức :meth:`~Connection.commit` và :meth:`~Connection.rollback` để lần lượt commit và rollback các giao dịch đang chờ xử lý. Bạn có thể chọn `hành vi giao dịch SQLite <SQLite transaction behaviour_>`_ bên dưới — tức là liệu và loại câu lệnh ``BEGIN`` nào mà :mod:`!sqlite3` thực thi ngầm – thông qua thuộc tính :attr:`~Connection.isolation_level`.

Nếu :attr:`~Connection.isolation_level` được đặt thành ``None``, hoàn toàn không có giao dịch nào được mở ngầm. Điều này đặt thư viện SQLite bên dưới ở `chế độ autocommit <autocommit mode_>`_, nhưng cũng cho phép người dùng tự xử lý giao dịch bằng các câu lệnh SQL tường minh. Có thể truy vấn chế độ autocommit của thư viện SQLite bên dưới bằng
thuộc tính :attr:`~Connection.in_transaction`.

Phương thức :meth:`~Cursor.executescript` ngầm commit mọi giao dịch đang chờ xử lý trước khi thực thi tập lệnh SQL đã cho, bất kể giá trị của :attr:`~Connection.isolation_level`.

.. versionchanged:: 3.6
   :mod:`!sqlite3` used to implicitly commit an open transaction before DDL
   các câu lệnh. Điều này không còn đúng nữa.

.. versionchanged:: 3.12
   Cách được khuyến nghị để kiểm soát transaction hiện nay là thông qua
   :attr:`~Connection.autocommit` thuộc tính.

.. _autocommit mode:
   https://www.sqlite.org/lang_transaction.html#implicit_versus_explicit_transactions

.. _SQLite transaction behaviour:
   https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions

.. testcleanup::

   import os
   os.remove("backup.db")
   os.remove("dump.sql")
   os.remove("example.db")
   os.remove("tutorial.db")

.. _`SQLite`: https://sqlite.org/
.. _`SQLite database existing only in memory`: https://sqlite.org/inmemorydb.html
.. _`threading mode`: https://sqlite.org/threadsafe.html
.. _`deterministic`: https://sqlite.org/deterministic.html
.. _`SQLite API`: https://sqlite.org/rescode.html
