.. highlight:: c

.. _cell-objects:

Đối tượng Cell
--------------

Các đối tượng "Cell" được dùng để triển khai các biến được tham chiếu bởi nhiều scope. Với mỗi biến như vậy, một đối tượng cell được tạo để lưu trữ giá trị; các biến cục bộ của mỗi stack frame tham chiếu đến giá trị này chứa một tham chiếu đến các cell từ những scope bên ngoài cũng sử dụng biến đó. Khi giá trị được truy cập, giá trị chứa trong cell được sử dụng thay vì chính đối tượng cell. Việc bỏ tham chiếu (de-reference) đối tượng cell này cần có sự hỗ trợ từ byte-code được sinh ra; các đối tượng này không tự động được bỏ tham chiếu khi được truy cập. Các đối tượng cell có lẽ không hữu ích ở nơi khác.


.. c:type:: PyCellObject

   Cấu trúc C được sử dụng cho các đối tượng cell.


.. c:var:: PyTypeObject PyCell_Type

   Đối tượng kiểu tương ứng với các đối tượng cell.


.. c:function:: int PyCell_Check(PyObject *ob)

   Trả về true nếu *ob* là một đối tượng cell; *ob* không được là ``NULL``. Hàm này luôn thành công.


.. c:function:: PyObject* PyCell_New(PyObject *ob)

   Tạo và trả về một đối tượng cell mới chứa giá trị *ob*. Tham số này có thể là ``NULL``.


.. c:function:: PyObject* PyCell_Get(PyObject *cell)

   Trả về nội dung của cell *cell*, có thể là ``NULL``. Nếu *cell* không phải là một đối tượng cell, trả về ``NULL`` và đặt exception.


.. c:function:: PyObject* PyCell_GET(PyObject *cell)

   Trả về nội dung của ô *cell*, nhưng không kiểm tra xem *cell* có khác ``NULL`` và là một đối tượng cell hay không.


.. c:function:: int PyCell_Set(PyObject *cell, PyObject *value)

   Đặt nội dung của đối tượng cell *cell* thành *value*.  Thao tác này giải phóng tham chiếu đến mọi nội dung hiện tại của ô. *value* có thể là ``NULL``.  *cell* phải khác ``NULL``.

   Nếu thành công, trả về ``0``. Nếu *cell* không phải là một đối tượng cell, đặt một exception và trả về ``-1``.


.. c:function:: void PyCell_SET(PyObject *cell, PyObject *value)

   Đặt giá trị của đối tượng cell *cell* thành *value*.  Không điều chỉnh reference count và không thực hiện kiểm tra an toàn; *cell* phải khác ``NULL`` và phải là một đối tượng cell.
