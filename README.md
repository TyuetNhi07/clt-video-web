# Mô phỏng Định lí Giới hạn Trung tâm (CLT)

Web responsive viết bằng FastAPI, phát video MP4 mô phỏng CLT, triển khai trên Render.

## Chạy cục bộ

```bash
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# macOS/Linux:         source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

Mở http://127.0.0.1:8000 (trang chính), /health (kiểm tra nhanh), /docs (tài liệu API).

## Sinh lại video (tùy chọn)

Cần `numpy`, `matplotlib` và `ffmpeg`:

```bash
pip install numpy matplotlib
python make_video.py
```

## Đưa lên GitHub

```bash
git init
git add .
git commit -m "Create responsive CLT video web"
git branch -M main
git remote add origin https://github.com/USERNAME/clt-video-web.git
git push -u origin main
```

## Triển khai trên Render

New > Web Service > chọn repo `clt-video-web`, branch `main`, runtime Python.

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Hoặc dùng Blueprint: Render đọc sẵn `render.yaml` ở thư mục gốc.
