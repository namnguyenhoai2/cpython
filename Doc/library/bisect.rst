:mod:`!bisect` --- Thuật toán chia đôi mảng
===========================================

.. module:: bisect
   :synopsis: Các thuật toán chia đôi mảng để tìm kiếm nhị phân.
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Raymond Hettinger <python at rcn.com>
.. example based on the PyModules FAQ entry by Aaron Watters <arw@pythonpros.com>

**Mã nguồn:** :source:`Lib/bisect.py`

--------------

Mô-đun này hỗ trợ duy trì một danh sách theo thứ tự đã sắp xếp mà không cần sắp xếp lại danh sách sau mỗi lần chèn. Đối với các danh sách dài chứa những phần tử có thao tác so sánh tốn kém, cách này có thể cải thiện hiệu năng so với việc tìm kiếm tuyến tính hoặc sắp xếp lại thường xuyên.

Mô-đun này có tên là :mod:`!bisect` vì sử dụng một thuật toán chia đôi cơ bản để thực hiện công việc. Không giống các công cụ chia đôi khác dùng để tìm kiếm một giá trị cụ thể, các hàm trong mô-đun này được thiết kế để xác định vị trí chèn. Do đó, các hàm không bao giờ gọi phương thức :meth:`~object.__eq__` để xác định xem đã tìm thấy một giá trị hay chưa. Thay vào đó, các hàm chỉ gọi phương thức :meth:`~object.__lt__` và trả về một vị trí chèn giữa các giá trị trong một mảng.

.. note::

   Các hàm trong mô-đun này không an toàn khi sử dụng trong môi trường đa luồng. Nếu nhiều thread đồng thời sử dụng các hàm :mod:`!bisect` trên cùng một sequence, điều này có thể dẫn đến hành vi không xác định. Tương tự, nếu sequence được cung cấp bị một thread khác thay đổi trong khi hàm :mod:`!bisect` đang hoạt động trên đó, kết quả sẽ không xác định. Ví dụ, việc sử dụng
   :py:func:`~bisect.insort_left` trên cùng một danh sách từ nhiều thread có thể khiến danh sách không còn được sắp xếp.

.. _bisect functions:

Các hàm sau được cung cấp:


.. function:: bisect_left(a, x, lo=0, hi=len(a), *, key=None)

   Xác định vị trí chèn *x* vào *a* để duy trì thứ tự đã sắp xếp. Có thể sử dụng các tham số *lo* và *hi* để chỉ định một phần của danh sách cần xem xét; theo mặc định, toàn bộ danh sách được sử dụng. Nếu *x* đã có trong *a*, vị trí chèn sẽ nằm trước (về bên trái) mọi phần tử hiện có. Giá trị trả về phù hợp để dùng làm tham số đầu tiên cho ``list.insert()``, với điều kiện *a* đã được sắp xếp.

   Vị trí chèn được trả về *ip* phân chia mảng *a* thành hai lát cắt, sao cho ``all(elem < x for elem in a[lo : ip])`` là đúng đối với lát cắt bên trái và ``all(elem >= x for elem in a[ip : hi])`` là đúng đối với lát cắt bên phải.

   *key* chỉ định một :term:`key function` nhận một đối số, được dùng để trích xuất khóa so sánh từ mỗi phần tử trong mảng. Để hỗ trợ tìm kiếm các bản ghi phức tạp, hàm key không được áp dụng cho giá trị *x*.

   Nếu *key* là ``None``, các phần tử sẽ được so sánh trực tiếp và không có hàm key nào được gọi.

   .. versionchanged:: 3.10
      Đã thêm tham số *key*.


.. function:: bisect_right(a, x, lo=0, hi=len(a), *, key=None)
              bisect(a, x, lo=0, hi=len(a), *, key=None)

   Tương tự như :py:func:`~bisect.bisect_left`, nhưng trả về một vị trí chèn nằm sau (về bên phải) mọi mục nhập hiện có của *x* trong *a*.

   Vị trí chèn được trả về *ip* phân chia mảng *a* thành hai lát cắt, sao cho ``all(elem <= x for elem in a[lo : ip])`` đúng với lát cắt bên trái và ``all(elem > x for elem in a[ip : hi])`` đúng với lát cắt bên phải.

   .. versionchanged:: 3.10
      Đã thêm tham số *key*.


.. function:: insort_left(a, x, lo=0, hi=len(a), *, key=None)

   Chèn *x* vào *a* theo thứ tự đã sắp xếp.

   Trước tiên, hàm này chạy :py:func:`~bisect.bisect_left` để xác định vị trí chèn. Tiếp theo, hàm chạy phương thức :meth:`~sequence.insert` trên *a* để chèn *x* vào vị trí thích hợp nhằm duy trì thứ tự sắp xếp.

   Để hỗ trợ chèn các bản ghi vào một bảng, hàm *key* (nếu có) được áp dụng cho *x* trong bước tìm kiếm nhưng không được áp dụng trong bước chèn.

   Hãy nhớ rằng phép tìm kiếm *O*\ (log *n*) bị chi phối bởi bước chèn chậm *O*\ (*n*).

   .. versionchanged:: 3.10
      Đã thêm tham số *key*.


.. function:: insort_right(a, x, lo=0, hi=len(a), *, key=None)
              insort(a, x, lo=0, hi=len(a), *, key=None)

   Tương tự như :py:func:`~bisect.insort_left`, nhưng chèn *x* vào *a* sau mọi mục hiện có của *x*.

   Trước tiên, hàm này chạy :py:func:`~bisect.bisect_right` để xác định vị trí chèn. Tiếp theo, hàm gọi phương thức :meth:`~sequence.insert` trên *a* để chèn *x* vào vị trí thích hợp nhằm duy trì thứ tự sắp xếp.

   Để hỗ trợ chèn các bản ghi vào một bảng, hàm *key* (nếu có) được áp dụng cho *x* trong bước tìm kiếm nhưng không được áp dụng trong bước chèn.

   Hãy nhớ rằng phép tìm kiếm *O*\ (log *n*) bị chi phối bởi bước chèn chậm *O*\ (*n*).

   .. versionchanged:: 3.10
      Đã thêm tham số *key*.


Ghi chú về hiệu năng
--------------------

Khi viết mã nhạy cảm về thời gian bằng *bisect()* và *insort()*, hãy ghi nhớ những điều sau:

* Phép chia đôi hiệu quả khi tìm kiếm các phạm vi giá trị. Để định vị các giá trị cụ thể, dictionaries có hiệu năng tốt hơn.

* Các hàm *insort()* có độ phức tạp *O*\ (*n*) vì bước tìm kiếm logarithmic bị chi phối bởi bước chèn có thời gian tuyến tính.

* Các hàm tìm kiếm không lưu trạng thái và loại bỏ kết quả của hàm key sau khi sử dụng. Do đó, nếu các hàm tìm kiếm được sử dụng trong một vòng lặp, hàm key có thể được gọi lặp đi lặp lại trên cùng các phần tử mảng. Nếu hàm key không nhanh, hãy cân nhắc bọc nó bằng
  :py:deco:`functools.cache` để tránh các phép tính trùng lặp. Ngoài ra, hãy cân nhắc tìm kiếm trong một mảng các key đã được tính trước để định vị điểm chèn (như minh họa trong phần ví dụ bên dưới).

.. seealso::

   * `Sorted Collections <https://grantjenks.com/docs/sortedcollections/>`_ là một module hiệu năng cao sử dụng *bisect* để quản lý các tập hợp dữ liệu đã được sắp xếp.

   * Công thức `SortedCollection recipe <https://code.activestate.com/recipes/577197-sortedcollection/>`_ sử dụng bisect để xây dựng một class collection đầy đủ tính năng, với các phương thức tìm kiếm đơn giản, dễ hiểu và hỗ trợ key-function. Các key được tính toán trước để tránh những lần gọi không cần thiết đến key function trong quá trình tìm kiếm.


Tìm kiếm trong các danh sách đã sắp xếp
---------------------------------------

Các `hàm bisect <bisect functions_>`_ ở trên hữu ích để tìm vị trí chèn, nhưng có thể khó dùng hoặc bất tiện cho các tác vụ tìm kiếm thông thường. Năm hàm sau đây cho thấy cách chuyển đổi chúng thành các phép tra cứu tiêu chuẩn cho danh sách đã sắp xếp::

    def index(a, x):
        'Locate the leftmost value exactly equal to x'
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    def find_lt(a, x):
        'Find rightmost value less than x'
        i = bisect_left(a, x)
        if i:
            return a[i-1]
        raise ValueError

    def find_le(a, x):
        'Find rightmost value less than or equal to x'
        i = bisect_right(a, x)
        if i:
            return a[i-1]
        raise ValueError

    def find_gt(a, x):
        'Find leftmost value greater than x'
        i = bisect_right(a, x)
        if i != len(a):
            return a[i]
        raise ValueError

    def find_ge(a, x):
        'Find leftmost item greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return a[i]
        raise ValueError


Ví dụ
-----

.. _bisect-example:

Hàm :py:func:`~bisect.bisect` có thể hữu ích cho việc tra cứu bảng số. Ví dụ này sử dụng :py:func:`~bisect.bisect` để tra cứu điểm chữ cho điểm số của một bài thi (chẳng hạn) dựa trên một tập hợp các mốc số được sắp xếp: từ 90 trở lên là 'A', từ 80 đến 89 là 'B', v.v.::

   >>> def grade(score):
   ...     i = bisect([60, 70, 80, 90], score)
   ...     return "FDCBA"[i]
   ...
   >>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
   ['F', 'A', 'C', 'C', 'B', 'A', 'A']

Các hàm :py:func:`~bisect.bisect` và :py:func:`~bisect.insort` cũng hoạt động với các danh sách tuple. Đối số *key* có thể được dùng để trích xuất trường dùng cho việc sắp xếp các bản ghi trong một bảng::

    >>> from collections import namedtuple
    >>> from operator import attrgetter
    >>> from bisect import bisect, insort
    >>> from pprint import pprint

    >>> Movie = namedtuple('Movie', ('name', 'released', 'director'))

    >>> movies = [
    ...     Movie('Jaws', 1975, 'Spielberg'),
    ...     Movie('Titanic', 1997, 'Cameron'),
    ...     Movie('The Birds', 1963, 'Hitchcock'),
    ...     Movie('Aliens', 1986, 'Cameron')
    ... ]

    >>> # Tìm bộ phim đầu tiên được phát hành sau năm 1960
    >>> by_year = attrgetter('released')
    >>> movies.sort(key=by_year)
    >>> movies[bisect(movies, 1960, key=by_year)]
    Movie(name='The Birds', released=1963, director='Hitchcock')

    >>> # Chèn một bộ phim trong khi vẫn duy trì thứ tự sắp xếp
    >>> romance = Movie('Love Story', 1970, 'Hiller')
    >>> insort(movies, romance, key=by_year)
    >>> pprint(movies)
    [Movie(name='The Birds', released=1963, director='Hitchcock'),
     Movie(name='Love Story', released=1970, director='Hiller'),
     Movie(name='Jaws', released=1975, director='Spielberg'),
     Movie(name='Aliens', released=1986, director='Cameron'),
     Movie(name='Titanic', released=1997, director='Cameron')]

Nếu hàm key tốn nhiều chi phí, bạn có thể tránh việc gọi hàm lặp lại bằng cách tìm kiếm trong một danh sách các key đã được tính trước để xác định chỉ mục của một bản ghi::

    >>> data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
    >>> data.sort(key=lambda r: r[1])       # Hoặc sử dụng operator.itemgetter(1).
    >>> keys = [r[1] for r in data]         # Tính trước một danh sách các key.
    >>> data[bisect_left(keys, 0)]
    ('black', 0)
    >>> data[bisect_left(keys, 1)]
    ('blue', 1)
    >>> data[bisect_left(keys, 5)]
    ('red', 5)
    >>> data[bisect_left(keys, 8)]
    ('yellow', 8)

.. _`Sorted Collections`: https://grantjenks.com/docs/sortedcollections/
.. _`SortedCollection recipe`: https://code.activestate.com/recipes/577197-sortedcollection/
