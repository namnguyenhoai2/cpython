Đang chờ bị xóa trong các phiên bản tương lai
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các API sau đây không còn được khuyến nghị và sẽ bị xóa, mặc dù hiện chưa có ngày cụ thể nào được lên lịch cho việc xóa chúng.

* :c:macro:`Py_TPFLAGS_HAVE_FINALIZE`: Không cần thiết kể từ Python 3.8.
* :c:func:`PyErr_Fetch`: Thay vào đó, hãy sử dụng :c:func:`PyErr_GetRaisedException`.
* :c:func:`PyErr_NormalizeException`: Thay vào đó, hãy sử dụng :c:func:`PyErr_GetRaisedException`.
* :c:func:`PyErr_Restore`: Thay vào đó, hãy sử dụng :c:func:`PyErr_SetRaisedException`.
* :c:func:`PyModule_GetFilename`: Thay vào đó, hãy sử dụng :c:func:`PyModule_GetFilenameObject`.
* :c:func:`PyOS_AfterFork`: Thay vào đó, hãy sử dụng :c:func:`PyOS_AfterFork_Child`.
* :c:func:`PySlice_GetIndicesEx`: Thay vào đó, hãy sử dụng :c:func:`PySlice_Unpack` và :c:func:`PySlice_AdjustIndices`.
* :c:func:`PyUnicode_READY`: Không cần thiết kể từ Python 3.12
* :c:func:`!PyErr_Display`: Thay vào đó, hãy sử dụng :c:func:`PyErr_DisplayException`.
* :c:func:`!_PyErr_ChainExceptions`: Thay vào đó, hãy sử dụng :c:func:`!_PyErr_ChainExceptions1`.
* Thành viên :c:member:`!PyBytesObject.ob_shash`: thay vào đó, hãy gọi :c:func:`PyObject_Hash`.
* API Thread Local Storage (TLS):

  * :c:func:`PyThread_create_key`: Thay vào đó, hãy sử dụng :c:func:`PyThread_tss_alloc`.
  * :c:func:`PyThread_delete_key`: Thay vào đó, hãy sử dụng :c:func:`PyThread_tss_free`.
  * :c:func:`PyThread_set_key_value`: Thay vào đó, hãy sử dụng :c:func:`PyThread_tss_set`.
  * :c:func:`PyThread_get_key_value`: Thay vào đó, hãy sử dụng :c:func:`PyThread_tss_get`.
  * :c:func:`PyThread_delete_key_value`: Thay vào đó, hãy sử dụng :c:func:`PyThread_tss_delete`.
  * :c:func:`PyThread_ReInitTLS`: Không cần thiết kể từ Python 3.7.
