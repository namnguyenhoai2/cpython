:mod:`!tkinter.font` --- Trình bao font Tkinter
===============================================

.. module:: tkinter.font
   :synopsis: Lớp trình bao font Tkinter

**Mã nguồn:** :source:`Lib/tkinter/font.py`

--------------

Mô-đun :mod:`!tkinter.font` cung cấp lớp :class:`Font` để tạo và sử dụng các font có tên.

Các độ đậm và kiểu nghiêng khác nhau của font là:

.. data:: NORMAL
          ĐẬM NGHIÊNG THƯỜNG

.. class:: Font(root=None, font=None, name=None, exists=False, **options)

   Lớp :class:`Font` đại diện cho một font có tên. Các thực thể *Font* được cấp tên duy nhất và có thể được chỉ định bằng họ font, kích thước và cấu hình kiểu. Font có tên là cách Tk tạo và nhận diện font như một đối tượng duy nhất, thay vì chỉ định font bằng các thuộc tính của nó trong mỗi lần xuất hiện.

   .. versionchanged:: 3.10
      Hai font hiện chỉ được xem là bằng nhau (``==``) khi cả hai đều là các instance :class:`Font` có cùng tên và thuộc cùng một trình thông dịch Tcl.

    đối số:

       | *font* - tuple chỉ định font (họ font, kích thước, các tùy chọn)
       | *name* - tên font duy nhất
       | *exists* - self trỏ đến font có tên hiện có nếu giá trị là true

    các tùy chọn từ khóa bổ sung (bị bỏ qua nếu đã chỉ định *font*):

       | *family* - họ font, ví dụ: Courier, Times
       | *size* - cỡ phông chữ
       | Nếu *size* là số dương, nó được hiểu là kích thước theo point.
       | Nếu *size* là số âm, giá trị tuyệt đối của nó được xem là
       | kích thước theo pixel.
       | *weight* - độ nhấn mạnh của phông chữ (NORMAL, BOLD)
       | *slant* - ROMAN, ITALIC
       | *underline* - gạch chân phông chữ (0 - không có, 1 - gạch chân)
       | *overstrike* - phông chữ gạch ngang (0 - không có, 1 - gạch ngang)

   .. method:: actual(option=None, displayof=None)

      Trả về các thuộc tính thực tế của font, có thể khác với các thuộc tính được yêu cầu do những hạn chế của nền tảng. Nếu không có *option*, trả về một dictionary chứa tất cả các thuộc tính; nếu cung cấp *option*, trả về giá trị của riêng thuộc tính đó. Các thuộc tính được xác định theo display của widget *displayof*, hoặc cửa sổ ứng dụng chính nếu không được chỉ định.

   .. method:: cget(option)

      Lấy một thuộc tính của font.

   .. method:: config(**options)
      :no-typesetting:

   .. method:: configure(**options)

      Sửa đổi một hoặc nhiều thuộc tính của font. Nếu không có đối số, trả về một dictionary chứa các thuộc tính hiện tại.

      :meth:`config` là bí danh của :meth:`!configure`.

   .. method:: copy()

      Trả về một bản sao riêng biệt của font hiện tại: một font có tên mới với cùng các thuộc tính nhưng tên khác, có thể được cấu hình độc lập với font ban đầu. Nếu font hiện tại bao bọc một mô tả font, bản sao sẽ thay vào đó là một font có tên với các thuộc tính đã được phân giải.

   .. method:: measure(text, displayof=None)

      Trả về lượng không gian mà văn bản sẽ chiếm trên display được chỉ định khi được định dạng bằng font hiện tại, dưới dạng một số nguyên pixel. Nếu không chỉ định display thì giả định sử dụng cửa sổ ứng dụng chính.

   .. method:: metrics(*options, **kw)

      Trả về dữ liệu riêng của font. Khi không có tùy chọn, trả về một dictionary ánh xạ từng tên metric với giá trị số nguyên tương ứng; nếu cung cấp một tên tùy chọn, trả về giá trị của metric đó dưới dạng số nguyên. Các tùy chọn gồm:

      *ascent* - khoảng cách giữa đường cơ sở và điểm cao nhất mà một
         ký tự của font có thể chiếm giữ

      *descent* - khoảng cách giữa đường cơ sở và điểm thấp nhất mà một
         ký tự của font có thể chiếm giữ

      *linespace* - khoảng cách dọc tối thiểu cần thiết giữa bất kỳ hai
         ký tự nào của font để đảm bảo các dòng không bị chồng lấn theo chiều dọc.

      *fixed* - 1 nếu font có độ rộng cố định, ngược lại là 0

.. function:: families(root=None, displayof=None)

   Trả về một tuple chứa tên của các font family hiện có.

.. function:: names(root=None)

   Trả về một tuple chứa tên của tất cả các font đã được định nghĩa.

.. function:: nametofont(name, root=None)

   Trả về biểu diễn :class:`Font` của font có tên hiện có *name*. *root* là widget có Tcl interpreter sở hữu font; nếu bị bỏ qua, cửa sổ root mặc định sẽ được sử dụng.

   .. versionchanged:: 3.10
      Tham số *root* đã được thêm vào.
