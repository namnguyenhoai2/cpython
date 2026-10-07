.. highlight:: c

.. _abstract:

*************************
Tầng Đối tượng Trừu tượng
*************************

Các hàm trong chương này tương tác với các đối tượng Python bất kể kiểu của chúng, hoặc với các nhóm lớn gồm nhiều kiểu đối tượng (ví dụ: tất cả các kiểu số hoặc tất cả các kiểu chuỗi). Khi được sử dụng với những kiểu đối tượng mà chúng không áp dụng được, các hàm này sẽ phát sinh một ngoại lệ Python.

Không thể sử dụng các hàm này trên những đối tượng chưa được khởi tạo đúng cách, chẳng hạn như một đối tượng danh sách được tạo bởi :c:func:`PyList_New`, nhưng các phần tử của nó chưa được đặt thành một giá trị \ ``NULL`` nào đó.

.. toctree::

   object.rst
   call.rst
   number.rst
   sequence.rst
   mapping.rst
   iter.rst
   buffer.rst
