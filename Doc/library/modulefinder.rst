:mod:`!modulefinder` --- Tìm các mô-đun được một tập lệnh sử dụng
=================================================================

.. module:: modulefinder
   :synopsis: Tìm các mô-đun được một tập lệnh sử dụng.

.. sectionauthor:: A.M. Kuchling <amk@amk.ca>

**Mã nguồn:** :source:`Lib/modulefinder.py`

--------------

Mô-đun này cung cấp một lớp :class:`ModuleFinder` có thể được sử dụng để xác định tập hợp các mô-đun được một tập lệnh import. ``modulefinder.py`` cũng có thể được chạy như một tập lệnh, với tên tệp của một tập lệnh Python làm đối số; sau đó, một báo cáo về các mô-đun đã import sẽ được in ra.


.. function:: AddPackagePath(pkg_name, path)

   Ghi nhận rằng package có tên *pkg_name* có thể được tìm thấy trong *path* được chỉ định.


.. function:: ReplacePackage(oldname, newname)

   Cho phép chỉ định rằng mô-đun có tên *oldname* thực chất là package có tên *newname*.


.. class:: ModuleFinder(path=None, debug=0, excludes=[], replace_paths=[])

   Lớp này cung cấp các phương thức :meth:`run_script` và :meth:`report` để xác định tập hợp các mô-đun được một tập lệnh import. *path* có thể là một danh sách các thư mục để tìm kiếm mô-đun; nếu không được chỉ định, ``sys.path`` sẽ được sử dụng. *debug* đặt mức độ debug; các giá trị cao hơn khiến lớp in ra các thông báo debug về những gì nó đang thực hiện. *excludes* là một danh sách các tên mô-đun cần loại trừ khỏi quá trình phân tích. *replace_paths* là một danh sách các tuple ``(oldpath, newpath)`` sẽ được thay thế trong các đường dẫn mô-đun.


   .. method:: report()

      In ra đầu ra tiêu chuẩn một báo cáo liệt kê các module được script import và đường dẫn của chúng, cũng như các module bị thiếu hoặc có vẻ bị thiếu.

   .. method:: run_script(pathname)

      Phân tích nội dung của tệp *pathname*, tệp này phải chứa mã Python.

   .. attribute:: modules

      Một dictionary ánh xạ tên module với các module. Xem
      :ref:`modulefinder-example`.


.. _modulefinder-example:

Ví dụ sử dụng :class:`ModuleFinder`
-----------------------------------

Script sẽ được phân tích sau đó (bacon.py)::

   import re, itertools

   try:
       import baconhameggs
   except ImportError:
       pass

   try:
       import guido.python.ham
   except ImportError:
       pass


Script sẽ xuất báo cáo về bacon.py::

   from modulefinder import ModuleFinder

   finder = ModuleFinder()
   finder.run_script('bacon.py')

   print('Loaded modules:')
   for name, mod in finder.modules.items():
       print('%s: ' % name, end='')
       print(','.join(list(mod.globalnames.keys())[:3]))

   print('-'*50)
   print('Modules not imported:')
   print('\n'.join(finder.badmodules.keys()))

Đầu ra mẫu (có thể thay đổi tùy thuộc vào kiến trúc)::

    Loaded modules:
    _types:
    copyreg:  _inverted_registry,_slotnames,__all__
    re._compiler:  isstring,_sre,_optimize_unicode
    _sre:
    re._constants:  REPEAT_ONE,makedict,AT_END_LINE
    sys:
    re:  __module__,finditer,_expand
    itertools:
    __main__:  re,itertools,baconhameggs
    re._parser:  _PATTERNENDERS,SRE_FLAG_UNICODE
    array:
    types:  __module__,IntType,TypeType
    ---------------------------------------------------
    Modules not imported:
    guido.python.ham
    baconhameggs


