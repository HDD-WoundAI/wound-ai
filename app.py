import streamlit as st
from PIL import Image
import base64
import io
import json
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="Assistente Pé Diabético", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ========================
# STORAGE
# ========================
DATA_FILE = "casos.json"

def guardar_caso(caso):
    try:
        with open(DATA_FILE, "r") as f:
            dados = json.load(f)
    except:
        dados = []

    dados.append(caso)

    with open(DATA_FILE, "w") as f:
        json.dump(dados, f)

# ========================
# SESSION
# ========================
if "ia_output" not in st.session_state:
    st.session_state.ia_output = None

# ========================
# 📦 SIDEBAR (CORRIGIDO)
# ========================
st.sidebar.title("📦 Stock disponível")

with st.sidebar.expander("🧼 Limpeza"):
    prontosan = st.checkbox("Prontosan", True)
    granudacyn = st.checkbox("Granudacyn", True)
    betadine = st.checkbox("Betadine", True)

with st.sidebar.expander("🧽 Desbridamento"):
    urgoclean = st.checkbox("Urgoclean", True)
    urgoclean_ag = st.checkbox("Urgoclean AG", True)
    flaminal = st.checkbox("Flaminal", True)
    ulcerase = st.checkbox("Ulcerase", True)

with st.sidebar.expander("🦠 Antimicrobianos"):
    mel = st.checkbox("Mel", True)
    inadine = st.checkbox("Inadine", False)
    iodosorb = st.checkbox("Iodosorb", False)
    silverderma = st.checkbox("Silverderma", True)

with st.sidebar.expander("🧸 Espumas"):
    polymem = st.checkbox("Polymem", True)
    mepilex = st.checkbox("Mepilex", True)
    mepilex_ag = st.checkbox("Mepilex AG", True)

with st.sidebar.expander("🕳️ Cavidade"):
    cronocol = st.checkbox("Cronocol", True)

# ========================
# UI
# ========================
st.title("👣 Assistente Pé Diabético")

nome = st.text_input("Nome / ID do doente")

# ========================
# 📸 IMAGEM
# ========================
imagem = st.file_uploader("Carregar imagem", type=["jpg", "png", "jpeg"])

if imagem:
    img = Image.open(imagem)
    img.thumbnail((800, 800))

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=70)
    bytes_data = buffer.getvalue()

    st.image(img, use_column_width=True)

# ========================
# IA
# ========================
if st.button("🧠 Análise automática") and imagem:

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
Analisa esta ferida.

Indica:
- tecido
- exsudado
- infeção

E sugere plano com materiais.
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        },
                    ],
                }
            ],
        )

        st.session_state.ia_output = response.choices[0].message.content

    except:
        st.warning("IA indisponível")

# ========================
# MOSTRAR IA
# ========================
if st.session_state.ia_output:
    st.markdown("## 🤖 Plano automático")
    st.write(st.session_state.ia_output)

# ========================
# INPUTS MANUAIS
# ========================
st.markdown("## 🔧 Ajustes manuais")

override = st.checkbox("Adicionar dados clínicos")

if override:
    infeccao = st.selectbox("Infeção", ["não", "sim"])
    exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
    cavidade = st.checkbox("Cavidade")
    vascular = st.checkbox("Compromisso vascular")

    # ========================
    # IPTB (REINTRODUZIDO)
    # ========================
    iptb = None

    if not vascular:
        st.markdown("### 📊 IPTB")

        braquial = st.number_input("Pressão braquial")
        tibial = st.number_input("Pressão tibial")

        if braquial > 0 and tibial > 0:
            iptb = tibial / braquial

            if iptb > 1.4:
                st.info(f"🔵 IPTB {iptb:.2f} → Calcificação")
            elif 0.9 <= iptb <= 1.3:
                st.success(f"🟢 IPTB {iptb:.2f} → Normal")
            elif 0.7 <= iptb < 0.9:
                st.warning(f"🟡 IPTB {iptb:.2f} → Ligeira")
            elif 0.4 <= iptb < 0.7:
                st.warning(f"🟠 IPTB {iptb:.2f} → Moderada")
            else:
                st.error(f"🔴 IPTB {iptb:.2f} → Grave")

# ========================
# DECISÃO
# ========================
if st.button("🧠 Gerar Plano"):

    st.markdown("## 🥇 Plano final")

    plano = []

    if override:

        if exsudado == "alto" and not vascular:
            plano.append("TPN (100 mmHg)")

        if infeccao == "sim":
            if mepilex_ag:
                plano.append("Mepilex AG")
            elif mel:
                plano.append("Mel")

        if cavidade and cronocol:
            plano.append("Cronocol")

        if urgoclean:
            plano.append("Urgoclean + hidrogel")

    else:
        plano.append("Seguir plano da IA")

    for p in plano:
        st.write(f"• {p}")

    # ALERTAS
    st.markdown("## ⚠️ Alertas")

    if override and iptb and iptb < 0.5:
        st.error("Isquemia crítica")

    if override and exsudado == "alto":
        st.warning("Risco de maceração")

    st.warning("Confirmar descarga")

# ========================
# GUARDAR
# ========================
if st.button("💾 Guardar caso"):

    caso = {
        "nome": nome,
        "data": str(datetime.now()),
        "plano": st.session_state.ia_output,
    }

    guardar_caso(caso)

    st.success("Caso guardado")
