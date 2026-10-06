# Ví dụ đơn giản trình bày cách dùng ID bền vững để pickle
# các đối tượng bên ngoài theo tham chiếu.

import pickle
import sqlite3
from collections import namedtuple

# Lớp đơn giản biểu diễn một bản ghi trong cơ sở dữ liệu.
MemoRecord = namedtuple("MemoRecord", "key, task")

class DBPickler(pickle.Pickler):

    def persistent_id(self, obj):
        # Thay vì pickle MemoRecord như một thể hiện lớp thông thường, ta xuất
        # một ID bền vững.
        if isinstance(obj, MemoRecord):
            # Ở đây, ID bền vững chỉ là một bộ chứa thẻ và khóa, tham chiếu tới
            # một bản ghi cụ thể trong cơ sở dữ liệu.
            return ("MemoRecord", obj.key)
        else:
            # Nếu obj không có ID bền vững, trả về None. Điều này nghĩa là obj
            # cần được pickle như thường lệ.
            return None


class DBUnpickler(pickle.Unpickler):

    def __init__(self, file, connection):
        super().__init__(file)
        self.connection = connection

    def persistent_load(self, pid):
        # Phương thức này được gọi khi gặp một ID bền vững.
        # Ở đây, pid là bộ được DBPickler trả về.
        cursor = self.connection.cursor()
        type_tag, key_id = pid
        if type_tag == "MemoRecord":
            # Lấy bản ghi được tham chiếu từ cơ sở dữ liệu rồi trả về.
            cursor.execute("SELECT * FROM memos WHERE key=?", (str(key_id),))
            key, task = cursor.fetchone()
            return MemoRecord(key, task)
        else:
            # Luôn phát sinh lỗi nếu không thể trả về đúng đối tượng.
            # Nếu không, unpickler sẽ cho rằng None là đối tượng được ID bền
            # vững tham chiếu đến.
            raise pickle.UnpicklingError("unsupported persistent object")


def main():
    import io
    import pprint

    # Khởi tạo và điền dữ liệu cho cơ sở dữ liệu.
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE memos(key INTEGER PRIMARY KEY, task TEXT)")
    tasks = (
        'give food to fish',
        'prepare group meeting',
        'fight with a zebra',
        )
    for task in tasks:
        cursor.execute("INSERT INTO memos VALUES(NULL, ?)", (task,))

    # Lấy các bản ghi sẽ được pickle.
    cursor.execute("SELECT * FROM memos")
    memos = [MemoRecord(key, task) for key, task in cursor]
    # Lưu các bản ghi bằng DBPickler tùy chỉnh.
    file = io.BytesIO()
    DBPickler(file).dump(memos)

    print("Pickled records:")
    pprint.pprint(memos)

    # Cập nhật một bản ghi để minh họa thêm.
    cursor.execute("UPDATE memos SET task='learn italian' WHERE key=1")

    # Tải các bản ghi từ luồng dữ liệu pickle.
    file.seek(0)
    memos = DBUnpickler(file, conn).load()

    print("Unpickled records:")
    pprint.pprint(memos)


if __name__ == '__main__':
    main()
