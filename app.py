import streamlit as st
from PIL import Image

# CONFIG
st.set_page_config(page_title="Assistente Pé Diabético", layout="centered")

# SIDEBAR STOCK
st.sidebar.title("📦 Stock disponível")

with st.sidebar.expander("🧸 Espumas"):
    polymem = st.checkbox("Polymem", True)
    mepilex = st.checkbox("Mepilex", True)
    mepilex_ag = st.checkbox("Mepilex AG", True)

with st.sidebar.expander("🧽 Desbridamento"):
    urgoclean = st.checkbox("Urgoclean", True)
    urgoclean_ag = st.checkbox("Urgoclean AG", True)

with st.sidebar.expander("🦠 Antimicrobianos"):
    mel = st.checkbox("Mel", True)
    inadine = st.checkbox("Inadine", False)
    iodosorb = st.checkbox("Iodosorb", False)
    silverderma = st.checkbox("Silverderma", True)

with st.sidebar.expander("🕳️ Cavidade"):
    cronocol = st.checkbox("Cronocol", True)

# UI
st.title("👣 Assistente Pé Diabético")

# 📸 UPLOAD DE IMAGEM
st.markdown("## 📸 Upload de Imagem")

imagem = st.file_uploader("Carregar imagem da ferida", type=["jpg", "png", "jpeg"])

if imagem:
    img = Image.open(imagem)
    st.image(img, caption="Imagem carregada", use_column_width=True)

    st.markdown("### 🔍 Sugestão baseada na imagem (assistida)")

    sugestao = st.selectbox(
        "O que predomina na imagem?",
        ["Selecionar", "Necrose", "Fibrina", "Granulação"]
    )

    if sugestao != "Selecionar":
        st.success(f"Sugestão inicial: {sugestao}")

# INPUTS
st.markdown("## 🧠 Dados Clínicos")

tecido = st.selectbox("Tecido", ["necrose", "fibrina", "granulação"])
exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
infeccao = st.selectbox("Infeção", ["não", "sim"])
cavidade = st.checkbox("Cavidade")
vascular = st.checkbox("Compromisso vascular")

st.markdown("---")

# BOTÃO
if st.button("🧠 Gerar Plano"):

    st.markdown("## 🥇 Plano Principal")

    plano = []

    if tecido == "fibrina":
        if urgoclean:
            plano.append("Urgoclean")
            plano.append("+ gota de hidrogel")

    elif tecido == "granulação":
        if polymem:
            plano.append("Polymem")

    elif tecido == "necrose":
        plano.append("Desbridamento")

    if infeccao == "sim":
        if mepilex_ag:
            plano.append("Mepilex AG")
        elif mel:
            plano.append("Mel")

    if cavidade and cronocol:
        plano.append("Cronocol")

    for p in plano:
        st.write(f"• {p}")

    st.markdown("---")

    st.markdown("## ⚠️ Alertas")

    if vascular and tecido == "fibrina":
        st.warning("Evitar hidrogel isolado")

    if infeccao == "sim" and cavidade:
        st.warning("Vigiar encerramento precoce")

    st.markdown("---")
    st.markdown("## 👣 Descarga")
    st.write("• Calçado tipo Baruk")
    st.write("• Feltro de descarga")
