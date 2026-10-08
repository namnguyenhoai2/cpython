.. _idle:

IDLE --- trình soạn thảo và shell Python
========================================

.. moduleauthor:: Guido van Rossum <guido@python.org>

**Mã nguồn:** :source:`Lib/idlelib/`

.. index::
   single: IDLE
   single: Python Editor
   single: Integrated Development Environment

..
   Hãy nhớ cập nhật Lib/idlelib/help.html bằng idlelib.help.copy_strip() khi sửa đổi tệp này.

--------------

IDLE là Môi trường Phát triển và Học tập Tích hợp của Python.

IDLE có các tính năng sau:

* đa nền tảng: hoạt động gần như giống nhau trên Windows, Unix và macOS

* cửa sổ shell Python (trình thông dịch tương tác) với khả năng tô màu mã đầu vào, đầu ra và thông báo lỗi

* trình soạn thảo văn bản đa cửa sổ với tính năng hoàn tác nhiều cấp, tô màu cú pháp Python, thụt lề thông minh, gợi ý lời gọi, tự động hoàn thành và các tính năng khác

* tìm kiếm trong bất kỳ cửa sổ nào, thay thế trong các cửa sổ trình soạn thảo và tìm kiếm qua nhiều tệp (grep)

* trình debugger với các điểm dừng được duy trì, khả năng thực hiện từng bước và xem các namespace toàn cục và cục bộ

* các hộp thoại cấu hình, trình duyệt và những hộp thoại khác

Ứng dụng IDLE được triển khai trong gói :mod:`idlelib`.

.. include:: ../includes/optional-module.rst

Menu
----

IDLE có hai loại cửa sổ chính: cửa sổ Shell và cửa sổ Editor. Có thể mở đồng thời nhiều cửa sổ Editor. Trên Windows và Linux, mỗi cửa sổ có menu trên cùng riêng. Mỗi menu được mô tả bên dưới đều cho biết loại cửa sổ mà nó liên kết.

Các cửa sổ output, chẳng hạn như cửa sổ được dùng cho Edit => Find in Files, là một kiểu con của cửa sổ editor. Hiện tại, chúng có cùng menu trên cùng nhưng có tiêu đề mặc định và menu ngữ cảnh khác.

Trên macOS, có một menu ứng dụng duy nhất. Menu này tự động thay đổi tùy theo cửa sổ hiện được chọn. Menu có menu IDLE, và một số mục được mô tả bên dưới được sắp xếp lại để tuân theo hướng dẫn của Apple.

File menu (Shell and Editor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New File
   Tạo một cửa sổ chỉnh sửa tệp mới.

Open...
   Mở một tệp hiện có bằng hộp thoại Open.

Open Module...
   Mở một module hiện có (tìm kiếm trong sys.path).

Recent Files
   Mở danh sách các tệp gần đây. Nhấp vào một tệp để mở.

.. index::
   single: Module browser
   single: Path browser

Module Browser
   Hiển thị các function, class và method trong tệp Editor hiện tại dưới dạng cấu trúc cây. Trong shell, trước tiên hãy mở một module.

Path Browser
   Hiển thị các thư mục, module, hàm, lớp và phương thức trong sys.path dưới dạng cấu trúc cây.

Save
   Lưu cửa sổ hiện tại vào tệp liên kết, nếu có. Các cửa sổ đã được thay đổi kể từ khi mở hoặc kể từ lần lưu gần nhất sẽ có \* ở trước và sau tiêu đề cửa sổ. Nếu không có tệp liên kết, hãy sử dụng Save As.

Save As...
   Lưu cửa sổ hiện tại bằng hộp thoại Save As. Tệp được lưu sẽ trở thành tệp liên kết mới của cửa sổ. (Nếu trình quản lý tệp được đặt để ẩn phần mở rộng, phần mở rộng hiện tại sẽ bị lược bỏ trong ô tên tệp. Nếu tên tệp mới không có '.', '.py' và '.txt' sẽ được thêm vào tương ứng cho tệp Python và tệp văn bản, ngoại trừ trên macOS Aqua, '.py' sẽ được thêm vào mọi tệp.)

Save Copy As...
   Lưu cửa sổ hiện tại vào một tệp khác mà không thay đổi tệp liên kết. (Xem lưu ý về phần mở rộng tên tệp trong Save As ở trên.)

Print Window
   In cửa sổ hiện tại bằng máy in mặc định.

Close Window
   Đóng cửa sổ hiện tại (nếu là editor chưa lưu, yêu cầu lưu; nếu là Shell chưa lưu, yêu cầu thoát quá trình thực thi). Việc gọi ``exit()`` hoặc ``close()`` trong cửa sổ Shell cũng đóng Shell. Nếu đây là cửa sổ duy nhất, đồng thời thoát IDLE.

Exit IDLE
   Đóng tất cả cửa sổ và thoát IDLE (yêu cầu lưu các cửa sổ chỉnh sửa chưa lưu).

Edit menu (Shell and Editor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hoàn tác
   Hoàn tác thay đổi gần nhất đối với cửa sổ hiện tại. Có thể hoàn tác tối đa 1000 thay đổi.

Làm lại
   Làm lại thay đổi gần nhất đã được hoàn tác đối với cửa sổ hiện tại.

Chọn tất cả
   Chọn toàn bộ nội dung của cửa sổ hiện tại.

Cắt
   Sao chép vùng chọn vào clipboard dùng chung của hệ thống; sau đó xóa vùng chọn.

Copy
   Sao chép vùng chọn vào clipboard dùng chung của hệ thống.

Paste
   Chèn nội dung của clipboard dùng chung của hệ thống vào cửa sổ hiện tại.

Các chức năng clipboard cũng có trong các menu ngữ cảnh.

Find...
   Mở hộp thoại tìm kiếm với nhiều tùy chọn

Find Again
   Lặp lại lần tìm kiếm gần nhất, nếu có.

Find Selection
   Tìm kiếm chuỗi hiện đang được chọn, nếu có.

Find in Files...
   Mở hộp thoại tìm kiếm tệp. Đưa kết quả vào một cửa sổ đầu ra mới.

Replace...
   Mở hộp thoại tìm kiếm và thay thế.

Go to Line
   Di chuyển con trỏ đến đầu dòng được yêu cầu và làm cho dòng đó hiển thị. Yêu cầu vượt quá cuối tệp sẽ chuyển đến cuối tệp. Xóa mọi vùng chọn và cập nhật trạng thái dòng và cột.

Show Completions
   Mở danh sách có thể cuộn, cho phép chọn các tên hiện có. Xem
   :ref:`Completions <completions>` trong phần Editing and Navigation bên dưới.

Expand Word
   Mở rộng tiền tố bạn đã nhập để khớp với một từ đầy đủ trong cùng cửa sổ; lặp lại để nhận một cách mở rộng khác.

Show Call Tip
   Sau một dấu ngoặc đơn chưa đóng của một hàm, mở một cửa sổ nhỏ với các gợi ý về tham số của hàm. Xem :ref:`Calltips <calltips>` trong phần Editing and Navigation bên dưới.

Show Surrounding Parens
   Tô sáng dấu ngoặc đơn bao quanh.

.. _format-menu:

Format menu (Editor window only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Định dạng đoạn văn
   Định dạng lại khối văn bản chứa con trỏ chèn văn bản. Tránh các dòng mã. Xem :ref:`Định dạng khối <format-block>` trong phần Chỉnh sửa và Điều hướng bên dưới.

Thụt lề vùng
   Dịch các dòng đã chọn sang phải theo độ rộng thụt lề (mặc định là 4 dấu cách).

Bỏ thụt lề vùng
   Dịch các dòng đã chọn sang trái theo độ rộng thụt lề (mặc định là 4 dấu cách).

Bỏ ghi chú vùng
   Chèn ## vào trước các dòng đã chọn.

Uncomment Region
   Xóa # hoặc ## ở đầu các dòng đã chọn.

Tabify Region
   Chuyển các đoạn *ở đầu* gồm dấu cách thành tab. (Lưu ý: Chúng tôi khuyến nghị sử dụng các khối 4 dấu cách để thụt lề mã Python.)

Untabify Region
   Chuyển *tất cả* tab thành số lượng dấu cách thích hợp.

Toggle Tabs
   Mở một hộp thoại để chuyển đổi giữa việc thụt lề bằng dấu cách và tab.

New Indent Width
   Mở một hộp thoại để thay đổi độ rộng thụt lề. Giá trị mặc định được cộng đồng Python chấp nhận là 4 dấu cách.

Strip Trailing Whitespace
   Xóa dấu cách ở cuối dòng và các ký tự khoảng trắng khác sau ký tự cuối cùng không phải khoảng trắng của một dòng bằng cách áp dụng :meth:`str.rstrip` cho từng dòng, bao gồm cả các dòng trong chuỗi nhiều dòng. Ngoại trừ các cửa sổ Shell, hãy xóa các dòng mới thừa ở cuối tệp.

.. index::
   single: Run script

Run menu (Editor window only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _run-module:

Run Module
   Thực hiện :ref:`Check Module <check-module>`. Nếu không có lỗi, hãy khởi động lại Shell để làm sạch môi trường, sau đó thực thi module. Kết quả được hiển thị trong Shell window. Lưu ý rằng để hiển thị kết quả, cần sử dụng ``print`` hoặc ``write``. Khi quá trình thực thi hoàn tất, Shell vẫn được chọn và hiển thị dấu nhắc. Lúc này, bạn có thể tương tác để khám phá kết quả thực thi. Điều này tương tự như thực thi một tệp bằng ``python -i file`` trên dòng lệnh.

.. _run-custom:

Run... Customized
   Tương tự như :ref:`Run Module <run-module>`, nhưng thực thi module với các thiết lập tùy chỉnh. *Command Line Arguments* mở rộng :data:`sys.argv` như thể chúng được truyền trên dòng lệnh. Có thể thực thi module trong Shell mà không cần khởi động lại.

.. _check-module:

Check Module
   Kiểm tra cú pháp của module hiện đang mở trong Editor window. Nếu module chưa được lưu, IDLE sẽ nhắc người dùng lưu hoặc tự động lưu, tùy theo lựa chọn trong tab General của hộp thoại Idle Settings. Nếu có lỗi cú pháp, vị trí gần đúng sẽ được chỉ báo trong Editor window.

.. _python-shell:

Python Shell
   Mở hoặc đánh thức cửa sổ Python Shell.


Shell menu (Shell window only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

View Last Restart
  Cuộn cửa sổ shell đến lần khởi động lại Shell gần nhất.

Restart Shell
  Khởi động lại shell để làm sạch môi trường và đặt lại phần hiển thị cũng như việc xử lý ngoại lệ.

Previous History
  Duyệt qua các lệnh trước đó trong lịch sử khớp với mục nhập hiện tại.

Next History
  Duyệt qua các lệnh sau đó trong lịch sử khớp với mục nhập hiện tại.

Interrupt Execution
  Dừng chương trình đang chạy.

Debug menu (Shell window only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to File/Line
   Tìm trên dòng hiện tại có con trỏ và dòng phía trên để tìm tên tệp và số dòng. Nếu tìm thấy, hãy mở tệp nếu tệp chưa được mở và hiển thị dòng đó. Sử dụng tính năng này để xem các dòng mã nguồn được tham chiếu trong traceback của ngoại lệ và các dòng được Find in Files tìm thấy. Tính năng này cũng có trong menu ngữ cảnh của cửa sổ Shell và các cửa sổ Output.

.. index::
   single: debugger
   single: stack viewer

Debugger (toggle)
   Khi được kích hoạt, mã được nhập trong Shell hoặc chạy từ một Editor sẽ chạy dưới debugger. Trong Editor, có thể đặt breakpoint bằng menu ngữ cảnh. Tính năng này vẫn chưa hoàn thiện và còn mang tính thử nghiệm.

Stack Viewer
   Hiển thị traceback của stack cho ngoại lệ gần nhất trong một widget dạng cây, cùng quyền truy cập vào các biến cục bộ và biến toàn cục.

Auto-open Stack Viewer
   Bật hoặc tắt việc tự động mở stack viewer khi xảy ra ngoại lệ không được xử lý.

Trình đơn Options (Shell và Editor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cấu hình IDLE
   Mở hộp thoại cấu hình và thay đổi tùy chọn cho các mục sau: phông chữ, thụt lề, keybinding, giao diện màu văn bản, cửa sổ khởi động và kích thước, các nguồn trợ giúp bổ sung, cùng các phần mở rộng. Trên macOS, mở hộp thoại cấu hình bằng cách chọn Preferences trong trình đơn ứng dụng. Để biết thêm chi tiết, xem
   :ref:`Thiết lập tùy chọn <preferences>` trong Help and preferences.

Hầu hết các tùy chọn cấu hình đều áp dụng cho tất cả cửa sổ hoặc tất cả cửa sổ được mở sau đó. Các mục tùy chọn bên dưới chỉ áp dụng cho cửa sổ đang hoạt động.

Show/Hide Code Context (Editor Window only)
   Mở một ngăn ở đầu cửa sổ soạn thảo, hiển thị ngữ cảnh khối của phần mã đã cuộn lên phía trên đầu cửa sổ. Xem
   :ref:`Code Context <code-context>` trong phần Editing and Navigation bên dưới.

Show/Hide Line Numbers (Editor Window only)
   Mở một cột ở bên trái cửa sổ chỉnh sửa để hiển thị số của từng dòng văn bản.  Theo mặc định, tùy chọn này bị tắt và có thể thay đổi trong phần tùy chọn (xem :ref:`Setting preferences <preferences>`).

Zoom/Restore Height
   Chuyển đổi cửa sổ giữa kích thước bình thường và chiều cao tối đa. Kích thước ban đầu mặc định là 40 dòng x 80 ký tự, trừ khi được thay đổi trong tab General của hộp thoại Configure IDLE.  Chiều cao tối đa của màn hình được xác định bằng cách tạm thời phóng to một cửa sổ vào lần đầu tiên cửa sổ được zoom trên màn hình. Việc thay đổi cài đặt màn hình có thể làm mất hiệu lực chiều cao đã lưu.  Tùy chọn chuyển đổi này không có tác dụng khi cửa sổ đã được phóng to.

Window menu (Shell and Editor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Liệt kê tên của tất cả các cửa sổ đang mở; chọn một cửa sổ để đưa nó lên phía trước (bỏ trạng thái thu nhỏ nếu cần).

Help menu (Shell and Editor)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

About IDLE
   Hiển thị phiên bản, bản quyền, giấy phép, thông tin ghi công và nhiều nội dung khác.

IDLE Help
   Hiển thị tài liệu IDLE này, trình bày các tùy chọn menu, cách chỉnh sửa và điều hướng cơ bản cùng các mẹo khác.

Python Docs
   Truy cập tài liệu Python cục bộ nếu đã được cài đặt hoặc khởi động trình duyệt web và mở docs.python.org để hiển thị tài liệu Python mới nhất.

Bản trình diễn Turtle
   Chạy module turtledemo với mã Python mẫu và các hình vẽ bằng turtle.

Có thể thêm các nguồn trợ giúp khác tại đây bằng hộp thoại Configure IDLE trong thẻ General. Xem tiểu mục :ref:`Help sources <help-sources>` bên dưới để biết thêm về các lựa chọn trong menu Help.

.. index::
   single: Cut
   single: Copy
   single: Paste
   single: Set Breakpoint
   single: Clear Breakpoint
   single: breakpoints

Menu ngữ cảnh
^^^^^^^^^^^^^

Mở menu ngữ cảnh bằng cách nhấp chuột phải trong một cửa sổ (Control-click trên macOS). Menu ngữ cảnh cũng có các chức năng clipboard tiêu chuẩn như trong menu Edit.

Cắt
   Sao chép phần được chọn vào clipboard trên toàn hệ thống, sau đó xóa phần được chọn.

Copy
   Sao chép vùng chọn vào clipboard trên toàn hệ thống.

Paste
   Chèn nội dung của clipboard trên toàn hệ thống vào cửa sổ hiện tại.

Các cửa sổ trình soạn thảo cũng có các chức năng breakpoint. Các dòng đã đặt breakpoint sẽ được đánh dấu đặc biệt. Breakpoint chỉ có tác dụng khi chạy dưới trình gỡ lỗi. Breakpoint của một tệp được lưu trong thư mục ``.idlerc`` của người dùng.

Set Breakpoint
   Đặt breakpoint trên dòng hiện tại.

Clear Breakpoint
   Xóa breakpoint trên dòng đó.

Các cửa sổ Shell và Output cũng có các mục sau.

Go to file/line
   Giống như trong menu Debug.

Cửa sổ Shell cũng có chức năng thu gọn output được giải thích trong phần *Python Shell window* bên dưới.

Squeeze
   Nếu con trỏ nằm trên một dòng output, thu gọn toàn bộ output nằm giữa đoạn code ở trên và prompt ở dưới thành nhãn 'Squeezed text'.


.. _editing-and-navigation:

Chỉnh sửa và điều hướng
-----------------------

Cửa sổ editor
^^^^^^^^^^^^^

IDLE có thể mở các cửa sổ editor khi khởi động, tùy thuộc vào cài đặt và cách bạn khởi động IDLE. Sau đó, hãy sử dụng menu File. Chỉ có thể mở một cửa sổ editor cho một tệp nhất định.

Thanh tiêu đề chứa tên tệp, đường dẫn đầy đủ, cùng phiên bản Python và IDLE đang chạy cửa sổ đó. Thanh trạng thái chứa số dòng ('Ln') và số cột ('Col'). Số dòng bắt đầu từ 1; số cột bắt đầu từ 0.

IDLE giả định rằng các tệp có phần mở rộng .py* đã biết chứa mã Python, còn các tệp khác thì không. Chạy mã Python bằng menu Run.

Liên kết phím
^^^^^^^^^^^^^

Con trỏ chèn của IDLE là một thanh dọc mảnh nằm giữa các vị trí ký tự. Khi nhập ký tự, con trỏ chèn và mọi thứ ở bên phải nó dịch sang phải một ký tự, còn ký tự mới được nhập vào khoảng trống mới.

Một số phím không phải ký tự sẽ di chuyển con trỏ và có thể xóa ký tự. Việc xóa không đưa văn bản vào clipboard, nhưng IDLE có danh sách hoàn tác. Trong tài liệu này, khi nói về các phím, 'C' đề cập đến phím :kbd:`Control` trên Windows và Unix, và phím :kbd:`Command` trên macOS. (Mọi nội dung đề cập như vậy đều giả định rằng các phím chưa được liên kết lại với chức năng khác.)

* Các phím mũi tên di chuyển con trỏ một ký tự hoặc một dòng.

* :kbd:`C-LeftArrow` và :kbd:`C-RightArrow` di chuyển sang trái hoặc phải một từ.

* :kbd:`Home` và :kbd:`End` di chuyển đến đầu hoặc cuối dòng.

* :kbd:`Page Up` và :kbd:`Page Down` di chuyển lên hoặc xuống một màn hình.

* :kbd:`C-Home` và :kbd:`C-End` di chuyển đến đầu hoặc cuối tệp.

* :kbd:`Backspace` và :kbd:`Del` (hoặc :kbd:`C-d`) xóa ký tự trước hoặc sau.

* :kbd:`C-Backspace` và :kbd:`C-Del` xóa một từ ở bên trái hoặc bên phải.

* :kbd:`C-k` xóa ('kill') mọi thứ ở bên phải.

Các keybinding tiêu chuẩn (như :kbd:`C-c` để sao chép và :kbd:`C-v` để dán) có thể hoạt động. Keybinding được chọn trong hộp thoại Configure IDLE.

Tự động thụt lề
^^^^^^^^^^^^^^^

Sau một câu lệnh mở khối, dòng tiếp theo được thụt vào 4 dấu cách (trong cửa sổ Python Shell là một tab). Sau một số từ khóa nhất định (break, return, v.v.), dòng tiếp theo sẽ được bỏ thụt lề. Ở phần thụt lề đầu dòng, :kbd:`Backspace` xóa tối đa 4 dấu cách nếu có. :kbd:`Tab` chèn dấu cách (trong cửa sổ Python Shell là một tab), số lượng phụ thuộc vào Indent width. Hiện tại, tab bị giới hạn ở bốn dấu cách do các hạn chế của Tcl/Tk.

Xem thêm các lệnh vùng thụt lề/bỏ thụt lề trên
:ref:`Format menu <format-menu>`.

Tìm kiếm và thay thế
^^^^^^^^^^^^^^^^^^^^

Mọi vùng chọn đều trở thành mục tiêu tìm kiếm. Tuy nhiên, chỉ các vùng chọn trong một dòng mới hoạt động vì việc tìm kiếm chỉ được thực hiện trong các dòng đã loại bỏ ký tự xuống dòng ở cuối. Nếu ``[x] Regular expression`` được chọn, mục tiêu sẽ được diễn giải theo module re của Python.

.. _completions:

Tính năng tự động hoàn thành
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tính năng tự động hoàn thành sẽ cung cấp các gợi ý khi được yêu cầu và khả dụng, cho tên module, thuộc tính của class hoặc function, hoặc tên tệp. Mỗi phương thức yêu cầu sẽ hiển thị một hộp gợi ý kèm các tên hiện có. (Xem phần tự động hoàn thành bằng phím tab bên dưới để biết ngoại lệ.) Đối với mọi hộp, hãy thay đổi tên đang được tự động hoàn thành và mục được tô sáng trong hộp bằng cách nhập và xóa ký tự; bằng cách nhấn :kbd:`Up`, :kbd:`Down`,
:kbd:`PageUp`, :kbd:`PageDown`, :kbd:`Home`, và :kbd:`End`; và bằng cách nhấp một lần vào bên trong hộp. Đóng hộp bằng :kbd:`Escape`,
:kbd:`Enter`, và nhấn đúp phím :kbd:`Tab` hoặc nhấp đúp bên ngoài hộp. Nhấp đúp bên trong hộp sẽ chọn mục và đóng hộp.

Một cách để mở hộp là nhập một ký tự khóa rồi chờ trong khoảng thời gian được định trước. Mặc định là 2 giây; hãy tùy chỉnh trong hộp thoại cài đặt. (Để ngăn cửa sổ bật lên tự động, hãy đặt độ trễ thành một số mili giây lớn, chẳng hạn như 100000000.) Đối với tên module được import hoặc các thuộc tính của class hay function, hãy nhập '.'. Đối với tên tệp trong thư mục gốc, hãy nhập :data:`os.sep` hoặc
:data:`os.altsep` ngay sau dấu ngoặc kép mở. (Trên Windows, có thể chỉ định ổ đĩa trước.) Di chuyển vào các thư mục con bằng cách nhập tên thư mục và dấu phân cách.

Thay vì chờ, hoặc sau khi một hộp đã đóng, hãy mở ngay hộp hoàn thành bằng Show Completions trong menu Edit. Phím tắt mặc định là :kbd:`C-space`. Nếu nhập tiền tố của tên mong muốn trước khi mở hộp, kết quả khớp đầu tiên hoặc gần đúng sẽ được hiển thị. Kết quả giống như khi nhập tiền tố sau khi hộp được hiển thị. Show Completions sau một dấu ngoặc kép sẽ hoàn thành tên tệp trong thư mục hiện tại thay vì thư mục gốc.

Nhấn :kbd:`Tab` sau một tiền tố thường có tác dụng giống như Show Completions. (Khi không có tiền tố, thao tác này sẽ thụt lề.) Tuy nhiên, nếu tiền tố chỉ khớp với một kết quả, kết quả đó sẽ được thêm ngay vào văn bản của trình soạn thảo mà không mở hộp.

Gọi 'Show Completions' hoặc nhấn :kbd:`Tab` sau một tiền tố, bên ngoài chuỗi và không có dấu '.' đứng trước, sẽ mở một hộp chứa các từ khóa, tên dựng sẵn và các tên cấp module hiện có.

Khi chỉnh sửa code trong trình soạn thảo (trái với Shell), hãy tăng số tên cấp module hiện có bằng cách chạy code và sau đó không khởi động lại Shell. Điều này đặc biệt hữu ích sau khi thêm các lệnh import ở đầu tệp. Thao tác này cũng làm tăng số khả năng hoàn thành thuộc tính.

Ban đầu, các hộp hoàn thành loại trừ những tên bắt đầu bằng '_' hoặc, đối với module, những tên không được đưa vào '__all__'. Có thể truy cập các tên ẩn bằng cách nhập '_' sau '.', trước hoặc sau khi mở hộp.

.. _calltips:

Gợi ý lệnh gọi
^^^^^^^^^^^^^^

Gợi ý lệnh gọi tự động hiển thị khi nhập :kbd:`(` sau tên của một hàm *accessible*. Biểu thức tên hàm có thể bao gồm dấu chấm và chỉ số. Gợi ý lệnh gọi vẫn hiển thị cho đến khi được nhấp vào, con trỏ được di chuyển ra khỏi vùng đối số hoặc nhập :kbd:`)`. Khi con trỏ nằm trong phần đối số của một định nghĩa, hãy chọn Edit rồi "Show Call Tip" trên menu hoặc nhập phím tắt tương ứng để hiển thị gợi ý lệnh gọi.

Gợi ý lệnh gọi bao gồm chữ ký của hàm và docstring cho đến dòng trống đầu tiên hoặc dòng không trống thứ năm của docstring. (Một số hàm builtin không có chữ ký có thể truy cập.) Dấu '/' hoặc '*' trong chữ ký cho biết các đối số đứng trước hoặc sau nó chỉ được truyền theo vị trí hoặc chỉ được truyền theo tên (keyword). Các chi tiết có thể thay đổi.

Trong Shell, các hàm có thể truy cập phụ thuộc vào những module đã được import vào tiến trình của người dùng, bao gồm cả các module do chính Idle import, và những định nghĩa đã được chạy, kể từ lần khởi động lại gần nhất.

Ví dụ, hãy khởi động lại Shell và nhập ``itertools.count(``. Gợi ý lệnh gọi xuất hiện vì Idle import itertools vào tiến trình của người dùng để tự sử dụng. (Điều này có thể thay đổi.) Nhập ``turtle.write(`` thì không có gì xuất hiện. Bản thân Idle không import turtle. Mục menu và phím tắt cũng không có tác dụng. Nhập ``import turtle``. Sau đó, ``turtle.write(`` sẽ hiển thị gợi ý lệnh gọi.

Trong trình soạn thảo, các câu lệnh import không có tác dụng cho đến khi chạy tệp. Bạn có thể muốn chạy tệp sau khi viết các câu lệnh import, sau khi thêm các định nghĩa hàm hoặc sau khi mở một tệp hiện có.

.. _format-block:

Format block
^^^^^^^^^^^^

Reformat Paragraph định dạng lại một khối ('paragraph') gồm các comment không trống, liên tiếp và có cùng mức thụt lề, một khối văn bản tương tự bên trong chuỗi nhiều dòng hoặc một phần được chọn của một trong hai loại trên. Nếu cần, hãy thêm một dòng trống để phân tách chuỗi với mã. Các dòng chưa đầy đủ trong vùng chọn sẽ được mở rộng thành các dòng hoàn chỉnh. Các dòng kết quả có cùng mức thụt lề như trước, nhưng có tổng độ dài tối đa là N cột (ký tự). Thay đổi giá trị N mặc định là 72 trong thẻ Window của IDLE Settings.

.. _code-context:

Code Context
^^^^^^^^^^^^

Trong một cửa sổ trình soạn thảo chứa mã Python, có thể bật hoặc tắt code context để hiển thị hoặc ẩn một ngăn ở đầu cửa sổ. Khi được hiển thị, ngăn này cố định các dòng mở đầu của những khối mã, chẳng hạn như các dòng bắt đầu bằng từ khóa ``class``, ``def`` hoặc ``if``, vốn nếu không sẽ cuộn khỏi tầm nhìn. Kích thước của ngăn sẽ được mở rộng hoặc thu hẹp khi cần để hiển thị tất cả các cấp context hiện tại, tối đa đến số dòng được xác định trong hộp thoại Configure IDLE (mặc định là 15). Nếu không có dòng context hiện tại nào và tính năng này được bật, một dòng trống duy nhất sẽ được hiển thị. Nhấp vào một dòng trong ngăn context sẽ đưa dòng đó lên đầu trình soạn thảo.

Có thể cấu hình màu văn bản và màu nền của ngăn context trong thẻ Highlights của hộp thoại Configure IDLE.

Cửa sổ Shell
^^^^^^^^^^^^

Trong Shell của IDLE, hãy nhập, chỉnh sửa và gọi lại các câu lệnh hoàn chỉnh. (Hầu hết console và terminal chỉ làm việc với một dòng vật lý tại một thời điểm).

Gửi một câu lệnh một dòng để thực thi bằng cách nhấn :kbd:`Return` khi con trỏ ở bất kỳ vị trí nào trên dòng. Nếu một dòng được mở rộng bằng Backslash (:kbd:`\\`), con trỏ phải nằm trên dòng vật lý cuối cùng. Gửi một câu lệnh phức hợp nhiều dòng bằng cách nhập một dòng trống sau câu lệnh.

Khi dán mã vào Shell, mã chưa được biên dịch và có thể thực thi cho đến khi nhấn :kbd:`Return`, như đã nêu ở trên. Bạn có thể chỉnh sửa mã đã dán trước. Nếu dán nhiều hơn một câu lệnh vào Shell, kết quả sẽ là một
:exc:`SyntaxError` khi nhiều câu lệnh được biên dịch như thể chúng là một.

Các dòng chứa ``RESTART`` cho biết tiến trình thực thi của người dùng đã được khởi động lại. Điều này xảy ra khi tiến trình thực thi của người dùng bị lỗi, khi yêu cầu khởi động lại trên menu Shell hoặc khi chạy mã trong cửa sổ trình soạn thảo.

Các tính năng chỉnh sửa được mô tả trong những tiểu mục trước cũng hoạt động khi nhập mã tương tác. Cửa sổ Shell của IDLE cũng phản hồi với các thao tác sau:

* :kbd:`C-c` cố gắng ngắt việc thực thi câu lệnh (nhưng có thể không thành công).

* :kbd:`C-d` đóng Shell nếu được nhập tại lời nhắc ``>>>``.

* :kbd:`Alt-p` và :kbd:`Alt-n` (:kbd:`C-p` và :kbd:`C-n` trên macOS) truy xuất vào lời nhắc hiện tại câu lệnh đã nhập trước đó hoặc tiếp theo khớp với bất kỳ nội dung nào đã được nhập.

* :kbd:`Return` khi con trỏ đang ở bất kỳ câu lệnh trước nào sẽ nối câu lệnh đó vào mọi nội dung đã nhập tại dấu nhắc.

Màu văn bản
^^^^^^^^^^^

Theo mặc định, IDLE hiển thị văn bản màu đen trên nền trắng, nhưng sẽ tô màu văn bản mang những ý nghĩa đặc biệt. Đối với shell, đó là đầu ra của shell, lỗi của shell, đầu ra của người dùng và lỗi của người dùng. Đối với mã Python, tại dấu nhắc shell hoặc trong trình soạn thảo, đó là từ khóa, tên class và function dựng sẵn, tên đứng sau ``class`` và ``def``, chuỗi và chú thích. Đối với mọi cửa sổ văn bản, đó là con trỏ (khi có), văn bản được tìm thấy (khi có thể) và văn bản được chọn.

IDLE cũng tô sáng :ref:`các soft keyword <soft-keywords>` :keyword:`match`,
:keyword:`case <match>`, và :keyword:`_ <wildcard-patterns>` trong các câu lệnh pattern-matching. Tuy nhiên, việc tô sáng này không hoàn hảo và sẽ không chính xác trong một số trường hợp hiếm gặp, bao gồm một số ``_``-s trong các pattern ``case``.

Việc tô màu văn bản được thực hiện ở chế độ nền, vì vậy đôi khi bạn sẽ thấy văn bản chưa được tô màu. Để thay đổi bảng màu, hãy sử dụng tab Highlighting trong hộp thoại Configure IDLE. Việc đánh dấu các dòng breakpoint của debugger trong trình soạn thảo, cũng như văn bản trong các cửa sổ bật lên và hộp thoại, không thể được người dùng cấu hình.


Khởi động và thực thi mã
------------------------

Khi khởi động với tùy chọn ``-s``, IDLE sẽ thực thi tệp được tham chiếu bởi biến môi trường :envvar:`IDLESTARTUP` hoặc :envvar:`PYTHONSTARTUP`. Trước tiên, IDLE kiểm tra ``IDLESTARTUP``; nếu ``IDLESTARTUP`` hiện diện, tệp được tham chiếu sẽ được chạy. Nếu ``IDLESTARTUP`` không hiện diện, IDLE sẽ kiểm tra ``PYTHONSTARTUP``. Các tệp được tham chiếu bởi những biến môi trường này là nơi thuận tiện để lưu trữ các hàm thường được sử dụng từ IDLE shell hoặc để thực thi các câu lệnh import nhằm nhập các module thường dùng.

Ngoài ra, ``Tk`` cũng tải một tệp khởi động nếu tệp đó hiện diện. Lưu ý rằng tệp Tk luôn được tải. Tệp bổ sung này là ``.Idle.py`` và được tìm trong thư mục chính của người dùng. Các câu lệnh trong tệp này sẽ được thực thi trong namespace Tk, vì vậy tệp này không hữu ích cho việc nhập các hàm để sử dụng từ Python shell của IDLE.

.. _idlelib-cli:

Cách sử dụng dòng lệnh
^^^^^^^^^^^^^^^^^^^^^^

.. program:: idle

Có thể gọi IDLE từ dòng lệnh với nhiều tùy chọn khác nhau. Cú pháp tổng quát là:

.. code-block:: bash

   python -m idlelib [options] [file ...]

Các tùy chọn sau đây hiện có:

.. option:: -c <command>

   Chạy lệnh Python được chỉ định trong cửa sổ shell. Ví dụ, truyền ``-c "print('Hello, World!')"``. Trên Windows, dấu ngoặc kép bên ngoài phải là dấu ngoặc kép như minh họa.

.. option:: -d

   Bật debugger và mở cửa sổ shell.

.. option:: -e

   Mở cửa sổ trình soạn thảo.

.. option:: -h

   In thông báo trợ giúp kèm các tổ hợp tùy chọn hợp lệ rồi thoát.

.. option:: -i

   Mở cửa sổ shell.

.. option:: -r <file>

   Chạy tệp được chỉ định trong cửa sổ shell.

.. option:: -s

   Chạy tệp khởi động (như được xác định bởi các biến môi trường :envvar:`IDLESTARTUP` hoặc :envvar:`PYTHONSTARTUP`) trước khi mở cửa sổ shell.

.. option:: -t <title>

   Đặt tiêu đề cho cửa sổ shell.

.. option:: -

   Đọc và thực thi đầu vào chuẩn trong cửa sổ shell. Tùy chọn này phải là tùy chọn cuối cùng trước mọi đối số.

Nếu có cung cấp đối số:

- Nếu ``-``, ``-c`` hoặc ``-r`` được sử dụng, tất cả các đối số sẽ được đặt trong ``sys.argv[1:]``, và ``sys.argv[0]`` được đặt thành lần lượt là ``''``, ``'-c'`` hoặc ``'-r'``. Cửa sổ trình soạn thảo sẽ không được mở, ngay cả khi đó là thiết lập mặc định trong hộp thoại *Options*.
- Nếu không, các đối số được coi là những tệp cần mở để chỉnh sửa, còn ``sys.argv`` phản ánh các đối số được truyền cho chính IDLE.


Lỗi khởi động
^^^^^^^^^^^^^

IDLE sử dụng một socket để giao tiếp giữa tiến trình GUI của IDLE và tiến trình thực thi mã của người dùng. Kết nối phải được thiết lập mỗi khi Shell khởi động hoặc khởi động lại. (Việc khởi động lại được biểu thị bằng một đường phân cách có nội dung 'RESTART'). Nếu tiến trình của người dùng không kết nối được với tiến trình GUI, tiến trình này thường hiển thị một hộp lỗi ``Tk`` với thông báo 'cannot connect' hướng dẫn người dùng đến đây. Sau đó, tiến trình sẽ thoát.

Một lỗi kết nối cụ thể trên các hệ thống Unix bắt nguồn từ việc cấu hình sai các quy tắc masquerading ở đâu đó trong thiết lập mạng của hệ thống. Khi IDLE được khởi động từ một terminal, bạn sẽ thấy một thông báo bắt đầu bằng ``** Invalid host:``. Giá trị hợp lệ là ``127.0.0.1 (idlelib.rpc.LOCALHOST)``. Có thể chẩn đoán bằng ``tcpconnect -irv 127.0.0.1 6543`` trong một cửa sổ terminal và ``tcplisten <same args>`` trong một cửa sổ khác.

Một nguyên nhân phổ biến gây lỗi là tệp do người dùng viết có cùng tên với một module của thư viện chuẩn, chẳng hạn như *random.py* và *tkinter.py*. Khi một tệp như vậy nằm trong cùng thư mục với tệp sắp được chạy, IDLE không thể import tệp của thư viện chuẩn. Cách khắc phục hiện tại là đổi tên tệp do người dùng viết.

Mặc dù hiện nay ít phổ biến hơn trước, chương trình antivirus hoặc firewall có thể chặn kết nối. Nếu không thể cấu hình chương trình cho phép kết nối, bạn phải tắt chương trình đó thì IDLE mới hoạt động. Cho phép kết nối nội bộ này là an toàn vì không có dữ liệu nào hiển thị trên các cổng bên ngoài. Một vấn đề tương tự là cấu hình mạng không chính xác, khiến các kết nối bị chặn.

Đôi khi các vấn đề trong quá trình cài đặt Python khiến IDLE không khởi động được: nhiều phiên bản có thể xung đột, hoặc một bản cài đặt có thể cần quyền quản trị viên. Nếu không thể khắc phục xung đột, hoặc không thể hay không muốn chạy với quyền quản trị viên, cách dễ nhất có thể là gỡ bỏ hoàn toàn Python rồi bắt đầu lại.

Một tiến trình pythonw.exe bị treo có thể gây ra vấn đề. Trên Windows, hãy dùng Task Manager để kiểm tra và dừng tiến trình đó nếu có. Đôi khi việc khởi động lại do chương trình bị lỗi hoặc Keyboard Interrupt (control-C) gây ra có thể không kết nối được. Đóng hộp thoại lỗi hoặc sử dụng Restart Shell trong menu Shell có thể khắc phục sự cố tạm thời.

Khi IDLE khởi động lần đầu, chương trình cố đọc các tệp cấu hình người dùng trong ``~/.idlerc/`` (~ là thư mục chính của người dùng). Nếu có vấn đề, một thông báo lỗi sẽ được hiển thị. Ngoài các lỗi đĩa ngẫu nhiên, bạn có thể ngăn tình trạng này bằng cách không bao giờ chỉnh sửa các tệp theo cách thủ công. Thay vào đó, hãy sử dụng hộp thoại cấu hình trong Options. Khi một tệp cấu hình người dùng đã có lỗi, giải pháp tốt nhất có thể là xóa tệp đó rồi bắt đầu lại bằng hộp thoại cài đặt.

Nếu IDLE thoát mà không hiển thị thông báo, và không được khởi động từ console, hãy thử khởi động chương trình từ console hoặc terminal (``python -m idlelib``) để xem có xuất hiện thông báo lỗi hay không.

Trên các hệ thống dựa trên Unix có tcl/tk cũ hơn ``8.6.11`` (xem ``About IDLE``), một số ký tự trong một số phông chữ có thể khiến tk gặp lỗi và hiển thị thông báo trên terminal. Điều này có thể xảy ra khi bạn khởi động IDLE để chỉnh sửa một tệp chứa ký tự như vậy hoặc sau đó khi nhập ký tự đó. Nếu không thể nâng cấp tcl/tk, hãy cấu hình lại IDLE để sử dụng một phông chữ hoạt động tốt hơn.

Chạy mã người dùng
^^^^^^^^^^^^^^^^^^

Ngoại trừ một số trường hợp hiếm gặp, kết quả thực thi mã Python bằng IDLE được dự định là giống với kết quả thực thi cùng đoạn mã bằng phương thức mặc định, trực tiếp với Python trong bảng điều khiển hệ thống ở chế độ văn bản hoặc cửa sổ terminal. Tuy nhiên, giao diện và cách vận hành khác nhau đôi khi ảnh hưởng đến các kết quả hiển thị. Chẳng hạn, ``sys.modules`` bắt đầu với nhiều mục hơn, còn ``threading.active_count()`` trả về 2 thay vì 1.

Theo mặc định, IDLE chạy mã người dùng trong một quy trình OS riêng thay vì trong quy trình giao diện người dùng chạy shell và editor. Trong quy trình thực thi, IDLE thay thế ``sys.stdin``, ``sys.stdout`` và ``sys.stderr`` bằng các đối tượng nhận đầu vào từ và gửi đầu ra đến cửa sổ Shell. Các giá trị ban đầu được lưu trong ``sys.__stdin__``, ``sys.__stdout__`` và ``sys.__stderr__`` không bị tác động, nhưng có thể được ``None``.

Việc gửi đầu ra của print từ một quy trình đến một tiện ích văn bản trong quy trình khác chậm hơn so với việc in ra terminal hệ thống trong cùng một quy trình. Điều này ảnh hưởng nhiều nhất khi in nhiều đối số, vì chuỗi cho từng đối số, từng dấu phân cách và ký tự xuống dòng được gửi riêng. Trong quá trình phát triển, điều này thường không thành vấn đề, nhưng nếu muốn in nhanh hơn trong IDLE, hãy định dạng và nối tất cả nội dung muốn hiển thị cùng nhau, sau đó in một chuỗi duy nhất. Cả chuỗi định dạng và :meth:`str.join` đều có thể giúp kết hợp các trường và dòng.

Các thay thế luồng tiêu chuẩn của IDLE không được kế thừa bởi các subprocess được tạo trong quy trình thực thi, dù được tạo trực tiếp bởi mã người dùng hay bởi các module như multiprocessing. Nếu subprocess đó sử dụng ``input`` từ sys.stdin hoặc ``print`` hay ``write`` đến sys.stdout hoặc sys.stderr, IDLE nên được khởi động trong cửa sổ dòng lệnh. (Trên Windows, hãy dùng ``python`` hoặc ``py`` thay vì ``pythonw`` hoặc ``pyw``.) Khi đó, subprocess phụ sẽ được gắn vào cửa sổ này để nhận đầu vào và xuất đầu ra.

Nếu ``sys`` bị mã người dùng đặt lại, chẳng hạn bằng ``importlib.reload(sys)``, các thay đổi của IDLE sẽ mất và việc nhận đầu vào từ bàn phím cũng như xuất đầu ra lên màn hình sẽ không hoạt động chính xác.

Khi Shell được focus, nó điều khiển bàn phím và màn hình. Điều này thường diễn ra trong suốt, nhưng các hàm truy cập trực tiếp vào bàn phím và màn hình sẽ không hoạt động. Những hàm này bao gồm các hàm dành riêng cho hệ thống, dùng để xác định xem một phím đã được nhấn hay chưa và nếu có thì đó là phím nào.

Mã IDLE chạy trong quy trình thực thi thêm các frame vào call stack, vốn sẽ không tồn tại nếu không có IDLE. IDLE bọc ``sys.getrecursionlimit`` và ``sys.setrecursionlimit`` để giảm ảnh hưởng của các frame bổ sung này.

Khi mã người dùng trực tiếp nâng SystemExit hoặc gọi sys.exit, IDLE sẽ quay lại dấu nhắc Shell thay vì thoát.

Đầu ra của người dùng trong Shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi một chương trình xuất văn bản, kết quả được xác định bởi thiết bị đầu ra tương ứng. Khi IDLE thực thi mã người dùng, ``sys.stdout`` và ``sys.stderr`` được kết nối với vùng hiển thị của Shell trong IDLE. Một số tính năng của nó được kế thừa từ widget Tk Text bên dưới. Các tính năng khác là những phần bổ sung được lập trình. Khi có liên quan, Shell được thiết kế cho quá trình phát triển thay vì chạy trong môi trường production.

Chẳng hạn, Shell không bao giờ loại bỏ đầu ra. Một chương trình gửi lượng đầu ra không giới hạn đến Shell cuối cùng sẽ lấp đầy bộ nhớ, dẫn đến lỗi bộ nhớ. Ngược lại, một số cửa sổ văn bản hệ thống chỉ giữ lại n dòng đầu ra cuối cùng. Chẳng hạn, console Windows giữ từ 1 đến 9999 dòng do người dùng thiết lập, mặc định là 300 dòng.

Một widget Tk Text, và do đó cả Shell của IDLE, hiển thị các ký tự (codepoint) trong tập con BMP (Basic Multilingual Plane) của Unicode. Những ký tự nào được hiển thị bằng glyph phù hợp và những ký tự nào được hiển thị bằng ô thay thế phụ thuộc vào hệ điều hành và các font đã cài đặt. Ký tự tab khiến văn bản tiếp theo bắt đầu sau điểm dừng tab kế tiếp. (Chúng xuất hiện sau mỗi 8 'ký tự'.) Ký tự xuống dòng khiến văn bản tiếp theo xuất hiện trên dòng mới. Các ký tự điều khiển khác bị bỏ qua hoặc được hiển thị dưới dạng khoảng trắng, ô vuông hoặc một dạng khác, tùy thuộc vào hệ điều hành và font. (Việc di chuyển con trỏ văn bản qua đầu ra như vậy bằng các phím mũi tên có thể cho thấy hành vi giãn cách khá bất ngờ.)::

   >>> s = 'a\tb\a<\x02><\r>\bc\nd'  # Nhập 22 ký tự.
   >>> len(s)
   14
   >>> s  # Hiển thị repr(s)
   'a\tb\x07<\x02><\r>\x08c\nd'
   >>> print(s, end='')  # Hiển thị s nguyên trạng.
   # Kết quả thay đổi tùy theo hệ điều hành và font. Hãy thử.

Hàm ``repr`` được dùng để echo tương tác các giá trị biểu thức. Hàm này trả về một phiên bản đã biến đổi của chuỗi đầu vào, trong đó các mã điều khiển, một số codepoint BMP và tất cả codepoint không thuộc BMP được thay thế bằng các mã escape. Như minh họa ở trên, hàm này cho phép xác định các ký tự trong một chuỗi, bất kể chúng được hiển thị như thế nào.

Đầu ra thông thường và đầu ra lỗi thường được giữ riêng (trên các dòng riêng biệt) với đầu vào mã và với nhau. Mỗi loại có màu highlight khác nhau.

Đối với traceback SyntaxError, dấu '^' thông thường đánh dấu vị trí phát hiện lỗi được thay thế bằng cách tô màu văn bản bằng highlight lỗi. Khi mã chạy từ một tệp gây ra các exception khác, bạn có thể nhấp chuột phải vào một dòng traceback để chuyển đến dòng tương ứng trong trình chỉnh sửa IDLE. Tệp sẽ được mở nếu cần.

Shell có một tính năng đặc biệt để thu gọn các dòng đầu ra thành nhãn 'Squeezed text'. Việc này được thực hiện tự động đối với đầu ra có hơn N dòng (N = 50 theo mặc định). Có thể thay đổi N trong phần PyShell của trang General trong hộp thoại Settings. Có thể thu gọn đầu ra có ít dòng hơn bằng cách nhấp chuột phải vào đầu ra. Tính năng này có thể hữu ích với những dòng đủ dài để làm chậm việc cuộn.

Đầu ra đã thu gọn được mở rộng tại chỗ bằng cách nhấp đúp vào nhãn. Bạn cũng có thể gửi đầu ra này vào clipboard hoặc một cửa sổ hiển thị riêng bằng cách nhấp chuột phải vào nhãn.

Phát triển ứng dụng tkinter
^^^^^^^^^^^^^^^^^^^^^^^^^^^

IDLE được thiết kế khác với Python tiêu chuẩn để hỗ trợ việc phát triển các chương trình tkinter. Nhập ``import tkinter as tk; root = tk.Tk()`` trong Python tiêu chuẩn thì không có gì xuất hiện. Nhập cùng lệnh đó trong IDLE thì một cửa sổ tk xuất hiện. Trong Python tiêu chuẩn, bạn cũng phải nhập ``root.update()`` để thấy cửa sổ. IDLE thực hiện thao tác tương đương ở chế độ nền, khoảng 20 lần mỗi giây, tức là khoảng mỗi 50 mili giây. Tiếp theo, nhập ``b = tk.Button(root, text='button'); b.pack()``. Một lần nữa, trong Python tiêu chuẩn sẽ không có gì thay đổi rõ ràng cho đến khi nhập ``root.update()``.

Hầu hết các chương trình tkinter đều chạy ``root.mainloop()``, thường sẽ không trả về cho đến khi ứng dụng tk bị hủy. Nếu chương trình được chạy bằng ``python -i`` hoặc từ trình soạn thảo IDLE, lời nhắc shell ``>>>`` sẽ không xuất hiện cho đến khi ``mainloop()`` trả về; khi đó không còn gì để tương tác.

Khi chạy một chương trình tkinter từ trình soạn thảo IDLE, bạn có thể chú thích lệnh gọi mainloop. Khi đó, lời nhắc shell xuất hiện ngay lập tức và bạn có thể tương tác với ứng dụng đang hoạt động. Chỉ cần nhớ bật lại lệnh gọi mainloop khi chạy trong Python tiêu chuẩn.

Chạy mà không có subprocess
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Theo mặc định, IDLE thực thi mã người dùng trong một subprocess riêng thông qua socket, sử dụng giao diện loopback nội bộ. Kết nối này không thể nhìn thấy từ bên ngoài và không có dữ liệu nào được gửi đến hoặc nhận từ internet. Nếu phần mềm tường lửa vẫn cảnh báo, bạn có thể bỏ qua.

Nếu không thể thiết lập kết nối socket, Idle sẽ thông báo cho bạn. Những lỗi như vậy đôi khi chỉ là tạm thời, nhưng nếu kéo dài, vấn đề có thể là do tường lửa chặn kết nối hoặc hệ thống cụ thể được cấu hình không đúng. Cho đến khi khắc phục được vấn đề, bạn có thể chạy Idle với tùy chọn dòng lệnh -n.

Nếu IDLE được khởi động với tùy chọn dòng lệnh -n, chương trình sẽ chạy trong một tiến trình duy nhất và không tạo tiến trình con để chạy máy chủ thực thi Python RPC. Điều này có thể hữu ích nếu Python không thể tạo tiến trình con hoặc giao diện socket RPC trên nền tảng của bạn. Tuy nhiên, ở chế độ này, mã người dùng không được cách ly khỏi chính IDLE. Ngoài ra, môi trường sẽ không được khởi động lại khi chọn Run/Run Module (F5). Nếu mã của bạn đã được sửa đổi, bạn phải reload() các module bị ảnh hưởng và import lại mọi mục cụ thể (ví dụ: from foo import baz) để các thay đổi có hiệu lực. Vì những lý do này, nếu có thể, bạn nên chạy IDLE với tiến trình con mặc định.

.. deprecated:: 3.4


Trợ giúp và tùy chọn
--------------------

.. _help-sources:

Nguồn trợ giúp
^^^^^^^^^^^^^^

Mục "IDLE Help" trong menu Help hiển thị phiên bản html đã định dạng của chương IDLE trong Library Reference. Kết quả được hiển thị trong cửa sổ văn bản tkinter chỉ đọc, gần giống với nội dung bạn thấy trong trình duyệt web. Di chuyển qua văn bản bằng con lăn chuột, thanh cuộn hoặc giữ các phím mũi tên lên và xuống. Hoặc nhấp vào nút TOC (Table of Contents) rồi chọn tiêu đề phần trong hộp được mở ra.

Mục "Python Docs" trong menu Help mở các nguồn trợ giúp phong phú, bao gồm cả tutorial, có tại ``docs.python.org/x.y``, trong đó 'x.y' là phiên bản Python đang chạy. Nếu hệ thống của bạn có bản sao ngoại tuyến của tài liệu (đây có thể là một tùy chọn khi cài đặt), bản sao đó sẽ được mở thay thế.

Bạn có thể thêm hoặc xóa các URL đã chọn khỏi menu trợ giúp bất cứ lúc nào bằng tab General của hộp thoại Configure IDLE.

.. _preferences:

Thiết lập tùy chọn
^^^^^^^^^^^^^^^^^^

Có thể thay đổi tùy chọn phông chữ, tô sáng, phím và tùy chọn chung thông qua Configure IDLE trong menu Option. Các cài đặt người dùng không mặc định được lưu trong thư mục ``.idlerc`` trong thư mục chính của người dùng. Có thể khắc phục các vấn đề do tệp cấu hình người dùng không hợp lệ gây ra bằng cách chỉnh sửa hoặc xóa một hay nhiều tệp trong ``.idlerc``.

Trên tab Font, hãy xem mẫu văn bản để thấy ảnh hưởng của kiểu và kích thước phông chữ lên nhiều ký tự trong nhiều ngôn ngữ. Chỉnh sửa mẫu để thêm các ký tự khác mà bạn quan tâm. Dùng mẫu để chọn các phông chữ đơn cách. Nếu một số ký tự gặp vấn đề trong Shell hoặc trình soạn thảo, hãy thêm chúng vào đầu mẫu rồi thử thay đổi kích thước trước, sau đó thay đổi phông chữ.

Trên tab Highlights and Keys, hãy chọn một chủ đề màu và bộ phím tích hợp sẵn hoặc tùy chỉnh. Để sử dụng chủ đề màu hoặc bộ phím tích hợp sẵn mới hơn với các phiên bản IDLE cũ hơn, hãy lưu chúng dưới dạng chủ đề màu hoặc bộ phím tùy chỉnh mới để các phiên bản IDLE cũ hơn có thể truy cập.

IDLE trên macOS
^^^^^^^^^^^^^^^

Trong System Preferences: Dock, bạn có thể đặt "Prefer tabs when opening documents" thành "Always". Cài đặt này không tương thích với framework GUI tk/tkinter được IDLE sử dụng và làm hỏng một vài tính năng của IDLE.

Tiện ích mở rộng
^^^^^^^^^^^^^^^^

IDLE có một cơ chế tiện ích mở rộng. Có thể thay đổi tùy chọn cho các tiện ích mở rộng bằng tab Extensions của hộp thoại tùy chọn. Xem phần đầu của config-extensions.def trong thư mục idlelib để biết thêm thông tin. Tiện ích mở rộng mặc định duy nhất hiện tại là zzdummy, một ví dụ cũng được dùng để kiểm thử.


idlelib --- triển khai ứng dụng IDLE
------------------------------------

.. module:: idlelib
   :synopsis: Gói triển khai cho shell/editor IDLE.

**Mã nguồn:** :source:`Lib/idlelib`

--------------

Gói Lib/idlelib triển khai ứng dụng IDLE. Xem phần còn lại của trang này để biết cách sử dụng IDLE.

Các tệp trong idlelib được mô tả trong idlelib/README.txt. Bạn có thể truy cập tệp này từ idlelib hoặc nhấp vào Help => About IDLE trong menu IDLE. Tệp này cũng ánh xạ các mục menu IDLE tới mã triển khai mục đó. Ngoại trừ các tệp được liệt kê trong phần 'Startup', mã idlelib là 'private' theo nghĩa các thay đổi về tính năng có thể được backport (xem :pep:`434`).
