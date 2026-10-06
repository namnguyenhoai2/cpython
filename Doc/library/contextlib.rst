:mod:`!contextlib` --- Tiện ích cho các ngữ cảnh của câu lệnh :keyword:`!with`\ -statement
==========================================================================================

.. module:: contextlib
   :synopsis: Các tiện ích cho ngữ cảnh câu lệnh with.

**Mã nguồn:** :source:`Lib/contextlib.py`

--------------

Mô-đun này cung cấp các tiện ích cho những tác vụ phổ biến liên quan đến câu lệnh :keyword:`with`. Để biết thêm thông tin, hãy xem cả :ref:`typecontextmanager` và
:ref:`context-managers`.


Các tiện ích
------------

Các hàm và lớp được cung cấp:

.. class:: AbstractContextManager

   Một :term:`abstract base class` dành cho các lớp triển khai
   :meth:`~object.__enter__` và :meth:`~object.__exit__`. Một triển khai mặc định cho :meth:`~object.__enter__` được cung cấp và trả về ``self``, trong khi :meth:`~object.__exit__` là một phương thức abstract, theo mặc định trả về ``None``. Xem thêm định nghĩa của :ref:`typecontextmanager`.

   .. versionadded:: 3.6


.. class:: AbstractAsyncContextManager

   Một :term:`abstract base class` dành cho các lớp triển khai
   :meth:`~object.__aenter__` và :meth:`~object.__aexit__`. Một triển khai mặc định cho :meth:`~object.__aenter__` được cung cấp và trả về ``self``, trong khi :meth:`~object.__aexit__` là một phương thức abstract, theo mặc định trả về ``None``. Xem thêm định nghĩa của
   :ref:`async-context-managers`.

   .. versionadded:: 3.7


.. decorator:: contextmanager

   Hàm này là một :term:`decorator` có thể được dùng để định nghĩa một factory function cho các context manager của câu lệnh :keyword:`with`, mà không cần tạo một class hoặc các phương thức :meth:`~object.__enter__` và :meth:`~object.__exit__` riêng biệt.

   Mặc dù nhiều đối tượng vốn hỗ trợ việc sử dụng trong các câu lệnh with, đôi khi cần quản lý một tài nguyên không phải là context manager và không triển khai phương thức ``close()`` để sử dụng với ``contextlib.closing``.

   Một ví dụ abstract có thể là đoạn sau để đảm bảo việc quản lý tài nguyên đúng cách::

      from contextlib import contextmanager

      @contextmanager
      def managed_resource(*args, **kwds):
          # Mã để lấy tài nguyên, ví dụ:
          resource = acquire_resource(*args, **kwds)
          try:
              yield resource
          finally:
              # Mã giải phóng tài nguyên, ví dụ:
              release_resource(resource)

   Sau đó có thể sử dụng hàm như sau::

      >>> with managed_resource(timeout=3600) as resource:
      ...     # Tài nguyên được giải phóng ở cuối khối này,
      ...     # ngay cả khi mã trong khối phát sinh ngoại lệ

   Hàm được trang trí phải trả về một :term:`generator`-iterator khi được gọi. Iterator này phải yield chính xác một giá trị, giá trị này sẽ được liên kết với các đích trong mệnh đề :keyword:`with` :keyword:`!as`, nếu có.

   Tại thời điểm generator thực hiện yield, khối được lồng trong câu lệnh :keyword:`with` sẽ được thực thi. Sau đó generator được tiếp tục sau khi thoát khỏi khối. Nếu một ngoại lệ chưa được xử lý xảy ra trong khối, ngoại lệ đó sẽ được phát sinh lại bên trong generator tại vị trí đã thực hiện yield. Do đó, bạn có thể sử dụng một
   :keyword:`try`...\ :keyword:`except`...\ :keyword:`finally` statement để bắt lỗi (nếu có), hoặc bảo đảm rằng một số thao tác dọn dẹp được thực hiện. Nếu một ngoại lệ chỉ được bắt để ghi log hoặc thực hiện một hành động nào đó (thay vì hoàn toàn bỏ qua ngoại lệ), generator phải phát sinh lại ngoại lệ đó. Nếu không, generator context manager sẽ cho câu lệnh :keyword:`!with` biết rằng ngoại lệ đã được xử lý, và quá trình thực thi sẽ tiếp tục với câu lệnh ngay sau câu lệnh :keyword:`!with`.

   :deco:`contextmanager` sử dụng :class:`ContextDecorator` để các context manager mà nó tạo ra có thể được dùng làm decorator cũng như trong các câu lệnh :keyword:`with`. Khi được dùng làm decorator, một instance generator mới được tạo ngầm trong mỗi lần gọi hàm (điều này cho phép các context manager “chỉ dùng một lần” vốn được tạo bởi :deco:`contextmanager` đáp ứng yêu cầu rằng context manager phải hỗ trợ nhiều lần gọi để có thể được dùng làm decorator).

   .. versionchanged:: 3.2
      Cách sử dụng :class:`ContextDecorator`.


.. decorator:: asynccontextmanager

   Tương tự như :deco:`~contextlib.contextmanager`, nhưng tạo ra một
   :ref:`context manager bất đồng bộ <async-context-managers>`.

   Hàm này là một :term:`decorator` có thể được dùng để định nghĩa một hàm factory cho các context manager bất đồng bộ dùng trong câu lệnh :keyword:`async with`, mà không cần tạo một class hoặc :meth:`~object.__aenter__` riêng biệt và
   :meth:`~object.__aexit__` các phương thức. Phải được áp dụng cho một hàm :term:`asynchronous generator`.

   Một ví dụ đơn giản::

      from contextlib import asynccontextmanager

      @asynccontextmanager
      async def get_connection():
          conn = await acquire_db_connection()
          try:
              yield conn
          finally:
              await release_db_connection(conn)

      async def get_all_users():
          async with get_connection() as conn:
              return conn.query('SELECT ...')

   .. versionadded:: 3.7

   Các context manager được định nghĩa bằng :deco:`asynccontextmanager` có thể được sử dụng dưới dạng decorator hoặc với các câu lệnh :keyword:`async with`::

     import time
     from contextlib import asynccontextmanager

     @asynccontextmanager
     async def timeit():
         now = time.monotonic()
         try:
             yield
         finally:
             print(f'it took {time.monotonic() - now}s to run')

     @timeit()
     async def main():
         # ... mã async ...

   Khi được sử dụng dưới dạng decorator, một instance generator mới sẽ được tạo ngầm trong mỗi lần gọi hàm. Điều này cho phép các context manager "one-shot" được tạo bởi :deco:`asynccontextmanager` đáp ứng yêu cầu rằng context manager phải hỗ trợ nhiều lần gọi để có thể được sử dụng dưới dạng decorator.

   .. versionchanged:: 3.10
      Các async context manager được tạo bằng :deco:`asynccontextmanager` có thể được sử dụng dưới dạng decorator.


.. function:: closing(thing)

   Trả về một context manager đóng *thing* khi khối lệnh hoàn tất. Về cơ bản, điều này tương đương với::

      from contextlib import contextmanager

      @contextmanager
      def closing(thing):
          try:
              yield thing
          finally:
              thing.close()

   Và cho phép bạn viết mã như sau::

      from contextlib import closing
      from urllib.request import urlopen

      with closing(urlopen('https://www.python.org')) as page:
          for line in page:
              print(line)

   mà không cần đóng ``page`` một cách rõ ràng. Ngay cả khi xảy ra lỗi, ``page.close()`` sẽ được gọi khi thoát khỏi khối :keyword:`with`.

   .. note::

      Hầu hết các kiểu quản lý tài nguyên đều hỗ trợ giao thức :term:`context manager`, giao thức này sẽ đóng *thing* khi thoát khỏi câu lệnh :keyword:`with`. Vì vậy, :func:`!closing` hữu ích nhất đối với các kiểu của bên thứ ba không hỗ trợ context manager. Ví dụ này chỉ nhằm mục đích minh họa, vì thông thường :func:`~urllib.request.urlopen` sẽ được sử dụng trong một context manager.

.. function:: aclosing(thing)

   Trả về một async context manager gọi phương thức ``aclose()`` của *thing* khi khối lệnh hoàn tất. Về cơ bản, điều này tương đương với::

      from contextlib import asynccontextmanager

      @asynccontextmanager
      async def aclosing(thing):
          try:
              yield thing
          finally:
              await thing.aclose()

   Đáng chú ý, ``aclosing()`` hỗ trợ việc dọn dẹp xác định các async generator khi chúng vô tình thoát sớm do :keyword:`break` hoặc một ngoại lệ. Ví dụ:::

      from contextlib import aclosing

      async with aclosing(my_generator()) as values:
          async for value in values:
              if value == 42:
                  break

   Mẫu này đảm bảo mã thoát bất đồng bộ của generator được thực thi trong cùng context với các lần lặp của nó (để các ngoại lệ và biến context hoạt động như mong đợi, đồng thời mã thoát không chạy sau khi vòng đời của một task mà nó phụ thuộc vào đã kết thúc).

   .. versionadded:: 3.10


.. _simplifying-support-for-single-optional-context-managers:

.. function:: nullcontext(enter_result=None)

   Trả về một context manager trả về *enter_result* từ :meth:`~object.__enter__`, nhưng không thực hiện thao tác nào khác. Nó được dùng làm đối tượng thay thế cho một context manager tùy chọn, ví dụ:::

      def myfunction(arg, ignore_exceptions=False):
          if ignore_exceptions:
              # Dùng suppress để bỏ qua mọi ngoại lệ.
              cm = contextlib.suppress(Exception)
          else:
              # Không bỏ qua bất kỳ ngoại lệ nào, cm không có tác dụng.
              cm = contextlib.nullcontext()
          with cm:
              # Thực hiện thao tác nào đó

   Một ví dụ sử dụng *enter_result*::

      def process_file(file_or_path):
          if isinstance(file_or_path, str):
              # Nếu là chuỗi, mở tệp
              cm = open(file_or_path)
          else:
              # Người gọi chịu trách nhiệm đóng tệp
              cm = nullcontext(file_or_path)

          with cm as file:
              # Thực hiện xử lý trên tệp

   Nó cũng có thể được dùng thay cho
   :ref:`asynchronous context managers <async-context-managers>`::

       async def send_http(session=None):
           if not session:
               # Nếu không có http session, tạo session bằng aiohttp
               cm = aiohttp.ClientSession()
           else:
               # Người gọi chịu trách nhiệm đóng session
               cm = nullcontext(session)

           async with cm as session:
               # Gửi các yêu cầu http bằng session

   .. versionadded:: 3.7

   .. versionchanged:: 3.10
      :term:`asynchronous context manager` support was added.



.. function:: suppress(*exceptions)

   Trả về một context manager để bỏ qua mọi exception được chỉ định nếu chúng xảy ra trong phần thân của câu lệnh :keyword:`!with` và sau đó tiếp tục thực thi với câu lệnh đầu tiên sau phần kết thúc của
   câu lệnh :keyword:`!with`.

   Cũng như mọi cơ chế khác hoàn toàn bỏ qua exception, context manager này chỉ nên được dùng để bao quát những lỗi rất cụ thể mà trong đó việc âm thầm tiếp tục thực thi chương trình được xác định là cách xử lý đúng đắn.

   Ví dụ::

       from contextlib import suppress

       with suppress(FileNotFoundError):
           os.remove('somefile.tmp')

       with suppress(FileNotFoundError):
           os.remove('someotherfile.tmp')

   Đoạn mã này tương đương với::

       try:
           os.remove('somefile.tmp')
       except FileNotFoundError:
           pass

       try:
           os.remove('someotherfile.tmp')
       except FileNotFoundError:
           pass

   Context manager này có thể tái nhập :ref:`reentrant <reentrant-cms>`.

   Nếu mã bên trong :keyword:`!with` block phát sinh một
   :exc:`BaseExceptionGroup`, các ngoại lệ bị loại bỏ sẽ được xóa khỏi nhóm. Bất kỳ ngoại lệ nào trong nhóm không bị loại bỏ sẽ được phát sinh lại trong một nhóm mới được tạo bằng phương thức :meth:`~BaseExceptionGroup.derive` của nhóm ban đầu.

   .. versionadded:: 3.4

   .. versionchanged:: 3.12
      ``suppress`` hiện hỗ trợ loại bỏ các ngoại lệ phát sinh trong một :exc:`BaseExceptionGroup`.

.. function:: redirect_stdout(new_target)

   Context manager để tạm thời chuyển hướng :data:`sys.stdout` đến một tệp khác hoặc một đối tượng giống tệp.

   Công cụ này bổ sung tính linh hoạt cho các hàm hoặc lớp hiện có mà đầu ra được gắn cố định với stdout.

   Ví dụ: đầu ra của :func:`help` thường được gửi đến *sys.stdout*. Bạn có thể thu đầu ra đó vào một chuỗi bằng cách chuyển hướng đầu ra đến một
   đối tượng :class:`io.StringIO`. Stream thay thế được trả về từ phương thức :class:`io.StringIO` và do đó có thể được dùng làm đích của
   phương thức :meth:`~object.__enter__`, vì vậy nó có thể được dùng làm đích của câu lệnh
   :keyword:`with`::

        with redirect_stdout(io.StringIO()) as f:
            help(pow)
        s = f.getvalue()

   Để gửi đầu ra của :func:`help` đến một tệp trên ổ đĩa, hãy chuyển hướng đầu ra đến một tệp thông thường::

        with open('help.txt', 'w') as f:
            with redirect_stdout(f):
                help(pow)

   Để gửi đầu ra của :func:`help` đến *sys.stderr*::

        with redirect_stdout(sys.stderr):
            help(pow)

   Lưu ý rằng tác dụng phụ toàn cục lên :data:`sys.stdout` có nghĩa là context manager này không phù hợp để sử dụng trong mã thư viện và hầu hết các ứng dụng đa luồng. Nó cũng không ảnh hưởng đến đầu ra của các subprocess. Tuy nhiên, đây vẫn là một cách hữu ích cho nhiều utility script.

   Context manager này có thể tái nhập :ref:`reentrant <reentrant-cms>`.

   .. versionadded:: 3.4


.. function:: redirect_stderr(new_target)

   Tương tự :func:`~contextlib.redirect_stdout` nhưng chuyển hướng
   :data:`sys.stderr` sang một tệp khác hoặc đối tượng tương tự tệp.

   Context manager này có thể tái nhập :ref:`reentrant <reentrant-cms>`.

   .. versionadded:: 3.5


.. function:: chdir(path)

   Trình quản lý ngữ cảnh không an toàn khi chạy song song để thay đổi thư mục làm việc hiện tại. Vì thao tác này thay đổi một trạng thái toàn cục là thư mục làm việc, nên nó không phù hợp để sử dụng trong hầu hết các ngữ cảnh có luồng hoặc async. Nó cũng không phù hợp với hầu hết các quá trình thực thi mã phi tuyến tính, chẳng hạn như generator, trong đó quá trình thực thi của chương trình tạm thời được nhường lại -- trừ khi bạn thực sự mong muốn điều đó, không nên yield khi trình quản lý ngữ cảnh này đang hoạt động.

   Đây là một wrapper đơn giản quanh :func:`~os.chdir`, thay đổi thư mục làm việc hiện tại khi bắt đầu và khôi phục thư mục cũ khi kết thúc.

   Context manager này có thể tái nhập :ref:`reentrant <reentrant-cms>`.

   .. versionadded:: 3.11


.. class:: ContextDecorator()

   Một lớp cơ sở cho phép sử dụng context manager dưới dạng decorator.

   Các context manager kế thừa từ ``ContextDecorator`` phải triển khai
   :meth:`~object.__enter__` và :meth:`~object.__exit__` như bình thường. ``__exit__`` vẫn giữ cơ chế xử lý ngoại lệ tùy chọn ngay cả khi được sử dụng dưới dạng decorator.

   ``ContextDecorator`` được :deco:`contextmanager` sử dụng, vì vậy bạn tự động có được chức năng này.

   Ví dụ về ``ContextDecorator``::

      from contextlib import ContextDecorator

      class mycontext(ContextDecorator):
          def __enter__(self):
              print('Starting')
              return self

          def __exit__(self, *exc):
              print('Finishing')
              return False

   Sau đó, có thể sử dụng lớp như sau::

      >>> @mycontext()
      ... def function():
      ...     print('The bit in the middle')
      ...
      >>> function()
      Starting
      The bit in the middle
      Finishing

      >>> with mycontext():
      ...     print('The bit in the middle')
      ...
      Starting
      The bit in the middle
      Finishing

   Thay đổi này chỉ là cú pháp rút gọn cho bất kỳ cấu trúc nào có dạng sau::

      def f():
          with cm():
              # Thực hiện công việc

   ``ContextDecorator`` cho phép bạn viết theo cách khác::

      @cm()
      def f():
          # Thực hiện công việc

   Điều này làm rõ rằng ``cm`` áp dụng cho toàn bộ hàm, thay vì chỉ một phần của hàm (và việc tiết kiệm một cấp độ thụt lề cũng rất tiện).

   Các context manager hiện có vốn đã có lớp cơ sở có thể được mở rộng bằng cách sử dụng ``ContextDecorator`` làm lớp mixin::

      from contextlib import ContextDecorator

      class mycontext(ContextBaseClass, ContextDecorator):
          def __enter__(self):
              return self

          def __exit__(self, *exc):
              return False

   .. note::
      Vì hàm được trang trí phải có khả năng được gọi nhiều lần, context manager bên dưới phải hỗ trợ việc sử dụng trong nhiều câu lệnh :keyword:`with`. Nếu không, nên sử dụng cấu trúc ban đầu với câu lệnh :keyword:`!with` tường minh bên trong hàm.

   .. versionadded:: 3.2


.. class:: AsyncContextDecorator

   Tương tự như :class:`ContextDecorator` nhưng chỉ dành cho các hàm bất đồng bộ.

   Ví dụ về ``AsyncContextDecorator``::

      from asyncio import run
      from contextlib import AsyncContextDecorator

      class mycontext(AsyncContextDecorator):
          async def __aenter__(self):
              print('Starting')
              return self

          async def __aexit__(self, *exc):
              print('Finishing')
              return False

   Sau đó, có thể sử dụng lớp như sau::

      >>> @mycontext()
      ... async def function():
      ...     print('The bit in the middle')
      ...
      >>> run(function())
      Starting
      The bit in the middle
      Finishing

      >>> async def function():
      ...    async with mycontext():
      ...         print('The bit in the middle')
      ...
      >>> run(function())
      Starting
      The bit in the middle
      Finishing

   .. versionadded:: 3.10


.. class:: ExitStack()

   Một context manager được thiết kế để giúp dễ dàng kết hợp các context manager và hàm dọn dẹp khác bằng chương trình, đặc biệt là những thành phần tùy chọn hoặc được điều khiển bởi dữ liệu đầu vào.

   Ví dụ: có thể dễ dàng xử lý một tập hợp tệp trong một câu lệnh with duy nhất như sau::

      with ExitStack() as stack:
          files = [stack.enter_context(open(fname)) for fname in filenames]
          # Tất cả các tệp đã mở sẽ tự động được đóng ở cuối
          # câu lệnh with, ngay cả khi các nỗ lực mở tệp sau đó
          # trong danh sách phát sinh ngoại lệ

   Phương thức :meth:`~object.__enter__` trả về thực thể :class:`ExitStack` và không thực hiện thêm thao tác nào.

   Mỗi thực thể duy trì một ngăn xếp các callback đã đăng ký. Các callback này được gọi theo thứ tự ngược lại khi thực thể được đóng (dù là tường minh hay ngầm định ở cuối câu lệnh :keyword:`with`). Lưu ý rằng các callback *không* được gọi ngầm định khi thực thể ngăn xếp ngữ cảnh được garbage collection.

   Mô hình ngăn xếp này được sử dụng để các context manager nhận tài nguyên trong phương thức ``__init__`` của chúng (chẳng hạn như đối tượng tệp) có thể được xử lý chính xác.

   Vì các callback đã đăng ký được gọi theo thứ tự ngược lại với thứ tự đăng ký, cách này hoạt động như thể đã sử dụng nhiều câu lệnh :keyword:`with` lồng nhau với tập callback đã đăng ký. Điều này cũng áp dụng cho việc xử lý ngoại lệ - nếu một callback bên trong suppress hoặc thay thế một ngoại lệ, các callback bên ngoài sẽ nhận được các đối số dựa trên trạng thái đã cập nhật đó.

   Đây là một API tương đối cấp thấp, đảm nhiệm các chi tiết để unwind chính xác ngăn xếp các callback thoát. API này cung cấp nền tảng phù hợp cho các context manager cấp cao hơn, vốn thao tác với ngăn xếp thoát theo những cách riêng cho từng ứng dụng.

   .. versionadded:: 3.3

   .. method:: enter_context(cm)

      Đi vào một context manager mới và thêm phương thức :meth:`~object.__exit__` của nó vào ngăn xếp callback. Giá trị trả về là kết quả của phương thức :meth:`~object.__enter__` của chính context manager đó.

      Các context manager này có thể suppress ngoại lệ, giống như cách chúng vẫn làm khi được sử dụng trực tiếp như một phần của câu lệnh :keyword:`with`.

      .. versionchanged:: 3.11
         Nêu :exc:`TypeError` thay vì :exc:`AttributeError` nếu *cm* không phải là một trình quản lý ngữ cảnh.

   .. method:: push(exit)

      Thêm phương thức :meth:`~object.__exit__` của trình quản lý ngữ cảnh vào ngăn xếp callback.

      Vì ``__enter__`` *không* được gọi, phương thức này có thể được dùng để bao phủ một phần triển khai :meth:`~object.__enter__` bằng phương thức riêng của trình quản lý ngữ cảnh
      :meth:`~object.__exit__`.

      Nếu được truyền một đối tượng không phải là trình quản lý ngữ cảnh, phương thức này giả định đó là một callback có cùng chữ ký với phương thức
      :meth:`~object.__exit__` của trình quản lý ngữ cảnh và thêm trực tiếp callback đó vào ngăn xếp callback.

      Bằng cách trả về các giá trị true, những callback này có thể ngăn chặn ngoại lệ giống như các phương thức :meth:`~object.__exit__` của trình quản lý ngữ cảnh.

      Đối tượng được truyền vào sẽ được trả về từ hàm, cho phép sử dụng phương thức này làm function decorator.

   .. method:: callback(callback, /, *args, **kwds)

      Chấp nhận một callback function tùy ý cùng các đối số và thêm chúng vào callback stack.

      Không giống các phương thức khác, các callback được thêm theo cách này không thể ngăn chặn exception (vì chúng không bao giờ được truyền thông tin chi tiết về exception).

      Callback được truyền vào sẽ được trả về từ hàm, cho phép sử dụng phương thức này làm function decorator.

   .. method:: pop_all()

      Chuyển callback stack sang một instance :class:`ExitStack` mới và trả về instance đó. Thao tác này không gọi callback nào - thay vào đó, chúng sẽ được gọi khi stack mới được đóng (dù là tường minh hay ngầm định ở cuối câu lệnh :keyword:`with`).

      Ví dụ: có thể mở một nhóm tệp dưới dạng thao tác "tất cả hoặc không gì cả" như sau::

         with ExitStack() as stack:
             files = [stack.enter_context(open(fname)) for fname in filenames]
             # Giữ lại phương thức close nhưng chưa gọi nó.
             close_files = stack.pop_all().close
             # nếu việc mở bất kỳ tệp nào không thành công, tất cả các tệp đã mở trước đó sẽ được
             # tự động đóng. Nếu tất cả các tệp đều được mở thành công,
             # chúng sẽ vẫn mở ngay cả sau khi câu lệnh with kết thúc.
             # Sau đó có thể gọi close_files() một cách rõ ràng để đóng tất cả chúng.

   .. method:: close()

      Giải phóng ngay lập tức ngăn xếp callback, gọi các callback theo thứ tự ngược với thứ tự đăng ký. Đối với mọi context manager và exit callback đã đăng ký, các đối số được truyền vào sẽ cho biết rằng không có ngoại lệ nào xảy ra.

.. class:: AsyncExitStack()

   Một :ref:`trình quản lý ngữ cảnh bất đồng bộ <async-context-managers>`, tương tự như :class:`ExitStack`, hỗ trợ kết hợp cả context manager đồng bộ và bất đồng bộ, đồng thời có các coroutine để xử lý logic dọn dẹp.

   Phương thức :meth:`~ExitStack.close` không được triển khai; phải sử dụng :meth:`aclose` thay thế.

   .. method:: enter_async_context(cm)
      :async:

      Tương tự :meth:`ExitStack.enter_context` nhưng yêu cầu một trình quản lý ngữ cảnh bất đồng bộ.

      .. versionchanged:: 3.11
         Ném :exc:`TypeError` thay vì :exc:`AttributeError` nếu *cm* không phải là trình quản lý ngữ cảnh bất đồng bộ.

   .. method:: push_async_exit(exit)

      Tương tự :meth:`ExitStack.push` nhưng yêu cầu một trình quản lý ngữ cảnh bất đồng bộ hoặc một hàm coroutine.

   .. method:: push_async_callback(callback, /, *args, **kwds)

      Tương tự :meth:`ExitStack.callback` nhưng yêu cầu một hàm coroutine.

   .. method:: aclose()
      :async:

      Tương tự :meth:`ExitStack.close` nhưng xử lý đúng các awaitable.

   Tiếp tục ví dụ về :deco:`asynccontextmanager`::

      async with AsyncExitStack() as stack:
          connections = [await stack.enter_async_context(get_connection())
              for i in range(5)]
          # Tất cả các kết nối đã mở sẽ tự động được giải phóng vào cuối
          # câu lệnh async with, ngay cả khi việc cố gắng mở một kết nối
          # ở vị trí sau trong danh sách gây ra ngoại lệ.

   .. versionadded:: 3.7

Ví dụ và công thức
------------------

Phần này mô tả một số ví dụ và công thức để sử dụng hiệu quả các công cụ do :mod:`!contextlib` cung cấp.


Hỗ trợ số lượng context manager biến đổi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trường hợp sử dụng chính của :class:`ExitStack` là trường hợp được nêu trong tài liệu của lớp: hỗ trợ một số lượng context manager (trình quản lý ngữ cảnh) và các thao tác dọn dẹp khác có thể biến đổi trong một câu lệnh :keyword:`with` duy nhất. Tính biến đổi này có thể bắt nguồn từ việc số lượng context manager cần dùng phụ thuộc vào đầu vào của người dùng (chẳng hạn như mở một tập hợp tệp do người dùng chỉ định), hoặc từ việc một số context manager là tùy chọn::

    with ExitStack() as stack:
        for resource in resources:
            stack.enter_context(resource)
        if need_special_resource():
            special = acquire_special_resource()
            stack.callback(release_special_resource, special)
        # Thực hiện các thao tác sử dụng tài nguyên đã nhận được

Như đã trình bày, :class:`ExitStack` cũng giúp việc sử dụng các câu lệnh :keyword:`with` để quản lý những tài nguyên tùy ý vốn không hỗ trợ sẵn giao thức quản lý ngữ cảnh trở nên khá dễ dàng.


Bắt các ngoại lệ từ các phương thức ``__enter__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Đôi khi, việc bắt các ngoại lệ từ phần triển khai phương thức :meth:`~object.__enter__` là cần thiết, *mà không* vô tình bắt các ngoại lệ từ phần thân câu lệnh :keyword:`with` hoặc phương thức :meth:`~object.__exit__` của context manager. Bằng cách sử dụng :class:`ExitStack`, có thể tách các bước trong giao thức quản lý ngữ cảnh ở một mức độ nhất định để cho phép thực hiện điều này::

   stack = ExitStack()
   try:
       x = stack.enter_context(cm)
   except Exception:
       # xử lý ngoại lệ của __enter__
   else:
       with stack:
           # Xử lý trường hợp bình thường

Việc thực sự cần làm điều này có thể cho thấy API nền tảng nên cung cấp một giao diện quản lý tài nguyên trực tiếp để sử dụng với
:keyword:`try`/:keyword:`except`/:keyword:`finally` câu lệnh, nhưng không phải API nào cũng được thiết kế tốt về mặt này. Khi context manager là API quản lý tài nguyên duy nhất được cung cấp, thì :class:`ExitStack` có thể giúp xử lý dễ dàng hơn nhiều tình huống không thể xử lý trực tiếp trong một
câu lệnh :keyword:`with`.


Dọn dẹp trong phần triển khai ``__enter__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Như đã nêu trong tài liệu về :meth:`ExitStack.push`, phương thức này có thể hữu ích khi dọn dẹp một tài nguyên đã được cấp phát nếu các bước sau đó trong phần triển khai :meth:`~object.__enter__` thất bại.

Dưới đây là ví dụ thực hiện việc này với một context manager chấp nhận các hàm thu nhận và giải phóng tài nguyên, cùng với một hàm xác thực tùy chọn, rồi ánh xạ chúng vào protocol quản lý context::

   from contextlib import contextmanager, AbstractContextManager, ExitStack

   class ResourceManager(AbstractContextManager):

       def __init__(self, acquire_resource, release_resource, check_resource_ok=None):
           self.acquire_resource = acquire_resource
           self.release_resource = release_resource
           if check_resource_ok is None:
               def check_resource_ok(resource):
                   return True
           self.check_resource_ok = check_resource_ok

       @contextmanager
       def _cleanup_on_error(self):
           with ExitStack() as stack:
               stack.push(self)
               yield
               # Việc kiểm tra xác thực đã thành công và không phát sinh exception
               # Vì vậy, chúng ta muốn giữ lại tài nguyên và truyền nó
               # trở lại cho caller
               stack.pop_all()

       def __enter__(self):
           resource = self.acquire_resource()
           with self._cleanup_on_error():
               if not self.check_resource_ok(resource):
                   msg = "Failed validation for {!r}"
                   raise RuntimeError(msg.format(resource))
           return resource

       def __exit__(self, *exc_details):
           # Chúng ta không cần lặp lại bất kỳ logic giải phóng tài nguyên nào
           self.release_resource()


Thay thế mọi chỗ sử dụng ``try-finally`` và các biến cờ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một mẫu bạn sẽ thỉnh thoảng thấy là một câu lệnh ``try-finally`` cùng với một biến cờ để cho biết liệu phần thân của mệnh đề ``finally`` có nên được thực thi hay không. Ở dạng đơn giản nhất (không thể được xử lý chỉ bằng cách sử dụng mệnh đề ``except`` thay thế), nó trông như sau::

   cleanup_needed = True
   try:
       result = perform_operation()
       if result:
           cleanup_needed = False
   finally:
       if cleanup_needed:
           cleanup_resources()

Cũng như với mọi mã dựa trên câu lệnh ``try``, điều này có thể gây ra vấn đề cho việc phát triển và review, vì mã thiết lập và mã dọn dẹp có thể bị ngăn cách bởi những đoạn mã dài tùy ý.

:class:`ExitStack` cho phép thay vào đó đăng ký một callback để thực thi khi kết thúc câu lệnh ``with``, rồi sau đó quyết định bỏ qua việc thực thi callback đó::

   from contextlib import ExitStack

   with ExitStack() as stack:
       stack.callback(cleanup_resources)
       result = perform_operation()
       if result:
           stack.pop_all()

Điều này cho phép làm rõ ngay từ đầu hành vi dọn dẹp dự kiến, thay vì yêu cầu một biến cờ riêng.

Nếu một ứng dụng cụ thể sử dụng mẫu này nhiều, có thể đơn giản hóa hơn nữa bằng một helper class nhỏ::

   from contextlib import ExitStack

   class Callback(ExitStack):
       def __init__(self, callback, /, *args, **kwds):
           super().__init__()
           self.callback(callback, *args, **kwds)

       def cancel(self):
           self.pop_all()

   with Callback(cleanup_resources) as cb:
       result = perform_operation()
       if result:
           cb.cancel()

Nếu việc dọn dẹp tài nguyên chưa được gói gọn một cách rõ ràng trong một hàm độc lập, bạn vẫn có thể sử dụng dạng decorator của
:meth:`ExitStack.callback` để khai báo trước việc dọn dẹp tài nguyên::

   from contextlib import ExitStack

   with ExitStack() as stack:
       @stack.callback
       def cleanup_resources():
           ...
       result = perform_operation()
       if result:
           stack.pop_all()

Do cách thức hoạt động của giao thức decorator, một hàm callback được khai báo theo cách này không thể nhận bất kỳ tham số nào. Thay vào đó, mọi tài nguyên cần được giải phóng phải được truy cập dưới dạng các biến closure.


Sử dụng context manager làm decorator cho hàm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`ContextDecorator` cho phép sử dụng một context manager trong cả câu lệnh ``with`` thông thường lẫn dưới dạng decorator cho hàm.

Ví dụ, đôi khi việc bọc các hàm hoặc nhóm câu lệnh bằng một logger có thể theo dõi thời điểm bắt đầu và thời điểm kết thúc là hữu ích. Thay vì viết riêng cả decorator cho hàm và context manager cho tác vụ này, việc kế thừa từ :class:`ContextDecorator` cung cấp cả hai khả năng trong một định nghĩa duy nhất::

    from contextlib import ContextDecorator
    import logging

    logging.basicConfig(level=logging.INFO)

    class track_entry_and_exit(ContextDecorator):
        def __init__(self, name):
            self.name = name

        def __enter__(self):
            logging.info('Entering: %s', self.name)

        def __exit__(self, exc_type, exc, exc_tb):
            logging.info('Exiting: %s', self.name)

Các instance của lớp này có thể được sử dụng vừa như một context manager::

    with track_entry_and_exit('widget loader'):
        print('Some time consuming activity goes here')
        load_widget()

Và cũng có thể dùng làm function decorator::

    @track_entry_and_exit('widget loader')
    def activity():
        print('Some time consuming activity goes here')
        load_widget()

Lưu ý rằng có thêm một hạn chế khi sử dụng context manager làm function decorator: không có cách nào truy cập giá trị trả về của
:meth:`~object.__enter__`. Nếu cần giá trị đó, bạn vẫn phải sử dụng một câu lệnh ``with`` rõ ràng.

.. seealso::

   :pep:`343` - Câu lệnh "with"
      Đặc tả, bối cảnh và các ví dụ cho câu lệnh :keyword:`with` của Python.

.. _single-use-reusable-and-reentrant-cms:

Context manager dùng một lần, có thể tái sử dụng và có thể reentrant
--------------------------------------------------------------------

Hầu hết context manager được viết theo cách khiến chúng chỉ có thể được sử dụng hiệu quả một lần trong câu lệnh :keyword:`with`. Các context manager dùng một lần này phải được tạo mới mỗi khi sử dụng; việc cố gắng sử dụng chúng lần thứ hai sẽ gây ra exception hoặc không hoạt động chính xác theo cách khác.

Hạn chế phổ biến này có nghĩa là nhìn chung bạn nên tạo các context manager trực tiếp trong phần đầu của câu lệnh :keyword:`with` nơi chúng được sử dụng (như trong tất cả các ví dụ sử dụng ở trên).

Tệp là một ví dụ về context manager về cơ bản chỉ có thể sử dụng một lần, vì câu lệnh :keyword:`with` đầu tiên sẽ đóng tệp, ngăn mọi thao tác IO tiếp theo sử dụng đối tượng tệp đó.

Các context manager được tạo bằng :deco:`contextmanager` cũng là những context manager chỉ có thể sử dụng một lần và sẽ báo lỗi về việc generator bên dưới không thực hiện yield nếu cố gắng sử dụng chúng lần thứ hai::

    >>> from contextlib import contextmanager
    >>> @contextmanager
    ... def singleuse():
    ...     print("Before")
    ...     yield
    ...     print("After")
    ...
    >>> cm = singleuse()
    >>> with cm:
    ...     pass
    ...
    Before
    After
    >>> with cm:
    ...     pass
    ...
    Traceback (most recent call last):
        ...
    RuntimeError: generator didn't yield


.. _reentrant-cms:

Context manager có thể tái nhập
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các context manager phức tạp hơn có thể là "reentrant". Những context manager này không chỉ có thể được sử dụng trong nhiều câu lệnh :keyword:`with`, mà còn có thể được sử dụng *bên trong* một câu lệnh :keyword:`!with` vốn đang sử dụng cùng context manager đó.

:class:`threading.RLock` là một ví dụ về context manager có thể tái nhập, cũng như
:func:`suppress`, :func:`redirect_stdout`, và :func:`chdir`. Sau đây là một ví dụ rất đơn giản về việc sử dụng có thể tái nhập::

    >>> from contextlib import redirect_stdout
    >>> from io import StringIO
    >>> stream = StringIO()
    >>> write_to_stream = redirect_stdout(stream)
    >>> with write_to_stream:
    ...     print("This is written to the stream rather than stdout")
    ...     with write_to_stream:
    ...         print("This is also written to the stream")
    ...
    >>> print("This is written directly to stdout")
    This is written directly to stdout
    >>> print(stream.getvalue())
    This is written to the stream rather than stdout
    This is also written to the stream

Các ví dụ thực tế về tính tái nhập thường liên quan đến nhiều hàm gọi lẫn nhau, vì vậy phức tạp hơn rất nhiều so với ví dụ này.

Cũng lưu ý rằng có thể tái nhập *không* đồng nghĩa với thread safe.
:func:`redirect_stdout`, chẳng hạn, chắc chắn không thread safe, vì nó thực hiện một thay đổi toàn cục đối với trạng thái hệ thống bằng cách liên kết :data:`sys.stdout` với một stream khác.


.. _reusable-cms:

Context manager có thể tái sử dụng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khác với context manager dùng một lần và context manager có thể tái nhập, context manager "có thể tái sử dụng" (hoặc nói hoàn toàn rõ ràng là context manager "có thể tái sử dụng nhưng không thể tái nhập", vì context manager có thể tái nhập cũng có thể tái sử dụng). Các context manager này hỗ trợ việc được sử dụng nhiều lần, nhưng sẽ thất bại (hoặc nói cách khác là không hoạt động chính xác) nếu chính instance context manager đó đã được sử dụng trong một câu lệnh with bao quanh.

:class:`threading.Lock` là một ví dụ về context manager có thể tái sử dụng nhưng không thể tái nhập (đối với một reentrant lock, cần sử dụng
:class:`threading.RLock` thay vào đó).

Một ví dụ khác về context manager có thể tái sử dụng nhưng không reentrant là
:class:`ExitStack`, vì nó gọi *tất cả* callback hiện đã đăng ký khi rời khỏi bất kỳ câu lệnh with nào, bất kể các callback đó được thêm vào ở đâu::

    >>> from contextlib import ExitStack
    >>> stack = ExitStack()
    >>> with stack:
    ...     stack.callback(print, "Callback: from first context")
    ...     print("Leaving first context")
    ...
    Leaving first context
    Callback: from first context
    >>> with stack:
    ...     stack.callback(print, "Callback: from second context")
    ...     print("Leaving second context")
    ...
    Leaving second context
    Callback: from second context
    >>> with stack:
    ...     stack.callback(print, "Callback: from outer context")
    ...     with stack:
    ...         stack.callback(print, "Callback: from inner context")
    ...         print("Leaving inner context")
    ...     print("Leaving outer context")
    ...
    Leaving inner context
    Callback: from inner context
    Callback: from outer context
    Leaving outer context

Như kết quả từ ví dụ cho thấy, việc tái sử dụng một đối tượng stack duy nhất trong nhiều câu lệnh with hoạt động chính xác, nhưng việc cố gắng lồng chúng sẽ khiến stack bị xóa vào cuối câu lệnh with bên trong cùng, đây khó có thể là hành vi mong muốn.

Sử dụng các instance :class:`ExitStack` riêng biệt thay vì tái sử dụng một instance duy nhất sẽ tránh được vấn đề đó::

    >>> from contextlib import ExitStack
    >>> with ExitStack() as outer_stack:
    ...     outer_stack.callback(print, "Callback: from outer context")
    ...     with ExitStack() as inner_stack:
    ...         inner_stack.callback(print, "Callback: from inner context")
    ...         print("Leaving inner context")
    ...     print("Leaving outer context")
    ...
    Leaving inner context
    Callback: from inner context
    Leaving outer context
    Callback: from outer context
