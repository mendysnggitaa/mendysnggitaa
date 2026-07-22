"""
Animasi Salju & Love (Hati) dengan Python (matplotlib)
--------------------------------------------------------
Cara jalankan:
    pip install matplotlib numpy
    python animasi_salju_love.py

Salju putih turun perlahan sambil bergoyang, dan hati-hati kecil warna-warni
melayang naik dari bawah layar. Latar belakang malam biru gelap.

CARA GANTI LIRIK:
Edit variabel DAFTAR_LIRIK di bawah. Tiap baris berupa tuple:
    ("teks lirik", durasi_tampil_dalam_detik)
Baris akan tampil di tengah layar, otomatis fade in/out, lalu ganti ke
baris berikutnya sesuai durasi yang kamu atur. Setelah baris terakhir
habis, lirik akan mengulang lagi dari baris pertama.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.path import Path
import random
import time

# ----- Pengaturan layar -----
LEBAR, TINGGI = 100, 100
JUMLAH_SALJU = 120
JUMLAH_HATI_MAKS = 25

WARNA_HATI = ["#ff5e78", "#ff8fa3", "#ff3b6e", "#ffd1dc", "#ff6fae"]

# ----- Daftar lirik & durasi tampil (dalam detik) -----
# GANTI teks di bawah ini dengan lirik/kalimat kamu sendiri.
# Format: (teks, durasi_detik). Baris berikutnya otomatis muncul setelah waktu habis.
# ----- Daftar lirik & durasi tampil (dalam detik) -----
# Durasi tiap baris di bawah sudah saya samakan sesuai catatan kamu (4, 5, 9, 5, 4, 3, 5 detik).
# Tinggal ganti teks "Baris 1", "Baris 2", dst dengan lirik aslinya ya —
# saya tidak menuliskan lirik lagu di sini karena itu materi berhak cipta.
# Format: (teks, durasi_detik).
DAFTAR_LIRIK = [
    ("So, what if I call", 4),
    ("And you pick up the phone?", 5),
    ("And I use this holiday to makе my way to your ghost", 9),
    ("Oh, what if you're lonely", 5),
    ("And you know I am too?", 4),
    ("Merry Christmas, I miss you", 3),
    ("I miss you", 5),
]

# ----- Bentuk hati sebagai Path custom, memakai rumus kurva hati matematika -----
# x = 16 sin^3(t) ; y = 13 cos(t) - 5 cos(2t) - 2 cos(3t) - cos(4t)
_t = np.linspace(0, 2 * np.pi, 60)
_hx = 16 * np.sin(_t) ** 3
_hy = 13 * np.cos(_t) - 5 * np.cos(2 * _t) - 2 * np.cos(3 * _t) - np.cos(4 * _t)
_skala = max(np.max(np.abs(_hx)), np.max(np.abs(_hy)))
_hx /= _skala
_hy /= _skala
_verts_hati = list(zip(_hx, _hy))
_codes_hati = [Path.MOVETO] + [Path.LINETO] * (len(_verts_hati) - 2) + [Path.CLOSEPOLY]
MARKER_HATI = Path(_verts_hati, _codes_hati)


class Salju:
    """Satu kepingan salju yang jatuh perlahan sambil bergoyang."""
    def __init__(self):
        self.x = random.uniform(0, LEBAR)
        self.y = random.uniform(0, TINGGI)
        self.ukuran = random.uniform(2, 7)
        self.kecepatan_jatuh = self.ukuran * random.uniform(0.03, 0.06)
        self.fase_goyang = random.uniform(0, 2 * np.pi)
        self.amplitudo_goyang = random.uniform(0.15, 0.5)
        self.kecerahan = random.uniform(0.55, 1.0)

    def update(self):
        self.y -= self.kecepatan_jatuh
        self.fase_goyang += 0.03
        self.x += np.sin(self.fase_goyang) * self.amplitudo_goyang
        if self.y < 0:
            self.y = TINGGI
            self.x = random.uniform(0, LEBAR)
        if self.x < 0:
            self.x = LEBAR
        elif self.x > LEBAR:
            self.x = 0


class Hati:
    """Satu hati kecil yang melayang naik dari bawah layar."""
    def __init__(self):
        self.x = random.uniform(5, LEBAR - 5)
        self.y = random.uniform(-10, 0)
        self.ukuran = random.uniform(80, 260)
        self.kecepatan_naik = random.uniform(0.25, 0.55)
        self.fase_goyang = random.uniform(0, 2 * np.pi)
        self.amplitudo_goyang = random.uniform(0.3, 1.0)
        self.warna = random.choice(WARNA_HATI)
        self.umur = 1.0
        self.laju_pudar = random.uniform(0.004, 0.008)

    def update(self):
        self.y += self.kecepatan_naik
        self.fase_goyang += 0.04
        self.x += np.sin(self.fase_goyang) * self.amplitudo_goyang * 0.15
        if self.y > TINGGI * 0.6:
            self.umur -= self.laju_pudar

    def hidup(self):
        return self.umur > 0 and self.y < TINGGI + 10


# ----- Setup gambar -----
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("#050615")
ax.set_facecolor("#050615")
ax.set_xlim(0, LEBAR)
ax.set_ylim(0, TINGGI)
ax.axis("off")
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Waktu mulai sungguhan (wall-clock), dipakai supaya durasi lirik akurat
# walau kecepatan render animasi berbeda-beda tiap komputer.
waktu_mulai = time.time()

# Bintang latar belakang
bintang_x = np.random.uniform(0, LEBAR, 90)
bintang_y = np.random.uniform(0, TINGGI, 90)
ax.scatter(bintang_x, bintang_y, s=3, color="white", alpha=0.4,
           edgecolors="none", zorder=0)

salju_list = [Salju() for _ in range(JUMLAH_SALJU)]
hati_list = []

scatter_salju_halo = ax.scatter([], [], c="white", edgecolors="none", zorder=1)
scatter_salju = ax.scatter([], [], c="white", edgecolors="none", zorder=2)
scatter_hati = ax.scatter([], [], marker=MARKER_HATI, edgecolors="none", zorder=3)

# Teks lirik di tengah layar (besar), dengan sedikit efek melayang naik-turun
teks_lirik = ax.text(
    LEBAR / 2, TINGGI / 2, "",
    color="white", fontsize=17, fontweight="bold",
    ha="center", va="center", zorder=5,
    alpha=0.0,
)


def buat_hati_baru():
    if len(hati_list) < JUMLAH_HATI_MAKS and random.random() < 0.06:
        hati_list.append(Hati())


# Hitung waktu mulai & selesai tiap baris lirik (kumulatif)
_batas_waktu = []
_t_kumulatif = 0.0
for _teks, _durasi in DAFTAR_LIRIK:
    _batas_waktu.append((_t_kumulatif, _t_kumulatif + _durasi, _teks))
    _t_kumulatif += _durasi
DURASI_TOTAL_LIRIK = _t_kumulatif


def ambil_lirik_aktif(waktu_detik):
    """Cari baris lirik yang aktif pada detik tertentu, plus alpha fade in/out."""
    if not _batas_waktu:
        return "", 0.0
    t = waktu_detik % DURASI_TOTAL_LIRIK  # ulang dari awal setelah selesai
    for mulai, selesai, teks in _batas_waktu:
        if mulai <= t < selesai:
            durasi_baris = selesai - mulai
            posisi = t - mulai
            FADE = 0.4  # detik untuk fade in/out
            if posisi < FADE:
                alpha = posisi / FADE
            elif (durasi_baris - posisi) < FADE:
                alpha = (durasi_baris - posisi) / FADE
            else:
                alpha = 1.0
            return teks, max(0.0, min(1.0, alpha))
    return "", 0.0


def update(frame):
    buat_hati_baru()

    for s in salju_list:
        s.update()

    for h in hati_list[:]:
        h.update()
        if not h.hidup():
            hati_list.remove(h)

    # ----- Gambar salju (inti terang + halo lembut di belakangnya) -----
    xs_s = [s.x for s in salju_list]
    ys_s = [s.y for s in salju_list]
    ukuran_inti = [s.ukuran ** 2 * 0.35 for s in salju_list]
    ukuran_halo = [s.ukuran ** 2 * 1.6 for s in salju_list]
    alpha_s = [s.kecerahan for s in salju_list]
    rgba_inti = [(1, 1, 1, a) for a in alpha_s]
    rgba_halo = [(0.85, 0.9, 1.0, a * 0.25) for a in alpha_s]

    scatter_salju_halo.set_offsets(np.column_stack([xs_s, ys_s]) if xs_s else np.empty((0, 2)))
    scatter_salju_halo.set_sizes(ukuran_halo)
    scatter_salju_halo.set_color(rgba_halo)

    scatter_salju.set_offsets(np.column_stack([xs_s, ys_s]) if xs_s else np.empty((0, 2)))
    scatter_salju.set_sizes(ukuran_inti)
    scatter_salju.set_color(rgba_inti)

    # ----- Gambar hati -----
    xs_h = [h.x for h in hati_list]
    ys_h = [h.y for h in hati_list]
    ukuran_h = [h.ukuran * max(h.umur, 0) for h in hati_list]
    rgba_h = []
    for h in hati_list:
        r_, g_, b_ = plt.matplotlib.colors.to_rgb(h.warna)
        rgba_h.append((r_, g_, b_, max(h.umur, 0)))

    scatter_hati.set_offsets(np.column_stack([xs_h, ys_h]) if xs_h else np.empty((0, 2)))
    scatter_hati.set_sizes(ukuran_h)
    scatter_hati.set_color(rgba_h)

    # ----- Gambar lirik -----
    waktu_detik = time.time() - waktu_mulai
    teks_aktif, alpha_teks = ambil_lirik_aktif(waktu_detik)
    teks_lirik.set_text(teks_aktif)
    teks_lirik.set_alpha(alpha_teks)

    return scatter_salju_halo, scatter_salju, scatter_hati, teks_lirik


ani = animation.FuncAnimation(
    fig, update, frames=600, interval=30, blit=True
)

plt.show()

# Jika ingin menyimpan sebagai video/gif, uncomment salah satu baris berikut:
# ani.save("salju_love.gif", writer="pillow", fps=30)
# ani.save("salju_love.mp4", writer="ffmpeg", fps=30)