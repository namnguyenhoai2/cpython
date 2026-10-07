Đang chờ xóa trong Python 3.17
------------------------------

* :mod:`collections.abc`:

  - :class:`collections.abc.ByteString` dự kiến sẽ bị xóa trong Python 3.17.

    Sử dụng ``isinstance(obj, collections.abc.Buffer)`` để kiểm tra trong runtime xem ``obj`` có triển khai :ref:`giao thức bộ đệm <bufferobjects>` hay không. Khi sử dụng trong chú thích kiểu, hãy dùng :class:`~collections.abc.Buffer` hoặc một union chỉ rõ các kiểu mà mã của bạn hỗ trợ (ví dụ: ``bytes | bytearray | memoryview``).

    :class:`!ByteString` ban đầu được dự định là một lớp trừu tượng, đóng vai trò là siêu kiểu của cả :class:`bytes` và :class:`bytearray`. Tuy nhiên, vì ABC này chưa bao giờ có phương thức nào, việc biết một đối tượng là một thể hiện của :class:`!ByteString` thực tế không cho bạn biết điều gì hữu ích về đối tượng đó. Các kiểu bộ đệm phổ biến khác như :class:`memoryview` cũng chưa bao giờ được hiểu là kiểu con của :class:`!ByteString` (dù trong runtime hay bởi các trình kiểm tra kiểu tĩnh).

    Xem :pep:`PEP 688 <688#current-options>` để biết thêm chi tiết. (Do Shantanu Jain đóng góp trong :gh:`91896`.)


* :mod:`typing`:

  - Trước Python 3.14, các union kiểu cũ được triển khai bằng lớp private ``typing._UnionGenericAlias``. Lớp này không còn cần thiết cho việc triển khai, nhưng vẫn được giữ lại để tương thích ngược và dự kiến sẽ bị xóa trong Python 3.17. Người dùng nên sử dụng các trình trợ giúp introspection đã được ghi lại như :func:`typing.get_origin` và :func:`typing.get_args` thay vì dựa vào các chi tiết triển khai private.
  - :class:`typing.ByteString`, đã không được dùng nữa kể từ Python 3.9, dự kiến sẽ bị xóa trong Python 3.17.

    Sử dụng ``isinstance(obj, collections.abc.Buffer)`` để kiểm tra trong runtime xem ``obj`` có triển khai :ref:`giao thức bộ đệm <bufferobjects>` hay không. Khi sử dụng trong chú thích kiểu, hãy dùng :class:`~collections.abc.Buffer` hoặc một union chỉ rõ các kiểu mà mã của bạn hỗ trợ (ví dụ: ``bytes | bytearray | memoryview``).

    :class:`!ByteString` ban đầu được dự định là một lớp trừu tượng, đóng vai trò là siêu kiểu của cả :class:`bytes` và :class:`bytearray`. Tuy nhiên, vì ABC này chưa bao giờ có phương thức nào, việc biết một đối tượng là một thể hiện của :class:`!ByteString` thực tế không cho bạn biết điều gì hữu ích về đối tượng đó. Các kiểu bộ đệm phổ biến khác như :class:`memoryview` cũng chưa bao giờ được hiểu là kiểu con của :class:`!ByteString` (dù trong runtime hay bởi các trình kiểm tra kiểu tĩnh).

    Xem :pep:`PEP 688 <688#current-options>` để biết thêm chi tiết. (Do Shantanu Jain đóng góp trong :gh:`91896`.)
