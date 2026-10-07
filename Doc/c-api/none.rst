.. highlight:: c

.. _noneobject:

Đối tượng ``None``
------------------

.. index:: pair: object; None

Lưu ý rằng :c:type:`PyTypeObject` cho ``None`` không được cung cấp trực tiếp trong Python/C API. Vì ``None`` là một singleton, chỉ cần kiểm tra identity của đối tượng (sử dụng ``==`` trong C). Vì lý do tương tự, không có hàm :c:func:`!PyNone_Check`.


.. c:var:: PyObject* Py_None

   Đối tượng Python ``None``, biểu thị việc thiếu giá trị. Đối tượng này không có phương thức và là :term:`immortal`.

   .. versionchanged:: 3.12
      :c:data:`Py_None` is :term:`immortal`.

.. c:macro:: Py_RETURN_NONE

   Trả về :c:data:`Py_None` từ một hàm.
