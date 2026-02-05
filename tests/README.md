# Testes - YT to MP3 API

Suite de testes automatizados para garantir a qualidade e confiabilidade do código.

## 📁 Estrutura

```
tests/
├── conftest.py              # Fixtures compartilhadas
├── unit/                    # Testes unitários
│   ├── test_validators.py   # Validação de URLs
│   ├── test_helpers.py      # Funções utilitárias
│   └── test_cleanup.py      # Limpeza de arquivos
└── integration/             # Testes de integração
    └── test_endpoints.py    # Endpoints da API
```

## 🚀 Como Rodar

### Rodar todos os testes
```bash
pytest
```

### Rodar testes com saída verbosa
```bash
pytest -v
```

### Rodar apenas testes unitários
```bash
pytest tests/unit/
```

### Rodar apenas testes de integração
```bash
pytest tests/integration/
```

### Rodar testes específicos
```bash
pytest tests/unit/test_validators.py
pytest tests/unit/test_helpers.py::TestSanitizeFilename
```

### Gerar relatório de cobertura
```bash
pytest --cov=app --cov-report=html
# Abrir htmlcov/index.html no navegador
```

## 📊 Cobertura de Testes (60 testes ✅)

### Testes de Integração (15 testes)

#### `test_endpoints.py`
Testa todos os endpoints da API:
- ✅ **Endpoint raiz** (`/`) - 2 testes
- ✅ **GET /api/formats** - Extração de metadados - 4 testes
  - Validação de parâmetros obrigatórios
  - Rejeição de URLs inválidas
  - Retorno de metadados corretos
  - Tratamento de erros
- ✅ **POST /api/download-stream** - Streaming de vídeo - 4 testes
  - Validação de campos obrigatórios (url, format_id)
  - Rejeição de URLs inválidas
  - Streaming funcional
- ✅ **POST /api/download** - Download de áudio MP3 - 3 testes
  - Validação de campos
  - Tratamento de erros de download
- ✅ **Documentação da API** - 2 testes
  - Swagger UI disponível
  - Schema OpenAPI válido com endpoints corretos

### Testes Unitários (45 testes)

#### `test_validators.py` - 9 testes
Testa validação de URLs do YouTube:
- ✅ URLs válidas: `youtube.com/watch`, `youtu.be`, `youtube.com/shorts`
- ✅ URLs com e sem `www`
- ✅ URLs com parâmetros adicionais
- ✅ Rejeição de outros domínios (Google, Vimeo)
- ✅ Rejeição de strings vazias e malformadas

#### `test_cleanup.py` - 6 testes
Testa limpeza de arquivos temporários:
- ✅ Remove pastas mais antigas que TTL (Time To Live)
- ✅ Preserva pastas recentes
- ✅ Lida corretamente com diretório vazio
- ✅ Lida com diretório inexistente
- ✅ Limpeza total remove todos os arquivos
- ✅ Recria diretório temp após limpeza

#### `test_helpers.py` - 30 testes

**TestSanitizeFilename** (8 testes):
- ✅ Remove caracteres especiais
- ✅ Substitui espaços por underscores
- ✅ Preserva caracteres alfanuméricos
- ✅ Preserva hífens e pontos
- ✅ Remove underscores múltiplos
- ✅ Remove pontos/underscores no início/fim
- ✅ Lida com string vazia
- ✅ Lida com apenas caracteres especiais

**TestFormatDuration** (7 testes):
- ✅ Formata 0 segundos como "0:00"
- ✅ Formata apenas segundos (ex: "0:45")
- ✅ Formata minutos e segundos (ex: "2:05")
- ✅ Formata horas, minutos e segundos (ex: "1:01:05")
- ✅ Formata minutos exatos
- ✅ Formata horas exatas
- ✅ Adiciona zero à esquerda corretamente

**TestFormatFilesize** (8 testes):
- ✅ Retorna None para valor None ou zero
- ✅ Formata bytes sem decimal
- ✅ Formata kilobytes com 1 casa decimal
- ✅ Formata megabytes
- ✅ Formata gigabytes
- ✅ Formata exatamente 1024 bytes
- ✅ Aceita entrada float

**TestGenerateVideoId** (7 testes):
- ✅ Gera ID com formato válido `timestamp_hash`
- ✅ Gera IDs diferentes para URLs diferentes
- ✅ Hash é consistente para mesma URL
- ✅ Hash tem exatamente 8 caracteres
- ✅ Timestamp aumenta entre chamadas
- ✅ Lida com URL vazia
- ✅ Lida com caracteres especiais na URL

## 🎯 Estratégia de Testes

### Mocks Utilizados
```python
# Mock de extração de metadados
@patch('app.routes.download.extract_video_metadata')

# Mock de download de áudio
@patch('app.routes.download.download_youtube_audio')

# Mock de streaming
@patch('app.routes.download.stream_video')
```

### Fixtures Disponíveis
- **`client`**: TestClient do FastAPI para testes de integração
- **`temp_dir_test`**: Diretório temporário isolado para testes
- **`sample_urls`**: URLs de exemplo para testes

## ✅ Resultados

```
============================= 60 passed, 10 warnings in 0.14s =============================
```

- **Total**: 60 testes
- **Status**: Todos passando ✅
- **Tempo de execução**: ~0.14 segundos
- **Warnings**: 10 (deprecations menores, não afetam funcionalidade)

## 📝 Observações

### Arquivos Removidos
- ❌ `test_id_generator.py` - Excluído (testava importação inexistente)
  - A função `generate_video_id` está em `helpers.py`, não em módulo separado
  - Testes migrados para `test_helpers.py`

### Melhorias Implementadas
- ✅ Testes agora refletem os endpoints reais da aplicação
- ✅ Cobertura completa das funções utilitárias
- ✅ Testes de integração para todos os 3 endpoints principais
- ✅ Validação de schemas e documentação OpenAPI
- ✅ Casos extremos (edge cases) cobertos

## 🔜 Próximas Melhorias

- [ ] Testes para o serviço `youtube.py` (extração de metadados)
- [ ] Testes para o módulo `downloader.py` (stream_video)
- [ ] Testes de performance e carga
- [ ] Testes end-to-end com vídeos reais (opcional)
- [ ] Aumentar cobertura de código para 100%
