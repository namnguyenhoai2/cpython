:mod:`!shutil` --- Các thao tác tệp ở cấp cao
=============================================

.. module:: shutil
   :synopsis: Các thao tác tệp ở cấp cao, bao gồm sao chép.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. partly based on the docstrings

**Mã nguồn:** :source:`Lib/shutil.py`

.. index::
   single: file; copying
   single: copying files

--------------

Mô-đun :mod:`!shutil` cung cấp một số thao tác ở cấp cao trên các tệp và tập hợp tệp. Cụ thể, mô-đun này cung cấp các hàm hỗ trợ sao chép và xóa tệp. Để thực hiện các thao tác trên từng tệp, hãy xem thêm
mô-đun :mod:`os`.

.. warning::

   Ngay cả các hàm sao chép tệp ở cấp cao hơn (:func:`shutil.copy`,
   :func:`shutil.copy2`) cũng không thể sao chép tất cả metadata của tệp.

   Trên các nền tảng POSIX, điều này có nghĩa là thông tin chủ sở hữu và nhóm của tệp cũng như ACL sẽ bị mất. Trên Mac OS, resource fork và các siêu dữ liệu khác không được sử dụng. Điều này có nghĩa là các tài nguyên sẽ bị mất, đồng thời mã loại tệp và mã trình tạo sẽ không chính xác. Trên Windows, chủ sở hữu tệp, ACL và alternate data streams sẽ không được sao chép.


.. _file-operations:

Các thao tác với thư mục và tệp
-------------------------------

.. function:: copyfileobj(fsrc, fdst[, length])

   Sao chép nội dung của :term:`đối tượng giống tệp <file object>` *fsrc* sang đối tượng giống tệp *fdst*. Số nguyên *length*, nếu được cung cấp, là kích thước bộ đệm. Cụ thể, giá trị *length* âm có nghĩa là sao chép dữ liệu mà không lặp qua dữ liệu nguồn theo từng khối; theo mặc định, dữ liệu được đọc theo từng khối để tránh tiêu thụ bộ nhớ không kiểm soát. Lưu ý rằng nếu vị trí tệp hiện tại của đối tượng *fsrc* không phải là 0, chỉ nội dung từ vị trí tệp hiện tại đến cuối tệp mới được sao chép.

   :func:`copyfileobj` sẽ *không* đảm bảo rằng luồng đích đã được flush khi hoàn tất việc sao chép. Nếu bạn muốn đọc từ đích sau khi hoàn tất thao tác sao chép (ví dụ: đọc nội dung của một tệp tạm thời đã được sao chép từ một HTTP stream), bạn phải đảm bảo rằng mình đã gọi :func:`~io.IOBase.flush` hoặc
   :func:`~io.IOBase.close` trên đối tượng giống tệp trước khi cố đọc tệp đích.

.. function:: copyfile(src, dst, *, follow_symlinks=True)

   Sao chép nội dung (không có siêu dữ liệu) của tệp có tên *src* sang tệp có tên *dst* và trả về *dst* theo cách hiệu quả nhất có thể. *src* và *dst* là :term:`đối tượng dạng đường dẫn <path-like object>` hoặc tên đường dẫn được cung cấp dưới dạng chuỗi.

   *dst* phải là tên tệp đích đầy đủ; hãy xem :func:`~shutil.copy` để biết cách sao chép chấp nhận đường dẫn thư mục đích. Nếu *src* và *dst* chỉ đến cùng một tệp, :exc:`SameFileError` sẽ được phát sinh.

   Vị trí đích phải có quyền ghi; nếu không, một ngoại lệ :exc:`OSError` sẽ được phát sinh. Nếu *dst* đã tồn tại, nó sẽ bị thay thế. Không thể sao chép các tệp đặc biệt như thiết bị ký tự, thiết bị khối và pipe bằng hàm này.

   Nếu *follow_symlinks* là false và *src* là một symbolic link, một symbolic link mới sẽ được tạo thay vì sao chép tệp mà *src* trỏ tới.

   .. audit-event:: shutil.copyfile src,dst shutil.copyfile

   .. versionchanged:: 3.3
      :exc:`IOError` used to be raised instead of :exc:`OSError`.
      Đã thêm đối số *follow_symlinks*. Hiện trả về *dst*.

   .. versionchanged:: 3.4
      Phát sinh :exc:`SameFileError` thay vì :exc:`Error`. Vì loại ngoại lệ trước là lớp con của loại ngoại lệ sau, thay đổi này vẫn tương thích ngược.

   .. versionchanged:: 3.8
      Các syscall sao chép nhanh dành riêng cho từng nền tảng có thể được sử dụng nội bộ để sao chép tệp hiệu quả hơn. Xem
      mục :ref:`shutil-platform-dependent-efficient-copy-operations`.

.. exception:: SpecialFileError

   Ngoại lệ này được phát sinh khi :func:`copyfile` hoặc :func:`copytree` cố gắng sao chép một named pipe.

   .. versionadded:: 2.7

.. exception:: SameFileError

   Ngoại lệ này được phát sinh nếu nguồn và đích trong :func:`copyfile` là cùng một tệp.

   .. versionadded:: 3.4


.. function:: copymode(src, dst, *, follow_symlinks=True)

   Sao chép các bit quyền từ *src* sang *dst*. Nội dung tệp, chủ sở hữu và nhóm không bị ảnh hưởng. *src* và *dst* là :term:`đối tượng dạng đường dẫn <path-like object>` hoặc tên đường dẫn được cung cấp dưới dạng chuỗi. Nếu *follow_symlinks* là false và cả *src* lẫn *dst* đều là liên kết tượng trưng,
   :func:`copymode` sẽ cố gắng sửa đổi mode của chính *dst* (thay vì tệp mà nó trỏ tới). Chức năng này không khả dụng trên mọi nền tảng; hãy xem :func:`copystat` để biết thêm thông tin. Nếu
   :func:`copymode` không thể sửa đổi các liên kết tượng trưng trên nền tảng cục bộ và được yêu cầu thực hiện việc đó, nó sẽ không làm gì và trả về.

   .. audit-event:: shutil.copymode src,dst shutil.copymode

   .. versionchanged:: 3.3
      Đã thêm đối số *follow_symlinks*.

.. function:: copystat(src, dst, *, follow_symlinks=True)

   Sao chép các bit quyền, thời điểm truy cập gần nhất, thời điểm sửa đổi gần nhất và các cờ từ *src* sang *dst*. Trên Linux, :func:`copystat` cũng sao chép "extended attributes" khi có thể. Nội dung tệp, chủ sở hữu và nhóm không bị ảnh hưởng. *src* và *dst* là :term:`đối tượng dạng đường dẫn <path-like object>` hoặc tên đường dẫn được cung cấp dưới dạng chuỗi.

   Nếu *follow_symlinks* là false và *src* cùng *dst* đều tham chiếu đến các liên kết tượng trưng, :func:`copystat` sẽ thao tác trên chính các liên kết tượng trưng thay vì các tệp mà chúng trỏ tới—đọc thông tin từ liên kết tượng trưng *src* và ghi thông tin vào liên kết tượng trưng *dst*.

   .. note::

      Không phải nền tảng nào cũng cung cấp khả năng kiểm tra và sửa đổi symbolic link. Bản thân Python có thể cho bạn biết những chức năng nào hiện có trên hệ thống cục bộ.

      * Nếu ``os.chmod in os.supports_follow_symlinks`` là ``True``, :func:`copystat` có thể sửa đổi các bit quyền của symbolic link.

      * Nếu ``os.utime in os.supports_follow_symlinks`` là ``True``, :func:`copystat` có thể sửa đổi thời điểm truy cập và sửa đổi lần cuối của symbolic link.

      * Nếu ``os.chflags in os.supports_follow_symlinks`` là ``True``, :func:`copystat` có thể sửa đổi các cờ của symbolic link. (``os.chflags`` không khả dụng trên tất cả các nền tảng.)

      Trên những nền tảng không có một phần hoặc toàn bộ chức năng này, khi được yêu cầu sửa đổi một symbolic link,
      :func:`copystat` sẽ sao chép mọi thứ có thể.
      :func:`copystat` không bao giờ trả về trạng thái thất bại.

      Vui lòng xem :data:`os.supports_follow_symlinks` để biết thêm thông tin.

   .. audit-event:: shutil.copystat src,dst shutil.copystat

   .. versionchanged:: 3.3
      Đã thêm đối số *follow_symlinks* và hỗ trợ các extended attributes của Linux.

.. function:: copy(src, dst, *, follow_symlinks=True)

   Sao chép tệp *src* vào tệp hoặc thư mục *dst*.  *src* và *dst* phải là :term:`path-like objects <path-like object>` hoặc chuỗi.  Nếu *dst* chỉ định một thư mục, tệp sẽ được sao chép vào *dst* bằng tên tệp cơ sở từ *src*. Nếu *dst* chỉ định một tệp đã tồn tại, tệp đó sẽ được thay thế. Trả về đường dẫn đến tệp mới được tạo.

   Nếu *follow_symlinks* là false và *src* là một symbolic link, *dst* sẽ được tạo dưới dạng một symbolic link.  Nếu *follow_symlinks* là true và *src* là một symbolic link, *dst* sẽ là bản sao của tệp mà *src* trỏ tới.

   :func:`~shutil.copy` sao chép dữ liệu tệp và chế độ quyền của tệp (xem :func:`os.chmod`).  Các siêu dữ liệu khác, chẳng hạn như thời gian tạo và sửa đổi tệp, không được giữ lại. Để giữ lại tất cả siêu dữ liệu tệp từ bản gốc, hãy sử dụng
   :func:`~shutil.copy2` thay vào đó.

   .. audit-event:: shutil.copyfile src,dst shutil.copy

   .. audit-event:: shutil.copymode src,dst shutil.copy

   .. versionchanged:: 3.3
      Đã thêm đối số *follow_symlinks*. Hiện trả về đường dẫn đến tệp mới được tạo.

   .. versionchanged:: 3.8
      Các syscall sao chép nhanh dành riêng cho từng nền tảng có thể được sử dụng nội bộ để sao chép tệp hiệu quả hơn. Xem
      mục :ref:`shutil-platform-dependent-efficient-copy-operations`.

.. function:: copy2(src, dst, *, follow_symlinks=True)

   Tương tự :func:`~shutil.copy`, ngoại trừ việc :func:`copy2` cũng cố gắng bảo toàn metadata của tệp.

   Khi *follow_symlinks* là false và *src* là một symbolic link, :func:`copy2` cố gắng sao chép tất cả metadata từ symbolic link *src* sang symbolic link *dst* mới được tạo. Tuy nhiên, chức năng này không khả dụng trên mọi nền tảng. Trên các nền tảng không hỗ trợ một phần hoặc toàn bộ chức năng này, :func:`copy2` sẽ bảo toàn mọi metadata mà nó có thể; :func:`copy2` không bao giờ đưa ra ngoại lệ chỉ vì không thể bảo toàn metadata của tệp.

   :func:`copy2` sử dụng :func:`copystat` để sao chép metadata của tệp. Vui lòng xem :func:`copystat` để biết thêm thông tin về hỗ trợ của nền tảng đối với việc sửa đổi metadata của symbolic link.

   .. audit-event:: shutil.copyfile src,dst shutil.copy2

   .. audit-event:: shutil.copystat src,dst shutil.copy2

   .. versionchanged:: 3.3
      Đã thêm đối số *follow_symlinks*, đồng thời cố gắng sao chép cả các thuộc tính mở rộng của hệ thống tệp (hiện chỉ hỗ trợ Linux). Hiện trả về đường dẫn đến tệp mới được tạo.

   .. versionchanged:: 3.8
      Các syscall sao chép nhanh dành riêng cho từng nền tảng có thể được sử dụng nội bộ để sao chép tệp hiệu quả hơn. Xem
      mục :ref:`shutil-platform-dependent-efficient-copy-operations`.

.. function:: ignore_patterns(*patterns)

   Hàm factory này tạo ra một hàm có thể được sử dụng làm callable cho
   :func:`copytree`\' đối số *ignore*, bỏ qua các tệp và thư mục khớp với một trong các *patterns* kiểu glob được cung cấp. Xem ví dụ bên dưới.


.. function:: copytree(src, dst, symlinks=False, ignore=None, \
              copy_function=copy2, ignore_dangling_symlinks=False, \ dirs_exist_ok=False)

   Sao chép đệ quy toàn bộ cây thư mục bắt đầu từ *src* vào một thư mục có tên *dst* và trả về thư mục đích. Theo mặc định, tất cả các thư mục trung gian cần thiết để chứa *dst* cũng sẽ được tạo.

   Quyền và thời gian của các thư mục được sao chép bằng :func:`copystat`, còn từng tệp được sao chép bằng :func:`~shutil.copy2`.

   Nếu *symlinks* là true, các symbolic link trong cây nguồn sẽ được biểu diễn dưới dạng symbolic link trong cây mới và metadata của các link ban đầu sẽ được sao chép trong phạm vi nền tảng cho phép; nếu là false hoặc bị bỏ qua, nội dung và metadata của các tệp được liên kết sẽ được sao chép vào cây mới.

   Khi *symlinks* là false, nếu tệp mà symlink trỏ tới không tồn tại, một exception sẽ được thêm vào danh sách các lỗi được nêu trong một :exc:`Error` exception ở cuối quá trình sao chép. Bạn có thể đặt flag tùy chọn *ignore_dangling_symlinks* thành true nếu muốn bỏ qua exception này. Lưu ý rằng tùy chọn này không có tác dụng trên các nền tảng không hỗ trợ :func:`os.symlink`.

   Nếu được cung cấp *ignore*, nó phải là một callable nhận thư mục đang được :func:`copytree` duyệt và danh sách nội dung của thư mục đó, do :func:`os.listdir` trả về, làm các đối số. Vì :func:`copytree` được gọi đệ quy, callable *ignore* sẽ được gọi một lần cho mỗi thư mục được sao chép. Callable này phải trả về một sequence gồm các tên thư mục và tệp tương đối với thư mục hiện tại (tức là một tập con các mục trong đối số thứ hai của nó); sau đó, các tên này sẽ bị bỏ qua trong quá trình sao chép. Có thể sử dụng :func:`ignore_patterns` để tạo một callable như vậy, nhằm bỏ qua các tên dựa trên các mẫu kiểu glob.

   Nếu xảy ra exception, một :exc:`Error` sẽ được nêu ra cùng với danh sách các lý do.

   Nếu được cung cấp *copy_function*, nó phải là một callable được sử dụng để sao chép từng tệp. Callable này sẽ được gọi với đường dẫn nguồn và đường dẫn đích làm các đối số. Theo mặc định, :func:`~shutil.copy2` được sử dụng, nhưng có thể sử dụng bất kỳ hàm nào hỗ trợ cùng signature (chẳng hạn như :func:`~shutil.copy`).

   Nếu *dirs_exist_ok* là false (giá trị mặc định) và *dst* đã tồn tại, một
   :exc:`FileExistsError` sẽ được nêu ra. Nếu *dirs_exist_ok* là true, thao tác sao chép sẽ tiếp tục nếu gặp các thư mục đã tồn tại, và các tệp trong cây *dst* sẽ bị ghi đè bởi các tệp tương ứng từ cây *src*.

   .. audit-event:: shutil.copytree src,dst shutil.copytree

   .. versionchanged:: 3.2
      Đã thêm đối số *copy_function* để có thể cung cấp một hàm sao chép tùy chỉnh. Đã thêm đối số *ignore_dangling_symlinks* để bỏ qua lỗi symlink treo khi *symlinks* là false.

   .. versionchanged:: 3.3
      Sao chép metadata khi *symlinks* là false. Hiện trả về *dst*.

   .. versionchanged:: 3.8
      Các syscall sao chép nhanh dành riêng cho từng nền tảng có thể được sử dụng nội bộ để sao chép tệp hiệu quả hơn. Xem
      mục :ref:`shutil-platform-dependent-efficient-copy-operations`.

   .. versionchanged:: 3.8
      Đã thêm tham số *dirs_exist_ok*.

.. function:: rmtree(path, ignore_errors=False, onerror=None, *, onexc=None, dir_fd=None)

   .. index:: single: directory; deleting

   Xóa toàn bộ cây thư mục; *path* phải trỏ đến một thư mục (nhưng không được là symbolic link trỏ đến thư mục). Nếu *ignore_errors* là true, các lỗi phát sinh từ việc xóa không thành công sẽ bị bỏ qua; nếu là false hoặc bị bỏ qua, các lỗi đó sẽ được xử lý bằng cách gọi handler được chỉ định bởi *onexc* hoặc *onerror*; nếu cả hai đều bị bỏ qua, các exception sẽ được truyền đến caller.

   Hàm này hỗ trợ :ref:`các path tương đối với file descriptor của thư mục <dir_fd>`.

   .. note::

      Trên các nền tảng hỗ trợ những hàm cần thiết dựa trên fd, một phiên bản chống tấn công symlink của :func:`rmtree` được sử dụng theo mặc định. Trên các nền tảng khác, triển khai :func:`rmtree` dễ bị tấn công symlink: nếu có thời điểm và điều kiện thích hợp, kẻ tấn công có thể thao túng các symlink trên hệ thống tệp để xóa những tệp mà chúng không thể truy cập theo cách khác. Ứng dụng có thể sử dụng thuộc tính hàm :data:`rmtree.avoids_symlink_attacks` để xác định trường hợp nào đang áp dụng.

   Nếu *onexc* được cung cấp, nó phải là một callable chấp nhận ba tham số: *function*, *path* và *excinfo*.

   Tham số đầu tiên, *function*, là hàm đã phát sinh ngoại lệ; hàm này phụ thuộc vào nền tảng và cách triển khai. Tham số thứ hai, *path*, sẽ là tên đường dẫn được truyền cho *function*. Tham số thứ ba, *excinfo*, là ngoại lệ đã phát sinh. Các ngoại lệ do *onexc* phát sinh sẽ không bị bắt.

   *onerror* đã bị ngừng sử dụng tương tự như *onexc*, ngoại trừ việc tham số thứ ba mà nó nhận được là tuple được trả về từ :func:`sys.exc_info`.

   .. seealso::
      :ref:`shutil-rmtree-example` for an example of handling the removal
      của một cây thư mục chứa các tệp chỉ đọc.

   .. audit-event:: shutil.rmtree path,dir_fd shutil.rmtree

   .. versionchanged:: 3.3
      Đã bổ sung một phiên bản chống tấn công symlink, phiên bản này được tự động sử dụng nếu nền tảng hỗ trợ các hàm dựa trên fd.

   .. versionchanged:: 3.8
      Trên Windows, nội dung của directory junction sẽ không còn bị xóa trước khi junction bị xóa.

   .. versionchanged:: 3.11
      Đã bổ sung tham số *dir_fd*.

   .. versionchanged:: 3.12
      Đã thêm tham số *onexc*, không còn dùng *onerror*.

   .. versionchanged:: 3.13
      :func:`!rmtree` now ignores :exc:`FileNotFoundError` exceptions for all
      nhưng là đường dẫn cấp cao nhất. Các ngoại lệ khác với :exc:`OSError` và các lớp con của :exc:`!OSError` giờ đây luôn được truyền tiếp cho caller.

   .. attribute:: rmtree.avoids_symlink_attacks

      Cho biết liệu platform và implementation hiện tại có cung cấp phiên bản :func:`rmtree` có khả năng chống tấn công symlink hay không. Hiện tại, điều này chỉ đúng với các platform hỗ trợ các hàm truy cập thư mục dựa trên fd.

      .. versionadded:: 3.3


.. function:: move(src, dst, copy_function=copy2)

   Di chuyển đệ quy một tệp hoặc thư mục (*src*) đến một vị trí khác và trả về đích.

   Nếu *dst* là một thư mục hiện có hoặc một symlink trỏ đến thư mục, thì *src* sẽ được di chuyển vào trong thư mục đó. Đường dẫn đích trong thư mục đó không được tồn tại từ trước.

   Nếu *dst* đã tồn tại nhưng không phải là một thư mục, nó có thể bị ghi đè tùy theo ngữ nghĩa của :func:`os.rename`.

   :func:`os.rename` được ưu tiên sử dụng nội bộ khi *src* và đích nằm trên cùng hệ thống tệp. Trong trường hợp :func:`os.rename` thất bại do :exc:`OSError` (ví dụ: người dùng có quyền ghi vào tệp đích nhưng không có quyền ghi vào thư mục cha), phương thức này chuyển sang sử dụng *copy_function*; khi đó, *src* được sao chép đến đích bằng *copy_function* rồi bị xóa.

   Trong trường hợp là symlink, một symlink mới trỏ đến đích của *src* sẽ được tạo tại đích hoặc được dùng làm đích, và *src* sẽ bị xóa.

   Nếu được cung cấp *copy_function*, giá trị này phải là một callable nhận hai đối số, *src* và đích, và sẽ được dùng để sao chép *src* đến đích nếu không thể sử dụng :func:`os.rename`. Nếu nguồn là một thư mục,
   :func:`copytree` được gọi với *copy_function* được truyền vào. Giá trị mặc định của *copy_function* là :func:`copy2`. Sử dụng :func:`~shutil.copy` làm *copy_function* cho phép thao tác di chuyển thành công khi không thể đồng thời sao chép metadata, nhưng đổi lại sẽ không sao chép bất kỳ metadata nào.

   .. audit-event:: shutil.move src,dst shutil.move

   .. versionchanged:: 3.3
      Đã bổ sung xử lý symlink rõ ràng cho các filesystem khác, qua đó điều chỉnh theo hành vi của :program:`mv` của GNU. Hiện trả về *dst*.

   .. versionchanged:: 3.5
      Đã bổ sung đối số từ khóa *copy_function*.

   .. versionchanged:: 3.8
      Các syscall sao chép nhanh dành riêng cho từng nền tảng có thể được sử dụng nội bộ để sao chép tệp hiệu quả hơn. Xem
      mục :ref:`shutil-platform-dependent-efficient-copy-operations`.

   .. versionchanged:: 3.9
      Chấp nhận một :term:`path-like object` cho cả *src* và *dst*.

.. function:: disk_usage(path)

   Trả về thống kê mức sử dụng đĩa của đường dẫn đã cho dưới dạng :term:`named tuple` với các thuộc tính *total*, *used* và *free*, lần lượt là dung lượng tổng, dung lượng đã sử dụng và dung lượng còn trống, tính bằng byte. *path* có thể là một tệp hoặc thư mục.

   .. note::

      Trên các hệ thống tệp Unix, *path* phải trỏ đến một đường dẫn trong một phân vùng hệ thống tệp **mounted**. Trên các nền tảng đó, CPython không cố gắng lấy thông tin sử dụng đĩa từ các hệ thống tệp chưa được mount.

   .. versionadded:: 3.3

   .. versionchanged:: 3.8
     Trên Windows, *path* giờ đây có thể là một tệp hoặc thư mục.

   .. availability:: Unix, Windows.

.. function:: chown(path, user=None, group=None, *, dir_fd=None, \
                    follow_symlinks=True)

   Thay đổi chủ sở hữu *user* và/hoặc *group* của *path* đã cho.

   *user* có thể là tên người dùng hệ thống hoặc uid; điều tương tự cũng áp dụng cho *group*. Bắt buộc phải cung cấp ít nhất một đối số.

   Xem thêm :func:`os.chown`, hàm nền tảng.

   .. audit-event:: shutil.chown path,user,group shutil.chown

   .. availability:: Unix.

   .. versionadded:: 3.3

   .. versionchanged:: 3.13
      Đã thêm các tham số *dir_fd* và *follow_symlinks*.


.. function:: which(cmd, mode=os.F_OK | os.X_OK, path=None)

   Trả về đường dẫn đến tệp thực thi sẽ được chạy nếu *cmd* đã cho được gọi. Nếu không có *cmd* nào được gọi, trả về ``None``.

   *mode* là mặt nạ quyền được truyền đến :func:`os.access`, theo mặc định xác định xem tệp có tồn tại và có thể thực thi hay không.

   *path* là một "``PATH`` chuỗi" chỉ định các thư mục cần tìm, được phân tách bằng :data:`os.pathsep`. Khi không chỉ định *path*, biến
   :envvar:`PATH` môi trường được đọc từ :data:`os.environ`, dự phòng về :data:`os.defpath` nếu biến này chưa được thiết lập.

   Nếu *cmd* chứa một thành phần thư mục, :func:`!which` chỉ kiểm tra trực tiếp đường dẫn được chỉ định và không tìm kiếm các thư mục được liệt kê trong *path* hoặc trong biến môi trường :envvar:`PATH` của hệ thống.

   Trên Windows, thư mục hiện tại được thêm vào đầu *path* nếu *mode* không bao gồm ``os.X_OK``. Khi *mode* có bao gồm ``os.X_OK``, Windows API ``NeedCurrentDirectoryForExePathW`` sẽ được tham vấn để xác định xem có nên thêm thư mục hiện tại vào đầu *path* hay không. Để tránh tham vấn thư mục làm việc hiện tại khi tìm các tệp thực thi: hãy đặt biến môi trường ``NoDefaultCurrentDirectoryInExePath``.

   Cũng trên Windows, biến môi trường :envvar:`PATHEXT` được dùng để phân giải các lệnh có thể chưa bao gồm phần mở rộng. Ví dụ, nếu bạn gọi ``shutil.which("python")``, :func:`which` sẽ tìm kiếm ``PATHEXT`` để biết rằng nó cần tìm ``python.exe`` trong các thư mục *path*. Ví dụ, trên Windows::

      >>> shutil.which("python")
      'C:\\Python33\\python.EXE'

   Điều này cũng được áp dụng khi *cmd* là một đường dẫn chứa thành phần thư mục::

      >>> shutil.which("C:\\Python33\\python")
      'C:\\Python33\\python.EXE'

   .. versionadded:: 3.3

   .. versionchanged:: 3.8
      Kiểu :class:`bytes` hiện được chấp nhận.  Nếu kiểu *cmd* là
      :class:`bytes`, thì kiểu kết quả cũng là :class:`bytes`.

   .. versionchanged:: 3.12
      Trên Windows, thư mục hiện tại không còn được thêm vào đầu đường dẫn tìm kiếm nếu *mode* bao gồm ``os.X_OK`` và WinAPI ``NeedCurrentDirectoryForExePathW(cmd)`` là false; nếu không, thư mục hiện tại sẽ được thêm vào đầu ngay cả khi nó đã có trong đường dẫn tìm kiếm; ``PATHEXT`` hiện được sử dụng ngay cả khi *cmd* bao gồm một thành phần thư mục hoặc kết thúc bằng phần mở rộng có trong ``PATHEXT``; và các tên tệp không có phần mở rộng giờ đây có thể được tìm thấy.

.. exception:: Error

   Ngoại lệ này tập hợp các ngoại lệ phát sinh trong một thao tác trên nhiều tệp. Đối với :func:`copytree`, đối số ngoại lệ là một danh sách gồm các bộ 3 phần tử (*srcname*, *dstname*, *exception*).

.. _shutil-platform-dependent-efficient-copy-operations:

Các thao tác sao chép hiệu quả phụ thuộc vào nền tảng
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bắt đầu từ Python 3.8, tất cả các hàm liên quan đến việc sao chép tệp (:func:`copyfile`, :func:`~shutil.copy`, :func:`copy2`,
:func:`copytree`, và :func:`move`) có thể sử dụng các system call "fast-copy" dành riêng cho từng nền tảng để sao chép tệp hiệu quả hơn (xem :issue:`33671`). "fast-copy" nghĩa là thao tác sao chép diễn ra bên trong kernel, tránh sử dụng các bộ đệm userspace trong Python như trong "``outfd.write(infd.read())``".

Trên macOS, `fcopyfile`_ được sử dụng để sao chép nội dung tệp (không bao gồm metadata).

Trên Linux, :func:`os.copy_file_range` hoặc :func:`os.sendfile` được sử dụng.

Trên Solaris, :func:`os.sendfile` được sử dụng.

Trên Windows, :func:`shutil.copyfile` sử dụng kích thước bộ đệm mặc định lớn hơn (1 MiB thay vì 64 KiB) và một biến thể dựa trên :func:`memoryview` của
:func:`shutil.copyfileobj` được sử dụng.

Nếu thao tác sao chép nhanh không thành công và không có dữ liệu nào được ghi vào tệp đích thì shutil sẽ âm thầm chuyển sang cách kém hiệu quả hơn
hàm :func:`copyfileobj` ở bên trong.

.. versionchanged:: 3.8

.. versionchanged:: 3.14
    Solaris hiện sử dụng :func:`os.sendfile`.

.. versionchanged:: 3.14
   Có thể sử dụng tính năng copy-on-write hoặc sao chép phía máy chủ ở bên trong thông qua
   :func:`os.copy_file_range` trên các hệ thống tệp Linux được hỗ trợ.

.. _shutil-copytree-example:

ví dụ về copytree
~~~~~~~~~~~~~~~~~

Ví dụ sử dụng hàm trợ giúp :func:`ignore_patterns`::

   from shutil import copytree, ignore_patterns

   copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))

Thao tác này sẽ sao chép mọi thứ ngoại trừ các tệp ``.pyc`` và các tệp hoặc thư mục có tên bắt đầu bằng ``tmp``.

Một ví dụ khác sử dụng đối số *ignore* để thêm một lệnh gọi logging::

   from shutil import copytree
   import logging

   def _logpath(path, names):
       logging.info('Working in %s', path)
       return []   # sẽ không bỏ qua gì cả

   copytree(source, destination, ignore=_logpath)


.. _shutil-rmtree-example:

Ví dụ rmtree
~~~~~~~~~~~~

Ví dụ này cho biết cách xóa một cây thư mục trên Windows khi một số tệp có bit chỉ-đọc được thiết lập. Ví dụ sử dụng callback onexc để xóa bit chỉ-đọc rồi thử lại thao tác xóa. Mọi lỗi tiếp theo sẽ được truyền lên.::

    import os, stat
    import shutil

    def remove_readonly(func, path, _):
        "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(directory, onexc=remove_readonly)

.. _archiving-operations:

Các thao tác lưu trữ
--------------------

.. versionadded:: 3.2

.. versionchanged:: 3.5
    Đã thêm hỗ trợ cho định dạng *xztar*.


Cũng cung cấp các tiện ích cấp cao để tạo và đọc các tệp đã nén và lưu trữ. Chúng dựa trên các mô-đun :mod:`zipfile` và :mod:`tarfile`.

.. function:: make_archive(base_name, format, [root_dir, [base_dir, [verbose, [dry_run, [owner, [group, [logger]]]]]]])

   Tạo một tệp lưu trữ (chẳng hạn như zip hoặc tar) và trả về tên của tệp đó.

   *base_name* là tên của tệp cần tạo, bao gồm cả đường dẫn, nhưng không có phần mở rộng dành riêng cho định dạng.

   *format* là định dạng lưu trữ: một trong các định dạng "zip" (nếu mô-đun :mod:`zlib` khả dụng), "tar", "gztar" (nếu
   mô-đun :mod:`zlib` khả dụng), "bztar" (nếu mô-đun :mod:`bz2` khả dụng), "xztar" (nếu mô-đun :mod:`lzma` khả dụng) hoặc "zstdtar" (nếu mô-đun :mod:`compression.zstd` khả dụng).

   *root_dir* là một thư mục sẽ trở thành thư mục gốc của tệp lưu trữ; mọi đường dẫn trong tệp lưu trữ sẽ tương đối với thư mục này. Ví dụ: chúng ta thường chdir vào *root_dir* trước khi tạo tệp lưu trữ.

   *base_dir* là thư mục nơi chúng ta bắt đầu lưu trữ; tức là *base_dir* sẽ là tiền tố chung của tất cả các tệp và thư mục trong kho lưu trữ. *base_dir* phải được cung cấp tương đối so với *root_dir*. Xem :ref:`shutil-archiving-example-with-basedir` để biết cách sử dụng *base_dir* và *root_dir* cùng nhau.

   *root_dir* và *base_dir* đều mặc định là thư mục hiện tại.

   Nếu *dry_run* là true, không có kho lưu trữ nào được tạo, nhưng các thao tác đáng lẽ sẽ được thực hiện sẽ được ghi nhật ký vào *logger*.

   *owner* và *group* được sử dụng khi tạo kho lưu trữ tar. Theo mặc định, chủ sở hữu và nhóm hiện tại sẽ được sử dụng.

   *logger* phải là một đối tượng tương thích với :pep:`282`, thường là một thể hiện của
   :class:`logging.Logger`.

   Đối số *verbose* không được sử dụng và đã không còn được khuyến nghị.

   .. audit-event:: shutil.make_archive base_name,format,root_dir,base_dir shutil.make_archive

   .. note::

      Hàm này không an toàn với thread khi các archiver tùy chỉnh được đăng ký với :func:`register_archive_format` không hỗ trợ đối số *root_dir*. Trong trường hợp này, hàm tạm thời thay đổi thư mục làm việc hiện tại của process thành *root_dir* để thực hiện việc lưu trữ.

   .. versionchanged:: 3.8
      Định dạng pax hiện đại (POSIX.1-2001) hiện được sử dụng thay cho định dạng GNU cũ cho các archive được tạo bằng ``format="tar"``.

   .. versionchanged:: 3.10.6
      Hàm này hiện an toàn với thread trong quá trình tạo các archive ``.zip`` và tar tiêu chuẩn.

.. function:: get_archive_formats()

   Trả về danh sách các định dạng được hỗ trợ để lưu trữ. Mỗi phần tử trong sequence được trả về là một tuple ``(name, description)``.

   Theo mặc định, :mod:`!shutil` cung cấp các định dạng sau:

   - *zip*: Tệp ZIP (nếu module :mod:`zlib` khả dụng).
   - *tar*: Tệp tar không nén. Sử dụng định dạng pax POSIX.1-2001 cho các archive mới.
   - *gztar*: Tệp tar được nén bằng gzip (nếu module :mod:`zlib` khả dụng).
   - *bztar*: tệp tar được nén bằng bzip2 (nếu có module :mod:`bz2`).
   - *xztar*: tệp tar được nén bằng xz (nếu có module :mod:`lzma`).
   - *zstdtar*: tệp tar được nén bằng Zstandard (nếu có module :mod:`compression.zstd`).

   Bạn có thể đăng ký các định dạng mới hoặc cung cấp archiver của riêng mình cho bất kỳ định dạng hiện có nào bằng cách sử dụng :func:`register_archive_format`.


.. function:: register_archive_format(name, function, [extra_args, [description]])

   Đăng ký một archiver cho định dạng *name*.

   *function* là hàm có thể gọi được dùng để tạo các tệp lưu trữ. Hàm này sẽ nhận *base_name* của tệp cần tạo, tiếp theo là *base_dir* (mặc định là :data:`os.curdir`) làm thư mục bắt đầu quá trình lưu trữ. Các đối số tiếp theo được truyền dưới dạng keyword argument: *owner*, *group*, *dry_run* và *logger* (được truyền vào như trong :func:`make_archive`).

   Nếu *function* có thuộc tính tùy chỉnh ``function.supports_root_dir`` được đặt thành ``True``, đối số *root_dir* sẽ được truyền dưới dạng keyword argument. Nếu không, thư mục làm việc hiện tại của tiến trình sẽ tạm thời được đổi thành *root_dir* trước khi gọi *function*. Trong trường hợp này, :func:`make_archive` không an toàn khi sử dụng với nhiều thread.

   Nếu được cung cấp, *extra_args* là một chuỗi các cặp ``(name, value)`` sẽ được sử dụng làm các đối số từ khóa bổ sung khi callable archiver được sử dụng.

   *description* được :func:`get_archive_formats` sử dụng để trả về danh sách các archiver. Mặc định là một chuỗi rỗng.

   .. versionchanged:: 3.12
      Đã bổ sung hỗ trợ cho các hàm hỗ trợ đối số *root_dir*.


.. function:: unregister_archive_format(name)

   Xóa định dạng archive *name* khỏi danh sách các định dạng được hỗ trợ.


.. function:: unpack_archive(filename[, extract_dir[, format[, filter]]])

   Giải nén một archive. *filename* là đường dẫn đầy đủ của archive.

   *extract_dir* là tên của thư mục đích nơi archive được giải nén. Nếu không được cung cấp, thư mục làm việc hiện tại sẽ được sử dụng.

   *format* là định dạng archive: một trong các định dạng "zip", "tar", "gztar", "bztar", "xztar" hoặc "zstdtar". Hoặc bất kỳ định dạng nào khác được đăng ký với
   :func:`register_unpack_format`. Nếu không được cung cấp, :func:`unpack_archive` sẽ sử dụng phần mở rộng tên tệp lưu trữ và kiểm tra xem có trình giải nén nào được đăng ký cho phần mở rộng đó hay không. Nếu không tìm thấy, một :exc:`ValueError` sẽ được ném ra.

   Đối số chỉ dùng cho từ khóa *filter* được truyền đến hàm giải nén bên dưới. Đối với tệp zip, *filter* không được chấp nhận. Đối với tệp tar, bạn nên sử dụng ``'data'`` (mặc định kể từ Python 3.14), trừ khi sử dụng các tính năng dành riêng cho tar và hệ thống tệp tương tự UNIX. (Xem :ref:`tarfile-extraction-filter` để biết chi tiết.)

   .. audit-event:: shutil.unpack_archive filename,extract_dir,format shutil.unpack_archive

   .. warning::

      Không bao giờ giải nén lưu trữ từ các nguồn không đáng tin cậy mà chưa kiểm tra trước. Có thể các tệp được tạo bên ngoài đường dẫn được chỉ định trong đối số *extract_dir*, chẳng hạn như các thành viên có tên tệp tuyệt đối hoặc tên tệp chứa thành phần "..".

      Kể từ Python 3.14, các giá trị mặc định cho cả hai định dạng tích hợp (tệp zip và tar) sẽ ngăn chặn những vấn đề bảo mật nguy hiểm nhất trong số đó, nhưng sẽ không ngăn chặn *all* hành vi ngoài ý muốn. Đọc phần :ref:`tarfile-further-verification` để biết các chi tiết dành riêng cho tar.

   .. versionchanged:: 3.7
      Chấp nhận một :term:`path-like object` cho *filename* và *extract_dir*.

   .. versionchanged:: 3.12
      Đã thêm đối số *filter*.

.. function:: register_unpack_format(name, extensions, function[, extra_args[, description]])

   Đăng ký một định dạng giải nén. *name* là tên của định dạng và *extensions* là danh sách các phần mở rộng tương ứng với định dạng đó, chẳng hạn như ``.zip`` đối với các tệp Zip.

   *function* là hàm có thể gọi sẽ được dùng để giải nén các tệp lưu trữ. Hàm này sẽ nhận:

   - đường dẫn của tệp lưu trữ, dưới dạng đối số vị trí;
   - thư mục mà tệp lưu trữ phải được giải nén vào, dưới dạng đối số vị trí;
   - có thể là đối số từ khóa *filter*, nếu đối số này được truyền cho
     :func:`unpack_archive`;
   - các đối số từ khóa bổ sung, được chỉ định bởi *extra_args* dưới dạng một chuỗi các tuple ``(name, value)``.

   Có thể cung cấp *description* để mô tả định dạng; giá trị này sẽ được hàm :func:`get_unpack_formats` trả về.


.. function:: unregister_unpack_format(name)

   Hủy đăng ký một định dạng giải nén. *name* là tên của định dạng.


.. function:: get_unpack_formats()

   Trả về danh sách tất cả các định dạng đã đăng ký để giải nén. Mỗi phần tử trong chuỗi được trả về là một tuple ``(name, extensions, description)``.

   Theo mặc định, :mod:`!shutil` cung cấp các định dạng sau:

   - *zip*: tệp ZIP (chỉ có thể giải nén các tệp nén nếu có mô-đun tương ứng).
   - *tar*: tệp tar không nén.
   - *gztar*: Tệp tar được nén bằng gzip (nếu module :mod:`zlib` khả dụng).
   - *bztar*: tệp tar được nén bằng bzip2 (nếu có module :mod:`bz2`).
   - *xztar*: tệp tar được nén bằng xz (nếu có module :mod:`lzma`).
   - *zstdtar*: tệp tar được nén bằng Zstandard (nếu có module :mod:`compression.zstd`).

   Bạn có thể đăng ký các định dạng mới hoặc cung cấp unpacker của riêng mình cho bất kỳ định dạng hiện có nào bằng cách sử dụng :func:`register_unpack_format`.


.. _shutil-archiving-example:

Ví dụ về lưu trữ
~~~~~~~~~~~~~~~~

Trong ví dụ này, chúng ta tạo một archive tar được nén bằng gzip chứa tất cả các tệp được tìm thấy trong thư mục :file:`.ssh` của người dùng::

    >>> from shutil import make_archive
    >>> import os
    >>> archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
    >>> root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
    >>> make_archive(archive_name, 'gztar', root_dir)
    '/Users/tarek/myarchive.tar.gz'

Archive kết quả chứa:

.. code-block:: shell-session

    $ tar -tzvf /Users/tarek/myarchive.tar.gz
    drwx------ tarek/staff       0 2010-02-01 16:23:40 ./
    -rw-r--r-- tarek/staff     609 2008-06-09 13:26:54 ./authorized_keys
    -rwxr-xr-x tarek/staff      65 2008-06-09 13:26:54 ./config
    -rwx------ tarek/staff     668 2008-06-09 13:26:54 ./id_dsa
    -rwxr-xr-x tarek/staff     609 2008-06-09 13:26:54 ./id_dsa.pub
    -rw------- tarek/staff    1675 2008-06-09 13:26:54 ./id_rsa
    -rw-r--r-- tarek/staff     397 2008-06-09 13:26:54 ./id_rsa.pub
    -rw-r--r-- tarek/staff   37192 2010-02-06 18:23:10 ./known_hosts


.. _shutil-archiving-example-with-basedir:

Ví dụ về lưu trữ với *base_dir*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trong ví dụ này, tương tự như `ví dụ ở trên <shutil-archiving-example_>`_, chúng ta trình bày cách sử dụng :func:`make_archive`, nhưng lần này với việc sử dụng *base_dir*. Bây giờ chúng ta có cấu trúc thư mục sau:

.. code-block:: shell-session

    $ tree tmp
    tmp
    └── root
        └── structure
            ├── content
                └── please_add.txt
            └── do_not_add.txt

Trong archive cuối cùng, :file:`please_add.txt` phải được bao gồm, nhưng
:file:`do_not_add.txt` thì không. Vì vậy, chúng ta sử dụng nội dung sau::

    >>> from shutil import make_archive
    >>> import os
    >>> archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
    >>> make_archive(
    ...     archive_name,
    ...     'tar',
    ...     root_dir='tmp/root',
    ...     base_dir='structure/content',
    ... )
    '/Users/tarek/myarchive.tar'

Liệt kê các tệp trong archive kết quả cho ta:

.. code-block:: shell-session

    $ python -m tarfile -l /Users/tarek/myarchive.tar
    structure/content/
    structure/content/please_add.txt


Truy vấn kích thước của terminal đầu ra
---------------------------------------

.. function:: get_terminal_size(fallback=(columns, lines))

   Lấy kích thước cửa sổ terminal.

   Với mỗi trong hai chiều, biến môi trường ``COLUMNS`` và ``LINES`` tương ứng sẽ được kiểm tra. Nếu biến được định nghĩa và giá trị là một số nguyên dương, giá trị đó sẽ được sử dụng.

   Khi ``COLUMNS`` hoặc ``LINES`` chưa được định nghĩa, đây là trường hợp phổ biến, terminal được kết nối với :data:`sys.__stdout__` sẽ được truy vấn bằng cách gọi :func:`os.get_terminal_size`.

   Nếu không thể truy vấn kích thước terminal thành công, do hệ thống không hỗ trợ truy vấn hoặc chúng ta không kết nối với terminal, thì giá trị được cung cấp trong tham số ``fallback`` sẽ được sử dụng. ``fallback`` mặc định là ``(80, 24)``, đây là kích thước mặc định được nhiều trình mô phỏng terminal sử dụng.

   Giá trị trả về là một tuple có tên thuộc kiểu :class:`os.terminal_size`.

   Xem thêm: The Single UNIX Specification, Version 2, `Các biến môi trường khác <Other Environment Variables_>`_.

   .. versionadded:: 3.3

   .. versionchanged:: 3.11
      Các giá trị ``fallback`` cũng được sử dụng nếu :func:`os.get_terminal_size` trả về các số 0.

.. _`fcopyfile`:
   http://www.manpagez.com/man/3/copyfile/

.. _`Other Environment Variables`:
   https://pubs.opengroup.org/onlinepubs/7908799/xbd/envvar.html#tag_002_003

.. _`one above`: shutil-archiving-example_
