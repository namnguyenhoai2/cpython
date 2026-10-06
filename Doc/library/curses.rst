:mod:`!curses` --- Xử lý terminal cho màn hình ô ký tự
======================================================

.. module:: curses
   :synopsis: Giao diện cho thư viện curses, cung cấp khả năng xử lý terminal di động.

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>
.. sectionauthor:: Eric Raymond <esr@thyrsus.com>

**Mã nguồn:** :source:`Lib/curses`

--------------

Mô-đun :mod:`!curses` cung cấp giao diện cho thư viện curses, tiêu chuẩn thực tế để xử lý terminal nâng cao và di động.

Mặc dù curses được sử dụng phổ biến nhất trong môi trường Unix, các phiên bản cũng có sẵn cho Windows, DOS và có thể cả các hệ thống khác. Mô-đun mở rộng này được thiết kế để tương thích với API của ncurses, một thư viện curses mã nguồn mở được lưu trữ trên Linux và các biến thể BSD của Unix.

.. include:: ../includes/wasm-mobile-notavail.rst

.. include:: ../includes/optional-module.rst

.. availability:: Unix.

.. note::

   Bất cứ khi nào tài liệu đề cập đến *ký tự*, ký tự đó có thể được chỉ định dưới dạng số nguyên, chuỗi Unicode gồm một ký tự hoặc chuỗi byte gồm một byte. Số nguyên là mã của một byte được mã hóa đơn, có thể kết hợp với các thuộc tính và một cặp màu, như được trả về bởi :meth:`window.inch`.

   Bất cứ khi nào tài liệu đề cập đến *chuỗi ký tự*, chuỗi đó có thể được chỉ định dưới dạng chuỗi Unicode hoặc chuỗi byte.

.. note::

   Việc có thể sử dụng curses từ nhiều thread hay không phụ thuộc vào thư viện nền tảng và cách thư viện đó được xây dựng. Trong nhiều bản triển khai, bao gồm cả bản build mặc định của ncurses, trạng thái màn hình được dùng chung và không an toàn với thread; vì các phương thức chặn và làm mới (chẳng hạn như :meth:`~window.getch` và :meth:`~window.refresh`) giải phóng :term:`GIL`, việc sử dụng không đồng bộ từ nhiều thread có thể khiến trình thông dịch bị lỗi. Hãy tuần tự hóa các lệnh gọi.

.. seealso::

   Mô-đun :mod:`curses.ascii`
      Các tiện ích để làm việc với các ký tự ASCII, bất kể cài đặt locale của bạn.

   Mô-đun :mod:`curses.panel`
      Một phần mở rộng ngăn xếp panel bổ sung chiều sâu cho các cửa sổ curses.

   Mô-đun :mod:`curses.textpad`
      Widget văn bản có thể chỉnh sửa cho curses, hỗ trợ các liên kết phím kiểu :program:`Emacs`\ .

   :ref:`curses-howto`
      Tài liệu hướng dẫn sử dụng curses với Python, do Andrew Kuchling và Eric Raymond biên soạn.


.. _curses-functions:

Các hàm
-------

Mô-đun :mod:`!curses` định nghĩa ngoại lệ sau:


.. exception:: error

   Ngoại lệ được đưa ra khi một hàm của thư viện curses trả về lỗi.

.. note::

   Bất cứ khi nào đối số *x* hoặc *y* của một hàm hoặc phương thức là tùy chọn, chúng sẽ mặc định là vị trí con trỏ hiện tại. Khi *attr* là tùy chọn, nó sẽ mặc định là :const:`A_NORMAL`.

Mô-đun :mod:`!curses` định nghĩa các hàm sau:


.. function:: assume_default_colors(fg, bg, /)

   Cho phép sử dụng các giá trị mặc định cho màu sắc trên những terminal hỗ trợ tính năng này. Sử dụng tùy chọn này để hỗ trợ độ trong suốt trong ứng dụng của bạn.

   * Gán màu tiền cảnh/hậu cảnh mặc định của terminal cho số màu ``-1``. Vì vậy, ``init_pair(x, COLOR_RED, -1)`` sẽ khởi tạo cặp *x* với tiền cảnh màu đỏ trên nền mặc định, còn ``init_pair(x, -1, COLOR_BLUE)`` sẽ khởi tạo cặp *x* với tiền cảnh mặc định trên nền màu xanh dương.

   * Thay đổi định nghĩa của cặp màu ``0`` thành ``(fg, bg)``.

   Đây là một phần mở rộng của ncurses.

   .. versionadded:: 3.14


.. function:: baudrate()

   Trả về tốc độ đầu ra của terminal tính bằng bit trên giây. Trên các trình mô phỏng terminal bằng phần mềm, giá trị này sẽ cố định ở mức cao. Tùy chọn này được giữ lại vì lý do lịch sử; trước đây, nó được dùng để viết các vòng lặp xuất dữ liệu nhằm tạo độ trễ và đôi khi thay đổi giao diện tùy theo tốc độ đường truyền.


.. function:: beep()

   Phát ra âm thanh chú ý ngắn.


.. function:: can_change_color()

   Trả về ``True`` hoặc ``False``, tùy thuộc vào việc lập trình viên có thể thay đổi màu hiển thị của terminal hay không.


.. function:: cbreak()

   Chuyển sang chế độ cbreak. Trong chế độ cbreak (đôi khi được gọi là chế độ "rare"), cơ chế đệm dòng bình thường của tty bị tắt và các ký tự có thể được đọc từng ký tự một. Tuy nhiên, không giống chế độ raw, các ký tự đặc biệt (ngắt, thoát, tạm dừng và điều khiển luồng) vẫn giữ nguyên tác động lên trình điều khiển tty và chương trình gọi. Gọi :func:`raw` trước, sau đó gọi :func:`cbreak` sẽ để terminal ở chế độ cbreak.


.. function:: color_content(color_number)

   Trả về cường độ của các thành phần đỏ, xanh lá và xanh dương (RGB) trong màu *color_number*, giá trị này phải nằm giữa ``0`` và ``COLORS - 1``. Trả về một bộ 3 giá trị, chứa các giá trị R,G,B của màu đã cho, nằm trong khoảng từ ``0`` (không có thành phần) đến ``1000`` (lượng thành phần tối đa). Phát sinh ngoại lệ nếu màu không được hỗ trợ.


.. function:: color_pair(pair_number)

   Trả về giá trị thuộc tính để hiển thị văn bản trong cặp màu được chỉ định. Chỉ 256 cặp màu đầu tiên được hỗ trợ. Giá trị thuộc tính này có thể được kết hợp với :const:`A_STANDOUT`, :const:`A_REVERSE` và các thuộc tính :const:`!A_\*` khác. :func:`pair_number` là hàm đối ứng với hàm này.


.. function:: curs_set(visibility)

   Đặt trạng thái con trỏ. *visibility* có thể được đặt thành ``0``, ``1`` hoặc ``2``, tương ứng với vô hình, bình thường hoặc rất dễ nhìn thấy. Nếu terminal hỗ trợ trạng thái hiển thị được yêu cầu, hãy trả về trạng thái con trỏ trước đó; nếu không, phát sinh ngoại lệ. Trên nhiều terminal, chế độ "visible" là con trỏ gạch chân, còn chế độ "very visible" là con trỏ khối.


.. function:: def_prog_mode()

   Lưu chế độ terminal hiện tại làm chế độ "program", tức chế độ khi chương trình đang chạy sử dụng curses. (Chế độ đối ứng là chế độ "shell", khi chương trình không sử dụng curses.) Các lần gọi :func:`reset_prog_mode` tiếp theo sẽ khôi phục chế độ này.


.. function:: def_shell_mode()

   Lưu chế độ terminal hiện tại làm chế độ "shell", tức chế độ khi chương trình đang chạy không sử dụng curses. (Chế độ đối ứng là chế độ "program", khi chương trình sử dụng các khả năng của curses.) Các lần gọi tiếp theo
   :func:`reset_shell_mode` sẽ khôi phục chế độ này.


.. function:: delay_output(ms)

   Chèn khoảng dừng *ms* mili giây vào đầu ra.


.. function:: doupdate()

   Cập nhật màn hình vật lý. Thư viện curses duy trì hai cấu trúc dữ liệu: một cấu trúc biểu diễn nội dung hiện tại của màn hình vật lý và một màn hình ảo biểu diễn trạng thái mong muốn tiếp theo. Hàm :func:`doupdate` cập nhật màn hình vật lý để khớp với màn hình ảo.

   Màn hình ảo có thể được cập nhật bằng một lệnh gọi :meth:`~window.noutrefresh` sau khi thực hiện các thao tác ghi như :meth:`~window.addstr` trên một cửa sổ. Thông thường
   lệnh gọi :meth:`~window.refresh` chỉ đơn giản là :meth:`!noutrefresh` theo sau bởi :func:`!doupdate`; nếu phải cập nhật nhiều cửa sổ, bạn có thể tăng hiệu năng và có thể giảm hiện tượng nhấp nháy màn hình bằng cách thực hiện các lệnh gọi :meth:`!noutrefresh` trên tất cả cửa sổ, sau đó thực hiện một lệnh gọi :func:`!doupdate` duy nhất.


.. function:: echo()

   Bật chế độ echo. Trong chế độ echo, mỗi ký tự nhập vào được hiển thị trên màn hình ngay khi được nhập.


.. function:: endwin()

   Hủy khởi tạo thư viện và đưa terminal về trạng thái bình thường.


.. function:: erasechar()

   Trả về ký tự xóa hiện tại của người dùng dưới dạng đối tượng bytes một byte. Trên các hệ điều hành Unix, đây là thuộc tính của tty điều khiển chương trình curses và không do chính thư viện curses thiết lập.


.. function:: filter()

   Nếu được sử dụng, thủ tục :func:`.filter` phải được gọi trước khi gọi :func:`initscr`. Khi đó, trong quá trình khởi tạo, :envvar:`LINES` được đặt thành ``1``; các khả năng ``clear``, ``cup``, ``cud``, ``cud1``, ``cuu1``, ``cuu``, ``vpa`` bị vô hiệu hóa; và chuỗi ``home`` được đặt thành giá trị của ``cr``. Kết quả là con trỏ bị giới hạn trong dòng hiện tại, và các cập nhật màn hình cũng vậy. Điều này có thể được dùng để bật tính năng chỉnh sửa từng dòng theo từng ký tự mà không chạm đến phần còn lại của màn hình.


.. function:: flash()

   Làm màn hình nhấp nháy. Nghĩa là chuyển màn hình sang chế độ video đảo ngược rồi chuyển lại trong một khoảng thời gian ngắn. Một số người thích một 'chuông hiển thị' như vậy hơn tín hiệu chú ý bằng âm thanh do :func:`beep` tạo ra.


.. function:: flushinp()

   Xóa tất cả các bộ đệm đầu vào. Thao tác này loại bỏ mọi dữ liệu typeahead mà người dùng đã nhập nhưng chương trình chưa xử lý.


.. function:: getmouse()

   Sau khi :meth:`~window.getch` trả về :const:`KEY_MOUSE` để báo hiệu một sự kiện chuột, cần gọi phương thức này để lấy sự kiện chuột đang chờ trong hàng đợi, được biểu diễn dưới dạng tuple 5 phần tử ``(id, x, y, z, bstate)``. *id* là một giá trị ID dùng để phân biệt nhiều thiết bị, còn *x*, *y*, *z* là các tọa độ của sự kiện. (*z* hiện chưa được sử dụng.) *bstate* là một giá trị số nguyên, trong đó các bit sẽ được thiết lập để cho biết loại sự kiện, và sẽ là phép OR theo bit của một hoặc nhiều hằng số sau đây, trong đó *n* là số nút từ 1 đến 5:
   :const:`BUTTONn_PRESSED`, :const:`BUTTONn_RELEASED`, :const:`BUTTONn_CLICKED`,
   :const:`BUTTONn_DOUBLE_CLICKED`, :const:`BUTTONn_TRIPLE_CLICKED`,
   :const:`BUTTON_SHIFT`, :const:`BUTTON_CTRL`, :const:`BUTTON_ALT`.

   .. versionchanged:: 3.10
      Các hằng số ``BUTTON5_*`` hiện được cung cấp nếu thư viện curses bên dưới cung cấp chúng.


.. function:: getsyx()

   Trả về tọa độ hiện tại của con trỏ màn hình ảo dưới dạng tuple ``(y, x)``. Nếu :meth:`leaveok <window.leaveok>` hiện là ``True``, thì trả về ``(-1, -1)``.


.. function:: getwin(file)

   Đọc dữ liệu liên quan đến cửa sổ được lưu trong tệp bởi một lần gọi :meth:`window.putwin` trước đó. Sau đó, thủ tục này tạo và khởi tạo một cửa sổ mới bằng dữ liệu đó, rồi trả về đối tượng cửa sổ mới. Đối số *file* phải là một đối tượng tệp được mở để đọc ở chế độ nhị phân.


.. function:: has_colors()

   Trả về ``True`` nếu terminal có thể hiển thị màu; nếu không, trả về ``False``.

.. function:: has_extended_color_support()

   Trả về ``True`` nếu module hỗ trợ extended colors; nếu không, trả về ``False``. Hỗ trợ extended colors cho phép sử dụng hơn 256 cặp màu trên các terminal hỗ trợ hơn 16 màu (ví dụ: xterm-256color).

   Hỗ trợ extended colors yêu cầu ncurses phiên bản 6.1 trở lên.

   .. versionadded:: 3.10

.. function:: has_ic()

   Trả về ``True`` nếu terminal có các khả năng chèn và xóa ký tự. Hàm này chỉ được giữ lại vì lý do lịch sử, vì mọi trình terminal emulator hiện đại đều có các khả năng này.


.. function:: has_il()

   Trả về ``True`` nếu terminal có các khả năng chèn và xóa dòng, hoặc có thể mô phỏng chúng bằng các vùng cuộn. Hàm này chỉ được giữ lại vì lý do lịch sử, vì mọi trình terminal emulator hiện đại đều có các khả năng này.


.. function:: has_key(ch)

   Nhận một giá trị phím *ch*, rồi trả về ``True`` nếu loại terminal hiện tại nhận diện một phím có giá trị đó.


.. function:: halfdelay(tenths)

   Được dùng cho chế độ half-delay, tương tự chế độ cbreak ở chỗ các ký tự do người dùng nhập sẽ ngay lập tức được cung cấp cho chương trình. Tuy nhiên, sau khi chờ *tenths* phần mười giây, hãy nêu một ngoại lệ nếu chưa có gì được nhập. Giá trị của *tenths* phải là một số nằm giữa ``1`` và ``255``. Sử dụng
   :func:`nocbreak` để thoát khỏi chế độ half-delay.


.. function:: init_color(color_number, r, g, b)

   Thay đổi định nghĩa của một màu, bằng cách cung cấp số của màu cần thay đổi, theo sau là ba giá trị RGB (cho mức độ của các thành phần đỏ, lục và lam). Giá trị của *color_number* phải nằm giữa ``0`` và ``COLORS - 1``. Mỗi giá trị *r*, *g*, *b* phải nằm giữa ``0`` và ``1000``. Khi sử dụng :func:`init_color`, mọi lần xuất hiện của màu đó trên màn hình sẽ ngay lập tức chuyển sang định nghĩa mới. Hàm này không thực hiện thao tác nào trên hầu hết các terminal; nó chỉ hoạt động nếu :func:`can_change_color` trả về ``True``.


.. function:: init_pair(pair_number, fg, bg)

   Thay đổi định nghĩa của một color-pair. Hàm này nhận ba đối số: số của color-pair cần thay đổi, số của màu foreground và số của màu background. Giá trị của *pair_number* phải nằm giữa ``1`` và ``COLOR_PAIRS - 1`` (color pair ``0`` chỉ có thể được thay đổi bằng
   :func:`use_default_colors` và :func:`assume_default_colors`). Giá trị của các đối số *fg* và *bg* phải nằm giữa ``0`` và ``COLORS - 1``, hoặc sau khi gọi :func:`!use_default_colors` hoặc
   :func:`!assume_default_colors`, ``-1``. Nếu color-pair đã được khởi tạo trước đó, màn hình sẽ được làm mới và mọi lần xuất hiện của color-pair đó sẽ được thay đổi theo định nghĩa mới.


.. function:: initscr()

   Khởi tạo thư viện. Trả về một đối tượng :ref:`window <curses-window-objects>` đại diện cho toàn bộ màn hình.

   Xem :func:`setupterm` để biết lưu ý về việc gọi nó trước hàm này.

   .. note::

      Nếu xảy ra lỗi khi mở terminal, thư viện curses bên dưới có thể khiến trình thông dịch thoát.


.. function:: intrflush(flag)

   Nếu *flag* là ``True``, việc nhấn phím ngắt (interrupt, break hoặc quit) sẽ xóa toàn bộ đầu ra trong hàng đợi của terminal driver. Nếu *flag* là ``False``, sẽ không thực hiện việc xóa nào.


.. function:: is_term_resized(nlines, ncols)

   Trả về ``True`` nếu :func:`resize_term` sẽ sửa đổi cấu trúc cửa sổ, nếu không thì trả về ``False``.


.. function:: isendwin()

   Trả về ``True`` nếu :func:`endwin` đã được gọi (nghĩa là thư viện curses đã được deinitialize).


.. function:: keyname(k)

   Trả về tên của phím có số *k* dưới dạng đối tượng bytes. Tên của phím tạo ra ký tự ASCII có thể in được chính là ký tự của phím đó. Tên của tổ hợp phím điều khiển là một đối tượng bytes gồm hai byte, bao gồm dấu mũ (``b'^'``) theo sau là ký tự ASCII có thể in được tương ứng. Tên của tổ hợp phím Alt (128--255) là một đối tượng bytes gồm tiền tố ``b'M-'`` theo sau là tên của ký tự ASCII tương ứng.

   Ném :exc:`ValueError` nếu *k* là số âm.


.. function:: killchar()

   Trả về một đối tượng bytes chứa ký tự xóa dòng hiện tại của người dùng dưới dạng đối tượng bytes một byte. Trên các hệ điều hành Unix, đây là thuộc tính của tty điều khiển chương trình curses và không được chính thư viện curses thiết lập.


.. function:: longname()

   Trả về một đối tượng bytes chứa trường tên dài của terminfo mô tả terminal hiện tại. Độ dài tối đa của phần mô tả chi tiết là 128 ký tự. Phần này chỉ được định nghĩa sau khi gọi :func:`initscr`.


.. function:: meta(flag)

   Nếu *flag* là ``True``, cho phép nhập các ký tự 8-bit. Nếu *flag* là ``False``, chỉ cho phép các ký tự 7-bit.


.. function:: mouseinterval(interval)

   Đặt thời gian tối đa tính bằng mili giây có thể trôi qua giữa các sự kiện nhấn và nhả để chúng được nhận dạng là một lần nhấp, rồi trả về giá trị khoảng thời gian trước đó. Giá trị mặc định là 166 mili giây, tức một phần sáu giây. Sử dụng *interval* âm để lấy giá trị khoảng thời gian mà không thay đổi nó.


.. function:: mousemask(mousemask)

   Đặt các sự kiện chuột sẽ được báo cáo và trả về một tuple ``(availmask, oldmask)``. *availmask* cho biết những sự kiện chuột được chỉ định nào có thể được báo cáo; nếu hoàn toàn thất bại, hàm trả về ``0``. *oldmask* là giá trị trước đó của mặt nạ sự kiện chuột. Nếu hàm này chưa bao giờ được gọi, sẽ không có sự kiện chuột nào được báo cáo.


.. function:: napms(ms)

   Tạm dừng trong *ms* mili giây.


.. function:: newpad(nlines, ncols)

   Tạo và trả về một con trỏ đến cấu trúc dữ liệu pad mới với số dòng và cột đã cho. Trả về một pad dưới dạng đối tượng cửa sổ.

   Pad tương tự như cửa sổ, ngoại trừ việc nó không bị giới hạn bởi kích thước màn hình và không nhất thiết được liên kết với một phần cụ thể của màn hình. Có thể sử dụng pad khi cần một cửa sổ lớn nhưng mỗi lần chỉ hiển thị một phần cửa sổ trên màn hình. Pad không tự động làm mới, chẳng hạn do cuộn hoặc hiển thị dữ liệu nhập. Các phương thức :meth:`~window.refresh` và :meth:`~window.noutrefresh` của pad yêu cầu 6 đối số để xác định phần pad cần hiển thị và vị trí trên màn hình được dùng để hiển thị. Các đối số là *pminrow*, *pmincol*, *sminrow*, *smincol*, *smaxrow*, *smaxcol*; các đối số *p* tham chiếu đến góc trên bên trái của vùng pad cần hiển thị, còn các đối số *s* xác định một vùng cắt trên màn hình, trong đó vùng pad sẽ được hiển thị.


.. function:: newwin(nlines, ncols)
              newwin(nlines, ncols, begin_y, begin_x)

   Trả về một :ref:`window <curses-window-objects>` mới, có góc trên bên trái tại ``(begin_y, begin_x)``, và có chiều cao/chiều rộng là *nlines*/*ncols*.

   Theo mặc định, cửa sổ sẽ mở rộng từ vị trí đã chỉ định đến góc dưới bên phải của màn hình.


.. function:: nl(flag=True)

   Bật chế độ newline. Chế độ này chuyển phím return thành newline khi nhập, và chuyển newline thành return cùng line-feed khi xuất. Chế độ newline ban đầu được bật.

   Nếu *flag* là ``False``, hiệu ứng sẽ giống như khi gọi :func:`nonl`.


.. function:: nocbreak()

   Thoát khỏi chế độ cbreak. Trở về chế độ "cooked" thông thường với bộ đệm theo dòng.


.. function:: noecho()

   Thoát khỏi chế độ echo. Tắt việc lặp lại các ký tự nhập vào.


.. function:: nonl()

   Thoát khỏi chế độ newline. Tắt việc chuyển return thành newline khi nhập, đồng thời tắt việc chuyển newline ở cấp thấp thành newline/return khi xuất (nhưng điều này không thay đổi hành vi của ``addch('\n')``, vốn luôn thực hiện tương đương return và line feed trên màn hình ảo). Khi tắt chuyển đổi, đôi khi curses có thể tăng tốc một chút thao tác di chuyển theo chiều dọc; đồng thời, nó sẽ có thể phát hiện phím return khi nhập.


.. function:: noqiflush()

   Khi sử dụng routine :func:`!noqiflush`, việc flush thông thường các hàng đợi đầu vào và đầu ra liên kết với các ký tự ``INTR``, ``QUIT`` và ``SUSP`` sẽ không được thực hiện. Bạn có thể muốn gọi :func:`!noqiflush` trong signal handler nếu muốn đầu ra tiếp tục như thể interrupt chưa xảy ra sau khi handler kết thúc.


.. function:: noraw()

   Thoát khỏi chế độ raw. Trở về chế độ "cooked" bình thường với bộ đệm theo dòng.


.. function:: pair_content(pair_number)

   Trả về một tuple ``(fg, bg)`` chứa các màu của cặp màu được yêu cầu. Giá trị của *pair_number* phải nằm trong khoảng từ ``0`` đến ``COLOR_PAIRS - 1``.


.. function:: pair_number(attr)

   Trả về số của cặp màu được đặt bởi giá trị thuộc tính *attr*.
   :func:`color_pair` là hàm tương ứng với hàm này.


.. function:: putp(str)

   Tương đương với ``tputs(str, 1, putchar)``; phát ra giá trị của một capability terminfo được chỉ định, dưới dạng đối tượng bytes, cho terminal hiện tại. Lưu ý rằng đầu ra của :func:`putp` luôn được gửi đến standard output.

   Phải gọi :func:`setupterm` (hoặc :func:`initscr`) trước.


.. function:: qiflush([flag])

   Nếu *flag* là ``False``, hiệu ứng sẽ giống như gọi :func:`noqiflush`. Nếu *flag* là ``True``, hoặc không cung cấp đối số, các queue sẽ được flush khi đọc các ký tự điều khiển này.


.. function:: raw()

   Bật raw mode. Trong raw mode, tính năng buffering dòng thông thường và việc xử lý các phím interrupt, quit, suspend và flow control bị tắt; các ký tự được cung cấp cho các hàm nhập của curses từng ký tự một.


.. function:: reset_prog_mode()

   Khôi phục terminal về chế độ "program", như đã được lưu trước đó bởi
   :func:`def_prog_mode`.


.. function:: reset_shell_mode()

   Khôi phục terminal về chế độ "shell", như đã được lưu trước đó bởi
   :func:`def_shell_mode`.


.. function:: resetty()

   Khôi phục trạng thái của các chế độ terminal về trạng thái tại lần gọi gần nhất đến
   :func:`savetty`.


.. function:: resize_term(nlines, ncols)

   Hàm backend được :func:`resizeterm` sử dụng, thực hiện phần lớn công việc; khi thay đổi kích thước các cửa sổ, :func:`resize_term` sẽ điền các vùng được mở rộng bằng khoảng trống. Ứng dụng gọi hàm này nên điền các vùng đó bằng dữ liệu phù hợp. Hàm :func:`!resize_term` cố gắng thay đổi kích thước tất cả các cửa sổ. Tuy nhiên, do calling convention của pads, không thể thay đổi kích thước các pad này nếu không có thêm tương tác với ứng dụng.


.. function:: resizeterm(nlines, ncols)

   Thay đổi kích thước các cửa sổ chuẩn và hiện tại theo các kích thước được chỉ định, đồng thời điều chỉnh các dữ liệu bookkeeping khác được thư viện curses sử dụng để ghi lại kích thước cửa sổ (đặc biệt là trình xử lý SIGWINCH).


.. function:: savetty()

   Lưu trạng thái hiện tại của các chế độ terminal vào một bộ đệm, có thể được sử dụng bởi
   :func:`resetty`.

.. function:: get_escdelay()

   Truy xuất giá trị được đặt bởi :func:`set_escdelay`.

   .. versionadded:: 3.9

.. function:: set_escdelay(ms)

   Đặt số mili giây cần chờ sau khi đọc một ký tự escape để phân biệt giữa một ký tự escape riêng lẻ được nhập bằng bàn phím và các chuỗi escape được gửi bởi các phím con trỏ và phím chức năng.

   .. versionadded:: 3.9

.. function:: get_tabsize()

   Truy xuất giá trị được đặt bởi :func:`set_tabsize`.

   .. versionadded:: 3.9

.. function:: set_tabsize(size)

   Đặt số cột mà thư viện curses sử dụng khi chuyển đổi một ký tự tab thành các dấu cách trong lúc thêm tab vào một cửa sổ.

   .. versionadded:: 3.9

.. function:: setsyx(y, x)

   Đặt con trỏ màn hình ảo thành *y*, *x*. Nếu *y* và *x* đều là ``-1``, thì
   :meth:`leaveok <window.leaveok>` được đặt ``True``.


.. function:: setupterm(term=None, fd=-1)

   Khởi tạo terminal. *term* là một chuỗi cung cấp tên terminal hoặc ``None``; nếu bị bỏ qua hoặc là ``None``, giá trị của
   :envvar:`TERM` biến môi trường sẽ được sử dụng. *fd* là file descriptor mà mọi chuỗi khởi tạo sẽ được gửi đến; nếu không được cung cấp hoặc là ``-1``, file descriptor của ``sys.stdout`` sẽ được sử dụng.

   Phát sinh :exc:`curses.error` nếu không tìm thấy terminal hoặc không thể đọc mục nhập terminfo của terminal đó. Nếu terminal đã được khởi tạo, hàm này không có tác dụng.

   .. note::

      Việc gọi :func:`initscr` sau :func:`setupterm` sẽ làm rò rỉ terminal mà :func:`setupterm` đã cấp phát: thư viện curses chỉ duy trì một terminal hiện tại và không giải phóng terminal đã được cấp phát trước đó.


.. function:: start_color()

   Phải gọi hàm này nếu lập trình viên muốn sử dụng màu sắc, và phải gọi trước mọi routine thao tác màu khác. Một cách làm tốt là gọi routine này ngay sau :func:`initscr`.

   :func:`start_color` khởi tạo tám màu cơ bản (đen, đỏ, xanh lá, vàng, xanh dương, tím magenta, xanh cyan và trắng), cùng hai biến toàn cục trong module :mod:`!curses`, là :const:`COLORS` và :const:`COLOR_PAIRS`, chứa số lượng màu và cặp màu tối đa mà terminal có thể hỗ trợ. Hàm này cũng khôi phục màu trên terminal về các giá trị khi terminal vừa được bật.


.. function:: termattrs()

   Trả về phép OR logic của tất cả thuộc tính hiển thị mà terminal hỗ trợ. Thông tin này hữu ích khi chương trình curses cần kiểm soát hoàn toàn giao diện của màn hình.


.. function:: termname()

   Trả về giá trị của biến môi trường :envvar:`TERM` dưới dạng đối tượng bytes, được cắt ngắn còn 14 ký tự.


.. function:: tigetflag(capname)

   Trả về giá trị của capability Boolean tương ứng với tên capability terminfo *capname* dưới dạng số nguyên. Trả về giá trị ``-1`` nếu *capname* không phải là capability Boolean, hoặc ``0`` nếu capability này bị hủy hoặc không có trong mô tả terminal.

   Phải gọi :func:`setupterm` (hoặc :func:`initscr`) trước.


.. function:: tigetnum(capname)

   Trả về giá trị của capability số tương ứng với tên capability terminfo *capname* dưới dạng số nguyên. Trả về giá trị ``-2`` nếu *capname* không phải là capability số, hoặc ``-1`` nếu capability này bị hủy hoặc không có trong mô tả terminal.

   Phải gọi :func:`setupterm` (hoặc :func:`initscr`) trước.


.. function:: tigetstr(capname)

   Trả về giá trị của capability chuỗi tương ứng với tên capability terminfo *capname* dưới dạng đối tượng bytes. Trả về ``None`` nếu *capname* không phải là "string capability" của terminfo, hoặc bị hủy hay không có trong mô tả terminal.

   Phải gọi :func:`setupterm` (hoặc :func:`initscr`) trước.


.. function:: tparm(str[, ...])

   Khởi tạo đối tượng bytes *str* với các tham số được cung cấp, trong đó *str* phải là một chuỗi byte có tham số thu được từ cơ sở dữ liệu terminfo. Ví dụ: ``tparm(tigetstr("cup"), 5, 3)`` có thể cho kết quả là ``b'\033[6;4H'``, kết quả chính xác tùy thuộc vào loại terminal. Có thể cung cấp tối đa chín tham số số nguyên.

   Phải gọi :func:`setupterm` (hoặc :func:`initscr`) trước.


.. function:: typeahead(fd)

   Chỉ định rằng file descriptor *fd* được sử dụng để kiểm tra typeahead. Nếu *fd* là ``-1``, thì không thực hiện kiểm tra typeahead.

   Thư viện curses thực hiện “tối ưu hóa line-breakout” bằng cách định kỳ tìm typeahead trong khi cập nhật màn hình. Nếu tìm thấy dữ liệu đầu vào và dữ liệu đó đến từ một tty, lần cập nhật hiện tại sẽ được trì hoãn cho đến khi refresh hoặc doupdate được gọi lại, giúp phản hồi nhanh hơn với các lệnh đã được nhập trước. Hàm này cho phép chỉ định một file descriptor khác để kiểm tra typeahead.


.. function:: unctrl(ch)

   Trả về một đối tượng bytes là biểu diễn có thể in được của ký tự *ch*; mọi thuộc tính và color pair đều bị bỏ qua. Các ký tự điều khiển được biểu diễn bằng dấu mũ theo sau là ký tự đó, chẳng hạn như ``b'^C'``. Các ký tự có thể in được giữ nguyên.


.. function:: ungetch(ch)

   Đưa *ch* vào để lần gọi :meth:`~window.getch` tiếp theo trả về nó.

   *ch* có thể là một số nguyên (mã phím hoặc mã của một byte đã mã hóa), một byte hoặc một chuỗi có độ dài 1 được mã hóa thành một byte duy nhất.

   .. note::

      Chỉ có thể đẩy một *ch* trước khi gọi :meth:`!getch`.


.. function:: update_lines_cols()

   Cập nhật các biến mô-đun :const:`LINES` và :const:`COLS`. Hữu ích để phát hiện việc thay đổi kích thước màn hình theo cách thủ công.

   .. versionadded:: 3.5


.. function:: unget_wch(ch)

   Đẩy *ch* để lần gọi :meth:`~window.get_wch` tiếp theo sẽ trả về giá trị đó.

   *ch* có thể là một số nguyên (mã ký tự, không phải mã phím) hoặc một chuỗi có độ dài bằng 1.

   .. note::

      Chỉ có thể đẩy một *ch* trước khi gọi :meth:`!get_wch`.

   .. versionadded:: 3.3


.. function:: ungetmouse(id, x, y, z, bstate)

   Đẩy một sự kiện :const:`KEY_MOUSE` vào hàng đợi đầu vào, liên kết dữ liệu trạng thái đã cho với sự kiện đó.


.. function:: use_env(flag)

   Nếu sử dụng, hàm này phải được gọi trước khi gọi :func:`initscr` hoặc newterm. Khi *flag* là ``False``, các giá trị về số dòng và số cột được chỉ định trong cơ sở dữ liệu terminfo sẽ được sử dụng, ngay cả khi các biến môi trường :envvar:`LINES` và :envvar:`COLUMNS` (được sử dụng theo mặc định) được thiết lập, hoặc nếu curses đang chạy trong một cửa sổ (trong trường hợp đó, hành vi mặc định sẽ là sử dụng kích thước cửa sổ nếu
   :envvar:`LINES` và :envvar:`COLUMNS` chưa được thiết lập).


.. function:: use_default_colors()

   Tương đương với ``assume_default_colors(-1, -1)``.


.. function:: wrapper(func, /, *args, **kwargs)

   Khởi tạo curses và gọi một đối tượng có thể gọi, *func*, đối tượng này sẽ là phần còn lại của ứng dụng sử dụng curses của bạn. Nếu ứng dụng phát sinh ngoại lệ, hàm này sẽ khôi phục terminal về trạng thái bình thường trước khi phát sinh lại ngoại lệ và tạo traceback. Sau đó, đối tượng có thể gọi *func* được truyền cửa sổ chính 'stdscr' làm đối số đầu tiên, tiếp theo là mọi đối số khác được truyền cho :func:`!wrapper`. Trước khi gọi *func*, :func:`!wrapper` bật chế độ cbreak, tắt echo, bật keypad của terminal và khởi tạo màu nếu terminal hỗ trợ màu. Khi thoát (dù bình thường hay do ngoại lệ), hàm này khôi phục chế độ cooked, bật echo và tắt keypad của terminal.


.. _curses-window-objects:

Đối tượng cửa sổ
----------------

.. class:: window

   Các đối tượng cửa sổ, được trả về bởi :func:`initscr` và :func:`newwin` ở trên, có các phương thức và thuộc tính sau:


.. method:: window.addch(ch[, attr])
            window.addch(y, x, ch[, attr])

   Vẽ ký tự *ch* tại ``(y, x)`` với các thuộc tính *attr*, ghi đè mọi ký tự đã được vẽ trước đó tại vị trí đó. Theo mặc định, vị trí ký tự và các thuộc tính là các thiết lập hiện tại của đối tượng cửa sổ.

   .. note::

      Ghi bên ngoài cửa sổ, cửa sổ con hoặc pad sẽ phát sinh :exc:`curses.error`. Việc cố gắng ghi vào góc dưới bên phải của cửa sổ, cửa sổ con hoặc pad sẽ khiến một ngoại lệ được phát sinh sau khi ký tự được in.


.. method:: window.addnstr(str, n[, attr])
            window.addnstr(y, x, str, n[, attr])

   Vẽ nhiều nhất *n* ký tự của chuỗi ký tự *str* tại ``(y, x)`` với các thuộc tính *attr*, ghi đè mọi nội dung trước đó trên màn hình.


.. method:: window.addstr(str[, attr])
            window.addstr(y, x, str[, attr])

   Vẽ chuỗi ký tự *str* tại ``(y, x)`` với các thuộc tính *attr*, ghi đè mọi nội dung trước đó trên màn hình.

   .. note::

      * Ghi bên ngoài cửa sổ, cửa sổ con hoặc pad sẽ phát sinh :exc:`curses.error`. Việc cố gắng ghi vào góc dưới bên phải của cửa sổ, cửa sổ con hoặc pad sẽ khiến một ngoại lệ được phát sinh sau khi chuỗi được in.

      * Một lỗi trong ncurses, backend của module Python này, có thể gây ra lỗi phân đoạn khi thay đổi kích thước cửa sổ. Lỗi này đã được khắc phục trong ncurses-6.1-20190511. Nếu bạn buộc phải sử dụng phiên bản ncurses cũ hơn, có thể tránh kích hoạt lỗi này bằng cách không gọi :meth:`!addstr` với một *str* chứa ký tự xuống dòng; thay vào đó, hãy gọi :meth:`!addstr` riêng cho từng dòng.


.. method:: window.attroff(attr)

   Xóa thuộc tính *attr* khỏi tập "background" được áp dụng cho mọi thao tác ghi vào cửa sổ hiện tại.


.. method:: window.attron(attr)

   Thêm thuộc tính *attr* vào tập "background" được áp dụng cho mọi thao tác ghi vào cửa sổ hiện tại.


.. method:: window.attrset(attr)

   Đặt tập thuộc tính "background" thành *attr*. Tập này ban đầu là ``0`` (không có thuộc tính).


.. method:: window.bkgd(ch[, attr])

   Đặt thuộc tính background của cửa sổ thành ký tự *ch*, với các thuộc tính *attr*. Sau đó, thay đổi này được áp dụng cho mọi vị trí ký tự trong cửa sổ:

   * Thuộc tính của mọi ký tự trong cửa sổ được thay đổi thành thuộc tính background mới.

   * Ở mọi vị trí xuất hiện ký tự background trước đây, ký tự đó được thay đổi thành ký tự background mới.


.. method:: window.bkgdset(ch[, attr])

   Đặt background của cửa sổ. Background của một cửa sổ bao gồm một ký tự và bất kỳ tổ hợp thuộc tính nào. Phần thuộc tính của background được kết hợp (theo phép OR) với mọi ký tự không trống được ghi vào cửa sổ. Cả phần ký tự và phần thuộc tính của background đều được kết hợp với các ký tự trống. Background trở thành một thuộc tính của ký tự và di chuyển cùng ký tự qua mọi thao tác cuộn và chèn/xóa dòng/ký tự.


.. method:: window.border([ls[, rs[, ts[, bs[, tl[, tr[, bl[, br]]]]]]]])

   Vẽ đường viền quanh các cạnh của cửa sổ. Mỗi tham số chỉ định ký tự sẽ được sử dụng cho một phần cụ thể của đường viền; xem bảng dưới đây để biết thêm chi tiết.

   .. note::

      Một giá trị ``0`` cho bất kỳ tham số nào sẽ khiến ký tự mặc định được sử dụng cho tham số đó. Các tham số từ khóa *không* thể được sử dụng. Các giá trị mặc định được liệt kê trong bảng này:

   +---------+-------------------+-----------------------+
   | Tham số | Mô tả             | Giá trị mặc định      |
   +=========+===================+=======================+
   | *ls*    | Bên trái          | :const:`ACS_VLINE`    |
   +---------+-------------------+-----------------------+
   | *rs*    | Bên phải          | :const:`ACS_VLINE`    |
   +---------+-------------------+-----------------------+
   | *ts*    | Trên              | :const:`ACS_HLINE`    |
   +---------+-------------------+-----------------------+
   | *bs*    | Dưới              | :const:`ACS_HLINE`    |
   +---------+-------------------+-----------------------+
   | *tl*    | Góc trên bên trái | :const:`ACS_ULCORNER` |
   +---------+-------------------+-----------------------+
   | *tr*    | Góc trên bên phải | :const:`ACS_URCORNER` |
   +---------+-------------------+-----------------------+
   | *bl*    | Góc dưới bên trái | :const:`ACS_LLCORNER` |
   +---------+-------------------+-----------------------+
   | *br*    | Góc dưới bên phải | :const:`ACS_LRCORNER` |
   +---------+-------------------+-----------------------+


.. method:: window.box([vertch, horch])

   Tương tự :meth:`border`, nhưng cả *ls* và *rs* đều là *vertch*, đồng thời cả *ts* và *bs* đều là *horch*. Hàm này luôn sử dụng các ký tự góc mặc định.


.. method:: window.chgat(attr)
            window.chgat(num, attr) window.chgat(y, x, attr) window.chgat(y, x, num, attr)

   Đặt thuộc tính cho *num* ký tự tại vị trí con trỏ hiện tại hoặc tại vị trí ``(y, x)`` nếu được cung cấp. Nếu *num* không được cung cấp hoặc là ``-1``, thuộc tính sẽ được đặt cho tất cả ký tự từ vị trí đó đến cuối dòng. Hàm này di chuyển con trỏ đến vị trí ``(y, x)`` nếu được cung cấp. Dòng đã thay đổi sẽ được đánh dấu bằng phương thức :meth:`touchline`, để nội dung được hiển thị lại trong lần làm mới cửa sổ tiếp theo.


.. method:: window.clear()

   Giống :meth:`erase`, nhưng cũng khiến toàn bộ cửa sổ được vẽ lại trong lần gọi :meth:`refresh` tiếp theo.


.. method:: window.clearok(flag)

   Nếu *flag* là ``True``, lần gọi :meth:`refresh` tiếp theo sẽ xóa hoàn toàn cửa sổ.


.. method:: window.clrtobot()

   Xóa từ vị trí con trỏ đến cuối cửa sổ: tất cả các dòng bên dưới con trỏ sẽ bị xóa, sau đó thực hiện thao tác tương đương với :meth:`clrtoeol`.


.. method:: window.clrtoeol()

   Xóa từ vị trí con trỏ đến cuối dòng.


.. method:: window.cursyncup()

   Cập nhật vị trí con trỏ hiện tại của tất cả các cửa sổ cha của cửa sổ để phản ánh vị trí con trỏ hiện tại của cửa sổ.


.. method:: window.delch([y, x])

   Xóa ký tự nằm dưới con trỏ hoặc tại ``(y, x)`` nếu được chỉ định. Tất cả các ký tự bên phải trên cùng dòng được dịch sang trái một vị trí.


.. method:: window.deleteln()

   Xóa dòng nằm dưới con trỏ. Tất cả các dòng tiếp theo được dịch lên một dòng.


.. method:: window.derwin(begin_y, begin_x)
            window.derwin(nlines, ncols, begin_y, begin_x)

   Là cách viết tắt của "derive window", :meth:`derwin` tương đương với việc gọi
   :meth:`subwin`, ngoại trừ *begin_y* và *begin_x* là các giá trị tương đối so với gốc của cửa sổ, thay vì tương đối so với toàn bộ màn hình. Trả về một đối tượng cửa sổ cho cửa sổ được tạo.


.. method:: window.echochar(ch[, attr])

   Thêm ký tự *ch* với thuộc tính *attr*, rồi ngay lập tức gọi :meth:`refresh` trên cửa sổ.


.. method:: window.enclose(y, x)

   Kiểm tra xem cặp tọa độ ô ký tự tương đối với màn hình đã cho có nằm trong cửa sổ đã cho hay không, trả về ``True`` hoặc ``False``. Điều này hữu ích để xác định tập con nào của các cửa sổ màn hình bao quanh vị trí của một sự kiện chuột.

   .. versionchanged:: 3.10
      Trước đây, hàm trả về ``1`` hoặc ``0`` thay vì ``True`` hoặc ``False``.


.. attribute:: window.encoding

   Encoding được dùng để mã hóa các đối số chuỗi của các phương thức và giải mã kết quả của chúng trong bản build không hỗ trợ wide-character. Thuộc tính encoding được kế thừa từ cửa sổ cha khi một subwindow được tạo, chẳng hạn bằng :meth:`window.subwin`. Theo mặc định, encoding của locale hiện tại được sử dụng (xem :func:`locale.getencoding`).

   .. versionadded:: 3.3


.. method:: window.erase()

   Xóa cửa sổ.


.. method:: window.getbegyx()

   Trả về một tuple ``(y, x)`` chứa tọa độ của góc trên bên trái.


.. method:: window.getbkgd()

   Trả về cặp ký tự/thuộc tính nền hiện tại của cửa sổ đã cho. Có thể trích xuất các thành phần của nó như các thành phần của :meth:`inch`.


.. method:: window.getch([y, x])

   Đọc một phím được nhấn, sau khi di chuyển con trỏ đến *y*, *x* nếu được chỉ định, rồi trả về phím đó dưới dạng số nguyên. Cửa sổ được refresh trước nếu đó không phải là pad và đã được sửa đổi kể từ lần refresh trước. Chờ cho đến khi một phím được nhấn, hoặc trả về ``-1`` nếu thao tác đọc không blocking hoặc hết thời gian chờ (xem :meth:`nodelay` và :meth:`timeout`).

   Một phím thông thường được trả về dưới dạng mã của một byte trong encoding của locale hiện tại, vì vậy một ký tự được mã hóa bằng nhiều byte sẽ cần nhiều lần gọi. Ví dụ, trong locale UTF-8, ``'é'`` được đọc thành ``195``, rồi ``169``. Hãy sử dụng :meth:`get_wch` để đọc nó dưới dạng một ký tự duy nhất.

   Ở chế độ keypad (xem :meth:`keypad`), các phím chức năng và những phím đặc biệt khác được trả về dưới dạng một trong các hằng số :ref:`KEY_* constants <curses-key-constants>`, không thể nhầm với phím thông thường. Nếu không, hoặc nếu escape sequence của chúng không đến kịp thời (xem :meth:`notimeout` và :func:`set_escdelay`), các byte của chúng sẽ được trả về từng byte một.

   Ở chế độ echo (xem :func:`echo`), phím được thêm vào cửa sổ như khi gọi
   :meth:`addch`; các phím đặc biệt không được echo.


.. method:: window.get_wch([y, x])

   Đọc một lần nhấn phím sau khi di chuyển con trỏ đến *y*, *x* nếu được chỉ định, rồi trả về phím đó dưới dạng :class:`str` một ký tự. Trước tiên, cửa sổ sẽ được refresh nếu đó không phải là pad và đã bị sửa đổi kể từ lần refresh gần nhất. Chờ cho đến khi một phím được nhấn, hoặc phát sinh :exc:`error` nếu thao tác đọc không blocking hoặc hết thời gian chờ (xem :meth:`nodelay` và :meth:`timeout`).

   Ở chế độ keypad (xem :meth:`keypad`), các phím chức năng và những phím đặc biệt khác được trả về dưới dạng một trong các hằng số :ref:`KEY_* constants <curses-key-constants>`, là một số nguyên. Nếu không, hoặc nếu escape sequence của chúng không đến kịp thời (xem :meth:`notimeout` và :func:`set_escdelay`), các ký tự của chúng sẽ được trả về từng ký tự một.

   Ở chế độ echo (xem :func:`echo`), phím được thêm vào cửa sổ như khi gọi
   :meth:`addch`; các phím đặc biệt không được echo.

   .. versionadded:: 3.3


.. method:: window.getkey([y, x])

   Đọc một lần nhấn phím như :meth:`getch`, nhưng trả về dưới dạng :class:`str`: một phím thông thường dưới dạng chuỗi một ký tự, byte được giải mã theo Latin-1, và một phím đặc biệt dưới dạng tên của phím đó, chẳng hạn như ``'KEY_UP'`` (xem :func:`keyname`). Phát sinh :exc:`error` thay vì trả về ``-1`` nếu không có dữ liệu đầu vào.


.. method:: window.getmaxyx()

   Trả về một tuple ``(y, x)`` gồm chiều cao và chiều rộng của cửa sổ.


.. method:: window.getparyx()

   Trả về tọa độ bắt đầu của cửa sổ này tương đối so với cửa sổ cha dưới dạng một tuple ``(y, x)``. Trả về ``(-1, -1)`` nếu cửa sổ này không có cửa sổ cha.


.. method:: window.getstr()
            window.getstr(n) window.getstr(y, x) window.getstr(y, x, n)

   Đọc một dòng dữ liệu đầu vào từ người dùng, với khả năng chỉnh sửa dòng cơ bản, sau khi di chuyển con trỏ đến *y*, *x* nếu được chỉ định. Trả về dòng đó dưới dạng đối tượng bytes, theo encoding của locale hiện tại và không bao gồm ký tự xuống dòng kết thúc. Đọc tối đa *n* byte; *n* mặc định là 2047 và không thể vượt quá giá trị này.

   .. versionchanged:: 3.14
      Giá trị tối đa của *n* đã được tăng từ 1023 lên 2047.


.. method:: window.getyx()

   Trả về một tuple ``(y, x)`` biểu thị vị trí con trỏ hiện tại tương đối so với góc trên bên trái của cửa sổ.


.. method:: window.hline(ch, n[, attr])
            window.hline(y, x, ch, n[, attr])

   Hiển thị một đường ngang bắt đầu tại ``(y, x)`` với độ dài *n*, gồm ký tự *ch* với các thuộc tính *attr*. Đường này dừng ở cạnh phải của cửa sổ nếu còn ít hơn *n* ô khả dụng.


.. method:: window.idcok(flag)

   Nếu *flag* là ``False``, curses không còn xem xét việc sử dụng tính năng chèn/xóa ký tự bằng phần cứng của terminal; nếu *flag* là ``True``, việc chèn và xóa ký tự sẽ được bật. Khi curses được khởi tạo lần đầu, việc chèn/xóa ký tự được bật theo mặc định.


.. method:: window.idlok(flag)

   Nếu *flag* là ``True``, :mod:`!curses` sẽ cố gắng sử dụng các khả năng chỉnh sửa dòng bằng phần cứng. Nếu không, curses sẽ không sử dụng chúng.


.. method:: window.immedok(flag)

   Nếu *flag* là ``True``, mọi thay đổi trong ảnh cửa sổ sẽ tự động khiến cửa sổ được làm mới; bạn không còn phải tự gọi :meth:`refresh`. Tuy nhiên, điều này có thể làm giảm đáng kể hiệu suất do các lần gọi wrefresh lặp lại. Tùy chọn này bị tắt theo mặc định.


.. method:: window.inch([y, x])

   Trả về ký tự tại vị trí đã cho trong cửa sổ. 8 bit thấp nhất là ký tự thực tế, còn các bit cao hơn là thuộc tính; hãy trích xuất chúng bằng các mặt nạ bit :data:`A_CHARTEXT` và :data:`A_ATTRIBUTES`, còn cặp màu bằng :func:`pair_number`. Byte ký tự là byte được mã hóa theo locale của ký tự trong ô, nhất quán với :meth:`instr`. Trên bản dựng wide-character, một ký tự không vừa trong một byte theo locale hiện tại sẽ có byte ký tự là ``0``; hãy dùng :meth:`instr` để đọc các ký tự đó.


.. method:: window.insch(ch[, attr])
            window.insch(y, x, ch[, attr])

   Chèn ký tự *ch* với thuộc tính *attr* trước ký tự bên dưới con trỏ, hoặc tại ``(y, x)`` nếu được chỉ định. Tất cả ký tự bên phải con trỏ được dịch sang phải một vị trí, khiến ký tự ngoài cùng bên phải trên dòng bị mất. Vị trí con trỏ không thay đổi.


.. method:: window.insdelln(nlines)

   Chèn *nlines* dòng vào cửa sổ được chỉ định, phía trên dòng hiện tại. *nlines* dòng dưới cùng sẽ bị mất. Với *nlines* âm, xóa *nlines* dòng bắt đầu từ dòng bên dưới con trỏ, rồi dịch các dòng còn lại lên trên. *nlines* dòng dưới cùng được xóa. Vị trí con trỏ hiện tại vẫn giữ nguyên.


.. method:: window.insertln()

   Chèn một dòng trống bên dưới con trỏ. Tất cả các dòng tiếp theo được dịch xuống một dòng.


.. method:: window.insnstr(str, n[, attr])
            window.insnstr(y, x, str, n[, attr])

   Chèn một chuỗi ký tự (nhiều ký tự nhất có thể vừa trên dòng) trước ký tự bên dưới con trỏ, tối đa *n* ký tự. Nếu *n* bằng không hoặc âm, toàn bộ chuỗi sẽ được chèn. Tất cả ký tự bên phải con trỏ được dịch sang phải, khiến các ký tự ngoài cùng bên phải trên dòng bị mất. Vị trí con trỏ không thay đổi (sau khi di chuyển đến *y*, *x*, nếu được chỉ định).


.. method:: window.insstr(str[, attr])
            window.insstr(y, x, str[, attr])

   Chèn một chuỗi ký tự (nhiều ký tự nhất có thể vừa trên dòng) trước ký tự dưới con trỏ. Tất cả ký tự bên phải con trỏ được dịch sang phải, trong đó các ký tự ngoài cùng bên phải trên dòng sẽ bị mất. Vị trí con trỏ không thay đổi (sau khi di chuyển đến *y*, *x*, nếu được chỉ định).


.. method:: window.instr([n])
            window.instr(y, x[, n])

   Đọc văn bản của cửa sổ từ vị trí con trỏ hiện tại, hoặc từ *y*, *x* nếu được chỉ định, đến cuối dòng, rồi trả về văn bản dưới dạng đối tượng bytes, với encoding của locale hiện tại. Các thuộc tính và cặp màu sẽ bị loại bỏ. Đọc nhiều nhất *n* byte; *n* mặc định là và không thể vượt quá 2047.

   .. versionchanged:: 3.14
      Giá trị tối đa của *n* đã được tăng từ 1023 lên 2047.


.. method:: window.is_linetouched(line)

   Trả về ``True`` nếu dòng được chỉ định đã được sửa đổi kể từ lần gọi gần nhất đến
   :meth:`refresh`; nếu không thì trả về ``False``. Phát sinh ngoại lệ :exc:`curses.error` nếu *line* không hợp lệ đối với cửa sổ đã cho.


.. method:: window.is_wintouched()

   Trả về ``True`` nếu cửa sổ được chỉ định đã được sửa đổi kể từ lần gọi gần nhất đến
   :meth:`refresh`; nếu không thì trả về ``False``.


.. method:: window.keypad(flag)

   Nếu *flag* là ``True``, các escape sequence do một số phím tạo ra (bàn phím số, phím chức năng) sẽ được :mod:`!curses` diễn giải. Nếu *flag* là ``False``, các escape sequence sẽ được giữ nguyên trong input stream. Chế độ bàn phím số bị tắt theo mặc định, nhưng :func:`wrapper` bật chế độ này cho cửa sổ chính.


.. method:: window.leaveok(flag)

   Nếu *flag* là ``True``, con trỏ sẽ được giữ nguyên tại vị trí hiện tại khi cập nhật, thay vì ở "cursor position". Điều này giảm việc di chuyển con trỏ khi có thể.

   Nếu *flag* là ``False``, con trỏ sẽ luôn ở "cursor position" sau khi cập nhật.


.. method:: window.move(new_y, new_x)

   Di chuyển con trỏ đến ``(new_y, new_x)``.


.. method:: window.mvderwin(y, x)

   Di chuyển cửa sổ bên trong cửa sổ cha. Các tham số tương đối với màn hình của cửa sổ không thay đổi. Routine này được dùng để hiển thị các phần khác nhau của cửa sổ cha tại cùng một vị trí vật lý trên màn hình.


.. method:: window.mvwin(new_y, new_x)

   Di chuyển cửa sổ sao cho góc trên bên trái của nó ở tại ``(new_y, new_x)``.

   Di chuyển cửa sổ sao cho bất kỳ phần nào của nó nằm ngoài màn hình sẽ gây ra lỗi: cửa sổ không được di chuyển và :exc:`curses.error` được ném ra.


.. method:: window.nodelay(flag)

   Nếu *flag* là ``True``, :meth:`getch` sẽ ở chế độ non-blocking.


.. method:: window.notimeout(flag)

   Nếu *flag* là ``True``, các escape sequence sẽ không bị timeout.

   Nếu *flag* là ``False``, sau vài mili giây, một escape sequence sẽ không được diễn giải mà sẽ được giữ nguyên trong input stream.


.. method:: window.noutrefresh()
            window.noutrefresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)

   Đánh dấu để refresh nhưng chờ. Hàm này cập nhật cấu trúc dữ liệu biểu diễn trạng thái mong muốn của cửa sổ, nhưng không buộc cập nhật màn hình vật lý. Để thực hiện việc đó, hãy gọi  :func:`doupdate`.

   6 đối số chỉ có thể được chỉ định, và khi đó là bắt buộc, khi cửa sổ là một pad được tạo bằng :func:`newpad`; chúng có cùng ý nghĩa như đối với
   :meth:`refresh`.


.. method:: window.overlay(destwin[, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol])

   Chồng cửa sổ lên trên *destwin*. Các cửa sổ không cần có cùng kích thước; chỉ vùng chồng lấn được sao chép. Việc sao chép này không phá hủy dữ liệu, nghĩa là ký tự nền hiện tại không ghi đè nội dung cũ của *destwin*.

   Để kiểm soát chi tiết vùng được sao chép, có thể sử dụng dạng thứ hai của
   :meth:`overlay`. *sminrow* và *smincol* là tọa độ góc trên bên trái của cửa sổ nguồn, còn các biến khác xác định một hình chữ nhật trong cửa sổ đích.


.. method:: window.overwrite(destwin[, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol])

   Ghi đè cửa sổ lên trên *destwin*. Các cửa sổ không cần có cùng kích thước; nếu không, chỉ vùng chồng lấn được sao chép. Việc sao chép này có tính phá hủy, nghĩa là ký tự nền hiện tại ghi đè nội dung cũ của *destwin*.

   Để kiểm soát chi tiết vùng được sao chép, có thể sử dụng dạng thứ hai của
   :meth:`overwrite`. *sminrow* và *smincol* là tọa độ góc trên bên trái của cửa sổ nguồn, còn các biến khác xác định một hình chữ nhật trong cửa sổ đích.


.. method:: window.putwin(file)

   Ghi tất cả dữ liệu liên kết với cửa sổ vào đối tượng tệp được cung cấp. Sau đó có thể truy xuất thông tin này bằng hàm :func:`getwin`.


.. method:: window.redrawln(beg, num)

   Cho biết rằng các dòng màn hình *num*, bắt đầu từ dòng *beg*, đã bị hỏng và phải được vẽ lại hoàn toàn trong lần gọi :meth:`refresh` tiếp theo.


.. method:: window.redrawwin()

   Đánh dấu toàn bộ cửa sổ, khiến cửa sổ được vẽ lại hoàn toàn trong lần gọi tiếp theo
   :meth:`refresh`.


.. method:: window.refresh([pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol])

   Cập nhật màn hình ngay lập tức (đồng bộ màn hình thực với các phương thức vẽ/xóa trước đó).

   Chỉ có thể chỉ định 6 đối số này, và khi đó chúng là bắt buộc, nếu cửa sổ là một pad được tạo bằng :func:`newpad`. Các tham số bổ sung là cần thiết để chỉ ra phần nào của pad và màn hình được sử dụng. *pminrow* và *pmincol* xác định góc trên bên trái của hình chữ nhật sẽ được hiển thị trong pad. *sminrow*, *smincol*, *smaxrow*, và *smaxcol* xác định các cạnh của hình chữ nhật sẽ được hiển thị trên màn hình. Góc dưới bên phải của hình chữ nhật sẽ được hiển thị trong pad được tính từ các tọa độ màn hình, vì hai hình chữ nhật phải có cùng kích thước. Cả hai hình chữ nhật phải nằm hoàn toàn בתוך cấu trúc tương ứng của chúng. Các giá trị âm của *pminrow*, *pmincol*, *sminrow*, hoặc *smincol* được xử lý như thể chúng bằng không.


.. method:: window.resize(nlines, ncols)

   Cấp phát lại vùng lưu trữ cho một cửa sổ để điều chỉnh kích thước của cửa sổ theo các giá trị được chỉ định. Nếu một trong hai chiều lớn hơn giá trị hiện tại, dữ liệu của cửa sổ sẽ được điền bằng các khoảng trắng có cách hiển thị nền hiện tại (được thiết lập bằng :meth:`bkgdset`) đã được hợp nhất vào chúng.


.. method:: window.scroll([lines=1])

   Cuộn màn hình hoặc vùng cuộn. Cuộn lên *lines* dòng nếu *lines* dương, hoặc cuộn xuống nếu giá trị này âm. Việc cuộn không có tác dụng trừ khi đã được bật cho cửa sổ bằng :meth:`scrollok`.


.. method:: window.scrollok(flag)

   Kiểm soát điều xảy ra khi con trỏ của một cửa sổ được di chuyển ra ngoài cạnh của cửa sổ hoặc vùng cuộn, do thao tác xuống dòng trên dòng cuối hoặc do nhập ký tự cuối cùng của dòng cuối. Nếu *flag* là ``False``, con trỏ sẽ được giữ lại trên dòng cuối. Nếu *flag* là ``True``, cửa sổ sẽ được cuộn lên một dòng. Lưu ý rằng để có hiệu ứng cuộn vật lý trên terminal, cũng cần gọi :meth:`idlok`.


.. method:: window.setscrreg(top, bottom)

   Đặt vùng cuộn từ dòng *top* đến dòng *bottom*. Mọi thao tác cuộn sẽ diễn ra trong vùng này.


.. method:: window.standend()

   Tắt thuộc tính standout. Trên một số terminal, thao tác này cũng tắt tất cả các thuộc tính.


.. method:: window.standout()

   Bật thuộc tính *A_STANDOUT*.


.. method:: window.subpad(begin_y, begin_x)
            window.subpad(nlines, ncols, begin_y, begin_x)

   Trả về một sub-pad có góc trên bên trái tại ``(begin_y, begin_x)``, với chiều rộng/chiều cao lần lượt là *ncols*/*nlines*. Tọa độ được tính tương đối so với pad cha, không giống :meth:`subwin`, vốn sử dụng tọa độ màn hình. Phương thức này chỉ khả dụng với các pad được tạo bằng :func:`newpad`.


.. method:: window.subwin(begin_y, begin_x)
            window.subwin(nlines, ncols, begin_y, begin_x)

   Trả về một cửa sổ con, có góc trên bên trái nằm tại các tọa độ tương đối so với màn hình ``(begin_y, begin_x)``, và có chiều rộng/chiều cao là *ncols*/*nlines*.

   Theo mặc định, cửa sổ con sẽ kéo dài từ vị trí được chỉ định đến góc dưới bên phải của cửa sổ.


.. method:: window.syncdown()

   Đánh dấu tất cả các vị trí trong cửa sổ đã được đánh dấu trong bất kỳ cửa sổ tổ tiên nào của nó. Quy trình này được :meth:`refresh` gọi, vì vậy hầu như không bao giờ cần gọi thủ công.


.. method:: window.syncok(flag)

   Nếu *flag* là ``True``, thì :meth:`syncup` sẽ được tự động gọi mỗi khi cửa sổ có thay đổi.


.. method:: window.syncup()

   Đánh dấu tất cả các vị trí trong các cửa sổ tổ tiên của cửa sổ đã bị thay đổi trong cửa sổ.


.. method:: window.timeout(delay)

   Thiết lập hành vi đọc blocking hoặc non-blocking cho cửa sổ. Nếu *delay* là số âm, thao tác đọc blocking được sử dụng (sẽ chờ vô thời hạn để nhận đầu vào). Nếu *delay* bằng không, thao tác đọc non-blocking được sử dụng, và :meth:`getch` sẽ trả về ``-1`` nếu không có đầu vào nào đang chờ. Nếu *delay* là số dương, thì
   :meth:`getch` sẽ chặn trong *delay* mili giây và trả về ``-1`` nếu vẫn không có đầu vào nào vào cuối khoảng thời gian đó.


.. method:: window.touchline(start, count[, changed])

   Giả sử đã thay đổi *count* dòng, bắt đầu từ dòng *start*. Nếu cung cấp *changed*, tham số này xác định liệu các dòng bị ảnh hưởng được đánh dấu là đã thay đổi (*changed*\ ``=True``) hay chưa thay đổi (*changed*\ ``=False``).


.. method:: window.touchwin()

   Giả sử toàn bộ cửa sổ đã được thay đổi nhằm phục vụ việc tối ưu hóa hiển thị.


.. method:: window.untouchwin()

   Đánh dấu tất cả các dòng trong cửa sổ là chưa thay đổi kể từ lần gọi gần nhất đến
   :meth:`refresh`.


.. method:: window.vline(ch, n[, attr])
            window.vline(y, x, ch, n[, attr])

   Hiển thị một dòng dọc bắt đầu từ ``(y, x)`` và có độ dài *n*, gồm ký tự *ch* với các thuộc tính *attr*.


Hằng số
-------

Module :mod:`!curses` định nghĩa các thành viên dữ liệu sau:


.. data:: ERR

   Một số routine curses trả về một số nguyên, chẳng hạn như :meth:`~window.getch`, sẽ trả về
   :const:`ERR` khi thất bại.


.. data:: OK

   Một số routine curses trả về một số nguyên, chẳng hạn như :func:`napms`, sẽ trả về
   :const:`OK` khi thành công.


.. data:: version

   Một đối tượng bytes biểu thị phiên bản hiện tại của module.


.. data:: ncurses_version

   Một named tuple chứa ba thành phần của phiên bản thư viện ncurses: *major*, *minor* và *patch*. Tất cả các giá trị đều là số nguyên. Các thành phần cũng có thể được truy cập theo tên, vì vậy ``curses.ncurses_version[0]`` tương đương với ``curses.ncurses_version.major`` và tương tự.

   Khả dụng: nếu sử dụng thư viện ncurses.

   .. versionadded:: 3.8

.. data:: COLORS

   Số lượng màu tối đa mà terminal có thể hỗ trợ. Chỉ được xác định sau khi gọi :func:`start_color`.

.. data:: COLOR_PAIRS

   Số lượng cặp màu tối đa mà terminal có thể hỗ trợ. Chỉ được xác định sau khi gọi :func:`start_color`.

.. data:: COLS

   Chiều rộng của màn hình, tức là số cột. Chỉ được xác định sau khi gọi :func:`initscr`. Được cập nhật bởi :func:`update_lines_cols`, :func:`resizeterm` và
   :func:`resize_term`.

.. data:: LINES

   Chiều cao của màn hình, tức là số dòng. Chỉ được xác định sau khi gọi :func:`initscr`. Được cập nhật bởi :func:`update_lines_cols`, :func:`resizeterm` và
   :func:`resize_term`.


Một số hằng số có sẵn để chỉ định các thuộc tính của ô ký tự. Các hằng số cụ thể có sẵn phụ thuộc vào hệ thống.

+------------------------+------------------------------+
| Thuộc tính             | Ý nghĩa                      |
+========================+==============================+
| .. data:: A_ALTCHARSET | Chế độ bộ ký tự thay thế     |
+------------------------+------------------------------+
| .. data:: A_BLINK      | Chế độ nhấp nháy             |
+------------------------+------------------------------+
| .. data:: A_BOLD       | Chế độ in đậm                |
+------------------------+------------------------------+
| .. data:: A_DIM        | Chế độ mờ                    |
+------------------------+------------------------------+
| .. data:: A_INVIS      | Chế độ ẩn hoặc trống         |
+------------------------+------------------------------+
| .. data:: A_ITALIC     | Chế độ in nghiêng            |
+------------------------+------------------------------+
| .. data:: A_NORMAL     | Thuộc tính bình thường       |
+------------------------+------------------------------+
| .. data:: A_PROTECT    | Chế độ bảo vệ                |
+------------------------+------------------------------+
| .. data:: A_REVERSE    | Đảo ngược màu nền và màu chữ |
+------------------------+------------------------------+
| .. data:: A_STANDOUT   | Chế độ nổi bật               |
+------------------------+------------------------------+
| .. data:: A_UNDERLINE  | Chế độ gạch chân             |
+------------------------+------------------------------+
| .. data:: A_HORIZONTAL | Làm nổi bật theo chiều ngang |
+------------------------+------------------------------+
| .. data:: A_LEFT       | Làm nổi bật bên trái         |
+------------------------+------------------------------+
| .. data:: A_LOW        | Làm nổi bật ở mức thấp       |
+------------------------+------------------------------+
| .. data:: A_RIGHT      | Tô sáng bên phải             |
+------------------------+------------------------------+
| .. data:: A_TOP        | Tô sáng phía trên            |
+------------------------+------------------------------+
| .. data:: A_VERTICAL   | Tô sáng theo chiều dọc       |
+------------------------+------------------------------+

.. versionadded:: 3.7
   ``A_ITALIC`` đã được thêm.

Có sẵn một số hằng số để trích xuất các thuộc tính tương ứng được một số phương thức trả về.

+------------------------+---------------------------------------------------+
| Mặt nạ bit             | Ý nghĩa                                           |
+========================+===================================================+
| .. data:: A_ATTRIBUTES | Mặt nạ bit để trích xuất các thuộc tính           |
+------------------------+---------------------------------------------------+
| .. data:: A_CHARTEXT   | Mặt nạ bit để trích xuất một ký tự                |
+------------------------+---------------------------------------------------+
| .. data:: A_COLOR      | Mặt nạ bit để trích xuất thông tin trường cặp màu |
+------------------------+---------------------------------------------------+

.. _curses-key-constants:

Các phím được tham chiếu bằng các hằng số nguyên có tên bắt đầu bằng ``KEY_``. Các keycap chính xác hiện có phụ thuộc vào hệ thống.

.. XXX this table is far too large! should it be alphabetized?

+-------------------------+--------------------------------------------------+
| Hằng số phím            | Phím                                             |
+=========================+==================================================+
| .. data:: KEY_MIN       | Giá trị phím tối thiểu                           |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_BREAK     | Phím Break (không đáng tin cậy)                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_DOWN      | Mũi tên xuống                                    |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_UP        | Mũi tên lên                                      |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_LEFT      | Mũi tên trái                                     |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_RIGHT     | Mũi tên phải                                     |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_HOME      | Phím Home (mũi tên lên + trái)                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_BACKSPACE | Backspace (không đáng tin cậy)                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_F0        | Phím chức năng. Hỗ trợ tối đa 64 phím chức năng. |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_Fn        | Giá trị của phím chức năng *n*                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_DL        | Xóa dòng                                         |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_IL        | Chèn dòng                                        |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_DC        | Xóa ký tự                                        |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_IC        | Chèn ký tự hoặc vào chế độ chèn                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_EIC       | Thoát chế độ chèn ký tự                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_CLEAR     | Xóa màn hình                                     |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_EOS       | Xóa đến cuối màn hình                            |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_EOL       | Xóa đến cuối dòng                                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SF        | Cuộn tiến 1 dòng                                 |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SR        | Cuộn lùi 1 dòng (ngược)                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_NPAGE     | Trang tiếp theo                                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_PPAGE     | Trang trước                                      |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_STAB      | Đặt tab                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_CTAB      | Xóa tab                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_CATAB     | Xóa tất cả tab                                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_ENTER     | Enter hoặc gửi (không đáng tin cậy)              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SRESET    | Đặt lại mềm (một phần) (không đáng tin cậy)      |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_RESET     | Đặt lại hoặc đặt lại cứng (không đáng tin cậy)   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_PRINT     | In                                               |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_LL        | Home xuống hoặc dưới cùng (góc dưới bên trái)    |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_A1        | Góc trên bên trái của bàn phím số                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_A3        | Góc trên bên phải của bàn phím số                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_B2        | Trung tâm của bàn phím số                        |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_C1        | Góc dưới bên trái của bàn phím số                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_C3        | Góc dưới bên phải của bàn phím số                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_BTAB      | Tab lùi                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_BEG       | Beg (beginning)                                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_CANCEL    | Cancel                                           |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_CLOSE     | Close                                            |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_COMMAND   | Cmd (command)                                    |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_COPY      | Copy                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_CREATE    | Create                                           |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_END       | End                                              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_EXIT      | Exit                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_FIND      | Find                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_HELP      | Help                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_MARK      | Mark                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_MESSAGE   | Message                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_MOVE      | Move                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_NEXT      | Next                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_OPEN      | Open                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_OPTIONS   | Options                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_PREVIOUS  | Prev (previous)                                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_REDO      | Redo                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_REFERENCE | Ref (reference)                                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_REFRESH   | Refresh                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_REPLACE   | Replace                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_RESTART   | Restart                                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_RESUME    | Resume                                           |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SAVE      | Save                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SBEG      | Shifted Beg (beginning)                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SCANCEL   | Shifted Cancel                                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SCOMMAND  | Shifted Command                                  |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SCOPY     | Shifted Copy                                     |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SCREATE   | Tạo bằng Shift                                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SDC       | Xóa ký tự bằng Shift                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SDL       | Xóa dòng bằng Shift                              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SELECT    | Chọn                                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SEND      | End bằng Shift                                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SEOL      | Xóa dòng bằng Shift                              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SEXIT     | Thoát bằng Shift                                 |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SFIND     | Tìm kiếm có Shift                                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SHELP     | Trợ giúp có Shift                                |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SHOME     | Home có Shift                                    |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SIC       | Input có Shift                                   |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SLEFT     | Mũi tên trái có Shift                            |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SMESSAGE  | Message có Shift                                 |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SMOVE     | Move có Shift                                    |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SNEXT     | Next khi nhấn Shift                              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SOPTIONS  | Options khi nhấn Shift                           |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SPREVIOUS | Prev khi nhấn Shift                              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SPRINT    | Print khi nhấn Shift                             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SREDO     | Redo khi nhấn Shift                              |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SREPLACE  | Replace khi nhấn Shift                           |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SRIGHT    | Mũi tên phải khi nhấn Shift                      |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SRSUME    | Tiếp tục với phím Shift                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SSAVE     | Lưu với phím Shift                               |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SSUSPEND  | Tạm dừng với phím Shift                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SUNDO     | Hoàn tác với phím Shift                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_SUSPEND   | Tạm dừng                                         |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_UNDO      | Hoàn tác                                         |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_MOUSE     | Đã xảy ra sự kiện chuột                          |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_RESIZE    | Sự kiện thay đổi kích thước terminal             |
+-------------------------+--------------------------------------------------+
| .. data:: KEY_MAX       | Giá trị phím tối đa                              |
+-------------------------+--------------------------------------------------+

Trên VT100 và các trình mô phỏng phần mềm của chúng, chẳng hạn như các trình mô phỏng terminal X, thường có ít nhất bốn phím chức năng (:const:`KEY_F1 <KEY_Fn>`, :const:`KEY_F2 <KEY_Fn>`,
:const:`KEY_F3 <KEY_Fn>`, :const:`KEY_F4 <KEY_Fn>`) khả dụng, và các phím mũi tên được ánh xạ tới
:const:`KEY_UP`, :const:`KEY_DOWN`, :const:`KEY_LEFT` và :const:`KEY_RIGHT` theo cách hiển nhiên. Nếu máy của bạn có bàn phím PC, bạn có thể yên tâm mong đợi các phím mũi tên và mười hai phím chức năng (các bàn phím PC cũ có thể chỉ có mười phím chức năng); ngoài ra, các ánh xạ bàn phím số sau đây là tiêu chuẩn:

+------------------+-----------+
| Phím             | Hằng số   |
+==================+===========+
| :kbd:`Insert`    | KEY_IC    |
+------------------+-----------+
| :kbd:`Delete`    | KEY_DC    |
+------------------+-----------+
| :kbd:`Home`      | KEY_HOME  |
+------------------+-----------+
| :kbd:`End`       | KEY_END   |
+------------------+-----------+
| :kbd:`Page Up`   | KEY_PPAGE |
+------------------+-----------+
| :kbd:`Page Down` | KEY_NPAGE |
+------------------+-----------+

.. _curses-acs-codes:

Bảng sau liệt kê các ký tự từ bộ ký tự thay thế. Các ký tự này được kế thừa từ thiết bị đầu cuối VT100 và thường có sẵn trong các trình mô phỏng phần mềm như thiết bị đầu cuối X. Khi không có ký tự đồ họa tương ứng, curses sẽ chuyển sang dùng một dạng biểu diễn ASCII có thể in được nhưng khá thô sơ.

.. note::

   Các hằng số này chỉ khả dụng sau khi :func:`initscr` đã được gọi.

+------------------------+----------------------------------------------+
| ACS code               | Ý nghĩa                                      |
+========================+==============================================+
| .. data:: ACS_BBSS     | tên thay thế cho góc trên bên phải           |
+------------------------+----------------------------------------------+
| .. data:: ACS_BLOCK    | khối hình vuông đặc                          |
+------------------------+----------------------------------------------+
| .. data:: ACS_BOARD    | bảng gồm các ô vuông                         |
+------------------------+----------------------------------------------+
| .. data:: ACS_BSBS     | tên thay thế cho đường ngang                 |
+------------------------+----------------------------------------------+
| .. data:: ACS_BSSB     | tên thay thế cho góc trên bên trái           |
+------------------------+----------------------------------------------+
| .. data:: ACS_BSSS     | tên thay thế cho nhánh chữ T phía trên       |
+------------------------+----------------------------------------------+
| .. data:: ACS_BTEE     | nhánh chữ T phía dưới                        |
+------------------------+----------------------------------------------+
| .. data:: ACS_BULLET   | dấu đầu dòng                                 |
+------------------------+----------------------------------------------+
| .. data:: ACS_CKBOARD  | bàn cờ (chấm li ti)                          |
+------------------------+----------------------------------------------+
| .. data:: ACS_DARROW   | mũi tên chỉ xuống                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_DEGREE   | ký hiệu độ                                   |
+------------------------+----------------------------------------------+
| .. data:: ACS_DIAMOND  | hình thoi                                    |
+------------------------+----------------------------------------------+
| .. data:: ACS_GEQUAL   | lớn hơn hoặc bằng                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_HLINE    | đường ngang                                  |
+------------------------+----------------------------------------------+
| .. data:: ACS_LANTERN  | biểu tượng đèn lồng                          |
+------------------------+----------------------------------------------+
| .. data:: ACS_LARROW   | mũi tên trái                                 |
+------------------------+----------------------------------------------+
| .. data:: ACS_LEQUAL   | nhỏ hơn hoặc bằng                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_LLCORNER | góc dưới bên trái                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_LRCORNER | góc dưới bên phải                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_LTEE     | chữ T bên trái                               |
+------------------------+----------------------------------------------+
| .. data:: ACS_NEQUAL   | dấu không bằng                               |
+------------------------+----------------------------------------------+
| .. data:: ACS_PI       | chữ cái pi                                   |
+------------------------+----------------------------------------------+
| .. data:: ACS_PLMINUS  | dấu cộng-trừ                                 |
+------------------------+----------------------------------------------+
| .. data:: ACS_PLUS     | dấu cộng lớn                                 |
+------------------------+----------------------------------------------+
| .. data:: ACS_RARROW   | mũi tên sang phải                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_RTEE     | đầu nối bên phải                             |
+------------------------+----------------------------------------------+
| .. data:: ACS_S1       | dòng quét 1                                  |
+------------------------+----------------------------------------------+
| .. data:: ACS_S3       | dòng quét 3                                  |
+------------------------+----------------------------------------------+
| .. data:: ACS_S7       | dòng quét 7                                  |
+------------------------+----------------------------------------------+
| .. data:: ACS_S9       | dòng quét 9                                  |
+------------------------+----------------------------------------------+
| .. data:: ACS_SBBS     | tên thay thế cho góc dưới bên phải           |
+------------------------+----------------------------------------------+
| .. data:: ACS_SBSB     | tên thay thế cho đường dọc                   |
+------------------------+----------------------------------------------+
| .. data:: ACS_SBSS     | tên gọi khác của chữ T bên phải              |
+------------------------+----------------------------------------------+
| .. data:: ACS_SSBB     | tên gọi khác của góc dưới bên trái           |
+------------------------+----------------------------------------------+
| .. data:: ACS_SSBS     | tên gọi khác của chữ T phía dưới             |
+------------------------+----------------------------------------------+
| .. data:: ACS_SSSB     | tên gọi khác của chữ T bên trái              |
+------------------------+----------------------------------------------+
| .. data:: ACS_SSSS     | tên gọi khác của giao điểm hoặc dấu cộng lớn |
+------------------------+----------------------------------------------+
| .. data:: ACS_STERLING | bảng Anh                                     |
+------------------------+----------------------------------------------+
| .. data:: ACS_TTEE     | chữ T phía trên                              |
+------------------------+----------------------------------------------+
| .. data:: ACS_UARROW   | mũi tên lên                                  |
+------------------------+----------------------------------------------+
| .. data:: ACS_ULCORNER | góc trên bên trái                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_URCORNER | góc trên bên phải                            |
+------------------------+----------------------------------------------+
| .. data:: ACS_VLINE    | đường dọc                                    |
+------------------------+----------------------------------------------+

Bảng sau liệt kê các hằng số nút chuột được :meth:`getmouse` sử dụng:

+----------------------------------+---------------------------------------------------+
| Hằng số nút chuột                | Ý nghĩa                                           |
+==================================+===================================================+
| .. data:: BUTTONn_PRESSED        | Nút chuột *n* được nhấn                           |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTONn_RELEASED       | Nút chuột *n* được nhả                            |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTONn_CLICKED        | Nút chuột *n* được nhấp                           |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTONn_DOUBLE_CLICKED | Nút chuột *n* được nhấp đúp                       |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTONn_TRIPLE_CLICKED | Nút chuột *n* được nhấp ba lần                    |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTON_SHIFT           | Shift đang được giữ khi trạng thái nút thay đổi   |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTON_CTRL            | Control đang được giữ khi trạng thái nút thay đổi |
+----------------------------------+---------------------------------------------------+
| .. data:: BUTTON_ALT             | Alt được nhấn khi trạng thái nút thay đổi         |
+----------------------------------+---------------------------------------------------+

.. versionchanged:: 3.10
   Các hằng số ``BUTTON5_*`` hiện được hiển thị nếu chúng được thư viện curses bên dưới cung cấp.

Bảng sau liệt kê các màu được định nghĩa sẵn:

+-------------------------+---------------------------------+
| Hằng số                 | Màu sắc                         |
+=========================+=================================+
| .. data:: COLOR_BLACK   | Đen                             |
+-------------------------+---------------------------------+
| .. data:: COLOR_BLUE    | Xanh lam                        |
+-------------------------+---------------------------------+
| .. data:: COLOR_CYAN    | Xanh lơ (xanh lam nhạt pha lục) |
+-------------------------+---------------------------------+
| .. data:: COLOR_GREEN   | Xanh lá                         |
+-------------------------+---------------------------------+
| .. data:: COLOR_MAGENTA | Đỏ tía (đỏ pha tím)             |
+-------------------------+---------------------------------+
| .. data:: COLOR_RED     | Đỏ                              |
+-------------------------+---------------------------------+
| .. data:: COLOR_WHITE   | Trắng                           |
+-------------------------+---------------------------------+
| .. data:: COLOR_YELLOW  | Vàng                            |
+-------------------------+---------------------------------+


:mod:`!curses.textpad` --- Widget nhập văn bản cho các chương trình curses
==========================================================================

.. module:: curses.textpad
   :synopsis: Chỉnh sửa đầu vào kiểu Emacs trong cửa sổ curses.
.. moduleauthor:: Eric Raymond <esr@thyrsus.com>
.. sectionauthor:: Eric Raymond <esr@thyrsus.com>


Mô-đun :mod:`!curses.textpad` cung cấp một lớp :class:`Textbox` xử lý việc chỉnh sửa văn bản cơ bản trong cửa sổ curses, hỗ trợ một tập hợp các liên kết phím tương tự như của Emacs (và do đó cũng tương tự như của Netscape Navigator, BBedit 6.x, FrameMaker và nhiều chương trình khác). Mô-đun này cũng cung cấp một hàm vẽ hình chữ nhật hữu ích để tạo khung cho các hộp văn bản hoặc phục vụ các mục đích khác.

Mô-đun :mod:`!curses.textpad` định nghĩa hàm sau:


.. function:: rectangle(win, uly, ulx, lry, lrx)

   Vẽ một hình chữ nhật. Đối số đầu tiên phải là một đối tượng cửa sổ; các đối số còn lại là tọa độ tương đối so với cửa sổ đó. Đối số thứ hai và thứ ba lần lượt là tọa độ y và x của góc trên bên trái của hình chữ nhật cần vẽ; đối số thứ tư và thứ năm lần lượt là tọa độ y và x của góc dưới bên phải. Hình chữ nhật sẽ được vẽ bằng các ký tự tạo hình VT100/IBM PC trên những terminal hỗ trợ điều này (bao gồm xterm và hầu hết các trình mô phỏng terminal bằng phần mềm khác). Nếu không, hình chữ nhật sẽ được vẽ bằng các dấu gạch ngang, thanh dọc và dấu cộng ASCII.


.. _curses-textpad-objects:

Các đối tượng Textbox
---------------------

Bạn có thể khởi tạo một đối tượng :class:`Textbox` như sau:


.. class:: Textbox(win, insert_mode=False)

   Trả về một đối tượng widget textbox. Đối số *win* phải là một curses
   Đối tượng :ref:`window <curses-window-objects>` mà textbox sẽ được chứa trong đó. Nếu *insert_mode* là true, textbox sẽ chèn các ký tự được nhập, đẩy phần văn bản hiện có sang phải, thay vì ghi đè lên đó. Con trỏ chỉnh sửa của textbox ban đầu nằm ở góc trên bên trái của window chứa nó, với tọa độ ``(0, 0)``. Cờ :attr:`stripspaces` của instance ban đầu được bật.

   Các đối tượng :class:`Textbox` có những phương thức sau:


   .. method:: edit(validate=None)

      Đây là entry point mà bạn thường sử dụng. Phương thức này nhận các phím bấm chỉnh sửa cho đến khi một trong các phím bấm kết thúc được nhập. Nếu cung cấp *validate*, giá trị này phải là một hàm. Hàm sẽ được gọi cho mỗi phím bấm được nhập, với phím bấm đó làm tham số; việc dispatch lệnh được thực hiện dựa trên kết quả. Nếu hàm trả về giá trị false, phím bấm sẽ bị bỏ qua. Phương thức này trả về nội dung của window dưới dạng chuỗi; việc các khoảng trắng trong window có được đưa vào hay không bị ảnh hưởng bởi
      thuộc tính :attr:`stripspaces`.


   .. method:: do_command(ch)

      Xử lý một phím bấm lệnh duy nhất. Trả về ``1`` để tiếp tục chỉnh sửa hoặc ``0`` nếu đã xử lý một phím bấm kết thúc. Sau đây là các phím bấm đặc biệt được hỗ trợ:

      +------------------+------------------------------------------------------------------------------------+
      | Phím bấm         | Thao tác                                                                           |
      +==================+====================================================================================+
      | :kbd:`Control-A` | Đi đến mép trái của cửa sổ.                                                        |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-B` | Di chuyển con trỏ sang trái, chuyển sang dòng trước nếu thích hợp.                 |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-D` | Xóa ký tự bên dưới con trỏ.                                                        |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-E` | Đi đến mép phải (khi stripspaces tắt) hoặc cuối dòng (khi stripspaces bật).        |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-F` | Di chuyển con trỏ sang phải, chuyển sang dòng tiếp theo khi thích hợp.             |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-G` | Kết thúc, trả về nội dung cửa sổ.                                                  |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-H` | Xóa ký tự về phía sau.                                                             |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-J` | Kết thúc nếu cửa sổ chỉ có 1 dòng, nếu không thì di chuyển đến đầu dòng tiếp theo. |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-K` | Nếu dòng trống, hãy xóa dòng đó; nếu không, hãy xóa đến cuối dòng.                 |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-L` | Làm mới màn hình.                                                                  |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-N` | Di chuyển con trỏ xuống; di chuyển xuống một dòng.                                 |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-O` | Chèn một dòng trống tại vị trí con trỏ.                                            |
      +------------------+------------------------------------------------------------------------------------+
      | :kbd:`Control-P` | Di chuyển con trỏ lên; di chuyển lên một dòng.                                     |
      +------------------+------------------------------------------------------------------------------------+

      Các thao tác di chuyển không làm gì nếu con trỏ ở cạnh mà tại đó không thể di chuyển. Các từ đồng nghĩa sau được hỗ trợ khi có thể:

      +--------------------------------+------------------+
      | Hằng số                        | Phím gõ          |
      +================================+==================+
      | :const:`~curses.KEY_LEFT`      | :kbd:`Control-B` |
      +--------------------------------+------------------+
      | :const:`~curses.KEY_RIGHT`     | :kbd:`Control-F` |
      +--------------------------------+------------------+
      | :const:`~curses.KEY_UP`        | :kbd:`Control-P` |
      +--------------------------------+------------------+
      | :const:`~curses.KEY_DOWN`      | :kbd:`Control-N` |
      +--------------------------------+------------------+
      | :const:`~curses.KEY_BACKSPACE` | :kbd:`Control-h` |
      +--------------------------------+------------------+

      Tất cả các phím gõ khác được xử lý như một lệnh để chèn ký tự đã cho và di chuyển sang phải (có ngắt dòng).


   .. method:: gather()

      Trả về nội dung của cửa sổ dưới dạng chuỗi; việc các khoảng trống trong cửa sổ có được bao gồm hay không phụ thuộc vào thành viên :attr:`stripspaces`.


   .. attribute:: stripspaces

      Thuộc tính này là một cờ điều khiển cách diễn giải các khoảng trống trong cửa sổ. Khi được bật, các khoảng trống ở cuối mỗi dòng sẽ bị bỏ qua; mọi thao tác di chuyển con trỏ khiến con trỏ dừng ở khoảng trống cuối dòng sẽ đưa con trỏ đến cuối dòng đó, đồng thời các khoảng trống ở cuối dòng sẽ bị loại bỏ khi thu thập nội dung cửa sổ.
