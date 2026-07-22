import sys
import time

lirik_lagu = [
    ("0:00", "Bila kau lihat", 90, 2250),
    ("0:03", "Ku tanpa sengaja..", 90, 2000),
    ("0:07", "Oohh..", 90, 850),
    ("0:08", "Beginikah surga", 90, 800),
    ("0:10", "Bayangkan", 110, 700),
    ("0:12", "Bila", 120, 850),
    ("0:13", "Kau ajakku bicara..", 125, 4200),
    ("0:20", "Ini semua bukan salahmu", 120, 2400),
    ("0:25", "Punya magis perekat yang sekuat itu", 90, 2000),
    ("0:30", "Dari lahir sudah begitu", 120, 1750),
    ("0:35", "Maafkan..", 120, 3000),
    ("0:39", "Aku jatuh suka", 120, 850),
]

WARNA = [
    "\033[38;5;220m",
    "\033[38;5;210m",
    "\033[38;5;80m",
]
RESET = "\033[0m"


def lirik(waktu, teks, kecepatan_ms, jeda_ms, warna):
    print(f"[{waktu}] ", end='')
    sys.stdout.write(warna)
    for karakter in teks:
        print(karakter, end='')
        sys.stdout.flush()
        time.sleep(kecepatan_ms / 1000)
    sys.stdout.write(RESET)
    print()
    time.sleep(jeda_ms / 1000)


def main():
    print("")
    for i, (waktu, teks, kecepatan_ms, jeda_ms) in enumerate(lirik_lagu):
        warna = WARNA[i % len(WARNA)]
        lirik(waktu, teks, kecepatan_ms, jeda_ms, warna)


if __name__ == "__main__":
    main()