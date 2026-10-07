.. highlight:: c

.. _life-cycle:

Vòng đời đối tượng
==================

Phần này giải thích cách các slot của một type liên quan với nhau trong suốt vòng đời của một đối tượng. Phần này không nhằm cung cấp tài liệu tham chiếu chính thức đầy đủ về các slot; thay vào đó, hãy tham khảo tài liệu dành riêng cho từng slot trong
:ref:`type-structs` để biết chi tiết về một slot cụ thể.


Các sự kiện trong vòng đời
--------------------------

Hình bên dưới minh họa thứ tự các sự kiện có thể xảy ra trong suốt vòng đời của một đối tượng. Mũi tên từ *A* đến *B* cho biết sự kiện *B* có thể xảy ra sau khi sự kiện *A* đã xảy ra, trong đó nhãn của mũi tên cho biết điều kiện phải đúng để *B* xảy ra sau *A*.

.. only:: builder_html

   .. raw:: html

      <style type="text/css">

   .. raw:: html
      :file: lifecycle.dot.css


   .. raw:: html

      </style>

   .. raw:: html
      :file: lifecycle.dot.svg


   .. raw:: html

      <script>
          (() => {
              const g = document.getElementById('life_events_graph');
              const title = g.querySelector(':scope > title');
              title.id = 'life-events-graph-title';
              const svg = g.closest('svg');
              svg.role = 'img';
              svg.setAttribute('aria-describedby',
                               'life-events-graph-description');
              svg.setAttribute('aria-labelledby', 'life-events-graph-title');
          })();
      </script>

.. only:: not builder_html

   .. image:: lifecycle.dot.svg
      :align: center
      :class: invert-in-dark-mode
      :alt: Sơ đồ minh họa các sự kiện trong vòng đời của một đối tượng. Được giải thích chi tiết bên dưới.

.. container::
   :name: life-events-graph-description

   Giải thích:

   * Khi một đối tượng mới được tạo bằng cách gọi kiểu của nó:

     #. :c:member:`~PyTypeObject.tp_new` được gọi để tạo một đối tượng mới.
     #. :c:member:`~PyTypeObject.tp_alloc` được gọi trực tiếp bởi
        :c:member:`~PyTypeObject.tp_new` để cấp phát bộ nhớ cho đối tượng mới.
     #. :c:member:`~PyTypeObject.tp_init` khởi tạo đối tượng vừa được tạo.
        :c:member:`!tp_init` có thể được gọi lại để khởi tạo lại một đối tượng nếu muốn. Lời gọi :c:member:`!tp_init` cũng có thể được bỏ qua hoàn toàn, chẳng hạn như khi mã Python gọi :py:meth:`~object.__new__`.

   * Sau khi :c:member:`!tp_init` hoàn tất, đối tượng đã sẵn sàng để sử dụng.
   * Một thời gian sau khi tham chiếu cuối cùng đến một đối tượng bị loại bỏ:

     #. Nếu một đối tượng không được đánh dấu là *finalized*, đối tượng đó có thể được finalized bằng cách đánh dấu là *finalized* và gọi
        hàm :c:member:`~PyTypeObject.tp_finalize`. Python *không* finalized một đối tượng khi tham chiếu cuối cùng đến đối tượng đó bị xóa; hãy dùng
        :c:func:`PyObject_CallFinalizerFromDealloc` để đảm bảo rằng
        :c:member:`~PyTypeObject.tp_finalize` luôn được gọi.
     #. Nếu đối tượng được đánh dấu là finalized,
        :c:member:`~PyTypeObject.tp_clear` có thể được garbage collector gọi để xóa các tham chiếu mà đối tượng đang giữ. Hàm này *không* được gọi khi reference count của đối tượng đạt đến 0.
     #. :c:member:`~PyTypeObject.tp_dealloc` được gọi để hủy đối tượng. Để tránh trùng lặp mã, :c:member:`~PyTypeObject.tp_dealloc` thường gọi :c:member:`~PyTypeObject.tp_clear` để giải phóng các tham chiếu của đối tượng.
     #. Khi :c:member:`~PyTypeObject.tp_dealloc` hoàn tất việc hủy đối tượng, nó sẽ trực tiếp gọi :c:member:`~PyTypeObject.tp_free` (thường được đặt thành
        :c:func:`PyObject_Free` hoặc :c:func:`PyObject_GC_Del`, tùy theo kiểu) để giải phóng bộ nhớ.

   * Hàm :c:member:`~PyTypeObject.tp_finalize` được phép thêm một tham chiếu đến đối tượng nếu muốn. Nếu thực hiện, đối tượng sẽ được *hồi sinh*, ngăn việc hủy đang chờ xử lý. (Chỉ
     :c:member:`!tp_finalize` được phép hồi sinh một đối tượng;
     :c:member:`~PyTypeObject.tp_clear` và
     :c:member:`~PyTypeObject.tp_dealloc` không thể thực hiện việc này nếu không gọi vào
     :c:member:`!tp_finalize`.) Việc hồi sinh một đối tượng có thể khiến dấu *finalized* của đối tượng bị xóa hoặc không. Hiện tại, Python không xóa dấu *finalized* khỏi một đối tượng được hồi sinh nếu đối tượng đó hỗ trợ thu gom rác (tức là cờ :c:macro:`Py_TPFLAGS_HAVE_GC` được đặt), nhưng lại xóa dấu này nếu đối tượng không hỗ trợ thu gom rác; một hoặc cả hai hành vi này có thể thay đổi trong tương lai.
   * :c:member:`~PyTypeObject.tp_dealloc` có thể tùy chọn gọi
     :c:member:`~PyTypeObject.tp_finalize` thông qua
     :c:func:`PyObject_CallFinalizerFromDealloc` nếu muốn tái sử dụng mã đó để hỗ trợ việc hủy đối tượng. Cách này được khuyến nghị vì đảm bảo rằng :c:member:`!tp_finalize` luôn được gọi trước khi hủy. Xem tài liệu :c:member:`~PyTypeObject.tp_dealloc` để biết mã ví dụ.
   * Nếu đối tượng là thành viên của một :term:`cyclic isolate` và một trong hai điều kiện sau
     :c:member:`~PyTypeObject.tp_clear` không phá vỡ được chu kỳ tham chiếu hoặc isolated tuần hoàn không được phát hiện (có thể do :func:`gc.disable` đã được gọi hoặc cờ :c:macro:`Py_TPFLAGS_HAVE_GC` bị bỏ sót nhầm trong một trong các kiểu liên quan), các đối tượng sẽ vĩnh viễn không thể được thu gom (chúng bị "rò rỉ"). Xem :data:`gc.garbage`.

   Nếu đối tượng được đánh dấu là hỗ trợ thu gom rác (the
   Cờ :c:macro:`Py_TPFLAGS_HAVE_GC` được đặt trong
   :c:member:`~PyTypeObject.tp_flags`), các sự kiện sau cũng có thể xảy ra:

   * Bộ thu gom rác thỉnh thoảng gọi
     :c:member:`~PyTypeObject.tp_traverse` để xác định các :term:`cyclic isolates <cyclic isolate>`.
   * Khi bộ thu gom rác phát hiện một :term:`cyclic isolate`, nó hoàn tất một trong các đối tượng thuộc nhóm bằng cách đánh dấu đối tượng đó là *finalized* và gọi hàm :c:member:`~PyTypeObject.tp_finalize` của đối tượng đó, nếu có. Quá trình này lặp lại cho đến khi cyclic isolate không còn tồn tại hoặc tất cả đối tượng đã được hoàn tất.
   * :c:member:`~PyTypeObject.tp_finalize` được phép phục hồi đối tượng bằng cách thêm một tham chiếu từ bên ngoài :term:`cyclic isolate`. Tham chiếu mới khiến nhóm đối tượng không còn tạo thành một cyclic isolate (chu kỳ tham chiếu vẫn có thể tồn tại, nhưng nếu tồn tại thì các đối tượng không còn bị cô lập).
   * Khi bộ thu gom rác phát hiện một :term:`cyclic isolate` và tất cả đối tượng trong nhóm đã được đánh dấu là *finalized*, bộ thu gom rác xóa một hoặc nhiều đối tượng chưa được xóa trong nhóm (có thể đồng thời) bằng cách gọi
     :c:member:`~PyTypeObject.tp_clear` function.  Quá trình này lặp lại miễn là cyclic isolate vẫn còn tồn tại và chưa phải tất cả đối tượng đều được giải phóng.


Hủy Cyclic Isolate
------------------

Dưới đây là các giai đoạn tồn tại của một :term:`cyclic isolate` giả định, tiếp tục tồn tại sau khi từng đối tượng thành viên được finalize hoặc giải phóng.  Đây là memory leak nếu một cyclic isolate trải qua tất cả các giai đoạn này; nó sẽ biến mất ngay khi tất cả đối tượng được giải phóng, nếu không biến mất sớm hơn.  Một cyclic isolate có thể biến mất vì reference cycle bị phá vỡ hoặc vì các đối tượng không còn isolated do finalizer resurrection (xem
:c:member:`~PyTypeObject.tp_finalize`).

0. **Có thể truy cập** (chưa phải là cyclic isolate): Tất cả đối tượng đang ở trạng thái bình thường và có thể truy cập.  Một reference cycle có thể tồn tại, nhưng một tham chiếu bên ngoài khiến các đối tượng chưa bị cô lập.
#. **Không thể truy cập nhưng nhất quán:** Tham chiếu cuối cùng từ bên ngoài nhóm đối tượng theo chu kỳ đã bị xóa, khiến các đối tượng trở nên cô lập (do đó một cyclic isolate được tạo ra).  Chưa có đối tượng nào trong nhóm được finalize hoặc giải phóng.  Cyclic isolate vẫn ở giai đoạn này cho đến một lần chạy sau đó của garbage collector (không nhất thiết là lần chạy kế tiếp vì lần chạy kế tiếp có thể không quét mọi đối tượng).
#. **Một phần đã finalized và một phần chưa:** Các đối tượng trong một cyclic isolate được finalize lần lượt, nghĩa là sẽ có một khoảng thời gian cyclic isolate bao gồm cả các đối tượng đã finalized và chưa finalized. Thứ tự finalization không được quy định, vì vậy có thể trông như ngẫu nhiên.  Một đối tượng đã finalized phải hoạt động hợp lý khi các đối tượng chưa finalized tương tác với nó, và một đối tượng chưa finalized phải có khả năng chịu được việc finalize một tập hợp bất kỳ các đối tượng mà nó tham chiếu.
#. **Tất cả đã finalized:** Tất cả đối tượng trong một cyclic isolate đều được finalized trước khi bất kỳ đối tượng nào trong số đó được giải phóng.
#. **Kết hợp giữa đã finalize và đã clear:** Các đối tượng có thể được clear tuần tự hoặc đồng thời (nhưng vẫn giữ :term:`GIL`); dù theo cách nào, một số đối tượng sẽ hoàn tất trước các đối tượng khác. Một đối tượng đã finalize phải có khả năng chịu được việc một tập hợp con các đối tượng được tham chiếu bị clear. :pep:`442` gọi giai đoạn này là "cyclic trash".
#. **Bị rò rỉ:** Nếu một cyclic isolate vẫn tồn tại sau khi tất cả đối tượng trong nhóm đã được finalize và clear, thì các đối tượng đó sẽ vĩnh viễn không thể được thu hồi (xem :data:`gc.garbage`). Đây là một lỗi nếu một cyclic isolate đạt đến giai đoạn này---điều đó có nghĩa là các phương thức :c:member:`~PyTypeObject.tp_clear` của những đối tượng tham gia đã không phá vỡ vòng tham chiếu như yêu cầu.

Nếu :c:member:`~PyTypeObject.tp_clear` không tồn tại, Python sẽ không có cách nào để phá vỡ một vòng tham chiếu một cách an toàn. Việc chỉ hủy một đối tượng trong cyclic isolate sẽ tạo ra một con trỏ treo, gây ra hành vi không xác định khi một đối tượng tham chiếu đến đối tượng đã bị hủy cũng bị hủy. Bước clear biến việc hủy đối tượng thành một quy trình gồm hai giai đoạn: trước hết
:c:member:`~PyTypeObject.tp_clear` được gọi để hủy một phần các đối tượng, đủ để gỡ chúng khỏi nhau, sau đó
:c:member:`~PyTypeObject.tp_dealloc` được gọi để hoàn tất việc hủy.

Không giống clearing, finalization không phải là một giai đoạn của việc hủy. Một đối tượng đã finalize vẫn phải hoạt động đúng bằng cách tiếp tục thực hiện các contract thiết kế của nó. Finalizer của một đối tượng được phép thực thi mã Python tùy ý, thậm chí còn có thể ngăn việc hủy sắp xảy ra bằng cách thêm một tham chiếu. Finalizer chỉ liên quan đến việc hủy theo thứ tự gọi---nếu được chạy, nó sẽ chạy trước khi việc hủy bắt đầu bằng :c:member:`~PyTypeObject.tp_clear` (nếu được gọi) và kết thúc bằng :c:member:`~PyTypeObject.tp_dealloc`.

Bước finalization không cần thiết để thu hồi an toàn các đối tượng trong một cyclic isolate, nhưng việc có bước này giúp thiết kế các kiểu hoạt động hợp lý hơn khi các đối tượng được clear. Việc clear một đối tượng có thể nhất thiết khiến đối tượng đó ở trạng thái hỏng, đã bị hủy một phần---có thể không an toàn khi gọi bất kỳ phương thức nào của đối tượng đã clear hoặc truy cập bất kỳ thuộc tính nào của nó. Với finalization, chỉ các đối tượng đã finalize mới có khả năng tương tác với các đối tượng đã clear; các đối tượng chưa finalize được đảm bảo chỉ tương tác với các đối tượng chưa clear (nhưng có thể đã finalize).

Tóm tắt các tương tác có thể xảy ra:

* Một đối tượng chưa được hoàn tất có thể có tham chiếu đến hoặc được tham chiếu từ các đối tượng chưa được hoàn tất và đã được hoàn tất, nhưng không thể có tham chiếu đến hoặc được tham chiếu từ các đối tượng đã được xóa.
* Một đối tượng đã được hoàn tất có thể có tham chiếu đến hoặc được tham chiếu từ các đối tượng chưa được hoàn tất, đã được hoàn tất và đã được xóa.
* Một đối tượng đã được xóa có thể có tham chiếu đến hoặc được tham chiếu từ các đối tượng đã được hoàn tất và đã được xóa, nhưng không thể có tham chiếu đến hoặc được tham chiếu từ các đối tượng chưa được hoàn tất.

Nếu không có chu trình tham chiếu nào, một đối tượng có thể được hủy đơn giản ngay khi tham chiếu cuối cùng đến nó bị xóa; các bước hoàn tất và xóa là không cần thiết để thu hồi an toàn các đối tượng không còn được sử dụng. Tuy nhiên, việc tự động gọi
:c:member:`~PyTypeObject.tp_finalize` và :c:member:`~PyTypeObject.tp_clear` trước khi hủy vẫn có thể hữu ích, vì việc thiết kế kiểu sẽ đơn giản hơn khi mọi đối tượng luôn trải qua cùng một chuỗi sự kiện, bất kể chúng có tham gia vào một isolate chu kỳ hay không. Hiện tại, Python chỉ gọi
:c:member:`~PyTypeObject.tp_finalize` và :c:member:`~PyTypeObject.tp_clear` khi cần để hủy một isolate chu kỳ; điều này có thể thay đổi trong phiên bản tương lai.


Các hàm
-------

Để cấp phát và giải phóng bộ nhớ, hãy xem :ref:`allocating-objects`.


.. c:function:: void PyObject_CallFinalizer(PyObject *op)

   Hoàn tất việc xử lý đối tượng như được mô tả trong :c:member:`~PyTypeObject.tp_finalize`. Hãy gọi hàm này (hoặc :c:func:`PyObject_CallFinalizerFromDealloc`) thay vì gọi trực tiếp :c:member:`~PyTypeObject.tp_finalize`, vì hàm này có thể loại bỏ các lệnh gọi trùng lặp đến :c:member:`!tp_finalize`. Hiện tại, các lệnh gọi chỉ được loại bỏ trùng lặp nếu kiểu hỗ trợ tính năng thu gom rác (garbage collection) (tức là cờ :c:macro:`Py_TPFLAGS_HAVE_GC` được đặt); điều này có thể thay đổi trong tương lai.

   .. versionadded:: 3.4


.. c:function:: int PyObject_CallFinalizerFromDealloc(PyObject *op)

   Tương tự như :c:func:`PyObject_CallFinalizer` nhưng được dùng để gọi ở đầu trình hủy (destructor) của đối tượng (:c:member:`~PyTypeObject.tp_dealloc`). Không được có bất kỳ tham chiếu nào đến đối tượng. Nếu trình hoàn tất (finalizer) của đối tượng phục sinh đối tượng, hàm này trả về -1; không được thực hiện thêm bước hủy nào. Nếu không, hàm này trả về 0 và quá trình hủy có thể tiếp tục bình thường.

   .. versionadded:: 3.4

   .. seealso::

      :c:member:`~PyTypeObject.tp_dealloc` cho mã ví dụ.
