import time, sys, os
from datetime import datetime

# ------------------
# ANIMASI & UTILITAS
# ------------------

def ketik(teks, delay=0.03):
    for char in teks:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def garis():
    print("─" * 55)

def animasi_cetak_struk(teks):
    for baris in teks.splitlines():
        for char in baris:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.002)
        print()
        time.sleep(0.05)

os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------
# SISTEM LOGIN & SIGN IN
# ----------------------

def muat_akun():
    akun = {}
    if os.path.exists("akun_kasir.txt"):
        with open("akun_kasir.txt") as f:
            for line in f:
                if ":" in line:
                    user, pw = line.strip().split(":")
                    akun[user] = pw
    return akun

def simpan_akun(akun):
    with open("akun_kasir.txt", "w") as f:
        for user, pw in akun.items():
            f.write(f"{user}:{pw}\n")

def muat_poin():
    poin = {}
    if os.path.exists("poin_pelanggan.txt"):
        with open("poin_pelanggan.txt") as f:
            for line in f:
                if ":" in line:
                    user, p = line.strip().split(":")
                    poin[user] = int(p)
    return poin

def simpan_poin(poin):
    with open("poin_pelanggan.txt", "w") as f:
        for user, p in poin.items():
            f.write(f"{user}:{p}\n")

def muat_voucher():
    voucher = {}
    if os.path.exists("voucher_diskon.txt"):
        with open("voucher_diskon.txt") as f:
            for line in f:
                if ":" in line:
                    user, val = line.strip().split(":")
                    voucher[user] = int(val)
    return voucher

def simpan_voucher(voucher):
    with open("voucher_diskon.txt", "w") as f:
        for user, val in voucher.items():
            f.write(f"{user}:{val}\n")

# --------------
# LOAD DATA USER
# --------------

akun_kasir = muat_akun()
poin_user = muat_poin()
voucher_user = muat_voucher()

# ----------------------
# PROSES LOGIN / SIGN IN
# ----------------------

while True:
    ketik("🔐 Selamat datang di Sistem Kasir WARBUM 🛒\n", 0.04)
    print("1. Login (sudah punya akun)")
    print("2. Sign In (buat akun baru)")
    mode = input("Pilih (1/2): ")

    if mode == "2":
        ketik("\n🆕 Pendaftaran Akun Baru", 0.03)
        new_user = input("Masukkan username baru: ")
        if new_user in akun_kasir:
            ketik("⚠️ Username sudah digunakan, silakan login.")
            continue
        new_pw = input("Masukkan password: ")
        akun_kasir[new_user] = new_pw
        poin_user[new_user] = 0
        voucher_user[new_user] = 0
        simpan_akun(akun_kasir)
        simpan_poin(poin_user)
        simpan_voucher(voucher_user)
        ketik("✅ Akun berhasil dibuat! Silakan login dengan akun baru Anda.\n", 0.04)
        continue

    elif mode == "1":
        user = input("\n👤 Username: ")
        pw = input("🔑 Password: ")
        if user in akun_kasir and akun_kasir[user] == pw:
            ketik(f"\n✅ Login berhasil! Selamat datang, {user.upper()}!\n", 0.04)
            login_user = user
            break
        else:
            ketik("❌ Username atau password salah!\n", 0.04)
    else:
        ketik("❌ Pilihan tidak valid!\n", 0.03)

# ----------
# MENU UTAMA
# ----------

def menu_awal():
    print("╔════════════════════════════════╗")
    print("║   WARBUM CASHIER SYSTEM MENU   ║")
    print("╚════════════════════════════════╝")
    print("1. Mulai Kasir 🛒")
    print("2. Earn Point (Tukar Poin 🎯)")
    print("3. Mode Admin ⚙️")
    print("4. Keluar 🚪")
    return input("Pilih menu (1-4): ")

# -----------------
# FUNGSI EARN POINT 
# -----------------

def earn_point(username):
    global poin_user, voucher_user
    garis()
    ketik("🎯 MENU PENUKARAN POIN\n", 0.03)
    poin_saya = poin_user.get(username, 0)
    ketik(f"💎 Poin kamu saat ini: {poin_saya}", 0.03)
    ketik(f"🎟️ Voucher kamu saat ini: {voucher_user.get(username, 0)} voucher diskon", 0.03)

    if poin_saya >= 100:
        tukar = input("Apakah kamu ingin menukar 100 poin menjadi 1 voucher diskon 10%? (yes/no): ").lower()
        if tukar == "yes":
            poin_user[username] -= 100
            voucher_user[username] = voucher_user.get(username, 0) + 1
            simpan_poin(poin_user)
            simpan_voucher(voucher_user)
            ketik("✅ Penukaran berhasil! Voucher dapat digunakan nanti.", 0.03)
        else:
            ketik("❌ Penukaran dibatalkan.", 0.03)
    else:
        ketik("⚠️ Poin kamu belum cukup (butuh minimal 100 poin).", 0.03)

# -----------------
# FUNGSI MODE ADMIN
# -----------------
transaksi_list = []
def mode_admin():
    global kategori_menu
    ketik("🧮 Masuk ke MODE ADMIN\n", 0.04)
    print("1. Lihat Statistik Penjualan")
    print("2. Tambahkan Menu Baru 🍽️")
    print("3. Kembali")
    pilihan_admin = input("Pilih menu admin (1-3): ")
    
    if pilihan_admin == "1":
        if not transaksi_list:
            ketik("⚠️ Belum ada transaksi untuk ditampilkan.", 0.03)
        else:
            total_transaksi = len(transaksi_list)
            total_pendapatan = sum(t["total_bayar"] for t in transaksi_list)
            
            # Hitung item terlaris
            item_counter = {}
            for t in transaksi_list:
                for _, nama, _, jumlah in t["keranjang"]:
                    item_counter[nama] = item_counter.get(nama, 0) + jumlah

            item_terlaris = max(item_counter, key=item_counter.get)
            
            ketik("📊 Statistik Penjualan", 0.03)
            garis()
            ketik(f"Total Transaksi   : {total_transaksi}")
            ketik(f"Total Pendapatan : Rp{int(total_pendapatan)}")
            ketik(f"Item Terlaris    : {item_terlaris} ({item_counter[item_terlaris]} pcs)")
            garis()
        
    if pilihan_admin == "2":
        print("\n📋 Tambah Menu Baru")
        for i, kategori in enumerate(kategori_menu.keys(), 1):
            print(f"{i}. {kategori}")
        pilih = int(input("Pilih kategori (1-3): "))
        kategori_terpilih = list(kategori_menu.keys())[pilih - 1]
        kode = input("Masukkan kode menu (huruf unik): ").upper()
        nama = input("Masukkan nama menu: ")
        harga = int(input("Masukkan harga menu: "))
        kategori_menu[kategori_terpilih].append([kode, nama, harga])
        ketik(f"✅ Menu '{nama}' berhasil ditambahkan ke {kategori_terpilih}!", 0.03)
    else:
        ketik("Kembali ke menu utama...")

# ---------
# DATA MENU
# ---------

kategori_menu = {
    "🍚 Makanan Utama": [
        ["A", "Nasi Goreng", 15000],
        ["B", "Mie Ayam", 12000],
        ["C", "Ayam Geprek", 14000],
    ],
    "☕ Minuman": [
        ["D", "Es Teh", 5000],
        ["E", "Kopi", 7000],
        ["F", "Jus Alpukat", 12000],
    ],
    "🍩 Cemilan / Dessert": [
        ["G", "Donat", 8000],
        ["H", "Pisang Goreng", 9000],
        ["I", "Roti Bakar", 10000]
    ]
}

# ------------
# FUNGSI KASIR
# ------------

def mulai_kasir(username):
    global poin_user, voucher_user
    keranjang = []

    while True:
        print("\n🍽️  PILIH KATEGORI MENU")
        for i, kategori in enumerate(kategori_menu.keys(), 1):
            print(f"{i}. {kategori}")
        garis()

        try:
            pilih_kat = int(input("Masukkan nomor kategori: "))
            kategori_terpilih = list(kategori_menu.keys())[pilih_kat - 1]
        except (ValueError, IndexError):
            ketik("❌ Pilihan tidak valid!", 0.04)
            continue

        print(f"\n--- {kategori_terpilih} ---")
        for kode, nama, harga in kategori_menu[kategori_terpilih]:
            print(f"{kode}. {nama:<15} - Rp{harga}")
        garis()

        pilihan = input("Masukkan kode item yang ingin dibeli: ").upper()
        ditemukan = False

        for daftar in kategori_menu.values():
            for kode, nama, harga in daftar:
                if pilihan == kode:
                    jumlah = int(input(f"Masukkan jumlah {nama}: "))
                    ditemukan = True
                    keranjang.append([kode, nama, harga, jumlah])
                    break

        if not ditemukan:
            ketik("❌ Kode tidak valid!", 0.04)

        lagi = input("Apakah ada tambahan menu? (yes/no): ").lower()
        if lagi != "yes":
            break

    garis()
    print("🧾  RINCIAN PESANAN")
    waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ketik(f"🕒 Waktu Transaksi: {waktu_transaksi}\n", 0.03)
    total = 0
    for _, nama, harga, jumlah in keranjang:
        subtotal = harga * jumlah
        ketik(f"{nama:<15} ({jumlah}x) = Rp{subtotal}", 0.01)
        total += subtotal
    garis()
    ketik(f"💰 Total sebelum diskon: Rp{total}")

    transaksi_list.append({
    "user": login_user,
    "waktu": waktu_transaksi,
    "keranjang": keranjang,
    "total_bayar": total,
    })
    
    # -----------------------
    # SISTEM DISKON KOMBINASI
    # -----------------------

    diskon = 0
    kembalian = 0

    if voucher_user.get(username, 0) > 0:
        gunakan = input(f"\n🎟️ Kamu punya {voucher_user[username]} voucher diskon 10%. Gunakan sekarang? (yes/no): ").lower()
        if gunakan == "yes":
            diskon = total * 0.1
            voucher_user[username] -= 1
            simpan_voucher(voucher_user)
            ketik("✅ Voucher diskon 10% digunakan!\n", 0.03)
    else:
        kode_diskon = input("\nApakah kamu punya kode diskon? (yes/no): ").lower()
        if kode_diskon == "yes":
            kode = input("Masukkan kode diskon: ").upper()
            if kode == "HEMAT10":
                diskon = total * 0.10
                ketik("✅ Diskon 10% diterapkan!")
            elif kode == "MAKAN20":
                diskon = total * 0.20
                ketik("✅ Diskon 20% diterapkan!")
            elif kode == "KOPI5K":
                diskon = 5000
                ketik("✅ Potongan Rp5.000 diterapkan!")
            else:
                ketik("❌ Kode tidak valid atau kadaluarsa.")

    total -= diskon
    garis()
    ketik(f"💸 Total diskon: Rp{int(diskon)}")
    ketik(f"💰 Total bayar: Rp{int(total)}")

    metode = int(input("\n1. Tunai\n2. QRIS\nPilih metode (1/2): "))
    if metode == 1:
        bayar = int(input("Nominal uang: "))
        if bayar < total:
            ketik("❌ Uang kurang!")
            return
        kembalian = bayar - total
        ketik(f"💵 Kembalian: Rp{kembalian}")
    else:
        ketik("💳 Pembayaran QRIS berhasil!")

    poin_didapat = int(total // 10000)
    poin_user[username] = poin_user.get(username, 0) + poin_didapat
    simpan_poin(poin_user)
    ketik(f"🎁 Kamu dapat {poin_didapat} poin! Total poin sekarang: {poin_user[username]}\n", 0.03)

    # CETAK STRUK DENGAN ANIMASI 
    garis()
    ketik("\n🖨️ Sedang mencetak struk...\n")
    time.sleep(1)

    struk = f"""
╔══════════════════════════════════╗
║          WARBUM CASHIER          ║
╚══════════════════════════════════╝
🕒 {waktu_transaksi}
👤 Kasir: {username}
────────────────────────────────────
"""
    for _, nama, harga, jumlah in keranjang:
        subtotal = harga * jumlah
        struk += f"{nama:<15} x{jumlah:<2} Rp{subtotal}\n"

    struk += f"""────────────────────────────────────
💸 Diskon     : Rp{int(diskon)}
💰 Total Bayar: Rp{int(total)}
💵 Kembalian  : Rp{int(kembalian)}
────────────────────────────────────
Terima kasih telah berbelanja 💚
WARBUM — Nikmati hari lezatmu 🍴
"""

    animasi_cetak_struk(struk)

    with open("struk_terakhir.txt", "w", encoding="utf-8") as f:
        f.write(struk)

    ketik("\n✅ Struk telah dicetak & disimpan (struk_terakhir.txt)\n")

# ---------------
# LOOP MENU UTAMA
# ---------------

while True:
    pilih = menu_awal()
    if pilih == "1":
        mulai_kasir(login_user)
    elif pilih == "2":
        earn_point(login_user)
    elif pilih == "3":
        mode_admin()
    elif pilih == "4":
        ketik("👋 Terima kasih telah menggunakan kasir WARBUM!")
        break
    else:
        ketik("❌ Pilihan tidak valid!")

# LINK WEBSITE https://wartegmasadepan163.streamlit.app/