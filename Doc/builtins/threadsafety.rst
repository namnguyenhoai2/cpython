.. _threadsafety:

*********************
Đảm bảo an toàn luồng
*********************

Trang này ghi lại các đảm bảo về an toàn luồng cho những kiểu dựng sẵn trong bản dựng free-threaded của Python. Các đảm bảo được mô tả ở đây áp dụng khi sử dụng Python với :term:`GIL` bị vô hiệu hóa (chế độ free-threaded). Khi GIL được bật, hầu hết các thao tác được tuần tự hóa một cách ngầm định.

Để biết hướng dẫn chung về cách viết mã an toàn luồng trong Python free-threaded, hãy xem
:ref:`freethreading-python-howto`.


.. _threadsafety-levels:

Các cấp độ an toàn luồng
========================

Tài liệu C API sử dụng các cấp độ sau để mô tả những đảm bảo về an toàn luồng của từng hàm. Các cấp độ được liệt kê từ ít an toàn nhất đến an toàn nhất.

.. _threadsafety-level-incompatible:

Không tương thích
-----------------

Một hàm hoặc thao tác không thể được làm cho an toàn khi sử dụng đồng thời, ngay cả khi có cơ chế đồng bộ hóa bên ngoài. Mã không tương thích thường truy cập trạng thái toàn cục theo cách không được đồng bộ hóa và chỉ được phép gọi từ một luồng duy nhất trong suốt vòng đời của chương trình.

Ví dụ: một hàm sửa đổi trạng thái trên toàn bộ tiến trình, chẳng hạn như các trình xử lý tín hiệu hoặc biến môi trường, trong đó các lệnh gọi đồng thời từ bất kỳ thread nào, ngay cả khi có cơ chế khóa bên ngoài, cũng có thể xung đột với runtime hoặc các thư viện khác.

.. _threadsafety-level-compatible:

Tương thích
-----------

Một hàm hoặc thao tác an toàn khi được gọi từ nhiều thread *provided* bên gọi cung cấp cơ chế đồng bộ hóa bên ngoài phù hợp, chẳng hạn như giữ một :term:`lock` trong suốt thời gian của mỗi lần gọi. Nếu không có cơ chế đồng bộ hóa như vậy, các lệnh gọi đồng thời có thể gây ra :term:`race conditions <race condition>` hoặc :term:`data races <data race>`.

Ví dụ: một hàm đọc từ hoặc ghi vào một đối tượng mà trạng thái bên trong không được bảo vệ bằng khóa. Bên gọi phải đảm bảo rằng không có hai thread nào truy cập cùng một đối tượng tại cùng một thời điểm.

.. _threadsafety-level-distinct:

An toàn trên các đối tượng khác nhau
------------------------------------

Một hàm hoặc thao tác an toàn khi được gọi từ nhiều thread mà không cần đồng bộ hóa bên ngoài, miễn là mỗi thread thao tác trên một đối tượng **different**. Hai thread có thể gọi hàm cùng lúc, nhưng không được truyền cùng một đối tượng (hoặc các đối tượng dùng chung trạng thái nền tảng) làm đối số.

Ví dụ: một hàm sửa đổi các trường của một struct bằng các thao tác ghi không nguyên tử. Hai thread có thể gọi hàm một cách an toàn trên từng instance struct riêng của mình, nhưng các lệnh gọi đồng thời trên cùng một instance *same* yêu cầu đồng bộ hóa bên ngoài.

.. _threadsafety-level-shared:

An toàn khi dùng trên các đối tượng dùng chung
----------------------------------------------

Một hàm hoặc thao tác an toàn khi được sử dụng đồng thời trên cùng một đối tượng **same**. Phần triển khai sử dụng cơ chế đồng bộ hóa nội bộ (chẳng hạn như
:term:`khóa riêng cho từng đối tượng <per-object lock>` hoặc
:ref:`đoạn găng <python-critical-section-api>`) để bảo vệ trạng thái có thể thay đổi dùng chung, vì vậy bên gọi không cần tự cung cấp cơ chế khóa.

Ví dụ: :c:func:`PyList_GetItemRef` có thể được gọi từ nhiều thread trên cùng một :c:type:`PyListObject` - nó sử dụng cơ chế đồng bộ hóa nội bộ để tuần tự hóa quyền truy cập.

.. _threadsafety-level-atomic:

Atomic
------

Một hàm hoặc thao tác có vẻ :term:`atomic <atomic operation>` đối với các thread khác - nó thực thi tức thời theo góc nhìn của các thread khác. Đây là dạng mạnh nhất của tính an toàn luồng.

Ví dụ: :c:func:`PyMutex_IsLocked` thực hiện việc đọc trạng thái mutex theo cách nguyên tử và có thể được gọi từ bất kỳ thread nào vào bất kỳ lúc nào.


.. _thread-safety-list:

Tính an toàn luồng đối với các đối tượng list
=============================================

Việc đọc một phần tử đơn lẻ từ một :class:`list` là
:term:`nguyên tử <atomic operation>`:

.. code-block::
   :class: good

   lst[i]   # list.__getitem__

Các phương thức sau duyệt qua list và sử dụng thao tác đọc :term:`nguyên tử <atomic operation>` của từng mục để thực hiện chức năng. Điều đó có nghĩa là chúng có thể trả về kết quả bị ảnh hưởng bởi các thay đổi đồng thời:

.. code-block::
   :class: maybe

   item in lst
   lst.index(item)
   lst.count(item)

Tất cả các thao tác trên đều tránh việc lấy :term:`khóa trên từng đối tượng <per-object lock>`. Chúng không chặn các thay đổi đồng thời. Các thao tác khác đang giữ khóa sẽ không ngăn chúng quan sát các trạng thái trung gian.

Tất cả các thao tác khác từ đây trở đi đều chặn bằng cách sử dụng :term:`per-object lock`.

Việc ghi một phần tử duy nhất bằng ``lst[i] = x`` là an toàn khi được gọi từ nhiều luồng và sẽ không làm hỏng danh sách.

Các thao tác sau đây trả về các đối tượng mới và có vẻ
:term:`nguyên tử <atomic operation>` đối với các luồng khác:

.. code-block::
   :class: good

   lst1 + lst2    # nối hai danh sách thành một danh sách mới
   x * lst        # lặp lst x lần vào một danh sách mới
   lst.copy()     # trả về một bản sao nông của danh sách

Các phương thức sau đây chỉ hoạt động trên một phần tử duy nhất và không cần dịch chuyển cũng :term:`nguyên tử <atomic operation>`:

.. code-block::
   :class: good

   lst.append(x)  # thêm vào cuối danh sách, không cần dịch chuyển
   lst.pop()      # lấy phần tử khỏi cuối danh sách, không cần dịch chuyển

Phương thức :meth:`~list.clear` cũng :term:`mang tính nguyên tử <atomic operation>`. Các luồng khác không thể quan sát các phần tử đang bị xóa.

Phương thức :meth:`~list.sort` không :term:`mang tính nguyên tử <atomic operation>`. Các luồng khác không thể quan sát các trạng thái trung gian trong khi sắp xếp, nhưng danh sách có vẻ trống trong suốt thời gian sắp xếp.

Các thao tác sau có thể cho phép các thao tác :term:`lock-free` quan sát các trạng thái trung gian vì chúng sửa đổi nhiều phần tử tại chỗ:

.. code-block::
   :class: maybe

   lst.insert(idx, item)  # dịch chuyển các phần tử
   lst.pop(idx)           # idx không ở cuối danh sách, dịch chuyển các phần tử
   lst *= x               # sao chép các phần tử tại chỗ

Phương thức :meth:`~list.remove` có thể cho phép sửa đổi đồng thời vì việc so sánh phần tử có thể thực thi mã Python tùy ý (thông qua
:meth:`~object.__eq__`).

:meth:`~list.extend` an toàn khi được gọi từ nhiều thread. Tuy nhiên, các đảm bảo của nó phụ thuộc vào iterable được truyền vào. Nếu đó là một :class:`list`, một
:class:`tuple`, một :class:`set`, một :class:`frozenset`, một :class:`dict` hoặc một
:ref:`đối tượng dạng xem dictionary <dict-views>` (nhưng không phải các lớp con của chúng), thao tác ``extend`` an toàn trước các sửa đổi đồng thời đối với iterable. Nếu không, một iterator sẽ được tạo và có thể bị thread khác sửa đổi đồng thời. Điều tương tự cũng áp dụng cho phép nối tại chỗ một list với các iterable khác khi sử dụng ``lst += iterable``.

Tương tự, việc gán cho một lát cắt của list bằng ``lst[i:j] = iterable`` là an toàn khi được gọi từ nhiều thread, nhưng ``iterable`` chỉ được khóa khi nó cũng là một :class:`list` (nhưng không phải các lớp con của nó).

Các thao tác bao gồm nhiều lần truy cập, cũng như việc lặp, không bao giờ mang tính nguyên tử. Ví dụ:

.. code-block::
   :class: bad

   # KHÔNG nguyên tử: đọc-sửa-ghi
   lst[i] = lst[i] + 1

   # KHÔNG nguyên tử: kiểm tra-rồi-hành động
   if lst:
       item = lst.pop()

   # KHÔNG an toàn luồng: lặp trong khi sửa đổi
   for item in lst:
       process(item)  # một luồng khác có thể sửa đổi lst

Hãy cân nhắc việc đồng bộ hóa bên ngoài khi chia sẻ các экземпляр :class:`list` giữa các luồng.


.. _thread-safety-dict:

Tính an toàn luồng của các đối tượng dict
=========================================

Việc tạo một dictionary bằng constructor :class:`dict` là nguyên tử khi đối số truyền vào là :class:`dict` hoặc :class:`tuple`. Khi sử dụng
phương thức :meth:`dict.fromkeys`, việc tạo dictionary là nguyên tử khi đối số là một :class:`dict`, :class:`tuple`, :class:`set` hoặc
:class:`frozenset`.

Các thao tác và hàm sau đây là :term:`lock-free` và
:term:`atomic <atomic operation>`.

.. code-block::
   :class: good

   d[key]       # dict.__getitem__
   d.get(key)   # dict.get
   key in d     # dict.__contains__
   len(d)       # dict.__len__

Tất cả các thao tác khác từ đây trở đi đều giữ :term:`per-object lock`.

Việc ghi hoặc xóa một mục đơn lẻ có thể được gọi an toàn từ nhiều thread và sẽ không làm hỏng dictionary:

.. code-block::
   :class: good

   d[key] = value        # write
   del d[key]            # xóa
   d.pop(key)            # xóa và trả về
   d.popitem()           # xóa và trả về mục cuối cùng
   d.setdefault(key, v)  # chèn nếu bị thiếu

Các thao tác này có thể so sánh các khóa bằng :meth:`~object.__eq__`, vốn có thể thực thi mã Python tùy ý. Trong quá trình so sánh như vậy, từ điển có thể bị một thread khác sửa đổi. Đối với các kiểu dựng sẵn như :class:`str`,
:class:`int`, và :class:`float`, triển khai :meth:`~object.__eq__` bằng C, khóa bên dưới không được giải phóng trong quá trình so sánh và đây không phải là vấn đề.

Các thao tác sau đây trả về các đối tượng mới và giữ :term:`per-object lock` trong suốt thời gian thực hiện thao tác:

.. code-block::
   :class: good

   d.copy()      # trả về một bản sao nông của dict
   d | other     # gộp hai dict thành một dict mới
   d.keys()      # trả về một đối tượng view dict_keys mới
   d.values()    # trả về một đối tượng view dict_values mới
   d.items()     # trả về một đối tượng view dict_items mới

Phương thức :meth:`~dict.clear` giữ khóa trong suốt thời gian thực thi. Các luồng khác không thể quan sát thấy các phần tử đang bị xóa.

Các thao tác sau đây khóa cả hai dict. Đối với :meth:`~dict.update` và ``|=``, điều này chỉ áp dụng khi toán hạng còn lại là một :class:`dict` sử dụng trình lặp dict tiêu chuẩn (nhưng không áp dụng cho các lớp con ghi đè thao tác lặp). Đối với phép so sánh bằng, điều này áp dụng cho :class:`dict` và các lớp con của nó:

.. code-block::
   :class: good

   d.update(other_dict)  # cả hai đều bị khóa khi other_dict là một dict
   d |= other_dict       # cả hai đều bị khóa khi other_dict là một dict
   d == other_dict       # cả hai đều bị khóa đối với dict và các lớp con

Tất cả các phép so sánh cũng so sánh các giá trị bằng :meth:`~object.__eq__`, vì vậy đối với các kiểu không tích hợp, khóa có thể được giải phóng trong khi so sánh.

:meth:`~dict.fromkeys` khóa cả dictionary mới và iterable khi iterable chính xác là một :class:`dict`, :class:`set`, hoặc
:class:`frozenset` (không phải lớp con):

.. code-block::
   :class: good

   dict.fromkeys(a_dict)      # khóa cả hai
   dict.fromkeys(a_set)       # khóa cả hai
   dict.fromkeys(a_frozenset) # khóa cả hai

Khi cập nhật từ một iterable không phải dict, chỉ dictionary đích được khóa. Iterable có thể bị một thread khác sửa đổi đồng thời:

.. code-block::
   :class: maybe

   d.update(iterable)        # iterable không phải dict: chỉ khóa d
   d |= iterable             # iterable không phải dict: chỉ khóa d
   dict.fromkeys(iterable)   # iterable không phải dict/set/frozenset: chỉ khóa result

Các thao tác liên quan đến nhiều lần truy cập, cũng như việc lặp, không bao giờ là atomic:

.. code-block::
   :class: bad

   # KHÔNG nguyên tử: đọc-sửa-ghi
   d[key] = d[key] + 1

   # KHÔNG nguyên tử: kiểm tra-rồi-thực hiện (TOCTOU)
   if key in d:
       del d[key]

   # KHÔNG an toàn khi chạy đa luồng: lặp trong khi sửa đổi
   for key, value in d.items():
       process(key)  # một thread khác có thể sửa đổi d

Để tránh các vấn đề time-of-check to time-of-use (TOCTOU), hãy sử dụng các thao tác nguyên tử hoặc xử lý các exception:

.. code-block::
   :class: good

   # Sử dụng pop() với giá trị mặc định thay vì kiểm tra-rồi-xóa
   d.pop(key, None)

   # Hoặc xử lý exception
   try:
       del d[key]
   except KeyError:
       pass

Để lặp an toàn qua một dictionary có thể bị thread khác sửa đổi, hãy lặp qua một bản sao:

.. code-block::
   :class: good

   # Tạo một bản sao để lặp an toàn
   for key, value in d.copy().items():
       process(key)

Hãy cân nhắc việc đồng bộ hóa bên ngoài khi chia sẻ các instance :class:`dict` giữa các thread.


.. _thread-safety-set:

Tính an toàn thread cho các đối tượng set
=========================================

Hàm :func:`len` không cần lock và :term:`atomic <atomic operation>`.

Thao tác đọc sau đây không cần lock. Thao tác này không chặn các sửa đổi đồng thời và có thể quan sát các trạng thái trung gian từ những thao tác đang giữ lock cho từng đối tượng:

.. code-block::
   :class: good

   elem in s    # set.__contains__

Thao tác này có thể so sánh các phần tử bằng :meth:`~object.__eq__`, và thao tác đó có thể thực thi mã Python tùy ý. Trong khi thực hiện các phép so sánh này, set có thể bị thread khác sửa đổi. Đối với các kiểu tích hợp như :class:`str`,
:class:`int`, và :class:`float`, :meth:`!__eq__` không giải phóng khóa nền tảng trong quá trình so sánh và đây không phải là vấn đề đáng lo ngại.

Tất cả các thao tác khác từ đây trở đi đều giữ khóa riêng của từng đối tượng.

Việc thêm hoặc xóa một phần tử đơn lẻ là an toàn khi được gọi từ nhiều thread và sẽ không làm hỏng set:

.. code-block::
   :class: good

   s.add(elem)      # thêm phần tử
   s.remove(elem)   # xóa phần tử, báo lỗi nếu không tồn tại
   s.discard(elem)  # xóa phần tử nếu có
   s.pop()          # xóa và trả về một phần tử bất kỳ

Các thao tác này cũng so sánh các phần tử, vì vậy các :meth:`~object.__eq__` tương tự như trên cũng được áp dụng.

Phương thức :meth:`~set.copy` trả về một đối tượng mới và giữ khóa trên mỗi đối tượng trong suốt thời gian thực thi, nhờ đó luôn mang tính nguyên tử.

Phương thức :meth:`~set.clear` giữ khóa trong suốt thời gian thực thi. Các thread khác không thể quan sát các phần tử đang bị xóa.

Các thao tác sau chỉ chấp nhận :class:`set` hoặc :class:`frozenset` làm toán hạng và luôn khóa cả hai đối tượng:

.. code-block::
   :class: good

   s |= other                   # other phải là set/frozenset
   s &= other                   # other phải là set/frozenset
   s -= other                   # other phải là set/frozenset
   s ^= other                   # other phải là set/frozenset
   s & other                    # other phải là set/frozenset
   s | other                    # other phải là set/frozenset
   s - other                    # other phải là set/frozenset
   s ^ other                    # other phải là set/frozenset

:meth:`set.update`, :meth:`set.union`, :meth:`set.intersection` và
:meth:`set.difference` có thể nhận nhiều iterable làm đối số. Tất cả chúng đều lặp qua tất cả các iterable được truyền vào và thực hiện những việc sau:

   * :meth:`set.update` và :meth:`set.union` chỉ khóa cả hai đối tượng khi toán hạng còn lại là :class:`set`, :class:`frozenset` hoặc :class:`dict`.
   * :meth:`set.intersection` và :meth:`set.difference` luôn cố gắng khóa tất cả các đối tượng.

:meth:`set.symmetric_difference` cố gắng khóa cả hai đối tượng.

Các biến thể update của những phương thức trên cũng có một số điểm khác biệt giữa chúng:

   * :meth:`set.difference_update` và :meth:`set.intersection_update` cố gắng khóa lần lượt từng đối tượng.
   * :meth:`set.symmetric_difference_update` chỉ khóa các đối số nếu nó thuộc kiểu :class:`set`, :class:`frozenset` hoặc :class:`dict`.

Các phương thức sau luôn cố gắng khóa cả hai đối tượng:

.. code-block::
   :class: good

   s.isdisjoint(other)          # cả hai đều bị khóa
   s.issubset(other)            # cả hai đều bị khóa
   s.issuperset(other)          # cả hai đều bị khóa

Các thao tác bao gồm nhiều lần truy cập, cũng như việc lặp, không bao giờ là atomic:

.. code-block::
   :class: bad

   # KHÔNG atomic: kiểm tra rồi thực hiện
   if elem in s:
         s.remove(elem)

   # KHÔNG an toàn với thread: lặp trong khi sửa đổi
   for elem in s:
         process(elem)  # một thread khác có thể sửa đổi s

Hãy cân nhắc việc đồng bộ hóa bên ngoài khi chia sẻ các thể hiện :class:`set` giữa các luồng. Xem :ref:`freethreading-python-howto` để biết thêm thông tin.


.. _thread-safety-bytearray:

An toàn luồng đối với các đối tượng bytearray
=============================================

   Hàm :func:`len` không cần khóa và :term:`atomic <atomic operation>`.

   Phép nối và phép so sánh sử dụng buffer protocol, giúp ngăn việc thay đổi kích thước nhưng không giữ khóa riêng của từng đối tượng. Các thao tác này có thể quan sát các trạng thái trung gian do những thay đổi đồng thời:

   .. code-block::
      :class: maybe

      ba + other    # có thể quan sát các lần ghi đồng thời
      ba == other   # có thể quan sát các lần ghi đồng thời
      ba < other    # có thể quan sát các lần ghi đồng thời

   Từ đây trở đi, tất cả các thao tác khác đều giữ khóa riêng của từng đối tượng.

   Việc đọc một phần tử hoặc slice đơn lẻ an toàn khi được gọi từ nhiều luồng:

   .. code-block::
      :class: good

      ba[i]        # bytearray.__getitem__
      ba[i:j]      # slice

   Các thao tác sau an toàn khi được gọi từ nhiều luồng và sẽ không làm hỏng bytearray:

   .. code-block::
      :class: good

      ba[i] = x         # ghi một byte
      ba[i:j] = values  # ghi một slice
      ba.append(x)      # thêm một byte
      ba.extend(other)  # mở rộng bằng iterable
      ba.insert(i, x)   # chèn một byte
      ba.pop()          # xóa và trả về byte cuối cùng
      ba.pop(i)         # xóa và trả về byte tại chỉ mục
      ba.remove(x)      # xóa lần xuất hiện đầu tiên
      ba.reverse()      # đảo ngược tại chỗ
      ba.clear()        # xóa tất cả byte

   Phép gán lát cắt khóa cả hai đối tượng khi *values* là một :class:`bytearray`:

   .. code-block::
      :class: good

      ba[i:j] = other_bytearray  # cả hai đều bị khóa

   Các thao tác sau đây trả về đối tượng mới và giữ khóa riêng của từng đối tượng trong suốt thời gian thực hiện:

   .. code-block::
      :class: good

      ba.copy()     # trả về bản sao nông
      ba * n        # lặp vào bytearray mới

   Phép kiểm tra phần tử giữ khóa trong suốt thời gian thực hiện:

   .. code-block::
      :class: good

      x in ba       # bytearray.__contains__

   Tất cả các phương thức bytearray khác (chẳng hạn như :meth:`~bytearray.find`,
   :meth:`~bytearray.replace`, :meth:`~bytearray.split`,
   :meth:`~bytearray.decode`, v.v.) giữ khóa cho từng đối tượng trong suốt thời gian thực thi.

   Các thao tác liên quan đến nhiều lần truy cập, cũng như việc lặp, không bao giờ có tính nguyên tử:

   .. code-block::
      :class: bad

      # KHÔNG có tính nguyên tử: kiểm tra rồi thực hiện
      if x in ba:
          ba.remove(x)

      # KHÔNG an toàn trong đa luồng: lặp trong khi đang sửa đổi
      for byte in ba:
          process(byte)  # một thread khác có thể sửa đổi ba

   Để lặp an toàn qua một bytearray có thể bị thread khác sửa đổi, hãy lặp qua một bản sao:

   .. code-block::
      :class: good

      # Tạo bản sao để lặp an toàn
      for byte in ba.copy():
          process(byte)

   Hãy cân nhắc việc đồng bộ hóa bên ngoài khi chia sẻ các đối tượng :class:`bytearray` giữa các luồng. Xem :ref:`freethreading-python-howto` để biết thêm thông tin.


.. _thread-safety-memoryview:

Tính an toàn luồng đối với các đối tượng memoryview
===================================================

Các đối tượng :class:`memoryview` cho phép truy cập dữ liệu nội bộ của một đối tượng nền tảng mà không cần sao chép. Tính an toàn luồng phụ thuộc vào cả chính memoryview và bộ xuất buffer nền tảng.

Việc triển khai memoryview sử dụng các thao tác nguyên tử để theo dõi những lần xuất của chính nó trong :term:`free-threaded build`. Việc tạo và giải phóng memoryview là an toàn luồng. Việc truy cập thuộc tính (ví dụ:
:attr:`~memoryview.shape`, :attr:`~memoryview.format`) đọc các trường bất biến trong suốt vòng đời của memoryview, vì vậy việc đọc đồng thời là an toàn miễn là memoryview chưa được giải phóng.

Tuy nhiên, dữ liệu thực tế được truy cập thông qua memoryview thuộc về đối tượng nền tảng. Việc truy cập đồng thời vào dữ liệu này chỉ an toàn nếu đối tượng nền tảng hỗ trợ điều đó:

* Đối với các đối tượng bất biến như :class:`bytes`, việc đọc đồng thời thông qua nhiều memoryview là an toàn.

* Đối với các đối tượng có thể thay đổi như :class:`bytearray`, việc đọc và ghi cùng một vùng bộ nhớ từ nhiều thread mà không có cơ chế đồng bộ bên ngoài là không an toàn và có thể dẫn đến hỏng dữ liệu. Lưu ý rằng ngay cả memoryview chỉ đọc của các đối tượng có thể thay đổi cũng không ngăn được các cuộc đua dữ liệu nếu đối tượng bên dưới bị sửa đổi từ một thread khác.

.. code-block::
   :class: bad

   # KHÔNG an toàn: ghi đồng thời vào cùng một buffer
   data = bytearray(1000)
   view = memoryview(data)
   # Thread 1: view[0:500] = b'x' * 500
   # Thread 2: view[0:500] = b'y' * 500

.. code-block::
   :class: good

   # An toàn: sử dụng lock khi truy cập đồng thời
   import threading
   lock = threading.Lock()
   data = bytearray(1000)
   view = memoryview(data)

   with lock:
       view[0:500] = b'x' * 500

Việc thay đổi kích thước hoặc cấp phát lại đối tượng bên dưới (chẳng hạn như gọi
:meth:`bytearray.resize`) trong khi một memoryview đang được export sẽ gây ra
:exc:`BufferError`. Điều này được đảm bảo bất kể việc phân luồng.
