# Contributing

Спасибо за участие в проекте Tinkoff Invest!

## Быстрый старт

1. Сделайте [fork](https://github.com/Tinkoff/invest-python/fork) проекта
2. Склонируйте репозиторий на свой локальный компьютер
    ```bash
    git clone https://github.com/Tinkoff/invest-python.git
    ```
3. Создайте новую ветку для ваших изменений
    ```bash
    git checkout -b branch_name
    ```
4. Добавьте изменения и выполните команды на локальной машине (см. ниже)
   1. Установите зависимости
   2. Проверьте свой код с помощью тестов и линтеров
5. Создайте коммит своих изменений. Формат описан ниже
    ```bash
    git add .
    git commit -m "feat: add new feature"
    ```
6. Отправьте свои изменения на github
    ```bash
    git push
    ```
7. Создайте Pull Request в этот репозиторий

## Commit Message Format

Мы придерживаемся соглашений [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) для наименование коммитов.

> A specification for adding human and machine readable meaning to commit messages.

Body и Footer можно указать по желанию.

### Commit Message Header

```
<type>(<scope>): <short summary>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Commit Scope: grpc, async, mypy, schemas, sandbox
  │
  └─⫸ Commit Type: feat|fix|build|ci|docs|perf|refactor|test|chore
```

#### Type

| feat     | Features                 | A new feature                                                                                          |
|----------|--------------------------|--------------------------------------------------------------------------------------------------------|
| fix      | Bug Fixes                | A bug fix                                                                                              |
| docs     | Documentation            | Documentation only changes                                                                             |
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) |
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                              |
| perf     | Performance Improvements | A code change that improves performance                                                                |
| test     | Tests                    | Adding missing tests or correcting existing tests                                                      |
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: mypy, pip, pytest)      |
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Github Actions)                     |
| chore    | Chores                   | Other changes that don't modify src or test files                                                      |
| revert   | Reverts                  | Reverts a previous commit                                                                              |

## Выполнение команд на локальной машине

Для работы с проектом рекомендуем использовать [poetry](https://pypi.org/project/poetry/).

Также рекомендуем использовать таск раннер make.

## Установка зависимостей

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
make git-lint
```

#### Using gitlint as a commit-msg hook

```
gitlint install-hook
# To remove the hook
gitlint uninstall-hook
```

### Запуск автоформатирования

```
make format
```

### Загрузка proto файлов

```
make download-protos
```

По дефолту загружает из ветки `main`.

### Генерация клиента

```
make gen-grpc
```

Затем, добавить изменения в модули:
- tinkoff/invest/\_\_init__.py
- tinkoff/invest/async_services.py
- tinkoff/invest/schemas.py
- tinkoff/invest/services.py

### Загрузка proto файлов и генерация клиента

Можно упростить все до одной команды.

```
make gen-client
```

### Release новой версии

```
make bump-version v=<new-version>
```

Команда установит новую версию.
Далее проходим процесс ревью и устанавливаем tag коммиту в ветке мастер и отправляем на сервер.
После отправки tag-а в github `git push --tags`, будет запущена джоба `publish_pypi`.

_Стоит запускать инструкцию `make bump-version`, как только все изменения были зафиксированы в гите._
