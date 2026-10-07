.. highlight:: c


.. _building-on-windows:

*******************************************
Xây dựng phần mở rộng C và C++ trên Windows
*******************************************

Chương này giải thích ngắn gọn cách tạo một mô-đun phần mở rộng Windows cho Python bằng Microsoft Visual C++, sau đó trình bày chi tiết hơn về cách thức hoạt động của nó. Phần giải thích này hữu ích cho cả lập trình viên Windows đang học cách xây dựng phần mở rộng Python và lập trình viên Unix quan tâm đến việc tạo ra phần mềm có thể được xây dựng thành công trên cả Unix và Windows.

Các tác giả mô-đun được khuyến khích sử dụng phương pháp distutils để xây dựng các mô-đun phần mở rộng, thay vì phương pháp được mô tả trong phần này. Bạn vẫn cần trình biên dịch C đã được dùng để xây dựng Python; thông thường là Microsoft Visual C++.

.. note::

   Chương này đề cập đến một số tên tệp có chứa số phiên bản Python được mã hóa. Các tên tệp này được biểu diễn bằng số phiên bản như sau: ``XY``; trên thực tế, ``'X'`` sẽ là số phiên bản chính và ``'Y'`` sẽ là số phiên bản phụ của bản phát hành Python mà bạn đang sử dụng. Ví dụ: nếu bạn đang sử dụng Python 2.2.1, ``XY`` thực tế sẽ là ``22``.


.. _win-cookbook:

Cách tiếp cận theo công thức
============================

Có hai cách tiếp cận để xây dựng các mô-đun phần mở rộng trên Windows, cũng giống như trên Unix: sử dụng gói ``setuptools`` để kiểm soát quy trình xây dựng, hoặc thực hiện mọi việc thủ công. Cách tiếp cận setuptools hoạt động tốt với hầu hết các phần mở rộng; tài liệu về việc sử dụng ``setuptools`` để xây dựng và đóng gói các mô-đun phần mở rộng có tại :ref:`setuptools-index`. Nếu bạn thực sự cần thực hiện mọi việc thủ công, việc nghiên cứu tệp dự án cho mô-đun
:source:`winsound <PCbuild/winsound.vcxproj>` thuộc thư viện chuẩn có thể mang lại nhiều điều bổ ích.


.. _dynamic-linking:

Sự khác biệt giữa Unix và Windows
=================================

.. sectionauthor:: Chris Phoenix <cphoenix@best.com>


Unix và Windows sử dụng các mô hình hoàn toàn khác nhau để nạp mã trong thời gian chạy. Trước khi thử xây dựng một module có thể được nạp động, hãy tìm hiểu cách hệ thống của bạn hoạt động.

Trong Unix, tệp shared object (:file:`.so`) chứa mã để chương trình sử dụng, cùng với tên của các hàm và dữ liệu mà tệp đó mong đợi tìm thấy trong chương trình. Khi tệp được liên kết với chương trình, tất cả tham chiếu đến các hàm và dữ liệu đó trong mã của tệp sẽ được thay đổi để trỏ đến vị trí thực tế trong chương trình, nơi các hàm và dữ liệu được đặt trong bộ nhớ. Về cơ bản, đây là một thao tác link.

Trong Windows, tệp dynamic-link library (:file:`.dll`) không có các tham chiếu chưa được giải quyết. Thay vào đó, việc truy cập các hàm hoặc dữ liệu được thực hiện thông qua một bảng tra cứu. Vì vậy, mã DLL không cần được điều chỉnh trong thời gian chạy để tham chiếu đến bộ nhớ của chương trình; thay vào đó, mã đã sử dụng bảng tra cứu của DLL, và bảng tra cứu được sửa đổi trong thời gian chạy để trỏ đến các hàm và dữ liệu.

Trong Unix, chỉ có một loại tệp thư viện (:file:`.a`) chứa mã từ nhiều tệp object (:file:`.o`). Trong bước link để tạo tệp shared object (:file:`.so`), linker có thể phát hiện rằng nó không biết một identifier được định nghĩa ở đâu. Linker sẽ tìm identifier đó trong các tệp object thuộc các thư viện; nếu tìm thấy, nó sẽ đưa toàn bộ mã từ tệp object đó vào.

Trong Windows, có hai loại thư viện: static library và import library (đều được gọi là :file:`.lib`). Static library tương tự như tệp :file:`.a` của Unix; nó chứa mã sẽ được đưa vào khi cần. Import library về cơ bản chỉ được dùng để xác nhận với linker rằng một identifier nhất định là hợp lệ và sẽ có mặt trong chương trình khi DLL được nạp. Vì vậy, linker sử dụng thông tin từ import library để xây dựng bảng tra cứu nhằm sử dụng các identifier không được đưa vào DLL. Khi một ứng dụng hoặc DLL được link, một import library có thể được tạo ra; import library này sẽ cần được sử dụng cho tất cả DLL về sau phụ thuộc vào các symbol trong ứng dụng hoặc DLL đó.

Giả sử bạn đang xây dựng hai module nạp động, B và C, vốn cần dùng chung một khối mã khác là A. Trên Unix, bạn sẽ *not* truyền :file:`A.a` cho linker đối với :file:`B.so` và :file:`C.so`; điều đó sẽ khiến mã được đưa vào hai lần, để B và C mỗi module có một bản sao riêng. Trong Windows, việc xây dựng
:file:`A.dll` cũng sẽ xây dựng :file:`A.lib`. Bạn *do* chuyển :file:`A.lib` cho linker để liên kết B và C. :file:`A.lib` không chứa mã; nó chỉ chứa thông tin sẽ được sử dụng trong runtime để truy cập mã của A.

Trong Windows, việc sử dụng import library gần giống như sử dụng ``import spam``; nó cho phép bạn truy cập các tên của spam nhưng không tạo một bản sao riêng. Trên Unix, việc liên kết với một library giống ``from spam import *`` hơn; nó thực sự tạo một bản sao riêng.

.. c:macro:: Py_NO_LINK_LIB

   Tắt linkage ngầm dựa trên ``#pragma`` với Python library, vốn được thực hiện bên trong các tệp header của CPython.

   .. versionadded:: 3.14


.. _win-dlls:

Sử dụng DLL trong thực tế
=========================

.. sectionauthor:: Chris Phoenix <cphoenix@best.com>


Python trên Windows được xây dựng bằng Microsoft Visual C++; việc sử dụng các compiler khác có thể hoạt động hoặc không. Phần còn lại của mục này dành riêng cho MSVC++.

Khi tạo DLL trong Windows, bạn có thể sử dụng CPython library theo hai cách:

1. Theo mặc định, việc đưa :file:`PC/pyconfig.h` vào trực tiếp hoặc thông qua
   :file:`Python.h` tạo liên kết ngầm, nhận biết cấu hình với thư viện. Tệp header chọn :file:`pythonXY_d.lib` cho Debug,
   :file:`pythonXY.lib` cho Release và :file:`pythonX.lib` cho Release khi :ref:`Limited API <stable-application-binary-interface>` được bật.

   Để xây dựng hai DLL, spam và ni (sử dụng các hàm C có trong spam), bạn có thể dùng các lệnh sau::

       cl /LD /I/python/include spam.c
       cl /LD /I/python/include ni.c spam.lib

   Lệnh đầu tiên đã tạo ba tệp: :file:`spam.obj`, :file:`spam.dll` và :file:`spam.lib`. :file:`Spam.dll` không chứa bất kỳ hàm Python nào (chẳng hạn như :c:func:`PyArg_ParseTuple`), nhưng nó biết cách tìm mã Python nhờ :file:`pythonXY.lib` được liên kết ngầm.

   Lệnh thứ hai đã tạo :file:`ni.dll` (cùng với :file:`.obj` và
   :file:`.lib`), tệp này biết cách tìm các hàm cần thiết từ spam và cả từ tệp thực thi Python.

2. Theo cách thủ công bằng cách định nghĩa macro :c:macro:`Py_NO_LINK_LIB` trước khi include
   :file:`Python.h`. Bạn phải truyền :file:`pythonXY.lib` cho linker.

   Để xây dựng hai DLL, spam và ni (sử dụng các hàm C có trong spam), bạn có thể dùng các lệnh sau::

      cl /LD /DPy_NO_LINK_LIB /I/python/include spam.c ../libs/pythonXY.lib
      cl /LD /DPy_NO_LINK_LIB /I/python/include ni.c spam.lib ../libs/pythonXY.lib

   Lệnh đầu tiên đã tạo ba tệp: :file:`spam.obj`, :file:`spam.dll` và :file:`spam.lib`.  :file:`Spam.dll` không chứa bất kỳ hàm Python nào (chẳng hạn như :c:func:`PyArg_ParseTuple`), nhưng nó biết cách tìm mã Python nhờ :file:`pythonXY.lib`.

   Lệnh thứ hai đã tạo :file:`ni.dll` (cùng với :file:`.obj` và
   :file:`.lib`), tệp này biết cách tìm các hàm cần thiết từ spam và cả từ tệp thực thi Python.

Không phải mọi identifier đều được export vào bảng tra cứu.  Nếu muốn các module khác (bao gồm cả Python) có thể nhìn thấy các identifier của mình, bạn phải khai báo ``_declspec(dllexport)``, như trong ``void _declspec(dllexport) initspam(void)`` hoặc ``PyObject _declspec(dllexport) *NiGetSpamData(void)``.

Developer Studio sẽ thêm vào rất nhiều import library mà bạn thực sự không cần, làm tệp thực thi tăng thêm khoảng 100K.  Để loại bỏ chúng, hãy sử dụng hộp thoại Project Settings, Link tab, để chỉ định *ignore default libraries*. Thêm :file:`msvcrt{xx}.lib` thích hợp vào danh sách các library.
