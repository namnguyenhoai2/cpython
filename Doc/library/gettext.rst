:mod:`!gettext` --- Dịch vụ quốc tế hóa đa ngôn ngữ
===================================================

.. module:: gettext
   :synopsis: Dịch vụ quốc tế hóa đa ngôn ngữ.

.. moduleauthor:: Barry A. Warsaw <barry@python.org>
.. sectionauthor:: Barry A. Warsaw <barry@python.org>

**Mã nguồn:** :source:`Lib/gettext.py`

--------------

Mô-đun :mod:`!gettext` cung cấp các dịch vụ quốc tế hóa (I18N) và bản địa hóa (L10N) cho các mô-đun và ứng dụng Python của bạn. Mô-đun này hỗ trợ cả API danh mục thông báo GNU :program:`gettext` và API cấp cao hơn dựa trên lớp, có thể phù hợp hơn với các tệp Python. Giao diện được mô tả dưới đây cho phép bạn viết thông báo của mô-đun và ứng dụng bằng một ngôn ngữ tự nhiên, đồng thời cung cấp một danh mục các thông báo đã dịch để chạy với các ngôn ngữ tự nhiên khác nhau.

Ngoài ra, một số gợi ý về việc bản địa hóa các mô-đun và ứng dụng Python của bạn cũng được cung cấp.


API GNU :program:`gettext`
--------------------------

Mô-đun :mod:`!gettext` định nghĩa API sau đây, rất tương tự với API GNU :program:`gettext`. Nếu sử dụng API này, bạn sẽ tác động trên toàn cục đến việc dịch toàn bộ ứng dụng của mình. Thông thường, đây là điều bạn muốn nếu ứng dụng của bạn chỉ sử dụng một ngôn ngữ, trong đó lựa chọn ngôn ngữ phụ thuộc vào locale của người dùng. Nếu bạn đang bản địa hóa một mô-đun Python hoặc nếu ứng dụng của bạn cần chuyển đổi ngôn ngữ trong khi đang chạy, có lẽ bạn nên sử dụng API dựa trên lớp thay thế.


.. function:: bindtextdomain(domain, localedir=None)

   Liên kết *domain* với thư mục locale *localedir*. Cụ thể hơn,
   :mod:`!gettext` sẽ tìm các tệp nhị phân :file:`.mo` cho domain đã cho bằng đường dẫn (trên Unix): :file:`{localedir}/{language}/LC_MESSAGES/{domain}.mo`, trong đó *language* được tìm kiếm trong các biến môi trường :envvar:`LANGUAGE`,
   :envvar:`LC_ALL`, :envvar:`LC_MESSAGES` và :envvar:`LANG` tương ứng.

   Nếu *localedir* bị bỏ qua hoặc là ``None``, thì binding hiện tại cho *domain* được trả về. [#]_


.. function:: textdomain(domain=None)

   Thay đổi hoặc truy vấn domain toàn cục hiện tại. Nếu *domain* là ``None``, thì domain toàn cục hiện tại được trả về; nếu không, domain toàn cục được đặt thành *domain* và giá trị này được trả về.


.. index:: single: _ (underscore); gettext
.. function:: gettext(message, /)

   Trả về bản dịch đã bản địa hóa của *message*, dựa trên domain toàn cục, ngôn ngữ và thư mục locale hiện tại. Hàm này thường được alias thành
   :func:`!_` trong namespace cục bộ (xem các ví dụ bên dưới).


.. function:: dgettext(domain, message, /)

   Giống như :func:`.gettext`, nhưng tra cứu thông báo trong *miền* được chỉ định.


.. function:: ngettext(singular, plural, n, /)

   Giống như :func:`.gettext`, nhưng xét đến các dạng số nhiều. Nếu tìm thấy bản dịch, áp dụng công thức số nhiều cho *n*, rồi trả về thông báo thu được (một số ngôn ngữ có nhiều hơn hai dạng số nhiều). Nếu không tìm thấy bản dịch, trả về *singular* nếu *n* bằng 1; nếu không thì trả về *plural*.

   Công thức số nhiều được lấy từ phần tiêu đề của catalog. Đây là một biểu thức C hoặc Python có biến tự do *n*; biểu thức này đánh giá thành chỉ mục của dạng số nhiều trong catalog. Xem `tài liệu GNU gettext <https://www.gnu.org/software/gettext/manual/gettext.html>`__ để biết cú pháp chính xác cần dùng trong các tệp :file:`.po` và công thức cho nhiều ngôn ngữ khác nhau.


.. function:: dngettext(domain, singular, plural, n, /)

   Giống như :func:`ngettext`, nhưng tra cứu thông báo trong *miền* được chỉ định.


.. function:: pgettext(context, message, /)
.. function:: dpgettext(domain, context, message, /)
.. function:: npgettext(context, singular, plural, n, /)
.. function:: dnpgettext(domain, context, singular, plural, n, /)

   Tương tự các hàm tương ứng không có ``p`` trong tiền tố (tức là :func:`gettext`, :func:`dgettext`, :func:`ngettext`, :func:`dngettext`), nhưng bản dịch bị giới hạn trong *ngữ cảnh* thông báo đã cho.

   .. versionadded:: 3.8


Lưu ý rằng GNU :program:`gettext` cũng định nghĩa một phương thức :func:`!dcgettext`, nhưng phương thức này được xem là không hữu ích nên hiện chưa được triển khai.

Sau đây là một ví dụ về cách sử dụng API điển hình::

   import gettext
   gettext.bindtextdomain('myapplication', '/path/to/my/language/directory')
   gettext.textdomain('myapplication')
   _ = gettext.gettext
   # ...
   print(_('This is a translatable string.'))


API dựa trên class
------------------

API dựa trên class của mô-đun :mod:`!gettext` mang lại cho bạn nhiều tính linh hoạt và tiện lợi hơn API GNU :program:`gettext`. Đây là cách được khuyến nghị để bản địa hóa các ứng dụng và mô-đun Python của bạn. :mod:`!gettext` định nghĩa một class :class:`GNUTranslations` dùng để phân tích các tệp theo định dạng GNU :file:`.mo` và có các phương thức trả về chuỗi. Các instance của class này cũng có thể tự cài đặt vào namespace tích hợp sẵn dưới dạng hàm :func:`!_`.


.. function:: find(domain, localedir=None, languages=None, all=False)

   Hàm này triển khai thuật toán tìm kiếm tệp :file:`.mo` tiêu chuẩn. Hàm nhận một *domain*, giống hệt đối số mà :func:`textdomain` nhận. *localedir* tùy chọn có cách hoạt động như trong :func:`bindtextdomain`. *languages* tùy chọn là một danh sách chuỗi, trong đó mỗi chuỗi là một mã ngôn ngữ.

   Nếu không cung cấp *localedir*, thư mục locale hệ thống mặc định sẽ được sử dụng. [#]_ Nếu không cung cấp *languages*, các biến môi trường sau sẽ được tìm kiếm: :envvar:`LANGUAGE`, :envvar:`LC_ALL`, :envvar:`LC_MESSAGES`, và
   :envvar:`LANG`. Giá trị đầu tiên không rỗng sẽ được sử dụng cho biến *languages*. Các biến môi trường phải chứa một danh sách ngôn ngữ được phân tách bằng dấu hai chấm; danh sách này sẽ được tách tại dấu hai chấm để tạo ra danh sách chuỗi mã ngôn ngữ mong đợi.

   Sau đó, :func:`find` mở rộng và chuẩn hóa các ngôn ngữ, rồi lặp qua chúng để tìm kiếm một tệp hiện có được tạo từ các thành phần sau:

   :file:`{localedir}/{language}/LC_MESSAGES/{domain}.mo`

   Tên tệp đầu tiên trong số đó tồn tại sẽ được :func:`find` trả về. Nếu không tìm thấy tệp nào như vậy, ``None`` sẽ được trả về. Nếu cung cấp *all*, hàm sẽ trả về danh sách tất cả tên tệp theo thứ tự chúng xuất hiện trong danh sách ngôn ngữ hoặc các biến môi trường.


.. function:: translation(domain, localedir=None, languages=None, class_=None, fallback=False)

   Trả về một thực thể ``*Translations`` dựa trên *domain*, *localedir* và *languages*, trước tiên được truyền vào :func:`find` để lấy danh sách các đường dẫn tệp :file:`.mo` tương ứng. Các thực thể có tên tệp :file:`.mo` giống hệt nhau sẽ được lưu vào bộ nhớ đệm. Lớp thực sự được khởi tạo là *class_* nếu được cung cấp; nếu không thì là :class:`GNUTranslations`. Hàm khởi tạo của lớp phải nhận một đối số :term:`file object` duy nhất.

   Nếu tìm thấy nhiều tệp, các tệp đứng sau sẽ được dùng làm phương án dự phòng cho các tệp đứng trước. Để cho phép thiết lập phương án dự phòng, :func:`copy.copy` được dùng để sao chép từng đối tượng bản dịch từ bộ nhớ đệm; dữ liệu thực tế của thực thể vẫn được dùng chung với bộ nhớ đệm.

   Nếu không tìm thấy tệp :file:`.mo`, hàm này sẽ phát sinh :exc:`OSError` nếu *fallback* là false (đây là giá trị mặc định), và trả về một
   thực thể :class:`NullTranslations` nếu *fallback* là true.

   .. versionchanged:: 3.3
      :exc:`IOError` used to be raised, it is now an alias of :exc:`OSError`.

   .. versionchanged:: 3.11
      Tham số *codeset* bị loại bỏ.

.. function:: install(domain, localedir=None, *, names=None)

   Thao tác này cài đặt hàm :func:`!_` vào namespace builtins của Python, dựa trên *domain* và *localedir*, là các giá trị được truyền vào hàm :func:`translation`.

   Đối với tham số *names*, hãy xem phần mô tả về phương thức :meth:`~NullTranslations.install` của đối tượng bản dịch.

   Như minh họa dưới đây, bạn thường đánh dấu các chuỗi trong ứng dụng của mình là những chuỗi cần dịch bằng cách bọc chúng trong một lệnh gọi đến hàm :func:`!_`, như sau::

      print(_('This string will be translated.'))

   Để thuận tiện, bạn muốn cài đặt hàm :func:`!_` vào namespace builtins của Python, để hàm này dễ dàng được truy cập trong tất cả các mô-đun của ứng dụng.

   .. versionchanged:: 3.11
      *names* hiện là một tham số chỉ nhận đối số theo từ khóa.

Lớp :class:`NullTranslations`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các lớp translation là những lớp thực sự triển khai việc dịch các chuỗi thông báo trong tệp nguồn gốc sang các chuỗi thông báo đã được dịch. Lớp cơ sở được tất cả các lớp translation sử dụng là :class:`NullTranslations`; lớp này cung cấp giao diện cơ bản mà bạn có thể dùng để viết các lớp translation chuyên biệt của riêng mình. Sau đây là các phương thức của :class:`!NullTranslations`:


.. class:: NullTranslations(fp=None)

   Nhận một :term:`file object` *fp* tùy chọn, nhưng lớp cơ sở sẽ bỏ qua đối số này. Khởi tạo các biến instance "được bảo vệ" *_info* và *_charset*, được các lớp dẫn xuất thiết lập, cũng như *_fallback*, được thiết lập thông qua
   :meth:`add_fallback`. Sau đó, nó gọi ``self._parse(fp)`` nếu *fp* không phải là ``None``.

   .. method:: _parse(fp)

      Không thực hiện thao tác nào trong lớp cơ sở, phương thức này nhận đối tượng tệp *fp* và đọc dữ liệu từ tệp, khởi tạo message catalog của nó. Nếu bạn có định dạng tệp message catalog không được hỗ trợ, hãy ghi đè phương thức này để phân tích định dạng của bạn.


   .. method:: add_fallback(fallback)

      Thêm *fallback* làm đối tượng dự phòng cho translation object hiện tại. Translation object nên tham vấn fallback nếu không thể cung cấp bản dịch cho một thông báo cụ thể.


   .. method:: gettext(message, /)

      Nếu đã thiết lập fallback, chuyển tiếp :meth:`!gettext` cho fallback. Nếu không, trả về *message*. Được ghi đè trong các lớp dẫn xuất.


   .. method:: ngettext(singular, plural, n, /)

      Nếu đã thiết lập fallback, chuyển tiếp :meth:`!ngettext` cho fallback. Nếu không, trả về *singular* nếu *n* bằng 1; nếu không thì trả về *plural*. Được ghi đè trong các lớp dẫn xuất.


   .. method:: pgettext(context, message, /)

      Nếu đã thiết lập fallback, chuyển tiếp :meth:`pgettext` cho fallback. Nếu không, trả về thông báo đã dịch. Được ghi đè trong các lớp dẫn xuất.

      .. versionadded:: 3.8


   .. method:: npgettext(context, singular, plural, n, /)

      Nếu đã thiết lập fallback, chuyển tiếp :meth:`npgettext` cho fallback. Nếu không, trả về thông báo đã dịch. Được ghi đè trong các lớp dẫn xuất.

      .. versionadded:: 3.8


   .. method:: info()

      Trả về một dictionary chứa metadata được tìm thấy trong tệp message catalog.


   .. method:: charset()

      Trả về encoding của tệp message catalog.


   .. method:: install(names=None)

      Phương thức này cài đặt :meth:`.gettext` vào namespace built-in, liên kết nó với ``_``.

      Nếu tham số *names* được cung cấp, tham số đó phải là một sequence chứa tên các hàm bạn muốn cài đặt vào namespace builtins, ngoài :func:`!_`. Các tên được hỗ trợ là ``'gettext'``, ``'ngettext'``, ``'pgettext'`` và ``'npgettext'``.

      Lưu ý rằng đây chỉ là một cách, dù là cách thuận tiện nhất, để cung cấp hàm :func:`!_` cho ứng dụng của bạn. Vì nó ảnh hưởng đến toàn bộ ứng dụng trên phạm vi toàn cục, cụ thể là namespace built-in, các module được bản địa hóa không bao giờ được cài đặt :func:`!_`. Thay vào đó, chúng nên sử dụng đoạn mã này để cung cấp :func:`!_` cho module của mình::

         import gettext
         t = gettext.translation('mymodule', ...)
         _ = t.gettext

      Cách này chỉ đặt :func:`!_` trong namespace toàn cục của module, nên chỉ ảnh hưởng đến các lệnh gọi bên trong module này.

      .. versionchanged:: 3.8
         Đã thêm ``'pgettext'`` và ``'npgettext'``.


Lớp :class:`GNUTranslations`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mô-đun :mod:`!gettext` cung cấp thêm một lớp được dẫn xuất từ
:class:`NullTranslations`: :class:`GNUTranslations`. Lớp này ghi đè
:meth:`!_parse` để cho phép đọc các tệp :file:`.mo` ở định dạng GNU :program:`gettext` theo cả định dạng big-endian và little-endian.

:class:`GNUTranslations` phân tích siêu dữ liệu tùy chọn từ translation catalog. Theo quy ước của GNU :program:`gettext`, siêu dữ liệu được đưa vào dưới dạng bản dịch cho chuỗi rỗng. Siêu dữ liệu này gồm các cặp :rfc:`822`\ -style ``key: value`` và phải chứa khóa ``Project-Id-Version``. Nếu tìm thấy khóa ``Content-Type``, thuộc tính ``charset`` sẽ được dùng để khởi tạo biến thể hiện :attr:`!_charset` "protected", mặc định là ``None`` nếu không tìm thấy. Nếu chỉ định encoding của bộ ký tự, thì tất cả message ID và chuỗi message đọc từ catalog sẽ được chuyển đổi sang Unicode bằng encoding này; nếu không, ASCII sẽ được giả định.

Vì message ID cũng được đọc dưới dạng chuỗi Unicode, tất cả các phương thức ``*gettext()`` sẽ coi message ID là chuỗi Unicode, không phải chuỗi byte.

Toàn bộ tập hợp các cặp khóa/giá trị được đặt vào một dictionary và gán làm biến thể hiện :attr:`!_info` "protected".

Nếu số magic của tệp :file:`.mo` không hợp lệ, số phiên bản chính không đúng như mong đợi hoặc xảy ra các vấn đề khác trong khi đọc tệp, việc khởi tạo một
Lớp :class:`GNUTranslations` có thể phát sinh :exc:`OSError`.

.. class:: GNUTranslations

   Các phương thức sau được ghi đè từ phần triển khai của lớp cơ sở:

   .. method:: gettext(message, /)

      Tra cứu mã định danh *message* trong catalog và trả về chuỗi thông báo tương ứng dưới dạng chuỗi Unicode. Nếu catalog không có mục nhập cho mã định danh *message* và một fallback đã được thiết lập, việc tra cứu sẽ được chuyển tiếp đến phương thức :meth:`~NullTranslations.gettext` của fallback. Nếu không, mã định danh *message* sẽ được trả về.


   .. method:: ngettext(singular, plural, n, /)

      Thực hiện tra cứu các dạng số nhiều của một mã định danh thông báo. *singular* được dùng làm mã định danh thông báo để tra cứu trong catalog, còn *n* được dùng để xác định dạng số nhiều cần sử dụng. Chuỗi thông báo được trả về là một chuỗi Unicode.

      Nếu không tìm thấy mã định danh thông báo trong catalog và một fallback được chỉ định, yêu cầu sẽ được chuyển tiếp đến phương thức :meth:`~NullTranslations.ngettext` của fallback. Nếu không, khi *n* bằng 1, *singular* sẽ được trả về; trong mọi trường hợp khác, *plural* sẽ được trả về.

      Sau đây là một ví dụ::

         n = len(os.listdir('.'))
         cat = GNUTranslations(somefile)
         message = cat.ngettext(
             'There is %(num)d file in this directory',
             'There are %(num)d files in this directory',
             n) % {'num': n}


   .. method:: pgettext(context, message, /)

      Tra cứu *context* và mã định danh *message* trong catalog, rồi trả về chuỗi thông báo tương ứng dưới dạng chuỗi Unicode. Nếu catalog không có mục nhập cho mã định danh *message* và *context*, đồng thời một fallback đã được thiết lập, việc tra cứu sẽ được chuyển tiếp đến
      phương thức :meth:`pgettext`. Nếu không, id *message* sẽ được trả về.

      .. versionadded:: 3.8


   .. method:: npgettext(context, singular, plural, n, /)

      Tra cứu các dạng số nhiều của message id. *singular* được sử dụng làm message id để tra cứu trong catalog, còn *n* được sử dụng để xác định dạng số nhiều cần dùng.

      Nếu không tìm thấy message id cho *context* trong catalog và có chỉ định fallback, yêu cầu sẽ được chuyển tiếp đến
      phương thức :meth:`npgettext`. Nếu không, khi *n* là 1 thì *singular* được trả về, còn *plural* được trả về trong mọi trường hợp khác.

      .. versionadded:: 3.8


Hỗ trợ catalog thông báo của Solaris
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hệ điều hành Solaris định nghĩa định dạng tệp nhị phân :file:`.mo` riêng, nhưng vì không tìm thấy tài liệu nào về định dạng này nên hiện tại định dạng này chưa được hỗ trợ.


Hàm khởi tạo Catalog
^^^^^^^^^^^^^^^^^^^^

.. index:: single: GNOME

GNOME sử dụng một phiên bản của module :mod:`!gettext` do James Henstridge viết, nhưng phiên bản này có API hơi khác. Cách sử dụng được ghi chép của nó là::

   import gettext
   cat = gettext.Catalog(domain, localedir)
   _ = cat.gettext
   print(_('hello world'))

Để tương thích với module cũ hơn này, hàm :func:`!Catalog` là bí danh của hàm :func:`translation` được mô tả ở trên.

Một điểm khác biệt giữa module này và module của Henstridge là: các đối tượng catalog của ông hỗ trợ truy cập thông qua mapping API, nhưng tính năng này dường như không được sử dụng nên hiện chưa được hỗ trợ.

.. _i18n-howto:

Quốc tế hóa các chương trình và module của bạn
----------------------------------------------

Quốc tế hóa (I18N) là quy trình giúp một chương trình nhận biết nhiều ngôn ngữ. Bản địa hóa (L10N) là việc điều chỉnh chương trình của bạn, sau khi đã được quốc tế hóa, cho phù hợp với ngôn ngữ và tập quán văn hóa địa phương. Để cung cấp các thông báo đa ngôn ngữ cho chương trình Python, bạn cần thực hiện các bước sau:

#. chuẩn bị chương trình hoặc module của bạn bằng cách đánh dấu riêng các chuỗi có thể dịch

#. chạy một bộ công cụ trên các tệp đã đánh dấu để tạo các catalog thông báo thô

#. tạo các bản dịch dành riêng cho từng ngôn ngữ của các message catalog

#. sử dụng module :mod:`!gettext` để các chuỗi thông báo được dịch chính xác

Để chuẩn bị code cho I18N, bạn cần xem xét tất cả các chuỗi trong các tệp của mình. Mọi chuỗi cần được dịch phải được đánh dấu bằng cách bọc nó trong ``_('...')`` --- tức là một lệnh gọi đến hàm :func:`_ <gettext>`. Ví dụ::

   filename = 'mylog.txt'
   message = _('writing a log message')
   with open(filename, 'w') as fp:
       fp.write(message)

Trong ví dụ này, chuỗi ``'writing a log message'`` được đánh dấu là ứng viên để dịch, còn các chuỗi ``'mylog.txt'`` và ``'w'`` thì không.

Có một số công cụ để trích xuất các chuỗi cần dịch. GNU :program:`gettext` ban đầu chỉ hỗ trợ mã nguồn C hoặc C++, nhưng phiên bản mở rộng :program:`xgettext` quét code được viết bằng nhiều ngôn ngữ, bao gồm Python, để tìm các chuỗi được đánh dấu là có thể dịch. `Babel <https://babel.pocoo.org/>`__ là một thư viện quốc tế hóa Python, bao gồm một script :file:`pybabel` để trích xuất và biên dịch các message catalog. Chương trình có tên :program:`xpot` của François Pinard thực hiện công việc tương tự và có sẵn trong gói `po-utils package <https://github.com/pinard/po-utils>`__ của ông.

(Python cũng bao gồm các phiên bản thuần Python của những chương trình này, có tên là
:program:`pygettext.py` và :program:`msgfmt.py`; một số bản phân phối Python sẽ cài đặt chúng cho bạn. :program:`pygettext.py` tương tự như
:program:`xgettext`, nhưng chỉ hiểu mã nguồn Python và không thể xử lý các ngôn ngữ lập trình khác như C hoặc C++.
:program:`pygettext.py` hỗ trợ giao diện dòng lệnh tương tự như
:program:`xgettext`; để biết chi tiết về cách sử dụng, hãy chạy ``pygettext.py --help``.  :program:`msgfmt.py` tương thích nhị phân với GNU
:program:`msgfmt`.  Với hai chương trình này, bạn có thể không cần gói GNU
:program:`gettext` để quốc tế hóa các ứng dụng Python của mình.)

:program:`xgettext`, :program:`pygettext`, và các công cụ tương tự tạo ra
:file:`.po` là các danh mục thông báo.  Đây là những tệp có cấu trúc, con người có thể đọc được, chứa mọi chuỗi được đánh dấu trong mã nguồn, cùng với một chỗ dành sẵn cho các phiên bản đã dịch của những chuỗi này.

Sau đó, các bản sao của những tệp :file:`.po` này được chuyển cho từng biên dịch viên là con người, những người viết bản dịch cho mọi ngôn ngữ tự nhiên được hỗ trợ. Họ gửi lại các phiên bản dành riêng cho từng ngôn ngữ dưới dạng tệp :file:`<language-name>.po`, tệp này được biên dịch thành tệp danh mục nhị phân :file:`.mo` mà máy có thể đọc bằng chương trình :program:`msgfmt`. Các tệp :file:`.mo` được sử dụng bởi
mô-đun :mod:`!gettext` để thực hiện việc dịch thực tế trong thời gian chạy.

Cách bạn sử dụng mô-đun :mod:`!gettext` trong mã của mình phụ thuộc vào việc bạn đang quốc tế hóa một mô-đun riêng lẻ hay toàn bộ ứng dụng. Hai phần tiếp theo sẽ lần lượt thảo luận về từng trường hợp.


Bản địa hóa mô-đun của bạn
^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu đang bản địa hóa mô-đun của mình, bạn phải cẩn thận để không thực hiện các thay đổi trên phạm vi toàn cục, chẳng hạn như đối với namespace tích hợp sẵn. Bạn không nên sử dụng GNU :program:`gettext` API mà thay vào đó hãy sử dụng API dựa trên lớp.

Giả sử mô-đun của bạn có tên là "spam" và các tệp :file:`.mo` bản dịch ngôn ngữ tự nhiên khác nhau của mô-đun nằm trong :file:`/usr/share/locale` ở định dạng GNU
:program:`gettext`. Đây là nội dung bạn sẽ đặt ở đầu mô-đun của mình::

   import gettext
   t = gettext.translation('spam', '/usr/share/locale')
   _ = t.gettext


Bản địa hóa ứng dụng của bạn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu bạn đang bản địa hóa ứng dụng của mình, bạn có thể cài đặt hàm :func:`!_` trên toàn cục vào không gian tên tích hợp sẵn, thường là trong tệp driver chính của ứng dụng. Điều này cho phép tất cả các tệp dành riêng cho ứng dụng của bạn chỉ cần sử dụng ``_('...')`` mà không phải cài đặt rõ ràng hàm này trong từng tệp.

Trong trường hợp đơn giản, bạn chỉ cần thêm đoạn mã sau vào tệp driver chính của ứng dụng::

   import gettext
   gettext.install('myapplication')

Nếu cần thiết lập thư mục locale, bạn có thể truyền thư mục đó vào
hàm :func:`install`::

   import gettext
   gettext.install('myapplication', '/usr/share/locale')


Thay đổi ngôn ngữ nhanh chóng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu chương trình của bạn cần hỗ trợ nhiều ngôn ngữ cùng lúc, bạn có thể muốn tạo nhiều phiên bản dịch, sau đó chuyển đổi rõ ràng giữa chúng như sau::

   import gettext

   lang1 = gettext.translation('myapplication', languages=['en'])
   lang2 = gettext.translation('myapplication', languages=['fr'])
   lang3 = gettext.translation('myapplication', languages=['de'])

   # bắt đầu bằng cách sử dụng language1
   lang1.install()

   # ... thời gian trôi qua, người dùng chọn language 2
   lang2.install()

   # ... thêm thời gian trôi qua, người dùng chọn language 3
   lang3.install()


Bản dịch trì hoãn
^^^^^^^^^^^^^^^^^

Trong hầu hết các tình huống lập trình, chuỗi được dịch ngay tại nơi chúng được viết. Tuy nhiên, đôi khi bạn cần đánh dấu các chuỗi để dịch, nhưng trì hoãn việc dịch thực tế đến sau. Một ví dụ kinh điển là::

   animals = ['mollusk',
              'albatross',
              'rat',
              'penguin',
              'python', ]
   # ...
   for a in animals:
       print(a)

Ở đây, bạn muốn đánh dấu các chuỗi trong danh sách ``animals`` là có thể dịch được, nhưng không thực sự muốn dịch chúng cho đến khi chúng được in ra.

Sau đây là một cách bạn có thể xử lý tình huống này::

   def _(message): return message

   animals = [_('mollusk'),
              _('albatross'),
              _('rat'),
              _('penguin'),
              _('python'), ]

   del _

   # ...
   for a in animals:
       print(_(a))

Điều này hoạt động vì định nghĩa giả của :func:`!_` chỉ đơn giản trả về chuỗi không thay đổi. Và định nghĩa giả này sẽ tạm thời ghi đè mọi định nghĩa của :func:`!_` trong namespace tích hợp sẵn (cho đến khi thực hiện lệnh :keyword:`del`). Tuy nhiên, hãy cẩn thận nếu bạn đã có định nghĩa trước đó của :func:`!_` trong namespace cục bộ.

Lưu ý rằng lần sử dụng thứ hai của :func:`!_` sẽ không xác định "a" là có thể dịch được sang chương trình :program:`gettext`, vì tham số này không phải là một string literal.

Một cách khác để xử lý việc này là sử dụng ví dụ sau::

   def N_(message): return message

   animals = [N_('mollusk'),
              N_('albatross'),
              N_('rat'),
              N_('penguin'),
              N_('python'), ]

   # ...
   for a in animals:
       print(_(a))

Trong trường hợp này, bạn đánh dấu các chuỗi có thể dịch bằng hàm
:func:`!N_`, hàm này sẽ không xung đột với bất kỳ định nghĩa nào của :func:`!_`. Tuy nhiên, bạn sẽ cần hướng dẫn chương trình trích xuất thông điệp tìm các chuỗi có thể dịch được đánh dấu bằng :func:`!N_`. :program:`xgettext`,
:program:`pygettext`, ``pybabel extract``, và :program:`xpot` đều hỗ trợ việc này thông qua tùy chọn dòng lệnh :option:`!-k`. Việc chọn :func:`!N_` ở đây hoàn toàn tùy ý; cũng có thể dễ dàng chọn :func:`!MarkThisStringForTranslation`.


Lời cảm ơn
----------

Những người sau đây đã đóng góp mã, phản hồi, đề xuất về thiết kế, các bản triển khai trước đây và kinh nghiệm quý báu vào quá trình tạo ra module này:

* Peter Funk

* James Henstridge

* Juan David Ibáñez Palomar

* Marc-André Lemburg

* Martin von Löwis

* François Pinard

* Barry Warsaw

* Gustavo Niemeyer

.. rubric:: Chú thích cuối trang

.. [#] Thư mục locale mặc định phụ thuộc vào hệ thống; ví dụ: trên Red Hat Linux, thư mục này là :file:`/usr/share/locale`, nhưng trên Solaris, nó là :file:`/usr/lib/locale`. Module :mod:`!gettext` không cố gắng hỗ trợ các giá trị mặc định phụ thuộc vào hệ thống này; thay vào đó, giá trị mặc định của module là :file:`{sys.base_prefix}/share/locale` (xem
   :data:`sys.base_prefix`). Vì lý do này, tốt nhất bạn luôn gọi
   :func:`bindtextdomain` với một đường dẫn tuyệt đối tường minh ngay khi bắt đầu ứng dụng.

.. [#] Xem chú thích cuối trang về :func:`bindtextdomain` ở trên.
