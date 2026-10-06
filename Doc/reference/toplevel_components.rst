
.. _top-level:

***************************
Các thành phần cấp cao nhất
***************************

.. index:: single: interpreter

Trình thông dịch Python có thể nhận đầu vào từ nhiều nguồn: từ một script được truyền cho nó dưới dạng đầu vào chuẩn hoặc đối số chương trình, được nhập tương tác, từ tệp mã nguồn của module, v.v. Chương này trình bày cú pháp được sử dụng trong các trường hợp này.


.. _programs:

Chương trình Python hoàn chỉnh
==============================

.. index:: single: program

.. index::
   pair: module; sys
   pair: module; __main__
   pair: module; builtins

Mặc dù đặc tả ngôn ngữ không nhất thiết phải quy định cách gọi trình thông dịch ngôn ngữ, nhưng việc có một khái niệm về chương trình Python hoàn chỉnh vẫn hữu ích. Một chương trình Python hoàn chỉnh được thực thi trong một môi trường được khởi tạo ở mức tối thiểu: tất cả module tích hợp sẵn và module chuẩn đều khả dụng, nhưng chưa module nào được khởi tạo, ngoại trừ :mod:`sys` (các dịch vụ hệ thống khác nhau), :mod:`builtins` (các hàm tích hợp sẵn, ngoại lệ và ``None``) và :mod:`__main__`. Thành phần sau được dùng để cung cấp namespace cục bộ và toàn cục cho việc thực thi chương trình hoàn chỉnh.

Cú pháp của một chương trình Python hoàn chỉnh là cú pháp dành cho đầu vào từ tệp, được mô tả trong phần tiếp theo.

.. index::
   single: interactive mode
   pair: module; __main__

Trình thông dịch cũng có thể được gọi ở chế độ tương tác; trong trường hợp này, nó không đọc và thực thi một chương trình hoàn chỉnh mà đọc và thực thi từng câu lệnh (có thể là câu lệnh phức hợp) một lần. Môi trường ban đầu giống hệt môi trường của một chương trình hoàn chỉnh; mỗi câu lệnh được thực thi trong namespace của
:mod:`__main__`.

.. index::
   single: UNIX
   single: Windows
   single: command line
   single: standard input

Một chương trình hoàn chỉnh có thể được truyền cho trình thông dịch theo ba dạng: với tùy chọn dòng lệnh :option:`-c` *string*, dưới dạng tệp được truyền làm đối số dòng lệnh đầu tiên hoặc dưới dạng đầu vào chuẩn. Nếu tệp hoặc đầu vào chuẩn là thiết bị tty, trình thông dịch sẽ chuyển sang chế độ tương tác; nếu không, nó thực thi tệp như một chương trình hoàn chỉnh.


.. _file-input:

Đầu vào tệp
===========

Mọi đầu vào được đọc từ các tệp không tương tác đều có cùng dạng:

.. grammar-snippet::
   :group: python-grammar

   file_input: (NEWLINE | `statement`)* ENDMARKER

Cú pháp này được sử dụng trong các trường hợp sau:

* khi phân tích cú pháp một chương trình Python hoàn chỉnh (từ một tệp hoặc từ một chuỗi);

* khi phân tích cú pháp một module;

* khi phân tích cú pháp một chuỗi được truyền vào hàm :func:`exec`;


.. _interactive:

Đầu vào tương tác
=================

Đầu vào ở chế độ tương tác được phân tích cú pháp bằng ngữ pháp sau:

.. grammar-snippet::
   :group: python-grammar

   interactive_input: [`stmt_list`] NEWLINE | `compound_stmt` NEWLINE | ENDMARKER

Lưu ý rằng một câu lệnh phức hợp (compound statement) ở cấp cao nhất phải được theo sau bởi một dòng trống trong chế độ tương tác; điều này cần thiết để giúp bộ phân tích cú pháp xác định phần kết thúc của đầu vào.


.. _expression-input:

Đầu vào biểu thức
=================

.. index:: single: input
.. index:: pair: built-in function; eval

:func:`eval` được sử dụng cho đầu vào biểu thức. Nó bỏ qua khoảng trắng ở đầu. Đối số chuỗi của :func:`eval` phải có dạng sau:

.. grammar-snippet::
   :group: python-grammar

   eval_input: `expression_list` NEWLINE* ENDMARKER
