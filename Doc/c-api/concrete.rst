.. highlight:: c


.. _concrete:

*********************
Tầng đối tượng cụ thể
*********************

Các hàm trong chương này dành riêng cho một số kiểu đối tượng Python nhất định. Việc truyền cho chúng một đối tượng không đúng kiểu là điều không nên làm; nếu nhận được một đối tượng từ chương trình Python và không chắc đối tượng đó có đúng kiểu hay không, trước tiên bạn phải thực hiện kiểm tra kiểu; ví dụ, để kiểm tra xem một đối tượng có phải là dictionary hay không, hãy sử dụng :c:func:`PyDict_Check`. Chương này được tổ chức theo dạng "cây gia đình" của các kiểu đối tượng Python.

.. warning::

   Mặc dù các hàm được mô tả trong chương này kiểm tra cẩn thận kiểu của những đối tượng được truyền vào, nhiều hàm trong số đó không kiểm tra xem ``NULL`` có được truyền vào thay cho một đối tượng hợp lệ hay không. Việc cho phép truyền ``NULL`` có thể gây ra lỗi vi phạm truy cập bộ nhớ và khiến trình thông dịch kết thúc ngay lập tức.


.. _fundamental:

Đối tượng cơ bản
================

Phần này mô tả các đối tượng kiểu Python và đối tượng singleton ``None``.

.. toctree::

   type.rst
   none.rst


.. _numericobjects:

Đối tượng số
============

.. index:: pair: object; numeric

.. toctree::

   long.rst
   bool.rst
   float.rst
   complex.rst


.. _sequenceobjects:

Đối tượng dãy
=============

.. index:: pair: object; sequence

Các thao tác chung trên đối tượng sequence đã được trình bày trong chương trước; phần này đề cập đến những loại đối tượng sequence cụ thể vốn có trong ngôn ngữ Python.

.. XXX sort out unicode, str, bytes and bytearray

.. toctree::

   bytes.rst
   bytearray.rst
   unicode.rst
   tuple.rst
   list.rst


.. _mapobjects:

Đối tượng container
===================

.. index:: pair: object; mapping

.. toctree::

   dict.rst
   set.rst


.. _otherobjects:

Đối tượng function
==================

.. toctree::

   function.rst
   method.rst
   cell.rst
   code.rst


Các đối tượng khác
==================

.. toctree::

   file.rst
   module.rst
   iterator.rst
   descriptor.rst
   slice.rst
   memoryview.rst
   picklebuffer.rst
   weakref.rst
   capsule.rst
   frame.rst
   gen.rst
   coro.rst
   contextvars.rst
   typehints.rst


C API cho các module mở rộng
============================

.. toctree::

   curses.rst
   datetime.rst
