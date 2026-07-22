import os
import sys
import time
import random
import unicodedata

# Lirik lagu beserta waktu tampil (timestamp dalam detik sejak lirik mulai berjalan)
# Ganti teks di bawah dengan lirik lagu (salin sendiri dari sumber resmi)
# Format: (waktu_tampil_detik, teks_lirik)
LYRICS = [
    (3.14, "Meski hatiku untuk kamu"),
    (9.57, "Dan hatimu tetap aku"),
    (13.73, "Jangan coba kita tuk bertemu"),
    (20.27, "Takkan sanggup aku bertahan diam"),
    (25.04, "Ingin berlari memelukmu"),
    (31.15, "Yang pernah kumiliki"),
]

# Set karakter Unicode estetik pilihanmu
FLAKES = ["⋆", "꙳", "•", "❅", "‧", "❆", "₊"]
WIDTH = 70
HEIGHT = 22
FPS = 0.04


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def get_padding():
    try:
        term_height = os.get_terminal_size().lines
        return max(0, (term_height - HEIGHT) // 2)
    except OSError:
        return 0


def get_visual_length(text):
    """Menghitung panjang visual teks, memperhitungkan karakter double-width"""
    length = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ("W", "F"):
            length += 2
        else:
            length += 1
    return length


def render(lyric: str, snow: list) -> str:
    """Mengatur pergerakan salju estetik dan menampilkan lirik dengan benar"""

    # Geser salju ke bawah (logic dari bawah ke atas)
    for r in range(HEIGHT - 1, 0, -1):
        for c in range(WIDTH):
            if snow[r - 1][c] != " ":
                # Kecepatan sedang
                if random.random() < 0.09:
                    snow[r][c] = snow[r - 1][c]
                    snow[r - 1][c] = " "

    # Bersihkan baris paling bawah secara berkala
    for c in range(WIDTH):
        if random.random() < 0.10:
            snow[HEIGHT - 1][c] = " "

    # Spawn salju baru di baris paling atas
    for c in range(WIDTH):
        if snow[0][c] == " ":
            snow[0][c] = random.choice(FLAKES) if random.random() < 0.010 else " "

    frame = [row[:] for row in snow]
    mid_row = HEIGHT * 3 // 5

    lyric_visual_len = get_visual_length(lyric)
    start_col = (WIDTH - lyric_visual_len) // 2

    for r_offset in [-1, 0, 1]:
        if 0 <= mid_row + r_offset < HEIGHT:
            frame[mid_row + r_offset] = [" "] * WIDTH

    col = start_col
    for ch in lyric:
        char_len = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if 0 <= col < WIDTH and col + char_len <= WIDTH:
            frame[mid_row][col] = ch
            if char_len == 2:
                frame[mid_row][col + 1] = ""
            col += char_len
        else:
            col += char_len

    return "\n".join("".join(row) for row in frame)


def render_simple_text(lines, pad_rows=0):
    """Menampilkan teks diam (judul/closing) di tengah layar bersih"""
    total_text_rows = len(lines)
    start_row = (HEIGHT - total_text_rows) // 2 + pad_rows

    frame = [[" "] * WIDTH for _ in range(HEIGHT)]

    for i, text in enumerate(lines):
        r = start_row + i
        if 0 <= r < HEIGHT:
            visual_len = get_visual_length(text)
            c = (WIDTH - visual_len) // 2

            curr_c = c
            for ch in text:
                char_len = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
                if 0 <= curr_c < WIDTH and curr_c + char_len <= WIDTH:
                    frame[r][curr_c] = ch
                    if char_len == 2:
                        frame[r][curr_c + 1] = ""
                    curr_c += char_len
                else:
                    curr_c += char_len

    return "\n".join("".join(row) for row in frame)


def cetak_lirik_tepi(snow, pad):
    """Menjalankan animasi salju sambil menampilkan lirik satu per satu.
    Setiap baris punya timestamp (detik sejak lirik mulai berjalan) kapan ia tampil,
    dan tetap tampil sampai timestamp baris berikutnya tiba."""
    start = time.time()

    for i, (ts, teks) in enumerate(LYRICS):
        # Tunggu sampai waktunya baris ini tampil, salju tetap bergerak
        while time.time() - start < ts:
            sys.stdout.write("\033[H" + "\n" * pad + render("", snow))
            sys.stdout.flush()
            time.sleep(FPS)

        # Tentukan kapan baris ini berhenti (yaitu saat baris berikutnya mulai)
        if i + 1 < len(LYRICS):
            ts_berikutnya = LYRICS[i + 1][0]
        else:
            ts_berikutnya = ts + 3.0  # baris terakhir tampil 3 detik

        while time.time() - start < ts_berikutnya:
            sys.stdout.write("\033[H" + "\n" * pad + render(teks, snow))
            sys.stdout.flush()
            time.sleep(FPS)


def main():
    snow = [[" "] * WIDTH for _ in range(HEIGHT)]
    pad = get_padding()

    try:
        hide_cursor()
        clear()

        title_lines = [
            "⋆꙳•❅*‧ ‧*❆ ₊⋆",
            "Titik Nadir",
            "Kahitna",
            "⋆꙳•❅*‧ ‧*❆ ₊⋆",
        ]

        title_output = render_simple_text(title_lines, pad_rows=-1)
        sys.stdout.write("\033[H" + "\n" * pad + title_output)
        sys.stdout.flush()
        time.sleep(3.0)

        deadline = time.time() + 4.0
        while time.time() < deadline:
            sys.stdout.write("\033[H" + "\n" * pad + render("", snow))
            sys.stdout.flush()
            time.sleep(FPS)

        cetak_lirik_tepi(snow, pad)

        clear()
        closing_lines = ["Code by [Mendysia Anggita Putri]"]
        closing_output = render_simple_text(closing_lines)
        sys.stdout.write("\033[H" + "\n" * pad + closing_output)
        sys.stdout.flush()
        time.sleep(3.5)
        clear()

    except KeyboardInterrupt:
        clear()
    finally:
        show_cursor()


if __name__ == "__main__":
    main()