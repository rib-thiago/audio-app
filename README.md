# 🎧 Audio-App: Caixa de Ferramentas de Áudio com FastAPI

Este projeto é uma aplicação web construída com **FastAPI** que oferece uma série de ferramentas para manipulação de arquivos de áudio. A aplicação permite realizar diversas operações em áudios, como conversão de formatos, extração de trechos, transcrição, amplificação, e muito mais. É um projeto em desenvolvimento, ideal para quem deseja explorar o FastAPI e aprimorar habilidades em frontend.

## 🚀 Funcionalidades

- [X] **🎼 Conversão de Formatos**: Converta arquivos de áudio entre diferentes formatos (MP3, WAV, etc.).
- [ ] **✂️ Extração de Trechos**: Selecione e extraia partes específicas do áudio.
- [ ] **📝 Transcrição**: Transcreva o áudio em texto.
- [ ] **🔊 Ganho de Volume**: Aumente ou diminua o volume do áudio.
- [ ] **🔗 União de Áudios**: Una dois ou mais arquivos de áudio em um único arquivo.


## 📦 Dependências Utilizadas 

- **FastAPI**: Framework web moderno e rápido para construção de APIs com Python.
- **ffmpeg-python**: Biblioteca para manipulação de áudio.
- **Jinja2**: Motor de template usado para renderizar páginas HTML.

## 🏃 Como Rodar o Projeto

1. **Clone o repositório**:
    
    ```bash
    git clone https://github.com/rib-thiago/audio-app
    cd audio-app
    ```

2. **Instale as dependências**:
    
    ```bash
    poetry install
    ```

3. **Execute a aplicação**:
    
    ```bash
    poetry run uvicorn main:app --reload
    ```

4. **Acesse a aplicação**:
    Abra o navegador e vá para `http://localhost:8000`.

## 🤝 Contribuição

Sinta-se à vontade para abrir issues e enviar pull requests. Toda ajuda é bem-vinda!

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

Feito por [Thiago Ribeiro](https://github.com/rib-thiago)