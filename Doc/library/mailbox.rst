:mod:`!mailbox` --- Thao tác với mailbox ở nhiều định dạng khác nhau
====================================================================

.. module:: mailbox
   :synopsis: Thao tác với mailbox ở nhiều định dạng khác nhau

.. moduleauthor:: Gregory K. Johnson <gkj@gregorykjohnson.com>
.. sectionauthor:: Gregory K. Johnson <gkj@gregorykjohnson.com>

**Mã nguồn:** :source:`Lib/mailbox.py`

--------------

Mô-đun này định nghĩa hai lớp, :class:`Mailbox` và :class:`Message`, để truy cập và thao tác với các mailbox trên đĩa cùng những message chứa trong đó.
:class:`!Mailbox` cung cấp ánh xạ giống dictionary từ các key đến các message.
:class:`!Message` mở rộng mô-đun :mod:`email.message`
lớp :class:`~email.message.Message` bằng trạng thái và hành vi dành riêng cho từng định dạng. Các định dạng mailbox được hỗ trợ gồm Maildir, mbox, MH, Babyl và MMDF.


.. seealso::

   Mô-đun :mod:`email`
      Biểu diễn và thao tác với các thư.


.. _mailbox-objects:

Các đối tượng :class:`!Mailbox`
-------------------------------

.. class:: Mailbox

   Một mailbox có thể được kiểm tra và sửa đổi.

   Lớp :class:`!Mailbox` định nghĩa một interface và không предназначена để được khởi tạo. Thay vào đó, các lớp con dành riêng cho từng định dạng nên kế thừa từ
   :class:`!Mailbox` và code của bạn nên khởi tạo một lớp con cụ thể.

   Interface :class:`!Mailbox` có dạng giống dictionary, với các key nhỏ tương ứng với các message. Các key được instance :class:`!Mailbox` cấp và chỉ có ý nghĩa đối với instance :class:`!Mailbox` đó. Một key tiếp tục xác định một message ngay cả khi message tương ứng được sửa đổi, chẳng hạn như bằng cách thay thế message đó bằng một message khác.

   Có thể thêm thư vào một instance :class:`!Mailbox` bằng phương thức giống set :meth:`add` và xóa thư bằng câu lệnh ``del`` hoặc các phương thức giống set :meth:`remove` và :meth:`discard`.

   Ngữ nghĩa của interface :class:`!Mailbox` khác với ngữ nghĩa của dictionary theo một số cách đáng chú ý. Mỗi khi một thư được yêu cầu, một biểu diễn mới (thường là một instance :class:`Message`) sẽ được tạo dựa trên trạng thái hiện tại của mailbox. Tương tự, khi một thư được thêm vào
   instance :class:`!Mailbox`, nội dung của biểu diễn thư được cung cấp sẽ được sao chép. Trong cả hai trường hợp, instance :class:`!Mailbox` không giữ tham chiếu đến biểu diễn thư.

   :class:`!Mailbox` :term:`iterator` mặc định lặp qua các biểu diễn thư, không phải các khóa như iterator :class:`dictionary <dict>` mặc định. Ngoài ra, việc sửa đổi mailbox trong khi lặp là an toàn và có hành vi được xác định rõ. Các thư được thêm vào mailbox sau khi iterator được tạo sẽ không được iterator nhìn thấy. Các thư bị xóa khỏi mailbox trước khi iterator trả về chúng sẽ bị bỏ qua một cách im lặng, mặc dù việc sử dụng một khóa từ iterator có thể dẫn đến
   ngoại lệ :exc:`KeyError` nếu thư tương ứng sau đó bị xóa.

   .. warning::

      Hãy hết sức thận trọng khi sửa đổi các mailbox có thể đồng thời bị một tiến trình khác thay đổi. Định dạng mailbox an toàn nhất để sử dụng cho những tác vụ như vậy là :class:`Maildir`; hãy cố tránh sử dụng các định dạng một tệp như
      :class:`mbox` cho việc ghi đồng thời. Nếu bạn đang sửa đổi một mailbox, bạn *phải* khóa nó bằng cách gọi các phương thức :meth:`lock` và :meth:`unlock` *trước khi* đọc bất kỳ thư nào trong tệp hoặc thực hiện thay đổi bằng cách thêm hoặc xóa thư. Không khóa mailbox có nguy cơ làm mất thư hoặc làm hỏng toàn bộ mailbox.

   Các instance :class:`!Mailbox` có những phương thức sau:


   .. method:: add(message)

      Thêm *message* vào mailbox và trả về khóa đã được gán cho nó.

      Tham số *message* có thể là một instance :class:`Message`, một
      instance :class:`email.message.Message`, một chuỗi, một chuỗi byte hoặc một đối tượng giống tệp (đối tượng này phải được mở ở chế độ nhị phân). Nếu *message* là một instance của lớp con :class:`Message` dành riêng cho định dạng tương ứng (ví dụ: nếu đó là một
      instance :class:`mboxMessage` và đây là một instance :class:`mbox`), thông tin dành riêng cho định dạng của nó sẽ được sử dụng. Nếu không, các giá trị mặc định hợp lý cho thông tin dành riêng cho định dạng sẽ được sử dụng.

      .. versionchanged:: 3.2
         Đã bổ sung hỗ trợ cho đầu vào nhị phân.


   .. method:: remove(key)
               __delitem__(key) discard(key)

      Xóa thư tương ứng với *key* khỏi hộp thư.

      Nếu không tồn tại thư như vậy, một ngoại lệ :exc:`KeyError` sẽ được phát sinh nếu phương thức được gọi dưới dạng :meth:`remove` hoặc :meth:`__delitem__`, nhưng sẽ không phát sinh ngoại lệ nếu phương thức được gọi dưới dạng :meth:`discard`. Hành vi của :meth:`discard` có thể được ưu tiên nếu định dạng hộp thư bên dưới hỗ trợ việc sửa đổi đồng thời bởi các tiến trình khác.


   .. method:: __setitem__(key, message)

      Thay thế thư tương ứng với *key* bằng *message*. Phát sinh một
      :exc:`KeyError` ngoại lệ nếu chưa có thư nào tương ứng với *key*.

      Tương tự như :meth:`add`, tham số *message* có thể là một :class:`Message` instance, một :class:`email.message.Message` instance, một chuỗi, một chuỗi byte hoặc một đối tượng dạng tệp (đối tượng này phải được mở ở chế độ nhị phân). Nếu *message* là một instance của lớp con :class:`Message` dành riêng cho định dạng tương ứng (ví dụ: nếu đó là một :class:`mboxMessage` instance và đây là một
      :class:`mbox` instance), thông tin dành riêng cho định dạng đó sẽ được sử dụng. Nếu không, thông tin dành riêng cho định dạng của thư hiện đang tương ứng với *key* sẽ được giữ nguyên.


   .. method:: iterkeys()

      Trả về một :term:`iterator` trên tất cả các key


   .. method:: keys()

      Giống như :meth:`iterkeys`, ngoại trừ việc một :class:`list` được trả về thay vì một :term:`iterator`


   .. method:: itervalues()
               __iter__()

      Trả về một :term:`iterator` chứa các biểu diễn của tất cả thư. Các thư được biểu diễn dưới dạng các thực thể thuộc lớp con :class:`Message` dành riêng cho định dạng tương ứng, trừ khi một message factory tùy chỉnh được chỉ định khi khởi tạo thực thể :class:`!Mailbox`.

      .. note::

         Cách hoạt động của :meth:`__iter__` khác với dictionary, vốn lặp qua các khóa.


   .. method:: values()

      Giống như :meth:`itervalues`, ngoại trừ việc một :class:`list` được trả về thay vì một :term:`iterator`


   .. method:: iteritems()

      Trả về một :term:`iterator` chứa các cặp (*key*, *message*), trong đó *key* là một khóa và *message* là một biểu diễn thư. Các thư được biểu diễn dưới dạng các thực thể thuộc lớp con dành riêng cho định dạng tương ứng
      :class:`Message`, trừ khi một message factory tùy chỉnh được chỉ định khi khởi tạo thực thể :class:`!Mailbox`.


   .. method:: items()

      Giống như :meth:`iteritems`, ngoại trừ việc trả về một :class:`list` các cặp thay vì một :term:`iterator` các cặp.


   .. method:: get(key, default=None)
               __getitem__(key)

      Trả về biểu diễn của thư tương ứng với *key*. Nếu không tồn tại thư như vậy, *default* sẽ được trả về nếu phương thức được gọi như sau
      :meth:`get` và một ngoại lệ :exc:`KeyError` sẽ được phát sinh nếu phương thức được gọi như :meth:`!__getitem__`. Thư được biểu diễn dưới dạng một instance của lớp con :class:`Message` dành riêng cho định dạng tương ứng, trừ khi một message factory tùy chỉnh được chỉ định khi khởi tạo instance :class:`!Mailbox`.


   .. method:: get_message(key)

      Trả về biểu diễn của thư tương ứng với *key* dưới dạng một instance của lớp con :class:`Message` dành riêng cho định dạng tương ứng, hoặc phát sinh ngoại lệ :exc:`KeyError` nếu không tồn tại thư như vậy.


   .. method:: get_bytes(key)

      Trả về biểu diễn dạng byte của thư tương ứng với *key*, hoặc phát sinh ngoại lệ :exc:`KeyError` nếu không tồn tại thư như vậy.

      .. versionadded:: 3.2


   .. method:: get_string(key)

      Trả về biểu diễn dạng chuỗi của thư tương ứng với *key*, hoặc phát sinh ngoại lệ :exc:`KeyError` nếu không tồn tại thư như vậy. Thư được xử lý thông qua :class:`email.message.Message` để chuyển đổi thành biểu diễn 7bit sạch.


   .. method:: get_file(key)

      Trả về một biểu diễn :term:`file-like <file-like object>` của thông điệp tương ứng với *key*, hoặc phát sinh một :exc:`KeyError` ngoại lệ nếu không tồn tại thông điệp đó. Đối tượng dạng tệp này hoạt động như thể được mở ở chế độ nhị phân. Cần đóng tệp này khi không còn cần đến nó nữa.

      .. versionchanged:: 3.2
         Đối tượng tệp thực sự là một :term:`binary file`; trước đây nó đã bị trả về không đúng ở chế độ văn bản. Ngoài ra, :term:`file-like object` hiện hỗ trợ giao thức :term:`context manager`: bạn có thể sử dụng một
         :keyword:`with` câu lệnh để tự động đóng nó.

      .. note::

         Không giống các cách biểu diễn thông điệp khác,
         Các biểu diễn :term:`file-like <file-like object>` không nhất thiết độc lập với thực thể :class:`!Mailbox` đã tạo ra chúng hoặc với mailbox bên dưới. Mỗi lớp con đều có tài liệu cụ thể hơn.


   .. method:: __contains__(key)

      Trả về ``True`` nếu *key* tương ứng với một thông điệp, và ``False`` nếu không.


   .. method:: __len__()

      Trả về số lượng thông điệp trong mailbox.


   .. method:: clear()

      Xóa tất cả thư khỏi hộp thư.


   .. method:: pop(key, default=None)

      Trả về biểu diễn của thư tương ứng với *key* và xóa thư đó. Nếu không tồn tại thư như vậy, trả về *default*. Thư được biểu diễn dưới dạng một instance của định dạng cụ thể phù hợp
      :class:`Message`, trừ khi một message factory tùy chỉnh được chỉ định khi khởi tạo thực thể :class:`!Mailbox`.


   .. method:: popitem()

      Trả về một cặp (*key*, *message*) bất kỳ, trong đó *key* là một key và *message* là biểu diễn của một thư, đồng thời xóa thư tương ứng. Nếu hộp thư trống, raise một :exc:`KeyError` exception. Thư được biểu diễn dưới dạng một instance của định dạng cụ thể phù hợp
      :class:`Message`, trừ khi một message factory tùy chỉnh được chỉ định khi khởi tạo thực thể :class:`!Mailbox`.


   .. method:: update(arg)

      Tham số *arg* phải là một ánh xạ từ *key* tới *message* hoặc một iterable gồm các cặp (*key*, *message*). Cập nhật hộp thư sao cho, với mỗi *key* và *message* đã cho, thư tương ứng với *key* được đặt thành *message* như thể sử dụng :meth:`__setitem__`. Tương tự :meth:`__setitem__`, mỗi *key* phải tương ứng với một thư đã có trong hộp thư; nếu không thì một
      :exc:`KeyError` exception sẽ được raise, vì vậy nhìn chung *arg* không nên là một instance của :class:`!Mailbox`.

      .. note::

         Không giống như với dictionary, keyword arguments không được hỗ trợ.


   .. method:: flush()

      Ghi mọi thay đổi đang chờ vào filesystem. Đối với một số lớp con của :class:`Mailbox`, các thay đổi luôn được ghi ngay lập tức và :meth:`!flush` không thực hiện thao tác nào, nhưng bạn vẫn nên tạo thói quen gọi phương thức này.


   .. method:: lock()

      Có được exclusive advisory lock trên mailbox để các tiến trình khác biết không được sửa đổi nó. Một :exc:`ExternalClashError` sẽ được phát sinh nếu không thể lấy lock. Cơ chế locking cụ thể được sử dụng phụ thuộc vào định dạng mailbox. Bạn *luôn luôn* nên lock mailbox trước khi thực hiện bất kỳ sửa đổi nào đối với nội dung của nó.


   .. method:: unlock()

      Giải phóng lock trên mailbox, nếu có.


   .. method:: close()

      Flush mailbox, mở khóa nếu cần và đóng mọi tệp đang mở. Đối với một số lớp con của :class:`!Mailbox`, phương thức này không thực hiện thao tác nào.


.. _mailbox-maildir:

Các đối tượng :class:`!Maildir`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: Maildir(dirname, factory=None, create=True)

   Một lớp con của :class:`Mailbox` dành cho các mailbox ở định dạng Maildir. Tham số *factory* là một đối tượng callable chấp nhận một biểu diễn message dạng tệp (hoạt động như thể được mở ở chế độ binary) và trả về một biểu diễn tùy chỉnh. Nếu *factory* là ``None``, :class:`MaildirMessage` được dùng làm biểu diễn message mặc định. Nếu *create* là ``True``, mailbox sẽ được tạo nếu chưa tồn tại.

   Nếu *create* là ``True`` và đường dẫn *dirname* tồn tại, đường dẫn này sẽ được coi là maildir hiện có mà không cần thử xác minh bố cục thư mục.

   *dirname* được đặt tên như vậy vì lý do lịch sử, thay vì *path*.

   Maildir là định dạng hộp thư dựa trên thư mục, được phát minh cho mail transfer agent qmail và hiện được nhiều chương trình khác hỗ trợ rộng rãi. Các thư trong hộp thư Maildir được lưu trong những tệp riêng biệt bên trong một cấu trúc thư mục chung. Thiết kế này cho phép nhiều chương trình không liên quan truy cập và sửa đổi các hộp thư Maildir mà không làm hỏng dữ liệu, vì vậy không cần khóa tệp.

   Hộp thư Maildir chứa ba thư mục con, cụ thể là: :file:`tmp`,
   :file:`new`, và :file:`cur`. Thư được tạo tạm thời trong thư mục con
   :file:`tmp`, sau đó được chuyển đến thư mục con :file:`new` để hoàn tất việc chuyển thư. Sau đó, mail user agent có thể chuyển thư đến thư mục con
   :file:`cur` và lưu thông tin về trạng thái của thư trong một phần "info" đặc biệt được nối vào tên tệp của thư.

   Các thư mục theo kiểu do tác nhân truyền thư Courier giới thiệu cũng được hỗ trợ. Mọi thư mục con của hộp thư chính đều được xem là một thư mục nếu ``'.'`` là ký tự đầu tiên trong tên của nó. Tên thư mục được biểu diễn bằng
   :class:`!Maildir` mà không có ``'.'`` ở đầu. Mỗi thư mục tự nó là một hộp thư Maildir nhưng không được chứa các thư mục khác. Thay vào đó, cấu trúc lồng nhau logic được biểu thị bằng ``'.'`` để phân tách các cấp, ví dụ: "Archived.2005.07".

   .. attribute:: Maildir.colon

      Đặc tả Maildir yêu cầu sử dụng dấu hai chấm (``':'``) trong một số tên tệp thư nhất định. Tuy nhiên, một số hệ điều hành không cho phép ký tự này trong tên tệp. Nếu muốn sử dụng định dạng giống Maildir trên một hệ điều hành như vậy, bạn nên chỉ định một ký tự khác để thay thế. Dấu chấm than (``'!'``) là một lựa chọn phổ biến. Ví dụ::

         import mailbox
         mailbox.Maildir.colon = '!'

      Thuộc tính :attr:`!colon` cũng có thể được thiết lập cho từng instance.

   .. versionchanged:: 3.13
      :class:`Maildir` now ignores files with a leading dot.

   Các instance :class:`!Maildir` có tất cả các phương thức của :class:`Mailbox` cùng với những phương thức sau:


   .. method:: list_folders()

      Trả về danh sách tên của tất cả các thư mục.


   .. method:: get_folder(folder)

      Trả về một instance :class:`!Maildir` đại diện cho thư mục có tên là *folder*. Một ngoại lệ :exc:`NoSuchMailboxError` sẽ được phát sinh nếu thư mục không tồn tại.


   .. method:: add_folder(folder)

      Tạo một thư mục có tên là *folder* và trả về một instance :class:`!Maildir` đại diện cho thư mục đó.


   .. method:: remove_folder(folder)

      Xóa thư mục có tên là *folder*. Nếu thư mục chứa bất kỳ thư nào, một ngoại lệ :exc:`NotEmptyError` sẽ được nêu ra và thư mục sẽ không bị xóa.


   .. method:: clean()

      Xóa các tệp tạm thời khỏi mailbox chưa được truy cập trong 36 giờ qua. Đặc tả Maildir quy định rằng các chương trình đọc thư nên thỉnh thoảng thực hiện việc này.


   .. method:: get_flags(key)

      Trả về dưới dạng chuỗi các cờ được thiết lập trên thư tương ứng với *key*. Kết quả này giống với ``get_message(key).get_flags()`` nhưng nhanh hơn nhiều vì không mở tệp thư. Sử dụng phương thức này khi lặp qua các key để xác định những thư cần lấy.

      Nếu bạn có một đối tượng :class:`MaildirMessage`, hãy sử dụng phương thức :meth:`~MaildirMessage.get_flags` của đối tượng đó thay thế, vì những thay đổi do :meth:`~MaildirMessage.set_flags` của thư thực hiện,
      Các phương thức :meth:`~MaildirMessage.add_flag` và :meth:`~MaildirMessage.remove_flag` không được phản ánh ở đây cho đến khi phương thức
      :meth:`__setitem__` của mailbox được gọi.

      .. versionadded:: 3.13


   .. method:: set_flags(key, flags)

      Đối với thư tương ứng với *key*, đặt các cờ được chỉ định bởi *flags* và bỏ đặt tất cả các cờ khác. Việc gọi ``some_mailbox.set_flags(key, flags)`` tương tự như::

         one_message = some_mailbox.get_message(key)
         one_message.set_flags(flags)
         some_mailbox[key] = one_message

      nhưng nhanh hơn vì không mở tệp thư.

      Nếu bạn có một đối tượng :class:`MaildirMessage`, hãy sử dụng phương thức :meth:`~MaildirMessage.set_flags` của đối tượng đó thay thế, vì các thay đổi được thực hiện bằng phương thức mailbox này sẽ không hiển thị trong phương thức của đối tượng thư, :meth:`~MaildirMessage.get_flags`.

      .. versionadded:: 3.13


   .. method:: add_flag(key, flag)

      Đối với thư tương ứng với *key*, đặt các cờ được chỉ định bởi *flag* mà không thay đổi các cờ khác. Để thêm nhiều cờ cùng lúc, *flag* có thể là một chuỗi gồm nhiều ký tự.

      Các điểm cần cân nhắc khi sử dụng phương thức này thay vì phương thức của đối tượng thư
      :meth:`~MaildirMessage.add_flag` tương tự như các điểm cần cân nhắc đối với :meth:`set_flags`; xem phần thảo luận ở đó.

      .. versionadded:: 3.13


   .. method:: remove_flag(key, flag)

      Đối với thư tương ứng với *key*, bỏ đặt các cờ được chỉ định bởi *flag* mà không thay đổi các cờ khác. Để xóa nhiều cờ cùng lúc, *flag* có thể là một chuỗi gồm nhiều ký tự.

      Các điểm cần cân nhắc khi sử dụng phương thức này thay vì phương thức của đối tượng thư
      Các phương thức :meth:`~MaildirMessage.remove_flag` tương tự như các phương thức dành cho :meth:`set_flags`; xem phần thảo luận ở đó.

      .. versionadded:: 3.13


   .. method:: get_info(key)

      Trả về một chuỗi chứa thông tin của thư tương ứng với *key*. Phương thức này tương tự như ``get_message(key).get_info()`` nhưng nhanh hơn nhiều vì không mở tệp thư. Hãy sử dụng phương thức này khi lặp qua các khóa để xác định những thư cần lấy thông tin.

      Nếu bạn có một đối tượng :class:`MaildirMessage`, hãy sử dụng phương thức :meth:`~MaildirMessage.get_info` của đối tượng đó, vì các thay đổi do phương thức :meth:`~MaildirMessage.set_info` của thư thực hiện sẽ không được phản ánh ở đây cho đến khi phương thức :meth:`__setitem__` của mailbox được gọi.

      .. versionadded:: 3.13


   .. method:: set_info(key, info)

      Đặt thông tin của thư tương ứng với *key* thành *info*. Việc gọi ``some_mailbox.set_info(key, flags)`` tương tự như::

         one_message = some_mailbox.get_message(key)
         one_message.set_info(info)
         some_mailbox[key] = one_message

      nhưng nhanh hơn vì không mở tệp thư.

      Nếu bạn có một đối tượng :class:`MaildirMessage`, hãy sử dụng phương thức :meth:`~MaildirMessage.set_info` của đối tượng đó, vì các thay đổi được thực hiện bằng phương thức của mailbox này sẽ không hiển thị trong phương thức của đối tượng thư, :meth:`~MaildirMessage.get_info`.

      .. versionadded:: 3.13

   Một số phương thức :class:`Mailbox` được triển khai bởi :class:`!Maildir` cần được lưu ý đặc biệt:


   .. method:: add(message)
               __setitem__(key, message) update(arg)

      .. warning::

         Các phương thức này tạo tên tệp duy nhất dựa trên process hiện tại
         ID. Khi sử dụng nhiều thread, có thể xảy ra xung đột tên không được phát hiện và
         gây hỏng mailbox trừ khi các thread được phối hợp để tránh sử dụng các phương thức này nhằm thao tác đồng thời trên cùng một mailbox.


   .. method:: flush()

      Mọi thay đổi đối với mailbox Maildir đều được áp dụng ngay lập tức, vì vậy phương thức này không thực hiện thao tác nào.


   .. method:: lock()
               unlock()

      Các mailbox Maildir không hỗ trợ (hoặc không yêu cầu) việc khóa, vì vậy các phương thức này không làm gì cả.


   .. method:: close()

      Các đối tượng :class:`!Maildir` không giữ bất kỳ tệp nào đang mở và các mailbox bên dưới không hỗ trợ khóa, vì vậy phương thức này không làm gì cả.


   .. method:: get_file(key)

      Tùy thuộc vào nền tảng máy chủ, bạn có thể không sửa đổi hoặc xóa được thông báo bên dưới trong khi tệp được trả về vẫn đang mở.


.. seealso::

   `Trang hướng dẫn sử dụng maildir của Courier <https://www.courier-mta.org/maildir.html>`_
      Đặc tả về định dạng này. Mô tả một phần mở rộng phổ biến để hỗ trợ các thư mục.

   `Sử dụng định dạng maildir <https://cr.yp.to/proto/maildir.html>`_
      Các ghi chú về Maildir của người phát minh ra nó. Bao gồm lược đồ tạo tên được cập nhật và thông tin chi tiết về ngữ nghĩa của "info".


.. _mailbox-mbox:

các đối tượng :class:`!mbox`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: mbox(path, factory=None, create=True)

   Một lớp con của :class:`Mailbox` dành cho các mailbox ở định dạng mbox. Tham số *factory* là một đối tượng có thể gọi, chấp nhận biểu diễn thư bằng tệp (hoạt động như thể được mở ở chế độ nhị phân) và trả về một biểu diễn tùy chỉnh. Nếu *factory* là ``None``, :class:`mboxMessage` được dùng làm biểu diễn thư mặc định. Nếu *create* là ``True``, mailbox sẽ được tạo nếu chưa tồn tại.

   Định dạng mbox là định dạng kinh điển để lưu trữ thư trên các hệ thống Unix. Tất cả thư trong một mailbox mbox được lưu trong một tệp duy nhất; phần bắt đầu của mỗi thư được đánh dấu bằng một dòng có năm ký tự đầu tiên là "From ".

   Có một số biến thể của định dạng mbox nhằm khắc phục những hạn chế được cho là tồn tại trong định dạng ban đầu. Để đảm bảo khả năng tương thích, :class:`!mbox` triển khai định dạng ban đầu, đôi khi được gọi là :dfn:`mboxo`. Điều này có nghĩa là header :mailheader:`Content-Length`, nếu có, sẽ bị bỏ qua và mọi chuỗi "From " xuất hiện ở đầu dòng trong phần thân thư sẽ được chuyển thành ">From " khi lưu thư, mặc dù các chuỗi ">From " sẽ không được chuyển thành "From " khi đọc thư.

   Một số phương thức :class:`Mailbox` được :class:`!mbox` triển khai cần được lưu ý riêng:


   .. method:: get_bytes(key, from_=False)

      Lưu ý: Phương thức này có thêm một tham số (*from_*) so với các lớp khác. Dòng đầu tiên của một mục trong tệp mbox là dòng Unix "From ". Nếu *from_* là False, dòng đầu tiên của tệp sẽ bị loại bỏ.

   .. method:: get_file(key, from_=False)

      Sử dụng tệp sau khi gọi :meth:`~Mailbox.flush` hoặc
      Việc :meth:`~Mailbox.close` trên instance :class:`!mbox` có thể cho kết quả không dự đoán được hoặc gây ra ngoại lệ.

      Lưu ý: Phương thức này có thêm một tham số (*from_*) so với các lớp khác. Dòng đầu tiên của một mục trong tệp mbox là dòng Unix "From ". Nếu *from_* là False, dòng đầu tiên của tệp sẽ bị loại bỏ.

   .. method:: get_string(key, from_=False)

      Lưu ý: Phương thức này có thêm một tham số (*from_*) so với các lớp khác. Dòng đầu tiên của một mục trong tệp mbox là dòng Unix "From ". Nếu *from_* là False, dòng đầu tiên của tệp sẽ bị loại bỏ.

   .. method:: lock()
               unlock()

      Có ba cơ chế khóa được sử dụng---khóa bằng tệp dot và, nếu có,
      các lệnh gọi hệ thống :c:func:`!flock` và :c:func:`!lockf`.


.. seealso::

   `Trang hướng dẫn mbox từ tin <http://www.tin.org/bin/man.cgi?section=5&topic=mbox>`_
      Đặc tả về định dạng, kèm chi tiết về việc khóa.

   `Định cấu hình Netscape Mail trên Unix: Vì sao định dạng Content-Length không tốt <https://www.jwz.org/doc/content-length.html>`_
      Lập luận ủng hộ việc sử dụng định dạng mbox nguyên bản thay vì một biến thể.

   `"mbox" là một họ gồm nhiều định dạng hộp thư không tương thích với nhau <https://www.loc.gov/preservation/digital/formats/fdd/fdd000383.shtml>`_
      Lịch sử của các biến thể mbox.


.. _mailbox-mh:

:class:`!MH` đối tượng
^^^^^^^^^^^^^^^^^^^^^^


.. class:: MH(path, factory=None, create=True)

   Một lớp con của :class:`Mailbox` dành cho các hộp thư ở định dạng MH. Tham số *factory* là một đối tượng có thể gọi, chấp nhận biểu diễn thư dạng tệp (hoạt động như thể được mở ở chế độ nhị phân) và trả về một biểu diễn tùy chỉnh. Nếu *factory* là ``None``, :class:`MHMessage` được dùng làm biểu diễn thư mặc định. Nếu *create* là ``True``, hộp thư sẽ được tạo nếu chưa tồn tại.

   MH là một định dạng mailbox dựa trên thư mục, được phát minh cho MH Message Handling System, một mail user agent. Mỗi thư trong mailbox MH nằm trong một tệp riêng. Một mailbox MH có thể chứa các mailbox MH khác (được gọi là :dfn:`folder`) bên cạnh các thư. Các folder có thể được lồng nhau vô hạn. Mailbox MH cũng hỗ trợ :dfn:`sequence`, là các danh sách có tên được dùng để nhóm các thư theo logic mà không di chuyển chúng vào các thư mục con. Các sequence được định nghĩa trong một tệp có tên :file:`.mh_sequences` trong mỗi folder.

   Lớp :class:`!MH` thao tác với các mailbox MH, nhưng không cố gắng mô phỏng tất cả hành vi của :program:`mh`. Cụ thể, lớp này không sửa đổi và cũng không bị ảnh hưởng bởi các tệp :file:`context` hoặc :file:`.mh_profile` được :program:`mh` sử dụng để lưu trạng thái và cấu hình của nó.

   Các đối tượng :class:`!MH` có tất cả các phương thức của :class:`Mailbox`, ngoài ra còn có những phương thức sau:

   .. versionchanged:: 3.13

      Các folder được hỗ trợ không chứa tệp :file:`.mh_sequences`.


   .. method:: list_folders()

      Trả về danh sách tên của tất cả các folder.


   .. method:: get_folder(folder)

      Trả về một thực thể :class:`!MH` đại diện cho folder có tên là *folder*. Một ngoại lệ :exc:`NoSuchMailboxError` được phát sinh nếu folder không tồn tại.


   .. method:: add_folder(folder)

      Tạo một folder có tên là *folder* và trả về một thực thể :class:`!MH` đại diện cho folder đó.


   .. method:: remove_folder(folder)

      Xóa thư mục có tên là *folder*. Nếu thư mục chứa bất kỳ thư nào, một ngoại lệ :exc:`NotEmptyError` sẽ được phát sinh và thư mục sẽ không bị xóa.


   .. method:: get_sequences()

      Trả về một dictionary ánh xạ tên các sequence tới danh sách key. Nếu không có sequence nào, một dictionary rỗng sẽ được trả về.


   .. method:: set_sequences(sequences)

      Định nghĩa lại các sequence tồn tại trong mailbox dựa trên *sequences*, một dictionary ánh xạ tên tới danh sách key, giống như được trả về bởi
      :meth:`get_sequences`.


   .. method:: pack()

      Đổi tên các thư trong mailbox nếu cần để loại bỏ các khoảng trống trong việc đánh số. Các mục trong danh sách sequence cũng được cập nhật tương ứng.

      .. note::

         Các key đã được cấp sẽ bị vô hiệu hóa bởi thao tác này và không nên được sử dụng sau đó.

   Một số :class:`Mailbox` phương thức được triển khai bởi :class:`!MH` đáng được lưu ý đặc biệt:


   .. method:: remove(key)
               __delitem__(key) discard(key)

      Các phương thức này ngay lập tức xóa thư. Quy ước của MH về việc đánh dấu một thư để xóa bằng cách thêm dấu phẩy vào trước tên thư không được sử dụng.


   .. method:: lock()
               unlock()

      Ba cơ chế khóa được sử dụng---khóa bằng dot và, nếu khả dụng, các
      :c:func:`!flock` và :c:func:`!lockf` system call. Đối với mailbox MH, khóa mailbox nghĩa là khóa tệp :file:`.mh_sequences` và chỉ khóa các tệp thư riêng lẻ trong khoảng thời gian thực hiện những thao tác ảnh hưởng đến chúng.


   .. method:: get_file(key)

      Tùy thuộc vào nền tảng máy chủ, có thể không thể xóa thư bên dưới trong khi tệp được trả về vẫn đang mở.


   .. method:: flush()

      Mọi thay đổi đối với mailbox MH đều được áp dụng ngay lập tức, vì vậy phương thức này không thực hiện thao tác nào.


   .. method:: close()

      Các instance :class:`!MH` không giữ tệp nào đang mở, vì vậy phương thức này tương đương với :meth:`unlock`.


.. seealso::

   `nmh - Hệ thống xử lý thư <https://www.nongnu.org/nmh/>`_
      Trang chủ của :program:`nmh`, một phiên bản cập nhật của :program:`mh` ban đầu.

   `MH & nmh: Email dành cho người dùng và lập trình viên <https://rand-mh.sourceforge.io/book/>`_
      Một cuốn sách được cấp phép GPL về :program:`mh` và :program:`nmh`, kèm một số thông tin về định dạng mailbox.


.. _mailbox-babyl:

:class:`!Babyl` các đối tượng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: Babyl(path, factory=None, create=True)

   Một lớp con của :class:`Mailbox` dành cho các mailbox ở định dạng Babyl. Tham số *factory* là một đối tượng callable chấp nhận biểu diễn thư dạng file (hoạt động như thể được mở ở chế độ nhị phân) và trả về một biểu diễn tùy chỉnh. Nếu *factory* là ``None``, :class:`BabylMessage` được dùng làm biểu diễn thư mặc định. Nếu *create* là ``True``, mailbox sẽ được tạo nếu chưa tồn tại.

   Babyl là một định dạng mailbox trong một tệp, được sử dụng bởi mail user agent Rmail đi kèm với Emacs. Phần đầu của một thư được biểu thị bằng một dòng chứa hai ký tự Control-Underscore (``'\037'``) và Control-L (``'\014'``). Phần cuối của một thư được biểu thị bằng phần bắt đầu của thư tiếp theo hoặc, trong trường hợp là thư cuối cùng, bằng một dòng chứa ký tự Control-Underscore (``'\037'``).

   Các thư trong một Babyl mailbox có hai tập header: header gốc và header được gọi là header hiển thị. Header hiển thị thường là một tập con của header gốc đã được định dạng lại hoặc rút gọn để trông hấp dẫn hơn. Mỗi thư trong Babyl mailbox cũng có một danh sách đi kèm gồm
   :dfn:`nhãn`, hoặc các chuỗi ngắn ghi lại thông tin bổ sung về thư, và một danh sách tất cả nhãn do người dùng định nghĩa được tìm thấy trong mailbox được lưu trong phần tùy chọn Babyl.

   Các instance :class:`!Babyl` có tất cả các phương thức của :class:`Mailbox` cùng với các phương thức sau:


   .. method:: get_labels()

      Trả về danh sách tên của tất cả nhãn do người dùng định nghĩa được sử dụng trong mailbox.

      .. note::

         Các thư thực tế được kiểm tra để xác định những nhãn nào tồn tại trong mailbox thay vì tham chiếu danh sách nhãn trong phần tùy chọn Babyl, nhưng phần Babyl được cập nhật mỗi khi mailbox được sửa đổi.

   Một số phương thức :class:`Mailbox` được :class:`!Babyl` triển khai cần được lưu ý đặc biệt:


   .. method:: get_file(key)

      Trong các Babyl mailbox, header của một thư không được lưu liên tục cùng với phần nội dung thư. Để tạo một biểu diễn giống tệp, header và phần nội dung được sao chép vào một instance :class:`io.BytesIO`, có API giống hệt API của một tệp. Do đó, đối tượng giống tệp này hoàn toàn độc lập với mailbox bên dưới, nhưng không tiết kiệm bộ nhớ hơn so với biểu diễn bằng chuỗi.


   .. method:: lock()
               unlock()

      Ba cơ chế khóa được sử dụng---khóa bằng tệp dot và, nếu có,
      :c:func:`!flock` và :c:func:`!lockf` system call.


.. seealso::

   `Format of Version 5 Babyl Files <https://quimby.gnus.org/notes/BABYL>`_
      Đặc tả về định dạng Babyl.

   `Reading Mail with Rmail <https://www.gnu.org/software/emacs/manual/html_node/emacs/Rmail.html>`_
      Tài liệu hướng dẫn về Rmail, kèm một số thông tin về ngữ nghĩa của Babyl.


.. _mailbox-mmdf:

Các đối tượng :class:`!MMDF`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: MMDF(path, factory=None, create=True)

   Một lớp con của :class:`Mailbox` dành cho các hộp thư ở định dạng MMDF. Tham số *factory* là một đối tượng có thể gọi, chấp nhận một biểu diễn thư dạng tệp (hoạt động như thể được mở ở chế độ nhị phân) và trả về một biểu diễn tùy chỉnh. Nếu *factory* là ``None``, :class:`MMDFMessage` được dùng làm biểu diễn thư mặc định. Nếu *create* là ``True``, hộp thư sẽ được tạo nếu chưa tồn tại.

   MMDF là một định dạng hộp thư trong một tệp duy nhất, được phát minh cho Multichannel Memorandum Distribution Facility, một mail transfer agent. Mỗi thư có cùng dạng với một thư mbox nhưng được đặt trước và sau bởi các dòng chứa bốn ký tự Control-A (``'\001'``). Cũng như với định dạng mbox, phần đầu mỗi thư được biểu thị bằng một dòng có năm ký tự đầu tiên là "From ", nhưng các lần xuất hiện thêm của "From " không được chuyển thành ">From " khi lưu thư, vì các dòng phân cách thư bổ sung ngăn việc nhầm những lần xuất hiện đó với phần bắt đầu của các thư tiếp theo.

   Một số phương thức :class:`Mailbox` do :class:`!MMDF` triển khai cần được lưu ý đặc biệt:


   .. method:: get_bytes(key, from_=False)

      Lưu ý: Phương thức này có thêm một tham số (*from_*) so với các lớp khác. Dòng đầu tiên của một mục trong tệp mbox là dòng Unix "From ". Nếu *from_* là False, dòng đầu tiên của tệp sẽ bị loại bỏ.

   .. method:: get_file(key, from_=False)

      Việc sử dụng tệp sau khi gọi :meth:`~Mailbox.flush` hoặc
      :meth:`~Mailbox.close` trên đối tượng :class:`!MMDF` có thể cho kết quả không thể dự đoán hoặc gây ra một exception.

      Lưu ý: Phương thức này có thêm một tham số (*from_*) so với các lớp khác. Dòng đầu tiên của một mục trong tệp mbox là dòng Unix "From ". Nếu *from_* là False, dòng đầu tiên của tệp sẽ bị loại bỏ.


   .. method:: lock()
               unlock()

      Ba cơ chế khóa được sử dụng---khóa bằng dấu chấm và, nếu có,
      :c:func:`!flock` và các lệnh gọi hệ thống :c:func:`!lockf`.


.. seealso::

   `trang man mmdf từ tin <http://www.tin.org/bin/man.cgi?section=5&topic=mmdf>`_
      Đặc tả về định dạng MMDF trong tài liệu của tin, một trình đọc tin tức.

   `MMDF <https://en.wikipedia.org/wiki/MMDF>`_
      Một bài viết trên Wikipedia mô tả Multichannel Memorandum Distribution Facility.


.. _mailbox-message-objects:

Các đối tượng :class:`!Message`
-------------------------------


.. class:: Message(message=None)

   Một lớp con của module :mod:`email.message`
   :class:`~email.message.Message`. Các lớp con của :class:`!mailbox.Message` bổ sung trạng thái và hành vi dành riêng cho định dạng hộp thư.

   Nếu *message* được bỏ qua, thực thể mới sẽ được tạo ở trạng thái mặc định, trống. Nếu *message* là một thực thể :class:`email.message.Message`, nội dung của nó sẽ được sao chép; hơn nữa, mọi thông tin dành riêng cho định dạng sẽ được chuyển đổi trong phạm vi có thể nếu *message* là một thực thể :class:`!Message`. Nếu *message* là một chuỗi, chuỗi byte hoặc tệp, nó phải chứa một thư :rfc:`5322`\  hợp lệ, và thư này sẽ được đọc rồi phân tích cú pháp. Các tệp nên được mở ở chế độ nhị phân, nhưng các tệp ở chế độ văn bản vẫn được chấp nhận để tương thích ngược.

   Trạng thái và hành vi dành riêng cho định dạng do các lớp con cung cấp có thể khác nhau, nhưng nhìn chung chỉ những thuộc tính không dành riêng cho một hộp thư cụ thể mới được hỗ trợ (mặc dù về nguyên tắc, các thuộc tính này dành riêng cho một định dạng hộp thư cụ thể). Ví dụ: vị trí trong tệp đối với các định dạng hộp thư dùng một tệp và tên tệp đối với các định dạng hộp thư dựa trên thư mục không được giữ lại, vì chúng chỉ áp dụng cho hộp thư ban đầu. Tuy nhiên, các trạng thái như việc người dùng đã đọc thư hay thư đã được đánh dấu là quan trọng vẫn được giữ lại, vì chúng áp dụng cho chính thư đó.

   Không bắt buộc phải sử dụng các thực thể :class:`!Message` để biểu diễn những thư được truy xuất bằng các thực thể :class:`Mailbox`. Trong một số tình huống, thời gian và bộ nhớ cần thiết để tạo các biểu diễn :class:`!Message` có thể không chấp nhận được. Trong những tình huống đó, các thực thể :class:`!Mailbox` cũng cung cấp các biểu diễn dạng chuỗi và giống tệp, đồng thời có thể chỉ định một message factory tùy chỉnh khi khởi tạo một thực thể :class:`!Mailbox`.


.. _mailbox-maildirmessage:

:class:`!MaildirMessage` đối tượng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: MaildirMessage(message=None)

   Một thư có các hành vi riêng của Maildir. Tham số *message* có cùng ý nghĩa như trong hàm khởi tạo :class:`Message`.

   Thông thường, một ứng dụng mail user agent sẽ di chuyển tất cả thư trong
   thư mục con :file:`new` sang thư mục con :file:`cur` sau lần đầu người dùng mở và đóng hộp thư, ghi nhận rằng các thư đã cũ bất kể chúng đã thực sự được đọc hay chưa. Mỗi thư trong :file:`cur` được thêm một phần "info" vào tên tệp để lưu thông tin về trạng thái của thư. (Một số trình đọc thư cũng có thể thêm phần "info" vào các thư trong
   :file:`new`.)  Phần "info" có thể có một trong hai dạng: nó có thể chứa "2," theo sau là một danh sách các cờ chuẩn hóa (ví dụ: "2,FR"), hoặc có thể chứa "1," theo sau là thông tin được gọi là thử nghiệm. Các cờ chuẩn cho thư Maildir như sau:

   +----+-------------------------+---------------------------------------+
   | Cờ | Ý nghĩa                 | Giải thích                            |
   +====+=========================+=======================================+
   | D  | Bản nháp                | Đang soạn                             |
   +----+-------------------------+---------------------------------------+
   | F  | Đã gắn cờ               | Được đánh dấu là quan trọng           |
   +----+-------------------------+---------------------------------------+
   | P  | Đã chuyển               | Đã chuyển tiếp, gửi lại hoặc hoàn trả |
   +----+-------------------------+---------------------------------------+
   | R  | Đã trả lời              | Đã trả lời                            |
   +----+-------------------------+---------------------------------------+
   | S  | Đã xem                  | Đã đọc                                |
   +----+-------------------------+---------------------------------------+
   | T  | Đã chuyển vào thùng rác | Được đánh dấu để xóa sau              |
   +----+-------------------------+---------------------------------------+

   Các instance của :class:`!MaildirMessage` cung cấp các phương thức sau:


   .. method:: get_subdir()

      Trả về "new" (nếu thư cần được lưu trong thư mục con :file:`new`) hoặc "cur" (nếu thư cần được lưu trong thư mục con :file:`cur`).

      .. note::

         Một thư thường được chuyển từ :file:`new` sang :file:`cur` sau khi hộp thư của thư đó được truy cập, bất kể thư đã được đọc hay chưa. Một thư ``msg`` đã được đọc nếu ``"S" in msg.get_flags()`` là ``True``.


   .. method:: set_subdir(subdir)

      Đặt thư mục con nơi thư sẽ được lưu trữ. Tham số *subdir* phải là "new" hoặc "cur".


   .. method:: get_flags()

      Trả về một chuỗi chỉ định các flag hiện đang được đặt. Nếu thư tuân theo định dạng Maildir chuẩn, kết quả là phép nối theo thứ tự bảng chữ cái của không hoặc một lần xuất hiện của từng flag trong ``'D'``, ``'F'``, ``'P'``, ``'R'``, ``'S'`` và ``'T'``. Chuỗi rỗng được trả về nếu không có flag nào được đặt hoặc nếu "info" chứa ngữ nghĩa thử nghiệm.


   .. method:: set_flags(flags)

      Đặt các flag được chỉ định bởi *flags* và bỏ đặt tất cả các flag khác.


   .. method:: add_flag(flag)

      Đặt các flag được chỉ định bởi *flag* mà không thay đổi các flag khác. Để thêm nhiều flag cùng lúc, *flag* có thể là một chuỗi gồm nhiều hơn một ký tự. "info" hiện tại sẽ bị ghi đè bất kể nó có chứa thông tin thử nghiệm thay vì các flag hay không.


   .. method:: remove_flag(flag)

      Bỏ đặt các flag được chỉ định bởi *flag* mà không thay đổi các flag khác. Để xóa nhiều flag cùng lúc, *flag* có thể là một chuỗi gồm nhiều hơn một ký tự. Nếu "info" chứa thông tin thử nghiệm thay vì các flag, "info" hiện tại sẽ không bị sửa đổi.


   .. method:: get_date()

      Trả về ngày gửi thư dưới dạng số dấu phẩy động biểu thị số giây kể từ kỷ nguyên.


   .. method:: set_date(date)

      Đặt ngày gửi của thư thành *date*, một số dấu phẩy động biểu thị số giây kể từ epoch.


   .. method:: get_info()

      Trả về một chuỗi chứa "info" của thư. Điều này hữu ích khi truy cập và sửa đổi "info" mang tính thử nghiệm (tức là không phải danh sách các cờ).


   .. method:: set_info(info)

      Đặt "info" thành *info*, giá trị này phải là một chuỗi.

Khi một thực thể :class:`!MaildirMessage` được tạo dựa trên một
thực thể :class:`mboxMessage` hoặc :class:`MMDFMessage`, các header :mailheader:`Status` và :mailheader:`X-Status` sẽ bị lược bỏ và các chuyển đổi sau được thực hiện:

+--------------------+---------------------------------------------------------------+
| Trạng thái kết quả | Trạng thái của :class:`mboxMessage` hoặc :class:`MMDFMessage` |
+====================+===============================================================+
| thư mục con "cur"  | cờ O                                                          |
+--------------------+---------------------------------------------------------------+
| cờ F               | cờ F                                                          |
+--------------------+---------------------------------------------------------------+
| cờ R               | cờ A                                                          |
+--------------------+---------------------------------------------------------------+
| cờ S               | cờ R                                                          |
+--------------------+---------------------------------------------------------------+
| cờ T               | cờ D                                                          |
+--------------------+---------------------------------------------------------------+

Khi một thực thể :class:`!MaildirMessage` được tạo dựa trên một
Với một instance :class:`MHMessage`, các chuyển đổi sau sẽ diễn ra:

+---------------------------+-------------------------------+
| Trạng thái kết quả        | trạng thái :class:`MHMessage` |
+===========================+===============================+
| thư mục con "cur"         | chuỗi "unseen"                |
+---------------------------+-------------------------------+
| thư mục con "cur" và cờ S | không có chuỗi "unseen"       |
+---------------------------+-------------------------------+
| cờ F                      | chuỗi "flagged"               |
+---------------------------+-------------------------------+
| cờ R                      | chuỗi "replied"               |
+---------------------------+-------------------------------+

Khi một instance :class:`!MaildirMessage` được tạo dựa trên một
instance :class:`BabylMessage`, các chuyển đổi sau sẽ diễn ra:

+---------------------------+----------------------------------+
| Trạng thái kết quả        | trạng thái :class:`BabylMessage` |
+===========================+==================================+
| thư mục con "cur"         | nhãn "unseen"                    |
+---------------------------+----------------------------------+
| thư mục con "cur" và cờ S | không có nhãn "unseen"           |
+---------------------------+----------------------------------+
| cờ P                      | nhãn "forwarded" hoặc "resent"   |
+---------------------------+----------------------------------+
| cờ R                      | nhãn "answered"                  |
+---------------------------+----------------------------------+
| cờ T                      | nhãn "deleted"                   |
+---------------------------+----------------------------------+


.. _mailbox-mboxmessage:

các đối tượng :class:`!mboxMessage`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: mboxMessage(message=None)

   Một message có các hành vi đặc thù của mbox. Tham số *message* có cùng ý nghĩa như với hàm khởi tạo :class:`Message`.

   Các message trong một mailbox mbox được lưu cùng nhau trong một tệp duy nhất. Địa chỉ phong bì của người gửi và thời điểm gửi thường được lưu trong một dòng bắt đầu bằng "From ", được dùng để chỉ phần bắt đầu của một message, mặc dù định dạng chính xác của dữ liệu này có sự khác biệt đáng kể giữa các cách triển khai mbox. Các cờ cho biết trạng thái của message, chẳng hạn như message đã được đọc hay được đánh dấu là quan trọng, thường được lưu trong
   các header :mailheader:`Status` và :mailheader:`X-Status`.

   Các cờ quy ước cho message mbox như sau:

   +----+------------+--------------------------------+
   | Cờ | Ý nghĩa    | Giải thích                     |
   +====+============+================================+
   | R  | Đã đọc     | Đã đọc                         |
   +----+------------+--------------------------------+
   | O  | Cũ         | Trước đó đã được MUA phát hiện |
   +----+------------+--------------------------------+
   | D  | Đã xóa     | Được đánh dấu để xóa sau       |
   +----+------------+--------------------------------+
   | F  | Đã gắn cờ  | Được đánh dấu là quan trọng    |
   +----+------------+--------------------------------+
   | A  | Đã trả lời | Đã hồi đáp                     |
   +----+------------+--------------------------------+

   Các cờ "R" và "O" được lưu trong header :mailheader:`Status`, còn các cờ "D", "F" và "A" được lưu trong header :mailheader:`X-Status`. Các cờ và header thường xuất hiện theo thứ tự được đề cập.

   Các instance :class:`!mboxMessage` cung cấp các phương thức sau:


   .. method:: get_from()

      Trả về một chuỗi biểu diễn dòng "From " đánh dấu phần bắt đầu của thư trong mailbox mbox. Phần "From " ở đầu và ký tự xuống dòng ở cuối không được bao gồm.


   .. method:: set_from(from_, time_=None)

      Đặt dòng "From " thành *from_*, giá trị này phải được chỉ định mà không có "From " ở đầu hoặc ký tự xuống dòng ở cuối. Để thuận tiện, có thể chỉ định *time_*, giá trị này sẽ được định dạng phù hợp và nối vào *from_*. Nếu *time_* được chỉ định, giá trị đó phải là một instance :class:`time.struct_time`, một tuple phù hợp để truyền vào :func:`time.strftime`, hoặc ``True`` (để sử dụng
      :func:`time.gmtime`).


   .. method:: get_flags()

      Trả về một chuỗi chỉ định các flag hiện đang được thiết lập. Nếu message tuân thủ định dạng quy ước, kết quả là phép nối theo thứ tự sau của không hoặc một lần xuất hiện của mỗi ``'R'``, ``'O'``, ``'D'``, ``'F'`` và ``'A'``.


   .. method:: set_flags(flags)

      Thiết lập các flag được chỉ định bởi *flags* và bỏ thiết lập tất cả các flag khác. Tham số *flags* phải là phép nối theo bất kỳ thứ tự nào của không hoặc nhiều lần xuất hiện của mỗi ``'R'``, ``'O'``, ``'D'``, ``'F'`` và ``'A'``.


   .. method:: add_flag(flag)

      Thiết lập các flag được chỉ định bởi *flag* mà không thay đổi các flag khác. Để thêm nhiều flag cùng lúc, *flag* có thể là một chuỗi gồm nhiều hơn một ký tự.


   .. method:: remove_flag(flag)

      Bỏ thiết lập các flag được chỉ định bởi *flag* mà không thay đổi các flag khác. Để xóa nhiều flag cùng lúc, *flag* có thể là một chuỗi gồm nhiều hơn một ký tự.

Khi một instance :class:`!mboxMessage` được tạo dựa trên một
instance :class:`MaildirMessage`, một dòng "From " được tạo dựa trên
ngày gửi của instance :class:`MaildirMessage` và các chuyển đổi sau được thực hiện:

+--------------------+------------------------------------+
| Trạng thái kết quả | :class:`MaildirMessage` trạng thái |
+====================+====================================+
| cờ R               | cờ S                               |
+--------------------+------------------------------------+
| cờ O               | thư mục con "cur"                  |
+--------------------+------------------------------------+
| cờ D               | Cờ T                               |
+--------------------+------------------------------------+
| Cờ F               | Cờ F                               |
+--------------------+------------------------------------+
| Cờ A               | Cờ R                               |
+--------------------+------------------------------------+

Khi một đối tượng :class:`!mboxMessage` được tạo dựa trên một
đối tượng :class:`MHMessage`, các chuyển đổi sau sẽ diễn ra:

+--------------------+-------------------------------+
| Trạng thái kết quả | trạng thái :class:`MHMessage` |
+====================+===============================+
| cờ R và cờ O       | không có sequence "unseen"    |
+--------------------+-------------------------------+
| cờ O               | sequence "unseen"             |
+--------------------+-------------------------------+
| cờ F               | chuỗi "flagged"               |
+--------------------+-------------------------------+
| Một cờ             | chuỗi "replied"               |
+--------------------+-------------------------------+

Khi một instance :class:`!mboxMessage` được tạo dựa trên một
:class:`BabylMessage` instance, các chuyển đổi sau sẽ diễn ra:

+--------------------+----------------------------------+
| Trạng thái kết quả | trạng thái :class:`BabylMessage` |
+====================+==================================+
| cờ R và cờ O       | không có nhãn "unseen"           |
+--------------------+----------------------------------+
| cờ O               | nhãn "unseen"                    |
+--------------------+----------------------------------+
| cờ D               | nhãn "deleted"                   |
+--------------------+----------------------------------+
| Một cờ             | nhãn "answered"                  |
+--------------------+----------------------------------+

Khi một instance :class:`!mboxMessage` được tạo dựa trên một
instance :class:`MMDFMessage`, dòng "From " được sao chép và tất cả các cờ tương ứng trực tiếp:

+--------------------+---------------------------------+
| Trạng thái kết quả | trạng thái :class:`MMDFMessage` |
+====================+=================================+
| cờ R               | cờ R                            |
+--------------------+---------------------------------+
| cờ O               | Cờ O                            |
+--------------------+---------------------------------+
| cờ D               | Cờ D                            |
+--------------------+---------------------------------+
| Cờ F               | Cờ F                            |
+--------------------+---------------------------------+
| Cờ A               | Một cờ                          |
+--------------------+---------------------------------+


.. _mailbox-mhmessage:

Các đối tượng :class:`!MHMessage`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: MHMessage(message=None)

   Một message với các hành vi dành riêng cho MH. Tham số *message* có cùng ý nghĩa như với hàm khởi tạo :class:`Message`.

   Các message MH không hỗ trợ mark hoặc flag theo nghĩa truyền thống, nhưng hỗ trợ sequence, tức các nhóm logic gồm những message tùy ý. Một số chương trình đọc thư (mặc dù không phải :program:`mh` tiêu chuẩn và
   :program:`nmh`) sử dụng sequence gần như cách flag được sử dụng với các định dạng khác, như sau:

   +-------------+-----------------------------------------------+
   | Sequence    | Giải thích                                    |
   +=============+===============================================+
   | chưa xem    | Chưa đọc nhưng trước đó đã được MUA phát hiện |
   +-------------+-----------------------------------------------+
   | đã trả lời  | Đã trả lời                                    |
   +-------------+-----------------------------------------------+
   | đã đánh dấu | Được đánh dấu là quan trọng                   |
   +-------------+-----------------------------------------------+

   Các đối tượng :class:`!MHMessage` cung cấp các phương thức sau:


   .. method:: get_sequences()

      Trả về danh sách tên của các sequence có chứa message này.


   .. method:: set_sequences(sequences)

      Đặt danh sách các sequence có chứa message này.


   .. method:: add_sequence(sequence)

      Thêm *sequence* vào danh sách các sequence có chứa message này.


   .. method:: remove_sequence(sequence)

      Xóa *sequence* khỏi danh sách các sequence có chứa message này.

Khi một instance :class:`!MHMessage` được tạo dựa trên một
instance :class:`MaildirMessage`, các chuyển đổi sau sẽ diễn ra:

+--------------------+------------------------------------+
| Trạng thái kết quả | trạng thái :class:`MaildirMessage` |
+====================+====================================+
| sequence "unseen"  | không có flag S                    |
+--------------------+------------------------------------+
| sequence "replied" | flag R                             |
+--------------------+------------------------------------+
| sequence "flagged" | flag F                             |
+--------------------+------------------------------------+

Khi một thể hiện :class:`!MHMessage` được tạo dựa trên một
thể hiện :class:`mboxMessage` hoặc :class:`MMDFMessage`, các header :mailheader:`Status` và :mailheader:`X-Status` bị bỏ qua và các chuyển đổi sau đây diễn ra:

+--------------------+---------------------------------------------------------------+
| Trạng thái kết quả | trạng thái của :class:`mboxMessage` hoặc :class:`MMDFMessage` |
+====================+===============================================================+
| sequence "unseen"  | không có cờ R                                                 |
+--------------------+---------------------------------------------------------------+
| sequence "replied" | Cờ A                                                          |
+--------------------+---------------------------------------------------------------+
| sequence "flagged" | Cờ F                                                          |
+--------------------+---------------------------------------------------------------+

Khi một instance :class:`!MHMessage` được tạo dựa trên một
Đối với một :class:`BabylMessage` instance, các chuyển đổi sau sẽ diễn ra:

+--------------------+----------------------------------+
| Trạng thái kết quả | trạng thái :class:`BabylMessage` |
+====================+==================================+
| sequence "unseen"  | nhãn "unseen"                    |
+--------------------+----------------------------------+
| sequence "replied" | nhãn "answered"                  |
+--------------------+----------------------------------+


.. _mailbox-babylmessage:

đối tượng :class:`!BabylMessage`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: BabylMessage(message=None)

   Một message có các hành vi riêng của Babyl. Tham số *message* có cùng ý nghĩa như trong constructor :class:`Message`.

   Một số nhãn message, được gọi là :dfn:`attributes`, được quy ước để có những ý nghĩa đặc biệt. Các attributes như sau:

   +----------------+-----------------------------------------------+
   | Nhãn           | Giải thích                                    |
   +================+===============================================+
   | chưa xem       | Chưa đọc nhưng trước đó đã được MUA phát hiện |
   +----------------+-----------------------------------------------+
   | đã xóa         | Được đánh dấu để xóa sau                      |
   +----------------+-----------------------------------------------+
   | đã lưu         | Đã sao chép sang tệp hoặc hộp thư khác        |
   +----------------+-----------------------------------------------+
   | đã trả lời     | Đã trả lời                                    |
   +----------------+-----------------------------------------------+
   | đã chuyển tiếp | Đã chuyển tiếp                                |
   +----------------+-----------------------------------------------+
   | đã chỉnh sửa   | Được người dùng sửa đổi                       |
   +----------------+-----------------------------------------------+
   | đã gửi lại     | Đã gửi lại                                    |
   +----------------+-----------------------------------------------+

   Theo mặc định, Rmail chỉ hiển thị các header hiển thị. Tuy nhiên, lớp :class:`!BabylMessage` sử dụng các header gốc vì chúng đầy đủ hơn. Nếu muốn, bạn có thể truy cập rõ ràng các header hiển thị.

   Các đối tượng :class:`!BabylMessage` cung cấp những phương thức sau:


   .. method:: get_labels()

      Trả về danh sách các nhãn trên thư.


   .. method:: set_labels(labels)

      Đặt danh sách nhãn trên thư thành *labels*.


   .. method:: add_label(label)

      Thêm *label* vào danh sách các nhãn trên thư.


   .. method:: remove_label(label)

      Xóa *label* khỏi danh sách nhãn trên thư.


   .. method:: get_visible()

      Trả về một instance :class:`Message` có các header là những header hiển thị của thư và phần thân rỗng.


   .. method:: set_visible(visible)

      Đặt các header hiển thị của thư giống với các header trong *message*. Tham số *visible* phải là một instance :class:`Message`, một
      instance :class:`email.message.Message`, một chuỗi hoặc một đối tượng giống tệp (đối tượng này phải được mở ở chế độ văn bản).


   .. method:: update_visible()

      Khi các header gốc của một instance :class:`!BabylMessage` được sửa đổi, các header hiển thị không tự động được sửa đổi tương ứng. Phương thức này cập nhật các header hiển thị như sau: mỗi header hiển thị có header gốc tương ứng được đặt thành giá trị của header gốc, mỗi header hiển thị không có header gốc tương ứng sẽ bị xóa, và bất kỳ :mailheader:`Date`, :mailheader:`From`, :mailheader:`Reply-To` nào
      :mailheader:`To`, :mailheader:`CC` và :mailheader:`Subject` xuất hiện trong các header gốc nhưng không có trong các header hiển thị sẽ được thêm vào các header hiển thị.

Khi một instance :class:`!BabylMessage` được tạo dựa trên một
Đối với một thể hiện :class:`MaildirMessage`, các chuyển đổi sau diễn ra:

+--------------------+------------------------------------+
| Trạng thái kết quả | Trạng thái :class:`MaildirMessage` |
+====================+====================================+
| nhãn "chưa xem"    | không có cờ S                      |
+--------------------+------------------------------------+
| nhãn "đã xóa"      | cờ T                               |
+--------------------+------------------------------------+
| nhãn "answered"    | cờ R                               |
+--------------------+------------------------------------+
| nhãn "forwarded"   | cờ P                               |
+--------------------+------------------------------------+

Khi một thực thể :class:`!BabylMessage` được tạo dựa trên một
thực thể :class:`mboxMessage` hoặc :class:`MMDFMessage`, các header :mailheader:`Status` và :mailheader:`X-Status` sẽ bị lược bỏ và các chuyển đổi sau sẽ diễn ra:

+--------------------+-----------------------------------------------------------+
| Trạng thái kết quả | trạng thái :class:`mboxMessage` hoặc :class:`MMDFMessage` |
+====================+===========================================================+
| nhãn "chưa xem"    | không có cờ R                                             |
+--------------------+-----------------------------------------------------------+
| nhãn "đã xóa"      | cờ D                                                      |
+--------------------+-----------------------------------------------------------+
| nhãn "answered"    | cờ A                                                      |
+--------------------+-----------------------------------------------------------+

Khi một thực thể :class:`!BabylMessage` được tạo dựa trên một
instance :class:`MHMessage`, các chuyển đổi sau diễn ra:

+--------------------+-------------------------------+
| Trạng thái kết quả | trạng thái :class:`MHMessage` |
+====================+===============================+
| nhãn "chưa xem"    | chuỗi "unseen"                |
+--------------------+-------------------------------+
| nhãn "answered"    | chuỗi "replied"               |
+--------------------+-------------------------------+


.. _mailbox-mmdfmessage:

các đối tượng :class:`!MMDFMessage`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: MMDFMessage(message=None)

   Một message với các hành vi dành riêng cho MMDF. Tham số *message* có cùng ý nghĩa như với hàm khởi tạo :class:`Message`.

   Tương tự message trong mailbox mbox, các message MMDF được lưu trữ cùng với địa chỉ người gửi và ngày gửi trong một dòng mở đầu bắt đầu bằng "From ". Tương tự, các cờ cho biết trạng thái của message thường được lưu trong các header :mailheader:`Status` và :mailheader:`X-Status`.

   Các cờ quy ước cho message MMDF giống hệt các cờ của message mbox và như sau:

   +----+-------------+---------------------------------+
   | Cờ | Ý nghĩa     | Giải thích                      |
   +====+=============+=================================+
   | R  | Đã đọc      | Đã đọc                          |
   +----+-------------+---------------------------------+
   | O  | Cũ          | Trước đây đã được MUA phát hiện |
   +----+-------------+---------------------------------+
   | D  | Đã xóa      | Được đánh dấu để xóa sau        |
   +----+-------------+---------------------------------+
   | F  | Được gắn cờ | Được đánh dấu là quan trọng     |
   +----+-------------+---------------------------------+
   | A  | Đã trả lời  | Đã trả lời cho                  |
   +----+-------------+---------------------------------+

   Các cờ "R" và "O" được lưu trong header :mailheader:`Status`, còn các cờ "D", "F" và "A" được lưu trong header :mailheader:`X-Status`. Các cờ và header thường xuất hiện theo thứ tự được đề cập.

   Các instance :class:`!MMDFMessage` cung cấp những phương thức sau, giống hệt các phương thức được cung cấp bởi :class:`mboxMessage`:


   .. method:: get_from()

      Trả về một chuỗi biểu diễn dòng "From " đánh dấu phần đầu của thư trong mailbox mbox. Phần "From " ở đầu và ký tự xuống dòng ở cuối không được bao gồm.


   .. method:: set_from(from_, time_=None)

      Đặt dòng "From " thành *from_*, giá trị này phải được chỉ định mà không có "From " ở đầu hoặc ký tự xuống dòng ở cuối. Để thuận tiện, có thể chỉ định *time_*; giá trị này sẽ được định dạng thích hợp và nối vào *from_*. Nếu chỉ định *time_*, giá trị đó phải là một instance :class:`time.struct_time`, một tuple phù hợp để truyền vào :func:`time.strftime`, hoặc ``True`` (để sử dụng
      :func:`time.gmtime`).


   .. method:: get_flags()

      Trả về một chuỗi chỉ định các cờ hiện đang được thiết lập. Nếu thư tuân theo định dạng quy ước, kết quả là phép nối, theo thứ tự sau, của không hoặc một lần xuất hiện của từng cờ trong ``'R'``, ``'O'``, ``'D'``, ``'F'`` và ``'A'``.


   .. method:: set_flags(flags)

      Đặt các cờ được chỉ định bởi *flags* và bỏ đặt tất cả các cờ khác. Tham số *flags* phải là phép nối, theo bất kỳ thứ tự nào, của không hoặc nhiều lần xuất hiện của từng cờ trong số ``'R'``, ``'O'``, ``'D'``, ``'F'`` và ``'A'``.


   .. method:: add_flag(flag)

      Đặt (các) cờ được chỉ định bởi *flag* mà không thay đổi các cờ khác. Để thêm nhiều cờ cùng lúc, *flag* có thể là một chuỗi gồm nhiều hơn một ký tự.


   .. method:: remove_flag(flag)

      Bỏ đặt (các) cờ được chỉ định bởi *flag* mà không thay đổi các cờ khác. Để xóa nhiều cờ cùng lúc, *flag* có thể là một chuỗi gồm nhiều hơn một ký tự.

Khi một thực thể :class:`!MMDFMessage` được tạo dựa trên một
thực thể :class:`MaildirMessage`, một dòng "From " được tạo dựa trên
ngày gửi của thực thể :class:`MaildirMessage` và các chuyển đổi sau được thực hiện:

+---------------------+------------------------------------+
| Trạng thái sau cùng | :class:`MaildirMessage` trạng thái |
+=====================+====================================+
| cờ R                | cờ S                               |
+---------------------+------------------------------------+
| cờ O                | thư mục con "cur"                  |
+---------------------+------------------------------------+
| cờ D                | cờ T                               |
+---------------------+------------------------------------+
| Cờ F                | Cờ F                               |
+---------------------+------------------------------------+
| Cờ A                | Cờ R                               |
+---------------------+------------------------------------+

Khi một thể hiện :class:`!MMDFMessage` được tạo dựa trên một
thể hiện :class:`MHMessage`, các chuyển đổi sau sẽ diễn ra:

+---------------------+-------------------------------+
| Trạng thái sau cùng | trạng thái :class:`MHMessage` |
+=====================+===============================+
| cờ R và cờ O        | không có sequence "unseen"    |
+---------------------+-------------------------------+
| cờ O                | sequence "unseen"             |
+---------------------+-------------------------------+
| cờ F                | sequence "flagged"            |
+---------------------+-------------------------------+
| Một cờ              | chuỗi "replied"               |
+---------------------+-------------------------------+

Khi một thực thể :class:`!MMDFMessage` được tạo dựa trên một
Đối với instance :class:`BabylMessage`, các chuyển đổi sau sẽ diễn ra:

+---------------------+----------------------------------+
| Trạng thái sau cùng | trạng thái :class:`BabylMessage` |
+=====================+==================================+
| cờ R và cờ O        | không có nhãn "unseen"           |
+---------------------+----------------------------------+
| cờ O                | nhãn "unseen"                    |
+---------------------+----------------------------------+
| cờ D                | nhãn "deleted"                   |
+---------------------+----------------------------------+
| Một cờ              | nhãn "answered"                  |
+---------------------+----------------------------------+

Khi một thể hiện :class:`!MMDFMessage` được tạo dựa trên một
Trong một :class:`mboxMessage` instance, dòng "From " được sao chép và tất cả các flag đều tương ứng trực tiếp:

+---------------------+---------------------------------+
| Trạng thái sau cùng | trạng thái :class:`mboxMessage` |
+=====================+=================================+
| cờ R                | Cờ R                            |
+---------------------+---------------------------------+
| cờ O                | Cờ O                            |
+---------------------+---------------------------------+
| cờ D                | Cờ D                            |
+---------------------+---------------------------------+
| Cờ F                | Cờ F                            |
+---------------------+---------------------------------+
| Cờ A                | Cờ A                            |
+---------------------+---------------------------------+


Ngoại lệ
--------

Các lớp ngoại lệ sau được định nghĩa trong module :mod:`!mailbox`:


.. exception:: Error()

   Lớp cơ sở cho tất cả các ngoại lệ khác dành riêng cho module.


.. exception:: NoSuchMailboxError()

   Được phát sinh khi dự kiến sẽ có một mailbox nhưng không tìm thấy, chẳng hạn như khi khởi tạo một
   lớp con :class:`Mailbox` với đường dẫn không tồn tại (và tham số *create* được đặt thành ``False``), hoặc khi mở một thư mục không tồn tại.


.. exception:: NotEmptyError()

   Được phát sinh khi một mailbox không trống nhưng được dự kiến là phải trống, chẳng hạn như khi xóa một thư mục chứa thư.


.. exception:: ExternalClashError()

   Được phát sinh khi một điều kiện liên quan đến mailbox nằm ngoài tầm kiểm soát của chương trình khiến chương trình không thể tiếp tục, chẳng hạn như khi không thể lấy được một lock mà chương trình khác đang giữ, hoặc khi một tên tệp được tạo duy nhất đã tồn tại.


.. exception:: FormatError()

   Được phát sinh khi dữ liệu trong một tệp không thể được phân tích cú pháp, chẳng hạn khi một thực thể :class:`MH` cố đọc một tệp :file:`.mh_sequences` bị hỏng.


.. _mailbox-examples:

Ví dụ
-----

Một ví dụ đơn giản về việc in tiêu đề của tất cả thư trong một mailbox có vẻ đáng chú ý::

   import mailbox
   for message in mailbox.mbox('~/mbox'):
       subject = message['subject']       # Có thể là None.
       if subject and 'python' in subject.lower():
           print(subject)

Để sao chép tất cả thư từ một mailbox Babyl sang một mailbox MH, đồng thời chuyển đổi mọi thông tin đặc thù của định dạng có thể chuyển đổi::

   import mailbox
   destination = mailbox.MH('~/Mail')
   destination.lock()
   for message in mailbox.Babyl('~/RMAIL'):
       destination.add(mailbox.MHMessage(message))
   destination.flush()
   destination.unlock()

Ví dụ này sắp xếp thư từ một số mailing list vào các mailbox khác nhau, đồng thời cẩn thận tránh làm hỏng thư do các chương trình khác sửa đổi đồng thời, tránh mất thư do chương trình bị gián đoạn hoặc kết thúc sớm do các thư không đúng định dạng trong mailbox::

   import mailbox
   import email.errors

   list_names = ('python-list', 'python-dev', 'python-bugs')

   boxes = {name: mailbox.mbox('~/email/%s' % name) for name in list_names}
   inbox = mailbox.Maildir('~/Maildir', factory=None)

   for key in inbox.iterkeys():
       try:
           message = inbox[key]
       except email.errors.MessageParseError:
           continue                # Thư không đúng định dạng. Cứ để nguyên.

       for name in list_names:
           list_id = message['list-id']
           if list_id and name in list_id:
               # Lấy mailbox để sử dụng
               box = boxes[name]

               # Ghi bản sao vào đĩa trước khi xóa bản gốc.
               # If there's a crash, you might duplicate a message, but
               # điều đó vẫn tốt hơn là mất hoàn toàn một message.
               box.lock()
               box.add(message)
               box.flush()
               box.unlock()

               # Xóa message gốc
               inbox.lock()
               inbox.discard(key)
               inbox.flush()
               inbox.unlock()
               break               # Đã tìm thấy đích nên dừng tìm kiếm.

   for box in boxes.itervalues():
       box.close()

.. _`maildir man page from Courier`: https://www.courier-mta.org/maildir.html
.. _`Using maildir format`: https://cr.yp.to/proto/maildir.html
.. _`mbox man page from tin`: http://www.tin.org/bin/man.cgi?section=5&topic=mbox
.. _`Configuring Netscape Mail on Unix: Why The Content-Length Format is Bad`: https://www.jwz.org/doc/content-length.html
.. _`"mbox" is a family of several mutually incompatible mailbox formats`: https://www.loc.gov/preservation/digital/formats/fdd/fdd000383.shtml
.. _`nmh - Message Handling System`: https://www.nongnu.org/nmh/
.. _`MH & nmh: Email for Users & Programmers`: https://rand-mh.sourceforge.io/book/
.. _`Format of Version 5 Babyl Files`: https://quimby.gnus.org/notes/BABYL
.. _`Reading Mail with Rmail`: https://www.gnu.org/software/emacs/manual/html_node/emacs/Rmail.html
.. _`mmdf man page from tin`: http://www.tin.org/bin/man.cgi?section=5&topic=mmdf
.. _`MMDF`: https://en.wikipedia.org/wiki/MMDF
