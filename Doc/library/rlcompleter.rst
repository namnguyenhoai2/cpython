:mod:`!rlcompleter` --- Hàm hoàn tất cho GNU readline
=====================================================

.. module:: rlcompleter
   :synopsis: Hoàn tất các định danh Python, phù hợp để sử dụng với thư viện GNU readline.

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/rlcompleter.py`

--------------

Mô-đun :mod:`!rlcompleter` định nghĩa một hàm hoàn tất phù hợp để truyền vào :func:`~readline.set_completer` trong mô-đun :mod:`readline`.

Khi mô-đun này được nhập trên nền tảng Unix có mô-đun :mod:`readline` available, một thực thể của lớp :class:`Completer` sẽ tự động được tạo và phương thức :meth:`~Completer.complete` của thực thể đó được đặt làm
:ref:`trình hoàn tất readline <readline-completion>`. Phương thức này cung cấp tính năng hoàn tất các :ref:`định danh và từ khóa <identifiers>` Python hợp lệ.

Ví dụ::

   >>> import rlcompleter
   >>> import readline
   >>> readline.parse_and_bind("tab: complete")
   >>> readline. <TAB PRESSED>
   readline.__doc__          readline.get_line_buffer(  readline.read_init_file(
   readline.__file__         readline.insert_text(      readline.set_completer(
   readline.__name__         readline.parse_and_bind(
   >>> readline.

Mô-đun :mod:`!rlcompleter` được thiết kế để sử dụng với Python's
:ref:`chế độ tương tác <tut-interactive>`.  Trừ khi Python được chạy với
:option:`-S` option, mô-đun sẽ được tự động nhập và cấu hình (xem :ref:`rlcompleter-config`).

Trên các nền tảng không có :mod:`readline`, lớp :class:`Completer` do mô-đun này định nghĩa vẫn có thể được sử dụng cho các mục đích tùy chỉnh.


.. _completer-objects:

.. class:: Completer

   Các đối tượng Completer có phương thức sau:

   .. method:: Completer.complete(text, state)

      Trả về nội dung hoàn thành khả dĩ tiếp theo cho *văn bản*.

      Khi được mô-đun :mod:`readline` gọi, phương thức này được gọi liên tiếp với ``state == 0, 1, 2, ...`` cho đến khi phương thức trả về ``None``.

      Nếu được gọi cho *text* không chứa ký tự dấu chấm (``'.'``), hàm này sẽ hoàn tất từ các tên hiện được định nghĩa trong :mod:`__main__`, :mod:`builtins` và các từ khóa (như được định nghĩa bởi mô-đun :mod:`keyword`).

      Nếu được gọi cho một tên có dấu chấm, hàm này sẽ cố gắng đánh giá mọi thành phần không có tác dụng phụ rõ ràng (các hàm sẽ không được đánh giá, nhưng hàm này có thể tạo ra các lệnh gọi đến
      :meth:`~object.__getattr__`) cho đến phần cuối cùng, rồi tìm các kết quả khớp cho phần còn lại thông qua hàm :func:`dir`. Mọi ngoại lệ phát sinh trong quá trình đánh giá biểu thức đều được bắt, im lặng xử lý và trả về :const:`None`.
