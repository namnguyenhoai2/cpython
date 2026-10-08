:mod:`!pickle` --- Tuần tự hóa đối tượng Python
===============================================

.. module:: pickle
   :synopsis: Chuyển đổi các đối tượng Python thành các luồng byte và ngược lại.

.. sectionauthor:: Jim Kerr <jbkerr@sr.hp.com>.
.. sectionauthor:: Barry Warsaw <barry@python.org>

**Mã nguồn:** :source:`Lib/pickle.py`

.. index::
   single: persistence
   pair: persistent; objects
   pair: serializing; objects
   pair: marshalling; objects
   pair: flattening; objects
   pair: pickling; objects

--------------

Mô-đun :mod:`!pickle` triển khai các giao thức nhị phân để tuần tự hóa và giải tuần tự hóa một cấu trúc đối tượng Python.  *"Pickling"* là quá trình chuyển một hệ phân cấp đối tượng Python thành một luồng byte, còn *"unpickling"* là thao tác ngược lại, trong đó một luồng byte (từ :term:`binary file` hoặc :term:`bytes-like object`) được chuyển đổi trở lại thành một hệ phân cấp đối tượng.  Pickling (và unpickling) còn được gọi là "serialization", "marshalling," [#]_ hoặc "flattening"; tuy nhiên, để tránh nhầm lẫn, các thuật ngữ được sử dụng ở đây là "pickling" và "unpickling".

.. warning::

   Mô-đun ``pickle`` **không an toàn**. Chỉ unpickle dữ liệu mà bạn tin cậy.

   Có thể tạo dữ liệu pickle độc hại khiến **thực thi mã tùy ý trong quá trình unpickling**. Không bao giờ unpickle dữ liệu có thể đến từ một nguồn không đáng tin cậy hoặc đã bị giả mạo.

   Hãy cân nhắc việc ký dữ liệu bằng :mod:`hmac` nếu bạn cần đảm bảo dữ liệu chưa bị giả mạo.

   Các định dạng serialization an toàn hơn như :mod:`json` có thể phù hợp hơn nếu bạn đang xử lý dữ liệu không đáng tin cậy. Xem :ref:`comparison-with-json`.


Mối quan hệ với các module Python khác
--------------------------------------

So sánh với ``marshal``
^^^^^^^^^^^^^^^^^^^^^^^

Python có một module serialization nguyên thủy hơn có tên là :mod:`marshal`, nhưng nhìn chung :mod:`!pickle` luôn nên là cách ưu tiên để serialize các object Python. :mod:`marshal` chủ yếu tồn tại để hỗ trợ các tệp :file:`.pyc` của Python.

Module :mod:`!pickle` khác với :mod:`marshal` ở một số điểm quan trọng:

* Không thể sử dụng :mod:`marshal` để serialize các class do người dùng định nghĩa và các instance của chúng. Tuy nhiên, :mod:`!pickle` có thể lưu và khôi phục các instance của class một cách minh bạch; nhưng định nghĩa class phải có thể import được và nằm trong cùng module như khi object được pickle.

* Định dạng serialization :mod:`marshal` không được đảm bảo là portable giữa các phiên bản Python. Vì nhiệm vụ chính của nó là hỗ trợ
  Đối với các tệp :file:`.pyc`, các nhà triển khai Python bảo lưu quyền thay đổi định dạng tuần tự hóa theo những cách không tương thích ngược nếu nhu cầu phát sinh. Định dạng tuần tự hóa :mod:`!pickle` được đảm bảo tương thích ngược giữa các bản phát hành Python, miễn là chọn một pickle protocol tương thích và mã pickling, unpickling xử lý các khác biệt về kiểu dữ liệu giữa Python 2 và Python 3 nếu dữ liệu của bạn đi qua ranh giới ngôn ngữ đặc biệt gây gián đoạn đó.


.. _comparison-with-json:

So sánh với ``json``
^^^^^^^^^^^^^^^^^^^^

Có những khác biệt cơ bản giữa các pickle protocol và `JSON (JavaScript Object Notation) <https://json.org>`_:

* JSON là một định dạng tuần tự hóa dạng văn bản (nó xuất ra văn bản unicode, mặc dù phần lớn thời gian văn bản này sau đó được mã hóa thành ``utf-8``), trong khi pickle là một định dạng tuần tự hóa nhị phân;

* JSON có thể đọc được bởi con người, còn pickle thì không;

* JSON có khả năng tương tác và được sử dụng rộng rãi bên ngoài hệ sinh thái Python, còn pickle chỉ dành riêng cho Python;

* Theo mặc định, JSON chỉ có thể biểu diễn một tập hợp con các kiểu dựng sẵn của Python và không thể biểu diễn các lớp tùy chỉnh; pickle có thể biểu diễn một số lượng cực lớn các kiểu Python (nhiều kiểu trong số đó được xử lý tự động nhờ sử dụng khéo léo các cơ chế introspection của Python; những trường hợp phức tạp có thể được giải quyết bằng cách triển khai :ref:`specific object APIs <pickle-inst>`);

* Không giống pickle, việc deserialize JSON không đáng tin cậy tự nó không tạo ra lỗ hổng cho phép thực thi mã tùy ý.

.. seealso::
   Mô-đun :mod:`json`: một mô-đun trong standard library cho phép serialize và deserialize JSON.


.. _pickle-protocols:

Định dạng luồng dữ liệu
-----------------------

.. index::
   single: External Data Representation

Định dạng dữ liệu được :mod:`!pickle` sử dụng dành riêng cho Python. Điều này có ưu điểm là không bị các tiêu chuẩn bên ngoài như JSON áp đặt hạn chế (JSON không thể biểu diễn việc chia sẻ con trỏ); tuy nhiên, điều đó có nghĩa là các chương trình không viết bằng Python có thể không tái tạo được các đối tượng Python đã được pickle.

Theo mặc định, định dạng dữ liệu :mod:`!pickle` sử dụng biểu diễn nhị phân tương đối nhỏ gọn. Nếu cần kích thước tối ưu, bạn có thể
:doc:`nén <archiving>` dữ liệu đã được pickle.

Mô-đun :mod:`pickletools` chứa các công cụ để phân tích các luồng dữ liệu được tạo bởi :mod:`!pickle`. Mã nguồn :mod:`pickletools` có các chú thích chi tiết về những opcode được các giao thức pickle sử dụng.

Hiện có 6 protocol khác nhau có thể được sử dụng để pickling. Protocol được sử dụng càng cao thì phiên bản Python cần thiết để đọc pickle được tạo ra càng mới.

* Protocol phiên bản 0 là protocol "con người có thể đọc được" ban đầu và tương thích ngược với các phiên bản Python trước đó.

* Protocol phiên bản 1 là một định dạng nhị phân cũ, cũng tương thích với các phiên bản Python trước đó.

* Protocol phiên bản 2 được giới thiệu trong Python 2.3. Protocol này cung cấp khả năng pickling hiệu quả hơn nhiều cho :term:`new-style classes <new-style class>`. Tham khảo :pep:`307` để biết thông tin về những cải tiến do protocol 2 mang lại.

* Protocol phiên bản 3 được bổ sung trong Python 3.0. Protocol này có hỗ trợ rõ ràng cho
  :class:`bytes` objects và không thể được unpickle bằng Python 2.x. Đây là protocol mặc định trong Python 3.0--3.7.

* Protocol phiên bản 4 được bổ sung trong Python 3.4. Protocol này bổ sung hỗ trợ cho các đối tượng rất lớn, pickling nhiều loại đối tượng hơn và một số tối ưu hóa định dạng dữ liệu. Đây là protocol mặc định trong Python 3.8--3.13. Tham khảo :pep:`3154` để biết thông tin về những cải tiến do protocol 4 mang lại.

* Protocol phiên bản 5 được bổ sung trong Python 3.8. Nó hỗ trợ dữ liệu ngoài luồng và tăng tốc dữ liệu trong luồng. Đây là protocol mặc định bắt đầu từ Python 3.14. Tham khảo :pep:`574` để biết thông tin về những cải tiến do protocol 5 mang lại.

.. note::
   Serialization là một khái niệm nguyên thủy hơn persistence; mặc dù
   :mod:`!pickle` đọc và ghi các đối tượng tệp, nhưng không xử lý vấn đề đặt tên cho các đối tượng persistent, cũng như vấn đề (thậm chí phức tạp hơn) về việc truy cập đồng thời vào các đối tượng persistent. Module :mod:`!pickle` có thể chuyển đổi một đối tượng phức tạp thành một luồng byte và chuyển đổi luồng byte đó thành một đối tượng có cùng cấu trúc bên trong. Có lẽ cách hiển nhiên nhất để sử dụng các luồng byte này là ghi chúng vào một tệp, nhưng cũng có thể gửi chúng qua mạng hoặc lưu trữ chúng trong cơ sở dữ liệu. Module :mod:`shelve` cung cấp một giao diện đơn giản để pickle và unpickle các đối tượng trên các tệp cơ sở dữ liệu kiểu DBM.


Giao diện module
----------------

Để serialize một hệ phân cấp đối tượng, bạn chỉ cần gọi hàm :func:`dumps`. Tương tự, để de-serialize một luồng dữ liệu, bạn gọi hàm :func:`loads`. Tuy nhiên, nếu muốn kiểm soát nhiều hơn việc serialize và de-serialize, bạn có thể lần lượt tạo một đối tượng :class:`Pickler` hoặc :class:`Unpickler`.

Module :mod:`!pickle` cung cấp các hằng số sau:


.. data:: HIGHEST_PROTOCOL

   Một số nguyên, :ref:`phiên bản giao thức <pickle-protocols>` cao nhất hiện có. Giá trị này có thể được truyền dưới dạng *giao thức* cho các hàm
   :func:`dump` và :func:`dumps`, cũng như constructor :class:`Pickler`.

.. data:: DEFAULT_PROTOCOL

   Một số nguyên, phiên bản protocol mặc định :ref:`protocol version <pickle-protocols>` được sử dụng để pickle. Có thể nhỏ hơn :data:`HIGHEST_PROTOCOL`. Hiện tại, protocol mặc định là 5, được giới thiệu trong Python 3.8 và không tương thích với các phiên bản trước đó. Phiên bản này bổ sung hỗ trợ cho các buffer ngoài luồng, trong đó dữ liệu tương thích với :pep:`3118` có thể được truyền riêng khỏi luồng pickle chính.

   .. versionchanged:: 3.0

      Protocol mặc định là 3.

   .. versionchanged:: 3.8

      Protocol mặc định là 4.

   .. versionchanged:: 3.14

      Protocol mặc định là 5.

Module :mod:`!pickle` cung cấp các hàm sau để giúp quá trình pickle thuận tiện hơn:

.. function:: dump(obj, file, protocol=None, *, fix_imports=True, buffer_callback=None)

   Ghi biểu diễn đã pickle của đối tượng *obj* vào tệp đã mở
   :term:`file object` *file*.  Điều này tương đương với ``Pickler(file, protocol).dump(obj)``.

   Các đối số *file*, *protocol*, *fix_imports* và *buffer_callback* có cùng ý nghĩa như trong hàm khởi tạo :class:`Pickler`.

   .. versionchanged:: 3.8
      Đối số *buffer_callback* đã được thêm.

.. function:: dumps(obj, protocol=None, *, fix_imports=True, buffer_callback=None)

   Trả về biểu diễn đã được pickle của đối tượng *obj* dưới dạng một đối tượng :class:`bytes`, thay vì ghi đối tượng đó vào tệp.

   Các đối số *protocol*, *fix_imports* và *buffer_callback* có cùng ý nghĩa như trong hàm khởi tạo :class:`Pickler`.

   .. versionchanged:: 3.8
      Đối số *buffer_callback* đã được thêm.

.. function:: load(file, *, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)

   Đọc biểu diễn đã được pickle của một đối tượng từ :term:`file object` *file* đang mở và trả về hệ phân cấp đối tượng được tái tạo như đã chỉ định trong đó. Điều này tương đương với ``Unpickler(file).load()``.

   Phiên bản protocol của pickle được tự động phát hiện, vì vậy không cần đối số protocol. Các byte nằm sau phần biểu diễn pickle của đối tượng sẽ bị bỏ qua.

   Các đối số *file*, *fix_imports*, *encoding*, *errors*, *strict* và *buffers* có cùng ý nghĩa như trong constructor :class:`Unpickler`.

   .. versionchanged:: 3.8
      Đối số *buffers* đã được bổ sung.

.. function:: loads(data, /, *, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)

   Trả về cấu trúc phân cấp đối tượng đã được tái tạo từ biểu diễn pickle *data* của một đối tượng. *data* phải là một :term:`bytes-like object`.

   Phiên bản protocol của pickle được tự động phát hiện, vì vậy không cần đối số protocol. Các byte nằm sau phần biểu diễn pickle của đối tượng sẽ bị bỏ qua.

   Các đối số *fix_imports*, *encoding*, *errors*, *strict* và *buffers* có cùng ý nghĩa như trong constructor :class:`Unpickler`.

   .. versionchanged:: 3.8
      Đối số *buffers* đã được bổ sung.


Mô-đun :mod:`!pickle` định nghĩa ba ngoại lệ:

.. exception:: PickleError

   Lớp cơ sở chung cho các ngoại lệ pickling khác. Lớp này kế thừa từ
   :exc:`Exception`.

.. exception:: PicklingError

   Ngoại lệ được phát sinh khi :class:`Pickler` gặp một đối tượng không thể pickling. Lớp này kế thừa từ :exc:`PickleError`.

   Tham khảo :ref:`pickle-picklable` để tìm hiểu những loại đối tượng nào có thể được pickling.

.. exception:: UnpicklingError

   Ngoại lệ được phát sinh khi xảy ra sự cố trong quá trình unpickling một đối tượng, chẳng hạn như dữ liệu bị hỏng hoặc vi phạm bảo mật. Lớp này kế thừa từ :exc:`PickleError`.

   Lưu ý rằng các ngoại lệ khác cũng có thể được phát sinh trong quá trình unpickling, bao gồm nhưng không nhất thiết giới hạn ở AttributeError, EOFError, ImportError và IndexError.


Mô-đun :mod:`!pickle` xuất ba lớp, :class:`Pickler`,
:class:`Unpickler` và :class:`PickleBuffer`:​

.. class:: Pickler(file, protocol=None, *, fix_imports=True, buffer_callback=None)

   Hàm này nhận một tệp nhị phân để ghi luồng dữ liệu pickle.

   Đối số *protocol*, là một số nguyên, cho biết pickler sẽ sử dụng protocol được chỉ định; các protocol được hỗ trợ là từ 0 đến :data:`HIGHEST_PROTOCOL`. Nếu không được chỉ định, giá trị mặc định là :data:`DEFAULT_PROTOCOL`. Nếu chỉ định một số âm, :data:`HIGHEST_PROTOCOL` sẽ được chọn.

   Đối số *file* phải có phương thức write() chấp nhận một đối số bytes duy nhất. Do đó, đối số này có thể là một tệp trên đĩa được mở để ghi nhị phân, một
   :class:`io.BytesIO` instance hoặc bất kỳ đối tượng tùy chỉnh nào khác đáp ứng giao diện này.

   Nếu *fix_imports* là true và *protocol* nhỏ hơn 3, pickle sẽ cố ánh xạ các tên mới trong Python 3 sang tên module cũ được sử dụng trong Python 2, để luồng dữ liệu pickle có thể đọc được bằng Python 2.

   Nếu *buffer_callback* là ``None`` (mặc định), các buffer view sẽ được tuần tự hóa vào *file* như một phần của luồng pickle.

   Nếu *buffer_callback* không phải là ``None``, thì nó có thể được gọi nhiều lần với một buffer view. Nếu callback trả về một giá trị false (chẳng hạn như ``None``), buffer được cung cấp sẽ được xử lý :ref:`out-of-band <pickle-oob>`; nếu không, buffer sẽ được tuần tự hóa in-band, tức là bên trong pickle stream.

   Đây là lỗi nếu *buffer_callback* không phải là ``None`` và *protocol* là ``None`` hoặc nhỏ hơn 5.

   .. versionchanged:: 3.8
      Đối số *buffer_callback* đã được thêm.

   .. method:: dump(obj)

      Ghi biểu diễn đã được pickle của *obj* vào đối tượng file đang mở được cung cấp trong constructor.

   .. method:: persistent_id(obj)

      Mặc định, không làm gì cả. Phương thức này tồn tại để subclass có thể override.

      Nếu :meth:`persistent_id` trả về ``None``, *obj* sẽ được pickle như bình thường. Bất kỳ giá trị nào khác sẽ khiến :class:`Pickler` phát ra giá trị được trả về dưới dạng persistent ID cho *obj*. Ý nghĩa của persistent ID này phải được định nghĩa bởi :meth:`Unpickler.persistent_load`. Lưu ý rằng giá trị được :meth:`persistent_id` trả về bản thân nó không thể có persistent ID.

      Xem :ref:`pickle-persistent` để biết chi tiết và các ví dụ về cách sử dụng.

      .. versionchanged:: 3.13
         Thêm phần triển khai mặc định của phương thức này trong phần triển khai bằng C của :class:`!Pickler`.

   .. attribute:: dispatch_table

      Bảng điều phối của một đối tượng pickler là một registry gồm các *hàm reduction* thuộc loại có thể được khai báo bằng
      :func:`copyreg.pickle`. Đây là một ánh xạ trong đó các khóa là các lớp, còn các giá trị là các hàm reduction. Một hàm reduction nhận một đối số thuộc lớp tương ứng và phải tuân theo cùng interface như một phương thức :meth:`~object.__reduce__`.

      Theo mặc định, một đối tượng pickler sẽ không có một
      :attr:`dispatch_table` attribute và thay vào đó sẽ sử dụng bảng điều phối toàn cục do module :mod:`copyreg` quản lý. Tuy nhiên, để tùy chỉnh việc pickling cho một đối tượng pickler cụ thể, bạn có thể đặt attribute :attr:`dispatch_table` thành một đối tượng dạng dict. Ngoài ra, nếu một subclass của :class:`Pickler` có một
      :attr:`dispatch_table` attribute thì attribute này sẽ được sử dụng làm bảng điều phối mặc định cho các instance của lớp đó.

      Xem :ref:`pickle-dispatch` để biết các ví dụ sử dụng.

      .. versionadded:: 3.3

   .. method:: reducer_override(obj)

      Reducer đặc biệt có thể được định nghĩa trong các lớp con của :class:`Pickler`. Phương thức này được ưu tiên hơn mọi reducer trong :attr:`dispatch_table`. Nó phải tuân theo cùng interface như một phương thức :meth:`~object.__reduce__`, và tùy chọn có thể trả về :data:`NotImplemented` để chuyển sang dùng
      Các reducer đã được đăng ký với :attr:`dispatch_table` để pickle ``obj``.

      Để xem ví dụ chi tiết, hãy xem :ref:`reducer_override`.

      .. versionadded:: 3.8

   .. attribute:: fast

      Đã lỗi thời. Bật fast mode nếu được đặt thành giá trị true. Fast mode vô hiệu hóa việc sử dụng memo, nhờ đó tăng tốc quá trình pickling bằng cách không tạo các opcode PUT thừa. Không nên sử dụng chế độ này với các đối tượng tự tham chiếu; nếu làm vậy, :class:`Pickler` sẽ đệ quy vô hạn.

      Sử dụng :func:`pickletools.optimize` nếu bạn cần các pickle nhỏ gọn hơn.

   .. method:: clear_memo()

      Xóa "memo" của pickler.

      Memo là cấu trúc dữ liệu ghi nhớ những đối tượng mà pickler đã thấy, nhờ đó các đối tượng dùng chung hoặc đệ quy được pickle bằng tham chiếu thay vì bằng giá trị. Phương thức này hữu ích khi tái sử dụng pickler.


.. class:: Unpickler(file, *, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)

   Đối tượng này nhận một tệp nhị phân để đọc một luồng dữ liệu pickle.

   Phiên bản protocol của pickle được tự động phát hiện, vì vậy không cần cung cấp đối số protocol.

   Đối số *file* phải có ba phương thức: phương thức read() nhận một đối số số nguyên, phương thức readinto() nhận một đối số bộ đệm và phương thức readline() không yêu cầu đối số nào, như trong
   :class:`io.BufferedIOBase` interface.  Vì vậy, *file* có thể là một tệp trên ổ đĩa được mở để đọc nhị phân, một đối tượng :class:`io.BytesIO`, hoặc bất kỳ đối tượng tùy chỉnh nào khác đáp ứng interface này.

   Các đối số tùy chọn *fix_imports*, *encoding* và *errors* được dùng để kiểm soát khả năng tương thích với các pickle stream được tạo bởi Python 2. Nếu *fix_imports* là true, pickle sẽ cố gắng ánh xạ các tên cũ của Python 2 sang các tên mới được dùng trong Python 3.  *encoding* và *errors* cho pickle biết cách giải mã các thực thể chuỗi 8-bit được pickle bởi Python 2; các giá trị mặc định lần lượt là 'ASCII' và 'strict'.  *encoding* có thể là 'bytes' để đọc các thực thể chuỗi 8-bit này dưới dạng đối tượng bytes. Việc sử dụng ``encoding='latin1'`` là bắt buộc khi unpickle các mảng NumPy và các thực thể của :class:`~datetime.datetime`, :class:`~datetime.date` và
   :class:`~datetime.time` được pickle bởi Python 2.

   Nếu *buffers* là ``None`` (mặc định), thì mọi dữ liệu cần thiết cho quá trình deserialization phải được chứa trong pickle stream.  Điều này có nghĩa là đối số *buffer_callback* đã là ``None`` khi một :class:`Pickler` được khởi tạo (hoặc khi :func:`dump` hoặc :func:`dumps` được gọi).

   Nếu *buffers* không phải là ``None``, thì đó phải là một iterable gồm các đối tượng hỗ trợ buffer, được sử dụng mỗi khi luồng pickle tham chiếu đến một buffer view :ref:`out-of-band <pickle-oob>`. Các buffer như vậy đã được truyền cho *buffer_callback* của một đối tượng Pickler.

   .. versionchanged:: 3.8
      Đối số *buffers* đã được bổ sung.

   .. method:: load()

      Đọc biểu diễn pickle của một đối tượng từ đối tượng tệp đang mở được cung cấp trong hàm khởi tạo, rồi trả về cấu trúc phân cấp đối tượng được tái tạo như đã chỉ định trong đó. Các byte nằm sau biểu diễn pickle của đối tượng sẽ bị bỏ qua.

   .. method:: persistent_load(pid)

      Theo mặc định, sẽ phát sinh một :exc:`UnpicklingError`.

      Nếu được định nghĩa, :meth:`persistent_load` sẽ trả về đối tượng được chỉ định bởi persistent ID *pid*. Nếu gặp một persistent ID không hợp lệ thì
      cần phát sinh :exc:`UnpicklingError`.

      Xem :ref:`pickle-persistent` để biết chi tiết và các ví dụ về cách sử dụng.

      .. versionchanged:: 3.13
         Thêm phần triển khai mặc định của phương thức này trong phần triển khai C của :class:`!Unpickler`.

   .. method:: find_class(module, name)

      Nhập *module* nếu cần và trả về đối tượng có tên *name* từ đó, trong đó các đối số *module* và *name* là các đối tượng :class:`str`. Lưu ý rằng, trái với tên gọi của nó, :meth:`find_class` cũng được dùng để tìm các hàm.

      Các lớp con có thể ghi đè phương thức này để kiểm soát loại đối tượng nào và cách chúng được tải, từ đó có khả năng giảm thiểu các rủi ro bảo mật. Tham khảo
      :ref:`pickle-restrict` để biết chi tiết.

      .. audit-event:: pickle.find_class module,name pickle.Unpickler.find_class

.. class:: PickleBuffer(buffer)

   Một wrapper cho một buffer biểu diễn dữ liệu có thể pickle. *buffer* phải là một
   đối tượng :ref:`buffer-providing <bufferobjects>`, chẳng hạn như một
   :term:`bytes-like object` hoặc một mảng N chiều.

   Bản thân :class:`PickleBuffer` cũng là một bộ cung cấp buffer, vì vậy có thể truyền nó cho các API khác yêu cầu một đối tượng cung cấp buffer, chẳng hạn như :class:`memoryview`.

   Các đối tượng :class:`PickleBuffer` chỉ có thể được tuần tự hóa bằng pickle protocol 5 trở lên. Chúng đủ điều kiện để thực hiện
   :ref:`tuần tự hóa ngoài băng <pickle-oob>`.

   .. versionadded:: 3.8

   .. method:: raw()

      Trả về một :class:`memoryview` của vùng bộ nhớ nằm bên dưới buffer này. Đối tượng được trả về là một memoryview một chiều, liên tục theo C với định dạng ``B`` (các byte không dấu). :exc:`BufferError` được phát sinh nếu buffer không liên tục theo C hoặc Fortran.

   .. method:: release()

      Giải phóng buffer bên dưới được đối tượng PickleBuffer cung cấp.


.. _pickle-picklable:

Những gì có thể được pickle và unpickle?
----------------------------------------

Các kiểu sau đây có thể được pickle:

* các hằng số tích hợp sẵn (``None``, ``True``, ``False``, ``Ellipsis``, và
  :data:`NotImplemented`);

* số nguyên, số dấu phẩy động, số phức;

* chuỗi, bytes, bytearray;

* tuple, list, set và dictionary chỉ chứa các đối tượng có thể pickle;

* các hàm (tích hợp sẵn và do người dùng định nghĩa) có thể truy cập từ cấp cao nhất của một module (sử dụng :keyword:`def`, không phải :keyword:`lambda`);

* các lớp có thể truy cập từ cấp cao nhất của một module;

* các instance của những lớp như vậy mà kết quả của việc gọi :meth:`~object.__getstate__` có thể pickle (xem phần :ref:`pickle-inst` để biết chi tiết).

Việc thử pickle các đối tượng không thể pickle sẽ gây ra ngoại lệ :exc:`PicklingError`; khi điều này xảy ra, một số byte không xác định có thể đã được ghi vào tệp bên dưới. Việc thử pickle một cấu trúc dữ liệu có tính đệ quy cao có thể vượt quá độ sâu đệ quy tối đa; trong trường hợp này, :exc:`RecursionError` sẽ được phát sinh. Bạn có thể thận trọng tăng giới hạn này bằng cách
:func:`sys.setrecursionlimit`.

Lưu ý rằng các hàm (hàm tích hợp và hàm do người dùng định nghĩa) được pickle theo đầy đủ
:term:`qualified name`, chứ không theo giá trị. [#]_ Điều này có nghĩa là chỉ tên hàm được pickle, cùng với tên của module và các lớp chứa hàm đó. Cả mã của hàm lẫn bất kỳ thuộc tính hàm nào của nó đều không được pickle. Vì vậy, module định nghĩa phải có thể được import trong môi trường unpickling, và module đó phải chứa đối tượng có tên tương ứng; nếu không, một ngoại lệ sẽ được phát sinh. [#]_

Tương tự, các lớp được pickle theo tên đầy đủ, vì vậy các hạn chế tương tự cũng được áp dụng trong môi trường unpickling. Lưu ý rằng không có mã hoặc dữ liệu nào của lớp được pickle, nên trong ví dụ sau, thuộc tính lớp ``attr`` không được khôi phục trong môi trường unpickling::

   class Foo:
       attr = 'A class attribute'

   picklestring = pickle.dumps(Foo)

Những hạn chế này là lý do các hàm và lớp có thể pickle phải được định nghĩa ở cấp cao nhất của một module.

Tương tự, khi các instance của lớp được pickle, mã và dữ liệu của lớp đó cũng không được pickle cùng với chúng. Chỉ dữ liệu của instance được pickle. Điều này được thực hiện có chủ đích, để bạn có thể sửa lỗi trong một lớp hoặc thêm các phương thức vào lớp mà vẫn tải được những đối tượng đã được tạo bằng phiên bản trước đó của lớp. Nếu dự định có các đối tượng tồn tại lâu dài và sẽ trải qua nhiều phiên bản của một lớp, bạn nên đặt một số phiên bản trong các đối tượng để phương thức :meth:`~object.__setstate__` của lớp có thể thực hiện các chuyển đổi phù hợp.


.. _pickle-inst:

Pickle các Instance của Lớp
---------------------------

.. currentmodule:: None

Trong phần này, chúng tôi mô tả các cơ chế chung có sẵn để bạn định nghĩa, tùy chỉnh và kiểm soát cách các instance của lớp được pickle và unpickle.

Trong hầu hết trường hợp, không cần thêm mã để các instance có thể được pickle. Theo mặc định, pickle sẽ lấy lớp và các thuộc tính của một instance bằng cách kiểm tra nội quan. Khi một instance của lớp được unpickle, phương thức :meth:`~object.__init__` của nó thường *không* được gọi. Hành vi mặc định trước hết tạo một instance chưa được khởi tạo, sau đó khôi phục các thuộc tính đã lưu. Đoạn mã sau đây minh họa cách triển khai hành vi này::

   def save(obj):
       return (obj.__class__, obj.__dict__)

   def restore(cls, attributes):
       obj = cls.__new__(cls)
       obj.__dict__.update(attributes)
       return obj

Các lớp có thể thay đổi hành vi mặc định bằng cách cung cấp một hoặc một số phương thức đặc biệt:

.. method:: object.__getnewargs_ex__()

   Trong các protocol 2 trở lên, những lớp triển khai
   phương thức :meth:`__getnewargs_ex__` có thể chỉ định các giá trị được truyền cho
   phương thức :meth:`__new__` khi unpickle. Phương thức này phải trả về một cặp ``(args, kwargs)`` trong đó *args* là một tuple gồm các đối số vị trí và *kwargs* là một dictionary gồm các đối số được đặt tên để tạo đối tượng. Các đối số này sẽ được truyền cho phương thức :meth:`__new__` khi unpickle.

   Bạn nên triển khai phương thức này nếu phương thức :meth:`__new__` của lớp yêu cầu các đối số chỉ dành cho keyword. Nếu không, để đảm bảo khả năng tương thích, bạn nên triển khai :meth:`__getnewargs__`.

   .. versionchanged:: 3.6
      :meth:`__getnewargs_ex__` is now used in protocols 2 and 3.


.. method:: object.__getnewargs__()

   Phương thức này có mục đích tương tự như :meth:`__getnewargs_ex__`, nhưng chỉ hỗ trợ các đối số vị trí. Phương thức phải trả về một tuple chứa các đối số ``args``, các đối số này sẽ được truyền cho phương thức :meth:`__new__` khi unpickling.

   :meth:`__getnewargs__` sẽ không được gọi nếu :meth:`__getnewargs_ex__` được định nghĩa.

   .. versionchanged:: 3.6
      Trước Python 3.6, :meth:`__getnewargs__` được gọi thay cho
      :meth:`__getnewargs_ex__` trong các protocol 2 và 3.


.. method:: object.__getstate__()

   Các class có thể kiểm soát thêm cách các instance của chúng được pickle bằng cách ghi đè phương thức :meth:`__getstate__`. Phương thức này được gọi và object được trả về sẽ được pickle làm nội dung của instance, thay cho state mặc định. Có một số trường hợp:

   * Đối với một class không có :attr:`~object.__dict__` của instance và không có
     :attr:`~object.__slots__`, state mặc định là ``None``.

   * Đối với một class có :attr:`~object.__dict__` của instance và không có
     :attr:`~object.__slots__`, trạng thái mặc định là ``self.__dict__``.

   * Đối với một class có :attr:`~object.__dict__` và
     :attr:`~object.__slots__`, trạng thái mặc định là một tuple gồm hai dictionary:  ``self.__dict__``, và một dictionary ánh xạ tên slot với các giá trị slot.  Chỉ những slot có giá trị mới được đưa vào dictionary sau.

   * Đối với một class có :attr:`~object.__slots__` và không có instance
     :attr:`~object.__dict__`, trạng thái mặc định là một tuple mà phần tử đầu tiên là ``None`` và phần tử thứ hai là một dictionary ánh xạ tên slot với các giá trị slot được mô tả trong mục trước.

   .. versionchanged:: 3.11
      Đã thêm implementation mặc định của phương thức ``__getstate__()`` trong
      :class:`object` lớp.


.. method:: object.__setstate__(state)

   Khi giải tuần tự hóa, nếu lớp định nghĩa :meth:`__setstate__`, phương thức này sẽ được gọi với trạng thái đã giải tuần tự. Trong trường hợp đó, đối tượng trạng thái không nhất thiết phải là một từ điển. Nếu không, trạng thái đã được pickle phải là một từ điển và các mục của nó được gán vào từ điển của thực thể mới.

   .. note::

      Nếu :meth:`__reduce__` trả về một trạng thái có giá trị ``None`` khi pickle, phương thức :meth:`__setstate__` sẽ không được gọi khi giải tuần tự hóa.


Tham khảo phần :ref:`pickle-state` để biết thêm thông tin về cách sử dụng các phương thức :meth:`~object.__getstate__` và :meth:`~object.__setstate__`.

.. note::

   Khi giải tuần tự hóa, một số phương thức như :meth:`~object.__getattr__`,
   :meth:`~object.__getattribute__`, hoặc :meth:`~object.__setattr__` có thể được gọi trên thực thể. Nếu các phương thức đó dựa vào một bất biến nội bộ nào đó đang đúng, kiểu này phải triển khai :meth:`~object.__new__` để thiết lập bất biến đó, vì :meth:`~object.__init__` không được gọi khi giải tuần tự hóa một thực thể.

.. index:: pair: copy; protocol

Như chúng ta sẽ thấy, pickle không trực tiếp sử dụng các phương thức được mô tả ở trên. Thực tế, các phương thức này là một phần của giao thức sao chép, giao thức này triển khai
phương thức đặc biệt :meth:`~object.__reduce__`. Giao thức copy cung cấp một giao diện thống nhất để lấy dữ liệu cần thiết cho việc pickle và sao chép đối tượng. [#]_

Mặc dù mạnh mẽ, việc triển khai :meth:`~object.__reduce__` trực tiếp trong các lớp của bạn dễ xảy ra lỗi. Vì lý do này, những người thiết kế lớp nên sử dụng giao diện cấp cao (tức là :meth:`~object.__getnewargs_ex__`, :meth:`~object.__getstate__` và
:meth:`~object.__setstate__`) bất cứ khi nào có thể. Tuy nhiên, chúng tôi sẽ trình bày những trường hợp mà việc sử dụng :meth:`!__reduce__` là lựa chọn duy nhất hoặc giúp pickle hiệu quả hơn, hoặc cả hai.

.. method:: object.__reduce__()

   Giao diện hiện được định nghĩa như sau. Phương thức :meth:`__reduce__` không nhận đối số nào và phải trả về một chuỗi hoặc tốt nhất là một tuple (đối tượng được trả về thường được gọi là "giá trị reduce").

   Nếu trả về một chuỗi, chuỗi đó phải được hiểu là tên của một biến toàn cục. Đó phải là tên cục bộ của đối tượng xét theo module của đối tượng; module pickle sẽ tìm kiếm trong namespace của module để xác định module của đối tượng: đối với một ``obj`` cần được pickle, thuộc tính ``__module__`` được tra cứu trực tiếp trên ``obj``, sau đó chuyển sang tra cứu trên kiểu của ``obj`` nếu không thiết lập thuộc tính instance ``__module__``. Hành vi này thường hữu ích cho các singleton.

   Khi trả về một tuple, tuple đó phải có từ hai đến sáu mục. Có thể bỏ qua các mục tùy chọn hoặc cung cấp ``None`` làm giá trị của chúng. Ý nghĩa của từng mục theo thứ tự là:

   .. XXX Mention __newobj__ special-case?

   * Một đối tượng callable sẽ được gọi để tạo phiên bản ban đầu của đối tượng.

   * Một tuple các đối số dành cho đối tượng callable. Phải cung cấp một tuple rỗng nếu callable không nhận bất kỳ đối số nào.

   * Tùy chọn, trạng thái của đối tượng, trạng thái này sẽ được truyền cho
     phương thức :meth:`__setstate__` như đã mô tả trước đó. Nếu đối tượng không có phương thức như vậy thì giá trị phải là một dictionary và sẽ được thêm vào thuộc tính :attr:`~object.__dict__` của đối tượng.

   * Tùy chọn, một iterator (không phải sequence) tạo ra các mục liên tiếp. Các mục này sẽ được nối vào đối tượng bằng ``obj.append(item)`` hoặc theo lô bằng ``obj.extend(list_of_items)``. Điều này chủ yếu được dùng cho các lớp con của list, nhưng cũng có thể được dùng bởi các lớp khác miễn là chúng có các phương thức :meth:`~sequence.append` và :meth:`~sequence.extend` với chữ ký phù hợp. (Việc sử dụng :meth:`!append` hay :meth:`!extend` phụ thuộc vào phiên bản giao thức pickle được dùng cũng như số lượng mục cần nối, vì vậy cả hai đều phải được hỗ trợ.)

   * Tùy chọn, một iterator (không phải sequence) tạo ra các cặp khóa-giá trị liên tiếp. Các mục này sẽ được lưu vào đối tượng bằng ``obj[key] = value``. Điều này chủ yếu được dùng cho các lớp con của dictionary, nhưng cũng có thể được dùng bởi các lớp khác miễn là chúng triển khai :meth:`__setitem__`.

   * Tùy chọn, một callable có chữ ký ``(obj, state)``. Callable này cho phép người dùng kiểm soát bằng lập trình hành vi cập nhật trạng thái của một đối tượng cụ thể, thay vì sử dụng phương thức ``obj`` tĩnh
     :meth:`__setstate__`. Nếu không phải ``None``, callable này sẽ được ưu tiên hơn ``obj``'s :meth:`__setstate__`.

     .. versionadded:: 3.8
        Mục tuple thứ sáu tùy chọn, ``(obj, state)``, đã được thêm vào.


.. method:: object.__reduce_ex__(protocol)

   Ngoài ra, có thể định nghĩa một phương thức :meth:`__reduce_ex__`. Điểm khác biệt duy nhất là phương thức này phải nhận một đối số số nguyên, là phiên bản giao thức. Khi được định nghĩa, pickle sẽ ưu tiên phương thức này hơn phương thức :meth:`__reduce__`. Ngoài ra, :meth:`__reduce__` tự động trở thành bí danh cho phiên bản mở rộng. Mục đích sử dụng chính của phương thức này là cung cấp các giá trị reduce tương thích ngược cho những bản phát hành Python cũ hơn.

.. currentmodule:: pickle

.. _pickle-persistent:

Lưu trữ đối tượng bên ngoài
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: persistent_id (pickle protocol)
   single: persistent_load (pickle protocol)

Để hỗ trợ việc lưu trữ đối tượng, module :mod:`!pickle` hỗ trợ khái niệm tham chiếu đến một đối tượng nằm ngoài luồng dữ liệu đã được pickle. Những đối tượng như vậy được tham chiếu bằng một ID bền vững, ID này phải là một chuỗi gồm các ký tự chữ và số (đối với protocol 0) [#]_ hoặc chỉ là một đối tượng bất kỳ (đối với mọi protocol mới hơn).

Việc phân giải các ID bền vững như vậy không được module :mod:`!pickle` định nghĩa; module này sẽ ủy quyền việc phân giải cho các phương thức do người dùng định nghĩa trên pickler và unpickler, :meth:`~Pickler.persistent_id` và
:meth:`~Unpickler.persistent_load` tương ứng.

Để pickle các đối tượng có ID bền vững bên ngoài, pickler phải có một phương thức :meth:`~Pickler.persistent_id` tùy chỉnh, nhận một đối tượng làm đối số và trả về ``None`` hoặc ID bền vững của đối tượng đó. Khi trả về ``None``, pickler chỉ pickle đối tượng như bình thường. Khi trả về một chuỗi ID bền vững, pickler sẽ pickle đối tượng đó cùng với một dấu đánh dấu để unpickler nhận diện nó là một ID bền vững.

Để unpickle các đối tượng bên ngoài, unpickler phải có một phương thức tùy chỉnh
:meth:`~Unpickler.persistent_load` nhận một đối tượng persistent ID và trả về đối tượng được tham chiếu.

Sau đây là một ví dụ toàn diện minh họa cách sử dụng persistent ID để pickle các đối tượng bên ngoài bằng tham chiếu.

.. literalinclude:: ../includes/dbpickle.py

.. _pickle-dispatch:

Bảng dispatch
^^^^^^^^^^^^^

Nếu muốn tùy chỉnh cách pickle một số lớp mà không ảnh hưởng đến bất kỳ mã nào khác phụ thuộc vào pickling, bạn có thể tạo một pickler với dispatch table riêng.

Dispatch table toàn cục do module :mod:`copyreg` quản lý có sẵn dưới dạng :data:`!copyreg.dispatch_table`. Vì vậy, bạn có thể chọn sử dụng một bản sao đã chỉnh sửa của :data:`!copyreg.dispatch_table` làm dispatch table riêng.

Ví dụ::

   f = io.BytesIO()
   p = pickle.Pickler(f)
   p.dispatch_table = copyreg.dispatch_table.copy()
   p.dispatch_table[SomeClass] = reduce_SomeClass

tạo một thể hiện của :class:`pickle.Pickler` với một bảng dispatch riêng, trong đó xử lý đặc biệt lớp ``SomeClass``. Ngoài ra, đoạn mã::

   class MyPickler(pickle.Pickler):
       dispatch_table = copyreg.dispatch_table.copy()
       dispatch_table[SomeClass] = reduce_SomeClass
   f = io.BytesIO()
   p = MyPickler(f)

thực hiện điều tương tự, nhưng theo mặc định, tất cả các thể hiện của ``MyPickler`` sẽ dùng chung bảng dispatch riêng. Mặt khác, đoạn mã::

   copyreg.pickle(SomeClass, reduce_SomeClass)
   f = io.BytesIO()
   p = pickle.Pickler(f)

sửa đổi bảng dispatch toàn cục được dùng chung bởi tất cả người dùng của mô-đun :mod:`copyreg`.

.. _pickle-state:

Xử lý các đối tượng có trạng thái
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: __getstate__() (copy protocol)
   single: __setstate__() (copy protocol)

Dưới đây là một ví dụ cho thấy cách sửa đổi hành vi pickling cho một lớp. Lớp :class:`!TextReader` bên dưới mở một tệp văn bản và trả về số dòng cùng nội dung dòng mỗi khi phương thức :meth:`!readline` của nó được gọi. Nếu một
thể hiện :class:`!TextReader` được pickle, tất cả các thuộc tính *ngoại trừ* thành viên đối tượng tệp đều được lưu. Khi thể hiện được giải pickle, tệp được mở lại và việc đọc tiếp tục từ vị trí trước đó. Các phương thức :meth:`!__setstate__` và
:meth:`!__getstate__` được dùng để triển khai hành vi này.::

   class TextReader:
       """Print and number lines in a text file."""

       def __init__(self, filename):
           self.filename = filename
           self.file = open(filename)
           self.lineno = 0

       def readline(self):
           self.lineno += 1
           line = self.file.readline()
           if not line:
               return None
           if line.endswith('\n'):
               line = line[:-1]
           return "%i: %s" % (self.lineno, line)

       def __getstate__(self):
           # Sao chép trạng thái của đối tượng từ self.__dict__, trong đó chứa
           # tất cả thuộc tính instance của chúng ta. Luôn sử dụng phương thức dict.copy()
           # để tránh sửa đổi trạng thái ban đầu.
           state = self.__dict__.copy()
           # Xóa các mục không thể pickle.
           del state['file']
           return state

       def __setstate__(self, state):
           # Khôi phục các thuộc tính instance (tức là filename và lineno).
           self.__dict__.update(state)
           # Khôi phục trạng thái của tệp đã mở trước đó. Để làm vậy, chúng ta cần
           # mở lại tệp và đọc từ đó cho đến khi số dòng được khôi phục.
           file = open(self.filename)
           for _ in range(self.lineno):
               file.readline()
           # Cuối cùng, lưu tệp.
           self.file = file


Một cách sử dụng mẫu có thể như sau::

   >>> reader = TextReader("hello.txt")
   >>> reader.readline()
   '1: Hello world!'
   >>> reader.readline()
   '2: I am line number two.'
   >>> new_reader = pickle.loads(pickle.dumps(reader))
   >>> new_reader.readline()
   '3: Goodbye!'

.. _reducer_override:

Tùy chỉnh reduction cho các kiểu, hàm và đối tượng khác
-------------------------------------------------------

.. versionadded:: 3.8

Đôi khi, :attr:`~Pickler.dispatch_table` có thể chưa đủ linh hoạt. Cụ thể, chúng ta có thể muốn tùy chỉnh quá trình pickling dựa trên một tiêu chí khác với kiểu của đối tượng, hoặc muốn tùy chỉnh quá trình pickling của các hàm và lớp.

Trong những trường hợp đó, có thể tạo lớp con từ lớp :class:`Pickler` và triển khai phương thức :meth:`~Pickler.reducer_override`. Phương thức này có thể trả về một tuple reduction tùy ý (xem :meth:`~object.__reduce__`). Ngoài ra, phương thức có thể trả về
:data:`NotImplemented` để quay lại hành vi truyền thống.

Nếu cả :attr:`~Pickler.dispatch_table` và
Sau khi :meth:`~Pickler.reducer_override` được định nghĩa, thì
Phương thức :meth:`~Pickler.reducer_override` được ưu tiên.

.. Note::
   Vì lý do hiệu năng, :meth:`~Pickler.reducer_override` có thể không được gọi đối với các đối tượng sau: ``None``, ``True``, ``False`` và các thực thể chính xác của :class:`int`, :class:`float`, :class:`bytes`,
   :class:`str`, :class:`dict`, :class:`set`, :class:`frozenset`, :class:`list` và :class:`tuple`.

Sau đây là một ví dụ đơn giản cho phép pickling và tái tạo một class nhất định::

   import io
   import pickle

   class MyClass:
       my_attribute = 1

   class MyPickler(pickle.Pickler):
       def reducer_override(self, obj):
           """Custom reducer for MyClass."""
           if getattr(obj, "__name__", None) == "MyClass":
               return type, (obj.__name__, obj.__bases__,
                             {'my_attribute': obj.my_attribute})
           else:
               # Đối với mọi đối tượng khác, dùng cơ chế reduction thông thường
               return NotImplemented

   f = io.BytesIO()
   p = MyPickler(f)
   p.dump(MyClass)

   del MyClass

   unpickled_class = pickle.loads(f.getvalue())

   assert isinstance(unpickled_class, type)
   assert unpickled_class.__name__ == "MyClass"
   assert unpickled_class.my_attribute == 1


.. _pickle-oob:

Bộ đệm ngoài băng
-----------------

.. versionadded:: 3.8

Trong một số ngữ cảnh, module :mod:`!pickle` được dùng để truyền một lượng dữ liệu khổng lồ. Vì vậy, việc giảm thiểu số lần sao chép bộ nhớ để duy trì hiệu năng và mức tiêu thụ tài nguyên có thể rất quan trọng. Tuy nhiên, hoạt động bình thường của module :mod:`!pickle`, khi chuyển đổi một cấu trúc đối tượng dạng đồ thị thành một luồng byte tuần tự, về bản chất bao gồm việc sao chép dữ liệu đến và đi từ luồng pickle.

Có thể bỏ qua ràng buộc này nếu cả *provider* (phần triển khai các kiểu đối tượng cần truyền) và *consumer* (phần triển khai hệ thống liên lạc) đều hỗ trợ các cơ chế truyền ngoài luồng do pickle protocol 5 trở lên cung cấp.

API của provider
^^^^^^^^^^^^^^^^

Các đối tượng dữ liệu lớn cần được pickle phải triển khai một phương thức :meth:`~object.__reduce_ex__` chuyên biệt cho protocol 5 trở lên, phương thức này trả về một
đối tượng :class:`PickleBuffer` (thay vì, chẳng hạn, một đối tượng :class:`bytes`) cho mọi dữ liệu lớn.

Một đối tượng :class:`PickleBuffer` *báo hiệu* rằng bộ đệm bên dưới đủ điều kiện để truyền dữ liệu ngoài luồng. Các đối tượng đó vẫn tương thích với cách sử dụng module :mod:`!pickle` thông thường. Tuy nhiên, consumer cũng có thể chủ động cho :mod:`!pickle` biết rằng họ sẽ tự xử lý các bộ đệm đó.

API của consumer
^^^^^^^^^^^^^^^^

Một hệ thống truyền thông có thể cho phép xử lý tùy chỉnh các đối tượng :class:`PickleBuffer` được tạo ra khi tuần tự hóa một đồ thị đối tượng.

Ở phía gửi, hệ thống cần truyền một đối số *buffer_callback* cho
:class:`Pickler` (hoặc cho hàm :func:`dump` hay :func:`dumps`), hàm này sẽ được gọi với mỗi :class:`PickleBuffer` được tạo ra trong quá trình pickle đồ thị đối tượng. Dữ liệu của các bộ đệm được tích lũy bởi *buffer_callback* sẽ không được sao chép vào luồng pickle; thay vào đó, chỉ một dấu đánh dấu nhẹ sẽ được chèn vào.

Ở phía nhận, hệ thống cần truyền một đối số *buffers* cho
:class:`Unpickler` (hoặc cho hàm :func:`load` hay :func:`loads`), đây là một iterable gồm các bộ đệm đã được truyền cho *buffer_callback*. Iterable đó phải tạo ra các bộ đệm theo đúng thứ tự chúng đã được truyền cho *buffer_callback*. Các bộ đệm đó sẽ cung cấp dữ liệu mà các hàm tái tạo của những đối tượng có quá trình pickle tạo ra
các đối tượng :class:`PickleBuffer` ban đầu cần.

Giữa phía gửi và phía nhận, hệ thống truyền thông có thể tự do triển khai cơ chế truyền riêng cho các bộ đệm ngoài băng. Các tối ưu hóa có thể bao gồm việc sử dụng bộ nhớ dùng chung hoặc nén phụ thuộc vào kiểu dữ liệu.

Ví dụ
^^^^^

Sau đây là một ví dụ đơn giản, trong đó chúng ta triển khai một lớp con :class:`bytearray` có thể tham gia vào quá trình pickle bộ đệm ngoài băng thông::

   class ZeroCopyByteArray(bytearray):

       def __reduce_ex__(self, protocol):
           if protocol >= 5:
               return type(self)._reconstruct, (PickleBuffer(self),), None
           else:
               # Không được sử dụng PickleBuffer với các giao thức pickle <= 4.
               return type(self)._reconstruct, (bytearray(self),)

       @classmethod
       def _reconstruct(cls, obj):
           with memoryview(obj) as m:
               # Lấy handle đến đối tượng bộ đệm ban đầu
               obj = m.obj
               if type(obj) is cls:
                   # Đối tượng bộ đệm ban đầu là ZeroCopyByteArray, trả về đối tượng đó
                   # nguyên trạng.
                   return obj
               else:
                   return cls(obj)

Hàm tái tạo (phương thức lớp ``_reconstruct``) trả về đối tượng cung cấp bộ đệm nếu đối tượng đó có đúng kiểu. Đây là một cách dễ dàng để mô phỏng hành vi zero-copy trong ví dụ đơn giản này.

Ở phía consumer, chúng ta có thể pickle các đối tượng đó theo cách thông thường; khi được unserialize, chúng sẽ cho chúng ta một bản sao của đối tượng ban đầu::

   b = ZeroCopyByteArray(b"abc")
   data = pickle.dumps(b, protocol=5)
   new_b = pickle.loads(data)
   print(b == new_b)  # Đúng
   print(b is new_b)  # Sai: một bản sao đã được tạo

Nhưng nếu chúng ta truyền một *buffer_callback* rồi cung cấp lại các buffer đã tích lũy khi unserialize, chúng ta có thể lấy lại đối tượng ban đầu::

   b = ZeroCopyByteArray(b"abc")
   buffers = []
   data = pickle.dumps(b, protocol=5, buffer_callback=buffers.append)
   new_b = pickle.loads(data, buffers=buffers)
   print(b == new_b)  # Đúng
   print(b is new_b)  # Đúng: không có bản sao nào được tạo

Ví dụ này bị giới hạn bởi thực tế là :class:`bytearray` tự cấp phát bộ nhớ: bạn không thể tạo một thực thể :class:`bytearray` được hỗ trợ bởi bộ nhớ của một đối tượng khác. Tuy nhiên, các kiểu dữ liệu của bên thứ ba như mảng NumPy không gặp giới hạn này và cho phép sử dụng pickle không sao chép (hoặc tạo ít bản sao nhất có thể) khi truyền dữ liệu giữa các process hoặc hệ thống riêng biệt.

.. seealso:: :pep:`574` -- Pickle giao thức 5 với dữ liệu ngoài băng


.. _pickle-restrict:

Hạn chế các đối tượng toàn cục
------------------------------

.. index::
   single: find_class() (pickle protocol)

Theo mặc định, thao tác unpickle sẽ import bất kỳ class hoặc function nào mà nó tìm thấy trong dữ liệu pickle. Đối với nhiều ứng dụng, hành vi này không thể chấp nhận được vì nó cho phép unpickler import và gọi mã tùy ý. Hãy xem luồng dữ liệu pickle được tạo thủ công này thực hiện điều gì khi được tải::

    >>> import pickle
    >>> pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
    hello world
    0

Trong ví dụ này, unpickler import function :func:`os.system` rồi áp dụng đối số chuỗi "echo hello world". Mặc dù ví dụ này vô hại, không khó để hình dung một ví dụ có thể gây hư hại cho hệ thống của bạn.

Vì lý do này, bạn có thể muốn kiểm soát những gì được unpickle bằng cách tùy chỉnh
:meth:`Unpickler.find_class`. Không giống như tên gọi của nó,
:meth:`Unpickler.find_class` được gọi mỗi khi một global (tức là một class hoặc một function) được yêu cầu. Vì vậy, bạn có thể hoàn toàn cấm các global hoặc giới hạn chúng vào một tập con an toàn.

Dưới đây là ví dụ về một unpickler chỉ cho phép một vài class an toàn từ
:mod:`builtins` module được tải::

   import builtins
   import io
   import pickle

   safe_builtins = {
       'range',
       'complex',
       'set',
       'frozenset',
       'slice',
   }

   class RestrictedUnpickler(pickle.Unpickler):

       def find_class(self, module, name):
           # Chỉ cho phép các class an toàn từ builtins.
           if module == "builtins" and name in safe_builtins:
               return getattr(builtins, name)
           # Cấm mọi thành phần khác.
           raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                        (module, name))

   def restricted_loads(s):
       """Helper function analogous to pickle.loads()."""
       return RestrictedUnpickler(io.BytesIO(s)).load()

Ví dụ sử dụng unpickler của chúng ta hoạt động như mong đợi::

    >>> restricted_loads(pickle.dumps([1, 2, range(15)]))
    [1, 2, range(0, 15)]
    >>> restricted_loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
    Traceback (most recent call last):
      ...
    pickle.UnpicklingError: global 'os.system' is forbidden
    >>> restricted_loads(b'cbuiltins\neval\n'
    ...                  b'(S\'getattr(__import__("os"), "system")'
    ...                  b'("echo hello world")\'\ntR.')
    Traceback (most recent call last):
      ...
    pickle.UnpicklingError: global 'builtins.eval' is forbidden


.. XXX Add note about how extension codes could evade our protection
   mechanism (e.g. cached classes do not invokes find_class()).

Như các ví dụ của chúng ta cho thấy, bạn phải cẩn thận với những gì cho phép được unpickle. Vì vậy, nếu bảo mật là mối quan tâm, bạn có thể cân nhắc các giải pháp thay thế như marshalling API trong :mod:`xmlrpc.client` hoặc các giải pháp của bên thứ ba.


Hiệu năng
---------

Các phiên bản gần đây của pickle protocol (từ protocol 2 trở lên) có các mã hóa nhị phân hiệu quả cho một số tính năng và kiểu dựng sẵn phổ biến. Ngoài ra, module :mod:`!pickle` còn có một trình tối ưu hóa trong suốt được viết bằng C.


.. _pickle-example:

Ví dụ
-----

Đối với đoạn mã đơn giản nhất, hãy sử dụng các hàm :func:`dump` và :func:`load`.::

   import pickle

   # Một tập hợp tùy ý gồm các đối tượng được pickle hỗ trợ.
   data = {
       'a': [1, 2.0, 3+4j],
       'b': ("character string", b"byte string"),
       'c': {None, True, False}
   }

   with open('data.pickle', 'wb') as f:
       # Pickle từ điển 'data' bằng protocol cao nhất hiện có.
       pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


Ví dụ sau đọc dữ liệu đã được pickle.::

   import pickle

   with open('data.pickle', 'rb') as f:
       # Phiên bản protocol được sử dụng sẽ được tự động phát hiện, vì vậy chúng ta không
       # cần chỉ định nó.
       data = pickle.load(f)


.. XXX: Add examples showing how to optimize pickles for size (like using
.. pickletools.optimize() or the gzip module).


.. _pickle-cli:

Giao diện dòng lệnh
-------------------

Mô-đun :mod:`!pickle` có thể được gọi như một script từ dòng lệnh và sẽ hiển thị nội dung của các tệp pickle. Tuy nhiên, khi tệp pickle bạn muốn kiểm tra đến từ một nguồn không đáng tin cậy, ``-m pickletools`` là lựa chọn an toàn hơn vì nó không thực thi bytecode pickle, xem
:ref:`cách sử dụng CLI của pickletools <pickletools-cli>`.

.. code-block:: bash

   python -m pickle pickle_file [pickle_file ...]

Tùy chọn sau được chấp nhận:

.. program:: pickle

.. option:: pickle_file

   Một tệp pickle cần đọc hoặc ``-`` để chỉ ra rằng sẽ đọc từ đầu vào chuẩn.


.. seealso::

   Mô-đun :mod:`copyreg`
      Đăng ký constructor giao diện Pickle cho các extension type.

   Mô-đun :mod:`pickletools`
      Các công cụ để làm việc với và phân tích dữ liệu đã được pickle.

   Mô-đun :mod:`shelve`
      Cơ sở dữ liệu đối tượng được lập chỉ mục; sử dụng :mod:`!pickle`.

   Mô-đun :mod:`copy`
      Sao chép đối tượng nông và sâu.

   Mô-đun :mod:`marshal`
      Serialization hiệu năng cao cho các kiểu dựng sẵn.


.. rubric:: Chú thích

.. [#] Đừng nhầm mô-đun này với mô-đun :mod:`marshal`

.. [#] Đây là lý do các hàm :keyword:`lambda` không thể được pickle:  tất cả
    các hàm :keyword:`!lambda` đều dùng chung một tên:  ``<lambda>``.

.. [#] Ngoại lệ được phát sinh nhiều khả năng sẽ là :exc:`ImportError` hoặc một
   :exc:`AttributeError` nhưng nó có thể là thứ khác.

.. [#] Mô-đun :mod:`copy` sử dụng giao thức này cho các thao tác sao chép nông và sao chép sâu.

.. [#] Giới hạn đối với các ký tự chữ và số là do các ID bền vững trong giao thức 0 được phân cách bằng ký tự xuống dòng. Do đó, nếu bất kỳ loại ký tự xuống dòng nào xuất hiện trong các ID bền vững, dữ liệu đã pickle tạo ra sẽ trở nên không thể đọc được.

.. _`JSON (JavaScript Object Notation)`: https://json.org
