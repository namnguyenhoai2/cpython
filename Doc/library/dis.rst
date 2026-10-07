:mod:`!dis` --- Trình dịch ngược bytecode Python
================================================

.. module:: dis
   :synopsis: Trình dịch ngược bytecode Python.

**Mã nguồn:** :source:`Lib/dis.py`

.. testsetup::

   import dis
   def myfunc(alist):
       return len(alist)

--------------

Mô-đun :mod:`!dis` hỗ trợ việc phân tích :term:`bytecode` của CPython bằng cách dịch ngược nó. Bytecode CPython mà mô-đun này nhận làm đầu vào được định nghĩa trong tệp :file:`Include/opcode.h` và được trình biên dịch cùng trình thông dịch sử dụng.

.. impl-detail::

   Bytecode là một chi tiết triển khai của trình thông dịch CPython. Không có gì đảm bảo rằng bytecode sẽ không được thêm, xóa hoặc thay đổi giữa các phiên bản Python. Không nên xem việc sử dụng mô-đun này là có thể hoạt động trên các Python VM hoặc các bản phát hành Python khác nhau.

   .. versionchanged:: 3.6
      Sử dụng 2 byte cho mỗi instruction. Trước đây, số byte thay đổi tùy theo instruction.

   .. versionchanged:: 3.10
      Đối số của các instruction nhảy, xử lý ngoại lệ và vòng lặp hiện là offset của instruction thay vì offset byte.

   .. versionchanged:: 3.11
      Một số lệnh đi kèm với một hoặc nhiều mục nhập bộ nhớ đệm nội tuyến, có dạng các lệnh :opcode:`CACHE`. Theo mặc định, các lệnh này bị ẩn, nhưng có thể hiển thị bằng cách truyền ``show_caches=True`` cho bất kỳ tiện ích :mod:`!dis` nào. Ngoài ra, interpreter hiện điều chỉnh bytecode để chuyên biệt hóa nó cho các điều kiện runtime khác nhau. Có thể hiển thị bytecode thích ứng bằng cách truyền ``adaptive=True``.

   .. versionchanged:: 3.12
      Đối số của một lệnh nhảy là độ lệch của lệnh đích so với lệnh xuất hiện ngay sau lệnh nhảy
      Các mục nhập :opcode:`CACHE`.

      Do đó, sự hiện diện của các lệnh :opcode:`CACHE` không ảnh hưởng đến các lệnh nhảy tiến, nhưng cần được tính đến khi phân tích các lệnh nhảy lùi.

   .. versionchanged:: 3.13
      Đầu ra hiển thị các nhãn logic thay vì độ lệch lệnh cho các đích nhảy và trình xử lý ngoại lệ. Tùy chọn dòng lệnh ``-O`` và đối số ``show_offsets`` đã được thêm vào.

   .. versionchanged:: 3.14
      Tùy chọn dòng lệnh :option:`-P <dis --show-positions>` và đối số ``show_positions`` đã được thêm vào.

      Tùy chọn dòng lệnh :option:`-S <dis --specialized>` được thêm vào.

Ví dụ: Với hàm :func:`!myfunc`::

   def myfunc(alist):
       return len(alist)

có thể sử dụng lệnh sau để hiển thị mã disassembly của hàm
:func:`!myfunc`:

.. doctest::

   >>> dis.dis(myfunc)
     2           RESUME                   0
   <BLANKLINE>
     3           LOAD_GLOBAL              1 (len + NULL)
                 LOAD_FAST_BORROW         0 (alist)
                 CALL                     1
                 RETURN_VALUE

(“2” là số dòng).

.. _dis-cli:

Giao diện dòng lệnh
-------------------

Có thể gọi mô-đun :mod:`!dis` dưới dạng script từ dòng lệnh:

.. code-block:: sh

   python -m dis [-h] [-C] [-O] [-P] [-S] [infile]

Các tùy chọn sau được chấp nhận:

.. program:: dis

.. option:: -h, --help

   Hiển thị thông tin sử dụng rồi thoát.

.. option:: -C, --show-caches

   Hiển thị các inline cache.

   .. versionadded:: 3.13

.. option:: -O, --show-offsets

   Hiển thị các offset của instruction.

   .. versionadded:: 3.13

.. option:: -P, --show-positions

   Hiển thị vị trí của các instruction trong mã nguồn.

   .. versionadded:: 3.14

.. option:: -S, --specialized

   Hiển thị bytecode chuyên biệt.

   .. versionadded:: 3.14

Nếu chỉ định :file:`infile`, mã đã được disassemble của mã đó sẽ được ghi vào stdout. Nếu không, việc disassemble sẽ được thực hiện trên mã nguồn đã biên dịch nhận được từ stdin.

Phân tích bytecode
------------------

.. versionadded:: 3.4

API phân tích bytecode cho phép các đoạn mã Python được bọc trong một
:class:`Bytecode` đối tượng cung cấp quyền truy cập dễ dàng vào thông tin chi tiết của mã đã biên dịch.

.. class:: Bytecode(x, *, first_line=None, current_offset=None,\
                    show_caches=False, adaptive=False, show_offsets=False,\ show_positions=False)

   Phân tích bytecode tương ứng với một hàm, generator, asynchronous generator, coroutine, method, chuỗi mã nguồn hoặc code object (do :func:`compile` trả về).

   Đây là một wrapper tiện ích bao quanh nhiều hàm được liệt kê bên dưới, đáng chú ý nhất là :func:`get_instructions`, vì việc lặp qua một instance :class:`Bytecode` sẽ trả về các thao tác bytecode dưới dạng các instance :class:`Instruction`.

   Nếu *first_line* không phải là ``None``, nó cho biết số dòng cần được báo cáo cho dòng mã nguồn đầu tiên trong đoạn mã đã disassemble. Nếu không, thông tin về dòng mã nguồn (nếu có) sẽ được lấy trực tiếp từ code object đã disassemble.

   Nếu *current_offset* không phải là ``None``, nó tham chiếu đến offset của một instruction trong đoạn mã đã disassemble. Việc thiết lập giá trị này sẽ khiến :meth:`.dis` hiển thị dấu chỉ báo "current instruction" bên cạnh opcode được chỉ định.

   Nếu *show_caches* là ``True``, :meth:`.dis` sẽ hiển thị các mục inline cache được interpreter sử dụng để specialize bytecode.

   Nếu *adaptive* là ``True``, :meth:`.dis` sẽ hiển thị bytecode chuyên biệt, có thể khác với bytecode ban đầu.

   Nếu *show_offsets* là ``True``, :meth:`.dis` sẽ bao gồm các offset của instruction trong đầu ra.

   Nếu *show_positions* là ``True``, :meth:`.dis` sẽ bao gồm các vị trí mã nguồn của instruction trong đầu ra.

   .. classmethod:: from_traceback(tb, *, show_caches=False)

      Tạo một instance :class:`Bytecode` từ traceback đã cho, đặt *current_offset* thành instruction gây ra exception.

   .. data:: codeobj

      Đối tượng code đã biên dịch.

   .. data:: first_line

      Dòng mã nguồn đầu tiên của đối tượng code (nếu có)

   .. method:: dis()

      Trả về chế độ xem được định dạng của các thao tác bytecode (giống như nội dung được in bởi
      :func:`dis.dis`, nhưng được trả về dưới dạng chuỗi nhiều dòng).

   .. method:: info()

      Trả về một chuỗi nhiều dòng đã được định dạng với thông tin chi tiết về đối tượng code, như :func:`code_info`.

   .. versionchanged:: 3.7
      Giờ đây có thể xử lý các đối tượng coroutine và asynchronous generator.

   .. versionchanged:: 3.11
      Đã thêm các tham số *show_caches* và *adaptive*.

   .. versionchanged:: 3.13
      Đã thêm tham số *show_offsets*.

   .. versionchanged:: 3.14
      Đã thêm tham số *show_positions*.

Ví dụ:

.. doctest::

    >>> bytecode = dis.Bytecode(myfunc)
    >>> for instr in bytecode:
    ...     print(instr.opname)
    ...
    RESUME
    LOAD_GLOBAL
    LOAD_FAST_BORROW
    CALL
    RETURN_VALUE


Các hàm phân tích
-----------------

Mô-đun :mod:`!dis` cũng định nghĩa các hàm phân tích sau đây để chuyển đổi trực tiếp đầu vào thành đầu ra mong muốn. Chúng có thể hữu ích khi chỉ thực hiện một thao tác duy nhất, vì đối tượng phân tích trung gian không hữu ích:

.. function:: code_info(x)

   Trả về một chuỗi nhiều dòng đã được định dạng, chứa thông tin chi tiết về đối tượng mã của hàm, generator, asynchronous generator, coroutine, phương thức, chuỗi mã nguồn hoặc đối tượng mã được cung cấp.

   Lưu ý rằng nội dung chính xác của các chuỗi thông tin mã phụ thuộc rất nhiều vào cách triển khai và có thể thay đổi tùy ý giữa các Python VM hoặc các bản phát hành Python.

   .. versionadded:: 3.2

   .. versionchanged:: 3.7
      Hiện tại, hàm này có thể xử lý các đối tượng coroutine và asynchronous generator.


.. function:: show_code(x, *, file=None)

   In thông tin chi tiết về đối tượng mã của hàm, phương thức, chuỗi mã nguồn hoặc đối tượng mã được cung cấp ra *file* (hoặc ``sys.stdout`` nếu không chỉ định *file*).

   Đây là cách viết tắt thuận tiện cho ``print(code_info(x), file=file)``, предназначено để khám phá tương tác tại dấu nhắc trình thông dịch.

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Đã thêm tham số *file*.


.. function:: dis(x=None, *, file=None, depth=None, show_caches=False,\
                  adaptive=False, show_offsets=False, show_positions=False)

   Giải mã đối tượng *x*. *x* có thể chỉ một module, một class, một method, một function, một generator, một asynchronous generator, một coroutine, một code object, một chuỗi mã nguồn hoặc một chuỗi byte của bytecode thô. Với một module, hàm này giải mã tất cả các function. Với một class, hàm này giải mã tất cả các method (bao gồm cả class method và static method). Với một code object hoặc chuỗi bytecode thô, hàm này in một dòng cho mỗi chỉ dẫn bytecode. Hàm này cũng giải mã đệ quy các code object lồng nhau. Chúng có thể bao gồm các biểu thức generator, các function lồng nhau, phần thân của các class lồng nhau và các code object được sử dụng cho :ref:`phạm vi chú thích <annotation-scopes>`. Các chuỗi trước tiên được biên dịch thành code object bằng hàm dựng sẵn :func:`compile` trước khi được giải mã. Nếu không cung cấp đối tượng nào, hàm này sẽ giải mã traceback gần nhất.

   Kết quả phân rã được ghi dưới dạng văn bản vào đối số *file* được cung cấp, nếu có, và vào ``sys.stdout`` nếu không.

   Độ sâu đệ quy tối đa được giới hạn bởi *depth*, trừ khi giá trị này là ``None``. ``depth=0`` có nghĩa là không đệ quy.

   Nếu *show_caches* là ``True``, hàm này sẽ hiển thị các mục nhập inline cache được interpreter sử dụng để chuyên biệt hóa bytecode.

   Nếu *adaptive* là ``True``, hàm này sẽ hiển thị bytecode đã được chuyên biệt hóa, có thể khác với bytecode ban đầu.

   .. versionchanged:: 3.4
      Đã thêm tham số *file*.

   .. versionchanged:: 3.7
      Đã triển khai việc disassemble đệ quy và thêm tham số *depth*.

   .. versionchanged:: 3.7
      Hiện tại, hàm này có thể xử lý các đối tượng coroutine và asynchronous generator.

   .. versionchanged:: 3.11
      Đã thêm các tham số *show_caches* và *adaptive*.

   .. versionchanged:: 3.13
      Đã thêm tham số *show_offsets*.

   .. versionchanged:: 3.14
      Đã thêm tham số *show_positions*.

.. function:: distb(tb=None, *, file=None, show_caches=False, adaptive=False,\
                    show_offset=False, show_positions=False)

   Dịch ngược hàm ở đỉnh ngăn xếp của traceback, sử dụng traceback gần nhất nếu không truyền traceback nào. Lệnh gây ra ngoại lệ sẽ được chỉ ra.

   Kết quả phân rã được ghi dưới dạng văn bản vào đối số *file* được cung cấp, nếu có, và vào ``sys.stdout`` nếu không.

   .. versionchanged:: 3.4
      Đã thêm tham số *file*.

   .. versionchanged:: 3.11
      Đã thêm các tham số *show_caches* và *adaptive*.

   .. versionchanged:: 3.13
      Đã thêm tham số *show_offsets*.

   .. versionchanged:: 3.14
      Đã thêm tham số *show_positions*.

.. function:: disassemble(code, lasti=-1, *, file=None, show_caches=False,\
                          adaptive=False, show_offsets=False, show_positions=False)
              disco(code, lasti=-1, *, file=None, show_caches=False, adaptive=False,\
                    show_offsets=False, show_positions=False)

   Giải mã một đối tượng code, cho biết instruction cuối cùng nếu *lasti* được cung cấp. Kết quả được chia thành các cột sau:

   #. vị trí trong mã nguồn của instruction. Thông tin vị trí đầy đủ được hiển thị nếu *show_positions* là true. Nếu không (mặc định), chỉ số dòng được hiển thị.
   #. instruction hiện tại, được biểu thị bằng ``-->``,
   #. instruction được gắn nhãn, được biểu thị bằng ``>>``,
   #. địa chỉ của instruction,
   #. tên mã thao tác,
   #. các tham số thao tác, và
   #. diễn giải các tham số trong dấu ngoặc đơn.

   Phần diễn giải tham số nhận diện tên biến cục bộ và toàn cục, các giá trị hằng, đích nhánh và các toán tử so sánh.

   Kết quả phân rã được ghi dưới dạng văn bản vào đối số *file* được cung cấp, nếu có, và vào ``sys.stdout`` nếu không.

   .. versionchanged:: 3.4
      Đã thêm tham số *file*.

   .. versionchanged:: 3.11
      Đã thêm các tham số *show_caches* và *adaptive*.

   .. versionchanged:: 3.13
      Đã thêm tham số *show_offsets*.

   .. versionchanged:: 3.14
      Đã thêm tham số *show_positions*.

.. function:: get_instructions(x, *, first_line=None, show_caches=False, adaptive=False)

   Trả về một bộ lặp trên các instruction trong function, method, chuỗi mã nguồn hoặc code object được cung cấp.

   Bộ lặp tạo ra một chuỗi các tuple có tên :class:`Instruction` cung cấp thông tin chi tiết về từng operation trong đoạn code được cung cấp.

   Nếu *first_line* không phải là ``None``, giá trị này cho biết số dòng cần được báo cáo cho dòng mã nguồn đầu tiên trong code đã disassemble. Nếu không, thông tin về dòng mã nguồn (nếu có) được lấy trực tiếp từ code object đã disassemble.

   Tham số *adaptive* hoạt động giống như trong :func:`dis`.

   .. versionadded:: 3.4

   .. versionchanged:: 3.11
      Đã thêm các tham số *show_caches* và *adaptive*.

   .. versionchanged:: 3.13
      Tham số *show_caches* đã không còn được dùng và không có tác dụng. Iterator tạo ra các instance :class:`Instruction` với trường *cache_info* được điền dữ liệu (bất kể giá trị của *show_caches*) và không còn tạo các mục riêng cho các mục nhập bộ nhớ đệm.

.. function:: findlinestarts(code)

   Hàm generator này sử dụng phương thức :meth:`~codeobject.co_lines` của đối tượng :ref:`code object <code-objects>` *code* để tìm các offset là vị trí bắt đầu của các dòng trong mã nguồn. Các offset này được tạo dưới dạng các cặp ``(offset, lineno)``.

   .. versionchanged:: 3.6
      Số dòng có thể giảm dần. Trước đây, chúng luôn tăng dần.

   .. versionchanged:: 3.10
      Phương thức :pep:`626` :meth:`~codeobject.co_lines` được sử dụng thay cho
      các thuộc tính :attr:`~codeobject.co_firstlineno` và :attr:`~codeobject.co_lnotab` của đối tượng :ref:`code object <code-objects>`.

   .. versionchanged:: 3.13
      Số dòng có thể là ``None`` đối với bytecode không ánh xạ tới các dòng trong mã nguồn.


.. function:: findlabels(code)

   Phát hiện tất cả các offset trong chuỗi bytecode đã biên dịch thô *code* là các đích nhảy, rồi trả về danh sách các offset này.


.. function:: stack_effect(opcode, oparg=None, *, jump=None)

   Tính hiệu ứng ngăn xếp của *opcode* với đối số *oparg*.

   Nếu mã có đích nhảy và *jump* là ``True``, :func:`~stack_effect` sẽ trả về hiệu ứng ngăn xếp của việc nhảy. Nếu *jump* là ``False``, nó sẽ trả về hiệu ứng ngăn xếp của việc không nhảy. Và nếu *jump* là ``None`` (mặc định), nó sẽ trả về hiệu ứng ngăn xếp lớn nhất trong cả hai trường hợp.

   .. versionadded:: 3.4

   .. versionchanged:: 3.8
      Đã thêm tham số *jump*.

   .. versionchanged:: 3.13
      Nếu ``oparg`` bị bỏ qua (hoặc là ``None``), hiệu ứng ngăn xếp hiện được trả về cho ``oparg=0``. Trước đây, đây là lỗi đối với các opcode sử dụng đối số của chúng. Việc truyền một số nguyên ``oparg`` khi ``opcode`` không sử dụng nó cũng không còn là lỗi; ``oparg`` trong trường hợp này sẽ bị bỏ qua.


.. _bytecodes:

Các lệnh Bytecode Python
------------------------

Hàm :func:`get_instructions` và lớp :class:`Bytecode` cung cấp thông tin chi tiết về các lệnh bytecode dưới dạng các thực thể :class:`Instruction`:

.. class:: Instruction

   Thông tin chi tiết về một thao tác bytecode

   .. data:: opcode

      mã số dạng số của thao tác, tương ứng với các giá trị opcode được liệt kê bên dưới và các giá trị bytecode trong :ref:`opcode_collections`.


   .. data:: opname

      tên thao tác ở dạng dễ đọc


   .. data:: baseopcode

      mã số dạng số của thao tác cơ sở nếu thao tác được chuyên biệt hóa; nếu không thì bằng :data:`opcode`


   .. data:: baseopname

      tên thao tác cơ sở ở dạng dễ đọc nếu thao tác được chuyên biệt hóa; nếu không thì bằng :data:`opname`


   .. data:: arg

      đối số dạng số của thao tác (nếu có), nếu không thì là ``None``

   .. data:: oparg

      bí danh của :data:`arg`

   .. data:: argval

      giá trị đối số đã được phân giải (nếu có), nếu không thì là ``None``


   .. data:: argrepr

      mô tả dễ đọc đối với đối số của thao tác (nếu có), nếu không thì là một chuỗi rỗng.


   .. data:: offset

      chỉ mục bắt đầu của thao tác trong chuỗi bytecode


   .. data:: start_offset

      chỉ mục bắt đầu của thao tác trong chuỗi bytecode, bao gồm các thao tác ``EXTENDED_ARG`` có tiền tố nếu có; nếu không thì bằng :data:`offset`


   .. data:: cache_offset

      chỉ mục bắt đầu của các mục bộ nhớ đệm theo sau thao tác


   .. data:: end_offset

      chỉ mục kết thúc của các mục bộ nhớ đệm theo sau thao tác


   .. data:: starts_line

      ``True`` nếu opcode này bắt đầu một dòng mã nguồn, nếu không thì là ``False``


   .. data:: line_number

      số dòng mã nguồn liên kết với opcode này (nếu có), nếu không thì là ``None``


   .. data:: is_jump_target

      ``True`` nếu mã khác nhảy đến đây, nếu không thì ``False``


   .. data:: jump_target

      chỉ mục bytecode của đích nhảy nếu đây là một thao tác nhảy, nếu không thì ``None``


   .. data:: positions

      :class:`dis.Positions` đối tượng chứa vị trí bắt đầu và kết thúc được bao phủ bởi lệnh này.

   .. data:: cache_info

      Thông tin về các mục bộ nhớ đệm của lệnh này, dưới dạng các bộ ba có dạng ``(name, size, data)``, trong đó ``name`` và ``size`` mô tả định dạng bộ nhớ đệm, còn data là nội dung của bộ nhớ đệm. ``cache_info`` là ``None`` nếu lệnh không có bộ nhớ đệm.

   .. versionadded:: 3.4

   .. versionchanged:: 3.11

      Trường ``positions`` được thêm vào.

   .. versionchanged:: 3.13

      Trường ``starts_line`` đã được thay đổi.

      Đã thêm các trường ``start_offset``, ``cache_offset``, ``end_offset``, ``baseopname``, ``baseopcode``, ``jump_target``, ``oparg``, ``line_number`` và ``cache_info``.


.. class:: Positions

   Trong trường hợp không có thông tin, một số trường có thể bị ``None``.

   .. data:: lineno
   .. data:: end_lineno
   .. data:: col_offset
   .. data:: end_col_offset

   .. versionadded:: 3.11


Trình biên dịch Python hiện tạo ra các chỉ thị bytecode sau đây.


**Các chỉ thị chung**

Trong phần sau, chúng ta sẽ gọi stack của trình thông dịch là ``STACK`` và mô tả các thao tác trên đó như thể nó là một danh sách Python. Đỉnh stack tương ứng với ``STACK[-1]`` trong ngôn ngữ này.

.. opcode:: NOP

   Đoạn mã không thực hiện gì. Được trình tối ưu hóa bytecode sử dụng làm chỗ giữ chỗ và để tạo các sự kiện truy vết dòng.


.. opcode:: NOT_TAKEN

   Đoạn mã không thực hiện gì. Được trình thông dịch sử dụng để ghi lại các sự kiện :monitoring-event:`BRANCH_LEFT` và :monitoring-event:`BRANCH_RIGHT` cho :mod:`sys.monitoring`.

   .. versionadded:: 3.14


.. opcode:: POP_ITER

   Xóa iterator khỏi đỉnh stack.

   .. versionadded:: 3.14


.. opcode:: POP_TOP

   Xóa phần tử trên cùng của stack::

      STACK.pop()


.. opcode:: END_FOR

   Xóa phần tử trên cùng của stack. Tương đương với ``POP_TOP``. Được dùng để dọn dẹp ở cuối các vòng lặp, vì vậy mới có tên này.

   .. versionadded:: 3.12


.. opcode:: END_SEND

   Triển khai ``del STACK[-2]``. Được dùng để dọn dẹp khi generator kết thúc.

   .. versionadded:: 3.12


.. opcode:: COPY (i)

   Đưa phần tử thứ i lên trên cùng của stack mà không xóa phần tử đó khỏi vị trí ban đầu::

      assert i > 0
      STACK.append(STACK[-i])

   .. versionadded:: 3.11


.. opcode:: SWAP (i)

   Hoán đổi phần tử trên cùng của stack với phần tử thứ i::

      STACK[-i], STACK[-1] = STACK[-1], STACK[-i]

   .. versionadded:: 3.11


.. opcode:: CACHE

   Thay vì là một instruction thực sự, opcode này được dùng để đánh dấu phần bộ nhớ bổ sung để interpreter có thể lưu các dữ liệu hữu ích trực tiếp trong bytecode. Nó tự động bị ẩn bởi mọi tiện ích ``dis``, nhưng có thể xem bằng ``show_caches=True``.

   Về mặt logic, phần bộ nhớ này thuộc về instruction ngay trước đó. Nhiều opcode yêu cầu có chính xác một số lượng cache nhất định theo sau chúng và sẽ chỉ thị cho interpreter bỏ qua chúng trong runtime.

   Các bộ nhớ đệm đã được điền dữ liệu có thể trông giống như những chỉ dẫn tùy ý, vì vậy cần hết sức cẩn thận khi đọc hoặc sửa đổi bytecode thô, thích ứng có chứa dữ liệu quickened.

   .. versionadded:: 3.11


**Các phép toán một ngôi**

Các phép toán một ngôi lấy phần tử trên cùng của ngăn xếp, áp dụng phép toán rồi đẩy kết quả trở lại ngăn xếp.


.. opcode:: UNARY_NEGATIVE

   Triển khai ``STACK[-1] = -STACK[-1]``.


.. opcode:: UNARY_NOT

   Triển khai ``STACK[-1] = not STACK[-1]``.

   .. versionchanged:: 3.13
      Chỉ dẫn này hiện yêu cầu một toán hạng :class:`bool` chính xác.


.. opcode:: UNARY_INVERT

   Triển khai ``STACK[-1] = ~STACK[-1]``.


.. opcode:: GET_ITER

   Triển khai ``STACK[-1] = iter(STACK[-1])``.


.. opcode:: GET_YIELD_FROM_ITER

   Nếu ``STACK[-1]`` là một đối tượng :term:`generator iterator` hoặc :term:`coroutine`, nó được giữ nguyên. Nếu không, triển khai ``STACK[-1] = iter(STACK[-1])``.

   .. versionadded:: 3.5


.. opcode:: TO_BOOL

   Triển khai ``STACK[-1] = bool(STACK[-1])``.

   .. versionadded:: 3.13


**Các phép toán nhị phân và tại chỗ**

Các phép toán nhị phân loại bỏ hai phần tử trên cùng khỏi stack (``STACK[-1]`` và ``STACK[-2]``). Chúng thực hiện phép toán, sau đó đưa kết quả trở lại stack.

Các phép toán tại chỗ tương tự như phép toán nhị phân, nhưng phép toán được thực hiện tại chỗ khi ``STACK[-2]`` hỗ trợ, và ``STACK[-1]`` kết quả có thể (nhưng không nhất thiết) là ``STACK[-2]`` ban đầu.


.. opcode:: BINARY_OP (op)

   Triển khai các toán tử nhị phân và tại chỗ (tùy thuộc vào giá trị của *op*)::

      rhs = STACK.pop()
      lhs = STACK.pop()
      STACK.append(lhs op rhs)

   .. versionadded:: 3.11
   .. versionchanged:: 3.14
      Với oparg :``NB_SUBSCR``, triển khai phép lập chỉ mục nhị phân (thay thế opcode ``BINARY_SUBSCR``)


.. opcode:: STORE_SUBSCR

   Triển khai::

      key = STACK.pop()
      container = STACK.pop()
      value = STACK.pop()
      container[key] = value


.. opcode:: DELETE_SUBSCR

   Triển khai::

      key = STACK.pop()
      container = STACK.pop()
      del container[key]

.. opcode:: BINARY_SLICE

   Triển khai::

      end = STACK.pop()
      start = STACK.pop()
      container = STACK.pop()
      STACK.append(container[start:end])

   .. versionadded:: 3.12


.. opcode:: STORE_SLICE

   Triển khai::

      end = STACK.pop()
      start = STACK.pop()
      container = STACK.pop()
      value = STACK.pop()
      container[start:end] = value

   .. versionadded:: 3.12


**Các opcode coroutine**

.. opcode:: GET_AWAITABLE (where)

   Triển khai ``STACK[-1] = get_awaitable(STACK[-1])``, trong đó ``get_awaitable(o)`` trả về ``o`` nếu ``o`` là một đối tượng coroutine hoặc một đối tượng generator có cờ :data:`~inspect.CO_ITERABLE_COROUTINE`, hoặc resolve ``o.__await__``.

    Nếu toán hạng ``where`` khác 0, nó cho biết vị trí thực hiện lệnh:

    * ``1``: Sau một lệnh gọi đến ``__aenter__``
    * ``2``: Sau một lệnh gọi đến ``__aexit__``

   .. versionadded:: 3.5

   .. versionchanged:: 3.11
      Trước đây, lệnh này không có oparg.


.. opcode:: GET_AITER

   Triển khai ``STACK[-1] = STACK[-1].__aiter__()``.

   .. versionadded:: 3.5
   .. versionchanged:: 3.7
      Không còn hỗ trợ việc trả về các đối tượng awaitable từ ``__aiter__``.


.. opcode:: GET_ANEXT

   Đẩy ``STACK.append(get_awaitable(STACK[-1].__anext__()))`` lên ngăn xếp. Xem ``GET_AWAITABLE`` để biết chi tiết về ``get_awaitable``.

   .. versionadded:: 3.5


.. opcode:: END_ASYNC_FOR

   Kết thúc một vòng lặp :keyword:`async for`. Xử lý một ngoại lệ được phát sinh khi chờ mục tiếp theo. Ngăn xếp chứa iterable bất đồng bộ trong ``STACK[-2]`` và ngoại lệ được phát sinh trong ``STACK[-1]``. Cả hai đều được lấy ra khỏi ngăn xếp. Nếu ngoại lệ không phải là :exc:`StopAsyncIteration`, ngoại lệ đó sẽ được phát sinh lại.

   .. versionadded:: 3.8

   .. versionchanged:: 3.11
      Biểu diễn ngoại lệ trên ngăn xếp giờ đây chỉ gồm một mục thay vì ba mục.


.. opcode:: CLEANUP_THROW

   Xử lý một ngoại lệ được phát sinh trong quá trình thực hiện :meth:`~generator.throw` hoặc
   lệnh gọi :meth:`~generator.close` thông qua frame hiện tại. Nếu ``STACK[-1]`` là một thể hiện của :exc:`StopIteration`, lấy ba giá trị khỏi ngăn xếp và đẩy thành viên ``value`` của nó vào ngăn xếp. Nếu không, phát sinh lại ``STACK[-1]``.

   .. versionadded:: 3.12



**Các opcode khác**

.. opcode:: SET_ADD (i)

   Triển khai::

      item = STACK.pop()
      set.add(STACK[-i], item)

   Dùng để triển khai các phép dựng set.


.. opcode:: LIST_APPEND (i)

   Triển khai::

      item = STACK.pop()
      list.append(STACK[-i], item)

   Được dùng để triển khai list comprehension.


.. opcode:: MAP_ADD (i)

   Triển khai::

      value = STACK.pop()
      key = STACK.pop()
      dict.__setitem__(STACK[-i], key, value)

   Được dùng để triển khai dict comprehension.

   .. versionadded:: 3.1
   .. versionchanged:: 3.8
      Giá trị map là ``STACK[-1]`` và khóa map là ``STACK[-2]``. Trước đây, chúng bị đảo ngược.

Đối với tất cả các instruction :opcode:`SET_ADD`, :opcode:`LIST_APPEND` và :opcode:`MAP_ADD`, trong khi giá trị hoặc cặp khóa/giá trị được thêm vào bị lấy ra khỏi stack, đối tượng container vẫn nằm trên stack để có thể được sử dụng cho các lần lặp tiếp theo của vòng lặp.


.. opcode:: RETURN_VALUE

   Trả về cùng ``STACK[-1]`` cho hàm gọi.


.. opcode:: YIELD_VALUE

   Sinh ``STACK.pop()`` từ một :term:`generator`.

   .. versionchanged:: 3.11
      oparg được đặt là độ sâu ngăn xếp.

   .. versionchanged:: 3.12
      oparg được đặt là độ sâu của khối ngoại lệ để đóng các generator hiệu quả.

   .. versionchanged:: 3.13
      oparg là ``1`` nếu lệnh này là một phần của yield-from hoặc await, và ``0`` trong các trường hợp khác.

.. opcode:: SETUP_ANNOTATIONS

   Kiểm tra xem ``__annotations__`` có được định nghĩa trong ``locals()`` hay không; nếu không, nó được thiết lập thành một ``dict`` rỗng. Opcode này chỉ được phát ra nếu phần thân của lớp hoặc module tĩnh chứa :term:`chú thích biến <variable annotation>`.

   .. versionadded:: 3.6


.. opcode:: POP_EXCEPT

   Lấy một giá trị khỏi ngăn xếp; giá trị này được dùng để khôi phục trạng thái ngoại lệ.

   .. versionchanged:: 3.11
      Biểu diễn ngoại lệ trên ngăn xếp giờ đây chỉ gồm một mục thay vì ba mục.

.. opcode:: RERAISE

   Ném lại ngoại lệ hiện đang ở đỉnh ngăn xếp. Nếu oparg khác không, lấy thêm một giá trị khỏi ngăn xếp để dùng thiết lập
   :attr:`~frame.f_lasti` của frame hiện tại.

   .. versionadded:: 3.9

   .. versionchanged:: 3.11
      Biểu diễn ngoại lệ trên ngăn xếp giờ đây chỉ gồm một mục thay vì ba mục.

.. opcode:: PUSH_EXC_INFO

   Lấy một giá trị khỏi ngăn xếp. Đẩy ngoại lệ hiện tại lên đỉnh ngăn xếp. Đẩy lại giá trị vừa lấy vào ngăn xếp. Được sử dụng trong các trình xử lý ngoại lệ.

   .. versionadded:: 3.11

.. opcode:: CHECK_EXC_MATCH

   Thực hiện việc đối sánh ngoại lệ cho ``except``. Kiểm tra xem ``STACK[-2]`` có phải là ngoại lệ khớp với ``STACK[-1]`` hay không. Lấy ``STACK[-1]`` khỏi ngăn xếp và đẩy kết quả boolean của phép kiểm tra.

   .. versionadded:: 3.11

.. opcode:: CHECK_EG_MATCH

   Thực hiện việc đối sánh ngoại lệ cho ``except*``. Áp dụng ``split(STACK[-1])`` lên nhóm ngoại lệ đại diện cho ``STACK[-2]``.

   Trong trường hợp khớp, lấy hai mục khỏi ngăn xếp và đẩy nhóm con không khớp (``None`` trong trường hợp khớp hoàn toàn), sau đó là nhóm con khớp. Khi không có kết quả khớp, lấy một mục (kiểu khớp) và đẩy ``None``.

   .. versionadded:: 3.11

.. opcode:: WITH_EXCEPT_START

   Gọi hàm ở vị trí 4 trên stack với các đối số (type, val, tb) biểu diễn ngoại lệ ở đầu stack. Được dùng để triển khai lệnh gọi ``context_manager.__exit__(*exc_info())`` khi một ngoại lệ đã xảy ra trong câu lệnh :keyword:`with`.

   .. versionadded:: 3.9

   .. versionchanged:: 3.11
      Hàm ``__exit__`` nằm ở vị trí 4 trên stack thay vì vị trí 7. Biểu diễn ngoại lệ trên stack giờ đây chỉ gồm một mục thay vì ba mục.


.. opcode:: LOAD_COMMON_CONSTANT

   Đẩy một hằng số phổ biến lên stack. Trình thông dịch chứa một danh sách hằng số được hardcode mà instruction này hỗ trợ. Được dùng bởi câu lệnh :keyword:`assert` để tải :exc:`AssertionError`.

   .. versionadded:: 3.14


.. opcode:: LOAD_BUILD_CLASS

   Đẩy :func:`!builtins.__build_class__` lên stack. Sau đó, nó được gọi để tạo một class.

.. opcode:: GET_LEN

   Thực hiện ``STACK.append(len(STACK[-1]))``. Được dùng trong các câu lệnh :keyword:`match` khi cần so sánh với cấu trúc của pattern.

   .. versionadded:: 3.10


.. opcode:: MATCH_MAPPING

   Nếu ``STACK[-1]`` là một instance của :class:`collections.abc.Mapping` (hoặc, chính xác hơn về mặt kỹ thuật: nếu nó có cờ :c:macro:`Py_TPFLAGS_MAPPING` được đặt trong
   :c:member:`~PyTypeObject.tp_flags`), đẩy ``True`` lên stack. Nếu không, đẩy ``False``.

   .. versionadded:: 3.10


.. opcode:: MATCH_SEQUENCE

   Nếu ``STACK[-1]`` là một thể hiện của :class:`collections.abc.Sequence` và *không phải* là một thể hiện của :class:`str`/:class:`bytes`/:class:`bytearray` (hoặc chính xác hơn: nếu nó có cờ :c:macro:`Py_TPFLAGS_SEQUENCE` được thiết lập trong :c:member:`~PyTypeObject.tp_flags`), đẩy ``True`` vào stack. Nếu không, đẩy ``False``.

   .. versionadded:: 3.10


.. opcode:: MATCH_KEYS

   ``STACK[-1]`` là một tuple gồm các khóa ánh xạ, còn ``STACK[-2]`` là đối tượng được so khớp. Nếu ``STACK[-2]`` chứa tất cả các khóa trong ``STACK[-1]``, đẩy một :class:`tuple` chứa các giá trị tương ứng. Nếu không, đẩy ``None``.

   .. versionadded:: 3.10

   .. versionchanged:: 3.11
      Trước đây, instruction này cũng đẩy một giá trị boolean cho biết thao tác thành công (``True``) hay thất bại (``False``).


.. opcode:: STORE_NAME (namei)

   Triển khai ``name = STACK.pop()``. *namei* là chỉ mục của *name* trong thuộc tính
   :attr:`~codeobject.co_names` của đối tượng :ref:`code object <code-objects>`. Trình biên dịch cố gắng sử dụng :opcode:`STORE_FAST` hoặc :opcode:`STORE_GLOBAL` nếu có thể.


.. opcode:: DELETE_NAME (namei)

   Triển khai ``del name``, trong đó *namei* là chỉ mục trong thuộc tính :attr:`~codeobject.co_names` của đối tượng :ref:`code object <code-objects>`.


.. opcode:: UNPACK_SEQUENCE (count)

   Giải nén ``STACK[-1]`` thành *count* giá trị riêng lẻ, được đưa vào stack từ phải sang trái. Yêu cầu phải có chính xác *count* giá trị.::

      assert(len(STACK[-1]) == count)
      STACK.extend(STACK.pop()[:-count-1:-1])


.. opcode:: UNPACK_EX (counts)

   Triển khai phép gán với đích có dấu sao: Giải nén một iterable trong ``STACK[-1]`` thành các giá trị riêng lẻ, trong đó tổng số giá trị có thể nhỏ hơn số lượng phần tử trong iterable: một trong các giá trị mới sẽ là một list chứa tất cả các phần tử còn lại.

   Số lượng giá trị trước và sau giá trị list được giới hạn ở mức 255.

   Số lượng giá trị trước giá trị list được mã hóa trong đối số của opcode. Số lượng giá trị sau list, nếu có, được mã hóa bằng ``EXTENDED_ARG``. Do đó, đối số có thể được xem là một giá trị gồm hai byte, trong đó byte thấp của *counts* là số lượng giá trị trước giá trị list, còn byte cao của *counts* là số lượng giá trị sau nó.

   Các giá trị được trích xuất được đưa vào stack theo thứ tự từ phải sang trái, tức là ``a, *b, c = d`` sẽ được lưu trữ sau khi thực thi dưới dạng ``STACK.extend((a, b, c))``.


.. opcode:: STORE_ATTR (namei)

   Triển khai::

      obj = STACK.pop()
      value = STACK.pop()
      obj.name = value

   trong đó *namei* là chỉ mục của name trong :attr:`~codeobject.co_names` của
   đối tượng :ref:`code object <code-objects>`.

.. opcode:: DELETE_ATTR (namei)

   Triển khai::

      obj = STACK.pop()
      del obj.name

   trong đó *namei* là chỉ mục của name trong :attr:`~codeobject.co_names` của
   đối tượng :ref:`code object <code-objects>`.


.. opcode:: STORE_GLOBAL (namei)

   Hoạt động như :opcode:`STORE_NAME`, nhưng lưu name dưới dạng biến toàn cục.


.. opcode:: DELETE_GLOBAL (namei)

   Hoạt động như :opcode:`DELETE_NAME`, nhưng xóa một name toàn cục.


.. opcode:: LOAD_CONST (consti)

   Đẩy ``co_consts[consti]`` lên stack.


.. opcode:: LOAD_SMALL_INT (i)

   Đẩy số nguyên ``i`` lên stack. ``i`` phải nằm trong ``range(256)``

   .. versionadded:: 3.14


.. opcode:: LOAD_NAME (namei)

   Đẩy giá trị liên kết với ``co_names[namei]`` lên stack. Tên này được tra cứu trong locals, sau đó globals, rồi builtins.


.. opcode:: LOAD_LOCALS

   Đẩy một tham chiếu đến từ điển locals lên stack. Thao tác này được dùng để chuẩn bị các từ điển namespace cho :opcode:`LOAD_FROM_DICT_OR_DEREF` và :opcode:`LOAD_FROM_DICT_OR_GLOBALS`.

   .. versionadded:: 3.12


.. opcode:: LOAD_FROM_DICT_OR_GLOBALS (i)

   Lấy một mapping khỏi stack và tra cứu giá trị của ``co_names[namei]``. Nếu không tìm thấy tên ở đó, tra cứu tên trong globals rồi đến builtins, tương tự như :opcode:`LOAD_GLOBAL`. Thao tác này được dùng để nạp các biến toàn cục trong
   :ref:`annotation scopes <annotation-scopes>` bên trong các thân lớp.

   .. versionadded:: 3.12


.. opcode:: BUILD_TEMPLATE

   Tạo một instance :class:`~string.templatelib.Template` mới từ một tuple gồm các chuỗi và một tuple gồm các phép nội suy, rồi đẩy đối tượng kết quả lên stack::

      interpolations = STACK.pop()
      strings = STACK.pop()
      STACK.append(_build_template(strings, interpolations))

   .. versionadded:: 3.14


.. opcode:: BUILD_INTERPOLATION (format)

   Tạo một instance :class:`~string.templatelib.Interpolation` mới từ một giá trị và biểu thức nguồn của giá trị đó, rồi đẩy đối tượng kết quả lên stack.

   Nếu không có đặc tả chuyển đổi hoặc định dạng, ``format`` được đặt thành ``2``.

   Nếu bit thấp nhất của ``format`` được thiết lập, điều đó cho biết phép nội suy chứa đặc tả định dạng.

   Nếu ``format >> 2`` khác không, điều đó cho biết phép nội suy chứa một phép chuyển đổi. Giá trị của ``format >> 2`` là kiểu chuyển đổi (``0`` khi không có chuyển đổi, ``1`` cho ``!s``, ``2`` cho ``!r`` và ``3`` cho ``!a``).::

      conversion = format >> 2
      if format & 1:
          format_spec = STACK.pop()
      else:
          format_spec = None
      expression = STACK.pop()
      value = STACK.pop()
      STACK.append(_build_interpolation(value, expression, conversion, format_spec))

   .. versionadded:: 3.14


.. opcode:: BUILD_TUPLE (count)

   Tạo một tuple bằng cách lấy *count* mục từ stack, rồi đẩy tuple kết quả vào stack::

      if count == 0:
          value = ()
      else:
          value = tuple(STACK[-count:])
          STACK = STACK[:-count]

      STACK.append(value)


.. opcode:: BUILD_LIST (count)

   Hoạt động như :opcode:`BUILD_TUPLE`, nhưng tạo một list.


.. opcode:: BUILD_SET (count)

   Hoạt động như :opcode:`BUILD_TUPLE`, nhưng tạo một set.


.. opcode:: BUILD_MAP (count)

   Đẩy một đối tượng dictionary mới vào stack. Lấy ``2 * count`` mục ra khỏi stack để dictionary chứa *count* mục: ``{..., STACK[-4]: STACK[-3], STACK[-2]: STACK[-1]}``.

   .. versionchanged:: 3.5
      Dictionary được tạo từ các mục trên stack thay vì tạo một dictionary rỗng có kích thước định trước để chứa *count* mục.


.. opcode:: BUILD_STRING (count)

   Nối *count* chuỗi từ stack và đẩy chuỗi kết quả lên stack.

   .. versionadded:: 3.6


.. opcode:: LIST_EXTEND (i)

   Triển khai::

      seq = STACK.pop()
      list.extend(STACK[-i], seq)

   Dùng để tạo lists.

   .. versionadded:: 3.9


.. opcode:: SET_UPDATE (i)

   Triển khai::

      seq = STACK.pop()
      set.update(STACK[-i], seq)

   Dùng để tạo sets.

   .. versionadded:: 3.9


.. opcode:: DICT_UPDATE (i)

   Triển khai::

      map = STACK.pop()
      dict.update(STACK[-i], map)

   Dùng để tạo dicts.

   .. versionadded:: 3.9


.. opcode:: DICT_MERGE (i)

   Tương tự :opcode:`DICT_UPDATE` nhưng sẽ raise exception khi có các key trùng lặp.

   .. versionadded:: 3.9


.. opcode:: LOAD_ATTR (namei)

   Nếu bit thấp của ``namei`` không được thiết lập, lệnh này thay thế ``STACK[-1]`` bằng ``getattr(STACK[-1], co_names[namei>>1])``.

   Nếu bit thấp của ``namei`` được thiết lập, lệnh này sẽ cố gắng tải một method có tên ``co_names[namei>>1]`` từ object ``STACK[-1]``. ``STACK[-1]`` được lấy ra khỏi stack. Bytecode này phân biệt hai trường hợp: nếu ``STACK[-1]`` có method với tên phù hợp, bytecode sẽ đẩy unbound method và ``STACK[-1]`` lên stack. ``STACK[-1]`` sẽ được :opcode:`CALL` hoặc :opcode:`CALL_KW` sử dụng làm đối số đầu tiên (``self``) khi gọi unbound method. Nếu không, ``NULL`` và object được trả về bởi phép tra cứu thuộc tính sẽ được đẩy lên stack.

   .. versionchanged:: 3.12
      Nếu bit thấp của ``namei`` được thiết lập, một ``NULL`` hoặc ``self`` sẽ được đẩy lên stack, lần lượt trước thuộc tính hoặc unbound method.


.. opcode:: LOAD_SUPER_ATTR (namei)

   Opcode này triển khai :func:`super`, cả ở dạng không đối số và dạng hai đối số (ví dụ: ``super().method()``, ``super().attr`` và ``super(cls, self).method()``, ``super(cls, self).attr``).

   Lệnh này lấy ba giá trị ra khỏi stack (từ đỉnh stack trở xuống):

   * ``self``: đối số đầu tiên của method hiện tại
   * ``cls``: lớp mà trong đó phương thức hiện tại được định nghĩa
   * ``super`` toàn cục

   Đối với đối số của nó, nó hoạt động tương tự như :opcode:`LOAD_ATTR`, ngoại trừ việc ``namei`` được dịch trái 2 bit thay vì 1 bit.

   Bit thấp nhất của ``namei`` báo hiệu việc thử tải một phương thức, như với
   :opcode:`LOAD_ATTR`, thao tác này đẩy ``NULL`` và phương thức đã tải vào ngăn xếp. Khi bit này không được đặt, một giá trị duy nhất được đẩy vào ngăn xếp.

   Bit thấp thứ hai của ``namei``, nếu được đặt, nghĩa là đây là một lệnh gọi có hai đối số đến :func:`super` (không được đặt nghĩa là không có đối số).

   .. versionadded:: 3.12


.. opcode:: COMPARE_OP (opname)

   Thực hiện một phép toán Boolean. Tên phép toán có thể được tìm thấy trong ``cmp_op[opname >> 5]``. Nếu bit thấp thứ năm của ``opname`` được đặt (``opname & 16``), kết quả phải được ép kiểu thành ``bool``.

   .. versionchanged:: 3.13
      Bit thấp thứ năm của oparg hiện cho biết việc ép chuyển đổi thành
      :class:`bool`.


.. opcode:: IS_OP (invert)

   Thực hiện phép so sánh ``is``, hoặc ``is not`` nếu ``invert`` là 1.

   .. versionadded:: 3.9


.. opcode:: CONTAINS_OP (invert)

   Thực hiện phép so sánh ``in``, hoặc ``not in`` nếu ``invert`` là 1.

   .. versionadded:: 3.9


.. opcode:: IMPORT_NAME (namei)

   Nhập module ``co_names[namei]``. ``STACK[-1]`` và ``STACK[-2]`` được lấy khỏi stack và cung cấp các đối số *fromlist* và *level* của :func:`__import__`. Đối tượng module được đẩy lên stack. Namespace hiện tại không bị ảnh hưởng: để có một câu lệnh import đúng nghĩa, một lệnh :opcode:`STORE_FAST` tiếp theo sẽ sửa đổi namespace.


.. opcode:: IMPORT_FROM (namei)

   Tải thuộc tính ``co_names[namei]`` từ module được tìm thấy trong ``STACK[-1]``. Đối tượng kết quả được đẩy lên stack để sau đó được lưu bởi một
   lệnh :opcode:`STORE_FAST`.


.. opcode:: JUMP_FORWARD (delta)

   Tăng bộ đếm bytecode thêm *delta*.


.. opcode:: JUMP_BACKWARD (delta)

   Giảm bộ đếm bytecode đi *delta*. Kiểm tra các ngắt.

   .. versionadded:: 3.11


.. opcode:: JUMP_BACKWARD_NO_INTERRUPT (delta)

   Giảm bộ đếm bytecode đi *delta*. Không kiểm tra các ngắt.

   .. versionadded:: 3.11


.. opcode:: POP_JUMP_IF_TRUE (delta)

   Nếu ``STACK[-1]`` là true, tăng bộ đếm bytecode thêm *delta*. ``STACK[-1]`` được lấy ra khỏi ngăn xếp.

   .. versionchanged:: 3.11
      oparg giờ đây là một delta tương đối thay vì một đích tuyệt đối. Opcode này là một pseudo-instruction, được thay thế trong bytecode cuối cùng bằng các phiên bản có hướng (tiến/lùi).

   .. versionchanged:: 3.12
      Đây không còn là một pseudo-instruction nữa.

   .. versionchanged:: 3.13
      Chỉ dẫn này hiện yêu cầu một toán hạng :class:`bool` chính xác.

.. opcode:: POP_JUMP_IF_FALSE (delta)

   Nếu ``STACK[-1]`` là false, tăng bộ đếm bytecode thêm *delta*. ``STACK[-1]`` được lấy ra khỏi ngăn xếp.

   .. versionchanged:: 3.11
      oparg giờ đây là một delta tương đối thay vì một đích tuyệt đối. Opcode này là một pseudo-instruction, được thay thế trong bytecode cuối cùng bằng các phiên bản có hướng (tiến/lùi).

   .. versionchanged:: 3.12
      Đây không còn là một pseudo-instruction nữa.

   .. versionchanged:: 3.13
      Chỉ dẫn này hiện yêu cầu một toán hạng :class:`bool` chính xác.

.. opcode:: POP_JUMP_IF_NOT_NONE (delta)

   Nếu ``STACK[-1]`` không phải ``None``, bộ đếm bytecode được tăng thêm *delta*. ``STACK[-1]`` được lấy ra khỏi ngăn xếp.

   .. versionadded:: 3.11

   .. versionchanged:: 3.12
      Đây không còn là một pseudo-instruction nữa.


.. opcode:: POP_JUMP_IF_NONE (delta)

   Nếu ``STACK[-1]`` là ``None``, bộ đếm bytecode được tăng thêm *delta*. ``STACK[-1]`` được lấy ra khỏi ngăn xếp.

   .. versionadded:: 3.11

   .. versionchanged:: 3.12
      Đây không còn là một pseudo-instruction nữa.

.. opcode:: FOR_ITER (delta)

   ``STACK[-1]`` là một :term:`iterator`. Gọi phương thức :meth:`~iterator.__next__` của nó. Nếu thao tác này tạo ra một giá trị mới, hãy đẩy giá trị đó vào stack (giữ iterator bên dưới nó). Nếu iterator cho biết nó đã :term:`exhausted` thì bộ đếm bytecode được tăng thêm *delta*.

   .. versionchanged:: 3.12
      Cho đến phiên bản 3.11, iterator bị lấy khỏi stack khi đã cạn.

.. opcode:: LOAD_GLOBAL (namei)

   Tải global có tên ``co_names[namei>>1]`` lên stack.

   .. versionchanged:: 3.11
      Nếu bit thấp của ``namei`` được đặt, thì một ``NULL`` được đẩy vào stack trước biến global.

.. opcode:: LOAD_FAST (var_num)

   Đẩy một tham chiếu đến local ``co_varnames[var_num]`` lên stack.

   .. versionchanged:: 3.12
      Opcode này hiện chỉ được sử dụng trong những tình huống mà local được đảm bảo đã được khởi tạo. Nó không thể phát sinh :exc:`UnboundLocalError`.

.. opcode:: LOAD_FAST_BORROW (var_num)

   Đẩy một tham chiếu mượn đến local ``co_varnames[var_num]`` lên stack.

   .. versionadded:: 3.14

.. opcode:: LOAD_FAST_LOAD_FAST (var_nums)

   Đẩy các tham chiếu đến ``co_varnames[var_nums >> 4]`` và ``co_varnames[var_nums & 15]`` lên stack.

   .. versionadded:: 3.13


.. opcode:: LOAD_FAST_BORROW_LOAD_FAST_BORROW (var_nums)

   Đẩy các tham chiếu mượn đến ``co_varnames[var_nums >> 4]`` và ``co_varnames[var_nums & 15]`` lên stack.

   .. versionadded:: 3.14

.. opcode:: LOAD_FAST_CHECK (var_num)

   Đẩy một tham chiếu đến biến cục bộ ``co_varnames[var_num]`` lên stack, đồng thời phát sinh :exc:`UnboundLocalError` nếu biến cục bộ chưa được khởi tạo.

   .. versionadded:: 3.12

.. opcode:: LOAD_FAST_AND_CLEAR (var_num)

   Đẩy một tham chiếu đến biến cục bộ ``co_varnames[var_num]`` lên stack (hoặc đẩy ``NULL`` lên stack nếu biến cục bộ chưa được khởi tạo), rồi đặt ``co_varnames[var_num]`` thành ``NULL``.

   .. versionadded:: 3.12

.. opcode:: STORE_FAST (var_num)

   Lưu ``STACK.pop()`` vào biến cục bộ ``co_varnames[var_num]``.

.. opcode:: STORE_FAST_STORE_FAST (var_nums)

   Lưu ``STACK[-1]`` vào ``co_varnames[var_nums >> 4]`` và ``STACK[-2]`` vào ``co_varnames[var_nums & 15]``.

   .. versionadded:: 3.13

.. opcode:: STORE_FAST_LOAD_FAST (var_nums)

   Lưu ``STACK.pop()`` vào biến cục bộ ``co_varnames[var_nums >> 4]`` và đẩy một tham chiếu đến biến cục bộ ``co_varnames[var_nums & 15]`` lên stack.

   .. versionadded:: 3.13

.. opcode:: DELETE_FAST (var_num)

   Xóa ``co_varnames[var_num]`` cục bộ.


.. opcode:: MAKE_CELL (i)

   Tạo một cell mới tại vị trí ``i``. Nếu vị trí đó không rỗng thì giá trị đó được lưu vào cell mới.

   .. versionadded:: 3.11


.. opcode:: LOAD_DEREF (i)

   Tải cell nằm ở vị trí ``i`` trong bộ lưu trữ "fast locals". Đẩy một tham chiếu đến đối tượng mà cell chứa lên stack.

   .. versionchanged:: 3.11
      ``i`` không còn được tính lệch theo độ dài của :attr:`~codeobject.co_varnames`.


.. opcode:: LOAD_FROM_DICT_OR_DEREF (i)

   Lấy một mapping ra khỏi stack và tra cứu tên tương ứng với vị trí ``i`` của bộ lưu trữ "fast locals" trong mapping này. Nếu không tìm thấy tên ở đó, tải tên từ cell nằm ở vị trí ``i``, tương tự như :opcode:`LOAD_DEREF`. Điều này được dùng để tải
   :term:`các biến closure <closure variable>` trong thân lớp (trước đây sử dụng
   :opcode:`!LOAD_CLASSDEREF`) và trong
   :ref:`annotation scopes <annotation-scopes>` bên trong các thân lớp.

   .. versionadded:: 3.12


.. opcode:: STORE_DEREF (i)

   Lưu ``STACK.pop()`` vào ô nằm trong vị trí ``i`` của vùng lưu trữ "fast locals".

   .. versionchanged:: 3.11
      ``i`` không còn được tính lệch theo độ dài của :attr:`~codeobject.co_varnames`.


.. opcode:: DELETE_DEREF (i)

   Xóa nội dung ô nằm trong vị trí ``i`` của vùng lưu trữ "fast locals". Được câu lệnh :keyword:`del` sử dụng.

   .. versionadded:: 3.2

   .. versionchanged:: 3.11
      ``i`` không còn được tính lệch theo độ dài của :attr:`~codeobject.co_varnames`.


.. opcode:: COPY_FREE_VARS (n)

   Sao chép các ``n`` :term:`biến tự do (closure) <closure variable>` từ closure vào frame. Loại bỏ nhu cầu về mã đặc biệt ở phía caller khi gọi closure.

   .. versionadded:: 3.11


.. opcode:: RAISE_VARARGS (argc)

   Phát sinh một ngoại lệ bằng một trong 3 dạng của câu lệnh ``raise``, tùy thuộc vào giá trị của *argc*:

   * 0: ``raise`` (nêu lại ngoại lệ trước đó)
   * 1: ``raise STACK[-1]`` (nêu một thể hiện hoặc kiểu ngoại lệ tại ``STACK[-1]``)
   * 2: ``raise STACK[-2] from STACK[-1]`` (nêu một thể hiện hoặc kiểu ngoại lệ tại ``STACK[-2]`` với ``__cause__`` được đặt thành ``STACK[-1]``)


.. opcode:: CALL (argc)

   Gọi một đối tượng callable với số lượng đối số được chỉ định bởi ``argc``. Trên stack, theo thứ tự tăng dần, là:

   * Callable
   * ``self`` hoặc ``NULL``
   * Các đối số vị trí còn lại

   ``argc`` là tổng số đối số vị trí, không bao gồm ``self``.

   ``CALL`` lấy tất cả đối số và đối tượng có thể gọi ra khỏi stack, gọi đối tượng có thể gọi đó với các đối số ấy, rồi đẩy giá trị trả về của đối tượng có thể gọi lên stack.

   .. versionadded:: 3.11

   .. versionchanged:: 3.13
      Đối tượng có thể gọi giờ đây luôn xuất hiện ở cùng một vị trí trên stack.

   .. versionchanged:: 3.13
      Các lệnh gọi có đối số từ khóa giờ đây được xử lý bởi :opcode:`CALL_KW`.


.. opcode:: CALL_KW (argc)

   Gọi một đối tượng có thể gọi với số lượng đối số được chỉ định bởi ``argc``, bao gồm một hoặc nhiều đối số được đặt tên. Trên stack có (theo thứ tự tăng dần):

   * Callable
   * ``self`` hoặc ``NULL``
   * Các đối số vị trí còn lại
   * Các đối số được đặt tên
   * Một :class:`tuple` gồm các tên đối số từ khóa

   ``argc`` là tổng số đối số vị trí và đối số được đặt tên, không bao gồm ``self``. Độ dài của tuple chứa các tên đối số từ khóa là số lượng đối số được đặt tên.

   ``CALL_KW`` lấy tất cả đối số, các tên từ khóa và đối tượng có thể gọi ra khỏi stack, gọi đối tượng có thể gọi với các đối số đó, rồi đẩy giá trị trả về do đối tượng có thể gọi trả về lên stack.

   .. versionadded:: 3.13


.. opcode:: CALL_FUNCTION_EX (flags)

   Gọi một đối tượng có thể gọi với tập hợp thay đổi các đối số vị trí và đối số từ khóa. Nếu bit thấp nhất của *flags* được đặt, phần tử trên cùng của stack chứa một đối tượng ánh xạ gồm các đối số từ khóa bổ sung. Trước khi đối tượng có thể gọi được gọi, đối tượng ánh xạ và đối tượng iterable lần lượt được "giải nén", rồi nội dung của chúng được truyền vào lần lượt dưới dạng đối số từ khóa và đối số vị trí. ``CALL_FUNCTION_EX`` lấy tất cả đối số và đối tượng có thể gọi ra khỏi stack, gọi đối tượng có thể gọi với các đối số đó, rồi đẩy giá trị trả về do đối tượng có thể gọi trả về lên stack.

   .. versionadded:: 3.6


.. opcode:: PUSH_NULL

   Đẩy một ``NULL`` lên stack. Được dùng trong chuỗi gọi để khớp với ``NULL`` được đẩy bởi
   :opcode:`!LOAD_METHOD` cho các lệnh gọi không phải phương thức.

   .. versionadded:: 3.11


.. opcode:: MAKE_FUNCTION

   Đẩy một đối tượng hàm mới lên stack, được tạo từ đối tượng mã tại ``STACK[-1]``.

   .. versionchanged:: 3.10
      Giá trị cờ ``0x04`` là một tuple các chuỗi thay vì dictionary

   .. versionchanged:: 3.11
      Tên đủ điều kiện tại ``STACK[-1]`` đã bị loại bỏ.

   .. versionchanged:: 3.13
      Các thuộc tính hàm bổ sung trên stack, được biểu thị bằng các cờ oparg, đã bị loại bỏ. Hiện chúng sử dụng :opcode:`SET_FUNCTION_ATTRIBUTE`.


.. opcode:: SET_FUNCTION_ATTRIBUTE (flag)

   Đặt một thuộc tính trên đối tượng hàm. Yêu cầu hàm tại ``STACK[-1]`` và giá trị thuộc tính cần đặt tại ``STACK[-2]``; lấy cả hai khỏi stack và để lại hàm tại ``STACK[-1]``. Cờ này xác định thuộc tính cần đặt:

   * ``0x01`` một tuple các giá trị mặc định cho các tham số chỉ vị trí và vị trí-hoặc-từ-khóa theo thứ tự vị trí
   * ``0x02`` một dictionary chứa các giá trị mặc định của các tham số chỉ nhận đối số theo từ khóa
   * ``0x04`` một tuple gồm các chuỗi chứa chú thích kiểu của các tham số
   * ``0x08`` một tuple chứa các cell cho các biến tự do, tạo thành một closure
   * ``0x10`` :term:`annotate function` cho đối tượng hàm

   .. versionadded:: 3.13

   .. versionchanged:: 3.14
      Đã thêm ``0x10`` để chỉ hàm annotate cho đối tượng hàm.


.. opcode:: BUILD_SLICE (argc)

   .. index:: pair: built-in function; slice

   Đẩy một đối tượng slice vào stack. *argc* phải là 2 hoặc 3. Nếu là 2, thực hiện::

      end = STACK.pop()
      start = STACK.pop()
      STACK.append(slice(start, end))

   nếu là 3, thực hiện::

      step = STACK.pop()
      end = STACK.pop()
      start = STACK.pop()
      STACK.append(slice(start, end, step))

   Xem hàm tích hợp sẵn :func:`slice` để biết thêm thông tin.


.. opcode:: EXTENDED_ARG (ext)

   Thêm tiền tố vào bất kỳ opcode nào có đối số quá lớn, không thể vừa trong một byte mặc định. *ext* chứa một byte bổ sung, đóng vai trò là các bit cao hơn trong đối số. Với mỗi opcode, cho phép tối đa ba ``EXTENDED_ARG`` có tiền tố, tạo thành một đối số dài từ hai đến bốn byte.


.. opcode:: CONVERT_VALUE (oparg)

   Chuyển đổi giá trị thành một chuỗi, tùy thuộc vào ``oparg``::

      value = STACK.pop()
      result = func(value)
      STACK.append(result)

   * ``oparg == 1``: gọi :func:`str` trên *giá trị*
   * ``oparg == 2``: gọi :func:`repr` trên *giá trị*
   * ``oparg == 3``: gọi :func:`ascii` trên *giá trị*

   Được sử dụng để triển khai các string literal có định dạng (f-string).

   .. versionadded:: 3.13


.. opcode:: FORMAT_SIMPLE

   Định dạng giá trị ở đầu ngăn xếp::

      value = STACK.pop()
      result = value.__format__("")
      STACK.append(result)

   Được sử dụng để triển khai các string literal có định dạng (f-string).

   .. versionadded:: 3.13

.. opcode:: FORMAT_WITH_SPEC

   Định dạng giá trị đã cho bằng đặc tả định dạng đã cho::

      spec = STACK.pop()
      value = STACK.pop()
      result = value.__format__(spec)
      STACK.append(result)

   Được sử dụng để triển khai các string literal có định dạng (f-string).

   .. versionadded:: 3.13


.. opcode:: MATCH_CLASS (count)

   ``STACK[-1]`` là một tuple gồm các tên thuộc tính keyword, ``STACK[-2]`` là lớp được dùng để đối sánh, còn ``STACK[-3]`` là đối tượng được đối sánh. *count* là số lượng mẫu con theo vị trí.

   Lấy ``STACK[-1]``, ``STACK[-2]`` và ``STACK[-3]`` ra khỏi ngăn xếp. Nếu ``STACK[-3]`` là một thể hiện của ``STACK[-2]`` và có các thuộc tính theo vị trí và keyword mà *count* và ``STACK[-1]`` yêu cầu, hãy đẩy một tuple gồm các thuộc tính đã trích xuất. Nếu không, hãy đẩy ``None``.

   .. versionadded:: 3.10

   .. versionchanged:: 3.11
      Trước đây, instruction này cũng đẩy một giá trị boolean cho biết thao tác thành công (``True``) hay thất bại (``False``).


.. opcode:: RESUME (context)

   Một thao tác no-op. Thực hiện các kiểm tra tracing, debugging và tối ưu hóa nội bộ.

   Toán hạng ``context`` gồm hai phần. Hai bit thấp nhất cho biết ``RESUME`` xuất hiện ở đâu:

   * ``0`` Phần đầu của một hàm không phải là generator, coroutine hay async generator
   * ``1`` Sau một biểu thức ``yield``
   * ``2`` Sau một biểu thức ``yield from``
   * ``3`` Sau một biểu thức ``await``

   Bit tiếp theo là ``1`` nếu RESUME ở độ sâu except ``1``, và ``0`` trong các trường hợp khác.

   .. versionadded:: 3.11

   .. versionchanged:: 3.13
      Giá trị oparg đã được thay đổi để bao gồm thông tin về độ sâu của except


.. opcode:: RETURN_GENERATOR

   Tạo một generator, coroutine hoặc async generator từ frame hiện tại. Được dùng làm opcode đầu tiên trong code object của các callable nêu trên. Xóa frame hiện tại và trả về generator mới được tạo.

   .. versionadded:: 3.11


.. opcode:: SEND (delta)

   Tương đương với ``STACK[-1] = STACK[-2].send(STACK[-1])``. Được dùng trong các câu lệnh ``yield from`` và ``await``.

   Nếu lệnh gọi phát sinh :exc:`StopIteration`, lấy giá trị trên cùng khỏi stack, đẩy thuộc tính ``value`` của exception vào stack và tăng bộ đếm bytecode thêm *delta*.

   .. versionadded:: 3.11


.. opcode:: HAVE_ARGUMENT

   Đây không thực sự là một opcode. Nó xác định ranh giới phân chia giữa các opcode trong phạm vi [0,255] không sử dụng đối số và các opcode có sử dụng đối số (``< HAVE_ARGUMENT`` và ``>= HAVE_ARGUMENT``, tương ứng).

   Nếu ứng dụng của bạn sử dụng pseudo instruction hoặc specialized instruction, hãy sử dụng collection :data:`hasarg` thay thế.

   .. versionchanged:: 3.6
      Giờ đây mọi instruction đều có một argument, nhưng các opcode ``< HAVE_ARGUMENT`` bỏ qua argument đó. Trước đây, chỉ các opcode ``>= HAVE_ARGUMENT`` mới có argument.

   .. versionchanged:: 3.12
      Các pseudo instruction đã được thêm vào module :mod:`!dis`, và đối với chúng, không đúng khi cho rằng việc so sánh với ``HAVE_ARGUMENT`` cho biết chúng có sử dụng arg của mình hay không.

   .. deprecated:: 3.13
      Thay vào đó, hãy sử dụng :data:`hasarg`.

.. opcode:: CALL_INTRINSIC_1

   Gọi một hàm intrinsic với một đối số. Truyền ``STACK[-1]`` làm đối số và đặt ``STACK[-1]`` thành kết quả. Được dùng để triển khai chức năng không yêu cầu hiệu năng cao.

   Operand xác định hàm intrinsic nào được gọi:

   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | Operand                           | Description                                                                                                                                       |
   +===================================+===================================================================================================================================================+
   | ``INTRINSIC_1_INVALID``           | Không hợp lệ                                                                                                                                      |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_PRINT``               | In đối số ra đầu ra chuẩn. Được sử dụng trong REPL.                                                                                               |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_IMPORT_STAR``         | Thực hiện ``import *`` cho module được đặt tên.                                                                                                   |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_STOPITERATION_ERROR`` | Trích xuất giá trị trả về từ ngoại lệ ``StopIteration``.                                                                                          |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_ASYNC_GEN_WRAP``      | Bọc một giá trị async generator                                                                                                                   |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_UNARY_POSITIVE``      | Thực hiện phép toán một ngôi ``+``                                                                                                                |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_LIST_TO_TUPLE``       | Chuyển đổi một danh sách thành một tuple                                                                                                          |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_TYPEVAR``             | Tạo một :class:`typing.TypeVar`                                                                                                                   |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_PARAMSPEC``           | Tạo một                                                                                                                                           |
   |                                   | :class:`typing.ParamSpec`                                                                                                                         |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_TYPEVARTUPLE``        | Tạo một                                                                                                                                           |
   |                                   | :class:`typing.TypeVarTuple`                                                                                                                      |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_SUBSCRIPT_GENERIC``   | Trả về :class:`typing.Generic` được lập chỉ mục bằng đối số                                                                                       |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``INTRINSIC_TYPEALIAS``           | Tạo một                                                                                                                                           |
   |                                   | :class:`typing.TypeAliasType`; được dùng trong câu lệnh :keyword:`type`. Đối số là một tuple gồm tên của type alias, các tham số kiểu và giá trị. |
   +-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+

   .. versionadded:: 3.12

.. opcode:: CALL_INTRINSIC_2

   Gọi một hàm nội tại với hai đối số. Được dùng để triển khai chức năng không quan trọng về hiệu năng::

      arg2 = STACK.pop()
      arg1 = STACK.pop()
      result = intrinsic2(arg1, arg2)
      STACK.append(result)

   Operand xác định hàm intrinsic nào được gọi:

   +----------------------------------------+--------------------------------------------------------+
   | Operand                                | Description                                            |
   +========================================+========================================================+
   | ``INTRINSIC_2_INVALID``                | Không hợp lệ                                           |
   +----------------------------------------+--------------------------------------------------------+
   | ``INTRINSIC_PREP_RERAISE_STAR``        | Tính toán                                              |
   |                                        | :exc:`ExceptionGroup` để raise từ một ``try-except*``. |
   +----------------------------------------+--------------------------------------------------------+
   | ``INTRINSIC_TYPEVAR_WITH_BOUND``       | Tạo một :class:`typing.TypeVar` với một bound.         |
   +----------------------------------------+--------------------------------------------------------+
   | ``INTRINSIC_TYPEVAR_WITH_CONSTRAINTS`` | Tạo một                                                |
   |                                        | :class:`typing.TypeVar` với các ràng buộc.             |
   +----------------------------------------+--------------------------------------------------------+
   | ``INTRINSIC_SET_FUNCTION_TYPE_PARAMS`` | Đặt thuộc tính ``__type_params__`` của một hàm.        |
   +----------------------------------------+--------------------------------------------------------+

   .. versionadded:: 3.12


.. opcode:: LOAD_SPECIAL

   Thực hiện tra cứu phương thức đặc biệt trên ``STACK[-1]``. Nếu ``type(STACK[-1]).__xxx__`` là một phương thức, để lại ``type(STACK[-1]).__xxx__; STACK[-1]`` trên ngăn xếp. Nếu ``type(STACK[-1]).__xxx__`` không phải là một phương thức, để lại ``STACK[-1].__xxx__; NULL`` trên ngăn xếp.

   .. versionadded:: 3.14


**Pseudo-instructions**

Các opcode này không xuất hiện trong bytecode Python. Chúng được compiler sử dụng nhưng được thay thế bằng các opcode thực hoặc bị loại bỏ trước khi bytecode được tạo.

.. opcode:: SETUP_FINALLY (target)

   Thiết lập trình xử lý ngoại lệ cho khối mã tiếp theo. Nếu xảy ra ngoại lệ, mức ngăn xếp giá trị được khôi phục về trạng thái hiện tại và quyền điều khiển được chuyển đến trình xử lý ngoại lệ tại ``target``.


.. opcode:: SETUP_CLEANUP (target)

   Tương tự như ``SETUP_FINALLY``, nhưng trong trường hợp xảy ra ngoại lệ, cũng đẩy lệnh cuối cùng (``lasti``) vào ngăn xếp để ``RERAISE`` có thể khôi phục lệnh đó. Nếu xảy ra ngoại lệ, mức ngăn xếp giá trị và lệnh cuối cùng trên frame được khôi phục về trạng thái hiện tại, đồng thời quyền điều khiển được chuyển đến trình xử lý ngoại lệ tại ``target``.


.. opcode:: SETUP_WITH (target)

   Giống như ``SETUP_CLEANUP``, nhưng trong trường hợp xảy ra ngoại lệ, một phần tử nữa sẽ được lấy ra khỏi stack trước khi quyền điều khiển được chuyển đến trình xử lý ngoại lệ tại ``target``.

   Biến thể này được dùng trong các cấu trúc :keyword:`with` và :keyword:`async with`, chúng đẩy giá trị trả về của
   :meth:`~object.__enter__` hoặc :meth:`~object.__aenter__` của context manager vào stack.


.. opcode:: POP_BLOCK

   Đánh dấu phần cuối của khối mã liên kết với ``SETUP_FINALLY``, ``SETUP_CLEANUP`` hoặc ``SETUP_WITH`` gần nhất.


.. opcode:: LOAD_CONST_IMMORTAL (consti)

   Hoạt động như :opcode:`LOAD_CONST`, nhưng hiệu quả hơn đối với các đối tượng bất tử.


.. opcode:: JUMP
            JUMP_NO_INTERRUPT

   Các lệnh nhảy tương đối không định hướng, được assembler thay thế bằng các lệnh tương ứng có hướng (tiến/lùi).

.. opcode:: JUMP_IF_TRUE
            JUMP_IF_FALSE

   Các phép nhảy có điều kiện không ảnh hưởng đến stack. Được thay thế bằng chuỗi ``COPY 1``, ``TO_BOOL``, ``POP_JUMP_IF_TRUE/FALSE``.

.. opcode:: LOAD_CLOSURE (i)

   Đẩy một tham chiếu đến cell nằm trong slot ``i`` của vùng lưu trữ "fast locals".

   Lưu ý rằng ``LOAD_CLOSURE`` được thay thế bằng ``LOAD_FAST`` trong assembler.

   .. versionchanged:: 3.13
      Opcode này hiện là một pseudo-instruction.


.. _opcode_collections:

Các tập hợp opcode
------------------

Các tập hợp này được cung cấp để tự động introspection các instruction bytecode:

.. versionchanged:: 3.12
   Các collection hiện cũng chứa các lệnh giả (pseudo-instruction) và các lệnh instrumented. Đây là những opcode có giá trị ``>= MIN_PSEUDO_OPCODE`` và ``>= MIN_INSTRUMENTED_OPCODE``.

.. data:: opname

   Chuỗi tên thao tác, có thể lập chỉ mục bằng bytecode.


.. data:: opmap

   Từ điển ánh xạ tên thao tác với bytecode.


.. data:: cmp_op

   Chuỗi của tất cả tên thao tác so sánh.


.. data:: hasarg

   Chuỗi các bytecode sử dụng đối số của chúng.

   .. versionadded:: 3.12


.. data:: hasconst

   Chuỗi các bytecode truy cập một hằng số.


.. data:: hasfree

   Chuỗi các bytecode truy cập một biến :term:`tự do (closure) <closure variable>`. Trong ngữ cảnh này, 'free' chỉ các tên trong scope hiện tại được các scope bên trong tham chiếu, hoặc các tên trong scope bên ngoài được tham chiếu từ scope này. Nó *không* bao gồm các tham chiếu đến scope global hoặc builtin.


.. data:: hasname

   Chuỗi bytecode truy cập một thuộc tính theo tên.


.. data:: hasjump

   Chuỗi bytecode có đích nhảy. Tất cả các lệnh nhảy đều là tương đối.

   .. versionadded:: 3.13

.. data:: haslocal

   Chuỗi bytecode truy cập một biến cục bộ.


.. data:: hascompare

   Chuỗi bytecode của các phép toán Boolean.

.. data:: hasexc

   Chuỗi bytecode thiết lập một trình xử lý ngoại lệ.

   .. versionadded:: 3.12


.. data:: hasjrel

   Chuỗi bytecode có đích nhảy tương đối.

   .. deprecated:: 3.13
      Tất cả các lệnh nhảy hiện đều là tương đối. Sử dụng :data:`hasjump`.


.. data:: hasjabs

   Chuỗi bytecode có một đích nhảy tuyệt đối.

   .. deprecated:: 3.13
      Tất cả các lệnh nhảy hiện đều là tương đối. Danh sách này trống.
