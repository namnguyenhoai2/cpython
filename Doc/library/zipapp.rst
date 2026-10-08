:mod:`!zipapp` --- Quản lý các kho lưu trữ zip Python có thể thực thi
=====================================================================

.. module:: zipapp
   :synopsis: Quản lý các kho lưu trữ zip Python có thể thực thi

.. versionadded:: 3.5

**Mã nguồn:** :source:`Lib/zipapp.py`

.. index::
   single: Executable Zip Files

--------------

Mô-đun này cung cấp các công cụ để quản lý việc tạo các tệp zip chứa mã Python, có thể được  :ref:`thực thi trực tiếp bằng trình thông dịch Python <using-on-interface-options>`.  Mô-đun này cung cấp cả một
:ref:`zipapp-command-line-interface` và một :ref:`zipapp-python-api`.


Ví dụ cơ bản
------------

Ví dụ sau đây cho thấy cách sử dụng :ref:`zipapp-command-line-interface` để tạo một kho lưu trữ có thể thực thi từ một thư mục chứa mã Python.  Khi chạy, kho lưu trữ sẽ thực thi hàm ``main`` từ mô-đun ``myapp`` trong kho lưu trữ.

.. code-block:: shell-session

   $ python -m zipapp myapp -m "myapp:main"
   $ python myapp.pyz
   <output from myapp>


.. _zipapp-command-line-interface:

Giao diện dòng lệnh
-------------------

Khi được gọi như một chương trình từ dòng lệnh, biểu mẫu sau được sử dụng:

.. code-block:: shell-session

   $ python -m zipapp source [options]

Nếu *source* là một thư mục, thao tác này sẽ tạo một archive từ nội dung của *source*. Nếu *source* là một tệp, tệp đó phải là một archive và sẽ được sao chép vào archive đích (hoặc nội dung dòng shebang của tệp sẽ được hiển thị nếu chỉ định tùy chọn --info).

Các tùy chọn sau được hỗ trợ:

.. program:: zipapp

.. option:: -o <output>, --output=<output>

   Ghi đầu ra vào một tệp có tên *output*. Nếu không chỉ định tùy chọn này, tên tệp đầu ra sẽ giống với *source* đầu vào, với phần mở rộng ``.pyz`` được thêm vào. Nếu cung cấp tên tệp rõ ràng, tên đó sẽ được sử dụng nguyên trạng (vì vậy cần thêm phần mở rộng ``.pyz`` nếu cần).

   Phải chỉ định tên tệp đầu ra nếu *source* là một archive (và trong trường hợp đó, *output* không được trùng với *source*).

.. option:: -p <interpreter>, --python=<interpreter>

   Thêm một dòng ``#!`` vào archive, chỉ định *interpreter* làm lệnh cần chạy. Ngoài ra, trên POSIX, đặt archive ở trạng thái có thể thực thi. Theo mặc định, không ghi dòng ``#!`` nào và không đặt tệp ở trạng thái có thể thực thi.

.. option:: -m <mainfn>, --main=<mainfn>

   Tạo một tệp ``__main__.py`` trong archive để thực thi *mainfn*. Đối số *mainfn* phải có dạng "pkg.mod:fn", trong đó "pkg.mod" là một package/module trong archive và "fn" là một callable trong module đã cho. Tệp ``__main__.py`` sẽ thực thi callable đó.

   Không thể chỉ định :option:`--main` khi sao chép archive.

.. option:: -c, --compress

   Nén các tệp bằng phương thức deflate, làm giảm kích thước tệp đầu ra. Theo mặc định, các tệp được lưu trong archive mà không nén.

   :option:`--compress` không có tác dụng khi sao chép archive.

   .. versionadded:: 3.7

.. option:: --info

   Hiển thị interpreter được nhúng trong archive cho mục đích chẩn đoán. Trong trường hợp này, mọi tùy chọn khác đều bị bỏ qua và SOURCE phải là một archive, không phải một thư mục.

.. option:: -h, --help

   In thông báo sử dụng ngắn gọn rồi thoát.


.. _zipapp-python-api:

Python API
----------

Mô-đun định nghĩa hai hàm tiện ích:


.. function:: create_archive(source, target=None, interpreter=None, main=None, filter=None, compressed=False)

   Tạo một kho lưu trữ ứng dụng từ *source*. Nguồn có thể là một trong các loại sau:

   * Tên của một thư mục hoặc một :term:`path-like object` trỏ đến một thư mục; trong trường hợp đó, một kho lưu trữ ứng dụng mới sẽ được tạo từ nội dung của thư mục đó.
   * Tên của một tệp kho lưu trữ ứng dụng hiện có hoặc một :term:`path-like object` trỏ đến tệp đó; trong trường hợp đó, tệp sẽ được sao chép vào đích và được sửa đổi để phản ánh giá trị được cung cấp cho đối số *interpreter*. Tên tệp phải bao gồm phần mở rộng ``.pyz``, nếu cần.
   * Một đối tượng tệp được mở để đọc ở chế độ byte. Nội dung của tệp phải là một kho lưu trữ ứng dụng và đối tượng tệp được giả định đang ở đầu kho lưu trữ.

   Đối số *target* xác định nơi kho lưu trữ kết quả sẽ được ghi:

   * Nếu đó là tên tệp hoặc một :term:`path-like object`, kho lưu trữ sẽ được ghi vào tệp đó.
   * Nếu đó là một đối tượng tệp đang mở, kho lưu trữ sẽ được ghi vào đối tượng tệp đó, và đối tượng này phải được mở để ghi ở chế độ byte.
   * Nếu target bị bỏ qua (hoặc ``None``), source phải là một thư mục và target sẽ là một tệp có cùng tên với source, được thêm phần mở rộng ``.pyz``.

   Đối số *interpreter* chỉ định tên của Python interpreter mà archive sẽ được thực thi bằng nó. Đối số này được ghi dưới dạng một dòng "shebang" ở đầu archive. Trên POSIX, dòng này sẽ được hệ điều hành diễn giải, còn trên Windows, dòng này sẽ được Python launcher xử lý. Việc bỏ qua *interpreter* khiến không có dòng shebang nào được ghi. Nếu chỉ định một interpreter và target là tên tệp, bit thực thi của tệp target sẽ được thiết lập.

   Đối số *main* chỉ định tên của một callable được dùng làm chương trình chính cho archive. Đối số này chỉ có thể được chỉ định nếu source là một thư mục và source chưa chứa tệp ``__main__.py``. Đối số *main* phải có dạng "pkg.module:callable", và archive sẽ được chạy bằng cách import "pkg.module" rồi thực thi callable đã cho mà không có đối số. Sẽ xảy ra lỗi nếu bỏ qua *main* khi source là một thư mục và không chứa tệp ``__main__.py``, vì khi đó archive kết quả sẽ không thể thực thi.

   Đối số tùy chọn *filter* chỉ định một hàm callback nhận một đối tượng Path biểu diễn đường dẫn đến tệp đang được thêm (tương đối với thư mục source). Hàm này phải trả về ``True`` nếu cần thêm tệp.

   Đối số tùy chọn *compressed* xác định liệu các tệp có được nén hay không. Nếu được đặt thành ``True``, các tệp trong archive sẽ được nén bằng phương thức deflate; nếu không, các tệp sẽ được lưu trữ không nén. Đối số này không có tác dụng khi sao chép một archive hiện có.

   Nếu một đối tượng tệp được chỉ định cho *source* hoặc *target*, người gọi có trách nhiệm đóng đối tượng đó sau khi gọi create_archive.

   Khi sao chép một archive hiện có, các đối tượng tệp được cung cấp chỉ cần có các phương thức ``read`` và ``readline``, hoặc ``write``. Khi tạo archive từ một thư mục, nếu đích là một đối tượng tệp thì đối tượng đó sẽ được truyền cho lớp ``zipfile.ZipFile``, và phải cung cấp các phương thức mà lớp đó cần.

   .. versionchanged:: 3.7
      Đã thêm các tham số *filter* và *compressed*.

.. function:: get_interpreter(archive)

   Trả về trình thông dịch được chỉ định trong dòng ``#!`` ở đầu archive. Nếu không có dòng ``#!``, trả về :const:`None`. Đối số *archive* có thể là tên tệp hoặc một đối tượng giống tệp được mở để đọc ở chế độ byte. Đối số này được giả định đang ở đầu archive.


.. _zipapp-examples:

Ví dụ
-----

Đóng gói một thư mục vào archive rồi chạy archive đó.

.. code-block:: shell-session

   $ python -m zipapp myapp
   $ python myapp.pyz
   <output from myapp>

Có thể thực hiện tương tự bằng hàm :func:`create_archive`::

   >>> import zipapp
   >>> zipapp.create_archive('myapp', 'myapp.pyz')

Để ứng dụng có thể thực thi trực tiếp trên POSIX, hãy chỉ định trình thông dịch cần sử dụng.

.. code-block:: shell-session

   $ python -m zipapp myapp -p "/usr/bin/env python"
   $ ./myapp.pyz
   <output from myapp>

Để thay thế dòng shebang trong một archive hiện có, hãy tạo một archive đã sửa đổi bằng hàm :func:`create_archive`::

   >>> import zipapp
   >>> zipapp.create_archive('old_archive.pyz', 'new_archive.pyz', '/usr/bin/python3')

Để cập nhật tệp tại chỗ, hãy thực hiện việc thay thế trong bộ nhớ bằng một đối tượng :class:`~io.BytesIO`, sau đó ghi đè lên tệp nguồn. Lưu ý rằng khi ghi đè tệp tại chỗ, có nguy cơ lỗi xảy ra và làm mất tệp gốc. Đoạn mã này không bảo vệ khỏi những lỗi như vậy, nhưng code production nên thực hiện việc đó. Ngoài ra, phương pháp này chỉ hoạt động nếu archive vừa với bộ nhớ::

   >>> import zipapp
   >>> import io
   >>> temp = io.BytesIO()
   >>> zipapp.create_archive('myapp.pyz', temp, '/usr/bin/python2')
   >>> with open('myapp.pyz', 'wb') as f:
   >>>     f.write(temp.getvalue())


.. _zipapp-specifying-the-interpreter:

Chỉ định Interpreter
--------------------

Lưu ý rằng nếu bạn chỉ định một interpreter rồi phân phối application archive của mình, bạn cần đảm bảo interpreter được sử dụng có tính portable. Python launcher cho Windows hỗ trợ hầu hết các dạng phổ biến của dòng ``#!`` POSIX, nhưng vẫn có những vấn đề khác cần cân nhắc:

* Nếu sử dụng "/usr/bin/env python" (hoặc các dạng khác của lệnh "python", chẳng hạn như "/usr/bin/python"), bạn cần cân nhắc rằng người dùng có thể có Python 2 hoặc Python 3 làm phiên bản mặc định, và viết code để hoạt động trên cả hai phiên bản.
* Nếu sử dụng một phiên bản cụ thể, chẳng hạn như "/usr/bin/env python3", application của bạn sẽ không hoạt động với những người dùng không có phiên bản đó. (Đây có thể là điều bạn muốn nếu bạn chưa làm cho code của mình tương thích với Python 2).
* Không có cách nào để chỉ định "python X.Y hoặc mới hơn", vì vậy hãy cẩn thận khi sử dụng một phiên bản chính xác như "/usr/bin/env python3.4", bởi bạn sẽ cần thay đổi dòng shebang cho người dùng Python 3.5 chẳng hạn.

Thông thường, bạn nên sử dụng "/usr/bin/env python2" hoặc "/usr/bin/env python3", tùy thuộc vào việc mã của bạn được viết cho Python 2 hay 3.


Tạo ứng dụng độc lập với zipapp
-------------------------------

Bằng cách sử dụng module :mod:`!zipapp`, bạn có thể tạo các chương trình Python tự chứa, có thể phân phối cho người dùng cuối, những người chỉ cần cài đặt một phiên bản Python phù hợp trên hệ thống của họ. Điều cốt lõi là đóng gói tất cả dependency của ứng dụng vào archive cùng với mã ứng dụng.

Các bước để tạo một archive độc lập như sau:

1. Tạo ứng dụng của bạn trong một thư mục như bình thường, để bạn có một thư mục ``myapp`` chứa tệp ``__main__.py`` cùng mọi mã hỗ trợ cho ứng dụng.

2. Cài đặt tất cả dependency của ứng dụng vào thư mục ``myapp`` bằng pip:

   .. code-block:: shell-session

      $ python -m pip install -r requirements.txt --target myapp

   (giả định rằng bạn có các yêu cầu của dự án trong tệp ``requirements.txt`` - nếu không, bạn chỉ cần liệt kê thủ công các dependency trên dòng lệnh pip).

3. Đóng gói ứng dụng bằng:

   .. code-block:: shell-session

      $ python -m zipapp -p "interpreter" myapp

Thao tác này sẽ tạo ra một tệp thực thi độc lập, có thể chạy trên bất kỳ máy nào có sẵn trình thông dịch phù hợp. Xem :ref:`zipapp-specifying-the-interpreter` để biết chi tiết. Bạn có thể phân phối tệp này cho người dùng dưới dạng một tệp duy nhất.

Trên Unix, tệp ``myapp.pyz`` có thể thực thi ngay. Bạn có thể đổi tên tệp để xóa phần mở rộng ``.pyz`` nếu muốn có tên lệnh "thuần túy". Trên Windows, tệp ``myapp.pyz[w]`` có thể thực thi vì trình thông dịch Python đăng ký các phần mở rộng tệp ``.pyz`` và ``.pyzw`` khi được cài đặt.


Lưu ý
~~~~~

Nếu ứng dụng của bạn phụ thuộc vào một package có chứa phần mở rộng C, package đó không thể chạy từ tệp zip (đây là một hạn chế của hệ điều hành, vì mã thực thi phải có trong hệ thống tệp để bộ nạp của hệ điều hành tải nó). Trong trường hợp này, bạn có thể loại trừ phần phụ thuộc đó khỏi zipfile, rồi yêu cầu người dùng cài đặt nó hoặc phân phối nó cùng với zipfile và thêm mã vào ``__main__.py`` để đưa thư mục chứa module đã giải nén vào ``sys.path``. Khi đó, bạn cần bảo đảm phân phối các binary phù hợp cho (các) kiến trúc đích của mình (và có thể chọn đúng phiên bản để thêm vào ``sys.path`` tại runtime, dựa trên máy của người dùng).


Định dạng Lưu trữ Ứng dụng Zip của Python
-----------------------------------------

Python có thể thực thi các tệp zip chứa tệp ``__main__.py`` kể từ phiên bản 2.6. Để được Python thực thi, một application archive chỉ cần là một tệp zip tiêu chuẩn chứa tệp ``__main__.py``, tệp này sẽ được chạy làm entry point của ứng dụng. Như thường lệ đối với mọi script Python, thư mục cha của script (trong trường hợp này là tệp zip) sẽ được đặt vào
:data:`sys.path` và do đó các module khác có thể được import từ tệp zip.

Định dạng tệp zip cho phép thêm tùy ý dữ liệu vào trước một tệp zip. Định dạng ứng dụng zip sử dụng khả năng này để thêm một dòng "shebang" POSIX chuẩn vào tệp (``#!/path/to/interpreter``).

Về mặt hình thức, định dạng ứng dụng zip của Python là:

1. Một dòng shebang tùy chọn, chứa các ký tự ``b'#!'`` theo sau là tên trình thông dịch, rồi đến ký tự xuống dòng (``b'\n'``). Tên trình thông dịch có thể là bất kỳ tên nào được hệ điều hành chấp nhận khi xử lý "shebang", hoặc được Python launcher trên Windows chấp nhận. Trình thông dịch phải được mã hóa bằng UTF-8 trên Windows và bằng :func:`sys.getfilesystemencoding` trên POSIX.
2. Dữ liệu zipfile chuẩn, được tạo bởi module :mod:`zipfile`. Nội dung zipfile *phải* bao gồm một tệp có tên ``__main__.py`` (tệp này phải nằm ở "gốc" của zipfile, tức là không được nằm trong thư mục con). Dữ liệu zipfile có thể được nén hoặc không nén.

Nếu một application archive có dòng shebang, nó có thể được đặt bit thực thi trên các hệ thống POSIX, cho phép thực thi trực tiếp.

Không bắt buộc phải sử dụng các công cụ trong module này để tạo application archive; module này chỉ nhằm mang lại sự tiện lợi, nhưng Python chấp nhận các archive ở định dạng nêu trên được tạo bằng bất kỳ phương thức nào.

