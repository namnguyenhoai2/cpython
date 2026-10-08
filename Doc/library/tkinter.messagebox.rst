:mod:`!tkinter.messagebox` --- Lời nhắc thông báo Tkinter
=========================================================

.. module:: tkinter.messagebox
   :synopsis: Nhiều loại hộp thoại cảnh báo

**Mã nguồn:** :source:`Lib/tkinter/messagebox.py`

--------------

Mô-đun :mod:`!tkinter.messagebox` cung cấp một lớp cơ sở mẫu cùng nhiều phương thức tiện ích cho các cấu hình thường dùng. Các hộp thông báo là modal: mỗi hộp sẽ chặn cho đến khi người dùng phản hồi, sau đó trả về một giá trị phụ thuộc vào hàm. Các hàm ``show*`` và :meth:`Message.show` trả về tên ký hiệu của nút mà người dùng đã nhấn dưới dạng chuỗi (chẳng hạn như :data:`OK` hoặc :data:`YES`). Các kiểu và bố cục hộp thông báo phổ biến bao gồm nhưng không chỉ giới hạn ở:

.. figure:: tk_msg.png

.. class:: Message(master=None, **options)

   Tạo một cửa sổ thông báo với thông báo, biểu tượng và tập hợp nút do ứng dụng chỉ định. Mỗi nút trong cửa sổ thông báo được xác định bằng một tên ký hiệu duy nhất (xem các tùy chọn *type*).

   Các tùy chọn sau được hỗ trợ:

      *command*
         Chỉ định hàm cần gọi khi người dùng đóng hộp thoại. Tên của nút mà người dùng nhấp để đóng hộp thoại được truyền dưới dạng đối số. Tùy chọn này chỉ khả dụng trên macOS.

      *default*
         Cung cấp :ref:`tên tượng trưng <messagebox-buttons>` của nút mặc định cho cửa sổ thông báo này (:data:`OK`, :data:`CANCEL`, v.v.). Nếu không chỉ định tùy chọn này, nút đầu tiên trong hộp thoại sẽ được đặt làm nút mặc định.

      *detail*
         Chỉ định thông báo bổ sung cho thông báo chính được cung cấp bởi tùy chọn *message*. Chi tiết thông báo sẽ được hiển thị bên dưới thông báo chính và, nếu được hệ điều hành hỗ trợ, bằng phông chữ ít được nhấn mạnh hơn thông báo chính.

      *icon*
         Chỉ định :ref:`icon <messagebox-icons>` cần hiển thị. Nếu không chỉ định tùy chọn này, biểu tượng :data:`INFO` sẽ được hiển thị.

      *message*
         Chỉ định thông báo sẽ hiển thị trong hộp thoại thông báo này. Giá trị mặc định là chuỗi rỗng.

      *parent*
         Đặt cửa sổ được chỉ định làm cửa sổ cha logic của hộp thoại thông báo. Hộp thoại thông báo được hiển thị bên trên cửa sổ cha.

      *title*
         Chỉ định một chuỗi để hiển thị làm tiêu đề của hộp thoại thông báo. Tùy chọn này bị bỏ qua trên macOS, nơi các nguyên tắc của nền tảng không cho phép sử dụng tiêu đề cho loại hộp thoại này.

      *type*
         Sắp xếp để :ref:`một tập hợp nút được xác định trước <messagebox-types>` hiển thị.

   .. note::

      Tk 8.6 đã bổ sung tùy chọn *command*.

   .. method:: show(**options)

      Hiển thị cửa sổ thông báo và chờ người dùng chọn một trong các nút. Sau đó trả về tên ký hiệu của nút đã chọn. Các đối số từ khóa có thể ghi đè các tùy chọn được chỉ định trong hàm khởi tạo.


**Hộp thoại thông tin**

.. function:: showinfo(title=None, message=None, **options)

   Tạo và hiển thị hộp thoại thông tin với tiêu đề và thông báo được chỉ định.

**Hộp thoại cảnh báo**

.. function:: showwarning(title=None, message=None, **options)

   Tạo và hiển thị hộp thoại cảnh báo với tiêu đề và thông báo được chỉ định.

.. function:: showerror(title=None, message=None, **options)

   Tạo và hiển thị hộp thông báo lỗi với tiêu đề và thông báo được chỉ định.

**Hộp thoại câu hỏi**

.. function:: askquestion(title=None, message=None, *, type=YESNO, **options)

   Đặt một câu hỏi. Theo mặc định, hiển thị các nút :data:`YES` và :data:`NO`. Trả về tên ký hiệu của nút được chọn.

.. function:: askokcancel(title=None, message=None, **options)

   Hỏi xem có nên tiếp tục thao tác hay không. Hiển thị các nút :data:`OK` và :data:`CANCEL`. Trả về ``True`` nếu câu trả lời là ok và ``False`` trong các trường hợp khác.

.. function:: askretrycancel(title=None, message=None, **options)

   Hỏi xem có nên thử lại thao tác hay không. Hiển thị các nút :data:`RETRY` và :data:`CANCEL`. Trả về ``True`` nếu câu trả lời là retry và ``False`` trong các trường hợp khác.

.. function:: askyesno(title=None, message=None, **options)

   Đặt một câu hỏi. Hiển thị các nút :data:`YES` và :data:`NO`. Trả về ``True`` nếu câu trả lời là yes và ``False`` trong các trường hợp khác.

.. function:: askyesnocancel(title=None, message=None, **options)

   Đặt một câu hỏi. Hiển thị các nút :data:`YES`, :data:`NO` và :data:`CANCEL`. Trả về ``True`` nếu câu trả lời là yes, ``None`` nếu bị hủy và ``False`` trong các trường hợp khác.


.. _messagebox-buttons:

Tên ký hiệu của các nút:

.. data:: ABORT
   :value: 'abort'
.. data:: RETRY
   :value: 'retry'
.. data:: IGNORE
   :value: 'ignore'
.. data:: OK
   :value: 'ok'
.. data:: CANCEL
   :value: 'cancel'
.. data:: YES
   :value: 'yes'
.. data:: NO
   :value: 'no'

.. _messagebox-types:

Các tập hợp nút được định nghĩa sẵn:

.. data:: ABORTRETRYIGNORE
   :value: 'abortretryignore'

   Hiển thị ba nút có tên ký hiệu là :data:`ABORT`,
   :data:`RETRY` và :data:`IGNORE`.

.. data:: OK
   :value: 'ok'
   :noindex:

   Hiển thị một nút có tên ký hiệu là :data:`OK`.

.. data:: OKCANCEL
   :value: 'okcancel'

   Hiển thị hai nút có tên ký hiệu là :data:`OK` và
   :data:`CANCEL`.

.. data:: RETRYCANCEL
   :value: 'retrycancel'

   Hiển thị hai nút có tên ký hiệu là :data:`RETRY` và
   :data:`CANCEL`.

.. data:: YESNO
   :value: 'yesno'

   Hiển thị hai nút có tên tượng trưng là :data:`YES` và
   :data:`NO`.

.. data:: YESNOCANCEL
   :value: 'yesnocancel'

   Hiển thị ba nút có tên tượng trưng là :data:`YES`,
   :data:`NO` và :data:`CANCEL`.

.. _messagebox-icons:

Hình ảnh biểu tượng:

.. data:: ERROR
   :value: 'error'
.. data:: INFO
   :value: 'info'
.. data:: QUESTION
   :value: 'question'
.. data:: WARNING
   :value: 'warning'
