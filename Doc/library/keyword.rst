:mod:`!keyword` --- Kiểm tra các từ khóa Python
===============================================

.. module:: keyword
   :synopsis: Kiểm tra xem một chuỗi có phải là từ khóa trong Python hay không.

**Mã nguồn:** :source:`Lib/keyword.py`

--------------

Mô-đun này cho phép một chương trình Python xác định xem một chuỗi có phải là
:ref:`từ khóa <keywords>` hoặc :ref:`từ khóa mềm <soft-keywords>` hay không.


.. function:: iskeyword(s)

   Trả về ``True`` nếu *s* là một :ref:`từ khóa <keywords>` Python.


.. data:: kwlist

   Dãy chứa tất cả :ref:`từ khóa <keywords>` được định nghĩa cho trình thông dịch.  Nếu có bất kỳ từ khóa nào được định nghĩa là chỉ hoạt động khi một số
   Các câu lệnh :mod:`__future__` đang có hiệu lực; các câu lệnh này cũng sẽ được bao gồm.


.. function:: issoftkeyword(s)

   Trả về ``True`` nếu *s* là một từ khóa :ref:`mềm <soft-keywords>` của Python.

   .. versionadded:: 3.9


.. data:: softkwlist

   Chuỗi chứa tất cả :ref:`từ khóa mềm <soft-keywords>` được định nghĩa cho trình thông dịch. Nếu bất kỳ từ khóa mềm nào được định nghĩa là chỉ hoạt động khi các điều kiện cụ thể
   Các câu lệnh :mod:`__future__` đang có hiệu lực; các câu lệnh này cũng sẽ được bao gồm.

   .. versionadded:: 3.9
