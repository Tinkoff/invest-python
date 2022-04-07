# Contributing

Спасибо за участие в проекте Tinkoff Invest!

## Быстрый старт

Рекомендуем использовать [poetry](https://pypi.org/project/poetry/)

```
pip install poetry
make install
```

### Запуск тестов

```
make test
```

### Запуск линтеров

```
make lint
```

### Запуск автоформатирования

```
make format
```

### Загрузка proto файлов

```
make download-protos
```

По дефолту загружает из ветки `main`

### Генерация клиента

```
make gen-grpc
```

Затем, добавить изменения в модули:
- tinkoff/invest/\_\_init__.py
- tinkoff/invest/async_services.py
- tinkoff/invest/schemas.py
- tinkoff/invest/services.py
