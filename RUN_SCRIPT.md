# run.sh - Script de Desenvolvimento

Script shell que facilita a execução de comandos Python/pip no projeto.

## 🎯 Por que usar?

Em vez de:
```bash
cd api
source venv/bin/activate
python3 -m pytest tests/unit/
```

Use:
```bash
./run.sh pytest tests/unit/
```

## ✨ Benefícios

- ✅ Muda automaticamente para pasta `api`
- ✅ Ativa automaticamente `venv/bin/activate`
- ✅ Cria venv se não existir
- ✅ Mostra informações úteis (diretório, Python version)
- ✅ Retorna código de erro correto
- ✅ Colorido e fácil de ler

## 🚀 Uso

### Setup inicial (deixar executável)
```bash
chmod +x run.sh
```

### Rodar sem argumentos (mostra ajuda)
```bash
./run.sh
```

### Exemplos de uso

#### Testes
```bash
# Todos os testes
./run.sh pytest

# Apenas unitários
./run.sh pytest tests/unit/ -v

# Apenas integração
./run.sh pytest tests/integration/

# Com cobertura
./run.sh pytest --cov=app --cov-report=html

# Teste específico
./run.sh pytest tests/unit/test_validators.py::TestValidateYoutubeUrl::test_valid_youtube_watch_url -v
```

#### Rodar aplicação
```bash
./run.sh python main.py
```

#### Instalar pacotes
```bash
./run.sh pip install -r requirements.txt
./run.sh pip install requests
```

#### Formatação de código
```bash
./run.sh black app/
./run.sh black tests/
```

#### Lint
```bash
./run.sh flake8 app/
```

## 📋 O que o script faz

1. **Valida projeto** - Verifica se pasta `api` existe
2. **Cria venv** - Se não existir, cria automaticamente
3. **Ativa venv** - Usa `source venv/bin/activate`
4. **Muda diretório** - Para `api/`
5. **Executa comando** - Passa tudo para shell
6. **Mostra resultado** - Indica sucesso/erro com cores

## 🎨 Output

```
📦 Executando em: /Users/daniel/pessoal/projetos/yt-to-mp3/api
🐍 Python: Python 3.10.6
🔧 Comando: pytest -v

tests/unit/test_validators.py::TestValidateYoutubeUrl::test_valid_youtube_watch_url PASSED

✅ Comando executado com sucesso
```

## 🔧 Troubleshooting

### "Permission denied"
```bash
chmod +x run.sh
```

### "Não encontrei pasta 'api'"
Certifique-se de rodar o script da raiz do projeto:
```bash
cd /Users/daniel/pessoal/projetos/yt-to-mp3
./run.sh pytest
```

### venv não existe
O script cria automaticamente, mas você pode criar manualmente:
```bash
./run.sh python -m venv venv
```

## 💡 Dicas

### Alias (opcional)
Adicione ao `.bashrc` ou `.zshrc`:
```bash
alias dev='./run.sh'
```

Depois use:
```bash
cd /Users/daniel/pessoal/projetos/yt-to-mp3
dev pytest
```

### Executar múltiplos comandos
```bash
./run.sh bash -c "python main.py && echo 'Done!'"
```

### Ver ajuda
```bash
./run.sh
```

---

**Criado:** 30 de janeiro de 2026
