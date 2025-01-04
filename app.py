from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import logging

# Configuração de logging para exibir mensagens no console
logging.basicConfig(level=logging.DEBUG)

# Instância do aplicativo Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições de outras origens

# Variável global para rastrear o progresso do download
progress = {
    "percentage": 0,  # Percentual do progresso
    "status": ""   # Status atual do download
}

def update_progress(percent, status):
    """
    Atualiza a variável global de progresso com o percentual e o status fornecidos.
    """
    global progress
    progress["percentage"] = percent
    progress["status"] = status
    logging.info(f"Progresso atualizado: {percent}% - Status: {status}")

@app.route('/')
def index():
    """
    Rota principal que renderiza a página inicial.
    """
    logging.info("Rota / acessada")
    return render_template('index.html')

@app.route('/get_progress', methods=['GET'])
def get_progress():
    """
    Rota para obter o progresso atual do download.
    """
    logging.info(f"Progresso atual enviado: {progress}")
    return jsonify(progress)

@app.route('/get_qualities', methods=['POST'])
def get_qualities():
    """
    Rota para obter as qualidades disponíveis para um vídeo do YouTube.
    """
    try:
        url = request.json.get('url')
        if not url:
            logging.warning("URL inválida recebida na rota /get_qualities")
            return jsonify({"error": "URL inválida."}), 400

        logging.info(f"Extraindo qualidades para URL: {url}")
        ydl_opts = {
            'quiet': True,  # Suprime logs detalhados
            'simulate': True,  # Simula o download sem baixar nada
            'noplaylist': True,  # Ignora listas de reprodução
            'forcejson': True,  # Retorna os metadados como JSON
            'cookiefile': './cookies.txt'  # Caminho para o arquivo de cookies
        }

        # Extrai informações sobre o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get('formats', [])  # Obtém as opções de formato
        qualities = [
            {
                'format_id': f['format_id'],
                'resolution': f.get('resolution', 'N/A'),
                'ext': f['ext'],
                'filesize': f.get('filesize', 'Desconhecido')
            } for f in formats if f.get('format_id')
        ]

        logging.info(f"Qualidades extraídas com sucesso: {qualities}")
        return jsonify(qualities)
    except Exception as e:
        logging.error(f"Erro ao carregar qualidades: {e}")
        return jsonify({"error": f"Erro ao carregar qualidades: {str(e)}"}), 500

@app.route('/download', methods=['POST'])
def download():
    """
    Rota para baixar o vídeo do YouTube com a qualidade selecionada.
    """
    try:
        data = request.json
        url = data.get('url')  # URL do vídeo
        format_id = data.get('quality')  # ID do formato selecionado

        if not url or not format_id:
            logging.warning("Dados insuficientes fornecidos para o download")
            return jsonify({"error": "Dados insuficientes fornecidos."}), 400

        logging.info(f"Iniciando download para URL: {url}, formato: {format_id}")
        output_path = './downloads/%(title)s.%(ext)s'  # Caminho para salvar o arquivo
        ydl_opts = {
            'format': format_id,  # Define o formato do download
            'outtmpl': output_path,  # Modelo de nome do arquivo
            'cookiefile': './cookies.txt',  # Caminho para o arquivo de cookies
            'progress_hooks': [
                lambda d: update_progress(
                    int(d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100),
                    d['status']
                )
            ]
        }

        # Realiza o download do vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)  # Obtém o nome do arquivo baixado

        logging.info("Download concluído com sucesso")

        # Envia o arquivo como resposta para o cliente
        return send_file(filename, as_attachment=True)

    except Exception as e:
        logging.error(f"Erro ao realizar o download: {e}")
        return jsonify({"error": f"Erro ao realizar o download: {str(e)}"}), 500

if __name__ == '__main__':
    """
    Inicializa o servidor Flask.
    """
    logging.info("Iniciando aplicação Flask")
    app.run(debug=True, host='0.0.0.0')
