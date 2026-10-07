Sắp bị loại bỏ trong Python 3.19
--------------------------------

* :mod:`ctypes`:

  * Ngầm chuyển sang bố cục struct tương thích với MSVC bằng cách đặt
    :attr:`~ctypes.Structure._pack_` nhưng không phải :attr:`~ctypes.Structure._layout_` trên các nền tảng không phải Windows.
