Trong Git Bash:

```bash
uv venv
source .venv/Scripts/activate
uv pip install -r requirements.txt

uv pip install sphinx-lint

./make.bat html
```

Tuy nhiên `make.bat` là script Windows, Git Bash đôi khi chạy được nhưng không tiện. Cách ổn định nhất là gọi Sphinx trực tiếp:

```bash
uv run sphinx-build -b html . _build/html
```

Lần đầu cài dependency:

```bash
uv venv
uv pip install -r requirements.txt
```

Các lần sau, chỉ cần build lại:

```bash
uv run sphinx-build -b html . _build/html
```

Mở bản docs đã build:

```bash
start _build/html/index.html
```

---

Có. Sphinx có sẵn EPUB builder:

```bash
uv run sphinx-build -b epub . _build/epub
```

File EPUB sẽ nằm trong `_build/epub/`, tên do cấu hình trong `conf.py` quyết định (thường kiểu `GodotEngine.epub`).

Có thể preview/tự build khi sửa bằng:

```bash
uv run sphinx-autobuild -b epub . _build/epub
```

Nhưng EPUB không phù hợp để preview liên tục như HTML; nên dùng HTML để dịch và kiểm tra nhanh, rồi build EPUB khi hoàn thành một phần/chương lớn.

Lưu ý: Godot Docs có nhiều directive, tab code, video, ảnh, link nội bộ. Một số thành phần vốn dành cho web có thể bị Sphinx giản lược hoặc hiển thị không đẹp trong EPUB.


---
# Check

uv run sphinx-build -b dummy --keep-going . _build/check


---
host on R2
300baicodethieunhi.com/godot
300baicodethieunhi.com/react
300baicodethieunhi.com/python