:mod:`!textwrap` --- Ngắt dòng và điền văn bản
==============================================

.. module:: textwrap
   :synopsis: Ngắt dòng và điền văn bản

.. moduleauthor:: Greg Ward <gward@python.net>
.. sectionauthor:: Greg Ward <gward@python.net>

**Mã nguồn:** :source:`Lib/textwrap.py`

--------------

Mô-đun :mod:`!textwrap` cung cấp một số hàm tiện ích, cũng như :class:`TextWrapper`, lớp thực hiện toàn bộ công việc. Nếu bạn chỉ ngắt dòng hoặc điền một hoặc hai chuỗi văn bản, các hàm tiện ích là đủ dùng; nếu không, bạn nên sử dụng một thực thể của
:class:`TextWrapper` để tăng hiệu quả.

.. function:: wrap(text, width=70, *, initial_indent="", \
                   subsequent_indent="", expand_tabs=True, \ replace_whitespace=True, fix_sentence_endings=False, \ break_long_words=True, drop_whitespace=True, \ break_on_hyphens=True, tabsize=8, max_lines=None, \ placeholder=' [...]')

   Ngắt dòng cho đoạn văn đơn trong *text* (một chuỗi) để mỗi dòng dài nhiều nhất *width* ký tự. Trả về một danh sách các dòng đầu ra, không có ký tự xuống dòng ở cuối.

   Các đối số từ khóa tùy chọn tương ứng với các thuộc tính của thực thể
   :class:`TextWrapper`, được mô tả bên dưới.

   Xem phương thức :meth:`TextWrapper.wrap` để biết thêm chi tiết về cách
   :func:`wrap` hoạt động.


.. function:: fill(text, width=70, *, initial_indent="", \
                   subsequent_indent="", expand_tabs=True, \ replace_whitespace=True, fix_sentence_endings=False, \ break_long_words=True, drop_whitespace=True, \ break_on_hyphens=True, tabsize=8, \ max_lines=None, placeholder=' [...]'

   Bọc đoạn văn đơn trong *text*, rồi trả về một chuỗi duy nhất chứa đoạn văn đã được bọc. :func:`fill` là cách viết tắt của::

      "\n".join(wrap(text, ...))

   Cụ thể, :func:`fill` chấp nhận chính xác các đối số từ khóa giống như
   :func:`wrap`.


.. function:: shorten(text, width, *, fix_sentence_endings=False, \
                      break_long_words=True, break_on_hyphens=True, \ placeholder=' [...]')

   Thu gọn và cắt ngắn *text* đã cho để vừa với *width* đã cho.

   Trước tiên, khoảng trắng trong *text* được thu gọn (toàn bộ khoảng trắng được thay thế bằng các dấu cách đơn). Nếu kết quả vừa với *width*, kết quả đó được trả về. Nếu không, đủ số từ ở cuối sẽ bị loại bỏ để các từ còn lại cùng với *placeholder* vừa trong *width*::

      >>> textwrap.shorten("Hello  world!", width=12)
      'Hello world!'
      >>> textwrap.shorten("Hello  world!", width=11)
      'Hello [...]'
      >>> textwrap.shorten("Hello world", width=10, placeholder="...")
      'Hello...'

   Các đối số từ khóa tùy chọn tương ứng với các thuộc tính của thực thể
   :class:`TextWrapper`, được ghi lại bên dưới. Lưu ý rằng khoảng trắng được thu gọn trước khi văn bản được truyền cho hàm :class:`TextWrapper` :meth:`fill`, vì vậy việc thay đổi giá trị của :attr:`.tabsize`, :attr:`.expand_tabs`,
   :attr:`.drop_whitespace`, và :attr:`.replace_whitespace` sẽ không có tác dụng.

   .. versionadded:: 3.4

.. function:: dedent(text)

   Xóa mọi khoảng trắng đứng đầu giống nhau khỏi mỗi dòng trong *text*.

   Điều này có thể được dùng để căn các chuỗi đặt trong dấu ngoặc kép ba dòng thẳng với mép trái của phần hiển thị, đồng thời vẫn trình bày chúng dưới dạng thụt lề trong mã nguồn.

   Lưu ý rằng tab và dấu cách đều được xem là khoảng trắng, nhưng chúng không tương đương nhau: các dòng ``"  hello"`` và ``"\thello"`` được xem là không có khoảng trắng đứng đầu chung.

   Các dòng chỉ chứa khoảng trắng sẽ bị bỏ qua trong đầu vào và được chuẩn hóa thành một ký tự xuống dòng trong đầu ra.

   Ví dụ::

      def test():
          # kết thúc dòng đầu tiên bằng \  để tránh dòng trống!
          s = '''\
          hello
            world
          '''
          print(repr(s))          # in ra '    hello\n      world\n    '
          print(repr(dedent(s)))  # in ra 'hello\n  world\n'

   .. versionchanged:: 3.14
      Hàm :func:`!dedent` hiện chuẩn hóa chính xác các dòng trống chỉ chứa ký tự khoảng trắng. Trước đây, phần triển khai chỉ chuẩn hóa các dòng trống chứa tab và dấu cách.

.. function:: indent(text, prefix, predicate=None)

   Thêm *prefix* vào đầu các dòng được chọn trong *text*.

   Các dòng được phân tách bằng cách gọi ``text.splitlines(True)``.

   Theo mặc định, *prefix* được thêm vào tất cả các dòng không chỉ gồm khoảng trắng (bao gồm cả mọi ký tự kết thúc dòng).

   Ví dụ::

      >>> s = 'hello\n\n \nworld'
      >>> indent(s, '  ')
      '  hello\n\n \n  world'

   Có thể sử dụng đối số tùy chọn *predicate* để kiểm soát những dòng được thụt lề. Ví dụ, dễ dàng thêm *prefix* vào cả các dòng trống và các dòng chỉ chứa khoảng trắng::

      >>> print(indent(s, '+ ', lambda line: True))
      + hello
      +
      +
      + world

   .. versionadded:: 3.3


:func:`wrap`, :func:`fill` và :func:`shorten` hoạt động bằng cách tạo ra một
:class:`TextWrapper` instance và gọi một phương thức duy nhất trên đó. Instance đó không được sử dụng lại, vì vậy đối với các ứng dụng xử lý nhiều chuỗi văn bản bằng :func:`wrap` và/hoặc :func:`fill`, việc tự tạo đối tượng :class:`TextWrapper` có thể hiệu quả hơn.

Văn bản được ưu tiên ngắt dòng tại các khoảng trắng và ngay sau dấu gạch nối trong những từ có gạch nối; chỉ khi đó các từ dài mới bị ngắt nếu cần, trừ khi
:attr:`TextWrapper.break_long_words` được đặt thành false.

.. class:: TextWrapper(**kwargs)

   Hàm khởi tạo :class:`TextWrapper` chấp nhận một số đối số từ khóa tùy chọn. Mỗi đối số từ khóa tương ứng với một thuộc tính của instance, vì vậy, chẳng hạn như::

      wrapper = TextWrapper(initial_indent="* ")

   tương đương với::

      wrapper = TextWrapper()
      wrapper.initial_indent = "* "

   Bạn có thể sử dụng lại cùng một đối tượng :class:`TextWrapper` nhiều lần và có thể thay đổi bất kỳ tùy chọn nào của nó bằng cách gán trực tiếp cho các thuộc tính của instance giữa các lần sử dụng.

   Các thuộc tính của instance :class:`TextWrapper` (và các đối số từ khóa của hàm khởi tạo) như sau:


   .. attribute:: width

      (mặc định: ``70``) Độ dài tối đa của các dòng được ngắt. Miễn là không có từ riêng lẻ nào trong văn bản đầu vào dài hơn :attr:`width`, thì
      :class:`TextWrapper` đảm bảo rằng không dòng đầu ra nào dài hơn
      :attr:`width` ký tự.


   .. attribute:: expand_tabs

      (mặc định: ``True``) Nếu là true, thì tất cả ký tự tab trong *text* sẽ được mở rộng thành dấu cách bằng phương thức :meth:`~str.expandtabs` của *text*.


   .. attribute:: tabsize

      (mặc định: ``8``) Nếu :attr:`expand_tabs` là true, thì tất cả ký tự tab trong *text* sẽ được mở rộng thành không hoặc nhiều dấu cách, tùy thuộc vào cột hiện tại và kích thước tab đã cho.

      .. versionadded:: 3.3


   .. attribute:: replace_whitespace

      (mặc định: ``True``) Nếu là true, sau khi mở rộng tab nhưng trước khi ngắt dòng, phương thức :meth:`wrap` sẽ thay thế mỗi ký tự khoảng trắng bằng một dấu cách. Các ký tự khoảng trắng được thay thế gồm: tab, dòng mới, tab dọc, formfeed và carriage return (``'\t\n\v\f\r'``).

      .. note::

         Nếu :attr:`expand_tabs` là false và :attr:`replace_whitespace` là true, mỗi ký tự tab sẽ được thay thế bằng một dấu cách duy nhất; điều này *không* giống với việc mở rộng tab.

      .. note::

         Nếu :attr:`replace_whitespace` là false, ký tự xuống dòng có thể xuất hiện giữa một dòng và gây ra kết quả bất thường. Vì lý do này, văn bản nên được chia thành các đoạn (bằng :meth:`str.splitlines` hoặc cách tương tự), sau đó mỗi đoạn được bọc dòng riêng.


   .. attribute:: drop_whitespace

      (mặc định: ``True``) Nếu là true, khoảng trắng ở đầu và cuối mỗi dòng (sau khi bọc dòng nhưng trước khi thụt lề) sẽ bị loại bỏ. Tuy nhiên, khoảng trắng ở đầu đoạn sẽ không bị loại bỏ nếu sau đó vẫn còn ký tự không phải khoảng trắng. Nếu phần khoảng trắng bị loại bỏ chiếm toàn bộ một dòng, toàn bộ dòng đó sẽ bị loại bỏ.


   .. attribute:: initial_indent

      (mặc định: ``''``) Chuỗi sẽ được thêm vào trước dòng đầu tiên của kết quả đã bọc dòng. Được tính vào độ dài của dòng đầu tiên. Chuỗi rỗng sẽ không được thụt lề.


   .. attribute:: subsequent_indent

      (mặc định: ``''``) Chuỗi sẽ được thêm vào trước mọi dòng của kết quả đã bọc dòng, ngoại trừ dòng đầu tiên. Được tính vào độ dài của mỗi dòng, ngoại trừ dòng đầu tiên.


   .. attribute:: fix_sentence_endings

      (mặc định: ``False``) Nếu là true, :class:`TextWrapper` sẽ cố gắng phát hiện phần kết thúc câu và đảm bảo các câu luôn được phân tách bằng chính xác hai khoảng trắng. Điều này thường được mong muốn đối với văn bản sử dụng phông chữ đơn cách. Tuy nhiên, thuật toán phát hiện câu không hoàn hảo: thuật toán giả định rằng phần kết thúc câu gồm một chữ cái viết thường, theo sau là một trong ``'.'``, ``'!'`` hoặc ``'?'``, có thể tiếp theo là một trong ``'"'`` hoặc ``"'"``, rồi đến một khoảng trắng. Một vấn đề với thuật toán này là nó không thể phân biệt giữa "Dr." trong::

         [...] Dr. Frankenstein's monster [...]

      và "Spot." trong::

         [...] See Spot. See Spot run [...]

      :attr:`fix_sentence_endings` mặc định là false.

      Vì thuật toán phát hiện câu dựa vào ``string.lowercase`` để định nghĩa "chữ cái viết thường" và quy ước dùng hai dấu cách sau dấu chấm để phân tách các câu trên cùng một dòng, thuật toán này chỉ áp dụng cho văn bản tiếng Anh.


   .. attribute:: break_long_words

      (mặc định: ``True``) Nếu là true, các từ dài hơn :attr:`width` sẽ được ngắt để đảm bảo không có dòng nào dài hơn :attr:`width`. Nếu là false, các từ dài sẽ không bị ngắt và một số dòng có thể dài hơn :attr:`width`. (Các từ dài sẽ được đặt trên một dòng riêng để giảm thiểu mức độ vượt quá :attr:`width`.)


   .. attribute:: break_on_hyphens

      (mặc định: ``True``) Nếu là true, việc ngắt dòng sẽ ưu tiên thực hiện tại khoảng trắng và ngay sau dấu gạch nối trong các từ ghép, theo thông lệ tiếng Anh. Nếu là false, chỉ khoảng trắng được xem là các vị trí có thể thích hợp để ngắt dòng, nhưng bạn cần đặt :attr:`break_long_words` thành false nếu muốn các từ thực sự không thể ngắt. Hành vi mặc định trong các phiên bản trước đây là luôn cho phép ngắt các từ có dấu gạch nối.


   .. attribute:: max_lines

      (mặc định: ``None``) Nếu không phải ``None``, đầu ra sẽ chứa nhiều nhất *max_lines* dòng, với *placeholder* xuất hiện ở cuối đầu ra.

      .. versionadded:: 3.4


   .. index:: single: ...; placeholder

   .. attribute:: placeholder

      (mặc định: ``' [...]'``) Chuỗi sẽ xuất hiện ở cuối văn bản đầu ra nếu văn bản đã bị cắt ngắn.

      .. versionadded:: 3.4


   :class:`TextWrapper` cũng cung cấp một số phương thức công khai, tương tự các hàm tiện ích ở cấp module:

   .. method:: wrap(text)

      Bọc đoạn văn duy nhất trong *text* (một chuỗi) để mỗi dòng có nhiều nhất
      dài :attr:`width` ký tự. Tất cả tùy chọn wrapping đều được lấy từ các thuộc tính của instance :class:`TextWrapper`. Trả về danh sách các dòng đầu ra, không có ký tự xuống dòng ở cuối. Nếu đầu ra sau khi wrapping không có nội dung, danh sách được trả về sẽ rỗng.


   .. method:: fill(text)

      Gói đoạn văn duy nhất trong *text*, rồi trả về một chuỗi duy nhất chứa đoạn văn đã được gói.
