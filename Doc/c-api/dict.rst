.. highlight:: c

.. _dictobjects:

Đối tượng từ điển
-----------------

.. index:: pair: object; dictionary


.. c:type:: PyDictObject

   Kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng từ điển Python.


.. c:var:: PyTypeObject PyDict_Type

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu từ điển Python. Đây là cùng một đối tượng với :class:`dict` trong tầng Python.


.. c:function:: int PyDict_Check(PyObject *p)

   Trả về true nếu *p* là một đối tượng dict hoặc là một instance của kiểu con của kiểu dict. Hàm này luôn thực thi thành công.


.. c:function:: int PyDict_CheckExact(PyObject *p)

   Trả về true nếu *p* là một đối tượng dict nhưng không phải là một instance của kiểu con của kiểu dict. Hàm này luôn thực thi thành công.


.. c:function:: PyObject* PyDict_New()

   Trả về một từ điển mới, rỗng hoặc ``NULL`` nếu xảy ra lỗi.


.. c:function:: PyObject* PyDictProxy_New(PyObject *mapping)

   Trả về một đối tượng :class:`types.MappingProxyType` cho một mapping áp dụng hành vi chỉ đọc. Đối tượng này thường được dùng để tạo một view nhằm ngăn việc sửa đổi từ điển đối với các kiểu lớp không động.


.. c:var:: PyTypeObject PyDictProxy_Type

   Kiểu đối tượng dành cho các đối tượng mapping proxy được tạo bởi
   :c:func:`PyDictProxy_New` và cho thuộc tính ``__dict__`` chỉ đọc của nhiều kiểu dựng sẵn. Một thực thể :c:type:`PyDictProxy_Type` cung cấp một chế độ xem động, chỉ đọc của một dictionary nền: các thay đổi đối với dictionary nền được phản ánh trong proxy, nhưng bản thân proxy không hỗ trợ các thao tác biến đổi. Điều này tương ứng với
   :class:`types.MappingProxyType` trong Python.


.. c:function:: void PyDict_Clear(PyObject *p)

   Xóa tất cả các cặp khóa-giá trị khỏi một dictionary hiện có.


.. c:function:: int PyDict_Contains(PyObject *p, PyObject *key)

   Xác định xem dictionary *p* có chứa *key* hay không. Nếu một mục trong *p* khớp với *key*, trả về ``1``, nếu không thì trả về ``0``. Khi có lỗi, trả về ``-1``. Tương đương với biểu thức Python ``key in p``.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.


.. c:function:: int PyDict_ContainsString(PyObject *p, const char *key)

   Điều này giống với :c:func:`PyDict_Contains`, nhưng *key* được chỉ định dưới dạng
   :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một
   :c:expr:`PyObject*`.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyDict_Copy(PyObject *p)

   Trả về một dictionary mới chứa các cặp khóa-giá trị giống với *p*.


.. c:function:: int PyDict_SetItem(PyObject *p, PyObject *key, PyObject *val)

   Chèn *val* vào dictionary *p* với khóa là *key*.  *key* phải là
   :term:`hashable`; nếu không, :exc:`TypeError` sẽ được phát sinh. Trả về ``0`` khi thành công hoặc ``-1`` khi thất bại. Hàm này *không* ":term:`steal`" một tham chiếu đến *val*.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.


.. c:function:: int PyDict_SetItemString(PyObject *p, const char *key, PyObject *val)

   Tương tự như :c:func:`PyDict_SetItem`, nhưng *key* được chỉ định dưới dạng :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một :c:expr:`PyObject*`.


.. c:function:: int PyDict_DelItem(PyObject *p, PyObject *key)

   Xóa mục trong dictionary *p* có khóa *key*. *key* phải là :term:`hashable`; nếu không, :exc:`TypeError` sẽ được phát sinh. Nếu *key* không có trong dictionary, :exc:`KeyError` sẽ được phát sinh. Trả về ``0`` khi thành công hoặc ``-1`` khi thất bại.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.


.. c:function:: int PyDict_DelItemString(PyObject *p, const char *key)

   Điều này giống với :c:func:`PyDict_DelItem`, nhưng *key* được chỉ định dưới dạng một :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một :c:expr:`PyObject*`.


.. c:function:: int PyDict_GetItemRef(PyObject *p, PyObject *key, PyObject **result)

   Trả về một :term:`strong reference` mới trỏ đến đối tượng trong dictionary *p* có khóa *key*:

   * Nếu khóa tồn tại, đặt *\*result* thành một :term:`strong reference` mới trỏ đến giá trị và trả về ``1``.
   * Nếu thiếu khóa, đặt *\*result* thành ``NULL`` và trả về ``0``.
   * Khi xảy ra lỗi, phát sinh một ngoại lệ, đặt *\*result* thành ``NULL`` và trả về ``-1``.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.

   .. versionadded:: 3.13

   Xem thêm hàm :c:func:`PyObject_GetItem`.


.. c:function:: PyObject* PyDict_GetItem(PyObject *p, PyObject *key)

   Trả về một :term:`borrowed reference` đến đối tượng trong từ điển *p* có khóa *key*. Trả về ``NULL`` nếu thiếu khóa *key* *without* đặt một ngoại lệ.

   .. note::

      Các ngoại lệ xảy ra khi lệnh này gọi :meth:`~object.__hash__` và
      các phương thức :meth:`~object.__eq__` bị bỏ qua một cách im lặng. Ưu tiên sử dụng hàm :c:func:`PyDict_GetItemWithError`.

   .. note::

      Trong :term:`free-threaded build`, giá trị được trả về
      :term:`borrowed reference` có thể trở nên không hợp lệ nếu một thread khác đồng thời sửa đổi từ điển. Ưu tiên :c:func:`PyDict_GetItemRef`, hàm này trả về một :term:`strong reference`.

   .. versionchanged:: 3.10
      Việc gọi API này mà không có :term:`attached thread state` trước đây đã được cho phép vì lý do lịch sử. Hiện nay việc đó không còn được phép.


.. c:function:: PyObject* PyDict_GetItemWithError(PyObject *p, PyObject *key)

   Biến thể của :c:func:`PyDict_GetItem` không bỏ qua các exception. Trả về ``NULL`` **with** một exception set nếu xảy ra exception. Trả về ``NULL`` **without** một exception set nếu không tìm thấy key.

   .. note::

      Trong :term:`free-threaded build`, giá trị được trả về
      :term:`borrowed reference` có thể trở nên không hợp lệ nếu một thread khác đồng thời sửa đổi từ điển. Ưu tiên :c:func:`PyDict_GetItemRef`, hàm này trả về một :term:`strong reference`.


.. c:function:: PyObject* PyDict_GetItemString(PyObject *p, const char *key)

   Điều này giống :c:func:`PyDict_GetItem`, nhưng *key* được chỉ định là một
   :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một
   :c:expr:`PyObject*`.

   .. note::

      Các ngoại lệ xảy ra khi lệnh này gọi :meth:`~object.__hash__` và
      :meth:`~object.__eq__` các phương thức hoặc trong khi tạo đối tượng :class:`str` tạm thời sẽ bị bỏ qua mà không báo lỗi. Nên sử dụng hàm :c:func:`PyDict_GetItemWithError` với chính bạn
      :c:func:`PyUnicode_FromString` *key* thay vào đó.

   .. note::

      Trong :term:`free-threaded build`, giá trị được trả về
      :term:`borrowed reference` có thể trở nên không hợp lệ nếu một thread khác đồng thời sửa đổi dictionary. Ưu tiên :c:func:`PyDict_GetItemStringRef`, hàm này trả về một :term:`strong reference`.


.. c:function:: int PyDict_GetItemStringRef(PyObject *p, const char *key, PyObject **result)

   Tương tự như :c:func:`PyDict_GetItemRef`, nhưng *key* được chỉ định là một
   :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một
   :c:expr:`PyObject*`.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyDict_SetDefault(PyObject *p, PyObject *key, PyObject *defaultobj)

   Đây cũng chính là :meth:`dict.setdefault` ở cấp Python. Nếu được cung cấp, hàm này trả về giá trị tương ứng với *key* từ dictionary *p*. Nếu key không có trong dict, key đó được chèn với giá trị *defaultobj* và *defaultobj* được trả về. Hàm này chỉ đánh giá hàm băm của *key* một lần, thay vì đánh giá riêng cho thao tác tra cứu và thao tác chèn.

   .. versionadded:: 3.4

   .. note::

      Trong :term:`free-threaded build`, giá trị được trả về
      :term:`borrowed reference` có thể trở nên không hợp lệ nếu một thread khác đồng thời sửa đổi dictionary. Nên dùng :c:func:`PyDict_SetDefaultRef`, hàm này trả về một :term:`strong reference`.



.. c:function:: int PyDict_SetDefaultRef(PyObject *p, PyObject *key, PyObject *default_value, PyObject **result)

   Chèn *default_value* vào dictionary *p* với khóa là *key* nếu khóa này chưa tồn tại trong dictionary. Nếu *result* không phải là ``NULL``, thì *\*result* được gán một :term:`strong reference` tới *default_value* nếu khóa chưa tồn tại, hoặc tới giá trị hiện có nếu *key* đã tồn tại trong dictionary. Trả về ``1`` nếu khóa đã tồn tại và *default_value* chưa được chèn, hoặc ``0`` nếu khóa chưa tồn tại và *default_value* đã được chèn. Khi thất bại, trả về ``-1``, thiết lập một exception và đặt ``*result`` thành ``NULL``.

   Để rõ ràng: nếu bạn có một strong reference tới *default_value* trước khi gọi hàm này, thì sau khi hàm trả về, bạn giữ một strong reference tới cả *default_value* và *\*result* (nếu nó không phải là ``NULL``). Các tham chiếu này có thể trỏ tới cùng một đối tượng; trong trường hợp đó, bạn giữ hai tham chiếu riêng biệt tới đối tượng đó.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.

   .. versionadded:: 3.13


.. c:function:: int PyDict_Pop(PyObject *p, PyObject *key, PyObject **result)

   Xóa *key* khỏi dictionary *p* và tùy chọn trả về giá trị đã xóa. Không raise :exc:`KeyError` nếu không tìm thấy khóa.

   - Nếu khóa tồn tại, đặt *\*result* thành một tham chiếu mới tới giá trị đã xóa nếu *result* không phải là ``NULL``, rồi trả về ``1``.
   - Nếu không tìm thấy khóa, đặt *\*result* thành ``NULL`` nếu *result* không phải là ``NULL``, rồi trả về ``0``.
   - Khi xảy ra lỗi, hãy phát sinh một exception và trả về ``-1``.

   Tương tự :meth:`dict.pop`, nhưng không có giá trị mặc định và không phát sinh :exc:`KeyError` nếu thiếu khóa.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.

   .. versionadded:: 3.13


.. c:function:: int PyDict_PopString(PyObject *p, const char *key, PyObject **result)

   Tương tự :c:func:`PyDict_Pop`, nhưng *key* được chỉ định là một
   :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một
   :c:expr:`PyObject*`.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyDict_Items(PyObject *p)

   Trả về một :c:type:`PyListObject` chứa tất cả các mục từ dictionary.


.. c:function:: PyObject* PyDict_Keys(PyObject *p)

   Trả về một :c:type:`PyListObject` chứa tất cả các khóa từ dictionary.


.. c:function:: PyObject* PyDict_Values(PyObject *p)

   Trả về một :c:type:`PyListObject` chứa tất cả các giá trị từ từ điển *p*.


.. c:function:: Py_ssize_t PyDict_Size(PyObject *p)

   .. index:: pair: built-in function; len

   Trả về số lượng phần tử trong từ điển. Điều này tương đương với ``len(p)`` trên một từ điển.


.. c:function:: Py_ssize_t PyDict_GET_SIZE(PyObject *p)

   Tương tự như :c:func:`PyDict_Size`, nhưng không kiểm tra lỗi.


.. c:function:: int PyDict_Next(PyObject *p, Py_ssize_t *ppos, PyObject **pkey, PyObject **pvalue)

   Lặp qua tất cả các cặp khóa-giá trị trong từ điển *p*.
   :c:type:`Py_ssize_t` được *ppos* tham chiếu đến phải được khởi tạo thành ``0`` trước lần gọi đầu tiên đến hàm này để bắt đầu quá trình lặp; hàm trả về true cho mỗi cặp trong từ điển và false sau khi tất cả các cặp đã được báo cáo. Các tham số *pkey* và *pvalue* phải trỏ đến các biến :c:expr:`PyObject*` sẽ lần lượt được điền bằng từng khóa và giá trị, hoặc có thể là ``NULL``. Mọi tham chiếu được trả về thông qua chúng đều là tham chiếu mượn. Không được thay đổi *ppos* trong quá trình lặp. Giá trị của nó biểu thị các offset trong cấu trúc từ điển nội bộ; vì cấu trúc này thưa nên các offset không liên tiếp.

   Ví dụ::

      PyObject *key, *value;
      Py_ssize_t pos = 0;

      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          /* do something interesting with the values... */
          ...
      }

   Không được thay đổi từ điển *p* trong quá trình lặp. Bạn có thể an toàn sửa đổi các giá trị của khóa khi lặp qua từ điển, nhưng chỉ khi tập hợp các khóa không thay đổi. Ví dụ::

      PyObject *key, *value;
      Py_ssize_t pos = 0;

      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          long i = PyLong_AsLong(value);
          if (i == -1 && PyErr_Occurred()) {
              return -1;
          }
          PyObject *o = PyLong_FromLong(i + 1);
          if (o == NULL)
              return -1;
          if (PyDict_SetItem(self->dict, key, o) < 0) {
              Py_DECREF(o);
              return -1;
          }
          Py_DECREF(o);
      }

   Hàm này không an toàn với thread trong bản build :term:`free-threaded <free threading>` nếu không có cơ chế đồng bộ hóa bên ngoài. Bạn có thể sử dụng
   :c:macro:`Py_BEGIN_CRITICAL_SECTION` để khóa dictionary trong khi lặp qua nó::

      Py_BEGIN_CRITICAL_SECTION(self->dict);
      while (PyDict_Next(self->dict, &pos, &key, &value)) {
          ...
      }
      Py_END_CRITICAL_SECTION();

   .. note::

      Trong bản build free-threaded, có thể sử dụng hàm này an toàn bên trong critical section. Tuy nhiên, các tham chiếu được trả về cho *pkey* và *pvalue* là :term:`borrowed <borrowed reference>` và chỉ hợp lệ khi critical section đang được giữ. Nếu cần sử dụng các đối tượng này bên ngoài critical section hoặc khi critical section có thể bị tạm dừng, hãy tạo một
      :term:`strong reference <strong reference>` (ví dụ: bằng cách sử dụng
      :c:func:`Py_NewRef`).

.. c:function:: int PyDict_Merge(PyObject *a, PyObject *b, int override)

   Lặp qua đối tượng mapping *b* và thêm các cặp khóa-giá trị vào dictionary *a*. *b* có thể là một dictionary hoặc bất kỳ đối tượng nào hỗ trợ :c:func:`PyMapping_Keys` và :c:func:`PyObject_GetItem`. Nếu *override* là true, các cặp hiện có trong *a* sẽ được thay thế nếu tìm thấy khóa tương ứng trong *b*; nếu không, các cặp chỉ được thêm vào khi không có khóa tương ứng trong *a*. Trả về ``0`` nếu thành công hoặc ``-1`` nếu một exception được phát sinh.

   .. note::

      Trong :term:`free-threaded build`, khi *b* là một
      :class:`dict` (với iterator tiêu chuẩn), cả *a* và *b* đều bị khóa trong suốt thời gian thực hiện thao tác. Khi *b* là một mapping không phải dict, chỉ *a* bị khóa; *b* có thể bị một thread khác sửa đổi đồng thời.


.. c:function:: int PyDict_Update(PyObject *a, PyObject *b)

   Điều này tương tự ``PyDict_Merge(a, b, 1)`` trong C và gần giống ``a.update(b)`` trong Python, ngoại trừ việc :c:func:`PyDict_Update` không chuyển sang lặp qua một chuỗi các cặp khóa-giá trị nếu đối số thứ hai không có thuộc tính "keys". Trả về ``0`` khi thành công hoặc ``-1`` nếu một ngoại lệ được phát sinh.

   .. note::

      Trong :term:`free-threaded build`, khi *b* là một
      :class:`dict` (với iterator tiêu chuẩn), cả *a* và *b* đều bị khóa trong suốt thời gian thực hiện thao tác. Khi *b* là một mapping không phải dict, chỉ *a* bị khóa; *b* có thể bị một thread khác sửa đổi đồng thời.


.. c:function:: int PyDict_MergeFromSeq2(PyObject *a, PyObject *seq2, int override)

   Cập nhật hoặc hợp nhất vào dictionary *a* từ các cặp khóa-giá trị trong *seq2*. *seq2* phải là một đối tượng iterable tạo ra các đối tượng iterable có độ dài 2, được xem là các cặp khóa-giá trị. Khi có khóa trùng lặp, khóa xuất hiện sau cùng sẽ được ưu tiên nếu *override* là true; nếu không, khóa xuất hiện đầu tiên sẽ được ưu tiên. Trả về ``0`` khi thành công hoặc ``-1`` nếu một ngoại lệ được phát sinh. Tương đương với Python (ngoại trừ giá trị trả về)::

      def PyDict_MergeFromSeq2(a, seq2, override):
          for key, value in seq2:
              if override or key not in a:
                  a[key] = value

   .. note::

      Trong bản build :term:`free-threaded <free threading>`, chỉ *a* được khóa. Việc lặp qua *seq2* không được đồng bộ hóa; *seq2* có thể bị một thread khác sửa đổi đồng thời.


.. c:function:: int PyDict_AddWatcher(PyDict_WatchCallback callback)

   Đăng ký *callback* làm dictionary watcher. Trả về một id dạng số nguyên không âm, id này phải được truyền vào các lần gọi sau của :c:func:`PyDict_Watch`. Trong trường hợp xảy ra lỗi (ví dụ: không còn watcher ID khả dụng), trả về ``-1`` và thiết lập một ngoại lệ.

   .. note::

      Hàm này không được đồng bộ hóa nội bộ. Trong
      bản dựng :term:`free-threaded <free threading>`, bên gọi nên đảm bảo không có lệnh gọi đồng thời nào đến :c:func:`PyDict_AddWatcher` hoặc
      :c:func:`PyDict_ClearWatcher` đang được thực hiện.

   .. versionadded:: 3.12

.. c:function:: int PyDict_ClearWatcher(int watcher_id)

   Xóa watcher được xác định bởi *watcher_id* đã được trả về trước đó từ
   :c:func:`PyDict_AddWatcher`. Trả về ``0`` khi thành công, ``-1`` khi có lỗi (ví dụ: nếu *watcher_id* đã cho không được đăng ký.)

   .. note::

      Hàm này không được đồng bộ hóa nội bộ. Trong
      bản dựng :term:`free-threaded <free threading>`, bên gọi nên đảm bảo không có lệnh gọi đồng thời nào đến :c:func:`PyDict_AddWatcher` hoặc
      :c:func:`PyDict_ClearWatcher` đang được thực hiện.

   .. versionadded:: 3.12

.. c:function:: int PyDict_Watch(int watcher_id, PyObject *dict)

   Đánh dấu dictionary *dict* là được theo dõi. Callback được cấp *watcher_id* bởi
   :c:func:`PyDict_AddWatcher` sẽ được gọi khi *dict* bị sửa đổi hoặc giải phóng. Trả về ``0`` khi thành công hoặc ``-1`` khi có lỗi.

   .. versionadded:: 3.12

.. c:function:: int PyDict_Unwatch(int watcher_id, PyObject *dict)

   Đánh dấu dictionary *dict* không còn được theo dõi. Callback được cấp *watcher_id* bởi :c:func:`PyDict_AddWatcher` sẽ không còn được gọi khi *dict* bị sửa đổi hoặc giải phóng. Dictionary trước đó phải được watcher này theo dõi. Trả về ``0`` khi thành công hoặc ``-1`` khi có lỗi.

   .. versionadded:: 3.12

.. c:type:: PyDict_WatchEvent

   Liệt kê các sự kiện có thể xảy ra của watcher dictionary: ``PyDict_EVENT_ADDED``, ``PyDict_EVENT_MODIFIED``, ``PyDict_EVENT_DELETED``, ``PyDict_EVENT_CLONED``, ``PyDict_EVENT_CLEARED`` hoặc ``PyDict_EVENT_DEALLOCATED``.

   .. versionadded:: 3.12

.. c:type:: int (*PyDict_WatchCallback)(PyDict_WatchEvent event, PyObject *dict, PyObject *key, PyObject *new_value)

   Kiểu của hàm callback theo dõi dict.

   Nếu *event* là ``PyDict_EVENT_CLEARED`` hoặc ``PyDict_EVENT_DEALLOCATED``, cả *key* và *new_value* sẽ là ``NULL``. Nếu *event* là ``PyDict_EVENT_ADDED`` hoặc ``PyDict_EVENT_MODIFIED``, *new_value* sẽ là giá trị mới của *key*. Nếu *event* là ``PyDict_EVENT_DELETED``, *key* đang bị xóa khỏi dictionary và *new_value* sẽ là ``NULL``.

   ``PyDict_EVENT_CLONED`` xảy ra khi *dict* trước đó đang rỗng và một dict khác được hợp nhất vào đó. Để duy trì hiệu quả của thao tác này, các sự kiện ``PyDict_EVENT_ADDED`` theo từng khóa sẽ không được phát ra trong trường hợp này; thay vào đó, một ``PyDict_EVENT_CLONED`` duy nhất sẽ được phát ra và *key* sẽ là dictionary nguồn.

   Callback có thể kiểm tra nhưng không được sửa đổi *dict*; việc này có thể gây ra những tác động không thể dự đoán, bao gồm đệ quy vô hạn. Không được kích hoạt việc thực thi mã Python trong callback, vì điều đó có thể sửa đổi dict như một tác dụng phụ.

   Nếu *event* là ``PyDict_EVENT_DEALLOCATED``, việc tạo một tham chiếu mới trong callback đến dict sắp bị hủy sẽ làm nó sống lại và ngăn không cho nó được giải phóng tại thời điểm này. Khi đối tượng được khôi phục này bị hủy sau đó, mọi callback của watcher đang hoạt động tại thời điểm đó sẽ được gọi lại.

   Callback được thực thi trước khi thay đổi được thông báo đối với *dict* diễn ra, vì vậy có thể kiểm tra trạng thái trước đó của *dict*.

   Nếu callback đặt một exception, nó phải trả về ``-1``; exception này sẽ được in dưới dạng unraisable exception bằng :c:func:`PyErr_WriteUnraisable`. Nếu không, nó nên trả về ``0``.

   Có thể đã có một exception đang chờ được đặt khi callback bắt đầu. Trong trường hợp này, callback nên trả về ``0`` và vẫn giữ nguyên exception đó. Điều này có nghĩa là callback không được gọi bất kỳ API nào khác có thể đặt exception, trừ khi trước tiên nó lưu và xóa trạng thái exception, rồi khôi phục trạng thái đó trước khi trả về.

   .. versionadded:: 3.12


Đối tượng view từ điển
^^^^^^^^^^^^^^^^^^^^^^

.. c:function:: int PyDictViewSet_Check(PyObject *op)

   Trả về true nếu *op* là một view của một set bên trong dict. Hiện tại, điều này tương đương với :c:expr:`PyDictKeys_Check(op) || PyDictItems_Check(op)`. Hàm này luôn thành công.


.. c:var:: PyTypeObject PyDictKeys_Type

   Đối tượng kiểu cho một view của các khóa dictionary. Trong Python, đây là kiểu của đối tượng được :meth:`dict.keys` trả về.


.. c:function:: int PyDictKeys_Check(PyObject *op)

   Trả về true nếu *op* là một thể hiện của view các khóa dictionary. Hàm này luôn thành công.


.. c:var:: PyTypeObject PyDictValues_Type

   Đối tượng kiểu cho một view của các giá trị dictionary. Trong Python, đây là kiểu của đối tượng được :meth:`dict.values` trả về.


.. c:function:: int PyDictValues_Check(PyObject *op)

   Trả về true nếu *op* là một thể hiện của view các giá trị dictionary. Hàm này luôn thành công.


.. c:var:: PyTypeObject PyDictItems_Type

   Đối tượng kiểu cho một view của các mục dictionary. Trong Python, đây là kiểu của đối tượng được :meth:`dict.items` trả về.


.. c:function:: int PyDictItems_Check(PyObject *op)

   Trả về true nếu *op* là một thể hiện của view các mục dictionary. Hàm này luôn thành công.


Dictionary có thứ tự
^^^^^^^^^^^^^^^^^^^^

C API của Python cung cấp giao diện cho :class:`collections.OrderedDict` từ C. Kể từ Python 3.7, dictionary được sắp xếp theo thứ tự mặc định, vì vậy thường không cần nhiều đến các hàm này; hãy ưu tiên ``PyDict*`` khi có thể.


.. c:var:: PyTypeObject PyODict_Type

   Đối tượng kiểu dành cho dictionary có thứ tự. Đây là cùng một đối tượng với
   :class:`collections.OrderedDict` ở lớp Python.


.. c:function:: int PyODict_Check(PyObject *od)

   Trả về true nếu *od* là một đối tượng dictionary có thứ tự hoặc là một thực thể của kiểu con của kiểu :class:`~collections.OrderedDict`. Hàm này luôn thực hiện thành công.


.. c:function:: int PyODict_CheckExact(PyObject *od)

   Trả về true nếu *od* là một đối tượng dictionary có thứ tự, nhưng không phải là một thực thể của kiểu con của kiểu :class:`~collections.OrderedDict`. Hàm này luôn thực hiện thành công.


.. c:var:: PyTypeObject PyODictKeys_Type

   Tương tự như :c:type:`PyDictKeys_Type` đối với dictionary có thứ tự.


.. c:var:: PyTypeObject PyODictValues_Type

   Tương tự như :c:type:`PyDictValues_Type` đối với dictionary có thứ tự.


.. c:var:: PyTypeObject PyODictItems_Type

   Tương tự như :c:type:`PyDictItems_Type` đối với các từ điển có thứ tự.


.. c:function:: PyObject *PyODict_New(void)

   Trả về một từ điển có thứ tự mới, rỗng hoặc ``NULL`` nếu không thành công.

   Tương tự như :c:func:`PyDict_New`.


.. c:function:: int PyODict_SetItem(PyObject *od, PyObject *key, PyObject *value)

   Chèn *value* vào từ điển có thứ tự *od* với khóa là *key*. Trả về ``0`` nếu thành công hoặc ``-1`` cùng với một ngoại lệ được thiết lập nếu không thành công.

   Tương tự như :c:func:`PyDict_SetItem`.


.. c:function:: int PyODict_DelItem(PyObject *od, PyObject *key)

   Xóa mục nhập trong từ điển có thứ tự *od* có khóa *key*. Trả về ``0`` nếu thành công hoặc ``-1`` cùng với một ngoại lệ được thiết lập nếu không thành công.

   Tương tự như :c:func:`PyDict_DelItem`.


Đây là các bí danh :term:`soft deprecated` cho các API ``PyDict``:


.. list-table::
   :widths: auto
   :header-rows: 1

   * * ``PyODict``
     * ``PyDict``
   * * .. c:macro:: PyODict_GetItem(od, key)
     * :c:func:`PyDict_GetItem`
   * * .. c:macro:: PyODict_GetItemWithError(od, key)
     * :c:func:`PyDict_GetItemWithError`
   * * .. c:macro:: PyODict_GetItemString(od, key)
     * :c:func:`PyDict_GetItemString`
   * * .. c:macro:: PyODict_Contains(od, key)
     * :c:func:`PyDict_Contains`
   * * .. c:macro:: PyODict_Size(od)
     * :c:func:`PyDict_Size`
   * * .. c:macro:: PyODict_SIZE(od)
     * :c:func:`PyDict_GET_SIZE`
