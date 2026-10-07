:mod:`!email.iterators`: Bộ lặp
-------------------------------

.. module:: email.iterators
   :synopsis: Lặp qua cây đối tượng message.

**Mã nguồn:** :source:`Lib/email/iterators.py`

--------------

Việc lặp qua cây đối tượng message khá dễ dàng với
:meth:`Message.walk <email.message.Message.walk>` phương thức.
Mô-đun :mod:`!email.iterators` cung cấp một số cách lặp ở cấp cao hữu ích trên các cây đối tượng message.


.. function:: body_line_iterator(msg, decode=False)

   Cách này lặp qua tất cả payload trong mọi phần con của *msg*, trả về các payload dạng chuỗi theo từng dòng.  Cách này bỏ qua tất cả header của các phần con, đồng thời bỏ qua mọi phần con có payload không phải là một chuỗi Python.  Cách này tương đương ở một mức độ nhất định với việc đọc biểu diễn văn bản phẳng của message từ một tệp bằng :meth:`~io.TextIOBase.readline`, bỏ qua tất cả header nằm xen giữa.

   Tùy chọn *decode* được truyền tiếp đến :meth:`Message.get_payload <email.message.Message.get_payload>`.


.. function:: typed_subpart_iterator(msg, maintype='text', subtype=None)

   Hàm này lặp qua tất cả các phần con của *msg*, chỉ trả về những phần con khớp với kiểu MIME được chỉ định bởi *maintype* và *subtype*.

   Lưu ý rằng *subtype* là tùy chọn; nếu bỏ qua, việc khớp kiểu MIME của phần con chỉ được thực hiện với kiểu chính. *maintype* cũng là tùy chọn; giá trị mặc định là
   :mimetype:`text`.

   Do đó, theo mặc định, :func:`typed_subpart_iterator` trả về mỗi phần con có kiểu MIME là :mimetype:`text/\*`.


Hàm sau đây được bổ sung như một công cụ hữu ích để gỡ lỗi. Không nên *not* coi hàm này là một phần của interface công khai được hỗ trợ của package.

.. function:: _structure(msg, fp=None, level=0, include_default=False)

   In ra biểu diễn thụt lề của các kiểu nội dung trong cấu trúc đối tượng message. Ví dụ:

   .. testsetup::

      import email
      from email.iterators import _structure
      somefile = open('../Lib/test/test_email/data/msg_02.txt')

   .. doctest::

      >>> msg = email.message_from_file(somefile)
      >>> _structure(msg)
      multipart/mixed
          text/plain
          text/plain
          multipart/digest
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
              message/rfc822
                  text/plain
          text/plain

   .. testcleanup::

      somefile.close()

   *fp* tùy chọn là một đối tượng giống tệp để in kết quả ra. Đối tượng này phải phù hợp với hàm :func:`print` của Python. *level* được sử dụng nội bộ. Nếu *include_default* là true, hàm cũng in kiểu mặc định.
