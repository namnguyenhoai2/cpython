.. _mod-weakref:

:mod:`!weakref` --- Tham chiếu yếu
==================================

.. module:: weakref
   :synopsis: Hỗ trợ tham chiếu yếu và từ điển yếu.

.. moduleauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. moduleauthor:: Neil Schemenauer <nas@arctrix.com>
.. moduleauthor:: Martin von Löwis <martin@loewis.home.cs.tu-berlin.de>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/weakref.py`

--------------

Mô-đun :mod:`!weakref` cho phép lập trình viên Python tạo ra các :dfn:`tham chiếu yếu` đến các đối tượng.

.. When making changes to the examples in this file, be sure to update
   Lib/test/test_weakref.py::libreftest too!

Trong phần sau, thuật ngữ :dfn:`đối tượng được tham chiếu` dùng để chỉ đối tượng được một tham chiếu yếu tham chiếu đến.

Một tham chiếu yếu đến một đối tượng không đủ để giữ đối tượng đó tồn tại: khi các tham chiếu duy nhất còn lại đến đối tượng được tham chiếu là các tham chiếu yếu,
:term:`garbage collection` có thể tự do hủy đối tượng được tham chiếu và sử dụng lại vùng nhớ của nó cho một mục đích khác. Tuy nhiên, cho đến khi đối tượng thực sự bị hủy, tham chiếu yếu vẫn có thể trả về đối tượng đó ngay cả khi không còn tham chiếu mạnh nào đến nó.

Một ứng dụng chính của weak reference là triển khai cache hoặc các ánh xạ lưu giữ những đối tượng lớn, trong đó mong muốn rằng một đối tượng lớn không được giữ lại chỉ vì nó xuất hiện trong cache hoặc ánh xạ.

Ví dụ, nếu bạn có một số đối tượng ảnh nhị phân lớn, bạn có thể muốn gắn một tên với mỗi đối tượng. Nếu bạn sử dụng từ điển Python để ánh xạ tên tới ảnh hoặc ảnh tới tên, các đối tượng ảnh sẽ vẫn tồn tại chỉ vì chúng xuất hiện dưới dạng giá trị hoặc khóa trong các từ điển.
Các lớp :class:`WeakKeyDictionary` và :class:`WeakValueDictionary` do module :mod:`!weakref` cung cấp là một lựa chọn thay thế, sử dụng weak reference để xây dựng các ánh xạ không giữ đối tượng tồn tại chỉ vì chúng xuất hiện trong các đối tượng ánh xạ. Ví dụ, nếu một đối tượng ảnh là một giá trị trong một
:class:`WeakValueDictionary`, thì khi các tham chiếu còn lại cuối cùng tới đối tượng ảnh đó chỉ là các weak reference do các ánh xạ yếu lưu giữ, garbage collection có thể thu hồi đối tượng này và các mục tương ứng trong các ánh xạ yếu sẽ פשוט được xóa.

:class:`WeakKeyDictionary` và :class:`WeakValueDictionary` sử dụng weak reference trong phần triển khai, thiết lập các hàm callback trên những weak reference để thông báo cho các từ điển yếu khi một khóa hoặc giá trị đã được garbage collection thu hồi. :class:`WeakSet` triển khai interface :class:`set`, nhưng lưu giữ weak reference tới các phần tử của nó, giống như
:class:`WeakKeyDictionary`.

:class:`finalize` cung cấp một cách đơn giản để đăng ký một hàm dọn dẹp sẽ được gọi khi một đối tượng được garbage collection thu hồi. Cách này đơn giản hơn so với việc thiết lập một hàm callback trên weak reference thô, vì module tự động đảm bảo rằng finalizer vẫn tồn tại cho đến khi đối tượng được thu hồi.

Hầu hết các chương trình sẽ thấy rằng việc sử dụng một trong các kiểu container yếu này hoặc :class:`finalize` là tất cả những gì chúng cần -- thường không cần tự tạo weak reference trực tiếp. Cơ chế cấp thấp được cung cấp bởi mô-đun :mod:`!weakref` để phục vụ các mục đích sử dụng nâng cao.

Không phải mọi đối tượng đều có thể được tham chiếu yếu. Các đối tượng hỗ trợ weak reference bao gồm các instance của class, các hàm được viết bằng Python (nhưng không phải bằng C), các phương thức của instance, các set, frozenset, một số :term:`đối tượng tệp <file object>`, :term:`generator <generator>`, các đối tượng kiểu, socket, mảng, deque, các đối tượng mẫu biểu thức chính quy và các đối tượng code.

.. versionchanged:: 3.2
   Đã bổ sung hỗ trợ cho thread.lock, threading.Lock và các đối tượng code.

Một số kiểu dựng sẵn như :class:`list` và :class:`dict` không trực tiếp hỗ trợ weak reference nhưng có thể bổ sung hỗ trợ thông qua việc tạo lớp con::

   class Dict(dict):
       pass

   obj = Dict(red=1, green=2, blue=3)   # đối tượng này có thể được tham chiếu yếu

.. impl-detail::

   Các kiểu dựng sẵn khác như :class:`tuple` và :class:`int` không hỗ trợ weak reference ngay cả khi được tạo lớp con.

Các kiểu mở rộng có thể dễ dàng được làm cho hỗ trợ weak reference; xem
:ref:`weakref-support`.

Khi ``__slots__`` được định nghĩa cho một kiểu nhất định, hỗ trợ weak reference bị vô hiệu hóa trừ khi một chuỗi ``'__weakref__'`` cũng có mặt trong dãy chuỗi của khai báo ``__slots__``. Xem tài liệu :ref:`__slots__ documentation <slots>` để biết chi tiết.

.. class:: ref(object[, callback])

   Trả về một weak reference tới *đối tượng*. Có thể truy xuất đối tượng gốc bằng cách gọi đối tượng reference nếu đối tượng được tham chiếu vẫn còn tồn tại; nếu đối tượng được tham chiếu không còn tồn tại, việc gọi đối tượng reference sẽ khiến :const:`None` được trả về. Nếu *callback* được cung cấp và không phải :const:`None`, đồng thời đối tượng weakref được trả về vẫn còn tồn tại, callback sẽ được gọi khi đối tượng sắp được hoàn tất; đối tượng weak reference sẽ được truyền làm tham số duy nhất cho callback; đối tượng được tham chiếu sẽ không còn khả dụng.

   Có thể tạo nhiều weak reference cho cùng một đối tượng. Các callback được đăng ký cho từng weak reference sẽ được gọi theo thứ tự từ callback được đăng ký gần nhất đến callback được đăng ký sớm nhất.

   Các exception do callback tạo ra sẽ được ghi nhận trên đầu ra lỗi chuẩn, nhưng không thể được truyền ra ngoài; chúng được xử lý chính xác như các exception phát sinh từ phương thức :meth:`~object.__del__` của một đối tượng.

   Weak reference là :term:`hashable` nếu *đối tượng* có thể băm. Chúng vẫn giữ nguyên giá trị băm ngay cả sau khi *đối tượng* đã bị xóa. Nếu
   :func:`hash` chỉ được gọi lần đầu sau khi *đối tượng* đã bị xóa, lần gọi đó sẽ gây ra :exc:`TypeError`.

   Weak reference hỗ trợ kiểm tra tính bằng nhau, nhưng không hỗ trợ sắp xếp. Nếu các đối tượng được tham chiếu vẫn còn tồn tại, hai reference có quan hệ bằng nhau giống với các đối tượng được tham chiếu (không phụ thuộc vào *callback*). Nếu một trong hai đối tượng được tham chiếu đã bị xóa, các reference chỉ bằng nhau khi chính các đối tượng reference là cùng một đối tượng.

   Đây là một kiểu có thể tạo lớp con thay vì một hàm factory.

   Weak reference được :ref:`generic <generics>` theo kiểu của đối tượng mà chúng tham chiếu.

   .. attribute:: __callback__

      Thuộc tính chỉ đọc này trả về callback hiện được liên kết với weakref. Nếu không có callback hoặc đối tượng được weakref tham chiếu không còn tồn tại thì thuộc tính này sẽ có giá trị ``None``.

   .. versionchanged:: 3.4
      Đã thêm thuộc tính :attr:`__callback__`.


.. function:: proxy(object[, callback])

   Trả về một proxy tới *object* sử dụng weak reference. Điều này cho phép sử dụng proxy trong hầu hết ngữ cảnh thay vì phải giải tham chiếu rõ ràng như khi sử dụng các đối tượng weak reference. Đối tượng được trả về sẽ có kiểu là ``ProxyType`` hoặc ``CallableProxyType``, tùy thuộc vào việc *object* có callable hay không. Các đối tượng proxy không :term:`hashable` bất kể đối tượng được tham chiếu là gì; điều này tránh một số vấn đề liên quan đến bản chất có thể thay đổi của chúng và ngăn việc sử dụng chúng làm khóa từ điển. *callback* giống với tham số cùng tên của hàm :func:`ref`.

   Việc truy cập một thuộc tính của đối tượng proxy sau khi đối tượng được tham chiếu đã được garbage collected sẽ gây ra :exc:`ReferenceError`.

   .. versionchanged:: 3.8
      Đã mở rộng hỗ trợ toán tử trên các đối tượng proxy để bao gồm các toán tử nhân ma trận ``@`` và ``@=``.


.. function:: getweakrefcount(object)

   Trả về số lượng weak reference và proxy tham chiếu đến *object*.


.. function:: getweakrefs(object)

   Trả về danh sách tất cả các đối tượng weak reference và proxy tham chiếu đến *object*.


.. class:: WeakKeyDictionary([dict])

   Lớp mapping tham chiếu yếu đến các khóa. Các mục trong dictionary sẽ bị loại bỏ khi không còn strong reference nào đến khóa. Có thể sử dụng lớp này để liên kết dữ liệu bổ sung với một đối tượng do các phần khác của ứng dụng sở hữu mà không cần thêm thuộc tính vào các đối tượng đó. Điều này đặc biệt hữu ích với những đối tượng ghi đè các thao tác truy cập thuộc tính.

   Lưu ý rằng khi một khóa có giá trị bằng với khóa hiện có (nhưng không cùng identity) được chèn vào dictionary, nó sẽ thay thế giá trị nhưng không thay thế khóa hiện có. Do đó, khi tham chiếu đến khóa ban đầu bị xóa, mục tương ứng trong dictionary cũng bị xóa::

      >>> class T(str): pass
      ...
      >>> k1, k2 = T(), T()
      >>> d = weakref.WeakKeyDictionary()
      >>> d[k1] = 1   # d = {k1: 1}
      >>> d[k2] = 2   # d = {k1: 2}
      >>> del k1      # d = {}

   Một cách khắc phục là xóa key trước khi gán lại::

      >>> class T(str): pass
      ...
      >>> k1, k2 = T(), T()
      >>> d = weakref.WeakKeyDictionary()
      >>> d[k1] = 1   # d = {k1: 1}
      >>> del d[k1]
      >>> d[k2] = 2   # d = {k2: 2}
      >>> del k1      # d = {k2: 2}

   .. versionchanged:: 3.9
      Đã bổ sung hỗ trợ cho các toán tử ``|`` và ``|=``, như được chỉ định trong :pep:`584`.

Các đối tượng :class:`WeakKeyDictionary` có thêm một phương thức cho phép truy cập trực tiếp vào các tham chiếu nội bộ. Các tham chiếu này không được đảm bảo là "còn hiệu lực" tại thời điểm được sử dụng, vì vậy cần kiểm tra kết quả của việc gọi các tham chiếu trước khi sử dụng. Bạn có thể dùng cách này để tránh tạo ra các tham chiếu khiến garbage collector giữ các key lâu hơn cần thiết.


.. method:: WeakKeyDictionary.keyrefs()

   Trả về một iterable chứa các tham chiếu yếu đến các key.


.. class:: WeakValueDictionary([dict])

   Lớp ánh xạ tham chiếu yếu đến các giá trị. Các mục trong từ điển sẽ bị loại bỏ khi không còn tham chiếu mạnh nào đến giá trị.

   .. versionchanged:: 3.9
      Đã bổ sung hỗ trợ cho các toán tử ``|`` và ``|=``, như được chỉ định trong :pep:`584`.

Các đối tượng :class:`WeakValueDictionary` có thêm một phương thức gặp những vấn đề giống như phương thức :meth:`WeakKeyDictionary.keyrefs`.


.. method:: WeakValueDictionary.valuerefs()

   Trả về một đối tượng iterable gồm các tham chiếu yếu đến các giá trị.


.. class:: WeakSet([elements])

   Lớp tập hợp duy trì các tham chiếu yếu đến các phần tử của nó. Một phần tử sẽ bị loại bỏ khi không còn tham chiếu mạnh nào đến nó.


.. class:: WeakMethod(method[, callback])

   Một lớp con :class:`ref` tùy chỉnh mô phỏng một tham chiếu yếu đến một bound method (tức là một phương thức được định nghĩa trên một lớp và được tra cứu trên một thực thể). Vì bound method có tính tạm thời, một tham chiếu yếu tiêu chuẩn không thể giữ nó. :class:`WeakMethod` có mã đặc biệt để tạo lại bound method cho đến khi đối tượng hoặc hàm gốc bị hủy::

      >>> class C:
      ...     def method(self):
      ...         print("method called!")
      ...
      >>> c = C()
      >>> r = weakref.ref(c.method)
      >>> r()
      >>> r = weakref.WeakMethod(c.method)
      >>> r()
      <bound method C.method of <__main__.C object at 0x7fc859830220>>
      >>> r()()
      method called!
      >>> del c
      >>> gc.collect()
      0
      >>> r()
      >>>

   *callback* giống với tham số cùng tên của hàm :func:`ref`.

   .. versionadded:: 3.4

.. class:: finalize(obj, func, /, *args, **kwargs)

   Trả về một đối tượng finalizer có thể gọi, đối tượng này sẽ được gọi khi *obj* được thu gom rác. Không giống một weak reference thông thường, finalizer sẽ luôn tồn tại cho đến khi đối tượng tham chiếu được thu gom, giúp đơn giản hóa đáng kể việc quản lý vòng đời.

   Một finalizer được xem là *alive* cho đến khi nó được gọi (dù là gọi tường minh hay khi thu gom rác), và sau đó nó sẽ *dead*. Việc gọi một finalizer còn sống sẽ trả về kết quả của việc đánh giá ``func(*arg, **kwargs)``, trong khi việc gọi một finalizer đã chết sẽ trả về :const:`None`.

   Các exception do callback của finalizer phát sinh trong quá trình thu gom rác sẽ được hiển thị trên đầu ra lỗi chuẩn, nhưng không thể được truyền đi. Chúng được xử lý giống như các exception phát sinh từ phương thức :meth:`~object.__del__` của một đối tượng hoặc callback của một weak reference.

   Khi chương trình thoát (hoặc nói chung, tại :term:`interpreter shutdown`), mỗi finalizer còn sống sẽ được gọi, trừ khi thuộc tính :attr:`atexit` của nó đã được đặt thành false. Chúng được gọi theo thứ tự ngược với thứ tự tạo.

   Một finalizer sẽ không bao giờ gọi callback của nó trong giai đoạn sau của :term:`interpreter shutdown`, khi các biến toàn cục của module có thể đã bị thay thế bằng :const:`None`.

   .. method:: __call__()

      Nếu *self* còn sống thì đánh dấu nó là đã chết và trả về kết quả của việc gọi ``func(*args, **kwargs)``. Nếu *self* đã chết thì trả về
      :const:`None`.

   .. method:: detach()

      Nếu *self* còn sống thì đánh dấu nó là đã chết và trả về tuple ``(obj, func, args, kwargs)``. Nếu *self* đã chết thì trả về
      :const:`None`.

   .. method:: peek()

      Nếu *self* còn sống thì trả về tuple ``(obj, func, args, kwargs)``. Nếu *self* đã bị hủy thì trả về :const:`None`.

   .. attribute:: alive

      Thuộc tính có giá trị true nếu finalizer còn sống, và false trong trường hợp ngược lại.

   .. attribute:: atexit

      Một thuộc tính boolean có thể ghi, mặc định là true. Khi
      :term:`interpreter shutdown`, tất cả các finalizer còn sống mà
      :attr:`.atexit` có giá trị true sẽ được gọi theo thứ tự ngược với thứ tự tạo.

   .. note::

      Điều quan trọng là đảm bảo *func*, *args* và *kwargs* không trực tiếp hoặc gián tiếp sở hữu bất kỳ tham chiếu nào đến *obj*, vì nếu không thì *obj* sẽ không bao giờ được garbage collector thu gom. Đặc biệt, *func* không nên là bound method của *obj*.

   .. versionadded:: 3.4


.. class:: ReferenceType

   Đối tượng kiểu dùng cho các đối tượng weak reference.


.. class:: ProxyType

   Đối tượng kiểu dành cho các proxy của những đối tượng không thể gọi được.


.. class:: CallableProxyType

   Đối tượng kiểu dành cho các proxy của những đối tượng có thể gọi được.


.. data:: ProxyTypes

   Sequence chứa tất cả các đối tượng kiểu dành cho proxy. Điều này có thể giúp việc kiểm tra xem một đối tượng có phải là proxy hay không trở nên đơn giản hơn mà không phụ thuộc vào việc phải chỉ rõ tên của cả hai kiểu proxy.


.. seealso::

   :pep:`205` - Weak References
      Đề xuất và lý do cho tính năng này, bao gồm các liên kết đến những triển khai trước đây và thông tin về các tính năng tương tự trong những ngôn ngữ khác.


.. _weakref-objects:

Đối tượng tham chiếu yếu
------------------------

Đối tượng tham chiếu yếu không có phương thức và thuộc tính nào ngoài
:attr:`ref.__callback__`. Một đối tượng tham chiếu yếu cho phép lấy đối tượng được tham chiếu, nếu đối tượng đó vẫn còn tồn tại, bằng cách gọi nó:

   >>> import weakref
   >>> class Object:
   ...     pass
   ...
   >>> o = Object()
   >>> r = weakref.ref(o)
   >>> o2 = r()
   >>> o is o2
   True

Nếu đối tượng được tham chiếu không còn tồn tại, việc gọi đối tượng tham chiếu sẽ trả về
:const:`None`:

   >>> del o, o2
   >>> print(r())
   None

Nên kiểm tra xem đối tượng tham chiếu yếu còn tồn tại hay không bằng biểu thức ``ref() is not None``. Thông thường, mã ứng dụng cần sử dụng một đối tượng tham chiếu nên tuân theo mẫu sau::

   # r là một đối tượng tham chiếu yếu
   o = r()
   if o is None:
       # đối tượng được tham chiếu đã được garbage collector thu gom
       print("Object has been deallocated; can't frobnicate.")
   else:
       print("Object is still live!")
       o.do_something_useful()

Việc sử dụng một phép kiểm tra riêng cho "trạng thái tồn tại" sẽ tạo ra các điều kiện tranh đua trong các ứng dụng đa luồng; một luồng khác có thể khiến một tham chiếu yếu trở nên không hợp lệ trước khi tham chiếu yếu được gọi; thành ngữ thể hiện ở trên cũng an toàn trong các ứng dụng đa luồng cũng như ứng dụng đơn luồng.

Có thể tạo các phiên bản chuyên biệt của các đối tượng :class:`ref` thông qua cơ chế kế thừa. Cách này được sử dụng trong quá trình triển khai :class:`WeakValueDictionary` để giảm chi phí bộ nhớ cho mỗi mục trong mapping. Điều này có thể hữu ích nhất khi liên kết thêm thông tin với một tham chiếu, nhưng cũng có thể được dùng để chèn thêm xử lý vào các lần gọi lấy đối tượng được tham chiếu.

Ví dụ này cho thấy cách sử dụng một lớp con của :class:`ref` để lưu trữ thêm thông tin về một đối tượng và ảnh hưởng đến giá trị được trả về khi truy cập đối tượng được tham chiếu::

   import weakref

   class ExtendedRef(weakref.ref):
       def __init__(self, ob, callback=None, /, **annotations):
           super().__init__(ob, callback)
           self.__counter = 0
           for k, v in annotations.items():
               setattr(self, k, v)

       def __call__(self):
           """Return a pair containing the referent and the number of
           times the reference has been called.
           """
           ob = super().__call__()
           if ob is not None:
               self.__counter += 1
               ob = (ob, self.__counter)
           return ob


.. _weakref-example:

Ví dụ
-----

Ví dụ đơn giản này cho thấy cách một ứng dụng có thể sử dụng ID đối tượng để truy xuất các đối tượng mà nó đã từng thấy. ID của các đối tượng sau đó có thể được sử dụng trong các cấu trúc dữ liệu khác mà không buộc các đối tượng phải tiếp tục tồn tại, nhưng vẫn có thể truy xuất các đối tượng theo ID nếu chúng còn tồn tại.

.. Example contributed by Tim Peters.

::

   import weakref

   _id2obj_dict = weakref.WeakValueDictionary()

   def remember(obj):
       oid = id(obj)
       _id2obj_dict[oid] = obj
       return oid

   def id2obj(oid):
       return _id2obj_dict[oid]


.. _finalize-examples:

Đối tượng Finalizer
-------------------

Lợi ích chính của việc sử dụng :class:`finalize` là giúp đăng ký callback một cách đơn giản mà không cần giữ lại đối tượng finalizer được trả về. Ví dụ:

    >>> import weakref
    >>> class Object:
    ...     pass
    ...
    >>> kenny = Object()
    >>> weakref.finalize(kenny, print, "You killed Kenny!")  #doctest:+ELLIPSIS
    <finalize object at ...; for 'Object' at ...>
    >>> del kenny
    You killed Kenny!

Bạn cũng có thể gọi trực tiếp finalizer. Tuy nhiên, finalizer sẽ gọi callback nhiều nhất một lần.

    >>> def callback(x, y, z):
    ...     print("CALLBACK")
    ...     return x + y + z
    ...
    >>> obj = Object()
    >>> f = weakref.finalize(obj, callback, 1, 2, z=3)
    >>> assert f.alive
    >>> assert f() == 6
    CALLBACK
    >>> assert not f.alive
    >>> f()                     # callback không được gọi vì finalizer đã chết
    >>> del obj                 # callback không được gọi vì finalizer đã chết

Bạn có thể hủy đăng ký một finalizer bằng method :meth:`~finalize.detach` của nó. Việc này sẽ hủy finalizer và trả về các đối số được truyền cho constructor khi nó được tạo.

    >>> obj = Object()
    >>> f = weakref.finalize(obj, callback, 1, 2, z=3)
    >>> f.detach()                                           #doctest:+ELLIPSIS
    (<...Object object ...>, <function callback ...>, (1, 2), {'z': 3})
    >>> newobj, func, args, kwargs = _
    >>> assert not f.alive
    >>> assert newobj is obj
    >>> assert func(*args, **kwargs) == 6
    CALLBACK

Nếu bạn không đặt thuộc tính :attr:`~finalize.atexit` thành
:const:`False`, một finalizer sẽ được gọi khi chương trình thoát nếu nó vẫn còn hoạt động. Ví dụ

.. doctest::
   :options: +SKIP

   >>> obj = Object()
   >>> weakref.finalize(obj, print, "obj dead or exiting")
   <finalize object at ...; for 'Object' at ...>
   >>> exit()
   obj dead or exiting


So sánh các finalizer với các method :meth:`~object.__del__`
------------------------------------------------------------

Giả sử chúng ta muốn tạo một class mà các instance của nó biểu diễn các thư mục tạm thời. Các thư mục này phải được xóa cùng với nội dung của chúng khi sự kiện đầu tiên trong các sự kiện sau đây xảy ra:

* đối tượng được garbage collect,
* phương thức :meth:`!remove` của đối tượng được gọi, hoặc
* chương trình kết thúc.

Chúng ta có thể thử triển khai class này bằng phương thức :meth:`~object.__del__` như sau::

    class TempDir:
        def __init__(self):
            self.name = tempfile.mkdtemp()

        def remove(self):
            if self.name is not None:
                shutil.rmtree(self.name)
                self.name = None

        @property
        def removed(self):
            return self.name is None

        def __del__(self):
            self.remove()

Bắt đầu từ Python 3.4, các phương thức :meth:`~object.__del__` không còn ngăn các reference cycle được garbage collect, và các biến toàn cục của module không còn bị buộc phải :const:`None` trong :term:`interpreter shutdown`. Vì vậy, đoạn mã này sẽ hoạt động mà không gặp vấn đề nào trên CPython.

Tuy nhiên, việc xử lý các phương thức :meth:`~object.__del__` nổi tiếng là phụ thuộc vào từng implementation, vì nó phụ thuộc vào các chi tiết nội bộ trong implementation của garbage collector của interpreter.

Một giải pháp thay thế mạnh mẽ hơn là định nghĩa một finalizer chỉ tham chiếu đến các hàm và đối tượng cụ thể mà nó cần, thay vì có quyền truy cập vào toàn bộ trạng thái của đối tượng::

    class TempDir:
        def __init__(self):
            self.name = tempfile.mkdtemp()
            self._finalizer = weakref.finalize(self, shutil.rmtree, self.name)

        def remove(self):
            self._finalizer()

        @property
        def removed(self):
            return not self._finalizer.alive

Được định nghĩa như vậy, finalizer của chúng ta chỉ nhận được tham chiếu đến những chi tiết cần thiết để dọn dẹp thư mục đúng cách. Nếu đối tượng không bao giờ được garbage collector thu gom, finalizer vẫn sẽ được gọi khi chương trình thoát.

Một ưu điểm khác của finalizer dựa trên weakref là chúng có thể được dùng để đăng ký finalizer cho các class mà định nghĩa do bên thứ ba kiểm soát, chẳng hạn như chạy mã khi một module được dỡ tải::

    import weakref, sys
    def unloading_module():
        # tham chiếu ngầm đến các biến toàn cục của module từ phần thân hàm
    weakref.finalize(sys.modules[__name__], unloading_module)


.. note::

   Nếu bạn tạo một đối tượng finalizer trong một daemonic thread ngay khi chương trình thoát, finalizer có thể không được gọi lúc thoát. Tuy nhiên, trong một daemonic thread
   :func:`atexit.register`, ``try: ... finally: ...`` và ``with: ...`` cũng không đảm bảo rằng quá trình dọn dẹp sẽ diễn ra.
