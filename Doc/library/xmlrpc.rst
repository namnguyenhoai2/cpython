:mod:`!xmlrpc` --- các module server và client XMLRPC
=====================================================

.. module:: xmlrpc
   :synopsis: Các module server và client triển khai XML-RPC.

XML-RPC là một phương thức Remote Procedure Call sử dụng XML được truyền qua HTTP làm phương tiện truyền tải. Với phương thức này, client có thể gọi các method kèm tham số trên một server từ xa (server được xác định bằng một URI) và nhận lại dữ liệu có cấu trúc.

``xmlrpc`` là một package tập hợp các module server và client triển khai XML-RPC. Các module gồm:

* :mod:`xmlrpc.client`
* :mod:`xmlrpc.server`
