"""Sinh video mô phỏng Định lí Giới hạn Trung tâm (CLT).

Chạy:  python make_video.py
Kết quả: static/video/clt_simulation.mp4  (H.264, yuv420p, không âm thanh)

Cần: numpy, matplotlib và ffmpeg. Không cần để triển khai web; chỉ chạy một lần
rồi commit tệp MP4.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation

OUT = Path(__file__).resolve().parent / "static" / "video" / "clt_simulation.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(2026)
N_VALUES = [1, 2, 5, 10, 30, 100]   # kích thước mẫu n
REPS = 20000                        # số lần lặp lấy mẫu
FRAMES_PER_N = 30                   # số khung hình cho mỗi n (fps = 10 -> 3 giây)
FPS = 10

# Phân phối không chuẩn: mũ Exp(1) có mu = 1, sigma = 1, lệch phải rõ rệt.
MU, SIGMA = 1.0, 1.0


def standardized_means(n: int) -> np.ndarray:
    """Z_n = (X_bar - mu) / (sigma / sqrt(n)) cho REPS lần lấy mẫu."""
    samples = rng.exponential(scale=1.0, size=(REPS, n))
    return (samples.mean(axis=1) - MU) / (SIGMA / np.sqrt(n))


DATA = {n: standardized_means(n) for n in N_VALUES}
BINS = np.linspace(-4, 6, 71)
XS = np.linspace(-4, 6, 400)
NORMAL = np.exp(-XS**2 / 2) / np.sqrt(2 * np.pi)

fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=100)
fig.patch.set_facecolor("#f3f7fb")


def draw(frame: int):
    idx = min(frame // FRAMES_PER_N, len(N_VALUES) - 1)
    n = N_VALUES[idx]
    # Histogram "mọc dần": số điểm dữ liệu hiển thị tăng theo khung hình.
    progress = (frame % FRAMES_PER_N + 1) / FRAMES_PER_N
    k = max(50, int(REPS * progress))
    z = DATA[n][:k]

    ax.clear()
    ax.set_facecolor("white")
    ax.hist(z, bins=BINS, density=True, color="#0b79d0", alpha=0.85,
            edgecolor="white", linewidth=0.4, label="Histogram của $Z_n$")
    ax.plot(XS, NORMAL, color="#c0392b", lw=2.5, label="$\\mathcal{N}(0,1)$")
    ax.set_xlim(-4, 6)
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("Trung bình mẫu chuẩn hóa $Z_n$", fontsize=12)
    ax.set_ylabel("Mật độ", fontsize=12)
    ax.set_title(f"Định lí giới hạn trung tâm — n = {n}   "
                 f"({k:,} lần lấy mẫu)", fontsize=15, color="#083b70")
    ax.text(0.98, 0.62, "Phân phối gốc: Exp(1)\n(lệch phải, không chuẩn)",
            transform=ax.transAxes, ha="right", fontsize=11, color="#172033")
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(alpha=0.25)


total_frames = len(N_VALUES) * FRAMES_PER_N
anim = FuncAnimation(fig, draw, frames=total_frames, interval=1000 / FPS)
writer = FFMpegWriter(
    fps=FPS,
    codec="libx264",
    extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-crf", "28", "-preset", "veryfast"],
)
anim.save(str(OUT), writer=writer)
print("Đã tạo:", OUT, f"({OUT.stat().st_size / 1024:.0f} KB)")
