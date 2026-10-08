:mod:`!fnmatch` --- Khớp mẫu tên tệp Unix
=========================================

.. module:: fnmatch
   :synopsis: Khớp mẫu tên tệp theo kiểu Unix shell.

**Mã nguồn:** :source:`Lib/fnmatch.py`

.. index:: single: filenames; wildcard expansion

.. index:: pair: module; re

--------------

Module này cung cấp khả năng hỗ trợ các ký tự đại diện theo kiểu Unix shell, vốn *không* giống với biểu thức chính quy (được mô tả trong module :mod:`re`). Các ký tự đặc biệt được sử dụng trong ký tự đại diện theo kiểu shell là:

.. index::
   single: * (asterisk); in glob-style wildcards
   single: ? (question mark); in glob-style wildcards
   single: [] (square brackets); in glob-style wildcards
   single: ! (exclamation); in glob-style wildcards
   single: - (minus); in glob-style wildcards

+------------+-------------------------------------------------+
| Mẫu        | Ý nghĩa                                         |
+============+=================================================+
| ``*``      | khớp mọi thứ                                    |
+------------+-------------------------------------------------+
| ``?``      | khớp với bất kỳ ký tự đơn nào                   |
+------------+-------------------------------------------------+
| ``[seq]``  | khớp với bất kỳ ký tự nào trong *seq*           |
+------------+-------------------------------------------------+
| ``[!seq]`` | khớp với bất kỳ ký tự nào không nằm trong *seq* |
+------------+-------------------------------------------------+

Để khớp theo nghĩa đen, hãy đặt các ký tự meta trong dấu ngoặc vuông. Ví dụ: ``'[?]'`` khớp với ký tự ``'?'``.

.. index:: pair: module; glob

Lưu ý rằng dấu phân cách tên tệp (``'/'`` trên Unix) *không* đặc biệt đối với module này. Xem module :mod:`glob` để mở rộng pathname (:mod:`glob` sử dụng
:func:`.filter` để khớp với các phân đoạn pathname). Tương tự, các tên tệp bắt đầu bằng dấu chấm không có gì đặc biệt đối với module này và được khớp bởi các mẫu ``*`` và ``?``.

Trừ khi có quy định khác, "chuỗi tên tệp" và "chuỗi mẫu" đều đề cập đến
:class:`str` hoặc ``ISO-8859-1`` được mã hóa thành các đối tượng :class:`bytes`. Lưu ý rằng các hàm được mô tả bên dưới không cho phép kết hợp một mẫu :class:`!bytes` với một tên tệp :class:`!str`, và ngược lại.

Cuối cùng, lưu ý rằng :deco:`functools.lru_cache` với *maxsize* là 32768 được dùng để lưu vào bộ nhớ đệm các mẫu regex đã biên dịch (có kiểu) trong các hàm sau: :func:`fnmatch`, :func:`fnmatchcase`, :func:`.filter`, :func:`.filterfalse`.


.. function:: fnmatch(name, pat)

   Kiểm tra xem chuỗi tên tệp *name* có khớp với chuỗi mẫu *pat* hay không, rồi trả về ``True`` hoặc ``False``. Cả hai tham số đều được chuẩn hóa chữ hoa chữ thường bằng :func:`os.path.normcase`. Có thể dùng :func:`fnmatchcase` để thực hiện so sánh phân biệt chữ hoa chữ thường, bất kể đó có phải là cách xử lý mặc định của hệ điều hành hay không.

   Ví dụ này sẽ in tất cả tên tệp trong thư mục hiện tại có phần mở rộng ``.txt``::

      import fnmatch
      import os

      for file in os.listdir('.'):
          if fnmatch.fnmatch(file, '*.txt'):
              print(file)


.. function:: fnmatchcase(name, pat)

   Kiểm tra xem chuỗi tên tệp *name* có khớp với chuỗi mẫu *pat* hay không, rồi trả về ``True`` hoặc ``False``; phép so sánh phân biệt chữ hoa chữ thường và không áp dụng :func:`os.path.normcase`.


.. function:: filter(names, pat)

   Tạo một danh sách từ những phần tử của :term:`iterable` gồm các chuỗi tên tệp *names* khớp với chuỗi mẫu *pat*. Hàm này tương đương với ``[n for n in names if fnmatch(n, pat)]``, nhưng được triển khai hiệu quả hơn.


.. function:: filterfalse(names, pat)

   Tạo một danh sách từ những phần tử của :term:`iterable` gồm các chuỗi tên tệp *names* không khớp với chuỗi mẫu *pat*. Hàm này tương đương với ``[n for n in names if not fnmatch(n, pat)]``, nhưng được triển khai hiệu quả hơn.

   .. versionadded:: 3.14


.. function:: translate(pat)

   Trả về mẫu kiểu shell *pat* được chuyển đổi thành biểu thức chính quy để sử dụng với :func:`re.match`. Mẫu này được mong đợi là một :class:`str`.

   Ví dụ:

      >>> import fnmatch, re
      >>>
      >>> regex = fnmatch.translate('*.txt')
      >>> regex
      '(?s:.*\\.txt)\\z'
      >>> reobj = re.compile(regex)
      >>> reobj.match('foobar.txt')
      <re.Match object; span=(0, 10), match='foobar.txt'>


.. seealso::

   Mô-đun :mod:`glob`
      Mở rộng đường dẫn theo kiểu Unix shell.
