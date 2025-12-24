import streamlit as st
import pandas as pd

st.set_page_config(page_title="CardioRisk AI", layout="wide")
st.title("🛡️ CardioRisk AI: Karar Destek Sistemi")

# GİRİŞ PANELİ
st.sidebar.header("📋 Hasta Verileri")
age = st.sidebar.slider("Yaş", 40, 89, 55)
sbp = st.sidebar.number_input("Sistolik Kan Basıncı (mmHg)", 90, 200, 140)
total_chol = st.sidebar.number_input("Total Kolesterol (mg/dL)", 100, 400, 210)
hdl_chol = st.sidebar.number_input("HDL Kolesterol (mg/dL)", 20, 100, 50)
smoke = st.sidebar.selectbox("Sigara Kullanımı", ["Hayır", "Evet"])

# SCORE2 MANTIĞI (Basitleştirilmiş)
# Matematiksel Model: $Risk = \beta_0 + \beta_1(Age) + \beta_2(SBP) + \beta_3(NonHDL)$
non_hdl = total_chol - hdl_chol
risk = (age - 35) * 0.2 + (sbp - 110) * 0.1 + (non_hdl - 100) * 0.05
if smoke == "Evet": risk *= 1.8
current_risk = round(max(0, min(risk, 100)), 1)

# SONUÇ EKRANI
st.subheader(f"📊 10 Yıllık KV Olay Riski: %{current_risk}")

# Basit Renkli Bar Grafiği (Plotly Gerektirmez)
chart_data = pd.DataFrame([current_risk], columns=["Mevcut Risk Oranı"])
st.bar_chart(chart_data)

if current_risk >= 15:
    st.error("Çok Yüksek Risk Kategorisindesiniz.")
elif current_risk >= 7.5:
    st.warning("Yüksek Risk Kategorisindesiniz.")
else:
    st.success("Düşük/Orta Risk Kategorisindesiniz.")

st.divider()
st.info("💡 AI Tavsiyesi: Sigarayı bırakmak ve tansiyonu 120 mmHg altına çekmek riskinizi yarı yarıya düşürebilir.")
