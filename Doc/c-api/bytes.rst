.. highlight:: c

.. _bytesobjects:

Đối tượng bytes
---------------

Các hàm này sẽ phát sinh :exc:`TypeError` khi mong đợi một tham số bytes nhưng được gọi với một tham số không phải bytes.

.. impl-detail::

   Bộ đệm nội bộ của :c:type:`PyBytesObject` luôn bao gồm thêm một byte null ở cuối để tương thích với các chuỗi C kết thúc bằng null. Byte bổ sung này không được tính trong :c:func:`PyBytes_Size` cũng như trong các đối số *độ dài* và *kích thước* khác nhau của các hàm bên dưới.

.. index:: pair: object; bytes


.. c:type:: PyBytesObject

   Kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng bytes trong Python.


.. c:var:: PyTypeObject PyBytes_Type

   Thể hiện này của :c:type:`PyTypeObject` đại diện cho kiểu bytes trong Python; nó chính là đối tượng :class:`bytes` ở lớp Python.


.. c:function:: int PyBytes_Check(PyObject *o)

   Trả về true nếu đối tượng *o* là một đối tượng bytes hoặc là một thể hiện của kiểu con của kiểu bytes. Hàm này luôn thành công.


.. c:function:: int PyBytes_CheckExact(PyObject *o)

   Trả về true nếu đối tượng *o* là một đối tượng bytes nhưng không phải là một thể hiện của kiểu con của kiểu bytes. Hàm này luôn thành công.


.. c:function:: PyObject* PyBytes_FromString(const char *v)

   Trả về một đối tượng bytes mới chứa bản sao của chuỗi *v* làm giá trị khi thành công và ``NULL`` khi thất bại. Tham số *v* không được là ``NULL``; tham số này sẽ không được kiểm tra.


.. c:function:: PyObject* PyBytes_FromStringAndSize(const char *v, Py_ssize_t len)

   Trả về một đối tượng bytes mới chứa bản sao của chuỗi *v* làm giá trị và có độ dài *len* khi thành công, và ``NULL`` khi thất bại. Nếu *v* là ``NULL``, nội dung của đối tượng bytes sẽ chưa được khởi tạo.


.. c:function:: PyObject* PyBytes_FromFormat(const char *format, ...)

   Nhận một chuỗi :c:func:`printf`\ -style *format* của C và một số lượng đối số thay đổi, tính kích thước của đối tượng bytes Python kết quả rồi trả về một đối tượng bytes với các giá trị được định dạng vào đó. Các đối số biến đổi phải là các kiểu C và phải tương ứng chính xác với các ký tự định dạng trong chuỗi *format*. Các ký tự định dạng sau được cho phép:

   .. % XXX: This should be exactly the same as the table in PyErr_Format.
   .. % One should just refer to the other.

   .. tabularcolumns:: |l|l|L|

   +-------------------+---------------+--------------------------------+
   | Format Characters | Type          | Comment                        |
   +===================+===============+================================+
   | ``%%``            | *n/a*         | The literal % character.       |
   +-------------------+---------------+--------------------------------+
   | ``%c``            | int           | A single byte,                 |
   |                   |               | represented as a C int.        |
   +-------------------+---------------+--------------------------------+
   | ``%d``            | int           | Equivalent to                  |
   |                   |               | ``printf("%d")``. [1]_         |
   +-------------------+---------------+--------------------------------+
   | ``%u``            | unsigned int  | Equivalent to                  |
   |                   |               | ``printf("%u")``. [1]_         |
   +-------------------+---------------+--------------------------------+
   | ``%ld``           | long          | Equivalent to                  |
   |                   |               | ``printf("%ld")``. [1]_        |
   +-------------------+---------------+--------------------------------+
   | ``%lu``           | unsigned long | Equivalent to                  |
   |                   |               | ``printf("%lu")``. [1]_        |
   +-------------------+---------------+--------------------------------+
   | ``%zd``           | :c:type:`\    | Equivalent to                  |
   |                   | Py_ssize_t`   | ``printf("%zd")``. [1]_        |
   +-------------------+---------------+--------------------------------+
   | ``%zu``           | size_t        | Equivalent to                  |
   |                   |               | ``printf("%zu")``. [1]_        |
   +-------------------+---------------+--------------------------------+
   | ``%i``            | int           | Equivalent to                  |
   |                   |               | ``printf("%i")``. [1]_         |
   +-------------------+---------------+--------------------------------+
   | ``%x``            | int           | Equivalent to                  |
   |                   |               | ``printf("%x")``. [1]_         |
   +-------------------+---------------+--------------------------------+
   | ``%s``            | const char\*  | A null-terminated C character  |
   |                   |               | array.                         |
   +-------------------+---------------+--------------------------------+
   | ``%p``            | const void\*  | The hex representation of a C  |
   |                   |               | pointer. Mostly equivalent to  |
   |                   |               | ``printf("%p")`` except that   |
   |                   |               | it is guaranteed to start with |
   |                   |               | the literal ``0x`` regardless  |
   |                   |               | of what the platform's         |
   |                   |               | ``printf`` yields.             |
   +-------------------+---------------+--------------------------------+

   Ký tự định dạng không được nhận diện sẽ khiến toàn bộ phần còn lại của chuỗi định dạng được sao chép nguyên trạng vào đối tượng kết quả, đồng thời mọi đối số thừa sẽ bị loại bỏ.

   .. [1] Đối với các chỉ định số nguyên (d, u, ld, lu, zd, zu, i, x): cờ chuyển đổi 0 vẫn có tác dụng ngay cả khi đã chỉ định độ chính xác.


.. c:function:: PyObject* PyBytes_FromFormatV(const char *format, va_list vargs)

   Tương tự như :c:func:`PyBytes_FromFormat`, ngoại trừ việc hàm này nhận chính xác hai đối số.


.. c:function:: PyObject* PyBytes_FromObject(PyObject *o)

   Trả về biểu diễn bytes của đối tượng *o* triển khai buffer protocol.

   .. note::
      Nếu đối tượng triển khai buffer protocol, thì buffer không được thay đổi trong khi đối tượng bytes đang được tạo.


.. c:function:: Py_ssize_t PyBytes_Size(PyObject *o)

   Trả về độ dài của các byte trong đối tượng bytes *o*.


.. c:function:: Py_ssize_t PyBytes_GET_SIZE(PyObject *o)

   Tương tự như :c:func:`PyBytes_Size`, nhưng không kiểm tra lỗi.


.. c:function:: char* PyBytes_AsString(PyObject *o)

   Trả về con trỏ đến nội dung của *o*. Con trỏ này trỏ đến buffer nội bộ của *o*, gồm ``len(o) + 1`` byte. Byte cuối cùng trong buffer luôn là null, bất kể có bất kỳ byte null nào khác hay không. Dữ liệu không được sửa đổi theo bất kỳ cách nào, trừ khi đối tượng vừa được tạo bằng ``PyBytes_FromStringAndSize(NULL, size)``. Không được giải phóng dữ liệu. Nếu *o* hoàn toàn không phải là đối tượng bytes, :c:func:`PyBytes_AsString` trả về ``NULL`` và phát sinh :exc:`TypeError`.


.. c:function:: char* PyBytes_AS_STRING(PyObject *string)

   Tương tự như :c:func:`PyBytes_AsString`, nhưng không kiểm tra lỗi.


.. c:function:: int PyBytes_AsStringAndSize(PyObject *obj, char **buffer, Py_ssize_t *length)

   Trả về nội dung kết thúc bằng null của đối tượng *obj* thông qua các biến đầu ra *buffer* và *length*. Trả về ``0`` khi thành công.

   Nếu *length* là ``NULL``, đối tượng bytes có thể không chứa các byte null nhúng; nếu có, hàm trả về ``-1`` và phát sinh :exc:`ValueError`.

   Bộ đệm đề cập đến bộ đệm nội bộ của *obj*, trong đó có thêm một byte null ở cuối (không được tính trong *length*). Dữ liệu không được sửa đổi dưới bất kỳ hình thức nào, trừ khi đối tượng vừa được tạo bằng ``PyBytes_FromStringAndSize(NULL, size)``. Không được giải phóng đối tượng này. Nếu *obj* hoàn toàn không phải là đối tượng bytes, :c:func:`PyBytes_AsStringAndSize` trả về ``-1`` và phát sinh :exc:`TypeError`.

   .. versionchanged:: 3.5
      Trước đây, :exc:`TypeError` được phát sinh khi gặp các byte null nằm trong đối tượng bytes.


.. c:function:: void PyBytes_Concat(PyObject **bytes, PyObject *newpart)

   Tạo một đối tượng bytes mới trong *\*bytes*, chứa nội dung của *newpart* được nối vào *bytes*; bên gọi sẽ sở hữu tham chiếu mới. Tham chiếu đến giá trị cũ của *bytes* sẽ bị ":term:`stolen <steal>`". Nếu không thể tạo đối tượng mới, tham chiếu cũ đến *bytes* vẫn sẽ bị "stolen", giá trị của *\*bytes* sẽ được đặt thành ``NULL``, và ngoại lệ thích hợp sẽ được thiết lập.

   .. note::
      Nếu *newpart* triển khai buffer protocol, thì không được thay đổi bộ đệm trong khi đối tượng bytes mới đang được tạo.

.. c:function:: void PyBytes_ConcatAndDel(PyObject **bytes, PyObject *newpart)

   Tạo một đối tượng bytes mới trong *\*bytes*, chứa nội dung của *newpart* được nối vào *bytes*. Phiên bản này giải phóng :term:`strong reference` khỏi *newpart* (tức là giảm reference count của đối tượng đó).

   .. note::
      Nếu *newpart* triển khai buffer protocol, thì không được thay đổi bộ đệm trong khi đối tượng bytes mới đang được tạo.


.. c:function:: PyObject* PyBytes_Join(PyObject *sep, PyObject *iterable)

   Tương tự như ``sep.join(iterable)`` trong Python.

   *sep* phải là một đối tượng :class:`bytes` của Python. (Lưu ý rằng :c:func:`PyUnicode_Join` chấp nhận dấu phân cách ``NULL`` và xử lý nó như một khoảng trắng, trong khi :c:func:`PyBytes_Join` không chấp nhận dấu phân cách ``NULL``.)

   *iterable* phải là một đối tượng iterable tạo ra các đối tượng triển khai
   :ref:`buffer protocol <bufferobjects>`.

   Khi thành công, trả về một đối tượng :class:`bytes` mới. Khi xảy ra lỗi, thiết lập một exception và trả về ``NULL``.

   .. versionadded:: 3.14

   .. note::
      Nếu các đối tượng *iterable* triển khai buffer protocol, thì không được thay đổi các buffer trong khi đối tượng bytes mới đang được tạo.

.. c:function:: int _PyBytes_Resize(PyObject **bytes, Py_ssize_t newsize)

   Thay đổi kích thước một đối tượng bytes. *newsize* sẽ là độ dài mới của đối tượng bytes. Bạn có thể hình dung thao tác này như việc tạo một đối tượng bytes mới và hủy đối tượng cũ, chỉ là hiệu quả hơn. Truyền địa chỉ của một đối tượng bytes hiện có dưới dạng lvalue (địa chỉ này có thể được ghi vào), cùng với kích thước mới mong muốn. Khi thành công, *\*bytes* chứa đối tượng bytes đã được thay đổi kích thước và ``0`` được trả về; địa chỉ trong *\*bytes* có thể khác giá trị đầu vào. Nếu thao tác cấp phát lại thất bại, đối tượng bytes ban đầu tại *\*bytes* sẽ được giải phóng, *\*bytes* được đặt thành ``NULL``, :exc:`MemoryError` được thiết lập và ``-1`` được trả về.


.. c:function:: PyObject *PyBytes_Repr(PyObject *bytes, int smartquotes)

   Lấy biểu diễn chuỗi của *bytes*. Hiện tại, hàm này được dùng để triển khai :meth:`!bytes.__repr__` trong Python.

   Hàm này không thực hiện kiểm tra kiểu; việc truyền *bytes* dưới dạng một đối tượng không phải bytes hoặc ``NULL`` sẽ dẫn đến hành vi không xác định.

   Nếu *smartquotes* là true, biểu diễn sẽ sử dụng chuỗi được đặt trong dấu nháy kép thay vì dấu nháy đơn khi có dấu nháy đơn trong *bytes*. Ví dụ: chuỗi byte ``'Python'`` sẽ được biểu diễn dưới dạng ``b"'Python'"`` khi *smartquotes* là true, hoặc ``b'\'Python\''`` khi giá trị này là false.

   Khi thành công, hàm này trả về một :term:`strong reference` tới một Python
   :class:`str` object chứa biểu diễn. Khi thất bại, hàm này trả về ``NULL`` cùng với một exception được thiết lập.


.. c:function:: PyObject *PyBytes_DecodeEscape(const char *s, Py_ssize_t len, const char *errors, Py_ssize_t unicode, const char *recode_encoding)

   Hủy escape một chuỗi có escape bằng dấu gạch chéo ngược *s*. *s* không được là ``NULL``. *len* phải là kích thước của *s*.

   *errors* phải là một trong các giá trị ``"strict"``, ``"replace"`` hoặc ``"ignore"``. Nếu *errors* là ``NULL``, thì ``"strict"`` được sử dụng theo mặc định.

   Khi thành công, hàm này trả về một :term:`strong reference` tới một Python
   :class:`bytes` đối tượng chứa chuỗi đã bỏ ký tự escape. Khi thất bại, hàm này trả về ``NULL`` cùng với một ngoại lệ đã được thiết lập.

   .. versionchanged:: 3.9
      *unicode* và *recode_encoding* hiện không còn được sử dụng.
