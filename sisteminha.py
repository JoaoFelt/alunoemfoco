import streamlit as st
import pandas as pd

st.set_page_config(page_title="Relatório de Reprovações", layout="wide")
st.title("📊 Relatório Interativo de Reprovações")

# Lê os dados
df = pd.read_csv("trypa5.csv", sep=",")
reprovados = df[df["Situacao"] == "Reprovacao"]

st.markdown("### 📌 Filtros interativos")

# Filtro por curso
cursos_disponiveis = sorted(reprovados["Curso"].dropna().unique())
curso_selecionado = st.selectbox("🎓 Filtrar por curso", ["Todos"] + cursos_disponiveis)

# Aplica o filtro se necessário
if curso_selecionado != "Todos":
    reprovados = reprovados[reprovados["Curso"] == curso_selecionado]

semestres = sorted(reprovados["Semestre"].dropna().unique())
semestre_selecionado = st.selectbox("📆 Filtrar por semestre", ["Todos"] + semestres)
if semestre_selecionado != "Todos":
    reprovados = reprovados[reprovados["Semestre"] == semestre_selecionado]


col1, col2 = st.columns(2)

# 🔍 Por aluno
with col1:
    st.subheader("👨‍🎓 Buscar por aluno")
    lista_alunos = sorted(reprovados["Estudante"].dropna().unique())
    aluno_escolhido = st.selectbox("Escolha um aluno", lista_alunos)

    if aluno_escolhido:
        dados_aluno = reprovados[reprovados["Estudante"] == aluno_escolhido][
            ["Curso", "Semestre", "Unidade Curricular Pendente", "Situacao"]
        ]
        st.write(f"Reprovações de **{aluno_escolhido}**:")
        st.dataframe(dados_aluno)

# 🔍 Por disciplina
with col2:
    st.subheader("📚 Buscar por disciplina")
    lista_disciplinas = sorted(reprovados["Unidade Curricular Pendente"].dropna().unique())
    disciplina_escolhida = st.selectbox("Escolha uma disciplina", lista_disciplinas)

    if disciplina_escolhida:
        dados_disciplina = reprovados[
            reprovados["Unidade Curricular Pendente"] == disciplina_escolhida
        ][["Curso","Estudante", "Semestre", "Situacao"]]
        st.write(f"Alunos reprovados em **{disciplina_escolhida}**:")
        st.dataframe(dados_disciplina)

# 🔢 Estatísticas adicionais
st.markdown("---")
st.subheader("📈 Estatísticas gerais de reprovações")

col3, col4 = st.columns(2)

# 📉 Disciplinas com mais reprovações
with col3:
    st.markdown("#### 📌 Disciplinas com mais reprovações")
    reprovacoes_disc = (
        reprovados["Unidade Curricular Pendente"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Disciplina", "Unidade Curricular Pendente": "Reprovações"})
    )
    st.dataframe(reprovacoes_disc)

# 📉 Alunos com mais reprovações
with col4:
    st.markdown("#### 📌 Alunos com mais reprovações")
    reprovacoes_alunos = (
        reprovados["Estudante"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Estudante", "Estudante": "Reprovações"})
    )
    st.dataframe(reprovacoes_alunos)


# 📥 Exportação dos dados
st.markdown("---")
st.subheader("📥 Exportar dados completos")

col5, col6 = st.columns(2)

with col5:
    csv_alunos = reprovados[["Estudante", "Unidade Curricular Pendente", "Situacao", "Semestre"]]
    csv_bytes_alunos = csv_alunos.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar relatório por aluno",
        data=csv_bytes_alunos,
        file_name="reprovacoes_por_aluno.csv",
        mime="text/csv"
    )

with col6:
    csv_disciplinas = reprovados[["Unidade Curricular Pendente", "Estudante", "Situacao", "Semestre"]]
    csv_bytes_disciplinas = csv_disciplinas.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar relatório por disciplina",
        data=csv_bytes_disciplinas,
        file_name="reprovacoes_por_disciplina.csv",
        mime="text/csv"
    )
