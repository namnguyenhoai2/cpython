:mod:`!annotationlib` --- Chức năng tự kiểm tra các chú thích
=============================================================

.. module:: annotationlib
   :synopsis: Chức năng tự kiểm tra các chú thích

.. versionadded:: 3.14

**Mã nguồn:** :source:`Lib/annotationlib.py`

.. testsetup:: default

   import annotationlib
   from annotationlib import *

--------------

Mô-đun :mod:`!annotationlib` cung cấp các công cụ để tự kiểm tra
:term:`các chú thích <annotation>` trên các mô-đun, lớp và hàm.

Các chú thích được :ref:`đánh giá một cách trì hoãn <lazy-evaluation>` và thường chứa các tham chiếu tiến đến những đối tượng chưa được định nghĩa tại thời điểm chú thích được tạo. Mô-đun này cung cấp một tập hợp các công cụ cấp thấp có thể được sử dụng để truy xuất chú thích một cách đáng tin cậy, ngay cả khi có các tham chiếu tiến và những trường hợp biên khác.

Mô-đun này hỗ trợ truy xuất chú thích theo ba định dạng chính (xem :class:`Format`), mỗi định dạng phù hợp nhất với những trường hợp sử dụng khác nhau:

* :attr:`~Format.VALUE` đánh giá các annotation và trả về giá trị của chúng. Đây là cách làm đơn giản nhất, nhưng có thể phát sinh lỗi, chẳng hạn khi các annotation chứa tham chiếu đến những tên chưa được định nghĩa.
* :attr:`~Format.FORWARDREF` trả về các đối tượng :class:`ForwardRef` cho những annotation không thể được phân giải, cho phép bạn kiểm tra các annotation mà không cần đánh giá chúng. Điều này hữu ích khi bạn cần làm việc với các annotation có thể chứa các forward reference chưa được phân giải.
* :attr:`~Format.STRING` trả về các annotation dưới dạng chuỗi, tương tự như cách chúng xuất hiện trong tệp mã nguồn. Điều này hữu ích cho các trình tạo tài liệu muốn hiển thị annotation theo cách dễ đọc.

Hàm :func:`get_annotations` là điểm truy cập chính để lấy các annotation. Với một function, class hoặc module, hàm này trả về một dictionary annotation ở định dạng được yêu cầu. Module này cũng cung cấp chức năng làm việc trực tiếp với :term:`annotate function` được dùng để đánh giá annotation, chẳng hạn như :func:`get_annotate_from_class_namespace` và :func:`call_annotate_function`, cũng như
hàm :func:`call_evaluate_function` để làm việc với
:term:`evaluate functions <evaluate function>`.

.. caution::

   Hầu hết chức năng trong module này có thể thực thi mã tùy ý; hãy xem
   :ref:`phần bảo mật <annotationlib-security>` để biết thêm thông tin.

.. seealso::

   :pep:`649` đã đề xuất mô hình hiện tại về cách annotation hoạt động trong Python.

   :pep:`749` đã mở rộng nhiều khía cạnh của :pep:`649` và giới thiệu
   :mod:`!annotationlib` module.

   :ref:`annotations-howto` cung cấp các phương pháp hay nhất để làm việc với annotation.

   :pypi:`typing-extensions` cung cấp bản backport của :func:`get_annotations` có thể hoạt động trên các phiên bản Python cũ hơn.

Ngữ nghĩa của annotation
------------------------

Cách các chú thích được đánh giá đã thay đổi trong suốt lịch sử Python 3 và hiện vẫn phụ thuộc vào một :ref:`lệnh import future <future>`. Có các mô hình thực thi chú thích sau:

* *Ngữ nghĩa mặc định* (mặc định trong Python 3.0 đến 3.13; xem :pep:`3107` và :pep:`526`): Các chú thích được đánh giá ngay khi được gặp trong mã nguồn.
* *Chú thích dạng chuỗi* (được sử dụng với ``from __future__ import annotations`` trong Python 3.7 trở lên; xem :pep:`563`): Các chú thích chỉ được lưu dưới dạng chuỗi.
* *Đánh giá trì hoãn* (mặc định trong Python 3.14 trở lên; xem :pep:`649` và
  :pep:`749`): Các chú thích được đánh giá một cách lười biếng, chỉ khi chúng được truy cập.

Ví dụ, hãy xem xét chương trình sau::

   def func(a: Cls) -> None:
       print(a)

   class Cls: pass

   print(func.__annotations__)

Chương trình này sẽ hoạt động như sau:

* Theo semantics mặc định (Python 3.13 trở về trước), nó sẽ ném ra một
  :exc:`NameError` tại dòng nơi ``func`` được định nghĩa, vì ``Cls`` là một tên chưa được định nghĩa tại thời điểm đó.
* Theo annotations dạng chuỗi (nếu sử dụng ``from __future__ import annotations``), nó sẽ in ``{'a': 'Cls', 'return': 'None'}``.
* Theo đánh giá trì hoãn (Python 3.14 trở lên), nó sẽ in ``{'a': <class 'Cls'>, 'return': None}``.

Semantics mặc định được sử dụng khi function annotations lần đầu được giới thiệu trong Python 3.0 (bởi :pep:`3107`) vì đây là cách đơn giản và trực quan nhất để triển khai annotations. Cùng mô hình thực thi đó được sử dụng khi variable annotations được giới thiệu trong Python 3.6 (bởi :pep:`526`). Tuy nhiên, semantics mặc định gây ra vấn đề khi sử dụng annotations làm type hints, chẳng hạn như cần tham chiếu đến những tên chưa được định nghĩa khi annotation được gặp. Ngoài ra, việc thực thi annotations tại thời điểm module được import gây ra các vấn đề về hiệu năng. Vì vậy, trong Python 3.7,
:pep:`563` đã giới thiệu khả năng lưu trữ annotations dưới dạng chuỗi bằng cú pháp ``from __future__ import annotations``. Khi đó, kế hoạch là cuối cùng sẽ đặt hành vi này làm mặc định, nhưng một vấn đề đã xuất hiện: annotations dạng chuỗi khó xử lý hơn đối với những công cụ kiểm tra annotations tại runtime. Một đề xuất thay thế, :pep:`649`, đã giới thiệu mô hình thực thi thứ ba, đó là đánh giá trì hoãn, và được triển khai trong Python 3.14. Annotations dạng chuỗi vẫn được sử dụng nếu có ``from __future__ import annotations``, nhưng hành vi này cuối cùng sẽ bị loại bỏ.

Các lớp
-------

.. class:: Format

   Một :class:`~enum.IntEnum` mô tả các định dạng mà trong đó chú thích có thể được trả về. Các thành viên của enum hoặc các giá trị số nguyên tương đương của chúng có thể được truyền vào :func:`get_annotations` và các hàm khác trong mô-đun này, cũng như vào các hàm :attr:`~object.__annotate__`.

   .. attribute:: VALUE
      :value: 1

      Các giá trị là kết quả của việc đánh giá các biểu thức chú thích.

   .. attribute:: VALUE_WITH_FAKE_GLOBALS
      :value: 2

      Giá trị đặc biệt được dùng để báo hiệu rằng một hàm annotate đang được đánh giá trong một môi trường đặc biệt với các biến toàn cục giả. Khi được truyền giá trị này, các hàm annotate phải trả về cùng giá trị như đối với định dạng :attr:`Format.VALUE`, hoặc phát sinh :exc:`NotImplementedError` để báo hiệu rằng chúng không hỗ trợ thực thi trong môi trường này. Định dạng này chỉ được sử dụng nội bộ và không được truyền vào các hàm trong mô-đun này.

   .. attribute:: FORWARDREF
      :value: 3

      Đối với các giá trị đã được định nghĩa, các giá trị là những giá trị chú thích thực (theo định dạng :attr:`Format.VALUE`), còn đối với các giá trị chưa được định nghĩa, chúng là các proxy :class:`ForwardRef`. Các đối tượng thực có thể chứa tham chiếu đến các đối tượng proxy :class:`ForwardRef`.

   .. attribute:: STRING
      :value: 4

      Các giá trị là chuỗi văn bản của chú thích như xuất hiện trong mã nguồn, có thể đã qua các sửa đổi bao gồm nhưng không giới hạn ở việc chuẩn hóa khoảng trắng và tối ưu hóa các giá trị hằng số.

      Các giá trị chính xác của những chuỗi này có thể thay đổi trong các phiên bản Python tương lai.

   .. versionadded:: 3.14

.. class:: ForwardRef

   Một đối tượng proxy cho các tham chiếu chuyển tiếp trong chú thích.

   Các instance của lớp này được trả về khi sử dụng định dạng :attr:`~Format.FORWARDREF` và chú thích chứa một tên không thể phân giải. Điều này có thể xảy ra khi sử dụng tham chiếu chuyển tiếp trong chú thích, chẳng hạn khi một lớp được tham chiếu trước khi được định nghĩa.

   .. attribute:: __forward_arg__

      Một chuỗi chứa đoạn mã đã được đánh giá để tạo ra
      :class:`~ForwardRef`. Chuỗi này có thể không hoàn toàn tương đương với mã nguồn ban đầu.

   .. method:: evaluate(*, owner=None, globals=None, locals=None, type_params=None, format=Format.VALUE)

      Đánh giá tham chiếu chuyển tiếp và trả về giá trị của nó.

      Nếu đối số *format* là :attr:`~Format.VALUE` (giá trị mặc định), phương thức này có thể ném ra một ngoại lệ, chẳng hạn như :exc:`NameError`, nếu tham chiếu chuyển tiếp trỏ đến một tên không thể phân giải. Các đối số của phương thức này có thể được dùng để cung cấp các liên kết cho những tên nếu không sẽ không được định nghĩa. Nếu đối số *format* là :attr:`~Format.FORWARDREF`, phương thức sẽ không bao giờ ném ra ngoại lệ, nhưng có thể trả về một instance :class:`~ForwardRef`. Ví dụ: nếu đối tượng tham chiếu chuyển tiếp chứa đoạn mã ``list[undefined]``, trong đó ``undefined`` là một tên chưa được định nghĩa, việc đánh giá nó bằng định dạng :attr:`~Format.FORWARDREF` sẽ trả về ``list[ForwardRef('undefined')]``. Nếu đối số *format* là
      :attr:`~Format.STRING`, phương thức sẽ trả về :attr:`~ForwardRef.__forward_arg__`.

      Tham số *owner* cung cấp cơ chế được ưu tiên để truyền thông tin về phạm vi đến phương thức này. Owner của một :class:`~ForwardRef` là đối tượng chứa chú thích mà từ đó :class:`~ForwardRef` được tạo ra, chẳng hạn như một đối tượng module, đối tượng kiểu hoặc đối tượng hàm.

      Các tham số *globals*, *locals* và *type_params* cung cấp một cơ chế chính xác hơn để tác động đến các tên khả dụng khi :class:`~ForwardRef` được đánh giá. *globals* và *locals* được truyền vào :func:`eval`, lần lượt biểu diễn các namespace toàn cục và cục bộ nơi tên đó được đánh giá. Tham số *type_params* liên quan đến các đối tượng được tạo bằng cú pháp native cho :ref:`generic classes <generic-classes>` và :ref:`functions <generic-functions>`. Đây là một tuple gồm các :ref:`type parameters <type-params>` nằm trong phạm vi khi forward reference được đánh giá. Ví dụ, nếu đang đánh giá một
      :class:`~ForwardRef` được lấy từ một annotation trong namespace của một generic class ``C``, thì *type_params* phải được đặt thành ``C.__type_params__``.

      Các instance :class:`~ForwardRef` do :func:`get_annotations` trả về sẽ giữ các tham chiếu đến thông tin về phạm vi mà chúng bắt nguồn, vì vậy việc gọi phương thức này mà không cung cấp thêm đối số có thể đủ để đánh giá các đối tượng đó. Các instance :class:`~ForwardRef` được tạo bằng những cách khác có thể không có thông tin về phạm vi của chúng, vì vậy có thể cần truyền đối số cho phương thức này để đánh giá chúng thành công.

      Nếu không cung cấp *owner*, *globals*, *locals* hoặc *type_params* nào và
      :class:`~ForwardRef` không chứa thông tin về nguồn gốc của nó, các dictionary globals và locals rỗng sẽ được sử dụng.

   .. versionadded:: 3.14


Các hàm
-------

.. function:: annotations_to_string(annotations)

   Chuyển một dict annotations chứa các giá trị runtime thành một dict chỉ chứa các chuỗi. Nếu các giá trị chưa phải là chuỗi, chúng sẽ được chuyển đổi bằng :func:`type_repr`. Đây là một helper dành cho các hàm annotate do người dùng cung cấp, hỗ trợ định dạng :attr:`~Format.STRING` nhưng không có quyền truy cập vào mã tạo ra các annotations.

   Ví dụ: cách này được dùng để triển khai định dạng :attr:`~Format.STRING` cho các lớp :class:`typing.TypedDict` được tạo thông qua cú pháp hàm:

   .. doctest::

       >>> from typing import TypedDict
       >>> Movie = TypedDict("movie", {"name": str, "year": int})
       >>> get_annotations(Movie, format=Format.STRING)
       {'name': 'str', 'year': 'int'}

   .. versionadded:: 3.14

.. function:: call_annotate_function(annotate, format, *, owner=None)

   Gọi :term:`annotate function` *annotate* với *format* đã cho, là một thành viên của enum :class:`Format`, rồi trả về từ điển chú thích do hàm tạo ra.

   Hàm trợ giúp này là bắt buộc vì các hàm annotate được compiler tạo cho các hàm, lớp và module chỉ hỗ trợ định dạng :attr:`~Format.VALUE` khi được gọi trực tiếp. Để hỗ trợ các định dạng khác, hàm này gọi hàm annotate trong một môi trường đặc biệt cho phép hàm đó tạo chú thích ở các định dạng khác. Đây là một khối xây dựng hữu ích khi triển khai chức năng cần đánh giá một phần các chú thích trong lúc một lớp đang được tạo.

   *owner* là đối tượng sở hữu hàm chú thích, thường là một hàm, lớp hoặc module. Nếu được cung cấp, nó được dùng trong
   định dạng :attr:`~Format.FORWARDREF` để tạo ra một đối tượng :class:`ForwardRef` chứa nhiều thông tin hơn.

   .. seealso::

      :PEP:`PEP 649 <649#the-stringizer-and-the-fake-globals-environment>` chứa phần giải thích về kỹ thuật triển khai được hàm này sử dụng.

   .. versionadded:: 3.14

.. function:: call_evaluate_function(evaluate, format, *, owner=None)

   Gọi :term:`evaluate function` *evaluate* với *format* đã cho, là một thành viên của enum :class:`Format`, rồi trả về giá trị do hàm tạo ra. Cách này tương tự như :func:`call_annotate_function`, nhưng cách sau luôn trả về một từ điển ánh xạ các chuỗi tới các chú thích, trong khi hàm này trả về một giá trị duy nhất.

   Nội dung này được dùng với các hàm evaluate được tạo cho những phần tử được đánh giá một cách trì hoãn liên quan đến bí danh kiểu và tham số kiểu:

   * :meth:`typing.TypeAliasType.evaluate_value`, giá trị của các bí danh kiểu
   * :meth:`typing.TypeVar.evaluate_bound`, giới hạn của các biến kiểu
   * :meth:`typing.TypeVar.evaluate_constraints`, các ràng buộc của các biến kiểu
   * :meth:`typing.TypeVar.evaluate_default`, giá trị mặc định của các biến kiểu
   * :meth:`typing.ParamSpec.evaluate_default`, giá trị mặc định của các đặc tả tham số
   * :meth:`typing.TypeVarTuple.evaluate_default`, giá trị mặc định của các bộ giá trị kiểu

   *owner* là đối tượng sở hữu hàm evaluate, chẳng hạn như đối tượng type alias hoặc type variable.

   *format* có thể được dùng để kiểm soát định dạng mà giá trị được trả về:

   .. doctest::

      >>> type Alias = undefined
      >>> call_evaluate_function(Alias.evaluate_value, Format.VALUE)
      Traceback (most recent call last):
      ...
      NameError: name 'undefined' is not defined
      >>> call_evaluate_function(Alias.evaluate_value, Format.FORWARDREF)
      ForwardRef('undefined')
      >>> call_evaluate_function(Alias.evaluate_value, Format.STRING)
      'undefined'

   .. versionadded:: 3.14

.. function:: get_annotate_from_class_namespace(namespace)

   Lấy :term:`annotate function` từ từ điển namespace của lớp *namespace*. Trả về :const:`!None` nếu namespace không chứa hàm annotate. Điều này chủ yếu hữu ích trước khi lớp được tạo hoàn chỉnh (ví dụ: trong một metaclass); sau khi lớp tồn tại, có thể lấy hàm annotate bằng ``cls.__annotate__``. Xem :ref:`below <annotationlib-metaclass>` để biết ví dụ sử dụng hàm này trong một metaclass.

   .. versionadded:: 3.14

.. function:: get_annotations(obj, *, globals=None, locals=None, eval_str=False, format=Format.VALUE)

   Tính toán dict annotations cho một đối tượng.

   *obj* có thể là một callable, class, module hoặc đối tượng khác có
   thuộc tính :attr:`~object.__annotate__` hoặc :attr:`~object.__annotations__`. Việc truyền bất kỳ đối tượng nào khác sẽ làm phát sinh :exc:`TypeError`.

   Tham số *format* kiểm soát định dạng mà annotations được trả về và phải là một thành viên của enum :class:`Format` hoặc giá trị số nguyên tương đương của enum đó. Các định dạng khác nhau hoạt động như sau:

   * VALUE: :attr:`!object.__annotations__` được thử trước; nếu không tồn tại, hàm :attr:`!object.__annotate__` sẽ được gọi nếu nó tồn tại.

   * FORWARDREF: Nếu :attr:`!object.__annotations__` tồn tại và có thể được đánh giá thành công, nó sẽ được sử dụng; nếu không, hàm :attr:`!object.__annotate__` sẽ được gọi. Nếu hàm này cũng không tồn tại, :attr:`!object.__annotations__` sẽ được thử lại và mọi lỗi khi truy cập nó sẽ được ném lại.

     * Khi gọi :attr:`!object.__annotate__`, trước tiên hàm được gọi với :attr:`~Format.FORWARDREF`. Nếu cách này chưa được triển khai, hàm sẽ kiểm tra xem :attr:`~Format.VALUE_WITH_FAKE_GLOBALS` có được hỗ trợ hay không và sử dụng nó trong môi trường globals giả lập. Nếu không định dạng nào trong hai định dạng này được hỗ trợ, hàm sẽ chuyển sang sử dụng :attr:`~Format.VALUE`. Nếu :attr:`~Format.VALUE` không thành công, lỗi từ lần gọi này sẽ được ném ra.

   * STRING: Nếu :attr:`!object.__annotate__` tồn tại, nó sẽ được gọi trước; nếu không, :attr:`!object.__annotations__` sẽ được sử dụng và chuyển thành chuỗi bằng :func:`annotations_to_string`.

     * Khi gọi :attr:`!object.__annotate__`, trước tiên hàm được gọi với :attr:`~Format.STRING`. Nếu cách này chưa được triển khai, hàm sẽ kiểm tra xem :attr:`~Format.VALUE_WITH_FAKE_GLOBALS` có được hỗ trợ hay không và sử dụng nó trong môi trường globals giả lập. Nếu không định dạng nào trong hai định dạng này được hỗ trợ, hàm sẽ chuyển sang sử dụng :attr:`~Format.VALUE` với kết quả được chuyển đổi bằng :func:`annotations_to_string`. Nếu :attr:`~Format.VALUE` không thành công, lỗi từ lần gọi này sẽ được ném ra.

   Trả về một dict. :func:`!get_annotations` trả về một dict mới mỗi khi được gọi; gọi nó hai lần trên cùng một đối tượng sẽ trả về hai dict khác nhau nhưng tương đương.

   Hàm này xử lý một số chi tiết cho bạn:

   * Nếu *eval_str* là true, các giá trị thuộc kiểu :class:`!str` sẽ được bỏ dạng chuỗi bằng :func:`eval`. Tùy chọn này nhằm sử dụng với các annotation ở dạng chuỗi (``from __future__ import annotations``). Sẽ xảy ra lỗi nếu đặt *eval_str* thành true với các định dạng khác :attr:`Format.VALUE`.
   * Nếu *obj* không có một dict annotations, hàm trả về một dict rỗng. (Các function và method luôn có một dict annotations; class, module và các kiểu callable khác có thể không có.)
   * Bỏ qua các annotation được kế thừa trên class, cũng như các annotation trên metaclass. Nếu một class không có dict annotations riêng, hàm trả về một dict rỗng.
   * Mọi lần truy cập vào member của object và giá trị trong dict đều được thực hiện bằng ``getattr()`` và ``dict.get()`` để đảm bảo an toàn.

   *eval_str* kiểm soát việc các giá trị thuộc kiểu :class:`!str` có được thay thế bằng kết quả gọi :func:`eval` trên các giá trị đó hay không:

   * Nếu eval_str là true, :func:`eval` sẽ được gọi trên các giá trị thuộc kiểu
     :class:`!str`. (Lưu ý rằng :func:`!get_annotations` không bắt các exception; nếu :func:`eval` phát sinh một exception, exception đó sẽ unwound stack vượt qua lệnh gọi :func:`!get_annotations`.)
   * Nếu *eval_str* là false (mặc định), các giá trị thuộc kiểu :class:`!str` sẽ không thay đổi.

   *globals* và *locals* được truyền vào :func:`eval`; xem tài liệu về :func:`eval` để biết thêm thông tin. Nếu *globals* hoặc *locals* là :const:`!None`, hàm này có thể thay thế giá trị đó bằng một giá trị mặc định dành riêng cho ngữ cảnh, tùy thuộc vào ``type(obj)``:

   * Nếu *obj* là một module, *globals* mặc định là ``obj.__dict__``.
   * Nếu *obj* là một class, *globals* mặc định là ``sys.modules[obj.__module__].__dict__`` và *locals* mặc định là namespace của class *obj*.
   * Nếu *obj* là một callable, *globals* mặc định là
     :attr:`obj.__globals__ <function.__globals__>`, mặc dù nếu *obj* là một hàm được bọc (sử dụng
     :func:`functools.update_wrapper`) hoặc một đối tượng :class:`functools.partial`, nó sẽ được bỏ bọc cho đến khi tìm thấy một hàm không được bọc.

   Gọi :func:`!get_annotations` là cách thực hành tốt nhất để truy cập dict annotations của bất kỳ đối tượng nào. Xem :ref:`annotations-howto` để biết thêm thông tin về các cách thực hành tốt nhất với annotations.

   .. doctest::

      >>> def f(a: int, b: str) -> float:
      ...     pass
      >>> get_annotations(f)
      {'a': <class 'int'>, 'b': <class 'str'>, 'return': <class 'float'>}

   .. versionadded:: 3.14

.. function:: type_repr(value)

   Chuyển đổi một giá trị Python bất kỳ sang định dạng phù hợp để sử dụng với
   định dạng :attr:`~Format.STRING`. Hàm này gọi :func:`repr` cho hầu hết các đối tượng, nhưng có cách xử lý đặc biệt đối với một số đối tượng, chẳng hạn như các đối tượng kiểu.

   Hàm này được dùng làm helper cho các hàm annotate do người dùng cung cấp, hỗ trợ định dạng :attr:`~Format.STRING` nhưng không có quyền truy cập vào mã tạo annotations. Hàm này cũng có thể được dùng để cung cấp biểu diễn chuỗi thân thiện với người dùng cho các đối tượng khác chứa những giá trị thường gặp trong annotations.

   .. versionadded:: 3.14


Các công thức
-------------

.. _annotationlib-metaclass:

Sử dụng annotations trong metaclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một :ref:`metaclass <metaclasses>` có thể muốn kiểm tra hoặc thậm chí sửa đổi annotations trong thân lớp trong quá trình tạo lớp. Để làm vậy, cần lấy annotations từ dictionary namespace của lớp. Đối với các lớp được tạo bằng ``from __future__ import annotations``, annotations sẽ nằm trong khóa ``__annotations__`` của dictionary. Đối với các lớp khác có annotations,
Có thể sử dụng :func:`get_annotate_from_class_namespace` để lấy hàm annotate, và :func:`call_annotate_function` để gọi hàm đó và truy xuất các annotation. Thông thường, sử dụng định dạng :attr:`~Format.FORWARDREF` sẽ là lựa chọn tốt nhất, vì định dạng này cho phép các annotation tham chiếu đến những tên chưa thể được phân giải khi lớp được tạo.

Để sửa đổi các annotation, tốt nhất là tạo một hàm annotate wrapper gọi hàm annotate ban đầu, thực hiện mọi điều chỉnh cần thiết, rồi trả về kết quả.

Dưới đây là ví dụ về một metaclass lọc tất cả các annotation :class:`typing.ClassVar` khỏi lớp và đặt chúng vào một thuộc tính riêng:

.. code-block:: python

   import annotationlib
   import typing

   class ClassVarSeparator(type):
      def __new__(mcls, name, bases, ns):
         if "__annotations__" in ns:  # from __future__ import annotations
            annotations = ns["__annotations__"]
            classvar_keys = {
               key for key, value in annotations.items()
               # Dùng phép so sánh chuỗi cho đơn giản; một giải pháp mạnh mẽ hơn
               # có thể sử dụng annotationlib.ForwardRef.evaluate
               if value.startswith("ClassVar")
            }
            classvars = {key: annotations[key] for key in classvar_keys}
            ns["__annotations__"] = {
               key: value for key, value in annotations.items()
               if key not in classvar_keys
            }
            wrapped_annotate = None
         elif annotate := annotationlib.get_annotate_from_class_namespace(ns):
            annotations = annotationlib.call_annotate_function(
               annotate, format=annotationlib.Format.FORWARDREF
            )
            classvar_keys = {
               key for key, value in annotations.items()
               if typing.get_origin(value) is typing.ClassVar
            }
            classvars = {key: annotations[key] for key in classvar_keys}

            def wrapped_annotate(format):
               annos = annotationlib.call_annotate_function(annotate, format, owner=typ)
               return {key: value for key, value in annos.items() if key not in classvar_keys}

         else:  # không có annotation
            classvars = {}
            wrapped_annotate = None
         typ = super().__new__(mcls, name, bases, ns)

         if wrapped_annotate is not None:
            # Bọc __annotate__ ban đầu bằng một wrapper để loại bỏ ClassVars
            typ.__annotate__ = wrapped_annotate
         typ.classvars = classvars  # Lưu ClassVars trong một thuộc tính riêng
         return typ


Tạo một hàm annotate có thể gọi tùy chỉnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các :term:`hàm annotate <annotate function>` tùy chỉnh có thể là các hàm nguyên bản, giống như những hàm được tự động tạo cho các hàm, lớp và mô-đun. Hoặc, chúng có thể tận dụng tính đóng gói do các lớp cung cấp; khi đó, bất kỳ :term:`callable` nào cũng có thể được sử dụng làm một :term:`annotate function`.

Để cung cấp trực tiếp :attr:`~Format.VALUE`, :attr:`~Format.STRING`, hoặc
các định dạng :attr:`~Format.FORWARDREF` trực tiếp, một :term:`annotate function` phải cung cấp thuộc tính sau:

* Một ``__call__`` có thể gọi với chữ ký ``__call__(format, /) -> dict``, không phát sinh :exc:`NotImplementedError` khi được gọi với một định dạng được hỗ trợ.

Để cung cấp định dạng :attr:`~Format.VALUE_WITH_FAKE_GLOBALS`, được dùng để tự động tạo :attr:`~Format.STRING` hoặc :attr:`~Format.FORWARDREF` nếu chúng không được hỗ trợ trực tiếp, các hàm :term:`annotate functions <annotate function>` phải cung cấp các thuộc tính sau:

* Một ``__call__`` có thể gọi được với chữ ký ``__call__(format, /) -> dict``, không phát sinh :exc:`NotImplementedError` khi được gọi với
  :attr:`~Format.VALUE_WITH_FAKE_GLOBALS`.
* Một :ref:`đối tượng code <code-objects>` ``__code__`` chứa code đã biên dịch cho hàm annotate.
* Tùy chọn: Một tuple chứa các giá trị mặc định cho đối số vị trí của hàm ``__kwdefaults__``, nếu hàm được biểu diễn bởi ``__code__`` sử dụng bất kỳ giá trị mặc định nào cho đối số vị trí.
* Tùy chọn: Một dict chứa các giá trị mặc định cho đối số từ khóa của hàm ``__defaults__``, nếu hàm được biểu diễn bởi ``__code__`` sử dụng bất kỳ giá trị mặc định nào cho đối số từ khóa.
* Tùy chọn: Tất cả :ref:`thuộc tính hàm khác <inspect-types>`.

.. code-block:: python

   class Annotate:
       called_formats = []

       def __call__(self, format=None, /, *, _self=None):
           # Khi được gọi với các biến toàn cục giả, `_self` sẽ là
           # giá trị self thực tế, và `self` sẽ là định dạng.
           if _self is not None:
               self, format = _self, self

           self.called_formats.append(format)
           if format <= 2:  # VALUE hoặc VALUE_WITH_FAKE_GLOBALS
               return {"x": MyType}
           raise NotImplementedError

       __code__ = __call__.__code__
       __defaults__ = (None,)
       __kwdefaults__ = property(lambda self: dict(_self=self))

       __globals__ = {}
       __builtins__ = {}
       __closure__ = None

Sau đó có thể gọi hàm này bằng:

.. code-block:: pycon

   >>> from annotationlib import call_annotate_function, Format
   >>> call_annotate_function(Annotate(), format=Format.STRING)
   {'x': 'MyType'}

Hoặc dùng hàm này làm hàm annotate cho một đối tượng:

.. code-block:: pycon

   >>> from annotationlib import get_annotations, Format
   >>> class C:
   ...   pass
   >>> C.__annotate__ = Annotate()
   >>> get_annotations(Annotate(), format=Format.STRING)
   {'x': 'MyType'}


Các hạn chế của định dạng ``STRING``
------------------------------------

Định dạng :attr:`~Format.STRING` nhằm mô phỏng mã nguồn của annotation, nhưng chiến lược triển khai được sử dụng đồng nghĩa với việc không phải lúc nào cũng có thể khôi phục chính xác mã nguồn ban đầu.

Trước hết, stringifier tất nhiên không thể khôi phục bất kỳ thông tin nào không có trong mã đã biên dịch, bao gồm chú thích, khoảng trắng, việc đặt dấu ngoặc và các phép toán được trình biên dịch đơn giản hóa.

Thứ hai, stringifier có thể chặn gần như mọi thao tác liên quan đến các tên được tra cứu trong một scope nào đó, nhưng không thể chặn các thao tác chỉ hoạt động trên các hằng số. Hệ quả là cũng không an toàn khi yêu cầu định dạng ``STRING`` trên mã không đáng tin cậy: Python đủ mạnh để có thể thực thi mã tùy ý ngay cả khi không có quyền truy cập vào bất kỳ globals hoặc builtins nào. Ví dụ:

.. code-block:: pycon

  >>> def f(x: (1).__class__.__base__.__subclasses__()[-1].__init__.__builtins__["print"]("Hello world")): pass
  ...
  >>> annotationlib.get_annotations(f, format=annotationlib.Format.STRING)
  Hello world
  {'x': 'None'}

.. note::
   Ví dụ cụ thể này hoạt động tại thời điểm viết tài liệu, nhưng dựa trên các chi tiết triển khai và không được đảm bảo sẽ hoạt động trong tương lai.

Trong số các loại biểu thức khác nhau tồn tại trong Python, được biểu diễn bởi module :mod:`ast`, một số biểu thức được hỗ trợ, nghĩa là định dạng ``STRING`` nhìn chung có thể khôi phục mã nguồn ban đầu; những biểu thức khác không được hỗ trợ, nghĩa là chúng có thể tạo ra đầu ra không chính xác hoặc lỗi.

Sau đây là những nội dung được hỗ trợ (đôi khi có điều kiện hạn chế):

* :class:`ast.BinOp`
* :class:`ast.UnaryOp`

  * :class:`ast.Invert` (``~``), :class:`ast.UAdd` (``+``) và :class:`ast.USub` (``-``) được hỗ trợ
  * :class:`ast.Not` (``not``) không được hỗ trợ

* :class:`ast.Dict` (trừ khi sử dụng phép unpacking ``**``)
* :class:`ast.Set`
* :class:`ast.Compare`

  * :class:`ast.Eq` và :class:`ast.NotEq` được hỗ trợ
  * :class:`ast.Lt`, :class:`ast.LtE`, :class:`ast.Gt` và :class:`ast.GtE` được hỗ trợ, nhưng toán hạng có thể bị đảo
  * :class:`ast.Is`, :class:`ast.IsNot`, :class:`ast.In` và :class:`ast.NotIn` không được hỗ trợ

* :class:`ast.Call` (ngoại trừ khi sử dụng thao tác unpacking ``**``)
* :class:`ast.Constant` (tuy nhiên không phải biểu diễn chính xác của hằng số; ví dụ: các escape sequence trong chuỗi bị mất; số thập lục phân được chuyển đổi thành số thập phân)
* :class:`ast.Attribute` (với giả định giá trị không phải là hằng số)
* :class:`ast.Subscript` (với giả định giá trị không phải là hằng số)
* :class:`ast.Starred` (``*`` giải nén)
* :class:`ast.Name`
* :class:`ast.List`
* :class:`ast.Tuple`
* :class:`ast.Slice`

Những trường hợp sau đây không được hỗ trợ, nhưng sẽ đưa ra lỗi rõ ràng khi stringifier gặp phải:

* :class:`ast.FormattedValue` (f-strings; lỗi không được phát hiện nếu sử dụng các conversion specifier như ``!r``)
* :class:`ast.JoinedStr` (f-strings)

Những nội dung sau không được hỗ trợ và dẫn đến kết quả đầu ra không chính xác:

* :class:`ast.BoolOp` (``and`` và ``or``)
* :class:`ast.IfExp`
* :class:`ast.Lambda`
* :class:`ast.ListComp`
* :class:`ast.SetComp`
* :class:`ast.DictComp`
* :class:`ast.GeneratorExp`

Những nội dung sau bị cấm trong các phạm vi chú thích và do đó không liên quan:

* :class:`ast.NamedExpr` (``:=``)
* :class:`ast.Await`
* :class:`ast.Yield`
* :class:`ast.YieldFrom`


Hạn chế của định dạng ``FORWARDREF``
------------------------------------

Định dạng :attr:`~Format.FORWARDREF` hướng đến việc tạo ra các giá trị thực nhiều nhất có thể, trong đó mọi thứ không thể được phân giải sẽ được thay thế bằng
các đối tượng :class:`ForwardRef`. Định dạng này chịu ảnh hưởng bởi những hạn chế nhìn chung giống với định dạng :attr:`~Format.STRING`: các chú thích thực hiện thao tác trên các literal hoặc sử dụng những kiểu biểu thức không được hỗ trợ có thể phát sinh ngoại lệ khi được đánh giá bằng định dạng :attr:`~Format.FORWARDREF`.

Dưới đây là một vài ví dụ về hành vi khi sử dụng các biểu thức không được hỗ trợ:

.. code-block:: pycon

   >>> from annotationlib import get_annotations, Format
   >>> def zerodiv(x: 1 / 0): ...
   >>> get_annotations(zerodiv, format=Format.STRING)
   Traceback (most recent call last):
     ...
   ZeroDivisionError: division by zero
   >>> get_annotations(zerodiv, format=Format.FORWARDREF)
   Traceback (most recent call last):
     ...
   ZeroDivisionError: division by zero
   >>> def ifexp(x: 1 if y else 0): ...
   >>> get_annotations(ifexp, format=Format.STRING)
   {'x': '1'}

.. _annotationlib-security:

Hệ quả bảo mật của việc kiểm tra nội quan các chú thích
-------------------------------------------------------

Phần lớn chức năng trong module này liên quan đến việc thực thi mã liên quan đến các chú thích, và mã đó có thể thực hiện những hành động tùy ý. Ví dụ:
:func:`get_annotations` có thể gọi một :term:`annotate function` tùy ý, và
:meth:`ForwardRef.evaluate` có thể gọi :func:`eval` trên một chuỗi bất kỳ. Mã nằm trong một chú thích có thể thực hiện các lời gọi hệ thống tùy ý, đi vào vòng lặp vô hạn hoặc thực hiện bất kỳ thao tác nào khác. Điều này cũng đúng với mọi lần truy cập thuộc tính :attr:`~object.__annotations__`, cũng như với nhiều hàm trong module :mod:`typing` dùng để làm việc với các chú thích, chẳng hạn như
:func:`typing.get_type_hints`.

Mọi vấn đề bảo mật phát sinh từ việc này cũng áp dụng ngay sau khi nhập mã có thể chứa các chú thích không đáng tin cậy: việc nhập mã luôn có thể khiến các thao tác tùy ý được thực hiện. Tuy nhiên, việc nhận các chuỗi hoặc dữ liệu đầu vào khác từ một nguồn không đáng tin cậy rồi truyền chúng cho bất kỳ API nào dùng để xem xét các chú thích là không an toàn, chẳng hạn như chỉnh sửa một dictionary ``__annotations__`` hoặc trực tiếp tạo một đối tượng :class:`ForwardRef`.
