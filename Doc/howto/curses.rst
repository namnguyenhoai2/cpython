.. _curses-howto:

****************************
Lập trình Curses bằng Python
****************************

.. currentmodule:: curses

:Author: A.M. Kuchling, Eric S. Raymond
:Release: 2.04


.. topic:: Tóm tắt

   Tài liệu này mô tả cách sử dụng mô-đun mở rộng :mod:`curses` để điều khiển màn hình ở chế độ văn bản.


curses là gì?
=============

Thư viện curses cung cấp một cơ chế vẽ màn hình và xử lý bàn phím độc lập với terminal cho các terminal dựa trên văn bản; những terminal như vậy bao gồm VT100, console Linux và terminal mô phỏng do nhiều chương trình cung cấp. Các terminal hiển thị hỗ trợ nhiều mã điều khiển để thực hiện những thao tác phổ biến như di chuyển con trỏ, cuộn màn hình và xóa các vùng. Các terminal khác nhau sử dụng những mã rất khác nhau và thường có các đặc điểm riêng nhỏ.

Trong thời đại của màn hình đồ họa, người ta có thể hỏi "tại sao phải bận tâm"? Đúng là các terminal hiển thị dạng ô ký tự đã là công nghệ lỗi thời, nhưng vẫn có những lĩnh vực mà khả năng thực hiện các thao tác phức tạp với chúng vẫn có giá trị. Một lĩnh vực là các hệ điều hành Unix có kích thước nhỏ hoặc nhúng không chạy máy chủ X. Một lĩnh vực khác là các công cụ như trình cài đặt hệ điều hành và trình cấu hình kernel, vốn có thể phải chạy trước khi bất kỳ hỗ trợ đồ họa nào khả dụng.

Thư viện curses cung cấp chức năng khá cơ bản, tạo cho lập trình viên một lớp trừu tượng về màn hình chứa nhiều cửa sổ văn bản không chồng lấp. Nội dung của một cửa sổ có thể được thay đổi theo nhiều cách—thêm văn bản, xóa văn bản, thay đổi giao diện—và thư viện curses sẽ xác định những mã điều khiển nào cần được gửi đến terminal để tạo ra đầu ra chính xác. curses không cung cấp nhiều khái niệm về giao diện người dùng như nút, hộp kiểm hoặc hộp thoại; nếu cần những tính năng như vậy, hãy cân nhắc một thư viện giao diện người dùng như
:pypi:`Urwid`.

Thư viện curses ban đầu được viết cho BSD Unix; các phiên bản Unix System V sau này của AT&T đã bổ sung nhiều cải tiến và hàm mới. BSD curses không còn được duy trì nữa và đã được thay thế bằng ncurses, một triển khai mã nguồn mở của giao diện AT&T. Nếu bạn đang sử dụng một Unix mã nguồn mở như Linux hoặc FreeBSD, hệ thống của bạn gần như chắc chắn sử dụng ncurses. Vì hầu hết các phiên bản Unix thương mại hiện nay đều dựa trên mã System V, có lẽ tất cả các hàm được mô tả ở đây đều khả dụng. Tuy nhiên, các phiên bản curses cũ hơn đi kèm với một số Unix độc quyền có thể không hỗ trợ mọi thứ.

Phiên bản Python dành cho Windows không bao gồm mô-đun :mod:`curses`. Gói :pypi:`windows-curses` của bên thứ ba cung cấp cùng giao diện trên Windows.


Mô-đun curses của Python
------------------------

Mô-đun Python là một wrapper khá đơn giản trên các hàm C do curses cung cấp; nếu bạn đã quen với lập trình curses bằng C, việc chuyển kiến thức đó sang Python thực sự rất dễ dàng. Điểm khác biệt lớn nhất là giao diện Python làm mọi thứ đơn giản hơn bằng cách hợp nhất các hàm C khác nhau như
:c:func:`!addstr`, :c:func:`!mvaddstr` và :c:func:`!mvwaddstr` thành một
phương thức :meth:`~curses.window.addstr`. Bạn sẽ tìm hiểu chi tiết hơn về điều này ở phần sau.

HOWTO này là phần giới thiệu về cách viết các chương trình dạng văn bản bằng curses và Python. Tài liệu không cố gắng trở thành hướng dẫn đầy đủ về curses API; để biết thêm, hãy xem phần về ncurses trong hướng dẫn thư viện Python và các trang hướng dẫn C về ncurses. Tuy nhiên, tài liệu sẽ cung cấp cho bạn những ý tưởng cơ bản.


Khởi động và kết thúc một ứng dụng curses
=========================================

Trước khi thực hiện bất kỳ thao tác nào, curses phải được khởi tạo. Việc này được thực hiện bằng cách gọi hàm :func:`~curses.initscr`, hàm này sẽ xác định loại terminal, gửi mọi mã thiết lập cần thiết đến terminal và tạo nhiều cấu trúc dữ liệu nội bộ khác nhau. Nếu thành công,
:func:`!initscr` trả về một đối tượng cửa sổ đại diện cho toàn bộ màn hình; đối tượng này thường được gọi là ``stdscr``, theo tên của biến C tương ứng.::

   import curses
   stdscr = curses.initscr()

Thông thường, các ứng dụng curses tắt việc tự động echo các phím lên màn hình để có thể đọc phím và chỉ hiển thị chúng trong những trường hợp nhất định. Việc này yêu cầu gọi
:func:`~curses.noecho`.::

   curses.noecho()

Các ứng dụng cũng thường cần phản hồi phím ngay lập tức mà không yêu cầu nhấn phím Enter; chế độ này được gọi là chế độ cbreak, trái ngược với chế độ nhập được đệm thông thường.::

   curses.cbreak()

Các terminal thường trả về những phím đặc biệt, chẳng hạn như các phím con trỏ hoặc các phím điều hướng như Page Up và Home, dưới dạng một chuỗi escape nhiều byte. Mặc dù bạn có thể viết ứng dụng để chờ các chuỗi như vậy và xử lý chúng tương ứng, curses có thể làm việc đó thay bạn và trả về một giá trị đặc biệt như
:const:`curses.KEY_LEFT`. Để curses thực hiện việc này, bạn phải bật chế độ keypad.::

   stdscr.keypad(True)

Việc kết thúc một ứng dụng curses dễ hơn nhiều so với việc khởi động. Bạn cần gọi::

   curses.nocbreak()
   stdscr.keypad(False)
   curses.echo()

để khôi phục các thiết lập terminal tương thích với curses. Sau đó gọi
hàm :func:`~curses.endwin` để đưa terminal về chế độ hoạt động ban đầu.::

   curses.endwin()

Một vấn đề phổ biến khi gỡ lỗi ứng dụng curses là terminal bị rối loạn khi ứng dụng bị lỗi mà không khôi phục terminal về trạng thái trước đó. Trong Python, điều này thường xảy ra khi mã của bạn có lỗi và phát sinh một ngoại lệ không được bắt. Chẳng hạn, các phím sẽ không còn được hiển thị trên màn hình khi bạn gõ, khiến việc sử dụng shell trở nên khó khăn.

Trong Python, bạn có thể tránh những rắc rối này và giúp việc gỡ lỗi dễ dàng hơn nhiều bằng cách import hàm :func:`curses.wrapper` và sử dụng nó như sau::

   from curses import wrapper

   def main(stdscr):
       # Xóa màn hình
       stdscr.clear()

       # Điều này gây ra ZeroDivisionError khi i == 10.
       for i in range(0, 11):
           v = i-10
           stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

           stdscr.refresh()
           stdscr.getkey()

   wrapper(main)

Hàm :func:`~curses.wrapper` nhận một đối tượng có thể gọi và thực hiện các bước khởi tạo được mô tả ở trên, đồng thời khởi tạo màu nếu có hỗ trợ màu. :func:`!wrapper` sau đó chạy đối tượng có thể gọi do bạn cung cấp. Khi đối tượng có thể gọi trả về, :func:`!wrapper` sẽ khôi phục trạng thái ban đầu của terminal. Đối tượng có thể gọi được gọi bên trong một
:keyword:`try`...\ :keyword:`except` bắt các ngoại lệ, khôi phục trạng thái của terminal rồi phát sinh lại ngoại lệ. Vì vậy, terminal của bạn sẽ không bị bỏ lại ở trạng thái bất thường khi xảy ra ngoại lệ, và bạn vẫn có thể đọc thông báo cùng traceback của ngoại lệ.


Windows và Pads
===============

Windows là abstraction cơ bản trong curses. Một đối tượng window biểu diễn một vùng hình chữ nhật trên màn hình và hỗ trợ các phương thức để hiển thị văn bản, xóa văn bản, cho phép người dùng nhập chuỗi, v.v.

Đối tượng ``stdscr`` được hàm :func:`~curses.initscr` trả về là một đối tượng window bao phủ toàn bộ màn hình. Nhiều chương trình có thể chỉ cần một window duy nhất này, nhưng bạn có thể muốn chia màn hình thành các window nhỏ hơn để vẽ lại hoặc xóa chúng riêng biệt. The
Hàm :func:`~curses.newwin` tạo một cửa sổ mới với kích thước đã cho và trả về đối tượng cửa sổ mới.::

   begin_x = 20; begin_y = 7
   height = 5; width = 40
   win = curses.newwin(height, width, begin_y, begin_x)

Lưu ý rằng hệ tọa độ được sử dụng trong curses khá khác thường. Tọa độ luôn được truyền theo thứ tự *y,x*, và góc trên bên trái của cửa sổ có tọa độ (0,0). Điều này trái với quy ước thông thường khi xử lý tọa độ, trong đó tọa độ *x* được đặt trước. Đây là một điểm khác biệt đáng tiếc so với hầu hết các ứng dụng máy tính khác, nhưng nó đã là một phần của curses kể từ khi được viết lần đầu và hiện đã quá muộn để thay đổi.

Ứng dụng của bạn có thể xác định kích thước màn hình bằng cách sử dụng
các biến :data:`curses.LINES` và :data:`curses.COLS` để lấy kích thước *y* và *x*. Khi đó, các tọa độ hợp lệ sẽ nằm trong khoảng từ ``(0,0)`` đến ``(curses.LINES - 1, curses.COLS - 1)``.

Khi gọi một phương thức để hiển thị hoặc xóa văn bản, hiệu ứng sẽ không ngay lập tức xuất hiện trên màn hình. Thay vào đó, bạn phải gọi
phương thức :meth:`~curses.window.refresh` của các đối tượng cửa sổ để cập nhật màn hình.

Điều này là do curses ban đầu được viết với các kết nối terminal tốc độ 300 baud chậm chạp; với những terminal này, việc giảm thiểu thời gian cần thiết để vẽ lại màn hình là rất quan trọng. Thay vào đó, curses tích lũy các thay đổi trên màn hình và hiển thị chúng theo cách hiệu quả nhất khi bạn gọi :meth:`!refresh`. Ví dụ: nếu chương trình của bạn hiển thị một số văn bản trong cửa sổ rồi xóa cửa sổ, thì không cần gửi văn bản ban đầu vì văn bản đó chưa bao giờ được hiển thị.

Trên thực tế, việc yêu cầu curses vẽ lại một cửa sổ một cách rõ ràng không thực sự khiến việc lập trình với curses phức tạp hơn nhiều. Hầu hết chương trình đều hoạt động dồn dập trong chốc lát rồi tạm dừng để chờ thao tác nhấn phím hoặc một hành động khác từ người dùng. Bạn chỉ cần đảm bảo màn hình đã được vẽ lại trước khi tạm dừng để chờ dữ liệu nhập từ người dùng, bằng cách gọi trước
:meth:`!stdscr.refresh` hoặc phương thức :meth:`!refresh` của một cửa sổ liên quan khác.

Pad là một trường hợp đặc biệt của cửa sổ; nó có thể lớn hơn màn hình hiển thị thực tế và tại mỗi thời điểm chỉ một phần của pad được hiển thị. Việc tạo pad yêu cầu chiều cao và chiều rộng của pad, còn việc làm mới pad yêu cầu cung cấp tọa độ của vùng trên màn hình nơi một phần của pad sẽ được hiển thị.::

   pad = curses.newpad(100, 100)
   # Các vòng lặp này điền các chữ cái vào pad; addch() được
   # giải thích trong phần tiếp theo
   for y in range(0, 99):
       for x in range(0, 99):
           pad.addch(y,x, ord('a') + (x*x+y*y) % 26)

   # Hiển thị một phần của pad ở giữa màn hình.
   # (0,0) : tọa độ của góc trên bên trái của vùng pad cần hiển thị.
   # (5,5) : tọa độ của góc trên bên trái của vùng cửa sổ sẽ được điền
   #         bằng nội dung của pad.
   # (20, 75) : tọa độ của góc dưới bên phải của vùng cửa sổ sẽ được
   #          : điền bằng nội dung của pad.
   pad.refresh( 0,0, 5,5, 20,75)

Lệnh gọi :meth:`!refresh` hiển thị một phần của pad trong hình chữ nhật kéo dài từ tọa độ (5,5) đến tọa độ (20,75) trên màn hình; góc trên bên trái của phần được hiển thị là tọa độ (0,0) trên pad. Ngoài điểm khác biệt đó, pad giống hệt các cửa sổ thông thường và hỗ trợ các phương thức tương tự.

Nếu có nhiều cửa sổ và pad trên màn hình, có một cách hiệu quả hơn để cập nhật màn hình và ngăn hiện tượng nhấp nháy khó chịu khi từng phần của màn hình được cập nhật. :meth:`!refresh` thực hiện hai việc:

1) Gọi phương thức :meth:`~curses.window.noutrefresh` của từng cửa sổ để cập nhật một cấu trúc dữ liệu bên dưới biểu thị trạng thái mong muốn của màn hình.
2) Gọi hàm :func:`~curses.doupdate` để thay đổi màn hình vật lý sao cho khớp với trạng thái mong muốn được ghi trong cấu trúc dữ liệu.

Thay vào đó, bạn có thể gọi :meth:`!noutrefresh` trên một số cửa sổ để cập nhật cấu trúc dữ liệu, sau đó gọi :func:`!doupdate` để cập nhật màn hình.


Hiển thị văn bản
================

Từ góc nhìn của một lập trình viên C, curses đôi khi có thể trông như một mê cung quanh co gồm nhiều hàm, mỗi hàm khác nhau một cách tinh tế. Ví dụ:
:c:func:`!addstr` hiển thị một chuỗi tại vị trí con trỏ hiện tại trong cửa sổ ``stdscr``, trong khi :c:func:`!mvaddstr` trước tiên di chuyển đến tọa độ y,x đã cho rồi mới hiển thị chuỗi. :c:func:`!waddstr` cũng giống như :c:func:`!addstr`, nhưng cho phép chỉ định một cửa sổ để sử dụng thay vì mặc định dùng ``stdscr``. :c:func:`!mvwaddstr` cho phép chỉ định cả cửa sổ và tọa độ.

May mắn là giao diện Python ẩn đi tất cả những chi tiết này. ``stdscr`` là một đối tượng cửa sổ giống như mọi đối tượng khác, và các phương thức như
:meth:`~curses.window.addstr` chấp nhận nhiều dạng đối số. Thông thường có bốn dạng khác nhau.

+-----------------------------------+------------------------------------------------------------------------------------------------+
| Dạng thức                         | Mô tả                                                                                          |
+===================================+================================================================================================+
| *str* hoặc *ch*                   | Hiển thị chuỗi *str* hoặc ký tự *ch* tại vị trí hiện tại                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| *str* hoặc *ch*, *attr*           | Hiển thị chuỗi *str* hoặc ký tự *ch*, sử dụng thuộc tính *attr* tại vị trí hiện tại            |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| *y*, *x*, *str* hoặc *ch*         | Di chuyển đến vị trí *y,x* trong cửa sổ và hiển thị *str* hoặc *ch*                            |
+-----------------------------------+------------------------------------------------------------------------------------------------+
| *y*, *x*, *str* hoặc *ch*, *attr* | Di chuyển đến vị trí *y,x* trong cửa sổ và hiển thị *str* hoặc *ch*, sử dụng thuộc tính *attr* |
+-----------------------------------+------------------------------------------------------------------------------------------------+

Các thuộc tính cho phép hiển thị văn bản ở dạng được làm nổi bật, chẳng hạn như chữ đậm, gạch chân, mã đảo màu hoặc có màu. Chúng sẽ được giải thích chi tiết hơn trong phần tiếp theo.


Phương thức :meth:`~curses.window.addstr` nhận một chuỗi Python hoặc chuỗi byte làm giá trị cần hiển thị. Nội dung của các chuỗi byte được gửi nguyên trạng đến terminal. Trong bản dựng không hỗ trợ ký tự chiều rộng, các chuỗi được mã hóa bằng giá trị của thuộc tính :attr:`~window.encoding` của cửa sổ; giá trị mặc định là encoding mặc định của hệ thống, do :func:`locale.getencoding` trả về.

Các phương thức :meth:`~curses.window.addch` nhận một ký tự, có thể là chuỗi có độ dài 1, chuỗi byte có độ dài 1 hoặc một số nguyên.

Các hằng số được cung cấp cho các ký tự của bộ ký tự thay thế của terminal. Ví dụ, :const:`ACS_PLMINUS` là ký hiệu +/-, còn :const:`ACS_ULCORNER` là góc trên bên trái của một khung (tiện dụng để vẽ đường viền). Bạn cũng có thể sử dụng ký tự Unicode tương ứng.

Các cửa sổ ghi nhớ vị trí con trỏ sau thao tác cuối cùng, vì vậy nếu bỏ qua tọa độ *y,x*, chuỗi hoặc ký tự sẽ được hiển thị tại vị trí mà thao tác cuối cùng dừng lại. Bạn cũng có thể di chuyển con trỏ bằng phương thức ``move(y,x)``. Vì một số terminal luôn hiển thị con trỏ nhấp nháy, bạn nên đảm bảo con trỏ được đặt ở một vị trí không gây mất tập trung; việc con trỏ nhấp nháy ở một vị trí có vẻ ngẫu nhiên có thể gây khó hiểu.

Nếu ứng dụng của bạn hoàn toàn không cần con trỏ nhấp nháy, bạn có thể gọi ``curs_set(False)`` để làm con trỏ ẩn đi. Phương thức cửa sổ :meth:`~curses.window.leaveok` thực hiện điều khác: khi đối số của nó là true, curses giữ con trỏ ở vị trí mà lần cập nhật gần nhất đặt nó vào, thay vì di chuyển con trỏ về vị trí con trỏ của cửa sổ.


Thuộc tính và màu sắc
---------------------

Các ký tự có thể được hiển thị theo nhiều cách khác nhau. Các dòng trạng thái trong ứng dụng dạng văn bản thường được hiển thị bằng video đảo (reverse video), hoặc trình xem văn bản có thể cần làm nổi bật một số từ nhất định. curses hỗ trợ việc này bằng cách cho phép bạn chỉ định một thuộc tính cho mỗi ô trên màn hình.

Một thuộc tính là một số nguyên, trong đó mỗi bit biểu thị một thuộc tính khác nhau. Bạn có thể thử hiển thị văn bản với nhiều bit thuộc tính được thiết lập, nhưng curses không đảm bảo rằng mọi tổ hợp có thể đều khả dụng hoặc tất cả đều khác biệt về mặt trực quan. Điều đó phụ thuộc vào khả năng của terminal đang được sử dụng, vì vậy cách an toàn nhất là chỉ dùng các thuộc tính phổ biến nhất, được liệt kê ở đây.

+----------------------+-------------------------------------+
| Thuộc tính           | Mô tả                               |
+======================+=====================================+
| :const:`A_BLINK`     | Văn bản nhấp nháy                   |
+----------------------+-------------------------------------+
| :const:`A_BOLD`      | Văn bản cực sáng hoặc in đậm        |
+----------------------+-------------------------------------+
| :const:`A_DIM`       | Văn bản nửa sáng                    |
+----------------------+-------------------------------------+
| :const:`A_REVERSE`   | Văn bản đảo màu                     |
+----------------------+-------------------------------------+
| :const:`A_STANDOUT`  | Chế độ làm nổi bật tốt nhất hiện có |
+----------------------+-------------------------------------+
| :const:`A_UNDERLINE` | Văn bản gạch chân                   |
+----------------------+-------------------------------------+

Vì vậy, để hiển thị một dòng trạng thái đảo màu ở dòng đầu tiên của màn hình, bạn có thể viết mã::

   stdscr.addstr(0, 0, "Current mode: Typing mode",
                 curses.A_REVERSE)
   stdscr.refresh()

Thư viện curses cũng hỗ trợ màu trên những terminal cung cấp tính năng này. Terminal phổ biến nhất như vậy có lẽ là console Linux, tiếp theo là các xterm có màu.

Để sử dụng màu, bạn phải gọi hàm :func:`~curses.start_color` ngay sau khi gọi :func:`~curses.initscr`, nhằm khởi tạo bộ màu mặc định (hàm :func:`curses.wrapper` tự động thực hiện việc này). Sau khi hoàn tất, hàm :func:`~curses.has_colors` trả về TRUE nếu terminal đang sử dụng thực sự có thể hiển thị màu. (Lưu ý: curses sử dụng cách viết 'color' của tiếng Anh-Mỹ thay vì cách viết 'colour' của tiếng Anh-Canada/Anh. Nếu bạn quen với cách viết của Anh, bạn sẽ phải chấp nhận viết sai chính tả vì lợi ích của các hàm này.)

Thư viện curses duy trì một số lượng hữu hạn các cặp màu, mỗi cặp gồm màu tiền cảnh (hoặc màu văn bản) và màu nền. Bạn có thể lấy giá trị thuộc tính tương ứng với một cặp màu bằng hàm :func:`~curses.color_pair`; giá trị này có thể được thực hiện phép OR theo bit với các thuộc tính khác như
:const:`A_REVERSE`, nhưng một lần nữa, các kết hợp như vậy không được đảm bảo hoạt động trên mọi terminal.

Một ví dụ hiển thị một dòng văn bản bằng cặp màu 1::

   stdscr.addstr("Pretty text", curses.color_pair(1))
   stdscr.refresh()

Như tôi đã nói trước đó, một cặp màu gồm màu tiền cảnh và màu nền. Hàm ``init_pair(n, f, b)`` thay đổi định nghĩa của cặp màu *n*, thành màu tiền cảnh f và màu nền b. Cặp màu 0 được cố định là chữ trắng trên nền đen và không thể thay đổi.

Các màu được đánh số, và :func:`start_color` khởi tạo 8 màu cơ bản khi kích hoạt chế độ màu. Đó là: 0:đen, 1:đỏ, 2:xanh lá, 3:vàng, 4:xanh dương, 5:tím đỏ, 6:xanh lơ và 7:trắng. Mô-đun :mod:`curses` định nghĩa các hằng số có tên cho từng màu này:
:const:`curses.COLOR_BLACK`, :const:`curses.COLOR_RED`, vân vân.

Hãy tổng hợp tất cả những điều này. Để đổi màu 1 thành chữ màu đỏ trên nền trắng, bạn sẽ gọi::

   curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

Khi bạn thay đổi một cặp màu, mọi văn bản đã hiển thị bằng cặp màu đó sẽ đổi sang các màu mới. Bạn cũng có thể hiển thị văn bản mới bằng màu này với::

   stdscr.addstr(0,0, "RED ALERT!", curses.color_pair(1))

Các terminal cao cấp có thể thay đổi định nghĩa của những màu thực tế thành một giá trị RGB cụ thể. Điều này cho phép bạn đổi màu 1, vốn thường là màu đỏ, thành tím, xanh dương hoặc bất kỳ màu nào khác mà bạn muốn. Đáng tiếc là Linux console không hỗ trợ tính năng này, nên tôi không thể thử và cũng không thể cung cấp ví dụ. Bạn có thể kiểm tra xem terminal của mình có làm được điều này hay không bằng cách gọi
:func:`~curses.can_change_color`, trả về ``True`` nếu có khả năng này. Nếu may mắn sở hữu một terminal tài năng như vậy, hãy xem các man page của hệ thống để biết thêm thông tin.


Nhập liệu từ người dùng
=======================

Thư viện C curses chỉ cung cấp các cơ chế nhập liệu rất đơn giản. Python's
Mô-đun :mod:`curses` bổ sung một widget nhập văn bản cơ bản. (Các thư viện khác như :pypi:`Urwid` có những bộ widget phong phú hơn.)

Có ba phương thức để nhận dữ liệu đầu vào từ một cửa sổ:

* :meth:`~curses.window.get_wch` làm mới màn hình rồi chờ người dùng nhấn một phím, đồng thời hiển thị phím đó nếu trước đó đã gọi :func:`~curses.echo`. Bạn cũng có thể tùy chọn chỉ định tọa độ để di chuyển con trỏ đến đó trước khi tạm dừng.

* :meth:`~curses.window.getch` cũng thực hiện tương tự nhưng trả về mã của phím thay vì một ký tự. Với ncurses, đây là một byte trong phần mã hóa của phím theo locale hiện tại, vì vậy một ký tự được mã hóa bằng nhiều byte sẽ cần nhiều lần gọi, mỗi lần một byte.

* :meth:`~curses.window.getkey` thực hiện tương tự :meth:`!getch` nhưng trả về một chuỗi: một phím thông thường dưới dạng chuỗi 1 ký tự, còn một phím đặc biệt dưới dạng tên của nó, chẳng hạn như ``KEY_UP``.

Có thể không chờ người dùng bằng cách sử dụng
phương thức window :meth:`~curses.window.nodelay`. Sau ``nodelay(True)``, thao tác đọc đối với window sẽ trở thành non-blocking. Để báo hiệu rằng chưa có dữ liệu đầu vào nào sẵn sàng,
:meth:`!get_wch` và :meth:`!getkey` sẽ phát sinh một ngoại lệ, còn :meth:`!getch` trả về ``-1``. Ngoài ra còn có hàm :func:`~curses.halfdelay`, có thể được dùng để (về cơ bản) đặt bộ hẹn giờ cho mỗi lần đọc; nếu không có dữ liệu đầu vào nào khả dụng trong khoảng thời gian chờ đã chỉ định (tính bằng phần mười giây), thao tác đọc sẽ thất bại theo cùng cách đó.

Các phím đặc biệt như Page Up, Home hoặc các phím con trỏ được cả ba hàm trả về dưới dạng một trong các hằng số :ref:`KEY_* <curses-key-constants>`, tất cả đều lớn hơn 255. Bạn có thể so sánh giá trị được trả về với các hằng số như
:const:`curses.KEY_PPAGE`,
:const:`curses.KEY_HOME` hoặc :const:`curses.KEY_LEFT`. Vòng lặp chính của chương trình có thể trông như sau::

   while True:
       c = stdscr.get_wch()
       if c == 'p':
           PrintDocument()
       elif c == 'q':
           break  # Thoát khỏi vòng lặp while
       elif c == curses.KEY_HOME:
           x = y = 0

Mô-đun :mod:`curses.ascii` cung cấp các hàm xác định nhóm ASCII, nhận đối số là số nguyên hoặc chuỗi 1 ký tự; chúng có thể hữu ích khi viết các phép kiểm tra dễ đọc hơn cho những vòng lặp như vậy. Mô-đun này cũng cung cấp các hàm chuyển đổi nhận đối số là số nguyên hoặc chuỗi 1 ký tự và trả về cùng kiểu dữ liệu. Ví dụ, :func:`curses.ascii.ctrl` trả về ký tự điều khiển tương ứng với đối số của nó.

Ngoài ra còn có một phương thức để lấy toàn bộ một dòng,
:meth:`~curses.window.getstr`. Phương thức này không được sử dụng thường xuyên vì chức năng khá hạn chế; các phím chỉnh sửa duy nhất khả dụng là các ký tự xóa và xóa dòng, cùng với phím Enter dùng để kết thúc dòng. Phương thức này trả về một đối tượng bytes và có thể được giới hạn tùy chọn ở một số byte cố định.::

   curses.echo()            # Bật chế độ hiển thị ký tự

   # Nhận một dòng tối đa 15 byte, với con trỏ ở dòng trên cùng
   s = stdscr.getstr(0,0, 15)

Module :mod:`curses.textpad` cung cấp một hộp văn bản hỗ trợ một tập hợp keybinding tương tự Emacs. Nhiều phương thức của
lớp :class:`~curses.textpad.Textbox` hỗ trợ chỉnh sửa với việc xác thực đầu vào và thu thập kết quả chỉnh sửa có hoặc không có khoảng trắng ở cuối. Đây là một ví dụ::

   import curses
   from curses.textpad import Textbox, rectangle

   def main(stdscr):
       stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

       editwin = curses.newwin(5,30, 2,1)
       rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
       stdscr.refresh()

       box = Textbox(editwin)

       # Cho phép người dùng chỉnh sửa cho đến khi nhấn Ctrl-G.
       box.edit()

       # Lấy nội dung thu được
       message = box.gather()

Xem tài liệu thư viện về :mod:`curses.textpad` để biết thêm chi tiết.


Để biết thêm thông tin
======================

HOWTO này không đề cập đến một số chủ đề nâng cao, chẳng hạn như đọc nội dung màn hình hoặc bắt các sự kiện chuột từ một phiên bản xterm, nhưng trang thư viện Python dành cho module :mod:`curses` hiện đã khá đầy đủ. Bạn nên xem trang đó tiếp theo.

Nếu không chắc chắn về hành vi chi tiết của các hàm curses, hãy tham khảo các trang hướng dẫn sử dụng dành cho bản triển khai curses của bạn, dù đó là ncurses hay bản của một nhà cung cấp Unix độc quyền. Các trang hướng dẫn sử dụng sẽ ghi lại mọi điểm khác biệt và cung cấp danh sách đầy đủ tất cả các hàm, thuộc tính và :ref:`ACS_\* <curses-acs-codes>` ký tự có sẵn cho bạn.

Vì API curses rất lớn nên một số hàm không được hỗ trợ trong giao diện Python. Thường thì nguyên nhân không phải vì chúng khó triển khai, mà vì chưa có ai cần đến chúng. Ngoài ra, Python hiện chưa hỗ trợ thư viện menu đi kèm với ncurses. Các bản vá bổ sung hỗ trợ cho những thư viện này luôn được hoan nghênh; hãy xem `Hướng dẫn dành cho nhà phát triển Python <https://devguide.python.org/>`_ để tìm hiểu thêm về cách gửi bản vá cho Python.

* `Lập trình với NCURSES <https://invisible-island.net/ncurses/ncurses-intro.html>`_: một hướng dẫn dài dành cho các lập trình viên C.
* `Trang man của ncurses <https://linux.die.net/man/3/ncurses>`_
* `Câu hỏi thường gặp về ncurses <https://invisible-island.net/ncurses/ncurses.faq.html>`_
* `"Use curses... don't swear" <https://www.youtube.com/watch?v=eN1eZtjLEnU>`_: video về một bài nói chuyện tại PyCon 2013 về việc điều khiển terminal bằng curses hoặc Urwid.
* `"Console Applications with Urwid" <https://pyvideo.org/video/1568/console-applications-with-urwid>`_: video về một bài nói chuyện tại PyCon CA 2012, trình bày một số ứng dụng được viết bằng Urwid.

.. _`the Python Developer's Guide`: https://devguide.python.org/
.. _`Writing Programs with NCURSES`: https://invisible-island.net/ncurses/ncurses-intro.html
.. _`The ncurses man page`: https://linux.die.net/man/3/ncurses
.. _`The ncurses FAQ`: https://invisible-island.net/ncurses/ncurses.faq.html
.. _`"Use curses... don't swear"`: https://www.youtube.com/watch?v=eN1eZtjLEnU
.. _`"Console Applications with Urwid"`: https://pyvideo.org/video/1568/console-applications-with-urwid
