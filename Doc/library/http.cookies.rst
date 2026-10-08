:mod:`!http.cookies` --- Quản lý trạng thái HTTP
================================================

.. module:: http.cookies
   :synopsis: Hỗ trợ quản lý trạng thái HTTP (cookie).

.. moduleauthor:: Timothy O'Malley <timo@alum.mit.edu>
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/http/cookies.py`

--------------

Mô-đun :mod:`!http.cookies` định nghĩa các lớp để trừu tượng hóa khái niệm cookie, một cơ chế quản lý trạng thái HTTP. Mô-đun này hỗ trợ cả cookie chỉ chứa chuỗi đơn giản và cung cấp một lớp trừu tượng cho phép sử dụng bất kỳ kiểu dữ liệu nào có thể tuần tự hóa làm giá trị cookie.

Mô-đun này trước đây áp dụng nghiêm ngặt các quy tắc phân tích cú pháp được mô tả trong
:rfc:`2109` và các đặc tả :rfc:`2068`. Kể từ đó, người ta phát hiện rằng MSIE 3.0x không tuân theo các quy tắc về ký tự được nêu trong những đặc tả đó; nhiều trình duyệt và máy chủ hiện nay cũng đã nới lỏng các quy tắc phân tích cú pháp khi xử lý cookie. Do đó, mô-đun này hiện sử dụng các quy tắc phân tích cú pháp ít nghiêm ngặt hơn một chút so với trước đây.

Tập ký tự, :data:`string.ascii_letters`, :data:`string.digits` và ``!#$%&'*+-.^_`|~:`` biểu thị tập hợp các ký tự hợp lệ được mô-đun này cho phép trong tên cookie (dưới dạng :attr:`~Morsel.key`).

.. versionchanged:: 3.3
   Cho phép ':' là một ký tự hợp lệ trong tên cookie.


.. note::

   Khi gặp cookie không hợp lệ, :exc:`CookieError` sẽ được phát sinh, vì vậy nếu dữ liệu cookie của bạn đến từ trình duyệt, bạn luôn nên chuẩn bị cho dữ liệu không hợp lệ và bắt :exc:`CookieError` khi phân tích cú pháp.


.. exception:: CookieError

   Ngoại lệ xảy ra do :rfc:`2109` không hợp lệ: thuộc tính không chính xác, header :mailheader:`Set-Cookie` không chính xác, v.v.


.. class:: BaseCookie([input])

   Lớp này là một đối tượng tương tự dictionary, có các khóa là chuỗi và các giá trị là các instance của :class:`Morsel`. Lưu ý rằng khi gán một giá trị cho một khóa, giá trị trước tiên được chuyển đổi thành một :class:`Morsel` chứa khóa và giá trị đó.

   Nếu cung cấp *input*, giá trị này sẽ được truyền cho phương thức :meth:`load`.


.. class:: SimpleCookie([input])

   Lớp này kế thừa từ :class:`BaseCookie` và ghi đè :meth:`~BaseCookie.value_decode` cùng :meth:`~BaseCookie.value_encode`. :class:`!SimpleCookie` hỗ trợ chuỗi làm giá trị cookie. Khi thiết lập giá trị, :class:`!SimpleCookie` gọi hàm dựng sẵn :func:`str` để chuyển đổi giá trị thành chuỗi. Các giá trị nhận được từ HTTP được giữ nguyên dưới dạng chuỗi.

.. seealso::

   Module :mod:`http.cookiejar`
      Xử lý cookie HTTP cho các *client web*.  :mod:`http.cookiejar` và
      :mod:`!http.cookies` module không phụ thuộc lẫn nhau.

   :rfc:`2109` - Cơ chế quản lý trạng thái HTTP
      Đây là đặc tả quản lý trạng thái được module này triển khai.


.. _cookie-objects:

Đối tượng Cookie
----------------


.. method:: BaseCookie.value_decode(val)

   Trả về một tuple ``(real_value, coded_value)`` từ biểu diễn chuỗi. ``real_value`` có thể thuộc bất kỳ kiểu nào. Phương thức này không thực hiện giải mã trong
   :class:`BaseCookie` --- nó tồn tại để có thể được ghi đè.


.. method:: BaseCookie.value_encode(val)

   Trả về một tuple ``(real_value, coded_value)``. *val* có thể thuộc bất kỳ kiểu nào, nhưng ``coded_value`` sẽ luôn được chuyển đổi thành một chuỗi. Phương thức này không thực hiện mã hóa trong :class:`BaseCookie` --- nó tồn tại để có thể được ghi đè.

   Nhìn chung, :meth:`value_encode` và
   :meth:`value_decode` là các phép nghịch đảo trên miền giá trị của *value_decode*.


.. method:: BaseCookie.output(attrs=None, header='Set-Cookie:', sep='\r\n')

   Trả về một biểu diễn chuỗi phù hợp để gửi dưới dạng HTTP header. *attrs* và *header* được gửi đến từng :class:`Morsel` bằng phương thức :meth:`~Morsel.output`. *sep* được dùng để nối các header lại với nhau và theo mặc định là tổ hợp ``'\r\n'`` (CRLF).


.. method:: BaseCookie.js_output(attrs=None)

   Trả về một đoạn mã JavaScript có thể nhúng; nếu được chạy trên trình duyệt hỗ trợ JavaScript, đoạn mã này sẽ hoạt động giống như khi các HTTP header được gửi.

   Ý nghĩa của *attrs* giống như trong :meth:`output`.


.. method:: BaseCookie.load(rawdata)

   Nếu *rawdata* là một chuỗi, hãy phân tích cú pháp chuỗi đó như một ``HTTP_COOKIE`` và thêm các giá trị tìm thấy ở đó dưới dạng :class:`Morsel`\ s. Nếu đó là một dictionary, thì tương đương với::

      for k, v in rawdata.items():
          cookie[k] = v


.. _morsel-objects:

Đối tượng Morsel
----------------


.. class:: Morsel

   Trừu tượng hóa một cặp khóa/giá trị, có một số thuộc tính :rfc:`2109`.

   Morsel là các đối tượng giống như dictionary, có tập hợp khóa cố định --- các
   thuộc tính :rfc:`2109` hợp lệ gồm:

     .. attribute:: expires
                    path comment domain max-age secure version httponly samesite partitioned

   Thuộc tính :attr:`httponly` chỉ định rằng cookie chỉ được truyền trong các yêu cầu HTTP và không thể được truy cập thông qua JavaScript. Điều này nhằm giảm thiểu một số hình thức tấn công cross-site scripting.

   Thuộc tính :attr:`samesite` kiểm soát thời điểm trình duyệt gửi cookie cùng các yêu cầu cross-site. Điều này giúp giảm thiểu các cuộc tấn công CSRF. Các giá trị hợp lệ là "Strict" (chỉ được gửi cùng các yêu cầu same-site), "Lax" (được gửi cùng các yêu cầu same-site và các thao tác điều hướng cấp cao nhất), và "None" (được gửi cùng các yêu cầu same-site và cross-site). Khi sử dụng "None", cũng phải đặt thuộc tính "secure", theo yêu cầu của các trình duyệt hiện đại.

   Thuộc tính :attr:`partitioned` cho user agent biết rằng các cookie cross-site này *chỉ nên* khả dụng trong cùng ngữ cảnh cấp cao nhất nơi cookie được thiết lập lần đầu. Để user agent chấp nhận điều này, bạn **phải** đồng thời thiết lập ``Secure``.

   Ngoài ra, bạn nên sử dụng tiền tố ``__Host`` khi thiết lập các cookie được phân vùng để ràng buộc chúng với hostname thay vì registrable domain. Đọc `CHIPS (Cookies Having Independent Partitioned State) <CHIPS (Cookies Having Independent Partitioned State)_>`_ để biết đầy đủ chi tiết và ví dụ.

   .. _CHIPS (Cookies Having Independent Partitioned State): https://github.com/privacycg/CHIPS/blob/main/README.md

   Các khóa không phân biệt chữ hoa chữ thường và giá trị mặc định của chúng là ``''``.

   .. versionchanged:: 3.5
      :meth:`!__eq__` now takes :attr:`~Morsel.key` and :attr:`~Morsel.value`
      có tính đến.

   .. versionchanged:: 3.7
      Các thuộc tính :attr:`~Morsel.key`, :attr:`~Morsel.value` và
      :attr:`~Morsel.coded_value` chỉ được đọc. Dùng :meth:`~Morsel.set` để thiết lập chúng.

   .. versionchanged:: 3.8
      Đã thêm hỗ trợ cho thuộc tính :attr:`samesite`.

   .. versionchanged:: 3.14
      Đã bổ sung hỗ trợ cho thuộc tính :attr:`partitioned`.


.. attribute:: Morsel.value

   Giá trị của cookie.


.. attribute:: Morsel.coded_value

   Giá trị đã mã hóa của cookie --- đây là giá trị cần được gửi đi.


.. attribute:: Morsel.key

   Tên của cookie.


.. method:: Morsel.set(key, value, coded_value)

   Thiết lập các thuộc tính *key*, *value* và *coded_value*.


.. method:: Morsel.isReservedKey(K)

   *K* có phải là một phần tử trong tập hợp các khóa của :class:`Morsel` hay không.


.. method:: Morsel.output(attrs=None, header='Set-Cookie:')

   Trả về biểu diễn chuỗi của Morsel, phù hợp để gửi dưới dạng HTTP header. Theo mặc định, tất cả các thuộc tính đều được включ, trừ khi cung cấp *attrs*, trong trường hợp đó, giá trị này phải là danh sách các thuộc tính cần sử dụng. *header* theo mặc định là ``"Set-Cookie:"``.


.. method:: Morsel.js_output(attrs=None)

   Trả về một đoạn mã JavaScript có thể nhúng; nếu được chạy trên trình duyệt hỗ trợ JavaScript, đoạn mã này sẽ hoạt động giống như khi tiêu đề HTTP được gửi.

   Ý nghĩa của *attrs* giống như trong :meth:`output`.


.. method:: Morsel.OutputString(attrs=None)

   Trả về một chuỗi biểu diễn Morsel, không có bất kỳ HTTP hoặc JavaScript bao quanh nào.

   Ý nghĩa của *attrs* giống như trong :meth:`output`.


.. method:: Morsel.update(values)

   Cập nhật các giá trị trong từ điển Morsel bằng các giá trị trong từ điển *values*. Phát sinh lỗi nếu bất kỳ khóa nào trong từ điển *values* không phải là thuộc tính :rfc:`2109` hợp lệ.

   .. versionchanged:: 3.5
      sẽ phát sinh lỗi đối với các khóa không hợp lệ.


.. method:: Morsel.copy(value)

   Trả về một bản sao nông của đối tượng Morsel.

   .. versionchanged:: 3.5
      trả về một đối tượng Morsel thay vì một dict.


.. method:: Morsel.setdefault(key, value=None)

   Phát sinh lỗi nếu key không phải là thuộc tính :rfc:`2109` hợp lệ; nếu không thì hoạt động giống như :meth:`dict.setdefault`.


.. _cookie-example:

Ví dụ
-----

Ví dụ sau đây minh họa cách sử dụng module :mod:`!http.cookies`.

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> from http import cookies
   >>> C = cookies.SimpleCookie()
   >>> C["fig"] = "newton"
   >>> C["sugar"] = "wafer"
   >>> print(C) # tạo các HTTP header
   Set-Cookie: fig=newton
   Set-Cookie: sugar=wafer
   >>> print(C.output()) # tương tự
   Set-Cookie: fig=newton
   Set-Cookie: sugar=wafer
   >>> C = cookies.SimpleCookie()
   >>> C["rocky"] = "road"
   >>> C["rocky"]["path"] = "/cookie"
   >>> print(C.output(header="Cookie:"))
   Cookie: rocky=road; Path=/cookie
   >>> print(C.output(attrs=[], header="Cookie:"))
   Cookie: rocky=road
   >>> C = cookies.SimpleCookie()
   >>> C.load("chips=ahoy; vienna=finger") # nạp từ một chuỗi (HTTP header)
   >>> print(C)
   Set-Cookie: chips=ahoy
   Set-Cookie: vienna=finger
   >>> C = cookies.SimpleCookie()
   >>> C.load('keebler="E=everybody; L=\\"Loves\\"; fudge=;";')
   >>> print(C)
   Set-Cookie: keebler="E=everybody; L=\"Loves\"; fudge=;"
   >>> C = cookies.SimpleCookie()
   >>> C["oreo"] = "doublestuff"
   >>> C["oreo"]["path"] = "/"
   >>> print(C)
   Set-Cookie: oreo=doublestuff; Path=/
   >>> C = cookies.SimpleCookie()
   >>> C["twix"] = "none for you"
   >>> C["twix"].value
   'none for you'
   >>> C = cookies.SimpleCookie()
   >>> C["number"] = 7 # tương đương với C["number"] = str(7)
   >>> C["string"] = "seven"
   >>> C["number"].value
   '7'
   >>> C["string"].value
   'seven'
   >>> print(C)
   Set-Cookie: number=7
   Set-Cookie: string=seven
