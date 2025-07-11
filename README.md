# Hero API
## Проект предоставляет API для работы с данными о супергероях, интегрируясь с SuperHero API.

## 🚀 Установка и запуск

## Требования

### Технологии и ЯП 
- Python 3.12+
- [Docker](https://hub.docker.com/r/microsoft/mssql-server)

### Установка зависимостей
- У вас должен быть установлен менеджер зависимостей [uv](https://github.com/astral-sh/uv)
```shell
uv init
```

```shell
uv install
```

### Переменные окружения
- Скопируйте файл .env.example и замените данные на ваши:
```shell
cp .env.example .env
```

### Запуск проекта
```shell
docker-compose up -d --build
```

## 📚 API Endpoints

### POST /hero/

- Добавляет героя в базу данных, предварительно проверяя его наличие в SuperHero API.

**Обязательные параметры:**
1. `name` - Имя героя

### GET /hero/

- Возвращает список героев с возможностью фильтрации.

**Обязательные параметры:**
1. `name` - точное совпадение имени
2. `intelligence` - фильтр по интеллекту (форматы: 100, >=80, <50)
3. `strength` - фильтр по силе
4. `speed` - фильтр по скорости
5. `power` - фильтр по мощи
6. `page` - номер страницы (по умолчанию 1)
7. `page_size` - размер страницы (по умолчанию 20, максимум 100)

## 🧪 Тестирование

### Требования

- Убедитесь, что тестовая БД запущена:
```shell
docker run -d --name test-postgres \
  -e POSTGRES_USER=test \
  -e POSTGRES_PASSWORD=test \
  -e POSTGRES_DB=test_db \
  -p 5433:5432 \
  postgres:16
```
- Поменяйте переменные окружения в файле pytest.ini

### Запустите тесты
```shell
pytest tests/ -v
```
