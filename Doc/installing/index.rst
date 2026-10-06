.. highlight:: shell

.. _installing-index:

*************************
Cài đặt các mô-đun Python
*************************

Là một dự án phát triển mã nguồn mở phổ biến, Python có một cộng đồng năng động
gồm các cộng tác viên và người dùng hỗ trợ dự án. Họ cũng cung cấp phần mềm của
mình để các nhà phát triển Python khác sử dụng theo các điều khoản giấy phép
mã nguồn mở.

Điều này cho phép người dùng Python chia sẻ và hợp tác hiệu quả, hưởng lợi từ
các giải pháp mà người khác đã tạo ra cho những vấn đề phổ biến (và đôi khi cả
những vấn đề hiếm gặp!), đồng thời có thể đóng góp các giải pháp của riêng họ
vào kho dùng chung.

Hướng dẫn này trình bày phần cài đặt của quy trình. Để biết cách tạo và chia sẻ
các dự án Python của riêng bạn, hãy xem
`Python packaging user guide`_.

.. _Python Packaging User Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/

.. note::

   Người dùng doanh nghiệp và các tổ chức khác cần lưu ý rằng nhiều tổ chức có
   chính sách riêng về việc sử dụng và đóng góp cho phần mềm mã nguồn mở. Hãy
   cân nhắc các chính sách đó khi sử dụng công cụ phân phối và cài đặt đi kèm
   Python.


Các thuật ngữ chính
=========

* :program:`pip` là chương trình cài đặt được ưu tiên. Nó được bao gồm mặc định
  trong các trình cài đặt Python dạng nhị phân.
* *Môi trường ảo* là môi trường Python được cô lập một phần, cho phép cài đặt
  gói để dùng cho một ứng dụng cụ thể thay vì cài đặt trên toàn hệ thống.
* ``venv`` là công cụ chuẩn để tạo môi trường ảo. Theo mặc định, nó cài đặt
  :program:`pip` vào mọi môi trường ảo được tạo.
* ``virtualenv`` là một lựa chọn thay thế của bên thứ ba (và là tiền thân) cho
  ``venv``.
* `Python Package Index (PyPI) <https://pypi.org>`__ là kho công khai các gói
  theo giấy phép mã nguồn mở, sẵn có để những người dùng Python khác sử dụng.
* `Python Packaging Authority
  <https://www.pypa.io/>`__ là nhóm các nhà phát triển và tác giả tài liệu chịu
  trách nhiệm bảo trì, phát triển các công cụ đóng gói chuẩn cùng các tiêu chuẩn
  siêu dữ liệu và định dạng tệp liên quan. Họ duy trì nhiều công cụ, tài liệu và
  trình theo dõi vấn đề trên `GitHub <https://github.com/pypa>`__.

.. versionchanged:: 3.5
   Hiện nay, nên sử dụng ``venv`` để tạo môi trường ảo.

.. seealso::

   `Python Packaging User Guide: Creating and using virtual environments
   <https://packaging.python.org/installing/#creating-virtual-environments>`__


Cách dùng cơ bản
===========

Các công cụ đóng gói chuẩn đều được thiết kế để sử dụng từ dòng lệnh.

Lệnh sau sẽ cài đặt phiên bản mới nhất của một mô-đun và các phần phụ thuộc của
nó từ PyPI::

    python -m pip install SomePackage

.. note::

   Đối với người dùng POSIX (bao gồm người dùng macOS và Linux), các ví dụ trong
   hướng dẫn này giả định rằng bạn sử dụng :term:`môi trường ảo <virtual environment>`.

   Đối với người dùng Windows, các ví dụ trong hướng dẫn này giả định rằng bạn
   đã chọn tùy chọn điều chỉnh biến môi trường PATH của hệ thống khi cài đặt
   Python.

Cũng có thể chỉ định trực tiếp phiên bản chính xác hoặc tối thiểu trên dòng
lệnh. Khi dùng các toán tử so sánh như ``>``, ``<`` hoặc ký tự đặc biệt khác mà
shell sẽ diễn giải, tên gói và phiên bản cần được đặt trong dấu nháy kép::

    python -m pip install SomePackage==1.0.4    # phiên bản cụ thể
    python -m pip install "SomePackage>=1.0.4"  # phiên bản tối thiểu

Thông thường, nếu một mô-đun phù hợp đã được cài đặt thì việc cố cài lại sẽ
không có tác dụng. Bạn phải yêu cầu rõ ràng nếu muốn nâng cấp các mô-đun hiện
có::

    python -m pip install --upgrade SomePackage

Bạn có thể tìm thêm thông tin và tài nguyên về :program:`pip` cùng các khả năng
của nó trong `Hướng dẫn người dùng Python Packaging <https://packaging.python.org>`__.

Việc tạo môi trường ảo được thực hiện qua mô-đun :mod:`venv`. Để cài gói vào
một môi trường ảo đang hoạt động, hãy dùng các lệnh ở trên.

.. seealso::

    `Python Packaging User Guide: Installing Python Distribution Packages
    <https://packaging.python.org/installing/>`__


Làm thế nào để ...?
=============

Đây là các câu trả lời nhanh hoặc liên kết cho một số tác vụ thường gặp.

.. installing-per-user-installation:

... chỉ cài đặt gói cho người dùng hiện tại?
-----------------------------------------------

Truyền tùy chọn ``--user`` cho ``python -m pip install`` sẽ chỉ cài đặt gói cho
người dùng hiện tại, thay vì cho mọi người dùng trên hệ thống.


... cài đặt các gói Python khoa học?
---------------------------------------

Một số gói Python khoa học có phần phụ thuộc nhị phân phức tạp và hiện chưa dễ
cài đặt trực tiếp bằng :program:`pip`. Người dùng thường sẽ dễ cài đặt các gói
này bằng
`other means <https://packaging.python.org/science/>`__
thay vì cố cài đặt chúng bằng :program:`pip`.

.. seealso::

   `Python Packaging User Guide: Installing Scientific Packages
   <https://packaging.python.org/science/>`__


... làm việc với nhiều phiên bản Python được cài song song?
----------------------------------------------------------------

Trên Linux, macOS và các hệ thống POSIX khác, hãy dùng lệnh Python có chỉ định
phiên bản kết hợp với tùy chọn ``-m`` để chạy bản :program:`pip` phù hợp::

   python3    -m pip install SomePackage  # Python 3 mặc định
   python3.14 -m pip install SomePackage  # cụ thể là Python 3.14

Các lệnh :program:`pip` có phiên bản tương ứng cũng có thể khả dụng.

Trên Windows, hãy dùng trình khởi chạy Python :program:`py` kết hợp với tùy
chọn ``-m``::

   py -3    -m pip install SomePackage  # Python 3 mặc định
   py -3.14 -m pip install SomePackage  # cụ thể là Python 3.14

.. other questions:

   Khi phần Phát triển & Triển khai của PPUG được hoàn thiện, nên liên kết một
   số mục trong đó từ các câu hỏi mới ở đây (đáng chú ý nhất là nên có một câu
   hỏi về việc tránh phụ thuộc vào PyPI, liên kết đến
   https://packaging.python.org/en/latest/guides/index-mirrors-and-caches/)


Các vấn đề cài đặt thường gặp
==========================

Cài đặt vào Python hệ thống trên Linux
------------------------------------------

Trên các hệ thống Linux, một bản cài đặt Python thường được bao gồm trong bản
phân phối. Việc cài đặt vào bản Python này cần quyền root trên hệ thống và có
thể ảnh hưởng đến hoạt động của trình quản lý gói hệ thống cùng các thành phần
khác nếu một thành phần bị nâng cấp ngoài dự kiến bằng :program:`pip`.

Trên những hệ thống như vậy, thường tốt hơn khi dùng môi trường ảo hoặc cài đặt
theo từng người dùng khi cài gói bằng :program:`pip`.


Chưa cài đặt Pip
-----------------

:program:`pip` có thể không được cài đặt mặc định. Một cách khắc phục khả dĩ là::

    python -m ensurepip --default-pip

Ngoài ra còn có các tài nguyên khác về `cài đặt pip
<https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-pip-setuptools-and-wheel-are-up-to-date>`__.


Cài đặt phần mở rộng nhị phân
----------------------------

Trước đây Python phụ thuộc nhiều vào việc phân phối dựa trên mã nguồn, trong đó
người dùng cuối được kỳ vọng biên dịch các mô-đun mở rộng từ mã nguồn trong quá
trình cài đặt.

Kể từ khi định dạng wheel nhị phân ra đời và có thể phát hành wheel qua PyPI,
vấn đề này đang giảm bớt, vì người dùng ngày càng thường xuyên cài được các
phần mở rộng dựng sẵn thay vì phải tự xây dựng chúng.

Một số giải pháp để cài đặt `phần mềm khoa học
<https://packaging.python.org/science/>`__
chưa có sẵn dưới dạng tệp wheel dựng sẵn cũng có thể giúp lấy các phần mở rộng
nhị phân khác mà không cần tự xây dựng trên máy cục bộ.

.. seealso::

   `Python Packaging User Guide: Binary Extensions
   <https://packaging.python.org/extensions/>`__
