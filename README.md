# YouTube Video Downloader

Este projeto permite listar formatos de vídeo disponíveis e baixar vídeos do YouTube em diferentes qualidades, exibindo uma barra de progresso em tempo real durante o download.

## Requisitos

Antes de começar, certifique-se de ter instalado os seguintes pacotes:

- Python 3.8 ou superior
- `flask`
- `flask-cors`
- `yt-dlp`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/1enzo1/ytdown.git
   cd ytdown
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install flask flask-cors yt-dlp
   ```

## Como usar

1. Inicie o servidor Flask:

   ```bash
   python app.py
   ```

   O servidor estará disponível em: `http://127.0.0.1:5000`

2. Acesse a interface HTML para listar os formatos e iniciar o download.

## Endpoints

### `/`

- **Método**: `GET`
- **Descrição**: Página inicial do servidor.

### `/list_formats`

- **Método**: `POST`
- **Descrição**: Lista os formatos de vídeo disponíveis para um URL do YouTube.
- **Parâmetros**:
  - `url`: URL do vídeo do YouTube.

- **Resposta**:
  ```json
  {
    "formats": [
      {"format_id": "22", "resolution": "720p", "ext": "mp4"},
      {"format_id": "18", "resolution": "360p", "ext": "mp4"}
    ]
  }
  ```

### `/download`

- **Método**: `POST`
- **Descrição**: Faz o download de um vídeo na qualidade selecionada.
- **Parâmetros**:
  - `url`: URL do vídeo do YouTube.
  - `format_id`: ID do formato do vídeo (obtido de `/list_formats`).

- **Resposta**: Retorna o arquivo de vídeo para download.

### `/download_progress`

- **Método**: `GET`
- **Descrição**: Retorna o progresso atual do download.
- **Resposta**:
  ```json
  {
    "status": "downloading",
    "progress": "50.0%",
    "eta": "30s"
  }
  ```

## Estrutura do Projeto

```
.
├── app.py               # Código principal do servidor Flask
├── templates
│   └── index.html       # Interface HTML
├── static
│   └── styles.css       # Estilos (opcional)
├── downloads            # Pasta onde os vídeos baixados são salvos
└── README.md            # Este arquivo
```

## Observações

- Use esta ferramenta apenas para downloads legais e respeitando os termos de uso do YouTube.
- Certifique-se de que possui permissão para baixar o conteúdo.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

