# Analisis topologi full-mesh enam server sebagai complete graph K6.
''' 
Nama: Ivanka Bunga A
NIM: 251524105
Kelas: 2D D4

Tugas:
o	Modelkan ini sebagai Complete Graph (Kn) dan gambarkan.
o	Representasikan graf ini dalam Incidence Matrix.
o	Analisis graf: hitung derajat setiap simpul dan verifikasi Handshaking Theorem.
o	Jelaskan pengaruh kegagalan satu server pada connectivity graf.

'''

from itertools import combinations
from math import cos, pi, sin


JUMLAH_SERVER = 6
SERVER = [f"S{i}" for i in range(1, JUMLAH_SERVER + 1)]
SISI = list(combinations(SERVER, 2))

 
def buat_graf_full_mesh():
	# Membuat daftar sisi K6;  setiap pasangan server terhubung langsung.
	return SISI.copy()


def buat_matriks_insidensi(simpul, sisi):
	# Menghasilkan matriks insidensi dengan baris simpul dan kolom sisi.
	return [
		[int(simpul_server in sisi_server) for sisi_server in sisi]
		for simpul_server in simpul
	]


def hitung_derajat(simpul, sisi):
	# Menghitung derajat tiap simpul: jumlah sisi yang memuat simpul tsb.
	return {
		simpul_server: sum(simpul_server in sisi_server for sisi_server in sisi)
		for simpul_server in simpul
	}


def cek_konektivitas(simpul, sisi):
	''' Mengecek apakah graf (simpul, sisi) terhubung penuh lewat BFS, 
	bukan cuma diasumsikan dari bentuk topologinya.'''
	if not simpul:
		return True

	tetangga = {simpul_server: set() for simpul_server in simpul}
	for simpul_awal, simpul_akhir in sisi:
		tetangga[simpul_awal].add(simpul_akhir)
		tetangga[simpul_akhir].add(simpul_awal)

	awal = simpul[0]
	terkunjungi = {awal}
	antrean = [awal]
	while antrean:
		sekarang = antrean.pop(0)
		for tetangga_server in tetangga[sekarang]:
			if tetangga_server not in terkunjungi:
				terkunjungi.add(tetangga_server)
				antrean.append(tetangga_server)

	return terkunjungi == set(simpul)


def cetak_matriks_insidensi(simpul, sisi, matriks, lebar_kolom=4):
	''' Mencetak matriks insidensi dengan lebar kolom header & data yang sama,
	supaya angka tetap lurus di bawah label sisinya walau jumlah sisi banyak.'''
	label_simpul_width = max(len(s) for s in simpul) + 1
	label_sisi = [f"e{indeks:02d}" for indeks in range(1, len(sisi) + 1)]

	print(" " * label_simpul_width + "".join(l.rjust(lebar_kolom) for l in label_sisi))
	for simpul_server, baris in zip(simpul, matriks):
		nilai = "".join(str(v).rjust(lebar_kolom) for v in baris)
		print(f"{simpul_server:<{label_simpul_width}}{nilai}")


def gambar_graf(simpul, sisi, simpan_ke=None):
	# Menggambar graf pada bidang; analisis tetap dapat dijalankan tanpa matplotlib.
	try:
		import matplotlib.pyplot as plt
	except ImportError:
		print("Matplotlib tidak tersedia; gunakan daftar sisi sebagai gambar teks.")
		return

	sudut = [2 * pi * indeks / len(simpul) for indeks in range(len(simpul))]
	posisi = {
		simpul_server: (cos(sudut[indeks]), sin(sudut[indeks]))
		for indeks, simpul_server in enumerate(simpul)
	}

	fig, sumbu = plt.subplots(figsize=(7, 7))
	for simpul_awal, simpul_akhir in sisi:
		x_awal, y_awal = posisi[simpul_awal]
		x_akhir, y_akhir = posisi[simpul_akhir]
		sumbu.plot([x_awal, x_akhir], [y_awal, y_akhir], color="steelblue", zorder=1)

	sumbu.scatter(
		[posisi[simpul_server][0] for simpul_server in simpul],
		[posisi[simpul_server][1] for simpul_server in simpul],
		s=900,
		color="tomato",
		edgecolor="black",
		zorder=2,
	)
	for simpul_server, (x_posisi, y_posisi) in posisi.items():
		sumbu.text(x_posisi, y_posisi, simpul_server, ha="center", va="center", zorder=3)

	sumbu.set_title("Complete Graph K6 - Topologi Full-Mesh")
	sumbu.axis("equal")
	sumbu.axis("off")

	if simpan_ke:
		plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
	plt.show()


def main():
	sisi = buat_graf_full_mesh()
	matriks = buat_matriks_insidensi(SERVER, sisi)
	derajat = hitung_derajat(SERVER, sisi)
	jumlah_sisi = len(sisi)
	total_derajat = sum(derajat.values())

	print("=== COMPLETE GRAPH K6 / FULL-MESH ===")
	print(f"Simpul (server): {SERVER}")
	print(f"Jumlah sisi/koneksi: |E| = {jumlah_sisi} = 6(6 - 1)/2")
	print("Daftar koneksi:")
	print(", ".join(f"{awal}-{akhir}" for awal, akhir in sisi))

	print("\n=== MATRIKS INSIDENSI ===")
	print("Baris = simpul, kolom = sisi")
	cetak_matriks_insidensi(SERVER, sisi, matriks)

	print("\n=== ANALISIS DERAJAT ===")
	for simpul_server, nilai_derajat in derajat.items():
		print(f"deg({simpul_server}) = {nilai_derajat}")
	print(f"Total derajat = {total_derajat}")
	print(f"2|E| = 2 * {jumlah_sisi} = {2 * jumlah_sisi}")
	print(f"Handshaking Theorem terpenuhi: {total_derajat == 2 * jumlah_sisi}")

	print("\n=== DAMPAK KEGAGALAN SATU SERVER ===")
	server_gagal = SERVER[0]
	simpul_tersisa = [server for server in SERVER if server != server_gagal]
	sisi_tersisa = [sisi_server for sisi_server in sisi if server_gagal not in sisi_server]
	derajat_tersisa = hitung_derajat(simpul_tersisa, sisi_tersisa)
	tetap_terhubung = cek_konektivitas(simpul_tersisa, sisi_tersisa)

	print(f"Jika {server_gagal} gagal, {len(sisi) - len(sisi_tersisa)} koneksi ikut hilang.")
	print(f"Graf tersisa adalah K5 dengan {len(sisi_tersisa)} koneksi.")
	print(f"Derajat setiap server yang tersisa: {list(derajat_tersisa.values())}")
	print(f"Verifikasi BFS -- graf tersisa terhubung penuh: {tetap_terhubung}")
	print("Namun, server yang gagal tidak dapat diakses dan redundansi total berkurang.")

	gambar_graf(SERVER, sisi, simpan_ke="full_mesh_K6.png")


if __name__ == "__main__":
	main()