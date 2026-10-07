.. _python_2.3_mro:

Thứ tự phân giải phương thức trong Python 2.3
=============================================

.. note::

   Đây là một tài liệu lịch sử, được cung cấp dưới dạng phụ lục cho tài liệu chính thức. Thứ tự phân giải phương thức được thảo luận ở đây đã được *giới thiệu* trong Python 2.3, nhưng vẫn được sử dụng trong các phiên bản sau này -- bao gồm cả Python 3.

Bởi `Michele Simionato <https://github.com/micheles>`__.

:Abstract:

  *Tài liệu này dành cho các lập trình viên Python muốn hiểu về Thứ tự phân giải phương thức C3 được sử dụng trong Python 2.3. Mặc dù không dành cho người mới bắt đầu, tài liệu khá giàu tính sư phạm với nhiều ví dụ được giải thích chi tiết. Tôi không biết có tài liệu nào khác được công khai với cùng phạm vi như vậy, vì thế tài liệu này sẽ hữu ích.*

Tuyên bố miễn trừ trách nhiệm:

   *Tôi tặng tài liệu này cho Python Software Foundation theo giấy phép Python 2.3. Như thường lệ trong những trường hợp này, tôi cảnh báo người đọc rằng những điều sau đây* sẽ *được cho là đúng, nhưng tôi không đưa ra bất kỳ bảo đảm nào. Hãy tự chịu mọi rủi ro và hậu quả khi sử dụng tài liệu này!*

Lời cảm ơn:

   *Tất cả những người trong mailing list Python đã gửi lời ủng hộ tôi. Paul Foley, người đã chỉ ra nhiều điểm chưa chính xác và khiến tôi bổ sung phần về thứ tự ưu tiên cục bộ. David Goodger đã giúp tôi định dạng bằng reStructuredText. David Mertz đã giúp tôi biên tập. Cuối cùng là Guido van Rossum, người đã nhiệt tình bổ sung tài liệu này vào trang chủ chính thức của Python 2.3.*

Phần mở đầu
-----------

                *Hạnh phúc thay người có thể hiểu được nguyên nhân của sự vật* -- Virgilius

Mọi chuyện bắt đầu từ một bài đăng của Samuele Pedroni trên mailing list dành cho các nhà phát triển Python [#]_. Trong bài đăng đó, Samuele chỉ ra rằng thứ tự phân giải phương thức của Python 2.2 không đơn điệu và đề xuất thay thế nó bằng thứ tự phân giải phương thức C3. Guido đồng ý với các lập luận của ông, vì vậy Python 2.3 hiện sử dụng C3. Bản thân phương thức C3 không liên quan gì đến Python, vì nó được phát minh bởi những người làm việc với Dylan và được mô tả trong một bài viết dành cho những người sử dụng Lisp [#]_. Bài viết này trình bày một thảo luận (hy vọng là dễ đọc) về thuật toán C3 dành cho các Pythonista muốn hiểu lý do của thay đổi này.

Trước hết, tôi xin lưu ý rằng những điều tôi sắp trình bày chỉ áp dụng cho *các lớp kiểu mới* được giới thiệu trong Python 2.2: *các lớp kiểu cũ* vẫn giữ thứ tự phân giải phương thức cũ, theo chiều sâu rồi từ trái sang phải. Vì vậy, không có mã cũ nào dành cho các lớp kiểu cũ bị phá vỡ; và ngay cả khi về nguyên tắc mã dành cho các lớp kiểu mới của Python 2.2 có thể bị phá vỡ, trên thực tế các trường hợp mà thứ tự phân giải C3 khác với thứ tự phân giải phương thức của Python 2.2 hiếm đến mức không dự kiến có sự phá vỡ mã thực sự nào. Vì vậy:

   *Đừng sợ!*

Hơn nữa, trừ khi bạn sử dụng nhiều kế thừa ở mức độ lớn và có các hệ phân cấp không tầm thường, bạn không cần hiểu thuật toán C3 và có thể dễ dàng bỏ qua bài viết này. Mặt khác, nếu bạn thực sự muốn biết cơ chế hoạt động của nhiều kế thừa, thì bài viết này dành cho bạn. Tin tốt là mọi thứ không phức tạp như bạn có thể nghĩ.

Hãy bắt đầu với một số định nghĩa cơ bản.

1) Với một lớp C trong một hệ phân cấp đa kế thừa phức tạp, việc xác định thứ tự các phương thức bị ghi đè, tức là xác định thứ tự các lớp tổ tiên của C, không phải là một nhiệm vụ đơn giản.

2) Danh sách các lớp tổ tiên của một lớp C, bao gồm chính lớp đó, được sắp xếp từ lớp tổ tiên gần nhất đến xa nhất, được gọi là danh sách ưu tiên lớp hoặc *phép tuyến tính hóa* của C.

3) *Thứ tự phân giải phương thức* (MRO) là tập hợp các quy tắc dùng để xây dựng phép tuyến tính hóa. Trong tài liệu Python, thành ngữ "MRO của C" cũng được dùng như từ đồng nghĩa với phép tuyến tính hóa của lớp C.

4) Chẳng hạn, trong trường hợp hệ phân cấp kế thừa đơn, nếu C là lớp con của C1, còn C1 là lớp con của C2, thì phép tuyến tính hóa của C đơn giản là danh sách [C, C1 , C2]. Tuy nhiên, với các hệ phân cấp đa kế thừa, việc xây dựng phép tuyến tính hóa phức tạp hơn, vì khó xây dựng một phép tuyến tính hóa vừa tuân thủ *thứ tự ưu tiên cục bộ* vừa tuân thủ *tính đơn điệu*.

5) Tôi sẽ thảo luận về thứ tự ưu tiên cục bộ sau, nhưng có thể đưa ra định nghĩa về tính đơn điệu ở đây. Một MRO là đơn điệu khi điều sau đây đúng: *nếu C1 đứng trước C2 trong phép tuyến tính hóa của C, thì C1 đứng trước C2 trong phép tuyến tính hóa của mọi lớp con của C*. Nếu không, thao tác tưởng như vô hại là tạo một lớp mới có thể làm thay đổi thứ tự phân giải phương thức, có khả năng dẫn đến những lỗi rất khó nhận thấy. Các ví dụ về trường hợp này sẽ được trình bày sau.

6) Không phải mọi lớp đều cho phép xây dựng phép tuyến tính hóa. Trong các hệ phân cấp phức tạp, có những trường hợp không thể tạo ra một lớp sao cho phép tuyến tính hóa của nó tuân thủ tất cả các thuộc tính mong muốn.

Sau đây là một ví dụ về tình huống này. Hãy xét hệ phân cấp

  >>> O = object
  >>> class X(O): pass
  >>> class Y(O): pass
  >>> class A(X,Y): pass
  >>> class B(Y,X): pass

có thể được biểu diễn bằng đồ thị kế thừa sau đây, trong đó tôi ký hiệu lớp ``object`` bằng O; đây là điểm bắt đầu của mọi hệ phân cấp đối với các class kiểu mới:

 .. code-block:: text

          -----------
         |           |
         |    O      |
         |  /   \    |
          - X    Y  /
            |  / | /
            | /  |/
            A    B
            \   /
              ?

Trong trường hợp này, không thể suy dẫn một class mới C từ A và B, vì X đứng trước Y trong A, nhưng Y lại đứng trước X trong B; do đó, thứ tự phân giải phương thức trong C sẽ không rõ ràng.

Python 2.3 phát sinh một ngoại lệ trong tình huống này (TypeError:  MRO conflict among bases Y, X), ngăn lập trình viên thiếu thận trọng tạo ra các hệ phân cấp không rõ ràng.  Ngược lại, Python 2.2 không phát sinh ngoại lệ mà chọn một thứ tự *tùy tiện* (trong trường hợp này là CABXYO).

Thứ tự phân giải phương thức C3
-------------------------------

Trước tiên, hãy giới thiệu một vài ký hiệu đơn giản sẽ hữu ích cho phần thảo luận sau đây.  Tôi sẽ sử dụng ký hiệu rút gọn::

  C1 C2 ... CN

để biểu thị danh sách các class [C1, C2, ... , CN].

*head* của danh sách là phần tử đầu tiên của danh sách::

  head = C1

trong khi *tail* là phần còn lại của danh sách::

  tail = C2 ... CN.

Tôi cũng sẽ sử dụng ký hiệu::

  C + (C1 C2 ... CN) = C C1 C2 ... CN

để biểu thị tổng của các danh sách [C] + [C1, C2, ... ,CN].

Bây giờ tôi có thể giải thích cách MRO hoạt động trong Python 2.3.

Hãy xét một lớp C trong một hệ phân cấp đa kế thừa, trong đó C kế thừa từ các lớp cơ sở B1, B2, ...  , BN. Chúng ta muốn tính phép tuyến tính hóa L[C] của lớp C. Quy tắc như sau:

  *phép tuyến tính hóa của C là tổng của C với phép trộn các phép tuyến tính hóa của các lớp cha và danh sách các lớp cha.*

Trong ký hiệu tượng trưng::

   L[C(B1 ... BN)] = C + merge(L[B1] ... L[BN], B1 ... BN)

Cụ thể, nếu C là lớp ``object``, không có lớp cha nào, thì phép tuyến tính hóa là hiển nhiên::

       L[object] = object.

Tuy nhiên, nhìn chung, cần tính phép trộn theo quy tắc sau:

  *lấy phần tử đầu của danh sách đầu tiên, tức là L[B1][0]; nếu phần tử đầu này không nằm trong phần đuôi của bất kỳ danh sách nào khác, thì thêm nó vào phép tuyến tính hóa của C và xóa nó khỏi các danh sách trong phép trộn; nếu không, chuyển sang phần tử đầu của danh sách tiếp theo và lấy nó nếu đó là một phần tử đầu hợp lệ. Sau đó lặp lại thao tác này cho đến khi tất cả các lớp được loại bỏ hoặc không thể tìm thấy phần tử đầu hợp lệ nào. Trong trường hợp này, không thể xây dựng phép trộn; Python 2.3 sẽ từ chối tạo lớp C và phát sinh một ngoại lệ.*

Quy tắc này đảm bảo rằng phép trộn *bảo toàn* thứ tự, nếu có thể bảo toàn thứ tự. Mặt khác, nếu không thể bảo toàn thứ tự (như trong ví dụ về sự bất đồng nghiêm trọng về thứ tự đã thảo luận ở trên), thì không thể tính được phép trộn.

Việc tính phép trộn là hiển nhiên nếu C chỉ có một lớp cha (kế thừa đơn); trong trường hợp này::

       L[C(B)] = C + merge(L[B],B) = C + L[B]

Tuy nhiên, trong trường hợp đa kế thừa, mọi thứ phức tạp hơn và tôi không nghĩ bạn có thể hiểu quy tắc này nếu không có vài ví dụ ;-)

Ví dụ
-----

Ví dụ đầu tiên. Xét hệ phân cấp sau:

  >>> O = object
  >>> class F(O): pass
  >>> class E(O): pass
  >>> class D(O): pass
  >>> class C(D,F): pass
  >>> class B(D,E): pass
  >>> class A(B,C): pass

Trong trường hợp này, đồ thị kế thừa có thể được vẽ như sau:

 .. code-block:: text

                            6
                           ---
  Level 3                 | O |                  (more general)
                        /  ---  \
                       /    |    \                      |
                      /     |     \                     |
                     /      |      \                    |
                    ---    ---    ---                   |
  Level 2        3 | D | 4| E |  | F | 5                |
                    ---    ---    ---                   |
                     \  \ _ /       |                   |
                      \    / \ _    |                   |
                       \  /      \  |                   |
                        ---      ---                    |
  Level 1            1 | B |    | C | 2                 |
                        ---      ---                    |
                          \      /                      |
                           \    /                      \ /
                             ---
  Level 0                 0 | A |                (more specialized)
                             ---


Các phép tuyến tính hóa của O,D,E và F là hiển nhiên::

  L[O] = O
  L[D] = D O
  L[E] = E O
  L[F] = F O

Có thể tính phép tuyến tính hóa của B như sau::

  L[B] = B + merge(DO, EO, DE)

Ta thấy D là phần tử đầu tốt, do đó ta chọn nó và còn phải tính ``merge(O,EO,E)``.  Bây giờ O không phải là phần tử đầu tốt, vì nó nằm trong phần đuôi của dãy EO.  Trong trường hợp này, quy tắc yêu cầu chúng ta bỏ qua dãy tiếp theo.  Sau đó, ta thấy E là phần tử đầu tốt; ta chọn nó và còn phải tính ``merge(O,O)``, cho kết quả là O. Do đó::

  L[B] =  B D E O

Áp dụng quy trình tương tự, ta được::

  L[C] = C + merge(DO,FO,DF)
       = C + D + merge(O,FO,F)
       = C + D + F + merge(O,O)
       = C D F O

Bây giờ chúng ta có thể tính::

  L[A] = A + merge(BDEO,CDFO,BC)
       = A + B + merge(DEO,CDFO,C)
       = A + B + C + merge(DEO,DFO)
       = A + B + C + D + merge(EO,FO)
       = A + B + C + D + E + merge(O,FO)
       = A + B + C + D + E + F + merge(O,O)
       = A B C D E F O

Trong ví dụ này, linearization được sắp xếp khá hợp lý theo cấp độ kế thừa, theo nghĩa là các cấp thấp hơn (tức là các lớp chuyên biệt hơn) có độ ưu tiên cao hơn (xem đồ thị kế thừa). Tuy nhiên, đây không phải là trường hợp tổng quát.

Tôi để người đọc tự tính linearization cho ví dụ thứ hai của tôi:

  >>> O = object
  >>> class F(O): pass
  >>> class E(O): pass
  >>> class D(O): pass
  >>> class C(D,F): pass
  >>> class B(E,D): pass
  >>> class A(B,C): pass

Điểm khác biệt duy nhất so với ví dụ trước là thay đổi B(D,E) --> B(E,D); tuy nhiên, ngay cả một sửa đổi nhỏ như vậy cũng làm thay đổi hoàn toàn thứ tự của hệ thống phân cấp:

 .. code-block:: text

                             6
                            ---
  Level 3                  | O |
                         /  ---  \
                        /    |    \
                       /     |     \
                      /      |      \
                    ---     ---    ---
  Level 2        2 | E | 4 | D |  | F | 5
                    ---     ---    ---
                     \      / \     /
                      \    /   \   /
                       \  /     \ /
                        ---     ---
  Level 1            1 | B |   | C | 3
                        ---     ---
                         \       /
                          \     /
                            ---
  Level 0                0 | A |
                            ---


Hãy lưu ý rằng lớp E, nằm ở cấp thứ hai của hệ thống phân cấp, đứng trước lớp C, nằm ở cấp thứ nhất của hệ thống phân cấp, tức là E chuyên biệt hơn C, dù nó nằm ở cấp cao hơn.

Một lập trình viên lười có thể lấy MRO trực tiếp từ Python 2.2, vì trong trường hợp này, nó trùng với linearization của Python 2.3. Chỉ cần gọi phương thức :meth:`~type.mro` của lớp A:

  >>> A.mro()  # doctest: +NORMALIZE_WHITESPACE
  [<class 'A'>, <class 'B'>, <class 'E'>,
  <class 'C'>, <class 'D'>, <class 'F'>,
  <class 'object'>]

Cuối cùng, hãy xem xét ví dụ được thảo luận trong phần đầu tiên, liên quan đến một bất đồng nghiêm trọng về thứ tự. Trong trường hợp này, việc tính các phép tuyến tính hóa của O, X, Y, A và B rất đơn giản:

 .. code-block:: text

  L[O] = 0
  L[X] = X O
  L[Y] = Y O
  L[A] = A X Y O
  L[B] = B Y X O

Tuy nhiên, không thể tính phép tuyến tính hóa cho một lớp C kế thừa từ A và B::

  L[C] = C + merge(AXYO, BYXO, AB)
       = C + A + merge(XYO, BYXO, B)
       = C + A + B + merge(XYO, YXO)

Tại thời điểm này, chúng ta không thể hợp nhất các danh sách XYO và YXO, vì X nằm ở phần đuôi của YXO trong khi Y nằm ở phần đuôi của XYO: do đó không có phần tử đầu phù hợp và thuật toán C3 dừng lại. Python 2.3 phát sinh lỗi và từ chối tạo lớp C.

Thứ tự phân giải phương thức không hợp lệ
-----------------------------------------

Một MRO là *không hợp lệ* khi nó vi phạm các thuộc tính nền tảng như thứ tự ưu tiên cục bộ và tính đơn điệu. Trong phần này, tôi sẽ chỉ ra rằng cả MRO của các lớp classic và MRO của các lớp new-style trong Python 2.2 đều không hợp lệ.

Bắt đầu với thứ tự ưu tiên cục bộ sẽ dễ hơn. Hãy xem xét ví dụ sau:

  >>> F=type('Food',(),{'remember2buy':'spam'})
  >>> E=type('Eggs',(F,),{'remember2buy':'eggs'})
  >>> G=type('GoodFood',(F,E),{}) # trong Python 2.3, đây là lỗi!  # doctest: +SKIP

với sơ đồ kế thừa

 .. code-block:: text

                O
                |
   (buy spam)   F
                | \
                | E   (buy eggs)
                | /
                G

         (buy eggs or spam ?)


Ta thấy rằng class G kế thừa từ F và E, trong đó F *before* E: do đó, ta sẽ mong đợi thuộc tính *G.remember2buy* được kế thừa bởi *F.remember2buy* chứ không phải bởi *E.remember2buy*: tuy nhiên Python 2.2 cho kết quả

  >>> G.remember2buy  # doctest: +SKIP
  'eggs'

Đây là sự phá vỡ thứ tự ưu tiên cục bộ, vì thứ tự trong danh sách ưu tiên cục bộ, tức danh sách các lớp cha của G, không được giữ nguyên trong phép tuyến tính hóa G của Python 2.2::

  L[G,P22]= G E F object   # F *follows* E

Có thể lập luận rằng lý do F đứng sau E trong phép tuyến tính hóa của Python 2.2 là F ít chuyên biệt hơn E, vì F là superclass của E; tuy nhiên, việc phá vỡ thứ tự ưu tiên cục bộ khá phản trực giác và dễ gây lỗi. Điều này đặc biệt đúng vì đây là một điểm khác biệt so với các class kiểu cũ:

  >>> class F: remember2buy='spam'
  >>> class E(F): remember2buy='eggs'
  >>> class G(F,E): pass  # doctest: +SKIP
  >>> G.remember2buy  # doctest: +SKIP
  'spam'

Trong trường hợp này, MRO là GFEF và thứ tự ưu tiên cục bộ được bảo toàn.

Theo quy tắc chung, nên tránh các hệ phân cấp như trên, vì không rõ F nên override E hay ngược lại. Python 2.3 giải quyết sự mơ hồ này bằng cách phát sinh một exception khi tạo class G, qua đó ngăn lập trình viên tạo ra các hệ phân cấp mơ hồ. Lý do là thuật toán C3 không thể thực hiện phép trộn khi::

   merge(FO,EFO,FE)

không thể tính toán được, vì F nằm ở cuối EFO còn E nằm ở cuối FE.

Giải pháp thực sự là thiết kế một hệ phân cấp không mơ hồ, tức là cho G kế thừa từ E và F (lớp cụ thể hơn đứng trước), thay vì từ F và E; trong trường hợp này, MRO chắc chắn là GEF.

 .. code-block:: text

                O
                |
                F (spam)
              / |
     (eggs)   E |
              \ |
                G
                  (eggs, no doubt)


Python 2.3 buộc lập trình viên phải viết các hệ phân cấp tốt (hoặc ít nhất là ít dễ gây lỗi hơn).

Nhân đây, tôi muốn chỉ ra rằng thuật toán của Python 2.3 đủ thông minh để nhận biết những lỗi rõ ràng, chẳng hạn như việc lặp lại các class trong danh sách các class cha:

  >>> class A(object): pass
  >>> class C(A,A): pass # lỗi
  Traceback (most recent call last):
    File "<stdin>", line 1, in ?
  TypeError: duplicate base class A

Trong tình huống này, Python 2.2 (cả đối với các lớp kiểu cũ và các lớp kiểu mới) sẽ không phát sinh ngoại lệ nào.

Cuối cùng, tôi muốn chỉ ra hai bài học mà chúng ta đã rút ra từ ví dụ này:

1. mặc dù có tên như vậy, MRO xác định thứ tự phân giải của các thuộc tính, không chỉ các phương thức;

2. món ăn mặc định của các Pythonista là spam !  (nhưng bạn đã biết điều đó rồi ;-)

Sau khi đã thảo luận về vấn đề thứ tự ưu tiên cục bộ, bây giờ hãy xem xét vấn đề tính đơn điệu. Mục tiêu của tôi là chỉ ra rằng cả MRO của các lớp kiểu cũ lẫn MRO của các lớp kiểu mới trong Python 2.2 đều không đơn điệu.

Để chứng minh rằng MRO của các lớp kiểu cũ không đơn điệu thì khá đơn giản, chỉ cần xem sơ đồ hình thoi:

 .. code-block:: text


                   C
                  / \
                 /   \
                A     B
                 \   /
                  \ /
                   D

Ta có thể dễ dàng nhận ra sự không nhất quán::

  L[B,P21] = B C        # B đứng trước C: các phương thức của B được ưu tiên
  L[D,P21] = D A C B C  # B đứng sau C: các phương thức của C được ưu tiên!

Mặt khác, không có vấn đề gì với các MRO của Python 2.2 và 2.3; chúng cung cấp cho cả hai::

  L[D] = D A B C

Guido chỉ ra trong bài tiểu luận [#]_ của mình rằng MRO cổ điển trên thực tế không quá tệ, vì thông thường ta có thể tránh các hình thoi đối với các class cổ điển. Nhưng mọi class kiểu mới đều kế thừa từ ``object``, do đó các hình thoi là không thể tránh khỏi và sự không nhất quán xuất hiện trong mọi đồ thị kế thừa đa cấp.

MRO của Python 2.2 khiến việc phá vỡ tính đơn điệu trở nên khó khăn, nhưng không phải là không thể. Ví dụ sau, ban đầu do Samuele Pedroni cung cấp, cho thấy MRO của Python 2.2 không đơn điệu:

  >>> class A(object): pass
  >>> class B(object): pass
  >>> class C(object): pass
  >>> class D(object): pass
  >>> class E(object): pass
  >>> class K1(A,B,C): pass
  >>> class K2(D,B,E): pass
  >>> class K3(D,A):   pass
  >>> class Z(K1,K2,K3): pass

Sau đây là các phép tuyến tính hóa theo MRO C3 (người đọc nên tự kiểm tra các phép tuyến tính hóa này như một bài tập và vẽ sơ đồ kế thừa ;-)::

  L[A] = A O
  L[B] = B O
  L[C] = C O
  L[D] = D O
  L[E] = E O
  L[K1]= K1 A B C O
  L[K2]= K2 D B E O
  L[K3]= K3 D A O
  L[Z] = Z K1 K2 K3 D A B C E O

Python 2.2 cho kết quả tuyến tính hóa hoàn toàn giống nhau đối với A, B, C, D, E, K1, K2 và K3, nhưng cho kết quả tuyến tính hóa khác đối với Z::

  L[Z,P22] = Z K1 K3 A K2 D B C E O

Rõ ràng phép tuyến tính hóa này là *sai*, vì A đứng trước D, trong khi trong phép tuyến tính hóa của K3, A đứng *sau* D. Nói cách khác, trong K3, các phương thức bắt nguồn từ D ghi đè các phương thức bắt nguồn từ A, nhưng trong Z, vốn vẫn là một lớp con của K3, các phương thức bắt nguồn từ A lại ghi đè các phương thức bắt nguồn từ D! Đây là hành vi vi phạm tính đơn điệu. Hơn nữa, phép tuyến tính hóa Z của Python 2.2 cũng không nhất quán với thứ tự ưu tiên cục bộ, vì danh sách ưu tiên cục bộ của lớp Z là [K1, K2, K3] (K2 đứng trước K3), trong khi trong phép tuyến tính hóa của Z, K2 *đứng sau* K3. Những vấn đề này giải thích tại sao quy tắc 2.2 đã bị loại bỏ để chuyển sang quy tắc C3.

Kết thúc
--------

Phần này dành cho độc giả thiếu kiên nhẫn, những người đã bỏ qua tất cả các phần trước và nhảy ngay đến cuối. Phần này cũng dành cho lập trình viên lười biếng, những người không muốn vận dụng trí óc. Cuối cùng, phần này dành cho lập trình viên có phần tự phụ; nếu không, họ đã chẳng đọc một bài viết về thứ tự phân giải phương thức C3 trong các hệ phân cấp đa kế thừa ;-) Ba đức tính này khi kết hợp với nhau (và *không* riêng lẻ) xứng đáng nhận một phần thưởng: phần thưởng là một script Python 2.2 ngắn gọn, cho phép bạn tính MRO 2.3 mà không gây rủi ro cho bộ não. Chỉ cần thay đổi dòng cuối cùng để thử các ví dụ khác nhau mà tôi đã thảo luận trong bài viết này.::

  #<mro.py>

  """C3 algorithm by Samuele Pedroni (with readability enhanced by me)."""

  class __metaclass__(type):
      "All classes are metamagically modified to be nicely printed"
      __repr__ = lambda cls: cls.__name__

  class ex_2:
      "Serious order disagreement" #Từ Guido
      class O: pass
      class X(O): pass
      class Y(O): pass
      class A(X,Y): pass
      class B(Y,X): pass
      try:
          class Z(A,B): pass #tạo Z(A,B) trong Python 2.2
      except TypeError:
          pass # Không thể tạo Z(A,B) trong Python 2.3

  class ex_5:
      "My first example"
      class O: pass
      class F(O): pass
      class E(O): pass
      class D(O): pass
      class C(D,F): pass
      class B(D,E): pass
      class A(B,C): pass

  class ex_6:
      "My second example"
      class O: pass
      class F(O): pass
      class E(O): pass
      class D(O): pass
      class C(D,F): pass
      class B(E,D): pass
      class A(B,C): pass

  class ex_9:
      "Difference between Python 2.2 MRO and C3" #Từ Samuele
      class O: pass
      class A(O): pass
      class B(O): pass
      class C(O): pass
      class D(O): pass
      class E(O): pass
      class K1(A,B,C): pass
      class K2(D,B,E): pass
      class K3(D,A): pass
      class Z(K1,K2,K3): pass

  def merge(seqs):
      print '\n\nCPL[%s]=%s' % (seqs[0][0],seqs),
      res = []; i=0
      while 1:
        nonemptyseqs=[seq for seq in seqs if seq]
        if not nonemptyseqs: return res
        i+=1; print '\n',i,'round: candidates...',
        for seq in nonemptyseqs: # tìm các ứng viên hợp nhất trong các đầu seq
            cand = seq[0]; print ' ',cand,
            nothead=[s for s in nonemptyseqs if cand in s[1:]]
            if nothead: cand=None #từ chối ứng viên
            else: break
        if not cand: raise "Inconsistent hierarchy"
        res.append(cand)
        for seq in nonemptyseqs: # xóa cand
            if seq[0] == cand: del seq[0]

  def mro(C):
      "Compute the class precedence list (mro) according to C3"
      return merge([[C]]+map(mro,C.__bases__)+[list(C.__bases__)])

  def print_mro(C):
      print '\nMRO[%s]=%s' % (C,mro(C))
      print '\nP22 MRO[%s]=%s' % (C,C.mro())

  print_mro(ex_9.Z)

  #</mro.py>

Vậy là hết,

                            Chúc bạn vui vẻ!


Tài nguyên
----------

.. [#] Chủ đề trên python-dev do Samuele Pedroni khởi xướng: https://mail.python.org/pipermail/python-dev/2002-October/029035.html

.. [#] Bài viết *Một phép tuyến tính hóa lớp cha đơn điệu cho Dylan*: https://doi.org/10.1145/236337.236343

.. [#] Bài tiểu luận của Guido van Rossum, *Hợp nhất các kiểu và lớp trong Python 2.2*: https://web.archive.org/web/20140210194412/http://www.python.org/download/releases/2.2.2/descrintro
