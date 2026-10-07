.. _annotations-howto:

***************************************
Các phương pháp hay nhất về Annotations
***************************************

:author: Larry Hastings

.. topic:: Tóm tắt

  Tài liệu này được thiết kế để trình bày các phương pháp hay nhất khi làm việc với các dict annotations. Nếu bạn viết mã Python kiểm tra ``__annotations__`` trên các đối tượng Python, chúng tôi khuyến khích bạn làm theo các hướng dẫn dưới đây.

  Tài liệu được tổ chức thành bốn phần: các phương pháp hay nhất để truy cập annotations của một đối tượng trong Python phiên bản 3.10 trở lên, các phương pháp hay nhất để truy cập annotations của một đối tượng trong Python phiên bản 3.9 trở xuống, các phương pháp hay nhất khác về ``__annotations__`` áp dụng cho mọi phiên bản Python, và các đặc điểm bất thường của ``__annotations__``.

  Lưu ý rằng tài liệu này chỉ đề cập đến việc làm việc với ``__annotations__``, không phải việc sử dụng *for* annotations. Nếu bạn đang tìm thông tin về cách sử dụng “type hints” trong mã của mình, hãy xem module :mod:`typing`.


Truy cập Dict Annotations của một đối tượng trong Python 3.10 trở lên
=====================================================================

Python 3.10 bổ sung một hàm mới vào thư viện chuẩn:
:func:`inspect.get_annotations`. Trong các phiên bản Python từ 3.10 đến 3.13, gọi hàm này là cách thực hành tốt nhất để truy cập dict chú thích của mọi đối tượng hỗ trợ chú thích. Hàm này cũng có thể giúp bạn "bỏ dạng chuỗi" khỏi các chú thích được biểu diễn dưới dạng chuỗi.

Trong Python 3.14, có một module :mod:`annotationlib` mới với các chức năng làm việc với chú thích. Module này bao gồm hàm :func:`annotationlib.get_annotations`, hàm thay thế cho :func:`inspect.get_annotations`.

Nếu vì lý do nào đó :func:`inspect.get_annotations` không phù hợp với trường hợp sử dụng của bạn, bạn có thể truy cập thủ công thành viên dữ liệu ``__annotations__``. Cách thực hành tốt nhất cho việc này cũng đã thay đổi trong Python 3.10: kể từ Python 3.10, ``o.__annotations__`` được đảm bảo *luôn* hoạt động trên các hàm, lớp và module Python. Nếu bạn chắc chắn đối tượng đang kiểm tra là một trong ba loại đối tượng *cụ thể* này, bạn có thể chỉ cần sử dụng ``o.__annotations__`` để truy cập dict chú thích của đối tượng.

Tuy nhiên, các loại callable khác--ví dụ như các callable được tạo bởi :func:`functools.partial`--có thể không có thuộc tính ``__annotations__`` được định nghĩa. Khi truy cập ``__annotations__`` của một đối tượng có thể chưa xác định, cách thực hành tốt nhất trong các phiên bản Python 3.10 trở lên là gọi :func:`getattr` với ba đối số, chẳng hạn như ``getattr(o, '__annotations__', None)``.

Trước Python 3.10, việc truy cập ``__annotations__`` trên một lớp không định nghĩa chú thích nào nhưng có lớp cha chứa chú thích sẽ trả về ``__annotations__`` của lớp cha. Trong Python 3.10 trở lên, chú thích của lớp con sẽ thay vào đó là một dict rỗng.


Truy cập Dict Chú Thích Của Một Đối Tượng Trong Python 3.9 Và Cũ Hơn
====================================================================

Trong Python 3.9 và các phiên bản cũ hơn, việc truy cập dictionary annotations của một đối tượng phức tạp hơn nhiều so với các phiên bản mới hơn. Vấn đề nằm ở một thiếu sót trong thiết kế của các phiên bản Python cũ này, cụ thể là liên quan đến class annotations.

Cách tốt nhất để truy cập dictionary annotations của các đối tượng khác--functions, các callable khác và modules--giống với cách tốt nhất trong 3.10, với điều kiện bạn không gọi
:func:`inspect.get_annotations`: bạn nên sử dụng phiên bản ba đối số
:func:`getattr` để truy cập thuộc tính ``__annotations__`` của đối tượng.

Đáng tiếc là đây không phải cách tốt nhất đối với classes. Vấn đề là, vì ``__annotations__`` là tùy chọn trên classes, đồng thời classes có thể kế thừa attributes từ các base class, việc truy cập thuộc tính ``__annotations__`` của một class có thể vô tình trả về dictionary annotations của một *lớp cơ sở.* Ví dụ::

    class Base:
        a: int = 3
        b: str = 'abc'

    class Derived(Base):
        pass

    print(Derived.__annotations__)

Lệnh này sẽ in dictionary annotations từ ``Base``, không phải từ ``Derived``.

Code của bạn sẽ cần một nhánh code riêng nếu đối tượng đang kiểm tra là một class (``isinstance(o, type)``). Trong trường hợp đó, cách tốt nhất dựa trên một chi tiết triển khai của Python 3.9 và các phiên bản trước: nếu một class có annotations được định nghĩa, chúng sẽ được lưu trong dictionary :attr:`~type.__dict__` của class. Vì class có thể có hoặc không có annotations được định nghĩa, cách tốt nhất là gọi method :meth:`~dict.get` trên dictionary của class.

Để tổng hợp lại, dưới đây là một đoạn mã mẫu truy cập an toàn vào thuộc tính ``__annotations__`` trên một đối tượng bất kỳ trong Python 3.9 trở về trước::

    if isinstance(o, type):
        ann = o.__dict__.get('__annotations__', None)
    else:
        ann = getattr(o, '__annotations__', None)

Sau khi chạy đoạn mã này, ``ann`` phải là một dictionary hoặc ``None``. Bạn nên kiểm tra lại kiểu của ``ann`` bằng :func:`isinstance` trước khi kiểm tra thêm.

Lưu ý rằng một số đối tượng kiểu đặc biệt hoặc không hợp lệ có thể không có thuộc tính :attr:`~type.__dict__`, vì vậy để an toàn hơn, bạn cũng có thể muốn dùng :func:`getattr` để truy cập :attr:`!__dict__`.


Chuyển thủ công các chú thích dạng chuỗi về giá trị
===================================================

Trong những trường hợp một số chú thích có thể được biểu diễn dưới dạng chuỗi (stringized) và bạn muốn đánh giá các chuỗi đó để tạo ra các giá trị Python mà chúng biểu diễn, tốt nhất là gọi :func:`inspect.get_annotations` để thực hiện việc này cho bạn.

Nếu bạn đang sử dụng Python 3.9 trở về trước, hoặc vì lý do nào đó không thể sử dụng :func:`inspect.get_annotations`, bạn sẽ cần sao chép logic của nó. Bạn nên xem xét cách triển khai :func:`inspect.get_annotations` trong phiên bản Python hiện tại và làm theo cách tiếp cận tương tự.

Tóm lại, nếu muốn đánh giá một chú thích dạng chuỗi trên một đối tượng bất kỳ ``o``:

* Nếu ``o`` là một module, hãy dùng ``o.__dict__`` làm ``globals`` khi gọi :func:`eval`.
* Nếu ``o`` là một class, hãy dùng ``sys.modules[o.__module__].__dict__`` làm ``globals`` và ``dict(vars(o))`` làm ``locals`` khi gọi :func:`eval`.
* Nếu ``o`` là một callable được bọc bằng :func:`functools.update_wrapper`,
  :deco:`functools.wraps` hoặc :func:`functools.partial`, hãy lần lượt bỏ lớp bọc bằng cách truy cập ``o.__wrapped__`` hoặc ``o.func`` tương ứng, cho đến khi tìm được function gốc không còn lớp bọc.
* Nếu ``o`` là một callable (nhưng không phải class), hãy dùng
  :attr:`o.__globals__ <function.__globals__>` làm globals khi gọi
  :func:`eval`.

Tuy nhiên, không phải mọi giá trị chuỗi được dùng làm annotation đều có thể được :func:`eval` chuyển đổi thành công thành các giá trị Python. Về lý thuyết, giá trị chuỗi có thể chứa bất kỳ chuỗi hợp lệ nào, và trên thực tế có những trường hợp sử dụng type hint hợp lệ yêu cầu chú thích bằng các giá trị chuỗi mà cụ thể là *không thể* được đánh giá. Ví dụ:

* :pep:`604` các kiểu union bằng ``|``, trước khi tính năng hỗ trợ cho việc này được thêm vào Python 3.10.
* Các định nghĩa không cần thiết trong runtime, chỉ được import khi :const:`typing.TYPE_CHECKING` là true.

Nếu :func:`eval` cố gắng đánh giá các giá trị như vậy, thao tác sẽ thất bại và phát sinh một exception. Vì vậy, khi thiết kế một library API làm việc với các annotation, bạn nên chỉ cố gắng đánh giá các giá trị chuỗi khi caller yêu cầu rõ ràng.


Các phương pháp hay nhất cho ``__annotations__`` trong mọi phiên bản Python
===========================================================================

* Bạn nên tránh gán trực tiếp cho member ``__annotations__`` của các object. Hãy để Python quản lý việc thiết lập ``__annotations__``.

* Nếu bạn gán trực tiếp cho member ``__annotations__`` của một object, bạn luôn nên đặt nó thành một object ``dict``.

* Bạn nên tránh truy cập trực tiếp ``__annotations__`` trên bất kỳ object nào. Thay vào đó, hãy sử dụng :func:`annotationlib.get_annotations` (Python 3.14+) hoặc :func:`inspect.get_annotations` (Python 3.10+).

* Nếu bạn truy cập trực tiếp thành viên ``__annotations__`` của một đối tượng, hãy đảm bảo đó là một dictionary trước khi kiểm tra nội dung của nó.

* Bạn nên tránh sửa đổi các dictionary ``__annotations__``.

* Bạn nên tránh xóa thuộc tính ``__annotations__`` của một đối tượng.


Các điểm đặc biệt của ``__annotations__``
=========================================

Trong tất cả các phiên bản Python 3, các đối tượng hàm sẽ tạo một dictionary chú thích một cách lười biếng nếu không có chú thích nào được định nghĩa trên đối tượng đó. Bạn có thể xóa thuộc tính ``__annotations__`` bằng ``del fn.__annotations__``, nhưng nếu sau đó bạn truy cập ``fn.__annotations__``, đối tượng sẽ tạo một dictionary trống mới, lưu và trả về dictionary đó dưới dạng chú thích của nó. Việc xóa chú thích của một hàm trước khi hàm đó tạo dictionary chú thích một cách lười biếng sẽ gây ra ``AttributeError``; sử dụng ``del fn.__annotations__`` hai lần liên tiếp luôn chắc chắn gây ra ``AttributeError``.

Mọi nội dung trong đoạn trên cũng áp dụng cho các đối tượng lớp và module trong Python 3.10 trở lên.

Trong tất cả các phiên bản Python 3, bạn có thể đặt ``__annotations__`` trên một đối tượng hàm thành ``None``. Tuy nhiên, việc truy cập các chú thích trên đối tượng đó bằng ``fn.__annotations__`` sau đó sẽ tạo một dictionary trống một cách lười biếng, như đã nêu trong đoạn đầu tiên của phần này. Điều này *không* đúng với module và lớp trong bất kỳ phiên bản Python nào; các đối tượng đó cho phép đặt ``__annotations__`` thành bất kỳ giá trị Python nào và sẽ giữ nguyên giá trị đã được đặt.

Nếu Python tự chuyển các annotation của bạn thành chuỗi (bằng cách sử dụng ``from __future__ import annotations``), và bạn chỉ định một chuỗi làm annotation, thì bản thân chuỗi đó sẽ được đặt trong dấu nháy. Nói cách khác, annotation được đặt trong dấu nháy *hai lần.*  Ví dụ::

     from __future__ import annotations
     def foo(a: "str"): pass

     print(foo.__annotations__)

Lệnh này in ra ``{'a': "'str'"}``. Điều này thực ra không nên được xem là một "quirk"; nó được đề cập ở đây đơn giản vì có thể gây bất ngờ.

Nếu bạn sử dụng một class có metaclass tùy chỉnh và truy cập ``__annotations__`` trên class đó, bạn có thể nhận thấy hành vi không mong đợi; xem
:pep:`749 <749#pep749-metaclasses>` để biết một số ví dụ. Bạn có thể tránh các quirk này bằng cách sử dụng :func:`annotationlib.get_annotations` trên Python 3.14+ hoặc
:func:`inspect.get_annotations` trên Python 3.10+. Trên các phiên bản Python cũ hơn, bạn có thể tránh những lỗi này bằng cách truy cập các annotation từ :attr:`~type.__dict__` của class (ví dụ: ``cls.__dict__.get('__annotations__', None)``).

Trong một số phiên bản Python, các instance của class có thể có thuộc tính ``__annotations__``. Tuy nhiên, đây không phải là chức năng được hỗ trợ. Nếu cần các annotation của một instance, bạn có thể sử dụng :func:`type` để truy cập class của nó (ví dụ: ``annotationlib.get_annotations(type(myinstance))`` trên Python 3.14+).
