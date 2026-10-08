:mod:`!urllib.error` --- Các lớp ngoại lệ do urllib.request phát sinh
=====================================================================

.. module:: urllib.error
   :synopsis: Các lớp ngoại lệ do urllib.request phát sinh.

.. moduleauthor:: Jeremy Hylton <jeremy@alum.mit.edu>
.. sectionauthor:: Senthil Kumaran <orsenthil@gmail.com>

**Mã nguồn:** :source:`Lib/urllib/error.py`

--------------

Module :mod:`!urllib.error` định nghĩa các lớp ngoại lệ cho những ngoại lệ do :mod:`urllib.request` phát sinh. Lớp ngoại lệ cơ sở là :exc:`URLError`.

Sau đây là các ngoại lệ mà :mod:`!urllib.error` phát sinh khi thích hợp:

.. exception:: URLError

   Các handler phát sinh ngoại lệ này (hoặc các ngoại lệ dẫn xuất) khi gặp sự cố. Đây là một lớp con của :exc:`OSError`.

   .. attribute:: reason

      Lý do gây ra lỗi này. Đó có thể là một chuỗi thông báo hoặc một instance ngoại lệ khác.

   .. versionchanged:: 3.3
      :exc:`URLError` used to be a subtype of :exc:`IOError`, which is now an
      bí danh của :exc:`OSError`.


.. exception:: HTTPError(url, code, msg, hdrs, fp)

   Mặc dù là một exception (lớp con của :exc:`URLError`), một
   :exc:`HTTPError` cũng có thể hoạt động như một giá trị trả về dạng giống tệp không phải exception (giống với giá trị mà :func:`~urllib.request.urlopen` trả về). Điều này hữu ích khi xử lý các lỗi HTTP đặc biệt, chẳng hạn như các yêu cầu xác thực.

   .. attribute:: url

      Chứa URL của request. Là bí danh cho thuộc tính *filename*.

   .. attribute:: code

      Mã trạng thái HTTP như được định nghĩa trong :rfc:`2616`. Giá trị số này tương ứng với một giá trị được tìm thấy trong từ điển mã như được nêu trong
      :attr:`http.server.BaseHTTPRequestHandler.responses`.

   .. attribute:: reason

      Đây thường là một chuỗi giải thích lý do xảy ra lỗi này. Là bí danh cho thuộc tính *msg*.

   .. attribute:: headers

      Các HTTP response headers của HTTP request gây ra
      :exc:`HTTPError`. Bí danh của thuộc tính *hdrs*.

      .. versionadded:: 3.4

   .. attribute:: fp

      Một đối tượng giống tệp, từ đó có thể đọc nội dung phần thân của lỗi HTTP.

.. exception:: ContentTooShortError(msg, content)

   Ngoại lệ này được phát sinh khi hàm :func:`~urllib.request.urlretrieve` phát hiện rằng lượng dữ liệu đã tải xuống ít hơn lượng dự kiến (được chỉ định bởi header *Content-Length*).

   .. attribute:: content

      Dữ liệu đã tải xuống (và được cho là đã bị cắt ngắn).
