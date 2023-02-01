PYTHONPATH = PYTHONPATH=./
POETRY_RUN = poetry run

PROTO_DIR = protos/tinkoff/invest/grpc
PACKAGE_PROTO_DIR = tinkoff/invest/grpc
OUT = .
PROTOS = protos

TEST = $(POETRY_RUN) pytest $(args)
MAIN_CODE = tinkoff examples scripts
CODE = tests $(MAIN_CODE)
EXCLUDE_CODE = tinkoff/invest/grpc

.PHONY: test
test:
	$(TEST) --cov

.PHONY: test-sandbox
test-sandbox:
	$(TEST) --test-sandbox --cov

.PHONY: lint
lint:
	$(POETRY_RUN) ruff $(CODE)
	$(POETRY_RUN) flake8 --jobs 1 --statistics --show-source $(CODE)
	$(POETRY_RUN) pylint --jobs 1 --rcfile=setup.cfg $(CODE)
	$(POETRY_RUN) bandit -r $(MAIN_CODE)
	$(POETRY_RUN) black --line-length=88 --exclude=$(EXCLUDE_CODE) --check $(CODE)
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures
	$(POETRY_RUN) mypy $(CODE)
	$(POETRY_RUN) poetry check
	$(POETRY_RUN) toml-sort --check pyproject.toml

.PHONY: format
format:
	$(POETRY_RUN) autoflake --recursive --in-place --remove-all-unused-imports --exclude=$(EXCLUDE_CODE) $(CODE)
	$(POETRY_RUN) isort $(CODE)
	$(POETRY_RUN) black --line-length=88 --exclude=$(EXCLUDE_CODE) $(CODE)
	$(POETRY_RUN) ruff --fix $(CODE)
	$(POETRY_RUN) toml-sort --in-place pyproject.toml

.PHONY: check
check: lint test

.PHONY: docs
docs:
	mkdir -p ./docs
	cp README.md ./docs/
	cp CHANGELOG.md ./docs/
	cp CONTRIBUTING.md ./docs/
	$(POETRY_RUN) mkdocs build -s -v

.PHONY: docs-serve
docs-serve:
	$(POETRY_RUN) mkdocs serve

.PHONY: next-version
next-version:
	@$(POETRY_RUN) python -m scripts.version

.PHONY: bump-version
bump-version:
	poetry version $(v)
	$(POETRY_RUN) python -m scripts.update_issue_templates $(v)
	git add . && git commit -m "chore(release): bump version to $(v)"
	git tag -a $(v) -m ""

.PHONY: install-poetry
install-poetry:
	pip install poetry==1.3.1

.PHONY: install-docs
install-docs:
	poetry install --only docs

.PHONY: install-bump
install-bump:
	poetry install --only bump

.PHONY: install
install:
	poetry install -E all

.PHONY: publish
publish:
	@poetry publish --build --no-interaction --username=$(pypi_username) --password=$(pypi_password)

.PHONY: download-protos
download-protos:
	$(POETRY_RUN) python -m scripts.download_protos

.PHONY: gen-grpc
gen-grpc:
	rm -r ${PACKAGE_PROTO_DIR}
	$(POETRY_RUN) python -m grpc_tools.protoc -I${PROTOS} --python_out=${OUT} --mypy_out=${OUT} --grpc_python_out=${OUT} ${PROTO_DIR}/*.proto
	touch ${PACKAGE_PROTO_DIR}/__init__.py

.PHONY: gen-grpc-new
gen-grpc-new:
	$(POETRY_RUN) python -m grpc_tools.protoc -I${PROTOS} --plugin=protoc-gen-custom-plugin=scripts/ohmyproto_plugin_main.py --custom-plugin_out=$(OUT) ${PROTO_DIR}/*.proto
	$(POETRY_RUN) python -m grpc_tools.protoc -I${PROTOS} --plugin=protoc-gen-custom-plugin=scripts/ohmyproto_plugin_grpc.py --custom-plugin_out=$(OUT) ${PROTO_DIR}/*.proto
	touch ${PACKAGE_PROTO_DIR}/__init__.py

.PHONY: gen-client
gen-client: download-protos gen-grpc
