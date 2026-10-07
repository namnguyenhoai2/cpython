.. highlight:: c

.. _reflection:

Phản chiếu
==========

.. c:function:: PyObject* PyEval_GetBuiltins(void)

   .. deprecated:: 3.13

      Thay vào đó, hãy sử dụng :c:func:`PyEval_GetFrameBuiltins`.

   Trả về một dictionary chứa các builtins trong khung thực thi hiện tại hoặc interpreter của trạng thái luồng nếu hiện không có khung nào đang được thực thi.


.. c:function:: PyObject* PyEval_GetLocals(void)

   .. deprecated:: 3.13

      Sử dụng :c:func:`PyEval_GetFrameLocals` để nhận được hành vi tương tự như khi gọi
      :func:`locals` trong mã Python, hoặc gọi :c:func:`PyFrame_GetLocals` trên kết quả của :c:func:`PyEval_GetFrame` để truy cập thuộc tính :attr:`~frame.f_locals` của khung hiện đang được thực thi.

   Trả về một mapping cho phép truy cập các biến cục bộ trong khung thực thi hiện tại hoặc ``NULL`` nếu hiện không có khung nào đang được thực thi.

   Tham khảo :func:`locals` để biết chi tiết về mapping được trả về ở các phạm vi khác nhau.

   Vì hàm này trả về một :term:`borrowed reference`, nên từ điển được trả về cho
   :term:`các phạm vi tối ưu hóa <optimized scope>` được lưu trong đối tượng frame và sẽ vẫn tồn tại chừng nào đối tượng frame còn tồn tại. Không giống như :c:func:`PyEval_GetFrameLocals` và
   :func:`locals`, các lần gọi tiếp theo đến hàm này trong cùng frame sẽ cập nhật nội dung của từ điển đã lưu trong bộ nhớ đệm để phản ánh các thay đổi về trạng thái của những biến cục bộ, thay vì trả về một ảnh chụp mới.

   .. versionchanged:: 3.13
      Trong :pep:`667`, :c:func:`PyFrame_GetLocals`, :func:`locals`, và
      :attr:`FrameType.f_locals <frame.f_locals>` không còn sử dụng từ điển bộ nhớ đệm dùng chung. Hãy tham khảo :ref:`mục What's New <whatsnew313-locals-semantics>` để biết thêm chi tiết.


.. c:function:: PyObject* PyEval_GetGlobals(void)

   .. deprecated:: 3.13

      Thay vào đó, hãy sử dụng :c:func:`PyEval_GetFrameGlobals`.

   Trả về một từ điển chứa các biến toàn cục trong frame thực thi hiện tại, hoặc ``NULL`` nếu hiện không có frame nào đang thực thi.


.. c:function:: PyFrameObject* PyEval_GetFrame(void)

   Trả về frame của :term:`attached thread state`, là ``NULL`` nếu hiện không có frame nào đang thực thi.

   Xem thêm :c:func:`PyThreadState_GetFrame`.


.. c:function:: PyObject* PyEval_GetFrameBuiltins(void)

   Trả về một dictionary chứa các builtins trong khung thực thi hiện tại hoặc interpreter của trạng thái luồng nếu hiện không có khung nào đang được thực thi.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyEval_GetFrameLocals(void)

   Trả về một dictionary chứa các biến cục bộ trong frame thực thi hiện tại, hoặc ``NULL`` nếu hiện không có frame nào đang thực thi. Tương đương với việc gọi
   :func:`locals` trong mã Python.

   Để truy cập :attr:`~frame.f_locals` trên frame hiện tại mà không tạo snapshot độc lập trong các scope được tối ưu hóa :term:`optimized scopes <optimized scope>`, hãy gọi :c:func:`PyFrame_GetLocals` trên kết quả của :c:func:`PyEval_GetFrame`.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyEval_GetFrameGlobals(void)

   Trả về một dictionary chứa các biến toàn cục trong frame thực thi hiện tại, hoặc ``NULL`` nếu hiện không có frame nào đang thực thi. Tương đương với việc gọi
   :func:`globals` trong mã Python.

   .. versionadded:: 3.13


.. c:function:: const char* PyEval_GetFuncName(PyObject *func)

   Trả về tên của *func* nếu đó là một đối tượng function, class hoặc instance; nếu không, trả về tên của *func*\s type.


.. c:function:: const char* PyEval_GetFuncDesc(PyObject *func)

   Trả về một chuỗi mô tả, tùy thuộc vào type của *func*. Các giá trị trả về bao gồm "()" cho function và method, " constructor", " instance" và " object". Khi được nối với kết quả của
   :c:func:`PyEval_GetFuncName`, kết quả sẽ là phần mô tả của *func*.
