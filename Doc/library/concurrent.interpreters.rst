:mod:`!concurrent.interpreters` --- Nhiều trình thông dịch trong cùng một tiến trình
====================================================================================

.. module:: concurrent.interpreters
   :synopsis: Nhiều trình thông dịch trong cùng một tiến trình

.. moduleauthor:: Eric Snow <ericsnowcurrently@gmail.com>
.. sectionauthor:: Eric Snow <ericsnowcurrently@gmail.com>

.. versionadded:: 3.14

**Mã nguồn:** :source:`Lib/concurrent/interpreters`

--------------

Module :mod:`!concurrent.interpreters` xây dựng các giao diện cấp cao hơn dựa trên module cấp thấp hơn :mod:`!_interpreters`.

Module này chủ yếu cung cấp một API cơ bản để quản lý các interpreter (còn gọi là "subinterpreter") và chạy các tác vụ trong đó. Việc chạy chủ yếu bao gồm chuyển sang một interpreter (trong thread hiện tại) và gọi một hàm trong ngữ cảnh thực thi đó.

Đối với tính đồng thời, bản thân các interpreter (và module này) không cung cấp nhiều hơn khả năng cô lập, mà riêng khả năng này thì không hữu ích. Tính đồng thời thực sự có sẵn riêng thông qua
:mod:`threads <threading>` -- xem `bên dưới <interp-concurrency_>`_.

.. seealso::

   :class:`~concurrent.futures.InterpreterPoolExecutor`
      Kết hợp thread với interpreter trong một giao diện quen thuộc.

   .. XXX Add references to the upcoming HOWTO docs in the seealso block.

   :ref:`isolating-extensions-howto`
      Cách cập nhật một extension module để hỗ trợ nhiều interpreter.

   :pep:`554`

   :pep:`734`

   :pep:`684`

.. XXX Why do we disallow multiple interpreters on WASM?

.. include:: ../includes/wasm-notavail.rst


Thông tin chi tiết chính
------------------------

Trước khi tìm hiểu sâu hơn, có một số ít chi tiết cần lưu ý khi sử dụng nhiều interpreter:

* `cô lập <interp-isolation_>`_, theo mặc định
* không có thread ngầm định
* chưa phải mọi package trên PyPI đều hỗ trợ sử dụng trong nhiều interpreter

.. XXX Are there other relevant details to list?


.. _interpreters-intro:

Giới thiệu
----------

"Trình thông dịch" về cơ bản là context thực thi của Python runtime. Nó chứa mọi trạng thái mà runtime cần để thực thi một chương trình. Những trạng thái này bao gồm import state và builtins. (Mỗi thread, ngay cả khi chỉ có main thread, đều có một số trạng thái runtime bổ sung, bên cạnh interpreter hiện tại, liên quan đến exception hiện tại và vòng lặp đánh giá bytecode.)

Khái niệm và chức năng của interpreter đã là một phần của Python kể từ phiên bản 2.2, nhưng tính năng này chỉ khả dụng thông qua C-API và không được nhiều người biết đến; `tính cô lập <interp-isolation_>`_ cũng tương đối chưa hoàn thiện cho đến phiên bản 3.12.

.. _interp-isolation:

Nhiều Interpreter và Tính cô lập
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một triển khai Python có thể hỗ trợ sử dụng nhiều interpreter trong cùng một process. CPython có hỗ trợ này. Mỗi interpreter về cơ bản được cô lập khỏi các interpreter khác (với một số ít ngoại lệ ở cấp process được quản lý cẩn thận đối với quy tắc này).

Tính cô lập đó chủ yếu hữu ích như một sự phân tách chặt chẽ giữa các thành phần logic riêng biệt của một chương trình, khi bạn muốn kiểm soát cẩn thận cách các thành phần đó tương tác với nhau.

.. note::

   Về mặt kỹ thuật, các interpreter trong cùng một process không bao giờ có thể được cô lập hoàn toàn khỏi nhau, vì có rất ít hạn chế đối với việc truy cập bộ nhớ trong cùng process. Python runtime cố gắng hết sức để duy trì tính cô lập, nhưng các extension module có thể dễ dàng vi phạm điều đó. Vì vậy, không sử dụng nhiều interpreter trong các tình huống nhạy cảm về bảo mật, khi chúng không nên có quyền truy cập vào dữ liệu của nhau.

Chạy trong một Interpreter
^^^^^^^^^^^^^^^^^^^^^^^^^^

Việc chạy trong một interpreter khác bao gồm chuyển sang interpreter đó trong thread hiện tại, sau đó gọi một hàm. Runtime sẽ thực thi hàm bằng trạng thái của interpreter hiện tại.
:mod:`!concurrent.interpreters` module cung cấp API cơ bản để tạo và quản lý các interpreter, cũng như thực hiện thao tác chuyển đổi và gọi.

Không có thread nào khác được tự động khởi động cho thao tác này. Tuy nhiên, có `một hàm trợ giúp <interp-call-in-thread_>`_ cho việc đó. Ngoài ra còn có một hàm trợ giúp chuyên dụng khác để gọi hàm builtin
:func:`exec` trong một interpreter.

Khi :func:`exec` (hoặc :func:`eval`) được gọi trong một interpreter, chúng chạy bằng module :mod:`!__main__` của interpreter đó làm namespace "globals". Điều tương tự cũng đúng với các hàm không liên kết với module nào. Đây cũng là cách các script được gọi từ dòng lệnh chạy trong module :mod:`!__main__`.


.. _interp-concurrency:

Tính đồng thời và tính song song
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Như đã lưu ý trước đó, các interpreter không tự cung cấp bất kỳ khả năng concurrency nào. Chúng chỉ đơn thuần biểu diễn context thực thi bị cô lập mà runtime sẽ sử dụng *trong thread hiện tại*. Sự cô lập đó khiến chúng tương tự như các process, nhưng chúng vẫn có được hiệu quả trong process, giống như các thread.

Dù vậy, các interpreter vẫn tự nhiên hỗ trợ một số dạng concurrency nhất định. Sự cô lập đó mang lại một tác động phụ mạnh mẽ. Nó cho phép một cách tiếp cận concurrency khác với cách bạn có thể thực hiện bằng async hoặc thread. Đây là một mô hình concurrency tương tự CSP hoặc mô hình actor, một mô hình tương đối dễ suy luận.

Bạn có thể tận dụng mô hình concurrency đó trong một thread duy nhất bằng cách chuyển đổi qua lại giữa các interpreter, theo phong cách Stackless. Tuy nhiên, mô hình này hữu ích hơn khi bạn kết hợp các interpreter với nhiều thread. Điều này chủ yếu bao gồm việc khởi động một thread mới, chuyển sang một interpreter khác rồi chạy nội dung bạn muốn ở đó.

Mỗi thread thực tế trong Python, ngay cả khi bạn chỉ chạy trong thread chính, đều có context thực thi *hiện tại* riêng. Nhiều thread có thể sử dụng cùng một interpreter hoặc các interpreter khác nhau.

Ở cấp độ khái quát, bạn có thể hình dung sự kết hợp giữa các thread và interpreter là các thread có cơ chế chia sẻ tùy chọn.

Một lợi ích đáng kể là các interpreter được cô lập đủ tốt để không chia sẻ :term:`GIL`, điều này có nghĩa là việc kết hợp các thread với nhiều interpreter cho phép đạt được khả năng parallelism đa lõi hoàn toàn. (Điều này đã đúng kể từ Python 3.12.)

Giao tiếp giữa các Interpreter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trong thực tế, nhiều interpreter chỉ hữu ích khi chúng ta có cách giao tiếp giữa chúng. Điều này thường liên quan đến một dạng truyền thông điệp nào đó, nhưng thậm chí có thể là việc chia sẻ dữ liệu theo một cách được quản lý cẩn thận.

Với suy nghĩ đó, module :mod:`!concurrent.interpreters` cung cấp một implementation :class:`queue.Queue`, có thể truy cập thông qua
:func:`create_queue`.

.. _interp-object-sharing:

Các đối tượng "chia sẻ"
^^^^^^^^^^^^^^^^^^^^^^^

Mọi dữ liệu thực sự được chia sẻ giữa các interpreter đều mất đi tính an toàn luồng do :term:`GIL` cung cấp. Có nhiều lựa chọn khác nhau để xử lý việc này trong các extension module. Tuy nhiên, từ mã Python, việc thiếu tính an toàn luồng có nghĩa là các đối tượng thực sự không thể được chia sẻ, ngoại trừ một vài trường hợp. Thay vào đó, phải tạo một bản sao, nghĩa là các đối tượng mutable sẽ không còn được đồng bộ.

Theo mặc định, hầu hết các đối tượng được sao chép bằng :mod:`pickle` khi được truyền sang một interpreter khác. Gần như tất cả các đối tượng builtin immutable đều được chia sẻ trực tiếp hoặc sao chép hiệu quả. Ví dụ:

* :const:`None`
* :class:`bool` (:const:`True` và :const:`False`)
* :class:`bytes`
* :class:`str`
* :class:`int`
* :class:`float`
* :class:`tuple` (các đối tượng được hỗ trợ tương tự)

Có một số ít kiểu Python thực sự chia sẻ dữ liệu có thể thay đổi giữa các trình thông dịch:

* :class:`memoryview`
* :class:`Queue`


Tham chiếu
----------

Mô-đun này định nghĩa các hàm sau:

.. function:: list_all()

   Trả về một :class:`list` gồm các đối tượng :class:`Interpreter`, mỗi đối tượng tương ứng với một trình thông dịch hiện có.

.. function:: get_current()

   Trả về một đối tượng :class:`Interpreter` cho trình thông dịch hiện đang chạy.

.. function:: get_main()

   Trả về một đối tượng :class:`Interpreter` cho trình thông dịch chính. Đây là trình thông dịch mà runtime tạo ra để chạy :term:`REPL` hoặc tập lệnh được cung cấp trên dòng lệnh. Thông thường, đây là trình thông dịch duy nhất.

.. function:: create()

   Khởi tạo một trình thông dịch Python mới (đang rảnh) và trả về một đối tượng :class:`Interpreter` cho trình thông dịch đó.

.. function:: create_queue()

   Khởi tạo một hàng đợi liên interpreter mới và trả về một đối tượng :class:`Queue` cho hàng đợi đó.


Các đối tượng interpreter
^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Interpreter(id)

   Một interpreter duy nhất trong process hiện tại.

   Thông thường, không nên gọi :class:`Interpreter` trực tiếp. Thay vào đó, hãy sử dụng :func:`create` hoặc một trong các hàm khác của module.

   .. attribute:: id

      (chỉ đọc)

      ID của interpreter bên dưới.

   .. attribute:: whence

      (chỉ đọc)

      Một chuỗi mô tả nguồn gốc của trình thông dịch.

   .. method:: is_running()

      Trả về ``True`` nếu trình thông dịch hiện đang thực thi mã trong mô-đun :mod:`!__main__` của nó và ``False`` trong trường hợp ngược lại.

   .. method:: close()

      Hoàn tất và hủy trình thông dịch.

   .. method:: prepare_main(ns=None, **kwargs)

      Liên kết các đối tượng trong mô-đun :mod:`!__main__` của trình thông dịch.

      Một số đối tượng thực sự được dùng chung và một số được sao chép một cách hiệu quả, nhưng hầu hết được sao chép thông qua :mod:`pickle`. Xem :ref:`interp-object-sharing`.

   .. method:: exec(code, /, dedent=True)

      Chạy mã nguồn đã cho trong trình thông dịch (trong luồng hiện tại).

   .. method:: call(callable, /, *args, **kwargs)

      Trả về kết quả của việc chạy hàm đã cho trong trình thông dịch (trong luồng hiện tại).

   .. _interp-call-in-thread:

   .. method:: call_in_thread(callable, /, *args, **kwargs)

      Chạy hàm đã cho trong interpreter (trong một thread mới).

Ngoại lệ
^^^^^^^^

.. exception:: InterpreterError

   Ngoại lệ này, là một lớp con của :exc:`Exception`, được phát sinh khi xảy ra lỗi liên quan đến interpreter.

.. exception:: InterpreterNotFoundError

   Ngoại lệ này, là một lớp con của :exc:`InterpreterError`, được phát sinh khi interpreter đích không còn tồn tại.

.. exception:: ExecutionFailed

   Ngoại lệ này, là một lớp con của :exc:`InterpreterError`, được phát sinh khi code đang chạy phát sinh một ngoại lệ chưa được bắt.

   .. attribute:: excinfo

      Ảnh chụp cơ bản của ngoại lệ được phát sinh trong interpreter khác.

.. XXX Document the excinfoattrs?

.. exception:: NotShareableError

   Ngoại lệ này, là một lớp con của :exc:`TypeError`, được phát sinh khi không thể gửi một đối tượng đến interpreter khác.


Giao tiếp giữa các trình thông dịch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Queue(id)

   Một wrapper cho hàng đợi cấp thấp, liên trình thông dịch, triển khai giao diện :class:`queue.Queue`. Hàng đợi nền tảng chỉ có thể được tạo thông qua :func:`create_queue`.

   Một số đối tượng thực sự được dùng chung và một số được sao chép một cách hiệu quả, nhưng hầu hết được sao chép thông qua :mod:`pickle`. Xem :ref:`interp-object-sharing`.

   .. attribute:: id

      (chỉ đọc)

      ID của hàng đợi.


.. exception:: QueueEmptyError

   Ngoại lệ này, là một lớp con của :exc:`queue.Empty`, được phát sinh từ
   :meth:`!Queue.get` và :meth:`!Queue.get_nowait` khi hàng đợi trống.

.. exception:: QueueFullError

   Ngoại lệ này, một lớp con của :exc:`queue.Full`, được phát sinh từ
   :meth:`!Queue.put` và :meth:`!Queue.put_nowait` khi hàng đợi đầy.


Cách sử dụng cơ bản
-------------------

Tạo một interpreter và chạy mã trong đó::

    from concurrent import interpreters

    interp = interpreters.create()

    # Chạy trong luồng hệ điều hành hiện tại.

    interp.exec('print("spam!")')

    interp.exec("""if True:
        print('spam!')
        """)

    from textwrap import dedent
    interp.exec(dedent("""
        print('spam!')
        """))

    def run(arg):
        return arg

    res = interp.call(run, 'spam!')
    print(res)

    def run():
        print('spam!')

    interp.call(run)

    # Chạy trong luồng hệ điều hành mới.

    t = interp.call_in_thread(run)
    t.join()

.. _`below`: interp-concurrency_
.. _`isolated`: interp-isolation_
.. _`isolation`: interp-isolation_
.. _`a helper`: interp-call-in-thread_
