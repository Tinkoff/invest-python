# Tinkoff Invest

[![PyPI](https://img.shields.io/pypi/v/tinkoff-investments)](https://pypi.org/project/tinkoff-investments/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinkoff-investments)](https://www.python.org/downloads/)

Данный репозиторий предоставляет клиент для взаимодействия с торговой платформой [Тинькофф Инвестиции](https://www.tinkoff.ru/invest/) на языке Python.

- [Документация](https://tinkoff.github.io/invest-python/)
- [Основной репозиторий с документацией](https://github.com/Tinkoff/investAPI)
- [Документация для разработчиков](https://tinkoff.github.io/investAPI/)

## Начало работы

<!-- termynal -->

```
$ pip install tinkoff-investments
```

## Возможности

- &#9745; Синхронный и асинхронный GRPC клиент
- &#9745; Возможность отменить все заявки
- &#9745; Выгрузка истории котировок "от" и "до"
- &#9745; Кеширование данных
- &#9745; Торговая стратегия

## Как пользоваться

### Получить список аккаунтов

```python
from tinkoff.invest import Client

TOKEN = 'token'

with Client(TOKEN) as client:
    print(client.users.get_accounts())
```

### Переопределить target

В Tinkoff Invest API есть два контура - "боевой", предназначенный для исполнения ордеров на бирже и "песочница", предназначенный для тестирования API и торговых гипотез, заявки с которого не выводятся на биржу, а исполняются в эмуляторе.

Переключение между контурами реализовано через target, INVEST_GRPC_API - "боевой", INVEST_GRPC_API_SANDBOX - "песочница"

```python
from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API

TOKEN = 'token'

with Client(TOKEN, target=INVEST_GRPC_API) as client:
    print(client.users.get_accounts())
```

> :warning: **Не публикуйте токены в общедоступные репозитории**
<br/>

Остальные примеры доступны в [examples](https://github.com/Tinkoff/invest-python/tree/main/examples).

## Contribution

Для тех, кто хочет внести свои изменения в проект.

- [CONTRIBUTING](https://github.com/Tinkoff/invest-python/blob/main/CONTRIBUTING.md)

## License

Лицензия [The Apache License](https://github.com/Tinkoff/invest-python/blob/main/LICENSE).
