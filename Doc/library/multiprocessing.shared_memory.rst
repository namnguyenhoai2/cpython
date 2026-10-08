:mod:`!multiprocessing.shared_memory` --- Bộ nhớ dùng chung để truy cập trực tiếp giữa các tiến trình
=====================================================================================================

.. module:: multiprocessing.shared_memory
   :synopsis: Cung cấp bộ nhớ dùng chung để truy cập trực tiếp giữa các tiến trình.

**Mã nguồn:** :source:`Lib/multiprocessing/shared_memory.py`

.. versionadded:: 3.8

.. index::
   single: Shared Memory
   single: POSIX Shared Memory
   single: Named Shared Memory

--------------

Mô-đun này cung cấp một lớp, :class:`SharedMemory`, để cấp phát và quản lý bộ nhớ dùng chung được một hoặc nhiều tiến trình trên máy đa lõi hoặc máy đa xử lý đối xứng (SMP) truy cập.  Để hỗ trợ quản lý vòng đời của bộ nhớ dùng chung, đặc biệt là giữa các tiến trình riêng biệt, một lớp con :class:`~multiprocessing.managers.BaseManager`,
:class:`~multiprocessing.managers.SharedMemoryManager`, cũng được cung cấp trong
:mod:`multiprocessing.managers` mô-đun.

Trong mô-đun này, bộ nhớ dùng chung đề cập đến các khối bộ nhớ dùng chung kiểu "POSIX" (mặc dù không nhất thiết được triển khai rõ ràng theo cách đó) và không đề cập đến "bộ nhớ dùng chung phân tán".  Kiểu bộ nhớ dùng chung này cho phép các tiến trình riêng biệt có khả năng đọc và ghi vào một vùng bộ nhớ biến động chung (hoặc dùng chung).  Theo quy ước, các tiến trình chỉ được phép truy cập không gian bộ nhớ của chính tiến trình đó, nhưng bộ nhớ dùng chung cho phép chia sẻ dữ liệu giữa các tiến trình, nhờ đó tránh phải gửi dữ liệu đó dưới dạng thông báo giữa các tiến trình.  Chia sẻ dữ liệu trực tiếp qua bộ nhớ có thể mang lại lợi ích đáng kể về hiệu năng so với chia sẻ dữ liệu qua đĩa, socket hoặc các phương thức giao tiếp khác yêu cầu tuần tự hóa/giải tuần tự hóa và sao chép dữ liệu.


.. class:: SharedMemory(name=None, create=False, size=0, *, track=True)

   Tạo một thực thể của lớp :class:`!SharedMemory` để tạo một shared memory block mới hoặc gắn vào một shared memory block hiện có. Mỗi shared memory block được gán một tên duy nhất. Nhờ đó, một process có thể tạo shared memory block với một tên cụ thể và một process khác có thể gắn vào chính shared memory block đó bằng tên tương tự.

   Là một tài nguyên dùng để chia sẻ dữ liệu giữa các process, các shared memory block có thể tồn tại lâu hơn process ban đầu đã tạo ra chúng. Khi một process không còn cần truy cập vào một shared memory block mà các process khác vẫn có thể cần, phương thức :meth:`close` nên được gọi. Khi không còn process nào cần một shared memory block, phương thức
   :meth:`unlink` nên được gọi để đảm bảo việc dọn dẹp đúng cách.

   :param name:Tên duy nhất của shared memory được yêu cầu, được chỉ định dưới dạng chuỗi. Khi tạo một shared memory block mới, nếu ``None`` (giá trị mặc định) được cung cấp cho tên, một tên mới sẽ được tạo.
   :type name: str | None

   :param bool create:Kiểm soát việc tạo một shared memory block mới (``True``) hay gắn vào một shared memory block hiện có (``False``).

   :param int size:Số byte được yêu cầu khi tạo một shared memory block mới. Vì một số nền tảng chọn cấp phát các phần bộ nhớ dựa trên kích thước trang bộ nhớ của nền tảng đó, kích thước chính xác của shared memory block có thể lớn hơn hoặc bằng kích thước được yêu cầu. Khi gắn vào một shared memory block hiện có, tham số *size* sẽ bị bỏ qua.

   :param bool track:Khi ``True``, hãy đăng ký khối bộ nhớ dùng chung với một tiến trình resource tracker trên các nền tảng mà hệ điều hành không tự động thực hiện việc này. Resource tracker đảm bảo dọn dẹp đúng cách bộ nhớ dùng chung ngay cả khi tất cả các tiến trình khác có quyền truy cập vào bộ nhớ đều thoát mà không thực hiện việc đó. Các tiến trình Python được tạo từ cùng một tiến trình tổ tiên bằng các cơ chế :mod:`multiprocessing` sẽ dùng chung một tiến trình resource tracker duy nhất, và vòng đời của các phân đoạn bộ nhớ dùng chung được tự động xử lý giữa các tiến trình này. Các tiến trình Python được tạo theo bất kỳ cách nào khác sẽ có resource tracker riêng khi truy cập bộ nhớ dùng chung với *track* được bật. Điều này khiến resource tracker của tiến trình đầu tiên kết thúc xóa bộ nhớ dùng chung. Để tránh vấn đề này, người dùng :mod:`subprocess` hoặc các tiến trình Python độc lập nên đặt *track* thành ``False`` khi đã có một tiến trình khác thực hiện việc ghi sổ. *track* bị bỏ qua trên Windows, hệ điều hành có cơ chế theo dõi riêng và tự động xóa bộ nhớ dùng chung khi tất cả các handle đến bộ nhớ đó đã được đóng.

   .. versionchanged:: 3.13
      Đã thêm tham số *track*.

   .. method:: close()

      Đóng file descriptor/handle tới bộ nhớ dùng chung từ instance này. :meth:`close` nên được gọi sau khi không còn cần truy cập khối bộ nhớ dùng chung từ instance này. Tùy thuộc vào hệ điều hành, bộ nhớ bên dưới có thể được giải phóng hoặc không, ngay cả khi tất cả các handle tới bộ nhớ đó đã được đóng. Để đảm bảo dọn dẹp đúng cách, hãy sử dụng phương thức :meth:`unlink`.

   .. method:: unlink()

      Xóa khối bộ nhớ dùng chung bên dưới. Chỉ nên gọi hàm này một lần cho mỗi khối bộ nhớ dùng chung, bất kể số lượng handle tới khối đó, kể cả trong các tiến trình khác.
      :meth:`unlink` và :meth:`close` có thể được gọi theo bất kỳ thứ tự nào, nhưng việc cố truy cập dữ liệu bên trong khối bộ nhớ dùng chung sau :meth:`unlink` có thể gây ra lỗi truy cập bộ nhớ, tùy thuộc vào nền tảng.

      Phương thức này không có tác dụng trên Windows; tại đó, cách duy nhất để xóa một khối bộ nhớ dùng chung là đóng tất cả các handle.

   .. attribute:: buf

      Một memoryview của nội dung khối bộ nhớ dùng chung.

   .. attribute:: name

      Quyền truy cập chỉ đọc vào tên duy nhất của khối bộ nhớ dùng chung.

   .. attribute:: size

      Quyền truy cập chỉ đọc vào kích thước tính bằng byte của khối bộ nhớ dùng chung.


Ví dụ sau đây minh họa cách sử dụng cấp thấp các thực thể :class:`SharedMemory`::

   >>> from multiprocessing import shared_memory
   >>> shm_a = shared_memory.SharedMemory(create=True, size=10)
   >>> type(shm_a.buf)
   <class 'memoryview'>
   >>> buffer = shm_a.buf
   >>> len(buffer)
   10
   >>> buffer[:4] = bytearray([22, 33, 44, 55])  # Sửa đổi nhiều byte cùng lúc
   >>> buffer[4] = 100                           # Sửa đổi từng byte một
   >>> # Gắn vào một khối bộ nhớ dùng chung hiện có
   >>> shm_b = shared_memory.SharedMemory(shm_a.name)
   >>> import array
   >>> array.array('b', shm_b.buf[:5])  # Sao chép dữ liệu vào một array.array mới
   array('b', [22, 33, 44, 55, 100])
   >>> shm_b.buf[:5] = b'howdy'  # Sửa đổi qua shm_b bằng bytes
   >>> bytes(shm_a.buf[:5])      # Truy cập qua shm_a
   b'howdy'
   >>> shm_b.close()   # Đóng từng thực thể SharedMemory
   >>> shm_a.close()
   >>> shm_a.unlink()  # Chỉ gọi unlink một lần để giải phóng bộ nhớ dùng chung



Ví dụ sau minh họa cách sử dụng thực tế lớp :class:`SharedMemory` với các mảng `NumPy <https://numpy.org/>`_, truy cập cùng một :class:`!numpy.ndarray` từ hai Python shell riêng biệt:

.. doctest::
   :options: +SKIP

   >>> # Trong Python interactive shell đầu tiên
   >>> import numpy as np
   >>> a = np.array([1, 1, 2, 3, 5, 8])  # Bắt đầu với một mảng NumPy hiện có
   >>> from multiprocessing import shared_memory
   >>> shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
   >>> # Bây giờ tạo một mảng NumPy được hỗ trợ bởi bộ nhớ dùng chung
   >>> b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
   >>> b[:] = a[:]  # Sao chép dữ liệu ban đầu vào bộ nhớ dùng chung
   >>> b
   array([1, 1, 2, 3, 5, 8])
   >>> type(b)
   <class 'numpy.ndarray'>
   >>> type(a)
   <class 'numpy.ndarray'>
   >>> shm.name  # Chúng ta không chỉ định tên nên một tên đã được tự động chọn
   'psm_21467_46075'

   >>> # Trong cùng shell hoặc một Python shell mới trên cùng máy
   >>> import numpy as np
   >>> from multiprocessing import shared_memory
   >>> # Gắn vào block bộ nhớ dùng chung hiện có
   >>> existing_shm = shared_memory.SharedMemory(name='psm_21467_46075')
   >>> # Lưu ý rằng trong ví dụ này, a.shape là (6,) và a.dtype là np.int64
   >>> c = np.ndarray((6,), dtype=np.int64, buffer=existing_shm.buf)
   >>> c
   array([1, 1, 2, 3, 5, 8])
   >>> c[-1] = 888
   >>> c
   array([  1,   1,   2,   3,   5, 888])

   >>> # Quay lại Python interactive shell đầu tiên, b phản ánh thay đổi này
   >>> b
   array([  1,   1,   2,   3,   5, 888])

   >>> # Dọn dẹp từ bên trong Python shell thứ hai
   >>> del c  # Không cần thiết; chỉ để nhấn mạnh rằng mảng không còn được sử dụng
   >>> existing_shm.close()

   >>> # Dọn dẹp từ bên trong Python shell đầu tiên
   >>> del b  # Không cần thiết; chỉ để nhấn mạnh rằng mảng không còn được sử dụng
   >>> shm.close()
   >>> shm.unlink()  # Giải phóng và release shared memory block ở bước cuối cùng


.. class:: SharedMemoryManager([address[, authkey]])
   :module: multiprocessing.managers

   Một lớp con của :class:`multiprocessing.managers.BaseManager` có thể được sử dụng để quản lý các shared memory block giữa các process.

   Một lệnh gọi đến :meth:`~multiprocessing.managers.BaseManager.start` trên một
   Một instance :class:`!SharedMemoryManager` khiến một process mới được khởi động. Process mới này chỉ có mục đích quản lý vòng đời của tất cả các khối bộ nhớ dùng chung được tạo thông qua nó. Để kích hoạt việc giải phóng tất cả các khối bộ nhớ dùng chung do process đó quản lý, hãy gọi
   :meth:`~multiprocessing.managers.BaseManager.shutdown` trên instance. Thao tác này kích hoạt một lệnh gọi :meth:`~multiprocessing.shared_memory.SharedMemory.unlink` trên tất cả các đối tượng :class:`SharedMemory` do process đó quản lý, sau đó dừng chính process đó. Bằng cách tạo các instance :class:`!SharedMemory` thông qua một :class:`!SharedMemoryManager`, chúng ta tránh phải theo dõi và kích hoạt thủ công việc giải phóng các tài nguyên bộ nhớ dùng chung.

   Lớp này cung cấp các phương thức để tạo và trả về các instance :class:`SharedMemory`, cũng như để tạo một đối tượng dạng danh sách (:class:`ShareableList`) được hỗ trợ bởi bộ nhớ dùng chung.

   Tham khảo :class:`~multiprocessing.managers.BaseManager` để biết mô tả về các đối số đầu vào tùy chọn *address* và *authkey* được kế thừa, cũng như cách sử dụng chúng để kết nối từ các process khác đến một dịch vụ :class:`!SharedMemoryManager` hiện có.

   .. method:: SharedMemory(size)

      Tạo và trả về một đối tượng :class:`SharedMemory` mới với *size* được chỉ định, tính bằng byte.

   .. method:: ShareableList(sequence)

      Tạo và trả về một đối tượng :class:`ShareableList` mới, được khởi tạo bằng các giá trị từ *sequence* đầu vào.


Ví dụ sau đây minh họa các cơ chế cơ bản của một
:class:`~multiprocessing.managers.SharedMemoryManager`:

.. doctest::
   :options: +SKIP

   >>> from multiprocessing.managers import SharedMemoryManager
   >>> smm = SharedMemoryManager()
   >>> smm.start()  # Khởi động tiến trình quản lý các khối bộ nhớ dùng chung
   >>> sl = smm.ShareableList(range(4))
   >>> sl
   ShareableList([0, 1, 2, 3], name='psm_6572_7512')
   >>> raw_shm = smm.SharedMemory(size=128)
   >>> another_sl = smm.ShareableList('alpha')
   >>> another_sl
   ShareableList(['a', 'l', 'p', 'h', 'a'], name='psm_6572_12221')
   >>> smm.shutdown()  # Gọi unlink() trên sl, raw_shm và another_sl

Ví dụ sau đây minh họa một mẫu có thể thuận tiện hơn khi sử dụng
:class:`~multiprocessing.managers.SharedMemoryManager` các đối tượng thông qua
câu lệnh :keyword:`with` để đảm bảo rằng tất cả các khối bộ nhớ dùng chung được giải phóng sau khi không còn cần thiết:

.. doctest::
   :options: +SKIP

   >>> with SharedMemoryManager() as smm:
   ...     sl = smm.ShareableList(range(2000))
   ...     # Chia công việc cho hai tiến trình, lưu các kết quả một phần vào sl
   ...     p1 = Process(target=do_work, args=(sl, 0, 1000))
   ...     p2 = Process(target=do_work, args=(sl, 1000, 2000))
   ...     p1.start()
   ...     p2.start()  # Có thể multiprocessing.Pool sẽ hiệu quả hơn
   ...     p1.join()
   ...     p2.join()   # Chờ mọi tác vụ hoàn tất trong cả hai tiến trình
   ...     total_result = sum(sl)  # Hợp nhất các kết quả từng phần hiện có trong sl

Khi sử dụng một :class:`~multiprocessing.managers.SharedMemoryManager` trong câu lệnh :keyword:`with`, tất cả các khối bộ nhớ dùng chung được tạo bằng manager đó sẽ được giải phóng khi khối mã của câu lệnh :keyword:`!with` hoàn tất thực thi.


.. class:: ShareableList(sequence=None, *, name=None)

   Cung cấp một đối tượng dạng danh sách có thể thay đổi, trong đó tất cả các giá trị được lưu trữ trong một khối bộ nhớ dùng chung. Điều này giới hạn các giá trị có thể lưu trữ ở những kiểu dữ liệu tích hợp sẵn sau:

   * :class:`int` (số nguyên có dấu 64 bit)
   * :class:`float`
   * :class:`bool`
   * :class:`str` (mỗi giá trị nhỏ hơn 10M byte khi được mã hóa dưới dạng UTF-8)
   * :class:`bytes` (mỗi giá trị nhỏ hơn 10M byte)
   * ``None``

   Kiểu :class:`list` dựng sẵn cũng khác biệt đáng kể ở chỗ các danh sách này không thể thay đổi độ dài tổng thể (tức là không có :meth:`!append`, :meth:`!insert`, v.v.) và không hỗ trợ việc tạo động các thực thể :class:`!ShareableList` mới thông qua thao tác cắt lát.

   *sequence* được dùng để điền các giá trị vào một :class:`!ShareableList` mới. Đặt thành ``None`` để thay vào đó gắn vào một thực thể đã tồn tại
   :class:`!ShareableList` bằng tên bộ nhớ dùng chung duy nhất của nó.

   *name* là tên duy nhất của vùng bộ nhớ dùng chung được yêu cầu, như được mô tả trong định nghĩa của :class:`SharedMemory`. Khi gắn vào một :class:`!ShareableList` đã tồn tại, hãy chỉ định tên duy nhất của khối bộ nhớ dùng chung của nó, đồng thời giữ *sequence* ở giá trị ``None``.

   .. note::

      Có một vấn đề đã biết đối với các giá trị :class:`bytes` và :class:`str`. Nếu chúng kết thúc bằng ``\x00`` byte hoặc ký tự null, các byte hoặc ký tự đó có thể bị *silently stripped* khi lấy chúng theo chỉ mục từ
      :class:`!ShareableList`. Hành vi ``.rstrip(b'\x00')`` này được xem là một lỗi và có thể sẽ bị loại bỏ trong tương lai. Xem :gh:`106939`.

   Đối với các ứng dụng gặp vấn đề khi loại bỏ các giá trị null ở cuối, hãy khắc phục bằng cách luôn thêm một byte khác 0 vào cuối các giá trị đó khi lưu, và luôn loại bỏ byte này khi lấy ra:

   .. doctest::

       >>> from multiprocessing import shared_memory
       >>> nul_bug_demo = shared_memory.ShareableList(['?\x00', b'\x03\x02\x01\x00\x00\x00'])
       >>> nul_bug_demo[0]
       '?'
       >>> nul_bug_demo[1]
       b'\x03\x02\x01'
       >>> nul_bug_demo.shm.unlink()
       >>> padded = shared_memory.ShareableList(['?\x00\x07', b'\x03\x02\x01\x00\x00\x00\x07'])
       >>> padded[0][:-1]
       '?\x00'
       >>> padded[1][:-1]
       b'\x03\x02\x01\x00\x00\x00'
       >>> padded.shm.unlink()

   .. method:: count(value)

      Trả về số lần xuất hiện của *value*.

   .. method:: index(value)

      Trả về vị trí chỉ mục đầu tiên của *value*. Phát sinh :exc:`ValueError` nếu không có *value*.

   .. attribute:: format

      Thuộc tính chỉ đọc chứa định dạng đóng gói :mod:`struct` được sử dụng bởi tất cả các giá trị hiện đang được lưu trữ.

   .. attribute:: shm

      Đối tượng :class:`SharedMemory` nơi các giá trị được lưu trữ.


Ví dụ sau minh họa cách sử dụng cơ bản một đối tượng :class:`ShareableList`:

   >>> from multiprocessing import shared_memory
   >>> a = shared_memory.ShareableList(['howdy', b'HoWdY', -273.154, 100, None, True, 42])
   >>> [ type(entry) for entry in a ]
   [<class 'str'>, <class 'bytes'>, <class 'float'>, <class 'int'>, <class 'NoneType'>, <class 'bool'>, <class 'int'>]
   >>> a[2]
   -273.154
   >>> a[2] = -78.5
   >>> a[2]
   -78.5
   >>> a[2] = 'dry ice'  # Cũng hỗ trợ thay đổi kiểu dữ liệu
   >>> a[2]
   'dry ice'
   >>> a[2] = 'larger than previously allocated storage space'
   Traceback (most recent call last):
     ...
   ValueError: exceeds available storage for existing str
   >>> a[2]
   'dry ice'
   >>> len(a)
   7
   >>> a.index(42)
   6
   >>> a.count(b'howdy')
   0
   >>> a.count(b'HoWdY')
   1
   >>> a.shm.close()
   >>> a.shm.unlink()
   >>> del a  # Không hỗ trợ sử dụng ShareableList sau khi gọi unlink()

Ví dụ sau minh họa cách một, hai hoặc nhiều tiến trình có thể truy cập cùng một :class:`ShareableList` bằng cách cung cấp tên của khối bộ nhớ dùng chung nằm phía sau nó:

   >>> b = shared_memory.ShareableList(range(5))         # Trong tiến trình thứ nhất
   >>> c = shared_memory.ShareableList(name=b.shm.name)  # Trong tiến trình thứ hai
   >>> c
   ShareableList([0, 1, 2, 3, 4], name='...')
   >>> c[-1] = -999
   >>> b[-1]
   -999
   >>> b.shm.close()
   >>> c.shm.close()
   >>> c.shm.unlink()

Các ví dụ sau cho thấy rằng các đối tượng :class:`ShareableList` (và các đối tượng :class:`SharedMemory` bên dưới) có thể được pickle và unpickle khi cần. Lưu ý rằng đối tượng đó vẫn sẽ là cùng một đối tượng dùng chung. Điều này xảy ra vì đối tượng được giải tuần tự có cùng tên duy nhất và chỉ được gắn vào một đối tượng hiện có cùng tên (nếu đối tượng đó vẫn còn tồn tại):

   >>> import pickle
   >>> from multiprocessing import shared_memory
   >>> sl = shared_memory.ShareableList(range(10))
   >>> list(sl)
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

   >>> deserialized_sl = pickle.loads(pickle.dumps(sl))
   >>> list(deserialized_sl)
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

   >>> sl[0] = -1
   >>> deserialized_sl[1] = -2
   >>> list(sl)
   [-1, -2, 2, 3, 4, 5, 6, 7, 8, 9]
   >>> list(deserialized_sl)
   [-1, -2, 2, 3, 4, 5, 6, 7, 8, 9]

   >>> sl.shm.close()
   >>> sl.shm.unlink()

.. _`NumPy arrays`: https://numpy.org/
