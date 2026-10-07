:mod:`!ensurepip` --- Khởi tạo bộ cài đặt ``pip``
=================================================

.. module:: ensurepip
   :synopsis: Khởi tạo bộ cài đặt "pip" vào một cài đặt Python hoặc môi trường ảo hiện có.

.. versionadded:: 3.4

**Mã nguồn:** :source:`Lib/ensurepip`

--------------

Gói :mod:`!ensurepip` cung cấp khả năng khởi tạo bộ cài đặt ``pip`` vào một cài đặt Python hoặc môi trường ảo hiện có. Cách khởi tạo này phản ánh thực tế rằng ``pip`` là một dự án độc lập với chu kỳ phát hành riêng, và phiên bản ổn định mới nhất hiện có được đóng gói cùng với các bản phát hành bảo trì và tính năng của trình thông dịch tham chiếu CPython.

Trong hầu hết trường hợp, người dùng cuối Python không cần gọi trực tiếp mô-đun này (vì ``pip`` thường được khởi tạo theo mặc định), nhưng có thể cần đến nó nếu việc cài đặt ``pip`` bị bỏ qua khi cài đặt Python (hoặc khi tạo môi trường ảo), hoặc sau khi ``pip`` được gỡ cài đặt một cách rõ ràng.

.. note::

   Mô-đun này *không* truy cập Internet. Tất cả các thành phần cần thiết để khởi tạo ``pip`` đều được tích hợp dưới dạng các phần nội bộ của gói.

.. include:: ../includes/optional-module.rst

.. seealso::

   :ref:`installing-index`
      Hướng dẫn dành cho người dùng cuối về cài đặt các gói Python

   :pep:`453`: Khởi tạo pip một cách tường minh trong các bản cài đặt Python
      Cơ sở lý luận và đặc tả ban đầu cho module này.

.. include:: ../includes/wasm-mobile-notavail.rst

.. _ensurepip-cli:

Giao diện dòng lệnh
-------------------

.. program:: ensurepip

Giao diện dòng lệnh được gọi bằng switch ``-m`` của trình thông dịch.

Cách gọi đơn giản nhất là::

    python -m ensurepip

Cách gọi này sẽ cài đặt ``pip`` nếu nó chưa được cài đặt, còn nếu đã được cài đặt thì không thực hiện thao tác nào. Để đảm bảo phiên bản ``pip`` đã cài đặt ít nhất cũng mới như phiên bản có trong ``ensurepip``, hãy truyền tùy chọn ``--upgrade``::

    python -m ensurepip --upgrade

Theo mặc định, ``pip`` được cài đặt vào virtual environment hiện tại (nếu đang có một virtual environment hoạt động) hoặc vào các site packages của hệ thống (nếu không có virtual environment hoạt động). Có thể kiểm soát vị trí cài đặt thông qua hai tùy chọn dòng lệnh bổ sung:

.. option:: --root <dir>

   Cài đặt ``pip`` tương đối với thư mục gốc đã cho thay vì thư mục gốc của môi trường ảo hiện đang hoạt động (nếu có) hoặc thư mục gốc mặc định của bản cài đặt Python hiện tại.

.. option:: --user

   Cài đặt ``pip`` vào thư mục gói của người dùng thay vì cài đặt trên toàn hệ thống cho bản cài đặt Python hiện tại (tùy chọn này không được phép bên trong môi trường ảo đang hoạt động).

Theo mặc định, các script ``pipX`` và ``pipX.Y`` sẽ được cài đặt (trong đó X.Y đại diện cho phiên bản Python được dùng để gọi ``ensurepip``). Có thể kiểm soát các script được cài đặt bằng hai tùy chọn dòng lệnh bổ sung:

.. option:: --altinstall

   Nếu yêu cầu cài đặt thay thế, script ``pipX`` sẽ *không* được cài đặt.

.. option:: --default-pip

   Nếu yêu cầu cài đặt "default pip", script ``pip`` sẽ được cài đặt cùng với hai script thông thường.

Việc cung cấp cả hai tùy chọn chọn script sẽ kích hoạt một ngoại lệ.

API mô-đun
----------

:mod:`!ensurepip` cung cấp hai hàm để sử dụng theo cách lập trình:

.. function:: version()

   Trả về một chuỗi chỉ định phiên bản pip có sẵn sẽ được cài đặt khi khởi tạo một môi trường.

.. function:: bootstrap(root=None, upgrade=False, user=False, \
                        altinstall=False, default_pip=False, \ verbosity=0)

   Khởi tạo ``pip`` vào môi trường hiện tại hoặc môi trường được chỉ định.

   *root* chỉ định một thư mục gốc thay thế để cài đặt tương đối với thư mục đó. Nếu *root* là ``None``, quá trình cài đặt sẽ sử dụng vị trí cài đặt mặc định cho môi trường hiện tại.

   *upgrade* cho biết có nâng cấp bản cài đặt hiện có của phiên bản ``pip`` trước đó lên phiên bản có sẵn hay không.

   *user* cho biết có sử dụng user scheme thay vì cài đặt trên toàn hệ thống hay không.

   Theo mặc định, các script ``pipX`` và ``pipX.Y`` sẽ được cài đặt (trong đó X.Y đại diện cho phiên bản Python hiện tại).

   Nếu *altinstall* được đặt, thì ``pipX`` sẽ *not* được cài đặt.

   Nếu *default_pip* được đặt, thì ``pip`` sẽ được cài đặt bổ sung cùng với hai script thông thường.

   Việc đặt cả *altinstall* và *default_pip* sẽ kích hoạt
   :exc:`ValueError`.

   *verbosity* kiểm soát mức độ thông tin xuất ra :data:`sys.stdout` từ thao tác bootstrap.

   .. audit-event:: ensurepip.bootstrap root ensurepip.bootstrap

   .. note::

      Quy trình bootstrap gây ra các tác động phụ trên cả ``sys.path`` và ``os.environ``. Việc gọi giao diện dòng lệnh trong một subprocess thay vào đó cho phép tránh các tác động phụ này.

   .. note::

      Quy trình bootstrap có thể cài đặt các module bổ sung mà ``pip`` yêu cầu, nhưng phần mềm khác không nên giả định rằng các dependency đó sẽ luôn hiện diện theo mặc định (vì các dependency có thể bị loại bỏ trong phiên bản tương lai của ``pip``).

