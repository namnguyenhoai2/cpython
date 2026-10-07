.. highlight:: c

Curses C API
------------

:mod:`curses` cung cấp một giao diện C nhỏ cho các extension module. Consumer phải include tệp header :file:`py_curses.h` (theo mặc định, :file:`Python.h` không include tệp này) và phải gọi :c:func:`import_curses`, thường là một phần của hàm khởi tạo module, để điền
:c:var:`PyCurses_API`.

.. warning::

   Cả C API lẫn module Python thuần :mod:`curses` đều không tương thích với subinterpreter.

.. c:macro:: import_curses()

   Import Curses C API. Macro này không cần dấu chấm phẩy khi được gọi.

   Nếu thành công, điền con trỏ :c:var:`PyCurses_API`.

   Nếu thất bại, đặt :c:var:`PyCurses_API` thành NULL và thiết lập một exception. Caller phải kiểm tra xem có xảy ra lỗi hay không thông qua :c:func:`PyErr_Occurred`:

   .. code-block::

      import_curses();  // dấu chấm phẩy là tùy chọn nhưng được khuyến nghị
      if (PyErr_Occurred()) { /* cleanup */ }


.. c:var:: void **PyCurses_API

   Đối tượng được cấp phát động chứa C API của curses. Biến này chỉ khả dụng sau khi :c:macro:`import_curses` thành công.

   ``PyCurses_API[0]`` tương ứng với :c:data:`PyCursesWindow_Type`.

   ``PyCurses_API[1]``, ``PyCurses_API[2]`` và ``PyCurses_API[3]`` là các con trỏ tới những hàm predicate thuộc kiểu ``int (*)(void)``.

   Khi được gọi, các predicate này trả về liệu :func:`curses.setupterm`,
   :func:`curses.initscr` và :func:`curses.start_color` lần lượt đã được gọi hay chưa.

   Xem thêm các macro tiện ích :c:macro:`PyCursesSetupTermCalled`,
   :c:macro:`PyCursesInitialised` và :c:macro:`PyCursesInitialisedColor`.

   .. note::

      Số lượng mục trong cấu trúc này có thể thay đổi. Hãy cân nhắc sử dụng :c:macro:`PyCurses_API_pointers` để kiểm tra xem có các trường mới hay không.


.. c:macro:: PyCurses_API_pointers

   Số lượng trường có thể truy cập (``4``) trong :c:var:`PyCurses_API`. Số này được tăng lên mỗi khi có trường mới được thêm vào.


.. c:var:: PyTypeObject PyCursesWindow_Type

   Kiểu :ref:`heap <heap-types>` tương ứng với :class:`curses.window`.


.. c:function:: int PyCursesWindow_Check(PyObject *op)

   Trả về true nếu *op* là một :class:`curses.window` instance, ngược lại trả về false.


Các macro sau đây là những macro tiện ích được mở rộng thành các câu lệnh C. Cụ thể, chúng chỉ có thể được sử dụng dưới dạng ``macro;`` hoặc ``macro``, nhưng không thể dưới dạng ``macro()`` hoặc ``macro();``.

.. c:macro:: PyCursesSetupTermCalled

   Macro kiểm tra xem :func:`curses.setupterm` đã được gọi hay chưa.

   Khai triển macro gần tương đương với:

   .. code-block::

      {
          typedef int (*predicate_t)(void);
          predicate_t was_setupterm_called = (predicate_t)PyCurses_API[1];
          if (!was_setupterm_called()) {
              return NULL;
          }
      }


.. c:macro:: PyCursesInitialised

   Macro kiểm tra xem :func:`curses.initscr` đã được gọi hay chưa.

   Khai triển macro gần tương đương với:

   .. code-block::

      {
          typedef int (*predicate_t)(void);
          predicate_t was_initscr_called = (predicate_t)PyCurses_API[2];
          if (!was_initscr_called()) {
              return NULL;
          }
      }


.. c:macro:: PyCursesInitialisedColor

   Macro kiểm tra xem :func:`curses.start_color` đã được gọi hay chưa.

   Khai triển macro gần tương đương với:

   .. code-block::

      {
          typedef int (*predicate_t)(void);
          predicate_t was_start_color_called = (predicate_t)PyCurses_API[3];
          if (!was_start_color_called()) {
              return NULL;
          }
      }


Dữ liệu nội bộ
--------------

Các đối tượng sau được C API cung cấp nhưng nên được xem là chỉ dùng nội bộ.

.. c:macro:: PyCurses_CAPSULE_NAME

   Tên của capsule curses cần truyền vào :c:func:`PyCapsule_Import`.

   Chỉ sử dụng nội bộ. Thay vào đó, hãy dùng :c:macro:`import_curses`.

