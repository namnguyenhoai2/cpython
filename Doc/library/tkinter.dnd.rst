:mod:`!tkinter.dnd` --- Hỗ trợ kéo và thả
=========================================

.. module:: tkinter.dnd
   :synopsis: Giao diện kéo và thả của Tkinter

**Mã nguồn:** :source:`Lib/tkinter/dnd.py`

--------------

.. note:: Tính năng này đang trong giai đoạn thử nghiệm và dự kiến sẽ bị loại bỏ khi được thay thế bằng Tk DND.

Module :mod:`!tkinter.dnd` cung cấp hỗ trợ kéo và thả cho các đối tượng trong cùng một ứng dụng, trong cùng một cửa sổ hoặc giữa các cửa sổ. Để cho phép kéo một đối tượng, bạn phải tạo một event binding cho đối tượng đó để bắt đầu quy trình kéo và thả. Thông thường, bạn liên kết một sự kiện ButtonPress với một callback function do bạn viết (xem :ref:`Bindings-and-Events`). Hàm này cần gọi :func:`dnd_start`, trong đó *source* là đối tượng sẽ được kéo, còn *event* là sự kiện đã gọi hàm đó (đối số của callback function).

Việc chọn một đối tượng đích diễn ra như sau:

#. Tìm kiếm từ trên xuống trong vùng bên dưới con trỏ chuột để tìm một widget đích:

   * widget đích phải có thuộc tính *dnd_accept* có thể gọi được;
   * nếu *dnd_accept* không tồn tại hoặc trả về ``None``, việc tìm kiếm sẽ chuyển sang widget cha;
   * nếu không tìm thấy widget đích, đối tượng đích là ``None``.

#. Gọi ``<old_target>.dnd_leave(source, event)``.
#. Gọi ``<new_target>.dnd_enter(source, event)``.
#. Gọi ``<target>.dnd_commit(source, event)`` để thông báo về thao tác thả.
#. Gọi ``<source>.dnd_end(target, event)`` để báo hiệu kết thúc thao tác kéo và thả.


.. class:: DndHandler(source, event)

   Lớp *DndHandler* xử lý các sự kiện kéo và thả bằng cách theo dõi các sự kiện Motion và ButtonRelease trên phần tử gốc của widget sự kiện.

   .. method:: cancel(event=None)

      Hủy quá trình kéo và thả.

   .. method:: finish(event, commit=0)

      Thực thi các hàm kết thúc thao tác kéo và thả.

   .. method:: on_motion(event)

      Kiểm tra vùng bên dưới chuột để tìm các đối tượng đích trong khi thực hiện thao tác kéo.

   .. method:: on_release(event)

      Báo hiệu kết thúc thao tác kéo khi mẫu release được kích hoạt.

.. function:: dnd_start(source, event)

   Hàm factory cho quá trình kéo và thả. Trả về instance :class:`DndHandler` quản lý thao tác kéo hoặc ``None`` nếu không thể bắt đầu thao tác kéo.

.. seealso::

   :ref:`Bindings-and-Events`
