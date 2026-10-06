:mod:`!copyreg` --- Đăng ký các hàm hỗ trợ :mod:`!pickle`
=========================================================

.. module:: copyreg
   :synopsis: Đăng ký các hàm hỗ trợ pickle.

**Mã nguồn:** :source:`Lib/copyreg.py`

.. index::
   pair: module; pickle
   pair: module; copy

--------------

Module :mod:`!copyreg` cung cấp cách định nghĩa các hàm được sử dụng khi pickling các đối tượng cụ thể. Các module :mod:`pickle` và :mod:`copy` sử dụng những hàm đó khi pickling/sao chép các đối tượng này. Module này cung cấp thông tin cấu hình về các hàm khởi tạo đối tượng không phải là class. Những hàm khởi tạo như vậy có thể là các hàm factory hoặc các thực thể của class.


.. function:: constructor(object)

   Khai báo *object* là một hàm khởi tạo hợp lệ. Nếu *object* không thể gọi được (và do đó không hợp lệ để làm hàm khởi tạo), sẽ phát sinh :exc:`TypeError`.


.. function:: pickle(type, function, constructor_ob=None)

   Khai báo rằng *function* nên được sử dụng làm hàm "reduction" cho các đối tượng thuộc kiểu *type*. *function* phải trả về một chuỗi hoặc một tuple chứa từ hai đến sáu phần tử. Xem :attr:`~pickle.Pickler.dispatch_table` để biết thêm chi tiết về giao diện của *function*.

   Tham số *constructor_ob* là một tính năng cũ và hiện bị bỏ qua, nhưng nếu được truyền vào thì phải là một đối tượng có thể gọi.

   Lưu ý rằng thuộc tính :attr:`~pickle.Pickler.dispatch_table` của một đối tượng pickler hoặc lớp con của :class:`pickle.Pickler` cũng có thể được dùng để khai báo các hàm reduction.

Ví dụ
-----

Ví dụ dưới đây minh họa cách đăng ký một hàm pickle và cách hàm đó được sử dụng:

   >>> import copyreg, copy, pickle
   >>> class C:
   ...     def __init__(self, a):
   ...         self.a = a
   ...
   >>> def pickle_c(c):
   ...     print("pickling a C instance...")
   ...     return C, (c.a,)
   ...
   >>> copyreg.pickle(C, pickle_c)
   >>> c = C(1)
   >>> d = copy.copy(c)  # doctest: +SKIP
   pickling a C instance...
   >>> p = pickle.dumps(c)  # doctest: +SKIP
   pickling a C instance...
