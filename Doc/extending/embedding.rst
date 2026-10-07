.. highlight:: c


.. _embedding:

**********************************
Nhúng Python vào một ứng dụng khác
**********************************

Các chương trước đã thảo luận về cách mở rộng Python, tức là cách mở rộng chức năng của Python bằng cách gắn vào đó một thư viện các hàm C. Bạn cũng có thể làm theo hướng ngược lại: tăng cường ứng dụng C/C++ của mình bằng cách nhúng Python vào đó. Việc nhúng cho phép ứng dụng của bạn triển khai một số chức năng bằng Python thay vì C hoặc C++. Cách này có thể được sử dụng cho nhiều mục đích; một ví dụ là cho phép người dùng tùy chỉnh ứng dụng theo nhu cầu bằng cách viết một số script bằng Python. Bạn cũng có thể tự sử dụng cách này nếu một số chức năng có thể được viết bằng Python dễ dàng hơn.

Nhúng Python tương tự như mở rộng Python, nhưng không hoàn toàn giống nhau. Điểm khác biệt là khi bạn mở rộng Python, chương trình chính của ứng dụng vẫn là trình thông dịch Python, còn khi bạn nhúng Python, chương trình chính có thể không liên quan gì đến Python — thay vào đó, một số phần của ứng dụng thỉnh thoảng gọi trình thông dịch Python để chạy một đoạn mã Python.

Vì vậy, nếu bạn nhúng Python, bạn đang cung cấp chương trình chính của riêng mình. Một trong những việc mà chương trình chính này phải làm là khởi tạo trình thông dịch Python. Tối thiểu, bạn phải gọi hàm :c:func:`Py_Initialize`. Bạn có thể tùy chọn truyền các đối số dòng lệnh cho Python. Sau đó, bạn có thể gọi trình thông dịch từ bất kỳ phần nào của ứng dụng.

Có một số cách khác nhau để gọi trình thông dịch: bạn có thể truyền một chuỗi chứa các câu lệnh Python cho :c:func:`PyRun_SimpleString`, hoặc truyền một con trỏ tệp stdio và tên tệp (chỉ để nhận diện trong thông báo lỗi) cho :c:func:`PyRun_SimpleFile`. Bạn cũng có thể gọi các thao tác ở cấp thấp hơn được mô tả trong các chương trước để tạo và sử dụng các đối tượng Python.


.. seealso::

   :ref:`c-api-index`
      Các chi tiết về giao diện C của Python được trình bày trong tài liệu này. Bạn có thể tìm thấy rất nhiều thông tin cần thiết tại đây.


.. _high-level-embedding:

Nhúng ở cấp độ rất cao
======================

Cách đơn giản nhất để nhúng Python là sử dụng giao diện cấp rất cao. Giao diện này được thiết kế để thực thi một tập lệnh Python mà không cần tương tác trực tiếp với ứng dụng. Ví dụ, bạn có thể dùng cách này để thực hiện một thao tác nào đó trên một tệp.::

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

   int
   main(int argc, char *argv[])
   {
       PyStatus status;
       PyConfig config;
       PyConfig_InitPythonConfig(&config);

       /* không bắt buộc nhưng được khuyến nghị */
       status = PyConfig_SetBytesString(&config, &config.program_name, argv[0]);
       if (PyStatus_Exception(status)) {
           goto exception;
       }

       status = Py_InitializeFromConfig(&config);
       if (PyStatus_Exception(status)) {
           goto exception;
       }
       PyConfig_Clear(&config);

       PyRun_SimpleString("from time import time,ctime\n"
                          "print('Today is', ctime(time()))\n");
       if (Py_FinalizeEx() < 0) {
           exit(120);
       }
       return 0;

     exception:
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
   }

.. note::

   ``#define PY_SSIZE_T_CLEAN`` được dùng để chỉ ra rằng ``Py_ssize_t`` nên được sử dụng trong một số API thay cho ``int``. Macro này không còn cần thiết kể từ Python 3.13, nhưng chúng tôi vẫn giữ lại để tương thích ngược. Xem :ref:`arg-parsing-string-and-buffers` để biết mô tả về macro này.

Việc thiết lập :c:member:`PyConfig.program_name` nên được gọi trước
:c:func:`Py_InitializeFromConfig` để thông báo cho trình thông dịch về các đường dẫn đến thư viện runtime của Python. Tiếp theo, trình thông dịch Python được khởi tạo bằng
:c:func:`Py_Initialize`, sau đó thực thi một tập lệnh Python được viết cố định để in ngày và giờ. Sau đó, lệnh gọi :c:func:`Py_FinalizeEx` sẽ tắt trình thông dịch, rồi chương trình kết thúc. Trong một chương trình thực tế, bạn có thể muốn lấy tập lệnh Python từ một nguồn khác, chẳng hạn như một routine của trình soạn thảo văn bản, một tệp hoặc một cơ sở dữ liệu. Việc lấy mã Python từ một tệp có thể được thực hiện tốt hơn bằng cách sử dụng hàm :c:func:`PyRun_SimpleFile`, nhờ đó bạn không phải tự cấp phát bộ nhớ và tải nội dung tệp.


.. _lower-level-embedding:

Vượt ra ngoài Nhúng ở Mức Rất Cao: Tổng quan
============================================

Giao diện cấp cao cho phép bạn thực thi các đoạn mã Python tùy ý từ ứng dụng của mình, nhưng việc trao đổi các giá trị dữ liệu phải nói là khá cồng kềnh. Nếu muốn làm điều đó, bạn nên sử dụng các lời gọi cấp thấp hơn. Đổi lại, bạn phải viết nhiều mã C hơn, nhưng có thể thực hiện gần như mọi việc.

Cần lưu ý rằng việc mở rộng Python và nhúng Python thực chất là cùng một hoạt động, dù mục đích khác nhau. Hầu hết các chủ đề được thảo luận trong những chương trước vẫn còn nguyên giá trị. Để thấy rõ điều này, hãy xem mã mở rộng từ Python sang C thực sự làm gì:

#. Chuyển đổi các giá trị dữ liệu từ Python sang C,

#. Thực hiện lời gọi hàm đến một routine C bằng các giá trị đã chuyển đổi, rồi

#. Chuyển đổi các giá trị dữ liệu từ lời gọi từ C sang Python.

Khi nhúng Python, mã giao diện sẽ:

#. Chuyển đổi các giá trị dữ liệu từ C sang Python,

#. Thực hiện lời gọi hàm đến một routine giao diện Python bằng các giá trị đã chuyển đổi, và

#. Chuyển đổi các giá trị dữ liệu từ lời gọi đó từ Python sang C.

Như bạn có thể thấy, các bước chuyển đổi dữ liệu chỉ đơn giản là được hoán đổi để phù hợp với hướng khác nhau của việc truyền dữ liệu giữa các ngôn ngữ. Điểm khác biệt duy nhất là routine được gọi giữa hai lần chuyển đổi dữ liệu. Khi mở rộng, bạn gọi một routine C; khi nhúng, bạn gọi một routine Python.

Chương này sẽ không trình bày cách chuyển đổi dữ liệu từ Python sang C và ngược lại. Ngoài ra, giả định rằng bạn đã hiểu cách sử dụng tham chiếu đúng cách và xử lý lỗi. Vì các khía cạnh này không khác với việc mở rộng interpreter, bạn có thể tham khảo các chương trước để biết thông tin cần thiết.


.. _pure-embedding:

Nhúng thuần túy
===============

Chương trình đầu tiên nhằm thực thi một hàm trong một script Python. Tương tự như trong phần về interface cấp độ rất cao, interpreter Python không tương tác trực tiếp với ứng dụng (nhưng điều đó sẽ thay đổi trong phần tiếp theo).

Mã để chạy một hàm được định nghĩa trong một script Python là:

.. literalinclude:: ../includes/run-func.c


Mã này tải một script Python bằng ``argv[1]`` và gọi hàm có tên được chỉ định trong ``argv[2]``. Các đối số số nguyên của hàm là những giá trị còn lại trong mảng ``argv``. Nếu bạn :ref:`biên dịch và liên kết <compiling>` chương trình này (hãy gọi tệp thực thi hoàn chỉnh là :program:`call`) rồi dùng nó để thực thi một script Python, chẳng hạn như:

.. code-block:: python

   def multiply(a,b):
       print("Will compute", a, "times", b)
       c = 0
       for i in range(0, a):
           c = c + b
       return c

thì kết quả sẽ là:

.. code-block:: shell-session

   $ call multiply multiply 3 2
   Will compute 3 times 2
   Result of call: 6

Mặc dù chương trình khá lớn so với chức năng của nó, phần lớn mã dùng để chuyển đổi dữ liệu giữa Python và C, cũng như báo cáo lỗi. Phần thú vị liên quan đến việc nhúng Python bắt đầu từ::

   Py_Initialize();
   pName = PyUnicode_DecodeFSDefault(argv[1]);
   /* Bỏ qua việc kiểm tra lỗi của pName */
   pModule = PyImport_Import(pName);

Sau khi khởi tạo interpreter, script được tải bằng
:c:func:`PyImport_Import`. Hàm này cần một chuỗi Python làm đối số, được tạo bằng routine chuyển đổi dữ liệu :c:func:`PyUnicode_DecodeFSDefault`.::

   pFunc = PyObject_GetAttrString(pModule, argv[2]);
   /* pFunc là một tham chiếu mới */

   if (pFunc && PyCallable_Check(pFunc)) {
       ...
   }
   Py_XDECREF(pFunc);

Sau khi script được tải, tên mà chúng ta đang tìm kiếm được lấy bằng
:c:func:`PyObject_GetAttrString`. Nếu tên này tồn tại và đối tượng được trả về có thể gọi được, bạn có thể an tâm giả định rằng đó là một hàm. Sau đó, chương trình tiếp tục tạo một tuple các đối số như bình thường. Tiếp theo, hàm Python được gọi với::

   pValue = PyObject_CallObject(pFunc, pArgs);

Khi hàm trả về, ``pValue`` либо là ``NULL`` hoặc chứa một tham chiếu đến giá trị trả về của hàm. Hãy nhớ giải phóng tham chiếu sau khi kiểm tra giá trị.


.. _extending-with-embedding:

Mở rộng Python được nhúng
=========================

Cho đến lúc này, trình thông dịch Python được nhúng chưa có quyền truy cập vào các chức năng của chính ứng dụng. Python API cho phép thực hiện điều này bằng cách mở rộng trình thông dịch được nhúng. Nghĩa là, trình thông dịch được nhúng được mở rộng bằng các thủ tục do ứng dụng cung cấp. Mặc dù nghe có vẻ phức tạp, nhưng thực ra không quá khó. Tạm thời hãy quên rằng ứng dụng khởi động trình thông dịch Python. Thay vào đó, hãy xem ứng dụng như một tập hợp các thủ tục con và viết một đoạn glue code để Python có thể truy cập các thủ tục đó, giống như khi bạn viết một Python extension thông thường. Ví dụ::

   static int numargs=0;

   /* Trả về số đối số của dòng lệnh ứng dụng */
   static PyObject*
   emb_numargs(PyObject *self, PyObject *args)
   {
       if(!PyArg_ParseTuple(args, ":numargs"))
           return NULL;
       return PyLong_FromLong(numargs);
   }

   static PyMethodDef emb_module_methods[] = {
       {"numargs", emb_numargs, METH_VARARGS,
        "Return the number of arguments received by the process."},
       {NULL, NULL, 0, NULL}
   };

   static struct PyModuleDef emb_module = {
       .m_base = PyModuleDef_HEAD_INIT,
       .m_name = "emb",
       .m_size = 0,
       .m_methods = emb_module_methods,
   };

   static PyObject*
   PyInit_emb(void)
   {
       return PyModuleDef_Init(&emb_module);
   }

Chèn đoạn mã trên ngay phía trên hàm :c:func:`main`. Đồng thời, chèn hai câu lệnh sau trước lệnh gọi đến :c:func:`Py_Initialize`::

   numargs = argc;
   PyImport_AppendInittab("emb", &PyInit_emb);

Hai dòng này khởi tạo biến ``numargs`` và làm cho
hàm :func:`!emb.numargs` có thể được trình thông dịch Python được nhúng truy cập. Với các phần mở rộng này, tập lệnh Python có thể thực hiện những việc như

.. code-block:: python

   import emb
   print("Number of arguments", emb.numargs())

Trong một ứng dụng thực tế, các method sẽ cung cấp cho Python một API của ứng dụng.

.. TODO: threads, code examples do not really behave well if errors happen
   (what to watch out for)


.. _embeddingincplusplus:

Nhúng Python vào C++
====================

Bạn cũng có thể nhúng Python vào một chương trình C++; cách thực hiện chính xác sẽ phụ thuộc vào chi tiết của hệ thống C++ được sử dụng; nhìn chung, bạn sẽ cần viết chương trình chính bằng C++ và sử dụng trình biên dịch C++ để biên dịch và liên kết chương trình. Bạn không cần biên dịch lại bản thân Python bằng C++.


.. _compiling:

Biên dịch và liên kết trên các hệ thống Unix-like
=================================================

Không phải lúc nào cũng dễ dàng tìm được các cờ thích hợp để truyền cho trình biên dịch (và linker) nhằm nhúng trình thông dịch Python vào ứng dụng của bạn, đặc biệt vì Python cần tải các module thư viện được triển khai dưới dạng phần mở rộng động C (:file:`.so` files) được liên kết với nó.

Để tìm các cờ cần thiết cho trình biên dịch và linker, bạn có thể thực thi
:file:`python{X.Y}-config` script được tạo trong quá trình cài đặt (một :file:`python3-config` script cũng có thể khả dụng). Script này có một số tùy chọn, trong đó các tùy chọn sau sẽ hữu ích trực tiếp cho bạn:

* ``pythonX.Y-config --cflags`` sẽ cung cấp cho bạn các cờ được khuyến nghị khi biên dịch:

  .. code-block:: shell-session

     $ /opt/bin/python3.11-config --cflags
     -I/opt/include/python3.11 -I/opt/include/python3.11 -Wsign-compare  -DNDEBUG -g -fwrapv -O3 -Wall

* ``pythonX.Y-config --ldflags --embed`` sẽ cung cấp cho bạn các cờ được khuyến nghị khi liên kết:

  .. code-block:: shell-session

     $ /opt/bin/python3.11-config --ldflags --embed
     -L/opt/lib/python3.11/config-3.11-x86_64-linux-gnu -L/opt/lib -lpython3.11 -lpthread -ldl  -lutil -lm

.. note::
   Để tránh nhầm lẫn giữa nhiều bản cài đặt Python (đặc biệt là giữa Python của hệ thống và Python do bạn tự biên dịch), bạn nên sử dụng đường dẫn tuyệt đối đến :file:`python{X.Y}-config`, như trong ví dụ trên.

Nếu quy trình này không hiệu quả với bạn (quy trình này không được đảm bảo hoạt động trên tất cả các nền tảng kiểu Unix; tuy nhiên, chúng tôi hoan nghênh :ref:`báo cáo lỗi <reporting-bugs>`), bạn sẽ phải đọc tài liệu của hệ thống về liên kết động và/hoặc kiểm tra :file:`Makefile` của Python (dùng :func:`sysconfig.get_makefile_filename` để tìm vị trí của tệp) và các tùy chọn biên dịch. Trong trường hợp này, mô-đun :mod:`sysconfig` là một công cụ hữu ích để trích xuất theo cách lập trình các giá trị cấu hình mà bạn sẽ muốn kết hợp với nhau. Ví dụ:

.. code-block:: pycon

   >>> import sysconfig
   >>> sysconfig.get_config_var('LIBS')
   '-lpthread -ldl  -lutil'
   >>> sysconfig.get_config_var('LINKFORSHARED')
   '-Xlinker -export-dynamic'


.. XXX similar documentation for Windows missing
