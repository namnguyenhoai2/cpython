.. _tut-errors:

***************
Lỗi và Ngoại lệ
***************

Cho đến nay, các thông báo lỗi mới chỉ được đề cập đến, nhưng nếu bạn đã thử các ví dụ, có lẽ bạn đã thấy một vài thông báo. Có (ít nhất) hai loại lỗi có thể phân biệt: *lỗi cú pháp* và *ngoại lệ*.


.. _tut-syntaxerrors:

Lỗi cú pháp
===========

Lỗi cú pháp, còn được gọi là lỗi phân tích cú pháp, có lẽ là loại lỗi phổ biến nhất mà bạn gặp phải khi vẫn đang học Python::

   >>> while True print('Hello world')
     File "<stdin>", line 1
       while True print('Hello world')
                  ^^^^^
   SyntaxError: invalid syntax

Bộ phân tích cú pháp lặp lại dòng gây lỗi và hiển thị các mũi tên nhỏ chỉ vào vị trí phát hiện lỗi. Lưu ý rằng đây không phải lúc nào cũng là vị trí cần sửa. Trong ví dụ này, lỗi được phát hiện tại hàm :func:`print`, vì ngay trước đó bị thiếu dấu hai chấm (``':'``).

Tên tệp (``<stdin>`` trong ví dụ của chúng ta) và số dòng được in ra để bạn biết cần tìm ở đâu trong trường hợp đầu vào đến từ một tệp.


.. _tut-exceptions:

Ngoại lệ
========

Ngay cả khi một câu lệnh hoặc biểu thức đúng về mặt cú pháp, nó vẫn có thể gây ra lỗi khi cố gắng thực thi. Các lỗi được phát hiện trong quá trình thực thi được gọi là *exceptions* và không phải lúc nào cũng nghiêm trọng: bạn sẽ sớm học cách xử lý chúng trong các chương trình Python. Tuy nhiên, hầu hết các exception không được chương trình xử lý và dẫn đến các thông báo lỗi như minh họa ở đây::

   >>> 10 * (1/0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       10 * (1/0)
             ~^~
   ZeroDivisionError: division by zero
   >>> 4 + spam*3
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       4 + spam*3
           ^^^^
   NameError: name 'spam' is not defined
   >>> '2' + 2
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       '2' + 2
       ~~~~^~~
   TypeError: can only concatenate str (not "int") to str

Dòng cuối cùng của thông báo lỗi cho biết điều gì đã xảy ra. Exception có nhiều kiểu khác nhau và kiểu được in như một phần của thông báo: các kiểu trong ví dụ là :exc:`ZeroDivisionError`, :exc:`NameError` và :exc:`TypeError`. Chuỗi được in dưới dạng kiểu exception là tên của exception tích hợp đã xảy ra. Điều này đúng với tất cả exception tích hợp, nhưng không nhất thiết đúng với exception do người dùng định nghĩa (mặc dù đây là một quy ước hữu ích). Tên các exception tiêu chuẩn là các identifier tích hợp (không phải từ khóa dành riêng).

Phần còn lại của dòng cung cấp thông tin chi tiết dựa trên kiểu exception và nguyên nhân gây ra nó.

Phần trước đó của thông báo lỗi cho biết ngữ cảnh nơi exception xảy ra, dưới dạng stack traceback. Nhìn chung, nó chứa một stack traceback liệt kê các dòng mã nguồn; tuy nhiên, nó sẽ không hiển thị các dòng được đọc từ standard input.

:ref:`bltin-exceptions` liệt kê các exception tích hợp và ý nghĩa của chúng.


.. _tut-handling:

Xử lý Exception
===============

Bạn có thể viết các chương trình xử lý những exception được chọn. Hãy xem ví dụ sau, trong đó chương trình yêu cầu người dùng nhập dữ liệu cho đến khi một số nguyên hợp lệ được nhập, nhưng cho phép người dùng ngắt chương trình (bằng :kbd:`Control-C` hoặc bất kỳ cách nào mà hệ điều hành hỗ trợ); lưu ý rằng việc ngắt do người dùng tạo ra được báo hiệu bằng cách phát sinh exception :exc:`KeyboardInterrupt`.::

   >>> while True:
   ...     try:
   ...         x = int(input("Please enter a number: "))
   ...         break
   ...     except ValueError:
   ...         print("Oops!  That was no valid number.  Try again...")
   ...

Câu lệnh :keyword:`try` hoạt động như sau.

* Trước tiên, *mệnh đề try* (các câu lệnh nằm giữa :keyword:`try` và
  :keyword:`except` từ khóa) được thực thi.

* Nếu không xảy ra ngoại lệ, *mệnh đề except* được bỏ qua và việc thực thi
  câu lệnh :keyword:`try` kết thúc.

* Nếu một ngoại lệ xảy ra trong khi thực thi mệnh đề :keyword:`try`, phần còn lại của mệnh đề sẽ bị bỏ qua. Sau đó, nếu kiểu của ngoại lệ đó khớp với ngoại lệ được nêu sau
  từ khóa :keyword:`except`, *mệnh đề except* được thực thi, rồi việc thực thi tiếp tục sau khối try/except.

* Nếu xảy ra một ngoại lệ không khớp với ngoại lệ được nêu trong mệnh đề *except clause*, ngoại lệ đó sẽ được chuyển tiếp đến các câu lệnh :keyword:`try` bên ngoài; nếu không tìm thấy trình xử lý nào, đó là một *unhandled exception* và quá trình thực thi dừng lại với một thông báo lỗi.

Một câu lệnh :keyword:`try` có thể có nhiều mệnh đề *except clause* để chỉ định các trình xử lý cho những ngoại lệ khác nhau. Tối đa một trình xử lý sẽ được thực thi. Các trình xử lý chỉ xử lý những ngoại lệ xảy ra trong *try clause* tương ứng, không xử lý các ngoại lệ xảy ra trong những trình xử lý khác của cùng câu lệnh :keyword:`!try`. Một *except clause* có thể nêu nhiều ngoại lệ, chẳng hạn như::

   ... except RuntimeError, TypeError, NameError:
   ...     pass

Một class trong mệnh đề :keyword:`except` sẽ khớp với các ngoại lệ là instance của chính class đó hoặc một trong các class dẫn xuất của nó (nhưng không theo chiều ngược lại --- một *except clause* liệt kê một class dẫn xuất sẽ không khớp với các instance của các class cơ sở của nó). Ví dụ, đoạn mã sau sẽ in B, C, D theo thứ tự đó::

   class B(Exception):
       pass

   class C(B):
       pass

   class D(C):
       pass

   for cls in [B, C, D]:
       try:
           raise cls()
       except D:
           print("D")
       except C:
           print("C")
       except B:
           print("B")

Lưu ý rằng nếu các mệnh đề *except clauses* được đảo ngược (với ``except B`` trước), kết quả sẽ là B, B, B --- *except clause* khớp đầu tiên sẽ được kích hoạt.

Khi xảy ra một ngoại lệ, ngoại lệ đó có thể có các giá trị đi kèm, còn được gọi là *arguments* của ngoại lệ. Sự hiện diện và kiểu của các arguments phụ thuộc vào kiểu ngoại lệ.

Mệnh đề *except clause* có thể chỉ định một biến sau tên ngoại lệ. Biến này được liên kết với instance ngoại lệ, thường có một thuộc tính ``args`` lưu trữ các arguments. Để thuận tiện, các kiểu ngoại lệ dựng sẵn định nghĩa :meth:`~object.__str__` để in tất cả các arguments mà không cần truy cập rõ ràng vào ``.args``.::

   >>> try:
   ...     raise Exception('spam', 'eggs')
   ... except Exception as inst:
   ...     print(type(inst))    # kiểu ngoại lệ
   ...     print(inst.args)     # các đối số được lưu trong .args
   ...     print(inst)          # __str__ cho phép in trực tiếp args,
   ...                          # nhưng có thể được ghi đè trong các subclass của exception
   ...     x, y = inst.args     # giải nén args
   ...     print('x =', x)
   ...     print('y =', y)
   ...
   <class 'Exception'>
   ('spam', 'eggs')
   ('spam', 'eggs')
   x = spam
   y = eggs

Đầu ra :meth:`~object.__str__` của exception được in dưới dạng phần cuối cùng ('chi tiết') của thông báo đối với các exception không được xử lý.

:exc:`BaseException` là lớp cơ sở chung của tất cả exception. Một trong các subclass của nó, :exc:`Exception`, là lớp cơ sở của tất cả exception không nghiêm trọng. Các exception không phải là subclass của :exc:`Exception` thường không được xử lý, vì chúng được dùng để cho biết rằng chương trình nên kết thúc. Chúng bao gồm :exc:`SystemExit`, được raise bởi :meth:`sys.exit`, và
:exc:`KeyboardInterrupt`, được raise khi người dùng muốn ngắt chương trình.

:exc:`Exception` có thể được sử dụng như một wildcard bắt được gần như mọi thứ. Tuy nhiên, nên chỉ định cụ thể nhất có thể các loại exception mà chúng ta dự định xử lý, đồng thời cho phép mọi exception không mong muốn được tiếp tục truyền lên.

Mẫu phổ biến nhất để xử lý :exc:`Exception` là in hoặc ghi log exception, sau đó raise lại exception đó (cho phép caller cũng xử lý exception).::

   import sys

   try:
       f = open('myfile.txt')
       s = f.readline()
       i = int(s.strip())
   except OSError as err:
       print("OS error:", err)
   except ValueError:
       print("Could not convert data to an integer.")
   except Exception as err:
       print(f"Unexpected {err=}, {type(err)=}")
       raise

Câu lệnh :keyword:`try` ... :keyword:`except` có một *else clause* tùy chọn; nếu có, mệnh đề này phải theo sau tất cả các *except clauses*. Mệnh đề này hữu ích cho phần code phải được thực thi nếu *try clause* không raise exception. Ví dụ::

   for arg in sys.argv[1:]:
       try:
           f = open(arg, 'r')
       except OSError:
           print('cannot open', arg)
       else:
           print(arg, 'has', len(f.readlines()), 'lines')
           f.close()

Sử dụng :keyword:`!else` clause tốt hơn việc thêm code vào :keyword:`try` clause vì cách này tránh vô tình bắt một exception không được raise bởi phần code được bảo vệ bởi :keyword:`!try` ...
Câu lệnh :keyword:`!except`.

Exception handler không chỉ xử lý các exception xảy ra ngay trong *try clause*, mà còn xử lý những exception xảy ra bên trong các hàm được gọi (kể cả gián tiếp) trong *try clause*. Ví dụ::

   >>> def this_fails():
   ...     x = 1/0
   ...
   >>> try:
   ...     this_fails()
   ... except ZeroDivisionError as err:
   ...     print('Handling run-time error:', err)
   ...
   Handling run-time error: division by zero


.. _tut-raising:

Raise Exception
===============

Câu lệnh :keyword:`raise` cho phép lập trình viên buộc một ngoại lệ được chỉ định xảy ra. Ví dụ::

   >>> raise NameError('HiThere')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       raise NameError('HiThere')
   NameError: HiThere

Đối số duy nhất của :keyword:`raise` cho biết ngoại lệ cần được đưa ra. Đối số này phải là một instance ngoại lệ hoặc một class ngoại lệ (một class kế thừa từ :class:`BaseException`, chẳng hạn như :exc:`Exception` hoặc một subclass của nó). Nếu truyền vào một class ngoại lệ, class đó sẽ được khởi tạo ngầm bằng cách gọi constructor của nó mà không có đối số nào::

   raise ValueError  # viết tắt của 'raise ValueError()'

Nếu bạn cần xác định xem một ngoại lệ có được đưa ra hay không nhưng không định xử lý nó, một dạng đơn giản hơn của câu lệnh :keyword:`raise` cho phép bạn đưa lại ngoại lệ đó::

   >>> try:
   ...     raise NameError('HiThere')
   ... except NameError:
   ...     print('An exception flew by!')
   ...     raise
   ...
   An exception flew by!
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise NameError('HiThere')
   NameError: HiThere


.. _tut-exception-chaining:

Chuỗi ngoại lệ
==============

Nếu một ngoại lệ chưa được xử lý xảy ra bên trong một khối :keyword:`except`, ngoại lệ đó sẽ được đính kèm với ngoại lệ đang được xử lý và được đưa vào thông báo lỗi::

    >>> try:
    ...     open("database.sqlite")
    ... except OSError:
    ...     raise RuntimeError("unable to handle error")
    ...
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
        open("database.sqlite")
        ~~~~^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'database.sqlite'
    <BLANKLINE>
    During handling of the above exception, another exception occurred:
    <BLANKLINE>
    Traceback (most recent call last):
      File "<stdin>", line 4, in <module>
        raise RuntimeError("unable to handle error")
    RuntimeError: unable to handle error

Để cho biết một ngoại lệ là hệ quả trực tiếp của một ngoại lệ khác,
Câu lệnh :keyword:`raise` cho phép một mệnh đề :keyword:`from<raise>` tùy chọn::

    # exc phải là một exception instance hoặc None.
    raise RuntimeError from exc

Điều này có thể hữu ích khi bạn chuyển đổi các exception. Ví dụ::

    >>> def func():
    ...     raise ConnectionError
    ...
    >>> try:
    ...     func()
    ... except ConnectionError as exc:
    ...     raise RuntimeError('Failed to open database') from exc
    ...
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
        func()
        ~~~~^^
      File "<stdin>", line 2, in func
    ConnectionError
    <BLANKLINE>
    The above exception was the direct cause of the following exception:
    <BLANKLINE>
    Traceback (most recent call last):
      File "<stdin>", line 4, in <module>
        raise RuntimeError('Failed to open database') from exc
    RuntimeError: Failed to open database

Câu lệnh này cũng cho phép vô hiệu hóa việc chaining exception tự động bằng idiom ``from None``::

    >>> try:
    ...     open('database.sqlite')
    ... except OSError:
    ...     raise RuntimeError from None
    ...
    Traceback (most recent call last):
      File "<stdin>", line 4, in <module>
        raise RuntimeError from None
    RuntimeError

Để biết thêm thông tin về cơ chế chaining, hãy xem :ref:`bltin-exceptions`.


.. _tut-userexceptions:

Các exception do người dùng định nghĩa
======================================

Các chương trình có thể đặt tên cho các exception của riêng mình bằng cách tạo một exception class mới (xem
:ref:`tut-classes` để biết thêm về các lớp Python). Các ngoại lệ thường nên được dẫn xuất từ lớp :exc:`Exception`, trực tiếp hoặc gián tiếp.

Có thể định nghĩa các lớp ngoại lệ thực hiện bất kỳ điều gì mà các lớp khác có thể thực hiện, nhưng chúng thường được giữ đơn giản, thường chỉ cung cấp một số thuộc tính cho phép các trình xử lý ngoại lệ trích xuất thông tin về lỗi.

Hầu hết các ngoại lệ được định nghĩa với tên kết thúc bằng "Error", tương tự như cách đặt tên của các ngoại lệ chuẩn.

Nhiều module chuẩn tự định nghĩa các ngoại lệ để báo cáo những lỗi có thể xảy ra trong các hàm do chúng định nghĩa.


.. _tut-cleanup:

Định nghĩa các tác vụ dọn dẹp
=============================

Câu lệnh :keyword:`try` có một mệnh đề tùy chọn khác, nhằm định nghĩa các tác vụ dọn dẹp phải được thực thi trong mọi trường hợp. Ví dụ:::

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print('Goodbye, world!')
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise KeyboardInterrupt
   KeyboardInterrupt

Nếu có mệnh đề :keyword:`finally`, mệnh đề :keyword:`!finally` sẽ thực thi như tác vụ cuối cùng trước khi câu lệnh :keyword:`try` hoàn tất. Mệnh đề :keyword:`!finally` sẽ chạy bất kể câu lệnh :keyword:`!try` có phát sinh ngoại lệ hay không. Các điểm sau đây thảo luận về những trường hợp phức tạp hơn khi xảy ra ngoại lệ:

* Nếu xảy ra ngoại lệ trong quá trình thực thi mệnh đề :keyword:`!try`, ngoại lệ đó có thể được xử lý bởi mệnh đề :keyword:`except`. Nếu ngoại lệ không được xử lý bởi mệnh đề :keyword:`!except`, ngoại lệ sẽ được ném lại sau khi mệnh đề :keyword:`!finally` đã được thực thi.

* Một ngoại lệ có thể xảy ra trong quá trình thực thi mệnh đề :keyword:`!except` hoặc :keyword:`!else`. Tương tự, ngoại lệ sẽ được ném lại sau khi mệnh đề :keyword:`!finally` đã được thực thi.

* Nếu mệnh đề :keyword:`!finally` thực thi một :keyword:`break`,
  :keyword:`continue` hoặc câu lệnh :keyword:`return`, các ngoại lệ sẽ không được ném lại. Điều này có thể gây nhầm lẫn và do đó không được khuyến khích. Kể từ phiên bản 3.14, compiler sẽ phát ra :exc:`SyntaxWarning` cho trường hợp này (xem :pep:`765`).

* Nếu câu lệnh :keyword:`!try` gặp một :keyword:`break`,
  :keyword:`continue` hoặc câu lệnh :keyword:`return`, thì
  mệnh đề :keyword:`!finally` sẽ được thực thi ngay trước
  việc thực thi câu lệnh :keyword:`!break`, :keyword:`!continue` hoặc :keyword:`!return`.

* Nếu mệnh đề :keyword:`!finally` chứa câu lệnh :keyword:`!return`, giá trị được trả về sẽ là giá trị từ
  câu lệnh :keyword:`!return` của mệnh đề :keyword:`!finally`, chứ không phải giá trị từ câu lệnh :keyword:`!return` của mệnh đề :keyword:`!try`. Điều này có thể gây khó hiểu và do đó không được khuyến khích. Kể từ phiên bản 3.14, trình biên dịch sẽ phát :exc:`SyntaxWarning` cho trường hợp này (xem :pep:`765`).

Ví dụ::

   >>> def bool_return():
   ...     try:
   ...         return True
   ...     finally:
   ...         return False
   ...
   >>> bool_return()
   False

Một ví dụ phức tạp hơn::

   >>> def divide(x, y):
   ...     try:
   ...         result = x / y
   ...     except ZeroDivisionError:
   ...         print("division by zero!")
   ...     else:
   ...         print("result is", result)
   ...     finally:
   ...         print("executing finally clause")
   ...
   >>> divide(2, 1)
   result is 2.0
   executing finally clause
   >>> divide(2, 0)
   division by zero!
   executing finally clause
   >>> divide("2", "1")
   executing finally clause
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       divide("2", "1")
       ~~~~~~^^^^^^^^^^
     File "<stdin>", line 3, in divide
       result = x / y
                ~~^~~
   TypeError: unsupported operand type(s) for /: 'str' and 'str'

Như bạn có thể thấy, mệnh đề :keyword:`finally` luôn được thực thi trong mọi trường hợp. Câu lệnh
:exc:`TypeError` phát sinh do chia hai chuỗi không được xử lý bởi
:keyword:`except` mệnh đề và do đó được phát sinh lại sau khi mệnh đề :keyword:`!finally` đã được thực thi.

Trong các ứng dụng thực tế, mệnh đề :keyword:`finally` hữu ích để giải phóng các tài nguyên bên ngoài (chẳng hạn như tệp hoặc kết nối mạng), bất kể việc sử dụng tài nguyên có thành công hay không.


.. _tut-cleanup-with:

Tác vụ dọn dẹp được định nghĩa sẵn
==================================

Một số đối tượng định nghĩa các tác vụ dọn dẹp tiêu chuẩn cần được thực hiện khi đối tượng không còn cần thiết, bất kể thao tác sử dụng đối tượng đó thành công hay thất bại. Hãy xem ví dụ sau, trong đó chương trình cố gắng mở một tệp và in nội dung của tệp ra màn hình.::

   for line in open("myfile.txt"):
       print(line, end="")

Vấn đề với đoạn mã này là nó để tệp mở trong một khoảng thời gian không xác định sau khi phần mã này thực thi xong. Đây không phải là vấn đề trong các script đơn giản, nhưng có thể gây ra vấn đề cho các ứng dụng lớn hơn. Câu lệnh :keyword:`with` cho phép sử dụng các đối tượng như tệp theo cách đảm bảo chúng luôn được dọn dẹp kịp thời và đúng cách.::

   with open("myfile.txt") as f:
       for line in f:
           print(line, end="")

Sau khi câu lệnh được thực thi, tệp *f* luôn được đóng, ngay cả khi gặp vấn đề trong quá trình xử lý các dòng. Những đối tượng, như tệp, cung cấp các tác vụ dọn dẹp được định nghĩa sẵn sẽ nêu rõ điều này trong tài liệu của chúng.


.. _tut-exception-groups:

Phát sinh và xử lý nhiều ngoại lệ không liên quan
=================================================

Có những tình huống cần báo cáo nhiều ngoại lệ đã xảy ra. Điều này thường gặp trong các framework concurrency, khi nhiều tác vụ có thể đã thất bại song song, nhưng cũng có những trường hợp sử dụng khác mà việc tiếp tục thực thi và thu thập nhiều lỗi thay vì raise ngoại lệ đầu tiên là điều mong muốn.

Builtin :exc:`ExceptionGroup` bao bọc một danh sách các instance ngoại lệ để chúng có thể được raise cùng nhau. Bản thân nó là một ngoại lệ, vì vậy có thể được catch như mọi ngoại lệ khác.::

   >>> def f():
   ...     excs = [OSError('error 1'), SystemError('error 2')]
   ...     raise ExceptionGroup('there were problems', excs)
   ...
   >>> f()
     + Exception Group Traceback (most recent call last):
     |   File "<stdin>", line 1, in <module>
     |     f()
     |     ~^^
     |   File "<stdin>", line 3, in f
     |     raise ExceptionGroup('there were problems', excs)
     | ExceptionGroup: there were problems (2 sub-exceptions)
     +-+---------------- 1 ----------------
       | OSError: error 1
       +---------------- 2 ----------------
       | SystemError: error 2
       +------------------------------------
   >>> try:
   ...     f()
   ... except Exception as e:
   ...     print(f'caught {type(e)}: {e}')
   ...
   caught <class 'ExceptionGroup'>: there were problems (2 sub-exceptions)
   >>>

Bằng cách sử dụng ``except*`` thay cho ``except``, chúng ta có thể chỉ xử lý những ngoại lệ trong group khớp với một kiểu nhất định. Trong ví dụ sau, minh họa một exception group lồng nhau, mỗi mệnh đề ``except*`` sẽ trích xuất khỏi group các ngoại lệ thuộc một kiểu nhất định, đồng thời để mọi ngoại lệ khác propagate đến các mệnh đề khác và cuối cùng được raise lại.::

   >>> def f():
   ...     raise ExceptionGroup(
   ...         "group1",
   ...         [
   ...             OSError(1),
   ...             SystemError(2),
   ...             ExceptionGroup(
   ...                 "group2",
   ...                 [
   ...                     OSError(3),
   ...                     RecursionError(4)
   ...                 ]
   ...             )
   ...         ]
   ...     )
   ...
   >>> try:
   ...     f()
   ... except* OSError as e:
   ...     print("There were OSErrors")
   ... except* SystemError as e:
   ...     print("There were SystemErrors")
   ...
   There were OSErrors
   There were SystemErrors
     + Exception Group Traceback (most recent call last):
     |   File "<stdin>", line 2, in <module>
     |     f()
     |     ~^^
     |   File "<stdin>", line 2, in f
     |     raise ExceptionGroup(
     |     ...<12 lines>...
     |     )
     | ExceptionGroup: group1 (1 sub-exception)
     +-+---------------- 1 ----------------
       | ExceptionGroup: group2 (1 sub-exception)
       +-+---------------- 1 ----------------
         | RecursionError: 4
         +------------------------------------
   >>>

Lưu ý rằng các ngoại lệ được lồng trong một exception group phải là instance, không phải type. Điều này là vì trong thực tế, các ngoại lệ thường là những ngoại lệ đã được chương trình raise và catch theo mẫu sau đây::

   >>> excs = []
   ... for test in tests:
   ...     try:
   ...         test.run()
   ...     except Exception as e:
   ...         excs.append(e)
   ...
   >>> if excs:
   ...    raise ExceptionGroup("Test Failures", excs)
   ...


.. _tut-exception-notes:

Bổ sung ghi chú cho ngoại lệ
============================

Khi một ngoại lệ được tạo để raise, nó thường được khởi tạo với thông tin mô tả lỗi đã xảy ra. Có những trường hợp việc bổ sung thông tin sau khi đã catch ngoại lệ sẽ rất hữu ích. Vì mục đích này, các ngoại lệ có một phương thức ``add_note(note)`` nhận một chuỗi và thêm chuỗi đó vào danh sách ghi chú của ngoại lệ. Việc hiển thị traceback tiêu chuẩn bao gồm tất cả ghi chú, theo thứ tự chúng được thêm vào, sau ngoại lệ.::

   >>> try:
   ...     raise TypeError('bad type')
   ... except Exception as e:
   ...     e.add_note('Add some information')
   ...     e.add_note('Add some more information')
   ...     raise
   ...
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise TypeError('bad type')
   TypeError: bad type
   Add some information
   Add some more information
   >>>

Ví dụ, khi thu thập các ngoại lệ vào một exception group, chúng ta có thể muốn thêm thông tin ngữ cảnh cho từng lỗi riêng lẻ. Trong ví dụ sau, mỗi ngoại lệ trong group có một ghi chú cho biết lỗi này đã xảy ra khi nào.::

   >>> def f():
   ...     raise OSError('operation failed')
   ...
   >>> excs = []
   >>> for i in range(3):
   ...     try:
   ...         f()
   ...     except Exception as e:
   ...         e.add_note(f'Happened in Iteration {i+1}')
   ...         excs.append(e)
   ...
   >>> raise ExceptionGroup('We have some problems', excs)
     + Exception Group Traceback (most recent call last):
     |   File "<stdin>", line 1, in <module>
     |     raise ExceptionGroup('We have some problems', excs)
     | ExceptionGroup: We have some problems (3 sub-exceptions)
     +-+---------------- 1 ----------------
       | Traceback (most recent call last):
       |   File "<stdin>", line 3, in <module>
       |     f()
       |     ~^^
       |   File "<stdin>", line 2, in f
       |     raise OSError('operation failed')
       | OSError: operation failed
       | Happened in Iteration 1
       +---------------- 2 ----------------
       | Traceback (most recent call last):
       |   File "<stdin>", line 3, in <module>
       |     f()
       |     ~^^
       |   File "<stdin>", line 2, in f
       |     raise OSError('operation failed')
       | OSError: operation failed
       | Happened in Iteration 2
       +---------------- 3 ----------------
       | Traceback (most recent call last):
       |   File "<stdin>", line 3, in <module>
       |     f()
       |     ~^^
       |   File "<stdin>", line 2, in f
       |     raise OSError('operation failed')
       | OSError: operation failed
       | Happened in Iteration 3
       +------------------------------------
   >>>
