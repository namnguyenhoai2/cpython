Dự kiến loại bỏ trong Python 3.18
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Các hàm private sau đây đã bị phản đối và dự kiến sẽ bị loại bỏ trong Python 3.18:

  * :c:func:`!_PyBytes_Join`: sử dụng :c:func:`PyBytes_Join`.
  * :c:func:`!_PyDict_GetItemStringWithError`: sử dụng :c:func:`PyDict_GetItemStringRef`.
  * :c:func:`!_PyDict_Pop()`: sử dụng :c:func:`PyDict_Pop`.
  * :c:func:`!_PyLong_Sign()`: sử dụng :c:func:`PyLong_GetSign`.
  * :c:func:`!_PyLong_FromDigits` và :c:func:`!_PyLong_New`: sử dụng :c:func:`PyLongWriter_Create`.
  * :c:func:`!_PyThreadState_UncheckedGet`: sử dụng :c:func:`PyThreadState_GetUnchecked`.
  * :c:func:`!_PyUnicode_AsString`: sử dụng :c:func:`PyUnicode_AsUTF8`.
  * :c:func:`!_PyUnicodeWriter_Init`: thay ``_PyUnicodeWriter_Init(&writer)`` bằng
    :c:func:`writer = PyUnicodeWriter_Create(0) <PyUnicodeWriter_Create>`.
  * :c:func:`!_PyUnicodeWriter_Finish`: thay ``_PyUnicodeWriter_Finish(&writer)`` bằng
    :c:func:`PyUnicodeWriter_Finish(writer) <PyUnicodeWriter_Finish>`.
  * :c:func:`!_PyUnicodeWriter_Dealloc`: thay ``_PyUnicodeWriter_Dealloc(&writer)`` bằng
    :c:func:`PyUnicodeWriter_Discard(writer) <PyUnicodeWriter_Discard>`.
  * :c:func:`!_PyUnicodeWriter_WriteChar`: thay thế ``_PyUnicodeWriter_WriteChar(&writer, ch)`` bằng
    :c:func:`PyUnicodeWriter_WriteChar(writer, ch) <PyUnicodeWriter_WriteChar>`.
  * :c:func:`!_PyUnicodeWriter_WriteStr`: thay thế ``_PyUnicodeWriter_WriteStr(&writer, str)`` bằng
    :c:func:`PyUnicodeWriter_WriteStr(writer, str) <PyUnicodeWriter_WriteStr>`.
  * :c:func:`!_PyUnicodeWriter_WriteSubstring`: thay thế ``_PyUnicodeWriter_WriteSubstring(&writer, str, start, end)`` bằng
    :c:func:`PyUnicodeWriter_WriteSubstring(writer, str, start, end) <PyUnicodeWriter_WriteSubstring>`.
  * :c:func:`!_PyUnicodeWriter_WriteASCIIString`: thay ``_PyUnicodeWriter_WriteASCIIString(&writer, str)`` bằng
    :c:func:`PyUnicodeWriter_WriteASCII(writer, str) <PyUnicodeWriter_WriteASCII>`.
  * :c:func:`!_PyUnicodeWriter_WriteLatin1String`: thay ``_PyUnicodeWriter_WriteLatin1String(&writer, str)`` bằng
    :c:func:`PyUnicodeWriter_WriteUTF8(writer, str) <PyUnicodeWriter_WriteUTF8>`.
  * :c:func:`!_PyUnicodeWriter_Prepare`: (không có cách thay thế).
  * :c:func:`!_PyUnicodeWriter_PrepareKind`: (không có cách thay thế).
  * :c:func:`!_Py_HashPointer`: sử dụng :c:func:`Py_HashPointer`.
  * :c:func:`!_Py_fopen_obj`: sử dụng :c:func:`Py_fopen`.

  Có thể sử dụng `dự án pythoncapi-compat <https://github.com/python/pythoncapi-compat/>`__ để có được các hàm public mới này trên Python 3.13 trở về trước. (Do Victor Stinner đóng góp trong :gh:`128863`.)
