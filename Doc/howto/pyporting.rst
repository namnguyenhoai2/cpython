:orphan:

.. _pyporting-howto:

*************************************
Cách chuyển mã Python 2 sang Python 3
*************************************

:author: Brett Cannon

Python 2 đã chính thức kết thúc vòng đời vào đầu năm 2020. Điều này có nghĩa là sẽ không có báo cáo lỗi, bản sửa lỗi hoặc thay đổi mới nào được thực hiện cho Python 2 - Python 2 không còn được hỗ trợ: xem :pep:`373` và `trạng thái của các phiên bản Python <https://devguide.python.org/versions>`_.

Nếu bạn muốn chuyển một extension module thay vì mã Python thuần, hãy xem :ref:`cporting-howto`.

Danh sách gửi thư python-porting_ đã được lưu trữ có thể chứa một số hướng dẫn hữu ích.

Kể từ Python 3.11, hướng dẫn chuyển mã ban đầu đã ngừng được duy trì. Bạn có thể tìm hướng dẫn cũ trong `kho lưu trữ <https://docs.python.org/3.10/howto/pyporting.html>`_.


Các hướng dẫn của bên thứ ba
============================

Ngoài ra, còn có nhiều hướng dẫn của bên thứ ba có thể hữu ích:

- `Hướng dẫn của Fedora <https://portingguide.readthedocs.io>`_
- `Hướng dẫn PyCon 2020 <https://www.youtube.com/watch?v=JgIgEjASOlk>`_
- `Hướng dẫn của DigitalOcean <https://www.digitalocean.com/community/tutorials/how-to-port-python-2-code-to-python-3>`_
- `Hướng dẫn của ActiveState <https://www.activestate.com/blog/how-to-migrate-python-2-applications-to-python-3>`_


.. _python-porting: https://mail.python.org/pipermail/python-porting/

.. _`status of Python versions`: https://devguide.python.org/versions
.. _`archive`: https://docs.python.org/3.10/howto/pyporting.html
.. _`Guide by Fedora`: https://portingguide.readthedocs.io
.. _`PyCon 2020 tutorial`: https://www.youtube.com/watch?v=JgIgEjASOlk
.. _`Guide by DigitalOcean`: https://www.digitalocean.com/community/tutorials/how-to-port-python-2-code-to-python-3
.. _`Guide by ActiveState`: https://www.activestate.com/blog/how-to-migrate-python-2-applications-to-python-3
