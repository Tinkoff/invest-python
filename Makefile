PROTO_DIR = protos/tinkoff/invest/grpc
PACKAGE_PROTO_DIR = tinkoff/invest/grpc
OUT = .
PROTOS = protos

.PHONY: gen
gen:
	rm -r ${PACKAGE_PROTO_DIR}
	python -m grpc_tools.protoc -I${PROTOS} --python_out=${OUT} --grpc_python_out=${OUT} ${PROTO_DIR}/*.proto
	touch ${PACKAGE_PROTO_DIR}/__init__.py

.PHONY: publish
publish:
	poetry publish --build --no-interaction --username=$(pypi_username) --password=$(pypi_password)
