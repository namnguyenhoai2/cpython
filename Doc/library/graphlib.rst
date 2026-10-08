:mod:`!graphlib` --- Chức năng làm việc với các cấu trúc dạng đồ thị
====================================================================

.. module:: graphlib
   :synopsis: Chức năng làm việc với các cấu trúc dạng đồ thị


**Mã nguồn:** :source:`Lib/graphlib.py`

.. testsetup:: default

   import graphlib
   from graphlib import *

--------------


.. class:: TopologicalSorter(graph=None)

   Cung cấp chức năng sắp xếp topo một đồ thị gồm các nút :term:`hashable`.

   Thứ tự topo là thứ tự tuyến tính của các đỉnh trong một đồ thị sao cho với mọi cạnh có hướng u -> v từ đỉnh u đến đỉnh v, đỉnh u đứng trước đỉnh v trong thứ tự đó. Ví dụ, các đỉnh của đồ thị có thể biểu diễn những tác vụ cần thực hiện, còn các cạnh có thể biểu diễn các ràng buộc rằng một tác vụ phải được thực hiện trước tác vụ khác; trong ví dụ này, thứ tự topo đơn giản là một chuỗi tác vụ hợp lệ. Có thể tạo một thứ tự topo đầy đủ khi và chỉ khi đồ thị không có chu trình có hướng, tức là khi đó là một đồ thị có hướng không chu trình.

   Nếu cung cấp đối số tùy chọn *graph*, đối số này phải là một dictionary biểu diễn một đồ thị có hướng không chu trình, trong đó các khóa là các nút và các giá trị là các iterable chứa tất cả nút tiền nhiệm của nút đó trong đồ thị (các nút có cạnh trỏ đến giá trị nằm trong khóa). Có thể thêm các nút khác vào đồ thị bằng phương thức :meth:`~TopologicalSorter.add`.

   Trong trường hợp tổng quát, các bước cần thực hiện để sắp xếp một đồ thị đã cho như sau:

   * Tạo một thực thể của :class:`TopologicalSorter` với một graph ban đầu tùy chọn.
   * Thêm các node bổ sung vào graph.
   * Gọi :meth:`~TopologicalSorter.prepare` trên graph.
   * Trong khi :meth:`~TopologicalSorter.is_active` là ``True``, lặp qua các node do :meth:`~TopologicalSorter.get_ready` trả về và xử lý chúng. Gọi :meth:`~TopologicalSorter.done` trên mỗi node khi node đó xử lý xong.

   Nếu chỉ cần sắp xếp ngay lập tức các node trong graph và không có xử lý song song, có thể sử dụng trực tiếp phương thức tiện ích
   :meth:`TopologicalSorter.static_order`:

   .. doctest::

       >>> graph = {"D": {"B", "C"}, "C": {"A"}, "B": {"A"}}
       >>> ts = TopologicalSorter(graph)
       >>> tuple(ts.static_order())
       ('A', 'C', 'B', 'D')

   Lớp này được thiết kế để dễ dàng hỗ trợ việc xử lý song song các node ngay khi chúng sẵn sàng. Ví dụ::

       topological_sorter = TopologicalSorter()

       # Thêm các node vào 'topological_sorter'...

       topological_sorter.prepare()
       while topological_sorter.is_active():
           for node in topological_sorter.get_ready():
               # Các worker thread hoặc process lấy các node cần xử lý từ
               # queue 'task_queue'.
               task_queue.put(node)

           # Khi hoàn tất công việc với một node, các worker đặt node đó vào
           # 'finalized_tasks_queue' để chúng ta có thể lấy thêm các node cần xử lý.
           # Định nghĩa của 'is_active()' đảm bảo rằng tại thời điểm này, ít
           # nhất một node đã được đặt vào 'task_queue' nhưng vẫn chưa
           # đã được truyền vào 'done()', vì vậy lệnh 'get()' blocking này cuối cùng phải
           # thành công. Sau khi gọi 'done()', chúng ta quay lại để gọi 'get_ready()'
           # một lần nữa, vì vậy hãy đưa các node mới được giải phóng vào 'task_queue' ngay khi
           # có thể về mặt logic.
           node = finalized_tasks_queue.get()
           topological_sorter.done(node)

   .. method:: add(node, *predecessors)

      Thêm một nút mới và các nút tiền nhiệm của nó vào đồ thị. Cả *nút* và tất cả các phần tử trong *các nút tiền nhiệm* đều phải là :term:`hashable`.

      Nếu được gọi nhiều lần với cùng một đối số node, tập dependency sẽ là hợp của tất cả dependency được truyền vào.

      Có thể thêm một node không có dependency (không cung cấp *predecessors*) hoặc cung cấp một dependency hai lần. Nếu một node chưa từng được cung cấp trước đó xuất hiện trong *predecessors*, node đó sẽ tự động được thêm vào graph mà không có predecessor nào của riêng nó.

      Đưa ra :exc:`ValueError` nếu được gọi sau :meth:`~TopologicalSorter.prepare`.

   .. method:: prepare()

      Đánh dấu đồ thị là đã hoàn tất và kiểm tra các chu kỳ trong đồ thị. Nếu phát hiện bất kỳ chu kỳ nào, :exc:`CycleError` sẽ được đưa ra, nhưng
      :meth:`~TopologicalSorter.get_ready` vẫn có thể được sử dụng để lấy nhiều node nhất có thể cho đến khi các chu kỳ ngăn cản tiến trình tiếp theo. Sau khi gọi hàm này, đồ thị không thể được sửa đổi, vì vậy không thể thêm node nào nữa bằng :meth:`~TopologicalSorter.add`.

      :exc:`ValueError` sẽ được đưa ra nếu quá trình sắp xếp đã được bắt đầu bởi
      :meth:`~.static_order` hoặc :meth:`~.get_ready`.

      .. versionchanged:: 3.14

         Giờ đây có thể gọi ``prepare()`` nhiều hơn một lần miễn là quá trình sắp xếp chưa bắt đầu. Trước đây, thao tác này sẽ đưa ra :exc:`ValueError`.

   .. method:: is_active()

      Trả về ``True`` nếu có thể thực hiện thêm tiến triển và ``False`` trong trường hợp ngược lại. Có thể thực hiện thêm tiến triển nếu các chu kỳ không cản trở việc phân giải và vẫn còn các node sẵn sàng chưa được ``False`` trả về
      :meth:`TopologicalSorter.get_ready` hoặc số nút được đánh dấu
      :meth:`TopologicalSorter.done` nhỏ hơn số lượng đã được trả về bởi :meth:`TopologicalSorter.get_ready`.

      Phương thức :meth:`~object.__bool__` của lớp này ủy quyền cho hàm này, vì vậy thay vì::

          if ts.is_active():
              ...

      chỉ cần thực hiện::

          if ts:
              ...

      Phát sinh :exc:`ValueError` nếu được gọi mà chưa gọi
      :meth:`~TopologicalSorter.prepare` trước đó.

   .. method:: done(*nodes)

      Đánh dấu một tập hợp các nút được :meth:`TopologicalSorter.get_ready` trả về là đã xử lý, bỏ chặn mọi nút kế nhiệm của từng nút trong *nodes* để chúng được trả về trong tương lai bởi một lệnh gọi tới :meth:`TopologicalSorter.get_ready`.

      Ném :exc:`ValueError` nếu bất kỳ node nào trong *nodes* đã được đánh dấu là đã xử lý bởi một lần gọi trước đó đến phương thức này, hoặc nếu một node chưa được thêm vào graph bằng cách sử dụng :meth:`TopologicalSorter.add`, nếu được gọi mà không gọi :meth:`~TopologicalSorter.prepare`, hoặc nếu node chưa được :meth:`~TopologicalSorter.get_ready` trả về.

   .. method:: get_ready()

      Trả về một ``tuple`` chứa tất cả các node đã sẵn sàng. Ban đầu, nó trả về tất cả các node không có predecessor, và sau khi các node đó được đánh dấu là đã xử lý bằng cách gọi :meth:`TopologicalSorter.done`, những lần gọi tiếp theo sẽ trả về tất cả các node mới có toàn bộ predecessor đã được xử lý. Khi không thể thực hiện thêm tiến triển nào, các tuple rỗng sẽ được trả về.

      Phát sinh :exc:`ValueError` nếu được gọi mà chưa gọi
      :meth:`~TopologicalSorter.prepare` trước đó.

   .. method:: static_order()

      Trả về một đối tượng iterator sẽ lặp qua các node theo thứ tự tô pô. Khi sử dụng phương thức này, không nên gọi :meth:`~TopologicalSorter.prepare` và
      không nên gọi :meth:`~TopologicalSorter.done`. Phương thức này tương đương với::

          def static_order(self):
              self.prepare()
              while self.is_active():
                  node_group = self.get_ready()
                  yield from node_group
                  self.done(*node_group)

      Thứ tự cụ thể được trả về có thể phụ thuộc vào thứ tự cụ thể mà các mục được chèn vào graph. Ví dụ:

      .. doctest::

          >>> ts = TopologicalSorter()
          >>> ts.add(3, 2, 1)
          >>> ts.add(1, 0)
          >>> print([*ts.static_order()])
          [2, 0, 1, 3]

          >>> ts2 = TopologicalSorter()
          >>> ts2.add(1, 0)
          >>> ts2.add(3, 2, 1)
          >>> print([*ts2.static_order()])
          [0, 2, 1, 3]

      Điều này là do "0" và "2" nằm cùng một cấp trong đồ thị (chúng sẽ được trả về trong cùng một lần gọi đến
      :meth:`~TopologicalSorter.get_ready`) và thứ tự giữa chúng được xác định bởi thứ tự chèn.


      Nếu phát hiện bất kỳ chu trình nào, :exc:`CycleError` sẽ được raise.

   .. versionadded:: 3.9


Ngoại lệ
--------
Module :mod:`!graphlib` định nghĩa các lớp ngoại lệ sau:

.. exception:: CycleError

   Lớp con của :exc:`ValueError`, được :meth:`TopologicalSorter.prepare` raise nếu có chu trình trong đồ thị đang xử lý. Nếu tồn tại nhiều chu trình, chỉ một lựa chọn không xác định trong số đó sẽ được báo cáo và đưa vào ngoại lệ.

   Có thể truy cập chu trình được phát hiện thông qua phần tử thứ hai trong thuộc tính :attr:`~BaseException.args` của instance ngoại lệ, và chu trình này gồm một danh sách các node, sao cho mỗi node là predecessor trực tiếp của node tiếp theo trong danh sách ở trong đồ thị. Trong danh sách được báo cáo, node đầu tiên và node cuối cùng sẽ giống nhau, để thể hiện rõ rằng đó là chu trình.
