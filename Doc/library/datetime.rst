:mod:`!datetime` --- Các kiểu ngày và giờ cơ bản
================================================

.. module:: datetime
   :synopsis: Các kiểu ngày và giờ cơ bản.

.. moduleauthor:: Tim Peters <tim@zope.com>
.. sectionauthor:: Tim Peters <tim@zope.com>
.. sectionauthor:: A.M. Kuchling <amk@amk.ca>

**Mã nguồn:** :source:`Lib/datetime.py`

--------------

Mô-đun :mod:`!datetime` cung cấp các lớp để thao tác với ngày và giờ.

Mặc dù hỗ trợ phép tính số học trên ngày và giờ, trọng tâm của việc triển khai là trích xuất thuộc tính hiệu quả để định dạng và thao tác đầu ra.

.. tip::

    Chuyển đến :ref:`các mã định dạng <format-codes>`.

.. seealso::

   Mô-đun :mod:`calendar`
      Các hàm chung liên quan đến lịch.

   Mô-đun :mod:`time`
      Truy cập và chuyển đổi thời gian.

   Mô-đun :mod:`zoneinfo`
      Các múi giờ cụ thể đại diện cho cơ sở dữ liệu múi giờ IANA.

   Gói `dateutil <https://dateutil.readthedocs.io/en/stable/>`_
      Thư viện bên thứ ba với khả năng hỗ trợ mở rộng cho múi giờ và phân tích cú pháp.

   Gói :pypi:`DateType`
      Thư viện bên thứ ba giới thiệu các kiểu tĩnh riêng biệt để, chẳng hạn, cho phép :term:`các trình kiểm tra kiểu tĩnh <static type checker>` phân biệt giữa các datetime naive và aware.


.. _datetime-naive-aware:

Các đối tượng aware và naive
----------------------------

Các đối tượng ngày và giờ có thể được phân loại là "aware" hoặc "naive" tùy thuộc vào việc chúng có bao gồm thông tin múi giờ hay không.

Với đủ kiến thức về các điều chỉnh thuật toán và chính trị áp dụng, chẳng hạn như thông tin về múi giờ và giờ mùa hè, một đối tượng **aware** có thể xác định vị trí của nó tương quan với các đối tượng aware khác. Một đối tượng aware biểu diễn một thời điểm cụ thể không thể bị diễn giải theo nhiều cách. [#]_

Một đối tượng **naive** không chứa đủ thông tin để xác định rõ ràng vị trí của nó tương quan với các đối tượng ngày/giờ khác. Việc một đối tượng naive biểu diễn Giờ Phối hợp Quốc tế (UTC), giờ địa phương hay giờ ở một múi giờ khác hoàn toàn tùy thuộc vào chương trình, cũng giống như việc một số cụ thể biểu diễn mét, dặm hay khối lượng là tùy thuộc vào chương trình. Các đối tượng naive dễ hiểu và dễ làm việc, nhưng phải đánh đổi bằng việc bỏ qua một số khía cạnh của thực tế.

Đối với các ứng dụng yêu cầu các đối tượng aware, các đối tượng :class:`.datetime` và :class:`.time` có một thuộc tính thông tin múi giờ tùy chọn, :attr:`!tzinfo`, có thể được đặt thành một instance của một lớp con của lớp trừu tượng :class:`!tzinfo`. Các đối tượng :class:`tzinfo` này lưu giữ thông tin về độ lệch so với giờ UTC, tên múi giờ và việc giờ mùa hè có đang được áp dụng hay không.

Chỉ có một lớp :class:`tzinfo` cụ thể, là lớp :class:`timezone`, được cung cấp bởi mô-đun :mod:`!datetime`. Lớp :class:`!timezone` có thể biểu diễn các múi giờ đơn giản với độ lệch cố định so với UTC, chẳng hạn như chính UTC hoặc các múi giờ EST và EDT của Bắc Mỹ. Việc hỗ trợ các múi giờ ở mức độ chi tiết hơn tùy thuộc vào ứng dụng. Các quy tắc điều chỉnh thời gian trên toàn thế giới mang tính chính trị nhiều hơn là hợp lý, thường xuyên thay đổi và không có tiêu chuẩn nào phù hợp với mọi ứng dụng ngoài UTC.


Hằng số
-------

Mô-đun :mod:`!datetime` xuất các hằng số sau:

.. data:: MINYEAR

   Số năm nhỏ nhất được phép trong đối tượng :class:`date` hoặc :class:`.datetime`.
   :const:`MINYEAR` là 1.


.. data:: MAXYEAR

   Số năm lớn nhất được phép trong đối tượng :class:`date` hoặc :class:`.datetime`.
   :const:`MAXYEAR` là 9999.


.. data:: UTC

   Bí danh cho singleton múi giờ UTC :attr:`datetime.timezone.utc`.

   .. versionadded:: 3.11


Các kiểu khả dụng
-----------------

.. class:: date
   :noindex:

   Một date lý tưởng không có thông tin múi giờ (naive), giả định rằng lịch Gregorian hiện tại luôn đã và sẽ luôn được áp dụng. Các thuộc tính: :attr:`year`, :attr:`month`, và
   :attr:`day`.


.. class:: time
   :noindex:

   Một time lý tưởng, không phụ thuộc vào bất kỳ ngày cụ thể nào, giả định rằng mỗi ngày luôn có chính xác 24\*60\*60 giây. (Ở đây không có khái niệm về "giây nhuận".) Các thuộc tính: :attr:`hour`, :attr:`minute`, :attr:`second`, :attr:`microsecond`, và :attr:`.tzinfo`.


.. class:: datetime
   :noindex:

   Sự kết hợp giữa một date và một time. Các thuộc tính: :attr:`year`, :attr:`month`,
   :attr:`day`, :attr:`hour`, :attr:`minute`, :attr:`second`, :attr:`microsecond`, và :attr:`.tzinfo`.


.. class:: timedelta
   :noindex:

   Một khoảng thời gian biểu thị sự chênh lệch giữa hai instance :class:`.datetime` hoặc :class:`date`, với độ phân giải đến microsecond.


.. class:: tzinfo
   :noindex:

   Một lớp cơ sở trừu tượng dành cho các đối tượng chứa thông tin múi giờ. Các đối tượng này được sử dụng bởi
   :class:`.datetime` và :class:`.time` để cung cấp khái niệm có thể tùy chỉnh về việc điều chỉnh thời gian (ví dụ: để tính đến múi giờ và/hoặc giờ mùa hè).


.. class:: timezone
   :noindex:

   Một lớp triển khai lớp cơ sở trừu tượng :class:`tzinfo` dưới dạng độ lệch cố định so với UTC.

   .. versionadded:: 3.2


Các đối tượng thuộc những kiểu này là bất biến.

Quan hệ kế thừa:

.. figure:: datetime-inheritance.svg
   :class: invert-in-dark-mode
   :align: center
   :alt: timedelta, tzinfo, time và date kế thừa từ object; timezone kế thừa từ tzinfo; còn datetime kế thừa từ date.


Các thuộc tính chung
^^^^^^^^^^^^^^^^^^^^

Các kiểu :class:`date`, :class:`.datetime`, :class:`.time` và :class:`timezone` có những đặc điểm chung sau:

- Các đối tượng thuộc những kiểu này là bất biến.
- Các đối tượng thuộc những kiểu này là :term:`hashable`, nghĩa là chúng có thể được dùng làm khóa từ điển.
- Các đối tượng thuộc những kiểu này hỗ trợ pickling hiệu quả thông qua mô-đun :mod:`pickle`.


Xác định một đối tượng là aware hay naive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các đối tượng thuộc kiểu :class:`date` luôn là naive.

Một đối tượng thuộc kiểu :class:`.time` hoặc :class:`.datetime` có thể là aware hoặc naive.

Một đối tượng :class:`.datetime` ``d`` là aware nếu cả hai điều kiện sau đều đúng:

1. ``d.tzinfo`` không phải ``None``
2. ``d.tzinfo.utcoffset(d)`` không trả về ``None``

Nếu không, ``d`` là naive.

Một đối tượng :class:`.time` ``t`` là aware nếu cả hai điều kiện sau đều đúng:

1. ``t.tzinfo`` không phải ``None``
2. ``t.tzinfo.utcoffset(None)`` không trả về ``None``.

Nếu không, ``t`` là naive.

Sự phân biệt giữa aware và naive không áp dụng cho các đối tượng :class:`timedelta`.


.. _datetime-timedelta:

Các đối tượng :class:`!timedelta`
---------------------------------

Một đối tượng :class:`timedelta` biểu diễn một khoảng thời gian, tức hiệu giữa hai
đối tượng :class:`.datetime` hoặc :class:`date`.

.. class:: timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

   Tất cả đối số đều là tùy chọn và mặc định là 0. Đối số có thể là số nguyên hoặc số thực, đồng thời có thể dương hoặc âm.

   Chỉ *days*, *seconds* và *microseconds* được lưu trữ nội bộ. Các đối số được chuyển đổi sang những đơn vị đó:

   * Một mili giây được chuyển đổi thành 1000 micro giây.
   * Một phút được chuyển đổi thành 60 giây.
   * Một giờ được chuyển đổi thành 3600 giây.
   * Một tuần được chuyển đổi thành 7 ngày.

   sau đó ngày, giây và micro giây được chuẩn hóa để biểu diễn là duy nhất, với

   * ``0 <= microseconds < 1000000``
   * ``0 <= seconds < 3600*24`` (số giây trong một ngày)
   * ``-999999999 <= days <= 999999999``

   Ví dụ sau minh họa cách mọi đối số ngoài *days*, *seconds* và *microseconds* được "gộp" và chuẩn hóa thành ba thuộc tính kết quả đó::

       >>> import datetime as dt
       >>> delta = dt.timedelta(
       ...     days=50,
       ...     seconds=27,
       ...     microseconds=10,
       ...     milliseconds=29000,
       ...     minutes=5,
       ...     hours=8,
       ...     weeks=2
       ... )
       >>> # Chỉ còn ngày, giây và microsecond
       >>> delta
       datetime.timedelta(days=64, seconds=29156, microseconds=10)

   .. tip::
      ``import datetime as dt`` thay vì ``import datetime`` hoặc ``from datetime import datetime`` để tránh nhầm lẫn giữa module và class. Xem `How I Import Python’s datetime Module <https://adamj.eu/tech/2019/09/12/how-i-import-pythons-datetime-module/>`__.

   Nếu bất kỳ đối số nào là số thực và có microsecond lẻ, phần microsecond lẻ còn lại từ tất cả các đối số sẽ được gộp lại, rồi tổng của chúng được làm tròn đến microsecond gần nhất, sử dụng quy tắc phân định round-half-to-even. Nếu không có đối số nào là số thực, quá trình chuyển đổi và chuẩn hóa là chính xác (không mất thông tin).

   Nếu giá trị ngày đã chuẩn hóa nằm ngoài phạm vi được chỉ định,
   :exc:`OverflowError` sẽ được raised.

   Lưu ý rằng việc chuẩn hóa các giá trị âm lúc đầu có thể gây bất ngờ. Ví dụ::

      >>> import datetime as dt
      >>> d = dt.timedelta(microseconds=-1)
      >>> (d.days, d.seconds, d.microseconds)
      (-1, 86399, 999999)

   Vì biểu diễn chuỗi của các đối tượng :class:`!timedelta` có thể gây nhầm lẫn, hãy sử dụng công thức sau để tạo ra định dạng dễ đọc hơn:

   .. code-block:: pycon

      >>> def pretty_timedelta(td):
      ...     if td.days >= 0:
      ...         return str(td)
      ...     return f'-({-td!s})'
      ...
      >>> d = timedelta(hours=-1)
      >>> str(d)  # không thân thiện với con người
      '-1 day, 23:00:00'
      >>> pretty_timedelta(d)
      '-(1:00:00)'


Các thuộc tính của lớp:

.. attribute:: timedelta.min

   Đối tượng :class:`timedelta` âm nhất, ``timedelta(-999999999)``.


.. attribute:: timedelta.max

   Đối tượng :class:`timedelta` dương nhất, ``timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)``.


.. attribute:: timedelta.resolution

   Hiệu nhỏ nhất có thể giữa các đối tượng :class:`timedelta` không bằng nhau, ``timedelta(microseconds=1)``.


Lưu ý rằng, do quá trình chuẩn hóa, ``timedelta.max`` lớn hơn ``-timedelta.min``. ``-timedelta.max`` không thể biểu diễn dưới dạng đối tượng :class:`timedelta`.


Các thuộc tính của instance (chỉ đọc):

.. attribute:: timedelta.days

   Trong khoảng từ -999.999.999 đến 999.999.999, bao gồm cả hai đầu mút.


.. attribute:: timedelta.seconds

   Trong khoảng từ 0 đến 86.399, bao gồm cả hai đầu mút.

   .. caution::

      Một lỗi khá phổ biến là code vô tình sử dụng thuộc tính này trong khi thực tế lại nhằm lấy một giá trị :meth:`~timedelta.total_seconds`:

      .. doctest::

         >>> import datetime as dt
         >>> duration = dt.timedelta(seconds=11235813)
         >>> duration.days, duration.seconds
         (130, 3813)
         >>> duration.total_seconds()
         11235813.0


.. attribute:: timedelta.microseconds

   Trong khoảng từ 0 đến 999.999, bao gồm cả hai đầu mút.


Các phép toán được hỗ trợ:

+--------------------------------+-----------------------------------------------+
| Operation                      | Result                                        |
+================================+===============================================+
| ``t1 = t2 + t3``               | Sum of ``t2`` and ``t3``.                     |
|                                | Afterwards ``t1 - t2 == t3`` and              |
|                                | ``t1 - t3 == t2`` are true. (1)               |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 - t3``               | Difference of ``t2``  and ``t3``. Afterwards  |
|                                | ``t1 == t2 - t3`` and ``t2 == t1 + t3`` are   |
|                                | true. (1)(6)                                  |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 * i or t1 = i * t2`` | Delta multiplied by an integer.               |
|                                | Afterwards ``t1 // i == t2`` is true,         |
|                                | provided ``i != 0``.                          |
+--------------------------------+-----------------------------------------------+
|                                | In general, ``t1  * i == t1 * (i-1) + t1``    |
|                                | is true. (1)                                  |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 * f or t1 = f * t2`` | Delta multiplied by a float. The result is    |
|                                | rounded to the nearest multiple of            |
|                                | timedelta.resolution using round-half-to-even.|
+--------------------------------+-----------------------------------------------+
| ``f = t2 / t3``                | Division (3) of overall duration ``t2`` by    |
|                                | interval unit ``t3``. Returns a :class:`float`|
|                                | object.                                       |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 / f or t1 = t2 / i`` | Delta divided by a float or an int. The result|
|                                | is rounded to the nearest multiple of         |
|                                | timedelta.resolution using round-half-to-even.|
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 // i`` or            | The floor is computed and the remainder (if   |
| ``t1 = t2 // t3``              | any) is thrown away. In the second case, an   |
|                                | integer is returned. (3)                      |
+--------------------------------+-----------------------------------------------+
| ``t1 = t2 % t3``               | The remainder is computed as a                |
|                                | :class:`timedelta` object. (3)                |
+--------------------------------+-----------------------------------------------+
| ``q, r = divmod(t1, t2)``      | Computes the quotient and the remainder:      |
|                                | ``q = t1 // t2`` (3) and ``r = t1 % t2``.     |
|                                | ``q`` is an integer and ``r`` is a            |
|                                | :class:`timedelta` object.                    |
+--------------------------------+-----------------------------------------------+
| ``+t1``                        | Returns a :class:`timedelta` object with the  |
|                                | same value. (2)                               |
+--------------------------------+-----------------------------------------------+
| ``-t1``                        | Equivalent to ``timedelta(-t1.days,           |
|                                | -t1.seconds, -t1.microseconds)``,             |
|                                | and to ``t1 * -1``. (1)(4)                    |
+--------------------------------+-----------------------------------------------+
| ``abs(t)``                     | Equivalent to ``+t`` when ``t.days >= 0``,    |
|                                | and to ``-t`` when ``t.days < 0``. (2)        |
+--------------------------------+-----------------------------------------------+
| ``str(t)``                     | Returns a string in the form                  |
|                                | ``[D day[s], ][H]H:MM:SS[.UUUUUU]``, where D  |
|                                | is negative for negative ``t``. (5)           |
+--------------------------------+-----------------------------------------------+
| ``repr(t)``                    | Returns a string representation of the        |
|                                | :class:`timedelta` object as a constructor    |
|                                | call with canonical attribute values.         |
+--------------------------------+-----------------------------------------------+

Lưu ý:

(1)
   Giá trị này chính xác nhưng có thể gây tràn số.

(2)
   Kết quả này chính xác và không thể bị tràn.

(3)
   Phép chia cho số không sẽ phát sinh :exc:`ZeroDivisionError`.

(4)
   ``-timedelta.max`` không thể biểu diễn dưới dạng đối tượng :class:`timedelta`.

(5)
   Biểu diễn chuỗi của các đối tượng :class:`timedelta` được chuẩn hóa tương tự như biểu diễn nội bộ của chúng. Điều này dẫn đến một số kết quả khá bất thường đối với các timedelta âm. Ví dụ::

      >>> timedelta(hours=-5)
      datetime.timedelta(days=-1, seconds=68400)
      >>> print(_)
      -1 day, 19:00:00

(6)
   Biểu thức ``t2 - t3`` sẽ luôn bằng biểu thức ``t2 + (-t3)``, ngoại trừ khi t3 bằng ``timedelta.max``; trong trường hợp đó, biểu thức đầu tiên sẽ tạo ra một kết quả, còn biểu thức sau sẽ bị tràn.

Ngoài các phép toán được liệt kê ở trên, các đối tượng :class:`timedelta` còn hỗ trợ một số phép cộng và phép trừ với các đối tượng :class:`date` và :class:`.datetime` (xem bên dưới).

.. versionchanged:: 3.2
   Phép chia lấy phần nguyên và phép chia thực của một đối tượng :class:`timedelta` cho một đối tượng khác
   Các phép toán với đối tượng :class:`!timedelta` hiện đã được hỗ trợ, cũng như các phép toán lấy phần dư và hàm :func:`divmod`. Phép chia thực và phép nhân một
   đối tượng :class:`!timedelta` với một đối tượng :class:`float` hiện đã được hỗ trợ.

Các đối tượng :class:`timedelta` hỗ trợ so sánh bằng và so sánh thứ tự.

Trong các ngữ cảnh Boolean, một đối tượng :class:`timedelta` được xem là đúng khi và chỉ khi nó không bằng ``timedelta(0)``.

Các phương thức của instance:

.. method:: timedelta.total_seconds()

   Trả về tổng số giây có trong khoảng thời gian. Tương đương với ``td / timedelta(seconds=1)``. Đối với các đơn vị khoảng thời gian khác giây, hãy sử dụng trực tiếp dạng phép chia (ví dụ: ``td / timedelta(microseconds=1)``).

   Lưu ý rằng đối với các khoảng thời gian rất lớn (lớn hơn 270 năm trên hầu hết các nền tảng), phương thức này sẽ mất độ chính xác đến microsecond.

   .. versionadded:: 3.2


Ví dụ sử dụng: :class:`!timedelta`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một ví dụ bổ sung về việc chuẩn hóa::

    >>> # Các thành phần của another_year cộng lại chính xác bằng 365 ngày
    >>> import datetime as dt
    >>> year = dt.timedelta(days=365)
    >>> another_year = dt.timedelta(weeks=40, days=84, hours=23,
    ...                             minutes=50, seconds=600)
    >>> year == another_year
    True
    >>> year.total_seconds()
    31536000.0

Ví dụ về phép tính số học với :class:`timedelta`::

    >>> import datetime as dt
    >>> year = dt.timedelta(days=365)
    >>> ten_years = 10 * year
    >>> ten_years
    datetime.timedelta(days=3650)
    >>> ten_years.days // 365
    10
    >>> nine_years = ten_years - year
    >>> nine_years
    datetime.timedelta(days=3285)
    >>> three_years = nine_years // 3
    >>> three_years, three_years.days // 365
    (datetime.timedelta(days=1095), 3)


.. _datetime-date:

Các đối tượng :class:`!date`
----------------------------

Đối tượng :class:`date` biểu diễn một ngày (năm, tháng và ngày) trong một lịch lý tưởng hóa, tức lịch Gregory hiện tại được mở rộng vô hạn theo cả hai hướng.

Ngày 1 tháng 1 của năm 1 được gọi là ngày số 1, ngày 2 tháng 1 của năm 1 được gọi là ngày số 2, và cứ tiếp tục như vậy. [#]_

.. class:: date(year, month, day)

   Tất cả các đối số đều bắt buộc. Các đối số phải là số nguyên, trong các phạm vi sau:

   * ``MINYEAR <= year <= MAXYEAR``
   * ``1 <= month <= 12``
   * ``1 <= day <= number of days in the given month and year``

   Nếu cung cấp một đối số nằm ngoài các phạm vi đó, :exc:`ValueError` sẽ được phát sinh.


Các hàm khởi tạo khác, tất cả các phương thức của lớp:

.. classmethod:: date.today()

   Trả về ngày hiện tại theo giờ địa phương.

   Điều này tương đương với ``date.fromtimestamp(time.time())``.


.. classmethod:: date.fromtimestamp(timestamp)

   Trả về ngày địa phương tương ứng với *timestamp* POSIX, chẳng hạn như giá trị được trả về bởi :func:`time.time`.

   Lệnh này có thể phát sinh :exc:`OverflowError` nếu timestamp nằm ngoài phạm vi giá trị được hàm :c:func:`localtime` C của nền tảng hỗ trợ, và :exc:`OSError` khi :c:func:`localtime` không thành công. Thông thường, phạm vi này bị giới hạn trong các năm từ 1970 đến 2038. Lưu ý rằng trên các hệ thống không phải POSIX có tính giây nhuận vào timestamp, các giây nhuận sẽ bị :meth:`fromtimestamp` bỏ qua.

   .. versionchanged:: 3.3
      Nêu :exc:`OverflowError` thay vì :exc:`ValueError` nếu timestamp nằm ngoài phạm vi giá trị được platform C hỗ trợ
      Hàm :c:func:`localtime`. Nêu :exc:`OSError` thay vì
      :exc:`ValueError` khi :c:func:`localtime` không thành công.


.. classmethod:: date.fromordinal(ordinal)

   Trả về ngày tương ứng với *ordinal* Gregorian mở rộng, trong đó ngày 1 tháng 1 của năm 1 có ordinal là 1.

   :exc:`ValueError` được nêu trừ khi ``1 <= ordinal <= date.max.toordinal()``. Với mọi ngày ``d``, ``date.fromordinal(d.toordinal()) == d``.


.. classmethod:: date.fromisoformat(date_string)

   Trả về một :class:`date` tương ứng với *date_string* được cung cấp ở bất kỳ định dạng ISO 8601 hợp lệ nào, với các ngoại lệ sau:

   1. Hiện chưa hỗ trợ ngày có độ chính xác rút gọn (``YYYY-MM``, ``YYYY``).
   2. Các biểu diễn ngày mở rộng hiện chưa được hỗ trợ (``±YYYYYY-MM-DD``).
   3. Ngày thứ tự hiện chưa được hỗ trợ (``YYYY-OOO``).

   Ví dụ::

      >>> import datetime as dt
      >>> dt.date.fromisoformat('2019-12-04')
      datetime.date(2019, 12, 4)
      >>> dt.date.fromisoformat('20191204')
      datetime.date(2019, 12, 4)
      >>> dt.date.fromisoformat('2021-W01-1')
      datetime.date(2021, 1, 4)

   .. versionadded:: 3.7
   .. versionchanged:: 3.11
      Trước đây, phương thức này chỉ hỗ trợ định dạng ``YYYY-MM-DD``.


.. classmethod:: date.fromisocalendar(year, week, day)

   Trả về một :class:`date` tương ứng với ngày theo lịch ISO được chỉ định bởi *year*, *week* và *day*. Đây là hàm ngược của hàm :meth:`date.isocalendar`.

   .. versionadded:: 3.8


.. classmethod:: date.strptime(date_string, format)

   Trả về một :class:`.date` tương ứng với *date_string*, được phân tích theo *format*. Điều này tương đương với::

     date(*(time.strptime(date_string, format)[0:3]))

   :exc:`ValueError` được phát sinh nếu không thể phân tích date_string và format bằng :func:`time.strptime` hoặc nếu hàm này trả về một giá trị không phải là time tuple. Xem thêm :ref:`strftime-strptime-behavior` và
   :meth:`date.fromisoformat`.

   .. note::

      Nếu *format* chỉ định một ngày trong tháng mà không có năm thì một
      :exc:`DeprecationWarning` được phát ra. Điều này nhằm tránh lỗi năm nhuận bốn năm một lần trong mã chỉ tìm cách phân tích tháng và ngày, vì năm mặc định được dùng khi không có năm trong định dạng không phải là năm nhuận. Các giá trị *format* như vậy có thể gây ra lỗi kể từ Python 3.15. Cách khắc phục là luôn bao gồm một năm trong *format*. Nếu phân tích các giá trị *date_string* không có năm, hãy thêm rõ ràng một năm nhuận trước khi phân tích:

      .. doctest::

         >>> import datetime as dt
         >>> date_string = "02/29"
         >>> when = dt.date.strptime(f"{date_string};1984", "%m/%d;%Y")  # Tránh lỗi năm nhuận.
         >>> when.strftime("%B %d")  # doctest: +SKIP
         'February 29'

   .. versionadded:: 3.14


Các thuộc tính của lớp:

.. attribute:: date.min

   Ngày sớm nhất có thể biểu diễn, ``date(MINYEAR, 1, 1)``.


.. attribute:: date.max

   Ngày muộn nhất có thể biểu diễn, ``date(MAXYEAR, 12, 31)``.


.. attribute:: date.resolution

   Khoảng chênh lệch nhỏ nhất có thể giữa các đối tượng date không bằng nhau, ``timedelta(days=1)``.


Các thuộc tính của thể hiện (chỉ đọc):

.. attribute:: date.year

   Nằm trong khoảng từ :const:`MINYEAR` đến :const:`MAXYEAR`, bao gồm cả hai giá trị.


.. attribute:: date.month

   Nằm trong khoảng từ 1 đến 12, bao gồm cả hai giá trị.


.. attribute:: date.day

   Nằm trong khoảng từ 1 đến số ngày của tháng đã cho trong năm đã cho.


Các thao tác được hỗ trợ:

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``date2 = date1 + timedelta`` | ``date2`` will be ``timedelta.days`` days    |
|                               | after ``date1``. (1)                         |
+-------------------------------+----------------------------------------------+
| ``date2 = date1 - timedelta`` | Computes ``date2`` such that ``date2 +       |
|                               | timedelta == date1``. (2)                    |
+-------------------------------+----------------------------------------------+
| ``timedelta = date1 - date2`` | \(3)                                         |
+-------------------------------+----------------------------------------------+
| | ``date1 == date2``          | Equality comparison. (4)                     |
| | ``date1 != date2``          |                                              |
+-------------------------------+----------------------------------------------+
| | ``date1 < date2``           | Order comparison. (5)                        |
| | ``date1 > date2``           |                                              |
| | ``date1 <= date2``          |                                              |
| | ``date1 >= date2``          |                                              |
+-------------------------------+----------------------------------------------+

Lưu ý:

(1)
   *date2* được dịch chuyển về phía trước theo thời gian nếu ``timedelta.days > 0``, hoặc lùi lại nếu ``timedelta.days < 0``. Sau đó ``date2 - date1 == timedelta.days``. ``timedelta.seconds`` và ``timedelta.microseconds`` bị bỏ qua.
   :exc:`OverflowError` được phát sinh nếu ``date2.year`` nhỏ hơn
   :const:`MINYEAR` hoặc lớn hơn :const:`MAXYEAR`.

(2)
   ``timedelta.seconds`` và ``timedelta.microseconds`` bị bỏ qua.

(3)
   Điều này là chính xác và không thể xảy ra tràn. ``timedelta.seconds`` và ``timedelta.microseconds`` là 0, còn ``date2 + timedelta == date1`` sau đó.

(4)
   Các đối tượng :class:`date` bằng nhau nếu chúng biểu diễn cùng một ngày.

   Các đối tượng :class:`!date` không đồng thời là các thực thể :class:`.datetime` thì không bao giờ bằng các đối tượng :class:`!datetime`, ngay cả khi chúng biểu diễn cùng một ngày.

(5)
   *date1* được xem là nhỏ hơn *date2* khi *date1* đứng trước *date2* về thời gian. Nói cách khác, ``date1 < date2`` khi và chỉ khi ``date1.toordinal() < date2.toordinal()``.

   Phép so sánh thứ tự giữa một đối tượng :class:`date` không đồng thời là một
   instance :class:`.datetime` và một đối tượng :class:`!datetime` sẽ phát sinh lỗi
   :exc:`TypeError`.

.. versionchanged:: 3.13
   Phép so sánh giữa đối tượng :class:`.datetime` và một instance của lớp con :class:`date` không phải là lớp con :class:`!datetime` không còn chuyển đối tượng sau thành :class:`!date`, bỏ qua phần thời gian và múi giờ. Có thể thay đổi hành vi mặc định bằng cách ghi đè các phương thức so sánh đặc biệt trong các lớp con.

Trong các ngữ cảnh Boolean, mọi đối tượng :class:`date` đều được xem là true.

Các phương thức instance:

.. method:: date.replace(year=self.year, month=self.month, day=self.day)

   Trả về một đối tượng :class:`date` mới với các giá trị giống nhau, nhưng các tham số được chỉ định đã được cập nhật.

   Ví dụ::

       >>> import datetime as dt
       >>> d = dt.date(2002, 12, 31)
       >>> d.replace(day=26)
       datetime.date(2002, 12, 26)

   Hàm generic :func:`copy.replace` cũng hỗ trợ các đối tượng :class:`date`.


.. method:: date.timetuple()

   Trả về một :class:`time.struct_time` như giá trị được trả về bởi :func:`time.localtime`.

   Giờ, phút và giây đều bằng 0, còn cờ DST là -1.

   ``d.timetuple()`` tương đương với::

     time.struct_time((d.year, d.month, d.day, 0, 0, 0, d.weekday(), yday, -1))

   trong đó ``yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1`` là số thứ tự của ngày trong năm hiện tại, bắt đầu từ 1 cho ngày 1 tháng 1.


.. method:: date.toordinal()

   Trả về số thứ tự Gregorian mở rộng của ngày, trong đó ngày 1 tháng 1 của năm 1 có số thứ tự là 1. Với mọi đối tượng :class:`date` ``d``, ``date.fromordinal(d.toordinal()) == d``.


.. method:: date.weekday()

   Trả về ngày trong tuần dưới dạng số nguyên, trong đó thứ Hai là 0 và Chủ nhật là 6. Ví dụ: ``date(2002, 12, 4).weekday() == 2``, là thứ Tư. Xem thêm
   :meth:`isoweekday`.


.. method:: date.isoweekday()

   Trả về ngày trong tuần dưới dạng số nguyên, trong đó thứ Hai là 1 và Chủ nhật là 7. Ví dụ: ``date(2002, 12, 4).isoweekday() == 3``, là thứ Tư. Xem thêm
   :meth:`weekday`, :meth:`isocalendar`.


.. method:: date.isocalendar()

   Trả về một đối tượng :term:`named tuple` gồm ba thành phần: ``year``, ``week`` và ``weekday``.

   Lịch ISO là một biến thể được sử dụng rộng rãi của lịch Gregory. [#]_

   Năm ISO gồm 52 hoặc 53 tuần trọn vẹn, trong đó một tuần bắt đầu vào thứ Hai và kết thúc vào Chủ nhật. Tuần đầu tiên của một năm ISO là tuần dương lịch (Gregory) đầu tiên của một năm có chứa thứ Năm. Tuần này được gọi là tuần số 1, và năm ISO của ngày thứ Năm đó trùng với năm Gregory của ngày đó.

   Ví dụ: năm 2004 bắt đầu vào thứ Năm, vì vậy tuần đầu tiên của năm ISO 2004 bắt đầu vào thứ Hai, ngày 29 tháng 12 năm 2003 và kết thúc vào Chủ nhật, ngày 4 tháng 1 năm 2004::

        >>> import datetime as dt
        >>> dt.date(2003, 12, 29).isocalendar()
        datetime.IsoCalendarDate(year=2004, week=1, weekday=1)
        >>> dt.date(2004, 1, 4).isocalendar()
        datetime.IsoCalendarDate(year=2004, week=1, weekday=7)

   .. versionchanged:: 3.9
      Kết quả đã được thay đổi từ tuple thành :term:`named tuple`.


.. method:: date.isoformat()

   Trả về một chuỗi biểu diễn ngày ở định dạng ISO 8601, ``YYYY-MM-DD``::

       >>> import datetime as dt
       >>> dt.date(2002, 12, 4).isoformat()
       '2002-12-04'


.. method:: date.__str__()

   Đối với một ngày ``d``, ``str(d)`` tương đương với ``d.isoformat()``.


.. method:: date.ctime()

   Trả về một chuỗi biểu diễn ngày::

       >>> import datetime as dt
       >>> dt.date(2002, 12, 4).ctime()
       'Wed Dec  4 00:00:00 2002'

   ``d.ctime()`` tương đương với::

     time.ctime(time.mktime(d.timetuple()))

   trên các nền tảng mà C gốc
   hàm :c:func:`ctime` (mà :func:`time.ctime` gọi, nhưng
   :meth:`date.ctime` không gọi) tuân thủ tiêu chuẩn C.


.. method:: date.strftime(format)

   Trả về một chuỗi biểu diễn ngày tháng, được điều khiển bởi một chuỗi định dạng tường minh. Các mã định dạng chỉ giờ, phút hoặc giây sẽ nhận giá trị 0. Xem thêm :ref:`strftime-strptime-behavior` và :meth:`date.isoformat`.


.. method:: date.__format__(format)

   Giống :meth:`.date.strftime`. Điều này cho phép chỉ định một chuỗi định dạng cho đối tượng :class:`.date` trong các chuỗi ký tự định dạng :ref:`formatted string literals <f-strings>` và khi sử dụng :meth:`str.format`. Xem thêm :ref:`strftime-strptime-behavior` và :meth:`date.isoformat`.


Các ví dụ sử dụng: :class:`!date`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ví dụ về cách đếm số ngày đến một sự kiện::

    >>> import time
    >>> import datetime as dt
    >>> today = dt.date.today()
    >>> today
    datetime.date(2007, 12, 5)
    >>> today == dt.date.fromtimestamp(time.time())
    True
    >>> my_birthday = dt.date(today.year, 6, 24)
    >>> if my_birthday < today:
    ...     my_birthday = my_birthday.replace(year=today.year + 1)
    ...
    >>> my_birthday
    datetime.date(2008, 6, 24)
    >>> time_to_birthday = abs(my_birthday - today)
    >>> time_to_birthday.days
    202

Các ví dụ khác về cách làm việc với :class:`date`:

.. doctest::

    >>> import datetime as dt
    >>> d = dt.date.fromordinal(730920) # Ngày thứ 730920 kể từ 1. 1. 0001
    >>> d
    datetime.date(2002, 3, 11)

    >>> # Các phương thức liên quan đến việc định dạng đầu ra chuỗi
    >>> d.isoformat()
    '2002-03-11'
    >>> d.strftime("%d/%m/%y")
    '11/03/02'
    >>> d.strftime("%A %d. %B %Y")
    'Monday 11. March 2002'
    >>> d.ctime()
    'Mon Mar 11 00:00:00 2002'
    >>> 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(d, "day", "month")
    'The day is 11, the month is March.'

    >>> # Các phương thức trích xuất 'thành phần' theo các lịch khác nhau
    >>> t = d.timetuple()
    >>> for i in t:     # doctest: +SKIP
    ...     print(i)
    2002                # năm
    3                   # tháng
    11                  # ngày
    0
    0
    0
    0                   # thứ trong tuần (0 = Thứ Hai)
    70                  # ngày thứ 70 trong năm
    -1
    >>> ic = d.isocalendar()
    >>> for i in ic:    # doctest: +SKIP
    ...     print(i)
    2002                # Năm ISO
    11                  # Số tuần ISO
    1                   # Số ngày ISO ( 1 = Thứ Hai )

    >>> # Đối tượng date là bất biến; mọi thao tác đều tạo ra một đối tượng mới
    >>> d.replace(year=2005)
    datetime.date(2005, 3, 11)


.. _datetime-datetime:

Các đối tượng :class:`!datetime`
--------------------------------

Một đối tượng :class:`.datetime` là một đối tượng duy nhất chứa mọi thông tin từ một đối tượng :class:`date` và một đối tượng :class:`.time`.

Giống như một đối tượng :class:`date`, :class:`.datetime` giả định lịch Gregory hiện tại được mở rộng theo cả hai hướng; giống như một đối tượng :class:`.time`,
:class:`!datetime` giả định rằng mỗi ngày có chính xác 3600\*24 giây.

Hàm khởi tạo:

.. class:: datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)

   Các đối số *year*, *month* và *day* là bắt buộc. *tzinfo* có thể là ``None`` hoặc một instance của một lớp con :class:`tzinfo`. Các đối số còn lại phải là số nguyên trong các phạm vi sau:

   * ``MINYEAR <= year <= MAXYEAR``,
   * ``1 <= month <= 12``,
   * ``1 <= day <= number of days in the given month and year``,
   * ``0 <= hour < 24``,
   * ``0 <= minute < 60``,
   * ``0 <= second < 60``,
   * ``0 <= microsecond < 1000000``,
   * ``fold in [0, 1]``.

   Nếu cung cấp một đối số nằm ngoài các phạm vi đó, :exc:`ValueError` sẽ được raise.

   .. versionchanged:: 3.6
      Đã thêm tham số *fold*.


Các hàm khởi tạo khác, tất cả đều là class method:

.. classmethod:: datetime.today()

   Trả về ngày và giờ địa phương hiện tại, kèm theo :attr:`.tzinfo` ``None``.

   Tương đương với::

     datetime.fromtimestamp(time.time())

   Xem thêm :meth:`now`, :meth:`fromtimestamp`.

   Về mặt chức năng, phương thức này tương đương với :meth:`now`, nhưng không có tham số ``tz``.


.. classmethod:: datetime.now(tz=None)

   Trả về ngày và giờ địa phương hiện tại.

   Nếu đối số tùy chọn *tz* là ``None`` hoặc không được chỉ định, giá trị này tương tự :meth:`today`, nhưng nếu có thể sẽ cung cấp độ chính xác cao hơn so với việc đi qua một timestamp :func:`time.time` (ví dụ: điều này có thể thực hiện được trên các nền tảng cung cấp hàm C
   :c:func:`gettimeofday`).

   Nếu *tz* không phải là ``None``, thì nó phải là một instance của một lớp con :class:`tzinfo`, và ngày giờ hiện tại được chuyển đổi sang múi giờ của *tz*.

   Hàm này được ưu tiên hơn :meth:`today` và :meth:`utcnow`.

   .. note::

      Các lần gọi tiếp theo đến :meth:`!datetime.now` có thể trả về cùng một thời điểm, tùy thuộc vào độ chính xác của clock bên dưới.


.. classmethod:: datetime.utcnow()

   Trả về ngày và giờ UTC hiện tại, với :attr:`.tzinfo` là ``None``.

   Tương tự như :meth:`now`, nhưng trả về ngày và giờ UTC hiện tại dưới dạng một
   đối tượng :class:`.datetime`. Có thể lấy datetime UTC hiện tại có thông tin múi giờ bằng cách gọi ``datetime.now(timezone.utc)``. Xem thêm :meth:`now`.

   .. warning::

      Vì các đối tượng ``datetime`` không có thông tin múi giờ được nhiều phương thức ``datetime`` xem là giờ địa phương, nên nên sử dụng datetime có thông tin múi giờ để biểu diễn thời gian UTC. Do đó, cách được khuyến nghị để tạo một đối tượng biểu diễn thời gian UTC hiện tại là gọi ``datetime.now(timezone.utc)``.

   .. deprecated:: 3.12

      Thay vào đó, hãy sử dụng :meth:`datetime.now` với :const:`UTC`.


.. classmethod:: datetime.fromtimestamp(timestamp, tz=None)

   Trả về ngày và giờ cục bộ tương ứng với timestamp POSIX, chẳng hạn như giá trị do :func:`time.time` trả về. Nếu đối số tùy chọn *tz* là ``None`` hoặc không được chỉ định, timestamp sẽ được chuyển đổi thành ngày và giờ cục bộ của nền tảng, còn đối tượng :class:`.datetime` được trả về sẽ là naive.

   Nếu *tz* không phải là ``None``, nó phải là một instance của một subclass của :class:`tzinfo`, và timestamp sẽ được chuyển đổi sang múi giờ của *tz*.

   :meth:`fromtimestamp` có thể phát sinh :exc:`OverflowError` nếu timestamp nằm ngoài phạm vi các giá trị được :c:func:`localtime` C của nền tảng hỗ trợ hoặc
   các hàm :c:func:`gmtime`, và :exc:`OSError` khi :c:func:`localtime` hoặc
   :c:func:`gmtime` gặp lỗi. Thông thường, phạm vi này chỉ giới hạn trong các năm từ 1970 đến 2038. Lưu ý rằng trên các hệ thống không phải POSIX có tính cả giây nhuận trong cách biểu diễn timestamp, các giây nhuận sẽ bị :meth:`fromtimestamp` bỏ qua, nên có thể xảy ra trường hợp hai timestamp chênh nhau một giây nhưng cho ra các đối tượng :class:`.datetime` giống hệt nhau. Phương thức này được ưu tiên hơn
   :meth:`utcfromtimestamp`.

   .. versionchanged:: 3.3
      Phát sinh :exc:`OverflowError` thay vì :exc:`ValueError` nếu timestamp nằm ngoài phạm vi các giá trị được C của nền tảng hỗ trợ
      các hàm :c:func:`localtime` hoặc :c:func:`gmtime`. Phát sinh :exc:`OSError` thay vì :exc:`ValueError` khi :c:func:`localtime` hoặc :c:func:`gmtime` bị lỗi.

   .. versionchanged:: 3.6
      :meth:`fromtimestamp` may return instances with :attr:`.fold` set to 1.

.. classmethod:: datetime.utcfromtimestamp(timestamp)

   Trả về :class:`.datetime` UTC tương ứng với dấu thời gian POSIX, với
   :attr:`.tzinfo` ``None``.  (Đối tượng kết quả là naive.)

   Thao tác này có thể phát sinh :exc:`OverflowError` nếu dấu thời gian nằm ngoài phạm vi giá trị được hàm :c:func:`gmtime` C của nền tảng hỗ trợ, và :exc:`OSError` khi :c:func:`gmtime` bị lỗi. Thông thường, phạm vi này bị giới hạn trong các năm từ 1970 đến 2038.

   Để lấy một đối tượng :class:`.datetime` aware, hãy gọi :meth:`fromtimestamp`::

     datetime.fromtimestamp(timestamp, timezone.utc)

   Trên các nền tảng tuân thủ POSIX, thao tác này tương đương với biểu thức sau::

     datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=timestamp)

   ngoại trừ việc công thức sau luôn hỗ trợ toàn bộ phạm vi năm: từ
   Bao gồm cả :const:`MINYEAR` và :const:`MAXYEAR`.

   .. warning::

      Vì các đối tượng ``datetime`` naive được nhiều phương thức ``datetime`` coi là giờ địa phương, nên ưu tiên sử dụng datetime aware để biểu diễn thời gian theo UTC. Do đó, cách được khuyến nghị để tạo một đối tượng biểu diễn một timestamp cụ thể theo UTC là gọi ``datetime.fromtimestamp(timestamp, tz=timezone.utc)``.

   .. versionchanged:: 3.3
      Phát sinh :exc:`OverflowError` thay vì :exc:`ValueError` nếu timestamp nằm ngoài phạm vi các giá trị được C của nền tảng hỗ trợ
      Hàm :c:func:`gmtime`. Gây ra :exc:`OSError` thay vì
      :exc:`ValueError` khi :c:func:`gmtime` không thành công.

   .. versionchanged:: 3.15
      Chấp nhận mọi số thực làm *timestamp*, không chỉ số nguyên hoặc số thực dấu phẩy động.

   .. deprecated:: 3.12

      Thay vào đó, hãy dùng :meth:`datetime.fromtimestamp` với :const:`UTC`.


.. classmethod:: datetime.fromordinal(ordinal)

   Trả về :class:`.datetime` tương ứng với ordinal theo lịch Gregory mở rộng, trong đó ngày 1 tháng 1 của năm 1 có ordinal là 1. :exc:`ValueError` được phát sinh trừ khi ``1 <= ordinal <= datetime.max.toordinal()``. Giờ, phút, giây và microsecond của kết quả đều bằng 0, và :attr:`.tzinfo` là ``None``.


.. classmethod:: datetime.combine(date, time, tzinfo=time.tzinfo)

   Trả về một đối tượng :class:`.datetime` mới có các thành phần ngày bằng với các thành phần của đối tượng :class:`date` đã cho, và các thành phần thời gian bằng với các thành phần của đối tượng :class:`.time` đã cho. Nếu cung cấp đối số *tzinfo*, giá trị của đối số này được dùng để thiết lập thuộc tính :attr:`.tzinfo` của kết quả; nếu không, thuộc tính :attr:`~.time.tzinfo` của đối số *time* được dùng. Nếu đối số *date* là một đối tượng :class:`!datetime`, các thành phần thời gian và thuộc tính :attr:`.tzinfo` của đối tượng đó sẽ bị bỏ qua.

   Với mọi đối tượng :class:`.datetime` ``d``, ``d == datetime.combine(d.date(), d.time(), d.tzinfo)``.

   .. versionchanged:: 3.6
      Đã thêm đối số *tzinfo*.


.. classmethod:: datetime.fromisoformat(date_string)

   Trả về một :class:`.datetime` tương ứng với một *date_string* ở bất kỳ định dạng ISO 8601 hợp lệ nào, với các ngoại lệ sau:

   1. Offset múi giờ có thể có phần giây lẻ.
   2. Dấu phân cách ``T`` có thể được thay thế bằng bất kỳ ký tự Unicode đơn nào.
   3. Không hỗ trợ giờ và phút dạng phân số.
   4. Hiện chưa hỗ trợ ngày tháng với độ chính xác rút gọn (``YYYY-MM``, ``YYYY``).
   5. Hiện chưa hỗ trợ các biểu diễn ngày tháng mở rộng (``±YYYYYY-MM-DD``).
   6. Hiện chưa hỗ trợ ngày thứ tự (``YYYY-OOO``).

   Ví dụ::

       >>> import datetime as dt
       >>> dt.datetime.fromisoformat('2011-11-04')
       datetime.datetime(2011, 11, 4, 0, 0)
       >>> dt.datetime.fromisoformat('20111104')
       datetime.datetime(2011, 11, 4, 0, 0)
       >>> dt.datetime.fromisoformat('2011-11-04T00:05:23')
       datetime.datetime(2011, 11, 4, 0, 5, 23)
       >>> dt.datetime.fromisoformat('2011-11-04T00:05:23Z')
       datetime.datetime(2011, 11, 4, 0, 5, 23, tzinfo=datetime.timezone.utc)
       >>> dt.datetime.fromisoformat('20111104T000523')
       datetime.datetime(2011, 11, 4, 0, 5, 23)
       >>> dt.datetime.fromisoformat('2011-W01-2T00:05:23.283')
       datetime.datetime(2011, 1, 4, 0, 5, 23, 283000)
       >>> dt.datetime.fromisoformat('2011-11-04 00:05:23.283')
       datetime.datetime(2011, 11, 4, 0, 5, 23, 283000)
       >>> dt.datetime.fromisoformat('2011-11-04 00:05:23.283+00:00')
       datetime.datetime(2011, 11, 4, 0, 5, 23, 283000, tzinfo=datetime.timezone.utc)
       >>> dt.datetime.fromisoformat('2011-11-04T00:05:23+04:00')   # doctest: +NORMALIZE_WHITESPACE
       datetime.datetime(2011, 11, 4, 0, 5, 23,
           tzinfo=datetime.timezone(datetime.timedelta(seconds=14400)))

   .. versionadded:: 3.7
   .. versionchanged:: 3.11
      Trước đây, phương thức này chỉ hỗ trợ các định dạng có thể được tạo ra bởi
      :meth:`date.isoformat` hoặc :meth:`datetime.isoformat`.


.. classmethod:: datetime.fromisocalendar(year, week, day)

   Trả về một :class:`.datetime` tương ứng với ngày theo lịch ISO được chỉ định bởi *year*, *week* và *day*. Các thành phần không phải ngày của datetime được điền bằng các giá trị mặc định thông thường. Đây là hàm nghịch đảo của hàm
   :meth:`datetime.isocalendar`.

   .. versionadded:: 3.8


.. classmethod:: datetime.strptime(date_string, format)

   Trả về một :class:`.datetime` tương ứng với *date_string*, được phân tích theo *format*.

   Nếu *format* không chứa thông tin microsecond hoặc múi giờ, thì điều này tương đương với::

     datetime(*(time.strptime(date_string, format)[0:6]))

   :exc:`ValueError` được phát sinh nếu không thể phân tích date_string và format bằng :func:`time.strptime`, hoặc nếu hàm này trả về một giá trị không phải là một time tuple. Xem thêm :ref:`strftime-strptime-behavior` và
   :meth:`datetime.fromisoformat`.

   .. versionchanged:: 3.13

      Nếu *format* chỉ định ngày trong tháng mà không có năm thì một
      :exc:`DeprecationWarning` hiện được phát ra. Điều này nhằm tránh lỗi năm nhuận bốn năm một lần trong mã chỉ tìm cách phân tích tháng và ngày, vì năm mặc định được sử dụng khi format không có năm không phải là năm nhuận. Các giá trị *format* như vậy có thể gây lỗi kể từ Python 3.15. Cách khắc phục là luôn включ năm trong *format*. Nếu phân tích các giá trị *date_string* không có năm, hãy thêm rõ ràng một năm nhuận trước khi phân tích:

      .. doctest::

         >>> import datetime as dt
         >>> date_string = "02/29"
         >>> when = dt.datetime.strptime(f"{date_string};1984", "%m/%d;%Y")  # Tránh lỗi năm nhuận.
         >>> when.strftime("%B %d")  # doctest: +SKIP
         'February 29'


Các thuộc tính lớp:

.. attribute:: datetime.min

   :class:`.datetime` có thể biểu diễn sớm nhất là ``datetime(MINYEAR, 1, 1, tzinfo=None)``.


.. attribute:: datetime.max

   :class:`.datetime` có thể biểu diễn muộn nhất là ``datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=None)``.


.. attribute:: datetime.resolution

   Độ chênh lệch nhỏ nhất có thể có giữa các đối tượng :class:`.datetime` không bằng nhau là ``timedelta(microseconds=1)``.


Các thuộc tính thực thể (chỉ đọc):

.. attribute:: datetime.year

   Trong khoảng từ :const:`MINYEAR` đến :const:`MAXYEAR`, bao gồm cả hai đầu mút.


.. attribute:: datetime.month

   Trong khoảng từ 1 đến 12, bao gồm cả hai đầu mút.


.. attribute:: datetime.day

   Trong khoảng từ 1 đến số ngày của tháng đã cho trong năm đã cho.


.. attribute:: datetime.hour

   Trong ``range(24)``.


.. attribute:: datetime.minute

   Trong ``range(60)``.


.. attribute:: datetime.second

   Trong ``range(60)``.


.. attribute:: datetime.microsecond

   Trong ``range(1000000)``.


.. attribute:: datetime.tzinfo

   Đối tượng được truyền làm đối số *tzinfo* cho hàm khởi tạo :class:`.datetime`, hoặc ``None`` nếu không truyền đối số nào.


.. attribute:: datetime.fold

   Trong ``[0, 1]``. Dùng để phân biệt các thời điểm theo giờ địa phương trong một khoảng thời gian lặp lại. (Khoảng thời gian lặp lại xảy ra khi đồng hồ được lùi lại vào cuối giờ mùa hè hoặc khi độ lệch UTC của múi giờ hiện tại bị giảm vì lý do chính trị.) Các giá trị 0 và 1 lần lượt biểu thị thời điểm sớm hơn và muộn hơn trong hai thời điểm có cùng biểu diễn theo giờ địa phương.

   .. versionadded:: 3.6


Các thao tác được hỗ trợ:

+---------------------------------------+--------------------------------+
| Operation                             | Result                         |
+=======================================+================================+
| ``datetime2 = datetime1 + timedelta`` | \(1)                           |
+---------------------------------------+--------------------------------+
| ``datetime2 = datetime1 - timedelta`` | \(2)                           |
+---------------------------------------+--------------------------------+
| ``timedelta = datetime1 - datetime2`` | \(3)                           |
+---------------------------------------+--------------------------------+
| | ``datetime1 == datetime2``          | Equality comparison. (4)       |
| | ``datetime1 != datetime2``          |                                |
+---------------------------------------+--------------------------------+
| | ``datetime1 < datetime2``           | Order comparison. (5)          |
| | ``datetime1 > datetime2``           |                                |
| | ``datetime1 <= datetime2``          |                                |
| | ``datetime1 >= datetime2``          |                                |
+---------------------------------------+--------------------------------+

(1)
   ``datetime2`` là khoảng thời lượng ``timedelta`` được trừ khỏi ``datetime1``, tiến về phía trước theo thời gian nếu ``timedelta.days > 0``, hoặc lùi lại nếu ``timedelta.days < 0``. Kết quả có cùng thuộc tính :attr:`~.datetime.tzinfo` như datetime đầu vào, và ``datetime2 - datetime1 == timedelta`` sau đó. :exc:`OverflowError` được phát sinh nếu ``datetime2.year`` nhỏ hơn :const:`MINYEAR` hoặc lớn hơn
   :const:`MAXYEAR`. Lưu ý rằng không thực hiện điều chỉnh múi giờ nào, ngay cả khi đầu vào là một đối tượng aware.

(2)
   Tính ``datetime2`` sao cho ``datetime2 + timedelta == datetime1``. Tương tự phép cộng, kết quả có cùng thuộc tính :attr:`~.datetime.tzinfo` như datetime đầu vào và không thực hiện điều chỉnh múi giờ nào, ngay cả khi đầu vào là aware.

(3)
   Phép trừ một :class:`.datetime` khỏi một :class:`!datetime` chỉ được định nghĩa khi cả hai toán hạng đều là naive hoặc cả hai đều là aware. Nếu một toán hạng là aware còn toán hạng kia là naive, :exc:`TypeError` được phát sinh.

   Nếu cả hai đều naive, hoặc cả hai đều aware và có cùng thuộc tính :attr:`~.datetime.tzinfo`, thì các thuộc tính :attr:`~.datetime.tzinfo` được bỏ qua, và kết quả là một đối tượng :class:`timedelta` ``t`` sao cho ``datetime2 + t == datetime1``. Trong trường hợp này, không thực hiện điều chỉnh múi giờ.

   Nếu cả hai đều aware và có các thuộc tính :attr:`~.datetime.tzinfo` khác nhau, ``a-b`` hoạt động như thể ``a`` và ``b`` trước tiên được chuyển đổi thành các đối tượng datetime UTC naive. Kết quả là ``(a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None)
   - b.utcoffset())`` ngoại trừ việc quá trình triển khai không bao giờ bị tràn.

(4)
   Các đối tượng :class:`.datetime` bằng nhau nếu chúng biểu diễn cùng ngày và giờ, có tính đến múi giờ.

   Các đối tượng :class:`.datetime` naive và aware không bao giờ bằng nhau.

   Nếu cả hai toán hạng so sánh đều aware và có cùng thuộc tính :attr:`!tzinfo`, thì các thuộc tính :attr:`!tzinfo` và :attr:`~.datetime.fold` được bỏ qua và các datetime cơ sở được so sánh. Nếu cả hai toán hạng so sánh đều aware và có các thuộc tính :attr:`~.datetime.tzinfo` khác nhau, phép so sánh diễn ra như thể các toán hạng trước tiên được chuyển đổi thành các datetime UTC, ngoại trừ việc quá trình triển khai không bao giờ bị tràn.
   Các thực thể :class:`.datetime` trong một khoảng lặp lại không bao giờ bằng
   Các thực thể :class:`!datetime` trong múi giờ khác.

(5)
   *datetime1* được xem là nhỏ hơn *datetime2* khi *datetime1* đứng trước *datetime2* về thời gian, có tính đến múi giờ.

   So sánh thứ tự giữa các đối tượng :class:`.datetime` naive và aware sẽ phát sinh :exc:`TypeError`.

   Nếu cả hai toán hạng so sánh đều aware và có cùng thuộc tính :attr:`!tzinfo`, thì các thuộc tính :attr:`!tzinfo` và :attr:`~.datetime.fold` được bỏ qua và các datetime cơ sở được so sánh. Nếu cả hai toán hạng so sánh đều aware và có các thuộc tính :attr:`~.datetime.tzinfo` khác nhau, phép so sánh diễn ra như thể các toán hạng trước tiên được chuyển đổi thành các datetime UTC, ngoại trừ việc quá trình triển khai không bao giờ bị tràn.

.. versionchanged:: 3.3
   So sánh bằng giữa các thực thể :class:`.datetime` aware và naive không phát sinh :exc:`TypeError`.

.. versionchanged:: 3.13
   Việc so sánh giữa đối tượng :class:`.datetime` và một thực thể của lớp con :class:`date` không phải là lớp con :class:`!datetime` không còn chuyển đổi thực thể sau thành :class:`!date`, bỏ qua phần thời gian và múi giờ. Có thể thay đổi hành vi mặc định bằng cách ghi đè các phương thức so sánh đặc biệt trong các lớp con.


Các phương thức của thực thể:

.. method:: datetime.date()

   Trả về đối tượng :class:`date` có cùng năm, tháng và ngày.


.. method:: datetime.time()

   Trả về đối tượng :class:`.time` có cùng giờ, phút, giây, microsecond và fold.
   :attr:`.tzinfo` là ``None``. Xem thêm phương thức :meth:`timetz`.

   .. versionchanged:: 3.6
      Giá trị fold được sao chép vào đối tượng :class:`.time` được trả về.


.. method:: datetime.timetz()

   Trả về đối tượng :class:`.time` có cùng các thuộc tính hour, minute, second, microsecond, fold và tzinfo. Xem thêm phương thức :meth:`time`.

   .. versionchanged:: 3.6
      Giá trị fold được sao chép vào đối tượng :class:`.time` được trả về.


.. method:: datetime.replace(year=self.year, month=self.month, day=self.day, \
   hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, \ tzinfo=self.tzinfo, *, fold=0)

   Trả về một đối tượng :class:`datetime` mới với các thuộc tính giống nhau, nhưng các tham số được chỉ định sẽ được cập nhật. Lưu ý rằng có thể chỉ định ``tzinfo=None`` để tạo một datetime naive từ một datetime aware mà không chuyển đổi dữ liệu ngày và giờ.

   Các đối tượng :class:`.datetime` cũng được generic function hỗ trợ
   :func:`copy.replace`.

   .. versionchanged:: 3.6
      Đã thêm tham số *fold*.


.. method:: datetime.astimezone(tz=None)

   Trả về một :class:`.datetime` đối tượng với thuộc tính :attr:`.tzinfo` *tz*, điều chỉnh dữ liệu ngày và giờ để kết quả có cùng thời điểm UTC với *self*, nhưng theo giờ địa phương của *tz*.

   Nếu được cung cấp, *tz* phải là một instance của một lớp con :class:`tzinfo`, và
   Các phương thức :meth:`utcoffset` và :meth:`dst` không được trả về ``None``. Nếu *self* là naive, nó được giả định là biểu thị thời gian trong múi giờ hệ thống.

   Nếu được gọi mà không có đối số (hoặc với ``tz=None``), múi giờ cục bộ của hệ thống sẽ được giả định làm múi giờ đích. Thuộc tính ``.tzinfo`` của instance datetime đã chuyển đổi sẽ được đặt thành một instance của :class:`timezone` với tên múi giờ và độ lệch được lấy từ hệ điều hành.

   Nếu ``self.tzinfo`` là *tz*, thì ``self.astimezone(tz)`` bằng *self*: không thực hiện điều chỉnh dữ liệu ngày hoặc giờ. Nếu không, kết quả là giờ địa phương trong múi giờ *tz*, biểu diễn cùng thời điểm UTC với *self*: sau ``astz = dt.astimezone(tz)``, ``astz - astz.utcoffset()`` sẽ có dữ liệu ngày và giờ giống như ``dt - dt.utcoffset()``.

   Nếu bạn chỉ muốn gắn một đối tượng :class:`timezone` *tz* vào datetime *dt* mà không điều chỉnh dữ liệu ngày và giờ, hãy sử dụng ``dt.replace(tzinfo=tz)``. Nếu bạn chỉ muốn xóa đối tượng :class:`!timezone` khỏi một datetime có thông tin múi giờ *dt* mà không chuyển đổi dữ liệu ngày và giờ, hãy sử dụng ``dt.replace(tzinfo=None)``.

   Lưu ý rằng phương thức :meth:`tzinfo.fromutc` mặc định có thể được ghi đè trong một
   lớp con :class:`tzinfo` để thay đổi kết quả do :meth:`astimezone` trả về. Bỏ qua các trường hợp lỗi, :meth:`astimezone` hoạt động giống như::

      def astimezone(self, tz):
          if self.tzinfo is tz:
              return self
          # Chuyển self sang UTC và gắn đối tượng múi giờ mới.
          utc = (self - self.utcoffset()).replace(tzinfo=tz)
          # Chuyển từ UTC sang giờ địa phương của tz.
          return tz.fromutc(utc)

   .. versionchanged:: 3.3
      *tz* giờ đây có thể được bỏ qua.

   .. versionchanged:: 3.6
      Giờ đây có thể gọi phương thức :meth:`astimezone` trên các instance naive được giả định là biểu diễn giờ địa phương của hệ thống.


.. method:: datetime.utcoffset()

   Nếu :attr:`.tzinfo` là ``None``, trả về ``None``, nếu không thì trả về ``self.tzinfo.utcoffset(self)`` và phát sinh ngoại lệ nếu giá trị sau không trả về ``None`` hoặc một đối tượng :class:`timedelta` có độ lớn nhỏ hơn một ngày.

   .. versionchanged:: 3.7
      Độ lệch UTC không bị giới hạn ở một số phút nguyên.


.. method:: datetime.dst()

   Nếu :attr:`.tzinfo` là ``None``, trả về ``None``, nếu không thì trả về ``self.tzinfo.dst(self)`` và phát sinh ngoại lệ nếu giá trị sau không trả về ``None`` hoặc một đối tượng :class:`timedelta` có độ lớn nhỏ hơn một ngày.

   .. versionchanged:: 3.7
      Độ lệch DST không bị giới hạn ở một số phút nguyên.


.. method:: datetime.tzname()

   Nếu :attr:`.tzinfo` là ``None``, trả về ``None``, nếu không thì trả về ``self.tzinfo.tzname(self)``, và phát sinh ngoại lệ nếu giá trị sau không trả về ``None`` hoặc một đối tượng chuỗi,


.. method:: datetime.timetuple()

   Trả về một :class:`time.struct_time` như giá trị được :func:`time.localtime` trả về.

   ``d.timetuple()`` tương đương với::

     time.struct_time((d.year, d.month, d.day,
                       d.hour, d.minute, d.second,
                       d.weekday(), yday, dst))

   trong đó ``yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1`` là số thứ tự của ngày trong năm hiện tại, bắt đầu từ 1 cho ngày 1 tháng 1. Cờ :attr:`~time.struct_time.tm_isdst` của kết quả được thiết lập theo
   phương thức :meth:`dst`: nếu :attr:`.tzinfo` là ``None`` hoặc :meth:`dst` trả về ``None``, thì :attr:`!tm_isdst` được đặt thành ``-1``; nếu không, khi :meth:`dst` trả về một giá trị khác không, :attr:`!tm_isdst` được đặt thành 1; nếu không, :attr:`!tm_isdst` được đặt thành 0.


.. method:: datetime.utctimetuple()

   Nếu :class:`.datetime` instance ``d`` là naive, điều này giống với ``d.timetuple()``, ngoại trừ việc :attr:`~.time.struct_time.tm_isdst` bị buộc đặt thành 0 bất kể ``d.dst()`` trả về gì. DST không bao giờ có hiệu lực đối với thời gian UTC.

   Nếu ``d`` là aware, ``d`` được chuẩn hóa thành thời gian UTC bằng cách trừ ``d.utcoffset()``, rồi trả về một :class:`time.struct_time` cho thời gian đã chuẩn hóa. :attr:`!tm_isdst` bị buộc đặt thành 0. Lưu ý rằng có thể phát sinh :exc:`OverflowError` nếu ``d.year`` là ``MINYEAR`` hoặc ``MAXYEAR`` và việc điều chỉnh sang UTC vượt qua ranh giới năm.

   .. warning::

      Vì các đối tượng ``datetime`` naive được nhiều phương thức ``datetime`` xử lý như thời gian cục bộ, nên ưu tiên sử dụng datetime aware để biểu diễn thời gian UTC; do đó, việc sử dụng :meth:`datetime.utctimetuple` có thể cho kết quả gây hiểu lầm. Nếu bạn có một ``datetime`` naive biểu diễn thời gian UTC, hãy sử dụng ``datetime.replace(tzinfo=timezone.utc)`` để chuyển nó thành aware, sau đó bạn có thể sử dụng :meth:`.datetime.timetuple`.


.. method:: datetime.toordinal()

   Trả về số thứ tự theo lịch Gregorian ngoại suy của ngày. Tương tự như ``self.date().toordinal()``.


.. method:: datetime.timestamp()

   Trả về dấu thời gian POSIX tương ứng với instance :class:`.datetime`. Giá trị trả về là một :class:`float` tương tự như giá trị được trả về bởi :func:`time.time`.

   Các instance :class:`.datetime` không có thông tin múi giờ được giả định là biểu diễn giờ địa phương và phương thức này dựa vào các hàm C của nền tảng để thực hiện việc chuyển đổi. Vì :class:`!datetime` hỗ trợ phạm vi giá trị rộng hơn các hàm C của nền tảng trên nhiều nền tảng, phương thức này có thể phát sinh :exc:`OverflowError` hoặc :exc:`OSError` đối với các thời điểm quá xa trong quá khứ hoặc tương lai.

   Đối với các instance :class:`.datetime` có thông tin múi giờ, giá trị trả về được tính như sau::

      (dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

   .. note::

      Không có phương thức nào để lấy trực tiếp dấu thời gian POSIX từ một instance :class:`.datetime` không có thông tin múi giờ biểu diễn thời gian UTC. Nếu ứng dụng của bạn sử dụng quy ước này và múi giờ hệ thống không được đặt thành UTC, bạn có thể lấy dấu thời gian POSIX bằng cách cung cấp ``tzinfo=timezone.utc``::

         timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

      hoặc bằng cách tính trực tiếp dấu thời gian::

         timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)

   .. versionadded:: 3.3

   .. versionchanged:: 3.6
      Phương thức :meth:`timestamp` sử dụng thuộc tính :attr:`.fold` để phân biệt các thời điểm trong khoảng thời gian lặp lại.

   .. versionchanged:: 3.6
      Phương thức này không còn dựa vào hàm C :c:func:`mktime` của nền tảng để thực hiện việc chuyển đổi.


.. method:: datetime.weekday()

   Trả về ngày trong tuần dưới dạng số nguyên, trong đó thứ Hai là 0 và Chủ nhật là 6. Giống với ``self.date().weekday()``. Xem thêm :meth:`isoweekday`.


.. method:: datetime.isoweekday()

   Trả về ngày trong tuần dưới dạng số nguyên, trong đó thứ Hai là 1 và Chủ nhật là 7. Giống với ``self.date().isoweekday()``. Xem thêm :meth:`weekday`,
   :meth:`isocalendar`.


.. method:: datetime.isocalendar()

   Trả về một :term:`named tuple` gồm ba thành phần: ``year``, ``week`` và ``weekday``. Giống với ``self.date().isocalendar()``.


.. method:: datetime.isoformat(sep='T', timespec='auto')

   Trả về một chuỗi biểu thị ngày và giờ theo định dạng ISO 8601:

   - ``YYYY-MM-DDTHH:MM:SS.ffffff``, nếu :attr:`microsecond` không phải là 0
   - ``YYYY-MM-DDTHH:MM:SS``, nếu :attr:`microsecond` là 0

   Nếu :meth:`utcoffset` không trả về ``None``, một chuỗi sẽ được nối thêm để biểu thị độ lệch UTC:

   - ``YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM[:SS[.ffffff]]``, nếu :attr:`microsecond` không phải là 0
   - ``YYYY-MM-DDTHH:MM:SS+HH:MM[:SS[.ffffff]]``, nếu :attr:`microsecond` là 0

   Ví dụ::

       >>> import datetime as dt
       >>> dt.datetime(2019, 5, 18, 15, 17, 8, 132263).isoformat()
       '2019-05-18T15:17:08.132263'
       >>> dt.datetime(2019, 5, 18, 15, 17, tzinfo=dt.timezone.utc).isoformat()
       '2019-05-18T15:17:00+00:00'

   Đối số tùy chọn *sep* (mặc định là ``'T'``) là dấu phân cách gồm một ký tự, được đặt giữa phần ngày và phần giờ của kết quả. Ví dụ::

      >>> import datetime as dt
      >>> class TZ(dt.tzinfo):
      ...     """A time zone with an arbitrary, constant -06:39 offset."""
      ...     def utcoffset(self, when):
      ...         return dt.timedelta(hours=-6, minutes=-39)
      ...
      >>> dt.datetime(2002, 12, 25, tzinfo=TZ()).isoformat(' ')
      '2002-12-25 00:00:00-06:39'
      >>> dt.datetime(2009, 11, 27, microsecond=100, tzinfo=TZ()).isoformat()
      '2009-11-27T00:00:00.000100-06:39'

   Đối số tùy chọn *timespec* chỉ định số thành phần bổ sung của thời gian cần đưa vào (mặc định là ``'auto'``). Có thể là một trong các giá trị sau:

   - ``'auto'``: Giống ``'seconds'`` nếu :attr:`microsecond` là 0, nếu không thì giống ``'microseconds'``.
   - ``'hours'``: Đưa :attr:`hour` vào định dạng ``HH`` gồm hai chữ số.
   - ``'minutes'``: Bao gồm :attr:`hour` và :attr:`minute` ở định dạng ``HH:MM``.
   - ``'seconds'``: Bao gồm :attr:`hour`, :attr:`minute` và :attr:`second` ở định dạng ``HH:MM:SS``.
   - ``'milliseconds'``: Bao gồm toàn bộ thời gian, nhưng cắt phần giây lẻ xuống còn mili giây. Định dạng ``HH:MM:SS.sss``.
   - ``'microseconds'``: Bao gồm toàn bộ thời gian ở định dạng ``HH:MM:SS.ffffff``.

   .. note::

      Các thành phần thời gian bị loại trừ sẽ bị cắt bỏ, không được làm tròn.

   :exc:`ValueError` sẽ được phát sinh khi đối số *timespec* không hợp lệ::


      >>> import datetime as dt
      >>> dt.datetime.now().isoformat(timespec='minutes')   # doctest: +SKIP
      '2002-12-25T00:00'
      >>> my_datetime = dt.datetime(2015, 1, 1, 12, 30, 59, 0)
      >>> my_datetime.isoformat(timespec='microseconds')
      '2015-01-01T12:30:59.000000'

   .. versionchanged:: 3.6
      Đã thêm tham số *timespec*.


.. method:: datetime.__str__()

   Đối với một thực thể :class:`.datetime` ``d``, ``str(d)`` tương đương với ``d.isoformat(' ')``.


.. method:: datetime.ctime()

   Trả về một chuỗi biểu diễn ngày và giờ::

       >>> import datetime as dt
       >>> dt.datetime(2002, 12, 4, 20, 30, 40).ctime()
       'Wed Dec  4 20:30:40 2002'

   Chuỗi đầu ra *không* bao gồm thông tin múi giờ, bất kể dữ liệu đầu vào là aware hay naive.

   ``d.ctime()`` tương đương với::

     time.ctime(time.mktime(d.timetuple()))

   trên các nền tảng mà hàm :c:func:`ctime` gốc của C (được :func:`time.ctime` gọi, nhưng
   :meth:`datetime.ctime` không gọi) tuân thủ tiêu chuẩn C.


.. method:: datetime.strftime(format)

   Trả về một chuỗi biểu diễn ngày và giờ, được điều khiển bởi một chuỗi định dạng tường minh. Xem thêm :ref:`strftime-strptime-behavior` và :meth:`datetime.isoformat`.


.. method:: datetime.__format__(format)

   Giống như :meth:`.datetime.strftime`. Điều này cho phép chỉ định một chuỗi định dạng cho đối tượng :class:`.datetime` trong :ref:`formatted string literals <f-strings>` và khi sử dụng :meth:`str.format`. Xem thêm :ref:`strftime-strptime-behavior` và :meth:`datetime.isoformat`.


Ví dụ sử dụng: :class:`!datetime`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ví dụ làm việc với các đối tượng :class:`.datetime`:

.. doctest::

    >>> import datetime as dt

    >>> # Sử dụng datetime.combine()
    >>> d = dt.date(2005, 7, 14)
    >>> t = dt.time(12, 30)
    >>> dt.datetime.combine(d, t)
    datetime.datetime(2005, 7, 14, 12, 30)

    >>> # Sử dụng datetime.now()
    >>> dt.datetime.now()   # doctest: +SKIP
    datetime.datetime(2007, 12, 6, 16, 29, 43, 79043)   # GMT +1
    >>> dt.datetime.now(dt.timezone.utc)   # doctest: +SKIP
    datetime.datetime(2007, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc)

    >>> # Sử dụng datetime.strptime()
    >>> my_datetime = dt.datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    >>> my_datetime
    datetime.datetime(2006, 11, 21, 16, 30)

    >>> # Sử dụng datetime.timetuple() để lấy tuple của tất cả thuộc tính
    >>> tt = my_datetime.timetuple()
    >>> for it in tt:   # doctest: +SKIP
    ...     print(it)
    ...
    2006    # năm
    11      # tháng
    21      # ngày
    16      # giờ
    30      # phút
    0       # giây
    1       # ngày trong tuần (0 = Thứ Hai)
    325     # số ngày kể từ ngày 1 tháng 1
    -1      # dst - phương thức tzinfo.dst() trả về None

    >>> # Ngày ở định dạng ISO
    >>> ic = my_datetime.isocalendar()
    >>> for it in ic:   # doctest: +SKIP
    ...     print(it)
    ...
    2006    # Năm ISO
    47      # Tuần ISO
    2       # Ngày trong tuần ISO

    >>> # Định dạng datetime
    >>> my_datetime.strftime("%A, %d. %B %Y %I:%M%p")
    'Tuesday, 21. November 2006 04:30PM'
    >>> 'The {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.'.format(my_datetime, "day", "month", "time")
    'The day is 21, the month is November, the time is 04:30PM.'

Ví dụ dưới đây định nghĩa một lớp con :class:`tzinfo` ghi lại thông tin múi giờ của Kabul, Afghanistan, nơi đã sử dụng UTC+4 cho đến năm 1945 và sau đó là UTC+4:30::

   import datetime as dt

   class KabulTz(dt.tzinfo):
       # Kabul dùng +4 cho đến năm 1945, khi chuyển sang +4:30
       UTC_MOVE_DATE = dt.datetime(1944, 12, 31, 20, tzinfo=dt.timezone.utc)

       def utcoffset(self, when):
           if when.year < 1945:
               return dt.timedelta(hours=4)
           elif (1945, 1, 1, 0, 0) <= when.timetuple()[:5] < (1945, 1, 1, 0, 30):
               # Một khoảng nửa giờ mơ hồ ("tưởng tượng") biểu thị
               # một 'fold' trong thời gian do chuyển từ +4 sang +4:30.
               # Nếu when nằm trong khoảng tưởng tượng, dùng fold để quyết định cách
               # phân giải. Xem PEP 495.
               return dt.timedelta(hours=4, minutes=(30 if when.fold else 0))
           else:
               return dt.timedelta(hours=4, minutes=30)

       def fromutc(self, when):
           # Áp dụng các bước kiểm tra tương tự như trong datetime.tzinfo
           if not isinstance(when, dt.datetime):
               raise TypeError("fromutc() requires a datetime argument")
           if when.tzinfo is not self:
               raise ValueError("when.tzinfo is not self")

           # Cần có một triển khai tùy chỉnh cho fromutc vì
           # đầu vào của hàm này là một datetime với các giá trị utc
           # nhưng tzinfo được đặt thành self.
           # Xem datetime.astimezone hoặc fromtimestamp.
           if when.replace(tzinfo=dt.timezone.utc) >= self.UTC_MOVE_DATE:
               return when + dt.timedelta(hours=4, minutes=30)
           else:
               return when + dt.timedelta(hours=4)

       def dst(self, when):
           # Kabul không áp dụng giờ mùa hè.
           return dt.timedelta(0)

       def tzname(self, when):
           if when >= self.UTC_MOVE_DATE:
               return "+04:30"
           return "+04"

Cách sử dụng ``KabulTz`` ở trên::

   >>> tz1 = KabulTz()

   >>> # Datetime trước khi thay đổi
   >>> dt1 = dt.datetime(1900, 11, 21, 16, 30, tzinfo=tz1)
   >>> print(dt1.utcoffset())
   4:00:00

   >>> # Datetime sau khi thay đổi
   >>> dt2 = dt.datetime(2006, 6, 14, 13, 0, tzinfo=tz1)
   >>> print(dt2.utcoffset())
   4:30:00

   >>> # Chuyển datetime sang múi giờ khác
   >>> dt3 = dt2.astimezone(dt.timezone.utc)
   >>> dt3
   datetime.datetime(2006, 6, 14, 8, 30, tzinfo=datetime.timezone.utc)
   >>> dt2
   datetime.datetime(2006, 6, 14, 13, 0, tzinfo=KabulTz())
   >>> dt2 == dt3
   True


.. _datetime-time:

:class:`!time` đối tượng
------------------------

Một đối tượng :class:`.time` đại diện cho một thời điểm trong ngày (giờ địa phương), độc lập với bất kỳ ngày cụ thể nào và có thể được điều chỉnh thông qua một đối tượng :class:`tzinfo`.

.. class:: time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)

   Tất cả đối số đều là tùy chọn. *tzinfo* có thể là ``None``, hoặc là một thể hiện của một
   :class:`tzinfo` lớp con. Các đối số còn lại phải là số nguyên trong các phạm vi sau:

   * ``0 <= hour < 24``,
   * ``0 <= minute < 60``,
   * ``0 <= second < 60``,
   * ``0 <= microsecond < 1000000``,
   * ``fold in [0, 1]``.

   Nếu cung cấp một đối số nằm ngoài các phạm vi đó, :exc:`ValueError` sẽ được phát sinh. Tất cả đều mặc định là 0, ngoại trừ *tzinfo*, mặc định là ``None``.


Các thuộc tính của lớp:


.. attribute:: time.min

   Thời điểm sớm nhất có thể biểu diễn, :class:`.time`, ``time(0, 0, 0, 0)``.


.. attribute:: time.max

   Thời điểm muộn nhất có thể biểu diễn, :class:`.time`, ``time(23, 59, 59, 999999)``.


.. attribute:: time.resolution

   Khoảng chênh lệch nhỏ nhất có thể có giữa các đối tượng :class:`.time` không bằng nhau, ``timedelta(microseconds=1)``, tuy nhiên lưu ý rằng phép tính số học trên
   các đối tượng :class:`.time` không được hỗ trợ.


Các thuộc tính của instance (chỉ đọc):

.. attribute:: time.hour

   Trong ``range(24)``.


.. attribute:: time.minute

   Trong ``range(60)``.


.. attribute:: time.second

   Trong ``range(60)``.


.. attribute:: time.microsecond

   Trong ``range(1000000)``.


.. attribute:: time.tzinfo

   Đối tượng được truyền làm đối số tzinfo cho hàm khởi tạo :class:`.time`, hoặc ``None`` nếu không truyền đối số này.


.. attribute:: time.fold

   Trong ``[0, 1]``. Được dùng để phân biệt các thời điểm theo giờ địa phương trong một khoảng thời gian lặp lại. (Khoảng thời gian lặp lại xảy ra khi đồng hồ được chỉnh lùi vào cuối giờ tiết kiệm ánh sáng ban ngày hoặc khi độ lệch UTC của múi giờ hiện tại bị giảm vì lý do chính trị.) Các giá trị 0 và 1 lần lượt biểu thị thời điểm sớm hơn và muộn hơn trong hai thời điểm có cùng biểu diễn giờ địa phương.

   .. versionadded:: 3.6


Các đối tượng :class:`.time` hỗ trợ so sánh bằng và so sánh thứ tự, trong đó ``a`` được xem là nhỏ hơn ``b`` khi ``a`` xảy ra trước ``b`` theo thời gian.

Các đối tượng :class:`!time` naive và aware không bao giờ bằng nhau. Việc so sánh thứ tự giữa các đối tượng :class:`!time` naive và aware sẽ phát sinh
:exc:`TypeError`.

Nếu cả hai đối tượng được so sánh đều aware và có cùng thuộc tính :attr:`~.time.tzinfo`, các thuộc tính :attr:`!tzinfo` và :attr:`!fold` sẽ bị bỏ qua và các thời điểm cơ sở được so sánh. Nếu cả hai đối tượng được so sánh đều aware và có các thuộc tính :attr:`!tzinfo` khác nhau, trước tiên các đối tượng được điều chỉnh bằng cách trừ đi độ lệch UTC của chúng (lấy từ ``self.utcoffset()``).

.. versionchanged:: 3.3
  So sánh bằng giữa các thực thể :class:`.time` aware và naive không gây ra :exc:`TypeError`.

Trong các ngữ cảnh Boolean, một đối tượng :class:`.time` luôn được xem là true.

.. versionchanged:: 3.5
   Trước Python 3.5, một đối tượng :class:`.time` được xem là false nếu biểu diễn thời điểm nửa đêm theo UTC. Hành vi này được xem là khó hiểu và dễ gây lỗi, nên đã bị loại bỏ trong Python 3.5. Xem :issue:`13936` để biết thêm thông tin.


Các hàm khởi tạo khác:

.. classmethod:: time.fromisoformat(time_string)

   Trả về một :class:`.time` tương ứng với *time_string* ở bất kỳ định dạng ISO 8601 hợp lệ nào, ngoại trừ các trường hợp sau:

   1. Múi giờ có thể có độ lệch tính bằng số giây phân số.
   2. Ký tự ``T`` ở đầu, thường bắt buộc trong các trường hợp có thể gây nhầm lẫn giữa ngày và giờ, là không bắt buộc.
   3. Phần giây lẻ có thể có bất kỳ số chữ số nào (mọi chữ số vượt quá 6 sẽ bị cắt bỏ).
   4. Không hỗ trợ phần giờ và phút lẻ.

   Ví dụ:

   .. doctest::

       >>> import datetime as dt
       >>> dt.time.fromisoformat('04:23:01')
       datetime.time(4, 23, 1)
       >>> dt.time.fromisoformat('T04:23:01')
       datetime.time(4, 23, 1)
       >>> dt.time.fromisoformat('T042301')
       datetime.time(4, 23, 1)
       >>> dt.time.fromisoformat('04:23:01.000384')
       datetime.time(4, 23, 1, 384)
       >>> dt.time.fromisoformat('04:23:01,000384')
       datetime.time(4, 23, 1, 384)
       >>> dt.time.fromisoformat('04:23:01+04:00')
       datetime.time(4, 23, 1, tzinfo=datetime.timezone(datetime.timedelta(seconds=14400)))
       >>> dt.time.fromisoformat('04:23:01Z')
       datetime.time(4, 23, 1, tzinfo=datetime.timezone.utc)
       >>> dt.time.fromisoformat('04:23:01+00:00')
       datetime.time(4, 23, 1, tzinfo=datetime.timezone.utc)


   .. versionadded:: 3.7
   .. versionchanged:: 3.11
      Trước đây, phương thức này chỉ hỗ trợ các định dạng có thể được tạo ra bởi
      :meth:`time.isoformat`.


.. classmethod:: time.strptime(date_string, format)

   Trả về một :class:`.time` tương ứng với *date_string*, được phân tích theo *format*.

   Nếu *format* không chứa thông tin microsecond hoặc múi giờ, điều này tương đương với::

     time(*(time.strptime(date_string, format)[3:6]))

   :exc:`ValueError` được phát sinh nếu không thể phân tích *date_string* và *format* bằng :func:`time.strptime`, hoặc nếu nó trả về một giá trị không phải là time tuple. Xem thêm :ref:`strftime-strptime-behavior` và
   :meth:`time.fromisoformat`.

   .. versionadded:: 3.14


Các phương thức instance:

.. method:: time.replace(hour=self.hour, minute=self.minute, second=self.second, \
   microsecond=self.microsecond, tzinfo=self.tzinfo, *, fold=0)

   Trả về một :class:`.time` mới với các giá trị giống nhau, nhưng các tham số được chỉ định sẽ được cập nhật. Lưu ý rằng có thể chỉ định ``tzinfo=None`` để tạo một :class:`!time` naive từ một :class:`!time` aware mà không chuyển đổi dữ liệu thời gian.

   Các đối tượng :class:`.time` cũng được generic function hỗ trợ
   :func:`copy.replace`.

   .. versionchanged:: 3.6
      Đã thêm tham số *fold*.


.. method:: time.isoformat(timespec='auto')

   Trả về một chuỗi biểu diễn thời gian theo định dạng ISO 8601, với một trong các dạng sau:

   - ``HH:MM:SS.ffffff``, nếu :attr:`microsecond` khác 0
   - ``HH:MM:SS``, nếu :attr:`microsecond` là 0
   - ``HH:MM:SS.ffffff+HH:MM[:SS[.ffffff]]``, nếu :meth:`utcoffset` không trả về ``None``
   - ``HH:MM:SS+HH:MM[:SS[.ffffff]]``, nếu :attr:`microsecond` là 0 và :meth:`utcoffset` không trả về ``None``

   Đối số tùy chọn *timespec* chỉ định số thành phần bổ sung của thời gian cần đưa vào (mặc định là ``'auto'``). Có thể là một trong các giá trị sau:

   - ``'auto'``: Giống như ``'seconds'`` nếu :attr:`microsecond` là 0, nếu không thì giống như ``'microseconds'``.
   - ``'hours'``: Bao gồm :attr:`hour` ở định dạng ``HH`` gồm hai chữ số.
   - ``'minutes'``: Bao gồm :attr:`hour` và :attr:`minute` ở định dạng ``HH:MM``.
   - ``'seconds'``: Bao gồm :attr:`hour`, :attr:`minute` và :attr:`second` theo định dạng ``HH:MM:SS``.
   - ``'milliseconds'``: Bao gồm thời gian đầy đủ, nhưng cắt phần giây lẻ đến mili giây. Định dạng ``HH:MM:SS.sss``.
   - ``'microseconds'``: Bao gồm thời gian đầy đủ theo định dạng ``HH:MM:SS.ffffff``.

   .. note::

      Các thành phần thời gian bị loại trừ sẽ được cắt bỏ, không được làm tròn.

   :exc:`ValueError` sẽ được phát sinh khi đối số *timespec* không hợp lệ.

   Ví dụ::

      >>> import datetime as dt
      >>> dt.time(hour=12, minute=34, second=56, microsecond=123456).isoformat(timespec='minutes')
      '12:34'
      >>> my_time = dt.time(hour=12, minute=34, second=56, microsecond=0)
      >>> my_time.isoformat(timespec='microseconds')
      '12:34:56.000000'
      >>> my_time.isoformat(timespec='auto')
      '12:34:56'

   .. versionchanged:: 3.6
      Đã thêm tham số *timespec*.


.. method:: time.__str__()

   Đối với một đối tượng time ``t``, ``str(t)`` tương đương với ``t.isoformat()``.


.. method:: time.strftime(format)

   Trả về một chuỗi biểu diễn thời gian, được điều khiển bằng một chuỗi định dạng tường minh. Xem thêm :ref:`strftime-strptime-behavior` và :meth:`time.isoformat`.


.. method:: time.__format__(format)

   Tương tự như :meth:`.time.strftime`. Điều này cho phép chỉ định một chuỗi định dạng cho đối tượng :class:`.time` trong :ref:`formatted string literals <f-strings>` và khi sử dụng :meth:`str.format`. Xem thêm :ref:`strftime-strptime-behavior` và :meth:`time.isoformat`.


.. method:: time.utcoffset()

   Nếu :attr:`.tzinfo` là ``None``, trả về ``None``; nếu không, trả về ``self.tzinfo.utcoffset(None)`` và phát sinh ngoại lệ nếu giá trị sau không trả về ``None`` hoặc một đối tượng :class:`timedelta` có độ lớn nhỏ hơn một ngày.

   .. versionchanged:: 3.7
      Độ lệch UTC không bị giới hạn ở một số phút nguyên.


.. method:: time.dst()

   Nếu :attr:`.tzinfo` là ``None``, trả về ``None``; nếu không, trả về ``self.tzinfo.dst(None)`` và phát sinh ngoại lệ nếu giá trị sau không trả về ``None`` hoặc một đối tượng :class:`timedelta` có độ lớn nhỏ hơn một ngày.

   .. versionchanged:: 3.7
      Độ lệch DST không bị giới hạn ở một số phút nguyên.


.. method:: time.tzname()

   Nếu :attr:`.tzinfo` là ``None``, trả về ``None``; nếu không thì trả về ``self.tzinfo.tzname(None)``, hoặc phát sinh một ngoại lệ nếu giá trị sau không trả về ``None`` hoặc một đối tượng chuỗi.


Ví dụ sử dụng: :class:`!time`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ví dụ làm việc với một đối tượng :class:`.time`::

    >>> import datetime as dt
    >>> class TZ1(dt.tzinfo):
    ...     def utcoffset(self, when):
    ...         return dt.timedelta(hours=1)
    ...     def dst(self, when):
    ...         return dt.timedelta(0)
    ...     def tzname(self, when):
    ...         return "+01:00"
    ...     def  __repr__(self):
    ...         return f"{self.__class__.__name__}()"
    ...
    >>> t = dt.time(12, 10, 30, tzinfo=TZ1())
    >>> t
    datetime.time(12, 10, 30, tzinfo=TZ1())
    >>> t.isoformat()
    '12:10:30+01:00'
    >>> t.dst()
    datetime.timedelta(0)
    >>> t.tzname()
    '+01:00'
    >>> t.strftime("%H:%M:%S %Z")
    '12:10:30 +01:00'
    >>> 'The {} is {:%H:%M}.'.format("time", t)
    'The time is 12:10.'


.. _datetime-tzinfo:

Các đối tượng :class:`!tzinfo`
------------------------------

.. class:: tzinfo()

   Đây là một :term:`abstract base class`, nghĩa là không nên khởi tạo trực tiếp lớp này. Hãy định nghĩa một lớp con của :class:`tzinfo` để nắm bắt thông tin về một múi giờ cụ thể.

   Một thực thể của (một lớp con cụ thể của) :class:`tzinfo` có thể được truyền cho các hàm khởi tạo của các đối tượng :class:`.datetime` và :class:`.time`. Các đối tượng sau xem các thuộc tính của chúng là theo giờ địa phương, còn đối tượng :class:`!tzinfo` hỗ trợ các phương thức cho biết độ lệch của giờ địa phương so với UTC, tên múi giờ và độ lệch DST, tất cả đều dựa trên một đối tượng ngày hoặc giờ được truyền cho chúng.

   Bạn cần tạo một lớp con cụ thể và (ít nhất) cung cấp các triển khai của những phương thức :class:`tzinfo` tiêu chuẩn cần thiết bởi
   các phương thức :class:`.datetime` bạn sử dụng. Mô-đun :mod:`!datetime` cung cấp
   :class:`timezone`, một lớp con cụ thể đơn giản của :class:`!tzinfo`, có thể biểu diễn các múi giờ có độ lệch cố định so với UTC, chẳng hạn như chính UTC hoặc EST và EDT của Bắc Mỹ.

   Yêu cầu đặc biệt đối với việc pickle: Một lớp con :class:`tzinfo` phải có một
   phương thức :meth:`~object.__init__` có thể được gọi mà không cần đối số; nếu không, đối tượng có thể được pickle nhưng có khả năng không thể unpickle lại. Đây là một yêu cầu kỹ thuật có thể được nới lỏng trong tương lai.

   Một lớp con cụ thể của :class:`tzinfo` có thể cần cài đặt các phương thức sau. Chính xác cần những phương thức nào phụ thuộc vào cách sử dụng các đối tượng :class:`tzinfo`
   :mod:`!datetime` các đối tượng. Nếu không chắc chắn, chỉ cần triển khai tất cả chúng.


.. method:: tzinfo.utcoffset(dt)

   Trả về độ lệch của giờ địa phương so với UTC dưới dạng một đối tượng :class:`timedelta` có giá trị dương ở phía đông UTC. Nếu giờ địa phương nằm ở phía tây UTC, giá trị này phải âm.

   Điều này biểu thị độ lệch *tổng cộng* so với UTC; ví dụ: nếu một
   :class:`tzinfo` đối tượng biểu thị cả múi giờ và các điều chỉnh DST,
   :meth:`utcoffset` nên trả về tổng của chúng. Nếu không biết độ lệch UTC, hãy trả về ``None``. Nếu không, giá trị được trả về phải là một đối tượng :class:`timedelta` nằm строго giữa ``-timedelta(hours=24)`` và ``timedelta(hours=24)`` (độ lớn của độ lệch phải nhỏ hơn một ngày). Hầu hết các triển khai của :meth:`utcoffset` có thể sẽ giống như một trong hai dạng sau::

      return CONSTANT                 # lớp có độ lệch cố định
      return CONSTANT + self.dst(dt)  # lớp nhận biết giờ mùa hè

   Nếu :meth:`utcoffset` không trả về ``None``, thì :meth:`dst` cũng không được trả về ``None``.

   Cài đặt mặc định của :meth:`utcoffset` sẽ phát sinh
   :exc:`NotImplementedError`.

   .. versionchanged:: 3.7
      Độ lệch UTC không bị giới hạn ở một số phút nguyên.


.. method:: tzinfo.dst(dt)

   Trả về điều chỉnh giờ mùa hè (DST) dưới dạng một đối tượng :class:`timedelta` hoặc ``None`` nếu không xác định được thông tin DST.

   Trả về ``timedelta(0)`` nếu DST không có hiệu lực. Nếu DST có hiệu lực, trả về độ lệch dưới dạng một đối tượng :class:`timedelta` (xem :meth:`utcoffset` để biết chi tiết). Lưu ý rằng độ lệch DST, nếu có, đã được cộng vào độ lệch UTC do :meth:`utcoffset` trả về, vì vậy không cần tham khảo :meth:`dst` trừ khi bạn muốn lấy riêng thông tin DST. Ví dụ, :meth:`datetime.timetuple` gọi phương thức :meth:`dst` của thuộc tính :attr:`~.datetime.tzinfo` để xác định cách đặt cờ :attr:`~time.struct_time.tm_isdst`, còn :meth:`tzinfo.fromutc` gọi :meth:`dst` để tính đến các thay đổi DST khi chuyển múi giờ.

   Một thực thể *tz* của một lớp con :class:`tzinfo` mô hình hóa cả giờ chuẩn và giờ mùa hè phải nhất quán theo nghĩa sau:

   ``tz.utcoffset(dt) - tz.dst(dt)``

   phải trả về cùng một kết quả cho mọi :class:`.datetime` *dt* có ``dt.tzinfo == tz``. Đối với các lớp con :class:`!tzinfo` hợp lý, biểu thức này cho ra "độ lệch chuẩn" của múi giờ, giá trị này không nên phụ thuộc vào ngày hoặc giờ, mà chỉ phụ thuộc vào vị trí địa lý. Việc triển khai :meth:`datetime.astimezone` dựa trên điều này nhưng không thể phát hiện các vi phạm; lập trình viên có trách nhiệm bảo đảm điều đó. Nếu một lớp con :class:`!tzinfo` không thể bảo đảm điều này, lớp đó có thể ghi đè cách triển khai mặc định của
   :meth:`tzinfo.fromutc` để hoạt động chính xác với :meth:`~.datetime.astimezone` trong mọi trường hợp.

   Hầu hết các cách triển khai :meth:`dst` có lẽ sẽ trông giống như một trong hai cách sau::

      import datetime as dt

      def dst(self, when):
          # lớp fixed-offset: không tính đến DST
          return dt.timedelta(0)

   hoặc::

      import datetime as dt

      def dst(self, when):
          # Mã đặt dston và dstoff thành thời điểm chuyển đổi DST của múi giờ
          # dựa trên when.year đầu vào và được biểu diễn
          # theo giờ địa phương chuẩn.

          if dston <= when.replace(tzinfo=None) < dstoff:
              return dt.timedelta(hours=1)
          else:
              return dt.timedelta(0)

   Triển khai mặc định của :meth:`dst` sẽ phát sinh :exc:`NotImplementedError`.

   .. versionchanged:: 3.7
      Độ lệch DST không bị giới hạn ở số phút nguyên.


.. method:: tzinfo.tzname(dt)

   Trả về tên múi giờ tương ứng với đối tượng :class:`.datetime` *dt*, dưới dạng một chuỗi. Mô-đun :mod:`!datetime` không quy định gì về tên chuỗi, và cũng không yêu cầu tên đó phải mang một ý nghĩa cụ thể nào. Ví dụ, ``"GMT"``, ``"UTC"``, ``"-500"``, ``"-5:00"``, ``"EDT"``, ``"US/Eastern"``, ``"America/New York"`` đều là các giá trị trả về hợp lệ. Trả về ``None`` nếu không biết tên chuỗi. Lưu ý rằng đây là một method thay vì một chuỗi cố định, chủ yếu vì một số lớp con của :class:`tzinfo` có thể muốn trả về các tên khác nhau tùy thuộc vào giá trị cụ thể của *dt* được truyền vào, đặc biệt nếu lớp :class:`!tzinfo` đang tính đến giờ mùa hè.

   Cài đặt mặc định của :meth:`tzname` sẽ raise :exc:`NotImplementedError`.


Các method này được gọi bởi một đối tượng :class:`.datetime` hoặc :class:`.time`, để phản hồi cho các method cùng tên của chúng. Một đối tượng :class:`!datetime` truyền chính nó làm đối số, còn một đối tượng :class:`!time` truyền ``None`` làm đối số. Vì vậy, các method của lớp con :class:`tzinfo` phải sẵn sàng nhận một đối số *dt* có giá trị ``None``, hoặc thuộc lớp :class:`!datetime`.

Khi truyền ``None`` vào, việc quyết định cách phản hồi phù hợp nhất thuộc về người thiết kế lớp. Ví dụ, trả về ``None`` là phù hợp nếu lớp muốn cho biết rằng các đối tượng thời gian không tham gia vào các protocol :class:`tzinfo`. Có thể hữu ích hơn nếu ``utcoffset(None)`` trả về độ lệch UTC tiêu chuẩn, vì không có quy ước nào khác để xác định độ lệch tiêu chuẩn.

Khi một đối tượng :class:`.datetime` được truyền vào để phản hồi cho một method :class:`!datetime`, ``dt.tzinfo`` là cùng một đối tượng với *self*. Các method :class:`tzinfo` có thể dựa vào điều này, trừ khi mã người dùng gọi trực tiếp các method :class:`!tzinfo`. Mục đích là để các method :class:`!tzinfo` diễn giải *dt* là giờ địa phương, và không cần phải quan tâm đến các đối tượng thuộc múi giờ khác.

Còn một method :class:`tzinfo` nữa mà lớp con có thể muốn ghi đè:


.. method:: tzinfo.fromutc(dt)

   Method này được gọi từ cài đặt mặc định của :meth:`datetime.astimezone`. Khi được gọi từ đó, ``dt.tzinfo`` là *self*, và dữ liệu ngày tháng và thời gian của *dt* được xem là biểu thị một thời điểm UTC. Mục đích của :meth:`fromutc` là điều chỉnh dữ liệu ngày tháng và thời gian, rồi trả về một datetime tương đương theo giờ địa phương của *self*.

   Hầu hết các lớp con của :class:`tzinfo` sẽ có thể kế thừa phần triển khai mặc định
   Việc triển khai :meth:`fromutc` có thể xử lý các múi giờ có độ lệch cố định, cũng như các múi giờ tính đến cả giờ chuẩn và giờ mùa hè, và thậm chí xử lý trường hợp thời điểm chuyển đổi DST của loại sau khác nhau giữa các năm. Một ví dụ về múi giờ mà phần triển khai :meth:`fromutc` mặc định có thể không xử lý đúng trong mọi trường hợp là múi giờ có độ lệch chuẩn (so với UTC) phụ thuộc vào ngày và giờ cụ thể được truyền vào; điều này có thể xảy ra vì lý do chính trị. Các phần triển khai mặc định của :meth:`~.datetime.astimezone` và
   :meth:`fromutc` có thể không tạo ra kết quả bạn muốn nếu kết quả đó là một trong những giờ bao quanh thời điểm độ lệch chuẩn thay đổi.

   Bỏ qua mã xử lý các trường hợp lỗi, phần triển khai :meth:`fromutc` mặc định hoạt động như sau::

      import datetime as dt

      def fromutc(self, when):
          # phát sinh lỗi ValueError nếu when.tzinfo không phải là self
          dtoff = when.utcoffset()
          dtdst = when.dst()
          # phát sinh lỗi ValueError nếu dtoff là None hoặc dtdst là None
          delta = dtoff - dtdst  # đây là độ lệch chuẩn của self
          if delta:
              when += delta   # chuyển đổi sang giờ địa phương tiêu chuẩn
              dtdst = when.dst()
              # tăng ValueError nếu dtdst là None
          if dtdst:
              return when + dtdst
          else:
              return when

Trong tệp :download:`tzinfo_examples.py <../includes/tzinfo_examples.py>` sau đây có một số ví dụ về
:class:`tzinfo` lớp:

.. literalinclude:: ../includes/tzinfo_examples.py

Lưu ý rằng mỗi năm có hai thời điểm phát sinh những điểm tinh tế không thể tránh khỏi trong một lớp con :class:`tzinfo` khi xử lý cả giờ tiêu chuẩn và giờ mùa hè, tại các thời điểm chuyển đổi DST. Cụ thể, hãy xét múi giờ miền Đông Hoa Kỳ (UTC -0500), trong đó EDT bắt đầu vào phút ngay sau 1:59 (EST) vào Chủ nhật thứ hai của tháng 3 và kết thúc vào phút ngay sau 1:59 (EDT) vào Chủ nhật đầu tiên của tháng 11::

     UTC   3:MM  4:MM  5:MM  6:MM  7:MM  8:MM
     EST  22:MM 23:MM  0:MM  1:MM  2:MM  3:MM
     EDT  23:MM  0:MM  1:MM  2:MM  3:MM  4:MM

   start  22:MM 23:MM  0:MM  1:MM  3:MM  4:MM

     end  23:MM  0:MM  1:MM  1:MM  2:MM  3:MM

Khi DST bắt đầu (dòng "start"), đồng hồ địa phương nhảy từ 1:59 đến 3:00. Thời gian địa phương có dạng 2:MM thực sự không có ý nghĩa vào ngày đó, vì vậy ``astimezone(Eastern)`` sẽ không trả về kết quả có ``hour == 2`` vào ngày DST bắt đầu. Ví dụ, tại thời điểm chuyển sang giờ mùa hè vào mùa xuân năm 2016, ta nhận được::

    >>> import datetime as dt
    >>> from tzinfo_examples import HOUR, Eastern
    >>> u0 = dt.datetime(2016, 3, 13, 5, tzinfo=dt.timezone.utc)
    >>> for i in range(4):
    ...     u = u0 + i*HOUR
    ...     t = u.astimezone(Eastern)
    ...     print(u.time(), 'UTC =', t.time(), t.tzname())
    ...
    05:00:00 UTC = 00:00:00 EST
    06:00:00 UTC = 01:00:00 EST
    07:00:00 UTC = 03:00:00 EDT
    08:00:00 UTC = 04:00:00 EDT


Khi DST kết thúc (dòng "end"), có một vấn đề còn nghiêm trọng hơn: có một giờ không thể biểu diễn rõ ràng theo giờ địa phương: giờ cuối cùng của giờ mùa hè. Ở miền Đông, đó là các thời điểm có dạng 5:MM UTC vào ngày giờ mùa hè kết thúc. Đồng hồ địa phương nhảy ngược từ 1:59 (giờ mùa hè) về 1:00 (giờ tiêu chuẩn) một lần nữa. Các thời điểm địa phương có dạng 1:MM là không rõ ràng.
:meth:`~.datetime.astimezone` mô phỏng cách hoạt động của đồng hồ địa phương bằng cách ánh xạ hai giờ UTC liền kề vào cùng một giờ địa phương tại thời điểm đó. Trong ví dụ về múi giờ Eastern, các thời điểm UTC có dạng 5:MM và 6:MM đều được ánh xạ thành 1:MM khi chuyển đổi sang Eastern, nhưng các thời điểm sớm hơn có thuộc tính :attr:`~.datetime.fold` được đặt là 0, còn các thời điểm muộn hơn có thuộc tính này được đặt là 1. Ví dụ, tại thời điểm chuyển tiếp lùi giờ vào mùa thu năm 2016, ta có::

    >>> import datetime as dt
    >>> from tzinfo_examples import HOUR, Eastern
    >>> u0 = dt.datetime(2016, 11, 6, 4, tzinfo=dt.timezone.utc)
    >>> for i in range(4):
    ...     u = u0 + i*HOUR
    ...     t = u.astimezone(Eastern)
    ...     print(u.time(), 'UTC =', t.time(), t.tzname(), t.fold)
    ...
    04:00:00 UTC = 00:00:00 EDT 0
    05:00:00 UTC = 01:00:00 EDT 0
    06:00:00 UTC = 01:00:00 EST 1
    07:00:00 UTC = 02:00:00 EST 0

Lưu ý rằng các đối tượng :class:`.datetime` chỉ khác nhau ở giá trị của
thuộc tính :attr:`~.datetime.fold` được xem là bằng nhau trong các phép so sánh.

Các ứng dụng không thể chấp nhận những điểm không rõ ràng về thời gian theo đồng hồ treo tường nên kiểm tra rõ ràng giá trị của thuộc tính :attr:`~.datetime.fold` hoặc tránh sử dụng các đối tượng hybrid
:class:`tzinfo` lớp con; không có điểm không rõ ràng nào khi sử dụng :class:`timezone`, hoặc bất kỳ lớp con :class:`!tzinfo` nào có độ lệch cố định khác (chẳng hạn như một lớp chỉ biểu diễn EST (độ lệch cố định -5 giờ), hoặc chỉ EDT (độ lệch cố định -4 giờ)).

.. seealso::

    :mod:`zoneinfo`
      Mô-đun :mod:`!datetime` có một lớp :class:`timezone` cơ bản (để xử lý các độ lệch tùy ý so với UTC) và thuộc tính :attr:`timezone.utc` của nó (một đối tượng :class:`!timezone` UTC).

      ``zoneinfo`` đưa *cơ sở dữ liệu múi giờ IANA* (còn được gọi là cơ sở dữ liệu Olson) vào Python, và bạn nên sử dụng nó.

   `cơ sở dữ liệu múi giờ IANA <https://www.iana.org/time-zones>`_
      Cơ sở dữ liệu múi giờ (thường được gọi là tz, tzdata hoặc zoneinfo) chứa mã và dữ liệu biểu diễn lịch sử giờ địa phương của nhiều địa điểm tiêu biểu trên toàn cầu. Cơ sở dữ liệu này được cập nhật định kỳ để phản ánh những thay đổi do các cơ quan chính trị thực hiện đối với ranh giới múi giờ, độ lệch UTC và các quy tắc giờ mùa hè.


.. _datetime-timezone:

Các đối tượng :class:`!timezone`
--------------------------------

Lớp :class:`timezone` là một lớp con của :class:`tzinfo`, trong đó mỗi thực thể biểu diễn một múi giờ được xác định bằng độ lệch cố định so với UTC.

Không thể sử dụng các đối tượng của lớp này để biểu diễn thông tin múi giờ tại những địa điểm sử dụng các độ lệch khác nhau vào những ngày khác nhau trong năm hoặc nơi giờ dân sự đã có những thay đổi trong lịch sử.


.. class:: timezone(offset, name=None)

  Đối số *offset* phải được chỉ định dưới dạng một đối tượng :class:`timedelta` biểu diễn chênh lệch giữa giờ địa phương và UTC. Giá trị này phải lớn hơn nghiêm ngặt ``-timedelta(hours=24)`` và nhỏ hơn nghiêm ngặt ``timedelta(hours=24)``; nếu không, :exc:`ValueError` sẽ được phát sinh.

  Đối số *name* là tùy chọn. Nếu được chỉ định, đối số này phải là một chuỗi được sử dụng làm giá trị mà phương thức :meth:`datetime.tzname` trả về.

  .. versionadded:: 3.2

  .. versionchanged:: 3.7
     Độ lệch UTC không bị giới hạn ở một số nguyên phút.


.. method:: timezone.utcoffset(dt)

  Trả về giá trị cố định được chỉ định khi thực thể :class:`timezone` được tạo.

  Đối số *dt* bị bỏ qua. Giá trị trả về là một thực thể :class:`timedelta`, bằng với chênh lệch giữa giờ địa phương và UTC.

  .. versionchanged:: 3.7
     Độ lệch UTC không bị giới hạn ở một số nguyên phút.


.. method:: timezone.tzname(dt)

  Trả về giá trị cố định được chỉ định khi thực thể :class:`timezone` được tạo.

  Nếu *name* không được cung cấp trong hàm khởi tạo, tên được ``tzname(dt)`` trả về sẽ được tạo từ giá trị của ``offset`` như sau. Nếu *offset* là ``timedelta(0)``, tên là "UTC"; nếu không, đó là một chuỗi có định dạng ``UTC±HH:MM``, trong đó ± là dấu của ``offset``, còn HH và MM lần lượt là hai chữ số của ``offset.hours`` và ``offset.minutes``.

  .. versionchanged:: 3.6
     Tên được tạo từ ``offset=timedelta(0)`` giờ đây là ``'UTC'`` thuần túy, không phải ``'UTC+00:00'``.


.. method:: timezone.dst(dt)

  Luôn trả về ``None``.


.. method:: timezone.fromutc(dt)

  Trả về ``dt + offset``. Đối số *dt* phải là một instance aware
  :class:`.datetime`, với ``tzinfo`` được đặt thành ``self``.


Các thuộc tính của class:

.. attribute:: timezone.utc

   Múi giờ UTC, ``timezone(timedelta(0))``.


.. index::
   single: % (percent); datetime format

.. _strftime-strptime-behavior:

Hành vi của :meth:`!strftime` và :meth:`!strptime` hoạt động
------------------------------------------------------------

Các đối tượng :class:`date`, :class:`.datetime` và :class:`.time` đều hỗ trợ phương thức ``strftime(format)``, dùng để tạo một chuỗi biểu thị thời gian theo một chuỗi định dạng được chỉ định rõ ràng.

Ngược lại, :meth:`date.strptime`, :meth:`datetime.strptime` và
Các phương thức lớp :meth:`time.strptime` tạo một đối tượng từ một chuỗi biểu diễn thời gian và một chuỗi định dạng tương ứng.

Bảng dưới đây cung cấp sự so sánh khái quát giữa :meth:`~.datetime.strftime` và :meth:`~.datetime.strptime`:

+------------------+---------------------------------------------------------------+--------------------------------------------------------------------------+
|                  | ``strftime``                                                  | ``strptime``                                                             |
+==================+===============================================================+==========================================================================+
| Cách sử dụng     | Chuyển đổi đối tượng thành chuỗi theo một định dạng nhất định | Phân tích cú pháp một chuỗi thành đối tượng dựa trên định dạng tương ứng |
+------------------+---------------------------------------------------------------+--------------------------------------------------------------------------+
| Loại phương thức | Phương thức instance                                          | Phương thức lớp                                                          |
+------------------+---------------------------------------------------------------+--------------------------------------------------------------------------+
| Chữ ký           | ``strftime(format)``                                          | ``strptime(date_string, format)``                                        |
+------------------+---------------------------------------------------------------+--------------------------------------------------------------------------+


   .. _format-codes:

Mã định dạng của :meth:`!strftime` và :meth:`!strptime`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các phương thức này chấp nhận những mã định dạng có thể dùng để phân tích cú pháp và định dạng ngày tháng::

   >>> import datetime as dt
   >>> dt.datetime.strptime('31/01/22 23:59:59.999999',
   ...                      '%d/%m/%y %H:%M:%S.%f')
   datetime.datetime(2022, 1, 31, 23, 59, 59, 999999)
   >>> _.strftime('%a %d %b %Y, %I:%M%p')
   'Mon 31 Jan 2022, 11:59PM'

Sau đây là danh sách tất cả mã định dạng mà tiêu chuẩn C năm 1989 yêu cầu; các mã này hoạt động trên mọi nền tảng có triển khai C tiêu chuẩn.

+-----------+--------------------------------+------------------------+-------+
| Directive | Meaning                        | Example                | Notes |
+===========+================================+========================+=======+
| ``%a``    | Weekday as locale's            || Sun, Mon, ..., Sat    | \(1)  |
|           | abbreviated name.              |  (en_US);              |       |
|           |                                || So, Mo, ..., Sa       |       |
|           |                                |  (de_DE)               |       |
+-----------+--------------------------------+------------------------+-------+
| ``%A``    | Weekday as locale's full name. || Sunday, Monday, ...,  | \(1)  |
|           |                                |  Saturday (en_US);     |       |
|           |                                || Sonntag, Montag, ..., |       |
|           |                                |  Samstag (de_DE)       |       |
+-----------+--------------------------------+------------------------+-------+
| ``%w``    | Weekday as a decimal number,   | 0, 1, ..., 6           |       |
|           | where 0 is Sunday and 6 is     |                        |       |
|           | Saturday.                      |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%d``    | Day of the month as a          | 01, 02, ..., 31        | \(9)  |
|           | zero-padded decimal number.    |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%b``    | Month as locale's abbreviated  || Jan, Feb, ..., Dec    | \(1)  |
|           | name.                          |  (en_US);              |       |
|           |                                || Jan, Feb, ..., Dez    |       |
|           |                                |  (de_DE)               |       |
+-----------+--------------------------------+------------------------+-------+
| ``%B``    | Month as locale's full name.   || January, February,    | \(1)  |
|           |                                |  ..., December (en_US);|       |
|           |                                || Januar, Februar, ..., |       |
|           |                                |  Dezember (de_DE)      |       |
+-----------+--------------------------------+------------------------+-------+
| ``%m``    | Month as a zero-padded         | 01, 02, ..., 12        | \(9)  |
|           | decimal number.                |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%y``    | Year without century as a      | 00, 01, ..., 99        | \(9)  |
|           | zero-padded decimal number.    |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%Y``    | Year with century as a decimal | 0001, 0002, ..., 2013, | \(2)  |
|           | number.                        | 2014, ..., 9998, 9999  |       |
+-----------+--------------------------------+------------------------+-------+
| ``%H``    | Hour (24-hour clock) as a      | 00, 01, ..., 23        | \(9)  |
|           | zero-padded decimal number.    |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%I``    | Hour (12-hour clock) as a      | 01, 02, ..., 12        | \(9)  |
|           | zero-padded decimal number.    |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%p``    | Locale's equivalent of either  || AM, PM (en_US);       | \(1), |
|           | AM or PM.                      || am, pm (de_DE)        | \(3)  |
+-----------+--------------------------------+------------------------+-------+
| ``%M``    | Minute as a zero-padded        | 00, 01, ..., 59        | \(9)  |
|           | decimal number.                |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%S``    | Second as a zero-padded        | 00, 01, ..., 59        | \(4), |
|           | decimal number.                |                        | \(9)  |
+-----------+--------------------------------+------------------------+-------+
| ``%f``    | Microsecond as a decimal       | 000000, 000001, ...,   | \(5)  |
|           | number, zero-padded to 6       | 999999                 |       |
|           | digits.                        |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%z``    | UTC offset in the form         | (empty), +0000,        | \(6)  |
|           | ``±HHMM[SS[.ffffff]]`` (empty  | -0400, +1030,          |       |
|           | string if the object is        | +063415,               |       |
|           | naive).                        | -030712.345216         |       |
+-----------+--------------------------------+------------------------+-------+
| ``%Z``    | Time zone name (empty string   | (empty), UTC, GMT      | \(6)  |
|           | if the object is naive).       |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%j``    | Day of the year as a           | 001, 002, ..., 366     | \(9)  |
|           | zero-padded decimal number.    |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%U``    | Week number of the year        | 00, 01, ..., 53        | \(7), |
|           | (Sunday as the first day of    |                        | \(9)  |
|           | the week) as a zero-padded     |                        |       |
|           | decimal number. All days in a  |                        |       |
|           | new year preceding the first   |                        |       |
|           | Sunday are considered to be in |                        |       |
|           | week 0.                        |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%W``    | Week number of the year        | 00, 01, ..., 53        | \(7), |
|           | (Monday as the first day of    |                        | \(9)  |
|           | the week) as a zero-padded     |                        |       |
|           | decimal number. All days in a  |                        |       |
|           | new year preceding the first   |                        |       |
|           | Monday are considered to be in |                        |       |
|           | week 0.                        |                        |       |
+-----------+--------------------------------+------------------------+-------+
| ``%c``    | Locale's appropriate date and  || Tue Aug 16 21:30:00   | \(1)  |
|           | time representation.           |  1988 (en_US);         |       |
|           |                                || Di 16 Aug 21:30:00    |       |
|           |                                |  1988 (de_DE)          |       |
+-----------+--------------------------------+------------------------+-------+
| ``%x``    | Locale's appropriate date      || 08/16/88 (None);      | \(1)  |
|           | representation.                || 08/16/1988 (en_US);   |       |
|           |                                || 16.08.1988 (de_DE)    |       |
+-----------+--------------------------------+------------------------+-------+
| ``%X``    | Locale's appropriate time      || 21:30:00 (en_US);     | \(1)  |
|           | representation.                || 21:30:00 (de_DE)      |       |
+-----------+--------------------------------+------------------------+-------+
| ``%%``    | A literal ``'%'`` character.   | %                      |       |
+-----------+--------------------------------+------------------------+-------+

Một số directive bổ sung không được tiêu chuẩn C89 yêu cầu cũng được đưa vào để thuận tiện. Tất cả các tham số này đều tương ứng với các giá trị ngày tháng theo ISO 8601.

+---------+--------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+---------+
| Chỉ thị | Ý nghĩa                                                                                                                  | Ví dụ                                                       | Ghi chú |
+=========+==========================================================================================================================+=============================================================+=========+
| ``%G``  | Năm ISO 8601 có thế kỷ, biểu thị năm chứa phần lớn hơn của tuần ISO (``%V``).                                            | 0001, 0002, ..., 2013,                                      | \(8)    |
|         |                                                                                                                          | 2014, ..., 9998, 9999                                       |         |
+---------+--------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+---------+
| ``%u``  | Ngày trong tuần theo ISO 8601 dưới dạng số thập phân, trong đó 1 là thứ Hai.                                             | 1, 2, ..., 7                                                |         |
+---------+--------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+---------+
| ``%V``  | Tuần theo ISO 8601 dưới dạng số thập phân, với thứ Hai là ngày đầu tiên trong tuần. Tuần 01 là tuần chứa ngày 4 tháng 1. | 01, 02, ..., 53                                             | \(8),   |
|         |                                                                                                                          |                                                             | \(9)    |
+---------+--------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+---------+
| ``%:z`` | Độ lệch UTC dưới dạng ``±HH:MM[:SS[.ffffff]]`` (chuỗi rỗng nếu đối tượng là naive).                                      | (rỗng), +00:00, -04:00, +10:30, +06:34:15, -03:07:12.345216 | \(6)    |
+---------+--------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------+---------+

Các mã này có thể không khả dụng trên mọi nền tảng khi được sử dụng với phương thức :meth:`~.datetime.strftime`. Các chỉ thị về năm ISO 8601 và tuần ISO 8601 không thể thay thế cho các chỉ thị về năm và số tuần ở trên. Việc gọi :meth:`~.datetime.strptime` với các chỉ thị ISO 8601 chưa đầy đủ hoặc không rõ ràng sẽ gây ra :exc:`ValueError`.

Bộ mã định dạng đầy đủ được hỗ trợ sẽ khác nhau tùy nền tảng, vì Python gọi hàm :c:func:`strftime` của thư viện C trên nền tảng đó, và các khác biệt giữa các nền tảng là phổ biến. Để xem toàn bộ mã định dạng được hỗ trợ trên nền tảng của bạn, hãy tham khảo tài liệu :manpage:`strftime(3)`. Cách xử lý các mã định dạng không được hỗ trợ cũng khác nhau giữa các nền tảng.

.. versionadded:: 3.6
   Đã thêm ``%G``, ``%u`` và ``%V``.

.. versionadded:: 3.12
   Đã thêm ``%:z``.


Chi tiết kỹ thuật
^^^^^^^^^^^^^^^^^

Nói chung, ``d.strftime(fmt)`` hoạt động giống như ``time.strftime(fmt, d.timetuple())`` của mô-đun :mod:`time`, mặc dù không phải mọi đối tượng đều hỗ trợ một
phương thức :meth:`~date.timetuple`.

Đối với các phương thức lớp :meth:`.datetime.strptime` và :meth:`.date.strptime`, giá trị mặc định là ``1900-01-01T00:00:00.000``: mọi thành phần không được chỉ định trong chuỗi định dạng sẽ được lấy từ giá trị mặc định.

.. note::
   Các chuỗi định dạng không có dấu phân cách có thể gây mơ hồ khi phân tích cú pháp. Ví dụ, với ``%Y%m%d``, chuỗi ``2026111`` có thể được phân tích cú pháp thành ``2026-11-01`` hoặc ``2026-01-11``. Hãy sử dụng dấu phân cách để đảm bảo dữ liệu đầu vào được phân tích cú pháp theo đúng mục đích.

.. note::
   Khi được dùng để phân tích cú pháp các ngày không đầy đủ, thiếu năm, :meth:`.datetime.strptime` và :meth:`.date.strptime` sẽ phát sinh ngoại lệ khi gặp ngày 29 tháng 2 vì năm mặc định 1900 *không phải* là năm nhuận. Luôn thêm một năm nhuận mặc định vào các chuỗi ngày không đầy đủ trước khi phân tích cú pháp.

.. testsetup::

    # doctest seems to turn the warning into an error which makes it
    # show up and require matching and prevents the actual interesting
    # exception from being raised.
    # Manually apply the catch_warnings context manager
    import warnings
    catch_warnings = warnings.catch_warnings()
    catch_warnings.__enter__()
    warnings.simplefilter("ignore")

.. testcleanup::

    catch_warnings.__exit__()

.. doctest::

    >>> import datetime as dt
    >>> value = "2/29"
    >>> dt.datetime.strptime(value, "%m/%d")
    Traceback (most recent call last):
    ...
    ValueError: day 29 must be in range 1..28 for month 2 in year 1900
    >>> dt.datetime.strptime(f"1904 {value}", "%Y %m/%d")
    datetime.datetime(1904, 2, 29, 0, 0)

Việc sử dụng ``datetime.strptime(date_string, format)`` tương đương với::

  datetime(*(time.strptime(date_string, format)[0:6]))

trừ khi định dạng bao gồm các thành phần nhỏ hơn một giây hoặc thông tin về độ lệch múi giờ; các thành phần này được hỗ trợ trong ``datetime.strptime`` nhưng bị ``time.strptime`` loại bỏ.

Đối với các đối tượng :class:`.time`, không nên sử dụng các mã định dạng cho năm, tháng và ngày, vì các đối tượng :class:`!time` không có những giá trị này. Nếu vẫn sử dụng, 1900 sẽ được thay thế cho năm, còn 1 được thay thế cho tháng và ngày.

Đối với các đối tượng :class:`date`, không nên sử dụng các mã định dạng cho giờ, phút, giây và microgiây, vì các đối tượng :class:`date` không có những giá trị này. Nếu vẫn sử dụng, 0 sẽ được thay thế cho các giá trị đó.

Vì cùng lý do, việc xử lý các chuỗi định dạng chứa các điểm mã Unicode không thể được biểu diễn trong charset của locale hiện tại cũng phụ thuộc vào nền tảng. Trên một số nền tảng, các điểm mã đó được giữ nguyên trong đầu ra, trong khi trên các nền tảng khác, ``strftime`` có thể phát sinh :exc:`UnicodeError` hoặc thay vào đó trả về một chuỗi rỗng.

Lưu ý:

(1)
   Vì định dạng phụ thuộc vào locale hiện tại, cần thận trọng khi đưa ra giả định về giá trị đầu ra. Thứ tự các trường sẽ thay đổi (ví dụ: "month/day/year" so với "day/month/year"), và đầu ra có thể chứa các ký tự không phải ASCII.

(2)
   Phương thức :meth:`~.datetime.strptime` có thể phân tích cú pháp các năm trong toàn bộ phạm vi [1, 9999], nhưng các năm < 1000 phải được điền số 0 để đạt độ rộng 4 chữ số.

   .. versionchanged:: 3.2
      Trong các phiên bản trước, phương thức :meth:`~.datetime.strftime` bị giới hạn ở các năm >= 1900.

   .. versionchanged:: 3.3
      Trong phiên bản 3.2, phương thức :meth:`~.datetime.strftime` chỉ áp dụng cho các năm >= 1000.

(3)
   Khi được sử dụng với phương thức :meth:`~.datetime.strptime`, directive ``%p`` chỉ ảnh hưởng đến trường giờ đầu ra nếu directive ``%I`` được sử dụng để phân tích giờ.

(4)
   Không giống module :mod:`time`, module :mod:`!datetime` không hỗ trợ giây nhuận.

(5)
   Khi được sử dụng với phương thức :meth:`~.datetime.strptime`, directive ``%f`` chấp nhận từ một đến sáu chữ số và bổ sung số 0 ở bên phải. ``%f`` là phần mở rộng của tập ký tự định dạng trong tiêu chuẩn C (nhưng được triển khai riêng trong các đối tượng datetime, vì vậy luôn khả dụng).

(6)
   Đối với một đối tượng naive, các mã định dạng ``%z``, ``%:z`` và ``%Z`` được thay thế bằng các chuỗi rỗng.

   Đối với một đối tượng aware:

   ``%z``
      :meth:`~.datetime.utcoffset` được chuyển đổi thành một chuỗi có dạng ``±HHMM[SS[.ffffff]]``, trong đó ``HH`` là một chuỗi gồm 2 chữ số biểu thị số giờ của độ lệch UTC, ``MM`` là một chuỗi gồm 2 chữ số biểu thị số phút của độ lệch UTC, ``SS`` là một chuỗi gồm 2 chữ số biểu thị số giây của độ lệch UTC và ``ffffff`` là một chuỗi gồm 6 chữ số biểu thị số microgiây của độ lệch UTC. Phần ``ffffff`` được lược bỏ khi độ lệch là một số nguyên giây, và cả phần ``ffffff`` lẫn ``SS`` đều được lược bỏ khi độ lệch là một số nguyên phút. Ví dụ, nếu
      :meth:`~.datetime.utcoffset` trả về ``timedelta(hours=-3, minutes=-30)``, ``%z`` được thay thế bằng chuỗi ``'-0330'``.

   .. versionchanged:: 3.7
      Độ lệch UTC không bị giới hạn ở một số phút nguyên.

   .. versionchanged:: 3.7
      Khi chỉ thị ``%z`` được cung cấp cho phương thức :meth:`~.datetime.strptime`, độ lệch UTC có thể có dấu hai chấm làm dấu phân cách giữa giờ, phút và giây. Ví dụ: ``'+01:00:00'`` sẽ được phân tích cú pháp thành độ lệch một giờ. Ngoài ra, việc cung cấp ``'Z'`` tương đương với ``'+00:00'``.

   ``%:z``
      Hoạt động hoàn toàn giống như ``%z``, nhưng có thêm dấu hai chấm làm dấu phân cách giữa giờ, phút và giây.

   ``%Z``
      Trong :meth:`~.datetime.strftime`, ``%Z`` được thay thế bằng một chuỗi rỗng nếu
      :meth:`~.datetime.tzname` trả về ``None``; nếu không, ``%Z`` được thay thế bằng giá trị trả về, giá trị này phải là một chuỗi.

      :meth:`~.datetime.strptime` chỉ chấp nhận một số giá trị nhất định cho ``%Z``:

      1. bất kỳ giá trị nào trong ``time.tzname`` cho locale của máy bạn
      2. các giá trị được hard-code ``UTC`` và ``GMT``

      Vì vậy, một người sống ở Nhật Bản có thể có ``JST``, ``UTC`` và ``GMT`` là các giá trị hợp lệ, nhưng có lẽ không phải ``EST``. Giá trị không hợp lệ sẽ gây ra ``ValueError``.

   .. versionchanged:: 3.2
      Khi chỉ thị ``%z`` được cung cấp cho phương thức :meth:`~.datetime.strptime`, một đối tượng :class:`.datetime` aware sẽ được tạo ra. ``tzinfo`` của kết quả sẽ được đặt thành một instance :class:`timezone`.

(7)
   Khi được sử dụng với phương thức :meth:`~.datetime.strptime`, ``%U`` và ``%W`` chỉ được dùng trong các phép tính khi ngày trong tuần và năm theo lịch (``%Y``) được chỉ định.

(8)
   Tương tự như ``%U`` và ``%W``, ``%V`` chỉ được dùng trong các phép tính khi ngày trong tuần và năm ISO (``%G``) được chỉ định trong một
   chuỗi định dạng :meth:`~.datetime.strptime`. Cũng lưu ý rằng ``%G`` và ``%Y`` không thể thay thế cho nhau.

(9)
   Khi được sử dụng với phương thức :meth:`~.datetime.strptime`, số 0 ở đầu là tùy chọn đối với các định dạng ``%d``, ``%m``, ``%H``, ``%I``, ``%M``, ``%S``, ``%j``, ``%U``, ``%W`` và ``%V``. Định dạng ``%y`` yêu cầu phải có số 0 ở đầu.

(10)
   Khi phân tích tháng và ngày bằng :meth:`~.datetime.strptime`, luôn đưa năm vào định dạng. Nếu giá trị bạn cần phân tích không có năm, hãy thêm một năm nhuận giả rõ ràng. Nếu không, mã của bạn sẽ phát sinh ngoại lệ khi gặp ngày nhuận vì năm mặc định mà trình phân tích sử dụng (1900) không phải là năm nhuận. Người dùng gặp lỗi này vào mỗi năm nhuận.

   .. doctest::

      >>> month_day = "02/29"
      >>> dt.datetime.strptime(f"{month_day};1984", "%m/%d;%Y")  # Không có lỗi năm nhuận.
      datetime.datetime(1984, 2, 29, 0, 0)

   .. deprecated-removed:: 3.13 3.15
      :meth:`~.datetime.strptime` calls using a format string containing
      một ngày trong tháng không có năm giờ sẽ phát ra một
      :exc:`DeprecationWarning`. Trong phiên bản 3.15 trở lên, chúng tôi có thể thay đổi điều này thành một lỗi hoặc thay đổi năm mặc định thành một năm nhuận. Xem :gh:`70647`.

.. rubric:: Chú thích cuối trang

.. [#] Nói cách khác, nếu bỏ qua các tác động của thuyết tương đối.

.. [#] Điều này phù hợp với định nghĩa về lịch "proleptic Gregorian" trong cuốn sách *Calendrical Calculations* của Dershowitz và Reingold, trong đó đây là lịch cơ sở cho mọi phép tính. Hãy xem cuốn sách để biết các thuật toán chuyển đổi giữa số thứ tự theo lịch proleptic Gregorian và nhiều hệ lịch khác.

.. [#] Hãy xem `hướng dẫn về toán học của lịch ISO 8601 <https://web.archive.org/web/20220531051136/https://webspace.science.uu.nl/~gent0113/calendar/isocalendar.htm>`_ do R. H. van Gent biên soạn để có lời giải thích dễ hiểu.

.. _`dateutil`: https://dateutil.readthedocs.io/en/stable/
.. _`IANA time zone database`: https://www.iana.org/time-zones
.. _`guide to the mathematics of the ISO 8601 calendar`: https://web.archive.org/web/20220531051136/https://webspace.science.uu.nl/~gent0113/calendar/isocalendar.htm
