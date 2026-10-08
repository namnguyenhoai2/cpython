:mod:`!html.entities` --- Định nghĩa các thực thể tổng quát của HTML
====================================================================

.. module:: html.entities
   :synopsis: Định nghĩa các thực thể tổng quát của HTML.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/html/entities.py`

--------------

Mô-đun này định nghĩa bốn từ điển, :data:`html5`,
:data:`name2codepoint`, :data:`codepoint2name`, và :data:`entitydefs`.


.. data:: html5

   Một từ điển ánh xạ các tham chiếu ký tự có tên HTML5 [#]_ với (các) ký tự Unicode tương đương, ví dụ ``html5['gt;'] == '>'``. Lưu ý rằng dấu chấm phẩy ở cuối được bao gồm trong tên (ví dụ ``'gt;'``), tuy nhiên tiêu chuẩn chấp nhận một số tên ngay cả khi không có dấu chấm phẩy: trong trường hợp này, tên xuất hiện cả khi có và không có ``';'``. Xem thêm :func:`html.unescape`.

   .. versionadded:: 3.3


.. data:: entitydefs

   Một từ điển ánh xạ các định nghĩa thực thể XHTML 1.0 với văn bản thay thế tương ứng trong ISO Latin-1.


.. data:: name2codepoint

   Một dictionary ánh xạ tên entity HTML4 tới các code point Unicode.


.. data:: codepoint2name

   Một dictionary ánh xạ các code point Unicode tới tên entity HTML4.


.. rubric:: Chú thích cuối trang

.. [#] Xem https://html.spec.whatwg.org/multipage/named-characters.html#named-character-references
