.. _timerfd-howto:

*******************************
HƯỚNG DẪN về bộ mô tả tệp timer
*******************************

:Release: 1.13

HƯỚNG DẪN này trình bày về khả năng hỗ trợ bộ mô tả tệp timer của Linux trong Python.


Ví dụ
=====

Ví dụ sau đây cho thấy cách sử dụng bộ mô tả tệp timer để thực thi một hàm hai lần mỗi giây:

.. code-block:: python

   # Các script thực tế nên thực sự sử dụng timer không chặn,
   # ở đây chúng ta sử dụng timer chặn để đơn giản hóa.
   import os, time

   # Tạo bộ mô tả tệp timer
   fd = os.timerfd_create(time.CLOCK_REALTIME)

   # Khởi động bộ hẹn giờ sau 1 giây, với khoảng thời gian là nửa giây
   os.timerfd_settime(fd, initial=1, interval=0.5)

   try:
       # Xử lý các sự kiện của bộ hẹn giờ bốn lần.
       for _ in range(4):
           # read() sẽ chặn cho đến khi bộ hẹn giờ hết hạn
           _ = os.read(fd, 8)
           print("Timer expired")
   finally:
       # Nhớ đóng bộ mô tả tệp của bộ hẹn giờ!
       os.close(fd)

Để tránh mất độ chính xác do kiểu :class:`float` gây ra, bộ mô tả tệp của bộ hẹn giờ cho phép chỉ định thời điểm hết hạn ban đầu và khoảng thời gian tính bằng nanosecond nguyên với các biến thể ``_ns`` của các hàm.

Ví dụ này cho thấy cách có thể sử dụng :func:`~select.epoll` với các bộ mô tả tệp của bộ hẹn giờ để chờ cho đến khi bộ mô tả tệp sẵn sàng cho việc đọc:

.. code-block:: python

   import os, time, select, socket, sys

   # Tạo một đối tượng epoll
   ep = select.epoll()

   # Trong ví dụ này, sử dụng địa chỉ loopback để gửi lệnh "stop" đến server.
   #
   # $ telnet 127.0.0.1 1234
   # Đang thử 127.0.0.1...
   # Đã kết nối với 127.0.0.1.
   # Ký tự thoát là '^]'.
   # stop
   # Kết nối đã bị máy chủ từ xa đóng.
   #
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.bind(("127.0.0.1", 1234))
   sock.setblocking(False)
   sock.listen(1)
   ep.register(sock, select.EPOLLIN)

   # Tạo các file descriptor của timer ở chế độ không chặn.
   num = 3
   fds = []
   for _ in range(num):
       fd = os.timerfd_create(time.CLOCK_REALTIME, flags=os.TFD_NONBLOCK)
       fds.append(fd)
       # Đăng ký file descriptor của timer cho các sự kiện đọc.
       ep.register(fd, select.EPOLLIN)

   # Khởi động timer bằng os.timerfd_settime_ns() với đơn vị nanosecond.
   # Timer 1 kích hoạt mỗi 0.25 giây; timer 2 mỗi 0.5 giây; v.v.
   for i, fd in enumerate(fds, start=1):
       one_sec_in_nsec = 10**9
       i = i * one_sec_in_nsec
       os.timerfd_settime_ns(fd, initial=i//4, interval=i//4)

   timeout = 3
   try:
       conn = None
       is_active = True
       while is_active:
           # Chờ timer hết hạn trong 3 giây.
           # epoll.poll() trả về một danh sách các cặp (fd, event).
           # fd là một file descriptor.
           # sock và conn[=returned value of socket.accept()] là các đối tượng socket, không phải file descriptor.
           # Vì vậy, hãy dùng sock.fileno() và conn.fileno() để lấy các file descriptor.
           events = ep.poll(timeout)

           # Nếu có nhiều timer file descriptor sẵn sàng để đọc cùng lúc,
           # epoll.poll() trả về một danh sách các cặp (fd, event).
           #
           # Trong thiết lập của ví dụ này,
           #    timer thứ nhất kích hoạt sau mỗi 0.25 giây. (0.25, 0.5, 0.75, 1.0, ...)
           #    timer thứ hai kích hoạt sau mỗi 0.5 giây. (0.5, 1.0, 1.5, 2.0, ...)
           #    Bộ hẹn giờ thứ 3 sau mỗi 0.75 giây, bắt đầu từ 0.75 giây. (0.75, 1.5, 2.25, 3.0, ...)
           #
           #    Sau 0.25 giây, chỉ bộ hẹn giờ thứ 1 kích hoạt.
           #    Sau 0.5 giây, bộ hẹn giờ thứ 1 và thứ 2 kích hoạt đồng thời.
           #    Sau 0.75 giây, bộ hẹn giờ thứ 1 và thứ 3 kích hoạt đồng thời.
           #    Sau 1.5 giây, bộ hẹn giờ thứ 1, thứ 2 và thứ 3 kích hoạt đồng thời.
           #
           # Nếu một bộ mô tả tệp của bộ hẹn giờ được báo hiệu nhiều hơn một lần kể từ
           # lần gọi os.read() gần nhất, os.read() trả về số lần được báo hiệu
           # theo thứ tự byte của máy chủ đối với các byte lớp.
           print(f"Signaled events={events}")
           for fd, event in events:
               if event & select.EPOLLIN:
                   if fd == sock.fileno():
                       # Kiểm tra xem có yêu cầu kết nối hay không.
                       print(f"Accepting connection {fd}")
                       conn, addr = sock.accept()
                       conn.setblocking(False)
                       print(f"Accepted connection {conn} from {addr}")
                       ep.register(conn, select.EPOLLIN)
                   elif conn and fd == conn.fileno():
                       # Kiểm tra xem có dữ liệu để đọc hay không.
                       print(f"Reading data {fd}")
                       data = conn.recv(1024)
                       if data:
                           # Bạn nên bắt ngoại lệ UnicodeDecodeError để đảm bảo an toàn.
                           cmd = data.decode()
                           if cmd.startswith("stop"):
                               print(f"Stopping server")
                               is_active = False
                           else:
                               print(f"Unknown command: {cmd}")
                       else:
                           # Không còn dữ liệu, đóng kết nối
                           print(f"Closing connection {fd}")
                           ep.unregister(conn)
                           conn.close()
                           conn = None
                   elif fd in fds:
                       print(f"Reading timer {fd}")
                       count = int.from_bytes(os.read(fd, 8), byteorder=sys.byteorder)
                       print(f"Timer {fds.index(fd) + 1} expired {count} times")
                   else:
                       print(f"Unknown file descriptor {fd}")
   finally:
       for fd in fds:
           ep.unregister(fd)
           os.close(fd)
       ep.close()

Ví dụ này cho thấy cách :func:`~select.select` có thể được sử dụng với các bộ mô tả tệp hẹn giờ để chờ cho đến khi bộ mô tả tệp sẵn sàng để đọc:

.. code-block:: python

   import os, time, select, socket, sys

   # Trong ví dụ này, sử dụng địa chỉ loopback để gửi lệnh "stop" đến server.
   #
   # $ telnet 127.0.0.1 1234
   # Đang thử 127.0.0.1...
   # Đã kết nối với 127.0.0.1.
   # Ký tự thoát là '^]'.
   # stop
   # Kết nối đã bị máy chủ từ xa đóng.
   #
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.bind(("127.0.0.1", 1234))
   sock.setblocking(False)
   sock.listen(1)

   # Tạo các file descriptor của timer ở chế độ không chặn.
   num = 3
   fds = [os.timerfd_create(time.CLOCK_REALTIME, flags=os.TFD_NONBLOCK)
          for _ in range(num)]
   select_fds = fds + [sock]

   # Khởi động các bộ hẹn giờ bằng os.timerfd_settime() theo đơn vị giây.
   # Timer 1 kích hoạt mỗi 0.25 giây; timer 2 mỗi 0.5 giây; v.v.
   for i, fd in enumerate(fds, start=1):
      os.timerfd_settime(fd, initial=i/4, interval=i/4)

   timeout = 3
   try:
       conn = None
       is_active = True
       while is_active:
          # Chờ timer hết hạn trong 3 giây.
          # select.select() trả về một danh sách các bộ mô tả tệp hoặc đối tượng.
          rfd, wfd, xfd = select.select(select_fds, select_fds, select_fds, timeout)
          for fd in rfd:
              if fd == sock:
                  # Kiểm tra xem có yêu cầu kết nối hay không.
                  print(f"Accepting connection {fd}")
                  conn, addr = sock.accept()
                  conn.setblocking(False)
                  print(f"Accepted connection {conn} from {addr}")
                  select_fds.append(conn)
              elif conn and fd == conn:
                  # Kiểm tra xem có dữ liệu để đọc hay không.
                  print(f"Reading data {fd}")
                  data = conn.recv(1024)
                  if data:
                      # Bạn nên bắt ngoại lệ UnicodeDecodeError để đảm bảo an toàn.
                      cmd = data.decode()
                      if cmd.startswith("stop"):
                          print(f"Stopping server")
                          is_active = False
                      else:
                          print(f"Unknown command: {cmd}")
                  else:
                      # Không còn dữ liệu, đóng kết nối
                      print(f"Closing connection {fd}")
                      select_fds.remove(conn)
                      conn.close()
                      conn = None
              elif fd in fds:
                  print(f"Reading timer {fd}")
                  count = int.from_bytes(os.read(fd, 8), byteorder=sys.byteorder)
                  print(f"Timer {fds.index(fd) + 1} expired {count} times")
              else:
                  print(f"Unknown file descriptor {fd}")
   finally:
       for fd in fds:
          os.close(fd)
       sock.close()
       sock = None

