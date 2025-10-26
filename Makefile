.PHONY: help clean ruff-fix ruff-check ruff-format pyright pyright-install

help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "Ruff (checagem/format):"
	@echo "  ruff-fix      - Formata e corrige código com Ruff (auto-fix lint e formatting)"
	@echo "  ruff-check    - Checa lint e formatting sem modificar arquivos"
	@echo "  ruff-format   - Checa apenas o formatting, sem lint"
	@echo ""
	@echo "Type Checking:"
	@echo "  pyright           - Executa checagem estática de tipos com Pyright"
	@echo "  pyright-install   - Instala o Pyright globalmente via npm"
	@echo ""
	@echo "Manutenção:"
	@echo "  clean         - Remove caches, arquivos gerados e artefatos de build"
	@echo ""
	@echo "Uso: make <comando>"

clean:
	rm -rf \
		__pycache__ \
		*.pyc \
		*.pyo \
		*.egg-info \
		*.egg \
		.eggs \
		build/ \
		dist/ \
		.ruff_cache/ \
		.mypy_cache/ \
		.pytest_cache/ \
		htmlcov/ \
		coverage.xml \
		.tox/ \
		.pyright/ \
		*.typed \
		*.lock \
		.cache/ \
		.pyre/ \
		.pytype/ \
		.nox/ \
		site/ \
		.DS_Store \
		|| true
	find . -name "*.pyc" -type f -delete 2>/dev/null || true
	find . -name "*.pyo" -type f -delete 2>/dev/null || true
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.egg" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".ruff_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".mypy_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pyright" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pyre" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytype" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".nox" -type d -exec rm -rf {} + 2>/dev/null || true



ruff-fix:
	uv run ruff format --check src/
	uv run ruff check src/ --fix

ruff-check:
	uv run ruff format src/ --check
	uv run ruff check src/

ruff-format:
	uv run ruff format --check src/

# Catch-all target to allow passing arguments
%:
	@:

# Pyright Commands
pyright-install:
	@echo "📦 Instalando Pyright globalmente via npm..."
	npm install -g pyright
	@echo "✅ Pyright instalado com sucesso!"

pyright:
	@echo "🔍 Executando checagem estática de tipos com Pyright..."
	@if command -v pyright >/dev/null 2>&1; then \
		pyright; \
	else \
		echo "❌ Pyright não encontrado. Instale com: make pyright-install"; \
		echo "   Ou instale via npm: npm install -g pyright"; \
		exit 1; \
	fi
