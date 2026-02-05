# Projeto de Análise de Reclamações e Sentimento

Projeto **educacional**, desenvolvido em parceria (backend + frontend), com o objetivo de estudar:

- Criação de APIs com **Flask**
- Leitura e filtragem de dados com **Pandas**
- Análise de sentimento usando **Transformers (Hugging Face)**
- Integração backend + frontend

O backend expõe rotas que permitem consultar reclamações de uma empresa a partir de um arquivo CSV e realizar uma análise de sentimento sobre essas reclamações.

---

## 📁 Estrutura do Projeto

```
BACK-END/
│
├── analyzer/
│   ├── __init__.py
│   └── analyzer.py
│
├── data/
│   └── basecompleta2025-12.csv
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.10+**
- **Flask** — API REST
- **Pandas** — Manipulação de dados
- **Transformers (Hugging Face)** — Análise de sentimento
- **nlptown/bert-base-multilingual-uncased-sentiment** — Modelo de NLP

---

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone <url-do-repositorio>
cd BACK-END
```

### 2️⃣ Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

> ⚠️ **Observação:** O primeiro uso da análise de sentimento pode demorar, pois o modelo será baixado automaticamente.

### 4️⃣ Baixar o arquivo de dados

Para baixar o arquivo com os dados acesse o link abaixo:

https://dados.mj.gov.br/dataset/reclamacoes-do-consumidor-gov-br

> É recomendado baixar a versão mais recente, porém fica ao critério do usuário.

Após baixar o arquivo, garanta que ele esteja na pasta `data`. 

```
data/basecompleta2025-12.csv
```

Caso o nome seja diferente, atualizar a variavél `CSV_PATH` no arquivo `app.py`.

Também é importante garantir que ele possui, no mínimo, as colunas:

- `Nome Fantasia`
- `Problema`

### 5️⃣ Executar a aplicação

```bash
python app.py
```

A API ficará disponível em:

```
http://localhost:5000
```

---

## 📡 Documentação da API

### 🔹 POST `/complaints`

Retorna uma amostra de reclamações de uma empresa específica.

#### 📥 Request

- **Method:** `POST`
- **Content-Type:** `application/json`

```json
{
  "EMPRESA_ALVO": "Nome da Empresa"
}
```

#### 📤 Response (200)

```json
{
  "data": [
    {
      "Nome Fantasia": "Empresa Exemplo",
      "Problema": "Descrição da reclamação",
      "...": "Outros campos do CSV"
    }
  ]
}
```

#### ❌ Response (404)

```json
{
  "error": "Erro ao consultar empresa",
  "detail": "Nenhuma reclamação encontrada para a empresa 'Empresa X'."
}
```

---

### 🔹 POST `/analyze`

Executa a **análise de sentimento** das reclamações de uma empresa e retorna um índice de satisfação.

#### 📥 Request

```json
{
  "EMPRESA_ALVO": "Nome da Empresa"
}
```

#### 📤 Response (200)

```json
{
  "empresa": "Nome da Empresa",
  "classificacao": "positiva | neutra | negativa",
  "indice_satisfacao": "0.42"
}
```

#### 📊 Como funciona a classificação

- O modelo retorna notas de **1 a 5 estrelas**
- Conversão usada:
  - **1–2 estrelas:** Negativo
  - **3 estrelas:** Neutro
  - **4–5 estrelas:** Positivo

O **índice de satisfação** é calculado como:

```
(quantidade_positivos - quantidade_negativos) / total
```

---

## 🧠 Observações Técnicas

- A amostra padrão é limitada a **200 reclamações** por empresa
- O filtro por empresa usa `str.contains`, portanto não exige nome exato
- O projeto não possui autenticação, pois é voltado exclusivamente para fins educacionais

---





## 📄 Licença

Projeto de uso livre para estudos e aprendizado.

#
