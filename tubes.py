print("╔════════════════════════════════╗")
print("║     SELF CASHIER MACHINE 🛒   ║")
print("╚════════════════════════════════╝")

# Daftar harga
daftar_harga = {
    "A": ("Nasi Goreng", 15000),
    "B": ("Mie Ayam", 12000),
    "C": ("Es Teh", 5000),
    "D": ("Kopi", 7000)
}

# Rekomendasi menu otomatis
rekomendasi = {
    "A": "Es Teh cocok untuk menemani Nasi Goreng 🍹",
    "B": "Es Teh dingin pas banget sama Mie Ayam 🍜",
    "C": "Kopi panas enak diminum setelah Es Teh ☕",
    "D": "Donat manis cocok untuk teman minum Kopi 🍩"
}

keranjang = {}

# === MULAI PROGRAM ===
while True:
    print("\n--- MENU UTAMA ---")
    for kode, (nama, harga) in daftar_harga.items():
        print(f"{kode}. {nama} - Rp{harga}")
    print("------------------")

    # Pilih item
    pilihan = input("Masukkan kode item yang ingin dibeli: ").upper()
    if pilihan in daftar_harga:
        jumlah = int(input(f"Masukkan jumlah {daftar_harga[pilihan][0]}: "))
        if pilihan in keranjang:
            keranjang[pilihan] += jumlah
        else:
            keranjang[pilihan] = jumlah
        
        # Tampilkan rekomendasi otomatis
        if pilihan in rekomendasi:
            print(f"💡 Rekomendasi: {rekomendasi[pilihan]}")

    else:
        print("Kode tidak valid!")

    # Tanya apakah ingin menambah item lain
    lagi = input("Apakah ada tambahan menu? (y/n): ").lower()
    if lagi != "y":
        break

# === RINGKASAN PESANAN ===
print("\n--- RINGKASAN PESANAN ---")
total = 0
for kode, jumlah in keranjang.items():
    nama, harga = daftar_harga[kode]
    subtotal = harga * jumlah
    print(f"{nama} ({jumlah}x) = Rp{subtotal}")
    total += subtotal
print(f"Total harga sebelum diskon: Rp{total}")
print("--------------------------")

# === SISTEM KODE DISKON ===
diskon = 0
kode_diskon = input("Apakah Anda memiliki kode diskon? (y/n): ").lower()

if kode_diskon == "y":
    kode = input("Masukkan kode diskon: ").upper()
    if kode == "HEMAT10":
        diskon = total * 0.10
        print("✅ Kode diterima! Anda mendapat diskon 10%")
    elif kode == "MAKAN20":
        diskon = total * 0.20
        print("✅ Kode diterima! Anda mendapat diskon 20%")
    elif kode == "KOPI5K":
        diskon = 5000
        print("✅ Kode diterima! Potongan langsung Rp5.000")
    else:
        print("❌ Kode tidak valid atau sudah kadaluarsa.")

# Update total setelah diskon
total -= diskon
if diskon > 0:
    print(f"Total diskon: Rp{int(diskon)}")
print(f"Total harga setelah diskon: Rp{int(total)}")
print("--------------------------")

# Tanya apakah ingin ubah pesanan
ubah = input("Apakah ada menu yang ingin diubah? (y/n): ").lower()
if ubah == "y":
    print("\nSilakan ubah pesanan Anda.")
    for kode, (nama, harga) in daftar_harga.items():
        print(f"{kode}. {nama}")
    kode_ubah = input("Masukkan kode item yang ingin diubah: ").upper()
    if kode_ubah in keranjang:
        baru = int(input("Masukkan jumlah baru: "))
        keranjang[kode_ubah] = baru
        print("Pesanan berhasil diperbarui!")
    else:
        print("Item tidak ditemukan di keranjang.")
    # Update total lagi
    total = sum(daftar_harga[k][1] * j for k, j in keranjang.items())

# === PEMBAYARAN ===
print("\n--- METODE PEMBAYARAN ---")
print("1. Tunai")
print("2. Non Tunai (QRIS)")
metode = int(input("Pilih metode pembayaran (1/2): "))

if metode == 1:
    bayar = int(input("Masukkan nominal uang: "))
    if bayar < total:
        print("Uang anda kurang, silakan periksa kembali!")
    elif bayar == total:
        print("Pembayaran pas. Terima kasih!")
    else:
        kembalian = bayar - total
        print(f"Kembalian anda: Rp{kembalian}")
elif metode == 2:
    print("Silakan scan kode QR untuk pembayaran non-tunai 💳")
else:
    print("Pilihan tidak valid.")

# === SISTEM POIN PELANGGAN ===
# 1 poin untuk setiap Rp10.000 pembelian
poin = int(total // 10000)
print(f"\n🎁 Anda mendapatkan {poin} poin reward dari pembelian ini!")

# Simpan poin ke file (untuk akumulasi)
with open("poin_pelanggan.txt", "a") as f:
    f.write(f"{poin}\n")

# Hitung total poin pelanggan
total_poin = sum(map(int, open("poin_pelanggan.txt").read().splitlines()))
print(f"Total poin Anda saat ini: {total_poin} ⭐")

# === CETAK STRUK ===
print("\n--- STRUK PEMBELIAN ---")
for kode, jumlah in keranjang.items():
    nama, harga = daftar_harga[kode]
    print(f"{nama} ({jumlah}x) - Rp{harga * jumlah}")
print("--------------------------")
if diskon > 0:
    print(f"Diskon diterapkan  : Rp{int(diskon)}")
print(f"Total Pembayaran   : Rp{int(total)}")
print(f"Poin Didapat       : {poin}")
print(f"Total Poin Anda    : {total_poin}")
print("--------------------------")
print("Terima kasih telah berbelanja di Self Cashier Machine 💖")

print("\nProgram selesai ✅")