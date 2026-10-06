:mod:`!curses.panel` --- Phần mở rộng ngăn xếp panel cho curses
===============================================================

.. module:: curses.panel
   :synopsis: Phần mở rộng ngăn xếp panel bổ sung độ sâu cho các cửa sổ curses.

.. sectionauthor:: A.M. Kuchling <amk@amk.ca>

--------------

Panel là các cửa sổ có thêm tính năng độ sâu, nhờ đó chúng có thể được xếp chồng lên nhau và chỉ những phần hiển thị của mỗi cửa sổ mới được hiển thị. Panel có thể được thêm vào, di chuyển lên hoặc xuống trong ngăn xếp và xóa bỏ.


.. _cursespanel-functions:

Các hàm
-------

Module :mod:`!curses.panel` định nghĩa ngoại lệ sau:


.. exception:: error

   Ngoại lệ được phát sinh khi một hàm của thư viện panel curses trả về lỗi.


Module :mod:`!curses.panel` định nghĩa các hàm sau:


.. function:: bottom_panel()

   Trả về panel ở dưới cùng trong ngăn xếp panel.


.. function:: new_panel(win)

   Trả về một đối tượng panel, liên kết đối tượng đó với cửa sổ đã cho *win* và đặt panel mới lên trên cùng của ngăn xếp panel. Hãy lưu ý rằng bạn cần giữ tham chiếu rõ ràng đến đối tượng panel được trả về. Nếu không, đối tượng panel sẽ bị garbage collection và bị xóa khỏi ngăn xếp panel.


.. function:: top_panel()

   Trả về panel ở trên cùng trong ngăn xếp panel.


.. function:: update_panels()

   Cập nhật màn hình ảo sau khi có thay đổi trong ngăn xếp panel. Thao tác này không gọi
   :func:`curses.doupdate`, vì vậy bạn sẽ phải tự thực hiện việc này.


.. _curses-panel-objects:

Các đối tượng panel
-------------------

.. raw:: html

   <!-- Keep the old URL fragments working (see gh-89554) -->
   <span id='curses.panel.Panel.above'></span>
   <span id='curses.panel.Panel.below'></span>
   <span id='curses.panel.Panel.bottom'></span>
   <span id='curses.panel.Panel.hidden'></span>
   <span id='curses.panel.Panel.hide'></span>
   <span id='curses.panel.Panel.move'></span>
   <span id='curses.panel.Panel.replace'></span>
   <span id='curses.panel.Panel.set_userptr'></span>
   <span id='curses.panel.Panel.show'></span>
   <span id='curses.panel.Panel.top'></span>
   <span id='curses.panel.Panel.userptr'></span>
   <span id='curses.panel.Panel.window'></span>

.. class:: panel

   Các đối tượng panel, như được :func:`new_panel` trả về ở trên, là các cửa sổ có thứ tự xếp chồng. Luôn có một cửa sổ được liên kết với một panel để xác định nội dung, trong khi các phương thức của panel chịu trách nhiệm về độ sâu của cửa sổ trong ngăn xếp panel.

   Các đối tượng Panel có các phương thức sau:


.. method:: panel.above()

   Trả về panel nằm trên panel hiện tại.


.. method:: panel.below()

   Trả về panel nằm dưới panel hiện tại.


.. method:: panel.bottom()

   Đưa panel xuống cuối stack.


.. method:: panel.hidden()

   Trả về ``True`` nếu panel bị ẩn (không hiển thị), nếu không thì trả về ``False``.


.. method:: panel.hide()

   Ẩn panel. Thao tác này không xóa đối tượng mà chỉ làm cho cửa sổ trên màn hình trở nên vô hình.


.. method:: panel.move(y, x)

   Di chuyển panel đến tọa độ màn hình ``(y, x)``.


.. method:: panel.replace(win)

   Thay đổi window được liên kết với panel thành window *win*.


.. method:: panel.set_userptr(obj)

   Đặt con trỏ user của panel thành *obj*. Con trỏ này được dùng để liên kết một phần dữ liệu bất kỳ với panel và có thể là bất kỳ đối tượng Python nào.


.. method:: panel.show()

   Hiển thị panel (có thể trước đó đã bị ẩn), đưa panel lên đầu ngăn xếp panel.


.. method:: panel.top()

   Đưa panel lên đầu ngăn xếp.


.. method:: panel.userptr()

   Trả về con trỏ user của panel. Con trỏ này có thể là bất kỳ đối tượng Python nào.


.. method:: panel.window()

   Trả về đối tượng window được liên kết với panel.

