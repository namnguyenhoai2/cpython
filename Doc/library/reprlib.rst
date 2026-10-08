:mod:`!reprlib` --- Cài đặt :func:`repr` thay thế
=================================================

.. module:: reprlib
   :synopsis: Cài đặt repr() thay thế với các giới hạn kích thước.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/reprlib.py`

--------------

Module :mod:`!reprlib` cung cấp một phương thức để tạo biểu diễn của đối tượng với các giới hạn về kích thước của chuỗi kết quả. Phương thức này được sử dụng trong trình gỡ lỗi Python và cũng có thể hữu ích trong các ngữ cảnh khác.

Module này cung cấp một class, một instance và một function:


.. class:: Repr(*, maxlevel=6, maxtuple=6, maxlist=6, maxarray=5, maxdict=4, \
                maxset=6, maxfrozenset=6, maxdeque=6, maxstring=30, maxlong=40, \ maxother=30, fillvalue="...", indent=None)

   Class cung cấp các dịch vụ định dạng hữu ích trong việc triển khai những function tương tự như :func:`repr` tích hợp sẵn; các giới hạn kích thước cho những loại đối tượng khác nhau được thêm vào để tránh tạo ra các biểu diễn quá dài.

   Các đối số từ khóa của hàm khởi tạo có thể được dùng như một cách viết tắt để thiết lập các thuộc tính của thể hiện :class:`Repr`. Điều này có nghĩa là phép khởi tạo sau đây::

      aRepr = reprlib.Repr(maxlevel=3)

   Tương đương với::

      aRepr = reprlib.Repr()
      aRepr.maxlevel = 3

   Xem phần `Repr Objects <Repr Objects_>`_ để biết thêm thông tin về các thuộc tính :class:`Repr`.

   .. versionchanged:: 3.12
      Cho phép thiết lập các thuộc tính thông qua đối số từ khóa.


.. data:: aRepr

   Đây là một thể hiện của :class:`Repr`, được dùng để cung cấp
   hàm :func:`.repr` được mô tả bên dưới. Việc thay đổi các thuộc tính của đối tượng này sẽ ảnh hưởng đến các giới hạn kích thước được :func:`.repr` và trình gỡ lỗi Python sử dụng.


.. function:: repr(obj)

   Đây là phương thức :meth:`~Repr.repr` của ``aRepr``. Phương thức này trả về một chuỗi tương tự chuỗi được hàm dựng sẵn cùng tên trả về, nhưng có giới hạn đối với hầu hết các kích thước.

Ngoài các công cụ giới hạn kích thước, mô-đun này còn cung cấp một decorator để phát hiện các lệnh gọi đệ quy đến :meth:`~object.__repr__` và thay thế chúng bằng một chuỗi giữ chỗ.


.. index:: single: ...; placeholder

.. decorator:: recursive_repr(fillvalue="...")

   Decorator cho các phương thức :meth:`~object.__repr__` để phát hiện các lệnh gọi đệ quy trong cùng một thread. Nếu thực hiện một lệnh gọi đệ quy, *fillvalue* sẽ được trả về; nếu không, lệnh gọi :meth:`!__repr__` thông thường sẽ được thực hiện. Ví dụ:

   .. doctest::

      >>> from reprlib import recursive_repr
      >>> class MyList(list):
      ...     @recursive_repr()
      ...     def __repr__(self):
      ...         return '<' + '|'.join(map(repr, self)) + '>'
      ...
      >>> m = MyList('abc')
      >>> m.append(m)
      >>> m.append('x')
      >>> print(m)
      <'a'|'b'|'c'|...|'x'>

   .. versionadded:: 3.2


.. _repr-objects:

.. _`Repr Objects`:

Đối tượng Repr
--------------

Các thực thể :class:`Repr` cung cấp một số thuộc tính có thể được dùng để giới hạn kích thước biểu diễn của các kiểu đối tượng khác nhau, cùng các phương thức định dạng những kiểu đối tượng cụ thể.


.. attribute:: Repr.fillvalue

   Chuỗi này được hiển thị cho các tham chiếu đệ quy. Giá trị mặc định là ``...``.

   .. versionadded:: 3.11


.. attribute:: Repr.maxlevel

   Giới hạn độ sâu khi tạo các biểu diễn đệ quy. Giá trị mặc định là ``6``.


.. attribute:: Repr.maxdict
               Repr.maxlist Repr.maxtuple Repr.maxset Repr.maxfrozenset Repr.maxdeque Repr.maxarray

   Giới hạn số lượng mục được biểu diễn cho kiểu đối tượng có tên. Giá trị mặc định là ``4`` cho :attr:`maxdict`, ``5`` cho :attr:`maxarray`, và ``6`` cho các kiểu còn lại.


.. attribute:: Repr.maxlong

   Số ký tự tối đa trong phần biểu diễn của một số nguyên. Các chữ số ở giữa sẽ bị lược bỏ. Giá trị mặc định là ``40``.


.. attribute:: Repr.maxstring

   Giới hạn số ký tự trong phần biểu diễn của chuỗi. Lưu ý rằng phần biểu diễn "bình thường" của chuỗi được dùng làm nguồn ký tự: nếu cần các chuỗi escape trong phần biểu diễn, chúng có thể bị biến đổi khi phần biểu diễn được rút ngắn. Giá trị mặc định là ``30``.


.. attribute:: Repr.maxother

   Giới hạn này được dùng để kiểm soát kích thước của các kiểu đối tượng không có phương thức định dạng cụ thể trên đối tượng :class:`Repr`. Giới hạn được áp dụng tương tự như :attr:`maxstring`. Giá trị mặc định là ``20``.


.. attribute:: Repr.indent

   Nếu thuộc tính này được đặt thành ``None`` (mặc định), đầu ra sẽ được định dạng không có ngắt dòng hoặc thụt lề, giống như :func:`repr` tiêu chuẩn. Ví dụ:

   .. doctest:: indent

      >>> example = [
      ...     1, 'spam', {'a': 2, 'b': 'spam eggs', 'c': {3: 4.5, 6: []}}, 'ham']
      >>> import reprlib
      >>> aRepr = reprlib.Repr()
      >>> print(aRepr.repr(example))
      [1, 'spam', {'a': 2, 'b': 'spam eggs', 'c': {3: 4.5, 6: []}}, 'ham']

   Nếu :attr:`~Repr.indent` được đặt thành một chuỗi, mỗi cấp đệ quy sẽ được đặt trên một dòng riêng và thụt lề bằng chuỗi đó:

   .. doctest:: indent

      >>> aRepr.indent = '-->'
      >>> print(aRepr.repr(example))
      [
      -->1,
      -->'spam',
      -->{
      -->-->'a': 2,
      -->-->'b': 'spam eggs',
      -->-->'c': {
      -->-->-->3: 4.5,
      -->-->-->6: [],
      -->-->},
      -->},
      -->'ham',
      ]

   Đặt :attr:`~Repr.indent` thành một giá trị số nguyên dương sẽ cho kết quả như khi đặt nó thành một chuỗi có số dấu cách tương ứng:

   .. doctest:: indent

      >>> aRepr.indent = 4
      >>> print(aRepr.repr(example))
      [
          1,
          'spam',
          {
              'a': 2,
              'b': 'spam eggs',
              'c': {
                  3: 4.5,
                  6: [],
              },
          },
          'ham',
      ]

   .. versionadded:: 3.12


.. method:: Repr.repr(obj)

   Tương đương với :func:`repr` tích hợp sẵn, sử dụng định dạng do instance áp đặt.


.. method:: Repr.repr1(obj, level)

   Phần triển khai đệ quy được :meth:`.repr` sử dụng. Phần này dùng kiểu của *obj* để xác định phương thức định dạng nào cần gọi, truyền cho phương thức đó *obj* và *level*. Các phương thức dành riêng cho từng kiểu nên gọi :meth:`repr1` để thực hiện định dạng đệ quy, với giá trị của *level* trong lời gọi đệ quy là ``level - 1``.


.. method:: Repr.repr_TYPE(obj, level)
   :noindex:

   Các phương thức định dạng cho từng kiểu cụ thể được triển khai dưới dạng các phương thức có tên dựa trên tên kiểu. Trong tên phương thức, **TYPE** được thay thế bằng ``'_'.join(type(obj).__name__.split())``. Việc điều phối đến các phương thức này do :meth:`repr1` xử lý. Các phương thức dành riêng cho từng kiểu cần định dạng đệ quy một giá trị nên gọi ``self.repr1(subobj, level - 1)``.


.. _subclassing-reprs:

Kế thừa Repr Objects
--------------------

Việc :meth:`Repr.repr1` sử dụng cơ chế dispatch động cho phép các lớp con của
:class:`Repr` bổ sung hỗ trợ cho các kiểu đối tượng tích hợp khác hoặc thay đổi cách xử lý các kiểu đã được hỗ trợ. Ví dụ này cho thấy cách bổ sung hỗ trợ đặc biệt cho các đối tượng tệp:

.. testcode::

   import reprlib
   import sys

   class MyRepr(reprlib.Repr):

       def repr_TextIOWrapper(self, obj, level):
           if obj.name in {'<stdin>', '<stdout>', '<stderr>'}:
               return obj.name
           return repr(obj)

   aRepr = MyRepr()
   print(aRepr.repr(sys.stdin))         # in ra '<stdin>'

.. testoutput::

   <stdin>
