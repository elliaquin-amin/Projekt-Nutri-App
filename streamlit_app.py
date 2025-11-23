import streamlit as st

def interface_prototipo():
    st.title("🍽️ NutriApp")

    # rf01,02 e 03 - um informativo geral
    with st.expander("ℹ️ Clique aqui para ver informações sobre os grupos alimentares"):
        st.markdown("""
        ### **Entenda os Grupos Alimentares**

        **Por que porções de 100g?**  
        A escolha segue a RDC 429/2020 e a IN 75/2020 da Anvisa, que determinam que os distribuidores
        devem informar os valores nutricionais com base em 100 g do produto.

        **1️⃣ Cereais, pães, raízes e tubérculos**  
        Fontes de **carboidratos**, que fornecem energia para o corpo.  
        - **Cereais**: arroz, milho, aveia, trigo, cevada.  
        - **Raízes**: mandioca, cenoura.  
        - **Tubérculos**: batata, inhame.  
        🔹 *Diferença:* raízes vêm da raiz da planta; tubérculos são caules modificados.

        **2️⃣ Verduras, legumes e frutas**  
        Ricos em **vitaminas, minerais e fibras**, auxiliam na regulação do organismo.  
        - **Verduras**: folhas e caules (alface, couve).  
        - **Legumes**: abobrinha, cenoura, beterraba.  
        - **Frutas**: maçã, banana, laranja.  
        🔹 *Diferença:* verduras vêm das folhas e caules; legumes de outras partes vegetais; frutas dos frutos maduros.

        **3️⃣ Carnes vermelhas ou brancas**  
        Fontes de **proteínas, ferro e vitaminas**.  
        - **Carnes vermelhas**: bovina, suína, ovina.  
        - **Carnes brancas**: aves e peixes — de digestão mais leve e menor teor de gordura.
        """)

    st.markdown("---")


    # rf04,05 e 06 — Cadastro de Alimentos

    st.subheader("🧾 Cadastro de Alimentos")

    # inicializa o armazenamento dos alimentos
    if "alimentos" not in st.session_state:
        st.session_state["alimentos"] = []

    # prosseguir com o fformulário de cadastro
    with st.form("form_cadastro"):
        nome = st.text_input("Nome do alimento (exemplo: Arroz integral)")
        grupo = st.selectbox(
            "Grupo Alimentar",
            [
                "Cereais, pães, raízes e tubérculos",
                "Verduras, legumes e frutas",
                "Carnes vermelhas ou brancas"
            ]
        )
        st.number_input("Calorias (kcal)", min_value=0.0, step=0.1)
        st.number_input("Carboidratos (g)", min_value=0.0, step=0.1)
        st.number_input("Proteínas (g)", min_value=0.0, step=0.1)
        st.number_input("Gorduras (g)", min_value=0.0, step=0.1)
        st.number_input("Fibras (g)", min_value=0.0, step=0.1)

        cadastrar = st.form_submit_button("Cadastrar")

    # ação para quando cadastrar
    if cadastrar and nome.strip():
        st.session_state["alimentos"].append(nome)
        st.success(f"✅ Alimento '{nome}' cadastrado com sucesso!")

    # exibição de alimento cadastrados até o momento
    st.markdown("---")
    st.subheader("📋 Alimentos Cadastrados")

    if st.session_state["alimentos"]:
        for i, alimento in enumerate(st.session_state["alimentos"], start=1):
            st.write(f"{i}. {alimento}")
    else:
        st.info("Nenhum alimento cadastrado até o momento.")
if __name__ == "__main__":
    interface_prototipo()
