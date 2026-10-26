"""
Task 04 - Alur Komando dalam Dinamika Demonstrasi
Nama: Ivanka Bunga A
NIM: 251524105
Kelas: 2D D4

Contoh akademik graf berarah komunikasi dan koordinasi saat demonstrasi.
Model ini menyederhanakan kenyataan: jalur komunikasi dan kewenangan dapat
berbeda menurut situasi, aturan, dan wilayah. Sisi menunjukkan pesan/koordinasi
yang dimodelkan, bukan otomatis hubungan komando atau kewenangan hukum.
"""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import networkx as nx


# Simpul mewakili peran, bukan orang atau institusi tertentu.
SIMPUL = (
    "Juru bicara mahasiswa",
    "Koordinator lapangan mahasiswa",
    "Peserta aksi",
    "Negosiator kepolisian",
    "Kepala kepolisian",
    "Komandan TNI",
    "Pejabat penghubung pemerintah",
    "Provokator/penyusup (hipotetis)",
)

# Sisi (A, B) berarti A menyampaikan informasi/koordinasi kepada B.
# Dua sisi berlawanan hanya dicantumkan jika model mengasumsikan komunikasi
# berlangsung pada kedua arah. Tidak semua hubungan bersifat timbal balik.
SISI = [
    ("Juru bicara mahasiswa", "Koordinator lapangan mahasiswa"),
    ("Koordinator lapangan mahasiswa", "Peserta aksi"),
    ("Juru bicara mahasiswa", "Negosiator kepolisian"),
    ("Negosiator kepolisian", "Juru bicara mahasiswa"),
    ("Kepala kepolisian", "Negosiator kepolisian"),
    ("Pejabat penghubung pemerintah", "Kepala kepolisian"),
    ("Pejabat penghubung pemerintah", "Komandan TNI"),
    ("Provokator/penyusup (hipotetis)", "Peserta aksi"),
    ("Provokator/penyusup (hipotetis)", "Koordinator lapangan mahasiswa"),
]


def simpan_graf_scc(graf, komponen, lokasi):
    """Menggambar graf terarah dengan warna berbeda untuk setiap SCC."""
    posisi = {
        "Pejabat penghubung pemerintah": (0, 4),
        "Kepala kepolisian": (3, 4),
        "Komandan TNI": (6, 4),
        "Juru bicara mahasiswa": (3, 2),
        "Negosiator kepolisian": (6, 2),
        "Provokator/penyusup (hipotetis)": (0, 0),
        "Koordinator lapangan mahasiswa": (3, 0),
        "Peserta aksi": (6, 0),
    }
    warna = (
        "#bfdbfe", "#fed7aa", "#e9d5ff", "#bbf7d0",
        "#fecaca", "#fbcfe8", "#bae6fd", "#e5e7eb",
    )
    nomor_scc = {
        simpul: nomor
        for nomor, anggota in enumerate(komponen, start=1)
        for simpul in anggota
    }
    label = {
        simpul: f"SCC {nomor_scc[simpul]}\n{textwrap.fill(simpul, width=17)}"
        for simpul in graf.nodes
    }

    plt.figure(figsize=(16, 10))
    nx.draw_networkx_edges(
        graf,
        posisi,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=30,
        width=1.8,
        edge_color="#344054",
        connectionstyle="arc3,rad=0.12",
        min_source_margin=65,
        min_target_margin=65,
    )
    nx.draw_networkx_nodes(
        graf,
        posisi,
        node_color=[warna[(nomor_scc[simpul] - 1) % len(warna)] for simpul in graf.nodes],
        node_size=12000,
        node_shape="s",
        edgecolors="#344054",
        linewidths=1.5,
    )
    nx.draw_networkx_labels(
        graf,
        posisi,
        labels=label,
        font_size=9,
        font_weight="bold",
    )
    plt.title("Strongly Connected Components (SCC)", fontsize=17, pad=18)
    plt.text(
        0.5,
        0.01,
        "Warna sama = anggota SCC yang sama. Panah menunjukkan arah informasi/koordinasi.",
        ha="center",
        transform=plt.gca().transAxes,
        fontsize=10,
    )
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(lokasi, dpi=200, bbox_inches="tight")
    plt.close()


def main():
    graf = nx.DiGraph()
    graf.add_nodes_from(SIMPUL)
    graf.add_edges_from(SISI)

    print("Simpul:")
    for simpul in sorted(SIMPUL):
        print(f"  - {simpul}")

    print("\nSisi berarah (pengirim -> penerima):")
    for asal, tujuan in SISI:
        print(f"  {asal} -> {tujuan}")

    print(
        f"\nTerhubung lemah: "
        f"{'Ya' if nx.is_weakly_connected(graf) else 'Tidak'}"
    )

    # Peserta aksi merupakan simpul tujuan saja dalam contoh ini. Tidak ada
    # jalur berarah dari peserta kembali ke juru bicara atau ke institusi lain.
    awal = "Peserta aksi"
    tercapai = nx.descendants(graf, awal) | {awal}
    terputus = sorted(set(graf.nodes) - tercapai)
    print(f"\nDari {awal!r}, simpul yang dapat dicapai: {sorted(tercapai)}")
    print(f"Jalur berarah yang terputus dari {awal!r}: {terputus}")
    print(
        f"Terhubung kuat: {'Ya' if nx.is_strongly_connected(graf) else 'Tidak'}"
    )

    print("\nStrongly Connected Components (SCC):")
    komponen = list(nx.strongly_connected_components(graf))
    for nomor, anggota in enumerate(komponen, start=1):
        print(f"  SCC {nomor}: {sorted(anggota)}")

    lokasi_gambar = Path(__file__).with_name("graf_scc_demonstrasi.png")
    simpan_graf_scc(graf, komponen, lokasi_gambar)
    print(f"\nGambar graf SCC disimpan di: {lokasi_gambar}")

    print(
        "\nMakna dalam konteks: anggota SCC saling dapat mencapai melalui jalur "
        "komunikasi berarah. Pada model ini juru bicara mahasiswa dan negosiator "
        "kepolisian membentuk SCC karena kanal negosiasi dimodelkan dua arah. "
        "Simpul lain menjadi SCC tunggal: informasi atau koordinasi di antaranya "
        "tidak membentuk putaran yang memungkinkan semua pihak saling mencapai."
    )
    print(
        "\nCatatan: simpul provokator/penyusup hanya skenario hipotetis untuk "
        "menganalisis arus informasi; keberadaannya tidak diasumsikan sebagai fakta."
    )


if __name__ == "__main__":
    main()