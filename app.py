import streamlit as st

# CONFIG
st.set_page_config(page_title="Assistente Pé Diabético", layout="centered")

# SIDEBAR STOCK
st.sidebar.title("📦 Stock disponível")

# ESPUMAS
with st.sidebar.expander("🧸 Espumas"):
    polymem = st.checkbox("Polymem", True)
    mepilex = st.checkbox("Mepilex", True)
    mepilex_ag = st.checkbox("Mepilex AG", True)

# LIMPEZA
with st.sidebar.expander("🧼 Limpeza"):
    prontosan = st.checkbox("Prontosan", True)
    granudacyn = st.checkbox("Granudacyn", True)
    betadine = st.checkbox("Betadine", True)

# DESBRIDAMENTO
with st.sidebar.expander("🧽 Desbridamento"):
    urgoclean = st.checkbox("Urgoclean", True)
    urgoclean_ag = st.checkbox("Urgoclean AG", True)
    ulcerase = st.checkbox("Ulcerase", True)
    flaminal_hydro = st.checkbox("Flaminal Hydro", True)

# ANTIMICROBIANOS
with st.sidebar.expander("🦠 Antimicrobianos"):
    mel = st.checkbox("Mel (L-Mesitran / Actilite)", True)
    inadine = st.checkbox("Inadine", False)
    iodosorb = st.checkbox("Iodosorb", False)
    silverderma = st.checkbox("Silverderma", True)

# ABSORÇÃO
with st.sidebar.expander("💧 Absorção"):
    aquacel = st.checkbox("Aquacel", False)
    aquacel_ag = st.checkbox("Aquacel AG", False)

# CAVIDADE
with st.sidebar.expander("🕳️ Cavidade"):
    cronocol = st.checkbox("Cronocol", True)

# UI
st.title("👣 Assistente Pé Diabético")
st.markdown("### Dados da Ferida")

tecido = st.selectbox("Tecido", ["necrose", "fibrina", "granulação"])
exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
infeccao = st.selectbox("Infeção", ["não", "sim"])
cavidade = st.checkbox("Cavidade")
vascular = st.checkbox("Compromisso vascular")

st.markdown("---")

# BOTÃO
if st.button("🧠 Gerar Plano de Tratamento"):

    # ========================
    # 🥇 PLANO PRINCIPAL
    # ========================
    st.markdown("## 🥇 Plano Principal")

    plano_principal = []

    if tecido == "fibrina":
        if urgoclean:
            plano_principal.append("Urgoclean")
            plano_principal.append("+ gota de hidrogel")

            if exsudado != "baixo":
                plano_principal.append("Cortes no apósito")

    elif tecido == "granulação":
        if polymem:
            plano_principal.append("Polymem")
        elif mepilex:
            plano_principal.append("Mepilex")

    elif tecido == "necrose":
        plano_principal.append("Desbridamento")

    if infeccao == "sim":
        if exsudado != "baixo" and mepilex_ag:
            plano_principal.append("Mepilex AG")
        elif mel:
            plano_principal.append("Mel + espuma")

    if cavidade and cronocol:
        plano_principal.append("Cronocol")

    for item in plano_principal:
        st.write(f"• {item}")

    st.markdown("---")

    # ========================
    # 🩺 PLANO DETALHADO
    # ========================
    st.markdown("## 🩺 Plano Detalhado")

    if vascular:
        st.markdown("### ⚠️ Vascular")
        st.write("• Evitar TPN")

    if tecido == "necrose":
        st.markdown("### 🧬 Necrose")
        st.write("• Desbridamento (bisturi / cureta)")
        st.write("• Hidrogel / Flaminal Hydro")

    elif tecido == "fibrina":
        st.markdown("### 🧽 Fibrina")
        st.write("• Urgoclean (preferido)")
        st.write("• + gota de hidrogel")

        if exsudado != "baixo":
            st.write("• Fazer cortes no apósito")

        if vascular:
            st.warning("Evitar hidrogel isolado em doente vascular")

    elif tecido == "granulação":
        st.markdown("### 🌱 Granulação")

        if polymem:
            st.write("• Polymem (preferido)")
        elif mepilex:
            st.write("• Mepilex")
        else:
            st.write("• Espuma")

    if infeccao == "sim":
        st.markdown("### 🦠 Infeção")

        if exsudado != "baixo" and mepilex_ag:
            st.write("• Mepilex AG (preferido)")

        if mel:
            st.write("• Mel + espuma")

        if urgoclean_ag:
            st.write("• Urgoclean AG")

        if iodosorb or inadine:
            st.write("• Iodo")
            st.warning("Risco de encerramento superficial precoce")

        if silverderma:
            st.write("• Silverderma (última linha)")

    if cavidade:
        st.markdown("### 🕳️ Cavidade")

        if cronocol:
            st.write("• Cronocol")

        if mel:
            st.write("• Mel tulle")

    if not vascular and exsudado == "alto":
        st.markdown("### ⚙️ TPN")
        st.write("• Considerar TPN a 100 mmHg")

    st.markdown("---")

    # ========================
    # ⚠️ ALERTAS CLÍNICOS
    # ========================
    st.markdown("## ⚠️ Alertas Clínicos")

    alertas = []

    if exsudado == "alto" and not (mepilex or polymem or aquacel):
        alertas.append("Exsudado alto sem absorção adequada → risco de maceração")

    if tecido == "fibrina" and vascular:
        alertas.append("Evitar hidrogel isolado em doente vascular")

    if infeccao == "sim" and cavidade and (iodosorb or inadine):
        alertas.append("Iodo pode causar encerramento superficial precoce")

    if infeccao == "sim" and exsudado == "baixo":
        alertas.append("Evitar prata sem exsudado significativo")

    alertas.append("Confirmar descarga adequada")

    for alerta in alertas:
        st.warning(alerta)

    # ========================
    # 👣 DESCARGA
    # ========================
    st.markdown("---")
    st.markdown("### 👣 Descarga (ESSENCIAL)")
    st.write("• Calçado tipo Baruk")
    st.write("• Feltro com abertura na zona da ferida")
