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
# 💾 STORAGE
# ========================
DATA_FILE = "casos.json"
PROFILES_FILE = "profiles.json"


# ========================
# 📥 LOAD GENÉRICO
# ========================
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return None


# ========================
# 📤 SAVE GENÉRICO
# ========================
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


# ========================
# 📁 CASOS
# ========================
def guardar_caso(caso):
    dados = load_json(DATA_FILE)

    if not dados:
        dados = []

    dados.append(caso)

    save_json(DATA_FILE, dados)


# ========================
# 📦 PERFIS
# ========================
def load_profiles():
    return load_json(PROFILES_FILE)


def save_profiles(profiles):
    save_json(PROFILES_FILE, profiles)

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
# 📦 SIDEBAR FINAL LIMPA
# ========================
st.sidebar.title("📦 Stock disponível")

# ========================
# KEYS DE STOCK
# ========================
stock_keys = [
    "prontosan","granudacyn","betadine",
    "urgoclean","urgoclean_ag","flaminal","ulcerase",
    "mel","inadine","iodosorb","silverderma",
    "polymem","mepilex","mepilex_ag",
    "cronocol"
]

# ========================
# 📦 PERFIS DE STOCK
# ========================
if "stock_profiles" not in st.session_state:

    saved_profiles = load_profiles()

    if saved_profiles:
        st.session_state.stock_profiles = saved_profiles
    else:
        st.session_state.stock_profiles = {
            "ULS (Completo)": {k: True for k in stock_keys},
            "HDD (Diabetes)": {
                "prontosan": True,
                "granudacyn": True,
                "betadine": True,
                "urgoclean": True,
                "urgoclean_ag": False,
                "flaminal": True,
                "ulcerase": False,
                "mel": True,
                "inadine": True,
                "iodosorb": False,
                "silverderma": True,
                "polymem": True,
                "mepilex": True,
                "mepilex_ag": True,
                "cronocol": True
            }
        }
# ========================
# INICIALIZAR STATE
# ========================
for k in stock_keys:
    if k not in st.session_state:
        st.session_state[k] = True

# ========================
# APLICAR PERFIL
# ========================
if st.session_state.get("apply_profile"):
    perfil_nome = st.session_state["apply_profile"]
    perfil_data = st.session_state.stock_profiles[perfil_nome]

    for k in stock_keys:
        st.session_state[k] = perfil_data.get(k, False)

    st.session_state["apply_profile"] = None
    st.rerun()


# ========================
# APLICAR RESET
# ========================
if st.session_state.get("reset_stock"):
    for k in stock_keys:
        st.session_state[k] = True
    st.session_state["reset_stock"] = False
    st.rerun()


# ========================
# APLICAR LIMPAR
# ========================
if st.session_state.get("clear_stock"):
    for k in stock_keys:
        st.session_state[k] = False
    st.session_state["clear_stock"] = False
    st.rerun()

# ========================
# 🧼 LIMPEZA
# ========================
with st.sidebar.expander("🧼 Limpeza"):
    st.checkbox("Prontosan", key="prontosan")
    st.checkbox("Granudacyn", key="granudacyn")
    st.checkbox("Betadine", key="betadine")


# ========================
# 🧽 DESBRIDAMENTO
# ========================
with st.sidebar.expander("🧽 Desbridamento"):
    st.checkbox("Urgoclean", key="urgoclean")
    st.checkbox("Urgoclean AG", key="urgoclean_ag")
    st.checkbox("Flaminal", key="flaminal")
    st.checkbox("Ulcerase", key="ulcerase")


# ========================
# 🦠 ANTIMICROBIANOS
# ========================
with st.sidebar.expander("🦠 Antimicrobianos"):
    st.checkbox("Mel", key="mel")
    st.checkbox("Inadine", key="inadine")
    st.checkbox("Iodosorb", key="iodosorb")
    st.checkbox("Silverderma", key="silverderma")


# ========================
# 🧸 ESPUMAS
# ========================
with st.sidebar.expander("🧸 Espumas"):
    st.checkbox("Polymem", key="polymem")
    st.checkbox("Mepilex", key="mepilex")
    st.checkbox("Mepilex AG", key="mepilex_ag")


# ========================
# 🕳️ CAVITÁRIO
# ========================
with st.sidebar.expander("🕳️ Material cavitário"):
    st.checkbox("Cronocol", key="cronocol")

st.sidebar.markdown("### 🏥 Perfis de stock")

perfil = st.sidebar.selectbox(
    "Selecionar perfil",
    list(st.session_state.stock_profiles.keys())
)

if st.sidebar.button("Aplicar perfil"):
    st.session_state["apply_profile"] = perfil
    st.rerun()


# 👇 GUARDAR / ATUALIZAR PERFIS (COM PERSISTÊNCIA)
st.sidebar.markdown("### 💾 Guardar perfil")

novo_nome = st.sidebar.text_input("Nome do novo perfil")

# 💾 GUARDAR NOVO PERFIL
if st.sidebar.button("Guardar perfil atual"):
    if not novo_nome:
        st.warning("Dá um nome ao perfil")
    elif novo_nome in st.session_state.stock_profiles:
        st.warning("Já existe um perfil com esse nome — usa 'Atualizar'")
    else:
        st.session_state.stock_profiles[novo_nome] = {
            k: st.session_state[k] for k in stock_keys
        }
        save_profiles(st.session_state.stock_profiles)
        st.success(f"Perfil '{novo_nome}' guardado")


# ✏️ ATUALIZAR PERFIL EXISTENTE
if st.sidebar.button("Atualizar perfil selecionado"):
    if perfil not in st.session_state.stock_profiles:
        st.warning("Perfil inválido")
    else:
        st.session_state.stock_profiles[perfil] = {
            k: st.session_state[k] for k in stock_keys
        }
        save_profiles(st.session_state.stock_profiles)
        st.success(f"Perfil '{perfil}' atualizado")

# ========================
# ⚙️ GESTÃO DE STOCK (SEGURO)
# ========================
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Gestão de stock")

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("🔄 Reset"):
        st.session_state["reset_stock"] = True
        st.rerun()

with col2:
    if st.button("🚫 Limpar"):
        st.session_state["clear_stock"] = True
        st.rerun()

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

    if st.session_state["polymem"]: stock.append("Polymem")
    if st.session_state["mepilex"]: stock.append("Mepilex")
    if st.session_state["mepilex_ag"]: stock.append("Mepilex AG")
    if st.session_state["urgoclean"]: stock.append("Urgoclean")
    if st.session_state["urgoclean_ag"]: stock.append("Urgoclean AG")
    if st.session_state["mel"]: stock.append("Mel")
    if st.session_state["cronocol"]: stock.append("Cronocol")
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
