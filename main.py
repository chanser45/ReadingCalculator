import streamlit as st
import datetime
import json
import os

# Kullanıcı ID'si (şimdilik manuel)
user_id = st.text_input("Kullanıcı ID'nizi girin", "guest")
data_path = f"data/{user_id}.json"

# Kullanıcı verilerini yükle
if os.path.exists(data_path):
    with open(data_path, "r") as f:
        user_data = json.load(f)
else:
    user_data = {"log": {}}

# Bugünün tarihi
bugun = str(datetime.date.today())
sayfa_sayisi = st.number_input("Bugün kaç sayfa okudun?", min_value=0, step=1)

tamam = st.button("Kaydet")
if tamam:
    user_data["log"][bugun] = user_data["log"].get(bugun, 0) + sayfa_sayisi
    with open(data_path, "w") as f:
        json.dump(user_data, f)
    st.success(f"{bugun} günü için {sayfa_sayisi} sayfa eklendi!")

# Toplam sayfa hesaplama
okuma_logu = user_data.get("log", {})
toplam_sayfa = sum(okuma_logu.values())

days_active = len(okuma_logu)
ortalama_gunluk = toplam_sayfa / days_active if days_active > 0 else 0

tahmini_yillik = ortalama_gunluk * 365
kitap_boyu = 300  # Ortalama kitap boyu
kitap_yillik = tahmini_yillik / kitap_boyu

st.header("📊 Okuma İstatistiklerin")
st.write(f"Toplam okuduğun sayfa: **{toplam_sayfa}**")
st.write(f"Günlük ortalaman: **{ortalama_gunluk:.2f}** sayfa")
st.write(f"Bu tempoyla yılda yaklaşık **{int(tahmini_yillik)}** sayfa, yani **{kitap_yillik:.1f}** kitap okursun.")

# Dünya ortalaması kıyası
# (örnek değer: dünya ortalaması yılda 12 kitap diyelim)
dunya_ortalama_kitap = 12
karsilastirma_orani = kitap_yillik / dunya_ortalama_kitap * 100
st.write(f"Bu tempoyla dünya ortalamasından **%{karsilastirma_orani:.1f}** daha fazla okuyorsun!")

# Motivasyon Mesajı
if kitap_yillik >= 20:
    st.success("Harika bir temposun var, bu şekilde devam edersen yılda 20'den fazla kitap bitirirsin!")
elif kitap_yillik >= 10:
    st.info("İyi gidiyorsun! Bu yıl en az 10 kitap bitireceksin gibi görünüyor.")
else:
    st.warning("Şu an düşük bir tempo, ama her sayfa bir ilerlemedir. Hadi biraz daha! 💪")
