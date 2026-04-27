import sys
import os
import json
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, send_file, render_template, jsonify
from gerar_relatorio import gerar_pdf

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar_pdf", methods=["POST"])
def endpoint_gerar_pdf():
    try:
        dados = request.get_json(force=True)
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
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port, debug=False)
