:mod:`!getopt` --- Bộ phân tích kiểu C cho các tùy chọn dòng lệnh
=================================================================

.. module:: getopt
   :synopsis: Bộ phân tích di động cho các tùy chọn dòng lệnh; hỗ trợ cả tên tùy chọn dạng ngắn và dạng dài.

**Mã nguồn:** :source:`Lib/getopt.py`

.. note::

   Module này được xem là đã hoàn thiện về tính năng. Một giải pháp thay thế có tính khai báo và khả năng mở rộng cao hơn cho API này được cung cấp trong module :mod:`optparse`. Các cải tiến chức năng khác cho việc xử lý tham số dòng lệnh được cung cấp dưới dạng các module bên thứ ba trên PyPI hoặc dưới dạng các tính năng trong module :mod:`argparse`.

--------------

Module này giúp các script phân tích các đối số dòng lệnh trong ``sys.argv``. Module hỗ trợ các quy ước giống như hàm :c:func:`!getopt` của Unix (bao gồm ý nghĩa đặc biệt của các đối số có dạng '``-``' và '``--``'). Các tùy chọn dài tương tự những tùy chọn được phần mềm GNU hỗ trợ cũng có thể được sử dụng thông qua đối số thứ ba tùy chọn.

Những người chưa quen với hàm :c:func:`!getopt` của Unix nên cân nhắc sử dụng module :mod:`argparse` thay thế. Những người đã quen với hàm :c:func:`!getopt` của Unix
:c:func:`!getopt`, nhưng muốn có hành vi tương đương trong khi viết ít mã hơn và nhận được thông báo trợ giúp và lỗi tốt hơn, nên cân nhắc sử dụng module :mod:`optparse`. Xem :ref:`choosing-an-argument-parser` để biết thêm chi tiết.

Mô-đun này cung cấp hai hàm và một ngoại lệ:


.. function:: getopt(args, shortopts, longopts=[])

   Phân tích các tùy chọn dòng lệnh và danh sách tham số. *args* là danh sách đối số cần phân tích, không bao gồm tham chiếu ở đầu đến chương trình đang chạy. Thông thường, điều này có nghĩa là ``sys.argv[1:]``. *shortopts* là chuỗi các chữ cái tùy chọn mà script muốn nhận dạng; các tùy chọn yêu cầu một đối số phải được theo sau bằng dấu hai chấm (``':'``), còn các tùy chọn chấp nhận đối số tùy chọn phải được theo sau bằng hai dấu hai chấm (``'::'``); tức là cùng định dạng mà Unix :c:func:`!getopt` sử dụng.

   .. note::

      Không giống GNU :c:func:`!getopt`, sau một đối số không phải tùy chọn, tất cả các đối số tiếp theo cũng được xem là không phải tùy chọn. Điều này tương tự cách các hệ thống Unix không phải GNU hoạt động.

   *longopts*, nếu được chỉ định, phải là danh sách các chuỗi chứa tên của những tùy chọn dài cần được hỗ trợ. Không được đưa các ký tự ``'--'`` ở đầu vào tên tùy chọn. Các tùy chọn dài yêu cầu một đối số phải được theo sau bằng dấu bằng (``'='``). Các tùy chọn dài chấp nhận một đối số tùy chọn phải được theo sau bằng dấu bằng và dấu hỏi (``'=?'``). Để chỉ chấp nhận các tùy chọn dài, *shortopts* phải là một chuỗi rỗng. Các tùy chọn dài trên dòng lệnh có thể được nhận dạng miễn là chúng cung cấp một tiền tố của tên tùy chọn khớp chính xác với một trong các tùy chọn được chấp nhận. Ví dụ, nếu *longopts* là ``['foo', 'frob']``, tùy chọn ``--fo`` sẽ khớp với ``--foo``, nhưng ``--f`` sẽ không khớp duy nhất, vì vậy :exc:`GetoptError` sẽ được phát sinh.

   Nếu *longopts* là một chuỗi, nó được xử lý như một danh sách chỉ có một phần tử.

   Giá trị trả về gồm hai phần tử: phần tử đầu tiên là danh sách các cặp ``(option, value)``; phần tử thứ hai là danh sách các đối số chương trình còn lại sau khi danh sách tùy chọn bị loại bỏ (đây là một lát cắt ở cuối của *args*). Mỗi cặp tùy chọn và giá trị được trả về có tùy chọn làm phần tử đầu tiên, với một dấu gạch nối ở trước đối với tùy chọn ngắn (ví dụ: ``'-x'``) hoặc hai dấu gạch nối đối với tùy chọn dài (ví dụ: ``'--long-option'``), và đối số của tùy chọn làm phần tử thứ hai, hoặc một chuỗi rỗng nếu tùy chọn không có đối số. Các tùy chọn xuất hiện trong danh sách theo cùng thứ tự mà chúng được tìm thấy, nhờ đó cho phép xuất hiện nhiều lần. Có thể trộn lẫn các tùy chọn dài và ngắn.

   .. versionchanged:: 3.14
      Có hỗ trợ các đối số tùy chọn.


.. function:: gnu_getopt(args, shortopts, longopts=[])

   Hàm này hoạt động giống như :func:`getopt`, ngoại trừ việc chế độ quét theo kiểu GNU được sử dụng theo mặc định. Điều này có nghĩa là các đối số tùy chọn và không phải tùy chọn có thể được xen kẽ. Hàm :func:`getopt` dừng xử lý các tùy chọn ngay khi gặp một đối số không phải tùy chọn.

   Nếu ký tự đầu tiên của chuỗi tùy chọn là ``'+'``, hoặc nếu biến môi trường :envvar:`!POSIXLY_CORRECT` được đặt, thì việc xử lý tùy chọn sẽ dừng ngay khi gặp một đối số không phải tùy chọn.

   Nếu ký tự đầu tiên của chuỗi tùy chọn là ``'-'``, các đối số không phải tùy chọn được theo sau bởi các tùy chọn sẽ được thêm vào danh sách các cặp tùy chọn và giá trị dưới dạng một cặp có ``None`` làm phần tử đầu tiên và danh sách các đối số không phải tùy chọn làm phần tử thứ hai. Phần tử thứ hai của kết quả :func:`!gnu_getopt` là danh sách các đối số của chương trình sau tùy chọn cuối cùng.

   .. versionchanged:: 3.14
      Hỗ trợ trả về các tùy chọn và đối số không phải tùy chọn xen kẽ theo đúng thứ tự.


.. exception:: GetoptError

   Lỗi này được phát sinh khi tìm thấy một tùy chọn không được nhận dạng trong danh sách đối số hoặc khi một tùy chọn yêu cầu đối số nhưng không được cung cấp đối số. Đối số của ngoại lệ là một chuỗi cho biết nguyên nhân của lỗi. Đối với các tùy chọn dài, việc cung cấp đối số cho một tùy chọn không yêu cầu đối số cũng sẽ khiến ngoại lệ này được phát sinh. Các thuộc tính :attr:`!msg` và :attr:`!opt` cung cấp thông báo lỗi và tùy chọn liên quan; nếu không có tùy chọn cụ thể nào liên quan đến ngoại lệ,
   :attr:`!opt` là một chuỗi rỗng.

.. XXX deprecated?
.. exception:: error

   Bí danh của :exc:`GetoptError`; để đảm bảo khả năng tương thích ngược.

Một ví dụ chỉ sử dụng các tùy chọn kiểu Unix:

.. doctest::

   >>> import getopt
   >>> args = '-a -b -cfoo -d bar a1 a2'.split()
   >>> args
   ['-a', '-b', '-cfoo', '-d', 'bar', 'a1', 'a2']
   >>> optlist, args = getopt.getopt(args, 'abc:d:')
   >>> optlist
   [('-a', ''), ('-b', ''), ('-c', 'foo'), ('-d', 'bar')]
   >>> args
   ['a1', 'a2']

Việc sử dụng tên tùy chọn dài cũng dễ dàng không kém:

.. doctest::

   >>> s = '--condition=foo --testing --output-file abc.def -x a1 a2'
   >>> args = s.split()
   >>> args
   ['--condition=foo', '--testing', '--output-file', 'abc.def', '-x', 'a1', 'a2']
   >>> optlist, args = getopt.getopt(args, 'x', [
   ...     'condition=', 'output-file=', 'testing'])
   >>> optlist
   [('--condition', 'foo'), ('--testing', ''), ('--output-file', 'abc.def'), ('-x', '')]
   >>> args
   ['a1', 'a2']

Các đối số tùy chọn nên được chỉ định một cách rõ ràng:

.. doctest::

   >>> s = '-Con -C --color=off --color a1 a2'
   >>> args = s.split()
   >>> args
   ['-Con', '-C', '--color=off', '--color', 'a1', 'a2']
   >>> optlist, args = getopt.getopt(args, 'C::', ['color=?'])
   >>> optlist
   [('-C', 'on'), ('-C', ''), ('--color', 'off'), ('--color', '')]
   >>> args
   ['a1', 'a2']

Có thể giữ nguyên thứ tự của các tùy chọn và đối số không phải tùy chọn:

.. doctest::

   >>> s = 'a1 -x a2 a3 a4 --long a5 a6'
   >>> args = s.split()
   >>> args
   ['a1', '-x', 'a2', 'a3', 'a4', '--long', 'a5', 'a6']
   >>> optlist, args = getopt.gnu_getopt(args, '-x:', ['long='])
   >>> optlist
   [(None, ['a1']), ('-x', 'a2'), (None, ['a3', 'a4']), ('--long', 'a5')]
   >>> args
   ['a6']

Trong một script, cách sử dụng điển hình sẽ như sau:

.. testcode::

   import getopt, sys

   def main():
       try:
           opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
       except getopt.GetoptError as err:
           # in thông tin trợ giúp rồi thoát:
           print(err)  # sẽ in ra nội dung tương tự "option -a not recognized"
           usage()
           sys.exit(2)
       output = None
       verbose = False
       for o, a in opts:
           if o == "-v":
               verbose = True
           elif o in ("-h", "--help"):
               usage()
               sys.exit()
           elif o in ("-o", "--output"):
               output = a
           else:
               assert False, "unhandled option"
       process(args, output=output, verbose=verbose)

   if __name__ == "__main__":
       main()

Lưu ý rằng có thể tạo một giao diện dòng lệnh tương đương với ít mã hơn và các thông báo trợ giúp cũng như lỗi giàu thông tin hơn bằng cách sử dụng mô-đun :mod:`optparse`:

.. testcode::

   import optparse

   if __name__ == '__main__':
       parser = optparse.OptionParser()
       parser.add_option('-o', '--output')
       parser.add_option('-v', dest='verbose', action='store_true')
       opts, args = parser.parse_args()
       process(args, output=opts.output, verbose=opts.verbose)

Trong trường hợp này, cũng có thể tạo một giao diện dòng lệnh gần tương đương bằng cách sử dụng mô-đun :mod:`argparse`:

.. testcode::

   import argparse

   if __name__ == '__main__':
       parser = argparse.ArgumentParser()
       parser.add_argument('-o', '--output')
       parser.add_argument('-v', dest='verbose', action='store_true')
       parser.add_argument('rest', nargs='*')
       args = parser.parse_args()
       process(args.rest, output=args.output, verbose=args.verbose)

Xem :ref:`choosing-an-argument-parser` để biết chi tiết về sự khác biệt trong hành vi giữa phiên bản ``argparse`` và phiên bản ``optparse`` (cũng như ``getopt``) của mã này.

.. seealso::

   Mô-đun :mod:`optparse`
      Phân tích tùy chọn dòng lệnh theo cách khai báo.

   Mô-đun :mod:`argparse`
      Thư viện phân tích tùy chọn và đối số dòng lệnh theo định hướng rõ ràng hơn.
