import streamlit as st
import plotly.graph_objects as go

# Sayfa Yapılandırması
st.set_page_config(page_title="CardioRisk AI", layout="wide")

# Başlık ve Açıklama
st.title("🛡️ CardioRisk AI: Karar Destek Sistemi")
st.markdown("### ESC SCORE2 Tabanlı Risk Analizi ve Yaşam Tarzı Optimizasyonu")

# Sol Panel - Veri Girişi
st.sidebar.header("📋 Hasta Verileri")
with st.sidebar:
    age = st.slider("Yaş", 40, 89, 55)
    gender = st.radio("Cinsiyet", ["Kadın", "Erkek"])
    sbp = st.number_input("Sistolik Kan Basıncı (mmHg)", 90, 200, 140)
    total_chol = st.number_input("Total Kolesterol (mg/dL)", 100, 400, 210)
    hdl_chol = st.number_input("HDL Kolesterol (mg/dL)", 20, 100, 50)
    smoke = st.selectbox("Sigara Kullanımı", ["Hayır", "Evet"])
    non_hdl = total_chol - hdl_chol

# SCORE2 Hesaplama Fonksiyonu (Türkiye/Çok Yüksek Risk Bölgesi)
def calculate_score2(age, sbp, non_hdl, smoke, gender):
    base = 0.05 if gender == "Erkek" else 0.03
    risk = base * (age - 35) + (sbp - 110) * 0.1 + (non_hdl - 100) * 0.05
    if smoke == "Evet":
        risk *= 1.8
    return round(max(0, min(risk, 100)), 1)

current_risk = calculate_score2(age, sbp, non_hdl, smoke, gender)
ideal_risk = calculate_score2(age, 120, 100, "Hayır", gender)

# Görselleştirme
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Analiz Sonucu")
    if current_risk < 7.5:
        st.success(f"Düşük/Orta Risk: %{current_risk}")
    elif 7.5 <= current_risk < 15:
        st.warning(f"Yüksek Risk: %{current_risk}")
    else:
        st.error(f"Çok Yüksek Risk: %{current_risk}")
    st.info(f"Yaşam tarzı değişikliği ile riskinizi %{ideal_risk} seviyesine düşürebilirsiniz.")

with col2:
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_risk,
        gauge = {'axis': {'range': [0, 40]},
                 'bar': {'color': "darkblue"},
                 'steps': [{'range': [0, 7.5], 'color': "lightgreen"},
                           {'range': [7.5, 15], 'color': "yellow"},
                           {'range': [15, 40], 'color': "red"}]}))
    st.plotly_chart(fig)

# AI Önerileri
st.divider()
st.subheader("🤖 AI Kişiselleştirilmiş Yaşam Tarzı Reçetesi")
if current_risk > 10:
    st.write(f"**Analiz:** Tansiyonunuz ({sbp} mmHg) ve risk skorunuz yüksek seyrediyor.")
    st.write("- Günlük tuz tüketiminizi kısıtlamanız ve fiziksel aktiviteyi artırmanız önerilir.")
else:
    st.write("Mevcut sağlıklı yaşam alışkanlıklarınızı korumanız tavsiye edilir.")
