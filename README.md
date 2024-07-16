## API Платформы для самообучения

**Backend-часть SPA веб-приложения для самообучения.**

- Размещение разделов и материалов для обучения
- Составление тестов
- Прохождение тестов и сбор статистики

### Стек технологий:

- `Python`
- `Django`
- `DRF`
- `PostgreSQL`

## Содержание

<details>
<summary>Инструкция по развертыванию проекта</summary>

#### 1. Скопируйте проект любым удобным способом.

#### 2. Установите зависимости из файла pyproject.toml

#### 3. Создайте базу данных

#### 4. Настройте переменные окружения:

1. Создайте файл `.env` в корневой директории
2. Скопируйте в него содержимое файла `.env_example` и подставьте свои значения

#### 5. Примените миграции

```
python manage.py migrate
```

#### 6. Запустите сервер

```
python manage.py runserver
```

</details>

<details>
<summary>Инструкция по развертыванию проекта с использованием Docker</summary>

#### 1. Скопируйте проект любым удобным способом.

#### 2. Настройте переменные окружения:

1. Создайте файл `.env` в корневой директории
2. Скопируйте в него содержимое файла `.env_example` и подставьте свои значения

#### 3. Запустите команду, для сборки контейнеров в docker-compose

```
docker-compose up -d --build
```

Чтобы попасть в контейнер с приложением и выполнять в нем команды, введите

```
docker exec -it <'id_контейнера' или имя 'app'> bash
```

</details>

<details>
<summary>Использование</summary>

#### 1. Административная панель:

Для доступа к админке создайте суперпользователя

1. Для создания суперпользователя (админа) выполните команду
    ```
    python manage.py csu
    ```
   E-mail и пароль суперпользоветеля для входа в админку вы можете посмотреть в
   файле `/users/management/commands/csu.py`. При желании, вы можете задать свои e-mail и пароль

2. Откройте административную панель по адресу http://localhost:8000/admin/ и введите e-mail и пароль суперпользователя

#### 2. Фикстуры:

В директории ./fixtures есть .json файлы, которые можно использовать для наполнения базы данных

```
python manage.py loaddata ..._data.json
```

#### 2. Принцип работы:

- Разделы, материалы, списки вопросов и ответов формируются по CRUD через запросы к серверу или через админку.

- Доступ к функционалу доступен только авторизованным пользователям.

- Тестирование пользователей осуществляется через GET-запрос на адрес http://localhost:8000/testing/int:pk/ , где pk -
  это id списка с вопросами по теме. Далее нужно отправить PATCH-запрос с телом вида {"answer_id": id}, где id - это
  айдишник ответа, который выбран как правильный. В конце тестирования будет выведена статистика с количеством
  правильных ответов.
- Чтобы пройти тестирование еще раз, нужно отправить POST-запрос на адрес http://localhost:8000/testing/int:pk/reset/
  для сброса результатов прошлого тестирования.

</details>

## Документация

Документация по API доступна по адресам:

- Swagger - http://127.0.0.1:8000/docs/
- Redoc - http://127.0.0.1:8000/redoc/
