:mod:`!difflib` --- Các công cụ hỗ trợ tính toán độ chênh lệch
==============================================================

.. module:: difflib
   :synopsis: Các công cụ hỗ trợ tính toán sự khác biệt giữa các đối tượng.

.. moduleauthor:: Tim Peters <tim_one@users.sourceforge.net>
.. sectionauthor:: Tim Peters <tim_one@users.sourceforge.net>
.. Markup by Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/difflib.py`

.. testsetup::

   import sys
   from difflib import *

--------------

Mô-đun này cung cấp các lớp và hàm để so sánh các chuỗi. Hầu hết chúng so sánh các chuỗi dòng văn bản (ví dụ: danh sách chuỗi hoặc :term:`đối tượng file <file object>`) và tạo ra các :dfn:`diff` -- các báo cáo về những điểm khác biệt. Có thể tạo diff ở nhiều định dạng khác nhau, bao gồm HTML, diff ngữ cảnh và diff thống nhất -- những định dạng được tạo bởi các công cụ như
:manpage:`diff <diff(1)>` và :manpage:`git diff <git-diff(1)>`.

Việc so sánh được thực hiện bằng một thuật toán đối sánh được triển khai trong
:class:`SequenceMatcher` -- một lớp linh hoạt để so sánh các cặp chuỗi thuộc mọi kiểu, không chỉ văn bản, miễn là các phần tử của chuỗi là
:term:`hashable`.


.. _difflib-junk:

Heuristic xác định phần tử rác
------------------------------

:mod:`!difflib` sử dụng một heuristic :dfn:`rác`: một số phần tử được xem là
:dfn:`rác`, và bị bỏ qua khi tìm kiếm các điểm tương đồng. Lý tưởng nhất là đây phải là những phần tử không đáng chú ý hoặc phổ biến, chẳng hạn như dòng trống hoặc khoảng trắng.

Heuristic này có thể tăng tốc thuật toán (vì giảm số tổ hợp có thể có) và tạo ra các kết quả dễ hiểu hơn đối với con người (thường ngắt tại khoảng trắng). Tuy nhiên, nó cũng có thể gây ra các trường hợp bất thường:

- Các phần tử rác được chọn không phù hợp có thể tạo ra kết quả **lớn** ngoài dự kiến (nhưng vẫn chính xác).
- Heuristic mặc định là **bất đối xứng**: chỉ chuỗi thứ hai được kiểm tra khi xác định phần tử nào được xem là rác, vì vậy việc so sánh A với B có thể cho kết quả khác với việc so sánh B với A rồi đảo ngược kết quả.

Theo mặc định, nếu chuỗi đầu vào thứ hai có ít nhất 200 phần tử, các phần tử chiếm hơn 1% trong số đó được xem là *rác*.

Tùy thuộc vào dữ liệu của bạn, bạn nên cân nhắc tắt heuristic này (bằng cách đặt đối số :class:`~difflib.SequenceMatcher`'s *autojunk* của ``False``) hoặc tinh chỉnh nó (bằng cách sử dụng đối số *isjunk*, có thể là một trong các
:ref:`hàm được định nghĩa sẵn <difflib-isjunk-functions>`).


Thuật toán :mod:`!difflib`
--------------------------

Thuật toán được sử dụng trong :class:`SequenceMatcher` có trước một thuật toán được Ratcliff và Obershelp công bố vào cuối những năm 1980, đồng thời cũng cầu kỳ hơn một chút so với thuật toán đó. Họ đặt cho thuật toán này cái tên cường điệu là "so khớp mẫu gestalt". Ý tưởng là tìm dãy con liên tiếp dài nhất cùng xuất hiện trong cả hai đầu vào, sau đó xử lý đệ quy các phần của các dãy nằm bên trái và bên phải dãy con khớp nhau.

.. seealso::

   `So khớp mẫu: Phương pháp Gestalt <https://jacobfilipp.com/DrDobbs/articles/DDJ/1988/8807/8807c/8807c.htm>`_
      Thảo luận về một thuật toán tương tự của John W. Ratcliff và D. E. Metzener. Bài viết này được đăng trên Dr. Dobb's Journal vào tháng 7 năm 1988.

Là một phần mở rộng của thuật toán Ratcliff và Obershelp, :mod:`!difflib` tìm kiếm dãy con liên tiếp dài nhất *không chứa phần tử rác*. Xem phần :ref:`difflib-junk` để biết chi tiết.

.. impl-detail:: Timing

   Thuật toán Ratcliff-Obershelp cơ bản có độ phức tạp thời gian bậc ba trong trường hợp xấu nhất và bậc hai trong trường hợp kỳ vọng.
   Thuật toán của :mod:`difflib` có độ phức tạp thời gian bậc hai trong trường hợp xấu nhất, còn hành vi trong trường hợp kỳ vọng phụ thuộc theo cách phức tạp vào số phần tử chung giữa các chuỗi; thời gian trong trường hợp tốt nhất là tuyến tính.


.. _difflib-diff-generation:

Tạo diff
--------

.. _differ-objects:

.. class:: Differ

   Đây là một lớp dùng để so sánh các chuỗi dòng văn bản và tạo ra các khác biệt hoặc delta mà con người có thể đọc được. Differ sử dụng :class:`SequenceMatcher` để so sánh các chuỗi dòng, cũng như để so sánh các chuỗi ký tự trong những dòng tương tự (gần khớp).

   Mỗi dòng trong delta của :class:`Differ` bắt đầu bằng một mã gồm hai chữ cái:

   +----------+------------------------------------------+
   | Mã       | Ý nghĩa                                  |
   +==========+==========================================+
   | ``'- '`` | dòng chỉ có trong chuỗi 1                |
   +----------+------------------------------------------+
   | ``'+ '`` | dòng chỉ có trong chuỗi 2                |
   +----------+------------------------------------------+
   | ``'  '`` | dòng chung cho cả hai chuỗi              |
   +----------+------------------------------------------+
   | ``'? '`` | dòng không có trong cả hai chuỗi đầu vào |
   +----------+------------------------------------------+

   Các dòng bắt đầu bằng '``?``' cố gắng hướng mắt người đọc đến những khác biệt trong dòng và không có trong cả hai chuỗi đầu vào. Những dòng này có thể gây nhầm lẫn nếu các chuỗi chứa ký tự khoảng trắng, chẳng hạn như dấu cách, tab hoặc ngắt dòng.

   Lưu ý rằng các phần chênh lệch do :class:`Differ`\  tạo ra không khẳng định là các diff **tối thiểu**. Ngược lại, diff tối thiểu thường phản trực giác đối với con người, vì chúng đồng bộ ở bất kỳ vị trí nào có thể, đôi khi tại các kết quả khớp tình cờ cách nhau 100 trang. Việc giới hạn các điểm đồng bộ vào những kết quả khớp liên tiếp sẽ duy trì một mức độ cục bộ nhất định, nhưng đôi khi phải trả giá bằng việc tạo ra diff dài hơn.

   Lớp :class:`Differ` có constructor sau đây:

   .. method:: __init__(linejunk=None, charjunk=None)

      Các tham số từ khóa tùy chọn *linejunk* và *charjunk* dùng cho các hàm lọc (hoặc ``None``):

      *linejunk*: Một hàm nhận một đối số chuỗi duy nhất và trả về true nếu chuỗi đó là rác. Giá trị mặc định là ``None``, nghĩa là không có dòng nào được xem là rác.

      *charjunk*: Một hàm nhận một đối số ký tự duy nhất (một chuỗi có độ dài 1) và trả về true nếu ký tự đó là rác. Giá trị mặc định là ``None``, nghĩa là không có ký tự nào được xem là rác.

      Các hàm lọc nội dung rác này giúp tăng tốc quá trình so khớp để tìm ra khác biệt và không khiến bất kỳ dòng hoặc ký tự khác biệt nào bị bỏ qua. Đọc phần mô tả về
      tham số *isjunk* của phương thức :meth:`~SequenceMatcher.find_longest_match` để biết thêm.

   Các đối tượng :class:`Differ` được sử dụng (các delta được tạo ra) thông qua một phương thức duy nhất:


   .. method:: Differ.compare(a, b)

      So sánh hai chuỗi dòng và tạo delta (một chuỗi các dòng).

      Mỗi chuỗi phải chứa các chuỗi riêng lẻ trên một dòng và kết thúc bằng ký tự xuống dòng. Có thể lấy các chuỗi như vậy từ
      phương thức :meth:`~io.IOBase.readlines` của các đối tượng giống tệp. Delta được tạo cũng bao gồm các chuỗi kết thúc bằng ký tự xuống dòng, sẵn sàng được in nguyên trạng bằng phương thức :meth:`~io.IOBase.writelines` của một đối tượng giống tệp.

.. class:: HtmlDiff

   Có thể dùng lớp này để tạo một bảng HTML (hoặc một tệp HTML hoàn chỉnh chứa bảng) hiển thị so sánh văn bản theo từng dòng, đặt cạnh nhau, với phần đánh dấu các thay đổi giữa các dòng và trong từng dòng. Có thể tạo bảng ở chế độ khác biệt đầy đủ hoặc khác biệt theo ngữ cảnh.

   .. warning::

      Các ký tự xuống dòng ở cuối sẽ bị loại bỏ trước khi tạo diff, vì vậy kết quả có thể không đầy đủ. Xem :gh:`71896` để biết chi tiết.

   Hàm khởi tạo của lớp này là:


   .. method:: __init__(tabsize=8, wrapcolumn=None, linejunk=None, charjunk=IS_CHARACTER_JUNK)

      Khởi tạo một thực thể của :class:`HtmlDiff`.

      *tabsize* là một đối số từ khóa tùy chọn dùng để chỉ định khoảng cách giữa các điểm dừng tab và mặc định là ``8``.

      *wrapcolumn* là một keyword tùy chọn dùng để chỉ định số cột tại đó các dòng được ngắt và bao dòng; mặc định là ``None``, nghĩa là các dòng không được bao.

      *linejunk* và *charjunk* là các đối số keyword tùy chọn được truyền vào :func:`ndiff` (được :class:`HtmlDiff` sử dụng để tạo các điểm khác biệt HTML hiển thị cạnh nhau). Xem
      :func:`ndiff` tài liệu để biết các giá trị mặc định và mô tả của đối số.

   Các phương thức sau là public:

   .. method:: make_file(fromlines, tolines, fromdesc='', todesc='', context=False, \
                         numlines=5, *, charset='utf-8')

      So sánh *fromlines* và *tolines* (các danh sách chuỗi), rồi trả về một chuỗi là một tệp HTML hoàn chỉnh chứa bảng hiển thị các điểm khác biệt giữa từng dòng, trong đó các thay đổi giữa các dòng và trong từng dòng được làm nổi bật.

      *fromdesc* và *todesc* là các đối số keyword tùy chọn dùng để chỉ định chuỗi tiêu đề cột của tệp nguồn và tệp đích (cả hai mặc định là chuỗi rỗng).

      *context* và *numlines* đều là các đối số từ khóa tùy chọn. Đặt *context* thành ``True`` khi cần hiển thị các khác biệt theo ngữ cảnh; nếu không, mặc định là ``False`` để hiển thị toàn bộ các tệp. *numlines* mặc định là ``5``. Khi *context* là ``True``, *numlines* kiểm soát số dòng ngữ cảnh bao quanh phần đánh dấu khác biệt. Khi *context* là ``False``, *numlines* kiểm soát số dòng được hiển thị trước phần đánh dấu khác biệt khi sử dụng các siêu liên kết "next" (đặt thành 0 sẽ khiến các siêu liên kết "next" đặt phần đánh dấu khác biệt tiếp theo ở đầu trình duyệt mà không có ngữ cảnh đứng trước).

      .. note::
         *fromdesc* và *todesc* được diễn giải dưới dạng HTML chưa escape và cần được escape đúng cách khi nhận dữ liệu đầu vào từ các nguồn không đáng tin cậy.

      .. versionchanged:: 3.5
         Đối số chỉ có từ khóa *charset* đã được thêm vào.  Charset mặc định của tài liệu HTML đã thay đổi từ ``'ISO-8859-1'`` thành ``'utf-8'``.

   .. method:: make_table(fromlines, tolines, fromdesc='', todesc='', context=False, numlines=5)

      So sánh *fromlines* và *tolines* (các danh sách chuỗi) rồi trả về một chuỗi là bảng HTML hoàn chỉnh, hiển thị các khác biệt theo từng dòng với những thay đổi giữa các dòng và trong từng dòng được đánh dấu.

      Các đối số của phương thức này giống với các đối số của phương thức :meth:`make_file`.



.. function:: context_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')

   So sánh *a* và *b* (các danh sách chuỗi); trả về một delta (một :term:`generator` tạo ra các dòng delta) ở định dạng context diff.

   Context diff là cách ngắn gọn để chỉ hiển thị những dòng đã thay đổi cùng với một vài dòng ngữ cảnh. Các thay đổi được hiển thị theo kiểu trước/sau. Số dòng ngữ cảnh được đặt bằng *n*, mặc định là ba.

   Theo mặc định, các dòng điều khiển diff (những dòng có ``***`` hoặc ``---``) được tạo với ký tự xuống dòng ở cuối. Điều này hữu ích để các đầu vào được tạo từ
   :func:`io.IOBase.readlines` tạo ra các bản diff phù hợp để sử dụng với
   :func:`io.IOBase.writelines` vì cả đầu vào và đầu ra đều có ký tự xuống dòng ở cuối.

   Đối với các đầu vào không có ký tự xuống dòng ở cuối, hãy đặt đối số *lineterm* thành ``""`` để đầu ra luôn không có ký tự xuống dòng.

   Định dạng context diff thường có phần header chứa tên tệp và thời gian sửa đổi. Có thể chỉ định một hoặc tất cả các giá trị này bằng các chuỗi cho *fromfile*, *tofile*, *fromfiledate* và *tofiledate*. Thời gian sửa đổi thường được biểu diễn theo định dạng ISO 8601. Nếu không được chỉ định, các chuỗi này mặc định là chuỗi rỗng.

      >>> import sys
      >>> from difflib import *
      >>> s1 = ['bacon\n', 'eggs\n', 'ham\n', 'guido\n']
      >>> s2 = ['python\n', 'eggy\n', 'hamster\n', 'guido\n']
      >>> sys.stdout.writelines(context_diff(s1, s2, fromfile='before.py',
      ...                        tofile='after.py'))
      *** before.py
      --- after.py
      ***************
      *** 1,4 ****
      ! bacon
      ! eggs
      ! ham
        guido
      --- 1,4 ----
      ! python
      ! eggy
      ! hamster
        guido

   Xem :ref:`difflib-interface` để biết ví dụ chi tiết hơn.


.. function:: get_close_matches(word, possibilities, n=3, cutoff=0.6)

   Trả về danh sách các kết quả khớp "đủ tốt" nhất. *word* là một sequence cần tìm các kết quả khớp gần (thường là một string), còn *possibilities* là danh sách các sequence dùng để đối chiếu với *word* (thường là một danh sách string).

   Đối số tùy chọn *n* (mặc định là ``3``) là số lượng tối đa các kết quả khớp gần nhất cần trả về; *n* phải lớn hơn ``0``.

   Đối số tùy chọn *cutoff* (mặc định là ``0.6``) là một số thực trong khoảng [0, 1]. Các khả năng không đạt mức tương đồng tối thiểu đó với *word* sẽ bị bỏ qua.

   Các kết quả khớp tốt nhất (không quá *n*) trong số các khả năng sẽ được trả về trong một danh sách, được sắp xếp theo điểm tương đồng, với kết quả tương đồng nhất ở trước.

      >>> get_close_matches('appel', ['ape', 'apple', 'peach', 'puppy'])
      ['apple', 'ape']
      >>> import keyword
      >>> get_close_matches('wheel', keyword.kwlist)
      ['while']
      >>> get_close_matches('pineapple', keyword.kwlist)
      []
      >>> get_close_matches('accept', keyword.kwlist)
      ['except']


.. function:: ndiff(a, b, linejunk=None, charjunk=IS_CHARACTER_JUNK)

   So sánh *a* và *b* (các danh sách chuỗi); trả về một delta theo kiểu :class:`Differ`\  (một :term:`generator` tạo ra các dòng delta).

   Các tham số keyword tùy chọn *linejunk* và *charjunk* là các hàm lọc (hoặc ``None``):

   *linejunk*: Một hàm nhận một đối số chuỗi duy nhất và trả về true nếu chuỗi đó là junk, hoặc false nếu không phải. Giá trị mặc định là ``None``. Ngoài ra còn có hàm cấp module :func:`IS_LINE_JUNK`, dùng để lọc các dòng không có ký tự hiển thị, ngoại trừ tối đa một ký tự dấu thăng (``'#'``) -- tuy nhiên, lớp :class:`SequenceMatcher` cơ sở thực hiện phân tích động để xác định những dòng xuất hiện quá thường xuyên đến mức tạo thành nhiễu, và cách này thường hiệu quả hơn so với việc sử dụng hàm này.

   *charjunk*: Một hàm nhận một ký tự (một chuỗi có độ dài 1) và trả về true nếu ký tự đó là junk, hoặc false nếu không phải. Giá trị mặc định là hàm cấp module :func:`IS_CHARACTER_JUNK`, dùng để lọc các ký tự khoảng trắng (dấu cách hoặc tab; không nên đưa ký tự xuống dòng vào hàm này!).

      >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(keepends=True),
      ...              'ore\ntree\nemu\n'.splitlines(keepends=True))
      >>> print(''.join(diff), end="")
      - one
      ?  ^
      + ore
      ?  ^
      - two
      - three
      ?  -
      + tree
      + emu


.. function:: restore(sequence, which)

   Trả về một trong hai chuỗi đã tạo ra delta.

   Với một *chuỗi* được tạo bởi :meth:`Differ.compare` hoặc :func:`ndiff`, trích xuất các dòng bắt nguồn từ tệp 1 hoặc 2 (tham số *which*), đồng thời loại bỏ tiền tố dòng.

   Ví dụ:

      >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(keepends=True),
      ...              'ore\ntree\nemu\n'.splitlines(keepends=True))
      >>> diff = list(diff) # chuyển delta đã tạo thành một danh sách
      >>> print(''.join(restore(diff, 1)), end="")
      one
      two
      three
      >>> print(''.join(restore(diff, 2)), end="")
      ore
      tree
      emu


.. function:: unified_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')

   So sánh *a* và *b* (các danh sách chuỗi); trả về một delta (một :term:`generator` tạo ra các dòng delta) ở định dạng unified diff.

   Unified diff là một cách ngắn gọn để chỉ hiển thị các dòng đã thay đổi cùng với một vài dòng ngữ cảnh. Các thay đổi được hiển thị theo kiểu inline (thay vì các khối before/after riêng biệt). Số lượng dòng ngữ cảnh được đặt bởi *n*, mặc định là ba.

   Theo mặc định, các dòng điều khiển diff (những dòng có ``---``, ``+++``, hoặc ``@@``) được tạo với một ký tự xuống dòng ở cuối. Điều này hữu ích để các đầu vào được tạo từ
   :func:`io.IOBase.readlines` tạo ra các bản diff phù hợp để sử dụng với
   :func:`io.IOBase.writelines` vì cả đầu vào và đầu ra đều có ký tự xuống dòng ở cuối.

   Đối với các đầu vào không có ký tự xuống dòng ở cuối, hãy đặt đối số *lineterm* thành ``""`` để đầu ra luôn không có ký tự xuống dòng.

   Định dạng unified diff thường có phần header chứa tên tệp và thời gian sửa đổi. Bạn có thể chỉ định một, một số hoặc tất cả các thông tin này bằng các chuỗi cho *fromfile*, *tofile*, *fromfiledate* và *tofiledate*. Thời gian sửa đổi thường được biểu diễn theo định dạng ISO 8601. Nếu không được chỉ định, các chuỗi sẽ mặc định là chuỗi trống.

      >>> s1 = ['bacon\n', 'eggs\n', 'ham\n', 'guido\n']
      >>> s2 = ['python\n', 'eggy\n', 'hamster\n', 'guido\n']
      >>> sys.stdout.writelines(unified_diff(s1, s2, fromfile='before.py', tofile='after.py'))
      --- before.py
      +++ after.py
      @@ -1,4 +1,4 @@
      -bacon
      -eggs
      -ham
      +python
      +eggy
      +hamster
       guido

   Xem :ref:`difflib-interface` để biết ví dụ chi tiết hơn.

.. function:: diff_bytes(dfunc, a, b, fromfile=b'', tofile=b'', fromfiledate=b'', tofiledate=b'', n=3, lineterm=b'\n')

   So sánh *a* và *b* (các danh sách đối tượng bytes) bằng *dfunc*; tạo ra một chuỗi các dòng delta (cũng là bytes) theo định dạng được trả về bởi *dfunc*. *dfunc* phải là một callable, thường là :func:`unified_diff` hoặc
   :func:`context_diff`.

   Cho phép bạn so sánh dữ liệu có encoding không xác định hoặc không nhất quán. Tất cả đầu vào ngoại trừ *n* phải là đối tượng bytes, không phải str. Hàm này hoạt động bằng cách chuyển đổi tất cả đầu vào (ngoại trừ *n*) sang str mà không làm mất dữ liệu, rồi gọi ``dfunc(a, b, fromfile, tofile, fromfiledate, tofiledate, n, lineterm)``. Đầu ra của *dfunc* sau đó được chuyển đổi обратно thành bytes, vì vậy các dòng delta bạn nhận được có cùng encoding không xác định hoặc không nhất quán như *a* và *b*.

   .. versionadded:: 3.5


.. _difflib-isjunk-functions:

Các hàm xác định dòng rác
-------------------------

.. function:: IS_LINE_JUNK(line)

   Trả về ``True`` cho các dòng có thể bỏ qua. Dòng *line* có thể bỏ qua nếu *line* trống hoặc chứa một ``'#'`` duy nhất; nếu không thì không thể bỏ qua. Được dùng làm giá trị mặc định cho tham số *linejunk* trong :func:`ndiff` ở các phiên bản cũ hơn.


.. function:: IS_CHARACTER_JUNK(ch)

   Trả về ``True`` cho các ký tự có thể bỏ qua. Ký tự *ch* có thể bỏ qua nếu *ch* là dấu cách hoặc tab; nếu không thì không thể bỏ qua. Được dùng làm giá trị mặc định cho tham số *charjunk* trong :func:`ndiff`.


.. _sequence-matcher:

Các đối tượng SequenceMatcher
-----------------------------

.. class:: SequenceMatcher(isjunk=None, a='', b='', autojunk=True)

   Đối số tùy chọn *isjunk* phải là ``None`` (mặc định) hoặc một hàm nhận một đối số, lấy một phần tử của sequence và trả về true khi và chỉ khi phần tử đó là "rác" và nên được bỏ qua. Truyền ``None`` cho *isjunk* tương đương với việc truyền ``lambda x: False``; nói cách khác, không có phần tử nào bị bỏ qua. Ví dụ, hãy truyền::

      lambda x: x in " \t"

   nếu bạn đang so sánh các dòng dưới dạng sequence gồm các ký tự và không muốn đồng bộ tại các khoảng trống hoặc tab cứng.

   Các đối số tùy chọn *a* và *b* là các sequence cần so sánh; cả hai mặc định là chuỗi rỗng. Các phần tử của cả hai sequence phải là :term:`hashable`.

   Có thể sử dụng đối số tùy chọn *autojunk* để tắt heuristic tự động xác định phần tử rác.

   .. versionchanged:: 3.2
      Đã thêm tham số *autojunk*.

   Các đối tượng SequenceMatcher có ba thuộc tính dữ liệu: *bjunk* là tập hợp các phần tử của *b* mà *isjunk* là ``True``; *bpopular* là tập hợp các phần tử không phải rác được heuristic xem là phổ biến (nếu heuristic này chưa bị tắt); *b2j* là một dict ánh xạ các phần tử còn lại của *b* tới danh sách các vị trí mà chúng xuất hiện. Cả ba thuộc tính đều được đặt lại bất cứ khi nào *b* được đặt lại bằng :meth:`set_seqs` hoặc :meth:`set_seq2`.

   .. versionadded:: 3.2
      Các thuộc tính *bjunk* và *bpopular*.

   Các đối tượng :class:`SequenceMatcher` có các phương thức sau:

   .. method:: set_seqs(a, b)

      Đặt hai chuỗi cần so sánh.

   :class:`SequenceMatcher` tính toán và lưu vào bộ nhớ đệm thông tin chi tiết về chuỗi thứ hai, vì vậy nếu bạn muốn so sánh một chuỗi với nhiều chuỗi, hãy dùng :meth:`set_seq2` để đặt chuỗi được sử dụng chung một lần, rồi gọi :meth:`set_seq1` nhiều lần, mỗi lần cho một chuỗi còn lại.


   .. method:: set_seq1(a)

      Đặt sequence đầu tiên cần so sánh. Sequence thứ hai cần so sánh không bị thay đổi.


   .. method:: set_seq2(b)

      Đặt sequence thứ hai cần so sánh. Sequence đầu tiên cần so sánh không bị thay đổi.


   .. method:: find_longest_match(alo=0, ahi=None, blo=0, bhi=None)

      Tìm block khớp dài nhất trong ``a[alo:ahi]`` và ``b[blo:bhi]``.

      Nếu *isjunk* bị bỏ qua hoặc là ``None``, :meth:`find_longest_match` trả về ``(i, j, k)`` sao cho ``a[i:i+k]`` bằng ``b[j:j+k]``, trong đó ``alo <= i <= i+k <= ahi`` và ``blo <= j <= j+k <= bhi``. Với mọi ``(i', j', k')`` thỏa mãn các điều kiện đó, các điều kiện bổ sung ``k >= k'``, ``i <= i'``, và nếu ``i == i'`` thì ``j <= j'`` cũng được thỏa mãn. Nói cách khác, trong tất cả các block khớp cực đại, trả về block bắt đầu sớm nhất trong *a*, và trong tất cả các block khớp cực đại bắt đầu sớm nhất trong *a*, trả về block bắt đầu sớm nhất trong *b*.

         >>> s = SequenceMatcher(None, " abcd", "abcd abcd")
         >>> s.find_longest_match(0, 5, 0, 9)
         Match(a=0, b=4, size=5)

      Nếu *isjunk* được cung cấp, trước tiên block khớp dài nhất được xác định như trên, nhưng với điều kiện bổ sung là không có phần tử rác nào xuất hiện trong block. Sau đó, block đó được mở rộng tối đa bằng cách chỉ khớp các phần tử rác ở cả hai bên. Vì vậy, block kết quả không bao giờ khớp trên phần tử rác, trừ khi các phần tử rác giống hệt nhau tình cờ nằm liền kề với một phần khớp đáng chú ý.

      Đây là ví dụ tương tự như trước, nhưng coi các khoảng trắng là phần tử rác. Điều đó ngăn ``' abcd'`` khớp trực tiếp với ``' abcd'`` ở cuối sequence thứ hai. Thay vào đó, chỉ ``'abcd'`` có thể khớp và khớp với ``'abcd'`` ở vị trí ngoài cùng bên trái trong sequence thứ hai:

         >>> s = SequenceMatcher(lambda x: x==" ", " abcd", "abcd abcd")
         >>> s.find_longest_match(0, 5, 0, 9)
         Match(a=1, b=0, size=4)

      Nếu không có block nào khớp, phương thức này trả về ``(alo, blo, 0)``.

      Phương thức này trả về một :term:`named tuple` ``Match(a, b, size)``.

      .. versionchanged:: 3.9
         Đã thêm các đối số mặc định.


   .. method:: get_matching_blocks()

      Trả về danh sách các bộ ba mô tả các dãy con khớp nhau không chồng lấn. Mỗi bộ ba có dạng ``(i, j, n)``, và có nghĩa là ``a[i:i+n] == b[j:j+n]``. Các bộ ba tăng dần đơn điệu theo *i* và *j*.

      Bộ ba cuối cùng là bộ giả và có giá trị ``(len(a), len(b), 0)``. Đây là bộ ba duy nhất có ``n == 0``. Nếu ``(i, j, n)`` và ``(i', j', n')`` là các bộ ba liền kề trong danh sách, và bộ thứ hai không phải là bộ cuối cùng trong danh sách, thì ``i+n < i'`` hoặc ``j+n < j'``; nói cách khác, các bộ ba liền kề luôn mô tả các khối bằng nhau không liền kề.

      .. XXX Explain why a dummy is used!

      .. doctest::

         >>> s = SequenceMatcher(None, "abxcd", "abcd")
         >>> s.get_matching_blocks()
         [Match(a=0, b=0, size=2), Match(a=3, b=2, size=2), Match(a=5, b=4, size=0)]


   .. method:: get_opcodes()

      Trả về danh sách các bộ 5 phần tử mô tả cách chuyển *a* thành *b*. Mỗi bộ có dạng ``(tag, i1, i2, j1, j2)``. Bộ đầu tiên có ``i1 == j1 == 0``, còn các bộ còn lại có *i1* bằng *i2* của bộ đứng trước, và tương tự, *j1* bằng *j2* trước đó.

      Các giá trị *tag* là các chuỗi, với những ý nghĩa sau:

      +---------------+--------------------------------------------------------------------------------------------+
      | Giá trị       | Ý nghĩa                                                                                    |
      +===============+============================================================================================+
      | ``'replace'`` | ``a[i1:i2]`` nên được thay thế bằng ``b[j1:j2]``.                                          |
      +---------------+--------------------------------------------------------------------------------------------+
      | ``'delete'``  | ``a[i1:i2]`` nên bị xóa. Lưu ý rằng ``j1 == j2`` trong trường hợp này.                     |
      +---------------+--------------------------------------------------------------------------------------------+
      | ``'insert'``  | ``b[j1:j2]`` nên được chèn tại ``a[i1:i1]``. Lưu ý rằng ``i1 == i2`` trong trường hợp này. |
      +---------------+--------------------------------------------------------------------------------------------+
      | ``'equal'``   | ``a[i1:i2] == b[j1:j2]`` (các chuỗi con bằng nhau).                                        |
      +---------------+--------------------------------------------------------------------------------------------+

      Ví dụ::

        >>> a = "qabxcd"
        >>> b = "abycdf"
        >>> s = SequenceMatcher(None, a, b)
        >>> for tag, i1, i2, j1, j2 in s.get_opcodes():
        ...     print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(
        ...         tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))
        delete    a[0:1] --> b[0:0]      'q' --> ''
        equal     a[1:3] --> b[0:2]     'ab' --> 'ab'
        replace   a[3:4] --> b[2:3]      'x' --> 'y'
        equal     a[4:6] --> b[3:5]     'cd' --> 'cd'
        insert    a[6:6] --> b[5:6]       '' --> 'f'


   .. method:: get_grouped_opcodes(n=3)

      Trả về một :term:`generator` gồm các nhóm có tối đa *n* dòng ngữ cảnh.

      Bắt đầu với các nhóm được :meth:`get_opcodes` trả về, phương thức này tách ra các cụm thay đổi nhỏ hơn và loại bỏ những khoảng xen giữa không có thay đổi.

      Các nhóm được trả về theo cùng định dạng như :meth:`get_opcodes`.


   .. method:: ratio()

      Trả về một giá trị đo độ tương đồng của các chuỗi dưới dạng số thực trong phạm vi [0, 1].

      Trong đó T là tổng số phần tử trong cả hai chuỗi, còn M là số lượng phần tử khớp, giá trị này là 2.0\*M / T. Lưu ý rằng giá trị này là ``1.0`` nếu hai chuỗi giống hệt nhau và là ``0.0`` nếu chúng không có điểm chung.

      Việc tính toán giá trị này tốn kém nếu :meth:`get_matching_blocks` hoặc
      :meth:`get_opcodes` chưa được gọi trước đó; trong trường hợp này, bạn có thể muốn thử :meth:`quick_ratio` hoặc :meth:`real_quick_ratio` trước để lấy một cận trên.


   .. method:: quick_ratio()

      Trả về một cận trên của :meth:`ratio` tương đối nhanh.


   .. method:: real_quick_ratio()

      Trả về một cận trên của :meth:`ratio` rất nhanh.


Ba phương thức trả về tỷ lệ giữa số ký tự khớp và tổng số ký tự có thể cho các kết quả khác nhau do mức độ xấp xỉ khác nhau, mặc dù
:meth:`~SequenceMatcher.quick_ratio` và :meth:`~SequenceMatcher.real_quick_ratio` luôn lớn hơn hoặc bằng :meth:`~SequenceMatcher.ratio`:

   >>> s = SequenceMatcher(None, "abcd", "bcde")
   >>> s.ratio()
   0.75
   >>> s.quick_ratio()
   0.75
   >>> s.real_quick_ratio()
   1.0


Ví dụ
-----

.. _sequencematcher-examples:

Ví dụ về SequenceMatcher
........................

Ví dụ này so sánh hai chuỗi, trong đó coi các khoảng trắng là "junk":

   >>> s = SequenceMatcher(lambda x: x == " ",
   ...                     "private Thread currentThread;",
   ...                     "private volatile Thread currentThread;")

:meth:`~SequenceMatcher.ratio` trả về một số thực trong [0, 1], đo độ tương đồng của các sequence. Theo quy tắc kinh nghiệm, giá trị :meth:`~SequenceMatcher.ratio` lớn hơn 0.6 có nghĩa là các sequence gần như khớp nhau:

   >>> print(round(s.ratio(), 3))
   0.866

Nếu bạn chỉ quan tâm đến vị trí các chuỗi khớp nhau,
:meth:`~SequenceMatcher.get_matching_blocks` rất tiện dụng:

   >>> for block in s.get_matching_blocks():
   ...     print("a[%d] and b[%d] match for %d elements" % block)
   a[0] and b[0] match for 8 elements
   a[8] and b[17] match for 21 elements
   a[29] and b[38] match for 0 elements

Lưu ý rằng tuple cuối cùng do :meth:`~SequenceMatcher.get_matching_blocks` trả về luôn là một tuple giả, ``(len(a), len(b), 0)``, và đây là trường hợp duy nhất mà phần tử cuối cùng của tuple (số phần tử khớp) là ``0``.

Nếu bạn muốn biết cách biến chuỗi thứ nhất thành chuỗi thứ hai, hãy sử dụng
:meth:`~SequenceMatcher.get_opcodes`:

   >>> for opcode in s.get_opcodes():
   ...     print("%6s a[%d:%d] b[%d:%d]" % opcode)
    equal a[0:8] b[0:8]
   insert a[8:8] b[8:17]
    equal a[8:29] b[17:38]

.. seealso::

   * Hàm :func:`get_close_matches` trong module này cho thấy mã đơn giản xây dựng trên :class:`SequenceMatcher` có thể được dùng để thực hiện công việc hữu ích như thế nào.

   * `Công thức kiểm soát phiên bản đơn giản <https://code.activestate.com/recipes/576729-simple-version-control/>`_ cho một ứng dụng nhỏ được xây dựng bằng :class:`SequenceMatcher`.


.. _differ-examples:

Ví dụ về Differ
...............

Ví dụ này so sánh hai văn bản. Trước tiên, chúng ta thiết lập các văn bản, là những chuỗi gồm các chuỗi một dòng riêng lẻ kết thúc bằng ký tự xuống dòng (các chuỗi như vậy cũng có thể lấy được từ phương thức :meth:`~io.IOBase.readlines` của các đối tượng dạng tệp):

   >>> text1 = '''  1. Beautiful is better than ugly.
   ...   2. Explicit is better than implicit.
   ...   3. Simple is better than complex.
   ...   4. Complex is better than complicated.
   ... '''.splitlines(keepends=True)
   >>> len(text1)
   4
   >>> text1[0][-1]
   '\n'
   >>> text2 = '''  1. Beautiful is better than ugly.
   ...   3.   Simple is better than complex.
   ...   4. Complicated is better than complex.
   ...   5. Flat is better than nested.
   ... '''.splitlines(keepends=True)

Tiếp theo, chúng ta khởi tạo một đối tượng Differ:

   >>> d = Differ()

Lưu ý rằng khi khởi tạo một đối tượng :class:`Differ`, chúng ta có thể truyền các hàm để lọc ra các dòng và ký tự “rác”. Xem hàm khởi tạo :meth:`Differ` để biết chi tiết.

Cuối cùng, chúng ta so sánh hai văn bản:

   >>> result = list(d.compare(text1, text2))

``result`` là một danh sách các chuỗi, vì vậy hãy in nó ở dạng dễ đọc:

   >>> from pprint import pprint
   >>> pprint(result)
   ['    1. Beautiful is better than ugly.\n',
    '-   2. Explicit is better than implicit.\n',
    '-   3. Simple is better than complex.\n',
    '+   3.   Simple is better than complex.\n',
    '?     ++\n',
    '-   4. Complex is better than complicated.\n',
    '?            ^                     ---- ^\n',
    '+   4. Complicated is better than complex.\n',
    '?           ++++ ^                      ^\n',
    '+   5. Flat is better than nested.\n']

Dưới dạng một chuỗi nhiều dòng, nó trông như sau:

   >>> import sys
   >>> sys.stdout.writelines(result)
       1. Beautiful is better than ugly.
   -   2. Explicit is better than implicit.
   -   3. Simple is better than complex.
   +   3.   Simple is better than complex.
   ?     ++
   -   4. Complex is better than complicated.
   ?            ^                     ---- ^
   +   4. Complicated is better than complex.
   ?           ++++ ^                      ^
   +   5. Flat is better than nested.


.. _difflib-interface:

Giao diện dòng lệnh cho difflib
...............................

Ví dụ này cho thấy cách sử dụng difflib để tạo một tiện ích tương tự ``diff``.

.. literalinclude:: ../includes/diff.py

Ví dụ về ndiff
..............

Ví dụ này cho thấy cách sử dụng :func:`difflib.ndiff`.

.. literalinclude:: ../includes/ndiff.py

.. _`Pattern Matching: The Gestalt Approach`: https://jacobfilipp.com/DrDobbs/articles/DDJ/1988/8807/8807c/8807c.htm
.. _`Simple version control recipe`: https://code.activestate.com/recipes/576729-simple-version-control/
