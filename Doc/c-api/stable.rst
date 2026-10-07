.. highlight:: c

.. _stable:

**********************
Tính ổn định của C API
**********************

Trừ khi có tài liệu nêu rõ khác đi, C API của Python được điều chỉnh bởi Chính sách tương thích ngược, :pep:`387`. Hầu hết các thay đổi đều tương thích với mã nguồn (thường chỉ bằng cách bổ sung API mới). Việc thay đổi API hiện có hoặc loại bỏ API chỉ được thực hiện sau một khoảng thời gian ngừng sử dụng hoặc để khắc phục các vấn đề nghiêm trọng.

Giao diện nhị phân ứng dụng (ABI) của CPython tương thích thuận và ngược giữa các bản phát hành phụ (nếu chúng được biên dịch theo cùng một cách; xem :ref:`stable-abi-platform` bên dưới). Vì vậy, mã được biên dịch cho Python 3.10.0 sẽ hoạt động trên 3.10.8 và ngược lại, nhưng sẽ cần được biên dịch riêng cho 3.9.x và 3.11.x.

Có hai cấp độ C API với các kỳ vọng khác nhau về tính ổn định:

- :ref:`Unstable API <unstable-c-api>` có thể thay đổi trong các phiên bản phụ mà không cần qua khoảng thời gian ngừng sử dụng. API này được đánh dấu bằng tiền tố ``PyUnstable`` trong tên.
- :ref:`Limited API <limited-c-api>` tương thích giữa một số bản phát hành phụ. Khi :c:macro:`Py_LIMITED_API` được định nghĩa, chỉ tập hợp con này được cung cấp từ ``Python.h``.

Các cấp độ này được thảo luận chi tiết hơn bên dưới.

Các tên có tiền tố dấu gạch dưới, chẳng hạn như ``_Py_InternalState``, là private API có thể thay đổi mà không báo trước, ngay cả trong các bản phát hành vá lỗi. Nếu bạn cần sử dụng API này, hãy cân nhắc liên hệ với `các nhà phát triển CPython <https://discuss.python.org/c/core-dev/c-api/30>`_ để thảo luận về việc bổ sung public API cho trường hợp sử dụng của bạn.

.. _unstable-c-api:

C API không ổn định
===================

.. index:: single: PyUnstable

Bất kỳ API nào có tên với tiền tố ``PyUnstable`` đều cung cấp các chi tiết triển khai của CPython và có thể thay đổi trong mọi bản phát hành phụ (ví dụ: từ 3.9 lên 3.10) mà không có bất kỳ cảnh báo ngừng sử dụng nào. Tuy nhiên, API này sẽ không thay đổi trong bản phát hành sửa lỗi (ví dụ: từ 3.10.0 lên 3.10.1).

API này nhìn chung предназнач cho các công cụ chuyên biệt, cấp thấp như trình gỡ lỗi.

Các dự án sử dụng API này được kỳ vọng sẽ theo dõi quá trình phát triển CPython và dành thêm công sức để điều chỉnh theo các thay đổi.

.. _stable-application-binary-interface:

Giao diện nhị phân ứng dụng ổn định
===================================

Để đơn giản, tài liệu này nói về *các extension*, nhưng Limited API và Stable ABI hoạt động theo cùng một cách đối với mọi trường hợp sử dụng API — ví dụ như nhúng Python.

.. _limited-c-api:

Limited C API
-------------

Python 3.2 đã giới thiệu *Limited API*, một tập con của C API của Python. Các extension chỉ sử dụng Limited API có thể được biên dịch một lần và nạp trên nhiều phiên bản Python. Nội dung của Limited API được :ref:`liệt kê bên dưới <limited-api-list>`.

.. c:macro:: Py_LIMITED_API

   Định nghĩa macro này trước khi include ``Python.h`` để chỉ sử dụng Limited API và chọn phiên bản Limited API.

   Định nghĩa ``Py_LIMITED_API`` thành giá trị của :c:macro:`PY_VERSION_HEX` tương ứng với phiên bản Python thấp nhất mà extension của bạn hỗ trợ. Extension sẽ tương thích ABI với mọi bản phát hành Python 3 kể từ phiên bản được chỉ định trở đi và có thể sử dụng Limited API được giới thiệu tối đa ở phiên bản đó.

   Thay vì sử dụng trực tiếp macro ``PY_VERSION_HEX``, hãy hardcode một minor version tối thiểu (ví dụ: ``0x030A0000`` cho Python 3.10) để đảm bảo tính ổn định khi biên dịch với các phiên bản Python trong tương lai.

   Bạn cũng có thể định nghĩa ``Py_LIMITED_API`` thành ``3``. Cách này hoạt động giống như ``0x03020000`` (Python 3.2, phiên bản đã giới thiệu Limited API).


.. _stable-abi:

Stable ABI
----------

Để bật tính năng này, Python cung cấp một *Stable ABI*: một tập hợp các symbol sẽ duy trì khả năng tương thích ABI giữa các phiên bản Python 3.x.

.. note::

   Stable ABI ngăn ngừa các vấn đề về ABI, chẳng hạn như lỗi linker do thiếu symbol hoặc hỏng dữ liệu do thay đổi bố cục cấu trúc hay chữ ký hàm. Tuy nhiên, những thay đổi khác trong Python có thể làm thay đổi *hành vi* của các extension. Xem Chính sách Tương thích Ngược của Python (:pep:`387`) để biết chi tiết.

Stable ABI chứa các symbol được cung cấp trong :ref:`Limited API <limited-c-api>`, nhưng cũng có những symbol khác – chẳng hạn như các hàm cần thiết để hỗ trợ những phiên bản cũ hơn của Limited API.

Trên Windows, các extension sử dụng Stable ABI nên được liên kết với ``python3.dll`` thay vì một thư viện dành riêng cho từng phiên bản như ``python39.dll``.

Trên một số nền tảng, Python sẽ tìm và tải các tệp thư viện dùng chung có tên kèm theo thẻ ``abi3`` (ví dụ: ``mymodule.abi3.so``). Python không kiểm tra xem các extension đó có tuân theo Stable ABI hay không. Người dùng (hoặc các công cụ đóng gói của họ) cần đảm bảo rằng, chẳng hạn, các extension được xây dựng với Limited API 3.10 trở lên không được cài đặt cho các phiên bản Python thấp hơn.

Tất cả các hàm trong Stable ABI đều hiện diện dưới dạng hàm trong thư viện dùng chung của Python, không chỉ dưới dạng macro. Nhờ đó, chúng có thể được sử dụng từ các ngôn ngữ không dùng bộ tiền xử lý C.


Phạm vi và hiệu năng của Limited API
------------------------------------

Mục tiêu của Limited API là cho phép mọi thứ có thể thực hiện bằng C API đầy đủ, nhưng có thể phải chịu mức suy giảm hiệu năng.

Ví dụ, mặc dù :c:func:`PyList_GetItem` khả dụng, biến thể macro “unsafe” :c:func:`PyList_GET_ITEM` lại không khả dụng. Macro này có thể nhanh hơn vì nó có thể dựa vào các chi tiết triển khai dành riêng cho từng phiên bản của đối tượng list.

Khi không định nghĩa ``Py_LIMITED_API``, một số hàm C API được inline hoặc thay thế bằng macro. Việc định nghĩa ``Py_LIMITED_API`` sẽ tắt quá trình inline này, giúp duy trì tính ổn định khi các cấu trúc dữ liệu của Python được cải thiện, nhưng có thể làm giảm hiệu năng.

Bằng cách bỏ qua định nghĩa ``Py_LIMITED_API``, bạn có thể biên dịch một extension Limited API với ABI dành riêng cho từng phiên bản. Điều này có thể cải thiện hiệu năng cho phiên bản Python đó, nhưng sẽ hạn chế khả năng tương thích. Khi đó, việc biên dịch với ``Py_LIMITED_API`` sẽ tạo ra một extension có thể được phân phối ở những nơi không có extension dành riêng cho từng phiên bản — chẳng hạn như các bản phát hành trước của một phiên bản Python sắp ra mắt.


Các điểm cần lưu ý về Limited API
---------------------------------

Lưu ý rằng việc biên dịch với ``Py_LIMITED_API`` *không* phải là một bảo đảm hoàn toàn rằng mã tuân theo :ref:`Limited API <limited-c-api>` hoặc :ref:`Stable ABI <stable-abi>`. ``Py_LIMITED_API`` chỉ bao quát các định nghĩa, nhưng một API còn bao gồm những vấn đề khác, chẳng hạn như ngữ nghĩa được mong đợi.

Một vấn đề mà ``Py_LIMITED_API`` không ngăn chặn được là gọi một hàm với các đối số không hợp lệ trong một phiên bản Python thấp hơn. Ví dụ, hãy xét một hàm bắt đầu chấp nhận ``NULL`` cho một đối số. Trong Python 3.9, ``NULL`` giờ đây chọn hành vi mặc định, nhưng trong Python 3.8, đối số sẽ được sử dụng trực tiếp, gây ra thao tác dereference ``NULL`` và làm chương trình bị crash. Lập luận tương tự cũng áp dụng cho các trường của struct.

Một vấn đề khác là hiện tại một số trường của struct không bị ẩn khi ``Py_LIMITED_API`` được định nghĩa, mặc dù chúng là một phần của Limited API.

Vì những lý do này, chúng tôi khuyến nghị kiểm thử một extension với *all* phiên bản Python nhỏ mà extension đó hỗ trợ, và tốt nhất là build với phiên bản *lowest* như vậy.

Chúng tôi cũng khuyến nghị xem lại tài liệu của tất cả API được sử dụng để kiểm tra xem chúng có được xác định rõ ràng là một phần của Limited API hay không. Ngay cả khi ``Py_LIMITED_API`` được định nghĩa, một số khai báo private vẫn được exposed vì lý do kỹ thuật (hoặc thậm chí là vô tình, do lỗi).

Cũng lưu ý rằng Limited API không nhất thiết ổn định: biên dịch với ``Py_LIMITED_API`` trên Python 3.8 có nghĩa là extension sẽ chạy được với Python 3.12, nhưng không nhất thiết sẽ *compile* với Python 3.12. Cụ thể, một số phần của Limited API có thể bị đánh dấu deprecated và bị xóa, miễn là Stable ABI vẫn ổn định.


.. _stable-abi-platform:

Các cân nhắc về nền tảng
========================

Độ ổn định của ABI không chỉ phụ thuộc vào Python mà còn phụ thuộc vào compiler được sử dụng, các thư viện cấp thấp hơn và các tùy chọn của compiler. Đối với :ref:`Stable ABI <stable-abi>`, những chi tiết này xác định một “platform”. Chúng thường phụ thuộc vào loại OS và kiến trúc bộ xử lý

Mỗi nhà phân phối Python cụ thể có trách nhiệm đảm bảo rằng tất cả phiên bản Python trên một platform cụ thể đều được build theo cách không làm hỏng Stable ABI. Đây là trường hợp đối với các bản phát hành Windows và macOS từ ``python.org`` cũng như nhiều nhà phân phối bên thứ ba.


.. _limited-api-list:

Nội dung của Limited API
========================


Hiện tại, :ref:`Limited API <limited-c-api>` bao gồm các mục sau:

.. limited-api-list::

.. _`CPython developers`: https://discuss.python.org/c/core-dev/c-api/30
