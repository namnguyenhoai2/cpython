:mod:`!mmap` --- Hỗ trợ tệp ánh xạ bộ nhớ
=========================================

.. module:: mmap
   :synopsis: Giao diện cho các tệp ánh xạ bộ nhớ trên Unix và Windows.

--------------

.. include:: ../includes/wasm-notavail.rst

Các đối tượng tệp ánh xạ bộ nhớ hoạt động vừa như :class:`bytearray` vừa như
:term:`các đối tượng tệp <file object>`. Bạn có thể sử dụng các đối tượng mmap ở hầu hết những nơi cần :class:`bytearray`; ví dụ, bạn có thể sử dụng module :mod:`re` để tìm kiếm trong một tệp ánh xạ bộ nhớ. Bạn cũng có thể thay đổi một byte bằng cách thực hiện ``obj[index] = 97``, hoặc thay đổi một dãy con bằng cách gán cho một lát cắt: ``obj[i1:i2] = b'...'``. Bạn cũng có thể đọc và ghi dữ liệu bắt đầu từ vị trí hiện tại trong tệp, đồng thời :meth:`seek` qua tệp đến các vị trí khác nhau.

Tệp ánh xạ bộ nhớ được tạo bởi hàm dựng :class:`~mmap.mmap`, hàm này khác nhau trên Unix và Windows. Trong cả hai trường hợp, bạn phải cung cấp một bộ mô tả tệp cho một tệp được mở để cập nhật. Nếu muốn ánh xạ một đối tượng tệp Python hiện có, hãy sử dụng phương thức :meth:`~io.IOBase.fileno` của đối tượng đó để lấy giá trị chính xác cho tham số *fileno*. Nếu không, bạn có thể mở tệp bằng
hàm :func:`os.open`, hàm này trả về trực tiếp một bộ mô tả tệp (tệp vẫn cần được đóng lại khi hoàn tất).

.. note::
   Nếu muốn tạo ánh xạ bộ nhớ cho một tệp có thể ghi và được đệm, trước tiên bạn nên :func:`~io.IOBase.flush` tệp. Điều này cần thiết để bảo đảm các thay đổi cục bộ đối với các bộ đệm thực sự khả dụng cho ánh xạ.

Đối với cả hai phiên bản Unix và Windows của constructor, *access* có thể được chỉ định dưới dạng tham số từ khóa tùy chọn. *access* chấp nhận một trong bốn giá trị: :const:`ACCESS_READ`, :const:`ACCESS_WRITE` hoặc :const:`ACCESS_COPY` để lần lượt chỉ định bộ nhớ chỉ đọc, write-through hoặc copy-on-write, hoặc
:const:`ACCESS_DEFAULT` để sử dụng *prot*.  *access* có thể được sử dụng trên cả Unix và Windows.  Nếu không chỉ định *access*, mmap trên Windows sẽ trả về một ánh xạ write-through.  Các giá trị bộ nhớ ban đầu cho cả ba loại access đều được lấy từ tệp được chỉ định.  Phép gán cho một ánh xạ bộ nhớ :const:`ACCESS_READ` sẽ gây ra ngoại lệ :exc:`TypeError`.  Phép gán cho một
:const:`ACCESS_WRITE` ánh xạ bộ nhớ sẽ ảnh hưởng đến cả bộ nhớ và tệp bên dưới. Phép gán cho một ánh xạ bộ nhớ :const:`ACCESS_COPY` sẽ ảnh hưởng đến bộ nhớ nhưng không cập nhật tệp bên dưới.

.. versionchanged:: 3.7
   Đã thêm hằng số :const:`ACCESS_DEFAULT`.

Để ánh xạ bộ nhớ ẩn danh, cần truyền -1 làm fileno cùng với độ dài.

.. class:: mmap(fileno, length, tagname=None, access=ACCESS_DEFAULT, offset=0)

   **(Windows version)** Ánh xạ *length* byte từ tệp được chỉ định bởi file handle *fileno* và tạo một đối tượng mmap. Nếu *length* lớn hơn kích thước hiện tại của tệp, tệp sẽ được mở rộng để chứa *length* byte. Nếu *length* là ``0``, độ dài tối đa của ánh xạ là kích thước hiện tại của tệp, ngoại trừ trường hợp tệp trống thì Windows sẽ phát sinh ngoại lệ (bạn không thể tạo ánh xạ trống trên Windows).

   *tagname*, nếu được chỉ định và không phải là ``None``, là một chuỗi cung cấp tên thẻ cho ánh xạ. Windows cho phép bạn có nhiều ánh xạ khác nhau trên cùng một tệp. Nếu chỉ định tên của một thẻ hiện có, thẻ đó sẽ được mở; nếu không, một thẻ mới với tên này sẽ được tạo. Nếu bỏ qua tham số này hoặc tham số là ``None``, ánh xạ sẽ được tạo mà không có tên. Tránh sử dụng tham số *tagname* sẽ giúp mã của bạn có tính di động giữa Unix và Windows.

   *offset* có thể được chỉ định dưới dạng một offset số nguyên không âm. Các tham chiếu mmap sẽ tương đối với offset tính từ đầu tệp. *offset* mặc định là 0.  *offset* phải là bội số của :const:`ALLOCATIONGRANULARITY`.

   .. audit-event:: mmap.__new__ fileno,length,access,offset mmap.mmap

.. class:: mmap(fileno, length, flags=MAP_SHARED, prot=PROT_WRITE|PROT_READ, \
                access=ACCESS_DEFAULT, offset=0, *, trackfd=True)
   :noindex:

   **(Unix version)** ánh xạ *length* byte từ tệp được chỉ định bởi file descriptor *fileno*, rồi trả về một đối tượng mmap.  Nếu *length* là ``0``, độ dài tối đa của ánh xạ sẽ là kích thước hiện tại của tệp khi
   :class:`~mmap.mmap` được gọi.

   *flags* chỉ định bản chất của ánh xạ. :const:`MAP_PRIVATE` tạo một ánh xạ copy-on-write riêng tư, vì vậy các thay đổi đối với nội dung của đối tượng mmap sẽ chỉ dành riêng cho process này, còn :const:`MAP_SHARED` tạo một ánh xạ được chia sẻ với tất cả các process khác ánh xạ cùng những vùng của tệp.  Giá trị mặc định là :const:`MAP_SHARED`. Một số hệ thống có thêm các flag khả dụng; danh sách đầy đủ được chỉ định trong
   :ref:`MAP_* constants <map-constants>`.

   *prot*, nếu được chỉ định, cho biết cơ chế bảo vệ bộ nhớ mong muốn; hai giá trị hữu ích nhất là :const:`PROT_READ` và :const:`PROT_WRITE`, dùng để chỉ định rằng các trang có thể được đọc hoặc ghi.  *prot* mặc định là
   :const:`PROT_READ \| PROT_WRITE`.

   *access* có thể được chỉ định thay cho *flags* và *prot* dưới dạng tham số từ khóa tùy chọn. Việc chỉ định đồng thời *flags*, *prot* và *access* sẽ gây ra lỗi. Xem phần mô tả về *access* ở trên để biết cách sử dụng tham số này.

   *offset* có thể được chỉ định dưới dạng một độ lệch số nguyên không âm. Các tham chiếu mmap sẽ tương đối so với độ lệch tính từ đầu tệp. *offset* mặc định là 0. *offset* phải là bội số của :const:`ALLOCATIONGRANULARITY`, có giá trị bằng :const:`PAGESIZE` trên các hệ thống Unix.

   Nếu *trackfd* là ``False``, bộ mô tả tệp được chỉ định bởi *fileno* sẽ không được nhân bản và đối tượng :class:`!mmap` kết quả sẽ không được liên kết với tệp bên dưới của map. Điều này có nghĩa là các phương thức :meth:`~mmap.mmap.size` và :meth:`~mmap.mmap.resize` sẽ không hoạt động. Chế độ này hữu ích để giới hạn số lượng bộ mô tả tệp đang mở.

   Để đảm bảo tính hợp lệ của memory mapping được tạo, tệp được chỉ định bởi bộ mô tả *fileno* sẽ tự động được đồng bộ nội bộ với vùng lưu trữ vật lý trên macOS.

   .. versionchanged:: 3.13
      Tham số *trackfd* đã được thêm vào.

   Ví dụ này minh họa một cách đơn giản để sử dụng :class:`~mmap.mmap`::

      import mmap

      # viết một tệp ví dụ đơn giản
      with open("hello.txt", "wb") as f:
          f.write(b"Hello Python!\n")

      with open("hello.txt", "r+b") as f:
          # ánh xạ bộ nhớ cho tệp, kích thước 0 nghĩa là toàn bộ tệp
          mm = mmap.mmap(f.fileno(), 0)
          # đọc nội dung bằng các phương thức tệp tiêu chuẩn
          print(mm.readline())  # in ra b"Hello Python!\n"
          # đọc nội dung bằng cú pháp lát cắt
          print(mm[:5])  # in ra b"Hello"
          # cập nhật nội dung bằng cú pháp lát cắt;
          # lưu ý rằng nội dung mới phải có cùng kích thước
          mm[6:] = b" world!\n"
          # ... và đọc lại bằng các phương thức tệp tiêu chuẩn
          mm.seek(0)
          print(mm.readline())  # in ra b"Hello  world!\n"
          # đóng map
          mm.close()


   :class:`~mmap.mmap` cũng có thể được sử dụng như một context manager trong câu lệnh :keyword:`with`::

      import mmap

      with mmap.mmap(-1, 13) as mm:
          mm.write(b"Hello world!")

   .. versionadded:: 3.2
      Hỗ trợ context manager.


   Ví dụ tiếp theo minh họa cách tạo một map ẩn danh và trao đổi dữ liệu giữa tiến trình cha và tiến trình con::

      import mmap
      import os

      mm = mmap.mmap(-1, 13)
      mm.write(b"Hello world!")

      pid = os.fork()

      if pid == 0:  # Trong một tiến trình con
          mm.seek(0)
          print(mm.readline())

          mm.close()

   .. audit-event:: mmap.__new__ fileno,length,access,offset mmap.mmap

   Các đối tượng tệp được ánh xạ vào bộ nhớ hỗ trợ các phương thức sau:

   .. method:: close()

      Đóng mmap. Các lần gọi tiếp theo đến những phương thức khác của đối tượng sẽ khiến một ngoại lệ ValueError được phát sinh. Thao tác này không đóng tệp đang mở.


   .. attribute:: closed

      ``True`` nếu tệp đã đóng.

      .. versionadded:: 3.2


   .. method:: find(sub[, start[, end]])

      Trả về chỉ mục nhỏ nhất trong đối tượng tại đó tìm thấy dãy con *sub*, sao cho *sub* nằm trong phạm vi [*start*, *end*]. Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt. Trả về ``-1`` nếu không tìm thấy.

      .. versionchanged:: 3.5
         Các đối tượng có thể ghi :term:`bytes-like object` hiện được chấp nhận.


   .. method:: flush()
               flush(offset, size, /)

      Ghi các thay đổi được thực hiện trên bản sao trong bộ nhớ của tệp trở lại đĩa. Nếu không sử dụng lệnh gọi này, không có gì đảm bảo rằng các thay đổi sẽ được ghi trở lại trước khi đối tượng bị hủy. Nếu chỉ định *offset* và *size*, chỉ các thay đổi trong phạm vi byte đã cho mới được ghi vào đĩa; nếu không, toàn bộ phạm vi của ánh xạ sẽ được ghi. *offset* phải là bội số của
      :const:`PAGESIZE` hoặc :const:`ALLOCATIONGRANULARITY`.

      ``None`` được trả về để cho biết thao tác thành công. Một ngoại lệ được phát sinh khi lệnh gọi thất bại.

      .. versionchanged:: 3.8
         Trước đây, một giá trị khác không được trả về khi thao tác thành công; giá trị không được trả về khi có lỗi trên Windows. Trên Unix, giá trị không được trả về khi thao tác thành công; một ngoại lệ được phát sinh khi có lỗi.


   .. method:: madvise(option[, start[, length]])

      Gửi advice *option* đến kernel về vùng bộ nhớ bắt đầu tại *start* và có độ dài *length* byte. *option* phải là một trong các
      :ref:`MADV_* hằng số <madvise-constants>` có sẵn trên hệ thống. Nếu *start* và *length* bị bỏ qua, toàn bộ mapping sẽ được bao phủ. Trên một số hệ thống (bao gồm Linux), *start* phải là bội số của
      :const:`PAGESIZE`.

      Khả dụng: Các hệ thống có lời gọi hệ thống ``madvise()``.

      .. versionadded:: 3.8


   .. method:: move(dest, src, count)

      Sao chép *count* byte bắt đầu từ offset *src* đến chỉ mục đích *dest*. Nếu mmap được tạo với :const:`ACCESS_READ`, các lệnh gọi đến move sẽ phát sinh ngoại lệ :exc:`TypeError`.


   .. method:: read([n])

      Trả về một :class:`bytes` chứa tối đa *n* byte, bắt đầu từ vị trí hiện tại trong tệp. Nếu đối số bị bỏ qua, là ``None`` hoặc số âm, trả về tất cả byte từ vị trí hiện tại trong tệp đến cuối vùng ánh xạ. Vị trí trong tệp được cập nhật để trỏ đến sau các byte đã được trả về.

      .. versionchanged:: 3.3
         Đối số có thể được bỏ qua hoặc là ``None``.

   .. method:: read_byte()

      Trả về một byte tại vị trí hiện tại trong tệp dưới dạng số nguyên và tiến vị trí trong tệp lên 1.


   .. method:: readline()

      Trả về một dòng đơn, bắt đầu từ vị trí hiện tại trong tệp và kéo dài đến ký tự xuống dòng tiếp theo. Vị trí trong tệp được cập nhật để trỏ đến sau các byte đã được trả về.


   .. method:: resize(newsize)

      Thay đổi kích thước vùng ánh xạ và tệp bên dưới, nếu có.

      Việc thay đổi kích thước một vùng ánh xạ được tạo với *access* là :const:`ACCESS_READ` hoặc
      :const:`ACCESS_COPY`, sẽ gây ra ngoại lệ :exc:`TypeError`. Việc thay đổi kích thước một vùng ánh xạ được tạo với *trackfd* được đặt thành ``False``, sẽ gây ra ngoại lệ :exc:`ValueError`.

      **Trên Windows**: Việc thay đổi kích thước bản đồ sẽ phát sinh một :exc:`OSError` nếu có các bản đồ khác đang trỏ đến cùng một tệp được đặt tên. Việc thay đổi kích thước một bản đồ ẩn danh (tức là trỏ đến pagefile) sẽ âm thầm tạo một bản đồ mới, trong đó dữ liệu ban đầu được sao chép đến độ dài của kích thước mới.

      .. versionchanged:: 3.11
         Không thành công đúng cách nếu cố gắng thay đổi kích thước khi đang có một bản đồ khác được giữ Cho phép thay đổi kích thước đối với bản đồ ẩn danh trên Windows

   .. method:: rfind(sub[, start[, end]])

      Trả về chỉ số lớn nhất trong đối tượng tại đó dãy con *sub* được tìm thấy, sao cho *sub* nằm trong phạm vi [*start*, *end*]. Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt. Trả về ``-1`` nếu không tìm thấy.

      .. versionchanged:: 3.5
         Các đối tượng có thể ghi :term:`bytes-like object` hiện được chấp nhận.


   .. method:: seek(pos[, whence])

      Đặt vị trí hiện tại của tệp. Đối số *whence* là tùy chọn và mặc định là ``os.SEEK_SET`` hoặc ``0`` (định vị tệp tuyệt đối); các giá trị khác là ``os.SEEK_CUR`` hoặc ``1`` (tìm kiếm tương đối so với vị trí hiện tại) và ``os.SEEK_END`` hoặc ``2`` (tìm kiếm tương đối so với cuối tệp).

      .. versionchanged:: 3.13
         Trả về vị trí tuyệt đối mới thay vì ``None``.

   .. method:: seekable()

      Trả về việc tệp có hỗ trợ tìm kiếm hay không; giá trị trả về luôn là ``True``.

      .. versionadded:: 3.13

   .. method:: size()

      Trả về độ dài của tệp, có thể lớn hơn kích thước của vùng được ánh xạ vào bộ nhớ.


   .. method:: tell()

      Trả về vị trí hiện tại của con trỏ tệp.


   .. method:: write(bytes)

      Ghi các byte trong *bytes* vào bộ nhớ tại vị trí hiện tại của con trỏ tệp và trả về số byte đã ghi (không bao giờ nhỏ hơn ``len(bytes)``, vì nếu thao tác ghi thất bại, một :exc:`ValueError` sẽ được phát sinh). Vị trí tệp được cập nhật để trỏ đến sau các byte đã ghi. Nếu mmap được tạo với :const:`ACCESS_READ`, thao tác ghi vào đó sẽ phát sinh ngoại lệ :exc:`TypeError`.

      .. versionchanged:: 3.5
         Các đối tượng có thể ghi :term:`bytes-like object` hiện được chấp nhận.

      .. versionchanged:: 3.6
         Số byte đã ghi hiện được trả về.


   .. method:: write_byte(byte)

      Ghi số nguyên *byte* vào bộ nhớ tại vị trí hiện tại của con trỏ tệp; vị trí tệp được tiến lên ``1``. Nếu mmap được tạo với :const:`ACCESS_READ`, thao tác ghi vào đó sẽ phát sinh ngoại lệ :exc:`TypeError`.

.. _madvise-constants:

MADV_* Hằng số
++++++++++++++

.. data:: MADV_NORMAL
          MADV_RANDOM MADV_SEQUENTIAL MADV_WILLNEED MADV_DONTNEED MADV_REMOVE MADV_DONTFORK MADV_DOFORK MADV_HWPOISON MADV_MERGEABLE MADV_UNMERGEABLE MADV_SOFT_OFFLINE MADV_HUGEPAGE MADV_NOHUGEPAGE MADV_DONTDUMP MADV_DODUMP MADV_FREE MADV_NOSYNC MADV_AUTOSYNC MADV_NOCORE MADV_CORE MADV_PROTECT MADV_FREE_REUSABLE MADV_FREE_REUSE

   Các tùy chọn này có thể được truyền vào :meth:`mmap.madvise`. Không phải tùy chọn nào cũng có trên mọi hệ thống.

   Tính khả dụng: Các hệ thống có lời gọi hệ thống madvise().

   .. versionadded:: 3.8

.. _map-constants:

MAP_* Hằng số
+++++++++++++

.. data:: MAP_SHARED
          MAP_PRIVATE MAP_32BIT MAP_ALIGNED_SUPER MAP_ANON MAP_ANONYMOUS MAP_CONCEAL MAP_DENYWRITE MAP_EXECUTABLE MAP_HASSEMAPHORE MAP_JIT MAP_NOCACHE MAP_NOEXTEND MAP_NORESERVE MAP_POPULATE MAP_RESILIENT_CODESIGN MAP_RESILIENT_MEDIA MAP_STACK MAP_TPRO MAP_TRANSLATED_ALLOW_EXECUTE MAP_UNIX03

    Đây là các cờ khác nhau có thể được truyền vào :meth:`mmap.mmap`. :data:`MAP_ALIGNED_SUPER` chỉ có trên FreeBSD và :data:`MAP_CONCEAL` chỉ có trên OpenBSD. Lưu ý rằng một số tùy chọn có thể không có trên một số hệ thống.

    .. versionchanged:: 3.10
       Đã thêm hằng số :data:`MAP_POPULATE`.

    .. versionadded:: 3.11
       Đã thêm hằng số :data:`MAP_STACK`.

    .. versionadded:: 3.12
       Đã thêm các hằng số :data:`MAP_ALIGNED_SUPER` và :data:`MAP_CONCEAL`.

    .. versionadded:: 3.13
       Đã thêm các hằng số :data:`MAP_32BIT`, :data:`MAP_HASSEMAPHORE`, :data:`MAP_JIT`,
       :data:`MAP_NOCACHE`, :data:`MAP_NOEXTEND`, :data:`MAP_NORESERVE`,
       :data:`MAP_RESILIENT_CODESIGN`, :data:`MAP_RESILIENT_MEDIA`,
       :data:`MAP_TPRO`, :data:`MAP_TRANSLATED_ALLOW_EXECUTE`, và
       các hằng số :data:`MAP_UNIX03`.

