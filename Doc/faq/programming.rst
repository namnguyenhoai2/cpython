:tocdepth: 2

===============================
Câu hỏi thường gặp về lập trình
===============================

.. only:: html

   .. contents::

Câu hỏi chung
=============

Có trình gỡ lỗi ở cấp mã nguồn với các điểm dừng và khả năng thực thi từng bước không?
--------------------------------------------------------------------------------------

Có.

Dưới đây là phần mô tả một số trình gỡ lỗi dành cho Python, cùng với hàm tích hợp sẵn
:func:`breakpoint` cho phép bạn chuyển sang bất kỳ trình gỡ lỗi nào trong số đó.

Mô-đun pdb là một trình gỡ lỗi đơn giản nhưng đầy đủ cho Python, hoạt động ở chế độ console. Mô-đun này thuộc thư viện Python tiêu chuẩn và được :mod:`documented in the Library Reference Manual <pdb>`. Bạn cũng có thể tự viết trình gỡ lỗi bằng cách sử dụng mã của pdb làm ví dụ.

Môi trường phát triển tương tác IDLE, là một phần của bản phân phối Python tiêu chuẩn (thường có sẵn dưới dạng :mod:`idlelib`), bao gồm một trình gỡ lỗi đồ họa.

PythonWin là một Python IDE bao gồm trình gỡ lỗi GUI dựa trên pdb. Trình gỡ lỗi PythonWin tô màu các breakpoint và có khá nhiều tính năng thú vị, chẳng hạn như gỡ lỗi các chương trình không phải PythonWin. PythonWin có sẵn trong dự án `pywin32 <https://github.com/mhammond/pywin32>`_ và là một phần của bản phân phối `ActivePython <https://www.activestate.com/products/python/>`_.

`Eric <https://eric-ide.python-projects.org/>`_ là một IDE được xây dựng trên PyQt và thành phần chỉnh sửa Scintilla.

`trepan3k <https://github.com/rocky/python3-trepan/>`_ là một trình gỡ lỗi tương tự gdb.

`Visual Studio Code <https://code.visualstudio.com/>`_ là một IDE có các công cụ gỡ lỗi tích hợp với phần mềm quản lý phiên bản.

Có một số Python IDE thương mại bao gồm các trình gỡ lỗi đồ họa. Các IDE đó gồm:

* `Wing IDE <https://wingware.com/>`_
* `PyCharm <https://www.jetbrains.com/pycharm/>`_


Có công cụ nào giúp tìm lỗi hoặc thực hiện phân tích tĩnh không?
----------------------------------------------------------------

Có.

`Ruff <https://docs.astral.sh/ruff/>`__, `Pylint <https://pylint.readthedocs.io/>`__ và `Pyflakes <https://github.com/PyCQA/pyflakes>`__ thực hiện các bước kiểm tra cơ bản, giúp bạn phát hiện lỗi sớm hơn.

Các trình kiểm tra kiểu tĩnh như `mypy <https://mypy-lang.org/>`__, `ty <https://docs.astral.sh/ty/>`__, `Pyrefly <https://pyrefly.org/>`__ và `pytype <https://github.com/google/pytype>`__ có thể kiểm tra các type hint trong mã nguồn Python.


.. _faq-create-standalone-binary:

Làm thế nào để tạo tệp nhị phân độc lập từ một script Python?
-------------------------------------------------------------

Bạn không cần khả năng biên dịch Python thành mã C nếu mục tiêu duy nhất của bạn là tạo một chương trình độc lập mà người dùng có thể tải xuống và chạy mà không phải cài đặt bản phân phối Python trước. Có một số công cụ xác định tập hợp các module mà chương trình yêu cầu, rồi liên kết các module này với một tệp nhị phân Python để tạo ra một tệp thực thi duy nhất.

Một cách là sử dụng công cụ freeze, được tích hợp trong cây mã nguồn Python dưới dạng
:source:`Tools/freeze`. Công cụ này chuyển mã bytecode Python thành các mảng C; với một trình biên dịch C, bạn có thể nhúng tất cả module vào một chương trình mới, sau đó liên kết chương trình đó với các module Python chuẩn.

Công cụ này hoạt động bằng cách quét đệ quy mã nguồn để tìm các câu lệnh import (ở cả hai dạng), đồng thời tìm các module trong đường dẫn Python chuẩn cũng như trong thư mục mã nguồn (đối với các module tích hợp sẵn). Sau đó, công cụ chuyển bytecode của các module được viết bằng Python thành mã C (các trình khởi tạo mảng có thể được chuyển thành các đối tượng mã bằng module marshal) và tạo một tệp cấu hình tùy chỉnh chỉ chứa những module tích hợp sẵn thực sự được chương trình sử dụng. Tiếp đó, công cụ biên dịch mã C đã tạo và liên kết mã này với phần còn lại của trình thông dịch Python để tạo thành một binary độc lập, hoạt động chính xác như script của bạn.

Các package sau có thể hỗ trợ tạo các executable cho console và GUI:

* `Nuitka <https://nuitka.net/>`_ (Đa nền tảng)
* `PyInstaller <https://pyinstaller.org/>`_ (Đa nền tảng)
* `PyOxidizer <https://pyoxidizer.readthedocs.io/en/stable/>`_ (Đa nền tảng)
* `cx_Freeze <https://marcelotduarte.github.io/cx_Freeze/>`_ (Đa nền tảng)
* `py2app <https://github.com/ronaldoussoren/py2app>`_ (chỉ dành cho macOS)
* `py2exe <https://www.py2exe.org/>`_ (chỉ dành cho Windows)


Có tiêu chuẩn lập trình hoặc hướng dẫn về phong cách viết mã cho các chương trình Python không?
-----------------------------------------------------------------------------------------------

Có. Phong cách viết mã bắt buộc đối với các module trong standard library được ghi lại trong
:pep:`8`.


Ngôn ngữ cốt lõi
================

.. _faq-unboundlocalerror:

Tại sao tôi lại nhận được lỗi UnboundLocalError khi biến đã có giá trị?
-----------------------------------------------------------------------

Có thể bạn sẽ bất ngờ khi gặp :exc:`UnboundLocalError` trong đoạn mã trước đó vẫn hoạt động, sau khi sửa bằng cách thêm một câu lệnh gán ở đâu đó trong phần thân của một hàm.

Đoạn mã này:

   >>> x = 10
   >>> def bar():
   ...     print(x)
   ...
   >>> bar()
   10

hoạt động, nhưng đoạn mã này:

   >>> x = 10
   >>> def foo():
   ...     print(x)
   ...     x += 1

dẫn đến :exc:`!UnboundLocalError`:

   >>> foo()
   Traceback (most recent call last):
     ...
   UnboundLocalError: cannot access local variable 'x' where it is not associated with a value

Điều này là do khi bạn thực hiện phép gán cho một biến trong một phạm vi, biến đó sẽ trở thành biến cục bộ trong phạm vi ấy và che khuất mọi biến cùng tên trong phạm vi bên ngoài. Vì câu lệnh cuối cùng trong foo gán một giá trị mới cho ``x``, trình biên dịch nhận diện nó là một biến cục bộ. Do đó, khi ``print(x)`` ở phía trước cố in biến cục bộ chưa được khởi tạo, lỗi sẽ xảy ra.

Trong ví dụ trên, bạn có thể truy cập biến thuộc phạm vi bên ngoài bằng cách khai báo biến đó là global:

   >>> x = 10
   >>> def foobar():
   ...     global x
   ...     print(x)
   ...     x += 1
   ...
   >>> foobar()
   10

Khai báo rõ ràng này là bắt buộc để nhắc bạn rằng (không giống tình huống có vẻ tương tự với các biến lớp và biến thực thể) bạn thực sự đang thay đổi giá trị của biến trong phạm vi bên ngoài:

   >>> print(x)
   11

Bạn có thể thực hiện điều tương tự trong một phạm vi lồng nhau bằng từ khóa :keyword:`nonlocal`:

   >>> def foo():
   ...    x = 10
   ...    def bar():
   ...        nonlocal x
   ...        print(x)
   ...        x += 1
   ...    bar()
   ...    print(x)
   ...
   >>> foo()
   10
   11


Các quy tắc đối với biến cục bộ và biến toàn cục trong Python là gì?
--------------------------------------------------------------------

Trong Python, các biến chỉ được tham chiếu bên trong một hàm sẽ mặc nhiên là biến toàn cục. Nếu một biến được gán giá trị ở bất kỳ đâu trong thân hàm, biến đó được xem là biến cục bộ, trừ khi được khai báo rõ ràng là biến toàn cục.

Mặc dù thoạt đầu hơi bất ngờ, nhưng chỉ cần suy xét một chút là có thể hiểu được điều này. Một mặt, việc yêu cầu :keyword:`global` đối với các biến được gán tạo ra một rào cản chống lại các tác dụng phụ ngoài ý muốn. Mặt khác, nếu ``global`` được yêu cầu cho mọi tham chiếu toàn cục, bạn sẽ phải sử dụng ``global`` mọi lúc. Bạn sẽ phải khai báo là biến toàn cục mọi tham chiếu đến một hàm dựng sẵn hoặc đến một thành phần của mô-đun đã import. Sự rườm rà này sẽ làm mất đi tính hữu ích của khai báo ``global`` trong việc xác định các tác dụng phụ.


Tại sao các lambda được định nghĩa trong một vòng lặp với những giá trị khác nhau lại đều trả về cùng một kết quả?
------------------------------------------------------------------------------------------------------------------

Giả sử bạn sử dụng vòng lặp for để định nghĩa một vài lambda khác nhau (hoặc thậm chí các hàm thông thường), chẳng hạn như sau::

   >>> squares = []
   >>> for x in range(5):
   ...     squares.append(lambda: x**2)

Thao tác này tạo ra một danh sách chứa 5 lambda tính toán ``x**2``. Bạn có thể mong đợi rằng khi được gọi, chúng lần lượt sẽ trả về ``0``, ``1``, ``4``, ``9`` và ``16``. Tuy nhiên, khi thực sự thử, bạn sẽ thấy rằng tất cả chúng đều trả về ``16``::

   >>> squares[2]()
   16
   >>> squares[4]()
   16

Điều này xảy ra vì ``x`` không phải là biến cục bộ của các lambda mà được định nghĩa trong scope bên ngoài, và nó được truy cập khi lambda được gọi --- chứ không phải khi được định nghĩa.  Khi vòng lặp kết thúc, giá trị của ``x`` là ``4``, vì vậy tất cả các hàm hiện đều trả về ``4**2``, tức là ``16``.  Bạn cũng có thể kiểm chứng điều này bằng cách thay đổi giá trị của ``x`` và xem kết quả của các lambda thay đổi như thế nào::

   >>> x = 8
   >>> squares[2]()
   64

Để tránh điều này, bạn cần lưu các giá trị vào những biến cục bộ của các lambda, ताकि chúng không phụ thuộc vào giá trị của ``x``::

   >>> squares = []
   >>> for x in range(5):
   ...     squares.append(lambda n=x: n**2)

Ở đây, ``n=x`` tạo một biến mới ``n`` cục bộ của lambda và được tính toán khi lambda được định nghĩa, để nó có cùng giá trị mà ``x`` có tại thời điểm đó trong vòng lặp.  Điều này có nghĩa là giá trị của ``n`` sẽ là ``0`` trong lambda thứ nhất, ``1`` trong lambda thứ hai, ``2`` trong lambda thứ ba, v.v. Vì vậy, mỗi lambda giờ sẽ trả về kết quả chính xác::

   >>> squares[2]()
   4
   >>> squares[4]()
   16

Lưu ý rằng hành vi này không chỉ xảy ra với lambda mà còn áp dụng cho cả các hàm thông thường.


Làm thế nào để chia sẻ các biến toàn cục giữa các module?
---------------------------------------------------------

Cách chuẩn để chia sẻ thông tin giữa các module trong cùng một chương trình là tạo một module đặc biệt (thường được gọi là config hoặc cfg).  Chỉ cần import module config trong tất cả các module của ứng dụng; khi đó module này sẽ khả dụng dưới dạng một tên toàn cục.  Vì mỗi module chỉ có một instance, mọi thay đổi được thực hiện đối với đối tượng module sẽ được phản ánh ở mọi nơi.  Ví dụ:

config.py::

   x = 0   # Giá trị mặc định của thiết lập cấu hình 'x'

mod.py::

   import config
   config.x = 1

main.py::

   import config
   import mod
   print(config.x)

Lưu ý rằng việc sử dụng một module cũng là cơ sở để triển khai mẫu thiết kế singleton, vì cùng một lý do.


"Các phương pháp hay nhất" khi sử dụng import trong một module là gì?
---------------------------------------------------------------------

Nhìn chung, đừng sử dụng ``from modulename import *``. Làm vậy sẽ làm rối namespace của bên import và khiến các linter khó phát hiện những tên chưa được định nghĩa hơn nhiều.

Đặt các module import ở đầu tệp. Làm vậy giúp làm rõ những module nào mà code của bạn yêu cầu và tránh các câu hỏi về việc tên module có nằm trong phạm vi hay không. Sử dụng một import trên mỗi dòng giúp dễ thêm và xóa các module import, nhưng sử dụng nhiều import trên một dòng sẽ tốn ít không gian màn hình hơn.

Bạn nên nhập các module theo thứ tự sau:

1. các module của standard library -- chẳng hạn như :mod:`sys`, :mod:`os`, :mod:`argparse`, :mod:`re`
2. các module của thư viện bên thứ ba (bất kỳ module nào được cài đặt trong thư mục site-packages của Python) -- chẳng hạn như :pypi:`dateutil`, :pypi:`requests`, :pypi:`tzdata`
3. các module được phát triển cục bộ

Đôi khi cần chuyển các lệnh nhập vào một hàm hoặc lớp để tránh các vấn đề do import vòng (circular import). Gordon McMillan nói:

   Import vòng không có vấn đề gì khi cả hai module đều sử dụng dạng import "import <module>". Chúng sẽ thất bại khi module thứ hai muốn lấy một tên từ module thứ nhất ("from module import name") và lệnh import nằm ở cấp cao nhất. Đó là vì các tên trong module thứ nhất chưa khả dụng, do module thứ nhất đang bận nhập module thứ hai.

Trong trường hợp này, nếu module thứ hai chỉ được sử dụng trong một hàm, bạn có thể dễ dàng chuyển lệnh import vào hàm đó. Đến khi lệnh import được gọi, module thứ nhất đã hoàn tất việc khởi tạo, và module thứ hai có thể thực hiện import của mình.

Cũng có thể cần đưa các câu lệnh import ra khỏi cấp cao nhất của mã nếu một số mô-đun phụ thuộc vào nền tảng. Trong trường hợp đó, thậm chí có thể không thể import tất cả các mô-đun ở đầu tệp. Khi đó, import các mô-đun phù hợp trong phần mã tương ứng với từng nền tảng là một lựa chọn tốt.

Chỉ chuyển các câu lệnh import vào phạm vi cục bộ, chẳng hạn như bên trong định nghĩa hàm, nếu cần làm vậy để giải quyết một vấn đề như tránh import vòng hoặc đang cố giảm thời gian khởi tạo của mô-đun. Kỹ thuật này đặc biệt hữu ích nếu nhiều import không cần thiết, tùy thuộc vào cách chương trình thực thi. Bạn cũng có thể muốn chuyển các câu lệnh import vào một hàm nếu các mô-đun chỉ được sử dụng trong hàm đó. Lưu ý rằng việc tải một mô-đun lần đầu có thể tốn kém do quá trình khởi tạo mô-đun chỉ diễn ra một lần, nhưng việc tải một mô-đun nhiều lần gần như không tốn chi phí, chỉ cần thực hiện một vài lần tra cứu dictionary. Ngay cả khi tên mô-đun đã ra khỏi phạm vi, mô-đun có thể vẫn khả dụng trong :data:`sys.modules`.


Tại sao các giá trị mặc định lại được dùng chung giữa các đối tượng?
--------------------------------------------------------------------

Loại lỗi này thường khiến những lập trình viên mới vào nghề mắc phải. Hãy xét hàm này::

   def foo(mydict={}):  # Nguy hiểm: tham chiếu dùng chung đến một dict cho mọi lần gọi
       ... compute something ...
       mydict[key] = value
       return mydict

Lần đầu gọi hàm này, ``mydict`` chứa một mục duy nhất. Lần thứ hai, ``mydict`` chứa hai mục vì khi ``foo()`` bắt đầu thực thi, ``mydict`` đã có sẵn một mục.

Thông thường, người ta kỳ vọng rằng một lần gọi hàm sẽ tạo các đối tượng mới cho những giá trị mặc định. Nhưng thực tế không phải vậy. Các giá trị mặc định được tạo đúng một lần, khi hàm được định nghĩa. Nếu đối tượng đó bị thay đổi, như dictionary trong ví dụ này, các lần gọi hàm sau đó sẽ tham chiếu đến đối tượng đã thay đổi này.

Theo định nghĩa, các đối tượng bất biến như số, chuỗi, tuple và ``None`` không thể bị thay đổi. Việc thay đổi các đối tượng khả biến như dictionary, list và các instance của class có thể dẫn đến nhầm lẫn.

Vì đặc điểm này, một thực hành lập trình tốt là không sử dụng các đối tượng khả biến làm giá trị mặc định. Thay vào đó, hãy dùng ``None`` làm giá trị mặc định và bên trong hàm, kiểm tra xem tham số có phải là ``None`` hay không rồi tạo một list/dictionary/đối tượng tương ứng mới nếu đúng như vậy. Ví dụ, đừng viết::

   def foo(mydict={}):
       ...

mà hãy::

   def foo(mydict=None):
       if mydict is None:
           mydict = {}  # Tạo dict mới cho namespace cục bộ

Đặc điểm này có thể hữu ích. Khi bạn có một hàm tốn nhiều thời gian để tính toán, một kỹ thuật phổ biến là lưu vào cache các tham số và giá trị kết quả của mỗi lần gọi hàm, rồi trả về giá trị đã lưu trong cache nếu cùng một giá trị được yêu cầu lại. Kỹ thuật này được gọi là "memoizing" và có thể được triển khai như sau::

   # Caller chỉ có thể cung cấp hai tham số và tùy chọn truyền _cache bằng keyword
   def expensive(arg1, arg2, *, _cache={}):
       if (arg1, arg2) in _cache:
           return _cache[(arg1, arg2)]

       # Tính giá trị
       result = ... expensive computation ...
       _cache[(arg1, arg2)] = result           # Lưu kết quả vào cache
       return result

Bạn có thể sử dụng một biến global chứa dictionary thay cho giá trị mặc định; đó là vấn đề về sở thích.


Làm cách nào để truyền các tham số tùy chọn hoặc tham số keyword từ một hàm này sang một hàm khác?
--------------------------------------------------------------------------------------------------

Thu thập các đối số bằng các specifier ``*`` và ``**`` trong danh sách tham số của hàm; thao tác này cung cấp cho bạn các đối số vị trí dưới dạng tuple và các đối số keyword dưới dạng dictionary. Sau đó, bạn có thể truyền các đối số này khi gọi một hàm khác bằng cách sử dụng ``*`` và ``**``::

   def f(x, *args, **kwargs):
       ...
       kwargs['width'] = '14.3c'
       ...
       g(x, *args, **kwargs)


.. index::
   single: argument; difference from parameter
   single: parameter; difference from argument

.. _faq-argument-vs-parameter:

Sự khác biệt giữa đối số và tham số là gì?
------------------------------------------

:term:`Tham số <parameter>` được xác định bởi các tên xuất hiện trong phần định nghĩa hàm, trong khi :term:`đối số <argument>` là các giá trị thực sự được truyền cho hàm khi gọi hàm đó. Tham số xác định hàm sẽ nhận loại gì
:term:`loại đối số <parameter>` nào. Ví dụ, với định nghĩa hàm::

   def func(foo, bar=None, **kwargs):
       pass

*foo*, *bar* và *kwargs* là các parameter của ``func``. Tuy nhiên, khi gọi ``func``, chẳng hạn::

   func(42, bar=314, extra=somevar)

các giá trị ``42``, ``314`` và ``somevar`` là các argument.


Tại sao việc thay đổi list 'y' cũng làm thay đổi list 'x'?
----------------------------------------------------------

Nếu bạn viết code như sau::

   >>> x = []
   >>> y = x
   >>> y.append(10)
   >>> y
   [10]
   >>> x
   [10]

có thể bạn thắc mắc tại sao việc thêm một phần tử vào ``y`` cũng làm thay đổi ``x``.

Có hai yếu tố dẫn đến kết quả này:

1) Các biến chỉ đơn giản là những tên tham chiếu đến các object. Việc thực hiện ``y = x`` không tạo bản sao của list -- nó tạo một biến mới ``y`` tham chiếu đến cùng object mà ``x`` tham chiếu. Điều này có nghĩa là chỉ có một object (list), và cả ``x`` lẫn ``y`` đều tham chiếu đến object đó.
2) Lists are :term:`mutable`, which means that you can change their content.

Sau lệnh gọi :meth:`~sequence.append`, nội dung của đối tượng có thể thay đổi đã đổi từ ``[]`` thành ``[10]``. Vì cả hai biến đều tham chiếu đến cùng một đối tượng, việc sử dụng một trong hai tên sẽ truy cập giá trị đã sửa đổi ``[10]``.

Nếu thay vào đó, chúng ta gán một đối tượng bất biến cho ``x``::

   >>> x = 5  # số nguyên là bất biến
   >>> y = x
   >>> x = x + 1  # 5 không thể bị thay đổi, ở đây chúng ta đang tạo một đối tượng mới
   >>> x
   6
   >>> y
   5

chúng ta có thể thấy rằng trong trường hợp này, ``x`` và ``y`` không còn bằng nhau nữa. Điều này là do các số nguyên :term:`immutable`, và khi thực hiện ``x = x + 1``, chúng ta không thay đổi số nguyên ``5`` bằng cách tăng giá trị của nó; thay vào đó, chúng ta tạo một đối tượng mới (số nguyên ``6``) và gán nó cho ``x`` (tức là thay đổi đối tượng mà ``x`` tham chiếu đến). Sau phép gán này, chúng ta có hai đối tượng (các số nguyên ``6`` và ``5``) và hai biến tham chiếu đến chúng (``x`` giờ đây tham chiếu đến ``6``, nhưng ``y`` vẫn tham chiếu đến ``5``).

Một số thao tác (ví dụ ``y.append(10)`` và ``y.sort()``) làm thay đổi đối tượng, trong khi các thao tác trông tương tự trên bề mặt (ví dụ ``y = y + [10]`` và :func:`sorted(y) <sorted>`) lại tạo một đối tượng mới. Nhìn chung trong Python (và trong mọi trường hợp trong standard library), một method làm thay đổi đối tượng sẽ trả về ``None`` để giúp tránh nhầm lẫn giữa hai loại thao tác này. Vì vậy, nếu bạn vô tình viết ``y.sort()`` với suy nghĩ rằng nó sẽ cung cấp cho bạn một bản sao đã được sắp xếp của ``y``, thì thay vào đó bạn sẽ nhận được ``None``, điều này có thể khiến chương trình của bạn phát sinh một lỗi dễ chẩn đoán.

Tuy nhiên, có một nhóm phép toán mà cùng một phép toán đôi khi có hành vi khác nhau với các kiểu khác nhau: các toán tử phép gán kết hợp. Ví dụ, ``+=`` thay đổi các list nhưng không thay đổi tuple hoặc int (``a_list += [1, 2, 3]`` tương đương với ``a_list.extend([1, 2, 3])`` và thay đổi ``a_list``, trong khi ``some_tuple += (1, 2, 3)`` và ``some_int += 1`` tạo các đối tượng mới).

Nói cách khác:

* Nếu có một đối tượng có thể thay đổi (chẳng hạn như :class:`list`, :class:`dict`, :class:`set`), ta có thể sử dụng một số phép toán cụ thể để thay đổi nó, và tất cả các biến tham chiếu đến nó sẽ thấy sự thay đổi đó.
* Nếu có một đối tượng bất biến (chẳng hạn như :class:`str`, :class:`int`, :class:`tuple`), tất cả các biến tham chiếu đến nó sẽ luôn thấy cùng một giá trị, nhưng các phép toán biến đổi giá trị đó thành một giá trị mới luôn trả về một đối tượng mới.

Nếu muốn biết hai biến có tham chiếu đến cùng một đối tượng hay không, bạn có thể sử dụng toán tử :keyword:`is` hoặc hàm tích hợp sẵn :func:`id`.


Làm thế nào để viết một hàm có tham số đầu ra (truyền tham chiếu)?
------------------------------------------------------------------

Hãy nhớ rằng các đối số được truyền bằng phép gán trong Python. Vì phép gán chỉ tạo các tham chiếu đến đối tượng, không có bí danh nào giữa tên đối số trong hàm gọi và hàm được gọi, nên không có cơ chế truyền tham chiếu. Bạn có thể đạt được hiệu ứng mong muốn bằng một số cách.

1) Bằng cách trả về một tuple chứa các kết quả::

      >>> def func1(a, b):
      ...     a = 'new-value'        # a và b là các tên cục bộ
      ...     b = b + 1              # được gán cho các đối tượng mới
      ...     return a, b            # trả về các giá trị mới
      ...
      >>> x, y = 'old-value', 99
      >>> func1(x, y)
      ('new-value', 100)

   This is almost always the clearest solution.

2) Bằng cách sử dụng các biến toàn cục. Cách này không an toàn với thread và không được khuyến nghị.

3) Bằng cách truyền một đối tượng có thể thay đổi (thay đổi trực tiếp tại chỗ)::

      >>> def func2(a):
      ...     a[0] = 'new-value'     # 'a' tham chiếu đến một mutable list
      ...     a[1] = a[1] + 1        # thay đổi một đối tượng dùng chung
      ...
      >>> args = ['old-value', 99]
      >>> func2(args)
      >>> args
      ['new-value', 100]

4) Bằng cách truyền vào một dictionary được biến đổi::

      >>> def func3(args):
      ...     args['a'] = 'new-value'     # args là một dictionary có thể biến đổi
      ...     args['b'] = args['b'] + 1   # thay đổi trực tiếp tại chỗ
      ...
      >>> args = {'a': 'old-value', 'b': 99}
      >>> func3(args)
      >>> args
      {'a': 'new-value', 'b': 100}

5) Hoặc đóng gói các giá trị trong một thực thể lớp::

      >>> class Namespace:
      ...     def __init__(self, /, **args):
      ...         for key, value in args.items():
      ...             setattr(self, key, value)
      ...
      >>> def func4(args):
      ...     args.a = 'new-value'        # args là một Namespace có thể biến đổi
      ...     args.b = args.b + 1         # thay đổi đối tượng trực tiếp tại chỗ
      ...
      >>> args = Namespace(a='old-value', b=99)
      >>> func4(args)
      >>> vars(args)
      {'a': 'new-value', 'b': 100}


   There's almost never a good reason to get this complicated.

Lựa chọn tốt nhất là trả về một tuple chứa nhiều kết quả.


Làm thế nào để tạo một higher-order function trong Python?
----------------------------------------------------------

Bạn có hai lựa chọn: sử dụng phạm vi lồng nhau hoặc sử dụng các callable object. Ví dụ, giả sử bạn muốn định nghĩa ``linear(a,b)``, hàm này trả về một function ``f(x)`` để tính giá trị ``a*x+b``. Sử dụng phạm vi lồng nhau::

   def linear(a, b):
       def result(x):
           return a * x + b
       return result

Hoặc sử dụng một callable object::

   class linear:

       def __init__(self, a, b):
           self.a, self.b = a, b

       def __call__(self, x):
           return self.a * x + self.b

Trong cả hai trường hợp,::

   taxes = linear(0.3, 2)

sẽ cho một callable object trong đó ``taxes(10e6) == 0.3 * 10e6 + 2``.

Cách tiếp cận bằng callable object có nhược điểm là chậm hơn một chút và tạo ra code dài hơn đôi chút. Tuy nhiên, lưu ý rằng một tập hợp các callable có thể dùng chung signature thông qua inheritance::

   class exponential(linear):
       # __init__ được kế thừa
       def __call__(self, x):
           return self.a * (x ** self.b)

Đối tượng có thể đóng gói trạng thái cho nhiều phương thức::

   class counter:

       value = 0

       def set(self, x):
           self.value = x

       def up(self):
           self.value = self.value + 1

       def down(self):
           self.value = self.value - 1

   count = counter()
   inc, dec, reset = count.up, count.down, count.set

Ở đây, ``inc()``, ``dec()`` và ``reset()`` hoạt động như các hàm dùng chung một biến đếm.


Làm thế nào để sao chép một đối tượng trong Python?
---------------------------------------------------

Nhìn chung, hãy thử :func:`copy.copy` hoặc :func:`copy.deepcopy` trong trường hợp thông thường. Không phải mọi đối tượng đều có thể được sao chép, nhưng hầu hết đều có thể.

Một số đối tượng có thể được sao chép dễ dàng hơn. Từ điển có một phương thức :meth:`~dict.copy`::

   newdict = olddict.copy()

Có thể sao chép các sequence bằng cách cắt lát::

   new_l = l[:]


Làm thế nào để tìm các phương thức hoặc thuộc tính của một đối tượng?
---------------------------------------------------------------------

Đối với một instance ``x`` của một class do người dùng định nghĩa, :func:`dir(x) <dir>` trả về một danh sách được sắp xếp theo thứ tự bảng chữ cái gồm các tên của các thuộc tính và phương thức của instance, cùng các thuộc tính và phương thức được định nghĩa bởi class đó.


Làm thế nào để code của tôi phát hiện tên của một đối tượng?
------------------------------------------------------------

Nói chung là không thể, vì các đối tượng thực sự không có tên. Về bản chất, phép gán luôn liên kết một tên với một giá trị; điều tương tự cũng đúng với các câu lệnh ``def`` và ``class``, nhưng trong trường hợp đó, giá trị là một callable. Hãy xem đoạn code sau::

   >>> class A:
   ...     pass
   ...
   >>> B = A
   >>> a = B()
   >>> b = a
   >>> print(b)
   <__main__.A object at 0x16D07CC>
   >>> print(a)
   <__main__.A object at 0x16D07CC>

Có thể nói class có một tên: mặc dù nó được liên kết với hai tên và được gọi thông qua tên ``B``, instance được tạo ra vẫn được xác định là một instance của class ``A``. Tuy nhiên, không thể nói instance đó có tên là ``a`` hay ``b``, vì cả hai tên đều được liên kết với cùng một giá trị.

Nói chung, code của bạn không cần phải "biết tên" của các giá trị cụ thể. Trừ khi bạn đang chủ ý viết các chương trình introspection, điều này thường cho thấy rằng thay đổi cách tiếp cận có thể sẽ hữu ích.

Trong comp.lang.python, Fredrik Lundh từng đưa ra một phép so sánh rất hay để trả lời câu hỏi này:

   Tương tự như khi bạn tìm tên của con mèo mà bạn thấy trên hiên nhà: bản thân con mèo (object) không thể cho bạn biết tên của nó, và nó cũng không thực sự quan tâm -- vì vậy cách duy nhất để biết nó được gọi là gì là hỏi tất cả hàng xóm (namespaces) xem đó có phải là mèo (object) của họ không...

   ....và đừng ngạc nhiên nếu bạn phát hiện ra rằng nó được biết đến bằng nhiều tên, hoặc hoàn toàn không có tên nào!


Có gì đáng chú ý về độ ưu tiên của toán tử dấu phẩy?
----------------------------------------------------

Dấu phẩy không phải là một toán tử trong Python. Hãy xem xét phiên làm việc này::

    >>> "a" in "b", "a"
    (False, 'a')

Vì dấu phẩy không phải là một toán tử mà là dấu phân cách giữa các biểu thức, đoạn trên được đánh giá như thể bạn đã nhập::

    ("a" in "b"), "a"

không::

    "a" in ("b", "a")

Điều tương tự cũng đúng với các toán tử gán khác nhau (``=``, ``+=``, vân vân). Chúng không thực sự là các toán tử mà là các dấu phân cách cú pháp trong các câu lệnh gán.


Có toán tử ba ngôi "?:" tương đương với C không?
------------------------------------------------

Có. Cú pháp như sau::

   [on_true] if [expression] else [on_false]

   x, y = 50, 25
   small = x if x < y else y

Trước khi cú pháp này được giới thiệu trong Python 2.5, một cách viết phổ biến là sử dụng các toán tử logic::

   [expression] and [on_true] or [on_false]

Tuy nhiên, cách viết này không an toàn, vì nó có thể cho kết quả sai khi *on_true* có giá trị boolean là false. Do đó, luôn nên sử dụng dạng ``... if ... else ...``.


Có thể viết các câu lệnh một dòng làm rối trong Python không?
-------------------------------------------------------------

Có. Thông thường, người ta thực hiện việc này bằng cách lồng :keyword:`lambda` vào trong
:keyword:`!lambda`. Xem ba ví dụ sau, được điều chỉnh đôi chút từ Ulf Bartelt::

   from functools import reduce

   # Các số nguyên tố < 1000
   print(list(filter(None,map(lambda y:y*reduce(lambda x,y:x*y!=0,
   map(lambda x,y=y:y%x,range(2,int(pow(y,0.5)+1))),1),range(2,1000)))))

   # 10 số Fibonacci đầu tiên
   print(list(map(lambda x,f=lambda x,f:(f(x-1,f)+f(x-2,f)) if x>1 else 1:
   f(x,f), range(10))))

   # Tập Mandelbrot
   print((lambda Ru,Ro,Iu,Io,IM,Sx,Sy:reduce(lambda x,y:x+'\n'+y,map(lambda y,
   Iu=Iu,Io=Io,Ru=Ru,Ro=Ro,Sy=Sy,L=lambda yc,Iu=Iu,Io=Io,Ru=Ru,Ro=Ro,i=IM,
   Sx=Sx,Sy=Sy:reduce(lambda x,y:x+y,map(lambda x,xc=Ru,yc=yc,Ru=Ru,Ro=Ro,
   i=i,Sx=Sx,F=lambda xc,yc,x,y,k,f=lambda xc,yc,x,y,k,f:(k<=0)or (x*x+y*y
   >=4.0) or 1+f(xc,yc,x*x-y*y+xc,2.0*x*y+yc,k-1,f):f(xc,yc,x,y,k,f):chr(
   64+F(Ru+x*(Ro-Ru)/Sx,yc,0,0,i)),range(Sx))):L(Iu+y*(Io-Iu)/Sy),range(Sy
   ))))(-2.1, 0.7, -1.2, 1.2, 30, 80, 24))
   #    \___ ___/  \___ ___/  |   |   |__ dòng trên màn hình
   #        V          V      |   |______ cột trên màn hình
   #        |          |      |__________ giá trị tối đa của "iterations"
   #        |          |_________________ phạm vi trên trục y
   #        |____________________________ khoảng trên trục x

Đừng thử làm theo ở nhà nhé, các bạn nhỏ!


.. _faq-positional-only-arguments:

Dấu gạch chéo(/) trong danh sách tham số của một hàm có ý nghĩa gì?
-------------------------------------------------------------------

Dấu gạch chéo trong danh sách đối số của một hàm cho biết các tham số đứng trước nó chỉ có thể được truyền theo vị trí. Các tham số chỉ có thể được truyền theo vị trí là những tham số không có tên có thể sử dụng từ bên ngoài. Khi gọi một hàm chấp nhận các tham số chỉ có thể được truyền theo vị trí, các đối số được ánh xạ tới các tham số chỉ dựa trên vị trí của chúng. Ví dụ: :func:`divmod` là một hàm chấp nhận các tham số chỉ có thể được truyền theo vị trí. Tài liệu của hàm có dạng như sau::

   >>> help(divmod)
   Help on built-in function divmod in module builtins:

   divmod(x, y, /)
       Return the tuple (x//y, x%y).  Invariant: div*y + mod == x.

Dấu gạch chéo ở cuối danh sách tham số có nghĩa là cả hai tham số đều chỉ có thể được truyền theo vị trí. Do đó, việc gọi :func:`divmod` bằng các đối số từ khóa sẽ dẫn đến lỗi::

   >>> divmod(x=3, y=4)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: divmod() takes no keyword arguments


Số và chuỗi
===========

Làm thế nào để chỉ định các số nguyên thập lục phân và bát phân?
----------------------------------------------------------------

Để chỉ định một chữ số bát phân, hãy đặt số 0 trước giá trị bát phân, rồi thêm chữ "o" thường hoặc hoa. Ví dụ, để đặt biến "a" thành giá trị bát phân "10" (8 ở hệ thập phân), hãy nhập::

   >>> a = 0o10
   >>> a
   8

Hệ thập lục phân cũng đơn giản như vậy. Chỉ cần đặt số 0 trước số thập lục phân, rồi thêm chữ "x" thường hoặc hoa. Các chữ số thập lục phân có thể được viết thường hoặc hoa. Ví dụ, trong trình thông dịch Python::

   >>> a = 0xa5
   >>> a
   165
   >>> b = 0XB2
   >>> b
   178


Tại sao -22 // 10 lại trả về -3?
--------------------------------

Điều này chủ yếu xuất phát từ mong muốn ``i % j`` có cùng dấu với ``j``. Nếu bạn muốn điều đó, đồng thời cũng muốn::

    i == (i // j) * j + (i % j)

thì phép chia số nguyên phải trả về phần nguyên dưới. C cũng yêu cầu đẳng thức đó đúng, và khi đó các compiler cắt ngắn ``i // j`` cần làm cho ``i % j`` có cùng dấu với ``i``.

Có rất ít trường hợp sử dụng thực tế cho ``i % j`` khi ``j`` là số âm. Khi ``j`` là số dương thì có rất nhiều, và trong hầu như mọi trường hợp đó, việc ``i % j`` là ``>= 0`` sẽ hữu ích hơn. Nếu đồng hồ hiện 10 giờ bây giờ, thì 200 giờ trước là mấy giờ? ``-190 % 12 == 2`` rất hữu ích; ``-190 % 12 == -10`` là một lỗi đang chực chờ gây rắc rối.


Làm thế nào để lấy thuộc tính của literal int thay vì gặp SyntaxError?
----------------------------------------------------------------------

Cố gắng tra cứu thuộc tính literal ``int`` theo cách thông thường sẽ gây ra :exc:`SyntaxError` vì dấu chấm được hiểu là dấu thập phân::

   >>> 1.__class__
     File "<stdin>", line 1
     1.__class__
      ^
   SyntaxError: invalid decimal literal

Giải pháp là tách literal khỏi dấu chấm bằng một khoảng trắng hoặc dấu ngoặc đơn.

   >>> 1 .__class__
   <class 'int'>
   >>> (1).__class__
   <class 'int'>


Làm thế nào để chuyển đổi một chuỗi thành một số?
-------------------------------------------------

Đối với số nguyên, hãy sử dụng hàm dựng kiểu tích hợp sẵn :func:`int`, chẳng hạn như ``int('144') == 144``. Tương tự, :func:`float` chuyển đổi thành số dấu phẩy động, chẳng hạn như ``float('144') == 144.0``.

Theo mặc định, các hàm này diễn giải số ở dạng thập phân, vì vậy ``int('0144') == 144`` cho kết quả đúng, còn ``int('0x144')`` gây ra :exc:`ValueError`. ``int(string, base)`` nhận cơ số cần chuyển đổi từ đó làm đối số tùy chọn thứ hai, vì vậy ``int( '0x144', 16) == 324``. Nếu cơ số được chỉ định là 0, số sẽ được diễn giải theo các quy tắc của Python: tiền tố '0o' cho biết số bát phân, còn '0x' cho biết số thập lục phân.

Không sử dụng hàm tích hợp sẵn :func:`eval` nếu tất cả những gì bạn cần chỉ là chuyển đổi chuỗi thành số. :func:`eval` sẽ chậm hơn đáng kể và gây ra rủi ro bảo mật: ai đó có thể truyền cho bạn một biểu thức Python có thể gây ra các tác dụng phụ không mong muốn. Chẳng hạn, ai đó có thể truyền ``__import__('os').system("rm -rf $HOME")``, thao tác này sẽ xóa thư mục chính của bạn.

:func:`eval` cũng có tác dụng diễn giải các số dưới dạng biểu thức Python, vì vậy, chẳng hạn, ``eval('09')`` gây ra lỗi cú pháp vì Python không cho phép số '0' đứng đầu trong một số thập phân (ngoại trừ '0').


Làm thế nào để chuyển một số thành chuỗi?
-----------------------------------------

Ví dụ, để chuyển số ``144`` thành chuỗi ``'144'``, hãy sử dụng hàm dựng kiểu tích hợp sẵn :func:`str`. Nếu muốn biểu diễn dưới dạng thập lục phân hoặc bát phân, hãy sử dụng các hàm tích hợp sẵn :func:`hex` hoặc :func:`oct`. Để định dạng nâng cao, hãy xem các phần :ref:`f-strings` và :ref:`formatstrings`. Ví dụ, ``"{:04d}".format(144)`` cho kết quả là ``'0144'`` và ``"{:.3f}".format(1.0/3.0)`` cho kết quả là ``'0.333'``.


Làm thế nào để sửa đổi một chuỗi tại chỗ?
-----------------------------------------

Bạn không thể làm vậy vì chuỗi là bất biến. Trong hầu hết các trường hợp, bạn chỉ nên tạo một chuỗi mới từ các phần khác nhau mà bạn muốn ghép lại. Tuy nhiên, nếu cần một đối tượng có khả năng sửa đổi dữ liệu Unicode tại chỗ, hãy thử sử dụng đối tượng :class:`io.StringIO` hoặc module :mod:`array`::

   >>> import io
   >>> s = "Hello, world"
   >>> sio = io.StringIO(s)
   >>> sio.getvalue()
   'Hello, world'
   >>> sio.seek(7)
   7
   >>> sio.write("there!")
   6
   >>> sio.getvalue()
   'Hello, there!'

   >>> import array
   >>> a = array.array('w', s)
   >>> print(a)
   array('w', 'Hello, world')
   >>> a[0] = 'y'
   >>> print(a)
   array('w', 'yello, world')
   >>> a.tounicode()
   'yello, world'


Làm thế nào để sử dụng chuỗi để gọi các hàm/phương thức?
--------------------------------------------------------

Có nhiều kỹ thuật khác nhau.

* Cách tốt nhất là sử dụng một dictionary ánh xạ các chuỗi tới các hàm. Ưu điểm chính của kỹ thuật này là các chuỗi không cần phải trùng với tên của các hàm. Đây cũng là kỹ thuật chính được sử dụng để mô phỏng cấu trúc case::

     def a():
         pass

     def b():
         pass

     dispatch = {'go': a, 'stop': b}  # Lưu ý không có dấu ngoặc đơn khi gọi các hàm

     dispatch[get_input()]()  # Lưu ý dấu ngoặc đơn ở cuối để gọi hàm

* Sử dụng hàm tích hợp sẵn :func:`getattr`::

     import foo
     getattr(foo, 'bar')()

  Note that :func:`getattr` works on any object, including classes, class
  instances, modules, and so on.

  This is used in several places in the standard library, like this::

     class Foo:
         def do_foo(self):
             ...

         def do_bar(self):
             ...

     f = getattr(foo_instance, 'do_' + opname)
     f()


* Sử dụng :func:`locals` để phân giải tên hàm::

     def myFunc():
         print("hello")

     fname = "myFunc"

     f = locals()[fname]
     f()


Có hàm tương đương với ``chomp()`` của Perl để xóa các ký tự xuống dòng ở cuối chuỗi không?
-------------------------------------------------------------------------------------------

Bạn có thể sử dụng ``S.rstrip("\r\n")`` để xóa mọi lần xuất hiện của bất kỳ ký tự kết thúc dòng nào ở cuối chuỗi ``S`` mà không xóa các khoảng trắng khác ở cuối. Nếu chuỗi ``S`` biểu diễn nhiều hơn một dòng, với nhiều dòng trống ở cuối, các ký tự kết thúc dòng của tất cả các dòng trống sẽ bị xóa::

   >>> lines = ("line 1 \r\n"
   ...          "\r\n"
   ...          "\r\n")
   >>> lines.rstrip("\n\r")
   'line 1 '

Vì cách này thường chỉ cần thiết khi đọc văn bản từng dòng một, sử dụng ``S.rstrip()`` theo cách này sẽ hoạt động hiệu quả.


Có tương đương với ``scanf()`` hoặc ``sscanf()`` không?
-------------------------------------------------------

Không hẳn là vậy.

Để phân tích cú pháp đầu vào đơn giản, cách dễ nhất thường là tách dòng thành các từ được phân cách bằng khoảng trắng bằng phương thức :meth:`~str.split` của các đối tượng chuỗi, sau đó chuyển đổi các chuỗi thập phân thành giá trị số bằng :func:`int` hoặc
:func:`float`.  :meth:`!split` hỗ trợ tham số "sep" tùy chọn, hữu ích nếu dòng sử dụng một ký tự khác khoảng trắng làm dấu phân cách.

Để phân tích cú pháp đầu vào phức tạp hơn, biểu thức chính quy mạnh hơn ``sscanf`` của C và phù hợp hơn với tác vụ này.


Lỗi ``UnicodeDecodeError`` hoặc ``UnicodeEncodeError`` có nghĩa là gì?
----------------------------------------------------------------------

Xem :ref:`unicode-howto`.


.. _faq-programming-raw-string-backslash:

Tôi có thể kết thúc chuỗi raw bằng một số lẻ dấu gạch chéo ngược không?
-----------------------------------------------------------------------

Chuỗi raw kết thúc bằng một số lẻ dấu gạch chéo ngược sẽ escape dấu ngoặc kép của chuỗi::

   >>> r'C:\this\will\not\work\'
     File "<stdin>", line 1
       r'C:\this\will\not\work\'
       ^
   SyntaxError: unterminated string literal (detected at line 1)

Có một số cách khắc phục vấn đề này. Một cách là sử dụng các chuỗi thông thường và nhân đôi dấu gạch chéo ngược::

   >>> 'C:\\this\\will\\work\\'
   'C:\\this\\will\\work\\'

Một cách khác là nối một chuỗi thông thường chứa dấu gạch chéo ngược đã được escape vào chuỗi raw::

   >>> r'C:\this\will\work' '\\'
   'C:\\this\\will\\work\\'

Bạn cũng có thể sử dụng :func:`os.path.join` để thêm một dấu gạch chéo ngược trên Windows::

   >>> os.path.join(r'C:\this\will\work', '')
   'C:\\this\\will\\work\\'

Lưu ý rằng mặc dù dấu gạch chéo ngược sẽ "escape" dấu ngoặc kép nhằm xác định vị trí kết thúc chuỗi raw, không có thao tác escape nào xảy ra khi diễn giải giá trị của chuỗi raw. Nghĩa là dấu gạch chéo ngược vẫn hiện diện trong giá trị của chuỗi raw::

   >>> r'backslash\'preserved'
   "backslash\\'preserved"

Xem thêm đặc tả trong :ref:`tài liệu tham chiếu ngôn ngữ <strings>`.


Hiệu năng
=========

Chương trình của tôi quá chậm. Làm thế nào để tăng tốc chương trình?
--------------------------------------------------------------------

Nhìn chung, đây là một vấn đề khó. Trước tiên, dưới đây là danh sách những điều cần ghi nhớ trước khi tìm hiểu sâu hơn:

* Đặc tính hiệu năng khác nhau giữa các bản triển khai Python. Câu hỏi thường gặp này tập trung vào :term:`CPython`.
* Hành vi có thể khác nhau giữa các hệ điều hành, đặc biệt khi nói đến I/O hoặc đa luồng.
* Bạn luôn nên xác định các điểm nóng trong chương trình *trước* khi cố gắng tối ưu hóa bất kỳ đoạn mã nào (xem module :mod:`profile`).
* Việc viết các tập lệnh benchmark sẽ cho phép bạn nhanh chóng lặp lại quy trình khi tìm kiếm cải tiến (xem module :mod:`timeit`).
* Bạn rất nên có độ bao phủ mã tốt (thông qua kiểm thử đơn vị hoặc bất kỳ kỹ thuật nào khác) trước khi có khả năng đưa vào các hồi quy bị che giấu trong những tối ưu hóa phức tạp.

Dù vậy, có rất nhiều thủ thuật để tăng tốc mã Python. Dưới đây là một số nguyên tắc chung có thể giúp bạn đạt được mức hiệu năng chấp nhận được:

* Làm cho các thuật toán của bạn nhanh hơn (hoặc chuyển sang các thuật toán nhanh hơn) có thể mang lại lợi ích lớn hơn nhiều so với việc cố rải các thủ thuật vi tối ưu hóa khắp mã của bạn.

* Hãy sử dụng đúng cấu trúc dữ liệu. Hãy đọc tài liệu về :ref:`bltin-types` và module :mod:`collections`.

* Khi thư viện chuẩn cung cấp một primitive để thực hiện việc gì đó, nhiều khả năng (dù không được đảm bảo) primitive đó sẽ nhanh hơn bất kỳ giải pháp thay thế nào bạn có thể nghĩ ra. Điều này càng đúng đối với các primitive được viết bằng C, chẳng hạn như các hàm built-in và một số kiểu mở rộng. Ví dụ, hãy nhớ sử dụng phương thức built-in :meth:`list.sort` hoặc hàm :func:`sorted` liên quan để thực hiện việc sắp xếp (và xem :ref:`sortinghowto` để biết các ví dụ về cách sử dụng tương đối nâng cao).

* Các abstraction thường tạo ra những lớp trung gian và buộc trình thông dịch phải làm việc nhiều hơn. Nếu các lớp trung gian nhiều hơn khối lượng công việc hữu ích được thực hiện, chương trình của bạn sẽ chậm hơn. Bạn nên tránh abstraction quá mức, đặc biệt dưới dạng các hàm hoặc phương thức nhỏ (những thành phần này cũng thường làm giảm khả năng dễ đọc).

Nếu bạn đã đạt đến giới hạn mà Python thuần túy cho phép, có những công cụ giúp bạn tiến xa hơn. Ví dụ, `Cython <https://cython.org>`_ có thể biên dịch một phiên bản mã Python được sửa đổi đôi chút thành một extension C và có thể được sử dụng trên nhiều nền tảng khác nhau. Cython có thể tận dụng việc biên dịch (và các chú thích kiểu tùy chọn) để làm cho mã của bạn nhanh hơn đáng kể so với khi được thông dịch. Nếu tự tin vào kỹ năng lập trình C của mình, bạn cũng có thể :ref:`tự viết một extension module bằng C <extending-index>`.

.. seealso::
   Trang wiki dành riêng cho `mẹo về hiệu năng <https://wiki.python.org/moin/PythonSpeed/PerformanceTips>`_.


.. _efficient_string_concatenation:

Cách hiệu quả nhất để nối nhiều chuỗi với nhau là gì?
-----------------------------------------------------

Các đối tượng :class:`str` và :class:`bytes` là bất biến, vì vậy việc nối nhiều chuỗi với nhau không hiệu quả vì mỗi lần nối lại tạo một đối tượng mới. Trong trường hợp tổng quát, chi phí thời gian chạy có độ phức tạp bậc hai theo tổng độ dài chuỗi. Xem :ref:`time-complexity` để biết thêm thông tin.

Để tích lũy nhiều đối tượng :class:`str`, cách viết được khuyến nghị là đưa chúng vào một danh sách và gọi :meth:`str.join` ở cuối::

   chunks = []
   for s in my_strings:
       chunks.append(s)
   result = ''.join(chunks)

(Một cách viết khác cũng khá hiệu quả là sử dụng :class:`io.StringIO`.)

Để tích lũy nhiều đối tượng :class:`bytes`, cách viết được khuyến nghị là mở rộng một đối tượng :class:`bytearray` bằng phép nối tại chỗ (toán tử ``+=``)::

   result = bytearray()
   for b in my_bytes_objects:
       result += b


Các sequence (tuple/list)
=========================

Làm thế nào để chuyển đổi giữa tuple và list?
---------------------------------------------

Hàm khởi tạo kiểu ``tuple(seq)`` chuyển đổi mọi sequence (thực ra là mọi iterable) thành một tuple có cùng các phần tử theo cùng thứ tự.

Ví dụ, ``tuple([1, 2, 3])`` cho kết quả ``(1, 2, 3)`` và ``tuple('abc')`` cho kết quả ``('a', 'b', 'c')``. Nếu đối số là một tuple, hàm không tạo bản sao mà trả về chính đối tượng đó, vì vậy gọi :func:`tuple` là một thao tác rẻ khi bạn không chắc một đối tượng đã là tuple hay chưa.

Hàm khởi tạo kiểu ``list(seq)`` chuyển đổi mọi sequence hoặc iterable thành một list có cùng các phần tử theo cùng thứ tự. Ví dụ, ``list((1, 2, 3))`` cho kết quả ``[1, 2, 3]`` và ``list('abc')`` cho kết quả ``['a', 'b', 'c']``. Nếu đối số là một list, hàm sẽ tạo một bản sao, giống như ``seq[:]``.


Chỉ mục âm là gì?
-----------------

Các sequence trong Python được lập chỉ mục bằng số dương và số âm. Với các số dương, 0 là chỉ mục đầu tiên, 1 là chỉ mục thứ hai, v.v. Với các chỉ mục âm, -1 là chỉ mục cuối cùng và -2 là chỉ mục áp chót (ngay trước chỉ mục cuối), v.v. Hãy coi ``seq[-n]`` giống như ``seq[len(seq)-n]``.

Việc sử dụng các chỉ mục âm có thể rất tiện lợi. Ví dụ, ``S[:-1]`` là toàn bộ chuỗi ngoại trừ ký tự cuối cùng, rất hữu ích khi xóa ký tự xuống dòng ở cuối chuỗi.


Làm thế nào để lặp qua một sequence theo thứ tự ngược?
------------------------------------------------------

Sử dụng hàm tích hợp :func:`reversed`::

   for x in reversed(sequence):
       ...  # làm gì đó với x ...

Cách này không tác động đến sequence ban đầu của bạn mà tạo một bản sao mới theo thứ tự ngược để lặp qua.


Làm thế nào để loại bỏ các phần tử trùng lặp khỏi một list?
-----------------------------------------------------------

Xem Python Cookbook để đọc phần thảo luận chi tiết về nhiều cách thực hiện việc này:

   https://code.activestate.com/recipes/52560/

Nếu bạn không ngại sắp xếp lại list, hãy sắp xếp nó rồi quét từ cuối list, xóa các phần tử trùng lặp khi thực hiện::

   if mylist:
       mylist.sort()
       last = mylist[-1]
       for i in range(len(mylist)-2, -1, -1):
           if last == mylist[i]:
               del mylist[i]
           else:
               last = mylist[i]

Nếu tất cả các phần tử của danh sách đều có thể được dùng làm khóa của set (nghĩa là, tất cả chúng đều
:term:`hashable`) thì cách này thường nhanh hơn::

   mylist = list(set(mylist))

Cách này chuyển danh sách thành một set, qua đó loại bỏ các phần tử trùng lặp, rồi chuyển ngược lại thành một danh sách.


Làm thế nào để xóa nhiều phần tử khỏi một danh sách?
----------------------------------------------------

Tương tự như khi loại bỏ các phần tử trùng lặp, một cách là lặp ngược một cách tường minh với điều kiện xóa. Tuy nhiên, việc sử dụng phép thay thế lát cắt với một vòng lặp xuôi tường minh hoặc ngầm định sẽ dễ dàng và nhanh hơn. Dưới đây là ba biến thể::

   mylist[:] = filter(keep_function, mylist)
   mylist[:] = (x for x in mylist if keep_condition)
   mylist[:] = [x for x in mylist if keep_condition]

List comprehension có thể là cách nhanh nhất.


Làm thế nào để tạo một mảng trong Python?
-----------------------------------------

Dùng một list::

   ["this", 1, "is", "an", "array"]

List tương đương với mảng C hoặc Pascal về độ phức tạp thời gian; điểm khác biệt chính là một list Python có thể chứa các đối tượng thuộc nhiều kiểu khác nhau.

Mô-đun ``array`` cũng cung cấp các phương thức để tạo mảng có kiểu cố định với biểu diễn nhỏ gọn, nhưng chúng có tốc độ truy cập theo chỉ mục chậm hơn list. Cũng lưu ý rằng `NumPy <https://numpy.org/>`_ và các package bên thứ ba khác cũng định nghĩa những cấu trúc dạng mảng với nhiều đặc điểm khác nhau.

Để có linked list kiểu Lisp, bạn có thể mô phỏng *cons cells* bằng tuple::

   lisp_list = ("like",  ("this",  ("example", None) ) )

Nếu cần khả năng thay đổi, bạn có thể dùng list thay vì tuple. Ở đây, tương đương của *car* trong Lisp là ``lisp_list[0]`` và tương đương của *cdr* là ``lisp_list[1]``. Chỉ làm vậy nếu bạn chắc chắn thực sự cần, vì cách này thường chậm hơn nhiều so với việc dùng list Python.


.. _faq-multidimensional-list:

Làm cách nào để tạo một list đa chiều?
--------------------------------------

Có lẽ bạn đã thử tạo một mảng đa chiều như sau::

   >>> A = [[None] * 2] * 3

Điều này trông có vẻ đúng nếu bạn in nó ra:

.. testsetup::

   A = [[None] * 2] * 3

.. doctest::

   >>> A
   [[None, None], [None, None], [None, None]]

Nhưng khi bạn gán một giá trị, nó lại xuất hiện ở nhiều vị trí:

.. testsetup::

   A = [[None] * 2] * 3

.. doctest::

   >>> A[0][0] = 5
   >>> A
   [[5, None], [5, None], [5, None]]

Lý do là việc nhân bản một danh sách bằng ``*`` không tạo ra các bản sao mà chỉ tạo các tham chiếu đến những đối tượng hiện có. ``*3`` tạo một danh sách chứa 3 tham chiếu đến cùng một danh sách có độ dài hai. Các thay đổi đối với một hàng sẽ hiển thị ở tất cả các hàng, và gần như chắc chắn đó không phải là điều bạn muốn.

Cách được khuyến nghị là trước tiên tạo một danh sách có độ dài mong muốn, sau đó điền vào từng phần tử bằng một danh sách mới được tạo::

   A = [None] * 3
   for i in range(3):
       A[i] = [None] * 2

Cách này tạo ra một danh sách chứa 3 danh sách khác nhau có độ dài hai. Bạn cũng có thể sử dụng list comprehension::

   w, h = 2, 3
   A = [[None] * w for i in range(h)]

Hoặc bạn có thể sử dụng một extension cung cấp kiểu dữ liệu ma trận; `NumPy <https://numpy.org/>`_ là thư viện được biết đến nhiều nhất.


Làm thế nào để áp dụng một method hoặc function cho một dãy các đối tượng?
--------------------------------------------------------------------------

Để gọi một method hoặc function và tích lũy các giá trị trả về vào một danh sách, :term:`list comprehension` là một giải pháp tao nhã::

   result = [obj.method() for obj in mylist]

   result = [function(obj) for obj in mylist]

Nếu chỉ muốn chạy method hoặc function mà không lưu các giá trị trả về, một vòng lặp :keyword:`for` thông thường là đủ::

   for obj in mylist:
       obj.method()

   for obj in mylist:
       function(obj)


.. _faq-augmented-assignment-tuple-error:

Tại sao a_tuple[i] += ['item'] lại phát sinh ngoại lệ khi phép cộng vẫn hoạt động?
----------------------------------------------------------------------------------

Lý do là sự kết hợp giữa việc các toán tử *phép gán* tăng cường là các toán tử gán, và sự khác biệt giữa các đối tượng mutable và immutable trong Python.

Thảo luận này áp dụng nói chung khi các toán tử gán tăng cường được áp dụng cho các phần tử của một tuple trỏ tới các đối tượng mutable, nhưng chúng ta sẽ dùng một ``list`` và ``+=`` làm ví dụ minh họa.

Nếu bạn viết::

   >>> a_tuple = (1, 2)
   >>> a_tuple[0] += 1
   Traceback (most recent call last):
      ...
   TypeError: 'tuple' object does not support item assignment

Lý do gây ra ngoại lệ sẽ ngay lập tức trở nên rõ ràng: ``1`` được thêm vào đối tượng mà ``a_tuple[0]`` trỏ tới (``1``), tạo ra đối tượng kết quả ``2``; nhưng khi cố gắng gán kết quả của phép tính, ``2``, cho phần tử ``0`` của tuple, chúng ta gặp lỗi vì không thể thay đổi phần tử của tuple đang trỏ tới đâu.

Về bản chất, câu lệnh phép gán kết hợp này thực hiện gần như sau::

   >>> result = a_tuple[0] + 1
   >>> a_tuple[0] = result
   Traceback (most recent call last):
     ...
   TypeError: 'tuple' object does not support item assignment

Chính phần phép gán của thao tác này gây ra lỗi, vì tuple là immutable.

Khi bạn viết một biểu thức như::

   >>> a_tuple = (['foo'], 'bar')
   >>> a_tuple[0] += ['item']
   Traceback (most recent call last):
     ...
   TypeError: 'tuple' object does not support item assignment

Ngoại lệ này có phần bất ngờ, và còn bất ngờ hơn là dù đã xảy ra lỗi, thao tác append vẫn thành công::

    >>> a_tuple[0]
    ['foo', 'item']

Để hiểu tại sao điều này xảy ra, bạn cần biết rằng (a) nếu một đối tượng triển khai một
:meth:`~object.__iadd__` magic method, phương thức này sẽ được gọi khi phép gán kết hợp ``+=`` được thực thi, và giá trị trả về của nó sẽ được sử dụng trong câu lệnh phép gán; và (b) đối với list, :meth:`!__iadd__` tương đương với việc gọi
:meth:`~sequence.extend` trên list rồi trả về list đó. Đó là lý do chúng ta nói rằng đối với list, ``+=`` là một "cách viết tắt" của :meth:`list.extend`::

    >>> a_list = []
    >>> a_list += [1]
    >>> a_list
    [1]

Điều này tương đương với::

    >>> result = a_list.__iadd__([1])
    >>> a_list = result

Đối tượng được a_list trỏ tới đã bị thay đổi, và con trỏ tới đối tượng đã thay đổi được gán trở lại cho ``a_list``. Kết quả cuối cùng của phép gán không làm thay đổi gì, vì đó là con trỏ tới cùng đối tượng mà ``a_list`` trước đó đã trỏ tới, nhưng phép gán vẫn được thực hiện.

Do đó, trong ví dụ về tuple của chúng ta, điều xảy ra tương đương với::

   >>> result = a_tuple[0].__iadd__(['item'])
   >>> a_tuple[0] = result
   Traceback (most recent call last):
     ...
   TypeError: 'tuple' object does not support item assignment

Phép :meth:`!__iadd__` thành công, vì vậy list được mở rộng, nhưng mặc dù ``result`` trỏ tới cùng đối tượng mà ``a_tuple[0]`` đã trỏ tới, phép gán cuối cùng đó vẫn gây ra lỗi, vì tuple là bất biến.


Tôi muốn thực hiện một phép sắp xếp phức tạp: Python có thể thực hiện Schwartzian Transform không?
--------------------------------------------------------------------------------------------------

Kỹ thuật này, được cho là do Randal Schwartz trong cộng đồng Perl phát triển, sắp xếp các phần tử của một list theo một thước đo ánh xạ mỗi phần tử tới "giá trị sắp xếp" của nó. Trong Python, hãy sử dụng đối số ``key`` cho phương thức :meth:`list.sort`::

   Isorted = L[:]
   Isorted.sort(key=lambda s: int(s[10:15]))


Làm thế nào để sắp xếp một list theo các giá trị từ một list khác?
------------------------------------------------------------------

Gộp chúng thành một iterator gồm các tuple, sắp xếp danh sách kết quả, rồi chọn ra phần tử bạn muốn.

   >>> list1 = ["what", "I'm", "sorting", "by"]
   >>> list2 = ["something", "else", "to", "sort"]
   >>> pairs = zip(list1, list2)
   >>> pairs = sorted(pairs)
   >>> pairs
   [("I'm", 'else'), ('by', 'sort'), ('sorting', 'to'), ('what', 'something')]
   >>> result = [x[1] for x in pairs]
   >>> result
   ['else', 'sort', 'to', 'something']


Đối tượng
=========

Class là gì?
------------

Class là kiểu đối tượng cụ thể được tạo ra bằng cách thực thi một câu lệnh class. Các đối tượng class được dùng làm mẫu để tạo các đối tượng instance, trong đó bao gồm cả dữ liệu (các thuộc tính) và mã (các phương thức) dành riêng cho một kiểu dữ liệu.

Một class có thể dựa trên một hoặc nhiều class khác, được gọi là các base class của nó. Khi đó, nó kế thừa các thuộc tính và phương thức của các base class. Điều này cho phép mô hình đối tượng được tinh chỉnh dần thông qua tính kế thừa. Bạn có thể có một class ``Mailbox`` tổng quát cung cấp các phương thức accessor cơ bản cho một mailbox, cùng các subclass như ``MboxMailbox``, ``MaildirMailbox``, ``OutlookMailbox`` để xử lý nhiều định dạng mailbox cụ thể khác nhau.


Method là gì?
-------------

Method là một hàm trên một đối tượng ``x`` nào đó mà bạn thường gọi như sau: ``x.name(arguments...)``. Các method được định nghĩa dưới dạng các hàm bên trong phần định nghĩa class::

   class C:
       def meth(self, arg):
           return arg * 2 + self.attribute


self là gì?
-----------

Self chỉ đơn thuần là tên gọi theo quy ước cho đối số đầu tiên của một method. Một method được định nghĩa là ``meth(self, a, b, c)`` nên được gọi là ``x.meth(a, b, c)`` đối với một instance ``x`` của class nơi định nghĩa đó xuất hiện; method được gọi sẽ cho rằng nó được gọi là ``meth(x, a, b, c)``.

Xem thêm :ref:`why-self`.


Làm thế nào để kiểm tra xem một object có phải là instance của một class nhất định hoặc của một subclass của class đó hay không?
--------------------------------------------------------------------------------------------------------------------------------

Hãy sử dụng built-in function :func:`isinstance(obj, cls) <isinstance>`. Bạn có thể kiểm tra xem một object có phải là instance của bất kỳ class nào trong số nhiều class hay không bằng cách cung cấp một tuple thay vì một class duy nhất, chẳng hạn như ``isinstance(obj, (class1, class2, ...))``, đồng thời cũng có thể kiểm tra xem một object có phải là một trong các built-in type của Python hay không, chẳng hạn như ``isinstance(obj, str)`` hoặc ``isinstance(obj, (int, float, complex))``.

Lưu ý rằng :func:`isinstance` cũng kiểm tra tính kế thừa ảo từ một
:term:`abstract base class`. Vì vậy, phép kiểm tra sẽ trả về ``True`` đối với một class đã đăng ký ngay cả khi class đó không kế thừa trực tiếp hoặc gián tiếp từ nó. Để kiểm tra "tính kế thừa thực sự", hãy quét :term:`method resolution order` (MRO) của class:

.. testcode::

    from collections.abc import Mapping

    class P:
         pass

    class C(P):
        pass

    Mapping.register(P)

.. doctest::

    >>> c = C()
    >>> isinstance(c, C)        # trực tiếp
    True
    >>> isinstance(c, P)        # gián tiếp
    True
    >>> isinstance(c, Mapping)  # ảo
    True

    # Chuỗi kế thừa thực tế
    >>> type(c).__mro__
    (<class 'C'>, <class 'P'>, <class 'object'>)

    # Kiểm tra "kế thừa thực sự"
    >>> Mapping in type(c).__mro__
    False

Lưu ý rằng hầu hết chương trình không thường xuyên sử dụng :func:`isinstance` trên các lớp do người dùng định nghĩa. Nếu bạn tự phát triển các lớp, phong cách lập trình hướng đối tượng phù hợp hơn là định nghĩa các phương thức trên lớp để đóng gói một hành vi cụ thể, thay vì kiểm tra lớp của đối tượng rồi thực hiện các thao tác khác nhau dựa trên lớp đó. Ví dụ: nếu bạn có một hàm thực hiện một việc gì đó::

   def search(obj):
       if isinstance(obj, Mailbox):
           ...  # mã để tìm kiếm một hộp thư
       elif isinstance(obj, Document):
           ...  # mã để tìm kiếm tài liệu
       elif ...

Một cách tiếp cận tốt hơn là định nghĩa phương thức ``search()`` trên tất cả các lớp rồi chỉ cần gọi phương thức đó::

   class Mailbox:
       def search(self):
           ...  # mã để tìm kiếm một hộp thư

   class Document:
       def search(self):
           ...  # mã để tìm kiếm tài liệu

   obj.search()


Ủy quyền là gì?
---------------

Ủy quyền là một kỹ thuật lập trình hướng đối tượng (còn được gọi là một design pattern). Giả sử bạn có một đối tượng ``x`` và muốn thay đổi hành vi của chỉ một trong các phương thức của nó. Bạn có thể tạo một lớp mới cung cấp cách triển khai mới cho phương thức mà bạn muốn thay đổi, đồng thời ủy quyền tất cả các phương thức khác cho phương thức tương ứng của ``x``.

Các lập trình viên Python có thể dễ dàng triển khai delegation. Ví dụ, lớp sau đây triển khai một lớp hoạt động như một tệp nhưng chuyển đổi tất cả dữ liệu được ghi thành chữ hoa::

   class UpperOut:

       def __init__(self, outfile):
           self._outfile = outfile

       def write(self, s):
           self._outfile.write(s.upper())

       def __getattr__(self, name):
           return getattr(self._outfile, name)

Ở đây, lớp ``UpperOut`` định nghĩa lại phương thức ``write()`` để chuyển chuỗi đối số thành chữ hoa trước khi gọi phương thức ``self._outfile.write()`` bên dưới. Tất cả các phương thức khác được ủy quyền cho đối tượng ``self._outfile`` bên dưới. Việc ủy quyền được thực hiện thông qua
phương thức :meth:`~object.__getattr__`; hãy tham khảo :ref:`tài liệu tham chiếu của ngôn ngữ <attribute-access>` để biết thêm thông tin về cách kiểm soát quyền truy cập thuộc tính.

Lưu ý rằng trong các trường hợp tổng quát hơn, việc ủy quyền có thể trở nên phức tạp hơn. Khi cần vừa thiết lập vừa truy xuất thuộc tính, lớp cũng phải định nghĩa phương thức :meth:`~object.__setattr__`, và phải thực hiện việc đó một cách cẩn thận. Cách triển khai cơ bản của
:meth:`!__setattr__` gần tương đương với đoạn mã sau::

   class X:
       ...
       def __setattr__(self, name, value):
           self.__dict__[name] = value
       ...

Nhiều cách triển khai :meth:`~object.__setattr__` gọi :meth:`!object.__setattr__` để thiết lập một thuộc tính trên self mà không gây ra đệ quy vô hạn::

   class X:
       def __setattr__(self, name, value):
           # Logic tùy chỉnh ở đây...
           object.__setattr__(self, name, value)

Ngoài ra, có thể thiết lập thuộc tính bằng cách chèn trực tiếp các mục vào :attr:`self.__dict__ <object.__dict__>`.


Làm thế nào để gọi một phương thức được định nghĩa trong lớp cơ sở từ một lớp dẫn xuất mở rộng lớp đó?
------------------------------------------------------------------------------------------------------

Sử dụng hàm dựng sẵn :func:`super`::

   class Derived(Base):
       def meth(self):
           super().meth()  # gọi Base.meth

Trong ví dụ, :func:`super` sẽ tự động xác định instance mà từ đó nó được gọi (giá trị ``self``), tra cứu :term:`method resolution order` (MRO) bằng ``type(self).__mro__``, rồi trả về phần tử tiếp theo sau ``Derived`` trong MRO: ``Base``.


Làm thế nào để tổ chức mã nguồn để dễ thay đổi lớp cơ sở hơn?
-------------------------------------------------------------

Bạn có thể gán lớp cơ sở cho một alias rồi kế thừa từ alias đó. Khi ấy, tất cả những gì bạn phải thay đổi là giá trị được gán cho alias. Ngoài ra, thủ thuật này cũng hữu ích nếu bạn muốn quyết định động lớp cơ sở nào sẽ được sử dụng (chẳng hạn tùy thuộc vào khả năng sẵn có của tài nguyên). Ví dụ::

   class Base:
       ...

   BaseAlias = Base

   class Derived(BaseAlias):
       ...


Làm thế nào để tạo dữ liệu tĩnh của lớp và các phương thức tĩnh của lớp?
------------------------------------------------------------------------

Python hỗ trợ cả dữ liệu static và các phương thức static (theo nghĩa của C++ hoặc Java).

Đối với dữ liệu static, chỉ cần định nghĩa một thuộc tính của lớp. Để gán giá trị mới cho thuộc tính, bạn phải sử dụng tường minh tên lớp trong phép gán::

   class C:
       count = 0   # số lần C.__init__ được gọi

       def __init__(self):
           C.count = C.count + 1

       def getcount(self):
           return C.count  # hoặc return self.count

``c.count`` cũng tham chiếu đến ``C.count`` đối với mọi ``c`` sao cho ``isinstance(c, C)`` đúng, trừ khi bị chính ``c`` hoặc một lớp nào đó trên đường dẫn tìm kiếm lớp cơ sở từ ``c.__class__`` ngược về ``C`` ghi đè.

Cảnh báo: trong một phương thức của C, phép gán như ``self.count = 42`` sẽ tạo một instance mới, không liên quan, có tên "count" trong dict riêng của ``self``. Việc liên kết lại một tên dữ liệu static của lớp luôn phải chỉ rõ lớp, dù ở bên trong một phương thức hay không::

   C.count = 314

Có thể sử dụng các phương thức static::

   class C:
       @staticmethod
       def static(arg1, arg2, arg3):
           # Không có tham số 'self'!
           ...

Tuy nhiên, một cách đơn giản hơn nhiều để đạt được hiệu ứng của một phương thức static là sử dụng một hàm cấp mô-đun đơn giản::

   def getcount():
       return C.count

Nếu mã của bạn được cấu trúc để định nghĩa một lớp (hoặc một hệ thống phân cấp các lớp có liên quan chặt chẽ) trong mỗi mô-đun, cách này sẽ cung cấp khả năng đóng gói mong muốn.


Làm thế nào để overload constructor (hoặc phương thức) trong Python?
--------------------------------------------------------------------

Câu trả lời này thực ra áp dụng cho tất cả các phương thức, nhưng câu hỏi thường xuất hiện trước tiên trong ngữ cảnh của constructor.

Trong C++, bạn sẽ viết:

.. code-block:: c++

    class C {
        C() { cout << "No arguments\n"; }
        C(int i) { cout << "Argument is " << i << "\n"; }
    }

Trong Python, bạn phải viết một constructor duy nhất để xử lý mọi trường hợp bằng cách sử dụng các đối số mặc định. Ví dụ::

   class C:
       def __init__(self, i=None):
           if i is None:
               print("No arguments")
           else:
               print("Argument is", i)

Điều này không hoàn toàn tương đương, nhưng trên thực tế thì đủ gần.

Bạn cũng có thể thử một danh sách đối số có độ dài thay đổi, chẳng hạn như::

   def __init__(self, *args):
       ...

Cách tiếp cận tương tự áp dụng cho mọi định nghĩa phương thức.


Tôi cố sử dụng __spam và nhận được lỗi về _SomeClassName__spam.
---------------------------------------------------------------

Tên biến có hai dấu gạch dưới ở đầu sẽ được "mangle" để cung cấp một cách đơn giản nhưng hiệu quả nhằm định nghĩa các biến riêng tư của lớp. Bất kỳ identifier nào có dạng ``__spam`` (ít nhất hai dấu gạch dưới ở đầu, nhiều nhất một dấu gạch dưới ở cuối) đều được thay thế về mặt văn bản bằng ``_classname__spam``, trong đó ``classname`` là tên lớp hiện tại sau khi bỏ mọi dấu gạch dưới ở đầu.

Identifier này có thể được sử dụng không thay đổi bên trong lớp, nhưng để truy cập nó bên ngoài lớp, phải sử dụng tên đã được mangle:

.. code-block:: python

   class A:
       def __one(self):
           return 1
       def two(self):
           return 2 * self.__one()

   class B(A):
       def three(self):
           return 3 * self._A__one()

   four = 4 * A()._A__one()

Cụ thể, điều này không đảm bảo tính riêng tư, vì người dùng bên ngoài vẫn có thể cố ý truy cập thuộc tính riêng tư; nhiều lập trình viên Python hoàn toàn không dùng tên biến riêng tư.

.. seealso::

   Xem :ref:`đặc tả về việc làm rối tên private <private-name-mangling>` để biết chi tiết và các trường hợp đặc biệt.


Lớp của tôi định nghĩa __del__ nhưng phương thức này không được gọi khi tôi xóa đối tượng.
------------------------------------------------------------------------------------------

Có một số nguyên nhân có thể dẫn đến điều này.

Câu lệnh :keyword:`del` không nhất thiết gọi :meth:`~object.__del__` -- nó chỉ giảm bộ đếm tham chiếu của đối tượng, và nếu bộ đếm này về 0
:meth:`!__del__` sẽ được gọi.

Nếu các cấu trúc dữ liệu của bạn chứa các liên kết vòng (ví dụ: một cây trong đó mỗi nút con có tham chiếu đến nút cha và mỗi nút cha có một danh sách các nút con), bộ đếm tham chiếu sẽ không bao giờ về 0. Thỉnh thoảng Python chạy một thuật toán để phát hiện các chu kỳ như vậy, nhưng garbage collector có thể chạy một thời gian sau khi tham chiếu cuối cùng đến cấu trúc dữ liệu của bạn biến mất, vì vậy phương thức :meth:`!__del__` của bạn có thể được gọi vào một thời điểm bất tiện và ngẫu nhiên. Điều này gây bất tiện nếu bạn đang cố tái hiện một sự cố. Tệ hơn nữa, thứ tự thực thi các phương thức :meth:`!__del__` của đối tượng là không xác định. Bạn có thể chạy :func:`gc.collect` để buộc thực hiện việc thu gom, nhưng có *các* trường hợp đặc biệt trong đó các đối tượng sẽ không bao giờ được thu gom.

Mặc dù có cycle collector, bạn vẫn nên định nghĩa một phương thức ``close()`` tường minh trên các đối tượng để gọi phương thức này bất cứ khi nào bạn không còn dùng chúng. Sau đó, phương thức ``close()`` có thể xóa các thuộc tính tham chiếu đến các đối tượng con. Đừng gọi trực tiếp :meth:`!__del__` -- :meth:`!__del__` nên gọi ``close()`` và ``close()`` phải đảm bảo rằng phương thức này có thể được gọi nhiều lần trên cùng một đối tượng.

Một cách khác để tránh các tham chiếu vòng là sử dụng mô-đun :mod:`weakref`, cho phép bạn trỏ đến các đối tượng mà không làm tăng số lượng tham chiếu của chúng. Chẳng hạn, các cấu trúc dữ liệu dạng cây nên sử dụng weak reference cho các tham chiếu đến nút cha và nút anh em (nếu cần!).

.. XXX relevant for Python 3?

   If the object has ever been a local variable in a function that caught an
   expression in an except clause, chances are that a reference to the object
   still exists in that function's stack frame as contained in the stack trace.
   Normally, calling :func:`sys.exc_clear` will take care of this by clearing
   the last recorded exception.

Cuối cùng, nếu phương thức :meth:`!__del__` của bạn phát sinh ngoại lệ, một thông báo cảnh báo sẽ được in ra :data:`sys.stderr`.


Làm thế nào để lấy danh sách tất cả các instance của một class nhất định?
-------------------------------------------------------------------------

Python không theo dõi tất cả các instance của một class (hoặc của một kiểu dựng sẵn). Bạn có thể lập trình constructor của class để theo dõi tất cả các instance bằng cách lưu một danh sách các weak reference đến từng instance.


Tại sao kết quả của ``id()`` dường như không phải là duy nhất?
--------------------------------------------------------------

Builtin :func:`id` trả về một số nguyên được đảm bảo là duy nhất trong suốt vòng đời của đối tượng. Vì trong CPython, đây là địa chỉ bộ nhớ của đối tượng, nên thường xảy ra trường hợp sau khi một đối tượng bị xóa khỏi bộ nhớ, đối tượng mới được tạo tiếp theo lại được cấp phát tại cùng vị trí trong bộ nhớ. Ví dụ sau minh họa điều này:

>>> id(1000) # doctest: +SKIP
13901272
>>> id(2000) # doctest: +SKIP
13901272

Hai id này thuộc về hai đối tượng số nguyên khác nhau, được tạo trước và bị xóa ngay sau khi thực thi lệnh gọi ``id()``. Để chắc chắn rằng các đối tượng bạn muốn kiểm tra id vẫn còn tồn tại, hãy tạo thêm một tham chiếu đến đối tượng:

>>> a = 1000; b = 2000
>>> id(a) # doctest: +SKIP
13901272
>>> id(b) # doctest: +SKIP
13891296


.. _faq-identity-with-is:

Khi nào tôi có thể dựa vào các phép kiểm tra identity với toán tử *is*?
-----------------------------------------------------------------------

Toán tử ``is`` kiểm tra identity của đối tượng. Phép kiểm tra ``a is b`` tương đương với ``id(a) == id(b)``.

Thuộc tính quan trọng nhất của phép kiểm tra identity là một đối tượng luôn giống hệt chính nó, ``a is a`` luôn trả về ``True``. Các phép kiểm tra identity thường nhanh hơn các phép kiểm tra bằng nhau. Và không giống các phép kiểm tra bằng nhau, các phép kiểm tra identity được đảm bảo luôn trả về một giá trị boolean ``True`` hoặc ``False``.

Tuy nhiên, phép kiểm tra identity *chỉ* có thể được dùng thay cho phép kiểm tra equality khi chắc chắn về identity của đối tượng. Nhìn chung, có ba trường hợp identity được đảm bảo:

1) Phép gán tạo ra các tên mới nhưng không thay đổi identity của đối tượng. Sau phép gán ``new = old``, chắc chắn rằng ``new is old``.

2) Đưa một đối tượng vào container lưu trữ các tham chiếu đến đối tượng không làm thay đổi identity của đối tượng. Sau phép gán list ``s[0] = x``, chắc chắn rằng ``s[0] is x``.

3) Nếu một đối tượng là singleton, điều đó có nghĩa là chỉ có thể tồn tại một instance của đối tượng đó. Sau các phép gán ``a = None`` và ``b = None``, chắc chắn rằng ``a is b`` vì ``None`` là singleton.

Trong hầu hết các trường hợp khác, không nên dùng phép kiểm tra identity và nên ưu tiên phép kiểm tra equality. Cụ thể, không nên dùng phép kiểm tra identity để kiểm tra các hằng số như :class:`int` và :class:`str`, vì không đảm bảo chúng là singleton::

    >>> a = 10_000_000
    >>> b = 5_000_000
    >>> c = b + 5_000_000
    >>> a is c
    False

    >>> a = 'Python'
    >>> b = 'Py'
    >>> c = b + 'thon'
    >>> a is c
    False

Tương tự, các instance mới của mutable container không bao giờ identical::

    >>> a = []
    >>> b = []
    >>> a is b
    False

Trong mã của standard library, bạn sẽ thấy một số mẫu phổ biến để sử dụng phép kiểm tra identity đúng cách:

1) Theo khuyến nghị của :pep:`8`, kiểm tra định danh là cách được ưu tiên để kiểm tra ``None``. Cách này khiến mã dễ đọc như tiếng Anh thông thường và tránh nhầm lẫn với các đối tượng khác có thể có giá trị boolean được đánh giá là false.

2) Việc phát hiện các đối số tùy chọn có thể phức tạp khi ``None`` là một giá trị đầu vào hợp lệ. Trong những trường hợp đó, bạn có thể tạo một đối tượng sentinel singleton được đảm bảo khác biệt với các đối tượng khác. Ví dụ sau đây minh họa cách triển khai một phương thức hoạt động như :meth:`dict.pop`:

   .. code-block:: python

      _sentinel = object()

      def pop(self, key, default=_sentinel):
          if key in self:
              value = self[key]
              del self[key]
              return value
          if default is _sentinel:
              raise KeyError(key)
          return default

3) Các triển khai container đôi khi cần bổ sung kiểm tra định danh cho các kiểm tra bằng nhau. Điều này ngăn mã bị nhầm lẫn bởi những đối tượng như ``float('NaN')``, vốn không bằng chính chúng.

Ví dụ, sau đây là triển khai của
:meth:`!collections.abc.Sequence.__contains__`::

    def __contains__(self, value):
        for v in self:
            if v is value or v == value:
                return True
        return False


Làm thế nào một lớp con có thể kiểm soát dữ liệu được lưu trữ trong một thực thể bất biến?
------------------------------------------------------------------------------------------

Khi tạo lớp con từ một kiểu bất biến, hãy ghi đè phương thức :meth:`~object.__new__` thay vì phương thức :meth:`~object.__init__`. Phương thức sau chỉ chạy *after* một thực thể được tạo, nên đã quá muộn để thay đổi dữ liệu trong một thực thể bất biến.

Tất cả các lớp bất biến này đều có chữ ký khác với lớp cha của chúng:

.. testcode::

    import datetime as dt

    class FirstOfMonthDate(dt.date):
        "Always choose the first day of the month"
        def __new__(cls, year, month, day):
            return super().__new__(cls, year, month, 1)

    class NamedInt(int):
        "Allow text names for some numbers"
        xlat = {'zero': 0, 'one': 1, 'ten': 10}
        def __new__(cls, value):
            value = cls.xlat.get(value, value)
            return super().__new__(cls, value)

    class TitleStr(str):
        "Convert str to name suitable for a URL path"
        def __new__(cls, s):
            s = s.lower().replace(' ', '-')
            s = ''.join([c for c in s if c.isalnum() or c == '-'])
            return super().__new__(cls, s)

Các lớp có thể được sử dụng như sau:

.. doctest::

    >>> FirstOfMonthDate(2012, 2, 14)
    FirstOfMonthDate(2012, 2, 1)
    >>> NamedInt('ten')
    10
    >>> NamedInt(20)
    20
    >>> TitleStr('Blog: Why Python Rocks')
    'blog-why-python-rocks'


.. _faq-cache-method-calls:

Làm thế nào để cache các lần gọi phương thức?
---------------------------------------------

Hai công cụ chính để cache các phương thức là
:deco:`functools.cached_property` và :deco:`functools.lru_cache`. Công cụ thứ nhất lưu trữ kết quả ở cấp instance, còn công cụ thứ hai lưu trữ kết quả ở cấp lớp.

Cách tiếp cận ``cached_property`` chỉ hoạt động với các phương thức không nhận đối số nào. Nó không tạo tham chiếu đến instance. Kết quả phương thức được cache sẽ chỉ được giữ lại chừng nào instance còn tồn tại.

Ưu điểm là khi một instance không còn được sử dụng, kết quả phương thức được cache sẽ được giải phóng ngay. Nhược điểm là nếu các instance tích lũy, thì các kết quả phương thức được tích lũy cũng sẽ tăng theo. Chúng có thể tăng không giới hạn.

Cách tiếp cận ``lru_cache`` hoạt động với các phương thức có :term:`hashable` đối số. Nó tạo tham chiếu đến instance, trừ khi có các biện pháp đặc biệt để truyền vào các weak reference.

Ưu điểm của thuật toán ít được sử dụng gần đây nhất là cache được giới hạn bởi *maxsize* được chỉ định. Nhược điểm là các đối tượng vẫn được duy trì cho đến khi hết thời gian lưu trong cache hoặc cache được xóa.

Ví dụ này minh họa nhiều kỹ thuật khác nhau::

    class Weather:
        "Lookup weather information on a government website"

        def __init__(self, station_id):
            self._station_id = station_id
            # _station_id là private và bất biến

        def current_temperature(self):
            "Latest hourly observation"
            # Không cache giá trị này vì các kết quả cũ
            # có thể đã lỗi thời.

        @cached_property
        def location(self):
            "Return the longitude/latitude coordinates of the station"
            # Kết quả chỉ phụ thuộc vào station_id

        @lru_cache(maxsize=20)
        def historic_rainfall(self, date, units='mm'):
            "Rainfall on a given date"
            # Phụ thuộc vào station_id, ngày và đơn vị.

Ví dụ trên giả định rằng *station_id* không bao giờ thay đổi. Nếu các thuộc tính của instance liên quan có thể thay đổi, không thể sử dụng ``cached_property`` approach vì nó không thể phát hiện những thay đổi đối với các thuộc tính đó.

Để ``lru_cache`` approach hoạt động khi *station_id* có thể thay đổi, class cần định nghĩa các phương thức :meth:`~object.__eq__` và :meth:`~object.__hash__` để cache có thể phát hiện những cập nhật thuộc tính liên quan::

    class Weather:
        "Example with a mutable station identifier"

        def __init__(self, station_id):
            self.station_id = station_id

        def change_station(self, station_id):
            self.station_id = station_id

        def __eq__(self, other):
            return self.station_id == other.station_id

        def __hash__(self):
            return hash(self.station_id)

        @lru_cache(maxsize=20)
        def historic_rainfall(self, date, units='cm'):
            'Rainfall on a given date'
            # Phụ thuộc vào station_id, ngày và đơn vị.


Các module
==========

Làm thế nào để tạo tệp .pyc?
----------------------------

Khi một module được import lần đầu (hoặc khi tệp mã nguồn đã thay đổi kể từ lúc tệp đã biên dịch hiện tại được tạo), một tệp ``.pyc`` chứa mã đã biên dịch sẽ được tạo trong thư mục con ``__pycache__`` của thư mục chứa tệp ``.py``. Tệp ``.pyc`` sẽ có tên tệp bắt đầu bằng cùng tên với tệp ``.py``, và kết thúc bằng ``.pyc``, với một phần ở giữa phụ thuộc vào binary ``python`` cụ thể đã tạo ra tệp đó. (Xem :pep:`3147` để biết chi tiết.)

Một lý do khiến tệp ``.pyc`` không được tạo có thể là vấn đề về quyền đối với thư mục chứa tệp mã nguồn, khiến không thể tạo thư mục con ``__pycache__``. Ví dụ, điều này có thể xảy ra nếu bạn phát triển bằng một user nhưng chạy bằng một user khác, chẳng hạn khi bạn kiểm thử bằng web server.

Trừ khi biến môi trường :envvar:`PYTHONDONTWRITEBYTECODE` được thiết lập, việc tạo tệp .pyc sẽ tự động diễn ra nếu bạn đang import một module và Python có khả năng (quyền, dung lượng trống, v.v.) tạo thư mục con ``__pycache__`` và ghi module đã biên dịch vào thư mục con đó.

Việc chạy Python trên một tập lệnh cấp cao nhất không được xem là thao tác import và sẽ không tạo ``.pyc``. Ví dụ, nếu bạn có module cấp cao nhất ``foo.py`` import một module khác là ``xyz.py``, khi chạy ``foo`` (bằng cách nhập ``python foo.py`` dưới dạng lệnh shell), một ``.pyc`` sẽ được tạo cho ``xyz`` vì ``xyz`` được import, nhưng sẽ không có tệp ``.pyc`` nào được tạo cho ``foo`` vì ``foo.py`` không được import.

Nếu cần tạo tệp ``.pyc`` cho ``foo`` -- tức là tạo tệp ``.pyc`` cho một module không được import -- bạn có thể sử dụng
các module :mod:`py_compile` và :mod:`compileall`.

Module :mod:`py_compile` có thể biên dịch thủ công bất kỳ module nào. Một cách là sử dụng hàm ``compile()`` trong module đó ở chế độ tương tác::

   >>> import py_compile
   >>> py_compile.compile('foo.py')                 # doctest: +SKIP

Thao tác này sẽ ghi ``.pyc`` vào thư mục con ``__pycache__`` tại cùng vị trí với ``foo.py`` (hoặc bạn có thể ghi đè vị trí đó bằng tham số tùy chọn *cfile*).

Bạn cũng có thể tự động biên dịch tất cả các tệp trong một hoặc nhiều thư mục bằng mô-đun :mod:`compileall`. Bạn có thể thực hiện việc này từ dấu nhắc shell bằng cách chạy ``compileall.py`` và cung cấp đường dẫn đến một thư mục chứa các tệp Python cần biên dịch::

       python -m compileall .


Làm thế nào để tìm tên mô-đun hiện tại?
---------------------------------------

Một mô-đun có thể tìm ra tên của chính nó bằng cách xem biến toàn cục được định nghĩa trước ``__name__``. Nếu biến này có giá trị ``'__main__'``, chương trình đang chạy dưới dạng một script. Nhiều mô-đun thường được sử dụng bằng cách import cũng cung cấp giao diện dòng lệnh hoặc chức năng tự kiểm tra, và chỉ thực thi mã này sau khi kiểm tra ``__name__``::

   def main():
       print('Running test...')
       ...

   if __name__ == '__main__':
       main()


Làm thế nào để các mô-đun import lẫn nhau?
------------------------------------------

Giả sử bạn có các mô-đun sau:

:file:`foo.py`::

   from bar import bar_var
   foo_var = 1

:file:`bar.py`::

   from foo import foo_var
   bar_var = 2

Vấn đề là trình thông dịch sẽ thực hiện các bước sau:

* main import ``foo``
* Các biến toàn cục rỗng cho ``foo`` được tạo
* ``foo`` được biên dịch và bắt đầu thực thi
* ``foo`` import ``bar``
* Các biến toàn cục rỗng cho ``bar`` được tạo
* ``bar`` được biên dịch và bắt đầu thực thi
* ``bar`` import ``foo`` (không thực hiện gì vì đã có một module có tên ``foo``)
* Cơ chế import cố đọc ``foo_var`` từ các biến toàn cục của ``foo`` để đặt ``bar.foo_var = foo.foo_var``

Bước cuối cùng không thành công vì Python vẫn chưa diễn giải xong ``foo`` và từ điển ký hiệu toàn cục của ``foo`` vẫn còn trống.

Điều tương tự cũng xảy ra khi bạn sử dụng ``import foo``, rồi cố truy cập ``foo.foo_var`` trong mã toàn cục.

Có (ít nhất) ba cách giải quyết khả thi cho vấn đề này.

Guido van Rossum khuyến nghị tránh mọi cách sử dụng ``from <module> import ...`` và đặt toàn bộ mã bên trong các hàm. Việc khởi tạo các biến toàn cục và biến lớp chỉ nên sử dụng hằng số hoặc các hàm dựng sẵn. Điều này có nghĩa là mọi thứ từ một module đã import đều được tham chiếu dưới dạng ``<module>.<name>``.

Jim Roskind đề xuất thực hiện các bước theo thứ tự sau trong mỗi module:

* các thành phần export (biến toàn cục, hàm và lớp không cần các lớp cơ sở đã import)
* các câu lệnh ``import``
* mã đang hoạt động (bao gồm cả các biến toàn cục được khởi tạo từ những giá trị đã import).

Van Rossum không mấy ưa cách tiếp cận này vì các câu lệnh import xuất hiện ở một vị trí khá kỳ lạ, nhưng cách này vẫn hoạt động.

Matthias Urlichs khuyến nghị tái cấu trúc mã của bạn để ngay từ đầu không cần đến import đệ quy.

Các giải pháp này không loại trừ lẫn nhau.


__import__('x.y.z') trả về <module 'x'>; làm thế nào để lấy z?
--------------------------------------------------------------

Hãy cân nhắc sử dụng hàm tiện ích :func:`~importlib.import_module` từ
:mod:`importlib` thay vào đó::

   z = importlib.import_module('x.y.z')


Khi tôi chỉnh sửa một module đã import rồi import lại module đó, các thay đổi không xuất hiện. Tại sao lại như vậy?
-------------------------------------------------------------------------------------------------------------------

Để tăng hiệu quả cũng như bảo đảm tính nhất quán, Python chỉ đọc tệp module vào lần đầu tiên module được import. Nếu không, trong một chương trình gồm nhiều module và mỗi module đều import cùng một module cơ bản, module cơ bản sẽ bị phân tích cú pháp lặp đi lặp lại nhiều lần. Để buộc đọc lại một module đã thay đổi, hãy làm như sau::

   import importlib
   import modname
   importlib.reload(modname)

Cảnh báo: kỹ thuật này không hoàn toàn đáng tin cậy. Cụ thể, các module chứa những câu lệnh như::

   from modname import some_objects

sẽ tiếp tục hoạt động với phiên bản cũ của các đối tượng đã import. Nếu module chứa các định nghĩa lớp, các instance lớp hiện có *không* được cập nhật để sử dụng định nghĩa lớp mới. Điều này có thể dẫn đến hành vi nghịch lý sau đây::

   >>> import importlib
   >>> import cls
   >>> c = cls.C()                # Tạo một instance của C
   >>> importlib.reload(cls)
   <module 'cls' from 'cls.py'>
   >>> isinstance(c, cls.C)       # isinstance là false?!?
   False

Bản chất của vấn đề sẽ trở nên rõ ràng nếu bạn in ra "identity" của các đối tượng lớp::

   >>> hex(id(c.__class__))
   '0x7352a0'
   >>> hex(id(cls.C))
   '0x4198d0'

.. _`pywin32`: https://github.com/mhammond/pywin32
.. _`ActivePython`: https://www.activestate.com/products/python/
.. _`Eric`: https://eric-ide.python-projects.org/
.. _`trepan3k`: https://github.com/rocky/python3-trepan/
.. _`Visual Studio Code`: https://code.visualstudio.com/
.. _`Wing IDE`: https://wingware.com/
.. _`PyCharm`: https://www.jetbrains.com/pycharm/
.. _`Nuitka`: https://nuitka.net/
.. _`PyInstaller`: https://pyinstaller.org/
.. _`PyOxidizer`: https://pyoxidizer.readthedocs.io/en/stable/
.. _`cx_Freeze`: https://marcelotduarte.github.io/cx_Freeze/
.. _`py2app`: https://github.com/ronaldoussoren/py2app
.. _`py2exe`: https://www.py2exe.org/
.. _`Cython`: https://cython.org
.. _`performance tips`: https://wiki.python.org/moin/PythonSpeed/PerformanceTips
.. _`NumPy`: https://numpy.org/
