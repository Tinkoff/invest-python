PYTHONPATH = PYTHONPATH=./

PROTO_DIR = protos/tinkoff/invest/grpc
PACKAGE_PROTO_DIR = tinkoff/invest/grpc
OUT = .
PROTOS = protos

TEST = pytest $(args) --verbosity=2 --showlocals --strict-markers --log-level=DEBUG
CODE = tests tinkoff examples
EXCLUDE_CODE = tinkoff/invest/grpc

.PHONY: test
test:
	$(TEST) --cov

.PHONY: lint
lint:
	flake8 --jobs 1 --statistics --show-source $(CODE)
	pylint --jobs 1 --rcfile=setup.cfg $(CODE)
	black --line-length=88 --exclude=$(EXCLUDE_CODE) --check $(CODE)
	pytest --dead-fixtures --dup-fixtures
	mypy $(CODE)
	poetry check
	toml-sort --check pyproject.toml

.PHONY: format
format:
	autoflake --recursive --in-place --remove-all-unused-imports --exclude=$(EXCLUDE_CODE) $(CODE)
	isort $(CODE)
	black --line-length=88 --exclude=$(EXCLUDE_CODE) $(CODE)
	toml-sort --in-place pyproject.toml

.PHONY: docs
docs:
	mkdocs build -s -v

.PHONY: docs-serve
docs-serve:
	mkdocs serve

.PHONY: docs-changelog
docs-changelog:
	git-changelog -o CHANGELOG.md  .

.PHONY: grpc-gen
grpc-gen:
	rm -r ${PACKAGE_PROTO_DIR}
	python -m grpc_tools.protoc -I${PROTOS} --python_out=${OUT} --grpc_python_out=${OUT} ${PROTO_DIR}/*.proto
	touch ${PACKAGE_PROTO_DIR}/__init__.py

.PHONY: publish
publish:
	poetry publish --build --no-interaction --username=$(pypi_username) --password=$(pypi_password)
