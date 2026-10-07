.. _email-examples:

:mod:`email`: Ví dụ
-------------------

Dưới đây là một vài ví dụ về cách sử dụng package :mod:`email` để đọc, ghi và gửi các email đơn giản, cũng như các message MIME phức tạp hơn.

Trước tiên, hãy xem cách tạo và gửi một message văn bản đơn giản (cả nội dung văn bản và địa chỉ đều có thể chứa các ký tự Unicode):

.. literalinclude:: ../includes/email-simple.py


Bạn có thể dễ dàng phân tích các header :rfc:`822` bằng cách sử dụng các class từ module :mod:`~email.parser`:

.. literalinclude:: ../includes/email-headers.py


Dưới đây là một ví dụ về cách gửi một message MIME chứa nhiều ảnh gia đình có thể đang nằm trong một thư mục:

.. literalinclude:: ../includes/email-mime.py


Dưới đây là một ví dụ về cách gửi toàn bộ nội dung của một thư mục dưới dạng email: [1]_

.. literalinclude:: ../includes/email-dir.py


Dưới đây là một ví dụ về cách giải nén một message MIME như message ở trên thành một thư mục chứa các tệp:

.. literalinclude:: ../includes/email-unpack.py


Dưới đây là một ví dụ về cách tạo một thư HTML với phiên bản văn bản thuần thay thế. Để nội dung thú vị hơn một chút, chúng ta đưa một hình ảnh liên quan vào phần HTML và lưu một bản sao của nội dung sắp gửi vào đĩa, đồng thời gửi nó đi.

.. literalinclude:: ../includes/email-alternative.py


Nếu chúng ta nhận được thư từ ví dụ trước, đây là một cách để xử lý thư đó:

.. literalinclude:: ../includes/email-read-alternative.py

Cho đến lời nhắc, đầu ra từ ví dụ trên là:

.. code-block:: none

    To: Penelope Pussycat <penelope@example.com>, Fabrette Pussycat <fabrette@example.com>
    From: Pepé Le Pew <pepe@example.com>
    Subject: Pourquoi pas des asperges pour ce midi ?

    Salut!

    Cette recette [1] sera sûrement un très bon repas.


.. rubric:: Chú thích cuối trang

.. [1] Xin cảm ơn Matthew Dixon Cowles vì nguồn cảm hứng và các ví dụ ban đầu.
