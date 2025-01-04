# YouTube Video Downloader

Este projeto é uma aplicação simples para baixar vídeos do YouTube. Ele permite selecionar a qualidade do vídeo antes do download, utilizando o framework Flask no backend e uma interface web estilizada em dark mode.

---

## Guia Rápido para Leigos

### Passos para usar o aplicativo:

1. **Abrir o terminal**:
   - No Windows, use o Prompt de Comando (cmd) ou PowerShell.
   - No Linux/Mac, use o Terminal.

2. **Navegar até a pasta do projeto**:
   Digite o comando para entrar na pasta onde você baixou o projeto:
   ```bash
   cd <pasta-do-projeto>
   ```

3. **Executar o aplicativo**:
   No terminal, execute:
   ```bash
   python app.py
   ```
   Isso iniciará o servidor local.

4. **Abrir o navegador**:
   No navegador, acesse:
   ```
   http://127.0.0.1:5000
   ```

5. **Usar a interface**:
   - Insira o link de um vídeo do YouTube.
   - Clique em "Carregar Qualidades".
   - Escolha a qualidade e clique em "Baixar".

### Observação
- Os vídeos baixados serão salvos na pasta `downloads` dentro do projeto.
- Certifique-se de que a URL do vídeo seja válida.

---

## Estrutura do Projeto

```
.
├── app.py               # Código principal do servidor Flask
├── templates
│   └── index.html       # Interface HTML
├── static
│   └── styles.css       # Estilos em dark mode
├── downloads            # Pasta onde os vídeos baixados são salvos
└── README.md            # Documentação do projeto
```

---

## Pré-requisitos

Certifique-se de ter o seguinte instalado em sua máquina:

- **Python 3.8+**
- **pip** (gerenciador de pacotes do Python)

Além disso, instale as bibliotecas necessárias executando:
```bash
pip install flask flask-cors yt-dlp
```

---

## Executando o Aplicativo

1. **Clone o repositório ou baixe o código fonte**:
   ```bash
   git clone <link-do-repositorio>
   cd <pasta-do-projeto>
   ```

2. **Inicie o servidor Flask**:
   ```bash
   python app.py
   ```

3. **Acesse o aplicativo no navegador**:
   Abra o navegador e vá para:
   ```
   http://127.0.0.1:5000
   ```

4. **Baixando Vídeos**:
   - Insira o link do vídeo no campo indicado.
   - Clique em "Carregar Qualidades" para listar as opções de qualidade.
   - Selecione a qualidade desejada e clique em "Baixar".

---


## Problemas Conhecidos
- Alguns vídeos podem não estar disponíveis para download devido a restrições do YouTube.
- Certifique-se de que a conexão com a internet esteja estável para evitar falhas no download.

---

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests no repositório.

---

**Autor**: Enzo Luchetti
**Licença**: MIT