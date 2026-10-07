.. highlight:: c

.. _freethreading-extensions-howto:

*****************************************
Hỗ trợ extension C API cho Free Threading
*****************************************

Bắt đầu từ bản phát hành 3.13, CPython hỗ trợ chạy với :term:`global interpreter lock` (GIL) bị vô hiệu hóa trong một cấu hình có tên :term:`free threading`. Tài liệu này mô tả cách điều chỉnh các extension C API để hỗ trợ free threading.


Xác định bản build Free-Threaded trong C
========================================

C API của CPython cung cấp macro ``Py_GIL_DISABLED``: trong bản build free-threaded, macro này được định nghĩa là ``1``, còn trong bản build thông thường thì không được định nghĩa. Bạn có thể dùng macro này để bật mã chỉ chạy trong bản build free-threaded::

    #ifdef Py_GIL_DISABLED
    /* code that only runs in the free-threaded build */
    #endif

.. note::

   Trên Windows, macro này không được tự động định nghĩa mà phải được chỉ định cho trình biên dịch khi build. Có thể dùng hàm :func:`sysconfig.get_config_var` để xác định interpreter đang chạy hiện tại có được định nghĩa macro này hay không.


Khởi tạo module
===============

Các module mở rộng cần chỉ rõ rằng chúng hỗ trợ chạy khi GIL bị vô hiệu hóa; nếu không, việc nhập module mở rộng sẽ phát sinh cảnh báo và bật GIL trong runtime.

Có hai cách để chỉ rõ rằng một module mở rộng hỗ trợ chạy khi GIL bị vô hiệu hóa, tùy thuộc vào việc module mở rộng đó sử dụng cơ chế khởi tạo nhiều giai đoạn hay một giai đoạn.

Khởi tạo nhiều giai đoạn
........................

Các module mở rộng sử dụng cơ chế khởi tạo nhiều giai đoạn (tức là
:c:func:`PyModuleDef_Init`) nên thêm một slot :c:data:`Py_mod_gil` vào định nghĩa module. Nếu module mở rộng của bạn hỗ trợ các phiên bản CPython cũ hơn, bạn nên bảo vệ slot này bằng kiểm tra :c:data:`PY_VERSION_HEX`.

::

    static struct PyModuleDef_Slot module_slots[] = {
        ...
    #if PY_VERSION_HEX >= 0x030D0000
        {Py_mod_gil, Py_MOD_GIL_NOT_USED},
    #endif
        {0, NULL}
    };

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        .m_slots = module_slots,
        ...
    };


Khởi tạo một pha
................

Các extension sử dụng khởi tạo một pha (tức là,
:c:func:`PyModule_Create`) nên gọi :c:func:`PyUnstable_Module_SetGIL` để cho biết rằng chúng hỗ trợ chạy khi GIL bị vô hiệu hóa. Hàm này chỉ được định nghĩa trong bản build free-threaded, vì vậy bạn nên bảo vệ lệnh gọi bằng ``#ifdef Py_GIL_DISABLED`` để tránh lỗi biên dịch trong bản build thông thường.

::

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        ...
    };

    PyMODINIT_FUNC
    PyInit_mymodule(void)
    {
        PyObject *m = PyModule_Create(&moduledef);
        if (m == NULL) {
            return NULL;
        }
    #ifdef Py_GIL_DISABLED
        PyUnstable_Module_SetGIL(m, Py_MOD_GIL_NOT_USED);
    #endif
        return m;
    }


Hướng dẫn chung về API
======================

Phần lớn C API an toàn với luồng, nhưng có một số ngoại lệ.

* **Trường của struct**: Việc truy cập trực tiếp vào các trường trong các đối tượng hoặc struct của Python C API không an toàn với luồng nếu trường đó có thể bị sửa đổi đồng thời.
* **Macro**: Các macro accessor như :c:macro:`PyList_GET_ITEM`,
  :c:macro:`PyList_SET_ITEM`, và các macro như
  :c:macro:`PySequence_Fast_GET_SIZE` sử dụng đối tượng được trả về bởi
  :c:func:`PySequence_Fast` không thực hiện bất kỳ thao tác kiểm tra lỗi hoặc khóa nào. Các macro này không an toàn với luồng nếu đối tượng container có thể bị sửa đổi đồng thời.
* **Tham chiếu mượn**: Các hàm C API trả về
  :term:`borrowed references <borrowed reference>` có thể không an toàn với thread nếu đối tượng chứa chúng bị sửa đổi đồng thời. Xem phần
  :ref:`borrowed references <borrowed-references>` để biết thêm thông tin.


Tính an toàn với thread của container
.....................................

Các container như :c:struct:`PyListObject`,
:c:struct:`PyDictObject`, và :c:struct:`PySetObject` thực hiện khóa nội bộ trong bản dựng free-threaded. Ví dụ, :c:func:`PyList_Append` sẽ khóa list trước khi thêm một mục.

.. _PyDict_Next:

``PyDict_Next``
'''''''''''''''

Một ngoại lệ đáng chú ý là :c:func:`PyDict_Next`, vốn không khóa dictionary. Bạn nên dùng :c:macro:`Py_BEGIN_CRITICAL_SECTION` để bảo vệ dictionary khi lặp qua nó nếu dictionary có thể bị sửa đổi đồng thời::

    Py_BEGIN_CRITICAL_SECTION(dict);
    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while (PyDict_Next(dict, &pos, &key, &value)) {
        ...
    }
    Py_END_CRITICAL_SECTION();


Các tham chiếu mượn
===================

.. _borrowed-references:

Một số hàm C API trả về :term:`tham chiếu mượn <borrowed reference>`. Các API này không an toàn với thread nếu đối tượng chứa chúng bị sửa đổi đồng thời. Ví dụ, không an toàn khi sử dụng :c:func:`PyList_GetItem` nếu danh sách có thể bị sửa đổi đồng thời.

Bảng sau liệt kê một số API tham chiếu mượn và các API thay thế trả về :term:`tham chiếu mạnh <strong reference>`.

+-----------------------------------+-----------------------------------+
| API tham chiếu mượn               | API tham chiếu mạnh               |
+===================================+===================================+
| :c:func:`PyList_GetItem`          | :c:func:`PyList_GetItemRef`       |
+-----------------------------------+-----------------------------------+
| :c:func:`PyList_GET_ITEM`         | :c:func:`PyList_GetItemRef`       |
+-----------------------------------+-----------------------------------+
| :c:func:`PyDict_GetItem`          | :c:func:`PyDict_GetItemRef`       |
+-----------------------------------+-----------------------------------+
| :c:func:`PyDict_GetItemWithError` | :c:func:`PyDict_GetItemRef`       |
+-----------------------------------+-----------------------------------+
| :c:func:`PyDict_GetItemString`    | :c:func:`PyDict_GetItemStringRef` |
+-----------------------------------+-----------------------------------+
| :c:func:`PyDict_SetDefault`       | :c:func:`PyDict_SetDefaultRef`    |
+-----------------------------------+-----------------------------------+
| :c:func:`PyDict_Next`             | không có (xem :ref:`PyDict_Next`) |
+-----------------------------------+-----------------------------------+
| :c:func:`PyWeakref_GetObject`     | :c:func:`PyWeakref_GetRef`        |
+-----------------------------------+-----------------------------------+
| :c:func:`PyWeakref_GET_OBJECT`    | :c:func:`PyWeakref_GetRef`        |
+-----------------------------------+-----------------------------------+
| :c:func:`PyImport_AddModule`      | :c:func:`PyImport_AddModuleRef`   |
+-----------------------------------+-----------------------------------+
| :c:func:`PyCell_GET`              | :c:func:`PyCell_Get`              |
+-----------------------------------+-----------------------------------+

Không phải tất cả API trả về tham chiếu mượn đều có vấn đề. Ví dụ, :c:func:`PyTuple_GetItem` an toàn vì tuple là bất biến. Tương tự, không phải mọi cách sử dụng các API trên đều có vấn đề. Ví dụ,
:c:func:`PyDict_GetItem` thường được sử dụng để phân tích các dictionary đối số từ khóa trong lời gọi hàm; những dictionary đối số từ khóa đó về cơ bản là riêng tư (không thể truy cập bởi các thread khác), vì vậy việc sử dụng tham chiếu mượn trong ngữ cảnh này là an toàn.

Một số hàm này được thêm vào Python 3.13. Bạn có thể sử dụng package `pythoncapi-compat <https://github.com/python/pythoncapi-compat>`_ để cung cấp các triển khai của những hàm này cho các phiên bản Python cũ hơn.


.. _free-threaded-memory-allocation:

API cấp phát bộ nhớ
===================

C API quản lý bộ nhớ của Python cung cấp các hàm trong ba
:ref:`miền cấp phát <allocator-domains>`: "raw", "mem" và "object". Để đảm bảo an toàn cho thread, bản build free-threaded yêu cầu chỉ các đối tượng Python mới được cấp phát bằng miền object và mọi đối tượng Python đều phải được cấp phát bằng miền đó. Điều này khác với các phiên bản Python trước đây, trong đó đây chỉ là một phương pháp tốt nhất chứ không phải yêu cầu bắt buộc.

.. note::

   Tìm các trường hợp sử dụng :c:func:`PyObject_Malloc` trong extension của bạn và kiểm tra để đảm bảo bộ nhớ được cấp phát được dùng cho các đối tượng Python. Hãy sử dụng :c:func:`PyMem_Malloc` để cấp phát các buffer thay vì
   :c:func:`PyObject_Malloc`.


API trạng thái thread và GIL
============================

Python cung cấp một tập hợp các hàm và macro để quản lý trạng thái thread và GIL, chẳng hạn như:

* :c:func:`PyGILState_Ensure` và :c:func:`PyGILState_Release`
* :c:func:`PyEval_SaveThread` và :c:func:`PyEval_RestoreThread`
* :c:macro:`Py_BEGIN_ALLOW_THREADS` và :c:macro:`Py_END_ALLOW_THREADS`

Các hàm này vẫn nên được sử dụng trong bản dựng free-threaded để quản lý trạng thái luồng ngay cả khi :term:`GIL` bị vô hiệu hóa. Ví dụ: nếu bạn tạo một luồng bên ngoài Python, bạn phải gọi :c:func:`PyGILState_Ensure` trước khi gọi Python API để đảm bảo luồng đó có trạng thái luồng Python hợp lệ.

Bạn vẫn nên gọi :c:func:`PyEval_SaveThread` hoặc
:c:macro:`Py_BEGIN_ALLOW_THREADS` xung quanh các thao tác chặn, chẳng hạn như I/O hoặc nhận khóa, để cho phép các luồng khác chạy
:term:`bộ thu gom rác theo chu kỳ <garbage collection>`.


Bảo vệ trạng thái nội bộ của extension
======================================

Extension của bạn có thể có trạng thái nội bộ trước đây được GIL bảo vệ. Bạn có thể cần thêm cơ chế khóa để bảo vệ trạng thái này. Cách tiếp cận sẽ phụ thuộc vào extension của bạn, nhưng một số mẫu thường gặp gồm:

* **Bộ nhớ đệm**: bộ nhớ đệm toàn cục là một nguồn phổ biến của trạng thái dùng chung. Hãy cân nhắc sử dụng một khóa để bảo vệ bộ nhớ đệm hoặc tắt bộ nhớ đệm này trong bản dựng free-threaded nếu bộ nhớ đệm không quan trọng đối với hiệu năng.
* **Trạng thái toàn cục**: trạng thái toàn cục có thể cần được bảo vệ bằng một khóa hoặc chuyển sang bộ nhớ lưu trữ cục bộ theo luồng. C11 và C++11 cung cấp ``thread_local`` hoặc ``_Thread_local`` cho `bộ nhớ lưu trữ cục bộ theo luồng <https://en.cppreference.com/w/c/language/storage_duration>`_.


Vùng tới hạn
============

.. _critical-sections:

Trong bản dựng free-threaded, CPython cung cấp một cơ chế có tên là "vùng tới hạn" để bảo vệ dữ liệu mà nếu không sẽ được GIL bảo vệ. Mặc dù các tác giả extension có thể không tương tác trực tiếp với phần triển khai vùng tới hạn nội bộ, việc hiểu rõ hành vi của chúng là rất quan trọng khi sử dụng một số hàm C API hoặc quản lý trạng thái dùng chung trong bản dựng free-threaded.

Vùng tới hạn là gì?
...................

Về mặt khái niệm, critical section hoạt động như một lớp tránh deadlock được xây dựng bên trên các mutex đơn giản. Mỗi thread duy trì một stack gồm các critical section đang hoạt động. Khi một thread cần lấy lock liên kết với một critical section (ví dụ: ngầm định khi gọi một hàm C API an toàn cho thread như
:c:func:`PyDict_SetItem`, hoặc tường minh bằng cách sử dụng macro), nó sẽ cố gắng lấy mutex nền tảng.

Sử dụng Critical Sections
.........................

Các API chính để sử dụng critical section là:

* :c:macro:`Py_BEGIN_CRITICAL_SECTION` và :c:macro:`Py_END_CRITICAL_SECTION` - Dùng để khóa một đối tượng duy nhất

* :c:macro:`Py_BEGIN_CRITICAL_SECTION2` và :c:macro:`Py_END_CRITICAL_SECTION2`
  - Dùng để khóa đồng thời hai đối tượng

Các macro này phải được sử dụng theo từng cặp tương ứng và phải xuất hiện trong cùng một phạm vi C, vì chúng thiết lập một phạm vi cục bộ mới. Các macro này không thực hiện thao tác nào trong các bản build không có free-threading, vì vậy có thể thêm chúng một cách an toàn vào mã cần hỗ trợ cả hai kiểu build.

Một trường hợp sử dụng phổ biến của critical section là khóa một đối tượng khi truy cập một thuộc tính nội bộ của đối tượng đó. Ví dụ: nếu một kiểu extension có trường count nội bộ, bạn có thể sử dụng critical section khi đọc hoặc ghi trường đó::

    // Đọc giá trị đếm, trả về một tham chiếu mới đến giá trị đếm nội bộ
    PyObject *result;
    Py_BEGIN_CRITICAL_SECTION(obj);
    result = Py_NewRef(obj->count);
    Py_END_CRITICAL_SECTION();
    return result;

    // Ghi giá trị đếm, tiêu thụ tham chiếu từ new_count
    Py_BEGIN_CRITICAL_SECTION(obj);
    obj->count = new_count;
    Py_END_CRITICAL_SECTION();


Cách Critical Section hoạt động
...............................

Không giống như các lock truyền thống, critical section không đảm bảo quyền truy cập độc quyền trong toàn bộ thời gian tồn tại của chúng. Nếu một thread bị chặn trong khi đang giữ critical section (ví dụ: khi lấy một lock khác hoặc thực hiện I/O), critical section sẽ tạm thời bị đình chỉ—tất cả lock được giải phóng—sau đó được tiếp tục khi thao tác gây chặn hoàn tất.

Hành vi này tương tự như những gì xảy ra với GIL khi một thread thực hiện một lời gọi gây chặn. Các điểm khác biệt chính là:

* Critical section hoạt động trên cơ sở từng đối tượng thay vì trên phạm vi toàn cục

* Critical section tuân theo kỷ luật ngăn xếp trong mỗi thread (các macro "begin" và "end" thực thi điều này vì chúng phải đi theo từng cặp và nằm trong cùng một phạm vi)

* Các vùng tới hạn tự động nhả và giành lại các khóa xung quanh những thao tác có khả năng bị chặn

Tránh deadlock
..............

Các vùng tới hạn giúp tránh deadlock theo hai cách:

1. Nếu một thread cố gắng giành một khóa đang được thread khác giữ, trước tiên nó sẽ tạm dừng tất cả các vùng tới hạn đang hoạt động và tạm thời nhả các khóa của chúng

2. Khi thao tác bị chặn hoàn tất, chỉ vùng tới hạn ngoài cùng mới được giành lại trước tiên

Điều này có nghĩa là bạn không thể dựa vào các vùng tới hạn lồng nhau để khóa nhiều đối tượng cùng lúc, vì vùng tới hạn bên trong có thể tạm dừng các vùng bên ngoài. Thay vào đó, hãy sử dụng
:c:macro:`Py_BEGIN_CRITICAL_SECTION2` để khóa đồng thời hai đối tượng.

Lưu ý rằng các lock được mô tả ở trên chỉ là các lock dựa trên :c:type:`PyMutex`. Việc triển khai critical section không biết đến hoặc không ảnh hưởng đến các cơ chế locking khác có thể đang được sử dụng, chẳng hạn như mutex POSIX. Cũng lưu ý rằng mặc dù việc blocking trên bất kỳ :c:type:`PyMutex` nào cũng khiến các critical section bị tạm ngưng, chỉ những mutex thuộc các critical section mới được giải phóng. Nếu sử dụng :c:type:`PyMutex` mà không có critical section, nó sẽ không được giải phóng và do đó không có cơ chế tránh deadlock tương tự.

Các lưu ý quan trọng
....................

* Các critical section có thể tạm thời giải phóng lock, cho phép các thread khác sửa đổi dữ liệu được bảo vệ. Hãy cẩn thận khi đưa ra giả định về trạng thái của dữ liệu sau các thao tác có thể bị blocking.

* Vì các lock có thể tạm thời được giải phóng (bị tạm ngưng), việc đi vào một critical section không đảm bảo quyền truy cập độc quyền vào tài nguyên được bảo vệ trong suốt thời gian của section đó. Nếu code bên trong một critical section gọi một hàm khác bị blocking (ví dụ: lấy một lock khác hoặc thực hiện I/O blocking), tất cả lock mà thread đang giữ thông qua các critical section sẽ được giải phóng. Điều này tương tự cách GIL có thể được giải phóng trong các lệnh gọi blocking.

* Tại mỗi thời điểm, chỉ các lock liên kết với critical section vừa được đi vào gần đây nhất (critical section trên cùng) mới được đảm bảo là đang được giữ. Các lock của những critical section lồng nhau ở bên ngoài có thể đã bị tạm ngưng.

* Bạn chỉ có thể lock tối đa hai đối tượng đồng thời bằng các API này. Nếu cần lock nhiều đối tượng hơn, bạn sẽ phải cấu trúc lại code.

* Mặc dù các critical section sẽ không xảy ra deadlock nếu bạn cố lock cùng một đối tượng hai lần, chúng kém hiệu quả hơn các reentrant lock được thiết kế riêng cho trường hợp sử dụng này.

* Khi sử dụng :c:macro:`Py_BEGIN_CRITICAL_SECTION2`, thứ tự của các đối tượng không ảnh hưởng đến tính chính xác (bản triển khai xử lý việc tránh deadlock), nhưng bạn nên luôn khóa các đối tượng theo một thứ tự nhất quán.

* Hãy nhớ rằng các macro critical section chủ yếu dùng để bảo vệ quyền truy cập vào *các đối tượng Python* có thể tham gia vào các thao tác nội bộ của CPython dễ gặp các tình huống deadlock được mô tả ở trên. Để bảo vệ trạng thái hoàn toàn nội bộ của extension, mutex tiêu chuẩn hoặc các primitive đồng bộ hóa khác có thể phù hợp hơn.


Xây dựng Extension cho Bản dựng Free-Threaded
=============================================

Các extension C API cần được xây dựng riêng cho bản dựng free-threaded. Các wheel, thư viện dùng chung và tệp nhị phân được nhận diện bằng hậu tố ``t``.

* `pypa/manylinux <https://github.com/pypa/manylinux>`_ hỗ trợ bản dựng free-threaded với hậu tố ``t``, chẳng hạn như ``python3.14t``.
* `pypa/cibuildwheel <https://github.com/pypa/cibuildwheel>`_ hỗ trợ xây dựng wheel cho bản dựng free-threaded của Python 3.14 trở lên.

Limited C API và Stable ABI
...........................

Bản dựng free-threaded hiện chưa hỗ trợ
:ref:`Limited C API <limited-c-api>` hoặc stable ABI. Nếu bạn sử dụng `setuptools <https://setuptools.pypa.io/en/latest/setuptools.html>`_ để build extension và hiện đang đặt ``py_limited_api=True`` bạn có thể sử dụng ``py_limited_api=not sysconfig.get_config_var("Py_GIL_DISABLED")`` để không dùng limited API khi build bằng bản dựng free-threaded.

.. note::
    Bạn sẽ cần build các wheel riêng dành riêng cho bản dựng free-threaded. Nếu hiện đang sử dụng stable ABI, bạn có thể tiếp tục build một wheel duy nhất cho nhiều phiên bản Python không phải free-threaded.


Windows
.......

Do một hạn chế của trình cài đặt Windows chính thức, bạn sẽ cần tự định nghĩa ``Py_GIL_DISABLED=1`` khi build extension từ mã nguồn.

.. seealso::

   `Porting Extension Modules to Support Free-Threading <https://py-free-threading.github.io/porting/>`_: Hướng dẫn chuyển đổi do cộng đồng duy trì dành cho tác giả extension.

.. _`pythoncapi-compat`: https://github.com/python/pythoncapi-compat
.. _`thread-local storage`: https://en.cppreference.com/w/c/language/storage_duration
.. _`pypa/manylinux`: https://github.com/pypa/manylinux
.. _`pypa/cibuildwheel`: https://github.com/pypa/cibuildwheel
.. _`setuptools`: https://setuptools.pypa.io/en/latest/setuptools.html
.. _`Porting Extension Modules to Support Free-Threading`: https://py-free-threading.github.io/porting/
