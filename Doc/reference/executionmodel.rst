
.. _execmodel:

****************
Mô hình thực thi
****************

.. index::
   single: execution model
   pair: code; block

.. _prog_structure:

Cấu trúc của một chương trình
=============================

.. index:: block

Một chương trình Python được cấu tạo từ các khối mã. Một :dfn:`khối` là một phần văn bản chương trình Python được thực thi như một đơn vị. Các khối bao gồm: một module, phần thân của một hàm và một định nghĩa lớp. Mỗi lệnh được nhập trong chế độ tương tác là một khối. Một tệp script (tệp được cung cấp dưới dạng đầu vào tiêu chuẩn cho trình thông dịch hoặc được chỉ định làm đối số dòng lệnh cho trình thông dịch) là một khối mã. Một lệnh script (lệnh được chỉ định trên dòng lệnh của trình thông dịch bằng tùy chọn :option:`-c`) là một khối mã. Một module được chạy dưới dạng script cấp cao nhất (với module ``__main__``) từ dòng lệnh bằng đối số :option:`-m` cũng là một khối mã. Đối số chuỗi được truyền cho các hàm tích hợp sẵn :func:`eval` và :func:`exec` là một khối mã.

.. index:: pair: execution; frame

Một khối mã được thực thi trong một :dfn:`khung thực thi`. Một khung chứa một số thông tin quản trị (được sử dụng để gỡ lỗi) và xác định việc thực thi sẽ tiếp tục ở đâu và như thế nào sau khi quá trình thực thi khối mã hoàn tất.

.. _naming:

Đặt tên và liên kết
===================

.. index::
   single: namespace
   single: scope

.. _bind_names:

Liên kết tên
------------

.. index::
   single: name
   pair: binding; name

:dfn:`Tên` tham chiếu đến các đối tượng. Tên được tạo ra bởi các thao tác liên kết tên.

.. index:: single: from; import statement

Các cấu trúc sau đây liên kết tên:

* tham số hình thức của hàm,
* định nghĩa lớp,
* định nghĩa hàm,
* biểu thức gán,
* :ref:`các đích là identifiers nếu xuất hiện trong phép gán: <assignment>`

  + :keyword:`for` phần đầu của vòng lặp,
  + sau :keyword:`!as` trong một câu lệnh :keyword:`with`, mệnh đề :keyword:`except`, mệnh đề :keyword:`except* <except_star>`, hoặc trong mẫu as khi so khớp mẫu cấu trúc,
  + trong một mẫu bắt giữ khi so khớp mẫu cấu trúc

* Các câu lệnh :keyword:`import`.
* Các câu lệnh :keyword:`type`.
* :ref:`danh sách tham số kiểu <type-params>`.

Câu lệnh :keyword:`!import` có dạng ``from ... import *`` liên kết tất cả các tên được định nghĩa trong module được nhập, ngoại trừ những tên bắt đầu bằng dấu gạch dưới. Dạng này chỉ có thể được sử dụng ở cấp module.

Một đích xuất hiện trong câu lệnh :keyword:`del` cũng được xem là đã liên kết cho mục đích này (mặc dù ngữ nghĩa thực tế là hủy liên kết tên đó).

Mỗi câu lệnh gán hoặc import đều xuất hiện bên trong một khối được xác định bởi định nghĩa lớp hoặc hàm, hoặc ở cấp mô-đun (khối mã cấp cao nhất).

.. index:: pair: free; variable

Nếu một tên được liên kết trong một khối, nó là một biến cục bộ của khối đó, trừ khi được khai báo là :keyword:`nonlocal` hoặc :keyword:`global`. Nếu một tên được liên kết ở cấp mô-đun, nó là một biến toàn cục. (Các biến của khối mã mô-đun vừa là cục bộ vừa là toàn cục.) Nếu một biến được sử dụng trong một khối mã nhưng không được định nghĩa ở đó, thì đó là một :term:`free variable`.

Mỗi lần xuất hiện của một tên trong văn bản chương trình đều tham chiếu đến :dfn:`liên kết` của tên đó, được thiết lập theo các quy tắc phân giải tên sau đây.

.. _resolve_names:

Phân giải tên
-------------

.. index:: scope

Một :dfn:`phạm vi` xác định khả năng hiển thị của một tên bên trong một khối. Nếu một biến cục bộ được định nghĩa trong một khối, phạm vi của biến đó bao gồm khối ấy. Nếu định nghĩa xuất hiện trong một khối hàm, phạm vi sẽ mở rộng đến mọi khối nằm bên trong khối định nghĩa, trừ khi một khối bên trong tạo ra một liên kết khác cho tên đó.

.. index:: single: environment

Khi một tên được sử dụng trong một khối mã, nó được phân giải bằng phạm vi bao quanh gần nhất. Tập hợp tất cả các phạm vi như vậy hiển thị với một khối mã được gọi là
:dfn:`môi trường`.

.. index::
   single: NameError (built-in exception)
   single: UnboundLocalError

Khi hoàn toàn không tìm thấy một tên, một exception :exc:`NameError` sẽ được raised. Nếu scope hiện tại là scope của một function và tên đó đề cập đến một biến cục bộ chưa được bind với một giá trị tại thời điểm tên được sử dụng, một exception :exc:`UnboundLocalError` sẽ được raised.
:exc:`UnboundLocalError` là một subclass của :exc:`NameError`.

Nếu một thao tác binding tên xuất hiện ở bất kỳ đâu trong một code block, mọi cách sử dụng tên đó trong block đều được xem là tham chiếu đến block hiện tại. Điều này có thể gây lỗi khi một tên được sử dụng trong block trước khi được bind. Quy tắc này khá tinh tế. Python không có khai báo và cho phép các thao tác binding tên xuất hiện ở bất kỳ đâu trong một code block. Có thể xác định các biến cục bộ của một code block bằng cách quét toàn bộ văn bản của block để tìm các thao tác binding tên. Xem :ref:`mục FAQ về UnboundLocalError <faq-unboundlocalerror>` để biết ví dụ.

Nếu câu lệnh :keyword:`global` xuất hiện trong một block, mọi cách sử dụng các tên được chỉ định trong câu lệnh đều đề cập đến các binding của những tên đó trong namespace cấp cao nhất. Các tên được phân giải trong namespace cấp cao nhất bằng cách tìm kiếm global namespace, tức namespace của module chứa code block, và builtins namespace, namespace của module :mod:`builtins`. Global namespace được tìm kiếm trước. Nếu không tìm thấy các tên ở đó, builtins namespace sẽ được tìm kiếm tiếp theo. Nếu cũng không tìm thấy các tên trong builtins namespace, các biến mới sẽ được tạo trong global namespace. Câu lệnh global phải đứng trước mọi cách sử dụng các tên được liệt kê.

Câu lệnh :keyword:`global` có cùng scope với một thao tác binding tên trong cùng block. Nếu scope bao quanh gần nhất của một biến tự do có chứa câu lệnh global, biến tự do đó được xem là biến global.

.. XXX say more about "nonlocal" semantics here

Câu lệnh :keyword:`nonlocal` khiến các tên tương ứng tham chiếu đến những biến đã được bind trước đó trong scope của function bao quanh gần nhất.
:exc:`SyntaxError` được raised tại thời điểm biên dịch nếu tên đã cho không tồn tại trong bất kỳ scope function bao quanh nào. :ref:`Type parameters <type-params>` không thể được bind lại bằng câu lệnh :keyword:`!nonlocal`.

.. index:: pair: module; __main__

Không gian tên cho một module được tự động tạo lần đầu module được import. Module chính của một script luôn được gọi là :mod:`__main__`.

Các khối định nghĩa class và các đối số truyền cho :func:`exec` và :func:`eval` có ý nghĩa đặc biệt trong ngữ cảnh phân giải tên. Định nghĩa class là một câu lệnh có thể thực thi, có thể sử dụng và định nghĩa các tên. Những tham chiếu này tuân theo các quy tắc phân giải tên thông thường, ngoại trừ việc các biến cục bộ chưa được liên kết sẽ được tra cứu trong không gian tên toàn cục. Không gian tên của định nghĩa class trở thành dictionary thuộc tính của class. Phạm vi của các tên được định nghĩa trong một khối class chỉ giới hạn ở khối class; phạm vi này không mở rộng đến các khối mã của method. Điều này bao gồm cả các biểu thức tạo và biểu thức trình tạo, nhưng không bao gồm
:ref:`phạm vi chú thích <annotation-scopes>`, vốn có quyền truy cập vào các phạm vi class bao quanh chúng. Điều này có nghĩa là đoạn sau sẽ thất bại::

   class A:
       a = 42
       b = list(a + i for i in range(10))

Tuy nhiên, đoạn sau sẽ thành công::

   class A:
       type Alias = Nested
       class Nested: pass

   print(A.Alias.__value__)  # <type 'A.Nested'>

.. _annotation-scopes:

Phạm vi chú thích
-----------------

:term:`Chú thích <annotation>`, :ref:`danh sách tham số kiểu <type-params>` và các câu lệnh :keyword:`type` giới thiệu *phạm vi chú thích*, hoạt động phần lớn giống như phạm vi hàm, nhưng có một số ngoại lệ được thảo luận bên dưới.

Phạm vi annotation được sử dụng trong các ngữ cảnh sau:

* :term:`Annotation của hàm <function annotation>`.
* :term:`Annotation của biến <variable annotation>`.
* Danh sách tham số kiểu cho :ref:`generic type aliases <generic-type-aliases>`.
* Danh sách tham số kiểu cho :ref:`generic functions <generic-functions>`. Các annotation của generic function được thực thi trong phạm vi annotation, nhưng các giá trị mặc định và decorator của hàm thì không.
* Danh sách tham số kiểu cho :ref:`generic classes <generic-classes>`. Các lớp cơ sở và đối số từ khóa của generic class được thực thi trong phạm vi annotation, nhưng các decorator của lớp thì không.
* Các bound, constraint và giá trị mặc định cho tham số kiểu (:ref:`được đánh giá một cách trì hoãn <lazy-evaluation>`).
* Giá trị của các bí danh kiểu (:ref:`được đánh giá một cách trì hoãn <lazy-evaluation>`).

Phạm vi chú thích khác với phạm vi hàm theo những cách sau:

* Phạm vi chú thích có quyền truy cập vào không gian tên của lớp bao quanh chúng. Nếu một phạm vi chú thích nằm ngay trong một phạm vi lớp, hoặc nằm trong một phạm vi chú thích khác vốn nằm ngay trong một phạm vi lớp, mã trong phạm vi chú thích có thể sử dụng các tên được định nghĩa trong phạm vi lớp như thể mã đó được thực thi trực tiếp trong thân lớp. Điều này khác với các hàm thông thường được định nghĩa bên trong lớp, vì chúng không thể truy cập các tên được định nghĩa trong phạm vi lớp.
* Các biểu thức trong phạm vi chú thích không thể chứa các biểu thức :keyword:`yield`, ``yield from``,
  :keyword:`await`, hoặc :token:`:= <python-grammar:assignment_expression>`. (Các biểu thức này được phép sử dụng trong những phạm vi khác nằm trong phạm vi chú thích.)
* Các tên được định nghĩa trong phạm vi chú thích không thể được liên kết lại bằng các câu lệnh :keyword:`nonlocal` trong những phạm vi bên trong. Điều này chỉ bao gồm các tham số kiểu, vì không có phần tử cú pháp nào khác có thể xuất hiện trong phạm vi chú thích và tạo ra tên mới.
* Mặc dù các phạm vi chú thích có một tên nội bộ, tên đó không được phản ánh trong
  :term:`qualified name` của các đối tượng được định nghĩa trong phạm vi. Thay vào đó, :attr:`~definition.__qualname__` của những đối tượng đó giống như thể đối tượng được định nghĩa trong phạm vi bao quanh.

.. versionadded:: 3.12
   Phạm vi chú thích được giới thiệu trong Python 3.12 như một phần của :pep:`695`.

.. versionchanged:: 3.13
   Phạm vi chú thích cũng được sử dụng cho các giá trị mặc định của tham số kiểu, được giới thiệu trong :pep:`696`.

.. versionchanged:: 3.14
   Phạm vi chú thích hiện cũng được sử dụng cho các chú thích, như được quy định trong
   :pep:`649` và :pep:`749`.

.. _lazy-evaluation:

Đánh giá lười
-------------

Hầu hết các phạm vi chú thích đều *được đánh giá một cách trì hoãn*. Điều này bao gồm các chú thích, các giá trị của bí danh kiểu được tạo thông qua câu lệnh :keyword:`type`, cũng như các cận, ràng buộc và giá trị mặc định của các biến kiểu được tạo thông qua :ref:`cú pháp tham số kiểu <type-params>`. Điều này có nghĩa là chúng không được đánh giá khi bí danh kiểu hoặc biến kiểu được tạo, hoặc khi đối tượng chứa các chú thích được tạo. Thay vào đó, chúng chỉ được đánh giá khi cần thiết, chẳng hạn như khi thuộc tính ``__value__`` trên một bí danh kiểu được truy cập.

Ví dụ:

.. doctest::

   >>> type Alias = 1/0
   >>> Alias.__value__
   Traceback (most recent call last):
     ...
   ZeroDivisionError: division by zero
   >>> def func[T: 1/0](): pass
   >>> T = func.__type_params__[0]
   >>> T.__bound__
   Traceback (most recent call last):
     ...
   ZeroDivisionError: division by zero

Trong trường hợp này, ngoại lệ chỉ được phát sinh khi thuộc tính ``__value__`` của bí danh kiểu hoặc thuộc tính ``__bound__`` của biến kiểu được truy cập.

Hành vi này chủ yếu hữu ích cho các tham chiếu đến những kiểu chưa được định nghĩa khi bí danh kiểu hoặc biến kiểu được tạo. Ví dụ, đánh giá trì hoãn cho phép tạo các bí danh kiểu đệ quy lẫn nhau::

   from typing import Literal

   type SimpleExpr = int | Parenthesized
   type Parenthesized = tuple[Literal["("], Expr, Literal[")"]]
   type Expr = SimpleExpr | tuple[SimpleExpr, Literal["+", "-"], Expr]

Các giá trị được đánh giá trì hoãn được đánh giá trong :ref:`phạm vi annotation <annotation-scopes>`, nghĩa là các tên xuất hiện bên trong giá trị được đánh giá trì hoãn sẽ được tra cứu như thể chúng được sử dụng trong phạm vi bao quanh trực tiếp.

.. versionadded:: 3.12

.. _restrict_exec:

Builtins và thực thi bị hạn chế
-------------------------------

.. index:: pair: restricted; execution

.. impl-detail::

   Người dùng không nên đụng đến ``__builtins__``; đây hoàn toàn là một chi tiết triển khai. Người dùng muốn ghi đè các giá trị trong namespace builtins nên
   :keyword:`import` mô-đun :mod:`builtins` và sửa đổi các thuộc tính của mô-đun đó cho phù hợp.

Không gian tên builtins liên kết với việc thực thi một khối mã thực sự được tìm thấy bằng cách tra cứu tên ``__builtins__`` trong không gian tên toàn cục của khối đó; đây phải là một dictionary hoặc một module (trong trường hợp sau, dictionary của module được sử dụng). Theo mặc định, khi ở trong
module :mod:`__main__`, ``__builtins__`` là module tích hợp sẵn
:mod:`builtins`; khi ở trong bất kỳ module nào khác, ``__builtins__`` là bí danh cho dictionary của chính module :mod:`builtins`.


.. _dynamic-features:

Tương tác với các tính năng động
--------------------------------

Việc phân giải tên của các biến tự do diễn ra tại runtime, không phải tại thời điểm biên dịch. Điều này có nghĩa là đoạn mã sau sẽ in ra 42::

   i = 10
   def f():
       print(i)
   i = 42
   f()

.. XXX from * also invalid with relative imports (at least currently)

Các hàm :func:`eval` và :func:`exec` không có quyền truy cập vào toàn bộ môi trường để phân giải tên. Tên có thể được phân giải trong không gian tên cục bộ và toàn cục của bên gọi. Các biến tự do không được phân giải trong không gian tên bao quanh gần nhất mà trong không gian tên toàn cục. [#]_ Các hàm :func:`exec` và
:func:`eval` có các đối số tùy chọn để ghi đè không gian tên toàn cục và cục bộ. Nếu chỉ định một không gian tên, nó sẽ được sử dụng cho cả hai.

.. XXX(ncoghlan) above is only accurate for string execution. When executing code objects,
   closure cells may now be passed explicitly to resolve co_freevars references.
   Docs issue: https://github.com/python/cpython/issues/122826

.. _exceptions:

Ngoại lệ
========

.. index:: single: exception

.. index::
   single: raise an exception
   single: handle an exception
   single: exception handler
   single: errors
   single: error handling

Ngoại lệ là một cách thoát khỏi luồng điều khiển thông thường của một khối mã để xử lý lỗi hoặc các điều kiện bất thường khác. Một ngoại lệ được *phát sinh* tại thời điểm phát hiện lỗi; ngoại lệ đó có thể được *xử lý* bởi khối mã bao quanh hoặc bởi bất kỳ khối mã nào trực tiếp hay gián tiếp gọi khối mã nơi xảy ra lỗi.

Trình thông dịch Python phát sinh một ngoại lệ khi phát hiện lỗi trong thời gian chạy (chẳng hạn như phép chia cho số không). Một chương trình Python cũng có thể phát sinh ngoại lệ một cách rõ ràng bằng câu lệnh :keyword:`raise`. Bộ xử lý ngoại lệ được chỉ định bằng câu lệnh :keyword:`try` ... :keyword:`except`. Mệnh đề :keyword:`finally` của câu lệnh như vậy có thể được dùng để chỉ định mã dọn dẹp không xử lý ngoại lệ, nhưng vẫn được thực thi bất kể trong đoạn mã trước đó có xảy ra ngoại lệ hay không.

.. index:: single: termination model

Python sử dụng mô hình "termination" để xử lý lỗi: một bộ xử lý ngoại lệ có thể xác định điều gì đã xảy ra và tiếp tục thực thi ở một cấp bên ngoài, nhưng không thể khắc phục nguyên nhân của lỗi rồi thử lại thao tác thất bại (ngoại trừ việc nhập lại đoạn mã gây lỗi từ đầu).

.. index:: single: SystemExit (built-in exception)

Khi một ngoại lệ hoàn toàn không được xử lý, trình thông dịch sẽ kết thúc việc thực thi chương trình hoặc quay lại vòng lặp chính tương tác. Trong cả hai trường hợp, trình thông dịch sẽ in ra stack traceback, ngoại trừ khi ngoại lệ là :exc:`SystemExit`.

Ngoại lệ được nhận diện bằng các instance của class. Mệnh đề :keyword:`except` được chọn tùy theo class của instance: mệnh đề này phải tham chiếu đến class của instance hoặc một :term:`lớp cơ sở không ảo <abstract base class>` của class đó. Handler có thể nhận instance và instance có thể mang thêm thông tin về điều kiện bất thường.

.. note::

   Thông báo ngoại lệ không thuộc Python API. Nội dung của chúng có thể thay đổi từ phiên bản Python này sang phiên bản Python khác mà không có cảnh báo, và mã chạy trên nhiều phiên bản của trình thông dịch không nên phụ thuộc vào nội dung đó.

Xem thêm phần mô tả về câu lệnh :keyword:`try` trong mục :ref:`try` và câu lệnh :keyword:`raise` trong mục :ref:`raise`.


.. _execcomponents:

Các thành phần runtime
======================

Mô hình điện toán tổng quát
---------------------------

Mô hình thực thi của Python không hoạt động độc lập. Nó chạy trên một host machine và thông qua runtime environment của host đó, bao gồm hệ điều hành (OS), nếu có. Khi một chương trình chạy, các lớp khái niệm mô tả cách chương trình chạy trên host có thể được hình dung như sau:

   | **máy host**
   | **process** (tài nguyên toàn cục)
   | **thread** (chạy mã máy)

Mỗi process đại diện cho một chương trình đang chạy trên host. Hãy coi bản thân mỗi process là phần dữ liệu của chương trình đó. Hãy coi các thread của process là phần thực thi của chương trình. Sự phân biệt này sẽ rất quan trọng để hiểu runtime Python trên phương diện khái niệm.

Process, với vai trò là phần dữ liệu, là ngữ cảnh thực thi trong đó chương trình chạy. Nó chủ yếu bao gồm tập hợp các tài nguyên được host cấp cho chương trình, gồm bộ nhớ, signal, file handle, socket và biến môi trường.

Các process được cô lập và độc lập với nhau. (Điều tương tự cũng đúng với các host.) Host quản lý quyền truy cập của process vào các tài nguyên được cấp cho nó, đồng thời điều phối giữa các process.

Mỗi thread đại diện cho việc thực thi thực tế mã máy của chương trình, chạy trong phạm vi các tài nguyên được cấp cho process của chương trình. Cách thức và thời điểm việc thực thi đó diễn ra hoàn toàn do host quyết định.

Từ góc nhìn của Python, một chương trình luôn bắt đầu với chính xác một thread. Tuy nhiên, chương trình có thể phát triển để chạy trên nhiều thread đồng thời. Không phải host nào cũng hỗ trợ nhiều thread trên mỗi process, nhưng hầu hết đều hỗ trợ. Không giống các process, các thread trong một process không bị cô lập và không độc lập với nhau. Cụ thể, tất cả thread trong một process đều chia sẻ tất cả tài nguyên của process đó.

Điểm cốt lõi của các thread là mỗi thread *chạy* độc lập, đồng thời với các thread khác. Điều đó có thể chỉ là đồng thời về mặt khái niệm ("concurrently") hoặc đồng thời về mặt vật lý ("in parallel"). Dù theo cách nào, các thread thực tế chạy với tốc độ không được đồng bộ hóa.

.. note::

   Tốc độ không được đồng bộ hóa đó có nghĩa là không có phần bộ nhớ nào của process được đảm bảo luôn nhất quán đối với mã đang chạy trong bất kỳ thread cụ thể nào. Vì vậy, các chương trình đa thread phải cẩn thận điều phối quyền truy cập vào những tài nguyên được chủ đích chia sẻ. Tương tự, chúng phải hết sức cẩn trọng không truy cập bất kỳ tài nguyên *khác* nào trong nhiều thread; nếu không, hai thread chạy cùng lúc có thể vô tình can thiệp vào việc sử dụng một số dữ liệu được chia sẻ của nhau. Tất cả những điều này đều đúng với cả các chương trình Python và runtime Python.

   Cái giá của yêu cầu rộng và thiếu cấu trúc này là sự đánh đổi cho mức độ concurrency thô mà các thread cung cấp. Việc không tuân thủ kỷ luật bắt buộc này thường đồng nghĩa với việc phải xử lý các lỗi không xác định và tình trạng hỏng dữ liệu.

Mô hình runtime của Python
--------------------------

Các lớp khái niệm giống nhau được áp dụng cho mỗi chương trình Python, cùng với một số lớp dữ liệu bổ sung dành riêng cho Python:

   | **máy chủ**
   | **process** (tài nguyên toàn cục)
   | runtime toàn cục của Python (*state*)
   | interpreter Python (*state*)
   | **luồng** (chạy bytecode Python và "C-API")
   | *Trạng thái luồng* Python

Ở cấp độ khái niệm: khi một chương trình Python khởi động, nó trông chính xác như sơ đồ đó, với mỗi thành phần một bản. Runtime có thể phát triển để bao gồm nhiều interpreter, và mỗi interpreter có thể phát triển để bao gồm nhiều trạng thái luồng.

.. note::

   Một triển khai Python không nhất thiết phải triển khai các lớp runtime một cách riêng biệt hoặc thậm chí một cách cụ thể. Ngoại lệ duy nhất là những nơi các lớp riêng biệt được chỉ định trực tiếp hoặc hiển thị cho người dùng, chẳng hạn như thông qua module :mod:`threading`.

.. note::

   Interpreter ban đầu thường được gọi là interpreter "main". Một số triển khai Python, như CPython, gán các vai trò đặc biệt cho interpreter main.

   Tương tự, host thread nơi runtime được khởi tạo được gọi là thread "main". Nó có thể khác với thread ban đầu của process, mặc dù hai thread này thường là một. Trong một số trường hợp, "main thread" có thể mang nghĩa cụ thể hơn và chỉ trạng thái luồng ban đầu. Một Python runtime có thể gán các trách nhiệm cụ thể cho main thread, chẳng hạn như xử lý signal.

Xét tổng thể, Python runtime bao gồm trạng thái runtime toàn cục, các interpreter và các trạng thái luồng. Runtime đảm bảo tất cả trạng thái đó luôn nhất quán trong suốt vòng đời của nó, đặc biệt khi được sử dụng với nhiều host thread.

Ở cấp độ khái niệm, runtime toàn cục chỉ là một tập hợp các trình thông dịch. Mặc dù các trình thông dịch này độc lập và được cô lập với nhau, chúng vẫn có thể chia sẻ một số dữ liệu hoặc tài nguyên khác. Runtime chịu trách nhiệm quản lý các tài nguyên toàn cục này một cách an toàn. Bản chất và cách quản lý cụ thể của các tài nguyên này phụ thuộc vào implementation. Xét cho cùng, tiện ích bên ngoài của runtime toàn cục chỉ giới hạn ở việc quản lý các trình thông dịch.

Ngược lại, về mặt khái niệm, "interpreter" chính là thứ mà chúng ta thường nghĩ đến khi nói về "Python runtime" (đầy đủ tính năng). Khi machine code đang thực thi trong một host thread tương tác với Python runtime, nó gọi vào Python trong ngữ cảnh của một interpreter cụ thể.

.. note::

   Thuật ngữ "interpreter" ở đây không giống với "bytecode interpreter", vốn thường xuyên chạy trong các thread để thực thi mã Python đã được biên dịch.

   Trong một thế giới lý tưởng, "Python runtime" sẽ dùng để chỉ thứ mà hiện nay chúng ta gọi là "interpreter". Tuy nhiên, nó đã được gọi là "interpreter" ít nhất từ khi được giới thiệu vào năm 1997 (`CPython:a027efa5b`_).

   .. _CPython:a027efa5b: https://github.com/python/cpython/commit/a027efa5b

Mỗi interpreter đóng gói hoàn toàn mọi trạng thái không thuộc phạm vi toàn process và không dành riêng cho thread mà Python runtime cần để hoạt động. Đáng chú ý là trạng thái của interpreter được duy trì giữa các lần sử dụng. Trạng thái này bao gồm những dữ liệu nền tảng như :data:`sys.modules`. Runtime đảm bảo nhiều thread sử dụng cùng một interpreter sẽ chia sẻ dữ liệu đó một cách an toàn.

Một Python implementation có thể hỗ trợ sử dụng đồng thời nhiều interpreter trong cùng một process. Chúng độc lập và được cô lập với nhau. Ví dụ, mỗi interpreter có riêng
:data:`sys.modules`.

Đối với trạng thái runtime dành riêng cho thread, mỗi interpreter có một tập hợp các thread state do nó quản lý, tương tự như cách runtime toàn cục chứa một tập hợp các interpreter. Nó có thể có thread state cho số lượng host thread tùy theo nhu cầu. Thậm chí, nó có thể có nhiều thread state cho cùng một host thread, mặc dù trường hợp này không phổ biến.

Về mặt khái niệm, mỗi trạng thái luồng chứa toàn bộ dữ liệu runtime dành riêng cho luồng mà một interpreter cần để hoạt động trong một luồng máy chủ. Trạng thái luồng bao gồm exception hiện đang được raised và call stack Python của luồng. Nó có thể bao gồm các tài nguyên khác dành riêng cho luồng.

.. note::

   Thuật ngữ "Python thread" đôi khi có thể dùng để chỉ một trạng thái luồng, nhưng thông thường nó có nghĩa là một luồng được tạo bằng module :mod:`threading`.

Trong suốt vòng đời của mình, mỗi trạng thái luồng luôn gắn với chính xác một interpreter và chính xác một luồng máy chủ. Trạng thái đó sẽ chỉ được sử dụng trong luồng đó và với interpreter đó.

Nhiều trạng thái luồng có thể được gắn với cùng một luồng máy chủ, dù là với các interpreter khác nhau hay thậm chí cùng một interpreter. Tuy nhiên, đối với bất kỳ luồng máy chủ nào, tại một thời điểm chỉ một trong các trạng thái luồng được gắn với nó có thể được luồng đó sử dụng.

Các trạng thái luồng được cô lập và độc lập với nhau, đồng thời không chia sẻ dữ liệu nào, ngoại trừ khả năng cùng chia sẻ một interpreter và các đối tượng hoặc tài nguyên khác thuộc về interpreter đó.

Sau khi chương trình đang chạy, có thể tạo các luồng Python mới bằng cách sử dụng
module :mod:`threading` (trên các nền tảng và bản triển khai Python có hỗ trợ luồng). Có thể tạo thêm các tiến trình bằng cách sử dụng
Các mô-đun :mod:`os`, :mod:`subprocess` và :mod:`multiprocessing`. Có thể tạo và sử dụng các interpreter bằng
Mô-đun :mod:`~concurrent.interpreters`. Có thể chạy các coroutine (async) bằng :mod:`asyncio` trong mỗi interpreter, thường chỉ trong một thread (thường là thread chính).


.. rubric:: Chú thích cuối trang

.. [#] Hạn chế này xảy ra vì mã được thực thi bởi các thao tác này không có sẵn tại thời điểm mô-đun được biên dịch.
