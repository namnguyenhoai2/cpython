
.. _datamodel:

***************
Mô hình dữ liệu
***************


.. _objects:

Đối tượng, giá trị và kiểu
==========================

.. index::
   single: object
   single: data

:dfn:`Đối tượng` là sự trừu tượng hóa dữ liệu của Python. Mọi dữ liệu trong một chương trình Python đều được biểu diễn bằng các đối tượng hoặc bằng các mối quan hệ giữa các đối tượng. Ngay cả mã cũng được biểu diễn bằng các đối tượng.

.. index::
   pair: built-in function; id
   pair: built-in function; type
   single: identity of an object
   single: value of an object
   single: type of an object
   single: mutable object
   single: immutable object

Mỗi đối tượng có một danh tính, một kiểu và một giá trị. *Danh tính* của một đối tượng không bao giờ thay đổi sau khi được tạo; bạn có thể xem nó là địa chỉ của đối tượng trong bộ nhớ. Toán tử :keyword:`is` so sánh danh tính của hai đối tượng; hàm
:func:`id` trả về một số nguyên biểu thị danh tính của đối tượng đó.

.. impl-detail::

   Đối với CPython, ``id(x)`` là địa chỉ bộ nhớ nơi ``x`` được lưu trữ.

Kiểu của một đối tượng xác định các thao tác mà đối tượng hỗ trợ (ví dụ: "nó có độ dài không?") và cũng xác định các giá trị có thể có cho những đối tượng thuộc kiểu đó. Hàm :func:`type` trả về kiểu của một đối tượng (bản thân kiểu đó cũng là một đối tượng). Cũng như danh tính của nó, :dfn:`kiểu` của một đối tượng cũng không thể thay đổi. [#]_

*Giá trị* của một số đối tượng có thể thay đổi. Các đối tượng có giá trị có thể thay đổi được gọi là *mutable*; các đối tượng có giá trị không thể thay đổi sau khi được tạo được gọi là *immutable*. (Giá trị của một đối tượng container immutable chứa tham chiếu đến một đối tượng mutable có thể thay đổi khi giá trị của đối tượng sau thay đổi; tuy nhiên, container vẫn được xem là immutable, vì tập hợp các đối tượng mà nó chứa không thể thay đổi. Vì vậy, tính bất biến không hoàn toàn giống với việc có một giá trị không thể thay đổi, mà tinh tế hơn.) Tính mutable của một đối tượng được xác định bởi kiểu của nó; chẳng hạn, số, chuỗi và tuple là immutable, trong khi dictionary và list là mutable.

.. index::
   single: garbage collection
   single: reference counting
   single: unreachable object

Các đối tượng không bao giờ bị hủy một cách tường minh; tuy nhiên, khi chúng trở nên không thể truy cập, chúng có thể được thu gom rác. Một implementation được phép trì hoãn việc thu gom rác hoặc bỏ qua hoàn toàn việc này --- cách thu gom rác được triển khai là vấn đề về chất lượng implementation, miễn là không thu gom bất kỳ đối tượng nào vẫn còn có thể truy cập.

.. impl-detail::

   Hiện tại, CPython sử dụng cơ chế đếm tham chiếu cùng với việc phát hiện trì hoãn (tùy chọn) các rác được liên kết theo chu kỳ; cơ chế này thu gom hầu hết đối tượng ngay khi chúng không thể truy cập, nhưng không đảm bảo thu gom rác chứa tham chiếu vòng. Xem tài liệu của module :mod:`gc` để biết thông tin về cách kiểm soát việc thu gom rác tuần hoàn. Các implementation khác hoạt động khác nhau và CPython có thể thay đổi. Đừng phụ thuộc vào việc các đối tượng được hoàn tất ngay lập tức khi chúng không thể truy cập (vì vậy bạn nên luôn đóng file một cách tường minh).

Lưu ý rằng việc sử dụng các công cụ tracing hoặc debugging của implementation có thể giữ lại các đối tượng mà bình thường có thể thu gom. Cũng lưu ý rằng việc bắt một exception bằng câu lệnh :keyword:`try`...\ :keyword:`except` có thể giữ các đối tượng tồn tại.

Một số đối tượng chứa tham chiếu đến các tài nguyên "bên ngoài" như file hoặc cửa sổ đang mở. Các tài nguyên này được hiểu là sẽ được giải phóng khi đối tượng được thu gom rác, nhưng vì việc thu gom rác không được đảm bảo xảy ra, các đối tượng như vậy cũng cung cấp một cách tường minh để giải phóng tài nguyên bên ngoài, thường là một method :meth:`!close`. Các chương trình được đặc biệt khuyến nghị đóng các đối tượng như vậy một cách tường minh. Câu lệnh :keyword:`try`...\ :keyword:`finally` và câu lệnh :keyword:`with` cung cấp những cách thuận tiện để thực hiện việc này.

.. index:: single: container

Một số đối tượng chứa tham chiếu đến các đối tượng khác; chúng được gọi là *container*. Ví dụ về container là tuple, list và dictionary. Các tham chiếu là một phần trong giá trị của container. Trong đa số trường hợp, khi nói về giá trị của container, chúng ta ngụ ý giá trị chứ không phải danh tính của các đối tượng được chứa; tuy nhiên, khi nói về tính mutable của container, chỉ danh tính của các đối tượng được chứa trực tiếp mới được ngụ ý. Vì vậy, nếu một container immutable (như tuple) chứa tham chiếu đến một đối tượng mutable, giá trị của nó sẽ thay đổi nếu đối tượng mutable đó thay đổi.

Kiểu ảnh hưởng đến gần như mọi khía cạnh trong hành vi của đối tượng. Theo một nghĩa nào đó, ngay cả tầm quan trọng của danh tính đối tượng cũng bị ảnh hưởng: với các kiểu immutable, những thao tác tính giá trị mới thực tế có thể trả về tham chiếu đến bất kỳ đối tượng hiện có nào có cùng kiểu và giá trị, trong khi điều này không được phép với đối tượng mutable. Ví dụ, sau ``a = 1; b = 1``, *a* và *b* có thể có hoặc không cùng tham chiếu đến một đối tượng có giá trị là một, tùy thuộc vào implementation. Điều này là do :class:`int` là một kiểu immutable, nên tham chiếu đến ``1`` có thể được tái sử dụng. Hành vi này phụ thuộc vào implementation được sử dụng, vì vậy không nên dựa vào nó, nhưng cần lưu ý khi sử dụng các phép kiểm tra danh tính đối tượng. Tuy nhiên, sau ``c = []; d = []``, *c* và *d* được đảm bảo tham chiếu đến hai list rỗng khác nhau, duy nhất, vừa được tạo. (Lưu ý rằng ``e = f = []`` gán đối tượng *cùng một* cho cả *e* và *f*.)


.. _types:

Hệ phân cấp kiểu chuẩn
======================

.. index::
   single: type
   pair: data; type
   pair: type; hierarchy
   pair: extension; module
   pair: C; language

Dưới đây là danh sách các kiểu được tích hợp sẵn trong Python. Các extension module (được viết bằng C, Java hoặc các ngôn ngữ khác, tùy thuộc vào implementation) có thể định nghĩa các kiểu bổ sung. Các phiên bản Python trong tương lai có thể thêm kiểu vào hệ phân cấp kiểu (ví dụ: số hữu tỉ, mảng số nguyên được lưu trữ hiệu quả, v.v.), mặc dù những phần bổ sung như vậy thường sẽ được cung cấp thông qua standard library.

.. index::
   single: attribute
   pair: special; attribute
   triple: generic; special; attribute

Một số mô tả kiểu bên dưới có một đoạn liệt kê các 'thuộc tính đặc biệt'. Đây là các thuộc tính cung cấp quyền truy cập vào implementation và không предназначены для общего использования. Định nghĩa của chúng có thể thay đổi trong tương lai.


None
----

.. index:: pair: object; None

Kiểu này có một giá trị duy nhất. Có một đối tượng duy nhất với giá trị này. Đối tượng này được truy cập thông qua tên tích hợp sẵn ``None``. Nó được dùng để biểu thị sự vắng mặt của một giá trị trong nhiều tình huống, ví dụ, nó được trả về từ các hàm không trả về rõ ràng bất cứ thứ gì. Giá trị chân lý của nó là false.


NotImplemented
--------------

.. index:: pair: object; NotImplemented

Kiểu này có một giá trị duy nhất. Có một đối tượng duy nhất với giá trị này. Đối tượng này được truy cập thông qua tên tích hợp sẵn :data:`NotImplemented`. Các phương thức số học và phương thức so sánh phong phú nên trả về giá trị này nếu chúng không triển khai phép toán cho các toán hạng được cung cấp. (Khi đó, trình thông dịch sẽ thử phép toán phản chiếu hoặc một phương án dự phòng khác, tùy thuộc vào toán tử.) Nó không nên được đánh giá trong ngữ cảnh boolean.

Xem
:ref:`implementing-the-arithmetic-operations` để biết thêm chi tiết.

.. versionchanged:: 3.9
   Việc đánh giá :data:`NotImplemented` trong ngữ cảnh boolean đã bị phản đối sử dụng.

.. versionchanged:: 3.14
   Việc đánh giá :data:`NotImplemented` trong ngữ cảnh boolean hiện sẽ phát sinh :exc:`TypeError`. Trước đây, nó được đánh giá thành :const:`True` và phát ra :exc:`DeprecationWarning` kể từ Python 3.9.


Ellipsis
--------
.. index::
   pair: object; Ellipsis
   single: ...; ellipsis literal

Kiểu này có một giá trị duy nhất. Có một đối tượng duy nhất mang giá trị này. Đối tượng này được truy cập thông qua literal ``...`` hoặc tên built-in ``Ellipsis``. Giá trị chân trị của nó là true.


:class:`numbers.Number`
-----------------------

.. index:: pair: object; numeric

Các đối tượng này được tạo bởi các literal số và được trả về làm kết quả bởi các toán tử số học cùng các hàm built-in số học. Đối tượng số là bất biến; sau khi được tạo, giá trị của chúng không bao giờ thay đổi. Dĩ nhiên, các số Python có liên hệ chặt chẽ với các số trong toán học, nhưng chịu những giới hạn của việc biểu diễn số trong máy tính.

Biểu diễn chuỗi của các lớp số, được tính bởi
:meth:`~object.__repr__` và :meth:`~object.__str__`, có các đặc tính sau:

* Chúng là các literal số hợp lệ; khi được truyền vào constructor của lớp tương ứng, chúng sẽ tạo ra một đối tượng có giá trị bằng số ban đầu.

* Biểu diễn dùng cơ số 10 khi có thể.

* Không hiển thị các số 0 ở đầu, ngoại trừ có thể là một số 0 duy nhất trước dấu thập phân.

* Không hiển thị các số 0 ở cuối, ngoại trừ có thể là một số 0 duy nhất sau dấu thập phân.

* Chỉ hiển thị dấu khi số là số âm.

Python phân biệt giữa số nguyên, số dấu phẩy động và số phức:


:class:`numbers.Integral`
^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: pair: object; integer

Chúng biểu thị các phần tử thuộc tập hợp toán học các số nguyên (dương và âm).

.. note::
   .. index:: pair: integer; representation

   Các quy tắc biểu diễn số nguyên nhằm đưa ra cách diễn giải có ý nghĩa nhất cho các phép toán dịch và che có liên quan đến số nguyên âm.

Có hai loại số nguyên:

Số nguyên (:class:`int`)
   Chúng biểu thị các số trong phạm vi không giới hạn, chỉ bị giới hạn bởi bộ nhớ (ảo) sẵn có. Đối với các phép toán dịch và che, giả định một biểu diễn nhị phân, trong đó các số âm được biểu diễn bằng một biến thể của bù 2, tạo cảm giác về một chuỗi vô hạn các bit dấu kéo dài về bên trái.

Giá trị Boolean (:class:`bool`)
   .. index::
      pair: object; Boolean
      single: False
      single: True

   Chúng biểu thị các giá trị chân lý False và True. Hai đối tượng biểu thị các giá trị ``False`` và ``True`` là các đối tượng Boolean duy nhất. Kiểu Boolean là một kiểu con của kiểu integer, và các giá trị Boolean hoạt động tương ứng như các giá trị 0 và 1 trong gần như mọi ngữ cảnh; ngoại lệ là khi được chuyển đổi thành chuỗi, chúng lần lượt trả về các chuỗi ``"False"`` hoặc ``"True"``.


.. _datamodel-float:

:class:`numbers.Real` (:class:`float`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; floating-point
   pair: floating-point; number
   pair: C; language
   pair: Java; language

Chúng biểu thị các số dấu phẩy động độ chính xác kép ở cấp máy. Phạm vi được chấp nhận và cách xử lý tràn số phụ thuộc vào kiến trúc máy bên dưới (cũng như việc triển khai C hoặc Java). Python không hỗ trợ số dấu phẩy động độ chính xác đơn; mức tiết kiệm tài nguyên bộ xử lý và bộ nhớ vốn thường là lý do để sử dụng chúng bị chi phí xử lý của việc dùng đối tượng trong Python lấn át, vì vậy không có lý do gì để làm ngôn ngữ phức tạp hơn bằng hai loại số dấu phẩy động.


:class:`numbers.Complex` (:class:`complex`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; complex
   pair: complex; number

Chúng biểu thị số phức dưới dạng một cặp số dấu phẩy động độ chính xác kép ở cấp máy. Các lưu ý tương tự như đối với số dấu phẩy động cũng được áp dụng. Phần thực và phần ảo của một số phức ``z`` có thể được truy xuất qua các thuộc tính chỉ đọc ``z.real`` và ``z.imag``.

.. _datamodel-sequences:

Các sequence
------------

.. index::
   pair: built-in function; len
   pair: object; sequence
   single: index operation
   single: item selection
   single: subscription

Chúng biểu thị các tập hợp hữu hạn có thứ tự, được đánh chỉ mục bằng các số không âm. Hàm tích hợp :func:`len` trả về số lượng phần tử của một sequence. Khi độ dài của một sequence là *n*, tập chỉ mục chứa các số 0, 1, ..., *n*-1. Phần tử *i* của sequence *a* được chọn bằng ``a[i]``. Một số sequence, bao gồm các sequence tích hợp, diễn giải chỉ số âm bằng cách cộng với độ dài của sequence. Ví dụ, ``a[-2]`` bằng ``a[n-2]``, là phần tử áp chót của sequence a có độ dài ``n``.

Giá trị kết quả phải là một số nguyên không âm nhỏ hơn số lượng phần tử trong sequence. Nếu không, một :exc:`IndexError` sẽ được phát sinh.

.. index::
   single: slicing
   single: start (slice object attribute)
   single: stop (slice object attribute)
   single: step (slice object attribute)

Sequence cũng hỗ trợ slicing: ``a[start:stop]`` chọn tất cả các phần tử có chỉ mục *k* sao cho *start* ``<=`` *k* ``<`` *stop*. Khi được dùng làm biểu thức, một slice là một sequence cùng kiểu. Nhận xét ở trên về chỉ số âm cũng áp dụng cho các vị trí slice âm. Lưu ý rằng không có lỗi nào được phát sinh nếu một vị trí slice nhỏ hơn không hoặc lớn hơn độ dài của sequence.

Nếu *start* bị thiếu hoặc là :data:`None`, thao tác cắt hoạt động như thể *start* bằng không. Nếu *stop* bị thiếu hoặc là ``None``, thao tác cắt hoạt động như thể *stop* bằng độ dài của sequence.

Một số sequence cũng hỗ trợ "extended slicing" với tham số "step" thứ ba: ``a[i:j:k]`` chọn tất cả phần tử của *a* có chỉ mục *x* sao cho ``x = i + n*k``, *n* ``>=`` ``0`` và *i* ``<=`` *x* ``<`` *j*.

Các sequence được phân biệt theo tính có thể thay đổi của chúng:


Sequence bất biến
^^^^^^^^^^^^^^^^^

.. index::
   pair: object; immutable sequence
   pair: object; immutable

Một object thuộc kiểu sequence bất biến không thể thay đổi sau khi được tạo. (Nếu object đó chứa các reference đến những object khác, các object khác này có thể thay đổi được và có thể bị thay đổi; tuy nhiên, tập hợp các object được một object bất biến tham chiếu trực tiếp không thể thay đổi.)

Các kiểu sau là sequence bất biến:

.. index::
   single: string; immutable sequences

String
   .. index::
      pair: built-in function; chr
      pair: built-in function; ord
      single: character
      pair: string; item
      single: Unicode

   Một string (:class:`str`) là một chuỗi các giá trị biểu diễn
   :dfn:`ký tự`, hay chính xác hơn là *các điểm mã Unicode*. Mọi điểm mã trong phạm vi từ ``0`` đến ``0x10FFFF`` đều có thể được biểu diễn trong một string.

   Python không có kiểu *ký tự* chuyên biệt. Thay vào đó, mỗi điểm mã trong string được biểu diễn bằng một đối tượng string có độ dài ``1``.

   Hàm dựng sẵn :func:`ord` chuyển đổi một điểm mã từ dạng string của nó thành một số nguyên trong phạm vi từ ``0`` đến ``0x10FFFF``; :func:`chr` chuyển đổi một số nguyên trong phạm vi từ ``0`` đến ``0x10FFFF`` thành đối tượng string có độ dài ``1`` tương ứng.
   Có thể dùng :meth:`str.encode` để chuyển đổi một :class:`str` thành
   :class:`bytes` bằng cách sử dụng mã hóa văn bản đã cho, và
   có thể dùng :meth:`bytes.decode` để thực hiện thao tác ngược lại.

Tuple
   .. index::
      pair: object; tuple
      pair: singleton; tuple
      pair: empty; tuple

   Các phần tử của một :class:`tuple` là các đối tượng Python bất kỳ. Tuple có từ hai phần tử trở lên được tạo thành bằng danh sách các biểu thức phân tách bằng dấu phẩy. Tuple có một phần tử (một 'singleton') có thể được tạo bằng cách thêm dấu phẩy vào một biểu thức (một biểu thức tự nó không tạo ra tuple, vì dấu ngoặc đơn phải có thể dùng để nhóm các biểu thức). Một tuple rỗng có thể được tạo bằng một cặp dấu ngoặc đơn rỗng.

Bytes
   .. index:: bytes, byte

   Một đối tượng :class:`bytes` là một mảng bất biến. Các phần tử là byte 8-bit, được biểu diễn bằng các số nguyên trong phạm vi 0 <= x < 256. Các literal bytes (như ``b'abc'``) và constructor dựng sẵn :func:`bytes` có thể được dùng để tạo đối tượng bytes. Ngoài ra, các đối tượng bytes có thể được giải mã thành chuỗi thông qua phương thức :meth:`~bytes.decode`.


Các sequence có thể thay đổi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; mutable sequence
   pair: object; mutable
   pair: assignment; statement
   single: subscription
   single: slicing

Các sequence có thể thay đổi có thể được sửa đổi sau khi được tạo. Ký pháp subscription và slicing có thể được dùng làm đích của các câu lệnh gán và :keyword:`del` (xóa).

.. note::
   .. index:: pair: module; array
   .. index:: pair: module; collections

   Module :mod:`collections` và :mod:`array` cung cấp thêm các ví dụ về các kiểu sequence có thể thay đổi.

Hiện có hai kiểu sequence có thể thay đổi (mutable) nội tại:

List
   .. index:: pair: object; list

   Các phần tử của một list có thể là các đối tượng Python bất kỳ. List được tạo bằng cách đặt một danh sách biểu thức phân tách bằng dấu phẩy trong dấu ngoặc vuông. (Lưu ý rằng không cần trường hợp đặc biệt nào để tạo list có độ dài 0 hoặc 1.)

Mảng byte
   .. index:: bytearray

   Đối tượng bytearray là một mảng có thể thay đổi. Chúng được tạo bởi hàm dựng tích hợp sẵn
   :func:`bytearray`. Ngoài việc có thể thay đổi (và do đó không thể băm), mảng byte còn cung cấp cùng interface và chức năng như các đối tượng :class:`bytes` bất biến.


Các kiểu set
------------

.. index::
   pair: built-in function; len
   pair: object; set type

Chúng biểu diễn các tập hợp hữu hạn, không có thứ tự, gồm những đối tượng duy nhất và bất biến. Do đó, không thể truy cập chúng bằng chỉ số. Tuy nhiên, có thể lặp qua chúng, và hàm dựng sẵn :func:`len` trả về số lượng phần tử trong một tập hợp. Các cách dùng phổ biến của tập hợp là kiểm tra thành viên nhanh, loại bỏ phần tử trùng lặp khỏi một chuỗi, và tính các phép toán toán học như giao, hợp, hiệu và hiệu đối xứng.

Đối với các phần tử của tập hợp, áp dụng cùng các quy tắc bất biến như đối với khóa từ điển. Lưu ý rằng các kiểu số tuân theo các quy tắc thông thường về so sánh số: nếu hai số được so sánh là bằng nhau (ví dụ: ``1`` và ``1.0``), chỉ một trong số chúng có thể nằm trong một tập hợp.

Hiện có hai kiểu tập hợp nội tại:


Tập hợp
   .. index:: pair: object; set

   Chúng biểu diễn một tập hợp có thể thay đổi. Chúng được tạo bằng constructor dựng sẵn :func:`set` và sau đó có thể được sửa đổi bằng một số phương thức, chẳng hạn như
   :meth:`~set.add`.


Tập hợp đóng băng
   .. index:: pair: object; frozenset

   Chúng biểu diễn một tập hợp bất biến. Chúng được tạo bằng hàm dựng sẵn
   constructor :func:`frozenset`. Vì frozenset là bất biến và
   :term:`hashable`, nó có thể კვლავ được dùng làm phần tử của một set khác hoặc làm khóa dictionary.


.. _datamodel-mappings:

Ánh xạ
------

.. index::
   pair: built-in function; len
   single: subscription
   pair: object; mapping

Các kiểu này biểu diễn những tập hợp hữu hạn các đối tượng được lập chỉ mục bởi các tập chỉ mục tùy ý. Ký pháp chỉ số ``a[k]`` chọn mục được lập chỉ mục bởi ``k`` từ ánh xạ ``a``; ký pháp này có thể được dùng trong biểu thức và làm đích của phép gán hoặc
các câu lệnh :keyword:`del`. Hàm dựng sẵn :func:`len` trả về số lượng mục trong một ánh xạ.

Hiện tại có một kiểu ánh xạ nội tại duy nhất:


Dictionary
^^^^^^^^^^

.. index:: pair: object; dictionary

Chúng biểu diễn các tập hợp hữu hạn gồm những đối tượng được lập chỉ mục bằng các giá trị gần như tùy ý. Những kiểu giá trị duy nhất không thể dùng làm khóa là các giá trị chứa list hoặc dictionary hay các kiểu mutable khác được so sánh theo giá trị thay vì theo định danh đối tượng, vì việc triển khai dictionary hiệu quả đòi hỏi giá trị hash của khóa phải không đổi. Các kiểu số dùng làm khóa tuân theo các quy tắc thông thường về so sánh số: nếu hai số so sánh bằng nhau (ví dụ: ``1`` và ``1.0``) thì chúng có thể được dùng thay thế cho nhau để lập chỉ mục cùng một mục dictionary.

Dictionary bảo toàn thứ tự chèn, nghĩa là các khóa sẽ được tạo ra theo đúng thứ tự chúng đã được thêm tuần tự vào dictionary. Tuy nhiên, việc thay thế một khóa hiện có không làm thay đổi thứ tự; còn việc xóa một khóa rồi chèn lại sẽ thêm khóa đó vào cuối thay vì giữ vị trí cũ.

Dictionary là mutable; chúng có thể được tạo bằng ký pháp ``{}`` (xem phần :ref:`dict`).

.. index::
   pair: module; dbm.ndbm
   pair: module; dbm.gnu

Các extension module :mod:`dbm.ndbm` và :mod:`dbm.gnu` cung cấp thêm các ví dụ về kiểu mapping, cũng như module :mod:`collections`.

.. versionchanged:: 3.7
   Dictionary không bảo toàn thứ tự chèn trong các phiên bản Python trước 3.6. Trong CPython 3.6, thứ tự chèn được bảo toàn, nhưng khi đó điều này được xem là một chi tiết triển khai thay vì một bảo đảm của ngôn ngữ.


Các kiểu callable
-----------------

.. index::
   pair: object; callable
   pair: function; call
   single: invocation
   pair: function; argument

Đây là các kiểu mà thao tác gọi hàm áp dụng được (xem phần
:ref:`calls`) có thể được áp dụng:


.. _user-defined-funcs:

Các hàm do người dùng định nghĩa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: user-defined; function
   pair: object; function
   pair: object; user-defined function

Một đối tượng hàm do người dùng định nghĩa được tạo bởi một định nghĩa hàm (xem mục :ref:`function`). Hàm này nên được gọi với một danh sách đối số chứa số lượng mục bằng với danh sách tham số hình thức của hàm.

Các thuộc tính chỉ đọc đặc biệt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
   single: __builtins__ (function attribute)
   single: __closure__ (function attribute)
   single: __globals__ (function attribute)
   pair: global; namespace

.. list-table::
   :header-rows: 1

   * - Thuộc tính
     - Ý nghĩa

   * - .. attribute:: function.__builtins__
     - Một tham chiếu đến :class:`dictionary <dict>` chứa không gian tên builtins của hàm.

       .. versionadded:: 3.10

   * - .. attribute:: function.__globals__
     - Tham chiếu đến :class:`dictionary <dict>` chứa các biến của hàm
       :ref:`biến toàn cục <naming>` -- không gian tên toàn cục của mô-đun nơi hàm được định nghĩa.

   * - .. attribute:: function.__closure__
     - ``None`` hoặc một :class:`tuple` gồm các ô chứa các liên kết cho những tên được chỉ định trong thuộc tính :attr:`~codeobject.co_freevars` của hàm
       :attr:`code object <function.__code__>`.

       Một đối tượng ô có thuộc tính ``cell_contents``. Thuộc tính này có thể được dùng để lấy giá trị của ô cũng như đặt giá trị.

Các thuộc tính đặc biệt có thể ghi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index::
   single: __doc__ (function attribute)
   single: __name__ (function attribute)
   single: __module__ (function attribute)
   single: __dict__ (function attribute)
   single: __defaults__ (function attribute)
   single: __code__ (function attribute)
   single: __annotations__ (function attribute)
   single: __annotate__ (function attribute)
   single: __kwdefaults__ (function attribute)
   single: __type_params__ (function attribute)

Hầu hết các thuộc tính này đều kiểm tra kiểu của giá trị được gán:

.. list-table::
   :header-rows: 1

   * - Thuộc tính
     - Ý nghĩa

   * - .. attribute:: function.__doc__
     - Chuỗi tài liệu của hàm hoặc ``None`` nếu không có.

   * - .. attribute:: function.__name__
     - Tên của hàm. Xem thêm: :attr:`__name__ attributes <definition.__name__>`.

   * - .. attribute:: function.__qualname__
     - :term:`qualified name` của hàm. Xem thêm: :attr:`__qualname__ attributes <definition.__qualname__>`.

       .. versionadded:: 3.3

   * - .. attribute:: function.__module__
     - Tên của module nơi hàm được định nghĩa hoặc ``None`` nếu không có.

   * - .. attribute:: function.__defaults__
     - Một :class:`tuple` chứa các giá trị :term:`parameter` mặc định cho những tham số có giá trị mặc định, hoặc ``None`` nếu không có tham số nào có giá trị mặc định.

   * - .. attribute:: function.__code__
     - :ref:`đối tượng mã <code-objects>` biểu diễn phần thân hàm đã được biên dịch.

   * - .. attribute:: function.__dict__
     - Không gian tên hỗ trợ các thuộc tính hàm tùy ý. Xem thêm: :attr:`__dict__ attributes <object.__dict__>`.

   * - .. attribute:: function.__annotations__
     - Một :class:`dictionary <dict>` chứa các annotation của
       :term:`parameters <parameter>`. Các khóa của dictionary là tên tham số, và ``'return'`` dành cho annotation trả về, nếu được cung cấp. Xem thêm: :attr:`object.__annotations__`.

       .. versionchanged:: 3.14
          Các annotation hiện được :ref:`đánh giá lười <lazy-evaluation>`. Xem :pep:`649`.

   * - .. attribute:: function.__annotate__
     - :term:`annotate function` dành cho hàm này, hoặc ``None`` nếu hàm không có annotation. Xem :attr:`object.__annotate__`.

       .. versionadded:: 3.14

   * - .. attribute:: function.__kwdefaults__
     - Một :class:`dictionary <dict>` chứa các giá trị mặc định cho các tham số chỉ nhận keyword
       :term:`parameters <parameter>`.

   * - .. attribute:: function.__type_params__
     - Một :class:`tuple` chứa các :ref:`tham số kiểu <type-params>` của một :ref:`hàm generic <generic-functions>`.

       .. versionadded:: 3.12

Các đối tượng hàm cũng hỗ trợ lấy và thiết lập các thuộc tính tùy ý; chẳng hạn, có thể dùng chúng để gắn metadata vào hàm. Ký pháp dấu chấm thuộc tính thông thường được dùng để lấy và thiết lập các thuộc tính đó.

.. impl-detail::

   Cách triển khai hiện tại của CPython chỉ hỗ trợ các thuộc tính hàm trên những hàm do người dùng định nghĩa. Các thuộc tính hàm trên
   :ref:`các hàm built-in <builtin-functions>` có thể được hỗ trợ trong tương lai.

Thông tin bổ sung về định nghĩa của một hàm có thể được truy xuất từ
:ref:`code object <code-objects>` của nó (có thể truy cập thông qua thuộc tính :attr:`~function.__code__`).


.. _instance-methods:

Các phương thức instance
^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; method
   pair: object; user-defined method
   pair: user-defined; method

Một đối tượng phương thức instance kết hợp một lớp, một instance của lớp và bất kỳ đối tượng callable nào (thông thường là một hàm do người dùng định nghĩa).

.. index::
   single: __func__ (method attribute)
   single: __self__ (method attribute)
   single: __doc__ (method attribute)
   single: __name__ (method attribute)
   single: __module__ (method attribute)

Các thuộc tính đặc biệt chỉ đọc:

.. list-table::

   * - .. attribute:: method.__self__
     - Tham chiếu đến đối tượng instance của lớp mà phương thức được
       :ref:`bound <method-binding>`

   * - .. attribute:: method.__func__
     - Tham chiếu đến :ref:`đối tượng function gốc <user-defined-funcs>`

   * - .. attribute:: method.__doc__
     - Tài liệu của phương thức (giống như :attr:`method.__func__.__doc__ <function.__doc__>`). Là :class:`string <str>` nếu hàm gốc có docstring, nếu không thì là ``None``.

   * - .. attribute:: method.__name__
     - Tên của phương thức (giống như :attr:`method.__func__.__name__ <function.__name__>`)

   * - .. attribute:: method.__module__
     - Tên của module nơi phương thức được định nghĩa, hoặc ``None`` nếu không khả dụng.

Các phương thức cũng hỗ trợ truy cập (nhưng không thiết lập) các thuộc tính hàm tùy ý trên :ref:`function object <user-defined-funcs>` cơ sở.

Các đối tượng phương thức do người dùng định nghĩa có thể được tạo khi lấy một thuộc tính của một lớp (có thể thông qua một instance của lớp đó), nếu thuộc tính đó là một :ref:`function object <user-defined-funcs>` do người dùng định nghĩa hoặc một
đối tượng :class:`classmethod`.

.. _method-binding:

Khi một đối tượng phương thức instance được tạo bằng cách truy xuất một đối tượng do người dùng định nghĩa
:ref:`đối tượng hàm <user-defined-funcs>` từ một class thông qua một trong các instance của nó, thuộc tính :attr:`~method.__self__` của đối tượng đó là instance này, và đối tượng phương thức được gọi là đã được *ràng buộc*. Thuộc tính :attr:`~method.__func__` của phương thức mới là đối tượng hàm gốc.

Khi một đối tượng phương thức instance được tạo bằng cách truy xuất một đối tượng :class:`classmethod` từ một class hoặc instance, thuộc tính :attr:`~method.__self__` của nó là chính class đó, và thuộc tính :attr:`~method.__func__` của nó là đối tượng hàm nền tảng của phương thức class.

Khi một đối tượng phương thức instance được gọi, hàm cơ sở (:attr:`~method.__func__`) sẽ được gọi, với instance của lớp (:attr:`~method.__self__`) được chèn vào đầu danh sách đối số. Ví dụ, khi
:class:`!C` là một lớp chứa định nghĩa cho một hàm
:meth:`!f`, và ``x`` là một instance của :class:`!C`, việc gọi ``x.f(1)`` tương đương với việc gọi ``C.f(x, 1)``.

Khi một đối tượng phương thức instance được tạo từ một đối tượng :class:`classmethod`, "instance của lớp" được lưu trong :attr:`~method.__self__` thực chất sẽ là chính lớp đó, vì vậy việc gọi ``x.f(1)`` hoặc ``C.f(1)`` đều tương đương với việc gọi ``f(C,1)``, trong đó ``f`` là hàm cơ sở.

Điều quan trọng cần lưu ý là các hàm do người dùng định nghĩa, vốn là thuộc tính của một instance lớp, sẽ không được chuyển đổi thành các bound method; điều này *chỉ* xảy ra khi hàm là một thuộc tính của lớp.


Hàm generator
^^^^^^^^^^^^^

.. index::
   single: generator; function
   single: generator; iterator

Một hàm hoặc phương thức chứa biểu thức :keyword:`yield` (xem phần
:ref:`yieldexpr`) được gọi là một :dfn:`hàm generator`. Khi được gọi, một hàm như vậy luôn trả về một :term:`iterator` đối tượng có thể dùng để thực thi phần thân của hàm: việc gọi phương thức của iterator
:meth:`iterator.__next__` sẽ khiến hàm thực thi cho đến khi cung cấp một giá trị bằng biểu thức :keyword:`!yield`. Khi hàm thực thi một câu lệnh :keyword:`return` hoặc chạy đến cuối hàm, một
:exc:`StopIteration` ngoại lệ được phát sinh và iterator sẽ đi đến cuối tập hợp các giá trị cần trả về.


Hàm coroutine
^^^^^^^^^^^^^

.. index::
   single: coroutine; function

Một hàm hoặc phương thức được định nghĩa bằng :keyword:`async def` được gọi là một :dfn:`hàm coroutine`. Khi được gọi, một hàm như vậy trả về một
:term:`coroutine` đối tượng. Nó có thể chứa các biểu thức :keyword:`await`, cũng như các câu lệnh :keyword:`async with` và :keyword:`async for`. Xem thêm phần :ref:`coroutine-objects`.


Hàm generator bất đồng bộ
^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: asynchronous generator; function
   single: asynchronous generator; asynchronous iterator

Một hàm hoặc phương thức được định nghĩa bằng :keyword:`async def` và chứa biểu thức :keyword:`yield` được gọi là một
:dfn:`hàm generator bất đồng bộ`. Khi được gọi, một hàm như vậy trả về một đối tượng :term:`asynchronous iterator` có thể được dùng trong một
câu lệnh :keyword:`async for` để thực thi phần thân của hàm.

Việc gọi
phương thức :meth:`aiterator.__anext__ <object.__anext__>` của iterator bất đồng bộ sẽ trả về một :term:`awaitable`; khi await đối tượng này, quá trình thực thi sẽ tiếp tục cho đến khi nó cung cấp một giá trị bằng biểu thức :keyword:`yield`. Khi hàm thực thi một câu lệnh :keyword:`return` rỗng hoặc chạy đến cuối, một ngoại lệ :exc:`StopAsyncIteration` sẽ được phát sinh và iterator bất đồng bộ sẽ đạt đến cuối tập giá trị cần yield.


.. _builtin-functions:

Các hàm tích hợp sẵn
^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; built-in function
   pair: object; function
   pair: C; language

Đối tượng hàm tích hợp sẵn là một wrapper quanh một hàm C. Ví dụ về các hàm tích hợp sẵn là :func:`len` và :func:`math.sin` (:mod:`math` là một module tích hợp sẵn chuẩn). Số lượng và kiểu đối số được xác định bởi hàm C. Các thuộc tính đặc biệt chỉ đọc:

* :attr:`!__doc__` là chuỗi tài liệu của hàm, hoặc ``None`` nếu không có. Xem :attr:`function.__doc__`.
* :attr:`!__name__` là tên của hàm. Xem :attr:`function.__name__`.
* :attr:`!__self__` được đặt thành ``None`` (nhưng hãy xem mục tiếp theo).
* :attr:`!__module__` là tên của mô-đun nơi hàm được định nghĩa, hoặc ``None`` nếu không có. Xem :attr:`function.__module__`.


.. _builtin-methods:

Các phương thức dựng sẵn
^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; built-in method
   pair: object; method
   pair: built-in; method

Đây thực chất là một dạng khác của hàm dựng sẵn, lần này chứa một đối tượng được truyền tới hàm C như một đối số bổ sung ngầm định. Một ví dụ về phương thức dựng sẵn là ``alist.append()``, giả sử *alist* là một đối tượng danh sách. Trong trường hợp này, thuộc tính chỉ đọc đặc biệt :attr:`!__self__` được đặt thành đối tượng được biểu thị bởi *alist*. (Thuộc tính này có cùng ngữ nghĩa như khi dùng với
:attr:`other instance methods <method.__self__>`.)

.. _classes:

Lớp
^^^

Các lớp có thể gọi được. Những đối tượng này thường hoạt động như các factory để tạo các instance mới của chính chúng, nhưng có thể có các biến thể đối với những kiểu lớp ghi đè :meth:`~object.__new__`. Các đối số của lời gọi được փոխանց cho
:meth:`!__new__` và, trong trường hợp điển hình, cho :meth:`~object.__init__` để khởi tạo instance mới.


Các instance của lớp
^^^^^^^^^^^^^^^^^^^^

Có thể làm cho các instance của những lớp tùy ý có thể gọi được bằng cách định nghĩa một
phương thức :meth:`~object.__call__` trong lớp của chúng.


.. _module-objects:

Module
------

.. index::
   pair: statement; import
   pair: object; module

Module là một đơn vị tổ chức cơ bản của mã Python và được tạo bởi :ref:`hệ thống import <importsystem>`, như được gọi bởi một trong hai cách sau
câu lệnh :keyword:`import`, hoặc bằng cách gọi các hàm như :func:`importlib.import_module` và hàm dựng sẵn
:func:`__import__`. Một đối tượng module có một namespace được triển khai bởi một
đối tượng :class:`dictionary <dict>` (đây là dictionary được tham chiếu bởi thuộc tính
:attr:`~function.__globals__` của các hàm được định nghĩa trong module). Các tham chiếu thuộc tính được chuyển thành các thao tác tra cứu trong dictionary này, ví dụ, ``m.x`` tương đương với ``m.__dict__["x"]``. Một đối tượng module không chứa code object được dùng để khởi tạo module (vì nó không cần thiết sau khi quá trình khởi tạo hoàn tất).

Việc gán thuộc tính sẽ cập nhật dictionary namespace của module, ví dụ, ``m.x = 1`` tương đương với ``m.__dict__["x"] = 1``.

.. index::
   single: __name__ (module attribute)
   single: __spec__ (module attribute)
   single: __package__ (module attribute)
   single: __loader__ (module attribute)
   single: __path__ (module attribute)
   single: __file__ (module attribute)
   single: __cached__ (module attribute)
   single: __doc__ (module attribute)
   single: __annotations__ (module attribute)
   single: __annotate__ (module attribute)
   pair: module; namespace

.. _import-mod-attrs:

Các thuộc tính liên quan đến import trên đối tượng module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các đối tượng module có các thuộc tính sau đây liên quan đến
:ref:`import system <importsystem>`. Khi một module được tạo bằng cơ chế liên kết với import system, các thuộc tính này được điền dựa trên module đó
:term:`spec <module spec>`, trước khi :term:`loader` thực thi và tải module.

Để tạo một module động thay vì sử dụng import system, bạn nên dùng :func:`importlib.util.module_from_spec`, hàm này sẽ đặt các thuộc tính do import kiểm soát thành những giá trị phù hợp. Bạn cũng có thể dùng constructor :class:`types.ModuleType` để tạo module trực tiếp, nhưng kỹ thuật này dễ gây lỗi hơn, vì với cách này, hầu hết thuộc tính phải được đặt thủ công trên đối tượng module sau khi nó được tạo.

.. caution::

   Ngoại trừ :attr:`~module.__name__`, bạn **rất** nên dựa vào :attr:`~module.__spec__` và các thuộc tính của nó thay vì bất kỳ thuộc tính riêng lẻ nào khác được liệt kê trong tiểu mục này. Lưu ý rằng việc cập nhật một thuộc tính trên :attr:`!__spec__` sẽ không cập nhật thuộc tính tương ứng trên chính module:

   .. doctest::

     >>> import typing
     >>> typing.__name__, typing.__spec__.name
     ('typing', 'typing')
     >>> typing.__spec__.name = 'spelling'
     >>> typing.__name__, typing.__spec__.name
     ('typing', 'spelling')
     >>> typing.__name__ = 'keyboard_smashing'
     >>> typing.__name__, typing.__spec__.name
     ('keyboard_smashing', 'spelling')

.. attribute:: module.__name__

   Tên được dùng để nhận diện duy nhất module trong import system. Với một module được thực thi trực tiếp, thuộc tính này sẽ được đặt thành ``"__main__"``.

   Thuộc tính này phải được đặt thành tên đầy đủ của module. Giá trị này được kỳ vọng khớp với giá trị của
   :attr:`module.__spec__.name <importlib.machinery.ModuleSpec.name>`.

.. attribute:: module.__spec__

   Bản ghi về trạng thái liên quan đến import system của module.

   Đặt thành :class:`module spec <importlib.machinery.ModuleSpec>` đã được dùng khi import module. Xem :ref:`module-specs` để biết thêm chi tiết.

   .. versionadded:: 3.4

.. attribute:: module.__package__

   :term:`package` mà một module thuộc về.

   Nếu module ở cấp cao nhất (nghĩa là không thuộc bất kỳ package cụ thể nào) thì thuộc tính này phải được đặt thành ``''`` (chuỗi rỗng). Nếu không, thuộc tính này phải được đặt thành tên package của module (có thể bằng
   :attr:`module.__name__` nếu bản thân module là một package). Xem :pep:`366` để biết thêm chi tiết.

   Thuộc tính này được dùng thay cho :attr:`~module.__name__` để tính các import tương đối tường minh cho các module chính. Theo mặc định, thuộc tính này là ``None`` đối với các module được tạo động bằng constructor :class:`types.ModuleType`; thay vào đó, hãy dùng :func:`importlib.util.module_from_spec` để bảo đảm thuộc tính được đặt thành một :class:`str`.

   Bạn **nên** sử dụng
   :attr:`module.__spec__.parent <importlib.machinery.ModuleSpec.parent>` thay vì :attr:`!module.__package__`. :attr:`__package__` hiện chỉ được dùng làm phương án dự phòng nếu :attr:`!__spec__.parent` chưa được đặt, và đường dẫn dự phòng này đã bị phản đối.

   .. versionchanged:: 3.4
      Thuộc tính này hiện mặc định là ``None`` đối với các module được tạo động bằng constructor :class:`types.ModuleType`. Trước đây, thuộc tính này là tùy chọn.

   .. versionchanged:: 3.6
      Giá trị của :attr:`!__package__` được kỳ vọng giống như
      :attr:`__spec__.parent <importlib.machinery.ModuleSpec.parent>`.
      :attr:`__package__` hiện chỉ được dùng làm phương án dự phòng trong quá trình phân giải import nếu :attr:`!__spec__.parent` chưa được định nghĩa.

   .. versionchanged:: 3.10
      :exc:`ImportWarning` is raised if an import resolution falls back to
      :attr:`!__package__` instead of
      :attr:`__spec__.parent <importlib.machinery.ModuleSpec.parent>`.

   .. versionchanged:: 3.12
      Phát sinh :exc:`DeprecationWarning` thay vì :exc:`ImportWarning` khi dùng :attr:`!__package__` làm phương án dự phòng trong quá trình phân giải import.

   .. deprecated-removed:: 3.13 3.15
      :attr:`!__package__` will cease to be set or taken into consideration
      bởi hệ thống import hoặc standard library.

.. attribute:: module.__loader__

   Đối tượng :term:`loader` mà cơ chế import đã dùng để tải module.

   Thuộc tính này chủ yếu hữu ích cho việc introspection, nhưng có thể được dùng cho chức năng bổ sung dành riêng cho loader, ví dụ như lấy dữ liệu liên kết với một loader.

   :attr:`!__loader__` mặc định là ``None`` đối với các module được tạo động bằng constructor :class:`types.ModuleType`; thay vào đó, hãy dùng :func:`importlib.util.module_from_spec` để bảo đảm thuộc tính được đặt thành một đối tượng :term:`loader`.

   Bạn **nên** sử dụng
   :attr:`module.__spec__.loader <importlib.machinery.ModuleSpec.loader>` thay vì :attr:`!module.__loader__`.

   .. versionchanged:: 3.4
      Thuộc tính này hiện mặc định là ``None`` đối với các module được tạo động bằng constructor :class:`types.ModuleType`. Trước đây, thuộc tính này là tùy chọn.

   .. deprecated-removed:: 3.12 3.16
      Việc đặt :attr:`!__loader__` trên một module nhưng không đặt
      :attr:`!__spec__.loader` đã lỗi thời. Trong Python 3.16,
      :attr:`!__loader__` sẽ không còn được hệ thống import hoặc thư viện chuẩn đặt hay xem xét.

.. attribute:: module.__path__

   Một :term:`sequence` chuỗi (có thể rỗng) liệt kê các vị trí nơi tìm thấy các submodule của package. Các module không phải package không nên có thuộc tính :attr:`!__path__`. Xem :ref:`package-path-rules` để biết thêm chi tiết.

   Bạn **nên** sử dụng
   :attr:`module.__spec__.submodule_search_locations <importlib.machinery.ModuleSpec.submodule_search_locations>` thay vì :attr:`!module.__path__`.

.. attribute:: module.__file__
.. attribute:: module.__cached__

   :attr:`!__file__` và :attr:`!__cached__` đều là các thuộc tính tùy chọn, có thể được thiết lập hoặc không. Cả hai thuộc tính nên là một :class:`str` khi khả dụng.

   :attr:`!__file__` cho biết pathname của tệp mà module được tải từ đó (nếu được tải từ một tệp), hoặc pathname của tệp shared library dành cho các extension module được tải động từ một shared library. Thuộc tính này có thể không có đối với một số loại module nhất định, chẳng hạn như các C module được liên kết tĩnh vào interpreter, và
   :ref:`import system <importsystem>` có thể chọn không thiết lập thuộc tính này nếu nó không có ý nghĩa ngữ nghĩa (ví dụ: một module được tải từ cơ sở dữ liệu).

   Nếu :attr:`!__file__` được thiết lập thì thuộc tính :attr:`!__cached__` cũng có thể được thiết lập, đây là đường dẫn đến bất kỳ phiên bản đã biên dịch nào của mã (ví dụ: một tệp đã byte-compiled). Tệp không cần tồn tại để thiết lập thuộc tính này; đường dẫn chỉ cần trỏ đến nơi tệp đã biên dịch *sẽ* tồn tại (xem :pep:`3147`).

   Lưu ý rằng :attr:`!__cached__` có thể được đặt ngay cả khi :attr:`!__file__` chưa được đặt. Tuy nhiên, tình huống đó khá không điển hình. Cuối cùng, việc
   :term:`loader` mới là điều khiến việc sử dụng module spec được cung cấp bởi
   :term:`finder` (từ đó :attr:`!__file__` và :attr:`!__cached__` được suy ra). Vì vậy, nếu một loader có thể tải từ một module đã được lưu trong bộ nhớ đệm nhưng ngoài trường hợp đó không tải từ tệp, thì tình huống không điển hình này có thể phù hợp.

   Bạn **nên** sử dụng
   :attr:`module.__spec__.cached <importlib.machinery.ModuleSpec.cached>` thay vì :attr:`!module.__cached__`.

   .. deprecated-removed:: 3.13 3.15
      Việc đặt :attr:`!__cached__` trên một module nhưng không đặt
      :attr:`!__spec__.cached` đã bị phản đối. Trong Python 3.15,
      :attr:`!__cached__` sẽ không còn được hệ thống import hoặc standard library thiết lập hay xem xét nữa.

Các thuộc tính có thể ghi khác trên đối tượng module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ngoài các thuộc tính liên quan đến import được liệt kê ở trên, đối tượng module cũng có các thuộc tính có thể ghi sau đây:

.. attribute:: module.__doc__

   Chuỗi tài liệu của module, hoặc ``None`` nếu không có. Xem thêm: :attr:`__doc__ attributes <definition.__doc__>`.

.. attribute:: module.__annotations__

   Một dictionary chứa :term:`các chú giải biến <variable annotation>` được thu thập trong quá trình thực thi phần thân module. Để biết các phương pháp tốt nhất khi làm việc với
   :attr:`!__annotations__`, xem :mod:`annotationlib`.

   .. versionchanged:: 3.14
      Các chú giải hiện được :ref:`đánh giá lười (lazily evaluated) <lazy-evaluation>`. Xem :pep:`649`.

.. attribute:: module.__annotate__

   :term:`annotate function` của mô-đun này, hoặc ``None`` nếu mô-đun không có annotation. Xem thêm: các thuộc tính :attr:`~object.__annotate__`.

   .. versionadded:: 3.14

Từ điển của mô-đun
^^^^^^^^^^^^^^^^^^

Các đối tượng mô-đun cũng có thuộc tính chỉ đọc đặc biệt sau:

.. index:: single: __dict__ (module attribute)
.. attribute:: module.__dict__

   Namespace của mô-đun dưới dạng một đối tượng từ điển. Không giống các thuộc tính khác được liệt kê ở đây, :attr:`!__dict__` không thể được truy cập như một biến toàn cục từ bên trong mô-đun; nó chỉ có thể được truy cập như một thuộc tính trên các đối tượng mô-đun.

   .. impl-detail::

      Do cách CPython xóa các từ điển mô-đun, từ điển mô-đun sẽ bị xóa khi mô-đun ra khỏi phạm vi ngay cả khi từ điển vẫn còn các tham chiếu đang hoạt động. Để tránh điều này, hãy sao chép từ điển hoặc giữ mô-đun tồn tại trong khi sử dụng trực tiếp từ điển của nó.


.. _class-attrs-and-methods:

Các lớp tùy chỉnh
-----------------

Các kiểu lớp tùy chỉnh thường được tạo bằng định nghĩa lớp (xem phần
:ref:`class`). Một lớp có một không gian tên được triển khai bằng đối tượng dictionary. Các tham chiếu thuộc tính của lớp được chuyển thành các thao tác tra cứu trong dictionary này, ví dụ, ``C.x`` được chuyển thành ``C.__dict__["x"]`` (mặc dù có một số hook cho phép dùng các cách khác để xác định vị trí thuộc tính). Khi không tìm thấy tên thuộc tính ở đó, việc tìm kiếm thuộc tính tiếp tục trong các lớp cơ sở. Việc tìm kiếm trong các lớp cơ sở này sử dụng thứ tự phân giải phương thức C3, hoạt động chính xác ngay cả khi có các cấu trúc kế thừa 'kim cương', trong đó nhiều đường dẫn kế thừa cùng dẫn trở lại một tổ tiên chung. Bạn có thể tìm thêm chi tiết về C3 MRO mà Python sử dụng tại
:ref:`python_2.3_mro`.

.. index::
   pair: object; class
   pair: object; class instance
   pair: object; instance
   pair: class object; call
   single: container
   pair: object; dictionary
   pair: class; attribute

Khi một tham chiếu thuộc tính của lớp (ví dụ đối với lớp :class:`!C`) sẽ cho ra một đối tượng class method, nó được chuyển thành một đối tượng instance method có
thuộc tính :attr:`~method.__self__` là :class:`!C`. Khi nó sẽ cho ra một đối tượng :class:`staticmethod`, nó được chuyển thành đối tượng được bao bọc bởi đối tượng static method. Xem phần :ref:`descriptors` để biết một cách khác mà các thuộc tính lấy từ một lớp có thể khác với những thuộc tính thực sự chứa trong
:attr:`~object.__dict__`.

.. index:: triple: class; attribute; assignment

Các phép gán thuộc tính lớp cập nhật dictionary của lớp, không bao giờ cập nhật dictionary của một lớp cơ sở.

.. index:: pair: class object; call

Một đối tượng lớp có thể được gọi (xem ở trên) để tạo ra một instance của lớp (xem bên dưới).

Các thuộc tính đặc biệt
^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: __name__ (class attribute)
   single: __module__ (class attribute)
   single: __dict__ (class attribute)
   single: __bases__ (class attribute)
   single: __base__ (class attribute)
   single: __doc__ (class attribute)
   single: __annotations__ (class attribute)
   single: __annotate__ (class attribute)
   single: __type_params__ (class attribute)
   single: __static_attributes__ (class attribute)
   single: __firstlineno__ (class attribute)

.. list-table::
   :header-rows: 1

   * - Thuộc tính
     - Ý nghĩa

   * - .. attribute:: type.__name__
     - Tên của lớp. Xem thêm: :attr:`__name__ attributes <definition.__name__>`.

   * - .. attribute:: type.__qualname__
     - :term:`qualified name` của lớp. Xem thêm: :attr:`__qualname__ attributes <definition.__qualname__>`.

   * - .. attribute:: type.__module__
     - Tên của module nơi lớp được định nghĩa.

   * - .. attribute:: type.__dict__
     - Một :class:`mapping proxy <types.MappingProxyType>` cung cấp chế độ xem chỉ đọc của namespace của lớp. Xem thêm: :attr:`__dict__ attributes <object.__dict__>`.

   * - .. attribute:: type.__bases__
     - Một :class:`tuple` chứa các lớp cơ sở của lớp. Trong hầu hết trường hợp, với một lớp được định nghĩa là ``class X(A, B, C)``, ``X.__bases__`` sẽ hoàn toàn bằng ``(A, B, C)``.

   * - .. attribute:: type.__base__
     - .. impl-detail::

          Lớp cơ sở duy nhất trong chuỗi kế thừa chịu trách nhiệm về bố cục bộ nhớ của các instance. Thuộc tính này tương ứng với
          :c:member:`~PyTypeObject.tp_base` ở cấp độ C.

   * - .. attribute:: type.__doc__
     - Chuỗi tài liệu của lớp, hoặc ``None`` nếu không được định nghĩa. Không được các lớp con kế thừa.

   * - .. attribute:: type.__annotations__
     - Một dictionary chứa
       :term:`các chú giải biến <variable annotation>` được thu thập trong quá trình thực thi thân lớp. Xem thêm:
       :attr:`__annotations__ attributes <object.__annotations__>`.

       Để biết các thực hành tốt nhất khi làm việc với :attr:`~object.__annotations__`, vui lòng xem :mod:`annotationlib`. Hãy dùng
       :func:`annotationlib.get_annotations` thay vì truy cập trực tiếp thuộc tính này.

       .. warning::

          Việc truy cập trực tiếp thuộc tính :attr:`!__annotations__` trên một đối tượng lớp có thể trả về các chú giải của nhầm lớp, cụ thể trong một số trường hợp khi lớp, lớp cơ sở của nó hoặc một metaclass được định nghĩa dưới ``from __future__ import annotations``. Xem :pep:`749 <749#pep749-metaclasses>` để biết chi tiết.

          Thuộc tính này không tồn tại trên một số lớp dựng sẵn. Trên các lớp do người dùng định nghĩa không có ``__annotations__``, đây là một từ điển rỗng.

       .. versionchanged:: 3.14
          Các annotation hiện được :ref:`đánh giá trì hoãn <lazy-evaluation>`. Xem :pep:`649`.

   * - .. method:: type.__annotate__
     - :term:`annotate function` của lớp này, hoặc ``None`` nếu lớp không có annotation. Xem thêm: :attr:`__annotate__ attributes <object.__annotate__>`.

       .. versionadded:: 3.14

   * - .. attribute:: type.__type_params__
     - Một :class:`tuple` chứa các :ref:`tham số kiểu <type-params>` của một :ref:`lớp generic <generic-classes>`.

       .. versionadded:: 3.12

   * - .. attribute:: type.__static_attributes__
     - Một :class:`tuple` chứa tên các thuộc tính của lớp này được gán thông qua ``self.X`` từ bất kỳ hàm nào trong thân lớp.

       .. versionadded:: 3.13

   * - .. attribute:: type.__firstlineno__
     - Số dòng của dòng đầu tiên trong định nghĩa lớp, bao gồm cả decorator. Việc thiết lập thuộc tính :attr:`~type.__module__` sẽ xóa
       mục :attr:`!__firstlineno__` khỏi từ điển của kiểu.

       .. versionadded:: 3.13

   * - .. attribute:: type.__mro__
     - :class:`tuple` của các lớp được xem xét khi tìm kiếm các lớp cơ sở trong quá trình phân giải phương thức.


Các phương thức đặc biệt
^^^^^^^^^^^^^^^^^^^^^^^^

Ngoài các thuộc tính đặc biệt được mô tả ở trên, mọi lớp Python cũng có sẵn hai phương thức sau:

.. method:: type.mro

   Phương thức này có thể được metaclass ghi đè để tùy chỉnh thứ tự phân giải phương thức cho các instance của nó. Phương thức này được gọi khi khởi tạo lớp, và kết quả của nó được lưu trong :attr:`~type.__mro__`.

.. method:: type.__subclasses__

   Mỗi lớp duy trì một danh sách các weak reference đến các lớp con trực tiếp của nó. Phương thức này trả về một danh sách gồm tất cả các reference đó vẫn còn tồn tại. Danh sách theo thứ tự định nghĩa. Ví dụ:

   .. doctest::

      >>> class A: pass
      >>> class B(A): pass
      >>> A.__subclasses__()
      [<class 'B'>]

Các instance của lớp
--------------------

.. index::
   pair: object; class instance
   pair: object; instance
   pair: class; instance
   pair: class instance; attribute

Một instance của lớp được tạo bằng cách gọi một đối tượng lớp (xem ở trên). Một instance của lớp có một namespace được triển khai dưới dạng dictionary, đây là nơi đầu tiên được tìm kiếm khi tham chiếu thuộc tính. Khi không tìm thấy một thuộc tính ở đó và lớp của instance có thuộc tính mang tên đó, quá trình tìm kiếm tiếp tục với các thuộc tính của lớp. Nếu tìm thấy một thuộc tính lớp là đối tượng hàm do người dùng định nghĩa, nó sẽ được chuyển đổi thành một đối tượng phương thức instance có thuộc tính :attr:`~method.__self__` là instance đó. Các đối tượng static method và class method cũng được chuyển đổi; xem phần "Classes" ở trên. Xem phần :ref:`descriptors` để biết một cách khác mà các thuộc tính của một lớp được truy xuất thông qua các instance của lớp đó có thể khác với các đối tượng thực sự được lưu trong :attr:`~object.__dict__` của lớp. Nếu không tìm thấy thuộc tính lớp nào và lớp của đối tượng có phương thức :meth:`~object.__getattr__`, phương thức đó sẽ được gọi để đáp ứng việc tra cứu.

.. index:: triple: class instance; attribute; assignment

Việc gán và xóa thuộc tính cập nhật dictionary của instance, không bao giờ cập nhật dictionary của class. Nếu class có một :meth:`~object.__setattr__` hoặc
phương thức :meth:`~object.__delattr__`, phương thức này sẽ được gọi thay vì cập nhật trực tiếp dictionary của instance.

.. index::
   pair: object; numeric
   pair: object; sequence
   pair: object; mapping

Các instance của class có thể hoạt động như số, sequence hoặc mapping nếu chúng có các phương thức mang những tên đặc biệt nhất định. Xem mục :ref:`specialnames`.

Các thuộc tính đặc biệt
^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: __dict__ (instance attribute)
   single: __class__ (instance attribute)

.. attribute:: object.__class__

   Class mà một instance của class thuộc về.

.. attribute:: object.__dict__

   Một dictionary hoặc đối tượng mapping khác được dùng để lưu trữ các thuộc tính (có thể ghi) của một object. Không phải mọi instance đều có thuộc tính :attr:`!__dict__`; xem mục về :ref:`slots` để biết thêm chi tiết.


Các đối tượng I/O (còn được gọi là file object)
-----------------------------------------------

.. index::
   pair: built-in function; open
   pair: module; io
   single: popen() (in module os)
   single: makefile() (socket method)
   single: sys.stdin
   single: sys.stdout
   single: sys.stderr
   single: stdio
   single: stdin (in module sys)
   single: stdout (in module sys)
   single: stderr (in module sys)

Một :term:`file object` đại diện cho một tệp đang mở. Có nhiều lối tắt để tạo đối tượng tệp: hàm dựng sẵn :func:`open`, cùng với :func:`os.popen`, :func:`os.fdopen` và
phương thức :meth:`~socket.socket.makefile` của các đối tượng socket (và có thể bởi các hàm hoặc phương thức khác do các extension module cung cấp).

Các đối tượng tệp triển khai các phương thức phổ biến, được liệt kê bên dưới, để đơn giản hóa việc sử dụng trong mã generic. Chúng được kỳ vọng là :ref:`context-managers`.

Các đối tượng ``sys.stdin``, ``sys.stdout`` và ``sys.stderr`` được khởi tạo thành các đối tượng tệp tương ứng với các luồng đầu vào, đầu ra và lỗi chuẩn của interpreter; tất cả đều được mở ở text mode và do đó tuân theo interface do abstract class :class:`io.TextIOBase` xác định.

.. method:: file.read(size=-1, /)

   Lấy tối đa *size* dữ liệu từ tệp. Để thuận tiện, nếu *size* không được chỉ định hoặc là -1, hãy lấy toàn bộ dữ liệu hiện có.

.. method:: file.write(data, /)

   Lưu *data* vào tệp.

.. method:: file.close()

   Flush mọi buffer và đóng tệp bên dưới.


Các kiểu nội bộ
---------------

.. index::
   single: internal type
   single: types, internal

Một vài kiểu được trình thông dịch sử dụng nội bộ được cung cấp cho người dùng. Định nghĩa của chúng có thể thay đổi trong các phiên bản trình thông dịch sau này, nhưng chúng được đề cập ở đây để đảm bảo tính đầy đủ.


.. _code-objects:

Đối tượng mã
^^^^^^^^^^^^

.. index:: bytecode, object; code, code object

Đối tượng mã biểu diễn mã Python thực thi đã được *biên dịch thành bytecode*, hoặc :term:`bytecode`. Điểm khác biệt giữa đối tượng mã và đối tượng hàm là đối tượng hàm chứa một tham chiếu tường minh đến globals của hàm (module nơi hàm được định nghĩa), trong khi đối tượng mã không chứa ngữ cảnh nào; ngoài ra, các giá trị đối số mặc định được lưu trong đối tượng hàm, không phải trong đối tượng mã (vì chúng biểu diễn các giá trị được tính tại run-time). Không giống đối tượng hàm, đối tượng mã là bất biến và không chứa tham chiếu nào (trực tiếp hoặc gián tiếp) đến các đối tượng có thể thay đổi.

.. index::
   single: co_argcount (code object attribute)
   single: co_posonlyargcount (code object attribute)
   single: co_kwonlyargcount (code object attribute)
   single: co_code (code object attribute)
   single: co_consts (code object attribute)
   single: co_filename (code object attribute)
   single: co_firstlineno (code object attribute)
   single: co_flags (code object attribute)
   single: co_lnotab (code object attribute)
   single: co_name (code object attribute)
   single: co_names (code object attribute)
   single: co_nlocals (code object attribute)
   single: co_stacksize (code object attribute)
   single: co_varnames (code object attribute)
   single: co_cellvars (code object attribute)
   single: co_freevars (code object attribute)
   single: co_qualname (code object attribute)

Các thuộc tính chỉ đọc đặc biệt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::

   * - .. attribute:: codeobject.co_name
     - Tên hàm

   * - .. attribute:: codeobject.co_qualname
     - Tên đầy đủ của hàm

       .. versionadded:: 3.11

   * - .. attribute:: codeobject.co_argcount
     - Tổng số :term:`tham số <parameter>` vị trí (bao gồm tham số chỉ vị trí và tham số có giá trị mặc định) mà hàm có

   * - .. attribute:: codeobject.co_posonlyargcount
     - Số :term:`tham số <parameter>` chỉ vị trí (bao gồm đối số có giá trị mặc định) mà hàm có

   * - .. attribute:: codeobject.co_kwonlyargcount
     - Số :term:`tham số <parameter>` chỉ từ khóa (bao gồm đối số có giá trị mặc định) mà hàm có

   * - .. attribute:: codeobject.co_nlocals
     - Số :ref:`biến cục bộ <naming>` được hàm sử dụng (bao gồm cả tham số)

   * - .. attribute:: codeobject.co_varnames
     - Một :class:`tuple` chứa tên của các biến cục bộ trong hàm (bắt đầu bằng tên tham số)

   * - .. attribute:: codeobject.co_cellvars
     - Một :class:`tuple` chứa tên của các :ref:`biến cục bộ <naming>` được tham chiếu từ ít nhất một :term:`nested scope` bên trong hàm

   * - .. attribute:: codeobject.co_freevars
     - Một :class:`tuple` chứa tên của
       :term:`các biến tự do (closure) <closure variable>` mà một :term:`nested scope` tham chiếu trong phạm vi bên ngoài. Xem thêm :attr:`function.__closure__`.

       Lưu ý: các tham chiếu đến tên global và builtin *không* được bao gồm.

   * - .. attribute:: codeobject.co_code
     - Một chuỗi biểu thị dãy lệnh :term:`bytecode` trong hàm

   * - .. attribute:: codeobject.co_consts
     - Một :class:`tuple` chứa các literal được :term:`bytecode` trong hàm sử dụng

   * - .. attribute:: codeobject.co_names
     - Một :class:`tuple` chứa các tên được :term:`bytecode` trong hàm sử dụng

   * - .. attribute:: codeobject.co_filename
     - Tên của tệp mà mã được biên dịch từ đó

   * - .. attribute:: codeobject.co_firstlineno
     - Số dòng của dòng đầu tiên của hàm

   * - .. attribute:: codeobject.co_lnotab
     - Một chuỗi mã hóa ánh xạ từ các độ lệch :term:`bytecode` sang số dòng. Để biết chi tiết, hãy xem mã nguồn của interpreter.

       .. deprecated:: 3.12
          Thuộc tính này của các code object đã bị phản đối và có thể bị loại bỏ trong Python 3.15.

   * - .. attribute:: codeobject.co_linetable
     - Một object :class:`bytes` chứa thông tin vị trí nguồn đã được mã hóa. Định dạng chính xác là một chi tiết triển khai và có thể thay đổi giữa các phiên bản Python. Hãy dùng :meth:`~codeobject.co_lines` và
       :meth:`~codeobject.co_positions` để truy cập thông tin về dòng và vị trí theo cách được hỗ trợ. Để tạo một bản sao đã sửa đổi của code object, hãy dùng :meth:`~codeobject.replace`.

       .. versionadded:: 3.10

   * - .. attribute:: codeobject.co_stacksize
     - Kích thước stack cần thiết của code object

   * - .. attribute:: codeobject.co_flags
     - Một :class:`integer <int>` mã hóa một số cờ cho interpreter.

.. index:: pair: object; generator

Các bit cờ sau được định nghĩa cho :attr:`~codeobject.co_flags`: bit ``0x04`` được đặt nếu hàm sử dụng cú pháp ``*arguments`` để chấp nhận số lượng tùy ý đối số vị trí; bit ``0x08`` được đặt nếu hàm sử dụng cú pháp ``**keywords`` để chấp nhận các đối số từ khóa tùy ý; bit ``0x20`` được đặt nếu hàm là một generator. Xem :ref:`inspect-module-co-flags` để biết chi tiết về ngữ nghĩa của từng cờ có thể xuất hiện.

Các khai báo tính năng tương lai (ví dụ: ``from __future__ import division``) cũng sử dụng các bit trong :attr:`~codeobject.co_flags` để cho biết liệu một đối tượng mã có được biên dịch với một tính năng cụ thể được bật hay không. Xem :attr:`~__future__._Feature.compiler_flag`.

Các bit khác trong :attr:`~codeobject.co_flags` được dành riêng cho mục đích sử dụng nội bộ.

.. index:: single: documentation string

Nếu một đối tượng mã biểu diễn một hàm và có docstring, bit :data:`~inspect.CO_HAS_DOCSTRING` được đặt trong :attr:`~codeobject.co_flags` và mục đầu tiên trong :attr:`~codeobject.co_consts` là docstring của hàm.

Các phương thức trên đối tượng mã
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: codeobject.co_positions()

   Trả về một iterable qua các vị trí mã nguồn của từng lệnh :term:`bytecode` trong đối tượng mã.

   Iterator trả về :class:`tuple`\s chứa ``(start_line, end_line, start_column, end_column)``. Bộ tuple thứ *i-th* tương ứng với vị trí của mã nguồn đã được biên dịch thành đơn vị mã thứ *i-th*. Thông tin cột là các offset byte utf-8 đánh chỉ mục từ 0 trên dòng mã nguồn đã cho.

   Thông tin vị trí này có thể bị thiếu. Danh sách không đầy đủ các trường hợp có thể xảy ra điều này:

   - Chạy trình thông dịch với :option:`-X` ``no_debug_ranges``.
   - Tải tệp pyc đã được biên dịch khi sử dụng :option:`-X` ``no_debug_ranges``.
   - Các bộ tuple vị trí tương ứng với các chỉ thị nhân tạo.
   - Các số dòng và cột không thể biểu diễn do những giới hạn đặc thù của phần triển khai.

   Khi điều này xảy ra, một số hoặc toàn bộ phần tử của bộ tuple có thể là
   :const:`None`.

   .. versionadded:: 3.11

   .. note::
      Tính năng này yêu cầu lưu trữ vị trí cột trong các code object, điều này có thể làm tăng nhẹ dung lượng đĩa mà các tệp Python đã biên dịch sử dụng hoặc mức sử dụng bộ nhớ của trình thông dịch. Để tránh lưu trữ thông tin bổ sung và/hoặc vô hiệu hóa việc in thông tin traceback bổ sung,
      Có thể sử dụng cờ dòng lệnh :option:`-X` ``no_debug_ranges`` hoặc biến môi trường :envvar:`PYTHONNODEBUGRANGES`.

.. method:: codeobject.co_lines()

   Trả về một iterator cung cấp thông tin về các phạm vi liên tiếp của
   :term:`bytecode`\s. Mỗi mục được cung cấp là một ``(start, end, lineno)``
   :class:`tuple`:

   * ``start`` (một :class:`int`) biểu thị offset (bao gồm) của điểm bắt đầu phạm vi :term:`bytecode`
   * ``end`` (một :class:`int`) biểu thị offset (không bao gồm) của điểm kết thúc phạm vi :term:`bytecode`
   * ``lineno`` là một :class:`int` biểu thị số dòng của
     phạm vi :term:`bytecode`, hoặc ``None`` nếu các bytecode trong phạm vi đã cho không có số dòng

   Các mục được cung cấp sẽ có các thuộc tính sau:

   * Phạm vi đầu tiên được trả về sẽ có ``start`` bằng 0.
   * Các phạm vi ``(start, end)`` sẽ không giảm và liên tiếp. Nghĩa là, với bất kỳ cặp :class:`tuple`\s nào, ``start`` của phạm vi thứ hai sẽ bằng ``end`` của phạm vi thứ nhất.
   * Không có phạm vi nào đi lùi: ``end >= start`` đối với mọi bộ ba.
   * :class:`tuple` cuối cùng được trả về sẽ có ``end`` bằng kích thước của
     :term:`bytecode`.

   Các phạm vi có độ rộng bằng 0, trong đó ``start == end``, được cho phép. Các phạm vi có độ rộng bằng 0 được dùng cho những dòng có mặt trong mã nguồn nhưng đã bị compiler :term:`bytecode` loại bỏ.

   .. versionadded:: 3.10

   .. seealso::

      :pep:`626` - Số dòng chính xác để debug và cho các công cụ khác.
         PEP đã giới thiệu phương thức :meth:`!co_lines`.

.. method:: codeobject.replace(**kwargs)

   Trả về một bản sao của đối tượng code với các giá trị mới cho những trường được chỉ định.

   Đối tượng code cũng được hỗ trợ bởi hàm tổng quát :func:`copy.replace`.

   .. versionadded:: 3.8


.. _frame-objects:

Đối tượng frame
^^^^^^^^^^^^^^^

.. index:: pair: object; frame

Đối tượng frame biểu diễn các frame thực thi. Chúng có thể xuất hiện trong
:ref:`đối tượng traceback <traceback-objects>`, và cũng được truyền đến các hàm trace đã đăng ký.

.. index::
   single: f_back (frame attribute)
   single: f_code (frame attribute)
   single: f_globals (frame attribute)
   single: f_locals (frame attribute)
   single: f_lasti (frame attribute)
   single: f_builtins (frame attribute)
   single: f_generator (frame attribute)

Các thuộc tính chỉ đọc đặc biệt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::

   * - .. attribute:: frame.f_back
     - Trỏ đến stack frame trước đó (về phía caller), hoặc ``None`` nếu đây là stack frame ở đáy

   * - .. attribute:: frame.f_code
     - Đối tượng :ref:`code object <code-objects>` đang được thực thi trong frame này. Việc truy cập thuộc tính này tạo ra một :ref:`auditing event <auditing>` ``object.__getattr__`` với các đối số ``obj`` và ``"f_code"``.

   * - .. attribute:: frame.f_locals
     - Ánh xạ được frame dùng để tra cứu
       :ref:`các biến cục bộ <naming>`. Nếu frame tham chiếu đến một :term:`optimized scope`, điều này có thể trả về một đối tượng proxy ghi xuyên.

       .. versionchanged:: 3.13
          Trả về một proxy cho các scope được tối ưu hóa.

   * - .. attribute:: frame.f_globals
     - Từ điển được frame dùng để tra cứu
       :ref:`các biến toàn cục <naming>`

   * - .. attribute:: frame.f_builtins
     - Từ điển được frame dùng để tra cứu
       :ref:`các tên dựng sẵn (nội tại) <naming>`

   * - .. attribute:: frame.f_lasti
     - "Lệnh chính xác" của đối tượng frame (đây là một chỉ mục vào chuỗi :term:`bytecode` của
       :ref:`đối tượng code <code-objects>`)"

   * - .. attribute:: frame.f_generator
     - Đối tượng :term:`generator` hoặc :term:`coroutine` sở hữu frame này, hoặc ``None`` nếu frame là một hàm thông thường.

       .. versionadded:: 3.14

.. index::
   single: f_trace (frame attribute)
   single: f_trace_lines (frame attribute)
   single: f_trace_opcodes (frame attribute)
   single: f_lineno (frame attribute)

Các thuộc tính đặc biệt có thể ghi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::

   * - .. attribute:: frame.f_trace
     - Nếu không phải ``None``, đây là một hàm được gọi cho nhiều sự kiện khác nhau trong quá trình thực thi code (được các debugger sử dụng). Thông thường, một sự kiện được kích hoạt cho mỗi dòng mã nguồn mới (xem :attr:`~frame.f_trace_lines`).

   * - .. attribute:: frame.f_trace_lines
     - Đặt thuộc tính này thành :const:`False` để vô hiệu hóa việc kích hoạt sự kiện tracing cho mỗi dòng mã nguồn.

   * - .. attribute:: frame.f_trace_opcodes
     - Đặt thuộc tính này thành :const:`True` để cho phép yêu cầu các event theo từng opcode. Lưu ý rằng điều này có thể dẫn đến hành vi interpreter không xác định nếu các exception do hàm trace phát sinh thoát ra khỏi hàm đang được trace.

   * - .. attribute:: frame.f_lineno
     - Số dòng hiện tại của frame -- việc ghi vào thuộc tính này từ bên trong một hàm trace sẽ nhảy đến dòng đã cho (chỉ áp dụng cho frame ở dưới cùng). Debugger có thể triển khai lệnh Jump (còn gọi là Set Next Statement) bằng cách ghi vào thuộc tính này.

Các phương thức của đối tượng frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Các đối tượng frame hỗ trợ một phương thức:

.. method:: frame.clear()

   Phương thức này xóa mọi tham chiếu đến :ref:`biến cục bộ <naming>` được frame giữ lại. Ngoài ra, nếu frame thuộc về một :term:`generator`, generator sẽ được hoàn tất. Điều này giúp phá vỡ các chu trình tham chiếu liên quan đến đối tượng frame (ví dụ, khi bắt một :ref:`exception <bltin-exceptions>` và lưu :ref:`traceback <traceback-objects>` của nó để sử dụng sau).

   :exc:`RuntimeError` được phát sinh nếu frame hiện đang thực thi hoặc bị tạm dừng.

   .. versionadded:: 3.4

   .. versionchanged:: 3.13
      Cố gắng xóa một frame đang tạm dừng sẽ phát sinh :exc:`RuntimeError` (điều này vốn luôn xảy ra đối với các frame đang thực thi).


.. _traceback-objects:

Đối tượng traceback
^^^^^^^^^^^^^^^^^^^

.. index::
   pair: object; traceback
   pair: stack; trace
   pair: exception; handler
   pair: execution; stack
   single: exc_info (in module sys)
   single: last_traceback (in module sys)
   single: sys.exc_info
   single: sys.exception
   single: sys.last_traceback

Đối tượng traceback biểu diễn stack trace của một :ref:`exception <tut-errors>`. Một đối tượng traceback được tạo ngầm khi xảy ra exception, và cũng có thể được tạo tường minh bằng cách gọi :class:`types.TracebackType`.

.. versionchanged:: 3.7
   Các đối tượng traceback giờ đây có thể được khởi tạo tường minh từ mã Python.

Đối với các traceback được tạo ngầm, khi việc tìm kiếm exception handler tháo ngăn xếp thực thi, tại mỗi cấp được tháo, một đối tượng traceback được chèn vào trước traceback hiện tại. Khi đi vào một exception handler, stack trace sẽ được cung cấp cho chương trình. (Xem phần
:ref:`try`.) Nó có thể được truy cập dưới dạng phần tử thứ ba của tuple được trả về bởi :func:`sys.exc_info`, và dưới dạng thuộc tính
:attr:`~BaseException.__traceback__` của exception đã được bắt.

Khi chương trình không có handler phù hợp, stack trace được ghi (với định dạng đẹp) vào luồng lỗi chuẩn; nếu interpreter ở chế độ tương tác, nó cũng được cung cấp cho người dùng dưới dạng :data:`sys.last_traceback`.

Đối với các traceback được tạo tường minh, người tạo traceback sẽ tự quyết định cách liên kết các thuộc tính :attr:`~traceback.tb_next` để tạo thành một stack trace hoàn chỉnh.

.. index::
   single: tb_frame (traceback attribute)
   single: tb_lineno (traceback attribute)
   single: tb_lasti (traceback attribute)
   pair: statement; try

Các thuộc tính chỉ đọc đặc biệt:

.. list-table::

   * - .. attribute:: traceback.tb_frame
     - Trỏ đến :ref:`frame <frame-objects>` thực thi của cấp hiện tại.

       Việc truy cập thuộc tính này sẽ phát sinh một
       :ref:`sự kiện auditing <auditing>` ``object.__getattr__`` với các đối số ``obj`` và ``"tb_frame"``.

   * - .. attribute:: traceback.tb_lineno
     - Cho biết số dòng nơi ngoại lệ xảy ra

   * - .. attribute:: traceback.tb_lasti
     - Cho biết "lệnh chính xác".

Số dòng và lệnh cuối cùng trong traceback có thể khác với số dòng của :ref:`đối tượng frame <frame-objects>` của nó nếu ngoại lệ xảy ra trong một
câu lệnh :keyword:`try` không có mệnh đề except tương ứng hoặc có một
mệnh đề :keyword:`finally`.

.. index::
   single: tb_next (traceback attribute)

.. attribute:: traceback.tb_next

   Thuộc tính đặc biệt có thể ghi :attr:`!tb_next` là cấp tiếp theo trong stack trace (hướng về frame nơi xảy ra ngoại lệ), hoặc ``None`` nếu không có cấp tiếp theo.

   .. versionchanged:: 3.7
      Thuộc tính này hiện có thể ghi được


Đối tượng slice
^^^^^^^^^^^^^^^

.. index:: pair: built-in function; slice

Đối tượng slice được dùng để biểu diễn các lát cắt cho
các phương thức :meth:`~object.__getitem__`. Chúng cũng được tạo bởi hàm dựng sẵn :func:`slice`.

.. index::
   single: start (slice object attribute)
   single: stop (slice object attribute)
   single: step (slice object attribute)

Các thuộc tính đặc biệt chỉ đọc: :attr:`~slice.start` là cận dưới;
:attr:`~slice.stop` là cận trên; :attr:`~slice.step` là giá trị bước; mỗi giá trị là ``None`` nếu bị bỏ qua. Các thuộc tính này có thể thuộc bất kỳ kiểu nào.

Các đối tượng slice hỗ trợ một phương thức:

.. method:: slice.indices(self, length)

   Phương thức này nhận một đối số số nguyên duy nhất *length* và tính toán thông tin về slice mà đối tượng slice sẽ mô tả nếu được áp dụng cho một sequence gồm *length* phần tử. Nó trả về một tuple gồm ba số nguyên; lần lượt là các chỉ mục *start* và *stop*, cùng *step* hoặc độ dài stride của slice. Các chỉ mục bị thiếu hoặc nằm ngoài giới hạn được xử lý theo cách nhất quán với các slice thông thường.


Các đối tượng phương thức tĩnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các đối tượng phương thức tĩnh cung cấp cách ngăn việc chuyển đổi các đối tượng hàm thành đối tượng phương thức được mô tả ở trên. Một đối tượng phương thức tĩnh là một wrapper bao quanh bất kỳ đối tượng nào khác, thường là một đối tượng phương thức do người dùng định nghĩa. Khi một đối tượng phương thức tĩnh được lấy từ một lớp hoặc một instance của lớp, đối tượng thực sự được trả về là đối tượng được bọc, đối tượng này không chịu bất kỳ sự chuyển đổi nào thêm. Các đối tượng phương thức tĩnh cũng có thể gọi được. Các đối tượng phương thức tĩnh được tạo bởi constructor dựng sẵn :func:`staticmethod`.


Các đối tượng phương thức lớp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một đối tượng phương thức lớp, giống như một đối tượng phương thức tĩnh, là một trình bao bọc quanh một đối tượng khác, làm thay đổi cách đối tượng đó được truy xuất từ các lớp và các thể hiện của lớp. Hành vi của các đối tượng phương thức lớp khi được truy xuất như vậy được mô tả ở trên, trong phần :ref:`"phương thức thể hiện" <instance-methods>`. Các đối tượng phương thức lớp được tạo bởi constructor tích hợp sẵn :func:`classmethod`.


.. _specialnames:

Tên phương thức đặc biệt
========================

.. index::
   pair: operator; overloading
   single: __getitem__() (mapping object method)

Một lớp có thể triển khai một số thao tác nhất định được gọi bằng cú pháp đặc biệt (chẳng hạn như các phép toán số học hoặc truy cập chỉ số và lát cắt) bằng cách định nghĩa các phương thức có tên đặc biệt. Đây là cách Python tiếp cận :dfn:`nạp chồng toán tử`, cho phép các lớp tự định nghĩa hành vi của chúng đối với các toán tử ngôn ngữ. Ví dụ, nếu một lớp định nghĩa một phương thức có tên là
:meth:`~object.__getitem__`, và ``x`` là một thể hiện của lớp này, thì ``x[i]`` gần tương đương với ``type(x).__getitem__(x, i)``. Ngoại trừ những trường hợp được đề cập, các nỗ lực thực hiện một thao tác sẽ phát sinh ngoại lệ khi không có phương thức phù hợp nào được định nghĩa (thông thường là
:exc:`AttributeError` hoặc :exc:`TypeError`).

Đặt một phương thức đặc biệt thành ``None`` cho biết thao tác tương ứng không khả dụng. Ví dụ, nếu một lớp đặt
Từ :meth:`~object.__iter__` đến ``None``, lớp không thể lặp, vì vậy việc gọi
:func:`iter` trên các instance của nó sẽ phát sinh :exc:`TypeError` (mà không quay về dùng :meth:`~object.__getitem__`). [#]_

Khi triển khai một lớp mô phỏng bất kỳ kiểu dựng sẵn nào, điều quan trọng là chỉ triển khai việc mô phỏng ở mức độ phù hợp với đối tượng đang được mô hình hóa. Ví dụ, một số sequence có thể hoạt động tốt khi truy xuất từng phần tử riêng lẻ, nhưng việc trích xuất một slice có thể không hợp lý. (Một ví dụ là interface :ref:`NodeList <dom-nodelist-objects>` trong Document Object Model của W3C.)


.. _customization:

Tùy biến cơ bản
---------------

.. method:: object.__new__(cls[, ...])

   .. index:: pair: subclassing; immutable types

   Được gọi để tạo một instance mới của lớp *cls*. :meth:`__new__` là một static method (được xử lý đặc biệt nên bạn không cần khai báo nó như vậy), nhận lớp mà instance được yêu cầu tạo làm đối số đầu tiên. Các đối số còn lại là những đối số được truyền vào biểu thức constructor của đối tượng (lời gọi đến lớp). Giá trị trả về của :meth:`__new__` phải là instance đối tượng mới (thường là một instance của *cls*).

   Các cách triển khai điển hình tạo một instance mới của lớp bằng cách gọi method :meth:`__new__` của superclass thông qua ``super().__new__(cls[, ...])`` với các đối số phù hợp, rồi sửa đổi instance mới tạo khi cần trước khi trả về nó.

   Nếu :meth:`__new__` được gọi trong quá trình khởi tạo đối tượng và nó trả về một instance của *cls*, thì method :meth:`__init__` của instance mới sẽ được gọi như ``__init__(self[, ...])``, trong đó *self* là instance mới và các đối số còn lại giống với những đối số đã được truyền vào constructor của đối tượng.

   Nếu :meth:`__new__` không trả về một instance của *cls*, thì :meth:`__new__` của instance mới
   Phương thức :meth:`__init__` sẽ không được gọi.

   :meth:`__new__` chủ yếu được dùng để cho phép các lớp con của những kiểu bất biến (như int, str hoặc tuple) tùy chỉnh việc tạo instance. Nó cũng thường được override trong các metaclass tùy chỉnh để tùy chỉnh việc tạo lớp.


.. method:: object.__init__(self[, ...])

   .. index:: pair: class; constructor

   Được gọi sau khi instance đã được tạo (bởi :meth:`__new__`), nhưng trước khi được trả về cho caller. Các đối số là những đối số được truyền vào biểu thức constructor của lớp. Nếu một lớp cơ sở có phương thức :meth:`__init__`, thì phương thức :meth:`__init__` của lớp dẫn xuất, nếu có, phải gọi rõ ràng phương thức đó để bảo đảm phần thuộc lớp cơ sở của instance được khởi tạo đúng cách; ví dụ: ``super().__init__([args...])``.

   Vì :meth:`__new__` và :meth:`__init__` phối hợp với nhau khi xây dựng object (:meth:`__new__` để tạo object và :meth:`__init__` để tùy chỉnh object), :meth:`__init__` không được trả về bất kỳ giá trị nào khác ngoài ``None``; nếu làm vậy, một :exc:`TypeError` sẽ được phát sinh tại runtime.


.. method:: object.__del__(self)

   .. index::
      single: destructor
      single: finalizer
      pair: statement; del

   Được gọi khi instance sắp bị hủy. Đây cũng được gọi là finalizer hoặc (không chính xác) destructor. Nếu một lớp cơ sở có một
   phương thức :meth:`__del__`, thì phương thức :meth:`__del__` của lớp dẫn xuất, nếu có, phải gọi rõ ràng phương thức đó để bảo đảm phần thuộc lớp cơ sở của instance được xóa đúng cách.

   Có thể (mặc dù không được khuyến nghị!) để phương thức :meth:`__del__` trì hoãn việc hủy instance bằng cách tạo một reference mới đến nó. Điều này được gọi là *hồi sinh* object. Việc :meth:`__del__` có được gọi lần thứ hai khi một object đã hồi sinh sắp bị hủy hay không phụ thuộc vào implementation; implementation :term:`CPython` hiện tại chỉ gọi nó một lần.

   Không có gì đảm bảo rằng các phương thức :meth:`__del__` được gọi cho những object vẫn còn tồn tại khi interpreter thoát.
   :class:`weakref.finalize` cung cấp một cách trực tiếp để đăng ký một hàm dọn dẹp được gọi khi một object được garbage collected.

   .. note::

      ``del x`` không gọi trực tiếp ``x.__del__()`` --- phương thức trước giảm reference count của ``x`` đi một, và phương thức sau chỉ được gọi khi reference count của ``x`` đạt đến không.

   .. impl-detail::
      Có thể một reference cycle ngăn reference count của một object giảm về không. Trong trường hợp này, cycle sau đó sẽ được :term:`cyclic garbage collector <garbage collection>` phát hiện và xóa. Một nguyên nhân phổ biến của reference cycle là khi một exception đã được bắt trong một biến local. Khi đó, các local của frame reference đến exception, exception reference đến traceback của chính nó, và traceback reference đến các local của mọi frame được bắt trong traceback.

      .. seealso::
         Tài liệu cho module :mod:`gc`.

   .. warning::

      Do các tình huống không ổn định mà trong đó các phương thức :meth:`__del__` được gọi, các exception xảy ra trong quá trình thực thi chúng sẽ bị bỏ qua và thay vào đó một cảnh báo được in ra ``sys.stderr``. Cụ thể:

      * :meth:`__del__` có thể được gọi khi mã tùy ý đang được thực thi, kể cả từ bất kỳ thread tùy ý nào. Nếu :meth:`__del__` cần lấy lock hoặc gọi bất kỳ tài nguyên chặn nào khác, nó có thể bị deadlock vì tài nguyên đó có thể đã được mã bị ngắt để thực thi :meth:`__del__` chiếm giữ.

      * :meth:`__del__` có thể được thực thi trong quá trình interpreter tắt. Do đó, các biến global mà nó cần truy cập (bao gồm cả các module khác) có thể đã bị xóa hoặc được đặt thành ``None``. Python đảm bảo rằng các global có tên bắt đầu bằng một dấu gạch dưới sẽ bị xóa khỏi module của chúng trước khi các global khác bị xóa; nếu không có tham chiếu nào khác đến các global đó, điều này có thể giúp đảm bảo rằng các module đã import vẫn khả dụng tại thời điểm phương thức
        :meth:`__del__` được gọi.


   .. index::
      single: repr() (built-in function); __repr__() (object method)

.. method:: object.__repr__(self)

   Được hàm built-in :func:`repr` gọi để tính biểu diễn chuỗi "chính thức" của một đối tượng. Nếu có thể, biểu diễn này nên trông như một biểu thức Python hợp lệ có thể dùng để tạo lại một đối tượng có cùng giá trị (trong một môi trường phù hợp). Nếu không thể, nên trả về một chuỗi có dạng ``<...some useful description...>``. Giá trị trả về phải là một đối tượng chuỗi. Nếu một class định nghĩa :meth:`__repr__` nhưng không định nghĩa :meth:`__str__`, thì :meth:`__repr__` cũng được dùng khi cần biểu diễn chuỗi "không chính thức" cho các instance của class đó.

   Điều này thường được dùng để debugging, vì vậy điều quan trọng là biểu diễn phải giàu thông tin và không mơ hồ. Một implementation mặc định được cung cấp bởi chính class
   :class:`object`.

   .. index::
      single: string; __str__() (object method)
      single: format() (built-in function); __str__() (object method)
      single: print() (built-in function); __str__() (object method)


.. method:: object.__str__(self)

   Được :func:`str(object) <str>`, implementation :meth:`__format__` mặc định và hàm built-in :func:`print` gọi để tính biểu diễn chuỗi "không chính thức" hoặc có thể in đẹp của một đối tượng. Giá trị trả về phải là một
   Đối tượng :ref:`str <textseq>`.

   Phương thức này khác với :meth:`object.__repr__` ở chỗ không yêu cầu :meth:`__str__` trả về một biểu thức Python hợp lệ: có thể dùng một biểu diễn thuận tiện hoặc ngắn gọn hơn.

   Cách triển khai mặc định do kiểu dựng sẵn :class:`object` xác định sẽ gọi :meth:`object.__repr__`.

   .. XXX what about subclasses of string?


.. method:: object.__bytes__(self)

   .. index:: pair: built-in function; bytes

   Được :ref:`bytes <func-bytes>` gọi để tính toán biểu diễn chuỗi byte của một đối tượng. Phương thức này phải trả về một đối tượng :class:`bytes`. Bản thân lớp :class:`object` không cung cấp phương thức này.

   .. index::
      single: string; __format__() (object method)
      pair: string; conversion
      pair: built-in function; print


.. method:: object.__format__(self, format_spec)

   Được hàm dựng sẵn :func:`format` gọi, cũng như gián tiếp bởi việc đánh giá :ref:`chuỗi ký tự định dạng <f-strings>` và phương thức :meth:`str.format`, để tạo ra biểu diễn chuỗi "được định dạng" của một đối tượng. Đối số *format_spec* là một chuỗi chứa mô tả về các tùy chọn định dạng mong muốn. Việc diễn giải đối số *format_spec* tùy thuộc vào kiểu triển khai :meth:`__format__`, tuy nhiên hầu hết các lớp sẽ hoặc ủy quyền việc định dạng cho một trong các kiểu dựng sẵn, hoặc sử dụng cú pháp tùy chọn định dạng tương tự.

   Xem :ref:`formatspec` để biết mô tả về cú pháp định dạng chuẩn.

   Giá trị trả về phải là một đối tượng chuỗi.

   Triển khai mặc định của lớp :class:`object` nên được truyền một chuỗi *format_spec* rỗng. Nó ủy quyền cho :meth:`__str__`.

   .. versionchanged:: 3.4
      Phương thức __format__ của chính ``object`` sẽ phát sinh một :exc:`TypeError` nếu được truyền bất kỳ chuỗi không rỗng nào.

   .. versionchanged:: 3.7
      ``object.__format__(x, '')`` hiện tương đương với ``str(x)`` thay vì ``format(str(x), '')``.


.. _richcmpfuncs:
.. method:: object.__lt__(self, other)
            object.__le__(self, other) object.__eq__(self, other) object.__ne__(self, other) object.__gt__(self, other) object.__ge__(self, other)

   .. index::
      single: comparisons

   Đây là các phương thức được gọi là "so sánh phong phú" (rich comparison). Mối tương ứng giữa các ký hiệu toán tử và tên phương thức như sau: ``x<y`` gọi ``x.__lt__(y)``, ``x<=y`` gọi ``x.__le__(y)``, ``x==y`` gọi ``x.__eq__(y)``, ``x!=y`` gọi ``x.__ne__(y)``, ``x>y`` gọi ``x.__gt__(y)``, và ``x>=y`` gọi ``x.__ge__(y)``.

   Một phương thức so sánh phong phú có thể trả về singleton :data:`NotImplemented` nếu nó không triển khai thao tác cho một cặp đối số nhất định. Theo quy ước, ``False`` và ``True`` được trả về khi so sánh thành công. Tuy nhiên, các phương thức này có thể trả về bất kỳ giá trị nào, vì vậy nếu toán tử so sánh được dùng trong ngữ cảnh Boolean (ví dụ: trong điều kiện của một câu lệnh ``if``), Python sẽ gọi
   :func:`bool` trên giá trị đó để xác định liệu kết quả là đúng hay sai.

   Theo mặc định, ``object`` triển khai :meth:`__eq__` bằng cách sử dụng ``is``, trả về
   :data:`NotImplemented` trong trường hợp phép so sánh cho kết quả false: ``True if x is y else NotImplemented``. Đối với :meth:`__ne__`, theo mặc định, nó ủy quyền cho :meth:`__eq__` và đảo ngược kết quả, trừ khi kết quả là
   :data:`!NotImplemented`. Không có mối quan hệ ngầm định nào khác giữa các toán tử so sánh hoặc các phần triển khai mặc định; ví dụ, tính đúng của ``(x<y or x==y)`` không hàm ý ``x<=y``. Để tự động tạo các phép toán sắp thứ tự từ một phép toán gốc duy nhất, hãy xem :deco:`functools.total_ordering`.

   Theo mặc định, lớp :class:`object` cung cấp các phần triển khai nhất quán với :ref:`expressions-value-comparisons`: phép so sánh bằng so sánh theo định danh đối tượng, và các phép so sánh thứ tự sẽ phát sinh :exc:`TypeError`. Mỗi phương thức mặc định có thể trực tiếp tạo ra các kết quả này, nhưng cũng có thể trả về
   :data:`NotImplemented`.

   Xem đoạn về :meth:`__hash__` để biết một số lưu ý quan trọng khi tạo các đối tượng :term:`hashable` hỗ trợ phép so sánh tùy chỉnh và có thể dùng làm khóa từ điển.

   Không có các phiên bản hoán đổi đối số của những phương thức này (để dùng khi đối số bên trái không hỗ trợ thao tác nhưng đối số bên phải có hỗ trợ); thay vào đó, :meth:`__lt__` và :meth:`__gt__` là phép phản chiếu của nhau,
   :meth:`__le__` và :meth:`__ge__` là phép phản chiếu của nhau, và
   :meth:`__eq__` và :meth:`__ne__` là phép phản chiếu của chính chúng. Nếu các toán hạng có kiểu khác nhau, và kiểu của toán hạng bên phải là lớp con trực tiếp hoặc gián tiếp của kiểu toán hạng bên trái, thì phương thức phản chiếu của toán hạng bên phải được ưu tiên; nếu không, phương thức của toán hạng bên trái được ưu tiên. Không xét đến việc kế thừa lớp con ảo.

   Khi không có phương thức phù hợp nào trả về giá trị khác :data:`NotImplemented`, các toán tử ``==`` và ``!=`` sẽ lần lượt quay về sử dụng ``is`` và ``is not``.

.. method:: object.__hash__(self)

   .. index::
      pair: object; dictionary
      pair: built-in function; hash

   Được gọi bởi hàm dựng sẵn :func:`hash` và cho các thao tác trên các phần tử của tập hợp được băm, bao gồm :class:`set`, :class:`frozenset`, và
   :class:`dict`. Phương thức ``__hash__()`` phải trả về một số nguyên. Thuộc tính duy nhất được yêu cầu là các đối tượng so sánh bằng nhau phải có cùng giá trị băm; bạn nên kết hợp các giá trị băm của những thành phần trong đối tượng cũng tham gia vào việc so sánh đối tượng bằng cách đóng gói chúng vào một tuple rồi băm tuple đó. Ví dụ::

       def __hash__(self):
           return hash((self.name, self.nick, self.color))

   .. note::

     :func:`hash` cắt ngắn giá trị được trả về từ phương thức tùy chỉnh của một đối tượng
     :meth:`__hash__` theo kích thước của một :c:type:`Py_ssize_t`. Kích thước này thường là 8 byte trên các bản dựng 64-bit và 4 byte trên các bản dựng 32-bit. Nếu :meth:`__hash__` của một đối tượng phải tương tác được trên các bản dựng có kích thước bit khác nhau, hãy chắc chắn kiểm tra độ rộng trên mọi bản dựng được hỗ trợ. Một cách dễ dàng để làm điều này là dùng ``python -c "import sys; print(sys.hash_info.width)"``.

   Nếu một lớp không định nghĩa phương thức :meth:`__eq__` thì lớp đó không nên định nghĩa một
   thao tác :meth:`__hash__` cũng vậy; nếu nó định nghĩa :meth:`__eq__` nhưng không định nghĩa
   :meth:`__hash__`, các thể hiện của nó sẽ không thể dùng làm phần tử trong các collection có thể băm. Nếu một lớp định nghĩa các đối tượng mutable và triển khai một
   phương thức :meth:`__eq__`, thì không nên triển khai :meth:`__hash__`, vì cách triển khai các collection :term:`hashable` yêu cầu giá trị hash của một khóa là bất biến (nếu giá trị hash của đối tượng thay đổi, nó sẽ nằm trong hash bucket không đúng).

   Theo mặc định, các lớp do người dùng định nghĩa có các phương thức :meth:`__eq__` và :meth:`__hash__` (được kế thừa từ lớp :class:`object`); với các phương thức này, mọi đối tượng được so sánh là không bằng nhau (trừ chính nó) và ``x.__hash__()`` trả về một giá trị phù hợp sao cho ``x == y`` ngụ ý cả ``x is y`` lẫn ``hash(x) == hash(y)``.

   Một lớp ghi đè :meth:`__eq__` và không định nghĩa :meth:`__hash__` sẽ có :meth:`__hash__` được ngầm đặt thành ``None``. Khi phương thức
   :meth:`__hash__` của một lớp là ``None``, các thể hiện của lớp sẽ phát sinh một :exc:`TypeError` phù hợp khi chương trình cố lấy giá trị hash của chúng, và cũng sẽ được nhận diện đúng là không thể băm khi kiểm tra ``isinstance(obj, collections.abc.Hashable)``.

   Nếu một lớp ghi đè :meth:`__eq__` cần giữ lại cách triển khai :meth:`__hash__` từ một lớp cha, phải báo rõ điều này cho interpreter bằng cách đặt ``__hash__ = <ParentClass>.__hash__``.

   Nếu một lớp không override :meth:`__eq__` muốn vô hiệu hóa hỗ trợ hash, lớp đó nên đưa ``__hash__ = None`` vào định nghĩa lớp. Một lớp định nghĩa :meth:`__hash__` riêng và chủ động raise :exc:`TypeError` sẽ bị một lệnh gọi ``isinstance(obj, collections.abc.Hashable)`` xác định nhầm là có thể hash.


   .. note::

      Theo mặc định, các giá trị :meth:`__hash__` của đối tượng str và bytes được "salt" bằng một giá trị ngẫu nhiên không thể dự đoán. Mặc dù chúng vẫn không đổi trong một process Python riêng lẻ, chúng không thể dự đoán giữa các lần gọi Python lặp lại.

      Điều này nhằm bảo vệ khỏi tấn công từ chối dịch vụ do các input được lựa chọn cẩn thận khai thác hiệu năng trường hợp xấu nhất của thao tác chèn dict, với độ phức tạp *O*\ (*n*\ :sup:`2`). Xem https://ocert.org/advisories/ocert-2011-003.html để biết chi tiết.

      Việc thay đổi giá trị hash ảnh hưởng đến thứ tự lặp của các set. Python chưa từng đảm bảo về thứ tự này (và thứ tự này thường khác nhau giữa các bản build 32-bit và 64-bit).

      Xem thêm :envvar:`PYTHONHASHSEED`.

   .. versionchanged:: 3.3
      Tính năng ngẫu nhiên hóa hash được bật theo mặc định.


.. method:: object.__bool__(self)

   .. index:: single: __len__() (mapping object method)

   Được gọi để triển khai việc kiểm tra giá trị chân lý và thao tác built-in ``bool()``; phải trả về ``False`` hoặc ``True``. Khi phương thức này không được định nghĩa, :meth:`~object.__len__` sẽ được gọi, nếu nó được định nghĩa, và đối tượng được xem là true nếu kết quả của nó khác 0. Nếu một lớp không định nghĩa phương thức nào trong hai phương thức này
   :meth:`!__len__` cũng không phải :meth:`!__bool__` (điều này đúng với chính lớp :class:`object`), thì mọi instance của nó đều được xem là true.


.. _attribute-access:

Tùy chỉnh việc truy cập attribute
---------------------------------

Có thể định nghĩa các method sau để tùy chỉnh ý nghĩa của việc truy cập attribute (sử dụng, gán hoặc xóa ``x.name``) đối với các instance của lớp.

.. XXX explain how descriptors interfere here!


.. method:: object.__getattr__(self, name)

   Được gọi khi việc truy cập attribute mặc định thất bại với một :exc:`AttributeError` (hoặc :meth:`__getattribute__` phát sinh một :exc:`AttributeError` vì *name* không phải là attribute của instance hoặc attribute trong cây lớp dành cho ``self``; hoặc :meth:`__get__` của một property *name* phát sinh
   :exc:`AttributeError`). Method này phải trả về giá trị attribute (đã được tính toán) hoặc phát sinh một exception :exc:`AttributeError`. Chính lớp :class:`object` không cung cấp method này.

   Lưu ý rằng nếu attribute được tìm thấy thông qua cơ chế thông thường,
   :meth:`__getattr__` không được gọi. (Đây là sự bất đối xứng có chủ ý giữa
   :meth:`__getattr__` và :meth:`__setattr__`.) Điều này được thực hiện vừa vì lý do hiệu quả, vừa vì nếu không thì :meth:`__getattr__` sẽ không có cách nào truy cập các thuộc tính khác của instance. Lưu ý rằng, ít nhất đối với biến instance, bạn có thể nắm toàn quyền kiểm soát bằng cách không chèn bất kỳ giá trị nào vào từ điển thuộc tính của instance (mà thay vào đó chèn chúng vào một object khác). Xem
   phương thức :meth:`__getattribute__` bên dưới để biết cách thực sự giành toàn quyền kiểm soát việc truy cập thuộc tính.


.. method:: object.__getattribute__(self, name)

   Được gọi vô điều kiện để triển khai việc truy cập thuộc tính cho các instance của class. Nếu class cũng định nghĩa :meth:`__getattr__`, phương thức sau sẽ không được gọi trừ khi :meth:`__getattribute__` hoặc gọi nó một cách tường minh, hoặc phát sinh một
   :exc:`AttributeError`. Phương thức này nên trả về giá trị thuộc tính (đã được tính toán) hoặc phát sinh ngoại lệ :exc:`AttributeError`. Để tránh đệ quy vô hạn trong phương thức này, phần triển khai của nó phải luôn gọi phương thức cùng tên của base class để truy cập bất kỳ thuộc tính nào mà nó cần, ví dụ: ``object.__getattribute__(self, name)``.

   .. note::

      Phương thức này vẫn có thể bị bỏ qua khi tra cứu các special method do được gọi ngầm thông qua cú pháp ngôn ngữ hoặc
      :ref:`các built-in function <builtin-functions>`. Xem :ref:`special-lookup`.

   .. audit-event:: object.__getattr__ obj,name object.__getattribute__

      Đối với một số thao tác truy cập thuộc tính nhạy cảm, sẽ phát sinh một
      Sự kiện kiểm tra :ref:`auditing event <auditing>` ``object.__getattr__`` với các đối số ``obj`` và ``name``.


.. method:: object.__setattr__(self, name, value)

   Được gọi khi có thao tác gán thuộc tính được thực hiện. Phương thức này được gọi thay cho cơ chế thông thường (tức là lưu giá trị vào từ điển instance). *name* là tên thuộc tính, *value* là giá trị sẽ được gán cho thuộc tính đó.

   Nếu :meth:`__setattr__` muốn gán cho một thuộc tính instance, nó nên gọi phương thức của lớp cơ sở có cùng tên, ví dụ: ``object.__setattr__(self, name, value)``.

   .. audit-event:: object.__setattr__ obj,name,value object.__setattr__

      Đối với một số thao tác gán thuộc tính nhạy cảm, phát sinh một
      Sự kiện kiểm tra :ref:`auditing event <auditing>` ``object.__setattr__`` với các đối số ``obj``, ``name``, ``value``.


.. method:: object.__delattr__(self, name)

   Tương tự :meth:`__setattr__` nhưng dành cho việc xóa thuộc tính thay vì gán. Chỉ nên triển khai phương thức này nếu ``del obj.name`` có ý nghĩa đối với đối tượng.

   .. audit-event:: object.__delattr__ obj,name object.__delattr__

      Đối với một số thao tác xóa thuộc tính nhạy cảm, phát sinh một
      :ref:`sự kiện auditing <auditing>` ``object.__delattr__`` với các đối số ``obj`` và ``name``.


.. method:: object.__dir__(self)

   Được gọi khi :func:`dir` được gọi trên đối tượng. Phải trả về một iterable. :func:`dir` chuyển iterable được trả về thành một list và sắp xếp nó.


Tùy chỉnh quyền truy cập thuộc tính của module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: __getattr__ (module attribute)
   single: __dir__ (module attribute)
   single: __class__ (module attribute)

.. method:: module.__getattr__
            module.__dir__

Các tên đặc biệt ``__getattr__`` và ``__dir__`` cũng có thể được dùng để tùy chỉnh quyền truy cập vào các thuộc tính của module. Hàm ``__getattr__`` ở cấp module phải nhận một đối số là tên của một thuộc tính, rồi trả về giá trị đã tính toán hoặc phát sinh :exc:`AttributeError`. Nếu không tìm thấy một thuộc tính trên đối tượng module bằng cách tra cứu thông thường, tức là
:meth:`object.__getattribute__`, thì ``__getattr__`` được tìm trong ``__dict__`` của module trước khi phát sinh :exc:`AttributeError`. Nếu tìm thấy, nó được gọi với tên thuộc tính và kết quả được trả về.

Hàm ``__dir__`` không được nhận đối số nào và phải trả về một iterable các string biểu thị những tên có thể truy cập trên module. Nếu có mặt, hàm này ghi đè việc tìm kiếm :func:`dir` tiêu chuẩn trên một module.

.. attribute:: module.__class__

Để tùy chỉnh chi tiết hơn hành vi của module (thiết lập thuộc tính, property, v.v.), có thể đặt thuộc tính ``__class__`` của một đối tượng module thành một subclass của :class:`types.ModuleType`. Ví dụ::

   import sys
   from types import ModuleType

   class VerboseModule(ModuleType):
       def __repr__(self):
           return f'Verbose {self.__name__}'

       def __setattr__(self, attr, value):
           print(f'Setting {attr}...')
           super().__setattr__(attr, value)

   sys.modules[__name__].__class__ = VerboseModule

.. note::
   Việc định nghĩa mô-đun ``__getattr__`` và thiết lập mô-đun ``__class__`` chỉ ảnh hưởng đến các tra cứu được thực hiện bằng cú pháp truy cập thuộc tính -- việc truy cập trực tiếp các biến toàn cục của mô-đun (dù bằng mã bên trong mô-đun hay thông qua tham chiếu đến dictionary biến toàn cục của mô-đun) không bị ảnh hưởng.

.. versionchanged:: 3.5
   Thuộc tính mô-đun ``__class__`` giờ đây có thể ghi được.

.. versionadded:: 3.7
   Các thuộc tính mô-đun ``__getattr__`` và ``__dir__``.

.. seealso::

   :pep:`562` - Mô-đun __getattr__ và __dir__
      Mô tả các hàm ``__getattr__`` và ``__dir__`` trên mô-đun.


.. _descriptors:

Triển khai Descriptors
^^^^^^^^^^^^^^^^^^^^^^

Các phương thức sau chỉ áp dụng khi một instance của lớp chứa phương thức (còn gọi là lớp *descriptor*) xuất hiện trong một lớp *owner* (descriptor phải nằm trong class dictionary của owner hoặc trong class dictionary của một trong các lớp cha của nó). Trong các ví dụ bên dưới, "thuộc tính" đề cập đến thuộc tính có tên là khóa của property trong :attr:`~object.__dict__` của lớp owner. Bản thân lớp :class:`object` không triển khai bất kỳ protocol nào trong số này.

.. method:: object.__get__(self, instance, owner=None)

   Được gọi để lấy thuộc tính của lớp sở hữu (truy cập thuộc tính lớp) hoặc của một instance của lớp đó (truy cập thuộc tính instance). Đối số tùy chọn *owner* là lớp sở hữu, còn *instance* là instance mà qua đó thuộc tính được truy cập, hoặc ``None`` khi thuộc tính được truy cập qua *owner*.

   Phương thức này phải trả về giá trị thuộc tính đã được tính toán hoặc phát sinh một
   :exc:`AttributeError` exception.

   :PEP:`252` chỉ định rằng :meth:`__get__` có thể gọi được với một hoặc hai đối số. Các descriptor dựng sẵn của chính Python hỗ trợ đặc tả này; tuy nhiên, có thể một số công cụ bên thứ ba có các descriptor yêu cầu cả hai đối số. Phần cài đặt :meth:`__getattribute__` của chính Python luôn truyền cả hai đối số, dù chúng có bắt buộc hay không.

.. method:: object.__set__(self, instance, value)

   Được gọi để đặt thuộc tính trên một instance *instance* của lớp sở hữu thành một giá trị mới, *value*.

   Lưu ý, việc thêm :meth:`__set__` hoặc :meth:`__delete__` sẽ thay đổi loại descriptor thành một "data descriptor". Xem :ref:`descriptor-invocation` để biết thêm chi tiết.

.. method:: object.__delete__(self, instance)

   Được gọi để xóa thuộc tính trên một instance *instance* của lớp sở hữu.

Các instance của descriptor cũng có thể có thuộc tính :attr:`!__objclass__`:

.. attribute:: object.__objclass__

   Module :mod:`inspect` diễn giải thuộc tính :attr:`!__objclass__` là chỉ định lớp nơi đối tượng này được định nghĩa (thiết lập thuộc tính này phù hợp có thể hỗ trợ introspection tại runtime đối với các thuộc tính lớp động). Đối với callable, thuộc tính này có thể cho biết một instance của kiểu đã cho (hoặc một lớp con) được mong đợi hoặc bắt buộc làm đối số vị trí đầu tiên (ví dụ, CPython đặt thuộc tính này cho các unbound method được triển khai bằng C).


.. _descriptor-invocation:

Gọi Descriptor
^^^^^^^^^^^^^^

Nói chung, descriptor là một thuộc tính đối tượng có "hành vi liên kết", tức là thuộc tính có việc truy cập đã bị ghi đè bởi các phương thức trong descriptor protocol: :meth:`~object.__get__`, :meth:`~object.__set__`, và
:meth:`~object.__delete__`. Nếu bất kỳ phương thức nào trong số đó được định nghĩa cho một đối tượng, đối tượng đó được gọi là descriptor.

Hành vi mặc định khi truy cập thuộc tính là lấy, thiết lập hoặc xóa thuộc tính khỏi dictionary của một đối tượng. Ví dụ, ``a.x`` có chuỗi tra cứu bắt đầu với ``a.__dict__['x']``, sau đó là ``type(a).__dict__['x']``, và tiếp tục qua các lớp cơ sở của ``type(a)``, không bao gồm metaclass.

Tuy nhiên, nếu giá trị được tra cứu là một đối tượng định nghĩa một trong các phương thức descriptor, Python có thể ghi đè hành vi mặc định và thay vào đó gọi phương thức descriptor. Vị trí xảy ra điều này trong chuỗi ưu tiên phụ thuộc vào các phương thức descriptor nào đã được định nghĩa và cách chúng được gọi.

Điểm khởi đầu để gọi descriptor là một binding, ``a.x``. Cách các đối số được tập hợp phụ thuộc vào ``a``:

Lời gọi trực tiếp
   Lời gọi đơn giản nhất và ít gặp nhất là khi mã người dùng trực tiếp gọi một phương thức descriptor: ``x.__get__(a)``.

Binding với instance
   Nếu binding với một object instance, ``a.x`` được chuyển thành lời gọi: ``type(a).__dict__['x'].__get__(a, type(a))``.

Binding với class
   Nếu binding với một class, ``A.x`` được chuyển thành lời gọi: ``A.__dict__['x'].__get__(None, A)``.

Liên kết Super
   Một phép tra cứu có dấu chấm như ``super(A, a).x`` sẽ tìm kiếm ``a.__class__.__mro__`` để lấy một lớp cơ sở ``B`` theo sau ``A``, rồi trả về ``B.__dict__['x'].__get__(a, A)``. Nếu không phải là descriptor, ``x`` sẽ được trả về không thay đổi.

.. testcode::
    :hide:

    class Desc:
        def __get__(*args):
            return args

    class B:

        x = Desc()

    class A(B):

        x = 999

        def m(self):
            'Demonstrate these two descriptor invocations are equivalent'
            result1 = super(A, self).x
            result2 = B.__dict__['x'].__get__(self, A)
            return result1 == result2

.. doctest::
    :hide:

    >>> a = A()
    >>> a.__class__.__mro__.index(B) > a.__class__.__mro__.index(A)
    True
    >>> super(A, a).x == B.__dict__['x'].__get__(a, A)
    True
    >>> a.m()
    True

Đối với các liên kết instance, thứ tự ưu tiên khi gọi descriptor phụ thuộc vào những phương thức descriptor nào được định nghĩa. Một descriptor có thể định nghĩa bất kỳ tổ hợp nào của :meth:`~object.__get__`, :meth:`~object.__set__` và
:meth:`~object.__delete__`. Nếu nó không định nghĩa :meth:`!__get__`, thì việc truy cập attribute sẽ trả về chính đối tượng descriptor, trừ khi có một giá trị trong instance dictionary của đối tượng. Nếu descriptor định nghĩa :meth:`!__set__` và/hoặc :meth:`!__delete__`, đó là data descriptor; nếu không định nghĩa cả hai, đó là non-data descriptor. Thông thường, data descriptor định nghĩa cả :meth:`!__get__` và :meth:`!__set__`, trong khi non-data descriptor chỉ có phương thức :meth:`!__get__`. Data descriptor có
:meth:`!__get__` và :meth:`!__set__` (và/hoặc :meth:`!__delete__`) được định nghĩa luôn ghi đè một định nghĩa lại trong instance dictionary. Ngược lại, non-data descriptor có thể bị các instance ghi đè.

Các phương thức Python (bao gồm cả những phương thức được trang trí bằng
:deco:`staticmethod` và :deco:`classmethod`) được triển khai dưới dạng non-data descriptor. Do đó, các instance có thể định nghĩa lại và ghi đè phương thức. Điều này cho phép từng instance có được hành vi khác với các instance khác của cùng một lớp.

Decorator :deco:`property` được triển khai dưới dạng một data descriptor. Do đó, các instance không thể ghi đè hành vi của một property.


.. _slots:

__slots__
^^^^^^^^^

*__slots__* cho phép chúng ta khai báo tường minh các data member (như property) và ngăn việc tạo :attr:`~object.__dict__` cùng *__weakref__* (trừ khi được khai báo tường minh trong *__slots__* hoặc có sẵn trong lớp cha).

Không gian tiết kiệm được so với việc dùng :attr:`~object.__dict__` có thể đáng kể. Tốc độ tra cứu attribute cũng có thể được cải thiện đáng kể.

.. data:: object.__slots__

   Biến lớp này có thể được gán một string, iterable hoặc sequence các string chứa tên biến được các instance sử dụng. *__slots__* dành sẵn không gian cho các biến đã khai báo và ngăn việc tự động tạo
   :attr:`~object.__dict__` và *__weakref__* cho mỗi instance.


.. _datamodel-note-slots:

Lưu ý khi sử dụng *__slots__*:

* Khi kế thừa từ một lớp không có *__slots__*, thì
  thuộc tính :attr:`~object.__dict__` và *__weakref__* của các instance sẽ luôn có thể truy cập được.

* Nếu không có biến :attr:`~object.__dict__`, các instance không thể được gán các biến mới không được liệt kê trong định nghĩa *__slots__*. Các nỗ lực gán cho một tên biến không được liệt kê sẽ phát sinh :exc:`AttributeError`. Nếu muốn cho phép gán động các biến mới, hãy thêm ``'__dict__'`` vào chuỗi các string trong khai báo *__slots__*.

* Nếu không có biến *__weakref__* cho mỗi instance, các lớp định nghĩa *__slots__* không hỗ trợ :mod:`weak references <weakref>` đến các instance của chúng. Nếu cần hỗ trợ weak reference, hãy thêm ``'__weakref__'`` vào chuỗi các string trong khai báo *__slots__*.

* *__slots__* được triển khai ở cấp lớp bằng cách tạo các :ref:`descriptors <descriptors>` cho mỗi tên biến. Do đó, không thể dùng các thuộc tính lớp để đặt giá trị mặc định cho các biến instance được xác định bởi *__slots__*; nếu không, thuộc tính lớp sẽ ghi đè việc gán descriptor.

* Tác dụng của một khai báo *__slots__* không chỉ giới hạn ở lớp nơi nó được định nghĩa. *__slots__* được khai báo trong các lớp cha sẽ khả dụng trong các lớp con. Tuy nhiên, các instance của một lớp con sẽ nhận được một
  :attr:`~object.__dict__` và *__weakref__* trừ khi lớp con cũng định nghĩa *__slots__* (chỉ nên chứa tên của các slot *bổ sung*).

* Nếu một lớp định nghĩa một slot cũng đã được định nghĩa trong lớp cơ sở, biến thực thể do slot của lớp cơ sở định nghĩa sẽ không thể truy cập được (trừ khi truy xuất descriptor của nó trực tiếp từ lớp cơ sở). Điều này khiến ý nghĩa của chương trình trở nên không xác định. Trong tương lai, có thể sẽ bổ sung một kiểm tra để ngăn điều này.

* :exc:`TypeError` sẽ được raise nếu các *__slots__* không rỗng được định nghĩa cho một lớp kế thừa từ một
  kiểu dựng sẵn "variable-length" :c:member:`như <PyTypeObject.tp_itemsize>`
  :class:`int`, :class:`bytes` và :class:`tuple`.

* Có thể gán bất kỳ :term:`iterable` không phải chuỗi nào cho *__slots__*.

* Nếu dùng một :class:`dictionary <dict>` để gán *__slots__*, các khóa của dictionary sẽ được dùng làm tên slot. Các giá trị của dictionary có thể được dùng để cung cấp docstring cho từng thuộc tính; các docstring này sẽ được nhận diện bởi
  :func:`inspect.getdoc` và hiển thị trong đầu ra của :func:`help`.

* Việc gán :attr:`~object.__class__` chỉ hoạt động nếu cả hai lớp có cùng *__slots__*.

* :ref:`Đa kế thừa <tut-multiple>` với nhiều lớp cha có slot có thể được sử dụng, nhưng chỉ một lớp cha được phép có các thuộc tính được tạo bởi slot (các lớp cơ sở khác phải có bố cục slot rỗng) - các trường hợp vi phạm sẽ phát sinh
  :exc:`TypeError`.

* Nếu một :term:`iterator` được dùng cho *__slots__* thì một :term:`descriptor` được tạo cho mỗi giá trị của iterator. Tuy nhiên, thuộc tính *__slots__* sẽ là một iterator rỗng.

.. _class-customization:

Tùy chỉnh việc tạo lớp
----------------------

Bất cứ khi nào một lớp kế thừa từ lớp khác, :meth:`~object.__init_subclass__` sẽ được gọi trên lớp cha. Bằng cách này, có thể viết các lớp thay đổi hành vi của các lớp con. Điều này có liên hệ chặt chẽ với class decorator, nhưng trong khi class decorator chỉ ảnh hưởng đến lớp cụ thể mà chúng được áp dụng, ``__init_subclass__`` chỉ áp dụng cho các lớp con được tạo sau này của lớp định nghĩa phương thức đó.

.. classmethod:: object.__init_subclass__(cls)

   Phương thức này được gọi bất cứ khi nào lớp chứa nó được tạo lớp con. Khi đó, *cls* là lớp con mới. Nếu được định nghĩa như một phương thức instance thông thường, phương thức này sẽ được ngầm chuyển thành một class method.

   Các đối số từ khóa được cung cấp cho một lớp mới sẽ được truyền đến ``__init_subclass__`` của lớp cha. Để tương thích với các lớp khác sử dụng ``__init_subclass__``, cần lấy ra các đối số từ khóa cần thiết và փոխանց các đối số còn lại cho lớp cơ sở, như trong::

       class Philosopher:
           def __init_subclass__(cls, /, default_name, **kwargs):
               super().__init_subclass__(**kwargs)
               cls.default_name = default_name

       class AustralianPhilosopher(Philosopher, default_name="Bruce"):
           pass

   Triển khai mặc định ``object.__init_subclass__`` không làm gì cả, nhưng sẽ phát sinh lỗi nếu được gọi với bất kỳ đối số nào.

   .. note::

      Gợi ý metaclass ``metaclass`` được phần còn lại của cơ chế type xử lý và không bao giờ được truyền đến các triển khai ``__init_subclass__``. Có thể truy cập metaclass thực tế (thay vì gợi ý tường minh) bằng ``type(cls)``.

   .. versionadded:: 3.6


Khi một lớp được tạo, :meth:`!type.__new__` quét các biến của lớp và gọi callback đến những biến có hook :meth:`~object.__set_name__`.

.. method:: object.__set_name__(self, owner, name)

   Được tự động gọi khi lớp sở hữu *owner* được tạo. Đối tượng đã được gán cho *name* trong lớp đó.::

       class A:
           x = C()  # Tự động gọi: x.__set_name__(A, 'x')

   Nếu biến lớp được gán sau khi lớp được tạo,
   :meth:`__set_name__` sẽ không được gọi tự động. Nếu cần, có thể gọi trực tiếp :meth:`__set_name__`::

       class A:
          pass

       c = C()
       A.x = c                  # Hook không được gọi
       c.__set_name__(A, 'x')   # Gọi hook theo cách thủ công

   Xem :ref:`class-object-creation` để biết thêm chi tiết.

   .. versionadded:: 3.6


.. _metaclasses:

Metaclass
^^^^^^^^^

.. index::
   single: metaclass
   pair: built-in function; type
   single: = (equals); class definition

Theo mặc định, các lớp được tạo bằng :func:`type`. Phần thân lớp được thực thi trong một namespace mới và tên lớp được liên kết cục bộ với kết quả của ``type(name, bases, namespace)``.

Có thể tùy chỉnh quá trình tạo lớp bằng cách truyền đối số từ khóa ``metaclass`` trong dòng định nghĩa lớp, hoặc bằng cách kế thừa từ một lớp hiện có đã bao gồm đối số này. Trong ví dụ sau, cả ``MyClass`` và ``MySubclass`` đều là các instance của ``Meta``::

   class Meta(type):
       pass

   class MyClass(metaclass=Meta):
       pass

   class MySubclass(MyClass):
       pass

Mọi đối số từ khóa khác được chỉ định trong định nghĩa lớp sẽ được chuyển tiếp đến tất cả các thao tác metaclass được mô tả bên dưới.

Khi một định nghĩa lớp được thực thi, các bước sau sẽ diễn ra:

* Các mục nhập MRO được phân giải;
* metaclass phù hợp được xác định;
* namespace của lớp được chuẩn bị;
* phần thân lớp được thực thi;
* đối tượng lớp được tạo.


Phân giải các mục nhập MRO
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: object.__mro_entries__(self, bases)

   Nếu một base xuất hiện trong định nghĩa lớp không phải là một instance của
   :class:`type`, thì một phương thức :meth:`!__mro_entries__` sẽ được tìm kiếm trên base đó. Nếu tìm thấy phương thức :meth:`!__mro_entries__`, base sẽ được thay thế bằng kết quả của lời gọi đến :meth:`!__mro_entries__` khi tạo lớp. Phương thức được gọi với tuple các base gốc được truyền vào tham số *bases*, và phải trả về một tuple các lớp sẽ được sử dụng thay cho base đó. Tuple trả về có thể rỗng: trong những trường hợp này, base gốc sẽ bị bỏ qua.

.. seealso::

   :func:`types.resolve_bases`
      Phân giải động các base không phải là instance của :class:`type`.

   :func:`types.get_original_bases`
      Truy xuất "các base gốc" của một lớp trước các sửa đổi bởi
      :meth:`~object.__mro_entries__`.

   :pep:`560`
      Hỗ trợ cốt lõi cho module typing và các kiểu generic.


Xác định metaclass phù hợp
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. index::
    single: metaclass hint

Metaclass phù hợp cho một định nghĩa lớp được xác định như sau:

* nếu không có lớp cơ sở và không có metaclass tường minh nào được cung cấp, thì :func:`type` sẽ được dùng;
* nếu một metaclass tường minh được cung cấp và nó *không* phải là một instance của
  :func:`type`, thì nó được dùng trực tiếp làm metaclass;
* nếu một instance của :func:`type` được cung cấp làm metaclass tường minh, hoặc các lớp cơ sở được định nghĩa, thì metaclass dẫn xuất nhất sẽ được dùng.

Metaclass dẫn xuất nhất được chọn từ metaclass được chỉ định tường minh (nếu có) và các metaclass (tức là ``type(cls)``) của tất cả các lớp cơ sở được chỉ định. Metaclass dẫn xuất nhất là metaclass là một subtype của *tất cả* các metaclass ứng viên này. Nếu không có metaclass ứng viên nào đáp ứng tiêu chí đó, thì định nghĩa lớp sẽ thất bại với ``TypeError``.


.. _prepare:

Chuẩn bị namespace của lớp
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
    single: __prepare__ (metaclass method)

Sau khi metaclass phù hợp đã được xác định, namespace của lớp sẽ được chuẩn bị. Nếu metaclass có một thuộc tính ``__prepare__``, thuộc tính đó được gọi dưới dạng ``namespace = metaclass.__prepare__(name, bases, **kwds)`` (trong đó các đối số keyword bổ sung, nếu có, đến từ định nghĩa lớp). Phương thức ``__prepare__`` nên được triển khai như một
:func:`classmethod <classmethod>`. Không gian tên do ``__prepare__`` trả về được truyền vào ``__new__``, nhưng khi đối tượng lớp cuối cùng được tạo, không gian tên sẽ được sao chép vào một ``dict`` mới.

Nếu metaclass không có thuộc tính ``__prepare__``, thì không gian tên của lớp được khởi tạo dưới dạng một ánh xạ có thứ tự rỗng.

.. seealso::

   :pep:`3115` - Metaclass trong Python 3000
      Đã giới thiệu hook không gian tên ``__prepare__``


Thực thi phần thân lớp
^^^^^^^^^^^^^^^^^^^^^^

.. index::
    single: class; body

Phần thân lớp được thực thi (xấp xỉ) dưới dạng ``exec(body, globals(), namespace)``. Điểm khác biệt chính so với một lệnh gọi thông thường đến :func:`exec` là phạm vi từ vựng cho phép phần thân lớp (bao gồm mọi method) tham chiếu các tên từ phạm vi hiện tại và các phạm vi bên ngoài khi định nghĩa lớp xuất hiện bên trong một function.

Tuy nhiên, ngay cả khi định nghĩa lớp xuất hiện bên trong function, các method được định nghĩa bên trong lớp vẫn không thể thấy các tên được định nghĩa ở phạm vi lớp. Các biến lớp phải được truy cập thông qua tham số đầu tiên của các instance method hoặc class method, hoặc thông qua tham chiếu ``__class__`` có phạm vi từ vựng ngầm định được mô tả trong phần tiếp theo.

.. _class-object-creation:

Tạo đối tượng lớp
^^^^^^^^^^^^^^^^^

.. index::
    single: __class__ (method cell)
    single: __classcell__ (class namespace entry)


Sau khi namespace của lớp đã được điền đầy bằng cách thực thi thân lớp, đối tượng lớp được tạo bằng cách gọi ``metaclass(name, bases, namespace, **kwds)`` (các từ khóa bổ sung được truyền ở đây cũng giống như các từ khóa được truyền cho ``__prepare__``).

Đối tượng lớp này sẽ được tham chiếu bởi dạng không đối số của :func:`super`. ``__class__`` là một tham chiếu closure ngầm được compiler tạo ra nếu bất kỳ phương thức nào trong thân lớp tham chiếu đến ``__class__`` hoặc ``super``. Điều này cho phép dạng không đối số của
:func:`super` xác định chính xác lớp đang được định nghĩa dựa trên lexical scoping, trong khi lớp hoặc instance được dùng để thực hiện lời gọi hiện tại được xác định dựa trên đối số đầu tiên truyền vào phương thức.

.. impl-detail::

   Trong CPython 3.6 trở lên, ô ``__class__`` được truyền đến metaclass dưới dạng một mục ``__classcell__`` trong namespace của lớp. Nếu có mặt, nó phải được truyền tiếp đến lời gọi ``type.__new__`` để lớp được khởi tạo đúng cách. Nếu không làm vậy sẽ dẫn đến :exc:`RuntimeError` trong Python 3.8.

Khi sử dụng metaclass mặc định :class:`type`, hoặc bất kỳ metaclass nào cuối cùng gọi ``type.__new__``, các bước tùy biến bổ sung sau đây sẽ được gọi sau khi tạo đối tượng lớp:

1) Phương thức ``type.__new__`` thu thập mọi thuộc tính trong namespace của lớp có định nghĩa một phương thức :meth:`~object.__set_name__`;
2) Các phương thức ``__set_name__`` đó được gọi với lớp đang được định nghĩa và tên đã gán của thuộc tính cụ thể đó;
3) hook :meth:`~object.__init_subclass__` được gọi trên lớp cha trực tiếp của lớp mới trong thứ tự phân giải phương thức của nó.

Sau khi đối tượng lớp được tạo, nó được truyền cho các class decorator có trong định nghĩa lớp (nếu có), và đối tượng kết quả được liên kết trong namespace cục bộ dưới dạng lớp đã định nghĩa.

Khi một lớp mới được tạo bởi ``type.__new__``, đối tượng được cung cấp làm tham số namespace sẽ được sao chép vào một mapping có thứ tự mới và đối tượng gốc bị loại bỏ. Bản sao mới được bọc trong một proxy chỉ đọc, rồi trở thành thuộc tính :attr:`~type.__dict__` của đối tượng lớp.

.. seealso::

   :pep:`3135` - super mới
      Mô tả tham chiếu closure ``__class__`` ngầm định


Các cách sử dụng metaclass
^^^^^^^^^^^^^^^^^^^^^^^^^^

Các ứng dụng tiềm năng của metaclass là vô hạn. Một số ý tưởng đã được khám phá gồm enum, logging, kiểm tra interface, delegation tự động, tạo property tự động, proxy, framework, và khóa/đồng bộ hóa tài nguyên tự động.


Tùy chỉnh việc kiểm tra instance và subclass
--------------------------------------------

Các phương thức sau được dùng để ghi đè hành vi mặc định của các
hàm dựng sẵn :func:`isinstance` và :func:`issubclass`.

Cụ thể, metaclass :class:`abc.ABCMeta` triển khai các phương thức này để cho phép bổ sung các Abstract Base Class (ABC) dưới dạng "lớp cơ sở ảo" vào bất kỳ class hoặc type nào (kể cả các type dựng sẵn), bao gồm cả các ABC khác.

.. method:: type.__instancecheck__(self, instance)

   Trả về true nếu *instance* nên được xem là instance (trực tiếp hoặc gián tiếp) của *class*. Nếu được định nghĩa, được gọi để triển khai ``isinstance(instance, class)``.


.. method:: type.__subclasscheck__(self, subclass)

   Trả về true nếu *subclass* nên được xem là subclass (trực tiếp hoặc gián tiếp) của *class*. Nếu được định nghĩa, được gọi để triển khai ``issubclass(subclass, class)``.


Lưu ý rằng các phương thức này được tra cứu trên type (metaclass) của một lớp. Chúng không thể được định nghĩa dưới dạng class method trong chính lớp đó. Điều này nhất quán với việc tra cứu các special method được gọi trên instance, chỉ khác là trong trường hợp này instance tự nó là một lớp.

.. seealso::

   :pep:`3119` - Giới thiệu về Abstract Base Classes
      Bao gồm đặc tả để tùy biến hành vi của :func:`isinstance` và
      :func:`issubclass` thông qua :meth:`~type.__instancecheck__` và
      :meth:`~type.__subclasscheck__`, kèm theo động cơ cho chức năng này trong bối cảnh bổ sung Abstract Base Classes (xem module :mod:`abc`) vào ngôn ngữ.


Mô phỏng generic type
---------------------

Khi sử dụng :term:`type annotation <annotation>`, thường sẽ hữu ích khi *tham số hóa* một :term:`generic type` bằng ký pháp dấu ngoặc vuông của Python. Ví dụ, annotation ``list[int]`` có thể được dùng để biểu thị một
:class:`list` trong đó mọi phần tử đều có kiểu :class:`int`.

.. seealso::

   :pep:`484` - Gợi ý kiểu (Type Hints)
      Giới thiệu framework của Python cho các chú thích kiểu

   :ref:`Các kiểu Generic Alias <types-genericalias>`
      Tài liệu về các đối tượng biểu diễn các lớp generic được tham số hóa

   :ref:`Generics`, :ref:`generic do người dùng định nghĩa <user-defined-generics>` và :class:`typing.Generic`
      Tài liệu về cách triển khai các lớp generic có thể được tham số hóa tại runtime và được các static type-checker hiểu.

Nhìn *chung*, một lớp chỉ có thể được tham số hóa nếu nó định nghĩa phương thức lớp đặc biệt ``__class_getitem__()``.

.. classmethod:: object.__class_getitem__(cls, key)

   Trả về một đối tượng biểu thị sự chuyên biệt hóa của một lớp generic theo các đối số kiểu được tìm thấy trong *key*.

   Khi được định nghĩa trên một lớp, ``__class_getitem__()`` tự động là một phương thức lớp. Do đó, không cần trang trí nó bằng
   :deco:`classmethod` khi định nghĩa nó.


Mục đích của *__class_getitem__*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mục đích của :meth:`~object.__class_getitem__` là cho phép tham số hóa tại runtime các lớp generic của standard library để áp dụng :term:`type hints <type hint>` cho các lớp này dễ dàng hơn.

Để triển khai các lớp generic tùy chỉnh có thể được tham số hóa tại runtime và được static type-checker hiểu, người dùng nên kế thừa từ một lớp standard library đã triển khai :meth:`~object.__class_getitem__`, hoặc kế thừa từ :class:`typing.Generic`, vốn có cách triển khai riêng cho ``__class_getitem__()``.

Các cách triển khai tùy chỉnh của :meth:`~object.__class_getitem__` trên các lớp được định nghĩa bên ngoài thư viện chuẩn có thể không được các type-checker bên thứ ba như mypy hiểu. Không khuyến khích sử dụng ``__class_getitem__()`` trên bất kỳ lớp nào cho mục đích ngoài type hinting.


.. _classgetitem-versus-getitem:


*__class_getitem__* so với *__getitem__*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Thông thường, thao tác :ref:`subscription <subscriptions>` của một đối tượng bằng dấu ngoặc vuông sẽ gọi instance method :meth:`~object.__getitem__` được định nghĩa trên lớp của đối tượng đó. Tuy nhiên, nếu đối tượng được subscription tự nó là một lớp, class method :meth:`~object.__class_getitem__` có thể được gọi thay thế. Nếu được định nghĩa đúng cách, ``__class_getitem__()`` sẽ trả về một đối tượng :ref:`GenericAlias <types-genericalias>`.

Khi gặp biểu thức :term:`expression` ``obj[x]``, trình thông dịch Python sẽ thực hiện quy trình gần giống như sau để quyết định liệu
:meth:`~object.__getitem__` hay :meth:`~object.__class_getitem__` nên được gọi::

   from inspect import isclass

   def subscribe(obj, x):
       """Return the result of the expression 'obj[x]'"""

       class_of_obj = type(obj)

       # Nếu lớp của obj định nghĩa __getitem__,
       # gọi class_of_obj.__getitem__(obj, x)
       if hasattr(class_of_obj, '__getitem__'):
           return class_of_obj.__getitem__(obj, x)

       # Ngược lại, nếu obj là một class và định nghĩa __class_getitem__,
       # gọi obj.__class_getitem__(x)
       elif isclass(obj) and hasattr(obj, '__class_getitem__'):
           return obj.__class_getitem__(x)

       # Ngược lại, phát sinh một exception
       else:
           raise TypeError(
               f"'{class_of_obj.__name__}' object is not subscriptable"
           )

Trong Python, mọi class đều tự thân là instance của các class khác. Class của một class được gọi là :term:`metaclass` của class đó, và hầu hết các class có
class :class:`type` làm metaclass. :class:`type` không định nghĩa
:meth:`~object.__getitem__`, nghĩa là các biểu thức như ``list[int]``, ``dict[str, float]`` và ``tuple[str, bytes]`` đều dẫn đến việc
:meth:`~object.__class_getitem__` được gọi::

   >>> # list có lớp "type" làm metaclass, giống như hầu hết các lớp:
   >>> type(list)
   <class 'type'>
   >>> type(dict) == type(list) == type(tuple) == type(str) == type(bytes)
   True
   >>> # "list[int]" gọi "list.__class_getitem__(int)"
   >>> list[int]
   list[int]
   >>> # list.__class_getitem__ trả về một đối tượng GenericAlias:
   >>> type(list[int])
   <class 'types.GenericAlias'>

Tuy nhiên, nếu một lớp có metaclass tùy chỉnh định nghĩa
:meth:`~object.__getitem__`, việc subscript lớp có thể dẫn đến hành vi khác. Bạn có thể tìm thấy một ví dụ về điều này trong module :mod:`enum`::

   >>> from enum import Enum
   >>> class Menu(Enum):
   ...     """A breakfast menu"""
   ...     SPAM = 'spam'
   ...     BACON = 'bacon'
   ...
   >>> # Các lớp Enum có một metaclass tùy chỉnh:
   >>> type(Menu)
   <class 'enum.EnumMeta'>
   >>> # EnumMeta định nghĩa __getitem__,
   >>> # vì vậy __class_getitem__ không được gọi,
   >>> # và kết quả không phải là một đối tượng GenericAlias:
   >>> Menu['SPAM']
   <Menu.SPAM: 'spam'>
   >>> type(Menu['SPAM'])
   <enum 'Menu'>


.. seealso::
   :pep:`560` - Core Support for typing module and generic types
      Introducing :meth:`~object.__class_getitem__`, and outlining when a
      :ref:`subscription<subscriptions>` results in ``__class_getitem__()``
      being called instead of :meth:`~object.__getitem__`


.. _callable-types:

Mô phỏng các đối tượng có thể gọi
---------------------------------


.. method:: object.__call__(self[, args...])

   .. index:: pair: call; instance

   Được gọi khi instance được "gọi" như một hàm; nếu phương thức này được định nghĩa, ``x(arg1, arg2, ...)`` gần tương đương với ``type(x).__call__(x, arg1, ...)``. Bản thân lớp :class:`object` không cung cấp phương thức này.


.. _sequence-types:

Mô phỏng các kiểu container
---------------------------

Có thể định nghĩa các phương thức sau để triển khai các đối tượng container. Không phương thức nào trong số này được chính lớp :class:`object` cung cấp. Container thường là
:term:`các sequence <sequence>` (chẳng hạn như :class:`lists <list>` hoặc
:class:`tuples <tuple>`) hoặc :term:`mappings <mapping>` (chẳng hạn như
:term:`dictionaries <dictionary>`), nhưng cũng có thể biểu diễn các container khác. Tập phương thức đầu tiên được dùng để mô phỏng sequence hoặc mapping; điểm khác biệt là đối với sequence, các khóa được phép phải là các số nguyên *k* sao cho ``0 <= k < N`` với *N* là độ dài của sequence, hoặc các đối tượng :class:`slice`, vốn xác định một phạm vi các mục. Mapping cũng nên cung cấp các phương thức
:meth:`!keys`, :meth:`!values`, :meth:`!items`, :meth:`!get`, :meth:`!clear`,
:meth:`!setdefault`, :meth:`!pop`, :meth:`!popitem`, :meth:`!copy`, và
:meth:`!update` hoạt động tương tự các phương thức dành cho đối tượng :class:`dictionary <dict>` tiêu chuẩn của Python. Module :mod:`collections.abc` cung cấp một
:class:`~collections.abc.MutableMapping`
:term:`abstract base class` để giúp tạo các phương thức đó từ một tập cơ sở gồm
:meth:`~object.__getitem__`, :meth:`~object.__setitem__`,
:meth:`~object.__delitem__`, và :meth:`!keys`.

Các sequence có thể thay đổi nên cung cấp các phương thức
:meth:`~sequence.append`, :meth:`~sequence.clear`, :meth:`~sequence.count`,
:meth:`~sequence.extend`, :meth:`~sequence.index`, :meth:`~sequence.insert`,
:meth:`~sequence.pop`, :meth:`~sequence.remove` và :meth:`~sequence.reverse`, giống như các đối tượng :class:`list` chuẩn của Python. Cuối cùng, các kiểu sequence nên triển khai phép cộng (nghĩa là nối) và phép nhân (nghĩa là lặp lại) bằng cách định nghĩa các phương thức
:meth:`~object.__add__`, :meth:`~object.__radd__`, :meth:`~object.__iadd__`,
:meth:`~object.__mul__`, :meth:`~object.__rmul__` và :meth:`~object.__imul__` được mô tả bên dưới; chúng không nên định nghĩa các toán tử số học khác.

Khuyến nghị rằng cả mapping lẫn sequence đều triển khai phương thức
:meth:`~object.__contains__` để cho phép sử dụng hiệu quả toán tử ``in``; với mapping, ``in`` nên tìm kiếm trong các khóa của mapping; với sequence, phương thức này nên tìm kiếm trong các giá trị. Cũng khuyến nghị rằng cả mapping lẫn sequence đều triển khai phương thức :meth:`~object.__iter__` để cho phép lặp hiệu quả qua container; với mapping, :meth:`!__iter__` nên lặp qua các khóa của đối tượng; với sequence, nó nên lặp qua các giá trị.

.. method:: object.__len__(self)

   .. index::
      pair: built-in function; len
      single: __bool__() (object method)

   Được gọi để triển khai hàm built-in :func:`len`. Phải trả về độ dài của đối tượng, là một số nguyên ``>=`` 0. Ngoài ra, một đối tượng không định nghĩa phương thức
   :meth:`~object.__bool__` và có phương thức :meth:`!__len__` trả về không thì được xem là false trong ngữ cảnh Boolean.

   .. impl-detail::

      Trong CPython, độ dài bắt buộc phải không vượt quá :data:`sys.maxsize`. Nếu độ dài lớn hơn :data:`!sys.maxsize`, một số tính năng (chẳng hạn như
      :func:`len` có thể phát sinh :exc:`OverflowError`. Để ngăn việc phát sinh
      :exc:`!OverflowError` thông qua kiểm tra giá trị chân lý, một đối tượng phải định nghĩa một
      phương thức :meth:`~object.__bool__`.


.. method:: object.__length_hint__(self)

   Được gọi để triển khai :func:`operator.length_hint`. Phải trả về độ dài ước tính của đối tượng (có thể lớn hơn hoặc nhỏ hơn độ dài thực tế). Độ dài phải là một số nguyên ``>=`` 0. Giá trị trả về cũng có thể là
   :data:`NotImplemented`, được xử lý giống như thể phương thức ``__length_hint__`` hoàn toàn không tồn tại. Phương thức này thuần túy là một tối ưu hóa và không bao giờ cần thiết để đảm bảo tính đúng đắn.

   .. versionadded:: 3.4


.. method:: object.__getitem__(self, subscript)

   Được gọi để triển khai phép truy cập chỉ mục *subscription*, tức là ``self[subscript]``. Xem :ref:`subscriptions` để biết chi tiết về cú pháp.

   Có hai loại đối tượng built-in hỗ trợ truy cập chỉ mục thông qua :meth:`!__getitem__`:

   - **sequence**, trong đó *subscript* (còn được gọi là
     :term:`index`) phải là một số nguyên hoặc một đối tượng :class:`slice`. Xem :ref:`tài liệu về sequence <datamodel-sequences>` để biết hành vi được mong đợi, bao gồm cả cách xử lý các đối tượng :class:`slice` và chỉ số âm.
   - **mapping**, trong đó *subscript* cũng được gọi là :term:`key`. Xem :ref:`tài liệu về mapping <datamodel-mappings>` để biết hành vi được mong đợi.

   Nếu *subscript* có kiểu không phù hợp, :meth:`!__getitem__` phải phát sinh :exc:`TypeError`. Nếu *subscript* có giá trị không phù hợp, :meth:`!__getitem__` phải phát sinh một :exc:`LookupError` hoặc một trong các lớp con của nó (:exc:`IndexError` cho sequence; :exc:`KeyError` cho mapping).

   .. index:: pair: object; slice

   .. note::

      Việc cắt lát được xử lý bởi :meth:`!__getitem__`, :meth:`~object.__setitem__` và :meth:`~object.__delitem__`. Một lời gọi như::

         a[1:2] = b

      được chuyển đổi thành::

         a[slice(1, 2, None)] = b

      và tương tự. Các thành phần slice bị thiếu luôn được điền bằng ``None``.

   .. note::

      Giao thức lặp sequence (ví dụ được dùng trong vòng lặp :keyword:`for`) kỳ vọng rằng một :exc:`IndexError` sẽ được phát sinh đối với các chỉ số không hợp lệ để có thể phát hiện đúng điểm kết thúc của một sequence.

   .. note::

      Khi :ref:`lập chỉ mục <subscriptions>` một *class*, phương thức lớp đặc biệt :meth:`~object.__class_getitem__` có thể được gọi thay cho
      :meth:`!__getitem__`. Xem :ref:`classgetitem-versus-getitem` để biết thêm chi tiết.


.. method:: object.__setitem__(self, key, value)

   Được gọi để triển khai việc gán cho ``self[key]``. Lưu ý tương tự như đối với
   :meth:`__getitem__`. Điều này chỉ nên được triển khai cho mapping nếu các đối tượng hỗ trợ thay đổi giá trị của các key, hoặc có thể thêm key mới, hoặc cho sequence nếu các phần tử có thể được thay thế. Cần phát sinh các exception tương tự cho các giá trị *key* không phù hợp như đối với phương thức :meth:`__getitem__`.


.. method:: object.__delitem__(self, key)

   Được gọi để triển khai việc xóa ``self[key]``. Lưu ý tương tự như đối với
   :meth:`__getitem__`. Điều này chỉ nên được triển khai cho mapping nếu các đối tượng hỗ trợ xóa key, hoặc cho sequence nếu các phần tử có thể bị xóa khỏi sequence. Cần phát sinh các exception tương tự cho các giá trị *key* không phù hợp như đối với phương thức :meth:`__getitem__`.


.. method:: object.__missing__(self, key)

   Được :class:`dict`\ .\ :meth:`__getitem__` gọi để triển khai ``self[key]`` cho các lớp con của dict khi khóa không có trong từ điển.


.. method:: object.__iter__(self)

   Phương thức này được gọi khi cần một :term:`iterator` cho một container. Phương thức này phải trả về một đối tượng iterator mới có thể lặp qua tất cả các đối tượng trong container. Đối với mapping, nó phải lặp qua các khóa của container.


.. method:: object.__reversed__(self)

   Được built-in :func:`reversed` gọi (nếu có) để triển khai việc lặp ngược. Phương thức này phải trả về một đối tượng iterator mới lặp qua tất cả các đối tượng trong container theo thứ tự ngược lại.

   Nếu không cung cấp phương thức :meth:`__reversed__`, built-in :func:`reversed` sẽ quay lại sử dụng giao thức sequence (:meth:`__len__` và
   :meth:`__getitem__`). Các đối tượng hỗ trợ giao thức sequence chỉ nên cung cấp :meth:`__reversed__` nếu chúng có thể cung cấp một cách triển khai hiệu quả hơn cách do :func:`reversed` cung cấp.


Các toán tử kiểm tra membership (:keyword:`in` và :keyword:`not in`) thường được triển khai bằng cách lặp qua một container. Tuy nhiên, các đối tượng container có thể cung cấp phương thức đặc biệt sau với cách triển khai hiệu quả hơn, đồng thời không yêu cầu đối tượng phải có thể lặp.

.. method:: object.__contains__(self, item)

   Được gọi để triển khai các toán tử kiểm tra membership. Phải trả về true nếu *item* nằm trong *self*, nếu không thì trả về false. Đối với các đối tượng mapping, phương thức này phải xét các khóa của mapping thay vì các giá trị hoặc các cặp khóa-item.

   Đối với các đối tượng không định nghĩa :meth:`__contains__`, phép kiểm tra thành viên trước tiên thử lặp qua :meth:`__iter__`, sau đó thử giao thức lặp sequence cũ qua :meth:`__getitem__`; xem :ref:`phần này trong tài liệu tham chiếu ngôn ngữ <membership-test-details>`.


.. _numeric-types:

Mô phỏng các kiểu số
--------------------

Có thể định nghĩa các phương thức sau để mô phỏng đối tượng số. Những phương thức tương ứng với các phép toán không được hỗ trợ bởi loại số cụ thể được triển khai (ví dụ: các phép toán bitwise đối với số không nguyên) nên được để không định nghĩa.


.. method:: object.__add__(self, other)
            object.__sub__(self, other) object.__mul__(self, other) object.__matmul__(self, other) object.__truediv__(self, other) object.__floordiv__(self, other) object.__mod__(self, other) object.__divmod__(self, other) object.__pow__(self, other[, modulo]) object.__lshift__(self, other) object.__rshift__(self, other) object.__and__(self, other) object.__xor__(self, other) object.__or__(self, other)

   .. index::
      pair: built-in function; divmod
      pair: built-in function; pow
      pair: built-in function; pow

   Các phương thức này được gọi để triển khai các phép toán số học nhị phân (``+``, ``-``, ``*``, ``@``, ``/``, ``//``, ``%``, :func:`divmod`,
   :func:`pow`, ``**``, ``<<``, ``>>``, ``&``, ``^``, ``|``). Ví dụ, để đánh giá biểu thức ``x + y``, trong đó *x* là một instance của lớp có phương thức :meth:`__add__`, ``type(x).__add__(x, y)`` được gọi. Phương thức
   :meth:`__divmod__` phải tương đương với việc sử dụng
   :meth:`__floordiv__` và :meth:`__mod__`; nó không nên liên quan đến
   :meth:`__truediv__`. Lưu ý rằng :meth:`__pow__` nên được định nghĩa để chấp nhận đối số thứ ba tùy chọn nếu cần hỗ trợ phiên bản ba đối số của hàm dựng sẵn :func:`pow`.

   Nếu một trong các phương thức đó không hỗ trợ phép toán với các đối số được cung cấp, phương thức đó nên trả về :data:`NotImplemented`.


.. method:: object.__radd__(self, other)
            object.__rsub__(self, other) object.__rmul__(self, other) object.__rmatmul__(self, other) object.__rtruediv__(self, other) object.__rfloordiv__(self, other) object.__rmod__(self, other) object.__rdivmod__(self, other) object.__rpow__(self, other[, modulo]) object.__rlshift__(self, other) object.__rrshift__(self, other) object.__rand__(self, other) object.__rxor__(self, other) object.__ror__(self, other)

   .. index::
      pair: built-in function; divmod
      pair: built-in function; pow

   Các phương thức này được gọi để triển khai các phép toán số học nhị phân (``+``, ``-``, ``*``, ``@``, ``/``, ``//``, ``%``, :func:`divmod`,
   :func:`pow`, ``**``, ``<<``, ``>>``, ``&``, ``^``, ``|``) với các toán hạng phản chiếu (hoán đổi). Các hàm này chỉ được gọi nếu các toán hạng có kiểu khác nhau, khi toán hạng bên trái không hỗ trợ phép toán tương ứng [#]_, hoặc lớp của toán hạng bên phải được dẫn xuất từ lớp của toán hạng bên trái. [#]_ Ví dụ, để đánh giá biểu thức ``x - y``, trong đó *y* là một thực thể của lớp có phương thức :meth:`__rsub__`, ``type(y).__rsub__(y, x)`` được gọi nếu ``type(x).__sub__(x, y)`` trả về :data:`NotImplemented` hoặc ``type(y)`` là một lớp con của ``type(x)``. [#]_

   Lưu ý rằng :meth:`__rpow__` nên được định nghĩa để chấp nhận đối số thứ ba tùy chọn nếu cần hỗ trợ phiên bản ba đối số của hàm dựng sẵn :func:`pow`.

   .. versionchanged:: 3.14

      Các :func:`pow` ba đối số hiện sẽ cố gọi :meth:`~object.__rpow__` nếu cần. Trước đây, phương thức này chỉ được gọi trong các :func:`!pow` hai đối số và toán tử lũy thừa nhị phân.

   .. note::

      Nếu kiểu của toán hạng bên phải là lớp con của kiểu của toán hạng bên trái và lớp con đó cung cấp một cách triển khai khác cho phương thức phản chiếu của phép toán, phương thức này sẽ được gọi trước phương thức không phản chiếu của toán hạng bên trái. Hành vi này cho phép các lớp con ghi đè các phép toán của tổ tiên chúng.

.. method:: object.__iadd__(self, other)
            object.__isub__(self, other) object.__imul__(self, other) object.__imatmul__(self, other) object.__itruediv__(self, other) object.__ifloordiv__(self, other) object.__imod__(self, other) object.__ipow__(self, other[, modulo]) object.__ilshift__(self, other) object.__irshift__(self, other) object.__iand__(self, other) object.__ixor__(self, other) object.__ior__(self, other)

   Các phương thức này được gọi để triển khai các phép gán số học tăng cường (``+=``, ``-=``, ``*=``, ``@=``, ``/=``, ``//=``, ``%=``, ``**=``, ``<<=``, ``>>=``, ``&=``, ``^=``, ``|=``). Các phương thức này nên cố thực hiện phép toán tại chỗ (sửa đổi *self*) và trả về kết quả (có thể là, nhưng không bắt buộc phải là, *self*). Nếu một phương thức cụ thể không được định nghĩa, hoặc nếu phương thức đó trả về :data:`NotImplemented`, phép gán tăng cường sẽ quay về dùng các phương thức thông thường. Ví dụ, nếu *x* là một instance của lớp có phương thức :meth:`__iadd__`, thì ``x += y`` tương đương với ``x = x.__iadd__(y)`` . Nếu :meth:`__iadd__` không tồn tại, hoặc nếu ``x.__iadd__(y)`` trả về :data:`!NotImplemented`, thì ``x.__add__(y)`` và ``y.__radd__(x)`` được xét đến, như khi đánh giá ``x + y``. Trong một số tình huống nhất định, phép gán tăng cường có thể gây ra các lỗi không mong muốn (xem
   :ref:`faq-augmented-assignment-tuple-error`), nhưng hành vi này thực tế là một phần của mô hình dữ liệu.


.. method:: object.__neg__(self)
            object.__pos__(self) object.__abs__(self) object.__invert__(self)

   .. index:: pair: built-in function; abs

   Được gọi để triển khai các phép toán số học một ngôi (``-``, ``+``, :func:`abs` và ``~``).


.. method:: object.__complex__(self)
            object.__int__(self) object.__float__(self)

   .. index::
      pair: built-in function; complex
      pair: built-in function; int
      pair: built-in function; float

   Được gọi để triển khai các hàm dựng sẵn :func:`complex`,
   :func:`int` và :func:`float`. Phải trả về một giá trị thuộc kiểu phù hợp.


.. method:: object.__index__(self)

   Được gọi để triển khai :func:`operator.index`, và bất cứ khi nào Python cần chuyển đổi đối tượng số sang đối tượng số nguyên mà không mất dữ liệu (chẳng hạn như trong slicing, hoặc trong các hàm dựng sẵn :func:`bin`, :func:`hex` và :func:`oct`). Sự hiện diện của phương thức này cho biết đối tượng số là một kiểu số nguyên. Phải trả về một số nguyên.

   Nếu :meth:`__int__`, :meth:`__float__` và :meth:`__complex__` không được định nghĩa, thì các hàm dựng sẵn tương ứng :func:`int`, :func:`float` và :func:`complex` sẽ dự phòng sang :meth:`__index__`.


.. method:: object.__round__(self, [,ndigits])
            object.__trunc__(self) object.__floor__(self) object.__ceil__(self)

   .. index:: pair: built-in function; round

   Được gọi để triển khai hàm dựng sẵn :func:`round` và các hàm :mod:`math` :func:`~math.trunc`, :func:`~math.floor` và :func:`~math.ceil`. Trừ khi *ndigits* được truyền cho :meth:`!__round__`, tất cả các phương thức này phải trả về giá trị của đối tượng được cắt ngắn thành một :class:`~numbers.Integral` (thông thường là một :class:`int`).

   .. versionchanged:: 3.14
      :func:`int` no longer delegates to the :meth:`~object.__trunc__` method.


.. _context-managers:

Context Manager của câu lệnh With
---------------------------------

:dfn:`context manager` là một đối tượng xác định ngữ cảnh runtime cần được thiết lập khi thực thi một câu lệnh :keyword:`with`. Context manager xử lý việc đi vào và thoát khỏi ngữ cảnh runtime mong muốn để thực thi khối mã. Context manager thường được gọi bằng cách sử dụng
câu lệnh :keyword:`!with` (được mô tả trong phần :ref:`with`), nhưng cũng có thể được sử dụng bằng cách gọi trực tiếp các phương thức của chúng.

.. index::
   pair: statement; with
   single: context manager

Các cách sử dụng điển hình của context manager bao gồm lưu và khôi phục nhiều loại trạng thái global, khóa và mở khóa tài nguyên, đóng các tệp đã mở, v.v.

Để biết thêm thông tin về context manager, xem :ref:`typecontextmanager`. Bản thân lớp :class:`object` không cung cấp các phương thức context manager.


.. method:: object.__enter__(self)

   Đi vào ngữ cảnh runtime liên quan đến đối tượng này. Câu lệnh :keyword:`with` sẽ gán giá trị trả về của phương thức này cho (các) target được chỉ định trong
   mệnh đề :keyword:`!as` của câu lệnh, nếu có.


.. method:: object.__exit__(self, exc_type, exc_value, traceback)

   Thoát khỏi context runtime liên quan đến đối tượng này. Các tham số mô tả exception đã khiến context bị thoát. Nếu context được thoát mà không có exception, cả ba đối số sẽ là :const:`None`.

   Nếu có một exception được cung cấp và phương thức muốn chặn exception đó (tức là ngăn nó được lan truyền), phương thức nên trả về một giá trị true. Nếu không, exception sẽ được xử lý bình thường khi thoát khỏi phương thức này.

   Lưu ý rằng các phương thức :meth:`~object.__exit__` không nên ném lại exception đã truyền vào; đây là trách nhiệm của caller.


.. seealso::

   :pep:`343` - Câu lệnh "with"
      Đặc tả, bối cảnh và ví dụ cho câu lệnh :keyword:`with` của Python.


.. _class-pattern-matching:

Tùy chỉnh đối số vị trí trong pattern matching của class
--------------------------------------------------------

Khi sử dụng tên class trong một pattern, theo mặc định không được phép dùng đối số vị trí trong pattern, tức là ``case MyClass(x, y)`` thường không hợp lệ nếu không có hỗ trợ đặc biệt trong ``MyClass``. Để có thể sử dụng kiểu pattern đó, class cần định nghĩa một thuộc tính *__match_args__*.

.. data:: object.__match_args__

   Biến lớp này có thể được gán một tuple các chuỗi. Khi lớp này được sử dụng trong một class pattern có các đối số vị trí, mỗi đối số vị trí sẽ được chuyển đổi thành một đối số từ khóa, sử dụng giá trị tương ứng trong *__match_args__* làm từ khóa. Việc không có thuộc tính này tương đương với việc đặt nó thành ``()``.

Ví dụ, nếu ``MyClass.__match_args__`` là ``("left", "center", "right")`` thì điều đó có nghĩa là ``case MyClass(x, y)`` tương đương với ``case MyClass(left=x, center=y)``. Lưu ý rằng số lượng đối số trong pattern phải nhỏ hơn hoặc bằng số phần tử trong *__match_args__*; nếu lớn hơn, lần thử khớp pattern sẽ phát sinh :exc:`TypeError`.

.. versionadded:: 3.10

.. seealso::

   :pep:`634` - Đối sánh mẫu cấu trúc
      Đặc tả cho câu lệnh ``match`` của Python.


.. _python-buffer-protocol:

Mô phỏng các kiểu buffer
------------------------

:ref:`buffer protocol <bufferobjects>` cung cấp cách để các đối tượng Python cung cấp quyền truy cập hiệu quả vào một mảng bộ nhớ cấp thấp. Protocol này được triển khai bởi các kiểu dựng sẵn như :class:`bytes` và :class:`memoryview`, đồng thời các thư viện bên thứ ba có thể định nghĩa thêm các kiểu buffer.

Mặc dù các kiểu buffer thường được triển khai bằng C, bạn cũng có thể triển khai protocol này bằng Python.

.. method:: object.__buffer__(self, flags)

   Được gọi khi một buffer được yêu cầu từ *self* (ví dụ, bởi
   :class:`memoryview` constructor). Đối số *flags* là một số nguyên biểu thị loại buffer được yêu cầu, chẳng hạn ảnh hưởng đến việc buffer trả về là chỉ đọc hay có thể ghi. :class:`inspect.BufferFlags` cung cấp một cách thuận tiện để diễn giải các cờ này. Phương thức phải trả về một đối tượng :class:`memoryview`.

   **An toàn luồng:** Trong Python :term:`free-threaded <free threading>`, các implementation phải quản lý mọi bộ đếm export nội bộ bằng các thao tác atomic. Phương thức phải an toàn khi được gọi đồng thời từ nhiều luồng, và dữ liệu nền tảng của buffer được trả về phải vẫn hợp lệ cho đến khi lời gọi :meth:`~object.__release_buffer__` tương ứng hoàn tất. Xem :ref:`thread-safety-memoryview` để biết chi tiết.

.. method:: object.__release_buffer__(self, buffer)

   Được gọi khi một buffer không còn cần thiết. Đối số *buffer* là một
   đối tượng :class:`memoryview` đã được trả về trước đó bởi
   :meth:`~object.__buffer__`. Phương thức phải giải phóng mọi tài nguyên liên kết với buffer. Phương thức này nên trả về ``None``.

   **An toàn luồng:** Trong Python :term:`free-threaded <free threading>`, mọi thao tác giảm bộ đếm export phải sử dụng các thao tác atomic. Việc dọn dẹp tài nguyên phải an toàn luồng, vì lần giải phóng cuối cùng có thể xảy ra đồng thời với các lần giải phóng từ những luồng khác.

   Các đối tượng buffer không cần thực hiện bất kỳ thao tác dọn dẹp nào thì không bắt buộc phải triển khai phương thức này.

.. versionadded:: 3.12

.. seealso::

   :pep:`688` - Giúp buffer protocol có thể truy cập được trong Python
      Giới thiệu các phương thức Python ``__buffer__`` và ``__release_buffer__``.

   :class:`collections.abc.Buffer`
      ABC cho các kiểu buffer.

Chú thích
---------

Các hàm, lớp và mô-đun có thể chứa :term:`annotations <annotation>`, là một cách để liên kết thông tin (thường là :term:`type hints <type hint>`) với một ký hiệu.

.. attribute:: object.__annotations__

   Thuộc tính này chứa các chú thích cho một đối tượng. Nó là
   :ref:`được đánh giá lười (lazily evaluated) <lazy-evaluation>`, vì vậy việc truy cập thuộc tính có thể thực thi mã tùy ý và phát sinh ngoại lệ. Nếu đánh giá thành công, thuộc tính được đặt thành một dictionary ánh xạ từ tên biến đến các annotation.

   .. versionchanged:: 3.14
      Annotation hiện được đánh giá lười.

.. method:: object.__annotate__(format)

   Một :term:`annotate function`. Trả về một đối tượng dictionary mới ánh xạ tên thuộc tính/tham số tới các giá trị annotation của chúng.

   Nhận một tham số format chỉ định định dạng mà các giá trị annotation sẽ được cung cấp. Nó phải là một thành viên của enum :class:`annotationlib.Format`, hoặc một số nguyên có giá trị tương ứng với một thành viên của enum.

   Nếu một hàm annotate không hỗ trợ format được yêu cầu, hàm đó phải phát sinh
   :exc:`NotImplementedError`. Các hàm annotate phải luôn hỗ trợ
   format :attr:`~annotationlib.Format.VALUE`; chúng không được phát sinh
   :exc:`NotImplementedError()` khi được gọi với định dạng này.

   Khi được gọi với định dạng :attr:`~annotationlib.Format.VALUE`, một hàm annotate có thể phát sinh
   :exc:`NameError`; hàm này không được phát sinh :exc:`!NameError` khi được gọi yêu cầu bất kỳ định dạng nào khác.

   Nếu một đối tượng không có annotation nào, tốt nhất nên đặt :attr:`~object.__annotate__` thành ``None`` (không thể xóa nó), thay vì đặt thành một hàm trả về dict rỗng.

   .. versionadded:: 3.14

.. seealso::

   :pep:`649` --- Đánh giá trì hoãn annotation bằng descriptor
      Giới thiệu việc đánh giá lười (lazy evaluation) các annotation và hàm ``__annotate__``.


.. _special-lookup:

Tra cứu special method
----------------------

Đối với các lớp tùy chỉnh, những lời gọi ngầm các phương thức đặc biệt chỉ được đảm bảo hoạt động đúng nếu được định nghĩa trên type của đối tượng, không phải trong từ điển instance của đối tượng. Hành vi đó là lý do đoạn mã sau phát sinh một ngoại lệ::

   >>> class C:
   ...     pass
   ...
   >>> c = C()
   >>> c.__len__ = lambda: 5
   >>> len(c)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: object of type 'C' has no len()

Cơ sở lý luận đằng sau hành vi này nằm ở một số phương thức đặc biệt như :meth:`~object.__hash__` và :meth:`~object.__repr__`, vốn được mọi đối tượng, bao gồm cả các đối tượng type, triển khai. Nếu việc tra cứu ngầm các phương thức này sử dụng quy trình tra cứu thông thường, chúng sẽ thất bại khi được gọi trên chính đối tượng type::

   >>> 1 .__hash__() == hash(1)
   True
   >>> int.__hash__() == hash(int)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: descriptor '__hash__' of 'int' object needs an argument

Việc cố gọi không đúng cách một phương thức unbound của một lớp theo cách này đôi khi được gọi là 'metaclass confusion', và được tránh bằng cách bỏ qua instance khi tra cứu các phương thức đặc biệt::

   >>> type(1).__hash__(1) == hash(1)
   True
   >>> type(int).__hash__(int) == hash(int)
   True

Ngoài việc bỏ qua mọi thuộc tính instance để đảm bảo tính đúng đắn, việc tra cứu ngầm phương thức đặc biệt nói chung cũng bỏ qua
phương thức :meth:`~object.__getattribute__` ngay cả của metaclass của đối tượng::

   >>> class Meta(type):
   ...     def __getattribute__(*args):
   ...         print("Metaclass getattribute invoked")
   ...         return type.__getattribute__(*args)
   ...
   >>> class C(object, metaclass=Meta):
   ...     def __len__(self):
   ...         return 10
   ...     def __getattribute__(*args):
   ...         print("Class getattribute invoked")
   ...         return object.__getattribute__(*args)
   ...
   >>> c = C()
   >>> c.__len__()                 # Tra cứu tường minh qua instance
   Class getattribute invoked
   10
   >>> type(c).__len__(c)          # Tra cứu tường minh qua type
   Metaclass getattribute invoked
   10
   >>> len(c)                      # Tra cứu ngầm định
   10

Việc bỏ qua cơ chế :meth:`~object.__getattribute__` theo cách này tạo ra đáng kể cơ hội tối ưu hoá tốc độ trong interpreter, đổi lại là giảm một phần tính linh hoạt khi xử lý các phương thức đặc biệt (phương thức đặc biệt *phải* được đặt trên chính đối tượng lớp để được interpreter gọi một cách nhất quán).


.. index::
   single: coroutine

Coroutine
=========


Đối tượng Awaitable
-------------------

Một đối tượng :term:`awaitable` thường triển khai một phương thức :meth:`~object.__await__`.
:term:`Các đối tượng coroutine <coroutine>` được trả về từ các hàm :keyword:`async def` là awaitable.

.. note::

   Các đối tượng :term:`generator iterator` được trả về từ các generator được trang trí bằng :func:`types.coroutine` cũng là awaitable, nhưng chúng không triển khai :meth:`~object.__await__`.

.. method:: object.__await__(self)

   Phải trả về một :term:`iterator`. Nên được dùng để triển khai
   các đối tượng :term:`awaitable`. Ví dụ, :class:`asyncio.Future` triển khai phương thức này để tương thích với biểu thức :keyword:`await`. Bản thân lớp :class:`object` không phải là awaitable và không cung cấp phương thức này.

   .. note::

      Ngôn ngữ không đặt ra bất kỳ hạn chế nào đối với kiểu hoặc giá trị của các đối tượng được yield bởi iterator do ``__await__`` trả về, vì điều này phụ thuộc vào cách triển khai của framework thực thi bất đồng bộ (ví dụ: :mod:`asyncio`) sẽ quản lý đối tượng :term:`awaitable`.


.. versionadded:: 3.5

.. seealso:: :pep:`492` để biết thêm thông tin về các đối tượng awaitable.


.. _coroutine-objects:

Đối tượng Coroutine
-------------------

:term:`Đối tượng coroutine <coroutine>` là các đối tượng :term:`awaitable`. Việc thực thi một coroutine có thể được điều khiển bằng cách gọi :meth:`~object.__await__` và lặp qua kết quả. Khi coroutine thực thi xong và trả về, iterator sẽ phát sinh :exc:`StopIteration`, và ngoại lệ này
có thuộc tính :attr:`~StopIteration.value` chứa giá trị trả về. Nếu coroutine phát sinh một ngoại lệ, ngoại lệ đó sẽ được iterator truyền đi. Coroutine không nên trực tiếp phát sinh các ngoại lệ :exc:`StopIteration` chưa được xử lý.

Coroutine cũng có các phương thức được liệt kê bên dưới, tương tự như các phương thức của generator (xem :ref:`generator-methods`). Tuy nhiên, không giống generator, coroutine không trực tiếp hỗ trợ việc lặp.

Coroutine là :ref:`generic <generics>` theo các kiểu của giá trị yield, send và return tương ứng.

.. versionchanged:: 3.5.2
   Đây là một :exc:`RuntimeError` khi await một coroutine nhiều hơn một lần.


.. method:: coroutine.send(value)

   Bắt đầu hoặc tiếp tục thực thi coroutine. Nếu *value* là ``None``, điều này tương đương với việc tiến iterator được trả về bởi
   :meth:`~object.__await__`. Nếu *value* không phải là ``None``, phương thức này ủy quyền cho phương thức :meth:`~generator.send` của iterator đã khiến coroutine tạm dừng. Kết quả (giá trị return,
   :exc:`StopIteration`, hoặc ngoại lệ khác) giống như khi lặp qua giá trị return của :meth:`!__await__`, được mô tả ở trên.

.. method:: coroutine.throw(value)
            coroutine.throw(type[, value[, traceback]])

   Phát sinh ngoại lệ đã chỉ định trong coroutine. Phương thức này ủy quyền cho phương thức :meth:`~generator.throw` của iterator đã khiến coroutine bị tạm dừng, nếu iterator đó có phương thức này. Nếu không, ngoại lệ được phát sinh tại điểm tạm dừng. Kết quả (giá trị trả về, :exc:`StopIteration` hoặc ngoại lệ khác) giống như khi lặp qua giá trị trả về :meth:`~object.__await__` được mô tả ở trên. Nếu ngoại lệ không được bắt trong coroutine, nó sẽ truyền ngược về caller.

   .. versionchanged:: 3.12

      Chữ ký thứ hai \(type\[, value\[, traceback\]\]\) đã lỗi thời và có thể bị loại bỏ trong một phiên bản Python tương lai.

.. method:: coroutine.close()

   Khiến coroutine tự dọn dẹp và thoát. Nếu coroutine đang bị tạm dừng, phương thức này trước tiên ủy quyền cho phương thức :meth:`~generator.close` của iterator đã khiến coroutine bị tạm dừng, nếu iterator đó có phương thức này. Sau đó, nó phát sinh :exc:`GeneratorExit` tại điểm tạm dừng, khiến coroutine ngay lập tức tự dọn dẹp. Cuối cùng, coroutine được đánh dấu là đã thực thi xong, ngay cả khi nó chưa từng được khởi chạy.

   Các đối tượng coroutine được tự động đóng bằng quy trình ở trên khi chúng sắp bị hủy.

.. _async-iterators:

Các Iterator Bất đồng bộ
------------------------

Một *iterator bất đồng bộ* có thể gọi code bất đồng bộ trong phương thức ``__anext__`` của nó.

Các iterator bất đồng bộ có thể được dùng trong một câu lệnh :keyword:`async for`.

Bản thân lớp :class:`object` không cung cấp các phương thức này.


.. method:: object.__aiter__(self)

   Phải trả về một đối tượng *asynchronous iterator*.

.. method:: object.__anext__(self)

   Phải trả về một *awaitable* cho kết quả là giá trị tiếp theo của iterator. Phải phát sinh lỗi :exc:`StopAsyncIteration` khi quá trình lặp kết thúc.

Ví dụ về một đối tượng iterable bất đồng bộ::

    class Reader:
        async def readline(self):
            ...

        def __aiter__(self):
            return self

        async def __anext__(self):
            val = await self.readline()
            if val == b'':
                raise StopAsyncIteration
            return val

.. versionadded:: 3.5

.. versionchanged:: 3.7
   Trước Python 3.7, :meth:`~object.__aiter__` có thể trả về một *awaitable* sẽ resolve thành một
   :term:`asynchronous iterator <asynchronous iterator>`.

   Kể từ Python 3.7, :meth:`~object.__aiter__` phải trả về một đối tượng asynchronous iterator. Việc trả về bất kỳ thứ gì khác sẽ dẫn đến lỗi :exc:`TypeError`.


.. _async-context-managers:

Trình quản lý ngữ cảnh bất đồng bộ
----------------------------------

Một *trình quản lý ngữ cảnh bất đồng bộ* là một *trình quản lý ngữ cảnh* có thể tạm dừng việc thực thi trong các phương thức ``__aenter__`` và ``__aexit__`` của nó.

Có thể sử dụng trình quản lý ngữ cảnh bất đồng bộ trong một câu lệnh :keyword:`async with`.

Bản thân lớp :class:`object` không cung cấp các phương thức này.

.. method:: object.__aenter__(self)

   Về ngữ nghĩa tương tự :meth:`~object.__enter__`, điểm khác biệt duy nhất là nó phải trả về một *awaitable*.

.. method:: object.__aexit__(self, exc_type, exc_value, traceback)

   Về ngữ nghĩa tương tự :meth:`~object.__exit__`, điểm khác biệt duy nhất là nó phải trả về một *awaitable*.

Ví dụ về một lớp trình quản lý ngữ cảnh bất đồng bộ::

    class AsyncContextManager:
        async def __aenter__(self):
            await log('entering context')

        async def __aexit__(self, exc_type, exc, tb):
            await log('exiting context')

.. versionadded:: 3.5


.. rubric:: Chú thích cuối trang

.. [#] Trong một số trường hợp, *có thể* thay đổi kiểu của một đối tượng, theo những điều kiện được kiểm soát nhất định. Tuy nhiên, nhìn chung đây không phải là ý hay, vì có thể dẫn đến những hành vi rất lạ nếu được xử lý không đúng cách.

.. [#] Các phương thức :meth:`~object.__hash__`, :meth:`~object.__iter__`,
   :meth:`~object.__reversed__`, :meth:`~object.__contains__`,
   :meth:`~object.__class_getitem__` và :meth:`~os.PathLike.__fspath__` được xử lý đặc biệt cho việc này. Các phương thức khác vẫn sẽ phát sinh :exc:`TypeError`, nhưng có thể làm vậy bằng cách dựa vào hành vi rằng ``None`` không thể gọi được.

.. [#] "Không hỗ trợ" ở đây nghĩa là lớp không có phương thức như vậy, hoặc phương thức trả về :data:`NotImplemented`. Không đặt phương thức thành ``None`` nếu bạn muốn buộc quay lui về phương thức phản chiếu của toán hạng bên phải—thay vào đó, điều này sẽ có tác dụng ngược lại là *chặn* rõ ràng việc quay lui đó.

.. [#] Đối với các toán hạng cùng kiểu, giả định rằng nếu phương thức không phản chiếu (chẳng hạn như :meth:`~object.__add__`) thất bại thì phép toán không được hỗ trợ, vì vậy phương thức phản chiếu không được gọi.

.. [#] Nếu kiểu của toán hạng bên phải là lớp con của kiểu của toán hạng bên trái, việc phương thức phản chiếu được ưu tiên cho phép các lớp con ghi đè các phép toán của tổ tiên.
