import pandas as pd
from transformers import pipeline
from pathlib import Path
from flask import jsonify

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "basecompleta2025-12.csv"
COL_EMPRESA = "Nome Fantasia"
COL_TEXTO = "Problema"
AMOSTRA = 200

def read_csv_to_df(EMPRESA_ALVO, AMOSTRA=AMOSTRA):
    try:
        df_raw = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

        print("Colunas disponíveis:") # para fins de debug
        print(df_raw.columns.tolist()[:40]) 

        
        df_empresa = df_raw[df_raw[COL_EMPRESA].str.contains(EMPRESA_ALVO, case=False, na=False)]
        
        if df_empresa.empty:
            raise ValueError(f"Nenhuma reclamação encontrada para a empresa '{EMPRESA_ALVO}'. Tem certeza de que o nome está correto?")

        print(f"Quantidade de reclamações encontradas para '{EMPRESA_ALVO}':", len(df_empresa))

        df_sample = df_empresa.head(AMOSTRA).copy()

        return df_sample
    
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        raise

def sentiment_analysis(df_sample):

    sentiment_model = pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )

    resultados = []

    for texto in df_sample[COL_TEXTO].fillna(""):
        sent = sentiment_model(texto)[0]
        estrelas = int(sent["label"].split()[0])
        score = sent["score"]

        if estrelas <= 2:
            sentimento = "negativo"
        elif estrelas == 3:
            sentimento = "neutro"
        else:
            sentimento = "positivo"

        resultados.append({
            "texto": texto,
            "estrelas": estrelas,
            "sentimento": sentimento,
            "confianca": score
        })

    df_sent = pd.DataFrame(resultados)

    print("\nPrévia dos resultados:")
    print(df_sent.head())
    
    total = len(df_sent)
    positivos = (df_sent["sentimento"] == "positivo").sum()
    negativos = (df_sent["sentimento"] == "negativo").sum()

    indice_satisfacao = (positivos - negativos) / total if total > 0 else 0

    return {
        "indice_satisfacao": f"{indice_satisfacao:.2f}",
        "classificacao": "positiva" if indice_satisfacao > 0 else "neutra" if indice_satisfacao == 0 else "negativa",   
    }