:mod:`!curses.ascii` --- Các tiện ích cho ký tự ASCII
=====================================================

.. module:: curses.ascii
   :synopsis: Các hằng số và hàm kiểm tra tư cách thành viên cho ký tự ASCII.

.. moduleauthor:: Eric S. Raymond <esr@thyrsus.com>
.. sectionauthor:: Eric S. Raymond <esr@thyrsus.com>

**Mã nguồn:** :source:`Lib/curses/ascii.py`

--------------

Mô-đun :mod:`!curses.ascii` cung cấp các hằng số tên cho ký tự ASCII và các hàm để kiểm tra tư cách thành viên trong nhiều lớp ký tự ASCII khác nhau. Các hằng số được cung cấp là tên của các ký tự điều khiển như sau:

+---------------+-------------------------------------------------------+
| Tên           | Ý nghĩa                                               |
+===============+=======================================================+
| .. data:: NUL |                                                       |
+---------------+-------------------------------------------------------+
| .. data:: SOH | Bắt đầu tiêu đề, ngắt console                         |
+---------------+-------------------------------------------------------+
| .. data:: STX | Bắt đầu văn bản                                       |
+---------------+-------------------------------------------------------+
| .. data:: ETX | Kết thúc văn bản                                      |
+---------------+-------------------------------------------------------+
| .. data:: EOT | Kết thúc truyền tin                                   |
+---------------+-------------------------------------------------------+
| .. data:: ENQ | Yêu cầu, đi kèm với điều khiển luồng :const:`ACK`     |
+---------------+-------------------------------------------------------+
| .. data:: ACK | Xác nhận                                              |
+---------------+-------------------------------------------------------+
| .. data:: BEL | Chuông                                                |
+---------------+-------------------------------------------------------+
| .. data:: BS  | Xóa lùi                                               |
+---------------+-------------------------------------------------------+
| .. data:: TAB | Tab                                                   |
+---------------+-------------------------------------------------------+
| .. data:: HT  | Bí danh của :const:`TAB`: "Tab ngang"                 |
+---------------+-------------------------------------------------------+
| .. data:: LF  | Xuống dòng                                            |
+---------------+-------------------------------------------------------+
| .. data:: NL  | Bí danh của :const:`LF`: "Dòng mới"                   |
+---------------+-------------------------------------------------------+
| .. data:: VT  | Tab dọc                                               |
+---------------+-------------------------------------------------------+
| .. data:: FF  | Nạp biểu mẫu                                          |
+---------------+-------------------------------------------------------+
| .. data:: CR  | Về đầu dòng                                           |
+---------------+-------------------------------------------------------+
| .. data:: SO  | Shift-out, bắt đầu bộ ký tự thay thế                  |
+---------------+-------------------------------------------------------+
| .. data:: SI  | Shift-in, tiếp tục sử dụng bộ ký tự mặc định          |
+---------------+-------------------------------------------------------+
| .. data:: DLE | Ký tự thoát liên kết dữ liệu                          |
+---------------+-------------------------------------------------------+
| .. data:: DC1 | XON, dùng để điều khiển luồng                         |
+---------------+-------------------------------------------------------+
| .. data:: DC2 | Điều khiển thiết bị 2, điều khiển luồng ở chế độ khối |
+---------------+-------------------------------------------------------+
| .. data:: DC3 | XOFF, dùng để điều khiển luồng                        |
+---------------+-------------------------------------------------------+
| .. data:: DC4 | Điều khiển thiết bị 4                                 |
+---------------+-------------------------------------------------------+
| .. data:: NAK | Xác nhận phủ định                                     |
+---------------+-------------------------------------------------------+
| .. data:: SYN | Trạng thái chờ đồng bộ                                |
+---------------+-------------------------------------------------------+
| .. data:: ETB | Kết thúc khối truyền                                  |
+---------------+-------------------------------------------------------+
| .. data:: CAN | Hủy                                                   |
+---------------+-------------------------------------------------------+
| .. data:: EM  | Kết thúc phương tiện                                  |
+---------------+-------------------------------------------------------+
| .. data:: SUB | Thay thế                                              |
+---------------+-------------------------------------------------------+
| .. data:: ESC | Thoát                                                 |
+---------------+-------------------------------------------------------+
| .. data:: FS  | Dấu phân cách tệp                                     |
+---------------+-------------------------------------------------------+
| .. data:: GS  | Dấu phân cách nhóm                                    |
+---------------+-------------------------------------------------------+
| .. data:: RS  | Dấu phân cách bản ghi, ký tự kết thúc chế độ khối     |
+---------------+-------------------------------------------------------+
| .. data:: US  | Dấu phân cách đơn vị                                  |
+---------------+-------------------------------------------------------+
| .. data:: SP  | Khoảng trắng                                          |
+---------------+-------------------------------------------------------+
| .. data:: DEL | Xóa                                                   |
+---------------+-------------------------------------------------------+

Lưu ý rằng nhiều ký tự trong số này ít có ý nghĩa thực tiễn trong cách sử dụng hiện đại. Các từ viết tắt gợi nhớ bắt nguồn từ những quy ước của máy điện báo, có trước máy tính kỹ thuật số.

Mô-đun cung cấp các hàm sau, được xây dựng theo các hàm trong thư viện C tiêu chuẩn:


.. function:: isalnum(c)

   Kiểm tra ký tự chữ-số ASCII; tương đương với ``isalpha(c) or isdigit(c)``.


.. function:: isalpha(c)

   Kiểm tra ký tự chữ cái ASCII; tương đương với ``isupper(c) or islower(c)``.


.. function:: isascii(c)

   Kiểm tra giá trị ký tự nằm trong bộ ký tự ASCII 7 bit.


.. function:: isblank(c)

   Kiểm tra ký tự khoảng trắng ASCII; dấu cách hoặc tab ngang.


.. function:: iscntrl(c)

   Kiểm tra ký tự điều khiển ASCII (trong phạm vi từ 0x00 đến 0x1f hoặc 0x7f).


.. function:: isdigit(c)

   Kiểm tra chữ số thập phân ASCII, từ ``'0'`` đến ``'9'``.  Tương đương với ``c in string.digits``.


.. function:: isgraph(c)

   Kiểm tra xem có ký tự ASCII có thể in được nào ngoại trừ dấu cách hay không.


.. function:: islower(c)

   Kiểm tra xem có ký tự ASCII viết thường hay không.


.. function:: isprint(c)

   Kiểm tra xem có ký tự ASCII có thể in được nào, bao gồm cả dấu cách, hay không.


.. function:: ispunct(c)

   Kiểm tra xem có ký tự ASCII có thể in được nào không phải là dấu cách hoặc ký tự chữ và số hay không.


.. function:: isspace(c)

   Kiểm tra các ký tự khoảng trắng ASCII; dấu cách, xuống dòng, xuống dòng về đầu dòng, ngắt trang, tab ngang, tab dọc.


.. function:: isupper(c)

   Kiểm tra xem có chữ cái ASCII viết hoa hay không.


.. function:: isxdigit(c)

   Kiểm tra xem có chữ số thập lục phân ASCII hay không. Tương đương với ``c in string.hexdigits``.


.. function:: isctrl(c)

   Kiểm tra ký tự điều khiển ASCII (giá trị thứ tự từ 0 đến 31). Không giống
   :func:`iscntrl`, hàm này không bao gồm ký tự xóa (0x7f).


.. function:: ismeta(c)

   Kiểm tra ký tự không phải ASCII (giá trị thứ tự từ 0x80 trở lên).

Các hàm này chấp nhận số nguyên hoặc chuỗi một ký tự; khi đối số là một chuỗi, trước tiên chuỗi đó được chuyển đổi bằng hàm dựng sẵn :func:`ord`.

Lưu ý rằng tất cả các hàm này đều kiểm tra các giá trị bit thứ tự được suy ra từ ký tự của chuỗi bạn truyền vào; chúng thực sự không biết gì về bảng mã ký tự của máy chủ.

Hai hàm sau đây nhận chuỗi một ký tự hoặc giá trị byte dạng số nguyên; chúng trả về giá trị cùng kiểu.


.. function:: ascii(c)

   Trả về giá trị ASCII tương ứng với 7 bit thấp của *c*.


.. function:: ctrl(c)

   Trả về ký tự điều khiển tương ứng với ký tự đã cho (giá trị bit của ký tự được thực hiện phép AND theo bit với 0x1f).


.. function:: alt(c)

   Trả về ký tự 8 bit tương ứng với ký tự ASCII đã cho (giá trị bit của ký tự được thực hiện phép OR theo bit với 0x80).

Hàm sau đây nhận một chuỗi gồm một ký tự hoặc một giá trị số nguyên; hàm trả về một chuỗi.


.. index::
   single: ^ (caret); in curses module
   single: ! (exclamation); in curses module

.. function:: unctrl(c)

   Trả về biểu diễn chuỗi của ký tự ASCII *c*. Nếu *c* có thể in được, chuỗi này chính là ký tự đó. Nếu ký tự là ký tự điều khiển (0x00--0x1f), chuỗi gồm một dấu mũ (``'^'``) theo sau là chữ cái viết hoa tương ứng. Nếu ký tự là ký tự xóa ASCII (0x7f), chuỗi là ``'^?'``. Nếu ký tự có bit meta (0x80) được thiết lập, bit meta sẽ bị loại bỏ, các quy tắc trước đó được áp dụng, rồi ``'!'`` được thêm vào trước kết quả.


.. data:: controlnames

   Một mảng chuỗi gồm 33 phần tử, chứa các mnemonic ASCII cho 32 ký tự điều khiển ASCII từ 0 (NUL) đến 0x1f (US), theo thứ tự, cùng với mnemonic ``SP`` cho ký tự khoảng trắng.

