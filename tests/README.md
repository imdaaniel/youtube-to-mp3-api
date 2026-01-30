# Testes - YT to MP3 API

Suite de testes automatizados para garantir a qualidade e confiabilidade do código.

## 📁 Estrutura

```
tests/
├── conftest.py              # Fixtures compartilhadas
├── unit/                    # Testes unitários
│   ├── test_validators.py   # Validação de URLs
│   ├── test_id_generator.py # Geração de IDs
│   └── test_cleanup.py      # Limpeza de arquivos
└── integration/             # Testes de integração
    └── test_endpoints.py    # Endpoints da API
```

## 🚀 Como Rodar

### Instalar dependências de teste
```bash
pip install -r requirements.txt
```

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
pytest tests/unit/test_validators.py::TestValidateYoutubeUrl::test_valid_youtube_watch_url
```

### Gerar relatório de cobertura
```bash
pytest --cov=app --cov-report=html
# Abrir htmlcov/index.html no navegador
```

## 📊 Cobertura de Testes

### Unit Tests (testes unitários)

#### `test_validators.py`
Testa validação de URLs do YouTube:
- ✅ URLs padrão `youtube.com/watch?v=...`
- ✅ URLs encurtadas `youtu.be/...`
- ✅ YouTube Shorts `youtube.com/shorts/...`
- ✅ Rejeição de URLs inválidas
- ✅ Tratamento de strings malformadas

**Cobertura:** 10 testes

#### `test_id_generator.py`
Testa geração de IDs únicos:
- ✅ Formato correto `timestamp_hash`
- ✅ IDs diferentes para URLs diferentes
- ✅ Hash consistente para mesma URL
- ✅ Timestamp incremental
- ✅ Tratamento de casos edge

**Cobertura:** 7 testes

#### `test_cleanup.py`
Testa limpeza de arquivos temporários:
- ✅ Remove pastas antigas (>TTL)
- ✅ Preserva pastas recentes
- ✅ Lida com diretórios vazios
- ✅ Cria diretório após limpeza total
- ✅ Tratamento de exceções

**Cobertura:** 6 testes

### Integration Tests (testes de integração)

#### `test_endpoints.py`
Testa endpoints da API:
- ✅ Endpoint raiz `/` retorna informações
- ✅ Validação de URLs em requisições
- ✅ Rejeição de URLs inválidas
- ✅ Documentação automática Swagger
- ✅ Schema OpenAPI válido

**Cobertura:** 13 testes + parametrizados

## 🎯 Exemplo de Teste

```python
def test_valid_youtube_watch_url(self):
    """Deve validar URL padrão do YouTube watch"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert validate_youtube_url(url) is True
```

## 🔄 Integração Contínua

Estes testes são projetados para rodar em CI/CD:

```yaml
# Exemplo GitHub Actions
- name: Run tests
  run: pytest --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## 📈 Métricas

- **Total de testes:** 36+
- **Tempo de execução:** ~5-10 segundos
- **Cobertura esperada:** >80%

## ⚠️ Notas Importantes

1. **Testes unitários não fazem requisições reais** - usam mocks
2. **Testes de integração com FastAPI TestClient** - não precisa servidor rodando
3. **Fixtures reutilizáveis** em `conftest.py`
4. **Parametrized tests** para testar múltiplos casos

## 🐛 Adicionando Novos Testes

1. Crie arquivo `test_*.py` em `tests/unit/` ou `tests/integration/`
2. Crie classe `Test*` dentro do arquivo
3. Crie funções `test_*` dentro da classe
4. Use fixtures de `conftest.py` quando necessário

Exemplo:
```python
class TestMyFeature:
    def test_something(self):
        """Descrição clara do teste"""
        result = my_function()
        assert result == expected
```

## 📚 Referências

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/fixture.html)
- [parametrized tests](https://docs.pytest.org/parametrize.html)
- [FastAPI testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)

---

**Última atualização:** 30 de janeiro de 2026
