:mod:`!tkinter.ttk` --- Widget theo chủ đề Tk
=============================================

.. module:: tkinter.ttk
   :synopsis: Bộ widget theo chủ đề Tk

.. sectionauthor:: Guilherme Polo <ggpolo@gmail.com>

**Mã nguồn:** :source:`Lib/tkinter/ttk.py`

.. index:: single: ttk

--------------

Mô-đun :mod:`!tkinter.ttk` cung cấp quyền truy cập vào bộ widget theo chủ đề Tk, được giới thiệu trong Tk 8.5. Các widget này điều chỉnh giao diện theo chủ đề gốc của nền tảng, mang lại cho ứng dụng giao diện đẹp hơn và nhất quán hơn so với các widget :mod:`tkinter` cổ điển, vốn có giao diện cố định.

Ý tưởng cơ bản của :mod:`!tkinter.ttk` là tách biệt, trong phạm vi có thể, mã triển khai hành vi của widget khỏi mã triển khai giao diện của nó.

Các widget Ttk được sử dụng giống như các widget :mod:`tkinter` cổ điển và dùng chung cơ chế: hệ thống phân cấp widget, các trình quản lý hình học, liên kết biến và liên kết sự kiện. Những khái niệm nền tảng này được trình bày trong tài liệu :mod:`tkinter` và không được lặp lại ở đây.

.. versionadded:: 3.1


.. seealso::

   `Hỗ trợ tạo kiểu cho Widget Tk (TIP #48) <https://tip.tcl-lang.org/48.html>`_
      Đề xuất Cải tiến Tcl đã giới thiệu engine tạo kiểu cho widget theo theme.


Sử dụng Ttk
-----------

Để bắt đầu sử dụng Ttk, hãy import module của nó::

   from tkinter import ttk

Để ghi đè các widget Tk cơ bản, câu lệnh import phải theo sau câu lệnh import Tk::

   from tkinter import *
   from tkinter.ttk import *

Đoạn mã đó khiến một số widget :mod:`!tkinter.ttk` (:class:`Button`,
:class:`Checkbutton`, :class:`Entry`, :class:`Frame`, :class:`Label`,
:class:`LabelFrame`, :class:`Menubutton`, :class:`OptionMenu`,
:class:`PanedWindow`, :class:`Radiobutton`, :class:`Scale`,
:class:`Scrollbar` và :class:`Spinbox`) tự động thay thế các widget Tk.

.. note::

   Việc ghi đè các widget cổ điển bằng ``from tkinter.ttk import *`` thuận tiện khi điều chỉnh mã hiện có, nhưng mã mới thường rõ ràng hơn nếu import module dưới tên ``from tkinter import ttk`` và tham chiếu rõ ràng đến các widget theo theme, chẳng hạn như ``ttk.Button``.

Điều này mang lại lợi ích trực tiếp là sử dụng các widget mới, giúp giao diện và trải nghiệm nhất quán hơn trên các nền tảng; tuy nhiên, các widget thay thế không hoàn toàn tương thích. Điểm khác biệt chính là các tùy chọn widget như ``fg``, ``bg`` và những tùy chọn khác liên quan đến kiểu dáng widget không còn xuất hiện trong các widget Ttk. Thay vào đó, hãy sử dụng lớp :class:`ttk.Style <Style>` để cải thiện hiệu ứng kiểu dáng.


Các widget Ttk
--------------

Ttk đi kèm 18 widget, trong đó 12 widget đã tồn tại trong tkinter:
:class:`Button`, :class:`Checkbutton`, :class:`Entry`, :class:`Frame`,
:class:`Label`, :class:`LabelFrame`, :class:`Menubutton`, :class:`PanedWindow`,
:class:`Radiobutton`, :class:`Scale`, :class:`Scrollbar` và :class:`Spinbox`. Sáu widget còn lại là: :class:`Combobox`, :class:`Notebook`,
:class:`Progressbar`, :class:`Separator`, :class:`Sizegrip` và
:class:`Treeview`. Tất cả đều là lớp con của :class:`Widget`.

Sử dụng các widget Ttk giúp ứng dụng có giao diện và trải nghiệm tốt hơn. Như đã thảo luận ở trên, có những khác biệt trong cách viết mã kiểu dáng.

Mã Tk::

   l1 = tkinter.Label(text="Test", fg="black", bg="white")
   l2 = tkinter.Label(text="Test", fg="black", bg="white")


Mã Ttk::

   style = ttk.Style()
   style.configure("BW.TLabel", foreground="black", background="white")

   l1 = ttk.Label(text="Test", style="BW.TLabel")
   l2 = ttk.Label(text="Test", style="BW.TLabel")

Để biết thêm thông tin về TtkStyling_, hãy xem tài liệu về lớp :class:`Style`.

Widget
------

:class:`ttk.Widget <Widget>` định nghĩa các tùy chọn và phương thức tiêu chuẩn được các widget theo chủ đề của Tk hỗ trợ và không được thiết kế để khởi tạo trực tiếp.


Tùy chọn tiêu chuẩn
^^^^^^^^^^^^^^^^^^^

Tất cả các widget :mod:`!ttk` đều chấp nhận các tùy chọn sau:

.. tabularcolumns:: |l|L|

+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn  | Mô tả                                                                                                                                                                                                                                                                                                                                                                                                        |
+===========+==============================================================================================================================================================================================================================================================================================================================================================================================================+
| class     | Chỉ định lớp của cửa sổ. Lớp này được sử dụng khi truy vấn cơ sở dữ liệu tùy chọn cho các tùy chọn khác của cửa sổ, để xác định bindtags mặc định cho cửa sổ và chọn bố cục cũng như kiểu mặc định của widget. Tùy chọn này chỉ đọc và chỉ có thể được chỉ định khi cửa sổ được tạo.                                                                                                                         |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| cursor    | Chỉ định con trỏ chuột được sử dụng cho widget. Xem kiểu tùy chọn *cursor* trong :ref:`Tk-option-data-types`. Nếu được đặt thành chuỗi rỗng (mặc định), con trỏ sẽ được kế thừa từ widget cha.                                                                                                                                                                                                               |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| takefocus | Xác định liệu cửa sổ có nhận được focus trong quá trình duyệt bằng bàn phím hay không. Giá trị trả về là 0, 1 hoặc một chuỗi rỗng. Nếu trả về 0, điều đó có nghĩa là cửa sổ sẽ bị bỏ qua hoàn toàn trong quá trình duyệt bằng bàn phím. Nếu là 1, cửa sổ sẽ nhận focus đầu vào miễn là cửa sổ đó có thể hiển thị. Còn chuỗi rỗng có nghĩa là các tập lệnh duyệt sẽ quyết định có focus vào cửa sổ hay không. |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| style     | Có thể được dùng để chỉ định kiểu widget tùy chỉnh.                                                                                                                                                                                                                                                                                                                                                          |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


.. _`Scrollable widget options`:

Tùy chọn widget có thể cuộn
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các tùy chọn sau được các widget do thanh cuộn điều khiển hỗ trợ.

.. tabularcolumns:: |l|L|

+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn       | Mô tả                                                                                                                                                         |
+================+===============================================================================================================================================================+
| xscrollcommand | Dùng để giao tiếp với các thanh cuộn ngang.                                                                                                                   |
|                |                                                                                                                                                               |
|                | Khi chế độ xem trong cửa sổ của widget thay đổi, widget sẽ gọi callback *xscrollcommand*.                                                                     |
|                |                                                                                                                                                               |
|                | Thông thường, tùy chọn này bao gồm method                                                                                                                     |
|                | :meth:`Scrollbar.set <tkinter.Scrollbar.set>` của một thanh cuộn nào đó. Điều này sẽ khiến thanh cuộn được cập nhật mỗi khi chế độ xem trong cửa sổ thay đổi. |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| yscrollcommand | Dùng để giao tiếp với các thanh cuộn dọc. Để biết thêm thông tin, hãy xem phần trên.                                                                          |
+----------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+


Các tùy chọn nhãn
^^^^^^^^^^^^^^^^^

Các tùy chọn sau được nhãn, nút và các widget tương tự nút hỗ trợ.

.. tabularcolumns:: |l|p{0.7\linewidth}|

+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn     | Mô tả                                                                                                                                                                                                                                                                                                                                                                                         |
+==============+===============================================================================================================================================================================================================================================================================================================================================================================================+
| text         | Chỉ định một chuỗi văn bản sẽ được hiển thị bên trong widget.                                                                                                                                                                                                                                                                                                                                 |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| textvariable | Chỉ định một tên có giá trị được sử dụng thay cho tài nguyên tùy chọn text.                                                                                                                                                                                                                                                                                                                   |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| underline    | Nếu được đặt, chỉ định chỉ mục (bắt đầu từ 0) của một ký tự cần gạch chân trong chuỗi văn bản. Ký tự được gạch chân được dùng để kích hoạt mnemonic.                                                                                                                                                                                                                                          |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| image        | Chỉ định một image cần hiển thị. Đây là danh sách gồm 1 hoặc nhiều phần tử. Phần tử đầu tiên là tên image mặc định. Phần còn lại của danh sách là một chuỗi các cặp statespec/value như được định nghĩa bởi :meth:`Style.map`, chỉ định các image khác nhau cần sử dụng khi widget ở một trạng thái cụ thể hoặc kết hợp các trạng thái. Tất cả image trong danh sách phải có cùng kích thước. |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| compound     | Chỉ định cách hiển thị image tương đối với văn bản trong trường hợp có cả tùy chọn text và image. Các giá trị hợp lệ là:                                                                                                                                                                                                                                                                      |
|              |                                                                                                                                                                                                                                                                                                                                                                                               |
|              | * text: chỉ hiển thị văn bản                                                                                                                                                                                                                                                                                                                                                                  |
|              | * image: chỉ hiển thị hình ảnh                                                                                                                                                                                                                                                                                                                                                                |
|              | * top, bottom, left, right: lần lượt hiển thị hình ảnh ở phía trên, phía dưới, bên trái hoặc bên phải văn bản.                                                                                                                                                                                                                                                                                |
|              | * none: mặc định. hiển thị hình ảnh nếu có, nếu không thì hiển thị văn bản.                                                                                                                                                                                                                                                                                                                   |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| width        | Nếu lớn hơn 0, chỉ định lượng không gian, tính theo độ rộng ký tự, cần cấp cho nhãn văn bản; nếu nhỏ hơn 0, chỉ định độ rộng tối thiểu. Nếu bằng 0 hoặc không được chỉ định, độ rộng tự nhiên của nhãn văn bản sẽ được sử dụng.                                                                                                                                                               |
+--------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Các tùy chọn tương thích
^^^^^^^^^^^^^^^^^^^^^^^^

.. tabularcolumns:: |l|L|

+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn | Mô tả                                                                                                                                                                                                                                          |
+==========+================================================================================================================================================================================================================================================+
| state    | Có thể được đặt thành "normal" hoặc "disabled" để điều khiển bit trạng thái "disabled". Đây là tùy chọn chỉ ghi: việc đặt tùy chọn này sẽ thay đổi trạng thái widget, nhưng phương thức :meth:`Widget.state` không ảnh hưởng đến tùy chọn này. |
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Trạng thái widget
^^^^^^^^^^^^^^^^^

Trạng thái widget là một bitmap gồm các cờ trạng thái độc lập.

.. tabularcolumns:: |l|L|

+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Cờ         | Mô tả                                                                                                                                                                                        |
+============+==============================================================================================================================================================================================+
| active     | Con trỏ chuột đang ở trên widget và việc nhấn nút chuột sẽ khiến một hành động nào đó xảy ra                                                                                                 |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| disabled   | Widget bị vô hiệu hóa theo điều khiển của chương trình                                                                                                                                       |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| focus      | Widget đang có focus bàn phím                                                                                                                                                                |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| pressed    | Widget đang được nhấn                                                                                                                                                                        |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| selected   | "On", "true" hoặc "current" cho những thành phần như Checkbutton và radiobutton                                                                                                              |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| background | Windows và Mac có khái niệm về cửa sổ "active" hoặc cửa sổ tiền cảnh. Trạng thái *background* được đặt cho các widget trong cửa sổ nền và được xóa đối với các widget trong cửa sổ tiền cảnh |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| readonly   | Widget không được cho phép người dùng sửa đổi                                                                                                                                                |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| alternate  | Định dạng hiển thị thay thế dành riêng cho widget                                                                                                                                            |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| invalid    | Giá trị của widget không hợp lệ                                                                                                                                                              |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Một đặc tả trạng thái là một chuỗi các tên trạng thái, có thể được thêm dấu chấm than ở đầu để cho biết bit đang tắt.


ttk.Widget
^^^^^^^^^^

Ngoài các phương thức được mô tả dưới đây, :class:`ttk.Widget <Widget>` hỗ trợ các phương thức :meth:`tkinter.Widget.cget <tkinter.Misc.cget>` và
:meth:`tkinter.Widget.configure <tkinter.Misc.configure>`.

.. class:: Widget

   .. method:: identify(x, y)

      Trả về tên của phần tử tại vị trí *x* *y*, hoặc chuỗi rỗng nếu điểm đó không nằm trong phần tử nào.

      *x* và *y* là tọa độ pixel tương đối so với widget.


   .. method:: instate(statespec, callback=None, *args, **kw)

      Kiểm tra trạng thái của widget. Nếu không chỉ định callback, trả về ``True`` nếu trạng thái của widget khớp với *statespec* và ``False`` trong trường hợp ngược lại. Nếu chỉ định callback, callback sẽ được gọi với các đối số args nếu trạng thái của widget khớp với *statespec*.


   .. method:: state(statespec=None)

      Sửa đổi hoặc truy vấn trạng thái của widget. Nếu chỉ định *statespec*, đặt trạng thái của widget theo đó và trả về một *statespec* mới cho biết các cờ nào đã được thay đổi. Nếu không chỉ định *statespec*, trả về các cờ trạng thái hiện đang được bật.

      Không nên nhầm lẫn với :meth:`Wm.state <tkinter.Wm.state>`.

   *statespec* thường sẽ là một list hoặc tuple.


Combobox
--------

Widget :class:`ttk.Combobox <Combobox>` kết hợp một trường văn bản với danh sách giá trị bật xuống. Widget này là một lớp con của :class:`Entry`.

Ngoài các phương thức kế thừa từ :class:`Widget`: :meth:`~tkinter.Misc.cget`,
:meth:`~tkinter.Misc.configure`, :meth:`~Widget.identify`,
:meth:`~Widget.instate` và :meth:`~Widget.state`, cùng các phương thức sau đây kế thừa từ :class:`Entry`: :meth:`~Entry.bbox`, :meth:`~tkinter.Entry.delete`,
:meth:`~tkinter.Entry.icursor`, :meth:`~tkinter.Entry.index`,
:meth:`~tkinter.Entry.insert`,
:meth:`selection* <tkinter.Entry.selection_adjust>`,
:meth:`xview* <tkinter.XView.xview>`, widget này còn có một số phương thức khác, được mô tả tại
:class:`ttk.Combobox <Combobox>`.


Options
^^^^^^^

Widget này chấp nhận các tùy chọn cụ thể sau:

.. tabularcolumns:: |l|L|

+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn        | Mô tả                                                                                                                                                                                                                                                                                                                                     |
+=================+===========================================================================================================================================================================================================================================================================================================================================+
| exportselection | Giá trị Boolean. Nếu được đặt, vùng chọn của widget sẽ được liên kết với vùng chọn X (có thể trả về bằng cách gọi Misc.selection_get, chẳng hạn).                                                                                                                                                                                         |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| justify         | Chỉ định cách văn bản được căn chỉnh trong widget. Một trong các giá trị "left", "center" hoặc "right".                                                                                                                                                                                                                                   |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| height          | Chỉ định chiều cao của hộp danh sách xổ xuống, tính theo số hàng.                                                                                                                                                                                                                                                                         |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| postcommand     | Một script (có thể đã được đăng ký bằng Misc.register) được gọi ngay trước khi hiển thị các giá trị. Script này có thể chỉ định những giá trị cần hiển thị.                                                                                                                                                                               |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| state           | Một trong các giá trị "normal", "readonly" hoặc "disabled". Ở trạng thái "readonly", không thể chỉnh sửa trực tiếp giá trị và người dùng chỉ có thể chọn một trong các giá trị từ danh sách thả xuống. Ở trạng thái "normal", trường văn bản có thể được chỉnh sửa trực tiếp. Ở trạng thái "disabled", không thể thực hiện tương tác nào. |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| textvariable    | Chỉ định một tên có giá trị được liên kết với giá trị của widget. Bất cứ khi nào giá trị liên kết với tên đó thay đổi, giá trị của widget cũng được cập nhật và ngược lại. Xem :class:`tkinter.StringVar`.                                                                                                                                |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| values          | Chỉ định danh sách các giá trị cần hiển thị trong hộp danh sách thả xuống.                                                                                                                                                                                                                                                                |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| width           | Chỉ định một giá trị số nguyên cho biết chiều rộng mong muốn của cửa sổ nhập, tính theo số ký tự có kích thước trung bình trong phông chữ của widget.                                                                                                                                                                                     |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. note::

   Tk 9.1 đã bổ sung tùy chọn *locale*, dùng để chọn locale được sử dụng nhằm xác định ranh giới từ và ký tự trong văn bản (mặc định là ``"C"``).


Sự kiện ảo
^^^^^^^^^^

Các widget combobox tạo ra sự kiện ảo **<<ComboboxSelected>>** khi người dùng chọn một phần tử từ danh sách các giá trị.


ttk.Combobox
^^^^^^^^^^^^

.. class:: Combobox

   .. method:: current(newindex=None)

      Nếu *newindex* được chỉ định, đặt giá trị của combobox thành vị trí phần tử *newindex*. Nếu không, trả về chỉ mục của giá trị hiện tại hoặc -1 nếu giá trị hiện tại không có trong danh sách values.


   .. method:: get()

      Trả về giá trị hiện tại của combobox.


   .. method:: set(value)

      Đặt giá trị của combobox thành *value*.


Spinbox
-------

Widget :class:`ttk.Spinbox <Spinbox>` là một :class:`ttk.Entry <Entry>` được bổ sung các mũi tên tăng và giảm. Widget này có thể được sử dụng cho các số hoặc danh sách giá trị chuỗi. Widget này là một lớp con của :class:`Entry`. Ngoài các phương thức được kế thừa từ :class:`Widget`: :meth:`~tkinter.Misc.cget`,
:meth:`~tkinter.Misc.configure`, :meth:`~Widget.identify`,
:meth:`~Widget.instate` và :meth:`~Widget.state`, cùng các phương thức sau được kế thừa từ :class:`Entry`: :meth:`~Entry.bbox`, :meth:`~tkinter.Entry.delete`,
:meth:`~tkinter.Entry.icursor`, :meth:`~tkinter.Entry.index`,
:meth:`~tkinter.Entry.insert`, :meth:`xview* <tkinter.XView.xview>`, nó còn có một số phương thức khác, được mô tả tại :class:`ttk.Spinbox <Spinbox>`.

Options
^^^^^^^

Widget này chấp nhận các tùy chọn cụ thể sau:

.. tabularcolumns:: |l|L|

+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn  | Mô tả                                                                                                                                                                                                                             |
+===========+===================================================================================================================================================================================================================================+
| from      | Giá trị dấu phẩy động. Nếu được đặt, đây là giá trị tối thiểu mà nút giảm sẽ giảm xuống. Phải được viết là ``from_`` khi được dùng làm đối số, vì ``from`` là một từ khóa Python.                                                 |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| to        | Giá trị số thực. Nếu được đặt, đây là giá trị tối đa mà nút increment sẽ tăng đến.                                                                                                                                                |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| increment | Giá trị số thực. Chỉ định mức thay đổi giá trị của các nút increment/decrement. Mặc định là 1.0.                                                                                                                                  |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| values    | Chuỗi các giá trị dạng chuỗi hoặc số thực. Nếu được chỉ định, các nút increment/decrement sẽ lần lượt chuyển qua các mục trong chuỗi này thay vì tăng hoặc giảm các số.                                                           |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| wrap      | Giá trị Boolean. Nếu ``True``, các nút tăng và giảm sẽ lần lượt chuyển từ giá trị ``to`` sang giá trị ``from`` hoặc từ giá trị ``from`` sang giá trị ``to``.                                                                      |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| format    | Giá trị chuỗi. Giá trị này chỉ định định dạng của các số được thiết lập bằng các nút tăng/giảm. Giá trị phải có dạng "%W.Pf", trong đó W là độ rộng được đệm của giá trị, P là độ chính xác, còn '%' và 'f' là các ký tự cố định. |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| command   | Python callable. Sẽ được gọi không có đối số mỗi khi người dùng nhấn một trong các nút tăng hoặc giảm.                                                                                                                            |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Sự kiện ảo
^^^^^^^^^^

Widget spinbox tạo một sự kiện ảo **<<Increment>>** khi người dùng nhấn <Up>, và một sự kiện ảo **<<Decrement>>** khi người dùng nhấn <Down>.

ttk.Spinbox
^^^^^^^^^^^

.. class:: Spinbox

   Với bước tăng không phải số nguyên, hãy xem :ref:`các giá trị số và locale <tkinter-numeric-locale>`.

   .. versionadded:: 3.8

   .. method:: get()

      Trả về giá trị hiện tại của spinbox.


   .. method:: set(value)

      Đặt giá trị của spinbox thành *value*.



Notebook
--------

Widget Ttk Notebook quản lý một tập hợp các cửa sổ và hiển thị từng cửa sổ một. Mỗi cửa sổ con được liên kết với một tab mà người dùng có thể chọn để thay đổi cửa sổ hiện đang hiển thị.


Options
^^^^^^^

Widget này chấp nhận các tùy chọn cụ thể sau:

.. tabularcolumns:: |l|L|

+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn | Mô tả                                                                                                                                                                                                                                                                             |
+==========+===================================================================================================================================================================================================================================================================================+
| height   | Nếu được cung cấp và lớn hơn 0, chỉ định chiều cao mong muốn của vùng pane (không bao gồm phần đệm bên trong hoặc các tab). Nếu không, chiều cao tối đa của tất cả pane sẽ được sử dụng.                                                                                          |
+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| padding  | Chỉ định khoảng không gian bổ sung cần thêm xung quanh bên ngoài notebook. padding là một danh sách gồm tối đa bốn đặc tả độ dài theo thứ tự trái trên phải dưới. Nếu chỉ định ít hơn bốn phần tử, bottom mặc định bằng top, right mặc định bằng left, và top mặc định bằng left. |
+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| width    | Nếu được chỉ định và lớn hơn 0, giá trị này chỉ định chiều rộng mong muốn của vùng pane (không bao gồm phần đệm bên trong). Nếu không, chiều rộng tối đa của tất cả các pane sẽ được sử dụng.                                                                                     |
+----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


.. _`Tab options`:

Tùy chọn tab
^^^^^^^^^^^^

Ngoài ra còn có các tùy chọn cụ thể cho tab:

.. tabularcolumns:: |l|L|

+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Option    | Description                                                                                                                                                                                                                                                                          |
+===========+======================================================================================================================================================================================================================================================================================+
| state     | "normal", "disabled" hoặc "hidden". Nếu là "disabled" thì không thể chọn tab. Nếu là "hidden" thì tab không được hiển thị.                                                                                                                                                           |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| sticky    | Chỉ định cách định vị cửa sổ con trong vùng pane. Giá trị là một chuỗi chứa không hoặc nhiều ký tự "n", "s", "e" hoặc "w". Mỗi chữ cái tương ứng với một phía (bắc, nam, đông hoặc tây) mà cửa sổ con sẽ được gắn vào, theo trình quản lý hình học :meth:`grid <tkinter.Grid.grid>`. |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| padding   | Chỉ định lượng khoảng trống bổ sung cần thêm giữa notebook và pane này. Cú pháp giống với tùy chọn padding được widget này sử dụng.                                                                                                                                                  |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| text      | Chỉ định văn bản sẽ được hiển thị trên tab.                                                                                                                                                                                                                                          |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| image     | Chỉ định hình ảnh sẽ hiển thị trong tab. Xem tùy chọn image được mô tả trong :class:`Widget`.                                                                                                                                                                                        |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| compound  | Chỉ định cách hiển thị hình ảnh so với văn bản trong trường hợp có cả hai tùy chọn text và image. Xem `Label Options <Label Options_>`_ để biết các giá trị hợp lệ.                                                                                                                  |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| underline | Chỉ định chỉ mục (bắt đầu từ 0) của một ký tự cần gạch chân trong chuỗi văn bản. Ký tự được gạch chân sẽ được dùng để kích hoạt mnemonic nếu :meth:`Notebook.enable_traversal` được gọi.                                                                                             |
+-----------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Các mã định danh của tab
^^^^^^^^^^^^^^^^^^^^^^^^

tab_id có trong một số phương thức của :class:`ttk.Notebook <Notebook>` có thể có bất kỳ dạng nào sau đây:

* Một số nguyên từ 0 đến số lượng thẻ
* Tên của một cửa sổ con
* Một đặc tả vị trí có dạng "@x,y", xác định thẻ
* Chuỗi ký tự cố định "current", xác định thẻ hiện được chọn
* Chuỗi ký tự cố định "end", trả về số lượng thẻ (chỉ hợp lệ cho
  :meth:`Notebook.index`)


Sự kiện ảo
^^^^^^^^^^

Widget này tạo một sự kiện ảo **<<NotebookTabChanged>>** sau khi một tab mới được chọn.


ttk.Notebook
^^^^^^^^^^^^

.. class:: Notebook

   .. method:: add(child, **kw)

      Thêm một tab mới vào notebook.

      Nếu cửa sổ hiện đang được notebook quản lý nhưng bị ẩn, cửa sổ sẽ được khôi phục về vị trí trước đó.

      Xem `Tab Options <Tab Options_>`_ để biết danh sách các tùy chọn có sẵn.


   .. method:: forget(tab_id)

      Xóa tab được chỉ định bởi *tab_id*, đồng thời bỏ ánh xạ và hủy quản lý cửa sổ liên kết.

      Điều này che khuất geometry-manager kế thừa :meth:`!forget`; hãy sử dụng :meth:`~tkinter.Pack.pack_forget`, :meth:`~tkinter.Grid.grid_forget` hoặc :meth:`~tkinter.Place.place_forget` để xóa chính widget đó khỏi manager của nó.


   .. method:: hide(tab_id)

      Ẩn tab được chỉ định bởi *tab_id*.

      Tab sẽ không được hiển thị, nhưng cửa sổ liên kết vẫn do notebook quản lý và cấu hình của nó vẫn được ghi nhớ. Có thể khôi phục các tab đã ẩn bằng lệnh :meth:`add`.


   .. method:: identify(x, y)

      Trả về tên của phần tử tab tại vị trí *x*, *y*, hoặc chuỗi rỗng nếu không có phần tử nào.


   .. method:: index(tab_id)

      Trả về chỉ mục số của tab được chỉ định bởi *tab_id*, hoặc tổng số tab nếu *tab_id* là chuỗi "end".


   .. method:: insert(pos, child, **kw)

      Chèn một ngăn tại vị trí được chỉ định.

      *pos* có thể là chuỗi "end", một chỉ mục số nguyên hoặc tên của một child đang được quản lý. Nếu *child* đã được notebook quản lý, di chuyển child đó đến vị trí được chỉ định.

      Xem `Tab Options <Tab Options_>`_ để biết danh sách các tùy chọn có sẵn.


   .. method:: select(tab_id=None)

      Chọn *tab_id* được chỉ định.

      Cửa sổ con tương ứng sẽ được hiển thị và cửa sổ đã chọn trước đó (nếu khác) sẽ được bỏ ánh xạ. Nếu bỏ qua *tab_id*, trả về tên widget của ngăn hiện đang được chọn.


   .. method:: tab(tab_id, option=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn của *tab_id* cụ thể.

      Nếu không cung cấp *kw*, trả về một từ điển chứa các giá trị tùy chọn của tab. Nếu chỉ định *option*, trả về giá trị của *option* đó. Nếu không, đặt các tùy chọn thành những giá trị tương ứng.


   .. method:: tabs()

      Trả về một tuple gồm các cửa sổ do notebook quản lý.


   .. method:: enable_traversal()

      Bật tính năng điều hướng bằng bàn phím cho cửa sổ cấp cao nhất chứa notebook này.

      Thao tác này sẽ mở rộng các binding cho cửa sổ cấp cao nhất chứa notebook như sau:

      * :kbd:`Control-Tab`: chọn tab ngay sau tab hiện được chọn.
      * :kbd:`Shift-Control-Tab`: chọn tab ngay trước tab hiện được chọn.
      * :kbd:`Alt-K`: khi *K* là ký tự mnemonic (được gạch chân) của bất kỳ tab nào, sẽ chọn tab đó.

      Có thể bật tính năng duyệt cho nhiều notebook trong cùng một toplevel, kể cả các notebook lồng nhau. Tuy nhiên, tính năng duyệt notebook chỉ hoạt động đúng nếu tất cả các pane là phần tử con trực tiếp của notebook.


Progressbar
-----------

Widget :class:`ttk.Progressbar <Progressbar>` hiển thị trạng thái của một thao tác chạy trong thời gian dài. Widget này có thể hoạt động ở hai chế độ: 1) chế độ determinate hiển thị phần công việc đã hoàn thành so với tổng khối lượng công việc cần thực hiện và 2) chế độ indeterminate hiển thị hoạt ảnh để cho người dùng biết rằng công việc đang tiến triển.


Options
^^^^^^^

Widget này chấp nhận các tùy chọn cụ thể sau:

.. tabularcolumns:: |l|L|

+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn | Mô tả                                                                                                                                                                                                                                                                   |
+==========+=========================================================================================================================================================================================================================================================================+
| orient   | Một trong hai giá trị "horizontal" hoặc "vertical". Chỉ định hướng của thanh tiến trình.                                                                                                                                                                                |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| length   | Chỉ định độ dài của trục dài của thanh tiến trình (chiều rộng nếu là horizontal, chiều cao nếu là vertical).                                                                                                                                                            |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mode     | Một trong hai giá trị "determinate" hoặc "indeterminate".                                                                                                                                                                                                               |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| maximum  | Một số chỉ định giá trị tối đa. Mặc định là 100.                                                                                                                                                                                                                        |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| value    | Giá trị hiện tại của thanh tiến trình. Ở chế độ "determinate", giá trị này biểu thị lượng công việc đã hoàn thành. Ở chế độ "indeterminate", giá trị này được hiểu theo modulo *maximum*; tức là thanh tiến trình hoàn tất một "cycle" khi giá trị tăng thêm *maximum*. |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| variable | Tên được liên kết với giá trị tùy chọn. Nếu được chỉ định, giá trị của thanh tiến trình sẽ tự động được đặt thành giá trị của tên này mỗi khi tên đó được sửa đổi.                                                                                                      |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| phase    | Tùy chọn chỉ đọc. Widget định kỳ tăng giá trị của tùy chọn này mỗi khi giá trị của nó lớn hơn 0 và, trong chế độ xác định, nhỏ hơn giá trị tối đa. Chủ đề hiện tại có thể sử dụng tùy chọn này để cung cấp thêm các hiệu ứng animation.                                 |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


ttk.Progressbar
^^^^^^^^^^^^^^^

.. class:: Progressbar

   .. method:: start(interval=None)

      Bắt đầu chế độ tự động tăng: lập lịch một sự kiện hẹn giờ lặp lại gọi
      :meth:`Progressbar.step` mỗi *interval* mili giây. Nếu bị bỏ qua, *interval* mặc định là 50 mili giây.


   .. method:: step(amount=None)

      Tăng giá trị của thanh tiến trình thêm *amount*.

      *amount* mặc định là 1.0 nếu bị bỏ qua.


   .. method:: stop()

      Dừng chế độ tự động tăng: hủy mọi sự kiện bộ hẹn giờ lặp lại do
      :meth:`Progressbar.start` khởi tạo cho thanh tiến trình này.


Separator
---------

Widget :class:`ttk.Separator <Separator>` hiển thị một thanh phân cách ngang hoặc dọc.

Widget này không có phương thức nào khác ngoài các phương thức được kế thừa từ
:class:`ttk.Widget <Widget>`.


Options
^^^^^^^

Widget này chấp nhận tùy chọn cụ thể sau:

.. tabularcolumns:: |l|L|

+----------+--------------------------------------------------------------------------+
| Tùy chọn | Mô tả                                                                    |
+==========+==========================================================================+
| orient   | Một trong "horizontal" hoặc "vertical". Chỉ định hướng của bộ phân cách. |
+----------+--------------------------------------------------------------------------+


Sizegrip
--------

Widget :class:`ttk.Sizegrip <Sizegrip>` (còn được gọi là hộp mở rộng) cho phép người dùng thay đổi kích thước cửa sổ cấp cao nhất chứa nó bằng cách nhấn và kéo tay nắm.

Widget này không có tùy chọn hay phương thức riêng nào, ngoài những tùy chọn và phương thức được kế thừa từ :class:`ttk.Widget <Widget>`.


Lưu ý dành riêng cho từng nền tảng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Trên macOS, theo mặc định, các cửa sổ toplevel tự động bao gồm một size grip tích hợp. Việc thêm một :class:`Sizegrip` không gây hại, vì size grip tích hợp sẽ chỉ che widget này.


Lỗi
^^^

* Nếu vị trí của toplevel chứa widget được chỉ định tương đối so với bên phải hoặc phía dưới màn hình (ví dụ, ....), widget :class:`Sizegrip` sẽ không thay đổi kích thước cửa sổ.
* Widget này chỉ hỗ trợ thay đổi kích thước theo hướng "southeast".


Treeview
--------

Widget :class:`ttk.Treeview <Treeview>` hiển thị một tập hợp các mục theo cấu trúc phân cấp. Mỗi mục có một nhãn dạng văn bản, một hình ảnh tùy chọn và một danh sách tùy chọn gồm các giá trị dữ liệu. Các giá trị dữ liệu được hiển thị trong những cột liên tiếp phía sau nhãn cây.

Có thể kiểm soát thứ tự hiển thị các giá trị dữ liệu bằng cách đặt tùy chọn widget ``displaycolumns``. Widget cây cũng có thể hiển thị tiêu đề cột. Có thể truy cập các cột theo số hoặc theo tên tượng trưng được liệt kê trong tùy chọn widget columns. Xem `Column Identifiers <Column Identifiers_>`_.

Mỗi mục được xác định bằng một tên duy nhất. Widget sẽ tạo ID mục nếu bên gọi không cung cấp. Có một mục gốc đặc biệt, có tên là ``{}``. Bản thân mục gốc không được hiển thị; các mục con của nó xuất hiện ở cấp cao nhất của cấu trúc phân cấp.

Mỗi mục cũng có một danh sách các thẻ, có thể dùng để liên kết các binding sự kiện với từng mục và kiểm soát giao diện của mục đó.

Widget Treeview hỗ trợ cuộn ngang và dọc theo các tùy chọn được mô tả trong `Scrollable Widget Options <Scrollable Widget Options_>`_ và các phương thức
:meth:`Treeview.xview` và :meth:`Treeview.yview`.


Options
^^^^^^^

Widget này chấp nhận các tùy chọn cụ thể sau:

.. tabularcolumns:: |l|p{0.7\linewidth}|

+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn       | Mô tả                                                                                                                                                                                                                                                                               |
+================+=====================================================================================================================================================================================================================================================================================+
| các cột        | Danh sách các mã định danh cột, chỉ định số lượng cột và tên của chúng.                                                                                                                                                                                                             |
+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| displaycolumns | Danh sách các mã định danh cột (là chỉ mục dạng ký hiệu hoặc số nguyên), chỉ định những cột dữ liệu được hiển thị và thứ tự xuất hiện của chúng, hoặc chuỗi "#all".                                                                                                                 |
+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| height         | Chỉ định số hàng sẽ hiển thị. Lưu ý: chiều rộng được yêu cầu được xác định từ tổng chiều rộng của các cột.                                                                                                                                                                          |
+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| padding        | Chỉ định phần đệm bên trong của widget. Phần đệm là một danh sách gồm tối đa bốn đặc tả độ dài.                                                                                                                                                                                     |
+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| selectmode     | Kiểm soát cách các class binding tích hợp sẵn quản lý việc chọn. Một trong các giá trị "extended", "browse" hoặc "none". Nếu được đặt thành "extended" (mặc định), có thể chọn nhiều mục. Nếu là "browse", mỗi lần chỉ chọn một mục. Nếu là "none", vùng chọn sẽ không bị thay đổi. |
|                |                                                                                                                                                                                                                                                                                     |
|                | Lưu ý rằng mã ứng dụng và các tag binding có thể thiết lập vùng chọn theo bất kỳ cách nào chúng muốn, bất kể giá trị của tùy chọn này.                                                                                                                                              |
+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| show           | Danh sách chứa không hoặc nhiều giá trị sau đây, xác định những phần tử nào của cây cần hiển thị.                                                                                                                                                                                   |
|                |                                                                                                                                                                                                                                                                                     |
|                | * tree: hiển thị nhãn cây trong cột #0.                                                                                                                                                                                                                                             |
|                | * headings: hiển thị hàng tiêu đề.                                                                                                                                                                                                                                                  |
|                |                                                                                                                                                                                                                                                                                     |
|                | Mặc định là "tree headings", tức là hiển thị tất cả các phần tử.                                                                                                                                                                                                                    |
|                |                                                                                                                                                                                                                                                                                     |
|                | **Note**: Cột #0 luôn tham chiếu đến cột cây, ngay cả khi không chỉ định show="tree".                                                                                                                                                                                               |
+----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. note::

   Tk 9.0 đã bổ sung một số :class:`Treeview` tính năng. Tùy chọn *selectmode* nhận thêm các giá trị ``"single"`` và ``"multiple"``; các tùy chọn widget mới *selecttype* (``"item"`` hoặc ``"cell"`` selection), *striped* (các hàng có sọc xen kẽ), và *titlecolumns* / *titleitems* (các cột hoặc hàng được cố định để không bị cuộn) đã được giới thiệu; tùy chọn cột *separator* được thêm vào; và các mục nhận thêm tùy chọn *hidden*. Tk 9.1 đã bổ sung các tùy chọn *rowheight* và *headingheight*.


.. _`Item options`:

Tùy chọn mục
^^^^^^^^^^^^

Có thể chỉ định các tùy chọn mục sau cho các mục trong các lệnh insert và item widget.

.. tabularcolumns:: |l|L|

+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn | Mô tả                                                                                                                                                                                                       |
+==========+=============================================================================================================================================================================================================+
| text     | Nhãn văn bản sẽ hiển thị cho mục.                                                                                                                                                                           |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| image    | Một Tk Image được hiển thị ở bên trái nhãn.                                                                                                                                                                 |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| values   | Danh sách các giá trị liên kết với item.                                                                                                                                                                    |
|          |                                                                                                                                                                                                             |
|          | Mỗi item phải có cùng số lượng giá trị với số cột tùy chọn của widget. Nếu có ít giá trị hơn số cột, các giá trị còn lại được xem là trống. Nếu có nhiều giá trị hơn số cột, các giá trị thừa sẽ bị bỏ qua. |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| open     | ``True``/``False`` giá trị cho biết các phần tử con của item có được hiển thị hay bị ẩn.                                                                                                                    |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tags     | Danh sách các thẻ được liên kết với mục này.                                                                                                                                                                |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Tùy chọn thẻ
^^^^^^^^^^^^

Có thể chỉ định các tùy chọn sau cho thẻ:

.. tabularcolumns:: |l|L|

+------------+--------------------------------------------------------------------------+
| Tùy chọn   | Mô tả                                                                    |
+============+==========================================================================+
| foreground | Chỉ định màu nền trước của văn bản.                                      |
+------------+--------------------------------------------------------------------------+
| background | Chỉ định màu nền của ô hoặc mục.                                         |
+------------+--------------------------------------------------------------------------+
| font       | Chỉ định font dùng khi vẽ văn bản.                                       |
+------------+--------------------------------------------------------------------------+
| image      | Chỉ định hình ảnh của mục trong trường hợp tùy chọn image của mục trống. |
+------------+--------------------------------------------------------------------------+


.. _`Column identifiers`:

Mã định danh cột
^^^^^^^^^^^^^^^^

Mã định danh cột có thể có một trong các dạng sau:

* Tên ký hiệu trong tùy chọn columns.
* Một số nguyên n, chỉ định cột dữ liệu thứ n.
* Một chuỗi có dạng #n, trong đó n là một số nguyên, chỉ định cột hiển thị thứ n.

Lưu ý:

* Các giá trị tùy chọn của Item có thể được hiển thị theo thứ tự khác với thứ tự chúng được lưu trữ.
* Cột #0 luôn tham chiếu đến cột cây, ngay cả khi không chỉ định show="tree".

Số cột dữ liệu là chỉ mục trong danh sách giá trị tùy chọn của một mục; số cột hiển thị là số cột trong cây nơi các giá trị được hiển thị. Nhãn cây được hiển thị ở cột #0. Nếu displaycolumns không được thiết lập, thì cột dữ liệu n được hiển thị ở cột #n+1. Một lần nữa, **cột #0 luôn đề cập đến cột cây**.


Sự kiện ảo
^^^^^^^^^^

Tiện ích Treeview tạo ra các sự kiện ảo sau đây.

.. tabularcolumns:: |l|L|

+--------------------+--------------------------------------------------------+
| Sự kiện            | Mô tả                                                  |
+====================+========================================================+
| <<TreeviewSelect>> | Được tạo mỗi khi vùng lựa chọn thay đổi.               |
+--------------------+--------------------------------------------------------+
| <<TreeviewOpen>>   | Được tạo ngay trước khi đặt mục focus thành open=True. |
+--------------------+--------------------------------------------------------+
| <<TreeviewClose>>  | Được tạo ngay sau khi đặt mục focus thành open=False.  |
+--------------------+--------------------------------------------------------+

Có thể sử dụng các phương thức :meth:`Treeview.focus` và :meth:`Treeview.selection` để xác định mục hoặc các mục bị ảnh hưởng.


ttk.Treeview
^^^^^^^^^^^^

.. class:: Treeview

   .. method:: bbox(item, column=None)

      Trả về bounding box (tương đối với cửa sổ của widget treeview) của *item* được chỉ định dưới dạng (x, y, width, height).

      Nếu *column* được chỉ định, trả về hộp giới hạn của ô đó. Nếu *item* không hiển thị (nghĩa là, nếu nó là hậu duệ của một item đã đóng hoặc đã cuộn ra ngoài màn hình), trả về một chuỗi rỗng.

      Điều này che khuất :meth:`!Misc.bbox` được kế thừa; hãy sử dụng :meth:`~tkinter.Misc.grid_bbox` cho hộp giới hạn của lưới.


   .. method:: get_children(item=None)

      Trả về một tuple gồm các phần tử con thuộc về *item*.

      Nếu *item* không được chỉ định, trả về các phần tử con của nút gốc.


   .. method:: set_children(item, *newchildren)

      Thay thế các phần tử con của *item* bằng *newchildren*.

      Các phần tử con có trong *item* nhưng không có trong *newchildren* sẽ được tách khỏi cây. Không item nào trong *newchildren* được là tổ tiên của *item*. Lưu ý rằng nếu không chỉ định *newchildren*, các phần tử con của *item* sẽ bị tách khỏi cây.


   .. method:: column(column, option=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cho *column* được chỉ định.

      Nếu không cung cấp *kw*, trả về một dict chứa các giá trị tùy chọn của cột. Nếu chỉ định *option* thì trả về giá trị của *option* đó. Nếu không, thiết lập các tùy chọn thành các giá trị tương ứng.

      Các tùy chọn/giá trị hợp lệ là:

      *id*
         Trả về tên cột. Đây là một tùy chọn chỉ đọc.
      *anchor*: Một trong các giá trị anchor tiêu chuẩn của Tk.
         Chỉ định cách căn chỉnh văn bản trong cột này so với ô.
      *minwidth*: width
         Chiều rộng tối thiểu của cột tính bằng pixel. Widget treeview sẽ không làm cho cột nhỏ hơn giá trị được chỉ định bởi tùy chọn này khi widget được thay đổi kích thước hoặc khi người dùng kéo cột.
      *separator*: ``True``/``False``
         Chỉ định liệu có vẽ dấu phân cách cột ở bên phải cột hay không.
      *stretch*: ``True``/``False``
         Chỉ định liệu chiều rộng của cột có được điều chỉnh khi widget được thay đổi kích thước hay không.
      *width*: width
         Chiều rộng của cột tính bằng pixel.

      Để cấu hình cột cây, hãy gọi hàm này với column = "#0"

   .. method:: delete(*items)

      Xóa tất cả *mục* được chỉ định cùng tất cả các mục con của chúng.

      Không thể xóa mục gốc.


   .. method:: detach(*items)

      Hủy liên kết tất cả *mục* được chỉ định khỏi cây.

      Các mục và tất cả các mục con của chúng vẫn tồn tại, đồng thời có thể được chèn lại vào một vị trí khác trong cây, nhưng sẽ không được hiển thị.

      Không thể tách mục gốc.


   .. method:: exists(item)

      Trả về ``True`` nếu *mục* được chỉ định hiện diện trong cây, nếu không thì trả về ``False``.


   .. method:: focus(item=None)

      Nếu chỉ định *item*, đặt mục được focus thành *item*. Nếu không, trả về mục đang được focus hiện tại hoặc '' nếu không có.

      Thuộc tính này che khuất :meth:`!Misc.focus` được kế thừa; sử dụng :meth:`~tkinter.Misc.focus_set` để focus chính widget.


   .. method:: heading(column, option=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn heading cho *column* được chỉ định.

      Nếu không cung cấp *kw*, trả về một dict chứa các giá trị tùy chọn của heading. Nếu chỉ định *option*, thì trả về giá trị của *option* đó. Nếu không, đặt các tùy chọn thành những giá trị tương ứng.

      Các tùy chọn/giá trị hợp lệ là:

      *text*: văn bản
         Văn bản hiển thị trong heading của cột.
      *image*: imageName
         Chỉ định một image sẽ được hiển thị ở bên phải tiêu đề cột.
      *anchor*: anchor
         Chỉ định cách căn chỉnh văn bản tiêu đề. Đây là một trong các giá trị anchor tiêu chuẩn của Tk.
      *command*: callback
         Một callback sẽ được gọi khi nhấn vào nhãn tiêu đề.

      Để cấu hình tiêu đề cột cây, hãy gọi hàm này với column = "#0".


   .. method:: identify(component, x, y)

      Trả về mô tả của *component* được chỉ định bên dưới điểm được xác định bởi *x* và *y*, hoặc chuỗi rỗng nếu không có *component* nào tại vị trí đó.


   .. method:: identify_row(y)

      Trả về ID của item tại vị trí *y*.


   .. method:: identify_column(x)

      Trả về mã định danh của cột hiển thị của ô tại vị trí *x*.

      Cột cây có ID #0.


   .. method:: identify_region(x, y)

      Trả về một trong các giá trị sau:

      +---------------+----------------------------------------+
      | vùng          | ý nghĩa                                |
      +===============+========================================+
      | tiêu đề       | Khu vực tiêu đề của cây.               |
      +---------------+----------------------------------------+
      | dấu phân cách | Khoảng trống giữa tiêu đề của hai cột. |
      +---------------+----------------------------------------+
      | cây           | Khu vực cây.                           |
      +---------------+----------------------------------------+
      | ô             | Một ô dữ liệu.                         |
      +---------------+----------------------------------------+

      Khả dụng: Tk 8.6.


   .. method:: identify_element(x, y)

      Trả về phần tử tại vị trí *x*, *y*.

      Khả dụng: Tk 8.6.


   .. method:: index(item)

      Trả về chỉ mục số nguyên của *item* trong danh sách các phần tử con của phần tử cha.


   .. method:: insert(parent, index, iid=None, **kw)

      Tạo một item mới và trả về mã định danh của item vừa tạo.

      *parent* là ID của item cha, hoặc chuỗi rỗng để tạo một item cấp cao nhất mới. *index* là một số nguyên hoặc giá trị "end", chỉ định vị trí chèn item mới trong danh sách các item con của item cha. Nếu *index* nhỏ hơn hoặc bằng không, node mới được chèn vào đầu; nếu *index* lớn hơn hoặc bằng số lượng item con hiện tại, node được chèn vào cuối. Nếu chỉ định *iid*, giá trị này được dùng làm mã định danh của item; *iid* không được tồn tại trong tree. Nếu không, một mã định danh duy nhất mới sẽ được tạo.

      Xem `Item Options <Item Options_>`_ để biết danh sách các tùy chọn hiện có.


   .. method:: item(item, option=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cho *item* được chỉ định.

      Nếu không cung cấp tùy chọn nào, một dict chứa các tùy chọn/giá trị cho item sẽ được trả về. Nếu chỉ định *option*, giá trị của tùy chọn đó sẽ được trả về. Nếu không, các tùy chọn sẽ được đặt thành những giá trị tương ứng được cung cấp bởi *kw*.


   .. method:: reattach(item, parent, index)
      :no-typesetting:

   .. method:: move(item, parent, index)

      Di chuyển *item* đến vị trí *index* trong danh sách các phần tử con của *parent*.

      Không được phép di chuyển một item vào bên dưới một trong các phần tử con của chính nó. Nếu *index* nhỏ hơn hoặc bằng không, *item* sẽ được di chuyển đến đầu danh sách; nếu lớn hơn hoặc bằng số lượng phần tử con, nó sẽ được di chuyển đến cuối danh sách. Nếu *item* đã được tách khỏi cây, nó sẽ được gắn lại.

      :meth:`reattach` là bí danh của :meth:`!move`.


   .. method:: next(item)

      Trả về mã định danh của phần tử cùng cấp tiếp theo của *item*, hoặc '' nếu *item* là phần tử con cuối cùng của parent.


   .. method:: parent(item)

      Trả về ID của mục cha của *item*, hoặc '' nếu *item* nằm ở cấp cao nhất trong hệ phân cấp.


   .. method:: prev(item)

      Trả về mã định danh của mục anh em liền trước *item*, hoặc '' nếu *item* là mục con đầu tiên của mục cha.


   .. method:: see(item)

      Đảm bảo rằng *item* hiển thị.

      Đặt tùy chọn open của tất cả các mục tổ tiên của *item* thành ``True``, đồng thời cuộn widget nếu cần để *item* nằm trong phần cây đang hiển thị.


   .. method:: selection()

      Trả về một tuple gồm các mục được chọn.

      .. versionchanged:: 3.8
         ``selection()`` không còn nhận đối số. Để thay đổi trạng thái lựa chọn, hãy sử dụng các phương thức selection sau đây.


   .. method:: selection_set(*items)

      *items* trở thành lựa chọn mới.

      .. versionchanged:: 3.6
         *items* có thể được truyền dưới dạng các đối số riêng biệt, không chỉ dưới dạng một tuple duy nhất.


   .. method:: selection_add(*items)

      Thêm *items* vào vùng lựa chọn.

      .. versionchanged:: 3.6
         *items* có thể được truyền dưới dạng các đối số riêng biệt, không chỉ dưới dạng một tuple duy nhất.


   .. method:: selection_remove(*items)

      Xóa *items* khỏi vùng lựa chọn.

      .. versionchanged:: 3.6
         *items* có thể được truyền dưới dạng các đối số riêng biệt, không chỉ dưới dạng một tuple duy nhất.


   .. method:: selection_toggle(*items)

      Chuyển đổi trạng thái lựa chọn của từng mục trong *items*.

      .. versionchanged:: 3.6
         *items* có thể được truyền dưới dạng các đối số riêng biệt, không chỉ dưới dạng một tuple duy nhất.


   .. method:: set(item, column=None, value=None)

      Với một đối số, trả về một từ điển gồm các cặp column/value cho *item* được chỉ định. Với hai đối số, trả về giá trị hiện tại của *column* được chỉ định. Với ba đối số, đặt giá trị của *column* đã cho trong *item* đã cho thành *value* được chỉ định.


   .. method:: tag_bind(tagname, sequence=None, callback=None)

      Liên kết một callback cho event *sequence* đã cho với tag *tagname*. Khi một event được chuyển đến một item, các callback cho tùy chọn tags của từng item sẽ được gọi.


   .. method:: tag_configure(tagname, option=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn cho *tagname* được chỉ định.

      Nếu *kw* không được cung cấp, trả về một dict gồm các thiết lập tùy chọn cho *tagname*. Nếu *option* được chỉ định, trả về giá trị của *option* đó cho *tagname* được chỉ định. Nếu không, đặt các tùy chọn thành các giá trị tương ứng cho *tagname* đã cho.


   .. method:: tag_has(tagname, item=None)

      Nếu *item* được chỉ định, trả về ``True`` nếu *item* được chỉ định có *tagname* đã cho và ``False`` nếu không. Nếu không, trả về một tuple gồm tất cả các item có tag được chỉ định.

      Tính khả dụng: Tk 8.6


   .. method:: xview(*args)

      Truy vấn hoặc sửa đổi vị trí theo chiều ngang của treeview.


   .. method:: yview(*args)

      Truy vấn hoặc sửa đổi vị trí theo chiều dọc của treeview.


.. _TtkStyling:

Tạo kiểu Ttk
------------

Mỗi widget trong :mod:`!ttk` được gán một style, trong đó chỉ định tập hợp các element cấu thành widget và cách chúng được sắp xếp, cùng với các cài đặt động và mặc định cho các tùy chọn của element. Theo mặc định, tên style giống với tên class của widget, nhưng có thể được ghi đè bằng tùy chọn style của widget. Nếu bạn không biết tên class của một widget, hãy sử dụng method
:meth:`Misc.winfo_class <tkinter.Misc.winfo_class>` (somewidget.winfo_class()).

.. seealso::

   `Giới thiệu về công cụ theme của Tk <https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_intro.html>`_
      Trang hướng dẫn ``ttk::intro`` giải thích cách công cụ theme hoạt động.

   `Bộ widget Tile <https://tktable.sourceforge.net/tile/tile-tcl2004.pdf>`_
      Bài viết năm 2004 của Joe English giới thiệu theme engine (khi đó là phần mở rộng *Tile* riêng biệt), kèm các sơ đồ minh họa cách các phần tử và layout kết hợp để tạo nên giao diện của một widget.


.. class:: Style

   Lớp này được dùng để thao tác với cơ sở dữ liệu style.


   .. method:: configure(style, query_opt=None, **kw)

      Truy vấn hoặc đặt giá trị mặc định của (các) tùy chọn được chỉ định trong *style*.

      Mỗi khóa trong *kw* là một tùy chọn và mỗi giá trị là một chuỗi xác định giá trị cho tùy chọn đó.

      Ví dụ, để thay đổi mọi button mặc định thành button phẳng với một chút khoảng đệm và màu nền khác::

         from tkinter import ttk
         import tkinter

         root = tkinter.Tk()

         ttk.Style().configure("TButton", padding=6, relief="flat",
            background="#ccc")

         btn = ttk.Button(text="Sample")
         btn.pack()

         root.mainloop()


   .. method:: map(style, query_opt=None, **kw)

      Truy vấn hoặc đặt các giá trị động của (các) tùy chọn được chỉ định trong *style*.

      Mỗi khóa trong *kw* là một tùy chọn và mỗi giá trị thường phải là một list hoặc tuple chứa các statespec được nhóm trong tuple, list hoặc một cấu trúc tùy thích khác. Một statespec là sự kết hợp của một hoặc nhiều state, theo sau là một giá trị.

      Một ví dụ có thể giúp dễ hiểu hơn::

         import tkinter
         from tkinter import ttk

         root = tkinter.Tk()

         style = ttk.Style()
         style.map("C.TButton",
             foreground=[('pressed', 'red'), ('active', 'blue')],
             background=[('pressed', '!disabled', 'black'), ('active', 'white')]
             )

         colored_btn = ttk.Button(text="Test", style="C.TButton").pack()

         root.mainloop()


      Lưu ý rằng thứ tự của các chuỗi (states, value) cho một tùy chọn rất quan trọng; chẳng hạn, nếu thứ tự được thay đổi thành ``[('active', 'blue'), ('pressed', 'red')]`` trong tùy chọn foreground, kết quả sẽ là foreground màu xanh lam khi widget ở trạng thái active hoặc pressed.

      Khi được gọi để truy vấn map (không chỉ định các giá trị cần đặt), hàm này trả về một dictionary ánh xạ mỗi tùy chọn tới danh sách statespec tương ứng.

      .. versionchanged:: 3.10
         Giá trị được trả về khi truy vấn map đã được sửa lại.


   .. method:: lookup(style, option, state=None, default=None)

      Trả về giá trị được chỉ định cho *tùy chọn* trong *style*.

      Nếu *state* được chỉ định, giá trị này phải là một chuỗi gồm một hoặc nhiều state. Nếu đối số *default* được đặt, đối số này sẽ được dùng làm giá trị dự phòng trong trường hợp không tìm thấy đặc tả nào cho tùy chọn.

      Để kiểm tra Button sử dụng font nào theo mặc định::

         from tkinter import ttk

         print(ttk.Style().lookup("TButton", "font"))


   .. method:: layout(style, layoutspec=None)

      Xác định bố cục widget cho *style* đã cho. Nếu *layoutspec* bị bỏ qua, trả về đặc tả bố cục cho style đã cho.

      *layoutspec*, nếu được chỉ định, phải là một danh sách hoặc một kiểu sequence khác (không bao gồm chuỗi), trong đó mỗi mục phải là một tuple, mục đầu tiên là tên bố cục và mục thứ hai phải có định dạng được mô tả trong `Layouts`_.

      Để hiểu định dạng này, hãy xem ví dụ sau (ví dụ này không nhằm thực hiện điều gì hữu ích)::

         from tkinter import ttk
         import tkinter

         root = tkinter.Tk()

         style = ttk.Style()
         style.layout("TMenubutton", [
            ("Menubutton.background", None),
            ("Menubutton.button", {"children":
                [("Menubutton.focus", {"children":
                    [("Menubutton.padding", {"children":
                        [("Menubutton.label", {"side": "left", "expand": 1})]
                    })]
                })]
            }),
         ])

         mbtn = ttk.Menubutton(text='Text')
         mbtn.pack()
         root.mainloop()


   .. method:: element_create(elementname, etype, *args, **kw)

      Tạo một element mới trong theme hiện tại, có *etype* đã cho; giá trị này phải là một trong các giá trị "image", "from" hoặc "vsapi". Giá trị sau cùng chỉ có trong Tk 8.6 trên Windows.

      Nếu sử dụng "image", *args* phải chứa tên image mặc định, theo sau là các cặp statespec/value (đây là imagespec), và *kw* có thể có các tùy chọn sau:

      border=padding
         padding là một danh sách gồm tối đa bốn số nguyên, lần lượt chỉ định các border bên trái, bên trên, bên phải và bên dưới.

      height=height
         Chỉ định chiều cao tối thiểu cho phần tử. Nếu nhỏ hơn 0, chiều cao của ảnh cơ sở được sử dụng làm mặc định.

      padding=padding
         Chỉ định phần đệm bên trong của phần tử. Nếu không được chỉ định, mặc định là giá trị của border.

      sticky=spec
         Chỉ định cách đặt ảnh trong vùng cuối cùng. spec chứa không hoặc nhiều ký tự "n", "s", "w" hoặc "e".

      width=width
         Chỉ định độ rộng tối thiểu cho phần tử. Nếu nhỏ hơn 0, độ rộng của ảnh cơ sở sẽ được dùng làm mặc định.

      Ví dụ::

         img1 = tkinter.PhotoImage(master=root, file='button.png')
         img1 = tkinter.PhotoImage(master=root, file='button-pressed.png')
         img1 = tkinter.PhotoImage(master=root, file='button-active.png')
         style = ttk.Style(root)
         style.element_create('Button.button', 'image',
                              img1, ('pressed', img2), ('active', img3),
                              border=(2, 4), sticky='we')

      Nếu "from" được dùng làm giá trị của *etype*,
      :meth:`element_create` sẽ sao chép một phần tử hiện có. *args* được kỳ vọng chứa một themename, từ đó phần tử sẽ được sao chép, và tùy chọn một phần tử để sao chép. Nếu không chỉ định phần tử để sao chép, một phần tử rỗng sẽ được dùng. *kw* sẽ bị loại bỏ.

      Ví dụ::

         style = ttk.Style(root)
         style.element_create('plain.background', 'from', 'default')

      Nếu "vsapi" được dùng làm giá trị của *etype*, :meth:`element_create` sẽ tạo một phần tử mới trong theme hiện tại, với giao diện trực quan được vẽ bằng Microsoft Visual Styles API, API chịu trách nhiệm cung cấp các kiểu theo theme trên Windows XP và Vista. *args* được kỳ vọng chứa lớp và phần Visual Styles như được nêu trong tài liệu Microsoft, theo sau là một chuỗi tùy chọn gồm các tuple của trạng thái ttk và giá trị trạng thái Visual Styles API tương ứng. *kw* có thể có các tùy chọn sau:

      padding=padding
         Chỉ định phần đệm bên trong của phần tử. *padding* là một danh sách gồm tối đa bốn số nguyên, lần lượt chỉ định lượng đệm bên trái, bên trên, bên phải và bên dưới. Nếu chỉ định ít hơn bốn phần tử, giá trị bottom mặc định là top, right mặc định là left và top mặc định là left. Nói cách khác, danh sách gồm ba số chỉ định phần đệm bên trái, theo chiều dọc và bên phải; danh sách gồm hai số chỉ định phần đệm theo chiều ngang và theo chiều dọc; một số duy nhất chỉ định cùng một phần đệm cho mọi phía xung quanh widget. Tùy chọn này không thể kết hợp với bất kỳ tùy chọn nào khác.

      margins=padding
         Chỉ định phần đệm bên ngoài của phần tử. *padding* là một danh sách gồm tối đa bốn số nguyên, lần lượt chỉ định lượng đệm bên trái, bên trên, bên phải và bên dưới. Tùy chọn này không thể kết hợp với bất kỳ tùy chọn nào khác.

      width=width
         Chỉ định chiều rộng của phần tử. Nếu đặt tùy chọn này, Visual Styles API sẽ không được truy vấn để lấy kích thước hoặc phần được khuyến nghị. Nếu đặt tùy chọn này, cũng nên đặt *height*. Không thể kết hợp các tùy chọn *width* và *height* với các tùy chọn *padding* hoặc *margins*.

      height=height
         Chỉ định chiều cao của phần tử. Xem các chú thích cho *width*.

      Ví dụ::

         style = ttk.Style(root)
         style.element_create('pin', 'vsapi', 'EXPLORERBAR', 3, [
                              ('pressed', '!selected', 3),
                              ('active', '!selected', 2),
                              ('pressed', 'selected', 6),
                              ('active', 'selected', 5),
                              ('selected', 4),
                              ('', 1)])
         style.layout('Explorer.Pin',
                      [('Explorer.Pin.pin', {'sticky': 'news'})])
         pin = ttk.Checkbutton(style='Explorer.Pin')
         pin.pack(expand=True, fill='both')

      .. versionchanged:: 3.13
         Đã bổ sung hỗ trợ cho bộ tạo phần tử "vsapi".

   .. method:: element_names()

      Trả về một tuple gồm các phần tử được định nghĩa trong theme hiện tại.


   .. method:: element_options(elementname)

      Trả về một tuple gồm các tùy chọn của *elementname*.


   .. method:: theme_create(themename, parent=None, settings=None)

      Tạo một theme mới.

      Sẽ xảy ra lỗi nếu *themename* đã tồn tại. Nếu chỉ định *parent*, theme mới sẽ kế thừa các style, phần tử và bố cục từ theme cha. Nếu có *settings*, chúng được yêu cầu phải có cùng cú pháp được sử dụng cho :meth:`theme_settings`.


   .. method:: theme_settings(themename, settings)

      Tạm thời đặt theme hiện tại thành *themename*, áp dụng *settings* được chỉ định, rồi khôi phục theme trước đó.

      Mỗi khóa trong *settings* là một style, và mỗi giá trị có thể chứa các khóa 'configure', 'map', 'layout' và 'element create'; các khóa này được mong đợi có cùng định dạng như định dạng được chỉ định bởi các phương thức
      :meth:`Style.configure`, :meth:`Style.map`, :meth:`Style.layout` và
      :meth:`Style.element_create` tương ứng.

      Ví dụ, hãy thay đổi Combobox của theme mặc định một chút::

         from tkinter import ttk
         import tkinter

         root = tkinter.Tk()

         style = ttk.Style()
         style.theme_settings("default", {
            "TCombobox": {
                "configure": {"padding": 5},
                "map": {
                    "background": [("active", "green2"),
                                   ("!disabled", "green4")],
                    "fieldbackground": [("!disabled", "green3")],
                    "foreground": [("focus", "OliveDrab1"),
                                   ("!disabled", "OliveDrab2")]
                }
            }
         })

         combo = ttk.Combobox().pack()

         root.mainloop()


   .. method:: theme_names()

      Trả về một tuple chứa tất cả các theme đã biết.


   .. method:: theme_use(themename=None)

      Nếu không cung cấp *themename*, trả về theme đang được sử dụng. Nếu không, đặt theme hiện tại thành *themename*, làm mới tất cả widget và phát ra sự kiện <<ThemeChanged>>.


.. _`Layouts`:

Bố cục
^^^^^^

Một bố cục có thể chỉ là ``None`` nếu không nhận tùy chọn nào, hoặc là một dict các tùy chọn chỉ định cách sắp xếp phần tử. Cơ chế bố cục sử dụng một phiên bản đơn giản hóa của pack geometry manager: với một vùng chứa ban đầu, mỗi phần tử được cấp phát một phần.

Các tùy chọn/giá trị hợp lệ là:

*side*: whichside
   Chỉ định cạnh của vùng chứa nơi đặt phần tử; một trong top, right, bottom hoặc left. Nếu bỏ qua, phần tử sẽ chiếm toàn bộ vùng chứa.

*sticky*: nswe
   Chỉ định vị trí đặt phần tử bên trong phần được cấp phát cho nó.

*unit*: 0 hoặc 1
   Nếu được đặt thành 1, khiến phần tử và tất cả phần tử con của nó được xem là một phần tử duy nhất cho mục đích của :meth:`Widget.identify` và các thao tác tương tự. Tùy chọn này được dùng cho những thành phần như nút kéo thanh cuộn có tay nắm.

*children*: [sublayout... ]
   Chỉ định danh sách các phần tử cần đặt bên trong phần tử này. Mỗi phần tử là một tuple (hoặc kiểu sequence khác), trong đó mục đầu tiên là tên bố cục, còn mục kia là một `Layout`_.

.. _Layout: `Layouts`_


Các widget bổ sung
------------------

Các widget theo theme sau đây hoàn thiện bộ widget :mod:`tkinter.ttk`. Mỗi widget là phiên bản theo theme của widget classic :mod:`tkinter` cùng tên và kế thừa các phương thức dùng chung của :class:`Widget`.

.. class:: Button(master=None, **kw)

   Widget Ttk :class:`Button`, hiển thị nhãn văn bản và/hoặc hình ảnh, đồng thời thực thi một command khi được nhấn. Đây là phiên bản theo theme của :class:`tkinter.Button` và kế thừa các phương thức widget dùng chung từ :class:`Widget`.

   .. method:: invoke()

      Gọi command liên kết với button và trả về kết quả của command đó.


.. class:: Checkbutton(master=None, **kw)

   Tiện ích Ttk :class:`Checkbutton`, được dùng để điều khiển một biến boolean có thể bật và tắt. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Checkbutton` và kế thừa các phương thức tiện ích chung từ :class:`Widget`.

   .. method:: invoke()

      Chuyển nút giữa trạng thái được chọn và không được chọn, gọi command liên kết với nút và trả về kết quả của command đó.


.. class:: Entry(master=None, widget=None, **kw)

   Tiện ích Ttk :class:`Entry`, hiển thị một chuỗi văn bản một dòng và cho phép người dùng chỉnh sửa chuỗi đó. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Entry` và kế thừa các phương thức tiện ích chung từ :class:`Widget`, cũng như các phương thức chỉnh sửa từ :class:`tkinter.Entry`.

   .. method:: bbox(index)

      Trả về một tuple ``(x, y, width, height)`` cho biết bounding box của ký tự tại *index* đã cho.

      Điều này che khuất :meth:`!Misc.bbox` được kế thừa; hãy dùng :meth:`~tkinter.Misc.grid_bbox` cho bounding box dạng lưới.

   .. method:: identify(x, y)

      Trả về tên của phần tử nằm dưới điểm được xác định bởi *x* và *y*, hoặc chuỗi rỗng nếu không có phần tử nào tại vị trí đó.

   .. method:: validate()

      Buộc kiểm tra validation của entry và trả về ``True`` nếu validation thành công, còn nếu không thì trả về ``False``.


.. class:: Frame(master=None, **kw)

   Widget Ttk :class:`Frame`, một container dùng để nhóm và sắp xếp các widget khác. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Frame` và kế thừa các phương thức widget chung từ :class:`Widget`.


.. class:: Label(master=None, **kw)

   Widget Ttk :class:`Label`, hiển thị nhãn văn bản và/hoặc hình ảnh. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Label` và kế thừa các phương thức widget chung từ :class:`Widget`.


.. class:: Labelframe(master=None, **kw)

   Widget Ttk :class:`Labelframe`, một container vẽ đường viền và nhãn tiêu đề xung quanh nội dung. Đây là phiên bản tương ứng theo theme của :class:`tkinter.LabelFrame` và kế thừa các phương thức widget chung từ :class:`Widget`.


.. class:: Menubutton(master=None, **kw)

   Widget Ttk :class:`Menubutton`, hiển thị nhãn văn bản và/hoặc hình ảnh, đồng thời bật lên một menu khi được nhấn. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Menubutton` và kế thừa các phương thức widget chung từ :class:`Widget`.


.. class:: OptionMenu(master, variable, default=None, *values, **kwargs)

   Widget Ttk :class:`OptionMenu`, một :class:`Menubutton` bật lên một menu gồm các lựa chọn loại trừ lẫn nhau. *variable* là biến theo dõi giá trị hiện được chọn, *default* là giá trị được đặt ban đầu, còn *values* là các mục hiển thị trong menu. Có thể cung cấp đối số từ khóa *command* để chỉ định một callable được gọi với giá trị đã chọn mỗi khi lựa chọn thay đổi; đối số từ khóa *style* đặt style được sử dụng bởi menubutton bên dưới; đối số từ khóa *direction* đặt vị trí đăng menu tương đối với menubutton (một trong ``'above'``, ``'below'`` (mặc định), ``'left'``, ``'right'`` hoặc ``'flush'``); và đối số từ khóa *name* đặt tên widget Tk.

   .. method:: set_menu(default=None, *values)

      Thay thế các mục của menu bằng *values*. Nếu có *default*, đồng thời đặt nó làm giá trị hiện tại của biến *variable*.

   .. method:: destroy()

      Hủy widget này và menu liên kết với nó.

   .. versionchanged:: 3.14
      Đã bổ sung hỗ trợ cho đối số từ khóa *name*.



.. class:: Panedwindow(master=None, **kw)

   Widget Ttk :class:`Panedwindow`, hiển thị một số cửa sổ con được xếp chồng theo chiều dọc hoặc chiều ngang. Người dùng có thể điều chỉnh kích thước tương đối của các cửa sổ con bằng cách kéo sash giữa các ngăn. Đây là phiên bản theo theme của :class:`tkinter.PanedWindow` và kế thừa các phương thức widget chung từ :class:`Widget`, cũng như các phương thức :meth:`!add` và :meth:`!panes` từ :class:`tkinter.PanedWindow`.

   .. method:: insert(pos, child, **kw)

      Chèn một ngăn chứa *child* tại vị trí *pos*. *pos* có thể là chuỗi ``'end'``, một chỉ mục số nguyên hoặc tên của cửa sổ con được quản lý. Nếu *child* đã được paned window quản lý, di chuyển nó đến vị trí được chỉ định. Mọi đối số từ khóa đều thiết lập các tùy chọn của ngăn.

   .. method:: forget(child)

      Xóa *child*, có thể là một chỉ mục số nguyên hoặc tên của cửa sổ con được quản lý, khỏi các ngăn.

      Điều này che khuất geometry manager được kế thừa :meth:`!forget`; sử dụng :meth:`~tkinter.Pack.pack_forget`, :meth:`~tkinter.Grid.grid_forget` hoặc :meth:`~tkinter.Place.place_forget` để xóa chính widget đó khỏi manager của nó.

   .. method:: pane(pane, option=None, **kw)

      Truy vấn hoặc sửa đổi các tùy chọn của *pane* được chỉ định, trong đó *pane* có thể là một chỉ mục số nguyên hoặc tên của cửa sổ con được quản lý. Nếu không cung cấp đối số nào, trả về một dictionary chứa các giá trị tùy chọn của ngăn. Nếu chỉ định *option*, trả về giá trị của tùy chọn đó. Nếu không, đặt các tùy chọn được cung cấp dưới dạng đối số từ khóa thành các giá trị tương ứng.

   .. method:: sashpos(index, newpos=None)

      Nếu chỉ định *newpos*, đặt vị trí của sash số *index* rồi trả về vị trí mới của nó. Thao tác này có thể điều chỉnh vị trí của các sash liền kề để đảm bảo các vị trí tăng dần đơn điệu; các vị trí cũng bị giới hạn trong khoảng từ 0 đến tổng kích thước của widget. Nếu bỏ qua *newpos*, trả về vị trí hiện tại của sash.


.. class:: Radiobutton(master=None, **kw)

   Widget Ttk :class:`Radiobutton`, được sử dụng như một phần của một nhóm để điều khiển một biến dùng chung duy nhất bằng cách chọn một trong số các giá trị loại trừ lẫn nhau. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Radiobutton` và kế thừa các phương thức widget chung từ :class:`Widget`.

   .. method:: invoke()

      Đặt biến tùy chọn thành giá trị của nút, chọn nút, gọi command được liên kết với nút và trả về kết quả của command đó.


.. class:: Scale(master=None, **kw)

   Widget Ttk :class:`Scale`, hiển thị một thanh trượt cho phép người dùng chọn một giá trị số trong một khoảng bằng cách di chuyển thanh trượt dọc theo rãnh. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Scale` và kế thừa các phương thức widget chung từ :class:`Widget`.

   .. method:: configure(cnf=None, **kw)

      Sửa đổi hoặc truy vấn các tùy chọn của widget, như
      :meth:`Widget.configure <tkinter.Misc.configure>`. Ngoài ra, phương thức này giới hạn các giá trị ``from`` và ``to`` để giá trị hiện tại luôn nằm trong khoảng do chúng xác định.

      .. versionchanged:: 3.9
         Giờ đây trả về giá trị cấu hình, như
         :meth:`Widget.configure <tkinter.Misc.configure>`.


   .. method:: get(x=None, y=None)

      Trả về giá trị hiện tại của scale. Nếu *x* và *y* được cung cấp, thay vào đó trả về giá trị tương ứng với tọa độ pixel *x*, *y*.


.. class:: Scrollbar(master=None, **kw)

   widget Ttk :class:`Scrollbar`, điều khiển khung nhìn của một widget có thể cuộn liên kết, chẳng hạn như :class:`Treeview`, :class:`Entry` hoặc
   :class:`tkinter.Text`. Đây là phiên bản tương ứng theo theme của :class:`tkinter.Scrollbar` và kế thừa các phương thức widget chung từ :class:`Widget`, cũng như các phương thức :meth:`!set` và
   :meth:`!get` từ :class:`tkinter.Scrollbar`.


.. class:: Separator(master=None, **kw)

   widget Ttk :class:`Separator`, hiển thị một đường phân cách ngang hoặc dọc. Widget này không có đối tác trực tiếp trong :mod:`tkinter` và kế thừa các phương thức widget chung từ :class:`Widget`.


.. class:: Sizegrip(master=None, **kw)

   widget Ttk :class:`Sizegrip`, hiển thị một tay nắm cho phép người dùng thay đổi kích thước cửa sổ toplevel chứa nó bằng cách nhấn và kéo tay nắm, thường được đặt ở góc dưới bên phải. Widget này không có đối tác trực tiếp trong :mod:`tkinter` và kế thừa các phương thức widget chung từ :class:`Widget`.


.. class:: LabeledScale(master=None, variable=None, from_=0, to=10, **kw)

   Một :class:`Frame` chứa một :class:`Scale` và một :class:`Label` hiển thị giá trị hiện tại của scale. *variable* là :class:`~tkinter.IntVar` được scale theo dõi (một biến sẽ được tạo nếu không được cung cấp), còn *from_* và *to* xác định phạm vi của scale.

   .. method:: destroy()

      Hủy widget này và xóa trace callback đã đăng ký trên biến liên kết.


.. class:: LabelFrame(master=None, **kw)

   Bí danh của :class:`Labelframe`, được giữ lại để tương thích về cách đặt tên với
   :class:`tkinter.LabelFrame`.


.. class:: PanedWindow(master=None, **kw)

   Bí danh của :class:`Panedwindow`, được giữ lại để tương thích về cách đặt tên với
   :class:`tkinter.PanedWindow`.

.. _`Tk Widget Styling Support (TIP #48)`: https://tip.tcl-lang.org/48.html
.. _`Introduction to the Tk theme engine`: https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_intro.html
.. _`The Tile Widget Set`: https://tktable.sourceforge.net/tile/tile-tcl2004.pdf
