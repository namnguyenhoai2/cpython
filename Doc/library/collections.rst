:mod:`!collections` --- Các kiểu dữ liệu container
==================================================

.. module:: collections
    :synopsis: Các kiểu dữ liệu container

.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>

**Mã nguồn:** :source:`Lib/collections/__init__.py`

.. testsetup:: *

    from collections import *
    import itertools
    __name__ = '<doctest>'

--------------

Mô-đun này triển khai các kiểu dữ liệu container chuyên biệt, cung cấp các lựa chọn thay thế cho các container tích hợp đa năng của Python, :class:`dict`, :class:`list`,
:class:`set`, và :class:`tuple`.

+----------------------+-------------------------------------------------------------------------------+
| :func:`namedtuple`   | hàm factory để tạo các lớp con của tuple với các trường được đặt tên          |
+----------------------+-------------------------------------------------------------------------------+
| :class:`deque`       | container dạng list với thao tác thêm và lấy phần tử nhanh chóng ở cả hai đầu |
+----------------------+-------------------------------------------------------------------------------+
| :class:`ChainMap`    | lớp tương tự dict để tạo một chế độ xem duy nhất từ nhiều mapping             |
+----------------------+-------------------------------------------------------------------------------+
| :class:`Counter`     | lớp con của dict để đếm các đối tượng :term:`hashable`                        |
+----------------------+-------------------------------------------------------------------------------+
| :class:`OrderedDict` | lớp con của dict ghi nhớ thứ tự các mục được thêm vào                         |
+----------------------+-------------------------------------------------------------------------------+
| :class:`defaultdict` | lớp con của dict gọi một hàm factory để cung cấp các giá trị còn thiếu        |
+----------------------+-------------------------------------------------------------------------------+
| :class:`UserDict`    | lớp bọc quanh các đối tượng dictionary để dễ dàng tạo lớp con của dict        |
+----------------------+-------------------------------------------------------------------------------+
| :class:`UserList`    | lớp bọc quanh các đối tượng list để dễ dàng tạo lớp con của list              |
+----------------------+-------------------------------------------------------------------------------+
| :class:`UserString`  | lớp bọc quanh các đối tượng string để dễ dàng tạo lớp con của string          |
+----------------------+-------------------------------------------------------------------------------+


:class:`ChainMap` đối tượng
---------------------------

.. versionadded:: 3.3

Một lớp :class:`ChainMap` được cung cấp để nhanh chóng liên kết một số mapping, cho phép xử lý chúng như một đơn vị duy nhất. Cách này thường nhanh hơn nhiều so với việc tạo một dictionary mới và thực hiện nhiều lần gọi :meth:`~dict.update`.

Lớp này có thể được dùng để mô phỏng các phạm vi lồng nhau và hữu ích trong việc tạo template.

.. class:: ChainMap(*maps)

    Một :class:`ChainMap` nhóm nhiều dict hoặc mapping khác lại với nhau để tạo một chế độ xem duy nhất có thể cập nhật. Nếu không chỉ định *maps*, một dictionary rỗng duy nhất sẽ được cung cấp để một chain mới luôn có ít nhất một mapping.

    Các mapping bên dưới được lưu trong một danh sách. Danh sách đó là công khai và có thể được truy cập hoặc cập nhật bằng thuộc tính *maps*. Không có trạng thái nào khác.

    Các thao tác tra cứu lần lượt tìm trong các mapping bên dưới cho đến khi tìm thấy một khóa. Ngược lại, thao tác ghi, cập nhật và xóa chỉ hoạt động trên mapping đầu tiên.

    Một :class:`ChainMap` kết hợp các mapping bên dưới theo tham chiếu. Vì vậy, nếu một trong các mapping bên dưới được cập nhật, những thay đổi đó sẽ được phản ánh trong :class:`ChainMap`.

    Tất cả các phương thức từ điển thông thường đều được hỗ trợ. Ngoài ra, còn có thuộc tính *maps*, một phương thức để tạo các ngữ cảnh con mới và một thuộc tính để truy cập tất cả các ánh xạ trừ ánh xạ đầu tiên:

    .. attribute:: maps

        Một danh sách các ánh xạ mà người dùng có thể cập nhật. Danh sách được sắp xếp từ ánh xạ được tìm kiếm đầu tiên đến ánh xạ được tìm kiếm cuối cùng. Đây là trạng thái duy nhất được lưu trữ và có thể được sửa đổi để thay đổi các ánh xạ được tìm kiếm. Danh sách luôn phải chứa ít nhất một ánh xạ.

    .. method:: new_child(m=None, **kwargs)

        Trả về một :class:`ChainMap` mới, chứa một map mới theo sau bởi tất cả các map trong instance hiện tại. Nếu ``m`` được chỉ định, nó sẽ trở thành map mới ở đầu danh sách các ánh xạ; nếu không được chỉ định, một dict rỗng sẽ được sử dụng, vì vậy lệnh gọi ``d.new_child()`` tương đương với: ``ChainMap({}, *d.maps)``. Nếu có chỉ định bất kỳ đối số keyword nào, chúng sẽ cập nhật map được truyền vào hoặc dict rỗng mới. Phương thức này được dùng để tạo các ngữ cảnh con có thể được cập nhật mà không làm thay đổi các giá trị trong bất kỳ ánh xạ cha nào.

        .. versionchanged:: 3.4
           Tham số ``m`` tùy chọn đã được bổ sung.

        .. versionchanged:: 3.10
           Đã bổ sung hỗ trợ cho các đối số keyword.

    .. attribute:: parents

        Thuộc tính trả về một :class:`ChainMap` mới, chứa tất cả các map trong instance hiện tại ngoại trừ map đầu tiên. Điều này hữu ích khi muốn bỏ qua map đầu tiên trong quá trình tìm kiếm. Các trường hợp sử dụng tương tự như đối với
        từ khóa :keyword:`nonlocal` trong :term:`nested scopes <nested scope>`. Các trường hợp sử dụng cũng tương tự như đối với thành phần tích hợp
        hàm :func:`super`. Tham chiếu đến ``d.parents`` tương đương với: ``ChainMap(*d.maps[1:])``.

    Lưu ý rằng thứ tự lặp của :class:`ChainMap` được xác định bằng cách quét các mapping từ cuối lên đầu::

        >>> baseline = {'music': 'bach', 'art': 'rembrandt'}
        >>> adjustments = {'art': 'van gogh', 'opera': 'carmen'}
        >>> list(ChainMap(adjustments, baseline))
        ['music', 'art', 'opera']

    Điều này tạo ra thứ tự giống với một chuỗi các lệnh gọi :meth:`dict.update` bắt đầu từ mapping cuối cùng::

        >>> combined = baseline.copy()
        >>> combined.update(adjustments)
        >>> list(combined)
        ['music', 'art', 'opera']

    .. versionchanged:: 3.9
       Đã bổ sung hỗ trợ cho các toán tử ``|`` và ``|=``, được chỉ định trong :pep:`584`.

.. seealso::

   * Lớp `MultiContext class <https://github.com/enthought/codetools/blob/4.0.0/codetools/contexts/multi_context.py>`_ trong gói `CodeTools package <https://github.com/enthought/codetools>`_ của Enthought có các tùy chọn hỗ trợ việc ghi vào bất kỳ mapping nào trong chuỗi.

   * `Context class <https://github.com/django/django/blob/main/django/template/context.py>`_ của Django dùng cho templating là một chuỗi mapping chỉ đọc. Nó cũng hỗ trợ việc đẩy và lấy các context tương tự như
     phương thức :meth:`~collections.ChainMap.new_child` và
     :attr:`~collections.ChainMap.parents` thuộc tính.

   * Công thức `Nested Contexts <https://code.activestate.com/recipes/577434-nested-contexts-a-chain-of-mapping-objects/>`_ có các tùy chọn để kiểm soát việc thao tác ghi và các thay đổi khác chỉ áp dụng cho mapping đầu tiên hay cho bất kỳ mapping nào trong chuỗi.

   * Một `phiên bản chỉ đọc được đơn giản hóa đáng kể của Chainmap <https://code.activestate.com/recipes/305268/>`_.


:class:`ChainMap` Ví dụ và công thức
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phần này trình bày nhiều cách tiếp cận khác nhau khi làm việc với các mapping được liên kết.


Ví dụ mô phỏng chuỗi tra cứu nội bộ của Python::

        import builtins
        pylookup = ChainMap(locals(), globals(), vars(builtins))

Ví dụ cho phép các đối số dòng lệnh do người dùng chỉ định được ưu tiên hơn các biến môi trường, còn các biến môi trường lại được ưu tiên hơn các giá trị mặc định::

        import os, argparse

        defaults = {'color': 'red', 'user': 'guest'}

        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--user')
        parser.add_argument('-c', '--color')
        namespace = parser.parse_args()
        command_line_args = {k: v for k, v in vars(namespace).items() if v is not None}

        combined = ChainMap(command_line_args, os.environ, defaults)
        print(combined['color'])
        print(combined['user'])

Các mẫu sử dụng lớp :class:`ChainMap` để mô phỏng các context lồng nhau::

        c = ChainMap()        # Tạo context gốc
        d = c.new_child()     # Tạo context con lồng nhau
        e = c.new_child()     # Con của c, độc lập với d
        e.maps[0]             # Dictionary của context hiện tại -- giống Python's locals()
        e.maps[-1]            # Context gốc -- giống Python's globals()
        e.parents             # Chuỗi context bao quanh -- giống Python's nonlocals

        d['x'] = 1            # Đặt giá trị trong context hiện tại
        d['x']                # Lấy key đầu tiên trong chuỗi context
        del d['x']            # Xóa khỏi context hiện tại
        list(d)               # Tất cả giá trị lồng nhau
        k in d                # Kiểm tra tất cả giá trị lồng nhau
        len(d)                # Số lượng giá trị lồng nhau
        d.items()             # Tất cả mục lồng nhau
        dict(d)               # Làm phẳng thành một dictionary thông thường

Lớp :class:`ChainMap` chỉ thực hiện cập nhật (ghi và xóa) trên mapping đầu tiên trong chuỗi, còn thao tác tra cứu sẽ tìm kiếm toàn bộ chuỗi. Tuy nhiên, nếu cần ghi và xóa sâu, bạn có thể dễ dàng tạo một lớp con để cập nhật các khóa được tìm thấy ở vị trí sâu hơn trong chuỗi::

    class DeepChainMap(ChainMap):
        'Variant of ChainMap that allows direct updates to inner scopes'

        def __setitem__(self, key, value):
            for mapping in self.maps:
                if key in mapping:
                    mapping[key] = value
                    return
            self.maps[0][key] = value

        def __delitem__(self, key):
            for mapping in self.maps:
                if key in mapping:
                    del mapping[key]
                    return
            raise KeyError(key)

    >>> d = DeepChainMap({'zebra': 'black'}, {'elephant': 'blue'}, {'lion': 'yellow'})
    >>> d['lion'] = 'orange'         # cập nhật một khóa hiện có ở sâu hai cấp
    >>> d['snake'] = 'red'           # các khóa mới được thêm vào dict trên cùng
    >>> del d['elephant']            # xóa một khóa hiện có ở sâu một cấp
    >>> d                            # hiển thị kết quả
    DeepChainMap({'zebra': 'black', 'snake': 'red'}, {}, {'lion': 'orange'})


các đối tượng :class:`Counter`
------------------------------

Một công cụ đếm được cung cấp để hỗ trợ việc thống kê thuận tiện và nhanh chóng. Ví dụ:::

    >>> # Đếm số lần xuất hiện của các từ trong một danh sách
    >>> cnt = Counter()
    >>> for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    ...     cnt[word] += 1
    ...
    >>> cnt
    Counter({'blue': 3, 'red': 2, 'green': 1})

    >>> # Tìm mười từ phổ biến nhất trong Hamlet
    >>> import re
    >>> words = re.findall(r'\w+', open('hamlet.txt').read().lower())
    >>> Counter(words).most_common(10)
    [('the', 1143), ('and', 966), ('to', 762), ('of', 669), ('i', 631),
     ('you', 554),  ('a', 546), ('my', 514), ('hamlet', 471), ('in', 451)]

.. class:: Counter(**kwargs)
           Counter(iterable, /, ****kwargs) Counter(mapping, /, ****kwargs)

    :class:`Counter` là một lớp con của :class:`dict` dùng để đếm các đối tượng :term:`hashable`. Đây là một collection trong đó các phần tử được lưu dưới dạng khóa từ điển và số lần xuất hiện của chúng được lưu dưới dạng giá trị từ điển. Số lần đếm có thể là bất kỳ giá trị số nguyên nào, kể cả số lần đếm bằng không hoặc âm. Lớp :class:`Counter` tương tự như bag hoặc multiset trong các ngôn ngữ khác.

    Các phần tử được đếm từ một *iterable* hoặc được khởi tạo từ một *mapping* khác (hoặc counter):

        >>> c = Counter()                           # Một Counter mới, rỗng
        >>> c = Counter('gallahad')                 # Một Counter mới từ một iterable
        >>> c = Counter({'red': 4, 'blue': 2})      # Một Counter mới từ một mapping
        >>> c = Counter(cats=4, dogs=8)             # Một Counter mới từ các đối số từ khóa

    Các đối tượng Counter có giao diện từ điển, ngoại trừ việc chúng trả về số lần đếm bằng không cho các mục bị thiếu thay vì phát sinh :exc:`KeyError`:

        >>> c = Counter(['eggs', 'ham'])
        >>> c['bacon']                              # Số lần xuất hiện của phần tử không tồn tại là 0
        0

    Đặt count về zero không xóa một phần tử khỏi counter. Sử dụng ``del`` để xóa hoàn toàn phần tử đó:

        >>> c['sausage'] = 0                        # Mục Counter có số đếm bằng 0
        >>> del c['sausage']                        # del thực sự xóa mục này

    .. versionadded:: 3.1

    .. versionchanged:: 3.7 Là một subclass của :class:`dict`, :class:`Counter`
       được thừa hưởng khả năng ghi nhớ thứ tự chèn. Các phép toán số học trên các đối tượng *Counter* cũng giữ nguyên thứ tự. Kết quả được sắp xếp theo thời điểm một phần tử được gặp lần đầu trong toán hạng bên trái, sau đó theo thứ tự gặp trong toán hạng bên phải.

    Các đối tượng Counter hỗ trợ thêm các phương thức ngoài những phương thức có sẵn cho mọi dictionary:

    .. method:: elements()

        Trả về một iterator trên các phần tử, lặp lại mỗi phần tử số lần tương ứng với count của nó. Các phần tử được trả về theo thứ tự gặp lần đầu. Nếu count của một phần tử nhỏ hơn một, :meth:`elements` sẽ bỏ qua phần tử đó.

            >>> c = Counter(a=4, b=2, c=0, d=-2)
            >>> sorted(c.elements())
            ['a', 'a', 'a', 'a', 'b', 'b']

    .. method:: most_common(n=None)

        Trả về danh sách *n* phần tử phổ biến nhất cùng count của chúng, từ phổ biến nhất đến ít phổ biến nhất. Nếu *n* bị bỏ qua hoặc ``None``,
        :meth:`most_common` trả về *all* phần tử trong counter. Các phần tử có count bằng nhau được sắp xếp theo thứ tự gặp lần đầu:

            >>> Counter('abracadabra').most_common(3)
            [('a', 5), ('b', 2), ('r', 2)]

    .. method:: subtract(**kwargs)
                subtract(iterable, /, ****kwargs) subtract(mapping, /, ****kwargs)

        Các phần tử được trừ khỏi một *iterable* hoặc từ một *mapping* khác (hoặc counter).  Tương tự :meth:`dict.update` nhưng trừ các count thay vì thay thế chúng.  Cả đầu vào và đầu ra đều có thể bằng không hoặc âm.

            >>> c = Counter(a=4, b=2, c=0, d=-2)
            >>> d = Counter(a=1, b=2, c=3, d=4)
            >>> c.subtract(d)
            >>> c
            Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})

        .. versionadded:: 3.2

    .. method:: total()

        Tính tổng các count.

            >>> c = Counter(a=10, b=5, c=0)
            >>> c.total()
            15

        .. versionadded:: 3.10

    Các phương thức dictionary thông thường đều khả dụng cho các đối tượng :class:`Counter`, ngoại trừ hai phương thức hoạt động khác đối với counter.

    .. method:: fromkeys(iterable)

        Phương thức lớp này không được triển khai cho các đối tượng :class:`Counter`.

    .. method:: update(**kwargs)
                update(iterable, /, ****kwargs) update(mapping, /, ****kwargs)

        Các phần tử được đếm từ một *iterable* hoặc được cộng thêm từ một *mapping* khác (hoặc counter).  Tương tự :meth:`dict.update` nhưng cộng các count thay vì thay thế chúng.  Ngoài ra, *iterable* được kỳ vọng là một chuỗi các phần tử, không phải một chuỗi các cặp ``(key, value)``.

Counter hỗ trợ các toán tử so sánh phong phú cho quan hệ bằng nhau, tập con và tập cha: ``==``, ``!=``, ``<``, ``<=``, ``>``, ``>=``. Tất cả các phép kiểm tra đó đều xem các phần tử bị thiếu là có số đếm bằng 0, vì vậy ``Counter(a=1) == Counter(a=1, b=0)`` trả về true.

.. versionchanged:: 3.10
   Các phép toán so sánh phong phú đã được bổ sung.

.. versionchanged:: 3.10
   Trong các phép kiểm tra bằng nhau, các phần tử bị thiếu được xem là có số đếm bằng 0. Trước đây, ``Counter(a=3)`` và ``Counter(a=3, b=0)`` được xem là khác nhau.

Các mẫu thường dùng khi làm việc với các đối tượng :class:`Counter`::

    c.total()                       # tổng của tất cả số đếm
    c.clear()                       # đặt lại tất cả số đếm
    list(c)                         # liệt kê các phần tử duy nhất
    set(c)                          # chuyển đổi thành một tập hợp
    dict(c)                         # chuyển đổi thành một từ điển thông thường
    c.items()                       # truy cập các cặp (elem, cnt)
    Counter(dict(list_of_pairs))    # chuyển đổi từ danh sách các cặp (elem, cnt)
    c.most_common()[:-n-1:-1]       # n phần tử ít phổ biến nhất
    +c                              # loại bỏ các số đếm bằng 0 và âm

Một số phép toán toán học được cung cấp để kết hợp các đối tượng :class:`Counter`, tạo ra các đa tập hợp (các bộ đếm có số đếm lớn hơn 0). Phép cộng và phép trừ kết hợp các bộ đếm bằng cách cộng hoặc trừ số đếm của các phần tử tương ứng. Phép giao và phép hợp trả về giá trị nhỏ nhất và lớn nhất của các số đếm tương ứng. Phép so sánh bằng và phép bao hàm so sánh các số đếm tương ứng. Mỗi phép toán có thể nhận đầu vào với các số đếm có dấu, nhưng kết quả sẽ loại bỏ các giá trị có số đếm bằng hoặc nhỏ hơn 0.

.. doctest::

    >>> c = Counter(a=3, b=1)
    >>> d = Counter(a=1, b=2)
    >>> c + d                       # cộng hai counter với nhau:  c[x] + d[x]
    Counter({'a': 4, 'b': 3})
    >>> c - d                       # phép trừ (chỉ giữ lại các số đếm dương)
    Counter({'a': 2})
    >>> c & d                       # phép giao:  min(c[x], d[x])
    Counter({'a': 1, 'b': 1})
    >>> c | d                       # phép hợp:  max(c[x], d[x])
    Counter({'a': 3, 'b': 2})
    >>> c == d                      # phép so sánh bằng:  c[x] == d[x]
    False
    >>> c <= d                      # phép bao hàm:  c[x] <= d[x]
    False

Phép cộng và phép trừ một ngôi là cách viết tắt của việc cộng với một counter rỗng hoặc trừ từ một counter rỗng.

    >>> c = Counter(a=2, b=-4)
    >>> +c
    Counter({'a': 2})
    >>> -c
    Counter({'b': 4})

.. versionadded:: 3.3
    Đã bổ sung hỗ trợ cho phép cộng một ngôi, phép trừ một ngôi và các phép toán multiset tại chỗ.

.. note::

    Counter chủ yếu được thiết kế để làm việc với các số nguyên dương nhằm biểu thị số đếm đang được cập nhật; tuy nhiên, việc sử dụng cho các trường hợp cần kiểu dữ liệu khác hoặc giá trị âm cũng không bị ngăn cản một cách không cần thiết. Để hỗ trợ các trường hợp đó, phần này trình bày các giới hạn tối thiểu về phạm vi và kiểu dữ liệu.

    * Lớp :class:`Counter` bản thân nó là một lớp con của dictionary, không đặt ra giới hạn nào đối với khóa và giá trị. Các giá trị được dùng để biểu thị số đếm, nhưng bạn *có thể* lưu bất kỳ thứ gì vào trường giá trị.

    * Phương thức :meth:`~Counter.most_common` chỉ yêu cầu các giá trị có thể được sắp thứ tự.

    * Đối với các phép toán tại chỗ như ``c[key] += 1``, kiểu giá trị chỉ cần hỗ trợ phép cộng và phép trừ. Vì vậy, phân số, số thực dấu phẩy động và số thập phân đều có thể hoạt động, đồng thời các giá trị âm cũng được hỗ trợ. Điều tương tự cũng đúng với
      :meth:`~Counter.update` và :meth:`~Counter.subtract`, cho phép các giá trị âm và bằng không ở cả đầu vào lẫn đầu ra.

    * Các phương thức multiset chỉ được thiết kế cho những trường hợp sử dụng với các giá trị dương. Đầu vào có thể là số âm hoặc bằng không, nhưng chỉ các đầu ra có giá trị dương mới được tạo ra. Không có giới hạn về kiểu dữ liệu, nhưng kiểu giá trị cần hỗ trợ phép cộng, phép trừ và phép so sánh.

    * Phương thức :meth:`~Counter.elements` yêu cầu các số lượng nguyên. Phương thức này bỏ qua các số lượng bằng không và âm.

.. seealso::

   * `lớp Bag <https://www.gnu.org/software/smalltalk/manual-base/html_node/Bag.html>`_ trong Smalltalk.

   * Mục Wikipedia về `Multisets <https://en.wikipedia.org/wiki/Multiset>`_.

   * Hướng dẫn về `multisets trong C++ <http://www.java2s.com/Tutorial/Cpp/0380__set-multiset/Catalog0380__set-multiset.htm>`_ kèm các ví dụ.

   * Để tìm hiểu về các phép toán toán học trên multisets và các trường hợp sử dụng chúng, hãy xem *Knuth, Donald. The Art of Computer Programming Volume II, Section 4.6.3, Exercise 19*.

   * Để liệt kê tất cả multisets khác nhau có kích thước cho trước trên một tập hợp phần tử cho trước, hãy xem :func:`itertools.combinations_with_replacement`::

        map(Counter, combinations_with_replacement('ABC', 2)) # --> AA AB AC BB BC CC


:class:`deque` đối tượng
------------------------

.. class:: deque([iterable, [maxlen]])

    Trả về một đối tượng deque mới được khởi tạo từ trái sang phải (bằng :meth:`append`) với dữ liệu từ *iterable*. Nếu *iterable* không được chỉ định, deque mới sẽ rỗng.

    Deque là sự khái quát hóa của stack và queue (tên này được phát âm là "deck" và là dạng viết tắt của "double-ended queue"). Deque hỗ trợ các thao tác append và pop an toàn với thread, tiết kiệm bộ nhớ từ cả hai đầu của deque, với hiệu năng *O*\ (1) xấp xỉ như nhau theo cả hai hướng.

    Mặc dù :class:`list` đối tượng hỗ trợ các thao tác tương tự, chúng được tối ưu hóa cho các thao tác có độ dài cố định nhanh và phải chịu chi phí di chuyển bộ nhớ *O*\ (*n*) đối với các thao tác ``pop(0)`` và ``insert(0, v)`` làm thay đổi cả kích thước lẫn vị trí của biểu diễn dữ liệu nền.


    Nếu *maxlen* không được chỉ định hoặc là ``None``, deque có thể tăng đến độ dài tùy ý. Nếu không, deque bị giới hạn ở độ dài tối đa đã chỉ định. Khi deque có độ dài giới hạn đã đầy, mỗi khi thêm các mục mới, một số lượng tương ứng các mục sẽ bị loại bỏ khỏi đầu đối diện. Deque có độ dài giới hạn cung cấp chức năng tương tự như ``tail`` bộ lọc trong Unix. Chúng cũng hữu ích để theo dõi các giao dịch và các tập dữ liệu khác mà chỉ hoạt động gần đây nhất mới đáng quan tâm.

    Các đối tượng Deque mang tính :ref:`generic <generics>` theo kiểu dữ liệu của nội dung bên trong.


    Các đối tượng Deque hỗ trợ những phương thức sau:

    .. method:: append(item, /)

        Thêm *item* vào phía bên phải của deque.


    .. method:: appendleft(item, /)

        Thêm *item* vào phía bên trái của deque.


    .. method:: clear()

        Xóa tất cả phần tử khỏi deque, khiến độ dài của nó bằng 0.


    .. method:: copy()

        Tạo một bản sao nông của deque.

        .. versionadded:: 3.5


    .. method:: count(value, /)

        Đếm số phần tử trong deque bằng *value*.

        .. versionadded:: 3.2


    .. method:: extend(iterable, /)

        Mở rộng phía bên phải của deque bằng cách nối thêm các phần tử từ đối số iterable.


    .. method:: extendleft(iterable, /)

        Mở rộng phía bên trái của deque bằng cách nối thêm các phần tử từ *iterable*. Lưu ý rằng chuỗi thao tác nối thêm vào bên trái sẽ đảo ngược thứ tự các phần tử trong đối số iterable.


    .. method:: index(value[, start[, stop]])

        Trả về vị trí của *value* trong deque (tại hoặc sau chỉ mục *start* và trước chỉ mục *stop*). Trả về kết quả khớp đầu tiên hoặc phát sinh
        :exc:`ValueError` nếu không tìm thấy.

        .. versionadded:: 3.5


    .. method:: insert(index, value, /)

        Chèn *value* vào deque tại vị trí *index*.

        Nếu thao tác chèn khiến deque bị giới hạn phát triển vượt quá *maxlen*, :exc:`IndexError` sẽ được phát sinh.

        .. versionadded:: 3.5


    .. method:: pop()

        Xóa và trả về một phần tử ở phía bên phải của deque. Nếu không có phần tử nào, phát sinh :exc:`IndexError`.


    .. method:: popleft()

        Xóa và trả về một phần tử ở phía bên trái của deque. Nếu không có phần tử nào, phát sinh :exc:`IndexError`.


    .. method:: remove(value, /)

        Xóa lần xuất hiện đầu tiên của *value*. Nếu không tìm thấy, phát sinh
        :exc:`ValueError`.


    .. method:: reverse()

        Đảo ngược các phần tử của deque tại chỗ rồi trả về ``None``.

        .. versionadded:: 3.2


    .. method:: rotate(n=1, /)

        Xoay deque *n* bước sang phải. Nếu *n* là số âm, hãy xoay sang trái.

        Khi deque không rỗng, xoay một bước sang phải tương đương với ``d.appendleft(d.pop())``, còn xoay một bước sang trái tương đương với ``d.append(d.popleft())``.


    Các đối tượng deque cũng cung cấp một thuộc tính chỉ đọc:

    .. attribute:: maxlen

        Kích thước tối đa của deque hoặc ``None`` nếu không giới hạn.

        .. versionadded:: 3.1


Ngoài các chức năng trên, deque còn hỗ trợ phép lặp, pickling, ``len(d)``, ``reversed(d)``, ``copy.copy(d)``, ``copy.deepcopy(d)``, kiểm tra phần tử với toán tử :keyword:`in`, và tham chiếu chỉ số con như ``d[0]`` để truy cập phần tử đầu tiên. Truy cập theo chỉ số có độ phức tạp *O*\ (1) ở cả hai đầu, nhưng chậm xuống *O*\ (*n*) ở giữa. Để truy cập ngẫu nhiên nhanh, hãy dùng list.

Bắt đầu từ phiên bản 3.5, deque hỗ trợ ``__add__()``, ``__mul__()`` và ``__imul__()``.

Ví dụ:

.. doctest::

    >>> from collections import deque
    >>> d = deque('ghi')                 # tạo một deque mới với ba phần tử
    >>> for elem in d:                   # lặp qua các phần tử của deque
    ...     print(elem.upper())
    G
    H
    I

    >>> d.append('j')                    # thêm một mục mới vào bên phải
    >>> d.appendleft('f')                # thêm một mục mới vào bên trái
    >>> d                                # hiển thị biểu diễn của deque
    deque(['f', 'g', 'h', 'i', 'j'])

    >>> d.pop()                          # trả về và xóa mục ngoài cùng bên phải
    'j'
    >>> d.popleft()                      # trả về và xóa phần tử ngoài cùng bên trái
    'f'
    >>> list(d)                          # liệt kê nội dung của deque
    ['g', 'h', 'i']
    >>> d[0]                             # xem phần tử ngoài cùng bên trái
    'g'
    >>> d[-1]                            # xem phần tử ngoài cùng bên phải
    'i'

    >>> list(reversed(d))                # liệt kê nội dung của deque theo thứ tự ngược lại
    ['i', 'h', 'g']
    >>> 'h' in d                         # tìm kiếm trong deque
    True
    >>> d.extend('jkl')                  # thêm nhiều phần tử cùng lúc
    >>> d
    deque(['g', 'h', 'i', 'j', 'k', 'l'])
    >>> d.rotate(1)                      # xoay phải
    >>> d
    deque(['l', 'g', 'h', 'i', 'j', 'k'])
    >>> d.rotate(-1)                     # xoay trái
    >>> d
    deque(['g', 'h', 'i', 'j', 'k', 'l'])

    >>> deque(reversed(d))               # tạo deque mới theo thứ tự đảo ngược
    deque(['l', 'k', 'j', 'i', 'h', 'g'])
    >>> d.clear()                        # làm rỗng deque
    >>> d.pop()                          # không thể pop từ deque rỗng
    Traceback (most recent call last):
        File "<pyshell#6>", line 1, in -toplevel-
            d.pop()
    IndexError: pop from an empty deque

    >>> d.extendleft('abc')              # extendleft() đảo ngược thứ tự đầu vào
    >>> d
    deque(['c', 'b', 'a'])


:class:`deque` Công thức
^^^^^^^^^^^^^^^^^^^^^^^^

Phần này trình bày nhiều cách tiếp cận khác nhau khi làm việc với deque.

Deque có độ dài giới hạn cung cấp chức năng tương tự bộ lọc ``tail`` trong Unix::

    def tail(filename, n=10):
        'Return the last n lines of a file'
        with open(filename) as f:
            return deque(f, n)

Một cách tiếp cận khác khi sử dụng deque là duy trì một chuỗi các phần tử mới được thêm vào bằng cách thêm vào bên phải và lấy ra từ bên trái::

    def moving_average(iterable, n=3):
        # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
        # https://en.wikipedia.org/wiki/Moving_average
        it = iter(iterable)
        d = deque(itertools.islice(it, n-1))
        d.appendleft(0)
        s = sum(d)
        for elem in it:
            s += elem - d.popleft()
            d.append(elem)
            yield s / n

Có thể triển khai `bộ lập lịch round-robin <https://en.wikipedia.org/wiki/Round-robin_scheduling>`_ bằng các iterator đầu vào được lưu trong một :class:`deque`. Các giá trị được trả về từ iterator đang hoạt động ở vị trí số không. Nếu iterator đó :term:`exhausted`, có thể xóa nó bằng :meth:`~deque.popleft`; nếu không, có thể đưa nó trở lại cuối bằng phương thức :meth:`~deque.rotate`::

    def roundrobin(*iterables):
        "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
        iterators = deque(map(iter, iterables))
        while iterators:
            try:
                while True:
                    yield next(iterators[0])
                    iterators.rotate(-1)
            except StopIteration:
                # Xóa iterator đã dùng hết.
                iterators.popleft()

Phương thức :meth:`~deque.rotate` cung cấp một cách để triển khai việc cắt lát và xóa :class:`deque`. Ví dụ: một triển khai thuần Python của ``del d[n]`` dựa vào phương thức ``rotate()`` để đưa các phần tử vào vị trí cần lấy ra::

    def delete_nth(d, n):
        d.rotate(-n)
        d.popleft()
        d.rotate(n)

Để triển khai việc cắt lát :class:`deque`, hãy sử dụng cách tiếp cận tương tự bằng cách áp dụng
:meth:`~deque.rotate` để đưa phần tử đích về phía bên trái của deque. Xóa các mục cũ bằng :meth:`~deque.popleft`, thêm các mục mới bằng :meth:`~deque.extend`, rồi đảo ngược phép xoay. Với một vài biến thể nhỏ của cách tiếp cận này, bạn có thể dễ dàng triển khai các thao tác ngăn xếp theo phong cách Forth như ``dup``, ``drop``, ``swap``, ``over``, ``pick``, ``rot`` và ``roll``.


Các đối tượng :class:`defaultdict`
----------------------------------

.. class:: defaultdict(default_factory=None, /, **kwargs)
           defaultdict(default_factory, mapping, /, ****kwargs) defaultdict(default_factory, iterable, /, ****kwargs)

    Trả về một đối tượng mới giống từ điển. :class:`defaultdict` là một lớp con của lớp :class:`dict` dựng sẵn. Lớp này ghi đè một phương thức và thêm một biến thực thể có thể ghi. Chức năng còn lại giống như chức năng của
    lớp :class:`dict` và không được mô tả ở đây.

    Đối số đầu tiên cung cấp giá trị ban đầu cho thuộc tính :attr:`default_factory`; theo mặc định, thuộc tính này là ``None``. Tất cả các đối số còn lại được xử lý giống như khi chúng được truyền cho hàm khởi tạo :class:`dict`, bao gồm cả các đối số từ khóa.

    :class:`!defaultdict`\s là :ref:`generic <generics>` trên hai kiểu, lần lượt biểu thị các kiểu của khóa và giá trị trong dictionary.


    Các đối tượng :class:`defaultdict` hỗ trợ phương thức sau, ngoài các thao tác :class:`dict` tiêu chuẩn:

    .. method:: __missing__(key, /)

        Nếu thuộc tính :attr:`default_factory` là ``None``, thao tác này sẽ phát sinh một
        ngoại lệ :exc:`KeyError` với *key* làm đối số.

        Nếu :attr:`default_factory` không phải là ``None``, nó được gọi không có đối số để cung cấp giá trị mặc định cho *key* đã cho; giá trị này được chèn vào dictionary cho *key*, rồi được trả về.

        Nếu việc gọi :attr:`default_factory` phát sinh một ngoại lệ, ngoại lệ này được truyền nguyên trạng.

        Phương thức này được gọi bởi phương thức :meth:`~object.__getitem__` của
        :class:`dict` lớp khi không tìm thấy khóa được yêu cầu; bất kỳ giá trị nào nó trả về hoặc ngoại lệ nào nó phát sinh sau đó cũng được :meth:`~object.__getitem__` trả về hoặc phát sinh.

        Lưu ý rằng :meth:`__missing__` *not* được gọi cho bất kỳ thao tác nào ngoài
        :meth:`~object.__getitem__`. Điều này có nghĩa là :meth:`~dict.get` sẽ, giống như các dictionary thông thường, trả về ``None`` theo mặc định thay vì sử dụng
        :attr:`default_factory`.


    Các đối tượng :class:`defaultdict` hỗ trợ biến instance sau:


    .. attribute:: default_factory

        Thuộc tính này được phương thức :meth:`~defaultdict.__missing__` sử dụng; nó được khởi tạo từ đối số đầu tiên của hàm khởi tạo, nếu có, hoặc được đặt thành ``None`` nếu không có.

    .. versionchanged:: 3.9
       Đã thêm các toán tử merge (``|``) và update (``|=``), được chỉ định trong
       :pep:`584`.


Các ví dụ về :class:`defaultdict`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dùng :class:`list` làm :attr:`~defaultdict.default_factory`, bạn có thể dễ dàng nhóm một chuỗi các cặp khóa-giá trị thành một dictionary gồm các list:

    >>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    >>> d = defaultdict(list)
    >>> for k, v in s:
    ...     d[k].append(v)
    ...
    >>> sorted(d.items())
    [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

Khi mỗi khóa được gặp lần đầu, khóa đó chưa có trong mapping; vì vậy một mục nhập được tự động tạo bằng hàm :attr:`~defaultdict.default_factory`, hàm này trả về một :class:`list` trống. Sau đó, thao tác :meth:`list.append` sẽ gắn giá trị vào list mới. Khi các khóa được gặp lại, việc tra cứu diễn ra bình thường (trả về list tương ứng với khóa đó) và
thao tác :meth:`list.append` thêm một giá trị khác vào list. Kỹ thuật này đơn giản và nhanh hơn kỹ thuật tương đương sử dụng :meth:`dict.setdefault`:

    >>> d = {}
    >>> for k, v in s:
    ...     d.setdefault(k, []).append(v)
    ...
    >>> sorted(d.items())
    [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

Đặt :attr:`~defaultdict.default_factory` thành :class:`int` khiến
:class:`defaultdict` hữu ích cho việc đếm (tương tự bag hoặc multiset trong các ngôn ngữ khác):

    >>> s = 'mississippi'
    >>> d = defaultdict(int)
    >>> for k in s:
    ...     d[k] += 1
    ...
    >>> sorted(d.items())
    [('i', 4), ('m', 1), ('p', 2), ('s', 4)]

Khi một chữ cái được gặp lần đầu, chữ cái đó không có trong mapping, vì vậy
hàm :attr:`~defaultdict.default_factory` gọi :func:`int` để cung cấp giá trị đếm mặc định bằng không. Sau đó, thao tác tăng dần sẽ xây dựng số đếm cho từng chữ cái.

Hàm :func:`int` luôn trả về số 0 chỉ là một trường hợp đặc biệt của các hàm hằng. Cách nhanh hơn và linh hoạt hơn để tạo các hàm hằng là sử dụng hàm lambda, có thể cung cấp bất kỳ giá trị hằng nào (không chỉ số 0):

    >>> def constant_factory(value):
    ...     return lambda: value
    ...
    >>> d = defaultdict(constant_factory('<missing>'))
    >>> d.update(name='John', action='ran')
    >>> '%(name)s %(action)s to %(object)s' % d
    'John ran to <missing>'

Đặt :attr:`~defaultdict.default_factory` thành :class:`set` khiến
:class:`defaultdict` trở nên hữu ích khi xây dựng một từ điển các tập hợp:

    >>> s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
    >>> d = defaultdict(set)
    >>> for k, v in s:
    ...     d[k].add(v)
    ...
    >>> sorted(d.items())
    [('blue', {2, 4}), ('red', {1, 3})]


Hàm Factory :func:`namedtuple` cho các tuple có trường được đặt tên
-------------------------------------------------------------------

Named tuple gán ý nghĩa cho từng vị trí trong một tuple và cho phép viết mã dễ đọc hơn, có khả năng tự mô tả. Chúng có thể được sử dụng ở bất cứ đâu có thể sử dụng tuple thông thường, đồng thời bổ sung khả năng truy cập các trường theo tên thay vì theo chỉ số vị trí.

.. function:: namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)

    Trả về một lớp con tuple mới có tên *typename*. Lớp con mới này được dùng để tạo các đối tượng giống tuple, có các trường có thể truy cập bằng tra cứu thuộc tính, đồng thời hỗ trợ lập chỉ mục và lặp. Các thực thể của lớp con cũng có một docstring hữu ích (với *typename* và *field_names*) cùng một phương thức hữu ích
    :meth:`~object.__repr__`, liệt kê nội dung tuple theo định dạng ``name=value``.

    *field_names* là một chuỗi các chuỗi, chẳng hạn như ``['x', 'y']``. Ngoài ra, *field_names* có thể là một chuỗi duy nhất, trong đó mỗi tên trường được phân tách bằng khoảng trắng và/hoặc dấu phẩy, chẳng hạn như ``'x y'`` hoặc ``'x, y'``.

    Có thể sử dụng bất kỳ Python identifier hợp lệ nào làm tên trường, ngoại trừ các tên bắt đầu bằng dấu gạch dưới. Identifier hợp lệ gồm các chữ cái, chữ số và dấu gạch dưới, nhưng không bắt đầu bằng chữ số hoặc dấu gạch dưới và không thể là :mod:`keyword` như *class*, *for*, *return*, *global*, *pass* hoặc *raise*.

    Nếu *rename* là true, các tên trường không hợp lệ sẽ tự động được thay thế bằng tên theo vị trí. Ví dụ, ``['abc', 'def', 'ghi', 'abc']`` được chuyển đổi thành ``['abc', '_1', 'ghi', '_3']``, loại bỏ từ khóa ``def`` và tên trường trùng lặp ``abc``.

    *defaults* có thể là ``None`` hoặc một :term:`iterable` các giá trị mặc định. Vì các trường có giá trị mặc định phải đứng sau mọi trường không có giá trị mặc định, *defaults* được áp dụng cho các tham số ngoài cùng bên phải. Ví dụ, nếu các tên trường là ``['x', 'y', 'z']`` và các giá trị mặc định là ``(1, 2)``, thì ``x`` sẽ là đối số bắt buộc, ``y`` sẽ nhận mặc định là ``1``, còn ``z`` sẽ nhận mặc định là ``2``.

    Nếu *module* được định nghĩa, thuộc tính :attr:`~type.__module__` của named tuple sẽ được đặt thành giá trị đó.

    Các instance của named tuple không có dictionary riêng cho từng instance, vì vậy chúng nhẹ và không cần nhiều bộ nhớ hơn tuple thông thường.

    Để hỗ trợ pickling, class named tuple nên được gán cho một biến trùng với *typename*.

    .. versionchanged:: 3.1
       Đã thêm hỗ trợ cho *rename*.

    .. versionchanged:: 3.6
       Các tham số *verbose* và *rename* trở thành
       :ref:`đối số chỉ dùng từ khóa <keyword-only_parameter>`.

    .. versionchanged:: 3.6
       Đã thêm tham số *module*.

    .. versionchanged:: 3.7
       Đã xóa tham số *verbose* và thuộc tính :attr:`!_source`.

    .. versionchanged:: 3.7
       Đã thêm tham số *defaults* và thuộc tính :attr:`~somenamedtuple._field_defaults`.

.. doctest::
    :options: +NORMALIZE_WHITESPACE

    >>> # Ví dụ cơ bản
    >>> Point = namedtuple('Point', ['x', 'y'])
    >>> p = Point(11, y=22)     # khởi tạo bằng đối số vị trí hoặc đối số từ khóa
    >>> p[0] + p[1]             # có thể lập chỉ mục như tuple thông thường (11, 22)
    33
    >>> x, y = p                # giải nén như tuple thông thường
    >>> x, y
    (11, 22)
    >>> p.x + p.y               # các trường cũng có thể được truy cập theo tên
    33
    >>> p                       # __repr__ dễ đọc theo kiểu name=value
    Point(x=11, y=22)

Named tuple đặc biệt hữu ích khi gán tên trường cho các tuple kết quả do các module :mod:`csv` hoặc :mod:`sqlite3` trả về::

    EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

    import csv
    for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
        print(emp.name, emp.title)

    import sqlite3
    conn = sqlite3.connect('/companydata')
    cursor = conn.cursor()
    cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
    for emp in map(EmployeeRecord._make, cursor.fetchall()):
        print(emp.name, emp.title)

Ngoài các phương thức được kế thừa từ tuple, named tuple còn hỗ trợ ba phương thức bổ sung và hai thuộc tính. Để tránh xung đột với tên trường, tên của các phương thức và thuộc tính bắt đầu bằng dấu gạch dưới.

.. classmethod:: somenamedtuple._make(iterable, /)

    Phương thức lớp tạo một instance mới từ một sequence hoặc iterable hiện có.

    .. doctest::

        >>> t = [11, 22]
        >>> Point._make(t)
        Point(x=11, y=22)

.. method:: somenamedtuple._asdict()

    Trả về một :class:`dict` mới ánh xạ tên trường tới các giá trị tương ứng:

    .. doctest::

        >>> p = Point(x=11, y=22)
        >>> p._asdict()
        {'x': 11, 'y': 22}

    .. versionchanged:: 3.1
        Trả về một :class:`OrderedDict` thay vì một :class:`dict` thông thường.

    .. versionchanged:: 3.8
        Trả về một :class:`dict` thông thường thay vì một :class:`OrderedDict`. Kể từ Python 3.7, dict thông thường được đảm bảo giữ thứ tự. Nếu cần các tính năng bổ sung của :class:`OrderedDict`, cách khắc phục được đề xuất là ép kiểu kết quả sang kiểu mong muốn: ``OrderedDict(nt._asdict())``.

.. method:: somenamedtuple._replace(**kwargs)

    Trả về một instance mới của named tuple, trong đó các trường được chỉ định được thay thế bằng các giá trị mới::

        >>> p = Point(x=11, y=22)
        >>> p._replace(x=33)
        Point(x=33, y=22)

        >>> for partnum, record in inventory.items():
        ...     inventory[partnum] = record._replace(price=newprices[partnum], timestamp=time.now())

    Named tuple cũng được hỗ trợ bởi generic function :func:`copy.replace`.

    .. versionchanged:: 3.13
       Phát sinh :exc:`TypeError` thay vì :exc:`ValueError` đối với các đối số keyword không hợp lệ.

.. attribute:: somenamedtuple._fields

    Tuple các chuỗi liệt kê tên trường. Hữu ích cho việc introspection và tạo các kiểu named tuple mới từ các named tuple hiện có.

    .. doctest::

        >>> p._fields            # xem tên các trường
        ('x', 'y')

        >>> Color = namedtuple('Color', 'red green blue')
        >>> Pixel = namedtuple('Pixel', Point._fields + Color._fields)
        >>> Pixel(11, 22, 128, 255, 0)
        Pixel(x=11, y=22, red=128, green=255, blue=0)

.. attribute:: somenamedtuple._field_defaults

   Dictionary ánh xạ tên trường với các giá trị mặc định.

   .. doctest::

        >>> Account = namedtuple('Account', ['type', 'balance'], defaults=[0])
        >>> Account._field_defaults
        {'balance': 0}
        >>> Account('premium')
        Account(type='premium', balance=0)

Để truy xuất một trường có tên được lưu trong một chuỗi, hãy sử dụng hàm :func:`getattr`:

    >>> getattr(p, 'x')
    11

Để chuyển đổi một dictionary thành named tuple, hãy sử dụng toán tử hai dấu sao (như được mô tả trong :ref:`tut-unpacking-arguments`):

    >>> d = {'x': 11, 'y': 22}
    >>> Point(**d)
    Point(x=11, y=22)

Vì named tuple là một lớp Python thông thường, bạn có thể dễ dàng thêm hoặc thay đổi chức năng bằng một subclass. Sau đây là cách thêm một trường được tính toán và một định dạng in có độ rộng cố định:

.. doctest::

    >>> class Point(namedtuple('Point', ['x', 'y'])):
    ...     __slots__ = ()
    ...     @property
    ...     def hypot(self):
    ...         return (self.x ** 2 + self.y ** 2) ** 0.5
    ...     def __str__(self):
    ...         return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)

    >>> for p in Point(3, 4), Point(14, 5/7):
    ...     print(p)
    Point: x= 3.000  y= 4.000  hypot= 5.000
    Point: x=14.000  y= 0.714  hypot=14.018

Subclass ở trên đặt ``__slots__`` thành một tuple rỗng. Điều này giúp giảm yêu cầu bộ nhớ bằng cách ngăn việc tạo các dictionary của instance.

Việc tạo lớp con không hữu ích khi thêm các trường được lưu trữ mới. Thay vào đó, chỉ cần tạo một kiểu tuple có tên mới từ thuộc tính :attr:`~somenamedtuple._fields`:

    >>> Point3D = namedtuple('Point3D', Point._fields + ('z',))

Có thể tùy chỉnh docstring bằng cách gán trực tiếp cho các trường ``__doc__``:

   >>> Book = namedtuple('Book', ['id', 'title', 'authors'])
   >>> Book.__doc__ += ': Hardcover book in active collection'
   >>> Book.id.__doc__ = '13-digit ISBN'
   >>> Book.title.__doc__ = 'Title of first printing'
   >>> Book.authors.__doc__ = 'List of authors sorted by last name'

.. versionchanged:: 3.5
   Docstring của thuộc tính đã có thể ghi được.

.. seealso::

   * Xem :class:`typing.NamedTuple` để biết cách thêm type hints cho các tuple có tên. Nó cũng cung cấp ký hiệu tao nhã bằng từ khóa :keyword:`class`::

         class Component(NamedTuple):
             part_number: int
             weight: float
             description: Optional[str] = None

   * Xem :meth:`types.SimpleNamespace` để biết một namespace có thể thay đổi dựa trên dictionary bên dưới thay vì tuple.

   * Mô-đun :mod:`dataclasses` cung cấp một decorator và các hàm để tự động thêm những special method được tạo tự động vào các lớp do người dùng định nghĩa.


Các đối tượng :class:`OrderedDict`
----------------------------------

Ordered dictionaries cũng giống như các dictionary thông thường nhưng có thêm một số khả năng liên quan đến các thao tác sắp xếp. Chúng trở nên kém quan trọng hơn kể từ khi lớp :class:`dict` tích hợp sẵn có khả năng ghi nhớ thứ tự chèn (hành vi mới này được đảm bảo trong Python 3.7).

Một số điểm khác biệt so với :class:`dict` vẫn còn tồn tại:

* :class:`dict` thông thường được thiết kế để thực hiện rất tốt các thao tác ánh xạ. Việc theo dõi thứ tự chèn chỉ là ưu tiên thứ yếu.

* :class:`OrderedDict` được thiết kế để thực hiện tốt các thao tác sắp xếp lại. Hiệu quả sử dụng bộ nhớ, tốc độ lặp và hiệu năng của các thao tác cập nhật là những ưu tiên thứ yếu.

* Thuật toán của :class:`OrderedDict` có thể xử lý các thao tác sắp xếp lại thường xuyên tốt hơn :class:`dict`. Như được minh họa trong các công thức bên dưới, điều này khiến nó phù hợp để triển khai nhiều loại bộ nhớ đệm LRU.

* Thao tác so sánh bằng của :class:`OrderedDict` kiểm tra xem thứ tự có trùng khớp hay không.

  Một :class:`dict` thông thường có thể mô phỏng phép kiểm tra bằng nhạy với thứ tự bằng ``p == q and all(k1 == k2 for k1, k2 in zip(p, q))``.

* Phương thức :meth:`~OrderedDict.popitem` của :class:`OrderedDict` có chữ ký khác. Phương thức này nhận một đối số tùy chọn để chỉ định mục được lấy ra.

  Một :class:`dict` thông thường có thể mô phỏng ``od.popitem(last=True)`` của OrderedDict bằng ``d.popitem()``, phương thức được đảm bảo sẽ lấy ra mục ngoài cùng bên phải (cuối cùng).

  Một :class:`dict` thông thường có thể mô phỏng ``od.popitem(last=False)`` của OrderedDict bằng ``(k := next(iter(d)), d.pop(k))``, phương thức sẽ trả về và xóa mục ngoài cùng bên trái (đầu tiên) nếu mục đó tồn tại.

* :class:`OrderedDict` có phương thức :meth:`~OrderedDict.move_to_end` để định vị lại một phần tử đến một đầu một cách hiệu quả.

  Một :class:`dict` thông thường có thể mô phỏng ``od.move_to_end(k, last=True)`` của OrderedDict bằng ``d[k] = d.pop(k)``, phương thức sẽ di chuyển khóa và giá trị liên kết với khóa đó đến vị trí ngoài cùng bên phải (cuối cùng).

  Một :class:`dict` thông thường không có cách tương đương hiệu quả với ``od.move_to_end(k, last=False)`` của OrderedDict, phương thức di chuyển khóa và giá trị liên kết với khóa đó đến vị trí ngoài cùng bên trái (đầu tiên).

* Cho đến Python 3.8, :class:`dict` không có phương thức :meth:`~object.__reversed__`.


.. class:: OrderedDict(**kwargs)
           OrderedDict(mapping, /, ****kwargs) OrderedDict(iterable, /, ****kwargs)

    Trả về một thể hiện của lớp con :class:`dict` có các phương thức được chuyên biệt hóa để sắp xếp lại thứ tự từ điển.

    .. versionadded:: 3.1

    .. method:: popitem(last=True)

        Phương thức :meth:`popitem` của các từ điển có thứ tự trả về và loại bỏ một cặp (khóa, giá trị). Các cặp được trả về theo
        thứ tự :abbr:`LIFO (vào sau, ra trước)` nếu *last* là true hoặc theo thứ tự :abbr:`FIFO (vào trước, ra trước)` nếu là false.

    .. method:: move_to_end(key, last=True)

        Di chuyển một *khóa* hiện có đến một trong hai đầu của từ điển có thứ tự. Mục này được di chuyển đến cuối bên phải nếu *last* là true (mặc định) hoặc đến đầu nếu *last* là false. Phát sinh :exc:`KeyError` nếu *khóa* không tồn tại:

        .. doctest::

            >>> d = OrderedDict.fromkeys('abcde')
            >>> d.move_to_end('b')
            >>> ''.join(d)
            'acdeb'
            >>> d.move_to_end('b', last=False)
            >>> ''.join(d)
            'bacde'

        .. versionadded:: 3.2

Ngoài các phương thức ánh xạ thông thường, các từ điển có thứ tự cũng hỗ trợ lặp ngược bằng cách sử dụng :func:`reversed`.

.. _collections_OrderedDict__eq__:

Các phép kiểm tra tính bằng nhau giữa các đối tượng :class:`OrderedDict` có xét đến thứ tự và gần tương đương với ``list(od1.items())==list(od2.items())``.

Các phép kiểm tra tính bằng giữa các đối tượng :class:`OrderedDict` và các đối tượng khác
Các đối tượng :class:`~collections.abc.Mapping` không phụ thuộc vào thứ tự, giống như các dictionary thông thường. Điều này cho phép thay thế các đối tượng :class:`OrderedDict` ở bất kỳ nơi nào sử dụng một dictionary thông thường.

.. versionchanged:: 3.5
   Các :term:`view <dictionary view>` items, keys và values của :class:`OrderedDict` hiện hỗ trợ lặp ngược bằng :func:`reversed`.

.. versionchanged:: 3.6
   Với việc chấp nhận :pep:`468`, thứ tự được giữ nguyên đối với các keyword argument truyền vào constructor :class:`OrderedDict` và phương thức :meth:`~dict.update` của nó.

.. versionchanged:: 3.9
   Đã thêm các toán tử merge (``|``) và update (``|=``), được đặc tả trong :pep:`584`.


:class:`OrderedDict` Ví dụ và công thức
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dễ dàng tạo một biến thể dictionary có thứ tự, ghi nhớ thứ tự các key được *chèn cuối cùng*. Nếu một entry mới ghi đè lên entry hiện có, vị trí chèn ban đầu sẽ được thay đổi và chuyển xuống cuối::

    class LastUpdatedOrderedDict(OrderedDict):
        'Store items in the order the keys were last added'

        def __setitem__(self, key, value):
            super().__setitem__(key, value)
            self.move_to_end(key)

Một :class:`OrderedDict` cũng sẽ hữu ích để triển khai các biến thể của :deco:`functools.lru_cache`:

.. testcode::

    from collections import OrderedDict
    from time import monotonic

    class TimeBoundedLRU:
        "LRU Cache that invalidates and refreshes old entries."

        def __init__(self, func, maxsize=128, maxage=30):
            self.cache = OrderedDict()      # { args : (timestamp, result)}
            self.func = func
            self.maxsize = maxsize
            self.maxage = maxage

        def __call__(self, *args):
            if args in self.cache:
                self.cache.move_to_end(args)
                timestamp, result = self.cache[args]
                if monotonic() - timestamp <= self.maxage:
                    return result
            result = self.func(*args)
            self.cache[args] = monotonic(), result
            if len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
            return result


.. testcode::

    class MultiHitLRUCache:
        """ LRU cache that defers caching a result until
            it has been requested multiple times.

            To avoid flushing the LRU cache with one-time requests,
            we don't cache until a request has been made more than once.

        """

        def __init__(self, func, maxsize=128, maxrequests=4096, cache_after=1):
            self.requests = OrderedDict()   # { uncached_key : request_count }
            self.cache = OrderedDict()      # { cached_key : function_result }
            self.func = func
            self.maxrequests = maxrequests  # số request chưa được cache tối đa
            self.maxsize = maxsize          # số giá trị trả về được lưu trữ tối đa
            self.cache_after = cache_after

        def __call__(self, *args):
            if args in self.cache:
                self.cache.move_to_end(args)
                return self.cache[args]
            result = self.func(*args)
            self.requests[args] = self.requests.get(args, 0) + 1
            if self.requests[args] <= self.cache_after:
                self.requests.move_to_end(args)
                if len(self.requests) > self.maxrequests:
                    self.requests.popitem(last=False)
            else:
                self.requests.pop(args, None)
                self.cache[args] = result
                if len(self.cache) > self.maxsize:
                    self.cache.popitem(last=False)
            return result

.. doctest::
    :hide:

    >>> def square(x):
    ...     return x * x
    ...
    >>> f = MultiHitLRUCache(square, maxsize=4, maxrequests=6)
    >>> list(map(f, range(10)))  # Các request đầu tiên, không cache
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    >>> f(4)  # Lưu yêu cầu thứ hai vào cache
    16
    >>> f(6)  # Lưu yêu cầu thứ hai vào cache
    36
    >>> f(2)  # Yêu cầu đầu tiên đã hết hạn, nên không lưu vào cache
    4
    >>> f(6)  # Cache hit
    36
    >>> f(4)  # Cache hit và chuyển lên đầu
    16
    >>> list(f.cache.values())
    [36, 16]
    >>> set(f.requests).isdisjoint(f.cache)
    True
    >>> list(map(f, [9, 8, 7]))   # Lưu các yêu cầu thứ hai này vào cache
    [81, 64, 49]
    >>> list(map(f, [7, 9]))  # Cache hits
    [49, 81]
    >>> list(f.cache.values())
    [16, 64, 49, 81]
    >>> set(f.requests).isdisjoint(f.cache)
    True

Các đối tượng :class:`UserDict`
-------------------------------

Lớp :class:`UserDict` hoạt động như một lớp bọc quanh các đối tượng dictionary. Nhu cầu về lớp này phần nào đã được thay thế bằng khả năng trực tiếp tạo lớp con từ :class:`dict`; tuy nhiên, lớp này có thể dễ làm việc hơn vì dictionary bên dưới có thể được truy cập dưới dạng một thuộc tính.

.. class:: UserDict(**kwargs)
           UserDict(mapping, /, ****kwargs) UserDict(iterable, /, ****kwargs)

    Lớp mô phỏng một dictionary. Nội dung của instance được lưu trong một dictionary thông thường, có thể truy cập thông qua thuộc tính :attr:`data` của
    :class:`!UserDict`. Nếu cung cấp đối số, chúng được dùng để khởi tạo :attr:`data`, giống như với một dictionary thông thường.

    Ngoài việc hỗ trợ các phương thức và phép toán của mapping,
    các instance :class:`!UserDict` cung cấp thuộc tính sau:

    .. attribute:: data

        Một dictionary thực được dùng để lưu trữ nội dung của lớp :class:`UserDict`.



Các đối tượng :class:`UserList`
-------------------------------

Lớp này hoạt động như một wrapper cho các đối tượng list. Đây là một lớp cơ sở hữu ích cho các lớp giống list của riêng bạn, cho phép chúng kế thừa từ lớp này rồi ghi đè các phương thức hiện có hoặc thêm phương thức mới. Theo cách này, bạn có thể thêm hành vi mới cho list.

Nhu cầu sử dụng lớp này phần nào đã giảm do khả năng tạo lớp con trực tiếp từ :class:`list`; tuy nhiên, lớp này có thể dễ làm việc hơn vì list bên dưới có thể được truy cập dưới dạng một thuộc tính.

.. class:: UserList([list])

    Lớp mô phỏng một list. Nội dung của instance được lưu trong một list thông thường, có thể truy cập thông qua thuộc tính :attr:`data` của các instance :class:`UserList`. Nội dung của instance ban đầu được đặt thành một bản sao của *list*, mặc định là list rỗng ``[]``. *list* có thể là bất kỳ iterable nào, chẳng hạn như một list Python thực hoặc một đối tượng :class:`UserList`.

    Ngoài việc hỗ trợ các phương thức và phép toán của các sequence có thể thay đổi,
    các instance :class:`UserList` cung cấp thuộc tính sau:

    .. attribute:: data

        Một đối tượng :class:`list` thực được dùng để lưu nội dung của
        lớp :class:`UserList`.

**Yêu cầu khi phân lớp:** Các lớp con của :class:`UserList` được kỳ vọng cung cấp một hàm khởi tạo có thể được gọi mà không có đối số hoặc với một đối số. Các thao tác trên danh sách trả về một sequence mới sẽ cố gắng tạo một instance của lớp triển khai thực tế. Để thực hiện việc này, nó giả định rằng hàm khởi tạo có thể được gọi với một tham số duy nhất, là một đối tượng sequence được dùng làm nguồn dữ liệu.

Nếu một lớp dẫn xuất không muốn tuân thủ yêu cầu này, cần ghi đè tất cả các phương thức đặc biệt được lớp này hỗ trợ; hãy tham khảo mã nguồn để biết thông tin về các phương thức cần cung cấp trong trường hợp đó.

Các đối tượng :class:`UserString`
---------------------------------

Lớp :class:`UserString` hoạt động như một wrapper quanh các đối tượng chuỗi. Nhu cầu về lớp này đã phần nào được thay thế bởi khả năng kế thừa trực tiếp từ :class:`str`; tuy nhiên, lớp này có thể dễ làm việc hơn vì chuỗi bên dưới có thể được truy cập dưới dạng một thuộc tính.

.. class:: UserString(seq)

    Lớp mô phỏng một đối tượng chuỗi. Nội dung của instance được lưu trong một đối tượng chuỗi thông thường, có thể truy cập thông qua
    :attr:`data` thuộc tính của các thực thể :class:`UserString`.  Nội dung của thực thể ban đầu được đặt thành một bản sao của *seq*.  Đối số *seq* có thể là bất kỳ đối tượng nào có thể được chuyển đổi thành một chuỗi bằng cách sử dụng hàm dựng sẵn
    :func:`str`.

    Ngoài việc hỗ trợ các phương thức và phép toán của chuỗi,
    các đối tượng :class:`UserString` cung cấp thuộc tính sau:

    .. attribute:: data

        Một đối tượng :class:`str` thực được dùng để lưu trữ nội dung của lớp
        :class:`UserString`.

    .. versionchanged:: 3.5
       Các phương thức mới ``__getnewargs__``, ``__rmod__``, ``casefold``, ``format_map``, ``isprintable`` và ``maketrans``.

.. _`MultiContext class`: https://github.com/enthought/codetools/blob/4.0.0/codetools/contexts/multi_context.py
.. _`CodeTools package`: https://github.com/enthought/codetools
.. _`Context class`: https://github.com/django/django/blob/main/django/template/context.py
.. _`Nested Contexts recipe`: https://code.activestate.com/recipes/577434-nested-contexts-a-chain-of-mapping-objects/
.. _`greatly simplified read-only version of Chainmap`: https://code.activestate.com/recipes/305268/
.. _`Bag class`: https://www.gnu.org/software/smalltalk/manual-base/html_node/Bag.html
.. _`Multisets`: https://en.wikipedia.org/wiki/Multiset
.. _`C++ multisets`: http://www.java2s.com/Tutorial/Cpp/0380__set-multiset/Catalog0380__set-multiset.htm
.. _`round-robin scheduler`: https://en.wikipedia.org/wiki/Round-robin_scheduling
