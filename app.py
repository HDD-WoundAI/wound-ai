import streamlit as st
from PIL import Image
import base64
import io
from openai import OpenAI

# CONFIG
st.set_page_config(page_title="Assistente Pé Diabético", layout="centered")

# OPENAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ========================
# SESSION STATE
# ========================
if "ia_resultado" not in st.session_state:
    st.session_state.ia_resultado = None

if "tecido_detectado" not in st.session_state:
    st.session_state.tecido_detectado = None

if "exsudado_detectado" not in st.session_state:
    st.session_state.exsudado_detectado = None

# ========================
# 📦 SIDEBAR STOCK COMPLETO
# ========================
st.sidebar.title("📦 Stock disponível")

with st.sidebar.expander("🧼 Limpeza"):
    prontosan = st.checkbox("Prontosan", True)
    granudacyn = st.checkbox("Granudacyn", True)
    betadine = st.checkbox("Betadine solução", True)

with st.sidebar.expander("🧽 Desbridamento / Fibrina"):
    urgoclean = st.checkbox("Urgoclean", True)
    urgoclean_ag = st.checkbox("Urgoclean AG", True)
    flaminal = st.checkbox("Flaminal Hydro", True)
    askina = st.checkbox("Askina gel", True)
    ulcerase = st.checkbox("Ulcerase", True)

with st.sidebar.expander("🍯 Antimicrobianos / Mel / Iodo"):
    mel = st.checkbox("Mel (L-Mesitran / Actilite)", True)
    inadine = st.checkbox("Inadine", False)
    iodosorb = st.checkbox("Iodosorb", False)
    silverderma = st.checkbox("Silverderma", True)
    nadiclox = st.checkbox("Nadiclox (fusidato)", True)

with st.sidebar.expander("🧸 Espumas / Absorção"):
    polymem = st.checkbox("Polymem", True)
    mepilex = st.checkbox("Mepilex", True)
    mepilex_ag = st.checkbox("Mepilex AG", True)
    aquacel = st.checkbox("Aquacel", False)
    aquacel_ag = st.checkbox("Aquacel AG", False)

with st.sidebar.expander("🕳️ Cavidade"):
    cronocol = st.checkbox("Cronocol", True)
    tulle_mel = st.checkbox("Tulle com mel", True)

# ========================
# UI
# ========================
st.title("👣 Assistente Pé Diabético")

# ========================
# 📸 IMAGEM + IA
# ========================
imagem = st.file_uploader("Carregar imagem", type=["jpg", "png", "jpeg"])

if imagem:
    img = Image.open(imagem)
    img.thumbnail((800, 800))

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=70)
    bytes_data = buffer.getvalue()

    st.image(img, use_column_width=True)

    if st.button("🔍 Analisar com IA"):

        base64_image = base64.b64encode(bytes_data).decode("utf-8")

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Identifica tecido (necrose, fibrina, granulação) e exsudado (baixo, moderado, alto)."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        ],
                    }
                ],
            )

            resultado = response.choices[0].message.content.lower()
            st.session_state.ia_resultado = resultado

            if "necrose" in resultado:
                st.session_state.tecido_detectado = "necrose"
            elif "fibrina" in resultado:
                st.session_state.tecido_detectado = "fibrina"
            elif "granulação" in resultado:
                st.session_state.tecido_detectado = "granulação"

            if "alto" in resultado:
                st.session_state.exsudado_detectado = "alto"
            elif "moderado" in resultado:
                st.session_state.exsudado_detectado = "moderado"
            elif "baixo" in resultado:
                st.session_state.exsudado_detectado = "baixo"

            st.success(resultado)

        except:
            st.warning("IA indisponível")

# ========================
# INPUTS
# ========================
st.markdown("## 🧠 Dados Clínicos")

tecido_opcoes = ["não determinado", "necrose", "fibrina", "granulação"]
tecido = st.selectbox("Tecido predominante", tecido_opcoes)

exsudado_opcoes = ["não determinado", "baixo", "moderado", "alto"]
exsudado = st.selectbox("Exsudado", exsudado_opcoes)

infeccao = st.selectbox("Infeção", ["não", "sim", "não determinado"])
cavidade = st.checkbox("Cavidade")

# ========================
# VASCULAR + IPTB
# ========================
st.markdown("## 🩸 Compromisso Vascular")

vascular = st.checkbox("Compromisso vascular conhecido")

iptb = None

if not vascular:
    pulsos = st.selectbox("Pulsos", ["não determinado", "sim", "não"])
    braquial = st.number_input("Pressão braquial")
    tibial = st.number_input("Pressão tibial")

    if braquial > 0 and tibial > 0:
        iptb = tibial / braquial

    if iptb:
        if iptb > 1.4:
            st.info(f"🔵 IPTB {iptb:.2f} → Calcificação")
        elif 0.9 <= iptb <= 1.3:
            st.success(f"🟢 IPTB {iptb:.2f} → Normal")
        elif 0.7 <= iptb < 0.9:
            st.warning(f"🟡 IPTB {iptb:.2f} → Obstrução ligeira")
        elif 0.4 <= iptb < 0.7:
            st.warning(f"🟠 IPTB {iptb:.2f} → Obstrução moderada")
        else:
            st.error(f"🔴 IPTB {iptb:.2f} → Isquemia grave")

# ========================
# DECISÃO FINAL
# ========================
st.markdown("---")

if st.button("🧠 Gerar Plano"):

    st.markdown("## 🥇 Plano")

    plano = []

    # FIBRINA
    if tecido == "fibrina":
        if urgoclean:
            plano.append("Urgoclean + hidrogel")
        elif mel:
            plano.append("Mel")

    # NECROSE
    if tecido == "necrose":
        plano.append("Desbridamento")

    # GRANULAÇÃO
    if tecido == "granulação":
        if polymem:
            plano.append("Polymem")
        else:
            plano.append("Espuma")

    # INFEÇÃO
    if infeccao == "sim":
        if mepilex_ag:
            plano.append("Mepilex AG")
        elif mel:
            plano.append("Mel")

    # CAVIDADE
    if cavidade:
        if cronocol:
            plano.append("Cronocol")
        elif tulle_mel:
            plano.append("Tulle com mel")

    # TPN
    if exsudado == "alto" and not vascular and tecido != "necrose":
        plano.append("TPN (100 mmHg)")

    for p in plano:
        st.write(f"• {p}")

    # ALERTAS
    st.markdown("## ⚠️ Alertas")

    if iptb and iptb < 0.5:
        st.error("Isquemia crítica")

    if exsudado == "alto":
        st.warning("Risco de maceração")

    st.warning("Confirmar descarga")

    # DESCARGA
    st.markdown("## 👣 Descarga")
    st.write("• Baruk")
    st.write("• Feltro de descarga")
