## Requirements

.PHONY: minimum-requirements
minimum-requirements:
	@PYTHONPATH=. python -m pip install -U -r requirements.txt

.PHONY: requirements-lint
requirements-lint:
	@PYTHONPATH=. python -m pip install -r requirements.lint.txt

.PHONY: requirements
## All requirements except docs
requirements: minimum-requirements requirements-lint

## Style Checks

.PHONY: check-black
check-black:
	@echo ""
	@echo "Code Style With Black"
	@echo "=========="
	@echo ""
	@python -m black --check -t py38 --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" . && echo "\n\nSuccess" || (echo "\n\nFailure\n\nRun \"make black\" to apply style formatting to your code"; return 2)
	@echo ""

.PHONY: check-flake8
check-flake8:
	@echo ""
	@echo "Flake 8 Lint"
	@echo "======="
	@echo ""
	@-python -m flake8 last_gas/ && echo "last_gas module success"
	@-python -m flake8 tests/ && echo "tests module success"
	@echo ""

.PHONY: checks
checks:
	@echo ""
	@echo "Code Style With Black & Flake 8 Lint"
	@echo "--------------------"
	@echo ""
	@make check-black
	@make check-flake8
	@echo ""

.PHONY: black
black:
	@python -m black -t py38 --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" .
