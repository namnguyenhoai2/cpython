:mod:`!plistlib` --- Tạo và phân tích các tệp Apple ``.plist``
==============================================================

.. module:: plistlib
   :synopsis: Tạo và phân tích các tệp plist của Apple.

.. moduleauthor:: Jack Jansen
.. sectionauthor:: Georg Brandl <georg@python.org>
.. (harvested from docstrings in the original file)

**Mã nguồn:** :source:`Lib/plistlib.py`

.. index::
   pair: plist; file
   single: property list

--------------

Mô-đun này cung cấp giao diện để đọc và ghi các tệp "property list" được Apple sử dụng, chủ yếu trên macOS và iOS. Mô-đun này hỗ trợ cả tệp plist nhị phân và XML.

Định dạng tệp property list (``.plist``) là một dạng tuần tự hóa đơn giản, hỗ trợ các kiểu đối tượng cơ bản như dictionary, list, số và chuỗi. Thông thường, đối tượng cấp cao nhất là một dictionary.

Để ghi và phân tích một tệp plist, hãy sử dụng :func:`dump` và
:func:`load` các hàm.

Để làm việc với dữ liệu plist dưới dạng đối tượng byte hoặc chuỗi, hãy sử dụng :func:`dumps` và :func:`loads`.

Các giá trị có thể là chuỗi, số nguyên, số thực, giá trị boolean, tuple, danh sách, từ điển (nhưng chỉ có khóa dạng chuỗi), đối tượng :class:`bytes`, :class:`bytearray` hoặc :class:`datetime.datetime`.

.. versionchanged:: 3.4
   API mới, API cũ không còn được dùng. Đã bổ sung hỗ trợ cho plist ở định dạng nhị phân.

.. versionchanged:: 3.8
   Đã bổ sung hỗ trợ đọc và ghi các token :class:`UID` trong plist nhị phân được NSKeyedArchiver và NSKeyedUnarchiver sử dụng.

.. versionchanged:: 3.9
   API cũ đã bị xóa.

.. seealso::

   `Tài liệu hướng dẫn PList <https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/PropertyLists/>`_
      Tài liệu của Apple về định dạng tệp.


Mô-đun này định nghĩa các hàm sau:

.. function:: load(fp, *, fmt=None, dict_type=dict, aware_datetime=False)

   Đọc tệp plist. *fp* phải là đối tượng tệp có thể đọc và ở dạng nhị phân. Trả về đối tượng gốc đã giải nén (thường là một dictionary).

   *fmt* là định dạng của tệp và các giá trị sau đây là hợp lệ:

   * :data:`None`: Tự động phát hiện định dạng tệp

   * :data:`FMT_XML`: Định dạng tệp XML

   * :data:`FMT_BINARY`: Định dạng plist nhị phân

   *dict_type* là kiểu được dùng cho các dictionary được đọc từ tệp plist.

   Khi *aware_datetime* là true, các trường có kiểu ``datetime.datetime`` sẽ được tạo dưới dạng :ref:`đối tượng aware <datetime-naive-aware>`, với
   :attr:`!tzinfo` dưới dạng :const:`datetime.UTC`.

   Dữ liệu XML cho định dạng :data:`FMT_XML` được phân tích bằng parser Expat từ :mod:`xml.parsers.expat` -- xem tài liệu của nó để biết các ngoại lệ có thể xảy ra với XML không đúng định dạng. Các phần tử không xác định sẽ đơn giản bị parser plist bỏ qua.

   Parser sẽ ném :exc:`InvalidFileException` khi không thể phân tích tệp.

   .. versionadded:: 3.4

   .. versionchanged:: 3.13
      Đã thêm tham số chỉ nhận theo từ khóa *aware_datetime*.


.. function:: loads(data, *, fmt=None, dict_type=dict, aware_datetime=False)

   Nạp một plist từ đối tượng bytes hoặc chuỗi. Xem :func:`load` để biết giải thích về các đối số từ khóa.

   .. versionadded:: 3.4

   .. versionchanged:: 3.13
      *data* có thể là một chuỗi khi *fmt* bằng :data:`FMT_XML`.

.. function:: dump(value, fp, *, fmt=FMT_XML, sort_keys=True, skipkeys=False, aware_datetime=False)

   Ghi *value* vào một tệp plist. *fp* phải là một đối tượng tệp nhị phân có thể ghi.

   Đối số *fmt* chỉ định định dạng của tệp plist và có thể nhận một trong các giá trị sau:

   * :data:`FMT_XML`: Tệp plist có định dạng XML

   * :data:`FMT_BINARY`: Tệp plist có định dạng nhị phân

   Khi *sort_keys* là true (mặc định), các key của dictionary sẽ được ghi vào plist theo thứ tự đã sắp xếp; nếu không, chúng sẽ được ghi theo thứ tự lặp của dictionary.

   Khi *skipkeys* là false (mặc định), hàm sẽ phát sinh :exc:`TypeError` nếu một key của dictionary không phải là chuỗi; nếu không, các key như vậy sẽ bị bỏ qua.

   Khi *aware_datetime* là true và bất kỳ trường nào có kiểu ``datetime.datetime`` được đặt thành một đối tượng :ref:`aware object <datetime-naive-aware>`, trường đó sẽ được chuyển đổi sang múi giờ UTC trước khi ghi.

   Sẽ phát sinh :exc:`TypeError` nếu đối tượng thuộc kiểu không được hỗ trợ hoặc là một container chứa các đối tượng thuộc những kiểu không được hỗ trợ.

   Sẽ phát sinh :exc:`OverflowError` đối với các giá trị số nguyên không thể biểu diễn trong tệp plist (dạng nhị phân).

   .. versionadded:: 3.4

   .. versionchanged:: 3.13
      Đã thêm tham số chỉ nhận theo từ khóa *aware_datetime*.


.. function:: dumps(value, *, fmt=FMT_XML, sort_keys=True, skipkeys=False, aware_datetime=False)

   Trả về *value* dưới dạng một đối tượng bytes được định dạng plist. Xem tài liệu về :func:`dump` để biết giải thích về các đối số từ khóa của hàm này.

   .. versionadded:: 3.4


Các lớp sau đây hiện có:

.. class:: UID(data)

   Bọc một :class:`int`. Được dùng khi đọc hoặc ghi dữ liệu được mã hóa bằng NSKeyedArchiver, trong đó chứa UID (xem hướng dẫn sử dụng PList).

   .. attribute:: data

      Giá trị Int của UID. Giá trị này phải nằm trong phạm vi ``0 <= data < 2**64``.

   .. versionadded:: 3.8


Các hằng số sau đây khả dụng:

.. data:: FMT_XML

   Định dạng XML cho các tệp plist.

   .. versionadded:: 3.4


.. data:: FMT_BINARY

   Định dạng nhị phân cho các tệp plist

   .. versionadded:: 3.4


Mô-đun định nghĩa các ngoại lệ sau:

.. exception:: InvalidFileException

   Được phát sinh khi không thể phân tích cú pháp một tệp.

   .. versionadded:: 3.4


Ví dụ
-----

Tạo plist::

    import datetime as dt
    import plistlib

    pl = dict(
        aString = "Doodah",
        aList = ["A", "B", 12, 32.1, [1, 2, 3]],
        aFloat = 0.1,
        anInt = 728,
        aDict = dict(
            anotherString = "<hello & hi there!>",
            aThirdString = "M\xe4ssig, Ma\xdf",
            aTrueValue = True,
            aFalseValue = False,
        ),
        someData = b"<binary gunk>",
        someMoreData = b"<lots of binary gunk>" * 10,
        aDate = dt.datetime.now()
    )
    print(plistlib.dumps(pl).decode())

Phân tích tệp plist::

    import plistlib

    plist = b"""<plist version="1.0">
    <dict>
        <key>foo</key>
        <string>bar</string>
    </dict>
    </plist>"""
    pl = plistlib.loads(plist)
    print(pl["foo"])

.. _`PList manual page`: https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/PropertyLists/
