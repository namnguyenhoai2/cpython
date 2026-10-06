.. _audit-events:

.. index:: single: audit events

Bảng sự kiện audit
==================

Bảng này chứa tất cả các sự kiện được phát ra bởi :func:`sys.audit` hoặc
các lệnh gọi :c:func:`PySys_Audit` trong runtime CPython và thư viện chuẩn. Các lệnh gọi này được bổ sung từ phiên bản 3.8 trở lên (xem :pep:`578`).

Xem :func:`sys.addaudithook` và :c:func:`PySys_AddAuditHook` để biết thông tin về cách xử lý các sự kiện này.

.. impl-detail::

   Bảng này được tạo từ tài liệu CPython và có thể không thể hiện các sự kiện do những implementation khác phát ra. Hãy xem tài liệu dành riêng cho runtime của bạn để biết các sự kiện thực sự được phát ra.

.. audit-event-table::

Các sự kiện sau được phát ra bên trong và không tương ứng với bất kỳ public API nào của CPython:

+----------------------------+-------------------------------------------+
| Sự kiện audit              | Đối số                                    |
+============================+===========================================+
| _winapi.CreateFile         | ``file_name``, ``desired_access``,        |
|                            | ``share_mode``, ``creation_disposition``, |
|                            | ``flags_and_attributes``                  |
+----------------------------+-------------------------------------------+
| _winapi.CreateJunction     | ``src_path``, ``dst_path``                |
+----------------------------+-------------------------------------------+
| _winapi.CreateNamedPipe    | ``name``, ``open_mode``, ``pipe_mode``    |
+----------------------------+-------------------------------------------+
| _winapi.CreatePipe         |                                           |
+----------------------------+-------------------------------------------+
| _winapi.CreateProcess      | ``application_name``, ``command_line``,   |
|                            | ``current_directory``                     |
+----------------------------+-------------------------------------------+
| _winapi.OpenProcess        | ``process_id``, ``desired_access``        |
+----------------------------+-------------------------------------------+
| _winapi.TerminateProcess   | ``handle``, ``exit_code``                 |
+----------------------------+-------------------------------------------+
| _posixsubprocess.fork_exec | ``exec_list``, ``args``, ``env``          |
+----------------------------+-------------------------------------------+
| ctypes.PyObj_FromPtr       | ``obj``                                   |
+----------------------------+-------------------------------------------+

.. versionadded:: 3.14
   Sự kiện audit nội bộ ``_posixsubprocess.fork_exec``.
