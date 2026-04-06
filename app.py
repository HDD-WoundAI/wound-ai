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
# STOCK (COMPLETO)
# ========================
if "stock" not in st.session_state:
    st.session_state.stock = {
        "prontosan": True,
        "granudacyn": True,
        "betadine": True,
        "urgoclean": True,
        "urgoclean_ag": True,
        "flaminal": True,
        "ulcerase": True,
        "mel": True,
        "inadine": True,
        "iodosorb": True,
        "silverderma": True,
        "polymem": True,
        "mepilex": True,
        "mepilex_ag": True,
        "cronocol": True
    }

# ========================
# 📦 SIDEBAR (COM STATE)
# ========================
st.sidebar.title("📦 Stock disponível")

with st.sidebar.expander("🧼 Limpeza"):
    prontosan = st.checkbox(
        "Prontosan",
        value=st.session_state.stock["prontosan"],
        key="prontosan_checkbox"
    )
    st.session_state.stock["prontosan"] = prontosan

    granudacyn = st.checkbox(
        "Granudacyn",
        value=st.session_state.stock["granudacyn"],
        key="granudacyn_checkbox"
    )
    st.session_state.stock["granudacyn"] = granudacyn

    betadine = st.checkbox(
        "Betadine",
        value=st.session_state.stock["betadine"],
        key="betadine_checkbox"
    )
    st.session_state.stock["betadine"] = betadine


with st.sidebar.expander("🧽 Desbridamento"):
    urgoclean = st.checkbox(
        "Urgoclean",
        value=st.session_state.stock["urgoclean"],
        key="urgoclean_checkbox"
    )
    st.session_state.stock["urgoclean"] = urgoclean

    urgoclean_ag = st.checkbox(
        "Urgoclean AG",
        value=st.session_state.stock["urgoclean_ag"],
        key="urgoclean_ag_checkbox"
    )
    st.session_state.stock["urgoclean_ag"] = urgoclean_ag

    flaminal = st.checkbox(
        "Flaminal",
        value=st.session_state.stock["flaminal"],
        key="flaminal_checkbox"
    )
    st.session_state.stock["flaminal"] = flaminal

    ulcerase = st.checkbox(
        "Ulcerase",
        value=st.session_state.stock["ulcerase"],
        key="ulcerase_checkbox"
    )
    st.session_state.stock["ulcerase"] = ulcerase


with st.sidebar.expander("🦠 Antimicrobianos"):
    mel = st.checkbox(
        "Mel",
        value=st.session_state.stock["mel"],
        key="mel_checkbox"
    )
    st.session_state.stock["mel"] = mel

    inadine = st.checkbox(
        "Inadine",
        value=st.session_state.stock["inadine"],
        key="inadine_checkbox"
    )
    st.session_state.stock["inadine"] = inadine

    iodosorb = st.checkbox(
        "Iodosorb",
        value=st.session_state.stock["iodosorb"],
        key="iodosorb_checkbox"
    )
    st.session_state.stock["iodosorb"] = iodosorb

    silverderma = st.checkbox(
        "Silverderma",
        value=st.session_state.stock["silverderma"],
        key="silverderma_checkbox"
    )
    st.session_state.stock["silverderma"] = silverderma


with st.sidebar.expander("🧸 Espumas"):
    polymem = st.checkbox(
        "Polymem",
        value=st.session_state.stock["polymem"],
        key="polymem_checkbox"
    )
    st.session_state.stock["polymem"] = polymem

    mepilex = st.checkbox(
        "Mepilex",
        value=st.session_state.stock["mepilex"],
        key="mepilex_checkbox"
    )
    st.session_state.stock["mepilex"] = mepilex

    mepilex_ag = st.checkbox(
        "Mepilex AG",
        value=st.session_state.stock["mepilex_ag"],
        key="mepilex_ag_checkbox"
    )
    st.session_state.stock["mepilex_ag"] = mepilex_ag


with st.sidebar.expander("🕳️ Material cavitário"):
    cronocol = st.checkbox(
        "Cronocol",
        value=st.session_state.stock["cronocol"],
        key="cronocol_checkbox"
    )
    st.session_state.stock["cronocol"] = cronocol


# 👇 SEM indentação (fora do expander)
st.sidebar.markdown("### ⚙️ Gestão de stock")

if st.sidebar.button("🔄 Reset stock"):
    st.session_state.stock = {k: True for k in st.session_state.stock}
    st.rerun()

if st.sidebar.button("🚫 Limpar stock"):
    st.session_state.stock = {k: False for k in st.session_state.stock}
    st.rerun()
# ========================
# UI
# ========================
st.title("👣 Assistente Pé Diabético")

col1, col2 = st.columns([2, 1])

with col1:
    nome = st.text_input("Nome do doente")

with col2:
    processo = st.text_input("Nº processo", max_chars=10)

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
# INPUTS MANUAIS
# ========================
st.markdown("## 🔧 Ajustes manuais")

override = st.checkbox("Adicionar dados clínicos")

if override:

    tecido = st.selectbox(
        "Tecido predominante",
        ["não determinado", "necrose", "fibrina", "granulação"],
        key="tecido"
    )

    infeccao = st.selectbox(
        "Infeção",
        ["não", "sim"],
        key="infeccao"
    )

    exsudado = st.selectbox(
        "Exsudado",
        ["baixo", "moderado", "alto"],
        key="exsudado"
    )

    fistula = st.checkbox(
        "Fístula",
        key="fistula"
    )
    # ========================
    # ========================
    # 🧠 NEUROPATIA
    # ========================
    st.markdown("## 🧠 Neuropatia")
    
    neuropatia = st.checkbox("Neuropatia conhecida")
    
    if not neuropatia:
    
        with st.expander("Avaliação da neuropatia"):
    
            st.markdown("### Sensibilidades")
    
            tactil = st.checkbox("Táctil (presente)", key="tactil")
            vibratoria = st.checkbox("Vibratória (presente)", key="vibratoria")
            dolorosa = st.checkbox("Dolorosa (presente)", key="dolorosa")
            termica = st.checkbox("Térmica (presente)", key="termica")
    
            # ========================
            # 🧠 INTERPRETAÇÃO CLÍNICA
            # ========================
            alteracoes = []
    
            if not tactil:
                alteracoes.append("táctil")
            if not vibratoria:
                alteracoes.append("vibratória")
            if not dolorosa:
                alteracoes.append("dolorosa")
            if not termica:
                alteracoes.append("térmica")
    
            if not tactil:
                st.error("Neuropatia provável: perda de sensibilidade protectora (táctil)")
    
            elif len(alteracoes) >= 2:
                st.warning("Neuropatia provável: múltiplas sensibilidades alteradas (" + ", ".join(alteracoes) + ")")
    
            elif alteracoes == ["vibratória"]:
                st.info("Neuropatia pouco provável: apenas sensibilidade vibratória ausente, variável de difícil avaliação. Isolada não atesta diagnóstico")
    
            elif len(alteracoes) == 1:
                st.warning("Neuropatia possível: alteração isolada (" + alteracoes[0] + ")")
    
            else:
                st.success("Sensibilidades preservadas")
        
    
    # ========================
    # 🩸 COMPROMISSO VASCULAR
    # ========================
    st.markdown("## 🩸 Compromisso Vascular")
    
    vascular = st.checkbox("Compromisso vascular conhecido")
    
    iptb = None
    
    if not vascular:
    
        with st.expander("Avaliação vascular"):
    
            pulsos = st.selectbox(
                "Pulsos",
                ["não determinado", "presentes", "ausentes"],
                key="pulsos"
            )
    
            iptb_direto = st.number_input(
                "IPTB (valor direto)",
                value=0.0,
                key="iptb_direto"
            )
    
            st.markdown("#### Ou calcular IPTB")
    
            braquial = st.number_input("Pressão braquial", key="braquial")
            tibial = st.number_input("Pressão tibial", key="tibial")
    
            if braquial > 0 and tibial > 0:
                iptb = tibial / braquial
    
            elif iptb_direto > 0:
                iptb = iptb_direto
    
            # RESULTADO
            if iptb:
    
                st.markdown("### 📊 Resultado IPTB")
    
                if iptb > 1.4:
                    st.info(f"🔵 IPTB {iptb:.2f} → Calcificação arterial / vasos não compressíveis")
    
                elif 0.9 <= iptb <= 1.3:
                    st.success(f"🟢 IPTB {iptb:.2f} → Normal")
    
                elif 0.7 <= iptb < 0.9:
                    st.warning(f"🟡 IPTB {iptb:.2f} → Obstrução ligeira")
    
                elif 0.4 <= iptb < 0.7:
                    st.warning(f"🟠 IPTB {iptb:.2f} → Obstrução moderada")
    
                elif iptb < 0.4:
                    st.error(f"🔴 IPTB {iptb:.2f} → Isquemia grave")
# ========================
# DECISÃO
# ========================
if st.button("🧠 Gerar Plano"):

    st.markdown("## 🥇 Plano de Tratamento")

    # ========================
    # 🤖 IA (PLANO PRINCIPAL)
    # ========================
    imagem_base64 = None

    if imagem:
        imagem_base64 = base64.b64encode(bytes_data).decode("utf-8")

    stock = []

    if polymem: stock.append("Polymem")
    if mepilex: stock.append("Mepilex")
    if mepilex_ag: stock.append("Mepilex AG")
    if urgoclean: stock.append("Urgoclean")
    if urgoclean_ag: stock.append("Urgoclean AG")
    if mel: stock.append("Mel")
    if cronocol: stock.append("Cronocol")

    contexto = ""

    if override:
        contexto += f"""
Tecido: {tecido}
Exsudado: {exsudado}
Infeção: {infeccao}
Fístula: {fistula}
Vascular: {vascular}
"""
        if iptb:
            contexto += f"\nIPTB: {iptb:.2f}"

    prompt = f"""
Define plano de tratamento para pé diabético.

Material disponível:
{", ".join(stock)}

{contexto}

Inclui:
- plano principal
- alternativas
- notas clínicas
"""

    try:
        if imagem_base64:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagem_base64}"}},
                        ],
                    }
                ],
            )
        else:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
            )

        resultado = response.choices[0].message.content

        st.write(resultado)

    except:
        st.error("Erro IA")

    # ========================
    # ⚙️ AJUSTES CLÍNICOS TEUS
    # ========================
    st.markdown("## ⚙️ Ajustes clínicos automáticos")

    plano = []

    if override:

        if exsudado == "alto" and not vascular:
            plano.append("Considerar TPN (100 mmHg)")

        if infeccao == "sim":
            plano.append("Garantir cobertura antimicrobiana")

        if fistula and cronocol:
            plano.append("Preencher cavidade com Cronocol")

        if urgoclean and tecido == "fibrina":
            plano.append("Urgoclean + hidrogel (potenciar desbridamento)")

    for p in plano:
        st.write(f"• {p}")

    # ========================
    # ⚠️ ALERTAS (MANTIDOS)
    # ========================
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
