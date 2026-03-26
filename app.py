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

# SIDEBAR
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

# ========================
# 📸 IMAGEM + IA
# ========================
st.markdown("## 📸 Upload de Imagem")

imagem = st.file_uploader("Carregar imagem", type=["jpg", "png", "jpeg"])

if imagem:
    img = Image.open(imagem)

    # Compressão
    img.thumbnail((800, 800))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=70)
    bytes_data = buffer.getvalue()

    st.image(img, caption="Imagem carregada", use_column_width=True)

    if st.button("🔍 Analisar com IA"):

        base64_image = base64.b64encode(bytes_data).decode("utf-8")

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """
Analisa esta ferida de pé diabético.

Identifica:
- tecidos (necrose, fibrina, granulação)
- exsudado (baixo, moderado, alto)

Sugere plano inicial.

Resposta curta.
"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
            )

            resultado = response.choices[0].message.content.lower()
            st.session_state.ia_resultado = resultado

            # Extrair tecido
            if "necrose" in resultado:
                st.session_state.tecido_detectado = "necrose"
            elif "fibrina" in resultado:
                st.session_state.tecido_detectado = "fibrina"
            elif "granulação" in resultado:
                st.session_state.tecido_detectado = "granulação"

            st.success(resultado)

        except Exception:
            st.warning("IA indisponível")

# ========================
# INPUTS
# ========================
st.markdown("## 🧠 Dados Clínicos")

opcoes_tecido = ["necrose", "fibrina", "granulação"]

if st.session_state.tecido_detectado in opcoes_tecido:
    tecido = st.selectbox(
        "Tecido",
        opcoes_tecido,
        index=opcoes_tecido.index(st.session_state.tecido_detectado),
    )
else:
    tecido = st.selectbox("Tecido", opcoes_tecido)

exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
infeccao = st.selectbox("Infeção", ["não", "sim"])
cavidade = st.checkbox("Cavidade")
vascular = st.checkbox("Compromisso vascular")

st.markdown("---")

# ========================
# BOTÃO PRINCIPAL
# ========================
if st.button("🧠 Gerar Plano"):

    # IA
    if st.session_state.ia_resultado:
        st.markdown("## 🤖 Sugestão da IA")
        st.write(st.session_state.ia_resultado)

    # ========================
    # 🥇 PLANO PRINCIPAL
    # ========================
    st.markdown("## 🥇 Plano Principal")

    plano = []

    if tecido == "fibrina":
        if urgoclean:
            plano.append("Urgoclean")
            plano.append("+ gota de hidrogel")
            if exsudado != "baixo":
                plano.append("Cortes no apósito")

    elif tecido == "granulação":
        if polymem:
            plano.append("Polymem")
        elif mepilex:
            plano.append("Mepilex")

    elif tecido == "necrose":
        plano.append("Desbridamento")

    if infeccao == "sim":
        if exsudado != "baixo" and mepilex_ag:
            plano.append("Mepilex AG")
        elif mel:
            plano.append("Mel + espuma")

    if cavidade and cronocol:
        plano.append("Cronocol")

    for p in plano:
        st.write(f"• {p}")

    st.markdown("---")

    # ========================
    # ⚙️ TPN GUIDELINES
    # ========================
    st.markdown("## ⚙️ Terapia de Pressão Negativa")

    usar_tpn = False
    motivo = []

    if exsudado == "alto":
        usar_tpn = True
        motivo.append("Exsudado elevado")

    if cavidade:
        usar_tpn = True
        motivo.append("Cavidade")

    if vascular:
        usar_tpn = False
        motivo = ["Compromisso vascular"]

    if tecido == "necrose":
        usar_tpn = False
        motivo = ["Necrose → desbridar primeiro"]

    if usar_tpn:
        st.success("TPN recomendada")
        st.write("• 100 mmHg")
        for m in motivo:
            st.write(f"• {m}")
    else:
        st.warning("TPN não recomendada")
        for m in motivo:
            st.write(f"• {m}")

    st.markdown("---")

    # ========================
    # ⚠️ ALERTAS
    # ========================
    st.markdown("## ⚠️ Alertas")

    if exsudado == "alto" and not (mepilex or polymem):
        st.warning("Risco de maceração")

    if tecido == "fibrina" and vascular:
        st.warning("Evitar hidrogel isolado")

    if infeccao == "sim" and cavidade and (iodosorb or inadine):
        st.warning("Risco de encerramento precoce")

    st.warning("Confirmar descarga adequada")

    st.markdown("---")

    # ========================
    # 👣 DESCARGA
    # ========================
    st.markdown("## 👣 Descarga")
    st.write("• Calçado tipo Baruk")
    st.write("• Feltro de descarga")
