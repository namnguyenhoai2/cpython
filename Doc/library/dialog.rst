Hộp thoại Tkinter
=================

:mod:`!tkinter.simpledialog` --- Hộp thoại nhập liệu Tkinter tiêu chuẩn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: tkinter.simpledialog
   :synopsis: Cửa sổ hộp thoại đơn giản

**Mã nguồn:** :source:`Lib/tkinter/simpledialog.py`

--------------

Mô-đun :mod:`!tkinter.simpledialog` chứa các lớp và hàm tiện ích để tạo các hộp thoại modal đơn giản nhằm nhận một giá trị từ người dùng.


.. function:: askfloat(title, prompt, *, initialvalue=None, minvalue=None, maxvalue=None, parent=None)
              askinteger(title, prompt, *, initialvalue=None, minvalue=None, maxvalue=None, parent=None) askstring(title, prompt, *, initialvalue=None, show=None, parent=None)

   Yêu cầu người dùng nhập một giá trị thuộc kiểu mong muốn và trả về giá trị đó, hoặc ``None`` nếu hộp thoại bị hủy.

   *title* là tiêu đề của hộp thoại, còn *prompt* là thông báo hiển thị phía trên ô nhập. *initialvalue* là giá trị được đặt sẵn trong ô nhập. *parent* là cửa sổ mà hộp thoại được hiển thị chồng lên.
   :func:`askinteger` và :func:`askfloat` cũng chấp nhận *minvalue* và *maxvalue*, dùng để giới hạn giá trị được chấp nhận.
   :func:`askstring` cũng chấp nhận *show*, một ký tự dùng để che văn bản đã nhập, chẳng hạn như ``'*'`` để ẩn mật khẩu.

.. class:: Dialog(parent, title=None)

   Lớp cơ sở cho các hộp thoại tùy chỉnh. Việc khởi tạo lớp này sẽ hiển thị hộp thoại theo chế độ modal và chỉ trả về khi người dùng đóng hộp thoại; giá trị đã nhập sau đó có trong thuộc tính :attr:`!result`.

   .. attribute:: result

      Giá trị do :meth:`apply` tạo ra, hoặc ``None`` nếu hộp thoại bị hủy.

   .. method:: body(master)

      Ghi đè để tạo giao diện hộp thoại và trả về widget cần được đặt tiêu điểm ban đầu.

   .. method:: buttonbox()

      Hành vi mặc định thêm các nút OK và Cancel. Ghi đè để tùy chỉnh bố cục nút.

   .. method:: validate()

      Xác thực dữ liệu do người dùng nhập. Trả về true nếu dữ liệu hợp lệ, khi đó hộp thoại tiếp tục
      :meth:`apply`; trả về false để giữ hộp thoại mở. Cách triển khai mặc định luôn trả về true; hãy ghi đè phương thức này để kiểm tra dữ liệu nhập.

   .. method:: apply()

      Xử lý dữ liệu do người dùng nhập, chẳng hạn bằng cách lưu trữ dữ liệu trong
      thuộc tính :attr:`!result`. Được gọi sau khi :meth:`validate` thành công và ngay trước khi hộp thoại bị hủy. Cách triển khai mặc định không thực hiện thao tác nào; hãy ghi đè phương thức này để xử lý hoặc lưu trữ kết quả.

   .. method:: destroy()

      Hủy cửa sổ hộp thoại, đồng thời xóa tham chiếu đến widget đang nhận focus ban đầu.


.. class:: SimpleDialog(master, text='', buttons=[], default=None, cancel=None, title=None, class_=None)

   Một hộp thoại modal đơn giản hiển thị thông báo *text* phía trên một hàng nút nhấn có nhãn được chỉ định bởi *buttons*, đồng thời trả về chỉ mục của nút mà người dùng nhấn. *default* là chỉ mục của nút được kích hoạt bằng phím Return, *cancel* là chỉ mục được trả về khi cửa sổ bị đóng thông qua window manager, *title* là tiêu đề cửa sổ, còn *class_* là tên lớp Tk của cửa sổ.

   .. method:: go()

      Hiển thị hộp thoại, chờ người dùng nhấn một nút hoặc đóng cửa sổ, rồi trả về chỉ mục của nút được chọn.



:mod:`!tkinter.filedialog` --- Hộp thoại chọn tệp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: tkinter.filedialog
   :synopsis: Các lớp hộp thoại để chọn tệp

**Mã nguồn:** :source:`Lib/tkinter/filedialog.py`

--------------

Mô-đun :mod:`!tkinter.filedialog` cung cấp các lớp và hàm factory để tạo cửa sổ chọn tệp/thư mục.

Hộp thoại tải/lưu gốc
---------------------

Các lớp và hàm sau đây cung cấp những cửa sổ hộp thoại tệp kết hợp giao diện và cảm nhận gốc với các tùy chọn cấu hình để tùy chỉnh hành vi. Các đối số từ khóa sau áp dụng cho những lớp và hàm được liệt kê bên dưới:

 | *parent* - cửa sổ để đặt hộp thoại lên trên

 | *title* - tiêu đề của cửa sổ

 | *initialdir* - thư mục mà hộp thoại bắt đầu mở

 | *initialfile* - tệp được chọn khi mở hộp thoại

 | *filetypes* - một chuỗi các tuple (label, pattern), cho phép wildcard '*'

 | *defaultextension* - phần mở rộng mặc định được thêm vào tệp (hộp thoại lưu)

 | *multiple* - khi là true, cho phép chọn nhiều mục


**Static factory functions**

Các hàm dưới đây khi được gọi sẽ tạo một hộp thoại modal có giao diện gốc, chờ người dùng lựa chọn rồi trả về lựa chọn đó. Giá trị trả về chính xác phụ thuộc vào hàm (xem bên dưới); khi hộp thoại bị hủy, giá trị đó là một chuỗi rỗng, một tuple rỗng hoặc ``None``. Kiểu chính xác của giá trị rỗng này có thể khác nhau giữa các nền tảng và phiên bản Tk, vì vậy hãy kiểm tra kết quả theo giá trị đúng (truth) thay vì so sánh với một giá trị cụ thể.

.. function:: askopenfile(mode="r", **options)
              askopenfiles(mode="r", ****options)

   Tạo một hộp thoại :class:`Open`.
   :func:`askopenfile` trả về đối tượng tệp đã mở hoặc ``None`` nếu hộp thoại bị hủy.
   :func:`askopenfiles` trả về danh sách các đối tượng tệp đã mở hoặc một tuple rỗng nếu bị hủy. Các tệp được mở ở chế độ *mode* (chỉ đọc ``'r'`` theo mặc định).

.. function:: asksaveasfile(mode="w", **options)

   Tạo một hộp thoại :class:`SaveAs` và trả về đối tượng tệp đã mở hoặc ``None`` nếu hộp thoại bị hủy. Tệp được mở ở chế độ *mode* (``'w'`` theo mặc định).

.. function:: askopenfilename(**options)
              askopenfilenames(****options)

   Tạo một hộp thoại :class:`Open`.
   :func:`askopenfilename` trả về tên tệp đã chọn dưới dạng chuỗi hoặc chuỗi rỗng nếu hộp thoại bị hủy.
   :func:`askopenfilenames` trả về một tuple chứa các tên tệp đã chọn hoặc một tuple rỗng nếu bị hủy.

.. function:: asksaveasfilename(**options)

   Tạo một hộp thoại :class:`SaveAs` và trả về tên tệp đã chọn dưới dạng chuỗi hoặc chuỗi rỗng nếu hộp thoại bị hủy.

.. function:: askdirectory(**options)

   Nhắc người dùng chọn một thư mục và trả về đường dẫn của thư mục đó dưới dạng chuỗi hoặc chuỗi rỗng nếu hộp thoại bị hủy. Tùy chọn keyword bổ sung: *mustexist* - nếu là true, người dùng chỉ có thể chọn một thư mục hiện có (theo mặc định là false).

.. class:: Open(master=None, **options)
           SaveAs(master=None, ****options) Directory(master=None, ****options)

   Ba lớp trên cung cấp các cửa sổ hộp thoại native để tải và lưu tệp cũng như chọn một thư mục.

**Các lớp tiện ích**

Các lớp dưới đây được dùng để tạo cửa sổ tệp/thư mục từ đầu. Chúng không mô phỏng giao diện và cách thức hoạt động nguyên bản của nền tảng.

.. note::  Lớp *FileDialog* nên được phân lớp để xử lý sự kiện và hành vi tùy chỉnh.

.. class:: FileDialog(master, title=None)

   Tạo hộp thoại chọn tệp cơ bản.

   .. method:: cancel_command(event=None)

      Kích hoạt việc kết thúc cửa sổ hộp thoại.

   .. method:: dirs_double_event(event)

      Trình xử lý sự kiện double-click trên thư mục.

   .. method:: dirs_select_event(event)

      Trình xử lý sự kiện click trên thư mục.

   .. method:: files_double_event(event)

      Trình xử lý sự kiện double-click trên tệp.

   .. method:: files_select_event(event)

      Trình xử lý sự kiện single-click trên tệp.

   .. method:: filter_command(event=None)

      Lọc các tệp theo thư mục.

   .. method:: get_filter()

      Lấy bộ lọc tệp hiện đang được sử dụng.

   .. method:: get_selection()

      Lấy mục hiện được chọn.

   .. method:: go(dir_or_file=os.curdir, pattern="*", default="", key=None)

      Hiển thị hộp thoại và bắt đầu vòng lặp sự kiện.

   .. method:: ok_event(event)

      Thoát hộp thoại và trả về lựa chọn hiện tại.

   .. method:: ok_command()

      Được gọi khi người dùng xác nhận lựa chọn hiện tại. Phần triển khai cơ sở chấp nhận lựa chọn và đóng hộp thoại;
      :class:`LoadFileDialog` và :class:`SaveFileDialog` ghi đè phương thức này để kiểm tra lựa chọn trước.

   .. method:: quit(how=None)

      Thoát hộp thoại và trả về tên tệp, nếu có.

   .. method:: set_filter(dir, pat)

      Đặt bộ lọc tệp.

   .. method:: set_selection(file)

      Cập nhật lựa chọn tệp hiện tại thành *file*.


.. class:: LoadFileDialog(master, title=None)

   Một lớp con của FileDialog tạo cửa sổ hộp thoại để chọn một tệp hiện có.

   .. method:: ok_command()

      Kiểm tra rằng một tệp đã được cung cấp và lựa chọn cho biết đó là một tệp đã tồn tại.

.. class:: SaveFileDialog(master, title=None)

   Một lớp con của FileDialog tạo cửa sổ hộp thoại để chọn tệp đích.

   .. method:: ok_command()

      Kiểm tra xem lựa chọn có trỏ đến một tệp hợp lệ không phải là thư mục hay không. Cần xác nhận nếu một tệp đã tồn tại được chọn.

:mod:`!tkinter.commondialog` --- Mẫu cửa sổ hộp thoại
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: tkinter.commondialog
   :synopsis: Lớp cơ sở Tkinter cho các hộp thoại

**Mã nguồn:** :source:`Lib/tkinter/commondialog.py`

--------------

Mô-đun :mod:`!tkinter.commondialog` cung cấp lớp :class:`Dialog`, là lớp cơ sở cho các hộp thoại được định nghĩa trong những mô-đun hỗ trợ khác.

.. class:: Dialog(master=None, **options)

   .. method:: show(**options)

      Hiển thị cửa sổ Dialog.


:mod:`!tkinter.dialog` --- Hộp thoại Tk cổ điển
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: tkinter.dialog
   :synopsis: Một hộp thoại đơn giản được xây dựng trên các widget Tk cổ điển.

**Mã nguồn:** :source:`Lib/tkinter/dialog.py`

--------------

Mô-đun :mod:`!tkinter.dialog` cung cấp một hộp thoại modal đơn giản được xây dựng trên các widget Tk cổ điển (không theo chủ đề).

.. data:: DIALOG_ICON

   Tên của một bitmap (``'questhead'``) thích hợp để sử dụng làm *bitmap* của một :class:`Dialog`.

.. class:: Dialog(master=None, cnf={}, **kw)

   Hiển thị một hộp thoại modal được xây dựng từ các widget Tk cổ điển (không theo chủ đề) và chờ người dùng nhấn một trong các nút của hộp thoại. Các tùy chọn, được cung cấp thông qua *cnf* hoặc dưới dạng đối số từ khóa, đều bắt buộc: *title* (tiêu đề cửa sổ), *text* (thông báo), *bitmap* (tên của biểu tượng bitmap, chẳng hạn như :data:`DIALOG_ICON`), *default* (chỉ mục của nút mặc định) và *strings* (chuỗi nhãn nút). Sau khi khởi tạo, thuộc tính :attr:`!num` chứa chỉ mục của nút mà người dùng đã nhấn.

   .. method:: destroy()

      Không thực hiện thao tác nào. Cửa sổ hộp thoại được tự động hủy trước khi hàm khởi tạo trả về, vì vậy phương thức này không còn việc gì cần thực hiện.


.. seealso::

   Các module :mod:`tkinter.messagebox`, :ref:`tut-files`
