# ============================================================================================
# PROGRAM KASIR WARBUM (Versi Final Sederhana)
# Fitur: Login, Simpan Akun, Poin, Voucher, Kode Diskon, Non Tunai, Admin, Transaksi Tersimpan
# ============================================================================================

## FUNGSI ##
# akun.txt                akun (Array)                              muat_akun() (Baca) / simpan_akun(akun) (Tulis)
# poin.txt                poin_user (Dictionary)                    muat_poin() (Baca) / simpan_poin(poin) (Tulis)
# voucher.txt             voucher_user (Dictionary)                 muat_voucher() (Baca) / simpan_voucher(voucher) (Tulis)
# transaksi.txt           riwayat_transaksi (Array)                 muat_transaksi() (Baca) / simpan_transaksi(transaksi) (Tulis)

## DATA GLOBAL ##
# akun                    Array                                     Dipakai saat Login/Daftar  
# poin_user               dictionary                                Dipakai saat Tukar Poin & Transaksi 
# voucher_user            dictionary                                Dipakai saat Tukar Poin & Transaksi
# riwayat_transaksi       Array                                     Dipakai oleh Mode Admin
# kategori_menu           Array                                     Digunakan saat Pemesanan & Admin
# username                string                                    Global State
# login                   boolean                                   Global State (Saat Inisialisasi)
# jalan                   boolean                                   Loop Kontrol Utama

## VARIABEL LOKAL ##
# keranjang               Array                                     List item yang sedang dipesan dalam transaksi. Format: [nama, harga, jumlah, subtotal]
# total                   integer                                   Total biaya awal (sebelum diskon).
# diskon                  integer                                   Nilai total diskon yang diterapkan (dari voucher/kode promo).
# total_bayar             integer                                   Total akhir yang harus dibayar setelah diskon.
# bayar                   integer                                   Nominal uang tunai yang diberikan pelanggan.
# kembalian               integer                                   Selisih uang kembali (bayar - total_bayar).
# poin_tambah             integer                                   Jumlah poin baru yang diperoleh pelanggan (Rp10.000 = 1 poin)
# mode                    string                                    Pilihan menu di dalam Mode Admin (1, 2, atau 3).
# pendapatan              integer                                   Total akumulasi pendapatan dari "riwayat_transaksi".
# pilih_kat               integer                                   Pilihan indeks kategori saat Admin menambah menu baru.


import os

# -----------------------------
# FUNGSI FILE UNTUK SIMPAN DATA
# -----------------------------
def muat_akun():
    akun = []
    if os.path.exists("akun.txt"):
        with open("akun.txt", "r") as f:
            for line in f:
                data = line.strip().split(":")
                if len(data) == 2:
                    akun.append([data[0], data[1]])
    return akun

def simpan_akun(akun):
    with open("akun.txt", "w") as f:
        for a in akun:
            f.write(a[0] + ":" + a[1] + "\n")

def muat_poin():
    poin = {}
    if os.path.exists("poin.txt"):
        with open("poin.txt", "r") as f:
            for line in f:
                data = line.strip().split(":")
                if len(data) == 2:
                    poin[data[0]] = int(data[1])
    return poin

def simpan_poin(poin):
    with open("poin.txt", "w") as f:
        for user in poin:
            f.write(user + ":" + str(poin[user]) + "\n")

def muat_voucher():
    voucher = {}
    if os.path.exists("voucher.txt"):
        with open("voucher.txt", "r") as f:
            for line in f:
                data = line.strip().split(":")
                if len(data) == 2:
                    voucher[data[0]] = int(data[1])
    return voucher

def simpan_voucher(voucher):
    with open("voucher.txt", "w") as f:
        for user in voucher:
            f.write(user + ":" + str(voucher[user]) + "\n")

def muat_transaksi():
    transaksi = []
    if os.path.exists("transaksi.txt"):
        with open("transaksi.txt", "r") as f:
            for line in f:
                data = line.strip().split("|")
                if len(data) == 3:
                    user = data[0]
                    deskripsi = data[1]
                    total = int(data[2])
                    transaksi.append([user, deskripsi, total])
    return transaksi

def simpan_transaksi(transaksi):
    with open("transaksi.txt", "w") as f:
        for t in transaksi:
            f.write(t[0] + "|" + t[1] + "|" + str(t[2]) + "\n")

# -----------------------------
# LOGIN DAN PENDAFTARAN
# -----------------------------
akun = muat_akun()
poin_user = muat_poin()
voucher_user = muat_voucher()
riwayat_transaksi = muat_transaksi()
username = ""
login = False

print("╔════════════════════════════════╗")
print("║      SELAMAT DATANG DI WARBUM  ║")
print("╚════════════════════════════════╝")

while not login:
    print("\n1. Login")
    print("2. Daftar Akun Baru")
    pilih = input("Pilih (1/2): ")

    if pilih == "1":
        user = input("Masukkan username: ")
        pw = input("Masukkan password: ")
        for a in akun:
            if a[0] == user and a[1] == pw:
                print("Login berhasil! Selamat datang,", user)
                username = user
                if username not in poin_user:
                    poin_user[username] = 0
                if username not in voucher_user:
                    voucher_user[username] = 0
                login = True
                break
        if not login:
            print("Username atau password salah!")

    elif pilih == "2":
        user_baru = input("Masukkan username baru: ")
        pw_baru = input("Masukkan password baru: ")
        akun.append([user_baru, pw_baru])
        simpan_akun(akun)
        poin_user[user_baru] = 0
        voucher_user[user_baru] = 0
        simpan_poin(poin_user)
        simpan_voucher(voucher_user)
        print("Akun berhasil dibuat! Silakan login.")
    else:
        print("Pilihan tidak valid!")

# -----------------------------
# DATA MENU
# -----------------------------
kategori_menu = [
    ["Makanan Utama", [
        ["A", "Nasi Goreng", 15000],
        ["B", "Mie Ayam", 12000],
        ["C", "Ayam Geprek", 14000]
    ]],
    ["Minuman", [
        ["D", "Es Teh", 5000],
        ["E", "Kopi", 7000],
        ["F", "Jus Alpukat", 12000]
    ]],
    ["Cemilan / Dessert", [
        ["G", "Donat", 8000],
        ["H", "Pisang Goreng", 9000],
        ["I", "Roti Bakar", 10000]
    ]]
]

jalan = True

# -----------------------------
# MENU UTAMA
# -----------------------------
while jalan:
    print("\n╔════════════════════════════════╗")
    print("║         MENU UTAMA WARBUM       ║")
    print("╚════════════════════════════════╝")
    print("1. Mulai Pemesanan")
    print("2. Tukar Poin")
    print("3. Mode Admin")
    print("4. Keluar")

    pilih = input("Pilih menu (1-4): ")

    # ===============================
    # FITUR 1: PEMESANAN
    # ===============================
    if pilih == "1":
        keranjang = []
        total = 0
        lanjut = True

        while lanjut:
            print("\nPilih kategori:")
            for i in range(len(kategori_menu)):
                print(str(i+1) + ". " + kategori_menu[i][0])
            kat = int(input("Masukkan nomor kategori: ")) - 1

            if 0 <= kat < len(kategori_menu):
                print("\n--- " + kategori_menu[kat][0] + " ---")
                for item in kategori_menu[kat][1]:
                    print(item[0] + ". " + item[1] + " - Rp" + str(item[2]))

                kode = input("Masukkan kode menu: ").upper()
                jumlah = int(input("Masukkan jumlah: "))
                ditemukan = False

                for m in kategori_menu[kat][1]:
                    if m[0] == kode:
                        subtotal = m[2] * jumlah
                        keranjang.append([m[1], m[2], jumlah, subtotal])
                        total += subtotal
                        print(m[1], "ditambahkan (" + str(jumlah) + "x)")
                        ditemukan = True
                        break

                if not ditemukan:
                    print("Kode menu tidak ditemukan!")
            else:
                print("Kategori tidak valid!")

            ulang = input("Tambah menu lain? (yes/no): ").lower()
            if ulang != "yes":
                lanjut = False

        print("\n=== RINCIAN PESANAN ===")
        for k in keranjang:
            print(k[0], "(" + str(k[2]) + "x) = Rp" + str(k[3]))
        print("Total sebelum diskon: Rp" + str(total))

        # Diskon dari voucher
        diskon = 0
        if voucher_user.get(username, 0) > 0:
            pakai = input("Gunakan voucher 10%? (yes/no): ").lower()
            if pakai == "yes":
                diskon = total * 0.1
                voucher_user[username] -= 1
                simpan_voucher(voucher_user)
                print("Voucher digunakan!")

        # Diskon dari kode promo
        else:
            pakai_kode = input("Punya kode diskon? (yes/no): ").lower()
            if pakai_kode == "yes":
                kode = input("Masukkan kode diskon: ").upper()
                if kode == "HEMAT10":
                    diskon = total * 0.10
                    print("Diskon 10% diterapkan!")
                elif kode == "MAKAN20":
                    diskon = total * 0.20
                    print("Diskon 20% diterapkan!")
                elif kode == "KOPI5K":
                    diskon = 5000
                    print("Potongan Rp5000 diterapkan!")
                else:
                    print("Kode tidak valid atau kadaluarsa.")

        total_bayar = total - diskon
        print("Total diskon: Rp" + str(int(diskon)))
        print("Total bayar: Rp" + str(int(total_bayar)))

        # Metode pembayaran
        print("\nPilih metode pembayaran:")
        print("1. Tunai")
        print("2. Non-Tunai (QRIS)")
        metode = input("Pilih (1/2): ")

        if metode == "1":
            bayar = int(input("Masukkan uang: "))
            if bayar >= total_bayar:
                kembalian = bayar - total_bayar
                print("Kembalian: Rp" + str(kembalian))
            else:
                print("Uang tidak cukup!")
                continue
        elif metode == "2":
            print("Pembayaran QRIS berhasil")
        else:
            print("Metode tidak valid!")
            continue

        poin_tambah = total_bayar // 10000
        poin_user[username] = poin_user.get(username, 0) + int(poin_tambah)
        simpan_poin(poin_user)
        print("Kamu dapat", poin_tambah, "poin! Total poin:", poin_user[username])

        riwayat_transaksi.append([username, "Transaksi", total_bayar])
        simpan_transaksi(riwayat_transaksi)

    # ===============================
    # FITUR 2: TUKAR POIN
    # ===============================
    elif pilih == "2":
        print("\n=== PENUKARAN POIN ===")
        print("Poin kamu:", poin_user.get(username, 0))
        print("Voucher kamu:", voucher_user.get(username, 0))

        if poin_user.get(username, 0) >= 100:
            tukar = input("Tukar 100 poin jadi 1 voucher? (yes/no): ").lower()
            if tukar == "yes":
                poin_user[username] -= 100
                voucher_user[username] = voucher_user.get(username, 0) + 1
                simpan_poin(poin_user)
                simpan_voucher(voucher_user)
                print("Penukaran berhasil! Voucher bertambah.")
            else:
                print("Penukaran dibatalkan.")
        else:
            print("Poin belum cukup (minimal 100 poin).")

    # ===============================
    # FITUR 3: MODE ADMIN
    # ===============================
    elif pilih == "3":
        if username != "admin":
            print("Akses ditolak! Hanya admin yang bisa masuk.")
        else:
            print("\n=== MODE ADMIN ===")
            print("1. Lihat Statistik Penjualan")
            print("2. Tambah Menu Baru")
            print("3. Kembali")
            mode = input("Pilih menu admin (1-3): ")

            if mode == "1":
                if len(riwayat_transaksi) == 0:
                    print("Belum ada transaksi.")
                else:
                    total_transaksi = len(riwayat_transaksi)
                    pendapatan = 0
                    for t in riwayat_transaksi:
                        pendapatan += t[2]

                    print("\n=== Statistik Penjualan ===")
                    print("Total Transaksi :", total_transaksi)
                    print("Total Pendapatan: Rp" + str(pendapatan))
                    print("\nDaftar Transaksi:")
                    for t in riwayat_transaksi:
                        print("-", t[0], "membayar Rp" + str(t[2]))

            elif mode == "2":
                print("\nKategori:")
                for i in range(len(kategori_menu)):
                    print(str(i+1) + ". " + kategori_menu[i][0])
                pilih_kat = int(input("Pilih kategori (1-3): ")) - 1

                if 0 <= pilih_kat < len(kategori_menu):
                    kode = input("Masukkan kode menu baru: ").upper()
                    nama = input("Masukkan nama menu: ")
                    harga = int(input("Masukkan harga menu: "))
                    kategori_menu[pilih_kat][1].append([kode, nama, harga])
                    print("Menu '" + nama + "' berhasil ditambahkan!")
                else:
                    print("Kategori tidak valid!")
            else:
                print("Kembali ke menu utama...")

    # ===============================
    # FITUR 4: KELUAR
    # ===============================
    elif pilih == "4":
        print("Terima kasih telah menggunakan kasir WARBUM!")
        jalan = False
    else:
        print("Pilihan tidak valid!")
