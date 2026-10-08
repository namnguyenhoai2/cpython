:mod:`!selectors` --- Ghép kênh I/O cấp cao
===========================================

.. module:: selectors
   :synopsis: Ghép kênh I/O cấp cao.

.. versionadded:: 3.4

**Mã nguồn:** :source:`Lib/selectors.py`

--------------

Giới thiệu
----------

Module này cung cấp khả năng ghép kênh I/O cấp cao và hiệu quả, được xây dựng dựa trên các
:mod:`select` nguyên thủy của module. Người dùng nên sử dụng module này thay thế, trừ khi họ muốn kiểm soát chính xác các nguyên thủy ở cấp hệ điều hành được sử dụng.

Module định nghĩa một lớp cơ sở trừu tượng :class:`BaseSelector`, cùng với một số triển khai cụ thể (:class:`KqueueSelector`, :class:`EpollSelector`...), có thể được dùng để chờ thông báo về trạng thái sẵn sàng I/O trên nhiều đối tượng tệp. Trong phần sau, "đối tượng tệp" đề cập đến bất kỳ đối tượng nào có một
:meth:`~io.IOBase.fileno` phương thức hoặc một file descriptor thô. Xem :term:`file object`.

:class:`DefaultSelector` là bí danh của implementation hiệu quả nhất hiện có trên nền tảng hiện tại: đây nên là lựa chọn mặc định cho hầu hết người dùng.

.. note::
   Loại đối tượng tệp được hỗ trợ phụ thuộc vào nền tảng: trên Windows, socket được hỗ trợ nhưng pipe thì không, trong khi trên Unix, cả hai đều được hỗ trợ (một số loại khác cũng có thể được hỗ trợ, chẳng hạn như fifo hoặc thiết bị tệp đặc biệt).

.. seealso::

   :mod:`select`
      Module multiplexing I/O cấp thấp.

.. include:: ../includes/wasm-notavail.rst

Các class
---------

Phân cấp class::

   BaseSelector
   +-- SelectSelector
   +-- PollSelector
   +-- EpollSelector
   +-- DevpollSelector
   +-- KqueueSelector


Trong phần sau, *events* là một bitwise mask cho biết cần chờ những sự kiện I/O nào trên một đối tượng tệp nhất định. Nó có thể là sự kết hợp của các hằng số dưới đây trong module:

   +-----------------------+------------+
   | Hằng số               | Ý nghĩa    |
   +=======================+============+
   | .. data:: EVENT_READ  | Có thể đọc |
   +-----------------------+------------+
   | .. data:: EVENT_WRITE | Có thể ghi |
   +-----------------------+------------+


.. class:: SelectorKey

   :class:`SelectorKey` là một :class:`~collections.namedtuple` dùng để liên kết một đối tượng tệp với file descriptor cơ bản, event mask đã chọn và dữ liệu đính kèm. Nó được một số phương thức :class:`BaseSelector` trả về.

   .. attribute:: fileobj

      Đối tượng tệp đã được đăng ký.

   .. attribute:: fd

      File descriptor cơ bản.

   .. attribute:: events

      Các sự kiện phải chờ trên đối tượng tệp này.

   .. attribute:: data

      Dữ liệu opaque tùy chọn được liên kết với đối tượng tệp này: ví dụ, dữ liệu này có thể được dùng để lưu trữ session ID riêng cho từng client.


.. class:: BaseSelector

   Một :class:`BaseSelector` được dùng để chờ trạng thái sẵn sàng của sự kiện I/O trên nhiều đối tượng tệp. Nó hỗ trợ đăng ký và hủy đăng ký các stream tệp, cũng như một phương thức chờ các sự kiện I/O trên những stream đó, với thời gian chờ tùy chọn. Đây là một abstract base class nên không thể được khởi tạo. Thay vào đó, hãy dùng
   :class:`DefaultSelector`, hoặc một trong các :class:`SelectSelector`,
   :class:`KqueueSelector` v.v. nếu bạn muốn sử dụng cụ thể một implementation và nền tảng của bạn hỗ trợ implementation đó.
   :class:`BaseSelector` và các implementation cụ thể của nó hỗ trợ
   protocol :term:`context manager`.

   .. method:: register(fileobj, events, data=None)
      :abstractmethod:

      Đăng ký một đối tượng tệp để chọn, đồng thời theo dõi đối tượng đó để phát hiện các sự kiện I/O.

      *fileobj* là đối tượng tệp cần theo dõi. Đối tượng này có thể là một bộ mô tả tệp dạng số nguyên hoặc một đối tượng có phương thức ``fileno()``. *events* là mặt nạ bit của các sự kiện cần theo dõi. *data* là một đối tượng không công khai cấu trúc.

      Phương thức này trả về một thực thể :class:`SelectorKey` mới hoặc phát sinh một
      :exc:`ValueError` trong trường hợp mặt nạ sự kiện hoặc bộ mô tả tệp không hợp lệ, hoặc
      :exc:`KeyError` nếu đối tượng tệp đã được đăng ký.

   .. method:: unregister(fileobj)
      :abstractmethod:

      Hủy đăng ký một đối tượng tệp khỏi hoạt động chọn, loại bỏ đối tượng đó khỏi danh sách theo dõi. Phải hủy đăng ký đối tượng tệp trước khi đóng đối tượng.

      *fileobj* phải là một đối tượng tệp đã được đăng ký trước đó.

      Phương thức này trả về instance :class:`SelectorKey` tương ứng hoặc phát sinh một
      :exc:`KeyError` nếu *fileobj* chưa được đăng ký. Phương thức sẽ phát sinh
      :exc:`ValueError` nếu *fileobj* không hợp lệ (ví dụ: không có phương thức ``fileno()`` hoặc phương thức ``fileno()`` trả về giá trị không hợp lệ).

   .. method:: modify(fileobj, events, data=None)

      Thay đổi các sự kiện được theo dõi hoặc dữ liệu đính kèm của đối tượng file đã đăng ký.

      Tương đương với ``BaseSelector.unregister(fileobj)`` theo sau bởi ``BaseSelector.register(fileobj, events, data)``, nhưng có thể được triển khai hiệu quả hơn.

      Phương thức này trả về một thực thể :class:`SelectorKey` mới hoặc phát sinh một
      :exc:`ValueError` trong trường hợp mặt nạ sự kiện hoặc bộ mô tả tệp không hợp lệ, hoặc
      :exc:`KeyError` nếu đối tượng tệp chưa được đăng ký.

   .. method:: select(timeout=None)
      :abstractmethod:

      Chờ cho đến khi một số đối tượng tệp đã đăng ký sẵn sàng hoặc thời gian chờ hết hạn.

      Nếu ``timeout > 0``, tùy chọn này chỉ định thời gian chờ tối đa, tính bằng giây. Nếu ``timeout <= 0``, lệnh gọi sẽ không chặn và sẽ báo cáo các đối tượng tệp hiện đang sẵn sàng. Nếu *timeout* là ``None``, lệnh gọi sẽ chặn cho đến khi một đối tượng tệp được theo dõi sẵn sàng.

      Phương thức này trả về một danh sách gồm các tuple ``(key, events)``, mỗi tuple tương ứng với một đối tượng tệp đang sẵn sàng.

      *key* là instance :class:`SelectorKey` tương ứng với một đối tượng tệp đang sẵn sàng. *events* là bitmask biểu thị các sự kiện đang sẵn sàng trên đối tượng tệp này.

      .. note::
          Phương thức này có thể trả về trước khi bất kỳ đối tượng tệp nào sẵn sàng hoặc trước khi thời gian chờ hết hạn nếu tiến trình hiện tại nhận được một signal: trong trường hợp này, một danh sách rỗng sẽ được trả về.

      .. versionchanged:: 3.5
         Selector sẽ được thử lại với thời gian chờ được tính toán lại khi bị gián đoạn bởi một signal nếu signal handler không phát sinh ngoại lệ (xem
         :pep:`475` để biết lý do), thay vì trả về một danh sách sự kiện rỗng trước khi hết thời gian chờ.

   .. method:: close()

      Đóng selector.

      Phải gọi phương thức này để đảm bảo mọi tài nguyên nền tảng được giải phóng. Không được sử dụng selector sau khi đã đóng.

   .. method:: get_key(fileobj)

      Trả về key được liên kết với một file object đã đăng ký.

      Phương thức này trả về instance :class:`SelectorKey` được liên kết với file object này hoặc phát sinh :exc:`KeyError` nếu file object chưa được đăng ký.

   .. method:: get_map()
      :abstractmethod:

      Trả về một mapping từ file object đến selector key.

      Phương thức này trả về một instance :class:`~collections.abc.Mapping` ánh xạ các file object đã đăng ký tới instance :class:`SelectorKey` tương ứng của chúng.


.. class:: DefaultSelector()

   Lớp selector mặc định, sử dụng triển khai hiệu quả nhất hiện có trên nền tảng hiện tại. Đây nên là lựa chọn mặc định cho hầu hết người dùng.


.. class:: SelectSelector()

   selector dựa trên :func:`select.select`.


.. class:: PollSelector()

   selector dựa trên :func:`select.poll`.


.. class:: EpollSelector()

   selector dựa trên :func:`select.epoll`.

   .. method:: fileno()

      Phương thức này trả về file descriptor được sử dụng bởi
      đối tượng :func:`select.epoll`.

.. class:: DevpollSelector()

   selector dựa trên :func:`select.devpoll`.

   .. method:: fileno()

      Phương thức này trả về file descriptor được sử dụng bởi
      :func:`select.devpoll` đối tượng.

   .. versionadded:: 3.5

.. class:: KqueueSelector()

   Bộ chọn dựa trên :func:`select.kqueue`.

   .. method:: fileno()

      Phương thức này trả về file descriptor được sử dụng bởi
      :func:`select.kqueue` đối tượng.


Ví dụ
-----

Dưới đây là một triển khai máy chủ echo đơn giản::

   import selectors
   import socket

   sel = selectors.DefaultSelector()

   def accept(sock, mask):
       conn, addr = sock.accept()  # Sẽ sẵn sàng
       print('accepted', conn, 'from', addr)
       conn.setblocking(False)
       sel.register(conn, selectors.EVENT_READ, read)

   def read(conn, mask):
       data = conn.recv(1000)  # Sẽ sẵn sàng
       if data:
           print('echoing', repr(data), 'to', conn)
           conn.send(data)  # Hy vọng nó sẽ không chặn
       else:
           print('closing', conn)
           sel.unregister(conn)
           conn.close()

   sock = socket.socket()
   sock.bind(('localhost', 1234))
   sock.listen(100)
   sock.setblocking(False)
   sel.register(sock, selectors.EVENT_READ, accept)

   while True:
       events = sel.select()
       for key, mask in events:
           callback = key.data
           callback(key.fileobj, mask)
