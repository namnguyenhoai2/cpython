.. highlight:: c

.. _extension-modules:

Định nghĩa các mô-đun mở rộng
-----------------------------

Một phần mở rộng C cho CPython là một thư viện dùng chung (ví dụ: tệp ``.so`` trên Linux, DLL ``.pyd`` trên Windows), có thể được tải vào tiến trình Python (ví dụ: được biên dịch với các tùy chọn trình biên dịch tương thích), và xuất một :ref:`hàm khởi tạo <extension-export-hook>`.

Để có thể được import theo mặc định (nghĩa là bởi
:py:class:`importlib.machinery.ExtensionFileLoader`), thư viện dùng chung phải có sẵn trong :py:attr:`sys.path`, và phải được đặt tên theo tên mô-đun cộng với một phần mở rộng được liệt kê trong
:py:attr:`importlib.machinery.EXTENSION_SUFFIXES`.

.. note::

   Tốt nhất nên xây dựng, đóng gói và phân phối các mô-đun mở rộng bằng các công cụ của bên thứ ba; việc này nằm ngoài phạm vi của tài liệu này. Một công cụ phù hợp là Setuptools, tài liệu của công cụ này có tại https://setuptools.pypa.io/en/latest/setuptools.html.

Thông thường, hàm khởi tạo trả về một định nghĩa mô-đun được khởi tạo bằng :c:func:`PyModuleDef_Init`. Điều này cho phép chia quá trình tạo thành nhiều giai đoạn:

- Trước khi bất kỳ đoạn mã đáng kể nào được thực thi, Python có thể xác định mô-đun hỗ trợ những khả năng nào, đồng thời điều chỉnh môi trường hoặc từ chối tải một phần mở rộng không tương thích.
- Theo mặc định, chính Python tạo đối tượng module -- tức là, nó thực hiện tương đương với :py:meth:`object.__new__` đối với các lớp. Nó cũng thiết lập các thuộc tính ban đầu như :attr:`~module.__package__` và
  :attr:`~module.__loader__`.
- Sau đó, đối tượng module được khởi tạo bằng mã dành riêng cho extension -- tương đương với :py:meth:`~object.__init__` trên các lớp.

Điều này được gọi là *khởi tạo nhiều giai đoạn* để phân biệt với lược đồ *khởi tạo một giai đoạn* cũ (nhưng vẫn được hỗ trợ), trong đó hàm khởi tạo trả về một module đã được xây dựng hoàn chỉnh. Xem :ref:`phần khởi tạo một giai đoạn bên dưới <single-phase-initialization>` để biết chi tiết.

.. versionchanged:: 3.5

   Đã bổ sung hỗ trợ cho khởi tạo nhiều giai đoạn (:pep:`489`).


Nhiều thực thể module
.....................

Theo mặc định, các extension module không phải là singleton. Ví dụ: nếu mục nhập :py:attr:`sys.modules` bị xóa rồi module được import lại, một đối tượng module mới sẽ được tạo và thường được nạp các đối tượng method và type mới. Module cũ sẽ được xử lý bởi cơ chế thu gom rác thông thường. Điều này phản ánh hành vi của các module Python thuần.

Các thực thể module bổ sung có thể được tạo trong
:ref:`các trình thông dịch con <sub-interpreter-support>` hoặc sau khi runtime Python được khởi tạo lại (:c:func:`Py_Finalize` và :c:func:`Py_Initialize`). Trong những trường hợp này, việc chia sẻ các đối tượng Python giữa các instance của module có thể gây ra lỗi nghiêm trọng hoặc hành vi không xác định.

Để tránh những vấn đề như vậy, mỗi instance của extension module phải được *cô lập*: các thay đổi đối với một instance không được ngầm ảnh hưởng đến các instance khác, và mọi trạng thái do module sở hữu, bao gồm các tham chiếu đến đối tượng Python, phải dành riêng cho một instance cụ thể của module. Xem :ref:`isolating-extensions-howto` để biết thêm chi tiết và hướng dẫn thực tế.

Một cách đơn giản hơn để tránh những vấn đề này là
:ref:`phát sinh lỗi khi khởi tạo lại <isolating-extensions-optout>`.

Tất cả các module được kỳ vọng hỗ trợ
:ref:`các trình thông dịch con <sub-interpreter-support>`, hoặc phải báo hiệu rõ ràng rằng chúng không hỗ trợ. Điều này thường đạt được bằng cách cô lập hoặc chặn việc khởi tạo lại, như trên. Một module cũng có thể bị giới hạn chỉ chạy trong trình thông dịch chính bằng cách sử dụng slot :c:data:`Py_mod_multiple_interpreters`.


.. _extension-export-hook:

Hàm khởi tạo
............

Hàm khởi tạo được định nghĩa bởi một extension module có chữ ký sau:

.. c:function:: PyObject* PyInit_modulename(void)

Tên của hàm phải là :samp:`PyInit_{<name>}`, trong đó ``<name>`` được thay thế bằng tên của module.

Đối với các module có tên chỉ gồm ASCII, hàm phải được đặt tên là
:samp:`PyInit_{<name>}`, trong đó ``<name>`` được thay thế bằng tên của module. Khi sử dụng :ref:`multi-phase-initialization`, có thể dùng tên module không phải ASCII. Trong trường hợp này, tên hàm khởi tạo là
:samp:`PyInitU_{<name>}`, trong đó ``<name>`` được mã hóa bằng encoding *punycode* của Python, với dấu gạch nối được thay thế bằng dấu gạch dưới. Trong Python:

.. code-block:: python

    def initfunc_name(name):
        try:
            suffix = b'_' + name.encode('ascii')
        except UnicodeEncodeError:
            suffix = b'U_' + name.encode('punycode').replace(b'-', b'_')
        return b'PyInit' + suffix

Bạn nên định nghĩa hàm khởi tạo bằng một helper macro:

.. c:macro:: PyMODINIT_FUNC

   Khai báo một hàm khởi tạo extension module. Macro này:

   * chỉ định kiểu trả về :c:expr:`PyObject*`,
   * thêm mọi khai báo liên kết đặc biệt mà nền tảng yêu cầu, và
   * đối với C++, khai báo hàm là ``extern "C"``.

Ví dụ: một module có tên ``spam`` sẽ được định nghĩa như sau::

   static struct PyModuleDef spam_module = {
       .m_base = PyModuleDef_HEAD_INIT,
       .m_name = "spam",
       ...
   };

   PyMODINIT_FUNC
   PyInit_spam(void)
   {
       return PyModuleDef_Init(&spam_module);
   }

Có thể export nhiều module từ một shared library bằng cách định nghĩa nhiều hàm khởi tạo. Tuy nhiên, để import chúng, bạn cần sử dụng symbolic link hoặc importer tùy chỉnh, vì theo mặc định, chỉ tìm thấy hàm tương ứng với tên tệp. Xem phần `Multiple modules in one library <https://peps.python.org/pep-0489/#multiple-modules-in-one-library>`__ trong :pep:`489` để biết chi tiết.

Hàm khởi tạo thường là mục không phải \ ``static`` duy nhất được định nghĩa trong mã nguồn C của module.


.. _multi-phase-initialization:

Khởi tạo nhiều giai đoạn
........................

Thông thường, :ref:`hàm khởi tạo <extension-export-hook>` (``PyInit_modulename``) trả về một thực thể :c:type:`PyModuleDef` có ``NULL`` :c:member:`~PyModuleDef.m_slots` không phải ``NULL``. Trước khi được trả về, thực thể ``PyModuleDef`` phải được khởi tạo bằng hàm sau:


.. c:function:: PyObject* PyModuleDef_Init(PyModuleDef *def)

   Đảm bảo rằng định nghĩa module là một đối tượng Python được khởi tạo đúng cách, báo cáo chính xác kiểu của nó và số lượng tham chiếu.

   Trả về *def* được chuyển kiểu thành ``PyObject*``, hoặc ``NULL`` nếu xảy ra lỗi.

   Việc gọi hàm này là bắt buộc đối với :ref:`multi-phase-initialization`. Không nên sử dụng hàm này trong các ngữ cảnh khác.

   Lưu ý rằng Python giả định các cấu trúc ``PyModuleDef`` được cấp phát tĩnh. Hàm này có thể trả về một tham chiếu mới hoặc một tham chiếu mượn; không được giải phóng tham chiếu này.

   .. versionadded:: 3.5


.. _single-phase-initialization:

Khởi tạo một giai đoạn kiểu cũ
..............................

.. attention::
   Khởi tạo một giai đoạn là cơ chế kiểu cũ để khởi tạo các module mở rộng, với những hạn chế và lỗi thiết kế đã biết. Tác giả module mở rộng được khuyến khích sử dụng khởi tạo nhiều giai đoạn thay thế.

Trong quá trình khởi tạo một pha,
:ref:`hàm khởi tạo <extension-export-hook>` (``PyInit_modulename``) sẽ tạo, điền dữ liệu và trả về một đối tượng module. Việc này thường được thực hiện bằng :c:func:`PyModule_Create` và các hàm như
:c:func:`PyModule_AddObjectRef`.

Việc khởi tạo một pha khác với :ref:`mặc định <multi-phase-initialization>` ở những điểm sau:

* Các module khởi tạo một pha là, hay chính xác hơn là *chứa*, các “singleton”.

  Khi module được khởi tạo lần đầu, Python lưu nội dung của ``__dict__`` của module (thông thường là các hàm và kiểu của module).

  Trong các lần import tiếp theo, Python không gọi lại hàm khởi tạo. Thay vào đó, Python tạo một đối tượng module mới với ``__dict__`` mới, rồi sao chép nội dung đã lưu vào đó. Ví dụ, với một module khởi tạo một pha ``_testsinglephase`` [#testsinglephase]_ định nghĩa một hàm ``sum`` và một lớp ngoại lệ ``error``:

  .. code-block:: python

     >>> import sys
     >>> import _testsinglephase as one
     >>> del sys.modules['_testsinglephase']
     >>> import _testsinglephase as two
     >>> one is two
     False
     >>> one.__dict__ is two.__dict__
     False
     >>> one.sum is two.sum
     True
     >>> one.error is two.error
     True

  Hành vi chính xác nên được xem là một chi tiết triển khai của CPython.

* Để khắc phục việc ``PyInit_modulename`` không nhận đối số *spec*, một phần trạng thái của cơ chế import được lưu lại và áp dụng cho module phù hợp đầu tiên được tạo trong lệnh gọi ``PyInit_modulename``. Cụ thể, khi một sub-module được import, cơ chế này thêm tên package cha vào trước tên của module.

  Một hàm ``PyInit_modulename`` khởi tạo một pha nên tạo đối tượng module “của nó” sớm nhất có thể, trước khi bất kỳ đối tượng module nào khác được tạo.

* Không hỗ trợ tên module không phải ASCII (``PyInitU_modulename``).

* Các module khởi tạo một pha hỗ trợ những hàm tra cứu module như
  :c:func:`PyState_FindModule`.

.. [#testsinglephase] ``_testsinglephase`` là một module nội bộ được sử dụng trong bộ kiểm thử tự thân của CPython; bản cài đặt của bạn có thể có hoặc không có module này.
