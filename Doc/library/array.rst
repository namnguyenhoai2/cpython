:mod:`!array` --- Mảng hiệu quả gồm các giá trị số
==================================================

.. module:: array
   :synopsis: Các mảng tiết kiệm không gian gồm các giá trị số có cùng kiểu.

.. index:: single: arrays

--------------

Mô-đun này định nghĩa một kiểu đối tượng có thể biểu diễn gọn một mảng gồm các giá trị cơ bản: ký tự, số nguyên, số dấu phẩy động. Các mảng là các kiểu :term:`sequence` có thể thay đổi và hoạt động gần giống như danh sách, ngoại trừ việc kiểu của các đối tượng được lưu trữ trong chúng bị giới hạn. Kiểu này được chỉ định tại thời điểm tạo đối tượng bằng cách sử dụng một
:dfn:`mã kiểu`, là một ký tự đơn. Các mã kiểu sau được định nghĩa:

+---------+--------------------+---------------+-------------------------------------+---------+
| Mã kiểu | Kiểu C             | Kiểu Python   | Kích thước tối thiểu tính bằng byte | Ghi chú |
+=========+====================+===============+=====================================+=========+
| ``'b'`` | signed char        | int           | 1                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'B'`` | unsigned char      | int           | 1                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'u'`` | wchar_t            | Ký tự Unicode | 2                                   | \(1)    |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'w'`` | Py_UCS4            | Ký tự Unicode | 4                                   | \(2)    |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'h'`` | short có dấu       | int           | 2                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'H'`` | short không dấu    | int           | 2                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'i'`` | signed int         | int           | 2                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'I'`` | unsigned int       | int           | 2                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'l'`` | signed long        | int           | 4                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'L'`` | unsigned long      | int           | 4                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'q'`` | signed long long   | int           | 8                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'Q'`` | unsigned long long | int           | 8                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'f'`` | float              | float         | 4                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+
| ``'d'`` | double             | float         | 8                                   |         |
+---------+--------------------+---------------+-------------------------------------+---------+

Ghi chú:

(1)
   Giá trị này có thể là 16 bit hoặc 32 bit tùy thuộc vào nền tảng.

   .. versionchanged:: 3.9
      ``array('u')`` hiện sử dụng :c:type:`wchar_t` làm kiểu C thay cho ``Py_UNICODE`` đã lỗi thời. Thay đổi này không ảnh hưởng đến hành vi của nó vì ``Py_UNICODE`` là bí danh của :c:type:`wchar_t` kể từ Python 3.3.

   .. deprecated-removed:: 3.3 3.16
      Vui lòng chuyển sang mã kiểu ``'w'``.

(2)
   .. versionadded:: 3.13

.. seealso::

   :ref:`ctypes <ctypes-fundamental-data-types>` và
   Các mô-đun :ref:`struct <format-characters>`, cũng như các mô-đun bên thứ ba như `numpy <https://numpy.org/doc/stable/reference/arrays.interface.html#object.__array_interface__>`__, sử dụng các mã kiểu tương tự -- nhưng hơi khác nhau --.


Biểu diễn thực tế của các giá trị được xác định bởi kiến trúc máy (nói chính xác hơn là bởi cách triển khai C). Có thể truy cập kích thước thực tế thông qua thuộc tính :attr:`array.itemsize`.

Mô-đun định nghĩa mục sau:


.. data:: typecodes

   Một chuỗi chứa tất cả các mã kiểu có sẵn.


Mô-đun định nghĩa kiểu sau:


.. class:: array(typecode[, initializer])

   Một mảng mới có các phần tử bị giới hạn bởi *typecode*, và được khởi tạo từ giá trị *initializer* tùy chọn, giá trị này phải là một đối tượng :class:`bytes` hoặc :class:`bytearray`, một chuỗi Unicode hoặc một đối tượng có thể lặp chứa các phần tử thuộc kiểu tương ứng.

   Nếu được cung cấp một đối tượng :class:`bytes` hoặc :class:`bytearray`, giá trị khởi tạo sẽ được truyền cho phương thức :meth:`frombytes` của mảng mới; nếu được cung cấp một chuỗi Unicode, giá trị khởi tạo sẽ được truyền cho
   :meth:`fromunicode` method; nếu không, iterator của initializer sẽ được truyền cho :meth:`extend` method để thêm các phần tử ban đầu vào mảng.

   Các đối tượng mảng hỗ trợ các thao tác :ref:`mutable <typesseq-mutable>` :term:`sequence` thông thường gồm lập chỉ mục, cắt lát, nối và nhân. Khi sử dụng phép gán lát cắt, giá trị được gán phải là một đối tượng mảng có cùng mã kiểu; trong mọi trường hợp khác,
   :exc:`TypeError` được phát sinh. Các đối tượng mảng cũng triển khai buffer interface và có thể được sử dụng ở bất cứ nơi nào hỗ trợ :term:`bytes-like objects <bytes-like object>`.

   Mảng có tính :ref:`generic <generics>` theo kiểu của các phần tử bên trong.

   .. audit-event:: array.__new__ typecode,initializer array.array


   .. attribute:: typecode

      Ký tự typecode được dùng để tạo mảng.


   .. attribute:: itemsize

      Độ dài tính bằng byte của một phần tử mảng trong biểu diễn nội bộ.


   .. method:: append(value, /)

      Thêm một phần tử mới có giá trị được chỉ định vào cuối mảng.


   .. method:: buffer_info()

      Trả về một tuple ``(address, length)`` cung cấp địa chỉ bộ nhớ hiện tại và độ dài theo số phần tử của buffer dùng để lưu nội dung của mảng. Kích thước của buffer bộ nhớ tính theo byte có thể được tính bằng ``array.buffer_info()[1] * array.itemsize``. Điều này đôi khi hữu ích khi làm việc với các interface I/O cấp thấp (và vốn không an toàn) yêu cầu địa chỉ bộ nhớ, chẳng hạn như một số
      thao tác :c:func:`!ioctl`. Các số được trả về hợp lệ miễn là mảng còn tồn tại và không có thao tác nào làm thay đổi độ dài được áp dụng cho mảng.

      .. note::

         Khi sử dụng các đối tượng array từ mã được viết bằng C hoặc C++ (cách duy nhất để thực sự sử dụng được thông tin này), việc sử dụng buffer interface được các đối tượng array hỗ trợ sẽ hợp lý hơn. Phương thức này được duy trì để tương thích ngược và nên tránh sử dụng trong mã mới. Buffer interface được mô tả trong :ref:`bufferobjects`.


   .. method:: byteswap()

      "Hoán đổi byte" tất cả các mục trong mảng. Thao tác này chỉ được hỗ trợ cho các giá trị có kích thước 1, 2, 4 hoặc 8 byte; với các kiểu giá trị khác, :exc:`RuntimeError` sẽ được nâng lên. Thao tác này hữu ích khi đọc dữ liệu từ một tệp được ghi trên máy có thứ tự byte khác.


   .. method:: count(value, /)

      Trả về số lần xuất hiện của *value* trong mảng.


   .. method:: extend(iterable, /)

      Nối các mục từ *iterable* vào cuối mảng. Nếu *iterable* là một array khác, nó phải có mã kiểu *exactly* giống nhau; nếu không, :exc:`TypeError` sẽ được nâng lên. Nếu *iterable* không phải là một array, nó phải là iterable và các phần tử của nó phải có đúng kiểu để được nối vào mảng.


   .. method:: frombytes(buffer, /)

      Nối các mục từ :term:`bytes-like object`, diễn giải nội dung của đối tượng này dưới dạng một array gồm các giá trị máy (như thể đối tượng này đã được đọc từ một tệp bằng phương thức :meth:`fromfile`).

      .. versionadded:: 3.2
         :meth:`!fromstring` is renamed to :meth:`frombytes` for clarity.


   .. method:: fromfile(f, n, /)

      Đọc *n* mục (dưới dạng các giá trị máy) từ :term:`file object` *f* và nối chúng vào cuối mảng.  Nếu có ít hơn *n* mục khả dụng,
      :exc:`EOFError` được phát sinh, nhưng các mục đã có vẫn được chèn vào mảng.


   .. method:: fromlist(list, /)

      Nối các mục từ danh sách.  Thao tác này tương đương với ``for x in list: a.append(x)``, ngoại trừ việc nếu xảy ra lỗi kiểu, mảng sẽ không thay đổi.


   .. method:: fromunicode(ustr, /)

      Mở rộng mảng này bằng dữ liệu từ chuỗi Unicode đã cho. Mảng phải có mã kiểu ``'u'`` hoặc ``'w'``; nếu không, :exc:`ValueError` sẽ được phát sinh. Sử dụng ``array.frombytes(unicodestring.encode(enc))`` để nối dữ liệu Unicode vào một mảng thuộc kiểu khác.


   .. method:: index(value[, start[, stop]])

      Trả về *i* nhỏ nhất sao cho *i* là chỉ mục của lần xuất hiện đầu tiên của *value* trong mảng.  Có thể chỉ định các đối số tùy chọn *start* và *stop* để tìm *value* trong một phần của mảng.  Phát sinh
      :exc:`ValueError` nếu không tìm thấy *value*.

      .. versionchanged:: 3.10
         Đã thêm các tham số tùy chọn *start* và *stop*.


   .. method:: insert(index, value, /)

      Chèn một phần tử mới *value* vào mảng trước vị trí *index*. Các giá trị âm được tính tương đối từ cuối mảng.


   .. method:: pop(index=-1, /)

      Xóa phần tử có chỉ mục *i* khỏi mảng và trả về phần tử đó. Đối số tùy chọn mặc định là ``-1``, vì vậy theo mặc định, phần tử cuối cùng sẽ được xóa và trả về.


   .. method:: remove(value, /)

      Xóa lần xuất hiện đầu tiên của *value* khỏi mảng.


   .. method:: clear()

      Xóa tất cả phần tử khỏi mảng.

      .. versionadded:: 3.13


   .. method:: reverse()

      Đảo ngược thứ tự các phần tử trong mảng.


   .. method:: tobytes()

      Chuyển mảng thành một mảng gồm các giá trị máy và trả về biểu diễn dạng byte (cùng một chuỗi byte sẽ được ghi vào một tệp bằng phương thức :meth:`tofile`.)

      .. versionadded:: 3.2
         :meth:`!tostring` is renamed to :meth:`tobytes` for clarity.


   .. method:: tofile(f, /)

      Ghi tất cả các phần tử (dưới dạng giá trị máy) vào :term:`file object` *f*.


   .. method:: tolist()

      Chuyển mảng thành một danh sách thông thường với các phần tử giống nhau.


   .. method:: tounicode()

      Chuyển mảng thành một chuỗi Unicode. Mảng phải có kiểu ``'u'`` hoặc ``'w'``; nếu không, một :exc:`ValueError` sẽ được phát sinh. Sử dụng ``array.tobytes().decode(enc)`` để lấy chuỗi Unicode từ một mảng thuộc kiểu khác.


Biểu diễn chuỗi của các đối tượng mảng có dạng ``array(typecode, initializer)``. *initializer* bị bỏ qua nếu mảng rỗng; nếu không, đó là một chuỗi Unicode nếu *typecode* là ``'u'`` hoặc ``'w'``, còn nếu không thì là một danh sách các số. Biểu diễn chuỗi được đảm bảo có thể chuyển đổi trở lại thành một mảng có cùng kiểu và giá trị bằng :func:`eval`, miễn là
lớp :class:`~array.array` đã được import bằng ``from array import array``. Các biến ``inf`` và ``nan`` cũng phải được định nghĩa nếu lớp này chứa các giá trị dấu phẩy động tương ứng. Ví dụ::

   array('l')
   array('w', 'hello \u2641')
   array('l', [1, 2, 3, 4, 5])
   array('d', [1.0, 2.0, 3.14, -inf, nan])


.. seealso::

   Mô-đun :mod:`struct`
      Đóng gói và giải nén dữ liệu nhị phân không đồng nhất.

   `NumPy <https://numpy.org/>`_
      Gói NumPy định nghĩa một kiểu mảng khác.

.. _`NumPy`: https://numpy.org/
