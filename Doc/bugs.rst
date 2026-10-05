.. _reporting-bugs:

*********
Xử lý lỗi
*********

Python là một ngôn ngữ lập trình成熟 đã xây dựng được danh tiếng về tính ổn định. Để duy trì danh tiếng này, các nhà phát triển muốn biết về mọi thiếu sót mà bạn phát hiện trong Python.

Đôi khi, tự sửa lỗi và đóng góp các bản vá cho Python sẽ nhanh hơn vì cách này tinh giản quy trình và có ít người tham gia hơn. Tìm hiểu cách
:ref:`đóng góp <contributing-to-python>`.

Lỗi tài liệu
============

Nếu bạn phát hiện lỗi trong tài liệu này hoặc muốn đề xuất một cải tiến, vui lòng gửi báo cáo lỗi trên :ref:`trình theo dõi issue <using-the-tracker>`. Nếu bạn có đề xuất về cách khắc phục, hãy gửi kèm đề xuất đó.

.. only:: translation

   Nếu lỗi hoặc cải tiến được đề xuất liên quan đến bản dịch của tài liệu này, thay vào đó hãy gửi báo cáo đến `repository của bản dịch <TRANSLATION_REPO_>`_.

Bạn cũng có thể mở một mục thảo luận trên `diễn đàn Documentation Discourse <https://discuss.python.org/c/documentation/26>`_ của chúng tôi.

Nếu bạn phát hiện lỗi trong theme (HTML / CSS / JavaScript) của tài liệu, vui lòng gửi báo cáo lỗi trên `trình theo dõi issue của python-doc-theme <https://github.com/python/python-docs-theme>`_.

.. seealso::

   `Lỗi tài liệu <Documentation bugs_>`_
      Danh sách các lỗi tài liệu đã được gửi đến trình theo dõi issue của Python.

   `Theo dõi issue <https://devguide.python.org/tracker/>`_
      Tổng quan về quy trình báo cáo một cải tiến trên trình theo dõi issue.

   `Đóng góp cho tài liệu <https://devguide.python.org/docquality/#helping-with-documentation>`_
      Hướng dẫn toàn diện dành cho những người quan tâm đến việc đóng góp cho tài liệu Python.

   `Bản dịch tài liệu <https://devguide.python.org/documentation/translating/>`_
      Danh sách các trang GitHub dành cho việc dịch tài liệu và những người liên hệ chính của từng trang.


.. _using-the-tracker:

Sử dụng trình theo dõi issue của Python
=======================================

Các báo cáo issue về bản thân Python nên được gửi thông qua trình theo dõi issue trên GitHub (https://github.com/python/cpython/issues). Trình theo dõi issue trên GitHub cung cấp một biểu mẫu web cho phép nhập và gửi thông tin liên quan đến các nhà phát triển.

Bước đầu tiên khi gửi báo cáo là xác định xem vấn đề đó đã được báo cáo hay chưa. Ngoài việc tiết kiệm thời gian cho các nhà phát triển, việc này còn giúp bạn biết những gì đã được thực hiện để khắc phục vấn đề; có thể vấn đề đó đã được sửa trong bản phát hành tiếp theo, hoặc cần thêm thông tin (trong trường hợp đó, bạn luôn được hoan nghênh cung cấp thông tin nếu có thể!). Để thực hiện việc này, hãy tìm kiếm trong trình theo dõi bằng hộp tìm kiếm ở đầu trang.

Nếu vấn đề bạn đang báo cáo chưa có trong danh sách, hãy đăng nhập vào GitHub. Nếu chưa có tài khoản GitHub, hãy tạo tài khoản mới bằng liên kết "Sign up". Không thể gửi báo cáo lỗi ẩn danh.

Sau khi đăng nhập, bạn có thể gửi một issue. Nhấp vào nút "New issue" trên thanh trên cùng để báo cáo issue mới.

Biểu mẫu gửi có hai trường là "Title" và "Comment".

Trong trường "Title", hãy nhập mô tả *very* ngắn gọn về vấn đề; dưới mười từ là phù hợp.

Trong trường "Comment", hãy mô tả chi tiết vấn đề, bao gồm cả điều bạn mong đợi sẽ xảy ra và điều thực sự đã xảy ra. Hãy nhớ cho biết liệu có module mở rộng nào liên quan hay không, cũng như nền tảng phần cứng và phần mềm bạn đang sử dụng (bao gồm thông tin phiên bản nếu phù hợp).

Mỗi báo cáo issue sẽ được một developer xem xét, người này sẽ xác định cần làm gì để khắc phục vấn đề. Bạn sẽ nhận được thông tin cập nhật mỗi khi có hành động được thực hiện đối với issue.


.. seealso::

   `Cách báo cáo bug hiệu quả <https://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_
      Bài viết trình bày khá chi tiết về cách tạo một báo cáo bug hữu ích. Bài viết mô tả loại thông tin nào hữu ích và tại sao thông tin đó hữu ích.

   `Hướng dẫn viết báo cáo lỗi <https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html>`_
      Thông tin về cách viết một báo cáo lỗi tốt. Một phần nội dung này cụ thể dành cho dự án Mozilla, nhưng cũng mô tả các phương pháp hay nói chung.

.. _contributing-to-python:

Bắt đầu tự mình đóng góp cho Python
===================================

Ngoài việc chỉ báo cáo các lỗi bạn phát hiện, bạn cũng được hoan nghênh gửi các bản vá để sửa chúng. Bạn có thể tìm thêm thông tin về cách bắt đầu viết bản vá cho Python trong `Python Developer's Guide <Python Developer's Guide_>`_. Nếu có câu hỏi, `danh sách thư core-mentorship <core-mentorship mailing list_>`_ là nơi thân thiện để nhận câu trả lời cho mọi câu hỏi liên quan đến quy trình sửa lỗi trong Python.

.. _Documentation bugs: https://github.com/python/cpython/issues?q=is%3Aissue+is%3Aopen+label%3Adocs
.. _Python Developer's Guide: https://devguide.python.org/
.. _core-mentorship mailing list: https://mail.python.org/mailman3/lists/core-mentorship.python.org/

.. _`translation’s repository`: TRANSLATION_REPO_
.. _`Documentation Discourse forum`: https://discuss.python.org/c/documentation/26
.. _`python-doc-theme issue tracker`: https://github.com/python/python-docs-theme
.. _`Issue Tracking`: https://devguide.python.org/tracker/
.. _`Helping with Documentation`: https://devguide.python.org/docquality/#helping-with-documentation
.. _`Documentation Translations`: https://devguide.python.org/documentation/translating/
.. _`How to Report Bugs Effectively`: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
.. _`Bug Writing Guidelines`: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
