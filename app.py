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

    st.markdown("## 🩺 Plano Sugerido")

    # VASCULAR
    if vascular:
        st.markdown("### ⚠️ Vascular")
        st.write("• Evitar TPN")

    # NECROSE
    if tecido == "necrose":
        st.markdown("### 🧬 Necrose")
        st.write("• Desbridamento (bisturi / cureta)")
        st.write("• Hidrogel / Flaminal Hydro")

    # FIBRINA
    elif tecido == "fibrina":
        st.markdown("### 🧽 Fibrina")

        st.markdown("⭐ Ideal:")
        st.write("• Limpeza eficaz com mínimo trauma")

        st.markdown("🟢 Com stock:")

        if urgoclean or urgoclean_ag:
            if infeccao == "sim" and urgoclean_ag:
                st.write("• Urgoclean AG")
            else:
                st.write("• Urgoclean (preferido)")

            st.write("• + gota de hidrogel")

            if exsudado != "baixo":
                st.write("• Fazer cortes no apósito")

        if not vascular:
            st.write("• Hidrogel (se necessário)")
        else:
            st.warning("Evitar hidrogel isolado em compromisso vascular")

        st.markdown("💡 Nota:")
        st.write("• Urgoclean menos agressivo em doente vascular")

    # GRANULAÇÃO
    elif tecido == "granulação":
        st.markdown("### 🌱 Granulação")

        st.markdown("⭐ Ideal:")
        st.write("• Proteção + ambiente húmido")

        st.markdown("🟢 Com stock:")

        if polymem:
            st.write("• Polymem (preferido)")
        elif mepilex:
            st.write("• Mepilex")
        else:
            st.write("• Espuma absorvente")

        st.markdown("💡 Nota:")
        st.write("• Evitar trauma no leito")

    # INFEÇÃO
    if infeccao == "sim":
        st.markdown("### 🦠 Infeção")

        st.markdown("⭐ Ideal:")
        st.write("• Antimicrobiano eficaz sem comprometer cicatrização")

        st.markdown("🟢 Com stock (prioridade clínica):")

        if exsudado != "baixo" and mepilex_ag:
            st.write("• Mepilex AG (preferido)")

        if mel:
            st.write("• Mel + espuma absorvente")

        if urgoclean_ag:
            st.write("• Urgoclean AG")

        if iodosorb or inadine:
            st.write("• Iodo (alternativa)")
            st.warning("Pode encerrar superficialmente → vigiar cavidade")

        if silverderma:
            st.write("• Silverderma (última linha)")

        st.markdown("⚠️ Nota:")
        st.write("• Evitar uso prolongado de prata")

    # CAVIDADE
    if cavidade:
        st.markdown("### 🕳️ Cavidade")

        if cronocol:
            st.write("• Cronocol")
        if mel:
            st.write("• Mel tulle")

    # TPN
    if not vascular and exsudado == "alto":
        st.markdown("### ⚙️ Terapia de Pressão Negativa")
        st.write("• Considerar TPN")
        st.write("• Pressão: 100 mmHg")

    # DESCARGA
    st.markdown("---")
    st.markdown("### 👣 Descarga (ESSENCIAL)")
    st.write("• Calçado tipo Baruk")
    st.write("• Feltro com abertura na zona da ferida")
