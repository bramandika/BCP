import streamlit as st
import random
from collections import defaultdict

# List semua nama peserta
nama_orang = [
    "Kezia Angel Tjhen",
    "Timoteis Maychael Valentino",
    "Jessica Yolanda Claudya",
    "Jessica Yoan Novelly",
    "Stephanie Elsyia",
    "Debora Sry Yellisyana Agustina",
    "Rut Anggita Theresia Imanuela S",
    "Abigail Carlene Elaine Affendi",
    "Samuel Christian Sianga",
    "Yohanes Darmawan",
    "Titus Theofilos Zhuliano Suitela",
    "Lukas Ofier Jezreelius Ricardo",
    "Daniel Mikhael Pranata",
    "Maria Berliana Evitani Panjaitan",
    "Dea Lidea Theresia Chrisutomo",
    "Maria Gabriella Verdony",
    "Kezia Alfani Yesti Gulo",
    "Timotius Christofer Prihadmoko",
    "Yohana Chelya Verdeeya Gabriela",
    "Gideon Bramandika",
    "Rut Cornellia Naomi Maribet Siahaan",
    "Nathan Daniel A",
    "Kezia Carissa Eliani",
    "Ester Aliana Abigail Wibowo",
    "Maria Natalie Margareta Elysabet",
    "Rachel Amabelle",
    "Hanna Veronica Nathalia",
    "Misael Steyo Dewantoro",
    "Elia Christophorus Natanel A P W S",
    "Achazia Ziselll Malobu"
]

st.title("Aplikasi Bagi sesi")

st.subheader("Pilih 2 Leader untuk Setiap Sesi")
leader_sesi = {}
for sesi in range(1, 7):
    leaders = st.multiselect(f"Leader Sesi {sesi} (Pilih 2 orang)", options=nama_orang, key=f"leader_{sesi}", max_selections=2)
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

    # Masukkan leader dulu
    for sesi, leaders in leader_sesi.items():
        for leader in leaders:
            jadwal_sesi[sesi].append(leader)
            jadwal_peserta[leader].append(sesi)

    # Penentuan sesi per orang
    if jumlah_hadir <= 8:
        sesi_per_orang = 6
    elif jumlah_hadir <= 11:
        sesi_per_orang = 5
    else:
        sesi_per_orang = 4

    total_slot = jumlah_hadir * sesi_per_orang
    peserta_per_sesi = total_slot // 6
    sisa_slot = total_slot % 6  # sesi yang butuh 1 orang tambahan

    st.info(f"{jumlah_hadir} peserta hadir → target: {sesi_per_orang} sesi per orang.")
    st.info(f"Setiap sesi targetnya sekitar {peserta_per_sesi} orang. {sisa_slot} sesi akan ditambah 1 orang.")

    # Hitung kapasitas maksimum tiap sesi
    kapasitas_sesi = {sesi: peserta_per_sesi for sesi in range(1, 7)}
    for i in range(1, 7):
        if sisa_slot > 0:
            kapasitas_sesi[i] += 1
            sisa_slot -= 1

    sesi_isi = {sesi: len(jadwal_sesi[sesi]) for sesi in range(1, 7)}

    # Penjadwalan peserta biasa
    random.shuffle(peserta_biasa)
    for peserta in peserta_biasa:
        available_sessions = [s for s in range(1, 7) if s not in jadwal_peserta[peserta] and sesi_isi[s] < kapasitas_sesi[s]]
        random.shuffle(available_sessions)
        
        for sesi in available_sessions:
            if len(jadwal_peserta[peserta]) < sesi_per_orang:
                jadwal_sesi[sesi].append(peserta)
                jadwal_peserta[peserta].append(sesi)
                sesi_isi[sesi] += 1

        if len(jadwal_peserta[peserta]) < sesi_per_orang:
            st.warning(f"⚠️ {peserta} hanya dapat {len(jadwal_peserta[peserta])} sesi!")

    st.subheader("Hasil Pembagian Sesi:")
    for sesi in sorted(jadwal_sesi):
        st.markdown(f"**Sesi {sesi} ({len(jadwal_sesi[sesi])} peserta)**")
        st.write(sorted(jadwal_sesi[sesi]))

    st.subheader("Rangkuman Per Peserta:")
    for peserta in sorted(jadwal_peserta):
        st.write(f"{peserta}: sesi {sorted(jadwal_peserta[peserta])}")
