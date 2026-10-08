:mod:`!heapq` --- Thuật toán hàng đợi heap
==========================================

.. module:: heapq
   :synopsis: Thuật toán hàng đợi heap (còn gọi là hàng đợi ưu tiên).

.. moduleauthor:: Kevin O'Connor
.. sectionauthor:: Guido van Rossum <guido@python.org>
.. sectionauthor:: François Pinard
.. sectionauthor:: Raymond Hettinger

**Mã nguồn:** :source:`Lib/heapq.py`

--------------

Mô-đun này cung cấp cách triển khai thuật toán hàng đợi heap, còn được gọi là thuật toán hàng đợi ưu tiên.

Min-heap là các cây nhị phân trong đó mọi nút cha đều có giá trị nhỏ hơn hoặc bằng giá trị của bất kỳ nút con nào. Chúng ta gọi điều kiện này là bất biến heap.

Đối với min-heap, cách triển khai này sử dụng các list sao cho ``heap[k] <= heap[2*k+1]`` và ``heap[k] <= heap[2*k+2]`` với mọi *k* mà các phần tử được so sánh tồn tại. Các phần tử được đánh số bắt đầu từ không. Đặc điểm đáng chú ý của min-heap là phần tử nhỏ nhất luôn là nút gốc, ``heap[0]``.

Max-heap thỏa mãn bất biến ngược lại: mọi nút cha đều có giá trị *greater* hơn bất kỳ nút con nào. Chúng được triển khai dưới dạng các list sao cho ``maxheap[2*k+1] <= maxheap[k]`` và ``maxheap[2*k+2] <= maxheap[k]`` với mọi *k* mà các phần tử được so sánh tồn tại. Nút gốc, ``maxheap[0]``, chứa phần tử *largest*; ``heap.sort(reverse=True)`` duy trì bất biến max-heap.

API :mod:`!heapq` khác với các thuật toán heap trong giáo trình ở hai khía cạnh: (a) Chúng tôi sử dụng indexing bắt đầu từ 0. Điều này khiến mối quan hệ giữa chỉ mục của một node và các chỉ mục của các node con kém rõ ràng hơn đôi chút, nhưng phù hợp hơn vì Python sử dụng indexing bắt đầu từ 0. (b) Các giáo trình thường tập trung vào max-heap vì chúng phù hợp với việc sắp xếp tại chỗ. Cách triển khai của chúng tôi ưu tiên min-heap vì chúng tương ứng tốt hơn với :class:`lists <list>` của Python.

Hai khía cạnh này giúp bạn có thể xem heap như một Python list thông thường mà không gặp bất ngờ: ``heap[0]`` là phần tử nhỏ nhất, và ``heap.sort()`` duy trì bất biến của heap!

Tương tự :meth:`list.sort`, cách triển khai này chỉ sử dụng toán tử ``<`` để so sánh, cho cả min-heap và max-heap.

Trong API dưới đây và trong tài liệu này, thuật ngữ không có tiền tố *heap* thường chỉ min-heap. API dành cho max-heap được đặt tên với hậu tố ``_max``.

Để tạo một heap, hãy sử dụng một list được khởi tạo là ``[]``, hoặc chuyển một list hiện có thành min-heap hoặc max-heap bằng các hàm :func:`heapify` hoặc :func:`heapify_max`, tương ứng.

Các hàm sau đây được cung cấp cho min-heap:


.. function:: heapify(x)

   Chuyển list *x* thành min-heap tại chỗ trong thời gian tuyến tính.


.. function:: heappush(heap, item)

   Đẩy giá trị *item* vào *heap*, đồng thời duy trì bất biến min-heap.


.. function:: heappop(heap)

   Lấy và trả về item nhỏ nhất từ *heap*, đồng thời duy trì bất biến min-heap. Nếu heap trống, :exc:`IndexError` sẽ được phát sinh. Để truy cập item nhỏ nhất mà không lấy nó ra, hãy sử dụng ``heap[0]``.


.. function:: heappushpop(heap, item)

   Đẩy *item* vào heap, sau đó lấy và trả về item nhỏ nhất từ *heap*. Thao tác kết hợp này chạy hiệu quả hơn so với :func:`heappush` rồi gọi riêng :func:`heappop`.


.. function:: heapreplace(heap, item)

   Lấy và trả về item nhỏ nhất từ *heap*, đồng thời đẩy *item* mới vào. Kích thước heap không thay đổi. Nếu heap trống, :exc:`IndexError` sẽ được phát sinh.

   Thao tác một bước này hiệu quả hơn so với :func:`heappop` rồi
   :func:`heappush` và có thể phù hợp hơn khi sử dụng heap có kích thước cố định. Tổ hợp pop/push luôn trả về một phần tử từ heap và thay thế nó bằng *item*.

   Giá trị được trả về có thể lớn hơn *item* đã thêm vào. Nếu không mong muốn điều đó, hãy cân nhắc sử dụng :func:`heappushpop` thay thế. Tổ hợp push/pop của nó trả về giá trị nhỏ hơn trong hai giá trị, đồng thời giữ giá trị lớn hơn trên heap.


Đối với max-heap, các hàm sau được cung cấp:


.. function:: heapify_max(x)

   Chuyển đổi danh sách *x* thành max-heap ngay tại chỗ trong thời gian tuyến tính.

   .. versionadded:: 3.14


.. function:: heappush_max(heap, item)

   Đẩy giá trị *item* vào max-heap *heap*, duy trì bất biến max-heap.

   .. versionadded:: 3.14


.. function:: heappop_max(heap)

   Lấy và trả về phần tử lớn nhất từ max-heap *heap*, duy trì bất biến max-heap. Nếu max-heap trống, :exc:`IndexError` sẽ được phát sinh. Để truy cập phần tử lớn nhất mà không lấy nó ra, hãy sử dụng ``maxheap[0]``.

   .. versionadded:: 3.14


.. function:: heappushpop_max(heap, item)

   Đẩy *item* vào max-heap *heap*, sau đó lấy và trả về phần tử lớn nhất từ *heap*. Thao tác kết hợp này hiệu quả hơn :func:`heappush_max` tiếp theo là một lệnh gọi riêng đến :func:`heappop_max`.

   .. versionadded:: 3.14


.. function:: heapreplace_max(heap, item)

   Lấy và trả về phần tử lớn nhất từ max-heap *heap*, đồng thời đẩy *item* mới vào. Kích thước max-heap không thay đổi. Nếu max-heap trống,
   :exc:`IndexError` sẽ được phát sinh.

   Giá trị được trả về có thể nhỏ hơn *item* đã được thêm vào. Tham khảo hàm tương tự :func:`heapreplace` để biết ghi chú sử dụng chi tiết.

   .. versionadded:: 3.14


Mô-đun này cũng cung cấp ba hàm đa dụng dựa trên heap.


.. function:: merge(*iterables, key=None, reverse=False)

   Trộn nhiều đầu vào đã được sắp xếp thành một đầu ra duy nhất cũng được sắp xếp (ví dụ: trộn các mục có dấu thời gian từ nhiều tệp nhật ký). Trả về một :term:`iterator` trên các giá trị đã sắp xếp.

   Tương tự như ``sorted(itertools.chain(*iterables))`` nhưng trả về một iterable, không tải toàn bộ dữ liệu vào bộ nhớ cùng một lúc và giả định rằng mỗi luồng đầu vào đã được sắp xếp (từ nhỏ đến lớn).

   Có hai đối số tùy chọn phải được chỉ định dưới dạng keyword argument.

   *key* chỉ định một :term:`key function` gồm một đối số, được dùng để trích xuất khóa so sánh từ mỗi phần tử đầu vào. Giá trị mặc định là ``None`` (so sánh trực tiếp các phần tử).

   *reverse* là một giá trị boolean. Nếu được đặt thành ``True``, các phần tử đầu vào sẽ được trộn như thể mỗi phép so sánh đều bị đảo ngược. Để đạt được hành vi tương tự ``sorted(itertools.chain(*iterables), reverse=True)``, tất cả iterable phải được sắp xếp từ lớn đến nhỏ.

   .. versionchanged:: 3.5
      Đã bổ sung các tham số tùy chọn *key* và *reverse*.


.. function:: nlargest(n, iterable, key=None)

   Trả về một danh sách gồm *n* phần tử lớn nhất từ tập dữ liệu được xác định bởi *iterable*.  *key*, nếu được cung cấp, chỉ định một hàm nhận một đối số, được dùng để trích xuất khóa so sánh từ mỗi phần tử trong *iterable* (ví dụ: ``key=str.lower``).  Tương đương với:  ``sorted(iterable, key=key, reverse=True)[:n]``.


.. function:: nsmallest(n, iterable, key=None)

   Trả về một danh sách gồm *n* phần tử nhỏ nhất từ tập dữ liệu được xác định bởi *iterable*.  *key*, nếu được cung cấp, chỉ định một hàm nhận một đối số, được dùng để trích xuất khóa so sánh từ mỗi phần tử trong *iterable* (ví dụ: ``key=str.lower``).  Tương đương với:  ``sorted(iterable, key=key)[:n]``.


Hai hàm sau hoạt động tốt nhất với các giá trị *n* nhỏ hơn.  Với các giá trị lớn hơn, sử dụng hàm :func:`sorted` sẽ hiệu quả hơn.  Ngoài ra, khi ``n==1``, việc sử dụng các hàm tích hợp sẵn :func:`min` và :func:`max` sẽ hiệu quả hơn.  Nếu cần sử dụng lặp lại các hàm này, hãy cân nhắc chuyển iterable thành một heap thực sự.


Các ví dụ cơ bản
----------------

Có thể triển khai `heapsort <https://en.wikipedia.org/wiki/Heapsort>`_ bằng cách đẩy tất cả giá trị vào một heap, sau đó lần lượt lấy ra các giá trị nhỏ nhất::

   >>> def heapsort(iterable):
   ...     h = []
   ...     for value in iterable:
   ...         heappush(h, value)
   ...     return [heappop(h) for i in range(len(h))]
   ...
   >>> heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Điều này tương tự như ``sorted(iterable)``, nhưng không giống :func:`sorted`, cách triển khai này không stable.

Các phần tử trong heap có thể là các tuple. Điều này hữu ích khi gán các giá trị dùng để so sánh (chẳng hạn như độ ưu tiên của tác vụ) cùng với bản ghi chính đang được theo dõi::

    >>> h = []
    >>> heappush(h, (5, 'write code'))
    >>> heappush(h, (7, 'release product'))
    >>> heappush(h, (1, 'write spec'))
    >>> heappush(h, (3, 'create tests'))
    >>> heappop(h)
    (1, 'write spec')


Các ứng dụng khác
-----------------

`Trung vị <https://en.wikipedia.org/wiki/Median>`_ là một đại lượng đo xu hướng trung tâm của một tập hợp số. Trong các phân phối bị lệch do các giá trị ngoại lệ, trung vị cung cấp một ước tính ổn định hơn so với giá trị trung bình (trung bình số học). Trung vị động là một `thuật toán trực tuyến <https://en.wikipedia.org/wiki/Online_algorithm>`_ được cập nhật liên tục khi dữ liệu mới xuất hiện.

Có thể triển khai trung vị động một cách hiệu quả bằng cách cân bằng hai heap: một max-heap chứa các giá trị nhỏ hơn hoặc bằng điểm giữa và một min-heap chứa các giá trị lớn hơn điểm giữa. Khi hai heap có cùng kích thước, trung vị mới là giá trị trung bình của các phần tử đầu của hai heap; nếu không, trung vị nằm ở phần tử đầu của heap lớn hơn::

    def running_median(iterable):
        "Yields the cumulative median of values seen so far."

        lo = []  # max-heap
        hi = []  # min-heap (có kích thước bằng hoặc nhỏ hơn lo một phần tử)

        for x in iterable:
            if len(lo) == len(hi):
                heappush_max(lo, heappushpop(hi, x))
                yield lo[0]
            else:
                heappush(hi, heappushpop_max(lo, x))
                yield (lo[0] + hi[0]) / 2

Ví dụ::

    >>> list(running_median([5.0, 9.0, 4.0, 12.0, 8.0, 9.0]))
    [5.0, 7.0, 5.0, 7.0, 8.0, 8.5]


Ghi chú triển khai Priority Queue
---------------------------------

Một `hàng đợi ưu tiên <https://en.wikipedia.org/wiki/Priority_queue>`_ thường được triển khai bằng heap và đặt ra một số thách thức khi triển khai:

* Tính ổn định khi sắp xếp: làm thế nào để hai tác vụ có cùng mức ưu tiên được trả về theo thứ tự chúng được thêm vào ban đầu?

* So sánh tuple sẽ không hoạt động với các cặp (priority, task) nếu các priority bằng nhau và các task không có thứ tự so sánh mặc định.

* Nếu priority của một task thay đổi, làm thế nào để di chuyển task đó đến vị trí mới trong heap?

* Hoặc nếu cần xóa một task đang chờ, làm thế nào để tìm và xóa task đó khỏi queue?

Một cách giải quyết hai thách thức đầu tiên là lưu các mục dưới dạng danh sách gồm 3 phần tử, bao gồm priority, số thứ tự mục nhập và task. Số thứ tự mục nhập đóng vai trò là tiêu chí phân định để hai task có cùng priority được trả về theo thứ tự chúng được thêm vào. Và vì không có hai số thứ tự mục nhập nào giống nhau, phép so sánh tuple sẽ không bao giờ cố gắng so sánh trực tiếp hai task.

Một giải pháp khác cho vấn đề các task không thể so sánh là tạo một lớp wrapper bỏ qua phần tử task và chỉ so sánh trường priority::

    from dataclasses import dataclass, field
    from typing import Any

    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)

Các thách thức còn lại xoay quanh việc tìm một task đang chờ xử lý và thay đổi priority của task đó hoặc xóa hoàn toàn task. Có thể tìm task bằng một dictionary trỏ đến một entry trong queue.

Việc xóa entry hoặc thay đổi priority của entry khó hơn vì sẽ phá vỡ các bất biến của cấu trúc heap. Vì vậy, một giải pháp khả thi là đánh dấu entry là đã bị xóa và thêm một entry mới với priority đã được điều chỉnh::

    pq = []                         # danh sách các entry được sắp xếp trong một heap
    entry_finder = {}               # ánh xạ các task tới các entry
    REMOVED = '<removed-task>'      # placeholder cho một task đã bị xóa
    counter = itertools.count()     # bộ đếm chuỗi tuần tự duy nhất

    def add_task(task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)

    def remove_task(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')


Lý thuyết
---------

Heap là các mảng mà ``a[k] <= a[2*k+1]`` và ``a[k] <= a[2*k+2]`` với mọi *k*, tính các phần tử bắt đầu từ 0. Để tiện so sánh, các phần tử không tồn tại được coi là vô hạn. Đặc điểm thú vị của heap là ``a[0]`` luôn là phần tử nhỏ nhất của nó.

Bất biến kỳ lạ ở trên nhằm biểu diễn một giải đấu bằng bộ nhớ một cách hiệu quả. Các số bên dưới là *k*, không phải ``a[k]``::

                                  0

                 1                                 2

         3               4                5               6

     7       8       9       10      11      12      13      14

   15 16   17 18   19 20   21 22   23 24   25 26   27 28   29 30

Trong cây ở trên, mỗi ô *k* nằm trên ``2*k+1`` và ``2*k+2``. Trong một giải đấu nhị phân thông thường mà ta thấy trong thể thao, mỗi ô là ô thắng hai ô mà nó nằm trên, và ta có thể lần theo người thắng xuống cây để xem tất cả đối thủ mà người đó từng gặp. Tuy nhiên, trong nhiều ứng dụng máy tính của các giải đấu như vậy, ta không cần lần theo lịch sử của người thắng. Để sử dụng bộ nhớ hiệu quả hơn, khi một người thắng được đưa lên, ta cố gắng thay thế nó bằng một phần tử khác ở cấp thấp hơn, và quy tắc trở thành: một ô cùng hai ô mà nó nằm trên chứa ba phần tử khác nhau, nhưng ô ở trên "thắng" hai ô bên dưới.

Nếu luôn duy trì bất biến của heap này, chỉ số 0 rõ ràng là người thắng chung cuộc. Cách đơn giản nhất về mặt thuật toán để xóa nó và tìm người thắng "tiếp theo" là đưa một phần tử thua nào đó (giả sử là ô 30 trong sơ đồ ở trên) vào vị trí 0, sau đó đẩy phần tử 0 mới này xuống cây, hoán đổi các giá trị, cho đến khi bất biến được thiết lập lại. Rõ ràng, thao tác này có độ phức tạp logarithm theo tổng số phần tử trong cây. Bằng cách lặp qua tất cả các phần tử, ta có một phép sắp xếp *O*\ (*n* log *n*).

Một đặc điểm hay của cách sắp xếp này là bạn có thể chèn các phần tử mới một cách hiệu quả trong khi quá trình sắp xếp đang diễn ra, miễn là các phần tử được chèn không "tốt hơn" phần tử 0 cuối cùng mà bạn đã lấy ra. Điều này đặc biệt hữu ích trong các ngữ cảnh mô phỏng, nơi cây chứa tất cả các sự kiện đến và điều kiện "thắng" có nghĩa là thời điểm được lập lịch nhỏ nhất. Khi một sự kiện lập lịch các sự kiện khác để thực thi, chúng được lập lịch vào tương lai, nên có thể dễ dàng đưa chúng vào heap. Vì vậy, heap là một cấu trúc phù hợp để triển khai các scheduler (đây là cấu trúc tôi đã dùng cho bộ tuần tự MIDI của mình :-).

Nhiều cấu trúc khác nhau để triển khai scheduler đã được nghiên cứu rộng rãi, và heap rất phù hợp cho việc này vì chúng có tốc độ tương đối nhanh, tốc độ gần như không đổi, đồng thời trường hợp xấu nhất không khác nhiều so với trường hợp trung bình. Tuy nhiên, có những cách biểu diễn khác hiệu quả hơn xét trên tổng thể, dù các trường hợp xấu nhất của chúng có thể rất tệ.

Heap cũng rất hữu ích trong việc sắp xếp dữ liệu lớn trên đĩa. Có lẽ bạn đều biết rằng một lần sắp xếp lớn bao gồm việc tạo ra các "run" (những chuỗi đã được sắp xếp trước, với kích thước thường liên quan đến dung lượng bộ nhớ CPU), sau đó là các lượt trộn những run này; quá trình trộn thường được tổ chức rất khéo léo [#]_. Điều rất quan trọng là lần sắp xếp ban đầu tạo ra các run dài nhất có thể. Tournament là một cách tốt để đạt được điều đó. Nếu sử dụng toàn bộ bộ nhớ có sẵn để chứa một tournament, bạn thay thế và đẩy xuống các phần tử vừa với run hiện tại, bạn sẽ tạo ra các run có kích thước gấp đôi bộ nhớ đối với dữ liệu đầu vào ngẫu nhiên, và lớn hơn nhiều đối với dữ liệu đầu vào được sắp xếp tương đối.

Hơn nữa, nếu bạn xuất phần tử thứ 0 ra đĩa và nhận được một dữ liệu đầu vào không thể vừa với tournament hiện tại (vì giá trị của nó "thắng" giá trị được xuất cuối cùng), nó cũng không thể vừa trong heap, nên kích thước heap giảm xuống. Phần bộ nhớ được giải phóng có thể ngay lập tức được tái sử dụng một cách khéo léo để dần xây dựng một heap thứ hai, heap này tăng trưởng với đúng tốc độ mà heap đầu tiên thu nhỏ. Khi heap đầu tiên biến mất hoàn toàn, bạn chuyển sang heap kia và bắt đầu một run mới. Thật khéo léo và khá hiệu quả!

Tóm lại, heap là một cấu trúc bộ nhớ hữu ích mà bạn nên biết. Tôi sử dụng chúng trong một vài ứng dụng, và tôi nghĩ nên duy trì một module 'heap'. :-)

.. rubric:: Chú thích cuối trang

.. [#] Các thuật toán cân bằng đĩa hiện nay phiền toái hơn là khéo léo, và đây là hệ quả của khả năng seek của các đĩa. Trên những thiết bị không thể seek, chẳng hạn như các ổ băng lớn, câu chuyện lại hoàn toàn khác, và người ta phải cực kỳ khéo léo để đảm bảo (từ rất lâu trước đó) rằng mỗi lần di chuyển băng sẽ hiệu quả nhất có thể (nghĩa là đóng góp tốt nhất vào việc "tiến triển" quá trình trộn). Một số loại băng thậm chí còn có thể đọc ngược, và điều này cũng được tận dụng để tránh thời gian tua lại. Tin tôi đi, những lần sắp xếp trên băng thực sự tốt rất ngoạn mục khi xem! Từ trước đến nay, sắp xếp luôn là một Nghệ thuật Vĩ đại! :-)

.. _`heapsort`: https://en.wikipedia.org/wiki/Heapsort
.. _`Medians`: https://en.wikipedia.org/wiki/Median
.. _`online algorithm`: https://en.wikipedia.org/wiki/Online_algorithm
.. _`priority queue`: https://en.wikipedia.org/wiki/Priority_queue
