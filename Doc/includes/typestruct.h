typedef struct _typeobject {
    PyObject_VAR_HEAD
    const char *tp_name; /* Để in, theo định dạng "<module>.<name>" */
    Py_ssize_t tp_basicsize, tp_itemsize; /* Để cấp phát */

    /* Các phương thức triển khai thao tác chuẩn */

    destructor tp_dealloc;
    Py_ssize_t tp_vectorcall_offset;
    getattrfunc tp_getattr;
    setattrfunc tp_setattr;
    PyAsyncMethods *tp_as_async; /* trước đây có tên là tp_compare (Python 2)
                                    hoặc tp_reserved (Python 3) */
    reprfunc tp_repr;

    /* Bộ phương thức cho các lớp chuẩn */

    PyNumberMethods *tp_as_number;
    PySequenceMethods *tp_as_sequence;
    PyMappingMethods *tp_as_mapping;

    /* Thêm các thao tác chuẩn (đặt ở đây để tương thích nhị phân) */

    hashfunc tp_hash;
    ternaryfunc tp_call;
    reprfunc tp_str;
    getattrofunc tp_getattro;
    setattrofunc tp_setattro;

    /* Hàm truy cập đối tượng dưới dạng bộ đệm vào/ra */
    PyBufferProcs *tp_as_buffer;

    /* Cờ xác định sự hiện diện của tính năng tùy chọn/mở rộng */
    unsigned long tp_flags;

    const char *tp_doc; /* Chuỗi tài liệu */

    /* Được gán ý nghĩa trong bản phát hành 2.0 */
    /* gọi hàm cho mọi đối tượng có thể truy cập */
    traverseproc tp_traverse;

    /* xóa các tham chiếu tới đối tượng chứa bên trong */
    inquiry tp_clear;

    /* Được gán ý nghĩa trong bản phát hành 2.1 */
    /* so sánh phong phú */
    richcmpfunc tp_richcompare;

    /* bộ kích hoạt tham chiếu yếu */
    Py_ssize_t tp_weaklistoffset;

    /* Bộ lặp */
    getiterfunc tp_iter;
    iternextfunc tp_iternext;

    /* Nội dung về bộ mô tả thuộc tính và kế thừa lớp con */
    PyMethodDef *tp_methods;
    PyMemberDef *tp_members;
    PyGetSetDef *tp_getset;
    // Tham chiếu mạnh với kiểu heap, tham chiếu mượn với kiểu tĩnh
    PyTypeObject *tp_base;
    PyObject *tp_dict;
    descrgetfunc tp_descr_get;
    descrsetfunc tp_descr_set;
    Py_ssize_t tp_dictoffset;
    initproc tp_init;
    allocfunc tp_alloc;
    newfunc tp_new;
    freefunc tp_free; /* Thủ tục giải phóng bộ nhớ cấp thấp */
    inquiry tp_is_gc; /* Dành cho PyObject_IS_GC */
    PyObject *tp_bases;
    PyObject *tp_mro; /* thứ tự phân giải phương thức */
    PyObject *tp_cache; /* không còn được dùng */
    void *tp_subclasses;  /* với kiểu dựng sẵn tĩnh, đây là một chỉ mục */
    PyObject *tp_weaklist; /* không dùng cho kiểu dựng sẵn tĩnh */
    destructor tp_del;

    /* Thẻ phiên bản của bộ đệm thuộc tính kiểu. Được thêm ở phiên bản 2.6.
     * Nếu bằng không, bộ đệm không hợp lệ và phải được khởi tạo.
     */
    unsigned int tp_version_tag;

    destructor tp_finalize;
    vectorcallfunc tp_vectorcall;

    /* tập bit chỉ các trình theo dõi kiểu quan tâm đến kiểu này */
    unsigned char tp_watched;

    /* Số lượng giá trị tp_version_tag đã dùng.
     * Đặt thành _Py_ATTR_CACHE_UNUSED nếu bộ đệm thuộc tính bị
     * vô hiệu cho kiểu này (ví dụ do các mục MRO tùy chỉnh).
     * Nếu không, bị giới hạn bởi MAX_VERSIONS_PER_CLASS (định nghĩa ở nơi khác).
     */
    uint16_t tp_versions_used;
} PyTypeObject;
