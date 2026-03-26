import streamlit as st

st.title("Assistente Pé Diabético 👣")

st.header("Dados da Ferida")

tecido = st.selectbox("Tipo de tecido", ["necrose", "fibrina", "granulação"])
exsudado = st.selectbox("Exsudado", ["baixo", "moderado", "alto"])
infeccao = st.selectbox("Infeção", ["não", "sim"])
cavidade = st.checkbox("Cavidade")
vascular = st.checkbox("Compromisso vascular")

st.header("Plano")

if st.button("Gerar Plano"):
    
    st.subheader("Recomendação:")

    if vascular:
        st.write("❌ Evitar TPN")

    if tecido == "necrose":
        st.write("➡️ Desbridamento (bisturi/cureta)")
        st.write("➡️ Hidrogel ou Flaminal Hydro")

    elif tecido == "fibrina":
        st.write("➡️ Urgoclean")
        st.write("💡 Adicionar gota de hidrogel")
        
        if exsudado != "baixo":
            st.write("✂️ Fazer cortes no apósito para drenagem")

    elif tecido == "granulação":
        st.write("➡️ Espuma ou Polymem")

    if infeccao == "sim":
        st.write("🦠 Considerar mel ou prata")

    if cavidade:
        st.write("🕳️ Cronocol ou mel tulle")

    if not vascular and exsudado == "alto":
        st.write("⚙️ Considerar TPN a 100 mmHg")

    st.write("👣 Implementar descarga (Baruk/feltro)")
