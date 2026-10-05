.. _glossary:

**************
Bảng thuật ngữ
**************

.. if you add new entries, keep the alphabetical sorting!

.. glossary::

   ``>>>``
      Dấu nhắc Python mặc định của shell :term:`interactive`. Thường được thấy trong các ví dụ mã có thể thực thi tương tác trong trình thông dịch.

   ``...``
      Có thể chỉ:

      * Dấu nhắc Python mặc định của shell :term:`interactive` khi nhập mã cho một khối mã thụt lề, khi ở bên trong một cặp dấu phân cách trái và phải tương ứng (dấu ngoặc đơn, dấu ngoặc vuông, dấu ngoặc nhọn hoặc dấu ngoặc kép ba), hoặc sau khi chỉ định một decorator.

      .. index:: single: ...; ellipsis literal

      * Dạng ba dấu chấm của đối tượng :ref:`Ellipsis <bltin-ellipsis-object>`.

   abstract base class
   lớp cơ sở trừu tượng
      Các lớp cơ sở trừu tượng bổ trợ cho :term:`duck-typing` bằng cách cung cấp một phương thức để định nghĩa các interface khi những kỹ thuật khác như
      :func:`hasattr` sẽ vụng về hoặc sai một cách tinh vi (ví dụ với
      :ref:`magic methods <special-lookup>`). ABCs giới thiệu các lớp con ảo, là những lớp không kế thừa từ một lớp nào nhưng vẫn được :func:`isinstance` và :func:`issubclass` nhận diện; xem
      :mod:`abc` tài liệu module. Python đi kèm nhiều ABC tích hợp sẵn cho các cấu trúc dữ liệu (trong module :mod:`collections.abc`), các số (trong
      :mod:`numbers` module), các stream (trong module :mod:`io`), các import finder và loader (trong module :mod:`importlib.abc`). Bạn có thể tạo ABC của riêng mình bằng module :mod:`abc`.

   annotate function
   hàm annotate
      Một callable có thể được gọi để lấy :term:`annotations <annotation>` của một đối tượng. Các hàm annotate thường là :term:`functions <function>`, được tự động tạo dưới dạng thuộc tính :attr:`~object.__annotate__` của các hàm, lớp và module. Các hàm annotate là một tập con của
      :term:`evaluate functions <evaluate function>`.

   annotation
   chú thích
      Nhãn được liên kết với một biến, thuộc tính lớp, hoặc tham số hay giá trị trả về của hàm, theo quy ước được sử dụng làm một :term:`type hint`.

      Không thể truy cập chú thích của các biến cục bộ trong runtime, nhưng có thể truy xuất chú thích của các biến toàn cục, thuộc tính lớp và hàm bằng cách gọi :func:`annotationlib.get_annotations` trên các module, lớp và hàm tương ứng.

      Xem :term:`variable annotation`, :term:`function annotation`, :pep:`484`,
      :pep:`526` và :pep:`649`, trong đó mô tả chức năng này. Ngoài ra, hãy xem :ref:`annotations-howto` để biết các phương pháp hay nhất khi làm việc với chú thích.

   argument
   đối số
      Giá trị được truyền cho một :term:`function` (hoặc :term:`method`) khi gọi hàm.  Có hai loại đối số:

      * :dfn:`đối số từ khóa`: một đối số đứng trước một mã định danh (ví dụ: ``name=``) trong một lệnh gọi hàm hoặc được truyền dưới dạng một giá trị trong từ điển, đứng trước ``**``. Ví dụ, ``3`` và ``5`` đều là các đối số từ khóa trong những lệnh gọi sau đến :func:`complex`::

           complex(real=3, imag=5)
           complex(**{'real': 3, 'imag': 5})

      * :dfn:`đối số vị trí`: một đối số không phải là đối số từ khóa. Đối số vị trí có thể xuất hiện ở đầu danh sách đối số và/hoặc được truyền dưới dạng các phần tử của một :term:`iterable` đứng trước ``*``. Ví dụ, ``3`` và ``5`` đều là các đối số vị trí trong những lệnh gọi sau::

           complex(3, 5)
           complex(*(3, 5))

      Các đối số được gán cho những biến cục bộ có tên trong thân hàm. Xem phần :ref:`calls` để biết các quy tắc chi phối việc gán này. Về mặt cú pháp, bất kỳ biểu thức nào cũng có thể được dùng để biểu diễn một đối số; giá trị sau khi được đánh giá sẽ được gán cho biến cục bộ.

      Xem thêm mục từ :term:`parameter` trong bảng thuật ngữ và câu hỏi thường gặp về
      :ref:`sự khác biệt giữa đối số và tham số <faq-argument-vs-parameter>`, và :pep:`362`.

   asynchronous context manager
   trình quản lý ngữ cảnh bất đồng bộ
      Một đối tượng điều khiển môi trường được nhìn thấy trong một
      :keyword:`async with` câu lệnh bằng cách định nghĩa :meth:`~object.__aenter__` và
      các phương thức :meth:`~object.__aexit__`. Được giới thiệu bởi :pep:`492`.

   asynchronous generator
   bộ sinh bất đồng bộ
      Được dùng theo cách không chính thức để chỉ một :term:`asynchronous generator function` hoặc một :term:`asynchronous generator iterator`, tùy theo ngữ cảnh. Các thuật ngữ chính thức :term:`asynchronous generator function` và
      :term:`asynchronous generator iterator` ít phổ biến trong thực tế; chỉ riêng "asynchronous generator" gần như luôn là đủ.

   asynchronous generator function
   hàm sinh bất đồng bộ
      Một hàm trả về một :term:`asynchronous generator iterator`. Hàm này trông giống một hàm coroutine được định nghĩa bằng :keyword:`async def`, ngoại trừ việc nó chứa các biểu thức :keyword:`yield` để tạo ra một chuỗi giá trị có thể sử dụng trong vòng lặp :keyword:`async for`. Xem :pep:`525`.

      Một hàm generator bất đồng bộ có thể chứa các biểu thức :keyword:`await` cũng như :keyword:`async for`, và các câu lệnh :keyword:`async with`.

   asynchronous generator iterator
   iterator của generator bất đồng bộ
      Một đối tượng được tạo bởi một :term:`asynchronous generator function`.

      Đây là một :term:`asynchronous iterator` mà khi được gọi bằng cách sử dụng
      Phương thức :meth:`~object.__anext__` trả về một đối tượng awaitable, đối tượng này sẽ thực thi phần thân của hàm generator bất đồng bộ cho đến lần tiếp theo
      biểu thức :keyword:`yield`.

      Mỗi :keyword:`yield` tạm thời đình chỉ quá trình xử lý và ghi nhớ trạng thái thực thi, bao gồm các biến cục bộ và các câu lệnh try đang chờ xử lý. Khi *asynchronous generator iterator* thực sự tiếp tục với một awaitable khác được :meth:`~object.__anext__` trả về, nó tiếp tục từ nơi đã dừng. Xem :pep:`492` và :pep:`525`.

   asynchronous iterable
   iterable bất đồng bộ
      Một đối tượng có thể được sử dụng trong câu lệnh :keyword:`async for`. Phải trả về một :term:`asynchronous iterator` từ
      phương thức :meth:`~object.__aiter__`. Được giới thiệu bởi :pep:`492`.

   asynchronous iterator
   iterator bất đồng bộ
      Một đối tượng triển khai các phương thức :meth:`~object.__aiter__` và :meth:`~object.__anext__`. :meth:`~object.__anext__` phải trả về một đối tượng :term:`awaitable`.
      :keyword:`async for` phân giải các awaitable được phương thức :meth:`~object.__anext__` của iterator bất đồng bộ trả về cho đến khi phương thức này phát sinh một
      ngoại lệ :exc:`StopAsyncIteration`. Được giới thiệu bởi :pep:`492`.

   atomic operation
   thao tác nguyên tử
      Một thao tác dường như được thực thi như một bước duy nhất, không thể phân chia: không luồng nào khác có thể quan sát thấy thao tác đó đang thực hiện dở, và các hiệu ứng của nó trở nên hiển thị cùng một lúc. Python không đảm bảo rằng các câu lệnh cấp cao là nguyên tử (ví dụ: ``x += 1`` thực hiện nhiều thao tác bytecode và không có tính nguyên tử). Tính nguyên tử chỉ được đảm bảo khi được tài liệu hóa rõ ràng. Xem thêm :term:`race condition` và :term:`data race`.

   trạng thái luồng được gắn kết

      Một :term:`thread state` đang hoạt động đối với luồng OS hiện tại.

      Khi một :term:`thread state` được gắn kết, luồng OS có quyền truy cập vào toàn bộ Python C API và có thể gọi trình thông dịch bytecode một cách an toàn.

      Trừ khi một hàm ghi rõ điều ngược lại, việc cố gắng gọi C API mà không có trạng thái luồng được gắn kết sẽ dẫn đến lỗi nghiêm trọng hoặc hành vi không xác định. Người dùng có thể gắn kết và tách trạng thái luồng một cách rõ ràng thông qua C API, hoặc runtime có thể thực hiện ngầm việc này, bao gồm trong các lệnh gọi C chặn và bởi trình thông dịch bytecode giữa các lần gọi.

      Trong hầu hết các bản build của Python, việc có một trạng thái luồng được gắn kết đồng nghĩa với việc caller đang nắm giữ :term:`GIL` của interpreter hiện tại, vì vậy tại một thời điểm chỉ một luồng OS có thể có trạng thái luồng được gắn kết. Trong
      Các bản build :term:`không có GIL <free-threaded build>` của Python cho phép các thread đồng thời giữ một thread state được đính kèm, nhờ đó trình thông dịch bytecode có thể thực sự chạy song song.

   attribute
   thuộc tính
      Một giá trị được liên kết với một object, thường được tham chiếu theo tên bằng các biểu thức có dấu chấm. Ví dụ, nếu một object *o* có một attribute *a* thì nó sẽ được tham chiếu là *o.a*.

      Có thể gán cho một object một attribute có tên không phải là identifier như được định nghĩa bởi :ref:`identifiers`, chẳng hạn bằng cách sử dụng
      :func:`setattr`, nếu object cho phép. Attribute như vậy sẽ không thể được truy cập bằng biểu thức có dấu chấm, mà thay vào đó cần được lấy bằng :func:`getattr`.

   awaitable
      Một object có thể được sử dụng trong biểu thức :keyword:`await`. Có thể là một :term:`coroutine` hoặc một object có method :meth:`~object.__await__`. Xem thêm :pep:`492`.

   BDFL
      Benevolent Dictator For Life, còn gọi là `Guido van Rossum <https://gvanrossum.github.io/>`_, người tạo ra Python.

   binary file
   tệp nhị phân
      Một :term:`file object` có khả năng đọc và ghi
      :term:`các đối tượng giống byte <bytes-like object>`. Ví dụ về tệp nhị phân là các tệp được mở ở chế độ nhị phân (``'rb'``, ``'wb'`` hoặc ``'rb+'``), :data:`sys.stdin.buffer <sys.stdin>`,
      :data:`sys.stdout.buffer <sys.stdout>`, và các thể hiện của
      :class:`io.BytesIO` và :class:`gzip.GzipFile`.

      Xem thêm :term:`text file` để biết về một đối tượng tệp có thể đọc và ghi
      các đối tượng :class:`str`.

   borrowed reference
   tham chiếu mượn
      Trong C API của Python, tham chiếu mượn là một tham chiếu đến một đối tượng mà mã sử dụng đối tượng đó không sở hữu tham chiếu. Tham chiếu này sẽ trở thành một con trỏ treo nếu đối tượng bị hủy. Ví dụ, quá trình garbage collection có thể xóa :term:`strong reference` cuối cùng đến đối tượng, từ đó hủy đối tượng.

      Bạn nên gọi :c:func:`Py_INCREF` trên :term:`borrowed reference` để chuyển nó thành :term:`strong reference` ngay tại chỗ, ngoại trừ khi đối tượng không thể bị hủy trước lần sử dụng cuối cùng của tham chiếu mượn. Có thể sử dụng hàm :c:func:`Py_NewRef` để tạo một
      :term:`strong reference`.

   bytes-like object
   đối tượng dạng bytes
      Một đối tượng hỗ trợ :ref:`bufferobjects` và có thể xuất một bộ đệm C-:term:`contiguous`. Điều này bao gồm tất cả :class:`bytes`,
      :class:`bytearray`, và các đối tượng :class:`array.array`, cũng như nhiều đối tượng :class:`memoryview` phổ biến. Các đối tượng giống bytes có thể được sử dụng cho nhiều thao tác làm việc với dữ liệu nhị phân; trong đó có nén, lưu vào tệp nhị phân và gửi qua socket.

      Một số thao tác cần dữ liệu nhị phân có thể thay đổi. Tài liệu thường gọi các đối tượng này là "các đối tượng giống bytes có thể đọc-ghi". Các đối tượng bộ đệm có thể thay đổi bao gồm :class:`bytearray` và một
      :class:`memoryview` của một :class:`bytearray`. Các thao tác khác yêu cầu dữ liệu nhị phân được lưu trong các đối tượng bất biến ("các đối tượng giống bytes chỉ đọc"); ví dụ gồm :class:`bytes` và một :class:`memoryview` của một đối tượng :class:`bytes`.

   bytecode
   mã byte
      Mã nguồn Python được biên dịch thành mã byte, biểu diễn nội bộ của một chương trình Python trong trình thông dịch CPython. Mã byte cũng được lưu vào bộ nhớ đệm trong các tệp ``.pyc``, nhờ đó việc thực thi cùng một tệp sẽ nhanh hơn vào lần thứ hai (có thể tránh biên dịch lại từ mã nguồn sang mã byte). "Ngôn ngữ trung gian" này được cho là chạy trên một
      :term:`virtual machine` thực thi mã máy tương ứng với từng mã byte. Lưu ý rằng mã byte không được kỳ vọng sẽ hoạt động giữa các máy ảo Python khác nhau, cũng như không ổn định giữa các bản phát hành Python.

      Danh sách các chỉ dẫn mã byte có thể được tìm thấy trong tài liệu về
      :ref:`mô-đun dis <bytecodes>`.

   callable
      Callable là một đối tượng có thể được gọi, có thể kèm theo một tập hợp đối số (xem :term:`argument`), với cú pháp sau đây::

         callable(argument1, argument2, argumentN)

      Một :term:`function`, và do đó là một :term:`method`, là một callable. Một instance của một class triển khai method :meth:`~object.__call__` cũng là một callable.

   callback
      Một hàm subroutine được truyền làm đối số để thực thi tại một thời điểm nào đó trong tương lai.

   class
      Một khuôn mẫu để tạo các đối tượng do người dùng định nghĩa. Định nghĩa lớp thường chứa các định nghĩa phương thức hoạt động trên các thể hiện của lớp.

   class variable
   biến lớp
      Một biến được định nghĩa trong một lớp và chỉ được phép sửa đổi ở cấp lớp (tức là không sửa đổi trong một thể hiện của lớp).

   closure variable
   biến closure
      Một :term:`free variable` được tham chiếu từ một :term:`nested scope` được định nghĩa trong một phạm vi bên ngoài, thay vì được phân giải trong runtime từ các namespace globals hoặc builtin. Có thể được định nghĩa rõ ràng bằng từ khóa :keyword:`nonlocal` để cho phép quyền ghi, hoặc được định nghĩa ngầm nếu biến chỉ được đọc.

      Ví dụ, trong hàm ``inner`` ở đoạn mã sau, cả ``x`` và ``print`` đều là
      :term:`biến tự do <free variable>`, nhưng chỉ ``x`` mới là một *biến closure*::

          def outer():
              x = 0
              def inner():
                  nonlocal x
                  x += 1
                  print(x)
              return inner

      Do thuộc tính :attr:`codeobject.co_freevars` (mặc dù tên gọi là như vậy, thuộc tính này chỉ bao gồm tên của các biến closure thay vì liệt kê tất cả các biến tự do được tham chiếu), thuật ngữ tổng quát hơn :term:`free variable` đôi khi được sử dụng ngay cả khi ý định cụ thể là đề cập đến các biến closure.

   complex number
   số phức
      Một phần mở rộng của hệ thống số thực quen thuộc, trong đó mọi số được biểu diễn dưới dạng tổng của phần thực và phần ảo.  Số ảo là các bội số thực của đơn vị ảo (căn bậc hai của ``-1``), thường được viết là ``i`` trong toán học hoặc ``j`` trong kỹ thuật.  Python tích hợp sẵn khả năng hỗ trợ số phức, được viết bằng ký hiệu sau; phần ảo được viết với hậu tố ``j``, ví dụ ``3+1j``.  Để truy cập các phiên bản tương ứng dành cho số phức của
      module :mod:`math`, hãy sử dụng :mod:`cmath`.  Việc sử dụng số phức là một tính năng toán học khá nâng cao.  Nếu bạn không nhận thức được nhu cầu sử dụng chúng, gần như chắc chắn bạn có thể an toàn bỏ qua chúng.

   concurrency
   tính đồng thời
      Khả năng của một chương trình máy tính thực hiện nhiều tác vụ cùng lúc.  Python cung cấp các thư viện để viết những chương trình sử dụng các dạng concurrency khác nhau.  :mod:`asyncio` là một thư viện dùng để xử lý các tác vụ bất đồng bộ và coroutine.  :mod:`threading` cung cấp quyền truy cập vào các thread của hệ điều hành, còn :mod:`multiprocessing` cung cấp quyền truy cập vào các process của hệ điều hành. Các bộ xử lý đa lõi có thể thực thi các thread và process trên những lõi CPU khác nhau cùng một lúc (xem
      :term:`parallelism`).

   concurrent modification
   sửa đổi đồng thời
      Khi nhiều luồng sửa đổi dữ liệu dùng chung cùng lúc. Việc sửa đổi đồng thời mà không được đồng bộ hóa đúng cách có thể gây ra
      :term:`các điều kiện tranh chấp <race condition>`, và cũng có thể dẫn đến
      :term:`tranh chấp dữ liệu <data race>`, hỏng dữ liệu hoặc cả hai.

   context
   ngữ cảnh
      Thuật ngữ này có các ý nghĩa khác nhau tùy thuộc vào nơi và cách nó được sử dụng. Một số ý nghĩa phổ biến:

      * Trạng thái hoặc môi trường tạm thời được thiết lập bởi một :term:`context manager` thông qua câu lệnh :keyword:`with`.
      * Tập hợp các liên kết khóa­giá trị gắn với một
        :class:`contextvars.Context` đối tượng và được truy cập thông qua
        Các đối tượng :class:`~contextvars.ContextVar`. Xem thêm :term:`context variable`.
      * Một đối tượng :class:`contextvars.Context`. Xem thêm :term:`current context`.

   context management protocol
   giao thức quản lý ngữ cảnh
      Các phương thức :meth:`~object.__enter__` và :meth:`~object.__exit__` được câu lệnh :keyword:`with` gọi. Xem :pep:`343`.

   context manager
   trình quản lý ngữ cảnh
      Một đối tượng triển khai :term:`context management protocol` và kiểm soát môi trường được thấy trong câu lệnh :keyword:`with`. Xem
      :pep:`343`.

   context variable
   biến context
      Một biến có giá trị phụ thuộc vào context nào là :term:`current context`. Các giá trị được truy cập thông qua các đối tượng :class:`contextvars.ContextVar`. Các biến context chủ yếu được dùng để cô lập trạng thái giữa các tác vụ bất đồng bộ chạy đồng thời.

   contiguous
   liền kề
      .. index:: C-contiguous, Fortran contiguous

      Một buffer được xem là liền kề chính xác khi nó là *C-contiguous* hoặc *Fortran contiguous*. Các buffer không chiều đều liền kề theo cả kiểu C và Fortran. Trong các mảng một chiều, các phần tử phải được bố trí trong bộ nhớ cạnh nhau, theo thứ tự chỉ mục tăng dần bắt đầu từ 0. Trong các mảng đa chiều C-contiguous, chỉ mục cuối cùng thay đổi nhanh nhất khi duyệt các phần tử theo thứ tự địa chỉ bộ nhớ. Tuy nhiên, trong các mảng Fortran contiguous, chỉ mục đầu tiên thay đổi nhanh nhất.

   coroutine
      Coroutine là một dạng tổng quát hơn của subroutine. Subroutine được đi vào tại một điểm và thoát ra tại một điểm khác. Coroutine có thể được đi vào, thoát ra và tiếp tục tại nhiều điểm khác nhau. Chúng có thể được triển khai bằng câu lệnh :keyword:`async def`. Xem thêm
      :pep:`492`.

   coroutine function
   hàm coroutine
      Một hàm trả về một đối tượng :term:`coroutine`. Một hàm coroutine có thể được định nghĩa bằng câu lệnh :keyword:`async def`, và có thể chứa :keyword:`await`, :keyword:`async for`, và
      các từ khóa :keyword:`async with`. Những từ khóa này được giới thiệu trong :pep:`492`.

   CPython
      Cách triển khai chuẩn của ngôn ngữ lập trình Python, được phân phối trên `python.org <https://www.python.org>`_. Thuật ngữ "CPython" được sử dụng khi cần phân biệt cách triển khai này với các cách triển khai khác như Jython hoặc IronPython.

   current context
   ngữ cảnh hiện tại
      Đối tượng :term:`context` (đối tượng :class:`contextvars.Context`) hiện đang được các đối tượng :class:`~contextvars.ContextVar` sử dụng để truy cập (lấy hoặc đặt) các giá trị của :term:`biến ngữ cảnh <context variable>`. Mỗi thread có ngữ cảnh hiện tại riêng. Các framework dùng để thực thi các tác vụ bất đồng bộ (xem :mod:`asyncio`) liên kết mỗi tác vụ với một ngữ cảnh, ngữ cảnh này trở thành ngữ cảnh hiện tại mỗi khi tác vụ bắt đầu hoặc tiếp tục thực thi.

   cyclic isolate
   isolate tuần hoàn
      Một nhóm gồm một hoặc nhiều đối tượng tham chiếu lẫn nhau trong một chu kỳ tham chiếu, nhưng không được các đối tượng bên ngoài nhóm tham chiếu đến. Mục tiêu của :term:`bộ thu gom rác theo chu kỳ <garbage collection>` là xác định các nhóm này và phá vỡ các chu kỳ tham chiếu để có thể thu hồi bộ nhớ.

   data race
   điều kiện tranh chấp dữ liệu
      Một tình huống trong đó nhiều thread đồng thời truy cập cùng một vị trí bộ nhớ, ít nhất một trong các lần truy cập là thao tác ghi, và các thread không sử dụng bất kỳ cơ chế đồng bộ hóa nào để kiểm soát quyền truy cập. Data race dẫn đến hành vi :term:`non-deterministic` không xác định và có thể gây hỏng dữ liệu. Việc sử dụng đúng :term:`locks <lock>` và các :term:`primitive đồng bộ hóa <synchronization primitive>` khác sẽ ngăn ngừa data race. Lưu ý rằng data race chỉ có thể xảy ra trong native code, nhưng :term:`native code` có thể bị bộc lộ trong một Python API. Xem thêm :term:`race condition` và
      :term:`thread-safe`.

   deadlock
      Tình huống trong đó hai hoặc nhiều tác vụ (thread, process hoặc coroutine) chờ vô thời hạn để tác vụ khác giải phóng tài nguyên hoặc hoàn tất hành động, khiến không tác vụ nào có thể tiếp tục tiến triển. Ví dụ: nếu thread A giữ lock 1 và chờ lock 2, trong khi thread B giữ lock 2 và chờ lock 1, cả hai thread sẽ chờ vô thời hạn. Trong Python, tình trạng này thường phát sinh do việc lấy nhiều lock theo các thứ tự xung đột hoặc do các dependency join/await vòng tròn. Có thể tránh deadlock bằng cách luôn lấy nhiều :term:`lock <lock>` theo một thứ tự nhất quán. Xem thêm
      :term:`lock` và :term:`reentrant`.

   decorator
      Một hàm trả về một hàm khác, thường được áp dụng như một phép biến đổi hàm bằng cú pháp ``@wrapper``. Các ví dụ phổ biến về decorator là :deco:`classmethod` và :deco:`staticmethod`.

      Cú pháp decorator chỉ là syntactic sugar; hai định nghĩa hàm sau tương đương về mặt ngữ nghĩa::

         def f(arg):
             ...
         f = staticmethod(f)

         @staticmethod
         def f(arg):
             ...

      Khái niệm tương tự cũng tồn tại với class, nhưng ít được sử dụng hơn ở đó. Xem tài liệu về :ref:`định nghĩa hàm <function>` và
      :ref:`định nghĩa class <class>` để biết thêm về decorator.

   descriptor
      Bất kỳ đối tượng nào định nghĩa các phương thức :meth:`~object.__get__`,
      :meth:`~object.__set__`, hoặc :meth:`~object.__delete__`. Khi một thuộc tính của class là descriptor, hành vi liên kết đặc biệt của nó được kích hoạt khi tra cứu thuộc tính. Thông thường, việc sử dụng *a.b* để lấy, đặt hoặc xóa một thuộc tính sẽ tra cứu đối tượng có tên *b* trong từ điển của class đối với *a*, nhưng nếu *b* là một descriptor, phương thức descriptor tương ứng sẽ được gọi. Hiểu về descriptor là chìa khóa để hiểu sâu về Python vì chúng là nền tảng của nhiều tính năng, bao gồm hàm, phương thức, thuộc tính, class method, static method và tham chiếu đến các lớp cha.

      Để biết thêm thông tin về các phương thức của descriptor, hãy xem :ref:`descriptors` hoặc :ref:`Hướng dẫn về Descriptor <descriptorhowto>`.

   dictionary
   từ điển
      Một mảng kết hợp, trong đó các khóa tùy ý được ánh xạ tới các giá trị. Các khóa có thể là bất kỳ đối tượng nào có :meth:`~object.__hash__` và
      các phương thức :meth:`~object.__eq__`. Trong Perl, được gọi là hash.

   dictionary comprehension
   phép biên dịch từ điển
      Một cách ngắn gọn để xử lý toàn bộ hoặc một phần các phần tử trong một iterable và trả về một từ điển chứa kết quả. ``results = {n: n ** 2 for n in range(10)}`` tạo một từ điển trong đó khóa ``n`` được ánh xạ tới giá trị ``n ** 2``. Xem :ref:`comprehensions`.

   dictionary view
   view từ điển
      Các đối tượng được trả về từ :meth:`dict.keys`, :meth:`dict.values` và
      :meth:`dict.items` được gọi là dictionary view. Chúng cung cấp một chế độ xem động đối với các mục trong dictionary, nghĩa là khi dictionary thay đổi, chế độ xem sẽ phản ánh những thay đổi đó. Để buộc dictionary view trở thành một danh sách đầy đủ, hãy sử dụng ``list(dictview)``.  Xem
      :ref:`dict-views`.

   docstring
      Một string literal xuất hiện dưới dạng biểu thức đầu tiên trong một class, function hoặc module. Mặc dù bị bỏ qua khi suite được thực thi, nó vẫn được compiler nhận diện và đặt vào thuộc tính :attr:`~definition.__doc__` của class, function hoặc module bao quanh. Vì có thể truy cập thông qua introspection, đây là nơi chuẩn để ghi tài liệu cho đối tượng.

   duck-typing
      Một phong cách lập trình không xem xét type của một đối tượng để xác định xem nó có interface phù hợp hay không; thay vào đó, method hoặc attribute được gọi hoặc sử dụng trực tiếp ("Nếu nó trông giống vịt và kêu như vịt thì chắc chắn nó là vịt.") Bằng cách nhấn mạnh interface thay vì các type cụ thể, code được thiết kế tốt sẽ linh hoạt hơn nhờ cho phép thay thế đa hình. Duck-typing tránh các phép kiểm tra sử dụng :func:`type` hoặc
      :func:`isinstance`.  (Tuy nhiên, lưu ý rằng duck-typing có thể được bổ trợ bằng :term:`abstract base classes <abstract base class>`.)  Thay vào đó, nó thường sử dụng các phép kiểm tra :func:`hasattr` hoặc lập trình :term:`EAFP`.

   dunder
      Cách viết tắt không chính thức của "double underscore", được dùng khi nói về một
      :term:`special method`. Ví dụ, ``__init__`` thường được phát âm là "dunder init".

   EAFP
      Dễ xin tha thứ hơn là xin phép. Phong cách viết mã Python phổ biến này giả định rằng các khóa hoặc thuộc tính hợp lệ tồn tại và bắt các ngoại lệ nếu giả định đó không đúng. Phong cách gọn gàng và nhanh này được đặc trưng bởi sự xuất hiện của nhiều câu lệnh :keyword:`try` và :keyword:`except`. Kỹ thuật này đối lập với phong cách :term:`LBYL`, vốn phổ biến trong nhiều ngôn ngữ khác như C.

   evaluate function
   hàm evaluate
      Một hàm có thể được gọi để đánh giá một thuộc tính được đánh giá một cách trì hoãn của một đối tượng, chẳng hạn như giá trị của các bí danh kiểu được tạo bằng câu lệnh :keyword:`type`.

   exhausted
   đã cạn
      Một :term:`iterator` đã tạo ra tất cả các giá trị của nó được gọi là
      :dfn:`đã cạn`. Các nỗ lực tiếp theo để lấy giá trị kế tiếp (ví dụ: các lệnh gọi đến
      :func:`next`) sẽ gây ra :exc:`StopIteration` (hoặc :exc:`StopAsyncIteration` trong trường hợp một :term:`asynchronous iterator`).

   expression
   biểu thức
      Một phần cú pháp có thể được đánh giá để tạo ra một giá trị nào đó. Nói cách khác, một biểu thức là sự kết hợp của các phần tử biểu thức như giá trị chữ, tên, truy cập thuộc tính, toán tử hoặc lệnh gọi hàm, tất cả đều trả về một giá trị. Không phải mọi cấu trúc ngôn ngữ đều là biểu thức. Ngoài ra còn có :term:`statement`\s không thể được sử dụng như biểu thức, chẳng hạn như :keyword:`while`. Phép gán cũng là câu lệnh, không phải biểu thức.

   extension module
   mô-đun mở rộng
      Một module được viết bằng C hoặc C++, sử dụng C API của Python để tương tác với phần lõi và mã của người dùng.

   f-string
   f-strings
      Các string literal có tiền tố ``f`` hoặc ``F`` thường được gọi là "f-string", viết tắt của
      :ref:`chuỗi ký tự được định dạng <f-strings>`. Xem thêm :pep:`498`.

   file object
   đối tượng file
      Một đối tượng cung cấp API hướng đến file (với các phương thức như
      :meth:`!read` hoặc :meth:`!write`) tới một tài nguyên bên dưới. Tùy vào cách được tạo, một đối tượng tệp có thể trung gian hóa quyền truy cập vào một tệp thực trên đĩa hoặc vào một loại thiết bị lưu trữ hay thiết bị liên lạc khác (ví dụ: đầu vào/đầu ra tiêu chuẩn, bộ đệm trong bộ nhớ, socket, pipe, v.v.). Đối tượng tệp cũng được gọi là :dfn:`file-like objects` hoặc
      :dfn:`streams`.

      Thực tế có ba loại đối tượng tệp: tệp thô
      :term:`binary files <binary file>`, tệp nhị phân được đệm
      :term:`binary files <binary file>` và :term:`text files <text file>`. Các interface của chúng được định nghĩa trong module :mod:`io`. Cách chuẩn để tạo một đối tượng tệp là sử dụng hàm :func:`open`.

   file-like object
   đối tượng giống tệp
      Một từ đồng nghĩa của :term:`file object`.

   filesystem encoding and error handler
   bộ mã hóa hệ thống tệp và trình xử lý lỗi
      Bộ mã hóa và trình xử lý lỗi được Python sử dụng để giải mã byte từ hệ điều hành và mã hóa Unicode cho hệ điều hành.

      Bộ mã hóa hệ thống tệp phải bảo đảm giải mã thành công mọi byte nhỏ hơn 128. Nếu bộ mã hóa hệ thống tệp không cung cấp được bảo đảm này, các hàm API có thể phát sinh :exc:`UnicodeError`.

      :func:`sys.getfilesystemencoding` và
      Có thể sử dụng các hàm :func:`sys.getfilesystemencodeerrors` để lấy bộ mã hóa hệ thống tệp và trình xử lý lỗi.

      :term:`filesystem encoding and error handler` được cấu hình khi Python khởi động bằng hàm :c:func:`PyConfig_Read`: xem
      :c:member:`~PyConfig.filesystem_encoding` và
      :c:member:`~PyConfig.filesystem_errors` các thành viên của :c:type:`PyConfig`.

      Xem thêm :term:`locale encoding`.

   finder
   trình tìm kiếm
      Một đối tượng cố gắng tìm :term:`loader` cho một module đang được import.

      Có hai loại trình tìm kiếm: :term:`trình tìm kiếm meta path <meta path finder>` dùng với :data:`sys.meta_path`, và :term:`trình tìm kiếm path entry <path entry finder>` dùng với :data:`sys.path_hooks`.

      Xem :ref:`finders-and-loaders` và :mod:`importlib` để biết thêm nhiều chi tiết.

   floor division
   phép chia lấy phần nguyên
      Phép chia trong toán học làm tròn xuống đến số nguyên gần nhất. Toán tử phép chia lấy phần nguyên làm tròn xuống là ``//``. Ví dụ, biểu thức ``11 // 4`` cho kết quả là ``2``, trái với ``2.75`` được trả về bởi phép chia thực float. Lưu ý rằng ``(-11) // 4`` là ``-3`` vì đó là ``-2.75`` được làm tròn *xuống*. Xem :pep:`238`.

   free threading
   đa luồng tự do
      Mô hình luồng trong đó nhiều luồng có thể đồng thời chạy bytecode Python trong cùng một interpreter. Điều này trái ngược với :term:`global interpreter lock`, vốn chỉ cho phép một luồng thực thi bytecode Python tại một thời điểm. Xem :pep:`703`.

   bản build hỗ trợ đa luồng tự do

      Bản build của :term:`CPython` hỗ trợ :term:`free threading`, được cấu hình bằng tùy chọn :option:`--disable-gil` trước khi biên dịch.

      Xem :ref:`freethreading-python-howto`.

   free variable
   biến tự do
      Về mặt hình thức, theo định nghĩa trong :ref:`mô hình thực thi ngôn ngữ <bind_names>`, biến tự do là bất kỳ biến nào được sử dụng trong một namespace nhưng không phải là biến cục bộ trong namespace đó. Xem :term:`closure variable` để biết ví dụ. Về mặt thực tiễn, do tên của thuộc tính :attr:`codeobject.co_freevars`, thuật ngữ này đôi khi cũng được dùng như từ đồng nghĩa với :term:`closure variable`.

   function
   hàm
      Một chuỗi các câu lệnh trả về một giá trị cho bên gọi. Hàm cũng có thể nhận không hoặc nhiều :term:`đối số <argument>`, được sử dụng trong quá trình thực thi phần thân hàm. Xem thêm :term:`parameter`, :term:`method` và phần :ref:`function`.

   function annotation
   chú thích hàm
      Một :term:`annotation` của tham số hàm hoặc giá trị trả về.

      Chú thích hàm thường được dùng cho
      :term:`gợi ý kiểu <type hint>`: ví dụ, hàm này dự kiến sẽ nhận hai
      :class:`int` các đối số và cũng được kỳ vọng có giá trị trả về :class:`int`::

         def sum_two_numbers(a: int, b: int) -> int:
            return a + b

      Cú pháp chú thích hàm được giải thích trong phần :ref:`function`.

      Xem :term:`variable annotation` và :pep:`484`, là những phần mô tả chức năng này. Đồng thời xem :ref:`annotations-howto` để biết các phương pháp hay nhất khi làm việc với chú thích.

   __future__
      Một :ref:`câu lệnh future <future>`, ``from __future__ import <feature>``, hướng dẫn compiler biên dịch module hiện tại bằng cú pháp hoặc ngữ nghĩa sẽ trở thành tiêu chuẩn trong một bản phát hành Python tương lai. Module :mod:`__future__` ghi lại các giá trị có thể có của *tính năng*. Bằng cách import module này và đánh giá các biến của nó, bạn có thể biết khi nào một tính năng mới lần đầu được thêm vào ngôn ngữ và khi nào nó sẽ (hoặc đã) trở thành mặc định::

         >>> import __future__
         >>> __future__.division
         _Feature((2, 2, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0), 8192)

   garbage collection
      Quá trình giải phóng bộ nhớ khi không còn được sử dụng. Python thực hiện garbage collection thông qua reference counting và một cyclic garbage collector có khả năng phát hiện và phá vỡ các reference cycle. Garbage collector có thể được điều khiển bằng module :mod:`gc`.

      .. index:: single: generator

   generator
      Được dùng không chính thức để chỉ một :term:`generator function` hoặc một
      :term:`generator iterator`, tùy theo ngữ cảnh. Các thuật ngữ chính thức
      :term:`generator function` và :term:`generator iterator` hiếm khi được dùng trong thực tế; hầu như luôn chỉ cần dùng "generator".

      .. index:: single: generator function

   generator function
   hàm generator
      Một hàm trả về một đối tượng :term:`generator`. Hàm này trông giống như một hàm thông thường, ngoại trừ việc chứa các biểu thức :keyword:`yield` để tạo ra một chuỗi giá trị có thể sử dụng trong :keyword:`for`\-loop hoặc được lấy lần lượt từng giá trị bằng hàm :func:`next`. Xem :ref:`yieldexpr`.

   generator iterator
   iterator generator
      Một đối tượng được tạo bởi :term:`generator function` hoặc một
      :term:`generator expression`.

      Mỗi :keyword:`yield` tạm thời đình chỉ quá trình xử lý và ghi nhớ trạng thái thực thi (bao gồm các biến cục bộ và các câu lệnh try đang chờ xử lý). Khi *bộ lặp generator* tiếp tục, nó sẽ tiếp tục từ vị trí đã dừng (trái với các hàm, vốn bắt đầu lại từ đầu trong mỗi lần gọi).

      Các bộ lặp generator cũng triển khai phương thức :meth:`~generator.send` để truyền một giá trị vào generator đang tạm dừng, và
      phương thức :meth:`~generator.throw` để phát sinh một ngoại lệ tại vị trí generator bị tạm dừng.  Xem :ref:`generator-methods`.

      .. index:: single: generator expression

   generator expression
   biểu thức generator
      Một :term:`expression` trả về một :term:`iterator`.  Nó có dạng giống một biểu thức thông thường theo sau là mệnh đề :keyword:`!for` xác định một biến vòng lặp, một phạm vi và một mệnh đề :keyword:`!if` tùy chọn.  Biểu thức kết hợp này tạo ra các giá trị cho một hàm bao quanh::

         >>> sum(i*i for i in range(10))         # sum of squares 0, 1, 4, ... 81
         285

   generic function
   hàm generic
      Một hàm được tạo thành từ nhiều hàm triển khai cùng một phép toán cho các kiểu khác nhau. Việc sử dụng triển khai nào trong một lần gọi được xác định bởi thuật toán dispatch.

      Xem thêm mục thuật ngữ :term:`single dispatch`,
      decorator :deco:`functools.singledispatch` và :pep:`443`.

   generic type
   kiểu generic
      Một :term:`type` có thể được tham số hóa; thường là một
      :ref:`lớp container <sequence-types>` chẳng hạn như :class:`list` hoặc
      :class:`dict`. Được dùng cho :term:`type hints <type hint>` và
      :term:`annotations <annotation>`.

      Để biết thêm chi tiết, hãy xem :ref:`các kiểu bí danh generic <types-genericalias>`,
      :pep:`483`, :pep:`484`, :pep:`585`, và mô-đun :mod:`typing`.

   GIL
      Xem :term:`global interpreter lock`.

   global interpreter lock
   khóa trình thông dịch toàn cục
      Cơ chế được trình thông dịch :term:`CPython` sử dụng để đảm bảo rằng tại một thời điểm chỉ có một thread thực thi Python :term:`bytecode`. Điều này đơn giản hóa việc triển khai CPython bằng cách khiến mô hình đối tượng (bao gồm các kiểu dựng sẵn quan trọng như :class:`dict`) mặc nhiên an toàn trước việc truy cập đồng thời. Việc khóa toàn bộ trình thông dịch giúp trình thông dịch dễ hỗ trợ đa luồng hơn, nhưng phải đánh đổi phần lớn khả năng xử lý song song mà các máy đa bộ xử lý mang lại.

      Tuy nhiên, một số mô-đun mở rộng, dù là mô-đun tiêu chuẩn hay của bên thứ ba, được thiết kế để giải phóng GIL khi thực hiện các tác vụ đòi hỏi nhiều tính toán như nén hoặc băm. Ngoài ra, GIL luôn được giải phóng khi thực hiện I/O.

      Kể từ Python 3.13, có thể tắt GIL bằng cấu hình build :option:`--disable-gil`. Sau khi build Python với tùy chọn này, mã phải được chạy với :option:`-X gil=0 <-X>` hoặc sau khi đặt biến môi trường :envvar:`PYTHON_GIL=0 <PYTHON_GIL>`. Tính năng này cải thiện hiệu năng cho các ứng dụng đa luồng và giúp sử dụng CPU đa lõi hiệu quả hơn. Để biết thêm chi tiết, xem :pep:`703`.

      Trong các phiên bản trước của C API của Python, một hàm có thể khai báo rằng cần giữ GIL để sử dụng hàm đó. Điều này đề cập đến việc có một
      :term:`attached thread state`.

   global state
   trạng thái toàn cục
      Dữ liệu có thể được truy cập trong toàn bộ chương trình, chẳng hạn như các biến cấp mô-đun, biến lớp hoặc biến tĩnh C trong :term:`extension modules <extension module>`. Trong các chương trình đa luồng, trạng thái toàn cục được chia sẻ giữa các luồng thường yêu cầu cơ chế đồng bộ hóa để tránh
      :term:`race conditions <race condition>` và
      :term:`data races <data race>`.

   hash-based pyc
   pyc dựa trên hash
      Tệp bộ nhớ đệm bytecode sử dụng hash thay vì thời điểm sửa đổi lần cuối của tệp nguồn tương ứng để xác định tính hợp lệ của tệp. Xem
      :ref:`pyc-invalidation`.

   hashable
   có thể băm
      Một đối tượng là *có thể băm* nếu nó có một giá trị hash không bao giờ thay đổi trong suốt vòng đời của đối tượng đó (đối tượng cần có một phương thức :meth:`~object.__hash__`), và có thể được so sánh với các đối tượng khác (đối tượng cần có một phương thức :meth:`~object.__eq__`). Các đối tượng có thể băm mà được so sánh là bằng nhau phải có cùng giá trị hash.

      Tính có thể băm giúp một đối tượng có thể được sử dụng làm khóa dictionary và phần tử set, vì các cấu trúc dữ liệu này sử dụng giá trị hash internally.

      Hầu hết các đối tượng tích hợp bất biến của Python đều có thể băm; các container có thể thay đổi (chẳng hạn như list hoặc dictionary) thì không; các container bất biến (chẳng hạn như tuple và frozenset) chỉ có thể băm nếu các phần tử của chúng có thể băm. Các đối tượng là instance của các lớp do người dùng định nghĩa mặc định đều có thể băm. Chúng đều được so sánh là không bằng nhau (ngoại trừ với chính chúng), và giá trị hash của chúng được suy ra từ :func:`id`.

   IDLE
      Môi trường Tích hợp Phát triển và Học tập cho Python.
      :ref:`idle` là một môi trường biên tập và thông dịch cơ bản được cung cấp cùng với bản phân phối tiêu chuẩn của Python.

   immortal
   bất tử
      *Các đối tượng bất tử* là một chi tiết triển khai của CPython được giới thiệu trong :pep:`683`.

      Nếu một đối tượng là bất tử, :term:`reference count` của nó không bao giờ được sửa đổi, vì vậy nó không bao giờ được giải phóng trong khi trình thông dịch đang chạy. Ví dụ: :const:`True` và :const:`None` là các đối tượng bất tử trong CPython.

      Có thể xác định các đối tượng bất tử thông qua :func:`sys._is_immortal`, hoặc thông qua :c:func:`PyUnstable_IsImmortal` trong C API.

   immutable
   bất biến
      Một đối tượng có giá trị cố định. Các đối tượng bất biến bao gồm số, chuỗi và tuple. Một đối tượng như vậy không thể bị thay đổi. Phải tạo một đối tượng mới nếu cần lưu trữ một giá trị khác. Chúng đóng vai trò quan trọng ở những nơi cần một giá trị băm không đổi, chẳng hạn như làm khóa trong dictionary. Các đối tượng bất biến vốn dĩ là :term:`thread-safe` vì trạng thái của chúng không thể bị sửa đổi sau khi được tạo, loại bỏ các mối lo ngại về việc :term:`concurrent modification` không được đồng bộ hóa đúng cách.

   import path
      Danh sách các vị trí (hoặc các mục :term:`path entries <path entry>`) được :term:`path based finder` tìm kiếm để tìm các module cần import. Trong quá trình import, danh sách các vị trí này thường được lấy từ :data:`sys.path`, nhưng đối với subpackage, danh sách cũng có thể được lấy từ thuộc tính ``__path__`` của package cha.

   importing
      Quá trình cung cấp code Python trong một module cho code Python trong một module khác.

   importer
      Một đối tượng vừa tìm vừa tải một module; cả một
      Đối tượng :term:`finder` và :term:`loader`.

   index
   chỉ mục
      Một giá trị số biểu thị vị trí của một phần tử trong :term:`sequence`.

      Trong Python, việc lập chỉ mục bắt đầu từ số không. Ví dụ: ``things[0]`` đặt tên cho phần tử *đầu tiên* của ``things``; ``things[1]`` đặt tên cho phần tử thứ hai.

      Trong một số ngữ cảnh, Python cho phép sử dụng chỉ mục âm để đếm từ cuối sequence, đồng thời cho phép lập chỉ mục bằng :term:`slices <slice>`.

      Xem thêm :term:`subscript`.

   interactive
   tương tác
      Python có một trình thông dịch tương tác, nghĩa là bạn có thể nhập các câu lệnh và biểu thức tại dấu nhắc của trình thông dịch, thực thi chúng ngay lập tức và xem kết quả. Chỉ cần khởi chạy ``python`` mà không truyền đối số nào (có thể bằng cách chọn nó từ menu chính của máy tính). Đây là một cách rất mạnh để thử nghiệm các ý tưởng mới hoặc kiểm tra các module và package (hãy nhớ ``help(x)``). Để biết thêm về chế độ tương tác, xem :ref:`tut-interac`.

   interpreted
   được thông dịch
      Python là một ngôn ngữ được thông dịch, trái ngược với ngôn ngữ được biên dịch, mặc dù sự khác biệt này có thể không rõ ràng do có sự hiện diện của trình biên dịch bytecode. Điều này có nghĩa là các tệp mã nguồn có thể được chạy trực tiếp mà không cần tạo rõ ràng một tệp thực thi rồi chạy tệp đó. Các ngôn ngữ được thông dịch thường có chu kỳ phát triển/gỡ lỗi ngắn hơn so với các ngôn ngữ được biên dịch, mặc dù các chương trình của chúng nhìn chung cũng chạy chậm hơn. Xem thêm :term:`interactive`.

   interpreter shutdown
   quá trình tắt trình thông dịch
      Khi được yêu cầu tắt, trình thông dịch Python chuyển sang một giai đoạn đặc biệt, trong đó nó dần giải phóng tất cả tài nguyên đã cấp phát, chẳng hạn như các module và nhiều cấu trúc nội bộ quan trọng. Nó cũng thực hiện một số lần gọi đến :term:`bộ thu gom rác <garbage collection>`. Điều này có thể kích hoạt việc thực thi mã trong các destructor do người dùng định nghĩa hoặc callback weakref. Mã được thực thi trong giai đoạn tắt có thể gặp nhiều ngoại lệ khác nhau vì các tài nguyên mà mã phụ thuộc vào có thể không còn hoạt động (các ví dụ phổ biến là các module thư viện hoặc cơ chế warnings).

      Lý do chính để tắt trình thông dịch là module ``__main__`` hoặc tập lệnh đang được chạy đã thực thi xong.

   iterable
      Một đối tượng có khả năng trả về từng phần tử của nó. Các iterable bao gồm tất cả kiểu sequence (chẳng hạn như :class:`list`, :class:`str` và :class:`tuple`) và một số kiểu không phải sequence như :class:`dict`,
      :term:`file objects <file object>`, và các đối tượng thuộc bất kỳ lớp nào do bạn định nghĩa với một phương thức :meth:`~object.__iter__` hoặc với một
      :meth:`~object.__getitem__` method triển khai ngữ nghĩa của :term:`sequence`.

      Iterable có thể được sử dụng trong vòng lặp :keyword:`for` và ở nhiều nơi khác khi cần một sequence (:func:`zip`, :func:`map`, ...). Khi một đối tượng iterable được truyền làm đối số cho hàm dựng sẵn :func:`iter`, hàm này trả về một iterator cho đối tượng đó. Iterator này phù hợp để duyệt một lần qua tập hợp các giá trị. Khi sử dụng iterable, bạn thường không cần gọi
      :func:`iter` hoặc tự xử lý các đối tượng iterator. Câu lệnh :keyword:`for` tự động thực hiện việc đó cho bạn bằng cách tạo một biến tạm thời không tên để chứa iterator trong suốt thời gian vòng lặp. Xem thêm
      :term:`iterator`, :term:`sequence` và :term:`generator`.

   iterator
      Một đối tượng biểu diễn một luồng dữ liệu. Việc gọi lặp lại iterator
      :meth:`~iterator.__next__` method (hoặc truyền nó vào hàm dựng sẵn
      :func:`next`) sẽ trả về lần lượt các mục trong luồng. Khi không còn dữ liệu nào, một :exc:`StopIteration` exception sẽ được phát sinh. Tại thời điểm này, đối tượng iterator là :term:`exhausted` và mọi lần gọi tiếp theo đến
      :meth:`!__next__` method của nó chỉ lại phát sinh :exc:`StopIteration`. Iterator bắt buộc phải có một :meth:`~iterator.__iter__` method trả về chính đối tượng iterator, vì vậy mọi iterator cũng đều là iterable và có thể được sử dụng ở hầu hết những nơi chấp nhận các iterable khác. Một ngoại lệ đáng chú ý là mã thực hiện nhiều lượt lặp. Một đối tượng container (chẳng hạn như một
      :class:`list`) tạo ra một iterator mới mỗi khi bạn truyền nó vào hàm
      :func:`iter` dựng sẵn hoặc sử dụng nó trong vòng lặp :keyword:`for`. Nếu thử làm điều này với một iterator, thao tác đó sẽ chỉ trả về cùng đối tượng iterator đã cạn kiệt được sử dụng trong lượt lặp trước, khiến nó trông như một container rỗng.

      Có thể tìm thêm thông tin trong :ref:`typeiter`.

      .. impl-detail::

         CPython does not consistently apply the requirement that an iterator
         define :meth:`~iterator.__iter__`.
         And also please note that :term:`free-threaded <free threading>`
         CPython does not guarantee :term:`thread-safe` behavior of iterator
         operations.

   key
   khóa
      Một giá trị xác định một mục nhập trong một :term:`mapping`. Xem thêm :term:`subscript`.

   key function
   hàm khóa
      Hàm khóa hoặc hàm sắp thứ tự là một đối tượng có thể gọi, trả về một giá trị được dùng để sắp xếp hoặc sắp thứ tự. Ví dụ, :func:`locale.strxfrm` được dùng để tạo ra một khóa sắp xếp có xét đến các quy ước sắp xếp đặc thù theo ngôn ngữ.

      Một số công cụ trong Python chấp nhận các hàm khóa để kiểm soát cách các phần tử được sắp xếp hoặc nhóm lại. Chúng bao gồm :func:`min`, :func:`max`,
      :func:`sorted`, :meth:`list.sort`, :func:`heapq.merge`,
      :func:`heapq.nsmallest`, :func:`heapq.nlargest`, và
      :func:`itertools.groupby`.

      Có một số cách để tạo một hàm khóa. Ví dụ. hàm
      Phương thức :meth:`str.casefold` có thể dùng làm hàm khóa cho các phép sắp xếp không phân biệt chữ hoa chữ thường. Ngoài ra, có thể xây dựng hàm khóa từ một
      biểu thức :keyword:`lambda` chẳng hạn như ``lambda r: (r[0], r[2])``. Ngoài ra,
      :func:`operator.attrgetter`, :func:`operator.itemgetter`, và
      :func:`operator.methodcaller` là ba hàm khởi tạo hàm khóa. Xem :ref:`Sorting HOW TO <sortinghowto>` để biết ví dụ về cách tạo và sử dụng các hàm khóa.

   keyword argument
   đối số từ khóa
      Xem :term:`argument`.

   lambda
      Một hàm inline ẩn danh chỉ gồm một :term:`expression`, được đánh giá khi hàm được gọi. Cú pháp để tạo một hàm lambda là ``lambda [parameters]: expression``

   LBYL
      Look before you leap. Phong cách lập trình này kiểm tra rõ ràng các điều kiện tiên quyết trước khi thực hiện lệnh gọi hoặc tra cứu. Phong cách này trái ngược với phương pháp :term:`EAFP` và được nhận biết qua việc có nhiều
      câu lệnh :keyword:`if`.

      Trong môi trường đa luồng, phương pháp LBYL có thể dẫn đến nguy cơ xuất hiện
      :term:`race condition` giữa "việc nhìn" và "việc nhảy". Ví dụ, đoạn mã ``if key in mapping: return mapping[key]`` có thể thất bại nếu một thread khác xóa *key* khỏi *mapping* sau khi kiểm tra nhưng trước khi tra cứu. Vấn đề này có thể được giải quyết bằng cách sử dụng :term:`locks <lock>` hoặc sử dụng phương pháp
      :term:`EAFP`. Xem thêm :term:`thread-safe`.

   trình phân tích từ vựng

      Tên gọi chính thức của *tokenizer*; xem :term:`token`.

   list
   danh sách
      Một :term:`sequence` tích hợp sẵn của Python.  Mặc dù có tên như vậy, nó giống một mảng trong các ngôn ngữ khác hơn là một danh sách liên kết, vì việc truy cập các phần tử có độ phức tạp *O*\ (1).  Xem :ref:`time-complexity`.

   list comprehension
   biểu thức list comprehension
      Một cách ngắn gọn để xử lý toàn bộ hoặc một phần các phần tử trong một sequence và trả về một danh sách chứa kết quả.  ``result = ['{:#04x}'.format(x) for x in range(256) if x % 2 == 0]`` tạo ra một danh sách các chuỗi chứa những số hex (0x..) chẵn trong phạm vi từ 0 đến 255. Mệnh đề :keyword:`if` là tùy chọn.  Nếu bỏ qua, tất cả các phần tử trong ``range(256)`` sẽ được xử lý.

   lock
   khóa
      Một :term:`synchronization primitive` chỉ cho phép một thread tại một thời điểm truy cập vào tài nguyên dùng chung. Một thread phải acquire lock trước khi truy cập tài nguyên được bảo vệ và release lock sau đó. Nếu một thread cố gắng acquire một lock đang được thread khác giữ, nó sẽ bị block cho đến khi lock khả dụng. Module :mod:`threading` của Python cung cấp :class:`~threading.Lock` (một basic lock) và
      :class:`~threading.RLock` (một :term:`reentrant` lock). Lock được dùng để ngăn :term:`race conditions <race condition>` và bảo đảm
      :term:`thread-safe` quyền truy cập vào dữ liệu dùng chung. Có các design pattern thay thế cho lock, chẳng hạn như queue, producer/consumer pattern và thread-local state. Xem thêm :term:`deadlock` và :term:`reentrant`.

   lock-free
      Một operation không acquire bất kỳ :term:`lock` nào và sử dụng các instruction atomic của CPU để bảo đảm tính chính xác. Các operation lock-free có thể thực thi đồng thời mà không block lẫn nhau và không thể bị block bởi các operation đang giữ lock. Trong Python :term:`free-threaded <free threading>`, các built-in type như :class:`dict` và :class:`list` cung cấp các thao tác đọc lock-free, nghĩa là các thread khác có thể quan sát các trạng thái trung gian trong quá trình sửa đổi nhiều bước, ngay cả khi những sửa đổi đó giữ :term:`per-object lock`.

   loader
      Một object tải một module. Nó phải định nghĩa các method :meth:`!exec_module` và :meth:`!create_module` để triển khai interface :class:`~importlib.abc.Loader`. Một loader thường được trả về bởi một :term:`finder`. Xem thêm:

      * :ref:`finders-and-loaders`
      * :class:`importlib.abc.Loader`
      * :pep:`302`

   locale encoding
   mã hóa locale
      Trên Unix, đây là cách mã hóa của locale LC_CTYPE. Có thể thiết lập bằng
      :func:`locale.setlocale(locale.LC_CTYPE, new_locale) <locale.setlocale>`.

      Trên Windows, đây là trang mã ANSI (ví dụ: ``"cp1252"``).

      Trên Android và VxWorks, Python sử dụng ``"utf-8"`` làm mã hóa locale.

      Có thể sử dụng :func:`locale.getencoding` để lấy mã hóa locale.

      Xem thêm :term:`filesystem encoding and error handler`.

   magic method
   phương thức ma thuật
      .. index:: pair: magic; method

      Một từ đồng nghĩa không trang trọng của :term:`special method`.

   mapping
   ánh xạ
      Một đối tượng container hỗ trợ tra cứu khóa tùy ý và triển khai các phương thức được chỉ định trong :class:`collections.abc.Mapping` hoặc
      :class:`collections.abc.MutableMapping`
      :ref:`các lớp cơ sở trừu tượng <collections-abstract-base-classes>`. Ví dụ bao gồm :class:`dict`, :class:`collections.defaultdict`,
      :class:`collections.OrderedDict` và :class:`collections.Counter`.

   meta path finder
      Một :term:`finder` được trả về khi tìm kiếm :data:`sys.meta_path`. Meta path finder có liên quan đến, nhưng khác với :term:`path entry finder <path entry finder>`.

      Xem :class:`importlib.abc.MetaPathFinder` để biết các phương thức mà các trình tìm kiếm meta path triển khai.

   metaclass
   siêu lớp
      Lớp của một lớp. Các định nghĩa lớp tạo ra một tên lớp, một từ điển lớp và một danh sách các lớp cơ sở. Siêu lớp chịu trách nhiệm nhận ba đối số đó và tạo lớp. Hầu hết các ngôn ngữ lập trình hướng đối tượng đều cung cấp một triển khai mặc định. Điểm đặc biệt của Python là bạn có thể tạo các siêu lớp tùy chỉnh. Hầu hết người dùng không bao giờ cần đến công cụ này, nhưng khi cần, siêu lớp có thể cung cấp các giải pháp mạnh mẽ và thanh lịch. Chúng đã được sử dụng để ghi nhật ký việc truy cập thuộc tính, bổ sung tính an toàn luồng, theo dõi việc tạo đối tượng, triển khai singleton và nhiều tác vụ khác.

      Có thể tìm thêm thông tin trong :ref:`metaclasses`.

   method
   phương thức
      Một hàm được định nghĩa bên trong thân lớp. Nếu được gọi như một thuộc tính của một thực thể thuộc lớp đó, phương thức sẽ nhận đối tượng thực thể làm :term:`argument` đầu tiên (thường được gọi là ``self``). Xem :term:`function` và :term:`nested scope`.

   method resolution order
   thứ tự phân giải phương thức
      Thứ tự phân giải phương thức là thứ tự các lớp cơ sở được tìm kiếm để tìm một thành viên trong quá trình tra cứu. Xem :ref:`python_2.3_mro` để biết chi tiết về thuật toán được trình thông dịch Python sử dụng kể từ bản phát hành 2.3.

   module
   mô-đun
      Một đối tượng đóng vai trò là đơn vị tổ chức của mã Python. Mô-đun có một namespace chứa các đối tượng Python tùy ý. Mô-đun được nạp vào Python bằng quá trình :term:`importing`.

      Xem thêm :term:`package`.

   module spec
   đặc tả mô-đun
      Một namespace chứa thông tin liên quan đến việc import được sử dụng để nạp một mô-đun. Một thể hiện của :class:`importlib.machinery.ModuleSpec`.

      Xem thêm :ref:`module-specs`.

   MRO
      Xem :term:`method resolution order`.

   mutable
      Một :term:`object` có trạng thái được phép thay đổi trong suốt quá trình chạy của chương trình. Trong các chương trình đa luồng, những đối tượng mutable được chia sẻ giữa các luồng cần được đồng bộ hóa cẩn thận để tránh
      :term:`race conditions <race condition>`. Xem thêm :term:`immutable`,
      :term:`thread-safe`, và :term:`concurrent modification`.

   named tuple
      Thuật ngữ "named tuple" áp dụng cho mọi kiểu hoặc lớp kế thừa từ tuple và có các phần tử có thể truy cập bằng chỉ mục đồng thời cũng có thể truy cập bằng các thuộc tính có tên. Kiểu hoặc lớp đó cũng có thể có thêm các tính năng khác.

      Một số kiểu dựng sẵn là named tuple, bao gồm các giá trị được trả về bởi :func:`time.localtime` và :func:`os.stat`. Một ví dụ khác là
      :data:`sys.float_info`::

           >>> sys.float_info[1]                   # indexed access
           1024
           >>> sys.float_info.max_exp              # named field access
           1024
           >>> isinstance(sys.float_info, tuple)   # kind of tuple
           True

      Một số named tuple là các kiểu dựng sẵn (chẳng hạn như những ví dụ trên). Ngoài ra, có thể tạo named tuple từ một định nghĩa lớp thông thường kế thừa từ :class:`tuple` và định nghĩa các trường có tên. Có thể viết lớp như vậy thủ công, hoặc tạo lớp bằng cách kế thừa :class:`typing.NamedTuple`, hoặc bằng hàm factory
      :func:`collections.namedtuple`. Các kỹ thuật sau cũng bổ sung một số phương thức có thể không có trong các named tuple được viết thủ công hoặc dựng sẵn.

   namespace
   không gian tên
      Nơi lưu trữ một biến. Không gian tên được triển khai dưới dạng các từ điển. Có các không gian tên cục bộ, toàn cục và dựng sẵn, cũng như các không gian tên lồng nhau trong các đối tượng (trong các phương thức). Không gian tên hỗ trợ tính mô-đun bằng cách ngăn ngừa xung đột tên. Ví dụ, các hàm
      :func:`builtins.open <.open>` và :func:`os.open` được phân biệt bằng không gian tên của chúng. Không gian tên cũng giúp mã dễ đọc và dễ bảo trì hơn bằng cách làm rõ mô-đun nào triển khai một hàm. Ví dụ, viết
      :func:`random.seed` hoặc :func:`itertools.islice` cho thấy rõ rằng các hàm đó lần lượt được triển khai bởi các module :mod:`random` và :mod:`itertools`.

   namespace package
   gói namespace
      Một :term:`package` chỉ đóng vai trò là vùng chứa cho các subpackage. Các gói namespace có thể không có biểu diễn vật lý và cụ thể không giống như một :term:`regular package` vì chúng không có tệp ``__init__.py``.

      Các gói namespace cho phép nhiều package có thể cài đặt riêng lẻ dùng chung một package cha. Nếu không, bạn nên sử dụng :term:`regular package`.

      Để biết thêm thông tin, hãy xem :pep:`420` và :ref:`reference-namespace-package`.

      Xem thêm :term:`module`.

   native code
   mã native
      Mã được biên dịch thành các chỉ thị máy và chạy trực tiếp trên bộ xử lý, trái ngược với mã được thông dịch hoặc chạy trong máy ảo. Trong ngữ cảnh Python, mã native thường đề cập đến mã C, C++, Rust hoặc Fortran trong các :term:`extension modules <extension module>` có thể được gọi từ Python. Xem thêm :term:`extension module`.

   nested scope
   phạm vi lồng nhau
      Khả năng tham chiếu đến một biến trong một định nghĩa bao quanh. Chẳng hạn, một hàm được định nghĩa bên trong một hàm khác có thể tham chiếu đến các biến trong hàm bên ngoài. Lưu ý rằng theo mặc định, phạm vi lồng nhau chỉ hoạt động đối với việc tham chiếu, không phải phép gán. Các biến cục bộ được đọc và ghi trong phạm vi gần nhất. Tương tự, các biến toàn cục được đọc và ghi vào namespace toàn cục. :keyword:`nonlocal` cho phép ghi vào các phạm vi bên ngoài.

   new-style class
   lớp kiểu mới
      Tên gọi cũ của loại lớp hiện được dùng cho mọi đối tượng lớp. Trong các phiên bản Python trước đây, chỉ các lớp kiểu mới mới có thể sử dụng những tính năng mới hơn, linh hoạt của Python như :attr:`~object.__slots__`, descriptor, property, :meth:`~object.__getattribute__`, class method và static method.

   non-deterministic
   không tất định
      Hành vi trong đó kết quả của một chương trình có thể thay đổi giữa các lần thực thi với cùng đầu vào. Trong các chương trình đa luồng, hành vi không tất định thường xuất phát từ :term:`race conditions <race condition>`, trong đó thời điểm tương đối hoặc sự đan xen của các luồng ảnh hưởng đến kết quả. Việc đồng bộ hóa đúng cách bằng :term:`locks <lock>` và các
      :term:`các nguyên thủy đồng bộ hóa <synchronization primitive>` giúp đảm bảo hành vi mang tính xác định.

   object
   đối tượng
      Bất kỳ dữ liệu nào có trạng thái (thuộc tính hoặc giá trị) và hành vi được xác định (các phương thức). Cũng là lớp cơ sở tối thượng của mọi :term:`new-style class`.

   optimized scope
   phạm vi tối ưu hóa
      Phạm vi mà trong đó tên biến cục bộ đích được trình biên dịch biết một cách đáng tin cậy khi mã được biên dịch, cho phép tối ưu hóa quyền truy cập đọc và ghi vào các tên này. Các namespace cục bộ của hàm, generator, coroutine, comprehension và biểu thức generator được tối ưu hóa theo cách này. Lưu ý: hầu hết các tối ưu hóa của trình thông dịch được áp dụng cho mọi phạm vi; chỉ những tối ưu hóa dựa trên một tập hợp tên biến cục bộ và nonlocal đã biết mới bị giới hạn trong các phạm vi tối ưu hóa.

   optional module
   mô-đun tùy chọn
      Một :term:`extension module` là một phần của :term:`standard library`, nhưng có thể không có trong một số bản dựng của :term:`CPython`, thường do thiếu thư viện bên thứ ba hoặc vì mô-đun này không khả dụng trên một nền tảng nhất định.

      Xem :ref:`optional-module-requirements` để biết danh sách các mô-đun tùy chọn yêu cầu thư viện của bên thứ ba.

   package
   gói
      Một :term:`module` trong Python có thể chứa các submodule hoặc, theo cách đệ quy, các subpackage. Về mặt kỹ thuật, package là một Python module có thuộc tính ``__path__``.

      Xem thêm :term:`regular package` và :term:`namespace package`.

   parallelism
   tính song song
      Thực thi nhiều thao tác cùng một lúc (ví dụ: trên nhiều lõi CPU). Trong các bản dựng Python có
      :term:`global interpreter lock (GIL) <global interpreter lock>`, mỗi lần chỉ có một thread chạy bytecode Python, vì vậy việc tận dụng nhiều lõi CPU thường cần nhiều process (ví dụ: :mod:`multiprocessing`) hoặc các phần mở rộng native giải phóng GIL. Trong Python :term:`free-threaded <free threading>`, nhiều thread Python có thể chạy mã Python đồng thời trên các lõi khác nhau.

   parameter
   tham số
      Một thực thể có tên trong định nghĩa :term:`function` (hoặc phương thức), chỉ định một :term:`argument` (hoặc trong một số trường hợp là các đối số) mà hàm có thể chấp nhận. Có năm loại tham số:

      * :dfn:`positional-or-keyword`: chỉ định một đối số có thể được truyền :term:`theo vị trí <argument>` hoặc dưới dạng :term:`đối số từ khóa <argument>`. Đây là loại tham số mặc định, chẳng hạn như *foo* và *bar* trong phần sau::

           def func(foo, bar=None): ...

      .. _positional-only_parameter:

      * :dfn:`positional-only`: chỉ định một đối số chỉ có thể được cung cấp theo vị trí. Có thể định nghĩa các tham số chỉ theo vị trí bằng cách thêm một ký tự ``/`` vào danh sách tham số của định nghĩa hàm, sau chúng; chẳng hạn như *posonly1* và *posonly2* trong phần sau::

           def func(posonly1, posonly2, /, positional_or_keyword): ...

      .. _keyword-only_parameter:

      * :dfn:`keyword-only`: chỉ định một đối số chỉ có thể được cung cấp bằng từ khóa. Có thể định nghĩa các tham số chỉ theo từ khóa bằng cách thêm một tham số var-positional duy nhất hoặc ``*`` trống vào danh sách tham số của định nghĩa hàm, trước chúng; chẳng hạn như *kw_only1* và *kw_only2* trong phần sau::

           def func(arg, *, kw_only1, kw_only2): ...

      * :dfn:`var-positional`: chỉ định rằng có thể cung cấp một chuỗi tùy ý các đối số theo vị trí (bổ sung cho mọi đối số theo vị trí đã được các tham số khác chấp nhận). Có thể định nghĩa tham số như vậy bằng cách thêm ``*`` vào trước tên tham số, chẳng hạn như *args* trong phần sau::

           def func(*args, **kwargs): ...

      * :dfn:`var-keyword`: chỉ định rằng có thể cung cấp tùy ý nhiều đối số từ khóa (bổ sung cho mọi đối số từ khóa đã được các tham số khác chấp nhận). Có thể định nghĩa tham số như vậy bằng cách thêm ``**`` vào trước tên tham số, chẳng hạn như *kwargs* trong ví dụ trên.

      Tham số có thể chỉ định cả đối số tùy chọn và bắt buộc, cũng như các giá trị mặc định cho một số đối số tùy chọn.

      Xem thêm mục từ :term:`argument` trong bảng thuật ngữ, câu hỏi thường gặp về
      :ref:`sự khác biệt giữa đối số và tham số <faq-argument-vs-parameter>`, lớp :class:`inspect.Parameter`, và
      mục :ref:`function`, và :pep:`362`.

   per-object lock
   khóa cho từng đối tượng
      Một :term:`lock` được liên kết với một thực thể đối tượng riêng lẻ thay vì một khóa toàn cục được chia sẻ giữa tất cả các đối tượng. Trong Python :term:`free-threaded <free threading>`, các kiểu dựng sẵn như :class:`dict` và
      :class:`list` sử dụng khóa cho từng đối tượng để cho phép các thao tác đồng thời trên những đối tượng khác nhau, đồng thời tuần tự hóa các thao tác trên cùng một đối tượng. Các thao tác đang giữ khóa cho từng đối tượng sẽ ngăn những thao tác khóa khác trên cùng đối tượng tiếp tục, nhưng không chặn các thao tác :term:`lock-free`.

   path entry
   mục nhập đường dẫn
      Một vị trí duy nhất trên :term:`import path` mà :term:`path based finder` tra cứu để tìm các module cần import.

   path entry finder
   trình tìm mục nhập đường dẫn
      Một :term:`finder` được trả về bởi một callable trên :data:`sys.path_hooks` (tức là một :term:`path entry hook`) có khả năng định vị các module khi được cung cấp một :term:`path entry`.

      Xem :class:`importlib.abc.PathEntryFinder` để biết các phương thức mà trình tìm mục nhập đường dẫn triển khai.

   path entry hook
   hook mục nhập đường dẫn
      Một callable trong danh sách :data:`sys.path_hooks` trả về một :term:`path entry finder` nếu nó biết cách tìm các module trên một :term:`path entry` cụ thể.

   path based finder
   trình tìm kiếm dựa trên đường dẫn
      Một trong các :term:`trình tìm kiếm meta path <meta path finder>` mặc định, tìm kiếm một :term:`import path` để tìm các mô-đun.

   path-like object
   đối tượng dạng đường dẫn
      Một đối tượng biểu diễn một đường dẫn trong hệ thống tệp. Đối tượng dạng đường dẫn là một đối tượng :class:`str` hoặc :class:`bytes` biểu diễn một đường dẫn, hoặc một đối tượng triển khai giao thức :class:`os.PathLike`. Một đối tượng hỗ trợ giao thức :class:`os.PathLike` có thể được chuyển đổi thành một đường dẫn hệ thống tệp :class:`str` hoặc
      :class:`bytes` bằng cách gọi hàm :func:`os.fspath`;
      :func:`os.fsdecode` và :func:`os.fsencode` có thể được dùng để đảm bảo kết quả là
      :class:`str` hoặc :class:`bytes` tương ứng. Được giới thiệu bởi :pep:`519`.

   PEP
      Đề xuất cải tiến Python. PEP là một tài liệu thiết kế cung cấp thông tin cho cộng đồng Python hoặc mô tả một tính năng mới cho Python, hay cho các quy trình hoặc môi trường của Python. PEP cần cung cấp đặc tả kỹ thuật súc tích và cơ sở lý luận cho các tính năng được đề xuất.

      PEP được dùng làm cơ chế chính để đề xuất các tính năng mới lớn, thu thập ý kiến đóng góp của cộng đồng về một vấn đề và ghi lại các quyết định thiết kế đã được đưa ra cho Python. Tác giả PEP chịu trách nhiệm xây dựng sự đồng thuận trong cộng đồng và ghi lại các ý kiến bất đồng.

      Xem :pep:`1`.

   portion
   phần
      Một tập hợp các tệp trong cùng một thư mục (có thể được lưu trữ trong tệp zip) đóng góp vào một namespace package, như được định nghĩa trong :pep:`420`.

   positional argument
   đối số vị trí
      Xem :term:`argument`.

   provisional API
   API tạm thời
      API tạm thời là API đã được cố ý loại khỏi các đảm bảo tương thích ngược của thư viện chuẩn. Mặc dù không dự kiến sẽ có những thay đổi lớn đối với các giao diện như vậy, miễn là chúng được đánh dấu là tạm thời, các thay đổi không tương thích ngược (bao gồm cả việc loại bỏ giao diện) vẫn có thể xảy ra nếu các nhà phát triển cốt lõi thấy cần thiết. Những thay đổi như vậy sẽ không được thực hiện tùy tiện -- chúng chỉ xảy ra nếu phát hiện các lỗi nghiêm trọng mang tính nền tảng mà trước khi đưa API vào thư viện đã không được phát hiện.

      Ngay cả đối với các API tạm thời, những thay đổi không tương thích ngược vẫn được xem là "giải pháp cuối cùng" - mọi nỗ lực vẫn sẽ được thực hiện để tìm ra phương án tương thích ngược cho mọi vấn đề đã được xác định.

      Quy trình này cho phép thư viện chuẩn tiếp tục phát triển theo thời gian mà không bị ràng buộc bởi các lỗi thiết kế có vấn đề trong những khoảng thời gian dài. Xem :pep:`411` để biết thêm chi tiết.

   provisional package
   gói tạm thời
      Xem :term:`provisional API`.

   Python 3000
      Biệt danh cho dòng bản phát hành Python 3.x (được đặt ra từ lâu, khi việc phát hành phiên bản 3 vẫn còn là chuyện của tương lai xa.) Tên này cũng được viết tắt là "Py3k".

   Pythonic
      Một ý tưởng hoặc đoạn mã tuân theo sát nhất các idiom phổ biến của ngôn ngữ Python, thay vì triển khai mã bằng những khái niệm thường dùng trong các ngôn ngữ khác. Ví dụ, một idiom phổ biến trong Python là lặp qua tất cả các phần tử của một iterable bằng câu lệnh :keyword:`for`. Nhiều ngôn ngữ khác không có kiểu cấu trúc này, nên những người chưa quen với Python đôi khi sử dụng một bộ đếm số thay thế::

          for i in range(len(food)):
              print(food[i])

      Trái ngược với phương pháp Pythonic gọn gàng hơn::

         for piece in food:
             print(piece)

   qualified name
   tên đủ điều kiện
      Một tên có dấu chấm thể hiện "đường dẫn" từ phạm vi toàn cục của một module đến một class, function hoặc method được định nghĩa trong module đó, như được định nghĩa trong
      :pep:`3155`. Đối với các hàm và lớp cấp cao nhất, tên đủ điều kiện giống với tên của đối tượng::

         >>> class C:
         ...     class D:
         ...         def meth(self):
         ...             pass
         ...
         >>> C.__qualname__
         'C'
         >>> C.D.__qualname__
         'C.D'
         >>> C.D.meth.__qualname__
         'C.D.meth'

      Khi được dùng để chỉ các module, *tên đầy đủ* có nghĩa là toàn bộ đường dẫn phân tách bằng dấu chấm đến module, bao gồm mọi package cha, ví dụ: ``email.mime.text``::

         >>> import email.mime.text
         >>> email.mime.text.__name__
         'email.mime.text'

   race condition
   điều kiện tranh đua
      Trạng thái của chương trình trong đó hành vi phụ thuộc vào thời điểm tương đối hoặc thứ tự của các sự kiện, đặc biệt là trong các chương trình đa luồng. Điều kiện tranh đua có thể dẫn đến
      :term:`non-deterministic` hành vi và các lỗi khó tái hiện. Một :term:`data race` là một loại điều kiện tranh đua cụ thể liên quan đến việc truy cập bộ nhớ dùng chung mà không được đồng bộ hóa. Phong cách viết mã :term:`LBYL` đặc biệt dễ phát sinh điều kiện tranh đua trong mã đa luồng. Việc sử dụng :term:`khóa <lock>` và các
      :term:`primitive đồng bộ hóa <synchronization primitive>` khác giúp ngăn ngừa điều kiện tranh đua.

   reference count
   bộ đếm tham chiếu
      Số lượng tham chiếu đến một đối tượng. Khi số lượng tham chiếu của một đối tượng giảm xuống bằng không, đối tượng đó sẽ được giải phóng. Một số đối tượng là
      :term:`immortal` và có số lượng tham chiếu không bao giờ được thay đổi, do đó các đối tượng này không bao giờ được giải phóng. Việc đếm tham chiếu thường không hiển thị trong mã Python, nhưng là một thành phần quan trọng của
      :term:`CPython` implementation. Lập trình viên có thể gọi hàm
      :func:`sys.getrefcount` để trả về số lượng tham chiếu của một đối tượng cụ thể.

      Trong :term:`CPython`, số lượng tham chiếu không được xem là các giá trị ổn định hoặc được định nghĩa rõ ràng; số lượng tham chiếu đến một đối tượng và cách mã Python ảnh hưởng đến số lượng đó có thể khác nhau giữa các phiên bản.

   regular package
   gói thông thường
      Một :term:`package` truyền thống, chẳng hạn như một thư mục chứa tệp ``__init__.py``.

      Xem thêm :term:`namespace package`.

   reentrant
      Thuộc tính của một hàm hoặc :term:`lock` cho phép nó được gọi hoặc thu nhận nhiều lần bởi cùng một thread mà không gây ra lỗi hoặc một
      :term:`deadlock`.

      Đối với các hàm, tính reentrant nghĩa là hàm có thể được gọi lại một cách an toàn trước khi lần gọi trước đó hoàn tất, điều này rất quan trọng khi các hàm có thể được gọi đệ quy hoặc từ các signal handler. Các hàm không an toàn với thread có thể là :term:`non-deterministic` nếu chúng được gọi reentrant trong một chương trình đa thread.

      Đối với lock, :class:`threading.RLock` của Python (reentrant lock) có tính reentrant, nghĩa là một thread đang giữ lock có thể thu nhận lock đó lần nữa mà không bị chặn. Ngược lại, :class:`threading.Lock` không có tính reentrant - việc cố gắng thu nhận nó hai lần từ cùng một thread sẽ gây ra deadlock.

      Xem thêm :term:`lock` và :term:`deadlock`.

   REPL
      Từ viết tắt của "vòng lặp read–eval–print", một tên gọi khác của
      :term:`interactive` shell của trình thông dịch.

   __slots__
      Một khai báo bên trong một lớp giúp tiết kiệm bộ nhớ bằng cách khai báo trước không gian cho các thuộc tính của instance và loại bỏ các dictionary của instance. Mặc dù phổ biến, kỹ thuật này khá khó triển khai chính xác và tốt nhất chỉ nên dùng trong những trường hợp hiếm hoi khi có số lượng lớn instance trong một ứng dụng bị giới hạn nghiêm ngặt về bộ nhớ.

   sequence
      Một :term:`iterable` hỗ trợ truy cập phần tử hiệu quả bằng các chỉ số nguyên thông qua phương thức đặc biệt :meth:`~object.__getitem__` và định nghĩa một
      phương thức :meth:`~object.__len__` trả về độ dài của sequence. Một số kiểu sequence tích hợp sẵn là :class:`list`, :class:`str`,
      :class:`tuple`, và :class:`bytes`. Lưu ý rằng :class:`dict` cũng hỗ trợ :meth:`~object.__getitem__` và :meth:`!__len__`, nhưng được xem là một mapping thay vì một sequence vì các phép tra cứu sử dụng các khóa tùy ý
      :term:`hashable` thay vì số nguyên.

      Lớp cơ sở trừu tượng :class:`collections.abc.Sequence` định nghĩa một interface phong phú hơn nhiều, vượt xa việc chỉ
      :meth:`~object.__getitem__` và :meth:`~object.__len__`, đồng thời bổ sung
      :meth:`~sequence.count`, :meth:`~sequence.index`,
      :meth:`~object.__contains__`, và :meth:`~object.__reversed__`. Các kiểu triển khai interface mở rộng này có thể được đăng ký rõ ràng bằng cách sử dụng
      :func:`~abc.ABCMeta.register`. Để xem thêm tài liệu về các phương thức sequence nói chung, hãy xem
      :ref:`Các thao tác sequence phổ biến <typesseq-common>`.

   set comprehension
   phép dựng set
      Một cách ngắn gọn để xử lý toàn bộ hoặc một phần các phần tử trong một iterable và trả về một set chứa các kết quả. ``results = {c for c in 'abracadabra' if c not in 'abc'}`` tạo ra set các chuỗi ``{'r', 'd'}``.  Xem
      :ref:`comprehensions`.

   single dispatch
   dispatch đơn
      Một dạng dispatch :term:`generic function` trong đó implementation được chọn dựa trên kiểu của một đối số duy nhất.

   slice
      Một đối tượng thuộc kiểu :class:`slice`, dùng để mô tả một phần của :term:`sequence`. Đối tượng slice được tạo khi sử dụng dạng :ref:`slicing <slicings>` của :ref:`subscript notation <subscriptions>`, với dấu hai chấm bên trong dấu ngoặc vuông, chẳng hạn như trong ``variable_name[1:3:5]``.

   soft deprecated
      Không nên sử dụng API đã bị soft deprecated trong mã mới, nhưng mã hiện có sử dụng API này vẫn an toàn. API vẫn được ghi tài liệu và kiểm thử, nhưng sẽ không được cải tiến thêm.

      Khác với deprecation thông thường, soft deprecation không có kế hoạch xóa API và sẽ không phát cảnh báo.

      Xem `PEP 387: Soft Deprecation <https://peps.python.org/pep-0387/#soft-deprecation>`_.

   special method
   phương thức đặc biệt
      .. index:: pair: special; method

      Một phương thức được Python gọi ngầm để thực hiện một thao tác nhất định trên một kiểu, chẳng hạn như phép cộng. Những phương thức này có tên bắt đầu và kết thúc bằng hai dấu gạch dưới. Các phương thức đặc biệt được ghi tài liệu tại
      :ref:`specialnames`.

   standard library
   thư viện chuẩn
      Tập hợp các :term:`packages <package>`, :term:`modules <module>` và :term:`extension modules <extension module>` được phân phối như một phần của gói trình thông dịch Python chính thức. Thành phần chính xác của tập hợp này có thể thay đổi tùy theo nền tảng, các thư viện hệ thống hiện có hoặc những tiêu chí khác. Tài liệu có tại :ref:`library-index`.

      Xem thêm :data:`sys.stdlib_module_names` để biết danh sách tất cả các tên mô-đun thư viện chuẩn có thể có.

   statement
   câu lệnh
      Câu lệnh là một phần của một suite (một "khối" mã). Câu lệnh có thể là một :term:`expression` hoặc một trong số các cấu trúc có từ khóa, chẳng hạn như :keyword:`if`, :keyword:`while` hoặc :keyword:`for`.

   static type checker
   trình kiểm tra kiểu tĩnh
      Một công cụ bên ngoài đọc và phân tích mã Python, tìm các vấn đề như kiểu không chính xác. Xem thêm :term:`type hints <type hint>` và mô-đun :mod:`typing`.

   stdlib
      Viết tắt của :term:`standard library`.

   steal
   đánh cắp
      Trong C API của Python, “*stealing*” một đối số có nghĩa là quyền sở hữu đối số đó được chuyển cho hàm được gọi. Bên gọi không được sử dụng tham chiếu đó sau khi gọi. Nhìn chung, các hàm “đánh cắp” một đối số vẫn làm như vậy ngay cả khi chúng thất bại.

      Xem :ref:`api-refcountdetails` để biết giải thích đầy đủ.

   strong reference
   tham chiếu mạnh
      Trong C API của Python, tham chiếu mạnh là tham chiếu đến một đối tượng do mã đang giữ tham chiếu đó sở hữu. Tham chiếu mạnh được tạo bằng cách gọi :c:func:`Py_INCREF` khi tham chiếu được tạo và được giải phóng bằng :c:func:`Py_DECREF` khi tham chiếu bị xóa.

      Có thể sử dụng hàm :c:func:`Py_NewRef` để tạo tham chiếu mạnh đến một đối tượng. Thông thường, phải gọi hàm :c:func:`Py_DECREF` trên tham chiếu mạnh trước khi thoát khỏi phạm vi của tham chiếu mạnh, để tránh làm rò rỉ một tham chiếu.

      Xem thêm :term:`borrowed reference`.

   subscript
   chỉ số dưới
      Biểu thức trong dấu ngoặc vuông của một
      :ref:`biểu thức subscription <subscriptions>`, chẳng hạn như ``3`` trong ``items[3]``. Thường được dùng để chọn một phần tử của một container. Còn được gọi là :term:`key` khi dùng chỉ số dưới với một :term:`mapping`, hoặc là :term:`index` khi dùng chỉ số dưới với một :term:`sequence`.

   synchronization primitive
   primitive đồng bộ hóa
      Một khối xây dựng cơ bản để điều phối (đồng bộ hóa) việc thực thi của nhiều thread nhằm bảo đảm :term:`thread-safe` quyền truy cập vào các tài nguyên dùng chung. Module :mod:`threading` của Python cung cấp một số synchronization primitive, bao gồm :class:`~threading.Lock`, :class:`~threading.RLock`,
      :class:`~threading.Semaphore`, :class:`~threading.Condition`,
      :class:`~threading.Event`, và :class:`~threading.Barrier`. Ngoài ra, module :mod:`queue` cung cấp các hàng đợi multi-producer, multi-consumer, đặc biệt hữu ích trong các chương trình đa thread. Các primitive này giúp ngăn ngừa :term:`race conditions <race condition>` và điều phối việc thực thi của các thread. Xem thêm :term:`lock`.

   t-string
   t-strings
      Các literal chuỗi được thêm tiền tố ``t`` hoặc ``T`` thường được gọi là "t-strings", viết tắt của
      :ref:`chuỗi ký tự mẫu <t-strings>`.

   text encoding
   mã hóa văn bản
      Một chuỗi trong Python là một dãy các điểm mã Unicode (trong phạm vi ``U+0000``--``U+10FFFF``). Để lưu trữ hoặc truyền một chuỗi, chuỗi đó cần được tuần tự hóa thành một dãy byte.

      Việc tuần tự hóa một chuỗi thành một dãy byte được gọi là "encoding", còn việc tạo lại chuỗi từ dãy byte được gọi là "decoding".

      Có nhiều cách tuần tự hóa văn bản khác nhau
      :ref:`codecs <standard-encodings>`, được gọi chung là "text encodings".

   text file
   tệp văn bản
      Một :term:`file object` có khả năng đọc và ghi các đối tượng :class:`str`. Thông thường, một tệp văn bản thực sự truy cập một datastream hướng byte và tự động xử lý :term:`text encoding`. Ví dụ về tệp văn bản là các tệp được mở ở chế độ văn bản (``'r'`` hoặc ``'w'``),
      :data:`sys.stdin`, :data:`sys.stdout`, và các instance của
      :class:`io.StringIO`.

      Xem thêm :term:`binary file` để biết về một file object có khả năng đọc và ghi
      :term:`bytes-like objects <bytes-like object>`.

   trạng thái thread

      Thông tin được runtime :term:`CPython` sử dụng để chạy trong một thread của hệ điều hành. Ví dụ: thông tin này bao gồm exception hiện tại, nếu có, và trạng thái của trình thông dịch bytecode.

      Mỗi trạng thái thread được liên kết với một thread duy nhất của hệ điều hành, nhưng các thread có thể có nhiều trạng thái thread khả dụng. Tối đa một trạng thái trong số đó có thể
      :term:`được gắn <attached thread state>` cùng một lúc.

      Cần có một :term:`attached thread state` để gọi hầu hết C API của Python, trừ khi một hàm nêu rõ điều ngược lại trong tài liệu. Trình thông dịch bytecode chỉ chạy dưới một trạng thái thread được gắn.

      Mỗi trạng thái thread thuộc về một interpreter duy nhất, nhưng mỗi interpreter có thể có nhiều trạng thái thread, bao gồm nhiều trạng thái cho cùng một thread của hệ điều hành. Các trạng thái thread từ nhiều interpreter có thể được liên kết với cùng một thread, nhưng tại bất kỳ thời điểm nào, chỉ một trạng thái có thể :term:`được gắn <attached thread state>` trong thread đó.

      Xem :ref:`Trạng thái thread và Global Interpreter Lock <threads>` để biết thêm thông tin.

   thread-safe
   an toàn luồng
      Một module, hàm hoặc lớp hoạt động chính xác khi được nhiều thread sử dụng đồng thời. Mã thread-safe sử dụng các
      :term:`primitive đồng bộ hóa <synchronization primitive>` thích hợp như
      :term:`khóa <lock>` để bảo vệ trạng thái có thể thay đổi được dùng chung, hoặc được thiết kế để hoàn toàn tránh trạng thái có thể thay đổi được dùng chung. Trong
      bản dựng :term:`free-threaded <free threading>`, các kiểu tích hợp như
      :class:`dict`, :class:`list` và :class:`set` sử dụng cơ chế khóa nội bộ để khiến nhiều thao tác trở nên thread-safe, mặc dù không nhất thiết đảm bảo tính an toàn luồng. Mã không thread-safe có thể gặp
      :term:`điều kiện tranh chấp <race condition>` và :term:`tranh chấp dữ liệu <data race>` khi được sử dụng trong các chương trình đa luồng.

   token

      Một đơn vị nhỏ của mã nguồn, được tạo bởi
      :ref:`bộ phân tích từ vựng <lexical>` (còn được gọi là *bộ tách token*). Tên, số, chuỗi, toán tử, dòng mới và các thành phần tương tự được biểu diễn dưới dạng token.

      Mô-đun :mod:`tokenize` cung cấp bộ phân tích từ vựng của Python. Mô-đun :mod:`token` chứa thông tin về các loại token khác nhau.

   triple-quoted string
   chuỗi được đặt trong ba dấu nháy
      Một chuỗi được bao quanh bởi ba dấu ngoặc kép (") hoặc ba dấu nháy đơn ('). Mặc dù chúng không cung cấp chức năng nào không có trong chuỗi được đặt trong dấu nháy đơn, chúng hữu ích vì nhiều lý do. Chúng cho phép bạn đưa các dấu nháy đơn và dấu ngoặc kép không cần escape vào trong chuỗi, đồng thời có thể kéo dài qua nhiều dòng mà không cần sử dụng ký tự tiếp dòng, nên đặc biệt hữu ích khi viết docstring.

   type
   kiểu
      Kiểu của một đối tượng Python xác định đó là loại đối tượng nào; mọi đối tượng đều có một kiểu. Có thể truy cập kiểu của một đối tượng dưới dạng
      thuộc tính :attr:`~object.__class__` hoặc có thể được truy xuất bằng ``type(obj)``.

   type alias
   bí danh kiểu
      Một từ đồng nghĩa với một kiểu, được tạo bằng cách gán kiểu đó cho một identifier.

      Bí danh kiểu hữu ích trong việc đơn giản hóa :term:`gợi ý kiểu <type hint>`. Ví dụ::

         def remove_gray_shades(
                 colors: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
             pass

      có thể được viết dễ đọc hơn như sau::

         Color = tuple[int, int, int]

         def remove_gray_shades(colors: list[Color]) -> list[Color]:
             pass

      Xem :mod:`typing` và :pep:`484`, là những nội dung mô tả chức năng này.

   type hint
   gợi ý kiểu
      Một :term:`annotation` chỉ định kiểu dự kiến cho một biến, thuộc tính lớp hoặc tham số hay giá trị trả về của hàm.

      Gợi ý kiểu là tùy chọn và không được Python bắt buộc thực thi, nhưng chúng hữu ích cho :term:`trình kiểm tra kiểu tĩnh <static type checker>`. Chúng cũng có thể hỗ trợ IDE trong việc hoàn thành mã và tái cấu trúc.

      Có thể truy cập gợi ý kiểu của các biến toàn cục, thuộc tính lớp và hàm, nhưng không phải biến cục bộ, bằng cách sử dụng
      :func:`typing.get_type_hints`.

      Xem :mod:`typing` và :pep:`484`, là những nội dung mô tả chức năng này.

   universal newlines
   dòng mới phổ quát
      Cách diễn giải các luồng văn bản trong đó tất cả những quy ước sau đều được công nhận là kết thúc một dòng: quy ước kết thúc dòng của Unix ``'\n'``, quy ước của Windows ``'\r\n'`` và quy ước cũ của Macintosh ``'\r'``. Xem :pep:`278` và :pep:`3116`, cũng như
      :func:`bytes.splitlines` để biết thêm một cách sử dụng.

   variable annotation
   chú thích biến
      Một :term:`annotation` của một biến hoặc thuộc tính lớp.

      Khi chú thích một biến hoặc thuộc tính lớp, phép gán là tùy chọn::

         class C:
             field: 'annotation'

      Chú thích biến thường được dùng cho
      :term:`gợi ý kiểu <type hint>`: ví dụ, biến này dự kiến sẽ nhận
      :class:`int` giá trị::

         count: int = 0

      Cú pháp chú thích biến được giải thích trong phần :ref:`annassign`.

      Xem :term:`function annotation`, :pep:`484` và :pep:`526`, trong đó mô tả chức năng này. Đồng thời xem :ref:`annotations-howto` để biết các phương pháp hay nhất khi làm việc với annotations.

   virtual environment
   môi trường ảo
      Một môi trường runtime được cô lập theo cơ chế hợp tác, cho phép người dùng và ứng dụng Python cài đặt và nâng cấp các package phân phối Python mà không ảnh hưởng đến hoạt động của những ứng dụng Python khác đang chạy trên cùng hệ thống.

      Xem thêm :mod:`venv`.

   virtual machine
   máy ảo
      Một máy tính được định nghĩa hoàn toàn bằng phần mềm. Máy ảo của Python thực thi :term:`bytecode` do trình biên dịch bytecode tạo ra.

   walrus operator
   toán tử walrus
      Một cách nói vui để gọi toán tử :ref:`biểu thức gán <assignment-expressions>` ``:=`` vì nó trông hơi giống một con hải mã nếu bạn nghiêng đầu.

   Zen of Python
      Danh sách các nguyên tắc và triết lý thiết kế của Python, hữu ích cho việc tìm hiểu và sử dụng ngôn ngữ này. Có thể xem danh sách bằng cách nhập "``import this``" tại dấu nhắc tương tác.

.. _`Guido van Rossum`: https://gvanrossum.github.io/
.. _`python.org`: https://www.python.org
.. _`PEP 387: Soft Deprecation`: https://peps.python.org/pep-0387/#soft-deprecation
