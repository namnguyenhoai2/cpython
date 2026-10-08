:mod:`!tkinter` --- Giao diện Python cho Tcl/Tk
===============================================

.. module:: tkinter
   :synopsis: Giao diện cho Tcl/Tk dùng để tạo giao diện người dùng đồ họa

.. moduleauthor:: Guido van Rossum <guido@Python.org>

**Mã nguồn:** :source:`Lib/tkinter/__init__.py`

--------------

Gói :mod:`!tkinter` ("giao diện Tk") là giao diện Python tiêu chuẩn cho bộ công cụ GUI Tcl/Tk. Cả Tk và :mod:`!tkinter` đều có trên hầu hết các nền tảng Unix, bao gồm macOS, cũng như trên các hệ thống Windows.

Chạy ``python -m tkinter`` từ dòng lệnh sẽ mở một cửa sổ minh họa giao diện Tk đơn giản, cho bạn biết rằng :mod:`!tkinter` đã được cài đặt đúng cách trên hệ thống, đồng thời hiển thị phiên bản Tcl/Tk đã cài đặt, để bạn có thể đọc tài liệu Tcl/Tk dành riêng cho phiên bản đó.

Tkinter hỗ trợ nhiều phiên bản Tcl/Tk, được xây dựng có hoặc không có hỗ trợ thread. Tcl/Tk 8.5.12 là phiên bản tối thiểu được hỗ trợ; bản phát hành binary chính thức của Python đi kèm Tcl/Tk 8.6. Xem mã nguồn của module :mod:`_tkinter` để biết thêm thông tin về các phiên bản được hỗ trợ.

.. versionchanged:: 3.11
   Đã loại bỏ hỗ trợ cho các phiên bản Tcl/Tk cũ hơn 8.5.12.

Tkinter không phải là một lớp bao bọc mỏng mà bổ sung khá nhiều logic riêng để mang lại trải nghiệm mang tính Python hơn. Tài liệu này sẽ tập trung vào những phần bổ sung và thay đổi đó, đồng thời tham chiếu tài liệu Tcl/Tk chính thức để biết chi tiết về những phần không thay đổi.

.. note::

   Tcl/Tk 8.5 (2007) giới thiệu một bộ thành phần giao diện người dùng theo chủ đề hiện đại cùng với API mới để sử dụng chúng (xem :mod:`tkinter.ttk`). Cả API cũ và mới vẫn đều khả dụng. Phần lớn tài liệu bạn tìm thấy trên mạng vẫn sử dụng API cũ và có thể đã lỗi thời nghiêm trọng.

.. include:: ../includes/optional-module.rst

.. seealso::

   * `TkDocs <https://tkdocs.com/>`_
      Hướng dẫn chuyên sâu về cách tạo giao diện người dùng bằng Tkinter. Giải thích các khái niệm chính và minh họa những cách tiếp cận được khuyến nghị bằng API hiện đại.

   * `Tài liệu tham khảo Tkinter 8.5: GUI cho Python <https://www.tkdocs.com/shipman/>`_
      Tài liệu tham khảo cho Tkinter 8.5, trình bày chi tiết các lớp, phương thức và tùy chọn hiện có.

   Tài nguyên Tcl/Tk:

   * `Các lệnh Tk <https://www.tcl-lang.org/man/tcl9.0/TkCmd/index.html>`_
      Tài liệu tham khảo đầy đủ về từng lệnh Tcl/Tk nền tảng được Tkinter sử dụng.

   * `Trang chủ Tcl/Tk <https://www.tcl.tk>`_
      Tài liệu bổ sung và các liên kết đến hoạt động phát triển Tcl/Tk core.

   Sách:

   * `Tkinter hiện đại dành cho các nhà phát triển Python bận rộn <https://tkdocs.com/book.html>`_
      Tác giả Mark Roseman. (ISBN 978-1999149567)

   * `Lập trình GUI bằng Python với Tkinter <https://www.packtpub.com/en-us/product/python-gui-programming-with-tkinter-9781788835886>`_
      Của Alan D. Moore. (ISBN 978-1788835886)

   * `Lập trình Python <https://learning-python.com/about-pp4e.html>`_
      Của Mark Lutz; trình bày rất đầy đủ về Tkinter. (ISBN 978-0596158101)

   * `Tcl và bộ công cụ Tk (ấn bản thứ 2) <https://www.amazon.com/exec/obidos/ASIN/032133633X>`_
      Của John Ousterhout, người phát minh ra Tcl/Tk, và Ken Jones; không đề cập đến Tkinter. (ISBN 978-0321336330)


Kiến trúc
---------

Tcl/Tk không phải là một thư viện đơn lẻ mà gồm một vài mô-đun riêng biệt, mỗi mô-đun có chức năng riêng và tài liệu chính thức riêng. Các bản phát hành binary của Python cũng đi kèm một mô-đun bổ sung.

Tcl
   Tcl là một ngôn ngữ lập trình thông dịch động, tương tự Python. Mặc dù có thể được sử dụng độc lập như một ngôn ngữ lập trình đa dụng, Tcl thường được nhúng vào các ứng dụng C nhất dưới dạng một scripting engine hoặc giao diện cho bộ công cụ Tk. Thư viện Tcl có một giao diện C để tạo và quản lý một hoặc nhiều phiên bản của trình thông dịch Tcl, chạy các lệnh và tập lệnh Tcl trong những phiên bản đó, cũng như thêm các lệnh tùy chỉnh được triển khai bằng Tcl hoặc C. Mỗi trình thông dịch có một hàng đợi sự kiện, cùng các cơ chế để gửi sự kiện đến đó và xử lý chúng. Không giống Python, mô hình thực thi của Tcl được thiết kế xoay quanh cơ chế đa nhiệm hợp tác, và Tkinter là cầu nối cho sự khác biệt này (xem `mô hình threading <Threading model_>`_ để biết chi tiết).

Tk
   Tk là một `gói Tcl <https://wiki.tcl-lang.org/37432>`_ được triển khai bằng C, bổ sung các lệnh tùy chỉnh để tạo và thao tác với các widget GUI. Mỗi
   :class:`Tk` đối tượng nhúng một phiên bản trình thông dịch Tcl riêng, trong đó Tk đã được nạp. Các widget của Tk có khả năng tùy biến rất cao, nhưng phải đánh đổi bằng diện mạo lỗi thời. Tk sử dụng hàng đợi sự kiện của Tcl để tạo và xử lý các sự kiện GUI.

Ttk
   Tk có giao diện theo chủ đề (Ttk) là một nhóm widget Tk mới hơn, cung cấp giao diện đẹp hơn nhiều trên các nền tảng khác nhau so với nhiều widget Tk kinh điển. Ttk được phân phối như một phần của Tk, bắt đầu từ phiên bản Tk 8.5. Python binding được cung cấp trong một module riêng biệt, :mod:`tkinter.ttk`.

Bên trong, Tk và Ttk sử dụng các tiện ích của hệ điều hành nền tảng, cụ thể là Xlib trên Unix/X11, Cocoa trên macOS và GDI trên Windows.

Khi ứng dụng Python của bạn sử dụng một class trong Tkinter, chẳng hạn để tạo một widget, module :mod:`!tkinter` trước tiên sẽ tạo một chuỗi lệnh Tcl/Tk. Module này truyền chuỗi lệnh Tcl đó cho một module nhị phân :mod:`_tkinter` nội bộ, sau đó module này gọi trình thông dịch Tcl để đánh giá chuỗi lệnh. Trình thông dịch Tcl sau đó sẽ gọi các package Tk và/hoặc Ttk, những package này lần lượt thực hiện các lệnh gọi đến Xlib, Cocoa hoặc GDI.


Các module Tkinter
------------------

Hỗ trợ cho Tkinter được phân bổ trên một số module. Hầu hết ứng dụng sẽ cần module :mod:`!tkinter` chính, cũng như module :mod:`tkinter.ttk`, cung cấp bộ widget theo chủ đề và API hiện đại::


   from tkinter import *
   from tkinter import ttk


Các module cung cấp hỗ trợ cho Tk bao gồm:

:mod:`!tkinter`
   Module Tkinter chính.

:mod:`tkinter.colorchooser`
   Hộp thoại cho phép người dùng chọn một màu.

:mod:`tkinter.commondialog`
   Lớp cơ sở cho các hộp thoại được định nghĩa trong những mô-đun khác được liệt kê ở đây.

:mod:`tkinter.filedialog`
   Các hộp thoại thông dụng cho phép người dùng chỉ định tệp để mở hoặc lưu.

:mod:`tkinter.font`
   Các tiện ích hỗ trợ làm việc với phông chữ.

:mod:`tkinter.messagebox`
   Truy cập vào các hộp thoại Tk tiêu chuẩn.

:mod:`tkinter.scrolledtext`
   Tiện ích văn bản tích hợp thanh cuộn dọc.

:mod:`tkinter.simpledialog`
   Các hộp thoại cơ bản và các hàm tiện lợi.

:mod:`tkinter.ttk`
   Bộ widget có giao diện theo chủ đề được giới thiệu trong Tk 8.5, cung cấp các lựa chọn hiện đại thay thế cho nhiều widget cổ điển trong module :mod:`!tkinter` chính.

Các module bổ sung:

.. module:: _tkinter
   :synopsis: Một module nhị phân chứa giao diện cấp thấp với Tcl/Tk.

:mod:`_tkinter`
   Một module nhị phân chứa giao diện cấp thấp với Tcl/Tk. Module này được module :mod:`!tkinter` chính tự động import và lập trình viên ứng dụng không bao giờ nên sử dụng trực tiếp. Thông thường, đây là một thư viện dùng chung (hoặc DLL), nhưng trong một số trường hợp có thể được liên kết tĩnh với trình thông dịch Python.

:mod:`idlelib`
   Môi trường Phát triển Tích hợp và Học tập (Integrated Development and Learning Environment - IDLE) của Python. Dựa trên :mod:`!tkinter`.

:mod:`!tkinter.constants`
   Các hằng số ký hiệu có thể được sử dụng thay cho chuỗi khi truyền nhiều tham số khác nhau cho các lệnh gọi Tkinter. Được module :mod:`!tkinter` chính tự động import.

:mod:`tkinter.dnd`
   (thử nghiệm) Hỗ trợ kéo và thả cho :mod:`!tkinter`. Tính năng này sẽ trở nên lỗi thời khi được thay thế bằng Tk DND.

:mod:`turtle`
   Đồ họa Turtle trong cửa sổ Tk.

.. currentmodule:: tkinter


Phao cứu sinh Tkinter
---------------------

Phần này không nhằm cung cấp một hướng dẫn toàn diện về Tk hay Tkinter. Để tìm hiểu nội dung đó, hãy tham khảo một trong các tài nguyên bên ngoài được đề cập trước đó. Thay vào đó, phần này cung cấp một định hướng rất nhanh về diện mạo của một ứng dụng Tkinter, xác định các khái niệm nền tảng của Tk và giải thích cấu trúc của lớp bao bọc Tkinter.

Phần còn lại sẽ giúp bạn xác định các lớp, phương thức và tùy chọn cần dùng trong ứng dụng Tkinter, cũng như nơi tìm tài liệu chi tiết hơn về chúng, bao gồm cả tài liệu tham khảo Tcl/Tk chính thức.


Chương trình Hello World
^^^^^^^^^^^^^^^^^^^^^^^^

Chúng ta sẽ bắt đầu bằng cách xem qua một ứng dụng "Hello World" trong Tkinter. Đây không phải là chương trình nhỏ nhất có thể viết, nhưng có đủ nội dung để minh họa một số khái niệm quan trọng mà bạn cần biết.

::

    from tkinter import *
    from tkinter import ttk
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()


Sau các câu lệnh import, dòng tiếp theo tạo một thể hiện của lớp :class:`Tk`, lớp này khởi tạo Tk và tạo trình thông dịch Tcl liên kết với nó. Dòng này cũng tạo một cửa sổ toplevel, được gọi là cửa sổ gốc, đóng vai trò là cửa sổ chính của ứng dụng.

Dòng sau đây tạo một frame widget, trong trường hợp này sẽ chứa một label và một button mà chúng ta sẽ tạo tiếp theo. Frame nằm gọn bên trong cửa sổ gốc.

Dòng tiếp theo tạo một label widget chứa một chuỗi văn bản tĩnh. Phương thức :meth:`~Grid.grid` được dùng để chỉ định bố cục tương đối (vị trí) của label bên trong frame widget chứa nó, tương tự như cách các bảng trong HTML hoạt động.

Sau đó, một button widget được tạo và đặt bên phải label. Khi được nhấn, nó sẽ gọi phương thức :meth:`~Misc.destroy` của cửa sổ gốc.

Cuối cùng, phương thức :meth:`mainloop` hiển thị mọi thứ và phản hồi dữ liệu đầu vào của người dùng cho đến khi chương trình kết thúc.



Các khái niệm Tk quan trọng
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ngay cả chương trình đơn giản này cũng minh họa các khái niệm Tk chính sau đây:

widgets
  Giao diện người dùng Tkinter được tạo thành từ các *widget* riêng lẻ. Mỗi widget được biểu diễn bằng một đối tượng Python, được khởi tạo từ các lớp như
  :class:`ttk.Frame`, :class:`ttk.Label`, và :class:`ttk.Button`.

phân cấp widget
  Các widget được sắp xếp theo một *cấu trúc phân cấp*. Nhãn và nút nằm trong một frame, và frame này lại nằm trong cửa sổ gốc. Khi tạo mỗi widget *con*, widget *cha* của nó được truyền làm đối số đầu tiên cho constructor của widget.

các tùy chọn cấu hình
  Widget có *các tùy chọn cấu hình*, dùng để thay đổi giao diện và hành vi của chúng, chẳng hạn như văn bản hiển thị trong nhãn hoặc nút. Các lớp widget khác nhau sẽ có những tập tùy chọn khác nhau.

quản lý bố cục
  Các widget không được tự động thêm vào giao diện người dùng khi chúng được tạo. Một *geometry manager* như ``grid`` sẽ kiểm soát vị trí đặt chúng trong giao diện người dùng.

vòng lặp sự kiện
  Tkinter chỉ phản hồi dữ liệu đầu vào của người dùng, các thay đổi từ chương trình của bạn và thậm chí cập nhật màn hình khi đang tích cực chạy một *vòng lặp sự kiện*. Nếu chương trình của bạn không chạy vòng lặp sự kiện, giao diện người dùng sẽ không được cập nhật.


Tìm hiểu cách Tkinter đóng gói Tcl/Tk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi ứng dụng sử dụng các lớp và phương thức của Tkinter, về bản chất Tkinter đang ghép các chuỗi biểu diễn các lệnh Tcl/Tk rồi thực thi những lệnh đó trong trình thông dịch Tcl gắn với :class:`Tk` instance của ứng dụng.

Cho dù bạn đang cố gắng tra cứu tài liệu tham khảo, tìm phương thức hoặc tùy chọn phù hợp, điều chỉnh một đoạn mã hiện có hay gỡ lỗi ứng dụng Tkinter, sẽ có lúc việc hiểu những lệnh Tcl/Tk nền tảng đó trông như thế nào rất hữu ích.

Để minh họa, dưới đây là phần tương đương trong Tcl/Tk của phần chính trong tập lệnh Tkinter ở trên.

::

    ttk::frame .frm -padding 10
    grid .frm
    grid [ttk::label .frm.lbl -text "Hello World!"] -column 0 -row 0
    grid [ttk::button .frm.btn -text "Quit" -command "destroy ."] -column 1 -row 0


Cú pháp của Tcl tương tự nhiều ngôn ngữ shell, trong đó từ đầu tiên là lệnh sẽ được thực thi, tiếp theo là các đối số của lệnh đó, được phân tách bằng dấu cách. Không đi quá sâu vào chi tiết, hãy lưu ý những điều sau:

* Các lệnh dùng để tạo widget (như ``ttk::frame``) tương ứng với các lớp widget trong Tkinter.

* Các tùy chọn widget của Tcl (như ``-text``) tương ứng với các đối số từ khóa trong Tkinter.

* Trong Tcl, các widget được tham chiếu bằng *pathname* (như ``.frm.btn``), trong khi Tkinter không sử dụng tên mà sử dụng các tham chiếu đối tượng.

* Vị trí của một widget trong hệ thống phân cấp widget được mã hóa trong pathname (phân cấp) của nó, sử dụng ``.`` (dấu chấm) làm dấu phân cách đường dẫn. Pathname của cửa sổ gốc chỉ là ``.`` (dấu chấm). Trong Tkinter, hệ thống phân cấp được xác định không phải bằng pathname mà bằng cách chỉ định widget cha khi tạo từng widget con.

* Các thao tác được triển khai dưới dạng các *commands* riêng biệt trong Tcl (như ``grid`` hoặc ``destroy``) được biểu diễn dưới dạng *methods* trên các đối tượng widget của Tkinter. Như bạn sẽ thấy ngay sau đây, đôi khi Tcl sử dụng những gì có vẻ như các lệnh gọi phương thức trên đối tượng widget, gần giống hơn với cách được sử dụng trong Tkinter.


Làm thế nào để...? Tùy chọn nào thực hiện...?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu bạn không chắc cách thực hiện một việc nào đó trong Tkinter và không thể tìm thấy ngay thông tin đó trong tài liệu hướng dẫn hoặc tài liệu tham khảo đang sử dụng, có một vài chiến lược có thể hữu ích.

Trước hết, hãy nhớ rằng chi tiết về cách hoạt động của từng widget có thể khác nhau giữa các phiên bản khác nhau của cả Tkinter và Tcl/Tk. Khi tìm kiếm tài liệu, hãy đảm bảo tài liệu đó tương ứng với các phiên bản Python và Tcl/Tk được cài đặt trên hệ thống của bạn.

Khi tìm cách sử dụng một API, việc biết chính xác tên của class, option hoặc method mà bạn đang dùng sẽ rất hữu ích. Introspection, είτε trong Python shell tương tác hoặc với :func:`print`, có thể giúp bạn xác định những gì mình cần.

Để biết những tùy chọn cấu hình nào có sẵn trên bất kỳ widget nào, hãy gọi
method :meth:`~Misc.configure` của nó; method này trả về một dictionary chứa nhiều thông tin về từng đối tượng, bao gồm các giá trị mặc định và hiện tại. Dùng :meth:`~Misc.keys` để chỉ lấy tên của từng tùy chọn.

::

    btn = ttk.Button(frm, ...)
    print(btn.configure().keys())

Vì hầu hết widget đều có nhiều tùy chọn cấu hình dùng chung, việc tìm hiểu tùy chọn nào là riêng của một class widget cụ thể có thể hữu ích. So sánh danh sách tùy chọn với danh sách của một widget đơn giản hơn, chẳng hạn như frame, là một cách để thực hiện việc đó.

::

    print(set(btn.configure().keys()) - set(frm.configure().keys()))

Tương tự, bạn có thể tìm các method có sẵn cho một đối tượng widget bằng hàm :func:`dir` tiêu chuẩn. Nếu thử, bạn sẽ thấy có hơn 200 method widget phổ biến, vì vậy việc xác định những method riêng của một class widget cũng rất hữu ích.

::

    print(dir(btn))
    print(set(dir(btn)) - set(dir(frm)))


Tra cứu sổ tay tham khảo Tcl/Tk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Như đã đề cập, sổ tay tham khảo chính thức về các `lệnh Tk <https://www.tcl-lang.org/man/tcl9.0/TkCmd/index.html>`_ (các trang hướng dẫn) thường là mô tả chính xác nhất về tác dụng của từng thao tác cụ thể trên widget. Ngay cả khi đã biết tên của tùy chọn hoặc phương thức cần dùng, bạn vẫn có thể phải tra cứu ở một vài nơi.

Mặc dù mọi thao tác trong Tkinter đều được triển khai dưới dạng các lời gọi phương thức trên đối tượng widget, bạn đã thấy rằng nhiều thao tác Tcl/Tk xuất hiện dưới dạng các lệnh nhận đường dẫn widget làm tham số đầu tiên, theo sau là các tham số tùy chọn, chẳng hạn như

::

    destroy .
    grid .frm.btn -column 0 -row 0

Tuy nhiên, một số thao tác khác trông giống các phương thức được gọi trên một đối tượng widget hơn (trên thực tế, khi bạn tạo một widget trong Tcl/Tk, nó tạo một lệnh Tcl có tên là đường dẫn widget, trong đó tham số đầu tiên của lệnh đó là tên của phương thức cần gọi).

::

    .frm.btn invoke
    .frm.lbl configure -text "Goodbye"


Trong tài liệu tham khảo Tcl/Tk chính thức, bạn sẽ tìm thấy hầu hết các thao tác trông giống như lời gọi phương thức trên trang hướng dẫn của một widget cụ thể (ví dụ: bạn sẽ tìm thấy phương thức :meth:`~tkinter.ttk.Button.invoke` trên trang hướng dẫn của `ttk::button <https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_button.html>`_), trong khi các hàm nhận một widget làm tham số thường có trang hướng dẫn riêng (ví dụ: `grid <https://www.tcl-lang.org/man/tcl9.0/TkCmd/grid.html>`_).

Bạn sẽ tìm thấy nhiều tùy chọn và phương thức phổ biến trong các trang hướng dẫn `tùy chọn <https://www.tcl-lang.org/man/tcl9.0/TkCmd/options.html>`_ hoặc `ttk::widget <https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_widget.html>`_, trong khi những tùy chọn và phương thức khác nằm trên trang hướng dẫn của một lớp widget cụ thể.

Bạn cũng sẽ thấy rằng nhiều phương thức Tkinter có tên ghép, chẳng hạn như
:meth:`~Misc.winfo_x`, :meth:`~Misc.winfo_height`,
:meth:`~Misc.winfo_viewable`. Bạn có thể tìm tài liệu về tất cả những nội dung này trong trang hướng dẫn `winfo <https://www.tcl-lang.org/man/tcl9.0/TkCmd/winfo.html>`_.

.. note::
   Hơi khó hiểu là tất cả widget Tkinter cũng có các phương thức không thực sự thao tác trên widget mà hoạt động ở phạm vi toàn cục, độc lập với mọi widget. Ví dụ gồm các phương thức truy cập clipboard hoặc chuông hệ thống. (Chúng được triển khai dưới dạng phương thức trong lớp cơ sở :class:`Widget` mà tất cả widget Tkinter đều kế thừa).


.. _`Threading model`:

Mô hình luồng
-------------

Python và Tcl/Tk có các mô hình luồng rất khác nhau, và :mod:`!tkinter` cố gắng kết nối hai mô hình này. Nếu sử dụng các luồng, bạn có thể cần lưu ý điều này.

Một trình thông dịch Python có thể có nhiều luồng liên kết với nó. Trong Tcl, có thể tạo nhiều luồng, nhưng mỗi luồng có một thực thể trình thông dịch Tcl riêng liên kết với nó. Các luồng cũng có thể tạo nhiều hơn một thực thể trình thông dịch, mặc dù mỗi thực thể trình thông dịch chỉ có thể được sử dụng bởi luồng đã tạo ra nó.

Mỗi đối tượng :class:`Tk` được tạo bởi :mod:`!tkinter` đều chứa một trình thông dịch Tcl. Đối tượng này cũng theo dõi luồng đã tạo ra trình thông dịch đó. Các lệnh gọi đến
:mod:`!tkinter` có thể được thực hiện từ bất kỳ luồng Python nào. Về nội bộ, nếu một lệnh gọi đến từ một luồng khác với luồng đã tạo đối tượng :class:`Tk`, một sự kiện sẽ được đăng vào hàng đợi sự kiện của trình thông dịch; khi được thực thi, kết quả sẽ được trả về cho luồng Python đã gọi.

Các ứng dụng Tcl/Tk thường được điều khiển bởi sự kiện, nghĩa là sau khi khởi tạo, interpreter chạy một vòng lặp sự kiện (tức là
:meth:`Tk.mainloop <Misc.mainloop>`) và phản hồi các sự kiện. Vì chỉ chạy trên một thread, các trình xử lý sự kiện phải phản hồi nhanh; nếu không, chúng sẽ chặn các sự kiện khác được xử lý. Để tránh điều này, mọi phép tính chạy lâu không nên chạy trong trình xử lý sự kiện, mà nên được chia thành các phần nhỏ hơn bằng timer hoặc chạy trong một thread khác. Điều này khác với nhiều GUI toolkit, trong đó GUI chạy trên một thread hoàn toàn tách biệt với toàn bộ mã ứng dụng, bao gồm cả các trình xử lý sự kiện.

Nếu Tcl interpreter không chạy vòng lặp sự kiện và xử lý các sự kiện, mọi
:mod:`!tkinter` được gọi từ các thread khác với thread đang chạy Tcl interpreter sẽ thất bại.

Có một số trường hợp đặc biệt:

* Các thư viện Tcl/Tk được xây dựng mà không hỗ trợ thread hiện nay rất hiếm: Tcl/Tk 8.6 đi kèm được xây dựng với hỗ trợ thread, vì vậy trường hợp này chỉ xảy ra với một số bản dựng cũ không hỗ trợ thread. Khi thư viện không nhận biết thread,
  :mod:`!tkinter` gọi thư viện từ thread Python khởi tạo, ngay cả khi thread này khác với thread đã tạo Tcl interpreter. Một global lock đảm bảo mỗi lần chỉ có một lệnh gọi được thực hiện.

* Mặc dù :mod:`!tkinter` cho phép bạn tạo nhiều hơn một instance của đối tượng :class:`Tk` (với interpreter riêng), tất cả các interpreter thuộc cùng một thread đều dùng chung một hàng đợi sự kiện, và điều này nhanh chóng trở nên rắc rối. Trên thực tế, đừng tạo nhiều hơn một instance của :class:`Tk` tại một thời điểm. Nếu không, tốt nhất là tạo chúng trong các thread riêng biệt và đảm bảo bạn đang chạy bản dựng Tcl/Tk hỗ trợ thread.

* Các trình xử lý sự kiện blocking không phải là cách duy nhất để ngăn Tcl interpreter chạy lại event loop. Thậm chí bạn có thể chạy nhiều event loop lồng nhau hoặc từ bỏ event loop hoàn toàn. Nếu bạn đang thực hiện bất kỳ thao tác phức tạp nào liên quan đến sự kiện hoặc thread, hãy lưu ý những khả năng này.

* Hiện tại có một vài hàm :mod:`!tkinter` được chọn chỉ hoạt động khi được gọi từ thread đã tạo Tcl interpreter.


Tài liệu tham khảo hữu ích
--------------------------


.. _tkinter-setting-options:

Thiết lập các tùy chọn
^^^^^^^^^^^^^^^^^^^^^^

Các tùy chọn kiểm soát những yếu tố như màu sắc và độ rộng đường viền của widget. Có thể thiết lập các tùy chọn theo ba cách:

Tại thời điểm tạo đối tượng, bằng cách sử dụng keyword arguments
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

      fred = Button(self, fg="red", bg="blue")

Sau khi tạo đối tượng, xử lý tên tùy chọn như một chỉ mục từ điển
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

      fred["fg"] = "red" fred["bg"] = "blue"

Sử dụng phương thức config() để cập nhật nhiều thuộc tính sau khi tạo đối tượng
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

      fred.config(fg="red", bg="blue")

.. note::

   Các tùy chọn ``fg`` và ``bg`` được sử dụng ở đây, cùng với các tùy chọn khác điều khiển giao diện của widget, thuộc về các widget :mod:`!tkinter` cổ điển. Các widget :mod:`tkinter.ttk` theo chủ đề được khuyến nghị trong phần giới thiệu không chấp nhận chúng; hãy tạo kiểu cho widget theo chủ đề thông qua lớp :class:`ttk.Style <tkinter.ttk.Style>`. Ba cách thiết lập tùy chọn được trình bày ở trên áp dụng cho cả hai bộ widget.

Để xem giải thích đầy đủ về một tùy chọn cụ thể và cách hoạt động của tùy chọn đó, hãy tham khảo các trang hướng dẫn Tk dành cho widget tương ứng.

Lưu ý rằng các trang man liệt kê "STANDARD OPTIONS" và "WIDGET SPECIFIC OPTIONS" cho từng widget. Mục đầu tiên là danh sách các tùy chọn dùng chung cho nhiều widget, còn mục sau là các tùy chọn riêng của widget cụ thể đó. Standard Options được mô tả trong trang man :manpage:`options(3)`.

Tài liệu này không phân biệt giữa các tùy chọn tiêu chuẩn và tùy chọn riêng của widget. Một số tùy chọn không áp dụng cho một số loại widget. Việc một widget có phản hồi với một tùy chọn cụ thể hay không phụ thuộc vào class của widget; button có tùy chọn ``command``, còn label thì không.

Các tùy chọn được một widget hỗ trợ được liệt kê trong trang man của widget đó hoặc có thể được truy vấn tại runtime bằng cách gọi method :meth:`~Misc.config` không có đối số, hoặc gọi method :meth:`~Misc.keys` trên widget đó. Giá trị trả về của các lệnh gọi này là một dictionary, trong đó key là tên của tùy chọn dưới dạng chuỗi (ví dụ: ``'relief'``) và value là các tuple gồm 5 phần tử.

Một số tùy chọn, chẳng hạn như ``bg``, là từ đồng nghĩa của các tùy chọn thông dụng có tên dài (``bg`` là dạng viết tắt của "background").

+---------+--------------------------------------------+--------------+
| Chỉ mục | Ý nghĩa                                    | Ví dụ        |
+=========+============================================+==============+
| 0       | tên tùy chọn                               | ``'relief'`` |
+---------+--------------------------------------------+--------------+
| 1       | tên tùy chọn dùng để tra cứu cơ sở dữ liệu | ``'relief'`` |
+---------+--------------------------------------------+--------------+
| 2       | lớp tùy chọn dùng để tra cứu cơ sở dữ liệu | ``'Relief'`` |
+---------+--------------------------------------------+--------------+
| 3       | giá trị mặc định                           | ``'raised'`` |
+---------+--------------------------------------------+--------------+
| 4       | giá trị hiện tại                           | ``'groove'`` |
+---------+--------------------------------------------+--------------+

Ví dụ::

   >>> print(fred.config())
   {'relief': ('relief', 'relief', 'Relief', 'raised', 'groove')}

Tất nhiên, từ điển được in ra sẽ bao gồm tất cả các tùy chọn hiện có và giá trị của chúng. Đây chỉ là một ví dụ.


.. _pack-the-packer:
.. _tkinter-geometry-management:
.. _the-packer:
.. _packer-options:

Quản lý bố cục
^^^^^^^^^^^^^^

.. index::
   single: geometry management (widgets)
   single: packing (widgets)

Việc tạo một widget không khiến widget đó hiển thị. Widget chỉ xuất hiện sau khi được chuyển cho *trình quản lý hình học*, thành phần xác định kích thước và vị trí của widget bên trong vùng chứa, đồng thời giữ cho bố cục được cập nhật khi vùng chứa được thay đổi kích thước hoặc nội dung của nó thay đổi. Quên gọi trình quản lý hình học là một lỗi phổ biến ở giai đoạn đầu: widget đã được tạo nhưng không có gì xuất hiện.

Tk cung cấp ba trình quản lý hình học. Mỗi trình quản lý đều được mọi widget kế thừa, vì vậy bất kỳ widget nào cũng có thể được quản lý bằng bất kỳ trình quản lý nào (nhưng hãy xem cảnh báo bên dưới về sự không tương thích giữa grid và pack). Lựa chọn phụ thuộc vào loại bố cục bạn muốn.

:meth:`grid <Grid.grid_configure>`
   Sắp xếp các widget trong một bảng hai chiều gồm các hàng và cột. Đây là trình quản lý linh hoạt nhất và là lựa chọn mặc định: những bố cục nếu không sẽ cần nhiều frame lồng nhau thường có thể được biểu diễn bằng một grid duy nhất, đồng thời có thể chỉ định cách các hàng và cột hấp thụ phần không gian thừa.

   ::

      ttk.Label(frm, text="Name:").grid(column=0, row=0, sticky="w")
      ttk.Entry(frm).grid(column=1, row=0)
      ttk.Button(frm, text="OK").grid(column=1, row=1, sticky="e")

:meth:`pack <Pack.pack_configure>`
   Xếp chồng các widget về một phía của vùng chứa -- ``"top"`` (mặc định), ``"bottom"``, ``"left"`` hoặc ``"right"`` -- và có thể khiến chúng lấp đầy hoặc mở rộng vào phần không gian còn lại. Cách này thuận tiện cho các sắp xếp đơn giản, chẳng hạn như một hàng hoặc cột widget duy nhất, hoặc một vùng nội dung được bao quanh bởi thanh công cụ và thanh trạng thái.

   ::

      toolbar.pack(side="top", fill="x")
      status.pack(side="bottom", fill="x")
      body.pack(side="left", expand=True, fill="both")

:meth:`place <Place.place_configure>`
   Đặt từng widget tại một vị trí cụ thể, được xác định bằng khoảng cách tuyệt đối trên màn hình hoặc bằng một phần kích thước của vùng chứa. Cách này cung cấp khả năng kiểm soát cao nhất nhưng ít hành vi tự động nhất, và được sử dụng ít nhất; nó phù hợp với các trường hợp đặc biệt như những widget chồng lấp hoặc các bố cục tùy chỉnh chính xác.

   ::

      background.place(x=0, y=0, relwidth=1.0, relheight=1.0)
      badge.place(relx=1.0, rely=0.0, anchor="ne")

Các widget Classic và themed :mod:`tkinter.ttk` có thể được quản lý thay thế cho nhau.

.. warning::

   Không áp dụng :meth:`!pack` và :meth:`!grid` cho hai widget dùng chung một container. Hai trình quản lý thương lượng kích thước theo những cách không tương thích, và ứng dụng có thể bị treo khi chúng liên tục thay đổi kích thước container theo hướng đối nghịch nhau. Để kết hợp chúng, hãy đặt các widget của mỗi trình quản lý trong một frame riêng.

Toàn bộ các tùy chọn mà mỗi trình quản lý chấp nhận, cùng với giá trị và giá trị mặc định của chúng, được ghi trong :meth:`Grid.grid_configure`, :meth:`Pack.pack_configure` và :meth:`Place.place_configure`; xem thêm các trang man :manpage:`grid(3tk)`, :manpage:`pack(3tk)` và :manpage:`place(3tk)`.


.. _coupling-widget-variables:

Liên kết biến widget
^^^^^^^^^^^^^^^^^^^^

Một số widget có thể liên kết trực tiếp giá trị hiện tại của chúng với một biến chương trình, để hai bên luôn đồng bộ. Các tùy chọn như ``variable``, ``textvariable``, ``value``, ``onvalue`` và ``offvalue`` thiết lập kết nối này: khi người dùng thay đổi widget, biến sẽ được cập nhật; và khi biến được gán giá trị, widget sẽ vẽ lại để khớp với biến.

Một widget chỉ có thể được liên kết với một đối tượng :class:`Variable`, không phải một biến Python thông thường. Đây không phải là hạn chế của :mod:`!tkinter` mà là hệ quả của sự khác biệt giữa hai ngôn ngữ: liên kết này dựa vào việc Tcl được thông báo mỗi khi giá trị thay đổi, còn Python không có cách nào phản ứng khi một biến thông thường được gán lại. Một :class:`Variable` giải quyết vấn đề này bằng cách lưu giá trị bên trong trình thông dịch Tcl và cung cấp giá trị đó thông qua các phương thức :meth:`~Variable.get` và :meth:`~Variable.set` tường minh.

Các lớp con có sẵn bao quát những kiểu thường gặp:
:class:`StringVar`, :class:`IntVar`, :class:`DoubleVar` và :class:`BooleanVar`. Truyền một đối tượng trong số đó vào tùy chọn ``textvariable`` (hoặc ``variable``) của widget, sau đó đọc và cập nhật nó bằng :meth:`~Variable.get` và :meth:`~Variable.set`; widget sẽ tự theo dõi đối tượng đó mà bạn không cần làm thêm gì.

Giữ tham chiếu đến biến chừng nào widget còn sử dụng biến đó -- chẳng hạn bằng cách lưu biến dưới dạng thuộc tính. Một :class:`Variable` bị thu gom rác sẽ xóa biến Tcl bên dưới, làm mất kết nối với widget (xem :class:`Variable`).

Ví dụ::

   import tkinter as tk
   from tkinter import ttk

   root = tk.Tk()

   # Tạo biến của ứng dụng và gán giá trị ban đầu cho biến.
   contents = tk.StringVar(value="this is a variable")

   # Yêu cầu widget entry theo dõi biến.
   entry = ttk.Entry(root, textvariable=contents)
   entry.pack()

   # In giá trị hiện tại mỗi khi người dùng nhấn Return.
   def print_contents(event):
       print("The current entry content is:", contents.get())

   entry.bind("<Return>", print_contents)

   # Việc đặt giá trị cho biến từ chương trình sẽ cập nhật entry thông qua
   # cùng một liên kết.
   def clear():
       contents.set("")

   ttk.Button(root, text="Clear", command=clear).pack()

   root.mainloop()

.. _tkinter-window-manager:

Trình quản lý cửa sổ
^^^^^^^^^^^^^^^^^^^^

.. index:: single: window manager (widgets)

*Trình quản lý cửa sổ* là bộ phận của desktop chịu trách nhiệm hiển thị thanh tiêu đề, đường viền và các điều khiển xung quanh mỗi cửa sổ cấp cao nhất, cũng như các thuộc tính như tiêu đề, vị trí, kích thước và biểu tượng của cửa sổ. Tk cung cấp quyền truy cập vào các thuộc tính này thông qua :class:`Wm` mixin, được kế thừa bởi cửa sổ gốc :class:`Tk` và mọi :class:`Toplevel`. Vì vậy, bạn gọi trực tiếp các phương thức của trình quản lý cửa sổ trên một cửa sổ cấp cao nhất. Mỗi phương thức có một tên ngắn và một tên tương đương có tiền tố ``wm_``, chẳng hạn như :meth:`~Wm.title` và :meth:`~Wm.wm_title`.

Các phương thức này tác động lên cửa sổ cấp cao nhất, bất kể nội dung của cửa sổ được xây dựng từ các widget cổ điển hay các widget :mod:`tkinter.ttk` theo chủ đề. Để truy cập cửa sổ cấp cao nhất chứa một widget bất kỳ, hãy gọi phương thức :meth:`~Misc.winfo_toplevel` của widget đó.

Ví dụ::

   import tkinter as tk
   from tkinter import ttk

   root = tk.Tk()
   root.title("My Application")
   root.geometry("640x480")
   root.minsize(320, 240)

   ttk.Label(root, text="Hello").pack(padx=20, pady=20)

   root.mainloop()

Xem :class:`Wm` để biết đầy đủ các phương thức của trình quản lý cửa sổ.


.. _Tk-option-data-types:

Các kiểu dữ liệu tùy chọn của Tk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: single: Tk Option Data Types

Nhiều tùy chọn widget được mô tả trong tài liệu tham khảo chấp nhận các giá trị thuộc một số ít kiểu dữ liệu phổ biến, được mô tả ở đây.

anchor
   Các giá trị hợp lệ là các hướng trên la bàn: ``"n"``, ``"ne"``, ``"e"``, ``"se"``, ``"s"``, ``"sw"``, ``"w"``, ``"nw"``, và ``"center"``.

bitmap
   Có mười bitmap được tích hợp sẵn và có tên: ``'error'``, ``'gray12'``, ``'gray25'``, ``'gray50'``, ``'gray75'``, ``'hourglass'``, ``'info'``, ``'questhead'``, ``'question'``, ``'warning'``. Để chỉ định tên tệp X bitmap, hãy cung cấp đường dẫn đầy đủ đến tệp, đặt trước bằng ``@``, như trong ``"@/usr/contrib/bitmap/gumby.bit"``.

boolean
   Bạn có thể truyền các số nguyên 0 hoặc 1, hoặc các chuỗi ``"yes"`` hoặc ``"no"``.

callback
   Đây là bất kỳ hàm Python nào không nhận đối số. Ví dụ::

      def print_it():
          print("hi there")
      fred["command"] = print_it

màu sắc
   Màu sắc có thể được cung cấp dưới dạng tên của các màu X trong tệp rgb.txt hoặc dưới dạng chuỗi biểu diễn các giá trị RGB trong phạm vi 4 bit: ``"#RGB"``, 8 bit: ``"#RRGGBB"``, 12 bit: ``"#RRRGGGBBB"`` hoặc 16 bit: ``"#RRRRGGGGBBBB"``, trong đó R,G,B ở đây đại diện cho bất kỳ chữ số thập lục phân hợp lệ nào. Xem trang hướng dẫn :manpage:`colors(3tk)` để biết danh sách các màu có tên.

con trỏ
   Tên của con trỏ chuột sẽ hiển thị khi con trỏ nằm trên widget. Tk cung cấp một tập hợp tên con trỏ có tính di động, khả dụng trên mọi nền tảng (ví dụ ``"arrow"``, ``"watch"``, ``"cross"`` hoặc ``"hand2"``); cũng có thể sử dụng các tên con trỏ X tiêu chuẩn từ :file:`cursorfont.h` mà không cần tiền tố ``XC_`` (do đó ``XC_hand2`` trở thành ``"hand2"``). Danh sách đầy đủ các tên, bao gồm cả những tên dành riêng cho từng nền tảng, được cung cấp trong trang hướng dẫn :manpage:`cursors(3tk)`. Bạn cũng có thể chỉ định tệp bitmap và tệp mask của riêng mình. Trên Windows, có thể sử dụng trực tiếp tệp con trỏ (:file:`.cur` hoặc :file:`.ani`) bằng cách cung cấp đường dẫn của tệp với tiền tố ``@``, như trong ``"@C:/cursors/bart.ani"``.

khoảng cách
   Khoảng cách trên màn hình có thể được chỉ định bằng pixel hoặc theo khoảng cách tuyệt đối. Pixel được biểu diễn bằng các số, còn khoảng cách tuyệt đối được biểu diễn bằng chuỗi, trong đó ký tự ở cuối biểu thị đơn vị: ``c`` cho centimet, ``i`` cho inch, ``m`` cho milimet, ``p`` cho point của máy in. Ví dụ, 3.5 inch được biểu diễn là ``"3.5i"``.

phông chữ
   Tk sử dụng một mô tả phông chữ như ``{courier 10 bold}``; trong
   :mod:`!tkinter` trường hợp này được truyền tự nhiên nhất dưới dạng một tuple gồm ``(family, size, *styles)`` (hoặc dưới dạng chuỗi tương đương ``"Courier 10 bold"``). Kích thước phông chữ với số dương được đo bằng point; kích thước với số âm được đo bằng pixel.

hình học
   Đây là một chuỗi có dạng ``widthxheight``, trong đó chiều rộng và chiều cao được đo bằng pixel đối với hầu hết widget (bằng số ký tự đối với các widget hiển thị văn bản). Ví dụ: ``fred["geometry"] = "200x100"``.

căn chỉnh
   Các giá trị hợp lệ là các chuỗi: ``"left"``, ``"center"`` và ``"right"``.

region
   Đây là một chuỗi gồm bốn phần tử được phân cách bằng dấu cách, mỗi phần tử đều là một khoảng cách hợp lệ (xem ở trên). Ví dụ: ``"2 3 4 5"`` và ``"3i 2i 4.5i 2i"`` và ``"3c 2c 4c 10.43c"`` đều là các region hợp lệ.

relief
   Xác định kiểu đường viền của widget. Các giá trị hợp lệ là: ``"raised"``, ``"sunken"``, ``"flat"``, ``"groove"``, ``"ridge"`` và ``"solid"``.

scrollcommand
   Đây hầu như luôn là phương thức :meth:`!set` của một widget scrollbar nào đó, nhưng cũng có thể là bất kỳ phương thức widget nào nhận một đối số duy nhất.

wrap
   Phải là một trong các giá trị sau: ``"none"``, ``"char"`` hoặc ``"word"``.

.. _Bindings-and-Events:

Bindings và sự kiện
^^^^^^^^^^^^^^^^^^^

.. index::
   single: bind (widgets)
   single: events (widgets)

Phương thức bind từ lệnh widget cho phép bạn theo dõi một số sự kiện nhất định và gọi một hàm callback khi loại sự kiện đó xảy ra. Dạng của phương thức bind là::

   def bind(self, sequence, func, add=''):

trong đó:

sequence
   là một chuỗi biểu thị loại sự kiện đích. Các sự kiện vật lý sử dụng dạng ``<modifier-modifier-type-detail>`` (ví dụ ``"<Enter>"`` hoặc ``"<Control-Button-1>"``); các sự kiện ảo do ứng dụng định nghĩa sử dụng cặp dấu ngoặc nhọn, như trong ``"<<Paste>>"``. (Xem
   trang hướng dẫn :manpage:`bind(3tk)` để biết chi tiết.)

func
   là một hàm Python, nhận một đối số và được gọi khi sự kiện xảy ra. Một instance Event sẽ được truyền vào làm đối số. (Các hàm được triển khai theo cách này thường được gọi là *callbacks*.)

add
   là tùy chọn, có thể là ``''`` hoặc ``'+'``. Truyền một chuỗi rỗng cho biết binding này sẽ thay thế mọi binding khác được liên kết với sự kiện này. Truyền một ``'+'`` có nghĩa là hàm này sẽ được thêm vào danh sách các hàm được liên kết với loại sự kiện này.

Ví dụ::

   def turn_red(self, event):
       event.widget["activeforeground"] = "red"

   self.button.bind("<Enter>", self.turn_red)

Lưu ý cách trường widget của sự kiện được truy cập trong callback ``turn_red()``. Trường này chứa widget đã bắt sự kiện X. Bảng sau liệt kê các trường sự kiện khác mà bạn có thể truy cập và cách chúng được ký hiệu trong Tk; điều này có thể hữu ích khi tham khảo các trang hướng dẫn của Tk.

+----+---------------------+----+---------------------+
| Tk | Tkinter Event Field | Tk | Tkinter Event Field |
+====+=====================+====+=====================+
| %f | focus               | %A | char                |
+----+---------------------+----+---------------------+
| %h | height              | %E | send_event          |
+----+---------------------+----+---------------------+
| %k | keycode             | %K | keysym              |
+----+---------------------+----+---------------------+
| %s | state               | %N | keysym_num          |
+----+---------------------+----+---------------------+
| %t | time                | %T | type                |
+----+---------------------+----+---------------------+
| %w | width               | %W | widget              |
+----+---------------------+----+---------------------+
| %x | x                   | %X | x_root              |
+----+---------------------+----+---------------------+
| %y | y                   | %Y | y_root              |
+----+---------------------+----+---------------------+
| %# | serial              | %b | num                 |
+----+---------------------+----+---------------------+
| %d | detail              | %D | delta               |
+----+---------------------+----+---------------------+

Tham số ``add`` ở trên chỉ ảnh hưởng đến các binding mà bạn tự tạo. Mỗi widget cũng kế thừa *các binding của lớp* để triển khai hành vi tiêu chuẩn của nó -- ví dụ: một :class:`Text` widget liên kết :kbd:`Control-t` để hoán đổi hai ký tự. Các binding này được mô tả trong phần bindings của trang hướng dẫn Tk của widget (chẳng hạn như :manpage:`text(3tk)` hoặc :manpage:`entry(3tk)`).

Các binding của lớp được xử lý riêng với binding của bạn, vì vậy việc tự binding một event không thay thế binding mặc định; cả hai đều chạy. Để ngăn một binding mặc định không mong muốn, hãy binding event trên widget và trả về chuỗi ``"break"`` từ callback của bạn.


Tham số index
^^^^^^^^^^^^^

Một số widget yêu cầu truyền các tham số "index". Các tham số này được dùng để trỏ đến một vị trí cụ thể trong widget Text, đến các ký tự cụ thể trong widget Entry hoặc đến các mục menu cụ thể trong widget Menu.

Các index của widget Entry (index, view index, v.v.)
   Widget Entry có các phương thức và tùy chọn tham chiếu đến vị trí ký tự trong văn bản đang hiển thị. Bất cứ khi nào cần một index, bạn có thể truyền vào:

   * một số nguyên biểu thị vị trí số của một ký tự, được đếm từ đầu văn bản, bắt đầu từ 0;

   * chuỗi ``"anchor"``, tham chiếu đến điểm neo của vùng chọn, được thiết lập bằng các phương thức selection của widget;

   * chuỗi ``"end"``, tham chiếu đến vị trí ngay sau ký tự cuối cùng;

   * chuỗi ``"insert"``, tham chiếu đến ký tự ngay sau con trỏ chèn;

   * các chuỗi ``"sel.first"`` và ``"sel.last"``, tham chiếu đến ký tự đầu tiên trong vùng chọn và vị trí ngay sau ký tự cuối cùng (sẽ xảy ra lỗi nếu sử dụng các chuỗi này khi không có vùng chọn nào);

   * một chuỗi gồm ``@`` theo sau là một số nguyên, như trong ``"@6"``, trong đó số nguyên được hiểu là tọa độ pixel x trong hệ tọa độ của entry, dùng để chọn ký tự bao quanh điểm đó.

Các chỉ mục của Text widget
   Ký hiệu chỉ mục cho Text widget rất phong phú và được mô tả rõ nhất trong các trang hướng dẫn của Tk.

Các chỉ mục menu (menu.invoke(), menu.entryconfig(), v.v.)
   Một số tùy chọn và phương thức dành cho menu thao tác với các mục menu cụ thể. Bất cứ khi nào cần một chỉ mục menu cho một tùy chọn hoặc tham số, bạn có thể truyền vào:

   * một số nguyên chỉ vị trí số của mục trong widget, được đếm từ trên xuống, bắt đầu từ 0;

   * chuỗi ``"active"``, chỉ vị trí menu hiện đang nằm dưới con trỏ;

   * chuỗi ``"last"`` chỉ mục menu cuối cùng;

   * một chuỗi gồm ``@`` theo sau là một số nguyên, như trong ``"@6"``, trong đó số nguyên được hiểu là tọa độ pixel y trong hệ tọa độ của menu;

   * chuỗi ``"none"``, cho biết hoàn toàn không có mục menu nào, thường được dùng với menu.activate() để hủy kích hoạt tất cả các mục, và cuối cùng,

   * một chuỗi văn bản được so khớp theo mẫu với nhãn của mục menu, được quét từ đầu menu đến cuối menu. Lưu ý rằng kiểu chỉ mục này được xét sau tất cả các kiểu khác, nghĩa là các kết quả khớp với các mục menu có nhãn ``last``, ``active`` hoặc ``none`` thay vào đó có thể được diễn giải là các literal nêu trên.


Hình ảnh
^^^^^^^^

Có thể tạo hình ảnh ở các định dạng khác nhau thông qua lớp con tương ứng của :class:`tkinter.Image`:

* :class:`BitmapImage` dành cho hình ảnh ở định dạng XBM.

* :class:`PhotoImage` dành cho hình ảnh ở các định dạng PGM, PPM, GIF và PNG. Định dạng sau được hỗ trợ kể từ Tk 8.6.

Mỗi loại hình ảnh đều được tạo thông qua tùy chọn ``file`` hoặc ``data`` (cũng có các tùy chọn khác).

.. versionchanged:: 3.13
   Đã thêm phương thức :class:`!PhotoImage` :meth:`!copy_replace` để sao chép một vùng từ hình ảnh này sang hình ảnh khác, có thể kèm theo phóng to pixel và/hoặc lấy mẫu con. Thêm tham số *from_coords* vào các phương thức :class:`!PhotoImage` :meth:`!copy`,
   :meth:`!zoom` và :meth:`!subsample`. Thêm các tham số *zoom* và *subsample* vào phương thức :class:`!PhotoImage`
   :meth:`!copy`.

Sau đó, đối tượng hình ảnh có thể được sử dụng ở bất kỳ nơi nào một widget hỗ trợ tùy chọn ``image`` (ví dụ: nhãn, nút, menu). Trong những trường hợp này, Tk sẽ không giữ tham chiếu đến hình ảnh. Khi tham chiếu Python cuối cùng đến đối tượng hình ảnh bị xóa, dữ liệu hình ảnh cũng bị xóa, và Tk sẽ hiển thị một ô trống ở mọi nơi hình ảnh từng được sử dụng.

.. seealso::

    Gói `Pillow <https://python-pillow.org/>`_ bổ sung hỗ trợ cho các định dạng như BMP, JPEG, TIFF và WebP, cùng nhiều định dạng khác.


Tham khảo
---------

.. currentmodule:: tkinter

Phần này mô tả các lớp, phương thức, hàm và hằng số của
:mod:`!tkinter` mô-đun. Hầu hết chúng bao bọc các lệnh Tcl/Tk; hãy tham khảo các trang hướng dẫn chính thức của Tcl/Tk để xem danh sách đầy đủ các tùy chọn của widget và biết thêm chi tiết.

.. exception:: TclError

   Ngoại lệ được phát sinh khi một lệnh gọi vào trình thông dịch Tcl thất bại, chẳng hạn khi một widget được cung cấp một tùy chọn không xác định hoặc một giá trị không hợp lệ.

Các lớp cơ sở và mixin
^^^^^^^^^^^^^^^^^^^^^^

.. class:: Misc()

   Lớp :class:`!Misc` là một mixin được :class:`Tk` kế thừa và, thông qua
   :class:`BaseWidget`, bởi mọi widget. Lớp này cung cấp tập hợp lớn các phương thức dùng chung cho tất cả đối tượng Tk: truy vấn thông tin cửa sổ, quản lý các liên kết sự kiện và event loop, điều khiển keyboard focus và pointer grab, truy cập selection, clipboard và option database, cùng nhiều dịch vụ tiện ích và introspection khác. Vì được kế thừa, các phương thức này khả dụng trên mọi widget và trên đối tượng ứng dụng :class:`Tk`, đồng thời được ghi lại một lần ở đây thay vì lặp lại cho từng widget.

   .. method:: cget(key)

      Trả về giá trị hiện tại của tùy chọn cấu hình có tên *key* cho widget này dưới dạng chuỗi. Biểu thức ``widget[key]`` tương đương và cũng có thể được sử dụng.

   .. method:: config(cnf=None, **kw)
      :no-typesetting:

   .. method:: configure(cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của widget. Khi không có đối số, trả về một dictionary ánh xạ mọi tên tùy chọn khả dụng tới một tuple mô tả tùy chọn đó (tên, tên tài nguyên X, lớp tài nguyên X, giá trị mặc định và giá trị hiện tại). Nếu cung cấp một tên tùy chọn duy nhất dưới dạng chuỗi, trả về tuple chỉ dành cho tùy chọn đó. Nếu cung cấp một hoặc nhiều keyword argument, hoặc truyền một dictionary dưới dạng *cnf*, đặt mỗi tùy chọn có tên thành giá trị tương ứng; biểu thức ``widget[key] = value`` đặt một tùy chọn duy nhất theo cách tương tự.

      :meth:`config` là bí danh của :meth:`!configure`.

   .. method:: keys()

      Trả về danh sách tên của tất cả tùy chọn cấu hình của widget này.

   .. method:: getboolean(s)

      Diễn giải chuỗi *s* dưới dạng một giá trị boolean của Tcl và trả về giá trị tương ứng
      :class:`bool`. Tcl chấp nhận các giá trị như ``'1'``, ``'0'``, ``'yes'``, ``'no'``, ``'true'`` và ``'false'``. Phát sinh :exc:`ValueError` nếu *s* không phải là một giá trị boolean hợp lệ.

   .. method:: getdouble(s)

      Diễn giải chuỗi *s* dưới dạng một số dấu phẩy động của Tcl và trả về dưới dạng một :class:`float`. Phát sinh :exc:`ValueError` nếu *s* không phải là một số hợp lệ.

      .. versionadded:: 3.5


   .. method:: getint(s)

      Diễn giải chuỗi *s* dưới dạng một số nguyên Tcl và trả về dưới dạng một
      :class:`int`. Phát sinh :exc:`ValueError` nếu *s* không phải là một số nguyên hợp lệ.

   .. method:: getvar(name)

      Trả về giá trị của biến toàn cục Tcl có tên *name*.

   .. method:: setvar(name, value)

      Đặt biến toàn cục Tcl có tên *name* thành *value*.

      Các phương thức :meth:`!getvar` và :meth:`!setvar` cho phép truy cập trực tiếp vào các biến Tcl. Trong hầu hết mã, thay vào đó bạn sẽ sử dụng một lớp con của :class:`Variable` chẳng hạn như
      :class:`StringVar` hoặc :class:`IntVar`, lớp này bao bọc một biến Tcl và chuyển đổi giá trị của biến này từ và sang một kiểu Python.

   .. method:: register(func, subst=None, needcleanup=1)

      Đăng ký callable Python *func* làm một lệnh Tcl và trả về tên của lệnh mới dưới dạng chuỗi. Mỗi khi Tcl gọi lệnh đó, *func* sẽ được gọi; nếu cung cấp *subst*, nó sẽ được áp dụng trước tiên cho các đối số của lệnh. Đây là cơ chế được sử dụng nội bộ để chuyển các callback Python thành tên lệnh được truyền cho các tùy chọn Tk như *command*. Trừ khi *needcleanup* là false, lệnh sẽ tự động bị xóa khi widget bị hủy.

      .. versionchanged:: 3.13
         Các đối số được truyền cho *func* không còn được chuyển đổi thành chuỗi.

   .. method:: deletecommand(name)

      Xóa lệnh Tcl có tên *name*, chẳng hạn như lệnh trước đó được trả về bởi
      :meth:`register`.

   .. method:: nametowidget(name)

      Trả về instance widget tương ứng với Tk pathname *name*.

   .. method:: send(interp, cmd, *args)

      Gửi lệnh Tcl *cmd*, cùng với *args* đã cho, đến trình thông dịch Tcl được đăng ký dưới tên *interp*, rồi trả về kết quả của lệnh. Tính năng này không khả dụng trên mọi nền tảng.

   .. method:: destroy()

      Hủy widget này cùng tất cả widget hậu duệ của nó, đồng thời xóa các lệnh Tcl liên kết với chúng.

   .. method:: lift(aboveThis=None)
      :no-typesetting:

   .. method:: tkraise(aboveThis=None)

      Đưa widget này lên trong thứ tự xếp chồng để nó được vẽ bên trên các widget cùng cấp. Nếu chỉ định *aboveThis*, widget sẽ được di chuyển đến ngay phía trên nó trong thứ tự xếp chồng.

      :meth:`lift` là bí danh của :meth:`!tkraise`.

   .. method:: lower(belowThis=None)

      Đưa widget này xuống trong thứ tự xếp chồng để nó được vẽ bên dưới các widget cùng cấp. Nếu chỉ định *belowThis*, widget sẽ được di chuyển đến ngay phía dưới nó trong thứ tự xếp chồng.

      :meth:`tkraise`/:meth:`lift` và :meth:`lower` bị ghi đè bởi
      widget :class:`Canvas`, trong đó chúng sẽ sắp xếp lại các mục canvas thay thế.

   .. method:: image_names()

      Trả về tên của tất cả hình ảnh hiện đang tồn tại trong trình thông dịch Tcl.

      Điều này bị widget :class:`Text` ghi đè, trong đó :meth:`!image_names` thay vào đó trả về tên của các hình ảnh được nhúng trong widget.

   .. method:: image_types()

      Trả về các loại hình ảnh hiện có, chẳng hạn như ``'photo'`` và ``'bitmap'``.

   .. method:: anchor(anchor=None)
      :no-typesetting:

   .. method:: grid_anchor(anchor=None)

      Đặt anchor kiểm soát vị trí đặt grid bên trong container này khi container lớn hơn grid và không có hàng hoặc cột nào có weight khác không. *anchor* là một trong các chuỗi anchor thông dụng, chẳng hạn như ``'nw'`` (mặc định) hoặc ``'center'``. Khi được gọi mà không có đối số, phương thức này không có tác dụng.

      :meth:`anchor` là bí danh của :meth:`!grid_anchor`.

      .. versionadded:: 3.3

   .. method:: bbox(column=None, row=None, col2=None, row2=None)
      :no-typesetting:

   .. method:: grid_bbox(column=None, row=None, col2=None, row2=None)

      Trả về bounding box, tính bằng pixel, của một vùng trong grid được bố trí trong container này, dưới dạng bộ 4 giá trị ``(xoffset, yoffset, width, height)``. Nếu không có đối số, bounding box của toàn bộ grid sẽ được trả về. Nếu *column* và *row* được cung cấp, hộp sẽ trải từ ô ở hàng và cột 0 đến ô đó; nếu *col2* và *row2* cũng được cung cấp, hộp sẽ trải từ ô (*column*, *row*) đến ô (*col2*, *row2*).

      :meth:`bbox` là bí danh của :meth:`!grid_bbox`, ngoại trừ trên :class:`Canvas`, :class:`Listbox`, :class:`Spinbox`,
      :class:`Text`, :class:`ttk.Entry <tkinter.ttk.Entry>` và
      :class:`ttk.Treeview <tkinter.ttk.Treeview>`, vốn cung cấp phương thức :meth:`!bbox` của riêng mình.

   .. method:: columnconfigure(index, cnf={}, **kw)
      :no-typesetting:

   .. method:: grid_columnconfigure(index, cnf={}, **kw)

      Truy vấn hoặc thiết lập các thuộc tính của cột (hoặc các cột) *index* trong lưới do container này quản lý. *index* có thể là số thứ tự của một cột; khi thiết lập các tùy chọn, giá trị này cũng có thể là danh sách số thứ tự cột, chuỗi ``'all'`` để áp dụng cho mọi cột hoặc một widget con có các cột mà nó chiếm giữ sẽ bị ảnh hưởng. Các tùy chọn được hỗ trợ là:

      *minsize*
         Kích thước tối thiểu của cột, tính bằng pixel.

      *weight*
         Một thiết lập số nguyên xác định phần không gian thừa được phân bổ cho cột là bao nhiêu. Trọng số ``0`` giữ cột ở kích thước được yêu cầu, còn cột có trọng số hai sẽ tăng nhanh gấp đôi cột có trọng số một.

      *uniform*
         Tên của một nhóm đồng nhất. Các cột có cùng tên nhóm không rỗng được giữ ở kích thước hoàn toàn tỷ lệ với trọng số của chúng.

      *pad*
         Khoảng trống bổ sung, tính bằng pixel, được thêm vào widget lớn nhất trong cột khi tính kích thước của cột.

      Với một tên tùy chọn duy nhất, trả về giá trị của tùy chọn đó; khi không có tùy chọn nào, trả về một dictionary chứa tất cả các tùy chọn.

      :meth:`columnconfigure` là bí danh của :meth:`!grid_columnconfigure`.

   .. method:: rowconfigure(index, cnf={}, **kw)
      :no-typesetting:

   .. method:: grid_rowconfigure(index, cnf={}, **kw)

      Truy vấn hoặc thiết lập các thuộc tính của hàng (hoặc các hàng) *index* trong grid do container này quản lý. *index* được diễn giải giống như đối với :meth:`grid_columnconfigure`, và các tùy chọn được hỗ trợ (*minsize*, *weight*, *uniform* và *pad*) cũng giống nhau, nhưng được áp dụng cho hàng thay vì cột.

      :meth:`rowconfigure` là bí danh của :meth:`!grid_rowconfigure`.

   .. method:: grid_location(x, y)

      Trả về ``(column, row)`` của ô lưới chứa pixel tại vị trí (*x*, *y*), được tính bằng pixel so với container này. Với các vị trí nằm phía trên hoặc bên trái lưới, ``-1`` được trả về cho tọa độ tương ứng.

   .. method:: grid_propagate()
               grid_propagate(flag)

      Bật hoặc tắt việc lan truyền hình học cho container này khi nó quản lý các widget con bằng grid geometry manager. Khi *flag* là true, container sẽ tự điều chỉnh kích thước để vừa với kích thước được yêu cầu của các widget con; khi là false, kích thước của nó do bạn kiểm soát. Khi được gọi mà không có đối số, trả về thiết lập hiện tại dưới dạng boolean.

   .. method:: size()
      :no-typesetting:

   .. method:: grid_size()

      Trả về kích thước của grid được container này quản lý dưới dạng một tuple ``(columns, rows)``.

      :meth:`size` là bí danh của :meth:`!grid_size`, ngoại trừ trên widget :class:`Listbox`, widget này cung cấp phương thức :meth:`!size` riêng.

   .. method:: grid_slaves(row=None, column=None)

      Trả về danh sách các widget con được quản lý trong grid của container này, theo thứ tự widget được quản lý gần đây nhất trước. Nếu cung cấp *row* hoặc *column*, chỉ trả về các widget con trong hàng hoặc cột đó.

   .. method:: propagate()
               propagate(flag)
      :no-typesetting:

   .. method:: pack_propagate()
               pack_propagate(flag)

      Bật hoặc tắt việc truyền kích thước cho vùng chứa này khi nó quản lý các widget con bằng trình quản lý hình học pack. Khi *flag* là true, vùng chứa sẽ tự thay đổi kích thước để vừa với kích thước được yêu cầu của các widget con; khi là false, kích thước của vùng chứa nằm dưới quyền kiểm soát của bạn. Khi được gọi không có đối số, trả về thiết lập hiện tại dưới dạng boolean.

      :meth:`propagate` là bí danh của :meth:`!pack_propagate`.

   .. method:: slaves()
      :no-typesetting:

   .. method:: pack_slaves()

      Trả về danh sách các widget con được vùng chứa này quản lý bằng trình quản lý hình học pack, theo thứ tự đóng gói.

      :meth:`slaves` là bí danh của :meth:`!pack_slaves`.

   .. method:: place_slaves()

      Trả về danh sách các widget con được vùng chứa này quản lý bằng trình quản lý hình học place.

   .. method:: bind(sequence=None, func=None, add=None)

      Liên kết mẫu sự kiện *sequence* trên widget này với hàm có thể gọi *func*.

      *sequence* là một mẫu sự kiện, chẳng hạn như ``'<Button-1>'`` (một lần nhấp chuột) hoặc ``'<KeyPress-a>'``, tùy chọn là phép nối của một số mẫu như vậy phải xảy ra liên tiếp trong thời gian ngắn. Khi sự kiện xảy ra, *func* được gọi với một thực thể :class:`Event` mô tả sự kiện đó làm đối số duy nhất; nếu *func* trả về chuỗi ``'break'``, không có binding nào khác cho sự kiện này được gọi.

      Nếu *add* là true, *func* sẽ được thêm vào các hàm đã liên kết với *sequence*; nếu không, nó sẽ thay thế các hàm đó. Binding này chỉ áp dụng cho widget này.

      :meth:`!bind` trả về một mã định danh dạng chuỗi (một *funcid*) mà sau đó có thể truyền vào :meth:`unbind` để xóa binding mà không làm rò rỉ lệnh Tcl liên quan.

      Nếu bỏ qua *func*, hãy trả về binding hiện được liên kết với *sequence*; nếu cũng bỏ qua *sequence*, hãy trả về danh sách tất cả các sequence có binding trên widget này.

   .. method:: bind_class(className, sequence=None, func=None, add=None)

      Tương tự :meth:`bind`, nhưng liên kết *func* với thẻ binding *className* thay vì với một widget duy nhất, để binding áp dụng cho mọi widget có thẻ đó. *className* thường là tên của một lớp widget, chẳng hạn như ``'Button'``, trong trường hợp đó binding ảnh hưởng đến mọi widget thuộc lớp đó. Có thể kiểm tra và thay đổi tập hợp các thẻ binding của một widget bằng
      :meth:`bindtags`.

      Các đối số còn lại và giá trị trả về giống như :meth:`bind`.

   .. method:: bind_all(sequence=None, func=None, add=None)

      Tương tự :meth:`bind`, nhưng liên kết *func* với thẻ binding đặc biệt ``'all'``, để binding áp dụng cho mọi widget trong ứng dụng.

      Các đối số còn lại và giá trị trả về giống như :meth:`bind`.

   .. method:: unbind(sequence, funcid=None)

      Xóa các binding cho mẫu sự kiện *sequence* trên widget này.

      Nếu *funcid* được cung cấp, chỉ hàm được xác định bởi nó (giá trị được trả về từ một lần gọi trước đó đến :meth:`bind`) bị xóa và lệnh Tcl liên kết với hàm đó cũng bị xóa. Nếu không, tất cả binding cho *sequence* sẽ bị hủy, khiến nó không còn binding.

      .. versionchanged:: 3.13
         Nếu *funcid* được cung cấp, chỉ callback đó bị hủy liên kết; các callback khác được liên kết với *sequence* vẫn được giữ lại.


   .. method:: unbind_class(className, sequence)

      Xóa tất cả binding cho mẫu sự kiện *sequence* khỏi thẻ binding *className*. Xem :meth:`bind_class`.

   .. method:: unbind_all(sequence)

      Xóa tất cả binding cho mẫu sự kiện *sequence* khỏi thẻ binding đặc biệt ``'all'``. Xem :meth:`bind_all`.

   .. method:: bindtags(tagList=None)

      Nếu *tagList* bị bỏ qua, trả về một tuple gồm các thẻ binding được liên kết với widget này. Khi một sự kiện xảy ra trong widget, sự kiện đó được áp dụng lần lượt cho từng thẻ binding của widget, và với mỗi thẻ, binding khớp cụ thể nhất sẽ được thực thi. Theo mặc định, một widget có bốn thẻ binding: pathname của chính nó, lớp widget, pathname của tổ tiên toplevel gần nhất và ``'all'``, theo thứ tự đó.

      Nếu *tagList* được cung cấp, nó phải là một chuỗi các string; các binding tag của widget được đặt thành các phần tử của chuỗi này, từ đó xác định thứ tự đánh giá các binding.

   Các phương thức có tiền tố ``event_`` xác định các sự kiện ảo và tạo sự kiện theo cách lập trình.

   .. method:: event_add(virtual, *sequences)

      Liên kết sự kiện ảo *virtual*, có tên theo dạng ``'<<Paste>>'``, với từng mẫu sự kiện vật lý được cung cấp bởi *sequences*, để sự kiện ảo được kích hoạt bất cứ khi nào một trong các mẫu đó xảy ra. Nếu *virtual* đã được định nghĩa, các sequence mới sẽ được thêm vào những sequence hiện có của nó.

   .. method:: event_delete(virtual, *sequences)

      Xóa từng *sequences* khỏi các sequence được liên kết với sự kiện ảo *virtual*. Các sequence hiện không được liên kết với *virtual* sẽ bị bỏ qua. Nếu không cung cấp *sequences*, tất cả sequence sự kiện vật lý sẽ bị xóa, khiến *virtual* không còn được kích hoạt.

   .. method:: event_generate(sequence, **kw)

      Tạo sự kiện *sequence* trên widget này và sắp xếp để sự kiện được xử lý giống như thể nó đến từ hệ thống cửa sổ. *sequence* phải là một mẫu sự kiện đơn, chẳng hạn như ``'<Button-1>'`` hoặc ``'<<Paste>>'``, không phải sự ghép nối của nhiều mẫu. Các đối số keyword chỉ định những trường bổ sung của sự kiện, chẳng hạn như *x* và *y* cho vị trí con trỏ, hoặc *when* để kiểm soát thời điểm xử lý sự kiện; hãy tham khảo trang hướng dẫn Tk ``event`` để biết danh sách đầy đủ.

   .. method:: event_info(virtual=None)

      Nếu bỏ qua *virtual*, trả về một tuple gồm tất cả sự kiện ảo hiện được định nghĩa. Nếu cung cấp *virtual*, trả về một tuple gồm các sequence sự kiện vật lý hiện được liên kết với nó, hoặc một tuple rỗng nếu nó chưa được định nghĩa.

   Các phương thức có tiền tố ``after`` lên lịch cho các callback chạy sau một khoảng trễ hoặc khi ứng dụng ở trạng thái idle.

   .. method:: after(ms, func=None, *args, **kw)

      Lên lịch để callable *func* được gọi sau *ms* mili giây, với *args* và *kw* được truyền cho nó dưới dạng đối số vị trí và đối số từ khóa. Trả về một định danh có thể được truyền cho :meth:`after_cancel` để hủy lần gọi này.

      Nếu bỏ qua *func*, thay vào đó sẽ tạm dừng trong *ms* mili giây, không xử lý sự kiện nào trong thời gian đó, và trả về ``None``.

      .. versionchanged:: 3.10
         Giờ đây, *func* có thể là bất kỳ đối tượng callable nào, không chỉ là một hàm.

      .. versionchanged:: 3.14
         Các đối số từ khóa giờ đây được truyền cho *func*.


   .. method:: after_cancel(id)

      Hủy một callback đã được lên lịch trước đó bằng :meth:`after` hoặc
      :meth:`after_idle`. *id* phải là một định danh được một trong các phương thức đó trả về; truyền một giá trị không phải là định danh như vậy sẽ gây ra :exc:`ValueError`. Nếu callback đã chạy hoặc đã bị hủy, thao tác này không có hiệu lực.

      .. versionchanged:: 3.7
         Việc truyền ``None`` (hoặc bất kỳ giá trị false nào) làm *id* giờ đây sẽ gây ra
         :exc:`ValueError`.


   .. method:: after_idle(func, *args, **kw)

      Lập lịch để callable *func* được gọi, với *args* và *kw* được truyền cho nó, khi vòng lặp chính của Tk chuyển sang trạng thái nhàn rỗi lần tiếp theo, tức là khi không còn sự kiện nào khác cần xử lý. Trả về một mã định danh có thể truyền cho :meth:`after_cancel` để hủy lệnh gọi này.

      .. versionchanged:: 3.14
         Các đối số từ khóa giờ đây được truyền cho *func*.


   .. method:: after_info(id=None)

      Nếu bỏ qua *id*, trả về một tuple chứa mã định danh của tất cả callback hiện đang được lập lịch bằng :meth:`after` và :meth:`after_idle` cho trình thông dịch này.

      Nếu cung cấp *id*, mã này phải xác định một callback chưa được chạy hoặc hủy, và giá trị trả về là một tuple ``(script, type)``, trong đó *script* tham chiếu đến hàm sẽ được gọi còn *type* là ``'idle'`` hoặc ``'timer'``. Một :exc:`TclError` sẽ được phát sinh nếu *id* không tồn tại.

      .. versionadded:: 3.13


   .. method:: mainloop(n=0)

      Đi vào vòng lặp sự kiện Tk, vòng lặp này xử lý các sự kiện cho đến khi tất cả cửa sổ bị hủy. Thông thường, thao tác này được gọi một lần trên cửa sổ gốc để chạy ứng dụng.

   .. method:: quit()

      Thoát khỏi trình thông dịch Tcl, khiến :meth:`mainloop` trả về.

   .. method:: update()

      Đi vào vòng lặp sự kiện cho đến khi tất cả sự kiện đang chờ, bao gồm cả idle callback, được xử lý. Thao tác này cập nhật màn hình và xử lý mọi sự kiện đã được xếp hàng, sau đó trả về.

   .. method:: update_idletasks()

      Đi vào event loop cho đến khi tất cả các idle callback đang chờ được gọi. Thao tác này cập nhật hiển thị của các cửa sổ, chẳng hạn sau khi thay đổi hình học, nhưng không xử lý các sự kiện do người dùng gây ra.

   .. method:: waitvar(name)
      :no-typesetting:

   .. method:: wait_variable(name)

      Chờ cho đến khi biến Tcl *name* được sửa đổi, đồng thời tiếp tục xử lý các sự kiện để ứng dụng vẫn phản hồi. *name* thường là một :class:`Variable` instance, chẳng hạn như một
      :class:`IntVar` hoặc :class:`StringVar`.

      :meth:`waitvar` là bí danh của :meth:`!wait_variable`.

   .. method:: wait_window(window=None)

      Chờ cho đến khi *window* bị hủy, đồng thời tiếp tục xử lý các sự kiện. Nếu bỏ qua *window*, widget này sẽ được sử dụng. Cách này thường được dùng để chờ người dùng hoàn tất thao tác với một hộp thoại.

   .. method:: wait_visibility(window=None)

      Chờ cho đến khi trạng thái hiển thị của *window* thay đổi, chẳng hạn khi cửa sổ xuất hiện lần đầu trên màn hình, đồng thời tiếp tục xử lý các sự kiện. Nếu bỏ qua *window*, widget này sẽ được sử dụng. Cách này thường được dùng để chờ một cửa sổ mới tạo trở nên hiển thị trước khi thao tác với cửa sổ đó.

   Các phương thức có tiền tố ``focus_`` quản lý keyboard focus.

   .. method:: focus_set()
      :no-typesetting:

   .. method:: focus()

      Chuyển tiêu điểm nhập liệu bàn phím cho phần hiển thị của widget này sang widget này. Nếu ứng dụng hiện không có tiêu điểm nhập liệu trên phần hiển thị của widget này, widget sẽ được ghi nhớ là cửa sổ tiêu điểm cho top level của nó, và tiêu điểm sẽ được chuyển hướng đến widget đó vào lần tiếp theo trình quản lý cửa sổ cấp tiêu điểm cho top level.
      :meth:`focus` là bí danh của :meth:`!focus_set`, ngoại trừ trên :class:`Canvas` và
      các widget :class:`ttk.Treeview <tkinter.ttk.Treeview>`, vốn cung cấp phương thức :meth:`!focus` riêng.

   .. method:: focus_force()

      Chuyển tiêu điểm nhập liệu bàn phím đến widget này ngay cả khi ứng dụng hiện không có tiêu điểm nhập liệu trên phần hiển thị của widget. Nên hạn chế sử dụng phương thức này, nếu có thể thì không sử dụng; thông thường, ứng dụng nên chờ trình quản lý cửa sổ cấp tiêu điểm cho mình thay vì tự giành tiêu điểm.

   .. method:: focus_get()

      Trả về widget hiện đang có tiêu điểm bàn phím trong ứng dụng, hoặc ``None`` nếu không có widget nào trong ứng dụng có tiêu điểm. Sử dụng :meth:`focus_displayof` để hoạt động chính xác với nhiều phần hiển thị.

   .. method:: focus_displayof()

      Trả về widget hiện đang có tiêu điểm bàn phím trên phần hiển thị nơi widget này nằm, hoặc ``None`` nếu không có widget nào trong ứng dụng có tiêu điểm trên phần hiển thị đó.

   .. method:: focus_lastfor()

      Trả về widget gần đây nhất từng có tiêu điểm bàn phím trong số tất cả widget thuộc cùng top level với widget này; đây là widget sẽ nhận tiêu điểm vào lần tiếp theo trình quản lý cửa sổ cấp tiêu điểm cho top level. Nếu chưa từng có widget nào trong top level đó có tiêu điểm, hoặc widget có tiêu điểm gần đây nhất đã bị xóa, thì chính top level được trả về.

   .. method:: tk_focusFollowsMouse()

      Cấu hình lại Tk để sử dụng mô hình focus ngầm, trong đó focus được đặt vào một widget mỗi khi con trỏ chuột đi vào widget đó. Không dễ tắt tính năng này sau khi đã bật.

   .. method:: tk_focusNext()

      Trả về widget tiếp theo sau widget này trong thứ tự duyệt bằng bàn phím, hoặc ``None`` nếu không có. Thứ tự duyệt trước tiên đi đến widget con tiếp theo, sau đó đệ quy qua các widget con của widget đó, rồi đến widget anh em tiếp theo ở vị trí cao hơn trong thứ tự xếp chồng. Một widget sẽ bị bỏ qua nếu tùy chọn ``takefocus`` của nó được đặt thành ``0``. Phương thức này được sử dụng trong các binding mặc định cho phím :kbd:`Tab`.

   .. method:: tk_focusPrev()

      Trả về widget trước widget này trong thứ tự duyệt bằng bàn phím, hoặc ``None`` nếu không có. Xem :meth:`tk_focusNext` để biết cách xác định thứ tự. Phương thức này được sử dụng trong các binding mặc định cho phím :kbd:`Shift-Tab`.

   Các phương thức có tiền tố ``grab_`` thiết lập và truy vấn input grab, chức năng chuyển hướng tất cả sự kiện đầu vào đến một widget duy nhất.

   .. method:: grab_set()

      Thiết lập local grab trên widget này. Grab giới hạn các sự kiện con trỏ trong widget này và các widget con của nó: khi con trỏ nằm ngoài cây con của widget, các thao tác nhấn và nhả nút cùng chuyển động của con trỏ sẽ được báo cáo cho grab widget, còn các cửa sổ bên ngoài cây con sẽ trở nên không tương tác cho đến khi grab được giải phóng. Local grab chỉ ảnh hưởng đến ứng dụng đang grab. Mọi grab trước đó do ứng dụng này thiết lập trên display của widget sẽ tự động được giải phóng. Thiết lập grab là cách thông thường để biến một hộp thoại thành modal: trong khi grab có hiệu lực, người dùng không thể tương tác với các cửa sổ khác của ứng dụng.

   .. method:: grab_set_global()

      Thiết lập global grab trên widget này. Global grab tương tự local grab được thiết lập bởi :meth:`grab_set`, nhưng khóa tất cả ứng dụng khác trên màn hình, כך chỉ cây con của widget này mới nhận được sự kiện con trỏ, đồng thời nó cũng grab bàn phím. Hãy thận trọng khi sử dụng: global grab có thể dễ dàng khiến display không thể sử dụng được, vì các ứng dụng khác sẽ ngừng nhận sự kiện cho đến khi grab được giải phóng.

   .. method:: grab_release()

      Giải phóng grab trên widget này nếu có; nếu không thì không thực hiện gì.

   .. method:: grab_current()

      Trả về widget hiện đang giữ grab trong ứng dụng này trên display của widget này, hoặc ``None`` nếu không có widget nào như vậy.

   .. method:: grab_status()

      Trả về ``None`` nếu hiện không đặt grab nào trên widget này, ``"local"`` nếu đặt grab cục bộ, hoặc ``"global"`` nếu đặt grab toàn cục.

   Các phương thức có tiền tố ``selection_`` dùng để truy xuất và quản lý X selection.

   .. method:: selection_clear(**kw)

      Xóa X selection để không còn cửa sổ nào sở hữu nó. Selection cần xóa được chỉ định bằng đối số từ khóa *selection*, là một tên atom chẳng hạn như ``'PRIMARY'`` hoặc ``'CLIPBOARD'``; mặc định là ``PRIMARY``. Đối số từ khóa *displayof* chỉ định một widget dùng để xác định display cần thao tác, và mặc định là widget này.

      Điều này được ghi đè bởi các widget :class:`Entry`, :class:`Listbox` và
      :class:`Spinbox`, trong đó :meth:`!selection_clear` thay vào đó sẽ xóa selection riêng của widget.

   .. method:: selection_get(**kw)

      Trả về nội dung của X selection hiện tại. Đối số từ khóa *selection* chỉ định selection và mặc định là ``PRIMARY``. Đối số từ khóa *type* chỉ định dạng mà dữ liệu sẽ được trả về (đích chuyển đổi mong muốn), là một tên atom chẳng hạn như ``'STRING'`` hoặc ``'FILE_NAME'``; mặc định là ``STRING``, ngoại trừ trên X11, nơi ``UTF8_STRING`` được thử trước và ``STRING`` được dùng làm phương án dự phòng. Đối số từ khóa *displayof* chỉ định một widget dùng để xác định display cần truy xuất selection, và mặc định là widget này.

   .. method:: selection_handle(command, **kw)

      Đăng ký *command* làm handler để cung cấp vùng chọn X do widget này sở hữu khi một ứng dụng khác yêu cầu. Khi vùng chọn được truy xuất, *command* được gọi với hai đối số: offset ký tự bắt đầu và số ký tự tối đa cần trả về; hàm này phải trả về nhiều nhất số ký tự đó của vùng chọn, bắt đầu từ offset đó. Với các vùng chọn rất dài, hàm sẽ được gọi lặp lại với các offset tăng dần. Đối số từ khóa *selection* chỉ định vùng chọn (mặc định là ``PRIMARY``), còn đối số từ khóa *type* chỉ định dạng vùng chọn mà handler cung cấp (chẳng hạn như ``'STRING'`` hoặc ``'FILE_NAME'``, mặc định là ``STRING``).

   .. method:: selection_own(**kw)

      Đặt widget này làm chủ sở hữu vùng chọn X trên display của nó. Chủ sở hữu trước đó, nếu có, sẽ được thông báo rằng vùng chọn đã bị mất. Đối số từ khóa *selection* chỉ định vùng chọn và mặc định là ``PRIMARY``.

   .. method:: selection_own_get(**kw)

      Trả về widget trong ứng dụng này đang sở hữu vùng chọn X trên display chứa widget này, hoặc ``None`` nếu không có widget nào trong ứng dụng này sở hữu vùng chọn. Đối số từ khóa *selection* chỉ định vùng chọn và mặc định là ``PRIMARY``. Đối số từ khóa *displayof* chỉ định một widget dùng để xác định display cần truy vấn và mặc định là widget này.

   Các phương thức có tiền tố ``clipboard_`` dùng để quản lý clipboard.

   .. method:: clipboard_append(string, **kw)

      Nối *string* vào clipboard Tk và giành quyền sở hữu clipboard trên display của widget này. Trước khi nối, cần làm trống clipboard bằng
      :meth:`clipboard_clear`; mọi thao tác nối phải được hoàn tất trước khi quay lại event loop để clipboard được cập nhật nguyên tử. Đối số từ khóa *type* chỉ định dạng dữ liệu, là một tên atom như ``'STRING'`` hoặc ``'FILE_NAME'`` (mặc định là ``STRING``), còn đối số từ khóa *format* chỉ định cách biểu diễn dùng để truyền dữ liệu (mặc định là ``STRING``). Đối số từ khóa *displayof* chỉ định một widget dùng để xác định display đích và mặc định là widget này. Có thể truy xuất nội dung bằng :meth:`clipboard_get` hoặc
      :meth:`selection_get`.

   .. method:: clipboard_clear(**kw)

      Giành quyền sở hữu clipboard trên display của widget này và xóa mọi nội dung trước đó. Đối số từ khóa *displayof* chỉ định một widget dùng để xác định display đích và mặc định là widget này.

   .. method:: clipboard_get(**kw)

      Lấy dữ liệu từ clipboard trên display của widget này. Đối số từ khóa *type* chỉ định dạng mà dữ liệu sẽ được trả về, một tên atom chẳng hạn như ``'STRING'`` hoặc ``'FILE_NAME'``; mặc định là ``STRING``, ngoại trừ trên X11, nơi ``UTF8_STRING`` được thử trước và ``STRING`` được dùng làm phương án dự phòng. Đối số từ khóa *displayof* chỉ định tên một widget xác định display và mặc định là cửa sổ gốc của ứng dụng. Tương đương với ``selection_get(selection='CLIPBOARD')``.

   Các phương thức có tiền tố ``option_`` sẽ truy vấn và sửa đổi cơ sở dữ liệu tùy chọn Tk.

   .. method:: option_add(pattern, value, priority=None)

      Thêm một tùy chọn vào cơ sở dữ liệu tùy chọn Tk, liên kết *value* với *pattern*. *pattern* bao gồm các tên và/hoặc lớp được phân tách bằng dấu hoa thị hoặc dấu chấm, theo định dạng X thông thường. *priority* là một số nguyên từ 0 đến 100 hoặc một trong các tên ký hiệu ``'widgetDefault'`` (20), ``'startupFile'`` (40), ``'userDefault'`` (60) hoặc ``'interactive'`` (80); mặc định là ``interactive``.

   .. method:: option_clear()

      Xóa cơ sở dữ liệu tùy chọn Tk. Các tùy chọn mặc định từ thuộc tính :envvar:`!RESOURCE_MANAGER` hoặc
      tệp :file:`.Xdefaults` sẽ được tự động tải lại vào lần tiếp theo một tùy chọn được thêm vào hoặc xóa khỏi cơ sở dữ liệu.

   .. method:: option_get(name, className)

      Trả về giá trị của tùy chọn khớp với widget này theo *name* và *className* từ cơ sở dữ liệu tùy chọn Tk, hoặc một chuỗi rỗng nếu không có mục nhập nào khớp. Khi có nhiều mục nhập khớp, mục có độ ưu tiên cao nhất sẽ được trả về; trong số các mục nhập có cùng độ ưu tiên, mục được thêm gần đây nhất sẽ được trả về.

   .. method:: option_readfile(fileName, priority=None)

      Đọc tệp có tên *fileName*, tệp này phải có định dạng chuẩn của cơ sở dữ liệu tài nguyên X chẳng hạn như :file:`.Xdefaults`, rồi thêm tất cả các tùy chọn mà tệp chỉ định vào cơ sở dữ liệu tùy chọn Tk. *priority* được diễn giải giống như đối với :meth:`option_add` và mặc định là ``interactive``.

   .. method:: bell(displayof=0)

      Rung chuông trên màn hình hiển thị của widget này bằng các thiết lập liên quan đến chuông hiện tại của màn hình, đồng thời đặt lại trình bảo vệ màn hình. Nếu *displayof* được cung cấp dưới dạng một widget, chuông sẽ được rung trên màn hình hiển thị của widget đó.

   .. method:: tk_setPalette(background, /)
               tk_setPalette(*args, **kw)

      Đặt một bảng màu mới cho tất cả phần tử widget Tk. Các widget hiện có được cập nhật và option database được thay đổi để các widget tạo sau này sử dụng màu mới. Nếu chỉ cung cấp một đối số màu, màu đó được dùng làm màu nền thông thường, từ đó tính toán một bảng màu hoàn chỉnh. Ngoài ra, có thể cung cấp các đối số dưới dạng các cặp từ khóa *name*/*value*, trong đó chỉ định tên của từng tùy chọn trong option database. Các tên tùy chọn được nhận dạng là ``activeBackground``, ``activeForeground``, ``background``, ``disabledForeground``, ``foreground``, ``highlightBackground``, ``highlightColor``, ``insertBackground``, ``selectColor``, ``selectBackground``, ``selectForeground`` và ``troughColor``; các giá trị mặc định hợp lý sẽ được tính cho những tùy chọn chưa được chỉ định.

   .. method:: tk_bisque()

      Khôi phục màu của ứng dụng về bảng màu nâu nhạt (bisque) được sử dụng trong Tk 3.6 và các phiên bản trước đó. Được cung cấp để đảm bảo khả năng tương thích ngược.

   .. method:: tk_strictMotif(boolean=None)

      Truy vấn hoặc đặt tùy chọn giao diện của Tk có phải tuân thủ nghiêm ngặt Motif hay không. Giá trị *boolean* true bật chế độ tuân thủ Motif nghiêm ngặt (ví dụ: không đổi màu khi chuột di chuyển qua thanh trượt). Trả về thiết lập kết quả.

   Các phương thức có tiền tố ``busy_`` quản lý trạng thái bận của một cửa sổ; trạng thái này hiển thị con trỏ bận và bỏ qua dữ liệu nhập của người dùng.

   .. method:: busy(**kw)
      :no-typesetting:

   .. method:: busy_hold(**kw)
      :no-typesetting:

   .. method:: tk_busy(**kw)
      :no-typesetting:

   .. method:: tk_busy_hold(**kw)

      Làm cho widget này hiển thị trạng thái bận. Một cửa sổ trong suốt được đặt phía trước widget, khiến widget đó và tất cả hậu duệ của nó trong hệ thống phân cấp widget bị chặn các sự kiện con trỏ và hiển thị con trỏ bận. Thông thường, cần gọi :meth:`update` ngay sau đó để đảm bảo thao tác giữ có hiệu lực trước khi ứng dụng bắt đầu xử lý.

      Tùy chọn cấu hình duy nhất được hỗ trợ là *cursor*, con trỏ sẽ được hiển thị khi widget đang bận; tùy chọn này có thể nhận bất kỳ giá trị nào được :meth:`!configure` chấp nhận.

      :meth:`busy_hold`, :meth:`busy` và :meth:`tk_busy` là bí danh của
      :meth:`!tk_busy_hold`.

      .. versionadded:: 3.13


   .. method:: busy_configure(cnf=None, **kw)
      :no-typesetting:

   .. method:: busy_config(cnf=None, **kw)
      :no-typesetting:

   .. method:: tk_busy_config(cnf=None, **kw)
      :no-typesetting:

   .. method:: tk_busy_configure(cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của cửa sổ bận. Widget phải trước đó đã được chuyển sang trạng thái bận bằng :meth:`tk_busy_hold`. Khi không có đối số, trả về một dictionary mô tả tất cả các tùy chọn hiện có; nếu *cnf* là tên của một tùy chọn, trả về một tuple mô tả tùy chọn đó. Nếu không, đặt các tùy chọn đã cho thành các giá trị đã cho. Các tùy chọn có thể nhận bất kỳ giá trị nào được :meth:`tk_busy_hold` chấp nhận.

      Cơ sở dữ liệu tùy chọn được tham chiếu thông qua tên hoặc class của widget. Ví dụ: nếu một widget :class:`Frame` có tên là ``frame`` cần được chuyển sang trạng thái bận, con trỏ bận có thể được chỉ định cho widget đó bằng một trong hai lệnh gọi sau::

         w.option_add('*frame.busyCursor', 'gumby')
         w.option_add('*Frame.BusyCursor', 'gumby')

      :meth:`busy_configure`, :meth:`busy_config` và :meth:`tk_busy_config` là bí danh của :meth:`!tk_busy_configure`.

      .. versionadded:: 3.13


   .. method:: busy_cget(option)
      :no-typesetting:

   .. method:: tk_busy_cget(option)

      Trả về giá trị hiện tại của tùy chọn cấu hình bận *option*. Widget phải trước đó đã được chuyển sang trạng thái bận bằng :meth:`tk_busy_hold`, và *option* có thể nhận bất kỳ giá trị nào được phương thức đó chấp nhận.

      :meth:`busy_cget` là bí danh của :meth:`!tk_busy_cget`.

      .. versionadded:: 3.13


   .. method:: busy_forget()
      :no-typesetting:

   .. method:: tk_busy_forget()

      Đặt widget về trạng thái không còn bận, giải phóng các tài nguyên (bao gồm cả cửa sổ trong suốt) được cấp phát khi widget được đặt ở trạng thái bận. Widget sẽ lại nhận được các sự kiện của người dùng. Các tài nguyên này cũng được giải phóng khi widget bị hủy.

      :meth:`busy_forget` là bí danh của :meth:`!tk_busy_forget`.

      .. versionadded:: 3.13


   .. method:: busy_status()
      :no-typesetting:

   .. method:: tk_busy_status()

      Trả về ``True`` nếu widget hiện đang bận, nếu không thì trả về ``False``.

      :meth:`busy_status` là bí danh của :meth:`!tk_busy_status`.

      .. versionadded:: 3.13


   .. method:: busy_current(pattern=None)
      :no-typesetting:

   .. method:: tk_busy_current(pattern=None)

      Trả về danh sách các widget hiện đang bận. Nếu cung cấp *pattern*, chỉ các widget bận có tên đường dẫn khớp với mẫu mới được trả về.

      :meth:`busy_current` là bí danh của :meth:`!tk_busy_current`.

      .. versionadded:: 3.13

   Các phương thức có tiền tố ``winfo_`` dùng để truy xuất thông tin về các cửa sổ do Tk quản lý.

   .. method:: winfo_atom(name, displayof=0)

      Trả về mã định danh số nguyên của atom có tên là *name*, đồng thời tạo atom mới nếu chưa tồn tại. Nếu được cung cấp *displayof*, atom sẽ được tra cứu trên display của cửa sổ đó; nếu không, nó sẽ được tra cứu trên display của cửa sổ chính của ứng dụng.

   .. method:: winfo_atomname(id, displayof=0)

      Trả về tên dạng văn bản của atom có mã định danh số nguyên là *id*. Đây là phép đảo của :meth:`winfo_atom`. Nếu được cung cấp *displayof*, mã định danh sẽ được tra cứu trên display của cửa sổ đó; nếu không, nó sẽ được tra cứu trên display của cửa sổ chính của ứng dụng.

   .. method:: winfo_cells()

      Trả về số ô trong colormap của widget.

   .. method:: winfo_children()

      Trả về danh sách chứa các widget là con của widget này, theo thứ tự xếp chồng từ thấp đến cao. Các cửa sổ Toplevel được trả về dưới dạng con của các phần tử cha logic của chúng.

   .. method:: winfo_class()

      Trả về tên lớp của widget.

   .. method:: winfo_colormapfull()

      Trả về ``True`` nếu colormap của widget được biết là đã đầy, nếu không thì trả về ``False``.

   .. method:: winfo_containing(rootX, rootY, displayof=0)

      Trả về widget chứa điểm được xác định bởi *rootX* và *rootY*, hoặc ``None`` nếu không có cửa sổ nào trong ứng dụng này chứa điểm đó. Tọa độ được tính theo đơn vị màn hình trong hệ tọa độ của cửa sổ gốc. Nếu được cung cấp *displayof*, tọa độ tham chiếu đến màn hình chứa cửa sổ đó; nếu không, chúng tham chiếu đến màn hình của cửa sổ chính của ứng dụng.

   .. method:: winfo_depth()

      Trả về độ sâu của widget, tức là số bit trên mỗi pixel.

   .. method:: winfo_exists()

      Trả về true nếu widget tồn tại, false nếu không.

   .. method:: winfo_fpixels(number)

      Trả về một giá trị dấu phẩy động cho biết số pixel trong widget tương ứng với khoảng cách màn hình *number* (ví dụ: ``"2.0c"`` hoặc ``"1i"``). Kết quả có thể là số lẻ; để lấy giá trị số nguyên đã làm tròn, hãy sử dụng
      :meth:`winfo_pixels`.

   .. method:: winfo_geometry()

      Trả về hình học của widget dưới dạng ``widthxheight+x+y``. Tất cả các kích thước đều tính bằng pixel. Một độ lệch có thể là số âm; xem :meth:`~Wm.geometry`.

   .. method:: winfo_height()

      Trả về chiều cao của widget tính bằng pixel. Khi một cửa sổ được tạo lần đầu, chiều cao của nó là 1 pixel; sau đó sẽ được trình quản lý hình học thay đổi. Xem thêm :meth:`winfo_reqheight`.

   .. method:: winfo_id()

      Trả về mã định danh cấp thấp, đặc thù cho nền tảng của widget. Trên Unix, đây là mã định danh cửa sổ X; còn trên Windows, đây là window handle.

   .. method:: winfo_interps(displayof=0)

      Trả về một tuple chứa tên của tất cả các trình thông dịch Tcl hiện đang được đăng ký cho một display cụ thể. Nếu cung cấp *displayof*, giá trị trả về tham chiếu đến display của cửa sổ đó; nếu không, nó tham chiếu đến display của cửa sổ chính của ứng dụng.

   .. method:: winfo_ismapped()

      Trả về true nếu widget hiện đang được ánh xạ, nếu không thì trả về false.

   .. method:: winfo_manager()

      Trả về tên của geometry manager hiện chịu trách nhiệm cho widget, hoặc một chuỗi rỗng nếu widget không được geometry manager nào quản lý.

   .. method:: winfo_name()

      Trả về tên của widget trong parent của nó, thay vì tên đường dẫn đầy đủ của widget.

   .. method:: winfo_parent()

      Trả về tên đường dẫn của parent của widget, hoặc một chuỗi rỗng nếu widget là cửa sổ chính của ứng dụng.

   .. method:: winfo_pathname(id, displayof=0)

      Trả về tên đường dẫn của cửa sổ có mã định danh là *id*. Nếu *displayof* được chỉ định, mã định danh sẽ được tra cứu trên display của cửa sổ đó; nếu không, mã định danh sẽ được tra cứu trên display của cửa sổ chính của ứng dụng.

   .. method:: winfo_pixels(number)

      Trả về số pixel trong widget tương ứng với khoảng cách trên màn hình *number* (ví dụ: ``"2.0c"`` hoặc ``"1i"``). Kết quả được làm tròn đến số nguyên gần nhất; để sử dụng kết quả dạng phân số, hãy dùng
      :meth:`winfo_fpixels`.

   .. method:: winfo_pointerx()

      Trả về tọa độ *x* của con trỏ, tính bằng pixel và tương đối so với cửa sổ gốc của màn hình (hoặc root ảo, nếu đang được sử dụng). Trả về ``-1`` nếu con trỏ không nằm trên cùng màn hình với widget.

   .. method:: winfo_pointerxy()

      Trả về tọa độ của con trỏ dưới dạng một ``(x, y)`` tuple, tính bằng pixel, tương đối so với cửa sổ gốc của màn hình (hoặc cửa sổ gốc ảo nếu đang được sử dụng). Cả hai tọa độ đều là ``-1`` nếu con trỏ không nằm trên cùng màn hình với widget.

   .. method:: winfo_pointery()

      Trả về tọa độ *y* của con trỏ, tính bằng pixel, tương đối so với cửa sổ gốc của màn hình (hoặc cửa sổ gốc ảo nếu đang được sử dụng). Trả về ``-1`` nếu con trỏ không nằm trên cùng màn hình với widget.

   .. method:: winfo_reqheight()

      Trả về chiều cao được yêu cầu của widget, tính bằng pixel. Đây là giá trị được geometry manager của widget sử dụng để tính toán geometry của nó.

   .. method:: winfo_reqwidth()

      Trả về chiều rộng được yêu cầu của widget, tính bằng pixel. Đây là giá trị được geometry manager của widget sử dụng để tính toán geometry của nó.

   .. method:: winfo_rgb(color)

      Trả về một tuple ``(r, g, b)`` gồm cường độ màu đỏ, xanh lá và xanh dương, trong phạm vi từ 0 đến 65535, tương ứng với *color* trong widget. *color* có thể được chỉ định dưới bất kỳ dạng nào được chấp nhận cho một tùy chọn màu.

   .. method:: winfo_rootx()

      Trả về tọa độ *x*, trong cửa sổ gốc của màn hình, của góc trên bên trái của đường viền widget (hoặc của chính widget nếu widget không có đường viền).

   .. method:: winfo_rooty()

      Trả về tọa độ *y*, trong cửa sổ gốc của màn hình, của góc trên bên trái của đường viền widget (hoặc của chính widget nếu widget không có đường viền).

   .. method:: winfo_screen()

      Trả về tên của màn hình được liên kết với widget, theo dạng ``displayName.screenIndex``.

   .. method:: winfo_screencells()

      Trả về số ô trong colormap mặc định của màn hình của widget.

   .. method:: winfo_screendepth()

      Trả về độ sâu của cửa sổ gốc của màn hình của widget, tức là số bit trên mỗi pixel.

   .. method:: winfo_screenheight()

      Trả về chiều cao tính bằng pixel của màn hình của widget.

   .. method:: winfo_screenmmheight()

      Trả về chiều cao tính bằng milimét của màn hình của widget.

   .. method:: winfo_screenmmwidth()

      Trả về chiều rộng tính bằng milimét của màn hình của widget.

   .. method:: winfo_screenvisual()

      Trả về lớp visual mặc định của màn hình của widget, một trong các lớp ``"directcolor"``, ``"grayscale"``, ``"pseudocolor"``, ``"staticcolor"``, ``"staticgray"`` hoặc ``"truecolor"``.

   .. method:: winfo_screenwidth()

      Trả về chiều rộng của màn hình của widget tính bằng pixel.

   .. method:: winfo_server()

      Trả về một chuỗi chứa thông tin về máy chủ cho phần hiển thị của widget. Định dạng chính xác của chuỗi này có thể khác nhau tùy theo nền tảng.

   .. method:: winfo_toplevel()

      Trả về cửa sổ ở cấp cao nhất trong hệ thống phân cấp chứa widget. Trong Tk chuẩn, đây luôn là một widget :class:`Toplevel`.

   .. method:: winfo_viewable()

      Trả về true nếu widget và tất cả các ancestor của nó cho đến cửa sổ toplevel gần nhất đều được ánh xạ, ngược lại trả về false.

   .. method:: winfo_visual()

      Trả về visual class của widget, là một trong ``"directcolor"``, ``"grayscale"``, ``"pseudocolor"``, ``"staticcolor"``, ``"staticgray"`` hoặc ``"truecolor"``.

   .. method:: winfo_visualid()

      Trả về mã định danh X cho visual của widget.

   .. method:: winfo_visualsavailable(includeids=False)

      Trả về danh sách mô tả các visual khả dụng cho màn hình của widget. Mỗi mục bao gồm một visual class (xem :meth:`winfo_visual`) theo sau là một độ sâu dạng số nguyên. Nếu *includeids* là true, mã định danh X của visual cũng được bao gồm.

   .. method:: winfo_vrootheight()

      Trả về chiều cao của cửa sổ gốc ảo được liên kết với widget nếu có; nếu không, trả về chiều cao màn hình của widget.

   .. method:: winfo_vrootwidth()

      Trả về chiều rộng của cửa sổ gốc ảo được liên kết với widget nếu có; nếu không, trả về chiều rộng màn hình của widget.

   .. method:: winfo_vrootx()

      Trả về độ lệch *x* của cửa sổ gốc ảo được liên kết với widget, tính tương đối so với cửa sổ gốc của màn hình chứa nó. Giá trị này thường bằng không hoặc âm, và bằng ``0`` nếu không có cửa sổ gốc ảo.

   .. method:: winfo_vrooty()

      Trả về độ lệch *y* của cửa sổ gốc ảo được liên kết với widget, tính tương đối so với cửa sổ gốc của màn hình chứa nó. Giá trị này thường bằng không hoặc âm, và bằng ``0`` nếu không có cửa sổ gốc ảo.

   .. method:: winfo_width()

      Trả về chiều rộng của widget tính bằng pixel. Khi một cửa sổ được tạo lần đầu, chiều rộng của nó là 1 pixel; sau đó chiều rộng này sẽ được geometry manager thay đổi. Xem thêm :meth:`winfo_reqwidth`.

   .. method:: winfo_x()

      Trả về tọa độ *x*, trong widget cha của widget, của góc trên bên trái đường viền widget (hoặc của chính widget nếu nó không có đường viền).

   .. method:: winfo_y()

      Trả về tọa độ *y*, trong widget cha của widget, của góc trên bên trái đường viền widget (hoặc của chính widget nếu nó không có đường viền).

   .. method:: info_patchlevel()

      Trả về cấp bản vá Tcl/Tk dưới dạng một named tuple với cùng năm trường như :data:`sys.version_info`: *major*, *minor*, *micro*, *releaselevel* và *serial*. *releaselevel* là ``'alpha'``, ``'beta'`` hoặc ``'final'``. Chuyển nó thành chuỗi sẽ cho phiên bản theo ký hiệu Tcl/Tk thông thường, chẳng hạn như ``'9.0.3'`` đối với bản phát hành chính thức hoặc ``'9.1b2'`` đối với bản phát hành thử nghiệm.

      .. versionadded:: 3.11



.. class:: Wm()

   Mixin :class:`!Wm` cung cấp quyền truy cập vào trình quản lý cửa sổ, cho phép ứng dụng kiểm soát các yếu tố như tiêu đề, hình học và biểu tượng của cửa sổ cấp cao nhất, cách cửa sổ được thay đổi kích thước và cách cửa sổ phản hồi với các giao thức của trình quản lý cửa sổ. Mixin này được trộn vào :class:`Tk` và :class:`Toplevel`, vì vậy các phương thức của nó khả dụng trên mọi cửa sổ cấp cao nhất. Mỗi phương thức có hai cách viết tương đương: tên ngắn và tên có tiền tố ``wm_`` (ví dụ: :meth:`title` và :meth:`wm_title`). Xem thêm :ref:`tkinter-window-manager`.

   .. method:: wm_aspect(minNumer=None, minDenom=None, maxNumer=None, maxDenom=None)
      :no-typesetting:

   .. method:: aspect(minNumer=None, minDenom=None, maxNumer=None, maxDenom=None)

      Giới hạn tỷ lệ khung hình (tỷ lệ giữa chiều rộng và chiều cao) của cửa sổ. Nếu cung cấp đủ cả bốn đối số, trình quản lý cửa sổ sẽ giữ tỷ lệ trong khoảng từ ``minNumer/minDenom`` đến ``maxNumer/maxDenom``; truyền các chuỗi rỗng sẽ xóa mọi giới hạn hiện có. Không có đối số, trả về một tuple gồm bốn giá trị hiện tại hoặc ``None`` nếu không có giới hạn tỷ lệ nào đang được áp dụng.
      :meth:`wm_aspect` là bí danh của :meth:`!aspect`.

   .. method:: wm_attributes(*args, return_python_dict=False, **kwargs)
      :no-typesetting:

   .. method:: attributes(*args, return_python_dict=False, **kwargs)

      Truy vấn hoặc thiết lập các thuộc tính dành riêng cho nền tảng của cửa sổ. Không có đối số, trả về các cờ dành riêng cho nền tảng cùng với giá trị của chúng; truyền *return_python_dict* là true để nhận chúng dưới dạng một dictionary. Một tên tùy chọn đơn lẻ như ``'alpha'`` sẽ trả về giá trị của tùy chọn đó, còn các tùy chọn được thiết lập bằng các đối số từ khóa (``alpha=0.5``).

      Các thuộc tính khả dụng khác nhau tùy theo nền tảng. Tất cả các nền tảng đều hỗ trợ:

      *alpha*
         Độ mờ của cửa sổ, từ ``0.0`` (hoàn toàn trong suốt) đến ``1.0`` (đục). Khi không hỗ trợ độ trong suốt, giá trị vẫn là ``1.0``.

      *appearance*
         Cho biết cửa sổ có được hiển thị ở chế độ tối trên Windows và macOS hay không: ``'auto'``, ``'light'`` hoặc ``'dark'`` (điều này không có tác dụng trên X11).

      *fullscreen*
         Cho biết cửa sổ có chiếm toàn bộ màn hình và không có đường viền hay không.

      *topmost*
         Cho biết cửa sổ có được hiển thị bên trên tất cả các cửa sổ khác hay không.

      Windows cũng hỗ trợ thêm:

      *disabled*
         Cho biết cửa sổ có đang ở trạng thái bị vô hiệu hóa hay không.

      *toolwindow*
         Cho biết cửa sổ có sử dụng kiểu cửa sổ công cụ hay không.

      *transparentcolor*
         Màu được đặt hoàn toàn trong suốt hoặc chuỗi rỗng nếu không có.

      macOS cũng hỗ trợ:

      *class*
         Liệu cửa sổ Aqua bên dưới là một ``nswindow`` hay một ``nspanel``; điều này chỉ có thể được thiết lập trước khi cửa sổ được tạo.

      *modified*
         Trạng thái sửa đổi được hiển thị bởi nút đóng và biểu tượng proxy của cửa sổ.

      *notify*
         Liệu biểu tượng dock của ứng dụng có nảy lên để yêu cầu chú ý hay không.

      *stylemask*
         Mặt nạ kiểu dáng của cửa sổ Aqua bên dưới, được cung cấp dưới dạng danh sách các tên bit chẳng hạn như ``titled`` hoặc ``resizable``.

      *tabbingid*
         Mã định danh của nhóm tab mà cửa sổ thuộc về.

      *tabbingmode*
         Cửa sổ có thể được mở dưới dạng tab hay không: ``'auto'``, ``'preferred'`` hoặc ``'disallowed'``.

      *titlepath*
         Đường dẫn của tệp được biểu thị bằng biểu tượng proxy của cửa sổ.

      *transparent*
         Xác định liệu vùng nội dung có trong suốt và bóng cửa sổ có được tắt hay không.

      X11 còn hỗ trợ:

      *type*
         Loại cửa sổ hoặc danh sách các loại theo thứ tự ưu tiên mà trình quản lý cửa sổ nên dùng để diễn giải cửa sổ, chẳng hạn như ``'dialog'`` hoặc ``'splash'``.

      *zoomed*
         Cho biết cửa sổ có đang được phóng to tối đa hay không.

      .. note::

         Tk 8.6 đã thêm thuộc tính *type*, còn Tk 9.0 đã thêm các thuộc tính *appearance*, *class*, *stylemask*, *tabbingid* và *tabbingmode*.

      Trên X11, các thay đổi được áp dụng không đồng bộ, vì vậy giá trị được truy vấn có thể chưa phản ánh yêu cầu gần đây nhất.
      :meth:`wm_attributes` là bí danh của :meth:`!attributes`.

      .. versionchanged:: 3.13
         Giờ đây, có thể truy vấn một thuộc tính riêng lẻ theo tên mà không cần ``-``, và có thể thiết lập các thuộc tính bằng keyword arguments. Tham số *return_python_dict* đã được thêm.

      .. deprecated:: 3.13
         Việc thiết lập một thuộc tính bằng cách truyền tên tùy chọn (có ``-`` ở đầu) và giá trị của nó dưới dạng hai đối số vị trí, như trong ``w.attributes('-alpha', 0.5)``, đã không còn được khuyến nghị; thay vào đó, hãy sử dụng keyword arguments.


   .. method:: wm_client(name=None)
      :no-typesetting:

   .. method:: client(name=None)

      Lưu *name*, vốn phải là tên của máy chủ nơi ứng dụng đang chạy, vào thuộc tính ``WM_CLIENT_MACHINE`` của cửa sổ để cửa sổ hoặc trình quản lý phiên sử dụng. Chuỗi rỗng sẽ xóa thuộc tính này. Nếu không có đối số, trả về tên được đặt gần đây nhất hoặc một chuỗi rỗng.
      :meth:`wm_client` là bí danh của :meth:`!client`.

   .. method:: wm_colormapwindows(*wlist)
      :no-typesetting:

   .. method:: colormapwindows(*wlist)

      Thao tác với thuộc tính ``WM_COLORMAP_WINDOWS``, thuộc tính này cho trình quản lý cửa sổ biết về những cửa sổ có colormap riêng. Nếu cung cấp *wlist*, hãy ghi đè thuộc tính bằng các cửa sổ đó (thứ tự của chúng là thứ tự ưu tiên khi cài đặt colormap). Nếu không có đối số, trả về danh sách các cửa sổ hiện được đặt tên trong thuộc tính.
      :meth:`wm_colormapwindows` là bí danh của :meth:`!colormapwindows`.

   .. method:: wm_command(value=None)
      :no-typesetting:

   .. method:: command(value=None)

      Lưu *value* vào thuộc tính ``WM_COMMAND`` của cửa sổ để cửa sổ hoặc trình quản lý phiên sử dụng; giá trị này phải là một danh sách chứa các từ trong lệnh dùng để gọi ứng dụng. Một chuỗi rỗng sẽ xóa thuộc tính. Nếu không có đối số, trả về giá trị được đặt gần đây nhất hoặc một chuỗi rỗng.
      :meth:`wm_command` là bí danh của :meth:`!command`.

   .. method:: wm_deiconify()
      :no-typesetting:

   .. method:: deiconify()

      Hiển thị cửa sổ ở dạng bình thường (không được biểu tượng hóa) bằng cách map cửa sổ. Nếu cửa sổ chưa từng được map, thao tác này đảm bảo cửa sổ sẽ xuất hiện ở trạng thái khôi phục khỏi biểu tượng khi được map lần đầu. Trên Windows, cửa sổ cũng được đưa lên trước và nhận focus.
      :meth:`wm_deiconify` là bí danh của :meth:`!deiconify`.

   .. method:: wm_focusmodel(model=None)
      :no-typesetting:

   .. method:: focusmodel(model=None)

      Đặt hoặc truy vấn mô hình focus cho cửa sổ. *model* là ``'active'`` (cửa sổ tự nhận focus đầu vào cho chính nó hoặc các cửa sổ con, ngay cả khi focus đang ở ứng dụng khác) hoặc ``'passive'`` (cửa sổ dựa vào trình quản lý cửa sổ để cấp focus cho nó). Nếu không có đối số, trả về mô hình hiện tại. Mặc định là ``'passive'``, đây cũng là giá trị mà lệnh :meth:`!focus` giả định.
      :meth:`wm_focusmodel` là bí danh của :meth:`!focusmodel`.

   .. method:: wm_forget(window)
      :no-typesetting:

   .. method:: forget(window)

      Bỏ ánh xạ *window* khỏi màn hình để trình quản lý cửa sổ không còn quản lý nó. Khi đó, :class:`Toplevel` được xử lý như :class:`Frame`, mặc dù cấu hình ``-menu`` của nó vẫn được ghi nhớ và menu sẽ xuất hiện lại nếu widget được quản lý trở lại.
      :meth:`wm_forget` là bí danh của :meth:`!forget`.

      Không được nhầm với :meth:`Pack.forget`.

      .. versionadded:: 3.3

   .. method:: wm_frame()
      :no-typesetting:

   .. method:: frame()

      Trả về mã định danh cửa sổ dành riêng cho nền tảng của khung trang trí ngoài cùng chứa cửa sổ, nếu trình quản lý cửa sổ đã tái gán cửa sổ đó vào một khung như vậy; nếu không, trả về mã định danh của chính cửa sổ.
      :meth:`wm_frame` là bí danh của :meth:`!frame`.

   .. method:: wm_geometry(newGeometry=None)
      :no-typesetting:

   .. method:: geometry(newGeometry=None)

      Đặt hoặc truy vấn hình học của cửa sổ. *newGeometry* có dạng ``=widthxheight+x+y``, trong đó có thể bỏ qua bất kỳ thành phần nào trong ``=``, ``widthxheight`` và vị trí ``+x+y``. *width* và *height* được tính bằng pixel (hoặc đơn vị lưới đối với cửa sổ dạng lưới); vị trí có tiền tố ``+`` được đo từ cạnh trái hoặc cạnh trên của màn hình, còn vị trí có tiền tố ``-`` được đo từ cạnh phải hoặc cạnh dưới. Độ lệch có thể là số âm, như trong ``'200x100+-9+-8'``, khi cạnh cửa sổ được đặt vượt ra ngoài cạnh tương ứng của màn hình. Chuỗi rỗng sẽ hủy hình học do người dùng chỉ định, cho phép cửa sổ trở về kích thước tự nhiên. Khi không có đối số, trả về hình học hiện tại dưới dạng chuỗi có dạng ``'200x200+10+10'``.
      :meth:`wm_geometry` là bí danh của :meth:`!geometry`.

   .. method:: wm_grid(baseWidth=None, baseHeight=None, widthInc=None, heightInc=None)
      :no-typesetting:

   .. method:: grid(baseWidth=None, baseHeight=None, widthInc=None, heightInc=None)

      Quản lý cửa sổ dưới dạng cửa sổ lưới và xác định mối quan hệ giữa các đơn vị lưới với pixel. *baseWidth* và *baseHeight* là số đơn vị lưới trong kích thước được yêu cầu nội bộ của cửa sổ, còn *widthInc* và *heightInc* là kích thước pixel của một đơn vị lưới ngang và dọc. Chuỗi rỗng sẽ tắt chế độ quản lý dạng lưới. Khi không có đối số, trả về một tuple gồm bốn giá trị hiện tại hoặc ``None`` nếu cửa sổ không ở dạng lưới.
      :meth:`wm_grid` là bí danh của :meth:`!grid`.

      Không nên nhầm lẫn với trình quản lý hình học dạng lưới :meth:`Grid.grid`.

   .. method:: wm_group(pathName=None)
      :no-typesetting:

   .. method:: group(pathName=None)

      Đặt hoặc truy vấn leader của một nhóm cửa sổ liên quan. *pathName* cung cấp tên đường dẫn của group leader; chẳng hạn, trình quản lý cửa sổ có thể bỏ ánh xạ tất cả cửa sổ trong nhóm khi leader được thu nhỏ thành biểu tượng. Chuỗi rỗng sẽ xóa cửa sổ khỏi mọi nhóm. Khi không có đối số, trả về tên đường dẫn của group leader hiện tại hoặc một chuỗi rỗng.
      :meth:`wm_group` là bí danh của :meth:`!group`.

   .. method:: wm_iconbitmap(bitmap=None, default=None)
      :no-typesetting:

   .. method:: iconbitmap(bitmap=None, default=None)

      Đặt hoặc truy vấn bitmap được window manager sử dụng cho biểu tượng của cửa sổ. *bitmap* chỉ định tên một bitmap ở một trong các dạng chuẩn được Tk chấp nhận; chuỗi rỗng hủy bitmap biểu tượng hiện tại. Khi không có đối số, trả về tên bitmap biểu tượng hiện tại hoặc một chuỗi rỗng. Trên Windows, đối số *default* chỉ định một biểu tượng (ví dụ: một ``.ico`` file) được áp dụng cho tất cả cửa sổ cấp cao nhất không có biểu tượng riêng.
      :meth:`wm_iconbitmap` là bí danh của :meth:`!iconbitmap`.

   .. method:: wm_iconify()
      :no-typesetting:

   .. method:: iconify()

      Thu nhỏ cửa sổ thành biểu tượng. Nếu cửa sổ chưa được ánh xạ lần đầu, sắp xếp để cửa sổ xuất hiện ở trạng thái thu nhỏ thành biểu tượng khi được ánh xạ sau đó.
      :meth:`wm_iconify` là bí danh của :meth:`!iconify`.

   .. method:: wm_iconmask(bitmap=None)
      :no-typesetting:

   .. method:: iconmask(bitmap=None)

      Đặt hoặc truy vấn bitmap được sử dụng làm mặt nạ cho biểu tượng (xem
      :meth:`iconbitmap`). Khi mặt nạ là 0, không biểu tượng nào được hiển thị; khi là 1, các bit tương ứng của bitmap biểu tượng được hiển thị. Chuỗi rỗng hủy mặt nạ hiện tại. Khi không có đối số, trả về tên mặt nạ biểu tượng hiện tại hoặc một chuỗi rỗng.
      :meth:`wm_iconmask` là bí danh của :meth:`!iconmask`.

   .. method:: wm_iconname(newName=None)
      :no-typesetting:

   .. method:: iconname(newName=None)

      Đặt hoặc truy vấn tên được trình quản lý cửa sổ hiển thị bên trong biểu tượng của cửa sổ. Khi không có đối số, trả về tên biểu tượng hiện tại hoặc chuỗi rỗng nếu chưa đặt tên nào (trong trường hợp đó, trình quản lý cửa sổ thường hiển thị tiêu đề của cửa sổ).
      :meth:`wm_iconname` là bí danh của :meth:`!iconname`.

   .. method:: wm_iconphoto(default=False, *images)
      :no-typesetting:

   .. method:: iconphoto(default=False, *images)

      Đặt biểu tượng thanh tiêu đề cho cửa sổ từ một hoặc nhiều đối tượng :class:`PhotoImage` được truyền trong *images*. Có thể cung cấp nhiều hình ảnh với các kích thước khác nhau (ví dụ 16x16 và 32x32) để trình quản lý cửa sổ có thể chọn hình ảnh phù hợp. Dữ liệu hình ảnh được chụp nhanh tại thời điểm gọi; các thay đổi về sau đối với hình ảnh sẽ không được phản ánh. Nếu *default* là true, biểu tượng cũng được áp dụng cho tất cả cửa sổ cấp cao nhất được tạo về sau. Trên macOS, chỉ hình ảnh đầu tiên được sử dụng.
      :meth:`wm_iconphoto` là bí danh của :meth:`!iconphoto`.

      .. versionadded:: 3.3

   .. method:: wm_iconposition(x=None, y=None)
      :no-typesetting:

   .. method:: iconposition(x=None, y=None)

      Đặt hoặc truy vấn gợi ý cho trình quản lý cửa sổ về vị trí đặt biểu tượng của cửa sổ. Chuỗi rỗng sẽ hủy gợi ý hiện có. Khi không có đối số, trả về tuple gồm hai giá trị hiện tại hoặc ``None`` nếu không có gợi ý nào đang có hiệu lực.
      :meth:`wm_iconposition` là bí danh của :meth:`!iconposition`.

   .. method:: wm_iconwindow(pathName=None)
      :no-typesetting:

   .. method:: iconwindow(pathName=None)

      Đặt hoặc truy vấn cửa sổ được sử dụng làm biểu tượng cho cửa sổ. Khi cửa sổ được thu nhỏ thành biểu tượng, *pathName* được ánh xạ để làm biểu tượng của cửa sổ đó và được hủy ánh xạ khi cửa sổ được khôi phục. Chuỗi rỗng sẽ hủy liên kết. Khi không có đối số, trả về tên đường dẫn của cửa sổ biểu tượng hiện tại hoặc chuỗi rỗng. Không phải mọi trình quản lý cửa sổ đều hỗ trợ cửa sổ biểu tượng, và khái niệm này không có ý nghĩa trên các nền tảng không phải X11.
      :meth:`wm_iconwindow` là bí danh của :meth:`!iconwindow`.

   .. method:: wm_manage(widget)
      :no-typesetting:

   .. method:: manage(widget)

      Biến *widget* thành một cửa sổ cấp cao nhất độc lập, được window manager trang trí bằng thanh tiêu đề, v.v. Chỉ các widget :class:`Frame`, :class:`LabelFrame` và :class:`Toplevel` mới được sử dụng (các phiên bản :mod:`tkinter.ttk` thì **not** được chấp nhận); truyền vào bất kỳ loại widget nào khác sẽ gây ra lỗi.
      :meth:`wm_manage` là bí danh của :meth:`!manage`.

      .. versionadded:: 3.3

   .. method:: wm_maxsize(width=None, height=None)
      :no-typesetting:

   .. method:: maxsize(width=None, height=None)

      Đặt hoặc truy vấn các kích thước tối đa được phép của cửa sổ, tính bằng pixel (hoặc đơn vị lưới đối với cửa sổ dạng lưới). Window manager giới hạn cửa sổ không được lớn hơn *width* và *height*. Khi không có đối số, trả về một tuple gồm chiều rộng và chiều cao tối đa hiện tại. Kích thước tối đa mặc định bằng kích thước màn hình.
      :meth:`wm_maxsize` là bí danh của :meth:`!maxsize`.

   .. method:: wm_minsize(width=None, height=None)
      :no-typesetting:

   .. method:: minsize(width=None, height=None)

      Đặt hoặc truy vấn các kích thước tối thiểu được phép của cửa sổ, tính bằng pixel (hoặc đơn vị lưới đối với cửa sổ dạng lưới). Window manager giới hạn cửa sổ không được nhỏ hơn *width* và *height*. Khi không có đối số, trả về một tuple gồm chiều rộng và chiều cao tối thiểu hiện tại. Kích thước tối thiểu mặc định là một pixel theo mỗi chiều.
      :meth:`wm_minsize` là bí danh của :meth:`!minsize`.

   .. method:: wm_overrideredirect(boolean=None)
      :no-typesetting:

   .. method:: overrideredirect(boolean=None)

      Đặt hoặc truy vấn cờ override-redirect cho cửa sổ. Khi cờ này được đặt, cửa sổ sẽ bị trình quản lý cửa sổ bỏ qua: cửa sổ không được đặt lại vào một khung trang trí và người dùng không thể thao tác với cửa sổ bằng các điều khiển trình quản lý cửa sổ thông thường. Khi không có đối số, trả về một giá trị boolean cho biết cờ có được đặt hay không, hoặc ``None`` nếu cờ chưa được đặt. Cờ này chỉ được tuân thủ đáng tin cậy khi cửa sổ được ánh xạ lần đầu hoặc được ánh xạ lại từ trạng thái withdrawn.
      :meth:`wm_overrideredirect` là bí danh của :meth:`!overrideredirect`.

   .. method:: wm_positionfrom(who=None)
      :no-typesetting:

   .. method:: positionfrom(who=None)

      Đặt hoặc truy vấn nguồn của vị trí hiện tại của cửa sổ. *who* có thể là ``'program'`` hoặc ``'user'``, cho biết vị trí được yêu cầu bởi chương trình hay người dùng; một chuỗi rỗng sẽ hủy nguồn hiện tại. Khi không có đối số, trả về nguồn hiện tại hoặc một chuỗi rỗng nếu chưa có nguồn nào được đặt. Tk tự động đặt nguồn thành ``'user'`` khi :meth:`geometry` được gọi, trừ khi nguồn đã được đặt rõ ràng thành ``'program'``.
      :meth:`wm_positionfrom` là bí danh của :meth:`!positionfrom`.

   .. method:: wm_protocol(name=None, func=None)
      :no-typesetting:

   .. method:: protocol(name=None, func=None)

      Đăng ký *func* làm trình xử lý cho giao thức của trình quản lý cửa sổ *name*, một atom chẳng hạn như ``'WM_DELETE_WINDOW'``, ``'WM_SAVE_YOURSELF'`` hoặc ``'WM_TAKE_FOCUS'``; sau đó *func* được gọi bất cứ khi nào trình quản lý cửa sổ gửi một thông báo của giao thức đó. Tk cài đặt một trình xử lý ``WM_DELETE_WINDOW`` mặc định để hủy cửa sổ; phương thức này có thể thay thế trình xử lý đó. Nếu *func* là một chuỗi rỗng, trình xử lý sẽ bị xóa. Khi chỉ có *name*, trả về tên của lệnh trình xử lý đã đăng ký cho lệnh đó hoặc một chuỗi rỗng nếu chưa đặt lệnh nào (trình xử lý ``WM_DELETE_WINDOW`` mặc định không được báo cáo); khi không có đối số, trả về một tuple gồm các giao thức hiện có trình xử lý.
      :meth:`wm_protocol` là bí danh của :meth:`!protocol`.

   .. method:: wm_resizable(width=None, height=None)
      :no-typesetting:

   .. method:: resizable(width=None, height=None)

      Kiểm soát việc người dùng có thể thay đổi kích thước cửa sổ một cách tương tác hay không. *width* và *height* là các giá trị boolean xác định chiều rộng và chiều cao của cửa sổ có thể được thay đổi hay không. Khi không có đối số, trả về một tuple gồm hai giá trị ``0``/``1`` cho biết mỗi chiều hiện có thể thay đổi kích thước hay không. Theo mặc định, cửa sổ có thể thay đổi kích thước theo cả hai chiều.
      :meth:`wm_resizable` là bí danh của :meth:`!resizable`.

   .. method:: wm_sizefrom(who=None)
      :no-typesetting:

   .. method:: sizefrom(who=None)

      Đặt hoặc truy vấn nguồn gốc của kích thước hiện tại của cửa sổ. *who* là ``'program'`` hoặc ``'user'``, cho biết kích thước được yêu cầu bởi chương trình hay người dùng; chuỗi rỗng sẽ hủy nguồn hiện tại. Nếu không có đối số, trả về nguồn hiện tại hoặc chuỗi rỗng nếu chưa có nguồn nào được đặt.
      :meth:`wm_sizefrom` là bí danh của :meth:`!sizefrom`.

   .. method:: wm_state(newstate=None)
      :no-typesetting:

   .. method:: state(newstate=None)

      Đặt hoặc truy vấn trạng thái của cửa sổ. Nếu không có đối số, trả về trạng thái hiện tại: một trong các giá trị ``'normal'``, ``'iconic'``, ``'withdrawn'``, ``'icon'`` hoặc, chỉ trên Windows và macOS, ``'zoomed'``. ``'iconic'`` chỉ cửa sổ đã được thu nhỏ thành biểu tượng, còn ``'icon'`` chỉ cửa sổ đóng vai trò là biểu tượng cho một cửa sổ khác (xem
      :meth:`iconwindow`); không thể đặt trạng thái ``'icon'``.
      :meth:`wm_state` là bí danh của :meth:`!state`.

      Không được nhầm lẫn với :meth:`ttk.Widget.state <tkinter.ttk.Widget.state>`.

   .. method:: wm_title(string=None)
      :no-typesetting:

   .. method:: title(string=None)

      Đặt hoặc truy vấn tiêu đề của cửa sổ, tiêu đề mà window manager sẽ hiển thị trên thanh tiêu đề của cửa sổ. Nếu không có đối số, trả về tiêu đề hiện tại. Tiêu đề mặc định là tên của cửa sổ.
      :meth:`wm_title` là bí danh của :meth:`!title`.

   .. method:: wm_transient(master=None)
      :no-typesetting:

   .. method:: transient(master=None)

      Đánh dấu cửa sổ là cửa sổ tạm thời (chẳng hạn như menu xổ xuống hoặc hộp thoại) hoạt động thay mặt cho *master*, là tên đường dẫn của một cửa sổ cấp cao nhất khác. Chuỗi rỗng sẽ xóa trạng thái tạm thời. Nếu không có đối số, trả về tên đường dẫn của master hiện tại hoặc một chuỗi rỗng. Cửa sổ tạm thời phản ánh các thay đổi trạng thái trong master của nó và có thể được window manager trang trí theo cách khác; việc đặt một cửa sổ làm cửa sổ tạm thời của chính nó là lỗi.
      :meth:`wm_transient` là bí danh của :meth:`!transient`.

   .. method:: wm_withdraw()
      :no-typesetting:

   .. method:: withdraw()

      Rút cửa sổ khỏi màn hình, bỏ ánh xạ cửa sổ và khiến window manager quên cửa sổ đó. Nếu cửa sổ chưa từng được ánh xạ, thay vào đó cửa sổ sẽ được ánh xạ ở trạng thái đã rút. Đôi khi cần rút cửa sổ rồi ánh xạ lại cửa sổ đó (chẳng hạn bằng :meth:`deiconify`) để một số window manager nhận biết các thay đổi đối với thuộc tính cửa sổ.
      :meth:`wm_withdraw` là bí danh của :meth:`!withdraw`.


.. class:: Pack()

   Trình quản lý hình học sắp xếp các widget bằng cách đóng gói chúng sát vào các cạnh của vùng chứa. Mixin :class:`!Pack` được tất cả widget kế thừa (thông qua
   :class:`Widget`) và cung cấp các phương thức để quản lý một widget bằng geometry manager *pack*. Xem thêm :ref:`tkinter-geometry-management`.

   .. note::

      :class:`Pack`, :class:`Place` và :class:`Grid` đều định nghĩa các tên phương thức ngắn :meth:`!forget`, :meth:`!info`, :meth:`!slaves`,
      :meth:`!content` và :meth:`!propagate`. Trên một widget, các tên không có tiền tố sẽ trỏ đến các phiên bản của geometry manager *pack*, vì :class:`Pack` và :class:`Misc` đứng trước :class:`Place` và
      :class:`Grid` trong thứ tự phân giải phương thức, bất kể manager nào thực sự quản lý widget; còn :meth:`!configure`/:meth:`!config` cấu hình các tùy chọn của widget, không phải geometry của nó. Sử dụng các phương thức tường minh ``pack_*``, ``grid_*`` và ``place_*`` (và ``pack``, ``grid``, ``place`` để cấu hình geometry) để thao tác với một geometry manager cụ thể.

   .. method:: configure(cnf={}, **kw)
      :no-typesetting:

   .. method:: config(cnf={}, **kw)
      :no-typesetting:

   .. method:: pack_configure(cnf={}, **kw)
               pack(cnf={}, ****kw)

      Đóng gói widget bên trong container của nó, đặt vị trí tương đối so với các widget cùng cấp đã được đóng gói ở đó. Các tùy chọn được hỗ trợ là:

      *side*
         Cạnh nào của vùng chứa để đặt widget sát vào: ``'top'`` (mặc định), ``'bottom'``, ``'left'`` hoặc ``'right'``.

      *fill*
         Có kéo giãn widget để lấp đầy phần được phân bổ cho nó hay không: ``'none'`` (mặc định), ``'x'``, ``'y'`` hoặc ``'both'``.

      *expand*
         Widget có nên mở rộng để sử dụng phần không gian dư thừa trong vùng chứa hay không (giá trị boolean, mặc định là false).

      *anchor*
         Đặt widget ở đâu trong phần được phân bổ cho nó khi phần này lớn hơn widget: một anchor như ``'n'`` hoặc ``'sw'`` (mặc định là ``'center'``).

      *ipadx*, *ipady*
         Khoảng đệm bên trong được thêm vào bên trái và bên phải (*ipadx*) hoặc bên trên và bên dưới (*ipady*) của widget, tính theo khoảng cách trên màn hình (mặc định là ``0``).

      *padx*, *pady*
         Khoảng đệm bên ngoài ở bên trái và bên phải (*padx*) hoặc bên trên và bên dưới (*pady*) của widget, tính theo khoảng cách trên màn hình hoặc một cặp gồm hai khoảng cách cho hai phía (mặc định là ``0``).

      *after*
         Đóng gói widget sau widget đã cho trong thứ tự đóng gói, sử dụng cùng một container.

      *before*
         Đóng gói widget trước widget đã cho trong thứ tự đóng gói, bằng cách sử dụng cùng một container.

      *in_*
         Container mà widget được đóng gói vào; mặc định là widget cha.

      :meth:`pack`, :meth:`configure` và :meth:`config` là các bí danh của
      :meth:`!pack_configure`.

   .. method:: forget()
      :no-typesetting:

   .. method:: pack_forget()

      Bỏ ánh xạ widget và xóa widget khỏi thứ tự đóng gói, đồng thời loại bỏ các tùy chọn đóng gói của nó. Sau đó, widget có thể được đóng gói lại bằng :meth:`pack_configure`.
      :meth:`forget` là bí danh của :meth:`!pack_forget`, ngoại trừ trên :class:`PanedWindow`,
      :class:`ttk.Notebook <tkinter.ttk.Notebook>` và
      :class:`ttk.PanedWindow <tkinter.ttk.PanedWindow>`, các lớp này cung cấp phương thức :meth:`!forget` riêng.

      Không nên nhầm lẫn với :meth:`Wm.forget`.

   .. method:: info()
      :no-typesetting:

   .. method:: pack_info()

      Trả về một dictionary chứa các tùy chọn packing hiện tại của widget.
      :meth:`info` là bí danh của :meth:`!pack_info`.

   .. method:: propagate()
               propagate(flag)
      :no-typesetting:

   .. method:: pack_propagate()
               pack_propagate(flag)

      Giống như :meth:`Misc.pack_propagate`, xem widget này như một container: bật hoặc tắt việc truyền hình học.
      :meth:`propagate` là bí danh của :meth:`!pack_propagate`.

   .. method:: slaves()
      :no-typesetting:

   .. method:: pack_slaves()

      Giống như :meth:`Misc.pack_slaves`: trả về danh sách các widget được pack trong widget này.
      :meth:`slaves` là bí danh của :meth:`!pack_slaves`.


.. class:: Place()

   Trình quản lý hình học đặt các widget tại những vị trí và kích thước cụ thể bên trong vùng chứa của chúng. Mix-in :class:`!Place` được tất cả các widget kế thừa (thông qua
   :class:`Widget`). Xem thêm :ref:`tkinter-geometry-management`.

   .. method:: configure(cnf={}, **kw)
      :no-typesetting:

   .. method:: config(cnf={}, **kw)
      :no-typesetting:

   .. method:: place_configure(cnf={}, **kw)
               place(cnf={}, ****kw)

      Đặt widget bên trong vùng chứa của nó tại một vị trí tuyệt đối hoặc tương đối. Các tùy chọn được hỗ trợ là:

      *x*, *y*
         Vị trí ngang và dọc tuyệt đối của điểm neo của widget, dưới dạng khoảng cách trên màn hình (mặc định ``0``).

      *relx*, *rely*
         Vị trí ngang và dọc của điểm neo của widget dưới dạng phân số của chiều rộng và chiều cao của container, trong đó ``0.0`` là cạnh trái hoặc cạnh trên, còn ``1.0`` là cạnh phải hoặc cạnh dưới. Nếu cung cấp cả tùy chọn tuyệt đối và tương đối, các giá trị của chúng sẽ được cộng lại.

      *anchor*
         Điểm nào của widget được đặt tại vị trí đã cho: một điểm neo như ``'n'`` hoặc ``'se'`` (mặc định ``'nw'``).

      *width*, *height*
         Chiều rộng và chiều cao tuyệt đối của widget, dưới dạng khoảng cách trên màn hình. Theo mặc định, kích thước được yêu cầu của widget sẽ được sử dụng.

      *relwidth*, *relheight*
         Chiều rộng và chiều cao của widget dưới dạng phần của chiều rộng và chiều cao của container. Nếu cung cấp cả tùy chọn tuyệt đối và tương đối, các giá trị của chúng sẽ được cộng lại.

      *bordermode*
         Cách đường viền của container ảnh hưởng đến việc định vị: ``'inside'`` (mặc định) đo vùng bên trong đường viền, ``'outside'`` đo vùng bao gồm cả đường viền, và ``'ignore'`` sử dụng vùng X chính thức.

      *in_*
         Container mà widget được đặt tương đối theo đó; nó phải là widget cha của widget hoặc một hậu duệ của widget cha, và mặc định là widget cha.

      :meth:`place`, :meth:`configure` và :meth:`config` là bí danh của
      :meth:`!place_configure`.

   .. method:: forget()
      :no-typesetting:

   .. method:: place_forget()

      Hủy ánh xạ widget và loại bỏ nó khỏi bố trí, đồng thời quên các tùy chọn vị trí của nó.

   .. method:: info()
      :no-typesetting:

   .. method:: place_info()

      Trả về một dictionary chứa các tùy chọn bố trí hiện tại của widget.

   .. method:: slaves()
      :no-typesetting:

   .. method:: place_slaves()

      Giống như :meth:`Misc.place_slaves`: trả về danh sách các widget được đặt trong widget này.


.. class:: Grid()

   Geometry manager sắp xếp các widget trong một lưới hai chiều gồm các hàng và cột bên trong container của chúng. Mix-in :class:`!Grid` được kế thừa bởi tất cả các widget (thông qua
   :class:`Widget`). Xem thêm :ref:`tkinter-geometry-management`.

   .. method:: configure(cnf={}, **kw)
      :no-typesetting:

   .. method:: config(cnf={}, **kw)
      :no-typesetting:

   .. method:: grid_configure(cnf={}, **kw)
               grid(cnf={}, ****kw)

      Đặt widget vào một ô trong lưới của container.

      Không được nhầm lẫn với :meth:`Wm.grid`.

      Các tùy chọn được hỗ trợ là:

      *row*, *column*
         Hàng và cột của ô nơi đặt widget, được tính từ ``0``. *column* mặc định là cột ngay sau widget trước đó được đặt trong cùng một lệnh gọi :meth:`!grid_configure` (hoặc ``0``), còn *row* mặc định là hàng trống tiếp theo.

      *rowspan*, *columnspan*
         Số hàng và cột mà widget sẽ trải rộng (mặc định là ``1``).

      *sticky*
         Cách định vị hoặc kéo giãn widget khi ô của nó lớn hơn widget: một chuỗi chứa không hoặc nhiều ký tự ``'n'``, ``'s'``, ``'e'`` và ``'w'``, chỉ định các cạnh của ô mà widget bám vào. Việc chỉ định cả ``'n'`` và ``'s'`` (hoặc ``'e'`` và ``'w'``) sẽ kéo giãn widget để lấp đầy chiều cao (hoặc chiều rộng) của ô. Mặc định là ``''``, căn giữa widget ở kích thước được yêu cầu.

      *ipadx*, *ipady*
         Khoảng đệm bên trong được thêm vào bên trái và bên phải (*ipadx*) hoặc bên trên và bên dưới (*ipady*) của widget, tính theo khoảng cách trên màn hình (mặc định là ``0``).

      *padx*, *pady*
         Khoảng đệm bên ngoài ở bên trái và bên phải (*padx*) hoặc bên trên và bên dưới (*pady*) của widget, tính theo khoảng cách trên màn hình hoặc một cặp gồm hai khoảng cách cho hai phía (mặc định là ``0``).

      *in_*
         Container có grid mà widget sẽ được đặt vào; mặc định là widget cha.

      :meth:`grid`, :meth:`configure` và :meth:`config` là các bí danh của
      :meth:`!grid_configure`.

   .. method:: forget()
      :no-typesetting:

   .. method:: grid_forget()

      Bỏ ánh xạ widget và xóa widget khỏi grid, đồng thời quên các tùy chọn grid của widget.

   .. method:: grid_remove()

      Gỡ widget khỏi grid và xóa nó khỏi grid, nhưng hãy nhớ các tùy chọn grid để widget được khôi phục vào cùng một ô nếu được thêm lại vào grid.

   .. method:: info()
      :no-typesetting:

   .. method:: grid_info()

      Trả về một dictionary chứa các tùy chọn grid hiện tại của widget.

   .. method:: bbox(column=None, row=None, col2=None, row2=None)
      :no-typesetting:

   .. method:: grid_bbox(column=None, row=None, col2=None, row2=None)

      Giống như :meth:`Misc.grid_bbox`.
      :meth:`bbox` là bí danh của :meth:`!grid_bbox`, ngoại trừ trên :class:`Canvas`, :class:`Listbox`, :class:`Spinbox`,
      :class:`Text`, :class:`ttk.Entry <tkinter.ttk.Entry>` và
      :class:`ttk.Treeview <tkinter.ttk.Treeview>`, vốn cung cấp phương thức :meth:`!bbox` của riêng mình.

   .. method:: columnconfigure(index, cnf={}, **kw)
      :no-typesetting:

   .. method:: grid_columnconfigure(index, cnf={}, **kw)

      Giống như :meth:`Misc.grid_columnconfigure`: truy vấn hoặc thiết lập các tùy chọn (chẳng hạn như *weight*, *minsize*, *pad* và *uniform*) của một cột grid.
      :meth:`columnconfigure` là bí danh của :meth:`!grid_columnconfigure`.

   .. method:: rowconfigure(index, cnf={}, **kw)
      :no-typesetting:

   .. method:: grid_rowconfigure(index, cnf={}, **kw)

      Giống như :meth:`Misc.grid_rowconfigure`: truy vấn hoặc thiết lập các tùy chọn của một hàng grid.
      :meth:`rowconfigure` là bí danh của :meth:`!grid_rowconfigure`.

   .. method:: location(x, y)
      :no-typesetting:

   .. method:: grid_location(x, y)

      Giống như :meth:`Misc.grid_location`: trả về ``(column, row)`` của ô bao phủ pixel tại *x*, *y*.
      :meth:`location` là bí danh của :meth:`!grid_location`.

   .. method:: size()
      :no-typesetting:

   .. method:: grid_size()

      Giống như :meth:`Misc.grid_size`: trả về một tuple ``(columns, rows)`` cho biết kích thước của grid.
      :meth:`size` là bí danh của :meth:`!grid_size`, ngoại trừ trên widget :class:`Listbox`, widget này cung cấp phương thức :meth:`!size` riêng.

   .. method:: propagate()
               propagate(flag)
      :no-typesetting:

   .. method:: grid_propagate()
               grid_propagate(flag)

      Tương tự như :meth:`Misc.grid_propagate`.

   .. method:: slaves(row=None, column=None)
      :no-typesetting:

   .. method:: grid_slaves(row=None, column=None)

      Tương tự như :meth:`Misc.grid_slaves`: trả về các widget được quản lý trong lưới, tùy chọn giới hạn ở một *hàng* và/hoặc *cột*.


.. class:: XView()

   Mixin cung cấp giao diện cuộn ngang được dùng chung bởi các widget như :class:`Entry`, :class:`Canvas`, :class:`Listbox`, :class:`Text` và
   :class:`Spinbox`. Phương thức :meth:`xview` của một widget được đăng ký làm *lệnh* của một :class:`Scrollbar` ngang.

   .. method:: xview(*args)

      Truy vấn hoặc thay đổi vị trí ngang của chế độ xem. Khi không có đối số, trả về một tuple ``(first, last)`` gồm hai phân số từ 0 đến 1, cho biết phần tài liệu hiện đang hiển thị. Nếu không, các đối số sẽ được truyền cho lệnh widget Tk ``xview`` và thường được tạo bởi một thanh cuộn; :meth:`xview_moveto` và
      :meth:`xview_scroll` cung cấp một giao diện thuận tiện hơn.

   .. method:: xview_moveto(fraction)

      Điều chỉnh chế độ xem để *fraction* của tổng chiều rộng tài liệu nằm ngoài màn hình về bên trái. *fraction* là một số nằm trong khoảng từ 0 đến 1.

   .. method:: xview_scroll(number, what)

      Dịch chế độ xem sang trái hoặc phải *number* đơn vị. *what* là ``'units'`` hoặc ``'pages'``; *number* âm sẽ cuộn sang trái, còn số dương sẽ cuộn sang phải.


.. class:: YView()

   Mixin cung cấp giao diện cuộn dọc được dùng chung bởi các widget như
   :class:`Canvas`, :class:`Listbox` và :class:`Text`. Phương thức :meth:`yview` của widget được đăng ký làm *command* của một cuộn dọc
   :class:`Scrollbar`.

   .. method:: yview(*args)

      Truy vấn hoặc thay đổi vị trí dọc của chế độ xem. Khi không có đối số, trả về một tuple ``(first, last)`` gồm hai phân số từ 0 đến 1 biểu thị phần tài liệu hiện đang hiển thị. Nếu không, các đối số được truyền cho lệnh widget Tk ``yview``, thường được tạo bởi một thanh cuộn; :meth:`yview_moveto` và
      :meth:`yview_scroll` cung cấp một giao diện thuận tiện hơn.

   .. method:: yview_moveto(fraction)

      Điều chỉnh chế độ xem sao cho *fraction* tổng chiều cao của tài liệu nằm ngoài màn hình, phía trên cạnh trên. *fraction* là một số nằm trong khoảng từ 0 đến 1.

   .. method:: yview_scroll(number, what)

      Dịch chế độ xem lên hoặc xuống *number* đơn vị. *what* là ``'units'`` hoặc ``'pages'``; *number* âm sẽ cuộn lên, còn số dương sẽ cuộn xuống.


.. class:: BaseWidget(master, widgetName, cnf={}, kw={}, extra=())

   Lớp cơ sở nội bộ cho tất cả widget. Lớp này kế thừa từ :class:`Misc` và bổ sung cơ chế tạo widget Tk bên dưới; mã ứng dụng thường sử dụng :class:`Widget` hoặc một lớp widget cụ thể thay vì khởi tạo trực tiếp :class:`!BaseWidget`.

   .. method:: destroy()

      Hủy widget này và tất cả các widget con của nó, xóa các widget Tk tương ứng và xóa các lệnh Tcl liên quan.


.. class:: Widget(master, widgetName, cnf={}, kw={}, extra=())

   Lớp cơ sở nội bộ cho các widget tiêu chuẩn. Lớp này kết hợp :class:`BaseWidget` với các mix-in của trình quản lý hình học
   :class:`Pack`, :class:`Place` và :class:`Grid`, để mọi widget đều có thể được quản lý bởi bất kỳ trình quản lý hình học nào trong ba trình quản lý. Các lớp widget cụ thể (:class:`Button`, :class:`Label`, v.v.) kế thừa từ :class:`!Widget`.


Widget cấp cao nhất
^^^^^^^^^^^^^^^^^^^

.. class:: Tk(screenName=None, baseName=None, className='Tk', useTk=True, sync=False, use=None)

   Tạo một widget Tk toplevel, thường là cửa sổ chính của một ứng dụng, và khởi tạo một trình thông dịch Tcl cho widget này. Mỗi instance có một trình thông dịch Tcl liên kết riêng. Kế thừa từ :class:`Misc` và :class:`Wm`.

   Để tạo một trình thông dịch Tcl mà không khởi tạo hệ thống con Tk, hãy sử dụng
   hàm factory :func:`Tcl` thay thế.

   Lớp :class:`Tk` thường được khởi tạo bằng tất cả các giá trị mặc định. Tuy nhiên, các đối số keyword sau hiện được nhận diện:

   *screenName*
      Khi được cung cấp (dưới dạng chuỗi), đối số này sẽ đặt biến môi trường :envvar:`DISPLAY`. (Chỉ X11)
   *baseName*
      Tên của tệp profile. Theo mặc định, *baseName* được suy ra từ tên chương trình (``sys.argv[0]``).
   *className*
      Tên của lớp widget. Được dùng làm tệp profile và cũng làm tên mà Tcl được gọi bằng tên đó (*argv0* trong *interp*).
   *useTk*
      Nếu ``True``, khởi tạo hệ thống Tk. Hàm :func:`tkinter.Tcl() <Tcl>` đặt giá trị này thành ``False``.
   *sync*
      Nếu ``True``, thực thi đồng bộ tất cả lệnh của X server để các lỗi được báo cáo ngay lập tức. Có thể dùng để debug. (Chỉ X11)
   *use*
      Chỉ định *id* của cửa sổ mà ứng dụng sẽ được nhúng vào, thay vì được tạo dưới dạng cửa sổ toplevel độc lập. *id* phải được chỉ định theo cùng cách với giá trị cho tùy chọn -use đối với các widget toplevel (nghĩa là có dạng giống như giá trị được trả về bởi
      :meth:`~Misc.winfo_id`).

      Lưu ý rằng trên một số nền tảng, tùy chọn này chỉ hoạt động chính xác nếu *id* tham chiếu đến một frame hoặc toplevel của Tk đã bật tùy chọn -container.

   :class:`Tk` đọc và diễn giải các tệp profile, có tên là
   :file:`.{className}.tcl` và :file:`.{baseName}.tcl`, vào trình thông dịch Tcl rồi gọi :func:`exec` trên nội dung của
   :file:`.{className}.py` và :file:`.{baseName}.py`. Đường dẫn đến các tệp profile là biến môi trường :envvar:`HOME` hoặc, nếu biến đó chưa được định nghĩa, thì là :data:`os.curdir`.

   .. note::

      Trên Windows, việc tạo một trình thông dịch Tcl (bằng cách khởi tạo :class:`Tk` hoặc gọi :func:`Tcl`) sẽ đặt biến môi trường :envvar:`HOME` cho tiến trình, nếu biến này chưa được đặt, thành ``%HOMEDRIVE%%HOMEPATH%`` (hoặc
      :envvar:`USERPROFILE`, hoặc ``c:\``). Việc này được Tcl thực hiện và có thể ảnh hưởng đến mã khác đọc :envvar:`HOME`.

   .. attribute:: tk

      Đối tượng ứng dụng Tk được tạo bằng cách khởi tạo :class:`Tk`. Đối tượng này cung cấp quyền truy cập vào trình thông dịch Tcl. Mỗi widget được gắn vào cùng một thực thể :class:`Tk` sẽ có cùng giá trị cho thuộc tính :attr:`tk` của nó.

   .. attribute:: master

      Đối tượng widget chứa widget này. Đối với :class:`Tk`, :attr:`!master` là :const:`None` vì đây là cửa sổ chính. Các thuật ngữ *master* và *parent* tương tự nhau và đôi khi được dùng thay thế cho nhau làm tên đối số; tuy nhiên, việc gọi
      :meth:`~Misc.winfo_parent` trả về một chuỗi chứa tên widget, còn
      :attr:`!master` trả về đối tượng. *parent*/*child* thể hiện mối quan hệ dạng cây, trong khi *master* (hoặc *container*)/*content* thể hiện cấu trúc container.

   .. attribute:: children

      Các widget con trực tiếp của widget này dưới dạng một :class:`dict`, trong đó tên widget con là các khóa và các đối tượng instance của widget con là các giá trị.

   .. method:: destroy()

      Hủy widget này cùng tất cả widget con cháu và, đối với cửa sổ chính, kết thúc kết nối với trình thông dịch Tcl bên dưới.

   .. method:: loadtk()

      Hoàn tất việc tải và khởi tạo hệ thống con Tk. Điều này chỉ cần thiết khi interpreter được tạo mà không có Tk (ví dụ thông qua :func:`Tcl`); nó được gọi tự động khi *useTk* là true.

   .. method:: readprofile(baseName, className)

      Đọc và nạp các tệp profile của người dùng :file:`.{className}.tcl` và
      :file:`.{baseName}.tcl` vào Tcl interpreter, đồng thời thực thi các tệp :file:`.{className}.py` và :file:`.{baseName}.py` tương ứng. Việc này được thực hiện trong quá trình khởi tạo; xem phần mô tả về constructor ở trên.

   .. method:: report_callback_exception(exc, val, tb)

      Báo cáo ngoại lệ callback. Phương thức này được gọi khi một ngoại lệ thoát ra khỏi callback Tkinter; *exc*, *val* và *tb* lần lượt là kiểu, giá trị và traceback của ngoại lệ do :func:`sys.exc_info` trả về. Cách triển khai mặc định sẽ in traceback vào :data:`sys.stderr`. Có thể ghi đè phương thức này để tùy chỉnh việc xử lý lỗi, chẳng hạn như hiển thị traceback trong một hộp thoại.


.. class:: Toplevel(master=None, cnf={}, **kw)

   Một widget :class:`!Toplevel` là một cửa sổ cấp cao nhất, tương tự như một
   :class:`Frame`, ngoại trừ việc X parent của nó là cửa sổ gốc của một màn hình thay vì logical parent của nó. Mục đích chính của nó là làm vùng chứa cho các hộp thoại và những tập hợp widget khác; các đặc điểm duy nhất có thể nhìn thấy là nền và một đường viền 3-D tùy chọn. Các tùy chọn đáng chú ý gồm *menu*, tùy chọn này cài đặt một :class:`Menu` làm menubar của cửa sổ. Nó kế thừa từ :class:`BaseWidget` và :class:`Wm`, vì vậy một toplevel được window manager quản lý. Hãy tham khảo trang hướng dẫn Tk ``toplevel`` để xem danh sách đầy đủ các tùy chọn.


Các lớp widget
^^^^^^^^^^^^^^

.. class:: Button(master=None, cnf={}, **kw)

   Một widget :class:`!Button` hiển thị chuỗi văn bản, bitmap hoặc hình ảnh và gọi một command khi người dùng nhấn vào nó (bằng cách nhấp nút chuột 1 trên nút hoặc, khi nút được focus, bằng cách nhấn phím cách). Kế thừa từ :class:`Widget`. Ngoài các tùy chọn widget tiêu chuẩn, một button chấp nhận các tùy chọn được mô tả trong trang hướng dẫn Tk ``button``, chẳng hạn như *command* (callback được gọi khi button được nhấn), *textvariable*, *state* và *default*.

   .. method:: invoke()

      Gọi command liên kết với button, nếu có, và trả về kết quả của command đó hoặc một chuỗi rỗng nếu button không có command liên kết. Thao tác này bị bỏ qua nếu trạng thái của button là ``disabled``.

   .. method:: flash()

      Làm button nhấp nháy bằng cách hiển thị lại nó nhiều lần, xen kẽ giữa các màu active và normal. Khi kết thúc hiệu ứng nhấp nháy, button được giữ ở cùng trạng thái normal hoặc active như khi phương thức được gọi. Thao tác này bị bỏ qua nếu trạng thái của button là ``disabled``.


.. class:: Canvas(master=None, cnf={}, **kw)

   Một widget :class:`!Canvas` triển khai đồ họa có cấu trúc. Widget này hiển thị任 ý số lượng *items*, chẳng hạn như cung tròn, đường thẳng, hình oval, đa giác, hình chữ nhật, văn bản, bitmap, hình ảnh và cửa sổ được nhúng; các item này có thể được vẽ, di chuyển, đổi màu và liên kết với các event. Kế thừa từ :class:`Widget`, :class:`XView` và :class:`YView`, vì vậy chế độ xem có thể được cuộn theo chiều ngang và chiều dọc bằng :meth:`~XView.xview` và :meth:`~YView.yview`. Tham khảo trang hướng dẫn Tk ``canvas`` để xem danh sách đầy đủ các tùy chọn của widget và item.

   Mỗi item có một *id* số nguyên duy nhất, được gán khi item được tạo, và không hoặc nhiều *tags* dạng chuỗi. Tag là một chuỗi tùy ý không có dạng số nguyên; cùng một tag có thể được nhiều item dùng chung, nhờ đó tag thuận tiện cho việc nhóm các item. Tag đặc biệt ``'all'`` khớp với mọi item trên canvas, còn ``'current'`` khớp với item ở trên cùng bên dưới con trỏ chuột. Hầu hết các phương thức nhận một đối số *tagOrId*, có thể là id số nguyên chỉ định một item duy nhất hoặc tag chỉ định không hoặc nhiều item; như được mô tả trong trang hướng dẫn Tk ``canvas``, tag cũng có thể là một biểu thức logic gồm các tag kết hợp bằng các toán tử ``&&``, ``||``, ``^``, ``!`` và dấu ngoặc đơn. Khi một phương thức hoạt động trên một item duy nhất nhận *tagOrId* khớp với nhiều item, phương thức thường sử dụng item khớp có vị trí thấp nhất trong danh sách hiển thị.

   Các item được lưu trong một *display list* xác định thứ tự vẽ: các item xuất hiện sau trong danh sách được vẽ chồng lên các item xuất hiện trước. Item mới được tạo sẽ được đặt ở đầu danh sách; thứ tự có thể được thay đổi bằng :meth:`tag_raise` và :meth:`tag_lower`.

   .. method:: create_arc(*args, **kw)
               create_bitmap(*args, **kw) create_image(*args, ****kw) create_line(*args, **kw) create_oval(*args, ****kw) create_polygon(*args, **kw) create_rectangle(*args, ****kw) create_text(*args, **kw) create_window(*args, ****kw)

      Tạo một item mới thuộc kiểu tương ứng và trả về id dạng số nguyên của item đó. Mỗi phương thức được gọi như ``create_TYPE(coord..., **options)``: các đối số vị trí đứng đầu cung cấp tọa độ xác định item (dưới dạng các số riêng biệt, một chuỗi số duy nhất hoặc các cặp tọa độ), còn các đối số keyword thiết lập những tùy chọn riêng của item. Tọa độ và khoảng cách trên màn hình có thể được cung cấp dưới dạng số (được hiểu là pixel) hoặc chuỗi có hậu tố đơn vị (``'m'``, ``'c'``, ``'i'`` hoặc ``'p'`` tương ứng với millimet, centimet, inch hoặc point của máy in), nhưng luôn được lưu trữ và trả về theo pixel.

      Các kiểu item gồm: ``arc`` (một vùng hình cung là một phần của hình oval, được xác định bởi hai góc đối diện theo đường chéo ``x1, y1, x2, y2`` của hình chữ nhật bao quanh); ``bitmap`` (một bitmap hai màu được đặt tại một điểm ``x, y``); ``image`` (một ảnh Tk được đặt tại một điểm ``x, y``); ``line`` (một đường thẳng hoặc đường cong đi qua các điểm ``x1, y1, ..., xn, yn``); ``oval`` (một hình tròn hoặc hình ellipse nội tiếp trong hình chữ nhật ``x1, y1, x2, y2``); ``polygon`` (một đa giác đóng đi qua các điểm ``x1, y1, ..., xn, yn``); ``rectangle`` (một hình chữ nhật có các góc ``x1, y1, x2, y2``); ``text`` (một chuỗi văn bản được đặt tại một điểm ``x, y``); và ``window`` (một widget con được nhúng vào canvas tại một điểm ``x, y``, được chỉ định bằng tùy chọn *window*).

      Hầu hết các kiểu item đều chấp nhận một tập hợp *standard item options* dùng chung, cùng với một vài tùy chọn riêng cho từng kiểu. Tên tùy chọn được truyền dưới dạng các đối số keyword, không có dấu gạch nối ở đầu.

      Các tùy chọn item tiêu chuẩn gồm:

      *fill*
         Màu dùng để tô phần bên trong của item hoặc để vẽ item *line* hay các ký tự của item *text*. Chuỗi rỗng (mặc định cho mọi kiểu, ngoại trừ *line* và *text*) khiến item không được tô.

      *outline*
         Màu được sử dụng để vẽ đường viền của mục. Chuỗi rỗng sẽ không vẽ đường viền.

      *width*
         Độ rộng của đường viền, mặc định là ``1.0``. Không có tác dụng nếu *outline* là chuỗi rỗng.

      *dash*
         Mẫu nét đứt cho đường viền, được cung cấp dưới dạng một chuỗi độ dài các đoạn tính bằng pixel hoặc một chuỗi gồm các ký tự ``'.'``, ``','``, ``'-'``, ``'_'`` và dấu cách. Mẫu rỗng (mặc định) sẽ vẽ đường viền liền.

      *dashoffset*
         Độ lệch ban đầu tính bằng pixel trong mẫu *dash*. Bị bỏ qua nếu không có mẫu *dash*.

      *stipple*
         Một bitmap được dùng làm mẫu stipple khi tô mục. Chỉ được hỗ trợ tốt trên X11.

      *outlinestipple*
         Một bitmap được dùng làm mẫu stipple khi vẽ đường viền. Không có tác dụng nếu *outline* trống.

      *offset*, *outlineoffset*
         Độ lệch của các mẫu stipple tô và đường viền, được chỉ định dưới dạng ``'x,y'`` hoặc một cạnh như ``'n'``, ``'se'`` hoặc ``'center'``. Độ lệch stipple chỉ được hỗ trợ trên X11.

      *state*
         Ghi đè trạng thái canvas cho mục này; một trong ``'normal'``, ``'disabled'`` hoặc ``'hidden'``.

      *tags*
         Một tag hoặc một chuỗi tag để liên kết với mục này, thay thế mọi tag hiện có.

      Nhiều tùy chọn trong số này có các biến thể *active...* và *disabled...* (chẳng hạn như *activefill*, *disabledfill*, *activewidth*, *disableddash*, *activeoutline*, *disabledstipple*) để ghi đè tùy chọn cơ sở khi mục là mục đang hoạt động (bên dưới con trỏ chuột) hoặc ở trạng thái bị vô hiệu hóa.

      Các loại mục sau hỗ trợ những tùy chọn bổ sung.

      Đối với các mục ``arc``:

      *start*
         Điểm bắt đầu của phạm vi góc của cung, tính bằng độ theo hướng ngược chiều kim đồng hồ từ vị trí 3 giờ.

      *extent*
         Kích thước của phạm vi góc, tính bằng độ ngược chiều kim đồng hồ từ *start*.

      *style*
         Cách vẽ cung: ``'pieslice'`` (mặc định), ``'chord'`` hoặc ``'arc'``.

      Đối với các mục ``line``:

      *arrow*
         Vị trí vẽ đầu mũi tên: ``'none'`` (mặc định), ``'first'``, ``'last'`` hoặc ``'both'``.

      *arrowshape*
         Một chuỗi gồm ba khoảng cách mô tả hình dạng của các đầu mũi tên.

      *capstyle*
         Cách vẽ các đầu đường: ``'butt'`` (mặc định), ``'projecting'`` hoặc ``'round'``.

      *joinstyle*
         Cách vẽ các đỉnh đường: ``'round'`` (mặc định), ``'bevel'`` hoặc ``'miter'``.

      *smooth*
         Phương thức làm mượt: giá trị false (mặc định) để không làm mượt, hoặc ``'true'``/``'bezier'`` hay ``'raw'`` để vẽ đường dưới dạng đường cong.

      *splinesteps*
         Số lượng đoạn thẳng xấp xỉ mỗi spline khi *smooth* được bật.

      Đối với ``polygon`` mục:

      *joinstyle*, *smooth*, *splinesteps*
         Tương tự như với các mục ``line``, áp dụng cho đường viền của đa giác.

      Đối với các mục ``text``:

      *text*
         Chuỗi cần hiển thị; các ký tự dòng mới sẽ bắt đầu dòng mới.

      *font*
         Phông chữ được sử dụng cho văn bản.

      *justify*
         Cách căn chỉnh các dòng: ``'left'`` (mặc định), ``'right'`` hoặc ``'center'``.

      *anchor*
         Văn bản được định vị như thế nào so với điểm của nó, mặc định là ``'center'``.

      *width*
         Độ dài dòng tối đa; nếu khác không, các dòng sẽ được ngắt tại khoảng trắng.

      *angle*
         Số độ xoay văn bản ngược chiều kim đồng hồ quanh điểm định vị, từ ``0.0`` đến ``360.0`` (mặc định là ``0.0``).

      *underline*
         Chỉ mục của ký tự cần gạch chân, hoặc ``-1`` nếu không có.

      Đối với các mục ``bitmap``:

      *bitmap*
         Bitmap cần hiển thị.

      *anchor*
         Cách bitmap được định vị tương đối so với điểm của nó.

      *background*, *foreground*
         Các màu được dùng cho các pixel ``0`` và ``1`` của bitmap; *background* trống khiến các pixel ``0`` trở nên trong suốt. Cả hai đều có các biến thể *active...* và *disabled...*, còn *bitmap* có các biến thể *activebitmap* và *disabledbitmap*.

      Đối với các mục ``image``:

      *image*
         Tk image cần hiển thị, được tạo trước đó bằng các image protocol.

      *anchor*
         Cách image được định vị so với điểm của nó.

      Cả hai tùy chọn đều có các biến thể *active...* và *disabled...* (*activeimage*, *disabledimage*) được dùng ở các trạng thái active và disabled.

      Đối với các mục ``window``:

      *window*
         Widget cần nhúng; widget này phải là phần tử con của canvas hoặc một trong các phần tử tổ tiên của canvas, và không được là cửa sổ cấp cao nhất.

      *anchor*
         Cách cửa sổ được định vị tương đối so với điểm của nó.

      *width*, *height*
         Kích thước được gán cho cửa sổ; nếu bằng 0 (mặc định), cửa sổ sẽ được cấp kích thước mà nó yêu cầu.

      Các mục ``oval`` và ``rectangle`` không có tùy chọn dành riêng cho từng kiểu; chúng chỉ sử dụng các tùy chọn mục tiêu chuẩn.

      .. note::

         Tk 8.6 đã thêm tùy chọn *angle* và Tk 9.0 đã thêm tùy chọn *underline* cho các mục ``text``.

   .. method:: coords(tagOrId)
               coords(tagOrId, coordList, /) coords(tagOrId, /, *coordList)

      Truy vấn hoặc sửa đổi tọa độ của một mục. Khi chỉ cung cấp *tagOrId*, trả về danh sách các tọa độ số thực của mục được xác định bởi *tagOrId* (mục đầu tiên khớp nếu có nhiều mục khớp). Khi cung cấp tọa độ mới, thay thế tọa độ của mục đó bằng các tọa độ mới; giống như các phương thức ``create_*``, tọa độ có thể được cung cấp dưới dạng các số riêng biệt, một chuỗi đơn hoặc các cặp tọa độ. Tọa độ được trả về luôn tính bằng pixel, bất kể đơn vị được dùng để chỉ định chúng; đối với hình chữ nhật, hình oval và cung, chúng được sắp xếp theo thứ tự trái, trên, phải, dưới.

      .. versionchanged:: 3.12
         Các đối số hiện được làm phẳng: tọa độ có thể được cung cấp dưới dạng các đối số riêng biệt, một chuỗi đơn hoặc được nhóm thành từng cặp, giống như các phương thức ``create_*``.


   .. method:: move(tagOrId, xAmount, yAmount, /)

      Di chuyển từng mục được xác định bởi *tagOrId* trong không gian tọa độ canvas bằng cách cộng *xAmount* vào mọi tọa độ x và *yAmount* vào mọi tọa độ y của mục đó.

   .. method:: moveto(tagOrId, x='', y='')

      Di chuyển các mục được xác định bởi *tagOrId* sao cho cặp tọa độ đầu tiên (góc trên bên trái của hộp bao) của mục khớp thấp nhất nằm tại vị trí (*x*, *y*). *x* hoặc *y* có thể là chuỗi rỗng; khi đó, tọa độ tương ứng không thay đổi. Tất cả các mục khớp vẫn giữ nguyên vị trí tương đối so với nhau.

      .. versionadded:: 3.8


   .. method:: scale(tagOrId, xOrigin, yOrigin, xScale, yScale, /)

      Điều chỉnh tỷ lệ tọa độ của tất cả các mục được chỉ định bởi *tagOrId* trong hệ tọa độ canvas. Mỗi tọa độ x được điều chỉnh sao cho khoảng cách từ *xOrigin* thay đổi theo hệ số *xScale*, và mỗi tọa độ y được điều chỉnh sao cho khoảng cách từ *yOrigin* thay đổi theo hệ số *yScale* (hệ số ``1.0`` giữ nguyên tọa độ).

   .. method:: delete(*tagOrIds)

      Xóa từng mục được chỉ định bởi các đối số *tagOrIds*.

   .. method:: dchars(tagOrId, first, /)
               dchars(tagOrId, first, last, /)

      Xóa khỏi từng mục được chỉ định bởi *tagOrId* các ký tự (đối với mục văn bản) hoặc tọa độ (đối với mục đường thẳng và đa giác) trong phạm vi từ *first* đến *last*, bao gồm cả hai đầu mút; *last* mặc định là *first*. Các mục không hỗ trợ lập chỉ mục sẽ bỏ qua thao tác này.

   .. method:: insert(tagOrId, beforeThis, string, /)

      Chèn *string* vào từng mục được chỉ định bởi *tagOrId*, ngay trước ký tự hoặc tọa độ có chỉ mục là *beforeThis*. Đối với các mục đường thẳng và đa giác, *string* phải là một chuỗi tọa độ hợp lệ.

   .. method:: itemcget(tagOrId, option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option* cho mục được chỉ định bởi *tagOrId* (mục khớp đầu tiên nếu có nhiều mục khớp). Phương thức này tương tự :meth:`~Misc.cget`, nhưng áp dụng cho một mục riêng lẻ.

   .. method:: itemconfig(tagOrId, cnf=None, **kw)
      :no-typesetting:

   .. method:: itemconfigure(tagOrId, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của các mục được chỉ định bởi *tagOrId*. Phương thức này tương tự :meth:`~Misc.configure`, ngoại trừ việc áp dụng cho từng mục riêng lẻ thay vì toàn bộ canvas. Khi không có tùy chọn nào, phương thức trả về một dictionary mô tả các tùy chọn hiện tại của mục khớp đầu tiên; nếu không, phương thức đặt các tùy chọn đã cho trên mọi mục khớp. Các tùy chọn hợp lệ là những tùy chọn được phương thức ``create_*`` tương ứng chấp nhận.
      :meth:`itemconfig` là bí danh của :meth:`!itemconfigure`.

   .. method:: type(tagOrId)

      Trả về kiểu của mục được chỉ định bởi *tagOrId* (mục đầu tiên khớp nếu nó khớp với nhiều mục), chẳng hạn như ``'rectangle'`` hoặc ``'text'``, hoặc ``None`` nếu *tagOrId* không khớp với mục nào.

   .. method:: gettags(tagOrId, /)

      Trả về một tuple gồm các thẻ liên kết với mục được chỉ định bởi *tagOrId* (mục đầu tiên khớp theo thứ tự display-list nếu nó khớp với nhiều mục). Trả về một tuple rỗng nếu không có mục nào khớp hoặc mục đó không có thẻ.

   .. method:: dtag(tagOrId, /)
               dtag(tagOrId, tagToDelete, /)

      Xóa thẻ *tagToDelete* (mặc định là *tagOrId*) khỏi từng mục được chỉ định bởi *tagOrId*. Các mục không có thẻ đó sẽ không bị ảnh hưởng.

   .. method:: addtag(newtag, searchSpec, /, *args)

      Thêm thẻ *newtag* vào từng mục được chọn bởi đặc tả tìm kiếm *searchSpec* (và mọi *args* bổ sung). *searchSpec* là một trong các giá trị ``'above'``, ``'all'``, ``'below'``, ``'closest'``, ``'enclosed'``, ``'overlapping'`` hoặc ``'withtag'``; các phương thức ``addtag_*`` bên dưới là các wrapper tiện lợi, cung cấp từng dạng này.

   .. method:: addtag_above(newtag, tagOrId)

      Thêm thẻ *newtag* vào mục ngay phía trên (sau) *tagOrId* trong display list.

   .. method:: addtag_all(newtag)

      Thêm tag *newtag* vào tất cả item trên canvas.

   .. method:: addtag_below(newtag, tagOrId)

      Thêm tag *newtag* vào item ngay bên dưới (trước) *tagOrId* trong danh sách hiển thị.

   .. method:: addtag_closest(newtag, x, y, halo=None, start=None)

      Thêm tag *newtag* vào item gần điểm (*x*, *y*) nhất. Nếu cung cấp *halo*, mọi item nằm trong khoảng cách đó tính từ điểm sẽ được xem là chồng lấn với điểm. Nếu cung cấp *start* (một tag hoặc id), chọn item gần nhất ở trên cùng nằm bên dưới *start* trong danh sách hiển thị; tùy chọn này có thể được dùng để duyệt qua tất cả các item gần nhất.

   .. method:: addtag_enclosed(newtag, x1, y1, x2, y2)

      Thêm tag *newtag* vào mọi item được bao hoàn toàn trong hình chữ nhật (*x1*, *y1*, *x2*, *y2*), trong đó *x1* <= *x2* và *y1* <= *y2*.

   .. method:: addtag_overlapping(newtag, x1, y1, x2, y2)

      Thêm tag *newtag* vào mọi item chồng lấn hoặc nằm trong hình chữ nhật (*x1*, *y1*, *x2*, *y2*), trong đó *x1* <= *x2* và *y1* <= *y2*.

   .. method:: addtag_withtag(newtag, tagOrId)

      Thêm tag *newtag* vào mọi item được chỉ định bởi *tagOrId*.

   .. method:: find(searchSpec, /, *args)

      Trả về một tuple chứa id của tất cả item được chọn bởi đặc tả tìm kiếm *searchSpec* (và mọi *args* bổ sung), theo thứ tự xếp chồng với item thấp nhất ở trước. Đặc tả tìm kiếm có một trong các dạng được :meth:`addtag` chấp nhận. Các phương thức ``find_*`` bên dưới là các wrapper thuận tiện hơn cho đặc tả này.

   .. method:: find_above(tagOrId)

      Trả về một tuple chứa id của item ngay phía trên *tagOrId* trong danh sách hiển thị.

   .. method:: find_all()

      Trả về một tuple gồm id của tất cả item trên canvas, theo thứ tự xếp chồng.

   .. method:: find_below(tagOrId)

      Trả về một tuple chứa id của item ngay phía dưới *tagOrId* trong danh sách hiển thị.

   .. method:: find_closest(x, y, halo=None, start=None)

      Trả về một tuple chứa id của item gần điểm (*x*, *y*) nhất. *halo* và *start* được diễn giải như đối với :meth:`addtag_closest`.

   .. method:: find_enclosed(x1, y1, x2, y2)

      Trả về một tuple gồm id của tất cả item nằm hoàn toàn trong hình chữ nhật (*x1*, *y1*, *x2*, *y2*).

   .. method:: find_overlapping(x1, y1, x2, y2)

      Trả về một tuple gồm id của tất cả item chồng lấn hoặc nằm trong hình chữ nhật (*x1*, *y1*, *x2*, *y2*).

   .. method:: find_withtag(tagOrId)

      Trả về một tuple gồm id của tất cả item được chỉ định bởi *tagOrId*.

   .. method:: lift(tagOrId, aboveThis=None, /)
      :no-typesetting:

   .. method:: tkraise(tagOrId, aboveThis=None, /)
      :no-typesetting:

   .. method:: tag_raise(tagOrId, aboveThis=None, /)

      Di chuyển tất cả các mục được chỉ định bởi *tagOrId* đến một vị trí mới trong danh sách hiển thị, ngay phía trên mục được chỉ định bởi *aboveThis*, hoặc lên đầu danh sách hiển thị nếu *aboveThis* bị bỏ qua. Khi di chuyển nhiều mục, thứ tự tương đối của chúng được giữ nguyên. Điều này không ảnh hưởng đến các mục cửa sổ được nhúng, vì thứ tự xếp chồng của chúng được điều khiển bởi :meth:`Misc.tkraise` và :meth:`Misc.lower`.
      :meth:`lift` và :meth:`tkraise` là các bí danh của :meth:`!tag_raise`.

   .. method:: lower(tagOrId, belowThis=None, /)
      :no-typesetting:

   .. method:: tag_lower(tagOrId, belowThis=None, /)

      Di chuyển tất cả các mục được chỉ định bởi *tagOrId* đến một vị trí mới trong danh sách hiển thị, ngay phía dưới mục được chỉ định bởi *belowThis*, hoặc xuống cuối danh sách hiển thị nếu *belowThis* bị bỏ qua. Khi di chuyển nhiều mục, thứ tự tương đối của chúng được giữ nguyên. Điều này không ảnh hưởng đến các mục cửa sổ được nhúng.
      :meth:`lower` là bí danh của :meth:`!tag_lower`.

      .. note::

         Trên một :class:`Canvas`, :meth:`tkraise`/:meth:`lift` và :meth:`lower` sắp xếp lại các mục canvas, che khuất :meth:`Misc.tkraise`/:meth:`Misc.lift` được kế thừa và
         các phương thức :meth:`Misc.lower` sắp xếp lại chính widget, vì vậy các phương thức này không khả dụng.

   .. method:: tag_bind(tagOrId, sequence=None, func=None, add=None)

      Liên kết callback *func* với sự kiện *sequence* cho tất cả các mục được chỉ định bởi *tagOrId*, để *func* được gọi bất cứ khi nào sự kiện đó xảy ra đối với một trong các mục. Điều này tương tự như :meth:`Widget.bind <Misc.bind>` nhưng hoạt động trên các mục canvas thay vì toàn bộ widget; chỉ có thể liên kết các sự kiện chuột, bàn phím và sự kiện ảo. Các sự kiện chuột được chuyển đến mục hiện tại còn các sự kiện bàn phím được chuyển đến mục đang được focus (xem :meth:`focus`). Nếu *add* là true, liên kết mới sẽ được thêm vào các liên kết hiện có cho cùng một sequence thay vì thay thế chúng. Trả về mã định danh của hàm đã liên kết, mã này có thể được truyền cho
      :meth:`tag_unbind`.

   .. method:: tag_unbind(tagOrId, sequence, funcid=None)

      Xóa liên kết của sự kiện *sequence* khỏi tất cả các mục được chỉ định bởi *tagOrId*. Nếu cung cấp *funcid*, chỉ callback đó (như được trả về bởi
      :meth:`tag_bind`) được hủy liên kết và hủy đăng ký.

      .. versionchanged:: 3.13
         Nếu cung cấp *funcid*, chỉ callback đó được hủy liên kết.


   .. method:: bbox(tagOrId, /, *tagOrIds)

      Trả về một bộ 4 phần tử ``(x1, y1, x2, y2)``, biểu thị hộp giới hạn gần đúng theo pixel, bao quanh tất cả các mục được chỉ định bởi *tagOrId* và mọi *tagOrIds* bổ sung. Kết quả có thể lớn hơn hộp giới hạn thực vài pixel. Trả về ``None`` nếu không có mục nào khớp hoặc các mục khớp không có gì để hiển thị.

      Phương thức này che khuất :meth:`!Misc.bbox` được kế thừa; hãy sử dụng :meth:`~Misc.grid_bbox` cho hộp giới hạn của grid.

   .. method:: canvasx(screenx, gridspacing=None)

      Với tọa độ x của cửa sổ *screenx*, trả về tọa độ x của canvas được hiển thị tại vị trí đó. Nếu cung cấp *gridspacing*, kết quả được làm tròn đến bội số gần nhất của *gridspacing* đơn vị.

   .. method:: canvasy(screeny, gridspacing=None)

      Với tọa độ y của cửa sổ *screeny*, trả về tọa độ y của canvas được hiển thị tại vị trí đó. Nếu cung cấp *gridspacing*, kết quả được làm tròn đến bội số gần nhất của *gridspacing* đơn vị.

   .. method:: focus()
               focus(tagOrId, /)

      Với *tagOrId*, đặt focus bàn phím của canvas vào mục đầu tiên được chỉ định bởi *tagOrId* có hỗ trợ con trỏ chèn; focus được giữ nguyên nếu không có mục nào như vậy. Nếu *tagOrId* là một chuỗi rỗng, đặt lại focus để không có mục nào có focus. Khi không có đối số, trả về id của mục hiện đang có focus hoặc một chuỗi rỗng nếu không có mục nào.

      Điều này che khuất :meth:`!Misc.focus` được kế thừa; hãy dùng :meth:`~Misc.focus_set` để đặt focus cho chính widget.

   .. method:: icursor(tagOrId, index, /)

      Đặt con trỏ chèn của các mục được chỉ định bởi *tagOrId* ngay trước ký tự được chỉ định bởi *index*. Các mục không hỗ trợ con trỏ chèn sẽ không bị ảnh hưởng. Con trỏ chỉ được hiển thị khi mục có focus, nhưng vị trí của nó có thể được đặt bất kỳ lúc nào.

   .. method:: index(tagOrId, index, /)

      Trả về dưới dạng số nguyên chỉ mục số trong *tagOrId* tương ứng với *index*, vốn là mô tả dạng văn bản của một vị trí (đối với các mục văn bản, là chỉ mục trong các ký tự; đối với các mục đường và đa giác, là chỉ mục trong các tọa độ). Nếu *tagOrId* khớp với nhiều mục, mục đầu tiên hỗ trợ lập chỉ mục sẽ được sử dụng.

   .. method:: select_adjust(tagOrId, index)

      Điều chỉnh đầu cuối của vùng chọn trong *tagOrId* gần với *index* nhất để nó nằm tại *index*, đồng thời đặt đầu còn lại làm điểm neo cho các
      :meth:`select_to` lệnh tiếp theo. Nếu vùng chọn hiện không nằm trong *tagOrId*, thao tác này sẽ hoạt động như
      :meth:`select_to`.

   .. method:: select_clear()

      Xóa vùng chọn nếu nó nằm trong canvas này; nếu không thì không làm gì.

   .. method:: select_from(tagOrId, index)

      Đặt điểm neo của vùng chọn ngay trước ký tự được chỉ định bởi *index* trong mục được chỉ định bởi *tagOrId*. Thao tác này không thay đổi vùng chọn; nó đặt điểm cuối cố định cho các lệnh gọi :meth:`select_to` trong tương lai.

   .. method:: select_item()

      Trả về id của mục chứa vùng chọn hoặc ``None`` nếu vùng chọn không nằm trong canvas này. Không giống :meth:`find` và các phương thức ``find_*``, phương thức này trả về id dưới dạng chuỗi thay vì số nguyên.

   .. method:: select_to(tagOrId, index)

      Đặt vùng chọn thành các ký tự của *tagOrId* nằm giữa điểm neo của vùng chọn và *index*, bao gồm cả *index*. Điểm neo là điểm được đặt bởi lệnh gọi :meth:`select_adjust` hoặc :meth:`select_from` gần đây nhất.

   .. method:: scan_mark(x, y)

      Ghi lại *x*, *y* và chế độ xem hiện tại để sử dụng với các lệnh gọi sau này
      :meth:`scan_dragto`. Thông thường, lệnh này được liên kết với thao tác nhấn nút chuột trong widget.

   .. method:: scan_dragto(x, y, gain=10)

      Cuộn canvas theo *gain* lần hiệu giữa *x*, *y* và các tọa độ được truyền cho lệnh gọi :meth:`scan_mark` gần đây nhất. Thông thường, lệnh này được liên kết với các sự kiện di chuyển chuột trong widget, tạo ra hiệu ứng kéo canvas ở tốc độ cao qua cửa sổ của nó.

   .. method:: postscript(cnf={}, **kw)

      Tạo biểu diễn PostScript (Encapsulated PostScript, phiên bản 3.0) của một phần hoặc toàn bộ canvas. Nếu cung cấp tùy chọn *file* hoặc *channel*, PostScript sẽ được ghi vào đó và một chuỗi rỗng được trả về; nếu không, nó sẽ được trả về dưới dạng chuỗi. Theo mặc định, chỉ vùng hiện đang hiển thị trong cửa sổ được tạo, vì vậy thường cần gọi :meth:`~Misc.update` trước hoặc sử dụng các tùy chọn *width* và *height*. Các tùy chọn được hỗ trợ bao gồm *colormap*, *colormode*, *file*, *fontmap*, *height*, *pageanchor*, *pageheight*, *pagewidth*, *pagex*, *pagey*, *rotate*, *width*, *x* và *y*.


.. class:: Checkbutton(master=None, cnf={}, **kw)

   Một :class:`!Checkbutton` widget hiển thị một chuỗi văn bản, bitmap hoặc hình ảnh cùng với một ô chỉ báo hình vuông, và chuyển đổi một lựa chọn Boolean khi được nhấn. Nó có toàn bộ hành vi của một nút đơn giản và ngoài ra còn có thể được chọn: khi được chọn, ô chỉ báo được vẽ với dấu kiểm và biến liên kết được đặt thành ``onvalue``, còn khi bỏ chọn, ô chỉ báo được vẽ trống và biến được đặt thành ``offvalue``. Kế thừa từ :class:`Widget`. Ngoài các tùy chọn widget tiêu chuẩn, một checkbutton chấp nhận các tùy chọn được ghi trong trang hướng dẫn Tk ``checkbutton``, chẳng hạn như *variable*, *onvalue*, *offvalue* và *command*.

   .. method:: invoke()

      Thực hiện đúng những gì sẽ xảy ra nếu người dùng nhấn checkbutton bằng chuột: chuyển đổi trạng thái lựa chọn của nút và gọi command liên kết, nếu có. Trả về kết quả của command hoặc một chuỗi rỗng nếu checkbutton không có command liên kết. Tùy chọn này bị bỏ qua nếu trạng thái của checkbutton là ``disabled``.

   .. method:: select()

      Chọn checkbutton và đặt biến liên kết thành ``onvalue`` của nó.

   .. method:: deselect()

      Bỏ chọn checkbutton và đặt biến liên kết thành ``offvalue`` của nó.

   .. method:: toggle()

      Chuyển đổi trạng thái lựa chọn của nút, hiển thị lại nút và sửa đổi biến liên kết để phản ánh trạng thái mới.

   .. method:: flash()

      Làm nhấp nháy checkbutton bằng cách hiển thị lại nó nhiều lần, xen kẽ giữa màu active và màu normal. Khi kết thúc, checkbutton được giữ ở cùng trạng thái normal hoặc active như khi phương thức được gọi. Tùy chọn này bị bỏ qua nếu trạng thái của checkbutton là ``disabled``.


.. class:: Entry(master=None, cnf={}, **kw)

   Một widget :class:`!Entry` hiển thị một dòng văn bản và cho phép người dùng chỉnh sửa dòng đó. Widget này kế thừa từ :class:`Widget` và :class:`XView`; vì các entry có thể chứa những chuỗi quá dài không vừa trong cửa sổ, chúng hỗ trợ cuộn ngang thông qua :meth:`~XView.xview`.

   Ngoài các tùy chọn widget tiêu chuẩn, một entry chấp nhận các tùy chọn được ghi lại trong trang hướng dẫn Tk ``entry``. Các tùy chọn đáng chú ý gồm *textvariable* (tên của một biến được giữ đồng bộ với nội dung của entry), *show* (nếu được đặt, mỗi ký tự sẽ được hiển thị bằng ký tự đã cho thay vì giá trị thực của nó, hữu ích khi nhập mật khẩu), *validate* và *validatecommand* (kết hợp với nhau cho phép một callback chấp nhận hoặc từ chối các chỉnh sửa), và *state* (một trong ``'normal'``, ``'disabled'`` hoặc ``'readonly'``).

   Nhiều phương thức dưới đây nhận một đối số *index* để chọn một ký tự trong chuỗi của entry. Như được mô tả trong trang hướng dẫn Tk ``entry``, *index* có thể là một số (đếm từ 0), ``'insert'`` (ký tự ngay sau con trỏ chèn), ``'end'`` (ngay sau ký tự cuối cùng), ``'anchor'`` (điểm neo của vùng chọn), ``'sel.first'`` và ``'sel.last'`` (hai đầu của vùng chọn), hoặc ``@x`` (ký tự bao phủ tọa độ pixel x *x* trong cửa sổ). Các chỉ mục nằm ngoài phạm vi sẽ được làm tròn về giá trị hợp lệ gần nhất.

   .. method:: delete(first, last=None)

      Xóa các ký tự từ chỉ mục *first* đến trước chỉ mục *last*. Nếu bỏ qua *last*, chỉ ký tự tại *first* sẽ bị xóa.

   .. method:: get()

      Trả về chuỗi hiện tại của entry.

   .. method:: insert(index, string)

      Chèn *string* ngay trước ký tự được chỉ định bởi *index*.

   .. method:: icursor(index)

      Đặt con trỏ chèn hiển thị ngay trước ký tự được chỉ định bởi *index*.

   .. method:: index(index)

      Trả về chỉ số dạng số tương ứng với *index*.

   .. method:: select_adjust(index)
      :no-typesetting:

   .. method:: selection_adjust(index)

      Xác định đầu cuối của vùng chọn gần nhất với ký tự được xác định bởi *index*, rồi điều chỉnh đầu cuối đó về *index* (bao gồm vị trí này nhưng không vượt quá nó); đầu còn lại trở thành điểm neo cho các lần gọi
      :meth:`selection_to` trong tương lai. Nếu không có vùng chọn nào trong entry, một vùng chọn mới sẽ được tạo giữa *index* và điểm neo gần nhất, bao gồm cả hai đầu.
      :meth:`select_adjust` là bí danh của :meth:`!selection_adjust`.

   .. method:: select_clear()
      :no-typesetting:

   .. method:: selection_clear()

      Xóa vùng chọn nếu hiện tại vùng chọn nằm trong widget này. Nếu vùng chọn không nằm trong widget này, phương thức sẽ không có tác dụng.
      :meth:`select_clear` là bí danh của :meth:`!selection_clear`.

      .. note::

         Điều này che khuất :meth:`Misc.selection_clear` được kế thừa, vốn xóa vùng chọn X; phương thức đó không khả dụng trên một :class:`Entry`.

   .. method:: select_from(index)
      :no-typesetting:

   .. method:: selection_from(index)

      Đặt điểm neo của vùng chọn ngay trước ký tự được chỉ định bởi *index*, mà không thay đổi vùng chọn.
      :meth:`select_from` là bí danh của :meth:`!selection_from`.

   .. method:: select_present()
      :no-typesetting:

   .. method:: selection_present()

      Trả về ``True`` nếu có các ký tự được chọn trong entry, nếu không thì trả về ``False``.
      :meth:`select_present` là bí danh của :meth:`!selection_present`.

   .. method:: select_range(start, end)
      :no-typesetting:

   .. method:: selection_range(start, end)

      Đặt vùng chọn bao gồm các ký tự bắt đầu từ ký tự có chỉ mục *start* và kết thúc bằng ký tự ngay trước *end*. Nếu *end* trỏ đến cùng ký tự với *start* hoặc một ký tự đứng trước đó, vùng chọn sẽ bị xóa.
      :meth:`select_range` là bí danh của :meth:`!selection_range`.

   .. method:: select_to(index)
      :no-typesetting:

   .. method:: selection_to(index)

      Đặt vùng chọn giữa điểm neo và *index*: nếu *index* nằm trước điểm neo, vùng chọn sẽ chạy từ *index* đến ngay trước điểm neo; nếu *index* nằm sau điểm neo, vùng chọn sẽ chạy từ điểm neo đến ngay trước *index*; nếu chúng trùng nhau thì không có gì xảy ra. Điểm neo là điểm được thiết lập bởi lệnh gọi :meth:`selection_from` hoặc :meth:`selection_adjust` gần đây nhất. Nếu không có vùng chọn trong entry, một vùng chọn mới sẽ được tạo bằng điểm neo gần đây nhất.
      :meth:`select_to` là bí danh của :meth:`!selection_to`.

   .. method:: scan_mark(x)

      Ghi lại *x* và chế độ xem hiện tại trong cửa sổ nhập liệu để sử dụng cho các
      lệnh gọi :meth:`scan_dragto`. Thông thường được liên kết với thao tác nhấn nút chuột trong widget.

   .. method:: scan_dragto(x)

      Tính hiệu giữa *x* và *x* được truyền cho lần
      gọi :meth:`scan_mark` gần nhất, rồi điều chỉnh chế độ xem sang trái hoặc phải một khoảng bằng 10 lần hiệu đó. Thông thường được liên kết với các sự kiện chuyển động của chuột để tạo hiệu ứng kéo mục nhập qua cửa sổ với tốc độ cao.


.. class:: Frame(master=None, cnf={}, **kw)

   Một widget :class:`!Frame` là một vùng chứa đơn giản. Mục đích chính của nó là làm khoảng đệm hoặc vùng chứa cho các bố cục cửa sổ phức tạp; các tính năng duy nhất của nó là nền và đường viền 3-D tùy chọn để làm cho khung có vẻ nổi lên hoặc lõm xuống. Kế thừa từ :class:`Widget`. Tham khảo trang hướng dẫn Tk ``frame`` để xem danh sách đầy đủ các tùy chọn.


.. class:: Label(master=None, cnf={}, **kw)

   Một widget :class:`!Label` hiển thị một chuỗi văn bản, bitmap hoặc hình ảnh không tương tác. Văn bản hiển thị được thiết lập bằng tùy chọn *text* hoặc liên kết với một biến thông qua *textvariable*, và có thể hiển thị hình ảnh bằng tùy chọn *image*. Văn bản phải sử dụng cùng một font nhưng có thể trải dài trên nhiều dòng, và một ký tự có thể được gạch chân bằng tùy chọn *underline*. Kế thừa từ :class:`Widget`. Tham khảo trang hướng dẫn Tk ``label`` để xem danh sách đầy đủ các tùy chọn.


.. class:: LabelFrame(master=None, cnf={}, **kw)

   Widget :class:`!LabelFrame` là một vùng chứa có các tính năng của một
   :class:`Frame` cùng với khả năng hiển thị nhãn. Văn bản nhãn được đặt bằng tùy chọn *text* và định vị bằng *labelanchor*, hoặc có thể dùng một widget bất kỳ làm nhãn bằng cách cung cấp widget đó dưới dạng tùy chọn *labelwidget*. Kế thừa từ :class:`Widget`. Tham khảo trang hướng dẫn Tk ``labelframe`` để xem danh sách đầy đủ các tùy chọn.


.. class:: Listbox(master=None, cnf={}, **kw)

   Widget :class:`!Listbox` hiển thị danh sách các mục văn bản một dòng, mỗi mục trên một dòng, trong đó người dùng có thể chọn một hoặc nhiều mục. Cách thức hoạt động của việc chọn được điều khiển bởi tùy chọn *selectmode*, có thể là ``browse`` (mặc định; tối đa một mục, có thể được kéo bằng chuột), ``single`` (tối đa một mục), ``multiple`` (bất kỳ số lượng mục nào, được bật hoặc tắt riêng lẻ), hoặc ``extended`` (bất kỳ số lượng mục nào, bao gồm các phạm vi không liền nhau, được chọn bằng cách nhấp và kéo). Kế thừa từ :class:`Widget`, :class:`XView` và :class:`YView`, nên chế độ xem có thể được cuộn theo chiều ngang và chiều dọc bằng :meth:`~XView.xview` và :meth:`~YView.yview`. Tham khảo trang hướng dẫn Tk ``listbox`` để xem danh sách đầy đủ các tùy chọn.

   Nhiều phương thức nhận đối số *index* xác định một mục cụ thể. Như được mô tả trong trang hướng dẫn Tk ``listbox``, *index* có thể là một chỉ mục dạng số (đếm từ 0 ở đầu), ``'active'`` (mục có con trỏ vị trí, được đặt bằng :meth:`activate`), ``'anchor'`` (anchor của vùng chọn, được đặt bằng :meth:`selection_anchor`), ``'end'`` (mục cuối cùng, hoặc đối với
   :meth:`index` và :meth:`insert` là vị trí ngay sau mục đó), hoặc ``@x,y`` (mục bao phủ các tọa độ pixel *x*, *y* trong cửa sổ listbox). Các đối số có tên *first* và *last* là các chỉ mục thuộc những dạng tương tự.

   .. method:: insert(index, *elements)

      Chèn các *elements* đã cho thành các mục mới ngay trước mục được chỉ định bởi *index*. Nếu *index* là ``'end'``, các mục mới sẽ được thêm vào cuối danh sách.

   .. method:: delete(first, last=None)

      Xóa các mục trong phạm vi từ *first* đến *last*, bao gồm cả hai đầu. Nếu bỏ qua *last*, giá trị mặc định là *first*, do đó chỉ một mục sẽ bị xóa.

   .. method:: get(first, last=None)

      Nếu bỏ qua *last*, trả về nội dung của mục được chỉ định bởi *first*, hoặc một chuỗi rỗng nếu *first* trỏ đến một mục không tồn tại. Nếu cung cấp *last*, trả về một tuple gồm tất cả các mục trong phạm vi từ *first* đến *last*, bao gồm cả hai đầu mút.

   .. method:: size()

      Trả về tổng số mục trong hộp danh sách.

      Giá trị này che khuất :meth:`!Misc.size` được kế thừa; hãy sử dụng :meth:`~Misc.grid_size` để lấy kích thước grid.

   .. method:: index(index)

      Trả về giá trị chỉ mục số nguyên tương ứng với *index*, hoặc ``None`` nếu *index* nằm ngoài phạm vi. Nếu *index* là ``'end'``, kết quả là số lượng mục trong hộp danh sách (không phải chỉ mục của mục cuối cùng).

   .. method:: bbox(index)

      Trả về một tuple ``(x, y, width, height)`` mô tả bounding box, tính bằng pixel và tương đối so với widget, của văn bản thuộc mục được chỉ định bởi *index*. Trả về ``None`` nếu không có phần nào của mục đó hiển thị trên màn hình, hoặc nếu *index* trỏ đến một mục không tồn tại; nếu mục chỉ hiển thị một phần, kết quả vẫn cung cấp toàn bộ vùng của mục, bao gồm cả những phần không hiển thị.

      Phương thức này che khuất :meth:`!Misc.bbox` được kế thừa; hãy sử dụng :meth:`~Misc.grid_bbox` cho hộp giới hạn của grid.

   .. method:: nearest(y)

      Với một tọa độ y nằm trong cửa sổ hộp danh sách, trả về chỉ mục của mục đang hiển thị gần tọa độ y đó nhất.

   .. method:: see(index)

      Điều chỉnh chế độ xem để mục được chỉ định bởi *index* hiển thị. Nếu mục đó đã hiển thị, phương thức không có tác dụng; nếu mục ở gần mép cửa sổ, listbox chỉ cuộn vừa đủ để đưa mục đó vào chế độ xem tại mép ấy; nếu không, listbox cuộn để đưa mục vào giữa.

   .. method:: activate(index)

      Đặt mục đang hoạt động thành mục được chỉ định bởi *index*. Nếu *index* nằm ngoài phạm vi các mục, mục gần nhất sẽ được kích hoạt thay thế. Mục đang hoạt động được vẽ theo quy định của tùy chọn *activestyle* khi widget nhận input focus, và có thể lấy chỉ số của mục này bằng ``'active'`` index.

   .. method:: curselection()

      Trả về một tuple chứa các chỉ số dạng số của tất cả mục hiện đang được chọn, hoặc một tuple rỗng nếu không có mục nào được chọn.

   .. method:: select_anchor(index)
      :no-typesetting:

   .. method:: selection_anchor(index)

      Đặt selection anchor thành mục được chỉ định bởi *index*. Nếu *index* tham chiếu đến một mục không tồn tại, mục gần nhất sẽ được sử dụng. Selection anchor là đầu cuối của vùng chọn được cố định khi kéo để mở rộng vùng chọn bằng chuột, và sau đó có thể được tham chiếu bằng ``'anchor'`` index.
      :meth:`select_anchor` là bí danh của :meth:`!selection_anchor`.

   .. method:: select_clear(first, last=None)
      :no-typesetting:

   .. method:: selection_clear(first, last=None)

      Bỏ chọn mọi mục đang được chọn trong phạm vi từ *first* đến *last*, bao gồm cả hai đầu. Trạng thái chọn của các mục nằm ngoài phạm vi này không thay đổi.
      :meth:`select_clear` là bí danh của :meth:`!selection_clear`.

      .. note::

         Điều này che khuất :meth:`Misc.selection_clear` được kế thừa, vốn xóa vùng chọn X; phương thức đó không khả dụng trên một :class:`Listbox`.

   .. method:: select_includes(index)
      :no-typesetting:

   .. method:: selection_includes(index)

      Trả về ``True`` nếu mục được chỉ định bởi *index* hiện đang được chọn, ``False`` nếu không.
      :meth:`select_includes` là bí danh của :meth:`!selection_includes`.

   .. method:: select_set(first, last=None)
      :no-typesetting:

   .. method:: selection_set(first, last=None)

      Chọn tất cả các mục trong phạm vi từ *first* đến *last*, bao gồm cả hai đầu, mà không ảnh hưởng đến trạng thái chọn của các mục nằm ngoài phạm vi đó.
      :meth:`select_set` là bí danh của :meth:`!selection_set`.

   .. method:: itemcget(index, option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option* cho mục được chỉ định bởi *index*.

   .. method:: itemconfig(index, cnf=None, **kw)
      :no-typesetting:

   .. method:: itemconfigure(index, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của mục được chỉ định bởi *index*. Điều này phản ánh :meth:`~Misc.configure`, ngoại trừ việc nó áp dụng cho từng mục riêng lẻ thay vì toàn bộ listbox. Khi không có tùy chọn nào, nó trả về một từ điển mô tả các tùy chọn hiện tại của mục; nếu không, nó đặt các tùy chọn được cung cấp. Các tùy chọn mục được hỗ trợ là *background*, *foreground*, *selectbackground* và *selectforeground*.
      :meth:`itemconfig` là bí danh của :meth:`!itemconfigure`.

   .. method:: scan_mark(x, y)

      Ghi lại *x*, *y* và chế độ xem hiện tại để sử dụng với các lệnh gọi sau này
      :meth:`scan_dragto`. Thông thường, lệnh này được liên kết với thao tác nhấn nút chuột trong widget.

   .. method:: scan_dragto(x, y)

      Cuộn listbox một khoảng bằng 10 lần chênh lệch giữa *x*, *y* và các tọa độ được truyền vào lần gọi :meth:`scan_mark` gần nhất. Thao tác này thường được liên kết với các sự kiện chuyển động chuột trong widget, tạo ra hiệu ứng kéo danh sách qua cửa sổ với tốc độ cao.


.. class:: Menu(master=None, cnf={}, **kw)

   Một widget :class:`!Menu` hiển thị một cột các mục, mỗi mục có thể là một command, checkbutton, radiobutton, cascade (hiển thị một submenu liên kết) hoặc separator. Menu được dùng làm menubar của cửa sổ toplevel, làm pulldown menu được hiển thị từ một mục cascade hoặc menubutton, và làm popup menu. Kế thừa từ :class:`Widget`.

   Nhiều phương thức của entry nhận một đối số *index* để chọn entry cần thao tác. Như được mô tả trong trang hướng dẫn Tk ``menu``, *index* có thể là một chỉ mục số (đếm từ 0 ở trên cùng), ``'active'`` (entry hiện đang active), ``'end'`` hoặc ``'last'`` (entry ở dưới cùng), ``'none'`` (không có entry nào, được viết là ``{}`` trong Tcl), ``@y`` (entry bao phủ tọa độ pixel y *y* trong cửa sổ menu), hoặc một mẫu được đối chiếu với nhãn của các entry từ trên xuống.

   .. method:: add(itemType, cnf={}, **kw)

      Thêm một entry mới vào cuối menu. *itemType* là một trong ``'command'``, ``'cascade'``, ``'checkbutton'``, ``'radiobutton'`` hoặc ``'separator'`` và xác định loại entry mới; các tùy chọn còn lại sẽ cấu hình entry đó. :meth:`!add_command`, :meth:`!add_cascade`, :meth:`!add_checkbutton`,
      Các phương thức tiện ích :meth:`!add_radiobutton` và :meth:`!add_separator` gọi phương thức này với *itemType* tương ứng.

      Mục nhập được cấu hình bằng các tùy chọn sau, mặc dù không phải tùy chọn nào cũng áp dụng cho mọi loại mục nhập (separator không chấp nhận tùy chọn nào trong số đó):

      *label*
         Văn bản sẽ hiển thị trong mục nhập.

      *command*
         Hàm sẽ được gọi khi mục nhập được kích hoạt (các mục nhập command, checkbutton và radiobutton).

      *accelerator*
         Một chuỗi được hiển thị ở bên phải mục nhập để quảng bá một phím tắt; bản thân chuỗi này không tạo liên kết phím.

      *underline*
         Chỉ mục của một ký tự trong nhãn cần gạch dưới để duyệt bằng bàn phím.

      *state*
         Một trong ``'normal'``, ``'active'`` hoặc ``'disabled'``.

      *image*
         Một hình ảnh được hiển thị thay cho hoặc cùng với nhãn văn bản.

      *compound*
         Vị trí hiển thị hình ảnh so với văn bản: ``'none'`` (mặc định), ``'text'``, ``'image'``, ``'top'``, ``'bottom'``, ``'left'`` hoặc ``'right'``.

      *bitmap*
         Một bitmap để hiển thị thay cho nhãn văn bản.

      *font*
         Phông chữ dùng cho văn bản.

      *background*, *foreground*
         Màu nền và màu chữ của entry ở trạng thái bình thường (bị bỏ qua trên macOS).

      *activebackground*, *activeforeground*
         Màu nền và màu chữ được sử dụng khi entry đang hoạt động (bị bỏ qua trên macOS).

      *columnbreak*
         Nếu là true, entry sẽ bắt đầu một cột mới thay vì được đặt bên dưới entry trước đó.

      *hidemargin*
         Nếu là true, phần lề tiêu chuẩn xung quanh entry sẽ bị bỏ qua, điều này hữu ích khi menu được dùng làm palette.

      *menu*
         Menu con do một mục cascade đăng lên; nó phải là con của menu này.

      *variable*
         Biến được liên kết với một mục checkbutton hoặc radiobutton.

      *onvalue*, *offvalue*
         Các giá trị được lưu trong *variable* khi một mục checkbutton được chọn hoặc bỏ chọn.

      *value*
         Giá trị được lưu trong *variable* khi một mục radiobutton được chọn.

      *indicatoron*
         Có hiển thị indicator của mục checkbutton hoặc radiobutton hay không.

      *selectcolor*
         Màu của indicator của mục checkbutton hoặc radiobutton khi mục đó được chọn.

      *selectimage*
         Ảnh được hiển thị khi một mục checkbutton hoặc radiobutton được chọn và *image* cũng được cung cấp.

   .. method:: add_cascade(cnf={}, **kw)

      Thêm một mục cascade mới vào cuối menu. Một mục cascade có submenu liên kết, được chỉ định bởi tùy chọn *menu* của mục đó; tùy chọn này phải là một mục con của menu hiện tại. Khi đăng mục, submenu sẽ được đăng bên cạnh mục đó.

   .. method:: add_checkbutton(cnf={}, **kw)

      Thêm một mục checkbutton mới vào cuối menu. Khi được gọi, mục checkbutton chuyển đổi giữa *onvalue* và *offvalue*, lưu kết quả vào *variable* liên kết với nó, đồng thời hiển thị một chỉ báo cho biết mục đó có được chọn hay không.

   .. method:: add_command(cnf={}, **kw)

      Thêm một mục command mới vào cuối menu. Mục command hoạt động gần giống một button: khi được gọi, callback được chỉ định bởi tùy chọn *command* của mục đó sẽ được gọi.

   .. method:: add_radiobutton(cnf={}, **kw)

      Thêm một mục radiobutton mới vào cuối menu. Các mục radiobutton dùng chung *variable* sẽ tạo thành một nhóm mà tại mỗi thời điểm chỉ có một mục được chọn; khi chọn một mục, *value* của mục đó sẽ được lưu vào biến.

   .. method:: add_separator(cnf={}, **kw)

      Thêm một dấu phân cách vào cuối menu. Dấu phân cách được hiển thị dưới dạng một đường ngang và không thể được kích hoạt hoặc gọi.

   .. method:: insert(index, itemType, cnf={}, **kw)

      Giống :meth:`add`, ngoại trừ mục mới được chèn ngay trước mục được chỉ định bởi *index* thay vì được thêm vào cuối menu. *itemType* là một trong các giá trị ``'command'``, ``'cascade'``, ``'checkbutton'``, ``'radiobutton'`` hoặc ``'separator'``. :meth:`!insert_command`, :meth:`!insert_cascade`,
      :meth:`!insert_checkbutton`, :meth:`!insert_radiobutton` và
      Các phương thức tiện ích :meth:`!insert_separator` gọi phương thức này với *itemType* tương ứng.

   .. method:: insert_cascade(index, cnf={}, **kw)

      Chèn một mục cascade mới trước mục được chỉ định bởi *index* (xem
      :meth:`add_cascade`).

   .. method:: insert_checkbutton(index, cnf={}, **kw)

      Chèn một mục checkbutton mới trước mục được chỉ định bởi *index* (xem
      :meth:`add_checkbutton`).

   .. method:: insert_command(index, cnf={}, **kw)

      Chèn một mục command mới trước mục được chỉ định bởi *index* (xem
      :meth:`add_command`).

   .. method:: insert_radiobutton(index, cnf={}, **kw)

      Chèn một mục radiobutton mới trước mục được chỉ định bởi *index* (xem
      :meth:`add_radiobutton`).

   .. method:: insert_separator(index, cnf={}, **kw)

      Chèn một dấu phân cách trước mục được chỉ định bởi *index* (xem
      :meth:`add_separator`).

   .. method:: delete(index1, index2=None)

      Xóa tất cả các mục menu giữa *index1* và *index2*, bao gồm cả hai mục này. Nếu *index2* bị bỏ qua, giá trị mặc định là *index1*, do đó một mục duy nhất sẽ bị xóa. Các nỗ lực xóa mục tear-off sẽ bị bỏ qua; hãy xóa mục đó bằng cách thay đổi tùy chọn *tearoff*.

   .. method:: entrycget(index, option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option* cho mục nhập được chỉ định bởi *index*.

   .. method:: entryconfig(index, cnf=None, **kw)
      :no-typesetting:

   .. method:: entryconfigure(index, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của mục nhập được chỉ định bởi *index*. Điều này phản chiếu :meth:`~Misc.configure`, ngoại trừ việc nó áp dụng cho một mục nhập riêng lẻ thay vì toàn bộ menu. Khi không có tùy chọn nào, hàm trả về một từ điển mô tả các tùy chọn hiện tại của mục nhập; nếu không, hàm sẽ đặt các tùy chọn đã cho. Các tùy chọn được hỗ trợ là những tùy chọn được :meth:`add` chấp nhận cho loại mục nhập đó.
      :meth:`entryconfig` là bí danh của :meth:`!entryconfigure`.

   .. method:: index(index)

      Trả về chỉ mục số tương ứng với *index*, hoặc ``None`` nếu *index* không chọn mục nhập nào.

   .. method:: type(index)

      Trả về loại của mục nhập được chỉ định bởi *index*: một trong các loại ``'command'``, ``'cascade'``, ``'checkbutton'``, ``'radiobutton'``, ``'separator'`` hoặc ``'tearoff'`` (đối với mục nhập tear-off).

   .. method:: activate(index)

      Đặt mục nhập được chỉ định bởi *index* làm mục nhập hiện hoạt, hiển thị lại mục nhập đó bằng các màu hiện hoạt và hủy kích hoạt mọi mục nhập hiện hoạt trước đó. Nếu *index* không chọn mục nhập nào hoặc mục nhập được chọn bị vô hiệu hóa, menu sẽ không còn mục nhập hiện hoạt nào.

   .. method:: invoke(index)

      Gọi hành động của mục nhập được chỉ định bởi *index*, như thể mục nhập đó đã được nhấp. Sẽ không có gì xảy ra nếu mục nhập bị vô hiệu hóa. Nếu mục nhập có *command* liên kết với nó, kết quả của command đó sẽ được trả về; nếu không, kết quả là một chuỗi rỗng.

   .. method:: post(x, y)

      Hiển thị menu trên màn hình tại các tọa độ của cửa sổ gốc *x* và *y*, điều chỉnh các tọa độ này nếu cần để toàn bộ menu hiển thị được. Nếu tùy chọn *postcommand* được chỉ định, tùy chọn này sẽ được đánh giá trước khi menu được hiển thị.

   .. method:: tk_popup(x, y, entry='')

      Hiển thị menu dưới dạng popup tại các tọa độ của cửa sổ gốc *x* và *y*. Nếu chỉ định *entry*, menu sẽ được định vị sao cho mục này hiển thị bên dưới con trỏ.

   .. method:: unpost()

      Bỏ ánh xạ menu để menu không còn được hiển thị, đồng thời bỏ hiển thị mọi menu con dạng cascade cấp thấp hơn đang được hiển thị. Việc này không ảnh hưởng đến Windows và macOS, vì các hệ điều hành này tự quản lý việc bỏ hiển thị menu.

   .. method:: xposition(index)

      Trả về tọa độ x, trong cửa sổ menu, của pixel ngoài cùng bên trái của mục được chỉ định bởi *index*.

      .. versionadded:: 3.3

   .. method:: yposition(index)

      Trả về tọa độ y, trong cửa sổ menu, của pixel trên cùng của mục được chỉ định bởi *index*.


.. class:: Menubutton(master=None, cnf={}, **kw)

   Một widget :class:`!Menubutton` hiển thị một chuỗi văn bản, bitmap hoặc hình ảnh, đồng thời hiển thị :class:`Menu` liên kết với nó, được chỉ định bởi tùy chọn *menu*, khi người dùng nhấn vào widget. Giống như :class:`Label`, widget này có thể hiển thị *text*, *textvariable* hoặc *image*, và tùy chọn *direction* kiểm soát vị trí menu so với nút. Kế thừa từ :class:`Widget`. Tham khảo trang hướng dẫn Tk ``menubutton`` để xem danh sách đầy đủ các tùy chọn.


.. class:: Message(master=None, cnf={}, **kw)

   Một widget :class:`!Message` hiển thị một chuỗi văn bản không tương tác, được chỉ định bởi tùy chọn *text* hoặc liên kết với một biến thông qua *textvariable*. Không giống :class:`Label`, widget này ngắt chuỗi thành nhiều dòng để tạo ra một tỷ lệ khung hình nhất định, chọn vị trí ngắt dòng tại ranh giới giữa các từ, đồng thời có thể căn văn bản sang trái, giữa hoặc phải. Kế thừa từ :class:`Widget`. Tham khảo trang hướng dẫn Tk ``message`` để xem danh sách đầy đủ các tùy chọn.


.. class:: OptionMenu(master, variable, value, *values, **kwargs)

   Một lớp con trợ giúp của :class:`Menubutton`, dùng để hiển thị menu bật lên gồm các lựa chọn loại trừ lẫn nhau. *variable* là một :class:`Variable` được giữ đồng bộ với lựa chọn, *value* là lựa chọn ban đầu, còn *values* là các mục còn lại trong menu. Đối số từ khóa *command* có thể nhận một callback được gọi với giá trị đã chọn, còn đối số từ khóa *name* thiết lập tên widget Tk.

   .. method:: destroy()

      Hủy widget, đồng thời dọn dẹp menu bật lên liên kết với widget.

   .. versionchanged:: 3.14
      Đã bổ sung hỗ trợ cho đối số từ khóa *name*.



.. class:: PanedWindow(master=None, cnf={}, **kw)

   :class:`!PanedWindow` là một widget geometry-manager sắp xếp bất kỳ số lượng *panes* con nào thành một hàng (khi *orient* là ``'horizontal'``) hoặc một cột (khi *orient* là ``'vertical'``). Mỗi pane chứa một widget, và mỗi cặp pane liền kề được ngăn cách bởi một *sash* có thể di chuyển; người dùng có thể kéo sash bằng chuột để thay đổi kích thước các widget ở hai bên. Kế thừa từ :class:`Widget`.

   Tùy chọn *orient* chọn hướng bố cục, *sashwidth* đặt chiều rộng của mỗi sash, còn *sashrelief* đặt kiểu nổi của sash. Khi *showhandle* là true, một tay nắm nhỏ được vẽ trên mỗi sash để người dùng có thể nắm và kéo sash. Tham khảo trang hướng dẫn Tk ``panedwindow`` để xem danh sách đầy đủ các tùy chọn.

   .. method:: add(child, **kw)

      Thêm *child* vào panedwindow dưới dạng pane mới, đặt sau tất cả các pane hiện có. Các đối số từ khóa chỉ định các tùy chọn quản lý riêng cho từng pane của *child*; chúng có thể là bất kỳ tùy chọn nào được :meth:`paneconfigure` chấp nhận.

   .. method:: forget(child)
      :no-typesetting:

   .. method:: remove(child)

      Xóa pane chứa *child* khỏi panedwindow. Tất cả tùy chọn quản lý hình học cho *child* sẽ bị quên.
      :meth:`forget` là bí danh của :meth:`!remove`. Nó che khuất geometry-manager được kế thừa :meth:`!forget`; hãy sử dụng :meth:`~Pack.pack_forget`, :meth:`~Grid.grid_forget` hoặc
      :meth:`~Place.place_forget` để xóa chính widget khỏi trình quản lý của nó.

   .. method:: panes()

      Trả về một tuple gồm các widget do panedwindow quản lý, mỗi pane một widget, theo đúng thứ tự.

   .. method:: panecget(child, option)

      Trả về giá trị hiện tại của tùy chọn quản lý *option* cho pane chứa *child*. *option* có thể là bất kỳ giá trị nào được :meth:`paneconfigure` cho phép.

   .. method:: paneconfig(tagOrId, cnf=None, **kw)
      :no-typesetting:

   .. method:: paneconfigure(tagOrId, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn quản lý của pane chứa widget *tagOrId*. Khi không có tùy chọn nào, trả về một dictionary mô tả tất cả tùy chọn hiện có của pane; khi được cung cấp một tên tùy chọn duy nhất dưới dạng chuỗi, trả về mô tả của tùy chọn đó; nếu không, đặt các tùy chọn đã cho. Các tùy chọn được hỗ trợ bao gồm *after* và *before* (chèn pane sau hoặc trước một cửa sổ khác đang được quản lý), *height* và *width* (kích thước bên ngoài của cửa sổ, bao gồm cả đường viền), *minsize* (kích thước tối thiểu theo chiều paned), *padx* và *pady* (khoảng trống bổ sung để chừa ở mỗi bên của cửa sổ), *sticky* (định vị hoặc kéo giãn cửa sổ trong một pane lớn hơn kích thước cần thiết, bằng chuỗi gồm các ký tự ``n``, ``s``, ``e`` và ``w``), *hide* (ẩn pane nhưng vẫn giữ pane trong danh sách các pane) và *stretch* (cách phân bổ khoảng trống bổ sung cho pane: một trong ``'always'``, ``'first'``, ``'last'``, ``'middle'`` hoặc ``'never'``).
      :meth:`paneconfig` là bí danh của :meth:`!paneconfigure`.

   .. method:: identify(x, y)

      Xác định thành phần panedwindow nằm bên dưới điểm được cho bởi *x* và *y*, trong tọa độ cửa sổ. Nếu điểm nằm trên một sash hoặc tay cầm sash, kết quả là một tuple gồm hai phần tử chứa chỉ mục của sash hoặc tay cầm và một từ cho biết điểm nằm trên sash hay tay cầm, chẳng hạn như ``(0, 'sash')`` hoặc ``(2, 'handle')``. Nếu điểm nằm trên bất kỳ phần nào khác của panedwindow, kết quả là một chuỗi rỗng.

   .. method:: sash(*args)

      Truy vấn hoặc thay đổi vị trí của các sash trong panedwindow. Đây là một lớp bao bọc mỏng quanh subcommand ``sash`` của Tk; thông thường nên sử dụng các phương thức tiện ích :meth:`sash_coord`, :meth:`sash_mark` và :meth:`sash_place` thay thế.

   .. method:: sash_coord(index)

      Trả về cặp tọa độ x và y hiện tại của sash được chỉ định bởi *index*, phải là một số nguyên từ 0 đến nhỏ hơn một đơn vị so với số ngăn trong panedwindow. Các tọa độ được trả về là tọa độ góc trên bên trái của vùng chứa sash.

   .. method:: sash_mark(index)

      Ghi lại vị trí chuột hiện tại của sash được chỉ định bởi *index*, để sử dụng cùng với các thao tác kéo sash về sau nhằm di chuyển sash.

   .. method:: sash_place(index, x, y)

      Đặt sash được chỉ định bởi *index* tại các tọa độ *x* và *y*.

   .. method:: proxy(*args)

      Truy vấn hoặc thay đổi vị trí của proxy sash, tức sash "bóng ma" được hiển thị khi sash đang được kéo với thao tác thay đổi kích thước không đục. Đây là một lớp bao bọc mỏng quanh subcommand ``proxy`` của Tk; thông thường nên sử dụng các phương thức tiện ích :meth:`proxy_coord`, :meth:`proxy_forget` và
      :meth:`proxy_place` thay thế.

   .. method:: proxy_coord()

      Trả về một tuple chứa tọa độ x và y của vị trí proxy gần đây nhất.

   .. method:: proxy_forget()

      Xóa proxy khỏi phần hiển thị.

   .. method:: proxy_place(x, y)

      Đặt proxy tại tọa độ *x* và *y*.


.. class:: Radiobutton(master=None, cnf={}, **kw)

   Một widget :class:`!Radiobutton` hiển thị một chuỗi văn bản, bitmap hoặc hình ảnh cùng với một chỉ báo hình thoi hoặc hình tròn, đồng thời chọn một lựa chọn trong số nhiều lựa chọn. Widget này có toàn bộ hành vi của một nút đơn giản và ngoài ra còn có thể được chọn: thông thường, một số radiobutton dùng chung một *variable*, và việc chọn một radiobutton sẽ đặt biến đó thành *value* của radiobutton; mỗi radiobutton cũng theo dõi biến này và tự động chọn hoặc bỏ chọn chính nó khi biến thay đổi. Kế thừa từ :class:`Widget`. Ngoài các tùy chọn widget tiêu chuẩn, radiobutton chấp nhận các tùy chọn được mô tả trong trang hướng dẫn Tk ``radiobutton``, chẳng hạn như *variable*, *value* và *command*.

   .. method:: invoke()

      Thực hiện chính xác những gì sẽ xảy ra nếu người dùng nhấn radiobutton bằng chuột: chọn nút và gọi command liên kết, nếu có. Trả về kết quả của command hoặc một chuỗi rỗng nếu radiobutton không liên kết với command nào. Tùy chọn này bị bỏ qua nếu trạng thái của radiobutton là ``disabled``.

   .. method:: select()

      Chọn radiobutton và đặt biến liên kết thành giá trị tương ứng với widget này.

   .. method:: deselect()

      Bỏ chọn radiobutton và đặt biến liên kết thành một chuỗi rỗng. Nếu radiobutton này hiện không được chọn, thao tác này không có tác dụng.

   .. method:: flash()

      Làm nhấp nháy radiobutton bằng cách hiển thị lại nó nhiều lần, xen kẽ giữa các màu active và normal. Khi kết thúc, radiobutton được giữ ở cùng trạng thái normal hoặc active như lúc phương thức được gọi. Tùy chọn này bị bỏ qua nếu trạng thái của radiobutton là ``disabled``.


.. class:: Scale(master=None, cnf={}, **kw)

   Một widget :class:`!Scale` cho phép người dùng chọn một giá trị số bằng cách di chuyển thanh trượt dọc theo rãnh. Widget này có thể được định hướng theo chiều dọc hoặc chiều ngang, đồng thời có thể tùy chọn hiển thị nhãn và giá trị hiện tại. Kế thừa từ :class:`Widget`.

   Ngoài các tùy chọn widget tiêu chuẩn, scale chấp nhận các tùy chọn được mô tả trong trang hướng dẫn Tk ``scale``, chẳng hạn như *from_*, *to*, *resolution*, *orient*, *tickinterval*, *variable* và *command*. Cũng như ở những nơi khác trong :mod:`!tkinter`, ký tự đầu ``-`` của tên tùy chọn Tk được lược bỏ; *from* được viết thành ``from_`` vì :keyword:`from` là một từ khóa Python.

   Với *resolution* không phải số nguyên, hãy xem :ref:`giá trị số và locale <tkinter-numeric-locale>`.

   .. method:: get()

      Trả về giá trị hiện tại của scale. Kết quả là một số nguyên nếu *resolution* của scale tạo ra các số nguyên, và là một số thực trong trường hợp ngược lại.

   .. method:: set(value)

      Đặt scale thành *value*, đồng thời di chuyển thanh trượt tương ứng. Việc này không có tác dụng nếu scale bị vô hiệu hóa.

   .. method:: coords(value=None)

      Trả về một tuple ``(x, y)`` chứa tọa độ pixel, tương đối so với widget, của điểm trên đường trung tâm của rãnh tương ứng với *value*. Nếu bỏ qua *value*, giá trị hiện tại của scale sẽ được sử dụng.

   .. method:: identify(x, y)

      Trả về một chuỗi mô tả phần của scale tại tọa độ pixel *x*, *y*: ``'slider'``, ``'trough1'`` (phần rãnh nằm phía trên hoặc bên trái thanh trượt), ``'trough2'`` (phía dưới hoặc bên phải thanh trượt), hoặc một chuỗi rỗng nếu điểm đó không nằm trên bất kỳ thành phần nào trong số này.


.. class:: Scrollbar(master=None, cnf={}, **kw)

   Một widget :class:`!Scrollbar` hiển thị một thanh trượt và hai mũi tên, cho phép người dùng cuộn một widget liên kết, chẳng hạn như :class:`Listbox`, :class:`Text`,
   :class:`Canvas` hoặc :class:`Entry`. Widget này được kết nối với widget được cuộn bằng cách đặt tùy chọn *xscrollcommand* hoặc *yscrollcommand* của widget đó thành phương thức :meth:`set` của thanh cuộn, và tùy chọn *command* của thanh cuộn thành phương thức của widget được cuộn
   :meth:`~XView.xview` hoặc :meth:`~YView.yview`. Kế thừa từ :class:`Widget`.

   .. method:: get()

      Trả về các thiết lập hiện tại của thanh cuộn dưới dạng một tuple ``(first, last)`` gồm hai phân số từ 0 đến 1, mô tả phần tài liệu hiện đang hiển thị, như được truyền lần cuối cho :meth:`set`.

   .. method:: set(first, last)

      Thiết lập thanh cuộn. *first* và *last* là các phân số từ 0 đến 1, biểu thị vị trí bắt đầu và kết thúc của phần tài liệu liên kết đang hiển thị. Phương thức này thường được đăng ký làm *xscrollcommand* hoặc *yscrollcommand* của widget được cuộn và được widget đó gọi.

   .. method:: activate(index=None)

      Đánh dấu phần tử *index* (một trong ``'arrow1'``, ``'slider'`` hoặc ``'arrow2'``) là đang hoạt động và hiển thị phần tử đó theo các tùy chọn *activebackground* và *activerelief*. Nếu bỏ qua *index*, trả về tên của phần tử hiện đang hoạt động hoặc ``None`` nếu không có phần tử nào đang hoạt động.

      .. versionchanged:: 3.5
         Đối số *index* hiện là tùy chọn.

   .. method:: delta(deltax, deltay)

      Trả về một số thực biểu thị mức thay đổi phân số trong thiết lập thanh cuộn tương ứng với việc di chuyển thanh trượt theo chiều ngang *deltax* pixel (đối với thanh cuộn ngang) hoặc theo chiều dọc *deltay* pixel (đối với thanh cuộn dọc).

   .. method:: fraction(x, y)

      Trả về một số thực từ 0 đến 1 cho biết vị trí của điểm tại tọa độ pixel *x*, *y* trong rãnh: 0 tương ứng với đầu trên hoặc bên trái của rãnh, còn 1 tương ứng với đầu dưới hoặc bên phải.

   .. method:: identify(x, y)

      Trả về tên của phần tử bên dưới tọa độ pixel *x*, *y* (chẳng hạn như ``'arrow1'``), hoặc một chuỗi rỗng nếu điểm đó không nằm trong bất kỳ phần tử nào của thanh cuộn.


.. class:: Spinbox(master=None, cnf={}, **kw)

   Một widget :class:`!Spinbox` là widget tương tự :class:`Entry`, có một cặp nút mũi tên lên/xuống cho phép người dùng duyệt từng bước qua một dải giá trị, bên cạnh việc chỉnh sửa trực tiếp giá trị. Tập giá trị có thể là một dải số được xác định bởi các tùy chọn *from_*, *to* và *increment*, hoặc một danh sách chuỗi rõ ràng được xác định bởi tùy chọn *values* (tùy chọn này được ưu tiên hơn dải giá trị). Mỗi khi một mũi tên được kích hoạt, callback *command*, nếu có, sẽ được gọi; tùy chọn *wrap* kiểm soát việc khi bước qua một đầu của dải thì có quay vòng về đầu kia hay không; tùy chọn *format* chỉ định cách định dạng các giá trị số; và tùy chọn *validate* cho phép xác thực văn bản đã nhập. Kế thừa từ :class:`Widget` và :class:`XView`.

   Với *increment* không phải số nguyên, hãy xem :ref:`numeric values and the locale <tkinter-numeric-locale>`.

   Nhiều phương thức nhận một đối số *index* xác định một ký tự trong chuỗi của spinbox. Như được mô tả trong trang hướng dẫn Tk ``spinbox``, *index* có thể là một chỉ mục số (đếm từ 0), ``'anchor'`` (điểm neo của vùng chọn), ``'end'`` (ngay sau ký tự cuối cùng), ``'insert'`` (ký tự ngay sau con trỏ chèn), ``'sel.first'`` hoặc ``'sel.last'`` (các đầu của vùng chọn), hoặc ``@x`` (ký tự bao phủ tọa độ pixel x *x* trong cửa sổ).

   .. method:: get()

      Trả về chuỗi của spinbox.

   .. method:: insert(index, s)

      Chèn các ký tự của chuỗi *s* ngay trước ký tự được xác định bởi *index*.

   .. method:: delete(first, last=None)

      Xóa một hoặc nhiều ký tự khỏi spinbox. *first* là chỉ mục của ký tự đầu tiên cần xóa, còn *last* là chỉ mục của ký tự ngay sau ký tự cuối cùng cần xóa. Nếu bỏ qua *last*, một ký tự duy nhất tại *first* sẽ bị xóa.

   .. method:: icursor(index)

      Đặt con trỏ chèn hiển thị ngay trước ký tự được chỉ định bởi *index*.

   .. method:: index(index)

      Trả về chỉ mục số tương ứng với *index*, dưới dạng chuỗi.

   .. method:: bbox(index)

      Trả về một tuple gồm bốn số nguyên ``(x, y, width, height)`` mô tả hộp giới hạn của ký tự được xác định bởi *index*. *x* và *y* là tọa độ pixel của góc trên bên trái của ký tự tính tương đối với widget, còn *width* và *height* là kích thước của ký tự tính bằng pixel. Hộp giới hạn có thể trỏ đến một vùng nằm ngoài khu vực hiển thị của cửa sổ.

      Phương thức này che khuất :meth:`!Misc.bbox` được kế thừa; hãy sử dụng :meth:`~Misc.grid_bbox` cho hộp giới hạn của grid.

   .. method:: identify(x, y)

      Trả về tên của phần tử cửa sổ tại tọa độ pixel *x*, *y*: một trong ``'buttondown'``, ``'buttonup'``, ``'entry'`` hoặc ``'none'``.

   .. method:: invoke(element)

      Gọi spin button được chỉ định bởi *element*, với ``'buttonup'`` hoặc ``'buttondown'``, để kích hoạt hành động liên kết với nó.

   .. method:: scan(*args)

      Một lớp bao bọc mỏng quanh lệnh con widget Tk ``scan``, được dùng để triển khai thao tác kéo nhanh chế độ xem: ``scan('mark', x)`` ghi lại *x* và chế độ xem hiện tại, còn ``scan('dragto', x)`` điều chỉnh chế độ xem tương đối so với điểm đánh dấu đó. Các phương thức :meth:`scan_mark` và :meth:`scan_dragto` bao bọc hai dạng này.

   .. method:: scan_mark(x)

      Ghi lại *x* và chế độ xem hiện tại trong cửa sổ spinbox để sử dụng với lệnh gọi :meth:`scan_dragto` sau đó. Thông thường, thao tác này được liên kết với sự kiện nhấn nút chuột trong widget.

   .. method:: scan_dragto(x)

      Điều chỉnh chế độ xem bằng 10 lần hiệu giữa *x* và *x* được truyền cho lệnh gọi :meth:`scan_mark` gần nhất. Thông thường, thao tác này được liên kết với các sự kiện chuyển động của chuột, tạo hiệu ứng kéo spinbox qua cửa sổ với tốc độ cao.

   .. method:: selection(*args)

      Một lớp bao bọc mỏng quanh lệnh con widget Tk ``selection``, được dùng để điều chỉnh vùng chọn trong spinbox. Nó có nhiều dạng tùy thuộc vào đối số đầu tiên, chẳng hạn như ``selection('adjust', index)``, ``selection('clear')``, ``selection('element', ?elem?)``, ``selection('from', index)``, ``selection('present')``, ``selection('range', start, end)`` và ``selection('to', index)``. Các phương thức :meth:`selection_adjust`, :meth:`selection_clear`,
      :meth:`selection_element`, :meth:`selection_from`,
      :meth:`selection_present`, :meth:`selection_range` và
      các phương thức :meth:`selection_to` bao bọc những dạng này.

   .. method:: selection_adjust(index)

      Xác định đầu của vùng chọn gần ký tự được chỉ định bởi *index* nhất và điều chỉnh đầu đó của vùng chọn đến *index* (bao gồm nhưng không vượt quá *index*). Đầu còn lại trở thành điểm neo cho các lệnh gọi :meth:`selection_to` trong tương lai. Nếu hiện tại vùng chọn không nằm trong spinbox, một vùng chọn mới sẽ được tạo để bao gồm các ký tự giữa *index* và điểm neo gần nhất, tính cả hai đầu.

   .. method:: selection_clear()

      Xóa vùng chọn nếu hiện tại nó nằm trong widget này. Nếu vùng chọn không nằm trong widget này, phương thức không có tác dụng.

      .. note::

         Phương thức này che khuất :meth:`Misc.selection_clear` được kế thừa, vốn xóa vùng chọn X; phương thức đó không khả dụng trên :class:`Spinbox`.

   .. method:: selection_element(element=None)

      Đặt hoặc lấy phần tử hiện được chọn. Nếu *element* (một trong ``'buttonup'``, ``'buttondown'`` hoặc ``'none'``) được cung cấp, nút spin đó sẽ được chọn và hiển thị ở trạng thái nhấn; nếu không, tên của phần tử hiện được chọn sẽ được trả về.

   .. method:: selection_from(index)

      Đặt điểm neo của vùng chọn ngay trước ký tự được chỉ định bởi *index*, mà không thay đổi chính vùng chọn.

      .. versionadded:: 3.8


   .. method:: selection_present()

      Trả về ``True`` nếu có các ký tự được chọn trong spinbox, nếu không thì trả về ``False``.

      .. versionadded:: 3.8


   .. method:: selection_range(start, end)

      Đặt vùng chọn bao gồm các ký tự bắt đầu từ ký tự có chỉ mục *start* và kết thúc bằng ký tự ngay trước *end*. Nếu *end* trỏ đến cùng ký tự với *start* hoặc một ký tự đứng trước đó, vùng chọn sẽ bị xóa.

      .. versionadded:: 3.8


   .. method:: selection_to(index)

      Đặt vùng chọn giữa *index* và điểm neo. Nếu *index* nằm trước điểm neo, vùng chọn chạy từ *index* đến nhưng không bao gồm điểm neo; nếu nằm sau, vùng chọn chạy từ điểm neo đến nhưng không bao gồm *index*; nếu trùng nhau thì không có gì xảy ra. Điểm neo là điểm được thiết lập bởi lệnh gọi :meth:`selection_from` hoặc :meth:`selection_adjust` gần đây nhất. Nếu vùng chọn không nằm trong widget này, một vùng chọn mới được tạo bằng điểm neo gần đây nhất.

      .. versionadded:: 3.8



.. class:: Text(master=None, cnf={}, **kw)

   Một widget :class:`!Text` hiển thị và chỉnh sửa văn bản nhiều dòng. Các phần của văn bản có thể được định kiểu bằng **tags**, các vị trí cụ thể có thể được chú thích bằng **marks** nổi, và hình ảnh tùy ý cùng các widget khác có thể được nhúng vào văn bản. Widget này cũng cung cấp cơ chế undo/redo không giới hạn và hỗ trợ các widget peer dùng chung dữ liệu cơ sở. Widget kế thừa từ :class:`Widget`, :class:`XView` và :class:`YView`, vì vậy chế độ xem có thể được cuộn theo chiều ngang và chiều dọc bằng :meth:`~XView.xview` và :meth:`~YView.yview`. Tham khảo trang hướng dẫn Tk ``text`` để xem danh sách đầy đủ các tùy chọn.

   Hầu hết các phương thức nhận một hoặc nhiều đối số *index* xác định một vị trí trong văn bản. Như được mô tả trên trang hướng dẫn Tk ``text``, index là một chuỗi gồm một base, có thể theo sau bởi một hoặc nhiều modifier. Base có thể là ``'line.char'`` (dòng *line*, ký tự *char*, trong đó các dòng được đánh số từ 1 và các ký tự trong một dòng được đánh số từ 0; ``'line.end'`` tham chiếu đến ký tự xuống dòng kết thúc dòng), ``'end'`` (vị trí ngay sau ký tự xuống dòng cuối cùng), tên của một mark, ``'tag.first'`` hoặc ``'tag.last'`` (ký tự đầu tiên được gắn *tag*, hoặc vị trí ngay sau ký tự cuối cùng như vậy), tên của một hình ảnh hoặc cửa sổ được nhúng, hoặc ``@x,y`` (ký tự bao phủ các tọa độ pixel *x*, *y* trong widget). Một modifier như ``'+5 chars'``, ``'-3 lines'``, ``'linestart'``, ``'lineend'``, ``'wordstart'`` hoặc ``'wordend'`` điều chỉnh index tương ứng với base của nó; có thể kết hợp nhiều modifier và chúng được áp dụng từ trái sang phải, chẳng hạn như ``'insert wordstart - 1 c'``.

   .. method:: insert(index, chars, *args)

      Chèn chuỗi *chars* ngay trước ký tự tại *index* (nếu *index* là ``'end'``, thì chèn ngay trước ký tự xuống dòng cuối cùng). Theo mặc định, văn bản mới kế thừa mọi tag có ở cả hai phía của điểm chèn. Nếu cung cấp *args*, đối số này gồm các giá trị xen kẽ *tagList*, *chars*: *chars* đứng trước sẽ nhận chính xác các tag được liệt kê (một danh sách tag có thể là một tên tag hoặc một chuỗi tên), ghi đè các tag xung quanh.

   .. method:: delete(index1, index2=None)

      Xóa phạm vi ký tự từ *index1* đến nhưng không bao gồm *index2*. Nếu bỏ qua *index2*, ký tự đơn tại *index1* sẽ bị xóa. Widget luôn giữ một ký tự xuống dòng ở vị trí cuối cùng, vì vậy thao tác xóa nếu làm mất ký tự này sẽ được điều chỉnh cho phù hợp.

   .. method:: replace(index1, index2, chars, *args)

      Thay thế phạm vi ký tự từ *index1* đến nhưng không bao gồm *index2* bằng *chars*. Thao tác này tương đương với một :meth:`delete` theo sau bởi một :meth:`insert` tại *index1*; *args* được diễn giải như đối với :meth:`insert`.

      .. versionadded:: 3.3

   .. method:: get(index1, index2=None)

      Trả về văn bản từ *index1* đến nhưng không bao gồm *index2* dưới dạng một chuỗi. Nếu bỏ qua *index2*, trả về ký tự đơn tại *index1*. Hình ảnh và cửa sổ được nhúng sẽ bị loại khỏi kết quả.

   .. method:: index(index)

      Trả về vị trí tương ứng với *index* ở dạng ``'line.char'`` chuẩn.

   .. method:: compare(index1, op, index2)

      So sánh các vị trí của *index1* và *index2* bằng toán tử quan hệ *op*, phải là một trong các toán tử ``'<'``, ``'<='``, ``'=='``, ``'>='``, ``'>'`` hoặc ``'!='``, rồi trả về kết quả boolean.

   .. method:: count(index1, index2, *options, return_ints=False)

      Đếm số mục thuộc các loại được yêu cầu nằm giữa *index1* và *index2*; số đếm là số âm nếu *index1* đứng sau *index2*. Mỗi tên trong *options* chỉ định một loại mục cần đếm: ``'chars'``, ``'displaychars'``, ``'displayindices'``, ``'displaylines'``, ``'indices'``, ``'lines'``, ``'xpixels'`` hoặc ``'ypixels'`` (mặc định, được dùng khi không cung cấp tùy chọn, là ``'indices'``). Pseudo-option ``'update'`` buộc mọi thông tin bố cục đã lỗi thời phải được tính toán lại trước khi đánh giá các tùy chọn tiếp theo. Khi *return_ints* là true và chỉ cung cấp một tùy chọn đếm, trả về một số nguyên thuần; nếu không, trả về một tuple có một số nguyên cho mỗi tùy chọn đếm (hoặc ``None`` nếu kết quả rỗng).

      .. versionadded:: 3.3

      .. versionchanged:: 3.13
         Đã thêm tham số *return_ints*.


   .. method:: see(index)

      Điều chỉnh chế độ xem để ký tự do *index* chỉ định được hiển thị. Nếu ký tự đó đã hiển thị, phương thức không có tác dụng; nếu nó chỉ nằm ngoài chế độ xem một đoạn ngắn, widget chỉ cuộn vừa đủ để đưa ký tự đến cạnh gần nhất, nếu không thì cuộn để căn giữa *index* trong cửa sổ.

   .. method:: bbox(index)

      Trả về một tuple ``(x, y, width, height)`` chứa bounding box, tính bằng pixel, của phần hiển thị của ký tự tại *index*, hoặc ``None`` nếu ký tự đó không hiển thị trên màn hình.

      Phương thức này che khuất :meth:`!Misc.bbox` được kế thừa; hãy sử dụng :meth:`~Misc.grid_bbox` cho hộp giới hạn của grid.

   .. method:: dlineinfo(index)

      Trả về một tuple ``(x, y, width, height, baseline)`` mô tả dòng hiển thị chứa *index*: bốn giá trị đầu tiên cung cấp bounding box của dòng theo pixel, còn *baseline* cung cấp độ lệch của baseline, được đo từ phía trên xuống của vùng. Trả về ``None`` nếu dòng hiển thị đó không hiển thị trên màn hình.

   .. method:: mark_set(markName, index)

      Đặt mark có tên *markName* vào vị trí ngay trước ký tự tại *index*, đồng thời tạo mark nếu mark đó chưa tồn tại. Mark được tạo theo cách này mặc định có right gravity.

   .. method:: mark_unset(*markNames)

      Xóa từng mark có tên được nêu trong *markNames*. Không được xóa các mark đặc biệt ``insert`` và ``current``.

   .. method:: mark_names()

      Trả về một tuple chứa tên của tất cả các mark hiện đang được đặt trong widget.

   .. method:: mark_gravity(markName, direction=None)

      Nếu bỏ qua *direction*, hãy trả về gravity của mark *markName*, có thể là ``'left'`` hoặc ``'right'``. Nếu không, hãy đặt gravity của mark thành *direction*. Gravity xác định văn bản được chèn tại vị trí của mark sẽ xuất hiện ở phía nào của mark: mark có right gravity (mặc định) sẽ nằm bên phải phần văn bản đó.

   .. method:: mark_next(index)

      Trả về tên của mark đầu tiên tại hoặc sau *index*, hoặc ``None`` nếu không có mark nào. Khi *index* là tên của một mark, việc tìm kiếm bắt đầu ngay sau mark đó.

   .. method:: mark_previous(index)

      Trả về tên của mark cuối cùng tại hoặc trước *index*, hoặc ``None`` nếu không có mark nào. Khi *index* là tên của một mark, việc tìm kiếm bắt đầu ngay trước mark đó.

   .. method:: tag_add(tagName, index1, *args)

      Thêm thẻ *tagName* vào phạm vi ký tự từ *index1* đến trước chỉ mục tiếp theo trong *args*. Các cặp chỉ mục tiếp theo có thể xuất hiện trong *args* để gắn thẻ cho các phạm vi bổ sung; một chỉ mục đơn ở cuối chỉ gắn thẻ cho ký tự tại chỉ mục đó.

   .. method:: tag_remove(tagName, index1, index2=None)

      Xóa thẻ *tagName* khỏi các ký tự từ *index1* đến trước *index2* (hoặc khỏi ký tự đơn tại *index1* nếu *index2* bị bỏ qua). Bản thân thẻ vẫn tiếp tục tồn tại ngay cả khi không có ký tự nào mang thẻ đó.

   .. method:: tag_delete(*tagNames)

      Xóa từng thẻ có tên trong *tagNames*, gỡ chúng khỏi mọi ký tự và loại bỏ các tùy chọn cùng các binding của chúng.

   .. method:: tag_config(tagName, cnf=None, **kw)
      :no-typesetting:

   .. method:: tag_configure(tagName, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của thẻ *tagName*. Thao tác này tương tự :meth:`~Misc.configure`, ngoại trừ việc áp dụng cho một thẻ thay vì toàn bộ widget: khi không có tùy chọn, thao tác trả về một dictionary mô tả các tùy chọn hiện tại; nếu không, thao tác sẽ đặt các tùy chọn được cung cấp. Việc định nghĩa thẻ theo cách này cũng khiến thẻ có mức ưu tiên cao hơn mọi thẻ hiện có.

      Các tùy chọn thẻ được hỗ trợ, tất cả đều điều khiển giao diện của văn bản được gắn thẻ, gồm:

      *font*
         Phông chữ dùng cho văn bản.

      *foreground*
         Màu được sử dụng cho văn bản.

      *background*
         Màu được sử dụng cho khu vực phía sau văn bản.

      *fgstipple*, *bgstipple*
         Các bitmap được sử dụng để tạo mẫu chấm cho tiền cảnh (văn bản) và nền; chỉ được hỗ trợ tốt trên X11.

      *borderwidth*
         Độ rộng của đường viền được vẽ quanh văn bản theo *relief* (mặc định là ``0``).

      *relief*
         Diện mạo 3-D của đường viền văn bản: ``'flat'`` (mặc định), ``'raised'``, ``'sunken'``, ``'ridge'``, ``'groove'`` hoặc ``'solid'``.

      *offset*
         Mức độ văn bản được nâng lên trên đường cơ sở (hoặc, nếu là số âm, hạ xuống dưới đường cơ sở), dùng cho chỉ số trên và chỉ số dưới.

      *underline*
         Có gạch chân văn bản hay không.

      *underlinefg*
         Màu của đường gạch chân; theo mặc định, màu này là màu của văn bản.

      *overstrike*
         Xác định có vẽ một đường xuyên qua giữa văn bản hay không.

      *overstrikefg*
         Màu của đường gạch ngang; theo mặc định, màu này là màu của văn bản.

      *elide*
         Văn bản có bị rút gọn (ẩn) hay không.

      *justify*
         Cách căn chỉnh ký tự đầu tiên của một dòng hiển thị: ``'left'`` (mặc định), ``'right'`` hoặc ``'center'``.

      *wrap*
         Cách ngắt các dòng quá dài: ``'char'``, ``'word'`` hoặc ``'none'``.

      *lmargin1*, *lmargin2*
         Độ thụt lề, tính bằng pixel, của dòng hiển thị đầu tiên của một dòng logic và của các dòng hiển thị còn lại.

      *lmargincolor*
         Màu của vùng lề bên trái.

      *rmargin*
         Lề bên phải, tính bằng pixel.

      *rmargincolor*
         Màu của vùng lề bên phải.

      *spacing1*, *spacing2*, *spacing3*
         Khoảng trống bổ sung, tính bằng pixel, phía trên dòng hiển thị đầu tiên của một dòng logic, giữa các dòng hiển thị của nó và phía dưới dòng hiển thị cuối cùng của nó.

      *tabs*
         Tập hợp các điểm dừng tab, có cùng định dạng với tùy chọn *tabs* của widget.

      *tabstyle*
         Cách diễn giải các điểm dừng tab: ``'tabular'`` hoặc ``'wordprocessor'``.

      *selectbackground*, *selectforeground*
         Màu nền và màu chữ được sử dụng cho văn bản khi văn bản được chọn.

      .. note::

         Tk 8.6 đã bổ sung các tùy chọn *lmargincolor*, *overstrikefg*, *rmargincolor*, *selectbackground*, *selectforeground* và *underlinefg*.

      :meth:`tag_config` là bí danh của :meth:`!tag_configure`.

   .. method:: tag_cget(tagName, option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option* cho tag *tagName*.

   .. method:: tag_names(index=None)

      Nếu bỏ qua *index*, trả về một tuple chứa tên của tất cả các tag được định nghĩa trong widget; nếu không, chỉ trả về tên của các tag được áp dụng cho ký tự tại *index*. Các tên được sắp xếp từ mức ưu tiên thấp nhất đến cao nhất.

   .. method:: tag_ranges(tagName)

      Trả về một tuple gồm các chỉ số mô tả tất cả các phạm vi văn bản được gắn tag *tagName*. Kết quả xen kẽ các chỉ số bắt đầu và kết thúc, nên các phần tử ``2*i`` và ``2*i+1`` bao quanh phạm vi thứ *i*.

   .. method:: tag_nextrange(tagName, index1, index2=None)

      Tìm kiếm về phía trước từ *index1* (tối đa đến *index2* nếu được cung cấp) để tìm phạm vi đầu tiên gồm các ký tự được gắn tag *tagName*, rồi trả về tuple gồm hai phần tử là chỉ số bắt đầu và kết thúc của phạm vi đó, hoặc một tuple rỗng nếu không có phạm vi như vậy.

   .. method:: tag_prevrange(tagName, index1, index2=None)

      Tìm kiếm ngược từ *index1* (lùi đến *index2* nếu được cung cấp) để tìm phạm vi liền trước gần nhất gồm các ký tự được gắn tag *tagName*, rồi trả về tuple gồm hai phần tử là chỉ số bắt đầu và kết thúc của phạm vi đó, hoặc một tuple rỗng nếu không có phạm vi như vậy.

   .. method:: tag_raise(tagName, aboveThis=None)

      Nâng mức ưu tiên của thẻ *tagName* lên ngay trên mức ưu tiên của *aboveThis*, hoặc lên mức ưu tiên cao nhất của tất cả các thẻ nếu bỏ qua *aboveThis*. Khi các tùy chọn hiển thị của những thẻ chồng lấp xung đột, thẻ có mức ưu tiên cao hơn sẽ được ưu tiên.

   .. method:: tag_lower(tagName, belowThis=None)

      Hạ mức ưu tiên của thẻ *tagName* xuống ngay dưới mức ưu tiên của *belowThis*, hoặc xuống mức ưu tiên thấp nhất của tất cả các thẻ nếu bỏ qua *belowThis*.

   .. method:: tag_bind(tagName, sequence, func, add=None)

      Liên kết sự kiện *sequence* trên các ký tự được gắn thẻ *tagName* với callback *func*, để *func* được gọi khi sự kiện đó xảy ra trên một ký tự như vậy. Nếu *add* là true, liên kết sẽ được thêm cùng với mọi liên kết hiện có cho *sequence*; nếu không, chúng sẽ được thay thế. Hoạt động giống như :meth:`~Misc.bind` và trả về mã định danh của liên kết mới.

   .. method:: tag_unbind(tagName, sequence, funcid=None)

      Xóa các liên kết của sự kiện *sequence* trên các ký tự được gắn thẻ *tagName*. Nếu cung cấp *funcid*, chỉ liên kết đó (do :meth:`tag_bind` trả về) sẽ bị xóa và callback của nó sẽ được hủy đăng ký.

      .. versionchanged:: 3.13
         Nếu cung cấp *funcid*, chỉ callback đó được hủy liên kết.


   .. method:: image_create(index, cnf={}, **kw)

      Nhúng một hình ảnh tại *index* và trả về tên được gán cho phiên bản hình ảnh này; tên đó sau đó có thể được dùng làm chỉ mục hoặc truyền cho các phương thức ``image_*`` khác. Các tùy chọn được cung cấp trong *cnf* và *kw* bao gồm *image* (hình ảnh Tk cần hiển thị), *name* (tên cơ sở cho phiên bản), *align*, *padx* và *pady*.

   .. method:: image_cget(index, option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option* cho hình ảnh được nhúng tại *index*.

   .. method:: image_configure(index, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của ảnh được nhúng tại *index*, tương tự :meth:`~Misc.configure` nhưng áp dụng cho ảnh đó.

   .. method:: image_names()

      Trả về một tuple chứa tên của tất cả ảnh được nhúng trong widget.

      .. note::

         Phương thức này che khuất :meth:`Misc.image_names` được kế thừa, vốn trả về tên của tất cả ảnh trong trình thông dịch Tcl; phương thức đó không khả dụng trên một :class:`Text`.

   .. method:: window_create(index, cnf={}, **kw)

      Nhúng một cửa sổ (bất kỳ widget nào) tại *index*. Các tùy chọn, được cung cấp trong *cnf* và *kw*, bao gồm *window* (widget cần nhúng), *create* (callback tạo widget theo yêu cầu), *align*, *stretch*, *padx* và *pady*. Widget được nhúng phải là một hậu duệ của phần tử cha của text widget.

   .. method:: window_cget(index, option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option* cho cửa sổ được nhúng tại *index*.

   .. method:: window_config(index, cnf=None, **kw)
      :no-typesetting:

   .. method:: window_configure(index, cnf=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cấu hình của cửa sổ được nhúng tại *index*, tương tự :meth:`~Misc.configure` nhưng áp dụng cho cửa sổ đó.

      :meth:`window_config` là bí danh của :meth:`!window_configure`.

   .. method:: window_names()

      Trả về một tuple chứa tên của tất cả cửa sổ được nhúng trong widget.

   .. method:: edit(*args)

      Wrapper cấp thấp quanh lệnh widget Tk ``edit`` để điều khiển cơ chế undo/redo và cờ modified; *args* là subcommand ``edit`` cùng các đối số của nó. Các phương thức :meth:`!edit_\*` bên dưới là những wrapper mỏng quanh lệnh này và thường thuận tiện hơn khi sử dụng.

   .. method:: edit_modified(arg=None)

      Nếu bỏ qua *arg*, trả về trạng thái hiện tại của cờ modified dưới dạng true hoặc false; cờ này được tự động đặt mỗi khi văn bản được chèn hoặc xóa. Nếu không, đặt cờ thành giá trị boolean *arg*.

   .. method:: edit_undo()

      Hoàn tác hành động chỉnh sửa gần đây nhất, tức là tất cả thao tác chèn và xóa được ghi vào undo stack kể từ separator trước đó, rồi chuyển hành động này vào redo stack. Phát sinh :exc:`TclError` nếu undo stack trống. Không có tác dụng trừ khi tùy chọn *undo* là true. Kể từ Tk 9.0, trả về một tuple gồm các chỉ mục phân định những phạm vi văn bản đã thay đổi.

   .. method:: edit_redo()

      Thực hiện lại hành động chỉnh sửa vừa được hoàn tác gần đây nhất, với điều kiện chưa có chỉnh sửa nào khác được thực hiện kể từ đó, rồi chuyển hành động này trở lại undo stack. Phát sinh :exc:`TclError` nếu redo stack trống. Không có tác dụng trừ khi tùy chọn *undo* là true. Kể từ Tk 9.0, trả về một tuple gồm các chỉ mục phân định những phạm vi văn bản đã thay đổi.

   .. method:: edit_reset()

      Xóa undo stack và redo stack.

   .. method:: edit_separator()

      Đẩy một separator vào undo stack, đánh dấu ranh giới giữa các hành động chỉnh sửa để undo và redo. Không có tác dụng trừ khi tùy chọn *undo* là true. Các separator được tự động chèn khi tùy chọn *autoseparators* là true.

   .. method:: search(pattern, index, stopindex=None, forwards=None, backwards=None, exact=None, regexp=None, nocase=None, count=None, elide=None)

      Tìm kiếm *pattern* bắt đầu từ *index* và trả về chỉ mục của ký tự đầu tiên trong kết quả khớp đầu tiên, hoặc một chuỗi rỗng nếu không có kết quả khớp. Nếu được cung cấp, việc tìm kiếm sẽ dừng tại *stopindex*; nếu không, tìm kiếm sẽ vòng qua hai đầu của văn bản cho đến khi quay lại vị trí bắt đầu. Các cờ keyword dạng boolean sau đây điều khiển việc tìm kiếm: *forwards* hoặc *backwards* chọn hướng tìm kiếm (mặc định là tiến); *exact* (mặc định) hoặc *regexp* chọn kiểu khớp literal hoặc biểu thức chính quy; *nocase* khiến việc khớp không phân biệt chữ hoa chữ thường; và *elide* khiến cả văn bản ẩn cũng được tìm kiếm. Nếu *count* là một :class:`Variable`, số lượng vị trí chỉ mục trong kết quả khớp sẽ được lưu vào đó.


   .. method:: scan_mark(x, y)

      Ghi lại *x*, *y* và chế độ xem hiện tại để sử dụng với các lệnh gọi sau này
      :meth:`scan_dragto`. Thông thường, lệnh này được liên kết với thao tác nhấn nút chuột trong widget.

   .. method:: scan_dragto(x, y)

      Cuộn widget một khoảng bằng 10 lần độ chênh lệch giữa *x*, *y* và tọa độ được truyền đến lời gọi :meth:`scan_mark` gần nhất. Thao tác này thường được liên kết với các sự kiện chuyển động của chuột, tạo hiệu ứng kéo văn bản qua cửa sổ với tốc độ cao.

   .. method:: debug(boolean=None)

      Nếu bỏ qua *boolean*, trả về việc các kiểm tra tính nhất quán nội bộ của cấu trúc dữ liệu B-tree có được bật hay không. Nếu không, bật hoặc tắt các kiểm tra này. Thiết lập này được dùng chung cho tất cả text widget và có thể làm chậm đáng kể các widget chứa lượng văn bản lớn.

   .. method:: dump(index1, index2=None, command=None, **kw)

      Trả về nội dung của widget từ *index1* đến nhưng không bao gồm *index2* (hoặc chỉ trả về đoạn tại *index1* nếu bỏ qua *index2*), bao gồm văn bản và thông tin về mark, tag, image và window. Kết quả là một danh sách các bộ ba ``(key, value, index)``, trong đó *key* là một trong các giá trị ``'text'``, ``'mark'``, ``'tagon'``, ``'tagoff'``, ``'image'`` hoặc ``'window'``. Theo mặc định, tất cả các loại đều được báo cáo; truyền bất kỳ đối số keyword nào sau đây với giá trị true: *all*, *text*, *mark*, *tag*, *image* hoặc *window* sẽ giới hạn kết xuất ở các loại được chọn. Nếu cung cấp *command*, lệnh này được gọi một lần cho mỗi bộ ba với ba giá trị làm đối số và không trả về gì.

   .. method:: peer_create(newPathName, cnf={}, **kw)

      Tạo một text widget peer với tên đường dẫn *newPathName*, dùng chung dữ liệu nền tảng của widget này (văn bản, mark, tag, image và ngăn xếp hoàn tác). Các thay đổi được thực hiện thông qua bất kỳ peer nào sẽ được phản ánh trong tất cả các peer. Theo mặc định, peer bao phủ cùng các dòng như widget này; có thể cung cấp các tùy chọn text tiêu chuẩn, bao gồm *startline* và *endline*, để ghi đè thiết lập này.

      .. versionadded:: 3.3

   .. method:: peer_names()

      Trả về một tuple gồm tên đường dẫn của các peer của widget này, không bao gồm chính widget đó.

      .. versionadded:: 3.3

   .. method:: yview_pickplace(*what)

      Điều chỉnh view để vị trí được chỉ định bởi *what* hiển thị. Đây là một cách tương đương đã lỗi thời của :meth:`see`, nên sử dụng cách đó thay thế.


Các lớp biến
^^^^^^^^^^^^

.. class:: Variable(master=None, value=None, name=None)

   Lớp cơ sở cho các wrapper biến Tk. Một biến Tk là một giá trị được lưu trong trình thông dịch Tcl và có thể liên kết với các widget thông qua các tùy chọn *variable* hoặc *textvariable* của chúng (xem
   :ref:`coupling-widget-variables`), để các thay đổi được truyền theo cả hai chiều: cập nhật biến sẽ cập nhật mọi widget liên kết với biến đó, và người dùng chỉnh sửa widget như vậy sẽ cập nhật biến.

   *master* là widget có trình thông dịch Tcl sở hữu biến; nếu bị bỏ qua, cửa sổ gốc mặc định sẽ được sử dụng. *value* là giá trị ban đầu; nếu bị bỏ qua, giá trị mặc định dành riêng cho kiểu sẽ được sử dụng. *name* là tên của biến trong trình thông dịch Tcl; nếu bị bỏ qua, một tên duy nhất có dạng ``'PY_VARnum'`` sẽ được tạo. Nếu *name* khớp với một biến hiện có và *value* bị bỏ qua, giá trị hiện có sẽ được giữ lại.

   Trong hầu hết trường hợp, bạn nên sử dụng một trong các lớp con có kiểu bên dưới --
   :class:`StringVar`, :class:`IntVar`, :class:`DoubleVar` hoặc
   :class:`BooleanVar` -- thay vì trực tiếp sử dụng :class:`!Variable`.

   .. note::

      Khi một :class:`!Variable` được thu gom rác, biến Tcl của nó sẽ bị hủy đặt. Hãy giữ một tham chiếu đến nó trong suốt thời gian một widget còn liên kết với nó, chẳng hạn bằng cách lưu nó dưới dạng thuộc tính thay vì trong một biến cục bộ. Nếu không, Tk sẽ tạo lại biến Tcl để widget tiếp tục hoạt động, nhưng biến này sẽ không bao giờ bị hủy đặt lại, làm rò rỉ một biến Tcl cho mỗi wrapper bị loại bỏ.

   .. versionchanged:: 3.10
      Hai biến hiện chỉ so sánh bằng nhau (``==``) khi chúng có cùng tên, thuộc cùng một lớp và thuộc cùng một trình thông dịch Tcl.

   .. method:: get()

      Trả về giá trị hiện tại của biến. Đối với lớp cơ sở, giá trị được trả về dưới dạng chuỗi; các lớp con có kiểu sẽ chuyển đổi giá trị thành kiểu Python thích hợp.

   .. method:: initialize(value)
      :no-typesetting:

   .. method:: set(value)

      Đặt biến thành *value*.
      :meth:`initialize` là bí danh của :meth:`!set`.

      .. versionadded:: 3.3
         Cách viết *initialize*.

   .. method:: trace_add(mode, callback)

      Đăng ký *callback* để được gọi khi biến được truy cập theo *mode*. *mode* là một trong các chuỗi ``'array'``, ``'read'``, ``'write'`` hoặc ``'unset'``, hay một danh sách hoặc tuple chứa các chuỗi như vậy.

      Khi được kích hoạt, *callback* được gọi với ba đối số: tên của biến Tcl, một chỉ mục (hoặc chuỗi rỗng nếu biến không phải là một phần tử của mảng), và *mode* đã kích hoạt lệnh gọi.

      Trả về tên nội bộ của callback đã đăng ký, tên này có thể được truyền cho :meth:`trace_remove`.

      .. versionadded:: 3.6

   .. method:: trace_remove(mode, cbname)

      Xóa một trace callback khỏi biến. *mode* phải khớp với *mode* đã được truyền cho :meth:`trace_add`, và *cbname* là tên callback được :meth:`trace_add` trả về.

      .. versionadded:: 3.6

   .. method:: trace_info()

      Trả về danh sách các cặp ``(modes, cbname)`` mô tả tất cả trace hiện đang được đặt trên biến, trong đó *modes* là một tuple gồm các chuỗi mode còn *cbname* là tên callback nội bộ.

      .. versionadded:: 3.6

   .. method:: trace(mode, callback)
      :no-typesetting:

   .. method:: trace_variable(mode, callback)

      Đăng ký *callback* để được gọi khi biến được truy cập theo *mode*. *mode* là một trong các chuỗi ``'r'``, ``'w'`` hoặc ``'u'``, tương ứng với đọc, ghi hoặc hủy thiết lập. Trả về tên nội bộ của callback đã đăng ký.
      :meth:`trace` là bí danh của :meth:`!trace_variable`.

      .. deprecated:: 3.6
         Thay vào đó, hãy sử dụng :meth:`trace_add`. Phương thức này bao bọc một tính năng của Tcl đã bị loại bỏ trong Tcl 9.0.

   .. method:: trace_vdelete(mode, cbname)

      Xóa trace callback có tên *cbname* đã đăng ký cho *mode* với
      :meth:`trace_variable`.

      .. deprecated:: 3.6
         Thay vào đó, hãy sử dụng :meth:`trace_remove`. Phương thức này bao bọc một tính năng của Tcl đã bị loại bỏ trong Tcl 9.0.

   .. method:: trace_vinfo()

      Trả về danh sách các cặp ``(mode, cbname)`` cho tất cả trace được thiết lập trên biến bằng :meth:`trace_variable`.

      .. deprecated:: 3.6
         Thay vào đó, hãy sử dụng :meth:`trace_info`. Phương thức này bao bọc một tính năng của Tcl đã bị loại bỏ trong Tcl 9.0.


.. class:: StringVar(master=None, value=None, name=None)

   Một lớp con :class:`Variable` chứa một chuỗi. Giá trị mặc định là ``''``.

   .. method:: get()

      Trả về giá trị của biến dưới dạng :class:`str`.


.. class:: IntVar(master=None, value=None, name=None)

   Một lớp con :class:`Variable` chứa một số nguyên. Giá trị mặc định là ``0``.

   .. method:: get()

      Trả về giá trị của biến dưới dạng :class:`int`.


.. class:: DoubleVar(master=None, value=None, name=None)

   Một lớp con :class:`Variable` chứa một số thực. Giá trị mặc định là ``0.0``.

   .. method:: get()

      Trả về giá trị của biến dưới dạng :class:`float`.

   .. _tkinter-numeric-locale:

   .. note::

      Giá trị dấu phẩy động luôn được phân tích cú pháp với dấu chấm (``.``) làm dấu phân cách thập phân, nhưng :class:`Spinbox`, :class:`Scale` và
      :class:`ttk.Spinbox <tkinter.ttk.Spinbox>` định dạng giá trị đó theo locale ``LC_NUMERIC``. Trong locale sử dụng dấu phẩy, chúng tạo ra một giá trị mà :meth:`get` không thể đọc, dẫn đến :exc:`TclError`. Đặt ``LC_NUMERIC`` thành một locale sử dụng dấu chấm (chẳng hạn như ``'C'``) để tránh điều này.


.. class:: BooleanVar(master=None, value=None, name=None)

   Một lớp con :class:`Variable` lưu một giá trị boolean. Giá trị mặc định là ``False``.

   .. method:: get()

      Trả về giá trị của biến dưới dạng :class:`bool`. Phát sinh :exc:`ValueError` nếu không thể diễn giải giá trị này thành boolean.

   .. method:: initialize(value)
      :no-typesetting:

   .. method:: set(value)

      Đặt biến thành *value*, chuyển đổi giá trị đó thành boolean.
      :meth:`initialize` là bí danh của :meth:`!set`.

      .. versionadded:: 3.3
         Cách viết *initialize*.


Các lớp hình ảnh
^^^^^^^^^^^^^^^^

.. class:: Image(imgtype, name=None, cnf={}, master=None, **kw)

   Lớp cơ sở cho hình ảnh Tk. *imgtype* là loại hình ảnh Tk, một trong ``'photo'`` hoặc ``'bitmap'``. Hình ảnh là một đối tượng có tên mà các widget có thể hiển thị thông qua tùy chọn *image*; việc xóa mọi tham chiếu đến đối tượng :class:`!Image` sẽ xóa hình ảnh Tk bên dưới. Thông thường, bạn tạo một :class:`PhotoImage` hoặc :class:`BitmapImage` thay vì tạo trực tiếp một :class:`!Image`.

   Các tùy chọn cấu hình của ảnh được cung cấp bởi *cnf* và *kw*, đồng thời có thể được truy vấn và thay đổi sau đó bằng mapping protocol (sử dụng ``image[key]``) hoặc bằng phương thức :meth:`configure`.

   .. method:: config(**kw)
      :no-typesetting:

   .. method:: configure(**kw)

      Sửa đổi một hoặc nhiều tùy chọn cấu hình của ảnh. Các tùy chọn hợp lệ phụ thuộc vào loại ảnh; xem :class:`PhotoImage` và
      :class:`BitmapImage`.
      :meth:`config` là bí danh của :meth:`!configure`.

   .. method:: height()

      Trả về chiều cao của ảnh, tính bằng pixel.

   .. method:: width()

      Trả về chiều rộng của ảnh, tính bằng pixel.

   .. method:: type()

      Trả về loại ảnh, tức là giá trị của *imgtype* được dùng khi tạo ảnh (ví dụ ``'photo'`` hoặc ``'bitmap'``).


.. class:: PhotoImage(name=None, cnf={}, master=None, **kw)

   Ảnh đầy đủ màu sắc (loại ảnh Tk ``photo``), được lưu trữ nội bộ với mức độ trong suốt khác nhau ở từng pixel. Ảnh có thể đọc và ghi các tệp GIF, PPM/PGM và (trong Tk 8.6 trở lên) PNG, đọc các tệp SVG (trong Tk 9.0 trở lên), cũng như được vẽ trong các widget. Kế thừa từ :class:`Image`.

   Các tùy chọn cấu hình bao gồm *data* (nội dung ảnh dưới dạng chuỗi), *file* (tên tệp để đọc nội dung), *format* (tên trình xử lý định dạng tệp), *width* và *height* (kích thước ảnh, được sử dụng khi dựng ảnh từng phần), *gamma* và *palette*.

   .. method:: blank()

      Xóa dữ liệu của ảnh; tức là đặt toàn bộ ảnh ở trạng thái không có dữ liệu, để ảnh được hiển thị trong suốt và nền của cửa sổ chứa ảnh sẽ hiển thị xuyên qua.

   .. method:: cget(option)

      Trả về giá trị hiện tại của tùy chọn cấu hình *option*.

   .. method:: copy(*, from_coords=None, zoom=None, subsample=None)

      Trả về một :class:`PhotoImage` mới chứa bản sao của ảnh này.

      *from_coords* chỉ định một vùng con hình chữ nhật của ảnh nguồn cần sao chép. Giá trị này phải là một tuple hoặc danh sách gồm từ 1 đến 4 số nguyên ``(x1, y1, x2, y2)``. ``(x1, y1)`` và ``(x2, y2)`` chỉ định hai góc đối diện theo đường chéo của hình chữ nhật. Nếu không chỉ định *x2* và *y2*, chúng sẽ mặc định là góc dưới bên phải của ảnh nguồn. Các pixel được sao chép bao gồm cạnh trái và cạnh trên của hình chữ nhật, nhưng không bao gồm cạnh dưới hoặc cạnh phải. Nếu không cung cấp *from_coords*, toàn bộ ảnh nguồn sẽ được sao chép.

      Nếu chỉ định *zoom* hoặc *subsample*, ảnh sẽ được biến đổi như trong các phương thức :meth:`zoom` hoặc :meth:`subsample`. Giá trị phải là một số nguyên đơn hoặc một cặp số nguyên.

      .. versionchanged:: 3.13
         Đã thêm các tham số *from_coords*, *zoom* và *subsample*.


   .. method:: copy_replace(sourceImage, *, from_coords=None, to=None, \
                            shrink=False, zoom=None, subsample=None, \ compositingrule=None)

      Sao chép một vùng từ *sourceImage* (phải là một :class:`PhotoImage`) vào hình ảnh này, có thể kèm theo phóng to pixel và/hoặc subsampling. Nếu không chỉ định tùy chọn nào, toàn bộ *sourceImage* sẽ được sao chép vào hình ảnh này, bắt đầu tại tọa độ ``(0, 0)``.

      *from_coords* chỉ định một vùng con hình chữ nhật của hình ảnh nguồn cần sao chép, như trong phương thức :meth:`copy`.

      *to* chỉ định một vùng con hình chữ nhật của hình ảnh đích sẽ bị tác động. Giá trị này phải là một tuple hoặc list gồm từ 1 đến 4 số nguyên ``(x1, y1, x2, y2)``. Nếu không chỉ định *x2* và *y2*, chúng mặc định là ``(x1, y1)`` cộng với kích thước của vùng nguồn (sau khi subsampling và phóng to, nếu được chỉ định). Nếu chỉ định *x2* và *y2*, vùng nguồn sẽ được lặp lại nếu cần để lấp đầy vùng đích theo dạng lát.

      Nếu *shrink* là true, kích thước của hình ảnh đích sẽ được giảm nếu cần, để vùng được sao chép vào nằm ở góc dưới bên phải của hình ảnh.

      Nếu chỉ định *zoom* hoặc *subsample*, ảnh sẽ được biến đổi như trong các phương thức :meth:`zoom` hoặc :meth:`subsample`. Giá trị phải là một số nguyên đơn hoặc một cặp số nguyên.

      *compositingrule* chỉ định cách các pixel trong suốt của hình ảnh nguồn được kết hợp với hình ảnh đích. Với ``'overlay'`` (mặc định), nội dung cũ của hình ảnh đích vẫn hiển thị, như thể hình ảnh nguồn được in trên một tấm phim trong suốt rồi đặt lên trên hình ảnh đích. Với ``'set'``, nội dung cũ của hình ảnh đích bị loại bỏ và hình ảnh nguồn được sử dụng nguyên trạng.

      .. versionadded:: 3.13


   .. method:: data(format=None, *, from_coords=None, background=None, \
                    grayscale=False)

      Trả về dữ liệu hình ảnh.

      *format* chỉ định tên của trình xử lý định dạng tệp hình ảnh cần sử dụng. Nếu không được cung cấp, dữ liệu được trả về dưới dạng một tuple (mỗi phần tử tương ứng với một hàng) gồm các chuỗi chứa các màu được phân tách bằng dấu cách (mỗi phần tử tương ứng với một pixel/cột) ở định dạng ``#RRGGBB``.

      *from_coords* chỉ định một vùng hình chữ nhật của hình ảnh cần trả về. Nó phải là một tuple hoặc một danh sách gồm từ 1 đến 4 số nguyên ``(x1, y1, x2, y2)``. Nếu chỉ chỉ định *x1* và *y1*, vùng này sẽ mở rộng từ ``(x1, y1)`` đến góc dưới bên phải của hình ảnh. Nếu cung cấp đủ cả bốn tọa độ, chúng chỉ định hai góc đối diện theo đường chéo của vùng, bao gồm ``(x1, y1)`` và không bao gồm ``(x2, y2)``. Nếu không cung cấp *from_coords*, toàn bộ hình ảnh sẽ được trả về.

      Nếu chỉ định *background*, dữ liệu sẽ không chứa thông tin về độ trong suốt; trong tất cả các pixel trong suốt, màu sẽ được thay thế bằng màu đã chỉ định.

      Nếu *grayscale* là true, dữ liệu sẽ không chứa thông tin màu; toàn bộ dữ liệu pixel được chuyển thành thang độ xám.

      .. versionadded:: 3.13


   .. method:: get(x, y)

      Trả về màu của pixel tại tọa độ (*x*, *y*) dưới dạng một tuple ``(r, g, b)`` gồm ba số nguyên từ 0 đến 255, lần lượt biểu thị các thành phần đỏ, lục và lam.

   .. method:: put(data, to=None)

      Đặt các pixel của ảnh thành các màu được chỉ định trong *data*, giá trị này phải là một chuỗi hoặc một chuỗi lồng nhau gồm các hàng pixel theo chiều ngang với các màu pixel (ví dụ ``"{red green} {blue yellow}"``).

      *to* chỉ định tọa độ của vùng ảnh mà dữ liệu được sao chép vào. Giá trị này phải là một tuple hoặc list gồm 2 hoặc 4 số nguyên ``(x1, y1)`` hoặc ``(x1, y1, x2, y2)``, lần lượt chỉ định góc trên bên trái và tùy chọn góc dưới bên phải của vùng. Vị trí mặc định là ``(0, 0)``.

   .. method:: read(filename, format=None, *, from_coords=None, to=None, \
                    shrink=False)

      Đọc dữ liệu ảnh từ tệp có tên *filename* vào ảnh.

      *format* chỉ định định dạng của dữ liệu ảnh trong tệp.

      *from_coords* chỉ định một vùng con hình chữ nhật của dữ liệu tệp ảnh sẽ được sao chép vào ảnh đích. Giá trị này phải là một tuple hoặc list gồm từ 1 đến 4 số nguyên ``(x1, y1, x2, y2)``. Nếu chỉ chỉ định *x1* và *y1*, vùng sẽ kéo dài từ ``(x1, y1)`` đến góc dưới bên phải của ảnh trong tệp. Nếu cung cấp cả bốn tọa độ, chúng chỉ định các góc đối diện theo đường chéo của vùng. Nếu không cung cấp *from_coords*, toàn bộ ảnh trong tệp sẽ được đọc.

      *to* chỉ định tọa độ của góc trên bên trái của vùng ảnh mà dữ liệu được đọc vào. Giá trị mặc định là ``(0, 0)``.

      Nếu *shrink* là true, kích thước của ảnh sẽ được giảm xuống nếu cần, để vùng mà dữ liệu tệp được đọc nằm ở góc dưới bên phải của ảnh.

      .. versionadded:: 3.13


   .. method:: subsample(x, y='', *, from_coords=None)

      Trả về một :class:`PhotoImage` mới dựa trên ảnh này nhưng chỉ sử dụng mỗi pixel thứ *x* theo hướng X và mỗi pixel thứ *y* theo hướng Y. Nếu không cung cấp *y*, giá trị mặc định sẽ giống với *x*.

      *from_coords* chỉ định một vùng con hình chữ nhật của hình ảnh nguồn cần sao chép, như trong phương thức :meth:`copy`.

      .. versionchanged:: 3.13
         Đã thêm tham số *from_coords*.


   .. method:: transparency_get(x, y)

      Trả về ``True`` nếu pixel tại tọa độ (*x*, *y*) hoàn toàn trong suốt; nếu không thì trả về ``False``.

      .. versionadded:: 3.8


   .. method:: transparency_set(x, y, boolean)

      Đặt pixel tại tọa độ (*x*, *y*) thành hoàn toàn trong suốt nếu *boolean* là true, nếu không thì thành hoàn toàn đục.

      .. versionadded:: 3.8


   .. method:: write(filename, format=None, from_coords=None, *, \
                     background=None, grayscale=False)

      Ghi dữ liệu hình ảnh từ ảnh vào tệp có tên *filename*.

      *format* chỉ định tên của trình xử lý định dạng tệp hình ảnh cần sử dụng. Nếu không được cung cấp, định dạng sẽ được suy đoán từ phần mở rộng tệp.

      *from_coords* chỉ định một vùng hình chữ nhật của ảnh cần được ghi. Giá trị này phải là một tuple hoặc một danh sách gồm từ 1 đến 4 số nguyên ``(x1, y1, x2, y2)``. Nếu chỉ chỉ định *x1* và *y1*, vùng sẽ kéo dài từ ``(x1, y1)`` đến góc dưới bên phải của ảnh. Nếu cung cấp đủ bốn tọa độ, chúng chỉ định hai góc đối diện theo đường chéo của vùng. Nếu không cung cấp *from_coords*, toàn bộ ảnh sẽ được ghi.

      Nếu chỉ định *background*, dữ liệu sẽ không chứa thông tin về độ trong suốt; trong tất cả các pixel trong suốt, màu sẽ được thay thế bằng màu đã chỉ định.

      Nếu *grayscale* là true, dữ liệu sẽ không chứa thông tin màu; toàn bộ dữ liệu pixel được chuyển thành thang độ xám.

      .. versionchanged:: 3.13
         Đã thêm các tham số *background* và *grayscale*.


   .. method:: zoom(x, y='', *, from_coords=None)

      Trả về một :class:`PhotoImage` mới với ảnh này được phóng đại theo hệ số *x* theo hướng X và *y* theo hướng Y. Nếu không cung cấp *y*, giá trị này mặc định giống với *x*.

      *from_coords* chỉ định một vùng con hình chữ nhật của hình ảnh nguồn cần sao chép, như trong phương thức :meth:`copy`.

      .. versionchanged:: 3.13
         Đã thêm tham số *from_coords*.



.. class:: BitmapImage(name=None, cnf={}, master=None, **kw)

   Một hình ảnh hai màu (kiểu hình ảnh Tk ``bitmap``) được tạo từ bitmap X11. Mỗi pixel hiển thị màu tiền cảnh, màu nền hoặc không hiển thị gì (tạo hiệu ứng trong suốt). Kế thừa từ :class:`Image`.

   Các tùy chọn cấu hình là *data* hoặc *file* (bitmap nguồn, được cung cấp dưới dạng chuỗi theo định dạng bitmap X11 hoặc tên của một tệp ở định dạng đó), *maskdata* hoặc *maskfile* (bitmap mặt nạ, với cùng các dạng trên), và *foreground* cùng *background* (hai màu). Với các pixel mà mặt nạ bằng không, hình ảnh không hiển thị gì; với các pixel khác, hình ảnh hiển thị màu tiền cảnh tại nơi nguồn bằng một và màu nền tại nơi nguồn bằng không. Nếu *background* được đặt thành chuỗi rỗng, các pixel nền sẽ trong suốt.

   :class:`!BitmapImage` không có phương thức riêng nào ngoài các phương thức được kế thừa từ
   :class:`Image`.


Các lớp khác
^^^^^^^^^^^^

.. class:: Event()

   Một vùng chứa các thuộc tính của một sự kiện được truyền đến một callback được liên kết bằng
   :meth:`Misc.bind`. Một instance :class:`!Event` có các thuộc tính sau, mỗi thuộc tính tương ứng với một trường của sự kiện Tk bên dưới; tùy thuộc vào loại sự kiện, một số thuộc tính có thể được đặt thành chuỗi ``'??'`` để cho biết chúng không có ý nghĩa. Xem :ref:`bindings-and-events`.

   .. attribute:: serial

      Số sê-ri của sự kiện.

   .. attribute:: num

      Nút chuột đã được nhấn hoặc thả (đối với các sự kiện nút).

   .. attribute:: focus

      Cửa sổ có đang được focus hay không (đối với các sự kiện ``Enter`` và ``Leave``).

   .. attribute:: height
                  width

      Chiều cao và chiều rộng mới của cửa sổ (đối với các sự kiện ``Configure`` và ``Expose``).

   .. attribute:: keycode

      keycode của phím đã được nhấn hoặc thả.

   .. attribute:: state

      Trạng thái của sự kiện, dưới dạng một số (đối với hầu hết các sự kiện) hoặc một chuỗi (đối với các sự kiện ``Visibility``).

   .. attribute:: time

      Dấu thời gian của sự kiện, tính bằng mili giây.

   .. attribute:: x
                  y

      Vị trí của con trỏ tương đối so với widget, tính bằng pixel.

   .. attribute:: x_root
                  y_root

      Vị trí của con trỏ tương đối so với góc trên bên trái của màn hình, tính bằng pixel.

   .. attribute:: char

      Ký tự được nhập, dưới dạng một chuỗi (đối với các sự kiện phím).

   .. attribute:: send_event

      ``True`` nếu sự kiện được gửi bởi một ứng dụng khác.

   .. attribute:: keysym

      Tên ký hiệu của phím đã được nhấn hoặc thả.

   .. attribute:: keysym_num

      Giá trị số của :attr:`keysym`.

   .. attribute:: type

      :class:`EventType` của sự kiện.

   .. attribute:: widget

      Widget nơi sự kiện xảy ra.

   .. attribute:: delta

      Mức độ xoay của con lăn chuột (đối với các sự kiện ``MouseWheel``).


.. class:: EventType(*values)

   Một :class:`enum.StrEnum` liệt kê các loại sự kiện Tk, được dùng làm giá trị của :attr:`Event.type`. Các thành phần của nó bao gồm, cùng với những thành phần khác, ``KeyPress``, ``KeyRelease``, ``ButtonPress``, ``ButtonRelease``, ``Motion``, ``Enter``, ``Leave``, ``FocusIn``, ``FocusOut``, ``Configure``, ``Map``, ``Unmap``, ``Expose``, ``Destroy`` và ``MouseWheel``.

   .. versionadded:: 3.6



.. class:: CallWrapper(func, subst, widget)

   Trợ giúp nội bộ bao bọc một callback Python để có thể gọi từ Tcl. *func* là hàm Python, *subst* là một hàm tùy chọn để tiền xử lý các đối số Tcl, còn *widget* là widget được dùng để báo lỗi. Các instance được :meth:`Misc.register` tự động tạo; thông thường không sử dụng trực tiếp class này.


Các hàm cấp mô-đun
^^^^^^^^^^^^^^^^^^

.. function:: Tcl(screenName=None, baseName=None, className='Tk', useTk=False)

   Hàm :func:`Tcl` là một hàm factory tạo ra một đối tượng tương tự đối tượng do class :class:`Tk` tạo ra, ngoại trừ việc nó không khởi tạo hệ thống Tk. Hàm này hữu ích nhất khi điều khiển trình thông dịch Tcl trong môi trường không muốn tạo các cửa sổ toplevel không cần thiết hoặc không thể tạo chúng (chẳng hạn như các hệ thống Unix/Linux không có X server). Một đối tượng được tạo bởi đối tượng :func:`Tcl` có thể tạo một cửa sổ Toplevel (đồng thời khởi tạo hệ thống Tk) bằng cách gọi phương thức :meth:`~Tk.loadtk` của nó.

.. function:: NoDefaultRoot()

   Ngăn việc tạo cửa sổ root mặc định ngầm. Sau đó, :mod:`!tkinter` không còn tự động tạo một root mặc định dùng chung, và các thao tác phụ thuộc vào root này — chẳng hạn như tạo một widget không chỉ rõ *master* — sẽ phát sinh :exc:`RuntimeError`. Hãy gọi hàm này sớm trong các ứng dụng lớn để chỉ rõ cửa sổ root.

.. function:: mainloop(n=0)

   Chạy vòng lặp sự kiện chính của Tk trên cửa sổ root mặc định cho đến khi tất cả các cửa sổ bị hủy. Tương đương với việc gọi :meth:`Misc.mainloop` trên root mặc định.

.. function:: getboolean(s)

   Chuyển đổi chuỗi boolean của Tcl *s* (một trong các giá trị ``'1'``, ``'true'``, ``'yes'``, ``'on'`` và các giá trị tương tự, hoặc các giá trị tương ứng với false) thành một giá trị Python
   :class:`bool`. Phát sinh :exc:`TclError` nếu giá trị không hợp lệ.

.. function:: getdouble(s)

   Chuyển *s* thành một số dấu phẩy động. Đây là :class:`float` tích hợp sẵn.

.. function:: getint(s)

   Chuyển *s* thành một số nguyên. Đây là :class:`int` tích hợp sẵn.

.. function:: image_names()

   Trả về tên của tất cả image hiện có trong interpreter của root mặc định.

.. function:: image_types()

   Trả về các loại image khả dụng (chẳng hạn như ``'photo'`` và ``'bitmap'``) trong interpreter của root mặc định.


.. _tkinter-file-handlers:

Bộ xử lý tệp
^^^^^^^^^^^^

Tk cho phép bạn đăng ký và hủy đăng ký một hàm callback, hàm này sẽ được gọi từ mainloop của Tk khi có thể thực hiện I/O trên một file descriptor. Mỗi file descriptor chỉ có thể đăng ký một handler. Mã ví dụ::

   import tkinter
   widget = tkinter.Tk()
   mask = tkinter.READABLE | tkinter.WRITABLE
   widget.tk.createfilehandler(file, mask, callback)
   ...
   widget.tk.deletefilehandler(file)

Tính năng này không khả dụng trên Windows.

Vì bạn không biết có bao nhiêu byte sẵn sàng để đọc, bạn có thể không muốn sử dụng :class:`~io.BufferedIOBase` hoặc :class:`~io.TextIOBase`
Các phương thức :meth:`~io.BufferedIOBase.read` hoặc :meth:`~io.IOBase.readline` sẽ buộc phải đọc một số byte được xác định trước. Đối với socket, :meth:`~socket.socket.recv` hoặc
các phương thức :meth:`~socket.socket.recvfrom` sẽ hoạt động tốt; đối với các tệp khác, hãy sử dụng thao tác đọc thô hoặc ``os.read(file.fileno(), maxbytecount)``.


.. method:: Widget.tk.createfilehandler(file, mask, func)

   Đăng ký hàm callback của trình xử lý tệp *func*. Đối số *file* có thể là một đối tượng có phương thức :meth:`~io.IOBase.fileno` (chẳng hạn như đối tượng tệp hoặc socket), hoặc một file descriptor dạng số nguyên. Đối số *mask* là sự kết hợp bằng phép OR của bất kỳ hằng số nào trong ba hằng số dưới đây. Callback được gọi như sau::

      callback(file, mask)


.. method:: Widget.tk.deletefilehandler(file)

   Hủy đăng ký trình xử lý tệp.


.. data:: READABLE
          WRITABLE EXCEPTION

   Các hằng số được sử dụng trong các đối số *mask*.


Hằng số
^^^^^^^

Các hằng số ký hiệu sau đây có trong cả hai namespace :mod:`!tkinter` và :mod:`!tkinter.constants`.

.. data:: TRUE
          YES ON

   Các giá trị Truthy, tất cả đều bằng số nguyên ``1``.

.. data:: FALSE
          NO OFF

   Các giá trị Falsy, tất cả đều bằng số nguyên ``0``.

.. data:: N
          S E W NE NW SE SW NS EW NSEW CENTER

   Các hướng la bàn (``'n'``, ``'s'``, ``'e'``, ``'w'`` và các hướng chéo, cạnh) cùng với ``CENTER`` (``'center'``), được dùng làm giá trị cho các tùy chọn *anchor* và *sticky*, cũng như bởi các phương thức như :meth:`Misc.grid_anchor`.

.. data:: LEFT
          RIGHT TOP BOTTOM

   Các cạnh cho tùy chọn *side* của packer (xem :meth:`Pack.pack_configure`).

.. data:: X
          Y BOTH NONE

   Các giá trị cho tùy chọn *fill* của packer: ``'x'``, ``'y'``, ``'both'`` hoặc ``'none'``.

.. data:: RAISED
          SUNKEN FLAT RIDGE GROOVE SOLID

   Các giá trị cho tùy chọn *relief*, tùy chọn kiểm soát đường viền 3-D của widget.

.. data:: HORIZONTAL
          VERTICAL

   Các giá trị cho tùy chọn *orient* của các widget như :class:`Scale`,
   :class:`Scrollbar` và :class:`PanedWindow`.

.. data:: CHAR
          WORD

   Các giá trị cho tùy chọn *wrap* của widget :class:`Text`, dùng để chọn cách ngắt dòng tại ranh giới ký tự hoặc từ.

.. data:: BASELINE

   Giá trị căn chỉnh văn bản ``'baseline'``.

.. data:: INSIDE
          OUTSIDE

   Các giá trị cho tùy chọn *bordermode* của placer (xem
   :meth:`Place.place_configure`).

.. data:: INSERT
          CURRENT END ANCHOR SEL SEL_FIRST SEL_LAST

   Các chỉ mục ký hiệu được sử dụng bởi các widget :class:`Text`, :class:`Entry`, :class:`Listbox` và :class:`Canvas`, chẳng hạn như ``'insert'`` (con trỏ chèn), ``'current'``, ``'end'``, ``'anchor'`` và các giới hạn của vùng chọn (``'sel.first'`` và ``'sel.last'``).

.. data:: ALL

   Thẻ đặc biệt ``'all'``, khớp với mọi mục của :class:`Canvas` hoặc mọi ký tự của :class:`Text` (ví dụ ``canvas.delete(ALL)``).

.. data:: NORMAL
          DISABLED ACTIVE HIDDEN

   Các giá trị cho tùy chọn *state* của nhiều widget và mục khác nhau.

.. data:: CASCADE
          CHECKBUTTON COMMAND RADIOBUTTON SEPARATOR

   Các loại mục menu, được dùng làm đối số *itemType* của :meth:`Menu.add` và
   :meth:`Menu.insert`.

.. data:: SINGLE
          BROWSE MULTIPLE EXTENDED

   Các giá trị cho tùy chọn *selectmode* của widget :class:`Listbox`.

.. data:: PIESLICE
          CHORD ARC

   Các giá trị cho tùy chọn *style* của các mục cung :class:`Canvas`.

.. data:: BUTT
          PROJECTING ROUND BEVEL MITER

   Các giá trị cho các tùy chọn *capstyle* (``'butt'``, ``'projecting'``, ``'round'``) và *joinstyle* (``'round'``, ``'bevel'``, ``'miter'``) của
   :class:`Canvas` các mục trên dòng.

.. data:: FIRST
          LAST

   Các giá trị cho tùy chọn *arrow* của :class:`Canvas` các mục dòng, cho biết đầu nào có đầu mũi tên.

.. data:: MOVETO
          SCROLL

   Đối số đầu tiên được một :class:`Scrollbar` truyền cho phương thức :meth:`XView.xview` hoặc :meth:`YView.yview` của widget được cuộn.

.. data:: UNITS
          PAGES

   Các giá trị cho đối số *what* của :meth:`XView.xview_scroll` và
   :meth:`YView.yview_scroll`.

.. data:: UNDERLINE
          NUMERIC DOTBOX

   Các giá trị tùy chọn khác: ``'underline'``, ``'numeric'`` và ``'dotbox'``.

.. _`TkDocs`: https://tkdocs.com/
.. _`Tkinter 8.5 reference: a GUI for Python`: https://www.tkdocs.com/shipman/
.. _`Tk commands`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/index.html
.. _`Tcl/Tk Home Page`: https://www.tcl.tk
.. _`Modern Tkinter for Busy Python Developers`: https://tkdocs.com/book.html
.. _`Python GUI programming with Tkinter`: https://www.packtpub.com/en-us/product/python-gui-programming-with-tkinter-9781788835886
.. _`Programming Python`: https://learning-python.com/about-pp4e.html
.. _`Tcl and the Tk Toolkit (2nd edition)`: https://www.amazon.com/exec/obidos/ASIN/032133633X
.. _`Tcl package`: https://wiki.tcl-lang.org/37432
.. _`ttk::button`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_button.html
.. _`grid`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/grid.html
.. _`options`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/options.html
.. _`ttk::widget`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_widget.html
.. _`winfo`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/winfo.html
.. _`Pillow`: https://python-pillow.org/
