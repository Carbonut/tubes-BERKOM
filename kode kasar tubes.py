print("╔═════════════════╗")
print("║ CASHIER MACHINE ║")
print("╚═════════════════╝")

daftar_harga = {"A": 5000, "B": 6000, "C": 7000, "D": 8000}

print("--- Daftar Harga Barang ---")
for nama_barang, harga_satuan in daftar_harga.items():
    print(f"Barang {nama_barang}: Rp{harga_satuan}")
print("---------------------------")

jumlah = {}
for nama_barang in daftar_harga:
    jumlah_barang = int(input(f"Masukkan jumlah barang {nama_barang} yang dibeli: ")) 
    jumlah[nama_barang] = jumlah_barang 

total_per_barang = {b: daftar_harga[b] * jumlah[b] for b in daftar_harga}

total_keseluruhan = sum(total_per_barang.values())

print("\n--- Rincian Belanja ---")
for b in total_per_barang:
    print(f"Barang {b}: {jumlah[b]} * Rp{daftar_harga[b]} = Rp{total_per_barang[b]}")

print("-----------------------")
print(f"Total yang harus dibayar = Rp{total_keseluruhan}")
print("-----------------------")

print("Metode pembayaran: ")
print("1. Tunai")
print("2. Non Tunai")
print("-----------------------")

pilihan=int(input("Pilih metode pembayaran anda: "))
print("-----------------------")

if pilihan == 1:
    bayar=int(input("Masukkan uang yang anda bayarkan: "))
    if bayar > total_keseluruhan :
        kembalian = bayar - total_keseluruhan
        print("-----------------------")
        print("Kembalian yang akan anda terima: Rp.", kembalian, ", Silakan menuju kasir, Terima kasih!")
    elif bayar == total_keseluruhan:
        print("-----------------------")
        print("Silakan menuju kasir, Terima kasih!")
    elif bayar < total_keseluruhan:
        print("-----------------------")
        print("Uang anda kurang, silakan periksa kembali!")

elif pilihan == 2:
    print("-----------------------")
    print("Silakan scan barcode dibawah ini!")


    