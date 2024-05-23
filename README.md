# Приложение для Хранения Книг

Веб-приложение для хранения и управления книгами. Оно позволяет пользователям загружать PDF-файлы книг, просматривать их, обновлять информацию о книгах и удалять их.

## Особенности

- Загрузка PDF-файлов книг
- Просмотр информации о загруженных книгах
- Обновление информации о книге
- Выгрузка CSV со списком книг
- Удаление книг

## Установка

1. Клонируйте этот репозиторий:

   ```bash
   git clone https://github.com/DaniilMashkov/book-storage.git
2.  Запустите с помощью docker-compose:
  ```bash
    docker-compose up --build
  ```
  Либо установите зависимости, примените миграции и запустите вручную:
  ```bash
      pip install -r requirements.txt
      alembic upgrade head
      uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```
 Приложение будет доступно по адресу
   ```bash
         http://localhost:8000/docs
   ```

##

- Запуск тестов командой
  ```bash
      pytest
  ```
- Также тесты запускаются автоматически при коммите в main [GitHub Actions](https://github.com/DaniilMashkov/FastAPI_BookStorage/actions)



