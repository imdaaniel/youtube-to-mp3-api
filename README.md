# YT to MP3 API

Converta vídeos do YouTube em arquivos MP3 através de uma API simples e moderna.

## 📋 Visão Geral

YT to MP3 é uma aplicação web que permite converter vídeos do YouTube em arquivos de áudio MP3. A API foi construída com **FastAPI** para fornecer uma solução rápida, confiável e fácil de usar.

### Características

- 🎵 Conversão de vídeos YouTube para MP3
- ⚡ API rápida e responsiva (construída com FastAPI)
- 🔄 Limpeza automática de arquivos temporários
- 📱 Interface web (em desenvolvimento)
- 🛡️ Validação de URLs
- 📊 Documentação automática (Swagger)

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.10+
- FFmpeg instalado
- pip

### Instalação

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd yt-to-mp3/api
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Certifique-se que o FFmpeg está instalado**

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
```bash
# Via Chocolatey
choco install ffmpeg
# Ou download manual: https://ffmpeg.org/download.html
```

### Execução

```bash
python3 main.py
```

A API estará disponível em: `http://127.0.0.1:8000`

**Documentação interativa:** http://127.0.0.1:8000/docs

---

## 📡 Uso da API

### Endpoint: POST `/api/download`

Baixa um vídeo do YouTube e retorna o arquivo MP3.

#### Request

```bash
curl -X POST http://127.0.0.1:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  -o musica.mp3
```

**Body (JSON):**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

#### Response

- **Status 200:** Arquivo MP3 em stream
  - Content-Type: `audio/mpeg`
  - Content-Disposition: `attachment; filename="titulo.mp3"`

- **Status 400:** URL inválida ou não é do YouTube
  ```json
  {
    "detail": "URL inválida ou não é um vídeo do YouTube"
  }
  ```

- **Status 500:** Erro ao processar
  ```json
  {
    "detail": "Erro ao baixar vídeo: [mensagem de erro]"
  }
  ```

### Exemplo com JavaScript/Fetch

```javascript
const downloadVideo = async (url) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) throw new Error('Download failed');

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `audio-${Date.now()}.mp3`;
    a.click();
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

---

## 📁 Estrutura do Projeto

```
yt-to-mp3/
├── api/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py              # Configurações centralizadas
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── downloader.py      # Lógica de download (yt-dlp)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── download.py        # Endpoint POST /api/download
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── download.py        # Schema DownloadRequest (Pydantic)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── cleanup.py         # Limpeza automática de arquivos
│   │   │   └── youtube.py         # Orquestração do download
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── id_generator.py    # Geração de IDs únicos
│   │       └── validators.py      # Validação de URLs
│   ├── docs/
│   │   └── sprints/
│   │       └── SPRINT-1-SERVE-API.md
│   ├── main.py                    # App factory + servidor
│   ├── transform.py               # Wrapper de compatibilidade
│   ├── requirements.txt           # Dependências
│   └── README.md                  # Este arquivo
└── frontend/                      # (em desenvolvimento)
    ├── contentScript.js
    ├── manifest.json
    └── popup.html
```

---

## 🛠️ Stack Técnico

### Backend
- **FastAPI** - Framework web assíncrono
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validação de dados
- **yt-dlp** - Download de vídeos YouTube
- **APScheduler** - Agendamento de tarefas (limpeza de arquivos)

### Frontend (em desenvolvimento)
- JavaScript vanilla
- Chrome Extension API

---

## 🔧 Configuração

Edite `app/config.py` para ajustar:

```python
# Limpeza automática
CLEANUP_INTERVAL_MINUTES = 2    # A cada 2 minutos
FILE_TTL_SECONDS = 300          # Arquivos com >5min são deletados

# Download
SOCKET_TIMEOUT = 60              # Timeout em segundos
RETRIES = 5                      # Tentativas de download
FRAGMENT_RETRIES = 5             # Tentativas de fragmentos
```

---

## 📊 Roadmap de Sprints

### ✅ Sprint 1: API de Download Básica
**Status:** COMPLETO ✅

**Objetivos:**
- [x] Criar endpoint FastAPI para receber URL do YouTube
- [x] Validar URLs (verificar se é YouTube)
- [x] Fazer download do áudio usando yt-dlp
- [x] Converter para MP3 (FFmpeg)
- [x] Retornar arquivo ao cliente via stream
- [x] Gerenciar arquivos temporários
- [x] Limpeza automática de arquivos antigos

**Entregas:**
- API funcional em `/api/download`
- Documentação automática em `/docs`
- Suporte a vídeos YouTube regulares
- Scheduler para limpeza a cada 2 minutos

**Tecnologias:**
- FastAPI + Uvicorn
- yt-dlp
- APScheduler
- Pydantic

---

### 🚀 Sprint 2: Suporte a YouTube Shorts
**Status:** EM PLANEJAMENTO 📋

**Objetivos:**
- [ ] Detectar se é um YouTube Short
- [ ] Adaptar estratégia de download para Shorts
- [ ] Testar compatibilidade com URLs curtas (youtu.be)
- [ ] Validar qualidade de áudio para vídeos curtos
- [ ] Documentar diferenças no comportamento

**Descrição:**
YouTube Shorts têm características diferentes de vídeos regulares:
- Comprimento máximo de 60 segundos
- URLs curtas (youtu.be/...)
- Diferentes clients de player
- Possíveis restrições de acesso

Esta sprint irá garantir que a API funcione perfeitamente com Shorts.

**Tecnologias esperadas:**
- Atualização de `app/utils/validators.py`
- Novos testes em `app/core/downloader.py`
- Documentação em `app/routes/download.py`

---

### 📅 Sprint 3+: Roadmap Futuro
- [ ] Interface web (frontend)
- [ ] Suporte a playlists
- [ ] Histórico de downloads
- [ ] Autenticação de usuários
- [ ] Banco de dados (armazenar metadados)
- [ ] Cache de áudios populares
- [ ] API de busca/recomendações
- [ ] Integração com redes sociais

---

## 🧪 Testes

*Em breve será adicionada suite de testes*

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=app
```

---

## 📝 Logging

A aplicação registra eventos importantes:

```
🚀 API iniciada
⏱️  Scheduler iniciado - limpeza a cada 2 minutos
[video_id] Iniciando download: https://...
[video_id] Download concluído: musica.mp3
[CLEANUP] Pasta deletada: timestamp_hash
🛑 API desligada
```

---

## ⚠️ Limitações Conhecidas

1. **Tamanho de arquivo:** YouTube Shorts podem ter qualidade reduzida
2. **Rate limiting:** YouTube pode bloquear após muitos downloads
3. **Autenticação:** Alguns vídeos privados não podem ser baixados
4. **Geo-restrição:** Alguns vídeos são bloqueados por país

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### Erro: "HTTP Error 403: Forbidden"
Tente atualizar yt-dlp:
```bash
pip install --upgrade yt-dlp
```

### FFmpeg não encontrado
Certifique-se que está instalado e no PATH:
```bash
ffmpeg -version
```

### Pasta `temp/` crescendo demais
O scheduler de limpeza deve rodar a cada 2 minutos. Verifique se está ativo nos logs.

---

## 📄 Licença

Este projeto é fornecido como-está para fins educacionais.

---

## 👨‍💻 Desenvolvimento

### Adicionar novo endpoint

1. Crie `app/routes/seu_endpoint.py`
2. Crie schema em `app/schemas/seu_endpoint.py` (se necessário)
3. Adicione serviço em `app/services/seu_endpoint.py` (se necessário)
4. Registre em `main.py`:

```python
from app.routes.seu_endpoint import router as seu_endpoint_router
app.include_router(seu_endpoint_router)
```

### Arquitetura

Cada camada tem responsabilidade clara:

- **Routes:** Expõem endpoints HTTP
- **Schemas:** Validam dados com Pydantic
- **Services:** Implementam lógica de negócio
- **Core:** Funcionalidades de infraestrutura
- **Utils:** Funções genéricas e reutilizáveis
- **Config:** Configurações centralizadas

---

## 📞 Suporte

Para reportar bugs ou sugerir features, abra uma issue no repositório.

---

**Última atualização:** 30 de janeiro de 2026
