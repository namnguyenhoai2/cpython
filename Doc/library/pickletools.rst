:mod:`!pickletools` --- Công cụ dành cho nhà phát triển pickle
==============================================================

.. module:: pickletools
   :synopsis: Chứa các chú thích chi tiết về các protocol pickle và opcode của máy pickle, cùng một số hàm hữu ích.

**Mã nguồn:** :source:`Lib/pickletools.py`

--------------


Mô-đun này chứa nhiều hằng số liên quan đến các chi tiết chuyên sâu của
:mod:`pickle` mô-đun, một số chú thích dài về cách triển khai và một vài hàm hữu ích để phân tích dữ liệu đã được pickle. Nội dung của mô-đun này hữu ích cho các nhà phát triển cốt lõi Python đang làm việc trên :mod:`pickle`; người dùng thông thường của mô-đun :mod:`pickle` có lẽ sẽ không thấy
:mod:`!pickletools` mô-đun này có liên quan.

.. _pickletools-cli:

Cách sử dụng dòng lệnh
----------------------

.. versionadded:: 3.2

Khi được gọi từ command line, ``python -m pickletools`` sẽ phân tích nội dung của một hoặc nhiều tệp pickle. Lưu ý rằng nếu bạn muốn xem đối tượng Python được lưu trong pickle thay vì các chi tiết của định dạng pickle, bạn có thể muốn sử dụng ``-m pickle`` thay thế. Tuy nhiên, khi tệp pickle bạn muốn kiểm tra đến từ một nguồn không đáng tin cậy, ``-m pickletools`` là lựa chọn an toàn hơn vì nó không thực thi bytecode của pickle.

Ví dụ, với một tuple ``(1, 2)`` được pickle trong tệp ``x.pickle``:

.. code-block:: shell-session

    $ python -m pickle x.pickle
    (1, 2)

    $ python -m pickletools x.pickle
        0: \x80 PROTO      3
        2: K    BININT1    1
        4: K    BININT1    2
        6: \x86 TUPLE2
        7: q    BINPUT     0
        9: .    STOP
    highest protocol among opcodes = 2

Các tùy chọn command line
^^^^^^^^^^^^^^^^^^^^^^^^^

.. program:: pickletools

.. option:: -a, --annotate

   Chú thích mỗi dòng bằng mô tả opcode ngắn gọn.

.. option:: -o, --output=<file>

   Tên của tệp mà đầu ra sẽ được ghi vào.

.. option:: -l, --indentlevel=<num>

   Số lượng khoảng trắng dùng để thụt lề một cấp MARK mới.

.. option:: -m, --memo

   Khi phân tích nhiều đối tượng, giữ nguyên memo giữa các lần phân tích.

.. option:: -p, --preamble=<preamble>

   Khi chỉ định nhiều hơn một tệp pickle, in phần mở đầu đã cho trước mỗi lần disassembly.

.. option:: pickle_file

   Một tệp pickle cần đọc, hoặc ``-`` để chỉ việc đọc từ đầu vào tiêu chuẩn.



Giao diện lập trình
-------------------


.. function:: dis(pickle, out=None, memo=None, indentlevel=4, annotate=0)

   Xuất bản disassembly dạng ký hiệu của pickle tới đối tượng dạng tệp *out*, mặc định là ``sys.stdout``. *pickle* có thể là một chuỗi hoặc một đối tượng dạng tệp. *memo* có thể là một từ điển Python được dùng làm memo của pickle; có thể sử dụng nó để thực hiện disassembly trên nhiều pickle được tạo bởi cùng một pickler. Các cấp độ liên tiếp, được biểu thị bằng các opcode ``MARK`` trong luồng, sẽ được thụt lề bằng *indentlevel* dấu cách. Nếu cung cấp giá trị khác không cho *annotate*, mỗi opcode trong đầu ra sẽ được chú thích bằng một mô tả ngắn. Giá trị của *annotate* được dùng làm gợi ý cho cột bắt đầu chú thích.

   .. versionchanged:: 3.2
      Đã thêm tham số *annotate*.

.. function:: genops(pickle)

   Cung cấp một :term:`iterator` trên tất cả các opcode trong một pickle, trả về một chuỗi các bộ ba ``(opcode, arg, pos)``. *opcode* là một thể hiện của
   lớp :class:`OpcodeInfo`; *arg* là giá trị đã giải mã, dưới dạng một đối tượng Python, của đối số của opcode; *pos* là vị trí của opcode này. *pickle* có thể là một chuỗi hoặc một đối tượng dạng tệp.

.. function:: optimize(picklestring)

   Trả về một chuỗi pickle tương đương mới sau khi loại bỏ các opcode ``PUT`` không được sử dụng. Pickle đã được tối ưu sẽ ngắn hơn, mất ít thời gian truyền hơn, cần ít dung lượng lưu trữ hơn và được unpickle hiệu quả hơn.
