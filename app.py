from flask import Flask, request, jsonify
from analyzer.analyzer import read_csv_to_df, sentiment_analysis

app = Flask(__name__)

@app.route("/complaints", methods=["POST"])
def analyze():
    data = request.get_json()
    EMPRESA_ALVO = data.get("EMPRESA_ALVO")
    
    try:
        df_sample = read_csv_to_df(EMPRESA_ALVO)
    except Exception as e:
        return jsonify({
            "error": "Erro ao consultar empresa",
            "detail": str(e)
        }), 404

    return jsonify({
        "data": df_sample.to_dict(orient="records"),
    })

@app.route("/analyze", methods=["POST"])
def sentiment():
    data = request.get_json()
    EMPRESA_ALVO = data.get("EMPRESA_ALVO")

    try:
        df_sample = read_csv_to_df(EMPRESA_ALVO)
    except Exception as e:
        return jsonify({
            "error": "Erro ao consultar empresa",
            "detail": str(e)
        }), 404
     
    resultados = sentiment_analysis(df_sample)

    return jsonify({
        "empresa": EMPRESA_ALVO,
        "classificacao": resultados["classificacao"],
        "indice_satisfacao": resultados["indice_satisfacao"]
    })

if __name__ == "__main__":
    app.run(debug=False)


