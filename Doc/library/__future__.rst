:mod:`!__future__` --- Định nghĩa các câu lệnh future
=====================================================

.. module:: __future__
   :synopsis: Future statement definitions

**Mã nguồn:** :source:`Lib/__future__.py`

--------------

Các import có dạng ``from __future__ import feature`` được gọi là
:ref:`các câu lệnh future <future>`. Trình biên dịch Python xử lý đặc biệt các câu lệnh này để cho phép sử dụng những tính năng Python mới trong các module chứa câu lệnh future trước bản phát hành mà trong đó tính năng đó trở thành tiêu chuẩn.

Mặc dù các câu lệnh future này được trình biên dịch Python gán thêm ý nghĩa đặc biệt, chúng vẫn được thực thi như mọi câu lệnh import khác và :mod:`!__future__` vẫn tồn tại, đồng thời được hệ thống import xử lý giống như bất kỳ module Python nào khác. Thiết kế này phục vụ ba mục đích:

* Tránh gây nhầm lẫn cho các công cụ hiện có vốn phân tích các câu lệnh import và mong đợi tìm thấy những module mà chúng đang import.

* Ghi lại thời điểm các thay đổi không tương thích được giới thiệu, cũng như thời điểm chúng sẽ được — hoặc đã được — bắt buộc áp dụng. Đây là một dạng tài liệu có thể thực thi và có thể được kiểm tra bằng lập trình thông qua việc import :mod:`!__future__` rồi kiểm tra nội dung của nó.

* Để đảm bảo rằng các :ref:`câu lệnh future <future>` chạy trên các bản phát hành trước Python 2.1 ít nhất cũng tạo ra ngoại lệ runtime (việc import :mod:`!__future__` sẽ thất bại vì trước phiên bản 2.1 không có module nào mang tên đó).

Nội dung module
---------------

Mô tả về bất kỳ tính năng nào cũng sẽ không bao giờ bị xóa khỏi :mod:`!__future__`. Kể từ khi được giới thiệu trong Python 2.1, các tính năng sau đã được đưa vào ngôn ngữ bằng cơ chế này:


.. list-table::
   :widths: auto
   :header-rows: 1

   * * tính năng
     * tùy chọn trong
     * bắt buộc trong
     * tác động
   * * .. data:: nested_scopes
     * 2.1.0b1
     * 2.2
     * :pep:`227`: *Phạm vi lồng nhau tĩnh*
   * * .. data:: generators
     * 2.2.0a1
     * 2.3
     * :pep:`255`: *Generator đơn giản*
   * * .. data:: division
     * 2.2.0a2
     * 3.0
     * :pep:`238`: *Thay đổi toán tử chia*
   * * .. data:: absolute_import
     * 2.5.0a1
     * 3.0
     * :pep:`328`: *Import: Nhiều dòng và tuyệt đối/tương đối*
   * * .. data:: with_statement
     * 2.5.0a1
     * 2.6
     * :pep:`343`: *Câu lệnh “with”*
   * * .. data:: print_function
     * 2.6.0a2
     * 3.0
     * :pep:`3105`: *Biến print thành một hàm*
   * * .. data:: unicode_literals
     * 2.6.0a2
     * 3.0
     * :pep:`3112`: *Literal bytes trong Python 3000*
   * * .. data:: generator_stop
     * 3.5.0b1
     * 3.7
     * :pep:`479`: *Xử lý StopIteration bên trong generator*
   * * .. data:: annotations
     * 3.7.0b1
     * Never [1]_
     * :pep:`563`: *Đánh giá trì hoãn các chú thích*,
       :pep:`649`: *Đánh giá trì hoãn các chú thích bằng descriptor*

.. XXX Adding a new entry?  Remember to update simple_stmts.rst, too.

.. _future-classes:

.. class:: _Feature

   Each statement in :file:`__future__.py` is of the form::

      FeatureName = _Feature(OptionalRelease, MandatoryRelease,
                             CompilerFlag)

   where, normally, *OptionalRelease* is less than *MandatoryRelease*, and both are
   5-tuples of the same form as :data:`sys.version_info`::

      (PY_MAJOR_VERSION, # the 2 in 2.1.0a3; an int
       PY_MINOR_VERSION, # the 1; an int
       PY_MICRO_VERSION, # the 0; an int
       PY_RELEASE_LEVEL, # "alpha", "beta", "candidate" or "final"; string
       PY_RELEASE_SERIAL # the 3; an int
      )

.. method:: _Feature.getOptionalRelease()

   *OptionalRelease* ghi nhận bản phát hành đầu tiên mà tính năng được chấp nhận.

.. method:: _Feature.getMandatoryRelease()

   Trong trường hợp một *MandatoryRelease* chưa xảy ra, *MandatoryRelease* dự đoán bản phát hành mà trong đó tính năng sẽ trở thành một phần của ngôn ngữ.

   Nếu không, *MandatoryRelease* ghi lại thời điểm tính năng trở thành một phần của ngôn ngữ; trong các bản phát hành từ thời điểm đó trở đi, các module không còn cần câu lệnh future để sử dụng tính năng nói trên, nhưng vẫn có thể tiếp tục dùng các import như vậy.

   *MandatoryRelease* cũng có thể là ``None``, nghĩa là một tính năng đã được lên kế hoạch bị loại bỏ hoặc vẫn chưa có quyết định.

.. attribute:: _Feature.compiler_flag

   *CompilerFlag* là cờ (bitfield) cần được truyền vào đối số thứ tư của hàm tích hợp :func:`compile` để bật tính năng trong mã được biên dịch động. Cờ này được lưu trong thuộc tính :attr:`_Feature.compiler_flag` trên các thực thể :class:`_Feature`.

.. [1]``from __future__ import annotations`` trước đây được dự kiến sẽ trở thành bắt buộc trong Python 3.10, nhưng thay đổi này đã bị trì hoãn và cuối cùng bị hủy bỏ. Tính năng này cuối cùng sẽ bị deprecated và loại bỏ. Xem
   :pep:`649` và :pep:`749`.


.. seealso::

   :ref:`future`
      Cách compiler xử lý các import future.

   :pep:`236` - Quay lại __future__
      Đề xuất ban đầu cho cơ chế __future__.
