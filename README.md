# Projeto YouTube Downloader

Este projeto permite realizar o download de vídeos do YouTube diretamente pelo navegador utilizando um servidor Flask.

## Estrutura do Projeto

```
.
├── app.py               # Código principal do servidor Flask
├── templates
│   └── index.html       # Interface HTML
├── static
│   └── styles.css       # Estilos
├── downloads            # Pasta temporária para downloads locais
├── README.md            # Este arquivo
├── requirements.txt     # Dependências do projeto
├── runtime.txt          # Versão do Python especificada
```

## Instalação e Execução Local

### 1. Requisitos
- Python 3.12
- pip (gerenciador de pacotes do Python)

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o Servidor Flask

```bash
python app.py
```

O servidor estará disponível em `http://127.0.0.1:5000`.

## Deploy no Render

### 1. Especifique a Versão do Python
Crie o arquivo `runtime.txt` com o seguinte conteúdo:
```
python-3.12.0
```

### 2. Configure o Repositório no Render
- Escolha **Web Services** ao criar o serviço.
- No campo **Start Command**, insira:
  ```bash
  gunicorn app:app
  ```
- No campo **Build Command**, insira:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Configuração da Porta
Certifique-se de que o Flask usa a porta definida pelo Render com o seguinte trecho no `app.py`:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### 4. Upload do Arquivo para o Cliente
O `app.py` já está configurado para enviar o vídeo diretamente para o cliente. Ele usa o método `send_file` para que o vídeo não seja armazenado permanentemente no servidor.

## Testes Locais

1. Insira o link do vídeo no campo de entrada.
2. Escolha a qualidade desejada.
3. Clique em **Baixar** e o arquivo será baixado diretamente para o seu dispositivo.

---

Se você tiver dúvidas ou encontrar problemas, sinta-se à vontade para abrir uma issue no repositório!