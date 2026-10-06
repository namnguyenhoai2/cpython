:mod:`!calendar` --- Các hàm chung liên quan đến lịch
=====================================================

.. module:: calendar
   :synopsis: Các hàm dùng để làm việc với lịch, bao gồm một số chức năng mô phỏng chương trình cal của Unix.

.. sectionauthor:: Drew Csillag <drew_csillag@geocities.com>

**Mã nguồn:** :source:`Lib/calendar.py`

--------------

Mô-đun này cho phép bạn xuất lịch giống như chương trình :program:`cal` của Unix và cung cấp thêm các hàm hữu ích liên quan đến lịch. Theo mặc định, các lịch này có thứ Hai là ngày đầu tuần và Chủ nhật là ngày cuối tuần (theo quy ước châu Âu). Sử dụng :func:`setfirstweekday` để đặt ngày đầu tuần là Chủ nhật (6) hoặc bất kỳ ngày nào khác trong tuần. Các tham số chỉ định ngày tháng được cung cấp dưới dạng số nguyên. Để biết các chức năng liên quan, hãy xem thêm các mô-đun :mod:`datetime` và :mod:`time`.

Các hàm và lớp được định nghĩa trong mô-đun này sử dụng một lịch lý tưởng hóa, tức lịch Gregory hiện tại được mở rộng vô hạn theo cả hai hướng. Điều này phù hợp với định nghĩa về lịch "Gregory suy diễn" (proleptic Gregorian) trong cuốn sách "Calendrical Calculations" của Dershowitz và Reingold, trong đó đây là lịch cơ sở cho mọi phép tính. Các năm bằng không và âm được diễn giải theo quy định của tiêu chuẩn ISO 8601. Năm 0 là năm 1 trước Công nguyên, năm -1 là năm 2 trước Công nguyên, v.v.


.. class:: Calendar(firstweekday=0)

   Tạo một đối tượng :class:`Calendar`. *firstweekday* là một số nguyên chỉ định ngày đầu tuần. :const:`MONDAY` là ``0`` (mặc định), :const:`SUNDAY` là ``6``.

   Một đối tượng :class:`Calendar` cung cấp một số phương thức có thể được sử dụng để chuẩn bị dữ liệu lịch cho việc định dạng. Bản thân lớp này không thực hiện bất kỳ việc định dạng nào. Đây là nhiệm vụ của các lớp con.


   Các instance của :class:`Calendar` có các phương thức và thuộc tính sau:

   .. attribute:: firstweekday

      Ngày đầu tiên trong tuần dưới dạng số nguyên (0--6).

      Bạn cũng có thể đặt và đọc thuộc tính này bằng cách sử dụng
      :meth:`~Calendar.setfirstweekday` và
      :meth:`~Calendar.getfirstweekday` tương ứng.

   .. method:: getfirstweekday()

      Trả về một :class:`int` cho ngày đầu tiên trong tuần hiện tại (0--6).

      Tương đương với việc đọc thuộc tính :attr:`~Calendar.firstweekday`.

   .. method:: setfirstweekday(firstweekday)

      Đặt ngày đầu tiên trong tuần thành *firstweekday*, được truyền dưới dạng :class:`int` (0--6).

      Tương đương với việc thiết lập thuộc tính :attr:`~Calendar.firstweekday`.

   .. method:: iterweekdays()

      Trả về một iterator cho các số thứ trong tuần sẽ được sử dụng trong một tuần. Giá trị đầu tiên từ iterator sẽ giống với giá trị của thuộc tính :attr:`~Calendar.firstweekday`.


   .. method:: itermonthdates(year, month)

      Trả về một iterator cho tháng *month* (1--12) trong năm *year*. Iterator này sẽ trả về tất cả các ngày (dưới dạng đối tượng :class:`datetime.date`) trong tháng, cùng với tất cả các ngày trước khi tháng bắt đầu hoặc sau khi tháng kết thúc cần thiết để tạo thành một tuần đầy đủ.


   .. method:: itermonthdays(year, month)

      Trả về một iterator cho tháng *month* trong năm *year* tương tự như
      :meth:`itermonthdates`, nhưng không bị giới hạn bởi phạm vi :class:`datetime.date`. Các ngày được trả về chỉ đơn giản là số ngày trong tháng. Đối với những ngày nằm ngoài tháng được chỉ định, số ngày là ``0``.


   .. method:: itermonthdays2(year, month)

      Trả về một iterator cho tháng *month* trong năm *year* tương tự như
      :meth:`itermonthdates`, nhưng không bị giới hạn bởi phạm vi :class:`datetime.date`. Các ngày được trả về sẽ là các tuple gồm số ngày trong tháng và số thứ trong tuần.


   .. method:: itermonthdays3(year, month)

      Trả về một iterator cho tháng *month* trong năm *year* tương tự như
      :meth:`itermonthdates`, nhưng không bị giới hạn bởi phạm vi :class:`datetime.date`. Các ngày được trả về sẽ là các tuple gồm số năm, số tháng và số ngày trong tháng.

      .. versionadded:: 3.7


   .. method:: itermonthdays4(year, month)

      Trả về một iterator cho tháng *month* trong năm *year* tương tự như
      :meth:`itermonthdates`, nhưng không bị giới hạn bởi phạm vi :class:`datetime.date`. Các ngày được trả về sẽ là các tuple gồm số năm, số tháng, số ngày trong tháng và số thứ trong tuần.

      .. versionadded:: 3.7


   .. method:: monthdatescalendar(year, month)

      Trả về danh sách các tuần trong tháng *month* của *year* dưới dạng các tuần đầy đủ. Mỗi tuần là một danh sách gồm bảy đối tượng :class:`datetime.date`.


   .. method:: monthdays2calendar(year, month)

      Trả về danh sách các tuần trong tháng *month* của *year* dưới dạng các tuần đầy đủ. Mỗi tuần là một danh sách gồm bảy tuple chứa số ngày và số thứ trong tuần.


   .. method:: monthdayscalendar(year, month)

      Trả về danh sách các tuần trong *tháng* của *năm* dưới dạng các tuần đầy đủ. Các tuần là danh sách gồm bảy số ngày.


   .. method:: yeardatescalendar(year, width=3)

      Trả về dữ liệu của năm được chỉ định, sẵn sàng để định dạng. Giá trị trả về là danh sách các hàng tháng. Mỗi hàng tháng chứa tối đa *width* tháng (mặc định là 3). Mỗi tháng chứa từ 4 đến 6 tuần và mỗi tuần chứa từ 1--7 ngày. Các ngày là các đối tượng :class:`datetime.date`.


   .. method:: yeardays2calendar(year, width=3)

      Trả về dữ liệu của năm được chỉ định, sẵn sàng để định dạng (tương tự như
      :meth:`yeardatescalendar`). Các phần tử trong danh sách tuần là các tuple gồm số ngày và số thứ trong tuần. Các số ngày nằm ngoài tháng này có giá trị bằng không.


   .. method:: yeardayscalendar(year, width=3)

      Trả về dữ liệu của năm được chỉ định, sẵn sàng để định dạng (tương tự như
      :meth:`yeardatescalendar`). Các phần tử trong danh sách tuần là các số ngày. Các số ngày nằm ngoài tháng này có giá trị bằng không.


.. class:: TextCalendar(firstweekday=0)

   Có thể sử dụng lớp này để tạo lịch dạng văn bản thuần túy.

   Các instance của :class:`TextCalendar` có các phương thức sau:


   .. method:: formatday(theday, weekday, width)

      Trả về một chuỗi biểu diễn một ngày đơn lẻ được định dạng với *width* đã cho. Nếu *theday* là ``0``, trả về một chuỗi gồm các khoảng trắng với độ rộng được chỉ định, biểu thị một ngày trống. Tham số *weekday* không được sử dụng.

   .. method:: formatweek(theweek, w=0)

      Trả về một tuần dưới dạng chuỗi không có ký tự xuống dòng. Nếu cung cấp *w*, tham số này chỉ định độ rộng của các cột ngày, được căn giữa. Phụ thuộc vào ngày đầu tuần được chỉ định trong hàm khởi tạo hoặc được đặt bởi
      :meth:`setfirstweekday` phương thức.


   .. method:: formatweekday(weekday, width)

      Trả về một chuỗi biểu diễn tên của một ngày trong tuần được định dạng theo *width* đã chỉ định. Tham số *weekday* là một số nguyên biểu diễn ngày trong tuần, trong đó ``0`` là thứ Hai và ``6`` là Chủ nhật.


   .. method:: formatweekheader(width)

      Trả về một chuỗi chứa hàng tiêu đề gồm tên các ngày trong tuần, được định dạng với *width* đã cho cho mỗi cột. Tên phụ thuộc vào cài đặt locale và được đệm đến độ rộng đã chỉ định.


   .. method:: formatmonth(theyear, themonth, w=0, l=0)

      Trả về lịch của một tháng dưới dạng chuỗi nhiều dòng. Nếu cung cấp *w*, tham số này chỉ định độ rộng của các cột ngày, được căn giữa. Nếu chỉ định *l*, tham số này chỉ định số dòng mà mỗi tuần sẽ sử dụng. Phụ thuộc vào ngày đầu tuần được chỉ định trong hàm khởi tạo hoặc được đặt bởi
      :meth:`setfirstweekday` phương thức.


   .. method:: formatmonthname(theyear, themonth, width=0, withyear=True)

      Trả về một chuỗi biểu diễn tên tháng được căn giữa trong *width* đã chỉ định. Nếu *withyear* là ``True``, hãy đưa năm vào kết quả. Các tham số *theyear* và *themonth* lần lượt chỉ định năm và tháng dùng để định dạng tên.


   .. method:: prmonth(theyear, themonth, w=0, l=0)

      In lịch của một tháng như được trả về bởi :meth:`formatmonth`.


   .. method:: formatyear(theyear, w=2, l=1, c=6, m=3)

      Trả về lịch *m* cột cho cả năm dưới dạng chuỗi nhiều dòng. Các tham số tùy chọn *w*, *l* và *c* lần lượt dùng để chỉ định độ rộng cột ngày, số dòng mỗi tuần và số khoảng trắng giữa các cột tháng. Phụ thuộc vào ngày đầu tiên trong tuần được chỉ định trong hàm khởi tạo hoặc được thiết lập bởi
      :meth:`setfirstweekday` phương thức. Năm sớm nhất mà lịch có thể được tạo phụ thuộc vào nền tảng.


   .. method:: pryear(theyear, w=2, l=1, c=6, m=3)

      In lịch của cả năm như được trả về bởi :meth:`formatyear`.


.. class:: HTMLCalendar(firstweekday=0)

   Có thể sử dụng lớp này để tạo lịch HTML.


   Các instance của :class:`!HTMLCalendar` có những phương thức sau:

   .. method:: formatmonth(theyear, themonth, withyear=True)

      Trả về lịch của một tháng dưới dạng bảng HTML. Nếu *withyear* là true, năm sẽ được đưa vào tiêu đề; nếu không, chỉ tên tháng được sử dụng.


   .. method:: formatyear(theyear, width=3)

      Trả về lịch của một năm dưới dạng bảng HTML. *width* (mặc định là 3) chỉ định số tháng trên mỗi hàng.


   .. method:: formatyearpage(theyear, width=3, css='calendar.css', encoding=None)

      Trả về lịch của một năm dưới dạng một trang HTML hoàn chỉnh. *width* (mặc định là
      3) chỉ định số tháng trên mỗi hàng. *css* là tên của bảng định kiểu xếp tầng sẽ được sử dụng.
      :const:`None` có thể được truyền vào nếu không muốn sử dụng bảng định kiểu nào. *encoding* chỉ định encoding sẽ được sử dụng cho đầu ra (mặc định là encoding mặc định của hệ thống).


   .. method:: formatmonthname(theyear, themonth, withyear=True)

      Trả về tên một tháng dưới dạng một hàng trong bảng HTML. Nếu *withyear* là true, năm sẽ được đưa vào hàng; nếu không, chỉ tên tháng được sử dụng.


   :class:`!HTMLCalendar` có các thuộc tính sau mà bạn có thể ghi đè để tùy chỉnh các lớp CSS được sử dụng bởi lịch:

   .. attribute:: cssclasses

      Danh sách các lớp CSS được sử dụng cho từng ngày trong tuần. Danh sách lớp mặc định là::

         cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

      có thể thêm các kiểu khác cho từng ngày::

         cssclasses = ["mon text-bold", "tue", "wed", "thu", "fri", "sat", "sun red"]

      Lưu ý rằng danh sách này phải có bảy phần tử.


   .. attribute:: cssclass_noday

      Lớp CSS cho một ngày trong tuần thuộc tháng trước hoặc tháng kế tiếp.

      .. versionadded:: 3.7


   .. attribute:: cssclasses_weekday_head

      Danh sách các lớp CSS được sử dụng cho tên các ngày trong tuần ở hàng tiêu đề. Mặc định giống với :attr:`cssclasses`.

      .. versionadded:: 3.7


   .. attribute:: cssclass_month_head

      Lớp CSS tiêu đề tháng (được :meth:`formatmonthname` sử dụng). Giá trị mặc định là ``"month"``.

      .. versionadded:: 3.7


   .. attribute:: cssclass_month

      Lớp CSS cho toàn bộ bảng của tháng (được :meth:`formatmonth` sử dụng). Giá trị mặc định là ``"month"``.

      .. versionadded:: 3.7


   .. attribute:: cssclass_year

      Lớp CSS cho toàn bộ bảng gồm các bảng của năm (được sử dụng bởi
      :meth:`formatyear`). Giá trị mặc định là ``"year"``.

      .. versionadded:: 3.7


   .. attribute:: cssclass_year_head

      Lớp CSS cho phần đầu bảng của toàn bộ năm (được sử dụng bởi
      :meth:`formatyear`). Giá trị mặc định là ``"year"``.

      .. versionadded:: 3.7


   Lưu ý rằng mặc dù cách đặt tên cho các thuộc tính lớp được mô tả ở trên là dạng số ít (ví dụ: ``cssclass_month`` ``cssclass_noday``), bạn có thể thay thế một lớp CSS duy nhất bằng danh sách các lớp CSS được phân tách bằng dấu cách, chẳng hạn như::

         "text-bold text-red"

   Sau đây là ví dụ về cách tùy chỉnh :class:`!HTMLCalendar`::

       class CustomHTMLCal(calendar.HTMLCalendar):
           cssclasses = [style + " text-nowrap" for style in
                         calendar.HTMLCalendar.cssclasses]
           cssclass_month_head = "text-center month-head"
           cssclass_month = "text-center month"
           cssclass_year = "text-italic lead"


.. class:: LocaleTextCalendar(firstweekday=0, locale=None)

   Lớp con này của :class:`TextCalendar` có thể nhận tên locale trong hàm khởi tạo và sẽ trả về tên các tháng và ngày trong tuần theo locale được chỉ định.


.. class:: LocaleHTMLCalendar(firstweekday=0, locale=None)

   Lớp con này của :class:`HTMLCalendar` có thể nhận tên locale trong hàm khởi tạo và sẽ trả về tên các tháng và ngày trong tuần theo locale được chỉ định.

.. note::

   Hàm khởi tạo cùng các phương thức :meth:`!formatweekday` và :meth:`!formatmonthname` của hai lớp này tạm thời thay đổi locale ``LC_TIME`` thành *locale*. Vì locale hiện tại là một thiết lập áp dụng trên toàn bộ process, chúng không an toàn khi sử dụng trong thread.


Đối với các lịch dạng văn bản đơn giản, module này cung cấp các hàm sau.

.. function:: setfirstweekday(firstweekday)

   Đặt ngày trong tuần (``0`` là thứ Hai, ``6`` là Chủ nhật) làm ngày bắt đầu mỗi tuần. Các giá trị :const:`MONDAY`, :const:`TUESDAY`, :const:`WEDNESDAY`, :const:`THURSDAY`,
   :const:`FRIDAY`, :const:`SATURDAY` và :const:`SUNDAY` được cung cấp để thuận tiện. Ví dụ, để đặt Chủ nhật là ngày đầu tiên trong tuần::

      import calendar
      calendar.setfirstweekday(calendar.SUNDAY)


.. function:: firstweekday()

   Trả về thiết lập hiện tại cho ngày bắt đầu mỗi tuần.


.. function:: isleap(year)

   Trả về :const:`True` nếu *year* là năm nhuận, nếu không thì trả về :const:`False`.


.. function:: leapdays(y1, y2)

   Trả về số năm nhuận trong phạm vi từ *y1* đến *y2* (không bao gồm), trong đó *y1* và *y2* là các năm.

   Hàm này hoạt động với các phạm vi bao gồm thời điểm chuyển sang thế kỷ mới.


.. function:: weekday(year, month, day)

   Trả về ngày trong tuần (``0`` là thứ Hai) của *year* (``1970``--...), *month* (``1``--``12``), *day* (``1``--``31``).


.. function:: weekheader(width)

   Trả về phần tiêu đề chứa tên viết tắt của các ngày trong tuần. *width* chỉ định độ rộng tính bằng ký tự của một ngày trong tuần.


.. function:: monthrange(year, month)

   Trả về ngày trong tuần của ngày đầu tiên trong tháng và số ngày trong tháng, cho *year* và *month* đã chỉ định.


.. function:: monthcalendar(year, month)

   Trả về một ma trận biểu diễn lịch của một tháng. Mỗi hàng biểu diễn một tuần; các ngày nằm ngoài tháng được biểu diễn bằng số 0. Mỗi tuần bắt đầu từ thứ Hai, trừ khi được thiết lập bởi :func:`setfirstweekday`.


.. function:: prmonth(theyear, themonth, w=0, l=0)

   In lịch của một tháng như được trả về bởi :func:`month`.


.. function:: month(theyear, themonth, w=0, l=0)

   Trả về lịch của một tháng dưới dạng chuỗi nhiều dòng bằng :meth:`~TextCalendar.formatmonth` của lớp :class:`TextCalendar`.


.. function:: prcal(theyear, w=0, l=0, c=6, m=3)

   In lịch của cả một năm như được trả về bởi :func:`calendar`.


.. function:: calendar(theyear, w=2, l=1, c=6, m=3)

   Trả về lịch 3 cột của cả một năm dưới dạng chuỗi nhiều dòng bằng :meth:`~TextCalendar.formatyear` của lớp :class:`TextCalendar`.


.. function:: timegm(tuple)

   Đây là một hàm tiện dụng nhưng không liên quan, nhận một tuple thời gian như tuple được trả về bởi hàm :func:`~time.gmtime` trong module :mod:`time`, rồi trả về giá trị Unix timestamp tương ứng, với giả định epoch là năm 1970 và sử dụng mã hóa POSIX. Trên thực tế, :func:`time.gmtime` và :func:`timegm` là hàm nghịch đảo của nhau.


Module :mod:`!calendar` xuất các thuộc tính dữ liệu sau:

.. data:: day_name

   Một dãy biểu diễn các ngày trong tuần theo locale hiện tại, trong đó thứ Hai là ngày số 0.

       >>> import calendar
       >>> list(calendar.day_name)
       ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


.. data:: day_abbr

   Một chuỗi biểu diễn các ngày trong tuần được viết tắt theo locale hiện tại, trong đó Mon là ngày số 0.

       >>> import calendar
       >>> list(calendar.day_abbr)
       ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

.. data:: MONDAY
          TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY

   Các bí danh cho các ngày trong tuần, trong đó ``MONDAY`` là ``0`` và ``SUNDAY`` là ``6``.

   .. versionadded:: 3.12


.. class:: Day

   Kiểu liệt kê xác định các ngày trong tuần dưới dạng các hằng số số nguyên. Các thành viên của kiểu liệt kê này được xuất vào phạm vi module dưới dạng
   :data:`MONDAY` đến :data:`SUNDAY`.

   .. versionadded:: 3.12


.. data:: month_name

   Một chuỗi biểu diễn các tháng trong năm theo locale hiện tại. Chuỗi này tuân theo quy ước thông thường, trong đó January là tháng số 1, vì vậy có độ dài là 13 và ``month_name[0]`` là chuỗi rỗng.

       >>> import calendar
       >>> list(calendar.month_name)
       ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


.. data:: month_abbr

   Một chuỗi biểu diễn các tháng trong năm được viết tắt theo locale hiện tại. Chuỗi này tuân theo quy ước thông thường, trong đó January là tháng số 1, vì vậy có độ dài là 13 và ``month_abbr[0]`` là chuỗi rỗng.

       >>> import calendar
       >>> list(calendar.month_abbr)
       ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

.. data:: JANUARY
          THÁNG HAI THÁNG BA THÁNG TƯ THÁNG NĂM THÁNG SÁU THÁNG BẢY THÁNG TÁM THÁNG CHÍN THÁNG MƯỜI THÁNG MƯỜI MỘT THÁNG MƯỜI HAI

   Các bí danh cho các tháng trong năm, trong đó ``JANUARY`` là ``1`` và ``DECEMBER`` là ``12``.

   .. versionadded:: 3.12


.. class:: Month

   Enumeration định nghĩa các tháng trong năm dưới dạng các hằng số số nguyên. Các thành viên của enumeration này được xuất vào phạm vi module dưới dạng
   :data:`JANUARY` đến :data:`DECEMBER`.

   .. versionadded:: 3.12


Module :mod:`!calendar` định nghĩa các ngoại lệ sau:

.. exception:: IllegalMonthError(month)

   Một lớp con của :exc:`ValueError` và :exc:`IndexError`, được phát sinh khi số tháng đã cho nằm ngoài phạm vi 1-12 (bao gồm cả hai đầu mút).

   .. versionchanged:: 3.12
      :exc:`IllegalMonthError` is now also a subclass of
      :exc:`ValueError`. New code should avoid catching
      :exc:`IndexError`.

   .. attribute:: month

      Số tháng không hợp lệ.


.. exception:: IllegalWeekdayError(weekday)

   Một lớp con của :exc:`ValueError`, được phát sinh khi số thứ tự ngày trong tuần đã cho nằm ngoài phạm vi từ 0 đến 6 (bao gồm cả hai đầu).

   .. attribute:: weekday

      Số thứ tự ngày trong tuần không hợp lệ.


.. seealso::

   Mô-đun :mod:`datetime`
      Giao diện hướng đối tượng dành cho ngày và giờ với chức năng tương tự như
      mô-đun :mod:`time`.

   Mô-đun :mod:`time`
      Các hàm cấp thấp liên quan đến thời gian.


.. _calendar-cli:

Cách sử dụng trên dòng lệnh
---------------------------

.. versionadded:: 2.5

Có thể chạy module :mod:`!calendar` dưới dạng script từ dòng lệnh để in lịch theo cách tương tác.

.. code-block:: shell

   python -m calendar [-h] [-L LOCALE] [-e ENCODING] [-t {text,html}]
                      [-w WIDTH] [-l LINES] [-s SPACING] [-m MONTHS] [-c CSS]
                      [-f FIRST_WEEKDAY] [year] [month]


Ví dụ, để in lịch cho năm 2000:

.. code-block:: console

   $ python -m calendar 2000
                                     2000

         January                   February                   March
   Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1  2          1  2  3  4  5  6             1  2  3  4  5
    3  4  5  6  7  8  9       7  8  9 10 11 12 13       6  7  8  9 10 11 12
   10 11 12 13 14 15 16      14 15 16 17 18 19 20      13 14 15 16 17 18 19
   17 18 19 20 21 22 23      21 22 23 24 25 26 27      20 21 22 23 24 25 26
   24 25 26 27 28 29 30      28 29                     27 28 29 30 31
   31

          April                      May                       June
   Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1  2       1  2  3  4  5  6  7                1  2  3  4
    3  4  5  6  7  8  9       8  9 10 11 12 13 14       5  6  7  8  9 10 11
   10 11 12 13 14 15 16      15 16 17 18 19 20 21      12 13 14 15 16 17 18
   17 18 19 20 21 22 23      22 23 24 25 26 27 28      19 20 21 22 23 24 25
   24 25 26 27 28 29 30      29 30 31                  26 27 28 29 30

           July                     August                  September
   Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1  2          1  2  3  4  5  6                   1  2  3
    3  4  5  6  7  8  9       7  8  9 10 11 12 13       4  5  6  7  8  9 10
   10 11 12 13 14 15 16      14 15 16 17 18 19 20      11 12 13 14 15 16 17
   17 18 19 20 21 22 23      21 22 23 24 25 26 27      18 19 20 21 22 23 24
   24 25 26 27 28 29 30      28 29 30 31               25 26 27 28 29 30
   31

         October                   November                  December
   Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                      1             1  2  3  4  5                   1  2  3
    2  3  4  5  6  7  8       6  7  8  9 10 11 12       4  5  6  7  8  9 10
    9 10 11 12 13 14 15      13 14 15 16 17 18 19      11 12 13 14 15 16 17
   16 17 18 19 20 21 22      20 21 22 23 24 25 26      18 19 20 21 22 23 24
   23 24 25 26 27 28 29      27 28 29 30               25 26 27 28 29 30 31
   30 31


Các tùy chọn sau được chấp nhận:

.. program:: calendar


.. option:: --help, -h

   Hiển thị thông báo trợ giúp rồi thoát.


.. option:: --locale LOCALE, -L LOCALE

   Locale được sử dụng cho tên tháng và ngày trong tuần. Mặc định là English.


.. option:: --encoding ENCODING, -e ENCODING

   Encoding được sử dụng cho đầu ra.
   :option:`--encoding` là bắt buộc nếu :option:`--locale` được thiết lập.


.. option:: --type {text,html}, -t {text,html}

   In lịch ra terminal dưới dạng văn bản hoặc dưới dạng tài liệu HTML.


.. option:: --first-weekday FIRST_WEEKDAY, -f FIRST_WEEKDAY

   Ngày trong tuần bắt đầu mỗi tuần. Phải là một số từ 0 (Thứ Hai) đến 6 (Chủ Nhật). Mặc định là 0.

   .. versionadded:: 3.13

.. option:: year

   Năm cần in lịch. Mặc định là năm hiện tại.


.. option:: month

   Tháng của :option:`year` đã chỉ định cần in lịch. Phải là một số từ 1 đến 12 và chỉ có thể được sử dụng ở chế độ văn bản. Mặc định là in lịch cho cả năm.


*Tùy chọn chế độ văn bản:*

.. option:: --width WIDTH, -w WIDTH

   Độ rộng của cột ngày theo số cột trong terminal. Ngày được in ở giữa cột. Mọi giá trị nhỏ hơn 2 đều bị bỏ qua. Mặc định là 2.


.. option:: --lines LINES, -l LINES

   Số dòng cho mỗi tuần trong các hàng của terminal. Ngày được in căn theo phía trên. Mọi giá trị nhỏ hơn 1 đều bị bỏ qua. Mặc định là 1.


.. option:: --spacing SPACING, -s SPACING

   Khoảng cách giữa các tháng theo cột. Mọi giá trị nhỏ hơn 2 đều bị bỏ qua. Mặc định là 6.


.. option:: --months MONTHS, -m MONTHS

   Số tháng được in trên mỗi hàng. Mặc định là 3.

.. versionchanged:: 3.14
   Theo mặc định, ngày hôm nay được đánh dấu bằng màu và có thể được
   :ref:`điều khiển bằng các biến môi trường <using-on-controlling-color>`.

*Các tùy chọn của chế độ HTML:*

.. option:: --css CSS, -c CSS

   Đường dẫn đến stylesheet CSS được sử dụng cho lịch. Đường dẫn này phải là đường dẫn tương đối so với HTML được tạo hoặc là URL HTTP tuyệt đối hoặc ``file:///``.
