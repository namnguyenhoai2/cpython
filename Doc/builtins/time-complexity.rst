.. _time-complexity:

=============================================================
Độ phức tạp thời gian của các thao tác trên các kiểu dựng sẵn
=============================================================

Trang này ghi lại độ phức tạp thời gian của nhiều thao tác trên các kiểu dựng sẵn trong CPython. Các triển khai Python khác có thể có đặc tính hiệu năng khác. Ngoài ra, các chi phí được liệt kê giả định các kiểu dựng sẵn chính xác, vì các thực thể của lớp con có thể có chi phí khác.

Chúng tôi sử dụng |big O notation|_ để mô tả thời gian chạy của một thao tác tăng như thế nào theo kích thước đầu vào. Nếu không có nêu khác, *n* biểu thị số phần tử hiện có trong container, còn *k* là giá trị của một tham số số, chẳng hạn như chỉ mục hoặc số lần lặp.

.. |big O notation| replace:: Ký hiệu Big *O*
.. _big O notation: https://en.wikipedia.org/wiki/Big_O_notation


:class:`!list`
==============

List là các sequence có thể thay đổi; để biết thêm chi tiết về quá trình triển khai, hãy xem
:ref:`how-are-lists-implemented`. Các chi phí lớn nhất phát sinh khi mở rộng vượt quá kích thước cấp phát hiện tại (vì mọi thứ phải được di chuyển), hoặc khi chèn hay xóa ở vị trí gần đầu (vì mọi thứ phía sau vị trí đó phải được di chuyển). Nếu bạn cần thêm hoặc xóa ở cả hai đầu, hãy cân nhắc sử dụng một
:class:`collections.deque` thay thế.

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - Sao chép (``l.copy()``)
     - *O*\ (*n*)
   * - Thêm (``l.append(x)``) [1]_
     - *O*\ (1)
   * - Lấy ra (``l.pop(k)``) [1]_ [2]_
     - *O*\ (*n* - *k*)
   * - Chèn (``l.insert(k, x)``) [1]_ [2]_
     - *O*\ (*n* - *k*)
   * - Lấy mục (``l[k]``)
     - *O*\ (1)
   * - Đặt mục (``l[k] = x``)
     - *O*\ (1)
   * - Xóa phần tử (``del l[k]``) [2]_
     - *O*\ (*n* - *k*)
   * - Lặp
     - *O*\ (*n*)
   * - Lấy slice (``l[i:j]``)
     - *O*\ (*j* - *i*)
   * - Gán slice (``l[i:j] = t``) [1]_
     - *O*\ (*j* - *i*) nếu len(*t*) == *j* - *i*, nếu không thì *O*\ (*n* - *i* + len(*t*) )
   * - Xóa slice (``del l[i:j]``)
     - *O*\ (*n* - *i*)
   * - Mở rộng (``l.extend(t)``) [1]_ [3]_
     - *O*\ (len(*t*))
   * - Sắp xếp (``l.sort()``) [4]_
     - *O*\ (*n* log *n*)
   * - Nối (``l1 + l2``)
     - *O*\ (len(*l1*) + len(*l2*))
   * - Nhân (``l * k``)
     - *O*\ (*nk*)
   * - ``x in l``
     - *O*\ (*n*)
   * - ``min(l)``, ``max(l)``
     - *O*\ (*n*)
   * - Lấy độ dài (``len(l)``) [5]_
     - *O*\ (1)


:class:`!tuple`
===============

Một :class:`tuple` là một chuỗi :term:`immutable`. Vì tuple không bao giờ thay đổi, nên không có chi phí chèn hoặc xóa, và việc tạo bản sao chỉ trả về cùng một đối tượng, do đó có thời gian hằng số (*O*\ (1)).

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - Sao chép (``tuple(t)``)
     - *O*\ (1)
   * - Lấy phần tử (``t[k]``)
     - *O*\ (1)
   * - Lấy lát cắt (``t[i:j]``)
     - *O*\ (*j* - *i*)
   * - Nối (``t1 + t2``)
     - *O*\ (len(*t1*) + len(*t2*))
   * - Nhân (``t * k``)
     - *O*\ (*nk*)
   * - Lặp
     - *O*\ (*n*)
   * - ``x in t``
     - *O*\ (*n*)
   * - ``min(t)``, ``max(t)``
     - *O*\ (*n*)
   * - Lấy độ dài (``len(t)``) [5]_
     - *O*\ (1)


:class:`!dict`
==============

Các thời gian được liệt kê cho các đối tượng dict là thời gian trong trường hợp trung bình, vì chúng giả định rằng hàm băm của các đối tượng đủ mạnh để khiến các vụ va chạm xảy ra không thường xuyên. Chúng cũng giả định rằng các khóa được phân bổ đồng đều trong tập hợp các khóa khả dĩ. Trong trường hợp xấu nhất, khi mọi khóa đều được băm thành cùng một giá trị, mỗi thao tác *O*\ (1) dưới đây thay vào đó sẽ mất thời gian *O*\ (*n*). Chúng cũng giả định rằng việc băm và so sánh một khóa có độ phức tạp *O*\ (1). Để biết thêm chi tiết về cách triển khai, hãy xem :ref:`how-are-dictionaries-implemented`.

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - ``key in d``
     - *O*\ (1)
   * - Sao chép (``d.copy()``) [7]_
     - *O*\ (*n*)
   * - Lấy phần tử (``d[key]``, ``d.get(key)``)
     - *O*\ (1)
   * - Đặt mục (``d[key] = value``) [1]_
     - *O*\ (1)
   * - Xóa mục (``del d[key]``, ``d.pop(key)``)
     - *O*\ (1)
   * - Cập nhật (``d.update(t)``, ``d |= t``) [1]_ [3]_ [7]_
     - *O*\ (len(*t*))
   * - Lặp lại [7]_
     - *O*\ (*n*)
   * - Lấy độ dài (``len(d)``) [5]_
     - *O*\ (1)


:class:`!set`, :class:`!frozenset`
==================================

Xem :class:`dict` vì các cài đặt :class:`set` và :class:`frozenset` tương tự, và các điểm cần lưu ý cũng giống nhau. Trong trường hợp xấu nhất, các thao tác *O*\ (1) thay vào đó mất *O*\ (*n*) thời gian, và các thao tác tra cứu mọi phần tử cũng suy giảm tương ứng.

Một :class:`frozenset` là :term:`immutable`, vì vậy nó không hỗ trợ các thao tác thêm, loại bỏ hoặc cập nhật tại chỗ. Các thao tác còn lại bên dưới áp dụng cho nó với cùng chi phí.

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - ``x in s``
     - *O*\ (1)
   * - Sao chép (``s.copy()``) [6]_ [7]_
     - *O*\ (*n*)
   * - Thêm (``s.add(x)``) [1]_
     - *O*\ (1)
   * - Loại bỏ (``s.discard(x)``, ``s.remove(x)``)
     - *O*\ (1)
   * - Phép hợp (``s1 | s2``, ``s1.union(s2)``) [7]_
     - *O*\ (len(*s1*) + len(*s2*))
   * - Cập nhật (``s1 |= s2``, ``s1.update(s2)``) [1]_ [7]_
     - *O*\ (len(*s2*))
   * - Phép giao (``s1 & s2``, ``s1.intersection(s2)``) [7]_ [8]_
     - *O*\ (min(len(*s1*), len(*s2*)))
   * - Cập nhật phép giao (``s1 &= s2``, ``s1.intersection_update(s2)``) [1]_ [7]_ [8]_
     - *O*\ (min(len(*s1*), len(*s2*)))
   * - Hiệu (``s1 - s2``, ``s1.difference(s2)``) [7]_ [9]_
     - *O*\ (len(*s1*))
   * - Cập nhật hiệu (``s1 -= s2``, ``s1.difference_update(s2)``) [1]_ [7]_ [8]_
     - *O*\ (min(len(*s1*), len(*s2*)))
   * - Hiệu đối xứng (``s1 ^ s2``, ``s1.symmetric_difference(s2)``) [7]_
     - *O*\ (len(*s1*) + len(*s2*))
   * - Cập nhật hiệu đối xứng (``s1 ^= s2``, ``s1.symmetric_difference_update(s2)``) [1]_ [7]_
     - *O*\ (len(*s2*))
   * - Lấy độ dài (``len(s)``) [5]_
     - *O*\ (1)


:class:`!str`, :class:`!bytes`, :class:`!bytearray`
===================================================

Các đối tượng :class:`str` và :class:`bytes` lần lượt là các chuỗi ký tự và byte bất biến. Tương tự như tuple, việc sao chép một đối tượng sẽ trả về chính đối tượng ban đầu. Một :class:`bytearray` có thể thay đổi, đồng thời hỗ trợ các thao tác biến đổi của :class:`list` (ngoại trừ :meth:`!sort`), với cùng chi phí. Tuy nhiên, việc xóa ở đầu bằng ``del`` (``del b[0]``, ``del b[:k]``) chỉ tiến vị trí bắt đầu của bộ đệm thay vì di chuyển các byte còn lại, và có chi phí trung bình *O*\ (1).

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - Lấy phần tử (``s[k]``)
     - *O*\ (1)
   * - Lấy lát cắt (``s[i:j]``)
     - *O*\ (*j* - *i*)
   * - Nối (``s + t``) [10]_
     - *O*\ (len(*s*) + len(*t*))
   * - Nhân (``s * k``)
     - *O*\ (*nk*)
   * - Tìm kiếm chuỗi con (``x in s``, ``s.find(x)``, ``s.index(x)``) [11]_
     - *O*\ (*n*)
   * - Tìm kiếm chuỗi con ngược (``s.rfind(x)``, ``s.rindex(x)``) [11]_ [12]_
     - *O*\ (*n* × len(*x*))
   * - Mã hóa hoặc giải mã [13]_
     - *O*\ (*n*)
   * - Phép lặp
     - *O*\ (*n*)
   * - Lấy độ dài (``len(s)``) [5]_
     - *O*\ (1)


:class:`!memoryview`
====================

Các đối tượng :class:`memoryview` cho phép mã Python truy cập dữ liệu nội bộ của một đối tượng hỗ trợ :ref:`buffer protocol <bufferobjects>` mà không cần sao chép. Cụ thể, việc cắt một memory view sẽ trả về một view mới trên cùng bộ đệm.

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - Tạo (``memoryview(obj)``)
     - *O*\ (1)
   * - Lấy mục (``v[k]``)
     - *O*\ (1)
   * - Lấy slice (``v[i:j]``)
     - *O*\ (1)
   * - Chỉ mục (``v.index(x)``) [11]_ [14]_
     - *O*\ (*n*)
   * - Đếm (``v.count(x)``) [14]_
     - *O*\ (*n*)
   * - Chuyển đổi thành bytes (``v.tobytes()``, ``bytes(v)``)
     - *O*\ (*n*)
   * - Lấy độ dài (``len(v)``) [5]_
     - *O*\ (1)


:class:`!range`
===============

Đối tượng :class:`range` tính toán các phần tử của nó theo yêu cầu từ các giá trị *start*, *stop* và *step*, vì vậy hầu hết các thao tác không phụ thuộc vào độ dài của range.

.. list-table::
   :header-rows: 1

   * - Thao tác
     - Độ phức tạp
   * - Lấy phần tử (``r[k]``)
     - *O*\ (1)
   * - Lấy lát cắt (``r[i:j]``)
     - *O*\ (1)
   * - ``x in r`` [15]_
     - *O*\ (1)
   * - Lập chỉ mục và đếm (``r.index(x)``, ``r.count(x)``) [15]_
     - *O*\ (1)
   * - Lặp lại
     - *O*\ (*n*)
   * - ``min(r)``, ``max(r)``
     - *O*\ (*n*)
   * - Lấy độ dài (``len(r)``) [5]_
     - *O*\ (1)


Ghi chú
=======

.. [1] Tính trung bình. Một thao tác riêng lẻ đôi khi có thể là *O*\ (*n*) khi bộ nhớ lưu trữ bên dưới được thay đổi kích thước, nhưng chi phí này được phân bổ cho nhiều thao tác, tùy thuộc vào lịch sử của container.

.. [2] Việc lấy ra hoặc xóa phần tử tại chỉ mục *k* của một danh sách có kích thước *n* sẽ dịch chuyển tất cả phần tử sau *k* sang trái một vị trí, di chuyển *n* - *k* - 1 phần tử; việc chèn tại chỉ mục *k* sẽ dịch chuyển các phần tử từ *k* trở đi sang phải một vị trí, di chuyển *n* - *k* phần tử. Trường hợp xấu nhất là chỉ mục 0, khi toàn bộ phần còn lại của danh sách phải được di chuyển; trường hợp trung bình, với một chỉ mục ở giữa danh sách, cần *O*\ (*n*/2) = *O*\ (*n*) thao tác; còn thao tác ở cuối danh sách không di chuyển gì và có độ phức tạp *O*\ (1).

.. [3] Cộng thêm chi phí duyệt qua *t*, việc này có thể tốn kém đối với một iterable bất kỳ.

.. [4] Đây là trường hợp xấu nhất. Việc sắp xếp có tính thích ứng, và dữ liệu đầu vào đã được sắp xếp hoặc sắp xếp theo thứ tự ngược chỉ cần *O*\ (*n*) phép so sánh. Xem :source:`Objects/listsort.txt` để biết thêm thông tin.

.. [5] Số lượng phần tử được lưu trong đối tượng, vì vậy ``len()`` không cần đếm chúng.

.. [6] Việc sao chép một :class:`frozenset` có độ phức tạp *O*\ (1), vì nó trả về đối tượng ban đầu.

.. [7] Các thao tác này quét bảng băm nội bộ của container, bảng này không được thu nhỏ khi các phần tử bị xóa. Sau khi xóa hầu hết các phần tử, chúng vẫn mất thời gian tỷ lệ thuận với kích thước trước đây của container, cho đến khi một lần chèn sau đó kích hoạt việc thay đổi kích thước.

.. [8] *O*\ (len(*t*)) nếu *t* không phải là set.

.. [9] *O*\ (len(*s*) + len(*t*)) nếu *t* không phải là set.

.. [10] Mỗi phép nối tạo ra một đối tượng mới, vì vậy việc xây dựng một chuỗi bằng cách nối nhiều phần trong một vòng lặp có độ phức tạp bậc hai theo tổng độ dài. Xem :ref:`ghi chú về việc nối các sequence bất biến <typesseq-repeated-concatenation>` để biết các phương án thay thế.

.. [11] Với các đối số *start* và *end*, *n* là độ dài của vùng được tìm kiếm thay vì độ dài của *s*, và không có gì được sao chép, không giống như khi slicing.

.. [12] Đây là trường hợp xấu nhất. Với dữ liệu đầu vào thông thường, việc tìm kiếm ngược là *O*\ (*n*). Ngược lại, việc tìm kiếm xuôi sử dụng một thuật toán phức tạp hơn với trường hợp xấu nhất có độ phức tạp tuyến tính, được mô tả trong
   :source:`Objects/stringlib/stringlib_find_two_way_notes.txt`.

.. [13] Điều này giả định một codec thực hiện một lượng công việc không đổi cho mỗi ký tự.

.. [14] Các phương thức này giải nén và so sánh từng phần tử riêng lẻ, vì vậy chúng chậm hơn nhiều so với các phương thức :class:`bytes` tương đương.

.. [15] Giả sử các đối số :class:`int` hoặc :class:`bool`. Với các kiểu khác, phạm vi được tìm kiếm như mọi sequence khác trong thời gian *O*\ (*n*).
