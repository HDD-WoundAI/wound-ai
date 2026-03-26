import streamlit as st
from PIL import Image
import base64
import io
import json
from datetime import datetime
from openai import OpenAI

# ========================
# CONFIG
# ========================
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
# 🧠 IA AUTOMÁTICA
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
Analisa esta ferida de pé diabético.

Indica:
- tecido predominante
- exsudado
- infeção provável

E sugere plano com materiais reais (ex: Urgoclean, Polymem, Mepilex AG, TPN).

Resposta curta e clínica.
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

        st.session_state.ia_output = response.choices[0].message.content

    except:
        st.warning("IA indisponível")

# ========================
# RESULTADO IA
# ========================
if st.session_state.ia_output:
    st.markdown("## 🤖 Plano automático")
    st.write(st.session_state.ia_output)

# ========================
# 🔧 AJUSTE MANUAL
# ========================
st.markdown("## 🔧 Ajustes manuais (opcional)")

override = st.checkbox("Adicionar informação manual")

plano_manual = []

if override:
    infeccao = st.selectbox("Infeção", ["não", "sim"])
    exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
    cavidade = st.checkbox("Cavidade")
    vascular = st.checkbox("Compromisso vascular")

    if st.button("🔄 Recalcular plano"):

        if exsudado == "alto" and not vascular:
            plano_manual.append("TPN (100 mmHg)")

        if infeccao == "sim":
            plano_manual.append("Mepilex AG ou Mel")

        if cavidade:
            plano_manual.append("Cronocol")

        st.markdown("## 🔁 Plano ajustado")
        for p in plano_manual:
            st.write(f"• {p}")

# ========================
# 💾 GUARDAR CASO
# ========================
if st.button("💾 Guardar caso"):

    caso = {
        "nome": nome,
        "data": str(datetime.now()),
        "plano": st.session_state.ia_output,
    }

    guardar_caso(caso)

    st.success("Caso guardado com sucesso")

# ========================
# 📊 SCORE DE RISCO
# ========================
st.markdown("## 📊 Score de risco")

score = 0

if override:
    if infeccao == "sim":
        score += 2
    if exsudado == "alto":
        score += 2
    if cavidade:
        score += 1
    if vascular:
        score += 2

if score >= 5:
    st.error("🔴 Alto risco")
elif score >= 3:
    st.warning("🟠 Risco moderado")
else:
    st.success("🟢 Baixo risco")
