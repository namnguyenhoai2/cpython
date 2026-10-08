:mod:`!winreg` --- truy cập registry Windows
============================================

.. module:: winreg
   :synopsis: Các routine và đối tượng để thao tác với registry Windows.

.. sectionauthor:: Mark Hammond <MarkH@ActiveState.com>

--------------

Các hàm này cung cấp API registry Windows cho Python. Thay vì sử dụng một số nguyên làm handle registry, một :ref:`đối tượng handle <handle-object>` được sử dụng để đảm bảo các handle được đóng đúng cách, ngay cả khi lập trình viên quên đóng chúng một cách rõ ràng.

.. availability:: Windows.

.. _exception-changed:

.. versionchanged:: 3.3
   Trước đây, một số hàm trong module này sẽ phát sinh một
   :exc:`WindowsError`, hiện là bí danh của :exc:`OSError`.

.. _functions:

Các hàm
-------

Module này cung cấp các hàm sau:


.. function:: CloseKey(hkey)

   Đóng một registry key đã được mở trước đó. Đối số *hkey* chỉ định một key đã được mở trước đó.

   .. note::

      Nếu *hkey* không được đóng bằng phương thức này (hoặc thông qua :meth:`hkey.Close() <PyHKEY.Close>`), nó sẽ được đóng khi đối tượng *hkey* bị Python hủy.


.. function:: ConnectRegistry(computer_name, key)

   Thiết lập kết nối đến một registry handle được định nghĩa trước trên máy tính khác và trả về một :ref:`handle object <handle-object>`.

   *computer_name* là tên của máy tính từ xa, có dạng ``r"\\computername"``. Nếu ``None``, máy tính cục bộ sẽ được sử dụng.

   *key* là handle được định nghĩa trước cần kết nối.

   Giá trị trả về là handle của key đã mở. Nếu hàm thất bại, một
   :exc:`OSError` ngoại lệ sẽ được phát sinh.

   .. audit-event:: winreg.ConnectRegistry computer_name,key winreg.ConnectRegistry

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: CreateKey(key, sub_key)

   Tạo hoặc mở khóa được chỉ định, trả về một
   :ref:`đối tượng handle <handle-object>`.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi xác định tên khóa mà phương thức này mở hoặc tạo.

   Nếu *key* là một trong các khóa được định nghĩa sẵn, *sub_key* có thể là ``None``. Trong trường hợp đó, handle được trả về chính là handle của khóa được truyền vào hàm.

   Nếu khóa đã tồn tại, hàm này sẽ mở khóa hiện có.

   Giá trị trả về là handle của key đã mở. Nếu hàm thất bại, một
   :exc:`OSError` ngoại lệ sẽ được phát sinh.

   .. audit-event:: winreg.CreateKey key,sub_key,access winreg.CreateKey

   .. audit-event:: winreg.OpenKey/result key winreg.CreateKey

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: CreateKeyEx(key, sub_key, reserved=0, access=KEY_WRITE)

   Tạo hoặc mở khóa được chỉ định, trả về một
   :ref:`đối tượng handle <handle-object>`.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi xác định tên khóa mà phương thức này mở hoặc tạo.

   *reserved* là một số nguyên dành riêng và phải bằng không. Giá trị mặc định là không.

   *access* là một số nguyên chỉ định access mask mô tả quyền truy cập bảo mật mong muốn cho key. Giá trị mặc định là :const:`KEY_WRITE`. Xem
   :ref:`Access Rights <access-rights>` để biết các giá trị được phép khác.

   Nếu *key* là một trong các khóa được định nghĩa sẵn, *sub_key* có thể là ``None``. Trong trường hợp đó, handle được trả về chính là handle của khóa được truyền vào hàm.

   Nếu khóa đã tồn tại, hàm này sẽ mở khóa hiện có.

   Giá trị trả về là handle của key đã mở. Nếu hàm thất bại, một
   :exc:`OSError` ngoại lệ sẽ được phát sinh.

   .. audit-event:: winreg.CreateKey key,sub_key,access winreg.CreateKeyEx

   .. audit-event:: winreg.OpenKey/result key winreg.CreateKeyEx

   .. versionadded:: 3.2

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: DeleteKey(key, sub_key)

   Xóa khóa được chỉ định.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi phải là khóa con của khóa được xác định bởi tham số *key*. Giá trị này không được là ``None``, và khóa không được có khóa con.

   *Phương thức này không thể xóa các key có subkey.*

   Nếu phương thức thành công, toàn bộ key, bao gồm tất cả các giá trị của nó, sẽ bị xóa. Nếu phương thức không thành công, một :exc:`OSError` exception sẽ được raised.

   .. audit-event:: winreg.DeleteKey key,sub_key,access winreg.DeleteKey

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: DeleteKeyEx(key, sub_key, access=KEY_WOW64_64KEY, reserved=0)

   Xóa khóa được chỉ định.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi phải là subkey của key được xác định bởi tham số *key*. Giá trị này không được là ``None``, và key không được có subkey.

   *reserved* là một số nguyên dành riêng và phải bằng không. Giá trị mặc định là không.

   *access* là một số nguyên chỉ định access mask mô tả quyền truy cập bảo mật mong muốn cho key. Giá trị mặc định là :const:`KEY_WOW64_64KEY`. Trên Windows 32-bit, các hằng số WOW64 bị bỏ qua. Xem :ref:`Access Rights <access-rights>` để biết các giá trị được phép khác.

   *Phương thức này không thể xóa các key có subkey.*

   Nếu phương thức thành công, toàn bộ key, bao gồm tất cả các giá trị của nó, sẽ bị xóa. Nếu phương thức không thành công, một :exc:`OSError` exception sẽ được raised.

   Trên các phiên bản Windows không được hỗ trợ, :exc:`NotImplementedError` sẽ được raised.

   .. audit-event:: winreg.DeleteKey key,sub_key,access winreg.DeleteKeyEx

   .. versionadded:: 3.2

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: DeleteValue(key, value)

   Xóa một giá trị có tên khỏi registry key.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *value* là một chuỗi xác định value cần xóa.

   .. audit-event:: winreg.DeleteValue key,value winreg.DeleteValue


.. function:: EnumKey(key, index)

   Liệt kê các khóa con của một khóa registry đang mở và trả về một chuỗi.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *index* là một số nguyên xác định chỉ mục của khóa cần truy xuất.

   Hàm này lấy tên của một subkey mỗi khi được gọi. Thông thường, hàm được gọi lặp lại cho đến khi phát sinh ngoại lệ :exc:`OSError`, cho biết không còn giá trị nào nữa.

   .. audit-event:: winreg.EnumKey key,index winreg.EnumKey

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: EnumValue(key, index)

   Liệt kê các giá trị của một registry key đang mở và trả về một tuple.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *index* là một số nguyên xác định chỉ mục của giá trị cần lấy.

   Hàm này lấy tên của một subkey mỗi khi được gọi. Thông thường, hàm được gọi lặp lại cho đến khi phát sinh ngoại lệ :exc:`OSError`, cho biết không còn giá trị nào nữa.

   Kết quả là một tuple gồm 3 mục:

   +---------+----------------------------------------------------------------------------------+
   | Chỉ mục | Ý nghĩa                                                                          |
   +=========+==================================================================================+
   | ``0``   | Một chuỗi xác định tên giá trị                                                   |
   +---------+----------------------------------------------------------------------------------+
   | ``1``   | Một đối tượng chứa dữ liệu giá trị và có kiểu phụ thuộc vào kiểu registry cơ bản |
   +---------+----------------------------------------------------------------------------------+
   | ``2``   | Một số nguyên xác định kiểu của dữ liệu giá trị (xem bảng trong tài liệu về      |
   |         | :meth:`SetValueEx`)                                                              |
   +---------+----------------------------------------------------------------------------------+

   .. audit-event:: winreg.EnumValue key,index winreg.EnumValue

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. index::
   single: % (percent); environment variables expansion (Windows)

.. function:: ExpandEnvironmentStrings(str)

   Mở rộng các placeholder của biến môi trường ``%NAME%`` trong các chuỗi như
   :const:`REG_EXPAND_SZ`::

      >>> ExpandEnvironmentStrings('%windir%')
      'C:\\Windows'

   .. audit-event:: winreg.ExpandEnvironmentStrings str winreg.ExpandEnvironmentStrings


.. function:: FlushKey(key)

   Ghi tất cả các thuộc tính của một key vào registry.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   Không cần gọi :func:`FlushKey` để thay đổi một key. Các thay đổi trong registry được registry ghi xuống đĩa bằng lazy flusher của nó. Các thay đổi trong registry cũng được ghi xuống đĩa khi hệ thống tắt. Không giống như :func:`CloseKey`,
   phương thức :func:`FlushKey` chỉ trả về khi toàn bộ dữ liệu đã được ghi vào registry. Ứng dụng chỉ nên gọi :func:`FlushKey` nếu cần sự chắc chắn tuyệt đối rằng các thay đổi trong registry đã được ghi xuống đĩa.

   .. note::

      Nếu bạn không biết liệu có cần gọi :func:`FlushKey` hay không thì có lẽ là không cần.


.. function:: LoadKey(key, sub_key, file_name)

   Tạo một khóa con bên dưới khóa được chỉ định và lưu thông tin đăng ký từ một tệp được chỉ định vào khóa con đó.

   *key* là một handle được trả về bởi :func:`ConnectRegistry` hoặc một trong các hằng số
   :const:`HKEY_USERS` hoặc :const:`HKEY_LOCAL_MACHINE`.

   *sub_key* là một chuỗi xác định khóa con cần tải.

   *file_name* là tên của tệp dùng để tải dữ liệu registry. Tệp này phải được tạo bằng hàm :func:`SaveKey`. Trong hệ thống tệp file allocation table (FAT), tên tệp có thể không có phần mở rộng.

   Lệnh gọi đến :func:`LoadKey` sẽ thất bại nếu tiến trình gọi không có
   :c:data:`!SE_RESTORE_PRIVILEGE` đặc quyền.  Lưu ý rằng đặc quyền khác với quyền truy cập -- xem `tài liệu về RegLoadKey <https://msdn.microsoft.com/en-us/library/ms724889%28v=VS.85%29.aspx>`__ để biết thêm chi tiết.

   Nếu *key* là một handle được trả về bởi :func:`ConnectRegistry`, thì đường dẫn được chỉ định trong *file_name* là đường dẫn tương đối so với máy tính từ xa.

   .. audit-event:: winreg.LoadKey key,sub_key,file_name winreg.LoadKey


.. function:: OpenKey(key, sub_key, reserved=0, access=KEY_READ)
              OpenKeyEx(key, sub_key, reserved=0, access=KEY_READ)

   Mở key được chỉ định và trả về một :ref:`handle object <handle-object>`.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi xác định sub_key cần mở.

   *reserved* là một số nguyên dành riêng và phải bằng không. Giá trị mặc định là không.

   *access* là một số nguyên chỉ định access mask mô tả quyền truy cập bảo mật mong muốn cho key. Giá trị mặc định là :const:`KEY_READ`. Xem :ref:`Quyền truy cập <access-rights>` để biết các giá trị được phép khác.

   Kết quả là một handle mới đến key được chỉ định.

   Nếu hàm không thành công, :exc:`OSError` sẽ được raise.

   .. audit-event:: winreg.OpenKey key,sub_key,access winreg.OpenKey

   .. audit-event:: winreg.OpenKey/result key winreg.OpenKey

   .. versionchanged:: 3.2
      Cho phép sử dụng các đối số có tên.

   .. versionchanged:: 3.3
      Xem :ref:`ở trên <exception-changed>`.


.. function:: QueryInfoKey(key)

   Trả về thông tin về một key dưới dạng tuple.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   Kết quả là một tuple gồm 3 mục:

   +---------+-----------------------------------------------------------------------------------------------------------------------------------------+
   | Chỉ mục | Ý nghĩa                                                                                                                                 |
   +=========+=========================================================================================================================================+
   | ``0``   | Một số nguyên cho biết số lượng khóa con mà khóa này có.                                                                                |
   +---------+-----------------------------------------------------------------------------------------------------------------------------------------+
   | ``1``   | Một số nguyên cho biết số lượng giá trị mà khóa này có.                                                                                 |
   +---------+-----------------------------------------------------------------------------------------------------------------------------------------+
   | ``2``   | Một số nguyên cho biết thời điểm khóa được sửa đổi lần cuối (nếu có), tính bằng các khoảng 100 nano giây kể từ ngày 1 tháng 1 năm 1601. |
   +---------+-----------------------------------------------------------------------------------------------------------------------------------------+

   .. audit-event:: winreg.QueryInfoKey key winreg.QueryInfoKey


.. function:: QueryValue(key, sub_key)

   Truy xuất giá trị không có tên của một key dưới dạng chuỗi.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi chứa tên của subkey mà giá trị được liên kết với nó. Nếu tham số này là ``None`` hoặc rỗng, hàm sẽ truy xuất giá trị được đặt bởi phương thức :func:`SetValue` cho key được xác định bởi *key*.

   Các giá trị trong registry có các thành phần tên, kiểu và dữ liệu. Phương thức này truy xuất dữ liệu của giá trị đầu tiên của một key có ``NULL`` name. Tuy nhiên, lệnh gọi API bên dưới không trả về kiểu, vì vậy hãy luôn sử dụng
   :func:`QueryValueEx` nếu có thể.

   .. audit-event:: winreg.QueryValue key,sub_key,value_name winreg.QueryValue


.. function:: QueryValueEx(key, value_name)

   Truy xuất kiểu và dữ liệu của một tên giá trị được chỉ định liên kết với một registry key đang mở.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *value_name* là một chuỗi cho biết giá trị cần truy vấn.

   Kết quả là một tuple gồm 2 mục:

   +---------+---------------------------------------------------------------------------------------+
   | Chỉ mục | Ý nghĩa                                                                               |
   +=========+=======================================================================================+
   | ``0``   | Giá trị của mục trong registry.                                                       |
   +---------+---------------------------------------------------------------------------------------+
   | ``1``   | Một số nguyên cho biết kiểu registry của giá trị này (xem bảng trong tài liệu để biết |
   |         | :meth:`SetValueEx`)                                                                   |
   +---------+---------------------------------------------------------------------------------------+

   .. audit-event:: winreg.QueryValue key,sub_key,value_name winreg.QueryValueEx


.. function:: SaveKey(key, file_name)

   Lưu key được chỉ định cùng tất cả subkey của nó vào file được chỉ định.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *file_name* là tên của file dùng để lưu dữ liệu registry. File này không được tồn tại trước đó. Nếu tên file này có phần mở rộng, không thể sử dụng tên file đó trên các hệ thống file allocation table (FAT) bằng phương thức :meth:`LoadKey`.

   Nếu *key* đại diện cho một key trên máy tính từ xa, đường dẫn được mô tả bởi *file_name* là đường dẫn tương đối với máy tính từ xa. Caller của phương thức này phải có đặc quyền bảo mật **SeBackupPrivilege**. Lưu ý rằng đặc quyền khác với quyền truy cập — xem `Conflicts Between User Rights and Permissions documentation <https://msdn.microsoft.com/en-us/library/ms724878%28v=VS.85%29.aspx>`__ để biết thêm chi tiết.

   Hàm này truyền ``NULL`` cho *security_attributes* đến API.

   .. audit-event:: winreg.SaveKey key,file_name winreg.SaveKey


.. function:: SetValue(key, sub_key, type, value)

   Liên kết một giá trị với một khóa được chỉ định.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *sub_key* là một chuỗi đặt tên cho khóa phụ mà giá trị được liên kết với.

   *type* là một số nguyên chỉ định kiểu dữ liệu. Hiện tại, giá trị này phải là
   :const:`REG_SZ`, nghĩa là chỉ các chuỗi được hỗ trợ. Sử dụng hàm :func:`SetValueEx` để hỗ trợ các kiểu dữ liệu khác.

   *value* là một chuỗi chỉ định giá trị mới.

   Nếu khóa được chỉ định bởi tham số *sub_key* không tồn tại, hàm SetValue sẽ tạo khóa đó.

   Độ dài giá trị bị giới hạn bởi bộ nhớ khả dụng. Các giá trị dài (hơn 2048 byte) nên được lưu dưới dạng tệp, với tên tệp được lưu trong registry cấu hình. Điều này giúp registry hoạt động hiệu quả.

   Khóa được xác định bởi tham số *key* phải được mở với
   :const:`KEY_SET_VALUE` quyền truy cập.

   .. audit-event:: winreg.SetValue key,sub_key,type,value winreg.SetValue


.. function:: SetValueEx(key, value_name, reserved, type, value)

   Lưu dữ liệu vào trường giá trị của một khóa registry đang mở.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   *value_name* là một chuỗi đặt tên cho khóa con mà giá trị được liên kết với.

   *reserved* có thể là bất kỳ giá trị nào -- API luôn truyền giá trị bằng không.

   *type* là một số nguyên chỉ định kiểu dữ liệu. Xem
   :ref:`Value Types <value-types>` để biết các kiểu khả dụng.

   *value* là một chuỗi chỉ định giá trị mới.

   Phương thức này cũng có thể đặt thông tin bổ sung về giá trị và kiểu cho khóa được chỉ định. Khóa được xác định bởi tham số key phải được mở bằng
   :const:`KEY_SET_VALUE` quyền truy cập.

   Để mở khóa, hãy sử dụng phương thức :func:`CreateKey` hoặc :func:`OpenKey`.

   Độ dài giá trị bị giới hạn bởi bộ nhớ khả dụng. Các giá trị dài (hơn 2048 byte) nên được lưu dưới dạng tệp, với tên tệp được lưu trong registry cấu hình. Điều này giúp registry hoạt động hiệu quả.

   .. audit-event:: winreg.SetValue key,sub_key,type,value winreg.SetValueEx


.. function:: DisableReflectionKey(key)

   Vô hiệu hóa tính năng phản chiếu registry đối với các tiến trình 32-bit chạy trên hệ điều hành 64-bit.

   *key* là một khóa đã được mở hoặc một trong các hằng số :ref:`HKEY_* constants <hkey-constants>` được định nghĩa sẵn.

   Thông thường sẽ gây ra :exc:`NotImplementedError` nếu được thực thi trên hệ điều hành 32-bit.

   Nếu khóa không nằm trong danh sách phản chiếu, hàm sẽ thực hiện thành công nhưng không có tác dụng. Việc vô hiệu hóa tính năng phản chiếu đối với một khóa không ảnh hưởng đến tính năng phản chiếu của bất kỳ khóa con nào.

   .. audit-event:: winreg.DisableReflectionKey key winreg.DisableReflectionKey


.. function:: EnableReflectionKey(key)

   Khôi phục tính năng phản chiếu registry cho khóa đã bị vô hiệu hóa được chỉ định.

   *key* là một khóa đã được mở hoặc một trong các hằng số :ref:`HKEY_* constants <hkey-constants>` được định nghĩa sẵn.

   Thông thường sẽ gây ra :exc:`NotImplementedError` nếu được thực thi trên hệ điều hành 32-bit.

   Việc khôi phục reflection cho một khóa không ảnh hưởng đến reflection của bất kỳ khóa con nào.

   .. audit-event:: winreg.EnableReflectionKey key winreg.EnableReflectionKey


.. function:: QueryReflectionKey(key)

   Xác định trạng thái reflection của khóa được chỉ định.

   *key* là một khóa đã được mở, hoặc một trong các
   :ref:`HKEY_* hằng số <hkey-constants>` được định nghĩa sẵn.

   Trả về ``True`` nếu reflection bị tắt.

   Thông thường sẽ gây ra :exc:`NotImplementedError` nếu được thực thi trên hệ điều hành 32-bit.

   .. audit-event:: winreg.QueryReflectionKey key winreg.QueryReflectionKey


.. _constants:

Hằng số
-------

Các hằng số sau đây được định nghĩa để sử dụng trong nhiều hàm :mod:`!winreg`.

.. _hkey-constants:

HKEY_* Hằng số
++++++++++++++

.. data:: HKEY_CLASSES_ROOT

   Các mục đăng ký bên dưới khóa này xác định các loại (hoặc lớp) tài liệu và các thuộc tính liên kết với những loại đó. Các ứng dụng Shell và COM sử dụng thông tin được lưu trữ dưới khóa này.


.. data:: HKEY_CURRENT_USER

   Các mục đăng ký bên dưới khóa này xác định tùy chọn của người dùng hiện tại. Những tùy chọn này bao gồm các thiết đặt của biến môi trường, dữ liệu về nhóm chương trình, màu sắc, máy in, kết nối mạng và tùy chọn ứng dụng.

.. data:: HKEY_LOCAL_MACHINE

   Các mục đăng ký bên dưới khóa này xác định trạng thái vật lý của máy tính, bao gồm dữ liệu về loại bus, bộ nhớ hệ thống và phần cứng, phần mềm đã cài đặt.

.. data:: HKEY_USERS

   Các mục Registry cấp dưới khóa này xác định cấu hình người dùng mặc định cho người dùng mới trên máy tính cục bộ và cấu hình người dùng cho người dùng hiện tại.

.. data:: HKEY_PERFORMANCE_DATA

   Các mục Registry cấp dưới khóa này cho phép bạn truy cập dữ liệu hiệu suất. Dữ liệu không thực sự được lưu trữ trong Registry; các hàm Registry khiến hệ thống thu thập dữ liệu từ nguồn của nó.


.. data:: HKEY_CURRENT_CONFIG

   Chứa thông tin về hồ sơ phần cứng hiện tại của hệ thống máy tính cục bộ.

.. data:: HKEY_DYN_DATA

   Khóa này không được sử dụng trong các phiên bản Windows sau Windows 98.


.. _access-rights:

Quyền truy cập
++++++++++++++

Để biết thêm thông tin, hãy xem `Bảo mật và quyền truy cập khóa Registry <https://msdn.microsoft.com/en-us/library/ms724878%28v=VS.85%29.aspx>`__.

.. data:: KEY_ALL_ACCESS

   Kết hợp STANDARD_RIGHTS_REQUIRED, :const:`KEY_QUERY_VALUE`,
   :const:`KEY_SET_VALUE`, :const:`KEY_CREATE_SUB_KEY`,
   quyền truy cập :const:`KEY_ENUMERATE_SUB_KEYS`, :const:`KEY_NOTIFY` và :const:`KEY_CREATE_LINK`.

.. data:: KEY_WRITE

   Kết hợp STANDARD_RIGHTS_WRITE, :const:`KEY_SET_VALUE` và
   quyền truy cập :const:`KEY_CREATE_SUB_KEY`.

.. data:: KEY_READ

   Kết hợp STANDARD_RIGHTS_READ, :const:`KEY_QUERY_VALUE`,
   các giá trị :const:`KEY_ENUMERATE_SUB_KEYS` và :const:`KEY_NOTIFY`.

.. data:: KEY_EXECUTE

   Tương đương với :const:`KEY_READ`.

.. data:: KEY_QUERY_VALUE

   Bắt buộc để truy vấn các giá trị của khóa registry.

.. data:: KEY_SET_VALUE

   Cần có để tạo, xóa hoặc đặt giá trị registry.

.. data:: KEY_CREATE_SUB_KEY

   Cần có để tạo khóa con của một khóa registry.

.. data:: KEY_ENUMERATE_SUB_KEYS

   Cần có để liệt kê các khóa con của một khóa registry.

.. data:: KEY_NOTIFY

   Cần có để yêu cầu thông báo thay đổi cho một khóa registry hoặc các khóa con của một khóa registry.

.. data:: KEY_CREATE_LINK

   Dành riêng cho hệ thống.


.. _64-bit-access-rights:

Dành riêng cho 64-bit
*********************

Để biết thêm thông tin, hãy xem `Truy cập chế độ xem registry thay thế <https://msdn.microsoft.com/en-us/library/aa384129(v=VS.85).aspx>`__.

.. data:: KEY_WOW64_64KEY

   Cho biết ứng dụng trên Windows 64-bit nên hoạt động trên chế độ xem registry 64-bit. Trên Windows 32-bit, hằng số này bị bỏ qua.

.. data:: KEY_WOW64_32KEY

   Cho biết ứng dụng trên Windows 64-bit nên hoạt động trên chế độ xem registry 32-bit. Trên Windows 32-bit, hằng số này bị bỏ qua.

.. _value-types:

Các loại giá trị
++++++++++++++++

Để biết thêm thông tin, hãy xem `Các loại giá trị Registry <https://msdn.microsoft.com/en-us/library/ms724884%28v=VS.85%29.aspx>`__.

.. data:: REG_BINARY

   Dữ liệu nhị phân dưới mọi dạng.

.. data:: REG_DWORD

   Số 32-bit.

.. data:: REG_DWORD_LITTLE_ENDIAN

   Số 32-bit ở định dạng little-endian. Tương đương với :const:`REG_DWORD`.

.. data:: REG_DWORD_BIG_ENDIAN

   Một số 32-bit ở định dạng big-endian.

.. data:: REG_EXPAND_SZ

   Chuỗi kết thúc bằng null chứa các tham chiếu đến biến môi trường (``%PATH%``).

.. data:: REG_LINK

   Một symbolic link Unicode.

.. data:: REG_MULTI_SZ

   Một dãy các chuỗi kết thúc bằng null, được kết thúc bởi hai ký tự null. (Python tự động xử lý việc kết thúc này.)

.. data:: REG_NONE

   Không có kiểu giá trị được xác định.

.. data:: REG_QWORD

   Một số 64-bit.

   .. versionadded:: 3.6

.. data:: REG_QWORD_LITTLE_ENDIAN

   Một số 64-bit ở định dạng little-endian. Tương đương với :const:`REG_QWORD`.

   .. versionadded:: 3.6

.. data:: REG_RESOURCE_LIST

   Danh sách tài nguyên của trình điều khiển thiết bị.

.. data:: REG_FULL_RESOURCE_DESCRIPTOR

   Thiết lập phần cứng.

.. data:: REG_RESOURCE_REQUIREMENTS_LIST

   Danh sách tài nguyên phần cứng.

.. data:: REG_SZ

   Chuỗi kết thúc bằng null.


.. _handle-object:

Đối tượng handle Registry
-------------------------

Đối tượng này bao bọc một đối tượng Windows HKEY và tự động đóng đối tượng đó khi đối tượng này bị hủy. Để đảm bảo dọn dẹp, bạn có thể gọi một trong hai
phương thức :meth:`~PyHKEY.Close` trên đối tượng hoặc hàm :func:`CloseKey`.

Tất cả các hàm registry trong mô-đun này đều trả về một trong các đối tượng này.

Tất cả các hàm registry trong mô-đun này chấp nhận đối tượng handle cũng chấp nhận một số nguyên; tuy nhiên, nên sử dụng đối tượng handle.

Các đối tượng handle cung cấp ngữ nghĩa cho :meth:`~object.__bool__` -- do đó::

   if handle:
       print("Yes")

sẽ in ``Yes`` nếu handle hiện hợp lệ (chưa bị đóng hoặc tách rời).

Các đối tượng handle có thể được chuyển đổi thành số nguyên (ví dụ: bằng cách sử dụng hàm dựng sẵn
:func:`int`), trong trường hợp đó, giá trị handle Windows bên dưới sẽ được trả về. Bạn cũng có thể sử dụng phương thức :meth:`~PyHKEY.Detach` để trả về handle dạng số nguyên, đồng thời ngắt kết nối handle Windows khỏi đối tượng handle.


.. method:: PyHKEY.Close()

   Đóng handle Windows bên dưới.

   Nếu handle đã được đóng, sẽ không phát sinh lỗi.


.. method:: PyHKEY.Detach()

   Tách Windows handle khỏi đối tượng handle.

   Kết quả là một số nguyên chứa giá trị của handle trước khi được tách. Nếu handle đã được tách hoặc đóng, hàm này sẽ trả về số 0.

   Sau khi gọi hàm này, handle về cơ bản đã bị vô hiệu hóa, nhưng chưa được đóng. Bạn sẽ gọi hàm này khi cần underlying Win32 handle tiếp tục tồn tại sau vòng đời của đối tượng handle.

   .. audit-event:: winreg.PyHKEY.Detach key winreg.PyHKEY.Detach


.. method:: PyHKEY.__enter__()
            PyHKEY.__exit__(*exc_info)

   Đối tượng HKEY triển khai :meth:`~object.__enter__` và
   :meth:`~object.__exit__` và do đó hỗ trợ context protocol cho
   :keyword:`with` câu lệnh::

      with OpenKey(HKEY_LOCAL_MACHINE, "foo") as key:
          ...  # làm việc với key

   sẽ tự động đóng *key* khi control rời khỏi khối :keyword:`with`.


