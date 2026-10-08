:mod:`!numbers` --- Các lớp cơ sở trừu tượng về số
==================================================

.. module:: numbers
   :synopsis: Các lớp cơ sở trừu tượng về số (Complex, Real, Integral, v.v.).

**Mã nguồn:** :source:`Lib/numbers.py`

--------------

Mô-đun :mod:`!numbers` (:pep:`3141`) định nghĩa một hệ phân cấp các kiểu số
:term:`lớp cơ sở trừu tượng <abstract base class>` lần lượt định nghĩa thêm nhiều phép toán. Không có kiểu nào được định nghĩa trong mô-đun này предназначены để tạo thực thể.


.. class:: Number

   Gốc của hệ phân cấp số. Nếu bạn chỉ muốn kiểm tra xem một đối số *x* có phải là một số hay không mà không quan tâm đến loại số nào, hãy sử dụng ``isinstance(x, Number)``.


Hệ phân cấp số
--------------

.. class:: Complex

   Các lớp con của kiểu này mô tả số phức và bao gồm các phép toán hoạt động trên kiểu :class:`complex` tích hợp sẵn. Các phép toán đó gồm: chuyển đổi sang
   :class:`complex` và :class:`bool`, :attr:`.real`, :attr:`.imag`, ``+``, ``-``, ``*``, ``/``, ``**``, :func:`abs`, :meth:`conjugate`, ``==`` và ``!=``. Tất cả đều là lớp trừu tượng, ngoại trừ ``-`` và ``!=``.

   .. attribute:: real

      Trừu tượng. Lấy phần thực của số này.

   .. attribute:: imag

      Trừu tượng. Lấy phần ảo của số này.

   .. method:: conjugate()
      :abstractmethod:

      Trừu tượng. Trả về số phức liên hợp. Ví dụ: ``(1+3j).conjugate() == (1-3j)``.

.. class:: Real

   Để :class:`Complex`, :class:`!Real` bổ sung các phép toán hoạt động trên số thực.

   Tóm lại, các phép toán đó là: chuyển đổi sang :class:`float`, :func:`math.trunc`,
   :func:`round`, :func:`math.floor`, :func:`math.ceil`, :func:`divmod`, ``//``, ``%``, ``<``, ``<=``, ``>``, và ``>=``.

   Real cũng cung cấp các giá trị mặc định cho :func:`complex`, :attr:`~Complex.real`,
   :attr:`~Complex.imag` và :meth:`~Complex.conjugate`.


.. class:: Rational

   Kế thừa :class:`Real` và bổ sung các thuộc tính :attr:`~Rational.numerator` và
   :attr:`~Rational.denominator`. Nó cũng cung cấp giá trị mặc định cho
   :func:`float`.

   Các giá trị :attr:`~Rational.numerator` và :attr:`~Rational.denominator` phải là các thực thể của :class:`Integral` và phải ở dạng tối giản, với
   :attr:`~Rational.denominator` dương.

   .. attribute:: numerator

      Trừu tượng. Tử số của số hữu tỉ này.

   .. attribute:: denominator

      Trừu tượng. Mẫu số của số hữu tỉ này.


.. class:: Integral

   Là lớp con của :class:`Rational` và bổ sung khả năng chuyển đổi sang :class:`int`. Cung cấp các giá trị mặc định cho :func:`float`, :attr:`~Rational.numerator`, và
   :attr:`~Rational.denominator`. Bổ sung các phương thức trừu tượng cho :func:`pow` với các thao tác modulus và chuỗi bit: ``<<``, ``>>``, ``&``, ``^``, ``|``, ``~``.


Lưu ý dành cho bên triển khai kiểu
----------------------------------

Bên triển khai cần cẩn thận để các số bằng nhau có giá trị bằng nhau và được băm thành cùng một giá trị. Điều này có thể tinh tế nếu có hai phần mở rộng khác nhau của các số thực. Xem thêm :ref:`numeric-hash`.


Bổ sung thêm các ABC số học
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dĩ nhiên, còn có nhiều ABC khả dĩ khác cho các số, và đây sẽ là một hệ phân cấp tồi nếu nó ngăn cản khả năng bổ sung chúng. Bạn có thể thêm ``MyFoo`` giữa :class:`Complex` và
:class:`Real` với::

    class MyFoo(Complex): ...
    MyFoo.register(Real)


.. _implementing-the-arithmetic-operations:

Triển khai các phép toán số học
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chúng ta muốn triển khai các phép toán số học để các phép toán mixed-mode либо gọi một implementation mà tác giả biết kiểu của cả hai đối số, либо chuyển đổi cả hai sang kiểu built-in gần nhất rồi thực hiện phép toán ở đó. Đối với các subtype của :class:`Integral`, điều này có nghĩa là :meth:`~object.__add__` và :meth:`~object.__radd__` nên được định nghĩa như sau::

    class MyIntegral(Integral):

        def __add__(self, other):
            if isinstance(other, MyIntegral):
                return do_my_adding_stuff(self, other)
            elif isinstance(other, OtherTypeIKnowAbout):
                return do_my_other_adding_stuff(self, other)
            else:
                return NotImplemented

        def __radd__(self, other):
            if isinstance(other, MyIntegral):
                return do_my_adding_stuff(other, self)
            elif isinstance(other, OtherTypeIKnowAbout):
                return do_my_other_adding_stuff(other, self)
            elif isinstance(other, Integral):
                return int(other) + int(self)
            elif isinstance(other, Real):
                return float(other) + float(self)
            elif isinstance(other, Complex):
                return complex(other) + complex(self)
            else:
                return NotImplemented


Có 5 trường hợp khác nhau đối với một phép toán mixed-type trên các subclass của :class:`Complex`. Tôi sẽ gọi toàn bộ đoạn code ở trên không tham chiếu đến ``MyIntegral`` và ``OtherTypeIKnowAbout`` là "boilerplate". ``a`` sẽ là một instance của ``A``, vốn là một subtype của :class:`Complex` (``a : A <: Complex``), và ``b : B <: Complex``. Tôi sẽ xét ``a + b``:

1. Nếu ``A`` định nghĩa một :meth:`~object.__add__` chấp nhận ``b``, thì mọi việc đều ổn.
2. Nếu ``A`` chuyển sang đoạn code boilerplate và trả về một giá trị từ :meth:`~object.__add__`, chúng ta sẽ bỏ lỡ khả năng ``B`` định nghĩa một :meth:`~object.__radd__` thông minh hơn, vì vậy boilerplate nên trả về :data:`NotImplemented` từ
   :meth:`!__add__`. (Hoặc ``A`` có thể hoàn toàn không triển khai :meth:`!__add__`.)
3. Sau đó, :meth:`~object.__radd__` của ``B`` có cơ hội được gọi. Nếu nó chấp nhận ``a``, mọi việc đều ổn.
4. Nếu nó chuyển sang phần boilerplate, thì không còn phương thức khả thi nào khác để thử, vì vậy đây là nơi phần triển khai mặc định nên được đặt.
5. Nếu ``B <: A``, Python thử ``B.__radd__`` trước ``A.__add__``. Điều này là hợp lý, vì nó được triển khai với hiểu biết về ``A``, nên có thể xử lý các instance đó trước khi ủy quyền cho :class:`Complex`.

Nếu ``A <: Complex`` và ``B <: Real`` mà không chia sẻ bất kỳ hiểu biết nào khác, thì phép toán chung thích hợp là phép toán liên quan đến :class:`complex` dựng sẵn, và cả hai :meth:`~object.__radd__` đều đi đến đó, vì vậy ``a+b == b+a``.

Vì hầu hết các phép toán trên bất kỳ kiểu cụ thể nào cũng sẽ rất giống nhau, nên việc định nghĩa một hàm helper để tạo ra các instance xuôi và ngược của bất kỳ toán tử nào cũng có thể hữu ích. Ví dụ:
:class:`fractions.Fraction` sử dụng::

    def _operator_fallbacks(monomorphic_operator, fallback_operator):
        def forward(a, b):
            if isinstance(b, (int, Fraction)):
                return monomorphic_operator(a, b)
            elif isinstance(b, float):
                return fallback_operator(float(a), b)
            elif isinstance(b, complex):
                return fallback_operator(complex(a), b)
            else:
                return NotImplemented
        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, Rational):
                # Bao gồm các số nguyên.
                return monomorphic_operator(a, b)
            elif isinstance(a, Real):
                return fallback_operator(float(a), float(b))
            elif isinstance(a, Complex):
                return fallback_operator(complex(a), complex(b))
            else:
                return NotImplemented
        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse

    def _add(a, b):
        """a + b"""
        return Fraction(a.numerator * b.denominator +
                        b.numerator * a.denominator,
                        a.denominator * b.denominator)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    # ...
