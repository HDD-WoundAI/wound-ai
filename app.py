import streamlit as st

# CONFIG
st.set_page_config(page_title="Assistente Pé Diabético", layout="centered")

# STOCK DISPONÍVEL
st.sidebar.title("📦 Stock disponível")

stock = {
    "polymem": st.sidebar.checkbox("Polymem", True),
    "urgoclean": st.sidebar.checkbox("Urgoclean", True),
    "urgoclean_ag": st.sidebar.checkbox("Urgoclean AG", True),
    "mel": st.sidebar.checkbox("Mel (L-Mesitran / Actilite)", True),
    "espuma": st.sidebar.checkbox("Espuma absorvente", True),
    "cronocol": st.sidebar.checkbox("Cronocol", True),
    "aquacel": st.sidebar.checkbox("Aquacel", False),
    "iodo": st.sidebar.checkbox("Iodo", False),
    "carvao": st.sidebar.checkbox("Carvão", False)
}

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

    # TECIDO
    if tecido == "necrose":
        st.markdown("### 🧬 Necrose")
        st.write("• Desbridamento (bisturi / cureta)")
        st.write("• Hidrogel / Flaminal Hydro")

    elif tecido == "fibrina":
        st.markdown("### 🧽 Fibrina")

        st.markdown("⭐ Ideal:")
        st.write("• Urgoclean sem prata")

        st.markdown("🟢 Com stock disponível:")

        if stock["urgoclean"]:
            if infeccao == "sim" and stock["urgoclean_ag"]:
                st.write("• Urgoclean AG")
            else:
                st.write("• Urgoclean")

            st.write("• + gota de hidrogel")

            if exsudado != "baixo":
                st.write("• Fazer cortes no apósito para drenagem")

        else:
            st.write("• Urgoclean indisponível")

            st.markdown("🔁 Alternativa:")
            if stock["mel"]:
                st.write("• Mel (L-Mesitran / Actilite)")
            else:
                st.write("• Espuma absorvente")

    elif tecido == "granulação":
        st.markdown("### 🌱 Granulação")

        st.markdown("⭐ Ideal:")
        st.write("• Espuma com silicone")

        st.markdown("🟢 Com stock:")

        if stock["polymem"]:
            st.write("• Polymem (preferido)")
        elif stock["espuma"]:
            st.write("• Espuma absorvente")
        else:
            st.write("• Proteção simples")

    # INFEÇÃO
    if infeccao == "sim":
        st.markdown("### 🦠 Infeção")

        st.markdown("⭐ Ideal:")
        st.write("• Prata direcionada (curto período)")

        st.markdown("🟢 Com stock:")

        if stock["mel"]:
            st.write("• Mel (preferido)")
        elif stock["urgoclean_ag"]:
            st.write("• Urgoclean AG")
        else:
            st.write("• Outro antimicrobiano")

        st.markdown("⚠️ Nota:")
        st.write("• Evitar uso prolongado de prata")

    # CAVIDADE
    if cavidade:
        st.markdown("### 🕳️ Cavidade")
        if stock["cronocol"]:
            st.write("• Cronocol")
        if stock["mel"]:
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
