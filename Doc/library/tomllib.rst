:mod:`!tomllib` --- Phân tích tệp TOML
======================================

.. module:: tomllib
   :synopsis: Phân tích tệp TOML.

.. versionadded:: 3.11

.. moduleauthor:: Taneli Hukkinen
.. sectionauthor:: Taneli Hukkinen

**Mã nguồn:** :source:`Lib/tomllib`

--------------

Mô-đun này cung cấp giao diện để phân tích TOML 1.0.0 (Tom's Obvious Minimal Language, `https://toml.io <https://toml.io/en/>`_). Mô-đun này không hỗ trợ ghi TOML.

.. warning::

   Hãy thận trọng khi phân tích dữ liệu từ các nguồn không đáng tin cậy. Một chuỗi TOML độc hại có thể khiến bộ giải mã tiêu tốn đáng kể tài nguyên CPU và bộ nhớ. Bạn nên giới hạn kích thước dữ liệu cần phân tích.

.. seealso::

    :pypi:`Tomli-W package <tomli-w>` là một trình ghi TOML có thể được sử dụng cùng với mô-đun này, cung cấp một API ghi quen thuộc với người dùng thư viện chuẩn
    các mô-đun :mod:`marshal` và :mod:`pickle`.

.. seealso::

    :pypi:`TOML Kit package <tomlkit>` là một thư viện TOML bảo toàn kiểu định dạng, có cả khả năng đọc và ghi. Đây là thư viện được khuyến nghị thay thế cho mô-đun này khi chỉnh sửa các tệp TOML đã tồn tại.


Mô-đun này định nghĩa các hàm sau:

.. function:: load(fp, /, *, parse_float=float)

   Đọc một tệp TOML. Đối số đầu tiên phải là một đối tượng tệp nhị phân có thể đọc được. Trả về một :class:`dict`. Chuyển đổi các kiểu TOML sang Python bằng
   :ref:`bảng chuyển đổi <toml-to-py-table>` này.

   *parse_float* sẽ được gọi với chuỗi của mỗi số thực TOML cần giải mã. Theo mặc định, hàm này tương đương với ``float(num_str)``. Có thể dùng cách này để sử dụng một kiểu dữ liệu hoặc trình phân tích cú pháp khác cho các số thực TOML (ví dụ: :class:`decimal.Decimal`). Hàm gọi được không được trả về một
   :class:`dict` hoặc một :class:`list`, nếu không sẽ phát sinh :exc:`ValueError`.

   :exc:`TOMLDecodeError` sẽ được phát sinh khi tài liệu TOML không hợp lệ.


.. function:: loads(s, /, *, parse_float=float)

   Tải TOML từ một đối tượng :class:`str`. Trả về một :class:`dict`. Chuyển đổi các kiểu TOML sang Python bằng :ref:`bảng chuyển đổi <toml-to-py-table>` này. Đối số *parse_float* có cùng ý nghĩa như trong :func:`load`.

   :exc:`TOMLDecodeError` sẽ được phát sinh khi tài liệu TOML không hợp lệ.


Các ngoại lệ sau đây khả dụng:

.. exception:: TOMLDecodeError(msg, doc, pos)

   Lớp con của :exc:`ValueError` với các thuộc tính bổ sung sau:

   .. attribute:: msg

      Thông báo lỗi chưa được định dạng.

   .. attribute:: doc

      Tài liệu TOML đang được phân tích cú pháp.

   .. attribute:: pos

      Chỉ mục của *doc* tại đó quá trình phân tích cú pháp thất bại.

   .. attribute:: lineno

      Dòng tương ứng với *pos*.

   .. attribute:: colno

      Cột tương ứng với *pos*.

   .. versionchanged:: 3.14
      Đã thêm các tham số *msg*, *doc* và *pos*. Đã thêm các thuộc tính :attr:`msg`, :attr:`doc`, :attr:`pos`, :attr:`lineno` và :attr:`colno`.

   .. deprecated:: 3.14
      Việc truyền các đối số positional tùy ý đã không còn được khuyến nghị.


Ví dụ
-----

Phân tích tệp TOML::

    import tomllib

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

Phân tích chuỗi TOML::

    import tomllib

    toml_str = """
    python-version = "3.11.0"
    python-implementation = "CPython"
    """

    data = tomllib.loads(toml_str)


Bảng chuyển đổi
---------------

.. _toml-to-py-table:

+---------------------+--------------------------------------------------------------------------------------+
| TOML                | Python                                                                               |
+=====================+======================================================================================+
| tài liệu TOML       | dict                                                                                 |
+---------------------+--------------------------------------------------------------------------------------+
| chuỗi               | str                                                                                  |
+---------------------+--------------------------------------------------------------------------------------+
| số nguyên           | int                                                                                  |
+---------------------+--------------------------------------------------------------------------------------+
| số thực             | float (có thể cấu hình bằng *parse_float*)                                           |
+---------------------+--------------------------------------------------------------------------------------+
| boolean             | bool                                                                                 |
+---------------------+--------------------------------------------------------------------------------------+
| ngày-giờ có độ lệch | datetime.datetime (``tzinfo`` được đặt thành một instance của ``datetime.timezone``) |
+---------------------+--------------------------------------------------------------------------------------+
| ngày-giờ cục bộ     | datetime.datetime (``tzinfo`` được đặt thành ``None``)                               |
+---------------------+--------------------------------------------------------------------------------------+
| ngày cục bộ         | datetime.date                                                                        |
+---------------------+--------------------------------------------------------------------------------------+
| giờ cục bộ          | datetime.time                                                                        |
+---------------------+--------------------------------------------------------------------------------------+
| mảng                | danh sách                                                                            |
+---------------------+--------------------------------------------------------------------------------------+
| bảng                | dict                                                                                 |
+---------------------+--------------------------------------------------------------------------------------+
| bảng nội tuyến      | dict                                                                                 |
+---------------------+--------------------------------------------------------------------------------------+
| mảng các bảng       | danh sách các dict                                                                   |
+---------------------+--------------------------------------------------------------------------------------+

.. _`https://toml.io`: https://toml.io/en/
