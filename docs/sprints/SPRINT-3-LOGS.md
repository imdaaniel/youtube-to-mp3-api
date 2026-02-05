# SPRINT 3 - Sistema de Logs com Detalhes de Erros

## 🎯 Objetivo

Implementar sistema de logging robusto que capture erros automaticamente via middleware, salvando logs estruturados em arquivos com rotação automática e detalhes contextuais.

## 📋 Requisitos

- Salvar logs de erros em arquivo
- Capturar detalhes completos das exceções (stack trace, contexto)
- Logs estruturados em JSON para facilitar parsing
- Rotação automática de arquivos de log
- Limpeza de logs antigos
- **NÃO** poluir código com try-catch
- Incluir dados da requisição (método, endpoint, IP, etc)
- Campo flexível para detalhes específicos

## 🏗️ Arquitetura

### Abordagem Híbrida

**Middleware de Logging:**
- Captura exceções não tratadas automaticamente
- Adiciona contexto da requisição HTTP
- Gera request_id único para rastreamento
- Calcula duração da requisição
- Loga com detalhes completos

**Logging Estratégico:**
- Logs info/debug em pontos críticos (sem try-catch)
- Informações de sucesso e progresso
- Deixar exceções propagarem naturalmente para o middleware

## 📊 Estrutura de Logs

### Formato JSON Estruturado

```json
{
  "timestamp": "2026-02-04T10:30:45.123456",
  "level": "ERROR",
  "request_id": "uuid-1234-5678",
  "method": "POST",
  "endpoint": "/api/download-stream",
  "client_ip": "127.0.0.1",
  "user_agent": "Mozilla/5.0...",
  "duration_ms": 1250,
  "status_code": 500,
  "error_type": "DownloadError",
  "error_message": "Failed to download video",
  "stack_trace": "Traceback (most recent call last):\n...",
  "details": {
    "url": "https://youtube.com/watch?v=...",
    "format_id": "137+140",
    "stage": "download",
    "yt_dlp_error": "HTTP Error 403: Forbidden"
  }
}
```

### Campos Padrão

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `timestamp` | string | ISO 8601 com microsegundos |
| `level` | string | ERROR, WARNING, INFO, DEBUG |
| `request_id` | string | UUID único por requisição |
| `method` | string | HTTP method (GET, POST, etc) |
| `endpoint` | string | Path da requisição |
| `client_ip` | string | IP do cliente |
| `user_agent` | string | User-Agent do cliente |
| `duration_ms` | int | Tempo de execução em ms |
| `status_code` | int | HTTP status code |
| `error_type` | string | Tipo da exceção |
| `error_message` | string | Mensagem de erro |
| `stack_trace` | string | Stack trace completo |
| `details` | object/string | Contexto específico (flexível) |

### Campo `details`

Campo flexível para contexto adicional:
- **Objeto/Dict**: dados estruturados (preferível)
- **String**: mensagens simples
- Cada endpoint/serviço adiciona seus próprios detalhes

## 🛠️ Implementação

### 1. Configuração (app/config.py)

Adicionar configurações de logging:

```python
# Logs
LOGS_DIR: Path = BASE_DIR / "logs"
LOG_LEVEL: str = "INFO"
LOG_RETENTION_DAYS: int = 30
LOG_WHEN: str = "midnight"  # Rotação à meia-noite
LOG_INTERVAL: int = 1  # Intervalo de rotação
LOG_BACKUP_COUNT: int = 30  # Manter 30 arquivos
```

### 2. Logger Configurado (app/utils/logger.py)

**Novo arquivo** com:
- Configuração do logging Python nativo
- `TimedRotatingFileHandler` para rotação por tempo
- Formatação JSON estruturada
- Logger singleton para toda aplicação

**Funções:**
```python
def setup_logger() -> logging.Logger
def get_logger() -> logging.Logger
```

### 3. Middleware de Logging (app/middleware/logging.py)

**Novo arquivo** com middleware FastAPI:

**Responsabilidades:**
- Gerar `request_id` único (UUID)
- Armazenar em `contextvars` para acesso global
- Capturar exceções não tratadas
- Extrair contexto da requisição (método, path, IP, headers)
- Calcular duração
- Logar em formato estruturado
- Re-lançar exceção para tratamento HTTP adequado

**Implementação:**
```python
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    # 1. Gerar request_id
    # 2. Armazenar em contextvars
    # 3. Tentar executar requisição
    # 4. Se erro: capturar, logar com detalhes, re-lançar
    # 5. Se sucesso: logar info (opcional)
```

### 4. Context Vars (app/utils/context.py)

**Novo arquivo** para propagação de request_id:

```python
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar('request_id', default=None)
request_details_var: ContextVar[dict] = ContextVar('request_details', default={})
```

### 5. Helper de Logging (app/utils/log_helpers.py)

**Novo arquivo** com funções utilitárias:

```python
def add_request_detail(key: str, value: Any)
def log_info(message: str, **details)
def log_error(message: str, exc: Exception = None, **details)
def format_exception(exc: Exception) -> dict
```

### 6. Logging Estratégico nos Serviços

Adicionar logs em pontos-chave **SEM try-catch**:

**app/services/youtube.py:**
```python
logger.info(f"Iniciando extração de metadados", extra={"url": url})
# ... código ...
logger.info(f"Download iniciado", extra={"url": url, "format": format_id})
```

**app/routes/download.py:**
```python
log_info("Request recebida", url=request.url, format_id=request.format_id)
# ... código ...
log_info("Download concluído", filename=filename, size_mb=size)
```

### 7. Limpeza de Logs Antigos (app/services/cleanup.py)

Adicionar função:

```python
def cleanup_old_logs():
    """Remove logs mais antigos que LOG_RETENTION_DAYS"""
    # Iterar por arquivos em LOGS_DIR
    # Verificar data de modificação
    # Remover se > retention
```

Integrar ao scheduler existente em `main.py`.

### 8. Integração no main.py

```python
from app.utils.logger import setup_logger
from app.middleware.logging import logging_middleware

def create_app():
    # Configurar logger
    setup_logger()
    
    app = FastAPI(...)
    
    # Adicionar middleware (ANTES de outros middlewares)
    app.middleware("http")(logging_middleware)
    
    # ... resto da configuração
```

### 9. .gitignore

Adicionar:
```
logs/*.log
logs/*.log.*
```

Manter `.gitkeep` no diretório.

## 📁 Arquivos a Criar/Modificar

### Novos Arquivos

- `app/utils/logger.py` - Configuração do logger
- `app/utils/context.py` - Context vars para request_id
- `app/utils/log_helpers.py` - Helpers de logging
- `app/middleware/logging.py` - Middleware de captura
- `logs/.gitkeep` - Manter diretório no git
- `tests/unit/test_logger.py` - Testes unitários
- `tests/integration/test_logging_middleware.py` - Testes de integração

### Arquivos a Modificar

- `app/config.py` - Adicionar configurações de logs
- `main.py` - Registrar middleware e configurar logger
- `app/services/cleanup.py` - Adicionar limpeza de logs
- `app/routes/download.py` - Adicionar logs estratégicos
- `app/services/youtube.py` - Adicionar logs estratégicos
- `app/core/downloader.py` - Adicionar logs estratégicos
- `.gitignore` - Ignorar arquivos de log

## 🧪 Testes

### Testes Unitários

**test_logger.py:**
- Configuração correta do logger
- Formatação JSON
- Rotação de arquivos
- Níveis de log

### Testes de Integração

**test_logging_middleware.py:**
- Captura de exceção e logging
- Request_id gerado corretamente
- Campos padrão presentes
- Campo details populado
- Logs salvos em arquivo

**Cenários:**
- Erro 404 (URL inválida)
- Erro 500 (falha no download)
- Sucesso (200)

## 📈 Níveis de Log

| Nível | Uso |
|-------|-----|
| **ERROR** | Exceções capturadas pelo middleware |
| **WARNING** | Situações anormais mas não críticas |
| **INFO** | Eventos importantes (download iniciado, concluído) |
| **DEBUG** | Detalhes de execução (desenvolvimento) |

## 🔒 Segurança

### Sanitização de Dados

- **NÃO** logar tokens ou credenciais
- **NÃO** logar dados sensíveis do usuário
- Truncar URLs muito longas
- Sanitizar user-agent

### Exemplo

```python
def sanitize_url(url: str) -> str:
    """Remove query params sensíveis"""
    # Implementar lógica
    
def sanitize_headers(headers: dict) -> dict:
    """Remove headers sensíveis"""
    sensitive = ['authorization', 'cookie']
    return {k: v for k, v in headers.items() if k.lower() not in sensitive}
```

## 📊 Monitoramento

Com logs estruturados em JSON, é possível:
- Importar para Elasticsearch/Kibana
- Análise com jq, grep, etc
- Dashboards de métricas
- Alertas automáticos

**Exemplo de query:**
```bash
# Contar erros por tipo
cat logs/app.log | jq -r '.error_type' | sort | uniq -c

# Filtrar erros de uma URL específica
cat logs/app.log | jq 'select(.details.url | contains("youtube.com"))'
```

## ✅ Critérios de Aceite

- [ ] Logs salvos em `logs/app.log`
- [ ] Formato JSON válido em cada linha
- [ ] Middleware captura exceções automaticamente
- [ ] Request_id único por requisição
- [ ] Campos padrão sempre presentes
- [ ] Campo details com contexto específico
- [ ] Stack trace completo nos erros
- [ ] Rotação automática (diária)
- [ ] Limpeza de logs > 30 dias
- [ ] Sem try-catch espalhado no código
- [ ] Logs de info em pontos estratégicos
- [ ] Testes passando

## 🚀 Ordem de Implementação

1. ✅ Criar estrutura de pastas (`logs/`)
2. ✅ Configurar settings (`app/config.py`)
3. ✅ Implementar logger base (`app/utils/logger.py`)
4. ✅ Criar context vars (`app/utils/context.py`)
5. ✅ Implementar middleware (`app/middleware/logging.py`)
6. ✅ Criar helpers (`app/utils/log_helpers.py`)
7. ✅ Integrar no main.py
8. ✅ Adicionar logs estratégicos nos serviços
9. ✅ Implementar limpeza de logs
10. ✅ Atualizar .gitignore
11. ✅ Escrever testes
12. ✅ Validar funcionamento

## 💡 Melhorias Futuras (Fase 2)

- Logging assíncrono com `QueueHandler`
- Integração com Sentry para alertas
- Dashboard de monitoramento
- Métricas de performance
- Logs de auditoria (quem fez o quê)
- Correlação entre múltiplas requisições
