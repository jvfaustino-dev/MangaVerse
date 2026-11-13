#python -m pip install flask requests
#py -m pip install --upgrade certifi requests

from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import requests

app = Flask(__name__)

# Pasta onde estão o HTML e o servidor
PASTA = Path(__file__).resolve().parent


# Abre a página principal do MangaVerse
@app.route("/")
def inicio():
    return send_from_directory(PASTA, "index.html")


# Faz a ponte entre o HTML e a API do MangaDex
@app.route("/api/manga")
def pesquisar_mangas():

    titulo = request.args.get("title", "").strip()

    if not titulo:
        return jsonify({
            "error": "Digite o nome de um mangá."
        }), 400

    # Parâmetros enviados ao MangaDex
    parametros = [
        ("title", titulo),
        ("limit", "10"),
        ("contentRating[]", "safe"),
        ("contentRating[]", "suggestive")
    ]

    cabecalhos = {
        "User-Agent": "MangaVerse/1.0"
    }

    try:
        resposta = requests.get(
            "https://api.mangadex.org/manga",
            params=parametros,
            headers=cabecalhos,
            timeout=20,
            verify=str(PASTA / "mangadex-ca-bundle.pem")
        )

        resposta.raise_for_status()

        # Devolve os resultados para o JavaScript
        return jsonify(resposta.json())

    except requests.HTTPError as erro:
        print("\n=== ERRO RETORNADO PELO MANGADEX ===")
        print("Status HTTP:", resposta.status_code)
        print("Resposta:", resposta.text[:1000])

        return jsonify({
            "error": "O MangaDex retornou um erro.",
            "status": resposta.status_code
        }), 502

    except requests.RequestException as erro:
        print("\n=== ERRO DE CONEXÃO ===")
        print("Detalhes:", repr(erro))

        return jsonify({
            "error": "Não foi possível conectar ao MangaDex."
        }), 502

    except requests.RequestException as erro:
        print("Erro de conexão:", erro)

        return jsonify({
            "error": "Não foi possível conectar ao MangaDex."
        }), 502


if __name__ == "__main__":
    print("MangaVerse iniciado!")
    print("Acesse: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )