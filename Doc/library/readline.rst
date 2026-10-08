:mod:`!readline` --- giao diện GNU readline
===========================================

.. module:: readline
   :synopsis: Hỗ trợ GNU readline cho Python.

.. sectionauthor:: Skip Montanaro <skip.montanaro@gmail.com>

--------------

Mô-đun :mod:`!readline` định nghĩa một số hàm để hỗ trợ việc hoàn tất và đọc/ghi các tệp lịch sử từ trình thông dịch Python. Mô-đun này có thể được sử dụng trực tiếp hoặc thông qua mô-đun :mod:`rlcompleter`, mô-đun hỗ trợ hoàn tất các định danh Python tại dấu nhắc tương tác. Các thiết lập được thực hiện bằng mô-đun này ảnh hưởng đến cả dấu nhắc tương tác của trình thông dịch và các dấu nhắc do hàm tích hợp :func:`input` cung cấp.

Các liên kết phím của Readline có thể được cấu hình thông qua một tệp khởi tạo, thường là ``.inputrc`` trong thư mục chính của bạn. Xem `Tệp khởi tạo Readline <https://tiswww.cwru.edu/php/chet/readline/rluserman.html#Readline-Init-File>`_ trong hướng dẫn sử dụng GNU Readline để biết thông tin về định dạng và các cấu trúc được phép trong tệp đó, cũng như các khả năng của thư viện Readline nói chung.

.. include:: ../includes/wasm-mobile-notavail.rst

.. include:: ../includes/optional-module.rst

.. availability:: Unix.

.. note::

  API của thư viện Readline nền tảng có thể được triển khai bởi thư viện ``editline`` (``libedit``) thay vì GNU readline. Trên macOS, mô-đun :mod:`!readline` phát hiện thư viện nào đang được sử dụng tại thời điểm chạy.

  Tệp cấu hình của ``editline`` khác với tệp cấu hình của GNU readline. Nếu bạn tải các chuỗi cấu hình theo cách lập trình, bạn có thể sử dụng :data:`backend` để xác định thư viện nào đang được sử dụng.

  Nếu bạn sử dụng tính năng mô phỏng readline ``editline``/``libedit`` trên macOS, tệp khởi tạo nằm trong thư mục chính của bạn có tên là ``.editrc``. Ví dụ, nội dung sau trong ``~/.editrc`` sẽ BẬT *vi* các liên kết phím và tính năng hoàn tất bằng TAB::

    python:bind -v
    python:bind ^I rl_complete

  Cũng lưu ý rằng các thư viện khác nhau có thể sử dụng các định dạng tệp history khác nhau. Khi chuyển đổi thư viện nền, các tệp history hiện có có thể không sử dụng được.

.. data:: backend

   Tên của thư viện Readline nền đang được sử dụng, ``"readline"`` hoặc ``"editline"``.

   .. versionadded:: 3.13

Tệp init
--------

Các hàm sau đây liên quan đến tệp init và cấu hình người dùng:


.. function:: parse_and_bind(string)

   Thực thi dòng init được cung cấp trong đối số *string*. Lệnh này gọi
   :c:func:`!rl_parse_and_bind` trong thư viện nền.


.. function:: read_init_file([filename])

   Thực thi tệp khởi tạo readline. Tên tệp mặc định là tên tệp được sử dụng gần đây nhất. Lệnh này gọi :c:func:`!rl_read_init_file` trong thư viện nền. Lệnh này phát sinh :ref:`sự kiện kiểm tra <auditing>` ``open`` với tên tệp nếu được cung cấp, và :code:`"<readline_init_file>"` nếu không, bất kể thư viện phân giải tệp nào.

   .. versionchanged:: 3.14
      Sự kiện kiểm tra đã được thêm.


Bộ đệm dòng
-----------

Các hàm sau đây hoạt động trên bộ đệm dòng:


.. function:: get_line_buffer()

   Trả về nội dung hiện tại của bộ đệm dòng (:c:data:`!rl_line_buffer` trong thư viện bên dưới).


.. function:: insert_text(string)

   Chèn văn bản vào bộ đệm dòng tại vị trí con trỏ. Thao tác này gọi
   :c:func:`!rl_insert_text` trong thư viện bên dưới nhưng bỏ qua giá trị trả về.


.. function:: redisplay()

   Thay đổi nội dung hiển thị trên màn hình để phản ánh nội dung hiện tại của bộ đệm dòng. Thao tác này gọi :c:func:`!rl_redisplay` trong thư viện bên dưới.


Tệp lịch sử
-----------

Các hàm sau đây hoạt động trên một tệp lịch sử:


.. function:: read_history_file([filename])

   Tải một tệp lịch sử readline và nối tệp đó vào danh sách lịch sử. Tên tệp mặc định là :file:`~/.history`.  Hàm này gọi
   :c:func:`!read_history` trong thư viện nền tảng và phát ra một :ref:`sự kiện auditing <auditing>` ``open`` với tên tệp nếu được cung cấp, và :code:`"~/.history"` nếu không.

   .. versionchanged:: 3.14
      Sự kiện auditing đã được thêm.


.. function:: write_history_file([filename])

   Lưu danh sách lịch sử vào một tệp lịch sử readline, ghi đè mọi tệp hiện có.  Tên tệp mặc định là :file:`~/.history`.  Hàm này gọi
   :c:func:`!write_history` trong thư viện nền tảng và phát ra một
   :ref:`sự kiện auditing <auditing>` ``open`` cùng với tên tệp nếu được cung cấp và
   :code:`"~/.history"` nếu không.

   .. versionchanged:: 3.14
      Sự kiện auditing đã được thêm.


.. function:: append_history_file(nelements[, filename])

   Nối các mục lịch sử *nelements* cuối cùng vào một tệp.  Tên tệp mặc định là
   :file:`~/.history`.  Tệp phải tồn tại từ trước.  Lệnh này gọi
   :c:func:`!append_history` trong thư viện nền tảng.  Hàm này chỉ tồn tại nếu Python được biên dịch cho một phiên bản thư viện hỗ trợ hàm này. Hàm này phát sinh một :ref:`sự kiện auditing <auditing>` ``open`` cùng với tên tệp nếu được cung cấp và :code:`"~/.history"` nếu không.

   .. versionadded:: 3.5

   .. versionchanged:: 3.14
      Sự kiện auditing đã được thêm.


.. function:: get_history_length()
              set_history_length(length)

   Đặt hoặc trả về số dòng mong muốn được lưu trong tệp lịch sử. Hàm :func:`write_history_file` sử dụng giá trị này để cắt ngắn tệp lịch sử bằng cách gọi :c:func:`!history_truncate_file` trong thư viện bên dưới. Các giá trị âm biểu thị kích thước tệp lịch sử không giới hạn.


Danh sách lịch sử
-----------------

Các hàm sau đây hoạt động trên một danh sách lịch sử toàn cục:


.. function:: clear_history()

   Xóa lịch sử hiện tại. Thao tác này gọi :c:func:`!clear_history` trong thư viện bên dưới. Hàm Python chỉ tồn tại nếu Python được biên dịch cho một phiên bản của thư viện có hỗ trợ hàm này.


.. function:: get_current_history_length()

   Trả về số mục hiện có trong lịch sử. (Điều này khác với
   :func:`get_history_length`, hàm trả về số dòng tối đa sẽ được ghi vào tệp lịch sử.)


.. function:: get_history_item(index)

   Trả về nội dung hiện tại của mục lịch sử tại *index*. Chỉ mục của mục được đánh số bắt đầu từ một. Thao tác này gọi :c:func:`!history_get` trong thư viện nền tảng.


.. function:: remove_history_item(pos)

   Xóa mục lịch sử được chỉ định theo vị trí khỏi lịch sử. Vị trí được đánh số bắt đầu từ không. Thao tác này gọi :c:func:`!remove_history` trong thư viện nền tảng.


.. function:: replace_history_item(pos, line)

   Thay thế mục lịch sử được chỉ định theo vị trí bằng *line*. Vị trí được đánh số bắt đầu từ không. Thao tác này gọi :c:func:`!replace_history_entry` trong thư viện nền tảng.


.. function:: add_history(line)

   Thêm *line* vào bộ đệm lịch sử, như thể đó là dòng cuối cùng được nhập. Thao tác này gọi :c:func:`!add_history` trong thư viện nền tảng.


.. function:: set_auto_history(enabled)

   Bật hoặc tắt việc tự động gọi :c:func:`!add_history` khi đọc đầu vào thông qua readline. Đối số *enabled* phải là một giá trị Boolean: khi là true, đối số này bật lịch sử tự động; khi là false, đối số này tắt lịch sử tự động.

   .. versionadded:: 3.6

   .. impl-detail::
      Lịch sử tự động được bật theo mặc định và các thay đổi đối với tùy chọn này không được duy trì qua nhiều phiên.


Các hook khởi động
------------------


.. function:: set_startup_hook([function])

   Thiết lập hoặc xóa hàm được gọi bởi callback :c:data:`!rl_startup_hook` của thư viện bên dưới. Nếu chỉ định *function*, hàm này sẽ được dùng làm hàm hook mới; nếu bỏ qua hoặc là ``None``, mọi hàm đã được cài đặt trước đó sẽ bị xóa. Hook được gọi không có đối số ngay trước khi readline in lời nhắc đầu tiên.


.. function:: set_pre_input_hook([function])

   Thiết lập hoặc xóa hàm được gọi bởi callback :c:data:`!rl_pre_input_hook` của thư viện bên dưới. Nếu chỉ định *function*, hàm này sẽ được dùng làm hàm hook mới; nếu bỏ qua hoặc là ``None``, mọi hàm đã được cài đặt trước đó sẽ bị xóa. Hook được gọi không có đối số sau khi lời nhắc đầu tiên được in và ngay trước khi readline bắt đầu đọc các ký tự đầu vào. Hàm này chỉ tồn tại nếu Python được biên dịch cho một phiên bản của thư viện có hỗ trợ hàm này.


.. _readline-completion:

Hoàn tất
--------

Các hàm sau đây liên quan đến việc triển khai hàm hoàn tất từ tùy chỉnh. Thông thường, chức năng này được kích hoạt bằng phím Tab, có thể gợi ý và tự động hoàn tất một từ đang được nhập. Theo mặc định, Readline được thiết lập để :mod:`rlcompleter` hoàn tất các định danh Python cho trình thông dịch tương tác. Nếu sử dụng module :mod:`!readline` với một completer tùy chỉnh, cần thiết lập một tập dấu phân cách từ khác.


.. function:: set_completer([function])

   Thiết lập hoặc xóa hàm completer. Nếu chỉ định *function*, hàm này sẽ được dùng làm hàm completer mới; nếu bỏ qua hoặc là ``None``, mọi hàm completer đã được cài đặt trước đó sẽ bị xóa. Hàm completer được gọi như ``function(text, state)``, với *state* trong ``0``, ``1``, ``2``, ... cho đến khi hàm trả về một giá trị không phải chuỗi. Hàm này cần trả về nội dung hoàn tất khả dĩ tiếp theo bắt đầu bằng *text*.

   Hàm completer đã cài đặt được gọi bởi callback *entry_func* được truyền cho :c:func:`!rl_completion_matches` trong thư viện bên dưới. Chuỗi *text* xuất phát từ tham số đầu tiên của
   callback :c:data:`!rl_attempted_completion_function` của thư viện bên dưới.


.. function:: get_completer()

   Lấy hàm completer hoặc ``None`` nếu chưa thiết lập hàm completer.


.. function:: get_completion_type()

   Lấy loại completion đang được thực hiện. Giá trị này trả về
   biến :c:data:`!rl_completion_type` trong thư viện nền tảng dưới dạng số nguyên.


.. function:: get_begidx()
              get_endidx()

   Lấy chỉ mục bắt đầu hoặc kết thúc của phạm vi completion. Các chỉ mục này là các đối số *start* và *end* được truyền vào
   callback :c:data:`!rl_attempted_completion_function` của thư viện nền tảng. Các giá trị có thể khác nhau trong cùng một tình huống chỉnh sửa đầu vào, tùy thuộc vào cách triển khai C readline nền tảng. Ví dụ: libedit được biết là hoạt động khác với libreadline.


.. function:: set_completer_delims(string)
              get_completer_delims()

   Đặt hoặc lấy các dấu phân cách từ cho việc completion. Các dấu này xác định vị trí bắt đầu của từ được xem xét để completion (phạm vi completion). Các hàm này truy cập biến :c:data:`!rl_completer_word_break_characters` trong thư viện bên dưới.


.. function:: set_completion_display_matches_hook([function])

   Đặt hoặc xóa hàm hiển thị completion. Nếu *function* được chỉ định, hàm này sẽ được dùng làm hàm hiển thị completion mới; nếu bị bỏ qua hoặc là ``None``, mọi hàm hiển thị completion đã được cài đặt sẽ bị xóa. Thao tác này đặt hoặc xóa
   callback :c:data:`!rl_completion_display_matches_hook` trong thư viện bên dưới. Hàm hiển thị completion được gọi dưới dạng ``function(substitution, [matches], longest_match_length)`` mỗi khi cần hiển thị các kết quả khớp.


.. _readline-example:

Ví dụ
-----

Ví dụ sau minh họa cách sử dụng các hàm đọc và ghi history của module :mod:`!readline` để tự động tải và lưu tệp history có tên :file:`.python_history` từ thư mục home của người dùng. Đoạn mã dưới đây thường được thực thi tự động trong các phiên tương tác từ tệp :envvar:`PYTHONSTARTUP` của người dùng.::

   import atexit
   import os
   import readline

   histfile = os.path.join(os.path.expanduser("~"), ".python_history")
   try:
       readline.read_history_file(histfile)
       # độ dài history mặc định là -1 (vô hạn), có thể tăng đến mức khó kiểm soát
       readline.set_history_length(1000)
   except FileNotFoundError:
       pass

   atexit.register(readline.write_history_file, histfile)

Đoạn mã này thực sự được tự động chạy khi Python được chạy trong
:ref:`chế độ tương tác <tut-interactive>` (xem :ref:`rlcompleter-config`).

Ví dụ sau đây đạt được cùng mục tiêu nhưng hỗ trợ các phiên tương tác đồng thời bằng cách chỉ nối thêm lịch sử mới.::

   import atexit
   import os
   import readline
   histfile = os.path.join(os.path.expanduser("~"), ".python_history")

   try:
       readline.read_history_file(histfile)
       h_len = readline.get_current_history_length()
   except FileNotFoundError:
       open(histfile, 'wb').close()
       h_len = 0

   def save(prev_h_len, histfile):
       new_h_len = readline.get_current_history_length()
       readline.set_history_length(1000)
       readline.append_history_file(new_h_len - prev_h_len, histfile)
   atexit.register(save, h_len, histfile)

Ví dụ sau đây mở rộng lớp :class:`code.InteractiveConsole` để hỗ trợ lưu/khôi phục lịch sử.::

   import atexit
   import code
   import os
   import readline

   class HistoryConsole(code.InteractiveConsole):
       def __init__(self, locals=None, filename="<console>",
                    histfile=os.path.expanduser("~/.console-history")):
           code.InteractiveConsole.__init__(self, locals, filename)
           self.init_history(histfile)

       def init_history(self, histfile):
           readline.parse_and_bind("tab: complete")
           if hasattr(readline, "read_history_file"):
               try:
                   readline.read_history_file(histfile)
               except FileNotFoundError:
                   pass
               atexit.register(self.save_history, histfile)

       def save_history(self, histfile):
           readline.set_history_length(1000)
           readline.write_history_file(histfile)

.. note::

   :term:`REPL` mới được giới thiệu trong phiên bản 3.13 không hỗ trợ readline. Tuy nhiên, vẫn có thể sử dụng readline bằng cách đặt biến môi trường :envvar:`PYTHON_BASIC_REPL`.

.. _`Readline Init File`: https://tiswww.cwru.edu/php/chet/readline/rluserman.html#Readline-Init-File
