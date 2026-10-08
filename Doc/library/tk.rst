.. _tkinter:

**********************************
Giao diện người dùng đồ họa với Tk
**********************************

.. index::
   single: GUI
   single: Graphical User Interface
   single: Tkinter
   single: Tk

Tk/Tcl từ lâu đã là một phần không thể thiếu của Python. Nó cung cấp một bộ công cụ cửa sổ mạnh mẽ và độc lập với nền tảng, sẵn có cho các lập trình viên Python thông qua package :mod:`tkinter` và module mở rộng :mod:`tkinter.ttk`.

Package :mod:`tkinter` là một lớp hướng đối tượng mỏng bên trên Tcl/Tk. Để sử dụng :mod:`tkinter`, bạn không cần viết mã Tcl, nhưng sẽ cần tham khảo tài liệu Tk và đôi khi cả tài liệu Tcl.
:mod:`tkinter` là một tập hợp các wrapper triển khai những widget Tk dưới dạng các lớp Python.

Ưu điểm chính của :mod:`tkinter` là tốc độ nhanh và thường được đóng gói sẵn cùng Python. Mặc dù tài liệu chuẩn còn hạn chế, vẫn có nhiều tài liệu hữu ích, bao gồm tài liệu tham khảo, hướng dẫn, sách và nhiều tài liệu khác. :mod:`tkinter` cũng nổi tiếng vì có giao diện và trải nghiệm lỗi thời, nhưng những điểm này đã được cải thiện đáng kể trong Tk 8.5. Tuy vậy, bạn có thể quan tâm đến nhiều thư viện GUI khác. Python wiki liệt kê một số `framework và công cụ GUI thay thế <https://wiki.python.org/moin/GuiProgramming>`_.

.. toctree::

   tkinter.rst
   tkinter.colorchooser.rst
   tkinter.font.rst
   dialog.rst
   tkinter.messagebox.rst
   tkinter.scrolledtext.rst
   tkinter.dnd.rst
   tkinter.ttk.rst
   idle.rst
   turtle.rst

.. Other sections I have in mind are
   Tkinter internals
   Freezing Tkinter applications

.. _`GUI frameworks and tools`: https://wiki.python.org/moin/GuiProgramming
