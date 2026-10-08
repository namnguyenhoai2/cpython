:mod:`!webbrowser` --- Trình điều khiển trình duyệt web tiện lợi
================================================================

.. module:: webbrowser
   :synopsis: Trình điều khiển dễ sử dụng cho các trình duyệt web.

.. moduleauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/webbrowser.py`

--------------

Mô-đun :mod:`!webbrowser` cung cấp giao diện cấp cao cho phép hiển thị các tài liệu trên nền web cho người dùng. Trong hầu hết trường hợp, chỉ cần gọi
hàm :func:`.open` của mô-đun này là đủ để thực hiện đúng việc cần làm.

Trên Unix, các trình duyệt đồ họa được ưu tiên trong X11, nhưng các trình duyệt ở chế độ văn bản sẽ được sử dụng nếu không có trình duyệt đồ họa hoặc không có màn hình X11. Nếu sử dụng trình duyệt ở chế độ văn bản, tiến trình gọi sẽ bị chặn cho đến khi người dùng thoát khỏi trình duyệt.

Nếu biến môi trường :envvar:`BROWSER` tồn tại, nó được hiểu là
Danh sách các trình duyệt được phân tách bằng :data:`os.pathsep` để thử trước các mặc định của nền tảng. Khi giá trị của một phần trong danh sách chứa chuỗi ``%s``, giá trị đó được diễn giải là một dòng lệnh trình duyệt theo nghĩa đen, dùng URL trong đối số thay thế cho ``%s``; nếu giá trị là một từ đơn chỉ một trong các trình duyệt đã đăng ký, trình duyệt này sẽ được thêm vào đầu danh sách tìm kiếm; nếu phần đó không chứa ``%s``, giá trị đó chỉ được diễn giải là tên của trình duyệt cần khởi chạy. [1]_

.. versionchanged:: 3.14

   Biến :envvar:`BROWSER` giờ đây cũng có thể được dùng để sắp xếp lại danh sách các giá trị mặc định của nền tảng. Điều này đặc biệt hữu ích trên macOS, nơi các giá trị mặc định của nền tảng không tham chiếu đến các công cụ dòng lệnh trên :envvar:`PATH`.


Trên các nền tảng không phải Unix hoặc khi có một trình duyệt từ xa trên Unix, tiến trình điều khiển sẽ không chờ người dùng sử dụng trình duyệt xong mà cho phép trình duyệt từ xa tự quản lý các cửa sổ của nó trên màn hình. Nếu không có trình duyệt từ xa trên Unix, tiến trình điều khiển sẽ khởi chạy một trình duyệt mới và chờ.

Trên iOS, biến môi trường :envvar:`BROWSER`, cũng như mọi đối số điều khiển việc tự động đưa trình duyệt lên trước, tùy chọn trình duyệt và việc tạo tab/cửa sổ mới, sẽ bị bỏ qua. Các trang web *luôn* được mở trong trình duyệt ưa thích của người dùng, trong một tab mới, đồng thời trình duyệt được đưa lên trước. Việc sử dụng
module :mod:`!webbrowser` trên iOS yêu cầu module :mod:`ctypes`. Nếu
:mod:`ctypes` không khả dụng, các lệnh gọi đến :func:`.open` sẽ thất bại.

.. _webbrowser-cli:

Giao diện dòng lệnh
-------------------

.. program:: webbrowser

Script :program:`webbrowser` có thể được sử dụng làm giao diện dòng lệnh cho module. Script này nhận một URL làm đối số. Script này nhận các tham số tùy chọn sau:

.. option:: -n, --new-window

   Mở URL trong một cửa sổ trình duyệt mới, nếu có thể.

.. option:: -t, --new-tab

   Mở URL trong một tab trình duyệt mới.

Đương nhiên, các tùy chọn này loại trừ lẫn nhau. Ví dụ sử dụng:

.. code-block:: bash

   python -m webbrowser -t "https://www.python.org"

.. availability:: not WASI, not Android.

Ngoại lệ sau được định nghĩa:


.. exception:: Error

   Ngoại lệ được phát sinh khi xảy ra lỗi điều khiển trình duyệt.

Các hàm sau được định nghĩa:


.. function:: open(url, new=0, autoraise=True)

   Hiển thị *url* bằng trình duyệt mặc định. Nếu *new* là 0, *url* sẽ được mở trong cùng cửa sổ trình duyệt nếu có thể. Nếu *new* là 1, một cửa sổ trình duyệt mới sẽ được mở nếu có thể. Nếu *new* là 2, một trang trình duyệt mới ("tab") sẽ được mở nếu có thể. Nếu *autoraise* là ``True``, cửa sổ sẽ được đưa lên trước nếu có thể (lưu ý rằng trong nhiều trình quản lý cửa sổ, điều này sẽ xảy ra bất kể giá trị của biến này).

   Trả về ``True`` nếu trình duyệt được khởi chạy thành công, nếu không thì trả về ``False``.

   Lưu ý rằng trên một số nền tảng, việc cố mở tên tệp bằng hàm này có thể hoạt động và khởi động chương trình liên kết của hệ điều hành. Tuy nhiên, điều này không được hỗ trợ và không có tính portable.

   .. audit-event:: webbrowser.open url webbrowser.open


.. function:: open_new(url)

   Mở *url* trong cửa sổ mới của trình duyệt mặc định nếu có thể; nếu không, mở *url* trong cửa sổ trình duyệt duy nhất.

   Trả về ``True`` nếu trình duyệt được khởi chạy thành công, nếu không thì trả về ``False``.


.. function:: open_new_tab(url)

   Mở *url* trong trang mới ("tab") của trình duyệt mặc định nếu có thể; nếu không, tương đương với :func:`open_new`.

   Trả về ``True`` nếu trình duyệt được khởi chạy thành công, nếu không thì trả về ``False``.


.. function:: get(using=None)

   Trả về một đối tượng controller cho loại trình duyệt *using*.  Nếu *using* là ``None``, hãy trả về một controller cho trình duyệt mặc định phù hợp với môi trường của bên gọi.


.. function:: register(name, constructor, instance=None, *, preferred=False)

   Đăng ký loại trình duyệt *name*.  Sau khi một loại trình duyệt được đăng ký, hàm
   :func:`get` có thể trả về một controller cho loại trình duyệt đó.  Nếu *instance* không được cung cấp hoặc là ``None``, *constructor* sẽ được gọi không có tham số để tạo một instance khi cần.  Nếu *instance* được cung cấp, *constructor* sẽ không bao giờ được gọi và có thể là ``None``.

   Đặt *preferred* thành ``True`` sẽ khiến trình duyệt này trở thành kết quả ưu tiên cho một lệnh gọi :func:`get` không có đối số.  Nếu không, entry point này chỉ hữu ích nếu bạn dự định đặt biến :envvar:`BROWSER` hoặc gọi
   :func:`get` với một đối số không rỗng khớp với tên của một handler mà bạn khai báo.

   .. versionchanged:: 3.7
      Đã thêm tham số chỉ dành cho keyword *preferred*.

Một số loại trình duyệt được định nghĩa sẵn.  Bảng này cung cấp các tên loại có thể được truyền vào hàm :func:`get` và các cách khởi tạo tương ứng cho các lớp controller, tất cả đều được định nghĩa trong module này.

+------------------------+----------------------------------+---------+
| Tên kiểu               | Tên lớp                          | Ghi chú |
+========================+==================================+=========+
| ``'mozilla'``          | ``Mozilla('mozilla')``           |         |
+------------------------+----------------------------------+---------+
| ``'firefox'``          | ``Mozilla('mozilla')``           |         |
+------------------------+----------------------------------+---------+
| ``'epiphany'``         | ``Epiphany('epiphany')``         |         |
+------------------------+----------------------------------+---------+
| ``'kfmclient'``        | ``Konqueror()``                  | \(1)    |
+------------------------+----------------------------------+---------+
| ``'konqueror'``        | ``Konqueror()``                  | \(1)    |
+------------------------+----------------------------------+---------+
| ``'kfm'``              | ``Konqueror()``                  | \(1)    |
+------------------------+----------------------------------+---------+
| ``'opera'``            | ``Opera()``                      |         |
+------------------------+----------------------------------+---------+
| ``'links'``            | ``GenericBrowser('links')``      |         |
+------------------------+----------------------------------+---------+
| ``'elinks'``           | ``Elinks('elinks')``             |         |
+------------------------+----------------------------------+---------+
| ``'lynx'``             | ``GenericBrowser('lynx')``       |         |
+------------------------+----------------------------------+---------+
| ``'w3m'``              | ``GenericBrowser('w3m')``        |         |
+------------------------+----------------------------------+---------+
| ``'windows-default'``  | ``WindowsDefault``               | \(2)    |
+------------------------+----------------------------------+---------+
| ``'macosx'``           | ``MacOSXOSAScript('default')``   | \(3)    |
+------------------------+----------------------------------+---------+
| ``'safari'``           | ``MacOSXOSAScript('safari')``    | \(3)    |
+------------------------+----------------------------------+---------+
| ``'google-chrome'``    | ``Chrome('google-chrome')``      |         |
+------------------------+----------------------------------+---------+
| ``'chrome'``           | ``Chrome('chrome')``             |         |
+------------------------+----------------------------------+---------+
| ``'chromium'``         | ``Chromium('chromium')``         |         |
+------------------------+----------------------------------+---------+
| ``'chromium-browser'`` | ``Chromium('chromium-browser')`` |         |
+------------------------+----------------------------------+---------+
| ``'iosbrowser'``       | ``IOSBrowser``                   | \(4)    |
+------------------------+----------------------------------+---------+

Ghi chú:

(1)
   "Konqueror" là trình quản lý tệp cho môi trường desktop KDE trên Unix và chỉ có ý nghĩa khi KDE đang chạy. Sẽ rất hữu ích nếu có cách phát hiện KDE đáng tin cậy; biến :envvar:`!KDEDIR` là chưa đủ. Cũng lưu ý rằng tên "kfm" vẫn được sử dụng ngay cả khi dùng lệnh :program:`konqueror` với KDE 2 --- phần triển khai sẽ chọn chiến lược tốt nhất để chạy Konqueror.

(2)
   Chỉ trên các nền tảng Windows.

(3)
   Chỉ trên macOS.

(4)
   Chỉ trên iOS.

.. versionadded:: 3.2
   Một lớp :class:`!MacOSXOSAScript` mới đã được thêm vào và được sử dụng trên Mac thay cho lớp :class:`!MacOSX` trước đây. Lớp này hỗ trợ mở các trình duyệt hiện không được đặt làm trình duyệt mặc định của hệ điều hành.

.. versionadded:: 3.3
   Đã thêm hỗ trợ cho Chrome/Chromium.

.. versionchanged:: 3.12
   Đã loại bỏ hỗ trợ cho một số trình duyệt lỗi thời. Các trình duyệt bị loại bỏ gồm Grail, Mosaic, Netscape, Galeon, Skipstone, Iceape và Firefox phiên bản 35 trở xuống.

.. versionchanged:: 3.13
   Đã thêm hỗ trợ cho iOS.

Sau đây là một số ví dụ đơn giản::

   url = 'https://docs.python.org/'

   # Mở URL trong tab mới nếu cửa sổ trình duyệt đã mở.
   webbrowser.open_new_tab(url)

   # Mở URL trong cửa sổ mới, đưa cửa sổ lên phía trước nếu có thể.
   webbrowser.open_new(url)


.. _browser-controllers:

Đối tượng điều khiển trình duyệt
--------------------------------

Các bộ điều khiển trình duyệt cung cấp thuộc tính :attr:`~controller.name` và ba phương thức sau, tương ứng với các hàm tiện ích cấp mô-đun:


.. attribute:: controller.name

   Tên phụ thuộc vào hệ thống của trình duyệt.


.. method:: controller.open(url, new=0, autoraise=True)

   Hiển thị *url* bằng trình duyệt do bộ điều khiển này quản lý. Nếu *new* là 1, một cửa sổ trình duyệt mới sẽ được mở nếu có thể. Nếu *new* là 2, một trang trình duyệt mới ("tab") sẽ được mở nếu có thể.


.. method:: controller.open_new(url)

   Mở *url* trong cửa sổ mới của trình duyệt do bộ điều khiển này quản lý nếu có thể; nếu không, mở *url* trong cửa sổ trình duyệt duy nhất. Bí danh
   :func:`open_new`.


.. method:: controller.open_new_tab(url)

   Mở *url* trong trang mới ("tab") của trình duyệt do bộ điều khiển này quản lý nếu có thể; nếu không, tương đương với :func:`open_new`.


.. rubric:: Chú thích cuối trang

.. [1] Các tệp thực thi được nêu ở đây mà không có đường dẫn đầy đủ sẽ được tìm kiếm trong các thư mục được chỉ định trong biến môi trường :envvar:`PATH`.
