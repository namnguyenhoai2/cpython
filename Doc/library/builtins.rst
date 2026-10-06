:mod:`!builtins` --- Đối tượng tích hợp sẵn
===========================================

.. module:: builtins
   :synopsis: Mô-đun cung cấp namespace tích hợp sẵn.

--------------

Mô-đun này cung cấp quyền truy cập trực tiếp vào tất cả các định danh 'tích hợp sẵn' của Python; chẳng hạn, ``builtins.open`` là tên đầy đủ của hàm tích hợp sẵn :func:`open`.

Mô-đun này thường không được hầu hết các ứng dụng truy cập một cách tường minh, nhưng có thể hữu ích trong các mô-đun cung cấp các đối tượng có cùng tên với một giá trị tích hợp sẵn, đồng thời cũng cần đến giá trị tích hợp sẵn có tên đó. Ví dụ: trong một mô-đun muốn triển khai hàm :func:`open` bao bọc hàm tích hợp sẵn
:func:`open`, mô-đun này có thể được sử dụng trực tiếp::

   import builtins

   def open(path):
       f = builtins.open(path, 'r')
       return UpperCaser(f)

   class UpperCaser:
       '''Wrapper around a file that converts output to uppercase.'''

       def __init__(self, f):
           self._f = f

       def read(self, count=-1):
           return self._f.read(count).upper()

       # ...

Về chi tiết triển khai, hầu hết các mô-đun đều có tên ``__builtins__`` được cung cấp như một phần của các biến global. Giá trị của ``__builtins__`` thường là mô-đun này hoặc giá trị của thuộc tính :attr:`~object.__dict__` của mô-đun này. Vì đây là chi tiết triển khai, các bản triển khai khác của Python có thể không sử dụng nó.

.. seealso::

   * :ref:`built-in-consts`
   * :ref:`bltin-exceptions`
   * :ref:`built-in-funcs`
   * :ref:`bltin-types`
