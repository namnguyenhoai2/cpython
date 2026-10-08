:mod:`!stringprep` --- Chuẩn bị chuỗi Internet
==============================================

.. module:: stringprep
   :synopsis: Chuẩn bị chuỗi theo RFC 3453

.. moduleauthor:: Martin v. Löwis <martin@v.loewis.de>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/stringprep.py`

--------------

Khi xác định các đối tượng (chẳng hạn như tên máy chủ) trên Internet, thường cần so sánh các định danh đó để xác định "bằng nhau". Cách thực hiện chính xác việc so sánh này có thể phụ thuộc vào miền ứng dụng, chẳng hạn như có phân biệt chữ hoa chữ thường hay không. Cũng có thể cần giới hạn các định danh được phép, chỉ cho phép những định danh gồm các ký tự "in được".

:rfc:`3454` định nghĩa một quy trình "chuẩn bị" các chuỗi Unicode trong các giao thức Internet. Trước khi truyền các chuỗi qua mạng, chúng được xử lý bằng quy trình chuẩn bị, sau đó có một dạng chuẩn hóa nhất định. RFC định nghĩa một tập hợp các bảng, có thể kết hợp thành các profile. Mỗi profile phải định nghĩa những bảng mà nó sử dụng và những phần tùy chọn nào khác của quy trình ``stringprep`` thuộc về profile đó. Một ví dụ về profile ``stringprep`` là ``nameprep``, được sử dụng cho các tên miền quốc tế hóa.

Module :mod:`!stringprep` chỉ cung cấp các bảng từ :rfc:`3454`. Vì các bảng này sẽ rất lớn nếu biểu diễn dưới dạng dictionary hoặc list, module sử dụng cơ sở dữ liệu ký tự Unicode ở bên trong. Chính mã nguồn của module được tạo bằng tiện ích ``mkstringprep.py``.

Do đó, các bảng này được cung cấp dưới dạng hàm, không phải cấu trúc dữ liệu. RFC có hai loại bảng: tập hợp và ánh xạ. Đối với một tập hợp,
:mod:`!stringprep` cung cấp “hàm đặc trưng”, tức là một hàm trả về ``True`` nếu tham số thuộc tập hợp. Đối với các ánh xạ, nó cung cấp hàm ánh xạ: khi nhận khóa, hàm trả về giá trị tương ứng. Dưới đây là danh sách tất cả các hàm có trong module.


.. function:: in_table_a1(code)

   Xác định xem *code* có nằm trong bảngA.1 (Các điểm mã chưa được gán trong Unicode 3.2) hay không.


.. function:: in_table_b1(code)

   Xác định xem *code* có nằm trong bảngB.1 (Thường được ánh xạ thành không có gì) hay không.


.. function:: map_table_b2(code)

   Trả về giá trị được ánh xạ cho *code* theo bảngB.2 (Ánh xạ để folding chữ hoa chữ thường được sử dụng cùng với NFKC).


.. function:: map_table_b3(code)

   Trả về giá trị được ánh xạ cho *code* theo bảngB.3 (Ánh xạ để folding chữ hoa chữ thường được sử dụng mà không chuẩn hóa).


.. function:: in_table_c11(code)

   Xác định xem *code* có nằm trong bảngC.1.1  (Các ký tự khoảng trắng ASCII) hay không.


.. function:: in_table_c12(code)

   Xác định xem *code* có nằm trong bảngC.1.2  (Các ký tự khoảng trắng không phải ASCII) hay không.


.. function:: in_table_c11_c12(code)

   Xác định xem *code* có nằm trong tableC.1 (Ký tự khoảng trắng, hợp của C.1.1 và C.1.2) hay không.


.. function:: in_table_c21(code)

   Xác định xem *code* có nằm trong tableC.2.1 (Các ký tự điều khiển ASCII) hay không.


.. function:: in_table_c22(code)

   Xác định xem *code* có nằm trong tableC.2.2 (Các ký tự điều khiển không phải ASCII) hay không.


.. function:: in_table_c21_c22(code)

   Xác định xem *code* có nằm trong tableC.2 (Các ký tự điều khiển, hợp của C.2.1 và C.2.2) hay không.


.. function:: in_table_c3(code)

   Xác định xem *code* có nằm trong tableC.3 (Vùng sử dụng riêng) hay không.


.. function:: in_table_c4(code)

   Xác định xem *code* có nằm trong tableC.4 (Các điểm mã không phải ký tự) hay không.


.. function:: in_table_c5(code)

   Xác định xem *code* có nằm trong tableC.5 (Các mã surrogate) hay không.


.. function:: in_table_c6(code)

   Xác định xem *code* có nằm trong tableC.6 (Không phù hợp với văn bản thuần túy).


.. function:: in_table_c7(code)

   Xác định xem *code* có nằm trong tableC.7 (Không phù hợp với biểu diễn chuẩn tắc).


.. function:: in_table_c8(code)

   Xác định xem *code* có nằm trong tableC.8 (Thay đổi thuộc tính hiển thị hoặc đã lỗi thời).


.. function:: in_table_c9(code)

   Xác định xem *code* có nằm trong tableC.9 (Ký tự gắn thẻ).


.. function:: in_table_d1(code)

   Xác định xem *code* có nằm trong tableD.1 (Các ký tự có thuộc tính hai chiều "R" hoặc "AL").


.. function:: in_table_d2(code)

   Xác định xem *code* có nằm trong tableD.2 (Các ký tự có thuộc tính hai chiều "L").

