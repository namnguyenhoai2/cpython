.. _socket-howto:

**************************
HƯỚNG DẪN LẬP TRÌNH SOCKET
**************************

:Author: Gordon McMillan


.. topic:: Tóm tắt

   Socket được sử dụng gần như ở mọi nơi, nhưng lại là một trong những công nghệ thường bị hiểu sai nghiêm trọng nhất. Đây là phần tổng quan ở mức rất cao về socket. Nội dung này không thực sự là một tutorial - bạn vẫn sẽ phải tự thực hiện một số công việc để đưa mọi thứ vào hoạt động. Tài liệu không đề cập đến các chi tiết nhỏ (và có rất nhiều chi tiết như vậy), nhưng tôi hy vọng nó sẽ cung cấp đủ kiến thức nền tảng để bạn bắt đầu sử dụng socket một cách hiệu quả.


Socket
======

Tôi chỉ nói về socket INET (tức IPv4), nhưng chúng chiếm ít nhất 99% số socket đang được sử dụng. Tôi cũng chỉ nói về socket STREAM (tức TCP) - trừ khi bạn thực sự biết mình đang làm gì (trong trường hợp đó, HOWTO này không dành cho bạn!), bạn sẽ nhận được hành vi và hiệu năng tốt hơn từ socket STREAM so với bất kỳ loại nào khác. Tôi sẽ cố gắng giải thích rõ socket là gì, đồng thời đưa ra một số gợi ý về cách làm việc với socket blocking và non-blocking. Tuy nhiên, tôi sẽ bắt đầu bằng việc nói về socket blocking. Bạn cần biết cách chúng hoạt động trước khi xử lý socket non-blocking.

Một phần nguyên nhân khiến những khái niệm này khó hiểu là "socket" có thể mang một số ý nghĩa hơi khác nhau tùy theo ngữ cảnh. Vì vậy, trước tiên hãy phân biệt giữa socket "client" - một endpoint của cuộc hội thoại - và socket "server", vốn giống một tổng đài viên hơn. Ứng dụng client (chẳng hạn như trình duyệt của bạn) chỉ sử dụng socket "client"; còn web server mà ứng dụng đó giao tiếp cùng sử dụng cả socket "server" lẫn socket "client".


Lịch sử
-------

Trong số nhiều dạng :abbr:`IPC (Giao tiếp giữa các tiến trình)`, socket là dạng phổ biến nhất. Trên bất kỳ nền tảng nào, có thể còn có những dạng IPC khác nhanh hơn, nhưng để giao tiếp đa nền tảng, socket gần như là lựa chọn duy nhất.

Socket được phát minh tại Berkeley trong BSD, một biến thể của Unix. Chúng lan rộng nhanh chóng cùng với Internet. Điều đó hoàn toàn có lý do --- sự kết hợp giữa socket và INET giúp việc giao tiếp với các máy tùy ý trên khắp thế giới trở nên dễ dàng đến khó tin (ít nhất là so với các phương thức khác).


Tạo một Socket
==============

Nói một cách khái quát, khi bạn nhấp vào liên kết đưa bạn đến trang này, trình duyệt của bạn đã thực hiện điều gì đó tương tự như sau::

   # tạo một socket INET, STREAMing
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # bây giờ kết nối với máy chủ web trên cổng 80 - cổng http thông thường
   s.connect(("www.python.org", 80))

Khi ``connect`` hoàn tất, socket ``s`` có thể được dùng để gửi yêu cầu lấy nội dung của trang. Chính socket đó sẽ đọc phản hồi rồi bị hủy. Đúng vậy, bị hủy. Client socket thường chỉ được dùng cho một lần trao đổi (hoặc một số ít lần trao đổi tuần tự).

Những gì diễn ra trên web server phức tạp hơn một chút. Trước tiên, web server tạo một "server socket"::

   # tạo một socket INET, STREAMing
   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # bind socket với một host công khai và một cổng được biết đến rộng rãi
   serversocket.bind((socket.gethostname(), 80))
   # trở thành một server socket
   serversocket.listen(5)

Có một vài điều cần lưu ý: chúng ta đã dùng ``socket.gethostname()`` để socket có thể được nhìn thấy từ bên ngoài. Nếu dùng ``s.bind(('localhost', 80))`` hoặc ``s.bind(('127.0.0.1', 80))``, chúng ta vẫn có một socket "server", nhưng socket đó chỉ hiển thị trong cùng một máy. ``s.bind(('', 80))`` chỉ ra rằng socket có thể được truy cập bằng bất kỳ địa chỉ nào mà máy đang có.

Điều thứ hai cần lưu ý: các cổng có số nhỏ thường được dành cho những dịch vụ "được biết đến rộng rãi" (HTTP, SNMP, v.v.). Nếu bạn đang thử nghiệm, hãy dùng một số lớn dễ nhớ (4 chữ số).

Cuối cùng, đối số truyền cho ``listen`` cho thư viện socket biết rằng chúng ta muốn nó xếp hàng tối đa 5 yêu cầu kết nối (mức tối đa thông thường) trước khi từ chối các kết nối bên ngoài. Nếu phần còn lại của mã được viết đúng cách thì như vậy là đủ.

Bây giờ, khi đã có một socket "server" đang lắng nghe trên cổng 80, chúng ta có thể进入 vòng lặp chính của web server::

   while True:
       # chấp nhận các kết nối từ bên ngoài
       (clientsocket, address) = serversocket.accept()
       # bây giờ làm gì đó với clientsocket
       # trong trường hợp này, chúng ta sẽ giả định đây là một threaded server
       ct = make_client_thread(clientsocket)
       ct.start()

Thực tế có 3 cách tổng quát để vòng lặp này hoạt động - phân công một thread để xử lý ``clientsocket``, tạo một process mới để xử lý ``clientsocket``, hoặc tái cấu trúc ứng dụng này để sử dụng các socket không chặn và multiplex giữa socket "server" của chúng ta với bất kỳ ``clientsocket``\ s nào đang hoạt động bằng cách sử dụng ``select``. Chúng ta sẽ tìm hiểu thêm về việc đó sau. Điều quan trọng cần hiểu lúc này là: đây là *tất cả* những gì một socket "server" thực hiện. Nó không gửi dữ liệu. Nó không nhận dữ liệu. Nó chỉ tạo ra các socket "client". Mỗi ``clientsocket`` được tạo ra để đáp lại việc một socket "client" *khác* nào đó thực hiện ``connect()`` tới host và cổng mà chúng ta đã bind. Ngay khi tạo ``clientsocket`` đó, chúng ta quay lại lắng nghe các kết nối khác. Hai "client" được tự do trò chuyện với nhau - chúng sử dụng một cổng được cấp phát động và cổng này sẽ được tái sử dụng khi cuộc trò chuyện kết thúc.


IPC
---

Nếu bạn cần IPC nhanh giữa hai tiến trình trên cùng một máy, bạn nên xem xét pipes hoặc shared memory. Nếu vẫn quyết định sử dụng socket AF_INET, hãy bind socket "server" vào ``'localhost'``. Trên hầu hết các nền tảng, cách này sẽ bỏ qua một vài tầng mã mạng và nhanh hơn đáng kể.

.. seealso::
   :mod:`multiprocessing` tích hợp IPC đa nền tảng vào một API cấp cao hơn.


Sử dụng socket
==============

Điều đầu tiên cần lưu ý là socket "client" của trình duyệt web và socket "client" của web server thực chất giống hệt nhau. Nói cách khác, đây là một cuộc trò chuyện "peer to peer". Hay nói theo cách khác, *với tư cách là người thiết kế, bạn sẽ phải quyết định các quy tắc ứng xử cho một cuộc trò chuyện*. Thông thường, socket ``connect``\ ing sẽ bắt đầu cuộc trò chuyện bằng cách gửi một request hoặc có thể là một signon. Nhưng đó là một quyết định thiết kế, không phải quy tắc của socket.

Giờ đây có hai nhóm động từ để sử dụng khi giao tiếp. Bạn có thể sử dụng ``send`` và ``recv``, hoặc biến socket client thành một đối tượng giống file và sử dụng ``read`` và ``write``. Đây là cách Java cung cấp socket. Tôi sẽ không trình bày cách này ở đây, ngoại trừ việc cảnh báo rằng bạn cần sử dụng ``flush`` trên socket. Đây là các "file" được buffer, và một lỗi phổ biến là ``write`` một thứ gì đó rồi ``read`` để chờ phản hồi. Nếu không có ``flush`` ở đó, bạn có thể phải chờ phản hồi mãi mãi, vì request có thể vẫn còn trong output buffer.

Giờ chúng ta đến với trở ngại lớn nhất của socket: ``send`` và ``recv`` hoạt động trên các network buffer. Chúng không nhất thiết xử lý tất cả các byte mà bạn đưa cho chúng (hoặc mong đợi nhận được từ chúng), vì trọng tâm chính của chúng là xử lý các network buffer. Nhìn chung, chúng trả về khi các network buffer liên quan đã được lấp đầy (``send``) hoặc làm rỗng (``recv``). Sau đó, chúng cho bạn biết đã xử lý bao nhiêu byte. *chính bạn* có trách nhiệm gọi lại chúng cho đến khi message của bạn được xử lý hoàn toàn.

Khi một ``recv`` trả về 0 byte, điều đó có nghĩa là phía bên kia đã đóng (hoặc đang trong quá trình đóng) connection. Bạn sẽ không bao giờ nhận thêm dữ liệu nào trên connection này nữa. Bạn vẫn có thể gửi dữ liệu thành công; tôi sẽ nói thêm về điều này sau.

Một giao thức như HTTP chỉ sử dụng socket cho một lần truyền. Client gửi một request, sau đó đọc phản hồi. Chỉ vậy thôi. Socket bị loại bỏ. Điều này có nghĩa là client có thể phát hiện phần cuối của phản hồi bằng cách nhận 0 byte.

Nhưng nếu bạn dự định tái sử dụng socket cho các lần truyền tiếp theo, bạn cần nhận ra rằng *không có* :abbr:`EOT (Kết thúc truyền)` *trên socket.* Tôi nhắc lại: nếu một socket ``send`` hoặc ``recv`` trả về sau khi xử lý 0 byte, kết nối đã bị ngắt. Nếu kết nối *chưa* bị ngắt, bạn có thể chờ trên một ``recv`` mãi mãi, vì socket sẽ *không* cho bạn biết rằng hiện không còn gì để đọc. Bây giờ, nếu suy nghĩ kỹ một chút, bạn sẽ nhận ra một sự thật cơ bản về socket: *message phải có độ dài cố định* (chán), *hoặc phải được phân cách* (đành chịu), *hoặc phải cho biết độ dài của chúng* (tốt hơn nhiều), *hoặc kết thúc bằng cách đóng kết nối*. Lựa chọn hoàn toàn thuộc về bạn (nhưng một số cách đúng đắn hơn những cách khác).

Giả sử bạn không muốn kết thúc kết nối, giải pháp đơn giản nhất là một message có độ dài cố định::

   class MySocket:
       """demonstration class only
         - coded for clarity, not efficiency
       """

       def __init__(self, sock=None):
           if sock is None:
               self.sock = socket.socket(
                               socket.AF_INET, socket.SOCK_STREAM)
           else:
               self.sock = sock

       def connect(self, host, port):
           self.sock.connect((host, port))

       def mysend(self, msg):
           totalsent = 0
           while totalsent < MSGLEN:
               sent = self.sock.send(msg[totalsent:])
               if sent == 0:
                   raise RuntimeError("socket connection broken")
               totalsent = totalsent + sent

       def myreceive(self):
           chunks = []
           bytes_recd = 0
           while bytes_recd < MSGLEN:
               chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
               if chunk == b'':
                   raise RuntimeError("socket connection broken")
               chunks.append(chunk)
               bytes_recd = bytes_recd + len(chunk)
           return b''.join(chunks)

Code gửi ở đây có thể dùng cho hầu hết mọi cơ chế messaging - trong Python, bạn gửi các string và có thể dùng ``len()`` để xác định độ dài của chúng (ngay cả khi chúng chứa các ký tự ``\0``). Chủ yếu chính code nhận mới trở nên phức tạp hơn. (Và trong C, mọi thứ cũng không tệ hơn nhiều, ngoại trừ việc bạn không thể dùng ``strlen`` nếu message chứa các ``\0``\ s.)

Một cải tiến đơn giản nhất là biến ký tự đầu tiên của message thành chỉ báo về loại message và để loại đó quyết định độ dài. Bây giờ bạn có hai ``recv``\ s - lần đầu để lấy ít nhất ký tự đầu tiên, nhờ đó bạn có thể tra cứu độ dài, và lần thứ hai trong một vòng lặp để lấy phần còn lại. Nếu quyết định chọn cách phân cách, bạn sẽ nhận dữ liệu theo một kích thước chunk tùy ý nào đó (4096 hoặc 8192 thường phù hợp với kích thước bộ đệm mạng), rồi quét phần đã nhận để tìm dấu phân cách.

Một điều phức tạp cần lưu ý: nếu conversational protocol của bạn cho phép gửi nhiều message liên tiếp (mà không cần một dạng reply nào đó), và bạn truyền cho ``recv`` một kích thước chunk tùy ý, bạn có thể đọc luôn phần bắt đầu của message tiếp theo. Bạn sẽ cần tách phần đó ra và giữ lại cho đến khi cần dùng.

Thêm độ dài của message vào đầu (chẳng hạn dưới dạng 5 ký tự số) khiến mọi thứ phức tạp hơn, vì (tin hay không tùy bạn), bạn có thể không nhận được cả 5 ký tự trong một ``recv``. Khi thử nghiệm, bạn có thể sẽ không gặp vấn đề; nhưng khi tải mạng cao, code của bạn sẽ nhanh chóng bị lỗi trừ khi bạn dùng hai vòng lặp ``recv`` - vòng đầu để xác định độ dài, vòng thứ hai để lấy phần dữ liệu của message. Rắc rối thật. Đây cũng là lúc bạn phát hiện rằng ``send`` không phải lúc nào cũng xử lý được mọi thứ chỉ trong một lần. Và dù đã đọc điều này, cuối cùng bạn vẫn sẽ bị nó làm cho khốn đốn!

Để tiết kiệm không gian, xây dựng nhân vật (và duy trì lợi thế cạnh tranh của tôi), những cải tiến này được để lại như một bài tập dành cho người đọc. Hãy chuyển sang việc dọn dẹp.


Dữ liệu nhị phân
----------------

Hoàn toàn có thể gửi dữ liệu nhị phân qua socket. Vấn đề chính là không phải máy nào cũng sử dụng cùng một định dạng cho dữ liệu nhị phân. Ví dụ, `thứ tự byte mạng <https://en.wikipedia.org/wiki/Endianness#Networking>`_ là big-endian, với byte có ý nghĩa lớn nhất nằm trước, vì vậy một số nguyên 16 bit có giá trị ``1`` sẽ là hai byte hex ``00 01``. Tuy nhiên, hầu hết các bộ xử lý phổ biến (x86/AMD64, ARM, RISC-V) đều là little-endian, với byte có ý nghĩa nhỏ nhất nằm trước - cùng ``1`` đó sẽ là ``01 00``.

Các thư viện socket có các lệnh gọi để chuyển đổi số nguyên 16 và 32 bit - ``ntohl, htonl, ntohs, htons`` trong đó "n" nghĩa là *mạng* và "h" nghĩa là *máy chủ*, "s" nghĩa là *short* và "l" nghĩa là *long*. Khi thứ tự mạng trùng với thứ tự máy chủ, các lệnh này không làm gì cả, nhưng khi máy sử dụng thứ tự byte đảo ngược, chúng sẽ hoán đổi các byte cho phù hợp.

Trong thời đại máy 64 bit hiện nay, biểu diễn ASCII của dữ liệu nhị phân thường nhỏ hơn biểu diễn nhị phân. Đó là vì đáng ngạc nhiên là phần lớn thời gian, hầu hết các số nguyên đều có giá trị 0, hoặc có thể là 1. Chuỗi ``"0"`` sẽ chiếm hai byte, trong khi một số nguyên 64 bit đầy đủ sẽ chiếm 8 byte. Tất nhiên, cách này không phù hợp lắm với các thông báo có độ dài cố định. Thật khó lựa chọn.


Ngắt kết nối
============

Nói chính xác, bạn phải sử dụng ``shutdown`` trên một socket trước khi ``close`` nó. ``shutdown`` là một thông báo mang tính khuyến cáo gửi đến socket ở đầu bên kia. Tùy thuộc vào đối số bạn truyền cho nó, điều này có thể có nghĩa là "Tôi sẽ không gửi thêm nữa, nhưng vẫn sẽ lắng nghe", hoặc "Tôi không lắng nghe, đi cho khuất mắt!". Tuy nhiên, hầu hết các thư viện socket đều đã quá quen với việc lập trình viên bỏ qua phép lịch sự này, nên thông thường ``close`` cũng giống như ``shutdown(); close()``. Vì vậy, trong hầu hết tình huống, không cần ``shutdown`` tường minh.

Một cách sử dụng ``shutdown`` hiệu quả là trong một cuộc trao đổi giống HTTP. Client gửi một request rồi thực hiện ``shutdown(1)``. Điều này cho server biết: "Client này đã gửi xong, nhưng vẫn có thể nhận dữ liệu." Server có thể phát hiện "EOF" khi nhận được 0 byte. Server có thể giả định rằng mình đã nhận đủ request. Server gửi phản hồi. Nếu ``send`` hoàn tất thành công thì quả thực client vẫn đang nhận dữ liệu.

Python tiến thêm một bước với việc tự động tắt kết nối và cho biết rằng khi một socket được garbage collect, nó sẽ tự động thực hiện ``close`` nếu cần. Tuy nhiên, dựa vào cơ chế này là một thói quen rất tệ. Nếu socket của bạn biến mất mà không thực hiện ``close``, socket ở đầu bên kia có thể bị treo vô thời hạn vì nghĩ rằng bạn chỉ đang xử lý chậm. *Vui lòng* ``close`` đóng các socket khi bạn dùng xong.


Khi Socket Bị Ngắt
------------------

Có lẽ điều tệ nhất khi sử dụng socket blocking là chuyện xảy ra khi phía bên kia bị ngắt đột ngột (mà không thực hiện ``close``). Socket của bạn nhiều khả năng sẽ bị treo. TCP là một giao thức đáng tin cậy và sẽ chờ rất lâu trước khi từ bỏ một kết nối. Nếu bạn sử dụng thread, toàn bộ thread về cơ bản đã chết. Bạn không thể làm được nhiều điều để khắc phục. Miễn là bạn không làm điều ngớ ngẩn, chẳng hạn như giữ một lock trong khi thực hiện thao tác đọc blocking, thread thực sự không tiêu tốn nhiều tài nguyên. Bạn *không* được cố giết thread — một phần lý do thread hiệu quả hơn process là vì chúng tránh được overhead liên quan đến việc tự động tái chế tài nguyên. Nói cách khác, nếu bạn thực sự giết được thread, rất có thể toàn bộ process của bạn sẽ bị hỏng.


Socket Non-blocking
===================

Nếu bạn đã hiểu phần trước, thì bạn đã biết gần hết những gì cần biết về cơ chế sử dụng socket. Bạn vẫn sẽ dùng những lời gọi tương tự, theo những cách gần như tương tự. Chỉ là nếu thực hiện đúng, ứng dụng của bạn sẽ gần như bị đảo ngược từ trong ra ngoài.

Trong Python, bạn dùng ``socket.setblocking(False)`` để chuyển nó sang chế độ non-blocking. Trong C, việc này phức tạp hơn (trước hết, bạn sẽ cần chọn giữa biến thể BSD ``O_NONBLOCK`` và biến thể POSIX gần như không thể phân biệt ``O_NDELAY``, vốn hoàn toàn khác với ``TCP_NODELAY``), nhưng ý tưởng hoàn toàn giống nhau. Bạn thực hiện việc này sau khi tạo socket nhưng trước khi sử dụng nó. (Thực ra, nếu bạn muốn, bạn có thể chuyển đổi qua lại.)

Khác biệt cơ bản về mặt cơ chế là ``send``, ``recv``, ``connect`` và ``accept`` có thể trả về mà chưa thực hiện được gì. Bạn (tất nhiên) có một số lựa chọn. Bạn có thể kiểm tra mã trả về và các mã lỗi rồi tự làm mình phát điên. Nếu không tin tôi, hãy thử một lần. Ứng dụng của bạn sẽ trở nên lớn, nhiều lỗi và ngốn CPU. Vì vậy, hãy bỏ qua những giải pháp ngớ ngẩn và làm cho đúng cách.

Hãy sử dụng ``select``.

Trong C, việc lập trình ``select`` khá phức tạp. Trong Python, việc này dễ như ăn bánh, nhưng khá giống với phiên bản C, nên nếu bạn hiểu ``select`` trong Python thì sẽ không gặp nhiều khó khăn khi làm việc đó trong C::

   ready_to_read, ready_to_write, in_error = \
                  select.select(
                     potential_readers,
                     potential_writers,
                     potential_errs,
                     timeout)

Bạn truyền cho ``select`` ba danh sách: danh sách đầu tiên chứa tất cả các socket mà bạn có thể muốn thử đọc; danh sách thứ hai chứa tất cả các socket mà bạn có thể muốn thử ghi vào; danh sách cuối cùng (thường để trống) chứa những socket mà bạn muốn kiểm tra lỗi. Lưu ý rằng một socket có thể nằm trong nhiều hơn một danh sách. Lệnh gọi ``select`` có tính blocking, nhưng bạn có thể cung cấp thời gian chờ. Nhìn chung, đây là việc hợp lý - hãy đặt thời gian chờ đủ dài (chẳng hạn một phút), trừ khi bạn có lý do chính đáng để làm khác.

Đổi lại, bạn sẽ nhận được ba danh sách. Chúng chứa các socket thực sự có thể đọc, có thể ghi và đang ở trạng thái lỗi. Mỗi danh sách trong số này là một tập con (có thể rỗng) của danh sách tương ứng mà bạn đã truyền vào.

Nếu một socket nằm trong danh sách đầu ra có thể đọc, bạn có thể gần như chắc chắn tuyệt đối rằng một ``recv`` trên socket đó sẽ trả về *một điều gì đó*. Ý tưởng tương tự cũng áp dụng cho danh sách có thể ghi. Bạn sẽ có thể gửi *một điều gì đó*. Có thể không phải tất cả những gì bạn muốn gửi, nhưng *một điều gì đó* vẫn tốt hơn là không có gì.  (Thực ra, bất kỳ socket nào tương đối khỏe mạnh cũng sẽ được trả về trong danh sách có thể ghi - điều đó chỉ có nghĩa là vẫn còn chỗ trống trong bộ đệm mạng gửi đi.)

Nếu bạn có một socket "server", hãy đặt nó vào danh sách potential_readers. Nếu nó xuất hiện trong danh sách có thể đọc, ``accept`` của bạn (gần như chắc chắn) sẽ hoạt động. Nếu bạn đã tạo một socket mới để ``connect`` với một đối tượng khác, hãy đặt nó vào danh sách potential_writers. Nếu nó xuất hiện trong danh sách có thể ghi, có khả năng khá cao là nó đã kết nối.

Thực ra, ``select`` có thể hữu ích ngay cả với socket blocking. Đây là một cách để xác định liệu bạn có bị block hay không - socket trả về trạng thái có thể đọc khi có dữ liệu trong các bộ đệm. Tuy nhiên, điều này vẫn không giải quyết được vấn đề xác định xem đầu bên kia đã hoàn tất hay chỉ đang bận xử lý việc khác.

**Cảnh báo về tính khả chuyển**: Trên Unix, ``select`` hoạt động cả với socket lẫn tệp. Đừng thử cách này trên Windows. Trên Windows, ``select`` chỉ hoạt động với socket. Cũng lưu ý rằng trong C, nhiều tùy chọn socket nâng cao được thực hiện theo cách khác trên Windows. Trên thực tế, với socket của mình, tôi thường sử dụng thread (hoạt động rất, rất tốt).

.. _`network byte order`: https://en.wikipedia.org/wiki/Endianness#Networking
