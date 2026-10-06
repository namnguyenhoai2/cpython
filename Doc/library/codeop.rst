:mod:`!codeop` --- Biên dịch mã Python
======================================

.. module:: codeop
   :synopsis: Biên dịch mã Python (có thể chưa hoàn chỉnh).

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>
.. sectionauthor:: Michael Hudson <mwh@python.net>

**Mã nguồn:** :source:`Lib/codeop.py`

--------------

Mô-đun :mod:`!codeop` cung cấp các tiện ích để mô phỏng vòng lặp đọc-đánh giá-in của Python, như được thực hiện trong mô-đun :mod:`code`. Do đó, có lẽ bạn không muốn sử dụng trực tiếp mô-đun này; nếu muốn đưa một vòng lặp như vậy vào chương trình, có lẽ bạn nên sử dụng mô-đun :mod:`code` thay thế.

Công việc này gồm hai phần:

#. Có khả năng xác định xem một dòng đầu vào đã hoàn tất một câu lệnh Python hay chưa: nói ngắn gọn là xác định xem tiếp theo cần in '``>>>``' hay '``...``'.

#. Ghi nhớ những câu lệnh future mà người dùng đã nhập, để các đầu vào tiếp theo có thể được biên dịch với những câu lệnh này đang có hiệu lực.

Mô-đun :mod:`!codeop` cung cấp một cách để thực hiện từng việc này, cũng như một cách để thực hiện cả hai việc.

Để chỉ thực hiện việc đầu tiên:

.. function:: compile_command(source, filename="<input>", symbol="single")

   Cố gắng biên dịch *source*, vốn phải là một chuỗi mã Python và trả về một đối tượng mã nếu *source* là mã Python hợp lệ. Trong trường hợp đó, thuộc tính filename của đối tượng mã sẽ là *filename*, với giá trị mặc định là ``'<input>'``. Trả về ``None`` nếu *source* là *not* mã Python hợp lệ nhưng lại là tiền tố của mã Python hợp lệ.

   Nếu có vấn đề với *source*, một exception sẽ được phát sinh.
   :exc:`SyntaxError` được phát sinh nếu cú pháp Python không hợp lệ, và
   :exc:`OverflowError` hoặc :exc:`ValueError` nếu có literal không hợp lệ.

   Đối số *symbol* xác định liệu *source* được biên dịch dưới dạng một câu lệnh (``'single'``, mặc định), dưới dạng một chuỗi :term:`statement` (``'exec'``) hay dưới dạng một :term:`expression` (``'eval'``). Bất kỳ giá trị nào khác sẽ khiến :exc:`ValueError` được phát sinh.

   .. note::

      Có khả năng (nhưng không đáng kể) parser dừng việc phân tích với kết quả thành công trước khi đến cuối mã nguồn; trong trường hợp này, các ký hiệu ở cuối có thể bị bỏ qua thay vì gây ra lỗi. Ví dụ, sau một dấu gạch chéo ngược theo sau bởi hai dòng mới có thể là nội dung rác bất kỳ. Điều này sẽ được khắc phục khi API của parser được cải thiện hơn.


.. class:: Compile()

   Các instance của lớp này có các phương thức :meth:`~object.__call__` với chữ ký giống hệt hàm dựng sẵn :func:`compile`, nhưng khác ở chỗ nếu instance biên dịch văn bản chương trình có chứa câu lệnh :mod:`__future__`, instance sẽ 'ghi nhớ' và biên dịch mọi văn bản chương trình tiếp theo với câu lệnh đó được áp dụng.


.. class:: CommandCompiler()

   Các instance của lớp này có các phương thức :meth:`~object.__call__` với chữ ký giống hệt
   :func:`compile_command`; điểm khác biệt là nếu instance biên dịch văn bản chương trình có chứa câu lệnh :mod:`__future__`, instance sẽ 'ghi nhớ' và biên dịch mọi văn bản chương trình tiếp theo với câu lệnh đó được áp dụng.
