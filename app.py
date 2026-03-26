import streamlit as st
# STOCK DISPONÍVEL
stock = {
    "polymem": True,
    "urgoclean": True,
    "urgoclean_ag": True,
    "mel": True,
    "espuma": True,
    "cronocol": True,
    "aquacel": False,  # evitado / sem preferência
    "iodo": False,
    "carvao": False
}

st.set_page_config(page_title="Pé Diabético", layout="centered")

st.title("👣 Assistente Pé Diabético")

st.markdown("### Dados da Ferida")

tecido = st.selectbox("Tecido", ["necrose", "fibrina", "granulação"])
exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
infeccao = st.selectbox("Infeção", ["não", "sim"])
cavidade = st.checkbox("Cavidade")
vascular = st.checkbox("Compromisso vascular")

st.markdown("---")

if st.button("🧠 Gerar Plano de Tratamento"):
    
    st.markdown("## 🩺 Plano Sugerido")

    if vascular:
        st.error("Evitar TPN por compromisso vascular")

    if tecido == "necrose":
        st.warning("Necrose presente → realizar desbridamento")
        st.write("• Bisturi / cureta")
        st.write("• Hidrogel / Flaminal Hydro")

    elif tecido == "fibrina":
    
    st.markdown("### 🧽 Fibrina")

    # IDEAL
    st.markdown("⭐ Ideal:")
    st.write("• Urgoclean sem prata")

    # STOCK
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
        st.warning("Urgoclean não disponível")

        # ALTERNATIVA
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
        st.write("• Proteção simples (tulle)")

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
        st.write("• Considerar outro antimicrobiano")

    st.markdown("⚠️ Nota:")
    st.write("• Evitar uso prolongado de prata")
    if cavidade:
        st.warning("Cavidade presente")
        st.write("• Cronocol ou mel tulle")

    if not vascular and exsudado == "alto":
        st.success("Elegível para TPN")
        st.write("• Pressão recomendada: 100 mmHg")

    st.markdown("---")
    st.markdown("### 👣 Descarga (ESSENCIAL)")
    st.write("• Calçado tipo Baruk")
    st.write("• Feltro com abertura na zona da ferida")
