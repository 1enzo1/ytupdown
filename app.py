from flask import Flask, render_template, request, jsonify, send_file
import os
from yt_dlp import YoutubeDL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

progress_data = {'status': 'idle', 'progress': 0.0, 'eta': ''}
server_status = {'running': True, 'tasks': []}

@app.route('/')
def home():
    global progress_data
    progress_data = {'status': 'idle', 'progress': 0.0, 'eta': ''}
    return render_template('index.html')

@app.route('/list_formats', methods=['POST'])
def list_formats():
    url = request.json.get('url')
    print(f"Recebido URL para listagem de formatos: {url}")
    if not url:
        print("Erro: URL não fornecida")
        return jsonify({'error': 'URL não fornecida'}), 400

    try:
        options = {
            'quiet': True
        }
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [{
                'format_id': f['format_id'],
                'resolution': f.get('format_note', 'Desconhecido'),
                'ext': f['ext']
            } for f in info.get('formats', []) if f.get('video_ext') != 'none']

        print(f"Formatos disponíveis: {formats}")
        return jsonify({'formats': formats})

    except Exception as e:
        print(f"Erro ao listar formatos: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_progress', methods=['GET'])
def download_progress():
    return jsonify(progress_data)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    format_id = request.json.get('format_id', 'best')  # Obtém o ID do formato solicitado
    print(f"Recebido URL: {url}, Formato: {format_id}")
    if not url:
        print("Erro: URL não fornecida")
        return jsonify({'error': 'URL não fornecida'}), 400

    def progress_hook(d):
        if d['status'] == 'downloading':
            progress_data['status'] = 'downloading'
            progress_data['progress'] = d['_percent_str'].strip()
            progress_data['eta'] = d.get('eta', 'Desconhecido')
            server_status['tasks'].append(f"Baixando: {d['_percent_str'].strip()} ETA: {d.get('eta', 'Desconhecido')}s")
        elif d['status'] == 'finished':
            progress_data['status'] = 'finished'
            progress_data['progress'] = 100.0
            progress_data['eta'] = ''
            server_status['tasks'].append("Download concluído.")

    try:
        options = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': format_id,
            'progress_hooks': [progress_hook]
        }
        with YoutubeDL(options) as ydl:
            print("Iniciando o download...")
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            print(f"Download concluído: {file_path}")

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        progress_data['status'] = 'error'
        progress_data['progress'] = 0.0
        progress_data['eta'] = ''
        server_status['tasks'].append(f"Erro: {str(e)}")
        print(f"Erro ao processar o download: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def server_status_view():
    return jsonify(server_status)

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    print("Servidor iniciado em http://127.0.0.1:5000")
    app.run(debug=True)
