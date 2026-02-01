# SPRINT 2 - Video Download com Streaming Direto

## 📋 Objetivo
Adicionar suporte a download de vídeos com qualidades selecionáveis, usando streaming direto (sem armazenar em disco/memória).

## 🏗️ Arquitetura

### Fluxo de Dois Passos

#### 1️⃣ Obter Metadados e Formatos Disponíveis
```
Cliente: GET /api/formats?url=https://youtube.com/watch?v=xxx
         ↓
API: Extrai metadados com yt-dlp (download=False)
     Tempo: ~2-4 segundos
     ↓
Resposta:
{
  "title": "Video Title",
  "duration": 240,
  "uploader": "Channel Name",
  "formats": [
    {
      "format_id": "22",
      "ext": "mp4",
      "height": 720,
      "width": 1280,
      "filesize": 157286400,
      "fps": 30,
      "vcodec": "h.264",
      "acodec": "aac"
    },
    {
      "format_id": "18",
      "ext": "mp4",
      "height": 360,
      "width": 640,
      "filesize": 45000000,
      "fps": 30,
      "vcodec": "h.264",
      "acodec": "aac"
    },
    {
      "format_id": "251",
      "ext": "m4a",
      "filesize": 5242880,
      "acodec": "opus"
    }
  ]
}
```

#### 2️⃣ Fazer Download com Streaming Direto
```
Cliente: POST /api/download
         {
           "url": "https://youtube.com/watch?v=xxx",
           "format_id": "22"
         }
         ↓
API: Inicia yt-dlp com output para stdout (-o -)
     Valida formato ANTES de enviar headers
     ↓
Resposta:
HTTP 200 OK
Content-Type: video/mp4
Content-Length: 157286400
Accept-Ranges: bytes

[stream de 157MB em chunks de 64KB]

Cliente: Recebe dados
         Mostra barra: "12MB / 150MB"
         Browser/downloader suporta pause/resume
```

## 💾 Streaming Direto (Sem Disco)

### Benefícios
| Aspecto | Antes (Salvar em /temp) | Agora (Stream Direto) |
|---------|------------------------|----------------------|
| **Memória** | Alto (arquivo inteiro na RAM) | Mínimo (chunks 64KB) |
| **Disco** | Alto (copia arquivo grande) | Zero |
| **I/O** | Alto (escrita + leitura) | Só rede |
| **Velocidade** | Mais lento | ⚡ Mais rápido |
| **Espaço /temp** | Ocupado durante transfer | Nunca ocupa |
| **Concorrência** | Limita quantidade simultânea | Escalável |
| **Cleanup** | Precisa deletar arquivo | Automático |

### Fluxo de Dados
```
YouTube → yt-dlp (stdout) → Chunks 64KB → Cliente
  (stream)   (pipe)         (buffer)      (recebe em tempo real)

Sem intermediários!
Sem salvar em disco!
Memória constante!
```

## 🔄 Tratamento de Erros e Retries

### Política de Retries

**yt-dlp oferece retries nativos:**
```python
ydl_opts = {
    'fragment_retries': 10,      # Retenta cada chunk individual
    'retries': 5,                 # Retenta conexão geral
    'socket_timeout': 30,
    'skip_unavailable_fragments': False,  # Falha se fragmento não conseguir
}
```

### Cenários de Falha

#### 1. Falha ANTES do Stream (Ideal)
```
GET /api/formats → OK
POST /api/download → yt-dlp testa conexão/formato
                  → Falha ANTES de enviar HTTP 200
                  → Retorna HTTP 500 + erro específico

Cliente vê erro antes de gastar dados/tempo
```

#### 2. Falha DURANTE o Stream (Raro, mas Possível)
```
HTTP 200 enviado → Cliente começou receber dados
              ↓
yt-dlp falha no chunk 50%
              ↓
Conexão TCP fecha com erro
              ↓
Cliente recebe HTTP 206 Partial Content (navegador trata)
Cliente pode fazer retry com Range header:
  GET /download
  Range: bytes=78643200-

Continua de onde parou!
```

### Headers de Suporte a Retry
```http
HTTP/1.1 200 OK
Content-Type: video/mp4
Content-Length: 157286400
Accept-Ranges: bytes
```

Cliente (navegador/downloader) reconhece `Accept-Ranges: bytes` e oferece pausa/resume.

## 📊 Metadados Prévios

### Extração sem Download
```python
# Extrair informações da página do YouTube
# Sem fazer download do vídeo
# Tempo: 2-4 segundos

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,
    'socket_timeout': 30,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)  # ← NÃO BAIXA!
```

### Informações Disponíveis
- `title`: Título do vídeo
- `duration`: Duração em segundos
- `uploader`: Nome do canal
- `formats`: Lista de todos os formatos disponíveis
  - `format_id`: ID do formato (para yt-dlp)
  - `ext`: Extensão (mp4, m4a, webm, etc)
  - `height`/`width`: Dimensões (vídeo)
  - `filesize`: Tamanho exato em bytes
  - `fps`: Frames por segundo
  - `vcodec`/`acodec`: Codecs de vídeo/áudio
  - `abr`: Bitrate áudio
  - `vbr`: Bitrate vídeo

### Validações com Metadados
```python
# Recusar vídeos muito grandes
if filesize > 5_000_000_000:  # > 5GB
    raise HTTPException(detail="Arquivo muito grande")

# Recusar vídeos muito longos
if duration > 3600:  # > 1 hora
    raise HTTPException(detail="Vídeo muito longo")

# Filtrar formatos viáveis
available_formats = [
    f for f in formats 
    if f.get('filesize', 0) < 500_000_000  # Máx 500MB
]
```

## 📝 Mudanças de Código

### Schemas Novos

**`app/schemas/download.py`**
- `FormatInfo`: Informações de um formato específico
- `VideoMetadata`: Metadados completos do vídeo
- `DownloadRequest`: Request para download (com `format_id`)

### Serviços Novos

**`app/services/youtube.py`**
- `extract_video_metadata()`: Extrai infos sem download
- `download_video_stream()`: Faz download em stream direto

**`app/core/downloader.py`**
- `get_formats()`: Wrapper para extração de formatos
- `stream_video()`: Abre processo yt-dlp com stdout como pipe

### Endpoints

**`app/routes/download.py`**

```python
@router.get("/api/formats")
async def get_formats(url: str) -> VideoMetadata:
    """
    Retorna metadados e formatos disponíveis de um vídeo.
    
    Query Parameters:
    - url: URL do vídeo do YouTube
    
    Response:
    - Título, duração, uploader
    - Lista de formatos com tamanho exato
    
    Tempo: ~2-4 segundos
    """

@router.post("/api/download")
async def download(request: DownloadRequest) -> StreamingResponse:
    """
    Faz download em streaming direto do vídeo.
    
    Request:
    - url: URL do vídeo do YouTube
    - format_id: ID do formato (obtido em /api/formats)
    
    Response:
    - Stream do vídeo com Content-Length definido
    - Suporta Range requests (pause/resume)
    - Headers: Accept-Ranges: bytes
    """
```

## 🔄 Comparação: Sprint 1 vs Sprint 2

### Sprint 1 (Áudio Apenas)
```
POST /download + FileResponse
└─ Salva MP3 em /temp
└─ Retorna arquivo inteiro
└─ Cleanup automático (5 min)
└─ Suporta YouTube Shorts (yt-dlp não diferencia)
```

### Sprint 2 (Adiciona Suporte a Vídeo)
```
📌 IMPORTANTE: Audio mantém implementação atual (sem mudanças)

GET /api/formats?url=...
└─ Extrai metadados de vídeo/áudio (2-4s)
└─ Cliente vê opções + tamanho + duração

POST /api/download + StreamingResponse
└─ Inicia stream yt-dlp → cliente (NOVO)
└─ Content-Length definido (barra de progresso!)
└─ Accept-Ranges: bytes (retry suportado)
└─ Zero disco
└─ Memória mínima (chunks 64KB)

Após validação de funcionalidade:
→ Considerar refatorar audio para usar novo sistema
```

## ✅ Checklist de Implementação

### Fase 1: Estrutura Base
- [ ] Criar schemas `FormatInfo`, `VideoMetadata`, `DownloadRequest`
- [ ] Função `extract_video_metadata()` em `services/youtube.py`
- [ ] Função `stream_video()` em `core/downloader.py`

### Fase 2: Endpoints
- [ ] Endpoint `GET /api/formats` em `routes/download.py`
- [ ] Refatorar `POST /api/download` para stream direto (com format_id)
- [ ] Adicionar validações de tamanho/duração
- [ ] Manter endpoint `/download` antigo funcional (audio)

### Fase 3: Validação e Documentação
- [ ] Testar fluxo completo (GET formats → POST download)
- [ ] Testar com diferentes qualidades de vídeo
- [Implementar extração de metadados (`GET /api/formats`)
3. Implementar streaming direto (`POST /api/download` com `format_id`)
4. Validar funcionalidade completa
5. Documentação e ajustes finais

### Notas Importantes

⚠️ **Audio não será refatorado agora**
- Endpoint `/api/download` (sem format_id) continua servindo audio como hoje
- Após validação de vídeo, considerar migração
- YouTube Shorts já funcionam com audio (yt-dlp não diferencia)

⚠️ **Sem testes nesta fase**
- Foco em implementação e funcionalidade
- Testes serão implementados POST-Sprint 2
- Validação manual durante desenvolvimento
### Fase 4 (Pós-Validação)
- [ ] Refatorar audio para usar novo sistema (POST-Sprint 2)
- [ ] Implementar testes completos (POST-Sprint 2)

## 🚀 Próximos Passos

1. Implementar schemas e funções de suporte
2. Testar extração de metadados
3. Implementar streaming direto
4. Testes end-to-end
5. Suporte a Shorts (Sprint 1.2 concorrente)

---

**Sprint Planning Date:** 31 de janeiro de 2026  
**Status:** Planejado para implementação
