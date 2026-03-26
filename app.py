import streamlit as st

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
        st.success("Fibrina → limpeza ativa")
        st.write("• Urgoclean")
        st.write("• + gota de hidrogel (potencia ação)")
        
        if exsudado != "baixo":
            st.write("• Fazer cortes no apósito para drenagem")

    elif tecido == "granulação":
        st.info("Granulação → proteger tecido")
        st.write("• Espuma absorvente")
        st.write("• Polymem")

    if infeccao == "sim":
        st.error("Infeção → adicionar antimicrobiano")
        st.write("• Mel ou prata")

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
