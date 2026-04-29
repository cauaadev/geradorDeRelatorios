<<<<<<< HEAD
import os
import sys
import io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file, render_template, jsonify, make_response
from service.PDFGenerator import PDFGenerator
from db.database import get_session, criar_tabelas
from service.PsicologoService import PsicologoService
from service.PacienteService import PacienteService
from db.database import Base

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

criar_tabelas()
=======
import sys
import os
import json
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, send_file, render_template, jsonify
from gerar_relatorio import gerar_pdf

app = Flask(__name__, template_folder="templates")
>>>>>>> 92acb7aa9806cf0dcdd4818fdfb6dcbcf92f40e8

@app.route("/")
def index():
    return render_template("index.html")

<<<<<<< HEAD

@app.route("/psicologos", methods=["GET"])
def listar_psicologos():
    with get_session() as session:
        return jsonify(PsicologoService(session).listar())

@app.route("/psicologos", methods=["POST"])
def cadastrar_psicologo():
    try:
        dados = request.get_json(force=True)
        with get_session() as session:
            psicologo = PsicologoService(session).cadastrar(dados)
            print(psicologo)
            return jsonify(psicologo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/psicologos/<int:id>", methods=["DELETE"])
def deletar_psicologo(id: int):
    with get_session() as session:
        ok = PsicologoService(session).deletar(id)
        return jsonify({"ok": ok})


@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    with get_session() as session:
        return jsonify(PacienteService(session).listar())

@app.route("/pacientes", methods=["POST"])
def cadastrar_paciente():
    try:
        dados = request.get_json(force=True)
        with get_session() as session:
            paciente = PacienteService(session).cadastrar(dados)
            return jsonify(paciente), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/pacientes/<int:id>", methods=["DELETE"])
def deletar_paciente(id: int):
    with get_session() as session:
        ok = PacienteService(session).deletar(id)
        return jsonify({"ok": ok})


=======
>>>>>>> 92acb7aa9806cf0dcdd4818fdfb6dcbcf92f40e8
@app.route("/gerar_pdf", methods=["POST"])
def endpoint_gerar_pdf():
    try:
        dados = request.get_json(force=True)
<<<<<<< HEAD

        if not dados:
            return jsonify({"error": "JSON inválido"}), 400

        pdf_bytes    = PDFGenerator(dados).gerar()
        nomeProfissional = dados['psicologo']['nome'].split()[0]
        titulo = dados['psicologo']['titulo'].split()[0]
        paciente = dados['paciente']['nome'].split()[0]

        nome_arquivo = f"relatorio{titulo}_{nomeProfissional}_{paciente}.pdf"
        

        response = make_response(send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=nome_arquivo
        ))
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

=======
        if not dados:
            return jsonify({"error": "JSON inválido"}), 400

        pdf_bytes = gerar_pdf(dados)
        nome_arquivo = f"relatorio_{dados['paciente']['nome'].split()[0]}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=nome_arquivo,
        )
>>>>>>> 92acb7aa9806cf0dcdd4818fdfb6dcbcf92f40e8
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

<<<<<<< HEAD

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port, debug=True)
=======
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port, debug=False)
>>>>>>> 92acb7aa9806cf0dcdd4818fdfb6dcbcf92f40e8
