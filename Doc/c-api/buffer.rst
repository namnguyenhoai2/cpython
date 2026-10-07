.. highlight:: c

.. index::
   single: buffer protocol
   single: buffer interface; (see buffer protocol)
   single: buffer object; (see buffer protocol)

.. _bufferobjects:

Giao thức Buffer
----------------

.. sectionauthor:: Greg Stein <gstein@lyra.org>
.. sectionauthor:: Benjamin Peterson
.. sectionauthor:: Stefan Krah


Một số đối tượng có sẵn trong Python bao bọc quyền truy cập vào một mảng bộ nhớ bên dưới hoặc *buffer*. Các đối tượng như vậy bao gồm :class:`bytes` dựng sẵn và
:class:`bytearray`, cùng một số kiểu mở rộng như :class:`array.array`. Các thư viện bên thứ ba có thể định nghĩa các kiểu riêng cho những mục đích đặc biệt, chẳng hạn như xử lý hình ảnh hoặc phân tích số.

Mặc dù mỗi kiểu trong số này có ngữ nghĩa riêng, chúng đều có chung đặc điểm là được hỗ trợ bởi một bộ đệm bộ nhớ có thể rất lớn. Do đó, trong một số trường hợp, việc truy cập trực tiếp vào bộ đệm đó mà không cần sao chép trung gian là điều mong muốn.

Python cung cấp một cơ chế như vậy ở cấp độ C và Python dưới dạng
:ref:`buffer protocol <bufferobjects>`. Giao thức này có hai phía:

.. index:: single: PyBufferProcs (C type)

- ở phía nhà sản xuất, một kiểu có thể export một "buffer interface", cho phép các đối tượng thuộc kiểu đó cung cấp thông tin về bộ đệm bên dưới của chúng. Giao diện này được mô tả trong phần :ref:`buffer-structs`; đối với Python, hãy xem :ref:`python-buffer-protocol`.

- Ở phía bên sử dụng, có một số cách để lấy con trỏ đến dữ liệu thô bên dưới của một đối tượng (chẳng hạn như một tham số phương thức). Để biết thông tin về Python, hãy xem :class:`memoryview`.

Các đối tượng đơn giản như :class:`bytes` và :class:`bytearray` cung cấp bộ đệm bên dưới của chúng dưới dạng hướng theo byte. Các dạng khác cũng có thể thực hiện được; chẳng hạn, các phần tử do một :class:`array.array` cung cấp có thể là các giá trị nhiều byte.

Một ví dụ về consumer của giao diện bộ đệm là phương thức :meth:`~io.BufferedIOBase.write` của các đối tượng tệp: bất kỳ đối tượng nào có thể xuất một chuỗi byte thông qua giao diện bộ đệm đều có thể được ghi vào tệp. Trong khi :meth:`!write` chỉ cần quyền truy cập chỉ đọc vào nội dung bên trong của đối tượng được truyền cho nó, các phương thức khác như :meth:`~io.BufferedIOBase.readinto` cần quyền ghi vào nội dung của đối số. Giao diện bộ đệm cho phép các đối tượng chủ động cho phép hoặc từ chối việc xuất bộ đệm đọc-ghi và chỉ đọc.

Có hai cách để consumer của giao diện bộ đệm lấy một bộ đệm trên đối tượng đích:

* gọi :c:func:`PyObject_GetBuffer` với các tham số phù hợp;

* gọi :c:func:`PyArg_ParseTuple` (hoặc một hàm cùng nhóm) với một trong các ``y*``, ``w*`` hoặc ``s*`` :ref:`mã định dạng <arg-parsing>`.

Trong cả hai trường hợp, phải gọi :c:func:`PyBuffer_Release` khi không còn cần bộ đệm nữa. Nếu không, có thể phát sinh nhiều vấn đề khác nhau, chẳng hạn như rò rỉ tài nguyên.

.. versionadded:: 3.12

   Giao thức buffer hiện có thể được truy cập trong Python, xem
   :ref:`python-buffer-protocol` và :class:`memoryview`.

.. _buffer-structure:

Cấu trúc buffer
===============

Các cấu trúc buffer (hay gọi đơn giản là "buffer") rất hữu ích để cung cấp dữ liệu nhị phân từ một đối tượng khác cho lập trình viên Python. Chúng cũng có thể được sử dụng như một cơ chế cắt không sao chép. Nhờ khả năng tham chiếu đến một vùng bộ nhớ, chúng ta có thể dễ dàng cung cấp bất kỳ dữ liệu nào cho lập trình viên Python. Vùng bộ nhớ đó có thể là một mảng hằng lớn trong một phần mở rộng C, một vùng bộ nhớ thô để thao tác trước khi truyền cho thư viện hệ điều hành, hoặc được dùng để truyền dữ liệu có cấu trúc dưới dạng gốc trong bộ nhớ của nó.

Không giống hầu hết các kiểu dữ liệu được trình thông dịch Python cung cấp, buffer không phải là các con trỏ :c:type:`PyObject` mà là những cấu trúc C đơn giản. Điều này cho phép tạo và sao chép chúng rất dễ dàng. Khi cần một wrapper tổng quát quanh một buffer, có thể tạo một đối tượng :ref:`memoryview <memoryview-objects>`.

Để biết hướng dẫn ngắn về cách viết một đối tượng xuất buffer, hãy xem
:ref:`Buffer Object Structures <buffer-structs>`. Để lấy một buffer, hãy xem :c:func:`PyObject_GetBuffer`.

.. c:type:: Py_buffer

   .. c:member:: void *buf

      Con trỏ đến vị trí bắt đầu của cấu trúc logic được mô tả bởi các trường của buffer. Đây có thể là bất kỳ vị trí nào trong khối memory vật lý bên dưới của exporter. Ví dụ, với :c:member:`~Py_buffer.strides` âm, giá trị này có thể trỏ đến cuối khối memory.

      Đối với các mảng :term:`contiguous`, giá trị này trỏ đến đầu khối memory.

   .. c:member:: PyObject *obj

      Một tham chiếu mới đến đối tượng exporter. Tham chiếu này thuộc quyền sở hữu của consumer và được tự động giải phóng (tức là giảm reference count) rồi đặt thành ``NULL`` bởi
      :c:func:`PyBuffer_Release`. Trường này tương đương với giá trị trả về của bất kỳ hàm C-API tiêu chuẩn nào.

      Trong trường hợp đặc biệt, đối với các buffer *tạm thời* được bọc bởi
      :c:func:`PyMemoryView_FromBuffer` hoặc :c:func:`PyBuffer_FillInfo`, trường này là ``NULL``. Nhìn chung, các đối tượng exporter KHÔNG ĐƯỢC sử dụng cơ chế này.

   .. c:member:: Py_ssize_t len

      ``product(shape) * itemsize``. Đối với các mảng contiguous, đây là độ dài của khối memory bên dưới. Đối với các mảng non-contiguous, đây là độ dài mà cấu trúc logic sẽ có nếu được sao chép sang dạng contiguous.

      Việc truy cập ``((char *)buf)[0] up to ((char *)buf)[len-1]`` chỉ hợp lệ nếu buffer được lấy từ một request bảo đảm tính liên tục. Trong hầu hết trường hợp, request đó sẽ là :c:macro:`PyBUF_SIMPLE` hoặc :c:macro:`PyBUF_WRITABLE`.

   .. c:member:: int readonly

      Một chỉ báo cho biết buffer có ở chế độ chỉ đọc hay không. Trường này được điều khiển bởi cờ :c:macro:`PyBUF_WRITABLE`.

   .. c:member:: Py_ssize_t itemsize

      Kích thước của một phần tử tính bằng byte. Tương đương với giá trị trả về khi gọi :func:`struct.calcsize` trên các giá trị ``NULL`` :c:member:`~Py_buffer.format` không phải ``NULL``.

      Ngoại lệ quan trọng: Nếu consumer yêu cầu một buffer mà không có cờ
      :c:macro:`PyBUF_FORMAT`, :c:member:`~Py_buffer.format` sẽ được đặt thành  ``NULL``,  nhưng :c:member:`~Py_buffer.itemsize` vẫn giữ giá trị của định dạng ban đầu.

      Nếu :c:member:`~Py_buffer.shape` hiện diện, đẳng thức ``product(shape) * itemsize == len`` vẫn đúng và consumer có thể sử dụng :c:member:`~Py_buffer.itemsize` để duyệt buffer.

      Nếu :c:member:`~Py_buffer.shape` là ``NULL`` do một request :c:macro:`PyBUF_SIMPLE` hoặc :c:macro:`PyBUF_WRITABLE`, consumer phải bỏ qua
      :c:member:`~Py_buffer.itemsize` và giả định ``itemsize == 1``.

   .. c:member:: char *format

      Một chuỗi kết thúc bằng *NULL* theo cú pháp kiểu module :mod:`struct`, mô tả nội dung của một mục đơn. Nếu đây là ``NULL``, ``"B"`` (các byte không dấu) được giả định.

      Trường này được điều khiển bởi cờ :c:macro:`PyBUF_FORMAT`.

   .. c:member:: int ndim

      Số chiều mà bộ nhớ biểu diễn dưới dạng một mảng n chiều. Nếu là ``0``, :c:member:`~Py_buffer.buf` trỏ đến một mục đơn biểu diễn một scalar. Trong trường hợp này, :c:member:`~Py_buffer.shape`, :c:member:`~Py_buffer.strides` và :c:member:`~Py_buffer.suboffsets` PHẢI là ``NULL``. Số chiều tối đa được xác định bởi :c:macro:`PyBUF_MAX_NDIM`.

   .. c:member:: Py_ssize_t *shape

      Một mảng :c:type:`Py_ssize_t` có độ dài :c:member:`~Py_buffer.ndim`, cho biết hình dạng của bộ nhớ dưới dạng một mảng n chiều. Lưu ý rằng ``shape[0] * ... * shape[ndim-1] * itemsize`` PHẢI bằng
      :c:member:`~Py_buffer.len`.

      Các giá trị hình dạng bị giới hạn ở ``shape[n] >= 0``. Trường hợp ``shape[n] == 0`` cần được chú ý đặc biệt. Xem `complex arrays <complex arrays_>`_ để biết thêm thông tin.

      Mảng hình dạng chỉ được đọc đối với consumer.

   .. c:member:: Py_ssize_t *strides

      Một mảng :c:type:`Py_ssize_t` có độ dài :c:member:`~Py_buffer.ndim`, cung cấp số byte cần bỏ qua để đi tới một phần tử mới trong mỗi chiều.

      Các giá trị stride có thể là bất kỳ số nguyên nào. Đối với các mảng thông thường, stride thường là số dương, nhưng bên sử dụng PHẢI có khả năng xử lý trường hợp ``strides[n] <= 0``. Xem `complex arrays <complex arrays_>`_ để biết thêm thông tin.

      Mảng stride chỉ được phép đọc đối với bên sử dụng.

   .. c:member:: Py_ssize_t *suboffsets

      Một mảng :c:type:`Py_ssize_t` có độ dài :c:member:`~Py_buffer.ndim`. Nếu ``suboffsets[n] >= 0``, các giá trị được lưu dọc theo chiều thứ n là các con trỏ và giá trị suboffset quy định số byte cần cộng vào mỗi con trỏ sau khi bỏ tham chiếu. Giá trị suboffset âm cho biết không được thực hiện bỏ tham chiếu (stride trong một khối bộ nhớ liền kề).

      Nếu tất cả suboffset đều âm (tức là không cần bỏ tham chiếu), thì trường này phải là ``NULL`` (giá trị mặc định).

      Kiểu biểu diễn mảng này được Python Imaging Library (PIL) sử dụng. Xem `complex arrays <complex arrays_>`_ để biết thêm thông tin về cách truy cập các phần tử của loại mảng này.

      Mảng suboffsets chỉ được phép đọc đối với bên sử dụng.

   .. c:member:: void *internal

      Trường này được đối tượng exporter sử dụng nội bộ. Ví dụ, exporter có thể chuyển trường này thành một số nguyên và dùng nó để lưu các cờ cho biết có cần giải phóng các mảng shape, strides và suboffsets khi buffer được giải phóng hay không. Consumer TUYỆT ĐỐI KHÔNG ĐƯỢC thay đổi giá trị này.


Hằng số:

.. c:macro:: PyBUF_MAX_NDIM

   Số chiều tối đa mà vùng nhớ biểu diễn. Exporter PHẢI tuân thủ giới hạn này; consumer của các buffer đa chiều NÊN có khả năng xử lý tối đa :c:macro:`!PyBUF_MAX_NDIM` chiều. Hiện được đặt là 64.


.. _buffer-request-types:

Các loại yêu cầu buffer
=======================

Buffer thường được lấy bằng cách gửi một yêu cầu buffer đến đối tượng exporter thông qua :c:func:`PyObject_GetBuffer`. Vì độ phức tạp của cấu trúc logic của vùng nhớ có thể thay đổi rất lớn, consumer sử dụng đối số *flags* để chỉ định chính xác loại buffer mà nó có thể xử lý.

Tất cả các trường :c:type:`Py_buffer` đều được xác định rõ ràng bởi loại yêu cầu.

các trường không phụ thuộc vào yêu cầu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Các trường sau đây không bị ảnh hưởng bởi *flags* và luôn phải được điền bằng các giá trị chính xác: :c:member:`~Py_buffer.obj`, :c:member:`~Py_buffer.buf`,
:c:member:`~Py_buffer.len`, :c:member:`~Py_buffer.itemsize`, :c:member:`~Py_buffer.ndim`.

readonly, format
~~~~~~~~~~~~~~~~

   .. c:macro:: PyBUF_WRITABLE

      Kiểm soát trường :c:member:`~Py_buffer.readonly`. Nếu được đặt, exporter PHẢI cung cấp một writable buffer; nếu không thì phải báo lỗi. Nếu không, exporter CÓ THỂ cung cấp writable buffer hoặc read-only buffer, nhưng lựa chọn này PHẢI nhất quán với tất cả consumer. Ví dụ, có thể dùng :c:expr:`PyBUF_SIMPLE | PyBUF_WRITABLE` để yêu cầu một writable buffer đơn giản.

   .. c:macro:: PyBUF_WRITEABLE

      Đây là bí danh của :c:macro:`PyBUF_WRITABLE`.

      .. soft-deprecated:: 3.13

   .. c:macro:: PyBUF_FORMAT

      Kiểm soát trường :c:member:`~Py_buffer.format`. Nếu được đặt, trường này PHẢI được điền chính xác. Nếu không, trường này PHẢI là ``NULL``.


:c:macro:`PyBUF_WRITABLE` có thể được \|'d với bất kỳ cờ nào trong phần tiếp theo. Vì :c:macro:`PyBUF_SIMPLE` được định nghĩa là 0, :c:macro:`PyBUF_WRITABLE` có thể được dùng như một cờ độc lập để yêu cầu một writable buffer đơn giản.

:c:macro:`PyBUF_FORMAT` phải được \|'d với bất kỳ cờ nào ngoại trừ :c:macro:`PyBUF_SIMPLE`, vì cờ sau đã ngầm định format ``B`` (các byte không dấu). Không thể dùng :c:macro:`!PyBUF_FORMAT` riêng lẻ.


shape, strides, suboffsets
~~~~~~~~~~~~~~~~~~~~~~~~~~

Các cờ kiểm soát cấu trúc logic của bộ nhớ được liệt kê theo thứ tự giảm dần về độ phức tạp. Lưu ý rằng mỗi cờ chứa tất cả các bit của những cờ bên dưới nó.

.. tabularcolumns:: |p{0.35\linewidth}|l|l|l|

+-----------------------------+-------+---------+------------+
| Yêu cầu                     | shape | strides | suboffsets |
+=============================+=======+=========+============+
| .. c:macro:: PyBUF_INDIRECT | có    | có      | nếu cần    |
+-----------------------------+-------+---------+------------+
| .. c:macro:: PyBUF_STRIDES  | có    | có      | NULL       |
+-----------------------------+-------+---------+------------+
| .. c:macro:: PyBUF_ND       | có    | NULL    | NULL       |
+-----------------------------+-------+---------+------------+
| .. c:macro:: PyBUF_SIMPLE   | NULL  | NULL    | NULL       |
+-----------------------------+-------+---------+------------+


.. index:: contiguous, C-contiguous, Fortran contiguous

yêu cầu về tính liên tục
~~~~~~~~~~~~~~~~~~~~~~~~

Có thể yêu cầu rõ ràng :term:`tính liên tục <contiguous>` theo C hoặc Fortran, có hoặc không có thông tin về stride. Nếu không có thông tin về stride, buffer phải liên tục theo C.

.. tabularcolumns:: |p{0.35\linewidth}|l|l|l|l|

+-----------------------------------+-------+---------+------------+----------+
| Request                           | shape | strides | suboffsets | contig   |
+===================================+=======+=========+============+==========+
| .. c:macro:: PyBUF_C_CONTIGUOUS   | có    | có      | NULL       | C        |
+-----------------------------------+-------+---------+------------+----------+
| .. c:macro:: PyBUF_F_CONTIGUOUS   | có    | có      | NULL       | F        |
+-----------------------------------+-------+---------+------------+----------+
| .. c:macro:: PyBUF_ANY_CONTIGUOUS | có    | có      | NULL       | C hoặc F |
+-----------------------------------+-------+---------+------------+----------+
| :c:macro:`PyBUF_ND`               | có    | NULL    | NULL       | C        |
+-----------------------------------+-------+---------+------------+----------+


các yêu cầu kết hợp
~~~~~~~~~~~~~~~~~~~

Mọi request khả dĩ đều được xác định đầy đủ bởi một số tổ hợp các flag trong phần trước. Để thuận tiện, buffer protocol cung cấp các tổ hợp thường dùng dưới dạng các flag đơn.

Trong bảng sau, *U* biểu thị tính liên tục không xác định. Consumer sẽ phải gọi :c:func:`PyBuffer_IsContiguous` để xác định tính liên tục.

.. tabularcolumns:: |p{0.35\linewidth}|l|l|l|l|l|l|

+-------------------------------+-------+---------+------------+--------+----------+--------+
| Yêu cầu                       | shape | strides | suboffsets | contig | chỉ đọc  | format |
+===============================+=======+=========+============+========+==========+========+
| .. c:macro:: PyBUF_FULL       | có    | có      | nếu cần    | U      | 0        | có     |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_FULL_RO    | có    | có      | nếu cần    | U      | 1 hoặc 0 | có     |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_RECORDS    | có    | có      | NULL       | U      | 0        | có     |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_RECORDS_RO | có    | có      | NULL       | U      | 1 hoặc 0 | có     |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_STRIDED    | có    | có      | NULL       | U      | 0        | NULL   |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_STRIDED_RO | có    | có      | NULL       | U      | 1 hoặc 0 | NULL   |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_CONTIG     | có    | NULL    | NULL       | C      | 0        | NULL   |
+-------------------------------+-------+---------+------------+--------+----------+--------+
| .. c:macro:: PyBUF_CONTIG_RO  | có    | NULL    | NULL       | C      | 1 hoặc 0 | NULL   |
+-------------------------------+-------+---------+------------+--------+----------+--------+


.. _`Complex arrays`:

Mảng phức tạp
=============

Theo kiểu NumPy: shape và strides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cấu trúc logic của các mảng theo kiểu NumPy được xác định bởi :c:member:`~Py_buffer.itemsize`,
:c:member:`~Py_buffer.ndim`, :c:member:`~Py_buffer.shape` và :c:member:`~Py_buffer.strides`.

Nếu ``ndim == 0``, vị trí bộ nhớ được :c:member:`~Py_buffer.buf` trỏ tới được diễn giải là một scalar có kích thước :c:member:`~Py_buffer.itemsize`. Trong trường hợp đó, cả :c:member:`~Py_buffer.shape` và :c:member:`~Py_buffer.strides` đều là ``NULL``.

Nếu :c:member:`~Py_buffer.strides` là ``NULL``, mảng được diễn giải là một mảng C n-chiều tiêu chuẩn. Nếu không, consumer phải truy cập mảng n-chiều như sau:

.. code-block:: c

   ptr = (char *)buf + indices[0] * strides[0] + ... + indices[n-1] * strides[n-1];
   item = *((typeof(item) *)ptr);


Như đã lưu ý ở trên, :c:member:`~Py_buffer.buf` có thể trỏ tới bất kỳ vị trí nào bên trong khối bộ nhớ thực tế. Exporter có thể kiểm tra tính hợp lệ của một buffer bằng hàm này:

.. code-block:: python

   def verify_structure(memlen, itemsize, ndim, shape, strides, offset):
       """Verify that the parameters represent a valid array within
          the bounds of the allocated memory:
              char *mem: start of the physical memory block
              memlen: length of the physical memory block
              offset: (char *)buf - mem
       """
       if offset % itemsize:
           return False
       if offset < 0 or offset+itemsize > memlen:
           return False
       if any(v % itemsize for v in strides):
           return False

       if ndim <= 0:
           return ndim == 0 and not shape and not strides
       if 0 in shape:
           return True

       imin = sum(strides[j]*(shape[j]-1) for j in range(ndim)
                  if strides[j] <= 0)
       imax = sum(strides[j]*(shape[j]-1) for j in range(ndim)
                  if strides[j] > 0)

       return 0 <= offset+imin and offset+imax+itemsize <= memlen


PIL-style: shape, strides và suboffsets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ngoài các phần tử thông thường, mảng PIL-style có thể chứa các con trỏ cần được đi theo để đến phần tử tiếp theo trong một chiều. Ví dụ, mảng C ba chiều thông thường ``char v[2][2][3]`` cũng có thể được xem như một mảng gồm 2 con trỏ trỏ tới 2 mảng hai chiều: ``char (*v[2])[2][3]``. Trong biểu diễn suboffsets, hai con trỏ đó có thể được nhúng ở đầu :c:member:`~Py_buffer.buf`, trỏ tới hai mảng ``char x[2][3]`` có thể nằm ở bất kỳ vị trí nào trong bộ nhớ.


Sau đây là một hàm trả về con trỏ tới phần tử trong một mảng N-D được trỏ tới bởi một chỉ mục N-chiều khi có cả các stride không phải ``NULL`` và suboffsets::

   void *get_item_pointer(int ndim, void *buf, Py_ssize_t *strides,
                          Py_ssize_t *suboffsets, Py_ssize_t *indices) {
       char *pointer = (char*)buf;
       int i;
       for (i = 0; i < ndim; i++) {
           pointer += strides[i] * indices[i];
           if (suboffsets[i] >=0 ) {
               pointer = *((char**)pointer) + suboffsets[i];
           }
       }
       return (void*)pointer;
   }


Các hàm liên quan đến buffer
============================

.. c:function:: int PyObject_CheckBuffer(PyObject *obj)

   Trả về ``1`` nếu *obj* hỗ trợ giao diện buffer, nếu không thì trả về ``0``. Khi trả về ``1``, điều đó không đảm bảo rằng :c:func:`PyObject_GetBuffer` sẽ thành công. Hàm này luôn thành công.


.. c:function:: int PyObject_GetBuffer(PyObject *exporter, Py_buffer *view, int flags)

   Gửi yêu cầu đến *exporter* để điền *view* theo chỉ định của *flags*. Nếu exporter không thể cung cấp buffer có kiểu chính xác, nó PHẢI phát sinh
   :exc:`BufferError`, đặt ``view->obj`` thành ``NULL`` và trả về ``-1``.

   Khi thành công, điền *view*, đặt ``view->obj`` thành một tham chiếu mới đến *exporter* và trả về 0. Trong trường hợp các buffer provider liên kết với nhau chuyển hướng yêu cầu đến một đối tượng duy nhất, ``view->obj`` CÓ THỂ tham chiếu đến đối tượng này thay vì *exporter* (Xem :ref:`Cấu trúc đối tượng buffer <buffer-structs>`).

   Các lời gọi thành công đến :c:func:`PyObject_GetBuffer` phải đi kèm với các lời gọi đến :c:func:`PyBuffer_Release`, tương tự như :c:func:`malloc` và :c:func:`free`. Do đó, sau khi consumer sử dụng xong buffer, phải gọi :c:func:`PyBuffer_Release` đúng một lần.


.. c:function:: void PyBuffer_Release(Py_buffer *view)

   Giải phóng buffer *view* và giải phóng :term:`strong reference` (tức là giảm số lượng tham chiếu) đến đối tượng hỗ trợ view, ``view->obj``. PHẢI gọi hàm này khi buffer không còn được sử dụng; nếu không, có thể xảy ra rò rỉ tham chiếu.

   Việc gọi hàm này trên một buffer không được lấy thông qua là một lỗi
   :c:func:`PyObject_GetBuffer`.


.. c:function:: Py_ssize_t PyBuffer_SizeFromFormat(const char *format)

   Trả về :c:member:`~Py_buffer.itemsize` ngầm định từ :c:member:`~Py_buffer.format`. Khi có lỗi, phát sinh một ngoại lệ và trả về -1.

   .. versionadded:: 3.9


.. c:function:: int PyBuffer_IsContiguous(const Py_buffer *view, char order)

   Trả về ``1`` nếu vùng nhớ được xác định bởi *view* có kiểu C (*order* là ``'C'``) hoặc kiểu Fortran (*order* là ``'F'``) :term:`contiguous`, hoặc thuộc cả hai kiểu (*order* là ``'A'``). Trả về ``0`` nếu không. Hàm này luôn thành công.


.. c:function:: void* PyBuffer_GetPointer(const Py_buffer *view, const Py_ssize_t *indices)

   Lấy vùng nhớ được trỏ tới bởi *indices* bên trong *view* đã cho. *indices* phải trỏ tới một mảng gồm các ``view->ndim`` chỉ số.


.. c:function:: int PyBuffer_FromContiguous(const Py_buffer *view, const void *buf, Py_ssize_t len, char fort)

   Sao chép *len* byte liên tiếp từ *buf* sang *view*. *fort* có thể là ``'C'`` hoặc ``'F'`` (tương ứng với thứ tự kiểu C hoặc kiểu Fortran). Trả về ``0`` khi thành công và ``-1`` khi có lỗi.


.. c:function:: int PyBuffer_ToContiguous(void *buf, const Py_buffer *src, Py_ssize_t len, char order)

   Sao chép *len* byte từ *src* sang biểu diễn liên tiếp của nó trong *buf*. *order* có thể là ``'C'``, ``'F'`` hoặc ``'A'`` (tương ứng với thứ tự kiểu C, kiểu Fortran hoặc cả hai). Trả về ``0`` khi thành công và ``-1`` khi có lỗi.

   Hàm này không thành công nếu *len* != *src->len*.


.. c:function:: int PyObject_CopyData(PyObject *dest, PyObject *src)

   Sao chép dữ liệu từ *src* sang *dest* buffer. Có thể chuyển đổi giữa các buffer kiểu C và kiểu Fortran.

   ``0`` được trả về khi thành công, ``-1`` khi có lỗi.

.. c:function:: void PyBuffer_FillContiguousStrides(int ndims, Py_ssize_t *shape, Py_ssize_t *strides, int itemsize, char order)

   Điền mảng *strides* bằng các bước theo byte của một mảng :term:`contiguous` (kiểu C nếu *order* là ``'C'`` hoặc kiểu Fortran nếu *order* là ``'F'``) có shape đã cho và số byte trên mỗi phần tử đã cho.


.. c:function:: int PyBuffer_FillInfo(Py_buffer *view, PyObject *exporter, void *buf, Py_ssize_t len, int readonly, int flags)

   Xử lý các yêu cầu về buffer cho một exporter muốn cung cấp *buf* có kích thước *len*, với khả năng ghi được thiết lập theo *readonly*. *buf* được diễn giải là một chuỗi các byte không dấu.

   Đối số *flags* cho biết loại yêu cầu. Hàm này luôn điền *view* theo chỉ định của flags, trừ khi *buf* đã được chỉ định là chỉ đọc và :c:macro:`PyBUF_WRITABLE` được thiết lập trong *flags*.

   Khi thành công, đặt ``view->obj`` thành một tham chiếu mới đến *exporter* và trả về 0. Nếu không, raise :exc:`BufferError`, đặt ``view->obj`` thành ``NULL`` và trả về ``-1``;”

   Nếu hàm này được sử dụng như một phần của :ref:`getbufferproc <buffer-structs>`, *exporter* PHẢI được đặt thành đối tượng xuất và *flags* phải được truyền nguyên trạng. Nếu không, *exporter* PHẢI là ``NULL``.
