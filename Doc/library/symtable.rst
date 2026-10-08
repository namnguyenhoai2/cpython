:mod:`!symtable` --- Truy cập vào các bảng ký hiệu của trình biên dịch
======================================================================

.. module:: symtable
   :synopsis: Giao diện để truy cập các bảng ký hiệu nội bộ của trình biên dịch.

**Mã nguồn:** :source:`Lib/symtable.py`

--------------

.. moduleauthor:: Jeremy Hylton <jeremy@alum.mit.edu>
.. sectionauthor:: Benjamin Peterson <benjamin@python.org>


Trình biên dịch tạo các bảng ký hiệu từ AST ngay trước khi tạo bytecode. Bảng ký hiệu chịu trách nhiệm tính toán phạm vi của mọi mã định danh trong mã. :mod:`!symtable` cung cấp giao diện để kiểm tra các bảng này.


Tạo bảng ký hiệu
----------------

.. function:: symtable(code, filename, compile_type)

   Trả về :class:`SymbolTable` cấp cao nhất cho mã nguồn Python *code*. *filename* là tên của tệp chứa mã. *compile_type* tương tự như đối số *mode* của :func:`compile`.


Kiểm tra bảng ký hiệu
---------------------

.. class:: SymbolTableType

   Một kiểu liệt kê cho biết loại của đối tượng :class:`SymbolTable`.

   .. attribute:: MODULE
      :value: "module"

      Được sử dụng cho bảng ký hiệu của một module.

   .. attribute:: FUNCTION
      :value: "function"

      Được sử dụng cho bảng ký hiệu của một hàm.

   .. attribute:: CLASS
      :value: "class"

      Được sử dụng cho bảng ký hiệu của một lớp.

   Các thành viên sau đây đề cập đến những dạng khác nhau của
   :ref:`phạm vi chú thích <annotation-scopes>`.

   .. attribute:: ANNOTATION
      :value: "annotation"

      Được sử dụng cho các chú thích nếu ``from __future__ import annotations`` đang hoạt động.

   .. attribute:: TYPE_ALIAS
      :value: "type alias"

      Được dùng cho bảng ký hiệu của các :keyword:`type` cấu trúc.

   .. attribute:: TYPE_PARAMETERS
      :value: "type parameters"

      Được dùng cho bảng ký hiệu của các :ref:`hàm generic <generic-functions>` hoặc :ref:`lớp generic <generic-classes>`.

   .. attribute:: TYPE_VARIABLE
      :value: "type variable"

      Được dùng cho bảng ký hiệu của bound, constraint tuple hoặc giá trị mặc định của một biến kiểu đơn lẻ theo nghĩa hình thức, tức là một đối tượng TypeVar, TypeVarTuple hoặc ParamSpec (hai đối tượng sau không hỗ trợ bound hoặc constraint tuple).

   .. versionadded:: 3.13

.. class:: SymbolTable

   Một bảng namespace cho một block. Constructor không public.

   .. method:: get_type()

      Trả về kiểu của bảng ký hiệu. Các giá trị có thể có là các thành viên của enumeration :class:`SymbolTableType`.

      .. versionchanged:: 3.12
         Đã bổ sung ``'annotation'``, ``'TypeVar bound'``, ``'type alias'`` và ``'type parameter'`` làm các giá trị trả về có thể có.

      .. versionchanged:: 3.13
         Các giá trị trả về là các thành viên của enumeration :class:`SymbolTableType`.

         Các giá trị chính xác của chuỗi được trả về có thể thay đổi trong tương lai, vì vậy bạn nên sử dụng các thành viên :class:`SymbolTableType` thay vì các chuỗi được ghi cứng.

   .. method:: get_id()

      Trả về mã định danh của bảng.

   .. method:: get_name()

      Trả về tên của bảng. Đây là tên của lớp nếu bảng dành cho một lớp, tên của hàm nếu bảng dành cho một hàm hoặc ``'top'`` nếu bảng là toàn cục (:meth:`get_type` trả về ``'module'``). Đối với các phạm vi tham số kiểu (được sử dụng cho các lớp generic, hàm generic và bí danh kiểu), đây là tên của lớp, hàm hoặc bí danh kiểu bên dưới. Đối với các phạm vi bí danh kiểu, đây là tên của bí danh kiểu. Đối với các phạm vi liên kết với :class:`~typing.TypeVar`, đây là tên của ``TypeVar``.

   .. method:: get_lineno()

      Trả về số của dòng đầu tiên trong khối mà bảng này biểu diễn.

   .. method:: is_optimized()

      Trả về ``True`` nếu các biến cục bộ trong bảng này có thể được tối ưu hóa.

   .. method:: is_nested()

      Trả về ``True`` nếu khối là một lớp hoặc hàm lồng nhau.

   .. method:: has_children()

      Trả về ``True`` nếu khối chứa các namespace lồng nhau. Có thể lấy chúng bằng :meth:`get_children`.

   .. method:: get_identifiers()

      Trả về một đối tượng view chứa tên của các symbol trong bảng. Xem :ref:`tài liệu về các đối tượng view <dict-views>`.

   .. method:: lookup(name)

      Tra cứu *name* trong bảng và trả về một thực thể :class:`Symbol`.

   .. method:: get_symbols()

      Trả về một danh sách các thực thể :class:`Symbol` tương ứng với các name trong bảng.

   .. method:: get_children()

      Trả về một danh sách các bảng symbol lồng nhau.


.. class:: Function

   Một namespace dành cho một hàm hoặc method. Lớp này kế thừa từ
   :class:`SymbolTable`.

   .. method:: get_parameters()

      Trả về một tuple chứa tên các parameter của hàm này.

   .. method:: get_locals()

      Trả về một tuple chứa tên các biến local trong hàm này.

   .. method:: get_globals()

      Trả về một tuple chứa tên các biến toàn cục trong hàm này.

   .. method:: get_nonlocals()

      Trả về một tuple chứa tên các biến nonlocal được khai báo tường minh trong hàm này.

   .. method:: get_frees()

      Trả về một tuple chứa tên các biến :term:`tự do (closure) <closure variable>` trong hàm này.


.. class:: Class

   Một namespace của một lớp. Lớp này kế thừa từ :class:`SymbolTable`.

   .. method:: get_methods()

      Trả về một tuple chứa tên của các hàm dạng phương thức được khai báo trong lớp.

      Ở đây, thuật ngữ 'phương thức' chỉ *bất kỳ* hàm nào được định nghĩa trong thân lớp thông qua :keyword:`def` hoặc :keyword:`async def`.

      Các hàm được định nghĩa trong một phạm vi sâu hơn (ví dụ: trong một lớp bên trong) sẽ không được :meth:`get_methods` phát hiện.

      Ví dụ:

      .. testsetup:: symtable.Class.get_methods

         import warnings
         context = warnings.catch_warnings()
         context.__enter__()
         warnings.simplefilter("ignore", category=DeprecationWarning)

      .. testcleanup:: symtable.Class.get_methods

         context.__exit__()

      .. doctest:: symtable.Class.get_methods

         >>> import symtable
         >>> st = symtable.symtable('''
         ... def outer(): pass
         ...
         ... class A:
         ...    def f():
         ...        def w(): pass
         ...
         ...    def g(self): pass
         ...
         ...    @classmethod
         ...    async def h(cls): pass
         ...
         ...    global outer
         ...    def outer(self): pass
         ... ''', 'test', 'exec')
         >>> class_A = st.get_children()[2]
         >>> class_A.get_methods()
         ('f', 'g', 'h')

      Mặc dù ``A().f()`` gây ra :exc:`TypeError` khi runtime, ``A.f`` vẫn được xem là một hàm dạng phương thức.

      .. deprecated-removed:: 3.14 3.16


.. class:: Symbol

   Một mục trong :class:`SymbolTable` tương ứng với một identifier trong mã nguồn. Hàm khởi tạo không phải là public.

   .. method:: get_name()

      Trả về tên của symbol.

   .. method:: is_referenced()

      Trả về ``True`` nếu symbol được sử dụng trong block của nó.

   .. method:: is_imported()

      Trả về ``True`` nếu symbol được tạo từ một câu lệnh import.

   .. method:: is_parameter()

      Trả về ``True`` nếu symbol là một parameter.

   .. method:: is_type_parameter()

      Trả về ``True`` nếu ký hiệu là tham số kiểu.

      .. versionadded:: 3.14

   .. method:: is_global()

      Trả về ``True`` nếu ký hiệu là biến toàn cục.

   .. method:: is_nonlocal()

      Trả về ``True`` nếu ký hiệu là biến nonlocal.

   .. method:: is_declared_global()

      Trả về ``True`` nếu ký hiệu được khai báo là global bằng câu lệnh global.

   .. method:: is_local()

      Trả về ``True`` nếu ký hiệu là biến cục bộ trong khối của nó.

   .. method:: is_annotated()

      Trả về ``True`` nếu ký hiệu có chú thích.

      .. versionadded:: 3.6

   .. method:: is_free()

      Trả về ``True`` nếu ký hiệu được tham chiếu trong khối của nó nhưng không được gán giá trị.

   .. method:: is_free_class()

      Trả về *True* nếu một symbol có phạm vi lớp là biến tự do từ góc nhìn của một phương thức.

      Xét ví dụ sau::

         def f():
             x = 1  # phạm vi hàm
             class C:
                 x = 2  # phạm vi lớp
                 def method(self):
                     return x

      Trong ví dụ này, symbol có phạm vi lớp ``x`` được xem là biến tự do từ góc nhìn của ``C.method``, nhờ đó cho phép đối tượng sau trả về *1* tại runtime thay vì *2*.

      .. versionadded:: 3.14

   .. method:: is_assigned()

      Trả về ``True`` nếu symbol được gán giá trị trong block của nó.

   .. method:: is_comp_iter()

      Trả về ``True`` nếu symbol là biến lặp của một phép comprehension.

      .. versionadded:: 3.14

   .. method:: is_comp_cell()

      Trả về ``True`` nếu symbol là một cell trong một comprehension được nội tuyến.

      .. versionadded:: 3.14

   .. method:: is_namespace()

      Trả về ``True`` nếu việc liên kết tên tạo ra namespace mới.

      Điều này sẽ đúng nếu tên được sử dụng làm đích của một câu lệnh function hoặc class.

      Ví dụ::

         >>> table = symtable.symtable("def some_func(): pass", "string", "exec")
         >>> table.lookup("some_func").is_namespace()
         True

      Lưu ý rằng một tên có thể được liên kết với nhiều đối tượng. Nếu kết quả là ``True``, tên cũng có thể được liên kết với các đối tượng khác, chẳng hạn như int hoặc list, vốn không tạo ra namespace mới.

   .. method:: get_namespaces()

      Trả về danh sách các namespace được liên kết với tên này.

   .. method:: get_namespace()

      Trả về namespace được liên kết với tên này. Nếu có nhiều hơn một hoặc không có namespace nào được liên kết với tên này, một :exc:`ValueError` sẽ được phát sinh.


.. _symtable-cli:

Cách sử dụng trên dòng lệnh
---------------------------

.. versionadded:: 3.13

Mô-đun :mod:`!symtable` có thể được thực thi dưới dạng một tập lệnh từ dòng lệnh.

.. code-block:: sh

   python -m symtable [infile...]

Các bảng ký hiệu được tạo cho những tệp mã nguồn Python được chỉ định và xuất ra stdout. Nếu không chỉ định tệp đầu vào, nội dung sẽ được đọc từ stdin.
