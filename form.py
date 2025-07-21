import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# --- Firebase Initialization ---
try:
    cred = credentials.Certificate(st.secrets["firebase"])
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    st.error(f"Error initializing Firebase: {e}")
    st.stop()


st.set_page_config(page_title="Event Kayıt", layout="centered")

st.title("Event Kayıt Formu")

# Session state'i misafir sayısı için initialize et
if 'guest_count' not in st.session_state:
    st.session_state.guest_count = 0
if 'misafir_durumu_onceki' not in st.session_state:
    st.session_state.misafir_durumu_onceki = "Hayır"


# --- Form Alanları ---

isim_soyisim = st.text_input("İsim Soyisim *")

st.write("Telefon Numarası *")
col1, col2 = st.columns([0.2, 0.8])
with col1:
    ulke_kodu = st.text_input("Ülke Kodu", value="+90", label_visibility="collapsed")
with col2:
    telefon_numarasi = st.text_input(
        " ",
        max_chars=10,
        placeholder="5XX XXX XX XX",
        label_visibility="collapsed"
    )

darka_uye = st.radio(
    "Darka Spor Kulübü Üyesi misiniz? *",
    ("Evet", "Hayır"),
    horizontal=True,
    index=None
)

misafir_var_mi = st.radio(
    "Evente Misafir/Çocuklarınızla mı katılıyorsunuz? *",
    ("Evet", "Hayır"),
    horizontal=True,
    index=1  # Default "Hayır"
)

# Kullanıcı seçimi "Evet"'ten "Hayır"'a değiştirdiğinde misafir verilerini temizle
if misafir_var_mi == "Hayır" and st.session_state.misafir_durumu_onceki == "Evet":
    # Önce mevcut misafir anahtarlarını sil
    for i in range(st.session_state.guest_count):
        guest_key = f"guest_{i}"
        if guest_key in st.session_state:
            del st.session_state[guest_key]
    # Sonra misafir sayısını sıfırla
    st.session_state.guest_count = 0

# Mevcut durumu bir sonraki çalıştırma için kaydet
st.session_state.misafir_durumu_onceki = misafir_var_mi


if misafir_var_mi == "Evet":
    st.subheader("Misafir/Çocuk Bilgileri")

    col1, col2, _ = st.columns([0.15, 0.15, 0.7])
    with col1:
        if st.button("➕ Ekle", use_container_width=True):
            st.session_state.guest_count += 1
    with col2:
        if st.button("➖ Sil", use_container_width=True, disabled=st.session_state.guest_count == 0):
            # En son misafir için state'i temizle
            if f'guest_{st.session_state.guest_count - 1}' in st.session_state:
                del st.session_state[f'guest_{st.session_state.guest_count - 1}']
            if st.session_state.guest_count > 0:
                st.session_state.guest_count -= 1


    for i in range(st.session_state.guest_count):
        st.text_input(
            f"Misafir {i+1} İsim Soyisim",
            key=f"guest_{i}"
        )

st.markdown("---")
submit_button = st.button("Kaydı Tamamla")

if submit_button:
    # Gerekli alanların kontrolü
    if not isim_soyisim or not telefon_numarasi or not darka_uye or not misafir_var_mi:
        st.error("Lütfen yıldız (*) ile işaretli tüm zorunlu alanları doldurun.")
    elif len(telefon_numarasi) != 10 or not telefon_numarasi.isdigit():
        st.error("Lütfen geçerli bir telefon numarası girin (10 haneli, rakamlardan oluşmalı, başında 0 olmadan).")
    else:
        # Misafir isimlerini topla
        guest_list = []
        if misafir_var_mi == "Evet":
            for i in range(st.session_state.guest_count):
                guest_name = st.session_state.get(f"guest_{i}", "").strip()
                if guest_name:
                    guest_list.append(guest_name)

        # Verileri hazırla (küçük harf, alt çizgi ve zaman damgası ile)
        registration_data = {
            "isim_soyisim": isim_soyisim.lower(),
            "telefon_numarasi": f"{ulke_kodu}{telefon_numarasi}",
            "darka_uyesi": darka_uye.lower(),
            "misafir_durumu": misafir_var_mi.lower(),
            "misafirler": [guest.lower() for guest in guest_list],
            "kayit_tarihi": firestore.SERVER_TIMESTAMP
        }

        try:
            # Verileri Firestore'a gönder
            participants_ref = db.collection('event_participants')
            participants_ref.add(registration_data)
            st.success("Kaydınız başarıyla tamamlandı ve veritabanına eklendi!")
            st.balloons()
        except Exception as e:
            st.error(f"Veritabanına kaydederken bir hata oluştu: {e}")

        st.json(registration_data)
