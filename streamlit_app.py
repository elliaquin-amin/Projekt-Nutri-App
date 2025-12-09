import streamlit as st
import plotly.graph_objects as go
from database import SessionLocal
from models import Alimento


# =====================================================
#               FUNÇÕES PARA O  BANCO DE DADOS
# =====================================================

def inserir_alimento(nome, grupo, cal, carb, prot, gord, fibra):
    db = SessionLocal()
    alimento = Alimento(
        nome=nome,
        grupo=grupo,
        cal=cal,
        carb=carb,
        prot=prot,
        gord=gord,
        fibra=fibra
    )
    db.add(alimento)
    db.commit()
    db.close()


def listar_alimentos():
    db = SessionLocal()
    dados = db.query(Alimento).all()
    db.close()
    return dados


def atualizar_alimento(id_, nome, grupo, cal, carb, prot, gord, fibra):
    db = SessionLocal()
    alimento = db.query(Alimento).filter(Alimento.id == id_).first()

    alimento.nome = nome
    alimento.grupo = grupo
    alimento.cal = cal
    alimento.carb = carb
    alimento.prot = prot
    alimento.gord = gord
    alimento.fibra = fibra

    db.commit()
    db.close()
# =====================================================
#                PAINEL DE ALIMENTOS 
# =====================================================

class PainelAlimentos:
    def __init__(self):
        if "edit_id" not in st.session_state:
            st.session_state["edit_id"] = None
    def cadastrar(self):
        st.subheader("📝 Cadastro de Alimentos")
        # ✔ RF03 — Permite o cadastro visual dos alimentos
        # ✔ RF04 — Exibe os campos nutricionais
        with st.form("form_cadastro", clear_on_submit=True):
            nome = st.text_input("Nome do alimento")
            grupo = st.selectbox(
                "Grupo Alimentar",
                [
                    "Cereais, pães, raízes e tubérculos",
                    "Verduras, legumes e frutas",
                    "Carnes vermelhas ou brancas"
                ]
            )
            cal = st.number_input("Calorias (kcal)", min_value=0.0)
            carb = st.number_input("Carboidratos (g)", min_value=0.0)
            prot = st.number_input("Proteínas (g)", min_value=0.0)
            gord = st.number_input("Gorduras (g)", min_value=0.0)
            fibra = st.number_input("Fibras (g)", min_value=0.0)

            cadastrar = st.form_submit_button("Cadastrar alimento")

        if cadastrar and nome.strip():
            inserir_alimento(nome, grupo, cal, carb, prot, gord, fibra)
            st.success(f"✔ '{nome}' cadastrado com sucesso!")

    def listar(self):
        st.subheader("📋 Alimentos Cadastrados")

        alimentos = listar_alimentos()

        if not alimentos:
            st.info("Nenhum alimento cadastrado ainda.")
            return

        # ✔ RF05 — Interface
        nomes = [a.nome for a in alimentos]

        idx = st.selectbox("Selecione para editar:", range(len(nomes)),
                           format_func=lambda x: nomes[x])

        if st.button("✏️ Editar alimento selecionado"):
            st.session_state["edit_id"] = alimentos[idx].id

        self.editar()

    def editar(self):
        id_ = st.session_state["edit_id"]
        if id_ is None:
            return  # edição não aberta → não renderiza nada

        alimentos = listar_alimentos()
        alimento = next(a for a in alimentos if a.id == id_)

        st.markdown("### ✏️ Editando alimento:")

        with st.form("form_editar"):
            nome = st.text_input("Nome", alimento.nome)
            grupo = st.selectbox(
                "Grupo",
                [
                    "Cereais, pães, raízes e tubérculos",
                    "Verduras, legumes e frutas",
                    "Carnes vermelhas ou brancas"
                ],
                index=[
                    "Cereais, pães, raízes e tubérculos",
                    "Verduras, legumes e frutas",
                    "Carnes vermelhas ou brancas"
                ].index(alimento.grupo)
            )
            cal = st.number_input("Calorias", value=float(alimento.cal))
            carb = st.number_input("Carboidratos", value=float(alimento.carb))
            prot = st.number_input("Proteínas", value=float(alimento.prot))
            gord = st.number_input("Gorduras", value=float(alimento.gord))
            fibra = st.number_input("Fibras", value=float(alimento.fibra))

            col1, col2 = st.columns(2)
            salvar = col1.form_submit_button("✔ Salvar alterações")
            cancelar = col2.form_submit_button("❌ Cancelar edição")

        # ---- BOTÃO SALVAR ----
        if salvar:
            atualizar_alimento(id_, nome, grupo, cal, carb, prot, gord, fibra)
            st.session_state["edit_id"] = None  # FECHA A ABA
            st.success("✔ Alterações salvas!")
            st.rerun()


        # ---- BOTÃO CANCELAR ----
        if cancelar:
            st.session_state["edit_id"] = None  # FECHA A ABA
            st.info("Edição cancelada.")
            st.rerun()


# =====================================================
#              PAINEL PARA PROJETTAR A REFEIÇÃO
# =====================================================

class PainelRefeicao:
    def __init__(self):
        if "refeicao" not in st.session_state:
            st.session_state["refeicao"] = {}
    def montar(self):
        st.subheader("🍽️ Montar Refeição (100g por clique)")
        # ✔ RF06 — Cálculo nutricional total
        alimentos = listar_alimentos()
        if not alimentos:
            st.info("Cadastre alimentos primeiro.")
            return
        nomes = [a.nome for a in alimentos]
        escolha = st.selectbox("Escolha um alimento:", nomes)
        if st.button("Adicionar 100g"):
            st.session_state["refeicao"].setdefault(escolha, 0)
            st.session_state["refeicao"][escolha] += 100
            st.success(f"➡ Adicionado 100g de {escolha}")
        if st.button("❌ Limpar refeição"):
            st.session_state["refeicao"] = {}
            st.warning("Refeição apagada.")

        self.exibir()

    def exibir(self):
        refeicao = st.session_state["refeicao"]
        st.markdown("---")
        st.subheader("📊 Itens da Refeição")
        if not refeicao:
            st.info("Nenhum alimento adicionado ainda.")
            return

        alimentos = listar_alimentos()
        dic = {a.nome: a for a in alimentos}
        st.write("### 🍽️ Sua refeição contém:")
        totais = {"cal": 0, "carb": 0, "prot": 0, "gord": 0, "fibra": 0}

        for nome, gramas in refeicao.items():
            st.write(f"- **{gramas}g** de **{nome}**")
            a = dic[nome]
            mult = gramas / 100

            totais["cal"] += a.cal * mult
            totais["carb"] += a.carb * mult
            totais["prot"] += a.prot * mult
            totais["gord"] += a.gord * mult
            totais["fibra"] += a.fibra * mult

        st.write("### 🔎 Totais nutricionais:")
        for k, v in totais.items():
            st.write(f"- **{k.upper()}**: {v:.1f}")

        # ✔ RF07 — Gráfico nutricional
        self.grafico(totais)

        # ✔ RF08 — Resumo textual da refeição
        self.resumo_textual(totais)

    def grafico(self, totais):
        labels = ["Calorias", "Carboidratos", "Proteínas", "Gorduras", "Fibras"]
        valores = [totais["cal"], totais["carb"], totais["prot"], totais["gord"], totais["fibra"]]

        fig = go.Figure(go.Bar(
            x=labels,
            y=valores,
            text=[f"{v:.1f}" for v in valores],
            textposition="outside",
            marker=dict(colorscale="Turbo", color=valores)
        ))

        fig.update_layout(
            title="🍽️ Composição Nutricional da Refeição",
            template="plotly_white",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # ✔ RF08 — RESUMO TEXTUAL DA REFEIÇÃO
    # =====================================================
    def resumo_textual(self, totais):
        st.markdown("---")
        st.subheader("📝 Resumo Textual da Refeição (RF08)")

        resumo = f"""
        Sua refeição possui **{totais['cal']:.1f} kcal**, composta por:

        - **{totais['carb']:.1f}g** de carboidratos  
        - **{totais['prot']:.1f}g** de proteínas  
        - **{totais['gord']:.1f}g** de gorduras  
        - **{totais['fibra']:.1f}g** de fibras  

        **Interpretação básica:**

        - Carboidratos → energia rápida  
        - Proteínas → construção muscular  
        - Gorduras → energia de longa duração  
        - Fibras → melhora da digestão  

        """

        st.markdown(resumo)


# =====================================================
#                    INTERFFACE PRINCIPAL
# =====================================================

def interface_prototipo():
    st.title("🍽️ NutriApp")

    # ✔ RF01 e RF02 — Informações + justificativa 100g
    with st.expander("ℹ️ Informações sobre grupos alimentares e porções"):
        st.markdown("""
       #### 1️⃣ Cereais, pães, raízes e tubérculos
        Fontes de carboidratos e energia.

        #### 2️⃣ Verduras, legumes e frutas
        Ricos em vitaminas, fibras e minerais.

        #### 3️⃣ Carnes vermelhas ou brancas
        Ricas em proteínas e ferro.

        ### Por que 100g?
        Segue a **RDC 429/2020** e **IN 75/2020 da Anvisa**.
        """)

    painel = PainelAlimentos()
    painel.cadastrar()
    painel.listar()

    st.markdown("---")

    refeicao = PainelRefeicao()
    refeicao.montar()


if __name__ == "__main__":
    interface_prototipo()
