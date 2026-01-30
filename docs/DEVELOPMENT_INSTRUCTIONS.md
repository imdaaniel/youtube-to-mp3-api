# 🚨 INSTRUÇÕES CRÍTICAS DE DESENVOLVIMENTO

## REGRA FUNDAMENTAL
**SEMPRE usar `./run.sh <comando>` para executar qualquer comando neste projeto.**

### ❌ ERRADO
```bash
pytest -v
python main.py
pip install package
```

### ✅ CORRETO
```bash
./run.sh pytest -v
./run.sh python main.py
./run.sh pip install package
```

## Por quê?
- `run.sh` garante o ambiente correto
- Mantém consistência em todo o projeto
- Facilita reprodução de problemas

## Exemplos de Uso
```bash
./run.sh pytest -v --tb=short
./run.sh python -m uvicorn app.main:app --reload
./run.sh pip install -r requirements.txt
./run.sh python -c "from app.config import settings; print(settings.TEMP_DIR)"
```

## Scope de Trabalho
- **TUDO** deve ficar em: `/Users/daniel/pessoal/projetos/yt-to-mp3/api/`
- Nunca criar arquivos fora dessa pasta
- Manter estrutura organizada

---
**Última atualização:** 30 de janeiro de 2026
