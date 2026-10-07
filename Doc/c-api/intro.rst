.. highlight:: c


.. _api-intro:

**********
Giới thiệu
**********

Application Programmer's Interface của Python cho phép các lập trình viên C và C++ truy cập trình thông dịch Python ở nhiều cấp độ khác nhau. API này cũng có thể được sử dụng hiệu quả từ C++, nhưng để ngắn gọn, nó thường được gọi là Python/C API. Có hai lý do hoàn toàn khác nhau để sử dụng Python/C API. Lý do đầu tiên là viết các *mô-đun mở rộng* cho những mục đích cụ thể; đây là các mô-đun C mở rộng trình thông dịch Python. Đây có lẽ là cách sử dụng phổ biến nhất. Lý do thứ hai là sử dụng Python như một thành phần trong một ứng dụng lớn hơn; kỹ thuật này thường được gọi là :dfn:`nhúng` Python vào một ứng dụng.

Việc viết một mô-đun mở rộng là một quy trình tương đối dễ hiểu, trong đó cách tiếp cận theo kiểu "cookbook" hoạt động khá hiệu quả. Có một số công cụ tự động hóa quy trình này ở một mức độ nhất định. Mặc dù mọi người đã nhúng Python vào các ứng dụng khác kể từ những ngày đầu của Python, quy trình nhúng Python kém đơn giản hơn so với việc viết một phần mở rộng.

Nhiều hàm API hữu ích независимо với việc bạn đang nhúng hay mở rộng Python; hơn nữa, hầu hết các ứng dụng nhúng Python cũng sẽ cần cung cấp một phần mở rộng tùy chỉnh, vì vậy có lẽ bạn nên làm quen với việc viết một phần mở rộng trước khi cố gắng nhúng Python vào một ứng dụng thực tế.


Khả năng tương thích với phiên bản ngôn ngữ
===========================================

C API của Python tương thích với các phiên bản C11 và C++11 của C và C++.

Đây là giới hạn thấp hơn: C API không yêu cầu các tính năng từ những phiên bản C/C++ mới hơn. Bạn *không* cần bật "c11 mode" của trình biên dịch.


Tiêu chuẩn viết mã
==================

Nếu bạn viết mã C để đưa vào CPython, bạn **phải** tuân theo các hướng dẫn và tiêu chuẩn được định nghĩa trong :PEP:`7`. Các hướng dẫn này được áp dụng bất kể phiên bản Python mà bạn đang đóng góp. Việc tuân theo các quy ước này không bắt buộc đối với các mô-đun mở rộng của bên thứ ba do bạn tự viết, trừ khi cuối cùng bạn dự định đóng góp chúng cho Python.


.. _api-includes:

Các tệp Include
===============

Tất cả định nghĩa hàm, kiểu và macro cần thiết để sử dụng Python/C API được đưa vào mã của bạn bằng dòng sau::

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

Điều này ngầm bao gồm các header tiêu chuẩn sau: ``<stdio.h>``, ``<string.h>``, ``<errno.h>``, ``<limits.h>``, ``<assert.h>`` và ``<stdlib.h>`` (nếu có).

.. note::

   Vì Python có thể định nghĩa một số macro tiền xử lý ảnh hưởng đến các header chuẩn trên một số hệ thống, bạn *phải* include :file:`Python.h` trước khi include bất kỳ header chuẩn nào.

   Khuyến nghị luôn định nghĩa ``PY_SSIZE_T_CLEAN`` trước khi include ``Python.h``. Xem :ref:`arg-parsing` để biết mô tả về macro này.

Tất cả tên hiển thị với người dùng được định nghĩa bởi Python.h (ngoại trừ những tên được định nghĩa bởi các header chuẩn được include) đều có một trong các tiền tố ``Py`` hoặc ``_Py``. Các tên bắt đầu bằng ``_Py`` dành cho mục đích nội bộ của triển khai Python và người viết extension không nên sử dụng chúng. Tên thành viên của cấu trúc không có tiền tố dành riêng.

.. note::

   Mã do người dùng viết không bao giờ nên định nghĩa các tên bắt đầu bằng ``Py`` hoặc ``_Py``. Điều này khiến người đọc nhầm lẫn và đe dọa tính khả chuyển của mã người dùng sang các phiên bản Python trong tương lai, vốn có thể định nghĩa thêm các tên bắt đầu bằng một trong những tiền tố này.

Các tệp header thường được cài đặt cùng với Python. Trên Unix, chúng nằm trong các thư mục :file:`{prefix}/include/pythonversion/` và
:file:`{exec_prefix}/include/pythonversion/`, trong đó :option:`prefix <--prefix>` và
:option:`exec_prefix <--exec-prefix>` được định nghĩa bởi các tham số tương ứng của Python's
:program:`configure` script và *version* là ``'%d.%d' % sys.version_info[:2]``. Trên Windows, các tệp header được cài đặt trong :file:`{prefix}/include`, trong đó ``prefix`` là thư mục cài đặt được chỉ định cho trình cài đặt.

Để include các tệp header, hãy đặt cả hai thư mục (nếu khác nhau) vào đường dẫn tìm kiếm include của compiler. *not* đặt các thư mục cha vào đường dẫn tìm kiếm rồi sử dụng ``#include <pythonX.Y/Python.h>``; cách này sẽ gây lỗi khi build đa nền tảng vì các tệp header độc lập với nền tảng nằm dưới
:option:`prefix <--prefix>` include các tệp header dành riêng cho nền tảng từ
:option:`exec_prefix <--exec-prefix>`.

Người dùng C++ cần lưu ý rằng mặc dù API được định nghĩa hoàn toàn bằng C, các tệp header vẫn khai báo đúng các entry point là ``extern "C"``. Do đó, không cần thực hiện thao tác đặc biệt nào để sử dụng API từ C++.


Các macro hữu ích
=================

Một số macro hữu ích được định nghĩa trong các tệp header của Python. Nhiều macro được định nghĩa gần nơi chúng được sử dụng (ví dụ: :c:macro:`Py_RETURN_NONE`,
:c:macro:`PyMODINIT_FUNC`). Những macro khác có tính tiện dụng tổng quát hơn được định nghĩa ở đây. Danh sách này không nhất thiết phải đầy đủ.

.. c:macro:: Py_CAN_START_THREADS

   Nếu macro này được định nghĩa, hệ thống hiện tại có thể khởi chạy các thread.

   Hiện tại, tất cả các hệ thống được CPython hỗ trợ (theo :pep:`11`), ngoại trừ một số nền tảng WebAssembly, đều hỗ trợ khởi chạy các thread.

   .. versionadded:: 3.13

.. c:macro:: Py_GETENV(s)

   Tương tự :samp:`getenv({s})`, nhưng trả về ``NULL`` nếu :option:`-E` được truyền trên dòng lệnh (xem :c:member:`PyConfig.use_environment`).


Macro docstring
---------------

.. c:macro:: PyDoc_STRVAR(name, str)

   Tạo một biến có tên *name* có thể được sử dụng trong docstring. Nếu Python được build mà không có docstring (:option:`--without-doc-strings`), giá trị sẽ là một chuỗi rỗng.

   Ví dụ::

      PyDoc_STRVAR(pop_doc, "Remove and return the rightmost element.");

      static PyMethodDef deque_methods[] = {
          // ...
          {"pop", (PyCFunction)deque_pop, METH_NOARGS, pop_doc},
          // ...
      }

   Mở rộng thành :samp:`PyDoc_VAR({name}) = PyDoc_STR({str})`.

.. c:macro:: PyDoc_STR(str)

   Mở rộng thành chuỗi đầu vào đã cho hoặc một chuỗi rỗng nếu docstring bị vô hiệu hóa (:option:`--without-doc-strings`).

   Ví dụ::

      static PyMethodDef pysqlite_row_methods[] = {
          {"keys", (PyCFunction)pysqlite_row_keys, METH_NOARGS,
              PyDoc_STR("Returns the keys of the row.")},
          {NULL, NULL}
      };

.. c:macro:: PyDoc_VAR(name)

   Khai báo một biến mảng ký tự tĩnh với *name* đã cho. Mở rộng thành :samp:`static const char {name}[]`

   Ví dụ::

      PyDoc_VAR(python_doc) = PyDoc_STR(
         "A genus of constricting snakes in the Pythonidae family native "
         "to the tropics and subtropics of the Eastern Hemisphere.");


Macro tiện ích chung
--------------------

Các macro sau đây dùng cho những tác vụ phổ biến không dành riêng cho Python.

.. c:macro:: Py_UNUSED(arg)

   Dùng macro này cho các đối số không được sử dụng trong định nghĩa hàm để tắt cảnh báo của compiler. Ví dụ: ``int func(int a, int Py_UNUSED(b)) { return a; }``.

   .. versionadded:: 3.4

.. c:macro:: Py_GCC_ATTRIBUTE(name)

   Sử dụng thuộc tính GCC *name*, ẩn thuộc tính này khỏi các compiler không hỗ trợ thuộc tính GCC (chẳng hạn như MSVC).

   Trên compiler GCC, macro này mở rộng thành :samp:`__attribute__(({name)})`, còn trên các compiler không hỗ trợ thuộc tính GCC, macro này mở rộng thành chuỗi rỗng.


Tiện ích số
^^^^^^^^^^^

.. c:macro:: Py_ABS(x)

   Trả về giá trị tuyệt đối của ``x``.

   Đối số có thể được đánh giá nhiều hơn một lần. Do đó, không truyền trực tiếp vào macro này một biểu thức có side effect.

   Nếu không thể biểu diễn kết quả (ví dụ: nếu ``x`` có
   giá trị :c:macro:`!INT_MIN` cho kiểu :c:expr:`int`), hành vi là không xác định.

   Tương ứng gần đúng với :samp:`(({x}) < 0 ? -({x}) : ({x}))`

   .. versionadded:: 3.3

.. c:macro:: Py_MAX(x, y)
             Py_MIN(x, y)

   Lần lượt trả về giá trị lớn hơn hoặc nhỏ hơn trong các đối số.

   Mọi đối số có thể được đánh giá nhiều hơn một lần. Do đó, không truyền trực tiếp vào macro này một biểu thức có tác dụng phụ.

   :c:macro:`!Py_MAX` tương ứng gần đúng với
   :samp:`((({x}) > ({y})) ? ({x}) : ({y}))`.

   .. versionadded:: 3.3

.. c:macro:: Py_ARITHMETIC_RIGHT_SHIFT(type, integer, positions)

   Tương tự như :samp:`{integer} >> {positions}`, nhưng buộc mở rộng dấu, vì tiêu chuẩn C không quy định liệu phép dịch phải của một số nguyên có dấu có thực hiện mở rộng dấu hay điền bằng số 0 hay không.

   *số nguyên* phải là bất kỳ kiểu số nguyên có dấu nào. *vị trí* là số vị trí cần dịch sang phải.

   Cả *số nguyên* và *vị trí* đều có thể được đánh giá nhiều lần; do đó, tránh truyền trực tiếp một lệnh gọi hàm hoặc thao tác khác có tác dụng phụ vào macro này. Thay vào đó, hãy lưu kết quả vào một biến rồi truyền biến đó.

   *type* không được sử dụng và chỉ được giữ lại để tương thích ngược. Trước đây, *type* được dùng để ép kiểu *số nguyên*.

   .. versionchanged:: 3.1

      Macro này hiện hợp lệ với mọi kiểu số nguyên có dấu, không chỉ những kiểu mà ``unsigned type`` hợp lệ. Do đó, *type* không còn được sử dụng.

.. c:macro:: Py_CHARMASK(c)

   Đối số phải là một ký tự hoặc một số nguyên trong phạm vi [-128, 127] hoặc [0, 255]. Macro này trả về ``c`` được ép kiểu thành một ``unsigned char``.


Các tiện ích assertion
^^^^^^^^^^^^^^^^^^^^^^

.. c:macro:: Py_UNREACHABLE()

   Sử dụng khi bạn có một đường dẫn mã mà theo thiết kế không thể được thực thi. Ví dụ: trong mệnh đề ``default:`` của câu lệnh ``switch``, trong đó mọi giá trị có thể đều đã được bao phủ trong các câu lệnh ``case``. Sử dụng ở những nơi bạn có thể muốn đặt một lệnh gọi ``assert(0)`` hoặc ``abort()``.

   Ở chế độ release, macro này giúp compiler tối ưu hóa mã và tránh cảnh báo về mã không thể truy cập. Ví dụ, macro này được triển khai bằng ``__builtin_unreachable()`` trên GCC ở chế độ release.

   Trong chế độ debug và trên các compiler không được hỗ trợ, macro này được mở rộng thành một lời gọi đến
   :c:func:`Py_FatalError`.

   Một trường hợp sử dụng ``Py_UNREACHABLE()`` là sau lời gọi đến một hàm không bao giờ trả về nhưng không được khai báo là ``_Noreturn``.

   Nếu một đường dẫn mã rất khó xảy ra nhưng vẫn có thể được thực thi trong trường hợp ngoại lệ, không được sử dụng macro này. Ví dụ: khi bộ nhớ thấp hoặc khi một system call trả về giá trị nằm ngoài phạm vi dự kiến. Trong trường hợp này, tốt hơn là báo lỗi cho caller. Nếu không thể báo lỗi cho caller, có thể sử dụng :c:func:`Py_FatalError`.

   .. versionadded:: 3.7

.. c:macro:: Py_SAFE_DOWNCAST(value, larger, smaller)

   Ép kiểu *value* sang kiểu *smaller* từ kiểu *larger*, đồng thời xác thực rằng không có thông tin nào bị mất.

   Trong các bản build release của Python, điều này gần tương đương với
   :samp:`(({smaller}) {value})` (trong C++, thay vào đó sẽ sử dụng :samp:`static_cast<{smaller}>({value})`).

   Trong các bản build debug (ngụ ý rằng :c:macro:`Py_DEBUG` được định nghĩa), điều này xác nhận rằng không có thông tin nào bị mất khi ép kiểu từ *larger* sang *smaller*.

   *giá trị*, *lớn hơn*, và *nhỏ hơn* đều có thể được đánh giá nhiều hơn một lần trong biểu thức; do đó, không truyền trực tiếp một biểu thức có side effect vào macro này.

.. c:macro:: Py_BUILD_ASSERT(cond)

   Kiểm tra một điều kiện tại thời điểm biên dịch *cond*, dưới dạng một câu lệnh. Quá trình build sẽ thất bại nếu điều kiện sai hoặc không thể được đánh giá tại thời điểm biên dịch.

   Về cơ bản, tương ứng với :samp:`static_assert({cond})` trên C23 trở lên.

   Ví dụ::

      Py_BUILD_ASSERT(sizeof(PyTime_t) == sizeof(int64_t));

   .. versionadded:: 3.3

.. c:macro:: Py_BUILD_ASSERT_EXPR(cond)

   Kiểm tra một điều kiện tại thời điểm biên dịch *cond*, dưới dạng một biểu thức có giá trị là ``0``. Quá trình build sẽ thất bại nếu điều kiện sai hoặc không thể được đánh giá tại thời điểm biên dịch.

   Ví dụ::

      #define foo_to_char(foo) \
          ((char *)(foo) + Py_BUILD_ASSERT_EXPR(offsetof(struct foo, string) == 0))

   .. versionadded:: 3.3


Tiện ích kích thước kiểu
^^^^^^^^^^^^^^^^^^^^^^^^

.. c:macro:: Py_ARRAY_LENGTH(array)

   Tính độ dài của một mảng C được cấp phát tĩnh tại thời điểm biên dịch.

   Đối số *array* phải là một mảng C có kích thước được biết tại thời điểm biên dịch. Việc truyền một mảng có kích thước không xác định, chẳng hạn như mảng được cấp phát trên heap, sẽ gây ra lỗi biên dịch trên một số compiler hoặc cho kết quả không chính xác trong các trường hợp khác.

   Điều này gần tương đương với::

      sizeof(array) / sizeof((array)[0])

.. c:macro:: Py_MEMBER_SIZE(type, member)

   Trả về kích thước tính bằng byte của *type* *member* trong một structure.

   Gần tương đương với :samp:`sizeof((({type} *)NULL)->{member})`.

   .. versionadded:: 3.6


Tiện ích định nghĩa macro
^^^^^^^^^^^^^^^^^^^^^^^^^

.. c:macro:: Py_FORCE_EXPANSION(X)

   Tương đương với :samp:`{X}`, hữu ích cho việc ghép token trong macro, vì các phép mở rộng macro trong *X* bị bộ tiền xử lý buộc phải đánh giá.

.. c:macro:: Py_STRINGIFY(x)

   Chuyển ``x`` thành một chuỗi C. Ví dụ, ``Py_STRINGIFY(123)`` trả về ``"123"``.

   .. versionadded:: 3.4


Các tiện ích khai báo
---------------------

Có thể sử dụng các macro sau trong các khai báo. Chúng hữu ích nhất khi định nghĩa chính C API và chỉ có phạm vi sử dụng hạn chế đối với các tác giả extension. Hầu hết chúng mở rộng thành cú pháp dành riêng cho từng compiler của các extension phổ biến cho ngôn ngữ C.

.. c:macro:: Py_ALWAYS_INLINE

   Yêu cầu compiler luôn inline một hàm static inline. Compiler có thể bỏ qua yêu cầu này và quyết định không inline hàm.

   Tương ứng với thuộc tính ``always_inline`` trong GCC và ``__forceinline`` trong MSVC.

   Có thể sử dụng nó để inline các hàm static inline quan trọng về hiệu năng khi build Python ở chế độ debug với tính năng inline hàm bị vô hiệu hóa. Ví dụ, MSC vô hiệu hóa tính năng inline hàm khi build ở chế độ debug.

   Việc áp dụng Py_ALWAYS_INLINE một cách máy móc cho một hàm inline static có thể khiến hiệu năng kém hơn (chẳng hạn do kích thước mã tăng). Trình biên dịch thường phân tích chi phí/lợi ích thông minh hơn lập trình viên.

   Nếu Python được :ref:`xây dựng ở chế độ debug <debug-build>` (nếu macro :c:macro:`Py_DEBUG` được định nghĩa), macro :c:macro:`Py_ALWAYS_INLINE` sẽ không thực hiện gì.

   Nó phải được chỉ định trước kiểu trả về của hàm. Cách sử dụng::

       static inline Py_ALWAYS_INLINE int random(void) { return 4; }

   .. versionadded:: 3.11

.. c:macro:: Py_NO_INLINE

   Tắt inline trên một hàm. Ví dụ, điều này làm giảm mức sử dụng stack C: hữu ích trong các bản build LTO+PGO vốn inline rất nhiều mã (xem
   :issue:`33720`).

   Tương ứng với thuộc tính/chỉ định ``noinline`` trên GCC và MSVC.

   Cách sử dụng::

       Py_NO_INLINE static int random(void) { return 4; }

   .. versionadded:: 3.11

.. c:macro:: Py_DEPRECATED(version)

   Sử dụng macro này để khai báo các API đã bị deprecated trong một phiên bản CPython cụ thể. Macro phải được đặt trước tên symbol.

   Ví dụ::

      Py_DEPRECATED(3.8) PyAPI_FUNC(int) Py_OldFunction(void);

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ MSVC.

.. c:macro:: Py_LOCAL(type)

   Khai báo một hàm trả về *type* được chỉ định, sử dụng bộ định tính gọi nhanh cho các hàm cục bộ trong tệp hiện tại. Về mặt ngữ nghĩa, điều này tương đương với :samp:`static {type}`.

.. c:macro:: Py_LOCAL_INLINE(type)

   Tương đương với :c:macro:`Py_LOCAL` nhưng đồng thời yêu cầu hàm được inline.

.. c:macro:: Py_LOCAL_SYMBOL

   Macro dùng để khai báo một symbol là cục bộ trong shared library (ẩn). Trên các nền tảng được hỗ trợ, macro này đảm bảo symbol không được export.

   Trên các phiên bản GCC/Clang tương thích, macro này mở rộng thành ``__attribute__((visibility("hidden")))``.

.. c:macro:: Py_EXPORTED_SYMBOL

   Macro dùng để khai báo một symbol (hàm hoặc dữ liệu) là được export. Trên Windows, macro này mở rộng thành ``__declspec(dllexport)``. Trên các phiên bản GCC/Clang tương thích, macro này mở rộng thành ``__attribute__((visibility("default")))``. Macro này dùng để định nghĩa chính C API; các extension module không nên sử dụng nó.


.. c:macro:: Py_IMPORTED_SYMBOL

   Macro dùng để khai báo một symbol là được import. Trên Windows, macro này mở rộng thành ``__declspec(dllimport)``. Macro này dùng để định nghĩa chính C API; các extension module không nên sử dụng nó.


.. c:macro:: PyAPI_FUNC(type)

   Macro được CPython sử dụng để khai báo một hàm là một phần của C API. Phần mở rộng của macro này phụ thuộc vào nền tảng và cấu hình bản build. Macro này dành cho việc định nghĩa chính C API của CPython; các extension module không nên sử dụng nó cho các symbol riêng của mình.


.. c:macro:: PyAPI_DATA(type)

   Macro được CPython sử dụng để khai báo một biến toàn cục công khai là một phần của C API. Phần mở rộng của macro này phụ thuộc vào nền tảng và cấu hình bản build. Macro này dành cho việc định nghĩa chính C API của CPython; các extension module không nên sử dụng nó cho các symbol riêng của mình.


Các macro lỗi thời
------------------

Các macro sau đây đã được sử dụng cho những tính năng đã được chuẩn hóa trong C11.

.. c:macro:: Py_ALIGNED(num)

   Chỉ định alignment là *num* byte trên các compiler hỗ trợ tính năng này.

   Hãy cân nhắc sử dụng specifier ``_Alignas`` tiêu chuẩn C11 thay cho macro này.

.. c:macro:: Py_LL(number)
             Py_ULL(number)

   Lần lượt sử dụng *number* làm hằng số nguyên ``long long`` hoặc ``unsigned long long``.

   Mở rộng thành *number* theo sau bởi ``LL`` hoặc ``LLU``, tương ứng, nhưng trên một số compiler cũ sẽ mở rộng thành một số hậu tố dành riêng cho compiler.

   Cân nhắc sử dụng trực tiếp các hậu tố theo tiêu chuẩn C99 là ``LL`` và ``LLU``.

.. c:macro:: Py_MEMCPY(dest, src, n)

   Đây là bí danh của :c:func:`!memcpy`.

   .. soft-deprecated:: 3.14
      Thay vào đó, hãy sử dụng trực tiếp :c:func:`!memcpy`.

.. c:macro:: Py_VA_COPY

   Đây là bí danh của hàm ``va_copy`` theo tiêu chuẩn C99.

   Trước đây, thao tác này sẽ sử dụng một phương thức dành riêng cho compiler để sao chép một ``va_list``.

   .. versionchanged:: 3.6
      Hiện nay, đây là bí danh của ``va_copy``.

   .. soft-deprecated:: 3.14


.. _api-objects:

Đối tượng, Kiểu và Số lượng tham chiếu
======================================

.. index:: pair: object; type

Hầu hết các hàm Python/C API đều có một hoặc nhiều đối số, cũng như một giá trị trả về thuộc kiểu :c:expr:`PyObject*`. Kiểu này là một con trỏ tới một kiểu dữ liệu không trong suốt, đại diện cho một đối tượng Python bất kỳ. Vì ngôn ngữ Python xử lý tất cả các kiểu đối tượng Python theo cùng một cách trong hầu hết các tình huống (ví dụ: phép gán, quy tắc phạm vi và truyền đối số), nên việc biểu diễn chúng bằng một kiểu C duy nhất là hoàn toàn phù hợp. Hầu hết mọi đối tượng Python đều nằm trên heap: bạn không bao giờ khai báo một biến tự động hoặc biến static thuộc kiểu
:c:type:`PyObject`, mà chỉ có thể khai báo các biến con trỏ thuộc kiểu :c:expr:`PyObject*`. Ngoại lệ duy nhất là các đối tượng kiểu; vì chúng không bao giờ được giải phóng, chúng thường là các đối tượng :c:type:`PyTypeObject` static.

Tất cả các đối tượng Python (kể cả số nguyên Python) đều có một :dfn:`type` và một
:dfn:`reference count`. Kiểu của một đối tượng xác định đó là loại đối tượng nào (ví dụ: một số nguyên, một danh sách hoặc một hàm do người dùng định nghĩa; còn nhiều loại khác được giải thích trong :ref:`types`). Với mỗi kiểu thường gặp đều có một macro để kiểm tra xem một đối tượng có thuộc kiểu đó hay không; chẳng hạn, ``PyList_Check(a)`` là true khi (và chỉ khi) đối tượng được trỏ tới bởi *a* là một danh sách Python.


.. _api-refcounts:

Số lượng tham chiếu
-------------------

Số lượng tham chiếu rất quan trọng vì máy tính ngày nay có dung lượng bộ nhớ hữu hạn (và thường bị giới hạn nghiêm trọng); nó đếm có bao nhiêu vị trí khác nhau có :term:`strong reference` đến một đối tượng. Vị trí như vậy có thể là một đối tượng khác, một biến C toàn cục (hoặc static), hoặc một biến cục bộ trong một hàm C nào đó. Khi :term:`strong reference` cuối cùng đến một đối tượng được giải phóng (tức là số lượng tham chiếu của nó trở thành không), đối tượng sẽ được giải phóng. Nếu đối tượng chứa các tham chiếu đến những đối tượng khác, các tham chiếu đó sẽ được giải phóng. Những đối tượng khác đó lần lượt có thể được giải phóng nếu không còn tham chiếu nào đến chúng, và cứ tiếp tục như vậy. (Ở đây có một vấn đề hiển nhiên với các đối tượng tham chiếu lẫn nhau; hiện tại, giải pháp là "đừng làm vậy.")

.. index::
   single: Py_INCREF (C function)
   single: Py_DECREF (C function)

Số lượng tham chiếu luôn được thao tác một cách tường minh. Cách thông thường là sử dụng macro :c:func:`Py_INCREF` để tạo một tham chiếu mới đến một đối tượng (tức là tăng số lượng tham chiếu lên một), và :c:func:`Py_DECREF` để giải phóng tham chiếu đó (tức là giảm số lượng tham chiếu đi một). Macro :c:func:`Py_DECREF` phức tạp hơn đáng kể so với macro incref, vì nó phải kiểm tra xem số lượng tham chiếu có trở thành không hay không, rồi khiến deallocator của đối tượng được gọi. Deallocator là một con trỏ hàm nằm trong cấu trúc kiểu của đối tượng. Deallocator dành riêng cho kiểu sẽ đảm nhiệm việc giải phóng các tham chiếu đến những đối tượng khác được chứa trong đối tượng nếu đây là một kiểu đối tượng hợp thành, chẳng hạn như list, đồng thời thực hiện mọi bước hoàn tất bổ sung cần thiết. Không thể xảy ra việc số lượng tham chiếu bị tràn; có ít nhất số bit đủ để chứa số lượng tham chiếu bằng số vị trí bộ nhớ riêng biệt trong bộ nhớ ảo (với giả định ``sizeof(Py_ssize_t) >= sizeof(void*)``). Do đó, thao tác tăng số lượng tham chiếu rất đơn giản.

Không cần phải giữ một :term:`strong reference` (tức là tăng số lượng tham chiếu) cho mọi biến cục bộ chứa con trỏ đến một đối tượng. Về lý thuyết, số lượng tham chiếu của đối tượng tăng lên một khi biến được cho trỏ đến đối tượng đó và giảm đi một khi biến ra khỏi phạm vi. Tuy nhiên, hai thay đổi này triệt tiêu lẫn nhau, nên cuối cùng số lượng tham chiếu không thay đổi. Lý do thực sự để sử dụng số lượng tham chiếu là ngăn không cho đối tượng bị giải phóng chừng nào biến của chúng ta còn trỏ đến nó. Nếu biết rằng có ít nhất một tham chiếu khác đến đối tượng tồn tại ít nhất lâu bằng biến của chúng ta, thì tạm thời không cần tạo một :term:`strong reference` mới (tức là tăng số lượng tham chiếu). Một tình huống quan trọng thường gặp là khi các đối tượng được truyền làm đối số cho các hàm C trong một extension module được gọi từ Python; cơ chế gọi đảm bảo giữ một tham chiếu đến mọi đối số trong suốt thời gian gọi.

Tuy nhiên, một sai lầm phổ biến là lấy một đối tượng ra khỏi list rồi giữ nó trong một khoảng thời gian mà không tạo một tham chiếu mới. Một thao tác khác hoàn toàn có thể loại bỏ đối tượng khỏi list, giải phóng tham chiếu đó và có khả năng giải phóng cả đối tượng. Mối nguy hiểm thực sự là những thao tác có vẻ vô hại có thể gọi mã Python tùy ý để thực hiện việc này; có một đường dẫn mã cho phép quyền điều khiển quay trở lại người dùng từ một :c:func:`Py_DECREF`, vì vậy hầu như mọi thao tác đều có khả năng nguy hiểm.

Một cách tiếp cận an toàn là luôn sử dụng các thao tác generic (các hàm có tên bắt đầu bằng ``PyObject_``, ``PyNumber_``, ``PySequence_`` hoặc ``PyMapping_``). Các thao tác này luôn tạo một :term:`strong reference` mới (tức là tăng số lượng tham chiếu) cho đối tượng mà chúng trả về. Điều này để lại cho bên gọi trách nhiệm gọi :c:func:`Py_DECREF` khi đã dùng xong kết quả; chẳng bao lâu việc này sẽ trở thành thói quen tự nhiên.


.. _api-refcountdetails:

Chi tiết về số lượng tham chiếu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hành vi đếm tham chiếu của các hàm trong Python/C API được giải thích rõ nhất theo khái niệm *ownership of references*. Quyền sở hữu áp dụng cho các tham chiếu, không bao giờ áp dụng cho các đối tượng (đối tượng không thuộc quyền sở hữu của ai: chúng luôn được chia sẻ). “Sở hữu một tham chiếu” nghĩa là chịu trách nhiệm gọi Py_DECREF trên tham chiếu đó khi không còn cần đến nó. Quyền sở hữu cũng có thể được chuyển giao, nghĩa là đoạn mã nhận quyền sở hữu tham chiếu sau đó chịu trách nhiệm giải phóng tham chiếu này bằng cách gọi :c:func:`Py_DECREF` hoặc :c:func:`Py_XDECREF` khi không còn cần đến nó---hoặc chuyển tiếp trách nhiệm này (thường là cho hàm gọi nó). Khi một hàm chuyển quyền sở hữu tham chiếu cho hàm gọi nó, hàm gọi được cho là nhận một tham chiếu *new*. Khi không có quyền sở hữu nào được chuyển giao, hàm gọi được cho là *borrow* tham chiếu đó. Không cần thực hiện gì đối với một
:term:`borrowed reference`.

Ngược lại, khi một hàm gọi truyền vào một tham chiếu đến một đối tượng, có hai khả năng: hàm đó *steals* một tham chiếu đến đối tượng hoặc không.

*Stealing a reference* có nghĩa là khi bạn truyền một tham chiếu cho một hàm, hàm đó giả định rằng giờ đây nó sở hữu tham chiếu ấy. Vì chủ sở hữu mới có thể sử dụng :c:func:`!Py_DECREF` tùy ý, bạn (hàm gọi) không được sử dụng tham chiếu đó sau lời gọi.

.. index::
   single: PyList_SetItem (C function)
   single: PyTuple_SetItem (C function)

Rất ít hàm lấy cắp tham chiếu; hai ngoại lệ đáng chú ý là
:c:func:`PyList_SetItem` và :c:func:`PyTuple_SetItem`, các hàm này lấy cắp một tham chiếu đến phần tử (nhưng không lấy cắp tham chiếu đến tuple hoặc list chứa phần tử đó!). Các hàm này được thiết kế để lấy cắp một tham chiếu vì một thành ngữ phổ biến khi điền tuple hoặc list bằng các đối tượng mới được tạo; ví dụ, mã để tạo tuple ``(1, 2, "three")`` có thể trông như sau (tạm thời bỏ qua việc xử lý lỗi; cách viết mã tốt hơn được trình bày bên dưới)::

   PyObject *t;

   t = PyTuple_New(3);
   PyTuple_SetItem(t, 0, PyLong_FromLong(1L));
   PyTuple_SetItem(t, 1, PyLong_FromLong(2L));
   PyTuple_SetItem(t, 2, PyUnicode_FromString("three"));

Ở đây, :c:func:`PyLong_FromLong` trả về một tham chiếu mới, ngay lập tức bị :c:func:`PyTuple_SetItem` lấy cắp. Khi muốn tiếp tục sử dụng một đối tượng dù tham chiếu đến đối tượng đó sẽ bị lấy cắp, hãy dùng :c:func:`Py_INCREF` để lấy thêm một tham chiếu trước khi gọi hàm lấy cắp tham chiếu.

Nhân tiện, :c:func:`PyTuple_SetItem` là cách *only* để thiết lập các phần tử tuple;
:c:func:`PySequence_SetItem` và :c:func:`PyObject_SetItem` từ chối thực hiện việc này vì tuple là một kiểu dữ liệu bất biến. Bạn chỉ nên sử dụng
:c:func:`PyTuple_SetItem` cho các tuple do chính bạn tạo.

Có thể viết code tương đương để điền dữ liệu vào một list bằng cách sử dụng :c:func:`PyList_New` và :c:func:`PyList_SetItem`.

Tuy nhiên, trên thực tế, bạn sẽ hiếm khi sử dụng những cách này để tạo và điền dữ liệu vào một tuple hoặc list. Có một hàm generic, :c:func:`Py_BuildValue`, có thể tạo hầu hết các object thông dụng từ các giá trị C, được điều khiển bởi chuỗi :dfn:`format string`. Ví dụ, hai khối code trên có thể được thay thế bằng đoạn sau (đoạn này cũng xử lý việc kiểm tra lỗi)::

   PyObject *tuple, *list;

   tuple = Py_BuildValue("(iis)", 1, 2, "three");
   list = Py_BuildValue("[iis]", 1, 2, "three");

Việc sử dụng :c:func:`PyObject_SetItem` và các hàm liên quan với những item mà bạn chỉ mượn các reference, chẳng hạn như các đối số được truyền vào hàm bạn đang viết, phổ biến hơn nhiều. Trong trường hợp đó, hành vi liên quan đến reference của chúng hợp lý hơn nhiều, vì bạn không phải lấy một reference mới chỉ để có thể chuyển reference đó đi ("để nó bị lấy mất"). Ví dụ, hàm này đặt tất cả item của một list (thực ra là bất kỳ mutable sequence nào) thành một item cho trước::

   int
   set_all(PyObject *target, PyObject *item)
   {
       Py_ssize_t i, n;

       n = PyObject_Length(target);
       if (n < 0)
           return -1;
       for (i = 0; i < n; i++) {
           PyObject *index = PyLong_FromSsize_t(i);
           if (!index)
               return -1;
           if (PyObject_SetItem(target, index, item) < 0) {
               Py_DECREF(index);
               return -1;
           }
           Py_DECREF(index);
       }
       return 0;
   }

.. index:: single: set_all()

Tình huống này hơi khác đối với các giá trị trả về của hàm. Mặc dù việc truyền một reference đến hầu hết các hàm không làm thay đổi trách nhiệm sở hữu của bạn đối với reference đó, nhiều hàm trả về một reference đến một object sẽ trao quyền sở hữu reference đó cho bạn. Lý do rất đơn giản: trong nhiều trường hợp, object được trả về được tạo ngay lúc đó, và reference bạn nhận được là reference duy nhất đến object. Vì vậy, các hàm generic trả về reference đến object, chẳng hạn như :c:func:`PyObject_GetItem` và :c:func:`PySequence_GetItem`, luôn trả về một reference mới (caller trở thành chủ sở hữu của reference).

Điều quan trọng cần nhận ra là việc bạn có sở hữu reference do một hàm trả về hay không chỉ phụ thuộc vào hàm bạn gọi --- *bộ lông* (kiểu của object được truyền làm đối số cho hàm) *không liên quan đến việc đó!* Vì vậy, nếu bạn lấy một item từ list bằng :c:func:`PyList_GetItem`, bạn không sở hữu reference đó --- nhưng nếu bạn lấy cùng item từ cùng list bằng :c:func:`PySequence_GetItem` (tình cờ nhận chính xác cùng các đối số), bạn sở hữu một reference đến object được trả về.

.. index::
   single: PyList_GetItem (C function)
   single: PySequence_GetItem (C function)

Sau đây là một ví dụ về cách bạn có thể viết một hàm tính tổng các phần tử trong một danh sách số nguyên; một lần sử dụng :c:func:`PyList_GetItem`, và một lần sử dụng :c:func:`PySequence_GetItem`.::

   long
   sum_list(PyObject *list)
   {
       Py_ssize_t i, n;
       long total = 0, value;
       PyObject *item;

       n = PyList_Size(list);
       if (n < 0)
           return -1; /* Không phải list */
       for (i = 0; i < n; i++) {
           item = PyList_GetItem(list, i); /* Không thể thất bại */
           if (!PyLong_Check(item)) continue; /* Bỏ qua giá trị không phải số nguyên */
           value = PyLong_AsLong(item);
           if (value == -1 && PyErr_Occurred())
               /* Số nguyên quá lớn để chứa trong kiểu long của C, thoát */
               return -1;
           total += value;
       }
       return total;
   }

.. index:: single: sum_list()

::

   long
   sum_sequence(PyObject *sequence)
   {
       Py_ssize_t i, n;
       long total = 0, value;
       PyObject *item;
       n = PySequence_Length(sequence);
       if (n < 0)
           return -1; /* Không có độ dài */
       for (i = 0; i < n; i++) {
           item = PySequence_GetItem(sequence, i);
           if (item == NULL)
               return -1; /* Không phải sequence, hoặc có lỗi khác */
           if (PyLong_Check(item)) {
               value = PyLong_AsLong(item);
               Py_DECREF(item);
               if (value == -1 && PyErr_Occurred())
                   /* Số nguyên quá lớn để chứa trong kiểu long của C, thoát */
                   return -1;
               total += value;
           }
           else {
               Py_DECREF(item); /* Loại bỏ quyền sở hữu tham chiếu */
           }
       }
       return total;
   }

.. index:: single: sum_sequence()


.. _api-types:

Các kiểu dữ liệu
----------------

Có một vài kiểu dữ liệu khác đóng vai trò quan trọng trong Python/C API; hầu hết là các kiểu C đơn giản như :c:expr:`int`, :c:expr:`long`,
:c:expr:`double` và :c:expr:`char*`. Một vài kiểu cấu trúc được dùng để mô tả các bảng tĩnh dùng để liệt kê những hàm được một module export hoặc các thuộc tính dữ liệu của một kiểu đối tượng mới, và một kiểu khác được dùng để mô tả giá trị của một số phức. Những kiểu này sẽ được thảo luận cùng với các hàm sử dụng chúng.

.. c:type:: Py_ssize_t

   Một kiểu số nguyên có dấu sao cho ``sizeof(Py_ssize_t) == sizeof(size_t)``. C99 không định nghĩa trực tiếp kiểu như vậy (size_t là một kiểu số nguyên không dấu). Xem :pep:`353` để biết chi tiết. ``PY_SSIZE_T_MAX`` là giá trị dương lớn nhất của kiểu :c:type:`Py_ssize_t`.


.. _api-exceptions:

Ngoại lệ
========

Lập trình viên Python chỉ cần xử lý ngoại lệ nếu yêu cầu xử lý lỗi cụ thể; các ngoại lệ không được xử lý sẽ tự động được truyền lên caller, rồi đến caller của caller, cứ như vậy cho đến khi chúng đến trình thông dịch cấp cao nhất, tại đó chúng được báo cáo cho người dùng kèm theo stack traceback.

.. index:: single: PyErr_Occurred (C function)

Tuy nhiên, đối với lập trình viên C, việc kiểm tra lỗi luôn phải được thực hiện một cách rõ ràng. Tất cả các hàm trong Python/C API đều có thể phát sinh ngoại lệ, trừ khi tài liệu của hàm nêu rõ điều ngược lại. Nhìn chung, khi gặp lỗi, một hàm sẽ thiết lập một ngoại lệ, loại bỏ mọi tham chiếu đến đối tượng mà nó sở hữu và trả về một chỉ báo lỗi. Nếu không có tài liệu nêu khác, chỉ báo này là ``NULL`` hoặc ``-1``, tùy thuộc vào kiểu giá trị trả về của hàm. Một số ít hàm trả về kết quả Boolean đúng/sai, trong đó false cho biết đã xảy ra lỗi. Rất ít hàm không trả về chỉ báo lỗi rõ ràng hoặc có giá trị trả về không rõ ràng, nên cần kiểm tra lỗi một cách rõ ràng bằng
:c:func:`PyErr_Occurred`. Những ngoại lệ này luôn được ghi rõ trong tài liệu.

.. index::
   single: PyErr_SetString (C function)
   single: PyErr_Clear (C function)

Trạng thái ngoại lệ được duy trì trong bộ lưu trữ riêng cho từng luồng (tương đương với việc sử dụng bộ lưu trữ toàn cục trong một ứng dụng không có luồng). Một luồng có thể ở một trong hai trạng thái: đã xảy ra ngoại lệ hoặc chưa. Có thể sử dụng hàm
:c:func:`PyErr_Occurred` để kiểm tra trạng thái này: hàm trả về một tham chiếu mượn đến đối tượng kiểu ngoại lệ khi đã xảy ra ngoại lệ và ``NULL`` trong trường hợp ngược lại. Có một số hàm dùng để thiết lập trạng thái ngoại lệ:
:c:func:`PyErr_SetString` là hàm phổ biến nhất (mặc dù không phải là hàm tổng quát nhất) để thiết lập trạng thái ngoại lệ, còn :c:func:`PyErr_Clear` sẽ xóa trạng thái ngoại lệ.

Trạng thái ngoại lệ đầy đủ bao gồm ba đối tượng (tất cả đều có thể là ``NULL``): kiểu ngoại lệ, giá trị ngoại lệ tương ứng và traceback. Những đối tượng này có ý nghĩa giống như kết quả Python của ``sys.exc_info()``; tuy nhiên, chúng không giống nhau: các đối tượng Python biểu diễn ngoại lệ gần nhất đang được xử lý bởi một Python :keyword:`try` ...
:keyword:`except`, trong khi trạng thái ngoại lệ ở cấp C chỉ tồn tại trong lúc một ngoại lệ được truyền qua lại giữa các hàm C cho đến khi đến vòng lặp chính của trình thông dịch bytecode Python, nơi chịu trách nhiệm chuyển nó sang ``sys.exc_info()`` và các đối tượng liên quan.

.. index:: single: exc_info (in module sys)

Lưu ý rằng kể từ Python 1.5, cách được ưu tiên và an toàn với thread để truy cập trạng thái ngoại lệ từ mã Python là gọi hàm :func:`sys.exc_info`, hàm này trả về trạng thái ngoại lệ theo từng thread cho mã Python. Ngoài ra, ngữ nghĩa của cả hai cách truy cập trạng thái ngoại lệ đã thay đổi, כך cho một hàm bắt một ngoại lệ sẽ lưu và khôi phục trạng thái ngoại lệ của thread đó để bảo toàn trạng thái ngoại lệ của hàm gọi nó. Điều này ngăn ngừa các lỗi thường gặp trong mã xử lý ngoại lệ do một hàm có vẻ vô hại ghi đè lên ngoại lệ đang được xử lý; đồng thời cũng giảm việc kéo dài vòng đời thường không mong muốn của các đối tượng được tham chiếu bởi các stack frame trong traceback.

Theo nguyên tắc chung, một hàm gọi một hàm khác để thực hiện một tác vụ nào đó nên kiểm tra xem hàm được gọi có phát sinh ngoại lệ hay không; nếu có, nó nên truyền trạng thái ngoại lệ cho hàm gọi nó. Nó nên loại bỏ mọi tham chiếu đối tượng mà nó sở hữu và trả về một chỉ báo lỗi, nhưng *không* được đặt một ngoại lệ khác — điều đó sẽ ghi đè lên ngoại lệ vừa được phát sinh và làm mất thông tin quan trọng về nguyên nhân chính xác của lỗi.

.. index:: single: sum_sequence()

Một ví dụ đơn giản về cách phát hiện ngoại lệ và truyền chúng đi được trình bày trong
:c:func:`!sum_sequence` ví dụ ở trên. Tình cờ là ví dụ này không cần dọn dẹp bất kỳ tham chiếu nào đang sở hữu khi phát hiện lỗi. Hàm ví dụ sau đây minh họa một số thao tác dọn dẹp khi có lỗi. Trước hết, để nhắc bạn nhớ lý do mình yêu thích Python, chúng ta trình bày mã Python tương đương::

   def incr_item(dict, key):
       try:
           item = dict[key]
       except KeyError:
           item = 0
       dict[key] = item + 1

.. index:: single: incr_item()

Dưới đây là mã C tương ứng, với đầy đủ chi tiết::

   int
   incr_item(PyObject *dict, PyObject *key)
   {
       /* Mọi đối tượng đều được khởi tạo thành NULL để dùng Py_XDECREF */
       PyObject *item = NULL, *const_one = NULL, *incremented_item = NULL;
       int rv = -1; /* Giá trị trả về được khởi tạo là -1 (thất bại) */

       item = PyObject_GetItem(dict, key);
       if (item == NULL) {
           /* Chỉ xử lý KeyError: */
           if (!PyErr_ExceptionMatches(PyExc_KeyError))
               goto error;

           /* Xóa lỗi và dùng giá trị không: */
           PyErr_Clear();
           item = PyLong_FromLong(0L);
           if (item == NULL)
               goto error;
       }
       const_one = PyLong_FromLong(1L);
       if (const_one == NULL)
           goto error;

       incremented_item = PyNumber_Add(item, const_one);
       if (incremented_item == NULL)
           goto error;

       if (PyObject_SetItem(dict, key, incremented_item) < 0)
           goto error;
       rv = 0; /* Thành công */
       /* Tiếp tục với mã dọn dẹp */

    error:
       /* Mã dọn dẹp, dùng chung cho đường dẫn thành công và thất bại */

       /* Dùng Py_XDECREF() để bỏ qua các tham chiếu NULL */
       Py_XDECREF(item);
       Py_XDECREF(const_one);
       Py_XDECREF(incremented_item);

       return rv; /* -1 khi lỗi, 0 khi thành công */
   }

.. index:: single: incr_item()

.. index::
   single: PyErr_ExceptionMatches (C function)
   single: PyErr_Clear (C function)
   single: Py_XDECREF (C function)

Ví dụ này minh họa một cách sử dụng được khuyến nghị của câu lệnh ``goto`` trong C! Nó minh họa cách sử dụng :c:func:`PyErr_ExceptionMatches` và
:c:func:`PyErr_Clear` để xử lý các ngoại lệ cụ thể, cũng như cách sử dụng
:c:func:`Py_XDECREF` để giải phóng các tham chiếu được sở hữu có thể là ``NULL`` (hãy lưu ý ``'X'`` trong tên; :c:func:`Py_DECREF` sẽ gây lỗi khi gặp một tham chiếu ``NULL``). Điều quan trọng là các biến được dùng để lưu giữ các tham chiếu được sở hữu phải được khởi tạo thành ``NULL`` để cách này hoạt động; tương tự, giá trị trả về dự kiến được khởi tạo thành ``-1`` (thất bại) và chỉ được đặt thành thành công sau khi lệnh gọi cuối cùng thực hiện thành công.


.. _api-embedding:

Nhúng Python
============

Nhiệm vụ quan trọng duy nhất mà những người nhúng (khác với người viết extension) trình thông dịch Python phải quan tâm là khởi tạo và có thể là kết thúc hoạt động của trình thông dịch Python. Hầu hết chức năng của trình thông dịch chỉ có thể được sử dụng sau khi trình thông dịch đã được khởi tạo.

.. index::
   single: Py_Initialize (C function)
   pair: module; builtins
   pair: module; __main__
   pair: module; sys
   triple: module; search; path
   single: path (in module sys)

Hàm khởi tạo cơ bản là :c:func:`Py_Initialize`. Hàm này khởi tạo bảng các module đã tải và tạo các module nền tảng
:mod:`builtins`, :mod:`__main__` và :mod:`sys`. Hàm này cũng khởi tạo đường dẫn tìm kiếm module (``sys.path``).

:c:func:`Py_Initialize` không thiết lập "danh sách đối số của script" (``sys.argv``). Nếu mã Python sẽ được thực thi sau đó cần biến này, hãy thiết lập
:c:member:`PyConfig.argv` và :c:member:`PyConfig.parse_argv` phải được thiết lập: xem
:ref:`Cấu hình khởi tạo Python <init-config>`.

Trên hầu hết các hệ thống (đặc biệt là Unix và Windows, mặc dù chi tiết có hơi khác nhau), :c:func:`Py_Initialize` tính toán đường dẫn tìm kiếm module dựa trên phỏng đoán tốt nhất về vị trí của tệp thực thi trình thông dịch Python tiêu chuẩn, với giả định rằng thư viện Python nằm ở một vị trí cố định tương đối so với tệp thực thi trình thông dịch Python. Cụ thể, nó tìm một thư mục có tên :file:`lib/python{X.Y}` tương đối so với thư mục cha, nơi tìm thấy tệp thực thi có tên :file:`python` trên đường dẫn tìm kiếm lệnh của shell (biến môi trường :envvar:`PATH`).

Ví dụ, nếu tệp thực thi Python được tìm thấy tại
:file:`/usr/local/bin/python`, nó sẽ giả định rằng các thư viện nằm tại
:file:`/usr/local/lib/python{X.Y}`. (Trên thực tế, đường dẫn cụ thể này cũng là vị trí "dự phòng", được sử dụng khi không tìm thấy tệp thực thi có tên :file:`python` trong :envvar:`PATH`.) Người dùng có thể ghi đè hành vi này bằng cách đặt biến môi trường :envvar:`PYTHONHOME`, hoặc chèn các thư mục bổ sung vào trước đường dẫn tiêu chuẩn bằng cách đặt :envvar:`PYTHONPATH`.

.. index::
   single: Py_GetPath (C function)
   single: Py_GetPrefix (C function)
   single: Py_GetExecPrefix (C function)
   single: Py_GetProgramFullPath (C function)

Ứng dụng nhúng có thể điều khiển quá trình tìm kiếm bằng cách đặt
:c:member:`PyConfig.program_name` *trước* khi gọi
:c:func:`Py_InitializeFromConfig`. Lưu ý rằng
:envvar:`PYTHONHOME` vẫn ghi đè điều này và :envvar:`PYTHONPATH` vẫn được chèn vào trước đường dẫn chuẩn.  Một ứng dụng cần toàn quyền kiểm soát phải cung cấp triển khai riêng cho :c:func:`Py_GetPath`,
:c:func:`Py_GetPrefix`, :c:func:`Py_GetExecPrefix`, và
:c:func:`Py_GetProgramFullPath` (tất cả đều được định nghĩa trong :file:`Modules/getpath.c`).

.. index:: single: Py_IsInitialized (C function)

Đôi khi, việc "hủy khởi tạo" Python là cần thiết.  Chẳng hạn, ứng dụng có thể muốn bắt đầu lại (thực hiện một lệnh gọi khác đến
:c:func:`Py_Initialize`) hoặc ứng dụng đã dùng xong Python và muốn giải phóng bộ nhớ do Python cấp phát.  Có thể thực hiện điều này bằng cách gọi :c:func:`Py_FinalizeEx`.  Hàm :c:func:`Py_IsInitialized` trả về true nếu Python hiện đang ở trạng thái đã khởi tạo.  Thông tin chi tiết hơn về các hàm này được cung cấp trong một chương sau. Lưu ý rằng :c:func:`Py_FinalizeEx` *không* giải phóng toàn bộ bộ nhớ do trình thông dịch Python cấp phát; chẳng hạn, hiện tại không thể giải phóng bộ nhớ do các extension module cấp phát.


.. _api-debugging:

Các bản build dùng để gỡ lỗi
============================

Python có thể được build với một số macro để bật thêm các bước kiểm tra interpreter và extension module. Các bước kiểm tra này thường tạo ra overhead lớn cho runtime, vì vậy mặc định chúng không được bật.

Danh sách đầy đủ các loại debug build khác nhau nằm trong tệp
:file:`Misc/SpecialBuilds.txt` của bản phân phối mã nguồn Python. Có các build hỗ trợ tracing reference count, debugging memory allocator hoặc profiling ở mức thấp vòng lặp chính của interpreter. Phần còn lại của mục này chỉ mô tả những build được sử dụng thường xuyên nhất.

.. c:macro:: Py_DEBUG

Biên dịch interpreter với macro :c:macro:`!Py_DEBUG` được định nghĩa sẽ tạo ra thứ thường được gọi là :ref:`a debug build of Python <debug-build>`.
:c:macro:`!Py_DEBUG` được bật trong Unix build bằng cách thêm
:option:`--with-pydebug` vào lệnh :file:`./configure`. Macro không dành riêng cho Python là :c:macro:`!_DEBUG` cũng ngầm bật tùy chọn này khi xuất hiện. Khi :c:macro:`!Py_DEBUG` được bật trong Unix build, trình biên dịch sẽ tắt tối ưu hóa.

Ngoài việc debugging reference count được mô tả bên dưới, các bước kiểm tra bổ sung cũng được thực hiện; xem :ref:`Python Debug Build <debug-build>`.

Việc định nghĩa ``Py_TRACE_REFS`` cho phép truy vết tham chiếu (xem :option:`configure --with-trace-refs option <--with-trace-refs>`). Khi được định nghĩa, một danh sách liên kết kép vòng tròn gồm các đối tượng đang hoạt động sẽ được duy trì bằng cách thêm hai trường bổ sung vào mỗi :c:type:`PyObject`. Tổng số lần cấp phát cũng được theo dõi. Khi thoát, tất cả các tham chiếu hiện có sẽ được in ra. (Trong chế độ tương tác, việc này diễn ra sau mỗi câu lệnh được trình thông dịch thực thi.)

Vui lòng tham khảo :file:`Misc/SpecialBuilds.txt` trong bản phân phối mã nguồn Python để biết thêm thông tin chi tiết.


.. _c-api-tools:

Các công cụ bên thứ ba được khuyến nghị
=======================================

Các công cụ bên thứ ba sau đây cung cấp cả những phương pháp đơn giản hơn và tinh vi hơn để tạo các phần mở rộng C, C++ và Rust cho Python:

* `Cython <https://cython.org/>`_
* `cffi <https://cffi.readthedocs.io>`_
* `HPy <https://hpyproject.org/>`_
* `nanobind <https://github.com/wjakob/nanobind>`_ (C++)
* `Numba <https://numba.pydata.org/>`_
* `pybind11 <https://pybind11.readthedocs.io/>`_ (C++)
* `PyO3 <https://pyo3.rs/>`_ (Rust)
* `SWIG <https://www.swig.org>`_

Việc sử dụng các công cụ như vậy có thể giúp tránh phải viết code gắn chặt với một phiên bản cụ thể của CPython, tránh các lỗi đếm tham chiếu và tập trung nhiều hơn vào code của riêng bạn thay vì sử dụng CPython API. Nhìn chung, các phiên bản Python mới có thể được hỗ trợ bằng cách cập nhật công cụ, và code của bạn thường sẽ tự động sử dụng các API mới hơn, hiệu quả hơn. Một số công cụ cũng hỗ trợ biên dịch cho các triển khai Python khác từ một bộ mã nguồn duy nhất.

Các dự án này không được cùng những người duy trì Python hỗ trợ, và bạn cần báo cáo vấn đề trực tiếp với các dự án đó. Hãy nhớ kiểm tra xem dự án còn được duy trì và hỗ trợ hay không, vì danh sách trên có thể trở nên lỗi thời.

.. seealso::

   `Hướng dẫn đóng gói Python: Phần mở rộng nhị phân <https://packaging.python.org/guides/packaging-binary-extensions/>`_
      Hướng dẫn đóng gói Python không chỉ đề cập đến một số công cụ hiện có giúp đơn giản hóa việc tạo các phần mở rộng nhị phân, mà còn thảo luận về nhiều lý do khiến việc tạo một extension module ngay từ đầu có thể là điều đáng cân nhắc.

.. _`Cython`: https://cython.org/
.. _`cffi`: https://cffi.readthedocs.io
.. _`HPy`: https://hpyproject.org/
.. _`nanobind`: https://github.com/wjakob/nanobind
.. _`Numba`: https://numba.pydata.org/
.. _`pybind11`: https://pybind11.readthedocs.io/
.. _`PyO3`: https://pyo3.rs/
.. _`SWIG`: https://www.swig.org
.. _`Python Packaging User Guide: Binary Extensions`: https://packaging.python.org/guides/packaging-binary-extensions/
