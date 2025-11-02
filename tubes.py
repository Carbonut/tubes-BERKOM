import time, sys, os
from datetime import datetime

# --------
# UTILITAS 
# --------

def cetak(teks):
    print(teks)

def garis():
    print("─" * 55)

def cetak_struk(teks):
    print(teks)

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
    cetak("🔐 Selamat datang di Sistem Kasir WARBUM 🛒\n")
    print("1. Login (sudah punya akun)")
    print("2. Sign In (buat akun baru)")
    mode = input("Pilih (1/2): ")

    if mode == "2":
        cetak("\n🆕 Pendaftaran Akun Baru")
        new_user = input("Masukkan username baru: ")
        if new_user in akun_kasir:
            cetak("⚠️ Username sudah digunakan, silakan login.")
            continue
        new_pw = input("Masukkan password: ")
        akun_kasir[new_user] = new_pw
        poin_user[new_user] = 0
        voucher_user[new_user] = 0
        simpan_akun(akun_kasir)
        simpan_poin(poin_user)
        simpan_voucher(voucher_user)
        cetak("✅ Akun berhasil dibuat! Silakan login dengan akun baru Anda.\n")
        continue

    elif mode == "1":
        user = input("\n👤 Username: ")
        pw = input("🔑 Password: ")
        if user in akun_kasir and akun_kasir[user] == pw:
            cetak(f"\n✅ Login berhasil! Selamat datang, {user.upper()}!\n")
            login_user = user
            break
        else:
            cetak("❌ Username atau password salah!\n")
    else:
        cetak("❌ Pilihan tidak valid!\n")

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
    cetak("🎯 MENU PENUKARAN POIN\n")
    poin_saya = poin_user.get(username, 0)
    cetak(f"💎 Poin kamu saat ini: {poin_saya}")
    cetak(f"🎟️ Voucher kamu saat ini: {voucher_user.get(username, 0)} voucher diskon")

    if poin_saya >= 100:
        tukar = input("Apakah kamu ingin menukar 100 poin menjadi 1 voucher diskon 10%? (yes/no): ").lower()
        if tukar == "yes":
            poin_user[username] -= 100
            voucher_user[username] = voucher_user.get(username, 0) + 1
            simpan_poin(poin_user)
            simpan_voucher(voucher_user)
            cetak("✅ Penukaran berhasil! Voucher dapat digunakan nanti.")
        else:
            cetak("❌ Penukaran dibatalkan.")
    else:
        cetak("⚠️ Poin kamu belum cukup (butuh minimal 100 poin).")

# -----------------
# FUNGSI MODE ADMIN
# -----------------
transaksi_list = []
def mode_admin():
    global kategori_menu
    cetak("🧮 Masuk ke MODE ADMIN\n")
    print("1. Lihat Statistik Penjualan")
    print("2. Tambahkan Menu Baru 🍽️")
    print("3. Kembali")
    pilihan_admin = input("Pilih menu admin (1-3): ")
    
    if pilihan_admin == "1":
        if not transaksi_list:
            cetak("⚠️ Belum ada transaksi untuk ditampilkan.")
        else:
            total_transaksi = len(transaksi_list)
            total_pendapatan = sum(t["total_bayar"] for t in transaksi_list)
            
            # Hitung item terlaris
            item_counter = {}
            for t in transaksi_list:
                for _, nama, _, jumlah in t["keranjang"]:
                    item_counter[nama] = item_counter.get(nama, 0) + jumlah

            item_terlaris = max(item_counter, key=item_counter.get)
            
            cetak("📊 Statistik Penjualan")
            garis()
            cetak(f"Total Transaksi   : {total_transaksi}")
            cetak(f"Total Pendapatan : Rp{int(total_pendapatan)}")
            cetak(f"Item Terlaris    : {item_terlaris} ({item_counter[item_terlaris]} pcs)")
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
        cetak(f"✅ Menu '{nama}' berhasil ditambahkan ke {kategori_terpilih}!")
    else:
        cetak("Kembali ke menu utama...")

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
            cetak("❌ Pilihan tidak valid!")
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
            cetak("❌ Kode tidak valid!")

        lagi = input("Apakah ada tambahan menu? (yes/no): ").lower()
        if lagi != "yes":
            break

    garis()
    print("🧾  RINCIAN PESANAN")
    waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cetak(f"🕒 Waktu Transaksi: {waktu_transaksi}\n")
    total = 0
    for _, nama, harga, jumlah in keranjang:
        subtotal = harga * jumlah
        cetak(f"{nama:<15} ({jumlah}x) = Rp{subtotal}")
        total += subtotal
    garis()
    cetak(f"💰 Total sebelum diskon: Rp{total}")

    transaksi_list.append({
        "user": username,
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
            cetak("✅ Voucher diskon 10% digunakan!")
    else:
        kode_diskon = input("\nApakah kamu punya kode diskon? (yes/no): ").lower()
        if kode_diskon == "yes":
            kode = input("Masukkan kode diskon: ").upper()
            if kode == "HEMAT10":
                diskon = total * 0.10
                cetak("✅ Diskon 10% diterapkan!")
            elif kode == "MAKAN20":
                diskon = total * 0.20
                cetak("✅ Diskon 20% diterapkan!")
            elif kode == "KOPI5K":
                diskon = 5000
                cetak("✅ Potongan Rp5.000 diterapkan!")
            else:
                cetak("❌ Kode tidak valid atau kadaluarsa.")

    total -= diskon
    garis()
    cetak(f"💸 Total diskon: Rp{int(diskon)}")
    cetak(f"💰 Total bayar: Rp{int(total)}")

    metode = int(input("\n1. Tunai\n2. QRIS\nPilih metode (1/2): "))
    if metode == 1:
        bayar = int(input("Nominal uang: "))
        if bayar < total:
            cetak("❌ Uang kurang!")
            return
        kembalian = bayar - total
        cetak(f"💵 Kembalian: Rp{kembalian}")
    else:
        cetak("💳 Pembayaran QRIS berhasil!")

    poin_didapat = int(total // 10000)
    poin_user[username] = poin_user.get(username, 0) + poin_didapat
    simpan_poin(poin_user)
    cetak(f"🎁 Kamu dapat {poin_didapat} poin! Total poin sekarang: {poin_user[username]}\n")

    # CETAK STRUK TANPA ANIMASI
    garis()
    cetak("\n🖨️ Sedang mencetak struk...\n")

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

    cetak_struk(struk)

    with open("struk_terakhir.txt", "w", encoding="utf-8") as f:
        f.write(struk)

    cetak("\n✅ Struk telah dicetak & disimpan (struk_terakhir.txt)\n")

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
        cetak("👋 Terima kasih telah menggunakan kasir WARBUM!")
        break
    else:
        cetak("❌ Pilihan tidak valid!")

# LINK WEBSITE https://wartegmasadepan163.streamlit.app/
