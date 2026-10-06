
.. _introduction:

**********
Giới thiệu
**********

Tài liệu tham khảo này mô tả ngôn ngữ lập trình Python. Tài liệu không nhằm mục đích hướng dẫn.

Mặc dù cố gắng diễn đạt chính xác nhất có thể, tôi đã chọn sử dụng tiếng Anh thay vì các đặc tả hình thức cho mọi phần, ngoại trừ cú pháp và phân tích từ vựng. Điều này giúp tài liệu dễ hiểu hơn đối với độc giả thông thường, nhưng sẽ để lại chỗ cho những điểm mơ hồ. Vì vậy, nếu bạn đến từ Sao Hỏa và cố gắng triển khai lại Python chỉ dựa trên tài liệu này, bạn có thể phải phỏng đoán một số điều và trên thực tế, có lẽ bạn sẽ kết thúc bằng việc triển khai một ngôn ngữ khá khác biệt. Mặt khác, nếu bạn đang sử dụng Python và muốn biết các quy tắc chính xác về một lĩnh vực cụ thể của ngôn ngữ, chắc chắn bạn sẽ có thể tìm thấy chúng ở đây. Nếu muốn xem một định nghĩa hình thức hơn về ngôn ngữ, có lẽ bạn có thể tình nguyện dành thời gian của mình --- hoặc phát minh một cỗ máy nhân bản :-).

Việc thêm quá nhiều chi tiết triển khai vào tài liệu tham khảo ngôn ngữ là rất nguy hiểm --- phần triển khai có thể thay đổi, và các bản triển khai khác của cùng một ngôn ngữ có thể hoạt động khác nhau. Mặt khác, CPython là bản triển khai Python được sử dụng rộng rãi nhất (mặc dù các bản triển khai thay thế vẫn tiếp tục nhận được sự hỗ trợ), và những đặc điểm riêng của nó đôi khi đáng được đề cập, đặc biệt khi phần triển khai áp đặt thêm các giới hạn. Vì vậy, bạn sẽ thấy những "ghi chú triển khai" ngắn được rải rác trong toàn bộ văn bản.

Mỗi bản triển khai Python đều đi kèm với một số module tích hợp sẵn và module chuẩn. Các module này được ghi chép trong :ref:`library-index`. Một vài module tích hợp sẵn được đề cập khi chúng tương tác đáng kể với định nghĩa ngôn ngữ.


.. _implementations:

Các bản triển khai thay thế
===========================

Mặc dù có một bản triển khai Python phổ biến hơn hẳn, vẫn có một số bản triển khai thay thế đặc biệt đáng chú ý đối với các nhóm đối tượng khác nhau.

Các bản triển khai được biết đến gồm:

CPython
   Đây là bản triển khai Python nguyên gốc và được duy trì tích cực nhất, được viết bằng C. Các tính năng ngôn ngữ mới thường xuất hiện đầu tiên ở đây.

Jython
   Python được triển khai bằng Java. Bản triển khai này có thể được sử dụng như một ngôn ngữ scripting cho các ứng dụng Java hoặc để tạo ứng dụng bằng cách sử dụng các thư viện lớp Java. Bản này cũng thường được dùng để tạo các bài kiểm thử cho thư viện Java. Có thể tìm thêm thông tin tại `trang web Jython <https://www.jython.org/>`_.

Python for .NET
   Bản triển khai này thực sự sử dụng bản triển khai CPython, nhưng là một ứng dụng .NET được quản lý và cung cấp các thư viện .NET. Bản này được tạo bởi Brian Lloyd. Để biết thêm thông tin, hãy xem `trang chủ Python for .NET <https://pythonnet.github.io/>`_.

IronPython
   Một Python thay thế cho .NET. Khác với Python.NET, đây là một triển khai Python hoàn chỉnh tạo ra IL và biên dịch trực tiếp mã Python thành các assembly .NET. Nó được tạo ra bởi Jim Hugunin, người sáng tạo ban đầu của Jython. Để biết thêm thông tin, hãy xem `trang web IronPython <https://ironpython.net/>`_.

PyPy
   Một triển khai Python được viết hoàn toàn bằng Python. Nó hỗ trợ một số tính năng nâng cao không có trong các triển khai khác, chẳng hạn như hỗ trợ stackless và trình biên dịch Just in Time. Một trong những mục tiêu của dự án là khuyến khích việc thử nghiệm với chính ngôn ngữ này bằng cách giúp sửa đổi trình thông dịch dễ dàng hơn (vì trình thông dịch được viết bằng Python). Thông tin bổ sung có trên `trang chủ của dự án PyPy <https://pypy.org/>`_.

Mỗi triển khai này đều khác với ngôn ngữ được mô tả trong tài liệu này theo một cách nào đó, hoặc cung cấp những thông tin cụ thể ngoài phạm vi tài liệu Python chuẩn. Vui lòng tham khảo tài liệu dành riêng cho từng triển khai để xác định những điều khác bạn cần biết về triển khai cụ thể đang sử dụng.


.. _notation:

Ký hiệu
=======

.. index:: BNF, grammar, syntax, notation

Các mô tả về phân tích từ vựng và cú pháp sử dụng một ký pháp ngữ pháp là sự kết hợp giữa `EBNF <https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form>`_ và `PEG <https://en.wikipedia.org/wiki/Parsing_expression_grammar>`_. Ví dụ:

.. grammar-snippet::
   :group: notation

   name:   `letter` (`letter` | `digit` | "_")*
   letter: "a"..."z" | "A"..."Z"
   digit:  "0"..."9"

Trong ví dụ này, dòng đầu tiên cho biết rằng một ``name`` là một ``letter`` theo sau bởi một chuỗi gồm không hoặc nhiều ``letter``\ s, ``digit``\ s và dấu gạch dưới. Đến lượt mình, một ``letter`` là bất kỳ ký tự đơn nào từ ``'a'`` đến ``'z'`` và từ ``A`` đến ``Z``; một ``digit`` là một ký tự đơn trong khoảng từ ``0`` đến ``9``.

Mỗi quy tắc bắt đầu bằng một tên (xác định quy tắc đang được định nghĩa), theo sau là dấu hai chấm, ``:``. Phần định nghĩa ở bên phải dấu hai chấm sử dụng các phần tử cú pháp sau:

* ``name``: Một tên tham chiếu đến một quy tắc khác. Khi có thể, tên đó là một liên kết đến định nghĩa của quy tắc.

  * ``TOKEN``: Một tên viết hoa tham chiếu đến một :term:`token`. Đối với các định nghĩa ngữ pháp, token cũng giống như quy tắc.

* ``"text"``, ``'text'``: Văn bản nằm trong dấu ngoặc đơn hoặc dấu ngoặc kép phải khớp chính xác (không bao gồm dấu ngoặc). Loại dấu ngoặc được chọn tùy theo ý nghĩa của ``text``:

  * ``'if'``: Một tên nằm trong dấu ngoặc đơn biểu thị một :ref:`keyword <keywords>`.
  * ``"case"``: Một tên nằm trong dấu ngoặc kép biểu thị một
    :ref:`từ khóa mềm <soft-keywords>`.
  * ``'@'``: Một ký hiệu không phải chữ cái được đặt trong dấu nháy đơn biểu thị một
    :py:data:`~token.OP` token, tức là một :ref:`dấu phân cách <delimiters>` hoặc
    :ref:`toán tử <operators>`.

* ``e1 e2``: Các mục chỉ được phân tách bằng khoảng trắng biểu thị một chuỗi. Ở đây, ``e1`` phải được theo sau bởi ``e2``.
* ``e1 | e2``: Dấu gạch đứng được dùng để phân tách các lựa chọn. Nó biểu thị "lựa chọn theo thứ tự" của PEG: nếu ``e1`` khớp, ``e2`` sẽ không được xét. Trong các văn phạm PEG truyền thống, ký hiệu này được viết là dấu gạch chéo, ``/``, thay vì dấu gạch đứng. Xem :pep:`617` để biết thêm bối cảnh và chi tiết.
* ``e*``: Dấu sao biểu thị không hoặc nhiều lần lặp của mục đứng trước.
* ``e+``: Tương tự, dấu cộng có nghĩa là một hoặc nhiều lần lặp.
* ``[e]``: Một cụm từ được đặt trong dấu ngoặc vuông có nghĩa là xuất hiện không hoặc một lần. Nói cách khác, cụm từ được đặt trong đó là tùy chọn.
* ``e?``: Dấu chấm hỏi có ý nghĩa hoàn toàn giống với dấu ngoặc vuông: phần tử đứng trước là tùy chọn.
* ``(e)``: Dấu ngoặc tròn được dùng để nhóm.

Ký hiệu sau đây chỉ được sử dụng trong
:ref:`các định nghĩa từ vựng <notation-lexical-vs-syntactic>`.

* ``"a"..."z"``: Hai ký tự literal được phân tách bằng ba dấu chấm có nghĩa là chọn bất kỳ một ký tự nào trong phạm vi ký tự ASCII đã cho (bao gồm cả hai đầu mút).
* ``<...>``: Một cụm từ nằm giữa các dấu ngoặc nhọn cung cấp mô tả không chính thức về ký hiệu được so khớp (ví dụ: ``<any ASCII character except "\">``), hoặc một chữ viết tắt được định nghĩa trong phần văn bản lân cận (ví dụ: ``<Lu>``).

.. _lexical-lookaheads:

Một số định nghĩa cũng sử dụng *lookaheads*, cho biết rằng một phần tử phải (hoặc không được) so khớp tại một vị trí nhất định, nhưng không tiêu thụ bất kỳ đầu vào nào:

* ``&e``: lookahead dương (nghĩa là, ``e`` bắt buộc phải so khớp)
* ``!e``: lookahead âm (nghĩa là, ``e`` bắt buộc *not* phải so khớp)

Các toán tử một ngôi (``*``, ``+``, ``?``) liên kết chặt nhất có thể; dấu gạch đứng (``|``) liên kết lỏng nhất.

Khoảng trắng chỉ có ý nghĩa khi dùng để phân tách các token.

Các quy tắc thường được viết trên một dòng, nhưng những quy tắc quá dài có thể được xuống dòng:

.. grammar-snippet::
   :group: notation

   literal: stringliteral | bytesliteral
            | integer | floatnumber | imagnumber

Ngoài ra, các quy tắc có thể được định dạng sao cho dòng đầu tiên kết thúc bằng dấu hai chấm, và mỗi lựa chọn bắt đầu bằng một dấu gạch đứng trên một dòng mới. Ví dụ:


.. grammar-snippet::
   :group: notation-alt

   literal:
      | stringliteral
      | bytesliteral
      | integer
      | floatnumber
      | imagnumber

Điều này *không* có nghĩa là có một lựa chọn đầu tiên rỗng.

.. index:: lexical definitions

.. _notation-lexical-vs-syntactic:

Định nghĩa từ vựng và cú pháp
-----------------------------

Có một số khác biệt giữa việc phân tích *từ vựng* và *cú pháp*: :term:`lexical analyzer` hoạt động trên từng ký tự riêng lẻ của mã nguồn đầu vào, trong khi *bộ phân tích cú pháp* (syntactic analyzer) hoạt động trên luồng :term:`token <token>` được tạo ra từ quá trình phân tích từ vựng. Tuy nhiên, trong một số trường hợp, ranh giới chính xác giữa hai giai đoạn là một chi tiết triển khai của CPython.

Điểm khác biệt thực tế giữa hai loại này là trong các định nghĩa *từ vựng*, mọi khoảng trắng đều có ý nghĩa. Bộ phân tích từ vựng :ref:`loại bỏ <whitespace>` mọi khoảng trắng không được chuyển thành các token như :data:`token.INDENT` hoặc :data:`~token.NEWLINE`. Sau đó, các định nghĩa *cú pháp* sử dụng những token này thay vì các ký tự mã nguồn.

Tài liệu này sử dụng cùng một ngữ pháp BNF cho cả hai kiểu định nghĩa. Mọi trường hợp sử dụng BNF trong chương tiếp theo (:ref:`lexical`) đều là các định nghĩa từ vựng; các trường hợp sử dụng trong những chương tiếp theo là các định nghĩa cú pháp.

.. _`the Jython website`: https://www.jython.org/
.. _`Python for .NET home page`: https://pythonnet.github.io/
.. _`the IronPython website`: https://ironpython.net/
.. _`the PyPy project's home page`: https://pypy.org/
.. _`EBNF`: https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form
.. _`PEG`: https://en.wikipedia.org/wiki/Parsing_expression_grammar
