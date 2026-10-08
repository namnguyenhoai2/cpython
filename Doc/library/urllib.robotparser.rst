:mod:`!urllib.robotparser` ---  Trình phân tích robots.txt
==========================================================

.. module:: urllib.robotparser
   :synopsis: Tải tệp robots.txt và trả lời các câu hỏi về khả năng fetch các URL khác.

.. sectionauthor:: Skip Montanaro <skip.montanaro@gmail.com>

**Mã nguồn:** :source:`Lib/urllib/robotparser.py`

.. index::
   single: WWW
   single: World Wide Web
   single: URL
   single: robots.txt

--------------

Module này cung cấp một lớp duy nhất, :class:`RobotFileParser`, dùng để trả lời các câu hỏi về việc một user agent cụ thể có thể fetch một URL trên website đã phát hành tệp :file:`robots.txt` hay không. Để biết thêm chi tiết về cấu trúc của các tệp :file:`robots.txt`, hãy xem :rfc:`9309`.


.. class:: RobotFileParser(url='')

   Lớp này cung cấp các phương thức để đọc, phân tích cú pháp và trả lời các câu hỏi về
   tệp :file:`robots.txt` tại *url*.

   .. method:: set_url(url)

      Thiết lập URL tham chiếu đến một tệp :file:`robots.txt`.

   .. method:: read()

      Đọc URL :file:`robots.txt` và truyền URL đó cho parser.

   .. method:: parse(lines)

      Phân tích đối số lines.

   .. method:: can_fetch(useragent, url)

      Trả về ``True`` nếu *useragent* được phép tải *url* theo các quy tắc có trong tệp :file:`robots.txt` đã được phân tích.

   .. method:: mtime()

      Trả về thời điểm tệp ``robots.txt`` được tải lần cuối. Điều này hữu ích cho các web spider chạy trong thời gian dài, cần định kỳ kiểm tra các tệp ``robots.txt`` mới.

   .. method:: modified()

      Đặt thời điểm tệp ``robots.txt`` được tải lần cuối thành thời điểm hiện tại.

   .. method:: crawl_delay(useragent)

      Trả về giá trị của tham số ``Crawl-delay`` từ ``robots.txt`` cho *useragent* đang xét. Nếu không có tham số đó, tham số không áp dụng cho *useragent* được chỉ định hoặc mục ``robots.txt`` của tham số này có cú pháp không hợp lệ, trả về ``None``.

      .. versionadded:: 3.6

   .. method:: request_rate(useragent)

      Trả về nội dung của tham số ``Request-rate`` từ ``robots.txt`` dưới dạng :term:`named tuple` ``RequestRate(requests, seconds)``. Nếu không có tham số đó, tham số không áp dụng cho *useragent* được chỉ định hoặc mục ``robots.txt`` của tham số này có cú pháp không hợp lệ, trả về ``None``.

      .. versionadded:: 3.6

   .. method:: site_maps()

      Trả về nội dung của tham số ``Sitemap`` từ ``robots.txt`` dưới dạng :func:`list`. Nếu không có tham số đó hoặc mục nhập ``robots.txt`` cho tham số này có cú pháp không hợp lệ, hãy trả về ``None``.

      .. versionadded:: 3.8


Ví dụ sau minh họa cách sử dụng cơ bản lớp :class:`RobotFileParser`::

   >>> import urllib.robotparser
   >>> rp = urllib.robotparser.RobotFileParser()
   >>> rp.set_url("http://www.pythontest.net/robots.txt")
   >>> rp.read()
   >>> rrate = rp.request_rate("*")
   >>> rrate.requests
   1
   >>> rrate.seconds
   1
   >>> rp.crawl_delay("*")
   6
   >>> rp.can_fetch("*", "http://www.pythontest.net/")
   True
   >>> rp.can_fetch("*", "http://www.pythontest.net/no-robots-here/")
   False
