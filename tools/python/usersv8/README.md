# Загрузчик с сайта users.v8

## Использование утилиты

Установка

```sh
pip install usersv8
```

Использование

```sh
usersv8 platform client --out-file client.rar --username my-username --password my-password
usersv8 --help
usersv8 platform --help
```

## Разработка

### Запуск тестов

```sh
python -m unittest
```

Тесты требуют установки следующих переменных окружения:

- USERS_USERNAME - логин от сайта [users.v8](https://users.v8.1c.ru)
- USERS_PASSWORD - пароль от сайта [users.v8](https://users.v8.1c.ru)

Для запуска тестов через VS Code переменные окружения можно указать в .env файле корневой директории. Пример [".env.example"](./.env.example)

### Настройки линтера и форматера

#### Форматер - black

Без настроек

#### Линтер - flake8

Настройки в ["setup.cfg"](./setup.cfg)

#### Общие

Настройки для VS Code в ["settings.example.json"](./.vscode/settings.example.json)
