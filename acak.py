import streamlit as st
import random
from collections import defaultdict

# List semua nama peserta
nama_orang = [
    "Kezia Angel Tjhen", "Timoteis Maychael Valentino", "Jessica Yolanda Claudya",
    "Jessica Yoan Novelly", "Stephanie Elsyia", "Debora Sry Yellisyana Agustina",
    "Rut Anggita Theresia Imanuela S", "Abigail Carlene Elaine Affendi",
    "Samuel Christian Sianga", "Yohanes Darmawan", "Titus Theofilos Zhuliano Suitela",
    "Lukas Ofier Jezreelius Ricardo", "Daniel Mikhael Pranata",
    "Maria Berliana Evitani Panjaitan", "Dea Lidea Theresia Chrisutomo",
    "Maria Gabriella Verdony", "Kezia Alfani Yesti Gulo", "Timotius Christofer Prihadmoko",
    "Yohana Chelya Verdeeya Gabriela", "Gideon Bramandika", "Rut Cornellia Naomi Maribet Siahaan",
    "Nathan Daniel A", "Kezia Carissa Eliani", "Ester Aliana Abigail Wibowo",
    "Maria Natalie Margareta Elysabet", "Rachel Amabelle", "Hanna Veronica Nathalia",
    "Misael Steyo Dewantoro", "Elia Christophorus Natanel A P W S", "Achazia Ziselll Malobu"
]

st.title("Aplikasi Bagi Sesi Choir")

# Checkbox untuk perbantuan
perbantuan = st.checkbox("Perbantuan Aktif?")

st.subheader("Pilih 2 Leader untuk Setiap Sesi")
leader_sesi = {}
for sesi in range(1, 7):
    leaders = st.multiselect(
        f"Leader Sesi {sesi} (Pilih 2 orang)",
        options=nama_orang,
        key=f"leader_{sesi}",
        max_selections=2
    )
    leader_sesi[sesi] = leaders

st.subheader("Pilih Peserta yang Tidak Hadir")
tidak_hadir = st.multiselect("Pilih peserta yang tidak hadir:", options=nama_orang)

if st.button("Generate Sesi"):
    peserta_hadir = [nama for nama in nama_orang if nama not in tidak_hadir]
    jumlah_hadir = len(peserta_hadir)

    # Validasi leader
    for sesi, leaders in leader_sesi.items():
        for leader in leaders:
            if leader in tidak_hadir:
                st.error(f"Leader '{leader}' di sesi {sesi} tidak hadir!")
                st.stop()

    semua_leader = [l for lst in leader_sesi.values() for l in lst]
    peserta_biasa = [p for p in peserta_hadir if p not in semua_leader]

    # Inisialisasi struktur sesi
    jadwal_sesi = defaultdict(list)
    jadwal_peserta = defaultdict(list)

    # Tambahkan leader ke sesi yang mereka pimpin
    for sesi, leaders in leader_sesi.items():
        for leader in leaders:
            jadwal_sesi[sesi].append(leader)
            jadwal_peserta[leader].append(sesi)

    if perbantuan:
        st.info("📌 Perbantuan aktif: Semua peserta wajib sesi 1 & 2, lalu 3 sesi tambahan dari sesi 3–6")

        # Semua peserta (termasuk leader) masuk sesi 1 & 2
        for peserta in peserta_hadir:
            for sesi in [1, 2]:
                if sesi not in jadwal_peserta[peserta]:
                    jadwal_sesi[sesi].append(peserta)
                    jadwal_peserta[peserta].append(sesi)

        # Semua peserta tambahkan 3 sesi acak dari 3–6
        for peserta in peserta_hadir:
            sesi_opsi = [s for s in [3, 4, 5, 6] if s not in jadwal_peserta[peserta]]
            random.shuffle(sesi_opsi)
            for sesi in sesi_opsi:
                if len(jadwal_peserta[peserta]) < 5:
                    jadwal_sesi[sesi].append(peserta)
                    jadwal_peserta[peserta].append(sesi)

            if len(jadwal_peserta[peserta]) < 5:
                st.warning(f"⚠️ {peserta} hanya dapat {len(jadwal_peserta[peserta])} sesi!")

    else:
        st.info("📌 Tanpa perbantuan: Peserta ikut 3 sesi dari pola 1-3-5 atau 2-4-6")

        pola1 = [1, 3, 5]
        pola2 = [2, 4, 6]

        for peserta in peserta_hadir:
            # Abaikan sesi yang sudah dia punya (mungkin karena dia leader)
            sesi_yang_sudah_diikuti = jadwal_peserta[peserta]
            sesi_kurang = 3 - len(sesi_yang_sudah_diikuti)

            if sesi_kurang > 0:
                pola = random.choice([pola1, pola2])
                opsi_sesi = [s for s in pola if s not in sesi_yang_sudah_diikuti]
                random.shuffle(opsi_sesi)

                for sesi in opsi_sesi:
                    if len(jadwal_peserta[peserta]) < 3:
                        jadwal_sesi[sesi].append(peserta)
                        jadwal_peserta[peserta].append(sesi)

            if len(jadwal_peserta[peserta]) < 3:
                st.warning(f"⚠️ {peserta} hanya dapat {len(jadwal_peserta[peserta])} sesi!")


    # Tampilkan hasil
    st.subheader("📋 Hasil Pembagian Sesi")
    for sesi in sorted(jadwal_sesi):
        st.markdown(f"**Sesi {sesi} ({len(jadwal_sesi[sesi])} peserta)**")
        st.write(sorted(jadwal_sesi[sesi]))

    st.subheader("👤 Rangkuman Per Peserta")
    for peserta in sorted(jadwal_peserta):
        st.write(f"{peserta}: sesi {sorted(jadwal_peserta[peserta])}")
