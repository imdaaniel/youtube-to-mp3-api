#!/bin/bash

##############################################################################
# Script wrapper para executar comandos Python/pip no projeto
# Uso: ./run.sh <comando> [argumentos...]
#
# Exemplos:
#   ./run.sh pytest
#   ./run.sh pytest tests/unit/ -v
#   ./run.sh pip install requests
#   ./run.sh python main.py
#   ./run.sh python -m pytest --cov=app
##############################################################################

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_DIR="$PROJECT_DIR"

# Verificar se está na raiz do projeto
if [ ! -d "$API_DIR" ]; then
    echo -e "${RED}❌ Erro: Não encontrei pasta 'api' em $PROJECT_DIR${NC}"
    exit 1
fi

# Verificar se tem venv
if [ ! -d "$API_DIR/venv" ]; then
    echo -e "${YELLOW}⚠️  Pasta venv não encontrada em $API_DIR/venv${NC}"
    echo -e "${YELLOW}Criando venv...${NC}"
    cd "$API_DIR"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erro ao criar venv${NC}"
        exit 1
    fi
fi

# Mudar para diretório api
cd "$API_DIR" || exit 1

# Ativar venv
source venv/bin/activate

# Se não passou comando, mostrar ajuda
if [ $# -eq 0 ]; then
    echo -e "${BLUE}YT to MP3 - Script de Desenvolvimento${NC}"
    echo ""
    echo "Uso: ./run.sh <comando> [argumentos...]"
    echo ""
    echo -e "${GREEN}Exemplos:${NC}"
    echo "  ./run.sh pytest                          # Rodar todos os testes"
    echo "  ./run.sh pytest tests/unit/ -v           # Rodar testes unitários com verbose"
    echo "  ./run.sh pytest --cov=app                # Rodar com cobertura"
    echo "  ./run.sh python main.py                  # Rodar aplicação"
    echo "  ./run.sh python -m pip install requests  # Instalar pacote"
    echo "  ./run.sh python -m pytest -v             # Pytest via python -m"
    echo "  ./run.sh pip install -r requirements.txt # Instalar dependências"
    echo ""
    echo -e "${GREEN}Comandos comuns:${NC}"
    echo "  ./run.sh pytest                    # Todos os testes"
    echo "  ./run.sh pytest tests/unit/ -v     # Testes unitários"
    echo "  ./run.sh pytest tests/integration/ # Testes integração"
    echo "  ./run.sh pytest --cov=app --cov-report=html"
    echo "  ./run.sh python main.py            # Inicia servidor"
    echo "  ./run.sh pip install -r requirements.txt"
    echo "  ./run.sh black app/                # Format código"
    echo ""
    echo -e "${GREEN}Comandos especiais:${NC}"
    echo "  ./run.sh clean                     # Limpa pasta temp/"
    echo "  ./run.sh clean-all                 # Limpa temp/ e .pytest_cache/"
    echo ""
    exit 0
fi

# Verificar comandos especiais
if [ "$1" = "clean" ]; then
    echo -e "${YELLOW}🧹 Limpando pasta temp/...${NC}"
    if [ -d "$API_DIR/temp" ]; then
        rm -rf "$API_DIR/temp"
        mkdir -p "$API_DIR/temp"
        echo -e "${GREEN}✅ Pasta temp/ limpa com sucesso${NC}"
    else
        echo -e "${YELLOW}⚠️  Pasta temp/ não existe${NC}"
    fi
    exit 0
fi

if [ "$1" = "clean-all" ]; then
    echo -e "${YELLOW}🧹 Limpando temp/, .pytest_cache/ e __pycache__...${NC}"
    
    # Limpar temp
    if [ -d "$API_DIR/temp" ]; then
        rm -rf "$API_DIR/temp"
        mkdir -p "$API_DIR/temp"
        echo -e "${GREEN}✅ temp/ limpo${NC}"
    fi
    
    # Limpar pytest cache
    if [ -d "$API_DIR/.pytest_cache" ]; then
        rm -rf "$API_DIR/.pytest_cache"
        echo -e "${GREEN}✅ .pytest_cache/ limpo${NC}"
    fi
    
    # Limpar pycache
    find "$API_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    echo -e "${GREEN}✅ __pycache__/ limpo${NC}"
    
    # Limpar arquivos .pyc
    find "$API_DIR" -name "*.pyc" -delete 2>/dev/null
    echo -e "${GREEN}✅ .pyc removidos${NC}"
    
    echo -e "${GREEN}✅ Limpeza completa concluída${NC}"
    exit 0
fi

# Executar comando
echo -e "${BLUE}📦 Executando em: $API_DIR${NC}"
echo -e "${BLUE}🐍 Python: $(python3 --version)${NC}"
echo -e "${BLUE}🔧 Comando: $@${NC}"
echo ""

# Executar
"$@"
EXIT_CODE=$?

# Mostrar resultado
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Comando executado com sucesso${NC}"
else
    echo -e "${RED}❌ Comando falhou com código: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
