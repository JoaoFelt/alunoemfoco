from flask import Flask, render_template, request, send_file
import pandas as pd
import sqlite3
import io

app = Flask(__name__)

# =========================
# CONEXÃO SQLITE
# =========================

def get_connection():
    return sqlite3.connect("academico.db")


# =========================
# PÁGINA PRINCIPAL
# =========================

@app.route("/")
def index():

    conn = get_connection()

    # =========================
    # BUSCA BASE
    # =========================

    query = """
        SELECT *
        FROM reprovacoes
        WHERE Situacao = 'Reprovacao'
    """

    reprovados = pd.read_sql_query(query, conn)

    # =========================
    # FILTRO CURSO
    # =========================

    cursos = sorted(
        reprovados["Curso"]
        .dropna()
        .unique()
    )

    curso = request.args.get(
        "curso",
        "Todos"
    )

    if curso != "Todos":

        reprovados = reprovados[
            reprovados["Curso"] == curso
        ]

    # =========================
    # FILTRO SEMESTRE
    # =========================

    semestres = sorted(
        reprovados["Semestre"]
        .dropna()
        .unique()
    )

    semestre = request.args.get(
        "semestre",
        "Todos"
    )

    if semestre != "Todos":

        reprovados = reprovados[
            reprovados["Semestre"] == semestre
        ]

    # =========================
    # BUSCA ALUNO
    # =========================

    alunos = sorted(
        reprovados["Estudante"]
        .dropna()
        .unique()
    )

    aluno = request.args.get(
        "aluno",
        ""
    )

    dados_aluno = None

    if aluno:

        dados_aluno = reprovados[
            reprovados["Estudante"] == aluno
        ][[
            "Curso",
            "Semestre",
            "Unidade Curricular Pendente",
            "Situacao"
        ]]

    # =========================
    # BUSCA DISCIPLINA
    # =========================

    disciplinas = sorted(
        reprovados[
            "Unidade Curricular Pendente"
        ]
        .dropna()
        .unique()
    )

    disciplina = request.args.get(
        "disciplina",
        ""
    )

    dados_disciplina = None

    if disciplina:

        dados_disciplina = reprovados[
            reprovados[
                "Unidade Curricular Pendente"
            ] == disciplina
        ][[
            "Curso",
            "Estudante",
            "Semestre",
            "Situacao"
        ]]

    # =========================
    # ESTATÍSTICAS
    # =========================

    reprovacoes_disc = (
        reprovados[
            "Unidade Curricular Pendente"
        ]
        .value_counts()
        .reset_index()
    )

    reprovacoes_disc.columns = [
        "Disciplina",
        "Reprovações"
    ]

    reprovacoes_alunos = (
        reprovados[
            "Estudante"
        ]
        .value_counts()
        .reset_index()
    )

    reprovacoes_alunos.columns = [
        "Estudante",
        "Reprovações"
    ]

    conn.close()

    return render_template(
        "index.html",

        cursos=cursos,
        curso=curso,

        semestres=semestres,
        semestre=semestre,

        alunos=alunos,
        aluno=aluno,

        disciplinas=disciplinas,
        disciplina=disciplina,

        dados_aluno=(

            dados_aluno.to_dict(
                orient="records"
            )

            if dados_aluno is not None
            else None
        ),

        dados_disciplina=(

            dados_disciplina.to_dict(
                orient="records"
            )

            if dados_disciplina is not None
            else None
        ),

        reprovacoes_disc=(

            reprovacoes_disc.to_dict(
                orient="records"
            )
        ),

        reprovacoes_alunos=(

            reprovacoes_alunos.to_dict(
                orient="records"
            )
        )
    )


# =========================
# EXPORTAR CSV ALUNOS
# =========================

@app.route("/download/alunos")
def download_alunos():

    conn = get_connection()

    query = """
        SELECT
            Estudante,
            [Unidade Curricular Pendente],
            Situacao,
            Semestre
        FROM reprovacoes
        WHERE Situacao = 'Reprovacao'
    """

    csv_alunos = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    output = io.StringIO()

    csv_alunos.to_csv(
        output,
        index=False
    )

    mem = io.BytesIO()

    mem.write(
        output.getvalue().encode("utf-8")
    )

    mem.seek(0)

    return send_file(
        mem,
        mimetype="text/csv",
        as_attachment=True,
        download_name="reprovacoes_alunos.csv"
    )


# =========================
# EXPORTAR CSV DISCIPLINAS
# =========================

@app.route("/download/disciplinas")
def download_disciplinas():

    conn = get_connection()

    query = """
        SELECT
            [Unidade Curricular Pendente],
            Estudante,
            Situacao,
            Semestre
        FROM reprovacoes
        WHERE Situacao = 'Reprovacao'
    """

    csv_disc = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    output = io.StringIO()

    csv_disc.to_csv(
        output,
        index=False
    )

    mem = io.BytesIO()

    mem.write(
        output.getvalue().encode("utf-8")
    )

    mem.seek(0)

    return send_file(
        mem,
        mimetype="text/csv",
        as_attachment=True,
        download_name="reprovacoes_disciplinas.csv"
    )


# =========================
# INICIAR
# =========================

if __name__ == "__main__":
    app.run(debug=True)