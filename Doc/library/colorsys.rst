:mod:`!colorsys` --- Chuyển đổi giữa các hệ màu
===============================================

.. module:: colorsys
   :synopsis: Các hàm chuyển đổi giữa RGB và các hệ màu khác.

.. sectionauthor:: David Ascher <da@python.net>

**Mã nguồn:** :source:`Lib/colorsys.py`

--------------

Mô-đun :mod:`!colorsys` xác định các phép chuyển đổi hai chiều của các giá trị màu giữa màu được biểu diễn trong không gian màu RGB (Đỏ Lục Lam) được màn hình máy tính sử dụng và ba hệ tọa độ khác: YIQ, HLS (Sắc độ Độ sáng Độ bão hòa) và HSV (Sắc độ Độ bão hòa Giá trị). Tọa độ trong tất cả các không gian màu này đều là các giá trị dấu phẩy động. Trong không gian YIQ, tọa độ Y nằm trong khoảng từ 0 đến 1, nhưng các tọa độ I và Q có thể dương hoặc âm. Trong tất cả các không gian khác, mọi tọa độ đều nằm trong khoảng từ 0 đến 1.

.. seealso::

   Có thể tìm thêm thông tin về các không gian màu tại https://www.poynton.ca/pdf/ColourFAQ.pdf và https://www.cambridgeincolour.com/tutorials/color-spaces.htm.

Mô-đun :mod:`!colorsys` xác định các hàm sau:


.. function:: rgb_to_yiq(r, g, b)

   Chuyển đổi màu từ tọa độ RGB sang tọa độ YIQ.


.. function:: yiq_to_rgb(y, i, q)

   Chuyển đổi màu từ tọa độ YIQ sang tọa độ RGB.


.. function:: rgb_to_hls(r, g, b)

   Chuyển đổi màu từ tọa độ RGB sang tọa độ HLS.


.. function:: hls_to_rgb(h, l, s)

   Chuyển đổi màu từ tọa độ HLS sang tọa độ RGB.


.. function:: rgb_to_hsv(r, g, b)

   Chuyển đổi màu từ tọa độ RGB sang tọa độ HSV.


.. function:: hsv_to_rgb(h, s, v)

   Chuyển đổi màu từ tọa độ HSV sang tọa độ RGB.

Ví dụ::

   >>> import colorsys
   >>> colorsys.rgb_to_hsv(0.2, 0.4, 0.4)
   (0.5, 0.5, 0.4)
   >>> colorsys.hsv_to_rgb(0.5, 0.5, 0.4)
   (0.2, 0.4, 0.4)
