from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# In-memory progress tracking
progress = {
    "percentage": 0,
    "status": ""
}

def update_progress(percent, status):
    global progress
    progress["percentage"] = percent
    progress["status"] = status
    logging.info(f"Progresso atualizado: {percent}% - Status: {status}")

@app.route('/')
def index():
    logging.info("Rota / acessada")
    return render_template('index.html')

@app.route('/get_progress', methods=['GET'])
def get_progress():
    logging.info(f"Progresso atual enviado: {progress}")
    return jsonify(progress)

@app.route('/get_qualities', methods=['POST'])
def get_qualities():
    try:
        url = request.json.get('url')
        if not url:
            logging.warning("URL inválida recebida na rota /get_qualities")
            return jsonify({"error": "URL inválida."}), 400

        logging.info(f"Extraindo qualidades para URL: {url}")
        ydl_opts = {
            'quiet': True,
            'simulate': True,
            'noplaylist': True,
            'forcejson': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get('formats', [])
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
    try:
        data = request.json
        url = data.get('url')
        format_id = data.get('quality')

        if not url or not format_id:
            logging.warning("Dados insuficientes fornecidos para o download")
            return jsonify({"error": "Dados insuficientes fornecidos."}), 400

        logging.info(f"Iniciando download para URL: {url}, formato: {format_id}")
        output_path = './downloads/%(title)s.%(ext)s'
        ydl_opts = {
            'format': format_id,
            'outtmpl': output_path,
            'progress_hooks': [
                lambda d: update_progress(
                    int(d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100),
                    d['status']
                )
            ]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        logging.info("Download concluído com sucesso")

        # Enviar o arquivo como resposta
        return send_file(filename, as_attachment=True)

    except Exception as e:
        logging.error(f"Erro ao realizar o download: {e}")
        return jsonify({"error": f"Erro ao realizar o download: {str(e)}"}), 500

if __name__ == '__main__':
    logging.info("Iniciando aplicação Flask")
    app.run(debug=True, host='0.0.0.0')
