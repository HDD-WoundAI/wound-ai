import streamlit as st
from PIL import Image
import base64
import io
from openai import OpenAI

# CONFIG
st.set_page_config(page_title="Assistente Pé Diabético", layout="centered")

# OPENAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# SESSION STATE
if "ia_resultado" not in st.session_state:
    st.session_state.ia_resultado = None

if "tecido_detectado" not in st.session_state:
    st.session_state.tecido_detectado = None

if "exsudado_detectado" not in st.session_state:
    st.session_state.exsudado_detectado = None

# ========================
# 📸 IMAGEM
# ========================
st.title("👣 Assistente Pé Diabético")

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

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Identifica tecido (necrose, fibrina, granulação) e exsudado (baixo, moderado, alto)."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        },
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

# ========================
# 🧠 INPUTS
# ========================
st.markdown("## 🧠 Dados Clínicos")

tecido_opcoes = ["não determinado", "necrose", "fibrina", "granulação"]

tecido = st.selectbox(
    "Tecido predominante",
    tecido_opcoes,
    index=tecido_opcoes.index(st.session_state.tecido_detectado)
    if st.session_state.tecido_detectado in tecido_opcoes else 0
)

exsudado_opcoes = ["não determinado", "baixo", "moderado", "alto"]

exsudado = st.selectbox(
    "Exsudado",
    exsudado_opcoes,
    index=exsudado_opcoes.index(st.session_state.exsudado_detectado)
    if st.session_state.exsudado_detectado in exsudado_opcoes else 0
)

infeccao = st.selectbox("Infeção", ["não", "sim", "não determinado"])
cavidade = st.checkbox("Cavidade")

# ========================
# 🩸 VASCULAR + IPTB
# ========================
st.markdown("## 🩸 Compromisso Vascular")

vascular = st.checkbox("Compromisso vascular conhecido")

iptb = None

if not vascular:
    pulsos = st.selectbox("Pulsos", ["não determinado", "sim", "não"])

    iptb_direto = st.number_input("IPTB direto", value=0.0)

    st.markdown("### Ou calcular IPTB")

    braquial = st.number_input("Pressão braquial")
    tibial = st.number_input("Pressão tibial")

    if braquial > 0 and tibial > 0:
        iptb = tibial / braquial

    elif iptb_direto > 0:
        iptb = iptb_direto

    # ========================
    # IPTB COLORIDO
    # ========================
    if iptb:
        st.markdown("### 📊 IPTB")

        if iptb > 1.4:
            st.markdown(f"<div style='background-color:#4da6ff;padding:10px;border-radius:8px'>🔵 IPTB: {iptb:.2f} → Calcificação arterial / vasos não compressíveis</div>", unsafe_allow_html=True)

        elif 0.9 <= iptb <= 1.3:
            st.markdown(f"<div style='background-color:#70db70;padding:10px;border-radius:8px'>🟢 IPTB: {iptb:.2f} → Normal</div>", unsafe_allow_html=True)

        elif 0.7 <= iptb < 0.9:
            st.markdown(f"<div style='background-color:#ffff66;padding:10px;border-radius:8px'>🟡 IPTB: {iptb:.2f} → Obstrução ligeira</div>", unsafe_allow_html=True)

        elif 0.4 <= iptb < 0.7:
            st.markdown(f"<div style='background-color:#ff9933;padding:10px;border-radius:8px'>🟠 IPTB: {iptb:.2f} → Obstrução moderada</div>", unsafe_allow_html=True)

        elif iptb < 0.4:
            st.markdown(f"<div style='background-color:#ff4d4d;padding:10px;border-radius:8px'>🔴 IPTB: {iptb:.2f} → Isquemia grave</div>", unsafe_allow_html=True)

# ========================
# DECISÃO
# ========================
st.markdown("---")

if st.button("🧠 Gerar Plano"):

    if st.session_state.ia_resultado:
        st.markdown("## 🤖 IA")
        st.write(st.session_state.ia_resultado)

    st.markdown("## 🥇 Plano")

    plano = []

    if tecido == "fibrina":
        plano.append("Urgoclean + hidrogel")

    elif tecido == "necrose":
        plano.append("Desbridamento")

    elif tecido == "granulação":
        plano.append("Polymem ou Mepilex")

    if infeccao == "sim":
        plano.append("Mepilex AG ou Mel")

    if cavidade:
        plano.append("Cronocol")

    if exsudado == "alto" and not vascular and tecido != "necrose":
        plano.append("TPN (100 mmHg)")

    for p in plano:
        st.write(f"• {p}")

    # ALERTAS
    st.markdown("## ⚠️ Alertas")

    if vascular:
        st.warning("Compromisso vascular")

    if iptb:
        if iptb < 0.5:
            st.error("Isquemia crítica → referenciar vascular")

        if iptb > 1.4:
            st.warning("Calcificação arterial")

    if exsudado == "alto":
        st.warning("Risco de maceração")

    st.warning("Confirmar descarga")

    # DESCARGA
    st.markdown("## 👣 Descarga")
    st.write("• Calçado tipo Baruk")
    st.write("• Feltro de descarga")
