:mod:`!tkinter.colorchooser` --- Hộp thoại chọn màu
===================================================

.. module:: tkinter.colorchooser
   :synopsis: Hộp thoại chọn màu

**Mã nguồn:** :source:`Lib/tkinter/colorchooser.py`

--------------

Mô-đun :mod:`!tkinter.colorchooser` cung cấp lớp :class:`Chooser` làm giao diện cho hộp thoại chọn màu gốc. ``Chooser`` triển khai một cửa sổ hộp thoại chọn màu dạng modal. Lớp ``Chooser`` kế thừa từ lớp :class:`~tkinter.commondialog.Dialog`.

.. class:: Chooser(master=None, **options)

   Lớp triển khai hộp thoại chọn màu dạng modal. Hầu hết các ứng dụng sử dụng hàm tiện ích :func:`askcolor` thay vì khởi tạo trực tiếp lớp này.

.. function:: askcolor(color=None, **options)

   Hiển thị hộp thoại chọn màu dạng modal và trả về màu đã chọn. *color* là màu được chọn khi hộp thoại mở. Giá trị trả về là một tuple ``((r, g, b), hexstr)``, trong đó ``r``, ``g`` và ``b`` là các thành phần đỏ, lục và lam dưới dạng số nguyên trong phạm vi 0–255, còn *hexstr* là chuỗi màu Tk tương đương, chẳng hạn như ``'#ff8000'``. Nếu người dùng hủy hộp thoại, ``(None, None)`` sẽ được trả về.

   .. versionchanged:: 3.10
      Các giá trị RGB trong màu trả về hiện là số nguyên trong phạm vi 0–255 thay vì số thực.


.. seealso::

   Mô-đun :mod:`tkinter.commondialog`
      Mô-đun hộp thoại tiêu chuẩn Tkinter

