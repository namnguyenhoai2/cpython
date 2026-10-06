:mod:`!copy` --- Các thao tác sao chép nông và sao chép sâu
===========================================================

.. module:: copy
   :synopsis: Các thao tác sao chép nông và sao chép sâu.

**Mã nguồn:** :source:`Lib/copy.py`

--------------

Các câu lệnh gán trong Python không sao chép đối tượng mà tạo liên kết giữa một đích và một đối tượng. Đối với các collection có thể thay đổi hoặc chứa các phần tử có thể thay đổi, đôi khi cần tạo một bản sao để có thể thay đổi một bản sao mà không làm thay đổi bản sao còn lại. Mô-đun này cung cấp các thao tác sao chép nông và sao chép sâu tổng quát (được giải thích bên dưới).


Tóm tắt giao diện:

.. function:: copy(obj)

   Trả về một bản sao nông của *obj*.


.. function:: deepcopy(obj[, memo])

   Trả về một bản sao sâu của *obj*.


.. function:: replace(obj, /, **changes)

   Tạo một đối tượng mới cùng kiểu với *obj*, thay thế các trường bằng các giá trị từ *changes*.

   .. versionadded:: 3.13


.. exception:: Error

   Được ném ra cho các lỗi riêng của mô-đun.

.. _shallow_vs_deep_copy:

Sự khác biệt giữa sao chép nông và sao chép sâu chỉ liên quan đến các đối tượng phức hợp (các đối tượng chứa những đối tượng khác, như danh sách hoặc thực thể lớp):

* Một *bản sao nông (shallow copy)* tạo một đối tượng phức hợp mới, sau đó (trong phạm vi có thể) chèn các *tham chiếu* đến những đối tượng có trong đối tượng ban đầu vào đó.

* Một *bản sao sâu (deep copy)* tạo một đối tượng phức hợp mới, sau đó đệ quy chèn các *bản sao* của những đối tượng có trong đối tượng ban đầu vào đó.

Các thao tác sao chép sâu thường có hai vấn đề không xảy ra với thao tác sao chép nông:

* Các đối tượng đệ quy (những đối tượng phức hợp trực tiếp hoặc gián tiếp chứa tham chiếu đến chính chúng) có thể gây ra một vòng lặp đệ quy.

* Vì bản sao sâu sao chép mọi thứ nên nó có thể sao chép quá nhiều, chẳng hạn như dữ liệu vốn được dự định để dùng chung giữa các bản sao.

Hàm :func:`deepcopy` tránh được những vấn đề này bằng cách:

* duy trì một từ điển ``memo`` chứa các đối tượng đã được sao chép trong lần sao chép hiện tại; và

* cho phép các lớp do người dùng định nghĩa ghi đè thao tác sao chép hoặc tập hợp các thành phần được sao chép.

Mô-đun này không sao chép các kiểu như module, method, stack trace, stack frame, file, socket, window hoặc các kiểu tương tự. Mô-đun này vẫn "sao chép" các function và class (cả nông lẫn sâu) bằng cách trả về nguyên trạng đối tượng ban đầu; điều này tương thích với cách mô-đun :mod:`pickle` xử lý chúng.

Có thể tạo bản sao nông của nhiều collection bằng cách sử dụng phương thức tương ứng
:meth:`!copy` (chẳng hạn như :meth:`list.copy`, :meth:`dict.copy` hoặc
:meth:`set.copy`), và đối với các sequence (chẳng hạn như list hoặc bytearray) bằng cách tạo một lát cắt của toàn bộ sequence (``sequence[:]``). Tuy nhiên, các phương thức này và thao tác tạo lát cắt có thể tạo một instance của kiểu cơ sở khi sao chép một instance của lớp con, trong khi :func:`copy.copy` thường trả về một instance cùng kiểu.

.. index:: pair: module; pickle

Các class có thể sử dụng cùng các interface để kiểm soát việc sao chép như khi kiểm soát việc pickling. Xem mô tả về module :mod:`pickle` để biết thông tin về các phương thức này. Trên thực tế, module :mod:`!copy` sử dụng các hàm pickle đã đăng ký từ module :mod:`copyreg`.

.. index::
   single: __copy__() (copy protocol)
   single: __deepcopy__() (copy protocol)

.. currentmodule:: None

Để một class định nghĩa triển khai sao chép của riêng mình, class đó có thể định nghĩa các phương thức đặc biệt :meth:`~object.__copy__` và :meth:`~object.__deepcopy__`.

.. method:: object.__copy__(self)
   :noindexentry:

   Được gọi để triển khai thao tác sao chép nông; không truyền thêm đối số nào.

.. method:: object.__deepcopy__(self, memo)
   :noindexentry:

   Được gọi để triển khai thao tác sao chép sâu; hàm này nhận một đối số là dictionary *memo*. Nếu triển khai ``__deepcopy__`` cần tạo bản sao sâu của một thành phần, nó nên gọi hàm :func:`~copy.deepcopy` với thành phần đó làm đối số đầu tiên và dictionary *memo* làm đối số thứ hai. Dictionary *memo* nên được xem là một đối tượng opaque.


.. index::
   single: __replace__() (replace protocol)

Hàm :func:`!copy.replace` bị giới hạn hơn :func:`~copy.copy` và :func:`~copy.deepcopy`, đồng thời chỉ hỗ trợ named tuple được tạo bởi :func:`~collections.namedtuple`,
:mod:`dataclasses`, và các class khác định nghĩa phương thức :meth:`~object.__replace__`.

.. method:: object.__replace__(self, /, **changes)
   :noindexentry:

   Phương thức này sẽ tạo một đối tượng mới cùng kiểu, thay thế các trường bằng các giá trị từ *changes*.

   .. versionadded:: 3.13


.. seealso::

   Mô-đun :mod:`pickle`
      Thảo luận về các phương thức đặc biệt được sử dụng để hỗ trợ việc truy xuất và khôi phục trạng thái đối tượng.

