:mod:`!contextvars` --- Biến ngữ cảnh
=====================================

.. module:: contextvars
   :synopsis: Biến ngữ cảnh

.. sectionauthor:: Yury Selivanov <yury@magic.io>

--------------

Mô-đun này cung cấp các API để quản lý, lưu trữ và truy cập trạng thái cục bộ theo ngữ cảnh. Lớp :class:`~contextvars.ContextVar` được dùng để khai báo và làm việc với *Biến ngữ cảnh*. Hàm :func:`~contextvars.copy_context` và lớp :class:`~contextvars.Context` nên được dùng để quản lý ngữ cảnh hiện tại trong các framework bất đồng bộ.

Các context manager có trạng thái nên sử dụng Biến ngữ cảnh thay vì :func:`threading.local` để ngăn trạng thái của chúng vô tình lan sang mã khác khi được sử dụng trong mã chạy đồng thời.

Xem thêm :pep:`567` để biết thêm chi tiết.

.. versionadded:: 3.7


Biến ngữ cảnh
-------------

.. class:: ContextVar(name, [*, default])

   Lớp này được dùng để khai báo một Biến ngữ cảnh mới, chẳng hạn như::

       var: ContextVar[int] = ContextVar('var', default=42)

   Tham số bắt buộc *name* được sử dụng cho mục đích introspection và debug.

   Tham số chỉ nhận từ khóa tùy chọn *default* được trả về bởi
   :meth:`ContextVar.get` khi không tìm thấy giá trị nào cho biến trong context hiện tại.

   **Lưu ý:** Context Variables nên được tạo ở cấp module cao nhất và không bao giờ nằm trong các closure. :class:`Context` object giữ các tham chiếu mạnh đến context variables, ngăn không cho context variables được garbage collection đúng cách.

   :class:`!ContextVar`\s là :ref:`generic <generics>` theo kiểu của giá trị mà chúng chứa.

   .. attribute:: ContextVar.name

      Tên của biến. Đây là thuộc tính chỉ đọc.

      .. versionadded:: 3.7.1

   .. method:: get([default])

      Trả về một giá trị cho context variable trong context hiện tại.

      Nếu không có giá trị cho biến trong context hiện tại, phương thức sẽ:

      * trả về giá trị của đối số *default* của phương thức, nếu được cung cấp; hoặc

      * trả về giá trị mặc định của biến context, nếu biến được tạo cùng một giá trị mặc định; hoặc

      * phát sinh một :exc:`LookupError`.

   .. method:: set(value)

      Gọi phương thức này để đặt giá trị mới cho biến context trong context hiện tại.

      Đối số bắt buộc *value* là giá trị mới của biến context.

      Trả về một đối tượng :class:`~contextvars.Token` có thể được sử dụng để khôi phục biến về giá trị trước đó thông qua
      :meth:`ContextVar.reset` phương thức.

      Để thuận tiện, đối tượng token có thể được sử dụng như một context manager để tránh phải gọi :meth:`ContextVar.reset` theo cách thủ công::

          var = ContextVar('var', default='default value')

          with var.set('new value'):
              assert var.get() == 'new value'

          assert var.get() == 'default value'

      Đây là cách viết rút gọn cho::

          var = ContextVar('var', default='default value')

          token = var.set('new value')
          try:
              assert var.get() == 'new value'
          finally:
              var.reset(token)

          assert var.get() == 'default value'

      .. versionadded:: 3.14

         Đã thêm hỗ trợ sử dụng token làm context manager.

   .. method:: reset(token)

      Đặt lại biến ngữ cảnh về giá trị mà nó có trước khi
      Phương thức :meth:`ContextVar.set` đã tạo *token* đã được sử dụng.

      Ví dụ::

          var = ContextVar('var')

          token = var.set('new value')
          # mã sử dụng 'var'; var.get() trả về 'new value'.
          var.reset(token)

          # Sau lệnh gọi reset, var lại không có giá trị, vì vậy
          # var.get() sẽ phát sinh LookupError.

      Không thể sử dụng cùng một *token* hai lần.


.. class:: Token

   Các đối tượng *Token* được trả về bởi phương thức :meth:`ContextVar.set` . Chúng có thể được truyền vào phương thức :meth:`ContextVar.reset` để khôi phục giá trị của biến về trạng thái trước thao tác *set* tương ứng. Một token không thể đặt lại một biến ngữ cảnh nhiều hơn một lần.

   Các token hỗ trợ :ref:`giao thức context manager <context-managers>` để tự động đặt lại các biến ngữ cảnh. Xem :meth:`ContextVar.set`.

   Các token là :ref:`generic <generics>` trên cùng kiểu với
   :class:`ContextVar` đã tạo ra chúng.

   .. versionadded:: 3.14

      Đã bổ sung hỗ trợ sử dụng dưới dạng context manager.

   .. attribute:: Token.var

      Một thuộc tính chỉ đọc. Trỏ đến đối tượng :class:`ContextVar` đã tạo token.

   .. attribute:: Token.old_value

      Một thuộc tính chỉ đọc. Được đặt thành giá trị mà biến có trước lần gọi phương thức :meth:`ContextVar.set` đã tạo token. Trỏ đến :attr:`Token.MISSING` nếu biến chưa được đặt trước lần gọi đó.

   .. attribute:: Token.MISSING

      Một đối tượng đánh dấu được :attr:`Token.old_value` sử dụng.


Quản lý Context thủ công
------------------------

.. function:: copy_context()

   Trả về một bản sao của đối tượng :class:`~contextvars.Context` hiện tại.

   Đoạn mã sau lấy một bản sao của context hiện tại và in tất cả các biến cùng giá trị của chúng đang được thiết lập trong đó::

      ctx: Context = copy_context()
      print(list(ctx.items()))

   Hàm này có độ phức tạp *O*\ (1), nghĩa là hoạt động nhanh như nhau đối với các context có ít biến context và các context có nhiều biến context.


.. class:: Context()

   Một ánh xạ từ :class:`ContextVars <ContextVar>` đến các giá trị tương ứng của chúng.

   ``Context()`` tạo một context trống không chứa giá trị nào. Để lấy một bản sao của context hiện tại, hãy sử dụng
   hàm :func:`~contextvars.copy_context`.

   Mỗi thread có một stack hiệu dụng riêng gồm các đối tượng :class:`!Context`.
   :term:`current context` là đối tượng :class:`!Context` ở trên cùng của stack thuộc thread hiện tại.  Tất cả các đối tượng :class:`!Context` trong các stack đều được xem là đã *entered*.

   *Việc đi vào* một context, có thể thực hiện bằng cách gọi phương thức :meth:`~Context.run` của context đó, khiến context trở thành context hiện tại bằng cách đẩy nó lên đầu ngăn xếp context của thread hiện tại.

   *Việc thoát* khỏi context hiện tại, có thể thực hiện bằng cách trả về từ callback được truyền cho phương thức :meth:`~Context.run`, sẽ khôi phục context hiện tại về trạng thái trước khi đi vào context bằng cách lấy context ra khỏi đầu ngăn xếp context.

   Vì mỗi thread có ngăn xếp context riêng, các đối tượng :class:`ContextVar` hoạt động tương tự như :func:`threading.local` khi các giá trị được gán trong các thread khác nhau.

   Việc cố gắng đi vào một context đã được đi vào, bao gồm cả các context được đi vào trong những thread khác, sẽ gây ra :exc:`RuntimeError`.

   Sau khi thoát khỏi một context, bạn có thể đi vào lại context đó sau này (từ bất kỳ thread nào).

   Mọi thay đổi đối với các giá trị :class:`ContextVar` thông qua phương thức :meth:`ContextVar.set` đều được ghi nhận trong context hiện tại. Phương thức :meth:`ContextVar.get` trả về giá trị được liên kết với context hiện tại. Việc thoát khỏi một context về cơ bản sẽ hoàn nguyên mọi thay đổi được thực hiện đối với các biến context trong khi context đang được đi vào (nếu cần, có thể khôi phục các giá trị bằng cách đi vào lại context).

   Context triển khai interface :class:`collections.abc.Mapping`.

   .. method:: run(callable, *args, **kwargs)

      Đi vào Context, thực thi ``callable(*args, **kwargs)``, sau đó thoát khỏi Context. Trả về giá trị trả về của *callable*, hoặc truyền tiếp một exception nếu có xảy ra.

      Ví dụ:

      .. testcode::

         import contextvars

         var = contextvars.ContextVar('var')
         var.set('spam')
         print(var.get())  # 'spam'

         ctx = contextvars.copy_context()

         def main():
             # 'var' được gán thành 'spam' trước khi
             # gọi 'copy_context()' và 'ctx.run(main)', vì vậy:
             print(var.get())  # 'spam'
             print(ctx[var])  # 'spam'

             var.set('ham')

             # Bây giờ, sau khi đặt 'var' thành 'ham':
             print(var.get())  # 'ham'
             print(ctx[var])  # 'ham'

         # Mọi thay đổi mà hàm 'main' thực hiện đối với 'var'
         # sẽ được chứa trong 'ctx'.
         ctx.run(main)

         # Hàm 'main()' đã được chạy trong ngữ cảnh 'ctx',
         # vì vậy các thay đổi đối với 'var' được chứa trong đó:
         print(ctx[var])  # 'ham'

         # Tuy nhiên, bên ngoài 'ctx', 'var' vẫn có giá trị là 'spam':
         print(var.get())  # 'spam'

      .. testoutput::
         :hide:

         spam
         spam
         spam
         ham
         ham
         ham
         spam

   .. method:: copy()

      Trả về một bản sao nông của đối tượng context.

   .. describe:: var in context

      Trả về ``True`` nếu *context* có giá trị được đặt cho *var*; nếu không, trả về ``False``.

   .. describe:: context[var]

      Trả về giá trị của biến *var* :class:`ContextVar`. Nếu biến không được đặt trong đối tượng context, một
      :exc:`KeyError` sẽ được phát sinh.

   .. method:: get(var, [default])

      Trả về giá trị của *var* nếu *var* có giá trị trong đối tượng context. Nếu không, trả về *default*. Nếu *default* không được cung cấp, trả về ``None``.

   .. describe:: iter(context)

      Trả về một iterator chứa các biến được lưu trữ trong đối tượng context.

   .. describe:: len(proxy)

      Trả về số lượng biến được thiết lập trong đối tượng context.

   .. method:: keys()

      Trả về danh sách tất cả các biến trong đối tượng context.

   .. method:: values()

      Trả về danh sách giá trị của tất cả các biến trong đối tượng context.


   .. method:: items()

      Trả về danh sách các tuple 2 phần tử chứa tất cả các biến và giá trị tương ứng của chúng trong đối tượng context.


Hỗ trợ asyncio
--------------

Các biến ngữ cảnh được hỗ trợ nguyên bản trong :mod:`asyncio` và sẵn sàng được sử dụng mà không cần cấu hình thêm. Ví dụ, sau đây là một echo server đơn giản sử dụng biến ngữ cảnh để cung cấp địa chỉ của client từ xa cho Task xử lý client đó::

    import asyncio
    import contextvars

    client_addr_var = contextvars.ContextVar('client_addr')

    def render_goodbye():
        # Có thể truy cập địa chỉ của client hiện đang được xử lý
        # mà không cần truyền địa chỉ đó một cách tường minh vào hàm này.

        client_addr = client_addr_var.get()
        return f'Good bye, client @ {client_addr}\r\n'.encode()

    async def handle_request(reader, writer):
        addr = writer.transport.get_extra_info('socket').getpeername()
        client_addr_var.set(addr)

        # Trong mọi code mà chúng ta gọi, giờ đây có thể lấy được
        # địa chỉ của client bằng cách gọi 'client_addr_var.get()'.

        while True:
            line = await reader.readline()
            print(line)
            if not line.strip():
                break

        writer.write(b'HTTP/1.1 200 OK\r\n')  # dòng trạng thái
        writer.write(b'\r\n')  # headers
        writer.write(render_goodbye())  # nội dung
        writer.close()

    async def main():
        srv = await asyncio.start_server(
            handle_request, '127.0.0.1', 8081)

        async with srv:
            await srv.serve_forever()

    asyncio.run(main())

    # Để kiểm tra, bạn có thể sử dụng telnet hoặc curl:
    #     telnet 127.0.0.1 8081
    #     curl 127.0.0.1:8081
