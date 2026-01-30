# Sprint 1: Expor API e Servir Áudio

## Objetivo
Criar um endpoint FastAPI que receba URL do YouTube, valide, baixe o áudio e retorne o arquivo MP3 como resposta da requisição.

## Requisitos Funcionais

### Endpoint: POST /download
**Descrição:** Recebe URL do YouTube, valida e retorna o áudio em MP3

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response (200):**
- Content-Type: audio/mpeg
- Content-Disposition: attachment; filename="titulo_do_video.mp3"
- Body: Stream do arquivo MP3

**Response (400):**
```json
{
  "detail": "URL inválida ou não é um vídeo do YouTube"
}
```

**Response (500):**
```json
{
  "detail": "Erro ao baixar vídeo: [mensagem de erro]"
}
```

## Decisões Técnicas

### ID do Vídeo
Usar timestamp + hash da URL para evitar colisões:
```python
video_id = f"{int(datetime.now().timestamp() * 1000)}_{hashlib.md5(url.encode()).hexdigest()[:8]}"
```

### Retorno do Arquivo
Retornar o arquivo MP3 diretamente na requisição (streaming) ao invés de endpoint separado:
- ✅ UX mais simples
- ✅ 1 requisição = download completo
- ✅ Menos código para MVP

## Arquitetura

```
POST /download
    ↓
[Validação de URL]
    ↓
[Download com yt-dlp]
    ↓
[Stream MP3 para cliente]
    ↓
[Limpeza de arquivo temporário]
```

## Estrutura de Pastas

```
api/
├── transform.py          (já existe - função download_audio)
├── main.py               (NOVO - servidor FastAPI)
├── requirements.txt      (NOVO - dependências)
└── docs/
    └── sprints/
        └── SPRINT-1-SERVE-API.md
```

## Dependências

- fastapi
- uvicorn
- yt-dlp
- python-multipart

## Validações

1. URL deve ser válida (HTTP/HTTPS)
2. URL deve ser do YouTube (youtube.com ou youtu.be)
3. Vídeo deve estar disponível para download
4. Extensão deve ser .mp3

## Tratamento de Erros

- URL inválida → 400 Bad Request
- Vídeo não encontrado/privado → 400 Bad Request
- Erro de download → 500 Internal Server Error
- Timeout → 504 Gateway Timeout
