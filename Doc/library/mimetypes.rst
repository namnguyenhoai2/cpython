:mod:`!mimetypes` --- Ánh xạ tên tệp với kiểu MIME
==================================================

.. module:: mimetypes
   :synopsis: Ánh xạ phần mở rộng tên tệp với kiểu MIME.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/mimetypes.py`

.. index:: pair: MIME; content type

--------------

Mô-đun :mod:`!mimetypes` chuyển đổi giữa tên tệp hoặc URL và kiểu MIME liên kết với phần mở rộng của tên tệp. Các chuyển đổi được cung cấp từ tên tệp sang kiểu MIME và từ kiểu MIME sang phần mở rộng tên tệp; việc mã hóa không được hỗ trợ cho chuyển đổi sau.

Mô-đun cung cấp một lớp và một số hàm tiện ích. Các hàm là giao diện thông thường của mô-đun này, nhưng một số ứng dụng cũng có thể quan tâm đến lớp này.

Các hàm được mô tả dưới đây cung cấp giao diện chính cho mô-đun này. Nếu mô-đun chưa được khởi tạo, chúng sẽ gọi :func:`init` nếu phụ thuộc vào thông tin mà :func:`init` thiết lập.


.. function:: guess_type(url, strict=True)

   .. index:: pair: MIME; headers

   Đoán kiểu của một tệp dựa trên tên tệp, đường dẫn hoặc URL được cung cấp bởi *url*. URL có thể là một chuỗi hoặc một :term:`path-like object`.

   Giá trị trả về là một tuple ``(type, encoding)`` trong đó *type* là ``None`` nếu không thể đoán được kiểu (hậu tố bị thiếu hoặc không xác định) hoặc là một chuỗi có dạng ``'type/subtype'``, có thể dùng cho một tiêu đề MIME :mailheader:`content-type` header.

   *encoding* là ``None`` khi không có encoding hoặc là tên của chương trình được dùng để mã hóa (ví dụ: :program:`compress` hoặc :program:`gzip`). encoding phù hợp để dùng làm header :mailheader:`Content-Encoding`, **không** như một
   :mailheader:`Content-Transfer-Encoding` header. Các ánh xạ được điều khiển bằng bảng. Các hậu tố encoding phân biệt chữ hoa chữ thường; các hậu tố type trước tiên được thử với phân biệt chữ hoa chữ thường, sau đó không phân biệt chữ hoa chữ thường.

   Đối số tùy chọn *strict* là một cờ chỉ định liệu danh sách các MIME type đã biết có bị giới hạn chỉ ở những type chính thức `được IANA đăng ký <https://www.iana.org/assignments/media-types/media-types.xhtml>`_ hay không. Tuy nhiên, hành vi của module này cũng phụ thuộc vào hệ điều hành bên dưới. Chỉ những loại tệp được hệ điều hành nhận diện hoặc được đăng ký rõ ràng với cơ sở dữ liệu nội bộ của Python mới có thể được xác định. Khi *strict* là ``True`` (mặc định), chỉ các type của IANA được hỗ trợ; khi *strict* là ``False``, một số MIME type không tiêu chuẩn nhưng thường được sử dụng cũng được nhận diện.

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ khi *url* là một :term:`path-like object`.

   .. soft-deprecated:: 3.13
      Truyền đường dẫn tệp thay vì URL. Dùng :func:`guess_file_type` cho việc này.


.. function:: guess_file_type(path, *, strict=True)

   .. index:: pair: MIME; headers

   Đoán type của tệp dựa trên đường dẫn được cung cấp bởi *path*. Tương tự hàm :func:`guess_type`, nhưng chấp nhận đường dẫn thay vì URL. path có thể là một chuỗi, một đối tượng bytes hoặc một :term:`path-like object`.

   .. versionadded:: 3.13


.. function:: guess_all_extensions(type, strict=True)

   Dự đoán các phần mở rộng của tệp dựa trên kiểu MIME của tệp, được chỉ định bởi *type*. Giá trị trả về là một danh sách các chuỗi chứa tất cả phần mở rộng tên tệp có thể có, bao gồm cả dấu chấm đứng đầu (``'.'``). Các phần mở rộng này không đảm bảo đã được liên kết với bất kỳ luồng dữ liệu cụ thể nào, nhưng sẽ được ánh xạ tới kiểu MIME *type* bởi :func:`guess_type` và :func:`guess_file_type`.

   Đối số tùy chọn *strict* có cùng ý nghĩa như đối với hàm :func:`guess_type`.


.. function:: guess_extension(type, strict=True)

   Dự đoán phần mở rộng cho một tệp dựa trên kiểu MIME của tệp, được chỉ định bởi *type*. Giá trị trả về là một chuỗi chứa phần mở rộng tên tệp, bao gồm cả dấu chấm đứng đầu (``'.'``). Phần mở rộng này không đảm bảo đã được liên kết với bất kỳ luồng dữ liệu cụ thể nào, nhưng sẽ được ánh xạ tới kiểu MIME *type* bởi
   :func:`guess_type` và :func:`guess_file_type`. Nếu không thể dự đoán phần mở rộng cho *type*, ``None`` sẽ được trả về.

   Đối số tùy chọn *strict* có cùng ý nghĩa như đối với hàm :func:`guess_type`.

Có một số hàm và mục dữ liệu bổ sung để kiểm soát hành vi của module.


.. function:: init(files=None)

   Khởi tạo các cấu trúc dữ liệu nội bộ. Nếu được cung cấp, *files* phải là một chuỗi tên tệp được dùng để bổ sung vào ánh xạ kiểu mặc định. Nếu bỏ qua, các tên tệp cần dùng sẽ được lấy từ :const:`knownfiles`; trên Windows, các thiết lập registry hiện tại sẽ được tải. Mỗi tệp được đặt tên trong *files* hoặc
   :const:`knownfiles` được ưu tiên hơn những đối số được đặt tên trước nó. Việc gọi
   :func:`init` nhiều lần là được phép.

   Việc chỉ định một danh sách rỗng cho *files* sẽ ngăn không cho các giá trị mặc định của hệ thống được áp dụng: chỉ các giá trị phổ biến mới có trong danh sách dựng sẵn.

   Nếu *files* là ``None``, cấu trúc dữ liệu nội bộ sẽ được xây dựng lại hoàn toàn về giá trị mặc định ban đầu. Đây là một thao tác ổn định và sẽ cho cùng một kết quả khi được gọi nhiều lần.

   .. versionchanged:: 3.2
      Trước đây, các thiết lập trong Windows registry bị bỏ qua.


.. function:: read_mime_types(file)

   Tải type map được chỉ định trong tệp có tên do *file* cung cấp, nếu tệp đó tồn tại. *file* phải là một chuỗi chỉ định tên tệp cần đọc. Type map được trả về dưới dạng một dictionary ánh xạ các phần mở rộng tệp, bao gồm dấu chấm đứng đầu (``'.'``), tới các chuỗi có dạng ``'type/subtype'``. Nếu tệp không tồn tại hoặc không thể đọc, ``None`` sẽ được trả về.


.. function:: add_type(type, ext, strict=True)

   Thêm một ánh xạ từ MIME type *type* tới phần mở rộng *ext*. Khi phần mở rộng đã được biết, type mới sẽ thay thế type cũ. Khi type đã được biết, phần mở rộng sẽ được thêm vào danh sách các phần mở rộng đã biết.

   Khi *strict* là ``True`` (mặc định), ánh xạ sẽ được thêm vào các kiểu MIME chính thức; nếu không, ánh xạ sẽ được thêm vào các kiểu không chuẩn.


.. data:: inited

   Cờ cho biết các cấu trúc dữ liệu toàn cục đã được khởi tạo hay chưa. Giá trị này được đặt thành ``True`` bởi :func:`init`.


.. data:: knownfiles

   .. index:: single: file; mime.types

   Danh sách các tên tệp ánh xạ kiểu thường được cài đặt. Các tệp này thường có tên là
   :file:`mime.types` và được các gói khác nhau cài đặt ở các vị trí khác nhau.


.. data:: suffix_map

   Từ điển ánh xạ các hậu tố sang các hậu tố. Từ điển này được dùng để nhận dạng các tệp đã mã hóa, trong đó mã hóa và kiểu được biểu thị bằng cùng một phần mở rộng. Ví dụ: phần mở rộng :file:`.tgz` được ánh xạ tới :file:`.tar.gz` để cho phép nhận dạng riêng mã hóa và kiểu.


.. data:: encodings_map

   Từ điển ánh xạ các phần mở rộng tên tệp sang các kiểu mã hóa.


.. data:: types_map

   Từ điển ánh xạ các phần mở rộng tên tệp sang các kiểu MIME.


.. data:: common_types

   Từ điển ánh xạ phần mở rộng tên tệp với các kiểu MIME không theo chuẩn nhưng thường gặp.


Ví dụ về cách sử dụng mô-đun::

   >>> import mimetypes
   >>> mimetypes.init()
   >>> mimetypes.knownfiles
   ['/etc/mime.types', '/etc/httpd/mime.types', ... ]
   >>> mimetypes.suffix_map['.tgz']
   '.tar.gz'
   >>> mimetypes.encodings_map['.gz']
   'gzip'
   >>> mimetypes.types_map['.tgz']
   'application/x-tar-gz'


.. _mimetypes-objects:

Đối tượng MimeTypes
-------------------

Lớp :class:`MimeTypes` có thể hữu ích cho các ứng dụng cần nhiều hơn một cơ sở dữ liệu kiểu MIME; lớp này cung cấp một giao diện tương tự giao diện của
mô-đun :mod:`!mimetypes`.


.. class:: MimeTypes(filenames=(), strict=True)

   Lớp này đại diện cho một cơ sở dữ liệu MIME-types. Theo mặc định, lớp này cung cấp quyền truy cập vào cùng cơ sở dữ liệu như phần còn lại của module này. Cơ sở dữ liệu ban đầu được tạo từ các bảng loại MIME tích hợp sẵn của Python. Cơ sở dữ liệu có thể được mở rộng bằng cách tải thêm
   các tệp theo kiểu :file:`mime.types`\  vào cơ sở dữ liệu bằng cách sử dụng :meth:`read` hoặc
   các phương thức :meth:`readfp`. Các từ điển ánh xạ cũng có thể được xóa trước khi tải thêm dữ liệu nếu không muốn sử dụng dữ liệu mặc định.

   Có thể sử dụng tham số tùy chọn *filenames* để tải thêm các tệp "chồng lên" cơ sở dữ liệu mặc định.


   .. attribute:: MimeTypes.suffix_map

      Từ điển ánh xạ các hậu tố sang các hậu tố. Từ điển này được dùng để nhận dạng các tệp đã mã hóa, trong đó mã hóa và kiểu được biểu thị bằng cùng một phần mở rộng. Ví dụ: phần mở rộng :file:`.tgz` được ánh xạ tới :file:`.tar.gz` để cho phép nhận dạng riêng mã hóa và kiểu. Từ điển này được khởi tạo với một số giá trị định sẵn.


   .. attribute:: MimeTypes.encodings_map

      Từ điển ánh xạ các phần mở rộng tên tệp tới các kiểu mã hóa. Từ điển này được khởi tạo với một số giá trị định sẵn.


   .. attribute:: MimeTypes.types_map

      Tuple chứa hai từ điển ánh xạ các phần mở rộng tên tệp tới các kiểu MIME: từ điển thứ nhất dành cho các kiểu không theo tiêu chuẩn và từ điển thứ hai dành cho các kiểu tiêu chuẩn. Chúng được khởi tạo với một số giá trị định sẵn và thông tin kiểu MIME được tải từ các tệp được chỉ định bởi đối số *filenames*.


   .. attribute:: MimeTypes.types_map_inv

      Tuple chứa hai từ điển ánh xạ các kiểu MIME tới danh sách phần mở rộng tên tệp: từ điển thứ nhất dành cho các kiểu không theo tiêu chuẩn và từ điển thứ hai dành cho các kiểu tiêu chuẩn. Chúng được khởi tạo với một số giá trị định sẵn và thông tin kiểu MIME được tải từ các tệp được chỉ định bởi đối số *filenames*.


   .. method:: MimeTypes.guess_extension(type, strict=True)

      Tương tự hàm :func:`guess_extension`, sử dụng các bảng được lưu trữ như một phần của đối tượng.


   .. method:: MimeTypes.guess_type(url, strict=True)

      Tương tự như hàm :func:`guess_type`, sử dụng các bảng được lưu trữ như một phần của đối tượng.


   .. method:: MimeTypes.guess_file_type(path, *, strict=True)

      Tương tự như hàm :func:`guess_file_type`, sử dụng các bảng được lưu trữ như một phần của đối tượng.

      .. versionadded:: 3.13


   .. method:: MimeTypes.guess_all_extensions(type, strict=True)

      Tương tự như hàm :func:`guess_all_extensions`, sử dụng các bảng được lưu trữ như một phần của đối tượng.


   .. method:: MimeTypes.read(filename, strict=True)

      Tải thông tin MIME từ tệp có tên *filename*. Tệp này được phân tích cú pháp bằng :meth:`readfp`.

      Nếu *strict* là ``True``, thông tin sẽ được thêm vào danh sách các loại tiêu chuẩn; nếu không, thông tin sẽ được thêm vào danh sách các loại không tiêu chuẩn.


   .. method:: MimeTypes.readfp(fp, strict=True)

      Tải thông tin loại MIME từ tệp đang mở *fp*. Tệp phải có định dạng của các tệp :file:`mime.types` tiêu chuẩn.

      Nếu *strict* là ``True``, thông tin sẽ được thêm vào danh sách các loại tiêu chuẩn; nếu không, thông tin sẽ được thêm vào danh sách các loại không tiêu chuẩn.


   .. method:: MimeTypes.read_windows_registry(strict=True)

      Tải thông tin về MIME type từ Windows registry.

      .. availability:: Windows.

      Nếu *strict* là ``True``, thông tin sẽ được thêm vào danh sách các loại tiêu chuẩn; nếu không, thông tin sẽ được thêm vào danh sách các loại không tiêu chuẩn.

      .. versionadded:: 3.2


   .. method:: MimeTypes.add_type(type, ext, strict=True)

      Thêm ánh xạ từ MIME type *type* đến phần mở rộng *ext*. Phần mở rộng hợp lệ bắt đầu bằng '.' hoặc để trống. Khi phần mở rộng đã được biết, type mới sẽ thay thế type cũ. Khi type đã được biết, phần mở rộng sẽ được thêm vào danh sách các phần mở rộng đã biết.

      Khi *strict* là ``True`` (mặc định), ánh xạ sẽ được thêm vào các MIME type chính thức; nếu không, ánh xạ sẽ được thêm vào các MIME type không theo chuẩn.

      .. deprecated-removed:: 3.14 3.16
         Các phần mở rộng không hợp lệ và không có dấu chấm sẽ gây ra một
         :exc:`ValueError` trong Python 3.16.


.. _mimetypes-cli:

Cách sử dụng dòng lệnh
----------------------

Module :mod:`!mimetypes` có thể được thực thi dưới dạng script từ dòng lệnh.

.. code-block:: sh

   python -m mimetypes [-h] [-e] [-l] type [type ...]

Các tùy chọn sau được chấp nhận:

.. program:: mimetypes

.. cmdoption:: -h
               --help

   Hiển thị thông báo trợ giúp rồi thoát.

.. cmdoption:: -e
               --extension

   Đoán phần mở rộng thay vì kiểu.

.. cmdoption:: -l
               --lenient

   Ngoài ra, hãy tìm kiếm một số kiểu phổ biến nhưng không theo chuẩn.

Theo mặc định, script chuyển đổi các kiểu MIME thành phần mở rộng tệp. Tuy nhiên, nếu chỉ định ``--extension``, script sẽ chuyển đổi các phần mở rộng tệp thành kiểu MIME.

Với mỗi mục ``type``, script ghi một dòng vào luồng đầu ra chuẩn. Nếu xuất hiện một kiểu không xác định, script ghi thông báo lỗi vào luồng đầu ra chuẩn và thoát với mã trả về ``1``.


.. mimetypes-cli-example:

Ví dụ dòng lệnh
---------------

Sau đây là một số ví dụ về cách sử dụng điển hình giao diện dòng lệnh của lệnh :mod:`!mimetypes`:

.. code-block:: console

   $ # get a MIME type by a file name
   $ python -m mimetypes filename.png
   type: image/png encoding: None

   $ # get a MIME type by a URL
   $ python -m mimetypes https://example.com/filename.txt
   type: text/plain encoding: None

   $ # get a complex MIME type
   $ python -m mimetypes filename.tar.gz
   type: application/x-tar encoding: gzip

   $ # get a MIME type for a rare file extension
   $ python -m mimetypes filename.pict
   error: media type unknown for filename.pict

   $ # now look in the extended database built into Python
   $ python -m mimetypes --lenient filename.pict
   type: image/pict encoding: None

   $ # get a file extension by a MIME type
   $ python -m mimetypes --extension text/javascript
   .js

   $ # get a file extension by a rare MIME type
   $ python -m mimetypes --extension text/xul
   error: unknown type text/xul

   $ # now look in the extended database again
   $ python -m mimetypes --extension --lenient text/xul
   .xul

   $ # try to feed an unknown file extension
   $ python -m mimetypes filename.sh filename.nc filename.xxx filename.txt
   type: application/x-sh encoding: None
   type: application/x-netcdf encoding: None
   error: media type unknown for filename.xxx
   type: text/plain encoding: None

   $ # try to feed an unknown MIME type
   $ python -m mimetypes --extension audio/aac audio/opus audio/future audio/x-wav
   .aac
   .opus
   error: unknown type audio/future

.. _`registered with IANA`: https://www.iana.org/assignments/media-types/media-types.xhtml
